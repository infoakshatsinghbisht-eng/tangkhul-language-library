"""Unit and integration tests for Step 15: Tangkhul Audio Corpus, Pronunciation Records,
and Permission-Aware Speech Data Infrastructure.

NOTE: All audio files used in these tests are purely synthetic test fixtures
generated programmatically for technical verification. They do NOT represent
authentic Tangkhul speech or linguistic evidence.
"""

from __future__ import annotations

import wave
from pathlib import Path

import pytest

from tangkhul_lib.audio.models import (
    AudioRecording,
    PronunciationRecord,
)
from tangkhul_lib.audio.permissions import (
    AudioPermissionService,
)
from tangkhul_lib.audio.service import AudioCorpusService
from tangkhul_lib.audio.validation import (
    AudioSecurityError,
    AudioValidationError,
    extract_audio_metadata,
    safe_resolve_audio_path,
    sanitize_filename,
)
from tangkhul_lib.cli import main
from tangkhul_lib.core.models import VocabularyEntry
from tangkhul_lib.storage.database import DatabaseManager


def create_synthetic_wav(
    target_path: Path,
    duration_seconds: float = 0.25,
    sample_rate: int = 16000,
    channels: int = 1,
) -> Path:
    """Generate a minimal synthetic PCM WAV audio fixture for technical format testing.

    THIS IS A TEST FIXTURE ONLY. It contains no human speech.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    num_frames = int(sample_rate * duration_seconds)

    with wave.open(str(target_path), "wb") as wav_out:
        wav_out.setnchannels(channels)
        wav_out.setsampwidth(2)  # 16-bit
        wav_out.setframerate(sample_rate)

        # Generate unique synthetic audio fixture frames
        import os
        raw_frames = os.urandom(num_frames * channels * 2)
        wav_out.writeframes(raw_frames)

    return target_path


@pytest.fixture
def mem_db() -> DatabaseManager:
    """Isolated in-memory DatabaseManager initialized with full schema."""
    db = DatabaseManager(":memory:")
    db.initialize_schema()
    return db


@pytest.fixture
def audio_test_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for synthetic audio files and exports."""
    audio_dir = tmp_path / "audio_storage"
    audio_dir.mkdir(parents=True, exist_ok=True)
    return audio_dir


@pytest.fixture
def audio_service(mem_db: DatabaseManager, audio_test_dir: Path) -> AudioCorpusService:
    """Instantiate AudioCorpusService pointing to temporary storage."""
    return AudioCorpusService(db_manager=mem_db, audio_root=audio_test_dir)


@pytest.fixture
def sample_vocab_entry(mem_db: DatabaseManager) -> VocabularyEntry:
    """Seed a sample vocabulary entry into the database for audio linkage tests."""
    repo = AudioCorpusService(mem_db).vocab_repo
    entry = VocabularyEntry(
        id="VOCAB-AUD-TEST-001",
        headword="ngashān",
        meanings=["custom", "tradition"],
        alternative_spellings=["ngashan"],
        dialect="Ukhrul",
        part_of_speech="noun",
    )
    repo.add(entry)
    return entry


# ==============================================================================
# 1. Technical Audio Validation & Path Security
# ==============================================================================


def test_synthetic_wav_extraction(tmp_path: Path) -> None:
    """Verify that extract_audio_metadata accurately extracts WAV technical specs."""
    wav_path = tmp_path / "test_tone.wav"
    create_synthetic_wav(wav_path, duration_seconds=0.5, sample_rate=16000, channels=1)

    meta = extract_audio_metadata(wav_path)
    assert meta["file_format"] == "wav"
    assert meta["sample_rate"] == 16000
    assert meta["channels"] == 1
    assert pytest.approx(meta["duration_seconds"], rel=1e-2) == 0.5
    assert meta["file_size_bytes"] > 0
    assert len(meta["checksum_sha256"]) == 64


def test_missing_and_empty_audio_files(tmp_path: Path) -> None:
    """Ensure missing and 0-byte audio files raise appropriate exceptions."""
    missing_file = tmp_path / "non_existent.wav"
    with pytest.raises(FileNotFoundError):
        extract_audio_metadata(missing_file)

    empty_file = tmp_path / "empty.wav"
    empty_file.write_bytes(b"")
    with pytest.raises(AudioValidationError, match="empty"):
        extract_audio_metadata(empty_file)


def test_unsupported_audio_format(tmp_path: Path) -> None:
    """Ensure unsupported audio extensions are rejected."""
    bad_file = tmp_path / "recording.txt"
    bad_file.write_text("not audio", encoding="utf-8")
    with pytest.raises(AudioValidationError, match="Unsupported audio format"):
        extract_audio_metadata(bad_file)


