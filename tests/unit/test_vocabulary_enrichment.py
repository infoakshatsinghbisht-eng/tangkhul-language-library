"""Unit and integration tests for Step 13 vocabulary enrichment pipeline and CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tangkhul_lib.cli import main
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import VocabularyRepository
from tangkhul_lib.vocabulary.enrichment import (
    VocabularyEnrichmentPipeline,
    classify_lexical_categories,
)


@pytest.fixture
def temp_db(tmp_path: Path) -> DatabaseManager:
    """Create an isolated, schema-initialized temporary SQLite database."""
    db_file = tmp_path / "test_corpus.sqlite"
    db_mgr = DatabaseManager(db_file)
    db_mgr.initialize_schema()
    return db_mgr


@pytest.fixture
def mock_config() -> LibraryConfig:
    """Create a test library configuration."""
    return LibraryConfig.from_environment()


@pytest.fixture
def enrichment_pipeline(
    temp_db: DatabaseManager,
    mock_config: LibraryConfig,
) -> VocabularyEnrichmentPipeline:
    """Instantiate VocabularyEnrichmentPipeline with temporary database."""
    return VocabularyEnrichmentPipeline(db_manager=temp_db, config=mock_config)


def test_permission_evaluation_tiers(enrichment_pipeline: VocabularyEnrichmentPipeline):
    """Test permission checks for public domain, restricted, and pending sources."""
    # 1. Public domain source is eligible
    res_pub = enrichment_pipeline.evaluate_source("DIC-HIST-001")
    assert res_pub["is_eligible"] is True
    assert res_pub["permission_status"] == "public_domain"
    assert res_pub["skip_reason"] is None

    # 2. Restricted modern dictionary is blocked
    res_restr = enrichment_pipeline.evaluate_source("DIC-TLS-001")
    assert res_restr["is_eligible"] is False
    assert res_restr["permission_status"] == "restricted"
    assert "restricted" in res_restr["skip_reason"].lower()

    # 3. Pending candidate glossary is blocked
    res_pend = enrichment_pipeline.evaluate_source("DIC-CAND-001")
    assert res_pend["is_eligible"] is False
    assert res_pend["verification_status"] == "needs_review"
    assert "needs_review" in res_pend["skip_reason"].lower()


def test_permission_denied_exception_on_preview(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
):
    """Test that previewing a restricted source raises PermissionDeniedError."""
    with pytest.raises(PermissionDeniedError) as exc_info:
        enrichment_pipeline.preview_source("DIC-TLS-001")
    assert "DIC-TLS-001" in str(exc_info.value)
    assert exc_info.value.permission_status == "restricted"


def test_structured_tsv_dictionary_extraction(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Test extracting lexical entries from an authentic TSV dictionary file."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    tsv_path = fixtures / "sample_pettigrew_dictionary.tsv"
    assert tsv_path.is_file(), f"Fixture missing: {tsv_path}"

    summary = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tsv_path,
        dry_run=False,
    )

    assert summary.status == "completed"
    assert summary.source_id == "DIC-HIST-001"
    assert summary.items_extracted >= 15
    assert summary.candidates_created >= 15
    assert summary.entries_updated == 0

    # Verify candidates in VocabularyRepository
    vocab_repo = VocabularyRepository(temp_db)
    entries = vocab_repo.list_all()
    headwords = {e.headword for e in entries}

    assert "khamatha" in headwords
    assert "shim" in headwords
    assert "akha" in headwords
    assert "luira" in headwords
    assert "shirui" in headwords

    # Verify provenance
    khamatha_entry = next(e for e in entries if e.headword == "khamatha")
    assert "good" in khamatha_entry.meanings[0].lower()
    assert khamatha_entry.dialect == "Ukhrul"
    assert khamatha_entry.part_of_speech == "adj"
    assert khamatha_entry.verification_status == "needs_review"
    assert khamatha_entry.review_status == "pending_review"
    assert len(khamatha_entry.provenance) == 1
    assert khamatha_entry.provenance[0].source_id == "DIC-HIST-001"
    assert "142" in (khamatha_entry.provenance[0].page_or_section or "")


def test_structured_jsonl_dialect_glossary_extraction(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Test extracting multi-dialect entries from a JSON Lines glossary file."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    jsonl_path = fixtures / "sample_dialect_glossary.jsonl"
    assert jsonl_path.is_file()

    summary = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=jsonl_path,
        dry_run=False,
    )

    assert summary.status == "completed"
    assert summary.items_extracted == 4
    assert "Phungcham" in summary.dialect_breakdown
    assert "Champhung" in summary.dialect_breakdown
    assert "Hundung" in summary.dialect_breakdown

    vocab_repo = VocabularyRepository(temp_db)
    entries = vocab_repo.list_all()
    headwords = {e.headword: e for e in entries}

    assert "kongrei" in headwords
    assert headwords["kongrei"].dialect == "Phungcham"
    assert "great river" in headwords["kongrei"].meanings

    assert "lengvai" in headwords
    assert headwords["lengvai"].dialect == "Champhung"


def test_formatted_text_line_parser_extraction(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Test extracting entries from formatted dictionary text lines."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    txt_path = fixtures / "sample_dictionary_text_lines.txt"
    assert txt_path.is_file()

    summary = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=txt_path,
        dry_run=False,
    )

    assert summary.status == "completed"
    assert summary.extraction_method == "text_line_parser"
    assert summary.items_extracted >= 8

    vocab_repo = VocabularyRepository(temp_db)
    entries = {e.headword: e for e in vocab_repo.list_all()}

    assert "kathum" in entries
    assert "three" in entries["kathum"].meanings[0].lower()
    assert entries["kathum"].part_of_speech == "num"


def test_running_text_lexicon_extraction(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Test extracting candidate vocabulary from running text without assuming meanings."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    txt_path = fixtures / "sample_tangkhul_book.txt"
    assert txt_path.is_file()

    summary = enrichment_pipeline.enrich_from_source(
        source_id="BK-HIST-001",
        file_path=txt_path,
        dry_run=False,
    )

    assert summary.status == "completed"
    assert "running_text" in summary.extraction_method
    assert summary.items_extracted > 0

    vocab_repo = VocabularyRepository(temp_db)
    entries = vocab_repo.list_all()

    # Running text tokens must not invent or fabricate meanings!
    for e in entries:
        assert e.meanings == [], f"Running text candidate '{e.headword}' has fabricated meanings"
        assert e.verification_status == "unverified"
        assert e.review_status == "pending_review"
        assert len(e.example_sentences) >= 1


def test_conservative_duplicate_suggestions(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Verify phonetic and fuzzy duplicates are suggested rather than automatically merged."""
    vocab_repo = VocabularyRepository(temp_db)

    # Pre-populate a canonical verified entry
    canonical = VocabularyEntry(
        id="VOCAB-CANONICAL-001",
        headword="ngashan",
        meanings=["epoch", "generation"],
        translations_en=["epoch", "generation"],
        alternative_spellings=["ngashang"],
        dialect_variants=[],
        dialect="Ukhrul",
        example_sentences=["Ngashan akha khani thot."],
        provenance=[
            ProvenanceRecord(
                source_id="DIC-HIST-001",
                resource_type="dictionaries",
                citation="Pettigrew 1918",
                permission_status="public_domain",
            )
        ],
        verification_status="verified",
    )
    vocab_repo.add(canonical)

    # Now create candidate with phonetic/orthographic variation 'ngasan'
    tsv_content = (
        "headword\tpart_of_speech\tdefinitions_en\tdialect\n"
        "ngasan\tnoun\tgeneration; age\tUkhrul\n"
    )
    tmp_file = temp_db.db_path.parent / "test_dup.tsv"
    tmp_file.write_text(tsv_content, encoding="utf-8")

    summary = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tmp_file,
        dry_run=True,
    )

    assert len(summary.duplicate_suggestions) > 0
    dup = summary.duplicate_suggestions[0]
    assert dup["candidate_headword"] == "ngasan"
    assert dup["matching_headword"] == "ngashan"
    assert dup["matching_entry_id"] == "VOCAB-CANONICAL-001"
    assert dup["match_type"] in {"phonetic", "fuzzy"}


