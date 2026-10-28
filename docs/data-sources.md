# Data Sources and Provenance

Preserving linguistic integrity requires that every piece of information in the **Tangkhul Language Library** is backed by authenticated provenance.

---

## 1. Provenance Model

Every lexical entry, book page, song stanza, cultural proverb, historical citation, or literary excerpt traces directly to an authorized source catalogued in `data/manifests/`.

### Provenance Tracking Fields
- **Source Identifier**: A stable ID referring to a record in `data/manifests/` (e.g. `BK-TLS-001`, `SNG-TRAD-001`, `DIC-HIST-001`, `CULT-FEAST-001`, `HIST-EVT-001`, `LIT-POEM-001`).
- **Resource Type**: Domain classification (`books`, `songs`, `dictionaries`, `culture`, `history`, `literature`).
- **Citation**: Bibliographic reference, recording metadata, or interview attribution.
- **Section / Page**: Exact locator within the primary document (page number, stanza number, entry number).
- **Context Sentence**: The verbatim sentence or clause where the word or usage occurred.
- **Year Recorded**: The publication, archival recording, or fieldwork year.
- **Permission Status**: Current legal or community authorization tier (`public_domain`, `permitted`, `community_authorized`, `restricted`, `pending`).

---

## 2. Documented Source Categories

1. **Books and Textbooks**:
   - Tangkhul Literature Society (TLS) textbooks and curricula (Bharatavani portal, Ministry of Education, Govt. of India).
   - Historical grammars and primers (Assam Secretariat, American Baptist Foreign Mission Society).
   - Linguistic monographs by the Central Institute of Indian Languages (CIIL), Mysore.
2. **Songs and Oral Literature**:
   - Traditional folk songs (*Haola*), seasonal agricultural festival chants (*Luira*, *Chumpha*), courting melodies (*Khangrei*), and memorial laments (*Thisham*).
   - Early Christian hymnals (*Jesuwui Laa* 1907, *Christian Songs* 1916).
   - Academic folk anthologies (Kamkhenthang 1989, Horam 1982, CIIL Bhasha Sanchika).
   - Modern recorded compositions (Rewben Mashangva, Diana Wungsek, Thangmeiso Shinglai, Nimshimphi Muivah).
3. **Dictionaries and Lexicons**:
   - Rev. William Pettigrew's 1918 *Tangkhul Naga Grammar and Dictionary (Ukhrul Dialect)* (Public Domain).
   - *Tangkhul Tui Dictionary* (N. Luikham 1997, Tangkhul Literature Society; indexed as metadata-only).
   - *Tangkhul-English-Hindi Dictionary* (Rekha Sharma, S. Arokianathan, E. Annamalai 1995, CIIL Mysore; metadata-only).
   - *Hindi-Tangkhul Dictionary* (Braj Bihari Kumar et al. 1975, Nagaland Bhasha Parishad; metadata-only).
   - *Tankhur Naga Vocabulary* (D.N.S. Bhat 1969, Deccan College Poona; metadata-only).
   - Comparative dialect glossaries and historical wordlists (McCulloch 1859, Grierson 1903 LSI).
4. **Cultural Knowledge, Proverbs, and Ethnographies**:
   - **Bharatavani Tangkhul Jnanakosha & Bhashakosha** (`https://sec.bharatavani.in/tangkhul/jnanakosha`): Knowledge portal by the Ministry of Education, documenting Tangkhul terminology, festivals, and cultural expressions.
   - **CIIL Bhasha Sanchika Tangkhul Collection** (`https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e`): Digital archival repository of Tangkhul linguistic and folklore materials.
   - **Tangkhul Literature Society (TLS)**: Cultural monographs, school texts (*Tangkhul Tuitam*), textile documentation, and traditional proverbs (*Paotam*).
   - **T.C. Hodson (1911)** *The Naga Tribes of Manipur* (Macmillan & Co., London): Early historical documentation of festivals (*Luira*, *Thisham*), village taboos (*Khamasit*), and material crafts (Public Domain).
   - **M. Horam (1977)** *Social and Cultural Life of the Nagas (The Tangkhuls)* (B.R. Publishing Corp.): Detailed study of village governance (*Hangva*), agricultural festivals (*Chumpha*, *Mangkhap*), and marriage rites (*Manom*).
   - **V. Ruivah (1993)** *The Tangkhul Nagas: An Anthropological Study*: Anthropological documentation of the *Longshim* youth dormitory system, youth festivals (*Yarra*), and *Yarnao* labor groups.
   - **K.S. Kasomwoshi (1991)** *Hao Tangkhul Chanjam*: Authoritative native-scholar anthology of traditional Tangkhul proverbs, customary jurisprudence maxims, and ethical teachings.
   - **S. Arokianathan (1982)** *Tangkhul Folk Literature* (CIIL Folklore Series): Oral romance ballad traditions (*Shimreishang Kala Maitonphi*) and indigenous metallurgical metaphors.
