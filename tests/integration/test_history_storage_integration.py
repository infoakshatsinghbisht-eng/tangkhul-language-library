"""Integration tests for history storage, SQLite schema, repository CRUD, and manifest sync."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import HistoryRepository, ManifestRepository


def test_database_history_crud_and_manifest_sync(tmp_path: Path) -> None:
    db_file = tmp_path / "history_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    history_repo = HistoryRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)

    rec = HistoricalRecord(
        id="HIST-TEST-EVT-001",
        title="Arrival of William Pettigrew in Hunphun",
        alternate_titles=["Pettigrew Ukhrul Mission Founding"],
        record_type="historical_event",
        summary="Rev. William Pettigrew established first mission school in Hunphun.",
        original_text="Hunphun Awunga Raihao khipak-eili Rev. Pettigrew phungchan.",
        translation_en="Rev. Pettigrew arrived in Hunphun under the chiefship of Raihao.",
        event_date="February 1896",
        sort_year=1896,
        period="Colonial Era",
        place="Hunphun / Ukhrul",
        village="Hunphun",
        dialect="Hunphun / Ukhrul",
        people_involved=["Rev. William Pettigrew", "Awunga Raihao"],
        source_id="HIST-HODSON-1911",
        source_title="The Naga Tribes of Manipur (Hodson 1911)",
        source_page="p. 42",
        permission_status="public_domain",
        access_status="metadata_only",
        evidence_type="archival_record",
        confidence=0.95,
        verification_status="verified",
        notes="Foundational milestone for modern Tangkhul education.",
    )
    history_repo.add(rec)

    # 1. Verify retrieval from SQLite history table
    retrieved = history_repo.get_by_id("HIST-TEST-EVT-001")
    assert retrieved is not None
    assert retrieved.id == "HIST-TEST-EVT-001"
    assert retrieved.title == "Arrival of William Pettigrew in Hunphun"
    assert retrieved.record_type == "historical_event"
    assert retrieved.sort_year == 1896
    assert retrieved.place == "Hunphun / Ukhrul"
    assert "Awunga Raihao" in retrieved.people_involved
    assert "Pettigrew Ukhrul Mission Founding" in retrieved.alternate_titles

    # 2. Verify manifest_records sync
    manifest_rec = manifest_repo.get_by_id("HIST-TEST-EVT-001")
    assert manifest_rec is not None
    assert manifest_rec.title == "Arrival of William Pettigrew in Hunphun"
    assert manifest_rec.resource_type == "history"
    assert manifest_rec.year == 1896
    assert manifest_rec.dialect == "Hunphun / Ukhrul"

    # 3. Test list_all and list_by_type
    all_recs = history_repo.list_all()
    assert len(all_recs) == 1
    events = history_repo.list_by_type("historical_event")
    assert len(events) == 1
    people = history_repo.list_by_type("person")
    assert len(people) == 0

    # 4. Test list_by_period and list_by_place
    period_recs = history_repo.list_by_period("Colonial Era")
    assert len(period_recs) == 1
    place_recs = history_repo.list_by_place("Hunphun")
    assert len(place_recs) == 1

    # 5. Test get_timeline
    timeline = history_repo.get_timeline(start_year=1890, end_year=1900)
    assert len(timeline) == 1
    assert timeline[0].sort_year == 1896

    # 6. Test count
    assert history_repo.count() == 1

    # 7. Test update
    updated = history_repo.update(
        "HIST-TEST-EVT-001", {"notes": "Updated note during test."}
    )
    assert updated.notes == "Updated note during test."
    refetched = history_repo.get_by_id("HIST-TEST-EVT-001")
    assert refetched is not None
    assert refetched.notes == "Updated note during test."

    # 8. Test token persistence
    tokens = [
        {
            "word_form": "Awunga",
            "page_or_section": "p. 42",
            "context_sentence": "Awunga Raihao",
        },
        {
            "word_form": "Hunphun",
            "page_or_section": "p. 42",
            "context_sentence": "Hunphun village",
        },
    ]
    history_repo.save_tokens("HIST-TEST-EVT-001", tokens)
    saved_tokens = history_repo.get_extracted_tokens("HIST-TEST-EVT-001")
    assert len(saved_tokens) == 2
    assert saved_tokens[0]["word_form"] == "Awunga"
