"""Text extraction interfaces for permitted documents and archives.

Planned Capabilities:
    - Text extraction from permitted OCR/PDF scans, text archives, and audio transcripts.
    - Preserving page numbers, chapter headings, and paragraph boundaries.
    - Cleaning extraneous scanner artifacts while preserving authentic Tangkhul characters.
"""

from __future__ import annotations

from pathlib import Path


class TextExtractor:
    """Interface for extracting text content from permitted source documents."""

    def extract_from_file(self, file_path: Path) -> str:
        """Extract plain text from document while preserving structural citations.

        Note:
            Planned interface. Extraction pipelines will be integrated in subsequent
            steps once permitted source files are catalogued.
        """
        raise NotImplementedError(
            "Text extraction is a planned feature and is not yet operational in Step 1."
        )
