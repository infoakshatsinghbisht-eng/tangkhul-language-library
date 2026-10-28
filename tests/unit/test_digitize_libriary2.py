"""Unit tests for the ingestion, deduplication, and digitization of libriary2."""

from __future__ import annotations

import json
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = ROOT / "data" / "exports"


def test_digitized_json_files_integrity() -> None:
    """Verify that all JSON exports for libriary2 exist, are valid JSON, and have expected sizes."""
    complete_json = EXPORTS_DIR / "digitized_libriary2_complete.json"
    lit_json = EXPORTS_DIR / "digitized_libriary2_literature.json"
    idioms_json = EXPORTS_DIR / "digitized_libriary2_idioms.json"
    dict_json = EXPORTS_DIR / "digitized_libriary2_dictionary.json"
    grammar_json = EXPORTS_DIR / "digitized_libriary2_grammar.json"
    alphabet_json = EXPORTS_DIR / "digitized_libriary2_alphabet.json"
    audit_json = EXPORTS_DIR / "digitized_libriary2_deduplication_audit.json"

    json_files = [
        complete_json,
        lit_json,
        idioms_json,
        dict_json,
        grammar_json,
        alphabet_json,
        audit_json,
    ]
    for p in json_files:
        assert p.exists(), f"Missing exported JSON file: {p}"
        assert p.stat().st_size > 500, f"File {p} is suspiciously small: {p.stat().st_size} bytes"

    # Verify complete JSON structure
    data = json.loads(complete_json.read_text(encoding="utf-8"))
    assert "metadata" in data
    assert "deduplication_audit" in data
    assert "alphabet" in data
    assert "grammar" in data
    assert "literature" in data
    assert "idioms" in data
    assert "dictionary" in data

    # Literature checks: 2 unique works
    assert len(data["literature"]) == 2
    titles = [work["title_tangkhul"] for work in data["literature"]]
    assert "Luklam Phila-vawui Tui" in titles
    assert "Lu Khayei: Haorao Phanit Lu" in titles

    # Idioms checks: 21 unique (1 duplicate deleted)
    assert len(data["idioms"]) == 21
    idiom_ids = [i["id"] for i in data["idioms"]]
    assert "idiom_07" not in idiom_ids, "Duplicate idiom_07 should have been deleted"
    assert "idiom_01" in idiom_ids
    assert "idiom_22" in idiom_ids

    # Dictionary checks: 6772 unique (1 duplicate deleted)
    assert len(data["dictionary"]) == 6772
    # Verify no duplicate (tangkhul, english) pairs exist
    seen_pairs = set()
    for w in data["dictionary"]:
        pair = (w["tangkhul"].strip().lower(), w["english"].strip().lower())
        assert pair not in seen_pairs, f"Found unexpected duplicate pair: {pair}"
        seen_pairs.add(pair)


def test_digitized_pdf_files_integrity() -> None:
    """Verify that all PDF exports for libriary2 exist, are valid PDF 1.4, and are readable."""
    compendium_pdf = EXPORTS_DIR / "digitized_libriary2_compendium.pdf"
    lit_pdf = EXPORTS_DIR / "digitized_libriary2_literature.pdf"
    idioms_pdf = EXPORTS_DIR / "digitized_libriary2_idioms.pdf"
    grammar_pdf = EXPORTS_DIR / "digitized_libriary2_grammar_and_alphabet.pdf"

    for p in [compendium_pdf, lit_pdf, idioms_pdf, grammar_pdf]:
        assert p.exists(), f"Missing PDF export: {p}"
        reader = pypdf.PdfReader(str(p))
        assert len(reader.pages) >= 1

    # Compendium PDF must contain all sections (22 pages)
    comp_reader = pypdf.PdfReader(str(compendium_pdf))
    assert len(comp_reader.pages) == 22

    # Domain PDFs page counts
    lit_reader = pypdf.PdfReader(str(lit_pdf))
    assert len(lit_reader.pages) == 2

    idiom_reader = pypdf.PdfReader(str(idioms_pdf))
    assert len(idiom_reader.pages) == 4

    gram_reader = pypdf.PdfReader(str(grammar_pdf))
    assert len(gram_reader.pages) == 2


def test_deduplication_audit_report_integrity() -> None:
    """Verify that the deduplication audit report accurately records all purged duplicates."""
    audit_json = EXPORTS_DIR / "digitized_libriary2_deduplication_audit.json"
    audit = json.loads(audit_json.read_text(encoding="utf-8"))

    # Idioms audit
    ia = audit["idioms_audit"]
    assert ia["raw_count"] == 22
    assert ia["deleted_duplicates_count"] == 1
    assert ia["retained_count"] == 21
    assert any(d["id"] == "idiom_07" for d in ia["deleted_records"])
    assert "CULT-PROV-004" in ia["deleted_records"][0]["reason"]

    # Dictionary audit
    da = audit["dictionary_audit"]
    assert da["raw_count"] == 6773
    assert da["deleted_duplicates_count"] == 1
    assert da["retained_count"] == 6772
    assert da["deleted_records"][0]["tangkhul"].strip().lower() == "hili"
    assert da["deleted_records"][0]["english"].strip().lower() == "here"

    # Literature audit
    la = audit["literature_audit"]
    assert la["raw_count"] == 2
    assert la["deleted_duplicates_count"] == 0
    assert la["retained_count"] == 2
