#!/usr/bin/env python3
"""Register Batch 2 historical Tangkhul songs (SNG-HIST-007 through SNG-HIST-014) in SQLite databases and index tokens."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.batch2_ingest_songs import BATCH2_SONGS
from tangkhul_lib.songs.extractor import SongLyricsExtractor
from tangkhul_lib.songs.models import SongRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import ManifestRepository, SongRepository

DB_FILE = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_FILE = ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"


def register_batch2() -> None:
    extractor = SongLyricsExtractor()

    for db_path in [DB_FILE, BUNDLED_DB_FILE]:
        if not db_path.exists():
            continue
        db_mgr = DatabaseManager(db_path)
        song_repo = SongRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        for s_data in BATCH2_SONGS:
            rec = {k: v for k, v in s_data.items() if k != "stanzas"}
            song = SongRecord.from_dict(rec)

            if not song_repo.get_by_id(song.id):
                song_repo.add(song)
            else:
                song_repo.update(song.id, rec)

            m_rec = song.to_manifest_record()
            if not manifest_repo.get_by_id(m_rec.id):
                manifest_repo.add(m_rec)

            if song.local_file_path:
                raw_path = ROOT / song.local_file_path
                if raw_path.exists():
                    raw_lines = extractor.parse_lyrics_text(raw_path.read_text(encoding="utf-8"))
                    raw_tokens, _ = extractor.extract_vocabulary_candidates(song, raw_lines)
                    song_repo.save_tokens(song.id, raw_tokens)

        print(f"Database sync ({db_path}): Total songs in repo: {song_repo.count()}")


if __name__ == "__main__":
    register_batch2()
