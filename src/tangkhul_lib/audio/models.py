"""Domain models and schema for Tangkhul Audio Corpus and Pronunciations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

VALID_AUDIO_FORMATS = frozenset({
    "wav",
    "mp3",
    "ogg",
    "flac",
    "m4a",
    "aac",
})

VALID_AUDIO_PERMISSION_STATUSES = frozenset({
    "pending",
    "authorized",
    "restricted",
    "withdrawn",
    "needs_review",
})

VALID_RECORDING_METHODS = frozenset({
    "field_recording",
    "studio",
    "archival_transfer",
    "community_submission",
    "metadata_only",
})

VALID_ANNOTATION_TYPES = frozenset({
    "segment",
    "word",
    "phoneme",
    "hypothesis",
})


@dataclass
class AudioSegmentTimestamp:
    """Optional time-aligned segment within an audio recording."""

    start_seconds: float
    end_seconds: float
    text_verbatim: str
    text_normalized: str = ""
    ipa: str | None = None
    confidence_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioSegmentTimestamp:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class AudioRecording:
    """Represents an individual audio recording in the Tangkhul speech corpus."""

    id: str
    title: str
    vocab_entry_id: str | None = None
    corpus_id: str | None = None
    description: str | None = None
    recording_date: str | None = None
    speaker_pseudonym: str | None = None
    dialect: str | None = None
    village: str | None = None
    region: str | None = None
    language: str = "Tangkhul"
    variety: str | None = None
    recording_method: str = "field_recording"
    recording_source: str | None = None
    file_path: str | None = None
    original_filename: str | None = None
    file_format: str = "wav"
    duration_seconds: float = 0.0
    sample_rate: int = 0
    channels: int = 1
    file_size_bytes: int = 0
    checksum_sha256: str = ""
    transcription: str | None = None
    transcription_normalized: str | None = None
    ipa_transcription: str | None = None
    transliteration: str | None = None
    source_title: str | None = None
    source_citation: str | None = None
    source_url: str | None = None
    license: str | None = None
    copyright_status: str = "copyright_retained"
    consent_status: str = "pending"
    permitted_uses: list[str] = field(default_factory=lambda: ["linguistic_research"])
    access_restrictions: str | None = None
    is_withdrawn: bool = False
    withdrawal_date: str | None = None
    withdrawal_reason: str | None = None
    verification_status: str = "unverified"
    notes: str | None = None
    segments: list[AudioSegmentTimestamp] = field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        res = asdict(self)
        res["segments"] = [s.to_dict() for s in self.segments]
        return res

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioRecording:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        if isinstance(filtered.get("permitted_uses"), str):
            try:
                filtered["permitted_uses"] = json.loads(filtered["permitted_uses"])
            except Exception:
                filtered["permitted_uses"] = [filtered["permitted_uses"]]
        if isinstance(filtered.get("segments"), str):
            try:
                seg_list = json.loads(filtered["segments"])
                filtered["segments"] = [AudioSegmentTimestamp.from_dict(s) for s in seg_list]
            except Exception:
                filtered["segments"] = []
        elif isinstance(filtered.get("segments"), list):
            filtered["segments"] = [
                s if isinstance(s, AudioSegmentTimestamp) else AudioSegmentTimestamp.from_dict(s)
                for s in filtered["segments"]
            ]
        if "is_withdrawn" in filtered:
            filtered["is_withdrawn"] = bool(filtered["is_withdrawn"])
        return cls(**filtered)


@dataclass
class PronunciationRecord:
    """Represents a pronunciation variant linked to a vocabulary entry."""

    id: str
    vocab_entry_id: str
    headword: str
    recording_id: str | None = None
    pronunciation_ipa: str | None = None
    pronunciation_phonetic: str | None = None
    dialect: str | None = None
    village: str | None = None
    speaker_pseudonym: str | None = None
    is_primary: bool = False
    source_citation: str | None = None
    verification_status: str = "unverified"
    review_status: str = "pending_review"
    review_notes: str | None = None
    reviewer: str | None = None
    reviewed_at: str | None = None
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PronunciationRecord:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        if "is_primary" in filtered:
            filtered["is_primary"] = bool(filtered["is_primary"])
        return cls(**filtered)


@dataclass
class AudioAnnotation:
    """Fine-grained annotation, hypothesis, or transcription segment for an audio recording."""

    id: str
    recording_id: str
    annotation_type: str = "segment"
    start_time_seconds: float = 0.0
    end_time_seconds: float = 0.0
    text_verbatim: str = ""
    text_normalized: str = ""
    ipa: str | None = None
    annotator_pseudonym: str | None = None
    confidence_score: float | None = None
    verification_status: str = "unverified"
    notes: str | None = None
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioAnnotation:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class AudioConsentRecord:
    """Immutable audit record documenting speaker consent grant, condition, or withdrawal."""

    recording_id: str
    speaker_pseudonym: str
    consent_status: str
    id: int | None = None
    permitted_uses: list[str] = field(default_factory=list)
    restrictions: str | None = None
    recorded_date: str | None = None
    withdrawn_date: str | None = None
    withdrawn_reason: str | None = None
    authorized_by: str | None = None
    timestamp: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioConsentRecord:
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        if isinstance(filtered.get("permitted_uses"), str):
            try:
                filtered["permitted_uses"] = json.loads(filtered["permitted_uses"])
            except Exception:
                filtered["permitted_uses"] = []
        return cls(**filtered)


@dataclass
class AudioCorpusSummary:
    """Telemetry and status summary of the Tangkhul Audio Corpus."""

    total_recordings: int = 0
    authorized_count: int = 0
    pending_count: int = 0
    restricted_count: int = 0
    withdrawn_count: int = 0
    metadata_only_count: int = 0
    total_duration_seconds: float = 0.0
    formats_breakdown: dict[str, int] = field(default_factory=dict)
    dialect_breakdown: dict[str, int] = field(default_factory=dict)
    linked_vocab_count: int = 0
    verified_pronunciations_count: int = 0
