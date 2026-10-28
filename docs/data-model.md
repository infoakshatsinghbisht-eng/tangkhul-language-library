# Data Model and Schema Specification

This document details the data structures and domain schemas used across the Tangkhul Language Library.

---

## 1. Resource Manifest Schema (`.jsonl`)

Manifest files in `data/manifests/` follow the JSON Lines format, where each line is an independent JSON object conforming to the `ManifestRecord` schema:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | Yes | Unique stable identifier (e.g., `BK-TLS-001`, `SNG-TRAD-001`, `DIC-HIST-001`). |
| `resource_type` | `string` | Yes | One of: `books`, `songs`, `dictionaries`, `culture`, `history`, `literature`. |
| `title` | `string` | Yes | Primary title in Tangkhul or original language. |
| `title_translation` | `string` | No | English translation of the title. |
| `creator` | `string` | No | Author, compiler, singer, or community contributor. |
| `year` | `integer` | No | Year of publication or primary recording. |
| `publisher` | `string` | No | Publisher, issuing society, or organization. |
| `language` | `string` | Yes | Default: `Tangkhul`. |
| `dialect` | `string` | No | Dialect variety (e.g., `Ukhrul Standard`, `Hunphun`, `Phungcham`). |
| `source_url` | `string` | No | Canonical link or archival record URL. |
| `source_identifier` | `string` | No | ISBN, DOI, call number, or library catalog ID. |
| `license` | `string` | No | Specific license if known (e.g., `Public Domain`, `CC-BY-NC-4.0`). |
| `permission_status` | `string` | Yes | One of: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`. |
| `local_path` | `string` | No | Relative path to local file inside `data/raw/` (uncommitted). |
| `verification_status` | `string` | Yes | One of: `unverified`, `partially_verified`, `verified`, `community_reviewed`, `needs_review`. |
| `notes` | `string` | No | Contextual notes, digitization history, or permissions context. |

---

## 2. Dictionaries Domain Schemas

### `DictionarySourceRecord`
```python
@dataclass
class DictionarySourceRecord:
    id: str
    title: str
    alternate_titles: list[str]
    authors: list[str]
    editors: list[str]
    compiler: str | None
    contributors: list[str]
    publisher: str | None
    publication_place: str | None
    publication_year: int | None
    edition: str | None
    languages: list[str]
    language_pair: str | None
    dialect: str | None
    source_type: str                   # dictionary, bilingual_dictionary, glossary, etc.
    isbn: str | None
    identifier: str | None
    source_url: str | None
    local_file_path: str | None
    license: str | None
    license_evidence: str | None
    permission_status: str             # public_domain, permitted, restricted, etc.
    access_status: str                 # metadata_only, full_text_available, etc.
    verification_status: str           # verified, needs_review, unverified
    notes: str | None
```

### `DictionaryEntryRecord`
```python
@dataclass
class DictionaryEntryRecord:
    id: str                            # e.g., DIC-HIST-001-ENT-0001
    dictionary_id: str                 # Reference to DictionarySourceRecord.id
    headword: str                      # Original Tangkhul surface form
    normalized_headword: str           # Lowercase NFC search key
    alternate_spellings: list[str]
    transliteration: str | None
    definitions_en: list[str]          # English glosses
    definitions_hi: list[str]          # Hindi glosses
    other_definitions: list[str]       # Manipuri (Meiteilon) or other glosses
    part_of_speech: str | None         # noun, verb, adjective, etc.
    pronunciation: str | None
    notes: str | None
    examples: list[str]
    dialect: str | None
    grammatical_info: str | None
    page_or_section: str | None        # Exact page/entry locator
    entry_number: str | None
    source_excerpt: str | None
    extraction_method: str
    confidence: float
    license: str | None
    permission_status: str
    verification_status: str
    vocabulary_id: str | None          # Link to VocabularyEntry.id
