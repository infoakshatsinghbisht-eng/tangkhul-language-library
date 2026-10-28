# Architecture Overview

The **Tangkhul Language Library** is designed as a modular, extensible, and provenance-focused Python toolkit.

---

## Architectural Principles

1. **Separation of Concerns**: Ingestion, validation, storage, vocabulary harmonization, and domain representations are strictly decoupled into dedicated packages.
2. **Unified Vocabulary Layer**: Rather than keeping vocabulary isolated within separate domain silos (e.g., words from books vs words from songs), a central vocabulary model links all surface words back to their origin manifests.
3. **Strict Non-Destructive Deduplication**: Two words with identical spellings may have different etymologies, tonal contours, dialect origins, or semantic senses. Deduplication never eliminates distinct senses or erases source citations.
4. **Data Hygiene & Privacy**: Large raw scans and copyright-sensitive digital media live outside Git and are referenced via metadata manifests.

---

## Package Structure (`src/tangkhul_lib/`)

```
tangkhul_lib/
├── core/                  # Foundational configuration, exceptions, and data models
│   ├── config.py          # Root path discovery and runtime settings
│   ├── exceptions.py      # Structured exception hierarchy
│   └── models.py          # Dataclass definitions: ManifestRecord, VocabularyEntry, ProvenanceRecord
├── vocabulary/            # Cross-cutting vocabulary engine
│   ├── search.py          # Search query interfaces (planned)
│   ├── normalization.py   # Non-destructive Unicode NFC normalization
│   ├── deduplication.py   # Provenance-preserving deduplication algorithms
│   └── provenance.py      # Attribution tracking helpers
├── books/                 # Domain module: Textbooks, grammar treatises, printed volumes
├── songs/                 # Domain module: Folk songs, ceremonial chants, lyrics
├── dictionaries/          # Domain module: Lexicons, wordlists, and multilingual glosses
├── culture/               # Domain module: Proverbs (Paotam), customs, material culture
├── history/               # Domain module: Historical chronicles, toponyms, oral genealogy
├── literature/            # Domain module: Folk tales (Khararchan), poetry, riddles
├── storage/               # Data persistence layer
│   ├── database.py        # SQLite database connection manager
│   └── repositories.py    # Repository pattern abstractions
├── ingestion/             # Ingestion pipelines
│   ├── text_extraction.py # Plain-text extraction interfaces (planned)
│   └── metadata_validation.py # JSONL schema validation
└── cli/                   # Command-line utility entrypoint
```

---

## Data Flow Diagram

```
[Raw Sources: Books, Songs, Oral Recordings, Lexicons]
                        │
                        ▼
           [data/manifests/*.jsonl]
                        │
         (Metadata Validation via Ingestion)
                        │
                        ▼
      [Unified Vocabulary & Corpus Storage]
         (SQLite / Repositories Layer)
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
[Domain Modules: Books, Songs,    [Vocabulary Engine:
 Culture, History, Literature]     Search, Lemmatization, Provenance]
```

---

## Unified Search Architecture (Step 10)

The search layer combines four search strategies designed specifically for Tangkhul data:

```
                      [User Query via CLI / API]
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
  [Substring Match]      [SQLite FTS5 Fulltext]    [Phonetic / Fuzzy]
          │                       │                       │
   Exact/NFC Substring       BM25 Ranking         Levenshtein Ratio /
     (All Platforms)      unicode61 Tokenizer      Tangkhul Phonetics
                                  │
                       (Fallback if FTS5 off)
                                  │
                                  ▼
                   [Permission & Privacy Shield]
                 (Exclude restricted items/context)
                                  │
                                  ▼
                     [Ranked Provenance Results]
```

### 1. SQLite FTS5 Full-Text Search

