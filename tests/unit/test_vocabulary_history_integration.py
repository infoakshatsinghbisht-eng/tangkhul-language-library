"""Unit tests for integration between the History Module and the shared vocabulary database."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import HistoryRepository, VocabularyRepository


def test_historical_vocabulary_extraction_and_provenance_enrichment(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    history_repo = HistoryRepository(db_manager)

    # 1. Pre-existing vocabulary entry previously catalogued from a dictionary
    dict_prov = ProvenanceRecord(
        source_id="DIC-PETT-001",
        resource_type="dictionaries",
        citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 110",
        page_or_section="p. 110",
        context_sentence="Awunga hi Hunphun wui arui ma.",
        permission_status="public_domain",
    )
    existing_vocab = VocabularyEntry(
        id="VOCAB-DIC-HIST-001",
        headword="awunga",
        meanings=["chief", "hereditary leader"],
        translations_en=["chief", "village king"],
        part_of_speech="noun",
        provenance=[dict_prov],
        verification_status="verified",
    )
    vocab_repo.add(existing_vocab)

    # 2. Add an authentic historical record containing "Awunga" and toponym "Hunphun"
    hist_rec = HistoricalRecord(
        id="HIST-EVT-SYN-001",
        title="Rev. Pettigrew Reception by Chief Raihao",
        record_type="historical_event",
        original_text="Hunphun Awunga Raihao khipak-eili Rev. Pettigrew phungchan.",
        translation_en="Rev. Pettigrew arrived in Hunphun under the auspices of Chief Raihao.",
        event_date="February 1896",
        sort_year=1896,
        period="Colonial Era",
        place="Hunphun / Ukhrul",
        village="Hunphun",
        people_involved=["Awunga Raihao", "Rev. William Pettigrew"],
        source_id="HIST-HODSON-1911",
        source_title="The Naga Tribes of Manipur (Hodson 1911)",
        source_page="p. 42",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    history_repo.add(hist_rec)

    # 3. Synchronize historical record candidate terms to shared vocabulary
    synced = history_repo.sync_record_to_vocabulary(hist_rec, vocab_repo)
    assert len(synced) > 0

    # Verify existing entry was enriched with history provenance without overwriting definitions
    awunga_entries = vocab_repo.search_by_headword("awunga")
    assert len(awunga_entries) >= 1
    enriched_entry = awunga_entries[0]
    assert enriched_entry.headword.lower() == "awunga"
    assert "chief" in enriched_entry.meanings

    # Confirm provenance contains both dictionary and history records
    prov_types = [p.resource_type for p in enriched_entry.provenance]
    assert "dictionaries" in prov_types
    assert "history" in prov_types

    hist_prov = next(p for p in enriched_entry.provenance if p.resource_type == "history")
    assert hist_prov.source_id == "HIST-EVT-SYN-001"
    assert "Pettigrew Reception" in hist_prov.citation
    assert hist_prov.recorded_year == 1896

    # Verify newly created toponym entry (e.g. Hunphun)
    hunphun_entries = vocab_repo.search_by_headword("Hunphun")
    assert len(hunphun_entries) >= 1
    hunphun_rec = hunphun_entries[0]
    assert hunphun_rec.headword == "Hunphun"
    assert hunphun_rec.provenance[0].resource_type == "history"


def test_restricted_history_record_does_not_leak_into_vocabulary(tmp_path: Path) -> None:
    db_file = tmp_path / "test_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    history_repo = HistoryRepository(db_manager)

    restricted_rec = HistoricalRecord(
        id="HIST-SECRET-001",
        title="Restricted Clan Chronicle",
        record_type="historical_document",
        original_text="SecretClanWord kachang.",
        permission_status="restricted",
        access_status="restricted",
        verification_status="needs_review",
    )
    history_repo.add(restricted_rec)

    # Attempting to sync restricted historical record must raise PermissionDeniedError
    with pytest.raises(PermissionDeniedError, match="restricted"):
        history_repo.sync_record_to_vocabulary(restricted_rec, vocab_repo)

    # Verify restricted terms did not leak into the vocabulary database
    results = vocab_repo.search_by_headword("SecretClanWord")
    assert len(results) == 0

    # Verify extracted tokens were not saved for this restricted record
    tokens = history_repo.get_extracted_tokens("HIST-SECRET-001")
    assert len(tokens) == 0
