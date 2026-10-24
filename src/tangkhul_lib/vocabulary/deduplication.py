"""Provenance-preserving vocabulary deduplication.

Crucial Rule:
    Deduplication must NEVER discard different meanings, dialect variants,
    or source provenance. Similar spellings must not be assumed to represent
    the same word without verified homophone/polysemy resolution.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry


def merge_provenance(
    existing: VocabularyEntry,
    new_provenance: list[ProvenanceRecord],
) -> None:
    """Safely append new provenance records to an existing entry without data loss."""
    seen = {
        (p.source_id, p.page_or_section, p.context_sentence)
        for p in existing.provenance
    }
    for prov in new_provenance:
        key = (prov.source_id, prov.page_or_section, prov.context_sentence)
        if key not in seen:
            existing.provenance.append(prov)
            seen.add(key)


def deduplicate_entries(entries: list[VocabularyEntry]) -> list[VocabularyEntry]:
    """Merge entries sharing identical headword, dialect, and senses.

    Distinct meanings, distinct dialect designations, and all provenance records
    are strictly preserved. Entries with differing meanings or dialects are
    retained as separate entries.
    """
    merged: dict[tuple[str, str | None, tuple[str, ...]], VocabularyEntry] = {}

    for entry in entries:
        # Group by headword, dialect, and tuple of sorted unique meanings
        sense_key = (
            entry.headword.strip().lower(),
            entry.dialect,
            tuple(sorted(set(entry.meanings))),
        )

        if sense_key not in merged:
            merged[sense_key] = entry
        else:
            target = merged[sense_key]
            # Accumulate alternative spellings
            for alt in entry.alternative_spellings:
                if alt not in target.alternative_spellings:
                    target.alternative_spellings.append(alt)
            # Accumulate example sentences
            for ex in entry.example_sentences:
                if ex not in target.example_sentences:
                    target.example_sentences.append(ex)
            # Merge provenance without loss
            merge_provenance(target, entry.provenance)

    return list(merged.values())
