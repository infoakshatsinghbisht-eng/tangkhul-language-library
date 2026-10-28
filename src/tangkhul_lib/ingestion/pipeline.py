"""Permission-aware document ingestion pipeline for Tangkhul Language Library."""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.core.models import (
    DocumentChunk,
    IngestedDocument,
    ManifestRecord,
    ProvenanceRecord,
    VocabularyEntry,
)
from tangkhul_lib.ingestion.metadata_validation import validate_manifest_file
from tangkhul_lib.ingestion.text_extraction import (
    ExtractionResult,
    TextExtractor,
    compute_file_hash,
    segment_into_chunks,
)
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import (
    DocumentRepository,
    ManifestRepository,
    VocabularyRepository,
)
from tangkhul_lib.vocabulary.normalization import normalize_unicode, sanitize_spacing

# Authorized permission tiers permitting digital text extraction
ALLOWED_INGESTION_PERMISSIONS = frozenset({
    "permitted",
    "public_domain",
    "community_authorized",
})


@dataclass
class PermissionEvaluation:
    """Detailed permission and verification evaluation for a source record."""

    source_id: str
    is_eligible: bool
    permission_status: str
    verification_status: str
    access_status: str | None
    skip_reason: str | None = None


class SourcePermissionChecker:
    """Validates copyright, licensing, community consent, and verification state."""

    @staticmethod
    def evaluate(record: ManifestRecord | dict[str, Any]) -> PermissionEvaluation:
        """Evaluate whether a record is legally and ethically eligible for full-text ingestion."""
        if isinstance(record, ManifestRecord):
            rec_id = record.id
            perm = (record.permission_status or "pending").strip().lower()
            verif = (record.verification_status or "unverified").strip().lower()
            access = getattr(record, "access_status", None)
        else:
            rec_id = str(record.get("id", ""))
            perm = str(record.get("permission_status", "pending")).strip().lower()
            verif = str(record.get("verification_status", "unverified")).strip().lower()
            access = record.get("access_status")

        if access:
            access = str(access).strip().lower()

        # 1. Check for explicit restriction
        if perm == "restricted" or access == "restricted":
            return PermissionEvaluation(
                source_id=rec_id,
                is_eligible=False,
                permission_status=perm,
                verification_status=verif,
                access_status=access,
                skip_reason=(
                    "Resource is explicitly marked 'restricted'. "
                    "Reproduction and full-text ingestion are forbidden."
                ),
            )

        # 2. Check candidate status
        if verif == "needs_review":
            return PermissionEvaluation(
                source_id=rec_id,
                is_eligible=False,
                permission_status=perm,
                verification_status=verif,
                access_status=access,
                skip_reason=(
                    "Source is a candidate record under review ('needs_review'); "
                    "requires bibliographic verification and clearance before ingestion."
                ),
            )

        # 3. Check for pending permissions
        if perm == "pending":
            return PermissionEvaluation(
                source_id=rec_id,
                is_eligible=False,
                permission_status=perm,
                verification_status=verif,
                access_status=access,
                skip_reason=(
                    "Permission status is 'pending'; reproduction rights have not "
                    "yet been confirmed."
                ),
            )

        # 4. Check for authorized tier
        if perm not in ALLOWED_INGESTION_PERMISSIONS:
            return PermissionEvaluation(
                source_id=rec_id,
                is_eligible=False,
                permission_status=perm,
                verification_status=verif,
                access_status=access,
                skip_reason=(
                    f"Permission status '{perm}' is not in authorized tiers: "
                    f"{sorted(ALLOWED_INGESTION_PERMISSIONS)}."
                ),
            )

        # Eligible
        return PermissionEvaluation(
            source_id=rec_id,
            is_eligible=True,
            permission_status=perm,
            verification_status=verif,
            access_status=access,
            skip_reason=None,
        )


