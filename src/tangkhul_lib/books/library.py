"""High-level library API for accessing complete cover-to-cover books in
the Tangkhul Language Library.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tangkhul_lib.books.builder import generate_book_pages_and_content
from tangkhul_lib.core.config import get_config
from tangkhul_lib.vocabulary.normalization import normalize_unicode


def _resolve_books_data_path() -> Path:
    """Find consolidated books JSON path, either in exports, package data, or manifest."""
    config = get_config()
    candidate_paths = [
        config.paths.data_dir / "exports" / "books.json",
        Path(__file__).resolve().parent.parent / "data" / "books.json",
    ]
    for p in candidate_paths:
        if p.is_file():
            return p
    return candidate_paths[1]


def get_all_books() -> list[dict[str, Any]]:
    """Retrieve all 23 catalogued books with complete cover-to-cover pages and chapters."""
    json_path = _resolve_books_data_path()
    if json_path.is_file():
        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) >= 20:
                    return data
        except Exception:
            pass

    # Fallback to generating on the fly from manifest
    config = get_config()
    manifest_file = config.paths.manifests_dir / "books.jsonl"
    books: list[dict[str, Any]] = []
    if manifest_file.is_file():
        with open(manifest_file, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    raw = json.loads(line)
                    books.append(generate_book_pages_and_content(raw))
    return books


def get_book(book_id: str) -> dict[str, Any] | None:
    """Retrieve a single book completely from cover to cover by its unique ID.

    Args:
        book_id: Book identifier (e.g. 'BK-ARCH-001', 'BK-HIST-001', 'BK-TLS-001').

    Returns:
        Complete book dictionary with metadata, front_matter, table_of_contents,
        chapters, pages (Page 1 to End Page), and back_matter; or None if not found.
    """
    clean_id = book_id.strip()
    config = get_config()

    # Check individual exported JSON first
    ind_path = config.paths.data_dir / "exports" / "books" / f"{clean_id}.json"
    if ind_path.is_file():
        try:
            with open(ind_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Check consolidated list
    for b in get_all_books():
        if b.get("id") == clean_id:
            return b

    return None


def get_book_pages(book_id: str) -> list[dict[str, Any]]:
    """Retrieve all pages (Page 1 to End Page) for a given book."""
    b = get_book(book_id)
    if b and "pages" in b:
        return b["pages"]
    return []


def get_book_page(book_id: str, page_number: int) -> dict[str, Any] | None:
    """Retrieve a specific page object from a book by its page number."""
    pages = get_book_pages(book_id)
    for p in pages:
        if p.get("page_number") == page_number:
            return p
    return None


def get_book_chapters(book_id: str) -> list[dict[str, Any]]:
    """Retrieve all chapters for a given book."""
    b = get_book(book_id)
    if b and "chapters" in b:
        return b["chapters"]
    return []


def get_book_chapter(book_id: str, chapter_number: int) -> dict[str, Any] | None:
    """Retrieve a specific chapter by its number (1-indexed)."""
    chapters = get_book_chapters(book_id)
    for ch in chapters:
        if ch.get("chapter_number") == chapter_number:
            return ch
    return None


def search_book_content(query: str, book_id: str | None = None) -> list[dict[str, Any]]:
    """Search text content across all pages and chapters in the library.

    Args:
        query: Search string (Tangkhul or English).
        book_id: Optional filter for a specific book ID.

    Returns:
        List of matching occurrences with book ID, page number, chapter, and text snippet.
    """
    results: list[dict[str, Any]] = []
    q_norm = normalize_unicode(query).lower().strip()
    if not q_norm:
        return results

    books = [get_book(book_id)] if book_id else get_all_books()

    for b in books:
        if not b:
            continue
        bid = b["id"]
        btitle = b["title"]

        for page in b.get("pages", []):
            pnum = page.get("page_number")
            ptype = page.get("page_type")
            page_text_lines = [
                l[2] if isinstance(l, (list, tuple)) and len(l) == 3 else str(l)
                for l in page.get("lines", [])
            ]
            content_str = (
                f"{page.get('tangkhul_content', '')} "
                f"{page.get('english_translation', '')} "
                f"{' '.join(page_text_lines)}"
            )
            content_norm = normalize_unicode(content_str).lower()

            if q_norm in content_norm:
                # Find matching line or snippet
                matching_snippet = ""
                for line_text in page_text_lines:
                    if q_norm in normalize_unicode(line_text).lower():
                        matching_snippet = line_text
                        break
                if not matching_snippet:
                    matching_snippet = page.get("tangkhul_content", "")[:120]

                results.append({
                    "book_id": bid,
                    "book_title": btitle,
                    "page_number": pnum,
                    "page_type": ptype,
                    "header": page.get("header"),
                    "snippet": matching_snippet,
                    "match_type": "page_content",
                })

    return results
