"""Self-contained bundled vocabulary loader and zero-dependency lexical API.

This module ensures the Tangkhul Language Library operates completely standalone
with zero requirement for an external database server or external file setup.
All curated vocabulary entries, meanings, dialect variants, and citations
are bundled directly inside the library package distribution.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path
from typing import Any

from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.vocabulary.normalization import normalize_unicode


def get_bundled_data_dir() -> Path:
    """Return the filesystem path to the internal package data directory."""
    pkg_dir = Path(__file__).resolve().parent.parent
    data_dir = pkg_dir / "data"
    return data_dir


def get_bundled_vocabulary_file() -> Path:
    """Return path to the bundled vocabulary.jsonl dataset."""
    return get_bundled_data_dir() / "vocabulary.jsonl"


def get_bundled_database_file() -> Path:
    """Return path to the bundled SQLite database file."""
    return get_bundled_data_dir() / "tangkhul_corpus.sqlite"


def _entry_from_raw_dict(d: dict[str, Any]) -> VocabularyEntry:
    """Safely construct a VocabularyEntry dataclass from raw dictionary data."""
    # Ensure lists for JSON fields
    meanings = d.get("meanings") or []
    if isinstance(meanings, str):
        try:
            meanings = json.loads(meanings)
        except Exception:
            meanings = [meanings]

    translations = d.get("translations_en") or []
    if isinstance(translations, str):
        try:
            translations = json.loads(translations)
        except Exception:
            translations = [translations]

    alt_spellings = d.get("alternative_spellings") or []
    if isinstance(alt_spellings, str):
        try:
            alt_spellings = json.loads(alt_spellings)
        except Exception:
            alt_spellings = [alt_spellings]

    dialect_variants = d.get("dialect_variants") or []
    if isinstance(dialect_variants, str):
        try:
            dialect_variants = json.loads(dialect_variants)
        except Exception:
            dialect_variants = [dialect_variants]

    examples = d.get("example_sentences") or []
    if isinstance(examples, str):
        try:
            examples = json.loads(examples)
        except Exception:
            examples = [examples]

    # Reconstruct provenance records
    raw_prov = d.get("provenance") or []
    if isinstance(raw_prov, str):
        try:
            raw_prov = json.loads(raw_prov)
        except Exception:
            raw_prov = []

    provenance: list[ProvenanceRecord] = []
    for p in raw_prov:
        if isinstance(p, dict):
            provenance.append(
                ProvenanceRecord(
                    source_id=p.get("source_id", ""),
                    resource_type=p.get("resource_type", "dictionaries"),
                    citation=p.get("citation", ""),
                    page_or_section=p.get("page_or_section"),
                    context_sentence=p.get("context_sentence"),
                    recorded_year=p.get("recorded_year"),
                    permission_status=p.get("permission_status", "pending"),
                )
            )

    return VocabularyEntry(
        id=d.get("id", ""),
        headword=d.get("headword", ""),
        meanings=meanings,
        translations_en=translations,
        alternative_spellings=alt_spellings,
        dialect_variants=dialect_variants,
        dialect=d.get("dialect"),
        part_of_speech=d.get("part_of_speech"),
        pronunciation=d.get("pronunciation"),
        example_sentences=examples,
        provenance=provenance,
        verification_status=d.get("verification_status", "unverified"),
        license_restrictions=d.get("license_restrictions"),
        review_status=d.get("review_status", "pending_review"),
        review_notes=d.get("review_notes"),
        reviewer=d.get("reviewer"),
        reviewed_at=d.get("reviewed_at"),
    )


@functools.lru_cache(maxsize=1)
def load_bundled_vocabulary() -> list[VocabularyEntry]:
    """Load all bundled vocabulary entries into memory from package data.

    Cached in-memory so subsequent calls incur zero filesystem overhead.
    """
    jsonl_path = get_bundled_vocabulary_file()
    entries: list[VocabularyEntry] = []

    if jsonl_path.is_file():
        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    entries.append(_entry_from_raw_dict(data))
                except Exception:
                    continue

    # Fallback to bundled SQLite if jsonl is missing or empty
    if not entries:
        db_path = get_bundled_database_file()
        if db_path.is_file():
            import sqlite3

            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM vocabulary_entries ORDER BY headword COLLATE NOCASE")
                for row in cur.fetchall():
                    entries.append(_entry_from_raw_dict(dict(row)))
            finally:
                conn.close()

    entries.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))
    return entries


def get_words() -> list[str]:
    """Return a sorted list of all Tangkhul headwords bundled in this library.

    Example:
        >>> import tangkhul_lib
        >>> words = tangkhul_lib.get_words()
        >>> "khamatha" in words
        True
    """
    vocab = load_bundled_vocabulary()
    return sorted({entry.headword for entry in vocab if entry.headword}, key=str.lower)


def get_vocabulary() -> list[VocabularyEntry]:
    """Return all bundled VocabularyEntry instances with complete linguistic metadata.

    Example:
        >>> import tangkhul_lib
        >>> vocab = tangkhul_lib.get_vocabulary()
        >>> len(vocab) > 200
        True
    """
    return list(load_bundled_vocabulary())


def lookup(headword: str) -> VocabularyEntry | None:
    """Lookup a vocabulary entry by exact headword or alternative spelling (NFC/case-insensitive).

    Args:
        headword: Target word string to locate.

    Returns:
        VocabularyEntry if found, else None.
    """
    if not headword:
        return None
    target_norm = normalize_unicode(headword).strip().lower()
    for entry in load_bundled_vocabulary():
        if normalize_unicode(entry.headword).strip().lower() == target_norm:
            return entry
        for alt in entry.alternative_spellings:
            if normalize_unicode(alt).strip().lower() == target_norm:
                return entry
    return None


def search(
    query: str,
    mode: str = "substring",
    limit: int = 50,
) -> list[VocabularyEntry]:
    """Search bundled vocabulary entries across headwords, spellings, and English glosses.

    Args:
        query: Search term (Tangkhul word or English meaning).
        mode: Matching mode ('substring' or 'fuzzy').
        limit: Maximum results to return (default: 50).

    Returns:
        Ranked list of matching VocabularyEntry objects.
    """
    q_norm = normalize_unicode(query).strip().lower()
    if not q_norm:
        return []

    vocab = load_bundled_vocabulary()
    matches: list[VocabularyEntry] = []

    for entry in vocab:
        head_norm = normalize_unicode(entry.headword).strip().lower()
        # Headword match
        if q_norm in head_norm:
            matches.append(entry)
            continue
        # Alternative spellings match
        if any(
            q_norm in normalize_unicode(alt).strip().lower()
            for alt in entry.alternative_spellings
        ):
            matches.append(entry)
            continue
        # Meanings & translations match
        if any(q_norm in normalize_unicode(m).strip().lower() for m in entry.meanings):
            matches.append(entry)
            continue
        if any(q_norm in normalize_unicode(t).strip().lower() for t in entry.translations_en):
            matches.append(entry)
            continue

    if limit and len(matches) > limit:
        return matches[:limit]
    return matches


def get_dictionary() -> dict[str, list[str]]:
    """Return a mapping of headwords to their primary English meanings.

    Example:
        >>> import tangkhul_lib
        >>> d = tangkhul_lib.get_dictionary()
        >>> d["khamatha"]
        ['good', 'fine', 'beautiful']
    """
    result: dict[str, list[str]] = {}
    for entry in load_bundled_vocabulary():
        if entry.headword and entry.meanings:
            result[entry.headword] = entry.meanings
    return result


def get_corpus_database() -> DatabaseManager:
    """Return a DatabaseManager pointing directly to the library's bundled SQLite corpus.

    Requires zero external database setup or server connection.
    """
    bundled_db = get_bundled_database_file()
    if bundled_db.is_file():
        return DatabaseManager(bundled_db)
    # Fallback to self-populating in-memory database
    mem_manager = DatabaseManager(":memory:")
    mem_manager.initialize_schema()
    return mem_manager
