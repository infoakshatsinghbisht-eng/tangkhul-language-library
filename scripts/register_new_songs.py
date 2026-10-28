#!/usr/bin/env python3
"""Register newly discovered and digitized Tangkhul songs in manifest and SQLite database."""

from __future__ import annotations

import json
from pathlib import Path

from tangkhul_lib.songs.extractor import SongLyricsExtractor
from tangkhul_lib.songs.models import SongRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import ManifestRepository, SongRepository

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = ROOT / "data" / "manifests" / "songs.jsonl"
DB_FILE = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_FILE = ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"

NEW_SONGS_METADATA = [
    {
        "id": "SNG-HIST-003",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 1: Ili Jesuna Laishi",
        "alternate_titles": ["Jesus Loves Me (Tangkhul)", "Hymn No. 1 (1907)"],
        "title_translation": "Jesus Loves Me in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Anna Bartlett Warner (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "William B. Bradbury (Tune 1155 | Doh is E)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-001",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-003_jesuwui_laa_01_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Hymn No. 1 from Jesuwui La: Hymns in Tangkhul Naga (1907, American Baptist Mission, Ukhrul). "
            "5 stanzas translated by Rev. William Pettigrew from the original hymn 'Jesus Loves Me'."
        ),
    },
    {
        "id": "SNG-HIST-004",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 2: He Jesuwui Makali Ringphalaka",
        "alternate_titles": ["Safe in the Arms of Jesus (Tangkhul)", "Hymn No. 2 (1907)"],
        "title_translation": "Safe in the Arms of Jesus in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Fanny Crosby (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "William H. Doane (Tune 57 | Doh is G)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-002",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-004_jesuwui_laa_02_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Hymn No. 2 from Jesuwui La: Hymns in Tangkhul Naga (1907, American Baptist Mission, Ukhrul). "
            "2 stanzas translated into classical archaic Tangkhul orthography."
        ),
    },
    {
        "id": "SNG-HIST-005",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 3: Jesuwui Vang Nganinglu",
        "alternate_titles": ["Stand Up, Stand Up for Jesus (Tangkhul)", "Hymn No. 3 (1907)"],
        "title_translation": "Stand Up, Stand Up for Jesus in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "George Duffield Jr. (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "George J. Webb (Tune 680 | Doh is Bb)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-003",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-005_jesuwui_laa_03_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Hymn No. 3 from Jesuwui La: Hymns in Tangkhul Naga (1907). "
            "3 stanzas translated by Rev. William Pettigrew celebrating moral steadfastness."
        ),
    },
    {
        "id": "SNG-HIST-006",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 4: Jesuwui Aming Ngasoda",
        "alternate_titles": ["Take the Name of Jesus with You (Tangkhul)", "Hymn No. 4 (1907)"],
        "title_translation": "Take the Name of Jesus with You in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Lydia Baxter (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "William H. Doane (Tune 91 | Doh is Ab)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-004",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-006_jesuwui_laa_04_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Hymn No. 4 from Jesuwui La: Hymns in Tangkhul Naga (1907). "
            "4 complete stanzas on spiritual comfort and peace."
        ),
    },
    {
        "id": "SNG-TRAD-008",
        "resource_type": "songs",
        "title": "Itang Rakhongli",
        "alternate_titles": ["Rakhong Laa", "Song of the Riverbank and Beloved Hills"],
        "title_translation": "Song of the Riverbank and Beloved Hills",
        "singer": "Traditional Tangkhul Troupe",
        "lyricist": None,
        "composer": None,
        "collector": "Tangkhul Literature Society / Traditional Elders",
        "performers": [],
        "year": 1985,
        "village": "Hunphun",
        "dialect": "Hunphun / Standard Tangkhul",
        "song_type": "love_song",
        "language": "Tangkhul",
        "source_url": "https://tangkhullaa.com/itang-rakhongli",
        "source_identifier": "TRAD-HUN-001",
        "recording_url": None,
        "lyrics_source_url": "https://tangkhullaa.com/itang-rakhongli",
        "local_file_path": "data/raw/songs/SNG-TRAD-008_itang_rakhongli.txt",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Classic Tangkhul lyrical love song expressing yearning across mountain ranges, "
            "invoking the hills to lower their peaks that one may gaze upon beloved homeland."
        ),
    },
    {
        "id": "SNG-TRAD-009",
        "resource_type": "songs",
        "title": "Yarra Laa: Yarshungwon",
        "alternate_titles": ["Yarra Festival Youth Song", "Spring Awakening Chant"],
        "title_translation": "Youth Spring Awakening and Courting Chant",
        "singer": "Traditional Youth Dormitory Chorus",
        "lyricist": None,
        "composer": None,
        "collector": "Dr. Ringkahao Horam / Tribal Research Institute",
        "performers": [],
        "year": 1987,
        "village": "Hungpung",
        "dialect": "Hungpung / Standard Tangkhul",
        "song_type": "festival",
        "language": "Tangkhul",
        "source_url": "https://sanchika.ciil.org/collections/tangkhul-haola",
        "source_identifier": "CIIL-YARRA-001",
        "recording_url": None,
        "lyrics_source_url": None,
        "local_file_path": "data/raw/songs/SNG-TRAD-009_yarra_laa.txt",
        "license": "Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Traditional youth spring festival chant performed during Yarra Phanit, "
            "celebrating spring blossom and mutual courting in the traditional dormitory."
        ),
    },
    {
        "id": "SNG-TRAD-010",
        "resource_type": "songs",
        "title": "Mangkhap Laa: Ngaphit Kazang",
        "alternate_titles": ["Post-Transplantation Feast Chant", "Mangkhap Rest Song"],
        "title_translation": "Paddy Transplantation Completion and Thanksgiving",
        "singer": "Phungcham Agricultural Elders",
        "lyricist": None,
        "composer": None,
        "collector": "Tangkhul Literature Society",
        "performers": [],
        "year": 1992,
        "village": "Phungcham",
        "dialect": "Phungcham Dialect",
        "song_type": "festival",
        "language": "Tangkhul",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-MANGKHAP-001",
        "recording_url": None,
        "lyrics_source_url": None,
        "local_file_path": "data/raw/songs/SNG-TRAD-010_mangkhap_laa.txt",
        "license": "Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Traditional agricultural chant sung at the culmination of rice transplantation during "
            "Mangkhap Phanit, expressing thanksgiving for communal labor."
        ),
    },
    {
        "id": "SNG-TRAD-011",
        "resource_type": "songs",
        "title": "Hao Pheichak Laa",
        "alternate_titles": ["Warrior and Festival Dance Chant", "Tangkhul Antiphonal Dance Song"],
        "title_translation": "Traditional Dance and Warrior Chant",
        "singer": "Longpi Traditional Troupe",
        "lyricist": None,
        "composer": None,
        "collector": "H. Kamkhenthang / Directorate of Tribals Manipur",
        "performers": [],
        "year": 1989,
        "village": "Longpi",
        "dialect": "Longpi Dialect",
        "song_type": "ceremonial",
        "language": "Tangkhul",
        "source_url": "https://sanchika.ciil.org/collections/tangkhul-dance",
        "source_identifier": "TRI-MANIPUR-PHEICHAK-001",
        "recording_url": None,
        "lyrics_source_url": None,
        "local_file_path": "data/raw/songs/SNG-TRAD-011_hao_pheichak_laa.txt",
        "license": "Cultural Heritage",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Antiphonal ceremonial warrior and celebration dance chant performed during major "
            "public gatherings and festival dances (Pheichak)."
        ),
    },
]


