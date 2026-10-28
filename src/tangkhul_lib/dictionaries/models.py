"""Domain models for Tangkhul dictionaries, glossaries, and lexical entries."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.core.models import (
    VALID_ACCESS_STATUSES,
    VALID_PERMISSION_STATUSES,
    VALID_VERIFICATION_STATUSES,
    ManifestRecord,
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.vocabulary.normalization import normalize_unicode

VALID_SOURCE_TYPES = frozenset({
    "dictionary",
    "bilingual_dictionary",
    "multilingual_dictionary",
    "glossary",
    "wordlist",
    "grammar_dictionary",
})


@dataclass
class DictionarySourceRecord:
    """Represents a verified or catalogued dictionary, glossary, or vocabulary source."""

    id: str
    title: str
    alternate_titles: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    editors: list[str] = field(default_factory=list)
    compiler: str | None = None
    contributors: list[str] = field(default_factory=list)
    publisher: str | None = None
    publication_place: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    languages: list[str] = field(default_factory=lambda: ["Tangkhul"])
    language_pair: str | None = None
    dialect: str | None = None
    source_type: str = "dictionary"
    isbn: str | None = None
    identifier: str | None = None
    source_url: str | None = None
    local_file_path: str | None = None
    license: str | None = None
    license_evidence: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None

    def validate(self) -> None:
        """Validate integrity and constraints of the dictionary source record."""
        if not self.id or not self.id.strip():
            raise ManifestValidationError("Dictionary record missing required field 'id'.")
        if not self.title or not self.title.strip():
            raise ManifestValidationError(
                f"Dictionary record '{self.id}' missing required field 'title'.",
                record_id=self.id,
            )
        if self.source_type not in VALID_SOURCE_TYPES:
            raise ManifestValidationError(
                f"Dictionary record '{self.id}' invalid source_type '{self.source_type}'. "
                f"Expected one of: {sorted(VALID_SOURCE_TYPES)}",
                record_id=self.id,
            )
        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Dictionary record '{self.id}' invalid permission '{self.permission_status}'.",
                record_id=self.id,
            )
        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Dictionary record '{self.id}' invalid access '{self.access_status}'.",
                record_id=self.id,
            )
        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Dictionary record '{self.id}' invalid status '{self.verification_status}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert source record to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DictionarySourceRecord:
        """Create DictionarySourceRecord from dictionary, handling alias fields."""
        d = dict(data)
        # Handle creator/author mappings from manifest format
        if "creator" in d and not d.get("authors") and not d.get("compiler"):
            creator_val = d.pop("creator")
            if creator_val:
                d["authors"] = [a.strip() for a in creator_val.split(",") if a.strip()]

        if "year" in d and "publication_year" not in d:
            d["publication_year"] = d.pop("year")

        if "source_identifier" in d and "identifier" not in d:
            d["identifier"] = d.pop("source_identifier")

        if "local_path" in d and "local_file_path" not in d:
            d["local_file_path"] = d.pop("local_path")

        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        return cls(**filtered)

    def to_manifest_record(self) -> ManifestRecord:
        """Convert to standard ManifestRecord format for JSON Lines persistence."""
        creator_str: str | None = None
        if self.compiler:
            creator_str = self.compiler
        elif self.authors:
            creator_str = ", ".join(self.authors)
        elif self.editors:
            creator_str = ", ".join(self.editors)

        return ManifestRecord(
            id=self.id,
            resource_type="dictionaries",
            title=self.title,
            title_translation=self.alternate_titles[0] if self.alternate_titles else None,
            creator=creator_str,
            year=self.publication_year,
            publisher=self.publisher,
            language=self.languages[0] if self.languages else "Tangkhul",
            dialect=self.dialect,
            source_url=self.source_url,
            source_identifier=self.identifier,
            license=self.license,
            permission_status=self.permission_status,
            local_path=self.local_file_path,
            verification_status=self.verification_status,
            notes=self.notes,
        )


@dataclass
class DictionaryEntryRecord:
    """Represents an individual entry/lemma extracted from an authentic dictionary source."""

    id: str
    dictionary_id: str
    headword: str
    normalized_headword: str | None = None
    alternate_spellings: list[str] = field(default_factory=list)
    transliteration: str | None = None
    definitions_en: list[str] = field(default_factory=list)
    definitions_hi: list[str] = field(default_factory=list)
    other_definitions: list[str] = field(default_factory=list)
    part_of_speech: str | None = None
    pronunciation: str | None = None
    notes: str | None = None
    examples: list[str] = field(default_factory=list)
    dialect: str | None = None
    grammatical_info: str | None = None
    page_or_section: str | None = None
    entry_number: str | None = None
    source_excerpt: str | None = None
    extraction_method: str = "manual_entry"
    confidence: float = 1.0
    license: str | None = None
    permission_status: str = "pending"
    verification_status: str = "unverified"
    vocabulary_id: str | None = None

    def __post_init__(self) -> None:
        if not self.normalized_headword and self.headword:
            self.normalized_headword = normalize_unicode(self.headword).strip().lower()

    def validate(self) -> None:
        """Validate integrity and required attributes of the entry record."""
        if not self.id or not self.id.strip():
            raise ManifestValidationError("Dictionary entry missing required field 'id'.")
        if not self.dictionary_id or not self.dictionary_id.strip():
            raise ManifestValidationError(
                f"Dictionary entry '{self.id}' missing required field 'dictionary_id'.",
                record_id=self.id,
            )
        if not self.headword or not self.headword.strip():
            raise ManifestValidationError(
                f"Dictionary entry '{self.id}' missing required field 'headword'.",
                record_id=self.id,
            )
        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Dictionary entry '{self.id}' invalid permission '{self.permission_status}'.",
                record_id=self.id,
            )
        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Dictionary entry '{self.id}' invalid status '{self.verification_status}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert entry record to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DictionaryEntryRecord:
        """Create DictionaryEntryRecord from dictionary."""
        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    def to_vocabulary_entry(self, citation: str | None = None) -> VocabularyEntry:
        """Construct a unified VocabularyEntry linked with a ProvenanceRecord."""
        vocab_id = self.vocabulary_id or f"VOCAB-{self.id}"
        combined_meanings: list[str] = []
        for m in self.definitions_en + self.other_definitions:
            if m and m not in combined_meanings:
                combined_meanings.append(m)

        cite_text = citation or f"Dictionary {self.dictionary_id}"
        if self.page_or_section:
            cite_text = f"{cite_text}, {self.page_or_section}"

        prov = ProvenanceRecord(
            source_id=self.dictionary_id,
            resource_type="dictionaries",
            citation=cite_text,
            page_or_section=self.page_or_section,
            context_sentence=self.examples[0] if self.examples else None,
            permission_status=self.permission_status,
        )

        return VocabularyEntry(
            id=vocab_id,
            headword=self.headword,
            meanings=combined_meanings,
            translations_en=list(self.definitions_en),
            alternative_spellings=list(self.alternate_spellings),
            dialect_variants=[],
            dialect=self.dialect,
            part_of_speech=self.part_of_speech,
            pronunciation=self.pronunciation,
            example_sentences=list(self.examples),
            provenance=[prov],
            verification_status=self.verification_status,
            license_restrictions=self.license,
        )
