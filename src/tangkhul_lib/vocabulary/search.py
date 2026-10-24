"""Vocabulary search interfaces for Tangkhul Language Library.

Planned Feature:
    Full-text and phonetic search across Tangkhul headwords, English definitions,
    dialectal variations, and source contexts. Not yet operational in Step 1.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tangkhul_lib.core.models import VocabularyEntry


class VocabularySearchEngine:
    """Interface for searching unified Tangkhul vocabulary records."""

    def __init__(self) -> None:
        self._is_ready = False

    def search_headword(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching headword or alternative spellings.

        Note:
            Planned interface. Implementation will be integrated once vocabulary
            storage and indexing are populated in subsequent steps.
        """
        raise NotImplementedError(
            "Vocabulary searching is a planned feature and is not yet operational in Step 1."
        )

    def search_meaning(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching glosses, translations, or definitions."""
        raise NotImplementedError(
            "Vocabulary searching is a planned feature and is not yet operational in Step 1."
        )
