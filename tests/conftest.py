"""Test fixtures and pytest configuration for Tangkhul Language Library."""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from tangkhul_lib.core.config import LibraryConfig, LibraryPaths


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory structure mimicking the project root."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        (root / "data" / "manifests").mkdir(parents=True)
        (root / "data" / "raw").mkdir(parents=True)
        (root / "data" / "database").mkdir(parents=True)
        yield root


@pytest.fixture
def mock_config(temp_project_dir: Path) -> LibraryConfig:
    """Provide a LibraryConfig pointing to temporary paths."""
    return LibraryConfig(paths=LibraryPaths(root_dir=temp_project_dir))
