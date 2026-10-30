# Tangkhul Language Library

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Step%2015%20(Audio%20Corpus%20%26%20Speech%20Infrastructure)-informational.svg)](#current-project-status)
[![Testing](https://img.shields.io/badge/Pytest-307%20Passing-brightgreen.svg)](#testing-and-development)
[![Linter](https://img.shields.io/badge/Ruff-Checked-blue.svg)](file:///f:/tangkhul-language-library/pyproject.toml)
[![License](https://img.shields.io/badge/License-Pending%20Confirmation-lightgrey.svg)](#license-and-citation)

A professional, modular Python library for **Tangkhul language preservation, linguistic research, vocabulary extraction, and cultural documentation**.

> 📌 **Executive Summary & Complete Navigation Guide**: For a high-level overview, complete file catalogue, and direct clickable navigation across all 15 implemented milestones, see [EXECUTIVE_SUMMARY.md](file:///f:/tangkhul-language-library/EXECUTIVE_SUMMARY.md).

---

## Table of Contents

- [Project Purpose and Objectives](#project-purpose-and-objectives)
- [Current Project Status](#current-project-status)
- [Planned Domain Modules](#planned-domain-modules)
- [Folder Structure and Architecture](#folder-structure-and-architecture)
- [Installation Instructions](#installation-instructions)
  - [Windows PowerShell](#windows-powershell)
  - [Linux and macOS](#linux-and-macos)
- [Quick-Start Example](#quick-start-example)
- [Unified Vocabulary Database Design](#unified-vocabulary-database-design)
- [Resource Manifest Schema](#resource-manifest-schema)
- [Data Sources and Provenance](#data-sources-and-provenance)
- [Data Quality and Verification](#data-quality-and-verification)
- [Data Storage Conventions and Git Hygiene](#data-storage-conventions-and-git-hygiene)
- [Copyright, Licensing, and Cultural Permissions](#copyright-licensing-and-cultural-permissions)
- [Testing and Development](#testing-and-development)
- [Contribution Guidelines](#contribution-guidelines)
- [Project Roadmap](#project-roadmap)
- [License and Citation](#license-and-citation)

---

## Project Purpose and Objectives

**Tangkhul** (*Tangkhul Naga*) is a Tibeto-Burman language of the Tangkhulic branch, spoken primarily in the Ukhrul and Kamjong districts of Manipur, northeast India, and in contiguous areas of Myanmar. It possesses an exceptionally rich heritage of oral traditions, intricate weaving and folk songs, customary laws, proverbs (*Paotam*), and significant dialectal variation across dozens of ancestral villages.

The **Tangkhul Language Library** aims to:
1. **Preserve Tangkhul Language Resources**: Systematically catalogue, protect, and digitize linguistic assets across print publications, folk songs, dictionaries, oral narratives, cultural records, and creative literature.
2. **Connect Vocabulary to Source Material**: Bridge isolated lexical entries directly to verified bibliographic sources, page numbers, stanzas, and real-world textual contexts through a unified provenance model.
3. **Respect Dialectal Diversity**: Document village-level dialect variants and historical spelling shifts alongside standard Ukhrul orthography without destructive flattening.
4. **Provide Open Computational Tools**: Offer Python developers, linguists, and educators reliable, tested tools for text normalization, manifest validation, and corpus access.

---

## Current Project Status

> **Important Notice on Implementation Status**:
> This project has completed **Step 15: Tangkhul Audio Corpus, Pronunciation Records & Permission-Aware Speech Data Infrastructure** and holds **35 fully digitized books (741 pages, 261 chapters)**, **48 fully digitized songs (with bilingual lyrics and stanzas)**, **32 fully digitized cultural records (proverbs, seasonal festivals, feasts of merit, stone pottery, and architecture)**, **16 fully digitized dictionaries (with historical backgrounds, phonological frameworks, and representative bilingual/trilingual headwords)**, **32 fully digitized historical records (events, biographies, sacred toponyms, Makhel dispersal, and royal chronicles)**, and **41 fully digitized literature works (epic ballads, folktales, fables, lyric poetry, full-length plays, short stories, and canonical readers)**.
>
> - **Operational and Audited**:
>   - **Audio Corpus & Pronunciation Data Architecture (`src/tangkhul_lib/audio/`)**: Relational and FTS5 data models for audio recordings, multiple pronunciation variants per vocabulary entry, word- and segment-level timestamps, and speaker consent records.
>   - **Zero-Dependency Technical Audio Validation**: Built-in WAV header parser (duration, sample rate, channels, file size) via standard library `wave` module, with optional fallback to `mutagen` for compressed audio (`mp3`, `ogg`, `flac`, `m4a`).
>   - **Path Traversal & Checksum Security**: Strict path confinement (`safe_resolve_audio_path`), filename sanitization, and SHA-256 fingerprinting to prevent directory traversal and detect duplicate files idempotently.
>   - **Permission & Ethical Consent Governance (`AudioPermissionService`)**: Five explicit clearance tiers (`pending`, `authorized`, `restricted`, `withdrawn`, `needs_review`), immutable audit logging (`AudioConsentRecord`), consent revocation workflow, and automatic metadata shielding (`[RESTRICTED AUDIO FILE - ACCESS PRIVILEGED]`, `[SHIELDED SPEAKER]`).
>   - **Permission-Enforced Distribution (`export_corpus`)**: Excludes pending, unverified, restricted, and withdrawn recordings, generating verified `audio_manifest.jsonl`.
>   - **Audio Command Suite (`tangkhul audio`)**: Subcommands for `summary`, `list`, `inspect`, `validate`, `import`, `search`, `pronunciation`, `permissions`, and `export`.
>   - **Multi-Reviewer Consensus Engine (`tangkhul review`)**: Step 14 community consensus engine with independent approvals, review tasks, and shielded offline packages.
>   - **Vocabulary Enrichment Pipeline (`tangkhul enrich`)**: Step 13 source-backed lexicon enrichment pipeline.
>   - **Vocabulary Review Service (`VocabularyReviewService`)**: Step 12 review lifecycle with immutable audit logging.
>   - **Document Ingestion Pipeline (`tangkhul ingest`)**: Step 11 permission-aware ingestion across PDF, TXT/MD, and DOCX.
>   - **SQLite FTS5 Full-Text Search & Phonetics (`tangkhul vocab`)**: Multi-mode search (`substring`, `fulltext`, `fuzzy`, `phonetic`) with BM25 ranking.
>   - **Six Operational Domain Modules**: Books, Songs, Dictionaries, Culture, History, and Literature (217 catalogued records, 0 duplicates, 35 full books, 48 songs, 32 cultural records, 16 dictionaries, 32 historical records, 54 literature works).
>   - **Test Suite**: 307 automated tests passing with 100% lint compliance under `ruff`.



---

## Planned Domain Modules

The library is organized into six specialized domain modules:

| Module | Python Namespace | Manifest File | Intended Scope & Planned Capabilities |
|---|---|---|---|
| **Books** | `tangkhul_lib.books` | `data/manifests/books.jsonl` | Textbooks, grammar treatises, historical monographs, and literary books. Supports resource cataloguing, bibliographic validation, permitted plain-text extraction, and paragraph-level vocabulary linking. |
| **Songs** | `tangkhul_lib.songs` | `data/manifests/songs.jsonl` | Traditional folk songs (*Luira*, *Chumpha* festival songs), ceremonial chants, historical laments, religious hymns, and contemporary compositions. Preserves stanzas, line glosses, and poetic vocabulary. |
| **Dictionaries** | `tangkhul_lib.dictionaries` | `data/manifests/dictionaries.jsonl` | Tangkhul-English, Tangkhul-Manipuri, and multilingual dictionaries and wordlists. Ingests lemmas, glosses, parts of speech, and grammatical cross-references into the unified vocabulary database. |
| **Culture** | `tangkhul_lib.culture` | `data/manifests/culture.jsonl` | Proverbs (*Paotam*), customary maxims, festivals (*Luira Phanit*, *Chumpha*, *Mangkhap*, *Thisham*), material culture (traditional weaving like *Haora*, *Luirim*), and customary governance (*Hangva*). |
| **History** | `tangkhul_lib.history` | `data/manifests/history.jsonl` | Community chronicles, ancestral migration traditions (*Makhel* dispersal), historical toponyms (gazetteer of villages and peaks), historical figures, and language documentation history. |
| **Literature** | `tangkhul_lib.literature` | `data/manifests/literature.jsonl` | Traditional folk tales (*Khararchan*), mythological legends, oral narratives, poetry, riddles, and allegories. Links literary expressions to the central lexicon. |

---

## Folder Structure and Architecture

```
tangkhul-language-library/
├── README.md                           # Main project documentation and specifications
├── LICENSE                             # Project licensing terms (pending confirmation)
├── pyproject.toml                      # Modern packaging configuration (PEP 517/518/621)
├── .gitignore                          # Git ignore rules for caches, builds, and raw media
├── .editorconfig                       # Consistent cross-editor whitespace formatting
├── CONTRIBUTING.md                     # Cultural guidelines and developer contribution rules
├── CHANGELOG.md                        # Project change log (Keep a Changelog standard)
├── CITATION.cff                        # Citation metadata format
│
├── docs/                               # Detailed documentation suite
│   ├── index.md                        # Documentation entrypoint
│   ├── installation.md                 # Operating system installation steps
│   ├── quickstart.md                   # Quickstart guide
│   ├── architecture.md                 # System architecture overview
│   ├── data-sources.md                 # Data sources and provenance model
│   ├── data-model.md                   # Manifest and vocabulary schema definitions
│   ├── licensing-and-permissions.md    # Copyright and community sovereignty terms
│   ├── contributing-data.md            # Guidelines for submitting language data
│   └── modules/                        # Documentation for planned modules
│       ├── books.md
│       ├── songs.md
│       ├── dictionaries.md
│       ├── culture.md
│       ├── history.md
│       └── literature.md
│
├── src/                                # Source tree (PEP 517 src-layout)
│   └── tangkhul_lib/                   # Primary Python package
│       ├── __init__.py                 # Package version and top-level exports
│       ├── py.typed                    # Marker file for PEP 561 typing support
│       ├── core/                       # Core configuration and foundation
│       │   ├── __init__.py
│       │   ├── config.py               # Path discovery and library settings
│       │   ├── exceptions.py           # Standard library exception hierarchy
│       │   └── models.py               # ManifestRecord, VocabularyEntry, ProvenanceRecord
│       ├── vocabulary/                 # Unified vocabulary operations
│       │   ├── __init__.py
│       │   ├── search.py               # Vocabulary search interfaces (planned)
│       │   ├── normalization.py        # Non-destructive Unicode normalization
│       │   ├── deduplication.py        # Provenance-preserving deduplication
│       │   └── provenance.py           # Provenance tracking helpers
│       ├── books/                      # Books domain module scaffolding
│       │   └── __init__.py
│       ├── songs/                      # Songs domain module scaffolding
│       │   └── __init__.py
│       ├── dictionaries/               # Dictionaries domain module scaffolding
│       │   └── __init__.py
│       ├── culture/                    # Culture domain module scaffolding
│       │   └── __init__.py
│       ├── history/                    # History domain module scaffolding
│       │   └── __init__.py
│       ├── literature/                 # Literature domain module scaffolding
│       │   └── __init__.py
│       ├── storage/                    # Persistence layer
│       │   ├── __init__.py
│       │   ├── database.py             # SQLite connection management
│       │   └── repositories.py         # Repository pattern abstractions
│       ├── ingestion/                  # Data ingestion and verification
│       │   ├── __init__.py
│       │   ├── text_extraction.py      # Plain-text extraction interfaces (planned)
│       │   └── metadata_validation.py  # JSONL manifest schema validator
│       └── cli/                        # Command-line interface
│           └── __init__.py
│
├── data/                               # Data storage area (Git hygiene enforced)
│   ├── README.md                       # Data storage conventions and rules
│   ├── manifests/                      # JSON Lines resource catalogues
│   │   ├── books.jsonl
│   │   ├── songs.jsonl
│   │   ├── dictionaries.jsonl
│   │   ├── culture.jsonl
│   │   ├── history.jsonl
│   │   └── literature.jsonl
│   ├── raw/                            # Original permitted files (not committed)
│   │   ├── books/
│   │   ├── songs/
│   │   ├── dictionaries/
│   │   ├── culture/
│   │   ├── history/
│   │   └── literature/
│   ├── processed/                      # Extracted and normalized texts
│   ├── exports/                        # Public export files (CSV, TEI/XML)
│   └── database/                       # Local SQLite corpus database
│
├── scripts/                            # Operational utility scripts
│   ├── validate_manifests.py           # Validates all manifest .jsonl files
│   └── inspect_sources.py              # Non-destructive storage inspection
│
├── tests/                              # Pytest test suite
│   ├── conftest.py                     # Fixtures and test environment setup
│   ├── test_package_import.py          # Package and submodule import verification
│   ├── unit/                           # Unit tests
│   │   ├── test_config_and_models.py   # Models, paths, and deduplication logic
│   │   └── test_manifest_validation.py # JSONL schema validation tests
│   ├── integration/                    # Integration test scaffolding
│   └── fixtures/                       # Test data fixtures
│
└── .github/                            # CI/CD and GitHub templates
    ├── workflows/
    │   └── tests.yml                   # Matrix CI (Ubuntu, Windows, macOS on Python 3.10-3.12)
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## Installation Instructions

### Prerequisites
- Python `>= 3.10`
- Git

### Windows PowerShell

```powershell
# 1. Clone repository
git clone https://github.com/your-org/tangkhul-language-library.git
cd tangkhul-language-library

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\Activate.ps1

# 4. Install in editable mode
python -m pip install -e .

# 5. Install with development tools (pytest, ruff)
python -m pip install -e ".[dev]"
```

### Linux and macOS

```bash
# 1. Clone repository
git clone https://github.com/your-org/tangkhul-language-library.git
cd tangkhul-language-library

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install in editable mode
python3 -m pip install -e .

# 5. Install with development tools
python3 -m pip install -e ".[dev]"
```

---

## Quick-Start Example

The following code works with the components implemented in this foundation step:

```python
import tangkhul_lib
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.core.models import ManifestRecord, ProvenanceRecord, VocabularyEntry
from tangkhul_lib.vocabulary.deduplication import deduplicate_entries
from tangkhul_lib.vocabulary.normalization import normalize_unicode

# 1. Verify library version
print(f"Loaded Tangkhul Language Library v{tangkhul_lib.__version__}")

# 2. Inspect project paths
config = LibraryConfig.from_environment()
print(f"Data root: {config.paths.data_dir}")

# 3. Create and inspect a verified manifest record
book_manifest = ManifestRecord(
    id="BK-0001",
    resource_type="books",
    title="Tangkhul Folk Tales",
    year=1978,
    language="Tangkhul",
    permission_status="community_authorized",
    verification_status="verified",
)
print(f"Manifest record created: {book_manifest.id} -> {book_manifest.title}")

# 4. Create vocabulary items with explicit provenance
source_ref = ProvenanceRecord(
    source_id="BK-0001",
    resource_type="books",
    citation="Tangkhul Folk Tales (1978), p. 24",
    page_or_section="p. 24",
    context_sentence="Ava vashungra ngasoda khararchan maranli.",
)

word_entry = VocabularyEntry(
    id="VOCAB-00101",
    headword=normalize_unicode("khararchan"),
    meanings=["traditional folk tale", "ancestral story"],
    part_of_speech="noun",
    provenance=[source_ref],
    verification_status="verified",
)

# 5. Demonstrate provenance-preserving deduplication
# Distinct meanings or dialect variants are never discarded
merged_list = deduplicate_entries([word_entry])
print(f"Headword: {merged_list[0].headword}, Sources: {len(merged_list[0].provenance)}")

# 6. Query Tangkhul history catalogue and chronological timeline
from tangkhul_lib.history.catalogue import HistoryCatalogue

history_cat = HistoryCatalogue.load_from_manifest(
    config.paths.manifests_dir / "history.jsonl"
)
print(f"Total catalogued historical records: {len(history_cat)}")
timeline = history_cat.get_timeline(start_year=1890, end_year=1920)
for evt in timeline:
    print(f"  {evt.sort_year}: {evt.title} [{evt.record_type}]")
```

### Command-Line Interface (`tangkhul`)

```bash
# Books catalogue
tangkhul books --list
tangkhul books --search "Grammar"
tangkhul books --id BK-HIST-001

# Songs catalogue
tangkhul songs --list
tangkhul songs --type folk

# Dictionaries catalogue
tangkhul dictionaries --list
tangkhul dictionaries --id DIC-HIST-001

# Culture catalogue
tangkhul culture --list
tangkhul culture --category proverb
tangkhul culture --search "Luira"

# History catalogue & timeline
tangkhul history --list
tangkhul history --id HIST-EVT-001
tangkhul history --type person
tangkhul history --period "Colonial Era"
tangkhul history --place "Ukhrul"
tangkhul history --verification-status needs_review

# Literature catalogue
tangkhul literature --list
tangkhul literature --id LIT-POEM-001
tangkhul literature --type poem
tangkhul literature --type folk_tale
tangkhul literature --genre ballad
tangkhul literature --search "Tangkhul poetry"
tangkhul literature --author "Luingam"
tangkhul literature --verification-status needs_review

# Unified Vocabulary Search (Cross-Module across all six modules)
tangkhul vocab --search "khamor"
tangkhul vocab --exact "khararchan"
tangkhul vocab --meaning "custom"
tangkhul vocab --dialect "Ukhrul"
tangkhul vocab --source-type books
tangkhul vocab --source-type songs
tangkhul vocab --source-type dictionaries
tangkhul vocab --source-type culture
tangkhul vocab --source-type history
tangkhul vocab --source-type literature
tangkhul vocab --verification-status verified
tangkhul vocab --limit 20
tangkhul vocab --id VOC-BK-0001

# Document Ingestion Pipeline
tangkhul ingest --list-sources
tangkhul ingest --source-id BK-HIST-001 --file path/to/document.pdf --dry-run
tangkhul ingest --search "ngashan" --limit 5

# Vocabulary Review & Validation Workflow
tangkhul review --list --status pending_review
tangkhul review --show VOCAB-CAND-001
tangkhul review --accept VOCAB-CAND-001 --reviewer "Elder-Khangam" --meaning "traditional custom"

# Authorized Vocabulary Enrichment (Step 13)
tangkhul enrich --list-sources --source-type dictionaries
tangkhul enrich --preview path/to/lexicon.tsv
tangkhul enrich --source-id DIC-HIST-001 --file path/to/lexicon.tsv --dry-run
tangkhul enrich --source-id DIC-HIST-001 --file path/to/lexicon.tsv --show-duplicates
tangkhul enrich --source-id DIC-HIST-001 --file path/to/lexicon.tsv --export-candidates data/review/candidates.jsonl
```

---

## Unified Vocabulary Database Design

Vocabulary in this library is designed not as isolated lists, but as an interconnected knowledge network spanning all six domain modules.

```
┌─────────────────────────────────────────────────────────────┐
│                   Unified Vocabulary Entry                  │
│                                                             │
│  - Headword (Original Tangkhul spelling, Unicode NFC)       │
│  - Meanings & Definitions (Tangkhul glosses)                │
│  - English Translations                                     │
│  - Alternative Spellings (Orthographic variants)            │
│  - Dialect Variants (e.g., Ukhrul, Hundung, Phadang, etc.)  │
│  - Part of Speech & Pronunciation (where recorded)          │
│  - Contextual Example Sentences                             │
│  - Verification Status & Licensing Constraints              │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐┌──────────────────────────────┐
│     Provenance Record 1      ││     Provenance Record 2      │
│ - Source: BK-0001 (Books)    ││ - Source: SNG-0004 (Songs)   │
│ - Citation: Pettigrew, p. 45 ││ - Citation: Luira Song St. 2 │
│ - Context Sentence           ││ - Context Sentence           │
└──────────────────────────────┘└──────────────────────────────┘
```

### Core Design Rules
1. **Preserve Authentic Orthography**: Never silently strip diacritics, tones, or glottal indicators.
2. **Preserve Dialectal Nuance**: Words from different villages or historical periods must retain their dialect tag. Similar spellings must not be assumed to be identical words without verification.
3. **Strict Non-Destructive Deduplication**: When merging records:
   - Identical words with different meanings are kept as distinct entries.
   - Identical words with the same meaning merge their provenance lists, ensuring that every citing source is documented.

---

## Resource Manifest Schema

Every catalogued asset is recorded as a JSON object on a single line in a `.jsonl` file in `data/manifests/`.

### Schema Specification

```json
{
  "id": "BK-0001",
  "resource_type": "books",
  "title": "Tangkhul Naga Grammar and Dictionary",
  "title_translation": "Tangkhul Naga Grammar and Dictionary",
  "creator": "Pettigrew, William",
  "year": 1918,
  "publisher": "Assam Secretariat Printing Office",
  "language": "Tangkhul",
  "dialect": "Ukhrul Standard",
  "source_url": "https://archive.org/details/tangkhulnagagram00pettgoog",
  "source_identifier": "OCLC: 504518280",
  "license": "Public Domain",
  "permission_status": "public_domain",
  "local_path": "data/raw/books/tangkhul_grammar_1918.pdf",
  "verification_status": "verified",
  "notes": "Historical grammatical reference and vocabulary."
}
```

### Allowed Enum Values
- **`resource_type`**: `books`, `songs`, `dictionaries`, `culture`, `history`, `literature`.
- **`permission_status`**: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`.
- **`verification_status`**: `unverified`, `partially_verified`, `verified`, `community_reviewed`.

---

## Data Sources and Provenance

- **Historical Sources**: 19th- and early 20th-century linguistic surveys and publications (e.g., William Pettigrew 1918, Grierson's Linguistic Survey of India Vol. III Part III).
- **Community Literature**: Works published by Tangkhul literature committees, educational texts, and local publications with appropriate permissions.
- **Oral Tradition & Fieldwork**: Folk songs and proverbs transcribed directly from community knowledge-bearers with informed consent.
- **Scholarly Studies**: Academic linguistic documentation on Tangkhulic phonetics, tone systems, and syntax.

---

## Data Quality and Verification

Every catalogued record and vocabulary entry passes through verification tiers:
1. **Unverified**: Raw extracted entry awaiting linguistic review.
2. **Partially Verified**: Bibliographic citation and spelling confirmed against source text.
3. **Verified**: Cross-checked by a language researcher against source context and orthographic conventions.
4. **Community Reviewed**: Approved by native Tangkhul language speakers and cultural custodians.

---

## Data Storage Conventions and Git Hygiene

To protect copyright and respect community ownership:
1. **Separation of Metadata and Media**:
   - Manifest files (`data/manifests/*.jsonl`) are version-controlled in Git.
   - Large raw source files (PDFs, audio recordings, scans) live in `data/raw/` and are strictly excluded from Git via `.gitignore`.
2. **No Fabricated Records**: Manifests and raw folders are not populated with placeholder data or invented books/songs. Real items are added only during verified ingestion phases.
3. **Local Databases**: SQLite database files (`data/database/*.sqlite`) are excluded from Git to prevent repository bloat and merge collisions.

---

## Copyright, Licensing, and Cultural Permissions

1. **Software Tooling**: Repository code and automation scripts are created for non-commercial linguistic preservation. Official open-source licensing terms are pending confirmation by community stakeholders.
2. **Cultural Heritage Sovereignty**: Tangkhul proverbs, songs, oral histories, and cultural traditions are the cultural and intellectual property of the Tangkhul community.
3. **Non-Commercial Research**: All catalogued data is intended strictly for non-commercial educational, linguistic, and cultural preservation purposes. Commercial exploitation is prohibited without community consent.

---

## Testing and Development

The repository contains automated tests and code-quality checks.

### Running Pytest
```bash
python -m pytest
```

### Running Ruff (Linter and Formatter)
```bash
python -m ruff check .
```

### Validating Manifests
```bash
python scripts/validate_manifests.py
```

### Inspecting Sources and Storage
```bash
python scripts/inspect_sources.py
```

---

## Contribution Guidelines

We welcome contributions from linguists, developers, and native Tangkhul speakers!
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for code standards and cultural principles.
- Use the issue templates in `.github/ISSUE_TEMPLATE/` for reporting bugs or proposing resources.
- Ensure all tests pass (`python -m pytest`) and linter checks succeed (`python -m ruff check .`) before submitting a pull request.

---

## Project Roadmap

- [x] **Step 1: Project Architecture and Packaging**
  - Package structure, `pyproject.toml`, core data models, manifest validator, initial test suite, and complete documentation.
- [x] **Step 2: Tangkhul Books Catalogue & Vocabulary Extraction**
  - Books domain module, verified manifest records, deduplication, and extraction pipelines.
- [x] **Step 3: Tangkhul Songs Catalogue & Musical Heritage Integration**
  - Songs module, folk and contemporary recordings, stanza/line parsing, and poetic vocabulary.
- [x] **Step 4: Tangkhul Dictionaries Module & Lexicographical Database**
  - Historical and contemporary dictionaries, headword normalization, multilingual definitions, and conflict detection.
- [x] **Step 5: Tangkhul Culture, Customs, Traditions & Proverbs Module**
  - Cultural catalogue, proverbs (*Paotam* / *Chanjam*), festivals, customs, rituals, and consent-gated extraction.
- [x] **Step 6: Tangkhul History Module & Chronological Timeline Integration**
  - Historical events, people, places, migrations, timelines, and toponym harvesting with approximate date support.
- [x] **Step 7: Tangkhul Literature Module & Unified Language Archive Integration**
  - Poetry, short stories, folk tales (*Khararchan*), drama (*Shongza*), riddles (*Paochirun*), and early prose translations.
- [x] **Step 10: Full-Text Search (FTS5), Phonetic Matching & Unified Lexical Index**
  - SQLite FTS5 integration, Soundex/Metaphone-adapted phonetic indexing, cross-domain querying, and provenance tracing.
- [x] **Step 11: Dialectal Harmonization & Cross-Village Linguistic Alignment**
  - Village-level dialect mapping, phonetic shift rules, multi-village lexical variants, and non-flattening harmonization.
- [x] **Step 12: Native-Speaker Review Workflow & Lexicon Verification**
  - Verification states (`pending`, `verified`, `needs_review`, `disputed`), reviewer attribution, and audit logs.
- [x] **Step 13: Authorized Vocabulary Expansion & Source-Backed Lexicon Enrichment**
  - Source-backed enrichment pipelines, citation-linked vocabulary expansion, and dialect-aware harvesting.
- [x] **Step 14: Native-Speaker Validation, Multi-Reviewer Consensus & Community Governance**
  - Multi-reviewer consensus algorithms, quorum requirements, dispute arbitration, and offline review package generation.
- [x] **Step 15: Tangkhul Audio Corpus, Pronunciation Records & Permission-Aware Speech Data Infrastructure** *(Current)*
  - Relational & FTS5 audio corpus schema, pronunciation variant linkage, zero-dependency audio validation, ethical consent state machine, metadata masking, and permission-enforced export engine.

---

## License and Citation

### License
The open-source license for this repository is currently **Pending Community Confirmation**. Please refer to [LICENSE](LICENSE) and [docs/licensing-and-permissions.md](docs/licensing-and-permissions.md) for details.

### Citation
If you use this library or data architecture in your research, please cite:

```bibtex
@software{tangkhul_language_library_2026,
  title        = {Tangkhul Language Library: A Modular Python Toolkit for Tangkhul Language Preservation and Linguistic Research},
  author       = {{Tangkhul Language Preservation Project Contributors}},
  year         = {2026},
  version      = {0.1.0-dev},
  url          = {https://github.com/your-org/tangkhul-language-library}
}
```
See also [CITATION.cff](CITATION.cff).
#   t a n g k h u l - l a n g u a g e - l i b r a r y  
 