```

---

## 3. Unified Vocabulary Entry Schema

```python
@dataclass
class VocabularyEntry:
    id: str                               # Unique entry ID (e.g., VOCAB-00012)
    headword: str                         # Original Tangkhul spelling
    meanings: list[str]                   # Tangkhul definitions or glosses
    translations_en: list[str]            # English translations
    alternative_spellings: list[str]      # Verified alternate spellings
    dialect_variants: list[str]           # Forms in other Tangkhul dialects
    dialect: str | None                   # Dialect designation for headword
    part_of_speech: str | None            # e.g., noun, verb, adjective, particle
    pronunciation: str | None             # Phonetic or IPA transcription
    example_sentences: list[str]          # Contextual example sentences
    provenance: list[ProvenanceRecord]    # Source references & attributions
    verification_status: str              # Verification state
    license_restrictions: str | None      # Any redistribution constraints
```

---

## 4. Provenance Record Schema

```python
@dataclass
class ProvenanceRecord:
    source_id: str                        # Reference to manifest `id`
    resource_type: str                    # Module type: books, songs, dictionaries, culture, etc.
    citation: str                         # Human-readable bibliographic citation
    page_or_section: str | None           # Page, stanza, or chapter
    context_sentence: str | None          # Sentence in which word occurred
    recorded_year: int | None             # Year source was published/recorded
    permission_status: str                # Legal/community status
```

---

## 5. Cultural Record Schema (`CulturalRecord`)

```python
@dataclass
class CulturalRecord:
    id: str                               # e.g., CULT-FEST-001, CULT-PROV-001
    title: str                            # Title or designation
    category: str                         # proverb, custom, festival, ritual, tradition, oral_tradition
    local_name: str | None                # Indigenous name (e.g., Luira Phanit, Haora)
    alternate_names: list[str]            # Spelling variants or alternate names
    subcategory: str | None               # agricultural, attire, justice, wisdom, etc.
    original_text: str | None             # Verbatim Tangkhul text (sayings, chants)
    translation_en: str | None            # English translation / gloss
    translations_other: list[str]         # Translations in Hindi, Meiteilon, etc.
    description: str | None               # Cultural and ethnographic account
    cultural_significance: str | None     # Purpose, spiritual context, symbolism
    season_or_timing: str | None          # When the practice occurs (e.g., January/February)
    village: str | None                   # Associated village (Hunphun, Phungcham, Champhung)
    dialect: str | None                   # Dialect variety (Ukhrul, Phungcham, etc.)
    language: str                         # Default: Tangkhul
    participants: list[str]               # Community roles (Awunga, Hangva elders, youth)
    procedure: list[str]                  # Sequence of customary practices
    related_records: list[str]            # Cross-links to songs, books, dictionary entries
    historical_period: str | None         # Historical period (e.g., 17th Century)
    year: int | None                      # Documented publication/recording year
    source_id: str | None                 # Source identifier (e.g., Hodson-1911-Ch3)
    source_title: str | None              # Publisher or publication work
    source_page: str | None               # Exact page in source
    source_section: str | None            # Section or chapter
    source_url: str | None                # Canonical link or repository landing page
    contributor: str | None               # Informant, elder, author, or documenting body
    contributor_consent: bool             # Whether consent was granted for publication
    license: str | None                   # Governing license
    permission_status: str                # community_authorized, public_domain, restricted, pending
    access_status: str                    # metadata_only, open_access, restricted, attributed
    verification_status: str              # verified, needs_review, unverified
    notes: str | None                     # Reviewer observations and notes
    resource_type: str                    # "culture"
