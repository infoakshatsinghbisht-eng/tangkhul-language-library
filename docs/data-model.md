# Data Model and Schema Specification

This document details the data structures and schemas used across the Tangkhul Language Library.

---

## 1. Resource Manifest Schema (`.jsonl`)

Manifest files in `data/manifests/` follow the JSON Lines format, where each line is an independent JSON object conforming to the `ManifestRecord` schema:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | Yes | Unique stable identifier (e.g., `BK-0001`, `SNG-0002`). |
| `resource_type` | `string` | Yes | One of: `books`, `songs`, `dictionaries`, `culture`, `history`, `literature`. |
| `title` | `string` | Yes | Primary title in Tangkhul or original language. |
| `title_translation` | `string` | No | English translation of the title. |
| `creator` | `string` | No | Author, compiler, singer, or community contributor. |
| `year` | `integer` | No | Year of publication or primary recording. |
| `publisher` | `string` | No | Publisher, issuing society, or organization. |
| `language` | `string` | Yes | Default: `Tangkhul`. |
| `dialect` | `string` | No | Dialect variety (e.g., `Ukhrul Standard`, `Hundung`, `Phadang`, `Tusom`). |
| `source_url` | `string` | No | Canonical link or archival record URL. |
| `source_identifier` | `string` | No | ISBN, DOI, call number, or library catalog ID. |
| `license` | `string` | No | Specific license if known (e.g., `Public Domain`, `CC-BY-NC-4.0`). |
| `permission_status` | `string` | Yes | One of: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`. |
| `local_path` | `string` | No | Relative path to local file inside `data/raw/` (uncommitted). |
| `verification_status` | `string` | Yes | One of: `unverified`, `partially_verified`, `verified`, `community_reviewed`. |
| `notes` | `string` | No | Contextual notes, digitization history, or permissions context. |

---

## 2. Unified Vocabulary Entry Schema

The `VocabularyEntry` dataclass represents a unified word entry synthesized from multiple sources:

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

## 3. Provenance Record Schema

```python
@dataclass
class ProvenanceRecord:
    source_id: str                        # Reference to manifest `id`
    resource_type: str                    # Module type
    citation: str                         # Human-readable bibliographic citation
    page_or_section: str | None           # Page, stanza, or chapter
    context_sentence: str | None          # Sentence in which word occurred
    recorded_year: int | None             # Year source was published/recorded
    permission_status: str                # Legal/community status
```
