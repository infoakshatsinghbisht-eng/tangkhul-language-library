"""Authorized vocabulary expansion, source-backed lexicon enrichment, and dialect collection.

This module coordinates permission verification, structured dictionary and running-text
lexicon extraction, conservative duplicate matching, dialect variation tracking, and
review candidate generation for the Tangkhul Language Library.
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from tangkhul_lib.core.exceptions import PermissionDeniedError, ResourceNotFoundError
from tangkhul_lib.core.models import (
    ManifestRecord,
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.dictionaries.extractor import DictionaryExtractor
from tangkhul_lib.dictionaries.models import DictionaryEntryRecord, DictionarySourceRecord
from tangkhul_lib.ingestion.pipeline import SourcePermissionChecker
from tangkhul_lib.ingestion.text_extraction import TextExtractor, compute_file_hash
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    DictionaryRepository,
    EnrichmentRepository,
    EnrichmentRunRecord,
    ManifestRepository,
    VocabularyRepository,
)
from tangkhul_lib.vocabulary.normalization import normalize_tangkhul_text, normalize_unicode
from tangkhul_lib.vocabulary.phonetic import TangkhulPhoneticEncoder, calculate_similarity

if TYPE_CHECKING:
    from tangkhul_lib.core.config import LibraryConfig


LEXICAL_CATEGORIES = (
    "nouns",
    "verbs",
    "adjectives",
    "adverbs",
    "pronouns",
    "particles",
    "greetings_conversational",
    "numbers_time",
    "family_kinship",
    "body",
    "food_agriculture",
    "environment_nature",
    "animals_plants",
    "tools_craft",
    "idioms_cultural",
    "dialect_variants",
)


def classify_lexical_categories(
    headword: str,
    meanings: list[str],
    part_of_speech: str | None = None,
    dialect: str | None = None,
    notes: str | None = None,
) -> list[str]:
    """Classify an entry into semantic and grammatical categories based on source evidence.

    Categories are assigned ONLY when supported by explicit source information,
    such as parts of speech, glosses, headword morphology, or dialect tags.
    """
    categories: set[str] = set()
    pos_clean = (part_of_speech or "").strip().lower()
    combined_gloss = " ".join(meanings).lower() + " " + (notes or "").lower()

    # 1. Grammatical categories
    if pos_clean in {"n", "noun", "proper noun"}:
        categories.add("nouns")
    elif pos_clean in {"v", "verb", "transitive verb", "intransitive verb"}:
        categories.add("verbs")
    elif pos_clean in {"adj", "adjective"}:
        categories.add("adjectives")
    elif pos_clean in {"adv", "adverb"}:
        categories.add("adverbs")
    elif pos_clean in {"pron", "pronoun"}:
        categories.add("pronouns")
    elif pos_clean in {"part", "particle", "postposition", "conj", "conjunction"}:
        categories.add("particles")

    # 2. Semantic domains based on source glosses
    # Greetings, questions, conversational expressions
    if any(
        kw in combined_gloss
        for kw in (
            "greeting",
            "hello",
            "welcome",
            "farewell",
            "question",
            "command",
            "interjection",
            "exclamation",
            "listen",
        )
    ) or headword.lower() in {"khamatha", "ning shong", "khulu"}:
        categories.add("greetings_conversational")

    # Numbers and time
    if any(
        kw in combined_gloss
        for kw in (
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "numeral",
            "number",
            "count",
            "year",
            "month",
            "day",
            "time",
            "season",
            "morning",
            "night",
            "yesterday",
            "tomorrow",
            "epoch",
            "generation",
        )
    ):
        categories.add("numbers_time")

    # Family and kinship
    if any(
        kw in combined_gloss
        for kw in (
            "father",
            "mother",
            "sister",
            "brother",
            "child",
            "son",
            "daughter",
            "clan",
            "family",
            "ancestor",
            "lineage",
            "kin",
            "husband",
            "wife",
            "parent",
        )
    ):
        categories.add("family_kinship")

    # Body
    if any(
        kw in combined_gloss
        for kw in (
            "eye",
            "head",
            "hand",
            "foot",
            "leg",
            "ear",
            "nose",
            "mouth",
            "hair",
            "body",
            "heart",
            "tooth",
            "blood",
            "bone",
            "arm",
            "finger",
        )
    ):
        categories.add("body")

    # Food and agriculture
    if any(
        kw in combined_gloss
        for kw in (
            "paddy",
            "rice",
            "grain",
            "granary",
            "field",
            "terrace",
            "harvest",
            "seed",
            "sow",
            "cultivate",
            "agriculture",
            "crop",
            "feast",
            "food",
            "cook",
            "eat",
            "drink",
            "meat",
            "festival",
        )
    ):
        categories.add("food_agriculture")

    # Environment and nature
    if any(
        kw in combined_gloss
        for kw in (
            "mountain",
            "peak",
            "hill",
            "river",
            "stream",
            "water",
            "forest",
            "earth",
            "sky",
            "stone",
            "rock",
            "wind",
            "rain",
            "sun",
            "moon",
            "star",
        )
    ):
        categories.add("environment_nature")

    # Animals and plants
    if any(
        kw in combined_gloss
        for kw in (
            "animal",
            "beast",
            "dog",
            "tiger",
            "bird",
            "fish",
            "tree",
            "flower",
            "bamboo",
            "plant",
            "flora",
            "fauna",
            "wild",
        )
    ):
        categories.add("animals_plants")

    # Tools, textiles, and traditional craft
    if any(
        kw in combined_gloss
        for kw in (
            "basket",
            "cloth",
            "shawl",
            "loom",
            "weave",
            "anvil",
            "spear",
            "tool",
            "pottery",
            "iron",
            "knife",
            "axe",
            "craft",
        )
    ):
        categories.add("tools_craft")

    # Idioms, proverbs, and fixed expressions
    if (
        "proverb" in combined_gloss
        or "saying" in combined_gloss
        or "idiom" in combined_gloss
        or len(headword.split()) > 1
    ):
        categories.add("idioms_cultural")

    # Dialect variants
    if dialect and dialect.strip().lower() not in {"standard", "standard tangkhul"}:
        categories.add("dialect_variants")

    return sorted(categories)


@dataclass
class EnrichmentItem:
    """Represents a candidate lexical item extracted from an authorized source."""

    headword: str
    meanings: list[str] = field(default_factory=list)
    translations_en: list[str] = field(default_factory=list)
    definitions_hi: list[str] = field(default_factory=list)
    part_of_speech: str | None = None
    dialect: str | None = None
    alternative_spellings: list[str] = field(default_factory=list)
    example_sentences: list[str] = field(default_factory=list)
    page_or_section: str | None = None
    entry_number: str | None = None
    extraction_method: str = "structured"
    source_excerpt: str | None = None
    confidence: float = 1.0
    notes: str | None = None


@dataclass
class EnrichmentSummary:
    """Detailed summary report of a vocabulary enrichment run."""

    source_id: str
    source_title: str
    permission_status: str
    file_path: str
    file_hash: str
    extraction_method: str
    status: str  # "completed", "dry_run", "skipped", "failed"
    items_extracted: int = 0
    candidates_created: int = 0
    entries_updated: int = 0
    duplicate_suggestions: list[dict[str, Any]] = field(default_factory=list)
    category_breakdown: dict[str, int] = field(default_factory=dict)
    data_gaps: list[str] = field(default_factory=list)
    dialect_breakdown: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    error_message: str | None = None
    already_processed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert summary to dictionary representation."""
        return asdict(self)


