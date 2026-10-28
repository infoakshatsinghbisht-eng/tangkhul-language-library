#!/usr/bin/env python3
"""Export all catalogued Tangkhul literary works into structured JSON and PDF formats.

Generates:
1. Consolidated JSON collections:
   - data/exports/literature.json (41 records)
   - src/tangkhul_lib/data/literature.json (41 records)
2. Individual JSON documents:
   - data/exports/literature/{id}.json (41 records)
3. Formatted PDF compendium & individual PDF documents:
   - data/exports/literature.pdf (Complete 43-page literary compendium & anthology)
   - data/exports/literature/{id}.pdf (Individual literary work monograph PDF documents)
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

from scripts.build_raw_literature import LITERATURE_RAW_DATA
from scripts.build_raw_literature_batch2 import LITERATURE_BATCH2_RAW_DATA
from scripts.build_raw_literature_batch3 import LITERATURE_BATCH3_RAW_DATA

ALL_LITERATURE_RAW_DATA = {
    **LITERATURE_RAW_DATA,
    **LITERATURE_BATCH2_RAW_DATA,
    **LITERATURE_BATCH3_RAW_DATA,
}


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


def export_literature() -> tuple[int, Path, Path]:
    """Export all catalogued literary works to consolidated and individual JSON/PDF files."""
    manifest_file = ROOT / "data" / "manifests" / "literature.jsonl"
    exports_dir = ROOT / "data" / "exports"
    literature_export_dir = exports_dir / "literature"
    bundled_dir = ROOT / "src" / "tangkhul_lib" / "data"

    literature_export_dir.mkdir(parents=True, exist_ok=True)
    bundled_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    # Enrich each record with structured texts, themes, meter, commentary, and terms
    enriched_literature: list[dict[str, Any]] = []
    for rec in records:
        lid = rec["id"]
        extra = ALL_LITERATURE_RAW_DATA.get(lid, {})
        item = dict(rec)
        t_stanzas = extra.get("tangkhul_text", [])
        e_stanzas = extra.get("english_text", [])
        item["indigenous_tangkhul_text"] = t_stanzas
        item["english_translation_text"] = e_stanzas
        item["literary_themes"] = extra.get("literary_themes", [])
        item["structure_and_meter"] = extra.get("structure_and_meter", "Traditional Free Verse")
        item["critical_commentary"] = extra.get("critical_commentary", "N/A")
        item["poetic_vocabulary_terms"] = extra.get("vocabulary_terms", {})
        item["stanza_count"] = len(t_stanzas)
        item["line_count"] = sum(
            len([line for line in s.splitlines() if line.strip()]) for s in t_stanzas
        )
        item["text_availability"] = "full_text"
        enriched_literature.append(item)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "literature.json"
    bundled_json = bundled_dir / "literature.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_literature, f, ensure_ascii=False, indent=2)
    with open(bundled_json, "w", encoding="utf-8") as f:
        json.dump(enriched_literature, f, ensure_ascii=False, indent=2)

    # 2. Build Multi-Page Master Compendium PDF
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Table of Contents chunking (22 items per page)
    toc_chunk_size = 22
    total_parts = (len(enriched_literature) + toc_chunk_size - 1) // toc_chunk_size
    for chunk_start in range(0, len(enriched_literature), toc_chunk_size):
        chunk = enriched_literature[chunk_start:chunk_start + toc_chunk_size]
        part_num = (chunk_start // toc_chunk_size) + 1
        cover_page: list[tuple[str, int, str]] = []
        if part_num == 1:
            cover_page.extend([
                ("/F2", 20, "Tangkhul Literary Anthology & Compendium"),
                ("/F2", 13, "Ballads, Folktales, Lyric Poetry, Dramas, Fables & Translations"),
                ("/F1", 10, "A Comprehensive Digital Preservation of Tangkhul Naga Literary Heritage"),
                ("/F1", 10, f"Total Catalogued Literary Masterpieces: {len(enriched_literature)}"),
                ("/F1", 10, "Genres: Ballad, Folktale, Children's Literature, Poetry, Play, Short Story, Anthology, Riddle"),
                ("/F1", 10, "Format: Tangkhul Literary Text, English Glosses, Metrical Structure, and Poetic Lexicon"),
                ("/F1", 10, "----------------------------------------------------------------------"),
                ("/F2", 11, f"Table of Literary Masterpieces (Part 1 of {total_parts}):"),
            ])
        else:
            cover_page.extend([
                ("/F2", 16, "Tangkhul Literary Anthology & Compendium"),
                ("/F2", 11, f"Table of Literary Masterpieces (Part {part_num} of {total_parts}):"),
                ("/F1", 10, "----------------------------------------------------------------------"),
            ])

        for idx, lit in enumerate(chunk, chunk_start + 1):
            type_str = lit.get("work_type", "literature").upper()
            yr_str = f"[{lit.get('year')}]" if lit.get("year") else ""
            cover_page.append(
                ("/F1", 9, f"  {idx:>2}. [{lit['id']:<14}] {lit['title'][:36]:<36} ({type_str}) {yr_str}")
            )

        cover_page.extend([
            ("/F1", 10, "----------------------------------------------------------------------"),
            ("/F1", 9, "Tangkhul Language Preservation Project - Digital Library Archive"),
        ])
        all_pdf_pages.append(cover_page)

    # Individual records: create pages for both consolidated PDF and individual PDF
    for lit in enriched_literature:
        # Save individual JSON
        ind_json = literature_export_dir / f"{lit['id']}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(lit, f, ensure_ascii=False, indent=2)

        creator_str = lit.get("creator") or lit.get("author") or "Traditional"
        # Build individual record page content
        page_items: list[tuple[str, int, str]] = [
            ("/F2", 14, f"[{lit['id']}] {lit['title'][:55]}"),
            ("/F2", 10, f"Translation: {lit.get('title_translation', 'N/A')[:65]}"),
            ("/F1", 9, f"Work Type: {lit.get('work_type', 'literature').upper()} | Creator: {creator_str[:35]} | Year: {lit.get('year', 'N/A')}"),
            ("/F1", 9, f"Village: {lit.get('village', 'N/A')} | Dialect: {lit.get('dialect', 'Standard Tangkhul')} | Book ID: {lit.get('book_id', 'N/A')}"),
            ("/F1", 9, f"Publisher / Source: {lit.get('publisher', 'N/A')[:50]}"),
            ("/F1", 9, f"Clearance: {lit.get('license', 'N/A')} | Permission: {lit.get('permission_status', 'pending')} | Status: {lit.get('verification_status', 'verified')}"),
            ("/F1", 9, "-" * 75),
        ]

        # Literary Themes & Metrical Structure
        if lit.get("literary_themes"):
            themes_str = ", ".join(lit["literary_themes"])
            wrapped_th = textwrap.wrap(f"Themes: {themes_str}", width=75)
            for tl in wrapped_th[:2]:
                page_items.append(("/F2", 9, tl))

        page_items.append(("/F1", 9, f"Structure & Meter: {lit.get('structure_and_meter', 'N/A')[:70]}"))
        page_items.append(("/F1", 9, "-" * 75))

        # Critical Commentary & Notes
        comm = lit.get("critical_commentary") or lit.get("notes") or ""
        if comm:
            wrapped_comm = textwrap.wrap(f"Critical Overview: {comm}", width=75)
            for cl in wrapped_comm[:2]:
                page_items.append(("/F1", 9, cl))
            page_items.append(("/F1", 9, "-" * 75))

        # Indigenous Literary Text Excerpt
        page_items.append(("/F2", 10, "Indigenous Tangkhul Literary Text / Stanzas:"))
        for tline in lit.get("indigenous_tangkhul_text", [])[:3]:
            # If multi-line stanza, take first two lines
            lines_in_s = [line.strip() for line in tline.splitlines() if line.strip()]
            for line in lines_in_s[:2]:
                page_items.append(("/F1", 9, f"  {line[:72]}"))

        page_items.append(("/F1", 9, "-" * 75))

        # English Translation
        page_items.append(("/F2", 10, "English Translation & Literary Rendering:"))
        for eline in lit.get("english_translation_text", [])[:3]:
            lines_in_e = [line.strip() for line in eline.splitlines() if line.strip()]
            for line in lines_in_e[:2]:
                page_items.append(("/F1", 9, f"  {line[:72]}"))

        page_items.append(("/F1", 9, "-" * 75))

        # Key Literary Vocabulary
        if lit.get("poetic_vocabulary_terms"):
            page_items.append(("/F2", 10, "Key Poetic & Literary Vocabulary Terms:"))
            term_items = list(lit["poetic_vocabulary_terms"].items())[:3]
            for term, gloss in term_items:
                page_items.append(("/F1", 9, f"  * {term:<18} : {gloss[:50]}"))

        page_items.append(("/F1", 9, "-" * 75))
        page_items.append(("/F1", 8, f"Tangkhul Language Library - Literature Archive Record {lit['id']}"))

        all_pdf_pages.append(page_items)

        # Generate Individual PDF for this literary work
        ind_pdf_bytes = build_pdf_document([page_items])
        ind_pdf_path = literature_export_dir / f"{lit['id']}.pdf"
        with open(ind_pdf_path, "wb") as pf:
            pf.write(ind_pdf_bytes)

    # Write Master Compendium PDF
    compendium_pdf = exports_dir / "literature.pdf"
    compendium_bytes = build_pdf_document(all_pdf_pages)
    with open(compendium_pdf, "wb") as pf:
        pf.write(compendium_bytes)

    # Validate output PDFs with pypdf
    reader = pypdf.PdfReader(str(compendium_pdf))
    print(f"Validated Master Compendium PDF: {len(reader.pages)} pages in {compendium_pdf.name}")

    return len(enriched_literature), consolidated_json, compendium_pdf


if __name__ == "__main__":
    count, json_path, pdf_path = export_literature()
    print("\n=======================================================")
    print(f"SUCCESS: Exported {count} literary works!")
    print(f"  Consolidated JSON: {json_path}")
    print(f"  Consolidated PDF:  {pdf_path}")
    print(f"  Individual JSONs:  data/exports/literature/ ({count} files)")
    print(f"  Individual PDFs:   data/exports/literature/ ({count} files)")
    print("=======================================================")
