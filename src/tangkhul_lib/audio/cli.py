"""Command-line interface operations for the Tangkhul Audio Corpus and Pronunciation system."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tangkhul_lib.audio.permissions import AudioPermissionDeniedError
from tangkhul_lib.audio.service import AudioCorpusService
from tangkhul_lib.audio.validation import AudioSecurityError, AudioValidationError
from tangkhul_lib.core.config import LibraryConfig
from tangkhul_lib.core.exceptions import ResourceNotFoundError
from tangkhul_lib.storage.database import DatabaseManager


def format_duration(seconds: float) -> str:
    """Format duration in seconds into mm:ss or hh:mm:ss."""
    if seconds <= 0:
        return "00:00"
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def get_service(config: LibraryConfig | None = None) -> AudioCorpusService:
    """Instantiate AudioCorpusService using LibraryConfig."""
    cfg = config or LibraryConfig.from_environment()
    db_path = cfg.paths.database_dir / cfg.sqlite_db_name
    db_manager = DatabaseManager(db_path)
    db_manager.initialize_schema()
    audio_root = cfg.paths.data_dir / "raw" / "audio"
    return AudioCorpusService(db_manager=db_manager, audio_root=audio_root)


def run_audio_cli(args: argparse.Namespace) -> int:
    """Execute audio subcommand dispatch based on parsed arguments."""
    config = LibraryConfig.from_environment()
    service = get_service(config)

    # Determine requested action
    action = args.action
    target = args.target

    if not action:
        if args.list:
            action = "list"
        elif getattr(args, "inspect_id", None):
            action = "inspect"
            target = args.inspect_id
        elif getattr(args, "import_file", None) or args.metadata_only:
            action = "import"
            target = getattr(args, "import_file", None)
        elif args.validate:
            action = "validate"
            target = args.validate
        elif args.search:
            action = "search"
            target = args.search
        elif args.pronunciation is not None:
            action = "pronunciation"
            target = args.pronunciation
        elif args.permissions:
            action = "permissions"
            target = args.permissions
        elif args.export:
            action = "export"
            target = args.export
        elif args.summary:
            action = "summary"
        else:
            action = "summary"

    # 1. SUMMARY
    if action == "summary":
        summary = service.get_summary()
        print("=" * 70)
        print("TANGKHUL AUDIO CORPUS & PRONUNCIATION TELEMETRY")
        print("=" * 70)
        print(f"Total Recordings:            {summary.total_recordings}")
        print(f"  - Authorized:              {summary.authorized_count}")
        print(f"  - Pending Clearance:       {summary.pending_count}")
        print(f"  - Restricted Access:       {summary.restricted_count}")
        print(f"  - Withdrawn (Revoked):     {summary.withdrawn_count}")
        dur_fmt = format_duration(summary.total_duration_seconds)
        print(f"Total Duration:              {dur_fmt} ({summary.total_duration_seconds:.1f}s)")
        print(f"Linked Vocabulary Entries:   {summary.linked_vocab_count}")
        print(f"Catalogued Pronunciations:   {summary.verified_pronunciations_count}")

        if summary.formats_breakdown:
            print("\nAudio Format Distribution:")
            for fmt, count in sorted(summary.formats_breakdown.items()):
                print(f"  - {fmt.upper():<10} {count:>5}")

        if summary.dialect_breakdown:
            print("\nDialect & Variety Coverage:")
            for dia, count in sorted(summary.dialect_breakdown.items()):
                print(f"  - {dia:<20} {count:>5}")
        print("=" * 70)
        return 0

    # 2. LIST
    if action == "list":
        recordings = service.list_recordings(
            dialect=args.dialect,
            village=args.village,
            consent_status=args.consent_status,
            include_withdrawn=args.include_withdrawn,
            limit=args.limit,
            offset=args.offset,
            is_privileged_view=args.privileged,
        )
        print("=" * 80)
        print(f"TANGKHUL AUDIO RECORDINGS ({len(recordings)} displayed)")
        print("=" * 80)
        if not recordings:
            print("No audio recordings found matching query criteria.")
            print("=" * 80)
            return 0

        hdr = (
            f"{'ID':<18} {'Title':<26} {'Dialect':<12} {'Status':<12} "
            f"{'Duration':<9} {'Vocab ID':<14}"
        )
        print(hdr)
        print("-" * 80)
        for r in recordings:
            status_flag = r["consent_status"].upper()
            if r["is_withdrawn"]:
                status_flag = "WITHDRAWN"
            elif r["access_restrictions"] == "restricted":
                status_flag = "RESTRICTED"

            dur_str = format_duration(r.get("duration_seconds", 0.0))
            vocab_str = r.get("vocab_entry_id") or "—"
            dia_str = r.get("dialect") or "General"
            title_str = (r.get("title") or "")[:24]

            row = (
                f"{r['id']:<18} {title_str:<26} {dia_str:<12} {status_flag:<12} "
                f"{dur_str:<9} {vocab_str:<14}"
            )
            print(row)
        print("=" * 80)
        return 0

    # 3. INSPECT
    if action == "inspect":
        rec_id = target or getattr(args, "inspect_id", None)
        if not rec_id:
            print(
                "Error: Specify recording ID to inspect (e.g. `tangkhul audio inspect <ID>`).",
                file=sys.stderr,
            )
            return 1

        rec = service.get_recording(rec_id, is_privileged_view=args.privileged)
        if not rec:
            print(f"Error: Audio recording '{rec_id}' not found.", file=sys.stderr)
            return 1

        print("=" * 70)
        print(f"AUDIO RECORDING: {rec['title']} ({rec['id']})")
        print("=" * 70)
        print(f"Title:               {rec['title']}")
        if rec.get("description"):
            print(f"Description:         {rec['description']}")
        print(f"Vocabulary Link:     {rec.get('vocab_entry_id') or 'None'}")
        print(f"Speaker Pseudonym:   {rec.get('speaker_pseudonym') or 'Unspecified'}")
        print(f"Dialect / Variety:   {rec.get('dialect') or 'Unspecified'}")
        if rec.get("village"):
            print(f"Village Origin:      {rec['village']}")
        if rec.get("region"):
            print(f"Region:              {rec['region']}")
        print(f"Recording Method:    {rec.get('recording_method')}")
        if rec.get("recording_date"):
            print(f"Recording Date:      {rec['recording_date']}")
        if rec.get("recording_source"):
            print(f"Source / Contributor:{rec['recording_source']}")

        print("\nTechnical Specifications:")
        print(f"  Format:            {rec.get('file_format', '').upper()}")
        r_dur = rec.get("duration_seconds", 0.0)
        print(f"  Duration:          {format_duration(r_dur)} ({r_dur:.2f}s)")
        print(f"  Sample Rate:       {rec.get('sample_rate', 0)} Hz")
        print(f"  Channels:          {rec.get('channels', 1)}")
        print(f"  File Size:         {rec.get('file_size_bytes', 0):,} bytes")
        print(f"  SHA-256 Checksum:  {rec.get('checksum_sha256') or 'N/A'}")
        print(f"  Managed File Path: {rec.get('file_path') or '[Metadata-Only]'}")

        print("\nTranscription & Linguistics:")
        print(f"  Transcription:     {rec.get('transcription') or 'N/A'}")
        if rec.get("transcription_normalized"):
            print(f"  Normalized:        {rec['transcription_normalized']}")
        if rec.get("ipa_transcription"):
            print(f"  IPA Pronunciation: /{rec['ipa_transcription']}/")
        if rec.get("transliteration"):
            print(f"  Transliteration:   {rec['transliteration']}")

        print("\nPermissions & Governance:")
        print(f"  Consent Status:    {rec.get('consent_status', '').upper()}")
        print(f"  Withdrawn:         {'YES' if rec.get('is_withdrawn') else 'NO'}")
        if rec.get("is_withdrawn"):
            print(f"  Withdrawal Date:   {rec.get('withdrawal_date')}")
            print(f"  Withdrawal Reason: {rec.get('withdrawal_reason')}")
        print(f"  Permitted Uses:    {', '.join(rec.get('permitted_uses', []))}")
        if rec.get("access_restrictions"):
            print(f"  Restrictions:      {rec['access_restrictions']}")
        print(f"  Verification:      {rec.get('verification_status')}")

        # Linked pronunciations
        if rec.get("vocab_entry_id"):
            prons = service.get_pronunciations_for_vocab(rec["vocab_entry_id"])
            if prons:
                print(f"\nLinked Pronunciation Records ({len(prons)}):")
                for p in prons:
                    ipa_str = f"/{p.pronunciation_ipa}/" if p.pronunciation_ipa else "N/A"
                    p_dia = p.dialect or "General"
                    print(
                        f"  * [{p.id}] Headword: '{p.headword}' | IPA: {ipa_str} | "
                        f"Dialect: {p_dia} | Status: {p.review_status}"
                    )

        print("=" * 70)
        return 0

    # 4. VALIDATE
    if action == "validate":
        file_path = target or args.validate
        if not file_path:
            print(
                "Error: Specify audio file path to validate "
                "(e.g. `tangkhul audio validate <FILE>`).",
                file=sys.stderr,
            )
            return 1

        try:
            meta = service.validate_audio_file(file_path)
        except (AudioValidationError, AudioSecurityError, FileNotFoundError) as err:
            print(f"Validation FAILED: {err}", file=sys.stderr)
            return 1

        print("=" * 70)
        print(f"AUDIO FILE VALIDATION: {Path(file_path).name}")
        print("=" * 70)
        print(f"File Path:        {Path(file_path).resolve()}")
        print(f"Status:           VALID ({meta['file_format'].upper()})")
        m_dur = meta["duration_seconds"]
        print(f"Duration:         {format_duration(m_dur)} ({m_dur:.2f}s)")
        print(f"Sample Rate:      {meta['sample_rate']} Hz")
        print(f"Channels:         {meta['channels']}")
        print(f"File Size:        {meta['file_size_bytes']:,} bytes")
        print(f"SHA-256 Checksum: {meta['checksum_sha256']}")
        if meta.get("warnings"):
            print(f"\nWarnings: {meta['warnings']}")
        print("=" * 70)
        return 0

    # 5. IMPORT
    if action == "import":
        source_path = target or getattr(args, "import_file", None)
        if not source_path and not args.metadata_only:
            print("Error: Specify audio file to import or use --metadata-only.", file=sys.stderr)
            return 1

        if not args.title:
            print("Error: --title is required when importing an audio recording.", file=sys.stderr)
            return 1

        permitted_list = None
        if args.permitted_uses:
            permitted_list = [u.strip() for u in args.permitted_uses.split(",") if u.strip()]

        try:
            res = service.import_audio_file(
                source_path=source_path,
                title=args.title,
                vocab_entry_id=args.vocab_id,
                headword=args.headword,
                speaker_pseudonym=args.speaker,
                dialect=args.dialect,
                village=args.village,
                region=args.region,
                recording_date=args.recording_date,
                recording_method=args.recording_method or "field_recording",
                recording_source=args.recording_source,
                transcription=args.transcription,
                ipa_transcription=args.ipa,
                transliteration=args.transliteration,
                source_citation=args.source_citation,
                consent_status=args.consent_status or "pending",
                permitted_uses=permitted_list,
                access_restrictions=args.access_restrictions,
                metadata_only=args.metadata_only,
                dry_run=args.dry_run,
            )
        except (
            AudioValidationError,
            AudioSecurityError,
            AudioPermissionDeniedError,
            ResourceNotFoundError,
            FileNotFoundError,
        ) as err:
            print(f"Import Error: {err}", file=sys.stderr)
            return 1

        if res["is_duplicate"]:
            print(
                f"DUPLICATE DETECTED: File matches existing recording ID '{res['duplicate_id']}'. "
                "Import skipped."
            )
            return 0

        mode_str = "[DRY-RUN] " if res["dry_run"] else ""
        rec = res["recording"]
        print("=" * 70)
        print(f"{mode_str}AUDIO RECORDING IMPORTED: {rec.title} ({rec.id})")
        print("=" * 70)
        print(f"Recording ID:     {rec.id}")
        print(f"Title:            {rec.title}")
        print(f"Consent Status:   {rec.consent_status.upper()}")
        print(f"Dialect:          {rec.dialect or 'General'}")
        if rec.speaker_pseudonym:
            print(f"Speaker:          {rec.speaker_pseudonym}")
        if rec.file_path:
            print(f"Managed File:     {rec.file_path}")
            print(f"Duration:         {format_duration(rec.duration_seconds)}")
            print(f"SHA-256 Checksum: {rec.checksum_sha256}")
        else:
            print("Managed File:     [Metadata-Only Record]")

        if res["pronunciation"]:
            pron = res["pronunciation"]
            print("\nLinked Pronunciation Record Created:")
            print(f"  ID:             {pron.id}")
            print(f"  Headword:       {pron.headword}")
            ipa_str = f"/{pron.pronunciation_ipa}/" if pron.pronunciation_ipa else "None"
            print(f"  IPA:            {ipa_str}")
            print(f"  Review Status:  {pron.review_status}")

        if res["warnings"]:
            print(f"\nWarnings: {res['warnings']}")
        print("=" * 70)
        return 0

    # 6. SEARCH
    if action == "search":
        query = target or args.search
        if not query:
            print(
                "Error: Specify search query (e.g. `tangkhul audio search <QUERY>`).",
                file=sys.stderr,
            )
            return 1

        results = service.search_audio(
            query=query,
            dialect=args.dialect,
            include_withdrawn=args.include_withdrawn,
            limit=args.limit,
            is_privileged_view=args.privileged,
        )
        print("=" * 80)
        print(f"AUDIO CORPUS SEARCH: '{query}' ({len(results)} match(es))")
        print("=" * 80)
        if not results:
            print("No audio recordings found matching search query.")
            print("=" * 80)
            return 0

        print(f"{'ID':<18} {'Title':<24} {'Transcription / Headword':<26} {'Dialect':<10}")
        print("-" * 80)
        for r in results:
            t_str = r.get("transcription") or r.get("ipa_transcription") or "—"
            if len(t_str) > 24:
                t_str = t_str[:22] + ".."
            dia_str = r.get("dialect") or "General"
            print(f"{r['id']:<18} {r['title'][:22]:<24} {t_str:<26} {dia_str:<10}")
        print("=" * 80)
        return 0

    # 7. PRONUNCIATION
    if action == "pronunciation":
        query = target or args.pronunciation or ""

        # Check if this is a review command
        if getattr(args, "review_decision", None):
            pron_id = getattr(args, "review_id", None) or query
            if not pron_id:
                print("Error: Specify pronunciation record ID to review.", file=sys.stderr)
                return 1
            if not getattr(args, "reviewer", None):
                print(
                    "Error: --reviewer pseudonym is required when reviewing a pronunciation.",
                    file=sys.stderr,
                )
                return 1

            try:
                updated_pron = service.review_pronunciation(
                    pronunciation_id=pron_id,
                    reviewer=args.reviewer,
                    decision=args.review_decision,
                    notes=getattr(args, "review_notes", None),
                )
            except ResourceNotFoundError as err:
                print(f"Review Error: {err}", file=sys.stderr)
                return 1

            print("=" * 70)
            print(f"PRONUNCIATION REVIEW RECORDED: {updated_pron.id}")
            print("=" * 70)
            print(f"Headword:            {updated_pron.headword}")
            print(f"Reviewer:            {updated_pron.reviewer}")
            print(f"Decision / Status:   {updated_pron.review_status.upper()}")
            print(f"Verification Status: {updated_pron.verification_status}")
            if updated_pron.review_notes:
                print(f"Notes:               {updated_pron.review_notes}")
            print("=" * 70)
            return 0

        # Query / listing pronunciations
        if args.vocab_id:
            prons = service.get_pronunciations_for_vocab(args.vocab_id)
        elif query:
            prons = service.search_pronunciations(
                query=query, dialect=args.dialect, limit=args.limit
            )
        else:
            prons = service.pron_repo.list_all(dialect=args.dialect, limit=args.limit)

        print("=" * 80)
        print(f"TANGKHUL PRONUNCIATION RECORDS ({len(prons)} displayed)")
        print("=" * 80)
        if not prons:
            print("No pronunciation records found matching query.")
            print("=" * 80)
            return 0

        print(f"{'ID':<18} {'Headword':<18} {'IPA':<18} {'Dialect':<12} {'Review Status':<12}")
        print("-" * 80)
        for p in prons:
            ipa_val = f"/{p.pronunciation_ipa}/" if p.pronunciation_ipa else "—"
            dia_val = p.dialect or "General"
            r_status = p.review_status
            print(f"{p.id:<18} {p.headword[:16]:<18} {ipa_val:<18} {dia_val:<12} {r_status:<12}")
        print("=" * 80)
        return 0

    # 8. PERMISSIONS
    if action == "permissions":
        rec_id = target or args.permissions
        if not rec_id:
            print(
                "Error: Specify recording ID for permissions inspection or withdrawal.",
                file=sys.stderr,
            )
            return 1

        if getattr(args, "withdraw", False):
            reason = getattr(args, "reason", None)
            if not reason:
                print(
                    "Error: --reason is required when withdrawing speaker consent.",
                    file=sys.stderr,
                )
                return 1

            try:
                updated_rec = service.withdraw_consent(
                    recording_id=rec_id,
                    reason=reason,
                    authorized_by=getattr(args, "authorized_by", None),
                )
            except ResourceNotFoundError as err:
                print(f"Withdrawal Error: {err}", file=sys.stderr)
                return 1

            print("=" * 70)
            print(f"CONSENT WITHDRAWN: {updated_rec.id}")
            print("=" * 70)
            print(f"Recording:        {updated_rec.title} ({updated_rec.id})")
            print("Status:           WITHDRAWN (Revoked)")
            print(f"Withdrawal Date:  {updated_rec.withdrawal_date}")
            print(f"Reason:           {updated_rec.withdrawal_reason}")
            print("Notice: Recording has been shielded and excluded from all future exports.")
            print("=" * 70)
            return 0

        # View permissions history
        rec = service.audio_repo.get_by_id(rec_id)
        if not rec:
            print(f"Error: Audio recording '{rec_id}' not found.", file=sys.stderr)
            return 1

        audit_events = service.consent_repo.get_by_recording_id(rec_id)
        print("=" * 70)
        print(f"CONSENT & PERMISSION AUDIT: {rec.title} ({rec.id})")
        print("=" * 70)
        print(f"Current Consent Status: {rec.consent_status.upper()}")
        print(f"Withdrawn:              {'YES' if rec.is_withdrawn else 'NO'}")
        print(f"Speaker Pseudonym:      {rec.speaker_pseudonym or 'Unspecified'}")
        print(f"Permitted Uses:         {', '.join(rec.permitted_uses)}")
        if rec.access_restrictions:
            print(f"Access Restrictions:    {rec.access_restrictions}")

        print(f"\nConsent Audit Events ({len(audit_events)}):")
        for ev in audit_events:
            print(
                f"  * [{ev.timestamp}] Status: {ev.consent_status.upper()} | "
                f"Speaker: {ev.speaker_pseudonym}"
            )
            if ev.withdrawn_reason:
                print(f"      Withdrawal Reason: {ev.withdrawn_reason}")
            if ev.authorized_by:
                print(f"      Authorized By: {ev.authorized_by}")
        print("=" * 70)
        return 0

    # 9. EXPORT
    if action == "export":
        out_dir = target or args.export
        if not out_dir:
            print(
                "Error: Specify destination directory for audio export "
                "(e.g. `tangkhul audio export <DIR>`).",
                file=sys.stderr,
            )
            return 1

        res = service.export_corpus(
            output_dir=out_dir,
            dialect=args.dialect,
            dry_run=args.dry_run,
        )
        mode_str = "[DRY-RUN] " if res["dry_run"] else ""
        print("=" * 70)
        print(f"{mode_str}TANGKHUL AUDIO CORPUS EXPORT SUMMARY")
        print("=" * 70)
        print(f"Export Directory:        {res['output_directory']}")
        print(f"Exported Audio Files:    {res['exported_count']}")
        print(f"Skipped Withdrawn:       {res['skipped_withdrawn']}")
        print(f"Skipped Unauthorized:    {res['skipped_unauthorized']}")
        print(f"Skipped Restricted:      {res['skipped_restricted']}")
        print(f"Skipped Missing Files:   {res['skipped_missing_file']}")
        if res["exported_count"] > 0 and not res["dry_run"]:
            manifest_p = Path(res["output_directory"]) / "audio_manifest.jsonl"
            print(f"Manifest Generated:      {manifest_p}")
        print("=" * 70)
        return 0

    print(f"Unknown audio action: {action}", file=sys.stderr)
    return 1
