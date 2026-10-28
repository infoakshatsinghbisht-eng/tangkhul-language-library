# Quickstart Guide

This guide demonstrates how to interact with the currently operational foundation of the **Tangkhul Language Library**.

> **Note on Project Status**:
> As of Step 1, this package provides the core architecture, data models, configuration manager, and manifest validation engine. Domain parsing pipelines (Books, Songs, etc.) and search operations are planned for subsequent steps and are not yet operational.

---

## 1. Inspecting Library Version and Environment

```python
import tangkhul_lib
from tangkhul_lib.core.config import LibraryConfig

print(f"Tangkhul Library Version: {tangkhul_lib.__version__}")

# Inspect detected paths
config = LibraryConfig.from_environment()
print(f"Project root: {config.paths.root_dir}")
print(f"Manifests directory: {config.paths.manifests_dir}")
```

---

## 2. Using Core Data Models

You can instantiate and validate `ManifestRecord` and `VocabularyEntry` data structures:

```python
from tangkhul_lib.core.models import ManifestRecord, ProvenanceRecord, VocabularyEntry

# Create a bibliographic manifest entry
record = ManifestRecord(
    id="BK-0001",
    resource_type="books",
    title="Tangkhul Folk Literature and Grammar",
    creator="Community Custodian",
    year=1975,
    language="Tangkhul",
    permission_status="community_authorized",
    verification_status="verified",
)

print(record.to_dict())

# Create a vocabulary entry with provenance
provenance = ProvenanceRecord(
    source_id="BK-0001",
    resource_type="books",
    citation="Tangkhul Folk Literature and Grammar, 1975, p. 12",
    page_or_section="p. 12",
    context_sentence="I ramli kaphung kazing kachon ngalung.",
)

entry = VocabularyEntry(
    id="VOCAB-0001",
    headword="kaphung",
    meanings=["mountain", "hill"],
    part_of_speech="noun",
    provenance=[provenance],
    verification_status="verified",
)

print(f"Headword: {entry.headword}")
print(f"Meanings: {entry.meanings}")
print(f"Sources cited: {len(entry.provenance)}")
```

---

## 3. Validating Manifests

Run validation on existing JSONL manifests using the built-in validator or command line:

```python
from pathlib import Path
from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file

manifest_path = Path("data/manifests/books.jsonl")
records = validate_manifest_file(manifest_path)
print(f"Validated {len(records)} books in manifest.")
```

Or from the command line:

```bash
python scripts/validate_manifests.py
```

---

## 4. Unified Vocabulary Search CLI

Query vocabulary across all six domain modules (Books, Songs, Dictionaries, Culture, History, Literature) with full provenance preservation and multi-mode search capabilities:

### 4.1 Search Modes

The unified vocabulary CLI supports four dedicated search strategies:

1. **Substring Match (`--mode substring`, default)**:
   Performs case-insensitive, Unicode-normalized substring matching against headwords and alternative spellings.
   ```bash
   tangkhul vocab --search "ngashan"
   tangkhul vocab --exact "ngashān"
   ```

2. **SQLite FTS5 Full-Text Search (`--mode fulltext`)**:
   Uses the SQLite FTS5 extension with `unicode61` tokenization and BM25 relevance ranking. Indexes headwords, alternative spellings, meanings, English glosses, example sentences, and dialect tags.
   ```bash
   tangkhul vocab --search "ngashan" --mode fulltext
   tangkhul vocab --meaning "traditional practice" --mode fulltext
   ```

3. **Fuzzy Similarity Match (`--mode fuzzy`)**:
   Employs conservative Levenshtein similarity ratio comparison against headwords and alternative spellings, tolerant of minor typos and orthographic variations.
   ```bash
   tangkhul vocab --search "ngashon" --mode fuzzy --threshold 0.70
   ```

4. **Tangkhul-Aware Phonetic Search (`--mode phonetic`)**:
   Normalizes orthographic forms according to documented phonetic and morphological patterns (macron folding, glottal/apostrophe stripping, velar nasal `ng` preservation).
   ```bash
   tangkhul vocab --search "ngashan" --mode phonetic
   ```
   To enable experimental Tangkhul dialect sound shifts (sibilant neutralization `sh`/`s`, aspirate simplification `kh`/`k`, liquid alternation `r`/`l`, and diphthong reduction `ei`/`ai`), pass `--experimental-phonetics`:
   ```bash
   tangkhul vocab --search "ngasan" --mode phonetic --experimental-phonetics
   ```

