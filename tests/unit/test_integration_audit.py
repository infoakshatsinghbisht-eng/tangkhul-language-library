"""Regression and quality audit tests for Step 8 integration audit.

Covers:
- Cross-manifest duplicate ID validation
- Storage and vocabulary sync idempotency (provenance & tokens)
- Permission gating and restricted content leak prevention
- Unicode normalization and Tangkhul character preservation
- Manifest verification status distribution
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import ManifestValidationError, PermissionDeniedError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord
from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.ingestion.metadata_validation import (
    validate_all_manifests,
    validate_manifest_file,
)
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    CultureRepository,
    DictionaryRepository,
    HistoryRepository,
    LiteratureRepository,
    VocabularyRepository,
)
from tangkhul_lib.vocabulary.normalization import normalize_unicode


def test_cross_manifest_duplicate_detection(tmp_path: Path) -> None:
    """Ensure duplicate IDs across two different manifest files trigger validation error."""
    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir()

    f1 = manifest_dir / "books.jsonl"
    f2 = manifest_dir / "songs.jsonl"

    rec1 = {
        "id": "COLLISION-001",
        "resource_type": "books",
        "title": "Book with Collision",
        "creator": "Author A",
        "year": 1990,
        "permission_status": "permitted",
        "verification_status": "verified",
    }
    rec2 = {
        "id": "COLLISION-001",
        "resource_type": "songs",
        "title": "Song with Same ID",
        "creator": "Performer B",
        "year": 1995,
        "permission_status": "permitted",
        "verification_status": "verified",
    }

    f1.write_text(json.dumps(rec1) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(rec2) + "\n", encoding="utf-8")

    # Single file validations should pass individually
    assert len(validate_manifest_file(f1)) == 1
    assert len(validate_manifest_file(f2)) == 1

    # Cross-manifest validation must detect the global ID collision
    err_match = "Cross-manifest duplicate record ID 'COLLISION-001'"
    with pytest.raises(ManifestValidationError, match=err_match):
        validate_all_manifests(manifest_dir)


def test_vocabulary_repository_add_idempotency(tmp_path: Path) -> None:
    """Repeatedly calling VocabularyRepository.add() updates cleanly without duplicating prov."""
    db_file = tmp_path / "audit_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    vocab_repo = VocabularyRepository(db_manager)

    entry = VocabularyEntry(
        id="VOC-AUDIT-001",
        headword="ngashān",
        meanings=["custom", "cultural practice"],
        translations_en=["custom", "tradition"],
        dialect="Ukhrul",
        provenance=[
            ProvenanceRecord(
                source_id="CULT-CUST-001",
                resource_type="culture",
                citation="Customary Practice",
                page_or_section="p. 10",
                permission_status="community_authorized",
            )
        ],
    )

    # First add
    vocab_repo.add(entry)
    retrieved1 = vocab_repo.get_by_id("VOC-AUDIT-001")
    assert retrieved1 is not None
    assert len(retrieved1.provenance) == 1

    # Second add with same entry
    vocab_repo.add(entry)
    retrieved2 = vocab_repo.get_by_id("VOC-AUDIT-001")
    assert retrieved2 is not None
    assert len(retrieved2.provenance) == 1, "Provenance rows must not duplicate on repeated add()"

    # Third add after appending a second distinct provenance
    entry.provenance.append(
        ProvenanceRecord(
            source_id="HIST-DOC-001",
            resource_type="history",
            citation="Historical Chronicle",
            page_or_section="p. 25",
            permission_status="community_authorized",
        )
    )
    vocab_repo.add(entry)
    retrieved3 = vocab_repo.get_by_id("VOC-AUDIT-001")
    assert retrieved3 is not None
    assert len(retrieved3.provenance) == 2


def test_culture_sync_idempotency(tmp_path: Path) -> None:
    """Repeated sync of cultural records does not duplicate provenance or tokens."""
    db_file = tmp_path / "culture_audit.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    culture_repo = CultureRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    record = CulturalRecord(
        id="CULT-AUDIT-001",
        title="Customary Proverb on Truth",
        category="proverb",
        original_text="Kachang khaleiya tui",
        translation_en="The word that is true",
        dialect="Ukhrul",
        year=1980,
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
    )
    culture_repo.add(record)

    # First sync
    culture_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens1 = culture_repo.get_extracted_tokens(record.id)
    assert len(tokens1) > 0

    vocab_entries1 = vocab_repo.search_by_headword("kachang")
    assert len(vocab_entries1) >= 1
    prov_count1 = len(vocab_entries1[0].provenance)

    # Second sync (idempotency check)
    culture_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens2 = culture_repo.get_extracted_tokens(record.id)
    assert len(tokens2) == len(tokens1), "Extracted tokens must not duplicate on repeated sync"

    vocab_entries2 = vocab_repo.search_by_headword("kachang")
    assert len(vocab_entries2) >= 1
    assert len(vocab_entries2[0].provenance) == prov_count1, (
        "Provenance records must not duplicate on repeated sync"
    )


def test_history_sync_idempotency(tmp_path: Path) -> None:
    """Repeated sync of historical records does not duplicate provenance or tokens."""
    db_file = tmp_path / "history_audit.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    history_repo = HistoryRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    record = HistoricalRecord(
        id="HIST-AUDIT-001",
        title="Historical Peace Treaty",
        record_type="historical_document",
        summary="Historic treaty between villages",
        original_text="Phungcham Hundung ningkham khangasam",
        sort_year=1920,
        dialect="Standard Tangkhul",
        permission_status="community_authorized",
        verification_status="verified",
    )
    history_repo.add(record)

    # Sync once
    history_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens1 = history_repo.get_extracted_tokens(record.id)

    # Sync twice
    history_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens2 = history_repo.get_extracted_tokens(record.id)
    assert len(tokens2) == len(tokens1)

    matching = vocab_repo.search_by_headword("ningkham")
    assert len(matching) >= 1
    assert len(matching[0].provenance) == 1


def test_literature_sync_idempotency(tmp_path: Path) -> None:
    """Repeated sync of literary records does not duplicate provenance or tokens."""
    db_file = tmp_path / "lit_audit.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    lit_repo = LiteratureRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    record = LiteraryRecord(
        id="LIT-AUDIT-001",
        title="Spring Poem",
        work_type="poem",
        original_text="Kaphung kazing rali mayaron kakhang",
        publication_year=1965,
        dialect="Ukhrul",
        permission_status="permitted",
        verification_status="verified",
    )
    lit_repo.add(record)

    # First sync
    lit_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens1 = lit_repo.get_extracted_tokens(record.id)

    # Second sync
    lit_repo.sync_record_to_vocabulary(record, vocab_repo)
    tokens2 = lit_repo.get_extracted_tokens(record.id)
    assert len(tokens2) == len(tokens1)

    matching = vocab_repo.search_by_headword("kazing")
    assert len(matching) >= 1
    assert len(matching[0].provenance) == 1


def test_dictionary_sync_idempotency(tmp_path: Path) -> None:
    """Ensure repeated dictionary entry sync does not duplicate provenance."""
    from tangkhul_lib.dictionaries.models import DictionarySourceRecord

    db_file = tmp_path / "dict_audit.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    dict_repo = DictionaryRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    # Add parent dictionary source first to satisfy foreign key constraint
    source = DictionarySourceRecord(
        id="DIC-AUDIT-SRC",
        title="Audit Dictionary Source",
        languages=["Tangkhul", "English"],
        language_pair="Tangkhul-English",
        dialect="Ukhrul",
        permission_status="community_authorized",
        verification_status="verified",
    )
    dict_repo.add(source)

    entry = DictionaryEntryRecord(
        id="DIC-AUDIT-E01",
        dictionary_id="DIC-AUDIT-SRC",
        headword="shimkhur",
        definitions_en=["family", "household clan"],
        dialect="Ukhrul",
        page_or_section="p. 45",
        permission_status="community_authorized",
        verification_status="verified",
    )

    # Sync first time
    v1 = dict_repo.sync_entry_to_vocabulary(entry, vocab_repo)
    assert len(v1.provenance) == 1

    # Sync second time
    v2 = dict_repo.sync_entry_to_vocabulary(entry, vocab_repo)
    assert len(v2.provenance) == 1, "Duplicate provenance must not be appended on repeat sync"


def test_restricted_records_blocked_from_vocabulary_sync(tmp_path: Path) -> None:
    """Restricted records must raise PermissionDeniedError across Culture, History, Literature."""
    db_file = tmp_path / "perm_audit.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    culture_repo = CultureRepository(db_manager)
    history_repo = HistoryRepository(db_manager)
    lit_repo = LiteratureRepository(db_manager)
    vocab_repo = VocabularyRepository(db_manager)

    cult_rec = CulturalRecord(
        id="CULT-SECRET-001",
        title="Sacred Clan Rite",
        category="ritual",
        original_text="Secret text",
        permission_status="restricted",
    )
    with pytest.raises(PermissionDeniedError, match="Cannot sync restricted cultural record"):
        culture_repo.sync_record_to_vocabulary(cult_rec, vocab_repo)

    hist_rec = HistoricalRecord(
        id="HIST-SECRET-001",
        title="Classified Historical Inscription",
        record_type="historical_document",
        original_text="Protected text",
        permission_status="restricted",
    )
    with pytest.raises(PermissionDeniedError, match="Cannot sync restricted historical record"):
        history_repo.sync_record_to_vocabulary(hist_rec, vocab_repo)

    lit_rec = LiteraryRecord(
        id="LIT-SECRET-001",
        title="Restricted Manuscript",
        work_type="manuscript",
        original_text="Restricted literature",
        permission_status="restricted",
    )
    with pytest.raises(PermissionDeniedError, match="Cannot sync restricted literary work"):
        lit_repo.sync_record_to_vocabulary(lit_rec, vocab_repo)


def test_unicode_and_tangkhul_character_preservation() -> None:
    """Ensure Tangkhul macrons and spelling distinctions are preserved under normalization."""
    # Tangkhul words with macrons
    words = [
        "ngavā",      # bird
        "ngashān",   # custom
        "kachipāt",  # separation
        "vā",        # go
        "sā",        # animal / make
        "yām",       # run
        "thā",       # moon / month
        "khamor",    # mouth
    ]
    for w in words:
        norm = normalize_unicode(w)
        assert norm == w, f"Normalization modified Tangkhul word with macron: {w} -> {norm}"

    # Verify that NFC normalization preserves combining diacritics
    decomposed = "nga\u0076a\u0304"  # ngavā in NFD
    composed = normalize_unicode(decomposed)
    assert composed == "ngavā"


def test_actual_repository_manifests_integrity() -> None:
    """Audit the real data/manifests/ directory for ID uniqueness and record count integrity."""
    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_dir = project_root / "data" / "manifests"

    assert manifest_dir.is_dir()
    manifest_map = validate_all_manifests(manifest_dir)

    expected_counts = {
        "books.jsonl": 35,
        "culture.jsonl": 35,
        "dictionaries.jsonl": 16,
        "history.jsonl": 32,
        "literature.jsonl": 60,
        "songs.jsonl": 48,
    }

    total_records = 0
    all_ids: set[str] = set()

    for filename, expected_len in expected_counts.items():
        assert filename in manifest_map, f"Missing manifest: {filename}"
        recs = manifest_map[filename]
        assert len(recs) == expected_len, (
            f"Manifest {filename} expected {expected_len} records, got {len(recs)}"
        )
        total_records += len(recs)
        for r in recs:
            assert r.id not in all_ids, f"Global duplicate ID found: {r.id}"
            all_ids.add(r.id)

    assert total_records == 226
    assert len(all_ids) == 226