```

---

## 6. Historical Record Schema (`HistoricalRecord`)

```python
@dataclass
class HistoricalRecord:
    id: str                               # e.g., HIST-EVT-001, HIST-PRS-001, HIST-PLC-001
    title: str                            # Title or designation of historical entity
    record_type: str                      # historical_event, person, place, migration,
                                          # community_history, language_history,
                                          # historical_document, timeline_event, oral_history
    alternate_titles: list[str]           # Alternate spellings, colloquial titles, colonial names
    summary: str | None                   # Objective contemporary summary
    description: str | None               # Comprehensive historical narrative
    original_text: str | None             # Verbatim historical phrase or primary quotation
    translation_en: str | None            # English translation / interpretation
    event_date: str | None                # Approximate date wording (e.g. "c. 1917–1918")
    sort_year: int | None                 # Normalized year for chronological sorting
    period: str | None                    # Historical era (e.g. Pre-colonial, Colonial Era, WWII)
    place: str | None                     # Historical settlement or geographic feature
    village: str | None                   # Associated Tangkhul village
    dialect: str | None                   # Documented dialect or linguistic variety
    language: str                         # Default: Tangkhul
    people_involved: list[str]            # Personalities, clans, or institutions involved
    related_events: list[str]             # Related historical event IDs
    related_records: list[str]            # Cross-module links to books, songs, dictionaries, culture
    source_id: str | None                 # Source identifier (e.g. HIST-HODSON-1911)
    source_title: str | None              # Title of cited publication or document
    source_page: str | None               # Page reference
    source_section: str | None            # Chapter or volume locator
    source_url: str | None                # Canonical archive link or repository landing page
    contributor: str | None               # Historian, elder, compiler, or institution
    contributor_consent: bool             # Consent for extraction/publication (default: True)
    evidence_type: str                    # primary_source, archival_record, scholarly_interpretation,
                                          # oral_tradition, ethnographic_account, candidate_fieldwork
    confidence: float                     # Confidence score between 0.0 and 1.0
    contradictory_accounts: list[str]     # Documented conflicting dates or interpretations
    license: str | None                   # Governing license (Public Domain, etc.)
    permission_status: str                # public_domain, community_authorized, restricted, pending
    access_status: str                    # metadata_only, open_access, restricted, attributed
    verification_status: str              # verified, needs_review, unverified
    notes: str | None                     # Reviewer observations and historiographical notes
    resource_type: str                    # "history"
```

---

## 7. Literary Record Schema (`LiteraryRecord`)

```python
@dataclass
class LiteraryRecord:
    id: str                               # e.g., LIT-POEM-001, LIT-FLK-001, LIT-PLAY-001
    title: str                            # Primary title in Tangkhul or documented form
    work_type: str                        # Primary genre (poem, short_story, folk_tale,
                                          # oral_narrative, riddle, proverb_collection,
                                          # play, novel, essay, literary_anthology,
                                          # ballad, children_literature, translation, other)
    alternate_titles: list[str]           # Alternate spellings, colloquial titles, English titles
    original_title: str | None            # Original Tangkhul title preserving orthography
    title_translation: str | None         # English translation of title
    genres: list[str]                     # Secondary or composite genres
    author: str | None                    # Primary author
    poet: str | None                      # Poet designation
    storyteller: str | None               # Traditional storyteller or elder
    playwright: str | None                # Dramatist
    translator: str | None                # Translator attribution
    editor: str | None                    # Editor or compiler
    collector: str | None                 # Folklorist or field collector
    contributor: str | None               # Contributing community member
    contributor_consent: bool             # Consent for indexing/extraction (default: True)
    publication_year: int | None          # Publication year
    composition_date: str | None          # Approximate era of oral/written composition
    edition: str | None                   # Edition or print run
    publisher: str | None                 # Publishing body or society
    publication_place: str | None         # Location of publication
    language: str                         # Default: Tangkhul
    dialect: str | None                   # Village or regional dialect
    village: str | None                   # Associated village
    region: str | None                    # Sub-regional area (Northern, Western, etc.)
    collection: str | None                # Anthology or series name
    anthology: str | None                 # Parent anthology name
    parent_work_id: str | None            # Link to parent collection record
    book_id: str | None                   # Link to parent book in books.jsonl (BK-TLS-007, etc.)
    isbn: str | None                      # ISBN where assigned
    identifier: str | None                # Archival call number or catalog identifier
    source_url: str | None                # Institutional archive link
    source_id: str | None                 # Source identifier
    source_title: str | None              # Source publication title
    source_page: str | None               # Page locator
    source_section: str | None            # Section or chapter
    local_path: str | None                # Local file path for authorized content
    license: str | None                   # Governing license
    license_evidence: str | None          # License terms or evidence citation
    permission_status: str                # permitted, public_domain, community_authorized, restricted, pending
    access_status: str                    # metadata_only, full_text_available, restricted
    verification_status: str              # verified, needs_review, unverified
    text_availability: str                # metadata_only, full_text, excerpt, restricted
    original_text: str | None             # Verbatim text or authorized excerpt
    translation_text: str | None          # Authorized translation text
    summary: str | None                   # Literary synopsis
    stanza_count: int | None              # Total stanzas in poetic work
    line_count: int | None                # Total lines in work
    related_authors: list[str]            # Associated poets, playwrights, or translators
    related_works: list[str]              # Related adaptations, earlier editions, translations
    related_records: list[str]            # Cross-module links to books, songs, culture, history
    notes: str | None                     # Reviewer observations and literary provenance
    resource_type: str                    # "literature"
