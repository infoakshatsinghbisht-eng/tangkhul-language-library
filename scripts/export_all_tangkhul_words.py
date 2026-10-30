"""Comprehensive Tangkhul Language Vocabulary Extraction Engine.

Extracts all authentic Tangkhul language words across all digitized datasets:
1. Master Dictionary (tangkhul_master_dictionary_deduplicated.json)
2. 35 Published Books (data/exports/books.json)
3. 60 Literary Works (data/exports/literature.json)
4. 48 Traditional & Modern Songs (data/exports/songs.json)
5. 35 Cultural Heritage Records (data/exports/culture.json)
6. 32 Historical Chronicles (data/exports/history.json)
7. 400 Grand Folk Riddles (data/exports/tangkhul_400_folk_riddles_grand_collection.json)
8. 35 Traditional Proverbs & Idioms (data/exports/tangkhul_proverbs_and_idioms_master.json)
9. Sacred Scriptures & Classical Epics (data/exports/tangkhul_sacred_scriptures_and_epics_collection.json)
10. Prayers, Rituals & Clan System Encyclopedia (data/exports/tangkhul_prayers_rituals_and_clans_master_encyclopedia.json)
11. Linguistic Encyclopedia & Number System (data/exports/tangkhul_linguistic_encyclopedia_and_number_system.json)
12. 16 Lexicographical Dictionaries (data/exports/dictionaries.json)
13. 1907 Complete Tangkhul Hymnal (data/raw/hymns_1907_full.txt)
14. 184 Raw Corpus Text Archives (data/raw/*/*.txt)

Outputs:
- data/exports/tangkhul_all_extracted_words.json
- data/exports/tangkhul_all_extracted_words.tsv
- data/exports/tangkhul_all_extracted_words.csv
- data/exports/TANGKHUL_EXTRACTED_WORDS_CATALOG.md
- SQLite table 'extracted_tangkhul_words' in both database files.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Ensure UTF-8 output on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# Standard English stopwords and structural metadata tokens to prevent lexical leakage
ENGLISH_STOPWORDS = {
    "a", "about", "above", "across", "after", "afterwards", "again", "against", "all",
    "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
    "amongst", "amount", "an", "and", "another", "answer", "any", "anyhow", "anyone",
    "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be",
    "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
    "behind", "being", "below", "beside", "besides", "between", "beyond", "both", "bottom",
    "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt",
    "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each",
    "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc",
    "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few",
    "fifteen", "fifty", "fill", "find", "fire", "first", "five", "for", "former",
    "formerly", "forty", "found", "four", "from", "front", "full", "further", "get",
    "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
    "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
    "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest",
    "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least",
    "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine",
    "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself",
    "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody",
    "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often",
    "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please",
    "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
    "serious", "several", "she", "should", "show", "side", "since", "sincere", "six",
    "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes",
    "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the",
    "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third",
    "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to",
    "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un",
    "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were",
    "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas",
    "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within",
    "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves",
    # Specific English words from titles, metadata, and structural headers
    "page", "chapter", "section", "entry", "citation", "example", "dictionary", "grammar",
    "noun", "verb", "adjective", "adverb", "pronoun", "preposition", "conjunction",
    "interjection", "title", "translation", "translator", "publisher", "published",
    "author", "compiler", "collector", "village", "dialect", "language", "license",
    "status", "review", "reviewer", "notes", "context", "alt", "genre", "stanzas",
    "verse", "verses", "lines", "proverb", "riddle", "folklore", "oral", "tradition",
    "historical", "chronicle", "ceremony", "festival", "ritual", "prayer", "clan",
    "academic", "copyright", "archive", "library", "source", "identifier", "url",
    "preservation", "digital", "record", "overview", "background", "classification",
    "district", "manipur", "india", "shillong", "assam", "pettigrew", "rev", "william",
    "arokianathan", "hodson", "mcculloch", "brown", "damant", "grierson", "luikham",
    "bhat", "mortensen", "ciil", "tls", "nbp", "soas", "stedt", "tddp", "unknown",
    "poetic", "literary", "ancestral", "traditional", "english", "hindi", "en", "hi",
    "meaning", "meanings", "word", "words", "sentence", "sentences", "question", "questions",
    "answer", "answers", "total", "count", "high", "low", "mountain", "hill", "river",
    "tree", "house", "village", "rock", "stone", "water", "fire", "earth", "sky",
    "heaven", "god", "spirit", "man", "woman", "child", "boy", "girl", "father",
    "mother", "brother", "sister", "son", "daughter", "king", "chief", "people"
}

# Regex to match Tangkhul words: Latin alphabetic characters including macrons, eng (ŋ), retroflex (ṇ), etc.
WORD_RE = re.compile(r"[A-Za-z\u00C0-\u024F\u1E00-\u1EFF]+(?:['’\-][A-Za-z\u00C0-\u024F\u1E00-\u1EFF]+)*")

def clean_word(w: str) -> str:
    """Strip extraneous typographical symbols, numbering, and edge punctuation."""
    w = w.strip(".,;:!?\"'()[]{}«»—– \t\n\r*~`#^/\\0123456789§†‡_")
    w = re.sub(r"^['’\-]+|['’\-]+$", "", w)
    return w

class TangkhulLexiconExtractor:
    def __init__(self):
        self.frequencies: Counter[str] = Counter()
        self.sources: defaultdict[str, set[str]] = defaultdict(set)
        self.verbatim_forms: defaultdict[str, Counter[str]] = defaultdict(Counter)
        self.examples: dict[str, str] = {}
        self.parts_of_speech: dict[str, str] = {}
        self.meanings: dict[str, str] = {}

    def record_word(self, raw_w: str, source_label: str, context: str = "", pos: str = "", meaning: str = ""):
        cleaned = clean_word(raw_w)
        if not cleaned or len(cleaned) < 1:
            return
        norm = cleaned.lower()
        if norm in ENGLISH_STOPWORDS or norm == "a":
            return
        # Every authentic Tangkhul word must contain at least one vowel
        vowels = "aeiouāēīōūáéíóúäëïöüâêîôûãõạẹịọụ"
        if not any(c in vowels for c in norm):
            return
        # In Tangkhul orthography, 'i' is the only valid single-character word (1st person pronoun "I")
        if len(norm) == 1 and norm != "i":
            return
        if re.fullmatch(r"[ivxlcdm]+", norm) and norm in {"ii", "iii", "iv", "vi", "vii", "viii", "ix", "xi", "xii", "xv", "xx"}:
            return
        
        self.frequencies[norm] += 1
        self.sources[norm].add(source_label)
        self.verbatim_forms[norm][cleaned] += 1
        
        if context and norm not in self.examples:
            self.examples[norm] = context[:140].replace("\n", " ").strip()
        if pos and norm not in self.parts_of_speech:
            self.parts_of_speech[norm] = pos
        if meaning and norm not in self.meanings:
            self.meanings[norm] = meaning

    def extract_from_text(self, text, source_label: str, pos: str = "", meaning: str = ""):
        if not text:
            return
        if isinstance(text, list):
            for item in text:
                self.extract_from_text(item, source_label, pos, meaning)
            return
        if not isinstance(text, str):
            return
        for m in WORD_RE.finditer(text):
            w = m.group()
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            ctx = text[start:end]
            self.record_word(w, source_label, ctx, pos, meaning)

    def process_all_corpora(self):
        print("Processing Master Dictionary...")
        mdict_path = ROOT / "data" / "exports" / "tangkhul_master_dictionary_deduplicated.json"
        if mdict_path.exists():
            with open(mdict_path, "r", encoding="utf-8") as f:
                mdict = json.load(f)
            for e in mdict.get("entries", []):
                src = e.get("source", "")
                tk = e.get("tangkhul", "")
                en = e.get("english", "")
                pos = e.get("pos", "")
                if "pettigrew_page_" in src:
                    try:
                        p = int(src.split("_")[-1])
                    except:
                        p = 0
                    if p >= 233:
                        self.extract_from_text(en, f"master_dict:{src}", pos, tk)
                    else:
                        self.extract_from_text(tk, f"master_dict:{src}", pos, en)
                else:
                    self.extract_from_text(tk, f"master_dict:{src}", pos, en)

        print("Processing Published Books...")
        books_path = ROOT / "data" / "exports" / "books.json"
        if books_path.exists():
            with open(books_path, "r", encoding="utf-8") as f:
                books = json.load(f)
            for b in books:
                b_id = b.get("id", "BK")
                for ch in b.get("chapters", []):
                    self.extract_from_text(ch.get("tangkhul_text"), f"book:{b_id}")
                    self.extract_from_text(ch.get("comprehension_questions"), f"book:{b_id}")
                    self.extract_from_text(ch.get("title"), f"book:{b_id}")
                    for v in ch.get("vocabulary", []):
                        if isinstance(v, dict):
                            self.extract_from_text(v.get("word"), f"book_vocab:{b_id}", v.get("pos", ""), v.get("meaning", ""))

        print("Processing Literature...")
        lit_path = ROOT / "data" / "exports" / "literature.json"
        if lit_path.exists():
            with open(lit_path, "r", encoding="utf-8") as f:
                lit = json.load(f)
            for l in lit:
                l_id = l.get("id", "LIT")
                self.extract_from_text(l.get("indigenous_tangkhul_text"), f"literature:{l_id}")
                self.extract_from_text(l.get("title_tangkhul"), f"literature:{l_id}")
                self.extract_from_text(l.get("poetic_vocabulary_terms"), f"literature_vocab:{l_id}")

        print("Processing Songs...")
        songs_path = ROOT / "data" / "exports" / "songs.json"
        if songs_path.exists():
            with open(songs_path, "r", encoding="utf-8") as f:
                songs = json.load(f)
            for s in songs:
                s_id = s.get("id", "SNG")
                self.extract_from_text(s.get("title"), f"song:{s_id}")
                for st in s.get("lyrics_stanzas", []):
                    self.extract_from_text(st.get("lines_tangkhul"), f"song:{s_id}")

        print("Processing Culture...")
        culture_path = ROOT / "data" / "exports" / "culture.json"
        if culture_path.exists():
            with open(culture_path, "r", encoding="utf-8") as f:
                culture = json.load(f)
            for c in culture:
                c_id = c.get("id", "CULT")
                self.extract_from_text(c.get("indigenous_tangkhul_text"), f"culture:{c_id}")

        print("Processing History...")
        history_path = ROOT / "data" / "exports" / "history.json"
        if history_path.exists():
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            for h in history:
                h_id = h.get("id", "HIST")
                self.extract_from_text(h.get("indigenous_tangkhul_chronicle"), f"history:{h_id}")
                if isinstance(h.get("historical_terms"), dict):
                    for term, mean in h["historical_terms"].items():
                        self.extract_from_text(term, f"history_term:{h_id}", "noun", mean)

        print("Processing 400 Folk Riddles...")
        riddles_path = ROOT / "data" / "exports" / "tangkhul_400_folk_riddles_grand_collection.json"
        if riddles_path.exists():
            with open(riddles_path, "r", encoding="utf-8") as f:
                riddles = json.load(f)
            for r in riddles.get("riddles", []):
                self.extract_from_text(r.get("tangkhul_riddle"), "riddles")
                self.extract_from_text(r.get("answer_tangkhul"), "riddles")
                self.extract_from_text(r.get("formula"), "riddles")

        print("Processing Proverbs & Idioms...")
        proverbs_path = ROOT / "data" / "exports" / "tangkhul_proverbs_and_idioms_master.json"
        if proverbs_path.exists():
            with open(proverbs_path, "r", encoding="utf-8") as f:
                proverbs = json.load(f)
            for p in proverbs.get("proverbs", []):
                self.extract_from_text(p.get("tangkhul"), "proverbs")

        print("Processing Sacred Scriptures & Classical Epics...")
        scrip_path = ROOT / "data" / "exports" / "tangkhul_sacred_scriptures_and_epics_collection.json"
        if scrip_path.exists():
            with open(scrip_path, "r", encoding="utf-8") as f:
                scrip = json.load(f)
            w = scrip.get("works", {})
            for sec in w.get("bible", {}).get("sections", []):
                for v in sec.get("verses", []):
                    self.extract_from_text(v.get("tangkhul"), "bible")
            for kan in w.get("ramayana", {}).get("kandas", []):
                for st in kan.get("stanzas", []):
                    self.extract_from_text(st.get("tangkhul"), "ramayana")
            for prv in w.get("mahabharata", {}).get("parvas", []):
                for st in prv.get("stanzas", []):
                    self.extract_from_text(st.get("tangkhul"), "mahabharata")
            for ch in w.get("bhagavad_gita", {}).get("chapters", []):
                for v in ch.get("verses", []):
                    self.extract_from_text(v.get("tangkhul"), "bhagavad_gita")

        print("Processing Prayers, Rituals & Clan System...")
        prayers_path = ROOT / "data" / "exports" / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.json"
        if prayers_path.exists():
            with open(prayers_path, "r", encoding="utf-8") as f:
                prayers = json.load(f)
            mods = prayers.get("modules", {})
            for sec in mods.get("prayers_and_invocations", {}).get("prayer_sections", []):
                for p in sec.get("prayers", []):
                    self.extract_from_text(p.get("tangkhul"), "prayers")
            for cyc in mods.get("rituals_and_ceremonies", {}).get("ceremonial_cycles", []):
                for rite in cyc.get("rites", []):
                    self.extract_from_text(rite.get("tangkhul_chants"), "rituals")
                    self.extract_from_text(rite.get("tangkhul"), "rituals")
            for clan in mods.get("clans_and_social_structure", {}).get("major_clans", []):
                self.extract_from_text(clan.get("clan_name"), "clans")

        print("Processing Linguistic Encyclopedia & Number System...")
        ling_path = ROOT / "data" / "exports" / "tangkhul_linguistic_encyclopedia_and_number_system.json"
        if ling_path.exists():
            with open(ling_path, "r", encoding="utf-8") as f:
                ling = json.load(f)
            def walk_ling(obj, path):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k in {"tangkhul", "tangkhul_name", "tangkhul_term", "tangkhul_text"}:
                            self.extract_from_text(v, f"ling:{path}")
                        else:
                            walk_ling(v, f"{path}.{k}")
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        walk_ling(item, f"{path}[{idx}]")
            walk_ling(ling.get("sections", {}), "ling")

        print("Processing Lexicographical Dictionaries...")
        dicts_path = ROOT / "data" / "exports" / "dictionaries.json"
        if dicts_path.exists():
            with open(dicts_path, "r", encoding="utf-8") as f:
                dicts = json.load(f)
            for d in dicts:
                d_id = d.get("id", "DIC")
                for ent in d.get("entries", []):
                    hw = ent.get("headword")
                    if hw:
                        self.extract_from_text(hw, f"dict:{d_id}", ent.get("part_of_speech", ""), "; ".join(ent.get("definitions_en", [])))
                    for ex in ent.get("examples", []):
                        if isinstance(ex, dict):
                            ex_text = ex.get("sentence") or ex.get("tangkhul") or ex.get("example")
                        elif isinstance(ex, str):
                            ex_text = ex.split("(")[0].strip()
                        else:
                            ex_text = ""
                        if ex_text:
                            self.extract_from_text(ex_text, f"dict_ex:{d_id}")

        print("Processing Libriary2 Literature & Idioms...")
        l2_lit_path = ROOT / "data" / "exports" / "digitized_libriary2_literature.json"
        if l2_lit_path.exists():
            with open(l2_lit_path, "r", encoding="utf-8") as f:
                l2_lit = json.load(f)
            for item in l2_lit:
                self.extract_from_text(item.get("tangkhul_text"), "libriary2_lit")
                self.extract_from_text(item.get("title_tangkhul"), "libriary2_lit")

        l2_idioms_path = ROOT / "data" / "exports" / "digitized_libriary2_idioms.json"
        if l2_idioms_path.exists():
            with open(l2_idioms_path, "r", encoding="utf-8") as f:
                l2_idioms = json.load(f)
            for item in l2_idioms:
                self.extract_from_text(item.get("tangkhul"), "libriary2_idioms", meaning=item.get("english", ""))

        print("Processing Research & Cultural Articles...")
        articles_path = ROOT / "data" / "exports" / "articles.json"
        if articles_path.exists():
            with open(articles_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
            for art in articles:
                aid = art.get("id", "ART")
                for s in art.get("sections", []):
                    for d in s.get("tangkhul_data", []):
                        tk = d.get("tangkhul", "")
                        tk_pure = re.sub(r'\([^)]*\)', '', tk)
                        for item in re.split(r'[/,;\s]+', tk_pure):
                            if item.strip():
                                self.extract_from_text(item, f"article_data:{aid}", meaning=d.get("gloss", ""))
                for p in art.get("pages", []):
                    tk_cont = p.get("tangkhul_content", "")
                    if tk_cont:
                        self.extract_from_text(tk_cont, f"article_page:{aid}")

        print("Processing Comprehensive & Descriptive Grammars...")
        gram_path = ROOT / "data" / "exports" / "tangkhul_comprehensive_grammar.json"
        if gram_path.exists():
            with open(gram_path, "r", encoding="utf-8") as f:
                gram = json.load(f)
            for ch in gram.get("chapters", []):
                for sec in ch.get("sections", []):
                    for rule in sec.get("rules", []):
                        for match in re.findall(r"'([^']+)'", rule):
                            self.extract_from_text(match, "grammar")

        l2_gram_path = ROOT / "data" / "exports" / "digitized_libriary2_grammar.json"
        if l2_gram_path.exists():
            with open(l2_gram_path, "r", encoding="utf-8") as f:
                l2_gram = json.load(f)
            for k, sec in l2_gram.items():
                if isinstance(sec, dict):
                    for ex in sec.get("examples", []):
                        if isinstance(ex, dict):
                            self.extract_from_text(ex.get("tangkhul_masc"), "grammar")
                            self.extract_from_text(ex.get("tangkhul_fem"), "grammar")
                            self.extract_from_text(ex.get("tangkhul"), "grammar")

        print("Processing 1907 Complete Tangkhul Hymnal...")
        hymns_path = ROOT / "data" / "raw" / "hymns_1907_full.txt"
        if hymns_path.exists():
            with open(hymns_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    l_str = line.strip()
                    if l_str and not l_str.isupper() and not l_str.startswith("HYMN"):
                        self.extract_from_text(l_str, "hymns_1907")

        print("Processing Raw Corpus Archives (184 text files)...")
        for rf in (ROOT / "data" / "raw").rglob("*.txt"):
            if rf.name == "hymns_1907_full.txt":
                continue
            try:
                with open(rf, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                in_tangkhul = False
                for line in lines:
                    line_s = line.strip()
                    if any(h in line_s.upper() for h in ["INDIGENOUS TANGKHUL", "TANGKHUL:", "LINES TANGKHUL:"]):
                        in_tangkhul = True
                        continue
                    elif any(h in line_s.upper() for h in ["ENGLISH TRANSLATION", "ENGLISH RENDITION", "METADATA", "SECTION 1:", "SECTION 3:", "===="]):
                        in_tangkhul = False
                        continue
                    if in_tangkhul and line_s and not line_s.startswith("#") and not line_s.startswith("-"):
                        self.extract_from_text(line_s, f"raw:{rf.stem}")
            except Exception:
                pass

        print(f"Extraction complete: {len(self.frequencies)} unique Tangkhul words found across {sum(self.frequencies.values())} tokens.")

    def compile_catalog(self) -> list[dict]:
        """Compile ranked lexicon records with full provenance."""
        catalog = []
        for rank, (norm_w, count) in enumerate(self.frequencies.most_common(), 1):
            verbatim = self.verbatim_forms[norm_w].most_common(1)[0][0] if self.verbatim_forms[norm_w] else norm_w
            pos = self.parts_of_speech.get(norm_w, "")
            meaning = self.meanings.get(norm_w, "")
            example = self.examples.get(norm_w, "")
            src_list = sorted(self.sources[norm_w])
            
            record = {
                "rank": rank,
                "word": norm_w,
                "canonical_form": verbatim,
                "frequency": count,
                "source_count": len(src_list),
                "part_of_speech": pos,
                "meaning": meaning,
                "example_sentence": example,
                "sources": src_list[:10]  # Store top 10 sources
            }
            catalog.append(record)
        return catalog

def export_results(catalog: list[dict], total_tokens: int):
    exports_dir = ROOT / "data" / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. JSON Export
    json_path = exports_dir / "tangkhul_all_extracted_words.json"
    print(f"Exporting JSON catalog to {json_path.name}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": "Complete Tangkhul Language Extracted Lexicon Catalog",
            "total_unique_words": len(catalog),
            "total_corpus_tokens": total_tokens,
            "provenance": "Extracted from 14 digitized library resources across dictionaries, literature, songs, books, culture, history, scriptures, riddles, proverbs, prayers, and hymnals.",
            "words": catalog
        }, f, ensure_ascii=False, indent=2)

    # 2. TSV Export
    tsv_path = exports_dir / "tangkhul_all_extracted_words.tsv"
    print(f"Exporting TSV catalog to {tsv_path.name}...")
    with open(tsv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["rank", "word", "canonical_form", "frequency", "source_count", "part_of_speech", "meaning", "example_sentence", "sources"])
        for item in catalog:
            writer.writerow([
                item["rank"],
                item["word"],
                item["canonical_form"],
                item["frequency"],
                item["source_count"],
                item["part_of_speech"],
                item["meaning"],
                item["example_sentence"],
                "; ".join(item["sources"])
            ])

    # 3. CSV Export (UTF-8 with BOM for Excel)
    csv_path = exports_dir / "tangkhul_all_extracted_words.csv"
    print(f"Exporting CSV catalog to {csv_path.name}...")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "word", "canonical_form", "frequency", "source_count", "part_of_speech", "meaning", "example_sentence", "sources"])
        for item in catalog:
            writer.writerow([
                item["rank"],
                item["word"],
                item["canonical_form"],
                item["frequency"],
                item["source_count"],
                item["part_of_speech"],
                item["meaning"],
                item["example_sentence"],
                "; ".join(item["sources"])
            ])

    # 4. Comprehensive Markdown Documentation Catalog
    md_path = exports_dir / "TANGKHUL_EXTRACTED_WORDS_CATALOG.md"
    print(f"Exporting Markdown summary to {md_path.name}...")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Complete Tangkhul Language Extracted Lexicon Catalog\n\n")
        f.write("## 1. Overview & Statistics\n\n")
        f.write(f"- **Total Unique Authentic Tangkhul Words**: `{len(catalog):,}`\n")
        f.write(f"- **Total Corpus Token Occurrences**: `{total_tokens:,}`\n")
        f.write("- **Orthography**: Standard Ukhrul Tangkhul Latin orthography with phonetic diacritics (`ā`, `ē`, `ī`, `ō`, `ū`, `ŋ`, `ṇ`).\n")
        f.write("- **Scope of Extraction**: Exhaustive analysis across all 14 library domains (Dictionaries, Published Books, Literature, Songs, Cultural Records, Historical Chronicles, 400 Folk Riddles, Proverbs, Scriptures & Epics, Prayers & Clans, Linguistic Encyclopedia, and 1907 Hymnal).\n\n")
        
        f.write("## 2. Top 100 Most Frequent Tangkhul Words\n\n")
        f.write("| Rank | Word | Canonical Form | Frequency | Sources | Part of Speech | English Gloss / Meaning |\n")
        f.write("|:---:|:---|:---|:---:|:---:|:---:|:---|\n")
        for item in catalog[:100]:
            meaning_short = item["meaning"][:50].replace("|", "\\|") if item["meaning"] else "—"
            pos_short = item["part_of_speech"] if item["part_of_speech"] else "—"
            f.write(f"| {item['rank']} | **{item['word']}** | {item['canonical_form']} | {item['frequency']:,} | {item['source_count']} | {pos_short} | {meaning_short} |\n")
        
        f.write("\n## 3. Data File Manifest\n\n")
        f.write("| Format | File Path | Description |\n")
        f.write("|:---|:---|:---|\n")
        f.write("| **JSON** | `data/exports/tangkhul_all_extracted_words.json` | Complete machine-readable catalog with metadata, examples, and sources |\n")
        f.write("| **TSV** | `data/exports/tangkhul_all_extracted_words.tsv` | Tab-delimited spreadsheet with full vocabulary details |\n")
        f.write("| **CSV** | `data/exports/tangkhul_all_extracted_words.csv` | Excel-compatible UTF-8 BOM comma-separated spreadsheet |\n")
        f.write("| **Markdown** | `data/exports/TANGKHUL_EXTRACTED_WORDS_CATALOG.md` | Executive reference report and top-100 vocabulary table |\n")

    # 5. Copy to package data directory
    pkg_data_dir = ROOT / "src" / "tangkhul_lib" / "data"
    if pkg_data_dir.exists():
        import shutil
        for fn in ["tangkhul_all_extracted_words.json", "tangkhul_all_extracted_words.tsv", "tangkhul_all_extracted_words.csv"]:
            src_f = exports_dir / fn
            dst_f = pkg_data_dir / fn
            if src_f.exists():
                shutil.copy2(src_f, dst_f)

    # 6. Populate SQLite Databases
    for db_path in [ROOT / "data" / "database" / "tangkhul_corpus.sqlite", ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"]:
        if not db_path.exists():
            continue
        print(f"Syncing vocabulary catalog into SQLite: {db_path}...")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS extracted_tangkhul_words")
        cur.execute("""
            CREATE TABLE extracted_tangkhul_words (
                rank INTEGER,
                word TEXT PRIMARY KEY,
                canonical_form TEXT,
                frequency INTEGER,
                source_count INTEGER,
                part_of_speech TEXT,
                meaning TEXT,
                example_sentence TEXT,
                sources TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ext_tk_freq ON extracted_tangkhul_words(frequency DESC)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ext_tk_rank ON extracted_tangkhul_words(rank ASC)")
        
        insert_rows = [
            (
                item["rank"],
                item["word"],
                item["canonical_form"],
                item["frequency"],
                item["source_count"],
                item["part_of_speech"],
                item["meaning"],
                item["example_sentence"],
                "; ".join(item["sources"])
            )
            for item in catalog
        ]
        cur.executemany("INSERT INTO extracted_tangkhul_words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_rows)
        conn.commit()
        conn.close()

def main():
    extractor = TangkhulLexiconExtractor()
    extractor.process_all_corpora()
    catalog = extractor.compile_catalog()
    total_tokens = sum(extractor.frequencies.values())
    export_results(catalog, total_tokens)
    print("\nSUCCESS: All Tangkhul words successfully extracted and exported!")

if __name__ == "__main__":
    main()
