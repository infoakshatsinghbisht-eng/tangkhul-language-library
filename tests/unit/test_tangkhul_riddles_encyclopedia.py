"""Unit tests for the 300 Tangkhul Folk Riddles Encyclopedia (Kakhangahan Sangrah)."""

from __future__ import annotations

import json
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = ROOT / "data" / "exports"
RAW_DIR = ROOT / "data" / "raw" / "literature"
BUNDLED_DIR = ROOT / "src" / "tangkhul_lib" / "data"


def test_300_riddles_json_catalogs() -> None:
    """Verify that both consolidated and bundled JSON files for 300 folk riddles exist."""
    j1 = EXPORTS_DIR / "tangkhul_300_folk_riddles.json"
    j2 = BUNDLED_DIR / "tangkhul_300_folk_riddles.json"

    assert j1.exists(), f"Missing {j1}"
    assert j2.exists(), f"Missing {j2}"
    assert j1.stat().st_size > 150_000

    data = json.loads(j1.read_text(encoding="utf-8"))
    assert "metadata" in data
    assert "riddles" in data
    assert data["metadata"]["total_riddles"] == 300
    assert data["metadata"]["total_sections"] == 11
    assert len(data["riddles"]) == 300

    # Verify first, middle, and last riddle
    r1 = data["riddles"][0]
    assert r1["number"] == 1
    assert "Zingkum saikora kharei" in r1["tangkhul_riddle"]
    assert "Tara" in r1["answer_tangkhul"]

    r150 = data["riddles"][149]
    assert r150["number"] == 150
    assert "Zingkum saikora khangam" in r150["tangkhul_riddle"]
    assert "Khangre-khur" in r150["answer_tangkhul"]

    r300 = data["riddles"][299]
    assert r300["number"] == 300
    assert "Tangkhul Ram" in r300["answer_tangkhul"]

    # Check all 300 have non-empty fields
    for r in data["riddles"]:
        assert r["tangkhul_riddle"].strip()
        assert r["english_translation"].strip()
        assert r["hindi_translation"].strip()
        assert r["answer_tangkhul"].strip()
        assert r["answer_english"].strip()
        assert r["answer_hindi"].strip()
        assert 1 <= r["section_number"] <= 11


def test_300_riddles_pdf_publication() -> None:
    """Verify that the 17-page publication PDF exists, is valid PDF 1.4, and has 17 pages."""
    pdf_path = EXPORTS_DIR / "tangkhul_300_folk_riddles.pdf"
    assert pdf_path.exists(), f"Missing {pdf_path}"
    assert pdf_path.stat().st_size > 50_000

    reader = pypdf.PdfReader(str(pdf_path))
    msg = f"Expected 17 pages matching source document, got {len(reader.pages)}"
    assert len(reader.pages) == 17, msg


def test_300_riddles_raw_monograph() -> None:
    """Verify that the raw monograph LIT-RIDD-003.txt exists and has comprehensive content."""
    raw_path = RAW_DIR / "LIT-RIDD-003.txt"
    assert raw_path.exists(), f"Missing {raw_path}"

    lines = raw_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 1500, f"Expected >= 1500 lines for 300 riddles monograph, got {len(lines)}"

    content = "\n".join(lines)
    assert "300 TANGKHUL FOLK RIDDLES" in content
    assert "LIT-RIDD-003" in content
    assert "LITERARY THEMES & MOTIFS" in content
