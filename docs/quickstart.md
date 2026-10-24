# Quickstart Guide

This guide demonstrates how to interact with the currently operational foundation of the **Tangkhul Language Library**.

> **Note on Project Status**:
> As of Step 1, this package provides the core architecture, data models, configuration manager, and manifest validation engine. Domain parsing pipelines (Books, Songs, etc.) and search operations are planned for subsequent steps and are not yet operational.

---

## 1. Inspecting Library Version and Environment

```python
import tangkhul_lib
from tangkhul_lib.core.config import LibraryConfig

print(f"Tangkhul Library Version: {tangkhul_lib.__version__}")

# Inspect detected paths
config = LibraryConfig.from_environment()
print(f"Project root: {config.paths.root_dir}")
print(f"Manifests directory: {config.paths.manifests_dir}")
```

---

## 2. Using Core Data Models

You can instantiate and validate `ManifestRecord` and `VocabularyEntry` data structures:

```python
from tangkhul_lib.core.models import ManifestRecord, ProvenanceRecord, VocabularyEntry

# Create a bibliographic manifest entry
record = ManifestRecord(
    id="BK-0001",
    resource_type="books",
    title="Tangkhul Folk Literature and Grammar",
    creator="Community Custodian",
    year=1975,
    language="Tangkhul",
    permission_status="community_authorized",
    verification_status="verified",
)

print(record.to_dict())

# Create a vocabulary entry with provenance
provenance = ProvenanceRecord(
    source_id="BK-0001",
    resource_type="books",
    citation="Tangkhul Folk Literature and Grammar, 1975, p. 12",
    page_or_section="p. 12",
    context_sentence="I ramli kaphung kazing kachon ngalung.",
)

entry = VocabularyEntry(
    id="VOCAB-0001",
    headword="kaphung",
    meanings=["mountain", "hill"],
    part_of_speech="noun",
    provenance=[provenance],
    verification_status="verified",
)

print(f"Headword: {entry.headword}")
print(f"Meanings: {entry.meanings}")
print(f"Sources cited: {len(entry.provenance)}")
```

---

## 3. Validating Manifests

Run validation on existing JSONL manifests using the built-in validator or command line:

```python
from pathlib import Path
from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file

manifest_path = Path("data/manifests/books.jsonl")
records = validate_manifest_file(manifest_path)
print(f"Validated {len(records)} books in manifest.")
```

Or from the command line:

```bash
python scripts/validate_manifests.py
```