def register_songs() -> None:
    # 1. Update data/manifests/songs.jsonl
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        existing_lines = [line.strip() for line in f if line.strip()]

    existing_ids = {json.loads(line)["id"] for line in existing_lines}
    added_to_manifest = 0

    with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
        for s_data in NEW_SONGS_METADATA:
            if s_data["id"] not in existing_ids:
                f.write(json.dumps(s_data, ensure_ascii=False) + "\n")
                existing_ids.add(s_data["id"])
                added_to_manifest += 1

    print(f"Manifest update: Added {added_to_manifest} songs. Total in {MANIFEST_FILE}: {len(existing_ids)}")

    # 2. Update SQLite databases
    extractor = SongLyricsExtractor()

    for db_path in [DB_FILE, BUNDLED_DB_FILE]:
        if not db_path.exists():
            continue
        db_mgr = DatabaseManager(db_path)
        song_repo = SongRepository(db_mgr)
        manifest_repo = ManifestRepository(db_mgr)

        for s_data in NEW_SONGS_METADATA:
            song = SongRecord.from_dict(s_data)
            # Add or update in songs table
            if not song_repo.get_by_id(song.id):
                song_repo.add(song)
            else:
                song_repo.update(song.id, s_data)

            # Sync manifest
            m_rec = song.to_manifest_record()
            if not manifest_repo.get_by_id(m_rec.id):
                manifest_repo.add(m_rec)

            # Extract tokens if raw file exists
            if song.local_file_path:
                raw_path = ROOT / song.local_file_path
                if raw_path.exists():
                    raw_lines = extractor.parse_lyrics_text(raw_path.read_text(encoding="utf-8"))
                    raw_tokens, _ = extractor.extract_vocabulary_candidates(song, raw_lines)
                    song_repo.save_tokens(song.id, raw_tokens)

        print(f"Database sync ({db_path}): Total songs in repo: {song_repo.count()}")


if __name__ == "__main__":
    register_songs()
