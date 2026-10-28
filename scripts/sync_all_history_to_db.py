#!/usr/bin/env python3
"""Sync all 24 historical records from data/manifests/history.jsonl into SQLite databases.

Enriches records with authentic Tangkhul narratives, English glosses, people, and significance
from scripts.build_raw_history.HISTORY_RAW_DATA.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_raw_history import HISTORY_RAW_DATA
from tangkhul_lib.history.models import HistoricalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import HistoryRepository, ManifestRepository

MANIFEST_FILE = ROOT / "data" / "manifests" / "history.jsonl"
DB_FILE = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB = ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"


def main() -> None:
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        records_raw = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(records_raw)} records from {MANIFEST_FILE}")

    for db_path in [DB_FILE, BUNDLED_DB]:
        if not db_path.exists():
            continue
        db_mgr = DatabaseManager(db_path)
        history_repo = HistoryRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        for d in records_raw:
            hid = d["id"]
            extra = HISTORY_RAW_DATA.get(hid, {})
            # Enrich fields
            if extra:
                d["original_text"] = "\n".join(extra.get("tangkhul_text", []))
                d["translation_en"] = "\n".join(extra.get("english_text", []))
                d["people_involved"] = extra.get("key_figures", [])
                d["description"] = extra.get("historical_significance")
                d["summary"] = d.get("notes")

            rec = HistoricalRecord.from_dict(d)
            history_repo.add(rec)
            m_rec = rec.to_manifest_record()
            manifest_repo.add(m_rec)

        print(f"Synced {db_path}: Total in history table: {history_repo.count()}")


if __name__ == "__main__":
    main()
