"""Comprehensive unit and integration tests for Vocabulary Review and Community Correction."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tangkhul_lib.cli import main
from tangkhul_lib.core.models import (
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    VocabularyRepository,
)
from tangkhul_lib.vocabulary.review import VocabularyReviewService


@pytest.fixture
def mem_db() -> DatabaseManager:
    """Provide an isolated in-memory DatabaseManager."""
    db = DatabaseManager(":memory:")
    db.initialize_schema()
    return db


@pytest.fixture
def sample_entries(mem_db: DatabaseManager) -> list[VocabularyEntry]:
    """Populate and return a representative set of vocabulary candidates."""
    repo = VocabularyRepository(mem_db)

    entries = [
        VocabularyEntry(
            id="VOCAB-TEST-001",
            headword="ngashān",
            meanings=["custom", "tradition"],
            alternative_spellings=["ngashan"],
            dialect="Ukhrul",
            part_of_speech="noun",
            example_sentences=["Tangkhul wui ngashan thotna."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Grammar & Dictionary, p. 12",
                    page_or_section="p. 12",
                    context_sentence="Tangkhul wui ngashan thotna.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="verified",
            review_status="accepted",
        ),
        VocabularyEntry(
            id="VOCAB-CAND-001",
            headword="ngashan",
            meanings=[],  # Missing meaning, candidate awaiting review
            alternative_spellings=[],
            dialect="Ukhrul",
            example_sentences=["Ngashan kaphungli lei."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Grammar & Dictionary, p. 45",
                    page_or_section="p. 45",
                    context_sentence="Ngashan kaphungli lei.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="unverified",
            review_status="pending_review",
        ),
        VocabularyEntry(
            id="VOCAB-CAND-002",
            headword="ngasan",  # Phonetic variant of ngashan
            meanings=[],
            dialect="Raphei",
            example_sentences=["Iram ngasan thada."],
            provenance=[
                ProvenanceRecord(
                    source_id="CULT-CUST-001",
                    resource_type="culture",
                    citation="Longshim System, p. 5",
                    page_or_section="p. 5",
                    context_sentence="Iram ngasan thada.",
                    recorded_year=1975,
                    permission_status="community_authorized",
                )
            ],
            verification_status="unverified",
            review_status="pending_review",
        ),
        VocabularyEntry(
            id="VOCAB-CAND-003",
            headword="khamasit_secret",
            meanings=["secret taboo rite"],
            dialect="Ukhrul",
            example_sentences=["Restricted sacred chant sentence."],
            provenance=[
                ProvenanceRecord(
                    source_id="CULT-RIT-001",
                    resource_type="culture",
                    citation="Khamasit Sacred Rituals, p. 1",
                    page_or_section="p. 1",
                    context_sentence="Restricted sacred chant sentence.",
                    recorded_year=1980,
                    permission_status="restricted",  # Restricted source
                )
            ],
            verification_status="needs_review",
            review_status="conflict",
            license_restrictions="restricted",
        ),
    ]

    for e in entries:
        repo.add(e)
    return entries


def test_review_queue_filtering_and_deterministic_order(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test review queue filtering by status, dialect, missing meanings, and deterministic order."""
    service = VocabularyReviewService(mem_db)

    # 1. Filter by review_status="pending_review"
    pending = service.get_review_queue(review_status="pending_review")
    assert len(pending) == 2
    assert all(e.review_status == "pending_review" for e in pending)

    # Verify deterministic ordering: headword asc / created_at asc
    assert [e.headword for e in pending] == ["ngasan", "ngashan"]

    # 2. Filter by missing meanings
    missing = service.get_review_queue(missing_meanings=True)
    assert len(missing) == 2
    assert all(len(e.meanings) == 0 for e in missing)

    # 3. Filter by dialect
    raphei = service.get_review_queue(dialect="Raphei")
    assert len(raphei) == 1
    assert raphei[0].headword == "ngasan"

    # 4. Filter by source_type="culture"
    cult = service.get_review_queue(source_type="culture")
    assert len(cult) == 2
    assert {e.id for e in cult} == {"VOCAB-CAND-002", "VOCAB-CAND-003"}


