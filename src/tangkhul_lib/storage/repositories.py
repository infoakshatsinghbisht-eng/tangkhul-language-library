"""Repository abstractions for vocabulary, provenance, manifests, and books."""

from __future__ import annotations

import datetime
import json
import re
import sqlite3
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any

from tangkhul_lib.core.exceptions import ResourceNotFoundError
from tangkhul_lib.core.models import (
    ConsensusEvaluation,
    DocumentChunk,
    IngestedDocument,
    ManifestRecord,
    ProvenanceRecord,
    ReviewTask,
    VocabularyEntry,
    VocabularyReviewRecord,
)
from tangkhul_lib.storage.database import FTS_SCHEMA_SQL, is_fts5_available

if TYPE_CHECKING:
    from tangkhul_lib.books.models import BookRecord
    from tangkhul_lib.culture.models import CulturalRecord
    from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord
    from tangkhul_lib.history.models import HistoricalRecord
    from tangkhul_lib.literature.models import LiteraryRecord
    from tangkhul_lib.songs.models import SongRecord
    from tangkhul_lib.storage.database import DatabaseManager


class ManifestRepository:
    """Repository interface for querying and persisting catalogued manifests."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, record: ManifestRecord, conn: Any = None) -> None:
        """Store or update a manifest record in the database."""
        sql = """
        INSERT INTO manifest_records (
            id, resource_type, title, title_translation, creator, year,
            publisher, language, dialect, source_url, source_identifier,
            license, permission_status, local_path, verification_status, notes
        ) VALUES (
            :id, :resource_type, :title, :title_translation, :creator, :year,
            :publisher, :language, :dialect, :source_url, :source_identifier,
            :license, :permission_status, :local_path, :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            resource_type = excluded.resource_type,
            title = excluded.title,
            title_translation = excluded.title_translation,
            creator = excluded.creator,
            year = excluded.year,
            publisher = excluded.publisher,
            language = excluded.language,
            dialect = excluded.dialect,
            source_url = excluded.source_url,
            source_identifier = excluded.source_identifier,
            license = excluded.license,
            permission_status = excluded.permission_status,
            local_path = excluded.local_path,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        if conn is not None:
            conn.execute(sql, record.to_dict())
        else:
            with self.db_manager.get_connection() as local_conn:
                local_conn.execute(sql, record.to_dict())
                local_conn.commit()

    def get_by_id(self, record_id: str) -> ManifestRecord | None:
        """Fetch a manifest record by unique identifier."""
        sql = "SELECT * FROM manifest_records WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (record_id,))
            row = cur.fetchone()
            if not row:
                return None
            return ManifestRecord.from_dict(dict(row))

    def list_by_type(self, resource_type: str) -> list[ManifestRecord]:
        """List manifests filtered by resource type."""
        sql = "SELECT * FROM manifest_records WHERE resource_type = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (resource_type,))
            return [ManifestRecord.from_dict(dict(row)) for row in cur.fetchall()]

    def list_all(self) -> list[ManifestRecord]:
        """List all manifest records."""
        sql = "SELECT * FROM manifest_records ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [ManifestRecord.from_dict(dict(row)) for row in cur.fetchall()]


class BookRepository:
    """Repository interface for persisting and querying Tangkhul book records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, book: BookRecord) -> None:
        """Store or update a book record in SQLite."""
        book.validate()
        sql = """
        INSERT INTO books (
            id, title, alternate_titles, authors, editors, publisher,
            publication_year, edition, subject, educational_level,
            language, dialect, isbn, source_url, source_identifier,
            catalogue_url, local_file_path, file_format, license,
            permission_status, access_status, verification_status, notes
        ) VALUES (
            :id, :title, :alternate_titles, :authors, :editors, :publisher,
            :publication_year, :edition, :subject, :educational_level,
            :language, :dialect, :isbn, :source_url, :source_identifier,
            :catalogue_url, :local_file_path, :file_format, :license,
            :permission_status, :access_status, :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            alternate_titles = excluded.alternate_titles,
            authors = excluded.authors,
            editors = excluded.editors,
            publisher = excluded.publisher,
            publication_year = excluded.publication_year,
            edition = excluded.edition,
            subject = excluded.subject,
            educational_level = excluded.educational_level,
            language = excluded.language,
            dialect = excluded.dialect,
            isbn = excluded.isbn,
            source_url = excluded.source_url,
            source_identifier = excluded.source_identifier,
            catalogue_url = excluded.catalogue_url,
            local_file_path = excluded.local_file_path,
            file_format = excluded.file_format,
            license = excluded.license,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        params = {
            "id": book.id,
            "title": book.title,
            "alternate_titles": json.dumps(book.alternate_titles, ensure_ascii=False),
            "authors": json.dumps(book.authors, ensure_ascii=False),
            "editors": json.dumps(book.editors, ensure_ascii=False),
            "publisher": book.publisher,
            "publication_year": book.publication_year,
            "edition": book.edition,
            "subject": book.subject,
            "educational_level": book.educational_level,
            "language": book.language,
            "dialect": book.dialect,
            "isbn": book.isbn,
            "source_url": book.source_url,
            "source_identifier": book.source_identifier,
            "catalogue_url": book.catalogue_url,
            "local_file_path": book.local_file_path,
            "file_format": book.file_format,
            "license": book.license,
            "permission_status": book.permission_status,
            "access_status": book.access_status,
            "verification_status": book.verification_status,
            "notes": book.notes,
        }
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, params)
            # Also synchronize to manifest_records table in the same transaction
            manifest_rec = book.to_manifest_record()
            ManifestRepository(self.db_manager).add(manifest_rec, conn=conn)
            conn.commit()

    def _row_to_book(self, row: dict[str, Any]) -> BookRecord:
        """Convert SQLite row to BookRecord."""
        from tangkhul_lib.books.models import BookRecord

        data = dict(row)
        for list_field in ("alternate_titles", "authors", "editors"):
            val = data.get(list_field)
            if isinstance(val, str):
                try:
                    data[list_field] = json.loads(val)
                except json.JSONDecodeError:
                    data[list_field] = [val]
            elif val is None:
                data[list_field] = []

        return BookRecord.from_dict(data)

    def get_by_id(self, book_id: str) -> BookRecord | None:
        """Retrieve a book by its unique ID."""
        sql = "SELECT * FROM books WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (book_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_book(dict(row))

    def list_all(self) -> list[BookRecord]:
        """List all books in the database."""
        sql = "SELECT * FROM books ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_book(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of books in the database."""
        sql = "SELECT COUNT(*) FROM books;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return cur.fetchone()[0]

    def update(self, book_id: str, updates: dict[str, Any]) -> BookRecord:
        """Update fields of an existing book."""
        current = self.get_by_id(book_id)
        if not current:
            raise ResourceNotFoundError(f"Book '{book_id}' not found in database.")

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.books.models import BookRecord

        updated_book = BookRecord.from_dict(data)
        self.add(updated_book)
        return updated_book

    def save_tokens(
        self,
        source_id: str,
        tokens: list[dict[str, Any]],
    ) -> None:
        """Persist extracted tokens for a source book."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                params = {
                    "source_id": source_id,
                    "word_form": tok.get("word_form", ""),
                    "page_or_section": tok.get("page_or_section"),
                    "context_sentence": tok.get("context_sentence"),
                    "extraction_method": tok.get("extraction_method", "text_extraction"),
                    "verification_status": tok.get("verification_status", "unverified"),
                }
                conn.execute(sql, params)
            conn.commit()

    def get_extracted_tokens(self, source_id: str) -> list[dict[str, Any]]:
        """Retrieve extracted tokens for a given source."""
        sql = "SELECT * FROM extracted_tokens WHERE source_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            return [dict(r) for r in cur.fetchall()]


class SongRepository:
    """Repository interface for persisting and querying Tangkhul song records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, song: SongRecord, conn: Any = None) -> None:
        """Store or update a song record in SQLite."""
        song.validate()
        sql = """
        INSERT INTO songs (
            id, title, alternate_titles, title_translation, singer, lyricist,
            composer, collector, performers, year, village, dialect, song_type,
            language, source_url, source_identifier, recording_url, lyrics_source_url,
            local_file_path, license, permission_status, access_status,
            verification_status, notes
        ) VALUES (
            :id, :title, :alternate_titles, :title_translation, :singer, :lyricist,
            :composer, :collector, :performers, :year, :village, :dialect, :song_type,
            :language, :source_url, :source_identifier, :recording_url, :lyrics_source_url,
            :local_file_path, :license, :permission_status, :access_status,
            :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            alternate_titles = excluded.alternate_titles,
            title_translation = excluded.title_translation,
            singer = excluded.singer,
            lyricist = excluded.lyricist,
            composer = excluded.composer,
            collector = excluded.collector,
            performers = excluded.performers,
            year = excluded.year,
            village = excluded.village,
            dialect = excluded.dialect,
            song_type = excluded.song_type,
            language = excluded.language,
            source_url = excluded.source_url,
            source_identifier = excluded.source_identifier,
            recording_url = excluded.recording_url,
            lyrics_source_url = excluded.lyrics_source_url,
            local_file_path = excluded.local_file_path,
            license = excluded.license,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        params = {
            "id": song.id,
            "title": song.title,
            "alternate_titles": json.dumps(song.alternate_titles, ensure_ascii=False),
            "title_translation": song.title_translation,
            "singer": song.singer,
            "lyricist": song.lyricist,
            "composer": song.composer,
            "collector": song.collector,
            "performers": json.dumps(song.performers, ensure_ascii=False),
            "year": song.year,
            "village": song.village,
            "dialect": song.dialect,
            "song_type": song.song_type,
            "language": song.language,
            "source_url": song.source_url,
            "source_identifier": song.source_identifier,
            "recording_url": song.recording_url,
            "lyrics_source_url": song.lyrics_source_url,
            "local_file_path": song.local_file_path,
            "license": song.license,
            "permission_status": song.permission_status,
            "access_status": song.access_status,
            "verification_status": song.verification_status,
            "notes": song.notes,
        }

        if conn is not None:
            conn.execute(sql, params)
            manifest_rec = song.to_manifest_record()
            ManifestRepository(self.db_manager).add(manifest_rec, conn=conn)
        else:
            with self.db_manager.get_connection() as local_conn:
                local_conn.execute(sql, params)
                manifest_rec = song.to_manifest_record()
                ManifestRepository(self.db_manager).add(manifest_rec, conn=local_conn)
                local_conn.commit()

    def _row_to_song(self, row: dict[str, Any]) -> SongRecord:
        """Convert SQLite row to SongRecord."""
        from tangkhul_lib.songs.models import SongRecord

        data = dict(row)
        for list_field in ("alternate_titles", "performers"):
            val = data.get(list_field)
            if isinstance(val, str):
                try:
                    data[list_field] = json.loads(val)
                except json.JSONDecodeError:
                    data[list_field] = [val]
            elif val is None:
                data[list_field] = []

        return SongRecord.from_dict(data)

    def get_by_id(self, song_id: str) -> SongRecord | None:
        """Retrieve a song by unique ID."""
        sql = "SELECT * FROM songs WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (song_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_song(dict(row))

    def list_all(self) -> list[SongRecord]:
        """List all songs in the database."""
        sql = "SELECT * FROM songs ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_song(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of songs in the database."""
        sql = "SELECT COUNT(*) FROM songs;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return cur.fetchone()[0]

    def update(self, song_id: str, updates: dict[str, Any]) -> SongRecord:
        """Update fields of an existing song."""
        current = self.get_by_id(song_id)
        if not current:
            raise ResourceNotFoundError(f"Song '{song_id}' not found in database.")

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.songs.models import SongRecord

        updated_song = SongRecord.from_dict(data)
        self.add(updated_song)
        return updated_song

    def save_tokens(self, source_id: str, tokens: list[dict[str, Any]]) -> None:
        """Persist extracted tokens for a song."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                params = {
                    "source_id": source_id,
                    "word_form": tok.get("word_form", ""),
                    "page_or_section": tok.get("page_or_section"),
                    "context_sentence": tok.get("context_sentence"),
                    "extraction_method": tok.get("extraction_method", "lyrics_extraction"),
                    "verification_status": tok.get("verification_status", "unverified"),
                }
                conn.execute(sql, params)
            conn.commit()

    def get_extracted_tokens(self, source_id: str) -> list[dict[str, Any]]:
        """Retrieve extracted tokens for a given song."""
        sql = "SELECT * FROM extracted_tokens WHERE source_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            return [dict(r) for r in cur.fetchall()]


def sanitize_fts_query(query: str) -> str:
    """Sanitize raw user query into safe, parameterized FTS5 query syntax."""
    q = query.strip()
    if not q:
        return ""

    if q.startswith('"') and q.endswith('"') and q.count('"') == 2:
        inner = q[1:-1].replace('"', '""').strip()
        return f'"{inner}"' if inner else ""

    tokens: list[str] = []
    raw_tokens = re.findall(r'("[^"]*"|\S+)', q)
    for tok in raw_tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok.startswith('"') and tok.endswith('"') and len(tok) >= 2:
            inner = tok[1:-1].replace('"', '""').strip()
            if inner:
                tokens.append(f'"{inner}"')
        elif tok.upper() in {"AND", "OR", "NOT"}:
            tokens.append(tok.upper())
        else:
            has_star = tok.endswith("*")
            clean = tok.rstrip("*").replace('"', "")
            if clean:
                if has_star:
                    tokens.append(f'"{clean}"*')
                else:
                    tokens.append(f'"{clean}"')

    if not tokens:
        return ""

    filtered: list[str] = []
    for t in tokens:
        if t in {"AND", "OR", "NOT"}:
            if not filtered or filtered[-1] in {"AND", "OR", "NOT"}:
                continue
            filtered.append(t)
        else:
            filtered.append(t)
    while filtered and filtered[-1] in {"AND", "OR", "NOT"}:
        filtered.pop()

    return " ".join(filtered)


class VocabularyRepository:
    """Repository interface for storing and querying unified vocabulary entries and provenance."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, entry: VocabularyEntry) -> None:
        """Persist a vocabulary entry and its associated provenance records."""
        entry_sql = """
        INSERT INTO vocabulary_entries (
            id, headword, meanings, translations_en, alternative_spellings,
            dialect_variants, dialect, part_of_speech, pronunciation,
            example_sentences, verification_status, license_restrictions,
            review_status, review_notes, reviewer, reviewed_at
        ) VALUES (
            :id, :headword, :meanings, :translations_en, :alternative_spellings,
            :dialect_variants, :dialect, :part_of_speech, :pronunciation,
            :example_sentences, :verification_status, :license_restrictions,
            :review_status, :review_notes, :reviewer, :reviewed_at
        )
        ON CONFLICT(id) DO UPDATE SET
            headword = excluded.headword,
            meanings = excluded.meanings,
            translations_en = excluded.translations_en,
            alternative_spellings = excluded.alternative_spellings,
            dialect_variants = excluded.dialect_variants,
            dialect = excluded.dialect,
            part_of_speech = excluded.part_of_speech,
            pronunciation = excluded.pronunciation,
            example_sentences = excluded.example_sentences,
            verification_status = excluded.verification_status,
            license_restrictions = excluded.license_restrictions,
            review_status = excluded.review_status,
            review_notes = excluded.review_notes,
            reviewer = excluded.reviewer,
            reviewed_at = excluded.reviewed_at;
        """
        params = {
            "id": entry.id,
            "headword": entry.headword,
            "meanings": json.dumps(entry.meanings, ensure_ascii=False),
            "translations_en": json.dumps(entry.translations_en, ensure_ascii=False),
            "alternative_spellings": json.dumps(entry.alternative_spellings, ensure_ascii=False),
            "dialect_variants": json.dumps(entry.dialect_variants, ensure_ascii=False),
            "dialect": entry.dialect,
            "part_of_speech": entry.part_of_speech,
            "pronunciation": entry.pronunciation,
            "example_sentences": json.dumps(entry.example_sentences, ensure_ascii=False),
            "verification_status": entry.verification_status,
            "license_restrictions": entry.license_restrictions,
            "review_status": entry.review_status,
            "review_notes": entry.review_notes,
            "reviewer": entry.reviewer,
            "reviewed_at": entry.reviewed_at,
        }

        with self.db_manager.get_connection() as conn:
            conn.execute(entry_sql, params)

            # Clear previous provenance records for this entry to guarantee idempotency on updates
            conn.execute("DELETE FROM provenance_records WHERE vocabulary_id = ?;", (entry.id,))

            # Insert new provenance records (deduplicating identical entries)
            prov_sql = """
            INSERT INTO provenance_records (
                vocabulary_id, source_id, resource_type, citation,
                page_or_section, context_sentence, recorded_year, permission_status
            ) VALUES (
                :vocabulary_id, :source_id, :resource_type, :citation,
                :page_or_section, :context_sentence, :recorded_year, :permission_status
            );
            """
            seen_prov: set[tuple[str, str | None, str | None]] = set()
            for prov in entry.provenance:
                key = (prov.source_id, prov.page_or_section, prov.context_sentence)
                if key in seen_prov:
                    continue
                seen_prov.add(key)
                p_params = prov.to_dict()
                p_params["vocabulary_id"] = entry.id
                conn.execute(prov_sql, p_params)

            if self.is_fts5_available(conn):
                self.index_vocabulary_entry(entry, conn=conn)

            conn.commit()

    def get_by_id(self, entry_id: str) -> VocabularyEntry | None:
        """Fetch an entry by unique identifier, including its provenance records."""
        sql = "SELECT * FROM vocabulary_entries WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (entry_id,))
            row = cur.fetchone()
            if not row:
                return None

            data = dict(row)
            for field_name in (
                "meanings",
                "translations_en",
                "alternative_spellings",
                "dialect_variants",
                "example_sentences",
            ):
                val = data.get(field_name)
                data[field_name] = json.loads(val) if val else []

            # Fetch provenance
            prov_sql = "SELECT * FROM provenance_records WHERE vocabulary_id = ? ORDER BY id;"
            p_cur = conn.execute(prov_sql, (entry_id,))
            provenance_list: list[ProvenanceRecord] = []
            for p_row in p_cur.fetchall():
                p_dict = dict(p_row)
                p_dict.pop("id", None)
                p_dict.pop("vocabulary_id", None)
                provenance_list.append(ProvenanceRecord(**p_dict))

            data["provenance"] = provenance_list
            valid_fields = set(VocabularyEntry.__dataclass_fields__.keys())
            filtered = {k: v for k, v in data.items() if k in valid_fields}
            return VocabularyEntry(**filtered)

    def count(self) -> int:
        """Count total vocabulary entries."""
        sql = "SELECT COUNT(*) FROM vocabulary_entries;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return int(cur.fetchone()[0])

    def list_all(self) -> list[VocabularyEntry]:
        """Fetch all vocabulary entries in a fast, batch-loaded manner."""
        with self.db_manager.get_connection() as conn:
            cur = conn.execute("SELECT * FROM vocabulary_entries ORDER BY headword;")
            rows = cur.fetchall()
            if not rows:
                return []

            p_cur = conn.execute("SELECT * FROM provenance_records ORDER BY id;")
            prov_by_vocab: dict[str, list[ProvenanceRecord]] = {}
            for p_row in p_cur.fetchall():
                p_dict = dict(p_row)
                p_dict.pop("id", None)
                v_id = p_dict.pop("vocabulary_id", None)
                if v_id:
                    prov_by_vocab.setdefault(v_id, []).append(ProvenanceRecord(**p_dict))

            valid_fields = set(VocabularyEntry.__dataclass_fields__.keys())
            results: list[VocabularyEntry] = []
            for row in rows:
                data = dict(row)
                for field_name in (
                    "meanings",
                    "translations_en",
                    "alternative_spellings",
                    "dialect_variants",
                    "example_sentences",
                ):
                    val = data.get(field_name)
                    data[field_name] = json.loads(val) if val else []

                data["provenance"] = prov_by_vocab.get(data["id"], [])
                filtered = {k: v for k, v in data.items() if k in valid_fields}
                results.append(VocabularyEntry(**filtered))
            return results

    def search_by_headword(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching headword (case-insensitive prefix/match)."""
        sql = "SELECT id FROM vocabulary_entries WHERE headword LIKE ? ORDER BY headword;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (f"%{query}%",))
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(entry_id) for entry_id in ids if entry_id is not None]  # type: ignore

    def search_exact(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching exact headword (case-insensitive)."""
        sql = (
            "SELECT id FROM vocabulary_entries "
            "WHERE LOWER(headword) = LOWER(?) ORDER BY headword;"
        )
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (query.strip(),))
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(entry_id) for entry_id in ids if entry_id is not None]  # type: ignore

    def search_by_meaning(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching meaning or translation."""
        sql = (
            "SELECT id FROM vocabulary_entries "
            "WHERE meanings LIKE ? OR translations_en LIKE ? "
            "ORDER BY headword;"
        )
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (f"%{query}%", f"%{query}%"))
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(entry_id) for entry_id in ids if entry_id is not None]  # type: ignore

    def delete(self, entry_id: str) -> None:
        """Delete a vocabulary entry and its associated provenance and FTS records."""
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM vocabulary_entries WHERE id = ?;", (entry_id,))
            conn.execute(
                "DELETE FROM provenance_records WHERE vocabulary_id = ?;",
                (entry_id,),
            )
            if self.is_fts5_available(conn):
                self.remove_from_fts(entry_id, conn=conn)
            conn.commit()

    def is_fts5_available(self, conn: sqlite3.Connection | None = None) -> bool:
        """Check if SQLite FTS5 extension is available."""
        if conn is not None:
            return is_fts5_available(conn)
        with self.db_manager.get_connection() as c:
            return is_fts5_available(c)

    def ensure_fts_schema(self, conn: sqlite3.Connection | None = None) -> bool:
        """Ensure the FTS5 virtual table exists."""
        if conn is not None:
            if not self.is_fts5_available(conn):
                return False
            try:
                conn.executescript(FTS_SCHEMA_SQL)
                return True
            except Exception:
                return False

        with self.db_manager.get_connection() as local_conn:
            if not self.is_fts5_available(local_conn):
                return False
            try:
                local_conn.executescript(FTS_SCHEMA_SQL)
                local_conn.commit()
                return True
            except Exception:
                return False

    def index_vocabulary_entry(
        self,
        entry: VocabularyEntry,
        conn: sqlite3.Connection | None = None,
    ) -> None:
        """Index a single vocabulary entry in FTS5 table."""
        # Never index restricted vocabulary
        if entry.license_restrictions == "restricted":
            self.remove_from_fts(entry.id, conn=conn)
            return

        # Filter out restricted example sentences
        safe_examples = [
            ex for ex in entry.example_sentences
            if entry.license_restrictions != "restricted"
        ]

        sql_delete = "DELETE FROM vocabulary_fts WHERE entry_id = ?;"
        sql_insert = """
        INSERT INTO vocabulary_fts (
            entry_id, headword, alternative_spellings, meanings,
            translations_en, example_sentences, dialect, part_of_speech
        ) VALUES (
            :entry_id, :headword, :alternative_spellings, :meanings,
            :translations_en, :example_sentences, :dialect, :part_of_speech
        );
        """
        params = {
            "entry_id": entry.id,
            "headword": entry.headword,
            "alternative_spellings": " ".join(entry.alternative_spellings),
            "meanings": " ".join(entry.meanings),
            "translations_en": " ".join(entry.translations_en),
            "example_sentences": " ".join(safe_examples),
            "dialect": entry.dialect or "",
            "part_of_speech": entry.part_of_speech or "",
        }

        if conn is not None:
            if not self.is_fts5_available(conn):
                return
            self.ensure_fts_schema(conn=conn)
            try:
                conn.execute(sql_delete, (entry.id,))
                conn.execute(sql_insert, params)
            except Exception:
                pass
        else:
            with self.db_manager.get_connection() as local_conn:
                if not self.is_fts5_available(local_conn):
                    return
                self.ensure_fts_schema(conn=local_conn)
                try:
                    local_conn.execute(sql_delete, (entry.id,))
                    local_conn.execute(sql_insert, params)
                    local_conn.commit()
                except Exception:
                    pass

    def remove_from_fts(
        self,
        entry_id: str,
        conn: sqlite3.Connection | None = None,
    ) -> None:
        """Remove an entry from the FTS5 index."""
        sql = "DELETE FROM vocabulary_fts WHERE entry_id = ?;"
        if conn is not None:
            if self.is_fts5_available(conn):
                try:
                    conn.execute(sql, (entry_id,))
                except Exception:
                    pass
        else:
            with self.db_manager.get_connection() as local_conn:
                if self.is_fts5_available(local_conn):
                    try:
                        local_conn.execute(sql, (entry_id,))
                        local_conn.commit()
                    except Exception:
                        pass

    def rebuild_fts_index(self) -> int:
        """Transactionally rebuild the FTS5 index for all eligible vocabulary entries."""
        with self.db_manager.get_connection() as conn:
            if not self.is_fts5_available(conn):
                return 0
            self.ensure_fts_schema(conn=conn)
            conn.execute("DELETE FROM vocabulary_fts;")

            indexed_count = 0
            for entry in self.list_all():
                if entry and entry.license_restrictions != "restricted":
                    self.index_vocabulary_entry(entry, conn=conn)
                    indexed_count += 1
            conn.commit()
            return indexed_count

    def search_fts(
        self,
        query: str,
        limit: int | None = None,
    ) -> list[tuple[VocabularyEntry, float]]:
        """Search vocabulary entries using FTS5 index, returning (entry, rank)."""
        safe_query = sanitize_fts_query(query)
        if not safe_query:
            return []

        with self.db_manager.get_connection() as conn:
            if not self.is_fts5_available(conn):
                return []
            self.ensure_fts_schema(conn=conn)

            sql = (
                "SELECT entry_id, bm25(vocabulary_fts) AS rank "
                "FROM vocabulary_fts "
                "WHERE vocabulary_fts MATCH ? "
                "ORDER BY rank ASC"
            )
            params: list[Any] = [safe_query]
            if limit is not None and limit > 0:
                sql += " LIMIT ?"
                params.append(limit)

            try:
                cur = conn.execute(sql, params)
                rows = cur.fetchall()
            except sqlite3.OperationalError:
                escaped = f'"{query.replace(chr(34), "")}"'
                try:
                    fallback_sql = (
                        "SELECT entry_id, bm25(vocabulary_fts) AS rank "
                        "FROM vocabulary_fts "
                        "WHERE vocabulary_fts MATCH ? "
                        "ORDER BY rank ASC"
                    )
                    f_params: list[Any] = [escaped]
                    if limit is not None and limit > 0:
                        fallback_sql += " LIMIT ?"
                        f_params.append(limit)
                    cur = conn.execute(fallback_sql, f_params)
                    rows = cur.fetchall()
                except Exception:
                    return []

            results: list[tuple[VocabularyEntry, float]] = []
            for row in rows:
                entry_id = row[0]
                rank = float(row[1]) if row[1] is not None else 0.0
                entry = self.get_by_id(entry_id)
                if entry and entry.license_restrictions != "restricted":
                    results.append((entry, rank))
            return results

    def list_review_queue(
        self,
        review_status: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        dialect: str | None = None,
        missing_meanings: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[VocabularyEntry]:
        """Fetch candidates in deterministic order for the review queue."""
        clauses = []
        params: list[Any] = []

        if review_status:
            clauses.append("v.review_status = ?")
            params.append(review_status)

        if dialect:
            clauses.append("LOWER(v.dialect) = LOWER(?)")
            params.append(dialect.strip())

        if missing_meanings:
            clauses.append(
                "(v.meanings IS NULL OR v.meanings = '[]' "
                "OR v.meanings = '' OR v.meanings = 'null')"
            )

        join_sql = ""
        if source_type or source_id:
            join_sql = "JOIN provenance_records p ON p.vocabulary_id = v.id"
            if source_type:
                clauses.append("p.resource_type = ?")
                params.append(source_type.strip())
            if source_id:
                clauses.append("p.source_id = ?")
                params.append(source_id.strip())

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
        SELECT DISTINCT v.id
        FROM vocabulary_entries v
        {join_sql}
        {where_sql}
        ORDER BY v.created_at ASC, v.headword ASC, v.id ASC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])

        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            ids = [r[0] for r in cur.fetchall()]

        if not ids:
            return []

        id_placeholders = ",".join("?" for _ in ids)
        with self.db_manager.get_connection() as conn:
            v_cur = conn.execute(
                f"SELECT * FROM vocabulary_entries WHERE id IN ({id_placeholders});",
                ids,
            )
            rows_by_id = {row["id"]: row for row in v_cur.fetchall()}

            p_sql = (
                f"SELECT * FROM provenance_records WHERE vocabulary_id IN ({id_placeholders}) "
                "ORDER BY id;"
            )
            p_cur = conn.execute(p_sql, ids)
            prov_by_vocab: dict[str, list[ProvenanceRecord]] = {}
            for p_row in p_cur.fetchall():
                p_dict = dict(p_row)
                p_dict.pop("id", None)
                v_id = p_dict.pop("vocabulary_id", None)
                if v_id:
                    prov_by_vocab.setdefault(v_id, []).append(ProvenanceRecord(**p_dict))

        valid_fields = set(VocabularyEntry.__dataclass_fields__.keys())
        entries: list[VocabularyEntry] = []
        for eid in ids:
            if eid not in rows_by_id:
                continue
            data = dict(rows_by_id[eid])
            for field_name in (
                "meanings",
                "translations_en",
                "alternative_spellings",
                "dialect_variants",
                "example_sentences",
            ):
                val = data.get(field_name)
                data[field_name] = json.loads(val) if val else []

            data["provenance"] = prov_by_vocab.get(eid, [])
            filtered = {k: v for k, v in data.items() if k in valid_fields}
            entries.append(VocabularyEntry(**filtered))
        return entries

    def count_review_queue(
        self,
        review_status: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        dialect: str | None = None,
        missing_meanings: bool = False,
    ) -> int:
        """Count total matching candidates in review queue."""
        clauses = []
        params: list[Any] = []

        if review_status:
            clauses.append("v.review_status = ?")
            params.append(review_status)

        if dialect:
            clauses.append("LOWER(v.dialect) = LOWER(?)")
            params.append(dialect.strip())

        if missing_meanings:
            clauses.append(
                "(v.meanings IS NULL OR v.meanings = '[]' "
                "OR v.meanings = '' OR v.meanings = 'null')"
            )

        join_sql = ""
        if source_type or source_id:
            join_sql = "JOIN provenance_records p ON p.vocabulary_id = v.id"
            if source_type:
                clauses.append("p.resource_type = ?")
                params.append(source_type.strip())
            if source_id:
                clauses.append("p.source_id = ?")
                params.append(source_id.strip())

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
        SELECT COUNT(DISTINCT v.id)
        FROM vocabulary_entries v
        {join_sql}
        {where_sql};
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            return row[0] if row else 0


class VocabularyReviewRepository:
    """Repository interface for persisting and querying vocabulary review audit history."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add_review(self, record: VocabularyReviewRecord) -> int:
        """Record an auditable review action in vocabulary_reviews table."""
        sql = """
        INSERT INTO vocabulary_reviews (
            entry_id, headword, decision, reviewer, notes,
            previous_state, new_state, suggested_meaning,
            suggested_pos, suggested_dialect, target_duplicate_id,
            spelling_assessment, meaning_assessment, pos_assessment,
            dialect_assessment, example_assessment, source_assessment,
            correction_proposals, counts_for_consensus, superseded_by_id
        ) VALUES (
            :entry_id, :headword, :decision, :reviewer, :notes,
            :previous_state, :new_state, :suggested_meaning,
            :suggested_pos, :suggested_dialect, :target_duplicate_id,
            :spelling_assessment, :meaning_assessment, :pos_assessment,
            :dialect_assessment, :example_assessment, :source_assessment,
            :correction_proposals, :counts_for_consensus, :superseded_by_id
        );
        """
        params = {
            "entry_id": record.entry_id,
            "headword": record.headword,
            "decision": record.decision,
            "reviewer": record.reviewer,
            "notes": record.notes,
            "previous_state": json.dumps(record.previous_state, ensure_ascii=False)
            if record.previous_state
            else None,
            "new_state": json.dumps(record.new_state, ensure_ascii=False)
            if record.new_state
            else None,
            "suggested_meaning": record.suggested_meaning,
            "suggested_pos": record.suggested_pos,
            "suggested_dialect": record.suggested_dialect,
            "target_duplicate_id": record.target_duplicate_id,
            "spelling_assessment": record.spelling_assessment,
            "meaning_assessment": record.meaning_assessment,
            "pos_assessment": record.pos_assessment,
            "dialect_assessment": record.dialect_assessment,
            "example_assessment": record.example_assessment,
            "source_assessment": record.source_assessment,
            "correction_proposals": json.dumps(record.correction_proposals, ensure_ascii=False)
            if record.correction_proposals
            else None,
            "counts_for_consensus": 1 if record.counts_for_consensus else 0,
            "superseded_by_id": record.superseded_by_id,
        }
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid or 0

    def get_reviews_for_entry(self, entry_id: str) -> list[VocabularyReviewRecord]:
        """Fetch all historical review decisions for a given vocabulary entry."""
        sql = """
        SELECT * FROM vocabulary_reviews
        WHERE entry_id = ?
        ORDER BY id ASC;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (entry_id,))
            rows = cur.fetchall()

        records: list[VocabularyReviewRecord] = []
        for row in rows:
            data = dict(row)
            if data.get("previous_state"):
                try:
                    data["previous_state"] = json.loads(data["previous_state"])
                except Exception:
                    data["previous_state"] = None
            if data.get("new_state"):
                try:
                    data["new_state"] = json.loads(data["new_state"])
                except Exception:
                    data["new_state"] = None
            if data.get("correction_proposals"):
                try:
                    data["correction_proposals"] = json.loads(data["correction_proposals"])
                except Exception:
                    data["correction_proposals"] = None
            records.append(VocabularyReviewRecord.from_dict(data))
        return records

    def list_recent_reviews(self, limit: int = 50) -> list[VocabularyReviewRecord]:
        """Fetch recent review decisions across all entries."""
        sql = """
        SELECT * FROM vocabulary_reviews
        ORDER BY id DESC
        LIMIT ?;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (limit,))
            rows = cur.fetchall()

        records: list[VocabularyReviewRecord] = []
        for row in rows:
            data = dict(row)
            if data.get("previous_state"):
                try:
                    data["previous_state"] = json.loads(data["previous_state"])
                except Exception:
                    data["previous_state"] = None
            if data.get("new_state"):
                try:
                    data["new_state"] = json.loads(data["new_state"])
                except Exception:
                    data["new_state"] = None
            if data.get("correction_proposals"):
                try:
                    data["correction_proposals"] = json.loads(data["correction_proposals"])
                except Exception:
                    data["correction_proposals"] = None
            records.append(VocabularyReviewRecord.from_dict(data))
        return records

    def list_reviews_by_reviewer(self, reviewer: str) -> list[VocabularyReviewRecord]:
        """Fetch all review decisions recorded by a given reviewer."""
        sql = """
        SELECT * FROM vocabulary_reviews
        WHERE reviewer = ?
        ORDER BY id DESC;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (reviewer,))
            rows = cur.fetchall()

        records: list[VocabularyReviewRecord] = []
        for row in rows:
            data = dict(row)
            if data.get("previous_state"):
                try:
                    data["previous_state"] = json.loads(data["previous_state"])
                except Exception:
                    data["previous_state"] = None
            if data.get("new_state"):
                try:
                    data["new_state"] = json.loads(data["new_state"])
                except Exception:
                    data["new_state"] = None
            if data.get("correction_proposals"):
                try:
                    data["correction_proposals"] = json.loads(data["correction_proposals"])
                except Exception:
                    data["correction_proposals"] = None
            records.append(VocabularyReviewRecord.from_dict(data))
        return records

    def get_all_reviews(self) -> list[VocabularyReviewRecord]:
        """Fetch all review records across all entries."""
        sql = "SELECT * FROM vocabulary_reviews ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            rows = cur.fetchall()

        records: list[VocabularyReviewRecord] = []
        for row in rows:
            data = dict(row)
            if data.get("previous_state"):
                try:
                    data["previous_state"] = json.loads(data["previous_state"])
                except Exception:
                    data["previous_state"] = None
            if data.get("new_state"):
                try:
                    data["new_state"] = json.loads(data["new_state"])
                except Exception:
                    data["new_state"] = None
            if data.get("correction_proposals"):
                try:
                    data["correction_proposals"] = json.loads(data["correction_proposals"])
                except Exception:
                    data["correction_proposals"] = None
            records.append(VocabularyReviewRecord.from_dict(data))
        return records


class ReviewTaskRepository:
    """Repository interface for persisting and managing structured review tasks."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add_task(self, task: ReviewTask) -> None:
        """Store or update a review task in review_tasks table."""
        sql = """
        INSERT OR REPLACE INTO review_tasks (
            id, entry_id, headword, task_type, review_dimensions,
            source_id, priority, reason, status, assigned_reviewer,
            created_at, completed_at, unresolved_disagreements, consensus_outcome
        ) VALUES (
            :id, :entry_id, :headword, :task_type, :review_dimensions,
            :source_id, :priority, :reason, :status, :assigned_reviewer,
            :created_at, :completed_at, :unresolved_disagreements, :consensus_outcome
        );
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        params = {
            "id": task.id,
            "entry_id": task.entry_id,
            "headword": task.headword,
            "task_type": task.task_type,
            "review_dimensions": json.dumps(task.review_dimensions, ensure_ascii=False),
            "source_id": task.source_id,
            "priority": task.priority,
            "reason": task.reason,
            "status": task.status,
            "assigned_reviewer": task.assigned_reviewer,
            "created_at": task.created_at or now,
            "completed_at": task.completed_at,
            "unresolved_disagreements": json.dumps(
                task.unresolved_disagreements, ensure_ascii=False
            ),
            "consensus_outcome": task.consensus_outcome,
        }
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def get_task(self, task_id: str) -> ReviewTask | None:
        """Fetch review task by its deterministic ID."""
        sql = "SELECT * FROM review_tasks WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (task_id,))
            row = cur.fetchone()
            if not row:
                return None
            return ReviewTask.from_dict(dict(row))

    def get_open_task_for_entry(self, entry_id: str) -> ReviewTask | None:
        """Fetch the current non-completed review task for an entry if one exists."""
        sql = """
        SELECT * FROM review_tasks
        WHERE entry_id = ? AND status != 'completed'
        ORDER BY created_at DESC
        LIMIT 1;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (entry_id,))
            row = cur.fetchone()
            if not row:
                return None
            return ReviewTask.from_dict(dict(row))

    def list_tasks(
        self,
        status: str | None = None,
        priority: str | None = None,
        assigned_reviewer: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ReviewTask]:
        """List tasks with deterministic filtering and priority sorting."""
        clauses = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if priority:
            clauses.append("priority = ?")
            params.append(priority)
        if assigned_reviewer:
            clauses.append("assigned_reviewer = ?")
            params.append(assigned_reviewer)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
        SELECT * FROM review_tasks
        {where_sql}
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                ELSE 4
            END,
            created_at ASC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            rows = cur.fetchall()
            return [ReviewTask.from_dict(dict(r)) for r in rows]

    def count_tasks(
        self,
        status: str | None = None,
        priority: str | None = None,
    ) -> int:
        """Count tasks matching status and priority filters."""
        clauses = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if priority:
            clauses.append("priority = ?")
            params.append(priority)
        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT COUNT(*) FROM review_tasks {where_sql};"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            return row[0] if row else 0


