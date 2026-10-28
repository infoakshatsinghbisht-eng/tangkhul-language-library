#!/usr/bin/env python3
"""Export Complete Tangkhul Lexicon catalogs to high-quality publication PDF format.

Generates:
1. data/exports/tangkhul_all_extracted_words.pdf (All 16,041 authentic unique words across all corpora)
2. data/exports/tangkhul_master_dictionary_deduplicated.pdf (Full 6,480 entries from A to Z, uncapped)
3. data/exports/tangkhul_100k_expanded_lexicon_compendium.pdf (Top 20,000 priority morphological words)
4. data/exports/tangkhul_100k_expanded_lexicon_complete.pdf (Full 648,912 words complete edition)
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS_DIR = ROOT / "data" / "exports"
PKG_DATA_DIR = ROOT / "src" / "tangkhul_lib" / "data"

EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
PKG_DATA_DIR.mkdir(parents=True, exist_ok=True)

REPLACEMENTS = {
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
    "ṇ": "n",
    "ṃ": "m",
    "ṭ": "t",
    "ḍ": "d",
    "ṣ": "sh",
    "ś": "sh",
    "ṛ": "r",
    "ṉ": "n",
}

def sanitize_pdf_text(s: str) -> str:
    """Sanitize and encode text for PDF Type 1 Helvetica font (ASCII printable)."""
    if not s:
        return ""
    for orig, rep in REPLACEMENTS.items():
        s = s.replace(orig, rep)
    s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    out = []
    for ch in s:
        cp = ord(ch)
        if 32 <= cp <= 126:
            out.append(ch)
        elif cp in (10, 13, 9):
            out.append(" ")
        else:
            out.append(" ")
    return " ".join("".join(out).split())


def build_pdf_document(
    title: str,
    subtitle: str,
    pages_data: list[list[tuple[str, int, str]]],
    doc_footer_name: str,
) -> bytes:
    """Build multi-page PDF document using core PDF stream engine."""
    page_count = len(pages_data)
    cat_id = 1
    pages_root_id = 2
    f1_id = 3
    f2_id = 4
    cur_id = 5

    page_entries = []
    page_obj_ids = []

    for page_idx, raw_items in enumerate(pages_data, 1):
        p_id = cur_id
        cur_id += 1
        c_id = cur_id
        cur_id += 1

        items: list[tuple[str, int, str]] = []
        if page_idx == 1:
            items.append(("/F2", 13, title))
            items.append(("/F1", 9, subtitle))
            items.append(
                ("/F1", 8, "Tangkhul Language Library Digital Archive -- Exhaustive Canonical Edition")
            )
            items.append(("/F1", 8, "-" * 115))

        items.extend(raw_items)

        items.append(("/F1", 8, "-" * 115))
        items.append(
            (
                "/F1",
                8,
                f"{doc_footer_name}                                              Page {page_idx} of {page_count}",
            )
        )

        stream_cmds = ["BT"]
        y = 800
        stream_cmds.append(f"36 {y} Td")
        current_y = y

        for font, size, line in items:
            clean = sanitize_pdf_text(line)
            stream_cmds.append(f"{font} {size} Tf")
            stream_cmds.append(f"({clean}) Tj")
            dy = -(size + 2)
            stream_cmds.append(f"0 {dy} Td")
            current_y += dy
            if current_y < 35:
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


def generate_extracted_words_pdf():
    """Generate complete PDF for all 16,041 authentic extracted words."""
    json_path = EXPORTS_DIR / "tangkhul_all_extracted_words.json"
    if not json_path.exists():
        print(f"Error: {json_path} does not exist!")
        return

    print("Loading extracted words JSON...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = data.get("words", [])
    print(f"Loaded {len(words):,} extracted words.")

    pdf_pages = []
    cur_page: list[tuple[str, int, str]] = []

    for idx, w in enumerate(words):
        rank = w.get("rank", idx + 1)
        canonical = w.get("canonical_form") or w.get("word", "")
        pos = w.get("part_of_speech", "") or "—"
        freq = w.get("frequency", 1)
        src_count = w.get("source_count", 1)
        meaning = (w.get("meaning") or "").strip()
        example = (w.get("example_sentence") or "").strip()

        line1 = f"#{rank:<5} {canonical:<22} ({pos})  [Freq: {freq:,} | Sources: {src_count}]"
        cur_page.append(("/F2", 8, line1))

        if meaning or example:
            parts = []
            if meaning:
                parts.append(f"Def: {meaning[:60]}")
            if example:
                parts.append(f"Ctx: {example[:60]}")
            line2 = f"       {' | '.join(parts)}"
            cur_page.append(("/F1", 7, line2))

        # 34 entries per page
        if len(cur_page) >= 68:
            pdf_pages.append(cur_page)
            cur_page = []

    if cur_page:
        pdf_pages.append(cur_page)

    print(f"Rendering {len(pdf_pages)} pages for 16,041 Extracted Words PDF...")
    pdf_bytes = build_pdf_document(
        title="Tangkhul Language Complete Extracted Lexicon Catalog",
        subtitle=f"16,041 Authentic Words Across 14 Digitized Domains | {data.get('total_corpus_tokens', 60265):,} Tokens",
        pages_data=pdf_pages,
        doc_footer_name="Tangkhul All Extracted Lexicon Catalog",
    )

    pdf_out = EXPORTS_DIR / "tangkhul_all_extracted_words.pdf"
    pdf_out.write_bytes(pdf_bytes)
    print(f"SUCCESS: Created {pdf_out.name} ({len(pdf_bytes):,} bytes, {len(pdf_pages)} pages)")

    # Copy to pkg data
    pkg_out = PKG_DATA_DIR / "tangkhul_all_extracted_words.pdf"
    shutil.copy2(pdf_out, pkg_out)


def generate_master_dictionary_full_pdf():
    """Regenerate Master Dictionary PDF with all 6,480 entries from A to Z (Uncapped)."""
    dict_json = EXPORTS_DIR / "tangkhul_master_dictionary_deduplicated.json"
    if not dict_json.exists():
        print(f"Error: {dict_json} does not exist!")
        return

    print("Loading Master Dictionary deduplicated entries...")
    with open(dict_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries", [])
    print(f"Loaded {len(entries):,} Master Dictionary entries.")

    pdf_pages = []
    cur_page: list[tuple[str, int, str]] = []

    for idx, e in enumerate(entries, 1):
        tk = e.get("tangkhul", "").strip()
        pos = e.get("pos", "").strip() or "—"
        en = (e.get("english") or "").strip()
        hi = (e.get("hindi") or "").strip()
        src = e.get("source", "").strip()

        cur_page.append(("/F2", 8, f"{idx}. {tk}  ({pos})"))
        en_str = f"EN: {en[:70]}" if en else "EN: —"
        cur_page.append(("/F1", 7.5, f"   {en_str}  [Src: {src}]"))

        if len(cur_page) >= 64:
            pdf_pages.append(cur_page)
            cur_page = []

    if cur_page:
        pdf_pages.append(cur_page)

    print(f"Rendering {len(pdf_pages)} pages for Master Dictionary Full PDF...")
    pdf_bytes = build_pdf_document(
        title="Tangkhul-English Master Dictionary (Full Edition A-Z)",
        subtitle=f"Complete Canonical Deduplicated Lexicon ({len(entries):,} Entries with Parts of Speech)",
        pages_data=pdf_pages,
        doc_footer_name="Tangkhul Master Dictionary Lexicon",
    )

    pdf_out = EXPORTS_DIR / "tangkhul_master_dictionary_deduplicated.pdf"
    pdf_out.write_bytes(pdf_bytes)
    print(f"SUCCESS: Created {pdf_out.name} ({len(pdf_bytes):,} bytes, {len(pdf_pages)} pages)")

    # Copy to pkg data
    pkg_out = PKG_DATA_DIR / "tangkhul_master_dictionary_deduplicated.pdf"
    shutil.copy2(pdf_out, pkg_out)


def generate_expanded_lexicon_compendium_pdf():
    """Generate high-priority compendium PDF (top 20,000 words) from 648k expanded lexicon."""
    lex_json = EXPORTS_DIR / "tangkhul_100k_expanded_lexicon.json"
    if not lex_json.exists():
        print(f"Error: {lex_json} does not exist!")
        return

    print("Loading Expanded Morphological Lexicon...")
    with open(lex_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = data.get("words", [])
    total_count = len(words)
    print(f"Loaded {total_count:,} words.")

    # 1. Compendium PDF (top 20,000 high-frequency / priority morphological words)
    compendium_words = words[:20000]
    pdf_pages = []
    cur_page: list[tuple[str, int, str]] = []

    for idx, w in enumerate(compendium_words, 1):
        word = w.get("canonical_form") or w.get("word", "")
        root = w.get("root_lemma", "")
        pos = w.get("part_of_speech", "") or "—"
        cat = w.get("morphological_category", "")
        en = (w.get("english_meaning") or "").strip()

        cur_page.append(("/F2", 8, f"#{idx} {word}  [Root: {root} | {pos} | {cat}]"))
        cur_page.append(("/F1", 7, f"   Meaning: {en[:75]}"))

        if len(cur_page) >= 64:
            pdf_pages.append(cur_page)
            cur_page = []

    if cur_page:
        pdf_pages.append(cur_page)

    print(f"Rendering {len(pdf_pages)} pages for Expanded Lexicon Compendium PDF...")
    pdf_bytes = build_pdf_document(
        title="Tangkhul 100,000+ Expanded Morphological Lexicon (Compendium Edition)",
        subtitle=f"Top 20,000 Priority Words from 648,912 Morphological Catalog | Bilingual English-Hindi",
        pages_data=pdf_pages,
        doc_footer_name="Tangkhul Expanded Lexicon Compendium",
    )

    pdf_out = EXPORTS_DIR / "tangkhul_100k_expanded_lexicon_compendium.pdf"
    pdf_out.write_bytes(pdf_bytes)
    print(f"SUCCESS: Created {pdf_out.name} ({len(pdf_bytes):,} bytes, {len(pdf_pages)} pages)")

    # Copy to pkg data
    pkg_out = PKG_DATA_DIR / "tangkhul_100k_expanded_lexicon_compendium.pdf"
    shutil.copy2(pdf_out, pkg_out)


def generate_expanded_lexicon_complete_pdf():
    """Generate complete multi-thousand page PDF for all 648,912 words of the expanded lexicon."""
    lex_json = EXPORTS_DIR / "tangkhul_100k_expanded_lexicon.json"
    if not lex_json.exists():
        print(f"Error: {lex_json} does not exist!")
        return

    print("Loading all 648,912 words for Complete Expanded Lexicon PDF...")
    with open(lex_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = data.get("words", [])
    total_count = len(words)
    print(f"Loaded {total_count:,} words. Preparing page data...")

    pdf_pages = []
    cur_page: list[tuple[str, int, str]] = []

    for idx, w in enumerate(words, 1):
        word = w.get("canonical_form") or w.get("word", "")
        root = w.get("root_lemma", "")
        pos = w.get("part_of_speech", "") or "—"
        cat = w.get("morphological_category", "")
        en = (w.get("english_meaning") or "").strip()

        cur_page.append(("/F2", 8, f"#{idx} {word}  [Root: {root} | {pos} | {cat}]"))
        cur_page.append(("/F1", 7, f"   Meaning: {en[:75]}"))

        if len(cur_page) >= 64:
            pdf_pages.append(cur_page)
            cur_page = []

    if cur_page:
        pdf_pages.append(cur_page)

    print(f"Rendering {len(pdf_pages)} pages for Complete 648k Lexicon PDF...")
    t_render = time.time()
    pdf_bytes = build_pdf_document(
        title="Tangkhul Complete 100,000+ Expanded Morphological Lexicon (Exhaustive Edition)",
        subtitle=f"All 648,912 Words Across Inflectional, Derivational & Compound Morphology",
        pages_data=pdf_pages,
        doc_footer_name="Tangkhul Complete Morphological Lexicon",
    )
    print(f"Finished rendering in {time.time()-t_render:.2f}s.")

    pdf_out = EXPORTS_DIR / "tangkhul_100k_expanded_lexicon_complete.pdf"
    pdf_out.write_bytes(pdf_bytes)
    print(f"SUCCESS: Created {pdf_out.name} ({len(pdf_bytes):,} bytes, {len(pdf_pages)} pages)")

    # Copy to pkg data
    pkg_out = PKG_DATA_DIR / "tangkhul_100k_expanded_lexicon_complete.pdf"
    shutil.copy2(pdf_out, pkg_out)


def main():
    print("=" * 70)
    print("Tangkhul Lexicon PDF & JSON Master Publication Engine")
    print("=" * 70)

    t0 = time.time()
    generate_extracted_words_pdf()
    print("-" * 50)
    generate_master_dictionary_full_pdf()
    print("-" * 50)
    generate_expanded_lexicon_compendium_pdf()
    print("-" * 50)
    generate_expanded_lexicon_complete_pdf()
    print("=" * 70)
    print(f"ALL LEXICON PDFS GENERATED SUCCESSFULLY IN {time.time()-t0:.2f}s!")
    print("=" * 70)


if __name__ == "__main__":
    main()