5. **Historical Archives, Chronicles, and Documents**:
   - **T. C. Hodson (1911)**, *The Naga Tribes of Manipur*: Primary ethnographic and colonial administrative monograph documenting sovereign village administration, chiefship (*Awunga*), clan lineages, and colonial interactions (Public Domain).
   - **Major W. McCulloch (1859)**, *Account of the Valley of Munnipore and of the Hill Tribes*: Pre-standardization vocabulary wordlists (Selections from the Records of the Government of India; Public Domain).
   - **G. A. Grierson (1903)**, *Linguistic Survey of India (LSI)* Vol. III, Part III: Comparative classification of the Tibeto-Burman language family and Tangkhul wordlists (Public Domain).
   - **Cheitharol Kumbaba** (The Royal Chronicle of the Kings of Manipur): State chronicle recording medieval and pre-colonial diplomatic treaties, tributes, and historical covenants between the Meitei Maharajas and Tangkhul hill chiefs.
   - **Assam Secretariat & Colonial War Office Records (1917–1918)**: Archival records documenting the recruitment, service, and France deployment of the 66th Manipur Labour Corps under R.S. Ruichumhao.
   - **WWII South East Asia Command & 50th Indian Parachute Brigade War Diaries (March 1944)**: Archival documentation of the Battle of Sangshak (delaying action against Japanese 31st Division).
   - **Tangkhul Long (TNL) & Tangkhul Literature Society (TLS) Archival Records (1935–present)**: Community historical minutes, constitution, and literary resolutions.
