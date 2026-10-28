from __future__ import annotations

import json
from pathlib import Path

import pypdf

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"


def test_linguistic_encyclopedia_json_structure() -> None:
    """Verify that the linguistic encyclopedia JSON exists and has all required modules."""
    for p in (
        EXPORTS_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.json",
        BUNDLED_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.json",
    ):
        assert p.exists(), f"File missing: {p}"
        data = json.load(open(p, encoding="utf-8"))

        sections = data["sections"]
        assert "1_number_system" in sections
        assert "2_calendar_and_time" in sections
        assert "3_traditional_measurements" in sections
        assert "4_kinship_terminology" in sections
        assert "5_conversational_phrases" in sections

        # Test Number System
        num_sys = sections["1_number_system"]
        assert len(num_sys["cardinal_numbers"]) == 100
        assert len(num_sys["higher_numbers"]) >= 6
        assert len(num_sys["ordinal_numbers"]) >= 10
        assert len(num_sys["multiplicative_and_distributive"]) >= 10
        assert len(num_sys["fractions"]) >= 4
        assert len(num_sys["numeral_classifiers"]) >= 6

        # Check numbers 1 to 100 sequence
        nums = [c["number"] for c in num_sys["cardinal_numbers"]]
        assert nums == list(range(1, 101))

        # Test Lunar Calendar
        cal = sections["2_calendar_and_time"]
        assert len(cal["lunar_months"]) == 12
        assert len(cal["seasons"]) == 4
        assert len(cal["day_and_night_divisions"]) == 11

        # Test Measurements
        meas = sections["3_traditional_measurements"]
        assert len(meas["linear_measures"]) == 5
        assert len(meas["capacity_measures"]) == 5
        assert len(meas["land_measures"]) >= 1

        # Test Kinship
        kin = sections["4_kinship_terminology"]
        assert len(kin) == 22

        # Test Conversations
        conv = sections["5_conversational_phrases"]
        assert len(conv) == 18


def test_linguistic_encyclopedia_pdf_generation() -> None:
    """Verify that the linguistic encyclopedia PDF is valid and has 8 pages."""
    pdf_path = EXPORTS_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.pdf"
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 20000

    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 8

    p1_text = reader.pages[0].extract_text()
    assert "NUMBER SYSTEM" in p1_text
