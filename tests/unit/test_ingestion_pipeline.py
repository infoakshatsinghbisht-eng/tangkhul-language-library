"""Comprehensive unit and integration tests for permission-aware document ingestion pipeline."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from pypdf import PdfWriter

from tangkhul_lib.cli import main
from tangkhul_lib.core.models import (
    DocumentChunk,
    IngestedDocument,
    ManifestRecord,
    VocabularyEntry,
)
from tangkhul_lib.ingestion.pipeline import (
    DocumentIngestionPipeline,
    SourcePermissionChecker,
)
from tangkhul_lib.ingestion.text_extraction import (
    ExtractedPage,
    ExtractionResult,
    TextExtractor,
    assess_extraction_quality,
    segment_into_chunks,
)
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    DocumentRepository,
)


@pytest.fixture
def mem_db() -> DatabaseManager:
    """Provide an isolated in-memory DatabaseManager."""
    db = DatabaseManager(":memory:")
    db.initialize_schema()
    return db


@pytest.fixture
def sample_pdf_with_text(tmp_path: Path) -> Path:
    """Create a synthetic PDF with a valid digital text stream."""
    pdf_path = tmp_path / "sample_text.pdf"
    pdf_data = (
        b"%PDF-1.4\n"
        b"1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj\n"
        b"3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        b"4 0 obj <</Length 44>> stream\n"
        b"BT /F1 12 Tf 50 250 Td (Tangkhul Tuitam) Tj ET\n"
        b"endstream endobj\n"
        b"5 0 obj <</Type /Font /Subtype /Type1 /BaseFont /Helvetica>> endobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000056 00000 n \n"
        b"0000000111 00000 n \n0000000234 00000 n \n0000000327 00000 n \n"
        b"trailer <</Size 6 /Root 1 0 R>>\nstartxref\n404\n%%EOF\n"
    )
    pdf_path.write_bytes(pdf_data)
    return pdf_path


@pytest.fixture
def sample_blank_pdf(tmp_path: Path) -> Path:
    """Create a synthetic blank PDF representing an un-OCR'd scan."""
    pdf_path = tmp_path / "blank_scan.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_blank_page(width=200, height=200)
    with pdf_path.open("wb") as f:
        writer.write(f)
    return pdf_path


@pytest.fixture
def sample_encrypted_pdf(tmp_path: Path) -> Path:
    """Create a synthetic encrypted/password-protected PDF."""
    pdf_path = tmp_path / "encrypted.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=150, height=150)
    writer.encrypt("secure_password")
    with pdf_path.open("wb") as f:
        writer.write(f)
    return pdf_path


@pytest.fixture
def sample_docx(tmp_path: Path) -> Path:
    """Create a synthetic Word (.docx) document."""
    docx_path = tmp_path / "sample.docx"
    xml_content = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        "<w:body>\n"
        "<w:p><w:r><w:t>Tangkhul Tuitam Khare.</w:t></w:r></w:p>\n"
        "<w:p><w:r><w:t>I ramli shim kathara sakashak thotna.</w:t></w:r></w:p>\n"
        "</w:body>\n"
        "</w:document>"
    )
    with zipfile.ZipFile(docx_path, "w") as z:
        z.writestr("word/document.xml", xml_content)
    return docx_path


def test_txt_and_markdown_extraction(tmp_path: Path) -> None:
    """Test text extraction from plain text and markdown with page boundaries."""
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text(
        "--- Page 1 ---\n"
        "Tangkhul Tuitam Khare.\n"
        "I ramli shim kathara sakashak thotna.\n\n"
        "--- Page 2 ---\n"
        "Zingkum kashakwui Tangkhul khararchan wari.\n",
        encoding="utf-8",
    )

    extractor = TextExtractor()
    res = extractor.extract_from_txt_file(txt_file, source_id="TEST-001")
    assert res.status == "extracted"
    assert res.page_count == 2
    assert res.pages[0].page_number == 1
    assert "Tangkhul Tuitam Khare." in res.pages[0].text
    assert res.pages[1].page_number == 2
    assert "Zingkum kashakwui" in res.pages[1].text
    assert res.word_count > 0


def test_txt_latin1_fallback(tmp_path: Path) -> None:
    """Test non-UTF8 text file fallback and warning generation."""
    txt_file = tmp_path / "latin1.txt"
    txt_file.write_bytes(b"Tangkhul \xe9cole")  # latin-1 byte

    extractor = TextExtractor()
    res = extractor.extract_from_txt_file(txt_file, source_id="TEST-002")
    assert res.status == "extracted"
    assert any("latin-1 fallback" in w for w in res.warnings)


