"""Register Batch 2 of newly discovered books in manifest and ingest into SQLite corpus."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.ingestion.pipeline import DocumentIngestionPipeline
from tangkhul_lib.storage.database import DatabaseManager

WORKSPACE = Path("f:/tangkhul-language-library")
MANIFEST_PATH = WORKSPACE / "data" / "manifests" / "books.jsonl"
RAW_DIR = WORKSPACE / "data" / "raw" / "books"

NEW_BOOKS_BATCH2 = [
    {
        "id": "BK-ARCH-004",
        "resource_type": "books",
        "title": "Pa o Kamata Isha mai Jesu Christawui Khararchan: John Kahona Kasa",
        "alternate_titles": ["The Gospel of St. John in Tangkhul Naga (1904)"],
        "authors": ["William Pettigrew"],
        "editors": [],
        "publisher": "British and Foreign Bible Society, London / Baptist Mission Press, Calcutta",
        "publication_year": 1904,
        "year": 1904,
        "edition": "First Edition",
        "subject": "Biblical Literature & Early Linguistic Translation",
        "educational_level": "Historical / Scriptural / Linguistic",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/gospelofstjohnintangkhul1904",
        "source_identifier": "BFBS-TKH-1904-JOHN",
        "catalogue_url": "https://archive.org/details/gospelofstjohnintangkhul1904",
        "local_file_path": "data/raw/books/BK-ARCH-004_pettigrew_1904.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Pioneering 1904 translation of the Gospel of John into Ukhrul Tangkhul by Rev. William Pettigrew. Published by BFBS. Public Domain.",
    },
    {
        "id": "BK-ARCH-005",
        "resource_type": "books",
        "title": "Pa o Kamata Isha mai Jesu Christawui Khararchan: Luke Kahona Kasan",
        "alternate_titles": ["The Gospel of St. Luke in Tangkhul Naga (1905)"],
        "authors": ["William Pettigrew"],
        "editors": [],
        "publisher": "British and Foreign Bible Society, London / Baptist Mission Press, Calcutta",
        "publication_year": 1905,
        "year": 1905,
        "edition": "First Edition",
        "subject": "Biblical Literature & Vernacular Translation",
        "educational_level": "Historical / Scriptural",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/gospelofstlukeintangkhul1905",
        "source_identifier": "BFBS-TKH-1905-LUKE",
        "catalogue_url": "https://archive.org/details/gospelofstlukeintangkhul1905",
        "local_file_path": "data/raw/books/BK-ARCH-005_pettigrew_1905_luke.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "1905 publication of St. Luke in Tangkhul Naga by Rev. William Pettigrew containing the Parable of the Good Samaritan and Prodigal Son. Public Domain.",
    },
    {
        "id": "BK-ARCH-006",
        "resource_type": "books",
        "title": "Pa o Kachatbingna Kasa wui Khararchan: The Acts of the Apostles",
        "alternate_titles": ["The Acts of the Apostles in Tangkhul Naga (1905)"],
        "authors": ["William Pettigrew"],
        "editors": [],
        "publisher": "British and Foreign Bible Society, London / Baptist Mission Press, Calcutta",
        "publication_year": 1905,
        "year": 1905,
        "edition": "First Edition",
        "subject": "Historical Narrative & Early Vernacular Prose",
        "educational_level": "Historical / Scriptural",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/actsoftheapostlesintangkhul1905",
        "source_identifier": "BFBS-TKH-1905-ACTS",
        "catalogue_url": "https://archive.org/details/actsoftheapostlesintangkhul1905",
        "local_file_path": "data/raw/books/BK-ARCH-006_pettigrew_1905_acts.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Early 20th-century Tangkhul rendering of the Acts of the Apostles by Rev. William Pettigrew. Public Domain.",
    },
    {
        "id": "BK-HIST-003",
        "resource_type": "books",
        "title": "History of the Tangkhul Nagas",
        "alternate_titles": ["History of the Tangkhul Nagas (Shimray 2001)"],
        "authors": ["A. S. W. Shimray"],
        "editors": [],
        "publisher": "Akansha Publishing House, New Delhi",
        "publication_year": 2001,
        "year": 2001,
        "edition": "First Edition",
        "subject": "History, Ethnography, and Customary Institutions",
        "educational_level": "College / Academic Research",
        "language": "English / Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "81-87606-04-5",
        "source_url": "https://openlibrary.org/books/OL3721385M/History_of_the_Tangkhul_Nagas",
        "source_identifier": "ISBN:81-87606-04-5",
        "catalogue_url": "https://openlibrary.org/books/OL3721385M/History_of_the_Tangkhul_Nagas",
        "local_file_path": "data/raw/books/BK-HIST-003_shimray_2001.txt",
        "file_format": "txt",
        "license": "Academic Research / Fair Use Documentation",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Comprehensive ethnographic and historical treatise by A.S.W. Shimray detailing Makhel origins, the Awunga chieftaincy, and village republics.",
    },
    {
        "id": "BK-LIT-004",
        "resource_type": "books",
        "title": "Wung (Tangkhul) Naga Okthot Mayonza",
        "alternate_titles": ["Tangkhul Customary Law, Jurisprudence, and Social Ethics"],
        "authors": ["T. Luikham"],
        "editors": [],
        "publisher": "Tangkhul Literature Society / Published at Imphal",
        "publication_year": 1961,
        "year": 1961,
        "edition": "First Edition",
        "subject": "Customary Law, Tribal Jurisprudence, and Ethics",
        "educational_level": "Community / Traditional Legal Bench",
        "language": "Tangkhul / English",
        "dialect": "Ukhrul / Wung",
        "isbn": None,
        "source_url": "https://openlibrary.org/works/OL1829462W/Wung_Naga_Okthot_Mayonza",
        "source_identifier": "LUIKHAM-1961-MAYONZA",
        "catalogue_url": "https://openlibrary.org/works/OL1829462W/Wung_Naga_Okthot_Mayonza",
        "local_file_path": "data/raw/books/BK-LIT-004_luikham_1961.txt",
        "file_format": "txt",
        "license": "Public Domain / Community Heritage Documentation",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Foundational codification of Tangkhul customary jurisprudence (Mayonza), trial by ordeal, land tenure, and marriage laws by indigenous scholar T. Luikham.",
    },
    {
        "id": "BK-LIT-005",
        "resource_type": "books",
        "title": "Tangkhul Folk Ballads and Oral Narratives (Wungram Khararchan)",
        "alternate_titles": ["Folk Ballads of the Tangkhul Nagas"],
        "authors": ["Khashim Ruivah"],
        "editors": [],
        "publisher": "Tribal Research Institute, Government of Manipur, Imphal",
        "publication_year": 1993,
        "year": 1993,
        "edition": "First Edition",
        "subject": "Oral Literature, Folk Ballads, and Epics",
        "educational_level": "Higher Secondary / University Literature",
        "language": "Tangkhul / English",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://archive.org/details/tangkhulfolkballadsruivah1993",
        "source_identifier": "TRI-MANIPUR-1993-RUIVAH",
        "catalogue_url": "https://archive.org/details/tangkhulfolkballadsruivah1993",
        "local_file_path": "data/raw/books/BK-LIT-005_ruivah_1993.txt",
        "file_format": "txt",
        "license": "Open Access (Tribal Research Institute)",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Fieldwork-based collection of ancestral ballads, courting dialogues (Mawonzai), funeral laments, and hunting chants by Prof. Khashim Ruivah.",
    },
]


def update_manifest() -> None:
    existing_ids = set()
    lines = []
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    data = json.loads(stripped)
                    existing_ids.add(data["id"])
                    lines.append(stripped)

    new_added = 0
    for book in NEW_BOOKS_BATCH2:
        if book["id"] not in existing_ids:
            lines.append(json.dumps(book, ensure_ascii=False))
            existing_ids.add(book["id"])
            new_added += 1

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        for line_str in lines:
            f.write(line_str + "\n")
    print(f"Manifest updated: {new_added} books added. Total records in books.jsonl: {len(lines)}")


def ingest_into_database() -> None:
    config = LibraryConfig.from_environment()
    db_manager = DatabaseManager(config.get_database_path())
    db_manager.initialize_schema()

    pipeline = DocumentIngestionPipeline(db_manager=db_manager, config=config)

    ingested = 0
    for book in NEW_BOOKS_BATCH2:
        bid = book["id"]
        fpath = RAW_DIR / Path(book["local_file_path"]).name
        if not fpath.exists():
            print(f"Warning: File not found {fpath}", flush=True)
            continue

        res = pipeline.ingest_document(bid, file_path=fpath, force=True)
        print(f"Ingested {bid} into SQLite: {res}", flush=True)
        ingested += 1

    bundled_db = WORKSPACE / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"
    shutil.copy2(config.get_database_path(), bundled_db)
    print(f"Successfully copied updated corpus database to {bundled_db}", flush=True)


if __name__ == "__main__":
    update_manifest()
    ingest_into_database()
