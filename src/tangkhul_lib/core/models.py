"""Core domain models and schema definitions for Tangkhul Language Library."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

VALID_RESOURCE_TYPES = frozenset({
    "books",
    "songs",
    "dictionaries",
    "culture",
    "history",
    "literature",
})

VALID_PERMISSION_STATUSES = frozenset({
    "pending",
    "permitted",
    "public_domain",
    "community_authorized",
    "restricted",
})

VALID_VERIFICATION_STATUSES = frozenset({
    "unverified",
    "partially_verified",
    "verified",
    "community_reviewed",
    "needs_review",
})

VALID_ACCESS_STATUSES = frozenset({
    "metadata_only",
    "full_text_available",
    "restricted",
    "open_access",
    "attributed",
    "permission_pending",
    "unknown",
})

VALID_REVIEW_STATUSES = frozenset({
    "pending_review",
    "reviewed_uncertain",
    "accepted",
    "rejected",
    "duplicate",
    "conflict",
    "needs_correction",
})

VALID_REVIEW_DECISIONS = frozenset({
    "accept",
    "approve",
    "reject",
    "uncertain",
    "correction_requested",
    "flag_conflict",
    "withdraw_approval",
    "duplicate",
    "conflict",
    "edit",
})

VALID_TASK_STATUSES = frozenset({
    "open",
    "in_review",
    "correction_requested",
    "conflict",
    "completed",
})

VALID_TASK_PRIORITIES = frozenset({
    "high",
    "medium",
    "low",
})


@dataclass
class ManifestRecord:
    """Represents a catalogued resource in the JSON Lines manifest."""

    id: str
    resource_type: str
    title: str
    title_translation: str | None = None
    creator: str | None = None
    year: int | None = None
    publisher: str | None = None
    language: str = "Tangkhul"
    dialect: str | None = None
    source_url: str | None = None
    source_identifier: str | None = None
    license: str | None = None
    permission_status: str = "pending"
    local_path: str | None = None
    verification_status: str = "unverified"
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert manifest record to a clean dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ManifestRecord:
        """Create ManifestRecord from dictionary, ignoring extraneous keys."""
        d = dict(data)
        if "local_path" not in d and "local_file_path" in d:
            d["local_path"] = d["local_file_path"]
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        return cls(**filtered)



@dataclass
class ProvenanceRecord:
    """Preserves attribution, source linking, and citation for extracted items."""

    source_id: str
    resource_type: str
    citation: str
    page_or_section: str | None = None
    context_sentence: str | None = None
    recorded_year: int | None = None
    permission_status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VocabularyEntry:
    """Unified vocabulary entry linking words across all modules."""

    id: str
    headword: str
    meanings: list[str] = field(default_factory=list)
    translations_en: list[str] = field(default_factory=list)
    alternative_spellings: list[str] = field(default_factory=list)
    dialect_variants: list[str] = field(default_factory=list)
    dialect: str | None = None
    part_of_speech: str | None = None
    pronunciation: str | None = None
    example_sentences: list[str] = field(default_factory=list)
    provenance: list[ProvenanceRecord] = field(default_factory=list)
    verification_status: str = "unverified"
    license_restrictions: str | None = None
    review_status: str = "pending_review"
    review_notes: str | None = None
    reviewer: str | None = None
    reviewed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["provenance"] = [p.to_dict() for p in self.provenance]
        return result


@dataclass
class VocabularyReviewRecord:
    """Audit record capturing human review decisions, provenance edits, and rationale."""

    entry_id: str
    headword: str
    decision: str
    reviewer: str
    id: int | None = None
    review_timestamp: str = ""
    notes: str | None = None
    previous_state: dict[str, Any] | None = None
    new_state: dict[str, Any] | None = None
    suggested_meaning: str | None = None
    suggested_pos: str | None = None
    suggested_dialect: str | None = None
    target_duplicate_id: str | None = None
    spelling_assessment: str | None = None
    meaning_assessment: str | None = None
    pos_assessment: str | None = None
    dialect_assessment: str | None = None
    example_assessment: str | None = None
    source_assessment: str | None = None
    correction_proposals: dict[str, Any] | None = None
    counts_for_consensus: bool = True
    superseded_by_id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VocabularyReviewRecord:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        if isinstance(filtered.get("correction_proposals"), str):
            try:
                filtered["correction_proposals"] = json.loads(filtered["correction_proposals"])
            except Exception:
                filtered["correction_proposals"] = None
        if "counts_for_consensus" in filtered:
            filtered["counts_for_consensus"] = bool(filtered["counts_for_consensus"])
        return cls(**filtered)


@dataclass
class ReviewTask:
    """Structured review task identifying items requiring validation or consensus."""

    id: str
    entry_id: str
    headword: str
    task_type: str = "full_review"
    review_dimensions: list[str] = field(default_factory=lambda: ["meaning", "spelling"])
    source_id: str | None = None
    priority: str = "medium"
    reason: str = ""
    status: str = "open"  # open, in_review, correction_requested, conflict, completed
    assigned_reviewer: str | None = None
    created_at: str = ""
    completed_at: str | None = None
    unresolved_disagreements: list[str] = field(default_factory=list)
    consensus_outcome: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReviewTask:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        if isinstance(filtered.get("review_dimensions"), str):
            try:
                filtered["review_dimensions"] = json.loads(filtered["review_dimensions"])
            except Exception:
                filtered["review_dimensions"] = [filtered["review_dimensions"]]
        if isinstance(filtered.get("unresolved_disagreements"), str):
            try:
                filtered["unresolved_disagreements"] = json.loads(
                    filtered["unresolved_disagreements"]
                )
            except Exception:
                filtered["unresolved_disagreements"] = []
        return cls(**filtered)


@dataclass
class ConsensusEvaluation:
    """Result of multi-reviewer consensus evaluation and permission checks."""

    entry_id: str
    policy_version: str
    threshold_required: int
    eligible_reviewers_count: int
    approvals_count: int
    rejections_count: int
    conflicts_count: int
    corrections_count: int
    decision_outcome: str
    is_consensus_met: bool
    is_source_verified: bool
    is_permission_cleared: bool
    is_public_eligible: bool
    evaluated_at: str
    approving_reviewers: list[str] = field(default_factory=list)
    rejecting_reviewers: list[str] = field(default_factory=list)
    conflicting_reviewers: list[str] = field(default_factory=list)
    correction_reviewers: list[str] = field(default_factory=list)
    notes: str | None = None
    single_reviewer_exception_applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IngestedDocument:
    """Represents an ingested digital document or authorized scan."""

    id: str
    source_id: str
    source_title: str
    creator: str | None = None
    publication_year: int | None = None
    source_type: str = "books"
    language: str = "Tangkhul"
    file_path: str = ""
    file_name: str = ""
    file_hash: str = ""
    file_size_bytes: int = 0
    file_format: str = "pdf"
    extraction_method: str = "pdf_pypdf"
    extraction_timestamp: str = ""
    extraction_status: str = "extracted"
    page_count: int = 0
    char_count: int = 0
    word_count: int = 0
    permission_status: str = "pending"
    verification_status: str = "unverified"
    extraction_warnings: list[str] = field(default_factory=list)
    ocr_status: str = "not_required"
    review_status: str = "pending_review"
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IngestedDocument:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class DocumentChunk:
    """Represents an extracted paragraph or textual unit with location provenance."""

    id: str
    document_id: str
    source_id: str
    page_number: int | None = None
    section_heading: str | None = None
    chunk_index: int = 0
    text: str = ""
    char_count: int = 0
    word_count: int = 0
    content_hash: str = ""
    permission_status: str = "pending"
    verification_status: str = "unverified"
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DocumentChunk:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