def test_docx_extraction(sample_docx: Path) -> None:
    """Test pure-Python docx extraction without external python-docx library."""
    extractor = TextExtractor()
    res = extractor.extract_from_docx_file(sample_docx, source_id="TEST-DOCX")
    assert res.status == "extracted"
    assert "Tangkhul Tuitam Khare." in res.full_text
    assert "I ramli shim kathara" in res.full_text


def test_docx_corrupt_file(tmp_path: Path) -> None:
    """Test error handling for corrupted/non-zip docx files."""
    bad_docx = tmp_path / "corrupt.docx"
    bad_docx.write_bytes(b"not a zip file content")

    extractor = TextExtractor()
    res = extractor.extract_from_docx_file(bad_docx, source_id="TEST-CORRUPT")
    assert res.status == "failed"
    assert any("Corrupted DOCX" in w for w in res.warnings)


def test_pdf_digital_extraction(sample_pdf_with_text: Path) -> None:
    """Test extracting digital text from a PDF."""
    extractor = TextExtractor()
    res = extractor.extract_from_pdf_file(sample_pdf_with_text, source_id="TEST-PDF")
    assert res.status in {"extracted", "partial"}
    assert res.page_count == 1
    assert "Tangkhul Tuitam" in res.full_text


def test_pdf_scanned_quality_detection(sample_blank_pdf: Path) -> None:
    """Test detection of scanned PDFs lacking a digital text layer."""
    extractor = TextExtractor()
    res = extractor.extract_from_pdf_file(sample_blank_pdf, source_id="TEST-SCAN")
    assert res.ocr_status == "ocr_needed"
    assert res.status == "needs_review"
    assert any("OCR is required" in w for w in res.warnings)


def test_pdf_encrypted_graceful_handling(sample_encrypted_pdf: Path) -> None:
    """Test handling of password-encrypted PDFs without crash."""
    extractor = TextExtractor()
    res = extractor.extract_from_pdf_file(sample_encrypted_pdf, source_id="TEST-ENC")
    assert "password-encrypted" in str(res.notes) or any(
        "encrypted" in w.lower() for w in res.warnings
    )


def test_assess_extraction_quality_replacement_chars() -> None:
    """Test quality assessment flags replacement characters and low char density."""
    pages = [
        ExtractedPage(page_number=1, text="Text with \ufffd corrupted \ufffd glyphs."),
    ]
    status, warnings, ocr_status = assess_extraction_quality(pages, "txt")
    assert any("replacement character" in w for w in warnings)


def test_source_permission_checker_rules() -> None:
    """Test permission validation logic across all tiers."""
    # 1. Permitted tier
    rec_pub = ManifestRecord(
        id="BK-001", resource_type="books", title="Pub",
        permission_status="public_domain", verification_status="verified"
    )
    eval_pub = SourcePermissionChecker.evaluate(rec_pub)
    assert eval_pub.is_eligible is True
    assert eval_pub.skip_reason is None

    rec_auth = ManifestRecord(
        id="BK-002", resource_type="books", title="Auth",
        permission_status="community_authorized", verification_status="verified"
    )
    assert SourcePermissionChecker.evaluate(rec_auth).is_eligible is True

    # 2. Pending permission
    rec_pending = ManifestRecord(
        id="BK-003", resource_type="books", title="Pending",
        permission_status="pending", verification_status="verified"
    )
    eval_pending = SourcePermissionChecker.evaluate(rec_pending)
    assert eval_pending.is_eligible is False
    assert "pending" in str(eval_pending.skip_reason)

    # 3. Restricted permission
    rec_restricted = ManifestRecord(
        id="BK-004", resource_type="books", title="Restricted",
        permission_status="restricted", verification_status="verified"
    )
    eval_restricted = SourcePermissionChecker.evaluate(rec_restricted)
    assert eval_restricted.is_eligible is False
    assert "restricted" in str(eval_restricted.skip_reason)

    # 4. Candidate needs_review
    rec_cand = ManifestRecord(
        id="BK-005", resource_type="books", title="Cand",
        permission_status="permitted", verification_status="needs_review"
    )
    eval_cand = SourcePermissionChecker.evaluate(rec_cand)
    assert eval_cand.is_eligible is False
    assert "needs_review" in str(eval_cand.skip_reason)


def test_segment_into_chunks() -> None:
    """Test paragraph segmentation, deterministic chunk IDs, and content hashes."""
    extraction = ExtractionResult(
        source_id="TEST-SRC",
        file_path=Path("sample.txt"),
        pages=[
            ExtractedPage(page_number=1, text="Paragraph one text.\n\nParagraph two text."),
            ExtractedPage(page_number=2, text="Paragraph three text."),
        ],
    )
    chunks = segment_into_chunks(
        extraction,
        doc_id="DOC-TEST",
        source_id="TEST-SRC",
        permission_status="permitted",
        verification_status="verified",
    )
    assert len(chunks) == 3
    assert chunks[0].id == "CHK-DOC-TEST-p001-c0001"
    assert chunks[0].page_number == 1
    assert chunks[0].text == "Paragraph one text."
    assert chunks[0].content_hash != ""
    assert chunks[2].page_number == 2
    assert chunks[2].text == "Paragraph three text."


