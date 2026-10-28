"""Comprehensive unit and integration tests for SQLite FTS5 and Tangkhul phonetic search."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from tangkhul_lib.cli import main
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager, is_fts5_available
from tangkhul_lib.storage.repositories import (
    VocabularyRepository,
    sanitize_fts_query,
)
from tangkhul_lib.vocabulary.phonetic import (
    EVIDENCE_BASED_RULES,
    EXPERIMENTAL_RULES,
    TangkhulPhoneticEncoder,
)
from tangkhul_lib.vocabulary.search import (
    VocabularySearchEngine,
    format_search_explanation,
)


@pytest.fixture
def mem_db() -> DatabaseManager:
    """Fixture providing an isolated in-memory DatabaseManager with initialized schema."""
    db = DatabaseManager(":memory:")
    db.initialize_schema()
    return db


@pytest.fixture
def sample_entries() -> list[VocabularyEntry]:
    """Fixture providing standard test vocabulary entries across dialects and sources."""
    return [
        VocabularyEntry(
            id="VOCAB-TEST-001",
            headword="ngashān",
            meanings=["custom", "traditional practice", "clan law"],
            translations_en=["custom", "traditional law"],
            part_of_speech="noun",
            dialect="Ukhrul",
            alternative_spellings=["ngashan"],
            verification_status="verified",
            provenance=[
                ProvenanceRecord(
                    source_id="DIC-TEST-001",
                    resource_type="dictionaries",
                    citation="Pettigrew 1918, p. 250",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
        ),
        VocabularyEntry(
            id="VOCAB-TEST-002",
            headword="khamor",
            meanings=["mouth", "speech", "oral proverb"],
            translations_en=["mouth", "speech"],
            part_of_speech="noun",
            dialect="Standard Tangkhul",
            alternative_spellings=["mor"],
            verification_status="verified",
            provenance=[
                ProvenanceRecord(
                    source_id="CUL-TEST-001",
                    resource_type="culture",
                    citation="Tangkhul Proverbs, 1978",
                    recorded_year=1978,
                    permission_status="permitted",
                )
            ],
        ),
        VocabularyEntry(
            id="VOCAB-TEST-003",
            headword="shim",
            meanings=["house", "dwelling place"],
            translations_en=["house", "home"],
            part_of_speech="noun",
            dialect="Ukhrul",
            alternative_spellings=["sim"],
            verification_status="verified",
            provenance=[
                ProvenanceRecord(
                    source_id="BK-TEST-001",
                    resource_type="books",
                    citation="Grammar 1969",
                    recorded_year=1969,
                    permission_status="permitted",
                )
            ],
        ),
        VocabularyEntry(
            id="VOCAB-TEST-RESTRICTED",
            headword="kakhangayung",
            meanings=["sacred esoteric chant"],
            translations_en=["secret chant"],
            part_of_speech="noun",
            dialect="Raphei",
            license_restrictions="restricted",
            verification_status="needs_review",
            provenance=[
                ProvenanceRecord(
                    source_id="CUL-RESTRICTED-001",
                    resource_type="culture",
                    citation="Restricted Clan Rites",
                    recorded_year=1950,
                    permission_status="restricted",
                    context_sentence="Secret chant text that must not be exposed.",
                )
            ],
        ),
    ]


def test_fts5_availability_and_fallback(mem_db: DatabaseManager) -> None:
    """Test FTS5 detection and graceful fallback when FTS5 is not active."""
    with mem_db.get_connection() as conn:
        available = is_fts5_available(conn)
        assert isinstance(available, bool)

    # When FTS5 is simulated as unavailable
    repo = VocabularyRepository(mem_db)
    with patch.object(repo, "is_fts5_available", return_value=False):
        engine = VocabularySearchEngine(repository=repo)
        results, matches, explanation = engine.search_with_matches(
            headword="ngashan", mode="fulltext"
        )
        assert explanation["fts5_available"] is False
        assert explanation["fallback_occurred"] is True
        assert "fell back to standard substring search" in explanation["fallback_reason"]


def test_fts_schema_idempotence(mem_db: DatabaseManager) -> None:
    """Ensure FTS schema creation can be invoked repeatedly without error."""
    mem_db.initialize_schema()
    mem_db.initialize_schema()
    repo = VocabularyRepository(mem_db)
    assert repo.ensure_fts_schema() is True


def test_fts_index_sync_and_rebuild(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test automatic indexing on add, removal on delete, and transactional rebuild."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    # Restricted entry should not be in FTS index
    fts_results = repo.search_fts("sacred esoteric chant")
    assert len(fts_results) == 0

    # Public entry should be indexed
    fts_results = repo.search_fts("custom")
    assert any(e.id == "VOCAB-TEST-001" for e, _ in fts_results)

    # Rebuild index safely
    count = repo.rebuild_fts_index()
    # 3 permitted entries out of 4
    assert count == 3

    # Delete entry and confirm FTS cleanup
    repo.delete("VOCAB-TEST-001")
    fts_after_del = repo.search_fts("custom")
    assert not any(e.id == "VOCAB-TEST-001" for e, _ in fts_after_del)


def test_fts_query_sanitizer() -> None:
    """Test FTS query string sanitization for malformed punctuation and operators."""
    assert sanitize_fts_query("") == ""
    assert sanitize_fts_query("   ") == ""
    # Unbalanced quotes
    sanitized = sanitize_fts_query('word "broken phrase')
    assert '"' in sanitized
    # Bare operators should be handled safely
    op_query = sanitize_fts_query("AND OR NOT * ^")
    assert op_query != ""
    # Hyphenated words should be safely quoted so they are not treated as NOT operators
    hyphen_query = sanitize_fts_query("folk-tale")
    assert '"folk-tale"' in hyphen_query


def test_fts_search_headwords_meanings_phrases(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test fulltext search across headwords, alternative spellings, and glosses."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    engine = VocabularySearchEngine(repository=repo)

    # Search headword via fulltext
    res_hw, _, _ = engine.search_with_matches(headword="khamor", mode="fulltext")
    assert any(e.id == "VOCAB-TEST-002" for e in res_hw)

    # Search meaning phrase via fulltext
    res_m, _, _ = engine.search_with_matches(meaning="traditional practice", mode="fulltext")
    assert any(e.id == "VOCAB-TEST-001" for e in res_m)

    # Multi-word query
    res_mw, _, _ = engine.search_with_matches(meaning="dwelling place", mode="fulltext")
    assert any(e.id == "VOCAB-TEST-003" for e in res_mw)


def test_unicode_macrons_and_diacritics(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test Unicode normalization and macron preservation in fulltext and phonetic."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    engine = VocabularySearchEngine(repository=repo)

    # Exact macron headword in fulltext
    res_macron, _, _ = engine.search_with_matches(headword="ngashān", mode="fulltext")
    assert any(e.headword == "ngashān" for e in res_macron)

    # ASCII search matches decomposed and precomposed representations
    res_ascii, _, _ = engine.search_with_matches(headword="ngashan", mode="fulltext")
    assert any(e.headword == "ngashān" for e in res_ascii)


def test_fuzzy_search_levenshtein(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test fuzzy similarity matching with typo tolerance."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    engine = VocabularySearchEngine(repository=repo)

    # Typo: "ngashon" instead of "ngashan"
    results, matches, expl = engine.search_with_matches(
        headword="ngashon", mode="fuzzy", threshold=0.75
    )
    assert any(e.headword == "ngashān" for e in results)
    match_entry = matches.get("VOCAB-TEST-001")
    assert match_entry is not None
    assert match_entry.match_mode == "fuzzy"
    assert match_entry.match_score >= 0.75


def test_tangkhul_phonetic_evidence_rules() -> None:
    """Test evidence-based phonetic normalization rules."""
    encoder = TangkhulPhoneticEncoder(include_experimental=False)
    assert len(encoder.active_rules) == len(EVIDENCE_BASED_RULES)

    # Macron folding
    assert encoder.encode("ngashān") == "ngashan"
    assert encoder.encode("āvā") == "ava"

    # Glottal normalization (apostrophes and glottal stops)
    assert encoder.encode("ha'i") == "hai"
    assert encoder.encode("ha’i") == "hai"

    # Velar nasal 'ng' is preserved as single nasal unit
    assert "ng" in encoder.encode("ngashan")


def test_tangkhul_phonetic_experimental_rules() -> None:
    """Test experimental phonetic rules (sibilants, aspirates, liquids, diphthongs)."""
    # By default, experimental rules are disabled
    strict_encoder = TangkhulPhoneticEncoder(include_experimental=False)
    assert strict_encoder.encode("khamor") != strict_encoder.encode("kamol")

    # With experimental rules enabled
    exp_encoder = TangkhulPhoneticEncoder(include_experimental=True)
    assert len(exp_encoder.active_rules) == len(EVIDENCE_BASED_RULES) + len(EXPERIMENTAL_RULES)

    # Sibilant neutralization: sh <-> s
    assert exp_encoder.encode("shim") == exp_encoder.encode("sim")

    # Aspirate simplification: kh -> k
    assert exp_encoder.encode("khamor") == exp_encoder.encode("kamor")

    # Liquid alternation: r -> l
    assert exp_encoder.encode("khamor") == exp_encoder.encode("kamol")

    # Diphthong reduction: ei -> ai
    assert exp_encoder.encode("phei") == exp_encoder.encode("phai")


def test_restricted_records_shielded_across_all_modes(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Ensure restricted records and contexts are excluded in every search mode."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    engine = VocabularySearchEngine(repository=repo)

    for mode in ["substring", "fulltext", "fuzzy", "phonetic"]:
        results, _, _ = engine.search_with_matches(
            headword="kakhangayung",
            mode=mode,
            threshold=0.5,
        )
        assert not any(e.id == "VOCAB-TEST-RESTRICTED" for e in results), (
            f"Restricted entry leaked in mode '{mode}'"
        )

        results_meaning, _, _ = engine.search_with_matches(
            meaning="sacred esoteric chant",
            mode=mode,
            threshold=0.5,
        )
        assert not any(e.id == "VOCAB-TEST-RESTRICTED" for e in results_meaning), (
            f"Restricted entry leaked by meaning in mode '{mode}'"
        )


def test_combined_filters_with_modes(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test combining search modes with secondary metadata filters."""
    repo = VocabularyRepository(mem_db)
    for entry in sample_entries:
        repo.add(entry)

    engine = VocabularySearchEngine(repository=repo)

    # Filter with dialect and source_type
    results, _, _ = engine.search_with_matches(
        headword="ngashan",
        dialect="Ukhrul",
        source_type="dictionaries",
        verification_status="verified",
        part_of_speech="noun",
        mode="fulltext",
    )
    assert len(results) == 1
    assert results[0].id == "VOCAB-TEST-001"

    # Mismatched dialect filter should yield no results
    results_mismatch, _, _ = engine.search_with_matches(
        headword="ngashan",
        dialect="Somdal",
        mode="fulltext",
    )
    assert len(results_mismatch) == 0


