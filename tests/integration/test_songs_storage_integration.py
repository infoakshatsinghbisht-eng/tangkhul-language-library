"""Integration tests for songs storage, repository CRUD, and manifest sync."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.songs.catalogue import SongCatalogue
from tangkhul_lib.songs.models import SongRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    ManifestRepository,
    SongRepository,
    VocabularyRepository,
)


def test_database_song_crud_and_manifest_sync(tmp_path: Path) -> None:
    db_file = tmp_path / "song_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    song_repo = SongRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)

    song = SongRecord(
        id="SNG-TRAD-001",
        title="Shimreishang Kala Maitonphi",
        alternate_titles=["Ashang Aton Laa"],
        singer="Traditional",
        village="Phungcham",
        song_type="ballad",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    song_repo.add(song)

    # Verify retrieval
    retrieved = song_repo.get_by_id("SNG-TRAD-001")
    assert retrieved is not None
    assert retrieved.id == "SNG-TRAD-001"
    assert retrieved.title == "Shimreishang Kala Maitonphi"
    assert retrieved.village == "Phungcham"

    # Verify manifest synchronization
    manifest_rec = manifest_repo.get_by_id("SNG-TRAD-001")
    assert manifest_rec is not None
    assert manifest_rec.title == "Shimreishang Kala Maitonphi"
    assert manifest_rec.resource_type == "songs"

    # Update metadata
    updated = song_repo.update("SNG-TRAD-001", {"notes": "Updated note from test."})
    assert updated.notes == "Updated note from test."
    assert song_repo.get_by_id("SNG-TRAD-001").notes == "Updated note from test."

    # Tokens persistence
    tokens = [
        {
            "word_form": "Shimreishang",
            "page_or_section": "Stanza 1, Line 1",
            "context_sentence": "Shimreishangwui ningli leikashi lei.",
        },
        {
            "word_form": "Maitonphi",
            "page_or_section": "Stanza 1, Line 2",
            "context_sentence": "Maitonphi kachihi ramwui won kapha.",
        },
    ]
    song_repo.save_tokens("SNG-TRAD-001", tokens)
    saved_tokens = song_repo.get_extracted_tokens("SNG-TRAD-001")
    assert len(saved_tokens) == 2
    assert saved_tokens[0]["word_form"] == "Shimreishang"


def test_vocabulary_linking_with_songs(tmp_path: Path) -> None:
    db_file = tmp_path / "song_vocab.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)

    prov = ProvenanceRecord(
        source_id="SNG-TRAD-001",
        resource_type="songs",
        citation="Shimreishang Kala Maitonphi [Stanza 1, Line 1]",
        page_or_section="Stanza 1, Line 1",
        context_sentence="Shimreishangwui ningli leikashi lei.",
    )
    vocab_entry = VocabularyEntry(
        id="VOC-SNG-001",
        headword="leikashi",
        meanings=[],
        translations_en=[],
        provenance=[prov],
        verification_status="unverified",
    )
    vocab_repo.add(vocab_entry)

    retrieved = vocab_repo.get_by_id("VOC-SNG-001")
    assert retrieved is not None
    assert retrieved.headword == "leikashi"
    assert len(retrieved.provenance) == 1
    assert retrieved.provenance[0].source_id == "SNG-TRAD-001"
    assert retrieved.provenance[0].resource_type == "songs"


def test_load_and_persist_songs_manifest(tmp_path: Path) -> None:
    data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "manifests"
    manifest_path = data_dir / "songs.jsonl"
    catalogue = SongCatalogue.load_from_manifest(manifest_path)
    assert len(catalogue) >= 20

    db_file = tmp_path / "all_songs.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    song_repo = SongRepository(db_manager)
    for s in catalogue.list_songs():
        song_repo.add(s)

    assert song_repo.count() == len(catalogue)
    assert song_repo.count() == 48
    s_rewben = song_repo.get_by_id("SNG-MOD-001")
    assert s_rewben is not None
    assert s_rewben.singer == "Rewben Mashangva"
    s_hymn = song_repo.get_by_id("SNG-HIST-003")
    assert s_hymn is not None
    assert "Jesus Loves Me" in (s_hymn.title_translation or "")
