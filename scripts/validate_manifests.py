#!/usr/bin/env python3
"""Script to validate all JSON Lines manifests in data/manifests/."""

from __future__ import annotations

import sys
from pathlib import Path

# Add src to sys.path so the script can run without prior package installation
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.ingestion.metadata_validation import validate_all_manifests


def main() -> int:
    manifest_dir = ROOT / "data" / "manifests"
    if not manifest_dir.is_dir():
        print(f"Error: Manifest directory not found at {manifest_dir}", file=sys.stderr)
        return 1

    print("=" * 65)
    print("Tangkhul Language Library -- Manifest & Cross-Catalogue Validation")
    print("=" * 65)

    try:
        manifest_map = validate_all_manifests(manifest_dir)
    except ManifestValidationError as exc:
        print(f"FAIL: Manifest validation failed: {exc}", file=sys.stderr)
        return 1

    total_records = 0
    for filename, records in manifest_map.items():
        total_records += len(records)
        print(f"OK:   {filename:<25} ({len(records)} record(s))")

    print("-" * 65)
    print(f"Validation completed. Total records across all manifests: {total_records}")
    print("Global ID uniqueness: Verified (no duplicate IDs across any catalogues)")
    print("Status: PASSED all manifest checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
