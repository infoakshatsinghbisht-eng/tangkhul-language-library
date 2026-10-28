#!/usr/bin/env python3
"""Inspect data sources, raw storage, manifests, and candidate acquisition readiness."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

# Ensure UTF-8 output on all platforms
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tangkhul_lib.core.config import LibraryConfig


def main() -> int:
    config = LibraryConfig.from_environment()
    paths = config.paths

    print("=" * 70)
    print("Tangkhul Language Library -- Source Inspection & Acquisition Readiness")
    print("=" * 70)
    print(f"Project Root:     {paths.root_dir}")
    print(f"Data Directory:   {paths.data_dir}")
    print(f"Database Dir:     {paths.database_dir}")
    print("-" * 70)

    total_records = 0
    verification_counts: Counter[str] = Counter()
    permission_counts: Counter[str] = Counter()
    candidate_records: list[dict[str, str]] = []

    print("\n[1] Manifest Catalogues (data/manifests/):")
    if paths.manifests_dir.exists():
        manifests = sorted(paths.manifests_dir.glob("*.jsonl"))
        for m in manifests:
            m_records = 0
            with m.open("r", encoding="utf-8") as f:
                for line in f:
                    line_s = line.strip()
                    if not line_s or line_s.startswith("#"):
                        continue
                    m_records += 1
                    try:
                        rec = json.loads(line_s)
                    except json.JSONDecodeError:
                        continue
                    ver = rec.get("verification_status", "unverified")
                    perm = rec.get("permission_status", "pending")
                    verification_counts[ver] += 1
                    permission_counts[perm] += 1
                    if ver == "needs_review" or "CAND" in str(rec.get("id")):
                        creator_raw = (
                            rec.get("creator")
                            or rec.get("author")
                            or rec.get("singer")
                            or "Unknown"
                        )
                        candidate_records.append({
                            "id": rec.get("id", "UNKNOWN"),
                            "module": m.stem,
                            "title": rec.get("title", "Untitled")[:40],
                            "creator": creator_raw[:25],
                            "verification": ver,
                            "permission": perm,
                            "url": rec.get("source_url") or "None (Archival/Citation)",
                            "notes": rec.get("notes", "")[:60] + "...",
                        })

            total_records += m_records
            size_bytes = m.stat().st_size
            print(f"  - {m.name:<25} {m_records:>3} record(s)  ({size_bytes:>6} bytes)")
        print(f"  Total Catalogued Records:   {total_records:>3}")
    else:
        print("  Directory does not exist.")

    print("\n[2] Verification Status Breakdown:")
    for status, count in sorted(verification_counts.items()):
        pct = (count / total_records * 100) if total_records else 0
        print(f"  - {status:<20} {count:>3} ({pct:>5.1f}%)")

    print("\n[3] Permission Tier Breakdown:")
    for tier, count in sorted(permission_counts.items()):
        pct = (count / total_records * 100) if total_records else 0
        print(f"  - {tier:<20} {count:>3} ({pct:>5.1f}%)")

    print("\n[4] Candidate Resources Awaiting Review & Acquisition Clearance:")
    if candidate_records:
        for c in candidate_records:
            print(f"  * [{c['id']}] ({c['module'].upper()}) {c['title']}")
            print(
                f"    Creator/Source: {c['creator']} | "
                f"Status: {c['verification']} / {c['permission']}"
            )
            print(f"    Discovery Ref:  {c['url']}")
            print(f"    Action Needed:  {c['notes']}")
    else:
        print("  No candidate records found.")

    print("\n[5] Raw Sources Storage (data/raw/):")
    if paths.raw_dir.exists():
        subdirs = sorted([d for d in paths.raw_dir.iterdir() if d.is_dir()])
        for d in subdirs:
            non_keep_files = [f for f in d.iterdir() if f.is_file() and f.name != ".gitkeep"]
            print(f"  - {d.name:<25} {len(non_keep_files):>3} source file(s)")
    else:
        print("  Directory does not exist.")

    print("\n[6] Database & Storage Status:")
    db_file = paths.database_dir / config.sqlite_db_name
    db_status = "present" if db_file.exists() else "not initialized (on-demand)"
    print(f"  - SQLite Database:  {db_status} ({db_file.name})")

    print("\n[7] Authoritative Discovery Repositories (For Future Acquisitions):")
    print("  - BharataVani Project:")
    print("      Textbooks:    https://bharatavani.in/tangkhul/textbook")
    print("      Bhashakosha:  https://bharatavani.in/tangkhul/bhashakosha")
    print("      Jnanakosha:   https://bharatavani.in/tangkhul/jnanakosha")
    print("  - CIIL Sanchika Repository:")
    print("      Collections:  https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e")
    print("  - Community Song Archives:")
    print("      Lyrics:       https://tangkhullyrics.com/ | https://www.tangkhullaa.com/")
    print("  - Linguistic & Cultural Documentation:")
    print("      Centre:       https://ibsdmirandahousecentrefornortheaststudies.wordpress.com/2017/04/04/3-april-2017/")

    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
