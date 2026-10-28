"""Permission-aware extraction of literary text segments, stanzas, and vocabulary."""

from __future__ import annotations

import re
from typing import Any

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class LiteratureExtractor:
    """Extracts candidate vocabulary, poetic stanzas, and text segments from literary sources."""

    def __init__(self, allow_unverified: bool = True) -> None:
        self.allow_unverified = allow_unverified

    def check_permissions(self, record: LiteraryRecord) -> bool:
        """Validate permission and consent controls before extracting literary data.

        Raises:
            PermissionDeniedError: If the record is restricted or lacks contributor consent.
        """
        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Literary work '{record.id}' is restricted.",
                resource_id=record.id,
            )
        if record.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Literary work '{record.id}' has restricted access.",
                resource_id=record.id,
            )
        if not record.contributor_consent:
            raise PermissionDeniedError(
                f"Consent not granted for extraction from literary work '{record.id}'.",
                resource_id=record.id,
            )
        return True

    def extract_from_record(self, record: LiteraryRecord) -> list[dict[str, Any]]:
        """Extract candidate literary tokens from a single record with permission checks."""
        self.check_permissions(record)
        return record.extract_vocabulary_candidates()

    def harvest_candidate_vocabulary(
        self,
        records: list[LiteraryRecord],
        skip_restricted: bool = True,
    ) -> list[dict[str, Any]]:
        """Extract candidate vocabulary from multiple literary works, handling restricted items."""
        all_candidates: list[dict[str, Any]] = []

        for rec in records:
            if rec.permission_status == "restricted" or not rec.contributor_consent:
                if skip_restricted:
                    continue
                raise PermissionDeniedError(
                    f"Restricted work '{rec.id}' encountered during candidate harvesting.",
                    resource_id=rec.id,
                )

            extracted = self.extract_from_record(rec)
            all_candidates.extend(extracted)

        # Deduplicate across entire batch by lowercase NFC
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for cand in all_candidates:
            w_norm = normalize_unicode(cand["word_form"]).lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(cand)

        return deduped

    def extract_stanzas_and_lines(
        self,
        text: str,
        source_id: str,
        permission_status: str = "permitted",
    ) -> list[dict[str, Any]]:
        """Extract stanzas and numbered lines from poetic texts or ballads.

        Raises:
            PermissionDeniedError: If the source is restricted.
        """
        if permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot extract stanzas from restricted source '{source_id}'.",
                resource_id=source_id,
            )

        norm_text = normalize_unicode(text)
        raw_stanzas = re.split(r"\n\s*\n", norm_text.strip())
        structured_lines: list[dict[str, Any]] = []

        overall_line_index = 1
        for s_idx, stanza_text in enumerate(raw_stanzas, start=1):
            lines = stanza_text.strip().splitlines()
            for l_idx, line in enumerate(lines, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                words = re.findall(r"\b[A-Za-zāēīōūĀĒĪŌŪ'-]+\b", clean_line, re.UNICODE)
                structured_lines.append({
                    "source_id": source_id,
                    "stanza_number": s_idx,
                    "line_in_stanza": l_idx,
                    "overall_line": overall_line_index,
                    "line_text": clean_line,
                    "word_count": len(words),
                    "extraction_method": "stanza_line_parsing",
                })
                overall_line_index += 1

        return structured_lines
