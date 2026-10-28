"""Unit tests for tangkhul CLI operations."""

from __future__ import annotations

from tangkhul_lib.cli import main


def test_cli_version(capsys) -> None:
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "tangkhul" in captured.out or "0.1.0" in captured.out


def test_cli_info(capsys) -> None:
    code = main(["--info"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Language Library" in captured.out
    assert "Project root:" in captured.out


def test_cli_books_list(capsys) -> None:
    code = main(["books", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Books Catalogue" in captured.out
    assert "BK-TLS-001" in captured.out


def test_cli_books_search(capsys) -> None:
    code = main(["books", "--search", "Grammar"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Tangkhul Grammar" in captured.out


def test_cli_books_id(capsys) -> None:
    code = main(["books", "--id", "BK-HIST-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Book ID:       BK-HIST-001" in captured.out
    assert "William Pettigrew" in captured.out


def test_cli_songs_list(capsys) -> None:
    code = main(["songs", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Songs Catalogue" in captured.out
    assert "SNG-TRAD-001" in captured.out


def test_cli_songs_search(capsys) -> None:
    code = main(["songs", "--search", "Shimreishang"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Shimreishang" in captured.out


def test_cli_songs_id(capsys) -> None:
    code = main(["songs", "--id", "SNG-TRAD-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Song ID:       SNG-TRAD-001" in captured.out
    assert "Shimreishang" in captured.out
    assert "Type:" in captured.out


def test_cli_songs_id_not_found(capsys) -> None:
    code = main(["songs", "--id", "SNG-NONEXISTENT-999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_songs_filter_type(capsys) -> None:
    code = main(["songs", "--type", "folk"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "folk" in captured.out


def test_cli_songs_filter_singer(capsys) -> None:
    code = main(["songs", "--singer", "Rewben"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Rewben Mashangva" in captured.out


def test_cli_dictionaries_list(capsys) -> None:
    code = main(["dictionaries", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Dictionaries Catalogue" in captured.out
    assert "DIC-HIST-001" in captured.out


def test_cli_dictionaries_search(capsys) -> None:
    code = main(["dictionaries", "--search", "Pettigrew"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Tangkhul Naga Grammar and Dictionary" in captured.out


def test_cli_dictionaries_id(capsys) -> None:
    code = main(["dictionaries", "--id", "DIC-HIST-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Dictionary ID: DIC-HIST-001" in captured.out
    assert "William Pettigrew" in captured.out
    assert "Permissions:" in captured.out


def test_cli_dictionaries_id_not_found(capsys) -> None:
    code = main(["dictionaries", "--id", "DIC-NONEXISTENT-999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_dictionaries_filter_author(capsys) -> None:
    code = main(["dictionaries", "--author", "Luikham"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Tangkhul Tui Dictionary" in captured.out


def test_cli_dictionaries_filter_language_pair(capsys) -> None:
    code = main(["dictionaries", "--language-pair", "Tangkhul-English"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "DIC-HIST-001" in captured.out


def test_cli_dictionaries_filter_verification_status(capsys) -> None:
    code = main(["dictionaries", "--verification-status", "needs_review"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "DIC-CAND-001" in captured.out


def test_cli_culture_list(capsys) -> None:
    code = main(["culture", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Culture Catalogue" in captured.out
    assert "CULT-FEST-001" in captured.out
    assert "Luira Phanit" in captured.out


def test_cli_culture_search(capsys) -> None:
    code = main(["culture", "--search", "Luira"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "CULT-FEST-001" in captured.out


def test_cli_culture_id(capsys) -> None:
    code = main(["culture", "--id", "CULT-FEST-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Record ID:     CULT-FEST-001" in captured.out
    assert "Luira Phanit" in captured.out
    assert "festival" in captured.out


def test_cli_culture_id_not_found(capsys) -> None:
    code = main(["culture", "--id", "CULT-NONEXISTENT-999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_culture_filter_category(capsys) -> None:
    code = main(["culture", "--category", "proverb"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "CULT-PROV-001" in captured.out


def test_cli_culture_filter_village(capsys) -> None:
    code = main(["culture", "--village", "Ukhrul"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Ukhrul" in captured.out


def test_cli_culture_filter_dialect(capsys) -> None:
    code = main(["culture", "--dialect", "Phungcham"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "CULT-ORAL-001" in captured.out


def test_cli_culture_filter_verification_status(capsys) -> None:
    code = main(["culture", "--verification-status", "needs_review"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "CULT-CAND-001" in captured.out


def test_cli_history_list(capsys) -> None:
    code = main(["history", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul History Catalogue" in captured.out
    assert "HIST-EVT-001" in captured.out


def test_cli_history_search(capsys) -> None:
    code = main(["history", "--search", "Ukhrul"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "HIST-PLC-001" in captured.out


def test_cli_history_id(capsys) -> None:
    code = main(["history", "--id", "HIST-EVT-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Record ID:     HIST-EVT-001" in captured.out
    assert "Pettigrew's Arrival" in captured.out
    assert "historical_event" in captured.out
    assert "Evidence:" in captured.out


def test_cli_history_id_not_found(capsys) -> None:
    code = main(["history", "--id", "HIST-NONEXISTENT-999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_history_filter_type(capsys) -> None:
    code = main(["history", "--type", "person"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "HIST-PRS-001" in captured.out


def test_cli_history_filter_period(capsys) -> None:
    code = main(["history", "--period", "Colonial"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "HIST-EVT-001" in captured.out


def test_cli_history_filter_place(capsys) -> None:
    code = main(["history", "--place", "Makhel"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "HIST-PLC-002" in captured.out


def test_cli_history_filter_verification_status(capsys) -> None:
    code = main(["history", "--verification-status", "needs_review"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "HIST-CAND-001" in captured.out


def test_cli_literature_list(capsys) -> None:
    code = main(["literature", "--list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tangkhul Literature Catalogue" in captured.out
    assert "LIT-POEM-001" in captured.out


def test_cli_literature_search(capsys) -> None:
    code = main(["literature", "--search", "Ava Ram"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "Ava Ram Leishat" in captured.out


def test_cli_literature_id(capsys) -> None:
    code = main(["literature", "--id", "LIT-POEM-001"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Work ID:       LIT-POEM-001" in captured.out
    assert "Ava Ram Leishat" in captured.out
    assert "Work Type:     poem" in captured.out
    assert "Author:        Luingam A. Shimray" in captured.out


def test_cli_literature_id_not_found(capsys) -> None:
    code = main(["literature", "--id", "LIT-NONEXISTENT-999"])
    assert code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_literature_filter_type(capsys) -> None:
    code = main(["literature", "--type", "folk_tale"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "LIT-FLK-003" in captured.out


def test_cli_literature_filter_genre(capsys) -> None:
    code = main(["literature", "--genre", "ballad"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "LIT-FLK-001" in captured.out


def test_cli_literature_filter_author(capsys) -> None:
    code = main(["literature", "--author", "Luingam"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "LIT-POEM-001" in captured.out


def test_cli_literature_filter_language(capsys) -> None:
    code = main(["literature", "--language", "Tangkhul"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out


def test_cli_literature_filter_verification_status(capsys) -> None:
    code = main(["literature", "--verification-status", "needs_review"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Found" in captured.out
    assert "LIT-CAND-001" in captured.out


