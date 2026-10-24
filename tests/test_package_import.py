"""Tests for package import, version attributes, and basic package integrity."""

from __future__ import annotations

import importlib


def test_package_import() -> None:
    """Verify that tangkhul_lib can be imported cleanly."""
    import tangkhul_lib

    assert hasattr(tangkhul_lib, "__version__")
    assert isinstance(tangkhul_lib.__version__, str)
    assert tangkhul_lib.__version__ == "0.1.0"


def test_submodules_import() -> None:
    """Verify that all architectural submodules can be imported without error."""
    submodules = [
        "tangkhul_lib.core",
        "tangkhul_lib.core.config",
        "tangkhul_lib.core.exceptions",
        "tangkhul_lib.core.models",
        "tangkhul_lib.vocabulary",
        "tangkhul_lib.vocabulary.search",
        "tangkhul_lib.vocabulary.normalization",
        "tangkhul_lib.vocabulary.deduplication",
        "tangkhul_lib.vocabulary.provenance",
        "tangkhul_lib.books",
        "tangkhul_lib.songs",
        "tangkhul_lib.dictionaries",
        "tangkhul_lib.culture",
        "tangkhul_lib.history",
        "tangkhul_lib.literature",
        "tangkhul_lib.storage",
        "tangkhul_lib.storage.database",
        "tangkhul_lib.storage.repositories",
        "tangkhul_lib.ingestion",
        "tangkhul_lib.ingestion.metadata_validation",
        "tangkhul_lib.ingestion.text_extraction",
        "tangkhul_lib.cli",
    ]
    for mod_name in submodules:
        mod = importlib.import_module(mod_name)
        assert mod is not None