- **Virtual Table**: `vocabulary_fts` using `tokenize='unicode61'`.
- **Searchable Fields**: Headwords, alternative spellings, meanings, English glosses, example sentences, dialects, and grammatical parts of speech.
- **BM25 Relevance Ranking**: Uses SQLite's built-in `bm25()` rank function for term weighting and document relevance.
- **Query Sanitization**: Malformed operators (unbalanced quotes, bare `NOT`, `AND`, `OR`, wildcards, and hyphens) are safely parsed and quoted by `sanitize_fts_query` to prevent runtime crashes or SQL syntax errors.
- **Availability & Fallback**: Automatically checks `is_fts5_available()`. If the running SQLite engine was built without FTS5, queries gracefully fall back to Unicode-normalized substring matching with a clear diagnostic explanation.

### 2. Tangkhul-Aware Phonetic & Fuzzy Search

Generic algorithms like English Soundex or Metaphone do not model Tangkhul phonology. The library implements a modular rule framework (`TangkhulPhoneticEncoder`):

#### Evidence-Based Transformations
Derived from published grammars and orthographies (William Pettigrew 1918, S. Arokianathan 1980/1987, Tangkhul Literature Society):
- **Macron Folding**: Normalizes macrons indicating vowel length (`ā`, `ē`, `ī`, `ō`, `ū` → `a`, `e`, `i`, `o`, `u`).
- **Glottal Normalization**: Normalizes typographic apostrophes and glottal stop notations (`’`, `'`).
- **Velar Nasal Preservation**: Preserves `ng` as an indivisible nasal unit.
- **Double-Vowel Length**: Neutralizes repetitive orthographic vowel elongation (`aa` → `a`).

#### Experimental Rules (Disabled by Default)
Tangkhul dialect sound shifts are quarantined and only enabled with `--experimental-phonetics`:
- **Sibilant Neutralization**: `sh` ↔ `s` (frequent between Northern Raphei varieties and Ukhrul Standard).
- **Aspirate Simplification**: `kh`, `th`, `ph` → `k`, `t`, `p` (simplification observed across colloquial registers).
- **Liquid Alternation**: `r` ↔ `l` (historical dialect alternation).
- **Diphthong Reduction**: `ei` ↔ `ai` (common spelling variations in early 20th-century missionary texts).

#### Linguistic Safeguards
- Phonetic keys are ephemeral and used solely for matching; original headwords, spellings, and dialect metadata are never modified in storage.
- Phonetic similarity never merges distinct vocabulary entries.

### 3. Index Lifecycle & Data Consistency

- **Idempotent Initialization**: Schema creation checks `IF NOT EXISTS` and executes safely across restarts.
- **Auto-Backfill**: When initialized, if `vocabulary_fts` is empty while relational entries exist, the index is backfilled automatically.
- **Synchronous Hooks**: `VocabularyRepository.add()` indexes entries upon creation; `delete()` removes them from `vocabulary_fts`.
- **Safe Rebuild**: `tangkhul vocab --rebuild-index` uses transactional execution (`BEGIN` / `COMMIT`) so partially completed operations do not corrupt the index.

### 4. Permission & Privacy Controls

- Records marked `license_restrictions == "restricted"` are excluded from FTS indexing and from all four search modes.
- Contextual example sentences belonging to restricted entries are masked from query results.
- Unverified candidate records retain `needs_review` status and cannot be promoted through search indexing.

### 5. Performance Trade-offs & Future Benchmarking

- Current index performance is optimized for vocabulary sets up to ~100,000 entries with millisecond response times.
- Fuzzy matching uses pure-Python Levenshtein calculations; for corpora exceeding 100,000 entries, C-accelerated extensions or trigram indexes should be evaluated.

---

## Document Ingestion Architecture (Step 11)

The document ingestion subsystem connects authorized digital sources (books, scanned PDFs, dictionaries, literature, and cultural records) to the unified database and search infrastructure:

```
[Local Document File (PDF, TXT, MD, DOCX)]
                   │
                   ▼
       [SourcePermissionChecker]
   (Enforce permitted/public_domain/community_authorized;
    Reject pending/restricted/needs_review with reasons)
                   │
                   ▼
            [TextExtractor]
   ┌───────────────┼───────────────┐
   ▼               ▼               ▼
(PDF via pypdf)  (TXT / MD)   (DOCX XML)
   │
   ▼
[Extraction Quality Assessment]
(Empty pages, replacement chars, OCR detection)
   │
   ▼
[Paragraph Chunking & Hashing]
(Deterministic chunk IDs, SHA-256 deduplication)
   │
   ├───────────────────────────────┐
   ▼                               ▼
[DocumentRepository]       [Vocabulary Synchronization]
(Store ingested_documents,  (Extract candidate tokens,
 document_chunks, & FTS5    normalize NFC, link provenance,
 document_chunks_fts)       retain unverified status)
```

### 1. Permission-Aware Source Selection
- **Mandatory Pre-Flight Validation**: Documents can only be ingested if matched against an authorized manifest record.
- **Tiers Allowed**: `permitted`, `public_domain`, `community_authorized`.
- **Tiers Blocked**: `pending` (under review), `restricted` (copyrighted/sensitive), `needs_review` (unverified candidates).
- **Zero Fabrication**: Missing metadata is never invented; permissions are never assumed based solely on publication year or online catalogue listings.

### 2. Multi-Format Extraction Capabilities
- **Text-based PDFs**: Extracted page-by-page via `pypdf`, preserving original pagination, empty page accounting, and password encryption detection.
- **Plain Text & Markdown**: Decoded with UTF-8 / fallback handling, preserving heading structures.
- **Word Documents (`.docx`)**: Pure-Python XML parsing via `zipfile` and `xml.etree.ElementTree` without requiring external binary dependencies.
- **Scanned PDF & OCR Detection**: Analyzes character density per page. If pages lack extractable text or contain excessive replacement characters (`\ufffd`), flags `ocr_status="ocr_needed"` and `extraction_status="needs_review"`. Pluggable `BaseOcrAdapter` interface allows connecting verified local OCR engines without automatic downloading of large models.

### 3. Paragraph Chunks and Deterministic Idempotency
- Documents are partitioned into paragraph-level `DocumentChunk` structures with page numbers, section headings, and character/word counts.
- Chunk IDs are deterministic: `CHK-{doc_id}-P{page}-{chunk_index}`.
- Content hashes (SHA-256) prevent duplicate imports of identical files unless `--force` is specified.

### 4. FTS5 Document Chunk Search
- `document_chunks_fts` provides full-text search across all extracted paragraphs with BM25 ranking.
- Restricted documents and unverified sensitive chunks are shielded from search results.
- Rebuilding (`--rebuild-chunks-index`) executes transactionally.

### 5. Vocabulary Linkage Without Fabrication
- Discovered tokens are normalized via Unicode NFC.
- Existing vocabulary entries matched against discovered tokens have their provenance records extended to cite the new document, page, and context sentence.
- Newly discovered tokens are added with `verification_status="unverified"` and an empty definitions list, ensuring zero hallucinated or fabricated linguistic meanings.

---

## Vocabulary Review & Community Correction Architecture (Step 12)

The vocabulary review subsystem transforms raw extracted candidate tokens and uncertain entries into validated, authoritative lexical records through human review and community validation:

```
[Harvested Candidate Tokens / Unverified Entries]
                       │
                       ▼
          [VocabularyReviewService]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[Review Queue Filtering]     [Duplicate Suggester]
(status, dialect, missing    (Exact NFC, Levenshtein,
 meanings, source types)      Phonetic Encoder)
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
           [Human Review Decision]
  ┌──────────────┬─────────────┬──────────────┬──────────────┐
  ▼              ▼             ▼              ▼              ▼
[Accept]      [Reject]      [Flag]         [Link Dup]     [Edit]
(verified)    (shielded)   (uncertain/    (merge prov,    (meanings,
                           conflict)       add alt-sp)    pos, dialect)
  │              │             │              │              │
  └──────────────┴─────────────┼──────────────┴──────────────┘
                               │
                               ▼
                [VocabularyReviewRepository]
                (Audit trail in vocabulary_reviews,
                 FTS5 fulltext synchronization)
```