def test_duplicate_suggestions(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test exact, alternate-spelling, and phonetic duplicate suggestions."""
    service = VocabularyReviewService(mem_db)

    cand_ngashan = service.vocab_repo.get_by_id("VOCAB-CAND-001")
    assert cand_ngashan is not None

    dups = service.find_duplicate_suggestions(cand_ngashan, threshold=0.70)
    assert len(dups) >= 1

    # Should suggest VOCAB-TEST-001 because it has alternative_spelling "ngashan"
    exact_sugg = [d for d in dups if d["entry_id"] == "VOCAB-TEST-001"]
    assert len(exact_sugg) == 1
    assert exact_sugg[0]["score"] == 1.0


def test_candidate_details_and_restricted_shielding(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test candidate details display and shielding of restricted source context."""
    service = VocabularyReviewService(mem_db)

    # 1. Normal un-restricted candidate
    details_normal = service.get_candidate_details("VOCAB-CAND-001")
    assert details_normal["is_restricted"] is False
    assert "Ngashan kaphungli lei." in details_normal["provenance"][0]["context_sentence"]

    # 2. Restricted candidate
    details_restricted = service.get_candidate_details("VOCAB-CAND-003")
    assert details_restricted["is_restricted"] is True
    # Context sentence must be masked!
    assert "RESTRICTED TEXT" in details_restricted["provenance"][0]["context_sentence"]
    assert "RESTRICTED EXAMPLE" in details_restricted["safe_example_sentences"][0]


def test_accept_candidate_requires_reviewer_and_meanings(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test accept decision requires non-empty reviewer and confirmed meanings."""
    service = VocabularyReviewService(mem_db)

    # 1. Missing reviewer error
    with pytest.raises(ValueError, match="Reviewer identifier or pseudonym is required"):
        service.accept_candidate("VOCAB-CAND-001", reviewer="", meanings=["custom"])

    # 2. Missing meanings error (entry has no meanings and none supplied)
    with pytest.raises(ValueError, match="without at least one confirmed meaning"):
        service.accept_candidate("VOCAB-CAND-001", reviewer="Linguist-Alice", meanings=[])

    # 3. Successful acceptance
    updated = service.accept_candidate(
        "VOCAB-CAND-001",
        reviewer="Linguist-Alice",
        meanings=["custom", "tribal tradition"],
        pos="noun",
        notes="Confirmed from Pettigrew grammar p. 45",
    )
    assert updated.review_status == "accepted"
    assert updated.verification_status == "verified"
    assert updated.reviewer == "Linguist-Alice"
    assert "custom" in updated.meanings
    assert updated.part_of_speech == "noun"

    # Verify audit history
    history = service.review_repo.get_reviews_for_entry("VOCAB-CAND-001")
    assert len(history) == 1
    assert history[0].decision == "accept"
    assert history[0].reviewer == "Linguist-Alice"
    assert history[0].previous_state is not None
    assert history[0].new_state is not None


def test_reject_candidate_requires_reason(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test rejecting a candidate requires reviewer and diagnostic reason, and shields entry."""
    service = VocabularyReviewService(mem_db)

    # Missing reason
    with pytest.raises(ValueError, match="clear diagnostic reason is required"):
        service.reject_candidate("VOCAB-CAND-002", reviewer="Elder-Wung", reason="")

    # Successful rejection
    updated = service.reject_candidate(
        "VOCAB-CAND-002",
        reviewer="Elder-Wung",
        reason="OCR scanning artifact; non-lexical token.",
    )
    assert updated.review_status == "rejected"
    assert updated.verification_status == "unverified"
    assert updated.license_restrictions == "restricted"  # Excluded from search
    assert updated.reviewer == "Elder-Wung"
    assert updated.review_notes == "OCR scanning artifact; non-lexical token."

    history = service.review_repo.get_reviews_for_entry("VOCAB-CAND-002")
    assert len(history) == 1
    assert history[0].decision == "reject"
    assert history[0].reviewer == "Elder-Wung"


def test_flag_candidate_uncertain_and_conflict(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test flagging candidate as reviewed_uncertain or conflict."""
    service = VocabularyReviewService(mem_db)

    # Flag as uncertain
    updated = service.flag_candidate(
        "VOCAB-CAND-001",
        reviewer="Linguist-Bob",
        decision="reviewed_uncertain",
        notes="Unclear tone mark; requires native speaker consultation.",
    )
    assert updated.review_status == "reviewed_uncertain"
    assert updated.verification_status == "needs_review"
    assert updated.review_notes == "Unclear tone mark; requires native speaker consultation."

    # Flag as conflict
    updated_conf = service.flag_candidate(
        "VOCAB-CAND-001",
        reviewer="Linguist-Carol",
        decision="conflict",
        notes="Pettigrew lists noun, but village elder claims verbal usage.",
    )
    assert updated_conf.review_status == "conflict"
    assert updated_conf.verification_status == "needs_review"

    history = service.review_repo.get_reviews_for_entry("VOCAB-CAND-001")
    assert len(history) == 2
    assert history[0].decision == "reviewed_uncertain"
    assert history[1].decision == "conflict"


def test_edit_candidate_preserves_headword(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test editing candidate fields preserves the original headword and records audit."""
    service = VocabularyReviewService(mem_db)

    updated = service.edit_candidate(
        "VOCAB-CAND-001",
        reviewer="Editor-Dave",
        meanings=["customary rule"],
        pos="noun",
        dialect="Hunphun",
        alternative_spellings=["ngashānn"],
        example_sentences=["Iram ngashan lei."],
        notes="Updated dialect to Hunphun.",
    )
    assert updated.headword == "ngashan"  # Preserved original headword!
    assert updated.meanings == ["customary rule"]
    assert updated.dialect == "Hunphun"
    assert "ngashānn" in updated.alternative_spellings

    history = service.review_repo.get_reviews_for_entry("VOCAB-CAND-001")
    assert len(history) == 1
    assert history[0].decision == "edit"


def test_link_duplicate_preserves_all_provenance(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test linking a duplicate transfers all citations and records alternative spelling."""
    service = VocabularyReviewService(mem_db)

    cand, target = service.link_duplicate(
        candidate_id="VOCAB-CAND-001",
        target_id="VOCAB-TEST-001",
        reviewer="Supervisor-Z",
        as_spelling=True,
        notes="Merged spelling variant.",
    )

    # Candidate should be marked as duplicate
    assert cand.review_status == "duplicate"
    assert cand.reviewer == "Supervisor-Z"

    # Target should now contain candidate's provenance citation!
    assert len(target.provenance) == 2
    prov_citations = [p.citation for p in target.provenance]
    assert "Grammar & Dictionary, p. 12" in prov_citations
    assert "Grammar & Dictionary, p. 45" in prov_citations

    # Target should include candidate's headword as alternative spelling
    assert "ngashan" in target.alternative_spellings

    # Audit records created for both
    cand_history = service.review_repo.get_reviews_for_entry("VOCAB-CAND-001")
    assert len(cand_history) == 1
    assert cand_history[0].decision == "duplicate"
    assert cand_history[0].target_duplicate_id == "VOCAB-TEST-001"

    target_history = service.review_repo.get_reviews_for_entry("VOCAB-TEST-001")
    assert len(target_history) == 1
    assert target_history[0].decision == "edit"


def test_link_duplicate_self_link_prohibited(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
) -> None:
    """Test linking an entry to itself raises an error."""
    service = VocabularyReviewService(mem_db)
    with pytest.raises(ValueError, match="Cannot link an entry as a duplicate of itself"):
        service.link_duplicate(
            candidate_id="VOCAB-CAND-001",
            target_id="VOCAB-CAND-001",
            reviewer="Rev",
        )


def test_offline_export_and_import(
    mem_db: DatabaseManager,
    sample_entries: list[VocabularyEntry],
    tmp_path: Path,
) -> None:
    """Test exporting candidates to JSONL and importing validated community corrections."""
    service = VocabularyReviewService(mem_db)

    export_file = tmp_path / "candidates_export.jsonl"
    count = service.export_candidates(
        output_path=export_file,
        review_status="pending_review",
        include_restricted=False,
    )
    assert count == 2
    assert export_file.exists()

    # Read exported JSON lines
    lines = export_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    exported_ids = {json.loads(line)["entry_id"] for line in lines}
    assert exported_ids == {"VOCAB-CAND-001", "VOCAB-CAND-002"}

    # Prepare correction file for import
    correction_file = tmp_path / "corrections.jsonl"
    corrections = [
        {
            "entry_id": "VOCAB-CAND-001",
            "decision": "accept",
            "reviewer": "Community-Elder-Khangam",
            "meanings": ["tribal code of conduct", "customary law"],
            "part_of_speech": "noun",
            "notes": "Verified by village customary court.",
        },
        {
            "entry_id": "VOCAB-CAND-002",
            "decision": "uncertain",
            "reviewer": "Field-Worker-Shimray",
            "notes": "Dialectal variant needing elder confirmation.",
        },
        {
            "entry_id": "NON-EXISTENT-ID",
            "decision": "accept",
            "reviewer": "Alice",
            "meanings": ["meaning"],
        },
    ]
    with correction_file.open("w", encoding="utf-8") as f:
        for c in corrections:
            f.write(json.dumps(c) + "\n")

    # Import corrections
    report = service.import_corrections(correction_file)
    assert report["total"] == 3
    assert report["applied"] == 2
    assert len(report["errors"]) == 1
    assert "NON-EXISTENT-ID" in report["errors"][0]

    # Verify that VOCAB-CAND-001 was accepted
    accepted_entry = service.vocab_repo.get_by_id("VOCAB-CAND-001")
    assert accepted_entry is not None
    assert accepted_entry.review_status == "accepted"
    assert accepted_entry.verification_status == "verified"
    assert "customary law" in accepted_entry.meanings

    # Verify that VOCAB-CAND-002 was flagged uncertain
    flagged_entry = service.vocab_repo.get_by_id("VOCAB-CAND-002")
    assert flagged_entry is not None
    assert flagged_entry.review_status == "reviewed_uncertain"
    assert flagged_entry.verification_status == "needs_review"


def test_cli_review_smoke(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """Test CLI review commands and arguments smoke execution."""
    # 1. Help
    try:
        main(["review", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    cap_help = capsys.readouterr().out
    assert "--list" in cap_help
    assert "--show" in cap_help
    assert "--accept" in cap_help
    assert "--reject" in cap_help
    assert "--flag" in cap_help
    assert "--link-duplicate" in cap_help
    assert "--export" in cap_help
    assert "--import-corrections" in cap_help

    # 2. List review queue
    code_list = main(["review", "--list"])
    assert code_list == 0
    cap_list = capsys.readouterr().out
    assert "VOCABULARY CANDIDATE REVIEW QUEUE" in cap_list

    # 3. Export to temp file
    exp_path = tmp_path / "cli_export.jsonl"
    code_exp = main(["review", "--export", str(exp_path)])
    assert code_exp == 0
    assert exp_path.exists()
    cap_exp = capsys.readouterr().out
    assert "Exported" in cap_exp

    # 4. Import from temp file (retain top 3 candidates for swift smoke validation)
    sample_lines = exp_path.read_text(encoding="utf-8").strip().splitlines()
    exp_path.write_text("\n".join(sample_lines[:3]) + "\n", encoding="utf-8")
    code_imp = main(["review", "--import-corrections", str(exp_path), "--reviewer", "CLI-Reviewer"])
    assert code_imp == 0
    cap_imp = capsys.readouterr().out
    assert "COMMUNITY REVIEW CORRECTIONS IMPORT REPORT" in cap_imp
