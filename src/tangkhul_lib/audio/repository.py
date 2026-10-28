"""Repository interfaces for Tangkhul audio corpus and pronunciation records."""

from __future__ import annotations

import json
import sqlite3
from typing import TYPE_CHECKING, Any

from tangkhul_lib.audio.models import (
    AudioAnnotation,
    AudioConsentRecord,
    AudioRecording,
    PronunciationRecord,
)

if TYPE_CHECKING:
    from tangkhul_lib.storage.database import DatabaseManager


class AudioRecordingRepository:
    """Repository interface for persisting, searching, and managing audio recordings."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, recording: AudioRecording) -> None:
        """Persist or update an audio recording in the database."""
        sql = """
        INSERT INTO audio_recordings (
            id, title, vocab_entry_id, corpus_id, description,
            recording_date, speaker_pseudonym, dialect, village, region,
            language, variety, recording_method, recording_source,
            file_path, original_filename, file_format, duration_seconds,
            sample_rate, channels, file_size_bytes, checksum_sha256,
            transcription, transcription_normalized, ipa_transcription, transliteration,
            source_title, source_citation, source_url, license,
            copyright_status, consent_status, permitted_uses, access_restrictions,
            is_withdrawn, withdrawal_date, withdrawal_reason,
            verification_status, notes, segments, created_at, updated_at
        ) VALUES (
            :id, :title, :vocab_entry_id, :corpus_id, :description,
            :recording_date, :speaker_pseudonym, :dialect, :village, :region,
            :language, :variety, :recording_method, :recording_source,
            :file_path, :original_filename, :file_format, :duration_seconds,
            :sample_rate, :channels, :file_size_bytes, :checksum_sha256,
            :transcription, :transcription_normalized, :ipa_transcription, :transliteration,
            :source_title, :source_citation, :source_url, :license,
            :copyright_status, :consent_status, :permitted_uses, :access_restrictions,
            :is_withdrawn, :withdrawal_date, :withdrawal_reason,
            :verification_status, :notes, :segments, :created_at, :updated_at
        )
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            vocab_entry_id = excluded.vocab_entry_id,
            corpus_id = excluded.corpus_id,
            description = excluded.description,
            recording_date = excluded.recording_date,
            speaker_pseudonym = excluded.speaker_pseudonym,
            dialect = excluded.dialect,
            village = excluded.village,
            region = excluded.region,
            language = excluded.language,
            variety = excluded.variety,
            recording_method = excluded.recording_method,
            recording_source = excluded.recording_source,
            file_path = excluded.file_path,
            original_filename = excluded.original_filename,
            file_format = excluded.file_format,
            duration_seconds = excluded.duration_seconds,
            sample_rate = excluded.sample_rate,
            channels = excluded.channels,
            file_size_bytes = excluded.file_size_bytes,
            checksum_sha256 = excluded.checksum_sha256,
            transcription = excluded.transcription,
            transcription_normalized = excluded.transcription_normalized,
            ipa_transcription = excluded.ipa_transcription,
            transliteration = excluded.transliteration,
            source_title = excluded.source_title,
            source_citation = excluded.source_citation,
            source_url = excluded.source_url,
            license = excluded.license,
            copyright_status = excluded.copyright_status,
            consent_status = excluded.consent_status,
            permitted_uses = excluded.permitted_uses,
            access_restrictions = excluded.access_restrictions,
            is_withdrawn = excluded.is_withdrawn,
            withdrawal_date = excluded.withdrawal_date,
            withdrawal_reason = excluded.withdrawal_reason,
            verification_status = excluded.verification_status,
            notes = excluded.notes,
            segments = excluded.segments,
            updated_at = excluded.updated_at;
        """
        params = {
            "id": recording.id,
            "title": recording.title,
            "vocab_entry_id": recording.vocab_entry_id,
            "corpus_id": recording.corpus_id,
            "description": recording.description,
            "recording_date": recording.recording_date,
            "speaker_pseudonym": recording.speaker_pseudonym,
            "dialect": recording.dialect,
            "village": recording.village,
            "region": recording.region,
            "language": recording.language,
            "variety": recording.variety,
            "recording_method": recording.recording_method,
            "recording_source": recording.recording_source,
            "file_path": recording.file_path,
            "original_filename": recording.original_filename,
            "file_format": recording.file_format,
            "duration_seconds": recording.duration_seconds,
            "sample_rate": recording.sample_rate,
            "channels": recording.channels,
            "file_size_bytes": recording.file_size_bytes,
            "checksum_sha256": recording.checksum_sha256,
            "transcription": recording.transcription,
            "transcription_normalized": recording.transcription_normalized,
            "ipa_transcription": recording.ipa_transcription,
            "transliteration": recording.transliteration,
            "source_title": recording.source_title,
            "source_citation": recording.source_citation,
            "source_url": recording.source_url,
            "license": recording.license,
            "copyright_status": recording.copyright_status,
            "consent_status": recording.consent_status,
            "permitted_uses": json.dumps(recording.permitted_uses, ensure_ascii=False),
            "access_restrictions": recording.access_restrictions,
            "is_withdrawn": 1 if recording.is_withdrawn else 0,
            "withdrawal_date": recording.withdrawal_date,
            "withdrawal_reason": recording.withdrawal_reason,
            "verification_status": recording.verification_status,
            "notes": recording.notes,
            "segments": json.dumps([s.to_dict() for s in recording.segments], ensure_ascii=False),
            "created_at": recording.created_at,
            "updated_at": recording.updated_at,
        }
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, params)
            self._index_fts(recording, conn)
            conn.commit()

    def _index_fts(self, recording: AudioRecording, conn: sqlite3.Connection) -> None:
        """Update FTS5 index for audio recording if available and not withdrawn."""
        try:
            conn.execute(
                "DELETE FROM audio_recordings_fts WHERE recording_id = ?;",
                (recording.id,),
            )
            if not recording.is_withdrawn and recording.consent_status == "authorized":
                conn.execute(
                    """
                    INSERT INTO audio_recordings_fts (
                        recording_id, title, transcription, transcription_normalized,
                        ipa_transcription, dialect, village, speaker_pseudonym
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        recording.id,
                        recording.title or "",
                        recording.transcription or "",
                        recording.transcription_normalized or "",
                        recording.ipa_transcription or "",
                        recording.dialect or "",
                        recording.village or "",
                        recording.speaker_pseudonym or "",
                    ),
                )
        except Exception:
            # FTS table may not be initialized or available
            pass

    def get_by_id(self, recording_id: str) -> AudioRecording | None:
        """Fetch an audio recording by its unique ID."""
        sql = "SELECT * FROM audio_recordings WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (recording_id,))
            row = cur.fetchone()
            if not row:
                return None
            return AudioRecording.from_dict(dict(row))

    def get_by_hash(self, checksum_sha256: str) -> AudioRecording | None:
        """Fetch an audio recording by its SHA-256 checksum."""
        if not checksum_sha256:
            return None
        sql = "SELECT * FROM audio_recordings WHERE checksum_sha256 = ? LIMIT 1;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (checksum_sha256,))
            row = cur.fetchone()
            if not row:
                return None
            return AudioRecording.from_dict(dict(row))

    def list_recordings(
        self,
        vocab_entry_id: str | None = None,
        dialect: str | None = None,
        village: str | None = None,
        consent_status: str | None = None,
        is_withdrawn: bool | None = None,
        verification_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[AudioRecording]:
        """List recordings with deterministic filtering."""
        clauses = []
        params: list[Any] = []

        if vocab_entry_id is not None:
            clauses.append("vocab_entry_id = ?")
            params.append(vocab_entry_id)
        if dialect is not None:
            clauses.append("dialect = ?")
            params.append(dialect)
        if village is not None:
            clauses.append("village = ?")
            params.append(village)
        if consent_status is not None:
            clauses.append("consent_status = ?")
            params.append(consent_status)
        if is_withdrawn is not None:
            clauses.append("is_withdrawn = ?")
            params.append(1 if is_withdrawn else 0)
        if verification_status is not None:
            clauses.append("verification_status = ?")
            params.append(verification_status)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
        SELECT * FROM audio_recordings
        {where_sql}
        ORDER BY id ASC
        LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])

        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            return [AudioRecording.from_dict(dict(r)) for r in cur.fetchall()]

    def search(
        self,
        query: str,
        dialect: str | None = None,
        include_withdrawn: bool = False,
        limit: int = 50,
    ) -> list[AudioRecording]:
        """Search recordings by title, transcription, IPA, or speaker pseudonym."""
        clean_q = query.strip()
        if not clean_q:
            return self.list_recordings(dialect=dialect, limit=limit)

        results: list[AudioRecording] = []
        with self.db_manager.get_connection() as conn:
            # Try FTS search first
            fts_worked = False
            try:
                fts_sql = """
                SELECT r.* FROM audio_recordings r
                JOIN audio_recordings_fts f ON r.id = f.recording_id
                WHERE audio_recordings_fts MATCH ?
                """
                fts_params: list[Any] = [f'"{clean_q}"*']
                if not include_withdrawn:
                    fts_sql += " AND r.is_withdrawn = 0"
                if dialect:
                    fts_sql += " AND r.dialect = ?"
                    fts_params.append(dialect)
                fts_sql += " ORDER BY r.id ASC LIMIT ?;"
                fts_params.append(limit)

                cur = conn.execute(fts_sql, fts_params)
                rows = cur.fetchall()
                if rows:
                    results = [AudioRecording.from_dict(dict(r)) for r in rows]
                    fts_worked = True
            except Exception:
                fts_worked = False

            if not fts_worked:
                like_pat = f"%{clean_q}%"
                like_sql = """
                SELECT * FROM audio_recordings
                WHERE (
                    title LIKE ? OR
                    transcription LIKE ? OR
                    transcription_normalized LIKE ? OR
                    ipa_transcription LIKE ? OR
                    speaker_pseudonym LIKE ? OR
                    village LIKE ?
                )
                """
                like_params: list[Any] = [like_pat] * 6
                if not include_withdrawn:
                    like_sql += " AND is_withdrawn = 0"
                if dialect:
                    like_sql += " AND dialect = ?"
                    like_params.append(dialect)
                like_sql += " ORDER BY id ASC LIMIT ?;"
                like_params.append(limit)

                cur = conn.execute(like_sql, like_params)
                results = [AudioRecording.from_dict(dict(r)) for r in cur.fetchall()]

        return results

    def count(
        self,
        consent_status: str | None = None,
        is_withdrawn: bool | None = None,
    ) -> int:
        """Count recordings matching filters."""
        clauses = []
        params: list[Any] = []
        if consent_status:
            clauses.append("consent_status = ?")
            params.append(consent_status)
        if is_withdrawn is not None:
            clauses.append("is_withdrawn = ?")
            params.append(1 if is_withdrawn else 0)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT COUNT(*) FROM audio_recordings {where_sql};"

        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            return cur.fetchone()[0]

    def delete(self, recording_id: str) -> bool:
        """Delete an audio recording and remove from FTS."""
        with self.db_manager.get_connection() as conn:
            cur = conn.execute("DELETE FROM audio_recordings WHERE id = ?;", (recording_id,))
            try:
                conn.execute(
                    "DELETE FROM audio_recordings_fts WHERE recording_id = ?;",
                    (recording_id,),
                )
            except Exception:
                pass
            conn.commit()
            return cur.rowcount > 0


