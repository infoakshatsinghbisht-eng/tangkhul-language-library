"""Dictionaries domain package for Tangkhul Language Library."""

from __future__ import annotations

from tangkhul_lib.dictionaries.catalogue import DictionaryCatalogue
from tangkhul_lib.dictionaries.extractor import DictionaryExtractor
from tangkhul_lib.dictionaries.models import (
    VALID_SOURCE_TYPES,
    DictionaryEntryRecord,
    DictionarySourceRecord,
)
from tangkhul_lib.storage.repositories import DictionaryRepository

MODULE_NAME = "dictionaries"

__all__ = [
    "MODULE_NAME",
    "VALID_SOURCE_TYPES",
    "DictionaryCatalogue",
    "DictionaryEntryRecord",
    "DictionaryExtractor",
    "DictionaryRepository",
    "DictionarySourceRecord",
]
