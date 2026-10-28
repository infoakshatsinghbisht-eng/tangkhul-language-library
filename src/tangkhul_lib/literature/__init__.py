"""Literature domain module for Tangkhul Language Library.

Provides models, catalogues, and extraction utilities for Tangkhul poetry,
short stories, folktales, drama, oral narratives, and literary anthologies.
"""

from __future__ import annotations

from tangkhul_lib.literature.catalogue import LiteratureCatalogue
from tangkhul_lib.literature.extractor import LiteratureExtractor
from tangkhul_lib.literature.models import (
    VALID_LITERARY_GENRES,
    VALID_TEXT_AVAILABILITY,
    LiteraryRecord,
)

MODULE_NAME = "literature"

__all__ = [
    "MODULE_NAME",
    "VALID_LITERARY_GENRES",
    "VALID_TEXT_AVAILABILITY",
    "LiteraryRecord",
    "LiteratureCatalogue",
    "LiteratureExtractor",
]
