# Dictionaries Module (`tangkhul_lib.dictionaries`)

The **Dictionaries** module is a core domain package in the Tangkhul Language Library. It provides structured bibliographic cataloguing for historical and modern Tangkhul dictionaries, glossaries, and wordlists; permission-enforcing entry extraction; duplicate and lexical conflict detection; and deep integration with the library's unified vocabulary database.

---

## 1. Module Purpose & Objectives

The lexicographical tradition of the Tangkhul language spans more than 160 years, beginning with Major M. McCulloch's 1859 wordlist, Rev. William Pettigrew's foundational 1918 *Tangkhul Naga Grammar and Dictionary*, mid-20th-century linguistic surveys (D.N.S. Bhat 1969), institutional multilingual lexicons (Nagaland Bhasha Parishad 1975, CIIL 1995), and authoritative community dictionaries produced by the Tangkhul Literature Society (N. Luikham 1997).

The primary objectives of `tangkhul_lib.dictionaries` are:
1. **Source Preservation & Cataloguing**: Systematically catalogue authentic Tangkhul dictionaries, trilingual glossaries, and comparative dialect wordlists with verified bibliographic metadata in [`data/manifests/dictionaries.jsonl`](file:///f:/tangkhul-language-library/data/manifests/dictionaries.jsonl).
2. **Permission-Governed Extraction**: Ingest lexical entries from authorized public domain or community-permitted sources while strictly blocking unauthorized extraction from modern in-copyright works (`metadata_only`).
3. **Unified Vocabulary Database Integration**: Connect extracted headwords and senses to the shared [`VocabularyRepository`](file:///f:/tangkhul-language-library/src/tangkhul_lib/storage/repositories.py) alongside vocabulary harvested from books and songs, maintaining full multi-source provenance.
4. **Dialect and Variant Preservation**: Preserve village dialect variants, phonetic transcriptions, and historical orthographies without destructive flattening or treating variations as errors.
5. **Conflict & Polysemy Resolution**: Distinguish genuine polysemous senses from duplicates, and flag conflicting definitions or spellings across different lexicographers for expert review.

---

## 2. Catalogue Schemas

### Dictionary Source Schema (`DictionarySourceRecord`)

Each dictionary resource in [`data/manifests/dictionaries.jsonl`](file:///f:/tangkhul-language-library/data/manifests/dictionaries.jsonl) implements [`DictionarySourceRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/dictionaries/models.py):

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Stable unique identifier (e.g. `DIC-HIST-001`, `DIC-TLS-001`). Required. |
| `title` | `str` | Full title of the dictionary as published. Required. |
| `alternate_titles` | `list[str]` | Subtitles, phonetic titles, or translations. |
| `authors` | `list[str]` | Authors or primary lexicographers. |
| `editors` | `list[str]` | Editors or editorial board members. |
| `compiler` | `str \| None` | Primary compiler if designated. |
| `contributors` | `list[str]` | Native informants, translators, or consultants. |
| `publisher` | `str \| None` | Publishing agency or press. |
| `publication_place` | `str \| None` | City/place of publication. |
| `publication_year` | `int \| None` | Year of publication (e.g. `1918`, `1997`). |
| `edition` | `str \| None` | Edition designation (e.g. `First Edition`). |
| `languages` | `list[str]` | List of languages covered (default: `["Tangkhul"]`). |
| `language_pair` | `str \| None` | Direction/pairing (e.g. `Tangkhul-English`, `Tangkhul-English-Hindi`). |
| `dialect` | `str \| None` | Dialect variety documented (e.g. `Ukhrul`, `Hunphun`, `Multidialectal`). |
| `source_type` | `str` | One of: `dictionary`, `bilingual_dictionary`, `multilingual_dictionary`, `glossary`, `wordlist`, `grammar_dictionary`. |
| `isbn` | `str \| None` | ISBN or standard identifier. |
| `identifier` | `str \| None` | Archival identifier (e.g. `Glottolog:pett1918tang`). |
| `source_url` | `str \| None` | Canonical repository link or digital landing page. |
| `local_file_path` | `str \| None` | Relative path to local authorized copy. |
| `license` | `str \| None` | License terms (e.g. `Public Domain`, `Copyright TLS`). |
| `license_evidence` | `str \| None` | Factual basis for license classification. |
| `permission_status` | `str` | One of: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`. |
| `access_status` | `str` | One of: `metadata_only`, `full_text_available`, `restricted`, `open_access`, `unknown`. |
| `verification_status` | `str` | One of: `verified`, `needs_review`, `partially_verified`, `unverified`, `community_reviewed`. |
| `notes` | `str \| None` | Lexicographical background and bibliographic notes. |

### Dictionary Entry Schema (`DictionaryEntryRecord`)

Individual headwords and lemmas extracted from permitted dictionaries implement [`DictionaryEntryRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/dictionaries/models.py):

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique entry ID (e.g. `DIC-HIST-001-ENT-0001`). Required. |
| `dictionary_id` | `str` | Stable ID of the source dictionary. Required. |
| `headword` | `str` | Tangkhul headword exactly as printed. Required. |
| `normalized_headword` | `str` | Search form (Unicode NFC, lowercase, normalized). |
| `alternate_spellings` | `list[str]` | Alternate spellings or dialect variations listed in source. |
| `transliteration` | `str \| None` | Romanized or phonetic transliteration. |
| `definitions_en` | `list[str]` | English definitions and glosses. |
| `definitions_hi` | `list[str]` | Hindi definitions and glosses. |
| `other_definitions` | `list[str]` | Definitions in Manipuri (Meiteilon) or other languages. |
| `part_of_speech` | `str \| None` | Grammatical class (`noun`, `verb`, `adjective`, `adverb`, `particle`, etc.). |
| `pronunciation` | `str \| None` | Phonemic transcription or tonal notation. |
| `notes` | `str \| None` | Usage notes, cultural context, or etymology. |
| `examples` | `list[str]` | Illustrative sentences or phrases from source. |
| `dialect` | `str \| None` | Documented dialect variety. |
| `grammatical_info` | `str \| None` | Conjugation class, inflection, or affixation rules. |
| `page_or_section` | `str \| None` | Exact page number or printed entry locator (e.g. `p. 320`). |
| `entry_number` | `str \| None` | Printed entry index or section number. |
| `source_excerpt` | `str \| None` | Verbatim short excerpt from the original dictionary. |
| `extraction_method` | `str` | e.g. `tabular_import`, `text_line_parser`, `manual_entry`. |
| `confidence` | `float` | Extraction confidence score (`0.0` to `1.0`). |
| `license` | `str \| None` | Licensing terms governing this entry. |
| `permission_status` | `str` | Permission tier (`public_domain`, `permitted`, etc.). |
| `verification_status` | `str` | Verification state (`verified`, `needs_review`). |
| `vocabulary_id` | `str \| None` | Foreign key linking to unified `vocabulary_entries.id`. |

---

## 3. Researched Tangkhul Dictionary Sources

The catalogue in [`data/manifests/dictionaries.jsonl`](file:///f:/tangkhul-language-library/data/manifests/dictionaries.jsonl) contains **16 authentic dictionary, glossary, and comparative lexicon sources**:
- **Verified Sources**: 15 records
- **Needs Review / Candidate Sources**: 1 record

| ID | Title | Authors / Compilers | Year | Language Pair | Status | Access |
|---|---|---|---|---|---|---|
| `DIC-HIST-003` | Comparison of Indo-Chinese Languages | Nathan Brown, Capt. George Gordon | 1837 | Tangkhul-English | Verified | Full Text (Public Domain) |
| `DIC-HIST-002` | Vocabulary of the Luhuppa (Tangkhul) Language | Major M. McCulloch | 1859 | Tangkhul-English | Verified | Full Text (Public Domain) |
| `DIC-HIST-004` | Tangkhul and Luhuppa Wordlist | G. H. Damant | 1880 | Tangkhul-English | Verified | Full Text (Public Domain) |
| `DIC-LSI-001` | Linguistic Survey of India: Tangkhul Wordlist | Sir George A. Grierson | 1903 | English-Tangkhul | Verified | Full Text (Public Domain) |
| `DIC-HIST-005` | Comparative Vocabulary of Naga Tribes of Manipur | T. C. Hodson | 1911 | Tangkhul-English | Verified | Full Text (Public Domain) |
| `DIC-HIST-001` | Tangkhul Naga Grammar and Dictionary | Rev. William Pettigrew | 1918 | Tangkhul-English | Verified | Full Text (Public Domain) |
| `DIC-DC-001` | Tankhur Naga Vocabulary | D. N. S. Bhat | 1969 | Tangkhul-English | Verified | Metadata Only (Copyright DC) |
| `DIC-SOAS-001` | Classification of the Naga Languages (Lexicon) | G. E. Marrison | 1967 | Tangkhul-English | Verified | Full Text (Educational) |
| `DIC-WUNG-001` | Tangkhul (Wung) Dictionary | T. Luikham | 1974 | Tangkhul-English | Verified | Metadata Only (Copyright TLS) |
| `DIC-NBP-001` | Hindi-Tangkhul Dictionary | B. B. Kumar, H. P. Rai, Pearson, Somi | 1975 | Hindi-Tangkhul | Verified | Metadata Only (Copyright NBP) |
| `DIC-CIIL-002` | CIIL Tangkhul Lexical Survey & Audio Lexicon | S. Arokianathan | 1982 | Tangkhul-English | Verified | Metadata Only (Copyright CIIL) |
| `DIC-CIIL-001` | Tangkhul-English-Hindi Dictionary | Rekha Sharma, S. Arokianathan, E. Annamalai | 1995 | Tangkhul-English-Hindi | Verified | Metadata Only (Copyright CIIL) |
| `DIC-TLS-002` | Tangkhul Tui | Tangkhul Literature Society | 1995 | Tangkhul | Verified | Metadata Only (Copyright TLS) |
| `DIC-TLS-001` | Tangkhul Tui Dictionary | N. Luikham | 1997 | Tangkhul-English | Verified | Metadata Only (Copyright TLS) |
| `DIC-STEDT-001` | Comparative Tangkhul & Proto-Tangkhulic Lexicon | David R. Mortensen | 2003 | Tangkhul-English | Verified | Full Text (CC-BY-NC 4.0) |
| `DIC-CAND-001` | Comparative Tangkhul Dialect Glossary | Tangkhul Dialect Documentation Project | 2018 | Tangkhul Dialects-English | Needs Review | Metadata Only (Review Pending) |

---

## 4. Permission Governance & Legal Safeguards

The Dictionaries Module enforces strict copyright boundaries:
1. **Public Domain Threshold**: Works published before 1925 (McCulloch 1859, Grierson 1903, Pettigrew 1918) are verified as public domain in India and the United States. Digital text extraction and vocabulary synchronization are fully enabled for these works.
2. **Modern Copyright Protection**: In-copyright dictionaries (N. Luikham 1997, CIIL 1995, Nagaland Bhasha Parishad 1975) are catalogued as `access_status="metadata_only"` and `permission_status="restricted"`. Attempting text or entry extraction raises [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py).
3. **Export Filtering**: When exporting entries via `export_entries_jsonl()` or `export_entries_csv()`, restricted entries are automatically omitted unless `permitted_only=False` is explicitly set with administrative authorization.

---

## 5. Unified Vocabulary Integration

The dictionary module enriches the existing shared [`VocabularyRepository`](file:///f:/tangkhul-language-library/src/tangkhul_lib/storage/repositories.py) instead of creating a disconnected lexicon:

```
[Book Extraction]      [Song Lyrics Extraction]      [Dictionary Extraction]
  (BK-TLS-007, p. 15)    (SNG-TRAD-001, Stanza 1)      (DIC-HIST-001, p. 320)
           \                       |                       /
            \                      |                      /
             v                     v                     v
   +--------------------------------------------------------------+
   |          Unified VocabularyEntry (e.g. "khararchan")          |
   |  - headword: "khararchan"                                    |
   |  - meanings: ["story of ancestors", "folk-tale", "legend"]   |
   |  - translations_en: ["ancestral story", "folk-tale"]         |
   |  - part_of_speech: "noun"                                    |
   |  - provenance:                                               |
   |      1. BK-TLS-007 (books) - Tangkhul Tuitam, p. 15          |
   |      2. DIC-HIST-001 (dictionaries) - Pettigrew (1918), p.320|
   +--------------------------------------------------------------+
```

### Key Integration Invariants:
1. **Non-Destructive Senses**: Distinct definitions from dictionaries are appended to the existing word entry without deleting definitions harvested from textbooks or songbooks.
2. **Multi-Source Provenance**: Each entry preserves full provenance tracking linking to `source_id`, `resource_type="dictionaries"`, exact page citations (`page_or_section="p. 320"`), and example sentences.
3. **Spelling & Dialect Variations**: Variants such as *ngashan* vs. *ngashān* are maintained with explicit source attribution and flagged via `catalogue.find_conflicts()` for lexicographical review.

---

## 6. CLI Usage Guide

The CLI exposes dictionary catalogue queries through the `tangkhul dictionaries` subcommand:

### List All Catalogued Dictionaries
```bash
tangkhul dictionaries --list
```

### Search by Title, Author, or Keyword
```bash
tangkhul dictionaries --search "Pettigrew"
tangkhul dictionaries --search "Hindi"
```

### Display Detailed Metadata for a Dictionary ID
```bash
tangkhul dictionaries --id DIC-HIST-001
tangkhul dictionaries --id DIC-TLS-001
```

### Search Lexical Entry by Headword
```bash
tangkhul dictionaries --entry "khararchan"
tangkhul dictionaries --entry "khamatha"
```

### Filter by Author, Language Pair, Dialect, or Verification Status
```bash
tangkhul dictionaries --author "Luikham"
tangkhul dictionaries --language-pair "Tangkhul-English"
tangkhul dictionaries --dialect "Ukhrul"
tangkhul dictionaries --verification-status "needs_review"
```

---

## 7. Adding New Dictionary Records

1. **Verify Bibliographic Details**: Confirm title, authors, publisher, publication year, and language coverage using authoritative catalogues (Bharatavani, CIIL, Glottolog, Library of Congress).
2. **Assess Copyright & Permissions**:
   - Out of copyright (published before 1925): `permission_status="public_domain"`, `access_status="full_text_available"`.
   - Modern publication without written permission: `permission_status="restricted"`, `access_status="metadata_only"`.
   - Fieldwork with community agreement: `permission_status="community_authorized"`.
3. **Append to Manifest**: Add the validated JSON line to [`data/manifests/dictionaries.jsonl`](file:///f:/tangkhul-language-library/data/manifests/dictionaries.jsonl).
4. **Validate & Test**:
   ```bash
   python scripts/validate_manifests.py
   pytest
   ruff check .
   ```

---

## 8. Vocabulary Enrichment & Candidate Expansion (Step 13)

Under Step 13, the dictionary extraction capabilities are integrated with the unified vocabulary enrichment pipeline:
- **Eligible Extraction**: Authorized public-domain dictionaries (`DIC-HIST-001` Pettigrew 1918, `DIC-LSI-001` Grierson 1903, `DIC-HIST-002` McCulloch 1859) can be ingested from structured files (TSV, CSV, JSONL) or formatted text lines (`headword (pos.) : definition`).
- **Permission Safeguards**: Modern in-copyright dictionaries (`DIC-TLS-001` Luikham 1997, `DIC-CIIL-001` Sharma et al. 1995, `DIC-NBP-001` 1975, `DIC-DC-001` Bhat 1969) remain strictly protected as `metadata_only`.
- **Lexical Quality & Categorization**: Extracted entries are classified into 16 grammatical and semantic domains (nouns, verbs, adjectives, numbers, family, agriculture, tools, etc.), with empty categories clearly highlighted as data gaps.
- **Deduplication & Provenance**: Duplicate candidates generate suggestions via phonetic and Levenshtein similarity rather than automatic merging.
- **CLI Commands**:
  ```bash
  tangkhul enrich --list-sources --source-type dictionaries
  tangkhul enrich --preview --source-id DIC-HIST-001 --file data/raw/dictionaries/pettigrew.tsv
  tangkhul enrich --source-id DIC-HIST-001 --file data/raw/dictionaries/pettigrew.tsv --dry-run
  tangkhul enrich --source-id DIC-HIST-001 --file data/raw/dictionaries/pettigrew.tsv --show-duplicates
  ```

---

## 9. Digital Exports & Lexicographical Compendium

The entire Tangkhul lexicographical catalogue is digitized and exported across multiple open formats:

1. **Consolidated JSON Datasets**:
   - [`data/exports/dictionaries.json`](file:///f:/tangkhul-language-library/data/exports/dictionaries.json): Complete machine-readable collection of all 10 dictionaries with full metadata, historical backgrounds, phonological frameworks, and representative lexical entries.
   - [`src/tangkhul_lib/data/dictionaries.json`](file:///f:/tangkhul-language-library/src/tangkhul_lib/data/dictionaries.json): Synchronized internal package distribution.

2. **Master PDF Compendium**:
   - [`data/exports/dictionaries.pdf`](file:///f:/tangkhul-language-library/data/exports/dictionaries.pdf): An 11-page formatted anthology comprising a cover page with Table of Contents and dedicated structured pages for each of the 10 dictionaries.

3. **Individual Resource Exports**:
   - [`data/exports/dictionaries/`](file:///f:/tangkhul-language-library/data/exports/dictionaries): Contains 20 standalone documents (10 JSON files and 10 individual PDF documents) matching each dictionary identifier (`DIC-HIST-001` through `DIC-CAND-001`).

4. **Raw Structured Text Files**:
   - [`data/raw/dictionaries/`](file:///f:/tangkhul-language-library/data/raw/dictionaries): Contains 10 contiguous UTF-8 text files documenting bibliographic overviews, orthography notes, and line-indexed representative headwords with English/Hindi definitions and contextual sentences.


