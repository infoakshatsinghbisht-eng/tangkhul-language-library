"""Command-line interface for Tangkhul Language Library."""

from __future__ import annotations

import argparse
import sys

from tangkhul_lib import __version__
from tangkhul_lib.books.catalogue import BookCatalogue
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.culture.catalogue import CultureCatalogue
from tangkhul_lib.dictionaries.catalogue import DictionaryCatalogue
from tangkhul_lib.history.catalogue import HistoryCatalogue
from tangkhul_lib.literature.catalogue import LiteratureCatalogue
from tangkhul_lib.songs.catalogue import SongCatalogue
from tangkhul_lib.songs.lyrics_data import get_song_lyrics


def main(argv: list[str] | None = None) -> int:
    """Entrypoint for the `tangkhul` command-line utility."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        prog="tangkhul",
        description="Tangkhul Language Library CLI — tools for language preservation and research.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Print project configuration and environment status.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Books subcommand
    books_parser = subparsers.add_parser("books", help="Tangkhul books catalogue operations")
    books_parser.add_argument("--list", action="store_true", help="List all catalogued books")
    books_parser.add_argument(
        "--search",
        type=str,
        help="Search books by title, author, or subject",
    )
    books_parser.add_argument("--id", type=str, help="Display detailed metadata for a book ID")
    books_parser.add_argument(
        "--full",
        action="store_true",
        help="Display complete cover-to-cover book with all chapters and pages",
    )
    books_parser.add_argument(
        "--chapters",
        action="store_true",
        help="List all chapters for the specified book ID",
    )
    books_parser.add_argument(
        "--chapter",
        type=int,
        help="Display specific chapter content by chapter number",
    )
    books_parser.add_argument(
        "--pages",
        action="store_true",
        help="List all pages from page 1 to end page for the specified book ID",
    )
    books_parser.add_argument(
        "--page",
        type=int,
        help="Display specific page content by page number",
    )
    books_parser.add_argument(
        "--search-content",
        type=str,
        help="Search full text across all pages and chapters of books",
    )


    # Songs subcommand
    songs_parser = subparsers.add_parser("songs", help="Tangkhul songs catalogue operations")
    songs_parser.add_argument("--list", action="store_true", help="List all catalogued songs")
    songs_parser.add_argument(
        "--search",
        type=str,
        help="Search songs by title, singer, village, or lyrics keywords",
    )
    songs_parser.add_argument("--id", type=str, help="Display detailed metadata for a song ID")
    songs_parser.add_argument("--type", type=str, help="Filter songs by song_type (e.g. folk)")
    songs_parser.add_argument("--singer", type=str, help="Filter songs by singer name")
    songs_parser.add_argument("--village", type=str, help="Filter songs by village origin")
    songs_parser.add_argument(
        "--lyrics",
        action="store_true",
        help="Display complete lyrics stanzas and line-by-line English translations",
    )
    songs_parser.add_argument(
        "--full",
        action="store_true",
        help="Display full song metadata along with complete lyrics stanzas and translations",
    )

    # Dictionaries subcommand
    dict_parser = subparsers.add_parser(
        "dictionaries", help="Tangkhul dictionaries and lexical catalogue operations"
    )
    dict_parser.add_argument(
        "--list", action="store_true", help="List all catalogued dictionary sources"
    )
    dict_parser.add_argument(
        "--search",
        type=str,
        help="Search dictionaries by title, author, or keyword",
    )
    dict_parser.add_argument("--id", type=str, help="Display detailed metadata for a dictionary ID")
    dict_parser.add_argument("--entry", type=str, help="Search lexical entry by headword")
    dict_parser.add_argument(
        "--language-pair", type=str, help="Filter dictionaries by language pair"
    )
    dict_parser.add_argument("--author", type=str, help="Filter dictionaries by author or compiler")
    dict_parser.add_argument("--dialect", type=str, help="Filter dictionaries by dialect variety")
    dict_parser.add_argument(
        "--verification-status",
        type=str,
        help="Filter dictionaries by verification status (e.g. needs_review, verified)",
    )

    # Culture subcommand
    culture_parser = subparsers.add_parser(
        "culture", help="Tangkhul culture, proverbs, festivals, and customs operations"
    )
    culture_parser.add_argument(
        "--list", action="store_true", help="List all catalogued cultural records"
    )
    culture_parser.add_argument(
        "--search",
        type=str,
        help="Search cultural records by title, local name, proverb, or keyword",
    )
    culture_parser.add_argument(
        "--id", type=str, help="Display detailed metadata for a cultural record ID"
    )
    culture_parser.add_argument(
        "--category",
        type=str,
        help="Filter cultural records by category (e.g. proverb, festival, custom)",
    )
    culture_parser.add_argument(
        "--village", type=str, help="Filter cultural records by village origin"
    )
    culture_parser.add_argument(
        "--dialect", type=str, help="Filter cultural records by dialect variety"
    )
    culture_parser.add_argument(
        "--verification-status",
        type=str,
        help="Filter cultural records by verification status (e.g. needs_review, verified)",
    )

    # History subcommand
    history_parser = subparsers.add_parser(
        "history", help="Tangkhul history and timeline catalogue operations"
    )
    history_parser.add_argument(
        "--list", action="store_true", help="List all catalogued historical records"
    )
    history_parser.add_argument(
        "--search",
        type=str,
        help="Search historical records by title, summary, or keyword",
    )
    history_parser.add_argument(
        "--id", type=str, help="Display detailed metadata for a historical record ID"
    )
    history_parser.add_argument(
        "--type",
        type=str,
        help="Filter historical records by record type (e.g. historical_event, person, place)",
    )
    history_parser.add_argument(
        "--period",
        type=str,
        help="Filter historical records by historical period (e.g. '19th century')",
    )
    history_parser.add_argument(
        "--place",
        type=str,
        help="Filter historical records by place or settlement name",
    )
    history_parser.add_argument(
        "--verification-status",
        type=str,
        help="Filter historical records by verification status (e.g. needs_review, verified)",
    )

    # Literature subcommand
    literature_parser = subparsers.add_parser(
        "literature", help="Tangkhul literature and literary works catalogue operations"
    )
    literature_parser.add_argument(
        "--list", action="store_true", help="List all catalogued literary works"
    )
    literature_parser.add_argument(
        "--search",
        type=str,
        help="Search literary works by title, author, or keyword",
    )
    literature_parser.add_argument(
        "--id", type=str, help="Display detailed metadata for a literary work ID"
    )
    literature_parser.add_argument(
        "--type",
        type=str,
        help="Filter literary works by work type (e.g. poem, folk_tale, play, short_story)",
    )
    literature_parser.add_argument(
        "--genre",
        type=str,
        help="Filter literary works by genre (e.g. ballad, lyric_poetry, fable)",
    )
    literature_parser.add_argument(
        "--author",
        type=str,
        help="Filter literary works by author, poet, or storyteller name",
    )
    literature_parser.add_argument(
        "--language",
        type=str,
        help="Filter literary works by language (e.g. Tangkhul)",
    )
    literature_parser.add_argument(
        "--verification-status",
        type=str,
        help="Filter literary works by verification status (e.g. needs_review, verified)",
    )

    # Vocab subcommand
    vocab_parser = subparsers.add_parser(
        "vocab",
        help="Unified Tangkhul vocabulary search across all six modules",
    )
    vocab_parser.add_argument(
        "--list",
        action="store_true",
        help="List catalogued vocabulary entries",
    )
    vocab_parser.add_argument(
        "--search",
        type=str,
        help="Search vocabulary headword or alternative spellings (partial match)",
    )
    vocab_parser.add_argument(
        "--exact",
        type=str,
        help="Search vocabulary by exact headword (case-insensitive, Unicode-normalized)",
    )
    vocab_parser.add_argument(
        "--meaning",
        type=str,
        help="Search vocabulary by English meaning, translation, or gloss",
    )
    vocab_parser.add_argument(
        "--dialect",
        type=str,
        help="Filter vocabulary by dialect or village variety (e.g. Ukhrul)",
    )
    vocab_parser.add_argument(
        "--part-of-speech",
        type=str,
        help="Filter vocabulary by grammatical part of speech (e.g. noun, verb)",
    )
    vocab_parser.add_argument(
        "--source-type",
        type=str,
        help="Filter vocabulary by source type (books, songs, culture, etc.)",
    )
    vocab_parser.add_argument(
        "--verification-status",
        type=str,
        help="Filter vocabulary by verification status (verified, unverified, needs_review)",
    )
    vocab_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of results to display (default: 20)",
    )
    vocab_parser.add_argument(
        "--id",
        type=str,
        help="Display detailed metadata for a vocabulary entry ID",
    )
    vocab_parser.add_argument(
        "--mode",
        type=str,
        choices=["substring", "fulltext", "fuzzy", "phonetic"],
        default="substring",
        help="Search matching strategy: substring, fulltext (FTS5), fuzzy, or phonetic",
    )
    vocab_parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild SQLite FTS5 full-text search index from active vocabulary entries",
    )
    vocab_parser.add_argument(
        "--explain-search",
        action="store_true",
        help="Display diagnostic explanation of the search strategy and execution",
    )
    vocab_parser.add_argument(
        "--threshold",
        type=float,
        default=0.65,
        help="Similarity threshold for fuzzy matching (0.0 to 1.0, default: 0.65)",
    )
    vocab_parser.add_argument(
        "--experimental-phonetics",
        action="store_true",
        help="Enable experimental Tangkhul dialect sound shift rules in phonetic search",
    )

    # Ingest subcommand
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Permission-aware digital document and scan ingestion pipeline",
    )
    ingest_parser.add_argument(
        "--source-id",
        type=str,
        help="Manifest record identifier of the source document to ingest",
    )
    ingest_parser.add_argument(
        "--file",
        type=str,
        help="Path to local document file (PDF, TXT, MD, DOCX) to ingest",
    )
    ingest_parser.add_argument(
        "--preview",
        type=str,
        help="Preview extraction results and quality checks for a file without saving",
    )
    ingest_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate ingestion and candidate extraction without modifying database",
    )
    ingest_parser.add_argument(
        "--force",
        action="store_true",
        help="Force reprocessing even if file hash is unchanged or previously ingested",
    )
    ingest_parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List eligible and ineligible sources across manifests with explicit skip reasons",
    )
    ingest_parser.add_argument(
        "--list-documents",
        action="store_true",
        help="List all ingested documents, page counts, word counts, and extraction statuses",
    )
    ingest_parser.add_argument(
        "--report",
        type=str,
        help="Display detailed extraction, quality, and chunk report for a document ID",
    )
    ingest_parser.add_argument(
        "--search",
        type=str,
        help="Search ingested document text chunks using SQLite FTS5",
    )
    ingest_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum search results to display (default: 10)",
    )
    ingest_parser.add_argument(
        "--rebuild-chunks-index",
        action="store_true",
        help="Rebuild the FTS5 full-text index for document chunks",
    )

    # Review subcommand
    review_parser = subparsers.add_parser(
        "review",
        help="Vocabulary review, validation, community correction, and duplicate management",
    )
    review_parser.add_argument(
        "--list",
        action="store_true",
        help="List candidate vocabulary entries in review queue",
    )
    review_parser.add_argument(
        "--status",
        type=str,
        default=None,
        help="Filter review queue by status (pending_review, reviewed_uncertain, accepted, etc.)",
    )
    review_parser.add_argument(
        "--source-type",
        type=str,
        help="Filter candidates by source type (books, songs, dictionaries, culture, etc.)",
    )
    review_parser.add_argument(
        "--source-id",
        type=str,
        help="Filter candidates by source manifest identifier",
    )
    review_parser.add_argument(
        "--dialect",
        type=str,
        help="Filter candidates by dialect variety",
    )
    review_parser.add_argument(
        "--missing-meaning",
        action="store_true",
        help="Filter queue for candidates lacking verified English meanings",
    )
    review_parser.add_argument(
        "--has-duplicates",
        action="store_true",
        help="Filter queue for candidates with suggested duplicate entries",
    )
    review_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum entries to list (default: 50)",
    )
    review_parser.add_argument(
        "--show",
        type=str,
        help="Display full candidate record, source context, citations, and duplicate suggestions",
    )
    review_parser.add_argument(
        "--accept",
        type=str,
        help="Accept a candidate as verified vocabulary entry",
    )
    review_parser.add_argument(
        "--reject",
        type=str,
        help="Reject a candidate as an invalid token or non-word OCR artifact",
    )
    review_parser.add_argument(
        "--reason",
        type=str,
        help="Diagnostic explanation for rejection",
    )
    review_parser.add_argument(
        "--flag",
        type=str,
        help="Flag candidate as uncertain or having conflicting definitions",
    )
    review_parser.add_argument(
        "--edit",
        type=str,
        help="Edit linguistic metadata of a candidate entry (meaning, pos, dialect, alt spelling)",
    )
    review_parser.add_argument(
        "--link-duplicate",
        type=str,
        help="Link a candidate entry as duplicate of canonical target entry",
    )
    review_parser.add_argument(
        "--target-id",
        type=str,
        help="Target canonical entry ID when linking duplicate",
    )
    review_parser.add_argument(
        "--no-alt-spelling",
        action="store_true",
        help="Do not add candidate headword as alternative spelling when linking duplicate",
    )
    review_parser.add_argument(
        "--reviewer",
        type=str,
        help="Reviewer identifier, username, or pseudonym",
    )
    review_parser.add_argument(
        "--meaning",
        type=str,
        action="append",
        help="Confirmed meaning or translation gloss (can be specified multiple times)",
    )
    review_parser.add_argument(
        "--pos",
        type=str,
        help="Part of speech (noun, verb, adjective, etc.)",
    )
    review_parser.add_argument(
        "--alt-spelling",
        type=str,
        action="append",
        help="Alternative orthographic spelling or variant",
    )
    review_parser.add_argument(
        "--example",
        type=str,
        action="append",
        help="Example sentence illustrating usage",
    )
    review_parser.add_argument(
        "--notes",
        type=str,
        help="Reviewer notes or rationale",
    )
    review_parser.add_argument(
        "--history",
        type=str,
        help="Display review audit history for a vocabulary entry ID",
    )
    review_parser.add_argument(
        "--export",
        type=str,
        help="Export candidates to JSONL file for offline community review",
    )
    review_parser.add_argument(
        "--import-corrections",
        type=str,
        help="Import community review corrections from JSONL file",
    )
    review_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive terminal review session for candidates",
    )
    review_parser.add_argument(
        "--consensus-policy",
        action="store_true",
        help="Display current multi-reviewer consensus policy and threshold rules",
    )
    review_parser.add_argument(
        "--consensus",
        type=str,
        nargs="?",
        const="all",
        help="Evaluate multi-reviewer consensus for a vocabulary entry ID or 'all'",
    )
    review_parser.add_argument(
        "--tasks",
        action="store_true",
        help="List structured review tasks requiring validation or consensus",
    )
    review_parser.add_argument(
        "--create-tasks",
        action="store_true",
        help="Idempotently generate review tasks for unresolved candidates",
    )
    review_parser.add_argument(
        "--claim-task",
        type=str,
        help="Claim or assign a structured review task by task ID",
    )
    review_parser.add_argument(
        "--decision",
        type=str,
        choices=[
            "approve",
            "correction_requested",
            "uncertain",
            "reject",
            "flag_conflict",
            "withdraw_approval",
        ],
        help="Record a structured review decision (requires --reviewer and --entry-id)",
    )
    review_parser.add_argument(
        "--entry-id",
        type=str,
        help="Target vocabulary entry ID for recording review decision or consensus",
    )
    review_parser.add_argument(
        "--priority",
        type=str,
        choices=["high", "medium", "low"],
        help="Filter review tasks by priority level",
    )
    review_parser.add_argument(
        "--spelling-assessment",
        type=str,
        help="Linguistic assessment of orthography/spelling",
    )
    review_parser.add_argument(
        "--meaning-assessment",
        type=str,
        help="Linguistic assessment of definitions and translations",
    )
    review_parser.add_argument(
        "--pos-assessment",
        type=str,
        help="Linguistic assessment of part of speech",
    )
    review_parser.add_argument(
        "--dialect-assessment",
        type=str,
        help="Linguistic assessment of dialect classification",
    )
    review_parser.add_argument(
        "--source-assessment",
        type=str,
        help="Assessment of source citations and evidence quality",
    )
    review_parser.add_argument(
        "--conflicts",
        action="store_true",
        help="List entries with unresolved conflicting review decisions",
    )
    review_parser.add_argument(
        "--export-package",
        type=str,
        help="Export versioned review package (JSON) for offline community review",
    )
    review_parser.add_argument(
        "--validate-package",
        type=str,
        help="Validate offline review package structure, decisions, and stale conflicts",
    )
    review_parser.add_argument(
        "--import-package",
        type=str,
        help="Import and apply reviewed offline package decisions",
    )
    review_parser.add_argument(
        "--reviewer-history",
        type=str,
        help="Display review audit history recorded by a specific reviewer pseudonym",
    )
    review_parser.add_argument(
        "--metrics",
        action="store_true",
        help="Display review quality, consensus status, and governance metrics",
    )

    # Enrich subcommand
    enrich_parser = subparsers.add_parser(
        "enrich",
        help="Authorized vocabulary expansion and source-backed lexicon enrichment",
    )
    enrich_parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List eligible and ineligible sources across manifests with permission states",
    )
    enrich_parser.add_argument(
        "--source-type",
        type=str,
        help="Filter vocabulary sources by type (e.g. dictionaries, books, literature)",
    )
    enrich_parser.add_argument(
        "--dialect",
        type=str,
        help="Filter sources or specify dialect for extracted candidates",
    )
    enrich_parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview candidate extraction and quality checks for a file and source without saving",
    )
    enrich_parser.add_argument(
        "--source-id",
        type=str,
        help="Manifest record identifier of the registered source to enrich from",
    )
    enrich_parser.add_argument(
        "--file",
        type=str,
        help="Path to local document or dataset file (JSONL, TSV, CSV, TXT, MD, PDF, DOCX)",
    )
    enrich_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate enrichment, candidate creation, and category analysis without saving",
    )
    enrich_parser.add_argument(
        "--force",
        action="store_true",
        help="Force reprocessing even if file hash was previously enriched",
    )
    enrich_parser.add_argument(
        "--show-duplicates",
        action="store_true",
        help="Display detected duplicate and phonetic suggestions in enrichment output",
    )
    enrich_parser.add_argument(
        "--summary",
        action="store_true",
        help="Display summary of recent enrichment runs or last run for a source",
    )
    enrich_parser.add_argument(
        "--export-candidates",
        type=str,
        help="Export pending review candidates to JSONL for offline community review",
    )
    enrich_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum items to display in preview or source listings (default: 20)",
    )

    # Audio subcommand (Step 15)
    audio_parser = subparsers.add_parser(
        "audio",
        help="Tangkhul audio corpus, pronunciation records, and speech infrastructure",
    )
    audio_parser.add_argument(
        "action",
        nargs="?",
        choices=[
            "list",
            "inspect",
            "import",
            "validate",
            "search",
            "pronunciation",
            "permissions",
            "export",
            "summary",
        ],
        help=(
            "Audio action to execute (list, inspect, import, validate, "
            "search, pronunciation, permissions, export, summary)"
        ),
    )
    audio_parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Target ID, file path, search query, or export directory",
    )
    audio_parser.add_argument(
        "--list",
        action="store_true",
        help="List catalogued audio recordings with permission and metadata status",
    )
    audio_parser.add_argument(
        "--inspect",
        "--id",
        dest="inspect_id",
        type=str,
        help="Inspect recording metadata, speech provenance, and consent status by recording ID",
    )
    audio_parser.add_argument(
        "--import-file",
        dest="import_file",
        type=str,
        help="Import an authorized local audio file into the managed corpus",
    )
    audio_parser.add_argument(
        "--validate",
        type=str,
        help="Validate technical specs, format, and path security of an audio file",
    )
    audio_parser.add_argument(
        "--search",
        type=str,
        help="Search audio recordings by title, transcription, IPA, speaker, or dialect",
    )
    audio_parser.add_argument(
        "--pronunciation",
        type=str,
        nargs="?",
        const="",
        help="Search or inspect pronunciation records by headword or recording ID",
    )
    audio_parser.add_argument(
        "--permissions",
        type=str,
        help="Inspect or manage consent and permission records for an audio recording ID",
    )
    audio_parser.add_argument(
        "--export",
        type=str,
        help="Export authorized, verified recordings and audio manifest to destination directory",
    )
    audio_parser.add_argument(
        "--summary",
        action="store_true",
        help="Display audio corpus telemetry, dialect coverage, and permission breakdown",
    )
    audio_parser.add_argument(
        "--title",
        type=str,
        help="Descriptive title of the audio recording",
    )
    audio_parser.add_argument(
        "--vocab-id",
        type=str,
        help="Vocabulary entry identifier to link with recording or pronunciation",
    )
    audio_parser.add_argument(
        "--headword",
        type=str,
        help="Target headword to link or create pronunciation variant for",
    )
    audio_parser.add_argument(
        "--speaker",
        type=str,
        help="Speaker pseudonym or non-identifying speaker reference",
    )
    audio_parser.add_argument(
        "--dialect",
        type=str,
        help="Dialect or language variety (e.g. Ukhrul, Raphei, Champhung)",
    )
    audio_parser.add_argument(
        "--village",
        type=str,
        help="Village or locality origin",
    )
    audio_parser.add_argument(
        "--region",
        type=str,
        help="Geographic region",
    )
    audio_parser.add_argument(
        "--recording-date",
        type=str,
        help="Date when recording was made (YYYY-MM-DD)",
    )
    audio_parser.add_argument(
        "--recording-method",
        type=str,
        default="field_recording",
        help="Recording method (field_recording, studio, archival_transfer, metadata_only)",
    )
    audio_parser.add_argument(
        "--recording-source",
        type=str,
        help="Recording source or archival contributor",
    )
    audio_parser.add_argument(
        "--transcription",
        type=str,
        help="Text transcription of spoken utterance",
    )
    audio_parser.add_argument(
        "--ipa",
        type=str,
        help="IPA (International Phonetic Alphabet) transcription",
    )
    audio_parser.add_argument(
        "--transliteration",
        type=str,
        help="Pronunciation transliteration or phonetic spelling",
    )
    audio_parser.add_argument(
        "--source-citation",
        type=str,
        help="Bibliographic or archival source citation for recording",
    )
    audio_parser.add_argument(
        "--consent-status",
        type=str,
        choices=["pending", "authorized", "restricted", "withdrawn", "needs_review"],
        help="Speaker consent and clearance status",
    )
    audio_parser.add_argument(
        "--permitted-uses",
        type=str,
        help="Comma-separated permitted uses (e.g. 'linguistic_research,educational')",
    )
    audio_parser.add_argument(
        "--access-restrictions",
        type=str,
        help="Access restriction conditions or cultural protocol notes",
    )
    audio_parser.add_argument(
        "--metadata-only",
        action="store_true",
        help=(
            "Register recording as metadata-only when binary file cannot "
            "legally or ethically be stored"
        ),
    )
    audio_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate import or export without writing files or database changes",
    )
    audio_parser.add_argument(
        "--privileged",
        action="store_true",
        help=(
            "Privileged view showing unshielded paths and transcriptions "
            "for authorized custodians"
        ),
    )
    audio_parser.add_argument(
        "--include-withdrawn",
        action="store_true",
        help="Include withdrawn recordings in listings or search results",
    )
    audio_parser.add_argument(
        "--withdraw",
        action="store_true",
        help="Revoke consent for a recording ID (requires --reason)",
    )
    audio_parser.add_argument(
        "--reason",
        type=str,
        help="Reason for consent revocation or withdrawal",
    )
    audio_parser.add_argument(
        "--authorized-by",
        type=str,
        help="Custodian or community representative authorizing consent action",
    )
    audio_parser.add_argument(
        "--review-decision",
        type=str,
        choices=["approve", "reject", "flag_conflict"],
        help="Record native-speaker or reviewer validation decision on pronunciation",
    )
    audio_parser.add_argument(
        "--review-id",
        type=str,
        help="Pronunciation ID to review",
    )
    audio_parser.add_argument(
        "--reviewer",
        type=str,
        help="Reviewer pseudonym or community validator identifier",
    )
    audio_parser.add_argument(
        "--review-notes",
        type=str,
        help="Reviewer assessment notes or phonetic observations",
    )
    audio_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum results to return (default: 50)",
    )
    audio_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Result offset for pagination (default: 0)",
    )

    args = parser.parse_args(argv)

    if args.info:
        config = LibraryConfig.from_environment()
        print(f"Tangkhul Language Library v{__version__}")
        print(f"Project root:   {config.paths.root_dir}")
        print(f"Data directory: {config.paths.data_dir}")
        print(f"Manifests:      {config.paths.manifests_dir}")
        return 0

    if args.command == "books":
        from tangkhul_lib.books.library import (
            get_book,
            get_book_chapter,
            get_book_page,
            search_book_content,
        )

        if args.search_content:
            matches = search_book_content(args.search_content, book_id=args.id)
            print(f"Content search for '{args.search_content}' ({len(matches)} match(es)):")
            for m in matches:
                print(f"  [{m['book_id']}] p. {m['page_number']}: {m['snippet']}")
            return 0

        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "books.jsonl"
        catalogue = BookCatalogue.load_from_manifest(manifest_path)

        if args.id:
            full_book = get_book(args.id)
            if not full_book:
                print(f"Book with ID '{args.id}' not found in library.", file=sys.stderr)
                return 1

            if args.full:
                print("=" * 70)
                print(f"COMPLETE COVER-TO-COVER BOOK: {full_book['title']}")
                tp = full_book.get("total_pages")
                tc = full_book.get("total_chapters")
                print(f"Book ID: {full_book['id']} | Total Pages: {tp} | Chapters: {tc}")
                print("=" * 70)
                for page in full_book.get("pages", []):
                    print(f"\n--- Page {page['page_number']} [{page['page_type']}] ---")
                    print(f"Header: {page.get('header')}")
                    if page.get("title"):
                        print(f"Title:  {page['title']}")
                    print("-" * 50)
                    for line in page.get("lines", []):
                        print(f"  {line}")
                print("\n" + "=" * 70)
                print("End of complete book.")
                print("=" * 70)
                return 0

            if args.chapters:
                chapters = full_book.get("chapters", [])
                print(f"Chapters for [{args.id}] {full_book['title']} ({len(chapters)} chapters):")
                for ch in chapters:
                    num = ch["chapter_number"]
                    rng = f"{ch['page_start']}-{ch['page_end']}"
                    print(f"  Chapter {num}: {ch['title']} (pp. {rng})")
                    print(f"    Summary: {ch['summary']}")
                return 0

            if args.chapter is not None:
                ch = get_book_chapter(args.id, args.chapter)
                if not ch:
                    print(f"Chapter {args.chapter} not found in book '{args.id}'.", file=sys.stderr)
                    return 1
                rng = f"{ch['page_start']}-{ch['page_end']}"
                print("=" * 60)
                print(f"Chapter {ch['chapter_number']}: {ch['title']} (pp. {rng})")
                print(f"Summary: {ch['summary']}")
                print("-" * 60)
                print("Tangkhul Reading Text:")
                print(ch["tangkhul_text"])
                print("-" * 60)
                print("English Translation:")
                print(ch["english_translation"])
                if ch.get("vocabulary"):
                    print("-" * 60)
                    print("Vocabulary:")
                    for v in ch["vocabulary"]:
                        print(f"  * {v['word']} ({v['pos']}): {v['meaning']}")
                print("=" * 60)
                return 0

            if args.pages:
                pages = full_book.get("pages", [])
                print(f"Pages for [{args.id}] {full_book['title']} ({len(pages)} pages):")
                for p in pages:
                    t = f" - {p['title']}" if p.get("title") else ""
                    print(f"  Page {p['page_number']:>2} [{p['page_type']}]{t}")
                return 0

            if args.page is not None:
                p = get_book_page(args.id, args.page)
                if not p:
                    print(f"Page {args.page} not found in book '{args.id}'.", file=sys.stderr)
                    return 1
                print("=" * 60)
                print(f"Page {p['page_number']} [{p['page_type']}]: {p.get('header')}")
                if p.get("title"):
                    print(f"Title: {p['title']}")
                print("-" * 60)
                for line in p.get("lines", []):
                    print(line)
                print("=" * 60)
                return 0

            # Default: show detailed bibliographic metadata + chapter summary
            print("=" * 60)
            print(f"Book ID:       {full_book['id']}")
            print(f"Title:         {full_book['title']}")
            if full_book.get("alternate_titles"):
                print(f"Alternates:    {', '.join(full_book['alternate_titles'])}")
            if full_book.get("authors"):
                print(f"Authors:       {', '.join(full_book['authors'])}")
            if full_book.get("publisher"):
                print(f"Publisher:     {full_book['publisher']}")
            if full_book.get("publication_year"):
                print(f"Year:          {full_book['publication_year']}")
            if full_book.get("educational_level"):
                print(f"Level:         {full_book['educational_level']}")
            if full_book.get("subject"):
                print(f"Subject:       {full_book['subject']}")
            print(f"Total Pages:   {full_book.get('total_pages', 'N/A')}")
            num_ch = full_book.get("total_chapters", len(full_book.get("chapters", [])))
            print(f"Chapters:      {num_ch}")
            print(f"Total Words:   {full_book.get('total_words', 'N/A')}")
            perm = full_book.get("permission_status")
            acc = full_book.get("access_status")
            print(f"Permissions:   {perm} (Access: {acc})")
            print(f"Verification:  {full_book.get('verification_status')}")
            if full_book.get("notes"):
                print(f"Notes:         {full_book['notes']}")
            print("-" * 60)
            print("Chapters:")
            for ch in full_book.get("chapters", []):
                rng = f"{ch['page_start']}-{ch['page_end']}"
                print(f"  Ch. {ch['chapter_number']}: {ch['title']} (pp. {rng})")
            print("=" * 60)
            print("Tip: Use --full, --chapters, --chapter <N>, --pages, or --page <N>.")
            return 0



        if args.search:
            results = catalogue.search_books(query=args.search)
            print(f"Found {len(results)} match(es) for query '{args.search}':")
            for b in results:
                yr = f"({b.publication_year})" if b.publication_year else ""
                lvl = f"[{b.educational_level}]" if b.educational_level else ""
                print(f"  - [{b.id}] {b.title} {lvl} {yr}")
            return 0

        if args.list:
            books = catalogue.list_books()
            print(f"Tangkhul Books Catalogue ({len(books)} entries):")
            for b in books:
                yr = f"({b.publication_year})" if b.publication_year else ""
                lvl = f"[{b.educational_level}]" if b.educational_level else ""
                print(f"  - [{b.id:<11}] {b.title:<36} {lvl:<18} {yr}")
            return 0

        books_parser.print_help()
        return 0

    if args.command == "songs":
        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "songs.jsonl"
        catalogue = SongCatalogue.load_from_manifest(manifest_path)

        if args.id:
            song = catalogue.get_song(args.id)
            if not song:
                print(f"Song with ID '{args.id}' not found in catalogue.", file=sys.stderr)
                return 1
            print("=" * 60)
            print(f"Song ID:       {song.id}")
            print(f"Title:         {song.title}")
            if song.alternate_titles:
                print(f"Alternates:    {', '.join(song.alternate_titles)}")
            if song.title_translation:
                print(f"Translation:   {song.title_translation}")
            if song.singer:
                print(f"Singer:        {song.singer}")
            if song.lyricist:
                print(f"Lyricist:      {song.lyricist}")
            if song.composer:
                print(f"Composer:      {song.composer}")
            if song.collector:
                print(f"Collector:     {song.collector}")
            if song.year:
                print(f"Year:          {song.year}")
            if song.song_type:
                print(f"Genre/Type:    {song.song_type}")
            if song.village:
                print(f"Village:       {song.village}")
            if song.dialect:
                print(f"Dialect:       {song.dialect}")
            if song.source_url:
                print(f"Source URL:    {song.source_url}")
            print(f"Permissions:   {song.permission_status} (Access: {song.access_status})")
            print(f"Verification:  {song.verification_status}")
            if song.notes:
                print(f"Notes:         {song.notes}")
            if getattr(args, "lyrics", False) or getattr(args, "full", False):
                stanzas = get_song_lyrics(song.id)
                print("-" * 60)
                print(f"LYRICS & TRANSLATIONS ({len(stanzas)} stanza(s)):")
                for s in stanzas:
                    st_num = s.get("stanza_number", 1)
                    print(f"\n[Stanza {st_num}]")
                    for tk, en in zip(
                        s.get("lines_tangkhul", []),
                        s.get("lines_translation", []),
                        strict=False,
                    ):
                        print(f"  Tangkhul: {tk}")
                        print(f"  English:  {en}")
            print("=" * 60)
            return 0

        if args.search or args.type or args.singer or args.village:
            results = catalogue.search_songs(
                query=args.search,
                song_type=args.type,
                singer=args.singer,
                village=args.village,
            )
            print(f"Found {len(results)} matching song(s):")
            for s in results:
                singer_str = f"({s.singer})" if s.singer else ""
                type_str = f"[{s.song_type}]" if s.song_type else ""
                vil_str = f"<{s.village}>" if s.village else ""
                print(f"  - [{s.id:<12}] {s.title:<32} {type_str:<12} {singer_str} {vil_str}")
            return 0

        if args.list:
            songs = catalogue.list_songs()
            print(f"Tangkhul Songs Catalogue ({len(songs)} entries):")
            for s in songs:
                singer_str = f"({s.singer})" if s.singer else ""
                type_str = f"[{s.song_type}]" if s.song_type else ""
                print(f"  - [{s.id:<12}] {s.title:<34} {type_str:<12} {singer_str}")
            return 0

        songs_parser.print_help()
        return 0

    if args.command == "dictionaries":
        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "dictionaries.jsonl"
        catalogue = DictionaryCatalogue.load_from_manifest(manifest_path)

        # Connect to DB if available to load imported entries
        db_path = config.paths.data_dir / "database" / "tangkhul_corpus.sqlite"
        if db_path.is_file():
            from tangkhul_lib.storage.database import DatabaseManager
            from tangkhul_lib.storage.repositories import DictionaryRepository

            db_manager = DatabaseManager(db_path)
            dict_repo = DictionaryRepository(db_manager)
            for src in catalogue.list_sources():
                for ent in dict_repo.list_entries_by_dictionary(src.id):
                    catalogue.add_entry(ent)

        if args.id:
            src = catalogue.get_source(args.id)
            if not src:
                print(f"Dictionary with ID '{args.id}' not found in catalogue.", file=sys.stderr)
                return 1
            print("=" * 60)
            print(f"Dictionary ID: {src.id}")
            print(f"Title:         {src.title}")
            if src.alternate_titles:
                print(f"Alternates:    {', '.join(src.alternate_titles)}")
            if src.authors:
                print(f"Authors:       {', '.join(src.authors)}")
            if src.compiler:
                print(f"Compiler:      {src.compiler}")
            if src.publisher:
                print(f"Publisher:     {src.publisher}")
            if src.publication_year:
                print(f"Year:          {src.publication_year}")
            if src.language_pair:
                print(f"Language Pair: {src.language_pair}")
            if src.dialect:
                print(f"Dialect:       {src.dialect}")
            if src.source_type:
                print(f"Source Type:   {src.source_type}")
            if src.source_url:
                print(f"Source URL:    {src.source_url}")
            print(f"Permissions:   {src.permission_status} (Access: {src.access_status})")
            print(f"Verification:  {src.verification_status}")
            if src.notes:
                print(f"Notes:         {src.notes}")
            print("=" * 60)
            return 0

        if args.entry:
            entries = catalogue.search_entries(headword=args.entry)
            print(f"Found {len(entries)} lexical entry match(es) for headword '{args.entry}':")
            for ent in entries:
                all_defs = ent.definitions_en or ent.definitions_hi or ent.other_definitions
                defs = "; ".join(all_defs)
                pos = f"[{ent.part_of_speech}]" if ent.part_of_speech else ""
                line_str = (
                    f"  - [{ent.id:<14}] {ent.headword:<12} {pos:<6} {defs} ({ent.dictionary_id})"
                )
                print(line_str)
            return 0

        filter_applied = (
            args.search
            or args.language_pair
            or args.author
            or args.dialect
            or args.verification_status
        )
        if filter_applied:
            results = catalogue.search_sources(
                query=args.search,
                author=args.author,
                language_pair=args.language_pair,
                dialect=args.dialect,
                verification_status=args.verification_status,
            )
            print(f"Found {len(results)} matching dictionary source(s):")
            for s in results:
                yr = f"({s.publication_year})" if s.publication_year else ""
                lp = f"[{s.language_pair}]" if s.language_pair else f"[{s.source_type}]"
                creators = s.authors or ([s.compiler] if s.compiler else [])
                auth = f"({', '.join(creators)})" if creators else ""
                print(f"  - [{s.id:<14}] {s.title:<40} {lp:<24} {auth} {yr}")
            return 0

        if args.list:
            sources = catalogue.list_sources()
            print(f"Tangkhul Dictionaries Catalogue ({len(sources)} entries):")
            for s in sources:
                yr = f"({s.publication_year})" if s.publication_year else ""
                st = f"[{s.source_type}]"
                print(f"  - [{s.id:<14}] {s.title:<45} {st:<20} {yr}")
            return 0

        dict_parser.print_help()
        return 0

    if args.command == "culture":
        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "culture.jsonl"
        catalogue = CultureCatalogue.load_from_manifest(manifest_path)

        if args.id:
            rec = catalogue.get_record(args.id)
            if not rec:
                print(
                    f"Cultural record with ID '{args.id}' not found in catalogue.",
                    file=sys.stderr,
                )
                return 1
            print("=" * 60)
            print(f"Record ID:     {rec.id}")
            print(f"Title:         {rec.title}")
            if rec.local_name and rec.local_name != rec.title:
                print(f"Local Name:    {rec.local_name}")
            if rec.alternate_names:
                print(f"Alternates:    {', '.join(rec.alternate_names)}")
            cat_label = f"{rec.category} ({rec.subcategory})" if rec.subcategory else rec.category
            print(f"Category:      {cat_label}")
            if rec.original_text:
                print(f"Original Text: {rec.original_text}")
            if rec.translation_en:
                print(f"Translation:   {rec.translation_en}")
            if rec.village:
                print(f"Village:       {rec.village}")
            if rec.dialect:
                print(f"Dialect:       {rec.dialect}")
            if rec.season_or_timing:
                print(f"Timing/Season: {rec.season_or_timing}")
            if rec.contributor:
                print(f"Contributor:   {rec.contributor}")
            if rec.year:
                print(f"Year:          {rec.year}")
            if rec.source_id or rec.source_title:
                src_info = rec.source_title or rec.source_id
                print(f"Source:        {src_info}")
            if rec.source_url:
                print(f"Source URL:    {rec.source_url}")
            print(f"Permissions:   {rec.permission_status} (Access: {rec.access_status})")
            print(f"Verification:  {rec.verification_status}")
            if rec.notes:
                print(f"Notes:         {rec.notes}")
            print("=" * 60)
            return 0

        filter_applied = (
            args.search
            or args.category
            or args.village
            or args.dialect
            or args.verification_status
        )
        if filter_applied:
            results = catalogue.search_records(
                query=args.search,
                category=args.category,
                village=args.village,
                dialect=args.dialect,
                verification_status=args.verification_status,
            )
            print(f"Found {len(results)} matching cultural record(s):")
            for r in results:
                cat_str = f"[{r.category}]"
                vil_str = f"<{r.village}>" if r.village else ""
                print(f"  - [{r.id:<14}] {r.title:<42} {cat_str:<16} {vil_str}")
            return 0

        if args.list:
            records = catalogue.list_records()
            print(f"Tangkhul Culture Catalogue ({len(records)} entries):")
            for r in records:
                cat_str = f"[{r.category}]"
                ver_str = f"({r.verification_status})"
                print(f"  - [{r.id:<14}] {r.title:<42} {cat_str:<16} {ver_str}")
            return 0

        culture_parser.print_help()
        return 0

    if args.command == "history":
        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "history.jsonl"
        catalogue = HistoryCatalogue.load_from_manifest(manifest_path)

        if args.id:
            rec = catalogue.get_record(args.id)
            if not rec:
                print(
                    f"Historical record with ID '{args.id}' not found in catalogue.",
                    file=sys.stderr,
                )
                return 1
            print("=" * 60)
            print(f"Record ID:     {rec.id}")
            print(f"Title:         {rec.title}")
            if rec.alternate_titles:
                print(f"Alternates:    {', '.join(rec.alternate_titles)}")
            print(f"Record Type:   {rec.record_type}")
            if rec.event_date:
                print(f"Event Date:    {rec.event_date}")
            if rec.sort_year:
                print(f"Sort Year:     {rec.sort_year}")
            if rec.period:
                print(f"Period:        {rec.period}")
            if rec.place:
                print(f"Place:         {rec.place}")
            if rec.village:
                print(f"Village:       {rec.village}")
            if rec.people_involved:
                print(f"People:        {', '.join(rec.people_involved)}")
            if rec.summary:
                print(f"Summary:       {rec.summary}")
            if rec.original_text:
                print(f"Original Text: {rec.original_text}")
            if rec.translation_en:
                print(f"Translation:   {rec.translation_en}")
            if rec.related_events:
                print(f"Related Evts:  {', '.join(rec.related_events)}")
            if rec.related_records:
                print(f"Related Recs:  {', '.join(rec.related_records)}")
            if rec.contradictory_accounts:
                print(f"Conflicts:     {'; '.join(rec.contradictory_accounts)}")
            if rec.source_id or rec.source_title:
                src_info = rec.source_title or rec.source_id
                if rec.source_page:
                    src_info = f"{src_info} (p. {rec.source_page})"
                print(f"Source:        {src_info}")
            if rec.source_url:
                print(f"Source URL:    {rec.source_url}")
            print(f"Evidence:      {rec.evidence_type} (Confidence: {rec.confidence})")
            print(f"Permissions:   {rec.permission_status} (Access: {rec.access_status})")
            print(f"Verification:  {rec.verification_status}")
            if rec.notes:
                print(f"Notes:         {rec.notes}")
            print("=" * 60)
            return 0

        filter_applied = (
            args.search
            or args.type
            or args.period
            or args.place
            or args.verification_status
        )
        if filter_applied:
            results = catalogue.search_records(
                query=args.search,
                record_type=args.type,
                period=args.period,
                place=args.place,
                verification_status=args.verification_status,
            )
            print(f"Found {len(results)} matching historical record(s):")
            for r in results:
                type_str = f"[{r.record_type}]"
                date_str = f"({r.event_date or r.sort_year or 'Undated'})"
                plc_str = f"<{r.place}>" if r.place else ""
                print(
                    f"  - [{r.id:<14}] {r.title:<38} {type_str:<18} {date_str:<12} {plc_str}"
                )
            return 0

        if args.list:
            records = catalogue.list_records(sort_by_date=True)
            print(f"Tangkhul History Catalogue ({len(records)} entries):")
            for r in records:
                type_str = f"[{r.record_type}]"
                date_str = f"({r.event_date or r.sort_year or 'Undated'})"
                ver_str = f"({r.verification_status})"
                print(
                    f"  - [{r.id:<14}] {r.title:<38} {type_str:<18} {date_str:<12} {ver_str}"
                )
            return 0

        history_parser.print_help()
        return 0

    if args.command == "literature":
        config = LibraryConfig.from_environment()
        manifest_path = config.paths.manifests_dir / "literature.jsonl"
        catalogue = LiteratureCatalogue.load_from_manifest(manifest_path)

        if args.id:
            work = catalogue.get_work(args.id)
            if not work:
                print(
                    f"Literary work with ID '{args.id}' not found in catalogue.",
                    file=sys.stderr,
                )
                return 1
            print("=" * 60)
            print(f"Work ID:       {work.id}")
            print(f"Title:         {work.title}")
            if work.alternate_titles:
                print(f"Alternates:    {', '.join(work.alternate_titles)}")
            if work.original_title:
                print(f"Tangkhul Title:{work.original_title}")
            if work.title_translation:
                print(f"English Title: {work.title_translation}")
            print(f"Work Type:     {work.work_type}")
            if work.genres:
                print(f"Genres:        {', '.join(work.genres)}")
            if work.author:
                print(f"Author:        {work.author}")
            if work.poet:
                print(f"Poet:          {work.poet}")
            if work.storyteller:
                print(f"Storyteller:   {work.storyteller}")
            if work.playwright:
                print(f"Playwright:    {work.playwright}")
            if work.translator:
                print(f"Translator:    {work.translator}")
            if work.editor:
                print(f"Editor:        {work.editor}")
            if work.collector:
                print(f"Collector:     {work.collector}")
            if work.publication_year:
                print(f"Year:          {work.publication_year}")
            if work.composition_date:
                print(f"Composition:   {work.composition_date}")
            if work.edition:
                print(f"Edition:       {work.edition}")
            if work.publisher:
                print(f"Publisher:     {work.publisher}")
            if work.language:
                print(f"Language:      {work.language}")
            if work.dialect:
                print(f"Dialect:       {work.dialect}")
            if work.village:
                print(f"Village:       {work.village}")
            if work.book_id:
                print(f"Parent Book:   {work.book_id}")
            if work.collection:
                print(f"Collection:    {work.collection}")
            if work.source_title or work.source_id:
                src = work.source_title or work.source_id
                if work.source_page:
                    src = f"{src} (p. {work.source_page})"
                print(f"Source:        {src}")
            if work.source_url:
                print(f"Source URL:    {work.source_url}")
            print(f"Permissions:   {work.permission_status} (Access: {work.access_status})")
            print(f"Verification:  {work.verification_status}")
            print(f"Text Avail:    {work.text_availability}")
            if work.notes:
                print(f"Notes:         {work.notes}")
            print("=" * 60)
            return 0

        filter_applied = (
            args.search
            or args.type
            or args.genre
            or args.author
            or args.language
            or args.verification_status
        )
        if filter_applied:
            results = catalogue.search_works(
                query=args.search,
                work_type=args.type,
                genre=args.genre,
                author=args.author,
                language=args.language,
                verification_status=args.verification_status,
            )
            print(f"Found {len(results)} matching literary work(s):")
            for w in results:
                type_str = f"[{w.work_type}]"
                yr_str = f"({w.publication_year or 'Undated'})"
                creator = w.author or w.poet or w.storyteller or w.playwright or ""
                auth_str = f"by {creator}" if creator else ""
                print(f"  - [{w.id:<14}] {w.title:<38} {type_str:<18} {yr_str:<10} {auth_str}")
            return 0

        if args.list:
            works = catalogue.list_works(sort_by_year=True)
            print(f"Tangkhul Literature Catalogue ({len(works)} entries):")
            for w in works:
                type_str = f"[{w.work_type}]"
                yr_str = f"({w.publication_year or 'Undated'})"
                ver_str = f"({w.verification_status})"
                print(f"  - [{w.id:<14}] {w.title:<38} {type_str:<18} {yr_str:<10} {ver_str}")
            return 0

        literature_parser.print_help()
        return 0

    if args.command == "vocab":
        from tangkhul_lib.vocabulary.search import (
            format_search_explanation,
            format_vocabulary_entry,
            load_unified_vocabulary_engine,
        )

        if args.limit is not None and args.limit <= 0:
            print("Error: --limit must be a positive integer.", file=sys.stderr)
            return 2

        if args.threshold is not None and not (0.0 <= args.threshold <= 1.0):
            print("Error: --threshold must be a float between 0.0 and 1.0.", file=sys.stderr)
            return 2

        valid_source_types = {
            "books",
            "songs",
            "dictionaries",
            "culture",
            "history",
            "literature",
            "book",
            "song",
            "dictionary",
            "cultural",
            "historical",
            "literary",
        }
        if args.source_type and args.source_type.strip().lower() not in valid_source_types:
            print(
                f"Error: Invalid --source-type '{args.source_type}'. "
                "Allowed types: books, songs, dictionaries, culture, history, literature.",
                file=sys.stderr,
            )
            return 2

        valid_verification_statuses = {
            "verified",
            "unverified",
            "needs_review",
            "partially_verified",
            "community_reviewed",
        }
        if (
            args.verification_status
            and args.verification_status.strip().lower() not in valid_verification_statuses
        ):
            print(
                f"Error: Invalid --verification-status '{args.verification_status}'. "
                "Allowed statuses: verified, unverified, needs_review, "
                "partially_verified, community_reviewed.",
                file=sys.stderr,
            )
            return 2

        config = LibraryConfig.from_environment()
        engine = load_unified_vocabulary_engine(config)

        if args.rebuild_index:
            if (
                args.search
                or args.exact
                or args.meaning
                or args.id
                or args.list
            ):
                print(
                    "Error: --rebuild-index cannot be combined with search queries "
                    "or entry display options.",
                    file=sys.stderr,
                )
                return 2

            if not engine.repository:
                print(
                    "Error: No database repository available for rebuilding index.",
                    file=sys.stderr,
                )
                return 1

            if not engine.repository.is_fts5_available():
                print(
                    "Warning: SQLite FTS5 extension is not available in the current environment.",
                    file=sys.stderr,
                )
                print("FTS5 full-text index could not be built.", file=sys.stderr)
                return 1

            count = engine.repository.rebuild_fts_index()
            print(f"FTS5 full-text search index rebuilt successfully ({count} records indexed).")
            return 0

        if args.id:
            entry = engine.repository.get_by_id(args.id) if engine.repository else None
            if not entry:
                print(f"Vocabulary entry with ID '{args.id}' not found.", file=sys.stderr)
                return 1
            print(format_vocabulary_entry(entry, manifest_repo=engine.manifest_repository))
            return 0

        if args.mode in {"fulltext", "fuzzy", "phonetic"} and not (
            args.search or args.meaning
        ):
            print(
                f"Error: Search mode '{args.mode}' requires a query term "
                "via --search or --meaning.",
                file=sys.stderr,
            )
            return 2

        has_query_or_filter = (
            args.search
            or args.exact
            or args.meaning
            or args.dialect
            or args.part_of_speech
            or args.source_type
            or args.verification_status
            or args.list
            or args.explain_search
        )
        if not has_query_or_filter:
            vocab_parser.print_help()
            return 0

        results, matches_info, explanation = engine.search_with_matches(
            headword=args.search,
            exact_headword=args.exact,
            meaning=args.meaning,
            dialect=args.dialect,
            part_of_speech=args.part_of_speech,
            source_type=args.source_type,
            verification_status=args.verification_status,
            limit=args.limit,
            mode=args.mode,
            threshold=args.threshold,
            include_experimental_phonetics=args.experimental_phonetics,
        )

        if args.explain_search:
            print(format_search_explanation(explanation))

        if not results:
            print("No vocabulary entries found matching the specified criteria.")
            return 0

        print(f"Found {len(results)} matching vocabulary entry/entries:")
        for e in results:
            match_info = matches_info.get(e.id)
            match_to_show = (
                match_info
                if (args.mode in {"fuzzy", "phonetic", "fulltext"} or args.explain_search)
                else None
            )
            print(
                format_vocabulary_entry(
                    e,
                    manifest_repo=engine.manifest_repository,
                    match=match_to_show,
                )
            )
        return 0

    if args.command == "ingest":
        from pathlib import Path

        from tangkhul_lib.ingestion.pipeline import DocumentIngestionPipeline
        from tangkhul_lib.storage.database import DatabaseManager

        config = LibraryConfig.from_environment()
        db_file = config.paths.database_dir / config.sqlite_db_name
        db_manager = DatabaseManager(db_file)
        db_manager.initialize_schema()
        pipeline = DocumentIngestionPipeline(db_manager, config=config)

        if args.list_sources:
            eligible, ineligible = pipeline.evaluate_all_sources()
            print("=" * 65)
            print("DOCUMENT INGESTION SOURCE ELIGIBILITY REPORT:")
            print(f"Total Sources Inspected: {len(eligible) + len(ineligible)}")
            print(f"Eligible for Ingestion:  {len(eligible)}")
            print(f"Ineligible / Skipped:    {len(ineligible)}")
            print("=" * 65)

            if eligible:
                print("\n[ELIGIBLE SOURCES] (Authorized permission tier, verified metadata):")
                for s in eligible:
                    has_file_str = "File Present" if s["has_local_file"] else "File Missing"
                    print(
                        f"  + [{s['source_id']:<14}] {s['title'][:30]:<32} "
                        f"({s['permission_status']}) [{has_file_str}]"
                    )

            if ineligible:
                print("\n[INELIGIBLE / SKIPPED SOURCES] (Explicit reason documented):")
                for s in ineligible:
                    print(
                        f"  - [{s['source_id']:<14}] {s['title'][:30]:<32} "
                        f"({s['permission_status']})"
                    )
                    print(f"      Reason: {s['skip_reason']}")
            return 0

        if args.preview:
            p_path = Path(args.preview)
            if not p_path.is_file():
                print(f"Error: Preview file not found: {p_path}", file=sys.stderr)
                return 1
            preview_data = pipeline.preview_document(p_path, source_id=args.source_id or "")
            print("=" * 65)
            print("DOCUMENT EXTRACTION PREVIEW (DRY RUN):")
            print(f"  File:               {preview_data['file_name']}")
            print(f"  Format:             {preview_data['file_format']}")
            print(f"  SHA-256:            {preview_data['file_hash']}")
            print(f"  Size:               {preview_data['file_size_bytes']} bytes")
            print(f"  Method:             {preview_data['extraction_method']}")
            print(f"  Status:             {preview_data['status']}")
            print(f"  OCR Status:         {preview_data['ocr_status']}")
            print(f"  Pages Detected:     {preview_data['page_count']}")
            print(
                f"  Words / Characters: {preview_data['word_count']} words, "
                f"{preview_data['char_count']} chars"
            )
            print(f"  Paragraph Chunks:   {preview_data['chunk_count']}")
            if preview_data.get("warnings"):
                print("  Warnings:")
                for w in preview_data["warnings"]:
                    print(f"    ! {w}")
            if preview_data.get("notes"):
                print(f"  Notes:              {preview_data['notes']}")
            print("=" * 65)
            if preview_data.get("sample_chunks"):
                print("\nSample Paragraph Chunks:")
                for sc in preview_data["sample_chunks"]:
                    p_info = f"p. {sc['page']}" if sc.get("page") else "no page"
                    print(f"  [{sc['id']}] ({p_info}, {sc['words']} words):")
                    print(f"    \"{sc['text']}\"")
            return 0

        if args.rebuild_chunks_index:
            if not pipeline.doc_repo.is_fts5_available():
                print("Warning: SQLite FTS5 extension is not available.", file=sys.stderr)
                return 1
            count = pipeline.doc_repo.rebuild_chunks_fts_index()
            print(f"Document chunks FTS5 index rebuilt successfully ({count} chunks indexed).")
            return 0

        if args.list_documents:
            docs = pipeline.doc_repo.list_documents()
            print("=" * 65)
            print(f"Ingested Documents ({len(docs)} document(s)):")
            print("=" * 65)
            if not docs:
                print("No documents have been ingested yet.")
                return 0
            for d in docs:
                print(f"  - [{d.id:<22}] Source: {d.source_id:<14} ({d.file_format.upper()})")
                print(f"      Title:    {d.source_title}")
                print(f"      Status:   {d.extraction_status} (OCR: {d.ocr_status})")
                print(
                    f"      Metrics:  {d.page_count} page(s), {d.word_count} words, "
                    f"{d.char_count} chars"
                )
                if d.extraction_warnings:
                    print(f"      Warnings: {', '.join(d.extraction_warnings[:2])}")
            return 0

        if args.report:
            doc = pipeline.doc_repo.get_document(args.report)
            if not doc:
                doc = pipeline.doc_repo.get_document_by_source_id(args.report)
            if not doc:
                print(
                    f"Error: Document with ID or Source ID '{args.report}' not found.",
                    file=sys.stderr,
                )
                return 1
            chunks = pipeline.doc_repo.get_chunks(doc.id)
            print("=" * 65)
            print("DOCUMENT INGESTION & EXTRACTION REPORT:")
            print(f"  Document ID:        {doc.id}")
            print(f"  Source ID:          {doc.source_id}")
            print(f"  Source Title:       {doc.source_title}")
            print(f"  Creator:            {doc.creator or 'Not recorded'}")
            print(f"  Year:               {doc.publication_year or 'Not recorded'}")
            print(f"  File Path:          {doc.file_path}")
            print(f"  File SHA-256:       {doc.file_hash}")
            print(f"  Format / Method:    {doc.file_format} / {doc.extraction_method}")
            print(f"  Status / OCR:       {doc.extraction_status} / {doc.ocr_status}")
            print(
                f"  Permissions:        {doc.permission_status} "
                f"(Verification: {doc.verification_status})"
            )
            print(f"  Review Status:      {doc.review_status}")
            print(f"  Pages / Chunks:     {doc.page_count} pages, {len(chunks)} paragraph chunks")
            print(f"  Words / Characters: {doc.word_count} words, {doc.char_count} chars")
            if doc.extraction_warnings:
                print("  Warnings:")
                for w in doc.extraction_warnings:
                    print(f"    ! {w}")
            if doc.notes:
                print(f"  Notes:              {doc.notes}")
            print("=" * 65)
            return 0

        if args.search:
            results = pipeline.doc_repo.search_chunks_fts(args.search, limit=args.limit)
            if not results:
                print(f"No document text chunks found matching query '{args.search}'.")
                return 0
            print(f"Found {len(results)} matching document paragraph chunk(s):")
            for chunk, rank in results:
                p_str = f"Page {chunk.page_number}" if chunk.page_number else "No page"
                print("=" * 65)
                print(f"Chunk ID:   {chunk.id} (Source: {chunk.source_id}, {p_str})")
                print(f"BM25 Rank:  {rank:.3f}")
                if chunk.section_heading:
                    print(f"Section:    {chunk.section_heading}")
                print(f"Text:       \"{chunk.text}\"")
            print("=" * 65)
            return 0

        if args.source_id:
            res = pipeline.ingest_document(
                source_id=args.source_id,
                file_path=args.file,
                force=args.force,
                dry_run=args.dry_run,
            )
            if not res.get("success"):
                if res.get("skipped"):
                    print(f"Ingestion skipped for '{args.source_id}': {res.get('reason')}")
                    return 0
                print(
                    f"Error ingesting '{args.source_id}': {res.get('error')}",
                    file=sys.stderr,
                )
                return 1

            if res.get("already_ingested"):
                print(f"Notice: {res.get('message')}")
                print(
                    f"Document ID: {res.get('document_id')} "
                    f"({res.get('page_count')} pages, {res.get('word_count')} words)"
                )
                return 0

            dry_str = " (DRY RUN)" if res.get("dry_run") else ""
            print("=" * 65)
            print(f"DOCUMENT INGESTION SUCCESSFUL{dry_str}:")
            print(f"  Source ID:              {res['source_id']}")
            print(f"  Document ID:            {res['document_id']}")
            print(f"  File Path:              {res['file_path']}")
            print(
                f"  Pages / Chunks:         {res['page_count']} pages, "
                f"{res['chunk_count']} chunks"
            )
            print(f"  Words / Characters:     {res['word_count']} words, {res['char_count']} chars")
            print(f"  Tokens Harvested:       {res['tokens_extracted']}")
            if not res.get("dry_run"):
                print(f"  Vocabulary Integrated:  {res['vocabulary_integrated']}")
            if res.get("warnings"):
                print("  Warnings:")
                for w in res["warnings"]:
                    print(f"    ! {w}")
            print("=" * 65)
            return 0

        ingest_parser.print_help()
        return 0

    if args.command == "review":
        from tangkhul_lib.vocabulary.review import VocabularyReviewService

        config = LibraryConfig.from_environment()
        service = VocabularyReviewService.from_config(config)

        if args.consensus_policy:
            pol = service.policy
            print("=" * 65)
            print("MULTI-REVIEWER CONSENSUS POLICY CONFIGURATION:")
            print("=" * 65)
            print(f"  Policy Version:            {pol.policy_version}")
            print(f"  Required Approvals:        {pol.required_approvals} independent reviewer(s)")
            print(
                "  Single Reviewer Exception: "
                f"{'Enabled' if pol.allow_single_reviewer_exception else 'Disabled'}"
            )
            print(
                "  Source Evidence Required:  "
                f"{'Yes' if pol.require_source_clearance else 'No'}"
            )
            elig_str = (
                ", ".join(pol.eligible_reviewers)
                if pol.eligible_reviewers is not None
                else "Unrestricted (all non-empty pseudonyms)"
            )
            print(f"  Eligible Reviewers Roster: {elig_str}")
            print("=" * 65)
            return 0

        if args.metrics:
            m = service.get_review_metrics()
            print("=" * 65)
            print("TANGKHUL VOCABULARY REVIEW QUALITY & GOVERNANCE METRICS:")
            print("=" * 65)
            print(f"  Total Library Entries:       {m['total_entries']}")
            print(f"  Candidates Awaiting Review:  {m['total_candidates']}")
            print(f"  Entries Meeting Consensus:   {m['entries_meeting_consensus']}")
            print(f"  Entries with Active Reviews: {m['entries_with_reviews']}")
            print(f"  Entries with Conflicts:      {m['entries_with_conflicts']}")
            print(f"  Entries Needing Correction:  {m['entries_awaiting_corrections']}")
            print(f"  Entries Lacking Provenance:  {m['entries_lacking_source_evidence']}")
            print(f"  Blocked by Copyright/Access: {m['entries_blocked_by_permissions']}")
            print("\n  Structured Review Tasks:")
            ts = m["tasks"]
            print(f"    Open:                 {ts['open']}")
            print(f"    In Review:            {ts['in_review']}")
            print(f"    Completed:            {ts['completed']}")
            print(f"    Conflicted:           {ts['conflict']}")
            print(f"    Correction Requested: {ts['correction_requested']}")
            print(f"    Total Tasks:          {ts['total_tasks']}")
            if m.get("average_review_time_seconds") is not None:
                print(
                    f"\n  Average Review Completion Time: {m['average_review_time_seconds']:.1f}s"
                )
            if m.get("reviewer_activity"):
                print("\n  Review Activity by Contributor / Pseudonym:")
                for rev, count in sorted(
                    m["reviewer_activity"].items(), key=lambda x: x[1], reverse=True
                ):
                    print(f"    * {rev:<24} : {count} decision(s)")
            print("=" * 65)
            return 0

        if args.conflicts:
            confs = service.get_unresolved_conflicts(limit=args.limit)
            print("=" * 65)
            print(f"UNRESOLVED VOCABULARY CONFLICTS ({len(confs)} entries found):")
            print("=" * 65)
            if not confs:
                print("No unresolved conflicting review decisions.")
                return 0
            for c in confs:
                print(
                    f"  - [{c['entry_id']}] '{c['headword']}' "
                    f"(Dialect: {c['dialect'] or 'Standard'})"
                )
                print(
                    f"      Meanings: {', '.join(c['meanings']) if c['meanings'] else '(None)'}"
                )
                print("      Review Decisions:")
                for r in c["review_history"]:
                    note_str = f" - Note: {r['notes']}" if r.get("notes") else ""
                    print(f"        * {r['decision'].upper()} by {r['reviewer']}{note_str}")
            print("=" * 65)
            return 0

        if args.reviewer_history:
            history = service.review_repo.list_reviews_by_reviewer(args.reviewer_history)
            print("=" * 65)
            print(
                f"REVIEW DECISION HISTORY FOR REVIEWER '{args.reviewer_history}' "
                f"({len(history)} decision(s)):"
            )
            print("=" * 65)
            if not history:
                print(f"No review decisions recorded for reviewer '{args.reviewer_history}'.")
                return 0
            for rev in history:
                ts = rev.review_timestamp or "Timestamp not recorded"
                counts_str = (
                    " [Counts for consensus]"
                    if rev.counts_for_consensus
                    else " [Excluded from consensus]"
                )
                note_str = f" — Note: {rev.notes}" if rev.notes else ""
                print(
                    f"  * [{ts}] Entry: {rev.entry_id} ('{rev.headword}') -> "
                    f"{rev.decision.upper()}{counts_str}{note_str}"
                )
            print("=" * 65)
            return 0

        if args.create_tasks:
            created = service.create_review_tasks(limit=args.limit)
            print("=" * 65)
            print(f"STRUCTURED REVIEW TASK GENERATION ({len(created)} task(s) created):")
            print("=" * 65)
            if not created:
                print("All eligible entries already have open review tasks or are verified.")
                return 0
            for t in created:
                print(
                    f"  - [{t.id:<24}] Priority: {t.priority.upper():<6} "
                    f"Type: {t.task_type:<18} Headword: '{t.headword}'"
                )
                print(f"      Reason: {t.reason}")
            print("=" * 65)
            return 0

        if args.tasks:
            task_list = service.list_tasks(
                status=args.status,
                priority=args.priority,
                assigned_reviewer=args.reviewer,
                limit=args.limit,
            )
            print("=" * 65)
            print(f"STRUCTURED REVIEW TASKS ({len(task_list)} task(s) listed):")
            print("=" * 65)
            if not task_list:
                print("No review tasks matching the specified criteria.")
                return 0
            for t in task_list:
                assigned = (
                    f" (Assigned: {t.assigned_reviewer})"
                    if t.assigned_reviewer
                    else " (Unassigned)"
                )
                print(
                    f"  - [{t.id:<24}] Status: {t.status:<12} "
                    f"Priority: {t.priority.upper():<6} '{t.headword}'{assigned}"
                )
                print(f"      Dimensions: {', '.join(t.review_dimensions)} | Reason: {t.reason}")
            print("=" * 65)
            return 0

        if args.claim_task:
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier or pseudonym is required to claim a task.",
                    file=sys.stderr,
                )
                return 1
            try:
                task = service.claim_task(task_id=args.claim_task, reviewer=args.reviewer)
                print(
                    f"Success: Task '{task.id}' claimed by '{task.assigned_reviewer}'. "
                    f"Status: {task.status}"
                )
                return 0
            except Exception as err:
                print(f"Error claiming task '{args.claim_task}': {err}", file=sys.stderr)
                return 1

        if args.decision:
            entry_id = (
                args.entry_id
                or args.show
                or args.accept
                or args.reject
                or args.flag
                or args.edit
            )
            if not entry_id:
                print(
                    "Error: --entry-id is required when recording a review decision.",
                    file=sys.stderr,
                )
                return 1
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier or pseudonym is required.",
                    file=sys.stderr,
                )
                return 1
            try:
                rec, eval_res = service.record_decision(
                    entry_id=entry_id,
                    reviewer=args.reviewer,
                    decision=args.decision,
                    spelling_assessment=args.spelling_assessment,
                    meaning_assessment=args.meaning_assessment,
                    pos_assessment=args.pos_assessment,
                    dialect_assessment=args.dialect_assessment,
                    source_assessment=args.source_assessment,
                    notes=args.notes,
                    auto_evaluate_consensus=True,
                )
                print(
                    f"Success: Recorded decision '{rec.decision.upper()}' for "
                    f"'{rec.headword}' ({rec.entry_id})."
                )
                if eval_res:
                    print(
                        f"  Consensus Status: {eval_res.decision_outcome.upper()} "
                        f"({eval_res.approvals_count}/{eval_res.threshold_required} approvals)"
                    )
                    if eval_res.notes:
                        print(f"  Notes: {eval_res.notes}")
                return 0
            except Exception as err:
                print(f"Error recording decision: {err}", file=sys.stderr)
                return 1

        if args.consensus:
            if args.consensus == "all":
                candidates = service.vocab_repo.list_review_queue(limit=args.limit)
                print("=" * 65)
                print(f"MULTI-REVIEWER CONSENSUS EVALUATION ({len(candidates)} entries):")
                print("=" * 65)
                for cand in candidates:
                    eval_res = service.evaluate_consensus(cand.id)
                    print(
                        f"  - [{cand.id}] '{cand.headword}': "
                        f"{eval_res.decision_outcome.upper()} "
                        f"({eval_res.approvals_count}/{eval_res.threshold_required} approvals)"
                    )
                print("=" * 65)
                return 0
            else:
                try:
                    eval_res = service.evaluate_consensus(args.consensus)
                    print("=" * 65)
                    print(f"CONSENSUS EVALUATION: {args.consensus}")
                    print("=" * 65)
                    print(f"  Decision Outcome:         {eval_res.decision_outcome.upper()}")
                    met_str = "Yes" if eval_res.is_consensus_met else "No"
                    print(f"  Consensus Threshold Met:  {met_str}")
                    print(
                        f"  Approvals:                {eval_res.approvals_count} of "
                        f"{eval_res.threshold_required} required"
                    )
                    if eval_res.approving_reviewers:
                        print(
                            f"  Approving Reviewers:      {', '.join(eval_res.approving_reviewers)}"
                        )
                    print(f"  Rejections:               {eval_res.rejections_count}")
                    print(f"  Conflicts:                {eval_res.conflicts_count}")
                    print(f"  Corrections Requested:    {eval_res.corrections_count}")
                    src_str = "Yes" if eval_res.is_source_verified else "No"
                    print(f"  Source Evidence Verified: {src_str}")
                    perm_str = "Yes" if eval_res.is_permission_cleared else "No"
                    print(f"  Permission Cleared:       {perm_str}")
                    pub_str = "Yes" if eval_res.is_public_eligible else "No"
                    print(f"  Public Release Eligible:  {pub_str}")
                    if eval_res.notes:
                        print(f"  Notes:                    {eval_res.notes}")
                    print("=" * 65)
                    return 0
                except Exception as err:
                    print(
                        f"Error evaluating consensus for '{args.consensus}': {err}",
                        file=sys.stderr,
                    )
                    return 1

        if args.export_package:
            try:
                cnt = service.export_review_package(
                    output_path=args.export_package,
                    limit=args.limit,
                )
                print(
                    f"Success: Exported versioned review package with {cnt} task(s) "
                    f"to '{args.export_package}'."
                )
                return 0
            except Exception as err:
                print(f"Error exporting review package: {err}", file=sys.stderr)
                return 1

        if args.validate_package:
            try:
                res = service.validate_review_package(args.validate_package)
                print("=" * 65)
                print("REVIEW PACKAGE VALIDATION REPORT:")
                print("=" * 65)
                print(f"  Package Valid:      {'PASSED' if res['valid'] else 'FAILED'}")
                print(f"  Total Tasks:        {res['total_tasks']}")
                print(f"  Valid Submissions:  {res['valid_submissions']}")
                print(f"  Stale Conflicts:    {res['stale_conflicts']}")
                if res["errors"]:
                    print(f"  Errors ({len(res['errors'])}):")
                    for e in res["errors"]:
                        print(f"    ! {e}")
                if res["warnings"]:
                    print(f"  Warnings ({len(res['warnings'])}):")
                    for w in res["warnings"]:
                        print(f"    * {w}")
                print("=" * 65)
                return 0 if res["valid"] else 1
            except Exception as err:
                print(f"Error validating package: {err}", file=sys.stderr)
                return 1

        if args.import_package:
            try:
                res = service.import_review_package(
                    input_path=args.import_package,
                    default_reviewer=args.reviewer,
                    dry_run=args.dry_run,
                )
                dry_str = " (DRY RUN)" if res.get("dry_run") else ""
                print("=" * 65)
                print(f"REVIEW PACKAGE IMPORT REPORT{dry_str}:")
                print("=" * 65)
                print(f"  Decisions Applied:  {res.get('applied_count', 0)}")
                if res.get("errors"):
                    print(f"  Errors ({len(res['errors'])}):")
                    for e in res["errors"]:
                        print(f"    ! {e}")
                if res.get("warnings"):
                    print(f"  Warnings ({len(res['warnings'])}):")
                    for w in res["warnings"]:
                        print(f"    * {w}")
                if res.get("evaluations"):
                    print(f"  Evaluations Run:    {len(res['evaluations'])}")
                print("=" * 65)
                return 0 if not res.get("errors") else 1
            except Exception as err:
                print(f"Error importing package: {err}", file=sys.stderr)
                return 1

        if args.show:
            try:
                details = service.get_candidate_details(args.show)
            except Exception as err:
                print(f"Error fetching candidate '{args.show}': {err}", file=sys.stderr)
                return 1

            entry = details["entry"]
            print("=" * 65)
            print(f"CANDIDATE VOCABULARY RECORD: {entry.headword} ({entry.id})")
            print("=" * 65)
            print(f"  Headword:             {entry.headword}")
            print(f"  Part of Speech:       {entry.part_of_speech or 'Not recorded'}")
            print(f"  Dialect:              {entry.dialect or 'Standard / Unspecified'}")
            print(f"  Verification Status:  {entry.verification_status}")
            print(f"  Review Status:        {entry.review_status}")
            if entry.reviewer:
                print(f"  Last Reviewer:        {entry.reviewer}")
            if entry.reviewed_at:
                print(f"  Reviewed At:          {entry.reviewed_at}")
            if entry.review_notes:
                print(f"  Review Notes:         {entry.review_notes}")

            print("\n  Meanings / Glosses:")
            if entry.meanings:
                for idx, m in enumerate(entry.meanings, start=1):
                    print(f"    {idx}. {m}")
            else:
                print("    (No verified meanings recorded - awaiting human review)")

            if entry.alternative_spellings:
                print(f"\n  Alternative Spellings: {', '.join(entry.alternative_spellings)}")

            if details["safe_example_sentences"]:
                print("\n  Example Sentences:")
                for ex in details["safe_example_sentences"]:
                    print(f"    - \"{ex}\"")

            print("\n  Source Provenance Citations:")
            if details["provenance"]:
                for p in details["provenance"]:
                    p_loc = f", {p['page_or_section']}" if p.get("page_or_section") else ""
                    print(f"    * [{p['source_id']}] ({p['resource_type']}) {p['citation']}{p_loc}")
                    if p.get("context_sentence"):
                        print(f"      Context: \"{p['context_sentence']}\"")
            else:
                print("    (No source citations recorded)")

            if details["duplicate_suggestions"]:
                print("\n  Suggested Duplicate / Variant Entries:")
                for dup in details["duplicate_suggestions"]:
                    m_str = (
                        f" - Meanings: {', '.join(dup['meanings'])}"
                        if dup.get("meanings")
                        else ""
                    )
                    print(
                        f"    ? [{dup['entry_id']}] '{dup['headword']}' "
                        f"({dup['match_type'].upper()}, score: {dup['score']:.2f}){m_str}"
                    )
                    print(f"      Reason: {dup['explanation']}")

            if details["review_history"]:
                print("\n  Review History & Audit Trail:")
                for h in details["review_history"]:
                    ts = h.get("review_timestamp") or "Timestamp not recorded"
                    h_notes = f" — Note: {h['notes']}" if h.get("notes") else ""
                    print(f"    * [{ts}] {h['decision'].upper()} by {h['reviewer']}{h_notes}")

            print("=" * 65)
            return 0

        if args.history:
            reviews = service.review_repo.get_reviews_for_entry(args.history)
            if not reviews:
                print(f"No review history found for entry '{args.history}'.")
                return 0
            print("=" * 65)
            print(f"REVIEW AUDIT HISTORY FOR '{args.history}' ({len(reviews)} decision(s)):")
            print("=" * 65)
            for rev in reviews:
                ts = rev.review_timestamp or "Timestamp not recorded"
                note_str = f"\n    Notes:    {rev.notes}" if rev.notes else ""
                dup_str = (
                    f"\n    Target:   {rev.target_duplicate_id}"
                    if rev.target_duplicate_id
                    else ""
                )
                print(
                    f"  * Decision: {rev.decision.upper()} by {rev.reviewer} "
                    f"on {ts}{note_str}{dup_str}"
                )
            print("=" * 65)
            return 0

        if args.accept:
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier is required to accept an entry.",
                    file=sys.stderr,
                )
                return 1
            try:
                updated = service.accept_candidate(
                    entry_id=args.accept,
                    reviewer=args.reviewer,
                    meanings=args.meaning,
                    pos=args.pos,
                    dialect=args.dialect,
                    notes=args.notes,
                )
                print(f"Success: Entry '{updated.headword}' ({updated.id}) accepted as verified.")
                print(f"  Meanings: {', '.join(updated.meanings)}")
                return 0
            except Exception as err:
                print(f"Error accepting '{args.accept}': {err}", file=sys.stderr)
                return 1

        if args.reject:
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier is required to reject an entry.",
                    file=sys.stderr,
                )
                return 1
            reason = args.reason or args.notes
            if not reason:
                print("Error: --reason is required when rejecting a candidate.", file=sys.stderr)
                return 1
            try:
                updated = service.reject_candidate(
                    entry_id=args.reject,
                    reviewer=args.reviewer,
                    reason=reason,
                )
                print(f"Success: Entry '{updated.headword}' ({updated.id}) rejected.")
                print(f"  Reason: {updated.review_notes}")
                return 0
            except Exception as err:
                print(f"Error rejecting '{args.reject}': {err}", file=sys.stderr)
                return 1

        if args.flag:
            if not args.reviewer:
                print("Error: --reviewer identifier is required to flag an entry.", file=sys.stderr)
                return 1
            decision = (
                args.status
                if args.status in {"reviewed_uncertain", "conflict"}
                else "reviewed_uncertain"
            )
            try:
                updated = service.flag_candidate(
                    entry_id=args.flag,
                    reviewer=args.reviewer,
                    decision=decision,
                    notes=args.notes or "",
                )
                print(
                    f"Success: Entry '{updated.headword}' ({updated.id}) "
                    f"flagged as '{decision}'."
                )
                return 0
            except Exception as err:
                print(f"Error flagging '{args.flag}': {err}", file=sys.stderr)
                return 1

        if args.edit:
            if not args.reviewer:
                print("Error: --reviewer identifier is required to edit an entry.", file=sys.stderr)
                return 1
            try:
                updated = service.edit_candidate(
                    entry_id=args.edit,
                    reviewer=args.reviewer,
                    meanings=args.meaning,
                    pos=args.pos,
                    dialect=args.dialect,
                    alternative_spellings=args.alt_spelling,
                    example_sentences=args.example,
                    notes=args.notes,
                )
                print(f"Success: Entry '{updated.headword}' ({updated.id}) updated.")
                return 0
            except Exception as err:
                print(f"Error editing '{args.edit}': {err}", file=sys.stderr)
                return 1

        if args.link_duplicate:
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier is required to link a duplicate.",
                    file=sys.stderr,
                )
                return 1
            if not args.target_id:
                print("Error: --target-id of canonical entry is required.", file=sys.stderr)
                return 1
            try:
                cand, target = service.link_duplicate(
                    candidate_id=args.link_duplicate,
                    target_id=args.target_id,
                    reviewer=args.reviewer,
                    as_spelling=not args.no_alt_spelling,
                    notes=args.notes,
                )
                print(
                    f"Success: Linked '{cand.headword}' ({cand.id}) as duplicate of "
                    f"'{target.headword}' ({target.id}). Provenance citations merged."
                )
                return 0
            except Exception as err:
                print(f"Error linking duplicate: {err}", file=sys.stderr)
                return 1

        if args.export:
            try:
                count = service.export_candidates(
                    output_path=args.export,
                    review_status=args.status or "pending_review",
                    source_type=args.source_type,
                    dialect=args.dialect,
                )
                print(f"Success: Exported {count} candidate(s) to '{args.export}'.")
                return 0
            except Exception as err:
                print(f"Error exporting candidates: {err}", file=sys.stderr)
                return 1

        if args.import_corrections:
            try:
                res = service.import_corrections(
                    input_path=args.import_corrections,
                    default_reviewer=args.reviewer,
                )
                print("=" * 65)
                print("COMMUNITY REVIEW CORRECTIONS IMPORT REPORT:")
                print(f"  Total records in file: {res['total']}")
                print(f"  Applied corrections:   {res['applied']}")
                if res["errors"]:
                    print(f"  Errors encountered:    {len(res['errors'])}")
                    for e in res["errors"]:
                        print(f"    ! {e}")
                print("=" * 65)
                return 0 if not res["errors"] else 1
            except Exception as err:
                print(f"Error importing corrections: {err}", file=sys.stderr)
                return 1

        if args.interactive:
            if not args.reviewer:
                print(
                    "Error: --reviewer identifier is required for interactive review.",
                    file=sys.stderr,
                )
                return 1
            queue = service.get_review_queue(
                review_status=args.status or "pending_review",
                source_type=args.source_type,
                source_id=args.source_id,
                dialect=args.dialect,
                missing_meanings=args.missing_meaning,
                has_duplicates=args.has_duplicates,
                limit=args.limit,
            )
            if not queue:
                print("No pending vocabulary candidates matching current filters.")
                return 0

            print(f"Starting interactive review session for {len(queue)} candidate(s).")
            print(
                "Commands: [a]ccept, [r]eject, [f]lag uncertain, [e]dit, "
                "[l]ink duplicate, [s]kip, [q]uit"
            )
            for idx, cand in enumerate(queue, start=1):
                print("-" * 65)
                print(f"[{idx}/{len(queue)}] Candidate: '{cand.headword}' (ID: {cand.id})")
                if cand.dialect:
                    print(f"  Dialect:   {cand.dialect}")
                if cand.meanings:
                    print(f"  Meanings:  {', '.join(cand.meanings)}")
                else:
                    print("  Meanings:  (None recorded)")
                if cand.provenance:
                    p = cand.provenance[0]
                    print(f"  Source:    [{p.source_id}] {p.citation}")
                    if p.context_sentence:
                        print(f"  Context:   \"{p.context_sentence}\"")

                dups = service.find_duplicate_suggestions(cand, threshold=0.75)
                if dups:
                    dup_h = dups[0]["headword"]
                    dup_e = dups[0]["entry_id"]
                    dup_x = dups[0]["explanation"]
                    print(f"  Suggested duplicate: '{dup_h}' ({dup_e}) — {dup_x}")

                try:
                    choice = input("Decision [a/r/f/e/l/s/q]: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print("\nReview session ended.")
                    break

                if choice == "q":
                    print("Review session aborted.")
                    break
                elif choice == "s":
                    continue
                elif choice == "a":
                    m_in = input("Enter confirmed meaning (comma-separated): ").strip()
                    meanings = [m.strip() for m in m_in.split(",") if m.strip()] if m_in else None
                    try:
                        service.accept_candidate(cand.id, reviewer=args.reviewer, meanings=meanings)
                        print(f"Accepted '{cand.headword}' as verified.")
                    except Exception as err:
                        print(f"Failed to accept: {err}")
                elif choice == "r":
                    reason = input("Enter reason for rejection: ").strip()
                    try:
                        service.reject_candidate(cand.id, reviewer=args.reviewer, reason=reason)
                        print(f"Rejected '{cand.headword}'.")
                    except Exception as err:
                        print(f"Failed to reject: {err}")
                elif choice == "f":
                    notes = input("Enter uncertainty notes: ").strip()
                    service.flag_candidate(cand.id, reviewer=args.reviewer, notes=notes)
                    print(f"Flagged '{cand.headword}'.")
                elif choice == "l":
                    t_id = input("Enter target canonical entry ID: ").strip()
                    try:
                        service.link_duplicate(cand.id, target_id=t_id, reviewer=args.reviewer)
                        print(f"Linked '{cand.headword}' to '{t_id}'.")
                    except Exception as err:
                        print(f"Failed to link: {err}")
                elif choice == "e":
                    m_in = input("Enter meaning(s): ").strip()
                    pos_in = input("Enter part of speech: ").strip()
                    meanings = [m.strip() for m in m_in.split(",") if m.strip()] if m_in else None
                    service.edit_candidate(
                        cand.id,
                        reviewer=args.reviewer,
                        meanings=meanings,
                        pos=pos_in or None,
                    )
                    print(f"Updated '{cand.headword}'.")

            return 0

        # Default: --list or fallback
        total_count = service.count_review_queue(
            review_status=args.status,
            source_type=args.source_type,
            source_id=args.source_id,
            dialect=args.dialect,
            missing_meanings=args.missing_meaning,
        )
        candidates = service.get_review_queue(
            review_status=args.status,
            source_type=args.source_type,
            source_id=args.source_id,
            dialect=args.dialect,
            missing_meanings=args.missing_meaning,
            has_duplicates=args.has_duplicates,
            limit=args.limit,
        )

        stat_filter = f" [{args.status}]" if args.status else ""
        print("=" * 65)
        print(f"VOCABULARY CANDIDATE REVIEW QUEUE{stat_filter}:")
        print(f"Total matching in queue: {total_count} (Showing top {len(candidates)})")
        print("=" * 65)
        if not candidates:
            print("No vocabulary candidates found matching current filter criteria.")
            print("=" * 65)
            return 0

        for cand in candidates:
            m_str = ", ".join(cand.meanings) if cand.meanings else "(Awaiting Meaning)"
            d_str = f" [{cand.dialect}]" if cand.dialect else ""
            p_count = f"{len(cand.provenance)} citation(s)"
            v_info = f"Verification: {cand.verification_status}, {p_count}"
            print(f"- [{cand.id:<18}] '{cand.headword}'{d_str}")
            print(f"    Meanings: {m_str}")
            print(f"    Status:   {cand.review_status:<16} ({v_info})")
        print("=" * 65)
        return 0

    if args.command == "enrich":
        from tangkhul_lib.storage.database import DatabaseManager
        from tangkhul_lib.vocabulary.enrichment import VocabularyEnrichmentPipeline

        config = LibraryConfig.from_environment()
        db_path = config.paths.data_dir / "database" / "tangkhul_corpus.sqlite"
        db_mgr = DatabaseManager(db_path)
        db_mgr.initialize_schema()
        pipeline = VocabularyEnrichmentPipeline(db_manager=db_mgr, config=config)

        if args.list_sources:
            eligible, ineligible = pipeline.list_eligible_sources(
                source_type=args.source_type,
                dialect=args.dialect,
            )
            print("=" * 70)
            print("TANGKHUL VOCABULARY ENRICHMENT SOURCES")
            print("=" * 70)
            print(f"\n[1] Eligible Sources for Vocabulary Extraction ({len(eligible)}):")
            if not eligible:
                print("  No eligible sources matching criteria.")
            for s in eligible:
                d_str = f" [{s['dialect']}]" if s.get("dialect") else ""
                print(f"  * [{s['source_id']:<14}] {s['title'][:40]:<42} {d_str}")
                print(f"      Tier: {s['permission_status']} | Module: {s['resource_type']}")

            print(f"\n[2] Ineligible / Blocked Sources ({len(ineligible)}):")
            for s in ineligible[: args.limit]:
                print(f"  * [{s['source_id']:<14}] {s['title'][:40]:<42}")
                print(f"      Status: {s['permission_status']} | Reason: {s['skip_reason']}")
            print("=" * 70)
            return 0

        if args.summary:
            if args.source_id:
                run = pipeline.enrich_repo.get_last_run_for_source(args.source_id)
                if not run:
                    print(f"No enrichment history found for source '{args.source_id}'.")
                    return 0
                runs = [run]
            else:
                runs = pipeline.enrich_repo.list_runs(limit=args.limit)

            if not runs:
                print("No enrichment runs recorded in database.")
                return 0

            print("=" * 70)
            print(f"VOCABULARY ENRICHMENT RUNS ({len(runs)}):")
            print("=" * 70)
            for r in runs:
                print(f"Run ID:    {r.id}")
                print(f"Source:    {r.source_id} (Method: {r.extraction_method})")
                print(f"Status:    {r.status.upper()}")
                stats_str = (
                    f"{r.items_extracted} extracted, {r.candidates_created} new candidates, "
                    f"{r.entries_updated} updated, {r.duplicates_detected} duplicates"
                )
                print(f"Stats:     {stats_str}")
                if r.file_path:
                    print(f"File:      {r.file_path}")
                if r.warnings:
                    print(f"Warnings:  {', '.join(r.warnings)}")
                if r.error_message:
                    print(f"Error:     {r.error_message}")
                print("-" * 70)
            return 0

        if args.export_candidates:
            count = pipeline.export_candidates(
                output_path=args.export_candidates,
                source_id=args.source_id,
                limit=args.limit,
            )
            print(
                f"Successfully exported {count} candidate(s) to '{args.export_candidates}'."
            )
            return 0

        if args.preview:
            if not args.source_id:
                print("Error: --source-id is required for preview.", file=sys.stderr)
                return 1
            try:
                res = pipeline.preview_source(
                    source_id=args.source_id,
                    file_path=args.file,
                    limit=args.limit,
                )
            except Exception as err:
                print(f"Preview error: {err}", file=sys.stderr)
                return 1

            print("=" * 70)
            print(f"PREVIEW ENRICHMENT: {res['title']} ({res['source_id']})")
            print("=" * 70)
            print(f"File:              {res['file_name']} ({res['file_format'].upper()})")
            print(f"Extraction Method: {res['extraction_method']}")
            print(f"Total Found:       {res['total_items_found']}")
            print(f"\nSample Lexical Items (showing top {len(res['sample_items'])}):")
            for item in res["sample_items"]:
                m_str = (
                    ", ".join(item["meanings"])
                    if item["meanings"]
                    else "(Running token / no definition)"
                )
                cats = f" [{', '.join(item['categories'])}]" if item["categories"] else ""
                hw_pos = f"  * '{item['headword']}' ({item['part_of_speech']})"
                print(f"{hw_pos} [{item['dialect']}]{cats}")
                print(f"      Meanings: {m_str}")
                if item["example"]:
                    print(f"      Example:  \"{item['example'][:80]}...\"")
            if res["warnings"]:
                print(f"\nWarnings: {res['warnings']}")
            print("=" * 70)
            return 0

        if args.source_id:
            try:
                summary = pipeline.enrich_from_source(
                    source_id=args.source_id,
                    file_path=args.file,
                    dialect=args.dialect,
                    force=args.force,
                    dry_run=args.dry_run,
                )
            except Exception as err:
                print(f"Enrichment error for '{args.source_id}': {err}", file=sys.stderr)
                return 1

            mode_str = "[DRY-RUN] " if summary.status == "dry_run" else ""
            print("=" * 70)
            print(
                f"{mode_str}VOCABULARY ENRICHMENT REPORT: "
                f"{summary.source_title} ({summary.source_id})"
            )
            print("=" * 70)
            print(f"Status:                 {summary.status.upper()}")
            print(f"Permission Status:      {summary.permission_status}")
            print(f"Extraction Method:      {summary.extraction_method}")
            print(f"Items Extracted:        {summary.items_extracted}")
            print(f"New Candidates Created: {summary.candidates_created}")
            print(f"Existing Updated:       {summary.entries_updated}")
            print(f"Duplicates Flagged:     {len(summary.duplicate_suggestions)}")

            if summary.category_breakdown:
                print("\nLexical & Grammatical Categories:")
                for cat, cnt in summary.category_breakdown.items():
                    if cnt > 0:
                        print(f"  - {cat:<26} {cnt:>4}")
            if summary.data_gaps:
                print("\nData Gaps (0 candidates found):")
                for gap in summary.data_gaps:
                    print(f"  - {gap:<26} [DATA GAP]")

            if summary.dialect_breakdown:
                print("\nDialect Varieties:")
                for d_name, cnt in summary.dialect_breakdown.items():
                    print(f"  - {d_name:<26} {cnt:>4}")

            if args.show_duplicates and summary.duplicate_suggestions:
                print(
                    "\nSuggested Duplicates / Phonetic Matches "
                    f"(Showing top {min(len(summary.duplicate_suggestions), 10)}):"
                )
                for dup in summary.duplicate_suggestions[:10]:
                    print(
                        f"  * '{dup['candidate_headword']}' -> '{dup['matching_headword']}' "
                        f"({dup['matching_entry_id']})"
                    )
                    print(
                        f"      Match: {dup['match_type'].upper()} ({dup['score']:.2f}) "
                        f"— {dup['explanation']}"
                    )

            if summary.warnings:
                print(f"\nWarnings: {summary.warnings}")
            if summary.error_message:
                print(f"\nError: {summary.error_message}")
            print("=" * 70)
            return 0 if summary.status in {"completed", "dry_run"} else 1

        enrich_parser.print_help()
        return 0

    if args.command == "audio":
        from tangkhul_lib.audio.cli import run_audio_cli
        return run_audio_cli(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
