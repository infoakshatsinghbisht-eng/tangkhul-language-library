from __future__ import annotations

import json
from pathlib import Path

import pypdf

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"


def test_master_dictionary_deduplication_integrity() -> None:
    """Verify that the master dictionary has exactly 6,480 deduplicated unique words."""
    for p in (
        EXPORTS_DIR / "tangkhul_master_dictionary_deduplicated.json",
        BUNDLED_DIR / "tangkhul_master_dictionary_deduplicated.json",
    ):
        assert p.exists(), f"Missing file: {p}"
        data = json.load(open(p, encoding="utf-8"))
        assert data["total_entries"] == 6480
        entries = data["entries"]
        assert len(entries) == 6480

        seen_normalized = set()
        for e in entries:
            norm = e["tangkhul_normalized"]
            assert norm not in seen_normalized, f"Duplicate found: {norm}"
            seen_normalized.add(norm)
            assert e["tangkhul"].strip()
            assert e["english"].strip()
            assert e["hindi"].strip()
            assert e["pos"] in (
                "noun",
                "verb",
                "adjective",
                "adverb",
                "preposition",
                "pronoun",
                "interjection",
                "conjunction",
                "phrase",
                "numeral",
            )

    pdf_path = EXPORTS_DIR / "tangkhul_master_dictionary_deduplicated.pdf"
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) >= 150


def test_comprehensive_grammar_integrity() -> None:
    """Verify that the 8-chapter Tangkhul grammar is exported in JSON and PDF."""
    json_path = EXPORTS_DIR / "tangkhul_comprehensive_grammar.json"
    assert json_path.exists()
    data = json.load(open(json_path, encoding="utf-8"))
    assert len(data["chapters"]) == 8

    pdf_path = EXPORTS_DIR / "tangkhul_comprehensive_grammar.pdf"
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 8


def test_proverbs_and_idioms_integrity() -> None:
    """Verify that 35 traditional proverbs and idioms are exported in JSON and PDF."""
    json_path = EXPORTS_DIR / "tangkhul_proverbs_and_idioms_master.json"
    assert json_path.exists()
    data = json.load(open(json_path, encoding="utf-8"))
    assert data["total_proverbs"] == 35
    assert len(data["proverbs"]) == 35

    ids = [p["id"] for p in data["proverbs"]]
    assert len(set(ids)) == 35

    pdf_path = EXPORTS_DIR / "tangkhul_proverbs_and_idioms_master.pdf"
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 6


def test_unified_master_corpus_integrity() -> None:
    """Verify the grand unified master corpus JSON and PDF."""
    json_path = EXPORTS_DIR / "tangkhul_master_corpus_unified.json"
    assert json_path.exists()
    data = json.load(open(json_path, encoding="utf-8"))

    stats = data["summary_statistics"]
    assert stats["total_catalogued_manifest_records"] == 226
    assert stats["books_count"] == 35
    assert stats["literature_works_count"] == 60
    assert stats["songs_and_hymns_count"] == 48
    assert stats["culture_records_count"] == 35
    assert stats["history_records_count"] == 32
    assert stats["dictionary_publications_count"] == 16
    assert stats["deduplicated_dictionary_lexicon_entries"] == 6480
    assert stats["folk_riddles_count"] == 400
    assert stats["proverbs_and_idioms_count"] == 35
    assert stats["grammar_chapters_count"] == 8
    assert stats["sacred_scriptures_and_epics_count"] == 4
    assert stats["prayers_rituals_and_clans_modules_count"] == 3
    assert stats["duplicate_manifest_records"] == 0
    assert stats["duplicate_dictionary_entries_merged"] == 293

    pdf_path = EXPORTS_DIR / "tangkhul_master_corpus_unified.pdf"
    assert pdf_path.exists()
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 5


def test_deduplication_audit_report_integrity() -> None:
    """Verify the deduplication audit report."""
    audit_path = EXPORTS_DIR / "tangkhul_deduplication_audit_report.json"
    assert audit_path.exists()
    report = json.load(open(audit_path, encoding="utf-8"))

    assert report["manifest_audit"]["total_records"] == 226
    assert report["manifest_audit"]["global_id_duplicates"] == 0
    assert report["dictionary_audit"]["duplicates_merged_count"] == 293
    assert report["riddles_audit"]["duplicate_riddles"] == 0
    assert report["proverbs_audit"]["duplicate_proverbs"] == 0
    assert report["scriptures_and_epics_audit"]["total_works"] == 4
    assert report["prayers_rituals_clans_audit"]["total_modules"] == 3
