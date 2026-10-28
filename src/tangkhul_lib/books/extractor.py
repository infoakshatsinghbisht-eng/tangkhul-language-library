"""Book text extraction and vocabulary candidate linking for Tangkhul Language Library."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.exceptions import PermissionRestrictedError, ResourceNotFoundError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.ingestion.text_extraction import ExtractionResult, TextExtractor
from tangkhul_lib.vocabulary.normalization import normalize_unicode, sanitize_spacing


class BookTextExtractor:
    """Manages permitted document text extraction and candidate vocabulary generation."""

    def __init__(self, extractor: TextExtractor | None = None) -> None:
        self.extractor = extractor or TextExtractor()

    def is_extraction_permitted(self, book: BookRecord) -> bool:
        """Check whether full-text processing is permitted by license and copyright."""
        if book.permission_status == "restricted" or book.access_status == "restricted":
            return False

        # Permitted if explicitly authorized, public domain, or open access
        allowed_permissions = {"permitted", "public_domain", "community_authorized"}
        allowed_access = {"full_text_available", "open_access"}

        return (
            book.permission_status in allowed_permissions
            or book.access_status in allowed_access
        )

    def extract_book_text(
        self,
        book: BookRecord,
        file_path: Path | None = None,
        enforce_permissions: bool = True,
    ) -> ExtractionResult:
        """Extract text from a book file while respecting copyright permissions.

        Raises:
            PermissionRestrictedError: If permissions forbid text extraction.
            ResourceNotFoundError: If file cannot be found.
        """
        if enforce_permissions and not self.is_extraction_permitted(book):
            raise PermissionRestrictedError(
                f"Full text extraction is not permitted for '{book.id}' "
                f"({book.title}). Permission status is '{book.permission_status}', "
                f"access status is '{book.access_status}'."
            )

        resolved_path = (
            Path(file_path)
            if file_path
            else (Path(book.local_file_path) if book.local_file_path else None)
        )
        if not resolved_path or not resolved_path.is_file():
            raise ResourceNotFoundError(
                f"No accessible local file for book '{book.id}'. "
                f"Path: {resolved_path}"
            )

        return self.extractor.extract_from_file(resolved_path, source_id=book.id)

    def extract_vocabulary_candidates(
        self,
        book: BookRecord,
        extraction: ExtractionResult,
    ) -> tuple[list[dict[str, Any]], list[VocabularyEntry]]:
        """Extract raw tokens and unverified candidate vocabulary entries from extracted pages.

        Preserves:
            - Original Tangkhul word forms (no forced orthographic alterations).
            - Sentence contexts.
            - Source book ID and citation with page numbers.
            - Unverified verification status (distinguishable from confirmed dictionary entries).
            - Empty meanings/translations (never invented).

        Returns:
            Tuple of (raw_tokens_list, vocabulary_entries_list).
        """
        raw_tokens: list[dict[str, Any]] = []
        vocab_map: dict[str, VocabularyEntry] = {}

        # Sentence splitter: handles periods, exclamation marks, question marks, and newlines
        sentence_regex = re.compile(r"([^\.\?!]+[\.\?!]?)", re.UNICODE)
        # Word tokenizer: keeps Latin letters, diacritics, and internal glottal hyphens/apostrophes
        word_regex = re.compile(r"\b[A-Za-zÀ-ÿĀ-žḀ-ỿ]+(?:['’-][A-Za-zÀ-ÿĀ-žḀ-ỿ]+)*\b", re.UNICODE)

        for page in extraction.pages:
            page_text = page.text.strip()
            if not page_text:
                continue

            page_ref = f"p. {page.page_number}" if page.page_number is not None else None
            citation_str = (
                f"{book.title} ({page_ref})" if page_ref else book.title
            )

            # Split text into sentences
            paragraphs = page_text.split("\n")
            for para in paragraphs:
                cleaned_para = sanitize_spacing(para)
                if not cleaned_para:
                    continue

                raw_sentences = sentence_regex.findall(cleaned_para)
                for sentence_str in raw_sentences:
                    sentence_clean = sanitize_spacing(sentence_str)
                    if not sentence_clean:
                        continue

                    words = word_regex.findall(sentence_clean)
                    for word in words:
                        word_form = normalize_unicode(word)
                        # Record raw token
                        token_entry = {
                            "source_id": book.id,
                            "word_form": word_form,
                            "page_or_section": page_ref,
                            "context_sentence": sentence_clean,
                            "extraction_method": extraction.extraction_method,
                            "verification_status": "unverified",
                        }
                        raw_tokens.append(token_entry)

                        # Accumulate in candidate vocabulary entries
                        word_key = word_form.lower()
                        prov_record = ProvenanceRecord(
                            source_id=book.id,
                            resource_type="books",
                            citation=citation_str,
                            page_or_section=page_ref,
                            context_sentence=sentence_clean,
                            recorded_year=book.publication_year,
                            permission_status=book.permission_status,
                        )

                        if word_key not in vocab_map:
                            entry_id = f"VOC-BK-{book.id}-{len(vocab_map) + 1:04d}"
                            vocab_map[word_key] = VocabularyEntry(
                                id=entry_id,
                                headword=word_form,
                                meanings=[],  # Senses are never fabricated
                                translations_en=[],  # Translations are never fabricated
                                alternative_spellings=[],
                                dialect_variants=[],
                                dialect=book.dialect,
                                example_sentences=[sentence_clean],
                                provenance=[prov_record],
                                verification_status="unverified",
                            )
                        else:
                            existing_entry = vocab_map[word_key]
                            # Preserve casing variation as alternative spelling if different
                            if (
                                word_form != existing_entry.headword
                                and word_form not in existing_entry.alternative_spellings
                            ):
                                existing_entry.alternative_spellings.append(word_form)

                            if (
                                sentence_clean not in existing_entry.example_sentences
                                and len(existing_entry.example_sentences) < 5
                            ):
                                existing_entry.example_sentences.append(sentence_clean)

                            # Append provenance safely
                            has_same_prov = any(
                                p.source_id == prov_record.source_id
                                and p.page_or_section == prov_record.page_or_section
                                and p.context_sentence == prov_record.context_sentence
                                for p in existing_entry.provenance
                            )
                            if not has_same_prov:
                                existing_entry.provenance.append(prov_record)

        return raw_tokens, list(vocab_map.values())