def test_document_repository_crud_and_fts(mem_db: DatabaseManager) -> None:
    """Test DocumentRepository persistence, chunk queries, and FTS5 BM25 search."""
    repo = DocumentRepository(mem_db)

    doc = IngestedDocument(
        id="DOC-TEST-001",
        source_id="BK-HIST-001",
        source_title="Tangkhul History Treatise",
        creator="Pettigrew",
        publication_year=1918,
        file_path="/data/test.txt",
        file_name="test.txt",
        file_hash="abc123hash",
        file_size_bytes=1024,
        file_format="txt",
        extraction_method="text_utf8",
        extraction_timestamp="2026-10-25T12:00:00Z",
        extraction_status="extracted",
        page_count=1,
        char_count=100,
        word_count=15,
        permission_status="public_domain",
        verification_status="verified",
    )

    chunks = [
        DocumentChunk(
            id="CHK-DOC-TEST-001-p001-c0001",
            document_id=doc.id,
            source_id=doc.source_id,
            page_number=1,
            section_heading="Chapter 1",
            chunk_index=1,
            text="I ramli shim kathara sakashak thotna Tangkhul.",
            char_count=45,
            word_count=7,
            content_hash="hash1",
            permission_status="public_domain",
            verification_status="verified",
        )
    ]

    repo.add_document(doc, chunks)

    # Retrieval
    saved_doc = repo.get_document(doc.id)
    assert saved_doc is not None
    assert saved_doc.source_title == "Tangkhul History Treatise"
    assert repo.get_document_by_source_id("BK-HIST-001") is not None
    assert repo.get_document_by_hash("abc123hash") is not None

    # Chunks retrieval
    saved_chunks = repo.get_chunks(doc.id)
    assert len(saved_chunks) == 1
    assert saved_chunks[0].text == "I ramli shim kathara sakashak thotna Tangkhul."

    # FTS5 search
    fts_results = repo.search_chunks_fts("kathara")
    assert len(fts_results) >= 1
    assert fts_results[0][0].id == chunks[0].id

    # Rebuild FTS5 index
    count = repo.rebuild_chunks_fts_index()
    assert count == 1

    # Deletion
    repo.delete_document(doc.id)
    assert repo.get_document(doc.id) is None
    assert len(repo.get_chunks(doc.id)) == 0


def test_restricted_chunks_shielded_from_fts(mem_db: DatabaseManager) -> None:
    """Ensure restricted chunks are never inserted into document_chunks_fts."""
    repo = DocumentRepository(mem_db)

    doc = IngestedDocument(
        id="DOC-RESTRICTED",
        source_id="DIC-RESTRICTED",
        source_title="Secret Rites",
        file_path="/data/secret.txt",
        file_name="secret.txt",
        file_hash="hash_secret",
        permission_status="restricted",
        verification_status="needs_review",
    )

    chunks = [
        DocumentChunk(
            id="CHK-SECRET-001",
            document_id=doc.id,
            source_id=doc.source_id,
            page_number=1,
            chunk_index=1,
            text="Secret esoteric passage that should never be indexed.",
            content_hash="hash_p",
            permission_status="restricted",
            verification_status="needs_review",
        )
    ]

    repo.add_document(doc, chunks)
    fts_results = repo.search_chunks_fts("esoteric")
    assert len(fts_results) == 0


