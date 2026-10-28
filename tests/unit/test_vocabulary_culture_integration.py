"""Unit tests for integration between the Culture Module and the shared vocabulary database."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository, VocabularyRepository


def test_cultural_vocabulary_extraction_and_provenance_enrichment(tmp_path: Path) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    culture_repo = CultureRepository(db_manager)

    # 1. Pre-existing vocabulary entry previously catalogued from a dictionary
    dict_prov = ProvenanceRecord(
        source_id="DIC-HIST-001",
        resource_type="dictionaries",
        citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 280",
        page_or_section="p. 280",
        context_sentence="Awunga hi Hunphunli wui awunga ma.",
        permission_status="public_domain",
    )
    existing_vocab = VocabularyEntry(
        id="VOCAB-DIC-001",
        headword="awunga",
        meanings=["chief", "hereditary king"],
        translations_en=["chief", "king"],
        part_of_speech="noun",
        provenance=[dict_prov],
        verification_status="verified",
    )
    vocab_repo.add(existing_vocab)

    # 2. Add an authentic cultural record containing "Awunga"
    cult_rec = CulturalRecord(
        id="CULT-RIT-002",
        title="Luira Shimlut-Kaphung Sod-Turning Rite",
        local_name="Shimlut-Kaphung",
        category="ritual",
        subcategory="agricultural",
        original_text="Awunga shimlut kaphung phanitli.",
        translation_en="Ceremonial First Sowing Ritual by the Village Chief",
        village="Hunphun",
        dialect="Hunphun / Ukhrul",
        year=1977,
        source_id="Horam-1977-Ch5",
        source_title="Social and Cultural Life of the Nagas (Horam 1977)",
        source_page="p. 88",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
    )
    culture_repo.add(cult_rec)

    # 3. Synchronize cultural record candidate terms to shared vocabulary
    synced = culture_repo.sync_record_to_vocabulary(cult_rec, vocab_repo)
    assert len(synced) > 0

    # Verify existing entry was enriched with culture provenance without destroying definitions
    awunga_entries = vocab_repo.search_by_headword("awunga")
    assert len(awunga_entries) >= 1
    enriched_entry = awunga_entries[0]
    assert enriched_entry.headword.lower() == "awunga"
    assert "chief" in enriched_entry.meanings

    # Confirm provenance contains both dictionary and culture records
    prov_types = [p.resource_type for p in enriched_entry.provenance]
    assert "dictionaries" in prov_types
    assert "culture" in prov_types

    cult_prov = next(p for p in enriched_entry.provenance if p.resource_type == "culture")
    assert cult_prov.source_id == "CULT-RIT-002"
    assert "Luira Shimlut-Kaphung" in cult_prov.citation


def test_restricted_culture_record_does_not_leak_into_vocabulary(tmp_path: Path) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    culture_repo = CultureRepository(db_manager)

    restricted_rec = CulturalRecord(
        id="CULT-RIT-SECRET",
        title="Restricted Clan Incantation",
        category="ritual",
        original_text="EsotericSecretWord kachang",
        permission_status="restricted",
        access_status="restricted",
        verification_status="verified",
    )
    culture_repo.add(restricted_rec)

    # Attempting to sync restricted record must be blocked
    with pytest.raises(PermissionDeniedError, match="Cannot sync restricted cultural record"):
        culture_repo.sync_record_to_vocabulary(restricted_rec, vocab_repo)

    # Verify no leaked word entered the shared vocabulary
    results = vocab_repo.search_by_headword("EsotericSecretWord")
    assert len(results) == 0
