"""Service layer coordinating Tangkhul audio corpus operations, pronunciations, and consent."""

from __future__ import annotations

import datetime
import json
import os
import shutil
from pathlib import Path
from typing import Any

from tangkhul_lib.audio.models import (
    AudioConsentRecord,
    AudioCorpusSummary,
    AudioRecording,
    PronunciationRecord,
)
from tangkhul_lib.audio.permissions import (
    AudioPermissionService,
)
from tangkhul_lib.audio.repository import (
    AudioAnnotationRepository,
    AudioConsentRepository,
    AudioRecordingRepository,
    PronunciationRepository,
)
from tangkhul_lib.audio.validation import (
    extract_audio_metadata,
    safe_resolve_audio_path,
    sanitize_filename,
)
from tangkhul_lib.core.exceptions import ResourceNotFoundError
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import VocabularyRepository
from tangkhul_lib.vocabulary.normalization import normalize_unicode


class AudioCorpusService:
    """Coordinates audio file ingestion, metadata extraction, vocabulary linking,
    consent lifecycle, and permission-aware audio corpus distribution.
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        audio_root: Path | str | None = None,
        audio_repo: AudioRecordingRepository | None = None,
        pron_repo: PronunciationRepository | None = None,
        annotation_repo: AudioAnnotationRepository | None = None,
        consent_repo: AudioConsentRepository | None = None,
        vocab_repo: VocabularyRepository | None = None,
    ) -> None:
        self.db_manager = db_manager
        self.audio_root = (
            Path(audio_root).resolve() if audio_root else Path("data/raw/audio").resolve()
        )
        self.audio_repo = audio_repo or AudioRecordingRepository(db_manager)
        self.pron_repo = pron_repo or PronunciationRepository(db_manager)
        self.annotation_repo = annotation_repo or AudioAnnotationRepository(db_manager)
        self.consent_repo = consent_repo or AudioConsentRepository(db_manager)
        self.vocab_repo = vocab_repo or VocabularyRepository(db_manager)

    @classmethod
    def current_iso_timestamp(cls) -> str:
        """Return current UTC timestamp in ISO 8601 format."""
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def validate_audio_file(self, file_path: Path | str) -> dict[str, Any]:
        """Validate technical specs and path safety for an audio file."""
        return extract_audio_metadata(file_path)

    def import_audio_file(
        self,
        source_path: Path | str | None,
        title: str,
        vocab_entry_id: str | None = None,
        headword: str | None = None,
        speaker_pseudonym: str | None = None,
        dialect: str | None = None,
        village: str | None = None,
        region: str | None = None,
        recording_date: str | None = None,
        recording_method: str = "field_recording",
        recording_source: str | None = None,
        transcription: str | None = None,
        ipa_transcription: str | None = None,
        transliteration: str | None = None,
        source_citation: str | None = None,
        consent_status: str = "pending",
        permitted_uses: list[str] | None = None,
        access_restrictions: str | None = None,
        metadata_only: bool = False,
        dry_run: bool = False,
        recording_id: str | None = None,
    ) -> dict[str, Any]:
        """Import an authorized audio recording into the managed audio corpus.

        Features:
            - Validates path safety and extracts technical audio metadata.
            - Computes SHA-256 and detects duplicates without destructive overwrites.
            - Links to vocabulary entry when a reliable match exists.
            - Creates linked PronunciationRecord when IPA or headword is available.
            - Logs initial AudioConsentRecord audit event.
            - Supports dry-run simulation.
        """
        now = self.current_iso_timestamp()
        clean_consent = AudioPermissionService.validate_permission_tier(consent_status)

        # 1. Resolve vocabulary entry link if provided
        linked_vocab = None
        if vocab_entry_id:
            linked_vocab = self.vocab_repo.get_by_id(vocab_entry_id)
            if not linked_vocab:
                raise ResourceNotFoundError(f"Vocabulary entry '{vocab_entry_id}' not found.")
        elif headword:
            # Search vocabulary for exact or normalized headword match
            exact_matches = self.vocab_repo.search_exact(headword)
            if exact_matches:
                linked_vocab = exact_matches[0]
                vocab_entry_id = linked_vocab.id

        # 2. Process physical audio file if not metadata-only
        tech_meta: dict[str, Any] = {
            "file_format": "wav",
            "file_size_bytes": 0,
            "duration_seconds": 0.0,
            "sample_rate": 0,
            "channels": 1,
            "checksum_sha256": "",
            "warnings": [],
        }
        dest_rel_path: str | None = None

        if not metadata_only and source_path is not None:
            p_source = Path(source_path)
            tech_meta = extract_audio_metadata(p_source)
            checksum = tech_meta["checksum_sha256"]

            # Duplicate detection by checksum
            existing_rec = self.audio_repo.get_by_hash(checksum)
            if existing_rec:
                return {
                    "recording": existing_rec,
                    "pronunciation": None,
                    "is_duplicate": True,
                    "duplicate_id": existing_rec.id,
                    "dry_run": dry_run,
                    "warnings": [
                        f"Audio file checksum '{checksum[:12]}...' already "
                        f"catalogued as '{existing_rec.id}'."
                    ],
                }

            # Prepare safe destination path
            clean_filename = sanitize_filename(p_source.name)
            subfolder = dialect.lower() if dialect else "general"
            dest_dir = self.audio_root / subfolder
            dest_file = dest_dir / clean_filename
            safe_dest = safe_resolve_audio_path(self.audio_root, dest_file)
            dest_rel_path = str(safe_dest.relative_to(self.audio_root)).replace("\\", "/")

            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                if not safe_dest.exists() or safe_dest != p_source.resolve():
                    shutil.copy2(p_source, safe_dest)

        rec_id = (
            recording_id or f"AUD-REC-{now[:10].replace('-', '')}-{os.urandom(3).hex().upper()}"
        )
        norm_transcription = normalize_unicode(transcription) if transcription else None

        dialect_val = (
            dialect.strip() if dialect else (linked_vocab.dialect if linked_vocab else None)
        )

        recording = AudioRecording(
            id=rec_id,
            title=title.strip(),
            vocab_entry_id=vocab_entry_id,
            speaker_pseudonym=speaker_pseudonym.strip() if speaker_pseudonym else None,
            dialect=dialect_val,
            village=village.strip() if village else None,
            region=region.strip() if region else None,
            recording_date=recording_date,
            recording_method=recording_method if not metadata_only else "metadata_only",
            recording_source=recording_source,
            file_path=dest_rel_path,
            original_filename=Path(source_path).name if source_path else None,
            file_format=tech_meta["file_format"],
            duration_seconds=tech_meta["duration_seconds"],
            sample_rate=tech_meta["sample_rate"],
            channels=tech_meta["channels"],
            file_size_bytes=tech_meta["file_size_bytes"],
            checksum_sha256=tech_meta["checksum_sha256"],
            transcription=transcription.strip() if transcription else None,
            transcription_normalized=norm_transcription,
            ipa_transcription=ipa_transcription.strip() if ipa_transcription else None,
            transliteration=transliteration.strip() if transliteration else None,
            source_citation=source_citation,
            consent_status=clean_consent,
            permitted_uses=permitted_uses or ["linguistic_research"],
            access_restrictions=access_restrictions,
            verification_status="verified" if clean_consent == "authorized" else "unverified",
            created_at=now,
            updated_at=now,
        )

        pronunciation_record: PronunciationRecord | None = None
        has_hw = headword or (linked_vocab and linked_vocab.headword)
        if vocab_entry_id and (ipa_transcription or has_hw):
            target_hw = headword or (linked_vocab.headword if linked_vocab else "")
            pron_id = f"PRON-{rec_id}"
            pronunciation_record = PronunciationRecord(
                id=pron_id,
                vocab_entry_id=vocab_entry_id,
                headword=target_hw,
                recording_id=rec_id if not metadata_only else None,
                pronunciation_ipa=ipa_transcription.strip() if ipa_transcription else None,
                dialect=recording.dialect,
                village=recording.village,
                speaker_pseudonym=recording.speaker_pseudonym,
                source_citation=source_citation,
                verification_status="unverified",
                review_status="pending_review",
                created_at=now,
            )

        consent_record = AudioConsentRecord(
            recording_id=rec_id,
            speaker_pseudonym=recording.speaker_pseudonym or "Anonymous",
            consent_status=clean_consent,
            permitted_uses=recording.permitted_uses,
            restrictions=access_restrictions,
            recorded_date=recording_date or now[:10],
            authorized_by="Library Audio Import Service",
            timestamp=now,
        )

        if not dry_run:
            self.audio_repo.add(recording)
            if pronunciation_record:
                self.pron_repo.add(pronunciation_record)
            self.consent_repo.record_event(consent_record)

        return {
            "recording": recording,
            "pronunciation": pronunciation_record,
            "consent_event": consent_record,
            "is_duplicate": False,
            "dry_run": dry_run,
            "warnings": tech_meta["warnings"],
        }

    def get_recording(
        self,
        recording_id: str,
        is_privileged_view: bool = False,
    ) -> dict[str, Any] | None:
        """Fetch recording by ID with sensitive details shielded unless privileged."""
        rec = self.audio_repo.get_by_id(recording_id)
        if not rec:
            return None
        return AudioPermissionService.mask_recording_metadata(
            rec, is_privileged_view=is_privileged_view
        )

    def list_recordings(
        self,
        dialect: str | None = None,
        village: str | None = None,
        consent_status: str | None = None,
        include_withdrawn: bool = False,
        limit: int = 50,
        offset: int = 0,
        is_privileged_view: bool = False,
    ) -> list[dict[str, Any]]:
        """List recordings with deterministic filtering and privacy shielding."""
        recs = self.audio_repo.list_recordings(
            dialect=dialect,
            village=village,
            consent_status=consent_status,
            is_withdrawn=False if not include_withdrawn else None,
            limit=limit,
            offset=offset,
        )
        return [
            AudioPermissionService.mask_recording_metadata(r, is_privileged_view=is_privileged_view)
            for r in recs
        ]

    def search_audio(
        self,
        query: str,
        dialect: str | None = None,
        include_withdrawn: bool = False,
        limit: int = 50,
        is_privileged_view: bool = False,
    ) -> list[dict[str, Any]]:
        """Search recordings across titles, transcriptions, IPA, and speakers with shielding."""
        results = self.audio_repo.search(
            query=query,
            dialect=dialect,
            include_withdrawn=include_withdrawn,
            limit=limit,
        )
        return [
            AudioPermissionService.mask_recording_metadata(r, is_privileged_view=is_privileged_view)
            for r in results
        ]

    def withdraw_consent(
        self,
        recording_id: str,
        reason: str,
        date: str | None = None,
        authorized_by: str | None = None,
    ) -> AudioRecording:
        """Withdraw consent for an audio recording, revoking export and playback rights."""
        rec = self.audio_repo.get_by_id(recording_id)
        if not rec:
            raise ResourceNotFoundError(f"Audio recording '{recording_id}' not found.")

        updated_rec, consent_audit = AudioPermissionService.withdraw_consent(
            recording=rec,
            reason=reason,
            date=date,
            authorized_by=authorized_by,
        )
        self.audio_repo.add(updated_rec)
        self.consent_repo.record_event(consent_audit)
        return updated_rec

    def get_pronunciations_for_vocab(
        self,
        vocab_entry_id: str,
    ) -> list[PronunciationRecord]:
        """Fetch all pronunciation variants linked to a vocabulary entry."""
        return self.pron_repo.get_by_vocab_id(vocab_entry_id)

    def search_pronunciations(
        self,
        query: str,
        dialect: str | None = None,
        limit: int = 50,
    ) -> list[PronunciationRecord]:
        """Search pronunciations by headword or dialect."""
        clean = normalize_unicode(query).strip().lower()
        all_prons = self.pron_repo.list_all(dialect=dialect, limit=limit * 2)
        matches = [
            p for p in all_prons
            if clean in normalize_unicode(p.headword).lower()
            or (p.pronunciation_ipa and clean in p.pronunciation_ipa.lower())
        ]
        return matches[:limit]

    def review_pronunciation(
        self,
        pronunciation_id: str,
        reviewer: str,
        decision: str,
        notes: str | None = None,
    ) -> PronunciationRecord:
        """Review and update pronunciation verification status."""
        pron = self.pron_repo.get_by_id(pronunciation_id)
        if not pron:
            raise ResourceNotFoundError(f"Pronunciation record '{pronunciation_id}' not found.")

        clean_dec = decision.strip().lower()
        now = self.current_iso_timestamp()

        pron.reviewer = reviewer.strip()
        pron.reviewed_at = now
        pron.review_notes = notes.strip() if notes else None

        if clean_dec in {"approve", "accept"}:
            pron.review_status = "accepted"
            pron.verification_status = "verified"
        elif clean_dec == "reject":
            pron.review_status = "rejected"
            pron.verification_status = "unverified"
        elif clean_dec == "flag_conflict":
            pron.review_status = "conflict"
            pron.verification_status = "needs_review"
        else:
            pron.review_status = clean_dec

        self.pron_repo.add(pron)
        return pron

    def export_corpus(
        self,
        output_dir: Path | str,
        dialect: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Export authorized recordings to a distribution directory with audio manifest.

        Strictly excludes any withdrawn, restricted, pending, or unverified audio files.
        """
        out_p = Path(output_dir).resolve()
        recordings = self.audio_repo.list_recordings(dialect=dialect, limit=5000)

        eligible: list[AudioRecording] = []
        skipped_withdrawn = 0
        skipped_unauthorized = 0
        skipped_restricted = 0
        skipped_missing_file = 0

        for r in recordings:
            if r.is_withdrawn:
                skipped_withdrawn += 1
                continue
            if not AudioPermissionService.can_export(r):
                if r.consent_status != "authorized":
                    skipped_unauthorized += 1
                elif r.access_restrictions == "restricted":
                    skipped_restricted += 1
                else:
                    skipped_unauthorized += 1
                continue

            if not r.file_path:
                continue

            # Verify local file exists
            audio_full_path = self.audio_root / r.file_path
            if not audio_full_path.is_file():
                skipped_missing_file += 1
                continue

            eligible.append(r)

        if not dry_run and eligible:
            out_p.mkdir(parents=True, exist_ok=True)
            export_audio_dir = out_p / "audio"
            export_audio_dir.mkdir(parents=True, exist_ok=True)

            manifest_records = []
            for r in eligible:
                src_audio = self.audio_root / r.file_path  # type: ignore[operator]
                dest_audio = export_audio_dir / src_audio.name
                shutil.copy2(src_audio, dest_audio)

                rec_dict = r.to_dict()
                rec_dict["file_path"] = f"audio/{src_audio.name}"
                manifest_records.append(rec_dict)

            manifest_path = out_p / "audio_manifest.jsonl"
            with manifest_path.open("w", encoding="utf-8") as f:
                for entry in manifest_records:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return {
            "exported_count": len(eligible),
            "output_directory": str(out_p),
            "dry_run": dry_run,
            "skipped_withdrawn": skipped_withdrawn,
            "skipped_unauthorized": skipped_unauthorized,
            "skipped_restricted": skipped_restricted,
            "skipped_missing_file": skipped_missing_file,
        }

    def get_summary(self) -> AudioCorpusSummary:
        """Tabulate real status, format distribution, and dialect coverage."""
        all_recs = self.audio_repo.list_recordings(limit=10000)

        authorized_count = sum(
            1 for r in all_recs if r.consent_status == "authorized" and not r.is_withdrawn
        )
        pending_count = sum(
            1 for r in all_recs if r.consent_status == "pending" and not r.is_withdrawn
        )
        metadata_only_count = sum(
            1 for r in all_recs if r.recording_method == "metadata_only" or not r.file_path
        )

        summary = AudioCorpusSummary(
            total_recordings=len(all_recs),
            authorized_count=authorized_count,
            pending_count=pending_count,
            restricted_count=sum(1 for r in all_recs if r.access_restrictions == "restricted"),
            withdrawn_count=sum(1 for r in all_recs if r.is_withdrawn),
            metadata_only_count=metadata_only_count,
            total_duration_seconds=round(sum(r.duration_seconds for r in all_recs), 2),
            linked_vocab_count=sum(1 for r in all_recs if r.vocab_entry_id),
            verified_pronunciations_count=self.pron_repo.count(),
        )

        for r in all_recs:
            fmt = (r.file_format or "unknown").lower()
            summary.formats_breakdown[fmt] = summary.formats_breakdown.get(fmt, 0) + 1
            dia = r.dialect or "Unassigned"
            summary.dialect_breakdown[dia] = summary.dialect_breakdown.get(dia, 0) + 1

        return summary
