# Licensing, Copyright, and Cultural Permissions

Preserving indigenous and regional languages requires strict adherence to ethical, legal, and community guidelines.

---

## 1. Project Software Licensing

- The code and tooling in this repository are developed for non-commercial educational, scholarly, and cultural preservation purposes.
- The open-source license for this repository is in active development with community and linguistic stakeholders.
- No assumption of public licensing or unilateral redistribution is made without explicit confirmation.

---

## 2. Cultural & Indigenous Heritage Permissions

Tangkhul proverbs, sacred festival rituals (*Luira*, *Chumpha*), traditional songs (*Haola*), oral narratives (*Khararchan*), and clan histories belong to the Tangkhul community.

### Principles:
1. **Community Sovereignty**: Cultural knowledge recorded in this library must respect traditional custodianship and indigenous intellectual property.
2. **Non-Commercial Research Use**: Linguistic corpora and cultural items are collected exclusively for non-commercial education, cultural preservation, and scholarly linguistic research.
3. **No Commercial Exploitation**: Scraping or repackaging cultural records or indigenous lexicons for commercial profit without community consent is strictly forbidden.
4. **Takedown & Correction Policy**: Community elders, authors, or custodians may request corrections, additions, or removal of sensitive recordings.

---

## 3. Data Ingestion Permission Tiers

Manifest records track permission status through explicit tiers:

- `public_domain`: Out-of-copyright historical works (e.g. pre-1925 publications: Pettigrew 1918, Grierson 1903, McCulloch 1859). Full-text extraction and vocabulary harvesting permitted.
- `permitted`: Contemporary publications where written permission from authors/publishers has been obtained.
- `community_authorized`: Traditional knowledge, oral literature, and folk recordings shared with community consent.
- `restricted`: In-copyright or sensitive materials indexed for bibliographic reference only (`access_status="metadata_only"`). Extraction is blocked by [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py).
- `pending`: Resources currently under copyright and permission review.

---

## 4. Specific Domain Permission Rules

### A. Books Module
- TLS textbooks indexed via Bharatavani are catalogued with bibliographic metadata. Full text is extracted only where permitted.

### B. Songs Module
- Traditional folk melodies and oral ballads (*Hao Laa*, *Shimreishang Kala Maitonphi*) are catalogued under `community_authorized` (Traditional Oral Heritage), respecting indigenous community ownership rather than classifying living heritage as expired statutory public domain.
- Contemporary recordings (Rewben Mashangva, Diana Wungsek, etc.) are catalogued as metadata only with canonical source links. Full commercial lyrics are not scraped without artist license.

### C. Dictionaries Module
- Modern copyrighted dictionaries (N. Luikham 1997 *Tangkhul Tui Dictionary*, CIIL 1995 *Tangkhul-English-Hindi Dictionary*, Nagaland Bhasha Parishad 1975 *Hindi-Tangkhul Dictionary*) are catalogued for bibliographic discovery as `metadata_only`.
- Public domain historical dictionaries (William Pettigrew 1918) permit full lexical entry extraction and synchronization with the unified vocabulary database.
- Exporting entries via `DictionaryCatalogue.export_entries_jsonl()` automatically excludes restricted entries by default.

### D. Culture Module
- Traditional cultural expressions, proverbs (*Paotam* / *Chanjam*), and public festivals (*Luira*, *Chumpha*, *Mangkhap*, *Thisham*) are catalogued under `community_authorized` (Traditional Oral Heritage), with verified pre-1925 publications (Pettigrew 1918) classified as `public_domain`.
- Sacred ceremonial formulas, taboo boundary rites (*Khamasit*), and esoteric clan monolith rites are marked `restricted` or `pending` community clearance.
- Contributor consent is tracked via `contributor_consent`; withholding consent blocks automated extraction.
- Automated token extraction and public catalogue exports (`export_jsonl`, `export_csv`) strictly omit restricted cultural records by default. Attempts to force extraction raise [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py).