def test_corrupt_wav_header(tmp_path: Path) -> None:
    """Ensure malformed or truncated WAV headers are detected as validation errors."""
    corrupt_file = tmp_path / "corrupt.wav"
    corrupt_file.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt invalid_content")
    with pytest.raises(AudioValidationError, match="Invalid or corrupt WAV"):
        extract_audio_metadata(corrupt_file)


def test_sanitize_filename() -> None:
    """Verify that sanitize_filename strips path traversal sequences and separators."""
    assert sanitize_filename("sample.wav") == "sample.wav"
    assert sanitize_filename("folder/sub/sample.wav") == "sample.wav"
    assert sanitize_filename("..\\..\\malicious.wav") == "malicious.wav"

    with pytest.raises(AudioSecurityError):
        sanitize_filename("")

    with pytest.raises(AudioSecurityError):
        sanitize_filename("..")


def test_safe_resolve_audio_path(tmp_path: Path) -> None:
    """Verify that safe_resolve_audio_path prevents directory traversal outside base dir."""
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # Valid relative path
    safe_path = safe_resolve_audio_path(base_dir, "sub/file.wav")
    assert safe_path == (base_dir / "sub" / "file.wav").resolve()

    # Path traversal attack
    with pytest.raises(AudioSecurityError, match="Path traversal detected"):
        safe_resolve_audio_path(base_dir, "../outside.wav")


# ==============================================================================
# 2. Duplicate Detection via SHA-256 Checksum
# ==============================================================================


def test_duplicate_checksum_detection(
    audio_service: AudioCorpusService,
    tmp_path: Path,
    sample_vocab_entry: VocabularyEntry,
) -> None:
    """Verify that importing the exact same audio file twice detects duplicates idempotently."""
    wav_file = tmp_path / "speech_clip.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.3, sample_rate=16000)

    # First import
    res1 = audio_service.import_audio_file(
        source_path=wav_file,
        title="First Recording",
        vocab_entry_id=sample_vocab_entry.id,
        consent_status="authorized",
    )
    assert not res1["is_duplicate"]
    rec1 = res1["recording"]

    # Second import with different title but identical checksum
    res2 = audio_service.import_audio_file(
        source_path=wav_file,
        title="Duplicate Attempt",
        vocab_entry_id=sample_vocab_entry.id,
        consent_status="authorized",
    )
    assert res2["is_duplicate"]
    assert res2["duplicate_id"] == rec1.id
    assert "already catalogued" in res2["warnings"][0]


# ==============================================================================
# 3. Audio Corpus Service: Ingestion, Metadata, and Vocabulary Linking
# ==============================================================================


def test_import_audio_with_vocab_linking(
    audio_service: AudioCorpusService,
    tmp_path: Path,
    sample_vocab_entry: VocabularyEntry,
) -> None:
    """Verify importing an authorized recording linked to an existing vocabulary entry."""
    wav_file = tmp_path / "ngashan_ukhrul.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.4, sample_rate=16000)

    res = audio_service.import_audio_file(
        source_path=wav_file,
        title="Pronunciation of ngashan",
        vocab_entry_id=sample_vocab_entry.id,
        speaker_pseudonym="Speaker_Ukr_01",
        dialect="Ukhrul",
        village="Hunphun",
        transcription="ngashan",
        ipa_transcription="ŋaʃan",
        consent_status="authorized",
        permitted_uses=["linguistic_research", "community_education"],
    )

    rec = res["recording"]
    assert rec.id.startswith("AUD-REC-")
    assert rec.vocab_entry_id == sample_vocab_entry.id
    assert rec.dialect == "Ukhrul"
    assert rec.speaker_pseudonym == "Speaker_Ukr_01"
    assert rec.ipa_transcription == "ŋaʃan"
    assert rec.consent_status == "authorized"
    assert rec.file_path is not None

    # Check linked pronunciation record was auto-created
    pron = res["pronunciation"]
    assert pron is not None
    assert pron.vocab_entry_id == sample_vocab_entry.id
    assert pron.headword == sample_vocab_entry.headword
    assert pron.pronunciation_ipa == "ŋaʃan"

    # Check consent audit record was logged
    consent_events = audio_service.consent_repo.get_by_recording_id(rec.id)
    assert len(consent_events) == 1
    assert consent_events[0].consent_status == "authorized"
    assert consent_events[0].speaker_pseudonym == "Speaker_Ukr_01"


