"""Catalogue and search interfaces for Tangkhul research articles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tangkhul_lib.articles.articles_data import get_all_articles_data
from tangkhul_lib.articles.models import ArticleRecord
from tangkhul_lib.core.config import get_config


class ArticleCatalogue:
    """Catalogue managing Tangkhul research and cultural articles."""

    def __init__(self, records: list[ArticleRecord] | None = None) -> None:
        self._records = records or []
        self._by_id = {r.id: r for r in self._records}

    @classmethod
    def load_default(cls) -> ArticleCatalogue:
        """Load default catalogued articles."""
        data = get_all_articles_data()
        records = [ArticleRecord.from_dict(d) for d in data]
        return cls(records)

    def get_article(self, article_id: str) -> ArticleRecord | None:
        """Retrieve an article record by ID."""
        return self._by_id.get(article_id.strip())

    def search(
        self,
        query: str | None = None,
        author: str | None = None,
        subject: str | None = None,
    ) -> list[ArticleRecord]:
        """Search articles by query string, author, or subject."""
        results = list(self._records)
        if query:
            q = query.lower()
            results = [
                r for r in results
                if q in r.title.lower()
                or any(q in t.lower() for t in r.alternate_titles)
                or q in r.abstract.lower()
                or any(q in k.lower() for k in r.keywords)
            ]
        if author:
            a = author.lower()
            results = [r for r in results if any(a in auth.lower() for auth in r.authors)]
        if subject:
            s = subject.lower()
            results = [r for r in results if s in r.subject.lower()]
        return results

    def list_all(self) -> list[ArticleRecord]:
        """List all catalogued articles."""
        return list(self._records)


def get_all_articles() -> list[dict[str, Any]]:
    """Retrieve all 10 digitized articles with complete content and pages."""
    config = get_config()
    consolidated_json = config.paths.data_dir / "exports" / "articles.json"
    if consolidated_json.is_file():
        try:
            with open(consolidated_json, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) == 10:
                    return data
        except Exception:
            pass
    return get_all_articles_data()


def get_article(article_id: str) -> dict[str, Any] | None:
    """Retrieve a single article by ID with full content and pages."""
    clean_id = article_id.strip()
    config = get_config()
    ind_json = config.paths.data_dir / "exports" / "articles" / f"{clean_id}.json"
    if ind_json.is_file():
        try:
            with open(ind_json, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    for a in get_all_articles_data():
        if a.get("id") == clean_id:
            return a
    return None
