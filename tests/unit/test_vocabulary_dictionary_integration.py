"""Unit tests for integration between dictionaries and the shared vocabulary database."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import DictionaryRepository, VocabularyRepository
from tangkhul_lib.vocabulary.search import VocabularySearchEngine


def test_cross_module_vocabulary_and_provenance_enrichment(tmp_path: Path) -> None:
    db_file = tmp_path / "corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)
    dict_repo = DictionaryRepository(db_manager)

    # 1. Existing vocabulary entry previously harvested from a book
    book_prov = ProvenanceRecord(
        source_id="BK-TLS-007",
        resource_type="books",
        citation="Tangkhul Tuitam (2000), p. 15",
        page_or_section="p. 15",
        context_sentence="Ava vashungra ngasoda khararchan maranli.",
        permission_status="community_authorized",
    )
    existing_vocab = VocabularyEntry(
        id="VOCAB-BK-001",
        headword="khararchan",
        meanings=["story of ancient ancestors"],
        translations_en=["ancestral story"],
        part_of_speech="noun",
        provenance=[book_prov],
        verification_status="verified",
    )
    vocab_repo.add(existing_vocab)

    # Dictionary source record
    from tangkhul_lib.dictionaries.models import DictionarySourceRecord

    dict_src = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    dict_repo.add(dict_src)

    # 2. Authentic dictionary entry from William Pettigrew 1918
    dict_entry = DictionaryEntryRecord(
        id="DIC-HIST-001-ENT-0042",
        dictionary_id="DIC-HIST-001",
        headword="khararchan",
        definitions_en=["folk-tale", "legend", "fable"],
        part_of_speech="noun",
        page_or_section="p. 320",
        examples=["Khararchan hili phanitwui tui kharara."],
        permission_status="public_domain",
        verification_status="verified",
    )

    # 3. Synchronize dictionary entry into unified vocabulary repository
    synced_vocab = dict_repo.sync_entry_to_vocabulary(dict_entry, vocab_repo)

    # 4. Verify merged vocabulary entry
    assert synced_vocab.id == "VOCAB-BK-001"
    assert synced_vocab.headword == "khararchan"

    # Both book meaning and dictionary definitions must be preserved
    assert "ancestral story" in synced_vocab.translations_en
    assert "folk-tale" in synced_vocab.translations_en
    assert "legend" in synced_vocab.translations_en

    # Both provenance records must be retained!
    assert len(synced_vocab.provenance) == 2
    res_types = [p.resource_type for p in synced_vocab.provenance]
    assert "books" in res_types
    assert "dictionaries" in res_types

    dict_prov = next(p for p in synced_vocab.provenance if p.resource_type == "dictionaries")
    assert dict_prov.source_id == "DIC-HIST-001"
    assert dict_prov.page_or_section == "p. 320"

    # 5. Verify query via VocabularySearchEngine
    engine = VocabularySearchEngine(repository=vocab_repo)
    results_hw = engine.search_headword("khararchan")
    assert len(results_hw) == 1
    assert results_hw[0].headword == "khararchan"

    results_meaning = engine.search_meaning("folk-tale")
    assert len(results_meaning) == 1
    assert results_meaning[0].id == "VOCAB-BK-001"

    # Search by source provenance
    results_src = engine.search_by_source("DIC-HIST-001")
    assert len(results_src) == 1
    assert results_src[0].id == "VOCAB-BK-001"
