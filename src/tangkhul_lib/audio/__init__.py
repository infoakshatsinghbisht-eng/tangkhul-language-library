"""Audio corpus, pronunciation records, and permission-aware speech data infrastructure."""

from __future__ import annotations

from tangkhul_lib.audio.models import (
    VALID_ANNOTATION_TYPES,
    VALID_AUDIO_FORMATS,
    VALID_AUDIO_PERMISSION_STATUSES,
    VALID_RECORDING_METHODS,
    AudioAnnotation,
    AudioConsentRecord,
    AudioCorpusSummary,
    AudioRecording,
    AudioSegmentTimestamp,
    PronunciationRecord,
)
from tangkhul_lib.audio.permissions import (
    AudioPermissionDeniedError,
    AudioPermissionService,
)
from tangkhul_lib.audio.repository import (
    AudioAnnotationRepository,
    AudioConsentRepository,
    AudioRecordingRepository,
    PronunciationRepository,
)
from tangkhul_lib.audio.service import AudioCorpusService
from tangkhul_lib.audio.validation import (
    AudioSecurityError,
    AudioValidationError,
    compute_file_sha256,
    extract_audio_metadata,
    safe_resolve_audio_path,
    sanitize_filename,
)

__all__ = [
    "VALID_ANNOTATION_TYPES",
    "VALID_AUDIO_FORMATS",
    "VALID_AUDIO_PERMISSION_STATUSES",
    "VALID_RECORDING_METHODS",
    "AudioAnnotation",
    "AudioAnnotationRepository",
    "AudioConsentRecord",
    "AudioConsentRepository",
    "AudioCorpusService",
    "AudioCorpusSummary",
    "AudioPermissionDeniedError",
    "AudioPermissionService",
    "AudioRecording",
    "AudioRecordingRepository",
    "AudioSecurityError",
    "AudioSegmentTimestamp",
    "AudioValidationError",
    "PronunciationRecord",
    "PronunciationRepository",
    "compute_file_sha256",
    "extract_audio_metadata",
    "safe_resolve_audio_path",
    "sanitize_filename",
]
