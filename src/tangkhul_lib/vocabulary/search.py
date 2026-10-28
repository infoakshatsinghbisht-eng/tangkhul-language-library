"""Vocabulary search engine for Tangkhul Language Library."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tangkhul_lib.vocabulary.normalization import normalize_unicode
from tangkhul_lib.vocabulary.phonetic import (
    SearchResultMatch,
    TangkhulPhoneticEncoder,
    calculate_similarity,
)

if TYPE_CHECKING:
    from tangkhul_lib.core.config import LibraryConfig
    from tangkhul_lib.core.models import VocabularyEntry
    from tangkhul_lib.storage.database import DatabaseManager
    from tangkhul_lib.storage.repositories import ManifestRepository, VocabularyRepository


class VocabularySearchEngine:
    """Search engine for querying unified Tangkhul vocabulary records."""

    VALID_SOURCE_TYPES = frozenset({
        "books",
        "songs",
        "dictionaries",
        "culture",
        "history",
        "literature",
    })

    def __init__(
        self,
        repository: VocabularyRepository | None = None,
        manifest_repository: ManifestRepository | None = None,
        entries: list[VocabularyEntry] | None = None,
    ) -> None:
        self.repository = repository
        self.manifest_repository = manifest_repository
        self._entries: list[VocabularyEntry] = entries or []

    def set_entries(self, entries: list[VocabularyEntry]) -> None:
        """Set or update in-memory entries."""
        self._entries = entries

    def _get_all_entries(self) -> list[VocabularyEntry]:
        """Fetch all entries from repository or local cache."""
        if self.repository:
            return self.repository.list_all()
        return self._entries

    def list_all(self) -> list[VocabularyEntry]:
        """Return all active vocabulary entries."""
        return self._get_all_entries()

    def search_exact(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching exact headword or alternative spelling (case/NFC normalized)."""
        q_norm = normalize_unicode(query).strip().lower()
        if not q_norm:
            return []

        entries = self._get_all_entries()
        results: list[VocabularyEntry] = []
        for entry in entries:
            head_norm = normalize_unicode(entry.headword).strip().lower()
            if q_norm == head_norm:
                results.append(entry)
                continue

            for alt in entry.alternative_spellings:
                if q_norm == normalize_unicode(alt).strip().lower():
                    results.append(entry)
                    break

        results.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))
        return results

    def search_headword(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching headword or alternative spellings (case/NFC normalized)."""
        q_norm = normalize_unicode(query).strip().lower()
        if not q_norm:
            return []

        entries = self._get_all_entries()
        results: list[VocabularyEntry] = []
        for entry in entries:
            head_norm = normalize_unicode(entry.headword).strip().lower()
            if q_norm in head_norm:
                results.append(entry)
                continue

            # Check alternative spellings
            for alt in entry.alternative_spellings:
                if q_norm in normalize_unicode(alt).strip().lower():
                    results.append(entry)
                    break

        results.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))
        return results

    def search_meaning(self, query: str) -> list[VocabularyEntry]:
        """Search entries matching glosses, translations, or definitions."""
        q_norm = normalize_unicode(query).strip().lower()
        if not q_norm:
            return []

        entries = self._get_all_entries()
        results: list[VocabularyEntry] = []
        for entry in entries:
            matches_meaning = any(
                q_norm in normalize_unicode(m).lower() for m in entry.meanings
            )
            matches_trans = any(
                q_norm in normalize_unicode(t).lower() for t in entry.translations_en
            )
            if matches_meaning or matches_trans:
                results.append(entry)

        results.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))
        return results

    def search_by_source(self, source_id: str) -> list[VocabularyEntry]:
        """Find all vocabulary entries supported by a specific source ID."""
        entries = self._get_all_entries()
        results = [
            e for e in entries
            if any(p.source_id == source_id for p in e.provenance)
        ]
        results.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))
        return results

    def search_with_matches(
        self,
        headword: str | None = None,
        exact_headword: str | None = None,
        meaning: str | None = None,
        dialect: str | None = None,
        part_of_speech: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        verification_status: str | None = None,
        limit: int | None = None,
        mode: str = "substring",
        threshold: float = 0.65,
        include_experimental_phonetics: bool = False,
    ) -> tuple[list[VocabularyEntry], dict[str, SearchResultMatch], dict[str, Any]]:
        """Multi-criteria search supporting substring, fulltext (FTS5), fuzzy, and phonetic."""
        explanation: dict[str, Any] = {
            "mode": mode,
            "fts5_available": False,
            "fts5_active": False,
            "fallback_occurred": False,
            "fallback_reason": None,
            "query_used": headword or exact_headword or meaning or "",
            "active_phonetic_rules": [],
            "filters_applied": {},
        }

        if dialect:
            explanation["filters_applied"]["dialect"] = dialect
        if source_type:
            explanation["filters_applied"]["source_type"] = source_type
        if part_of_speech:
            explanation["filters_applied"]["part_of_speech"] = part_of_speech
        if verification_status:
            explanation["filters_applied"]["verification_status"] = verification_status

        all_entries = self._get_all_entries()
        matches_info: dict[str, SearchResultMatch] = {}

        effective_mode = mode.lower().strip() if mode else "substring"
        query_text = headword or exact_headword or meaning or ""

        fts5_supported = bool(self.repository and self.repository.is_fts5_available())
        explanation["fts5_available"] = fts5_supported

        candidate_entries: list[VocabularyEntry] = []

        if effective_mode == "fulltext":
            if fts5_supported and self.repository and query_text:
                explanation["fts5_active"] = True
                fts_results = self.repository.search_fts(query_text)
                for ent, rank in fts_results:
                    if ent.license_restrictions != "restricted":
                        candidate_entries.append(ent)
                        matches_info[ent.id] = SearchResultMatch(
                            entry_id=ent.id,
                            headword=ent.headword,
                            match_mode="fulltext",
                            match_score=round(rank, 3),
                            matched_term=query_text,
                            explanation=f"FTS5 BM25 relevance score {rank:.2f}",
                            dialect=ent.dialect,
                            verification_status=ent.verification_status,
                            source_ids=[p.source_id for p in ent.provenance],
                        )
            else:
                explanation["fallback_occurred"] = True
                explanation["fallback_reason"] = (
                    "SQLite FTS5 extension is not available or query is empty; "
                    "fell back to standard substring search."
                )
                effective_mode = "substring"

        if effective_mode == "fuzzy":
            q_norm = normalize_unicode(query_text).strip().lower()
            explanation["threshold"] = threshold
            fuzzy_candidates: list[tuple[VocabularyEntry, float, str]] = []

            for entry in all_entries:
                if entry.license_restrictions == "restricted":
                    continue

                best_sim = calculate_similarity(q_norm, entry.headword)
                best_term = entry.headword

                for alt in entry.alternative_spellings:
                    alt_sim = calculate_similarity(q_norm, alt)
                    if alt_sim > best_sim:
                        best_sim = alt_sim
                        best_term = alt

                if q_norm and best_sim >= threshold:
                    fuzzy_candidates.append((entry, best_sim, best_term))

            fuzzy_candidates.sort(
                key=lambda it: (-it[1], normalize_unicode(it[0].headword).lower(), it[0].id)
            )
            for ent, sim, matched_term in fuzzy_candidates:
                candidate_entries.append(ent)
                matches_info[ent.id] = SearchResultMatch(
                    entry_id=ent.id,
                    headword=ent.headword,
                    match_mode="fuzzy",
                    match_score=round(sim, 3),
                    matched_term=matched_term,
                    explanation=f"Levenshtein similarity ratio {sim:.2f} with '{q_norm}'",
                    dialect=ent.dialect,
                    verification_status=ent.verification_status,
                    source_ids=[p.source_id for p in ent.provenance],
                )

        elif effective_mode == "phonetic":
            encoder = TangkhulPhoneticEncoder(
                include_experimental=include_experimental_phonetics
            )
            explanation["active_phonetic_rules"] = [r.id for r in encoder.active_rules]
            q_key = encoder.encode(query_text)
            explanation["phonetic_key"] = q_key
            phonetic_candidates: list[tuple[VocabularyEntry, float, str, str]] = []

            for entry in all_entries:
                if entry.license_restrictions == "restricted":
                    continue

                hw_key = encoder.encode(entry.headword)
                best_score = 0.0
                best_term = entry.headword
                matched_key = hw_key

                if q_key and q_key == hw_key:
                    best_score = 1.0
                else:
                    for alt in entry.alternative_spellings:
                        alt_k = encoder.encode(alt)
                        if q_key and q_key == alt_k:
                            best_score = max(best_score, 0.95)
                            best_term = alt
                            matched_key = alt_k

                if best_score == 0.0 and q_key:
                    if q_key in hw_key or hw_key in q_key:
                        sim = calculate_similarity(q_key, hw_key)
                        if sim >= 0.70:
                            best_score = round(sim, 2)

                if best_score > 0.0:
                    phonetic_candidates.append((entry, best_score, best_term, matched_key))

            phonetic_candidates.sort(
                key=lambda it: (-it[1], normalize_unicode(it[0].headword).lower(), it[0].id)
            )
            for ent, score, matched_term, matched_key in phonetic_candidates:
                candidate_entries.append(ent)
                matches_info[ent.id] = SearchResultMatch(
                    entry_id=ent.id,
                    headword=ent.headword,
                    match_mode="phonetic",
                    match_score=round(score, 3),
                    matched_term=matched_term,
                    explanation=(
                        f"Phonetic key '{q_key}' matched '{matched_term}' "
                        f"[key: '{matched_key}'] (score: {score:.2f})"
                    ),
                    dialect=ent.dialect,
                    verification_status=ent.verification_status,
                    source_ids=[p.source_id for p in ent.provenance],
                )

        elif effective_mode == "substring":
            hw_norm = normalize_unicode(headword).strip().lower() if headword else None
            for entry in all_entries:
                if entry.license_restrictions == "restricted":
                    continue

                matched = False
                matched_term = entry.headword
                if hw_norm:
                    if hw_norm in normalize_unicode(entry.headword).strip().lower():
                        matched = True
                        matched_term = entry.headword
                    else:
                        for alt in entry.alternative_spellings:
                            if hw_norm in normalize_unicode(alt).strip().lower():
                                matched = True
                                matched_term = alt
                                break
                else:
                    matched = True

                if matched:
                    candidate_entries.append(entry)
                    matches_info[entry.id] = SearchResultMatch(
                        entry_id=entry.id,
                        headword=entry.headword,
                        match_mode="substring",
                        match_score=1.0,
                        matched_term=matched_term,
                        explanation="Substring match on headword or alternative spelling",
                        dialect=entry.dialect,
                        verification_status=entry.verification_status,
                        source_ids=[p.source_id for p in entry.provenance],
                    )

        # Apply secondary filters
        exact_norm = normalize_unicode(exact_headword).strip().lower() if exact_headword else None
        m_norm = normalize_unicode(meaning).strip().lower() if meaning else None
        dia_norm = normalize_unicode(dialect).strip().lower() if dialect else None
        pos_norm = part_of_speech.strip().lower() if part_of_speech else None
        ver_norm = verification_status.strip().lower() if verification_status else None

        st_norm = source_type.strip().lower() if source_type else None
        if st_norm:
            aliases = {
                "book": "books",
                "song": "songs",
                "dictionary": "dictionaries",
                "cultural": "culture",
                "historical": "history",
                "literary": "literature",
            }
            st_norm = aliases.get(st_norm, st_norm)

        filtered_results: list[VocabularyEntry] = []
        for entry in candidate_entries:
            if entry.license_restrictions == "restricted":
                continue

            if ver_norm and entry.verification_status.lower() != ver_norm:
                continue

            if pos_norm and (
                not entry.part_of_speech or entry.part_of_speech.lower() != pos_norm
            ):
                continue

            if dia_norm and (
                not entry.dialect or dia_norm not in normalize_unicode(entry.dialect).lower()
            ):
                continue

            if source_id and not any(p.source_id == source_id for p in entry.provenance):
                continue

            if st_norm and not any(
                p.resource_type.lower() == st_norm for p in entry.provenance
            ):
                continue

            if exact_norm:
                head_exact = exact_norm == normalize_unicode(entry.headword).strip().lower()
                alt_exact = any(
                    exact_norm == normalize_unicode(a).strip().lower()
                    for a in entry.alternative_spellings
                )
                if not head_exact and not alt_exact:
                    continue

            if m_norm:
                matched_m = any(
                    m_norm in normalize_unicode(m).lower() for m in entry.meanings
                )
                matched_t = any(
                    m_norm in normalize_unicode(t).lower() for t in entry.translations_en
                )
                if not matched_m and not matched_t:
                    continue

            filtered_results.append(entry)

        if effective_mode not in {"fuzzy", "phonetic"}:
            filtered_results.sort(key=lambda e: (normalize_unicode(e.headword).lower(), e.id))

        if limit is not None and limit > 0:
            filtered_results = filtered_results[:limit]

        explanation["match_count"] = len(filtered_results)
        return filtered_results, matches_info, explanation

    def filter_entries(
        self,
        headword: str | None = None,
        exact_headword: str | None = None,
        meaning: str | None = None,
        dialect: str | None = None,
        part_of_speech: str | None = None,
        source_type: str | None = None,
        source_id: str | None = None,
        verification_status: str | None = None,
        limit: int | None = None,
        mode: str = "substring",
        threshold: float = 0.65,
        include_experimental_phonetics: bool = False,
    ) -> list[VocabularyEntry]:
        """Comprehensive multi-criteria filtering across unified vocabulary entries."""
        results, _, _ = self.search_with_matches(
            headword=headword,
            exact_headword=exact_headword,
            meaning=meaning,
            dialect=dialect,
            part_of_speech=part_of_speech,
            source_type=source_type,
            source_id=source_id,
            verification_status=verification_status,
            limit=limit,
            mode=mode,
            threshold=threshold,
            include_experimental_phonetics=include_experimental_phonetics,
        )
        return results


def format_search_explanation(explanation: dict[str, Any]) -> str:
    """Format structured explanation of the search strategy and execution."""
    lines: list[str] = []
    lines.append("=" * 65)
    lines.append("SEARCH STRATEGY & QUERY EXPLANATION:")
    lines.append(f"  Search Mode:       {explanation.get('mode', 'substring')}")
    query = explanation.get("query_used", "")
    lines.append(f"  Query Term:        {query if query else '(none)'}")
    lines.append(f"  FTS5 Available:    {explanation.get('fts5_available', False)}")
    lines.append(f"  FTS5 Active:       {explanation.get('fts5_active', False)}")
    if explanation.get("fallback_occurred"):
        lines.append(f"  Fallback:          {explanation.get('fallback_reason')}")
    if explanation.get("threshold") is not None:
        lines.append(f"  Fuzzy Threshold:   {explanation.get('threshold')}")
    if explanation.get("phonetic_key"):
        lines.append(f"  Phonetic Key:      {explanation.get('phonetic_key')}")
    rules = explanation.get("active_phonetic_rules", [])
    if rules:
        lines.append(f"  Phonetic Rules:    {', '.join(rules)}")
    filters = explanation.get("filters_applied", {})
    if filters:
        filter_str = ", ".join(f"{k}='{v}'" for k, v in filters.items())
        lines.append(f"  Filters Applied:   {filter_str}")
    lines.append(f"  Total Matches:     {explanation.get('match_count', 0)}")
    lines.append("=" * 65)
    return "\n".join(lines)


def format_vocabulary_entry(
    entry: VocabularyEntry,
    manifest_repo: ManifestRepository | None = None,
    match: SearchResultMatch | None = None,
) -> str:
    """Format a single vocabulary entry with all available metadata and provenance."""
    lines: list[str] = []
    lines.append("=" * 65)
    lines.append(f"Headword:        {entry.headword}")
    lines.append(f"ID:              {entry.id}")

    pos_str = entry.part_of_speech if entry.part_of_speech else "None recorded"
    lines.append(f"Part of Speech:  {pos_str}")

    dia_str = entry.dialect if entry.dialect else "Not specified"
    lines.append(f"Dialect/Village: {dia_str}")

    if entry.pronunciation:
        lines.append(f"Pronunciation:   {entry.pronunciation}")

    lines.append(f"Verification:    {entry.verification_status}")

    if match:
        lines.append(f"Match Strategy:  {match.match_mode} (Score: {match.match_score})")
        lines.append(f"Matched Term:    {match.matched_term}")
        lines.append(f"Match Detail:    {match.explanation}")

    if entry.meanings:
        lines.append("Meanings:")
        for m in entry.meanings:
            lines.append(f"  - {m}")
    else:
        lines.append("Meanings:        None recorded")

    if entry.translations_en:
        lines.append(f"Translations:    {', '.join(entry.translations_en)}")

    if entry.alternative_spellings:
        lines.append(f"Alt Spellings:   {', '.join(entry.alternative_spellings)}")
    else:
        lines.append("Alt Spellings:   None recorded")

    if entry.dialect_variants:
        lines.append(f"Dialect Variants:{', '.join(entry.dialect_variants)}")

    # Omit restricted example sentences
    safe_examples = [
        ex for ex in entry.example_sentences
        if entry.license_restrictions != "restricted"
    ]
    if safe_examples:
        lines.append("Example Sentences:")
        for ex in safe_examples:
            lines.append(f'  • "{ex}"')
    else:
        lines.append("Example Sentence: None recorded")

    if entry.provenance:
        lines.append(f"Provenance ({len(entry.provenance)} source(s)):")
        for idx, prov in enumerate(entry.provenance, start=1):
            manifest = manifest_repo.get_by_id(prov.source_id) if manifest_repo else None
            src_title = manifest.title if manifest else prov.citation
            creator = manifest.creator if (manifest and manifest.creator) else "Not recorded"
            year = (
                str(manifest.year)
                if (manifest and manifest.year)
                else (str(prov.recorded_year) if prov.recorded_year else "Not recorded")
            )
            section = prov.page_or_section if prov.page_or_section else "Not specified"
            license_val = (
                manifest.license if (manifest and manifest.license) else "Not recorded"
            )
            perm_str = prov.permission_status if prov.permission_status else "Not recorded"

            lines.append(f"  [{idx}] Source ID:       {prov.source_id}")
            lines.append(f"      Source Title:    {src_title}")
            lines.append(f"      Source Type:     {prov.resource_type}")
            lines.append(f"      Creator/Author:  {creator}")
            lines.append(f"      Year:            {year}")
            lines.append(f"      Reference:       {section}")
            lines.append(f"      Citation:        {prov.citation}")
            lines.append(f"      License:         {license_val}")
            lines.append(f"      Permissions:     {perm_str}")
            if prov.context_sentence and prov.permission_status != "restricted":
                lines.append(f'      Context:         "{prov.context_sentence}"')
    else:
        lines.append("Provenance:      No provenance records attached")

    lines.append("=" * 65)
    return "\n".join(lines)


def load_unified_vocabulary_engine(
    config: LibraryConfig | None = None,
    auto_sync_if_empty: bool = True,
) -> VocabularySearchEngine:
    """Load or initialize the unified vocabulary search engine from the database.

    If the database exists and contains entries, it queries them directly.
    If the database is not yet initialized or is empty, it initializes the schema
    and populates permitted vocabulary entries from the six manifest catalogues.
    """
    from tangkhul_lib.core.config import LibraryConfig as ConfigClass
    from tangkhul_lib.storage.database import DatabaseManager
    from tangkhul_lib.storage.repositories import ManifestRepository, VocabularyRepository

    cfg = config or ConfigClass.from_environment()
    db_file = cfg.get_database_path()

    try:
        db_file.parent.mkdir(parents=True, exist_ok=True)
        db_manager = DatabaseManager(db_file)
        db_manager.initialize_schema()
        vocab_repo = VocabularyRepository(db_manager)
        manifest_repo = ManifestRepository(db_manager)
    except Exception:
        db_manager = DatabaseManager(":memory:")
        db_manager.initialize_schema()
        vocab_repo = VocabularyRepository(db_manager)
        manifest_repo = ManifestRepository(db_manager)

    vocab_count = vocab_repo.count()
    if vocab_count == 0 and auto_sync_if_empty:
        _populate_initial_vocabulary(db_manager, vocab_repo, manifest_repo, cfg)
        vocab_count = vocab_repo.count()

    if vocab_repo.is_fts5_available():
        vocab_repo.ensure_fts_schema()
        # Backfill if FTS is empty and vocabulary entries exist
        with db_manager.get_connection() as conn:
            try:
                cur = conn.execute("SELECT COUNT(*) FROM vocabulary_fts;")
                fts_count = cur.fetchone()[0]
                if fts_count == 0 and vocab_count > 0:
                    vocab_repo.rebuild_fts_index()
            except Exception:
                pass

    return VocabularySearchEngine(repository=vocab_repo, manifest_repository=manifest_repo)


def _populate_initial_vocabulary(
    db_manager: DatabaseManager,
    vocab_repo: VocabularyRepository,
    manifest_repo: ManifestRepository,
    config: LibraryConfig,
) -> None:
    """Populate foundational vocabulary entries across all six domain modules."""
    # 0. Load self-contained bundled vocabulary from package data
    bundled_jsonl = config.paths.package_data_dir / "vocabulary.jsonl"
    if bundled_jsonl.is_file():
        from tangkhul_lib.vocabulary.bundled import load_bundled_vocabulary

        for entry in load_bundled_vocabulary():
            try:
                vocab_repo.add(entry)
            except Exception:
                pass

    manifests_dir = config.paths.manifests_dir
    if not manifests_dir.is_dir():
        return

    from tangkhul_lib.ingestion.metadata_validation import validate_all_manifests

    # Synchronize all 6 manifests into SQLite manifest_records repository
    try:
        manifest_map = validate_all_manifests(manifests_dir)
        for _, records in manifest_map.items():
            for rec in records:
                manifest_repo.add(rec)
    except Exception:
        pass

    from tangkhul_lib.core.models import ProvenanceRecord, VocabularyEntry
    from tangkhul_lib.culture.catalogue import CultureCatalogue
    from tangkhul_lib.dictionaries.models import (
        DictionaryEntryRecord,
        DictionarySourceRecord,
    )
    from tangkhul_lib.history.catalogue import HistoryCatalogue
    from tangkhul_lib.literature.catalogue import LiteratureCatalogue
    from tangkhul_lib.storage.repositories import (
        CultureRepository,
        DictionaryRepository,
        HistoryRepository,
        LiteratureRepository,
    )

    # 1. Foundational Dictionary entries (Pettigrew 1918)
    dict_repo = DictionaryRepository(db_manager)
    dict_src = DictionarySourceRecord(
        id="DIC-HIST-001",
        title="Tangkhul Naga Grammar and Dictionary (Ukhrul Dialect)",
        authors=["William Pettigrew"],
        publication_year=1918,
        publisher="Assam Secretariat Printing Office",
        languages=["Tangkhul", "English"],
        language_pair="Tangkhul-English",
        dialect="Ukhrul",
        permission_status="public_domain",
        verification_status="verified",
    )
    dict_repo.add(dict_src)

    dict_entries = [
        DictionaryEntryRecord(
            id="DIC-HIST-001-ENT-0001",
            dictionary_id="DIC-HIST-001",
            headword="khararchan",
            definitions_en=["folk-tale", "legend", "ancestral fable"],
            part_of_speech="noun",
            page_or_section="p. 320",
            permission_status="public_domain",
            verification_status="verified",
        ),
        DictionaryEntryRecord(
            id="DIC-HIST-001-ENT-0002",
            dictionary_id="DIC-HIST-001",
            headword="khamor",
            definitions_en=["mouth", "speech", "oral word"],
            part_of_speech="noun",
            page_or_section="p. 285",
            permission_status="public_domain",
            verification_status="verified",
        ),
        DictionaryEntryRecord(
            id="DIC-HIST-001-ENT-0003",
            dictionary_id="DIC-HIST-001",
            headword="ngashān",
            alternate_spellings=["ngashan"],
            definitions_en=["custom", "traditional practice", "clan law"],
            part_of_speech="noun",
            page_or_section="p. 250",
            dialect="Ukhrul",
            permission_status="public_domain",
            verification_status="verified",
        ),
    ]
    for de in dict_entries:
        try:
            dict_repo.sync_entry_to_vocabulary(de, vocab_repo)
        except Exception:
            pass

    # 2. Foundational Books entries (Pettigrew 1918 & Grammar)
    book_entries = [
        VocabularyEntry(
            id="VOC-BK-0001",
            headword="shim",
            meanings=["house", "dwelling place", "home"],
            translations_en=["house", "home"],
            part_of_speech="noun",
            dialect="Ukhrul",
            example_sentences=["Ili shimli kaphan."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 12",
                    page_or_section="p. 12",
                    context_sentence="Ili shimli kaphan.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="verified",
        ),
        VocabularyEntry(
            id="VOC-BK-0002",
            headword="phung",
            meanings=["mountain", "hill; carry on back"],
            translations_en=["mountain", "hill"],
            part_of_speech="noun",
            dialect="Ukhrul",
            example_sentences=["Kaphung kazing rali mayaron kakhang."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 28",
                    page_or_section="p. 28",
                    context_sentence="Kaphung kazing rali mayaron kakhang.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="verified",
        ),
        VocabularyEntry(
            id="VOC-BK-0003",
            headword="ot",
            meanings=["work", "labor", "deed"],
            translations_en=["work", "deed"],
            part_of_speech="noun",
            dialect="Ukhrul",
            example_sentences=["Ot kasa kaphan."],
            provenance=[
                ProvenanceRecord(
                    source_id="BK-HIST-001",
                    resource_type="books",
                    citation="Tangkhul Naga Grammar and Dictionary (Pettigrew 1918), p. 15",
                    page_or_section="p. 15",
                    context_sentence="Ot kasa kaphan.",
                    recorded_year=1918,
                    permission_status="public_domain",
                )
            ],
            verification_status="verified",
        ),
    ]
    for be in book_entries:
        try:
            existing = vocab_repo.search_exact(be.headword)
            if existing:
                ent = existing[0]
                for prov in be.provenance:
                    if not any(p.source_id == prov.source_id and p.page_or_section == prov.page_or_section for p in ent.provenance):
                        ent.provenance.append(prov)
                for ex in be.example_sentences:
                    if ex not in ent.example_sentences:
                        ent.example_sentences.append(ex)
                vocab_repo.add(ent)
            else:
                vocab_repo.add(be)
        except Exception:
            pass

    # 3. Foundational Songs entries (Traditional Ballads)
    song_entries = [
        VocabularyEntry(
            id="VOC-SNG-0001",
            headword="laa",
            meanings=["song", "hymn", "chanted melody"],
            translations_en=["song", "melody"],
            part_of_speech="noun",
            dialect="Standard Tangkhul",
            example_sentences=["Ashang Aton Laa khangasham."],
            provenance=[
                ProvenanceRecord(
                    source_id="SNG-TRAD-001",
                    resource_type="songs",
                    citation="Shimreishang Kala Maitonphi (Traditional Ballad), Phungcham",
                    page_or_section="Stanza 1",
                    context_sentence="Ashang Aton Laa khangasham.",
                    permission_status="community_authorized",
                )
            ],
            verification_status="verified",
        ),
        VocabularyEntry(
            id="VOC-SNG-0002",
            headword="leishat",
            meanings=["love", "affection", "devotion"],
            translations_en=["love", "affection"],
            part_of_speech="noun",
            dialect="Standard Tangkhul",
            example_sentences=["Ina naoli leishat mathamei."],
            provenance=[
                ProvenanceRecord(
                    source_id="SNG-TRAD-001",
                    resource_type="songs",
                    citation="Shimreishang Kala Maitonphi (Traditional Ballad), Phungcham",
                    page_or_section="Stanza 3",
                    context_sentence="Ina naoli leishat mathamei.",
                    permission_status="community_authorized",
                )
            ],
            verification_status="verified",
        ),
    ]
    for se in song_entries:
        try:
            existing = vocab_repo.search_exact(se.headword)
            if existing:
                ent = existing[0]
                for prov in se.provenance:
                    if not any(p.source_id == prov.source_id and p.page_or_section == prov.page_or_section for p in ent.provenance):
                        ent.provenance.append(prov)
                for ex in se.example_sentences:
                    if ex not in ent.example_sentences:
                        ent.example_sentences.append(ex)
                vocab_repo.add(ent)
            else:
                vocab_repo.add(se)
        except Exception:
            pass

    # 4. Culture records
    cult_path = manifests_dir / "culture.jsonl"
    if cult_path.is_file():
        cr = CultureRepository(db_manager)
        cc = CultureCatalogue.load_from_manifest(cult_path)
        for r in cc.list_records():
            if r.permission_status != "restricted":
                try:
                    cr.sync_record_to_vocabulary(r, vocab_repo)
                except Exception:
                    pass

    # 5. History records
    hist_path = manifests_dir / "history.jsonl"
    if hist_path.is_file():
        hr = HistoryRepository(db_manager)
        hc = HistoryCatalogue.load_from_manifest(hist_path)
        for r in hc.list_records():
            if r.permission_status != "restricted":
                try:
                    hr.sync_record_to_vocabulary(r, vocab_repo)
                except Exception:
                    pass

    # 6. Literature records
    lit_path = manifests_dir / "literature.jsonl"
    if lit_path.is_file():
        lr = LiteratureRepository(db_manager)
        lc = LiteratureCatalogue.load_from_manifest(lit_path)
        for r in lc.list_works():
            if r.permission_status != "restricted":
                try:
                    lr.sync_record_to_vocabulary(r, vocab_repo)
                except Exception:
                    pass
