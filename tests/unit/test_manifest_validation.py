"""Unit tests for JSON Lines manifest schema validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.ingestion.metadata_validation import (
    validate_manifest_file,
    validate_manifest_record,
)


def test_valid_manifest_record() -> None:
    data = {
        "id": "BK-0001",
        "resource_type": "books",
        "title": "Tangkhul Primer",
        "creator": "Linguistic Researcher",
        "year": 1920,
        "language": "Tangkhul",
        "permission_status": "public_domain",
        "verification_status": "verified",
    }
    rec = validate_manifest_record(data)
    assert rec.id == "BK-0001"
    assert rec.year == 1920


def test_missing_id_raises_error() -> None:
    data = {
        "resource_type": "books",
        "title": "Tangkhul Primer",
    }
    with pytest.raises(ManifestValidationError, match="Missing or invalid 'id'"):
        validate_manifest_record(data)


def test_invalid_resource_type_raises_error() -> None:
    data = {
        "id": "BK-0001",
        "resource_type": "invalid_type",
        "title": "Tangkhul Primer",
    }
    with pytest.raises(ManifestValidationError, match="Invalid resource_type"):
        validate_manifest_record(data)


def test_empty_title_raises_error() -> None:
    data = {
        "id": "BK-0001",
        "resource_type": "books",
        "title": "   ",
    }
    with pytest.raises(ManifestValidationError, match="missing or empty 'title'"):
        validate_manifest_record(data)


def test_validate_manifest_file(tmp_path: Path) -> None:
    manifest_file = tmp_path / "test_manifest.jsonl"
    lines = [
        json.dumps({
            "id": "BK-0001",
            "resource_type": "books",
            "title": "Tangkhul Primer",
            "year": 1920,
            "permission_status": "public_domain",
            "verification_status": "verified",
        }),
        json.dumps({
            "id": "BK-0002",
            "resource_type": "books",
            "title": "Tangkhul Reader",
            "year": 1925,
            "permission_status": "permitted",
            "verification_status": "unverified",
        }),
    ]
    manifest_file.write_text("\n".join(lines), encoding="utf-8")

    records = validate_manifest_file(manifest_file)
    assert len(records) == 2
    assert records[0].id == "BK-0001"
    assert records[1].id == "BK-0002"


def test_validate_manifest_file_catches_duplicate_ids(tmp_path: Path) -> None:
    manifest_file = tmp_path / "duplicate_manifest.jsonl"
    lines = [
        json.dumps({
            "id": "BK-0001",
            "resource_type": "books",
            "title": "Book 1",
        }),
        json.dumps({
            "id": "BK-0001",
            "resource_type": "books",
            "title": "Book 2",
        }),
    ]
    manifest_file.write_text("\n".join(lines), encoding="utf-8")

    with pytest.raises(ManifestValidationError, match="Duplicate record ID"):
        validate_manifest_file(manifest_file)
