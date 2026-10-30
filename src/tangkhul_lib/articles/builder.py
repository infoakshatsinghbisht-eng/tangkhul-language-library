"""Builder and PDF generator for digitized Tangkhul research articles."""

from __future__ import annotations

from typing import Any


def sanitize_pdf_text(text: str) -> str:
    """Sanitize and encode string for PDF Type 1 Helvetica font (Latin-1)."""
    replacements = {
        "—": "--",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "*",
        "ā": "a",
        "ē": "e",
        "ī": "i",
        "ō": "o",
        "ū": "u",
        "Ā": "A",
        "Ē": "E",
        "Ī": "I",
        "Ō": "O",
        "Ū": "U",
        "ə": "e",
        "ŋ": "ng",
        "ʰ": "h",
        "ʔ": "'",
        "ʂ": "sh",
        "á": "a",
        "à": "a",
        "í": "i",
        "ì": "i",
        "ú": "u",
        "ù": "u",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return escaped.encode("latin-1", "replace").decode("latin-1")


def build_pdf_document(pages_content: list[list[tuple[str, int, str]]]) -> bytes:
    """Build a multi-page PDF 1.4 document from structured lines."""
    cat_id = 1
    pages_root_id = 2
    f1_id = 3
    f2_id = 4

    cur_id = 5
    page_entries: list[tuple[int, int, bytes]] = []
    page_obj_ids: list[int] = []

    for page_items in pages_content:
        p_id = cur_id
        cur_id += 1
        c_id = cur_id
        cur_id += 1

        stream_cmds = ["BT"]
        y = 780
        stream_cmds.append(f"50 {y} Td")
        current_y = y

        for font, size, line in page_items:
            clean = sanitize_pdf_text(line)
            stream_cmds.append(f"{font} {size} Tf")
            stream_cmds.append(f"({clean}) Tj")
            dy = -(size + 4)
            stream_cmds.append(f"0 {dy} Td")
            current_y += dy
            if current_y < 45:
                break

        stream_cmds.append("ET")
        c_stream = "\n".join(stream_cmds).encode("latin-1", "replace")
        page_entries.append((p_id, c_id, c_stream))
        page_obj_ids.append(p_id)

    obj_dict: dict[int, bytes] = {}
    obj_dict[cat_id] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids_str = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    obj_dict[pages_root_id] = (
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>".encode("latin-1")
    )
    obj_dict[f1_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    obj_dict[f2_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"

    for pid, cid, cstream in page_entries:
        obj_dict[pid] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {cid} 0 R >>"
        ).encode("latin-1")
        obj_dict[cid] = (
            f"<< /Length {len(cstream)} >>\nstream\n".encode("latin-1")
            + cstream
            + b"\nendstream"
        )

    out = bytearray()
    out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: dict[int, int] = {}
    total_objs = max(obj_dict.keys())

    for oid in sorted(obj_dict.keys()):
        offsets[oid] = len(out)
        out.extend(f"{oid} 0 obj\n".encode("latin-1"))
        out.extend(obj_dict[oid])
        out.extend(b"\nendobj\n")

    xref_offset = len(out)
    out.extend(f"xref\n0 {total_objs + 1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for oid in range(1, total_objs + 1):
        if oid in offsets:
            out.extend(f"{offsets[oid]:010d} 00000 n \n".encode("latin-1"))
        else:
            out.extend(b"0000000000 00000 f \n")

    out.extend(
        f"trailer\n<< /Size {total_objs + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("latin-1")
    )
    return bytes(out)


def generate_article_pdf(article_data: dict[str, Any]) -> bytes:
    """Generate multi-page PDF bytes for a single article."""
    pages = article_data.get("pages", [])
    pages_content = [p.get("lines", []) for p in pages]
    return build_pdf_document(pages_content)