class ConsensusRepository:
    """Repository interface for persisting and querying consensus evaluations."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def record_evaluation(self, eval_res: ConsensusEvaluation) -> int:
        """Persist a consensus evaluation record."""
        sql = """
        INSERT INTO review_consensus (
            entry_id, policy_version, threshold_required,
            eligible_reviewers_count, approvals_count, rejections_count,
            conflicts_count, corrections_count, decision_outcome,
            evaluated_at, notes
        ) VALUES (
            :entry_id, :policy_version, :threshold_required,
            :eligible_reviewers_count, :approvals_count, :rejections_count,
            :conflicts_count, :corrections_count, :decision_outcome,
            :evaluated_at, :notes
        );
        """
        params = {
            "entry_id": eval_res.entry_id,
            "policy_version": eval_res.policy_version,
            "threshold_required": eval_res.threshold_required,
            "eligible_reviewers_count": eval_res.eligible_reviewers_count,
            "approvals_count": eval_res.approvals_count,
            "rejections_count": eval_res.rejections_count,
            "conflicts_count": eval_res.conflicts_count,
            "corrections_count": eval_res.corrections_count,
            "decision_outcome": eval_res.decision_outcome,
            "evaluated_at": eval_res.evaluated_at,
            "notes": eval_res.notes,
        }
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid or 0

    def get_latest_for_entry(self, entry_id: str) -> dict[str, Any] | None:
        """Fetch the most recent consensus evaluation for an entry."""
        sql = """
        SELECT * FROM review_consensus
        WHERE entry_id = ?
        ORDER BY id DESC
        LIMIT 1;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (entry_id,))
            row = cur.fetchone()
            return dict(row) if row else None