```

---

## 8. SQLite Relational Schema

The shared SQLite database (`data/database/tangkhul_corpus.sqlite`) contains unified tables:
- `manifest_records`: Cross-module catalogue index.
- `books`: Primary book metadata and educational classification.
- `songs`: Song metadata, collector attribution, and musical genres.
- `dictionaries` & `dictionary_entries`: Lexicographical sources and individual lemmas.
- `culture`: Cultural records, proverbs, festivals, attire, rituals, and customs.
- `history`: Historical events, historical figures, settlements, migrations, language history, and timelines.
- `literature`: Literary works, poetry, plays, folktales, short stories, riddles, ballads, and translations.
- `vocabulary_entries`: Unified shared lexicon with multi-source provenance.
- `vocabulary_fts`: SQLite FTS5 virtual table (`tokenize='unicode61'`) indexing permitted vocabulary entries for BM25 full-text ranking.
- `provenance_records`: Source tracing linking words to books, songs, dictionaries, culture, history, and literature.
- `extracted_tokens`: Permitted candidate word tokens harvested during ingestion.
- `ingested_documents`: Ingested document records with checksums, extraction metadata, and review states.
- `document_chunks`: Extracted text paragraphs with page/section provenance and content hashes.
- `document_chunks_fts`: SQLite FTS5 virtual table (`tokenize='unicode61'`) indexing permitted document chunks.
- `vocabulary_reviews`: Audit history recording human review decisions, before/after snapshots, reviewer attribution, and duplicate links.

---

## 9. Search Result Match Model (`SearchResultMatch`)

Used by the unified vocabulary search engine across fulltext, fuzzy, phonetic, and substring modes:

```python
@dataclass
class SearchResultMatch:
    entry_id: str                      # VocabularyEntry.id
    headword: str                      # Stored headword
    match_mode: str                    # substring, fulltext, fuzzy, or phonetic
    match_score: float                 # Normalized relevance score or BM25 rank
    matched_term: str                  # Matched query token or headword/alternate
    explanation: str                   # Human-readable match diagnostic detail
    dialect: str | None = None         # Dialect designation
    verification_status: str | None = None # Verification status
    source_ids: list[str] = field(default_factory=list) # Contributing source manifest IDs
```

---

## 10. Ingested Document Model (`IngestedDocument`)

Represents an authorized digital document processed through the ingestion pipeline:

```python
@dataclass
class IngestedDocument:
    id: str                            # Stable document ID (e.g. DOC-BK-TLS-001-A1B2C3D4)
    source_id: str                     # Original manifest record ID (e.g. BK-TLS-001)
    source_title: str                  # Title from manifest
    creator: str | None                # Author / creator
    publication_year: int | None       # Year of publication
    source_type: str                   # books, songs, dictionaries, culture, history, literature
    language: str                      # Default: Tangkhul
    file_path: str                     # Path to local source file
    file_name: str                     # Base name of the file
    file_hash: str                     # SHA-256 hexadecimal hash
    file_size_bytes: int               # File size in bytes
    file_format: str                   # pdf, txt, md, docx
    extraction_method: str             # pypdf, text_utf8, docx_xml, ocr
    extraction_timestamp: str          # ISO 8601 UTC timestamp
    extraction_status: str             # extracted, needs_review, failed, skipped
    page_count: int                    # Total pages processed
    char_count: int                    # Total extracted characters
    word_count: int                    # Total extracted words
    permission_status: str             # permitted, public_domain, community_authorized
    verification_status: str           # verified, unverified, needs_review
    extraction_warnings: list[str]     # Diagnostic extraction warnings
    ocr_status: str                    # not_required, ocr_needed, ocr_performed, ocr_failed
    review_status: str                 # verified, pending_review, needs_correction
    notes: str | None = None           # Additional reviewer or archival notes
    created_at: str | None = None
    updated_at: str | None = None
