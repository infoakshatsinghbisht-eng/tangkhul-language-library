"""Unit tests for dictionary metadata models, catalogue searching, and duplicate detection."""

from __future__ import annotations

import pytest

from tangkhul_lib.core.exceptions import ManifestValidationError
from tangkhul_lib.dictionaries.catalogue import DictionaryCatalogue
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord


def test_dictionary_source_validation() -> None:
    # Valid source record
    src = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        authors=["William Pettigrew"],
        publication_year=1918,
        language_pair="Tangkhul-English",
        source_type="grammar_dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    src.validate()
    assert src.id == "DIC-HIST-001"
    assert src.authors == ["William Pettigrew"]

    # Manifest conversion
    man_rec = src.to_manifest_record()
    assert man_rec.id == "DIC-HIST-001"
    assert man_rec.resource_type == "dictionaries"
    assert man_rec.creator == "William Pettigrew"

    # Missing ID raises error
    with pytest.raises(ManifestValidationError):
        DictionarySourceRecord(id="", title="Test Dictionary").validate()

    # Invalid source_type raises error
    with pytest.raises(ManifestValidationError):
        DictionarySourceRecord(
            id="DIC-ERR-001",
            title="Test Dictionary",
            source_type="unsupported_type",
        ).validate()


def test_dictionary_entry_validation_and_vocabulary_conversion() -> None:
    entry = DictionaryEntryRecord(
        id="DIC-HIST-001-ENT-0001",
        dictionary_id="DIC-HIST-001",
        headword="khararchan",
        definitions_en=["folk-tale", "fable", "ancient story"],
        part_of_speech="noun",
        page_or_section="p. 320",
        permission_status="public_domain",
        verification_status="verified",
    )
    entry.validate()
    assert entry.normalized_headword == "khararchan"

    # Convert to unified VocabularyEntry
    vocab = entry.to_vocabulary_entry()
    assert vocab.headword == "khararchan"
    assert "folk-tale" in vocab.meanings
    assert "folk-tale" in vocab.translations_en
    assert vocab.part_of_speech == "noun"
    assert len(vocab.provenance) == 1
    assert vocab.provenance[0].source_id == "DIC-HIST-001"
    assert vocab.provenance[0].page_or_section == "p. 320"


def test_dictionary_catalogue_search_and_filter() -> None:
    src1 = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        authors=["William Pettigrew"],
        publication_year=1918,
        language_pair="Tangkhul-English",
        dialect="Ukhrul",
        source_type="grammar_dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    src2 = DictionarySourceRecord(
        id="DIC-TLS-001",
        title="Tangkhul Tui Dictionary",
        authors=["N. Luikham"],
        publication_year=1997,
        language_pair="Tangkhul-English",
        dialect="Ukhrul",
        source_type="dictionary",
        permission_status="restricted",
        access_status="metadata_only",
        verification_status="verified",
    )
    src3 = DictionarySourceRecord(
        id="DIC-CAND-001",
        title="Comparative Tangkhul Dialect Glossary",
        authors=["Tangkhul Documentation Project"],
        publication_year=2018,
        language_pair="Tangkhul-English",
        dialect="Multidialectal",
        source_type="glossary",
        permission_status="pending",
        access_status="metadata_only",
        verification_status="needs_review",
    )

    catalogue = DictionaryCatalogue()
    catalogue.add_source(src1)
    catalogue.add_source(src2)
    catalogue.add_source(src3)

    assert len(catalogue.list_sources()) == 3

    # Filter by author
    res_author = catalogue.search_sources(author="Luikham")
    assert len(res_author) == 1
    assert res_author[0].id == "DIC-TLS-001"

    # Filter by verification status
    res_review = catalogue.search_sources(verification_status="needs_review")
    assert len(res_review) == 1
    assert res_review[0].id == "DIC-CAND-001"

    # Filter by year
    res_year = catalogue.search_sources(year=1918)
    assert len(res_year) == 1
    assert res_year[0].id == "DIC-HIST-001"

    # Free query search
    res_query = catalogue.search_sources(query="Grammar")
    assert len(res_query) == 1
    assert res_query[0].id == "DIC-HIST-001"


def test_duplicate_detection_preserves_distinct_senses() -> None:
    catalogue = DictionaryCatalogue()

    # Sense 1: noun "akha" = fish
    entry_fish = DictionaryEntryRecord(
        id="ENT-001",
        dictionary_id="DIC-TEST-001",
        headword="akha",
        definitions_en=["fish"],
        part_of_speech="noun",
        permission_status="permitted",
        verification_status="verified",
    )
    # Sense 2: numeral "akha" = one
    entry_one = DictionaryEntryRecord(
        id="ENT-002",
        dictionary_id="DIC-TEST-001",
        headword="akha",
        definitions_en=["one", "single"],
        part_of_speech="numeral",
        permission_status="permitted",
        verification_status="verified",
    )
    # True duplicate of entry_fish
    entry_fish_dup = DictionaryEntryRecord(
        id="ENT-003",
        dictionary_id="DIC-TEST-001",
        headword="akha",
        definitions_en=["fish"],
        part_of_speech="noun",
        permission_status="permitted",
        verification_status="verified",
    )

    catalogue.add_entry(entry_fish)
    catalogue.add_entry(entry_one)
    catalogue.add_entry(entry_fish_dup)

    # entry_fish should match entry_fish_dup as duplicate, but NOT entry_one
    dups_for_fish = catalogue.find_likely_duplicates(entry_fish)
    assert len(dups_for_fish) == 1
    assert dups_for_fish[0].id == "ENT-003"

    # entry_one has distinct meaning and POS -> no duplicates found
    dups_for_one = catalogue.find_likely_duplicates(entry_one)
    assert len(dups_for_one) == 0