def test_metadata_only_import(audio_service: AudioCorpusService) -> None:
    """Verify metadata-only recording registration when audio cannot be redistributed."""
    res = audio_service.import_audio_file(
        source_path=None,
        title="Archival Folk Speech Reference",
        dialect="Raphei",
        speaker_pseudonym="Elder_Rph_02",
        transcription="Phanit kasa",
        ipa_transcription="pʰanit kasa",
        consent_status="pending",
        metadata_only=True,
    )

    rec = res["recording"]
    assert rec.recording_method == "metadata_only"
    assert rec.file_path is None
    assert rec.file_size_bytes == 0
    assert rec.consent_status == "pending"


def test_dry_run_import(
    audio_service: AudioCorpusService,
    tmp_path: Path,
) -> None:
    """Verify that dry-run import simulates registration without mutating the database."""
    wav_file = tmp_path / "dry_run.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.2)

    res = audio_service.import_audio_file(
        source_path=wav_file,
        title="Dry Run Test",
        consent_status="authorized",
        dry_run=True,
    )

    assert res["dry_run"] is True
    # Verify nothing was added to database
    assert audio_service.audio_repo.count() == 0
    assert audio_service.pron_repo.count() == 0


# ==============================================================================
# 4. Consent Lifecycle, Access Control, and Withdrawal Safeguards
# ==============================================================================


def test_permission_service_access_rules() -> None:
    """Test explicit permission status checks for audio binary access and export."""
    # Authorized recording
    rec_auth = AudioRecording(
        id="R1",
        title="Auth",
        consent_status="authorized",
        verification_status="verified",
    )
    assert AudioPermissionService.can_access_audio(rec_auth) is True
    assert AudioPermissionService.can_export(rec_auth) is True

    # Pending consent
    rec_pending = AudioRecording(
        id="R2",
        title="Pending",
        consent_status="pending",
        verification_status="unverified",
    )
    assert AudioPermissionService.can_access_audio(rec_pending) is False
    assert AudioPermissionService.can_export(rec_pending) is False

    # Restricted access
    rec_restricted = AudioRecording(
        id="R3",
        title="Restricted",
        consent_status="authorized",
        access_restrictions="restricted",
        verification_status="verified",
    )
    assert AudioPermissionService.can_access_audio(rec_restricted) is False
    assert AudioPermissionService.can_export(rec_restricted) is False

    # Withdrawn consent
    rec_withdrawn = AudioRecording(
        id="R4",
        title="Withdrawn",
        consent_status="withdrawn",
        is_withdrawn=True,
        verification_status="verified",
    )
    assert AudioPermissionService.can_access_audio(rec_withdrawn) is False
    assert AudioPermissionService.can_export(rec_withdrawn) is False


def test_consent_withdrawal_and_audit(
    audio_service: AudioCorpusService,
    tmp_path: Path,
) -> None:
    """Verify speaker consent withdrawal revokes rights and logs immutable audit trail."""
    wav_file = tmp_path / "consent_test.wav"
    create_synthetic_wav(wav_file)

    res = audio_service.import_audio_file(
        source_path=wav_file,
        title="Song Snippet",
        speaker_pseudonym="Performer_A",
        consent_status="authorized",
    )
    rec_id = res["recording"].id

    # Initially accessible
    rec = audio_service.audio_repo.get_by_id(rec_id)
    assert rec is not None
    assert AudioPermissionService.can_access_audio(rec) is True

    # Withdraw consent
    updated_rec = audio_service.withdraw_consent(
        recording_id=rec_id,
        reason="Speaker requested removal from public access repository.",
        authorized_by="Community Custodian Committee",
    )

    assert updated_rec.is_withdrawn is True
    assert updated_rec.consent_status == "withdrawn"
    assert "Speaker requested removal" in updated_rec.withdrawal_reason
    assert AudioPermissionService.can_access_audio(updated_rec) is False

    # Verify audit log captures both initial consent and withdrawal event
    events = audio_service.consent_repo.get_by_recording_id(rec_id)
    assert len(events) == 2
    assert events[0].consent_status == "authorized"
    assert events[1].consent_status == "withdrawn"
    assert events[1].withdrawn_reason == "Speaker requested removal from public access repository."


