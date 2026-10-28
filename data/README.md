# Data Storage Conventions and Hygiene

This directory contains data structures, manifests, raw sources, and database files for the **Tangkhul Language Library**.

---

## Directory Organization

```
data/
├── README.md                   # This convention guide
├── manifests/                  # JSON Lines (.jsonl) cataloguing resource metadata
│   ├── books.jsonl
│   ├── songs.jsonl
│   ├── dictionaries.jsonl
│   ├── culture.jsonl
│   ├── history.jsonl
│   └── literature.jsonl
├── raw/                        # Original permitted source files (NOT committed to git)
│   ├── books/
│   ├── songs/
│   ├── dictionaries/
│   ├── culture/
│   ├── history/
│   └── literature/
├── processed/                  # Normalized texts and extracted plain-text corpora
├── exports/                    # Exported datasets (CSV, JSON, TEI/XML)
├── review/                     # Offline review exchange JSONL candidates (shielded)
└── database/                   # Local SQLite databases (tangkhul_corpus.sqlite)
```

---

## Storage & Hygiene Rules

1. **Manifests vs. Sources**:
   - `data/manifests/` contains **metadata only** formatted as JSON Lines (`.jsonl`). Each line is a self-contained JSON object recording identity, bibliographic provenance, permissions, and verification status.
   - Large digital source files (PDF scans, audio recordings, EPUBs) live in `data/raw/` and are **never committed to Git**.

2. **Copyright & Permissions**:
   - Do not commit copyrighted books, commercial recordings, or proprietary song collections to this repository.
   - Public accessibility of a URL does not imply permission to download or redistribute.
   - Resources must declare explicit `permission_status` (`permitted`, `public_domain`, `community_authorized`, or `restricted`) before inclusion in ingestion pipelines.

3. **No Fabricated Data**:
   - In accordance with linguistic integrity standards, manifest files are not pre-populated with synthetic or placeholder entries. Actual historical publications, verified dictionary editions, and community-attested songs will be added during designated ingestion phases.

4. **Git Tracking**:
   - `data/raw/`, `data/database/*.sqlite`, and temporary exports are excluded by `.gitignore`.
   - `.gitkeep` markers ensure directory presence without committing unverified or copyright-restricted payloads.

5. **Vocabulary Enrichment Hygiene (Step 13)**:
   - Candidate vocabulary files imported via `tangkhul enrich` must correspond to a verified, authorized manifest record (`public_domain`, `permitted`, or `community_authorized`).
   - Content from `restricted` (modern copyrighted publications) or `pending` sources cannot be extracted into the vocabulary corpus.
   - Candidate exports in `data/review/` automatically shield and mask restricted context sentences (`[RESTRICTED TEXT - ACCESS PRIVILEGED]`) to prevent unauthorized leakage.

