"""Tangkhul-aware phonetic and fuzzy search algorithms.

Linguistic Note:
    Standard English phonetic algorithms (Soundex, Metaphone) do not accurately
    model Tibeto-Burman / Tangkhul phonology. This module implements a modular,
    configurable phonetic and similarity engine with explicit distinction between
    evidence-based transformations (documented in Tangkhul grammar and lexicography)
    and experimental dialectal rules.
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Callable
from dataclasses import dataclass, field

from tangkhul_lib.vocabulary.normalization import normalize_unicode


@dataclass(frozen=True)
class PhoneticRule:
    """Represents a discrete orthographic or phonological transformation rule."""

    id: str
    name: str
    description: str
    is_experimental: bool
    transform: Callable[[str], str]


# ---------------------------------------------------------------------------
# Evidence-Based Transformations
# (Documented in Pettigrew 1918, Arokianathan 1980/1987, TLS orthography)
# ---------------------------------------------------------------------------

def _fold_macrons(text: str) -> str:
    """Fold Tangkhul vowel macrons (indicating length) to base vowels.

    Evidence: Pettigrew (1918) and modern TLS textbooks use ā, ē, ī, ō, ū for
    vowel length, which are frequently typed as standard vowels on ASCII keyboards.
    """
    replacements = {
        "ā": "a",
        "ē": "e",
        "ī": "i",
        "ō": "o",
        "ū": "u",
        "Ā": "a",
        "Ē": "e",
        "Ī": "i",
        "Ō": "o",
        "Ū": "u",
    }
    for macron_char, base_char in replacements.items():
        text = text.replace(macron_char, base_char)
    return text


def _normalize_double_vowels(text: str) -> str:
    """Normalize repeated double vowels used orthographically for vowel length.

    Evidence: Informal and folk transcriptions often represent vowel length
    via doubling (e.g. 'laa' for 'lā', 'tashaa' for 'tashā').
    """
    for v in ("a", "e", "i", "o", "u"):
        text = re.sub(f"{v}+", v, text)
    return text


def _normalize_apostrophes_and_glottals(text: str) -> str:
    """Normalize apostrophes, glottal markers, and typographic quotes.

    Evidence: Tangkhul transcriptions use various single quote characters
    (U+0027, U+2018, U+2019, U+02BC) for glottal stops or grammatical contractions.
    """
    glottal_chars = ["'", "’", "‘", "ʻ", "ʼ", "`"]
    for gc in glottal_chars:
        text = text.replace(gc, "")
    return text


def _preserve_velar_nasal(text: str) -> str:
    """Ensure digraph 'ng' (representing phonemic velar nasal [ŋ]) is protected.

    Evidence: Tangkhul has phonemic velar nasal [ŋ] written as 'ng' in onset,
    intervocalic, and coda positions (e.g. 'ngashān', 'kaphung', 'ngalung').
    """
    return text.lower()


# ---------------------------------------------------------------------------
# Experimental Transformations
# (Documented as heuristic / village dialect variations, not universal)
# ---------------------------------------------------------------------------

def _neutralize_sibilants(text: str) -> str:
    """Map 'sh' to 's' reflecting Northern/Southern village dialect variation.

    Experimental: In certain village dialects (e.g., Huishu, Chingjaroi),
    standard Ukhrul 'sh' corresponds to alveolar sibilants 's'.
    """
    return text.replace("sh", "s")


def _simplify_aspirates(text: str) -> str:
    """Map aspirated stops (kh, th, ph) to plain stops (k, t, p).

    Experimental: Aspiration distinctions are phonemic in standard Ukhrul,
    but user queries frequently omit the 'h' in typing (e.g. 'kararchan' for 'khararchan').
    """
    text = text.replace("kh", "k")
    text = text.replace("th", "t")
    text = text.replace("ph", "p")
    return text


def _alternate_liquids(text: str) -> str:
    """Normalize liquid consonants 'r' and 'l'.

    Experimental: Liquid variation between r and l occurs across regional dialects.
    """
    return text.replace("l", "r")


def _reduce_diphthongs(text: str) -> str:
    """Normalize common vowel diphthong variants (e.g. 'ei' -> 'ai', 'ou' -> 'o').

    Experimental: Regional spelling variations frequently alternate between
    diphthong representations (e.g., 'leishat' vs 'laishat').
    """
    text = text.replace("ei", "ai")
    text = text.replace("ou", "o")
    return text


EVIDENCE_BASED_RULES: list[PhoneticRule] = [
    PhoneticRule(
        id="macron_folding",
        name="Macron & Tone Folding",
        description="Folds vowel length macrons (ā, ē, ī, ō, ū) to base ASCII vowels.",
        is_experimental=False,
        transform=_fold_macrons,
    ),
    PhoneticRule(
        id="glottal_normalization",
        name="Glottal & Apostrophe Normalization",
        description="Strips typographic and glottal apostrophes without losing stem.",
        is_experimental=False,
        transform=_normalize_apostrophes_and_glottals,
    ),
    PhoneticRule(
        id="velar_nasal",
        name="Velar Nasal Preservation",
        description="Standardizes phonemic velar nasal 'ng' representation.",
        is_experimental=False,
        transform=_preserve_velar_nasal,
    ),
    PhoneticRule(
        id="double_vowel_length",
        name="Double Vowel Length Normalization",
        description="Normalizes repeated length vowels (aa -> a, ee -> e, etc.).",
        is_experimental=False,
        transform=_normalize_double_vowels,
    ),
]

EXPERIMENTAL_RULES: list[PhoneticRule] = [
    PhoneticRule(
        id="sibilant_neutralization",
        name="Sibilant Neutralization (sh -> s)",
        description="Maps 'sh' to 's' reflecting regional village dialect shifts.",
        is_experimental=True,
        transform=_neutralize_sibilants,
    ),
    PhoneticRule(
        id="aspirate_simplification",
        name="Aspirate Simplification (kh/th/ph -> k/t/p)",
        description="Simplifies aspirated stops to match un-aspirated keyboard queries.",
        is_experimental=True,
        transform=_simplify_aspirates,
    ),
    PhoneticRule(
        id="liquid_alternation",
        name="Liquid Alternation (l -> r)",
        description="Accounts for village dialect alternations between r and l liquids.",
        is_experimental=True,
        transform=_alternate_liquids,
    ),
    PhoneticRule(
        id="diphthong_reduction",
        name="Diphthong Reduction (ei -> ai, ou -> o)",
        description="Normalizes diphthong orthographic variations across publications.",
        is_experimental=True,
        transform=_reduce_diphthongs,
    ),
]


class TangkhulPhoneticEncoder:
    """Configurable encoder generating phonetic matching keys for Tangkhul terms."""

    def __init__(
        self,
        include_experimental: bool = False,
        enabled_rule_ids: set[str] | None = None,
    ) -> None:
        self.include_experimental = include_experimental
        self._rules: list[PhoneticRule] = list(EVIDENCE_BASED_RULES)
        if include_experimental:
            self._rules.extend(EXPERIMENTAL_RULES)

        if enabled_rule_ids is not None:
            self._rules = [r for r in self._rules if r.id in enabled_rule_ids]

    @property
    def active_rules(self) -> list[PhoneticRule]:
        """Return the active transformation rules."""
        return list(self._rules)

    def encode(self, word: str) -> str:
        """Generate a phonetic search key for the input word.

        The original word is never replaced in storage; this key is used solely
        for index-matching and similarity indexing.
        """
        if not word:
            return ""

        key = normalize_unicode(word).strip().lower()
        for rule in self._rules:
            key = rule.transform(key)

        # Remove any non-alphanumeric remaining artifacts
        key = re.sub(r"[^\w]", "", key)
        return key

    def get_rules_catalog(self) -> list[dict[str, str | bool]]:
        """Return a structured description of all available rules and their status."""
        catalog: list[dict[str, str | bool]] = []
        all_rules = EVIDENCE_BASED_RULES + EXPERIMENTAL_RULES
        active_ids = {r.id for r in self._rules}
        for r in all_rules:
            catalog.append({
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "is_experimental": r.is_experimental,
                "is_active": r.id in active_ids,
            })
        return catalog


def calculate_similarity(s1: str, s2: str) -> float:
    """Calculate normalized similarity ratio (0.0 to 1.0) between two strings.

    Uses SequenceMatcher ratio on Unicode-normalized, case-folded strings.
    """
    norm1 = normalize_unicode(s1).strip().lower()
    norm2 = normalize_unicode(s2).strip().lower()

    if not norm1 and not norm2:
        return 1.0
    if not norm1 or not norm2:
        return 0.0
    if norm1 == norm2:
        return 1.0

    return difflib.SequenceMatcher(None, norm1, norm2).ratio()


@dataclass
class SearchResultMatch:
    """Encapsulates a search result with ranking and scoring explanation."""

    entry_id: str
    headword: str
    match_mode: str
    match_score: float
    matched_term: str
    explanation: str
    dialect: str | None = None
    verification_status: str = "unverified"
    source_ids: list[str] = field(default_factory=list)
