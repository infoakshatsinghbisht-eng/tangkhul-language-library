"""Catalogue management for Tangkhul songs and musical records."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError, ResourceNotFoundError
from tangkhul_lib.songs.models import SongRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class SongCatalogue:
    """Manages in-memory and persistent catalogue of Tangkhul songs."""

    def __init__(self, records: list[SongRecord] | None = None) -> None:
        self._records: dict[str, SongRecord] = {}
        if records:
            for rec in records:
                self.add_song(rec)

    def __len__(self) -> int:
        return len(self._records)

    def add_song(self, song: SongRecord, allow_overwrite: bool = False) -> None:
        """Add a SongRecord to the catalogue.

        Raises:
            ManifestValidationError: If validation fails or duplicate ID exists.
        """
        song.validate()
        if song.id in self._records and not allow_overwrite:
            raise ManifestValidationError(
                f"Song record with ID '{song.id}' already exists in catalogue.",
                record_id=song.id,
            )
        self._records[song.id] = song

    def get_song(self, song_id: str) -> SongRecord | None:
        """Retrieve a song by unique ID."""
        return self._records.get(song_id)

    def list_songs(self) -> list[SongRecord]:
        """List all songs in catalogue."""
        return list(self._records.values())

    def search_songs(
        self,
        query: str | None = None,
        title: str | None = None,
        singer: str | None = None,
        lyricist: str | None = None,
        composer: str | None = None,
        collector: str | None = None,
        year: int | None = None,
        dialect: str | None = None,
        village: str | None = None,
        song_type: str | None = None,
        verification_status: str | None = None,
    ) -> list[SongRecord]:
        """Search and filter songs by metadata fields."""
        results: list[SongRecord] = []

        q_norm = normalize_unicode(query).lower() if query else None
        t_norm = normalize_unicode(title).lower() if title else None
        s_norm = normalize_unicode(singer).lower() if singer else None
        l_norm = normalize_unicode(lyricist).lower() if lyricist else None
        c_norm = normalize_unicode(composer).lower() if composer else None
        col_norm = normalize_unicode(collector).lower() if collector else None
        v_norm = normalize_unicode(village).lower() if village else None
        d_norm = normalize_unicode(dialect).lower() if dialect else None
        type_norm = song_type.strip().lower() if song_type else None
        ver_norm = verification_status.strip().lower() if verification_status else None

        for song in self._records.values():
            if year is not None and song.year != year:
                continue

            if ver_norm and song.verification_status.lower() != ver_norm:
                continue

            if type_norm and (not song.song_type or song.song_type.lower() != type_norm):
                continue

            if t_norm and t_norm not in normalize_unicode(song.title).lower():
                matches_alt = any(
                    t_norm in normalize_unicode(alt).lower() for alt in song.alternate_titles
                )
                if not matches_alt:
                    continue

            if s_norm:
                singer_match = song.singer and s_norm in normalize_unicode(song.singer).lower()
                perf_match = any(
                    s_norm in normalize_unicode(p).lower() for p in song.performers
                )
                if not singer_match and not perf_match:
                    continue

            if l_norm and (
                not song.lyricist or l_norm not in normalize_unicode(song.lyricist).lower()
            ):
                continue

            if c_norm and (
                not song.composer or c_norm not in normalize_unicode(song.composer).lower()
            ):
                continue

            if col_norm and (
                not song.collector or col_norm not in normalize_unicode(song.collector).lower()
            ):
                continue

            if v_norm and (
                not song.village or v_norm not in normalize_unicode(song.village).lower()
            ):
                continue

            if d_norm and (
                not song.dialect or d_norm not in normalize_unicode(song.dialect).lower()
            ):
                continue

            if q_norm:
                haystack = " ".join([
                    song.title,
                    " ".join(song.alternate_titles),
                    song.title_translation or "",
                    song.singer or "",
                    song.lyricist or "",
                    song.composer or "",
                    song.collector or "",
                    " ".join(song.performers),
                    song.village or "",
                    song.dialect or "",
                    song.song_type or "",
                    song.notes or "",
                ]).lower()
                if q_norm not in normalize_unicode(haystack):
                    continue

            results.append(song)

        return results

    def detect_duplicates(self, candidate: SongRecord) -> list[tuple[SongRecord, str]]:
        """Identify potential duplicate records and link alternate recordings.

        Distinguishes:
            - True duplicates: Identical title, singer, and year.
            - Alternate recordings/versions: Identical title but different singer,
              village dialect, or recording session.

        Returns:
            List of tuples (existing_song, relationship_reason).
        """
        matches: list[tuple[SongRecord, str]] = []
        c_title_norm = normalize_unicode(candidate.title).strip().lower()
        c_singer_norm = (
            normalize_unicode(candidate.singer).strip().lower() if candidate.singer else None
        )
        c_village_norm = (
            normalize_unicode(candidate.village).strip().lower() if candidate.village else None
        )
        c_year = candidate.year

        for existing in self._records.values():
            if existing.id == candidate.id:
                continue

            e_title_norm = normalize_unicode(existing.title).strip().lower()
            if e_title_norm != c_title_norm:
                continue

            e_singer_norm = (
                normalize_unicode(existing.singer).strip().lower() if existing.singer else None
            )
            e_village_norm = (
                normalize_unicode(existing.village).strip().lower() if existing.village else None
            )
            e_year = existing.year

            # If title and singer match
            if c_singer_norm and e_singer_norm and c_singer_norm == e_singer_norm:
                if c_year and e_year and c_year == e_year:
                    msg = f"Duplicate: title, singer ('{candidate.singer}'), year {c_year}"
                    matches.append((existing, msg))
                else:
                    msg = f"Alternate recording by same artist ('{candidate.singer}')"
                    matches.append((existing, msg))
            elif c_singer_norm and e_singer_norm and c_singer_norm != e_singer_norm:
                msg = (
                    f"Alternate performance by different artist "
                    f"('{existing.singer}' vs '{candidate.singer}')"
                )
                matches.append((existing, msg))
            elif c_village_norm and e_village_norm and c_village_norm != e_village_norm:
                msg = f"Regional/village variant ({existing.village} vs {candidate.village})"
                matches.append((existing, msg))
            else:
                matches.append((existing, "Potential alternate recording of same title"))

        return matches

    def update_song(self, song_id: str, updates: dict[str, Any]) -> SongRecord:
        """Update fields of an existing song while retaining unchanged metadata.

        Raises:
            ResourceNotFoundError: If song_id is not in catalogue.
            ManifestValidationError: If updated record fails validation.
        """
        existing = self.get_song(song_id)
        if not existing:
            raise ResourceNotFoundError(f"Song '{song_id}' not found in catalogue.")

        current_data = existing.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        current_data.update(updates_clean)

        updated_record = SongRecord.from_dict(current_data)
        updated_record.validate()
        self._records[song_id] = updated_record
        return updated_record

    def export_catalogue(self, target_path: Path, format: str = "jsonl") -> Path:
        """Export the song catalogue to JSON Lines or CSV."""
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if format.lower() == "jsonl":
            with target_path.open("w", encoding="utf-8") as f:
                for song in self._records.values():
                    f.write(json.dumps(song.to_dict(), ensure_ascii=False) + "\n")
        elif format.lower() == "csv":
            fields = [
                "id",
                "title",
                "alternate_titles",
                "title_translation",
                "singer",
                "lyricist",
                "composer",
                "collector",
                "year",
                "village",
                "dialect",
                "song_type",
                "language",
                "source_url",
                "recording_url",
                "permission_status",
                "access_status",
                "verification_status",
            ]
            with target_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
                for song in self._records.values():
                    row = song.to_dict()
                    row["alternate_titles"] = "; ".join(row.get("alternate_titles", []))
                    row["performers"] = ", ".join(row.get("performers", []))
                    writer.writerow(row)
        else:
            raise ValueError(f"Unsupported export format '{format}'. Use 'jsonl' or 'csv'.")

        return target_path

    @classmethod
    def load_from_manifest(cls, manifest_path: Path) -> SongCatalogue:
        """Load songs from a JSON Lines manifest file."""
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

                song = SongRecord.from_dict(data)
                catalogue.add_song(song, allow_overwrite=True)

        return catalogue
