"""Permission-aware extraction of historical vocabulary, toponyms, and event entities."""

from __future__ import annotations

import re
from typing import Any

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class HistoryExtractor:
    """Extracts candidate historical vocabulary, toponyms, and entity terms from sources."""

    def __init__(self, allow_unverified: bool = True) -> None:
        self.allow_unverified = allow_unverified

    def check_permissions(self, record: HistoricalRecord) -> bool:
        """Validate permission and consent controls before extracting historical data.

        Raises:
            PermissionDeniedError: If the record is restricted or lacks contributor consent.
        """
        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Historical record '{record.id}' is restricted.",
                resource_id=record.id,
            )
        if record.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Record '{record.id}' has restricted access status.",
                resource_id=record.id,
            )
        if not record.contributor_consent:
            raise PermissionDeniedError(
                f"Consent not granted for extraction from record '{record.id}'.",
                resource_id=record.id,
            )
        return True

    def extract_from_record(self, record: HistoricalRecord) -> list[dict[str, Any]]:
        """Extract candidate historical tokens and toponyms from a single record."""
        self.check_permissions(record)
        return record.extract_vocabulary_candidates()

    def harvest_candidate_vocabulary(
        self,
        records: list[HistoricalRecord],
        skip_restricted: bool = True,
    ) -> list[dict[str, Any]]:
        """Extract candidate vocabulary from multiple records, skipping restricted items."""
        all_candidates: list[dict[str, Any]] = []

        for rec in records:
            if rec.permission_status == "restricted" or not rec.contributor_consent:
                if skip_restricted:
                    continue
                raise PermissionDeniedError(
                    f"Restricted record '{rec.id}' encountered during candidate harvesting.",
                    resource_id=rec.id,
                )

            extracted = self.extract_from_record(rec)
            all_candidates.extend(extracted)

        # Deduplicate across entire batch
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for cand in all_candidates:
            w_norm = normalize_unicode(cand["word_form"]).lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(cand)

        return deduped

    def extract_toponyms(
        self,
        text: str,
        source_id: str,
        permission_status: str = "permitted",
    ) -> list[dict[str, Any]]:
        """Extract historical place names, peaks, and settlements from text sources."""
        if permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot extract toponyms from restricted source '{source_id}'.",
                resource_id=source_id,
            )

        norm_text = normalize_unicode(text)
        toponyms: list[dict[str, Any]] = []

        # Match toponym patterns like: "Village: X", "Peak: Y", or capitalized settlement names
        pattern = re.compile(
            r"\b([A-Z][a-zāēīōū]+(?:\s+[A-Z][a-zāēīōū]+)?)\s+(?:Village|Peak|Ridge|Plateau|River|Hill)\b",
            re.UNICODE,
        )

        for match in pattern.finditer(norm_text):
            place_name = match.group(1).strip()
            full_match = match.group(0).strip()
            toponyms.append({
                "word_form": place_name,
                "context_sentence": full_match,
                "source_id": source_id,
                "extraction_method": "toponym_extraction",
                "verification_status": "unverified",
            })

        return toponyms
