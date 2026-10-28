"""Integration tests for culture storage, SQLite schema, repository CRUD, and manifest sync."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository, ManifestRepository


def test_database_culture_crud_and_manifest_sync(tmp_path: Path) -> None:
    db_file = tmp_path / "culture_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    culture_repo = CultureRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)

    rec = CulturalRecord(
        id="CULT-FEST-001",
        title="Luira Phanit",
        local_name="Luira",
        alternate_names=["Lui-Phanit"],
        category="festival",
        subcategory="agricultural",
        translation_en="Seed-Sowing Festival",
        village="Hunphun / Ukhrul",
        dialect="Hunphun / Ukhrul",
        year=1911,
        source_id="Hodson-1911-Ch3",
        source_title="The Naga Tribes of Manipur (Hodson 1911)",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
        notes="Spring seed-sowing festival.",
    )
    culture_repo.add(rec)

    # 1. Verify retrieval from SQLite culture table
    retrieved = culture_repo.get_by_id("CULT-FEST-001")
    assert retrieved is not None
    assert retrieved.id == "CULT-FEST-001"
    assert retrieved.title == "Luira Phanit"
    assert retrieved.category == "festival"
    assert retrieved.village == "Hunphun / Ukhrul"
    assert "Lui-Phanit" in retrieved.alternate_names

    # 2. Verify manifest_records sync
    manifest_rec = manifest_repo.get_by_id("CULT-FEST-001")
    assert manifest_rec is not None
    assert manifest_rec.title == "Luira Phanit"
    assert manifest_rec.resource_type == "culture"
    assert manifest_rec.dialect == "Hunphun / Ukhrul"

    # 3. Test list_all and list_by_category
    all_recs = culture_repo.list_all()
    assert len(all_recs) == 1
    festivals = culture_repo.list_by_category("festival")
    assert len(festivals) == 1
    customs = culture_repo.list_by_category("custom")
    assert len(customs) == 0

    # 4. Test count
    assert culture_repo.count() == 1

    # 5. Test update
    updated = culture_repo.update("CULT-FEST-001", {"notes": "Updated note during test."})
    assert updated.notes == "Updated note during test."
    refetched = culture_repo.get_by_id("CULT-FEST-001")
    assert refetched is not None
    assert refetched.notes == "Updated note during test."

    # 6. Test token persistence
    tokens = [
        {"word_form": "Luira", "page_or_section": "p. 80", "context_sentence": "Luira phanit"},
        {"word_form": "Phanit", "page_or_section": "p. 80", "context_sentence": "Luira phanit"},
    ]
    culture_repo.save_tokens("CULT-FEST-001", tokens)
    saved_tokens = culture_repo.get_extracted_tokens("CULT-FEST-001")
    assert len(saved_tokens) == 2
    assert saved_tokens[0]["word_form"] == "Luira"