### E. History Module
- Historical administrative records and out-of-copyright colonial publications (T.C. Hodson 1911, G.A. Grierson 1903, Major W. McCulloch 1859, Pettigrew 1918) are catalogued as `public_domain`.
- Oral histories, clan genealogies, and village-specific dispute narratives require explicit contributor consent (`contributor_consent=True`). Where clan clearance is pending or restricted, records are marked `restricted` or `pending` with `access_status="metadata_only"`.
- Automated extraction via [`HistoryExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/history/extractor.py) and vocabulary synchronization strictly block restricted historical text, raising [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py).
- Public exports (`export_jsonl`, `export_json`, `export_csv`) omit restricted historical records by default to prevent unauthorized leakage of private community heritage.

### F. Literature Module
- Out-of-copyright literature (Rev. William Pettigrew 1903 *Kakashak Naomayawui Khararchan* in Grierson's LSI) is catalogued as `public_domain`, enabling full-text linguistic processing and historical syntax analysis.
- Traditional oral folktales (*Khararchan*), ballads (*Shimreishang Kala Maitonphi*), and animal fables published in CIIL Folklore series or TLS collections are catalogued under `community_authorized`.
- Modern published poems (Luingam A. Shimray, Y.K. Shimray, T. Luikham, S. Kanrei), short stories (R. Shaiza, K.S. Kasomwoshi, V. Ruivah), and drama (*Shongza* 2007) are indexed for educational and bibliographic discovery with `access_status="metadata_only"`. Complete modern literary works are never scraped or reproduced without explicit author or TLS authorization.
- Automated text extraction via [`LiteratureExtractor`](file:///f:/tangkhul-language-library/src/tangkhul_lib/literature/extractor.py) and lexicon synchronization via `LiteratureRepository.sync_record_to_vocabulary` strictly verify permission status and contributor consent, raising [`PermissionDeniedError`](file:///f:/tangkhul-language-library/src/tangkhul_lib/core/exceptions.py) if restricted.
- Public exports (`export_jsonl`, `export_csv`) filter out restricted literary works by default.

---

## 5. Ingestion Pipeline Permission Gates (Step 11)

The document ingestion pipeline (`tangkhul ingest`) implements strict pre-flight authorization checks before reading or parsing any local document file:

1. **Mandatory Explicit Permission**:
   - Files can only be ingested if associated with an existing source manifest record whose permission status is explicitly `permitted`, `public_domain`, or `community_authorized`.
   - Records with status `pending`, `restricted`, or missing permission metadata are strictly skipped.
   - Candidate records with `verification_status="needs_review"` are not ingested automatically, even if local files exist.

2. **No Assumptions Based on Age or Catalogues**:
   - Publication date, out-of-print status, or archival listings do not confer permission to ingest full text without verified public domain status (e.g. pre-1925) or explicit authorization.
   - Missing metadata is never fabricated.

3. **Restricted Content Shielding**:
   - Paragraph chunks and extracted tokens inherit source permission and access classifications.
   - Restricted or unverified chunks are excluded from SQLite FTS5 search indexing (`document_chunks_fts`).

4. **Vocabulary Candidate Quarantine**:
   - Machine-extracted tokens from newly ingested documents are quarantined with `verification_status="unverified"` and an empty definitions list until validated by a linguist or community reviewer.
   - Machine extraction never invents English definitions or linguistic meanings.

---

## 6. Vocabulary Review and Community Validation Ethics (Step 12)

Human validation of vocabulary entries must respect community intellectual sovereignty, privacy, and linguistic integrity:

1. **Restricted Context Shielding**:
   - Context sentences drawn from records marked `restricted` or taboo cultural practices (such as *Khamasit*) are masked during candidate inspection, interactive review sessions, and community JSONL exports.
   - Example sentences from unverified or restricted records are never published into open search indexes.

2. **Immutable Source Permissions**:
   - Accepting, editing, or linking a vocabulary candidate modifies only lexical attributes and verification status in the vocabulary layer. It **never** alters the permission status of underlying bibliographic source manifests (e.g. in `books.jsonl` or `culture.jsonl`).

3. **Ethical Attribution & Accountability**:
   - All review decisions (`accept`, `reject`, `flag`, `duplicate`, `edit`) record real reviewer identifiers or authenticated community pseudonyms with timestamps. Fabricating reviewer approvals or community endorsement is prohibited.

4. **Preservation of Dialect Diversity**:
   - Village varieties and non-standard dialect spellings (such as Northern Raphei forms) must never be rejected solely because they diverge from standard Ukhrul orthography. They should be verified as dialect variants with accurate village attribution.

---

## 7. Vocabulary Enrichment Permission Boundaries (Step 13)

Vocabulary expansion and lexicon enrichment must strictly respect source licenses, copyright boundaries, and cultural privacy:

1. **Prohibition on Unauthorized Extraction**:
   - Sources marked `restricted` (such as modern copyrighted dictionaries by TLS, CIIL, or Nagaland Bhasha Parishad) or `pending` cannot be processed for vocabulary extraction.
   - Extraction attempts on ineligible sources raise `PermissionDeniedError` or produce explicit skip reports without touching local source text.

2. **Protection of Human-Reviewed Definitions**:
   - Existing human-reviewed or community-accepted definitions are immutable against automated overwriting during enrichment. Newly extracted candidates with matching headwords append source citations and non-conflicting example sentences only.

3. **Shielded Offline Community Review Exports**:
   - When exporting candidates for community review (`tangkhul enrich --export-candidates`), example sentences originating from restricted records are replaced with `[RESTRICTED TEXT - ACCESS PRIVILEGED]`.

4. **No Automated Merging**:
   - Phonetic and orthographic similarities are surfaced strictly as suggestions for human review. Dialect variants and polysemous senses are preserved distinct.

---

## 8. Multi-Reviewer Consensus & Source Clearance Separation (Step 14)

Step 14 establishes explicit boundaries separating linguistic review consensus from source evidence verification and copyright/cultural permission clearance:

1. **Decoupling of Linguistic Approval from Public Release**:
   - A vocabulary candidate can achieve unanimous linguistic approval (e.g., native speakers confirming its accurate spelling and grammatical meaning) without being cleared for public distribution.
   - Promotion to `verification_status="verified"` and public search index inclusion strictly requires:
     1. Multi-reviewer consensus meeting the configured threshold (default: 2 independent eligible reviewers).
     2. Valid, traceable source evidence citations in catalogued library manifests.
     3. Complete clearance from copyright and cultural access restrictions (`permission_status != 'restricted'`).
   - If a candidate achieves linguistic approval but lacks source citations, its consensus evaluation outcome is permanently recorded as `lacks_source_evidence`.
   - If a candidate references restricted cultural rites or copyrighted material, its consensus evaluation outcome is recorded as `permission_blocked`.

2. **Governance is not Native Authority**:
   - Software-enforced consensus thresholds (e.g. 2 approvals) are procedural governance safeguards. They do not constitute or replace actual community authorization or native-speaker linguistic authority.
   - Evaluator eligibility rosters prevent unqualified automated or unauthorized claims of consensus.

3. **Offline Package Privacy & Context Shielding**:
   - Exported offline review packages (`Schema 2.0 JSON`) shield all restricted context sentences as `[RESTRICTED TEXT - ACCESS PRIVILEGED]`.
   - Reviewer attributions may use community-approved pseudonyms to protect contributor privacy while maintaining an auditable decision trail.

---

## 9. Audio Corpus, Speaker Consent, and Speech Data Ethics (Step 15)

Step 15 enforces strict ethical, legal, and cultural protocols governing the Tangkhul Audio Corpus:

1. **Speaker Sovereignty & Non-Assumed Consent**:
   - Audio recordings are never treated as automatically cleared for reuse simply because they exist in public spaces or online repositories.
   - Web scraping, automated downloads, or unsolicited harvesting of spoken recordings from community platforms is strictly prohibited.
   - Every audio entry requires an affirmative consent determination (`pending`, `authorized`, `restricted`, `withdrawn`, or `needs_review`).

2. **Speaker Privacy & Non-Identifying Pseudonyms**:
   - Speaker identities must be recorded using non-identifying contributor pseudonyms (e.g. `Speaker_Hunphun_01`, `Elder_Rph_02`).
   - Personal contact details, full legal names, and private speaker identifiers are strictly excluded from public records, CLI listings, logs, and export manifests.

3. **Consent Withdrawal & Permanent Revocation**:
   - Tangkhul speakers and community custodians retain the perpetual right to revoke or withdraw consent for any recording.
   - Executing `tangkhul audio permissions <ID> --withdraw --reason ...` updates the recording to `is_withdrawn=True`, sets consent to `withdrawn`, appends an immutable audit event to `audio_consent_records`, and immediately excludes the recording from all future exports and audio access routines.

4. **Cultural & Sacred Protections**:
   - Material marked `restricted` (such as sacred ritual chants, customary clan rites, or taboo lore) is shielded by default.
   - Public inspection and search commands automatically mask binary file paths and sensitive transcriptions as `[RESTRICTED AUDIO FILE - ACCESS PRIVILEGED]` and `[RESTRICTED TEXT - SACRED/TABOO CONTENT]`.

5. **Metadata-Only Representation**:
   - When an audio recording cannot legally or ethically be stored or distributed (due to copyright retention, publisher restrictions, or community sensitivity), the library supports `metadata_only` mode.
   - This records dialect, phonetic transcription, speaker reference, and bibliographic provenance without retaining or exposing the restricted audio binary.




