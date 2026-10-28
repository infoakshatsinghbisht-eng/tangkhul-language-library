"""In-memory dictionary catalogue, search, filtering, and export engine."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class DictionaryCatalogue:
    """Catalogue managing dictionary sources, entries, duplicate checks, and exports."""

    def __init__(
        self,
        sources: dict[str, DictionarySourceRecord] | None = None,
        entries: list[DictionaryEntryRecord] | None = None,
    ) -> None:
        self.sources: dict[str, DictionarySourceRecord] = sources or {}
        self.entries: list[DictionaryEntryRecord] = entries or []
        self._entries_by_id: dict[str, DictionaryEntryRecord] = {e.id: e for e in self.entries}

    @classmethod
    def load_from_manifest(
        cls,
        manifest_path: Path,
        entries_path: Path | None = None,
    ) -> DictionaryCatalogue:
        """Instantiate catalogue by loading sources and optional entries."""
        m_path = Path(manifest_path)
        sources: dict[str, DictionarySourceRecord] = {}

        if m_path.is_file():
            with m_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if not line_str or line_str.startswith("#"):
                        continue
                    data = json.loads(line_str)
                    src = DictionarySourceRecord.from_dict(data)
                    sources[src.id] = src

        entries: list[DictionaryEntryRecord] = []
        if entries_path and Path(entries_path).is_file():
            with Path(entries_path).open("r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if not line_str or line_str.startswith("#"):
                        continue
                    data = json.loads(line_str)
                    ent = DictionaryEntryRecord.from_dict(data)
                    entries.append(ent)

        return cls(sources=sources, entries=entries)

    def add_source(self, source: DictionarySourceRecord) -> None:
        """Add or update a dictionary source in the catalogue."""
        source.validate()
        self.sources[source.id] = source

    def get_source(self, source_id: str) -> DictionarySourceRecord | None:
        """Retrieve a dictionary source by its stable ID."""
        return self.sources.get(source_id)

    def list_sources(self) -> list[DictionarySourceRecord]:
        """Return all catalogued dictionary sources sorted by ID."""
        return sorted(self.sources.values(), key=lambda s: s.id)

    def add_entry(self, entry: DictionaryEntryRecord) -> None:
        """Add an entry to the catalogue."""
        entry.validate()
        self.entries.append(entry)
        self._entries_by_id[entry.id] = entry

    def get_entry(self, entry_id: str) -> DictionaryEntryRecord | None:
        """Retrieve an entry by its stable ID."""
        return self._entries_by_id.get(entry_id)

    def list_entries(self, dictionary_id: str | None = None) -> list[DictionaryEntryRecord]:
        """Return entries, optionally filtered by dictionary_id."""
        if dictionary_id:
            return [e for e in self.entries if e.dictionary_id == dictionary_id]
        return list(self.entries)

    def search_sources(
        self,
        query: str | None = None,
        author: str | None = None,
        year: int | None = None,
        language_pair: str | None = None,
        dialect: str | None = None,
        source_type: str | None = None,
        verification_status: str | None = None,
    ) -> list[DictionarySourceRecord]:
        """Filter dictionary sources across metadata fields."""
        results: list[DictionarySourceRecord] = []
        q_norm = normalize_unicode(query).lower() if query else None
        auth_norm = normalize_unicode(author).lower() if author else None
        lp_norm = normalize_unicode(language_pair).lower() if language_pair else None
        dia_norm = normalize_unicode(dialect).lower() if dialect else None

        for src in self.sources.values():
            if year and src.publication_year != year:
                continue
            if source_type and src.source_type != source_type:
                continue
            if verification_status and src.verification_status != verification_status:
                continue

            if auth_norm:
                all_creators = src.authors + src.editors + src.contributors
                if src.compiler:
                    all_creators.append(src.compiler)
                matched = any(auth_norm in normalize_unicode(a).lower() for a in all_creators)
                if not matched:
                    continue

            if lp_norm:
                if (
                    not src.language_pair
                    or lp_norm not in normalize_unicode(src.language_pair).lower()
                ):
                    continue

            if dia_norm:
                if not src.dialect or dia_norm not in normalize_unicode(src.dialect).lower():
                    continue

            if q_norm:
                haystack = " ".join([
                    src.title,
                    " ".join(src.alternate_titles),
                    src.publisher or "",
                    src.compiler or "",
                    " ".join(src.authors),
                    src.notes or "",
                ])
                if q_norm not in normalize_unicode(haystack).lower():
                    continue

            results.append(src)

        return sorted(results, key=lambda s: s.id)

    def search_entries(
        self,
        headword: str | None = None,
        meaning: str | None = None,
        english: str | None = None,
        hindi: str | None = None,
        part_of_speech: str | None = None,
        dialect: str | None = None,
        source_id: str | None = None,
        verification_status: str | None = None,
    ) -> list[DictionaryEntryRecord]:
        """Search and filter lexical entries across linguistic criteria."""
        results: list[DictionaryEntryRecord] = []
        hw_norm = normalize_unicode(headword).strip().lower() if headword else None
        m_norm = normalize_unicode(meaning).strip().lower() if meaning else None
        en_norm = normalize_unicode(english).strip().lower() if english else None
        hi_norm = normalize_unicode(hindi).strip().lower() if hindi else None
        pos_norm = part_of_speech.strip().lower() if part_of_speech else None
        dia_norm = normalize_unicode(dialect).strip().lower() if dialect else None

        for ent in self.entries:
            if source_id and ent.dictionary_id != source_id:
                continue
            if verification_status and ent.verification_status != verification_status:
                continue
            if pos_norm and (not ent.part_of_speech or ent.part_of_speech.lower() != pos_norm):
                continue
            if dia_norm and (
                not ent.dialect or dia_norm not in normalize_unicode(ent.dialect).lower()
            ):
                continue

            if hw_norm:
                head_match = (
                    hw_norm in ent.normalized_headword if ent.normalized_headword else False
                )
                alt_match = any(
                    hw_norm in normalize_unicode(a).strip().lower()
                    for a in ent.alternate_spellings
                )
                if not head_match and not alt_match:
                    continue

            if en_norm:
                matched_en = any(
                    en_norm in normalize_unicode(defn).lower()
                    for defn in ent.definitions_en
                )
                if not matched_en:
                    continue

            if hi_norm:
                matched_hi = any(
                    hi_norm in normalize_unicode(defn).lower()
                    for defn in ent.definitions_hi
                )
                if not matched_hi:
                    continue

            if m_norm:
                all_defs = ent.definitions_en + ent.definitions_hi + ent.other_definitions
                matched_m = any(
                    m_norm in normalize_unicode(defn).lower()
                    for defn in all_defs
                )
                if not matched_m:
                    continue

            results.append(ent)

        return results

    def find_likely_duplicates(
        self,
        entry: DictionaryEntryRecord,
    ) -> list[DictionaryEntryRecord]:
        """Identify duplicate records while strictly preserving distinct senses.

        Entries with matching headwords but distinct definitions or different parts of speech
        represent polysemous words or distinct senses, NOT duplicates.
        """
        duplicates: list[DictionaryEntryRecord] = []
        target_norm = entry.normalized_headword or normalize_unicode(entry.headword).strip().lower()
        target_defs = set(d.strip().lower() for d in entry.definitions_en + entry.other_definitions)

        for candidate in self.entries:
            if candidate.id == entry.id:
                continue

            cand_norm = (
                candidate.normalized_headword
                or normalize_unicode(candidate.headword).strip().lower()
            )
            if cand_norm != target_norm:
                continue

            # Check if senses/definitions overlap substantially
            cand_defs = set(
                d.strip().lower()
                for d in candidate.definitions_en + candidate.other_definitions
            )
            overlap = target_defs.intersection(cand_defs)
            same_pos = candidate.part_of_speech == entry.part_of_speech

            if overlap and same_pos and candidate.dictionary_id == entry.dictionary_id:
                duplicates.append(candidate)

        return duplicates

    def find_conflicts(self) -> list[dict[str, Any]]:
        """Identify headwords with conflicting definitions, spellings, or POS across sources."""
        import unicodedata

        grouped: dict[str, list[DictionaryEntryRecord]] = defaultdict(list)
        for ent in self.entries:
            raw = ent.headword.strip().lower()
            nfd = unicodedata.normalize("NFD", raw)
            base_key = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
            grouped[base_key].append(ent)

        conflicts: list[dict[str, Any]] = []
        for norm_hw, group in grouped.items():
            if len(group) < 2:
                continue

            sources = set(e.dictionary_id for e in group)
            pos_set = set(e.part_of_speech for e in group if e.part_of_speech)
            spellings = set(e.headword for e in group)

            if len(pos_set) > 1 or len(spellings) > 1:
                conflicts.append({
                    "headword_norm": norm_hw,
                    "spellings": sorted(spellings),
                    "parts_of_speech": sorted(pos_set),
                    "sources": sorted(sources),
                    "entry_count": len(group),
                    "entries": [e.id for e in group],
                })

        return conflicts

    def get_source_report(self) -> dict[str, Any]:
        """Generate structured breakdown of sources and their access/permission status."""
        total_sources = len(self.sources)
        verified_count = sum(
            1 for s in self.sources.values() if s.verification_status == "verified"
        )
        needs_review_count = sum(
            1 for s in self.sources.values() if s.verification_status == "needs_review"
        )
        metadata_only = sum(
            1 for s in self.sources.values() if s.access_status == "metadata_only"
        )
        full_text = sum(
            1 for s in self.sources.values()
            if s.access_status in ("full_text_available", "open_access")
        )

        entries_by_src: dict[str, int] = defaultdict(int)
        for e in self.entries:
            entries_by_src[e.dictionary_id] += 1

        return {
            "total_sources": total_sources,
            "verified_sources": verified_count,
            "needs_review_sources": needs_review_count,
            "metadata_only_sources": metadata_only,
            "full_text_sources": full_text,
            "total_entries": len(self.entries),
            "entries_per_source": dict(entries_by_src),
        }

    def export_sources_jsonl(self, output_path: Path) -> None:
        """Export dictionary source records to JSON Lines."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for src in self.list_sources():
                f.write(json.dumps(src.to_manifest_record().to_dict(), ensure_ascii=False) + "\n")

    def export_sources_csv(self, output_path: Path) -> None:
        """Export dictionary source metadata to CSV."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "id", "title", "authors", "publication_year", "publisher",
            "language_pair", "dialect", "source_type", "permission_status",
            "access_status", "verification_status", "source_url"
        ]
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for src in self.list_sources():
                writer.writerow({
                    "id": src.id,
                    "title": src.title,
                    "authors": "; ".join(src.authors),
                    "publication_year": src.publication_year or "",
                    "publisher": src.publisher or "",
                    "language_pair": src.language_pair or "",
                    "dialect": src.dialect or "",
                    "source_type": src.source_type,
                    "permission_status": src.permission_status,
                    "access_status": src.access_status,
                    "verification_status": src.verification_status,
                    "source_url": src.source_url or "",
                })

    def export_entries_jsonl(self, output_path: Path, permitted_only: bool = True) -> None:
        """Export dictionary entries to JSON Lines, filtering restricted content by default."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for ent in self.entries:
                if permitted_only and ent.permission_status in ("restricted", "pending"):
                    continue
                f.write(json.dumps(ent.to_dict(), ensure_ascii=False) + "\n")

    def export_entries_csv(self, output_path: Path, permitted_only: bool = True) -> None:
        """Export dictionary entries to CSV."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "id", "dictionary_id", "headword", "definitions_en", "definitions_hi",
            "part_of_speech", "dialect", "page_or_section", "permission_status",
            "verification_status"
        ]
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ent in self.entries:
                if permitted_only and ent.permission_status in ("restricted", "pending"):
                    continue
                writer.writerow({
                    "id": ent.id,
                    "dictionary_id": ent.dictionary_id,
                    "headword": ent.headword,
                    "definitions_en": "; ".join(ent.definitions_en),
                    "definitions_hi": "; ".join(ent.definitions_hi),
                    "part_of_speech": ent.part_of_speech or "",
                    "dialect": ent.dialect or "",
                    "page_or_section": ent.page_or_section or "",
                    "permission_status": ent.permission_status,
                    "verification_status": ent.verification_status,
                })
