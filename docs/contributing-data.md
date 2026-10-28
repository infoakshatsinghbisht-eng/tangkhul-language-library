# Contributing Data

This guide explains how linguists, community members, and researchers can contribute verified Tangkhul language resources.

---

## What Can Be Contributed?

1. **Manifest Records**: Bibliographic and metadata entries for published Tangkhul books, song collections, grammar guides, dictionaries, cultural documentation, historical events, and literary works.
2. **Dictionary & Lexical Entries**: Verified Tangkhul headwords, definitions, grammatical parts of speech, and example sentences from authorized sources or native speaker contributions.
3. **Oral Transcriptions**: Verified transcripts of folklore, stories, songs, poetry, and proverbs with full recording attribution and community consent.
4. **Lexical Corrections**: Corrections of typos, dialectal notes, part-of-speech clarifications, or additional example sentences.

---

## Step-by-Step Data Contribution

### 1. Identify Target Module
Determine which module manifest the resource belongs to:
- `data/manifests/books.jsonl`
- `data/manifests/songs.jsonl`
- `data/manifests/dictionaries.jsonl`
- `data/manifests/culture.jsonl`
- `data/manifests/history.jsonl`
- `data/manifests/literature.jsonl`

### 2. Format as JSON Lines
Add a new JSON object adhering strictly to the `ManifestRecord` schema:

```json
{"id": "LIT-POEM-001", "resource_type": "literature", "title": "Ava Ram Leishat", "creator": "Luingam A. Shimray", "year": 2000, "language": "Tangkhul", "permission_status": "permitted", "verification_status": "verified"}
```

### 3. Adding Lexical Entries
When contributing new lexical entries:
- Maintain exact original surface orthography (do not omit traditional accents or macrons).
- Provide definitions in English and/or Hindi.
- Never invent missing definitions or translations.
- Include precise page, section, or informant attribution.
- Tag community elder or fieldwork contributions with `extraction_method="community_contribution"`.

### 4. Contributing Cultural Records & Proverbs
When contributing cultural practices, festivals, customs, or proverbs:
- **Village Specificity**: Specify the exact village (e.g. *Hunphun*, *Phungcham*, *Champhung*) and dialect. Avoid generalizing one village's customs across all Tangkhul communities.
- **Original Orthography**: Provide verbatim Tangkhul sayings (*Paotam*) alongside translations and contextual interpretations.
- **Consent & Privacy**: Ensure contributor consent is obtained for field recordings and interviews (`contributor_consent=True`).
- **Restricted Knowledge**: Sacred ritual formulas, incantations, or taboo observations must be marked with `permission_status="restricted"` to prevent automated indexing and public exposure.
- **Verification Tier**: Mark unconfirmed sayings or field recordings as `verification_status="needs_review"`.

### 5. Contributing Historical Records, Settlements, and Timelines
When contributing historical events, pioneering biographies, migration accounts, or settlement toponyms:
- **No Fabrication**: Never invent dates, migration paths, genealogies, or historical quotes. If a date is approximate, use `event_date="c. 1917–1918"` and set `sort_year=1917` for timeline ordering.
- **Divergent Accounts**: When oral traditions differ from colonial or valley chronicles, record both perspectives in `contradictory_accounts` without discarding either.
- **Evidence Classification**: Tag evidence honestly (`primary_source`, `archival_record`, `scholarly_interpretation`, `oral_tradition`, `candidate_fieldwork`).
- **Toponyms & Settlement Names**: Preserve original indigenous place names (*Hunphun*, *Makhel*, *Sangshak*, *Phungcham*) alongside alternate administrative or colonial designations.
- **Uncertain Claims**: Any disputed ancestral or clan claim must be tagged with `verification_status="needs_review"`.

