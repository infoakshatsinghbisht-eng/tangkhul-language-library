"""Catalogue management, search, duplicate detection, and exports for Tangkhul culture."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError, ResourceNotFoundError
from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class CultureCatalogue:
    """In-memory catalogue managing cultural records, proverbs, festivals, and customs."""

    def __init__(self, records: list[CulturalRecord] | None = None) -> None:
        self._records: dict[str, CulturalRecord] = {}
        if records:
            for rec in records:
                self.add_record(rec)

    def __len__(self) -> int:
        return len(self._records)

    @classmethod
    def load_from_manifest(cls, manifest_path: Path) -> CultureCatalogue:
        """Instantiate CultureCatalogue by loading records from a JSONL manifest file."""
        m_path = Path(manifest_path)
        records: list[CulturalRecord] = []

        if m_path.is_file():
            with m_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if not line_str or line_str.startswith("#"):
                        continue
                    data = json.loads(line_str)
                    rec = CulturalRecord.from_dict(data)
                    records.append(rec)

        return cls(records=records)

    def add_record(self, record: CulturalRecord, allow_overwrite: bool = False) -> None:
        """Add a CulturalRecord to the catalogue.

        Raises:
            ManifestValidationError: If validation fails or duplicate ID exists.
        """
        record.validate()
        if record.id in self._records and not allow_overwrite:
            raise ManifestValidationError(
                f"Cultural record with ID '{record.id}' already exists in catalogue.",
                record_id=record.id,
            )
        self._records[record.id] = record

    def get_record(self, record_id: str) -> CulturalRecord | None:
        """Retrieve a cultural record by unique ID."""
        return self._records.get(record_id)

    def list_records(self) -> list[CulturalRecord]:
        """List all cultural records sorted by ID."""
        return sorted(self._records.values(), key=lambda r: r.id)

    def search_records(
        self,
        query: str | None = None,
        title: str | None = None,
        local_name: str | None = None,
        category: str | None = None,
        village: str | None = None,
        dialect: str | None = None,
        occasion: str | None = None,
        source: str | None = None,
        contributor: str | None = None,
        verification_status: str | None = None,
        include_restricted: bool = True,
    ) -> list[CulturalRecord]:
        """Search and filter cultural records across multiple fields with normalization."""
        results: list[CulturalRecord] = []

        q_norm = normalize_unicode(query).lower() if query else None
        t_norm = normalize_unicode(title).lower() if title else None
        l_norm = normalize_unicode(local_name).lower() if local_name else None
        cat_norm = category.strip().lower() if category else None
        vil_norm = normalize_unicode(village).lower() if village else None
        dial_norm = normalize_unicode(dialect).lower() if dialect else None
        occ_norm = normalize_unicode(occasion).lower() if occasion else None
        src_norm = normalize_unicode(source).lower() if source else None
        contrib_norm = normalize_unicode(contributor).lower() if contributor else None
        ver_norm = verification_status.strip().lower() if verification_status else None

        for rec in self._records.values():
            if not include_restricted and (
                rec.permission_status == "restricted" or rec.access_status == "restricted"
            ):
                continue

            if cat_norm and rec.category.lower() != cat_norm:
                continue

            if ver_norm and rec.verification_status.lower() != ver_norm:
                continue

            if vil_norm:
                rec_vil = normalize_unicode(rec.village or "").lower()
                rec_dial = normalize_unicode(rec.dialect or "").lower()
                if vil_norm not in rec_vil and vil_norm not in rec_dial:
                    continue

            if dial_norm:
                rec_dial = normalize_unicode(rec.dialect or "").lower()
                if dial_norm not in rec_dial:
                    continue

            if occ_norm:
                rec_occ = normalize_unicode(rec.season_or_timing or "").lower()
                if occ_norm not in rec_occ:
                    continue

            if src_norm:
                rec_src = " ".join([
                    rec.source_id or "",
                    rec.source_title or "",
                    rec.source_url or "",
                ])
                if src_norm not in normalize_unicode(rec_src).lower():
                    continue

            if contrib_norm:
                rec_contrib = normalize_unicode(rec.contributor or "").lower()
                if contrib_norm not in rec_contrib:
                    continue

            if t_norm:
                rec_title = normalize_unicode(rec.title).lower()
                rec_alts = " ".join(normalize_unicode(a).lower() for a in rec.alternate_names)
                if t_norm not in rec_title and t_norm not in rec_alts:
                    continue

            if l_norm:
                rec_local = normalize_unicode(rec.local_name or "").lower()
                if l_norm not in rec_local:
                    continue

            if q_norm:
                searchable_text = " ".join([
                    rec.title,
                    rec.local_name or "",
                    " ".join(rec.alternate_names),
                    rec.original_text or "",
                    rec.translation_en or "",
                    rec.description or "",
                    rec.cultural_significance or "",
                    rec.notes or "",
                    rec.category,
                    rec.village or "",
                    rec.dialect or "",
                ])
                if q_norm not in normalize_unicode(searchable_text).lower():
                    continue

            results.append(rec)

        return sorted(results, key=lambda r: r.id)

    def find_likely_duplicates(self) -> list[tuple[CulturalRecord, CulturalRecord, str]]:
        """Identify potential duplicate cultural records without collapsing regional variants.

        Returns pairs of records that share identical names and categories within the same
        village/community, distinguishing them from valid regional variants across villages.
        """
        duplicates: list[tuple[CulturalRecord, CulturalRecord, str]] = []
        records_list = list(self._records.values())

        for i in range(len(records_list)):
            for j in range(i + 1, len(records_list)):
                r1 = records_list[i]
                r2 = records_list[j]

                if r1.id == r2.id:
                    continue

                # Same category comparison
                if r1.category == r2.category:
                    # Compare normalized titles
                    t1 = normalize_unicode(r1.title).lower()
                    t2 = normalize_unicode(r2.title).lower()

                    v1 = normalize_unicode(r1.village or "").lower()
                    v2 = normalize_unicode(r2.village or "").lower()

                    if t1 == t2 and v1 == v2:
                        reason = (
                            f"Identical title '{r1.title}' and category '{r1.category}' "
                            f"in same village '{r1.village or 'unspecified'}'"
                        )
                        duplicates.append((r1, r2, reason))
                    elif r1.local_name and r2.local_name:
                        l1 = normalize_unicode(r1.local_name).lower()
                        l2 = normalize_unicode(r2.local_name).lower()
                        if l1 == l2 and v1 == v2:
                            reason = (
                                f"Identical local name '{r1.local_name}' in "
                                f"'{r1.village or 'unspecified'}'"
                            )
                            duplicates.append((r1, r2, reason))

        return duplicates

    def find_conflicts(self) -> list[dict[str, Any]]:
        """Detect differing interpretations or descriptions across sources for cultural concepts."""
        grouped: dict[str, list[CulturalRecord]] = defaultdict(list)

        for rec in self._records.values():
            key = normalize_unicode(rec.local_name or rec.title).lower().strip()
            # Clean common prefixes/suffixes for grouping
            key = key.replace("proverb on ", "").replace("festival", "").strip()
            grouped[key].append(rec)

        conflicts: list[dict[str, Any]] = []
        for key, group in grouped.items():
            if len(group) > 1:
                sources = {
                    r.source_id or r.source_title
                    for r in group
                    if r.source_id or r.source_title
                }
                villages = {r.village for r in group if r.village}
                if len(sources) > 1 or len(villages) > 1:
                    conflicts.append({
                        "concept": key,
                        "record_ids": [r.id for r in group],
                        "sources": list(sources),
                        "villages": list(villages),
                        "descriptions": [r.description or r.notes for r in group],
                        "interpretation_count": len(group),
                    })

        return conflicts

    def link_related_records(self, record_id: str, related_id: str) -> None:
        """Establish a bidirectional relationship between two cultural or corpus records."""
        rec = self.get_record(record_id)
        if not rec:
            raise ResourceNotFoundError(f"Record '{record_id}' not found in catalogue.")

        if related_id not in rec.related_records:
            rec.related_records.append(related_id)

        # If related_id is also a cultural record, link reciprocally
        target = self.get_record(related_id)
        if target and record_id not in target.related_records:
            target.related_records.append(record_id)

    def get_culture_report(self) -> dict[str, Any]:
        """Generate comprehensive status report of verified, pending, and sensitive records."""
        by_category: dict[str, int] = defaultdict(int)
        by_verification: dict[str, int] = defaultdict(int)
        restricted_count = 0
        records_with_original_text = 0
        records_with_translation = 0
        missing_source_metadata: list[str] = []

        for rec in self._records.values():
            by_category[rec.category] += 1
            by_verification[rec.verification_status] += 1

            if rec.permission_status == "restricted" or rec.access_status == "restricted":
                restricted_count += 1

            if rec.original_text:
                records_with_original_text += 1

            if rec.translation_en or rec.translations_other:
                records_with_translation += 1

            if not rec.source_id and not rec.source_url and not rec.source_title:
                missing_source_metadata.append(rec.id)

        return {
            "total_records": len(self._records),
            "by_category": dict(by_category),
            "by_verification": dict(by_verification),
            "verified_count": by_verification.get("verified", 0),
            "needs_review_count": by_verification.get("needs_review", 0),
            "restricted_count": restricted_count,
            "records_with_original_text": records_with_original_text,
            "records_with_translation": records_with_translation,
            "missing_source_metadata": missing_source_metadata,
        }

    def export_jsonl(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted cultural records to a JSONL file.

        Restricted records are omitted unless explicitly included.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0

        with path.open("w", encoding="utf-8") as f:
            for rec in self.list_records():
                if not include_restricted and (
                    rec.permission_status == "restricted"
                    or rec.access_status == "restricted"
                ):
                    continue
                f.write(json.dumps(rec.to_dict(), ensure_ascii=False) + "\n")
                count += 1

        return count

    def export_csv(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted cultural records to a CSV file.

        Restricted records are omitted unless explicitly requested.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "id",
            "title",
            "local_name",
            "category",
            "subcategory",
            "original_text",
            "translation_en",
            "village",
            "dialect",
            "year",
            "source_id",
            "source_title",
            "source_url",
            "permission_status",
            "verification_status",
            "notes",
        ]

        count = 0
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()

            for rec in self.list_records():
                if not include_restricted and (
                    rec.permission_status == "restricted"
                    or rec.access_status == "restricted"
                ):
                    continue
                writer.writerow(rec.to_dict())
                count += 1

        return count
