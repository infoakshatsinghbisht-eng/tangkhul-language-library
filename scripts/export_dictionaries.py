#!/usr/bin/env python3
"""Export all catalogued Tangkhul dictionary records into structured JSON and PDF formats.

Generates:
1. Consolidated JSON collections:
   - data/exports/dictionaries.json
   - src/tangkhul_lib/data/dictionaries.json
2. Individual JSON documents:
   - data/exports/dictionaries/{id}.json (10 records)
3. Formatted PDF anthology & individual PDF documents:
   - data/exports/dictionaries.pdf (Complete 10-record lexicographical compendium)
   - data/exports/dictionaries/{id}.pdf (Individual dictionary PDF documents)
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import pypdf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_raw_dictionaries import DICTIONARIES_RAW_DATA


def sanitize_pdf_text(text: str) -> str:
    """Sanitize and encode string for PDF Type 1 Helvetica font (Latin-1)."""
    replacements = {
        "—": "--",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "*",
        "ā": "a",
        "ē": "e",
        "ī": "i",
        "ō": "o",
        "ū": "u",
        "Ā": "A",
        "Ē": "E",
        "Ī": "I",
        "Ō": "O",
        "Ū": "U",
        "ǝ": "e",
        "ɛ": "e",
        "ɔ": "o",
        "ʰ": "h",
        "ŋ": "ng",
        "♭": "b",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return escaped.encode("latin-1", "replace").decode("latin-1")


def build_pdf_document(pages_content: list[list[tuple[str, int, str]]]) -> bytes:
    """Build a multi-page PDF 1.4 document from structured lines."""
    cat_id = 1
    pages_root_id = 2
    f1_id = 3
    f2_id = 4

    cur_id = 5
    page_entries: list[tuple[int, int, bytes]] = []
    page_obj_ids: list[int] = []

    for page_items in pages_content:
        p_id = cur_id
        cur_id += 1
        c_id = cur_id
        cur_id += 1

        stream_cmds = ["BT"]
        y = 780
        stream_cmds.append(f"50 {y} Td")
        current_y = y

        for font, size, line in page_items:
            clean = sanitize_pdf_text(line)
            stream_cmds.append(f"{font} {size} Tf")
            stream_cmds.append(f"({clean}) Tj")
            dy = -(size + 4)
            stream_cmds.append(f"0 {dy} Td")
            current_y += dy
            if current_y < 50:
                break

        stream_cmds.append("ET")
        c_stream = "\n".join(stream_cmds).encode("latin-1", "replace")
        page_entries.append((p_id, c_id, c_stream))
        page_obj_ids.append(p_id)

    obj_dict: dict[int, bytes] = {}
    obj_dict[cat_id] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids_str = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    obj_dict[pages_root_id] = (
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>".encode("latin-1")
    )
    obj_dict[f1_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    obj_dict[f2_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"

    for pid, cid, cstream in page_entries:
        p_def = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Contents {cid} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> >>"
        )
        obj_dict[pid] = p_def.encode("latin-1")
        c_def = f"<< /Length {len(cstream)} >>\nstream\n".encode("latin-1") + cstream + b"\nendstream"
        obj_dict[cid] = c_def

    out = bytearray(b"%PDF-1.4\n")
    offsets: dict[int, int] = {}
    for oid in sorted(obj_dict.keys()):
        offsets[oid] = len(out)
        out.extend(f"{oid} 0 obj\n".encode("latin-1"))
        out.extend(obj_dict[oid])
        out.extend(b"\nendobj\n")

    xref_offset = len(out)
    out.extend(f"xref\n0 {len(obj_dict)+1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for oid in sorted(obj_dict.keys()):
        out.extend(f"{offsets[oid]:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer\n<< /Size {len(obj_dict)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
            "latin-1"
        )
    )
    return bytes(out)


def create_dictionary_page(d: dict[str, Any], page_num: int | None = None) -> list[tuple[str, int, str]]:
    """Format an individual dictionary record into a structured page of PDF lines."""
    lines: list[tuple[str, int, str]] = []

    did = d["id"]
    title = d.get("title", "Tangkhul Dictionary")
    creator = d.get("creator") or d.get("authors", "Various")
    year = d.get("year") or d.get("publication_year", "N/A")
    publisher = d.get("publisher", "Independent")
    lang_pair = d.get("language_pair", "Tangkhul-English")
    dialect = d.get("dialect", "Ukhrul")
    source_type = d.get("source_type", "dictionary").replace("_", " ").title()
    license_val = d.get("license", "Public Domain")
    perm_status = d.get("permission_status", "pending").upper()
    bg = d.get("background", d.get("notes", ""))
    entries = d.get("entries", [])

    # Header block
    lines.append(("/F2", 15, f"{did}: {title[:48]}"))
    if d.get("alternate_title") and d["alternate_title"] != title:
        lines.append(("/F2", 10, f"Alternative Title: {d['alternate_title']}"))
    lines.append(("/F1", 9, f"Lexicographer / Compiler: {creator} | Year: {year} | Publisher: {publisher[:35]}"))
    lines.append(("/F1", 9, f"Language Pair: {lang_pair} | Dialect: {dialect} | Type: {source_type}"))
    lines.append(("/F2", 9, f"Permission Tier: {perm_status} | License: {license_val}"))
    lines.append(("/F1", 8, "-" * 88))

    # Historical & Lexicographical Background
    lines.append(("/F2", 10, "Historical & Lexicographical Background:"))
    wrapped_bg = textwrap.wrap(bg, width=82)
    for bgl in wrapped_bg[:4]:  # limit lines to keep page balanced
        lines.append(("/F1", 8, f"  {bgl}"))

    # Phonology & Orthography Notes
    if d.get("phonology_notes"):
        lines.append(("/F2", 9, "Phonological & Orthographic Framework:"))
        wrapped_ph = textwrap.wrap(d["phonology_notes"], width=82)
        for phl in wrapped_ph[:2]:
            lines.append(("/F1", 8, f"  {phl}"))

    lines.append(("/F1", 8, "-" * 88))

    # Representative Lexicon
    lines.append(("/F2", 10, f"Representative Lexicon & Extracted Headwords ({len(entries)} items):"))
    for idx, ent in enumerate(entries[:10], 1):  # display up to 10 prominent entries
        hw = ent.get("headword", "")
        pos = ent.get("part_of_speech", "noun")
        defs = ", ".join(ent.get("definitions_en", []))
        hi_defs = f" [Hi: {', '.join(ent.get('definitions_hi', []))}]" if ent.get("definitions_hi") else ""
        pg = f" ({ent.get('page', '')})" if ent.get("page") else ""
        alts = f" <Alt: {', '.join(ent.get('alternative_spellings', []))}>" if ent.get("alternative_spellings") else ""
        ex = f" -- Ex: {ent.get('example', '')}" if ent.get("example") else ""

        entry_line = f"  {idx:>2}. {hw} ({pos}): {defs}{hi_defs}{pg}{alts}{ex}"
        if len(entry_line) > 86:
            entry_line = entry_line[:83] + "..."
        lines.append(("/F1", 8, entry_line))

    # Footer notice
    lines.append(("/F1", 8, "-" * 88))
    pg_str = f" | Page {page_num}" if page_num else ""
    lines.append(("/F1", 7, f"Tangkhul Language Library Digital Preservation Archive{pg_str}"))

    return lines


def export_dictionaries() -> tuple[int, Path, Path]:
    """Export all catalogued dictionary records to consolidated and individual JSON/PDF files."""
    manifest_file = ROOT / "data" / "manifests" / "dictionaries.jsonl"
    exports_dir = ROOT / "data" / "exports"
    dict_export_dir = exports_dir / "dictionaries"
    bundled_dir = ROOT / "src" / "tangkhul_lib" / "data"

    dict_export_dir.mkdir(parents=True, exist_ok=True)
    bundled_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    # Enrich each record with structured entries, background, and phonology notes
    enriched_dictionaries: list[dict[str, Any]] = []
    for rec in records:
        did = rec["id"]
        extra = DICTIONARIES_RAW_DATA.get(did, {})
        item = dict(rec)
        item["alternate_title"] = extra.get("alternate_title", rec.get("title_translation"))
        item["background"] = extra.get("background", rec.get("notes"))
        item["phonology_notes"] = extra.get("phonology_notes", "")
        item["entries"] = extra.get("entries", [])
        enriched_dictionaries.append(item)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "dictionaries.json"
    bundled_json = bundled_dir / "dictionaries.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_dictionaries, f, ensure_ascii=False, indent=2)
    with open(bundled_json, "w", encoding="utf-8") as f:
        json.dump(enriched_dictionaries, f, ensure_ascii=False, indent=2)

    # 2. Build Multi-Page PDF Compendium
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Cover Page
    cover_page: list[tuple[str, int, str]] = [
        ("/F2", 20, "Tangkhul Lexicographical Compendium"),
        ("/F2", 13, "Historical Dictionaries, Field Wordlists & Trilingual Lexicons (1859 - 2018)"),
        ("/F1", 10, "A Comprehensive Digital Preservation of Tangkhul Naga Lexicography"),
        ("/F1", 10, f"Total Catalogued Dictionary Resources: {len(enriched_dictionaries)}"),
        ("/F1", 10, "Preservation Scope: Historical Grammar-Dictionaries, School Wordbooks, Dialect Glossaries"),
        ("/F1", 10, "Format: Normalized Headwords, Phonemic Notes, Bilingual/Trilingual Glosses, and Citations"),
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F2", 11, "Table of Catalogued Dictionaries:"),
    ]

    for idx, d in enumerate(enriched_dictionaries, 1):
        creator_short = (d.get("creator") or "Unknown").split(",")[0]
        year_str = str(d.get("year", "N/A"))
        pair_str = d.get("language_pair", "Tangkhul")
        cover_page.append((
            "/F1",
            9,
            f"  {idx:>2}. [{d['id']:<12}] {d['title'][:34]:<34} ({creator_short}, {year_str}) [{pair_str}]",
        ))

    cover_page.extend([
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F1", 9, "Tangkhul Language Preservation Project - Digital Library Archive"),
    ])
    all_pdf_pages.append(cover_page)

    # Individual dictionary pages
    for page_idx, d in enumerate(enriched_dictionaries, 2):
        # Save individual JSON
        ind_json = dict_export_dir / f"{d['id']}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

        # Build individual page for compendium
        dict_page = create_dictionary_page(d, page_num=page_idx)
        all_pdf_pages.append(dict_page)

        # Build and save individual PDF
        ind_pdf_bytes = build_pdf_document([create_dictionary_page(d, page_num=1)])
        ind_pdf_path = dict_export_dir / f"{d['id']}.pdf"
        ind_pdf_path.write_bytes(ind_pdf_bytes)

    # Master compendium PDF
    compendium_pdf_bytes = build_pdf_document(all_pdf_pages)
    compendium_pdf_path = exports_dir / "dictionaries.pdf"
    compendium_pdf_path.write_bytes(compendium_pdf_bytes)

    # Validate generated PDF with pypdf
    reader = pypdf.PdfReader(str(compendium_pdf_path))
    num_pages = len(reader.pages)
    print(
        f"Exported {len(enriched_dictionaries)} dictionaries: "
        f"JSON -> {consolidated_json.name}, PDF -> {compendium_pdf_path.name} ({num_pages} pages)"
    )

    return len(enriched_dictionaries), consolidated_json, compendium_pdf_path


def main() -> None:
    export_dictionaries()


if __name__ == "__main__":
    main()
