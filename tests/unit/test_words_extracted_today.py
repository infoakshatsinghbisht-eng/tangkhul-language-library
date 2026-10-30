"""Unit tests for words extracted today from newly digitalized books and articles."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = WORKSPACE / "data" / "exports"
DB_PATH = WORKSPACE / "data" / "database" / "tangkhul_corpus.sqlite"


def test_today_words_json_integrity() -> None:
    """Verify that JSON export exists, is valid, and contains expected metadata and words."""
    json_path = EXPORTS_DIR / "tangkhul_words_extracted_today.json"
    assert json_path.is_file(), f"Missing {json_path}"

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_unique_words"] == 2566
    assert data["total_tokens"] >= 12000
    assert len(data["words"]) == 2566

    # Check alias and direct array format
    alias_path = EXPORTS_DIR / "words_extracted_today.json"
    assert alias_path.is_file()
    direct_array_path = EXPORTS_DIR / "extracted_words.json"
    assert direct_array_path.is_file()
    with open(direct_array_path, encoding="utf-8") as f:
        direct_words = json.load(f)
    assert len(direct_words) == 2566

    # Check key-value dictionary format
    dict_path = EXPORTS_DIR / "tangkhul_words_dictionary.json"
    assert dict_path.is_file()
    with open(dict_path, encoding="utf-8") as f:
        dict_data = json.load(f)
    assert len(dict_data) == 2566
    assert "kala" in dict_data

    # Check top word
    top_word = data["words"][0]
    assert top_word["rank"] == 1
    assert top_word["word"] == "kala"
    assert "और" in top_word["meaning_hi"]

    # Check that novels, biographies, translations, and articles are represented
    assert any(w["is_novel_vocab"] for w in data["words"])
    assert any(w["is_biography_vocab"] for w in data["words"])
    assert any(w["is_translation_vocab"] for w in data["words"])
    assert any(w["is_article_vocab"] for w in data["words"])


def test_today_words_csv_and_tsv_integrity() -> None:
    """Verify that CSV, TSV, PDF, and ODF files exist on disk with valid file size."""
    csv_path = EXPORTS_DIR / "tangkhul_words_extracted_today.csv"
    tsv_path = EXPORTS_DIR / "tangkhul_words_extracted_today.tsv"
    pdf_path = EXPORTS_DIR / "tangkhul_words_extracted_today.pdf"
    odt_path = EXPORTS_DIR / "tangkhul_words_extracted_today.odt"
    md_path = EXPORTS_DIR / "WORDS_EXTRACTED_TODAY_REPORT.md"

    assert csv_path.is_file()
    assert tsv_path.is_file()
    assert pdf_path.is_file()
    assert odt_path.is_file()
    assert md_path.is_file()

    assert csv_path.stat().st_size > 50000
    assert tsv_path.stat().st_size > 50000
    assert pdf_path.stat().st_size > 100000
    assert odt_path.stat().st_size > 50000
    assert md_path.stat().st_size > 5000


def test_today_words_sqlite_table() -> None:
    """Verify that table 'words_extracted_today' exists in SQLite database and has 2566 rows."""
    assert DB_PATH.is_file()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    count = cur.execute("SELECT count(*) FROM words_extracted_today").fetchone()[0]
    assert count == 2566

    # Query for specific novel terms
    res = cur.execute("SELECT word, meaning_en, meaning_hi FROM words_extracted_today WHERE word = 'kala'").fetchone()
    assert res is not None
    assert res[0] == "kala"
    assert "conjunction" in res[1].lower()

    # Query for novel and biography flag
    novel_count = cur.execute("SELECT count(*) FROM words_extracted_today WHERE is_novel = 1").fetchone()[0]
    assert novel_count >= 500

    biog_count = cur.execute("SELECT count(*) FROM words_extracted_today WHERE is_biography = 1").fetchone()[0]
    assert biog_count >= 400

    conn.close()