### 4.2 Diagnostic Search Explanation (`--explain-search`)

Display detailed diagnostics showing which search strategy was executed, FTS5 engine status, fallback behavior (if FTS5 is unavailable), active phonetic rules, and applied filters:

```bash
tangkhul vocab --search "ngashan" --mode fulltext --explain-search
```

### 4.3 Rebuilding the FTS5 Full-Text Index (`--rebuild-index`)

Safely recreate and repopulate the FTS5 search index from all active, permitted vocabulary entries:

```bash
tangkhul vocab --rebuild-index
```

### 4.4 Multi-Criteria Filtering

Search modes work seamlessly alongside secondary bibliographic and linguistic filters:

```bash
# Fulltext search filtered by dialect and verified status
tangkhul vocab --search "custom" --mode fulltext --dialect "Ukhrul" --verification-status verified

# Fuzzy search within specific source modules
tangkhul vocab --search "proverb" --mode fuzzy --source-type culture --limit 5
```

---

## 5. Permission-Aware Document Ingestion (`tangkhul ingest`)

The document ingestion pipeline processes authorized digital books, scanned PDFs, dictionaries, and literature, extracting text page-by-page, segmenting into paragraph chunks, and indexing text and vocabulary:

### 5.1 Inspecting Source Eligibility

Inspect all 138 catalogued sources across all six manifests to see which sources are eligible or ineligible:

```bash
tangkhul ingest --list-sources
```

### 5.2 Previewing Extraction Without Saving

Preview text extraction, page breakdown, character count, and quality checks on a local document file before committing anything to storage:

```bash
tangkhul ingest --preview path/to/document.pdf
```

### 5.3 Simulating Ingestion with Dry Run

Simulate complete ingestion, permission checking, paragraph chunking, and candidate vocabulary token extraction without touching the database or filesystem:

```bash
tangkhul ingest --source-id "BK-PET-001" --file path/to/document.pdf --dry-run
```

### 5.4 Ingesting an Authorized Document

Ingest an authorized local document by providing its manifest record ID and local file path:

```bash
tangkhul ingest --source-id "BK-PET-001" --file path/to/document.pdf
```

### 5.5 Searching Ingested Document Chunks via SQLite FTS5

Full-text search across all ingested document paragraphs with page numbers, section headings, and BM25 relevance ranking:

```bash
tangkhul ingest --search "ngashan" --limit 5
```

### 5.6 Generating Detailed Ingestion & Extraction Reports

View a detailed report of an ingested document, including file metadata, SHA-256 hash, extraction status, OCR requirements, warnings, and chunk breakdown:

```bash
tangkhul ingest --report DOC-BK-PET-001-A1B2C3D4
```

### 5.7 Listing Ingested Documents

List all documents currently stored in the library with page counts and status:

```bash
tangkhul ingest --list-documents
```

### 5.8 Rebuilding the Document Chunks FTS5 Index

Rebuild the FTS5 full-text index for all permitted document chunks:

```bash
tangkhul ingest --rebuild-chunks-index
```

---

## 6. Vocabulary Review & Community Correction Workflow (`tangkhul review`)

Transform harvested candidate tokens into fully verified lexical entries through explicit human review, preserving source citations, dialect variants, and audit history:

### 6.1 Listing Candidates in Review Queue

List candidates awaiting review with rich filters:

```bash
# List all pending candidates
tangkhul review --list --status pending_review

# List candidates lacking verified definitions
tangkhul review --list --missing-meaning

# List candidates filtered by dialect variety
tangkhul review --list --dialect "Ukhrul"

# List candidates with suggested duplicates
tangkhul review --list --has-duplicates
```

### 6.2 Inspecting Full Candidate Details & Suggested Duplicates

View complete candidate record with source provenance, context sentences, duplicate suggestions, and audit history:

```bash
tangkhul review --show VOCAB-CAND-001
```

### 6.3 Accepting a Candidate as Verified

Accept a candidate as verified after providing or confirming its meaning (requires `--reviewer` and `--meaning`):

```bash
tangkhul review --accept VOCAB-CAND-001 \
  --reviewer "Elder-Khangam" \
  --meaning "traditional custom" \
  --pos "noun" \
  --notes "Confirmed from community elders"
```

### 6.4 Rejecting an Invalid Token or OCR Artifact

Reject non-lexical tokens, scanning artifacts, or typos (requires `--reviewer` and `--reason`):

