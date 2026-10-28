"""Unit tests for Tangkhul cultural records, metadata validation, and catalogue management."""

from __future__ import annotations

from pathlib import Path

import pytest

from tangkhul_lib.core.exceptions import (
    ManifestValidationError,
    PermissionDeniedError,
    ResourceNotFoundError,
)
from tangkhul_lib.culture.catalogue import CultureCatalogue
from tangkhul_lib.culture.models import VALID_CULTURE_CATEGORIES, CulturalRecord


def test_valid_cultural_record_creation() -> None:
    rec = CulturalRecord(
        id="CULT-FEST-001",
        title="Luira Phanit",
        local_name="Luira Phanit",
        category="festival",
        subcategory="agricultural",
        translation_en="Seed-Sowing Festival",
        village="Hunphun / Ukhrul",
        dialect="Hunphun / Ukhrul",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
        notes="Spring seed-sowing festival.",
    )
    rec.validate()
    assert rec.id == "CULT-FEST-001"
    assert rec.category == "festival"
    assert rec.category in VALID_CULTURE_CATEGORIES

    d = rec.to_dict()
    assert d["id"] == "CULT-FEST-001"
    assert d["resource_type"] == "culture"

    reconstructed = CulturalRecord.from_dict(d)
    assert reconstructed.id == rec.id
    assert reconstructed.title == rec.title
    assert reconstructed.village == "Hunphun / Ukhrul"


def test_cultural_record_validation_failures() -> None:
    # Missing ID
    with pytest.raises(ManifestValidationError, match="missing required field 'id'"):
        CulturalRecord(id="", title="Title", category="proverb").validate()

    # Missing Title
    with pytest.raises(ManifestValidationError, match="missing required field 'title'"):
        CulturalRecord(id="CULT-001", title="   ", category="proverb").validate()

    # Missing Category
    with pytest.raises(ManifestValidationError, match="missing required field 'category'"):
        CulturalRecord(id="CULT-001", title="Valid Title", category="").validate()

    # Invalid Permission Status
    with pytest.raises(ManifestValidationError, match="invalid permission_status"):
        CulturalRecord(
            id="CULT-001",
            title="Valid Title",
            category="custom",
            permission_status="unknown_status",
        ).validate()

    # Invalid Access Status
    with pytest.raises(ManifestValidationError, match="invalid access_status"):
        CulturalRecord(
            id="CULT-001",
            title="Valid Title",
            category="custom",
            access_status="forbidden",
        ).validate()

    # Invalid Verification Status
    with pytest.raises(ManifestValidationError, match="invalid verification_status"):
        CulturalRecord(
            id="CULT-001",
            title="Valid Title",
            category="custom",
            verification_status="bogus_status",
        ).validate()


