#!/usr/bin/env python3
"""Update src/tangkhul_lib/songs/lyrics_data.py with Batch 2 historical hymns."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.batch2_ingest_songs import BATCH2_SONGS

TARGET_FILE = ROOT / "src" / "tangkhul_lib" / "songs" / "lyrics_data.py"


def main():
    content = TARGET_FILE.read_text(encoding="utf-8")

    if '"SNG-HIST-007"' in content:
        print("SNG-HIST-007 is already present in lyrics_data.py")
        return

    # Build the python snippet for the 8 songs
    new_entries = []
    for song in BATCH2_SONGS:
        sid = song["id"]
        stanzas = song["stanzas"]
        entry = f'    "{sid}": [\n'
        for st in stanzas:
            entry += "        {\n"
            entry += f'            "stanza_number": {st["stanza_number"]},\n'
            entry += '            "lines_tangkhul": [\n'
            for line in st["lines_tangkhul"]:
                # Escape any inner quotes if needed
                clean_line = line.replace('"', '\\"')
                entry += f'                "{clean_line}",\n'
            entry += "            ],\n"
            entry += '            "lines_translation": [\n'
            for line in st["lines_translation"]:
                clean_line = line.replace('"', '\\"')
                entry += f'                "{clean_line}",\n'
            entry += "            ],\n"
            entry += "        },\n"
        entry += "    ],\n"
        new_entries.append(entry)

    insert_text = "".join(new_entries)

    # Insert right after SNG-HIST-006:
    pattern = r'(\s+"SNG-HIST-006":\s+\[[\s\S]*?\n\s+\]),\n'
    match = re.search(pattern, content)
    if not match:
        raise ValueError("Could not find SNG-HIST-006 in lyrics_data.py")

    pos = match.end()
    new_content = content[:pos] + insert_text + content[pos:]
    TARGET_FILE.write_text(new_content, encoding="utf-8")
    print("Successfully updated src/tangkhul_lib/songs/lyrics_data.py!")


if __name__ == "__main__":
    main()
