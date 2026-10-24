"""Orthographic and text normalization interfaces for Tangkhul language data.

Design Note:
    Tangkhul orthography utilizes Latin-based script with specific diacritics and
    glottal/tonal conventions (e.g., standard Ukhrul orthography). Normalization
    must preserve tone marks, diacritics, and dialect-specific spellings rather
    than flattening them destructively.
"""

from __future__ import annotations

import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize text using Unicode Normalization Form C (NFC).

    Preserves diacritics and combined characters without altering
    dialect-specific orthography.
    """
    return unicodedata.normalize("NFC", text.strip())


def sanitize_spacing(text: str) -> str:
    """Collapse extraneous internal whitespace while preserving line tokens."""
    return " ".join(text.split())
