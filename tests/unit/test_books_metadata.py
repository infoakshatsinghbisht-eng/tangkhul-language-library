"""Unit tests for Tangkhul book metadata models and catalogue management."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.books.catalogue import BookCatalogue
from tangkhul_lib.books.models import BookRecord
from tangkhul_lib.core.exceptions import ManifestValidationError, ResourceNotFoundError


def test_valid_book_record_creation() -> None:
    book = BookRecord(
        id="BK-TLS-001",
        title="Wontui Tangkhul",
        alternate_titles=["Wontui Tangkhul, Class II"],
        authors=[],
        editors=[],
        publisher="Tangkhul Literature Society, Manipur",
        publication_year=2022,
        subject="Literature",
        educational_level="Class II",
        language="Tangkhul",
        dialect="Standard Tangkhul",
        source_url="https://bharatavani.in/tangkhul/textbook",
        source_identifier="BVP-TB-TKH-001",
        permission_status="pending",
        access_status="metadata_only",
        verification_status="verified",
    )
    book.validate()
    assert book.id == "BK-TLS-001"
    assert book.year == 2022
    assert book.publication_year == 2022
    assert book.educational_level == "Class II"

    d = book.to_dict()
    assert d["id"] == "BK-TLS-001"
    assert d["year"] == 2022

    reconstructed = BookRecord.from_dict(d)
    assert reconstructed.id == book.id
    assert reconstructed.title == book.title
    assert reconstructed.publication_year == book.publication_year


def test_book_record_validation_errors() -> None:
    # Empty ID
    with pytest.raises(ManifestValidationError, match="non-empty string"):
        BookRecord(id="", title="Title").validate()

    # Empty Title
    with pytest.raises(ManifestValidationError, match="missing or empty 'title'"):
        BookRecord(id="BK-001", title="   ").validate()

    # Invalid permission status
    with pytest.raises(ManifestValidationError, match="Invalid permission_status"):
        BookRecord(
            id="BK-001",
            title="Title",
            permission_status="unauthorized_status",
        ).validate()

    # Invalid verification status
    with pytest.raises(ManifestValidationError, match="Invalid verification_status"):
        BookRecord(
            id="BK-001",
            title="Title",
            verification_status="totally_fake",
        ).validate()

    # Invalid access status
    with pytest.raises(ManifestValidationError, match="Invalid access_status"):
        BookRecord(
            id="BK-001",
            title="Title",
            access_status="unknown_status",
        ).validate()


def test_book_record_unknown_fields_and_manifest_conversion() -> None:
    data = {
        "id": "BK-HIST-001",
        "title": "Tangkhul Naga Grammar and Dictionary",
        "authors": ["William Pettigrew"],
        "publication_year": 1918,
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "unknown_extra_field": "ignored_safely",
    }
    book = BookRecord.from_dict(data)
    assert book.id == "BK-HIST-001"
    assert book.authors == ["William Pettigrew"]

    manifest_rec = book.to_manifest_record()
    assert manifest_rec.id == "BK-HIST-001"
    assert manifest_rec.creator == "William Pettigrew"
    assert manifest_rec.year == 1918
    assert manifest_rec.resource_type == "books"


def test_catalogue_add_and_get() -> None:
    catalogue = BookCatalogue()
    b1 = BookRecord(
        id="BK-TLS-001",
        title="Wontui Tangkhul",
        subject="Literature",
        educational_level="Class II",
        publication_year=2022,
        publisher="Tangkhul Literature Society, Manipur",
        verification_status="verified",
    )
    catalogue.add_book(b1)
    assert len(catalogue) == 1
    assert catalogue.get_book("BK-TLS-001") == b1
    assert catalogue.get_book("NON_EXISTENT") is None

    # Duplicate ID prevents accidental overwrite
    with pytest.raises(ManifestValidationError, match="already exists"):
        catalogue.add_book(b1, allow_overwrite=False)

    # Overwrite allowed when explicitly requested
    catalogue.add_book(b1, allow_overwrite=True)
    assert len(catalogue) == 1


def test_catalogue_search_and_filter() -> None:
    b1 = BookRecord(
        id="BK-TLS-001",
        title="Wontui Tangkhul",
        subject="Literature",
        educational_level="Class II",
        publication_year=2022,
        publisher="Tangkhul Literature Society, Manipur",
        verification_status="verified",
    )
    b2 = BookRecord(
        id="BK-TLS-006",
        title="Zingshan Tangkhul Kachishata",
        subject="History",
        educational_level="Class VIII",
        publication_year=2021,
        publisher="Tangkhul Literature Society, Manipur",
        verification_status="verified",
    )
    b3 = BookRecord(
        id="BK-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary",
        authors=["William Pettigrew"],
        subject="Grammar and Lexicography",
        educational_level="Academic",
        publication_year=1918,
        publisher="Assam Secretariat Printing Office",
        verification_status="verified",
        permission_status="public_domain",
        access_status="full_text_available",
    )
    catalogue = BookCatalogue([b1, b2, b3])

    # Search by author
    res_author = catalogue.search_books(author="Pettigrew")
    assert len(res_author) == 1
    assert res_author[0].id == "BK-HIST-001"

    # Filter by subject
    res_subj = catalogue.search_books(subject="History")
    assert len(res_subj) == 1
    assert res_subj[0].id == "BK-TLS-006"

    # Filter by year
    res_year = catalogue.search_books(publication_year=2022)
    assert len(res_year) == 1
    assert res_year[0].id == "BK-TLS-001"

    # Search query
    res_q = catalogue.search_books(query="grammar")
    assert len(res_q) == 1
    assert res_q[0].id == "BK-HIST-001"


def test_duplicate_detection_distinguishes_distinct_class_editions() -> None:
    # Zingyar Tangkhul Class IV (2022) vs Zingyar Tangkhul Class V (2021)
    b_class4 = BookRecord(
        id="BK-TLS-002",
        title="Zingyar Tangkhul",
        educational_level="Class IV",
        publication_year=2022,
        publisher="Tangkhul Literature Society, Manipur",
    )
    b_class5 = BookRecord(
        id="BK-TLS-003",
        title="Zingyar Tangkhul",
        educational_level="Class V",
        publication_year=2021,
        publisher="Tangkhul Literature Society, Manipur",
    )

    catalogue = BookCatalogue([b_class4])

    # Distinct levels should NOT be flagged as duplicate
    dups = catalogue.detect_duplicates(b_class5)
    assert len(dups) == 0

    # True duplicate (same title and same level)
    candidate_duplicate = BookRecord(
        id="BK-NEW-001",
        title="Zingyar Tangkhul",
        educational_level="Class IV",
        publication_year=2022,
        publisher="Tangkhul Literature Society, Manipur",
    )
    dups2 = catalogue.detect_duplicates(candidate_duplicate)
    assert len(dups2) == 1
    assert dups2[0][0].id == "BK-TLS-002"


def test_catalogue_update_and_export(tmp_path: Path) -> None:
    b1 = BookRecord(
        id="BK-TLS-001",
        title="Wontui Tangkhul",
        subject="Literature",
        educational_level="Class II",
        publication_year=2022,
        verification_status="verified",
    )
    catalogue = BookCatalogue([b1])

    # Update metadata
    updated = catalogue.update_book("BK-TLS-001", {"notes": "Updated verification notes."})
    assert updated.notes == "Updated verification notes."
    assert catalogue.get_book("BK-TLS-001").notes == "Updated verification notes."

    # Updating non-existent book
    with pytest.raises(ResourceNotFoundError):
        catalogue.update_book("NON_EXISTENT", {"notes": "abc"})

    # Export to JSONL and CSV
    jsonl_out = tmp_path / "books_export.jsonl"
    csv_out = tmp_path / "books_export.csv"
    catalogue.export_catalogue(jsonl_out, format="jsonl")
    catalogue.export_catalogue(csv_out, format="csv")

    assert jsonl_out.is_file()
    assert csv_out.is_file()

    # Load from exported manifest
    loaded_catalogue = BookCatalogue.load_from_manifest(jsonl_out)
    assert len(loaded_catalogue) == 1
    assert loaded_catalogue.get_book("BK-TLS-001").title == "Wontui Tangkhul"
