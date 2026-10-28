#!/usr/bin/env python3
"""Export all catalogued Tangkhul cultural heritage records into structured JSON and PDF formats.

Generates:
1. Consolidated JSON collections:
   - data/exports/culture.json
   - src/tangkhul_lib/data/culture.json
2. Individual JSON documents:
   - data/exports/culture/{id}.json (24 records)
3. Formatted PDF anthology & individual PDF documents:
   - data/exports/culture.pdf (Complete 24-record cultural compendium)
   - data/exports/culture/{id}.pdf (Individual cultural resource PDF documents)
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

from scripts.build_raw_culture import CULTURE_RAW_DATA


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


def export_culture() -> tuple[int, Path, Path]:
    """Export all catalogued culture records to consolidated and individual JSON/PDF files."""
    manifest_file = ROOT / "data" / "manifests" / "culture.jsonl"
    exports_dir = ROOT / "data" / "exports"
    culture_export_dir = exports_dir / "culture"
    bundled_dir = ROOT / "src" / "tangkhul_lib" / "data"

    culture_export_dir.mkdir(parents=True, exist_ok=True)
    bundled_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    # Enrich each record with structured texts, procedure, and timing
    enriched_culture: list[dict[str, Any]] = []
    for rec in records:
        cid = rec["id"]
        extra = CULTURE_RAW_DATA.get(cid, {})
        item = dict(rec)
        item["indigenous_tangkhul_text"] = extra.get("tangkhul_text", [])
        item["english_translation_text"] = extra.get("english_text", [])
        item["procedural_stages"] = extra.get("procedure", [])
        item["ceremonial_participants"] = extra.get("participants", [])
        item["seasonal_timing"] = extra.get("timing", "N/A")
        enriched_culture.append(item)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "culture.json"
    bundled_json = bundled_dir / "culture.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_culture, f, ensure_ascii=False, indent=2)
    with open(bundled_json, "w", encoding="utf-8") as f:
        json.dump(enriched_culture, f, ensure_ascii=False, indent=2)

    # 2. Build PDF Document
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Cover Page
    cover_page: list[tuple[str, int, str]] = [
        ("/F2", 20, "Tangkhul Cultural Heritage Compendium"),
        ("/F2", 13, "Traditional Festivals, Proverbs, Customs, Attire & Oral Lore"),
        ("/F1", 10, "A Comprehensive Digital Preservation of Tangkhul Naga Indigenous Heritage"),
        ("/F1", 10, f"Total Catalogued Cultural Resources: {len(enriched_culture)}"),
        ("/F1", 10, "Preservation Scope: Festivals, Proverbs (Paotam), Social Institutions, Crafts & Rituals"),
        ("/F1", 10, "Format: Verbatim Indigenous Texts, English Glosses, Procedures, and Ethnography"),
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F2", 11, "Table of Cultural Heritage Resources:"),
    ]

    for idx, c in enumerate(enriched_culture, 1):
        cat_str = c.get("category", "heritage").upper()
        vlg_str = f"[{c.get('village')}]" if c.get("village") else ""
        cover_page.append(("/F1", 9, f"  {idx:>2}. [{c['id']:<14}] {c['title'][:36]:<36} ({cat_str}) {vlg_str}"))

    cover_page.extend([
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F1", 9, "Tangkhul Language Preservation Project - Digital Library Archive"),
    ])
    all_pdf_pages.append(cover_page)

    # Individual records
    for c in enriched_culture:
        # Save individual JSON
        ind_json = culture_export_dir / f"{c['id']}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(c, f, ensure_ascii=False, indent=2)

        # Build Cultural Resource PDF Page
        cult_page: list[tuple[str, int, str]] = [
            ("/F2", 16, f"{c['title']}"),
            ("/F2", 11, f"Resource Identifier: {c['id']}"),
        ]
        if c.get("title_translation"):
            cult_page.append(("/F1", 11, f"English Translation: {c['title_translation']}"))

        cult_page.extend([
            ("/F1", 10, f"Category: {c.get('category', 'culture').title()} | Subcategory: {c.get('subcategory', 'general').title()}"),
            ("/F1", 10, f"Village / Region: {c.get('village') or 'Ukhrul Region'} | Dialect: {c.get('dialect') or 'Standard Tangkhul'}"),
            ("/F1", 10, f"Contributor / Source: {c.get('creator') or 'Traditional Lore'} ({c.get('publisher') or 'Oral Heritage'})"),
            ("/F1", 10, f"License: {c.get('license') or 'Traditional Cultural Heritage'} (Permissions: {c.get('permission_status')})"),
            ("/F1", 10, f"Seasonal Timing / Occasion: {c.get('seasonal_timing', 'N/A')}"),
            ("/F1", 10, "----------------------------------------------------------------------"),
        ])

        if c.get("notes"):
            cult_page.append(("/F2", 10, "Ethnographic Summary & Context:"))
            for line in textwrap.wrap(c["notes"], width=72):
                cult_page.append(("/F1", 9, f"  {line}"))
            cult_page.append(("/F1", 8, " "))

        if c.get("indigenous_tangkhul_text"):
            cult_page.append(("/F2", 10, "Indigenous Tangkhul Text / Chants / Sayings:"))
            for t_line in c["indigenous_tangkhul_text"]:
                for wrap_line in textwrap.wrap(f'"{t_line}"', width=72):
                    cult_page.append(("/F1", 9, f"  {wrap_line}"))
            cult_page.append(("/F1", 8, " "))

        if c.get("english_translation_text"):
            cult_page.append(("/F2", 10, "English Translation & Meaning:"))
            for e_line in c["english_translation_text"]:
                for wrap_line in textwrap.wrap(f'"{e_line}"', width=72):
                    cult_page.append(("/F1", 9, f"  {wrap_line}"))
            cult_page.append(("/F1", 8, " "))

        if c.get("procedural_stages"):
            cult_page.append(("/F2", 10, "Procedural Sequence / Observance Steps:"))
            for step in c["procedural_stages"]:
                for wrap_line in textwrap.wrap(step, width=72):
                    cult_page.append(("/F1", 9, f"  {wrap_line}"))
            cult_page.append(("/F1", 8, " "))

        if c.get("ceremonial_participants"):
            parts_str = ", ".join(c["ceremonial_participants"])
            cult_page.append(("/F2", 10, "Ceremonial Participants & Roles:"))
            for wrap_line in textwrap.wrap(parts_str, width=72):
                cult_page.append(("/F1", 9, f"  {wrap_line}"))
            cult_page.append(("/F1", 8, " "))

        cult_page.extend([
            ("/F1", 8, "----------------------------------------------------------------------"),
            ("/F1", 8, "Tangkhul Language Preservation Project - Cultural Heritage Compendium"),
        ])

        # Save individual PDF
        ind_pdf_bytes = build_pdf_document([cult_page])
        ind_pdf_path = culture_export_dir / f"{c['id']}.pdf"
        ind_pdf_path.write_bytes(ind_pdf_bytes)

        # Append to master compendium
        all_pdf_pages.append(cult_page)

    # Save complete Culture Compendium PDF
    consolidated_pdf = exports_dir / "culture.pdf"
    consolidated_pdf.write_bytes(build_pdf_document(all_pdf_pages))

    return len(enriched_culture), consolidated_json, consolidated_pdf


def main() -> int:
    print("=" * 65)
    print("Tangkhul Language Library -- Culture Full JSON/PDF Exporter")
    print("=" * 65)

    n_cult, cult_json, cult_pdf = export_culture()
    print(f"OK: Exported {n_cult} Cultural Resources to:")
    print(f"    - Consolidated JSON: {cult_json}")
    print(f"    - Consolidated PDF:  {cult_pdf}")
    print(f"    - Individual files:  data/exports/culture/ ({n_cult} .json, {n_cult} .pdf)")

    # Validate generated PDF using pypdf
    print("-" * 65)
    c_reader = pypdf.PdfReader(str(cult_pdf))
    print(f"Validation: culture.pdf is valid ({len(c_reader.pages)} pages)")
    print("=" * 65)
    print("SUCCESS: All cultural resources downloaded/saved in JSON and PDF formats!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
