"""Domain models for Tangkhul historical records, events, figures, places, and timelines."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError, PermissionDeniedError
from tangkhul_lib.core.models import (
    VALID_ACCESS_STATUSES,
    VALID_PERMISSION_STATUSES,
    VALID_VERIFICATION_STATUSES,
    ManifestRecord,
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.vocabulary.normalization import normalize_unicode

VALID_HISTORY_RECORD_TYPES = frozenset({
    "historical_event",
    "person",
    "place",
    "migration",
    "community_history",
    "language_history",
    "historical_document",
    "timeline_event",
    "oral_history",
})

VALID_EVIDENCE_TYPES = frozenset({
    "primary_source",
    "archival_record",
    "scholarly_interpretation",
    "oral_tradition",
    "ethnographic_account",
    "epigraphic_evidence",
    "candidate_fieldwork",
})


@dataclass
class HistoricalRecord:
    """Represents a source-backed Tangkhul historical record, event, person, or settlement."""

    id: str
    title: str
    record_type: str = "historical_event"
    alternate_titles: list[str] = field(default_factory=list)
    summary: str | None = None
    description: str | None = None
    original_text: str | None = None
    translation_en: str | None = None
    event_date: str | None = None
    sort_year: int | None = None
    period: str | None = None
    place: str | None = None
    village: str | None = None
    dialect: str | None = None
    language: str = "Tangkhul"
    people_involved: list[str] = field(default_factory=list)
    related_events: list[str] = field(default_factory=list)
    related_records: list[str] = field(default_factory=list)
    source_id: str | None = None
    source_title: str | None = None
    source_page: str | None = None
    source_section: str | None = None
    source_url: str | None = None
    contributor: str | None = None
    contributor_consent: bool = True
    evidence_type: str = "scholarly_interpretation"
    confidence: float = 1.0
    contradictory_accounts: list[str] = field(default_factory=list)
    license: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None
    resource_type: str = "history"

    def validate(self) -> None:
        """Validate integrity and schema constraints of the historical record."""
        if not self.id or not self.id.strip():
            raise ManifestValidationError("Historical record missing required field 'id'.")
        if not self.title or not self.title.strip():
            raise ManifestValidationError(
                f"Historical record '{self.id}' missing required field 'title'.",
                record_id=self.id,
            )
        if not self.record_type or not self.record_type.strip():
            raise ManifestValidationError(
                f"Historical record '{self.id}' missing required field 'record_type'.",
                record_id=self.id,
            )
        if self.record_type not in VALID_HISTORY_RECORD_TYPES:
            raise ManifestValidationError(
                f"Historical record '{self.id}' has invalid record_type "
                f"'{self.record_type}'.",
                record_id=self.id,
            )
        if self.evidence_type not in VALID_EVIDENCE_TYPES:
            raise ManifestValidationError(
                f"Historical record '{self.id}' has invalid evidence_type "
                f"'{self.evidence_type}'.",
                record_id=self.id,
            )
        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Historical record '{self.id}' has invalid permission_status "
                f"'{self.permission_status}'.",
                record_id=self.id,
            )
        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Historical record '{self.id}' has invalid access_status "
                f"'{self.access_status}'.",
                record_id=self.id,
            )
        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Historical record '{self.id}' has invalid verification_status "
                f"'{self.verification_status}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert historical record to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HistoricalRecord:
        """Create HistoricalRecord from dictionary, handling manifest alias fields."""
        d = dict(data)

        # Handle record_type vs category alias
        if "category" in d and not d.get("record_type"):
            d["record_type"] = d.pop("category")

        # Handle year -> sort_year
        if "year" in d and d.get("sort_year") is None:
            val = d.pop("year")
            if isinstance(val, int):
                d["sort_year"] = val
            elif isinstance(val, str) and val.isdigit():
                d["sort_year"] = int(val)

        # Handle title_translation -> translation_en
        if "title_translation" in d and not d.get("translation_en"):
            d["translation_en"] = d.pop("title_translation")

        # Handle creator -> contributor
        if "creator" in d and not d.get("contributor"):
            d["contributor"] = d.pop("creator")

        # Handle publisher -> source_title
        if "publisher" in d and not d.get("source_title"):
            d["source_title"] = d.pop("publisher")

        # Handle source_identifier -> source_id
        if "source_identifier" in d and not d.get("source_id"):
            d["source_id"] = d.pop("source_identifier")

        # Filter fields matching dataclass
        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in d.items() if k in valid_fields}

        # Ensure list fields are lists
        for list_fld in (
            "alternate_titles",
            "people_involved",
            "related_events",
            "related_records",
            "contradictory_accounts",
        ):
            if list_fld in filtered and isinstance(filtered[list_fld], str):
                filtered[list_fld] = [filtered[list_fld]]
            elif list_fld not in filtered:
                filtered[list_fld] = []

        return cls(**filtered)

    def to_manifest_record(self) -> ManifestRecord:
        """Produce standard ManifestRecord representation for cross-module catalogue."""
        self.validate()
        return ManifestRecord(
            id=self.id,
            resource_type="history",
            title=self.title,
            title_translation=self.translation_en,
            creator=self.contributor,
            year=self.sort_year,
            publisher=self.source_title,
            language=self.language or "Tangkhul",
            dialect=self.dialect,
            source_url=self.source_url,
            source_identifier=self.source_id,
            license=self.license,
            permission_status=self.permission_status,
            local_path=None,
            verification_status=self.verification_status,
            notes=self.notes,
        )

    def to_manifest_dict(self) -> dict[str, Any]:
        """Convert to manifest-compliant JSONL dictionary."""
        return {
            "id": self.id,
            "resource_type": "history",
            "title": self.title,
            "title_translation": self.translation_en,
            "creator": self.contributor,
            "year": self.sort_year,
            "publisher": self.source_title,
            "language": self.language or "Tangkhul",
            "dialect": self.dialect,
            "category": self.record_type,
            "source_url": self.source_url,
            "source_identifier": self.source_id,
            "license": self.license,
            "permission_status": self.permission_status,
            "local_path": None,
            "verification_status": self.verification_status,
            "notes": self.notes,
        }

    def extract_vocabulary_candidates(self) -> list[dict[str, Any]]:
        """Extract candidate historical terms, place names, and phrases from this record.

        Raises:
            PermissionDeniedError: If the record is restricted or lacks contributor consent.
        """
        if self.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot extract vocabulary from restricted historical record '{self.id}'.",
                resource_id=self.id,
            )
        if not self.contributor_consent:
            raise PermissionDeniedError(
                f"Consent not granted for vocabulary extraction from record '{self.id}'.",
                resource_id=self.id,
            )

        candidates: list[dict[str, Any]] = []

        # 1. Original text if present
        if self.original_text:
            cleaned = normalize_unicode(self.original_text)
            words = re.findall(r"[\w'-]+", cleaned)
            for w in words:
                w_clean = w.strip()
                if len(w_clean) > 1 and not w_clean.isdigit():
                    candidates.append({
                        "word_form": w_clean,
                        "source_id": self.id,
                        "context_sentence": self.original_text,
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "historical_text_extraction",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # 2. Historical place names, people, or title terms
        for term_source in [self.place, self.village, self.title, *self.people_involved]:
            if not term_source:
                continue
            norm_term = normalize_unicode(term_source)
            for part in norm_term.split():
                clean_part = part.strip(",.:;\"'()[]")
                common_exclusions = {
                    "history", "historical", "event", "period", "battle", "the", "and", "of",
                }
                if (
                    len(clean_part) > 2
                    and not clean_part.isdigit()
                    and clean_part.lower() not in common_exclusions
                ):
                    ctx = f"{self.title} - {self.summary or self.notes or ''}"
                    candidates.append({
                        "word_form": clean_part,
                        "source_id": self.id,
                        "context_sentence": ctx,
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "historical_entity_extraction",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # Deduplicate candidates
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for c in candidates:
            w_norm = c["word_form"].lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(c)

        return deduped

    def to_vocabulary_entry(self, headword: str) -> VocabularyEntry:
        """Construct a new VocabularyEntry rooted in this historical record's provenance."""
        norm_headword = normalize_unicode(headword)
        meaning = self.translation_en or self.summary or self.title
        meanings = [meaning] if meaning else []

        prov = ProvenanceRecord(
            source_id=self.id,
            resource_type="history",
            citation=f"{self.title} ({self.source_title or 'Historical Record'})",
            page_or_section=self.source_page or self.source_section,
            context_sentence=self.original_text or self.summary or self.notes,
            recorded_year=self.sort_year,
            permission_status=self.permission_status,
        )

        return VocabularyEntry(
            id=f"VOCAB-{self.id}-{norm_headword.lower()}",
            headword=norm_headword,
            meanings=meanings,
            translations_en=meanings,
            dialect=self.dialect,
            example_sentences=[self.original_text] if self.original_text else [],
            verification_status="needs_review",
            license_restrictions=self.license,
            provenance=[prov],
        )