```

---

## 11. Document Chunk Model (`DocumentChunk`)

Represents an individual paragraph or structural segment of an ingested document:

```python
@dataclass
class DocumentChunk:
    id: str                            # Deterministic ID (e.g. CHK-DOC-001-P1-0)
    document_id: str                   # IngestedDocument.id
    source_id: str                     # Manifest source ID
    page_number: int | None            # Page locator (1-indexed for PDF/DOCX)
    section_heading: str | None        # Nearest section or chapter heading
    chunk_index: int                   # Sequential index within document
    text: str                          # Original text content
    char_count: int                    # Character count
    word_count: int                    # Word count
    content_hash: str                  # SHA-256 hash of chunk text
    permission_status: str             # Inherited permission tier
    verification_status: str           # Inherited verification status
    created_at: str | None = None
```

---

## 12. Vocabulary Review Audit Model (`VocabularyReviewRecord`)

Represents an auditable human review decision, community correction, or duplicate linking operation:

```python
@dataclass
class VocabularyReviewRecord:
    entry_id: str                      # Reference to VocabularyEntry.id
    headword: str                      # Surface form of the vocabulary headword
    decision: str                      # accept, reject, uncertain, duplicate, conflict, edit
    reviewer: str                      # Reviewer identifier, username, or pseudonym
    id: int | None = None              # Autoincrement primary key in vocabulary_reviews
    review_timestamp: str = ""         # Timestamp of decision
    notes: str | None = None           # Diagnostic rationale, uncertainty notes, or references
    previous_state: dict | None = None # Snapshot of VocabularyEntry prior to change
    new_state: dict | None = None      # Snapshot of VocabularyEntry after change
    suggested_meaning: str | None = None # Meaning gloss confirmed or updated
    suggested_pos: str | None = None   # Part of speech confirmed
    suggested_dialect: str | None = None # Dialect variety confirmed
    target_duplicate_id: str | None = None # Canonical entry ID if linked as duplicate
```

---

## 13. Vocabulary Enrichment Record Models (`EnrichmentRunRecord` & `EnrichmentSummary`)

Step 13 introduces structured provenance and telemetry tracking for vocabulary enrichment executions.

### Enrichment Run Schema (`EnrichmentRunRecord`)

Represents an idempotent, auditable enrichment run logged in the `enrichment_runs` table:

```python
@dataclass
class EnrichmentRunRecord:
    id: str                             # Deterministic ID: ENR-{source_id}-{YYYYMMDDHHMMSS}
    source_id: str                      # Foreign reference to manifest source ID
    input_file_path: str                # Path to source file processed
    file_hash: str                      # SHA-256 hash of source content for idempotency
    run_timestamp: str                  # ISO-8601 execution timestamp
    dry_run: bool                       # True if simulated without DB commits
    total_extracted: int                # Headwords/tokens parsed
    new_candidates: int                 # Review candidates created
    exact_matches: int                  # Existing exact matches found
    duplicates_detected: int            # Conservative phonetic/orthographic suggestions
    skipped_items: int                  # Duplicates or non-lexical tokens bypassed
    errors_count: int                   # Non-fatal warnings encountered
    lexical_categories: dict[str, int]  # Semantic & grammatical category breakdown
    dialect_distribution: dict[str, int] # Dialect occurrences (Ukhrul, Phungcham, etc.)
    status: str                         # "success", "partial", "failed", "blocked"
