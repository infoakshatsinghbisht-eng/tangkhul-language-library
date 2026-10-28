"""
Unit tests for Volume II of Tangkhul Folk Riddles & Grand Compendium (400 Riddles).
Verifies JSON datasets, publication PDFs, and raw monograph archives.
"""

from __future__ import annotations

import json
from pathlib import Path

import pypdf

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"
RAW_DIR = WORKSPACE_ROOT / "data" / "raw" / "literature"


def test_volume2_riddles_json_structure() -> None:
    """Verify that tangkhul_more_folk_riddles.json exists with 100 valid entries."""
    for path in (
        EXPORTS_DIR / "tangkhul_more_folk_riddles.json",
        BUNDLED_DIR / "tangkhul_more_folk_riddles.json",
    ):
        assert path.exists(), f"File missing: {path}"
        data = json.loads(path.read_text(encoding="utf-8"))

        assert data["volume"] == 2
        assert data["total_riddles"] == 100
        assert data["identifier"] == "LIT-RIDD-004"
        assert len(data["sections"]) == 5

        riddles = data["riddles"]
        assert len(riddles) == 100

        for r in riddles:
            num = r["number"]
            assert 301 <= num <= 400
            assert r["tangkhul_riddle"].strip()
            assert r["english_translation"].strip()
            assert r["hindi_translation"].strip()
            assert r["answer_tangkhul"].strip()
            assert r["answer_english"].strip()
            assert r["answer_hindi"].strip()


def test_volume2_riddles_pdf_generation() -> None:
    """Verify that tangkhul_more_folk_riddles.pdf is a valid, readable multi-page document."""
    pdf_path = EXPORTS_DIR / "tangkhul_more_folk_riddles.pdf"
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 40000

    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 13

    first_page_text = reader.pages[0].extract_text()
    assert "Tangkhul" in first_page_text


def test_grand_compendium_400_riddles() -> None:
    """Verify the 400-riddle Grand Compendium JSON and PDF."""
    json_path = EXPORTS_DIR / "tangkhul_400_folk_riddles_grand_collection.json"
    assert json_path.exists()
    data = json.loads(json_path.read_text(encoding="utf-8"))

    assert data["total_riddles"] == 400
    assert len(data["riddles"]) == 400

    numbers = [r["number"] for r in data["riddles"]]
    assert numbers == list(range(1, 401))

    pdf_path = EXPORTS_DIR / "tangkhul_400_folk_riddles_grand_collection.pdf"
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 50


def test_volume2_raw_monograph_archive() -> None:
    """Verify raw literature archive LIT-RIDD-004.txt."""
    raw_path = RAW_DIR / "LIT-RIDD-004.txt"
    assert raw_path.exists()

    content = raw_path.read_text(encoding="utf-8")
    assert "LIT-RIDD-004" in content
    assert "[301] TANGKHUL:" in content
    assert "[400] TANGKHUL:" in content
    assert "END OF RECORD: LIT-RIDD-004" in content
    assert len(content.splitlines()) >= 600
