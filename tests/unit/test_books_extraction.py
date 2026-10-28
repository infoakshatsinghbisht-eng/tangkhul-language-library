"""Unit tests for text extraction and candidate vocabulary extraction."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.books.extractor import BookTextExtractor
from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.exceptions import PermissionRestrictedError, ResourceNotFoundError
from tangkhul_lib.ingestion.text_extraction import TextExtractor


def test_text_extractor_with_page_markers() -> None:
    raw = """
    --- Page 1 ---
    Tangkhul Tuitam Khare.
    Shim kathara sakashak thotna.

    --- Page 2 ---
    Zingkum kashakwui Tangkhul khararchan wari.
    """
    extractor = TextExtractor()
    res = extractor.extract_from_text(raw, source_id="TEST-001")
    assert res.source_id == "TEST-001"
    assert len(res.pages) == 2
    assert res.pages[0].page_number == 1
    assert "Tangkhul Tuitam Khare" in res.pages[0].text
    assert res.pages[1].page_number == 2
    assert "khararchan" in res.pages[1].text
    assert res.status == "extracted"


def test_text_extractor_plain_without_markers(tmp_path: Path) -> None:
    sample_file = tmp_path / "plain_text.txt"
    sample_file.write_text("Tangkhul language documentation.", encoding="utf-8")

    extractor = TextExtractor()
    res = extractor.extract_from_txt_file(sample_file, source_id="BK-001")
    assert len(res.pages) == 1
    assert res.pages[0].page_number == 1
    assert res.pages[0].text == "Tangkhul language documentation."


def test_text_extractor_missing_file() -> None:
    extractor = TextExtractor()
    with pytest.raises(ResourceNotFoundError):
        extractor.extract_from_file(Path("/non/existent/path/file.txt"))


def test_text_extractor_scanned_file_requires_review(tmp_path: Path) -> None:
    scanned_file = tmp_path / "scan.png"
    scanned_file.write_bytes(b"\x89PNG\r\n\x1a\n")

    extractor = TextExtractor()
    res = extractor.extract_from_file(scanned_file, source_id="SCAN-001")
    assert res.status == "needs_review"
    assert res.extraction_method == "ocr_pending_review"


def test_pdf_extraction_with_pypdf(tmp_path: Path) -> None:
    try:
        import pypdf

        pdf_path = tmp_path / "test.pdf"
        writer = pypdf.PdfWriter()
        # Create a blank page
        writer.add_blank_page(width=200, height=200)
        with pdf_path.open("wb") as f:
            writer.write(f)

        extractor = TextExtractor()
        res = extractor.extract_from_pdf_file(pdf_path, source_id="PDF-001")
        assert len(res.pages) == 1
        assert res.pages[0].page_number == 1
        # Blank page has no text, so status is needs_review
        assert res.status == "needs_review"
    except ImportError:
        pytest.skip("pypdf not installed")


def test_book_extractor_permission_enforcement(tmp_path: Path) -> None:
    sample_file = tmp_path / "restricted_book.txt"
    sample_file.write_text("Protected content.", encoding="utf-8")

    restricted_book = BookRecord(
        id="BK-RESTRICTED",
        title="Restricted Copyrighted Book",
        local_file_path=str(sample_file),
        permission_status="restricted",
        access_status="restricted",
    )
    b_extractor = BookTextExtractor()
    assert not b_extractor.is_extraction_permitted(restricted_book)

    with pytest.raises(PermissionRestrictedError, match="not permitted"):
        b_extractor.extract_book_text(restricted_book)


def test_vocabulary_candidates_generation(tmp_path: Path) -> None:
    text_content = """--- Page 1 ---
Tangkhul Tuitam Khare.
I ramli shim kathara sakashak thotna.

--- Page 2 ---
Zingkum kashakwui Tangkhul khararchan wari.
Haora kachon pamli chitharan thot khangatei lei.
"""
    file_path = tmp_path / "sample_book.txt"
    file_path.write_text(text_content, encoding="utf-8")

    book = BookRecord(
        id="BK-TEST-001",
        title="Tangkhul Reader Volume I",
        publication_year=2020,
        local_file_path=str(file_path),
        permission_status="permitted",
        access_status="full_text_available",
    )

    b_extractor = BookTextExtractor()
    extraction = b_extractor.extract_book_text(book)
    raw_tokens, candidate_vocab = b_extractor.extract_vocabulary_candidates(book, extraction)

    assert len(raw_tokens) > 0
    assert len(candidate_vocab) > 0

    # Ensure unverified status and no fabricated meanings/translations
    for entry in candidate_vocab:
        assert entry.verification_status == "unverified"
        assert entry.meanings == []
        assert entry.translations_en == []
        assert len(entry.provenance) >= 1
        prov = entry.provenance[0]
        assert prov.source_id == "BK-TEST-001"
        assert prov.recorded_year == 2020
        assert "p. " in (prov.page_or_section or "")

    # Check that headwords like 'shim' and 'haora' or 'khararchan' exist
    headwords = {e.headword.lower() for e in candidate_vocab}
    assert "shim" in headwords or "tangkhul" in headwords or "khararchan" in headwords
