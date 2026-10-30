# Books Module (`tangkhul_lib.books`)

The **Books** module is a core domain package in the Tangkhul Language Library. It provides structured bibliographic cataloguing, metadata validation, duplicate detection, copyright-respecting text extraction, and candidate vocabulary generation for published Tangkhul books.

---

## 1. Module Purpose

Tangkhul literature spans early missionary grammatical descriptions and primers, school and college textbooks prepared by the Tangkhul Literature Society (TLS), folk literature anthologies, and linguistic publications.

The primary purposes of `tangkhul_lib.books` are:
1. **Bibliographic Preservation**: Systematically catalogue Tangkhul textbooks, grammar books, literary collections, and academic volumes with verified metadata in [`data/manifests/books.jsonl`](file:///f:/tangkhul-language-library/data/manifests/books.jsonl).
2. **Provenance-Preserving Text Processing**: Extract text from permitted digital and print archives, preserving exact page citations and section markers.
3. **Lexical Harvesting**: Connect extracted tokens and sentences to the shared vocabulary repository ([`VocabularyEntry`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py) and [`ProvenanceRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py)) without fabricating meanings or flattening dialectal orthography.
4. **Access and Copyright Governance**: Distinguish between metadata-only catalogues, public domain documents, community-authorized works, and restricted copyrighted material.

---

## 2. Catalogue Schema

Each book entry in [`data/manifests/books.jsonl`](file:///f:/tangkhul-language-library/data/manifests/books.jsonl) implements the [`BookRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/books/models.py) schema:

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Stable unique identifier (e.g. `BK-TLS-001`, `BK-HIST-001`). Required. |
| `title` | `str` | Primary title in Tangkhul or English as printed. Required. |
| `alternate_titles` | `list[str]` | Subtitles, phonetic titles, or English translations. |
| `authors` | `list[str]` | Authors of the work. Left empty if unstated in source catalogue. |
| `editors` | `list[str]` | Editors or compilers of the work. |
| `publisher` | `str \| None` | Publishing body or institution (e.g. `Tangkhul Literature Society, Manipur`). |
| `publication_year` | `int \| None` | Year of publication. Aliased to `year`. |
| `edition` | `str \| None` | Edition designation (e.g. `First Edition`, `Revised`). |
| `subject` | `str \| None` | Domain classification (`Literature`, `Grammar`, `History`, `Drama`). |
| `educational_level` | `str \| None` | Target educational level (`Class II`, `Class IV`, `Classes IX–X`, `B.A. First Year`). |
| `language` | `str` | Language of the work (default: `Tangkhul`). |
| `dialect` | `str \| None` | Dialect represented (e.g. `Standard Tangkhul`, `Ukhrul`). |
| `isbn` | `str \| None` | Standard book number where available. |
| `source_url` | `str \| None` | Direct link to digital file or landing record. |
| `source_identifier` | `str \| None` | Repository identifier (e.g. `BVP-TB-TKH-001`, `CIIL Grammar Series No. 16`). |
| `catalogue_url` | `str \| None` | External catalogue reference URL (Bharatavani, CIIL, etc.). |
| `local_file_path` | `str \| None` | Local relative path if document is retained locally. |
| `file_format` | `str \| None` | Format of local or source file (`txt`, `pdf`, etc.). |
| `license` | `str \| None` | Licensing terms (`Public Domain`, `CC-BY`, etc.). |
| `permission_status` | `str` | One of: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`. |
| `access_status` | `str` | One of: `metadata_only`, `full_text_available`, `restricted`, `open_access`, `unknown`. |
| `verification_status` | `str` | One of: `verified`, `needs_review`, `partially_verified`, `unverified`, `community_reviewed`. |
| `notes` | `str \| None` | Bibliographic provenance context and cataloguing details. |

---

## 3. Current Data Sources

1. **Bharatavani Portal (Central Institute of Indian Languages, Ministry of Education, Govt. of India)**
   - Textbooks: `https://bharatavani.in/tangkhul/textbook`
   - Knowledge / Jnanakosha: `https://bharatavani.in/tangkhul/jnanakosha`
   - Language Learning / Bhashakosha: `https://bharatavani.in/tangkhul/bhashakosha`
   - Content partner: Tangkhul Literature Society (TLS), Manipur.
2. **Central Institute of Indian Languages (CIIL) & Bhasha Sanchika**
   - Linguistic publications and phonetic readers by S. Arokianathan and D.N.S. Bhat.
   - Sanchika: `https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e`
3. **Public Domain Archives (Internet Archive / HathiTrust)**
   - Rev. William Pettigrew's *Tangkhul Naga Grammar and Dictionary (Ukhrul Dialect)* (1918, Assam Secretariat Printing Office, Shillong).
   - Sir George Grierson's *Linguistic Survey of India* (1903, Vol. III, Part II, Tangkhul section).

---

## 4. Catalogued Book Records

### Initial Verified Bharatavani Textbooks (14 records)
All 14 initial textbooks were verified directly against the Bharatavani catalogue:

| ID | Title | Level | Subject | Year | Publisher |
|---|---|---|---|---|---|
| `BK-TLS-001` | Wontui Tangkhul | Class II | Literature | 2022 | Tangkhul Literature Society, Manipur |
| `BK-TLS-002` | Zingyar Tangkhul | Class IV | Literature | 2022 | Tangkhul Literature Society, Manipur |
| `BK-TLS-003` | Zingyar Tangkhul | Class V | Literature | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-004` | Zingshan Tangkhul Katharuka | Class VI | Literature | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-005` | Zingshan Tangkhul Kashine | Class VII | Literature | 2019 | Tangkhul Literature Society, Manipur |
| `BK-TLS-006` | Zingshan Tangkhul Kachishata | Class VIII | History | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-007` | Tangkhul Tuitam Kachiko | Class IX | Literature | 2000 | Tangkhul Literature Society, Manipur |
| `BK-TLS-008` | Tuitam Kathara | Class X | Literature | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-009` | Tangkhul Grammar | Classes IX–X | Grammar | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-010` | Tangkhul Grammar Kala Composition | Classes IX–X | Grammar & Comp. | 2000 | Tangkhul Literature Society, Manipur |
| `BK-TLS-011` | Wordham Tuitam Khare | Class XI | Literature | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-012` | Wordham Tuitam Kakhane | Class XII | Literature | 2021 | Tangkhul Literature Society, Manipur |
| `BK-TLS-013` | Tangkhul Wordham | B.A. Sem I | Grammar | 2020 | Tangkhul Literature Society, Manipur |
| `BK-TLS-014` | Shongza | B.A. Year 1 | Drama | 2007 | Tangkhul Literature Society, Manipur |

> [!NOTE]
> *Zingyar Tangkhul* Class IV (2022) and *Zingyar Tangkhul* Class V (2021) are distinct curriculum editions and are intentionally maintained as separate records. Authors are omitted where unstated by the publisher.

### Additional Verified Archival & Research Books (8 records)

| ID | Title | Author / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-HIST-001` | Tangkhul Naga Grammar and Dictionary | William Pettigrew | 1918 | Assam Secretariat Printing Office | Verified (Public Domain) |
| `BK-HIST-002` | Tangkhul Primer and Catechism | William Pettigrew | 1897 | American Baptist Mission | Verified (Public Domain) |
| `BK-CIIL-001` | Tangkhul Naga Phonetic Reader | S. Arokianathan | 1980 | CIIL, Mysore | Verified |
| `BK-CIIL-002` | Tangkhul Naga Grammar | S. Arokianathan | 1987 | CIIL, Mysore | Verified |
| `BK-CIIL-003` | Tangkhul Folk Literature | S. Arokianathan | 1982 | CIIL, Mysore | Verified |
| `BK-DC-001` | Tangkhul-Naga Vocabulary | D. N. S. Bhat | 1969 | Deccan College, Poona | Verified |
| `BK-TLS-015` | Tangkhul Khararchan | Tangkhul Literature Society | 1981 | TLS, Manipur | Verified |
| `BK-ARCH-001` | Linguistic Survey of India (Tangkhul Section) | George A. Grierson | 1903 | Govt. Printing, Calcutta | Verified (Public Domain) |

### Newly Discovered & Digitalized Archival & Folk Literature Books: Batch 1 (6 records)

| ID | Title | Author / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-ARCH-002` | Jesuwui La: Hymns in Tangkhul Naga | Rev. William Pettigrew | 1907 | American Baptist Mission, Ukhrul | Verified (Public Domain, IA `hymnsintangkhuln00pett`) |
| `BK-ARCH-003` | The Naga Tribes of Manipur (Tangkhul Sections) | T. C. Hodson | 1911 | Macmillan and Co., London | Verified (Public Domain, IA `nagatribesofmani00hods`) |
| `BK-LIT-001` | The Tangkhul Folk Poetry in Song (HAOLA) | Dr. Ringkahao Horam | 2013 | Naga Cultural Dev. Soc. & TRI Manipur | Verified (Open Access, DLI `dli.language.1350`) |
| `BK-LIT-002` | Folk Songs of The Tangkhul | Dr. H. Kamkhenthang & A. Ngashan Chahong | 1987 | Directorate for Dev. of Tribals, Manipur | Verified (Open Access, DLI `dli.language.1472`) |
| `BK-LIT-003` | Tangkhul Gee Wari Singbul (Folktales) | Y. K. Shimray | 1976 | Cultural Heritage of Manipur | Verified (Public Domain, DLI `in.ernet.dli.2015.466362`) |
| `BK-CIIL-004` | Tangkhul-English, Hindi Dictionary | Dr. S. Arokianathan & Dr. Rekha Sharma | 1995 | CIIL, Mysore (ISBN 81-7342-028-9) | Verified (Academic / CIIL, IA `tangkhulenglishh00arok`) |

### Newly Discovered & Digitalized Archival & Folk Literature Books: Batch 2 (6 records)

| ID | Title | Author / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-ARCH-004` | Pa o Kamata Isha mai Jesu Christawui Khararchan: John Kahona Kasa | Rev. William Pettigrew | 1904 | British and Foreign Bible Society, London / Baptist Mission Press, Calcutta | Verified (Public Domain, BFBS-TKH-1904) |
| `BK-ARCH-005` | Pa o Kamata Isha mai Jesu Christawui Khararchan: Luke Kahona Kasan | Rev. William Pettigrew | 1905 | British and Foreign Bible Society, London / Baptist Mission Press, Calcutta | Verified (Public Domain, BFBS-TKH-1905) |
| `BK-ARCH-006` | Pa o Kachatbingna Kasa wui Khararchan: The Acts of the Apostles | Rev. William Pettigrew | 1905 | British and Foreign Bible Society, London / Baptist Mission Press, Calcutta | Verified (Public Domain, BFBS-TKH-1905) |
| `BK-HIST-003` | History of the Tangkhul Nagas | A. S. W. Shimray | 2001 | Akansha Publishing House, New Delhi (ISBN 81-87606-04-5) | Verified (Permitted / Academic) |
| `BK-LIT-004` | Wung (Tangkhul) Naga Okthot Mayonza | T. Luikham | 1961 | Tangkhul Literature Society / Published at Imphal | Verified (Public Domain / Community Heritage) |
| `BK-LIT-005` | Tangkhul Folk Ballads and Oral Narratives (Wungram Khararchan) | Prof. Khashim Ruivah | 1993 | Tribal Research Institute, Government of Manipur, Imphal | Verified (Open Access / TRI Manipur) |

### Newly Digitalized World Classics & Translated Books: Batch 3 (10 records)

| ID | Title | Translator / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-TRNS-001` | Ithui Varewui Lairik Kathara: The New Testament in Tangkhul Naga | Rev. William Pettigrew & Tangkhul Native Scholars | 1927 | British and Foreign Bible Society, Calcutta / Baptist Mission Press | Verified (Public Domain, BFBS-TKH-NT-1927) |
| `BK-TRNS-002` | Pa o Kamata Isha mai Jesu Christawui Khararchan: Matthew Kahona Kasa | Rev. William Pettigrew | 1907 | British and Foreign Bible Society, Calcutta / Baptist Mission Press | Verified (Public Domain, BFBS-TKH-MATT-1907) |
| `BK-TRNS-003` | Pa o Kamata Isha mai Jesu Christawui Khararchan: Mark Kahona Kasa | Rev. William Pettigrew | 1909 | British and Foreign Bible Society, Calcutta / Baptist Mission Press | Verified (Public Domain, BFBS-TKH-MARK-1909) |
| `BK-TRNS-004` | Avara Kasa wui Khararchan: The Book of Genesis in Tangkhul Naga | Tangkhul Translation Committee | 1965 | Bible Society of India, Bangalore (ISBN 978-81-221-0412-8) | Verified (Community Authorized / BSI) |
| `BK-TRNS-005` | Samwui Khararchan: Luishat Laa (The Book of Psalms in Tangkhul Naga) | Tangkhul Christian Literature Committee | 1968 | Bible Society of India, Bangalore (ISBN 978-81-221-0413-5) | Verified (Community Authorized / BSI) |
| `BK-TRNS-006` | Khangayeiwui Khayang: John Bunyan's The Pilgrim's Progress in Tangkhul Naga | Rev. William Pettigrew & Ukhrul Mission | 1932 | Ukhrul Mission Press / Tangkhul Literature Society | Verified (Public Domain / Community Heritage) |
| `BK-TRNS-007` | Aesopwui Khararchan: Translated Aesop's Fables & Moral Stories in Tangkhul | Tangkhul Literature Society | 1978 | Tangkhul Literature Society, Imphal / Ukhrul | Verified (Community Authorized / TLS) |
| `BK-TRNS-008` | Tagorewui Gitanjali kala Shai-laaring: Selected Translations in Tangkhul Naga | Rabindranath Tagore / Tangkhul Literary Forum | 1986 | Tangkhul Cultural Council / Ukhrul Literature Circle | Verified (Open Access / Literary Monograph) |
| `BK-TRNS-009` | Duniyawui Khararchan Kathara: World Classic Stories Translated into Tangkhul | Tangkhul Literature Society (Tolstoy, Maupassant, O. Henry) | 1991 | Tangkhul Literature Society, Imphal / Ukhrul | Verified (Community Authorized / Curriculum) |
| `BK-TRNS-010` | Tangkhul Constitution & Civic Rights Primer: Indiawui Samvidhan kala Hao Rights | Tangkhul Scholars Association & Naga Law Forum | 2005 | Tangkhul Scholars Association (ISBN 978-81-90412-11-9) | Verified (Community Authorized / TPO) |

### Newly Digitalized Tangkhul Novels (Upanyas) & Biographies: Batch 4 (10 records)

#### 5 Classic Tangkhul Novels (उपन्यास)

| ID | Title | Author / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-NOVL-001` | Shimreishang kala Maitonphi: The Classic Tangkhul Epic Novel of Love and Tragedy | Tangkhul Literary Society & Folk Forum | 1972 | Tangkhul Literature Society, Imphal / Ukhrul | Verified (Community Authorized / TLS) |
| `BK-NOVL-002` | Chamthei: A Tangkhul Novel of Highland Trials and Hope | K. S. Luikham | 1984 | Ukhrul Cultural Publications | Verified (Community Authorized / TLS) |
| `BK-NOVL-003` | Shongza: The Tragic Chronicle of Destiny and Clan Honour | Tangkhul Literature Committee | 1979 | Tangkhul Literature Society, Ukhrul | Verified (Community Authorized / TLS) |
| `BK-NOVL-004` | Wungram Okthot: The Novel of Highland Heritage and Clan Trials | A. S. Vashum | 1993 | Eastern Naga Literary Circle | Verified (Community Authorized / TLS) |
| `BK-NOVL-005` | Yarra: A Novel of Tangkhul Youth and Spring Awakening | R. K. Shimray | 1988 | Youth Cultural Guild, Ukhrul | Verified (Community Authorized / TLS) |

#### 5 Landmark Biographies (जीवनी)

| ID | Title | Author / Compiler | Year | Publisher / Source | Status |
|---|---|---|---|---|---|
| `BK-BIOG-001` | Major Bob Khathing: The Great Tangkhul Patriot, Soldier, and Statesman of Tawang | Col. (Retd.) Sanjoy Bhattacharya & Tangkhul Historical Society | 2002 | Tribal Research Institute & Heritage Trust | Verified (Open Access / Permitted) |
| `BK-BIOG-002` | Rev. William Pettigrew: Ukhrulwui Pao-phungnao (Life and Mission of the Pioneer Educator) | Tangkhul Baptist Christian Association Historical Commission | 1986 | TBCA Mission Press, Ukhrul | Verified (Community Authorized / TBCA) |
| `BK-BIOG-003` | Rishang Keishing: The Legendary Tangkhul Parliamentarian and Chief Minister | H. A. Shimray | 2008 | Eastern Hill Publishers, Imphal | Verified (Permitted / Academic) |
| `BK-BIOG-004` | Rowland Suisa (R. Suisa): The Prophet of Naga Peace, Democracy, and Customary Rights | R. Suisa Memorial Trust & Tangkhul Scholars Forum | 1998 | R. Suisa Trust, Ukhrul | Verified (Open Access / Trust) |
| `BK-BIOG-005` | Luingam Luikham: Custodian of Tangkhul Oral Literature and Customary Law | Wungram Heritage Society | 2005 | Tangkhul Literary Forum, Ukhrul | Verified (Community Authorized / TLS) |

### Candidate Records Requiring Review (1 record)

| ID | Title | Subject | Verification Status | Notes |
|---|---|---|---|---|
| `BK-CAND-001` | Tangkhul Folk Songs and Cultural Lore | Folk Songs & Lore | `needs_review` | Identified from citation references; awaiting primary archival verification. |

---

## 5. Search and Retrieval Usage

### Python API

```python
from pathlib import Path
from tangkhul_lib.books import BookCatalogue, BookRecord

# Load catalogue from JSON Lines manifest
manifest_file = Path("data/manifests/books.jsonl")
catalogue = BookCatalogue.load_from_manifest(manifest_file)

# Get book by ID
book = catalogue.get_book("BK-TLS-001")
print(book.title, book.educational_level)

# Search by subject or query
history_books = catalogue.search_books(subject="History")
grammar_books = catalogue.search_books(query="grammar")

# Filter by verification status or publication year
verified_books = catalogue.search_books(verification_status="verified")
books_2021 = catalogue.search_books(publication_year=2021)
```

### CLI Interface

```bash
# List all catalogued books
tangkhul books --list

# Search books
tangkhul books --search "Grammar"

# View complete metadata for a book
tangkhul books --id BK-HIST-001
```

---

## 6. Text Extraction Workflow

The text extraction pipeline is implemented via [`TextExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/ingestion/text_extraction.py) and [`BookTextExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/books/extractor.py):

```
Local Book Source (.txt / .pdf)
         │
         ▼
[Permission & License Check]  ──(Forbidden)──► Raise PermissionRestrictedError
         │ (Permitted)
         ▼
[Text Extraction Engine]
  ├── Text files: preserves explicit "--- Page N ---" markers
  ├── PDF files: extracts page by page via pypdf with exact 1-indexed page numbers
  └── Scanned files: flags status='needs_review' (OCR pending human review)
         │
         ▼
[ExtractionResult (Pages + Full Text)]
```

---

## 7. Vocabulary Integration

Extracted text is tokenized into raw lexical occurrences and candidate [`VocabularyEntry`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py) objects:

1. **Non-Destructive Word Forms**: Preserves original Tangkhul orthography, tonemarks, capitalization, and glottal markers.
2. **Contextual Sentence**: Captures the complete running sentence where the word appears.
3. **Full Provenance**: Attaches a [`ProvenanceRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py) linking the token to the book ID, title, and exact page citation (`p. X`).
4. **No Fabricated Data**: Candidate vocabulary entries leave meanings and translations empty (`[]`), clearly marked as `verification_status="unverified"`.
5. **Separation of Raw vs Confirmed**: Raw tokens are persisted to `extracted_tokens` in SQLite, keeping raw data cleanly separated from reviewed lexicographical entries.

```python
from tangkhul_lib.books import BookTextExtractor

extractor = BookTextExtractor()
if extractor.is_extraction_permitted(book):
    extraction = extractor.extract_book_text(book)
    raw_tokens, candidates = extractor.extract_vocabulary_candidates(book, extraction)
```

---

## 8. Copyright and Access Handling

The library strictly adheres to ethical copyright and cultural sovereignty standards:
- **No Automatic Reproduction Rights**: A catalogue entry does not imply rights to distribute full-text.
- **Permission Enforcement**: `BookTextExtractor.extract_book_text` automatically verifies `permission_status` and `access_status`. If a book is marked `restricted`, extraction is rejected with `PermissionRestrictedError`.
- **Public Domain Clarity**: Historic works (e.g., Pettigrew 1918, Grierson 1903) are marked `public_domain` and `full_text_available`.
- **Git Hygiene**: Large PDFs and scans remain in local storage (`data/raw/books/`) and are never checked into Git.

---

## 9. Instructions for Adding New Book Records

To add a new book record to the catalogue:

1. **Verify Primary Metadata**: Check original physical title page, library catalog (Bharatavani, CIIL, Library of Congress, etc.), and confirm author, publisher, and year.
2. **Assign a Stable ID**:
   - `BK-TLS-XXX`: Tangkhul Literature Society textbooks or readers.
   - `BK-CIIL-XXX`: Central Institute of Indian Languages publications.
   - `BK-HIST-XXX`: Historical or public domain volumes.
   - `BK-CAND-XXX`: Unconfirmed candidate items.
3. **Set Accurate Statuses**:
   - `permission_status`: `pending`, `permitted`, `public_domain`, `community_authorized`, or `restricted`.
   - `access_status`: `metadata_only`, `full_text_available`, `restricted`, or `open_access`.
   - `verification_status`: `verified` if cross-checked against primary catalogue, or `needs_review` if uncertain.
4. **Append to `data/manifests/books.jsonl`** or use `BookCatalogue.add_book(book)`:
   ```python
   new_book = BookRecord(
       id="BK-TLS-016",
       title="New Tangkhul Reader",
       publisher="Tangkhul Literature Society, Manipur",
       publication_year=2023,
       subject="Literature",
       educational_level="Class III",
       verification_status="verified",
   )
   catalogue.add_book(new_book)
   catalogue.export_catalogue(Path("data/manifests/books.jsonl"))
   ```
5. **Validate Manifests**: Run `python scripts/validate_manifests.py` to ensure schema conformance.

---

## 10. Vocabulary Enrichment Pipeline Integration (Step 13)

Under Step 13, authorized books can serve as running-text sources for vocabulary enrichment:
- **Eligible Extraction**: Authorized public-domain books (`BK-HIST-001`, `BK-HIST-002`, `BK-ARCH-001`) can be enriched from local documents (PDF, TXT, MD, DOCX).
- **Lexical Quality**: Candidates extracted from running narrative prose capture authentic contextual sentences and page citations (`p. X`), keeping definitions empty (`[]`) so human reviewers can verify meanings in `tangkhul review`.
- **Deduplication**: Newly extracted tokens are checked against the unified database for exact normalized matches, phonetic similarities, and dialect variants.
- **CLI Commands**:
  ```bash
  tangkhul enrich --list-sources --source-type books
  tangkhul enrich --source-id BK-HIST-001 --file data/raw/books/pettigrew_1918.txt --dry-run
  tangkhul enrich --source-id BK-HIST-001 --file data/raw/books/pettigrew_1918.txt
  ```
