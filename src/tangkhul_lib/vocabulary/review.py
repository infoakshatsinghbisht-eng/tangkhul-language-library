"""Vocabulary review, validation, community correction, and duplicate management service.

This module provides the core business logic for human review of candidate vocabulary
entries harvested from authorized documents, dictionaries, literature, and cultural records.
"""

from __future__ import annotations

import datetime
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from tangkhul_lib.core.exceptions import ResourceNotFoundError
from tangkhul_lib.core.models import (
    VALID_REVIEW_DECISIONS,
    ConsensusEvaluation,
    ReviewTask,
    VocabularyEntry,
    VocabularyReviewRecord,
)
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    ConsensusRepository,
    ManifestRepository,
    ReviewTaskRepository,
    VocabularyRepository,
    VocabularyReviewRepository,
)
from tangkhul_lib.vocabulary.normalization import normalize_unicode
from tangkhul_lib.vocabulary.phonetic import TangkhulPhoneticEncoder, calculate_similarity

if TYPE_CHECKING:
    from tangkhul_lib.core.config import LibraryConfig


def current_iso_timestamp() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@dataclass
class ConsensusPolicy:
    """Configurable multi-reviewer consensus policy.

    Rules:
        - Default threshold: 2 independent eligible reviewers required for verification.
        - Prevent repeated approvals by the same reviewer from counting multiple times.
        - Unresolved conflicts, correction requests, and rejections block verification.
        - Single-reviewer exception allowed only when explicitly configured for a specific workflow.
        - Keeps linguistic consensus separate from source verification and copyright clearance.
    """

    policy_version: str = "1.0"
    required_approvals: int = 2
    allow_single_reviewer_exception: bool = False
    eligible_reviewers: list[str] | None = None
    require_source_clearance: bool = True
    require_community_authorization_for_sensitive: bool = True

    @classmethod
    def from_config_or_env(cls, config: LibraryConfig | None = None) -> ConsensusPolicy:
        """Create policy from environment variables or LibraryConfig."""
        threshold_str = os.environ.get("TANGKHUL_CONSENSUS_THRESHOLD", "2")
        try:
            threshold = int(threshold_str)
        except ValueError:
            threshold = 2
        allow_single = os.environ.get(
            "TANGKHUL_ALLOW_SINGLE_REVIEWER_EXCEPTION", ""
        ).strip().lower() in {"1", "true", "yes"}
        elig_str = os.environ.get("TANGKHUL_ELIGIBLE_REVIEWERS")
        eligible = (
            [r.strip() for r in elig_str.split(",") if r.strip()]
            if elig_str
            else None
        )
        return cls(
            required_approvals=threshold,
            allow_single_reviewer_exception=allow_single,
            eligible_reviewers=eligible,
        )


