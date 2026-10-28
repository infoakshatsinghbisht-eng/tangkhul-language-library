"""Audio file validation, technical metadata extraction, and path security utilities."""

from __future__ import annotations

import hashlib
import os
import wave
from pathlib import Path
from typing import Any

from tangkhul_lib.audio.models import VALID_AUDIO_FORMATS


class AudioSecurityError(Exception):
    """Raised when an unsafe path, path traversal, or unpermitted file access is detected."""


class AudioValidationError(Exception):
    """Raised when an audio file fails technical format, header, or integrity checks."""


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing path separators and dangerous control characters."""
    clean = os.path.basename(filename.strip().replace("\\", "/"))
    clean = clean.replace("\0", "").replace("..", "")
    if not clean or clean in {".", ".."}:
        raise AudioSecurityError(f"Invalid or unsafe filename: '{filename}'")
    return clean


def safe_resolve_audio_path(base_dir: Path | str, target_path: Path | str) -> Path:
    """Resolve target path ensuring it resides strictly within base_dir.

    Raises:
        AudioSecurityError: If target path escapes base_dir via directory traversal.
    """
    base_resolved = Path(base_dir).resolve()
    target = Path(target_path)

    if not target.is_absolute():
        resolved = (base_resolved / target).resolve()
    else:
        resolved = target.resolve()

    try:
        # Check if resolved path is relative to base_resolved
        resolved.relative_to(base_resolved)
    except ValueError as err:
        raise AudioSecurityError(
            f"Path traversal detected: '{target_path}' escapes base directory '{base_dir}'."
        ) from err

    return resolved


def compute_file_sha256(file_path: Path | str, chunk_size: int = 65536) -> str:
    """Calculate the SHA-256 checksum of an audio file."""
    p = Path(file_path)
    if not p.is_file():
        raise FileNotFoundError(f"Audio file not found: '{file_path}'")

    hasher = hashlib.sha256()
    with p.open("rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def extract_audio_metadata(file_path: Path | str) -> dict[str, Any]:
    """Extract technical audio metadata (duration, sample rate, channels, size, format).

    Uses the standard library wave module for WAV files without external dependencies.
    Falls back gracefully to optional mutagen for compressed formats if available.

    Returns:
        dict containing:
            - file_format (str)
            - file_size_bytes (int)
            - duration_seconds (float)
            - sample_rate (int)
            - channels (int)
            - checksum_sha256 (str)
            - warnings (list[str])
    """
    p = Path(file_path)
    if not p.is_file():
        raise FileNotFoundError(f"Audio file not found: '{file_path}'")

    ext = p.suffix.lower().lstrip(".")
    if not ext or ext not in VALID_AUDIO_FORMATS:
        raise AudioValidationError(
            f"Unsupported audio format '{ext}'. Allowed formats: {sorted(VALID_AUDIO_FORMATS)}"
        )

    file_size = p.stat().st_size
    if file_size == 0:
        raise AudioValidationError(f"Audio file is empty (0 bytes): '{file_path}'")

    checksum = compute_file_sha256(p)
    duration = 0.0
    sample_rate = 0
    channels = 1
    warnings: list[str] = []

    if ext == "wav":
        try:
            with wave.open(str(p), "rb") as wf:
                channels = wf.getnchannels()
                sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                if sample_rate > 0:
                    duration = round(n_frames / float(sample_rate), 3)
        except wave.Error as err:
            raise AudioValidationError(f"Invalid or corrupt WAV audio header: {err}") from err
        except Exception as err:
            raise AudioValidationError(f"Failed to read WAV audio file: {err}") from err
    else:
        # Check for optional mutagen
        try:
            import mutagen  # type: ignore

            audio_info = mutagen.File(str(p))
            if audio_info is not None and audio_info.info is not None:
                duration = round(float(getattr(audio_info.info, "length", 0.0)), 3)
                sample_rate = int(getattr(audio_info.info, "sample_rate", 0))
                channels = int(getattr(audio_info.info, "channels", 1))
            else:
                warnings.append(
                    f"Format '{ext}' metadata could not be fully parsed by mutagen."
                )
        except ImportError:
            warnings.append(
                f"Optional dependency 'mutagen' is not installed. "
                f"Basic file metadata recorded for '{ext}'."
            )
        except Exception as err:
            warnings.append(f"Could not parse compressed audio tags: {err}")

    return {
        "file_format": ext,
        "file_size_bytes": file_size,
        "duration_seconds": duration,
        "sample_rate": sample_rate,
        "channels": channels,
        "checksum_sha256": checksum,
        "warnings": warnings,
    }