def test_metadata_shielding_for_restricted_records() -> None:
    """Verify that unprivileged views mask sensitive paths and transcriptions."""
    rec = AudioRecording(
        id="AUD-RESTRICTED-01",
        title="Sacred Ritual Chant",
        file_path="general/sacred.wav",
        speaker_pseudonym="Elder_X",
        transcription="Sacred verbatim ritual text",
        access_restrictions="restricted",
        consent_status="authorized",
    )

    # Ordinary / public view
    masked = AudioPermissionService.mask_recording_metadata(rec, is_privileged_view=False)
    assert masked["file_path"] == "[RESTRICTED AUDIO FILE - ACCESS PRIVILEGED]"
    assert masked["transcription"] == "[RESTRICTED TEXT - SACRED/TABOO CONTENT]"
    assert masked["speaker_pseudonym"] == "[SHIELDED SPEAKER]"

    # Privileged custodian view
    unmasked = AudioPermissionService.mask_recording_metadata(rec, is_privileged_view=True)
    assert unmasked["file_path"] == "general/sacred.wav"
    assert unmasked["transcription"] == "Sacred verbatim ritual text"
    assert unmasked["speaker_pseudonym"] == "Elder_X"


# ==============================================================================
# 5. Pronunciation Records & Native-Speaker Review Workflow
# ==============================================================================


def test_multiple_pronunciation_variants(
    audio_service: AudioCorpusService,
    sample_vocab_entry: VocabularyEntry,
) -> None:
    """Verify multiple pronunciation variants can be linked to one vocabulary entry."""
    # Variant 1: Standard Ukhrul
    p1 = PronunciationRecord(
        id="PRON-001",
        vocab_entry_id=sample_vocab_entry.id,
        headword=sample_vocab_entry.headword,
        pronunciation_ipa="ŋaʃan",
        dialect="Ukhrul",
        is_primary=True,
    )
    audio_service.pron_repo.add(p1)

    # Variant 2: Raphei dialect variant
    p2 = PronunciationRecord(
        id="PRON-002",
        vocab_entry_id=sample_vocab_entry.id,
        headword=sample_vocab_entry.headword,
        pronunciation_ipa="ŋasʰan",
        dialect="Raphei",
        is_primary=False,
    )
    audio_service.pron_repo.add(p2)

    linked = audio_service.get_pronunciations_for_vocab(sample_vocab_entry.id)
    assert len(linked) == 2
    assert {p.pronunciation_ipa for p in linked} == {"ŋaʃan", "ŋasʰan"}


def test_pronunciation_review_workflow(
    audio_service: AudioCorpusService,
    sample_vocab_entry: VocabularyEntry,
) -> None:
    """Verify pronunciation review decisions (approve, reject, flag_conflict)."""
    pron = PronunciationRecord(
        id="PRON-REV-01",
        vocab_entry_id=sample_vocab_entry.id,
        headword="ngashan",
        pronunciation_ipa="ŋaʃan",
        review_status="pending_review",
        verification_status="unverified",
    )
    audio_service.pron_repo.add(pron)

    # Reviewer approves
    reviewed = audio_service.review_pronunciation(
        pronunciation_id="PRON-REV-01",
        reviewer="linguist_tangkhul_01",
        decision="approve",
        notes="Accurate Ukhrul standard pronunciation.",
    )

    assert reviewed.review_status == "accepted"
    assert reviewed.verification_status == "verified"
    assert reviewed.reviewer == "linguist_tangkhul_01"


# ==============================================================================
# 6. Corpus Export with Strict Permission Safeguards
# ==============================================================================


def test_corpus_export_filters(
    audio_service: AudioCorpusService,
    tmp_path: Path,
) -> None:
    """Verify that audio corpus export strictly excludes pending, restricted, or withdrawn files."""
    # 1. Authorized & verified recording (should be exported)
    wav1 = tmp_path / "valid.wav"
    create_synthetic_wav(wav1, duration_seconds=0.35)
    res1 = audio_service.import_audio_file(
        source_path=wav1,
        title="Cleared Speech",
        consent_status="authorized",
    )

    # 2. Pending recording (should be skipped)
    wav2 = tmp_path / "pending.wav"
    create_synthetic_wav(wav2, duration_seconds=0.45)
    audio_service.import_audio_file(
        source_path=wav2,
        title="Pending Recording",
        consent_status="pending",
    )

    # 3. Withdrawn recording (should be skipped)
    wav3 = tmp_path / "withdrawn.wav"
    create_synthetic_wav(wav3, duration_seconds=0.55)
    res3 = audio_service.import_audio_file(
        source_path=wav3,
        title="Withdrawn Item",
        consent_status="authorized",
    )
    audio_service.withdraw_consent(res3["recording"].id, reason="Speaker withdrawn")

    # Run export
    export_dir = tmp_path / "export_output"
    export_res = audio_service.export_corpus(export_dir, dry_run=False)

    assert export_res["exported_count"] == 1
    assert export_res["skipped_unauthorized"] >= 1
    assert export_res["skipped_withdrawn"] >= 1

    # Check manifest exists in export
    manifest_file = export_dir / "audio_manifest.jsonl"
    assert manifest_file.is_file()
    lines = manifest_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert res1["recording"].id in lines[0]


