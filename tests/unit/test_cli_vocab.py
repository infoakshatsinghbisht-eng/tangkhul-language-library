"""Comprehensive unit tests for unified Tangkhul vocabulary search CLI."""

from __future__ import annotations

import pytest

from tangkhul_lib.cli import main
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import VocabularyRepository
from tangkhul_lib.vocabulary.search import (
    VocabularySearchEngine,
    format_vocabulary_entry,
)


def test_cli_vocab_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test vocab subcommand help display."""
    try:
        main(["vocab", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "tangkhul vocab" in captured.out
    assert "--search" in captured.out
    assert "--exact" in captured.out
    assert "--meaning" in captured.out
    assert "--dialect" in captured.out
    assert "--source-type" in captured.out
    assert "--verification-status" in captured.out
    assert "--limit" in captured.out


def test_cli_vocab_no_args_shows_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Running vocab without arguments displays help text and exits 0."""
    code = main(["vocab"])
    assert code == 0
    captured = capsys.readouterr()
    assert "tangkhul vocab" in captured.out
    assert "--search" in captured.out


def test_cli_vocab_exact_search(capsys: pytest.CaptureFixture[str]) -> None:
    """Test exact headword search with case-insensitivity."""
    code = main(["vocab", "--exact", "khararchan"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "khararchan" in captured.out.lower()

    # Case-insensitive exact search
    code_upper = main(["vocab", "--exact", "KHARARCHAN"])
    assert code_upper == 0
    captured_upper = capsys.readouterr()
    assert "Found" in captured_upper.out
    assert "khararchan" in captured_upper.out.lower()


def test_cli_vocab_partial_search(capsys: pytest.CaptureFixture[str]) -> None:
    """Test partial headword search."""
    code = main(["vocab", "--search", "mor"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "khamor" in captured.out.lower()


def test_cli_vocab_alt_spelling_and_unicode_preservation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test searching alternative spellings and preserving Unicode macrons."""
    # Searching by ASCII alternate spelling finds the macron headword ngashān
    code = main(["vocab", "--search", "ngashan"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "ngashān" in captured.out or "ngashan" in captured.out

    # Exact search with Unicode macron
    code_exact = main(["vocab", "--exact", "ngashān"])
    assert code_exact == 0
    captured_exact = capsys.readouterr()
    assert "Found" in captured_exact.out
    assert "ngashān" in captured_exact.out


def test_cli_vocab_meaning_filter(capsys: pytest.CaptureFixture[str]) -> None:
    """Test search by English meaning and translation gloss."""
    code = main(["vocab", "--meaning", "dwelling place"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "shim" in captured.out


def test_cli_vocab_dialect_filter(capsys: pytest.CaptureFixture[str]) -> None:
    """Test filtering vocabulary by dialect."""
    code = main(["vocab", "--dialect", "Ukhrul", "--limit", "5"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Ukhrul" in captured.out


@pytest.mark.parametrize(
    "src_type",
    ["books", "songs", "dictionaries", "culture", "history", "literature"],
)
def test_cli_vocab_all_six_source_types(
    src_type: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test filtering vocabulary by all six source types."""
    code = main(["vocab", "--source-type", src_type, "--limit", "2"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert f"[{src_type}]" in captured.out.lower() or src_type in captured.out.lower()


def test_cli_vocab_verification_status_filter(capsys: pytest.CaptureFixture[str]) -> None:
    """Test filtering by verification status."""
    code_verified = main(["vocab", "--verification-status", "verified", "--limit", "3"])
    assert code_verified == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Verification:    verified" in captured.out


def test_cli_vocab_limit(capsys: pytest.CaptureFixture[str]) -> None:
    """Test limit constraint."""
    code = main(["vocab", "--list", "--limit", "3"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found 3 matching vocabulary entry/entries:" in captured.out


def test_cli_vocab_invalid_limit(capsys: pytest.CaptureFixture[str]) -> None:
    """Test validation error on non-positive limit."""
    code_zero = main(["vocab", "--limit", "0"])
    assert code_zero == 2
    err_zero = capsys.readouterr().err
    assert "positive integer" in err_zero

    code_neg = main(["vocab", "--limit", "-10"])
    assert code_neg == 2
    err_neg = capsys.readouterr().err
    assert "positive integer" in err_neg


def test_cli_vocab_invalid_source_type(capsys: pytest.CaptureFixture[str]) -> None:
    """Test validation error on unsupported source type."""
    code = main(["vocab", "--source-type", "nonexistent_domain"])
    assert code == 2
    err = capsys.readouterr().err
    assert "Invalid --source-type" in err
    assert "books, songs, dictionaries, culture, history, literature" in err


def test_cli_vocab_invalid_verification_status(capsys: pytest.CaptureFixture[str]) -> None:
    """Test validation error on invalid verification status."""
    code = main(["vocab", "--verification-status", "bogus_status"])
    assert code == 2
    err = capsys.readouterr().err
    assert "Invalid --verification-status" in err


def test_cli_vocab_empty_results(capsys: pytest.CaptureFixture[str]) -> None:
    """Test output when search yields no matches."""
    code = main(["vocab", "--search", "zz_nonexistent_tangkhul_query_12345"])
    assert code == 0
    captured = capsys.readouterr()
    assert "No vocabulary entries found matching the specified criteria." in captured.out


def test_cli_vocab_by_id(capsys: pytest.CaptureFixture[str]) -> None:
    """Test fetching a specific vocabulary entry by ID."""
    code = main(["vocab", "--id", "VOC-BK-0001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Headword:        shim" in captured.out
    assert "ID:              VOC-BK-0001" in captured.out


def test_cli_vocab_by_id_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Test fetching nonexistent ID returns error code 1."""
    code = main(["vocab", "--id", "VOC-DOES-NOT-EXIST-9999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_restricted_data_protection() -> None:
    """Verify restricted vocabulary items and example sentences are never exposed."""
    db_manager = DatabaseManager(":memory:")
    db_manager.initialize_schema()
    vocab_repo = VocabularyRepository(db_manager)

    restricted_entry = VocabularyEntry(
        id="VOC-RESTRICTED-001",
        headword="secretword",
        meanings=["confidential meaning"],
        example_sentences=["Restricted ceremonial phrase."],
        license_restrictions="restricted",
        provenance=[
            ProvenanceRecord(
                source_id="SRC-RESTRICTED",
                resource_type="culture",
                citation="Restricted Clan Rites",
                permission_status="restricted",
                context_sentence="Secret ceremonial context sentence",
            )
        ],
    )
    vocab_repo.add(restricted_entry)

    engine = VocabularySearchEngine(repository=vocab_repo)
    results = engine.filter_entries(headword="secretword")
    assert len(results) == 0

    # Also test format_vocabulary_entry strips restricted context and examples
    unrestricted_entry = VocabularyEntry(
        id="VOC-PUB-001",
        headword="publicword",
        meanings=["open meaning"],
        example_sentences=["Public phrase."],
        provenance=[
            ProvenanceRecord(
                source_id="SRC-RESTRICTED-PROV",
                resource_type="songs",
                citation="Private Song Book",
                permission_status="restricted",
                context_sentence="Restricted song line",
            )
        ],
    )
    formatted = format_vocabulary_entry(unrestricted_entry)
    assert "Restricted song line" not in formatted
    assert "Public phrase." in formatted


def test_missing_optional_fields_formatting() -> None:
    """Test that missing optional fields do not crash and display 'None recorded' or equivalent."""
    sparse_entry = VocabularyEntry(
        id="VOC-SPARSE-001",
        headword="sparseword",
        meanings=[],
        translations_en=[],
        alternative_spellings=[],
        dialect_variants=[],
        dialect=None,
        part_of_speech=None,
        pronunciation=None,
        example_sentences=[],
        provenance=[],
    )
    formatted = format_vocabulary_entry(sparse_entry)
    assert "Headword:        sparseword" in formatted
    assert "Part of Speech:  None recorded" in formatted
    assert "Dialect/Village: Not specified" in formatted
    assert "Meanings:        None recorded" in formatted
    assert "Alt Spellings:   None recorded" in formatted
    assert "Provenance:      No provenance records attached" in formatted


def test_multiple_provenance_without_duplicates() -> None:
    """Test that multiple provenance records are formatted without duplication."""
    entry = VocabularyEntry(
        id="VOC-MULTI-001",
        headword="multiword",
        meanings=["sample meaning"],
        provenance=[
            ProvenanceRecord(
                source_id="SRC-001",
                resource_type="books",
                citation="Book One, p. 10",
                page_or_section="p. 10",
            ),
            ProvenanceRecord(
                source_id="SRC-002",
                resource_type="songs",
                citation="Song Archive, Stanza 2",
                page_or_section="Stanza 2",
            ),
        ],
    )
    formatted = format_vocabulary_entry(entry)
    assert "Provenance (2 source(s)):" in formatted
    assert "[1] Source ID:       SRC-001" in formatted
    assert "[2] Source ID:       SRC-002" in formatted


def test_existing_cli_commands_regression(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure adding 'vocab' command did not break existing subcommands."""
    assert main(["books", "--list"]) == 0
    assert "Tangkhul Books Catalogue" in capsys.readouterr().out

    assert main(["songs", "--list"]) == 0
    assert "Tangkhul Songs Catalogue" in capsys.readouterr().out

    assert main(["dictionaries", "--list"]) == 0
    assert "Tangkhul Dictionaries Catalogue" in capsys.readouterr().out

    assert main(["culture", "--list"]) == 0
    assert "Tangkhul Culture Catalogue" in capsys.readouterr().out

    assert main(["history", "--list"]) == 0
    assert "Tangkhul History Catalogue" in capsys.readouterr().out

    assert main(["literature", "--list"]) == 0
    assert "Tangkhul Literature Catalogue" in capsys.readouterr().out
