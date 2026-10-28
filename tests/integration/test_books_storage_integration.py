"""Integration tests for books storage, repository operations, and vocabulary database."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.books.catalogue import BookCatalogue
from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    BookRepository,
    ManifestRepository,
    VocabularyRepository,
)
from tangkhul_lib.vocabulary.search import VocabularySearchEngine


def test_database_schema_initialization_and_book_crud(tmp_path: Path) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    assert db_file.is_file()

    book_repo = BookRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)

    book = BookRecord(
        id="BK-TLS-001",
        title="Wontui Tangkhul",
        alternate_titles=["Wontui Tangkhul, Class II"],
        authors=[],
        publisher="Tangkhul Literature Society, Manipur",
        publication_year=2022,
        subject="Literature",
        educational_level="Class II",
        permission_status="pending",
        access_status="metadata_only",
        verification_status="verified",
    )
    book_repo.add(book)

    # Verify retrieval
    retrieved = book_repo.get_by_id("BK-TLS-001")
    assert retrieved is not None
    assert retrieved.id == "BK-TLS-001"
    assert retrieved.title == "Wontui Tangkhul"
    assert retrieved.educational_level == "Class II"

    # Verify manifest synchronization
    manifest_rec = manifest_repo.get_by_id("BK-TLS-001")
    assert manifest_rec is not None
    assert manifest_rec.title == "Wontui Tangkhul"
    assert manifest_rec.resource_type == "books"

    # Update book
    updated = book_repo.update("BK-TLS-001", {"notes": "Updated via integration test."})
    assert updated.notes == "Updated via integration test."
    assert book_repo.get_by_id("BK-TLS-001").notes == "Updated via integration test."

    # Tokens storage
    tokens = [
        {
            "word_form": "Wontui",
            "page_or_section": "p. 1",
            "context_sentence": "Wontui kachiko.",
        },
        {
            "word_form": "Tangkhul",
            "page_or_section": "p. 1",
            "context_sentence": "Tangkhul tuitam.",
        },
    ]
    book_repo.save_tokens("BK-TLS-001", tokens)
    saved_tokens = book_repo.get_extracted_tokens("BK-TLS-001")
    assert len(saved_tokens) == 2
    assert saved_tokens[0]["word_form"] == "Wontui"


def test_vocabulary_repository_and_search_integration(tmp_path: Path) -> None:
    db_file = tmp_path / "vocab_test.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)

    prov = ProvenanceRecord(
        source_id="BK-HIST-001",
        resource_type="books",
        citation="Pettigrew 1918, p. 12",
        page_or_section="p. 12",
        context_sentence="Shim kathara sakashak.",
        recorded_year=1918,
    )
    entry = VocabularyEntry(
        id="VOC-001",
        headword="shim",
        meanings=["house", "dwelling"],
        translations_en=["house"],
        alternative_spellings=["chim"],
        provenance=[prov],
        verification_status="verified",
    )
    vocab_repo.add(entry)

    # Retrieve and verify
    retrieved = vocab_repo.get_by_id("VOC-001")
    assert retrieved is not None
    assert retrieved.headword == "shim"
    assert retrieved.meanings == ["house", "dwelling"]
    assert len(retrieved.provenance) == 1
    assert retrieved.provenance[0].source_id == "BK-HIST-001"
    assert retrieved.provenance[0].page_or_section == "p. 12"

    # Search engine integration
    search_engine = VocabularySearchEngine(repository=vocab_repo)
    matches = search_engine.search_headword("shi")
    assert len(matches) == 1
    assert matches[0].headword == "shim"

    meaning_matches = search_engine.search_meaning("dwelling")
    assert len(meaning_matches) == 1
    assert meaning_matches[0].headword == "shim"


def test_load_and_persist_manifest_catalogue(tmp_path: Path) -> None:
    data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "manifests"
    manifest_path = data_dir / "books.jsonl"
    catalogue = BookCatalogue.load_from_manifest(manifest_path)
    assert len(catalogue) >= 14

    # Persist all records into a fresh SQLite database
    db_file = tmp_path / "manifest_sync.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    book_repo = BookRepository(db_manager)
    for book in catalogue.list_books():
        book_repo.add(book)

    assert book_repo.count() == len(catalogue)
    retrieved_pettigrew = book_repo.get_by_id("BK-HIST-001")
    assert retrieved_pettigrew is not None
    assert "Pettigrew" in retrieved_pettigrew.authors[0]