6. **Tangkhul Literature, Folktales, Poetry, and Drama**:
   - **Tangkhul Literature Society (TLS) Curriculum Readers & Drama** (via Bharatavani Portal):
     - *Tangkhul Tuitam Kachiko* (Class IX Reader, 2000): Features modern poetry (*Ava Ram Leishat* by Luingam A. Shimray) and realistic short stories (*Maranwon* by R. Shaiza).
     - *Tuitam Kathara* (Class X Reader, 2021): Matriculation reader featuring nature lyric poetry (*Shirui Kashongwui Won* by T. Luikham).
     - *Wordham Tuitam Khare* & *Wordham Tuitam Kakhane* (Classes XI & XII Readers, 2021): Higher secondary literature anthologies featuring social reflective verse (*Kachamwui Meikha* by Y.K. Shimray) and community renaissance poetry (*Ngashan Kathara* by S. Kanrei).
     - *Shongza* (TLS Dramatic Board, 2007): Full-length undergraduate collegiate drama addressing customary clan dispute arbitration, youth romance, and modern social reconciliation.
     - *Hao Khararchan: Tangkhul Folktales Collection* (TLS 1981): Canonical compilation of ancestral folktales (*Kashunao wui Khararchan*, etc.).
     - Primary curriculum moral fables: *Zingyar Tangkhul* (*Kachakui Kala Shanao*) and *Wontui Tangkhul* (*Sikui Kala Machun*).
   - **Central Institute of Indian Languages (CIIL) Archival Publications**:
     - *Tangkhul Folk Literature* (S. Arokianathan 1982): Scholarly folklore publication documenting the 17th-century Phungcham tragic romance ballad *Shimreishang Kala Maitonphi*, animal fables (*Huikhayei Kala Sha*), and traditional youth riddles (*Paochirun*).
   - **Early Translations and Archival Prose**:
     - *Kakashak Naomayawui Khararchan: Parable of the Prodigal Son in Tangkhul* (Rev. William Pettigrew 1903, in Grierson's *Linguistic Survey of India*, Vol. III, Part II; Public Domain): Earliest formally documented continuous narrative prose specimen in Tangkhul.
     - *Kristianwui Khangaran* (Tangkhul Christian Literature Committee 1953): Tangkhul translation of John Bunyan's *Pilgrim's Progress*.

---

## 3. Provenance Integrity Policy

- **No Synthetic Records**: Fabricated entries or machine-generated translations must never be presented as authentic Tangkhul language data.
- **Multi-Source Evidence**: When multiple sources attest a word (e.g. attested in a school textbook, a poem, and documented in a 1918 dictionary), all source citations are appended to the entry's provenance history without overwriting each other.
- **Quarantine of Candidate Data**: Unreviewed field notes or low-confidence OCR extracts remain isolated with `verification_status="needs_review"` or `"unverified"` until reviewed by native speaker scholars.
- **Clear Demarcation of Oral Traditions**: Oral history and migration traditions are clearly distinguished from independently corroborated archival or epigraphic evidence.

---

## 4. Step 13 Concrete Tangkhul Source Audit for Vocabulary Enrichment

Under Step 13, known historical, linguistic, and modern educational Tangkhul sources were systematically audited for legal accessibility, bibliographic metadata, and enrichment eligibility:

| Resource / Document | Creator(s) | Year | Manifest ID | Permission Tier | Processing Status |
|---|---|---|---|---|---|
| *Tangkhul Naga Grammar and Dictionary (Ukhrul Dialect)* | Rev. William Pettigrew | 1918 | `DIC-HIST-001` / `BK-HIST-001` | `public_domain` | **Eligible**: Lexicon and illustrative sentences extractable |
| *Tangkhul Primer and Catechism* | Rev. William Pettigrew | 1897 | `BK-HIST-002` | `public_domain` | **Eligible**: Running text extractable |
| *Linguistic Survey of India*, Vol. III, Part II | G. A. Grierson | 1903 | `DIC-LSI-001` / `BK-ARCH-001` | `public_domain` | **Eligible**: 241-word comparative list and text specimen |
| *Vocabulary of the Luhuppa (Tangkhul) Language* | Major M. McCulloch | 1859 | `DIC-HIST-002` | `public_domain` | **Eligible**: Historical Luhuppa wordlist extractable |
| *The Naga Tribes of Manipur* | T. C. Hodson | 1911 | Cited in 16 manifest records | `public_domain` | **Discovery Lead**: Specific cultural and linguistic passages |
| *The Lushai Kuki Clans* | J. Shakespear | 1912 | Archival Discovery | `public_domain` | **Discovery Lead**: Comparative border passages only (not a dictionary) |
| *Tangkhul Naga Phonetic Reader* | S. Arokianathan, E. Annamalai (ed.) | 1980 | `BK-CIIL-001` | `pending` | **Blocked**: Metadata only; pending formal permission |
| *Tangkhul Naga Grammar* | S. Arokianathan | 1987 | `BK-CIIL-002` | `pending` | **Blocked**: Metadata only; pending formal permission |
| *Tangkhul Folk Literature* | S. Arokianathan | 1982 | `BK-CIIL-003` / `LIT-ANTH-001` | `permitted` | Metadata & authorized cultural oral traditions |
| *Tangkhul-Naga Vocabulary* | D. N. S. Bhat | 1969 | `DIC-DC-001` / `BK-DC-001` | `restricted` | **Blocked**: Deccan College copyright; metadata only |
| *Tangkhul Tui Dictionary* | N. Luikham | 1997 | `DIC-TLS-001` | `restricted` | **Blocked**: Tangkhul Literature Society copyright; metadata only |
| *Tangkhul-English-Hindi Dictionary* | Rekha Sharma, S. Arokianathan, E. Annamalai | 1995 | `DIC-CIIL-001` | `restricted` | **Blocked**: CIIL copyright; metadata only |
| *Hindi-Tangkhul Dictionary* | B. B. Kumar et al. | 1975 | `DIC-NBP-001` | `restricted` | **Blocked**: Nagaland Bhasha Parishad copyright; metadata only |
| *CIIL Tangkhul Lexical Survey* | S. Arokianathan / CIIL | 1982 | `DIC-CIIL-002` | `restricted` | **Blocked**: CIIL audio archive; metadata only |
| *TLS Textbooks & Educational Wordbooks* (15 vols.) | Tangkhul Literature Society | 1981–2022 | `BK-TLS-001` to `015`, `DIC-TLS-002` | `pending` / `restricted` | **Blocked**: Educational curriculum copyright; metadata only |
