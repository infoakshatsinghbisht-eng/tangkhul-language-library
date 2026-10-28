"""Catalogue management, search, and export operations for Tangkhul literature."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import (
    ManifestValidationError,
    PermissionDeniedError,
    ResourceNotFoundError,
)
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class LiteratureCatalogue:
    """In-memory catalogue managing literary works, folktales, poems, plays, and anthologies."""

    def __init__(self, records: list[LiteraryRecord] | None = None) -> None:
        self._records: dict[str, LiteraryRecord] = {}
        if records:
            for rec in records:
                self.add_work(rec)

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self):
        return iter(self._records.values())

    def add_work(self, record: LiteraryRecord, allow_overwrite: bool = False) -> None:
        """Add a LiteraryRecord to the catalogue.

        Raises:
            ManifestValidationError: If validation fails or duplicate ID exists.
        """
        record.validate()
        if record.id in self._records and not allow_overwrite:
            raise ManifestValidationError(
                f"Literary work with ID '{record.id}' already exists in catalogue.",
                record_id=record.id,
            )
        self._records[record.id] = record

    def get_work(
        self, work_id: str, allow_restricted: bool = True
    ) -> LiteraryRecord | None:
        """Retrieve a literary work by unique ID.

        Raises:
            PermissionDeniedError: If allow_restricted is False and the work is restricted.
        """
        rec = self._records.get(work_id)
        if rec and not allow_restricted:
            if rec.permission_status == "restricted" or rec.access_status == "restricted":
                raise PermissionDeniedError(
                    f"Access to restricted literary work '{work_id}' is denied.",
                    resource_id=work_id,
                )
        return rec

    def list_works(self, sort_by_year: bool = False) -> list[LiteraryRecord]:
        """List all literary works, sorted by ID or chronologically by year."""
        if sort_by_year:
            return sorted(
                self._records.values(),
                key=lambda r: (
                    r.publication_year is None,
                    r.publication_year or 0,
                    r.id,
                ),
            )
        return sorted(self._records.values(), key=lambda r: r.id)

    def search_works(
        self,
        query: str | None = None,
        title: str | None = None,
        author: str | None = None,
        translator: str | None = None,
        work_type: str | None = None,
        genre: str | None = None,
        language: str | None = None,
        dialect: str | None = None,
        village: str | None = None,
        access_status: str | None = None,
        verification_status: str | None = None,
        include_restricted: bool = True,
    ) -> list[LiteraryRecord]:
        """Search and filter literary works across multiple dimensions."""
        results: list[LiteraryRecord] = []

        q_norm = normalize_unicode(query).lower() if query else None
        t_norm = normalize_unicode(title).lower() if title else None
        a_norm = normalize_unicode(author).lower() if author else None
        tr_norm = normalize_unicode(translator).lower() if translator else None
        type_target = (work_type or genre or "").strip().lower()
        l_norm = language.strip().lower() if language else None
        d_norm = normalize_unicode(dialect).lower() if dialect else None
        v_norm = normalize_unicode(village).lower() if village else None
        acc_norm = access_status.strip().lower() if access_status else None
        ver_norm = verification_status.strip().lower() if verification_status else None

        for rec in self._records.values():
            if not include_restricted and (
                rec.permission_status == "restricted" or rec.access_status == "restricted"
            ):
                continue

            if type_target:
                matches_type = rec.work_type.lower() == type_target
                matches_genre = any(g.lower() == type_target for g in rec.genres)
                if not (matches_type or matches_genre):
                    continue

            if ver_norm and rec.verification_status.lower() != ver_norm:
                continue

            if acc_norm and rec.access_status.lower() != acc_norm:
                continue

            if l_norm and (rec.language or "").lower() != l_norm:
                continue

            if d_norm:
                rec_d = normalize_unicode(rec.dialect or "").lower()
                if d_norm not in rec_d:
                    continue

            if v_norm:
                rec_v = normalize_unicode(rec.village or "").lower()
                rec_r = normalize_unicode(rec.region or "").lower()
                if v_norm not in rec_v and v_norm not in rec_r:
                    continue

            if a_norm:
                creator_fields = [
                    rec.author,
                    rec.poet,
                    rec.storyteller,
                    rec.playwright,
                    rec.editor,
                    rec.collector,
                    rec.contributor,
                ]
                creator_text = " ".join(
                    normalize_unicode(c).lower() for c in creator_fields if c
                )
                if a_norm not in creator_text:
                    continue

            if tr_norm:
                rec_tr = normalize_unicode(rec.translator or "").lower()
                if tr_norm not in rec_tr:
                    continue

            if t_norm:
                titles = [rec.title, rec.original_title, rec.title_translation]
                titles.extend(rec.alternate_titles)
                title_text = " ".join(
                    normalize_unicode(t).lower() for t in titles if t
                )
                if t_norm not in title_text:
                    continue

            if q_norm:
                corpus_parts = [
                    rec.title,
                    rec.original_title,
                    rec.title_translation,
                    rec.author,
                    rec.poet,
                    rec.storyteller,
                    rec.playwright,
                    rec.translator,
                    rec.summary,
                    rec.original_text,
                    rec.translation_text,
                    rec.collection,
                    rec.anthology,
                    rec.notes,
                ]
                corpus_parts.extend(rec.alternate_titles)
                corpus_parts.extend(rec.genres)
                corpus_text = " ".join(
                    normalize_unicode(p).lower() for p in corpus_parts if p
                )
                if q_norm not in corpus_text:
                    continue

            results.append(rec)

        return sorted(results, key=lambda r: r.id)

    def get_works_by_genre(self, genre: str) -> list[LiteraryRecord]:
        """Return all works matching a given literary genre."""
        return self.search_works(genre=genre)

    def get_works_by_author(self, author: str) -> list[LiteraryRecord]:
        """Return all works attributed to an author, poet, or storyteller."""
        return self.search_works(author=author)

    def get_works_by_book_id(self, book_id: str) -> list[LiteraryRecord]:
        """Return all literary works linked to a specific book ID in the Books module."""
        return [
            r for r in self._records.values()
            if r.book_id and r.book_id.strip() == book_id.strip()
        ]

    def get_related_works(self, work_id: str | LiteraryRecord) -> list[LiteraryRecord]:
        """Return all works connected to the given work or work ID via relationships."""
        if isinstance(work_id, LiteraryRecord):
            rec = work_id
        else:
            rec = self.get_work(work_id)
            if not rec:
                raise ResourceNotFoundError(f"Literary work '{work_id}' not found.")

        related_ids = set(rec.related_works + rec.related_records)
        if rec.parent_work_id:
            related_ids.add(rec.parent_work_id)

        results: list[LiteraryRecord] = []
        for rid in related_ids:
            target = self.get_work(rid)
            if target:
                results.append(target)

        return sorted(results, key=lambda r: r.id)

    def find_duplicates(self) -> list[tuple[LiteraryRecord, LiteraryRecord]]:
        """Identify potential duplicate literary works by normalized title or source."""
        duplicates: list[tuple[LiteraryRecord, LiteraryRecord]] = []
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

    def find_likely_duplicates(self, record: LiteraryRecord) -> list[LiteraryRecord]:
        """Find likely duplicate works or adaptations sharing titles or sources with a record."""
        target_norm = normalize_unicode(record.title).strip().lower()
        target_words = set(re.findall(r"\w+", target_norm))
        duplicates: list[LiteraryRecord] = []

        for other in self._records.values():
            if other.id == record.id:
                continue
            other_norm = normalize_unicode(other.title).strip().lower()
            other_words = set(re.findall(r"\w+", other_norm))

            # Exact title or alternate title match
            if target_norm == other_norm or target_norm in [
                normalize_unicode(a).strip().lower() for a in other.alternate_titles
            ]:
                duplicates.append(other)
                continue

            # Significant word overlap (e.g. Maitonphi)
            common = target_words.intersection(other_words) - {
                "and", "the", "of", "in", "a", "kala", "wui", "tangkhul"
            }
            if len(common) >= 1 and any(len(w) > 4 for w in common):
                duplicates.append(other)
                continue

            # Same source ID and page
            if (
                record.source_id
                and record.source_id == other.source_id
                and record.source_page
                and record.source_page == other.source_page
            ):
                duplicates.append(other)

        return sorted(duplicates, key=lambda r: r.id)

    def find_related_works(self, record: LiteraryRecord) -> list[LiteraryRecord]:
        """Find related works, adaptations, translations, or parent collections."""
        direct = self.get_related_works(record)
        dupes_and_adaptations = self.find_likely_duplicates(record)
        combined = {r.id: r for r in direct + dupes_and_adaptations}
        return sorted(list(combined.values()), key=lambda r: r.id)

    def find_adaptations(self) -> list[dict[str, Any]]:
        """Group retellings, verse-dramas, and translations sharing core stories."""
        grouped: dict[str, list[LiteraryRecord]] = defaultdict(list)
        for rec in self._records.values():
            key = normalize_unicode(rec.title).lower().strip()
            for prefix in ("the legend of ", "story of ", "tale of ", "ballad of "):
                if key.startswith(prefix):
                    key = key[len(prefix):].strip()
            grouped[key].append(rec)

        adaptations: list[dict[str, Any]] = []
        for concept, group in grouped.items():
            if len(group) > 1:
                types = {r.work_type for r in group}
                adaptations.append({
                    "concept": concept,
                    "work_ids": [r.id for r in group],
                    "work_types": sorted(list(types)),
                    "authors": [r.author for r in group if r.author],
                })
        return adaptations

    def get_literature_report(self) -> dict[str, Any]:
        """Generate comprehensive summary report of the literature catalogue."""
        by_genre: dict[str, int] = defaultdict(int)
        by_verification: dict[str, int] = defaultdict(int)
        by_permission: dict[str, int] = defaultdict(int)
        by_availability: dict[str, int] = defaultdict(int)
        full_text_count = 0
        metadata_only_count = 0
        restricted_count = 0
        linked_to_books_count = 0
        missing_source_metadata: list[str] = []

        for rec in self._records.values():
            by_genre[rec.work_type] += 1
            by_verification[rec.verification_status] += 1
            by_permission[rec.permission_status] += 1
            by_availability[rec.text_availability] += 1

            if rec.permission_status == "restricted" or rec.access_status == "restricted":
                restricted_count += 1

            if rec.text_availability == "full_text" or rec.original_text:
                full_text_count += 1
            else:
                metadata_only_count += 1

            if rec.book_id:
                linked_to_books_count += 1

            if not rec.source_id and not rec.source_url and not rec.source_title:
                missing_source_metadata.append(rec.id)

        return {
            "total_records": len(self._records),
            "by_genre": dict(by_genre),
            "by_verification": dict(by_verification),
            "by_permission": dict(by_permission),
            "by_availability": dict(by_availability),
            "verified_count": by_verification.get("verified", 0),
            "needs_review_count": by_verification.get("needs_review", 0),
            "full_text_count": full_text_count,
            "metadata_only_count": metadata_only_count,
            "restricted_count": restricted_count,
            "linked_to_books_count": linked_to_books_count,
            "missing_source_metadata": missing_source_metadata,
        }

    def export_jsonl(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted literary records to a JSONL file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0

        with path.open("w", encoding="utf-8") as f:
            for rec in self.list_works():
                if not include_restricted and (
                    rec.permission_status == "restricted"
                    or rec.access_status == "restricted"
                ):
                    continue
                f.write(json.dumps(rec.to_dict(), ensure_ascii=False) + "\n")
                count += 1

        return count

    def export_json(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted literary records to a JSON array file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        items = [
            rec.to_dict()
            for rec in self.list_works()
            if include_restricted
            or (
                rec.permission_status != "restricted"
                and rec.access_status != "restricted"
            )
        ]
        with path.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        return len(items)

    def export_csv(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted literary records to a CSV file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "id",
            "title",
            "work_type",
            "author",
            "publication_year",
            "language",
            "dialect",
            "village",
            "book_id",
            "source_id",
            "source_title",
            "source_url",
            "permission_status",
            "access_status",
            "verification_status",
            "text_availability",
            "summary",
        ]

        count = 0
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()

            for rec in self.list_works():
                if not include_restricted and (
                    rec.permission_status == "restricted"
                    or rec.access_status == "restricted"
                ):
                    continue
                writer.writerow(rec.to_dict())
                count += 1

        return count

    def generate_catalogue_report(self) -> dict[str, Any]:
        """Generate comprehensive summary report of the literature catalogue."""
        rep = self.get_literature_report()
        rep["total_works"] = rep["total_records"]
        rep["full_text_permitted_count"] = rep["full_text_count"]
        rep["by_verification_status"] = rep["by_verification"]
        return rep

    def export_to_jsonl(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted literary records to a JSONL file (alias)."""
        return self.export_jsonl(output_path, include_restricted=include_restricted)

    def export_to_csv(self, output_path: Path, include_restricted: bool = False) -> int:
        """Export permitted literary records to a CSV file (alias)."""
        return self.export_csv(output_path, include_restricted=include_restricted)

    @classmethod
    def load_from_manifest(cls, manifest_path: Path) -> LiteratureCatalogue:
        """Instantiate a LiteratureCatalogue from a JSONL manifest file."""
        catalogue = cls()
        path = Path(manifest_path)
        if not path.is_file():
            raise ResourceNotFoundError(f"Literature manifest file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ManifestValidationError(
                        f"JSON syntax error in literature manifest on line {line_no}: {exc}",
                        line_number=line_no,
                    ) from exc
                record = LiteraryRecord.from_dict(data)
                catalogue.add_work(record)

        return catalogue