```

### SQLite Schema (`enrichment_runs`)

```sql
CREATE TABLE IF NOT EXISTS enrichment_runs (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    input_file_path TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    run_timestamp TEXT NOT NULL,
    dry_run INTEGER NOT NULL DEFAULT 0,
    total_extracted INTEGER NOT NULL DEFAULT 0,
    new_candidates INTEGER NOT NULL DEFAULT 0,
    exact_matches INTEGER NOT NULL DEFAULT 0,
    duplicates_detected INTEGER NOT NULL DEFAULT 0,
    skipped_items INTEGER NOT NULL DEFAULT 0,
    errors_count INTEGER NOT NULL DEFAULT 0,
    lexical_categories TEXT,
    dialect_distribution TEXT,
    status TEXT NOT NULL DEFAULT 'success'
);
CREATE INDEX IF NOT EXISTS idx_enrichment_runs_source ON enrichment_runs (source_id);
```

### In-Memory Enrichment Summary Model (`EnrichmentSummary`)

```python
@dataclass
class EnrichmentSummary:
    source_id: str
    source_title: str
    permission_tier: str
    total_extracted: int = 0
    new_candidates: int = 0
    exact_matches: int = 0
    potential_duplicates: int = 0
    skipped_items: int = 0
    errors: list[str] = field(default_factory=list)
    permission_skips: list[str] = field(default_factory=list)
    categories_found: dict[str, int] = field(default_factory=dict)
    data_gaps: list[str] = field(default_factory=list)
    dialect_breakdown: dict[str, int] = field(default_factory=dict)
    run_id: str = ""
    dry_run: bool = False
```

---

## 14. Multi-Reviewer Consensus and Review Task Models

Step 14 introduces structured models for multi-reviewer consensus evaluation, fine-grained review assessments, and auditable task queues.

### Extended Review Record (`VocabularyReviewRecord`)

Builds upon Step 12 with multi-dimensional linguistic and source evidence assessments:

```python
@dataclass
class VocabularyReviewRecord:
    entry_id: str                              # Reference to VocabularyEntry.id
    headword: str                              # Surface form of the headword
    decision: str                              # approve, correction_requested, uncertain, reject, flag_conflict, withdraw_approval
    reviewer: str                              # Reviewer identifier or community pseudonym
    id: int | None = None                      # Autoincrement primary key
    review_timestamp: str = ""                 # ISO-8601 UTC timestamp
    notes: str | None = None                   # Reviewer notes or uncertainty explanations
    previous_state: dict | None = None         # Entry snapshot prior to decision
    new_state: dict | None = None              # Entry snapshot after decision
    spelling_assessment: str | None = None     # accurate, variant, typo, needs_standardization
    meaning_assessment: str | None = None      # verified, inaccurate, incomplete, polysemous
    pos_assessment: str | None = None          # noun, verb, adjective, etc.
    dialect_assessment: str | None = None      # Ukhrul, Raphei, Western, etc.
    example_assessment: str | None = None      # natural, archaic, ungrammatical
    source_assessment: str | None = None       # verified, unverified, questionable
    correction_proposals: dict[str, Any] | None = None # Explicit proposed corrections
    counts_for_consensus: bool = True          # False for ineligible or withdrawn reviews
    superseded_by_id: int | None = None        # ID of decision superseding this record
```

### Review Task Model (`ReviewTask`)

Tracks prioritized units of review work for unresolved candidates:

```python
@dataclass
class ReviewTask:
    id: str                                    # Task ID: TASK-{entry_id}
    entry_id: str                              # Target VocabularyEntry.id
    headword: str                              # Surface headword
    task_type: str = "full_review"             # meaning_review, conflict_resolution, etc.
    review_dimensions: list[str] = field(default_factory=lambda: ["meaning", "spelling"])
    source_id: str | None = None               # Primary source citation
    priority: str = "medium"                   # high, medium, low
    reason: str = ""                           # Diagnostic priority reason
    status: str = "open"                       # open, in_review, correction_requested, conflict, completed
    assigned_reviewer: str | None = None       # Claimed reviewer or pseudonym
    created_at: str = ""                       # Creation timestamp
    completed_at: str | None = None            # Completion timestamp
    unresolved_disagreements: list[str] = field(default_factory=list)
    consensus_outcome: str | None = None       # verified, rejected, conflict, etc.
