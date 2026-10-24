# Contributing to Tangkhul Language Library

Thank you for your interest in contributing to the **Tangkhul Language Library**! This project is dedicated to the ethical preservation, documentation, and linguistic research of the Tangkhul language and cultural heritage.

## Core Principles

1. **Cultural Respect and Sensitivity**: Tangkhul linguistic traditions, folk songs, sacred customs, and historical narratives belong to the Tangkhul community. Contributions must respect community norms, local elders, and cultural custodians.
2. **Provenance and Verification**: Every vocabulary item, text extraction, or cultural record must have explicit provenance (source citation, author/performer, year, page number or recording reference). Fabricated or unverified entries are not permitted.
3. **Copyright & Permission**: Only contribute materials where you have verified explicit permission or public domain status. Publicly accessible URLs do not automatically imply permission to redistribute.
4. **Dialectal Inclusivity**: Tangkhul has rich dialectal diversity across villages and regions (e.g., Ukhrul standard, northern, southern, and eastern dialects). Variations should be recorded with dialect provenance rather than overwritten or forcibly harmonized.

---

## Development Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-org/tangkhul-language-library.git
cd tangkhul-language-library

# Create a virtual environment
python -m venv .venv

# Activate on Windows PowerShell:
.venv\Scripts\Activate.ps1

# Activate on Linux / macOS:
source .venv/bin/activate

# Install in editable mode with development dependencies
python -m pip install -e ".[dev]"
```

### 3. Running Checks

Always run tests and linting before submitting a pull request:

```bash
# Run test suite
python -m pytest

# Run linter
python -m ruff check .

# Validate manifests
python scripts/validate_manifests.py
```

---

## Contributing Data

When contributing metadata manifests or permitted source materials:
1. Manifests belong in `data/manifests/<module>.jsonl`.
2. Do not commit large binary files (PDFs, audio files, scans) directly into Git. Use cloud archival storage or permitted local paths.
3. Validate each manifest line using `scripts/validate_manifests.py`.
4. Ensure mandatory fields (`id`, `resource_type`, `title`, `language`, `permission_status`, `verification_status`) are present and accurate.

---

## Submitting Pull Requests

1. Create a feature branch: `git checkout -b feature/your-feature-name`.
2. Keep commits atomic, informative, and focused on a single change.
3. Ensure all tests and lint checks pass cleanly.
4. Submit a Pull Request detailing the changes, linguistic or technical rationale, and any references consulted.
