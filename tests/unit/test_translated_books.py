"""Unit tests for newly digitalized translated books into Tangkhul Naga."""

from __future__ import annotations

import json
from pathlib import Path

from tangkhul_lib.books.library import get_all_books, get_book
from tangkhul_lib.books.translated_books_data import get_all_translated_books

WORKSPACE = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = WORKSPACE / "data" / "exports" / "books"


def test_translated_books_count() -> None:
    """Verify that all 10 translated books are defined and loadable."""
    translated = get_all_translated_books()
    assert len(translated) == 10
    ids = [b["id"] for b in translated]
    assert "BK-TRNS-001" in ids  # New Testament 1927
    assert "BK-TRNS-002" in ids  # Matthew 1907
    assert "BK-TRNS-003" in ids  # Mark 1909
    assert "BK-TRNS-004" in ids  # Genesis
    assert "BK-TRNS-005" in ids  # Psalms
    assert "BK-TRNS-006" in ids  # Pilgrim's Progress
    assert "BK-TRNS-007" in ids  # Aesop's Fables
    assert "BK-TRNS-008" in ids  # Tagore's Gitanjali
    assert "BK-TRNS-009" in ids  # World Stories
    assert "BK-TRNS-010" in ids  # Constitution Primer


def test_translated_books_structure() -> None:
    """Verify chapters, pages, vocabulary, and grammar in translated books."""
    translated = get_all_translated_books()
    for b in translated:
        assert b["id"].startswith("BK-TRNS-")
        assert len(b["title"]) > 5
        assert len(b["chapters"]) >= 4
        assert len(b["pages"]) >= 16
        assert b["total_pages"] >= 16
        assert b["total_chapters"] >= 4
        assert b["total_words"] > 400

        # Check first chapter
        ch1 = b["chapters"][0]
        assert ch1["chapter_number"] == 1
        assert len(ch1["tangkhul_text"]) > 40
        assert len(ch1["english_translation"]) > 40
        assert len(ch1["vocabulary"]) >= 2


def test_translated_books_exported_files() -> None:
    """Verify that JSON, PDF, and raw text files exist for all translated books."""
    for b in get_all_translated_books():
        bid = b["id"]
        json_path = EXPORTS_DIR / f"{bid}.json"
        pdf_path = EXPORTS_DIR / f"{bid}.pdf"
        raw_path = WORKSPACE / "data" / "raw" / "books" / f"{bid}.txt"

        assert json_path.is_file(), f"Missing JSON export: {json_path}"
        assert pdf_path.is_file(), f"Missing PDF export: {pdf_path}"
        assert raw_path.is_file(), f"Missing raw text: {raw_path}"

        assert json_path.stat().st_size > 5000
        assert pdf_path.stat().st_size > 5000
        assert raw_path.stat().st_size > 1000

        # Verify JSON content
        data = json.load(open(json_path, encoding="utf-8"))
        assert data["id"] == bid
        assert len(data["pages"]) >= 16


def test_get_book_retrieval_for_translations() -> None:
    """Verify that get_book retrieves translated volumes via library API."""
    nt = get_book("BK-TRNS-001")
    assert nt is not None
    assert "New Testament" in nt["title"]
    assert len(nt["chapters"]) == 7

    aesop = get_book("BK-TRNS-007")
    assert aesop is not None
    assert "Aesop" in aesop["title"]
