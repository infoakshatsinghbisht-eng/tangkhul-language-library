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
