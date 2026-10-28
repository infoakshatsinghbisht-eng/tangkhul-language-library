"""Domain models and schema definitions for Tangkhul literature."""

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

VALID_LITERARY_GENRES = frozenset({
    "poem",
    "short_story",
    "folk_tale",
    "oral_narrative",
    "riddle",
    "proverb_collection",
    "play",
    "novel",
    "essay",
    "literary_anthology",
    "ballad",
    "children_literature",
    "translation",
    "other",
})

VALID_TEXT_AVAILABILITY = frozenset({
    "full_text",
    "excerpt",
    "metadata_only",
    "restricted",
})


@dataclass
class LiteraryRecord:
    """Represents a catalogued Tangkhul literary work, poem, folktale, play, or anthology."""

    id: str
    title: str
    work_type: str = "folk_tale"
    alternate_titles: list[str] = field(default_factory=list)
    original_title: str | None = None
    title_translation: str | None = None
    genres: list[str] = field(default_factory=list)
    author: str | None = None
    poet: str | None = None
    storyteller: str | None = None
    playwright: str | None = None
    translator: str | None = None
    editor: str | None = None
    collector: str | None = None
    contributor: str | None = None
    contributor_consent: bool = True
    publication_year: int | None = None
    composition_date: str | None = None
    edition: str | None = None
    publisher: str | None = None
    publication_place: str | None = None
    language: str = "Tangkhul"
    dialect: str | None = None
    village: str | None = None
    region: str | None = None
    collection: str | None = None
    anthology: str | None = None
    parent_work_id: str | None = None
    book_id: str | None = None
    isbn: str | None = None
    identifier: str | None = None
    source_url: str | None = None
    source_id: str | None = None
    source_title: str | None = None
    source_page: str | None = None
    source_section: str | None = None
    local_path: str | None = None
    license: str | None = None
    license_evidence: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    text_availability: str = "metadata_only"
    original_text: str | None = None
    translation_text: str | None = None
    summary: str | None = None
    stanza_count: int | None = None
    line_count: int | None = None
    related_authors: list[str] = field(default_factory=list)
    related_works: list[str] = field(default_factory=list)
    related_records: list[str] = field(default_factory=list)
    notes: str | None = None
    resource_type: str = "literature"

    def validate(self) -> None:
        """Validate integrity and schema constraints of the literary record."""
        if not self.id or not self.id.strip():
            raise ManifestValidationError("Literary record missing required field 'id'.")
        if not self.title or not self.title.strip():
            raise ManifestValidationError(
                f"Literary record '{self.id}' missing required field 'title'.",
                record_id=self.id,
            )
        if not self.work_type or not self.work_type.strip():
            raise ManifestValidationError(
                f"Literary record '{self.id}' missing required field 'work_type'.",
                record_id=self.id,
            )
        if self.work_type not in VALID_LITERARY_GENRES:
            raise ManifestValidationError(
                f"Literary record '{self.id}' has invalid work_type '{self.work_type}'. "
                f"Expected one of: {sorted(VALID_LITERARY_GENRES)}",
                record_id=self.id,
            )
        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Literary record '{self.id}' has invalid permission_status "
                f"'{self.permission_status}'.",
                record_id=self.id,
            )
        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Literary record '{self.id}' has invalid access_status "
                f"'{self.access_status}'.",
                record_id=self.id,
            )
        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Literary record '{self.id}' has invalid verification_status "
                f"'{self.verification_status}'.",
                record_id=self.id,
            )
        if (
            self.text_availability
            and self.text_availability not in VALID_TEXT_AVAILABILITY
        ):
            raise ManifestValidationError(
                f"Literary record '{self.id}' has invalid text_availability "
                f"'{self.text_availability}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert literary record to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LiteraryRecord:
        """Create LiteraryRecord from dictionary, handling manifest alias fields."""
        d = dict(data)

        # Handle work_type vs category vs genre alias
        if "category" in d and not d.get("work_type"):
            d["work_type"] = d.pop("category")
        elif "genre" in d and not d.get("work_type"):
            d["work_type"] = d.pop("genre")

        # Handle year -> publication_year
        if "year" in d and d.get("publication_year") is None:
            val = d.pop("year")
            if isinstance(val, int):
                d["publication_year"] = val
            elif isinstance(val, str) and val.isdigit():
                d["publication_year"] = int(val)

        # Handle creator -> author
        if "creator" in d and not d.get("author"):
            d["author"] = d.pop("creator")

        # Handle title_translation / translation_en
        if "translation_en" in d and not d.get("title_translation"):
            d["title_translation"] = d.pop("translation_en")

        # Handle source_identifier -> identifier
        if "source_identifier" in d and not d.get("identifier"):
            d["identifier"] = d.pop("source_identifier")

        # Filter fields matching dataclass
        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in d.items() if k in valid_fields}

        # Ensure list fields are lists
        for list_fld in (
            "alternate_titles",
            "genres",
            "related_authors",
            "related_works",
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
        creator = (
            self.author
            or self.poet
            or self.storyteller
            or self.playwright
            or self.contributor
        )
        return ManifestRecord(
            id=self.id,
            resource_type="literature",
            title=self.title,
            title_translation=self.title_translation,
            creator=creator,
            year=self.publication_year,
            publisher=self.publisher or self.source_title,
            language=self.language or "Tangkhul",
            dialect=self.dialect,
            source_url=self.source_url,
            source_identifier=self.identifier or self.source_id,
            license=self.license,
            permission_status=self.permission_status,
            local_path=self.local_path,
            verification_status=self.verification_status,
            notes=self.notes,
        )

    def to_manifest_dict(self) -> dict[str, Any]:
        """Convert to manifest-compliant JSONL dictionary."""
        creator = (
            self.author
            or self.poet
            or self.storyteller
            or self.playwright
            or self.contributor
        )
        return {
            "id": self.id,
            "resource_type": "literature",
            "title": self.title,
            "title_translation": self.title_translation,
            "creator": creator,
            "year": self.publication_year,
            "publisher": self.publisher or self.source_title,
            "language": self.language or "Tangkhul",
            "dialect": self.dialect,
            "category": self.work_type,
            "work_type": self.work_type,
            "author": self.author,
            "book_id": self.book_id,
            "source_url": self.source_url,
            "source_identifier": self.identifier or self.source_id,
            "license": self.license,
            "permission_status": self.permission_status,
            "access_status": self.access_status,
            "verification_status": self.verification_status,
            "local_path": self.local_path,
            "notes": self.notes,
        }

    def extract_vocabulary_candidates(self) -> list[dict[str, Any]]:
        """Extract candidate lexical words and phrases with exact source location.

        Preserves original orthography, macrons, and diacritics without destructive flattening.
        """
        if self.permission_status == "restricted" or self.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: literary record '{self.id}' has restricted status."
            )

        candidates: list[dict[str, Any]] = []

        # 1. Harvest from verbatim literary text if available
        if self.original_text:
            text_norm = normalize_unicode(self.original_text)
            words = re.findall(r"\b[A-Za-zāēīōūĀĒĪŌŪ'-]+\b", text_norm, re.UNICODE)
            for w in words:
                w_clean = w.strip("'-")
                if len(w_clean) > 1 and not w_clean.isdigit():
                    candidates.append({
                        "word_form": w_clean,
                        "source_id": self.id,
                        "context_sentence": self.original_text,
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "literary_text_extraction",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # 2. Harvest from original Tangkhul title
        source_title = self.original_title or self.title
        if source_title:
            t_norm = normalize_unicode(source_title)
            for part in re.findall(r"\b[A-Za-zāēīōūĀĒĪŌŪ'-]+\b", t_norm, re.UNICODE):
                clean_part = part.strip("'-")
                common_exclusions = {
                    "and", "the", "of", "in", "by", "for", "class", "tangkhul",
                    "kala", "wui", "li", "eili",
                }
                if (
                    len(clean_part) > 2
                    and not clean_part.isdigit()
                    and clean_part.lower() not in common_exclusions
                ):
                    candidates.append({
                        "word_form": clean_part,
                        "source_id": self.id,
                        "context_sentence": f"Title of literary work {self.id}: {self.title}",
                        "page_or_section": self.source_page or self.source_section,
                        "extraction_method": "literary_title_harvest",
                        "verification_status": self.verification_status,
                        "dialect": self.dialect,
                    })

        # Deduplicate candidates across word_form
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for c in candidates:
            w_norm = c["word_form"].lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(c)

        return deduped

    def to_vocabulary_entry(self, headword: str) -> VocabularyEntry:
        """Construct a new VocabularyEntry rooted in this literary work's provenance."""
        norm_headword = normalize_unicode(headword)
        meaning = self.title_translation or self.summary or self.title
        meanings = [meaning] if meaning else []

        prov = ProvenanceRecord(
            source_id=self.id,
            resource_type="literature",
            citation=f"Literary work {self.id}: {self.title} ({self.author or 'Traditional'})",
            page_or_section=self.source_page or self.source_section,
            context_sentence=self.original_text or self.summary or self.notes,
            recorded_year=self.publication_year,
            permission_status=self.permission_status,
        )

        return VocabularyEntry(
            id=f"VOCAB-{self.id}-{norm_headword.lower()}",
            headword=norm_headword,
            meanings=meanings,
            translations_en=meanings,
            dialect=self.dialect,
            example_sentences=[self.original_text] if self.original_text else [],
            verification_status="unverified",
            license_restrictions=self.license,
            provenance=[prov],
        )

    def extract_candidate_tokens(self, min_length: int = 2) -> list[str]:
        """Extract candidate lexical tokens from permitted literary text or title."""
        if self.permission_status == "restricted" or self.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: literary record '{self.id}' has restricted status."
            )
        candidates = self.extract_vocabulary_candidates()
        tokens = [
            c["word_form"].lower()
            for c in candidates
            if len(c["word_form"]) >= min_length
        ]
        return sorted(list(set(tokens)))

    def to_candidate_vocabulary_entries(
        self, min_length: int = 2
    ) -> list[VocabularyEntry]:
        """Convert extracted candidates into unverified candidate VocabularyEntry instances."""
        if self.permission_status == "restricted" or self.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: literary record '{self.id}' has restricted status."
            )
        tokens = self.extract_candidate_tokens(min_length=min_length)
        return [self.to_vocabulary_entry(t) for t in tokens]
