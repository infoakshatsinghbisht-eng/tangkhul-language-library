"""Unit tests for integration between the Literature Module and the shared vocabulary database."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, VocabularyRepository


def test_literary_vocabulary_extraction_and_provenance_enrichment(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    literature_repo = LiteratureRepository(db_manager)

    # 1. Pre-existing vocabulary entry previously catalogued from a dictionary
    dict_prov = ProvenanceRecord(
        source_id="DIC-PETT-001",
        resource_type="dictionaries",
        citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 115",
        page_or_section="p. 115",
        context_sentence="Leikashi hi phaning ngasak kaji wui tuitui.",
        permission_status="public_domain",
    )
    existing_vocab = VocabularyEntry(
        id="VOCAB-DIC-LIT-001",
        headword="leikashi",
        meanings=["love", "affection", "compassion"],
        translations_en=["love", "affection"],
        part_of_speech="noun",
        provenance=[dict_prov],
        verification_status="verified",
    )
    vocab_repo.add(existing_vocab)

    # 2. Add an authentic literary record containing "leikashi"
    lit_rec = LiteraryRecord(
        id="LIT-POEM-SYN-001",
        title="Ava Ram Leishat",
        original_title="Ava Ram Leishat",
        work_type="poem",
        author="Luingam A. Shimray",
        original_text="Iramwui ngalungli leikashi mayonser.",
        translation_text="In our ancestral land love blossoms everywhere.",
        publication_year=2000,
        permission_status="permitted",
        access_status="metadata_only",
        text_availability="excerpt",
        verification_status="verified",
    )
    literature_repo.add(lit_rec)

    # 3. Synchronize literary record into shared vocabulary
    synced = literature_repo.sync_record_to_vocabulary(lit_rec, vocab_repo)
    assert len(synced) > 0

    # 4. Verify existing lemma "leikashi" has enriched provenance
    leikashi_matches = vocab_repo.search_by_headword("leikashi")
    assert len(leikashi_matches) >= 1
    leikashi_entry = next(e for e in leikashi_matches if e.headword.lower() == "leikashi")

    # Should retain original dictionary provenance and append literature provenance
    assert len(leikashi_entry.provenance) >= 2
    prov_sources = [p.source_id for p in leikashi_entry.provenance]
    prov_types = [p.resource_type for p in leikashi_entry.provenance]
    assert "DIC-PETT-001" in prov_sources
    assert "LIT-POEM-SYN-001" in prov_sources
    assert "dictionaries" in prov_types
    assert "literature" in prov_types

    # 5. Verify new candidate vocabulary entries were created
    iramwui_matches = vocab_repo.search_by_headword("iramwui")
    assert len(iramwui_matches) >= 1
    iramwui_entry = iramwui_matches[0]
    assert iramwui_entry.verification_status == "unverified"
    assert len(iramwui_entry.provenance) == 1
    assert iramwui_entry.provenance[0].source_id == "LIT-POEM-SYN-001"
    assert iramwui_entry.provenance[0].resource_type == "literature"


def test_restricted_literary_record_blocks_vocabulary_sync(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "test_corpus_restr.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    literature_repo = LiteratureRepository(db_manager)

    restricted_rec = LiteraryRecord(
        id="LIT-RESTR-SYN-001",
        title="Restricted Modern Verse",
        work_type="poem",
        original_text="Confidential unpublished poem.",
        permission_status="restricted",
        access_status="restricted",
    )

    with pytest.raises(PermissionDeniedError, match="Cannot sync restricted"):
        literature_repo.sync_record_to_vocabulary(restricted_rec, vocab_repo)

    # Ensure no tokens leaked
    tokens = literature_repo.get_extracted_tokens("LIT-RESTR-SYN-001")
    assert len(tokens) == 0
