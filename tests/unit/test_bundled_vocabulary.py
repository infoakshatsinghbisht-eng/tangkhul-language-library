"""Unit tests for self-contained bundled vocabulary storage and zero-dependency API."""

from __future__ import annotations

import tangkhul_lib
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.core.models import VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.vocabulary.bundled import (
    get_bundled_data_dir,
    get_bundled_database_file,
    get_bundled_vocabulary_file,
)
from tangkhul_lib.vocabulary.search import load_unified_vocabulary_engine


def test_bundled_files_exist() -> None:
    """Verify that bundled dataset files exist inside the package distribution."""
    data_dir = get_bundled_data_dir()
    assert data_dir.is_dir(), f"Bundled data dir missing: {data_dir}"

    vocab_file = get_bundled_vocabulary_file()
    assert vocab_file.is_file(), f"Bundled vocabulary.jsonl missing: {vocab_file}"
    assert vocab_file.stat().st_size > 1000

    db_file = get_bundled_database_file()
    assert db_file.is_file(), f"Bundled SQLite database missing: {db_file}"
    assert db_file.stat().st_size > 10000


def test_get_words_zero_external_dependency() -> None:
    """Verify get_words() returns a non-empty list of Tangkhul words without external database."""
    words = tangkhul_lib.get_words()
    assert isinstance(words, list)
    assert len(words) >= 200, f"Expected at least 200 words, got {len(words)}"

    # Check key Tangkhul vocabulary
    words_lower = {w.lower() for w in words}
    expected_words = [
        "khamatha",  # good, beautiful
        "shim",      # house
        "ngalung",   # stone
        "laa",       # song
        "leishat",   # love
        "shirui",    # mountain
        "luira",     # festival
        "kazip",     # gather
        "khamor",    # mouth / speech
    ]
    for ew in expected_words:
        assert ew in words_lower, f"Expected '{ew}' in bundled words list"


def test_get_vocabulary_entries() -> None:
    """Verify get_vocabulary() returns full VocabularyEntry instances."""
    vocab = tangkhul_lib.get_vocabulary()
    assert isinstance(vocab, list)
    assert len(vocab) >= 200

    for entry in vocab[:20]:
        assert isinstance(entry, VocabularyEntry)
        assert entry.id
        assert entry.headword
        assert isinstance(entry.meanings, list)


def test_lookup_word() -> None:
    """Verify lookup() finds words by exact headword or case-insensitive NFC matching."""
    # Exact lookup
    entry = tangkhul_lib.lookup("khamatha")
    assert entry is not None
    assert entry.headword.lower() == "khamatha"
    assert any("good" in m.lower() or "beautiful" in m.lower() for m in entry.meanings)

    # Case-insensitive lookup
    entry_caps = tangkhul_lib.lookup("KHAMATHA")
    assert entry_caps is not None
    assert entry_caps.id == entry.id

    # House lookup
    shim = tangkhul_lib.lookup("shim")
    assert shim is not None
    assert any("house" in m.lower() or "dwelling" in m.lower() for m in shim.meanings)

    # Non-existent word
    missing = tangkhul_lib.lookup("non_existent_xyz_123")
    assert missing is None


def test_search_bundled_words() -> None:
    """Verify search() queries across headwords and English meanings."""
    # Search by English meaning
    results_house = tangkhul_lib.search("house")
    assert len(results_house) > 0
    headwords = [r.headword.lower() for r in results_house]
    assert "shim" in headwords

    # Search by Tangkhul word prefix
    results_kha = tangkhul_lib.search("kha")
    assert len(results_kha) > 0

    # Search empty string
    assert tangkhul_lib.search("") == []


def test_get_dictionary() -> None:
    """Verify get_dictionary() provides headword to meanings dictionary."""
    d = tangkhul_lib.get_dictionary()
    assert isinstance(d, dict)
    assert len(d) >= 200
    assert "khamatha" in d or "shim" in d


def test_get_corpus_database() -> None:
    """Verify get_corpus_database() provides embedded SQLite connection with zero setup."""
    db_mgr = tangkhul_lib.get_corpus_database()
    assert isinstance(db_mgr, DatabaseManager)

    with db_mgr.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vocabulary_entries")
        count = cur.fetchone()[0]
        assert count >= 200


def test_engine_fallback_without_manifests(tmp_path) -> None:
    """Verify load_unified_vocabulary_engine works in isolated directory with no external DB."""
    # Config pointing to isolated empty directory
    isolated_cfg = LibraryConfig.from_environment()
    isolated_db_file = tmp_path / "test_isolated.sqlite"
    isolated_mgr = DatabaseManager(isolated_db_file)
    isolated_mgr.initialize_schema()

    # Engine loaded with isolated database
    engine = load_unified_vocabulary_engine(config=isolated_cfg, auto_sync_if_empty=True)
    assert engine is not None
    all_entries = engine.list_all()
    assert len(all_entries) >= 200
