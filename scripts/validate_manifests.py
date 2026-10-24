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
from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file


def main() -> int:
    manifest_dir = ROOT / "data" / "manifests"
    if not manifest_dir.is_dir():
        print(f"Error: Manifest directory not found at {manifest_dir}", file=sys.stderr)
        return 1

    manifest_files = sorted(manifest_dir.glob("*.jsonl"))
    if not manifest_files:
        print(f"No .jsonl manifest files found in {manifest_dir}")
        return 0

    print("=" * 60)
    print("Tangkhul Language Library -- Manifest Validation")
    print("=" * 60)

    total_records = 0
    errors_found = False

    for file_path in manifest_files:
        try:
            records = validate_manifest_file(file_path)
            total_records += len(records)
            print(f"OK:   {file_path.name:<25} ({len(records)} record(s))")
        except ManifestValidationError as exc:
            errors_found = True
            print(f"FAIL: {file_path.name:<25} Error: {exc}", file=sys.stderr)

    print("-" * 60)
    print(f"Validation completed. Total records across all manifests: {total_records}")

    if errors_found:
        print("Status: FAILED due to validation errors.", file=sys.stderr)
        return 1

    print("Status: PASSED all manifest checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