```bash
tangkhul review --reject VOCAB-CAND-002 \
  --reviewer "Linguist-Alice" \
  --reason "Non-lexical OCR artifact; ligature error"
```

### 6.5 Flagging Uncertain Candidates or Semantic Conflicts

Flag words needing further community or linguistic consultation:

```bash
tangkhul review --flag VOCAB-CAND-001 \
  --reviewer "Linguist-Alice" \
  --status reviewed_uncertain \
  --notes "Tone contour uncertain; consult Phungcham elders"
```

### 6.6 Linking Confirmed Duplicates

Link an orthographic or spelling variant to a canonical entry, automatically transferring all provenance citations:

```bash
tangkhul review --link-duplicate VOCAB-CAND-001 \
  --target-id VOCAB-MAIN-001 \
  --reviewer "Supervisor-Z" \
  --notes "Merged alternative spelling"
```

### 6.7 Viewing Review Audit History

Inspect chronological decisions, reviewer identity, timestamp, and notes for any entry:

```bash
tangkhul review --history VOCAB-MAIN-001
```

### 6.8 Offline Community Review Exchanges (Export & Import)

Export candidates to a clean JSONL file (automatically shielding restricted sentences), share with community members, and import validated corrections:

```bash
# Export pending candidates to JSONL
tangkhul review --export data/review/pending_candidates.jsonl

# Import community review corrections
tangkhul review --import-corrections data/review/community_corrections.jsonl \
  --reviewer "Hunphun-Youth-Council"
```

### 6.9 Interactive Review Session

Launch a terminal-based interactive review session stepping through pending candidates:

```bash
tangkhul review --interactive --reviewer "Linguist-Bob" --limit 20
```

---

## 7. Authorized Vocabulary Enrichment (`tangkhul enrich`)

Step 13 introduces source-backed lexicon enrichment and dialect-aware data collection. It parses structured vocabularies, formatted glossaries, and running text from permitted and public-domain sources, extracts candidates, classifies categories, preserves dialect markers, and stages new entries for human review without overwriting existing verified definitions.

### 7.1 Listing Eligible Vocabulary Sources

Inspect all catalogued sources across all six manifests to check their enrichment eligibility, license tier, and dialect:

```bash
# List all eligible vocabulary sources across all modules
tangkhul enrich --list-sources

# Filter by source module
tangkhul enrich --list-sources --source-type dictionaries

# Filter by dialect variety
tangkhul enrich --list-sources --dialect "Ukhrul"
```

### 7.2 Previewing Lexical Extraction Without Commits

Preview headwords, glosses, parts of speech, and dialect tags from any local file:

```bash
tangkhul enrich --preview path/to/lexicon.tsv --limit 10
```

### 7.3 Simulating Enrichment with Dry Run

Simulate full enrichment, permission verification, category classification, duplicate detection, and data gap analysis without writing to the database:

```bash
tangkhul enrich --source-id "DIC-HIST-001" --file path/to/lexicon.tsv --dry-run
```

### 7.4 Ingesting & Enriching from an Authorized Source

Process an authorized dictionary or glossary file, registering candidate vocabulary entries and provenance:

```bash
tangkhul enrich --source-id "DIC-HIST-001" --file path/to/lexicon.tsv
```

### 7.5 Inspecting Duplicate Suggestions & Phonetic Variants

Enrich a source while showing conservative phonetic, orthographic, and Levenshtein duplicate suggestions:

```bash
tangkhul enrich --source-id "DIC-HIST-001" --file path/to/lexicon.tsv --show-duplicates
```

### 7.6 Overriding Idempotency Protection (`--force`)

By default, files with matching SHA-256 hashes are skipped. To reprocess an updated or modified file:

```bash
tangkhul enrich --source-id "DIC-HIST-001" --file path/to/lexicon.tsv --force
```

### 7.7 Exporting Review Candidates to JSONL

Export extracted candidates directly into a JSONL file for offline linguistic review, with restricted sentences automatically shielded:

```bash
tangkhul enrich --source-id "DIC-HIST-001" --file path/to/lexicon.tsv \
  --export-candidates data/review/pettigrew_candidates.jsonl
```

---

## 8. Multi-Reviewer Consensus & Community Governance (`tangkhul review`)

Step 14 introduces multi-reviewer consensus, native-speaker validation workflows, independent review assessments, structured review task dispatching, and shielded offline package exchanges.