### 1. Review States & Lifecycle
- `pending_review`: Initial state for newly extracted tokens and unreviewed candidates.
- `accepted`: Promoted to `verification_status="verified"` after a reviewer confirms at least one verified meaning. Synchronizes to SQLite FTS5 index.
- `rejected`: Invalid tokens, typos, or OCR artifacts. Retained for auditability with `license_restrictions="restricted"` to shield from public search.
- `reviewed_uncertain`: Reviewed by linguist/elder but requiring further native speaker consultation.
- `conflict`: Conflicting definitions or part-of-speech usages across sources requiring reconciliation.
- `duplicate`: Confirmed variant linked to a canonical entry.

### 2. Evidence-Based Review Rules
- **No Hallucinated Meanings**: Accepting a candidate strictly requires at least one confirmed definition.
- **Mandatory Attribution**: Every decision records the reviewer's identifier or pseudonym and UTC timestamp.
- **Auditable Change Snapshots**: Every action captures before and after JSON snapshots in `vocabulary_reviews`.

### 3. Duplicate Suggestion & Non-Destructive Linking
- Suggestions combine:
  - Exact NFC normalized matching.
  - Tangkhul phonetic encoding (accounting for macrons, glottals, and velar nasals).
  - Conservative Levenshtein distance similarity.
- When linking a duplicate, all source citations and context sentences are merged into the canonical entry without loss.
- The duplicate candidate's headword is recorded as an alternative spelling of the canonical entry.

### 4. Privacy & Cultural Safeguards
- Restricted cultural passages and sensitive sentences are masked during queue display, show reports, and offline JSONL exports.
- Review decisions never alter underlying source manifest permission tiers.

---

## Vocabulary Enrichment Pipeline Architecture (Step 13)

Step 13 establishes a verified, source-backed lexicon enrichment pipeline connecting legally accessible historical and linguistic documents with the unified vocabulary repository:

```
[Registered Source & File]
           │
           ▼
[Evaluate Source Permissions] ────(If restricted / pending)────► [Skip / Log Blocked Reason]
           │
           │ (If public_domain / permitted / community_authorized)
           ▼
[Format-Aware Lexical Extractor]
┌─────────────────────────────────┼─────────────────────────────────┐
▼                                 ▼                                 ▼
[Structured TSV/CSV/JSONL]      [Formatted Text Lines]          [Running Text Ingestion]
(headword, gloss, POS, dialect) (word (pos) : definition)       (tokenize, NFC, filter stopwords)
           │                                 │                                 │
           └─────────────────────────────────┼─────────────────────────────────┘
                                             │
                                             ▼
                             [Conservative Duplicate Detection]
                             (Exact NFC, Tangkhul Phonetics, Levenshtein)
                                             │
                                             ├─────────────────────────────────┐
                                             ▼                                 ▼
                             [Existing Entry Found]                 [New Headword Form]
                             - Preserve human reviewed definitions  - Create VocabularyEntry
                             - Append source provenance              (status: pending_review)
                             - Record dialect / variant link        - Tag lexical category
                                             │                                 │
                                             └────────────────┬────────────────┘
                                                              │
                                                              ▼
                                                [Database Transaction]
                                                - Insert/update vocabulary entries
                                                - Insert vocabulary_provenance
                                                - Record enrichment_runs telemetry
                                                - Sync to vocabulary_fts FTS5 index
```

### 1. Permission Gates & Shielding
- Evaluates source permissions strictly before reading file contents.
- Allows only `public_domain`, `permitted`, and `community_authorized` resources.
- Silently rejects or blocks `restricted`, `pending`, and `needs_review` resources, generating diagnostic audit reasons without parsing protected content.
- Restricts JSONL candidate exports by masking sensitive context sentences as `[RESTRICTED TEXT - ACCESS PRIVILEGED]`.

### 2. Dual Lexical Extraction Modality
- **Dictionary & Glossary Mode**: Parses explicit headwords, parts of speech, glosses, and dialect tags from TSV, CSV, JSONL, or formatted lines (`headword (pos.) : definition`).
- **Running-Text Mode**: Extracts authentic attested tokens from literary and historical prose (TXT, MD, PDF, DOCX), applying Unicode NFC normalization, filtering punctuation and numerals, and attaching sentence-level provenance.