```

### Consensus Evaluation Model (`ConsensusEvaluation`)

Captures the deterministic evaluation of all active reviews for an entry:

```python
@dataclass
class ConsensusEvaluation:
    entry_id: str                              # Target VocabularyEntry.id
    policy_version: str                        # Version of consensus policy evaluated
    threshold_required: int                    # Required independent approvals (default: 2)
    eligible_reviewers_count: int              # Total eligible reviewers configured
    approvals_count: int                       # Active independent approvals
    rejections_count: int                      # Rejections blocking verification
    conflicts_count: int                       # Unresolved dialect/orthographic conflicts
    corrections_count: int                     # Active correction requests
    decision_outcome: str                      # verified, rejected, conflict, correction_requested, lacks_source_evidence, permission_blocked, pending_consensus
    is_consensus_met: bool                     # True if linguistic threshold satisfied
    is_source_verified: bool                   # True if entry has source citations
    is_permission_cleared: bool                # True if sources clear license restrictions
    is_public_eligible: bool                   # is_source_verified and is_permission_cleared
    evaluated_at: str                          # ISO-8601 evaluation timestamp
    approving_reviewers: list[str]             # List of unique approving reviewer IDs
    rejecting_reviewers: list[str]             # List of rejecting reviewer IDs
    conflicting_reviewers: list[str]           # List of conflict flagging reviewer IDs
    correction_reviewers: list[str]            # List of correction requesting reviewer IDs
    notes: str | None = None                   # Evaluation summary notes
    single_reviewer_exception_applied: bool = False # Explicit single-reviewer exception flag
```

### SQLite Tables (`review_tasks` & `review_consensus`)

```sql
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
    created_at TEXT NOT NULL,
    completed_at TEXT,
    unresolved_disagreements TEXT,
    consensus_outcome TEXT
);
CREATE INDEX IF NOT EXISTS idx_review_tasks_entry ON review_tasks (entry_id);
CREATE INDEX IF NOT EXISTS idx_review_tasks_status ON review_tasks (status);
CREATE INDEX IF NOT EXISTS idx_review_tasks_priority ON review_tasks (priority);

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
    is_consensus_met INTEGER NOT NULL,
    is_source_verified INTEGER NOT NULL,
    is_permission_cleared INTEGER NOT NULL,
    is_public_eligible INTEGER NOT NULL,
    evaluated_at TEXT NOT NULL,
    approving_reviewers TEXT,
    rejecting_reviewers TEXT,
    conflicting_reviewers TEXT,
    correction_reviewers TEXT,
    notes TEXT,
    single_reviewer_exception INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_review_consensus_entry ON review_consensus (entry_id);
