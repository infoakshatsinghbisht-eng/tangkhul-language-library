"""Integration tests for DictionaryRepository and SQLite persistence."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    DictionaryRepository,
    ManifestRepository,
    VocabularyRepository,
)


def test_database_dictionary_crud_and_manifest_sync(tmp_path: Path) -> None:
    db_file = tmp_path / "dict_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    dict_repo = DictionaryRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    # 1. Add source record
    src = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        alternate_titles=["Ukhrul Dialect Dictionary"],
        authors=["William Pettigrew"],
        publication_year=1918,
        publisher="Assam Secretariat Printing Office",
        languages=["Tangkhul", "English"],
        language_pair="Tangkhul-English",
        dialect="Ukhrul",
        source_type="grammar_dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    dict_repo.add(src)

    # Verify retrieval
    retrieved = dict_repo.get_by_id("DIC-HIST-001")
    assert retrieved is not None
    assert retrieved.id == "DIC-HIST-001"
    assert retrieved.title == "Tangkhul Naga Grammar and Dictionary"
    assert retrieved.authors == ["William Pettigrew"]
    assert retrieved.language_pair == "Tangkhul-English"

    # Verify manifest synchronization
    man_rec = manifest_repo.get_by_id("DIC-HIST-001")
    assert man_rec is not None
    assert man_rec.title == "Tangkhul Naga Grammar and Dictionary"
    assert man_rec.resource_type == "dictionaries"
    assert man_rec.creator == "William Pettigrew"

    # Update metadata
    updated = dict_repo.update("DIC-HIST-001", {"notes": "Updated historical notes."})
    assert updated.notes == "Updated historical notes."
    refetched = dict_repo.get_by_id("DIC-HIST-001")
    assert refetched is not None
    assert refetched.notes == "Updated historical notes."

    # 2. Add dictionary entries
    ent1 = DictionaryEntryRecord(
        id="DIC-HIST-001-ENT-0001",
        dictionary_id="DIC-HIST-001",
        headword="khamatha",
        definitions_en=["good", "beautiful"],
        part_of_speech="adjective",
        page_or_section="p. 312",
        permission_status="public_domain",
        verification_status="verified",
    )
    ent2 = DictionaryEntryRecord(
        id="DIC-HIST-001-ENT-0002",
        dictionary_id="DIC-HIST-001",
        headword="akha",
        definitions_en=["fish"],
        part_of_speech="noun",
        page_or_section="p. 280",
        permission_status="public_domain",
        verification_status="verified",
    )
    dict_repo.add_entry(ent1)
    dict_repo.add_entry(ent2)

    entries = dict_repo.list_entries_by_dictionary("DIC-HIST-001")
    assert len(entries) == 2
    assert {e.headword for e in entries} == {"khamatha", "akha"}

    # 3. Synchronize entry to vocabulary
    vocab_entry = dict_repo.sync_entry_to_vocabulary(ent1, vocab_repo)
    assert vocab_entry.headword == "khamatha"
    assert "good" in vocab_entry.translations_en

    # Verify entry updated with vocabulary_id
    updated_ent1 = dict_repo.get_entry_by_id("DIC-HIST-001-ENT-0001")
    assert updated_ent1 is not None
    assert updated_ent1.vocabulary_id == vocab_entry.id
