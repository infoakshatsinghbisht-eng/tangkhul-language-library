"""Unit tests for Tangkhul Sacred Scriptures & Classical Epics Digitization.

Validates:
- Holy Bible, Ramayana, Mahabharata, Bhagavad Gita JSON and PDF exports
- Consolidated scriptures and epics collection
- Raw literature monograph text files
- Manifest registration and database persistence
"""

from __future__ import annotations

import json
from pathlib import Path

import pypdf

from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"
BUNDLED_DIR = PROJECT_ROOT / "src" / "tangkhul_lib" / "data"
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "literature"
MANIFEST_FILE = PROJECT_ROOT / "data" / "manifests" / "literature.jsonl"
DB_PATH = PROJECT_ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_PATH = BUNDLED_DIR / "tangkhul_corpus.sqlite"

EXPECTED_WORKS = [
    {
        "id": "LIT-SCRP-001",
        "file_prefix": "tangkhul_holy_bible_scriptures",
        "title_keyword": "Varivara",
        "category": "sacred_scripture",
        "sections_key": "sections",
    },
    {
        "id": "LIT-EPIC-001",
        "file_prefix": "tangkhul_ramayana_epic",
        "title_keyword": "Ramwui",
        "category": "epic_poetry",
        "sections_key": "kandas",
    },
    {
        "id": "LIT-EPIC-002",
        "file_prefix": "tangkhul_mahabharata_epic",
        "title_keyword": "Mahabharata",
        "category": "epic_poetry",
        "sections_key": "parvas",
    },
    {
        "id": "LIT-EPIC-003",
        "file_prefix": "tangkhul_bhagavad_gita",
        "title_keyword": "Bhagavad Gita",
        "category": "philosophical_classic",
        "sections_key": "chapters",
    },
]


def test_individual_scriptures_and_epics_json_exports() -> None:
    """Verify individual JSON exports exist in both exports and bundled directories."""
    for work in EXPECTED_WORKS:
        json_name = f"{work['file_prefix']}.json"
        exp_path = EXPORTS_DIR / json_name
        bnd_path = BUNDLED_DIR / json_name

        assert exp_path.exists(), f"Missing export JSON: {exp_path}"
        assert bnd_path.exists(), f"Missing bundled JSON: {bnd_path}"

        with open(exp_path, encoding="utf-8") as f:
            data = json.load(f)

        assert data["id"] == work["id"]
        assert work["title_keyword"] in data["title"]
        assert data["language"] == "Tangkhul"
        assert work["sections_key"] in data

        # Check bundled copy matches
        with open(bnd_path, encoding="utf-8") as f:
            bnd_data = json.load(f)
        assert bnd_data == data


def test_individual_scriptures_and_epics_pdf_exports() -> None:
    """Verify individual PDF documents are valid and have readable pages."""
    for work in EXPECTED_WORKS:
        pdf_name = f"{work['file_prefix']}.pdf"
        pdf_path = EXPORTS_DIR / pdf_name

        assert pdf_path.exists(), f"Missing PDF export: {pdf_path}"
        reader = pypdf.PdfReader(str(pdf_path))
        assert len(reader.pages) >= 1
        page_text = reader.pages[0].extract_text()
        assert len(page_text) > 100


def test_consolidated_scriptures_and_epics_collection() -> None:
    """Verify master consolidated collection JSON and PDF."""
    cons_json = EXPORTS_DIR / "tangkhul_sacred_scriptures_and_epics_collection.json"
    cons_pdf = EXPORTS_DIR / "tangkhul_sacred_scriptures_and_epics_collection.pdf"
    bnd_json = BUNDLED_DIR / "tangkhul_sacred_scriptures_and_epics_collection.json"

    assert cons_json.exists()
    assert cons_pdf.exists()
    assert bnd_json.exists()

    with open(cons_json, encoding="utf-8") as f:
        data = json.load(f)

    assert "Tangkhul Sacred Scriptures" in data["title"]
    assert "works" in data
    assert len(data["works"]) == 4

    # Verify all 4 work IDs are present
    work_ids = {w["id"] for w in data["works"].values()}
    assert work_ids == {"LIT-SCRP-001", "LIT-EPIC-001", "LIT-EPIC-002", "LIT-EPIC-003"}

    # Verify consolidated PDF
    reader = pypdf.PdfReader(str(cons_pdf))
    assert len(reader.pages) >= 1


def test_raw_literature_monographs_integrity() -> None:
    """Verify raw literature text files exist and meet minimum line count requirements."""
    for work in EXPECTED_WORKS:
        raw_file = RAW_DIR / f"{work['id']}.txt"
        assert raw_file.exists(), f"Missing raw file: {raw_file}"
        lines = raw_file.read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 50, f"Raw file {raw_file} too short: {len(lines)} lines"
        content = "\n".join(lines)
        assert work["title_keyword"] in content
        assert "INDIGENOUS TANGKHUL LITERARY TEXT" in content
        assert "LITERARY THEMES & CULTURAL SIGNIFICANCE" in content


def test_manifest_registration() -> None:
    """Verify scriptures and epics are properly registered in literature.jsonl."""
    assert MANIFEST_FILE.exists()
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    rec_by_id = {r["id"]: r for r in records}
    assert len(records) == 60

    for work in EXPECTED_WORKS:
        wid = work["id"]
        assert wid in rec_by_id, f"Missing manifest entry: {wid}"
        rec = rec_by_id[wid]
        assert work["title_keyword"] in rec["title"]
        assert rec["resource_type"] == "literature"
        assert rec["verification_status"] == "verified"
        assert rec["access_status"] in ("metadata_only", "open")
        assert rec["language"] == "Tangkhul"


def test_database_persistence() -> None:
    """Verify scriptures and epics are queryable in both SQLite databases."""
    for db_p in [DB_PATH, BUNDLED_DB_PATH]:
        if not db_p.exists():
            continue
        db_mgr = DatabaseManager(db_p)
        repo = LiteratureRepository(db_mgr)
        for work in EXPECTED_WORKS:
            rec = repo.get_by_id(work["id"])
            assert rec is not None, f"Missing DB record {work['id']} in {db_p.name}"
            assert work["title_keyword"] in rec.title
            assert rec.original_text is not None
            assert len(rec.original_text) > 50
