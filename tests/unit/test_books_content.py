"""Unit tests for complete cover-to-cover book access and content search."""

from __future__ import annotations

import json
from pathlib import Path

from tangkhul_lib.books.content import BookChapter, BookPage
from tangkhul_lib.books.library import (
    get_all_books,
    get_book,
    get_book_chapter,
    get_book_chapters,
    get_book_page,
    get_book_pages,
    search_book_content,
)


def test_book_content_models() -> None:
    """Test BookPage and BookChapter data classes."""
    page = BookPage(
        page_number=1,
        page_type="cover",
        header="Test Header",
        title="Test Book",
        lines=["Line 1", "Line 2"],
        tangkhul_content="Tangkhul text",
        english_translation="English text",
    )
    p_dict = page.to_dict()
    assert p_dict["page_number"] == 1
    assert p_dict["page_type"] == "cover"

    ch = BookChapter(
        chapter_number=1,
        title="Chapter 1: Test",
        page_start=4,
        page_end=5,
        summary="Chapter summary",
        tangkhul_text="Tangkhul chapter text",
        english_translation="English chapter translation",
    )
    c_dict = ch.to_dict()
    assert c_dict["chapter_number"] == 1
    assert c_dict["page_start"] == 4


def test_get_all_books() -> None:
    """Test get_all_books retrieves all 35 catalogued books with full content."""
    books = get_all_books()
    assert len(books) == 35
    for b in books:
        assert "id" in b
        assert "title" in b
        assert "front_matter" in b
        assert "table_of_contents" in b
        assert "chapters" in b
        assert len(b["chapters"]) >= 6
        assert "pages" in b
        assert len(b["pages"]) >= 18
        assert "back_matter" in b
        assert b["total_pages"] >= 18


def test_get_book_by_id() -> None:
    """Test get_book for specific historical and curriculum volumes."""
    arch = get_book("BK-ARCH-001")
    assert arch is not None
    assert "Grierson" in arch["authors"][0]
    assert arch["total_pages"] == 20
    assert arch["total_chapters"] == 7

    hist = get_book("BK-HIST-001")
    assert hist is not None
    assert "Pettigrew" in hist["authors"][0]
    assert hist["total_pages"] == 20

    tls = get_book("BK-TLS-001")
    assert tls is not None
    assert tls["title"] == "Wontui Tangkhul"
    assert tls["total_pages"] == 22

    # Nonexistent book returns None
    missing = get_book("BK-NONEXISTENT")
    assert missing is None


def test_get_book_pages_and_page() -> None:
    """Test page retrieval and individual page lookup."""
    pages = get_book_pages("BK-ARCH-001")
    assert len(pages) == 20

    # Page 1: Cover
    p1 = pages[0]
    assert p1["page_number"] == 1
    assert p1["page_type"] == "cover"

    # Page 2: Front Matter
    p2 = pages[1]
    assert p2["page_number"] == 2
    assert p2["page_type"] == "front_matter"

    # Page 3: TOC
    p3 = pages[2]
    assert p3["page_number"] == 3
    assert p3["page_type"] == "table_of_contents"

    # Specific page query
    p14 = get_book_page("BK-ARCH-001", 14)
    assert p14 is not None
    assert "Prodigal Son" in p14["header"]
    assert "mayarnaowon" in p14["tangkhul_content"].lower()

    # Nonexistent page
    p999 = get_book_page("BK-ARCH-001", 999)
    assert p999 is None


def test_get_book_chapters_and_chapter() -> None:
    """Test chapter retrieval and chapter-specific queries."""
    chapters = get_book_chapters("BK-ARCH-001")
    assert len(chapters) == 7

    ch6 = get_book_chapter("BK-ARCH-001", 6)
    assert ch6 is not None
    assert "Prodigal Son" in ch6["title"]
    assert "mayarnaowon khani leiyi" in ch6["tangkhul_text"]
    assert len(ch6["vocabulary"]) >= 3

    # Nonexistent chapter
    ch99 = get_book_chapter("BK-ARCH-001", 99)
    assert ch99 is None


def test_search_book_content() -> None:
    """Test searching full text across book pages and chapters."""
    results = search_book_content("prodigal")
    assert len(results) >= 2
    assert any(r["book_id"] == "BK-ARCH-001" for r in results)

    # Scoped search to a specific book
    results_scoped = search_book_content("mayarnaowon", book_id="BK-ARCH-001")
    assert len(results_scoped) >= 1
    assert all(r["book_id"] == "BK-ARCH-001" for r in results_scoped)

    # Empty query returns empty list
    assert search_book_content("") == []


def test_exported_files_integrity() -> None:
    """Verify that export files on disk are complete, valid, and match expectations."""
    root = Path(__file__).resolve().parent.parent.parent
    books_json = root / "data" / "exports" / "books.json"
    assert books_json.is_file()

    with open(books_json, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 35

    # Check that individual JSONs exist for all 35 books
    for b in data:
        ind_json = root / "data" / "exports" / "books" / f"{b['id']}.json"
        assert ind_json.is_file(), f"Missing individual JSON for {b['id']}"
        ind_pdf = root / "data" / "exports" / "books" / f"{b['id']}.pdf"
        assert ind_pdf.is_file(), f"Missing individual PDF for {b['id']}"
        assert ind_pdf.stat().st_size > 1000

    # Check consolidated PDF
    books_pdf = root / "data" / "exports" / "books.pdf"
    assert books_pdf.is_file()
    assert books_pdf.stat().st_size > 50000
