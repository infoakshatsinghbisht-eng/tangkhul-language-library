#!/usr/bin/env python3
"""Sync all 25 literary records from data/manifests/literature.jsonl into SQLite databases.

Enriches records with authentic Tangkhul literary texts, English translations, stanza/line counts,
and critical commentary from scripts.build_raw_literature.LITERATURE_RAW_DATA.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_raw_literature import LITERATURE_RAW_DATA
from scripts.build_raw_literature_batch2 import LITERATURE_BATCH2_RAW_DATA
from scripts.build_raw_literature_batch3 import LITERATURE_BATCH3_RAW_DATA
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, ManifestRepository

ALL_LITERATURE_RAW_DATA = {
    **LITERATURE_RAW_DATA,
    **LITERATURE_BATCH2_RAW_DATA,
    **LITERATURE_BATCH3_RAW_DATA,
}

MANIFEST_FILE = ROOT / "data" / "manifests" / "literature.jsonl"
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
        db_mgr.initialize_schema()
        lit_repo = LiteratureRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        for d in records_raw:
            lid = d["id"]
            extra = ALL_LITERATURE_RAW_DATA.get(lid, {})
            if extra:
                t_stanzas = extra.get("tangkhul_text", [])
                e_stanzas = extra.get("english_text", [])
                d["original_text"] = "\n\n".join(t_stanzas)
                d["translation_text"] = "\n\n".join(e_stanzas)
                d["text_availability"] = "full_text"
                d["stanza_count"] = len(t_stanzas)
                d["line_count"] = sum(
                    len([line for line in s.splitlines() if line.strip()])
                    for s in t_stanzas
                )
                if extra.get("critical_commentary"):
                    d["summary"] = extra.get("critical_commentary")

            rec = LiteraryRecord.from_dict(d)
            lit_repo.add(rec)
            m_rec = rec.to_manifest_record()
            manifest_repo.add(m_rec)

        print(f"Synced {db_path}: Total in literature table: {lit_repo.count()}")


if __name__ == "__main__":
    main()