### 3. Human Definition Protection & Non-Destructive Merging
- Never overwrites definitions or notes previously confirmed by human reviewers (`verification_status == 'verified'`).
- If an existing entry is found, appends source provenance while preserving human determinations.
- Suggests duplicate and dialect variants without automatic conflation, requiring human approval via the Step 12 review workflow.

### 4. Telemetry and Idempotency
- Every run is tracked in the `enrichment_runs` table with file hash (SHA-256), timestamp, item counts, categories found, dialect distribution, and status.
- Re-running against an identical source file hash is recognized as idempotent and skips redundant writes unless `--force` is specified.
---

## Section 14: Multi-Reviewer Consensus & Community Governance Architecture

Step 14 extends the review system with multi-reviewer consensus policies, native-speaker validation, structured task dispatching, and shielded offline exchanges.

```
                  [Pending / Extracted Vocabulary Candidates]
                                       │
                                       ▼
                       [Structured Review Task Engine]
                    (Priority: missing meanings, conflicts,
                     OCR warnings, awaiting 2nd reviewer)
                                       │
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
          [Direct CLI Review]                [Offline Review Package]
       (tangkhul review --decision)           (Schema 2.0 JSON, shielded)
                     │                                   │
                     │                        (Validate, dry-run, import)
                     │                                   │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                         [Immutable Review Audit Log]
                      (Spelling, Meaning, POS, Dialect,
                       Source Evidence, Correction Proposals)
                                       │
                                       ▼
                       [Consensus Evaluation Service]
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
  [Approvals < Threshold]      [Unresolved Conflict /       [Linguistic Approvals >= 2]
     outcome: pending            Correction Requested]                    │
  (Awaiting 2nd reviewer)     (review_status: conflict /                  ▼
                               needs_correction)           [Source Evidence & Permission Gate]
                                                                          │
                                       ┌──────────────────────────────────┴──────────────────────────────────┐
                                       ▼                                                                     ▼
                        [Sufficient Source & Cleared]                                         [No Source or Restricted]
                          - verification_status: verified                                       - outcome: lacks_source_evidence
                          - review_status: accepted                                               or permission_blocked
                          - Synchronized to FTS5 search                                         - Candidate remains unverified
                          - ReviewTask status: completed                                        - Restricted text shielded
```

### 1. Decoupled Governance Pillars
Linguistic plausibility is strictly decoupled from source evidence verification and copyright/cultural clearance:
- **Linguistic Review**: Assesses whether the headword spelling, definition, part of speech, dialect, and usage are linguistically accurate in Tangkhul.
- **Source Verification**: Requires attested occurrences and page/section citations in the library's catalogued manifests. An unbacked word cannot be verified regardless of review approvals.
- **Copyright & Cultural Clearance**: Respects license restrictions. Material marked `restricted` is blocked from public promotion and export, even if fully attested and linguistically valid.

### 2. Multi-Reviewer Consensus Engine
- **Default Policy**: Requires at least two independent eligible reviewer approvals before promoting a candidate to `verified`.
- **Deduplicated Identities**: Multiple submissions by the same contributor identity count as a single active vote.
- **Withdrawn Approvals**: Supersede previous approvals in the immutable history, automatically reverting verification if consensus drops below the threshold.
- **Role Eligibility**: Optional explicit reviewer whitelist prevents unauthorized or arbitrary consensus claims.
- **Single-Reviewer Exceptions**: Supported only when explicitly configured for emergency or authorized administrative workflows, and logged transparently in consensus telemetry.

### 3. Idempotent Review Tasks
- Review tasks are generated deterministically based on data quality gaps (missing meanings, unassigned dialects, OCR warnings, and single-review entries).
- Re-running task generation is idempotent and never creates duplicate tasks for unresolved issues.
- Tasks track assignment, required dimensions, unresolved disagreements, and completion timestamps.

