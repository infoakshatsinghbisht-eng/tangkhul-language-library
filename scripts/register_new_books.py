"""Register 6 new books in manifest and ingest into SQLite corpus database."""

from __future__ import annotations

import json
from pathlib import Path

from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.ingestion.pipeline import DocumentIngestionPipeline
from tangkhul_lib.storage.database import DatabaseManager

WORKSPACE = Path("f:/tangkhul-language-library")
MANIFEST_PATH = WORKSPACE / "data" / "manifests" / "books.jsonl"
RAW_DIR = WORKSPACE / "data" / "raw" / "books"

NEW_BOOKS = [
    {
        "id": "BK-ARCH-002",
        "resource_type": "books",
        "title": "Jesuwui La: Hymns in Tangkhul Naga",
        "alternate_titles": ["Hymns in Tangkhul Naga (1907)"],
        "authors": ["William Pettigrew"],
        "editors": [],
        "publisher": "American Baptist Mission House, Ukhrul, Manipur",
        "publication_year": 1907,
        "year": 1907,
        "edition": "Second Edition",
        "subject": "Hymnology and Devotional Poetry",
        "educational_level": "Historical / Church / Elementary",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "hymnsintangkhuln00pett",
        "catalogue_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/books/BK-ARCH-002_pettigrew_1907.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Second edition of 78-page historical Tangkhul hymnal compiled by Rev. William Pettigrew in Ukhrul, Manipur. Public Domain.",
    },
    {
        "id": "BK-ARCH-003",
        "resource_type": "books",
        "title": "The Naga Tribes of Manipur: Tangkhul Sections",
        "alternate_titles": ["The Naga Tribes of Manipur (1911)"],
        "authors": ["Thomas Callan Hodson"],
        "editors": [],
        "publisher": "Macmillan and Co., Limited, London",
        "publication_year": 1911,
        "year": 1911,
        "edition": "First Edition",
        "subject": "Ethnography, Linguistics and Customary Law",
        "educational_level": "Academic / Historical",
        "language": "Tangkhul",
        "dialect": "Ukhrul / Raphei / Kamo",
        "isbn": None,
        "source_url": "https://archive.org/details/nagatribesofmani00hods",
        "source_identifier": "nagatribesofmani00hods",
        "catalogue_url": "https://archive.org/details/nagatribesofmani00hods",
        "local_file_path": "data/raw/books/BK-ARCH-003_hodson_1911.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Classic ethnographic and linguistic documentation of Tangkhul social organization, folktales, ballads, and vocabulary. Public Domain.",
    },
    {
        "id": "BK-LIT-001",
        "resource_type": "books",
        "title": "The Tangkhul Folk Poetry in Song (HAOLA)",
        "alternate_titles": ["Haolaa: Tangkhul Folk Poetry"],
        "authors": ["Ringkahao Horam"],
        "editors": [],
        "publisher": "Naga Cultural Development Society (NCDS) & Tribal Research Institute, Manipur",
        "publication_year": 2013,
        "year": 2013,
        "edition": "First Edition",
        "subject": "Folk Poetry and Traditional Music",
        "educational_level": "Academic / Cultural",
        "language": "Tangkhul",
        "dialect": "Standard & Regional Tangkhul Dialects",
        "isbn": None,
        "source_url": "https://archive.org/details/dli.language.1350",
        "source_identifier": "dli.language.1350",
        "catalogue_url": "https://archive.org/details/dli.language.1350",
        "local_file_path": "data/raw/books/BK-LIT-001_horam_2013.txt",
        "file_format": "txt",
        "license": "Educational Cultural Heritage",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Comprehensive 161-poem anthology of traditional Tangkhul folk poetry (Haolaa) covering migration, agricultural cycles, romance, and laments.",
    },
    {
        "id": "BK-LIT-002",
        "resource_type": "books",
        "title": "Folk Songs of The Tangkhul",
        "alternate_titles": ["Tangkhul Hao Art & Cultural Council Folk Songs"],
        "authors": ["H. Kamkhenthang", "A. Ngashan Chahong"],
        "editors": [],
        "publisher": "Directorate for Development of Tribals & Backward Classes, Manipur",
        "publication_year": 1987,
        "year": 1987,
        "edition": "First Edition",
        "subject": "Ethnomusicology and Oral Lore",
        "educational_level": "Community / Cultural",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://archive.org/details/dli.language.1472",
        "source_identifier": "dli.language.1472",
        "catalogue_url": "https://archive.org/details/dli.language.1472",
        "local_file_path": "data/raw/books/BK-LIT-002_kamkhenthang_1987.txt",
        "file_format": "txt",
        "license": "Government Documentation Scheme",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Anthology of 27 representative genres of Tangkhul folk music documented under the North Eastern Council Scheme of Tribal Culture.",
    },
    {
        "id": "BK-LIT-003",
        "resource_type": "books",
        "title": "Tangkhul Gee Wari Singbul (Tangkhul Folktale Compendium)",
        "alternate_titles": ["Tangkhul Folktales and Legends"],
        "authors": ["Y. K. Shimray"],
        "editors": [],
        "publisher": "Cultural Heritage of Manipur, Imphal",
        "publication_year": 1976,
        "year": 1976,
        "edition": "First Edition",
        "subject": "Oral Literature and Mythological Legends",
        "educational_level": "General / Cultural",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://archive.org/details/in.ernet.dli.2015.466362",
        "source_identifier": "in.ernet.dli.2015.466362",
        "catalogue_url": "https://archive.org/details/in.ernet.dli.2015.466362",
        "local_file_path": "data/raw/books/BK-LIT-003_shimray_1976.txt",
        "file_format": "txt",
        "license": "Cultural Preservation",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Classic anthology of 35 Tangkhul folktales, founding myths of Hundung and Ukhrul, animal fables, and customary legal allegories.",
    },
    {
        "id": "BK-CIIL-004",
        "resource_type": "books",
        "title": "Tangkhul-English, Hindi Dictionary",
        "alternate_titles": ["Tangkhul Trilingual Dictionary"],
        "authors": ["S. Arokianathan", "Rekha Sharma"],
        "editors": [],
        "publisher": "Central Institute of Indian Languages, Mysore",
        "publication_year": 1995,
        "year": 1995,
        "edition": "First Edition",
        "subject": "Trilingual Lexicography",
        "educational_level": "Academic / Reference",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "81-7342-028-9",
        "source_url": "https://archive.org/details/tangkhulenglishh00arok",
        "source_identifier": "tangkhulenglishh00arok",
        "catalogue_url": "https://archive.org/details/tangkhulenglishh00arok",
        "local_file_path": "data/raw/books/BK-CIIL-004_arokianathan_1995.txt",
        "file_format": "txt",
        "license": "Academic Research Edition",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Comprehensive 140-page trilingual reference lexicon published by CIIL, documenting word classes, phonetic forms, and syntactic patterns.",
    },
]

