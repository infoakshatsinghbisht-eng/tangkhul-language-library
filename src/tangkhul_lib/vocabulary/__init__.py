"""Vocabulary management, normalization, deduplication, and provenance tracking.

This module defines the architectural interfaces for unified vocabulary collection
across all six domain modules (books, songs, dictionaries, culture, history, literature).
"""

from __future__ import annotations

__all__ = [
    "deduplication",
    "normalization",
    "provenance",
    "search",
]