### 6. Contributing Literary Works, Folktales, and Poetry
When contributing poems, folktales, short stories, drama, or anthologies:
- **Genre Classification**: Specify the exact genre under `work_type` and `genres` (supported: `poem`, `short_story`, `folk_tale`, `oral_narrative`, `riddle`, `proverb_collection`, `play`, `novel`, `essay`, `literary_anthology`, `ballad`, `children_literature`, `translation`).
- **Preserve Original Titles & Orthography**: Retain exact original Tangkhul titles and diacritics in `original_title` without flattening during normalization.
- **Author vs Oral Storyteller**: Distinguish written authorship (`author`, `poet`, `playwright`) from oral custodianship (`storyteller`, `collector`).
- **Relational Linking**: If an individual short story or poem is part of an existing catalogued textbook reader (e.g. *Maranwon* in *Tangkhul Tuitam Kachiko*), link using `book_id="BK-TLS-007"` rather than duplicating the parent publication entry.
- **Adaptations & Retellings**: Preserve relationships between distinct versions (e.g. ballad *Shimreishang Kala Maitonphi* `LIT-FLK-001` and stage verse-drama adaptation `LIT-PLAY-002`) in `related_works`.
- **Copyright Compliance**: In-copyright contemporary works must be marked `access_status="metadata_only"`. Full texts are accepted only with explicit written clearance or public domain evidence.

### 7. Participating in Native-Speaker Validation & Community Governance
When validating candidate vocabulary, correcting definitions, or resolving dialect disputes:
- **Independent Judgment**: Each review decision must reflect your own linguistic knowledge or direct elder consultations. Do not vote repeatedly under different accounts or copy other reviewers' notes.
- **Attributable Pseudonyms**: You may use a consistent community pseudonym (e.g. `Somrei-Elder-01`, `Ukhrul-Consultant-M`) to maintain privacy while ensuring decision accountability.
- **Two-Reviewer Consensus**: Under default policy, a candidate requires at least two independent eligible reviewer approvals before promotion to `verified`.
- **Handling Disagreements**: If you encounter an unfamiliar form or disputed meaning, choose `flag_conflict` or `correction_requested` rather than outright rejection. Tangkhul village dialects vary significantly across regions.
- **Offline Review Packages**: Review packages (`.json`) can be edited offline and imported using `tangkhul review --import-package`. Never modify the `task_id` or `entry_id` fields.
- **Respect Source Boundaries**: Linguistic correctness does not override copyright or sacred cultural restrictions. Respect `restricted` classifications.

### 8. Contributing Audio Recordings & Pronunciation Records
When contributing spoken recordings or phonetic pronunciations:
- **Explicit Documented Consent**: Recordings must be accompanied by documented consent from the speaker or authorized village authority. Never harvest or scrape recordings from the web or social media.
- **Speaker Privacy & Pseudonyms**: Use non-identifying speaker codes (e.g. `Speaker_Hunphun_01`, `Elder_Rph_02`). Never include phone numbers, personal addresses, or identifying personal data.
- **Technical Standards**: Uncompressed 16-bit PCM WAV (16 kHz or 44.1 kHz, mono) is preferred. Supported compressed formats (`mp3`, `ogg`, `flac`, `m4a`) are accepted with optional `mutagen` dependency.
- **Dialect & Village Documentation**: Specify village and dialect only when explicitly known and approved for storage (e.g. `dialect="Ukhrul"`, `village="Hunphun"`).
- **Phonetic & Orthographic Transcriptions**: Supply both standard surface orthography and IPA transcription (`/ŋaʃan/`). Do not invent IPA characters if uncertain.
- **Metadata-Only Contributions**: If copyright or clan restrictions prevent sharing the raw audio file, submit a metadata-only record via `tangkhul audio import --metadata-only` preserving provenance without distributing the binary.
- **Right of Withdrawal**: Speakers or community elders retain the permanent right to withdraw recordings at any time by contacting library maintainers.

### 9. Validate
Run the validation scripts, test suite, and linter before submitting:

```bash
python scripts/validate_manifests.py
python scripts/inspect_sources.py
pytest
ruff check .
```

### 10. Submit Pull Request
Include citations, permissions proof, or background information in your pull request description.

