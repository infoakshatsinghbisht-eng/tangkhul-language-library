"""Unit tests for lyrics extraction, permission enforcement, and vocabulary candidates."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import PermissionRestrictedError, ResourceNotFoundError
from tangkhul_lib.songs.extractor import SongLyricsExtractor
from tangkhul_lib.songs.models import SongRecord


def test_lyrics_parsing_into_stanzas_and_lines() -> None:
    text = """
    Shimreishangwui ningli leikashi lei.
    Atonphi kachihi ramwui won kapha.

    Iram Phungchamli ningkachon pamei.
    Chitharan leikashi thot khangatei lei.
    """
    extractor = SongLyricsExtractor()
    parsed = extractor.parse_lyrics_text(text)
    assert len(parsed) == 4
    # Stanza 1, Line 1
    assert parsed[0] == (1, 1, "Shimreishangwui ningli leikashi lei.")
    # Stanza 1, Line 2
    assert parsed[1] == (1, 2, "Atonphi kachihi ramwui won kapha.")
    # Stanza 2, Line 1
    assert parsed[2] == (2, 1, "Iram Phungchamli ningkachon pamei.")
    # Stanza 2, Line 2
    assert parsed[3] == (2, 2, "Chitharan leikashi thot khangatei lei.")


def test_lyrics_file_missing_and_permissions(tmp_path: Path) -> None:
    extractor = SongLyricsExtractor()
    song = SongRecord(
        id="SNG-001",
        title="Test Song",
        permission_status="permitted",
        access_status="full_text_available",
    )
    with pytest.raises(ResourceNotFoundError):
        extractor.extract_lyrics_file(song, file_path=tmp_path / "missing.txt")

    # Restricted song
    lyrics_file = tmp_path / "lyrics.txt"
    lyrics_file.write_text("Secret protected lyrics.", encoding="utf-8")
    restricted_song = SongRecord(
        id="SNG-RES",
        title="Restricted Song",
        local_file_path=str(lyrics_file),
        permission_status="restricted",
        access_status="restricted",
    )
    with pytest.raises(PermissionRestrictedError, match="not permitted"):
        extractor.extract_lyrics_file(restricted_song)


def test_lyrics_vocabulary_candidate_generation() -> None:
    song = SongRecord(
        id="SNG-TRAD-001",
        title="Shimreishang Kala Maitonphi",
        singer="Phungcham Village Troupe",
        year=1990,
        village="Phungcham",
        permission_status="public_domain",
        access_status="full_text_available",
    )
    lyrics = [
        (1, 1, "Shimreishangwui ningli leikashi lei."),
        (1, 2, "Atonphi kachihi ramwui won kapha."),
    ]

    extractor = SongLyricsExtractor()
    raw_tokens, candidates = extractor.extract_vocabulary_candidates(song, lyrics)

    assert len(raw_tokens) > 0
    assert len(candidates) > 0

    # Ensure unverified status and no fabricated translations
    for entry in candidates:
        assert entry.verification_status == "unverified"
        assert entry.meanings == []
        assert entry.translations_en == []
        assert len(entry.provenance) >= 1
        prov = entry.provenance[0]
        assert prov.source_id == "SNG-TRAD-001"
        assert prov.resource_type == "songs"
        assert "Stanza 1, Line" in (prov.page_or_section or "")

    # Check that headwords like 'leikashi' or 'ramwui' exist
    headwords = {c.headword.lower() for c in candidates}
    assert "leikashi" in headwords or "atonphi" in headwords or "shimreishangwui" in headwords
