"""Unit tests for Tangkhul literary records, metadata validation, and catalogue operations."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import (
    ManifestValidationError,
    PermissionDeniedError,
)
from tangkhul_lib.literature.catalogue import LiteratureCatalogue
from tangkhul_lib.literature.models import (
    VALID_LITERARY_GENRES,
    VALID_TEXT_AVAILABILITY,
    LiteraryRecord,
)


def test_valid_literary_record_creation() -> None:
    rec = LiteraryRecord(
        id="LIT-TEST-001",
        title="Shimreishang Kala Maitonphi",
        alternate_titles=["Maitonphi Shimreishang Khararchan"],
        original_title="Shimreishang Kala Maitonphi",
        title_translation="Shimreishang and Maitonphi",
        work_type="ballad",
        genres=["ballad", "oral_narrative"],
        author="Traditional",
        storyteller="Tangkhul Elders of Phungcham",
        publication_year=1982,
        composition_date="c. 17th century",
        edition="First Edition",
        publisher="Central Institute of Indian Languages",
        publication_place="Mysore",
        language="Tangkhul",
        dialect="Phungcham",
        village="Phungcham",
        region="Northern Tangkhul",
        book_id="BK-CIIL-003",
        source_id="CIIL-TFL-1982",
        source_title="Tangkhul Folk Literature (Arokianathan 1982)",
        source_page="pp. 12-45",
        license="CC-BY-NC-SA-4.0",
        license_evidence="Institutional research publication under CIIL archival terms.",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
        text_availability="metadata_only",
        notes="Synthetic test record based on authentic Phungcham romantic ballad.",
    )
    rec.validate()
    assert rec.id == "LIT-TEST-001"
    assert rec.work_type == "ballad"
    assert rec.work_type in VALID_LITERARY_GENRES
    assert rec.text_availability in VALID_TEXT_AVAILABILITY

    d = rec.to_dict()
    assert d["id"] == "LIT-TEST-001"
    assert d["work_type"] == "ballad"
    assert d["storyteller"] == "Tangkhul Elders of Phungcham"

    reconstructed = LiteraryRecord.from_dict(d)
    assert reconstructed.id == rec.id
    assert reconstructed.title == rec.title
    assert reconstructed.publication_year == 1982
    assert reconstructed.book_id == "BK-CIIL-003"


def test_literary_record_validation_failures() -> None:
    # Missing ID
    with pytest.raises(ManifestValidationError, match="missing required field 'id'"):
        LiteraryRecord(id="", title="Test Title", work_type="poem").validate()

    # Missing Title
    with pytest.raises(ManifestValidationError, match="missing required field 'title'"):
        LiteraryRecord(id="LIT-001", title="   ", work_type="poem").validate()

    # Missing Work Type
    with pytest.raises(ManifestValidationError, match="missing required field 'work_type'"):
        LiteraryRecord(id="LIT-001", title="Valid Title", work_type="").validate()

    # Invalid Work Type
    with pytest.raises(ManifestValidationError, match="invalid work_type"):
        LiteraryRecord(
            id="LIT-001",
            title="Valid Title",
            work_type="fantasy_epic",
        ).validate()

    # Invalid Text Availability
    with pytest.raises(ManifestValidationError, match="invalid text_availability"):
        LiteraryRecord(
            id="LIT-001",
            title="Valid Title",
            work_type="poem",
            text_availability="unknown_format",
        ).validate()

    # Invalid Permission Status
    with pytest.raises(ManifestValidationError, match="invalid permission_status"):
        LiteraryRecord(
            id="LIT-001",
            title="Valid Title",
            work_type="poem",
            permission_status="unauthorized_status",
        ).validate()

    # Invalid Access Status
    with pytest.raises(ManifestValidationError, match="invalid access_status"):
        LiteraryRecord(
            id="LIT-001",
            title="Valid Title",
            work_type="poem",
            access_status="forbidden_access",
        ).validate()

    # Invalid Verification Status
    with pytest.raises(ManifestValidationError, match="invalid verification_status"):
        LiteraryRecord(
            id="LIT-001",
            title="Valid Title",
            work_type="poem",
            verification_status="certified_gold",
        ).validate()


def test_literary_record_alias_and_coercion_in_from_dict() -> None:
    data = {
        "id": "LIT-ALIAS-001",
        "title": "Folktale of the Tiger and Monkey",
        "category": "folk_tale",
        "year": "1995",
        "creator": "Khutingla Zimik",
        "translation_en": "Tiger and Monkey Story",
        "source_identifier": "TLS-1995-01",
        "genres": ["folk_tale", "fable"],
    }
    rec = LiteraryRecord.from_dict(data)
    assert rec.work_type == "folk_tale"
    assert rec.publication_year == 1995
    assert rec.author == "Khutingla Zimik"
    assert rec.title_translation == "Tiger and Monkey Story"
    assert rec.identifier == "TLS-1995-01"
    assert "fable" in rec.genres


def test_candidate_token_extraction_and_vocabulary_conversion() -> None:
    rec = LiteraryRecord(
        id="LIT-VOC-TEST-001",
        title="Ava Ram Leishat",
        original_title="Ava Ram Leishat",
        work_type="poem",
        author="Luingam A. Shimray",
        original_text="Iramwui ngalungli leikashi mayonser, shongza khararchan.",
        translation_text="In our ancestral land love blossoms everywhere.",
        permission_status="public_domain",
        access_status="metadata_only",
        text_availability="excerpt",
        verification_status="verified",
    )
    tokens = rec.extract_candidate_tokens(min_length=3)
    assert len(tokens) > 0
    assert "iramwui" in tokens
    assert "leikashi" in tokens
    assert "shongza" in tokens
    assert "khararchan" in tokens

    candidates = rec.to_candidate_vocabulary_entries()
    assert len(candidates) > 0
    for cand in candidates:
        assert cand.verification_status == "unverified"
        assert len(cand.provenance) == 1
        prov = cand.provenance[0]
        assert prov.source_id == "LIT-VOC-TEST-001"
        assert prov.resource_type == "literature"
        assert prov.context_sentence == rec.original_text


def test_permission_denial_on_restricted_text_extraction() -> None:
    restricted_rec = LiteraryRecord(
        id="LIT-RESTR-001",
        title="Copyrighted Modern Novel Excerpt",
        work_type="novel",
        original_text="Confidential modern literary prose.",
        permission_status="restricted",
        access_status="restricted",
        text_availability="restricted",
    )
    with pytest.raises(PermissionDeniedError, match="Extraction prohibited"):
        restricted_rec.extract_candidate_tokens()

    with pytest.raises(PermissionDeniedError, match="Extraction prohibited"):
        restricted_rec.to_candidate_vocabulary_entries()


def test_literature_catalogue_search_and_filters() -> None:
    manifest_path = Path("data/manifests/literature.jsonl")
    catalogue = LiteratureCatalogue.load_from_manifest(manifest_path)
    assert len(catalogue) >= 20

    # 1. Search by title
    results = catalogue.search_works(query="Ava Ram")
    assert len(results) >= 1
    assert any(r.id == "LIT-POEM-001" for r in results)

    # 2. Filter by work_type
    poems = catalogue.search_works(work_type="poem")
    assert len(poems) >= 4
    assert all("poem" == p.work_type or "poem" in p.genres for p in poems)

    # 3. Filter by author
    luingam_works = catalogue.search_works(author="Luingam")
    assert len(luingam_works) >= 1
    assert any("Luingam A. Shimray" in (w.author or "") for w in luingam_works)

    # 4. Filter by genre
    ballads = catalogue.search_works(genre="ballad")
    assert len(ballads) >= 1
    assert any(b.id == "LIT-FLK-001" for b in ballads)

    # 5. Filter by verification status
    needs_review = catalogue.search_works(verification_status="needs_review")
    assert len(needs_review) >= 1
    assert any(w.id == "LIT-CAND-001" for w in needs_review)


def test_duplicate_and_adaptation_detection() -> None:
    manifest_path = Path("data/manifests/literature.jsonl")
    catalogue = LiteratureCatalogue.load_from_manifest(manifest_path)

    # Detect adaptations of Shimreishang Kala Maitonphi
    # (Ballad LIT-FLK-001 and Play LIT-PLAY-002)
    flk_001 = catalogue.get_work("LIT-FLK-001")
    assert flk_001 is not None
    related = catalogue.find_related_works(flk_001)
    assert len(related) >= 1
    assert any(r.id == "LIT-PLAY-002" for r in related)

    # Find duplicates with distinct editions
    dupes = catalogue.find_likely_duplicates(flk_001)
    # Should identify LIT-PLAY-002 as sharing root title without merging them
    assert any(d.id == "LIT-PLAY-002" for d in dupes)


def test_catalogue_report_and_exports(tmp_path: Path) -> None:
    manifest_path = Path("data/manifests/literature.jsonl")
    catalogue = LiteratureCatalogue.load_from_manifest(manifest_path)

    report = catalogue.generate_catalogue_report()
    assert report["total_works"] >= 20
    assert "metadata_only_count" in report
    assert "full_text_permitted_count" in report
    assert "by_genre" in report
    assert "by_verification_status" in report

    # Export to JSONL
    jsonl_out = tmp_path / "literature_export.jsonl"
    count_jsonl = catalogue.export_to_jsonl(jsonl_out, include_restricted=False)
    assert count_jsonl > 0
    assert jsonl_out.exists()

    # Export to CSV
    csv_out = tmp_path / "literature_export.csv"
    count_csv = catalogue.export_to_csv(csv_out, include_restricted=False)
    assert count_csv == count_jsonl
    assert csv_out.exists()


def test_literature_raw_files_integrity() -> None:
    """Verify that all 55 raw literature text files exist and have substantial content."""
    raw_dir = Path("data/raw/literature")
    assert raw_dir.is_dir()

    manifest_path = Path("data/manifests/literature.jsonl")
    with open(manifest_path, encoding="utf-8") as f:
        manifest_records = [json.loads(line) for line in f if line.strip()]

    assert len(manifest_records) == 60
    for rec in manifest_records:
        rel_path = rec.get("local_path")
        assert rel_path, f"Manifest record {rec['id']} missing local_path"
        raw_file = Path(rel_path)
        assert raw_file.exists(), f"Raw file {raw_file} does not exist"
        lines = raw_file.read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 50, f"Raw file {raw_file} has only {len(lines)} lines"
        content = "\n".join(lines)
        if rec["id"] == "LIT-RIDD-003":
            assert "300 TANGKHUL FOLK RIDDLES" in content
            assert "LITERARY THEMES & MOTIFS" in content
        elif rec["id"] == "LIT-RIDD-004":
            assert "100 ADDITIONAL TANGKHUL FOLK RIDDLES" in content
            assert "LITERARY THEMES & CULTURAL SIGNIFICANCE" in content
        elif rec["id"] in ("LIT-SCRP-001", "LIT-EPIC-001", "LIT-EPIC-002", "LIT-EPIC-003"):
            assert "INDIGENOUS TANGKHUL LITERARY TEXT" in content
            assert "LITERARY THEMES & CULTURAL SIGNIFICANCE" in content
        else:
            assert "INDIGENOUS TANGKHUL LITERARY TEXT" in content
            assert "ENGLISH POETIC TRANSLATION" in content
            assert "LITERARY THEMES & MOTIFS" in content


def test_literature_exports_integrity() -> None:
    """Verify consolidated and individual JSON/PDF exports for literature."""
    import pypdf

    exports_dir = Path("data/exports")
    lit_exports_dir = exports_dir / "literature"
    bundled_dir = Path("src/tangkhul_lib/data")

    # Consolidated JSON
    cons_json = exports_dir / "literature.json"
    bundled_json = bundled_dir / "literature.json"
    assert cons_json.exists()
    assert bundled_json.exists()

    with open(cons_json, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 60

    # Master Compendium PDF
    master_pdf = exports_dir / "literature.pdf"
    assert master_pdf.exists()
    reader = pypdf.PdfReader(str(master_pdf))
    assert len(reader.pages) == 63  # 3 cover/TOC + 60 literature monograph pages

    # Individual files
    assert lit_exports_dir.is_dir()
    for rec in data:
        lid = rec["id"]
        ind_json = lit_exports_dir / f"{lid}.json"
        assert ind_json.exists()
        with open(ind_json, encoding="utf-8") as f:
            ind_data = json.load(f)
        assert ind_data["id"] == lid

        ind_pdf = lit_exports_dir / f"{lid}.pdf"
        assert ind_pdf.exists()
        ind_reader = pypdf.PdfReader(str(ind_pdf))
        assert len(ind_reader.pages) >= 1


def test_database_literature_persistence() -> None:
    """Verify that all 60 literature records are persisted in SQLite database."""
    from tangkhul_lib.storage.database import DatabaseManager
    from tangkhul_lib.storage.repositories import LiteratureRepository

    for db_path in [
        Path("data/database/tangkhul_corpus.sqlite"),
        Path("src/tangkhul_lib/data/tangkhul_corpus.sqlite"),
    ]:
        if not db_path.exists():
            continue
        db_mgr = DatabaseManager(db_path)
        lit_repo = LiteratureRepository(db_mgr)
        assert lit_repo.count() >= 60

        rec = lit_repo.get_by_id("LIT-FLK-001")
        assert rec is not None
        assert rec.title == "Shimreishang Kala Maitonphi"
        assert rec.original_text is not None
        assert "Shimreishang" in rec.original_text
        assert rec.translation_text is not None

        # Verify Batch 2 record
        rec2 = lit_repo.get_by_id("LIT-PLAY-003")
        assert rec2 is not None
        assert rec2.title == "Asang Eina Aton"
        assert rec2.original_text is not None
        assert "Asang" in rec2.original_text

        # Verify Batch 3 record
        rec3 = lit_repo.get_by_id("LIT-FLK-014")
        assert rec3 is not None
        assert rec3.title == "Kasomwoshi Kala Khaying-Sha"
        assert rec3.original_text is not None
        assert "Kasomwoshi" in rec3.original_text

        # Verify 300 Riddles Encyclopedia
        rec4 = lit_repo.get_by_id("LIT-RIDD-003")
        assert rec4 is not None
        assert "300 Tangkhul" in rec4.title

        # Verify 100 Additional Riddles
        rec5 = lit_repo.get_by_id("LIT-RIDD-004")
        assert rec5 is not None
        assert "100 Additional" in rec5.title

        # Verify Holy Bible
        rec_bible = lit_repo.get_by_id("LIT-SCRP-001")
        assert rec_bible is not None
        assert "Holy Bible" in rec_bible.title or "Varivara" in rec_bible.title

        # Verify Ramayana
        rec_ramayana = lit_repo.get_by_id("LIT-EPIC-001")
        assert rec_ramayana is not None
        assert "Ramwui" in rec_ramayana.title or "Ramayana" in rec_ramayana.title

        # Verify Mahabharata
        rec_mhb = lit_repo.get_by_id("LIT-EPIC-002")
        assert rec_mhb is not None
        assert "Mahabharata" in rec_mhb.title

        # Verify Bhagavad Gita
        rec_gita = lit_repo.get_by_id("LIT-EPIC-003")
        assert rec_gita is not None
        assert "Bhagavad Gita" in rec_gita.title

