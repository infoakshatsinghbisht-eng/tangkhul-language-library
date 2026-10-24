# Contributing Data

This guide explains how linguists, community members, and researchers can contribute verified Tangkhul language resources.

---

## What Can Be Contributed?

1. **Manifest Records**: Bibliographic and metadata entries for published Tangkhul books, song collections, grammar guides, or dictionaries.
2. **Oral Transcriptions**: Verified transcripts of folklore, stories, songs, and proverbs with full recording attribution and community consent.
3. **Lexical Corrections**: Corrections of typos, dialectal notes, part-of-speech clarifications, or additional example sentences.

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
{"id": "BK-0001", "resource_type": "books", "title": "Tangkhul Primer", "creator": "Pettigrew, W.", "year": 1918, "language": "Tangkhul", "permission_status": "public_domain", "verification_status": "verified"}
```

### 3. Validate
Run the validation script before submitting:

```bash
python scripts/validate_manifests.py
```

### 4. Submit Pull Request
Include citations, permissions proof, or background information in your pull request description.
