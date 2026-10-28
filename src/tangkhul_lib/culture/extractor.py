"""Permission-aware extraction of cultural knowledge, proverbs, and candidate vocabulary."""

from __future__ import annotations

import re
from typing import Any

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class CultureExtractor:
    """Extracts candidate vocabulary, proverbs, and sayings from authorized cultural records."""

    def __init__(self, allow_unverified: bool = True) -> None:
        self.allow_unverified = allow_unverified

    def check_permissions(self, record: CulturalRecord) -> bool:
        """Validate permission and consent controls before extracting text or vocabulary.

        Raises:
            PermissionDeniedError: If the record is restricted or lacks contributor consent.
        """
        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Record '{record.id}' is marked as restricted.",
                resource_id=record.id,
            )
        if record.access_status == "restricted":
            raise PermissionDeniedError(
                f"Extraction prohibited: Record '{record.id}' has restricted access status.",
                resource_id=record.id,
            )
        if not record.contributor_consent:
            raise PermissionDeniedError(
                f"Extraction prohibited: Contributor consent withheld for record '{record.id}'.",
                resource_id=record.id,
            )
        return True

    def extract_from_record(self, record: CulturalRecord) -> list[dict[str, Any]]:
        """Extract candidate lexical tokens and expressions from a single cultural record.

        Enforces strict permission gates. Preserves original Tangkhul orthography and provenance.
        """
        self.check_permissions(record)
        return record.extract_vocabulary_candidates()

    def extract_proverbs_from_text(
        self,
        text: str,
        source_id: str,
        permission_status: str = "permitted",
    ) -> list[dict[str, Any]]:
        """Parse structured Tangkhul proverb collections (Paotam/Chanjam) from text sources."""
        if permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot extract proverbs from restricted source '{source_id}'.",
                resource_id=source_id,
            )

        norm_text = normalize_unicode(text)
        proverbs: list[dict[str, Any]] = []

        for line in norm_text.splitlines():
            line_str = line.strip()
            if not line_str or line_str.endswith(":") or line_str.startswith("#"):
                continue

            sep_match = re.search(r"\s+[:—–=]\s+", line_str)
            if not sep_match:
                continue

            left_part = line_str[:sep_match.start()].strip()
            right_part = line_str[sep_match.end():].strip()

            orig_saying = re.sub(r"^(?:[-*]\s*|\d+[\.\)]\s*)", "", left_part).strip()
            meaning = right_part

            header_keywords = ("collection", "chapter", "section", "contents")
            if (
                len(orig_saying.split()) >= 2
                and len(meaning) >= 3
                and not any(h in orig_saying.lower() for h in header_keywords)
            ):
                proverbs.append({
                    "original_text": orig_saying,
                    "translation_en": meaning,
                    "source_id": source_id,
                    "category": "proverb",
                    "permission_status": permission_status,
                })

        return proverbs

    def harvest_candidate_vocabulary(
        self,
        records: list[CulturalRecord],
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

        # Deduplicate across entire harvested batch
        seen_words: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for cand in all_candidates:
            w_norm = normalize_unicode(cand["word_form"]).lower()
            if w_norm not in seen_words:
                seen_words.add(w_norm)
                deduped.append(cand)

        return deduped
