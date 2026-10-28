"""Exception hierarchy for Tangkhul Language Library."""

from __future__ import annotations


class TangkhulLibError(Exception):
    """Base exception for all errors raised by the Tangkhul Language Library."""


class ConfigurationError(TangkhulLibError):
    """Raised when there is an issue with library or environment configuration."""


class ManifestValidationError(TangkhulLibError):
    """Raised when a manifest record fails schema or data validation."""

    def __init__(self, message: str, record_id: str | None = None, line_number: int | None = None):
        super().__init__(message)
        self.record_id = record_id
        self.line_number = line_number


class ResourceNotFoundError(TangkhulLibError):
    """Raised when a requested resource or manifest cannot be located."""


class ProvenanceError(TangkhulLibError):
    """Raised when an entry lacks required provenance or attribution metadata."""


class DeduplicationError(TangkhulLibError):
    """Raised when deduplication would result in loss of distinct meaning or provenance."""


class PermissionRestrictedError(TangkhulLibError):
    """Raised when access, extraction, or processing is restricted by permissions."""

    def __init__(
        self,
        message: str,
        record_id: str | None = None,
        permission_status: str | None = None,
        resource_id: str | None = None,
    ):
        super().__init__(message)
        self.record_id = record_id or resource_id
        self.resource_id = self.record_id
        self.permission_status = permission_status


PermissionDeniedError = PermissionRestrictedError

class ExtractionError(TangkhulLibError):
    """Raised when text or token extraction fails on a document."""