def test_pipeline_dry_run_and_idempotency(mem_db: DatabaseManager, tmp_path: Path) -> None:
    """Test pipeline preview, dry-run, and idempotent re-ingestion behavior."""
    sample_file = tmp_path / "book.txt"
    sample_file.write_text(
        "--- Page 1 ---\n"
        "Tangkhul Tuitam Khare.\n"
        "I ramli shim kathara sakashak thotna.\n",
        encoding="utf-8",
    )

    pipeline = DocumentIngestionPipeline(mem_db)
    # Register an eligible manifest record
    manifest = ManifestRecord(
        id="BK-TEST-ELIGIBLE",
        resource_type="books",
        title="Tangkhul Primer 1918",
        creator="William Pettigrew",
        year=1918,
        permission_status="public_domain",
        verification_status="verified",
        local_path=str(sample_file),
    )
    pipeline.manifest_repo.add(manifest)

    # 1. Preview
    preview = pipeline.preview_document(sample_file, source_id="BK-TEST-ELIGIBLE")
    assert preview["chunk_count"] == 1
    assert preview["word_count"] > 0

    # 2. Dry run
    res_dry = pipeline.ingest_document("BK-TEST-ELIGIBLE", file_path=sample_file, dry_run=True)
    assert res_dry["success"] is True
    assert res_dry["dry_run"] is True
    # DB must remain empty after dry run
    assert pipeline.doc_repo.get_document_by_source_id("BK-TEST-ELIGIBLE") is None

    # 3. Real ingestion
    res_real = pipeline.ingest_document("BK-TEST-ELIGIBLE", file_path=sample_file)
    assert res_real["success"] is True
    assert res_real.get("already_ingested") is not True
    doc = pipeline.doc_repo.get_document_by_source_id("BK-TEST-ELIGIBLE")
    assert doc is not None

    # 4. Repeated ingestion without changes -> already_ingested
    res_repeat = pipeline.ingest_document("BK-TEST-ELIGIBLE", file_path=sample_file)
    assert res_repeat["success"] is True
    assert res_repeat.get("already_ingested") is True

    # 5. Repeated ingestion with force=True -> reprocessed
    res_force = pipeline.ingest_document("BK-TEST-ELIGIBLE", file_path=sample_file, force=True)
    assert res_force["success"] is True
    assert res_force.get("already_ingested") is not True


def test_pipeline_vocabulary_integration(mem_db: DatabaseManager, tmp_path: Path) -> None:
    """Test candidate vocabulary extraction links without fabricating meanings."""
    sample_file = tmp_path / "vocab_sample.txt"
    sample_file.write_text(
        "Tangkhul khararchan wari wui kachotna.\n",
        encoding="utf-8",
    )

    pipeline = DocumentIngestionPipeline(mem_db)
    # Add an existing verified entry
    pipeline.vocab_repo.add(
        VocabularyEntry(
            id="VOCAB-EXISTING-001",
            headword="khararchan",
            meanings=["legend", "folk narrative"],
            translations_en=["folk tale"],
            verification_status="verified",
        )
    )

    manifest = ManifestRecord(
        id="BK-VOCAB-001",
        resource_type="books",
        title="Oral Traditions",
        permission_status="community_authorized",
        verification_status="verified",
        local_path=str(sample_file),
    )
    pipeline.manifest_repo.add(manifest)

    res = pipeline.ingest_document("BK-VOCAB-001", file_path=sample_file)
    assert res["success"] is True

    # Check that existing entry khararchan got extended provenance without losing verified status
    updated_entry = pipeline.vocab_repo.get_by_id("VOCAB-EXISTING-001")
    assert updated_entry is not None
    assert updated_entry.verification_status == "verified"
    assert any(p.source_id == "BK-VOCAB-001" for p in updated_entry.provenance)

    # Check candidate entries created for other tokens (e.g., wari)
    # have unverified status & empty meanings
    all_vocab = pipeline.vocab_repo.list_all()
    wari_entries = [e for e in all_vocab if e.headword.lower() == "wari"]
    if wari_entries:
        assert wari_entries[0].verification_status == "unverified"
        assert len(wari_entries[0].meanings) == 0  # No fabricated meanings!


def test_cli_ingest_smoke(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI ingest subcommand arguments and smoke execution."""
    # 1. Help
    try:
        main(["ingest", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "--list-sources" in captured.out
    assert "--preview" in captured.out
    assert "--dry-run" in captured.out

    # 2. List sources
    code_list = main(["ingest", "--list-sources"])
    assert code_list == 0
    cap_list = capsys.readouterr()
    assert "DOCUMENT INGESTION SOURCE ELIGIBILITY REPORT" in cap_list.out
    assert "ELIGIBLE SOURCES" in cap_list.out
    assert "INELIGIBLE / SKIPPED SOURCES" in cap_list.out

    # 3. Preview fixture file
    code_prev = main(["ingest", "--preview", "tests/fixtures/sample_tangkhul_book.txt"])
    assert code_prev == 0
    cap_prev = capsys.readouterr()
    assert "DOCUMENT EXTRACTION PREVIEW" in cap_prev.out
    assert "sample_tangkhul_book.txt" in cap_prev.out

    # 4. Preview non-existent file
    code_bad = main(["ingest", "--preview", "non_existent_file.pdf"])
    assert code_bad == 1
    assert "not found" in capsys.readouterr().err

    code_skip = main(
        ["ingest", "--source-id", "BK-TLS-001", "--file", "tests/fixtures/sample_tangkhul_book.txt"]
    )
    assert code_skip == 0
    assert "Ingestion skipped" in capsys.readouterr().out
