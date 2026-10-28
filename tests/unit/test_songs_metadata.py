"""Unit tests for Tangkhul song metadata models and catalogue management."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import ManifestValidationError, ResourceNotFoundError
from tangkhul_lib.songs.catalogue import SongCatalogue
from tangkhul_lib.songs.models import SongRecord, SongRecording


def test_valid_song_record_creation() -> None:
    song = SongRecord(
        id="SNG-TRAD-001",
        title="Shimreishang Kala Maitonphi",
        alternate_titles=["Ashang Aton Laa"],
        title_translation="Ballad of Shimreishang and Maitonphi",
        singer="Traditional",
        village="Phungcham",
        dialect="Phungcham",
        song_type="ballad",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    song.validate()
    assert song.id == "SNG-TRAD-001"
    assert song.village == "Phungcham"
    assert song.song_type == "ballad"

    d = song.to_dict()
    assert d["id"] == "SNG-TRAD-001"
    assert d["resource_type"] == "songs"

    reconstructed = SongRecord.from_dict(d)
    assert reconstructed.id == song.id
    assert reconstructed.title == song.title


def test_song_record_validation_errors() -> None:
    # Empty ID
    with pytest.raises(ManifestValidationError, match="non-empty string"):
        SongRecord(id="", title="Title").validate()

    # Empty Title
    with pytest.raises(ManifestValidationError, match="missing or empty 'title'"):
        SongRecord(id="SNG-001", title="   ").validate()

    # Invalid permission status
    with pytest.raises(ManifestValidationError, match="Invalid permission_status"):
        SongRecord(
            id="SNG-001",
            title="Title",
            permission_status="invalid_permission",
        ).validate()

    # Invalid access status
    with pytest.raises(ManifestValidationError, match="Invalid access_status"):
        SongRecord(
            id="SNG-001",
            title="Title",
            access_status="invalid_access",
        ).validate()

    # Invalid verification status
    with pytest.raises(ManifestValidationError, match="Invalid verification_status"):
        SongRecord(
            id="SNG-001",
            title="Title",
            verification_status="invalid_verification",
        ).validate()


def test_song_recording_metadata() -> None:
    recording = SongRecording(
        recording_title="Oral Harvest Chant",
        source="Fieldwork Session 2018",
        performer="Village Elder",
        village="Phungcham",
        dialect="Phungcham",
        duration_seconds=184,
        media_format="wav",
        transcript_available=True,
    )
    d = recording.to_dict()
    assert d["duration_seconds"] == 184
    assert d["transcript_available"] is True
    assert d["performer"] == "Village Elder"


def test_song_manifest_conversion() -> None:
    song = SongRecord(
        id="SNG-MOD-001",
        title="Saharwon Kapaiwon",
        singer="Rewben Mashangva",
        composer="Rewben Mashangva",
        year=2005,
        village="Choithar",
        permission_status="pending",
        verification_status="verified",
    )
    manifest_rec = song.to_manifest_record()
    assert manifest_rec.id == "SNG-MOD-001"
    assert manifest_rec.resource_type == "songs"
    assert manifest_rec.creator == "Rewben Mashangva"
    assert manifest_rec.year == 2005


def test_catalogue_search_and_filters() -> None:
    s1 = SongRecord(
        id="SNG-1",
        title="Shimreishang Kala Maitonphi",
        singer="Traditional",
        village="Phungcham",
        song_type="ballad",
        verification_status="verified",
    )
    s2 = SongRecord(
        id="SNG-2",
        title="Made in Ukhrul",
        singer="Thangmeiso Shinglai",
        village="Ukhrul",
        song_type="modern",
        verification_status="verified",
    )
    s3 = SongRecord(
        id="SNG-3",
        title="Saharwon Kapaiwon",
        singer="Rewben Mashangva",
        village="Choithar",
        song_type="folk",
        verification_status="verified",
    )

    catalogue = SongCatalogue([s1, s2, s3])
    assert len(catalogue) == 3

    # Filter by singer
    res_singer = catalogue.search_songs(singer="Rewben")
    assert len(res_singer) == 1
    assert res_singer[0].id == "SNG-3"

    # Filter by song_type
    res_type = catalogue.search_songs(song_type="ballad")
    assert len(res_type) == 1
    assert res_type[0].id == "SNG-1"

    # Filter by village
    res_vil = catalogue.search_songs(village="Ukhrul")
    assert len(res_vil) == 1
    assert res_vil[0].id == "SNG-2"


def test_duplicate_detection_links_alternate_performances() -> None:
    s1 = SongRecord(
        id="SNG-TRAD-001",
        title="Shimreishang Kala Maitonphi",
        singer="Phungcham Troupe",
        village="Phungcham",
        year=1990,
    )
    s_alt = SongRecord(
        id="SNG-NEW-002",
        title="Shimreishang Kala Maitonphi",
        singer="Ukhrul Choir",
        village="Ukhrul",
        year=2015,
    )

    catalogue = SongCatalogue([s1])
    matches = catalogue.detect_duplicates(s_alt)
    assert len(matches) == 1
    # Differentiates alternate performance by different artist
    assert "Alternate performance" in matches[0][1]


def test_catalogue_export_and_manifest_load(tmp_path: Path) -> None:
    s1 = SongRecord(
        id="SNG-MOD-001",
        title="Saharwon Kapaiwon",
        singer="Rewben Mashangva",
        year=2005,
    )
    catalogue = SongCatalogue([s1])

    jsonl_out = tmp_path / "songs_export.jsonl"
    csv_out = tmp_path / "songs_export.csv"
    catalogue.export_catalogue(jsonl_out, format="jsonl")
    catalogue.export_catalogue(csv_out, format="csv")

    assert jsonl_out.is_file()
    assert csv_out.is_file()

    loaded = SongCatalogue.load_from_manifest(jsonl_out)
    assert len(loaded) == 1
    assert loaded.get_song("SNG-MOD-001").singer == "Rewben Mashangva"

    # Updating non-existent song
    with pytest.raises(ResourceNotFoundError):
        catalogue.update_song("NON_EXISTENT", {"notes": "abc"})
