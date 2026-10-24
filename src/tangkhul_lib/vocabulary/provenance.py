"""Provenance tracking interfaces and attribution helpers."""

from __future__ import annotations

from tangkhul_lib.core.exceptions import ProvenanceError
from tangkhul_lib.core.models import ProvenanceRecord


def create_provenance_record(
    source_id: str,
    resource_type: str,
    citation: str,
    page_or_section: str | None = None,
    context_sentence: str | None = None,
    recorded_year: int | None = None,
    permission_status: str = "pending",
) -> ProvenanceRecord:
    """Create and validate a new ProvenanceRecord.

    Raises:
        ProvenanceError: If required identification or citation is missing.
    """
    if not source_id or not source_id.strip():
        raise ProvenanceError("Provenance record requires a non-empty source_id.")
    if not citation or not citation.strip():
        raise ProvenanceError("Provenance record requires a non-empty citation.")

    return ProvenanceRecord(
        source_id=source_id.strip(),
        resource_type=resource_type.strip(),
        citation=citation.strip(),
        page_or_section=page_or_section.strip() if page_or_section else None,
        context_sentence=context_sentence.strip() if context_sentence else None,
        recorded_year=recorded_year,
        permission_status=permission_status,
    )
