"""Core domain models and schema definitions for Tangkhul Language Library."""

from __future__ import annotations

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
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
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

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["provenance"] = [p.to_dict() for p in self.provenance]
        return result
