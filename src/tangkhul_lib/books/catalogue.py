"""Catalogue management for Tangkhul book records."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.exceptions import ManifestValidationError, ResourceNotFoundError
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class BookCatalogue:
    """Manages the in-memory and persistent catalogue of Tangkhul books."""

    def __init__(self, records: list[BookRecord] | None = None) -> None:
        self._records: dict[str, BookRecord] = {}
        if records:
            for rec in records:
                self.add_book(rec)

    def __len__(self) -> int:
        return len(self._records)

    def add_book(self, book: BookRecord, allow_overwrite: bool = False) -> None:
        """Add a BookRecord to the catalogue.

        Raises:
            ManifestValidationError: If validation fails or duplicate ID exists.
        """
        book.validate()
        if book.id in self._records and not allow_overwrite:
            raise ManifestValidationError(
                f"Book record with ID '{book.id}' already exists in catalogue.",
                record_id=book.id,
            )
        self._records[book.id] = book

    def get_book(self, book_id: str) -> BookRecord | None:
        """Retrieve a book by its unique ID."""
        return self._records.get(book_id)

    def list_books(self) -> list[BookRecord]:
        """List all books in the catalogue."""
        return list(self._records.values())

    def search_books(
        self,
        query: str | None = None,
        author: str | None = None,
        title: str | None = None,
        publication_year: int | None = None,
        subject: str | None = None,
        publisher: str | None = None,
        verification_status: str | None = None,
        educational_level: str | None = None,
    ) -> list[BookRecord]:
        """Search and filter books in the catalogue."""
        results: list[BookRecord] = []

        q_norm = normalize_unicode(query).lower() if query else None
        a_norm = normalize_unicode(author).lower() if author else None
        t_norm = normalize_unicode(title).lower() if title else None
        s_norm = normalize_unicode(subject).lower() if subject else None
        p_norm = normalize_unicode(publisher).lower() if publisher else None
        v_norm = verification_status.strip().lower() if verification_status else None
        e_norm = normalize_unicode(educational_level).lower() if educational_level else None

        for book in self._records.values():
            if publication_year is not None and book.publication_year != publication_year:
                continue

            if v_norm and book.verification_status.lower() != v_norm:
                continue

            if t_norm and t_norm not in normalize_unicode(book.title).lower():
                # Check alternate titles as well
                matches_alt = any(
                    t_norm in normalize_unicode(alt).lower() for alt in book.alternate_titles
                )
                if not matches_alt:
                    continue

            if a_norm:
                author_matches = any(
                    a_norm in normalize_unicode(auth).lower() for auth in book.authors
                ) or any(a_norm in normalize_unicode(ed).lower() for ed in book.editors)
                if not author_matches:
                    continue

            if s_norm:
                if not book.subject or s_norm not in normalize_unicode(book.subject).lower():
                    continue

            if p_norm:
                if not book.publisher or p_norm not in normalize_unicode(book.publisher).lower():
                    continue

            if e_norm:
                if (
                    not book.educational_level
                    or e_norm not in normalize_unicode(book.educational_level).lower()
                ):
                    continue

            if q_norm:
                haystack = " ".join([
                    book.title,
                    " ".join(book.alternate_titles),
                    " ".join(book.authors),
                    " ".join(book.editors),
                    book.publisher or "",
                    book.subject or "",
                    book.educational_level or "",
                    book.notes or "",
                ]).lower()
                if q_norm not in normalize_unicode(haystack):
                    continue

            results.append(book)

        return results

    def detect_duplicates(self, candidate: BookRecord) -> list[tuple[BookRecord, str]]:
        """Identify potential duplicate records without misclassifying distinct editions.

        Returns:
            List of tuples (existing_book, reason_string).
        """
        duplicates: list[tuple[BookRecord, str]] = []
        c_title_norm = normalize_unicode(candidate.title).strip().lower()
        c_level_norm = (
            normalize_unicode(candidate.educational_level).strip().lower()
            if candidate.educational_level
            else None
        )
        c_year = candidate.publication_year
        c_isbn = candidate.isbn.strip().replace("-", "") if candidate.isbn else None

        for existing in self._records.values():
            if existing.id == candidate.id:
                continue

            e_isbn = existing.isbn.strip().replace("-", "") if existing.isbn else None
            if c_isbn and e_isbn and c_isbn == e_isbn:
                duplicates.append((existing, f"Matching ISBN: {candidate.isbn}"))
                continue

            e_title_norm = normalize_unicode(existing.title).strip().lower()
            if e_title_norm != c_title_norm:
                continue

            e_level_norm = (
                normalize_unicode(existing.educational_level).strip().lower()
                if existing.educational_level
                else None
            )
            e_year = existing.publication_year

            # If educational level differs, they are distinct levels (e.g. Class IV vs Class V)
            if c_level_norm and e_level_norm and c_level_norm != e_level_norm:
                continue

            # If editions or years differ when levels are absent, treat as separate editions
            if candidate.edition and existing.edition and candidate.edition != existing.edition:
                continue

            # If title and level are identical
            if c_level_norm and e_level_norm and c_level_norm == e_level_norm:
                if c_year == e_year:
                    msg = (
                        f"Identical title, level ('{existing.educational_level}'), "
                        f"and year ({c_year})"
                    )
                    duplicates.append((existing, msg))
                else:
                    msg = (
                        f"Same title and level ('{existing.educational_level}'), "
                        f"differing years ({existing.publication_year} vs {c_year})"
                    )
                    duplicates.append((existing, msg))
            elif not c_level_norm and not e_level_norm:
                if c_year and e_year and c_year == e_year:
                    msg = f"Identical title and publication year ({c_year})"
                    duplicates.append((existing, msg))
                elif not c_year and not e_year:
                    duplicates.append((existing, "Identical title with unspecified year and level"))

        return duplicates

    def update_book(self, book_id: str, updates: dict[str, Any]) -> BookRecord:
        """Update fields of an existing book while retaining unchanged metadata.

        Raises:
            ResourceNotFoundError: If book_id is not in catalogue.
            ManifestValidationError: If updated record fails validation.
        """
        existing = self.get_book(book_id)
        if not existing:
            raise ResourceNotFoundError(f"Book '{book_id}' not found in catalogue.")

        current_data = existing.to_dict()
        # Disallow updating immutable id
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        current_data.update(updates_clean)

        updated_record = BookRecord.from_dict(current_data)
        updated_record.validate()
        self._records[book_id] = updated_record
        return updated_record

    def export_catalogue(self, target_path: Path, format: str = "jsonl") -> Path:
        """Export the catalogue to JSON Lines or CSV."""
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if format.lower() == "jsonl":
            with target_path.open("w", encoding="utf-8") as f:
                for book in self._records.values():
                    f.write(json.dumps(book.to_dict(), ensure_ascii=False) + "\n")
        elif format.lower() == "csv":
            fields = [
                "id",
                "title",
                "alternate_titles",
                "authors",
                "editors",
                "publisher",
                "publication_year",
                "subject",
                "educational_level",
                "language",
                "isbn",
                "source_url",
                "permission_status",
                "access_status",
                "verification_status",
            ]
            with target_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
                for book in self._records.values():
                    row = book.to_dict()
                    row["alternate_titles"] = "; ".join(row.get("alternate_titles", []))
                    row["authors"] = ", ".join(row.get("authors", []))
                    row["editors"] = ", ".join(row.get("editors", []))
                    writer.writerow(row)
        else:
            raise ValueError(f"Unsupported export format '{format}'. Use 'jsonl' or 'csv'.")

        return target_path

    @classmethod
    def load_from_manifest(cls, manifest_path: Path) -> BookCatalogue:
        """Load books from a JSON Lines manifest file."""
        path = Path(manifest_path)
        if not path.is_file():
            return cls([])

        catalogue = cls()
        with path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                line_str = line.strip()
                if not line_str or line_str.startswith("#"):
                    continue
                try:
                    data = json.loads(line_str)
                except json.JSONDecodeError as exc:
                    raise ManifestValidationError(
                        f"Malformed JSON on line {idx} in {path.name}: {exc}",
                        line_number=idx,
                    ) from exc

                book = BookRecord.from_dict(data)
                catalogue.add_book(book, allow_overwrite=True)

        return catalogue
