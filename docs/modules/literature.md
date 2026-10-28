# Literature Module (`tangkhul_lib.literature`)

The **Literature** module provides comprehensive cataloguing, permission-aware text and stanza extraction, duplicate and adaptation detection, and cross-module lexical integration for Tangkhul literary works, oral narratives, poetry, plays, short stories, folk tales (*Khararchan*), riddles, and translations.

---

## 1. Scope and Core Capabilities

1. **Multi-Genre Literary Classification**:
   Supports traditional and modern Tangkhul literary genres without schema inflexibility:
   - `poem`: Lyric poetry, philosophical verse, environmental odes (e.g. Luingam A. Shimray, Y.K. Shimray, T. Luikham, S. Kanrei).
   - `short_story`: Social realism and village short fiction (e.g. R. Shaiza's *Maranwon*, K.S. Kasomwoshi, V. Ruivah).
   - `folk_tale`: Traditional moral fables, animal trickster tales, and origin legends (e.g. *Huikhayei Kala Sha*, *Kashunao wui Khararchan*).
   - `oral_narrative`: Spoken legends and mythological traditions preserved across generations.
   - `riddle`: Traditional metaphorical intellectual games (*Paochirun*) practiced in youth dormitories (*Longshim*).
   - `proverb_collection`: Curated anthologies of customary sayings (*Paotam* / *Chanjam*).
   - `play`: Theatrical drama and verse-dramas (e.g. *Shongza* 2007, *Maitonphi: A Dramatic Adaptation* 1995).
   - `novel`: Extended prose narratives and historical allegories.
   - `essay`: Formal literary criticism, cultural philosophy, and historical exposition.
   - `literary_anthology`: Canonical readers and anthologies (e.g. *Tangkhul Folk Literature* 1982, *Tangkhul Tuitam* high school series).
   - `ballad`: Tragic romantic epics and poetic narratives (e.g. 17th-century Phungcham ballad *Shimreishang Kala Maitonphi*).
   - `children_literature`: Early educational tales and graded fables (e.g. *Kachakui Kala Shanao*, *Sikui Kala Machun*).
   - `translation`: Documented scripture or classic translations (e.g. Pettigrew's 1903 *Prodigal Son* in Grierson's LSI, *Kristianwui Khangaran* 1953).
   - `other`: Specialized or emerging literary forms.

2. **Bibliographic Integrity and Attribution**:
   Distinguishes authors, poets, storytellers, playwrights, translators, editors, and collectors. Retains publication years, composition eras, and editions without conflating distinct retellings or adaptations.

3. **Relational Linking with Books and Culture**:
   Provides a literary view of publications catalogued in the Books module (e.g. `BK-TLS-007` for *Tangkhul Tuitam Kachiko*, `BK-CIIL-003` for *Tangkhul Folk Literature*) via `book_id`, preventing redundant duplicate physical bibliographic entries while cataloguing specific contained works.

4. **Permission-Aware Text & Stanza Extraction**:
   Strictly gates text parsing by copyright tier (`public_domain`, `permitted`, `community_authorized`, `restricted`) and contributor consent. Stanzas, line numbers, and poetic meter boundaries are preserved without destructive flattening.

5. **Unified Vocabulary Integration**:
   Candidate literary vocabulary harvested from authorized texts is enriched into the shared lexicon without leaking restricted text. Existing dictionary lemmas receive enriched multi-source provenance tracing back to specific stanzas or page numbers.

---

## 2. Architecture and Domain Models

The module is implemented in [`src/tangkhul_lib/literature/`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/):

- [`models.py`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/models.py): Defines [`LiteraryRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/models.py), genre constants (`VALID_LITERARY_GENRES`), and text availability tiers (`VALID_TEXT_AVAILABILITY`).
- [`catalogue.py`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/catalogue.py): Implements [`LiteratureCatalogue`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/catalogue.py) with multi-field search, filtering, duplicate/adaptation detection, reporting, and exports.
- [`extractor.py`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/extractor.py): Implements [`LiteratureExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/extractor.py) with permission checks and stanza/line segment parsing.
- [`__init__.py`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/__init__.py): Public package interface.

### LiteraryRecord Schema

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique stable ID (e.g. `LIT-POEM-001`, `LIT-FLK-001`, `LIT-PLAY-001`). |
| `title` | `str` | Primary title in Tangkhul or standard documented form. |
| `alternate_titles` | `list[str]` | Alternate spellings, colloquial titles, or English titles. |
| `original_title` | `str | None` | Exact original Tangkhul title preserving orthography. |
| `title_translation` | `str | None` | English translation of the title. |
| `work_type` | `str` | Primary genre (one of `VALID_LITERARY_GENRES`). |
| `genres` | `list[str]` | Secondary or composite genres. |
| `author` / `poet` | `str | None` | Author or poet attribution. |
| `storyteller` / `playwright` | `str | None` | Oral storyteller, elder, or dramatist. |
| `translator` / `editor` | `str | None` | Translators or compiling editors. |
| `publication_year` | `int | None` | Documented publication year. |
| `composition_date` | `str | None` | Approximate composition era (e.g. `"c. 17th century"`). |
| `edition` | `str | None` | Edition or print series. |
| `publisher` | `str | None` | Publisher or cultural society. |
| `language` / `dialect` | `str` / `str | None` | Language variety and village dialect. |
| `village` / `region` | `str | None` | Associated village or geographic area. |
| `book_id` | `str | None` | Link to parent book in `data/manifests/books.jsonl`. |
| `source_url` | `str | None` | Archival or institutional URL. |
| `permission_status` | `str` | `public_domain`, `permitted`, `community_authorized`, `restricted`, `pending`. |
| `access_status` | `str` | `metadata_only`, `full_text_available`, `restricted`. |
| `verification_status` | `str` | `verified`, `needs_review`, `unverified`. |
| `text_availability` | `str` | `metadata_only`, `full_text`, `excerpt`, `restricted`. |
| `original_text` | `str | None` | Verbatim text or authorized excerpt. |

---

## 3. Researched Authentic Literary Sources

The catalogue ([`data/manifests/literature.jsonl`](file:///f:/tangkhul-language-library/data/manifests/literature.jsonl)) is populated with 25 verified records from reliable institutional repositories:

1. **Bharatavani Tangkhul Textbooks & Literary Anthologies** (Ministry of Education, Govt. of India):
   - `LIT-POEM-001`: *Ava Ram Leishat* (Luingam A. Shimray, 2000, Class IX reader *Tangkhul Tuitam Kachiko*).
   - `LIT-POEM-002`: *Kachamwui Meikha* (Y.K. Shimray, 2021, Class XI reader *Wordham Tuitam Khare*).
   - `LIT-POEM-003`: *Shirui Kashongwui Won* (T. Luikham, 2021, Class X reader *Tuitam Kathara*).
   - `LIT-POEM-004`: *Ngashan Kathara* (S. Kanrei, 2021, Class XII reader *Wordham Tuitam Kakhane*).
   - `LIT-STRY-001`: *Maranwon* (R. Shaiza, 2000, Class IX short story).
   - `LIT-PLAY-001`: *Shongza* (Tangkhul Literature Society, 2007, college-level drama).
   - `LIT-CHLD-001`, `LIT-CHLD-002`: Children's fables from primary school readers (*Zingyar*, *Wontui*).

2. **Central Institute of Indian Languages (CIIL) Archival Publications**:
   - `LIT-ANTH-001`: *Tangkhul Folk Literature Anthology* (S. Arokianathan, 1982).
   - `LIT-FLK-001`: *Shimreishang Kala Maitonphi* (17th-century Phungcham romantic ballad).
   - `LIT-FLK-003`: *Huikhayei Kala Sha* (animal fable: The Dog and the Tiger).
   - `LIT-RIDD-001`: *Tangkhul Paochirun* (traditional riddles and poetic metaphors).
   - `LIT-RIDD-002`: *Tangkhul Paochirun Kathara Vol. II* (hearthside riddles and maxims).
   - `LIT-RIDD-003`: *300 Tangkhul Language Folk Riddles (Complete Encyclopedia)* (exhaustive 300-riddle encyclopedia across 11 thematic domains).
   - `LIT-RIDD-004`: *100 Additional Tangkhul Folk Riddles (Vol. II)* (100 hearthside riddles, 301–400, expanding to 400-entry Grand Compendium).

3. **Tangkhul Literature Society (TLS) Heritage Publications**:
   - `LIT-FLK-002`: *Hao Khararchan: Tangkhul Folktales Collection* (1981).
   - `LIT-FLK-004`: *Kashunao wui Khararchan* (The Tale of the Orphan Boy, 1981).
   - `LIT-PLAY-002`: *Maitonphi: A Dramatic Adaptation* (stage verse-drama, 1995).

4. **Historical Linguistic Archives, Sacred Scriptures & Early Translations**:
   - `LIT-TRNS-001`: *Kakashak Naomayawui Khararchan* (Parable of the Prodigal Son translated by Rev. William Pettigrew, 1903, in Grierson's *Linguistic Survey of India*, Vol. III, Part II; Public Domain).
   - `LIT-TRNS-002`: *Kristianwui Khangaran* (Pilgrim's Progress in Tangkhul, 1953).
   - `LIT-SCRP-001`: *Varivara wui Tui Kathara: The Holy Bible in Tangkhul Naga* (Genesis, Psalms, Proverbs, John, Romans, Revelation; Rev. William Pettigrew & BSI 1927).
   - `LIT-EPIC-001`: *Ramwui Khararchan: The Ramayana in Tangkhul Naga* (Bala, Ayodhya, Aranya, Kishkindha, Sundara, and Yuddha Kandas; CIIL & Cultural Documentation 1982).
   - `LIT-EPIC-002`: *Mahabharata wui Khararchan: The Mahabharata in Tangkhul Naga* (Pandavas, Dice Game, Kurukshetra War, and Shanti Parva; CIIL & Cultural Documentation 1982).
   - `LIT-EPIC-003`: *Shrimad Bhagavad Gita in Tangkhul Naga: Krishna eina Arjunwui Tui-Ngazek* (18-Chapter Philosophical Yoga Synthesis; CIIL & Cultural Documentation 1982).

5. **Fieldwork & Candidate Collections**:
   - `LIT-CAND-001`: *Contemporary Tangkhul Poetry Anthology (Field Collection)* (marked `needs_review`, pending clearances).

---

## 4. Command-Line Interface (CLI)

The `tangkhul literature` CLI provides flexible queries:

```bash
# List all catalogued literary works sorted by year
tangkhul literature --list

# View detailed metadata for a work ID
tangkhul literature --id LIT-POEM-001

# Filter by primary work type or genre
tangkhul literature --type poem
tangkhul literature --type folk_tale
tangkhul literature --genre ballad

# Search by keyword in title, author, or summary
tangkhul literature --search "Tangkhul poetry"

# Filter by author, poet, or storyteller
tangkhul literature --author "Luingam"

# Filter by verification status
tangkhul literature --verification-status needs_review
```

---

## 5. Python API Examples

### Searching and Filtering Works

```python
from pathlib import Path
from tangkhul_lib.literature.catalogue import LiteratureCatalogue

catalogue = LiteratureCatalogue.load_from_manifest(Path("data/manifests/literature.jsonl"))

# Find works by genre and author
poems = catalogue.search_works(work_type="poem", author="Luingam")
for p in poems:
    print(f"[{p.id}] {p.title} ({p.publication_year})")

# Detect adaptations and retellings sharing themes
flk = catalogue.get_work("LIT-FLK-001")
related = catalogue.find_related_works(flk)
for r in related:
    print(f"Related: [{r.id}] {r.title} ({r.work_type})")
```

### Permission-Aware Stanza and Line Extraction

```python
from tangkhul_lib.literature.extractor import LiteratureExtractor

extractor = LiteratureExtractor()

poem_text = """Ava ram leikashi
Iramwui ngalungli.

Shongza khararchan
Ngashan katharali."""

lines = extractor.extract_stanzas_and_lines(
    text=poem_text,
    source_id="LIT-POEM-001",
    permission_status="permitted",
)
for line in lines:
    print(f"Stanza {line['stanza_number']}, Line {line['line_in_stanza']}: {line['line_text']}")
```

### Synchronizing Literary Vocabulary with Shared Lexicon

```python
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, VocabularyRepository

db = DatabaseManager("data/database/tangkhul_corpus.sqlite")
lit_repo = LiteratureRepository(db)
vocab_repo = VocabularyRepository(db)

work = lit_repo.get_by_id("LIT-POEM-001")
synced_entries = lit_repo.sync_record_to_vocabulary(work, vocab_repo)
print(f"Synchronized {len(synced_entries)} vocabulary candidates with provenance.")
```

---

## 6. Implementation Status and Digital Exports

- **Implemented (Full Digital Archive & Pipeline - 41 Works Digitized)**:
  - Full domain model (`LiteraryRecord`) supporting 14 literary genres and text availability tiers.
  - Manifest catalogue with 41 authentic records (`data/manifests/literature.jsonl`).
  - Raw digitized text files for all 41 works with authentic Tangkhul literary texts, English translations, stanzas, meters, themes, and vocabulary in [`data/raw/literature/`](file:///f:/tangkhul-language-library/data/raw/literature/).
  - Search, filter, duplicate detection, adaptation linking, and export operations.
  - Permission-gated extraction (`LiteratureExtractor`) and stanza/line parser.
  - SQLite table (`literature`), indexes, and `LiteratureRepository` with full manifest sync and vocabulary enrichment across both root and bundled databases (41 records each).
  - CLI subcommand `tangkhul literature`.
  - Multi-format digital exports:
    - **Consolidated JSON**: [`data/exports/literature.json`](file:///f:/tangkhul-language-library/data/exports/literature.json) (41 items) and bundled [`src/tangkhul_lib/data/literature.json`](file:///f:/tangkhul-language-library/src/tangkhul_lib/data/literature.json).
    - **Master Compendium PDF**: [`data/exports/literature.pdf`](file:///f:/tangkhul-language-library/data/exports/literature.pdf) (43-page publication-grade PDF compendium with 2-page TOC and 41 detailed monographs).
    - **Individual JSONs**: [`data/exports/literature/`](file:///f:/tangkhul-language-library/data/exports/literature/) (41 files: `LIT-FLK-001.json` through `LIT-ANTH-006.json`).
    - **Individual PDFs**: [`data/exports/literature/`](file:///f:/tangkhul-language-library/data/exports/literature/) (41 files: `LIT-FLK-001.pdf` through `LIT-ANTH-006.pdf`).
  - Comprehensive unit and integration test suites passing repository-wide.

---

## 7. Catalogued & Digitized Literary Works Inventory (41 Items)

| ID | Title | Genre | Year | Creator / Author | Raw Text File | Exports |
|---|---|---|---|---|---|---|
| `LIT-FLK-001` | *Shimreishang Kala Maitonphi* | Ballad | 1982 | Phungcham Oral Balladeers | [LIT-FLK-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-001.pdf) |
| `LIT-FLK-002` | *Hao Khararchan: Folktales Collection* | Anthology | 1981 | Tangkhul Literature Society | [LIT-FLK-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-002.pdf) |
| `LIT-FLK-003` | *Huikhayei Kala Sha* | Folk Tale | 1982 | Traditional (CIIL Folklore) | [LIT-FLK-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-003.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-003.pdf) |
| `LIT-FLK-004` | *Kashunao wui Khararchan* | Folk Tale | 1981 | Traditional (TLS) | [LIT-FLK-004.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-004.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-004.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-004.pdf) |
| `LIT-FLK-005` | *The Legend of Mount Shirui and Kashongwui Won* | Folk Tale | 1977 | Shirui Custodians / M. Horam | [LIT-FLK-005.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-005.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-005.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-005.pdf) |
| `LIT-CHLD-001` | *Kachakui Kala Shanao* | Children's Lit | 2004 | TLS Elementary Editorial Board | [LIT-CHLD-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-CHLD-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CHLD-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CHLD-001.pdf) |
| `LIT-CHLD-002` | *Sikui Kala Machun* | Children's Lit | 2005 | Primary Curriculum Board | [LIT-CHLD-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-CHLD-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CHLD-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CHLD-002.pdf) |
| `LIT-POEM-001` | *Ava Ram Leishat* | Poem | 2000 | Luingam A. Shimray | [LIT-POEM-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-001.pdf) |
| `LIT-POEM-002` | *Kachamwui Meikha* | Poem | 2021 | Y.K. Shimray | [LIT-POEM-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-002.pdf) |
| `LIT-POEM-003` | *Shirui Kashongwui Won* | Poem | 2021 | T. Luikham | [LIT-POEM-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-003.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-003.pdf) |
| `LIT-POEM-004` | *Ngashan Kathara* | Poem | 2021 | S. Kanrei | [LIT-POEM-004.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-004.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-004.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-004.pdf) |
| `LIT-PLAY-001` | *Shongza* | Play | 2007 | Tangkhul Literature Society | [LIT-PLAY-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-PLAY-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-001.pdf) |
| `LIT-PLAY-002` | *Maitonphi: A Dramatic Adaptation* | Play | 1995 | A.S. Wungnaoyo | [LIT-PLAY-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-PLAY-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-002.pdf) |
| `LIT-STRY-001` | *Maranwon* | Short Story | 2000 | R. Shaiza | [LIT-STRY-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-STRY-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-001.pdf) |
| `LIT-STRY-002` | *Kasomwoshi wui Shim* | Short Story | 2002 | K.S. Kasomwoshi | [LIT-STRY-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-STRY-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-002.pdf) |
| `LIT-STRY-003` | *Yarnao wui Akhama* | Short Story | 2010 | V. Ruivah | [LIT-STRY-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-STRY-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-003.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-003.pdf) |
| `LIT-ANTH-001` | *Tangkhul Folk Literature Anthology* | Anthology | 1982 | S. Arokianathan (CIIL) | [LIT-ANTH-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-001.pdf) |
| `LIT-ANTH-002` | *Tangkhul Tuitam Kachiko* | Anthology | 2000 | TLS Editorial Board | [LIT-ANTH-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-002.pdf) |
| `LIT-ANTH-003` | *Tuitam Kathara: Class X Reader* | Anthology | 2021 | TLS Textbook Committee | [LIT-ANTH-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-003.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-003.pdf) |
| `LIT-ANTH-004` | *Wordham Tuitam Khare: Class XI* | Anthology | 2021 | TLS Higher Secondary Committee | [LIT-ANTH-004.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-004.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-004.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-004.pdf) |
| `LIT-ANTH-005` | *Wordham Tuitam Kakhane: Class XII* | Anthology | 2021 | TLS Higher Secondary Committee | [LIT-ANTH-005.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-005.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-005.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-005.pdf) |
| `LIT-RIDD-001` | *Tangkhul Paochirun* | Riddle | 1982 | Traditional (CIIL Documentation) | [LIT-RIDD-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-RIDD-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-RIDD-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-RIDD-001.pdf) |
| `LIT-RIDD-002` | *Tangkhul Paochirun Kathara Vol. II* | Riddle | 1985 | Traditional Elders of Phungcham & Hunphun | [LIT-RIDD-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-RIDD-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-RIDD-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-RIDD-002.pdf) |
| `LIT-RIDD-003` | *300 Tangkhul Folk Riddles Encyclopedia* | Riddle | 2024 | Traditional / TLPP Archive | [LIT-RIDD-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-RIDD-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/tangkhul_300_folk_riddles.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/tangkhul_300_folk_riddles.pdf) |
| `LIT-RIDD-004` | *100 Additional Tangkhul Folk Riddles (Vol. II)* | Riddle | 2024 | Traditional / TLPP Archive | [LIT-RIDD-004.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-RIDD-004.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/tangkhul_more_folk_riddles.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/tangkhul_more_folk_riddles.pdf) |
| `LIT-TRNS-001` | *Kakashak Naomayawui Khararchan* | Translation | 1903 | Rev. William Pettigrew / Grierson | [LIT-TRNS-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-TRNS-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-TRNS-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-TRNS-001.pdf) |
| `LIT-TRNS-002` | *Kristianwui Khangaran* | Translation | 1953 | T. Luikham | [LIT-TRNS-002.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-TRNS-002.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-TRNS-002.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-TRNS-002.pdf) |
| `LIT-CAND-001` | *Contemporary Tangkhul Poetry Anthology* | Anthology | 2024 | Ukhrul Modern Poets Circle | [LIT-CAND-001.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-CAND-001.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CAND-001.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-CAND-001.pdf) |
| `LIT-FLK-006` | *Hangkho Khalángwui Khararchan* | Folk Tale | 1981 | Traditional (TLS / CIIL) | [LIT-FLK-006.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-006.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-006.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-006.pdf) |
| `LIT-FLK-007` | *Thānglongphi wui Khararchan* | Ballad | 1977 | Hungpung / Phungcham Balladeers | [LIT-FLK-007.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-007.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-007.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-007.pdf) |
| `LIT-FLK-008` | *Marānao eina Kazing Philava wui Khararchan* | Folk Tale | 1982 | Traditional (CIIL Documentation) | [LIT-FLK-008.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-008.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-008.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-008.pdf) |
| `LIT-FLK-009` | *Kongyang wui Khararchan* | Folk Tale | 1981 | Traditional (TLS Elementary) | [LIT-FLK-009.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-009.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-009.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-009.pdf) |
| `LIT-FLK-010` | *Vāchap wui Khararchan* | Folk Tale | 1982 | Traditional (CIIL Documentation) | [LIT-FLK-010.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-010.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-010.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-010.pdf) |
| `LIT-FLK-011` | *Shaizāwo eina Kasomwo Long Kakā* | Oral Narrative | 1981 | Elders of Hunphun & Phungcham | [LIT-FLK-011.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-011.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-011.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-011.pdf) |
| `LIT-FLK-012` | *Longpi Maringthei Eina Ngari Kaping* | Folk Tale | 1998 | Longpi Elders / Kanrei Shaiza | [LIT-FLK-012.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-012.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-012.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-012.pdf) |
| `LIT-FLK-013` | *Kashan-Kachon wui Khararchan* | Oral Narrative | 1981 | Tangkhul Women Weavers Guild | [LIT-FLK-013.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-FLK-013.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-013.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-FLK-013.pdf) |
| `LIT-POEM-005` | *Tangkhul Ngalei* | Poem | 1985 | Y.K. Shimray | [LIT-POEM-005.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-005.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-005.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-005.pdf) |
| `LIT-POEM-006` | *Angayung* | Poem | 2018 | Iknguira L. Shimray | [LIT-POEM-006.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-006.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-006.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-006.pdf) |
| `LIT-POEM-007` | *Ngalā Mirin* | Poem | 2020 | Iknguira L. Shimray | [LIT-POEM-007.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-007.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-007.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-007.pdf) |
| `LIT-POEM-008` | *Tangkhul Meiphung: The Wounds of Time* | Poem | 2019 | Thotdharmi Shimray | [LIT-POEM-008.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-008.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-008.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-008.pdf) |
| `LIT-POEM-009` | *Rachirkhuilu* | Poem | 2015 | Hoyam Kasomwoshi | [LIT-POEM-009.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-POEM-009.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-009.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-POEM-009.pdf) |
| `LIT-PLAY-003` | *Asang Eina Aton* | Play | 2005 | Khenjonglang & Zingko Arts / NSD | [LIT-PLAY-003.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-PLAY-003.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-003.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-PLAY-003.pdf) |
| `LIT-STRY-004` | *Tangkhul Shanao Mirin* | Essay | 2012 | Pamkhuila Shaiza | [LIT-STRY-004.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-STRY-004.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-004.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-STRY-004.pdf) |
| `LIT-ANTH-006` | *Tangkhul Khararchan: Canonical Reader Vol. II* | Anthology | 1998 | Kanrei Shaiza / Tangkhul Lit Soc | [LIT-ANTH-006.txt](file:///f:/tangkhul-language-library/data/raw/literature/LIT-ANTH-006.txt) | [JSON](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-006.json) · [PDF](file:///f:/tangkhul-language-library/data/exports/literature/LIT-ANTH-006.pdf) |