class PronunciationRepository:
    """Repository interface for vocabulary pronunciation records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, pron: PronunciationRecord) -> None:
        """Persist or update a pronunciation record."""
        sql = """
        INSERT OR REPLACE INTO pronunciation_records (
            id, vocab_entry_id, headword, recording_id,
            pronunciation_ipa, pronunciation_phonetic, dialect, village,
            speaker_pseudonym, is_primary, source_citation,
            verification_status, review_status, review_notes,
            reviewer, reviewed_at, created_at
        ) VALUES (
            :id, :vocab_entry_id, :headword, :recording_id,
            :pronunciation_ipa, :pronunciation_phonetic, :dialect, :village,
            :speaker_pseudonym, :is_primary, :source_citation,
            :verification_status, :review_status, :review_notes,
            :reviewer, :reviewed_at, :created_at
        );
        """
        params = {
            "id": pron.id,
            "vocab_entry_id": pron.vocab_entry_id,
            "headword": pron.headword,
            "recording_id": pron.recording_id,
            "pronunciation_ipa": pron.pronunciation_ipa,
            "pronunciation_phonetic": pron.pronunciation_phonetic,
            "dialect": pron.dialect,
            "village": pron.village,
            "speaker_pseudonym": pron.speaker_pseudonym,
            "is_primary": 1 if pron.is_primary else 0,
            "source_citation": pron.source_citation,
            "verification_status": pron.verification_status,
            "review_status": pron.review_status,
            "review_notes": pron.review_notes,
            "reviewer": pron.reviewer,
            "reviewed_at": pron.reviewed_at,
            "created_at": pron.created_at,
        }
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def get_by_id(self, pron_id: str) -> PronunciationRecord | None:
        """Fetch pronunciation record by ID."""
        sql = "SELECT * FROM pronunciation_records WHERE id = ?;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (pron_id,))
            row = cur.fetchone()
            if not row:
                return None
            return PronunciationRecord.from_dict(dict(row))

    def get_by_vocab_id(self, vocab_entry_id: str) -> list[PronunciationRecord]:
        """Fetch all pronunciation records linked to a vocabulary entry."""
        sql = (
            "SELECT * FROM pronunciation_records WHERE vocab_entry_id = ? "
            "ORDER BY is_primary DESC, id ASC;"
        )
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (vocab_entry_id,))
            return [PronunciationRecord.from_dict(dict(r)) for r in cur.fetchall()]

    def get_by_recording_id(self, recording_id: str) -> list[PronunciationRecord]:
        """Fetch all pronunciation records linked to an audio recording."""
        sql = "SELECT * FROM pronunciation_records WHERE recording_id = ? ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (recording_id,))
            return [PronunciationRecord.from_dict(dict(r)) for r in cur.fetchall()]

    def list_all(
        self,
        dialect: str | None = None,
        review_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[PronunciationRecord]:
        """List pronunciation records with optional filters."""
        clauses = []
        params: list[Any] = []
        if dialect:
            clauses.append("dialect = ?")
            params.append(dialect)
        if review_status:
            clauses.append("review_status = ?")
            params.append(review_status)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT * FROM pronunciation_records {where_sql} ORDER BY id ASC LIMIT ? OFFSET ?;"
        params.extend([limit, offset])

        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            return [PronunciationRecord.from_dict(dict(r)) for r in cur.fetchall()]

    def count(self) -> int:
        """Count total pronunciation records."""
        with self.db_manager.get_connection() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM pronunciation_records;")
            return cur.fetchone()[0]


class AudioAnnotationRepository:
    """Repository interface for timestamped audio annotations."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def add(self, annotation: AudioAnnotation) -> None:
        """Persist or update an audio annotation."""
        sql = """
        INSERT OR REPLACE INTO audio_annotations (
            id, recording_id, annotation_type, start_time_seconds,
            end_time_seconds, text_verbatim, text_normalized, ipa,
            annotator_pseudonym, confidence_score, verification_status,
            notes, created_at
        ) VALUES (
            :id, :recording_id, :annotation_type, :start_time_seconds,
            :end_time_seconds, :text_verbatim, :text_normalized, :ipa,
            :annotator_pseudonym, :confidence_score, :verification_status,
            :notes, :created_at
        );
        """
        params = annotation.to_dict()
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def get_by_recording_id(self, recording_id: str) -> list[AudioAnnotation]:
        """Fetch all annotations for a recording ordered by start time."""
        sql = (
            "SELECT * FROM audio_annotations WHERE recording_id = ? "
            "ORDER BY start_time_seconds ASC, id ASC;"
        )
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (recording_id,))
            return [AudioAnnotation.from_dict(dict(r)) for r in cur.fetchall()]

    def delete_by_recording_id(self, recording_id: str) -> None:
        """Delete all annotations for a recording."""
        sql = "DELETE FROM audio_annotations WHERE recording_id = ?;"
        with self.db_manager.get_connection() as conn:
            conn.execute(sql, (recording_id,))
            conn.commit()


