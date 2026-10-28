"""Unit tests for Tangkhul Prayers, Rituals, Ceremonies & Clan System Digitization."""

from __future__ import annotations

import json
from pathlib import Path

import pypdf

from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"
BUNDLED_DIR = PROJECT_ROOT / "src" / "tangkhul_lib" / "data"
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "culture"
MANIFEST_FILE = PROJECT_ROOT / "data" / "manifests" / "culture.jsonl"
DB_PATH = PROJECT_ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_PATH = BUNDLED_DIR / "tangkhul_corpus.sqlite"

EXPECTED_HERITAGE_MODULES = [
    {
        "id": "CULT-PRAY-001",
        "file_prefix": "tangkhul_prayers_and_invocations",
        "title_keyword": "Prayers",
        "category": "ritual",
        "key_field": "prayer_sections",
    },
    {
        "id": "CULT-RIT-003",
        "file_prefix": "tangkhul_rituals_and_ceremonies",
        "title_keyword": "Rituals",
        "category": "ritual",
        "key_field": "ceremonial_cycles",
    },
    {
        "id": "CULT-SOC-001",
        "file_prefix": "tangkhul_clans_kinship_and_social_structure",
        "title_keyword": "Clan",
        "category": "custom",
        "key_field": "major_clans",
    },
]


def test_individual_prayers_rituals_clans_json_exports() -> None:
    """Verify individual JSON exports exist in both exports and bundled directories."""
    for mod in EXPECTED_HERITAGE_MODULES:
        json_name = f"{mod['file_prefix']}.json"
        exp_path = EXPORTS_DIR / json_name
        bnd_path = BUNDLED_DIR / json_name

        assert exp_path.exists(), f"Missing export JSON: {exp_path}"
        assert bnd_path.exists(), f"Missing bundled JSON: {bnd_path}"

        with open(exp_path, encoding="utf-8") as f:
            data = json.load(f)

        assert data["id"] == mod["id"]
        assert mod["title_keyword"] in data["title"]
        assert data["language"] == "Tangkhul"
        assert mod["key_field"] in data

        with open(bnd_path, encoding="utf-8") as f:
            bnd_data = json.load(f)
        assert bnd_data == data


def test_individual_prayers_rituals_clans_pdf_exports() -> None:
    """Verify individual PDF documents are valid and have readable pages."""
    for mod in EXPECTED_HERITAGE_MODULES:
        pdf_name = f"{mod['file_prefix']}.pdf"
        pdf_path = EXPORTS_DIR / pdf_name

        assert pdf_path.exists(), f"Missing PDF export: {pdf_path}"
        reader = pypdf.PdfReader(str(pdf_path))
        assert len(reader.pages) >= 1
        page_text = reader.pages[0].extract_text()
        assert len(page_text) > 100


def test_consolidated_prayers_rituals_clans_master_encyclopedia() -> None:
    """Verify master consolidated encyclopedia JSON and PDF."""
    cons_json = EXPORTS_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.json"
    cons_pdf = EXPORTS_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.pdf"
    bnd_json = BUNDLED_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.json"

    assert cons_json.exists()
    assert cons_pdf.exists()
    assert bnd_json.exists()

    with open(cons_json, encoding="utf-8") as f:
        data = json.load(f)

    assert "Tangkhul Prayers, Rituals & Clan System" in data["title"]
    assert "modules" in data
    assert len(data["modules"]) == 3
    assert "prayers_and_invocations" in data["modules"]
    assert "rituals_and_ceremonies" in data["modules"]
    assert "clans_and_social_structure" in data["modules"]

    reader = pypdf.PdfReader(str(cons_pdf))
    assert len(reader.pages) >= 1


def test_raw_culture_monographs_integrity() -> None:
    """Verify raw culture monograph text files exist and have rich content."""
    for mod in EXPECTED_HERITAGE_MODULES:
        manifest_records = [
            json.loads(line)
            for line in MANIFEST_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rec = next(r for r in manifest_records if r["id"] == mod["id"])
        raw_file = PROJECT_ROOT / rec["local_path"]

        assert raw_file.exists(), f"Missing raw file: {raw_file}"
        lines = raw_file.read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 50, f"Raw file {raw_file} too short: {len(lines)} lines"
        content = "\n".join(lines)
        assert f"RESOURCE IDENTIFIER: {mod['id']}" in content
        assert "CULTURAL HERITAGE PRESERVATION NOTICE" in content


def test_manifest_registration_and_db_sync() -> None:
    """Verify culture manifest registration and SQLite persistence."""
    assert MANIFEST_FILE.exists()
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    rec_by_id = {r["id"]: r for r in records}
    assert len(records) == 35

    for mod in EXPECTED_HERITAGE_MODULES:
        mid = mod["id"]
        assert mid in rec_by_id
        rec = rec_by_id[mid]
        assert rec["resource_type"] == "culture"
        assert rec["verification_status"] == "verified"

    for db_p in [DB_PATH, BUNDLED_DB_PATH]:
        if not db_p.exists():
            continue
        db_mgr = DatabaseManager(db_p)
        repo = CultureRepository(db_mgr)
        for mod in EXPECTED_HERITAGE_MODULES:
            r = repo.get_by_id(mod["id"])
            assert r is not None, f"Missing record {mod['id']} in {db_p.name}"
            assert mod["title_keyword"] in r.title
            assert r.original_text is not None
            assert len(r.original_text) > 50