def test_updating_verified_entry_preserves_human_definitions(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Verify that enriching an existing verified entry does not overwrite verified definitions."""
    vocab_repo = VocabularyRepository(temp_db)

    initial_entry = VocabularyEntry(
        id="VOCAB-TEST-001",
        headword="khamatha",
        meanings=["Curated High-Value Definition"],
        translations_en=["Curated High-Value Definition"],
        alternative_spellings=[],
        dialect_variants=[],
        dialect="Ukhrul",
        example_sentences=["Initial example."],
        provenance=[
            ProvenanceRecord(
                source_id="INITIAL-001",
                resource_type="books",
                citation="Initial Source",
                permission_status="public_domain",
            )
        ],
        verification_status="verified",
        review_status="accepted",
        reviewer="Elder-Reviewer",
    )
    vocab_repo.add(initial_entry)

    # Ingest candidate with exact headword but new translation
    tsv_content = (
        "headword\tpart_of_speech\tdefinitions_en\tdialect\tpage\n"
        "khamatha\tadj\tnew secondary gloss\tUkhrul\tp. 50\n"
    )
    tmp_file = temp_db.db_path.parent / "test_update.tsv"
    tmp_file.write_text(tsv_content, encoding="utf-8")

    summary = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tmp_file,
        dry_run=False,
    )

    assert summary.entries_updated == 1
    updated = vocab_repo.get_by_id("VOCAB-TEST-001")
    assert updated is not None

    # Verified definition must NOT be overwritten!
    assert updated.meanings[0] == "Curated High-Value Definition"
    assert updated.verification_status == "verified"
    assert updated.reviewer == "Elder-Reviewer"
    # Provenance citation must be added
    assert len(updated.provenance) == 2
    assert any(p.source_id == "DIC-HIST-001" for p in updated.provenance)


def test_dry_run_and_idempotence(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
):
    """Test dry-run simulation and idempotent reprocessing checks."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    tsv_path = fixtures / "sample_pettigrew_dictionary.tsv"
    vocab_repo = VocabularyRepository(temp_db)

    # 1. Dry run
    summary_dry = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tsv_path,
        dry_run=True,
    )
    assert summary_dry.status == "dry_run"
    assert summary_dry.items_extracted >= 15
    assert len(vocab_repo.list_all()) == 0  # Nothing written to database!

    # 2. Live run
    summary_live = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tsv_path,
        dry_run=False,
    )
    assert summary_live.status == "completed"
    count_after_live = len(vocab_repo.list_all())
    assert count_after_live >= 15

    # 3. Idempotent re-run on unchanged file
    summary_re = enrichment_pipeline.enrich_from_source(
        source_id="DIC-HIST-001",
        file_path=tsv_path,
        dry_run=False,
        force=False,
    )
    assert summary_re.already_processed is True
    assert len(vocab_repo.list_all()) == count_after_live  # No duplicate entries!


