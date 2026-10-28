# Culture Module (`tangkhul_lib.culture`)

The **Culture** module is a core domain package in the Tangkhul Language Library. It provides structured ethnographic cataloguing for Tangkhul proverbs (*Paotam* / *Chanjam*), traditional customs, annual agricultural and memorial festivals, textile and basketry arts, rituals, and oral narratives; permission- and consent-enforcing extraction; conflict and regional variant detection; and deep integration with the library's unified vocabulary database.

---

## 1. Module Purpose & Objectives

Tangkhul cultural heritage embodies centuries of oral wisdom, community governance, mountain agriculture, and ceremonial art. Documented in early historical ethnographies (T.C. Hodson 1911, William Pettigrew 1918), indigenous sociological studies (M. Horam 1977, V. Ruivah 1993, K.S. Kasomwoshi 1991), institutional collections (CIIL Bhasha Sanchika, Bharatavani Jnanakosha & Bhashakosha), and publications of the Tangkhul Literature Society (TLS), this heritage requires responsible preservation that respects cultural sensitivity and intellectual property.

The primary objectives of `tangkhul_lib.culture` are:
1. **Authentic Source Cataloguing**: Systematically catalogue authentic Tangkhul cultural practices, proverbs, customs, and oral narratives with verified bibliographic citations in [`data/manifests/culture.jsonl`](file:///f:/tangkhul-language-library/data/manifests/culture.jsonl).
2. **Culturally Sensitive Knowledge Governance**: Support access tiers (`community_authorized`, `public_domain`, `restricted`, `pending`) and consent tracking to safeguard sacred ceremonial incantations (*Khamasit*) and private community lore from unauthorized public export.
3. **Preservation of Regional Variations**: Document village-specific practices (e.g. Ukhrul / Hunphun, Phungcham, Champhung, Makhel) without presenting one village's custom as universal across all Tangkhul communities.
4. **Lexicon Integration**: Harvest candidate vocabulary, dialect terms, and illustrative context sentences from authorized cultural records into the unified [`VocabularyRepository`](file:///f:/tangkhul-language-library/src/tangkhul_lib/storage/repositories.py) with multi-source provenance.
5. **Search & Discovery**: Provide robust filtering across categories, villages, dialects, occasions, and verification statuses via the `tangkhul culture` CLI and programmatic APIs.

---

## 2. Catalogue Schema (`CulturalRecord`)

Each cultural resource in [`data/manifests/culture.jsonl`](file:///f:/tangkhul-language-library/data/manifests/culture.jsonl) implements [`CulturalRecord`](file:///f:/tangkhul-language-library/src/tangkhul_lib/culture/models.py):

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Stable unique identifier (e.g. `CULT-FEST-001`, `CULT-PROV-001`). Required. |
| `title` | `str` | Title or common designation of the cultural entity. Required. |
| `category` | `str` | Primary category (`proverb`, `custom`, `festival`, `ritual`, `tradition`, `oral_tradition`). Required. |
| `local_name` | `str \| None` | Indigenous Tangkhul name (e.g. *Luira Phanit*, *Haora*, *Khamasit*). |
| `alternate_names` | `list[str]` | Alternate spellings, colloquial titles, or dialect designations. |
| `subcategory` | `str \| None` | Domain subcategory (e.g. `agricultural`, `attire`, `justice`, `wisdom`, `governance`). |
| `original_text` | `str \| None` | Verbatim Tangkhul text (proverbs, chants, sayings) when documented. |
| `translation_en` | `str \| None` | English translation or meaning of the original text. |
| `translations_other` | `list[str]` | Translations in Hindi, Meiteilon, or other languages. |
| `description` | `str \| None` | Descriptive cultural account and ethnographic interpretation. |
| `cultural_significance` | `str \| None` | Symbolic meaning, purpose, ethics, or spiritual context. |
| `season_or_timing` | `str \| None` | Calendar timing, agricultural phase, or time of day (e.g. `January/February`, `Post-harvest`). |
| `village` | `str \| None` | Specific village origin or association (e.g. `Hunphun`, `Ukhrul`, `Phungcham`, `Champhung`). |
| `dialect` | `str \| None` | Language variety or dialect documented (e.g. `Ukhrul`, `Phungcham`, `Standard Tangkhul`). |
| `language` | `str` | Language name (default: `Tangkhul`). |
| `participants` | `list[str]` | Community groups or roles involved (e.g. `Awunga`, `Hangva`, `Youth`, `Women`). |
| `procedure` | `list[str]` | Chronological sequence or procedural steps of the custom or ritual. |
| `related_records` | `list[str]` | Cross-references to related songs, books, dictionary entries, or cultural records. |
| `historical_period` | `str \| None` | Historical era or period (e.g. `17th Century`, `Pre-colonial`). |
| `year` | `int \| None` | Publication or recording year. |
| `source_id` | `str \| None` | Source identifier (e.g. `Hodson-1911-Ch3`, `Kasomwoshi-Chanjam-014`). |
| `source_title` | `str \| None` | Publishing work or source title (e.g. `The Naga Tribes of Manipur`). |
| `source_page` | `str \| None` | Page reference in the source. |
| `source_section` | `str \| None` | Chapter or section locator. |
| `source_url` | `str \| None` | Canonical repository link or digital landing page. |
| `contributor` | `str \| None` | Informant, elder, author, or documenting institution. |
| `contributor_consent` | `bool` | Whether consent was given for extraction and publication (default: `True`). |
| `license` | `str \| None` | Governing license (e.g. `Public Domain`, `Traditional Cultural Expression`). |
| `permission_status` | `str` | One of: `community_authorized`, `public_domain`, `restricted`, `pending`, `permitted`. |
| `access_status` | `str` | One of: `metadata_only`, `open_access`, `restricted`, `attributed`, `permission_pending`. |
| `verification_status` | `str` | One of: `verified`, `needs_review`, `partially_verified`, `unverified`. |
| `notes` | `str \| None` | Ethnographic commentary, context, and reviewer observations. |

---

## 3. Researched Tangkhul Cultural Domains

The catalogue in [`data/manifests/culture.jsonl`](file:///f:/tangkhul-language-library/data/manifests/culture.jsonl) documents **35 authentic cultural records** across six distinct genres:

### A. Festivals (*Phanit*)
Tangkhul seasonal life revolves around agricultural feasts and ancestral celebrations:
- **`CULT-FEST-001` (Luira Phanit)**: The principal seed-sowing spring festival celebrated in January/February marking the inauguration of the agricultural cycle. Features ceremonial sod-turning by the *Awunga* (hereditary chief), wrestling (*Kaphung*), and sacred dances.
- **`CULT-FEST-002` (Chumpha Phanit)**: The post-harvest thanksgiving festival celebrated in December, specially honoring women as granary custodians and blessing communal food security.
- **`CULT-FEST-003` (Mangkhap Phanit)**: Mid-summer feast of rest celebrated in July following arduous terrace paddy transplantation.
- **`CULT-FEST-004` (Thisham Phanit)**: Feast of departing souls held in winter, guiding the spirits of family members deceased during the year to *Kasa Akhava* (ancestral realm) with pine torches.
- **`CULT-FEST-005` (Yarra Phanit)**: Spring youth festival hosted within village dormitories (*Longshim*) celebrating camaraderie, folk songs, and feast exchanges.
- **`CULT-FEST-006` (Dharreo Phanit)**: Autumn pre-harvest blessing festival celebrated in October before sickle touches the standing grain, praying for protection against storms and vermin.
- **`CULT-FEST-007` (Khamang Phanit)**: Autumn communal river expedition where river channels are treated with pulverized wild walnut root (*Ngasung*) to stun fish, accompanied by riverside fellowship banquets.

### B. Traditional Sayings & Proverbs (*Paotam* / *Chanjam*)
Indigenous moral and customary philosophy preserved in poetic couplets:
- **`CULT-PROV-001`**: *"Hanna hannui shaiphamei, tuiva arartui phamei"* — Tender greens are tasty, but elder counsel is sweeter (values intergenerational wisdom over youthful impulse).
- **`CULT-PROV-002`**: *"Nguihaowada masi kongra li machikhai paimana"* — A person cannot be drowned for a mistake (Tangkhul customary jurisprudence prioritizes restitution and reconciliation).
- **`CULT-PROV-003`**: *"Khamor kachangna phei ngazekli"* — Sharp words pierce deeper than spear wounds (warning on verbal ethics).
- **`CULT-PROV-004`**: *"Faphei meikachui thalakli"* — Making a fuss like a dog with a singed paw (satirizes theatrical overreaction).
- **`CULT-PROV-005`**: *"Ava ram shungli leishat mathamei"* — No love is greater than love for the motherland (patriotic reverence for ancestral land).
- **`CULT-PROV-006`**: *"Shiyan mahara ngalemli"* — Iron is tempered by striking (indigenous metallurgy metaphor for moral resilience).
- **`CULT-PROV-007`**: *"Theikahaina kaphaningli, matheikahaina mikli"* — The wise perceive with the mind, the foolish perceive only with the eyes (discernment over superficial appearance).
- **`CULT-PROV-008`**: *"Khare khangatei makhangaza, thot khangatei maharmana"* — Habit is hard to alter, but transforming a generation requires steadfast wisdom.

### C. Customs, Clans & Community Institutions
- **`CULT-CUST-001` (Longshim)**: The traditional youth dormitory system (divided into *Mayarshim* for boys and *Ngashim* for girls), functioning as the academy for transmitting customary lore, songs, weaving, and craft skills.
- **`CULT-CUST-002` (Hangva)**: The customary council of village clan elders assisting the hereditary chief (*Awunga*) in dispute arbitration and boundary governance.
- **`CULT-CUST-003` (Yarnao)**: Cooperative labor exchange peer groups rotating farm labor across terraced mountain fields.
- **`CULT-CUST-004` (Manom)**: Customary exogamous marriage negotiations, presentation of handwoven shawls, and communal feasting.
- **`CULT-CUST-005` (Maran Kasa & Tarang)**: The pinnacle feast of merit cycle hosted by a benefactor, granting the prerogative to erect the forked sacred *Tarang* post and build a *Lengcheng Shim*.
- **`CULT-SOC-001` (Tangkhul Clan System & Social Order)**: Comprehensive codification clarifying the complete absence of caste stratification; detailing the 11 major patrilineal clans (*Shang / Shangnao*: Shimray, Luikham, Kasomwoshi, Zimik, Vashum, Shaiza, Ruivah, Shingnaisui, Sareo, A'Shao, etc.), strict clan exogamy rules (*Shang wui Shimlut*), and hereditary village democracy (*Awunga* and *Hangva*).

### D. Material Culture, Architecture & Traditional Crafts
- **`CULT-TRAD-001` (Haora)**: Renowned traditional handwoven men's shawl with red, white, and black bands, accented by delicate *Ramik* (peacock eye) edge embroidery.
- **`CULT-TRAD-002` (Chonkhom)**: Prestigious red-based women's shawl worn during weddings and solemn ceremonies.
- **`CULT-TRAD-003` (Seichan Kashan)**: Intricately patterned handwoven wraparound skirt featuring ancestral geometric motifs.
- **`CULT-TRAD-004` (Longkhor)**: Handcrafted conical bamboo basket with head tumpline for mountain agricultural transport.
- **`CULT-TRAD-005` (Longpi Hamlei)**: Ancient indigenous black serpentinite stone pottery of Longpi village, crafted without a wheel and polished with *Mahasa/Chiron* leaves.
- **`CULT-TRAD-006` (Lengcheng Shim)**: Traditional high-status house architecture featuring carved facade relief planks and crossed wooden roof-horns (*Lengcheng Kui*).
- **`CULT-TRAD-007` (Kalhang Salt-Making)**: Indigenous mineral salt extraction from natural mountain brine wells (*Machi kong*), boiled into solid circular salt currency cakes.

### E. Documented Rituals, Prayers & Ceremonies
- **`CULT-PRAY-001` (Tangkhul Traditional Prayers & Invocations)**: Comprehensive archive of invocations to the Supreme Creator (*Varivara-li Hai-kaphā*), agricultural seed-sowing chants, sacred hearth kindling (*Meiphung Kathara*), wilderness wayfarer protection (*Khayang Shongfa*), and ancestral memorial chants (*Thisham Kasa Akhava*).
- **`CULT-RIT-001` (Khamasit)**: Solemn village boundary closure and taboo (*genna*) days observed to maintain balance with spiritual entities. Esoteric sacred formulas remain restricted.
- **`CULT-RIT-002` (Luira Shimlut-Kaphung)**: Dawn sod-turning ritual performed by the village chief before any villager may commence field planting.
- **`CULT-RIT-003` (Tangkhul Sacred Rituals, Ceremonies & Taboos)**: Master codification of agrarian seasonal cycles, lifecycle rites of passage (birth, naming, youth dormitory induction, marriage, house dedication, death), prestige feast cycles (*Maran Kasa*), chiefly enthronement, and sacred taboo (*Khamthei*) boundaries.
- **`CULT-CAND-001` (Champhung Monolith Rites)**: Fieldwork documentation on megalith pulling rites under review for clan clearance.

### F. Oral Traditions & Narratives
- **`CULT-ORAL-001` (Shimreishang Kala Maitonphi)**: The 17th-century Phungcham tragic romance tradition preserving archaic dialect vocabulary and mourning laments.
- **`CULT-ORAL-002` (Makhel Dispersal)**: Sacred ancestral narrative recounting the common dispersal of clans from Makhel under the wild pear tree.

---

## 4. Responsible Handling of Culturally Sensitive Knowledge

Tangkhul indigenous knowledge contains sacred, lineage-restricted, and ceremonial elements. The Culture Module enforces responsible stewardship:
- **No Blanket Public Domain Assumption**: Living oral contributions and field recordings require explicit consent (`contributor_consent=True`).
- **Restricted Access Enforcement**: Records marked `permission_status="restricted"` or `access_status="restricted"` are strictly excluded from automated vocabulary harvesting and public JSONL/CSV exports unless explicitly overridden.
- **Attribution & Context Preservation**: The specific village origin, dialect variety, and publishing source are permanently attached to prevent homogenization across the diverse Tangkhul region.
- **Review Workflow**: Records pending community clearance (e.g. `CULT-CAND-001`) are flagged as `needs_review` and separated from verified public documentation.

---

## 5. Vocabulary Integration with Shared Lexicon

The Culture Module integrates natively with [`tangkhul_lib.vocabulary`](file:///f:/tangkhul-language-library/src/tangkhul_lib/vocabulary/):
- **Candidate Harvesting**: [`CultureExtractor.extract_from_record()`](file:///f:/tangkhul-language-library/src/tangkhul_lib/culture/extractor.py) extracts terms and expressions from authorized records.
- **Lexicon Synchronization**: [`CultureRepository.sync_record_to_vocabulary()`](file:///f:/tangkhul-language-library/src/tangkhul_lib/storage/repositories.py) checks whether candidate headwords already exist in [`VocabularyRepository`](file:///f:/tangkhul-language-library/src/tangkhul_lib/storage/repositories.py). If found, it enriches the entry's provenance (`resource_type="culture"`) without overwriting dictionary definitions. If new, it adds a candidate entry with `needs_review` status.
- **Leakage Prevention**: Synchronizing or harvesting from restricted cultural records raises [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py), guaranteeing sensitive ritual terms cannot leak into public vocabulary databases.

---

## 6. CLI Command Reference

The `tangkhul culture` CLI provides full catalogue search and inspection capabilities:

```bash
# 1. List all catalogued cultural records
tangkhul culture --list

# 2. Search by keyword across title, local name, proverbs, and description
tangkhul culture --search "Luira"

# 3. Display full metadata for a specific cultural record
tangkhul culture --id CULT-FEST-001

# 4. Filter by cultural category (e.g. proverb, festival, custom, tradition, ritual)
tangkhul culture --category proverb
tangkhul culture --category festival

# 5. Filter by village origin or village-associated dialect
tangkhul culture --village Ukhrul
tangkhul culture --village Phungcham

# 6. Filter by dialect variety
tangkhul culture --dialect Ukhrul
tangkhul culture --dialect Phungcham

# 7. Filter by verification status (e.g. verified, needs_review)
tangkhul culture --verification-status needs_review
```

---

## 7. Python API Examples

### Loading Catalogue and Querying Records

```python
from pathlib import Path
from tangkhul_lib.culture.catalogue import CultureCatalogue

manifest_path = Path("data/manifests/culture.jsonl")
catalogue = CultureCatalogue.load_from_manifest(manifest_path)

# Retrieve a single record
luira = catalogue.get_record("CULT-FEST-001")
print(f"{luira.title} ({luira.translation_en}) - Village: {luira.village}")

# Search proverbs
proverbs = catalogue.search_records(category="proverb")
for p in proverbs:
    print(f"[{p.id}] {p.title}: {p.original_text}")

# Generate status report
report = catalogue.get_culture_report()
print(f"Total: {report['total_records']}, Verified: {report['verified_count']}, Restricted: {report['restricted_count']}")
```

### Permission-Governed Vocabulary Synchronization

```python
from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository, VocabularyRepository

db_manager = DatabaseManager(Path("data/database/tangkhul_corpus.sqlite"))
db_manager.initialize_schema()

cult_repo = CultureRepository(db_manager)
vocab_repo = VocabularyRepository(db_manager)

record = cult_repo.get_by_id("CULT-PROV-001")
if record:
    # Extracts candidate tokens and attaches culture provenance to unified vocabulary
    synced_entries = cult_repo.sync_record_to_vocabulary(record, vocab_repo)
    print(f"Synchronized {len(synced_entries)} vocabulary entries.")
```

---

## 9. Digital Exports & Compendium Documentation

All 32 catalogued cultural heritage records are exported into structured, persistent digital formats:

1. **Consolidated Cultural Collections**:
   - [`data/exports/culture.json`](file:///f:/tangkhul-language-library/data/exports/culture.json) & [`src/tangkhul_lib/data/culture.json`](file:///f:/tangkhul-language-library/src/tangkhul_lib/data/culture.json): Complete collection containing verbatim Tangkhul texts, English glosses, procedural sequences, ceremonial participants, and seasonal timings.
   - [`data/exports/culture.pdf`](file:///f:/tangkhul-language-library/data/exports/culture.pdf): 33-page Master Cultural Heritage Compendium with Cover Page, Table of Cultural Resources, and full ethnographic accounts.
2. **Individual Cultural Documents**:
   - [`data/exports/culture/`](file:///f:/tangkhul-language-library/data/exports/culture): 32 individual JSON documents (`{id}.json`) and 32 individual PDF documents (`{id}.pdf`).
3. **Raw Plaintext Files**:
   - [`data/raw/culture/`](file:///f:/tangkhul-language-library/data/raw/culture): 32 structured plaintext files with bibliographic headers, Tangkhul proverbs/chants, and procedural stages.
