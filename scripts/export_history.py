#!/usr/bin/env python3
"""Export all catalogued Tangkhul historical records into structured JSON and PDF formats.

Generates:
1. Consolidated JSON collections:
   - data/exports/history.json (24 records)
   - src/tangkhul_lib/data/history.json (24 records)
2. Individual JSON documents:
   - data/exports/history/{id}.json (24 records)
3. Formatted PDF compendium & individual PDF documents:
   - data/exports/history.pdf (Complete 25-page historical compendium & chronicle)
   - data/exports/history/{id}.pdf (Individual historical record PDF documents)
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

from scripts.build_raw_history import HISTORY_RAW_DATA


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


def export_history() -> tuple[int, Path, Path]:
    """Export all catalogued historical records to consolidated and individual JSON/PDF files."""
    manifest_file = ROOT / "data" / "manifests" / "history.jsonl"
    exports_dir = ROOT / "data" / "exports"
    history_export_dir = exports_dir / "history"
    bundled_dir = ROOT / "src" / "tangkhul_lib" / "data"

    history_export_dir.mkdir(parents=True, exist_ok=True)
    bundled_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    # Enrich each record with structured texts, milestones, key figures, and terms
    enriched_history: list[dict[str, Any]] = []
    for rec in records:
        hid = rec["id"]
        extra = HISTORY_RAW_DATA.get(hid, {})
        item = dict(rec)
        item["indigenous_tangkhul_chronicle"] = extra.get("tangkhul_text", [])
        item["english_translation_text"] = extra.get("english_text", [])
        item["chronicle_milestones"] = extra.get("chronicle_milestones", [])
        item["key_figures"] = extra.get("key_figures", [])
        item["geographical_scope"] = extra.get("geographical_scope", "N/A")
        item["historical_significance"] = extra.get("historical_significance", "N/A")
        item["historical_terms"] = extra.get("vocabulary_terms", {})
        enriched_history.append(item)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "history.json"
    bundled_json = bundled_dir / "history.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_history, f, ensure_ascii=False, indent=2)
    with open(bundled_json, "w", encoding="utf-8") as f:
        json.dump(enriched_history, f, ensure_ascii=False, indent=2)

    # 2. Build Multi-Page Master Compendium PDF
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Cover Page
    cover_page: list[tuple[str, int, str]] = [
        ("/F2", 20, "Tangkhul Historical Chronicles & Gazetteer"),
        ("/F2", 13, "Events, Pioneers, Sacred Toponyms, Migrations & Treaties"),
        ("/F1", 10, "A Comprehensive Digital Preservation of Tangkhul Naga Historical Heritage"),
        ("/F1", 10, f"Total Catalogued Historical Records: {len(enriched_history)}"),
        ("/F1", 10, "Scope: Events, Biographies, Toponyms, Dispersal from Makhel, Linguistic Milestones"),
        ("/F1", 10, "Format: Tangkhul Chronicles, English Glosses, Milestones, and Terminologies"),
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F2", 11, "Table of Historical Records:"),
    ]

    for idx, h in enumerate(enriched_history, 1):
        cat_str = h.get("category", "history").upper()
        yr_str = f"[{h.get('year')}]" if h.get("year") else ""
        cover_page.append(("/F1", 9, f"  {idx:>2}. [{h['id']:<14}] {h['title'][:36]:<36} ({cat_str}) {yr_str}"))

    cover_page.extend([
        ("/F1", 10, "----------------------------------------------------------------------"),
        ("/F1", 9, "Tangkhul Language Preservation Project - Digital Library Archive"),
    ])
    all_pdf_pages.append(cover_page)

    # Individual records: create pages for both consolidated PDF and individual PDF
    for h in enriched_history:
        # Save individual JSON
        ind_json = history_export_dir / f"{h['id']}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(h, f, ensure_ascii=False, indent=2)

        # Build individual record page content
        page_items: list[tuple[str, int, str]] = [
            ("/F2", 14, f"[{h['id']}] {h['title'][:55]}"),
            ("/F2", 10, f"Translation / Context: {h.get('title_translation', 'N/A')[:65]}"),
            ("/F1", 9, f"Category: {h.get('category', 'history').upper()} | Period: {h.get('period', 'N/A')} | Date: {h.get('event_date', 'N/A')}"),
            ("/F1", 9, f"Place: {h.get('place', 'N/A')} [{h.get('village', 'N/A')}] | Dialect: {h.get('dialect', 'Ukhrul')}"),
            ("/F1", 9, f"Source: {h.get('publisher', 'N/A')[:55]} ({h.get('year', 'N/A')})"),
            ("/F1", 9, f"Clearance: {h.get('license', 'N/A')} | Permission: {h.get('permission_status', 'pending')} | Status: {h.get('verification_status', 'verified')}"),
            ("/F1", 9, "-" * 75),
        ]

        # Key Figures & Topography
        if h.get("key_figures"):
            figures_str = ", ".join(h["key_figures"])
            wrapped_fig = textwrap.wrap(f"Key Figures: {figures_str}", width=75)
            for fl in wrapped_fig:
                page_items.append(("/F2", 9, fl))

        page_items.append(("/F1", 9, f"Topography: {h.get('geographical_scope', 'N/A')[:70]}"))
        page_items.append(("/F1", 9, "-" * 75))

        # Overview & Notes
        if h.get("notes"):
            wrapped_notes = textwrap.wrap(f"Overview: {h['notes']}", width=75)
            for nl in wrapped_notes[:3]:
                page_items.append(("/F1", 9, nl))
            page_items.append(("/F1", 9, "-" * 75))

        # Indigenous Chronicle
        page_items.append(("/F2", 10, "Indigenous Tangkhul Chronicle / Oral Memory:"))
        for tline in h.get("indigenous_tangkhul_chronicle", []):
            page_items.append(("/F1", 9, f"  {tline[:72]}"))

        page_items.append(("/F1", 9, "-" * 75))

        # English Translation
        page_items.append(("/F2", 10, "English Translation & Scholarly Interpretation:"))
        for eline in h.get("english_translation_text", []):
            page_items.append(("/F1", 9, f"  {eline[:72]}"))

        page_items.append(("/F1", 9, "-" * 75))

        # Milestones / Stages
        if h.get("chronicle_milestones"):
            page_items.append(("/F2", 10, "Chronological Milestones & Key Events:"))
            for m in h["chronicle_milestones"][:4]:
                wrapped_m = textwrap.wrap(m, width=72)
                for ml in wrapped_m[:2]:
                    page_items.append(("/F1", 9, f"  {ml}"))

            page_items.append(("/F1", 9, "-" * 75))

        # Key Terminology
        if h.get("historical_terms"):
            page_items.append(("/F2", 10, "Key Tangkhul Historical Terminology:"))
            term_items = list(h["historical_terms"].items())[:3]
            for term, gloss in term_items:
                page_items.append(("/F1", 9, f"  * {term:<18} : {gloss[:50]}"))

        page_items.append(("/F1", 9, "-" * 75))
        page_items.append(("/F1", 8, f"Tangkhul Language Library - Historical Archive Record {h['id']}"))

        all_pdf_pages.append(page_items)

        # Generate Individual PDF for this history record
        ind_pdf_bytes = build_pdf_document([page_items])
        ind_pdf_path = history_export_dir / f"{h['id']}.pdf"
        with open(ind_pdf_path, "wb") as pf:
            pf.write(ind_pdf_bytes)

    # Write Master Compendium PDF
    compendium_pdf = exports_dir / "history.pdf"
    compendium_bytes = build_pdf_document(all_pdf_pages)
    with open(compendium_pdf, "wb") as pf:
        pf.write(compendium_bytes)

    # Validate output PDFs with pypdf
    reader = pypdf.PdfReader(str(compendium_pdf))
    print(f"Validated Master Compendium PDF: {len(reader.pages)} pages in {compendium_pdf.name}")

    return len(enriched_history), consolidated_json, compendium_pdf


if __name__ == "__main__":
    count, json_path, pdf_path = export_history()
    print("\n=======================================================")
    print(f"SUCCESS: Exported {count} historical records!")
    print(f"  Consolidated JSON: {json_path}")
    print(f"  Consolidated PDF:  {pdf_path}")
    print(f"  Individual JSONs:  data/exports/history/ ({count} files)")
    print(f"  Individual PDFs:   data/exports/history/ ({count} files)")
    print("=======================================================")
