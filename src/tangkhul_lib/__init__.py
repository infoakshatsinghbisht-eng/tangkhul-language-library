"""Tangkhul Language Library.

A modular Python library for Tangkhul language preservation, linguistic research,
complete cover-to-cover book access, vocabulary extraction, and cultural documentation.
"""

from __future__ import annotations

from tangkhul_lib.books.library import (
    get_all_books,
    get_book,
    get_book_chapter,
    get_book_chapters,
    get_book_page,
    get_book_pages,
    search_book_content,
)
from tangkhul_lib.vocabulary.bundled import (
    get_corpus_database,
    get_dictionary,
    get_vocabulary,
    get_words,
    load_bundled_vocabulary,
    lookup,
    search,
)

__version__ = "0.1.0"
__author__ = "Tangkhul Language Preservation Project Contributors"

__all__ = [
    "__author__",
    "__version__",
    "get_all_books",
    "get_book",
    "get_book_chapter",
    "get_book_chapters",
    "get_book_page",
    "get_book_pages",
    "get_corpus_database",
    "get_dictionary",
    "get_vocabulary",
    "get_words",
    "load_bundled_vocabulary",
    "lookup",
    "search",
    "search_book_content",
]
