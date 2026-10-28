"""Permission-aware dictionary entry extractor and parser."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord
from tangkhul_lib.vocabulary.normalization import sanitize_spacing


class DictionaryExtractor:
    """Extractor for parsing dictionary entries from authorized files while checking permissions."""

    def check_permissions(self, source: DictionarySourceRecord) -> None:
        """Validate whether the dictionary source permits entry-level text extraction."""
        if source.permission_status == "restricted" or source.access_status == "metadata_only":
            perm_str = (
                f"Permission status: '{source.permission_status}', "
                f"Access status: '{source.access_status}'."
            )
            raise PermissionDeniedError(
                f"Text/entry extraction is not permitted for dictionary '{source.id}'. "
                f"{perm_str} Only bibliographic metadata is allowed for this source.",
                record_id=source.id,
                permission_status=source.permission_status,
            )

    def extract_from_tsv_or_csv(
        self,
        source: DictionarySourceRecord,
        file_path: Path,
        delimiter: str = "\t",
        enforce_permissions: bool = True,
    ) -> list[DictionaryEntryRecord]:
        """Extract entries from a tabular CSV or TSV file."""
        if enforce_permissions:
            self.check_permissions(source)

        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        entries: list[DictionaryEntryRecord] = []
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for idx, row in enumerate(reader, start=1):
                hw = sanitize_spacing(row.get("headword", "") or row.get("word", ""))
                if not hw:
                    continue

                defs_en_raw = (
                    row.get("definitions_en")
                    or row.get("english")
                    or row.get("definition", "")
                )
                defs_en = [d.strip() for d in re.split(r"[;,]", defs_en_raw) if d.strip()]

                defs_hi_raw = row.get("definitions_hi") or row.get("hindi", "")
                defs_hi = [d.strip() for d in re.split(r"[;,]", defs_hi_raw) if d.strip()]

                pos = row.get("part_of_speech") or row.get("pos")
                if pos:
                    pos = pos.strip().lower()

                page = row.get("page") or row.get("page_or_section")
                alt_raw = row.get("alternative_spellings") or row.get("alternate_spellings", "")
                alt_spellings = [a.strip() for a in alt_raw.split(";") if a.strip()]

                confidence = float(row.get("confidence", 1.0))
                ver_status = "verified" if confidence >= 0.9 else "needs_review"

                ent = DictionaryEntryRecord(
                    id=f"{source.id}-ENT-{idx:04d}",
                    dictionary_id=source.id,
                    headword=hw,
                    alternate_spellings=alt_spellings,
                    definitions_en=defs_en,
                    definitions_hi=defs_hi,
                    part_of_speech=pos,
                    dialect=row.get("dialect") or source.dialect,
                    page_or_section=page,
                    extraction_method="tabular_import",
                    confidence=confidence,
                    permission_status=source.permission_status,
                    verification_status=ver_status,
                )
                entries.append(ent)

        return entries

    def extract_from_jsonl(
        self,
        source: DictionarySourceRecord,
        file_path: Path,
        enforce_permissions: bool = True,
    ) -> list[DictionaryEntryRecord]:
        """Extract entries from a JSON Lines file."""
        if enforce_permissions:
            self.check_permissions(source)

        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        entries: list[DictionaryEntryRecord] = []
        with path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                line_str = line.strip()
                if not line_str or line_str.startswith("#"):
                    continue
                data = json.loads(line_str)
                data.setdefault("id", f"{source.id}-ENT-{idx:04d}")
                data.setdefault("dictionary_id", source.id)
                data.setdefault("permission_status", source.permission_status)
                ent = DictionaryEntryRecord.from_dict(data)
                entries.append(ent)

        return entries

    def parse_text_lines(
        self,
        source: DictionarySourceRecord,
        lines: list[str],
        enforce_permissions: bool = True,
    ) -> list[DictionaryEntryRecord]:
        """Parse structured text lines into dictionary entries.

        Expected pattern:
        `headword (pos.) definition` or `headword : definition`
        """
        if enforce_permissions:
            self.check_permissions(source)

        entries: list[DictionaryEntryRecord] = []
        pattern = re.compile(
            r"^([A-Za-zāēīōūĀĒĪŌŪ\-\'\s]+?)(?:\s*\(([a-z\.\,\s]+)\))?\s*[:\-–]\s*(.+)$"
        )

        for idx, line in enumerate(lines, start=1):
            line_clean = sanitize_spacing(line)
            if not line_clean or line_clean.startswith("#"):
                continue

            match = pattern.match(line_clean)
            if match:
                hw = match.group(1).strip()
                pos_raw = match.group(2)
                defn_raw = match.group(3).strip()

                pos = pos_raw.strip().rstrip(".").lower() if pos_raw else None
                defs = [d.strip() for d in re.split(r"[;,]", defn_raw) if d.strip()]

                ent = DictionaryEntryRecord(
                    id=f"{source.id}-ENT-{idx:04d}",
                    dictionary_id=source.id,
                    headword=hw,
                    definitions_en=defs,
                    part_of_speech=pos,
                    dialect=source.dialect,
                    extraction_method="text_line_parser",
                    confidence=0.95,
                    permission_status=source.permission_status,
                    verification_status="verified",
                )
                entries.append(ent)
            else:
                # Unparsed line flagged for review
                parts = line_clean.split(" ", 1)
                hw = parts[0].strip()
                defn = parts[1].strip() if len(parts) > 1 else ""
                ent = DictionaryEntryRecord(
                    id=f"{source.id}-ENT-{idx:04d}",
                    dictionary_id=source.id,
                    headword=hw,
                    definitions_en=[defn] if defn else [],
                    dialect=source.dialect,
                    extraction_method="fallback_line_parser",
                    confidence=0.6,
                    permission_status=source.permission_status,
                    verification_status="needs_review",
                    notes="Unstructured line format; needs human verification.",
                )
                entries.append(ent)

        return entries
