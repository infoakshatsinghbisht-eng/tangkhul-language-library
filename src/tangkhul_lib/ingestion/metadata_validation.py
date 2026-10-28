"""Manifest schema and metadata validation for Tangkhul Language Library."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.core.models import (
    VALID_PERMISSION_STATUSES,
    VALID_RESOURCE_TYPES,
    VALID_VERIFICATION_STATUSES,
    ManifestRecord,
)


def validate_manifest_record(
    data: dict[str, Any],
    line_number: int | None = None,
) -> ManifestRecord:
    """Validate a single dictionary against the ManifestRecord schema.

    Raises:
        ManifestValidationError: If any required field is missing or invalid.
    """
    rec_id = data.get("id")
    if not rec_id or not isinstance(rec_id, str) or not rec_id.strip():
        raise ManifestValidationError(
            f"Missing or invalid 'id' on line {line_number or 'unknown'}",
            record_id=str(rec_id),
            line_number=line_number,
        )

    resource_type = data.get("resource_type")
    if resource_type not in VALID_RESOURCE_TYPES:
        raise ManifestValidationError(
            f"Invalid resource_type '{resource_type}' for record '{rec_id}'. "
            f"Expected one of: {sorted(VALID_RESOURCE_TYPES)}",
            record_id=rec_id,
            line_number=line_number,
        )

    title = data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        raise ManifestValidationError(
            f"Record '{rec_id}' has missing or empty 'title'.",
            record_id=rec_id,
            line_number=line_number,
        )

    permission_status = data.get("permission_status", "pending")
    if permission_status not in VALID_PERMISSION_STATUSES:
        raise ManifestValidationError(
            f"Invalid permission_status '{permission_status}' for record '{rec_id}'. "
            f"Expected one of: {sorted(VALID_PERMISSION_STATUSES)}",
            record_id=rec_id,
            line_number=line_number,
        )

    verification_status = data.get("verification_status", "unverified")
    if verification_status not in VALID_VERIFICATION_STATUSES:
        raise ManifestValidationError(
            f"Invalid verification_status '{verification_status}' for record '{rec_id}'. "
            f"Expected one of: {sorted(VALID_VERIFICATION_STATUSES)}",
            record_id=rec_id,
            line_number=line_number,
        )

    year = data.get("year")
    if year is not None and not isinstance(year, int):
        raise ManifestValidationError(
            f"Record '{rec_id}' year must be an integer, got: {type(year).__name__}",
            record_id=rec_id,
            line_number=line_number,
        )

    return ManifestRecord.from_dict(data)


def validate_manifest_file(file_path: Path) -> list[ManifestRecord]:
    """Validate a JSON Lines (.jsonl) manifest file.

    Returns:
        List of validated ManifestRecord instances.

    Raises:
        ManifestValidationError: If JSON is malformed or validation fails.
    """
    path = Path(file_path)
    if not path.is_file():
        raise ManifestValidationError(f"Manifest file not found: {path}")

    records: list[ManifestRecord] = []
    seen_ids: set[str] = set()

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

            if not isinstance(data, dict):
                raise ManifestValidationError(
                    f"Line {idx} in {path.name} is not a JSON object.",
                    line_number=idx,
                )

            record = validate_manifest_record(data, line_number=idx)

            if record.id in seen_ids:
                raise ManifestValidationError(
                    f"Duplicate record ID '{record.id}' found on line {idx} in {path.name}.",
                    record_id=record.id,
                    line_number=idx,
                )

            seen_ids.add(record.id)
            records.append(record)

    return records


def validate_all_manifests(manifest_dir: Path) -> dict[str, list[ManifestRecord]]:
    """Validate all JSON Lines manifests in a directory and enforce cross-manifest ID uniqueness.

    Returns:
        Mapping of manifest filename to list of validated ManifestRecord instances.

    Raises:
        ManifestValidationError: If any file fails validation or if a duplicate ID
            exists across different manifest files.
    """
    path = Path(manifest_dir)
    if not path.is_dir():
        raise ManifestValidationError(f"Manifest directory not found: {path}")

    manifest_files = sorted(path.glob("*.jsonl"))
    results: dict[str, list[ManifestRecord]] = {}
    global_id_map: dict[str, str] = {}

    for mf in manifest_files:
        file_records = validate_manifest_file(mf)
        for rec in file_records:
            if rec.id in global_id_map:
                prev_file = global_id_map[rec.id]
                raise ManifestValidationError(
                    f"Cross-manifest duplicate record ID '{rec.id}' in {mf.name}; "
                    f"already declared in {prev_file}.",
                    record_id=rec.id,
                )
            global_id_map[rec.id] = mf.name
        results[mf.name] = file_records

    return results
