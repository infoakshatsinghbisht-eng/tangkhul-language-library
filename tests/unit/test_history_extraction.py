"""Unit tests for permission-aware historical extraction and toponym harvesting."""

from __future__ import annotations

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.history.extractor import HistoryExtractor
from tangkhul_lib.history.models import HistoricalRecord


def test_history_extractor_permission_enforcement() -> None:
    extractor = HistoryExtractor()

    # Authorized record
    auth_rec = HistoricalRecord(
        id="HIST-EXT-001",
        title="Public Historical Event",
        record_type="historical_event",
        original_text="Hunphun khare eili.",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
        contributor_consent=True,
    )
    assert extractor.check_permissions(auth_rec) is True

    # Restricted permission_status
    restricted_rec = HistoricalRecord(
        id="HIST-EXT-002",
        title="Restricted Clan Genealogy",
        record_type="person",
        original_text="Secret genealogy",
        permission_status="restricted",
        access_status="metadata_only",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Extraction prohibited"):
        extractor.check_permissions(restricted_rec)

    # Restricted access_status
    restricted_access_rec = HistoricalRecord(
        id="HIST-EXT-003",
        title="Restricted Access Chronicle",
        record_type="historical_document",
        access_status="restricted",
        permission_status="public_domain",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="restricted access status"):
        extractor.check_permissions(restricted_access_rec)

    # Withheld contributor consent
    no_consent_rec = HistoricalRecord(
        id="HIST-EXT-004",
        title="Unconsented Oral Interview",
        record_type="oral_history",
        contributor_consent=False,
        permission_status="community_authorized",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Consent not granted"):
        extractor.check_permissions(no_consent_rec)


def test_history_extractor_extract_from_record() -> None:
    extractor = HistoryExtractor()
    rec = HistoricalRecord(
        id="HIST-EXT-005",
        title="Battle of Sangshak Delaying Action",
        record_type="historical_event",
        original_text="Sangshak eili Japanese rāhaoda maran ngasak.",
        place="Sangshak",
        village="Sangshak",
        people_involved=["Major Bob Khating"],
        source_id="SRC-WW2-HIST",
        source_page="112",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    candidates = extractor.extract_from_record(rec)
    assert len(candidates) >= 3
    words = [c["word_form"] for c in candidates]
    assert "Sangshak" in words
    assert "Bob" in words or "Major" in words
    assert "Japanese" in words


def test_history_extractor_harvest_candidate_vocabulary() -> None:
    extractor = HistoryExtractor()
    r1 = HistoricalRecord(
        id="HIST-HARV-001",
        title="Record One",
        record_type="place",
        original_text="Shirui Kashong kaphung.",
        place="Shirui",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r2 = HistoricalRecord(
        id="HIST-HARV-002",
        title="Record Two Duplicate",
        record_type="place",
        original_text="Shirui kaphung kapai.",
        place="Shirui",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
    )
    r3 = HistoricalRecord(
        id="HIST-HARV-003",
        title="Restricted Record",
        record_type="oral_history",
        original_text="Private text",
        permission_status="restricted",
        access_status="restricted",
        verification_status="needs_review",
    )

    # Harvesting with skip_restricted=True
    harvested = extractor.harvest_candidate_vocabulary([r1, r2, r3], skip_restricted=True)
    words = [h["word_form"].lower() for h in harvested]
    assert "shirui" in words
    assert "kashong" in words
    assert "kaphung" in words
    # Check deduplication: each word form should only appear once
    assert len(words) == len(set(words))

    # Harvesting with skip_restricted=False should raise PermissionDeniedError
    with pytest.raises(PermissionDeniedError, match="Restricted record"):
        extractor.harvest_candidate_vocabulary([r1, r3], skip_restricted=False)


def test_history_extractor_extract_toponyms() -> None:
    extractor = HistoryExtractor()
    sample_text = (
        "The historical expedition traversed Hunphun Village, ascended Shirui Peak, "
        "and established an outpost near Khangkhui Hill overlooking the ridge."
    )
    toponyms = extractor.extract_toponyms(
        text=sample_text,
        source_id="HIST-EXPEDITION-1910",
        permission_status="public_domain",
    )
    assert len(toponyms) >= 3
    names = [t["word_form"] for t in toponyms]
    assert "Hunphun" in names
    assert "Shirui" in names
    assert "Khangkhui" in names

    # Restricted source should raise error
    with pytest.raises(PermissionDeniedError, match="restricted source"):
        extractor.extract_toponyms(
            text=sample_text,
            source_id="HIST-CONFIDENTIAL-DOC",
            permission_status="restricted",
        )