def test_format_search_explanation() -> None:
    """Test diagnostic formatting of search explanation."""
    expl = {
        "mode": "fuzzy",
        "query_used": "ngashon",
        "fts5_available": True,
        "fts5_active": False,
        "threshold": 0.75,
        "filters_applied": {"dialect": "Ukhrul"},
        "match_count": 1,
    }
    formatted = format_search_explanation(expl)
    assert "SEARCH STRATEGY & QUERY EXPLANATION:" in formatted
    assert "Search Mode:       fuzzy" in formatted
    assert "Fuzzy Threshold:   0.75" in formatted
    assert "Total Matches:     1" in formatted


def test_cli_vocab_rebuild_index_command(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI --rebuild-index flag execution."""
    code = main(["vocab", "--rebuild-index"])
    assert code == 0
    captured = capsys.readouterr()
    assert "FTS5 full-text search index rebuilt successfully" in captured.out
    assert "records indexed" in captured.out


def test_cli_vocab_rebuild_index_incompatible_options(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test error when --rebuild-index is combined with search queries."""
    code = main(["vocab", "--rebuild-index", "--search", "test"])
    assert code == 2
    captured = capsys.readouterr()
    assert "cannot be combined" in captured.err


def test_cli_vocab_mode_requires_query(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that fulltext, fuzzy, and phonetic modes require a query term."""
    code = main(["vocab", "--mode", "fulltext"])
    assert code == 2
    captured = capsys.readouterr()
    assert "requires a query term" in captured.err


def test_cli_vocab_invalid_threshold(capsys: pytest.CaptureFixture[str]) -> None:
    """Test error reporting on out-of-range threshold."""
    code = main(["vocab", "--search", "ngashan", "--mode", "fuzzy", "--threshold", "1.5"])
    assert code == 2
    captured = capsys.readouterr()
    assert "--threshold must be a float between 0.0 and 1.0" in captured.err


def test_cli_vocab_fulltext_and_explain(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI fulltext search with --explain-search."""
    code = main(["vocab", "--search", "ngashan", "--mode", "fulltext", "--explain-search"])
    assert code == 0
    captured = capsys.readouterr()
    assert "SEARCH STRATEGY & QUERY EXPLANATION:" in captured.out
    assert "Search Mode:       fulltext" in captured.out
    assert "Match Strategy:  fulltext" in captured.out


def test_cli_vocab_phonetic_and_experimental(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI phonetic search with experimental sound shift rules."""
    code = main(
        [
            "vocab",
            "--search",
            "ngashan",
            "--mode",
            "phonetic",
            "--experimental-phonetics",
            "--explain-search",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "SEARCH STRATEGY & QUERY EXPLANATION:" in captured.out
    assert "Search Mode:       phonetic" in captured.out
    assert "sibilant_neutralization" in captured.out
