# Songs Module (`tangkhul_lib.songs`)

The **Songs** module is a core domain package in the Tangkhul Language Library. It provides structured song cataloguing, metadata validation, duplicate and alternate-recording detection, lyrics parsing, oral recording metadata tracking, and candidate vocabulary generation for traditional folk melodies, historical hymns, ceremonial verses, and modern Tangkhul musical compositions.

---

## 1. Module Purpose & Scope

Tangkhul oral literature is exceptionally rich in lyrical poetry, songcraft (*Laa*), and antiphonal chants. From ceremonial invocations sung during agricultural cycles (*Luira*, *Chumpha*) to mourning laments (*Thisham*), youth courting duets (*Khangrei*), and the legendary romantic ballad of *Shimreishang Kala Maitonphi*, songs are central to Tangkhul cultural and linguistic transmission.

The primary purposes of `tangkhul_lib.songs` are:
1. **Lyrical and Archival Preservation**: Catalogue traditional folk songs, historical songbooks, published anthologies, and contemporary recordings with verifiable metadata in [`data/manifests/songs.jsonl`](file:///f:/tangkhul-language-library/data/manifests/songs.jsonl).
2. **Audio/Video Recording Metadata**: Track performance and oral field recording metadata (performer, village, collector, recording date, media format, lyrics/transcript availability) without demanding local binary audio file downloads.
3. **Provenance-Preserving Lyrics Extraction**: Extract stanzas and line-by-line verses from authorized lyrics sources while recording exact line citations (`stanza_number:line_number`).
4. **Candidate Lexical Harvesting**: Harvest candidate vocabulary items and contextual sentences into the shared vocabulary repository ([`VocabularyEntry`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py) and [`ProvenanceRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py)) as unverified tokens, distinguishing archaic and poetic words from standard colloquial dictionary entries.
5. **Copyright and Permissions Governance**: Strictly enforce permission boundaries (`public_domain`, `permitted`, `community_authorized`, `metadata_only`, `restricted`) before extracting lyrics.

---

## 2. Catalogue Schema

Each song entry in [`data/manifests/songs.jsonl`](file:///f:/tangkhul-language-library/data/manifests/songs.jsonl) implements the [`SongRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/songs/models.py) schema:

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Stable unique identifier (e.g. `SNG-TRAD-001`, `SNG-MOD-001`). Required. |
| `title` | `str` | Primary song title in Tangkhul or English as documented. Required. |
| `alternate_titles` | `list[str]` | Alternate spellings, subtitle, or traditional variant titles. |
| `title_translation` | `str \| None` | English translation or gloss of the song title. |
| `singer` | `str \| None` | Primary vocal performer or singer. |
| `lyricist` | `str \| None` | Traditional composer or lyricist of the song. |
| `composer` | `str \| None` | Musical composer or arranger. |
| `collector` | `str \| None` | Ethnographer, researcher, or archivist who recorded the song. |
| `performers` | `list[str]` | Accompanying performers, choir, or band members. |
| `year` | `int \| None` | Year of composition, recording, or publication. |
| `village` | `str \| None` | Village of origin or performance location (e.g. `Phungcham`, `Choithar`, `Ukhrul`, `Hungpung`). |
| `dialect` | `str \| None` | Dialect variant (e.g. `Standard Tangkhul`, `Phungcham`, `Hundung`). |
| `song_type` | `str` | Genre classification (`folk`, `traditional`, `hymn`, `love_song`, `modern`, `ballad`, `ceremonial`, `lament`, `collection`). |
| `language` | `str` | Language of the work (default: `Tangkhul`). |
| `source_url` | `str \| None` | Primary documentation URL or canonical repository link. |
| `source_identifier` | `str \| None` | Cataloguing or archival ID (e.g. `CATA-NE-TRAD-001`, `Sanchika-CIIL-Audio-041`). |
| `recording_url` | `str \| None` | Direct audio/video streaming or archival URL. |
| `lyrics_source_url` | `str \| None` | Verified URL where song lyrics are documented. |
| `local_file_path` | `str \| None` | Local relative path if authorized lyrics file is retained. |
| `license` | `str \| None` | Licensing terms (`Public Domain`, `CC-BY-NC`, `Copyrighted`, etc.). |
| `permission_status` | `str` | One of: `pending`, `permitted`, `public_domain`, `community_authorized`, `restricted`. |
| `access_status` | `str` | One of: `metadata_only`, `full_text_available`, `restricted`, `open_access`, `unknown`. |
| `verification_status` | `str` | One of: `verified`, `needs_review`, `partially_verified`, `unverified`, `community_reviewed`. |
| `notes` | `str \| None` | Provenance context, ritual background, and cataloguing notes. |
| `recordings` | `list[dict]` | Associated audio/video performance metadata ([`SongRecording`](file:///f:/tangkhul-language-library/src/tangkhul_lib/songs/models.py)). |

### Associated Recording Schema (`SongRecording`)

A song can reference one or more recorded performances without conflating the song's identity with a specific recording:

| Field | Type | Description |
|---|---|---|
| `recording_id` | `str` | Unique recording identifier (e.g. `REC-SNG-001-A`). |
| `title` | `str` | Specific performance or track title. |
| `performer` | `str \| None` | Performer or narrator of this specific take. |
| `collector` | `str \| None` | Field researcher or sound engineer who recorded it. |
| `date_recorded` | `str \| None` | Date string (e.g. `2019-04-12` or `1982`). |
| `location` | `str \| None` | Village or recording studio location. |
| `media_format` | `str \| None` | Format (`mp3`, `wav`, `mp4`, `cassette`, `field_tape`). |
| `duration_seconds` | `int \| None` | Duration of the recording in seconds. |
| `has_transcript` | `bool` | Whether verified lyrical transcript is available. |
| `recording_url` | `str \| None` | Archival or stream link. |
| `permission_status` | `str` | Access permission (`metadata_only`, `open_access`, etc.). |

---

## 3. Research Sources & Discovery

The song records were researched and validated across five authoritative repositories and discovery channels:

1. **Tangkhul Lyrics (`tangkhullyrics.com`)**
   - Active community-maintained archive of contemporary Tangkhul gospel, modern, and folk song lyrics.
   - Provides verified titles, singers, and lyrics across contemporary Ukhrul and wider diaspora artists.
2. **Tangkhul Laa Lyrics (`tangkhullaa.com`)**
   - Repository of traditional *Hao Laa* lyrics, hymns, and popular folk melodies with attribution to songwriters and lyricists.
3. **Bharatavani Tangkhul Knowledge Resources (`sec.bharatavani.in/tangkhul/jnanakosha`)**
   - Central Institute of Indian Languages (CIIL) portal documenting Tangkhul folk literature, oral genres, and songbooks published in partnership with the Tangkhul Literature Society (TLS).
4. **CIIL Bhasha Sanchika Collection (`sanchika.ciil.org`)**
   - Collection `29bbe44e-238a-4d46-b979-97a0429a310e` containing audio recordings and field documentation of Tangkhul dialect varieties and folk songs recorded during linguistic surveys (Arokianathan 1980–1987).
5. **Miranda House Centre for Northeast Studies (CATA Archival Publications)**
   - Research publications documenting oral history, song traditions, and indigenous cultural expressions from Ukhrul and surrounding villages (`https://ibsdmirandahousecentrefornortheaststudies.wordpress.com/2017/04/04/3-april-2017/`).

---

## 4. Catalogued Song Records Breakdown

[`data/manifests/songs.jsonl`](file:///f:/tangkhul-language-library/data/manifests/songs.jsonl) contains **48 authentic records**:
- **Verified Records**: 47
- **Candidate Records**: 1 (`SNG-CAND-001` candidate oral recording from Phadang village)
- **Digitalized Full-Text Stanzas & Translations**: 48 songs available via `tangkhul_lib.songs.lyrics_data`, individual JSON/PDF exports, and CLI `--lyrics`.

### Traditional & Folk Songs (11 records)

| ID | Title | Genre | Village | Context / Significance |
|---|---|---|---|---|
| `SNG-TRAD-001` | Shimreishang Kala Maitonphi | Ballad | Phungcham | Legendary 17th-century Tangkhul tragic love ballad from Phungcham village. |
| `SNG-TRAD-002` | Haola: Luira Laa | Festival | Ukhrul | Spring seed-sowing festival song invoking prosperity and fertility (*Luira Phanit*). |
| `SNG-TRAD-003` | Haola: Chumpha Laa | Festival | Ukhrul | Harvest thanksgiving song sung during the entry of new grain into family granaries. |
| `SNG-TRAD-004` | Haola: Khangrei Laa | Folk | Ukhrul | Traditional youth dormitory courting song sung antiphonally by young men and women. |
| `SNG-TRAD-005` | Haola: Thisham Laa | Lament | Ukhrul | Traditional memorial soul-departure song sung during the *Thisham* feast of the dead. |
| `SNG-TRAD-006` | Haola: Ngashan Laa | Ceremonial | Ukhrul | Traditional ceremonial song celebrating ancestral heritage, shawl weaving, and attire. |
| `SNG-TRAD-007` | Haola: Mawon Laa | Lullaby | Ukhrul | Traditional folk lullaby and infant blessing conveying parental hopes and prosperity. |
| `SNG-TRAD-008` | Itang Rakhongli | Love Song | Hunphun | Classic lyrical love song invoking the mountain hills to lower their peaks for longing eyes. |
| `SNG-TRAD-009` | Yarra Laa: Yarshungwon | Festival | Hungpung | Traditional youth spring festival chant performed during *Yarra Phanit* courting. |
| `SNG-TRAD-010` | Mangkhap Laa: Ngaphit Kazang | Festival | Phungcham | Post-transplantation thanksgiving chant celebrating communal terrace labor. |
| `SNG-TRAD-011` | Hao Pheichak Laa | Ceremonial | Longpi | Antiphonal ceremonial warrior and celebration dance chant performed during festivals. |

### Historical Hymnals & Archival Songs (14 records)

| ID | Title | Compiler / Translator | Year | Significance |
|---|---|---|---|---|
| `SNG-HIST-001` | Jesuwui Laa | Rev. William Pettigrew | 1907 | Earliest known printed Tangkhul Christian hymnal (American Baptist Mission). |
| `SNG-HIST-002` | Christian Songs (1916) | Mission Congregation / CATA | 1916 | Scanned historical compilation of Christian songs printed in Roman script. |
| `SNG-HIST-003` | Jesuwui Laa No. 1: Ili Jesuna Laishi | Rev. William Pettigrew | 1907 | *Jesus Loves Me* in archaic 1907 Tangkhul orthography with 5 full stanzas (Tune 1155). |
| `SNG-HIST-004` | Jesuwui Laa No. 2: He Jesuwui Makali Ringphalaka | Rev. William Pettigrew | 1907 | *Safe in the Arms of Jesus* in classical Tangkhul translation with 2 stanzas (Tune 57). |
| `SNG-HIST-005` | Jesuwui Laa No. 3: Jesuwui Vang Nganinglu | Rev. William Pettigrew | 1907 | *Stand Up for Jesus* martial hymn celebrating spiritual steadfastness (Tune 680). |
| `SNG-HIST-006` | Jesuwui Laa No. 4: Jesuwui Aming Ngasoda | Rev. William Pettigrew | 1907 | *Take the Name of Jesus with You* 4 complete stanzas on peace and protection (Tune 91). |
| `SNG-HIST-007` | Jesuwui Laa No. 5: Jesu Nawui Ming Phaningda | Rev. William Pettigrew | 1907 | *Jesus, the Very Thought of Thee* 5 stanzas translated into classical Tangkhul (Tune 60). |
| `SNG-HIST-008` | Jesuwui Laa No. 8: Jesuwui Krushwui Pamli | Rev. William Pettigrew | 1907 | *Beneath the Cross of Jesus* 4 stanzas on redemption and devotion (Tune 139). |
| `SNG-HIST-009` | Jesuwui Laa No. 9: Arui Chimik Tunra | Rev. William Pettigrew | 1907 | *Now the Day Is Over* 7 stanzas evening prayer and lullaby (Tune 296). |
| `SNG-HIST-010` | Jesuwui Laa No. 10: Jesuwui Mi Chatsa | Rev. William Pettigrew | 1907 | *Onward, Christian Soldiers* 5 stanzas march and congregation anthem (Tune 706). |
| `SNG-HIST-011` | Jesuwui Laa No. 14: Ringkapha Tui Jesu Amai | Rev. William Pettigrew | 1907 | *Blessed Assurance* 3 stanzas with joyful refrain (Tune 873). |
| `SNG-HIST-012` | Jesuwui Laa No. 17: Arui Ngayali Ili Ngachonlu | Rev. William Pettigrew | 1907 | *Abide with Me* 6 complete stanzas on lifelong faith and hope (Tune 297). |
| `SNG-HIST-013` | Jesuwui Laa No. 28: Jesuna Ili Laishi | Rev. William Pettigrew | 1907 | *Jesus, Lover of My Soul* 4 stanzas on peace in spiritual storms (Tune 227). |
| `SNG-HIST-014` | Jesuwui Laa No. 31: Makashiman Lungkhuri | Rev. William Pettigrew | 1907 | *Rock of Ages* 4 stanzas on humility and divine refuge (Tune 237). |

### Folk Collections & Anthologies (2 records)

| ID | Title | Collector / Editor | Year | Significance |
|---|---|---|---|---|
| `SNG-COL-001` | The Tangkhul Folk Poetry in Song (HAOLA) | Dr. Ringkahao Horam | 2013 | Research compilation catalogued at CIIL Bhasha Sanchika. |
| `SNG-COL-002` | Folk Songs of the Tangkhul | H. Kamkhenthang | 1989 | Ethnographic collection published by Tribal Research Institute Manipur. |

### Modern & Folk Contemporary Songs (20 records)

| ID | Title | Genre | Singer / Artist | Village |
|---|---|---|---|---|
| `SNG-MOD-001` | Saharwon Kapaiwon | Folk | Rewben Mashangva | Choithar |
| `SNG-MOD-002` | Chihohaira | Festival | Rewben Mashangva | Choithar |
| `SNG-MOD-003` | Mayokachang Tam Wonrei | Folk | Rewben Mashangva | Choithar |
| `SNG-MOD-004` | Ngayang Kahai Leishat | Love Song | Rewben Mashangva | Choithar |
| `SNG-MOD-005` | Made in Ukhrul | Modern | Thangmeiso Shinglai | Ukhrul |
| `SNG-MOD-006` | Ningna Khamaya | Love Song | Thangmeiso Shinglai | Ukhrul |
| `SNG-MOD-007` | Nganam Kapha Won | Love Song | Thangmeiso Shinglai | Ukhrul |
| `SNG-MOD-008` | Huinahao | Folk | Thangmeiso Shinglai | Ukhrul |
| `SNG-MOD-009` | Iwui Mirinwui Khararchan | Ballad | Diana Wungsek | Ukhrul |
| `SNG-MOD-010` | Ramreichan | Patriotic | Diana Wungsek | Ukhrul |
| `SNG-MOD-011` | Ngathor Zingran Thada | Love Song | Diana Wungsek | Ukhrul |
| `SNG-MOD-012` | Kharao Amei | Love Song | Diana Wungsek & Thotreiso | Ukhrul |
| `SNG-MOD-013` | Iram Rakhongli | Folk | Nimshimphi Muivah | Ukhrul |
| `SNG-MOD-014` | Hunkhamang Mikumo Mirin | Ballad | Nimshimphi Muivah | Ukhrul |
| `SNG-MOD-015` | Ramna Ngateida | Modern | Nimshimphi Muivah | Ukhrul |
| `SNG-MOD-016` | Longkata Chara | Lament | Nimshimphi Muivah | Ukhrul |
| `SNG-MOD-017` | Achanwon | Love Song | Shimreingam Horam | Ukhrul |
| `SNG-MOD-018` | Awon Thada Rakhawon | Love Song | Shimreingam Horam | Ukhrul |
| `SNG-MOD-019` | Chingri Kahai | Ballad | Shimreingam Horam | Ukhrul |
| `SNG-MOD-020` | Mailemphy | Love Song | Shimreingam Horam | Ukhrul |

### Candidate Oral Recording (1 record)

| ID | Title | Village | Collector | Status |
|---|---|---|---|---|
| `SNG-CAND-001` | Phadang Village Harvest Chant | Phadang | Linguistic Survey Field Team | Needs Review (`needs_review`) |

---

## 5. Duplicate Detection & Version Linking

In oral traditions, songs exist in multiple recordings, covers, village dialects, and lyrical variants. Destructively merging records causes data loss and corrupts dialect provenance.

The [`SongCatalogue`](file:///f:/tangkhul-language-library/src/tangkhul_lib/songs/catalogue.py) implements non-destructive duplicate and alternate version detection:
- `find_likely_duplicates(song)`: Identifies songs with identical normalized titles and performers or source URLs.
- `find_alternate_versions(song)`: Detects versions sharing the same song title but performed by different singers, belonging to different villages, or representing dialect variants (e.g. *Manganuishon* recorded by Nimshimphi Muivah vs. Rewben Mashangva).

---

## 6. Lyrics Extraction & Permissions Enforcement

The [`SongLyricsExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/songs/extractor.py) extracts lyrics while strictly observing copyright and access boundaries:

```python
from tangkhul_lib.songs.extractor import SongLyricsExtractor
from tangkhul_lib.songs.models import SongRecord

extractor = SongLyricsExtractor()

# Attempting extraction on restricted or metadata_only records raises PermissionDeniedError
try:
    extractor.extract_lyrics_file(song, enforce_permissions=True)
except PermissionDeniedError:
    print("Full lyrics extraction blocked: Record is metadata_only or restricted.")
```

When permitted:
1. **Stanza and Line Parsing**: Splits lyrics into stanzas separated by blank lines and tracks `(stanza_idx, line_idx, line_text)`.
2. **Spacing and Orthography Sanitization**: Normalizes Unicode punctuation while preserving Tangkhul diacritics and vowels (`ā`, `ō`).
3. **Line-Level Citations**: Generates citations formatted as `Stanza 1, Line 2` for all extracted text.

---

## 7. Vocabulary Integration & Provenance

When lyrics are processed, candidate tokens are extracted using [`extract_vocabulary_candidates`](file:///f:/tangkhul-language-library/src/tangkhul_lib/songs/extractor.py):

- **Zero Invention**: Candidates preserve exact original surface forms. Definitions are **never** fabricated.
- **Provenance Linkage**: Each token links to [`ProvenanceRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/models.py) referencing `song_id`, stanza number, line number, and full context sentence.
- **Quarantine Partition**: Candidate tokens are labeled `verification_status="unverified"` and stored in the database's `extracted_tokens` table, completely isolated from confirmed dictionary headwords until verified by language experts.

---

## 8. CLI Usage Guide

The CLI exposes song catalogue queries via the `tangkhul songs` subcommand:

### List All Catalogued Songs
```bash
tangkhul songs --list
```

### Search by Keyword, Title, or Topic
```bash
tangkhul songs --search "Shimreishang"
tangkhul songs --search "Luira"
```

### Retrieve Full Song Details by ID
```bash
tangkhul songs --id SNG-TRAD-001

# Display complete lyrics stanzas and bilingual line glosses
tangkhul songs --id SNG-HIST-003 --lyrics

# Display full metadata together with all lyrics and translations
tangkhul songs --id SNG-TRAD-008 --full
```

### Filter by Genre / Song Type
```bash
tangkhul songs --type folk
tangkhul songs --type love_song
tangkhul songs --type hymn
```

### Filter by Singer / Performer
```bash
tangkhul songs --singer "Rewben Mashangva"
tangkhul songs --singer "Diana Wungsek"
```

### Filter by Village
```bash
tangkhul songs --village "Phungcham"
tangkhul songs --village "Choithar"
```

---

## 9. Instructions for Adding New Song Records

1. **Verify Authenticity**: Confirm the song has documented roots in Tangkhul community life, verified artist recordings, published songbooks, or archival records.
2. **Assign a Stable ID**:
   - `SNG-TRAD-xxx` for traditional folk melodies, chants, and ballads.
   - `SNG-HIST-xxx` for historical hymnals or early printed songbooks.
   - `SNG-COLL-xxx` for published song anthologies.
   - `SNG-MOD-xxx` for modern, recorded, or published songs.
   - `SNG-ORAL-xxx` for candidate oral field recordings.
3. **Verify Permission**: Mark `permission_status` as `public_domain` for pre-1950 traditional folk works, `permitted` if authorized by the creator, or `restricted` / `metadata_only` if copyright is unconfirmed.
4. **Append to Manifest**: Add the JSON line to [`data/manifests/songs.jsonl`](file:///f:/tangkhul-language-library/data/manifests/songs.jsonl).
5. **Run Validation**:
   ```bash
   python scripts/validate_manifests.py
   pytest
   ruff check .
   ```