def test_conflict_detection() -> None:
    catalogue = DictionaryCatalogue()
    e1 = DictionaryEntryRecord(
        id="ENT-001",
        dictionary_id="DIC-SRC-A",
        headword="ngashan",
        definitions_en=["custom", "tradition"],
        part_of_speech="noun",
        permission_status="permitted",
        verification_status="verified",
    )
    e2 = DictionaryEntryRecord(
        id="ENT-002",
        dictionary_id="DIC-SRC-B",
        headword="ngashān",  # Variant spelling with macron
        definitions_en=["attire", "shawl"],
        part_of_speech="noun",
        permission_status="permitted",
        verification_status="verified",
    )
    catalogue.add_entry(e1)
    catalogue.add_entry(e2)

    conflicts = catalogue.find_conflicts()
    assert len(conflicts) >= 1
    assert conflicts[0]["headword_norm"] in ("ngashan", "ngashān")
    assert len(conflicts[0]["spellings"]) == 2


def test_source_report_generation() -> None:
    src_pub = DictionarySourceRecord(
        id="DIC-PUB",
        title="Public Lexicon",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    src_res = DictionarySourceRecord(
        id="DIC-RES",
        title="Restricted Lexicon",
        permission_status="restricted",
        access_status="metadata_only",
        verification_status="needs_review",
    )
    catalogue = DictionaryCatalogue()
    catalogue.add_source(src_pub)
    catalogue.add_source(src_res)

    report = catalogue.get_source_report()
    assert report["total_sources"] == 2
    assert report["verified_sources"] == 1
    assert report["needs_review_sources"] == 1
    assert report["metadata_only_sources"] == 1
    assert report["full_text_sources"] == 1


def test_actual_dictionaries_manifest_and_raw_files() -> None:
    """Verify that all 10 dictionaries have valid manifest entries and non-empty raw text files."""
    import json
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent.parent
    manifest_path = project_root / "data" / "manifests" / "dictionaries.jsonl"

    assert manifest_path.is_file(), "Missing data/manifests/dictionaries.jsonl"
    with manifest_path.open(encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    assert len(records) == 16

    for rec in records:
        assert rec["resource_type"] == "dictionaries"
        assert rec["id"].startswith("DIC-")
        assert rec["local_path"] is not None
        raw_file = project_root / rec["local_path"]
        assert raw_file.is_file(), f"Missing raw dictionary file: {raw_file}"
        assert raw_file.stat().st_size > 500, f"Raw file unexpectedly small: {raw_file}"
        content = raw_file.read_text(encoding="utf-8")
        assert "SECTION 1: BIBLIOGRAPHIC" in content
        assert "SECTION 2: REPRESENTATIVE LEXICON" in content


def test_dictionaries_json_and_pdf_exports() -> None:
    """Verify that dictionary JSON and PDF exports exist and are valid."""
    import json
    from pathlib import Path

    import pypdf

    project_root = Path(__file__).resolve().parent.parent.parent
    exports_dir = project_root / "data" / "exports"
    dict_exports_dir = exports_dir / "dictionaries"

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "dictionaries.json"
    assert consolidated_json.is_file()
    with consolidated_json.open(encoding="utf-8") as f:
        items = json.load(f)
    assert len(items) == 16

    # 2. Master Compendium PDF
    compendium_pdf = exports_dir / "dictionaries.pdf"
    assert compendium_pdf.is_file()
    reader = pypdf.PdfReader(str(compendium_pdf))
    assert len(reader.pages) == 17
    assert "Tangkhul Lexicographical Compendium" in reader.pages[0].extract_text()

    # 3. Individual JSON and PDF documents
    for item in items:
        did = item["id"]
        ind_json = dict_exports_dir / f"{did}.json"
        assert ind_json.is_file(), f"Missing individual JSON for {did}"
        with ind_json.open(encoding="utf-8") as f:
            ind_data = json.load(f)
        assert ind_data["id"] == did
        assert len(ind_data.get("entries", [])) >= 10

        ind_pdf = dict_exports_dir / f"{did}.pdf"
        assert ind_pdf.is_file(), f"Missing individual PDF for {did}"
        ind_reader = pypdf.PdfReader(str(ind_pdf))
        assert len(ind_reader.pages) == 1
        assert did in ind_reader.pages[0].extract_text()


def test_database_dictionaries_persistence() -> None:
    """Verify that all 16 dictionaries and their lexical entries are persisted in SQLite."""
    import sqlite3
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent.parent
    db_path = project_root / "data" / "database" / "tangkhul_corpus.sqlite"
    assert db_path.is_file()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM dictionaries")
    dict_count = cur.fetchone()[0]
    assert dict_count == 16

    cur.execute("SELECT COUNT(*) FROM dictionary_entries")
    entry_count = cur.fetchone()[0]
    assert entry_count >= 150

    conn.close()