class VocabularyEnrichmentPipeline:
    """Coordinates authorized vocabulary expansion, candidate extraction,
    conservative deduplication, and review integration.
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        config: LibraryConfig | None = None,
        extractor: TextExtractor | None = None,
        dict_extractor: DictionaryExtractor | None = None,
        vocab_repo: VocabularyRepository | None = None,
        manifest_repo: ManifestRepository | None = None,
        dict_repo: DictionaryRepository | None = None,
        enrich_repo: EnrichmentRepository | None = None,
    ) -> None:
        self.db_manager = db_manager
        self.extractor = extractor or TextExtractor()
        self.dict_extractor = dict_extractor or DictionaryExtractor()
        self.vocab_repo = vocab_repo or VocabularyRepository(db_manager)
        self.manifest_repo = manifest_repo or ManifestRepository(db_manager)
        self.dict_repo = dict_repo or DictionaryRepository(db_manager)
        self.enrich_repo = enrich_repo or EnrichmentRepository(db_manager)
        self.phonetic_encoder = TangkhulPhoneticEncoder()

        if config is None:
            from tangkhul_lib.core.config import LibraryConfig

            self.config = LibraryConfig.from_environment()
        else:
            self.config = config

    def evaluate_source(self, source_id: str) -> dict[str, Any]:
        """Check licensing and permissions before allowing vocabulary extraction."""
        manifest = self.get_manifest_record(source_id)
        if not manifest:
            raise ResourceNotFoundError(
                f"Source manifest record '{source_id}' not found in any catalogue."
            )

        perm_eval = SourcePermissionChecker.evaluate(manifest)
        return {
            "source_id": source_id,
            "title": manifest.title,
            "creator": manifest.creator,
            "year": manifest.year,
            "resource_type": manifest.resource_type,
            "dialect": manifest.dialect,
            "permission_status": perm_eval.permission_status,
            "verification_status": perm_eval.verification_status,
            "access_status": perm_eval.access_status,
            "is_eligible": perm_eval.is_eligible,
            "skip_reason": perm_eval.skip_reason,
            "local_path": manifest.local_path,
        }

    def list_eligible_sources(
        self,
        source_type: str | None = None,
        dialect: str | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """List eligible and ineligible vocabulary enrichment sources across manifests."""
        manifests_dir = self.config.paths.manifests_dir
        manifest_files = [
            "dictionaries.jsonl",
            "books.jsonl",
            "literature.jsonl",
            "culture.jsonl",
            "history.jsonl",
            "songs.jsonl",
        ]

        eligible: list[dict[str, Any]] = []
        ineligible: list[dict[str, Any]] = []

        from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file

        for m_name in manifest_files:
            m_path = manifests_dir / m_name
            if not m_path.is_file():
                continue

            try:
                records = validate_manifest_file(m_path)
            except Exception:
                continue

            for rec in records:
                if source_type and rec.resource_type.lower() != source_type.lower():
                    continue
                if dialect and rec.dialect and dialect.lower() not in rec.dialect.lower():
                    continue

                eval_res = SourcePermissionChecker.evaluate(rec)
                info = {
                    "source_id": rec.id,
                    "title": rec.title,
                    "creator": rec.creator,
                    "year": rec.year,
                    "resource_type": rec.resource_type,
                    "dialect": rec.dialect,
                    "permission_status": eval_res.permission_status,
                    "verification_status": eval_res.verification_status,
                    "is_eligible": eval_res.is_eligible,
                    "skip_reason": eval_res.skip_reason,
                }
                if eval_res.is_eligible:
                    eligible.append(info)
                else:
                    ineligible.append(info)

        return eligible, ineligible

    def get_manifest_record(self, source_id: str) -> ManifestRecord | None:
        """Resolve manifest record from database or JSONL manifests."""
        record = self.manifest_repo.get_by_id(source_id)
        if record:
            return record

        from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file

        manifests_dir = self.config.paths.manifests_dir
        for m_path in manifests_dir.glob("*.jsonl"):
            try:
                records = validate_manifest_file(m_path)
                for r in records:
                    if r.id == source_id:
                        self.manifest_repo.add(r)
                        return r
            except Exception:
                continue
        return None

    def preview_source(
        self,
        source_id: str,
        file_path: Path | str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Inspect a source and preview extracted candidates without modifying the database."""
        manifest = self.get_manifest_record(source_id)
        if not manifest:
            raise ResourceNotFoundError(
                f"Source manifest record '{source_id}' not found in any catalogue."
            )

        perm_info = self.evaluate_source(source_id)
        if not perm_info["is_eligible"]:
            raise PermissionDeniedError(
                f"Text/entry extraction is not permitted for '{source_id}'. "
                f"Permission status: '{perm_info['permission_status']}'. "
                f"Reason: {perm_info['skip_reason']}",
                record_id=source_id,
                permission_status=perm_info["permission_status"],
            )

        resolved_path = self._resolve_file_path(manifest, file_path)
        items, extraction_method, warnings = self._extract_items_from_file(
            manifest=manifest,
            file_path=resolved_path,
        )

        samples = []
        for item in items[:limit]:
            categories = classify_lexical_categories(
                headword=item.headword,
                meanings=item.meanings,
                part_of_speech=item.part_of_speech,
                dialect=item.dialect or manifest.dialect,
                notes=item.notes,
            )
            samples.append({
                "headword": item.headword,
                "meanings": item.meanings,
                "part_of_speech": item.part_of_speech or "unrecorded",
                "dialect": item.dialect or manifest.dialect or "Ukhrul",
                "page_or_section": item.page_or_section,
                "example": item.example_sentences[0] if item.example_sentences else None,
                "categories": categories,
            })

        return {
            "source_id": source_id,
            "title": manifest.title,
            "file_name": resolved_path.name,
            "file_format": resolved_path.suffix.lower().lstrip("."),
            "extraction_method": extraction_method,
            "total_items_found": len(items),
            "preview_limit": limit,
            "sample_items": samples,
            "warnings": warnings,
        }

    def enrich_from_source(
        self,
        source_id: str,
        file_path: Path | str | None = None,
        dialect: str | None = None,
        force: bool = False,
        dry_run: bool = False,
    ) -> EnrichmentSummary:
        """Enrich vocabulary from an authorized source file into the unified database."""
        manifest = self.get_manifest_record(source_id)
        if not manifest:
            raise ResourceNotFoundError(
                f"Source manifest record '{source_id}' not found in any catalogue."
            )

        # 1. Permission check
        perm_info = self.evaluate_source(source_id)
        if not perm_info["is_eligible"] and not force:
            return EnrichmentSummary(
                source_id=source_id,
                source_title=manifest.title,
                permission_status=perm_info["permission_status"],
                file_path=str(file_path or manifest.local_path or ""),
                file_hash="",
                extraction_method="none",
                status="skipped",
                error_message=perm_info["skip_reason"],
            )

        # 2. Local file resolution
        resolved_path = self._resolve_file_path(manifest, file_path)
        file_hash = compute_file_hash(resolved_path)

        # 3. Idempotency check
        last_run = self.enrich_repo.get_last_run_for_source(source_id)
        if (
            last_run
            and last_run.file_hash == file_hash
            and last_run.status == "completed"
            and not force
            and not dry_run
        ):
            return EnrichmentSummary(
                source_id=source_id,
                source_title=manifest.title,
                permission_status=manifest.permission_status,
                file_path=str(resolved_path),
                file_hash=file_hash,
                extraction_method=last_run.extraction_method,
                status="completed",
                items_extracted=last_run.items_extracted,
                candidates_created=last_run.candidates_created,
                entries_updated=last_run.entries_updated,
                already_processed=True,
                warnings=[
                    "Source file unchanged; already enriched. Pass --force to reprocess."
                ],
            )

        # 4. Extract lexical items
        try:
            items, extraction_method, warnings = self._extract_items_from_file(
                manifest=manifest,
                file_path=resolved_path,
                dialect_override=dialect,
            )
        except Exception as e:
            return EnrichmentSummary(
                source_id=source_id,
                source_title=manifest.title,
                permission_status=manifest.permission_status,
                file_path=str(resolved_path),
                file_hash=file_hash,
                extraction_method="failed",
                status="failed",
                error_message=f"Extraction failure: {e}",
            )

        # 5. Process candidate items, matching against unified database
        category_counts: dict[str, int] = {cat: 0 for cat in LEXICAL_CATEGORIES}
        dialect_counts: dict[str, int] = {}
        duplicate_suggestions: list[dict[str, Any]] = []

        existing_entries = self.vocab_repo.list_all()
        existing_lookup: dict[str, VocabularyEntry] = {
            e.headword.strip().lower(): e for e in existing_entries
        }

        candidates_to_add: list[VocabularyEntry] = []
        entries_to_update: list[VocabularyEntry] = []
        dict_entries_to_add: list[DictionaryEntryRecord] = []

        for idx, item in enumerate(items, start=1):
            hw_clean = normalize_tangkhul_text(item.headword).strip()
            if not hw_clean or len(hw_clean) < 2:
                continue

            entry_dialect = item.dialect or dialect or manifest.dialect or "Ukhrul"
            dialect_counts[entry_dialect] = dialect_counts.get(entry_dialect, 0) + 1

            cats = classify_lexical_categories(
                headword=hw_clean,
                meanings=item.meanings,
                part_of_speech=item.part_of_speech,
                dialect=entry_dialect,
                notes=item.notes,
            )
            for cat in cats:
                category_counts[cat] = category_counts.get(cat, 0) + 1

            hw_key = hw_clean.lower()
            citation_str = (
                f"{manifest.title} ({item.page_or_section})"
                if item.page_or_section
                else manifest.title
            )

            context_sent = (
                item.example_sentences[0]
                if item.example_sentences
                else item.source_excerpt
            )

            prov = ProvenanceRecord(
                source_id=manifest.id,
                resource_type=manifest.resource_type,
                citation=citation_str,
                page_or_section=item.page_or_section,
                context_sentence=context_sent,
                recorded_year=manifest.year,
                permission_status=manifest.permission_status,
            )

            # Check conservative duplicate / similarity matches across active entries
            dups = self._find_potential_duplicates(hw_clean, existing_entries)
            if dups:
                for d in dups:
                    duplicate_suggestions.append({
                        "candidate_headword": hw_clean,
                        "candidate_meanings": item.meanings,
                        "candidate_dialect": entry_dialect,
                        "matching_entry_id": d["entry_id"],
                        "matching_headword": d["headword"],
                        "matching_meanings": d["meanings"],
                        "match_type": d["match_type"],
                        "score": d["score"],
                        "explanation": d["explanation"],
                    })

            # Check exact match
            if hw_key in existing_lookup:
                target = existing_lookup[hw_key]
                # Conservative rule: Never overwrite verified human definitions
                if target.verification_status != "verified" and item.meanings:
                    for m in item.meanings:
                        if m not in target.meanings:
                            target.meanings.append(m)
                    if item.part_of_speech and not target.part_of_speech:
                        target.part_of_speech = item.part_of_speech
                    if item.dialect and not target.dialect:
                        target.dialect = item.dialect

                # Add provenance citation
                has_prov = any(
                    p.source_id == prov.source_id and p.page_or_section == prov.page_or_section
                    for p in target.provenance
                )
                if not has_prov:
                    target.provenance.append(prov)

                for ex in item.example_sentences:
                    if ex not in target.example_sentences and len(target.example_sentences) < 5:
                        target.example_sentences.append(ex)

                for alt in item.alternative_spellings:
                    if alt not in target.alternative_spellings and alt != target.headword:
                        target.alternative_spellings.append(alt)

                entries_to_update.append(target)
            else:
                cand_id = f"VOCAB-{manifest.id}-{idx:04d}"
                is_dict_source = manifest.resource_type == "dictionaries"
                verif_stat = "needs_review" if (is_dict_source and item.meanings) else "unverified"

                new_entry = VocabularyEntry(
                    id=cand_id,
                    headword=hw_clean,
                    meanings=list(item.meanings),
                    translations_en=list(item.translations_en or item.meanings),
                    alternative_spellings=list(item.alternative_spellings),
                    dialect_variants=[],
                    dialect=entry_dialect,
                    part_of_speech=item.part_of_speech,
                    pronunciation=None,
                    example_sentences=list(item.example_sentences),
                    provenance=[prov],
                    verification_status=verif_stat,
                    license_restrictions=manifest.license,
                    review_status="pending_review",
                    review_notes=f"Extracted via {extraction_method} from {manifest.id}.",
                )
                candidates_to_add.append(new_entry)
                existing_lookup[hw_key] = new_entry

            # If source is dictionary, prepare dictionary_entries record
            if manifest.resource_type == "dictionaries":
                dict_ent = DictionaryEntryRecord(
                    id=f"{manifest.id}-ENT-{idx:04d}",
                    dictionary_id=manifest.id,
                    headword=hw_clean,
                    definitions_en=list(item.meanings),
                    definitions_hi=list(item.definitions_hi),
                    part_of_speech=item.part_of_speech,
                    dialect=entry_dialect,
                    page_or_section=item.page_or_section,
                    entry_number=item.entry_number or f"{idx}",
                    source_excerpt=item.source_excerpt,
                    extraction_method=extraction_method,
                    confidence=item.confidence,
                    permission_status=manifest.permission_status,
                    verification_status="needs_review",
                )
                dict_entries_to_add.append(dict_ent)

        # Identify data gaps (categories with 0 candidates)
        data_gaps = [cat for cat, cnt in category_counts.items() if cnt == 0]

        summary = EnrichmentSummary(
            source_id=source_id,
            source_title=manifest.title,
            permission_status=manifest.permission_status,
            file_path=str(resolved_path),
            file_hash=file_hash,
            extraction_method=extraction_method,
            status="dry_run" if dry_run else "completed",
            items_extracted=len(items),
            candidates_created=len(candidates_to_add),
            entries_updated=len(entries_to_update),
            duplicate_suggestions=duplicate_suggestions[:50],
            category_breakdown=category_counts,
            data_gaps=data_gaps,
            dialect_breakdown=dialect_counts,
            warnings=warnings,
        )

        if dry_run:
            return summary

        # 6. Database persistence with transactional integrity
        run_record = EnrichmentRunRecord(
            id=f"ENRICH-{source_id}-{file_hash[:8]}",
            source_id=source_id,
            file_path=str(resolved_path),
            file_hash=file_hash,
            extraction_method=extraction_method,
            status="completed",
            items_extracted=len(items),
            candidates_created=len(candidates_to_add),
            entries_updated=len(entries_to_update),
            duplicates_detected=len(duplicate_suggestions),
            warnings=warnings,
        )

        try:
            # Ensure dictionary parent record exists for foreign key constraint
            if dict_entries_to_add:
                dict_src = self.dict_repo.get_by_id(manifest.id)
                if not dict_src:
                    dict_src = DictionarySourceRecord(
                        id=manifest.id,
                        title=manifest.title,
                        authors=[manifest.creator] if manifest.creator else [],
                        publication_year=manifest.year,
                        publisher=manifest.publisher,
                        dialect=manifest.dialect,
                        source_url=manifest.source_url,
                        license=manifest.license,
                        permission_status=manifest.permission_status,
                        access_status=getattr(
                            manifest, "access_status", "full_text_available"
                        ),
                        verification_status=manifest.verification_status,
                    )
                    self.dict_repo.add(dict_src)

            # Add new candidates
            for cand in candidates_to_add:
                self.vocab_repo.add(cand)

            # Update matched entries
            for upd in entries_to_update:
                self.vocab_repo.add(upd)

            # Add dictionary records if applicable
            for de in dict_entries_to_add:
                self.dict_repo.add_entry(de)

            # Record run
            self.enrich_repo.record_run(run_record)
        except Exception as e:
            raise RuntimeError(
                f"Transaction rolled back during enrichment of '{source_id}': {e}"
            ) from e

        return summary

    def export_candidates(
        self,
        output_path: Path | str,
        source_id: str | None = None,
        limit: int = 500,
    ) -> int:
        """Export newly extracted candidates to a JSONL file for offline community review."""
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        candidates = self.vocab_repo.list_review_queue(
            review_status="pending_review",
            source_id=source_id,
            limit=limit,
        )

        exported_count = 0
        with out.open("w", encoding="utf-8") as f:
            for cand in candidates:
                # Mask restricted sentences in exported files
                shielded_prov = []
                for p in cand.provenance:
                    p_dict = p.to_dict()
                    if (p.permission_status or "").strip().lower() == "restricted":
                        p_dict["context_sentence"] = "[RESTRICTED TEXT - ACCESS PRIVILEGED]"
                    shielded_prov.append(p_dict)

                record = {
                    "entry_id": cand.id,
                    "headword": cand.headword,
                    "meanings": cand.meanings,
                    "translations_en": cand.translations_en,
                    "alternative_spellings": cand.alternative_spellings,
                    "part_of_speech": cand.part_of_speech,
                    "dialect": cand.dialect,
                    "verification_status": cand.verification_status,
                    "review_status": cand.review_status,
                    "review_notes": cand.review_notes,
                    "provenance": shielded_prov,
                    "categories": classify_lexical_categories(
                        headword=cand.headword,
                        meanings=cand.meanings,
                        part_of_speech=cand.part_of_speech,
                        dialect=cand.dialect,
                    ),
                    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                exported_count += 1

        return exported_count

    def _resolve_file_path(
        self,
        manifest: ManifestRecord,
        file_path: Path | str | None,
    ) -> Path:
        """Resolve absolute local file path from parameter or manifest."""
        resolved: Path | None = None
        if file_path:
            resolved = Path(file_path)
        elif manifest.local_path:
            resolved = Path(manifest.local_path)
            if not resolved.is_absolute():
                resolved = self.config.paths.root_dir / resolved

        if not resolved or not resolved.is_file():
            raise FileNotFoundError(
                f"No accessible local file found for '{manifest.id}'. "
                f"Specified path: '{resolved}'."
            )
        return resolved

    def _extract_items_from_file(
        self,
        manifest: ManifestRecord,
        file_path: Path,
        dialect_override: str | None = None,
    ) -> tuple[list[EnrichmentItem], str, list[str]]:
        """Extract lexical items according to the detected file structure and format."""
        suffix = file_path.suffix.lower()
        warnings: list[str] = []
        dialect = dialect_override or manifest.dialect or "Ukhrul"

        # 1. Structured JSON Lines file
        if suffix in {".jsonl", ".json"}:
            dict_src = DictionarySourceRecord(
                id=manifest.id,
                title=manifest.title,
                dialect=dialect,
                permission_status=manifest.permission_status,
                access_status=getattr(manifest, "access_status", "full_text_available"),
                verification_status=manifest.verification_status,
            )
            dict_entries = self.dict_extractor.extract_from_jsonl(
                source=dict_src,
                file_path=file_path,
                enforce_permissions=False,
            )
            items = [
                EnrichmentItem(
                    headword=de.headword,
                    meanings=de.definitions_en,
                    translations_en=de.definitions_en,
                    definitions_hi=de.definitions_hi,
                    part_of_speech=de.part_of_speech,
                    dialect=de.dialect or dialect,
                    alternative_spellings=de.alternate_spellings,
                    example_sentences=de.examples,
                    page_or_section=de.page_or_section,
                    entry_number=de.entry_number,
                    extraction_method="structured_jsonl",
                    confidence=de.confidence,
                    notes=de.notes,
                )
                for de in dict_entries
            ]
            return items, "structured_jsonl", warnings

        # 2. Structured Tabular file (TSV or CSV)
        if suffix in {".tsv", ".csv"}:
            delimiter = "\t" if suffix == ".tsv" else ","
            dict_src = DictionarySourceRecord(
                id=manifest.id,
                title=manifest.title,
                dialect=dialect,
                permission_status=manifest.permission_status,
                access_status=getattr(manifest, "access_status", "full_text_available"),
                verification_status=manifest.verification_status,
            )
            dict_entries = self.dict_extractor.extract_from_tsv_or_csv(
                source=dict_src,
                file_path=file_path,
                delimiter=delimiter,
                enforce_permissions=False,
            )
            items = [
                EnrichmentItem(
                    headword=de.headword,
                    meanings=de.definitions_en,
                    translations_en=de.definitions_en,
                    definitions_hi=de.definitions_hi,
                    part_of_speech=de.part_of_speech,
                    dialect=de.dialect or dialect,
                    alternative_spellings=de.alternate_spellings,
                    example_sentences=de.examples,
                    page_or_section=de.page_or_section,
                    entry_number=de.entry_number,
                    extraction_method="tabular_import",
                    confidence=de.confidence,
                    notes=de.notes,
                )
                for de in dict_entries
            ]
            return items, "tabular_import", warnings

        # 3. Plain Text File (.txt) — check if structured dictionary lines or running text
        if suffix == ".txt":
            content = file_path.read_text(encoding="utf-8", errors="replace")
            lines = [line.strip() for line in content.splitlines() if line.strip()]

            # Heuristic: if many lines have ':' or '-' separating words,
            # treat as formatted dictionary lines
            pattern = re.compile(
                r"^([A-Za-zāēīōūĀĒĪŌŪ\-\'\s]+?)(?:\s*\(([a-z\.\,\s]+)\))?\s*[:\-–]\s*(.+)$"
            )
            matches_count = sum(1 for line in lines[:20] if pattern.match(line))
            if matches_count >= 3 and len(lines) > 0:
                dict_src = DictionarySourceRecord(
                    id=manifest.id,
                    title=manifest.title,
                    dialect=dialect,
                    permission_status=manifest.permission_status,
                    access_status=getattr(manifest, "access_status", "full_text_available"),
                    verification_status=manifest.verification_status,
                )
                parsed = self.dict_extractor.parse_text_lines(
                    source=dict_src,
                    lines=lines,
                    enforce_permissions=False,
                )
                items = [
                    EnrichmentItem(
                        headword=de.headword,
                        meanings=de.definitions_en,
                        translations_en=de.definitions_en,
                        part_of_speech=de.part_of_speech,
                        dialect=de.dialect or dialect,
                        alternative_spellings=de.alternate_spellings,
                        example_sentences=de.examples,
                        extraction_method="text_line_parser",
                        confidence=de.confidence,
                        notes=de.notes,
                    )
                    for de in parsed
                ]
                return items, "text_line_parser", warnings

        # 4. Running text (TXT, MD, PDF, DOCX)
        ext_res = self.extractor.extract_from_file(file_path, source_id=manifest.id)
        if ext_res.status == "failed":
            warnings.extend(ext_res.warnings)
            raise ValueError(f"Running text extraction failed: {ext_res.notes}")

        word_regex = re.compile(r"\b[A-Za-zÀ-ÿĀ-žḀ-ỿ]+(?:['’-][A-Za-zÀ-ÿĀ-žḀ-ỿ]+)*\b")
        sentence_regex = re.compile(r"([^\.\?!]+[\.\?!]?)", re.UNICODE)

        extracted_words: dict[str, EnrichmentItem] = {}
        for p in ext_res.pages:
            sentences = sentence_regex.findall(p.text)
            for s in sentences:
                s_clean = s.strip()
                if len(s_clean) < 3:
                    continue
                words = word_regex.findall(s_clean)
                for w in words:
                    norm = normalize_unicode(w).strip()
                    if len(norm) < 2:
                        continue
                    key = norm.lower()
                    page_str = f"p. {p.page_number}" if p.page_number is not None else None
                    if key not in extracted_words:
                        extracted_words[key] = EnrichmentItem(
                            headword=norm,
                            meanings=[],  # Running text has no assumed meanings
                            translations_en=[],
                            dialect=dialect,
                            example_sentences=[s_clean],
                            page_or_section=page_str,
                            extraction_method=f"running_text_{ext_res.extraction_method}",
                            confidence=0.8,
                        )
                    else:
                        item = extracted_words[key]
                        if (
                            s_clean not in item.example_sentences
                            and len(item.example_sentences) < 3
                        ):
                            item.example_sentences.append(s_clean)
                        if norm != item.headword and norm not in item.alternative_spellings:
                            item.alternative_spellings.append(norm)

        return list(extracted_words.values()), f"running_text_{ext_res.extraction_method}", warnings

    def _find_potential_duplicates(
        self,
        headword: str,
        existing_entries: list[VocabularyEntry],
        threshold: float = 0.75,
    ) -> list[dict[str, Any]]:
        """Identify potential phonetic and fuzzy duplicate suggestions without merging."""
        target_norm = normalize_unicode(headword).strip().lower()
        target_phonetic = self.phonetic_encoder.encode(headword)
        suggestions: list[dict[str, Any]] = []

        for other in existing_entries:
            other_norm = normalize_unicode(other.headword).strip().lower()
            if target_norm == other_norm:
                continue  # Exact match handled separately

            other_phonetic = self.phonetic_encoder.encode(other.headword)
            if target_phonetic and target_phonetic == other_phonetic:
                expl = f"Phonetic equivalence ({target_phonetic}) with '{other.headword}'"
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "match_type": "phonetic",
                    "score": 0.90,
                    "explanation": expl,
                })
                continue

            sim = calculate_similarity(headword, other.headword)
            if sim >= threshold:
                expl = f"Fuzzy orthographic similarity ({sim:.2f}) with '{other.headword}'"
                suggestions.append({
                    "entry_id": other.id,
                    "headword": other.headword,
                    "meanings": other.meanings,
                    "dialect": other.dialect,
                    "match_type": "fuzzy",
                    "score": round(sim, 3),
                    "explanation": expl,
                })

        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions
