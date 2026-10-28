"""Data models and interfaces for complete cover-to-cover books in Tangkhul Language Library."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class BookPage:
    """Represents an individual physical or digital page of a book from page 1 to end page."""

    page_number: int
    # e.g., 'cover', 'front_matter', 'table_of_contents', 'chapter', 'reading', 'back_matter'
    page_type: str

    header: str
    title: str | None = None
    lines: list[str] = field(default_factory=list)
    tangkhul_content: str = ""
    english_translation: str = ""
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BookSection:
    """Represents a specific subsection within a book chapter."""

    section_number: str
    title: str
    tangkhul_text: str
    english_translation: str
    linguistic_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BookChapter:
    """Represents a complete chapter within a book."""

    chapter_number: int
    title: str
    page_start: int
    page_end: int
    summary: str
    sections: list[dict[str, Any]] = field(default_factory=list)
    tangkhul_text: str = ""
    english_translation: str = ""
    vocabulary: list[dict[str, str]] = field(default_factory=list)
    grammar_points: list[str] = field(default_factory=list)
    comprehension_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class FullBookDocument:
    """Comprehensive cover-to-cover book document including all pages and chapters."""

    id: str
    title: str
    alternate_titles: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    editors: list[str] = field(default_factory=list)
    publisher: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    subject: str | None = None
    educational_level: str | None = None
    language: str = "Tangkhul"
    dialect: str | None = None
    isbn: str | None = None
    source_url: str | None = None
    source_identifier: str | None = None
    license: str | None = None
    permission_status: str = "pending"
    access_status: str = "metadata_only"
    verification_status: str = "unverified"
    notes: str | None = None
    front_matter: dict[str, Any] = field(default_factory=dict)
    table_of_contents: list[dict[str, Any]] = field(default_factory=list)
    chapters: list[dict[str, Any]] = field(default_factory=list)
    pages: list[dict[str, Any]] = field(default_factory=list)
    back_matter: dict[str, Any] = field(default_factory=dict)
    total_pages: int = 0
    total_chapters: int = 0
    total_words: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