def test_category_classification_and_data_gaps():
    """Test classification of lexical items into categories and reporting data gaps."""
    # Noun, Agriculture, Tools
    cats_basket = classify_lexical_categories(
        headword="longkhor",
        meanings=["conical bamboo basket for carrying grain"],
        part_of_speech="noun",
        dialect="Ukhrul",
    )
    assert "nouns" in cats_basket
    assert "tools_craft" in cats_basket
    assert "food_agriculture" in cats_basket

    # Number
    cats_num = classify_lexical_categories(
        headword="kathum",
        meanings=["numeral three"],
        part_of_speech="num",
    )
    assert "numbers_time" in cats_num

    # Kinship
    cats_fam = classify_lexical_categories(
        headword="ava",
        meanings=["father; male parent"],
        part_of_speech="noun",
    )
    assert "family_kinship" in cats_fam
    assert "nouns" in cats_fam


def test_candidate_export_with_restricted_shielding(
    enrichment_pipeline: VocabularyEnrichmentPipeline,
    temp_db: DatabaseManager,
    tmp_path: Path,
):
    """Test candidate export shields restricted sentences."""
    vocab_repo = VocabularyRepository(temp_db)

    cand = VocabularyEntry(
        id="VOCAB-EXPORT-001",
        headword="khamasit",
        meanings=["sacred village taboo"],
        translations_en=["sacred village taboo"],
        alternative_spellings=[],
        dialect_variants=[],
        dialect="Ukhrul",
        example_sentences=["Secret incantation sentence."],
        provenance=[
            ProvenanceRecord(
                source_id="CULT-RIT-001",
                resource_type="culture",
                citation="Sacred Taboo Rites",
                context_sentence="Secret incantation sentence.",
                permission_status="restricted",
            )
        ],
        verification_status="needs_review",
        review_status="pending_review",
    )
    vocab_repo.add(cand)

    out_jsonl = tmp_path / "exported_candidates.jsonl"
    count = enrichment_pipeline.export_candidates(output_path=out_jsonl)
    assert count == 1
    assert out_jsonl.is_file()

    with out_jsonl.open("r", encoding="utf-8") as f:
        line = json.loads(f.readline())
        assert line["entry_id"] == "VOCAB-EXPORT-001"
        prov = line["provenance"][0]
        assert prov["context_sentence"] == "[RESTRICTED TEXT - ACCESS PRIVILEGED]"


def test_cli_enrich_smoke(capsys: pytest.CaptureFixture):
    """Smoke test CLI enrich subcommands."""
    fixtures = Path(__file__).resolve().parent.parent / "fixtures"
    tsv_path = fixtures / "sample_pettigrew_dictionary.tsv"

    # 1. List sources
    ret = main(["enrich", "--list-sources"])
    assert ret == 0
    out = capsys.readouterr().out
    assert "TANGKHUL VOCABULARY ENRICHMENT SOURCES" in out
    assert "DIC-HIST-001" in out

    # 2. Preview source
    preview_args = [
        "enrich",
        "--preview",
        "--source-id",
        "DIC-HIST-001",
        "--file",
        str(tsv_path),
        "--limit",
        "3",
    ]
    ret = main(preview_args)
    assert ret == 0
    out = capsys.readouterr().out
    assert "PREVIEW ENRICHMENT:" in out
    assert "sample_pettigrew_dictionary.tsv" in out

    # 3. Dry-run enrichment
    enrich_args = [
        "enrich",
        "--source-id",
        "DIC-HIST-001",
        "--file",
        str(tsv_path),
        "--dry-run",
        "--show-duplicates",
    ]
    ret = main(enrich_args)
    assert ret == 0
    out = capsys.readouterr().out
    assert "[DRY-RUN]" in out
    assert "VOCABULARY ENRICHMENT REPORT:" in out
    assert "Lexical & Grammatical Categories:" in out

    # 4. Summary
    ret = main(["enrich", "--summary"])
    assert ret == 0
