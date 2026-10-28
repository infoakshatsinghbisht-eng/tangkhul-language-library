"""Unit and integration tests for Step 14: Native-Speaker Validation, Multi-Reviewer Consensus,
and Community Vocabulary Governance.
"""

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
from tangkhul_lib.vocabulary.review import ConsensusPolicy, VocabularyReviewService
from tangkhul_lib.vocabulary.search import VocabularySearchEngine


@pytest.fixture
def mem_db() -> DatabaseManager:
    """Provide an isolated in-memory DatabaseManager."""
    db = DatabaseManager(":memory:")
    db.initialize_schema()
    return db


@pytest.fixture
def governance_service(mem_db: DatabaseManager) -> VocabularyReviewService:
    """Create VocabularyReviewService with default consensus policy (threshold=2)."""
    policy = ConsensusPolicy(required_approvals=2, allow_single_reviewer_exception=False)
    return VocabularyReviewService(db_manager=mem_db, policy=policy)


@pytest.fixture
def populated_entries(mem_db: DatabaseManager) -> list[VocabularyEntry]:
    """Seed test vocabulary candidates with various provenance and review states."""
    repo = VocabularyReviewService(mem_db).vocab_repo

    entries = [
        VocabularyEntry(
            id="VOCAB-GOV-001",
            headword="ngashān",
            meanings=["custom", "tradition"],
            alternative_spellings=["ngashan"],
            dialect="Ukhrul",
            part_of_speech="noun",
            example_sentences=["Tangkhul wui ngashan."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Grammar & Dictionary, p. 12",
                    page_or_section="p. 12",
                    context_sentence="Tangkhul wui ngashan.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="unverified",
            review_status="pending_review",
        ),
        VocabularyEntry(
            id="VOCAB-GOV-002",
            headword="luira",
            meanings=[],  # Missing meanings -> High priority for review
            dialect="Ukhrul",
            provenance=[
                ProvenanceRecord(
                    source_id="CULT-CUST-001",
                    resource_type="culture",
                    citation="Seed Sowing Festival, p. 3",
                    page_or_section="p. 3",
                    context_sentence="Luira phanit ngashan.",
                    recorded_year=1975,
                    permission_status="community_authorized",
                )
            ],
            verification_status="unverified",
            review_status="pending_review",
        ),
        VocabularyEntry(
            id="VOCAB-GOV-003",
            headword="secret_chant",
            meanings=["esoteric ritual phrase"],
            provenance=[
                ProvenanceRecord(
                    source_id="CULT-RIT-001",
                    resource_type="culture",
                    citation="Sacred Rites, p. 99",
                    page_or_section="p. 99",
                    context_sentence="Secret chant words.",
                    recorded_year=1980,
                    permission_status="restricted",  # Restricted permission
                )
            ],
            verification_status="unverified",
            review_status="pending_review",
            license_restrictions="restricted",
        ),
        VocabularyEntry(
            id="VOCAB-GOV-004",
            headword="unbacked_word",
            meanings=["invented or unbacked headword"],
            provenance=[],  # Lacks source evidence
            verification_status="unverified",
            review_status="pending_review",
        ),
    ]

    for e in entries:
        repo.add(e)
    return entries


class TestMultiReviewerConsensus:
    """Test multi-reviewer consensus evaluation, thresholds, and role eligibility."""

    def test_default_threshold_requires_two_independent_approvals(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Default threshold is 2: candidate is only promoted after two independent approvals."""
        entry_id = "VOCAB-GOV-001"

        # First approval by reviewer_alpha
        rev1, eval_res1 = governance_service.record_decision(
            entry_id=entry_id,
            reviewer="reviewer_alpha",
            decision="approve",
            spelling_assessment="accurate",
            meaning_assessment="verified",
            pos_assessment="noun",
            source_assessment="reliable",
            notes="Spelling and definition verified against 1918 grammar.",
        )
        assert rev1.decision == "approve"
        assert rev1.counts_for_consensus is True
        assert eval_res1 is not None
        assert eval_res1.is_consensus_met is False

        # Candidate still awaiting second approval
        entry_after_1 = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry_after_1 is not None
        assert entry_after_1.verification_status == "unverified"
        assert entry_after_1.review_status == "pending_review"

        # Consensus evaluation confirms threshold not met yet
        eval_1 = governance_service.evaluate_consensus(entry_id)
        assert eval_1.is_consensus_met is False
        assert eval_1.approvals_count == 1
        assert eval_1.threshold_required == 2
        assert eval_1.decision_outcome == "pending_consensus"

        # Second approval by independent reviewer_beta
        rev2, eval_res2 = governance_service.record_decision(
            entry_id=entry_id,
            reviewer="reviewer_beta",
            decision="approve",
            spelling_assessment="accurate",
            meaning_assessment="verified",
            notes="Second native speaker independent validation.",
        )
        assert rev2.decision == "approve"
        assert eval_res2 is not None
        assert eval_res2.is_consensus_met is True

        # Now consensus threshold is satisfied!
        eval_2 = governance_service.evaluate_consensus(entry_id)
        assert eval_2.is_consensus_met is True
        assert eval_2.approvals_count == 2
        assert eval_2.approving_reviewers == ["reviewer_alpha", "reviewer_beta"]
        assert eval_2.decision_outcome == "verified"

        # Entry is promoted to verified and review_status=accepted
        entry_promoted = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry_promoted is not None
        assert entry_promoted.verification_status == "verified"
        assert entry_promoted.review_status == "accepted"

    def test_single_reviewer_multiple_approvals_cannot_meet_threshold(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Multiple submissions by the same reviewer count as only 1 vote."""
        entry_id = "VOCAB-GOV-001"

        governance_service.record_decision(
            entry_id=entry_id,
            reviewer="single_reviewer",
            decision="approve",
            notes="First vote.",
        )
        governance_service.record_decision(
            entry_id=entry_id,
            reviewer="single_reviewer",
            decision="approve",
            notes="Second repeated vote by same reviewer.",
        )
        governance_service.record_decision(
            entry_id=entry_id,
            reviewer="single_reviewer",
            decision="approve",
            notes="Third repeated vote.",
        )

        eval_res = governance_service.evaluate_consensus(entry_id)
        assert eval_res.approvals_count == 1  # Deduplicated by reviewer identity
        assert eval_res.is_consensus_met is False
        assert eval_res.decision_outcome == "pending_consensus"

        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.verification_status == "unverified"

    def test_withdrawn_approval_reverts_consensus(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Withdrawing an approval supersedes previous decision and reverts consensus."""
        entry_id = "VOCAB-GOV-001"

        # Both approve initially -> reaches consensus
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_2", decision="approve"
        )
        eval_1 = governance_service.evaluate_consensus(entry_id)
        assert eval_1.is_consensus_met is True
        assert eval_1.decision_outcome == "verified"

        # rev_2 withdraws approval
        withdrawn, _ = governance_service.record_decision(
            entry_id=entry_id,
            reviewer="rev_2",
            decision="withdraw_approval",
            notes="Discovered potential inaccuracy in meaning.",
        )
        assert withdrawn.decision == "withdraw_approval"
        assert withdrawn.counts_for_consensus is False

        # Re-evaluate consensus: approvals dropped to 1
        eval_2 = governance_service.evaluate_consensus(entry_id)
        assert eval_2.is_consensus_met is False
        assert eval_2.approvals_count == 1
        assert eval_2.decision_outcome == "pending_consensus"

        # Entry is no longer verified
        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.verification_status != "verified"

    def test_unresolved_conflicts_block_promotion(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """A flag_conflict or conflict decision blocks verification even with approvals."""
        entry_id = "VOCAB-GOV-001"

        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id=entry_id,
            reviewer="rev_2",
            decision="flag_conflict",
            notes="Conflicting dialect usage reported in southern villages.",
        )

        eval_res = governance_service.evaluate_consensus(entry_id)
        assert eval_res.is_consensus_met is False
        assert eval_res.conflicts_count == 1
        assert eval_res.decision_outcome == "conflict"

        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.review_status == "conflict"
        assert entry.verification_status == "needs_review"

    def test_correction_requested_blocks_premature_verification(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Correction requested halts consensus until corrections are resolved."""
        entry_id = "VOCAB-GOV-001"

        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id=entry_id,
            reviewer="rev_2",
            decision="correction_requested",
            correction_proposals={"spelling": "ngashān", "dialect": "Ukhrul"},
            notes="Please add macron to vowel a.",
        )

        eval_res = governance_service.evaluate_consensus(entry_id)
        assert eval_res.is_consensus_met is False
        assert eval_res.corrections_count == 1
        assert eval_res.decision_outcome == "correction_requested"

        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.review_status == "needs_correction"

    def test_ineligible_reviewer_excluded_from_consensus(
        self, mem_db: DatabaseManager, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Ineligible reviewers are recorded immutably but excluded from consensus."""
        policy = ConsensusPolicy(
            required_approvals=2,
            eligible_reviewers=["elder_somrei", "scholar_won"],
        )
        service = VocabularyReviewService(db_manager=mem_db, policy=policy)

        entry_id = "VOCAB-GOV-001"

        # Unauthorized reviewer submits approval
        rev_anon, _ = service.record_decision(
            entry_id=entry_id,
            reviewer="unauthorized_guest",
            decision="approve",
        )
        assert rev_anon.counts_for_consensus is False
        assert "[Ineligible reviewer" in (rev_anon.notes or "")

        # Eligible reviewer submits approval
        rev_auth, _ = service.record_decision(
            entry_id=entry_id,
            reviewer="elder_somrei",
            decision="approve",
        )
        assert rev_auth.counts_for_consensus is True

        eval_res = service.evaluate_consensus(entry_id)
        assert eval_res.approvals_count == 1  # Only elder_somrei counted!
        assert eval_res.is_consensus_met is False

    def test_explicit_single_reviewer_exception(
        self, mem_db: DatabaseManager, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Documented single-reviewer exception only functions when explicitly configured."""
        policy = ConsensusPolicy(
            required_approvals=1,
            allow_single_reviewer_exception=True,
        )
        service = VocabularyReviewService(db_manager=mem_db, policy=policy)

        entry_id = "VOCAB-GOV-001"
        service.record_decision(
            entry_id=entry_id,
            reviewer="sole_validator",
            decision="approve",
        )

        eval_res = service.evaluate_consensus(entry_id)
        assert eval_res.is_consensus_met is True
        assert eval_res.decision_outcome == "verified"
        assert "Single-reviewer exception policy applied" in (eval_res.notes or "")


class TestLinguisticReviewVsPermissionClearance:
    """Validate that linguistic approval is decoupled from copyright and provenance clearance."""

    def test_candidate_without_source_evidence_cannot_be_verified(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Unbacked candidates cannot reach consensus even with two approvals."""
        entry_id = "VOCAB-GOV-004"  # Has no provenance records

        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_2", decision="approve"
        )

        eval_res = governance_service.evaluate_consensus(entry_id)
        assert eval_res.is_source_verified is False
        assert eval_res.decision_outcome == "lacks_source_evidence"
        assert "lacks source evidence" in (eval_res.notes or "").lower()

        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.verification_status != "verified"

    def test_restricted_candidate_is_permission_blocked(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Culturally restricted candidate cannot be promoted to public verified status."""
        entry_id = "VOCAB-GOV-003"  # Restricted ritual chant

        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_2", decision="approve"
        )

        eval_res = governance_service.evaluate_consensus(entry_id)
        assert eval_res.is_permission_cleared is False
        assert eval_res.is_public_eligible is False
        assert eval_res.decision_outcome == "permission_blocked"

        entry = governance_service.vocab_repo.get_by_id(entry_id)
        assert entry is not None
        assert entry.verification_status != "verified"


class TestReviewTasksAndWorkflow:
    """Test idempotent review task creation, prioritization, and assignment."""

    def test_create_review_tasks_prioritization_and_idempotence(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Tasks prioritize missing meanings and are idempotent on repeated runs."""
        # First task generation run
        created_first = governance_service.create_review_tasks(limit=10)
        assert len(created_first) >= 2

        # Check prioritization: VOCAB-GOV-002 has missing meanings -> high priority
        task_luira = next((t for t in created_first if t.entry_id == "VOCAB-GOV-002"), None)
        assert task_luira is not None
        assert task_luira.priority == "high"
        assert "missing verified meanings" in task_luira.reason
        assert "meaning" in task_luira.review_dimensions

        # Re-running task creation must be idempotent (0 duplicate tasks created)
        created_second = governance_service.create_review_tasks(limit=10)
        assert len(created_second) == 0

    def test_claim_review_task(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Claiming a task assigns attributable reviewer and transitions state to in_review."""
        tasks = governance_service.create_review_tasks(limit=5)
        task = tasks[0]

        claimed = governance_service.claim_task(task.id, reviewer="contributor_pseudonym_42")
        assert claimed.status == "in_review"
        assert claimed.assigned_reviewer == "contributor_pseudonym_42"

        # Check repository reflects change
        fetched = governance_service.get_task(task.id)
        assert fetched is not None
        assert fetched.assigned_reviewer == "contributor_pseudonym_42"


class TestOfflineCommunityReviewPackages:
    """Test JSON export, schema validation, restricted context shielding, and package import."""

    def test_export_package_masks_restricted_context(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry],
        tmp_path: Path
    ) -> None:
        """Review package export version 2.0 shields restricted texts with privilege notices."""
        governance_service.create_review_tasks(limit=10)

        out_path = tmp_path / "review_package.json"
        task_count = governance_service.export_review_package(str(out_path), limit=10)
        assert task_count > 0

        with open(out_path, encoding="utf-8") as f:
            pkg = json.load(f)

        assert pkg["package_schema_version"] == "2.0"
        assert "tasks" in pkg
        assert len(pkg["tasks"]) > 0

        # Find item for VOCAB-GOV-003 (restricted)
        restricted_task = next(
            (t for t in pkg["tasks"] if t["entry_id"] == "VOCAB-GOV-003"), None
        )
        assert restricted_task is not None
        # Verify context sentence was shielded in provenance!
        assert len(restricted_task["provenance"]) > 0
        ref = restricted_task["provenance"][0]
        assert ref["context_sentence"] == "[RESTRICTED TEXT - ACCESS PRIVILEGED]"

    def test_validate_and_import_offline_package(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry],
        tmp_path: Path
    ) -> None:
        """Offline package validation and import applies decisions and completes tasks."""
        governance_service.create_review_tasks(limit=10)
        pkg_path = tmp_path / "offline_batch.json"
        governance_service.export_review_package(str(pkg_path), limit=10)

        with open(pkg_path, encoding="utf-8") as f:
            pkg = json.load(f)

        # Reviewer fills out decision in task for VOCAB-GOV-001
        for item in pkg["tasks"]:
            if item["entry_id"] == "VOCAB-GOV-001":
                item["submission"] = {
                    "reviewer": "offline_reviewer_01",
                    "decision": "approve",
                    "spelling_assessment": "accurate",
                    "meaning_assessment": "verified",
                    "notes": "Reviewed offline via JSON package.",
                }

        with open(pkg_path, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2)

        # Validate package
        val_res = governance_service.validate_review_package(str(pkg_path))
        assert val_res["valid"] is True
        assert val_res["valid_submissions"] == 1

        # Dry run import
        dry_res = governance_service.import_review_package(str(pkg_path), dry_run=True)
        assert dry_res["applied_count"] == 1
        assert dry_res["dry_run"] is True

        # Actual import
        imp_res = governance_service.import_review_package(str(pkg_path), dry_run=False)
        assert imp_res["applied_count"] == 1
        assert imp_res["dry_run"] is False

        # Verify decision recorded in database
        reviews = governance_service.review_repo.get_reviews_for_entry("VOCAB-GOV-001")
        assert any(r.reviewer == "offline_reviewer_01" for r in reviews)

    def test_stale_package_conflict_detection(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry],
        tmp_path: Path
    ) -> None:
        """Detecting when an entry in a package was modified after package generation."""
        governance_service.create_review_tasks(limit=5)
        pkg_path = tmp_path / "stale_batch.json"
        governance_service.export_review_package(str(pkg_path), limit=5)

        # Simulate later database review that advances updated_at
        governance_service.record_decision(
            entry_id="VOCAB-GOV-001",
            reviewer="online_elder",
            decision="approve",
        )

        with open(pkg_path, encoding="utf-8") as f:
            pkg = json.load(f)

        # Make the package baseline old
        for item in pkg["tasks"]:
            if item["entry_id"] == "VOCAB-GOV-001":
                item["baseline_updated_at"] = "2020-01-01T00:00:00Z"
                item["submission"] = {
                    "reviewer": "late_reviewer",
                    "decision": "reject",
                    "notes": "Stale edit.",
                }

        with open(pkg_path, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2)

        val_res = governance_service.validate_review_package(str(pkg_path))
        assert val_res["stale_conflicts"] >= 1


class TestQualityMetricsAndFTS5:
    """Test review metrics calculations and FTS5 synchronization."""

    def test_review_quality_metrics(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Metrics accurately tabulate database records without fabrication."""
        governance_service.create_review_tasks(limit=10)
        governance_service.record_decision(
            entry_id="VOCAB-GOV-001", reviewer="rev_1", decision="approve"
        )
        governance_service.record_decision(
            entry_id="VOCAB-GOV-001", reviewer="rev_2", decision="approve"
        )

        metrics = governance_service.get_review_metrics()
        assert metrics["total_entries"] == 4
        assert metrics["total_candidates"] == 3
        assert metrics["entries_with_reviews"] == 1
        assert metrics["entries_meeting_consensus"] == 1
        assert metrics["tasks"]["open"] >= 1
        assert "reviewer_activity" in metrics
        assert metrics["reviewer_activity"]["rev_1"] == 1

    def test_fts5_synchronization_on_consensus_promotion(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Promoted candidate is indexed and discoverable in FTS5 search."""
        service = governance_service
        search_engine = VocabularySearchEngine(repository=service.vocab_repo)

        # Before consensus, VOCAB-GOV-001 is unverified
        _ = search_engine.search_headword("ngashān")
        entry_before = service.vocab_repo.get_by_id("VOCAB-GOV-001")
        assert entry_before is not None
        assert entry_before.verification_status != "verified"

        # Reach consensus
        service.record_decision(
            entry_id="VOCAB-GOV-001", reviewer="validator_a", decision="approve"
        )
        service.record_decision(
            entry_id="VOCAB-GOV-001", reviewer="validator_b", decision="approve"
        )

        entry_after = service.vocab_repo.get_by_id("VOCAB-GOV-001")
        assert entry_after is not None
        assert entry_after.verification_status == "verified"
        assert entry_after.review_status == "accepted"

        # FTS5 search finds entry
        results_after = service.vocab_repo.search_fts("ngashān")
        assert any(entry.id == "VOCAB-GOV-001" for entry, _rank in results_after)

    def test_backward_compatibility_step12_review(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Step 12 accept_candidate method remains fully functional and updates consensus."""
        res = governance_service.accept_candidate(
            entry_id="VOCAB-GOV-001",
            reviewer="legacy_reviewer",
            meanings=["custom", "tradition"],
            notes="Step 12 compatible legacy review.",
        )
        assert res.id == "VOCAB-GOV-001"
        reviews = governance_service.review_repo.get_reviews_for_entry("VOCAB-GOV-001")
        assert len(reviews) == 1
        assert reviews[0].reviewer == "legacy_reviewer"


class TestCLIGovernanceSmoke:
    """CLI smoke tests for Step 14 review options."""

    def test_cli_consensus_policy_and_metrics(self) -> None:
        """Run tangkhul review --consensus-policy and --metrics via CLI."""
        assert main(["review", "--consensus-policy"]) == 0
        assert main(["review", "--metrics"]) == 0

    def test_cli_tasks_and_create(self) -> None:
        """Run tangkhul review --create-tasks and --tasks."""
        assert main(["review", "--create-tasks", "--limit", "5"]) == 0
        assert main(["review", "--tasks", "--limit", "5"]) == 0


class TestGovernanceDatabaseIntegrity:
    """Test database migration safety, immutable history, and transaction integrity."""

    def test_schema_migration_is_idempotent(self, mem_db: DatabaseManager) -> None:
        """Calling initialize_schema repeatedly executes migrations safely without failure."""
        mem_db.initialize_schema()
        mem_db.initialize_schema()

    def test_immutable_review_history_records_sequential_decisions(
        self, governance_service: VocabularyReviewService, populated_entries: list[VocabularyEntry]
    ) -> None:
        """Review decisions are never overwritten; sequential changes append audit records."""
        entry_id = "VOCAB-GOV-001"
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="approve", notes="Decision 1"
        )
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="withdraw_approval", notes="Decision 2"
        )
        governance_service.record_decision(
            entry_id=entry_id, reviewer="rev_1", decision="flag_conflict", notes="Decision 3"
        )

        history = governance_service.review_repo.get_reviews_for_entry(entry_id)
        assert len(history) == 3
        assert [r.decision for r in history] == ["approve", "withdraw_approval", "flag_conflict"]
        assert [r.notes for r in history] == ["Decision 1", "Decision 2", "Decision 3"]