class AudioConsentRepository:
    """Repository interface for immutable consent audit records."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def record_event(self, event: AudioConsentRecord) -> int:
        """Record an immutable consent event."""
        sql = """
        INSERT INTO audio_consent_records (
            recording_id, speaker_pseudonym, consent_status,
            permitted_uses, restrictions, recorded_date,
            withdrawn_date, withdrawn_reason, authorized_by, timestamp
        ) VALUES (
            :recording_id, :speaker_pseudonym, :consent_status,
            :permitted_uses, :restrictions, :recorded_date,
            :withdrawn_date, :withdrawn_reason, :authorized_by, :timestamp
        );
        """
        params = {
            "recording_id": event.recording_id,
            "speaker_pseudonym": event.speaker_pseudonym,
            "consent_status": event.consent_status,
            "permitted_uses": json.dumps(event.permitted_uses, ensure_ascii=False),
            "restrictions": event.restrictions,
            "recorded_date": event.recorded_date,
            "withdrawn_date": event.withdrawn_date,
            "withdrawn_reason": event.withdrawn_reason,
            "authorized_by": event.authorized_by,
            "timestamp": event.timestamp,
        }
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid

    def get_history(self, recording_id: str) -> list[AudioConsentRecord]:
        """Fetch complete chronological consent audit history for a recording."""
        sql = "SELECT * FROM audio_consent_records WHERE recording_id = ? ORDER BY id ASC;"
        with self.db_manager.get_connection() as conn:
            cur = conn.execute(sql, (recording_id,))
            return [AudioConsentRecord.from_dict(dict(r)) for r in cur.fetchall()]

    def get_by_recording_id(self, recording_id: str) -> list[AudioConsentRecord]:
        """Alias for get_history to fetch consent records by recording ID."""
        return self.get_history(recording_id)