# 1. Update manifest
existing_lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
existing_ids = set()
for line in existing_lines:
    if line.strip():
        rec = json.loads(line)
        existing_ids.add(rec["id"])

added = 0
with MANIFEST_PATH.open("a", encoding="utf-8") as f:
    for nb in NEW_BOOKS:
        # Validate through BookRecord dataclass
        record = BookRecord(**nb)
        record.validate()
        if nb["id"] not in existing_ids:
            f.write(json.dumps(nb, ensure_ascii=False) + "\n")
            existing_ids.add(nb["id"])
            added += 1
            print(f"Added to manifest: {nb['id']} - {nb['title']}")
        else:
            print(f"Already in manifest: {nb['id']}")

print(f"Manifest updated. Total books in manifest: {len(existing_ids)}")

# 2. Ingest raw files into SQLite database
config = LibraryConfig.from_environment()
db_manager = DatabaseManager(config.get_database_path())
pipeline = DocumentIngestionPipeline(
    db_manager=db_manager,
    config=config,
)

ingested = 0
for nb in NEW_BOOKS:
    bid = nb["id"]
    fpath = RAW_DIR / Path(nb["local_file_path"]).name
    if fpath.exists():
        doc_id = pipeline.ingest_document(bid, file_path=fpath, force=True)
        print(f"Ingested {bid} into SQLite (Doc ID: {doc_id})")
        ingested += 1

import shutil

bundled_db = WORKSPACE / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"
shutil.copy2(config.get_database_path(), bundled_db)
print(f"Copied updated database to {bundled_db}")
print("Ingestion complete.")
