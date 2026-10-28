"""Text extraction interfaces and document processors for Tangkhul Language Library."""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from tangkhul_lib.core.exceptions import ResourceNotFoundError
from tangkhul_lib.core.models import DocumentChunk
from tangkhul_lib.vocabulary.normalization import normalize_unicode, sanitize_spacing


def compute_file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a local file."""
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class ExtractedPage:
    """Represents text extracted from a specific page or section of a document."""

    page_number: int | None
    text: str
    section_title: str | None = None

    @property
    def char_count(self) -> int:
        return len(self.text)

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def is_empty(self) -> bool:
        return not bool(self.text.strip())

    @property
    def replacement_char_count(self) -> int:
        return self.text.count("\ufffd")


@dataclass
class ExtractionResult:
    """Complete result of a document text extraction process."""

    source_id: str
    file_path: Path
    pages: list[ExtractedPage] = field(default_factory=list)
    full_text: str = ""
    extraction_method: str = "text_utf8"
    status: str = "extracted"  # 'extracted', 'partial', 'needs_review', 'empty', 'failed'
    notes: str | None = None
    warnings: list[str] = field(default_factory=list)
    file_hash: str = ""
    file_size_bytes: int = 0
    ocr_status: str = "not_required"  # 'not_required', 'ocr_needed', 'ocr_completed'

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def char_count(self) -> int:
        return sum(p.char_count for p in self.pages)

    @property
    def word_count(self) -> int:
        return sum(p.word_count for p in self.pages)


def assess_extraction_quality(
    pages: list[ExtractedPage],
    file_format: str,
) -> tuple[str, list[str], str]:
    """Assess extraction quality, returning (status, warnings, ocr_status)."""
    warnings: list[str] = []
    ocr_status = "not_required"

    total_pages = len(pages)
    if total_pages == 0:
        return "empty", ["Document contains zero pages."], "not_required"

    empty_pages = [p.page_number for p in pages if p.is_empty and p.page_number is not None]
    total_chars = sum(p.char_count for p in pages)
    total_replacements = sum(p.replacement_char_count for p in pages)

    if len(empty_pages) == total_pages:
        if file_format.lower() in {"pdf", "png", "jpg", "jpeg", "tiff", "tif"}:
            warnings.append("Document has no extractable digital text layer; OCR is required.")
            return "needs_review", warnings, "ocr_needed"
        return "empty", ["Document contains only whitespace or empty text."], "not_required"

    if empty_pages:
        pct_empty = (len(empty_pages) / total_pages) * 100
        warnings.append(
            f"Document contains {len(empty_pages)} of {total_pages} empty page(s) "
            f"({pct_empty:.1f}%)."
        )

    if total_replacements > 0:
        warnings.append(
            f"Detected {total_replacements} Unicode replacement character(s) (\\ufffd); "
            "possible encoding or font-mapping corruption."
        )

    valid_pages = total_pages - len(empty_pages)
    avg_chars = total_chars / valid_pages if valid_pages > 0 else 0
    if file_format.lower() == "pdf" and avg_chars < 30:
        warnings.append(
            f"Very low character density detected (avg {avg_chars:.1f} chars/page); "
            "document may contain un-OCR'd scanned page plates."
        )
        ocr_status = "ocr_needed"

    status = "partial" if empty_pages and len(empty_pages) < total_pages else "extracted"
    return status, warnings, ocr_status


class BaseOcrAdapter:
    """Pluggable OCR interface for processing scanned pages and plates."""

    def is_available(self) -> bool:
        """Return True if the underlying OCR engine is installed and operational."""
        return False

    def extract_text(self, file_path: Path) -> list[ExtractedPage]:
        """Extract text from scanned pages using OCR engine."""
        raise NotImplementedError("OCR adapter not implemented")


class NoOpOcrAdapter(BaseOcrAdapter):
    """Default fallback when no OCR engine is available."""

    def is_available(self) -> bool:
        return False

    def extract_text(self, file_path: Path) -> list[ExtractedPage]:
        return []


class TextExtractor:
    """Extracts text content and page structures from permitted documents."""

    def __init__(self, ocr_adapter: BaseOcrAdapter | None = None) -> None:
        self.ocr_adapter = ocr_adapter or NoOpOcrAdapter()

    def extract_from_text(
        self,
        raw_text: str,
        source_id: str = "",
        file_path: Path | None = None,
    ) -> ExtractionResult:
        """Extract pages from a plain text string, identifying page markers if present."""
        path = file_path or Path("<in-memory-text>")
        normalized = normalize_unicode(raw_text)

        page_pattern = re.compile(
            r"(?:^|\n)[ \t]*(?:[-=]{3,}\s*Page\s+(\d+)\s*[-=]{3,}|\[Page\s+(\d+)\])",
            re.IGNORECASE,
        )

        matches = list(page_pattern.finditer(normalized))
        pages: list[ExtractedPage] = []

        if not matches:
            pages.append(ExtractedPage(page_number=1, text=normalized.strip()))
        else:
            first_m = matches[0]
            preamble = normalized[: first_m.start()].strip()
            if preamble:
                pages.append(
                    ExtractedPage(page_number=None, text=preamble, section_title="Front Matter")
                )

            for idx, m in enumerate(matches):
                page_num_str = m.group(1) or m.group(2)
                page_num = int(page_num_str) if page_num_str else (idx + 1)
                start_pos = m.end()
                end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(normalized)
                page_text = normalized[start_pos:end_pos].strip()
                pages.append(ExtractedPage(page_number=page_num, text=page_text))

        full_text = "\n\n".join(p.text for p in pages if p.text)
        status, warnings, ocr_status = assess_extraction_quality(pages, "txt")

        return ExtractionResult(
            source_id=source_id,
            file_path=path,
            pages=pages,
            full_text=full_text,
            extraction_method="text_utf8",
            status=status,
            warnings=warnings,
            ocr_status=ocr_status,
        )

    def extract_from_txt_file(
        self,
        file_path: Path,
        source_id: str = "",
    ) -> ExtractionResult:
        """Extract text from a UTF-8 encoded text or Markdown file."""
        path = Path(file_path)
        if not path.is_file():
            raise ResourceNotFoundError(f"File not found: {path}")

        file_hash = compute_file_hash(path)
        file_size = path.stat().st_size
        warnings: list[str] = []

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="latin-1")
            warnings.append("File contains non-UTF-8 bytes; decoded using latin-1 fallback.")

        res = self.extract_from_text(content, source_id=source_id, file_path=path)
        res.file_hash = file_hash
        res.file_size_bytes = file_size
        res.warnings.extend(warnings)
        return res

    def extract_from_pdf_file(
        self,
        file_path: Path,
        source_id: str = "",
    ) -> ExtractionResult:
        """Extract text page by page from a text-based PDF document."""
        path = Path(file_path)
        if not path.is_file():
            raise ResourceNotFoundError(f"PDF file not found: {path}")

        file_hash = compute_file_hash(path)
        file_size = path.stat().st_size

        try:
            import pypdf
        except ImportError:
            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=[],
                full_text="",
                extraction_method="pdf_pypdf_unavailable",
                status="needs_review",
                notes="pypdf package is not installed; digital PDF extraction unavailable.",
                file_hash=file_hash,
                file_size_bytes=file_size,
            )

        try:
            reader = pypdf.PdfReader(str(path))
            if reader.is_encrypted:
                # Attempt empty password decryption
                try:
                    decrypted = reader.decrypt("")
                    if decrypted == 0:
                        return ExtractionResult(
                            source_id=source_id,
                            file_path=path,
                            pages=[],
                            full_text="",
                            extraction_method="pdf_pypdf",
                            status="failed",
                            notes="PDF is password-encrypted and cannot be decrypted without key.",
                            warnings=["PDF is password-encrypted."],
                            file_hash=file_hash,
                            file_size_bytes=file_size,
                        )
                except Exception as dec_err:
                    return ExtractionResult(
                        source_id=source_id,
                        file_path=path,
                        pages=[],
                        full_text="",
                        extraction_method="pdf_pypdf",
                        status="failed",
                        notes=f"Encrypted PDF decryption failed: {dec_err}",
                        warnings=["Encrypted PDF decryption failed."],
                        file_hash=file_hash,
                        file_size_bytes=file_size,
                    )

            pages: list[ExtractedPage] = []
            page_warnings: list[str] = []

            for idx, page in enumerate(reader.pages, start=1):
                try:
                    raw_page_text = page.extract_text() or ""
                    clean_page_text = normalize_unicode(raw_page_text)
                    pages.append(ExtractedPage(page_number=idx, text=clean_page_text))
                except Exception as p_err:
                    pages.append(ExtractedPage(page_number=idx, text=""))
                    page_warnings.append(f"Page {idx} extraction failed: {p_err}")

            full_text = "\n\n".join(p.text for p in pages if p.text)
            status, warnings, ocr_status = assess_extraction_quality(pages, "pdf")
            warnings.extend(page_warnings)

            notes = None
            if ocr_status == "ocr_needed":
                notes = "PDF has no digital text layer or very low text volume; OCR required."

            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=pages,
                full_text=full_text,
                extraction_method="pdf_pypdf",
                status=status,
                notes=notes,
                warnings=warnings,
                file_hash=file_hash,
                file_size_bytes=file_size,
                ocr_status=ocr_status,
            )
        except Exception as exc:
            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=[],
                full_text="",
                extraction_method="pdf_pypdf",
                status="failed",
                notes=f"PDF parsing error: {exc}",
                warnings=[f"PDF read failure: {exc}"],
                file_hash=file_hash,
                file_size_bytes=file_size,
            )

    def extract_from_docx_file(
        self,
        file_path: Path,
        source_id: str = "",
    ) -> ExtractionResult:
        """Extract text paragraphs from a Word (.docx) document without external dependencies."""
        path = Path(file_path)
        if not path.is_file():
            raise ResourceNotFoundError(f"DOCX file not found: {path}")

        file_hash = compute_file_hash(path)
        file_size = path.stat().st_size

        if not zipfile.is_zipfile(path):
            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=[],
                full_text="",
                extraction_method="docx_xml",
                status="failed",
                notes="File is not a valid DOCX zip archive.",
                warnings=["Corrupted DOCX archive"],
                file_hash=file_hash,
                file_size_bytes=file_size,
            )

        try:
            with zipfile.ZipFile(path, "r") as z:
                xml_content = z.read("word/document.xml")

            root = ET.fromstring(xml_content)
            # Namespace for WordprocessingML
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            paragraphs: list[str] = []
            pages: list[ExtractedPage] = []
            curr_page_paras: list[str] = []
            page_num = 1

            for p in root.findall(".//w:p", ns):
                texts = [t.text for t in p.findall(".//w:t", ns) if t.text]
                p_text = sanitize_spacing("".join(texts))
                if p_text:
                    paragraphs.append(p_text)
                    curr_page_paras.append(p_text)

                # Check for page break element in this paragraph
                if p.findall(".//w:br[@w:type='page']", ns) or p.findall(
                    ".//w:lastRenderedPageBreak", ns
                ):
                    pages.append(
                        ExtractedPage(
                            page_number=page_num,
                            text="\n\n".join(curr_page_paras),
                        )
                    )
                    page_num += 1
                    curr_page_paras = []

            if curr_page_paras or not pages:
                pages.append(
                    ExtractedPage(
                        page_number=page_num,
                        text="\n\n".join(curr_page_paras),
                    )
                )

            full_text = "\n\n".join(paragraphs)
            status, warnings, ocr_status = assess_extraction_quality(pages, "docx")

            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=pages,
                full_text=full_text,
                extraction_method="docx_xml",
                status=status,
                warnings=warnings,
                file_hash=file_hash,
                file_size_bytes=file_size,
                ocr_status=ocr_status,
            )
        except Exception as exc:
            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=[],
                full_text="",
                extraction_method="docx_xml",
                status="failed",
                notes=f"DOCX extraction error: {exc}",
                warnings=[f"DOCX extraction failed: {exc}"],
                file_hash=file_hash,
                file_size_bytes=file_size,
            )

    def extract_from_scanned_file(
        self,
        file_path: Path,
        source_id: str = "",
    ) -> ExtractionResult:
        """Interface for scanned document extraction requiring OCR review."""
        path = Path(file_path)
        if not path.is_file():
            raise ResourceNotFoundError(f"Scanned image/file not found: {path}")

        file_hash = compute_file_hash(path)
        file_size = path.stat().st_size

        if self.ocr_adapter.is_available():
            pages = self.ocr_adapter.extract_text(path)
            full_text = "\n\n".join(p.text for p in pages if p.text)
            return ExtractionResult(
                source_id=source_id,
                file_path=path,
                pages=pages,
                full_text=full_text,
                extraction_method="ocr_active",
                status="needs_review",  # Machine-extracted OCR output must be reviewed
                notes="OCR engine extraction completed; flagged for human review and verification.",
                file_hash=file_hash,
                file_size_bytes=file_size,
                ocr_status="ocr_completed",
            )

        return ExtractionResult(
            source_id=source_id,
            file_path=path,
            pages=[ExtractedPage(page_number=1, text="")],
            full_text="",
            extraction_method="ocr_pending_review",
            status="needs_review",
            notes=(
                "Scanned document flagged for OCR review and verification. "
                "OCR engine not installed."
            ),
            warnings=["OCR engine not available; document flagged for manual review."],
            file_hash=file_hash,
            file_size_bytes=file_size,
            ocr_status="ocr_needed",
        )

    def extract_from_file(
        self,
        file_path: Path,
        source_id: str = "",
    ) -> ExtractionResult:
        """Dispatch extraction based on file extension."""
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext in {".txt", ".text", ".md", ".json", ".csv"}:
            return self.extract_from_txt_file(path, source_id=source_id)
        elif ext == ".pdf":
            return self.extract_from_pdf_file(path, source_id=source_id)
        elif ext == ".docx":
            return self.extract_from_docx_file(path, source_id=source_id)
        elif ext in {".png", ".jpg", ".jpeg", ".tiff", ".tif"}:
            return self.extract_from_scanned_file(path, source_id=source_id)
        else:
            return self.extract_from_txt_file(path, source_id=source_id)


def segment_into_chunks(
    extraction: ExtractionResult,
    doc_id: str,
    source_id: str,
    permission_status: str,
    verification_status: str,
) -> list[DocumentChunk]:
    """Segment extracted pages into location-preserving paragraph chunks."""
    chunks: list[DocumentChunk] = []
    chunk_counter = 0

    for page in extraction.pages:
        page_text = page.text.strip()
        if not page_text:
            continue

        raw_paragraphs = re.split(r"\n\s*\n+", page_text)
        for raw_p in raw_paragraphs:
            clean_p = sanitize_spacing(raw_p)
            if not clean_p:
                continue

            chunk_counter += 1
            content_hash = hashlib.sha256(clean_p.encode("utf-8")).hexdigest()
            p_num = page.page_number if page.page_number is not None else 1
            chunk_id = f"CHK-{doc_id}-p{p_num:03d}-c{chunk_counter:04d}"

            chunk = DocumentChunk(
                id=chunk_id,
                document_id=doc_id,
                source_id=source_id,
                page_number=page.page_number,
                section_heading=page.section_title,
                chunk_index=chunk_counter,
                text=clean_p,
                char_count=len(clean_p),
                word_count=len(clean_p.split()),
                content_hash=content_hash,
                permission_status=permission_status,
                verification_status=verification_status,
            )
            chunks.append(chunk)

    return chunks
