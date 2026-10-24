"""Unit tests for configuration paths and core domain models."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.config import LibraryPaths
from tangkhul_lib.core.exceptions import ProvenanceError
from tangkhul_lib.core.models import (
    ManifestRecord,
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.vocabulary.deduplication import deduplicate_entries
from tangkhul_lib.vocabulary.normalization import normalize_unicode, sanitize_spacing
from tangkhul_lib.vocabulary.provenance import create_provenance_record


def test_library_paths() -> None:
    root = Path("/dummy/project/root")
    paths = LibraryPaths(root_dir=root)
    assert paths.data_dir == root / "data"
    assert paths.manifests_dir == root / "data" / "manifests"
    assert paths.raw_dir == root / "data" / "raw"
    assert paths.database_dir == root / "data" / "database"


def test_manifest_record_dict_conversion() -> None:
    record = ManifestRecord(
        id="BK-0001",
        resource_type="books",
        title="Tangkhul Grammar and Vocabulary",
        creator="Rev. W. Pettigrew",
        year=1918,
        language="Tangkhul",
        permission_status="public_domain",
        verification_status="verified",
    )
    d = record.to_dict()
    assert d["id"] == "BK-0001"
    assert d["resource_type"] == "books"
    assert d["year"] == 1918

    reconstructed = ManifestRecord.from_dict(d)
    assert reconstructed == record


def test_provenance_creation_validation() -> None:
    rec = create_provenance_record(
        source_id="BK-0001",
        resource_type="books",
        citation="Pettigrew, 1918, p. 45",
        page_or_section="p. 45",
        context_sentence="Example sentence in Tangkhul.",
        recorded_year=1918,
    )
    assert rec.source_id == "BK-0001"
    assert rec.page_or_section == "p. 45"

    with pytest.raises(ProvenanceError):
        create_provenance_record(source_id="", resource_type="books", citation="citation")

    with pytest.raises(ProvenanceError):
        create_provenance_record(source_id="BK-0001", resource_type="books", citation="")


def test_normalization() -> None:
    assert normalize_unicode("Tangkhul \u0065\u0301") == "Tangkhul \u00e9"
    raw_spacing = "  Tangkhul   language   preservation  "
    assert sanitize_spacing(raw_spacing) == "Tangkhul language preservation"


def test_deduplication_preserves_distinct_meanings() -> None:
    p1 = ProvenanceRecord(source_id="SRC-1", resource_type="dictionaries", citation="Dict 1, p. 10")
    p2 = ProvenanceRecord(source_id="SRC-2", resource_type="books", citation="Book 1, p. 20")

    e1 = VocabularyEntry(
        id="V-1",
        headword="shim",
        meanings=["house", "dwelling"],
        provenance=[p1],
    )
    # Different sense/meaning
    e2 = VocabularyEntry(
        id="V-2",
        headword="shim",
        meanings=["family lineage"],
        provenance=[p2],
    )

    # Distinct senses should NOT be merged destructively
    result = deduplicate_entries([e1, e2])
    assert len(result) == 2


def test_deduplication_merges_identical_sense_and_preserves_provenance() -> None:
    p1 = ProvenanceRecord(source_id="SRC-1", resource_type="dictionaries", citation="Dict 1, p. 10")
    p2 = ProvenanceRecord(source_id="SRC-2", resource_type="books", citation="Book 1, p. 20")

    e1 = VocabularyEntry(
        id="V-1",
        headword="haora",
        meanings=["traditional woven shawl"],
        provenance=[p1],
    )
    e2 = VocabularyEntry(
        id="V-2",
        headword="haora",
        meanings=["traditional woven shawl"],
        alternative_spellings=["haorah"],
        provenance=[p2],
    )

    result = deduplicate_entries([e1, e2])
    assert len(result) == 1
    merged = result[0]
    assert len(merged.provenance) == 2
    assert "haorah" in merged.alternative_spellings
