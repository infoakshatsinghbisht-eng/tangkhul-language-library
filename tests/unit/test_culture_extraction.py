"""Unit tests for permission-aware cultural extraction and proverb parsing."""

from __future__ import annotations

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.culture.extractor import CultureExtractor
from tangkhul_lib.culture.models import CulturalRecord


def test_culture_extractor_permission_enforcement() -> None:
    extractor = CultureExtractor()

    # Authorized record
    auth_rec = CulturalRecord(
        id="CULT-PROV-001",
        title="Proverb on Counsel",
        category="proverb",
        original_text="Hanna hannui shaiphamei.",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
        contributor_consent=True,
    )
    assert extractor.check_permissions(auth_rec) is True

    # Restricted record
    restricted_rec = CulturalRecord(
        id="CULT-RIT-001",
        title="Esoteric Clan Incantation",
        category="ritual",
        original_text="Secret text",
        permission_status="restricted",
        access_status="restricted",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Extraction prohibited"):
        extractor.check_permissions(restricted_rec)

    # Consent withheld
    no_consent_rec = CulturalRecord(
        id="CULT-ORAL-001",
        title="Private Oral Lore",
        category="oral_tradition",
        original_text="Private lore",
        contributor_consent=False,
        permission_status="community_authorized",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Contributor consent withheld"):
        extractor.check_permissions(no_consent_rec)


def test_culture_extractor_proverbs_parsing() -> None:
    extractor = CultureExtractor()
    sample_text = """
    Tangkhul Paotam Collection:
    1. Hanna hannui shaiphamei : Tender greens are tasty, but elder counsel is sweeter.
    2. Nguihaowada masi kongra li : A person cannot be drowned for a mistake.
    3. Khamor kachangna phei ngazekli : Sharp words pierce deeper than spear wounds.
    """
    proverbs = extractor.extract_proverbs_from_text(
        text=sample_text,
        source_id="Kasomwoshi-Chanjam",
        permission_status="public_domain",
    )
    assert len(proverbs) == 3
    assert proverbs[0]["original_text"] == "Hanna hannui shaiphamei"
    assert "elder counsel" in proverbs[0]["translation_en"].lower()
    assert proverbs[0]["category"] == "proverb"

    # Restricted source test
    with pytest.raises(PermissionDeniedError, match="restricted source"):
        extractor.extract_proverbs_from_text(
            text=sample_text,
            source_id="Restricted-Source",
            permission_status="restricted",
        )


def test_harvest_candidate_vocabulary() -> None:
    extractor = CultureExtractor()
    r1 = CulturalRecord(
        id="CULT-FEST-001",
        title="Luira Phanit Seed Festival",
        local_name="Luira Phanit",
        category="festival",
        original_text="Awunga kaphung kachang",
        permission_status="community_authorized",
        verification_status="verified",
    )
    r2 = CulturalRecord(
        id="CULT-PROV-001",
        title="Elder Saying",
        category="proverb",
        original_text="Hanna hannui shaiphamei",
        permission_status="public_domain",
        verification_status="verified",
    )
    r3_restricted = CulturalRecord(
        id="CULT-RIT-RESTRICTED",
        title="Taboo Rite",
        category="ritual",
        original_text="Restricted rite",
        permission_status="restricted",
        verification_status="verified",
    )

    harvested = extractor.harvest_candidate_vocabulary(
        [r1, r2, r3_restricted], skip_restricted=True
    )
    assert len(harvested) > 0
    words = [h["word_form"].lower() for h in harvested]
    assert "awunga" in words
    assert "hanna" in words
    # Restricted record content is not harvested
    assert "restricted" not in words

    # If skip_restricted=False, it should raise PermissionDeniedError
    with pytest.raises(PermissionDeniedError, match="Restricted record"):
        extractor.harvest_candidate_vocabulary([r1, r3_restricted], skip_restricted=False)
