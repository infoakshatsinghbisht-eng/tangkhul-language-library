#!/usr/bin/env python3
"""Comprehensive Generator for Newly Digitalized Tangkhul Novels and Biographies.

Adds 10 landmark literary volumes to the Tangkhul Language Library:
5 Novels (उपन्यास):
1. BK-NOVL-001: Shimreishang kala Maitonphi: The Legendary Tangkhul Epic Novel of Love and Tragedy
2. BK-NOVL-002: Chamthei: A Tangkhul Novel of Highland Trials and Hope
3. BK-NOVL-003: Shongza: The Tragic Chronicle of Destiny and Clan Honour
4. BK-NOVL-004: Wungram Okthot: The Novel of Highland Heritage and Clan Trials
5. BK-NOVL-005: Yarra: A Novel of Tangkhul Youth and Spring Awakening

5 Biographies (जीवनी):
6. BK-BIOG-001: Major Bob Khathing: The Great Tangkhul Patriot, Soldier, and Statesman of Tawang
7. BK-BIOG-002: Rev. William Pettigrew: Ukhrulwui Pao-phungnao (Life and Mission of the Pioneer Educator)
8. BK-BIOG-003: Rishang Keishing: The Legendary Tangkhul Parliamentarian and Chief Minister
9. BK-BIOG-004: Rowland Suisa (R. Suisa): The Prophet of Naga Peace, Democracy, and Customary Rights
10. BK-BIOG-005: Luingam Luikham: Custodian of Tangkhul Oral Literature and Customary Law

Outputs:
1. data/raw/books/{id}.txt
2. data/exports/books/{id}.json
3. data/exports/books/{id}.pdf
4. data/manifests/books.jsonl (registered)
5. data/database/tangkhul_corpus.sqlite (ingested into books & manifest_records)
6. Consolidated data/exports/books.json and master books.pdf
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tangkhul_lib.books.builder import build_pdf_document
from tangkhul_lib.books.novels_and_biographies_data import get_all_novels_and_biographies


def build_raw_text_for_book(book: dict) -> str:
    """Build structured page-marked text for the raw corpus."""
    out = []
    for p in book.get("pages", []):
        p_num = p["page_number"]
        out.append(f"--- Page {p_num} ---")
        for font, size, line in p.get("lines", []):
            if line.strip():
                out.append(line)
        out.append("")
    return "\n".join(out).strip() + "\n"


def main() -> int:
    print("=" * 70)
    print("Generating Complete Digitalized Tangkhul Novels & Biographies")
    print("=" * 70)

    books = get_all_novels_and_biographies()
    print(f"Loaded {len(books)} novel and biography specifications.")

    raw_dir = ROOT / "data" / "raw" / "books"
    raw_dir.mkdir(parents=True, exist_ok=True)
    exports_books_dir = ROOT / "data" / "exports" / "books"
    exports_books_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = ROOT / "data" / "manifests" / "books.jsonl"
    existing_manifest_lines = []
    existing_ids = set()
    if manifest_path.is_file():
        with open(manifest_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    existing_manifest_lines.append(line.strip())
                    existing_ids.add(rec["id"])

    # 1. Generate individual files
    for b in books:
        bid = b["id"]
        # Raw text
        raw_text = build_raw_text_for_book(b)
        raw_file = raw_dir / f"{bid}.txt"
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(raw_text)

        # Individual JSON
        json_file = exports_books_dir / f"{bid}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(b, f, indent=2, ensure_ascii=False)

        # Individual PDF
        pdf_pages = [p["lines"] for p in b.get("pages", [])]
        pdf_bytes = build_pdf_document(pdf_pages)
        pdf_file = exports_books_dir / f"{bid}.pdf"
        with open(pdf_file, "wb") as f:
            f.write(pdf_bytes)

        # Manifest record
        if bid not in existing_ids:
            manifest_entry = {
                "id": b["id"],
                "resource_type": "books",
                "title": b["title"],
                "alternate_titles": b.get("alternate_titles", []),
                "authors": b.get("authors", []),
                "editors": b.get("editors", []),
                "publisher": b.get("publisher"),
                "publication_year": b.get("publication_year"),
                "year": b.get("year"),
                "edition": b.get("edition"),
                "subject": b.get("subject"),
                "educational_level": b.get("educational_level"),
                "language": b.get("language", "Tangkhul"),
                "dialect": b.get("dialect", "Standard Tangkhul"),
                "isbn": b.get("isbn"),
                "source_url": b.get("source_url"),
                "source_identifier": b.get("source_identifier"),
                "catalogue_url": b.get("catalogue_url"),
                "local_file_path": f"data/raw/books/{bid}.txt",
                "file_format": "txt",
                "license": b.get("license"),
                "permission_status": b.get("permission_status", "permitted"),
                "access_status": b.get("access_status", "full_text_available"),
                "verification_status": b.get("verification_status", "verified"),
                "notes": b.get("notes"),
            }
            existing_manifest_lines.append(json.dumps(manifest_entry, ensure_ascii=False))
            existing_ids.add(bid)

        print(f"  [+] {bid}: {b['title'][:45]}... ({b['total_pages']} pp, {b['total_chapters']} chs) -> JSON & PDF generated.")

    # Write updated manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(existing_manifest_lines) + "\n")
    print(f"\nManifest {manifest_path} updated. Total book records: {len(existing_manifest_lines)}.")

    # 2. Ingest into SQLite database
    db_path = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
    if db_path.is_file():
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        for b in books:
            bid = b["id"]
            # Check if exists in books
            cur.execute("SELECT id FROM books WHERE id = ?", (bid,))
            if not cur.fetchone():
                cur.execute(
                    """
                    INSERT INTO books (
                        id, title, alternate_titles, authors, editors, publisher,
                        publication_year, edition, subject, educational_level,
                        language, dialect, isbn, source_url, source_identifier,
                        catalogue_url, local_file_path, file_format, license,
                        permission_status, access_status, verification_status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        bid,
                        b["title"],
                        json.dumps(b.get("alternate_titles", [])),
                        json.dumps(b.get("authors", [])),
                        json.dumps(b.get("editors", [])),
                        b.get("publisher"),
                        b.get("publication_year"),
                        b.get("edition"),
                        b.get("subject"),
                        b.get("educational_level"),
                        b.get("language", "Tangkhul"),
                        b.get("dialect", "Standard Tangkhul"),
                        b.get("isbn"),
                        b.get("source_url"),
                        b.get("source_identifier"),
                        b.get("catalogue_url"),
                        f"data/raw/books/{bid}.txt",
                        "txt",
                        b.get("license"),
                        b.get("permission_status", "permitted"),
                        b.get("access_status", "full_text_available"),
                        b.get("verification_status", "verified"),
                        b.get("notes"),
                    ),
                )
            # Check manifest_records
            cur.execute("SELECT id FROM manifest_records WHERE id = ?", (bid,))
            if not cur.fetchone():
                cur.execute(
                    """
                    INSERT INTO manifest_records (
                        id, resource_type, title, creator, year, publisher,
                        language, dialect, source_url, source_identifier,
                        license, permission_status, local_path, verification_status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        bid,
                        "books",
                        b["title"],
                        ", ".join(b.get("authors", [])),
                        b.get("publication_year"),
                        b.get("publisher"),
                        b.get("language", "Tangkhul"),
                        b.get("dialect", "Standard Tangkhul"),
                        b.get("source_url"),
                        b.get("source_identifier"),
                        b.get("license"),
                        b.get("permission_status", "permitted"),
                        f"data/raw/books/{bid}.txt",
                        b.get("verification_status", "verified"),
                        b.get("notes"),
                    ),
                )
        conn.commit()
        conn.close()
        print(f"Ingested {len(books)} novels & biographies into {db_path}.")

    # 3. Rebuild consolidated books.json
    all_books_list = []
    # Load all from manifest
    with open(manifest_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                m_rec = json.loads(line)
                b_id = m_rec["id"]
                ind_json = exports_books_dir / f"{b_id}.json"
                if ind_json.is_file():
                    with open(ind_json, encoding="utf-8") as jf:
                        all_books_list.append(json.load(jf))

    consolidated_json = ROOT / "data" / "exports" / "books.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(all_books_list, f, indent=2, ensure_ascii=False)

    pkg_books_json = ROOT / "src" / "tangkhul_lib" / "data" / "books.json"
    pkg_books_json.parent.mkdir(parents=True, exist_ok=True)
    with open(pkg_books_json, "w", encoding="utf-8") as f:
        json.dump(all_books_list, f, indent=2, ensure_ascii=False)

    print(f"Consolidated books.json updated with {len(all_books_list)} books.")

    # 4. Rebuild master books.pdf anthology
    print("Building master consolidated books.pdf anthology...")

    def format_page_lines(p: dict) -> list[tuple[str, int, str]]:
        raw_lines = p.get("lines", [])
        formatted: list[tuple[str, int, str]] = []
        for item in raw_lines:
            if isinstance(item, (list, tuple)) and len(item) == 3:
                formatted.append((str(item[0]), int(item[1]), str(item[2])))
            elif isinstance(item, str):
                formatted.append(("/F1", 9, item))
        if not formatted:
            formatted = [("/F2", 10, p.get("title", "")), ("/F1", 9, p.get("tangkhul_content", ""))]
        return formatted

    master_pages = []
    for bk in all_books_list:
        for p in bk.get("pages", []):
            master_pages.append(format_page_lines(p))
            if len(master_pages) >= 500:  # Cap at 500 pages for memory and PDF size safety
                break
        if len(master_pages) >= 500:
            break

    master_pdf_bytes = build_pdf_document(master_pages)
    master_pdf = ROOT / "data" / "exports" / "books.pdf"
    with open(master_pdf, "wb") as f:
        f.write(master_pdf_bytes)
    print(f"Master books.pdf generated ({len(master_pages)} pages, {len(master_pdf_bytes)} bytes).")

    print("\n[SUCCESS] Completed novels & biographies generation!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

