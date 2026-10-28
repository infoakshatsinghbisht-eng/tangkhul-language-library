"""Unit tests for dictionary entry extraction, permission enforcement, and format parsing."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.dictionaries.catalogue import DictionaryCatalogue
from tangkhul_lib.dictionaries.extractor import DictionaryExtractor
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord


def test_permission_barrier_blocks_restricted_dictionary() -> None:
    restricted_source = DictionarySourceRecord(
        id="DIC-TLS-001",
        title="Tangkhul Tui Dictionary",
        permission_status="restricted",
        access_status="metadata_only",
        verification_status="verified",
    )
    extractor = DictionaryExtractor()

    # check_permissions must raise PermissionDeniedError
    with pytest.raises(PermissionDeniedError) as exc_info:
        extractor.check_permissions(restricted_source)

    assert "not permitted" in str(exc_info.value)
    assert exc_info.value.record_id == "DIC-TLS-001"

    # Attempting parse_text_lines on restricted source must raise error
    with pytest.raises(PermissionDeniedError):
        extractor.parse_text_lines(
            restricted_source,
            ["akha : fish"],
            enforce_permissions=True,
        )


def test_text_lines_parsing_and_confidence_review() -> None:
    pub_source = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    extractor = DictionaryExtractor()

    lines = [
        "khararchan (n.) : folk-tale, ancient story, legend",
        "khamatha (adj.) : good, beautiful, handsome",
        "unstructured line without colon or punctuation",
    ]

    entries = extractor.parse_text_lines(pub_source, lines)
    assert len(entries) == 3

    # Entry 1: structured noun
    e1 = entries[0]
    assert e1.headword == "khararchan"
    assert e1.part_of_speech == "n"
    assert "folk-tale" in e1.definitions_en
    assert e1.verification_status == "verified"
    assert e1.confidence >= 0.9

    # Entry 2: structured adjective
    e2 = entries[1]
    assert e2.headword == "khamatha"
    assert e2.part_of_speech == "adj"
    assert "good" in e2.definitions_en

    # Entry 3: unparsed fallback -> flagged for review
    e3 = entries[2]
    assert e3.headword == "unstructured"
    assert e3.verification_status == "needs_review"
    assert e3.confidence < 0.8


def test_tsv_extraction(tmp_path: Path) -> None:
    pub_source = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        permission_status="public_domain",
        access_status="full_text_available",
        verification_status="verified",
    )
    tsv_file = tmp_path / "sample_lexicon.tsv"
    tsv_file.write_text(
        "headword\tenglish\thindi\tpos\tpage\n"
        "ngashan\tcustom; attire\triti-rivaj\tnoun\t345\n"
        "luira\tseed-sowing feast\tbovai parab\tnoun\t334\n",
        encoding="utf-8",
    )

    extractor = DictionaryExtractor()
    entries = extractor.extract_from_tsv_or_csv(pub_source, tsv_file)
    assert len(entries) == 2

    assert entries[0].headword == "ngashan"
    assert "custom" in entries[0].definitions_en
    assert "riti-rivaj" in entries[0].definitions_hi
    assert entries[0].page_or_section == "345"

    assert entries[1].headword == "luira"
    assert entries[1].definitions_en == ["seed-sowing feast"]


def test_restricted_export_prevention(tmp_path: Path) -> None:
    catalogue = DictionaryCatalogue()
    ent_pub = DictionaryEntryRecord(
        id="ENT-PUB-001",
        dictionary_id="DIC-PUB",
        headword="akha",
        definitions_en=["fish"],
        permission_status="public_domain",
        verification_status="verified",
    )
    ent_res = DictionaryEntryRecord(
        id="ENT-RES-001",
        dictionary_id="DIC-RES",
        headword="secretword",
        definitions_en=["confidential meaning"],
        permission_status="restricted",
        verification_status="verified",
    )
    catalogue.add_entry(ent_pub)
    catalogue.add_entry(ent_res)

    export_jsonl = tmp_path / "exported_entries.jsonl"
    catalogue.export_entries_jsonl(export_jsonl, permitted_only=True)

    content = export_jsonl.read_text(encoding="utf-8")
    assert "ENT-PUB-001" in content
    assert "ENT-RES-001" not in content
    assert "secretword" not in content