class VocabularyReviewService:
    """Coordinates vocabulary review, audit history, duplicate suggestions,
    multi-reviewer consensus, and offline community review exchanges.
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        vocab_repo: VocabularyRepository | None = None,
        review_repo: VocabularyReviewRepository | None = None,
        manifest_repo: ManifestRepository | None = None,
        task_repo: ReviewTaskRepository | None = None,
        consensus_repo: ConsensusRepository | None = None,
        policy: ConsensusPolicy | None = None,
    ) -> None:
        self.db_manager = db_manager
        self.vocab_repo = vocab_repo or VocabularyRepository(db_manager)
        self.review_repo = review_repo or VocabularyReviewRepository(db_manager)
        self.manifest_repo = manifest_repo or ManifestRepository(db_manager)
        self.task_repo = task_repo or ReviewTaskRepository(db_manager)
        self.consensus_repo = consensus_repo or ConsensusRepository(db_manager)
        self.policy = policy or ConsensusPolicy.from_config_or_env()
        self.phonetic_encoder = TangkhulPhoneticEncoder()

    @classmethod
    def from_config(
        cls,
        config: LibraryConfig,
        policy: ConsensusPolicy | None = None,
    ) -> VocabularyReviewService:
        """Instantiate review service from global library configuration."""
        db_path = config.paths.data_dir / "database" / "tangkhul_corpus.sqlite"
        db_mgr = DatabaseManager(db_path)
        db_mgr.initialize_schema()
        pol = policy or ConsensusPolicy.from_config_or_env(config)
        return cls(db_mgr, policy=pol)

    def get_review_queue(
        self,
        review_status: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        dialect: str | None = None,
        missing_meanings: bool = False,
        has_duplicates: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[VocabularyEntry]:
        """Fetch vocabulary candidate entries in deterministic order with rich filtering."""
        candidates = self.vocab_repo.list_review_queue(
            review_status=review_status,
            source_type=source_type,
            source_id=source_id,
            dialect=dialect,
            missing_meanings=missing_meanings,
            limit=limit,
            offset=offset,
        )

        if not has_duplicates:
            return candidates

        # Filter for candidates that have at least one suggested duplicate
        filtered: list[VocabularyEntry] = []
        for cand in candidates:
            dups = self.find_duplicate_suggestions(cand, threshold=0.75)
            if dups:
                filtered.append(cand)
        return filtered

    def count_review_queue(
        self,
        review_status: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        dialect: str | None = None,
        missing_meanings: bool = False,
    ) -> int:
        """Count total matching candidates in review queue."""
        return self.vocab_repo.count_review_queue(
            review_status=review_status,
            source_type=source_type,
            source_id=source_id,
            dialect=dialect,
            missing_meanings=missing_meanings,
        )

    def find_duplicate_suggestions(
        self,
        entry: VocabularyEntry,
        threshold: float = 0.75,
    ) -> list[dict[str, Any]]:
        """Identify potential duplicate entries using exact, phonetic, and fuzzy similarity.

        Rules:
            - Never automatically merges candidates; suggestions require explicit human action.
            - Considers headword, alternative spellings, and phonetic encodings.
        """
        all_entries = self.vocab_repo.list_all()
        target_headword_norm = normalize_unicode(entry.headword).strip().lower()
        target_phonetic = self.phonetic_encoder.encode(entry.headword)

        suggestions: list[dict[str, Any]] = []

        for other in all_entries:
            if other.id == entry.id:
                continue

            other_headword_norm = normalize_unicode(other.headword).strip().lower()
            other_phonetic = self.phonetic_encoder.encode(other.headword)

            # 1. Exact case-insensitive match (different ID)
            if target_headword_norm == other_headword_norm:
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "verification_status": other.verification_status,
                    "match_type": "exact",
                    "score": 1.0,
                    "explanation": f"Identical normalized headword '{other.headword}'",
                })
                continue

            # 2. Check alternative spellings match
            other_alts_norm = [
                normalize_unicode(a).strip().lower() for a in other.alternative_spellings
            ]
            if target_headword_norm in other_alts_norm:
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "verification_status": other.verification_status,
                    "match_type": "exact",
                    "score": 1.0,
                    "explanation": f"Matches alternate spelling of '{other.headword}'",
                })
                continue

            # 3. Phonetic match
            if target_phonetic and target_phonetic == other_phonetic:
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "verification_status": other.verification_status,
                    "match_type": "phonetic",
                    "score": 0.90,
                    "explanation": (
                        f"Phonetic equivalence ({target_phonetic}) with '{other.headword}'"
                    ),
                })
                continue

            # 4. Levenshtein fuzzy similarity
            sim = calculate_similarity(entry.headword, other.headword)
            if sim >= threshold:
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "verification_status": other.verification_status,
                    "match_type": "fuzzy",
                    "score": round(sim, 3),
                    "explanation": f"Fuzzy similarity ({sim:.2f}) with '{other.headword}'",
                })

        # Sort suggestions by highest score descending
        suggestions.sort(key=lambda s: s["score"], reverse=True)
        return suggestions

    def get_candidate_details(self, entry_id: str) -> dict[str, Any]:
        """Fetch candidate details, citations, duplicate suggestions, and audit history."""
        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        # Enrich provenance citations and shield restricted sentences
        enriched_provenance: list[dict[str, Any]] = []
        is_restricted = entry.license_restrictions == "restricted"

        for p in entry.provenance:
            p_perm = (p.permission_status or "pending").strip().lower()
            p_is_restricted = p_perm == "restricted"
            if p_is_restricted:
                is_restricted = True

            context_str = p.context_sentence
            if p_is_restricted and context_str:
                context_str = "[RESTRICTED TEXT - MASKED FOR PRIVACY SAFEGUARD]"

            enriched_provenance.append({
                "source_id": p.source_id,
                "resource_type": p.resource_type,
                "citation": p.citation,
                "page_or_section": p.page_or_section,
                "context_sentence": context_str,
                "recorded_year": p.recorded_year,
                "permission_status": p.permission_status,
                "is_restricted": p_is_restricted,
            })

        duplicate_suggestions = self.find_duplicate_suggestions(entry, threshold=0.75)
        review_history = self.review_repo.get_reviews_for_entry(entry_id)

        # Mask restricted example sentences on entry display
        safe_examples = []
        for ex in entry.example_sentences:
            if is_restricted:
                safe_examples.append("[RESTRICTED EXAMPLE SENTENCE - MASKED]")
            else:
                safe_examples.append(ex)

        return {
            "entry": entry,
            "safe_example_sentences": safe_examples,
            "provenance": enriched_provenance,
            "duplicate_suggestions": duplicate_suggestions,
            "review_history": [r.to_dict() for r in review_history],
            "is_restricted": is_restricted,
        }

    def accept_candidate(
        self,
        entry_id: str,
        reviewer: str,
        meanings: list[str] | None = None,
        pos: str | None = None,
        dialect: str | None = None,
        notes: str | None = None,
    ) -> VocabularyEntry:
        """Accept a vocabulary candidate as verified after confirming its meaning."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required for acceptance.")

        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        # Assemble new meanings
        active_meanings = list(entry.meanings)
        if meanings:
            for m in meanings:
                clean_m = m.strip()
                if clean_m and clean_m not in active_meanings:
                    active_meanings.append(clean_m)

        if not active_meanings:
            raise ValueError(
                f"Cannot accept candidate '{entry.headword}' without at least "
                "one confirmed meaning."
            )

        prev_state = entry.to_dict()

        entry.meanings = active_meanings
        if pos:
            entry.part_of_speech = pos.strip()
        if dialect:
            entry.dialect = dialect.strip()

        entry.review_status = "accepted"
        entry.verification_status = "verified"
        entry.reviewer = reviewer.strip()
        entry.reviewed_at = current_iso_timestamp()
        if notes:
            entry.review_notes = notes.strip()

        self.vocab_repo.add(entry)

        # Audit log record
        audit_record = VocabularyReviewRecord(
            entry_id=entry.id,
            headword=entry.headword,
            decision="accept",
            reviewer=reviewer.strip(),
            notes=notes.strip() if notes else None,
            previous_state=prev_state,
            new_state=entry.to_dict(),
            suggested_meaning=", ".join(active_meanings),
            suggested_pos=entry.part_of_speech,
            suggested_dialect=entry.dialect,
        )
        self.review_repo.add_review(audit_record)

        return entry

    def reject_candidate(
        self,
        entry_id: str,
        reviewer: str,
        reason: str,
    ) -> VocabularyEntry:
        """Reject a candidate as an invalid token, typo, or non-lexical OCR artifact."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required for rejection.")
        if not reason or not reason.strip():
            raise ValueError("A clear diagnostic reason is required when rejecting a candidate.")

        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        prev_state = entry.to_dict()

        entry.review_status = "rejected"
        entry.verification_status = "unverified"
        entry.license_restrictions = "restricted"  # Shielded from public search
        entry.reviewer = reviewer.strip()
        entry.reviewed_at = current_iso_timestamp()
        entry.review_notes = reason.strip()

        self.vocab_repo.add(entry)

        # Audit log record
        audit_record = VocabularyReviewRecord(
            entry_id=entry.id,
            headword=entry.headword,
            decision="reject",
            reviewer=reviewer.strip(),
            notes=reason.strip(),
            previous_state=prev_state,
            new_state=entry.to_dict(),
        )
        self.review_repo.add_review(audit_record)

        return entry

    def flag_candidate(
        self,
        entry_id: str,
        reviewer: str,
        decision: str = "reviewed_uncertain",
        notes: str = "",
    ) -> VocabularyEntry:
        """Flag a candidate as uncertain or having conflicting definitions."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required.")
        if decision not in {"reviewed_uncertain", "conflict"}:
            raise ValueError(
                f"Flag decision must be 'reviewed_uncertain' or 'conflict', got '{decision}'."
            )

        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        prev_state = entry.to_dict()

        entry.review_status = decision
        entry.verification_status = "needs_review"
        entry.reviewer = reviewer.strip()
        entry.reviewed_at = current_iso_timestamp()
        if notes:
            entry.review_notes = notes.strip()

        self.vocab_repo.add(entry)

        audit_record = VocabularyReviewRecord(
            entry_id=entry.id,
            headword=entry.headword,
            decision=decision,
            reviewer=reviewer.strip(),
            notes=notes.strip() if notes else None,
            previous_state=prev_state,
            new_state=entry.to_dict(),
        )
        self.review_repo.add_review(audit_record)

        return entry

    def edit_candidate(
        self,
        entry_id: str,
        reviewer: str,
        meanings: list[str] | None = None,
        pos: str | None = None,
        dialect: str | None = None,
        alternative_spellings: list[str] | None = None,
        example_sentences: list[str] | None = None,
        notes: str | None = None,
    ) -> VocabularyEntry:
        """Edit linguistic fields of a vocabulary candidate while preserving original headword."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required.")

        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        prev_state = entry.to_dict()

        if meanings is not None:
            entry.meanings = [m.strip() for m in meanings if m.strip()]
        if pos is not None:
            entry.part_of_speech = pos.strip() if pos else None
        if dialect is not None:
            entry.dialect = dialect.strip() if dialect else None
        if alternative_spellings is not None:
            clean_alts = [a.strip() for a in alternative_spellings if a.strip()]
            for alt in clean_alts:
                if alt not in entry.alternative_spellings and alt != entry.headword:
                    entry.alternative_spellings.append(alt)
        if example_sentences is not None:
            clean_exs = [e.strip() for e in example_sentences if e.strip()]
            for ex in clean_exs:
                if ex not in entry.example_sentences:
                    entry.example_sentences.append(ex)

        entry.reviewer = reviewer.strip()
        entry.reviewed_at = current_iso_timestamp()
        if notes:
            entry.review_notes = notes.strip()

        self.vocab_repo.add(entry)

        audit_record = VocabularyReviewRecord(
            entry_id=entry.id,
            headword=entry.headword,
            decision="edit",
            reviewer=reviewer.strip(),
            notes=notes.strip() if notes else None,
            previous_state=prev_state,
            new_state=entry.to_dict(),
            suggested_meaning=", ".join(entry.meanings) if entry.meanings else None,
            suggested_pos=entry.part_of_speech,
            suggested_dialect=entry.dialect,
        )
        self.review_repo.add_review(audit_record)

        return entry

    def link_duplicate(
        self,
        candidate_id: str,
        target_id: str,
        reviewer: str,
        as_spelling: bool = True,
        notes: str | None = None,
    ) -> tuple[VocabularyEntry, VocabularyEntry]:
        """Link a candidate entry to a canonical target entry as a confirmed duplicate.

        Rules:
            - Transfers all provenance citations from candidate to target.
            - Merges candidate's headword as an alternative spelling of target.
            - Retains candidate record with review_status="duplicate" for auditability.
            - Synchronizes target entry FTS5 index.
        """
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required.")
        if candidate_id == target_id:
            raise ValueError("Cannot link an entry as a duplicate of itself.")

        candidate = self.vocab_repo.get_by_id(candidate_id)
        if candidate is None:
            raise ResourceNotFoundError(f"Candidate entry '{candidate_id}' not found.")

        target = self.vocab_repo.get_by_id(target_id)
        if target is None:
            raise ResourceNotFoundError(f"Target entry '{target_id}' not found.")

        prev_candidate_state = candidate.to_dict()
        prev_target_state = target.to_dict()

        # 1. Merge provenance citations to target without duplicates
        for prov in candidate.provenance:
            has_prov = any(
                p.source_id == prov.source_id
                and p.page_or_section == prov.page_or_section
                and p.context_sentence == prov.context_sentence
                for p in target.provenance
            )
            if not has_prov:
                target.provenance.append(prov)

        # 2. Optionally record candidate headword as alternative spelling
        cand_headword = normalize_unicode(candidate.headword).strip()
        if (
            as_spelling
            and cand_headword != target.headword
            and cand_headword not in target.alternative_spellings
        ):
            target.alternative_spellings.append(cand_headword)

        # Also add any alternative spellings from candidate
        for alt in candidate.alternative_spellings:
            clean_alt = normalize_unicode(alt).strip()
            if clean_alt != target.headword and clean_alt not in target.alternative_spellings:
                target.alternative_spellings.append(clean_alt)

        # 3. Merge example sentences
        for ex in candidate.example_sentences:
            if ex not in target.example_sentences and len(target.example_sentences) < 10:
                target.example_sentences.append(ex)

        # 4. Mark candidate as duplicate
        candidate.review_status = "duplicate"
        candidate.verification_status = "unverified"
        candidate.reviewer = reviewer.strip()
        candidate.reviewed_at = current_iso_timestamp()
        link_note = f"Linked as duplicate to '{target.headword}' ({target.id})."
        candidate.review_notes = f"{link_note} {notes or ''}".strip()

        # Save target and candidate
        self.vocab_repo.add(target)
        self.vocab_repo.add(candidate)

        # Audit log for candidate
        audit_record = VocabularyReviewRecord(
            entry_id=candidate.id,
            headword=candidate.headword,
            decision="duplicate",
            reviewer=reviewer.strip(),
            notes=notes.strip() if notes else link_note,
            previous_state=prev_candidate_state,
            new_state=candidate.to_dict(),
            target_duplicate_id=target.id,
        )
        self.review_repo.add_review(audit_record)

        # Audit log for target
        target_audit = VocabularyReviewRecord(
            entry_id=target.id,
            headword=target.headword,
            decision="edit",
            reviewer=reviewer.strip(),
            notes=f"Absorbed duplicate candidate '{candidate.headword}' ({candidate.id}).",
            previous_state=prev_target_state,
            new_state=target.to_dict(),
            target_duplicate_id=candidate.id,
        )
        self.review_repo.add_review(target_audit)

        return candidate, target

    def export_candidates(
        self,
        output_path: Path | str,
        review_status: str | None = "pending_review",
        source_type: str | None = None,
        dialect: str | None = None,
        include_restricted: bool = False,
    ) -> int:
        """Export candidates to a JSONL file for offline community review.

        Privacy and Cultural Safeguards:
            - Strictly masks or omits restricted context sentences and restricted citations
              unless explicitly requested for authorized offline archiving.
        """
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        candidates = self.vocab_repo.list_review_queue(
            review_status=review_status,
            source_type=source_type,
            dialect=dialect,
            limit=5000,
            offset=0,
        )

        exported_count = 0
        with out_p.open("w", encoding="utf-8") as f:
            for cand in candidates:
                # Privacy check
                is_restricted = cand.license_restrictions == "restricted"
                safe_examples = []
                for ex in cand.example_sentences:
                    if is_restricted and not include_restricted:
                        continue
                    safe_examples.append(ex)

                safe_provenance = []
                for p in cand.provenance:
                    p_perm = (p.permission_status or "pending").strip().lower()
                    if p_perm == "restricted" and not include_restricted:
                        continue
                    safe_provenance.append({
                        "source_id": p.source_id,
                        "resource_type": p.resource_type,
                        "citation": p.citation,
                        "page_or_section": p.page_or_section,
                        "context_sentence": (
                            p.context_sentence
                            if not (p_perm == "restricted" and not include_restricted)
                            else None
                        ),
                    })

                record = {
                    "entry_id": cand.id,
                    "headword": cand.headword,
                    "meanings": cand.meanings,
                    "translations_en": cand.translations_en,
                    "part_of_speech": cand.part_of_speech,
                    "dialect": cand.dialect,
                    "alternative_spellings": cand.alternative_spellings,
                    "example_sentences": safe_examples,
                    "provenance": safe_provenance,
                    "review_status": cand.review_status,
                    "verification_status": cand.verification_status,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                exported_count += 1

        return exported_count

    def import_corrections(
        self,
        input_path: Path | str,
        default_reviewer: str | None = None,
    ) -> dict[str, Any]:
        """Import community corrections from JSONL file after validating structure and evidence.

        Valid decisions in import records:
            - `accept`: Requires meanings and reviewer.
            - `reject`: Requires reason and reviewer.
            - `uncertain` / `conflict`: Requires reviewer and optional notes.
            - `edit`: Applies field modifications.
            - `duplicate`: Requires target_id and reviewer.
        """
        in_p = Path(input_path)
        if not in_p.exists():
            raise FileNotFoundError(f"Correction file '{input_path}' does not exist.")

        total_records = 0
        applied_count = 0
        errors: list[str] = []

        with in_p.open("r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                total_records += 1
                try:
                    data = json.loads(line)
                except Exception as err:
                    errors.append(f"Line {line_no}: Invalid JSON — {err}")
                    continue

                entry_id = data.get("entry_id")
                if not entry_id:
                    errors.append(f"Line {line_no}: Missing required 'entry_id'.")
                    continue

                decision = data.get("decision", "edit").strip().lower()
                if decision not in VALID_REVIEW_DECISIONS:
                    errors.append(
                        f"Line {line_no}: Invalid decision '{decision}'. "
                        f"Allowed: {sorted(VALID_REVIEW_DECISIONS)}."
                    )
                    continue

                reviewer = data.get("reviewer") or default_reviewer
                if not reviewer or not reviewer.strip():
                    errors.append(f"Line {line_no}: Reviewer identifier missing.")
                    continue

                notes = data.get("notes")
                meanings = data.get("meanings")
                pos = data.get("part_of_speech")
                dialect = data.get("dialect")
                alts = data.get("alternative_spellings")
                examples = data.get("example_sentences")
                target_id = data.get("target_id")

                try:
                    if decision == "accept":
                        self.accept_candidate(
                            entry_id=entry_id,
                            reviewer=reviewer,
                            meanings=meanings,
                            pos=pos,
                            dialect=dialect,
                            notes=notes,
                        )
                    elif decision == "reject":
                        reason = notes or data.get("reason") or "Rejected via community import"
                        self.reject_candidate(
                            entry_id=entry_id,
                            reviewer=reviewer,
                            reason=reason,
                        )
                    elif decision in {"uncertain", "conflict"}:
                        stat = (
                            "conflict" if decision == "conflict" else "reviewed_uncertain"
                        )
                        self.flag_candidate(
                            entry_id=entry_id,
                            reviewer=reviewer,
                            decision=stat,
                            notes=notes or "",
                        )
                    elif decision == "duplicate":
                        if not target_id:
                            errors.append(
                                f"Line {line_no}: Duplicate decision requires 'target_id'."
                            )
                            continue
                        self.link_duplicate(
                            candidate_id=entry_id,
                            target_id=target_id,
                            reviewer=reviewer,
                            notes=notes,
                        )
                    elif decision == "edit":
                        self.edit_candidate(
                            entry_id=entry_id,
                            reviewer=reviewer,
                            meanings=meanings,
                            pos=pos,
                            dialect=dialect,
                            alternative_spellings=alts,
                            example_sentences=examples,
                            notes=notes,
                        )
                    applied_count += 1
                except Exception as op_err:
                    errors.append(f"Line {line_no} ({entry_id}): {op_err}")

        return {
            "total": total_records,
            "applied": applied_count,
            "errors": errors,
        }

    def record_decision(
        self,
        entry_id: str,
        reviewer: str,
        decision: str,
        spelling_assessment: str | None = None,
        meaning_assessment: str | None = None,
        pos_assessment: str | None = None,
        dialect_assessment: str | None = None,
        example_assessment: str | None = None,
        source_assessment: str | None = None,
        correction_proposals: dict[str, Any] | None = None,
        notes: str | None = None,
        auto_evaluate_consensus: bool = True,
    ) -> tuple[VocabularyReviewRecord, ConsensusEvaluation | None]:
        """Record an immutable, structured review decision for a vocabulary entry."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required.")

        clean_rev = reviewer.strip()
        dec = decision.strip().lower()
        if dec == "accept":
            dec = "approve"
        if dec not in VALID_REVIEW_DECISIONS:
            raise ValueError(
                f"Invalid review decision '{decision}'. "
                f"Allowed: {sorted(VALID_REVIEW_DECISIONS)}."
            )

        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        # Check eligibility and whether decision counts towards consensus
        counts = True
        annotated_notes = notes.strip() if notes else None
        if self.policy.eligible_reviewers is not None:
            if clean_rev not in self.policy.eligible_reviewers:
                counts = False
                note_suffix = "[Ineligible reviewer: decision excluded from consensus]"
                annotated_notes = (
                    f"{annotated_notes} {note_suffix}".strip()
                    if annotated_notes
                    else note_suffix
                )

        if dec == "withdraw_approval":
            counts = False

        audit_record = VocabularyReviewRecord(
            entry_id=entry.id,
            headword=entry.headword,
            decision=dec,
            reviewer=clean_rev,
            review_timestamp=current_iso_timestamp(),
            notes=annotated_notes,
            previous_state=entry.to_dict(),
            new_state=None,
            spelling_assessment=spelling_assessment,
            meaning_assessment=meaning_assessment,
            pos_assessment=pos_assessment,
            dialect_assessment=dialect_assessment,
            example_assessment=example_assessment,
            source_assessment=source_assessment,
            correction_proposals=correction_proposals,
            counts_for_consensus=counts,
        )

        rec_id = self.review_repo.add_review(audit_record)
        audit_record.id = rec_id

        entry.reviewed_at = audit_record.review_timestamp
        self.vocab_repo.add(entry)

        eval_res = None
        if auto_evaluate_consensus:
            eval_res = self.evaluate_consensus(entry_id)

        return audit_record, eval_res

    def evaluate_consensus(
        self,
        entry_id: str,
        policy: ConsensusPolicy | None = None,
    ) -> ConsensusEvaluation:
        """Evaluate multi-reviewer consensus and source/permission eligibility."""
        pol = policy or self.policy
        entry = self.vocab_repo.get_by_id(entry_id)
        if entry is None:
            raise ResourceNotFoundError(f"Vocabulary entry '{entry_id}' not found.")

        all_reviews = self.review_repo.get_reviews_for_entry(entry_id)

        # Track latest decision per reviewer
        latest_by_reviewer: dict[str, VocabularyReviewRecord] = {}
        for r in all_reviews:
            latest_by_reviewer[r.reviewer] = r

        approving: list[str] = []
        rejecting: list[str] = []
        conflicting: list[str] = []
        corrections: list[str] = []

        eligible_count = 0
        for rev_name, r in latest_by_reviewer.items():
            if pol.eligible_reviewers is not None and rev_name not in pol.eligible_reviewers:
                continue
            eligible_count += 1

            if not r.counts_for_consensus or r.decision == "withdraw_approval":
                continue

            if r.decision in {"approve", "accept"}:
                approving.append(rev_name)
            elif r.decision == "reject":
                rejecting.append(rev_name)
            elif r.decision in {"flag_conflict", "conflict"}:
                conflicting.append(rev_name)
            elif r.decision == "correction_requested":
                corrections.append(rev_name)

        needed = 1 if pol.allow_single_reviewer_exception else pol.required_approvals

        # Source evidence check
        is_source_verified = len(entry.provenance) > 0

        # Permission check
        is_permission_cleared = True
        if entry.license_restrictions == "restricted":
            is_permission_cleared = False
        for p in entry.provenance:
            if (p.permission_status or "").strip().lower() == "restricted":
                is_permission_cleared = False

        is_public_eligible = is_source_verified and is_permission_cleared
        is_consensus_met = False
        notes_parts = []

        if rejecting:
            outcome = "rejected"
            notes_parts.append(f"Rejected by: {', '.join(rejecting)}")
        elif conflicting:
            outcome = "conflict"
            notes_parts.append(f"Conflict flagged by: {', '.join(conflicting)}")
        elif corrections:
            outcome = "correction_requested"
            notes_parts.append(f"Corrections requested by: {', '.join(corrections)}")
        elif len(approving) >= needed:
            is_consensus_met = True
            if not is_source_verified:
                outcome = "lacks_source_evidence"
                notes_parts.append(
                    "Linguistic consensus met but entry lacks source evidence citations."
                )
            elif not is_permission_cleared:
                outcome = "permission_blocked"
                notes_parts.append(
                    "Linguistic consensus met but entry is blocked by copyright restrictions."
                )
            else:
                outcome = "verified"
                rev_str = ", ".join(approving)
                if pol.allow_single_reviewer_exception:
                    notes_parts.append(
                        f"Single-reviewer exception policy applied. Verified by: {rev_str}"
                    )
                else:
                    notes_parts.append(
                        f"Verified by consensus of {len(approving)} reviewers: {rev_str}"
                    )
        else:
            outcome = "pending_consensus"
            notes_parts.append(
                f"Pending consensus: {len(approving)} of {needed} approvals recorded."
            )

        # Update entry status if warranted
        if outcome == "verified":
            entry.verification_status = "verified"
            entry.review_status = "accepted"
            entry.reviewed_at = current_iso_timestamp()
            self.vocab_repo.add(entry)
            self.vocab_repo.index_vocabulary_entry(entry)
            task = self.task_repo.get_open_task_for_entry(entry.id)
            if task:
                task.status = "completed"
                task.completed_at = current_iso_timestamp()
                task.consensus_outcome = "verified"
                self.task_repo.add_task(task)
        elif outcome == "conflict":
            entry.review_status = "conflict"
            entry.verification_status = "needs_review"
            self.vocab_repo.add(entry)
            task = self.task_repo.get_open_task_for_entry(entry.id)
            if task:
                task.status = "conflict"
                task.unresolved_disagreements = conflicting
                self.task_repo.add_task(task)
        elif outcome == "correction_requested":
            entry.review_status = "needs_correction"
            entry.verification_status = "needs_review"
            self.vocab_repo.add(entry)
            task = self.task_repo.get_open_task_for_entry(entry.id)
            if task:
                task.status = "correction_requested"
                self.task_repo.add_task(task)
        elif outcome == "rejected":
            entry.review_status = "rejected"
            entry.verification_status = "unverified"
            entry.license_restrictions = "restricted"
            self.vocab_repo.add(entry)
            self.vocab_repo.remove_from_fts(entry.id)
            task = self.task_repo.get_open_task_for_entry(entry.id)
            if task:
                task.status = "completed"
                task.completed_at = current_iso_timestamp()
                task.consensus_outcome = "rejected"
                self.task_repo.add_task(task)
        elif outcome == "pending_consensus":
            if entry.verification_status == "verified":
                entry.verification_status = "unverified"
                entry.review_status = "pending_review"
                self.vocab_repo.add(entry)
                self.vocab_repo.remove_from_fts(entry.id)

        eval_res = ConsensusEvaluation(
            entry_id=entry.id,
            policy_version=pol.policy_version,
            threshold_required=needed,
            eligible_reviewers_count=eligible_count,
            approvals_count=len(approving),
            rejections_count=len(rejecting),
            conflicts_count=len(conflicting),
            corrections_count=len(corrections),
            decision_outcome=outcome,
            is_consensus_met=is_consensus_met,
            is_source_verified=is_source_verified,
            is_permission_cleared=is_permission_cleared,
            is_public_eligible=is_public_eligible,
            evaluated_at=current_iso_timestamp(),
            approving_reviewers=approving,
            rejecting_reviewers=rejecting,
            conflicting_reviewers=conflicting,
            correction_reviewers=corrections,
            notes="; ".join(notes_parts) if notes_parts else None,
            single_reviewer_exception_applied=pol.allow_single_reviewer_exception,
        )

        self.consensus_repo.record_evaluation(eval_res)
        return eval_res

    def create_review_tasks(self, limit: int = 100) -> list[ReviewTask]:
        """Generate structured review tasks for candidates requiring attention."""
        candidates = self.vocab_repo.list_review_queue(limit=limit, offset=0)
        created_tasks: list[ReviewTask] = []

        for cand in candidates:
            # Check if task already exists
            existing = self.task_repo.get_open_task_for_entry(cand.id)
            if existing is not None:
                continue

            # Skip verified entries unless conflicted
            if cand.verification_status == "verified" and cand.review_status != "conflict":
                continue

            dimensions = ["spelling", "meaning", "pos", "dialect"]
            source_id = cand.provenance[0].source_id if cand.provenance else None

            if not cand.meanings:
                priority = "high"
                task_type = "meaning_review"
                reason = "Candidate entry is missing verified meanings/definitions."
            elif cand.review_status == "conflict":
                priority = "high"
                task_type = "conflict_resolution"
                reason = "Conflicting definitions or dialect forms across reviewers."
            elif cand.dialect is None:
                priority = "medium"
                task_type = "dialect_review"
                reason = "Dialect classification is unassigned."
            elif self.find_duplicate_suggestions(cand, threshold=0.75):
                priority = "medium"
                task_type = "duplicate_review"
                reason = "Potential duplicate entries detected."
            else:
                priority = "low"
                task_type = "general_validation"
                reason = "Candidate awaiting independent reviewer consensus."

            task_id = f"TASK-{cand.id}"

            task = ReviewTask(
                id=task_id,
                entry_id=cand.id,
                headword=cand.headword,
                task_type=task_type,
                review_dimensions=dimensions,
                source_id=source_id,
                priority=priority,
                reason=reason,
                status="open",
                created_at=current_iso_timestamp(),
            )
            self.task_repo.add_task(task)
            created_tasks.append(task)

        return created_tasks

    def claim_task(self, task_id: str, reviewer: str) -> ReviewTask:
        """Claim or assign an open review task to an attributable reviewer."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Reviewer identifier or pseudonym is required.")
        task = self.task_repo.get_task(task_id)
        if task is None:
            raise ResourceNotFoundError(f"Review task '{task_id}' not found.")
        task.assigned_reviewer = reviewer.strip()
        task.status = "in_review"
        self.task_repo.add_task(task)
        return task

    def list_tasks(
        self,
        status: str | None = None,
        priority: str | None = None,
        assigned_reviewer: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ReviewTask]:
        """List review tasks with deterministic filtering."""
        return self.task_repo.list_tasks(
            status=status,
            priority=priority,
            assigned_reviewer=assigned_reviewer,
            limit=limit,
            offset=offset,
        )

    def get_task(self, task_id: str) -> ReviewTask | None:
        """Fetch review task by ID."""
        return self.task_repo.get_task(task_id)

    def export_review_package(
        self,
        output_path: Path | str,
        task_ids: list[str] | None = None,
        entry_ids: list[str] | None = None,
        limit: int = 100,
    ) -> int:
        """Export versioned review package for offline community review."""
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        tasks_to_export: list[ReviewTask] = []
        if task_ids:
            for tid in task_ids:
                t = self.task_repo.get_task(tid)
                if t and t.status != "completed":
                    tasks_to_export.append(t)
        elif entry_ids:
            for eid in entry_ids:
                t = self.task_repo.get_open_task_for_entry(eid)
                if t:
                    tasks_to_export.append(t)
                else:
                    entry = self.vocab_repo.get_by_id(eid)
                    if entry:
                        tasks_to_export.append(
                            ReviewTask(
                                id=f"TASK-{entry.id}",
                                entry_id=entry.id,
                                headword=entry.headword,
                                task_type="general_validation",
                                review_dimensions=["meaning", "spelling", "pos", "dialect"],
                                reason="Offline review package request",
                                status="open",
                                created_at=current_iso_timestamp(),
                            )
                        )
        else:
            tasks_to_export = self.task_repo.list_tasks(status="open", limit=limit)
            if not tasks_to_export:
                self.create_review_tasks(limit=limit)
                tasks_to_export = self.task_repo.list_tasks(status="open", limit=limit)

        package_items = []
        for t in tasks_to_export:
            entry = self.vocab_repo.get_by_id(t.entry_id)
            if entry is None:
                continue

            is_restricted = entry.license_restrictions == "restricted"
            safe_examples = []
            for ex in entry.example_sentences:
                if is_restricted:
                    safe_examples.append("[RESTRICTED TEXT - ACCESS PRIVILEGED]")
                else:
                    safe_examples.append(ex)

            safe_prov = []
            for p in entry.provenance:
                p_perm = (p.permission_status or "").strip().lower()
                p_is_restr = p_perm == "restricted"
                context_str = p.context_sentence
                if p_is_restr and context_str:
                    context_str = "[RESTRICTED TEXT - ACCESS PRIVILEGED]"
                safe_prov.append({
                    "source_id": p.source_id,
                    "citation": p.citation,
                    "page_or_section": p.page_or_section,
                    "context_sentence": context_str,
                    "permission_status": p.permission_status,
                })

            item = {
                "task_id": t.id,
                "entry_id": t.entry_id,
                "headword": t.headword,
                "alternative_spellings": entry.alternative_spellings,
                "meanings": entry.meanings,
                "translations_en": entry.translations_en,
                "part_of_speech": entry.part_of_speech,
                "dialect": entry.dialect,
                "example_sentences": safe_examples,
                "provenance": safe_prov,
                "review_dimensions": t.review_dimensions,
                "priority": t.priority,
                "reason": t.reason,
                "baseline_updated_at": entry.reviewed_at or "",
                "submission": {
                    "reviewer": t.assigned_reviewer or "",
                    "decision": "",
                    "spelling_assessment": "",
                    "meaning_assessment": "",
                    "pos_assessment": "",
                    "dialect_assessment": "",
                    "source_assessment": "",
                    "correction_proposals": {},
                    "notes": "",
                },
            }
            package_items.append(item)

        package_data = {
            "package_schema_version": "2.0",
            "exported_at": current_iso_timestamp(),
            "task_count": len(package_items),
            "tasks": package_items,
        }

        with out_p.open("w", encoding="utf-8") as f:
            json.dump(package_data, f, ensure_ascii=False, indent=2)

        return len(package_items)

    def validate_review_package(
        self,
        input_path: Path | str,
    ) -> dict[str, Any]:
        """Validate review package schema, decisions, timestamps, and detect conflicts."""
        in_p = Path(input_path)
        if not in_p.exists():
            raise FileNotFoundError(f"Package file '{input_path}' not found.")

        try:
            with in_p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Invalid JSON: {e}"],
                "warnings": [],
                "total_tasks": 0,
                "valid_submissions": 0,
                "stale_conflicts": 0,
            }

        version = data.get("package_schema_version")
        if version not in {"1.0", "2.0"}:
            return {
                "valid": False,
                "errors": [
                    f"Unsupported package schema version '{version}'. Expected '1.0' or '2.0'."
                ],
                "warnings": [],
                "total_tasks": 0,
                "valid_submissions": 0,
                "stale_conflicts": 0,
            }

        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            return {
                "valid": False,
                "errors": ["Package missing 'tasks' array."],
                "warnings": [],
                "total_tasks": 0,
                "valid_submissions": 0,
                "stale_conflicts": 0,
            }

        errors: list[str] = []
        warnings: list[str] = []
        valid_items = 0
        stale_conflicts = 0

        for i, item in enumerate(tasks, start=1):
            entry_id = item.get("entry_id")
            if not entry_id:
                errors.append(f"Task #{i}: Missing required 'entry_id'.")
                continue

            entry = self.vocab_repo.get_by_id(entry_id)
            if entry is None:
                errors.append(f"Task #{i}: Entry '{entry_id}' does not exist in library.")
                continue

            sub = item.get("submission") or {}
            decision = sub.get("decision", "").strip().lower()
            reviewer = sub.get("reviewer", "").strip()

            if not decision:
                warnings.append(f"Task #{i} ({entry_id}): Submission decision is empty.")
                continue

            if decision not in VALID_REVIEW_DECISIONS:
                errors.append(
                    f"Task #{i} ({entry_id}): Invalid decision '{decision}'. "
                    f"Allowed: {sorted(VALID_REVIEW_DECISIONS)}."
                )
                continue

            if not reviewer:
                errors.append(f"Task #{i} ({entry_id}): Reviewer identifier or pseudonym missing.")
                continue

            if self.policy.eligible_reviewers is not None:
                if reviewer not in self.policy.eligible_reviewers:
                    warnings.append(
                        f"Task #{i} ({entry_id}): Reviewer '{reviewer}' is not in configured "
                        "eligible reviewer list."
                    )

            # Check duplicate submission
            existing_reviews = self.review_repo.get_reviews_for_entry(entry_id)
            notes = (sub.get("notes") or "").strip()
            is_dup = any(
                r.reviewer == reviewer
                and r.decision == decision
                and (r.notes or "").strip() == notes
                for r in existing_reviews
            )
            if is_dup:
                warnings.append(
                    f"Task #{i} ({entry_id}): Duplicate submission for reviewer '{reviewer}'."
                )

            # Check stale package conflict
            baseline_ts = item.get("baseline_updated_at")
            if baseline_ts and entry.reviewed_at:
                if entry.reviewed_at > baseline_ts:
                    stale_conflicts += 1
                    warnings.append(
                        f"Task #{i} ({entry_id}): Stale package detected. Entry was reviewed at "
                        f"{entry.reviewed_at} after package export at {baseline_ts}."
                    )

            valid_items += 1

        is_valid = len(errors) == 0 and valid_items > 0
        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "total_tasks": len(tasks),
            "valid_submissions": valid_items,
            "stale_conflicts": stale_conflicts,
        }

    def import_review_package(
        self,
        input_path: Path | str,
        default_reviewer: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Validate and apply reviewed package decisions, updating consensus."""
        val = self.validate_review_package(input_path)
        if not val["valid"] and not dry_run:
            return {
                "applied_count": 0,
                "errors": val["errors"],
                "warnings": val["warnings"],
                "dry_run": dry_run,
            }

        if dry_run:
            return {
                "applied_count": val["valid_submissions"],
                "valid": val["valid"],
                "errors": val["errors"],
                "warnings": val["warnings"],
                "dry_run": True,
            }

        with Path(input_path).open("r", encoding="utf-8") as f:
            data = json.load(f)

        applied = 0
        evaluations = []
        import_errors = []

        for item in data.get("tasks", []):
            entry_id = item.get("entry_id")
            sub = item.get("submission") or {}
            dec = sub.get("decision", "").strip().lower()
            rev = sub.get("reviewer", "").strip() or (default_reviewer or "").strip()

            if not dec or not rev or not entry_id:
                continue

            try:
                rec, eval_res = self.record_decision(
                    entry_id=entry_id,
                    reviewer=rev,
                    decision=dec,
                    spelling_assessment=sub.get("spelling_assessment"),
                    meaning_assessment=sub.get("meaning_assessment"),
                    pos_assessment=sub.get("pos_assessment"),
                    dialect_assessment=sub.get("dialect_assessment"),
                    source_assessment=sub.get("source_assessment"),
                    correction_proposals=sub.get("correction_proposals"),
                    notes=sub.get("notes"),
                    auto_evaluate_consensus=True,
                )
                applied += 1
                if eval_res:
                    evaluations.append(eval_res.to_dict())
            except Exception as e:
                import_errors.append(f"Entry '{entry_id}': {e}")

        return {
            "applied_count": applied,
            "errors": import_errors,
            "warnings": val["warnings"],
            "evaluations": evaluations,
            "dry_run": False,
        }

    def get_review_metrics(self) -> dict[str, Any]:
        """Calculate review quality, consensus status, and governance metrics."""
        all_entries = self.vocab_repo.list_all()
        total_entries = len(all_entries)
        candidates = [e for e in all_entries if e.verification_status != "verified"]
        total_candidates = len(candidates)

        open_tasks = self.task_repo.count_tasks(status="open")
        in_review_tasks = self.task_repo.count_tasks(status="in_review")
        completed_tasks = self.task_repo.count_tasks(status="completed")
        conflict_tasks = self.task_repo.count_tasks(status="conflict")
        correction_tasks = self.task_repo.count_tasks(status="correction_requested")

        all_reviews = self.review_repo.get_all_reviews()
        entries_with_reviews = len({r.entry_id for r in all_reviews})

        reviewer_counts: dict[str, int] = {}
        for r in all_reviews:
            reviewer_counts[r.reviewer] = reviewer_counts.get(r.reviewer, 0) + 1

        entries_meeting_consensus = sum(
            1 for e in all_entries if e.verification_status == "verified"
        )
        entries_conflicted = sum(
            1 for e in all_entries if e.review_status == "conflict"
        )
        entries_needs_correction = sum(
            1 for e in all_entries if e.review_status == "needs_correction"
        )
        entries_lacking_source = sum(
            1 for e in all_entries if len(e.provenance) == 0
        )
        entries_restricted = sum(
            1 for e in all_entries
            if e.license_restrictions == "restricted"
            or any((p.permission_status or "").lower() == "restricted" for p in e.provenance)
        )

        completed_task_objs = self.task_repo.list_tasks(status="completed", limit=1000)
        durations = []
        for t in completed_task_objs:
            if t.created_at and t.completed_at:
                try:
                    c_dt = datetime.datetime.fromisoformat(t.created_at)
                    f_dt = datetime.datetime.fromisoformat(t.completed_at)
                    durations.append((f_dt - c_dt).total_seconds())
                except Exception:
                    pass
        avg_time = round(sum(durations) / len(durations), 1) if durations else None

        return {
            "total_entries": total_entries,
            "total_candidates": total_candidates,
            "tasks": {
                "open": open_tasks,
                "in_review": in_review_tasks,
                "completed": completed_tasks,
                "conflict": conflict_tasks,
                "correction_requested": correction_tasks,
                "total_tasks": (
                    open_tasks
                    + in_review_tasks
                    + completed_tasks
                    + conflict_tasks
                    + correction_tasks
                ),
            },
            "entries_with_reviews": entries_with_reviews,
            "entries_meeting_consensus": entries_meeting_consensus,
            "entries_with_conflicts": entries_conflicted,
            "entries_awaiting_corrections": entries_needs_correction,
            "entries_lacking_source_evidence": entries_lacking_source,
            "entries_blocked_by_permissions": entries_restricted,
            "reviewer_activity": reviewer_counts,
            "average_review_time_seconds": avg_time,
            "consensus_policy": {
                "version": self.policy.policy_version,
                "threshold": self.policy.required_approvals,
                "single_reviewer_exception": self.policy.allow_single_reviewer_exception,
                "eligible_reviewers_count": (
                    len(self.policy.eligible_reviewers)
                    if self.policy.eligible_reviewers is not None
                    else "unrestricted"
                ),
            },
        }

    def get_unresolved_conflicts(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return list of entries with active conflicting review decisions."""
        conflicted_entries = self.vocab_repo.list_review_queue(
            review_status="conflict", limit=limit
        )
        results = []
        for e in conflicted_entries:
            details = self.get_candidate_details(e.id)
            results.append({
                "entry_id": e.id,
                "headword": e.headword,
                "dialect": e.dialect,
                "meanings": e.meanings,
                "review_history": details["review_history"],
            })
        return results