# ==============================================================================
# 7. Database Migration & Idempotency
# ==============================================================================


def test_schema_migration_idempotency(mem_db: DatabaseManager) -> None:
    """Verify that re-initializing schema repeatedly is idempotent and does not corrupt data."""
    repo = AudioCorpusService(mem_db).audio_repo
    rec = AudioRecording(id="REC-IDEM-01", title="Idempotency Test")
    repo.add(rec)

    # Re-run schema initialization
    mem_db.initialize_schema()

    # Verify record persists
    fetched = repo.get_by_id("REC-IDEM-01")
    assert fetched is not None
    assert fetched.title == "Idempotency Test"


# ==============================================================================
# 8. CLI Audio Integration Smoke Tests
# ==============================================================================


def test_cli_audio_summary(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify `tangkhul audio summary` CLI command runs cleanly."""
    rc = main(["audio", "summary"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "TANGKHUL AUDIO CORPUS & PRONUNCIATION TELEMETRY" in out
    assert "Total Recordings:" in out


def test_cli_audio_list_and_flags(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify `tangkhul audio list` and `tangkhul audio --list` execute cleanly."""
    rc1 = main(["audio", "list"])
    assert rc1 == 0
    out1 = capsys.readouterr().out
    assert "TANGKHUL AUDIO RECORDINGS" in out1

    rc2 = main(["audio", "--list"])
    assert rc2 == 0
    out2 = capsys.readouterr().out
    assert "TANGKHUL AUDIO RECORDINGS" in out2


def test_cli_audio_validate(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify `tangkhul audio validate` CLI command analyzes synthetic audio fixture."""
    wav_file = tmp_path / "cli_valid.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.3)

    rc = main(["audio", "validate", str(wav_file)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "AUDIO FILE VALIDATION" in out
    assert "Status:           VALID (WAV)" in out


def test_cli_audio_import_and_inspect(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify `tangkhul audio import` and `tangkhul audio inspect` CLI workflow."""
    wav_file = tmp_path / "cli_import.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.25)

    # 1. Import
    rc_import = main([
        "audio",
        "import",
        str(wav_file),
        "--title",
        "CLI Test Audio",
        "--speaker",
        "Speaker_Test_09",
        "--dialect",
        "Ukhrul",
        "--consent-status",
        "authorized",
    ])
    assert rc_import == 0
    out_import = capsys.readouterr().out
    assert "AUDIO RECORDING IMPORTED" in out_import
    assert "CLI Test Audio" in out_import

    # Extract recording ID from output
    rec_id = None
    for line in out_import.splitlines():
        if "Recording ID:" in line:
            rec_id = line.split(":", 1)[1].strip()
            break
    assert rec_id is not None

    # 2. Inspect
    rc_inspect = main(["audio", "inspect", rec_id])
    assert rc_inspect == 0
    out_inspect = capsys.readouterr().out
    assert "AUDIO RECORDING: CLI Test Audio" in out_inspect
    assert "Speaker_Test_09" in out_inspect
    assert "Consent Status:    AUTHORIZED" in out_inspect


def test_cli_audio_permissions_withdrawal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify consent withdrawal via `tangkhul audio permissions --withdraw`."""
    wav_file = tmp_path / "cli_withdraw.wav"
    create_synthetic_wav(wav_file, duration_seconds=0.38)

    # Import
    main([
        "audio",
        "import",
        str(wav_file),
        "--title",
        "Withdrawal CLI Test",
        "--consent-status",
        "authorized",
    ])
    out_import = capsys.readouterr().out
    rec_id = None
    for line in out_import.splitlines():
        if "Recording ID:" in line:
            rec_id = line.split(":", 1)[1].strip()
            break
    assert rec_id is not None

    # Withdraw consent
    rc_withdraw = main([
        "audio",
        "permissions",
        rec_id,
        "--withdraw",
        "--reason",
        "Speaker requested complete removal.",
        "--authorized-by",
        "Ethical Committee",
    ])
    assert rc_withdraw == 0
    out_withdraw = capsys.readouterr().out
    assert "CONSENT WITHDRAWN" in out_withdraw
    assert "Status:           WITHDRAWN (Revoked)" in out_withdraw

    # Verify inspection confirms withdrawal
    main(["audio", "inspect", rec_id])
    out_inspect = capsys.readouterr().out
    assert "Withdrawn:         YES" in out_inspect
    assert "Withdrawal Reason: Speaker requested complete removal." in out_inspect
