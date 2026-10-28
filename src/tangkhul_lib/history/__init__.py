"""History domain module for Tangkhul Language Library.

Preserves Tangkhul community history, ancestral migration traditions (e.g., Makhel),
historical settlements, prominent figures, language documentation milestones,
and chronologically ordered timelines with strict provenance and source attribution.
"""

from __future__ import annotations

from tangkhul_lib.history.catalogue import HistoryCatalogue
from tangkhul_lib.history.extractor import HistoryExtractor
from tangkhul_lib.history.models import (
    VALID_EVIDENCE_TYPES,
    VALID_HISTORY_RECORD_TYPES,
    HistoricalRecord,
)
from tangkhul_lib.storage.repositories import HistoryRepository

MODULE_NAME = "history"

__all__ = [
    "MODULE_NAME",
    "VALID_EVIDENCE_TYPES",
    "VALID_HISTORY_RECORD_TYPES",
    "HistoricalRecord",
    "HistoryCatalogue",
    "HistoryExtractor",
    "HistoryRepository",
]
