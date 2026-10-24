# Changelog

All notable changes to the Tangkhul Language Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-24

### Added
- Initial project architecture and directory layout (`src/` layout with `tangkhul_lib`).
- Python package packaging via `pyproject.toml` (Python >= 3.10, setuptools, pytest, ruff).
- Core package scaffolding:
  - `tangkhul_lib.core`: configuration management, custom exceptions, and core domain dataclasses (`ManifestRecord`, `VocabularyEntry`, `ProvenanceRecord`).
  - `tangkhul_lib.vocabulary`: interfaces for search, normalization, deduplication, and provenance tracking.
  - Planned domain module packages (`books`, `songs`, `dictionaries`, `culture`, `history`, `literature`).
  - Storage package scaffolding (`database`, `repositories`).
  - Ingestion package with manifest schema validation (`metadata_validation.py`).
  - Command-line interface package entrypoint stub (`cli`).
- Comprehensive documentation suite under `docs/` and root `README.md`:
  - Architecture overview, data model, manifest schemas, installation, and module roadmaps.
  - Storage conventions and Git hygiene instructions in `data/README.md`.
- Utility inspection and manifest validation scripts (`scripts/validate_manifests.py`, `scripts/inspect_sources.py`).
- Automated test suite validating package imports, core models, configuration paths, and schema validation.
- GitHub Actions CI workflow for test execution and lint checking.
- Contribution guidelines (`CONTRIBUTING.md`), Code of Conduct notes, and citation specification (`CITATION.cff`).
