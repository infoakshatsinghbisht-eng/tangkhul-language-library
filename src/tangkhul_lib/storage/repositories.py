"""Repository abstractions for vocabulary, provenance, and manifests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tangkhul_lib.core.models import ManifestRecord, VocabularyEntry
    from tangkhul_lib.storage.database import DatabaseManager


class VocabularyRepository:
    """Repository pattern interface for storing and retrieving vocabulary entries."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, entry: VocabularyEntry) -> None:
        """Persist a vocabulary entry with provenance."""
        raise NotImplementedError("Vocabulary persistence is not yet operational in Step 1.")

    def get_by_id(self, entry_id: str) -> VocabularyEntry | None:
        """Fetch an entry by unique identifier."""
        raise NotImplementedError("Vocabulary persistence is not yet operational in Step 1.")


class ManifestRepository:
    """Repository interface for querying catalogued manifests."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, record: ManifestRecord) -> None:
        """Store a manifest record."""
        raise NotImplementedError("Manifest persistence is not yet operational in Step 1.")

    def list_by_type(self, resource_type: str) -> list[ManifestRecord]:
        """List manifests filtered by resource type."""
        raise NotImplementedError("Manifest persistence is not yet operational in Step 1.")