> [!IMPORTANT]
> Software-enforced consensus is a governance mechanism, not a substitute for qualified native-speaker judgment, cultural authority, or formal legal clearance. Linguistic validation is strictly decoupled from source evidence verification and copyright permission.

### 8.1 Viewing Active Consensus Policy

Inspect the currently configured consensus rules (approval threshold, single-reviewer exception flags, eligible reviewer rosters, and source verification prerequisites):

```bash
tangkhul review --consensus-policy
```

### 8.2 Review Quality & Governance Metrics

Generate a real-time audit report tabulating candidate verification states, open/in-progress tasks, consensus counts, conflicts, permission-blocked records, and reviewer contributions:

```bash
tangkhul review --metrics
```

### 8.3 Generating & Listing Structured Review Tasks

Idempotently scan pending vocabulary candidates, prioritizing missing meanings, dialect ambiguities, and existing reviews awaiting second validation:

```bash
# Generate prioritized review tasks idempotently
tangkhul review --create-tasks --limit 20

# List review tasks (optionally filter by status: open, in_review, conflict, etc.)
tangkhul review --tasks --status open --limit 10
```

### 8.4 Claiming a Review Task

Assign a review task to an attributable contributor identity or community-approved pseudonym:

```bash
tangkhul review --claim-task TASK-VOCAB-001 --reviewer "Somrei-Elder-01"
```

### 8.5 Recording Structured Review Decisions

Record immutable multi-dimensional review assessments (spelling, meaning, part-of-speech, dialect, and source evidence):

```bash
tangkhul review \
  --decision approve \
  --entry-id VOCAB-001 \
  --reviewer "Somrei-Elder-01" \
  --spelling-assessment accurate \
  --meaning-assessment verified \
  --pos-assessment noun \
  --source-assessment reliable \
  --notes "Spelling and definition verified against standard Ukhrul usage."
```

If corrections are required or conflicts are discovered:

```bash
# Request corrections
tangkhul review \
  --decision correction_requested \
  --entry-id VOCAB-002 \
  --reviewer "Linguist-Alice" \
  --notes "Vowel a requires macron."

# Flag conflicting dialect forms
tangkhul review \
  --decision flag_conflict \
  --entry-id VOCAB-003 \
  --reviewer "Elder-Wung" \
  --notes "Contested tone marker between Raphei and Ukhrul varieties."

# Withdraw a previous approval
tangkhul review \
  --decision withdraw_approval \
  --entry-id VOCAB-001 \
  --reviewer "Somrei-Elder-01" \
  --notes "Discovered polysemous nuance requiring re-evaluation."
```

### 8.6 Evaluating Multi-Reviewer Consensus

Evaluate whether a candidate meets the configured threshold (default: 2 independent eligible reviewers), verifies source evidence, and clears copyright restrictions:

```bash
# Evaluate a single entry
tangkhul review --consensus VOCAB-001

# Evaluate all reviewable entries
tangkhul review --consensus
```

### 8.7 Viewing Active Unresolved Conflicts

List entries with conflicting reviewer assessments or dialect disagreements:

```bash
tangkhul review --conflicts
```

### 8.8 Offline Review Packages (Version 2.0 JSON)

Exchange structured review tasks with native speakers, community elders, and linguistic consultants who work offline:

```bash
# 1. Export tasks to a shielded review package (sensitive texts masked automatically)
tangkhul review --export-package data/review/batch_01.json --limit 25

# 2. Validate package schema, decisions, duplicate submissions, and stale edits
tangkhul review --validate-package data/review/batch_01_reviewed.json

# 3. Simulate import in dry-run mode
tangkhul review --import-package data/review/batch_01_reviewed.json --dry-run

# 4. Import reviewed decisions and update consensus
tangkhul review --import-package data/review/batch_01_reviewed.json
```

### 8.9 Reviewer Decision History

Inspect all sequential decisions recorded for a specific reviewer or community pseudonym:

```bash
tangkhul review --reviewer-history "Somrei-Elder-01"
```

---

## 9. Audio Corpus, Pronunciation & Speech Operations (`tangkhul audio`)

Step 15 introduces full audio corpus management, technical audio validation, speaker consent tracking, pronunciation variant linkage, and permission-aware speech data distribution.

> [!IMPORTANT]
> The Tangkhul Language Library never fabricates audio recordings, speaker identities, or consent records. Audio files must only be imported when explicit speaker consent or community authorization has been documented.

