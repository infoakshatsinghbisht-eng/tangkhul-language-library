"""Unit tests for newly digitalized Tangkhul research articles."""

from __future__ import annotations

import json
from pathlib import Path

from tangkhul_lib.articles.articles_data import get_all_articles_data
from tangkhul_lib.articles.catalogue import ArticleCatalogue, get_all_articles, get_article
from tangkhul_lib.articles.models import ArticleRecord

WORKSPACE = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = WORKSPACE / "data" / "exports" / "articles"


def test_articles_count_and_ids() -> None:
    """Verify that all 10 research articles are correctly registered."""
    articles = get_all_articles_data()
    assert len(articles) == 10
    ids = [a["id"] for a in articles]
    assert "ART-LING-001" in ids  # Mortensen & Keogh 2003
    assert "ART-LING-002" in ids  # Mortensen & Miller 2013
    assert "ART-LING-003" in ids  # Matisoff 1972
    assert "ART-LING-004" in ids  # Ahum 1997
    assert "ART-LING-005" in ids  # Gopal 2016
    assert "ART-LING-006" in ids  # Luikham, Zimik et al. 2020
    assert "ART-LING-007" in ids  # Arokianathan 1984
    assert "ART-LING-008" in ids  # Khayi & Subbarao 2012
    assert "ART-CULT-001" in ids  # Ruivah 1987 (Luira Phanit)
    assert "ART-CULT-002" in ids  # Luikham & Shimray 2004 (Hao Ngashan)


def test_article_record_model_validation() -> None:
    """Verify that ArticleRecord dataclass validates all records."""
    for art in get_all_articles_data():
        rec = ArticleRecord.from_dict(art)
        rec.validate()
        assert rec.id.startswith("ART-")
        assert len(rec.authors) >= 1
        assert len(rec.title) > 10
        assert len(rec.abstract) > 50


def test_articles_exported_files() -> None:
    """Verify JSON, PDF, and raw text exports exist on disk."""
    for art in get_all_articles_data():
        aid = art["id"]
        json_path = EXPORTS_DIR / f"{aid}.json"
        pdf_path = EXPORTS_DIR / f"{aid}.pdf"
        raw_path = WORKSPACE / "data" / "raw" / "articles" / f"{aid}.txt"

        assert json_path.is_file(), f"Missing JSON: {json_path}"
        assert pdf_path.is_file(), f"Missing PDF: {pdf_path}"
        assert raw_path.is_file(), f"Missing raw text: {raw_path}"

        assert json_path.stat().st_size > 2000
        assert pdf_path.stat().st_size > 2000

    # Master compendiums
    assert (WORKSPACE / "data" / "exports" / "articles.json").is_file()
    assert (WORKSPACE / "data" / "exports" / "articles.pdf").is_file()


def test_article_catalogue_search() -> None:
    """Verify search functionality across articles."""
    catalogue = ArticleCatalogue.load_default()
    assert len(catalogue.list_all()) == 10

    # Search by author
    mortensen_arts = catalogue.search(author="Mortensen")
    assert len(mortensen_arts) == 2

    # Search by subject
    ling_arts = catalogue.search(subject="Linguistics")
    assert len(ling_arts) >= 5

    # Search by query
    luira_arts = catalogue.search(query="Luira")
    assert len(luira_arts) >= 1
    assert luira_arts[0].id == "ART-CULT-001"

    # API function retrieval
    art = get_article("ART-LING-003")
    assert art is not None
    assert "Matisoff" in art["authors"][0]
