#!/usr/bin/env python3
"""Script to inspect data sources, raw storage, and manifest statistics without modifying files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tangkhul_lib.core.config import LibraryConfig


def main() -> int:
    config = LibraryConfig.from_environment()
    paths = config.paths

    print("=" * 65)
    print("Tangkhul Language Library -- Source & Storage Inspection")
    print("=" * 65)
    print(f"Project Root:     {paths.root_dir}")
    print(f"Data Directory:   {paths.data_dir}")
    print(f"Database Dir:     {paths.database_dir}")
    print("-" * 65)

    print("\n[1] Manifest Catalogues (data/manifests/):")
    if paths.manifests_dir.exists():
        manifests = sorted(paths.manifests_dir.glob("*.jsonl"))
        for m in manifests:
            with m.open("r", encoding="utf-8") as f:
                line_count = sum(
                    1 for line in f if line.strip() and not line.startswith("#")
                )
            size_bytes = m.stat().st_size
            print(f"  - {m.name:<25} {line_count:>4} record(s)  ({size_bytes} bytes)")
    else:
        print("  Directory does not exist.")

    print("\n[2] Raw Sources (data/raw/):")
    if paths.raw_dir.exists():
        subdirs = sorted([d for d in paths.raw_dir.iterdir() if d.is_dir()])
        for d in subdirs:
            non_keep_files = [f for f in d.iterdir() if f.is_file() and f.name != ".gitkeep"]
            print(f"  - {d.name:<25} {len(non_keep_files):>4} source file(s)")
    else:
        print("  Directory does not exist.")

    print("\n[3] Processed & Database Status:")
    db_file = paths.database_dir / config.sqlite_db_name
    db_status = "present" if db_file.exists() else "not initialized (planned)"
    print(f"  - SQLite Database:  {db_status} ({db_file.name})")

    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(main())