class DocumentIngestionPipeline:
    """Coordinates permission checks, text extraction, document storage, and vocab linking."""

    def __init__(
        self,
        db_manager: DatabaseManager,
        extractor: TextExtractor | None = None,
        config: LibraryConfig | None = None,
    ) -> None:
        self.db_manager = db_manager
        self.extractor = extractor or TextExtractor()
        self.config = config or LibraryConfig.from_environment()
        self.doc_repo = DocumentRepository(db_manager)
        self.manifest_repo = ManifestRepository(db_manager)
        self.vocab_repo = VocabularyRepository(db_manager)

    def evaluate_all_sources(
        self,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Scan all six manifest catalogues and categorize sources as eligible or ineligible."""
        manifests_dir = self.config.paths.manifests_dir
        manifest_files = [
            "books.jsonl",
            "songs.jsonl",
            "dictionaries.jsonl",
            "culture.jsonl",
            "history.jsonl",
            "literature.jsonl",
        ]

        eligible: list[dict[str, Any]] = []
        ineligible: list[dict[str, Any]] = []

        for m_name in manifest_files:
            m_path = manifests_dir / m_name
            if not m_path.is_file():
                continue

            try:
                records = validate_manifest_file(m_path)
            except Exception:
                continue

            for rec in records:
                eval_res = SourcePermissionChecker.evaluate(rec)
                info = {
                    "source_id": rec.id,
                    "title": rec.title,
                    "creator": rec.creator,
                    "year": rec.year,
                    "resource_type": rec.resource_type,
                    "permission_status": eval_res.permission_status,
                    "verification_status": eval_res.verification_status,
                    "local_path": rec.local_path,
                    "has_local_file": bool(rec.local_path and Path(rec.local_path).is_file()),
                    "skip_reason": eval_res.skip_reason,
                }
                if eval_res.is_eligible:
                    eligible.append(info)
                else:
                    ineligible.append(info)

        return eligible, ineligible

    def get_manifest_record(self, source_id: str) -> ManifestRecord | None:
        """Look up a manifest record from the database or manifest catalogues."""
        record = self.manifest_repo.get_by_id(source_id)
        if record:
            return record

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

    def preview_document(
        self,
        file_path: Path | str,
        source_id: str = "",
    ) -> dict[str, Any]:
        """Inspect a local file and preview extraction results without saving to the database."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        extraction = self.extractor.extract_from_file(path, source_id=source_id)
        mock_chunks = segment_into_chunks(
            extraction,
            doc_id="PREVIEW",
            source_id=source_id,
            permission_status="preview",
            verification_status="unverified",
        )

        sample_chunks = [
            {
                "id": c.id,
                "page": c.page_number,
                "text": (c.text[:120] + "...") if len(c.text) > 120 else c.text,
                "words": c.word_count,
            }
            for c in mock_chunks[:5]
        ]

        return {
            "source_id": source_id,
            "file_name": path.name,
            "file_format": path.suffix.lower().lstrip("."),
            "file_hash": extraction.file_hash,
            "file_size_bytes": extraction.file_size_bytes,
            "extraction_method": extraction.extraction_method,
            "status": extraction.status,
            "ocr_status": extraction.ocr_status,
            "page_count": extraction.page_count,
            "char_count": extraction.char_count,
            "word_count": extraction.word_count,
            "chunk_count": len(mock_chunks),
            "warnings": extraction.warnings,
            "notes": extraction.notes,
            "sample_chunks": sample_chunks,
        }

    def ingest_document(
        self,
        source_id: str,
        file_path: Path | str | None = None,
        force: bool = False,
        dry_run: bool = False,
        integrate_vocab: bool = True,
    ) -> dict[str, Any]:
        """Execute permission validation, extraction, persistence, and candidate vocabulary."""
        manifest = self.get_manifest_record(source_id)
        if not manifest:
            return {
                "success": False,
                "source_id": source_id,
                "error": f"Source manifest record '{source_id}' not found in any catalogue.",
            }

        # Validate permission
        perm_eval = SourcePermissionChecker.evaluate(manifest)
        if not perm_eval.is_eligible and not force:
            return {
                "success": False,
                "source_id": source_id,
                "skipped": True,
                "permission_status": perm_eval.permission_status,
                "verification_status": perm_eval.verification_status,
                "reason": perm_eval.skip_reason,
            }

        # Resolve local file
        resolved_path: Path | None = None
        if file_path:
            resolved_path = Path(file_path)
        elif manifest.local_path:
            resolved_path = Path(manifest.local_path)
            if not resolved_path.is_absolute():
                resolved_path = self.config.paths.root_dir / resolved_path

        if not resolved_path or not resolved_path.is_file():
            return {
                "success": False,
                "source_id": source_id,
                "skipped": True,
                "reason": f"No accessible local file found for '{source_id}' at: {resolved_path}",
            }

        file_hash = compute_file_hash(resolved_path)

        # Check for idempotent re-ingestion
        existing_doc = self.doc_repo.get_document_by_source_id(source_id)
        if existing_doc and existing_doc.file_hash == file_hash and not force and not dry_run:
            return {
                "success": True,
                "source_id": source_id,
                "document_id": existing_doc.id,
                "already_ingested": True,
                "message": (
                    "File hash unchanged; document already ingested. "
                    "Pass --force to reprocess."
                ),
                "page_count": existing_doc.page_count,
                "word_count": existing_doc.word_count,
            }

        # Extract text
        extraction = self.extractor.extract_from_file(resolved_path, source_id=source_id)
        if extraction.status == "failed":
            return {
                "success": False,
                "source_id": source_id,
                "error": f"Extraction failed: {extraction.notes or 'Unknown extraction error.'}",
                "warnings": extraction.warnings,
            }

        doc_id = f"DOC-{source_id}-{file_hash[:8]}"
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        ingested_doc = IngestedDocument(
            id=doc_id,
            source_id=source_id,
            source_title=manifest.title,
            creator=manifest.creator,
            publication_year=manifest.year,
            source_type=manifest.resource_type,
            language=manifest.language or "Tangkhul",
            file_path=str(resolved_path),
            file_name=resolved_path.name,
            file_hash=file_hash,
            file_size_bytes=extraction.file_size_bytes,
            file_format=resolved_path.suffix.lower().lstrip("."),
            extraction_method=extraction.extraction_method,
            extraction_timestamp=timestamp,
            extraction_status=extraction.status,
            page_count=extraction.page_count,
            char_count=extraction.char_count,
            word_count=extraction.word_count,
            permission_status=manifest.permission_status,
            verification_status=manifest.verification_status,
            extraction_warnings=extraction.warnings,
            ocr_status=extraction.ocr_status,
            review_status="pending_review",
            notes=extraction.notes,
        )

        chunks = segment_into_chunks(
            extraction,
            doc_id=doc_id,
            source_id=source_id,
            permission_status=manifest.permission_status,
            verification_status=manifest.verification_status,
        )

        # Candidate vocabulary extraction
        tokens_extracted, candidate_entries = self._extract_vocabulary_candidates(
            manifest=manifest,
            extraction=extraction,
            chunks=chunks,
        )

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "source_id": source_id,
                "document_id": doc_id,
                "file_path": str(resolved_path),
                "file_format": ingested_doc.file_format,
                "page_count": extraction.page_count,
                "char_count": extraction.char_count,
                "word_count": extraction.word_count,
                "chunk_count": len(chunks),
                "tokens_extracted": len(tokens_extracted),
                "vocabulary_candidates": len(candidate_entries),
                "warnings": extraction.warnings,
                "ocr_status": extraction.ocr_status,
                "notes": extraction.notes,
            }

        # Persist document and chunks
        self.doc_repo.add_document(ingested_doc, chunks)

        # Persist tokens to extracted_tokens table
        self._persist_tokens(source_id, tokens_extracted)

        # Synchronize candidate vocabulary entries
        synced_count = self._integrate_vocabulary(candidate_entries) if integrate_vocab else 0

        return {
            "success": True,
            "source_id": source_id,
            "document_id": doc_id,
            "file_path": str(resolved_path),
            "page_count": extraction.page_count,
            "char_count": extraction.char_count,
            "word_count": extraction.word_count,
            "chunk_count": len(chunks),
            "tokens_extracted": len(tokens_extracted),
            "vocabulary_integrated": synced_count,
            "warnings": extraction.warnings,
            "ocr_status": extraction.ocr_status,
            "extraction_status": extraction.status,
        }

    def _extract_vocabulary_candidates(
        self,
        manifest: ManifestRecord,
        extraction: ExtractionResult,
        chunks: list[DocumentChunk],
    ) -> tuple[list[dict[str, Any]], list[VocabularyEntry]]:
        """Extract candidate tokens and vocabulary entries preserving provenance."""
        raw_tokens: list[dict[str, Any]] = []
        vocab_map: dict[str, VocabularyEntry] = {}

        sentence_regex = re.compile(r"([^\.\?!]+[\.\?!]?)", re.UNICODE)
        word_regex = re.compile(
            r"\b[A-Za-zÀ-ÿĀ-žḀ-ỿ]+(?:['’-][A-Za-zÀ-ÿĀ-žḀ-ỿ]+)*\b",
            re.UNICODE,
        )

        for chunk in chunks:
            page_ref = f"p. {chunk.page_number}" if chunk.page_number is not None else None
            citation_str = (
                f"{manifest.title} ({page_ref})" if page_ref else manifest.title
            )

            sentences = sentence_regex.findall(chunk.text)
            for s in sentences:
                clean_s = sanitize_spacing(s)
                if not clean_s or len(clean_s) < 3:
                    continue

                words = word_regex.findall(clean_s)
                for w in words:
                    norm_w = normalize_unicode(w)
                    if len(norm_w) < 2:
                        continue

                    raw_tokens.append({
                        "source_id": manifest.id,
                        "word_form": norm_w,
                        "page_or_section": page_ref,
                        "context_sentence": clean_s,
                        "extraction_method": extraction.extraction_method,
                        "verification_status": "unverified",
                    })

                    key = norm_w.lower()
                    prov = ProvenanceRecord(
                        source_id=manifest.id,
                        resource_type=manifest.resource_type,
                        citation=citation_str,
                        page_or_section=page_ref,
                        context_sentence=clean_s,
                        recorded_year=manifest.year,
                        permission_status=manifest.permission_status,
                    )

                    if key not in vocab_map:
                        cand_id = f"VOCAB-{manifest.id}-{len(vocab_map) + 1:04d}"
                        vocab_map[key] = VocabularyEntry(
                            id=cand_id,
                            headword=norm_w,
                            meanings=[],  # Meanings are never fabricated
                            translations_en=[],
                            alternative_spellings=[],
                            dialect_variants=[],
                            dialect=manifest.dialect,
                            example_sentences=[clean_s],
                            provenance=[prov],
                            verification_status="unverified",
                        )
                    else:
                        entry = vocab_map[key]
                        if (
                            norm_w != entry.headword
                            and norm_w not in entry.alternative_spellings
                        ):
                            entry.alternative_spellings.append(norm_w)
                        if (
                            clean_s not in entry.example_sentences
                            and len(entry.example_sentences) < 5
                        ):
                            entry.example_sentences.append(clean_s)
                        has_same = any(
                            p.source_id == prov.source_id
                            and p.page_or_section == prov.page_or_section
                            and p.context_sentence == prov.context_sentence
                            for p in entry.provenance
                        )
                        if not has_same:
                            entry.provenance.append(prov)

        return raw_tokens, list(vocab_map.values())

    def _persist_tokens(self, source_id: str, tokens: list[dict[str, Any]]) -> None:
        """Persist extracted tokens into extracted_tokens table."""
        sql = """
        INSERT INTO extracted_tokens (
            source_id, word_form, page_or_section, context_sentence,
            extraction_method, verification_status
        ) VALUES (
            :source_id, :word_form, :page_or_section, :context_sentence,
            :extraction_method, :verification_status
        );
        """
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM extracted_tokens WHERE source_id = ?;", (source_id,))
            for tok in tokens:
                conn.execute(sql, tok)
            conn.commit()

    def _integrate_vocabulary(self, candidates: list[VocabularyEntry]) -> int:
        """Safely connect extracted candidate vocabulary with unified vocabulary entries."""
        existing_entries = self.vocab_repo.list_all()
        existing_lookup: dict[str, VocabularyEntry] = {
            e.headword.strip().lower(): e for e in existing_entries
        }

        integrated_count = 0
        for cand in candidates:
            cand_key = cand.headword.strip().lower()
            if cand_key in existing_lookup:
                # Confident match: extend provenance without overwriting verification status
                target = existing_lookup[cand_key]
                for prov in cand.provenance:
                    has_prov = any(
                        p.source_id == prov.source_id
                        and p.page_or_section == prov.page_or_section
                        for p in target.provenance
                    )
                    if not has_prov:
                        target.provenance.append(prov)
                for ex in cand.example_sentences:
                    if ex not in target.example_sentences and len(target.example_sentences) < 5:
                        target.example_sentences.append(ex)
                for alt in cand.alternative_spellings:
                    if alt not in target.alternative_spellings and alt != target.headword:
                        target.alternative_spellings.append(alt)
                self.vocab_repo.add(target)
                integrated_count += 1
            else:
                # Add candidate vocabulary entry as unverified
                self.vocab_repo.add(cand)
                existing_lookup[cand_key] = cand
                integrated_count += 1

        return integrated_count
