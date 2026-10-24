"""Database connectivity and schema initialization interfaces.

Planned Storage Backend:
    SQLite database storing unified vocabulary, source provenance, and manifest catalogues.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseManager:
    """Manages SQLite connections for Tangkhul corpus and vocabulary data."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a configured SQLite connection."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize_schema(self) -> None:
        """Initialize database schema tables.

        Note:
            Planned interface. Step 1 defines the architecture; full table schemas
            will be populated during data ingestion steps.
        """
        raise NotImplementedError(
            "Database schema initialization is a planned feature and is not yet "
            "operational in Step 1."
        )
