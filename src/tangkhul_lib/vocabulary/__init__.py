"""Vocabulary management, normalization, deduplication, and provenance tracking.

This module defines the architectural interfaces for unified vocabulary collection
across all six domain modules (books, songs, dictionaries, culture, history, literature).
"""

from tangkhul_lib.vocabulary.bundled import (
    get_corpus_database,
    get_dictionary,
    get_vocabulary,
    get_words,
    load_bundled_vocabulary,
    lookup,
    search,
)

__all__ = [
    "bundled",
    "deduplication",
    "enrichment",
    "get_corpus_database",
    "get_dictionary",
    "get_vocabulary",
    "get_words",
    "load_bundled_vocabulary",
    "lookup",
    "normalization",
    "phonetic",
    "provenance",
    "review",
    "search",
]
