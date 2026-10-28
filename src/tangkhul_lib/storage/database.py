"""Database connectivity and schema initialization interfaces.

Storage Backend:
    SQLite database storing unified vocabulary, source provenance, manifest catalogues,
    and domain-specific tables (books, etc.).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS manifest_records (
    id TEXT PRIMARY KEY,
    resource_type TEXT NOT NULL,
    title TEXT NOT NULL,
    title_translation TEXT,
    creator TEXT,
    year INTEGER,
    publisher TEXT,
    language TEXT DEFAULT 'Tangkhul',
    dialect TEXT,
    source_url TEXT,
    source_identifier TEXT,
    license TEXT,
    permission_status TEXT DEFAULT 'pending',
    local_path TEXT,
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    alternate_titles TEXT,
    authors TEXT,
    editors TEXT,
    publisher TEXT,
    publication_year INTEGER,
    edition TEXT,
    subject TEXT,
    educational_level TEXT,
    language TEXT DEFAULT 'Tangkhul',
    dialect TEXT,
    isbn TEXT,
    source_url TEXT,
    source_identifier TEXT,
    catalogue_url TEXT,
    local_file_path TEXT,
    file_format TEXT,
    license TEXT,
    permission_status TEXT DEFAULT 'pending',
    access_status TEXT DEFAULT 'metadata_only',
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS songs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    alternate_titles TEXT,
    title_translation TEXT,
    singer TEXT,
    lyricist TEXT,
    composer TEXT,
    collector TEXT,
    performers TEXT,
    year INTEGER,
    village TEXT,
    dialect TEXT,
    song_type TEXT,
    language TEXT DEFAULT 'Tangkhul',
    source_url TEXT,
    source_identifier TEXT,
    recording_url TEXT,
    lyrics_source_url TEXT,
    local_file_path TEXT,
    license TEXT,
    permission_status TEXT DEFAULT 'pending',
    access_status TEXT DEFAULT 'metadata_only',
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dictionary_id) REFERENCES dictionaries(id) ON DELETE CASCADE,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary_entries(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS vocabulary_entries (
    id TEXT PRIMARY KEY,
    headword TEXT NOT NULL,
    meanings TEXT,
    translations_en TEXT,
    alternative_spellings TEXT,
    dialect_variants TEXT,
    dialect TEXT,
    part_of_speech TEXT,
    pronunciation TEXT,
    example_sentences TEXT,
    verification_status TEXT DEFAULT 'unverified',
    license_restrictions TEXT,
    review_status TEXT DEFAULT 'pending_review',
    review_notes TEXT,
    reviewer TEXT,
    reviewed_at TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS provenance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vocabulary_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    citation TEXT NOT NULL,
    page_or_section TEXT,
    context_sentence TEXT,
    recorded_year INTEGER,
    permission_status TEXT DEFAULT 'pending',
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary_entries(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS extracted_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    word_form TEXT NOT NULL,
    page_or_section TEXT,
    context_sentence TEXT,
    extraction_method TEXT,
    verification_status TEXT DEFAULT 'unverified',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS culture (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    local_name TEXT,
    alternate_names TEXT,
    category TEXT NOT NULL,
    subcategory TEXT,
    original_text TEXT,
    translation_en TEXT,
    translations_other TEXT,
    description TEXT,
    cultural_significance TEXT,
    season_or_timing TEXT,
    village TEXT,
    dialect TEXT,
    language TEXT DEFAULT 'Tangkhul',
    participants TEXT,
    procedure TEXT,
    related_records TEXT,
    historical_period TEXT,
    year INTEGER,
    source_id TEXT,
    source_title TEXT,
    source_page TEXT,
    source_section TEXT,
    source_url TEXT,
    contributor TEXT,
    contributor_consent INTEGER DEFAULT 1,
    license TEXT,
    permission_status TEXT DEFAULT 'pending',
    access_status TEXT DEFAULT 'metadata_only',
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS history (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    record_type TEXT NOT NULL,
    alternate_titles TEXT,
    summary TEXT,
    description TEXT,
    original_text TEXT,
    translation_en TEXT,
    event_date TEXT,
    sort_year INTEGER,
    period TEXT,
    place TEXT,
    village TEXT,
    dialect TEXT,
    language TEXT DEFAULT 'Tangkhul',
    people_involved TEXT,
    related_events TEXT,
    related_records TEXT,
    source_id TEXT,
    source_title TEXT,
    source_page TEXT,
    source_section TEXT,
    source_url TEXT,
    contributor TEXT,
    contributor_consent INTEGER DEFAULT 1,
    evidence_type TEXT DEFAULT 'scholarly_interpretation',
    confidence REAL DEFAULT 1.0,
    contradictory_accounts TEXT,
    license TEXT,
    permission_status TEXT DEFAULT 'pending',
    access_status TEXT DEFAULT 'metadata_only',
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS literature (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    work_type TEXT NOT NULL,
    alternate_titles TEXT,
    original_title TEXT,
    title_translation TEXT,
    genres TEXT,
    author TEXT,
    poet TEXT,
    storyteller TEXT,
    playwright TEXT,
    translator TEXT,
    editor TEXT,
    collector TEXT,
    contributor TEXT,
    contributor_consent INTEGER DEFAULT 1,
    publication_year INTEGER,
    composition_date TEXT,
    edition TEXT,
    publisher TEXT,
    publication_place TEXT,
    language TEXT DEFAULT 'Tangkhul',
    dialect TEXT,
    village TEXT,
    region TEXT,
    collection TEXT,
    anthology TEXT,
    parent_work_id TEXT,
    book_id TEXT,
    isbn TEXT,
    identifier TEXT,
    source_url TEXT,
    source_id TEXT,
    source_title TEXT,
    source_page TEXT,
    source_section TEXT,
    local_path TEXT,
    license TEXT,
    license_evidence TEXT,
    permission_status TEXT DEFAULT 'pending',
    access_status TEXT DEFAULT 'metadata_only',
    verification_status TEXT DEFAULT 'unverified',
    text_availability TEXT DEFAULT 'metadata_only',
    original_text TEXT,
    translation_text TEXT,
    summary TEXT,
    stanza_count INTEGER,
    line_count INTEGER,
    related_authors TEXT,
    related_works TEXT,
    related_records TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_year ON books(publication_year);
CREATE INDEX IF NOT EXISTS idx_songs_title ON songs(title);
CREATE INDEX IF NOT EXISTS idx_songs_singer ON songs(singer);
CREATE INDEX IF NOT EXISTS idx_songs_type ON songs(song_type);
CREATE INDEX IF NOT EXISTS idx_songs_village ON songs(village);
CREATE INDEX IF NOT EXISTS idx_dict_title ON dictionaries(title);
CREATE INDEX IF NOT EXISTS idx_dict_year ON dictionaries(publication_year);
CREATE INDEX IF NOT EXISTS idx_dict_type ON dictionaries(source_type);
CREATE INDEX IF NOT EXISTS idx_dict_lang_pair ON dictionaries(language_pair);
CREATE INDEX IF NOT EXISTS idx_dict_entries_headword ON dictionary_entries(headword);
CREATE INDEX IF NOT EXISTS idx_dict_entries_norm ON dictionary_entries(normalized_headword);
CREATE INDEX IF NOT EXISTS idx_dict_entries_dict ON dictionary_entries(dictionary_id);
CREATE INDEX IF NOT EXISTS idx_dict_entries_pos ON dictionary_entries(part_of_speech);
CREATE INDEX IF NOT EXISTS idx_dict_entries_vocab ON dictionary_entries(vocabulary_id);
CREATE INDEX IF NOT EXISTS idx_culture_title ON culture(title);
CREATE INDEX IF NOT EXISTS idx_culture_cat ON culture(category);
CREATE INDEX IF NOT EXISTS idx_culture_village ON culture(village);
CREATE INDEX IF NOT EXISTS idx_culture_dialect ON culture(dialect);
CREATE INDEX IF NOT EXISTS idx_culture_verif ON culture(verification_status);
CREATE INDEX IF NOT EXISTS idx_history_title ON history(title);
CREATE INDEX IF NOT EXISTS idx_history_type ON history(record_type);
CREATE INDEX IF NOT EXISTS idx_history_period ON history(period);
CREATE INDEX IF NOT EXISTS idx_history_place ON history(place);
CREATE INDEX IF NOT EXISTS idx_history_year ON history(sort_year);
CREATE INDEX IF NOT EXISTS idx_history_verif ON history(verification_status);
CREATE INDEX IF NOT EXISTS idx_lit_title ON literature(title);
CREATE INDEX IF NOT EXISTS idx_lit_type ON literature(work_type);
CREATE INDEX IF NOT EXISTS idx_lit_author ON literature(author);
CREATE INDEX IF NOT EXISTS idx_lit_year ON literature(publication_year);
CREATE INDEX IF NOT EXISTS idx_lit_book ON literature(book_id);
CREATE INDEX IF NOT EXISTS idx_lit_verif ON literature(verification_status);
CREATE INDEX IF NOT EXISTS idx_vocab_headword ON vocabulary_entries(headword);
CREATE INDEX IF NOT EXISTS idx_provenance_source ON provenance_records(source_id);
CREATE INDEX IF NOT EXISTS idx_tokens_word ON extracted_tokens(word_form);

CREATE TABLE IF NOT EXISTS ingested_documents (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    source_title TEXT NOT NULL,
    creator TEXT,
    publication_year INTEGER,
    source_type TEXT NOT NULL,
    language TEXT DEFAULT 'Tangkhul',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    file_size_bytes INTEGER DEFAULT 0,
    file_format TEXT NOT NULL,
    extraction_method TEXT NOT NULL,
    extraction_timestamp TEXT NOT NULL,
    extraction_status TEXT DEFAULT 'extracted',
    page_count INTEGER DEFAULT 0,
    char_count INTEGER DEFAULT 0,
    word_count INTEGER DEFAULT 0,
    permission_status TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    extraction_warnings TEXT,
    ocr_status TEXT DEFAULT 'not_required',
    review_status TEXT DEFAULT 'pending_review',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    page_number INTEGER,
    section_heading TEXT,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    char_count INTEGER DEFAULT 0,
    word_count INTEGER DEFAULT 0,
    content_hash TEXT NOT NULL,
    permission_status TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES ingested_documents(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ingested_docs_source ON ingested_documents(source_id);
CREATE INDEX IF NOT EXISTS idx_ingested_docs_hash ON ingested_documents(file_hash);
CREATE INDEX IF NOT EXISTS idx_doc_chunks_doc ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_doc_chunks_source ON document_chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_doc_chunks_page ON document_chunks(page_number);

CREATE TABLE IF NOT EXISTS vocabulary_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    headword TEXT NOT NULL,
    decision TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    previous_state TEXT,
    new_state TEXT,
    suggested_meaning TEXT,
    suggested_pos TEXT,
    suggested_dialect TEXT,
    target_duplicate_id TEXT,
    spelling_assessment TEXT,
    meaning_assessment TEXT,
    pos_assessment TEXT,
    dialect_assessment TEXT,
    example_assessment TEXT,
    source_assessment TEXT,
    correction_proposals TEXT,
    counts_for_consensus INTEGER DEFAULT 1,
    superseded_by_id INTEGER,
    FOREIGN KEY (entry_id) REFERENCES vocabulary_entries(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_vocab_reviews_entry ON vocabulary_reviews(entry_id);
CREATE INDEX IF NOT EXISTS idx_vocab_reviews_decision ON vocabulary_reviews(decision);
CREATE INDEX IF NOT EXISTS idx_vocab_reviews_reviewer ON vocabulary_reviews(reviewer);
CREATE INDEX IF NOT EXISTS idx_vocab_review_status ON vocabulary_entries(review_status);

CREATE TABLE IF NOT EXISTS review_tasks (
    id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    headword TEXT NOT NULL,
    task_type TEXT NOT NULL,
    review_dimensions TEXT NOT NULL,
    source_id TEXT,
    priority TEXT NOT NULL DEFAULT 'medium',
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    assigned_reviewer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    unresolved_disagreements TEXT,
    consensus_outcome TEXT,
    FOREIGN KEY (entry_id) REFERENCES vocabulary_entries(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_review_tasks_entry ON review_tasks(entry_id);
CREATE INDEX IF NOT EXISTS idx_review_tasks_status ON review_tasks(status);
CREATE INDEX IF NOT EXISTS idx_review_tasks_priority ON review_tasks(priority);

CREATE TABLE IF NOT EXISTS review_consensus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    threshold_required INTEGER NOT NULL,
    eligible_reviewers_count INTEGER NOT NULL,
    approvals_count INTEGER NOT NULL,
    rejections_count INTEGER NOT NULL,
    conflicts_count INTEGER NOT NULL,
    corrections_count INTEGER NOT NULL,
    decision_outcome TEXT NOT NULL,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES vocabulary_entries(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_review_consensus_entry ON review_consensus(entry_id);

CREATE TABLE IF NOT EXISTS enrichment_runs (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    file_path TEXT,
    file_hash TEXT,
    extraction_method TEXT,
    status TEXT DEFAULT 'completed',
    items_extracted INTEGER DEFAULT 0,
    candidates_created INTEGER DEFAULT 0,
    entries_updated INTEGER DEFAULT 0,
    duplicates_detected INTEGER DEFAULT 0,
    warnings TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_enrichment_runs_source ON enrichment_runs(source_id);

CREATE TABLE IF NOT EXISTS audio_recordings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    vocab_entry_id TEXT,
    corpus_id TEXT,
    description TEXT,
    recording_date TEXT,
    speaker_pseudonym TEXT,
    dialect TEXT,
    village TEXT,
    region TEXT,
    language TEXT DEFAULT 'Tangkhul',
    variety TEXT,
    recording_method TEXT DEFAULT 'field_recording',
    recording_source TEXT,
    file_path TEXT,
    original_filename TEXT,
    file_format TEXT DEFAULT 'wav',
    duration_seconds REAL DEFAULT 0.0,
    sample_rate INTEGER DEFAULT 0,
    channels INTEGER DEFAULT 1,
    file_size_bytes INTEGER DEFAULT 0,
    checksum_sha256 TEXT,
    transcription TEXT,
    transcription_normalized TEXT,
    ipa_transcription TEXT,
    transliteration TEXT,
    source_title TEXT,
    source_citation TEXT,
    source_url TEXT,
    license TEXT,
    copyright_status TEXT DEFAULT 'copyright_retained',
    consent_status TEXT DEFAULT 'pending',
    permitted_uses TEXT,
    access_restrictions TEXT,
    is_withdrawn INTEGER DEFAULT 0,
    withdrawal_date TEXT,
    withdrawal_reason TEXT,
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    segments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vocab_entry_id) REFERENCES vocabulary_entries(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audio_rec_vocab ON audio_recordings(vocab_entry_id);
CREATE INDEX IF NOT EXISTS idx_audio_rec_hash ON audio_recordings(checksum_sha256);
CREATE INDEX IF NOT EXISTS idx_audio_rec_consent ON audio_recordings(consent_status);
CREATE INDEX IF NOT EXISTS idx_audio_rec_dialect ON audio_recordings(dialect);
CREATE INDEX IF NOT EXISTS idx_audio_rec_withdrawn ON audio_recordings(is_withdrawn);

CREATE TABLE IF NOT EXISTS pronunciation_records (
    id TEXT PRIMARY KEY,
    vocab_entry_id TEXT NOT NULL,
    headword TEXT NOT NULL,
    recording_id TEXT,
    pronunciation_ipa TEXT,
    pronunciation_phonetic TEXT,
    dialect TEXT,
    village TEXT,
    speaker_pseudonym TEXT,
    is_primary INTEGER DEFAULT 0,
    source_citation TEXT,
    verification_status TEXT DEFAULT 'unverified',
    review_status TEXT DEFAULT 'pending_review',
    review_notes TEXT,
    reviewer TEXT,
    reviewed_at TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vocab_entry_id) REFERENCES vocabulary_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (recording_id) REFERENCES audio_recordings(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_pronunciation_vocab ON pronunciation_records(vocab_entry_id);
CREATE INDEX IF NOT EXISTS idx_pronunciation_rec ON pronunciation_records(recording_id);
CREATE INDEX IF NOT EXISTS idx_pronunciation_dialect ON pronunciation_records(dialect);
CREATE INDEX IF NOT EXISTS idx_pronunciation_status ON pronunciation_records(review_status);

CREATE TABLE IF NOT EXISTS audio_annotations (
    id TEXT PRIMARY KEY,
    recording_id TEXT NOT NULL,
    annotation_type TEXT DEFAULT 'segment',
    start_time_seconds REAL DEFAULT 0.0,
    end_time_seconds REAL DEFAULT 0.0,
    text_verbatim TEXT NOT NULL,
    text_normalized TEXT,
    ipa TEXT,
    annotator_pseudonym TEXT,
    confidence_score REAL,
    verification_status TEXT DEFAULT 'unverified',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES audio_recordings(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_audio_anno_rec ON audio_annotations(recording_id);

CREATE TABLE IF NOT EXISTS audio_consent_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recording_id TEXT NOT NULL,
    speaker_pseudonym TEXT NOT NULL,
    consent_status TEXT NOT NULL,
    permitted_uses TEXT,
    restrictions TEXT,
    recorded_date TEXT,
    withdrawn_date TEXT,
    withdrawn_reason TEXT,
    authorized_by TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES audio_recordings(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_audio_consent_rec ON audio_consent_records(recording_id);
"""