```

## 15. Audio Corpus, Pronunciation & Speech Data Infrastructure

Step 15 introduces four relational tables and one FTS5 virtual table for audio recordings, pronunciation variants, fine-grained annotations, and speaker consent records.

### Audio Recording Model (`AudioRecording`)

```python
@dataclass
class AudioRecording:
    id: str                                    # Stable identifier (AUD-REC-YYYYMMDD-HEX)
    title: str                                 # Recording title or descriptive phrase
    vocab_entry_id: str | None = None          # Linked VocabularyEntry.id (if available)
    corpus_id: str | None = None               # Optional audio corpus collection ID
    description: str | None = None             # Linguistic or situational context
    recording_date: str | None = None          # Date of recording (YYYY-MM-DD)
    speaker_pseudonym: str | None = None       # Non-identifying speaker reference
    dialect: str | None = None                 # Dialect (Ukhrul, Raphei, Champhung, etc.)
    village: str | None = None                 # Village locality
    region: str | None = None                  # Regional variety
    language: str = "Tangkhul"                 # Language label
    variety: str | None = None                 # Variety / sub-dialect
    recording_method: str = "field_recording"  # field_recording, studio, archival_transfer, metadata_only
    recording_source: str | None = None        # Contributor citation or archival source
    file_path: str | None = None               # Safe relative path in data/raw/audio/
    original_filename: str | None = None       # Source audio filename
    file_format: str = "wav"                   # wav, mp3, ogg, flac, m4a, aac
    duration_seconds: float = 0.0              # Audio duration in seconds
    sample_rate: int = 0                       # Sample rate in Hz (e.g. 16000, 44100)
    channels: int = 1                          # Channel count (1=mono, 2=stereo)
    file_size_bytes: int = 0                   # File size in bytes
    checksum_sha256: str = ""                  # SHA-256 integrity & deduplication hash
    transcription: str | None = None           # Verbatim transcription
    transcription_normalized: str | None = None # Normalized transcription for search
    ipa_transcription: str | None = None       # IPA phonetic transcription
    transliteration: str | None = None         # Phonetic transliteration
    source_title: str | None = None            # Source title if archival transfer
    source_citation: str | None = None         # Bibliographic or archival citation
    source_url: str | None = None              # Web URL (if public/authorized)
    license: str | None = None                 # Legal license specification
    copyright_status: str = "copyright_retained" # copyright_retained, public_domain, cc_by
    consent_status: str = "pending"            # pending, authorized, restricted, withdrawn, needs_review
    permitted_uses: list[str] = field(default_factory=lambda: ["linguistic_research"])
    access_restrictions: str | None = None     # Specific restrictions (e.g. restricted)
    is_withdrawn: bool = False                 # True if speaker revoked consent
    withdrawal_date: str | None = None         # Date consent was revoked
    withdrawal_reason: str | None = None       # Documented reason for withdrawal
    verification_status: str = "unverified"    # verified, unverified, community_reviewed
    notes: str | None = None                   # Curatorial and audio notes
    segments: list[AudioSegmentTimestamp] = field(default_factory=list) # Time alignments
    created_at: str | None = None              # ISO UTC creation timestamp
    updated_at: str | None = None              # ISO UTC update timestamp
```

### Pronunciation Record Model (`PronunciationRecord`)

Supports multiple pronunciation variants and dialect variations per vocabulary entry without destructive overwrites:

```python
@dataclass
class PronunciationRecord:
    id: str                                    # PRON-{recording_id} or PRON-{seq}
    vocab_entry_id: str                        # Foreign key to VocabularyEntry.id
    headword: str                              # Target headword
    recording_id: str | None = None            # Foreign key to AudioRecording.id
    pronunciation_ipa: str | None = None       # Standard IPA transcription
    pronunciation_phonetic: str | None = None  # Informal phonetic spelling
    dialect: str | None = None                 # Dialect variety (e.g. Ukhrul, Raphei)
    village: str | None = None                 # Village variety
    speaker_pseudonym: str | None = None       # Non-identifying speaker reference
    is_primary: bool = False                   # Flag indicating primary/standard variant
    source_citation: str | None = None         # Supporting linguistic citation
    verification_status: str = "unverified"    # verified, unverified, needs_review
    review_status: str = "pending_review"      # pending_review, accepted, rejected, conflict
    review_notes: str | None = None            # Native-speaker reviewer assessment notes
    reviewer: str | None = None                # Reviewer pseudonym
    reviewed_at: str | None = None             # ISO review timestamp
    created_at: str | None = None              # ISO creation timestamp
```

### Audio Consent Audit Record (`AudioConsentRecord`)

Provides an append-only, immutable audit trail for speaker consent grants and revocations:

```python
@dataclass
class AudioConsentRecord:
    recording_id: str                          # Linked AudioRecording.id
    speaker_pseudonym: str                     # Non-identifying speaker reference
    consent_status: str                        # authorized, pending, withdrawn, restricted
    id: int | None = None                      # Auto-incrementing audit log sequence ID
    permitted_uses: list[str] = field(default_factory=list)
    restrictions: str | None = None            # Access limits or sacred taboos
    recorded_date: str | None = None           # Date consent was recorded
    withdrawn_date: str | None = None          # Date consent was revoked
    withdrawn_reason: str | None = None        # Reason for consent revocation
    authorized_by: str | None = None           # Custodian or representative authorizing action
    timestamp: str | None = None               # ISO UTC event timestamp
```

### Audio SQLite Schema

```sql
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
```








