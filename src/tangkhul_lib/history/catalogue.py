"""Catalogue management, chronological timeline, search, and exports for Tangkhul history."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import (
    ManifestValidationError,
    PermissionDeniedError,
    ResourceNotFoundError,
)
from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class HistoryCatalogue:
    """In-memory catalogue managing historical events, figures, places, and timelines."""

    def __init__(self, records: list[HistoricalRecord] | None = None) -> None:
        self._records: dict[str, HistoricalRecord] = {}
        if records:
            for rec in records:
                self.add_record(rec)

    def __len__(self) -> int:
        return len(self._records)

    @classmethod
    def load_from_manifest(cls, manifest_path: Path) -> HistoryCatalogue:
        """Instantiate HistoryCatalogue by loading records from a JSONL manifest file."""
        m_path = Path(manifest_path)
        records: list[HistoricalRecord] = []

        if m_path.is_file():
            with m_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if not line_str or line_str.startswith("#"):
                        continue
                    data = json.loads(line_str)
                    rec = HistoricalRecord.from_dict(data)
                    records.append(rec)

        return cls(records=records)

    def add_record(self, record: HistoricalRecord, allow_overwrite: bool = False) -> None:
        """Add a HistoricalRecord to the catalogue.

        Raises:
            ManifestValidationError: If validation fails or duplicate ID exists.
        """
        record.validate()
        if record.id in self._records and not allow_overwrite:
            raise ManifestValidationError(
                f"Historical record with ID '{record.id}' already exists in catalogue.",
                record_id=record.id,
            )
        self._records[record.id] = record

    def get_record(
        self, record_id: str, allow_restricted: bool = True
    ) -> HistoricalRecord | None:
        """Retrieve a historical record by its unique ID."""
        rec = self._records.get(record_id)
        if rec and not allow_restricted:
            if rec.permission_status == "restricted" or rec.access_status == "restricted":
                raise PermissionDeniedError(
                    f"Access to restricted historical record '{record_id}' is denied.",
                    resource_id=record_id,
                )
        return rec

    def list_records(self, sort_by_date: bool = False) -> list[HistoricalRecord]:
        """List all historical records sorted by ID or chronologically."""
        if sort_by_date:
            return sorted(
                self._records.values(),
                key=lambda r: (r.sort_year is None, r.sort_year or 0, r.id),
            )
        return sorted(self._records.values(), key=lambda r: r.id)

    def search_records(
        self,
        query: str | None = None,
        title: str | None = None,
        record_type: str | None = None,
        period: str | None = None,
        place: str | None = None,
        person: str | None = None,
        village: str | None = None,
        dialect: str | None = None,
        verification_status: str | None = None,
        include_restricted: bool = True,
    ) -> list[HistoricalRecord]:
        """Search and filter historical records across multiple fields with normalization."""
        results: list[HistoricalRecord] = []

        q_norm = normalize_unicode(query).lower() if query else None
        t_norm = normalize_unicode(title).lower() if title else None
        type_norm = record_type.strip().lower() if record_type else None
        per_norm = normalize_unicode(period).lower() if period else None
        plc_norm = normalize_unicode(place).lower() if place else None
        prs_norm = normalize_unicode(person).lower() if person else None
        vil_norm = normalize_unicode(village).lower() if village else None
        dial_norm = normalize_unicode(dialect).lower() if dialect else None
        ver_norm = verification_status.strip().lower() if verification_status else None

        for rec in self._records.values():
            if not include_restricted and (
                rec.permission_status == "restricted" or rec.access_status == "restricted"
            ):
                continue

            if type_norm and rec.record_type.lower() != type_norm:
                continue

            if ver_norm and rec.verification_status.lower() != ver_norm:
                continue

            if per_norm:
                rec_per = normalize_unicode(rec.period or "").lower()
                rec_date = normalize_unicode(rec.event_date or "").lower()
                if per_norm not in rec_per and per_norm not in rec_date:
                    continue

            if plc_norm:
                rec_plc = normalize_unicode(rec.place or "").lower()
                rec_vil = normalize_unicode(rec.village or "").lower()
                if plc_norm not in rec_plc and plc_norm not in rec_vil:
                    continue

            if vil_norm:
                rec_vil = normalize_unicode(rec.village or "").lower()
                rec_plc = normalize_unicode(rec.place or "").lower()
                rec_dial = normalize_unicode(rec.dialect or "").lower()
                if vil_norm not in rec_vil and vil_norm not in rec_plc and vil_norm not in rec_dial:
                    continue

            if prs_norm:
                people_text = " ".join(normalize_unicode(p).lower() for p in rec.people_involved)
                rec_title = normalize_unicode(rec.title).lower()
                if prs_norm not in people_text and prs_norm not in rec_title:
                    continue

            if dial_norm:
                rec_dial = normalize_unicode(rec.dialect or "").lower()
                if dial_norm not in rec_dial:
                    continue

            if t_norm:
                rec_title = normalize_unicode(rec.title).lower()
                rec_alts = " ".join(normalize_unicode(a).lower() for a in rec.alternate_titles)
                if t_norm not in rec_title and t_norm not in rec_alts:
                    continue

            if q_norm:
                searchable_text = " ".join([
                    rec.title,
                    " ".join(rec.alternate_titles),
                    rec.summary or "",
                    rec.description or "",
                    rec.original_text or "",
                    rec.translation_en or "",
                    rec.place or "",
                    rec.village or "",
                    rec.period or "",
                    rec.event_date or "",
                    " ".join(rec.people_involved),
                    rec.notes or "",
                    rec.source_title or "",
                    rec.source_id or "",
                ])
                if q_norm not in normalize_unicode(searchable_text).lower():
                    continue

            results.append(rec)

        return sorted(results, key=lambda r: r.id)

    def get_timeline(
        self,
        start_year: int | None = None,
        end_year: int | None = None,
        period: str | None = None,
        include_undated: bool = False,
    ) -> list[HistoricalRecord]:
        """Return historical events ordered chronologically by sort_year."""
        filtered: list[HistoricalRecord] = []
        p_norm = normalize_unicode(period).lower() if period else None

        for rec in self._records.values():
            if p_norm:
                rec_per = normalize_unicode(rec.period or "").lower()
                if p_norm not in rec_per:
                    continue

            if rec.sort_year is not None:
                if start_year is not None and rec.sort_year < start_year:
                    continue
                if end_year is not None and rec.sort_year > end_year:
                    continue
                filtered.append(rec)
            elif include_undated:
                filtered.append(rec)

        # Sort dated items by sort_year ascending, then undated items by ID
        return sorted(
            filtered,
            key=lambda r: (r.sort_year if r.sort_year is not None else 9999, r.id),
        )

    def get_related_records(self, record_id: str) -> list[HistoricalRecord]:
        """Return all catalogued historical records connected to the given record ID."""
        rec = self.get_record(record_id)
        if not rec:
            raise ResourceNotFoundError(f"Historical record '{record_id}' not found.")

        related_ids = set(rec.related_events + rec.related_records)
        results: list[HistoricalRecord] = []
        for rid in related_ids:
            target = self.get_record(rid)
            if target:
                results.append(target)

        return sorted(results, key=lambda r: r.id)

    def find_conflicts(self) -> list[dict[str, Any]]:
        """Detect contradictory dates, locations, or source interpretations across records."""
        grouped: dict[str, list[HistoricalRecord]] = defaultdict(list)

        for rec in self._records.values():
            # Group by normalized title base or place
            key = normalize_unicode(rec.title).lower().strip()
            # Clean common words for conceptual grouping
            for prefix in ("the ", "battle of ", "publication of "):
                if key.startswith(prefix):
                    key = key[len(prefix):].strip()
            grouped[key].append(rec)

        conflicts: list[dict[str, Any]] = []
        for key, group in grouped.items():
            if len(group) > 1:
                years = {r.sort_year for r in group if r.sort_year is not None}
                sources = {
                    r.source_id or r.source_title
                    for r in group
                    if r.source_id or r.source_title
                }
                places = {r.place for r in group if r.place}

                if len(years) > 1 or len(sources) > 1 or len(places) > 1:
                    conflicts.append({
                        "concept": key,
                        "record_ids": [r.id for r in group],
                        "years": sorted(list(years)),
                        "places": sorted(list(places)),
                        "sources": sorted(list(sources)),
                        "accounts": [r.summary or r.notes for r in group],
                    })

        return conflicts

    def get_history_report(self) -> dict[str, Any]:
        """Generate comprehensive status report of catalogued historical assets and evidence."""
        by_type: dict[str, int] = defaultdict(int)
        by_verification: dict[str, int] = defaultdict(int)
        by_period: dict[str, int] = defaultdict(int)
        restricted_count = 0
        primary_source_count = 0
        records_with_timeline = 0
        missing_source_metadata: list[str] = []

        for rec in self._records.values():
            by_type[rec.record_type] += 1
            by_verification[rec.verification_status] += 1
            if rec.period:
                by_period[rec.period] += 1

            if rec.permission_status == "restricted" or rec.access_status == "restricted":
                restricted_count += 1

            if rec.evidence_type in {"primary_source", "archival_record"}:
                primary_source_count += 1

            if rec.sort_year is not None:
                records_with_timeline += 1

            if not rec.source_id and not rec.source_url and not rec.source_title:
                missing_source_metadata.append(rec.id)

        return {
            "total_records": len(self._records),
            "by_type": dict(by_type),
            "by_verification": dict(by_verification),
            "by_period": dict(by_period),
            "verified_count": by_verification.get("verified", 0),
            "needs_review_count": by_verification.get("needs_review", 0),
            "restricted_count": restricted_count,
            "primary_source_count": primary_source_count,
            "records_with_timeline": records_with_timeline,
            "missing_source_metadata": missing_source_metadata,
        }

    def export_jsonl(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted historical records to a JSONL file."""
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
        """Export permitted historical records to a CSV file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "id",
            "title",
            "record_type",
            "event_date",
            "sort_year",
            "period",
            "place",
            "village",
            "dialect",
            "evidence_type",
            "source_id",
            "source_title",
            "source_url",
            "permission_status",
            "verification_status",
            "summary",
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

    def export_json(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted historical records to a JSON array file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        items = [
            rec.to_dict()
            for rec in self.list_records()
            if include_restricted
            or (
                rec.permission_status != "restricted"
                and rec.access_status != "restricted"
            )
        ]
        with path.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        return len(items)

    def find_duplicates(self) -> list[tuple[HistoricalRecord, HistoricalRecord]]:
        """Identify potential duplicate historical records by identical titles or sources."""
        duplicates: list[tuple[HistoricalRecord, HistoricalRecord]] = []
        records = list(self._records.values())
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                r1 = records[i]
                r2 = records[j]
                t1 = normalize_unicode(r1.title).strip().lower()
                t2 = normalize_unicode(r2.title).strip().lower()
                same_source = (
                    bool(r1.source_id)
                    and r1.source_id == r2.source_id
                    and bool(r1.source_page)
                    and r1.source_page == r2.source_page
                )
                if t1 == t2 or same_source:
                    duplicates.append((r1, r2))
        return duplicates
