"""Book metadata models for the Tangkhul Language Library."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.core.models import (
    VALID_ACCESS_STATUSES,
    VALID_PERMISSION_STATUSES,
    VALID_VERIFICATION_STATUSES,
    ManifestRecord,
)


@dataclass
class BookRecord:
    """Comprehensive bibliographic metadata record for a Tangkhul book."""

    id: str
    title: str
    alternate_titles: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    editors: list[str] = field(default_factory=list)
    publisher: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    subject: str | None = None
    educational_level: str | None = None
    language: str = "Tangkhul"
    dialect: str | None = None
    isbn: str | None = None
    source_url: str | None = None
    source_identifier: str | None = None
    catalogue_url: str | None = None
    local_file_path: str | None = None
    file_format: str | None = None
    license: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None
    resource_type: str = "books"
    year: int | None = None

    def __post_init__(self) -> None:
        # Keep year and publication_year in sync
        if self.publication_year is not None and self.year is None:
            self.year = self.publication_year
        elif self.year is not None and self.publication_year is None:
            self.publication_year = self.year

    def validate(self) -> None:
        """Validate required fields and valid domain values.

        Raises:
            ManifestValidationError: If any required field is missing or invalid.
        """
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            raise ManifestValidationError("Book record ID must be a non-empty string.")

        if not self.title or not isinstance(self.title, str) or not self.title.strip():
            raise ManifestValidationError(
                f"Book '{self.id}' has missing or empty 'title'.",
                record_id=self.id,
            )

        if self.publication_year is not None and not isinstance(self.publication_year, int):
            raise ManifestValidationError(
                f"Book '{self.id}' publication_year must be an integer, got: "
                f"{type(self.publication_year).__name__}",
                record_id=self.id,
            )

        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Invalid permission_status '{self.permission_status}' for book '{self.id}'. "
                f"Expected one of: {sorted(VALID_PERMISSION_STATUSES)}",
                record_id=self.id,
            )

        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Invalid verification_status '{self.verification_status}' for book '{self.id}'. "
                f"Expected one of: {sorted(VALID_VERIFICATION_STATUSES)}",
                record_id=self.id,
            )

        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Invalid access_status '{self.access_status}' for book '{self.id}'. "
                f"Expected one of: {sorted(VALID_ACCESS_STATUSES)}",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert BookRecord to a dictionary containing only standard fields."""
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BookRecord:
        """Create a BookRecord instance from a dictionary, handling types cleanly."""
        data_copy = dict(data)

        # Normalize authors / editors / alternate_titles if given as strings
        if isinstance(data_copy.get("authors"), str):
            data_copy["authors"] = [a.strip() for a in data_copy["authors"].split(",") if a.strip()]
        if isinstance(data_copy.get("editors"), str):
            data_copy["editors"] = [e.strip() for e in data_copy["editors"].split(",") if e.strip()]
        if isinstance(data_copy.get("alternate_titles"), str):
            data_copy["alternate_titles"] = [
                t.strip() for t in data_copy["alternate_titles"].split(";") if t.strip()
            ]

        # Year conversion if string
        year_val = data_copy.get("publication_year") or data_copy.get("year")
        if year_val is not None and not isinstance(year_val, int):
            try:
                year_val = int(str(year_val).strip())
                data_copy["publication_year"] = year_val
                data_copy["year"] = year_val
            except (ValueError, TypeError):
                pass

        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data_copy.items() if k in valid_fields}
        record = cls(**filtered)
        record.validate()
        return record

    def to_manifest_record(self) -> ManifestRecord:
        """Convert to standard library ManifestRecord."""
        creator_str = None
        if self.authors:
            creator_str = ", ".join(self.authors)
        elif self.editors:
            creator_str = f"Ed. {', '.join(self.editors)}"

        return ManifestRecord(
            id=self.id,
            resource_type="books",
            title=self.title,
            title_translation=self.alternate_titles[0] if self.alternate_titles else None,
            creator=creator_str,
            year=self.publication_year,
            publisher=self.publisher,
            language=self.language,
            dialect=self.dialect,
            source_url=self.source_url,
            source_identifier=self.source_identifier,
            license=self.license,
            permission_status=self.permission_status,
            local_path=self.local_file_path,
            verification_status=self.verification_status,
            notes=self.notes,
        )
