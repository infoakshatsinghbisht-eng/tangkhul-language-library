"""Unit tests for Tangkhul historical records, metadata validation, and catalogue management."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import (
    ManifestValidationError,
    PermissionDeniedError,
)
from tangkhul_lib.history.catalogue import HistoryCatalogue
from tangkhul_lib.history.models import (
    VALID_EVIDENCE_TYPES,
    VALID_HISTORY_RECORD_TYPES,
    HistoricalRecord,
)


def test_valid_historical_record_creation() -> None:
    rec = HistoricalRecord(
        id="HIST-TEST-001",
        title="Establishment of Hunphun Settlement",
        alternate_titles=["Hunphun Village Founding"],
        record_type="place",
        summary="Founding of the ancestral settlement of Hunphun.",
        event_date="c. 14th century",
        sort_year=1350,
        period="Pre-colonial",
        place="Hunphun / Ukhrul",
        village="Hunphun",
        dialect="Hunphun / Ukhrul",
        permission_status="public_domain",
        access_status="metadata_only",
        evidence_type="oral_tradition",
        confidence=0.85,
        verification_status="verified",
        notes="Synthetic test record for settlement history.",
    )
    rec.validate()
    assert rec.id == "HIST-TEST-001"
    assert rec.record_type == "place"
    assert rec.record_type in VALID_HISTORY_RECORD_TYPES
    assert rec.evidence_type in VALID_EVIDENCE_TYPES

    d = rec.to_dict()
    assert d["id"] == "HIST-TEST-001"
    assert d["record_type"] == "place"

    reconstructed = HistoricalRecord.from_dict(d)
    assert reconstructed.id == rec.id
    assert reconstructed.title == rec.title
    assert reconstructed.sort_year == 1350


def test_historical_record_validation_failures() -> None:
    # Missing ID
    with pytest.raises(ManifestValidationError, match="missing required field 'id'"):
        HistoricalRecord(id="", title="Event", record_type="historical_event").validate()

    # Missing Title
    with pytest.raises(ManifestValidationError, match="missing required field 'title'"):
        HistoricalRecord(id="HIST-001", title="   ", record_type="historical_event").validate()

    # Missing Record Type
    with pytest.raises(ManifestValidationError, match="missing required field 'record_type'"):
        HistoricalRecord(id="HIST-001", title="Valid Title", record_type="").validate()

    # Invalid Record Type
    with pytest.raises(ManifestValidationError, match="invalid record_type"):
        HistoricalRecord(
            id="HIST-001",
            title="Valid Title",
            record_type="mythology",
        ).validate()

    # Invalid Evidence Type
    with pytest.raises(ManifestValidationError, match="invalid evidence_type"):
        HistoricalRecord(
            id="HIST-001",
            title="Valid Title",
            record_type="historical_event",
            evidence_type="rumor",
        ).validate()

    # Invalid Permission Status
    with pytest.raises(ManifestValidationError, match="invalid permission_status"):
        HistoricalRecord(
            id="HIST-001",
            title="Valid Title",
            record_type="historical_event",
            permission_status="invalid_status",
        ).validate()

    # Invalid Verification Status
    with pytest.raises(ManifestValidationError, match="invalid verification_status"):
        HistoricalRecord(
            id="HIST-001",
            title="Valid Title",
            record_type="historical_event",
            verification_status="certified",
        ).validate()


def test_all_record_types_valid() -> None:
    for rtype in VALID_HISTORY_RECORD_TYPES:
        rec = HistoricalRecord(
            id=f"HIST-TYPE-{rtype[:4].upper()}",
            title=f"Sample {rtype}",
            record_type=rtype,
            permission_status="public_domain",
            access_status="metadata_only",
            verification_status="verified",
        )
        rec.validate()
        assert rec.record_type == rtype


def test_approximate_dates_and_uncertainty() -> None:
    rec = HistoricalRecord(
        id="HIST-DATE-001",
        title="Circa Event",
        record_type="historical_event",
        event_date="c. 1917–1918 (WWI Service)",
        sort_year=1917,
        period="World War I",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    rec.validate()
    assert rec.event_date == "c. 1917–1918 (WWI Service)"
    assert rec.sort_year == 1917


def test_contradictory_accounts_support() -> None:
    rec = HistoricalRecord(
        id="HIST-CONF-001",
        title="Disputed Chronology Event",
        record_type="historical_event",
        event_date="1919 or 1920",
        sort_year=1919,
        contradictory_accounts=[
            "Colonial report records arrival in October 1919.",
            "Local village oral account recalls spring 1920.",
        ],
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="needs_review",
    )
    rec.validate()
    assert len(rec.contradictory_accounts) == 2
    assert "Colonial report" in rec.contradictory_accounts[0]


def test_candidate_vocabulary_generation() -> None:
    rec = HistoricalRecord(
        id="HIST-VOCAB-001",
        title="Pettigrew Arrival in Hunphun",
        record_type="historical_event",
        original_text="Hunphun Awunga Raihao khipak-eili Rev. Pettigrew phungchan.",
        place="Hunphun / Ukhrul",
        village="Hunphun",
        people_involved=["Rev. William Pettigrew", "Awunga Raihao"],
        source_id="HIST-SRC-001",
        source_page="42",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    candidates = rec.extract_vocabulary_candidates()
    words = [c["word_form"] for c in candidates]
    # Check that key toponyms and words are harvested
    assert "Hunphun" in words
    assert "Awunga" in words
    assert "phungchan" in words

    # Check candidate metadata
    for c in candidates:
        assert c["source_id"] == "HIST-VOCAB-001"
        assert c["page_or_section"] == "42"
        assert c["extraction_method"] in {
            "historical_entity_extraction",
            "historical_text_extraction",
        }


def test_catalogue_management_and_querying(tmp_path: Path) -> None:
    manifest_file = tmp_path / "test_history.jsonl"
    r1 = HistoricalRecord(
        id="HIST-CAT-001",
        title="Foundation of Tangkhul Long",
        record_type="community_history",
        event_date="1935",
        sort_year=1935,
        period="Pre-Independence",
        place="Ukhrul",
        village="Ukhrul",
        people_involved=["R.S. Ruichumhao"],
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r2 = HistoricalRecord(
        id="HIST-CAT-002",
        title="Battle of Sangshak",
        alternate_titles=["Sangshak Defense"],
        record_type="historical_event",
        event_date="March 1944",
        sort_year=1944,
        period="World War II",
        place="Sangshak",
        village="Sangshak",
        related_records=["HIST-CAT-001"],
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r3 = HistoricalRecord(
        id="HIST-CAT-003",
        title="Restricted Historical Memoir",
        record_type="oral_history",
        event_date="1950",
        sort_year=1950,
        permission_status="restricted",
        access_status="restricted",
        verification_status="needs_review",
    )

    manifest_file.write_text(
        "\n".join(
            [
                r1.to_manifest_dict().__repr__().replace("'", '"'),  # simple JSON representation
            ]
        ),
        encoding="utf-8",
    )

    cat = HistoryCatalogue()
    cat.add_record(r1)
    cat.add_record(r2)
    cat.add_record(r3)

    assert len(cat) == 3
    assert cat.get_record("HIST-CAT-001") == r1
    assert cat.get_record("NON-EXISTENT") is None

    # Search by query
    found = cat.search_records(query="Sangshak")
    assert len(found) == 1
    assert found[0].id == "HIST-CAT-002"

    # Search by type
    events = cat.search_records(record_type="historical_event")
    assert len(events) == 1
    assert events[0].id == "HIST-CAT-002"

    # Search by period
    ww2 = cat.search_records(period="World War II")
    assert len(ww2) == 1
    assert ww2[0].id == "HIST-CAT-002"

    # Timeline ordering
    timeline = cat.get_timeline(start_year=1930, end_year=1945)
    assert len(timeline) == 2
    assert timeline[0].sort_year == 1935
    assert timeline[1].sort_year == 1944

    # Restricted exclusion by default
    res = cat.search_records(include_restricted=False)
    assert all(r.permission_status != "restricted" for r in res)

    # Restricted access check
    with pytest.raises(PermissionDeniedError, match="restricted"):
        cat.get_record("HIST-CAT-003", allow_restricted=False)


def test_catalogue_duplicate_detection() -> None:
    cat = HistoryCatalogue()
    r1 = HistoricalRecord(
        id="HIST-DUP-001",
        title="Makhel Dispersal Tradition",
        alternate_titles=["Makhel Migration"],
        record_type="migration",
        source_id="SRC-MAKHEL",
        source_page="15",
        sort_year=1200,
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r2 = HistoricalRecord(
        id="HIST-DUP-002",
        title="Makhel Dispersal Tradition",
        alternate_titles=["Makhel Migration Route"],
        record_type="migration",
        source_id="SRC-MAKHEL",
        source_page="15",
        sort_year=1200,
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    cat.add_record(r1)
    cat.add_record(r2)

    dupes = cat.find_duplicates()
    assert len(dupes) >= 1
    pair = dupes[0]
    assert pair[0].title == pair[1].title


def test_catalogue_export_and_report(tmp_path: Path) -> None:
    cat = HistoryCatalogue()
    rec = HistoricalRecord(
        id="HIST-EXP-001",
        title="Pettigrew Grammar Publication",
        record_type="language_history",
        event_date="1918",
        sort_year=1918,
        place="Ukhrul",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    cat.add_record(rec)

    json_export = tmp_path / "export.json"
    cat.export_json(json_export)
    assert json_export.exists()
    assert "HIST-EXP-001" in json_export.read_text(encoding="utf-8")

    csv_export = tmp_path / "export.csv"
    cat.export_csv(csv_export)
    assert csv_export.exists()
    assert "HIST-EXP-001" in csv_export.read_text(encoding="utf-8")

    report = cat.get_history_report()
    assert report["total_records"] == 1
    assert "language_history" in report["by_type"]


def test_history_raw_files_integrity() -> None:
    """Verify that all 32 raw history files exist in data/raw/history/ with substantial content."""
    project_root = Path(__file__).resolve().parent.parent.parent
    raw_dir = project_root / "data" / "raw" / "history"
    manifest_file = project_root / "data" / "manifests" / "history.jsonl"

    import json

    with manifest_file.open(encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    assert len(records) == 32

    for rec in records:
        hid = rec["id"]
        raw_path = raw_dir / f"{hid}.txt"
        assert raw_path.is_file(), f"Missing raw file for {hid}"
        lines = raw_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 50, f"Raw file {hid} has fewer than 50 lines ({len(lines)})"
        assert hid in lines[2]


def test_history_exports_integrity() -> None:
    """Verify that consolidated and individual JSON/PDF exports exist and are valid."""
    import json

    import pypdf

    project_root = Path(__file__).resolve().parent.parent.parent
    exports_dir = project_root / "data" / "exports"
    hist_exports_dir = exports_dir / "history"

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "history.json"
    assert consolidated_json.is_file()
    with consolidated_json.open(encoding="utf-8") as f:
        items = json.load(f)
    assert len(items) == 32

    # 2. Master Compendium PDF
    compendium_pdf = exports_dir / "history.pdf"
    assert compendium_pdf.is_file()
    reader = pypdf.PdfReader(str(compendium_pdf))
    assert len(reader.pages) == 33
    assert "Tangkhul Historical Chronicles & Gazetteer" in reader.pages[0].extract_text()

    # 3. Individual JSON and PDF documents
    for item in items:
        hid = item["id"]
        ind_json = hist_exports_dir / f"{hid}.json"
        assert ind_json.is_file(), f"Missing individual JSON for {hid}"
        with ind_json.open(encoding="utf-8") as f:
            ind_data = json.load(f)
        assert ind_data["id"] == hid
        assert "indigenous_tangkhul_chronicle" in ind_data
        assert len(ind_data.get("indigenous_tangkhul_chronicle", [])) >= 2

        ind_pdf = hist_exports_dir / f"{hid}.pdf"
        assert ind_pdf.is_file(), f"Missing individual PDF for {hid}"
        ind_reader = pypdf.PdfReader(str(ind_pdf))
        assert len(ind_reader.pages) == 1
        assert hid in ind_reader.pages[0].extract_text()


def test_database_history_persistence() -> None:
    """Verify that all 32 historical records are persisted in SQLite."""
    import sqlite3

    project_root = Path(__file__).resolve().parent.parent.parent
    db_path = project_root / "data" / "database" / "tangkhul_corpus.sqlite"
    assert db_path.is_file()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM history")
    hist_count = cur.fetchone()[0]
    assert hist_count == 32

    conn.close()


