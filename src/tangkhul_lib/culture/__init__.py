"""Culture domain module for Tangkhul Language Library.

Preserves Tangkhul cultural heritage, customs, traditional festivals (Luira, Chumpha,
Mangkhap, Thisham), proverbs (Paotam/Chanjam), textile arts (Haora, Chonkhom),
rituals, and oral traditions with strict permission and consent controls.
"""

from __future__ import annotations

from tangkhul_lib.culture.catalogue import CultureCatalogue
from tangkhul_lib.culture.extractor import CultureExtractor
from tangkhul_lib.culture.models import VALID_CULTURE_CATEGORIES, CulturalRecord
from tangkhul_lib.storage.repositories import CultureRepository

MODULE_NAME = "culture"

__all__ = [
    "MODULE_NAME",
    "VALID_CULTURE_CATEGORIES",
    "CulturalRecord",
    "CultureCatalogue",
    "CultureExtractor",
    "CultureRepository",
]
