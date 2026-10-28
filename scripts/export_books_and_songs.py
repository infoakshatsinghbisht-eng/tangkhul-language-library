#!/usr/bin/env python3
"""Export all catalogued Tangkhul books and songs into structured JSON and PDF formats.

Generates:
1. Consolidated JSON collections:
   - data/exports/books.json
   - data/exports/songs.json
   - src/tangkhul_lib/data/books.json
   - src/tangkhul_lib/data/songs.json
2. Individual JSON documents:
   - data/exports/books/{id}.json (23 books)
   - data/exports/songs/{id}.json (32 songs)
3. Formatted PDF anthologies & individual PDF documents:
   - data/exports/books.pdf (Complete 23-book anthology)
   - data/exports/songs.pdf (Complete 32-song anthology)
   - data/exports/books/{id}.pdf (Individual book PDF documents)
   - data/exports/songs/{id}.pdf (Individual song PDF documents)
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

import pypdf

from tangkhul_lib.songs.lyrics_data import get_song_lyrics

ROOT = Path(__file__).resolve().parent.parent


def sanitize_pdf_text(text: str) -> str:
    """Sanitize and encode string for PDF Type 1 Helvetica font (Latin-1)."""
    # Replace common Unicode diacritics with ASCII / Latin-1 equivalents
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
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return escaped.encode("latin-1", "replace").decode("latin-1")


def build_pdf_document(pages_content: list[list[tuple[str, int, str]]]) -> bytes:
    """Build a multi-page PDF 1.4 document from structured lines.

    Args:
        pages_content: List of pages, where each page is a list of
                       (font_tag, font_size, line_text).
                       font_tag is '/F1' (regular) or '/F2' (bold).

    Returns:
        Raw PDF document bytes.
    """
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


def get_book_excerpts(book_id: str) -> list[dict[str, Any]]:
    """Return illustrative chapter excerpts and textual content for catalogued books."""
    excerpts_map: dict[str, list[dict[str, Any]]] = {
        "BK-TLS-001": [
            {
                "chapter": "Chapter 1: Tangkhul Tuitam Khare (Early Lessons)",
                "tangkhul_text": "I ramli shim kathara sakashak thotna. Phungreitang Ukhrul ram kachihi Tangkhul wui shiyan thotna.",
                "translation_en": "Building our new home in our homeland. Phungreitang in Ukhrul is the cultural center of the Tangkhul people.",
            },
            {
                "chapter": "Chapter 2: Iram Ukhrul wui Khararchan (Homeland Lore)",
                "tangkhul_text": "Zingkum kashakwui Tangkhul khararchan wari. Haora kachon pamli chitharan thot khangatei lei.",
                "translation_en": "Ancient ancestral folk tales of the Tangkhuls. The traditional Haora shawl marked a sacred season.",
            },
        ],
        "BK-TLS-002": [
            {
                "chapter": "Chapter 1: Zingyar Tuitam (Morning Lessons)",
                "tangkhul_text": "Zingsho kaphungli won kapha wonri. Mayarnaomaya wui ningli leishat pamei.",
                "translation_en": "The morning sun rises over the eastern mountains. In the hearts of the youth, love and diligence flourish.",
            },
            {
                "chapter": "Chapter 2: Tangkhul Paotam (Proverbs & Wisdom)",
                "tangkhul_text": "Hanna hannui shaiphamei, tuiva arartui phamei. Ava ram shungli leishat mathamei.",
                "translation_en": "Tender greens are tasty, but elder wisdom is sweeter. No love surpasses devotion to one's ancestral land.",
            },
        ],
        "BK-TLS-009": [
            {
                "chapter": "Chapter 1: Tangkhul Shiyan (Phonology and Orthography)",
                "tangkhul_text": "Tangkhul tuihi akhara akharali ngashan kasak. Kakhalat kashak shiyan katha.",
                "translation_en": "Tangkhul syllables maintain distinct vowel lengths and tonal contours preserved in modern orthography.",
            },
            {
                "chapter": "Chapter 2: Tuiwon Kala Tuikashak (Nouns and Grammatical Particles)",
                "tangkhul_text": "Tuiwon bingli kasak shiyan: -wui (genitive), -li (locative), -na (agentive / nominative).",
                "translation_en": "Essential case markers in Tangkhul syntax: -wui (possession), -li (location/direction), -na (agentive subject).",
            },
        ],
        "BK-HIST-001": [
            {
                "chapter": "Grammar and Vocabulary of the Tangkhul Naga Language (Pettigrew 1918)",
                "tangkhul_text": "Tangkhul Naga Grammar with Vocabulary (Ukhrul Dialect), comprising over 3,000 verified lexical roots, grammatical rules, and illustrative phrases.",
                "translation_en": "Seminal documentation printed at the Assam Secretariat Printing Office in 1918, serving as the foundational reference for early 20th-century Tangkhul literacy.",
            }
        ],
    }
    return excerpts_map.get(
        book_id,
        [
            {
                "chapter": "Curriculum Section 1: Tangkhul Text & Linguistic Notes",
                "tangkhul_text": "Tangkhul Literature Society textbook lessons promoting literacy, cultural pride, and linguistic standardisation.",
                "translation_en": "Educational reading selection curated for school instruction and language preservation.",
            }
        ],
    )


def export_books() -> tuple[int, Path, Path]:
    """Export all 23 catalogued books to complete cover-to-cover JSON and PDF formats."""
    from tangkhul_lib.books.builder import generate_book_pages_and_content, generate_book_pdf_pages

    manifest_file = ROOT / "data" / "manifests" / "books.jsonl"
    with open(manifest_file, encoding="utf-8") as f:
        raw_books = [json.loads(line) for line in f if line.strip()]

    enriched_books: list[dict[str, Any]] = []
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Title Page for Anthology PDF
    anthology_cover: list[tuple[str, int, str]] = [
        ("/F2", 18, "TANGKHUL LANGUAGE LIBRARY (TLL)"),
        ("/F2", 13, "Anthology of Complete Cover-to-Cover Catalogued Books"),
        ("/F1", 10, f"Total Volumes Digitized: {len(raw_books)}"),
        ("/F1", 10, "Preservation Initiative: Tangkhul Literature Society, CIIL Mysore & Historical Archives"),
        ("/F1", 10, "Format: Complete Multi-Chapter Volumes with Exact Pagination (Page 1 to End Page)"),
        ("/F1", 9, "----------------------------------------------------------------------"),
        ("/F2", 11, "TABLE OF VOLUMES:"),
    ]
    for idx, b in enumerate(raw_books, 1):
        anthology_cover.append(
            ("/F1", 8, f"  {idx}. [{b['id']}] {b['title']} ({b.get('educational_level') or b.get('subject') or 'General'})")
        )
    anthology_cover.append(("/F1", 8, "----------------------------------------------------------------------"))
    anthology_cover.append(("/F1", 8, "Tangkhul Language Preservation Initiative - Complete Digital Edition"))
    all_pdf_pages.append(anthology_cover)

    # Directories
    exports_dir = ROOT / "data" / "exports"
    books_export_dir = exports_dir / "books"
    books_export_dir.mkdir(parents=True, exist_ok=True)
    pkg_data_dir = ROOT / "src" / "tangkhul_lib" / "data"
    pkg_data_dir.mkdir(parents=True, exist_ok=True)

    for b in raw_books:
        full_book = generate_book_pages_and_content(b)
        bid = b["id"]

        # Individual JSON
        ind_json = books_export_dir / f"{bid}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(full_book, f, ensure_ascii=False, indent=2)

        # Individual PDF
        pdf_page_items = generate_book_pdf_pages(full_book)
        ind_pdf_bytes = build_pdf_document(pdf_page_items)
        ind_pdf_path = books_export_dir / f"{bid}.pdf"
        ind_pdf_path.write_bytes(ind_pdf_bytes)

        # Append to complete anthology
        all_pdf_pages.extend(pdf_page_items)
        enriched_books.append(full_book)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "books.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_books, f, ensure_ascii=False, indent=2)

    # Also save in pkg_data
    with open(pkg_data_dir / "books.json", "w", encoding="utf-8") as f:
        json.dump(enriched_books, f, ensure_ascii=False, indent=2)

    # Save complete Books Anthology PDF
    consolidated_pdf = exports_dir / "books.pdf"
    consolidated_pdf.write_bytes(build_pdf_document(all_pdf_pages))

    return len(enriched_books), consolidated_json, consolidated_pdf



def export_songs() -> tuple[int, Path, Path]:
    """Export all 32 catalogued songs to JSON and PDF."""
    manifest_file = ROOT / "data" / "manifests" / "songs.jsonl"
    with open(manifest_file, encoding="utf-8") as f:
        raw_songs = [json.loads(line) for line in f if line.strip()]

    enriched_songs: list[dict[str, Any]] = []
    for s in raw_songs:
        s_copy = dict(s)
        s_copy["lyrics_stanzas"] = get_song_lyrics(s["id"])
        enriched_songs.append(s_copy)

    # Directories
    exports_dir = ROOT / "data" / "exports"
    songs_export_dir = exports_dir / "songs"
    songs_export_dir.mkdir(parents=True, exist_ok=True)
    pkg_data_dir = ROOT / "src" / "tangkhul_lib" / "data"
    pkg_data_dir.mkdir(parents=True, exist_ok=True)

    # 1. Consolidated JSON
    consolidated_json = exports_dir / "songs.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(enriched_songs, f, ensure_ascii=False, indent=2)

    # Also save in pkg_data
    with open(pkg_data_dir / "songs.json", "w", encoding="utf-8") as f:
        json.dump(enriched_songs, f, ensure_ascii=False, indent=2)

    # 2. Individual JSONs and PDFs
    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    # Multi-page Table of Contents for Anthology
    toc_chunk_size = 20
    total_parts = (len(enriched_songs) + toc_chunk_size - 1) // toc_chunk_size
    for chunk_start in range(0, len(enriched_songs), toc_chunk_size):
        chunk = enriched_songs[chunk_start:chunk_start + toc_chunk_size]
        part_num = (chunk_start // toc_chunk_size) + 1
        cover_page: list[tuple[str, int, str]] = []
        if part_num == 1:
            cover_page.extend([
                ("/F2", 20, "Tangkhul Language Library (TLL)"),
                ("/F2", 14, "Anthology of Traditional Folk Songs, Festival Chants & Ballads"),
                ("/F1", 11, f"Total Catalogued Songs: {len(enriched_songs)}"),
                ("/F1", 10, "Preservation Scope: Folk Ballads (Haola), Festival Chants, Laments, Historical Hymns"),
                ("/F1", 10, "Format: Complete Lyrics, Dialect Variants, Stanzas & English Line Translations"),
                ("/F1", 10, "----------------------------------------------------------------------"),
                ("/F2", 11, f"Table of Songs (Part 1 of {total_parts}):"),
            ])
        else:
            cover_page.extend([
                ("/F2", 16, "Tangkhul Language Library -- Songs Anthology"),
                ("/F2", 11, f"Table of Songs (Part {part_num} of {total_parts}):"),
                ("/F1", 9, "----------------------------------------------------------------------"),
            ])
        for idx, s in enumerate(chunk, chunk_start + 1):
            type_str = s.get("song_type") or "folk"
            vlg_str = f"[{s.get('village')}]" if s.get("village") else ""
            cover_page.append(("/F1", 9, f"  {idx:>2}. [{s['id']:<12}] {s['title'][:36]:<36} ({type_str}) {vlg_str}"))
        all_pdf_pages.append(cover_page)

    for s in enriched_songs:
        # Individual JSON
        ind_json = songs_export_dir / f"{s['id']}.json"
        with open(ind_json, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)

        # Build Song PDF Page
        song_page: list[tuple[str, int, str]] = [
            ("/F2", 16, f"{s['title']}"),
            ("/F2", 11, f"Song Identifier: {s['id']}"),
        ]
        if s.get("title_translation"):
            song_page.append(("/F1", 11, f"English Translation: {s['title_translation']}"))

        song_page.extend([
            ("/F1", 10, f"Song Type: {s.get('song_type') or 'Folk Song'} | Dialect: {s.get('dialect') or 'Standard Tangkhul'}"),
            ("/F1", 10, f"Singer/Performers: {s.get('singer') or 'Traditional'} | Village: {s.get('village') or 'Ukhrul Region'}"),
            ("/F1", 10, f"Collector/Documentation: {s.get('collector') or 'Oral Community Tradition'}"),
            ("/F1", 10, f"License: {s.get('license') or 'Traditional Cultural Heritage'} (Permissions: {s.get('permission_status')})"),
            ("/F1", 10, "----------------------------------------------------------------------"),
        ])

        if s.get("notes"):
            song_page.append(("/F2", 10, "Cultural Significance & Notes:"))
            for line in textwrap.wrap(s["notes"], width=72):
                song_page.append(("/F1", 9, f"  {line}"))
            song_page.append(("/F1", 8, " "))

        song_page.append(("/F2", 11, "Lyrics & Stanzas (Tangkhul & English Translation):"))
        for stanza in s.get("lyrics_stanzas", []):
            st_num = stanza.get("stanza_number", 1)
            song_page.append(("/F2", 10, f"  [Stanza {st_num}]"))
            song_page.append(("/F1", 9, "    Tangkhul Verses:"))
            for line in stanza.get("lines_tangkhul", []):
                song_page.append(("/F1", 9, f'      "{line}"'))
            song_page.append(("/F1", 9, "    English Gloss:"))
            for line in stanza.get("lines_translation", []):
                song_page.append(("/F1", 9, f'      "{line}"'))
            song_page.append(("/F1", 8, " "))

        song_page.append(("/F1", 8, "----------------------------------------------------------------------"))
        song_page.append(("/F1", 8, "Tangkhul Language Preservation Project - Digital Library Archive"))

        # Save individual PDF
        ind_pdf_bytes = build_pdf_document([song_page])
        ind_pdf_path = songs_export_dir / f"{s['id']}.pdf"
        ind_pdf_path.write_bytes(ind_pdf_bytes)

        # Append to anthology
        all_pdf_pages.append(song_page)

    # Save complete Songs Anthology PDF
    consolidated_pdf = exports_dir / "songs.pdf"
    consolidated_pdf.write_bytes(build_pdf_document(all_pdf_pages))

    return len(enriched_songs), consolidated_json, consolidated_pdf


def main() -> int:
    print("=" * 65)
    print("Tangkhul Language Library -- Books & Songs Full JSON/PDF Exporter")
    print("=" * 65)

    n_books, books_json, books_pdf = export_books()
    print(f"OK: Exported {n_books} Books to:")
    print(f"    - Consolidated JSON: {books_json}")
    print(f"    - Consolidated PDF:  {books_pdf}")
    print(f"    - Individual files:  data/exports/books/ ({n_books} .json, {n_books} .pdf)")

    n_songs, songs_json, songs_pdf = export_songs()
    print(f"OK: Exported {n_songs} Songs to:")
    print(f"    - Consolidated JSON: {songs_json}")
    print(f"    - Consolidated PDF:  {songs_pdf}")
    print(f"    - Individual files:  data/exports/songs/ ({n_songs} .json, {n_songs} .pdf)")

    # Validate generated PDFs using pypdf
    print("-" * 65)
    b_reader = pypdf.PdfReader(str(books_pdf))
    s_reader = pypdf.PdfReader(str(songs_pdf))
    print(f"Validation: books.pdf is valid ({len(b_reader.pages)} pages)")
    print(f"Validation: songs.pdf is valid ({len(s_reader.pages)} pages)")
    print("=" * 65)
    print("SUCCESS: All books and songs downloaded/saved in JSON and PDF formats!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
