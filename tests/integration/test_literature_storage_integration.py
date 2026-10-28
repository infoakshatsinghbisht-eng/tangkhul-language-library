"""Integration tests for literature storage, SQLite schema, repository CRUD, and manifest sync."""

from __future__ import annotations

from pathlib import Path

from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, ManifestRepository


def test_database_literature_crud_and_manifest_sync(tmp_path: Path) -> None:
    db_file = tmp_path / "literature_corpus.sqlite"
    db_manager = DatabaseManager(db_file)
    db_manager.initialize_schema()

    literature_repo = LiteratureRepository(db_manager)
    manifest_repo = ManifestRepository(db_manager)

    rec = LiteraryRecord(
        id="LIT-TEST-BALLAD-001",
        title="Shimreishang Kala Maitonphi",
        alternate_titles=["Maitonphi Shimreishang Khararchan"],
        original_title="Shimreishang Kala Maitonphi",
        title_translation="The Ballad of Shimreishang and Maitonphi",
        work_type="ballad",
        genres=["ballad", "oral_narrative"],
        author="Traditional",
        storyteller="Phungcham Oral Custodians",
        publication_year=1982,
        composition_date="c. 17th century",
        edition="First Edition",
        publisher="Central Institute of Indian Languages, Mysore",
        language="Tangkhul",
        dialect="Phungcham / Standard Tangkhul",
        village="Phungcham",
        region="Northern Tangkhul",
        book_id="BK-CIIL-003",
        source_id="CIIL-FLK-1982-SKM",
        source_title="Tangkhul Folk Literature (Arokianathan 1982)",
        source_page="pp. 12-45",
        license="Traditional Oral Heritage",
        permission_status="community_authorized",
        access_status="metadata_only",
        verification_status="verified",
        text_availability="metadata_only",
        notes="Phungcham tragic romantic ballad preserving archaic poetic expressions.",
    )
    literature_repo.add(rec)

    # 1. Verify retrieval from SQLite literature table
    retrieved = literature_repo.get_by_id("LIT-TEST-BALLAD-001")
    assert retrieved is not None
    assert retrieved.id == "LIT-TEST-BALLAD-001"
    assert retrieved.title == "Shimreishang Kala Maitonphi"
    assert retrieved.work_type == "ballad"
    assert "ballad" in retrieved.genres
    assert retrieved.publication_year == 1982
    assert retrieved.village == "Phungcham"
    assert retrieved.book_id == "BK-CIIL-003"
    assert retrieved.storyteller == "Phungcham Oral Custodians"
    assert "Maitonphi Shimreishang Khararchan" in retrieved.alternate_titles

    # 2. Verify manifest_records sync
    manifest_rec = manifest_repo.get_by_id("LIT-TEST-BALLAD-001")
    assert manifest_rec is not None
    assert manifest_rec.id == "LIT-TEST-BALLAD-001"
    assert manifest_rec.resource_type == "literature"
    assert manifest_rec.title == "Shimreishang Kala Maitonphi"

    # 3. Add second record
    rec2 = LiteraryRecord(
        id="LIT-TEST-POEM-001",
        title="Ava Ram Leishat",
        original_title="Ava Ram Leishat",
        work_type="poem",
        genres=["poem"],
        author="Luingam A. Shimray",
        poet="Luingam A. Shimray",
        publication_year=2000,
        publisher="Tangkhul Literature Society, Manipur",
        village="Ukhrul",
        book_id="BK-TLS-007",
        permission_status="permitted",
        access_status="metadata_only",
        verification_status="verified",
    )
    literature_repo.add(rec2)

    # 4. Count and list operations
    assert literature_repo.count() == 2
    all_works = literature_repo.list_all()
    assert len(all_works) == 2

    sorted_works = literature_repo.list_all(sort_by_year=True)
    assert sorted_works[0].publication_year == 1982
    assert sorted_works[1].publication_year == 2000

    # 5. Queries by genre, author, book_id
    ballads = literature_repo.list_by_genre("ballad")
    assert len(ballads) == 1
    assert ballads[0].id == "LIT-TEST-BALLAD-001"

    author_matches = literature_repo.list_by_author("Luingam")
    assert len(author_matches) == 1
    assert author_matches[0].id == "LIT-TEST-POEM-001"

    book_links = literature_repo.list_by_book_id("BK-TLS-007")
    assert len(book_links) == 1
    assert book_links[0].id == "LIT-TEST-POEM-001"

    # 6. Update operation
    updated = literature_repo.update("LIT-TEST-POEM-001", {"notes": "Updated educational notes."})
    assert updated.notes == "Updated educational notes."
    refetched = literature_repo.get_by_id("LIT-TEST-POEM-001")
    assert refetched is not None
    assert refetched.notes == "Updated educational notes."

    # 7. Token persistence
    sample_tokens = [
        {"word_form": "iramwui", "context_sentence": "Iramwui ngalungli."},
        {"word_form": "leikashi", "context_sentence": "Leikashi mayonser."},
    ]
    literature_repo.save_tokens("LIT-TEST-POEM-001", sample_tokens)
    stored_tokens = literature_repo.get_extracted_tokens("LIT-TEST-POEM-001")
    assert len(stored_tokens) == 2
    word_forms = [t["word_form"] for t in stored_tokens]
    assert "iramwui" in word_forms
    assert "leikashi" in word_forms
