"""Script to ingest public domain books into the SQLite corpus database."""

import sys

from tangkhul_lib.core.config import get_config
from tangkhul_lib.ingestion.pipeline import DocumentIngestionPipeline
from tangkhul_lib.storage.database import DatabaseManager

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

config = get_config()
db = DatabaseManager(config.get_database_path())
pipeline = DocumentIngestionPipeline(db_manager=db)

raw_dir = config.paths.raw_dir / "books"
for sid, fname in [
    ("BK-ARCH-001", "BK-ARCH-001_grierson_1903.txt"),
    ("BK-HIST-001", "BK-HIST-001_pettigrew_1918.txt"),
    ("BK-HIST-002", "BK-HIST-002_pettigrew_1897.txt"),
]:
    fpath = raw_dir / fname
    res = pipeline.ingest_document(sid, file_path=fpath, force=True)
    success = res.get("success")
    pages = res.get("page_count")
    chunks = res.get("chunks_count") or res.get("chunk_count")
    tokens = res.get("tokens_extracted")
    reason = res.get("reason")
    print(f"Ingested {sid}: success={success}, pages={pages}, chunks={chunks}, tokens={tokens}, reason={reason}")