### 9.1 Audio Telemetry and Metrics (`tangkhul audio summary`)

Display high-level statistics covering total recordings, clearance tiers (authorized, pending, restricted, withdrawn, metadata-only), cumulative duration, and dialect breakdowns:

```bash
tangkhul audio summary
# or
tangkhul audio --summary
```

### 9.2 Listing Audio Recordings (`tangkhul audio list`)

List recordings with deterministic status indicators and privacy shielding:

```bash
# List all active recordings
tangkhul audio list

# Filter by dialect variety and consent status
tangkhul audio list --dialect "Ukhrul" --consent-status authorized

# Include withdrawn recordings for archival audits
tangkhul audio list --include-withdrawn
```

### 9.3 Inspecting Audio Records (`tangkhul audio inspect`)

View detailed metadata, technical specifications, linked vocabulary items, transcriptions, and consent audit logs:

```bash
# Standard public inspection (sensitive transcriptions & paths shielded if restricted)
tangkhul audio inspect AUD-REC-20261026-A1B2C3

# Privileged inspection for authorized custodians
tangkhul audio inspect AUD-REC-20261026-A1B2C3 --privileged
```

### 9.4 Technical Audio Validation (`tangkhul audio validate`)

Validate file integrity, sample rate, channel count, duration, format, and calculate SHA-256 checksums without external dependencies:

```bash
tangkhul audio validate path/to/sample_utterance.wav
```

### 9.5 Importing Authorized Recordings (`tangkhul audio import`)

Import an authorized audio recording into the library's managed audio directory with vocabulary linking and deduplication checks:

```bash
# Import an authorized field recording linked to an existing vocabulary entry
tangkhul audio import path/to/recording.wav \
  --title "Pronunciation of ngashan" \
  --vocab-id "VOCAB-HIST-001" \
  --headword "ngashān" \
  --speaker "Speaker_Hunphun_01" \
  --dialect "Ukhrul" \
  --village "Hunphun" \
  --transcription "ngashan" \
  --ipa "ŋaʃan" \
  --consent-status authorized \
  --permitted-uses "linguistic_research,community_education"

# Simulate import in dry-run mode
tangkhul audio import path/to/recording.wav --title "Dry Run" --dry-run

# Register metadata-only record when audio cannot legally or ethically be stored
tangkhul audio import --metadata-only \
  --title "Archival Chant Metadata Reference" \
  --dialect "Raphei" \
  --speaker "Elder_Rph_02" \
  --consent-status pending
```

### 9.6 Searching Audio by Transcript or Headword (`tangkhul audio search`)

Search across recordings using titles, verbatim transcriptions, normalized spellings, IPA forms, or speaker pseudonyms:

```bash
tangkhul audio search "ngashan"
tangkhul audio search "ŋaʃan" --dialect "Ukhrul"
```

### 9.7 Pronunciation Management & Native-Speaker Review (`tangkhul audio pronunciation`)

Manage multi-variant pronunciation records linked to vocabulary entries:

```bash
# List or search pronunciations by headword
tangkhul audio pronunciation "ngashān"

# View all pronunciations linked to a specific vocabulary entry ID
tangkhul audio pronunciation --vocab-id "VOCAB-HIST-001"

# Record a native-speaker review decision on a pronunciation record
tangkhul audio pronunciation PRON-001 \
  --review-decision approve \
  --reviewer "native_speaker_ukr_01" \
  --review-notes "Accurate traditional Ukhrul pronunciation."
```

### 9.8 Consent Audits & Revocation (`tangkhul audio permissions`)

Inspect the immutable consent audit history or withdraw speaker consent:

```bash
# Inspect consent audit history
tangkhul audio permissions AUD-REC-20261026-A1B2C3

# Withdraw consent (immediately shields recording and revokes all future exports)
tangkhul audio permissions AUD-REC-20261026-A1B2C3 \
  --withdraw \
  --reason "Speaker requested removal from digital research distribution." \
  --authorized-by "Village Linguistic Custodian Committee"
```

### 9.9 Exporting Authorized Audio Corpus (`tangkhul audio export`)

Export authorized, verified recordings and generate `audio_manifest.jsonl` while strictly excluding pending, restricted, or withdrawn materials:

```bash
# Dry-run export simulation
tangkhul audio export data/exports/speech_bundle/ --dry-run

# Export cleared audio files and JSONL manifest
tangkhul audio export data/exports/speech_bundle/
```