def test_diacritic_and_orthography_preservation() -> None:
    rec = CulturalRecord(
        id="CULT-PROV-TEST",
        title="Paotam: Ākhamatha ramkashan",
        original_text="Ākhamatha ramkashanli leishat phāmei.",
        translation_en="In the homeland, love is sweet.",
        category="proverb",
        dialect="Ukhrul",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    rec.validate()
    assert "Ā" in rec.title
    assert "ā" in rec.original_text

    manifest_rec = rec.to_manifest_record()
    assert manifest_rec.title == rec.title
    assert manifest_rec.language == "Tangkhul"


def test_vocabulary_candidate_extraction_and_permission_gate() -> None:
    rec = CulturalRecord(
        id="CULT-PROV-001",
        title="Hanna hannui shaiphamei",
        category="proverb",
        original_text="Hanna hannui shaiphamei, tuiva arartui phamei.",
        translation_en="Tender Greens are Tasty, but Elder Wisdom is Sweeter",
        dialect="Ukhrul",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    candidates = rec.extract_vocabulary_candidates()
    assert len(candidates) > 0
    words = [c["word_form"].lower() for c in candidates]
    assert "hanna" in words
    assert "hannui" in words

    # Test restricted record extraction failure
    restricted_rec = CulturalRecord(
        id="CULT-RIT-RESTRICTED",
        title="Sacred Clan Rite",
        category="ritual",
        original_text="Khamasit ritual incantation text",
        permission_status="restricted",
        access_status="restricted",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Cannot extract vocabulary from restricted"):
        restricted_rec.extract_vocabulary_candidates()

    # Test consent withholding failure
    no_consent_rec = CulturalRecord(
        id="CULT-ORAL-NOCONSENT",
        title="Private Lineage Narrative",
        category="oral_tradition",
        original_text="Secret elder narrative",
        contributor_consent=False,
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Consent not granted"):
        no_consent_rec.extract_vocabulary_candidates()


def test_catalogue_search_filtering_and_reports(tmp_path: Path) -> None:
    r1 = CulturalRecord(
        id="CULT-FEST-001",
        title="Luira Phanit",
        local_name="Luira Phanit",
        category="festival",
        village="Hunphun",
        dialect="Ukhrul",
        season_or_timing="January / February",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
    )
    r2 = CulturalRecord(
        id="CULT-PROV-001",
        title="Elder Counsel Paotam",
        local_name="Hanna hannui",
        category="proverb",
        village="Ukhrul",
        dialect="Ukhrul",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r3 = CulturalRecord(
        id="CULT-RIT-001",
        title="Sacred Taboo Observance",
        local_name="Khamasit",
        category="ritual",
        village="Ukhrul",
        dialect="Ukhrul",
        permission_status="restricted",
        access_status="restricted",
        verification_status="verified",
    )

    catalogue = CultureCatalogue([r1, r2, r3])
    assert len(catalogue) == 3

    # Search by category
    festivals = catalogue.search_records(category="festival")
    assert len(festivals) == 1
    assert festivals[0].id == "CULT-FEST-001"

    # Search with restricted exclusion
    unrestricted = catalogue.search_records(include_restricted=False)
    assert len(unrestricted) == 2
    assert all(r.id != "CULT-RIT-001" for r in unrestricted)

    # Search by query
    matches = catalogue.search_records(query="Hanna")
    assert len(matches) == 1
    assert matches[0].id == "CULT-PROV-001"

    # Report generation
    report = catalogue.get_culture_report()
    assert report["total_records"] == 3
    assert report["by_category"]["festival"] == 1
    assert report["by_category"]["proverb"] == 1
    assert report["restricted_count"] == 1

    # Exports
    jsonl_path = tmp_path / "culture_export.jsonl"
    count = catalogue.export_jsonl(jsonl_path, include_restricted=False)
    assert count == 2  # r3 is restricted and skipped

    csv_path = tmp_path / "culture_export.csv"
    count_csv = catalogue.export_csv(csv_path, include_restricted=False)
    assert count_csv == 2


def test_catalogue_duplicate_and_conflict_detection() -> None:
    rec1 = CulturalRecord(
        id="CULT-FEST-A",
        title="Luira Phanit",
        local_name="Luira",
        category="festival",
        village="Ukhrul",
        source_id="Source-1",
        description="Version 1 description",
        permission_status="community_authorized",
        verification_status="verified",
    )
    rec2 = CulturalRecord(
        id="CULT-FEST-B",
        title="Luira Phanit",
        local_name="Luira",
        category="festival",
        village="Ukhrul",
        source_id="Source-2",
        description="Version 2 description",
        permission_status="community_authorized",
        verification_status="verified",
    )
    # Regional variant from another village
    rec3 = CulturalRecord(
        id="CULT-FEST-C",
        title="Luira Phanit",
        local_name="Luira",
        category="festival",
        village="Phungcham",
        source_id="Source-3",
        permission_status="community_authorized",
        verification_status="verified",
    )

    catalogue = CultureCatalogue([rec1, rec2, rec3])
    dups = catalogue.find_likely_duplicates()
    # rec1 and rec2 share identical title/local_name in the same village
    assert len(dups) >= 1
    dup_ids = {(pair[0].id, pair[1].id) for pair in dups}
    assert ("CULT-FEST-A", "CULT-FEST-B") in dup_ids

    # Conflicting interpretations across sources
    conflicts = catalogue.find_conflicts()
    assert len(conflicts) >= 1
    concept_conflict = conflicts[0]
    assert "CULT-FEST-A" in concept_conflict["record_ids"]
    assert "CULT-FEST-B" in concept_conflict["record_ids"]
    assert len(concept_conflict["sources"]) >= 2


def test_catalogue_linking_records() -> None:
    rec1 = CulturalRecord(
        id="CULT-FEST-001",
        title="Luira Phanit",
        category="festival",
        permission_status="community_authorized",
        verification_status="verified",
    )
    rec2 = CulturalRecord(
        id="CULT-RIT-002",
        title="Luira Shimlut-Kaphung",
        category="ritual",
        permission_status="community_authorized",
        verification_status="verified",
    )
    catalogue = CultureCatalogue([rec1, rec2])
    catalogue.link_related_records("CULT-FEST-001", "CULT-RIT-002")

    assert "CULT-RIT-002" in rec1.related_records
    assert "CULT-FEST-001" in rec2.related_records

    with pytest.raises(ResourceNotFoundError):
        catalogue.link_related_records("CULT-NONEXISTENT", "CULT-RIT-002")


def test_culture_exports_and_raw_files_integrity() -> None:
    """Verify that all 24 cultural records have raw files, individual exports, and valid PDFs."""
    import json

    import pypdf

    root = Path(__file__).resolve().parent.parent.parent
    exports_dir = root / "data" / "exports"
    cult_exports_dir = exports_dir / "culture"

    manifest_file = root / "data" / "manifests" / "culture.jsonl"
    with open(manifest_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    assert len(records) == 35

    # Consolidated JSON and PDF
    assert (exports_dir / "culture.json").is_file()
    assert (exports_dir / "culture.pdf").is_file()

    reader = pypdf.PdfReader(str(exports_dir / "culture.pdf"))
    assert len(reader.pages) == 36

    # Individual files
    for r in records:
        cid = r["id"]
        # Raw file
        local_path = root / r["local_path"]
        assert local_path.is_file(), f"Missing raw culture file: {local_path}"
        content = local_path.read_text(encoding="utf-8")
        assert f"RESOURCE IDENTIFIER: {cid}" in content

        # Individual JSON
        ind_json = cult_exports_dir / f"{cid}.json"
        assert ind_json.is_file(), f"Missing individual culture JSON: {ind_json}"

        # Individual PDF
        ind_pdf = cult_exports_dir / f"{cid}.pdf"
        assert ind_pdf.is_file(), f"Missing individual culture PDF: {ind_pdf}"
        ind_reader = pypdf.PdfReader(str(ind_pdf))
        assert len(ind_reader.pages) >= 1

    # Verify dedicated newly added resources exist
    id_set = {r["id"] for r in records}
    assert "CULT-PRAY-001" in id_set
    assert "CULT-RIT-003" in id_set
    assert "CULT-SOC-001" in id_set
