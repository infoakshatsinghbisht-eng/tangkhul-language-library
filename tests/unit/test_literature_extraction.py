"""Unit tests for permission-aware literary text extraction and stanza parsing."""

from __future__ import annotations

import pytest

from tangkhul_lib.core.exceptions import PermissionDeniedError
from tangkhul_lib.literature.extractor import LiteratureExtractor
from tangkhul_lib.literature.models import LiteraryRecord


def test_literature_extractor_permission_enforcement() -> None:
    extractor = LiteratureExtractor()

    # Authorized record
    auth_rec = LiteraryRecord(
        id="LIT-EXT-001",
        title="Public Folktale Excerpt",
        work_type="folk_tale",
        original_text="Tangkhul khararchan akhama.",
        permission_status="public_domain",
        access_status="metadata_only",
        verification_status="verified",
        contributor_consent=True,
    )
    assert extractor.check_permissions(auth_rec) is True

    # Restricted permission_status
    restricted_rec = LiteraryRecord(
        id="LIT-EXT-002",
        title="Restricted Modern Poem",
        work_type="poem",
        original_text="Copyrighted contemporary lines.",
        permission_status="restricted",
        access_status="metadata_only",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="restricted"):
        extractor.check_permissions(restricted_rec)

    # Restricted access_status
    restricted_access_rec = LiteraryRecord(
        id="LIT-EXT-003",
        title="Restricted Access Manuscript",
        work_type="novel",
        access_status="restricted",
        permission_status="permitted",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="restricted access"):
        extractor.check_permissions(restricted_access_rec)

    # Withheld contributor consent
    no_consent_rec = LiteraryRecord(
        id="LIT-EXT-004",
        title="Unconsented Oral Ballad Recording",
        work_type="ballad",
        contributor_consent=False,
        permission_status="community_authorized",
        verification_status="verified",
    )
    with pytest.raises(PermissionDeniedError, match="Consent not granted"):
        extractor.check_permissions(no_consent_rec)


def test_literature_extractor_extract_from_record() -> None:
    extractor = LiteratureExtractor()

    rec = LiteraryRecord(
        id="LIT-EXT-005",
        title="The Tale of the Clever Monkey",
        original_title="Shokanao wui Khararchan",
        work_type="folk_tale",
        original_text="Shokanao chi ngachada kharing wui ramli mashan kaho.",
        source_page="p. 18",
        permission_status="permitted",
        access_status="metadata_only",
        verification_status="verified",
    )
    candidates = extractor.extract_from_record(rec)
    assert len(candidates) > 0
    words = [c["word_form"].lower() for c in candidates]
    assert "shokanao" in words
    assert "khararchan" in words
    assert all(c["source_id"] == "LIT-EXT-005" for c in candidates)


def test_harvest_candidate_vocabulary_batch_and_skipping() -> None:
    extractor = LiteratureExtractor()

    rec1 = LiteraryRecord(
        id="LIT-BATCH-001",
        title="First Folk Story",
        original_title="Khararchan Khare",
        work_type="folk_tale",
        original_text="Iramwui ngalungli leikashi.",
        permission_status="permitted",
    )
    rec2 = LiteraryRecord(
        id="LIT-BATCH-002",
        title="Restricted Modern Poem",
        work_type="poem",
        original_text="Private text.",
        permission_status="restricted",
    )
    rec3 = LiteraryRecord(
        id="LIT-BATCH-003",
        title="Second Folk Story",
        original_title="Khararchan Kakhane",
        work_type="folk_tale",
        original_text="Ngalungli kacham meikha.",
        permission_status="permitted",
    )

    # With skip_restricted=True (default), rec2 is safely bypassed
    harvested = extractor.harvest_candidate_vocabulary([rec1, rec2, rec3], skip_restricted=True)
    assert len(harvested) > 0
    words = [h["word_form"].lower() for h in harvested]
    assert "iramwui" in words
    assert "ngalungli" in words
    assert "private" not in words

    # With skip_restricted=False, restricted record triggers error
    with pytest.raises(PermissionDeniedError, match="Restricted work"):
        extractor.harvest_candidate_vocabulary([rec1, rec2, rec3], skip_restricted=False)


def test_extract_stanzas_and_lines() -> None:
    extractor = LiteratureExtractor()

    poem_text = """
    Ava ram leikashi
    Iramwui ngalungli.

    Shongza khararchan
    Ngashan katharali.
    """
    lines = extractor.extract_stanzas_and_lines(
        text=poem_text,
        source_id="LIT-POEM-SYN-001",
        permission_status="permitted",
    )

    assert len(lines) == 4
    # Stanza 1
    assert lines[0]["stanza_number"] == 1
    assert lines[0]["line_in_stanza"] == 1
    assert lines[0]["overall_line"] == 1
    assert lines[0]["line_text"] == "Ava ram leikashi"
    assert lines[1]["stanza_number"] == 1
    assert lines[1]["line_in_stanza"] == 2
    assert lines[1]["overall_line"] == 2

    # Stanza 2
    assert lines[2]["stanza_number"] == 2
    assert lines[2]["line_in_stanza"] == 1
    assert lines[2]["overall_line"] == 3
    assert lines[2]["line_text"] == "Shongza khararchan"
    assert lines[3]["stanza_number"] == 2
    assert lines[3]["line_in_stanza"] == 2
    assert lines[3]["overall_line"] == 4

    # Permission check enforcement on restricted text
    with pytest.raises(PermissionDeniedError, match="restricted source"):
        extractor.extract_stanzas_and_lines(
            text=poem_text,
            source_id="LIT-POEM-SYN-002",
            permission_status="restricted",
        )