class DictionaryRepository:
    """Repository interface for persisting Tangkhul dictionaries and lexical entries."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, source: DictionarySourceRecord, conn: Any = None) -> None:
        """Store or update a dictionary source in SQLite and synchronize to manifests."""
        source.validate()
        sql = """
        INSERT INTO dictionaries (
            id, title, alternate_titles, authors, editors, compiler,
            contributors, publisher, publication_place, publication_year,
            edition, languages, language_pair, dialect, source_type,
            isbn, identifier, source_url, local_file_path, license,
            license_evidence, permission_status, access_status,
            verification_status, notes
        ) VALUES (
            :id, :title, :alternate_titles, :authors, :editors, :compiler,
            :contributors, :publisher, :publication_place, :publication_year,
            :edition, :languages, :language_pair, :dialect, :source_type,
            :isbn, :identifier, :source_url, :local_file_path, :license,
            :license_evidence, :permission_status, :access_status,
            :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            alternate_titles = excluded.alternate_titles,
            authors = excluded.authors,
            editors = excluded.editors,
            compiler = excluded.compiler,
            contributors = excluded.contributors,
            publisher = excluded.publisher,
            publication_place = excluded.publication_place,
            publication_year = excluded.publication_year,
            edition = excluded.edition,
            languages = excluded.languages,
            language_pair = excluded.language_pair,
            dialect = excluded.dialect,
            source_type = excluded.source_type,
            isbn = excluded.isbn,
            identifier = excluded.identifier,
            source_url = excluded.source_url,
            local_file_path = excluded.local_file_path,
            license = excluded.license,
            license_evidence = excluded.license_evidence,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        params = {
            "id": source.id,
            "title": source.title,
            "alternate_titles": json.dumps(source.alternate_titles, ensure_ascii=False),
            "authors": json.dumps(source.authors, ensure_ascii=False),
            "editors": json.dumps(source.editors, ensure_ascii=False),
            "compiler": source.compiler,
            "contributors": json.dumps(source.contributors, ensure_ascii=False),
            "publisher": source.publisher,
            "publication_place": source.publication_place,
            "publication_year": source.publication_year,
            "edition": source.edition,
            "languages": json.dumps(source.languages, ensure_ascii=False),
            "language_pair": source.language_pair,
            "dialect": source.dialect,
            "source_type": source.source_type,
            "isbn": source.isbn,
            "identifier": source.identifier,
            "source_url": source.source_url,
            "local_file_path": source.local_file_path,
            "license": source.license,
            "license_evidence": source.license_evidence,
            "permission_status": source.permission_status,
            "access_status": source.access_status,
            "verification_status": source.verification_status,
            "notes": source.notes,
        }

        manifest_rec = source.to_manifest_record()
        manifest_repo = ManifestRepository(self.db_manager)

        if conn is not None:
            conn.execute(sql, params)
            manifest_repo.add(manifest_rec, conn=conn)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                manifest_repo.add(manifest_rec, conn=c)
                c.commit()

    def _row_to_source(self, row: dict[str, Any]) -> DictionarySourceRecord:
        from tangkhul_lib.dictionaries.models import DictionarySourceRecord

        d = dict(row)
        for fld in ("alternate_titles", "authors", "editors", "contributors", "languages"):
            val = d.get(fld)
            d[fld] = json.loads(val) if val else []
        return DictionarySourceRecord.from_dict(d)

    def get_by_id(self, source_id: str) -> DictionarySourceRecord | None:
        """Fetch dictionary source by unique ID."""
        sql = "SELECT * FROM dictionaries WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_source(dict(row))

    def list_all(self) -> list[DictionarySourceRecord]:
        """Fetch all dictionary sources ordered by ID."""
        sql = "SELECT * FROM dictionaries ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_source(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of dictionary sources."""
        sql = "SELECT COUNT(*) FROM dictionaries;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return int(cur.fetchone()[0])

    def update(self, source_id: str, updates: dict[str, Any]) -> DictionarySourceRecord:
        """Update fields of an existing dictionary source."""
        current = self.get_by_id(source_id)
        if not current:
            raise ResourceNotFoundError(f"Dictionary '{source_id}' not found in database.")

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.dictionaries.models import DictionarySourceRecord

        updated_src = DictionarySourceRecord.from_dict(data)
        self.add(updated_src)
        return updated_src

    def add_entry(self, entry: DictionaryEntryRecord, conn: Any = None) -> None:
        """Store or update a dictionary entry in SQLite."""
        entry.validate()
        sql = """
        INSERT INTO dictionary_entries (
            id, dictionary_id, headword, normalized_headword,
            alternate_spellings, transliteration, definitions_en,
            definitions_hi, other_definitions, part_of_speech,
            pronunciation, notes, examples, dialect, grammatical_info,
            page_or_section, entry_number, source_excerpt,
            extraction_method, confidence, license, permission_status,
            verification_status, vocabulary_id
        ) VALUES (
            :id, :dictionary_id, :headword, :normalized_headword,
            :alternate_spellings, :transliteration, :definitions_en,
            :definitions_hi, :other_definitions, :part_of_speech,
            :pronunciation, :notes, :examples, :dialect, :grammatical_info,
            :page_or_section, :entry_number, :source_excerpt,
            :extraction_method, :confidence, :license, :permission_status,
            :verification_status, :vocabulary_id
        )
        ON CONFLICT(id) DO UPDATE SET
            dictionary_id = excluded.dictionary_id,
            headword = excluded.headword,
            normalized_headword = excluded.normalized_headword,
            alternate_spellings = excluded.alternate_spellings,
            transliteration = excluded.transliteration,
            definitions_en = excluded.definitions_en,
            definitions_hi = excluded.definitions_hi,
            other_definitions = excluded.other_definitions,
            part_of_speech = excluded.part_of_speech,
            pronunciation = excluded.pronunciation,
            notes = excluded.notes,
            examples = excluded.examples,
            dialect = excluded.dialect,
            grammatical_info = excluded.grammatical_info,
            page_or_section = excluded.page_or_section,
            entry_number = excluded.entry_number,
            source_excerpt = excluded.source_excerpt,
            extraction_method = excluded.extraction_method,
            confidence = excluded.confidence,
            license = excluded.license,
            permission_status = excluded.permission_status,
            verification_status = excluded.verification_status,
            vocabulary_id = excluded.vocabulary_id;
        """
        params = {
            "id": entry.id,
            "dictionary_id": entry.dictionary_id,
            "headword": entry.headword,
            "normalized_headword": entry.normalized_headword,
            "alternate_spellings": json.dumps(entry.alternate_spellings, ensure_ascii=False),
            "transliteration": entry.transliteration,
            "definitions_en": json.dumps(entry.definitions_en, ensure_ascii=False),
            "definitions_hi": json.dumps(entry.definitions_hi, ensure_ascii=False),
            "other_definitions": json.dumps(entry.other_definitions, ensure_ascii=False),
            "part_of_speech": entry.part_of_speech,
            "pronunciation": entry.pronunciation,
            "notes": entry.notes,
            "examples": json.dumps(entry.examples, ensure_ascii=False),
            "dialect": entry.dialect,
            "grammatical_info": entry.grammatical_info,
            "page_or_section": entry.page_or_section,
            "entry_number": entry.entry_number,
            "source_excerpt": entry.source_excerpt,
            "extraction_method": entry.extraction_method,
            "confidence": entry.confidence,
            "license": entry.license,
            "permission_status": entry.permission_status,
            "verification_status": entry.verification_status,
            "vocabulary_id": entry.vocabulary_id,
        }

        if conn is not None:
            conn.execute(sql, params)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                c.commit()

    def _row_to_entry(self, row: dict[str, Any]) -> DictionaryEntryRecord:
        from tangkhul_lib.dictionaries.models import DictionaryEntryRecord

        d = dict(row)
        for fld in (
            "alternate_spellings",
            "definitions_en",
            "definitions_hi",
            "other_definitions",
            "examples",
        ):
            val = d.get(fld)
            d[fld] = json.loads(val) if val else []
        return DictionaryEntryRecord.from_dict(d)

    def get_entry_by_id(self, entry_id: str) -> DictionaryEntryRecord | None:
        """Fetch dictionary entry by unique entry ID."""
        sql = "SELECT * FROM dictionary_entries WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (entry_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_entry(dict(row))

    def list_entries_by_dictionary(self, dictionary_id: str) -> list[DictionaryEntryRecord]:
        """Fetch all entries belonging to a dictionary source."""
        sql = "SELECT * FROM dictionary_entries WHERE dictionary_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (dictionary_id,))
            return [self._row_to_entry(dict(r)) for r in cur.fetchall()]

    def sync_entry_to_vocabulary(
        self,
        entry: DictionaryEntryRecord,
        vocab_repo: VocabularyRepository,
    ) -> VocabularyEntry:
        """Enrich shared vocabulary database with dictionary entry, preserving provenance."""
        norm_hw = entry.normalized_headword or entry.headword.strip().lower()
        candidates = vocab_repo.search_by_headword(norm_hw)

        matching_vocab: VocabularyEntry | None = None
        for cand in candidates:
            cand_norm = cand.headword.strip().lower()
            if cand_norm == norm_hw and cand.dialect == entry.dialect:
                matching_vocab = cand
                break

        if matching_vocab:
            # Merge dictionary senses without discarding existing senses
            for defn in entry.definitions_en + entry.other_definitions:
                if defn and defn not in matching_vocab.meanings:
                    matching_vocab.meanings.append(defn)
                if defn and defn not in matching_vocab.translations_en:
                    matching_vocab.translations_en.append(defn)

            for alt in entry.alternate_spellings:
                if alt not in matching_vocab.alternative_spellings:
                    matching_vocab.alternative_spellings.append(alt)

            for ex in entry.examples:
                if ex not in matching_vocab.example_sentences:
                    matching_vocab.example_sentences.append(ex)

            if not matching_vocab.part_of_speech and entry.part_of_speech:
                matching_vocab.part_of_speech = entry.part_of_speech

            cite_text = f"Dictionary {entry.dictionary_id}"
            if entry.page_or_section:
                cite_text = f"{cite_text}, {entry.page_or_section}"

            matched_prov = next(
                (
                    p
                    for p in matching_vocab.provenance
                    if p.source_id == entry.dictionary_id
                    and p.page_or_section == entry.page_or_section
                ),
                None,
            )
            if matched_prov:
                matched_prov.citation = cite_text
                matched_prov.permission_status = entry.permission_status
                if entry.examples:
                    matched_prov.context_sentence = entry.examples[0]
            else:
                prov = ProvenanceRecord(
                    source_id=entry.dictionary_id,
                    resource_type="dictionaries",
                    citation=cite_text,
                    page_or_section=entry.page_or_section,
                    context_sentence=entry.examples[0] if entry.examples else None,
                    permission_status=entry.permission_status,
                )
                matching_vocab.provenance.append(prov)
            vocab_repo.add(matching_vocab)
            vocab_entry = matching_vocab
        else:
            vocab_entry = entry.to_vocabulary_entry()
            vocab_repo.add(vocab_entry)

        entry.vocabulary_id = vocab_entry.id
        self.add_entry(entry)
        return vocab_entry


class CultureRepository:
    """Repository interface for persisting and querying Tangkhul cultural records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, record: CulturalRecord, conn: Any = None) -> None:
        """Store or update a cultural record in SQLite and synchronize to manifests."""
        record.validate()
        sql = """
        INSERT INTO culture (
            id, title, local_name, alternate_names, category, subcategory,
            original_text, translation_en, translations_other, description,
            cultural_significance, season_or_timing, village, dialect,
            language, participants, procedure, related_records,
            historical_period, year, source_id, source_title, source_page,
            source_section, source_url, contributor, contributor_consent,
            license, permission_status, access_status, verification_status, notes
        ) VALUES (
            :id, :title, :local_name, :alternate_names, :category, :subcategory,
            :original_text, :translation_en, :translations_other, :description,
            :cultural_significance, :season_or_timing, :village, :dialect,
            :language, :participants, :procedure, :related_records,
            :historical_period, :year, :source_id, :source_title, :source_page,
            :source_section, :source_url, :contributor, :contributor_consent,
            :license, :permission_status, :access_status, :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            local_name = excluded.local_name,
            alternate_names = excluded.alternate_names,
            category = excluded.category,
            subcategory = excluded.subcategory,
            original_text = excluded.original_text,
            translation_en = excluded.translation_en,
            translations_other = excluded.translations_other,
            description = excluded.description,
            cultural_significance = excluded.cultural_significance,
            season_or_timing = excluded.season_or_timing,
            village = excluded.village,
            dialect = excluded.dialect,
            language = excluded.language,
            participants = excluded.participants,
            procedure = excluded.procedure,
            related_records = excluded.related_records,
            historical_period = excluded.historical_period,
            year = excluded.year,
            source_id = excluded.source_id,
            source_title = excluded.source_title,
            source_page = excluded.source_page,
            source_section = excluded.source_section,
            source_url = excluded.source_url,
            contributor = excluded.contributor,
            contributor_consent = excluded.contributor_consent,
            license = excluded.license,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        params = {
            "id": record.id,
            "title": record.title,
            "local_name": record.local_name,
            "alternate_names": json.dumps(record.alternate_names, ensure_ascii=False),
            "category": record.category,
            "subcategory": record.subcategory,
            "original_text": record.original_text,
            "translation_en": record.translation_en,
            "translations_other": json.dumps(record.translations_other, ensure_ascii=False),
            "description": record.description,
            "cultural_significance": record.cultural_significance,
            "season_or_timing": record.season_or_timing,
            "village": record.village,
            "dialect": record.dialect,
            "language": record.language,
            "participants": json.dumps(record.participants, ensure_ascii=False),
            "procedure": json.dumps(record.procedure, ensure_ascii=False),
            "related_records": json.dumps(record.related_records, ensure_ascii=False),
            "historical_period": record.historical_period,
            "year": record.year,
            "source_id": record.source_id,
            "source_title": record.source_title,
            "source_page": record.source_page,
            "source_section": record.source_section,
            "source_url": record.source_url,
            "contributor": record.contributor,
            "contributor_consent": 1 if record.contributor_consent else 0,
            "license": record.license,
            "permission_status": record.permission_status,
            "access_status": record.access_status,
            "verification_status": record.verification_status,
            "notes": record.notes,
        }

        manifest_rec = record.to_manifest_record()
        manifest_repo = ManifestRepository(self.db_manager)

        if conn is not None:
            conn.execute(sql, params)
            manifest_repo.add(manifest_rec, conn=conn)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                manifest_repo.add(manifest_rec, conn=c)
                c.commit()

    def _row_to_record(self, row: dict[str, Any]) -> CulturalRecord:
        from tangkhul_lib.culture.models import CulturalRecord

        d = dict(row)
        for fld in (
            "alternate_names",
            "translations_other",
            "participants",
            "procedure",
            "related_records",
        ):
            val = d.get(fld)
            d[fld] = json.loads(val) if val else []

        if "contributor_consent" in d:
            d["contributor_consent"] = bool(d["contributor_consent"])

        return CulturalRecord.from_dict(d)

    def get_by_id(self, record_id: str) -> CulturalRecord | None:
        """Fetch cultural record by unique ID."""
        sql = "SELECT * FROM culture WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (record_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_record(dict(row))

    def list_all(self) -> list[CulturalRecord]:
        """Fetch all cultural records ordered by ID."""
        sql = "SELECT * FROM culture ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_category(self, category: str) -> list[CulturalRecord]:
        """Fetch all cultural records belonging to a category."""
        sql = "SELECT * FROM culture WHERE category = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (category,))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of cultural records."""
        sql = "SELECT COUNT(*) FROM culture;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return int(cur.fetchone()[0])

    def update(self, record_id: str, updates: dict[str, Any]) -> CulturalRecord:
        """Update fields of an existing cultural record."""
        current = self.get_by_id(record_id)
        if not current:
            raise ResourceNotFoundError(f"Cultural record '{record_id}' not found in database.")

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.culture.models import CulturalRecord

        updated_rec = CulturalRecord.from_dict(data)
        self.add(updated_rec)
        return updated_rec

    def save_tokens(self, source_id: str, tokens: list[dict[str, Any]]) -> None:
        """Persist extracted tokens for a cultural source."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                params = {
                    "source_id": source_id,
                    "word_form": tok.get("word_form", ""),
                    "page_or_section": tok.get("page_or_section"),
                    "context_sentence": tok.get("context_sentence"),
                    "extraction_method": tok.get("extraction_method", "cultural_extraction"),
                    "verification_status": tok.get("verification_status", "unverified"),
                }
                conn.execute(sql, params)
            conn.commit()

    def get_extracted_tokens(self, source_id: str) -> list[dict[str, Any]]:
        """Retrieve extracted tokens for a given cultural source."""
        sql = "SELECT * FROM extracted_tokens WHERE source_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            return [dict(r) for r in cur.fetchall()]

    def sync_record_to_vocabulary(
        self,
        record: CulturalRecord,
        vocab_repo: VocabularyRepository,
    ) -> list[VocabularyEntry]:
        """Extract candidates and enrich shared vocabulary without leaking restricted data."""
        from tangkhul_lib.core.exceptions import PermissionDeniedError

        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot sync restricted cultural record '{record.id}' to shared lexicon.",
                resource_id=record.id,
            )

        candidates = record.extract_vocabulary_candidates()
        self.save_tokens(record.id, candidates)

        synced_entries: list[VocabularyEntry] = []
        for cand in candidates:
            word = cand["word_form"]
            existing = vocab_repo.search_by_headword(word)

            matched: VocabularyEntry | None = None
            for item in existing:
                if item.headword.strip().lower() == word.strip().lower():
                    matched = item
                    break

            if matched:
                cite_text = f"Cultural record {record.id}: {record.title}"
                if record.source_title:
                    cite_text = f"{cite_text} ({record.source_title})"

                cand_page = cand.get("page_or_section")
                cand_ctx = cand.get("context_sentence")
                matched_prov = next(
                    (
                        p
                        for p in matched.provenance
                        if p.source_id == record.id
                        and p.page_or_section == cand_page
                    ),
                    None,
                )
                if matched_prov:
                    matched_prov.citation = cite_text
                    matched_prov.permission_status = record.permission_status
                    if cand_ctx:
                        matched_prov.context_sentence = cand_ctx
                    matched_prov.recorded_year = record.year
                else:
                    prov = ProvenanceRecord(
                        source_id=record.id,
                        resource_type="culture",
                        citation=cite_text,
                        page_or_section=cand_page,
                        context_sentence=cand_ctx,
                        recorded_year=record.year,
                        permission_status=record.permission_status,
                    )
                    matched.provenance.append(prov)
                vocab_repo.add(matched)
                synced_entries.append(matched)
            else:
                new_entry = record.to_vocabulary_entry(headword=word)
                vocab_repo.add(new_entry)
                synced_entries.append(new_entry)

        return synced_entries


class HistoryRepository:
    """Repository interface for persisting and querying Tangkhul historical records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, record: HistoricalRecord, conn: Any = None) -> None:
        """Store or update a historical record in the SQLite database and sync manifest."""
        sql = """
        INSERT INTO history (
            id, title, record_type, alternate_titles, summary, description,
            original_text, translation_en, event_date, sort_year, period,
            place, village, dialect, language, people_involved, related_events,
            related_records, source_id, source_title, source_page, source_section,
            source_url, contributor, contributor_consent, evidence_type,
            confidence, contradictory_accounts, license, permission_status,
            access_status, verification_status, notes
        ) VALUES (
            :id, :title, :record_type, :alternate_titles, :summary, :description,
            :original_text, :translation_en, :event_date, :sort_year, :period,
            :place, :village, :dialect, :language, :people_involved, :related_events,
            :related_records, :source_id, :source_title, :source_page, :source_section,
            :source_url, :contributor, :contributor_consent, :evidence_type,
            :confidence, :contradictory_accounts, :license, :permission_status,
            :access_status, :verification_status, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            record_type = excluded.record_type,
            alternate_titles = excluded.alternate_titles,
            summary = excluded.summary,
            description = excluded.description,
            original_text = excluded.original_text,
            translation_en = excluded.translation_en,
            event_date = excluded.event_date,
            sort_year = excluded.sort_year,
            period = excluded.period,
            place = excluded.place,
            village = excluded.village,
            dialect = excluded.dialect,
            language = excluded.language,
            people_involved = excluded.people_involved,
            related_events = excluded.related_events,
            related_records = excluded.related_records,
            source_id = excluded.source_id,
            source_title = excluded.source_title,
            source_page = excluded.source_page,
            source_section = excluded.source_section,
            source_url = excluded.source_url,
            contributor = excluded.contributor,
            contributor_consent = excluded.contributor_consent,
            evidence_type = excluded.evidence_type,
            confidence = excluded.confidence,
            contradictory_accounts = excluded.contradictory_accounts,
            license = excluded.license,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            notes = excluded.notes;
        """
        params = {
            "id": record.id,
            "title": record.title,
            "record_type": record.record_type,
            "alternate_titles": json.dumps(record.alternate_titles, ensure_ascii=False),
            "summary": record.summary,
            "description": record.description,
            "original_text": record.original_text,
            "translation_en": record.translation_en,
            "event_date": record.event_date,
            "sort_year": record.sort_year,
            "period": record.period,
            "place": record.place,
            "village": record.village,
            "dialect": record.dialect,
            "language": record.language,
            "people_involved": json.dumps(record.people_involved, ensure_ascii=False),
            "related_events": json.dumps(record.related_events, ensure_ascii=False),
            "related_records": json.dumps(record.related_records, ensure_ascii=False),
            "source_id": record.source_id,
            "source_title": record.source_title,
            "source_page": record.source_page,
            "source_section": record.source_section,
            "source_url": record.source_url,
            "contributor": record.contributor,
            "contributor_consent": 1 if record.contributor_consent else 0,
            "evidence_type": record.evidence_type,
            "confidence": record.confidence,
            "contradictory_accounts": json.dumps(
                record.contradictory_accounts, ensure_ascii=False
            ),
            "license": record.license,
            "permission_status": record.permission_status,
            "access_status": record.access_status,
            "verification_status": record.verification_status,
            "notes": record.notes,
        }

        manifest_rec = record.to_manifest_record()
        manifest_repo = ManifestRepository(self.db_manager)

        if conn is not None:
            conn.execute(sql, params)
            manifest_repo.add(manifest_rec, conn=conn)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                manifest_repo.add(manifest_rec, conn=c)
                c.commit()

    def _row_to_record(self, row: dict[str, Any]) -> HistoricalRecord:
        from tangkhul_lib.history.models import HistoricalRecord

        d = dict(row)
        for fld in (
            "alternate_titles",
            "people_involved",
            "related_events",
            "related_records",
            "contradictory_accounts",
        ):
            val = d.get(fld)
            if isinstance(val, str):
                try:
                    d[fld] = json.loads(val)
                except Exception:
                    d[fld] = [val] if val else []
            elif val is None:
                d[fld] = []

        if "contributor_consent" in d:
            d["contributor_consent"] = bool(d["contributor_consent"])

        d.pop("created_at", None)
        return HistoricalRecord.from_dict(d)

    def get_by_id(self, record_id: str) -> HistoricalRecord | None:
        """Fetch historical record by ID."""
        sql = "SELECT * FROM history WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (record_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_record(dict(row))

    def list_all(self, sort_by_date: bool = True) -> list[HistoricalRecord]:
        """Fetch all historical records, sorted chronologically or by ID."""
        if sort_by_date:
            sql = """
            SELECT * FROM history
            ORDER BY CASE WHEN sort_year IS NULL THEN 1 ELSE 0 END, sort_year ASC, id ASC;
            """
        else:
            sql = "SELECT * FROM history ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_type(self, record_type: str) -> list[HistoricalRecord]:
        """Filter historical records by record type."""
        sql = """
        SELECT * FROM history
        WHERE record_type = ?
        ORDER BY CASE WHEN sort_year IS NULL THEN 1 ELSE 0 END, sort_year ASC, id ASC;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (record_type,))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_period(self, period: str) -> list[HistoricalRecord]:
        """Filter historical records by historical period."""
        sql = """
        SELECT * FROM history
        WHERE period = ? COLLATE NOCASE
        ORDER BY CASE WHEN sort_year IS NULL THEN 1 ELSE 0 END, sort_year ASC, id ASC;
        """
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (period,))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_place(self, place: str) -> list[HistoricalRecord]:
        """Filter historical records by place or settlement."""
        sql = """
        SELECT * FROM history
        WHERE place LIKE ? OR village LIKE ?
        ORDER BY CASE WHEN sort_year IS NULL THEN 1 ELSE 0 END, sort_year ASC, id ASC;
        """
        pattern = f"%{place}%"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (pattern, pattern))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def get_timeline(
        self,
        start_year: int | None = None,
        end_year: int | None = None,
    ) -> list[HistoricalRecord]:
        """Fetch chronologically ordered records within an optional year range."""
        conditions = ["sort_year IS NOT NULL"]
        params: list[Any] = []
        if start_year is not None:
            conditions.append("sort_year >= ?")
            params.append(start_year)
        if end_year is not None:
            conditions.append("sort_year <= ?")
            params.append(end_year)

        where_clause = " AND ".join(conditions)
        sql = f"SELECT * FROM history WHERE {where_clause} ORDER BY sort_year ASC, id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, tuple(params))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of historical records."""
        sql = "SELECT COUNT(*) FROM history;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return int(cur.fetchone()[0])

    def update(self, record_id: str, updates: dict[str, Any]) -> HistoricalRecord:
        """Update fields of an existing historical record."""
        current = self.get_by_id(record_id)
        if not current:
            raise ResourceNotFoundError(
                f"Historical record '{record_id}' not found in database."
            )

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.history.models import HistoricalRecord

        updated_rec = HistoricalRecord.from_dict(data)
        self.add(updated_rec)
        return updated_rec

    def save_tokens(self, source_id: str, tokens: list[dict[str, Any]]) -> None:
        """Persist extracted tokens for a historical source."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                params = {
                    "source_id": source_id,
                    "word_form": tok.get("word_form", ""),
                    "page_or_section": tok.get("page_or_section"),
                    "context_sentence": tok.get("context_sentence"),
                    "extraction_method": tok.get(
                        "extraction_method", "historical_extraction"
                    ),
                    "verification_status": tok.get("verification_status", "unverified"),
                }
                conn.execute(sql, params)
            conn.commit()

    def get_extracted_tokens(self, source_id: str) -> list[dict[str, Any]]:
        """Retrieve extracted tokens for a given historical source."""
        sql = "SELECT * FROM extracted_tokens WHERE source_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            return [dict(r) for r in cur.fetchall()]

    def sync_record_to_vocabulary(
        self,
        record: HistoricalRecord,
        vocab_repo: VocabularyRepository,
    ) -> list[VocabularyEntry]:
        """Extract candidates and enrich shared vocabulary without leaking restricted data."""
        from tangkhul_lib.core.exceptions import PermissionDeniedError

        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot sync restricted historical record '{record.id}' to shared lexicon.",
                resource_id=record.id,
            )

        candidates = record.extract_vocabulary_candidates()
        self.save_tokens(record.id, candidates)

        synced_entries: list[VocabularyEntry] = []
        for cand in candidates:
            word = cand["word_form"]
            existing = vocab_repo.search_by_headword(word)

            matched: VocabularyEntry | None = None
            for item in existing:
                if item.headword.strip().lower() == word.strip().lower():
                    matched = item
                    break

            if matched:
                cite_text = f"Historical record {record.id}: {record.title}"
                if record.source_title:
                    cite_text = f"{cite_text} ({record.source_title})"

                cand_page = cand.get("page_or_section")
                cand_ctx = cand.get("context_sentence")
                matched_prov = next(
                    (
                        p
                        for p in matched.provenance
                        if p.source_id == record.id
                        and p.page_or_section == cand_page
                    ),
                    None,
                )
                if matched_prov:
                    matched_prov.citation = cite_text
                    matched_prov.permission_status = record.permission_status
                    if cand_ctx:
                        matched_prov.context_sentence = cand_ctx
                    matched_prov.recorded_year = record.sort_year
                else:
                    prov = ProvenanceRecord(
                        source_id=record.id,
                        resource_type="history",
                        citation=cite_text,
                        page_or_section=cand_page,
                        context_sentence=cand_ctx,
                        recorded_year=record.sort_year,
                        permission_status=record.permission_status,
                    )
                    matched.provenance.append(prov)
                vocab_repo.add(matched)
                synced_entries.append(matched)
            else:
                new_entry = record.to_vocabulary_entry(headword=word)
                vocab_repo.add(new_entry)
                synced_entries.append(new_entry)

        return synced_entries


class LiteratureRepository:
    """Repository interface for persisting and querying Tangkhul literary works."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, record: LiteraryRecord, conn: Any = None) -> None:
        """Store or update a literary record in SQLite database and sync manifest."""
        sql = """
        INSERT INTO literature (
            id, title, work_type, alternate_titles, original_title, title_translation,
            genres, author, poet, storyteller, playwright, translator, editor,
            collector, contributor, contributor_consent, publication_year,
            composition_date, edition, publisher, publication_place, language,
            dialect, village, region, collection, anthology, parent_work_id,
            book_id, isbn, identifier, source_url, source_id, source_title,
            source_page, source_section, local_path, license, license_evidence,
            permission_status, access_status, verification_status,
            text_availability, original_text, translation_text, summary,
            stanza_count, line_count, related_authors, related_works,
            related_records, notes
        ) VALUES (
            :id, :title, :work_type, :alternate_titles, :original_title, :title_translation,
            :genres, :author, :poet, :storyteller, :playwright, :translator, :editor,
            :collector, :contributor, :contributor_consent, :publication_year,
            :composition_date, :edition, :publisher, :publication_place, :language,
            :dialect, :village, :region, :collection, :anthology, :parent_work_id,
            :book_id, :isbn, :identifier, :source_url, :source_id, :source_title,
            :source_page, :source_section, :local_path, :license, :license_evidence,
            :permission_status, :access_status, :verification_status,
            :text_availability, :original_text, :translation_text, :summary,
            :stanza_count, :line_count, :related_authors, :related_works,
            :related_records, :notes
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            work_type = excluded.work_type,
            alternate_titles = excluded.alternate_titles,
            original_title = excluded.original_title,
            title_translation = excluded.title_translation,
            genres = excluded.genres,
            author = excluded.author,
            poet = excluded.poet,
            storyteller = excluded.storyteller,
            playwright = excluded.playwright,
            translator = excluded.translator,
            editor = excluded.editor,
            collector = excluded.collector,
            contributor = excluded.contributor,
            contributor_consent = excluded.contributor_consent,
            publication_year = excluded.publication_year,
            composition_date = excluded.composition_date,
            edition = excluded.edition,
            publisher = excluded.publisher,
            publication_place = excluded.publication_place,
            language = excluded.language,
            dialect = excluded.dialect,
            village = excluded.village,
            region = excluded.region,
            collection = excluded.collection,
            anthology = excluded.anthology,
            parent_work_id = excluded.parent_work_id,
            book_id = excluded.book_id,
            isbn = excluded.isbn,
            identifier = excluded.identifier,
            source_url = excluded.source_url,
            source_id = excluded.source_id,
            source_title = excluded.source_title,
            source_page = excluded.source_page,
            source_section = excluded.source_section,
            local_path = excluded.local_path,
            license = excluded.license,
            license_evidence = excluded.license_evidence,
            permission_status = excluded.permission_status,
            access_status = excluded.access_status,
            verification_status = excluded.verification_status,
            text_availability = excluded.text_availability,
            original_text = excluded.original_text,
            translation_text = excluded.translation_text,
            summary = excluded.summary,
            stanza_count = excluded.stanza_count,
            line_count = excluded.line_count,
            related_authors = excluded.related_authors,
            related_works = excluded.related_works,
            related_records = excluded.related_records,
            notes = excluded.notes;
        """
        params = {
            "id": record.id,
            "title": record.title,
            "work_type": record.work_type,
            "alternate_titles": json.dumps(record.alternate_titles, ensure_ascii=False),
            "original_title": record.original_title,
            "title_translation": record.title_translation,
            "genres": json.dumps(record.genres, ensure_ascii=False),
            "author": record.author,
            "poet": record.poet,
            "storyteller": record.storyteller,
            "playwright": record.playwright,
            "translator": record.translator,
            "editor": record.editor,
            "collector": record.collector,
            "contributor": record.contributor,
            "contributor_consent": 1 if record.contributor_consent else 0,
            "publication_year": record.publication_year,
            "composition_date": record.composition_date,
            "edition": record.edition,
            "publisher": record.publisher,
            "publication_place": record.publication_place,
            "language": record.language,
            "dialect": record.dialect,
            "village": record.village,
            "region": record.region,
            "collection": record.collection,
            "anthology": record.anthology,
            "parent_work_id": record.parent_work_id,
            "book_id": record.book_id,
            "isbn": record.isbn,
            "identifier": record.identifier,
            "source_url": record.source_url,
            "source_id": record.source_id,
            "source_title": record.source_title,
            "source_page": record.source_page,
            "source_section": record.source_section,
            "local_path": record.local_path,
            "license": record.license,
            "license_evidence": record.license_evidence,
            "permission_status": record.permission_status,
            "access_status": record.access_status,
            "verification_status": record.verification_status,
            "text_availability": record.text_availability,
            "original_text": record.original_text,
            "translation_text": record.translation_text,
            "summary": record.summary,
            "stanza_count": record.stanza_count,
            "line_count": record.line_count,
            "related_authors": json.dumps(record.related_authors, ensure_ascii=False),
            "related_works": json.dumps(record.related_works, ensure_ascii=False),
            "related_records": json.dumps(record.related_records, ensure_ascii=False),
            "notes": record.notes,
        }

        manifest_rec = record.to_manifest_record()
        manifest_repo = ManifestRepository(self.db_manager)

        if conn is not None:
            conn.execute(sql, params)
            manifest_repo.add(manifest_rec, conn=conn)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                manifest_repo.add(manifest_rec, conn=c)
                c.commit()

    def _row_to_record(self, row: dict[str, Any]) -> LiteraryRecord:
        from tangkhul_lib.literature.models import LiteraryRecord

        d = dict(row)
        for fld in (
            "alternate_titles",
            "genres",
            "related_authors",
            "related_works",
            "related_records",
        ):
            val = d.get(fld)
            if isinstance(val, str):
                try:
                    d[fld] = json.loads(val)
                except Exception:
                    d[fld] = [val] if val else []
            elif val is None:
                d[fld] = []

        if "contributor_consent" in d:
            d["contributor_consent"] = bool(d["contributor_consent"])

        d.pop("created_at", None)
        return LiteraryRecord.from_dict(d)

    def get_by_id(self, work_id: str) -> LiteraryRecord | None:
        """Fetch literary work by ID."""
        sql = "SELECT * FROM literature WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (work_id,))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_record(dict(row))

    def list_all(self, sort_by_year: bool = False) -> list[LiteraryRecord]:
        """Fetch all literary works, sorted by ID or chronologically."""
        if sort_by_year:
            sql = """
            SELECT * FROM literature
            ORDER BY CASE WHEN publication_year IS NULL THEN 1 ELSE 0 END,
                     publication_year ASC, id ASC;
            """
        else:
            sql = "SELECT * FROM literature ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_genre(self, genre: str) -> list[LiteraryRecord]:
        """Filter literary works by work_type or genre."""
        sql = """
        SELECT * FROM literature
        WHERE work_type = ? OR genres LIKE ?
        ORDER BY id ASC;
        """
        pattern = f"%\"{genre}\"%"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (genre, pattern))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_author(self, author: str) -> list[LiteraryRecord]:
        """Filter literary works by author, poet, or storyteller."""
        sql = """
        SELECT * FROM literature
        WHERE author LIKE ? OR poet LIKE ? OR storyteller LIKE ? OR playwright LIKE ?
        ORDER BY id ASC;
        """
        pattern = f"%{author}%"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (pattern, pattern, pattern, pattern))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def list_by_book_id(self, book_id: str) -> list[LiteraryRecord]:
        """Filter literary works linked to a specific book ID."""
        sql = "SELECT * FROM literature WHERE book_id = ? ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (book_id,))
            return [self._row_to_record(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Return total count of literary records."""
        sql = "SELECT COUNT(*) FROM literature;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            return int(cur.fetchone()[0])

    def update(self, work_id: str, updates: dict[str, Any]) -> LiteraryRecord:
        """Update fields of an existing literary work."""
        current = self.get_by_id(work_id)
        if not current:
            raise ResourceNotFoundError(
                f"Literary work '{work_id}' not found in database."
            )

        data = current.to_dict()
        updates_clean = {k: v for k, v in updates.items() if k != "id"}
        data.update(updates_clean)

        from tangkhul_lib.literature.models import LiteraryRecord

        updated_rec = LiteraryRecord.from_dict(data)
        self.add(updated_rec)
        return updated_rec

    def save_tokens(self, source_id: str, tokens: list[dict[str, Any]]) -> None:
        """Persist extracted tokens for a literary work."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                params = {
                    "source_id": source_id,
                    "word_form": tok.get("word_form", ""),
                    "page_or_section": tok.get("page_or_section"),
                    "context_sentence": tok.get("context_sentence"),
                    "extraction_method": tok.get(
                        "extraction_method", "literary_extraction"
                    ),
                    "verification_status": tok.get("verification_status", "unverified"),
                }
                conn.execute(sql, params)
            conn.commit()

    def get_extracted_tokens(self, source_id: str) -> list[dict[str, Any]]:
        """Retrieve extracted tokens for a given literary work."""
        sql = "SELECT * FROM extracted_tokens WHERE source_id = ? ORDER BY id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            return [dict(r) for r in cur.fetchall()]

    def sync_record_to_vocabulary(
        self,
        record: LiteraryRecord,
        vocab_repo: VocabularyRepository,
    ) -> list[VocabularyEntry]:
        """Extract candidates and enrich shared vocabulary without leaking restricted data."""
        from tangkhul_lib.core.exceptions import PermissionDeniedError

        if record.permission_status == "restricted":
            raise PermissionDeniedError(
                f"Cannot sync restricted literary work '{record.id}' to shared lexicon.",
                resource_id=record.id,
            )

        candidates = record.extract_vocabulary_candidates()
        self.save_tokens(record.id, candidates)

        synced_entries: list[VocabularyEntry] = []
        for cand in candidates:
            word = cand["word_form"]
            existing = vocab_repo.search_by_headword(word)

            matched: VocabularyEntry | None = None
            for item in existing:
                if item.headword.strip().lower() == word.strip().lower():
                    matched = item
                    break

            if matched:
                cite_text = f"Literary work {record.id}: {record.title}"
                if record.author:
                    cite_text = f"{cite_text} by {record.author}"

                cand_page = cand.get("page_or_section")
                cand_ctx = cand.get("context_sentence")
                matched_prov = next(
                    (
                        p
                        for p in matched.provenance
                        if p.source_id == record.id
                        and p.page_or_section == cand_page
                    ),
                    None,
                )
                if matched_prov:
                    matched_prov.citation = cite_text
                    matched_prov.permission_status = record.permission_status
                    if cand_ctx:
                        matched_prov.context_sentence = cand_ctx
                    matched_prov.recorded_year = record.publication_year
                else:
                    prov = ProvenanceRecord(
                        source_id=record.id,
                        resource_type="literature",
                        citation=cite_text,
                        page_or_section=cand_page,
                        context_sentence=cand_ctx,
                        recorded_year=record.publication_year,
                        permission_status=record.permission_status,
                    )
                    matched.provenance.append(prov)
                vocab_repo.add(matched)
                synced_entries.append(matched)
            else:
                new_entry = record.to_vocabulary_entry(headword=word)
                vocab_repo.add(new_entry)
                synced_entries.append(new_entry)

        return synced_entries


class DocumentRepository:
    """Repository interface for persisting and querying ingested documents and chunks."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def is_fts5_available(self, conn: sqlite3.Connection | None = None) -> bool:
        """Check if SQLite FTS5 extension is available."""
        return is_fts5_available(conn)

    def add_document(
        self,
        doc: IngestedDocument,
        chunks: list[DocumentChunk],
    ) -> None:
        """Persist or update an ingested document and its paragraph chunks transactionally."""
        doc_sql = """
        INSERT INTO ingested_documents (
            id, source_id, source_title, creator, publication_year,
            source_type, language, file_path, file_name, file_hash,
            file_size_bytes, file_format, extraction_method, extraction_timestamp,
            extraction_status, page_count, char_count, word_count,
            permission_status, verification_status, extraction_warnings,
            ocr_status, review_status, notes, updated_at
        ) VALUES (
            :id, :source_id, :source_title, :creator, :publication_year,
            :source_type, :language, :file_path, :file_name, :file_hash,
            :file_size_bytes, :file_format, :extraction_method, :extraction_timestamp,
            :extraction_status, :page_count, :char_count, :word_count,
            :permission_status, :verification_status, :extraction_warnings,
            :ocr_status, :review_status, :notes, CURRENT_TIMESTAMP
        )
        ON CONFLICT(id) DO UPDATE SET
            source_title = excluded.source_title,
            creator = excluded.creator,
            publication_year = excluded.publication_year,
            file_path = excluded.file_path,
            file_name = excluded.file_name,
            file_hash = excluded.file_hash,
            file_size_bytes = excluded.file_size_bytes,
            file_format = excluded.file_format,
            extraction_method = excluded.extraction_method,
            extraction_timestamp = excluded.extraction_timestamp,
            extraction_status = excluded.extraction_status,
            page_count = excluded.page_count,
            char_count = excluded.char_count,
            word_count = excluded.word_count,
            permission_status = excluded.permission_status,
            verification_status = excluded.verification_status,
            extraction_warnings = excluded.extraction_warnings,
            ocr_status = excluded.ocr_status,
            review_status = excluded.review_status,
            notes = excluded.notes,
            updated_at = CURRENT_TIMESTAMP;
        """
        doc_params = doc.to_dict()
        doc_params["extraction_warnings"] = json.dumps(
            doc.extraction_warnings, ensure_ascii=False
        )

        chunk_sql = """
        INSERT INTO document_chunks (
            id, document_id, source_id, page_number, section_heading,
            chunk_index, text, char_count, word_count, content_hash,
            permission_status, verification_status
        ) VALUES (
            :id, :document_id, :source_id, :page_number, :section_heading,
            :chunk_index, :text, :char_count, :word_count, :content_hash,
            :permission_status, :verification_status
        );
        """

        fts_insert = """
        INSERT INTO document_chunks_fts (
            chunk_id, document_id, source_id, page_number, section_heading, text
        ) VALUES (
            :chunk_id, :document_id, :source_id, :page_number, :section_heading, :text
        );
        """

        with self.db_manager.get_connection() as conn:
            conn.execute(doc_sql, doc_params)

            # Clear old chunks for idempotent re-ingestion
            conn.execute("DELETE FROM document_chunks WHERE document_id = ?;", (doc.id,))
            if self.is_fts5_available(conn):
                try:
                    conn.execute(
                        "DELETE FROM document_chunks_fts WHERE document_id = ?;",
                        (doc.id,),
                    )
                except Exception:
                    pass

            for chunk in chunks:
                conn.execute(chunk_sql, chunk.to_dict())
                # Only index non-restricted chunks into FTS
                if (
                    self.is_fts5_available(conn)
                    and chunk.permission_status != "restricted"
                ):
                    try:
                        conn.execute(
                            fts_insert,
                            {
                                "chunk_id": chunk.id,
                                "document_id": chunk.document_id,
                                "source_id": chunk.source_id,
                                "page_number": chunk.page_number,
                                "section_heading": chunk.section_heading or "",
                                "text": chunk.text,
                            },
                        )
                    except Exception:
                        pass

            conn.commit()

    def get_document(self, doc_id: str) -> IngestedDocument | None:
        """Fetch an ingested document by unique document ID."""
        sql = "SELECT * FROM ingested_documents WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (doc_id,))
            row = cur.fetchone()
            if not row:
                return None
            data = dict(row)
            warns = data.get("extraction_warnings")
            data["extraction_warnings"] = json.loads(warns) if warns else []
            data.pop("created_at", None)
            data.pop("updated_at", None)
            return IngestedDocument.from_dict(data)

    def get_document_by_source_id(self, source_id: str) -> IngestedDocument | None:
        """Fetch an ingested document by source manifest ID."""
        sql = "SELECT * FROM ingested_documents WHERE source_id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            row = cur.fetchone()
            if not row:
                return None
            data = dict(row)
            warns = data.get("extraction_warnings")
            data["extraction_warnings"] = json.loads(warns) if warns else []
            data.pop("created_at", None)
            data.pop("updated_at", None)
            return IngestedDocument.from_dict(data)

    def get_document_by_hash(self, file_hash: str) -> IngestedDocument | None:
        """Fetch an ingested document by file SHA-256 hash."""
        sql = "SELECT * FROM ingested_documents WHERE file_hash = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (file_hash,))
            row = cur.fetchone()
            if not row:
                return None
            data = dict(row)
            warns = data.get("extraction_warnings")
            data["extraction_warnings"] = json.loads(warns) if warns else []
            data.pop("created_at", None)
            data.pop("updated_at", None)
            return IngestedDocument.from_dict(data)

    def list_documents(self) -> list[IngestedDocument]:
        """List all ingested documents."""
        sql = "SELECT * FROM ingested_documents ORDER BY source_id;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql)
            docs: list[IngestedDocument] = []
            for row in cur.fetchall():
                data = dict(row)
                warns = data.get("extraction_warnings")
                data["extraction_warnings"] = json.loads(warns) if warns else []
                data.pop("created_at", None)
                data.pop("updated_at", None)
                docs.append(IngestedDocument.from_dict(data))
            return docs

    def get_chunks(self, doc_id: str) -> list[DocumentChunk]:
        """Fetch all paragraph chunks for a document ordered by chunk index."""
        sql = "SELECT * FROM document_chunks WHERE document_id = ? ORDER BY chunk_index;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (doc_id,))
            chunks: list[DocumentChunk] = []
            for row in cur.fetchall():
                data = dict(row)
                chunks.append(DocumentChunk.from_dict(data))
            return chunks

    def get_chunks_by_source_id(self, source_id: str) -> list[DocumentChunk]:
        """Fetch all paragraph chunks for a source manifest ID."""
        sql = "SELECT * FROM document_chunks WHERE source_id = ? ORDER BY chunk_index;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            chunks: list[DocumentChunk] = []
            for row in cur.fetchall():
                data = dict(row)
                chunks.append(DocumentChunk.from_dict(data))
            return chunks

    def delete_document(self, doc_id: str) -> None:
        """Delete document, its chunks, and corresponding FTS records transactionally."""
        with self.db_manager.get_connection() as conn:
            if self.is_fts5_available(conn):
                try:
                    conn.execute(
                        "DELETE FROM document_chunks_fts WHERE document_id = ?;",
                        (doc_id,),
                    )
                except Exception:
                    pass
            conn.execute("DELETE FROM document_chunks WHERE document_id = ?;", (doc_id,))
            conn.execute("DELETE FROM ingested_documents WHERE id = ?;", (doc_id,))
            conn.commit()

    def rebuild_chunks_fts_index(self) -> int:
        """Safely recreate and rebuild the FTS5 search index for permitted document chunks."""
        with self.db_manager.get_connection() as conn:
            if not self.is_fts5_available(conn):
                return 0

            conn.execute("BEGIN IMMEDIATE;")
            try:
                conn.execute("DELETE FROM document_chunks_fts;")
                insert_sql = """
                INSERT INTO document_chunks_fts (
                    chunk_id, document_id, source_id, page_number, section_heading, text
                )
                SELECT id, document_id, source_id, page_number,
                       COALESCE(section_heading, ''), text
                FROM document_chunks
                WHERE permission_status != 'restricted';
                """
                conn.execute(insert_sql)
                cur = conn.execute("SELECT COUNT(*) FROM document_chunks_fts;")
                count = cur.fetchone()[0]
                conn.commit()
                return int(count)
            except Exception:
                conn.rollback()
                raise

    def search_chunks_fts(
        self,
        query: str,
        limit: int = 20,
    ) -> list[tuple[DocumentChunk, float]]:
        """Search document text chunks using SQLite FTS5 with BM25 ranking."""
        cleaned_query = sanitize_fts_query(query)
        if not cleaned_query:
            return []

        with self.db_manager.get_connection() as conn:
            if not self.is_fts5_available(conn):
                return []

            sql = """
            SELECT dc.id, dc.document_id, dc.source_id, dc.page_number,
                   dc.section_heading, dc.chunk_index, dc.text, dc.char_count,
                   dc.word_count, dc.content_hash, dc.permission_status,
                   dc.verification_status, dc.created_at, fts.rank
            FROM document_chunks_fts fts
            JOIN document_chunks dc ON dc.id = fts.chunk_id
            WHERE document_chunks_fts MATCH ?
              AND dc.permission_status != 'restricted'
            ORDER BY fts.rank ASC
            LIMIT ?;
            """
            try:
                cur = conn.execute(sql, (cleaned_query, limit))
                rows = cur.fetchall()
            except Exception:
                # Fallback quoting query
                escaped = f'"{cleaned_query.replace(chr(34), "")}"'
                try:
                    cur = conn.execute(sql, (escaped, limit))
                    rows = cur.fetchall()
                except Exception:
                    return []

            results: list[tuple[DocumentChunk, float]] = []
            for row in rows:
                data = dict(row)
                rank = float(data.pop("rank", 0.0))
                chunk = DocumentChunk.from_dict(data)
                results.append((chunk, rank))
            return results


@dataclass
class EnrichmentRunRecord:
    """Represents an execution record of the vocabulary enrichment pipeline."""

    id: str
    source_id: str
    file_path: str | None = None
    file_hash: str | None = None
    extraction_method: str = "structured"
    status: str = "completed"
    items_extracted: int = 0
    candidates_created: int = 0
    entries_updated: int = 0
    duplicates_detected: int = 0
    warnings: list[str] = field(default_factory=list)
    error_message: str | None = None
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EnrichmentRunRecord:
        """Create EnrichmentRunRecord from dictionary."""
        d = dict(data)
        if isinstance(d.get("warnings"), str):
            try:
                d["warnings"] = json.loads(d["warnings"])
            except Exception:
                d["warnings"] = []
        valid_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        return cls(**filtered)


class EnrichmentRepository:
    """Repository for tracking vocabulary enrichment executions and idempotency."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def record_run(self, run: EnrichmentRunRecord, conn: Any = None) -> None:
        """Persist or update an enrichment run record."""
        sql = """
        INSERT INTO enrichment_runs (
            id, source_id, file_path, file_hash, extraction_method,
            status, items_extracted, candidates_created, entries_updated,
            duplicates_detected, warnings, error_message
        ) VALUES (
            :id, :source_id, :file_path, :file_hash, :extraction_method,
            :status, :items_extracted, :candidates_created, :entries_updated,
            :duplicates_detected, :warnings, :error_message
        )
        ON CONFLICT(id) DO UPDATE SET
            status = excluded.status,
            items_extracted = excluded.items_extracted,
            candidates_created = excluded.candidates_created,
            entries_updated = excluded.entries_updated,
            duplicates_detected = excluded.duplicates_detected,
            warnings = excluded.warnings,
            error_message = excluded.error_message;
        """
        params = {
            "id": run.id,
            "source_id": run.source_id,
            "file_path": run.file_path,
            "file_hash": run.file_hash,
            "extraction_method": run.extraction_method,
            "status": run.status,
            "items_extracted": run.items_extracted,
            "candidates_created": run.candidates_created,
            "entries_updated": run.entries_updated,
            "duplicates_detected": run.duplicates_detected,
            "warnings": json.dumps(run.warnings, ensure_ascii=False),
            "error_message": run.error_message,
        }
        if conn is not None:
            conn.execute(sql, params)
        else:
            with self.db_manager.get_connection() as c:
                c.execute(sql, params)
                c.commit()

    def get_last_run_for_source(self, source_id: str) -> EnrichmentRunRecord | None:
        """Fetch the most recent enrichment run for a source."""
        sql = (
            "SELECT * FROM enrichment_runs WHERE source_id = ? "
            "ORDER BY created_at DESC LIMIT 1;"
        )
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (source_id,))
            row = cur.fetchone()
            if not row:
                return None
            return EnrichmentRunRecord.from_dict(dict(row))

    def list_runs(self, limit: int = 50) -> list[EnrichmentRunRecord]:
        """List recent enrichment runs."""
        sql = "SELECT * FROM enrichment_runs ORDER BY created_at DESC LIMIT ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (limit,))
            return [EnrichmentRunRecord.from_dict(dict(r)) for r in cur.fetchall()]


# Audio Corpus & Pronunciation Repositories (Step 15)
from tangkhul_lib.audio.repository import (  # noqa: E402
    AudioAnnotationRepository,
    AudioConsentRepository,
    AudioRecordingRepository,
    PronunciationRepository,
)

__all__ = [
    "AudioAnnotationRepository",
    "AudioConsentRepository",
    "AudioRecordingRepository",
    "PronunciationRepository",
]


