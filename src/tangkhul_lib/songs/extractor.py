"""Lyrics text extraction and vocabulary candidate linking for Tangkhul songs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tangkhul_lib.core.exceptions import PermissionRestrictedError, ResourceNotFoundError
from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
from tangkhul_lib.songs.models import SongRecord
from tangkhul_lib.vocabulary.normalization import normalize_unicode, sanitize_spacing


class SongLyricsExtractor:
    """Manages lyrics parsing, permission enforcement, and candidate vocabulary harvesting."""

    def is_extraction_permitted(self, song: SongRecord) -> bool:
        """Check whether lyrics extraction is permitted by license and rights status."""
        if song.permission_status == "restricted" or song.access_status == "restricted":
            return False

        allowed_permissions = {"permitted", "public_domain", "community_authorized"}
        allowed_access = {"full_text_available", "open_access"}

        return (
            song.permission_status in allowed_permissions
            or song.access_status in allowed_access
        )

    def parse_lyrics_text(self, text: str) -> list[tuple[int, int, str]]:
        """Parse structured stanzas and lines from lyrics text.

        Returns:
            List of (stanza_number, line_number_within_stanza, line_text).
        """
        normalized = normalize_unicode(text)
        stanzas = [s.strip() for s in re.split(r"\n\s*\n", normalized) if s.strip()]

        parsed_lines: list[tuple[int, int, str]] = []
        for stanza_idx, stanza in enumerate(stanzas, start=1):
            lines = [
                sanitize_spacing(raw_line)
                for raw_line in stanza.split("\n")
                if sanitize_spacing(raw_line)
            ]
            for line_idx, line in enumerate(lines, start=1):
                parsed_lines.append((stanza_idx, line_idx, line))

        return parsed_lines

    def extract_lyrics_file(
        self,
        song: SongRecord,
        file_path: Path | None = None,
        enforce_permissions: bool = True,
    ) -> list[tuple[int, int, str]]:
        """Extract stanzas and lines from a local lyrics file while checking permissions.

        Raises:
            PermissionRestrictedError: If song permissions forbid lyrics extraction.
            ResourceNotFoundError: If file cannot be found.
        """
        if enforce_permissions and not self.is_extraction_permitted(song):
            raise PermissionRestrictedError(
                f"Lyrics processing is not permitted for song '{song.id}' ({song.title}). "
                f"Permission status: '{song.permission_status}', access: '{song.access_status}'."
            )

        target = Path(file_path) if file_path else (
            Path(song.local_file_path) if song.local_file_path else None
        )
        if not target or not target.is_file():
            raise ResourceNotFoundError(
                f"No accessible lyrics file for song '{song.id}'. Path: {target}"
            )

        try:
            content = target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = target.read_text(encoding="latin-1")

        return self.parse_lyrics_text(content)

    def extract_vocabulary_candidates(
        self,
        song: SongRecord,
        parsed_lines: list[tuple[int, int, str]],
    ) -> tuple[list[dict[str, Any]], list[VocabularyEntry]]:
        """Extract raw tokens and unverified candidate vocabulary from lyrics lines.

        Preserves:
            - Original poetic Tangkhul word forms and orthography.
            - Stanza and line context.
            - Attribution to singer, lyricist, village, and year.
            - Provenance citation with line references.
            - Empty meanings and translations (never fabricated).
            - Unverified verification status.

        Returns:
            Tuple of (raw_tokens_list, candidate_vocabulary_list).
        """
        raw_tokens: list[dict[str, Any]] = []
        vocab_map: dict[str, VocabularyEntry] = {}

        word_regex = re.compile(
            r"\b[A-Za-zÀ-ÿĀ-žḀ-ỿ]+(?:['’-][A-Za-zÀ-ÿĀ-žḀ-ỿ]+)*\b",
            re.UNICODE,
        )

        for stanza_num, line_num, line_text in parsed_lines:
            line_ref = f"Stanza {stanza_num}, Line {line_num}"
            performer_info = f" ({song.singer})" if song.singer else ""
            citation_str = f"{song.title}{performer_info} [{line_ref}]"

            words = word_regex.findall(line_text)
            for word in words:
                word_form = normalize_unicode(word)
                token_entry = {
                    "source_id": song.id,
                    "word_form": word_form,
                    "page_or_section": line_ref,
                    "context_sentence": line_text,
                    "extraction_method": "lyrics_extraction",
                    "verification_status": "unverified",
                }
                raw_tokens.append(token_entry)

                word_key = word_form.lower()
                prov_record = ProvenanceRecord(
                    source_id=song.id,
                    resource_type="songs",
                    citation=citation_str,
                    page_or_section=line_ref,
                    context_sentence=line_text,
                    recorded_year=song.year,
                    permission_status=song.permission_status,
                )

                if word_key not in vocab_map:
                    entry_id = f"VOC-SNG-{song.id}-{len(vocab_map) + 1:04d}"
                    vocab_map[word_key] = VocabularyEntry(
                        id=entry_id,
                        headword=word_form,
                        meanings=[],
                        translations_en=[],
                        alternative_spellings=[],
                        dialect_variants=[],
                        dialect=song.dialect,
                        example_sentences=[line_text],
                        provenance=[prov_record],
                        verification_status="unverified",
                    )
                else:
                    existing = vocab_map[word_key]
                    if (
                        word_form != existing.headword
                        and word_form not in existing.alternative_spellings
                    ):
                        existing.alternative_spellings.append(word_form)

                    if (
                        line_text not in existing.example_sentences
                        and len(existing.example_sentences) < 5
                    ):
                        existing.example_sentences.append(line_text)

                    has_same_prov = any(
                        p.source_id == prov_record.source_id
                        and p.page_or_section == prov_record.page_or_section
                        and p.context_sentence == prov_record.context_sentence
                        for p in existing.provenance
                    )
                    if not has_same_prov:
                        existing.provenance.append(prov_record)

        return raw_tokens, list(vocab_map.values())
