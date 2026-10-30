"""Article metadata models for Tangkhul Language Library."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.core.models import (
    VALID_ACCESS_STATUSES,
    VALID_PERMISSION_STATUSES,
    VALID_VERIFICATION_STATUSES,
)


@dataclass
class ArticleRecord:
    """Bibliographic metadata record for a research or cultural article."""

    id: str
    title: str
    alternate_titles: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    journal: str | None = None
    volume_issue: str | None = None
    publication_year: int | None = None
    year: int | None = None
    publisher: str | None = None
    subject: str = "Linguistics"
    keywords: list[str] = field(default_factory=list)
    abstract: str = ""
    language: str = "Tangkhul & English"
    doi_url: str | None = None
    source_url: str | None = None
    source_identifier: str | None = None
    catalogue_url: str | None = None
    local_file_path: str | None = None
    file_format: str = "txt"
    license: str | None = None
    permission_status: str = "permitted"
    access_status: str = "full_text_available"
    verification_status: str = "verified"
    notes: str | None = None
    resource_type: str = "literature"
    work_type: str = "essay"

    def __post_init__(self) -> None:
        if self.publication_year is not None and self.year is None:
            self.year = self.publication_year
        elif self.year is not None and self.publication_year is None:
            self.publication_year = self.year

    def validate(self) -> None:
        """Validate required fields.

        Raises:
            ManifestValidationError: If any required field is invalid.
        """
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            raise ManifestValidationError("Article record ID must be a non-empty string.")

        if not self.title or not isinstance(self.title, str) or not self.title.strip():
            raise ManifestValidationError(
                f"Article '{self.id}' has missing or empty 'title'.",
                record_id=self.id,
            )

        if self.publication_year is not None and not isinstance(self.publication_year, int):
            raise ManifestValidationError(
                f"Article '{self.id}' publication_year must be an integer.",
                record_id=self.id,
            )

        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Invalid permission_status '{self.permission_status}' for article '{self.id}'.",
                record_id=self.id,
            )

        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Invalid verification_status '{self.verification_status}' for article '{self.id}'.",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArticleRecord:
        """Construct record from dictionary."""
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

