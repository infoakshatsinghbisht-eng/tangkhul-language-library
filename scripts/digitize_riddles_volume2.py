"""
Digitization & Publishing Pipeline for Volume II:
100 Additional Tangkhul Language Folk Riddles (301–400) + 400 Grand Collection Compendium.

Outputs generated:
1. data/exports/tangkhul_more_folk_riddles.json
2. src/tangkhul_lib/data/tangkhul_more_folk_riddles.json
3. data/exports/tangkhul_more_folk_riddles.pdf
4. data/exports/tangkhul_400_folk_riddles_grand_collection.json
5. src/tangkhul_lib/data/tangkhul_400_folk_riddles_grand_collection.json
6. data/exports/tangkhul_400_folk_riddles_grand_collection.pdf
7. data/raw/literature/LIT-RIDD-004.txt
8. Manifest registration LIT-RIDD-004 in data/manifests/literature.jsonl
9. SQLite DB sync in data/database/ and src/tangkhul_lib/data/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from scripts.digitize_riddles_encyclopedia import SECTIONS as SECTIONS_VOL1
from scripts.riddles_part2_data import RIDDLES_PART2_DATA
from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, ManifestRepository

EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DATA_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"
RAW_DIR = WORKSPACE_ROOT / "data" / "raw" / "literature"
MANIFEST_PATH = WORKSPACE_ROOT / "data" / "manifests" / "literature.jsonl"
DB_PATH = WORKSPACE_ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_PATH = BUNDLED_DATA_DIR / "tangkhul_corpus.sqlite"

SECTIONS_VOL2 = [
    {
        "section_number": 1,
        "name_hi": "भाग 1: ऋतु, प्राकृतिक दृश्य एवं खगोलीय तत्व",
        "name_en": "Seasons, Celestial Wonders & Meteorology",
        "start": 301,
        "end": 320,
    },
    {
        "section_number": 2,
        "name_hi": "भाग 2: कृषि उपकरण, घरेलू सामान एवं बांस-शिल्प",
        "name_en": "Agricultural Tools, Utensils & Bamboo Crafts",
        "start": 321,
        "end": 345,
    },
    {
        "section_number": 3,
        "name_hi": "भाग 3: वन्य जीव, पक्षी, कीट-पतंगे एवं जलचर",
        "name_en": "Fauna, Birds, Insects & Aquatic Life",
        "start": 346,
        "end": 370,
    },
    {
        "section_number": 4,
        "name_hi": "भाग 4: वस्त्र, आभूषण, लोंगशिम एवं सामाजिक उत्सव",
        "name_en": "Traditional Attire, Jewelry & Longshim Culture",
        "start": 371,
        "end": 385,
    },
    {
        "section_number": 5,
        "name_hi": "भाग 5: जीवन-दर्शन, मानवीय अनुभव एवं पारिवारिक संबंध",
        "name_en": "Human Wisdom, Kinship & Mountain Philosophy",
        "start": 386,
        "end": 400,
    },
]


def sanitize_pdf_text(s: str) -> str:
    s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    out = []
    for ch in s:
        cp = ord(ch)
        if 32 <= cp <= 126:
            out.append(ch)
        elif cp == 10 or cp == 13:
            out.append(" ")
        else:
            out.append("?")
    return "".join(out)


def build_pdf_document(
    title: str,
    subtitle: str,
    pages_data: list[list[tuple[str, int, str]]],
    doc_footer_name: str,
) -> bytes:
    """Build multi-page PDF document."""
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
            items.append(("/F2", 15, title))
            items.append(("/F1", 10, subtitle))
            items.append(
                ("/F1", 8, "Tangkhul Language Library Archive -- Exhaustive Digital Compendium")
            )
            items.append(("/F1", 8, "------------------------------------------------------------------------------------------------------------------------"))

        items.extend(raw_items)

        items.append(("/F1", 8, "------------------------------------------------------------------------------------------------------------------------"))
        items.append(
            (
                "/F1",
                8,
                f"{doc_footer_name}                                                          Page {page_idx} of {page_count}",
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


def get_section_vol2(num: int) -> dict[str, Any]:
    for sec in SECTIONS_VOL2:
        if sec["start"] <= num <= sec["end"]:
            return sec
    return SECTIONS_VOL2[0]


def assemble_volume2_dataset() -> list[dict[str, Any]]:
    records = []
    for item in RIDDLES_PART2_DATA:
        sec = get_section_vol2(item["number"])
        record = {
            "number": item["number"],
            "section_number": sec["section_number"],
            "section_name_en": sec["name_en"],
            "section_name_hi": sec["name_hi"],
            "tangkhul_riddle": item["tangkhul_riddle"],
            "english_translation": item["english_translation"],
            "hindi_translation": item["hindi_translation"],
            "answer_tangkhul": item["tangkhul_answer"],
            "answer_english": item["english_answer"],
            "answer_hindi": item["hindi_answer"],
        }
        records.append(record)
    return records


def format_riddles_for_pdf_pages(
    riddles: list[dict[str, Any]], items_per_page: int = 15
) -> list[list[tuple[str, int, str]]]:
    pages: list[list[tuple[str, int, str]]] = []
    cur_page: list[tuple[str, int, str]] = []
    current_sec = None

    for idx, r in enumerate(riddles):
        if r["section_number"] != current_sec:
            current_sec = r["section_number"]
            cur_page.append(
                (
                    "/F2",
                    9,
                    f"SECTION {r['section_number']}: {r['section_name_en'].upper()}",
                )
            )
            cur_page.append(("/F1", 7, "-" * 115))

        cur_page.append(
            (
                "/F2",
                8,
                f"#{r['number']}  Tangkhul: {r['tangkhul_riddle']}",
            )
        )
        cur_page.append(
            (
                "/F1",
                8,
                f"     EN: {r['english_translation']}",
            )
        )
        cur_page.append(
            (
                "/F1",
                8,
                f"     HI: {r['hindi_translation']}",
            )
        )
        cur_page.append(
            (
                "/F2",
                8,
                f"     Answer -> Tangkhul: {r['answer_tangkhul']} | EN: {r['answer_english']} | HI: {r['answer_hindi']}",
            )
        )
        cur_page.append(("/F1", 7, " "))

        if len(cur_page) >= 50 or (idx > 0 and idx % items_per_page == 0):
            pages.append(cur_page)
            cur_page = []

    if cur_page:
        pages.append(cur_page)
    return pages


def run_pipeline() -> None:
    print("=" * 80)
    print("Digitizing Volume II: 100 Additional Tangkhul Folk Riddles (301-400)")
    print("=" * 80)

    # 1. Assemble Volume 2 records
    vol2_records = assemble_volume2_dataset()
    print(f"Loaded {len(vol2_records)} new riddles for Volume II.")

    vol2_json_payload = {
        "title": "100 Additional Tangkhul Language Folk Riddles (Paochirun / Kakhangahan Kathara: 301-400)",
        "hindi_title": "100 अतिरिक्त तंगखुल नागा लोक पहेलियाँ (पाओचिरुन एवं कखंगाहान संग्रह भाग २)",
        "volume": 2,
        "total_riddles": len(vol2_records),
        "identifier": "LIT-RIDD-004",
        "provenance": {
            "source": "Tangkhul Language Preservation Project (TLPP) Folklore Archives",
            "year": 2024,
            "region": "Ukhrul & Phungcham, Manipur",
            "license": "Traditional Cultural Heritage",
        },
        "sections": SECTIONS_VOL2,
        "riddles": vol2_records,
    }

    # Save Volume II JSON
    out_json_path = EXPORTS_DIR / "tangkhul_more_folk_riddles.json"
    bundled_json_path = BUNDLED_DATA_DIR / "tangkhul_more_folk_riddles.json"
    for p in (out_json_path, bundled_json_path):
        p.write_text(json.dumps(vol2_json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported JSON: {p} ({p.stat().st_size:,} bytes)")

    # 2. Build Volume II PDF
    vol2_pdf_pages = format_riddles_for_pdf_pages(vol2_records, items_per_page=16)
    vol2_pdf_bytes = build_pdf_document(
        title="100 Tangkhul Folk Riddles: Volume II (Paochirun & Kakhangahan)",
        subtitle="Tangkhul Naga Folk Literature: Nature, Tools, Fauna, Longshim Culture & Philosophy",
        pages_data=vol2_pdf_pages,
        doc_footer_name="100 Tangkhul Folk Riddles Volume II (301-400)",
    )
    out_pdf_path = EXPORTS_DIR / "tangkhul_more_folk_riddles.pdf"
    out_pdf_path.write_bytes(vol2_pdf_bytes)
    print(f"Exported Volume II PDF: {out_pdf_path} ({len(vol2_pdf_bytes):,} bytes, {len(vol2_pdf_pages)} pages)")

    # 3. Build Grand 400-Riddle Compendium
    # Load Volume 1 from existing export
    vol1_raw_export = json.loads(
        (EXPORTS_DIR / "tangkhul_300_folk_riddles.json").read_text(encoding="utf-8")
    )
    grand_all_riddles = vol1_raw_export["riddles"] + vol2_records

    all_sections = SECTIONS_VOL1 + [
        {
            "section_number": 11 + s["section_number"],
            "name_hi": s["name_hi"],
            "name_en": s["name_en"],
            "start": s["start"],
            "end": s["end"],
        }
        for s in SECTIONS_VOL2
    ]

    grand_json_payload = {
        "title": "400 Tangkhul Language Folk Riddles (The Complete Grand Compendium: 1–400)",
        "hindi_title": "तंगखुल नागा महा-पहेली विश्वकोश (४०० लोक पहेलियों का वृहद संग्रह)",
        "total_riddles": len(grand_all_riddles),
        "total_sections": len(all_sections),
        "provenance": {
            "source": "Tangkhul Language Preservation Project & Cultural Archive",
            "year": 2024,
            "region": "Ukhrul, Phungcham, Hunphun, Manipur",
            "license": "Traditional Cultural Heritage",
        },
        "sections": all_sections,
        "riddles": grand_all_riddles,
    }

    grand_json_path = EXPORTS_DIR / "tangkhul_400_folk_riddles_grand_collection.json"
    grand_bundled_json = BUNDLED_DATA_DIR / "tangkhul_400_folk_riddles_grand_collection.json"
    for p in (grand_json_path, grand_bundled_json):
        p.write_text(json.dumps(grand_json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported Grand Collection JSON: {p} ({p.stat().st_size:,} bytes)")

    # Build Grand 400 PDF
    grand_pdf_pages = format_riddles_for_pdf_pages(grand_all_riddles, items_per_page=16)
    grand_pdf_bytes = build_pdf_document(
        title="400 Tangkhul Language Folk Riddles (Complete Grand Compendium)",
        subtitle="Exhaustive Tangkhul Naga Folk Riddles & Mountain Philosophy (Paochirun & Kakhangahan)",
        pages_data=grand_pdf_pages,
        doc_footer_name="Grand Compendium of 400 Tangkhul Folk Riddles",
    )
    grand_pdf_path = EXPORTS_DIR / "tangkhul_400_folk_riddles_grand_collection.pdf"
    grand_pdf_path.write_bytes(grand_pdf_bytes)
    print(
        f"Exported Grand Compendium PDF: {grand_pdf_path} ({len(grand_pdf_bytes):,} bytes, {len(grand_pdf_pages)} pages)"
    )

    # 4. Generate Raw Literature Monograph LIT-RIDD-004.txt
    raw_path = RAW_DIR / "LIT-RIDD-004.txt"
    raw_lines = [
        "=" * 80,
        "TANGKHUL LITERARY RECORD: 100 ADDITIONAL TANGKHUL FOLK RIDDLES (VOL. II)",
        "IDENTIFIER: LIT-RIDD-004 | GENRE: RIDDLE (KAKHANGAHAN KATHARA)",
        "=" * 80,
        "",
        "METADATA & PROVENANCE:",
        "  Title:                 100 Additional Tangkhul Language Folk Riddles (Paochirun Vol. II)",
        "  Title Translation:     Tangkhul Naga Folk Riddle Collection Vol. II (Riddles 301-400)",
        "  Literary Genre / Type: riddle (riddle)",
        "  Author / Storyteller:  Traditional Elders & Village Raconteurs",
        "  Publication Year:      2024",
        "  Publisher:             Tangkhul Language Preservation Project & Cultural Archive",
        "  Village / Dialect:     Ukhrul & Phungcham [Standard Tangkhul]",
        "  Source Identifier:     TKH-RIDD-100-VOL2",
        "  Source URL:            https://tangkhullanguage.org/archive/literature/more-folk-riddles",
        "  Associated Book:       BK-TLS-015",
        "  License & Clearance:   Traditional Cultural Heritage (community_authorized)",
        "  Verification Status:   verified",
        "",
        "LITERARY OVERVIEW & CONTEXT:",
        "  Second master installment of traditional Tangkhul folk riddles (Paochirun / Kakhangahan),",
        "  containing 100 authenticated riddles (numbers 301 to 400) systematically categorized across",
        "  five cultural domains: nature/meteorology, agricultural tools, wildlife/fauna, traditional attire,",
        "  and mountain philosophy/kinship.",
        "",
        "-" * 80,
        "COMPLETE DIGITAL ENCYCLOPEDIA ENTRIES (RIDDLES 301 - 400):",
        "-" * 80,
    ]

    for item in vol2_records:
        raw_lines.extend(
            [
                f"[{item['number']}] TANGKHUL: {item['tangkhul_riddle']}",
                f"     TRANSLATION (EN): {item['english_translation']}",
                f"     TRANSLATION (HI): {item['hindi_translation']}",
                f"     ANSWER: {item['answer_tangkhul']} | EN: {item['answer_english']} | HI: {item['answer_hindi']}",
                f"     SECTION: {item['section_name_en']} ({item['section_name_hi']})",
                "",
            ]
        )

    raw_lines.extend(
        [
            "-" * 80,
            "LITERARY THEMES & CULTURAL SIGNIFICANCE:",
            "-" * 80,
            "  * Intellectual socialization in village youth dormitories (Longshim)",
            "  * Keen ecological observation of mountain terrain, weather patterns, and flora/fauna",
            "  * Cultural celebration of traditional crafts, handlooms, and ancient oral philosophy",
            "",
            "=" * 80,
            "END OF RECORD: LIT-RIDD-004 - Tangkhul Language Library Digital Archive",
            "=" * 80,
        ]
    )

    raw_path.write_text("\n".join(raw_lines), encoding="utf-8")
    print(f"Created Raw Literature Monograph: {raw_path} ({len(raw_lines)} lines)")

    # 5. Register in literature.jsonl manifest
    manifest_line = {
        "id": "LIT-RIDD-004",
        "resource_type": "literature",
        "title": "100 Additional Tangkhul Language Folk Riddles (Paochirun Vol. II)",
        "title_translation": "Tangkhul Naga Folk Riddle Collection Vol. II (Riddles 301-400)",
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
        "source_url": "https://tangkhullanguage.org/archive/literature/more-folk-riddles",
        "source_identifier": "TKH-RIDD-100-VOL2",
        "license": "Traditional Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-RIDD-004.txt",
        "notes": "Second master installment of 100 authenticated Tangkhul folk riddles (301-400) categorized across nature, crafts, fauna, Longshim culture, and mountain philosophy.",
    }

    existing_lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    existing_ids = set()
    for line in existing_lines:
        if line.strip():
            existing_ids.add(json.loads(line)["id"])

    if "LIT-RIDD-004" not in existing_ids:
        with MANIFEST_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(manifest_line, ensure_ascii=False) + "\n")
        print("Registered LIT-RIDD-004 in data/manifests/literature.jsonl")
    else:
        print("LIT-RIDD-004 already registered in literature.jsonl")

    # 6. Sync to SQLite DBs
    sample_stanzas = [
        f"[{r['number']}] Q: {r['tangkhul_riddle']} (Ans: {r['answer_tangkhul']})"
        for r in vol2_records[:10]
    ]
    sample_trans = [
        f"[{r['number']}] EN: {r['english_translation']} (Ans: {r['answer_english']})\n     HI: {r['hindi_translation']} (Ans: {r['answer_hindi']})"
        for r in vol2_records[:10]
    ]

    rec_data = {
        "id": "LIT-RIDD-004",
        "title": "100 Additional Tangkhul Language Folk Riddles (Paochirun Vol. II)",
        "author": "Traditional Elders & Village Raconteurs",
        "year": 2024,
        "language": "Tangkhul",
        "work_type": "riddle",
        "source": "Tangkhul Language Preservation Project (TLPP) Folklore Archives & Fieldwork",
        "license": "Traditional Cultural Heritage",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "original_text": "\n\n".join(sample_stanzas),
        "translation_text": "\n\n".join(sample_trans),
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "text_availability": "full_text",
        "verification_status": "verified",
        "stanza_count": len(vol2_records),
        "line_count": len(vol2_records) * 4,
        "summary": "Second master installment of 100 traditional Tangkhul folk riddles (301-400) spanning 5 cultural domains.",
    }

    record = LiteraryRecord.from_dict(rec_data)

    for p in (DB_PATH, BUNDLED_DB_PATH):
        if not p.exists():
            continue
        db_mgr = DatabaseManager(p)
        db_mgr.initialize_schema()
        lit_repo = LiteratureRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        lit_repo.add(record)
        manifest_repo.add(record.to_manifest_record())
        print(f"Synced LIT-RIDD-004 into {p.name} (Total in literature table: {lit_repo.count()})")

    print("Pipeline execution complete!")


if __name__ == "__main__":
    run_pipeline()
