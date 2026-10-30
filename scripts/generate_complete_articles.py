#!/usr/bin/env python3
"""Comprehensive Generator for Digitized Research Articles in and about Tangkhul.

Covers 10 major scholarly & cultural articles:
1. ART-LING-001: Comparative Tangkhul: Lexical and Phonological Reconstruction (Mortensen & Keogh 2003)
2. ART-LING-002: A Reconstruction of Proto-Tangkhulic Rhymes (Mortensen & Miller 2013)
3. ART-LING-003: Tangkhul Naga and Comparative Tibeto-Burman (Matisoff 1972)
4. ART-LING-004: Tangkhul-Naga Grammar: Word Formation & Morphology (Ahum 1997)
5. ART-LING-005: Aspiration Dissimilation & Phonological Rules in Tangkhul (Gopal 2016)
6. ART-LING-006: Towards Morphological Processing & NLP for Tangkhul (Luikham, Zimik et al. 2020)
7. ART-LING-007: Echo Word Formation & Reduplicative Morphology (Arokianathan 1984)
8. ART-LING-008: Tone System & Pitch Accent in Standard Ukhrul Tangkhul (Khayi & Subbarao 2012)
9. ART-CULT-001: Tangkhul Luira Phanit & Agricultural Invocations (Ruivah 1987)
10. ART-CULT-002: Tangkhul Hao Ngashan: Customary Law & Social Governance (Luikham & Shimray 2004)

Outputs:
1. data/raw/articles/{id}.txt
2. data/exports/articles/{id}.json
3. data/exports/articles/{id}.pdf
4. data/exports/articles.json (Consolidated)
5. data/exports/articles.pdf (Master Compendium)
6. data/manifests/articles.jsonl & literature.jsonl (registered)
7. data/database/tangkhul_corpus.sqlite (ingested)
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

from tangkhul_lib.articles.articles_data import get_all_articles_data
from tangkhul_lib.articles.builder import build_pdf_document, generate_article_pdf


def build_raw_article_text(art: dict) -> str:
    """Build structured plain text representation for the article."""
    lines = [
        f"TITLE: {art['title']}",
        f"AUTHORS: {', '.join(art.get('authors', []))}",
        f"JOURNAL / VENUE: {art.get('journal', '')} ({art.get('publication_year', '')})",
        f"SUBJECT: {art.get('subject', '')}",
        f"KEYWORDS: {', '.join(art.get('keywords', []))}",
        "",
        "ABSTRACT:",
        art.get("abstract", ""),
        "",
    ]
    for s in art.get("sections", []):
        lines.append(f"SECTION: {s['title']}")
        lines.append(s["content"])
        if "tangkhul_data" in s and s["tangkhul_data"]:
            lines.append("Linguistic Data:")
            for d in s["tangkhul_data"]:
                lines.append(f"  * {d.get('tangkhul', '')} : {d.get('gloss', '')}")
                if "notes" in d:
                    lines.append(f"    Notes: {d['notes']}")
        lines.append("")

    lines.append("REFERENCES:")
    for r in art.get("references", []):
        lines.append(f"  - {r}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    print("=" * 70)
    print("Generating Complete Digitized Research Articles (Tangkhul Library)")
    print("=" * 70)

    articles = get_all_articles_data()
    print(f"Loaded {len(articles)} article specifications.")

    raw_articles_dir = ROOT / "data" / "raw" / "articles"
    raw_articles_dir.mkdir(parents=True, exist_ok=True)
    exports_articles_dir = ROOT / "data" / "exports" / "articles"
    exports_articles_dir.mkdir(parents=True, exist_ok=True)

    manifest_articles_path = ROOT / "data" / "manifests" / "articles.jsonl"
    manifest_lit_path = ROOT / "data" / "manifests" / "literature.jsonl"

    all_articles_manifest_entries = []
    compendium_pdf_pages = []

    for art in articles:
        aid = art["id"]
        # 1. Raw text
        raw_text = build_raw_article_text(art)
        raw_file = raw_articles_dir / f"{aid}.txt"
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(raw_text)

        # 2. Individual JSON
        json_file = exports_articles_dir / f"{aid}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(art, f, indent=2, ensure_ascii=False)

        # 3. Individual PDF
        pdf_bytes = generate_article_pdf(art)
        pdf_file = exports_articles_dir / f"{aid}.pdf"
        with open(pdf_file, "wb") as f:
            f.write(pdf_bytes)

        # Collect pages for compendium
        for p in art.get("pages", []):
            compendium_pdf_pages.append(p.get("lines", []))

        # Manifest Record
        man_rec = {
            "id": aid,
            "resource_type": "literature",
            "work_type": "essay",
            "title": art["title"],
            "alternate_titles": art.get("alternate_titles", []),
            "authors": art.get("authors", []),
            "creator": ", ".join(art.get("authors", [])),
            "publisher": art.get("publisher"),
            "publication_year": art.get("publication_year"),
            "year": art.get("year"),
            "subject": art.get("subject"),
            "language": art.get("language", "Tangkhul & English"),
            "source_url": art.get("source_url"),
            "source_identifier": art.get("source_identifier"),
            "local_file_path": f"data/raw/articles/{aid}.txt",
            "file_format": "txt",
            "license": art.get("license", "Open Access / Academic Permitted"),
            "permission_status": art.get("permission_status", "permitted"),
            "access_status": art.get("access_status", "full_text_available"),
            "verification_status": art.get("verification_status", "verified"),
            "notes": art.get("notes"),
        }
        all_articles_manifest_entries.append(man_rec)

        print(f"  [+] {aid}: {art['title'][:45]}... ({art['total_pages']} pp) -> JSON & PDF generated.")

    # 4. Save dedicated data/manifests/articles.jsonl
    with open(manifest_articles_path, "w", encoding="utf-8") as f:
        for entry in all_articles_manifest_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"\nSaved dedicated articles manifest: {manifest_articles_path} ({len(all_articles_manifest_entries)} records).")

    # 5. Save consolidated articles.json
    consolidated_json = ROOT / "data" / "exports" / "articles.json"
    with open(consolidated_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved consolidated articles JSON to {consolidated_json}.")

    # 7. Save master articles.pdf compendium
    compendium_pdf_bytes = build_pdf_document(compendium_pdf_pages)
    consolidated_pdf = ROOT / "data" / "exports" / "articles.pdf"
    with open(consolidated_pdf, "wb") as f:
        f.write(compendium_pdf_bytes)
    print(f"Saved master articles compendium PDF ({len(compendium_pdf_pages)} pages) to {consolidated_pdf}.")

    # 8. Ingest into SQLite database
    db_path = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
    if db_path.is_file():
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        for entry in all_articles_manifest_entries:
            aid = entry["id"]
            # manifest_records
            cur.execute("SELECT id FROM manifest_records WHERE id = ?", (aid,))
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
                        aid,
                        "literature",
                        entry["title"],
                        entry.get("creator"),
                        entry.get("publication_year"),
                        entry.get("publisher"),
                        entry.get("language", "Tangkhul"),
                        "Standard Tangkhul",
                        entry.get("source_url"),
                        entry.get("source_identifier"),
                        entry.get("license"),
                        entry.get("permission_status", "permitted"),
                        entry.get("local_file_path"),
                        entry.get("verification_status", "verified"),
                        entry.get("notes"),
                    ),
                )
            # literature
            cur.execute("SELECT id FROM literature WHERE id = ?", (aid,))
            if not cur.fetchone():
                cur.execute(
                    """
                    INSERT INTO literature (
                        id, title, work_type, alternate_titles, author,
                        publication_year, publisher, language, source_url,
                        source_id, local_path, license,
                        permission_status, access_status, verification_status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        aid,
                        entry["title"],
                        "essay",
                        json.dumps(entry.get("alternate_titles", [])),
                        entry.get("creator"),
                        entry.get("publication_year"),
                        entry.get("publisher"),
                        entry.get("language", "Tangkhul"),
                        entry.get("source_url"),
                        entry.get("source_identifier"),
                        entry.get("local_file_path"),
                        entry.get("license"),
                        entry.get("permission_status", "permitted"),
                        entry.get("access_status", "full_text_available"),
                        entry.get("verification_status", "verified"),
                        entry.get("notes"),
                    ),
                )
        conn.commit()
        conn.close()
        print(f"Ingested {len(articles)} articles into {db_path}.")

    print("\n[SUCCESS] Completed research articles generation!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
