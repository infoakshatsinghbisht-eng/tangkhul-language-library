"""Domain models for Tangkhul cultural records, proverbs, customs, festivals, and rituals."""

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

VALID_CULTURE_CATEGORIES = frozenset({
    "proverb",
    "custom",
    "festival",
    "ritual",
    "tradition",
    "oral_tradition",
})


@dataclass
class CulturalRecord:
    """Comprehensive domain model for a Tangkhul cultural entity, custom, or oral tradition."""

    id: str
    title: str
    category: str
    local_name: str | None = None
    alternate_names: list[str] = field(default_factory=list)
    subcategory: str | None = None
    original_text: str | None = None
    translation_en: str | None = None
    translations_other: list[str] = field(default_factory=list)
    description: str | None = None
    cultural_significance: str | None = None
    season_or_timing: str | None = None
    village: str | None = None
    dialect: str | None = None
    language: str = "Tangkhul"
    participants: list[str] = field(default_factory=list)
    procedure: list[str] = field(default_factory=list)
    related_records: list[str] = field(default_factory=list)
    historical_period: str | None = None
    year: int | None = None
    source_id: str | None = None
    source_title: str | None = None
    source_page: str | None = None
    source_section: str | None = None
    source_url: str | None = None
    contributor: str | None = None
    contributor_consent: bool = True
    license: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None
    resource_type: str = "culture"

    def validate(self) -> None:
        """Validate integrity and schema constraints of the cultural record."""
        if not self.id or not self.id.strip():
            raise ManifestValidationError("Cultural record missing required field 'id'.")
        if not self.title or not self.title.strip():
            raise ManifestValidationError(
                f"Cultural record '{self.id}' missing required field 'title'.",
                record_id=self.id,
            )
        if not self.category or not self.category.strip():
            raise ManifestValidationError(
                f"Cultural record '{self.id}' missing required field 'category'.",
                record_id=self.id,
            )
        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Cultural record '{self.id}' has invalid permission_status "
                f"'{self.permission_status}'.",
                record_id=self.id,
            )
        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Cultural record '{self.id}' has invalid access_status "
                f"'{self.access_status}'.",
                record_id=self.id,
            )
        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Cultural record '{self.id}' has invalid verification_status "
                f"'{self.verification_status}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert cultural record to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CulturalRecord:
        """Create CulturalRecord from dictionary, normalizing manifest alias fields."""
        d = dict(data)

        # Handle title translation alias
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

        # Parse local_name if not provided but present in title (e.g. 'Luira Phanit' or title)
        if not d.get("local_name"):
            d["local_name"] = d.get("title")

        # Parse original_text from notes if missing (e.g. "Original saying: '...'")
        notes_str = d.get("notes") or ""
        if not d.get("original_text") and "Original saying:" in notes_str:
            match = re.search(r"Original saying:\s*['\"]([^'\"]+)['\"]", notes_str)
            if match:
                d["original_text"] = match.group(1).strip()

        # Filter only fields that belong to CulturalRecord
        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in d.items() if k in valid_fields}

        # Ensure lists are lists
        for list_fld in (
            "alternate_names",
            "translations_other",
            "participants",
            "procedure",
            "related_records",
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
            resource_type="culture",
            title=self.title,
            title_translation=self.translation_en,
            creator=self.contributor,
            year=self.year,
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
            "resource_type": "culture",
            "title": self.title,
            "title_translation": self.translation_en,
            "creator": self.contributor,
            "year": self.year,
            "publisher": self.source_title,
            "language": self.language or "Tangkhul",
            "dialect": self.dialect,
            "category": self.category,
            "subcategory": self.subcategory,
            "source_url": self.source_url,
            "source_identifier": self.source_id,
            "license": self.license,
            "permission_status": self.permission_status,
            "local_path": None,
            "verification_status": self.verification_status,
            "notes": self.notes,
        }

    def extract_vocabulary_candidates(self) -> list[dict[str, Any]]:
        """Extract candidate Tangkhul lexical items and phrases from this authorized record.

        Raises:
            PermissionDeniedError: If the record is restricted or lacks contributor consent.
        """
        if self.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot extract vocabulary from restricted cultural record '{self.id}'.",
                resource_id=self.id,
            )
        if not self.contributor_consent:
            raise PermissionDeniedError(
                f"Consent not granted for vocabulary extraction from record '{self.id}'.",
                resource_id=self.id,
            )

        candidates: list[dict[str, Any]] = []

        # 1. If original_text is present (e.g. proverb, song, or prayer)
        if self.original_text:
            cleaned_text = normalize_unicode(self.original_text)
            words = re.findall(r"[\w'-]+", cleaned_text)
            for w in words:
                w_clean = w.strip()
                if len(w_clean) > 1 and not w_clean.isdigit():
                    candidates.append({
                        "word_form": w_clean,
                        "source_id": self.id,
                        "context_sentence": self.original_text,
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "cultural_text_extraction",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # 2. Extract key cultural local name / title terms
        for term_source in [self.local_name, self.title]:
            if not term_source:
                continue
            norm_term = normalize_unicode(term_source)
            for part in norm_term.split():
                clean_part = part.strip(",.:;\"'()[]")
                common_exclusions = {
                    "proverb", "festival", "tradition", "custom", "the", "and",
                }
                if (
                    len(clean_part) > 2
                    and not clean_part.isdigit()
                    and clean_part.lower() not in common_exclusions
                ):
                    ctx = f"{self.title} - {self.description or self.notes or ''}"
                    candidates.append({
                        "word_form": clean_part,
                        "source_id": self.id,
                        "context_sentence": ctx,
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "cultural_title_extraction",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # Deduplicate candidates by word_form
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for c in candidates:
            w_norm = c["word_form"].lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(c)

        return deduped

    def to_vocabulary_entry(self, headword: str) -> VocabularyEntry:
        """Construct a new VocabularyEntry rooted in this cultural record's provenance."""
        norm_headword = normalize_unicode(headword)
        meaning = self.translation_en or self.description or self.title
        meanings = [meaning] if meaning else []

        prov = ProvenanceRecord(
            source_id=self.id,
            resource_type="culture",
            citation=f"{self.title} ({self.source_title or 'Cultural Source'})",
            page_or_section=self.source_page or self.source_section,
            context_sentence=self.original_text or self.description or self.notes,
            recorded_year=self.year,
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
