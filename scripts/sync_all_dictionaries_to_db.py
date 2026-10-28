#!/usr/bin/env python3
"""Synchronize all 10 dictionary sources and their lexical entries into both SQLite databases.

Synchronizes:
- data/database/tangkhul_corpus.sqlite
- src/tangkhul_lib/data/tangkhul_corpus.sqlite
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_raw_dictionaries import DICTIONARIES_RAW_DATA
from tangkhul_lib.vocabulary.normalization import normalize_unicode

DATABASES = [
    ROOT / "data" / "database" / "tangkhul_corpus.sqlite",
    ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite",
]


def sync_dictionaries_to_database(db_path: Path) -> None:
    """Sync dictionaries and dictionary_entries tables in the specified SQLite database."""
    if not db_path.is_file():
        print(f"Skipping non-existent DB: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Ensure tables exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dictionaries (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        alternate_titles TEXT,
        authors TEXT,
        editors TEXT,
        compiler TEXT,
        contributors TEXT,
        publisher TEXT,
        publication_place TEXT,
        publication_year INTEGER,
        edition TEXT,
        languages TEXT,
        language_pair TEXT,
        dialect TEXT,
        source_type TEXT,
        isbn TEXT,
        identifier TEXT,
        source_url TEXT,
        local_file_path TEXT,
        license TEXT,
        license_evidence TEXT,
        permission_status TEXT DEFAULT 'pending',
        access_status TEXT DEFAULT 'metadata_only',
        verification_status TEXT DEFAULT 'unverified',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dictionary_entries (
        id TEXT PRIMARY KEY,
        dictionary_id TEXT NOT NULL,
        headword TEXT NOT NULL,
        normalized_headword TEXT NOT NULL,
        alternate_spellings TEXT,
        transliteration TEXT,
        definitions_en TEXT,
        definitions_hi TEXT,
        other_definitions TEXT,
        part_of_speech TEXT,
        pronunciation TEXT,
        notes TEXT,
        examples TEXT,
        dialect TEXT,
        grammatical_info TEXT,
        page_or_section TEXT,
        entry_number TEXT,
        source_excerpt TEXT,
        extraction_method TEXT,
        confidence REAL DEFAULT 1.0,
        license TEXT,
        permission_status TEXT DEFAULT 'pending',
        verification_status TEXT DEFAULT 'unverified',
        vocabulary_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    manifest_file = ROOT / "data" / "manifests" / "dictionaries.jsonl"
    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    # Insert or update dictionaries
    for rec in records:
        rid = rec["id"]
        extra = DICTIONARIES_RAW_DATA.get(rid, {})

        authors_val = json.dumps([a.strip() for a in rec.get("creator", "").split(",") if a.strip()])
        alt_titles = json.dumps([rec["title_translation"]] if rec.get("title_translation") else [])
        languages_val = json.dumps(["Tangkhul"])

        cur.execute(
            """
            INSERT INTO dictionaries (
                id, title, alternate_titles, authors, editors, compiler, contributors,
                publisher, publication_place, publication_year, edition, languages,
                language_pair, dialect, source_type, isbn, identifier, source_url,
                local_file_path, license, license_evidence, permission_status,
                access_status, verification_status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                alternate_titles=excluded.alternate_titles,
                authors=excluded.authors,
                publisher=excluded.publisher,
                publication_year=excluded.publication_year,
                languages=excluded.languages,
                language_pair=excluded.language_pair,
                dialect=excluded.dialect,
                source_type=excluded.source_type,
                identifier=excluded.identifier,
                source_url=excluded.source_url,
                local_file_path=excluded.local_file_path,
                license=excluded.license,
                permission_status=excluded.permission_status,
                access_status=excluded.access_status,
                verification_status=excluded.verification_status,
                notes=excluded.notes
            """,
            (
                rid,
                rec["title"],
                alt_titles,
                authors_val,
                json.dumps([]),
                None,
                json.dumps([]),
                rec.get("publisher"),
                None,
                rec.get("year"),
                None,
                languages_val,
                rec.get("language_pair"),
                rec.get("dialect"),
                rec.get("source_type", "dictionary"),
                None,
                rec.get("source_identifier"),
                rec.get("source_url"),
                rec.get("local_path"),
                rec.get("license"),
                None,
                rec.get("permission_status", "pending"),
                extra.get("access_status", "metadata_only"),
                rec.get("verification_status", "unverified"),
                rec.get("notes"),
            ),
        )

        # Synchronize manifest_records table
        cur.execute(
            """
            INSERT INTO manifest_records (
                id, resource_type, title, title_translation, creator, year,
                publisher, language, dialect, source_url, source_identifier,
                license, permission_status, local_path, verification_status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                title_translation=excluded.title_translation,
                creator=excluded.creator,
                year=excluded.year,
                publisher=excluded.publisher,
                language=excluded.language,
                dialect=excluded.dialect,
                source_url=excluded.source_url,
                source_identifier=excluded.source_identifier,
                license=excluded.license,
                permission_status=excluded.permission_status,
                local_path=excluded.local_path,
                verification_status=excluded.verification_status,
                notes=excluded.notes
            """,
            (
                rid,
                "dictionaries",
                rec["title"],
                rec.get("title_translation"),
                rec.get("creator"),
                rec.get("year"),
                rec.get("publisher"),
                rec.get("language", "Tangkhul"),
                rec.get("dialect"),
                rec.get("source_url"),
                rec.get("source_identifier"),
                rec.get("license"),
                rec.get("permission_status", "pending"),
                rec.get("local_path"),
                rec.get("verification_status", "unverified"),
                rec.get("notes"),
            ),
        )

    # Insert or update dictionary_entries
    total_entries_synced = 0
    for did, data in DICTIONARIES_RAW_DATA.items():
        for idx, ent in enumerate(data["entries"], 1):
            ent_id = f"{did}-ENT-{idx:04d}"
            hw = ent["headword"]
            norm_hw = normalize_unicode(hw).strip().lower()
            alts = json.dumps(ent.get("alternative_spellings", []))
            defs_en = json.dumps(ent.get("definitions_en", []))
            defs_hi = json.dumps(ent.get("definitions_hi", []))
            pos = ent.get("part_of_speech", "noun")
            page = ent.get("page", "")
            examples = json.dumps([ent["example"]] if ent.get("example") else [])
            perm = data.get("permission_status", "pending")
            ver = "verified" if perm == "public_domain" else "needs_review"

            cur.execute(
                """
                INSERT INTO dictionary_entries (
                    id, dictionary_id, headword, normalized_headword,
                    alternate_spellings, transliteration, definitions_en,
                    definitions_hi, other_definitions, part_of_speech,
                    pronunciation, notes, examples, dialect, page_or_section,
                    extraction_method, confidence, license, permission_status,
                    verification_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    dictionary_id=excluded.dictionary_id,
                    headword=excluded.headword,
                    normalized_headword=excluded.normalized_headword,
                    alternate_spellings=excluded.alternate_spellings,
                    definitions_en=excluded.definitions_en,
                    definitions_hi=excluded.definitions_hi,
                    part_of_speech=excluded.part_of_speech,
                    examples=excluded.examples,
                    dialect=excluded.dialect,
                    page_or_section=excluded.page_or_section,
                    license=excluded.license,
                    permission_status=excluded.permission_status,
                    verification_status=excluded.verification_status
                """,
                (
                    ent_id,
                    did,
                    hw,
                    norm_hw,
                    alts,
                    None,
                    defs_en,
                    defs_hi,
                    json.dumps([]),
                    pos,
                    None,
                    None,
                    examples,
                    ent.get("dialect", data.get("dialect")),
                    page,
                    "structured_ingest",
                    1.0,
                    data.get("license"),
                    perm,
                    ver,
                ),
            )
            total_entries_synced += 1

    conn.commit()
    conn.close()
    print(f"Synced {len(records)} dictionaries and {total_entries_synced} entries to {db_path.name}")


def main() -> None:
    for db in DATABASES:
        sync_dictionaries_to_database(db)


if __name__ == "__main__":
    main()
