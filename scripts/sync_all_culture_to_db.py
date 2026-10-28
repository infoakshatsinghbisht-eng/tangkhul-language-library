#!/usr/bin/env python3
"""Sync all 32 cultural records from data/manifests/culture.jsonl into SQLite databases."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tangkhul_lib.culture.catalogue import CultureCatalogue
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository, ManifestRepository

MANIFEST_FILE = ROOT / "data" / "manifests" / "culture.jsonl"
DB_FILE = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB = ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"


def main():
    catalogue = CultureCatalogue.load_from_manifest(MANIFEST_FILE)
    print(f"Loaded {len(catalogue)} records from {MANIFEST_FILE}")

    for db_path in [DB_FILE, BUNDLED_DB]:
        if not db_path.exists():
            continue
        db_mgr = DatabaseManager(db_path)
        cult_repo = CultureRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        for rec in catalogue.list_records():
            cult_repo.add(rec)
            m_rec = rec.to_manifest_record()
            manifest_repo.add(m_rec)

        print(f"Synced {db_path}: Total in culture table: {cult_repo.count()}")


if __name__ == "__main__":
    main()
