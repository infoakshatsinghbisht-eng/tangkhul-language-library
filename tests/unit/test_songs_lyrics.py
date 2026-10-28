"""Unit tests for Tangkhul songs lyrics registry, stanzas, and CLI lyrics display."""

from __future__ import annotations

import pytest

from tangkhul_lib.cli import main
from tangkhul_lib.songs.lyrics_data import (
    SONGS_LYRICS_REGISTRY,
    get_song_lyrics,
    has_song_lyrics,
)


def test_lyrics_registry_completeness() -> None:
    """Verify that lyrics registry covers key songs with non-empty verses and translations."""
    assert len(SONGS_LYRICS_REGISTRY) >= 48

    for song_id, stanzas in SONGS_LYRICS_REGISTRY.items():
        assert len(stanzas) >= 1, f"Song {song_id} has no stanzas"
        for stanza in stanzas:
            assert "stanza_number" in stanza
            assert "lines_tangkhul" in stanza
            assert "lines_translation" in stanza
            assert len(stanza["lines_tangkhul"]) > 0, f"Empty Tangkhul lines in {song_id}"
            assert len(stanza["lines_translation"]) > 0, f"Empty translation lines in {song_id}"


def test_new_hymns_lyrics_content() -> None:
    """Test authentic Pettigrew 1907 hymns lyrics and translations."""
    # SNG-HIST-003: Jesus Loves Me (5 stanzas)
    hymn1 = get_song_lyrics("SNG-HIST-003")
    assert len(hymn1) == 5
    assert has_song_lyrics("SNG-HIST-003") is True
    assert "Ili Jesuna laishi" in hymn1[0]["lines_tangkhul"][0]
    assert "Jesus loves me" in hymn1[0]["lines_translation"][0]

    # SNG-HIST-004: Safe in the Arms of Jesus (2 stanzas)
    hymn2 = get_song_lyrics("SNG-HIST-004")
    assert len(hymn2) == 2
    assert "He Jesuwui makali" in hymn2[0]["lines_tangkhul"][0]

    # SNG-HIST-005: Stand Up for Jesus (3 stanzas)
    hymn3 = get_song_lyrics("SNG-HIST-005")
    assert len(hymn3) == 3
    assert "Jesuwui vang nganinglu" in hymn3[0]["lines_tangkhul"][0]

    # SNG-HIST-006: Take the Name of Jesus (4 stanzas)
    hymn4 = get_song_lyrics("SNG-HIST-006")
    assert len(hymn4) == 4
    assert "Jesuwui aming ngasoda" in hymn4[0]["lines_tangkhul"][0]


def test_batch2_hymns_lyrics_content() -> None:
    """Test Batch 2 Pettigrew 1907 historical hymns stanzas and translations."""
    # SNG-HIST-007: Jesus the Very Thought of Thee (5 stanzas)
    h7 = get_song_lyrics("SNG-HIST-007")
    assert len(h7) == 5
    assert "Jesu nawui ming phaningda" in h7[0]["lines_tangkhul"][0]

    # SNG-HIST-008: Beneath the Cross of Jesus (4 stanzas)
    h8 = get_song_lyrics("SNG-HIST-008")
    assert len(h8) == 4
    assert "Jesuwui krushwui pamli" in h8[0]["lines_tangkhul"][0]

    # SNG-HIST-009: Now the Day Is Over (7 stanzas)
    h9 = get_song_lyrics("SNG-HIST-009")
    assert len(h9) == 7
    assert "Arui chimik tunra" in h9[0]["lines_tangkhul"][0]

    # SNG-HIST-010: Onward, Christian Soldiers (5 stanzas)
    h10 = get_song_lyrics("SNG-HIST-010")
    assert len(h10) == 5
    assert "Jesuwui mi chatsa" in h10[0]["lines_tangkhul"][0]

    # SNG-HIST-011: Blessed Assurance (3 stanzas)
    h11 = get_song_lyrics("SNG-HIST-011")
    assert len(h11) == 3
    assert "Ringkapha tui Jesu Amai!" in h11[0]["lines_tangkhul"][0]

    # SNG-HIST-012: Abide with Me (6 stanzas)
    h12 = get_song_lyrics("SNG-HIST-012")
    assert len(h12) == 6
    assert "Arui ngayali ili ngachonlu" in h12[0]["lines_tangkhul"][0]

    # SNG-HIST-013: Jesus, Lover of My Soul (4 stanzas)
    h13 = get_song_lyrics("SNG-HIST-013")
    assert len(h13) == 4
    assert "Jesuna ili laishi" in h13[0]["lines_tangkhul"][0]

    # SNG-HIST-014: Rock of Ages (4 stanzas)
    h14 = get_song_lyrics("SNG-HIST-014")
    assert len(h14) == 4
    assert "Makashiman lungkhuri" in h14[0]["lines_tangkhul"][0]


def test_new_traditional_songs_lyrics_content() -> None:
    """Test traditional Tangkhul songs lyrics and translations."""
    # SNG-TRAD-008: Itang Rakhongli (3 stanzas)
    sng8 = get_song_lyrics("SNG-TRAD-008")
    assert len(sng8) == 3
    assert "Itang rakhongli" in sng8[0]["lines_tangkhul"][0]

    # SNG-TRAD-009: Yarra Laa (3 stanzas)
    sng9 = get_song_lyrics("SNG-TRAD-009")
    assert len(sng9) == 3
    assert "Yarra phanit" in sng9[0]["lines_tangkhul"][0]

    # SNG-TRAD-010: Mangkhap Laa (3 stanzas)
    sng10 = get_song_lyrics("SNG-TRAD-010")
    assert len(sng10) == 3
    assert "Mangkhap phanitli" in sng10[0]["lines_tangkhul"][0]

    # SNG-TRAD-011: Hao Pheichak Laa (3 stanzas)
    sng11 = get_song_lyrics("SNG-TRAD-011")
    assert len(sng11) == 3
    assert "Hao pheichakli" in sng11[0]["lines_tangkhul"][0]


def test_cli_song_lyrics_flag(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI --id with --lyrics displays stanzas and translations."""
    code = main(["songs", "--id", "SNG-HIST-003", "--lyrics"])
    assert code == 0
    out = capsys.readouterr().out
    assert "LYRICS & TRANSLATIONS (5 stanza(s)):" in out
    assert "Ili Jesuna laishi" in out
    assert "Jesus loves me" in out


def test_fallback_song_lyrics() -> None:
    """Test fallback stanza for an unknown song ID."""
    assert has_song_lyrics("UNKNOWN-SONG-ID") is False
    fallback = get_song_lyrics("UNKNOWN-SONG-ID")
    assert len(fallback) == 1
    assert "Iram kaphungli" in fallback[0]["lines_tangkhul"][0]
