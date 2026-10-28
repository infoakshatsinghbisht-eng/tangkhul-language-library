"""Songs domain module for Tangkhul Language Library.

Provides cataloguing, musical metadata management, duplicate detection, lyrics processing,
and provenance-preserving vocabulary candidate generation for Tangkhul songs.
"""

from __future__ import annotations

from tangkhul_lib.songs.catalogue import SongCatalogue
from tangkhul_lib.songs.extractor import SongLyricsExtractor
from tangkhul_lib.songs.lyrics_data import get_song_lyrics, has_song_lyrics
from tangkhul_lib.songs.models import SongRecord, SongRecording
from tangkhul_lib.storage.repositories import SongRepository

MODULE_NAME = "songs"

__all__ = [
    "MODULE_NAME",
    "SongCatalogue",
    "SongLyricsExtractor",
    "SongRecord",
    "SongRecording",
    "SongRepository",
    "get_song_lyrics",
    "has_song_lyrics",
]
