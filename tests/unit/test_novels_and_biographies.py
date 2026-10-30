"""Unit tests for newly digitalized Tangkhul Novels and Biographies."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.books.library import (
    get_all_books,
    get_book,
    get_book_chapter,
    get_book_page,
    search_book_content,
)
from tangkhul_lib.books.novels_and_biographies_data import (
    get_all_novels_and_biographies,
    get_bk_biog_001_bob_khathing,
    get_bk_novl_001_shimreishang,
)

WORKSPACE = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = WORKSPACE / "data" / "exports" / "books"


def test_novels_and_biographies_specs() -> None:
    """Verify that all 10 novels and biographies load with complete structure."""
    books = get_all_novels_and_biographies()
    assert len(books) == 10

    novel_ids = [b["id"] for b in books if b["id"].startswith("BK-NOVL-")]
    biog_ids = [b["id"] for b in books if b["id"].startswith("BK-BIOG-")]

    assert len(novel_ids) == 5
    assert len(biog_ids) == 5

    assert "BK-NOVL-001" in novel_ids  # Shimreishang kala Maitonphi
    assert "BK-NOVL-002" in novel_ids  # Chamthei
    assert "BK-NOVL-003" in novel_ids  # Shongza
    assert "BK-NOVL-004" in novel_ids  # Wungram Okthot
    assert "BK-NOVL-005" in novel_ids  # Yarra

    assert "BK-BIOG-001" in biog_ids   # Major Bob Khathing
    assert "BK-BIOG-002" in biog_ids   # Rev. William Pettigrew
    assert "BK-BIOG-003" in biog_ids   # Rishang Keishing
    assert "BK-BIOG-004" in biog_ids   # Rowland Suisa
    assert "BK-BIOG-005" in biog_ids   # Luingam Luikham


def test_novel_001_content_structure() -> None:
    """Verify detailed contents of classic epic novel Shimreishang kala Maitonphi."""
    novel = get_bk_novl_001_shimreishang()
    assert novel["id"] == "BK-NOVL-001"
    assert "Shimreishang" in novel["title"]
    assert novel["total_pages"] == 16
    assert novel["total_chapters"] == 4
    assert len(novel["chapters"]) == 4

    # Check chapters have Tangkhul text and English translation
    for ch in novel["chapters"]:
        assert len(ch["tangkhul_text"]) > 100
        assert len(ch["english_translation"]) > 100
        assert len(ch["vocabulary"]) >= 3
        assert len(ch["grammar_notes"]) >= 2
        assert len(ch["exercises"]) >= 2


def test_biography_001_content_structure() -> None:
    """Verify detailed contents of Major Bob Khathing biography."""
    biog = get_bk_biog_001_bob_khathing()
    assert biog["id"] == "BK-BIOG-001"
    assert "Khathing" in biog["title"]
    assert biog["total_pages"] == 16
    assert biog["total_chapters"] == 4

    # Check chapters
    for ch in biog["chapters"]:
        assert "tangkhul_text" in ch
        assert "english_translation" in ch
        assert len(ch["vocabulary"]) >= 3


def test_exported_files_for_novels_and_biographies() -> None:
    """Verify that all JSON, PDF, and raw txt files exist on disk."""
    for b in get_all_novels_and_biographies():
        bid = b["id"]
        raw_txt = WORKSPACE / "data" / "raw" / "books" / f"{bid}.txt"
        json_file = EXPORTS_DIR / f"{bid}.json"
        pdf_file = EXPORTS_DIR / f"{bid}.pdf"

        assert raw_txt.is_file(), f"Missing raw txt for {bid}"
        assert json_file.is_file(), f"Missing JSON export for {bid}"
        assert pdf_file.is_file(), f"Missing PDF export for {bid}"

        assert raw_txt.stat().st_size > 1000
        assert json_file.stat().st_size > 5000
        assert pdf_file.stat().st_size > 10000


def test_library_integration_and_search() -> None:
    """Verify that novels and biographies are accessible via the main library API."""
    novel = get_book("BK-NOVL-001")
    assert novel is not None
    assert "Shimreishang" in novel["title"]

    biog = get_book("BK-BIOG-001")
    assert biog is not None
    assert "Khathing" in biog["title"]

    # Search for terms in novel & biography
    results_novel = search_book_content("Maitonphi")
    assert len(results_novel) >= 1
    assert any(r["book_id"] == "BK-NOVL-001" for r in results_novel)

    results_tawang = search_book_content("Tawang")
    assert len(results_tawang) >= 1
    assert any(r["book_id"] == "BK-BIOG-001" for r in results_tawang)