### 4. Shielded Offline Review Packages
- Versioned JSON packages (`package_schema_version: "2.0"`) allow native speakers and community elders to review tasks in disconnected environments.
- Automatically masks sensitive cultural text and restricted sentences with privilege notices.
- Import engine detects stale packages (where the database entry was updated after package export), prevents duplicate submissions, and validates against tampering before committing.

## 15. Audio Corpus, Pronunciation Records, and Speech Infrastructure

### 1. Architectural Principles
Step 15 introduces an ethical, permission-aware audio corpus and pronunciation infrastructure into the Tangkhul Language Library. The speech layer integrates directly with the existing shared SQLite database, unified vocabulary entries, provenance tracking, and native-speaker review workflows.

```
+-----------------------------------------------------------------------------------+
|                        TANGKHUL AUDIO & SPEECH INFRASTRUCTURE                     |
+-----------------------------------------------------------------------------------+
                                          │
       ┌──────────────────────────────────┴──────────────────────────────────┐
       ▼                                                                     ▼
[Audio File Validation & Ingestion]                        [Metadata-Only Registration]
- Valid formats: WAV (zero-dependency wave),                - Used when audio cannot legally
  MP3, OGG, FLAC, M4A, AAC (mutagen optional)                 or ethically be stored locally
- Path security (safe_resolve_audio_path)                   - Catalogues speaker, dialect,
- Checksum deduplication (SHA-256)                            transcription, & provenance
       │                                                                     │
       └──────────────────────────────────┬──────────────────────────────────┘
                                          ▼
                      [Audio Corpus Storage & Repositories]
                      - audio_recordings (metadata, paths, technical specs)
                      - pronunciation_records (linked to vocabulary_entries)
                      - audio_annotations (word- and segment-level timestamps)
                      - audio_consent_records (immutable audit events)
                      - audio_recordings_fts (SQLite FTS5 speech index)
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                  ▼                                  ▼
[Consent & Permissions]        [Pronunciation Workflow]             [Permissioned Export]
- can_access_audio()           - Multi-variant IPA per headword     - Excludes withdrawn,
- can_export()                 - Native-speaker consensus review      restricted, pending
- withdraw_consent()           - Verbatim + normalized text         - Generates versioned
- mask_recording_metadata()    - Retains audit history                audio_manifest.jsonl
```

### 2. Audio Validation & Path Security
- **Zero-Dependency Core**: Physical WAV audio metadata extraction uses Python's standard library `wave` module (channels, sample rate, duration, and file size) without requiring GPU acceleration or paid external APIs.
- **Optional Formats**: Compressed audio formats (`mp3`, `ogg`, `flac`, `m4a`) are supported via the optional `mutagen` library when available.
- **Path Traversal Protection**: All file operations resolve paths strictly within the library's managed `data/raw/audio/` directory via `safe_resolve_audio_path()`. Escaping paths (`../`) or directory traversal attacks raise an `AudioSecurityError`.
- **Integrity & Checksum Deduplication**: Every imported audio file is fingerprinted using SHA-256 (`compute_file_sha256()`). Duplicate files are detected immediately to prevent accidental overwrites or duplicate database records with conflicting provenance.

### 3. Ethical Consent & Access Governance
- **Strict Permission Hierarchy**: Audio recordings are governed by five explicit permission tiers: `pending`, `authorized`, `restricted`, `withdrawn`, and `needs_review`.
- **Consent Revocation Workflow**: When a speaker or community custodian revokes consent, `withdraw_consent()` updates the recording to `is_withdrawn=True`, sets status to `withdrawn`, and appends an immutable `AudioConsentRecord` to the audit log.
- **Cultural & Privacy Shielding**: Public listings, inspect views, and export routines automatically mask restricted files, sensitive sacred transcriptions, and speaker pseudonyms (`[SHIELDED SPEAKER]`, `[RESTRICTED AUDIO FILE - ACCESS PRIVILEGED]`) unless viewed by an authorized custodian.
- **Safe Export Engine**: `export_corpus()` verifies both consent authorization and linguistic verification before writing out audio files and `audio_manifest.jsonl`, strictly filtering out unverified, pending, restricted, or withdrawn materials.






