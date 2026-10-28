#!/usr/bin/env python3
"""Fix placement of SNG-HIST-007 through SNG-HIST-014 in lyrics_data.py."""

from pathlib import Path

TARGET = Path("src/tangkhul_lib/songs/lyrics_data.py")


def main():
    with open(TARGET, encoding="utf-8") as f:
        lines = f.readlines()

    # Find where SNG-HIST-007 starts
    idx_start = -1
    for i, line in enumerate(lines):
        if line.strip() == '"SNG-HIST-007": [':
            idx_start = i
            break

    # Find where SNG-HIST-014 ends
    idx_end = -1
    for i in range(idx_start, len(lines)):
        if lines[i].strip() == '"lines_translation": [' and "Take the name of Jesus" in lines[i + 1]:
            idx_end = i
            break

    print(f"SNG-HIST-007 starts at line {idx_start + 1}, ends before line {idx_end + 1}")
    batch2_block = lines[idx_start:idx_end]

    # Clean out batch2_block from inside SNG-HIST-006
    cleaned_lines = lines[:idx_start] + lines[idx_end:]

    # Find true end of SNG-HIST-006
    sng006_end = -1
    for i, line in enumerate(cleaned_lines):
        if "King of kings in heaven" in line:
            for k in range(i, i + 10):
                if cleaned_lines[k].strip() == "],":
                    sng006_end = k + 1
                    break
            break

    print(f"SNG-HIST-006 ends at line {sng006_end}")
    final_lines = cleaned_lines[:sng006_end] + batch2_block + cleaned_lines[sng006_end:]

    with open(TARGET, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print("Fixed lyrics_data.py!")


if __name__ == "__main__":
    main()