FTS_SCHEMA_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS vocabulary_fts USING fts5(
    entry_id UNINDEXED,
    headword,
    alternative_spellings,
    meanings,
    translations_en,
    example_sentences,
    dialect,
    part_of_speech,
    tokenize = 'unicode61'
);

CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts USING fts5(
    chunk_id UNINDEXED,
    document_id UNINDEXED,
    source_id UNINDEXED,
    page_number UNINDEXED,
    section_heading,
    text,
    tokenize = 'unicode61'
);

CREATE VIRTUAL TABLE IF NOT EXISTS audio_recordings_fts USING fts5(
    recording_id UNINDEXED,
    title,
    transcription,
    transcription_normalized,
    ipa_transcription,
    dialect,
    village,
    speaker_pseudonym,
    tokenize = 'unicode61'
);
"""


def is_fts5_available(conn: sqlite3.Connection | None = None) -> bool:
    """Check if SQLite FTS5 extension is available."""
    close_after = False
    if conn is None:
        conn = sqlite3.connect(":memory:")
        close_after = True
    try:
        cur = conn.cursor()
        cur.execute("CREATE VIRTUAL TABLE temp._fts5_check USING fts5(x);")
        cur.execute("DROP TABLE temp._fts5_check;")
        return True
    except Exception:
        return False
    finally:
        if close_after:
            conn.close()


class DatabaseManager:
    """Manages SQLite connections for Tangkhul corpus and vocabulary data."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path) if not isinstance(db_path, Path) else db_path
        self._mem_conn: sqlite3.Connection | None = None
        if str(self.db_path) == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:")
            self._mem_conn.row_factory = sqlite3.Row
            self._mem_conn.execute("PRAGMA foreign_keys = ON;")

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a configured SQLite connection."""
        if self._mem_conn is not None:
            return self._mem_conn
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _migrate_schema(self, conn: sqlite3.Connection) -> None:
        """Apply safe idempotent column additions to existing tables."""
        try:
            cur = conn.execute("PRAGMA table_info(vocabulary_entries);")
            cols = {row["name"] for row in cur.fetchall()}
            if "review_status" not in cols:
                conn.execute(
                    "ALTER TABLE vocabulary_entries ADD COLUMN "
                    "review_status TEXT DEFAULT 'pending_review';"
                )
            if "review_notes" not in cols:
                conn.execute(
                    "ALTER TABLE vocabulary_entries ADD COLUMN review_notes TEXT;"
                )
            if "reviewer" not in cols:
                conn.execute(
                    "ALTER TABLE vocabulary_entries ADD COLUMN reviewer TEXT;"
                )
            if "reviewed_at" not in cols:
                conn.execute(
                    "ALTER TABLE vocabulary_entries ADD COLUMN reviewed_at TEXT;"
                )
        except Exception:
            pass

        try:
            cur_r = conn.execute("PRAGMA table_info(vocabulary_reviews);")
            r_cols = {row["name"] for row in cur_r.fetchall()}
            review_cols_to_add = [
                ("spelling_assessment", "TEXT"),
                ("meaning_assessment", "TEXT"),
                ("pos_assessment", "TEXT"),
                ("dialect_assessment", "TEXT"),
                ("example_assessment", "TEXT"),
                ("source_assessment", "TEXT"),
                ("correction_proposals", "TEXT"),
                ("counts_for_consensus", "INTEGER DEFAULT 1"),
                ("superseded_by_id", "INTEGER"),
            ]
            for col_name, col_type in review_cols_to_add:
                if col_name not in r_cols:
                    conn.execute(
                        f"ALTER TABLE vocabulary_reviews ADD COLUMN {col_name} {col_type};"
                    )
        except Exception:
            pass

    def initialize_schema(self) -> None:
        """Initialize database tables, views, and indexes."""
        with self.get_connection() as conn:
            self._migrate_schema(conn)
            conn.executescript(SCHEMA_SQL)
            if is_fts5_available(conn):
                try:
                    conn.executescript(FTS_SCHEMA_SQL)
                except Exception:
                    pass
            conn.commit()
