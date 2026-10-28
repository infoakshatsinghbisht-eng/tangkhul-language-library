"""Song and musical metadata models for Tangkhul Language Library."""

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

VALID_SONG_TYPES = frozenset({
    "folk",
    "festival",
    "hymn",
    "modern",
    "ballad",
    "lament",
    "love_song",
    "lullaby",
    "ceremonial",
    "patriotic",
    "other",
})


@dataclass
class SongRecording:
    """Metadata describing an audio/video recording of an oral or musical performance."""

    recording_title: str
    source: str
    performer: str | None = None
    collector: str | None = None
    recording_date: str | None = None
    recording_year: int | None = None
    location: str | None = None
    village: str | None = None
    dialect: str | None = None
    duration_seconds: int | None = None
    media_format: str | None = None
    recording_url: str | None = None
    transcript_available: bool = False
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert recording metadata to dictionary."""
        return asdict(self)


@dataclass
class SongRecord:
    """Bibliographic, musical, and oral metadata record for a Tangkhul song."""

    id: str
    title: str
    alternate_titles: list[str] = field(default_factory=list)
    title_translation: str | None = None
    singer: str | None = None
    lyricist: str | None = None
    composer: str | None = None
    collector: str | None = None
    performers: list[str] = field(default_factory=list)
    year: int | None = None
    village: str | None = None
    dialect: str | None = None
    song_type: str | None = None
    language: str = "Tangkhul"
    source_url: str | None = None
    source_identifier: str | None = None
    recording_url: str | None = None
    lyrics_source_url: str | None = None
    local_file_path: str | None = None
    license: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None
    resource_type: str = "songs"

    def validate(self) -> None:
        """Validate required fields and schema constraints.

        Raises:
            ManifestValidationError: If any required field is missing or invalid.
        """
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            raise ManifestValidationError("Song record ID must be a non-empty string.")

        if not self.title or not isinstance(self.title, str) or not self.title.strip():
            raise ManifestValidationError(
                f"Song '{self.id}' has missing or empty 'title'.",
                record_id=self.id,
            )

        if self.year is not None and not isinstance(self.year, int):
            raise ManifestValidationError(
                f"Song '{self.id}' year must be an integer, got: {type(self.year).__name__}",
                record_id=self.id,
            )

        if self.permission_status not in VALID_PERMISSION_STATUSES:
            raise ManifestValidationError(
                f"Invalid permission_status '{self.permission_status}' for song '{self.id}'. "
                f"Expected one of: {sorted(VALID_PERMISSION_STATUSES)}",
                record_id=self.id,
            )

        if self.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ManifestValidationError(
                f"Invalid verification_status '{self.verification_status}' for song '{self.id}'. "
                f"Expected one of: {sorted(VALID_VERIFICATION_STATUSES)}",
                record_id=self.id,
            )

        if self.access_status not in VALID_ACCESS_STATUSES:
            raise ManifestValidationError(
                f"Invalid access_status '{self.access_status}' for song '{self.id}'. "
                f"Expected one of: {sorted(VALID_ACCESS_STATUSES)}",
                record_id=self.id,
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert SongRecord to a serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SongRecord:
        """Instantiate a SongRecord from dictionary with type cleanup."""
        data_copy = dict(data)

        # Normalize list fields if passed as delimited strings
        if isinstance(data_copy.get("alternate_titles"), str):
            data_copy["alternate_titles"] = [
                t.strip() for t in data_copy["alternate_titles"].split(";") if t.strip()
            ]
        if isinstance(data_copy.get("performers"), str):
            data_copy["performers"] = [
                p.strip() for p in data_copy["performers"].split(",") if p.strip()
            ]

        # Year conversion
        year_val = data_copy.get("year")
        if year_val is not None and not isinstance(year_val, int):
            try:
                data_copy["year"] = int(str(year_val).strip())
            except (ValueError, TypeError):
                pass

        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data_copy.items() if k in valid_fields}
        record = cls(**filtered)
        record.validate()
        return record

    def to_manifest_record(self) -> ManifestRecord:
        """Convert to standard library ManifestRecord."""
        creator_parts: list[str] = []
        if self.singer:
            creator_parts.append(self.singer)
        if self.lyricist and self.lyricist != self.singer:
            creator_parts.append(f"Lyrics: {self.lyricist}")
        if self.composer and self.composer != self.singer:
            creator_parts.append(f"Comp: {self.composer}")
        if self.collector:
            creator_parts.append(f"Coll: {self.collector}")

        creator_str = ", ".join(creator_parts) if creator_parts else None

        return ManifestRecord(
            id=self.id,
            resource_type="songs",
            title=self.title,
            title_translation=self.title_translation,
            creator=creator_str,
            year=self.year,
            publisher=None,
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
