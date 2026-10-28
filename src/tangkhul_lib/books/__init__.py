"""Books domain module for Tangkhul Language Library.

Provides cataloguing, metadata management, duplicate detection, permitted text extraction,
and complete cover-to-cover book access (from page 1 to end page, all chapters and content).
"""

from __future__ import annotations

from tangkhul_lib.books.catalogue import BookCatalogue
from tangkhul_lib.books.content import BookChapter, BookPage, BookSection, FullBookDocument
from tangkhul_lib.books.extractor import BookTextExtractor
from tangkhul_lib.books.library import (
    get_all_books,
    get_book,
    get_book_chapter,
    get_book_chapters,
    get_book_page,
    get_book_pages,
    search_book_content,
)
from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.storage.repositories import BookRepository

MODULE_NAME = "books"

__all__ = [
    "MODULE_NAME",
    "BookCatalogue",
    "BookChapter",
    "BookPage",
    "BookRecord",
    "BookRepository",
    "BookSection",
    "BookTextExtractor",
    "FullBookDocument",
    "get_all_books",
    "get_book",
    "get_book_chapter",
    "get_book_chapters",
    "get_book_page",
    "get_book_pages",
    "search_book_content",
]
