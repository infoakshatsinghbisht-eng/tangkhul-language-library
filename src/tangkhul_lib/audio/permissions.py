"""Consent, copyright, and ethical access control for the Tangkhul Audio Corpus."""

from __future__ import annotations

import datetime
from typing import Any

from tangkhul_lib.audio.models import (
    VALID_AUDIO_PERMISSION_STATUSES,
    AudioConsentRecord,
    AudioRecording,
)


class AudioPermissionDeniedError(Exception):
    """Raised when an operation is attempted on restricted, pending, or withdrawn audio."""


class AudioPermissionService:
    """Evaluates consent, copyright clearance, and cultural privacy for audio recordings."""

    @staticmethod
    def current_iso_timestamp() -> str:
        """Return current UTC timestamp in ISO 8601 format."""
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    @classmethod
    def can_access_audio(cls, recording: AudioRecording) -> bool:
        """Check whether audio binary file can be accessed or played locally.

        Audio is accessible ONLY if consent is authorized, not withdrawn, and not restricted.
        """
        if recording.is_withdrawn:
            return False
        if recording.consent_status != "authorized":
            return False
        if recording.access_restrictions == "restricted":
            return False
        return True

    @classmethod
    def can_export(cls, recording: AudioRecording) -> bool:
        """Check whether recording is cleared for open or shared distribution.

        Strictly blocks withdrawn, pending, restricted, or needs_review recordings.
        """
        if recording.is_withdrawn:
            return False
        if recording.consent_status != "authorized":
            return False
        if recording.access_restrictions == "restricted":
            return False
        if recording.verification_status not in {"verified", "community_reviewed"}:
            # Must have passed validation
            return False
        return True

    @classmethod
    def withdraw_consent(
        cls,
        recording: AudioRecording,
        reason: str,
        date: str | None = None,
        authorized_by: str | None = None,
    ) -> tuple[AudioRecording, AudioConsentRecord]:
        """Withdraw consent for an audio recording, revoking all processing and export rights.

        Returns updated AudioRecording and an immutable AudioConsentRecord audit event.
        """
        now = cls.current_iso_timestamp()
        w_date = date or now

        recording.is_withdrawn = True
        recording.consent_status = "withdrawn"
        recording.withdrawal_date = w_date
        recording.withdrawal_reason = reason.strip()
        recording.updated_at = now

        consent_record = AudioConsentRecord(
            recording_id=recording.id,
            speaker_pseudonym=recording.speaker_pseudonym or "Anonymous",
            consent_status="withdrawn",
            permitted_uses=[],
            restrictions="Consent withdrawn by speaker or community custodian.",
            withdrawn_date=w_date,
            withdrawn_reason=reason.strip(),
            authorized_by=authorized_by,
            timestamp=now,
        )

        return recording, consent_record

    @classmethod
    def mask_recording_metadata(
        cls,
        recording: AudioRecording,
        is_privileged_view: bool = False,
    ) -> dict[str, Any]:
        """Return presentation dict with sensitive details masked if restricted or withdrawn."""
        data = recording.to_dict()

        if not is_privileged_view:
            if recording.is_withdrawn:
                data["file_path"] = "[WITHDRAWN - CONSENT REVOKED]"
                data["transcription"] = "[WITHDRAWN TRANSCRIPTION]"
                data["ipa_transcription"] = None
                data["transliteration"] = None
                data["speaker_pseudonym"] = "[SHIELDED SPEAKER]"
            elif (
                recording.consent_status != "authorized"
                or recording.access_restrictions == "restricted"
            ):
                data["file_path"] = "[RESTRICTED AUDIO FILE - ACCESS PRIVILEGED]"
                if recording.access_restrictions == "restricted":
                    data["transcription"] = "[RESTRICTED TEXT - SACRED/TABOO CONTENT]"
                    data["ipa_transcription"] = None
                    data["transliteration"] = None
                    data["speaker_pseudonym"] = "[SHIELDED SPEAKER]"

        return data

    @classmethod
    def validate_permission_tier(cls, status: str) -> str:
        """Validate permission status against valid set."""
        clean = status.strip().lower()
        if clean not in VALID_AUDIO_PERMISSION_STATUSES:
            raise ValueError(
                f"Invalid audio permission status '{status}'. "
                f"Allowed: {sorted(VALID_AUDIO_PERMISSION_STATUSES)}"
            )
        return clean
