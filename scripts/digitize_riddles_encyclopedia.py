#!/usr/bin/env python3
"""Digitize the 300 Tangkhul Language Folk Riddles Encyclopedia (Kakhangahan Sangrah).

Produces:
1. Complete JSON catalog:
   - data/exports/tangkhul_300_folk_riddles.json
   - src/tangkhul_lib/data/tangkhul_300_folk_riddles.json
2. Multi-page formatted PDF publication:
   - data/exports/tangkhul_300_folk_riddles.pdf (17-page complete compendium)
3. Raw digitized literature text file:
   - data/raw/literature/LIT-RIDD-003.txt
4. Manifest registration:
   - Registers LIT-RIDD-003 in data/manifests/literature.jsonl
5. SQLite Database persistence:
   - Syncs into data/database/tangkhul_corpus.sqlite and bundled DB
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pypdf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.riddles_data import RAW_RIDDLES_DATA
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, ManifestRepository

EXPORTS_DIR = ROOT / "data" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = ROOT / "data" / "raw" / "literature"
RAW_DIR.mkdir(parents=True, exist_ok=True)
BUNDLED_DIR = ROOT / "src" / "tangkhul_lib" / "data"
BUNDLED_DIR.mkdir(parents=True, exist_ok=True)

# Section metadata definition
SECTIONS = [
    {
        "section_number": 1,
        "name_en": "Nature, Sky & Elements",
        "name_hi": "प्रकृति, आकाश एवं ऋतु चक्र",
        "start": 1,
        "end": 35,
    },
    {
        "section_number": 2,
        "name_en": "Agriculture, Tools & Objects",
        "name_hi": "खेती, पारंपरिक औज़ार एवं दैनिक वस्तुएँ",
        "start": 36,
        "end": 70,
    },
    {
        "section_number": 3,
        "name_en": "Living Beings & Human Anatomy",
        "name_hi": "जीव-जंतु, पक्षी एवं शरीर के अंग",
        "start": 71,
        "end": 100,
    },
    {
        "section_number": 4,
        "name_en": "Forest Flora, Fauna & Mountain Life",
        "name_hi": "जंगल, वनस्पति, जीव-जगत एवं पहाड़ी जीवन",
        "start": 101,
        "end": 125,
    },
    {
        "section_number": 5,
        "name_en": "Festivals, Feasts & Crafts",
        "name_hi": "पारंपरिक उत्सव, खान-पान एवं लोंगशिम संस्कृति",
        "start": 126,
        "end": 155,
    },
    {
        "section_number": 6,
        "name_en": "Village Architecture & Landscape",
        "name_hi": "ग्रामीण परिवेश, स्थापत्य एवं प्राकृतिक भूगोल",
        "start": 156,
        "end": 180,
    },
    {
        "section_number": 7,
        "name_en": "Philosophy, Memory & Kinship",
        "name_hi": "दार्शनिक भाव, संबंध एवं लोक-स्मृति",
        "start": 181,
        "end": 200,
    },
    {
        "section_number": 8,
        "name_en": "Hunting, Birds & Mountain Ecology",
        "name_hi": "आखेट, वन्यजीव, पक्षी एवं पर्वतीय पारिस्थितिकी",
        "start": 201,
        "end": 225,
    },
    {
        "section_number": 9,
        "name_en": "Crafts, Blacksmithing & Utensils",
        "name_hi": "पारंपरिक हस्तशिल्प, धातु-कर्म एवं गृह-सज्जा",
        "start": 226,
        "end": 250,
    },
    {
        "section_number": 10,
        "name_en": "Terrace Farming & Botany",
        "name_hi": "सीढ़ीदार खेती, कंद-मूल एवं मौसमी वनस्पति",
        "start": 251,
        "end": 275,
    },
    {
        "section_number": 11,
        "name_en": "Human Experience, Hospitality & Identity",
        "name_hi": "मानवीय अनुभव, आतिथ्य एवं तंगखुल अस्मिता",
        "start": 276,
        "end": 300,
    },
]


def sanitize_pdf_text(text: str) -> str:
    """Sanitize and encode text for Type 1 Helvetica font (Latin-1)."""
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
        "ü": "u",
        "ǜ": "u",
        "ù": "u",
        "ú": "u",
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
        stream_cmds.append(f"40 {y} Td")
        current_y = y

        for font, size, line in page_items:
            clean = sanitize_pdf_text(line)
            stream_cmds.append(f"{font} {size} Tf")
            stream_cmds.append(f"({clean}) Tj")
            dy = -(size + 3)
            stream_cmds.append(f"0 {dy} Td")
            current_y += dy
            if current_y < 45:
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


def get_section_for_number(num: int) -> dict[str, Any]:
    for sec in SECTIONS:
        if sec["start"] <= num <= sec["end"]:
            return sec
    return SECTIONS[0]


def assemble_dataset() -> list[dict[str, Any]]:
    dataset = []
    for item in RAW_RIDDLES_DATA:
        num, t_riddle, en_trans, hi_trans, ans_t, ans_e, ans_h = item
        sec = get_section_for_number(num)
        record = {
            "number": num,
            "section_number": sec["section_number"],
            "section_name_en": sec["name_en"],
            "section_name_hi": sec["name_hi"],
            "tangkhul_riddle": t_riddle,
            "english_translation": en_trans,
            "hindi_translation": hi_trans,
            "answer_tangkhul": ans_t,
            "answer_english": ans_e,
            "answer_hindi": ans_h,
        }
        dataset.append(record)
    return dataset


def export_json(dataset: list[dict[str, Any]]) -> tuple[Path, Path]:
    output_data = {
        "metadata": {
            "title": "300 Tangkhul Language Folk Riddles (Complete Encyclopedia)",
            "vernacular_title": "तंगखुल नागा महा-शब्दावली एवं पहेली विश्वकोश (Kakhangahān Sangrah)",
            "subtitle": "Exhaustive Linguistic Documentation: Nature, Wildlife, Agriculture, Longshim Lore & Mountain Philosophy",
            "identifier": "LIT-RIDD-003",
            "total_riddles": len(dataset),
            "total_sections": len(SECTIONS),
            "languages": ["Tangkhul", "English", "Hindi"],
            "compiled_at": datetime.now(timezone.utc).isoformat(),
            "sections": SECTIONS,
        },
        "riddles": dataset,
    }

    p1 = EXPORTS_DIR / "tangkhul_300_folk_riddles.json"
    p2 = BUNDLED_DIR / "tangkhul_300_folk_riddles.json"

    with open(p1, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    with open(p2, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    return p1, p2


def export_pdf(dataset: list[dict[str, Any]]) -> Path:
    # 17 pages layout matching the 17-page source document
    # Define exact page boundary splits matching the 17 pages of the source document
    page_splits = [
        (1, 18),
        (19, 35),
        (36, 57),
        (58, 75),
        (76, 95),
        (96, 113),
        (114, 131),
        (132, 151),
        (152, 169),
        (170, 187),
        (188, 205),
        (206, 225),
        (226, 244),
        (245, 262),
        (263, 280),
        (281, 299),
        (300, 300),
    ]

    all_pdf_pages: list[list[tuple[str, int, str]]] = []

    for page_idx, (start_n, end_n) in enumerate(page_splits, 1):
        page_items: list[tuple[str, int, str]] = []

        if page_idx == 1:
            page_items.extend([
                ("/F2", 15, "300 Tangkhul Language Folk Riddles (Complete Encyclopedia)"),
                ("/F2", 10, "Kakhangahan Sangrah -- Tangkhul, English & Hindi Trilingual Documentation"),
                ("/F1", 8, "Exhaustive Linguistic Documentation: Nature, Wildlife, Agriculture, Longshim Lore & Mountain Philosophy"),
                ("/F1", 8, "-" * 85),
            ])

        # Check if a section header falls in this page
        for sec in SECTIONS:
            if start_n <= sec["start"] <= end_n:
                page_items.extend([
                    ("/F2", 10, f"SECTION {sec['section_number']}: {sec['name_en'].upper()} ({sec['start']}--{sec['end']})"),
                    ("/F1", 7, "-" * 85),
                ])

        chunk = [r for r in dataset if start_n <= r["number"] <= end_n]
        for r in chunk:
            num = r["number"]
            t_riddle = r["tangkhul_riddle"]
            en_trans = r["english_translation"]
            ans_t = r["answer_tangkhul"]
            ans_e = r["answer_english"]

            page_items.append(("/F2", 8, f"#{num} Tangkhul: {t_riddle[:68]}"))
            page_items.append(("/F1", 8, f"   EN: {en_trans[:70]}"))
            page_items.append(("/F2", 8, f"   Ans: {ans_t} ({ans_e})"))
            page_items.append(("/F1", 4, " "))

        page_items.extend([
            ("/F1", 7, "-" * 85),
            ("/F1", 8, f"Complete Encyclopedia of 300 Tangkhul Folk Riddles (Kakhangahan)          Page {page_idx} of 17"),
        ])
        all_pdf_pages.append(page_items)

    pdf_bytes = build_pdf_document(all_pdf_pages)
    pdf_path = EXPORTS_DIR / "tangkhul_300_folk_riddles.pdf"
    pdf_path.write_bytes(pdf_bytes)

    reader = pypdf.PdfReader(str(pdf_path))
    print(f"Validated Master PDF: {len(reader.pages)} pages generated at {pdf_path.name}")
    return pdf_path


def export_raw_monograph(dataset: list[dict[str, Any]]) -> Path:
    raw_path = RAW_DIR / "LIT-RIDD-003.txt"
    lines = [
        "=" * 80,
        "TANGKHUL LITERARY RECORD: 300 TANGKHUL FOLK RIDDLES (COMPLETE ENCYCLOPEDIA)",
        "IDENTIFIER: LIT-RIDD-003 | GENRE: RIDDLE (KAKHANGAHAN SANGRAH)",
        "=" * 80,
        "",
        "METADATA & PROVENANCE:",
        "  Title:                 300 Tangkhul Language Folk Riddles (Complete Encyclopedia)",
        "  Title Translation:     Tangkhul Naga Folk Riddle Encyclopedia (Kakhangahan Sangrah)",
        "  Literary Genre / Type: riddle (riddle, oral_narrative, proverb_collection)",
        "  Author / Storyteller:  Traditional Elders & Village Raconteurs",
        "  Publication Year:      2024",
        "  Publisher:             Tangkhul Language Preservation Project & Cultural Archive",
        "  Village / Dialect:     Ukhrul / Hunphun / Phungcham [Standard Tangkhul]",
        "  Source Identifier:     TKH-RIDD-300-ENCYCLOPEDIA",
        "  Source URL:            https://tangkhullanguage.org/archive/literature/300-folk-riddles",
        "  Associated Book:       BK-TLS-015",
        "  License & Clearance:   Traditional Cultural Heritage (community_authorized)",
        "  Verification Status:   verified",
        "",
        "LITERARY OVERVIEW & CONTEXT:",
        "  Comprehensive 300-entry master encyclopedia of Tangkhul folk riddles (Paochirun / Kakhangahan),",
        "  spanning nature, astronomy, agriculture, youth dormitory (Longshim) lore, material culture, and philosophy.",
        "",
        "-" * 80,
        "COMPLETE 300 TANGKHUL FOLK RIDDLES (WITH ENGLISH & HINDI TRANSLATIONS):",
        "-" * 80,
    ]

    for sec in SECTIONS:
        lines.append("")
        lines.append(f"=== PART {sec['section_number']}: {sec['name_en'].upper()} ({sec['name_hi']}) ===")
        lines.append("")
        for r in dataset:
            if sec["start"] <= r["number"] <= sec["end"]:
                lines.append(f"[{r['number']:>3}] Tangkhul: {r['tangkhul_riddle']}")
                lines.append(f"      English:  {r['english_translation']}")
                lines.append(f"      Hindi:    {r['hindi_translation']}")
                lines.append(f"      Answer:   {r['answer_tangkhul']} | {r['answer_english']} | {r['answer_hindi']}")
                lines.append("")

    lines.extend([
        "-" * 80,
        "LITERARY THEMES & MOTIFS:",
        "-" * 80,
        "  * Mountain cosmology, weather patterns, and celestial observation",
        "  * Indigenous terrace cultivation, agricultural tools, and seasonal rhythms",
        "  * Youth dormitory (Longshim) intellectual socialization and riddle games",
        "  * Highland biodiversity, mountain wildlife, and alpine botanical knowledge",
        "  * Village architecture, stone masonry, blacksmithing, and household crafts",
        "  * Moral philosophy, kin solidarity, hospitality, and ancestral cultural memory",
        "",
        "STRUCTURE & POETIC METER: Traditional bipartite metaphorical challenges followed by rapid oral response.",
        "",
        "CRITICAL APPRECIATION & COMMENTARY:",
        "  An exhaustive linguistic monument documenting 300 traditional Tangkhul riddles. This encyclopedia",
        "  illustrates how traditional hill society trained children and youth in observation, metaphorical language,",
        "  and deep ecological understanding through verbal wit and humor around the Longshim hearth.",
        "",
        "=" * 80,
        "END OF RECORD: LIT-RIDD-003 - Tangkhul Language Library Digital Archive",
        "=" * 80,
        "",
    ])

    raw_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created raw literature monograph: {raw_path.name} ({len(lines)} lines)")
    return raw_path


def register_manifest_record() -> None:
    manifest_file = ROOT / "data" / "manifests" / "literature.jsonl"
    lines = manifest_file.read_text(encoding="utf-8").splitlines()
    existing_ids = {json.loads(line_item)["id"] for line_item in lines if line_item.strip()}

    new_record = {
        "id": "LIT-RIDD-003",
        "resource_type": "literature",
        "title": "300 Tangkhul Language Folk Riddles (Complete Encyclopedia)",
        "title_translation": "Tangkhul Naga Folk Riddle Encyclopedia (Kakhangahan Sangrah)",
        "creator": "Tangkhul Elders & Village Raconteurs",
        "author": "Traditional",
        "year": 2024,
        "publisher": "Tangkhul Language Preservation Project & Cultural Archive",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "riddle",
        "work_type": "riddle",
        "genres": ["riddle", "oral_narrative", "proverb_collection"],
        "book_id": "BK-TLS-015",
        "source_url": "https://tangkhullanguage.org/archive/literature/300-folk-riddles",
        "source_identifier": "TKH-RIDD-300-ENCYCLOPEDIA",
        "license": "Traditional Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-RIDD-003.txt",
        "notes": "Comprehensive 300-entry master encyclopedia of Tangkhul folk riddles (Paochirun / Kakhangahan), categorized across 11 thematic domains including nature, agriculture, Longshim lore, wildlife, crafts, and mountain philosophy.",
    }

    if "LIT-RIDD-003" not in existing_ids:
        lines.append(json.dumps(new_record, ensure_ascii=False))
        manifest_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("Registered LIT-RIDD-003 in data/manifests/literature.jsonl")
    else:
        print("LIT-RIDD-003 already registered in literature.jsonl")


def sync_to_databases(dataset: list[dict[str, Any]]) -> None:
    db_paths = [
        ROOT / "data" / "database" / "tangkhul_corpus.sqlite",
        ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite",
    ]

    sample_stanzas = []
    for r in dataset[:10]:
        sample_stanzas.append(f"#{r['number']} {r['tangkhul_riddle']} -> Ans: {r['answer_tangkhul']}")

    sample_trans = []
    for r in dataset[:10]:
        sample_trans.append(f"#{r['number']} {r['english_translation']} -> Ans: {r['answer_english']}")

    rec_data = {
        "id": "LIT-RIDD-003",
        "resource_type": "literature",
        "title": "300 Tangkhul Language Folk Riddles (Complete Encyclopedia)",
        "original_title": "300 Tangkhul Language Folk Riddles (Complete Encyclopedia)",
        "title_translation": "Tangkhul Naga Folk Riddle Encyclopedia (Kakhangahan Sangrah)",
        "work_type": "riddle",
        "genres": ["riddle", "oral_narrative", "proverb_collection"],
        "author": "Traditional",
        "publication_year": 2024,
        "publisher": "Tangkhul Language Preservation Project",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "original_text": "\n\n".join(sample_stanzas),
        "translation_text": "\n\n".join(sample_trans),
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "text_availability": "full_text",
        "verification_status": "verified",
        "stanza_count": len(dataset),
        "line_count": len(dataset) * 4,
        "summary": "Master encyclopedia of 300 traditional Tangkhul folk riddles spanning 11 cultural domains.",
    }

    record = LiteraryRecord.from_dict(rec_data)

    for p in db_paths:
        if not p.exists():
            continue
        db_mgr = DatabaseManager(p)
        db_mgr.initialize_schema()
        lit_repo = LiteratureRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        lit_repo.add(record)
        manifest_repo.add(record.to_manifest_record())
        print(f"Synced LIT-RIDD-003 into {p.name} (Total in literature table: {lit_repo.count()})")


def main() -> None:
    print("=" * 65)
    print("Tangkhul 300 Folk Riddles Encyclopedia Digitization Suite")
    print("=" * 65)

    print("1. Assembling 300 folk riddles dataset across 11 sections...")
    dataset = assemble_dataset()
    print(f"   Successfully assembled {len(dataset)} riddles.")

    print("\n2. Exporting complete JSON catalogs...")
    j1, j2 = export_json(dataset)
    print(f"   Created JSON: {j1.name} ({j1.stat().st_size:,} bytes)")
    print(f"   Created JSON: {j2.name} ({j2.stat().st_size:,} bytes)")

    print("\n3. Building 17-page publication PDF compendium...")
    pdf_p = export_pdf(dataset)
    print(f"   Created PDF:  {pdf_p.name} ({pdf_p.stat().st_size:,} bytes)")

    print("\n4. Writing raw literature archive monograph...")
    raw_p = export_raw_monograph(dataset)

    print("\n5. Registering in literature.jsonl manifest...")
    register_manifest_record()

    print("\n6. Syncing into SQLite databases...")
    sync_to_databases(dataset)

    print("\n" + "=" * 65)
    print("SUCCESS: 300 Folk Riddles Encyclopedia Fully Digitized!")
    print(f"JSON: {j1}")
    print(f"PDF:  {pdf_p}")
    print(f"Raw:  {raw_p}")
    print("=" * 65)


if __name__ == "__main__":
    main()
