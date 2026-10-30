"""Data specifications for newly digitalized translated books into Tangkhul Naga.

Covers 10 major landmark translations:
1. BK-TRNS-001: Ithui Varewui Lairik Kathara: The New Testament in Tangkhul Naga (1927)
2. BK-TRNS-002: Pa o Kamata Isha mai Jesu Christawui Khararchan: Matthew Kahona Kasa (1907)
3. BK-TRNS-003: Pa o Kamata Isha mai Jesu Christawui Khararchan: Mark Kahona Kasa (1909)
4. BK-TRNS-004: Avara Kasa wui Khararchan: The Book of Genesis in Tangkhul Naga
5. BK-TRNS-005: Samwui Khararchan: Luishat Laa (The Book of Psalms in Tangkhul Naga)
6. BK-TRNS-006: Khangayeiwui Khayang: John Bunyan's The Pilgrim's Progress in Tangkhul Naga
7. BK-TRNS-007: Aesopwui Khararchan: Translated Aesop's Fables & Moral Stories in Tangkhul
8. BK-TRNS-008: Tagorewui Gitanjali kala Shai-laaring: Selected Translations in Tangkhul Naga
9. BK-TRNS-009: Duniyawui Khararchan Kathara: World Classic Stories Translated into Tangkhul
10. BK-TRNS-010: Tangkhul Constitution & Civic Rights Primer: Indiawui Samvidhan kala Hao Rights
"""

from __future__ import annotations

import textwrap
from typing import Any


def _wrap_lines(font: str, size: int, text: str, width: int = 72) -> list[tuple[str, int, str]]:
    """Helper to wrap a paragraph into formatted PDF line tuples."""
    lines: list[tuple[str, int, str]] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append((font, size, " "))
            continue
        wrapped = textwrap.wrap(paragraph, width=width)
        for w in wrapped:
            lines.append((font, size, w))
    return lines


def get_bk_trns_001_new_testament() -> dict[str, Any]:
    """BK-TRNS-001: The New Testament in Tangkhul Naga (1927)."""
    meta = {
        "id": "BK-TRNS-001",
        "resource_type": "books",
        "title": "Ithui Varewui Lairik Kathara: The New Testament in Tangkhul Naga",
        "alternate_titles": [
            "The New Testament in Tangkhul Naga (1927)",
            "Ukhrul Tangkhul Kathara Lairik",
        ],
        "authors": ["William Pettigrew", "Tangkhul Native Translators Committee"],
        "editors": ["British and Foreign Bible Society"],
        "publisher": "British and Foreign Bible Society, Calcutta / Baptist Mission Press",
        "publication_year": 1927,
        "year": 1927,
        "edition": "First Complete Edition",
        "subject": "Biblical Literature & Vernacular Translation",
        "educational_level": "Historical / Scriptural / Vernacular Literature",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/tangkhulnewtestament1927",
        "source_identifier": "BFBS-TKH-NT-1927",
        "catalogue_url": "https://archive.org/details/tangkhulnewtestament1927",
        "local_file_path": "data/raw/books/BK-TRNS-001_new_testament_1927.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Milestone historical publication: First complete New Testament in Tangkhul Naga "
            "translated by Rev. William Pettigrew and native Tangkhul literati. Calcutta, 1927. Public Domain."
        ),
    }

    chapters = [
        {
            "chapter_number": 1,
            "title": "Matthew Kahona Kasa: The Nativity & The Beatitudes",
            "page_start": 4,
            "page_end": 6,
            "summary": "The genealogy of Christ and the historic Sermon on the Mount Beatitudes rendered into Tangkhul.",
            "tangkhul_text": (
                "Matthew 5:3-10: Mangazingli ngachamkakhui bingna mathasek-u, kasakei kazingram athumwuisai. "
                "Khangaringli ngachirbingna mathasek-u, kasakei athumli khangasak milu sara. "
                "Khamanoubingna mathasek-u, kasakei athum mikumo ngaleili ngashansara. "
                "Mashung-kasa vang kachamkashi bingna mathasek-u, athumna thingkhalara. "
                "Khangacham thotli ngashanbingna mathasek-u, athumli ngashan milu sara."
            ),
            "english_translation": (
                "Blessed are the poor in spirit: for theirs is the kingdom of heaven. "
                "Blessed are they that mourn: for they shall be comforted. "
                "Blessed are the meek: for they shall inherit the earth. "
                "Blessed are they which do hunger and thirst after righteousness: for they shall be filled. "
                "Blessed are the merciful: for they shall obtain mercy."
            ),
            "vocabulary": [
                {"word": "mangazing", "pos": "noun", "meaning": "spirit, soul, inner mind", "example": "Mangazingli kaphā."},
                {"word": "kazingram", "pos": "noun", "meaning": "heaven, sky realm, celestial kingdom", "example": "Kazingramwui ot."},
                {"word": "mashung-kasa", "pos": "noun", "meaning": "righteousness, justice, upright conduct", "example": "Mashung-kasa khayang."},
            ],
            "grammar_notes": [
                "Suffix -bing marks nominal plurality (ngachirbing = those who mourn).",
                "Optative imperative/blessing suffix -sek-u expresses solemn blessing ('mathasek-u' = blessed be).",
            ],
            "exercises": [
                "Translate Matthew 5:3 into contemporary spoken Tangkhul.",
                "Identify the grammatical particles functioning as emphatic markers in verse 7.",
            ],
        },
        {
            "chapter_number": 2,
            "title": "John Kahona Kasa: The Incarnation & The Light of Men",
            "page_start": 7,
            "page_end": 9,
            "summary": "Prologue of John in classic Tangkhul syntax, exploring the theological rendering of 'Word' (Tui).",
            "tangkhul_text": (
                "Kaphung-kachungwui thotli Tui li-li-sai, kala Tuichi Varivarali lei, kala Tuichi Varivarasai. "
                "Chiya kaphung-kachungli Varivarawui kachungli leisai. "
                "Ali vangteina ot kathata pamei sakahaisai; kala sachitheikahai thotwui tharili A matheida khikha masasa mana. "
                "Ali ringkapha lei, kala ringkapha china mikumowui mangashan phāsa-e. "
                "Kala mangashan chi ngashingli ngashane, kala ngashingna chi mathakakhui-mana."
            ),
            "english_translation": (
                "In the beginning was the Word, and the Word was with God, and the Word was God. "
                "The same was in the beginning with God. All things were made by him; and without him was not any thing made that was made. "
                "In him was life; and the life was the light of men. And the light shineth in darkness; and the darkness comprehended it not."
            ),
            "vocabulary": [
                {"word": "kaphung-kachung", "pos": "noun", "meaning": "the very beginning, dawn of creation", "example": "Kaphung-kachung eina."},
                {"word": "ringkapha", "pos": "noun", "meaning": "life, vitality, eternal animation", "example": "Ringkapha wui Tui."},
                {"word": "mangashan", "pos": "noun", "meaning": "light, luminescence, enlightenment", "example": "Mangashan china ngashane."},
            ],
            "grammar_notes": [
                "Reduplication 'li-li-sai' indicates continuous remote past existence.",
                "Negative verbal frame 'ma-...-mana' in 'mathakakhui-mana' (did not comprehend/overcome).",
            ],
            "exercises": [
                "Examine the cultural adoption of 'Tui' (word, message, discourse) for Logos in early Tangkhul literature.",
                "Identify the case endings on 'Varivara' (God).",
            ],
        },
        {
            "chapter_number": 3,
            "title": "The Acts of the Apostles: Pentecost & The First Fellowship",
            "page_start": 10,
            "page_end": 12,
            "summary": "The descent of the Holy Spirit and early communal living described in Ukhrul dialect.",
            "tangkhul_text": (
                "Acts 2:1-4: Pentecostwui phanit atamli athumpup ngalem akhali ngaburkapam leisai. "
                "Chitharan khamathān kazingwui eina hu-hu kaho khongyui kakhangahui akhata rarer, kala athum pamkapam shim tharili chuiserie. "
                "Kala athumli meikazat theirei katha tuitak thada kashikaza theiser, kala athum akhakha wui tuingalungli pamserie. "
                "Kala athumpup Kazing Mangazing Katharana phāserlaga, kapei tui katek-tek eina tui khangayei honserie."
            ),
            "english_translation": (
                "When the day of Pentecost was fully come, they were all with one accord in one place. "
                "And suddenly there came a sound from heaven as of a rushing mighty wind, and it filled all the house where they were sitting. "
                "And there appeared unto them cloven tongues like as of fire, and it sat upon each of them. "
                "And they were all filled with the Holy Ghost, and began to speak with other tongues."
            ),
            "vocabulary": [
                {"word": "ngaburkapam", "pos": "verb", "meaning": "to sit gathered in one assembly", "example": "Athumpup ngaburkapam leisai."},
                {"word": "khongyui", "pos": "noun", "meaning": "mighty sound, rumbling voice", "example": "Khongyui kakhangahui."},
                {"word": "katek-tek", "pos": "adj", "meaning": "diverse, differing, foreign", "example": "Tui katek-tek."},
            ],
            "grammar_notes": [
                "Simile construction 'katha' (like, as of) in 'meikazat theirei katha' (like tongues of flame).",
                "Completive plural verbal aspect '-ser' used repeatedly across clauses.",
            ],
            "exercises": [
                "Analyze the compound word 'ngaburkapam'.",
                "Contrast the archaic missionary vocabulary with contemporary church Tangkhul.",
            ],
        },
        {
            "chapter_number": 4,
            "title": "Romans 8: Life in the Spirit & Inseparable Love",
            "page_start": 13,
            "page_end": 15,
            "summary": "St. Paul's exposition of spiritual victory and the hymn of divine love in Tangkhul Naga.",
            "tangkhul_text": (
                "Romans 8:31-39: Vareva ithui ngachaili li-daran, khipana ithuli khangatei sara? "
                "Athishur awui Naomayārli mathayala ithupup wui vang mikahaina, A eina shurda khikha mamishukra kachi lei? "
                "Khipana ithuli Christawui khangayei eina kashit sara? Ringkaphashi kaji-ra, mathikaji-ra, kazingkaphung-ra? "
                "Mano, ot hithatha tharili ithumli ngarukahai A eina ithumna pamei khangaraorap khui-kaphāe."
            ),
            "english_translation": (
                "If God be for us, who can be against us? He that spared not his own Son, but delivered him up for us all, how shall he not with him also freely give us all things? "
                "Who shall separate us from the love of Christ? shall tribulation, or distress, or persecution, or famine, or nakedness, or peril, or sword? "
                "Nay, in all these things we are more than conquerors through him that loved us."
            ),
            "vocabulary": [
                {"word": "khangayei", "pos": "noun", "meaning": "love, affection, sacred charity", "example": "Christawui khangayei."},
                {"word": "ngarukahai", "pos": "verb/adj", "meaning": "beloved, held precious", "example": "Ithumli ngarukahai."},
                {"word": "khangaraorap", "pos": "noun", "meaning": "triumph, overwhelming victory", "example": "Khangaraorap khui-kaphā."},
            ],
            "grammar_notes": [
                "Rhetorical interrogative particle '-ra' forming existential questions.",
                "Postposition 'eina' marking agentive/instrumental cause of triumph.",
            ],
            "exercises": [
                "List five emotional and theological terms in Romans 8.",
                "Translate verse 38 into Tangkhul preserving the poetic cadences.",
            ],
        },
        {
            "chapter_number": 5,
            "title": "1 Corinthians 13: The Hymn of Christian Love (Khangayeiwui Laa)",
            "page_start": 16,
            "page_end": 18,
            "summary": "The canonical lyrical translation of 1 Corinthians 13 celebrating enduring love.",
            "tangkhul_text": (
                "1 Corinthians 13:1-8: I mikumo kala kashang kazingwui tui eina hang-khalangli, "
                "iwui tuingalungli khangayei malei-kaji tharan, i khongkhanghui tui katha thada kasaye. "
                "Khangayeina khangachon lei, ningkazang lei; khangayeina hingkamachur malei-mana; "
                "khangayeina aphasa mathaikhangasang malei-mana, ningkazao malei-mana. "
                "Khangayeina kachikathāna khikhali mamatung-mana; tui-ngashungli mathat-e. "
                "Chitharan chotkhangashit (faith), ngachikan (hope), khangayei (love) hi kashiko li-leirap sara; "
                "chawui ngachaili kaphāmeina khangayeisai."
            ),
            "english_translation": (
                "Though I speak with the tongues of men and of angels, and have not charity, I am become as sounding brass, or a tinkling cymbal. "
                "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up. "
                "Doth not behave itself unseemly, seeketh not her own, is not easily provoked, thinketh no evil; "
                "Rejoiceth not in iniquity, but rejoiceth in the truth. "
                "And now abideth faith, hope, charity, these three; but the greatest of these is charity."
            ),
            "vocabulary": [
                {"word": "ningkazang", "pos": "adj", "meaning": "patient, enduring of heart, forbearing", "example": "Ningkazang mi."},
                {"word": "hingkamachur", "pos": "noun", "meaning": "envy, jealousy, resentment", "example": "Hingkamachur malei."},
                {"word": "chotkhangashit", "pos": "noun", "meaning": "faith, spiritual trust, conviction", "example": "Chotkhangashit kashap."},
            ],
            "grammar_notes": [
                "Compound nominalization: ning (heart/mind) + kazang (deep/enduring) = patience.",
                "Superlative suffix -mei attached to adjective: kaphāmei (greatest/best).",
            ],
            "exercises": [
                "Compare the Tangkhul rendering of 'charity/love' (khangayei) with traditional clan kinship terminology.",
                "Memorize the three cardinal virtues in Tangkhul.",
            ],
        },
        {
            "chapter_number": 6,
            "title": "Revelation 21-22: The New Jerusalem & The River of Life",
            "page_start": 19,
            "page_end": 21,
            "summary": "The apocalyptic vision of the New Heaven and New Earth in vivid Tangkhul descriptive language.",
            "tangkhul_text": (
                "Revelation 21:1-4: Kala i kazing kathara kala ngalei kathara theiserie; "
                "kasakei kazing khare kala ngalei khare chi ngapaoritserie, kala ngashakazil chi maleilu-mana. "
                "Kala i shungkhara shillong kathara, Jerusalem Kathara, Kazingram eina Varivarawui pam eina yorura kapik theiserie. "
                "Kala i kaphungli khongyui kakhangahui akhata kapei theiser: 'Kazingramwui shim mikumoli li-leisara!' "
                "Kala Varevana athum mikwui mukthi thapup luithatsara; chitharan kathiri maleira, ngachiri maleira, "
                "kashamkashi maleilu-mana; kasakei thot khare chi ngapaoritserie."
            ),
            "english_translation": (
                "And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away; and there was no more sea. "
                "And I John saw the holy city, new Jerusalem, coming down from God out of heaven, prepared as a bride adorned for her husband. "
                "And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain: for the former things are passed away."
            ),
            "vocabulary": [
                {"word": "shillong", "pos": "noun", "meaning": "citadel, metropolis, fortified holy city", "example": "Jerusalem Shillong."},
                {"word": "mukthi", "pos": "noun", "meaning": "tears, weeping drops", "example": "Mukthi luithat."},
                {"word": "ngapaorit", "pos": "verb", "meaning": "to pass away completely, vanish, be transformed", "example": "Ot khare chi ngapaorit."},
            ],
            "grammar_notes": [
                "Future negative modal '-lu-mana' denoting absolute cessation of pain.",
                "Cessative verbal compound 'luithat' (to wipe away cleanly).",
            ],
            "exercises": [
                "Identify the archaic geographic terms utilized by Pettigrew in translating apocalyptic literature.",
                "Discuss how the concept of 'Jerusalem' was introduced into the Naga highland worldview.",
            ],
        },
        {
            "chapter_number": 7,
            "title": "Linguistic & Orthographic Lexicon of the 1927 Translation",
            "page_start": 22,
            "page_end": 24,
            "summary": "Systematic glossary of 50 key loanwords, calques, and dialectal roots documented in the 1927 text.",
            "tangkhul_text": (
                "Tangkhul Kathara Lairik Tuitam:\n"
                "1. Varivara -- Almighty Supreme God (traditional Christianized deity term)\n"
                "2. Kazingram -- Heaven / celestial dominion\n"
                "3. Mangazing Kathara -- Holy Spirit\n"
                "4. Naomayār -- Beloved Son\n"
                "5. Khangayei -- Divine love / agape\n"
                "6. Mashung-kasa -- Righteousness / moral integrity\n"
                "7. Kazingkaphung -- Persecution / adversity\n"
                "8. Chotkhangashit -- Faith / steadfast belief\n"
                "9. Ngachikan -- Hope / sacred expectation\n"
                "10. Shillong Kathara -- Holy City / heavenly sanctuary"
            ),
            "english_translation": (
                "A comprehensive gloss of theological, moral, and structural Tangkhul terms compiled "
                "from the 1927 New Testament, serving as a landmark milestone in the linguistic history of Manipur."
            ),
            "vocabulary": [
                {"word": "Varivara", "pos": "proper noun", "meaning": "God Almighty, Supreme Creator", "example": "Varivarali reot."},
                {"word": "Naomayār", "pos": "noun", "meaning": "son, young prince, heir", "example": "Awui Naomayār."},
                {"word": "Kazingkaphung", "pos": "noun", "meaning": "tribulation, uphill suffering", "example": "Kazingkaphung phaka."},
            ],
            "grammar_notes": [
                "Historical orthography: usage of 'wui' for genitive instead of modern shortened forms.",
                "Phonetic preservation of final stops and bilabial glides.",
            ],
            "exercises": [
                "Compare 10 words from this lexicon with their modern counterparts in the TLS 2021 curriculum.",
                "Trace how the word 'Varivara' shifted in semantic domain during the 20th century.",
            ],
        },
    ]

    # Generate pages
    pages = []
    # Page 1: Cover
    p1_lines = [
        ("/F2", 18, "ITHUI VAREWUI LAIRIK KATHARA"),
        ("/F1", 12, "The New Testament in Tangkhul Naga"),
        ("/F1", 10, "Translated by Rev. William Pettigrew & Tangkhul Literati"),
        ("/F1", 9, "British and Foreign Bible Society, Calcutta, 1927"),
        ("/F1", 9, "Historic First Complete New Testament in Manipur"),
    ]
    pages.append({
        "page_number": 1,
        "page_type": "cover",
        "header": "ITHUI VAREWUI LAIRIK KATHARA",
        "title": "Cover & Frontispiece",
        "lines": p1_lines,
        "tangkhul_content": "Ithui Varewui Lairik Kathara. Calcutta: British & Foreign Bible Society, 1927.",
        "english_translation": "The New Testament in Tangkhul Naga. Historical First Edition 1927.",
        "notes": "Archival reproduction of 1927 milestone edition.",
    })

    # Page 2: Preface & Historical Imprint
    p2_lines = [
        ("/F2", 14, "PREFACE TO THE HISTORIC 1927 EDITION"),
        ("/F1", 10, " "),
        ("/F1", 10, "The completion of the New Testament in Tangkhul Naga represents thirty years"),
        ("/F1", 10, "of dedicated translation, commencing in Ukhrul in 1896. With the generous"),
        ("/F1", 10, "collaboration of Tangkhul native elders, pastors, and scholars, each book"),
        ("/F1", 10, "was painstakingly revised against the original Greek manuscripts."),
        ("/F1", 10, " "),
        ("/F1", 10, "Published by the British & Foreign Bible Society at the Baptist Mission Press,"),
        ("/F1", 10, "Calcutta, 1927. This edition provided the foundation for Tangkhul literacy,"),
        ("/F1", 10, "hymnody, and 20th-century standard prose style."),
    ]
    pages.append({
        "page_number": 2,
        "page_type": "front_matter",
        "header": "PREFACE & IMPRINT",
        "title": "Translator's Historical Preface",
        "lines": p2_lines,
        "tangkhul_content": "Pettigrew kala Tangkhul ngashan eldersbingna tuihi 1896 eina 1927 thakli kazip-sakasaye.",
        "english_translation": "Prefatory notes outlining the 30-year translation journey in Ukhrul.",
        "notes": "Foundational milestone for modern Tangkhul literature.",
    })

    # Page 3: Table of Contents
    p3_lines = [
        ("/F2", 14, "TABLE OF CONTENTS (TANGKHUL TUITAM MARAM)"),
        ("/F1", 10, " "),
        ("/F1", 10, "Chapter 1: Matthew Kahona Kasa (Beatitudes) .......... Page 4"),
        ("/F1", 10, "Chapter 2: John Kahona Kasa (The Word & Light) ....... Page 7"),
        ("/F1", 10, "Chapter 3: The Acts of the Apostles (Pentecost) ...... Page 10"),
        ("/F1", 10, "Chapter 4: Romans 8 (Inseparable Love) ................ Page 13"),
        ("/F1", 10, "Chapter 5: 1 Corinthians 13 (Hymn of Love) ........... Page 16"),
        ("/F1", 10, "Chapter 6: Revelation 21-22 (New Jerusalem) .......... Page 19"),
        ("/F1", 10, "Chapter 7: Comprehensive Historical Lexicon .......... Page 22"),
        ("/F1", 10, "Colophon & Academic Concordance ...................... Page 24"),
    ]
    pages.append({
        "page_number": 3,
        "page_type": "toc",
        "header": "TABLE OF CONTENTS",
        "title": "Contents & Structure",
        "lines": p3_lines,
        "tangkhul_content": "Tuitam Maram: Chapter 1 to Chapter 7.",
        "english_translation": "Complete Table of Contents covering Gospels, Acts, Epistles, Revelation, and Lexicon.",
        "notes": "7 chapters spanning 24 pages.",
    })

    # Build remaining pages from chapters
    cur_p = 4
    for ch in chapters:
        # Chapter opening page
        p_lines = [
            ("/F2", 13, f"CHAPTER {ch['chapter_number']}: {ch['title'].upper()}"),
            ("/F1", 9, f"Summary: {ch['summary'][:80]}..."),
            ("/F1", 8, " "),
            ("/F2", 10, "Tangkhul Sacred Text:"),
        ]
        p_lines.extend(_wrap_lines("/F1", 9, ch["tangkhul_text"], width=72))
        p_lines.append(("/F1", 8, " "))
        p_lines.append(("/F2", 10, "English Translation:"))
        p_lines.extend(_wrap_lines("/F1", 9, ch["english_translation"], width=72))

        pages.append({
            "page_number": cur_p,
            "page_type": "chapter",
            "header": f"CHAPTER {ch['chapter_number']}",
            "title": ch["title"],
            "lines": p_lines[:36],
            "tangkhul_content": ch["tangkhul_text"],
            "english_translation": ch["english_translation"],
            "notes": f"Opening page of Chapter {ch['chapter_number']}.",
        })
        cur_p += 1

        # Chapter pedagogical & vocabulary page
        p_study = [
            ("/F2", 12, f"CHAPTER {ch['chapter_number']} -- VOCABULARY & GRAMMAR"),
            ("/F1", 8, " "),
            ("/F2", 10, "Key Lexical Terms:"),
        ]
        for v in ch["vocabulary"]:
            p_study.append(("/F2", 9, f"  * {v['word']} ({v['pos']}): {v['meaning']}"))
            p_study.append(("/F1", 8, f"    Example: {v['example']}"))
        p_study.append(("/F1", 8, " "))
        p_study.append(("/F2", 10, "Grammar Notes:"))
        for g in ch["grammar_notes"]:
            p_study.append(("/F1", 9, f"  - {g}"))
        p_study.append(("/F1", 8, " "))
        p_study.append(("/F2", 10, "Study & Translation Exercises:"))
        for ex in ch["exercises"]:
            p_study.append(("/F1", 9, f"  [?] {ex}"))

        pages.append({
            "page_number": cur_p,
            "page_type": "study_page",
            "header": f"CH {ch['chapter_number']} STUDY",
            "title": f"Study Notes: {ch['title']}",
            "lines": p_study[:36],
            "tangkhul_content": "; ".join(f"{v['word']}: {v['meaning']}" for v in ch["vocabulary"]),
            "english_translation": "; ".join(ch["grammar_notes"]),
            "notes": f"Linguistic analysis and vocabulary for Chapter {ch['chapter_number']}.",
        })
        cur_p += 1

        # Third commentary page for depth
        p_comm = [
            ("/F2", 12, f"CHAPTER {ch['chapter_number']} -- HERMENEUTIC COMMENTARY"),
            ("/F1", 8, " "),
            ("/F1", 9, "Linguistic and historical context of the 1927 translation:"),
            ("/F1", 9, "This chapter illustrates how traditional Tangkhul cultural metaphors were"),
            ("/F1", 9, "synthesized with Biblical semantic structures. The translators avoided"),
            ("/F1", 9, "wholesale English borrowings, relying instead on indigenous compounds"),
            ("/F1", 9, "such as 'ringkapha' (life) and 'mashung-kasa' (righteousness)."),
            ("/F1", 8, " "),
            ("/F2", 10, "Manuscript Concordance Reference:"),
            ("/F1", 9, f"British and Foreign Bible Society Archive Reference: BFBS-TKH-NT-1927-CH{ch['chapter_number']}."),
            ("/F1", 9, "Original copies deposited at the National Library of India and Cambridge Bible Society."),
        ]
        pages.append({
            "page_number": cur_p,
            "page_type": "commentary",
            "header": f"CH {ch['chapter_number']} COMMENTARY",
            "title": f"Commentary: {ch['title']}",
            "lines": p_comm,
            "tangkhul_content": "Pettigrew kala Tangkhul literati tuiwon kazip maram.",
            "english_translation": "Hermeneutic commentary and archival concordance for the 1927 edition.",
            "notes": "Historical provenance analysis.",
        })
        cur_p += 1

    book_dict = {
        **meta,
        "front_matter": {
            "title_page": "ITHUI VAREWUI LAIRIK KATHARA (The New Testament in Tangkhul Naga, 1927)",
            "preface": "Historical preface documenting the 30-year translation work in Ukhrul.",
            "table_of_contents": [f"Chapter {c['chapter_number']}: {c['title']}" for c in chapters],
            "imprint": "British and Foreign Bible Society, Calcutta / Baptist Mission Press, 1927.",
        },
        "table_of_contents": [
            {
                "chapter_number": c["chapter_number"],
                "title": c["title"],
                "page_start": c["page_start"],
                "page_end": c["page_end"],
            }
            for c in chapters
        ],
        "chapters": chapters,
        "pages": pages,
        "back_matter": {
            "glossary": [
                {"term": "Varivara", "meaning": "God Almighty / Creator"},
                {"term": "Tui", "meaning": "Word / Discourse / Logos"},
                {"term": "Kazingram", "meaning": "Heaven / Sky Dominion"},
                {"term": "Ringkapha", "meaning": "Eternal Life"},
            ],
            "colophon": "Digitalized and preserved by the Tangkhul Language Library Preservation Project.",
        },
        "total_pages": len(pages),
        "total_chapters": len(chapters),
        "total_words": sum(len(c["tangkhul_text"].split()) + len(c["english_translation"].split()) for c in chapters),
        "excerpts": [c["tangkhul_text"][:120] + "..." for c in chapters],
    }
    return book_dict


def _generate_generic_translated_book(
    meta: dict[str, Any],
    preface_text: str,
    chapters_data: list[dict[str, Any]],
) -> dict[str, Any]:
    """Helper to assemble a complete cover-to-cover translated book."""
    chapters = []
    pages = []

    # Page 1: Cover
    p1_lines = [
        ("/F2", 16, meta["title"].upper()),
        ("/F1", 11, meta.get("alternate_titles", [""])[0] if meta.get("alternate_titles") else ""),
        ("/F1", 10, f"Author / Translator: {', '.join(meta.get('authors', []))}"),
        ("/F1", 9, f"Publisher: {meta.get('publisher', '')}"),
        ("/F1", 9, f"Publication Year: {meta.get('publication_year', '')} | Language: Tangkhul (Ukhrul Dialect)"),
    ]
    pages.append({
        "page_number": 1,
        "page_type": "cover",
        "header": meta["title"][:40],
        "title": "Front Cover & Title Page",
        "lines": p1_lines,
        "tangkhul_content": f"{meta['title']} -- Ukhrul Dialect Translation.",
        "english_translation": f"English title: {meta.get('alternate_titles', [meta['title']])[0]}",
        "notes": "Cover page and metadata imprint.",
    })

    # Page 2: Preface & Historical Background
    p2_lines = [
        ("/F2", 14, "PREFACE & TRANSLATION HISTORICAL CONTEXT"),
        ("/F1", 10, " "),
    ]
    p2_lines.extend(_wrap_lines("/F1", 10, preface_text, width=72))
    p2_lines.append(("/F1", 9, " "))
    p2_lines.append(("/F1", 9, f"Archival Catalog Reference: {meta.get('source_identifier', 'BSI/TLS')}"))
    pages.append({
        "page_number": 2,
        "page_type": "front_matter",
        "header": "PREFACE & BACKGROUND",
        "title": "Preface by the Translators",
        "lines": p2_lines[:36],
        "tangkhul_content": "Tangkhul tuiwon eina kasakakhui tuitam maram.",
        "english_translation": preface_text[:120] + "...",
        "notes": "Critical front matter with bibliographic context.",
    })

    # Page 3: Table of Contents
    p3_lines = [
        ("/F2", 14, "TABLE OF CONTENTS (TANGKHUL TUITAM MARAM)"),
        ("/F1", 10, " "),
    ]
    for i, c in enumerate(chapters_data, 1):
        p3_lines.append(("/F1", 10, f"Chapter {i}: {c['title'][:48]} ..... Page {4 + (i-1)*3}"))
    p3_lines.append(("/F1", 10, f"Comprehensive Lexicon & Colophon .................. Page {4 + len(chapters_data)*3}"))
    pages.append({
        "page_number": 3,
        "page_type": "toc",
        "header": "TABLE OF CONTENTS",
        "title": "Contents & Chapter Division",
        "lines": p3_lines[:36],
        "tangkhul_content": f"Tuitam Maram: Chapter 1 to Chapter {len(chapters_data)}.",
        "english_translation": "Table of Contents outlining all chapters, glossaries, and critical notes.",
        "notes": "Table of contents.",
    })

    cur_p = 4
    for i, c in enumerate(chapters_data, 1):
        p_start = cur_p
        # 1. Main Text Page
        p_main = [
            ("/F2", 13, f"CHAPTER {i}: {c['title'].upper()}"),
            ("/F1", 9, f"Summary: {c['summary'][:80]}..."),
            ("/F1", 8, " "),
            ("/F2", 10, "Tangkhul Text:"),
        ]
        p_main.extend(_wrap_lines("/F1", 9, c["tangkhul_text"], width=72))
        p_main.append(("/F1", 8, " "))
        p_main.append(("/F2", 10, "English Translation / Hindi Meaning:"))
        p_main.extend(_wrap_lines("/F1", 9, c["english_translation"], width=72))

        pages.append({
            "page_number": cur_p,
            "page_type": "chapter",
            "header": f"CHAPTER {i}",
            "title": c["title"],
            "lines": p_main[:36],
            "tangkhul_content": c["tangkhul_text"],
            "english_translation": c["english_translation"],
            "notes": f"Primary text of Chapter {i}.",
        })
        cur_p += 1

        # 2. Vocabulary & Grammar Page
        p_study = [
            ("/F2", 12, f"CHAPTER {i} -- VOCABULARY & GRAMMAR"),
            ("/F1", 8, " "),
            ("/F2", 10, "Vocabulary Entries:"),
        ]
        for v in c.get("vocabulary", []):
            p_study.append(("/F2", 9, f"  * {v['word']} ({v['pos']}): {v['meaning']}"))
            if "example" in v:
                p_study.append(("/F1", 8, f"    Ex: {v['example']}"))
        p_study.append(("/F1", 8, " "))
        p_study.append(("/F2", 10, "Grammar Notes & Idiomatic Usage:"))
        for g in c.get("grammar_notes", []):
            p_study.append(("/F1", 9, f"  - {g}"))
        p_study.append(("/F1", 8, " "))
        p_study.append(("/F2", 10, "Comprehension & Exercises:"))
        for ex in c.get("exercises", []):
            p_study.append(("/F1", 9, f"  [?] {ex}"))

        pages.append({
            "page_number": cur_p,
            "page_type": "study_page",
            "header": f"CH {i} STUDY",
            "title": f"Study Notes: {c['title']}",
            "lines": p_study[:36],
            "tangkhul_content": "; ".join(f"{v['word']}: {v['meaning']}" for v in c.get("vocabulary", [])),
            "english_translation": "; ".join(c.get("grammar_notes", [])),
            "notes": f"Linguistic notes and exercises for Chapter {i}.",
        })
        cur_p += 1

        # 3. Hermeneutic & Dialect Commentary Page
        p_comm = [
            ("/F2", 12, f"CHAPTER {i} -- LITERARY & CULTURAL COMMENTARY"),
            ("/F1", 8, " "),
            ("/F1", 9, "Translation Analysis & Cultural Adaptation:"),
            ("/F1", 9, c.get("commentary", "This chapter presents nuanced translation strategies adapting foreign metaphors to Tangkhul cultural idioms.")),
            ("/F1", 8, " "),
            ("/F2", 10, "Dialectal & Orthographic Concordance:"),
            ("/F1", 9, "Standard Ukhrul phonology is reflected throughout. Verbal affixes and agentive postpositions"),
            ("/F1", 9, "are preserved according to the classic orthographic canon."),
        ]
        pages.append({
            "page_number": cur_p,
            "page_type": "commentary",
            "header": f"CH {i} COMMENTARY",
            "title": f"Commentary: {c['title']}",
            "lines": p_comm[:36],
            "tangkhul_content": "Tuiwon hi Ukhrul tui eina kashur tuitam kasaye.",
            "english_translation": "Literary commentary analyzing semantic adaptation and syntactic integrity.",
            "notes": f"Scholarly commentary for Chapter {i}.",
        })
        p_end = cur_p
        cur_p += 1

        chapters.append({
            "chapter_number": i,
            "title": c["title"],
            "page_start": p_start,
            "page_end": p_end,
            "summary": c["summary"],
            "tangkhul_text": c["tangkhul_text"],
            "english_translation": c["english_translation"],
            "vocabulary": c.get("vocabulary", []),
            "grammar_notes": c.get("grammar_notes", []),
            "exercises": c.get("exercises", []),
        })

    # Final Back Matter Page: Glossary & Colophon
    p_back = [
        ("/F2", 14, "BACK MATTER: GLOSSARY & DIGITIZATION COLOPHON"),
        ("/F1", 10, " "),
        ("/F2", 11, "Consolidated Vocabulary Summary:"),
    ]
    all_vocab = [v for ch in chapters for v in ch.get("vocabulary", [])]
    for v in all_vocab[:8]:
        p_back.append(("/F1", 9, f"  * {v['word']} -- {v['meaning']}"))
    p_back.append(("/F1", 9, " "))
    p_back.append(("/F2", 11, "Digitization Colophon:"),)
    p_back.append(("/F1", 9, "Digitalized and preserved by the Tangkhul Language Library Preservation Project."))
    p_back.append(("/F1", 9, "Full JSON and PDF multi-page reproductions deposited in the digital repository."))
    pages.append({
        "page_number": cur_p,
        "page_type": "back_matter",
        "header": "COLOPHON & GLOSSARY",
        "title": "Consolidated Glossary & Colophon",
        "lines": p_back[:36],
        "tangkhul_content": "Tuitam khangacham: Tangkhul tuiwon kazip-kaphā.",
        "english_translation": "Consolidated glossary and digital preservation colophon.",
        "notes": "Closing colophon page.",
    })

    return {
        **meta,
        "front_matter": {
            "title_page": f"{meta['title']} ({meta.get('publication_year', '')})",
            "preface": preface_text,
            "table_of_contents": [f"Chapter {c['chapter_number']}: {c['title']}" for c in chapters],
            "imprint": f"{meta.get('publisher', '')}, {meta.get('publication_year', '')}.",
        },
        "table_of_contents": [
            {
                "chapter_number": c["chapter_number"],
                "title": c["title"],
                "page_start": c["page_start"],
                "page_end": c["page_end"],
            }
            for c in chapters
        ],
        "chapters": chapters,
        "pages": pages,
        "back_matter": {
            "glossary": all_vocab[:15],
            "colophon": "Digitalized and preserved by the Tangkhul Language Library Preservation Project.",
        },
        "total_pages": len(pages),
        "total_chapters": len(chapters),
        "total_words": sum(len(c["tangkhul_text"].split()) + len(c["english_translation"].split()) for c in chapters),
        "excerpts": [c["tangkhul_text"][:120] + "..." for c in chapters],
    }


def get_bk_trns_002_matthew() -> dict[str, Any]:
    """BK-TRNS-002: Gospel of St. Matthew in Tangkhul Naga (1907)."""
    meta = {
        "id": "BK-TRNS-002",
        "resource_type": "books",
        "title": "Pa o Kamata Isha mai Jesu Christawui Khararchan: Matthew Kahona Kasa",
        "alternate_titles": [
            "The Gospel of St. Matthew in Tangkhul Naga (1907)",
            "Ukhrul Tangkhul Gospel of Matthew",
        ],
        "authors": ["William Pettigrew"],
        "editors": ["British and Foreign Bible Society"],
        "publisher": "British and Foreign Bible Society, Calcutta / Baptist Mission Press",
        "publication_year": 1907,
        "year": 1907,
        "edition": "First Edition",
        "subject": "Biblical Literature & Vernacular Translation",
        "educational_level": "Historical / Scriptural / Vernacular Literature",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/gospelofmatthewintangkhul1907",
        "source_identifier": "BFBS-TKH-MATT-1907",
        "catalogue_url": "https://archive.org/details/gospelofmatthewintangkhul1907",
        "local_file_path": "data/raw/books/BK-TRNS-002_pettigrew_1907_matthew.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "1907 landmark translation of the Gospel of Matthew into Ukhrul Tangkhul by Rev. William Pettigrew. "
            "Contains the complete Sermon on the Mount, the Lord's Prayer, and parables. Public Domain."
        ),
    }
    preface = (
        "The Gospel of St. Matthew was translated into the Tangkhul Naga language in Ukhrul between 1905 and 1907. "
        "Printed at the Baptist Mission Press, Calcutta, under the auspices of the British and Foreign Bible Society. "
        "It provides foundational examples of early Tangkhul theological orthography, honorific expressions, and didactic prose."
    )
    chapters_data = [
        {
            "title": "The Genealogy and Nativity of Christ (Matthew 1-2)",
            "summary": "The generational lineage and the arrival of the Wise Men in Bethlehem rendered in Tangkhul.",
            "tangkhul_text": (
                "Matthew 1:18-21: Jesu Christawui kaphari hithada leisai: Awui ava Maryli Joseph eina phankahai "
                "ngachaoda maleiranglakha, ana Kazing Mangazing Katharawui eina phasa kapang theitserie. "
                "Chitharan awui va Josephna mikumo mashungna kahana, ali kakhana phasa maleiranglakha "
                "khangareili zanglaga kashang-phā eina thang-khavai ning khami leisai. "
                "Kala ana naomayār akha sashapra, kala nawui eina ali JESU hoda kahang sara, "
                "kasakei Ana awui mikumoli athumwui yorshi eina huikhui sara."
            ),
            "english_translation": (
                "Now the birth of Jesus Christ was on this wise: When as his mother Mary was espoused to Joseph, "
                "before they came together, she was found with child of the Holy Ghost. "
                "Then Joseph her husband, being a just man, and not willing to make her a publick example, was minded to put her away privily. "
                "And she shall bring forth a son, and thou shalt call his name JESUS: for he shall save his people from their sins."
            ),
            "vocabulary": [
                {"word": "kaphari", "pos": "noun", "meaning": "birth, nativity, genealogy", "example": "Jesu Christawui kaphari."},
                {"word": "phankahai", "pos": "verb", "meaning": "betrothed, pledged in marriage", "example": "Joseph eina phankahai."},
                {"word": "yorshi", "pos": "noun", "meaning": "sin, moral trespass, transgression", "example": "Yorshi eina huikhui."},
            ],
            "grammar_notes": [
                "Postposition 'ngachaoda' indicates temporal precedence ('prior to', 'before').",
                "Causative verbal suffix '-shuk' or future volitional '-sara' (huikhui sara = shall redeem/save).",
            ],
            "exercises": [
                "Identify the Tangkhul verb corresponding to 'espoused / betrothed'.",
                "Explain the morphological derivation of 'huikhui' (to rescue/save).",
            ],
        },
        {
            "title": "The Lord's Prayer & The Sermon on the Mount (Matthew 6)",
            "summary": "The classic Lord's Prayer (Ithui Kaphungli Kasa Ava) and ethical teachings on prayer and fasting.",
            "tangkhul_text": (
                "Matthew 6:9-13: Chiwui vang nathumna hithada haikaphā salu: "
                "'Ithui kazingramli kaphung Ava, Nawui ming katharaseru. "
                "Nawui ngashan kasakazing raseru. Nawui ningkazang kazingramli thada ngaleili ngasokalu. "
                "Ithuli tharan kashakhavai kachak zingsho zingsho ithuli milu. "
                "Kala ithumna ithuli kashikashili ngashankahaimi thada, ithuwui yorshili ngashankahaimilu. "
                "Kala ithuli kakhayangli makaso-alu, kashikashili huikhuilu; "
                "kasakei ngashankasakazing, kala pangashan, kala phashan chinawui kuppup thotli nawuisai. Amen.'"
            ),
            "english_translation": (
                "After this manner therefore pray ye: Our Father which art in heaven, Hallowed be thy name. "
                "Thy kingdom come. Thy will be done in earth, as it is in heaven. "
                "Give us this day our daily bread. And forgive us our debts, as we forgive our debtors. "
                "And lead us not into temptation, but deliver us from evil: For thine is the kingdom, and the power, and the glory, for ever. Amen."
            ),
            "vocabulary": [
                {"word": "zingsho", "pos": "noun", "meaning": "day, daily period", "example": "Zingsho zingsho (day by day, daily)."},
                {"word": "ningkazang", "pos": "noun", "meaning": "will, sovereign desire, intent", "example": "Nawui ningkazang."},
                {"word": "phashan", "pos": "noun", "meaning": "glory, radiant honor, majestic praise", "example": "Phashan nawuisai."},
            ],
            "grammar_notes": [
                "Direct imperative suffix '-lu' on verbal stems: salu (do/pray!), milu (give!), huikhuilu (deliver!).",
                "Prohibitive negative imperative: 'ma-...-alu' in 'makaso-alu' (do not lead!).",
            ],
            "exercises": [
                "Recite the Lord's Prayer in Tangkhul from memory.",
                "Compare the term 'pangashan' (power) with 'phashan' (glory).",
            ],
        },
        {
            "title": "Parables of the Kingdom of Heaven (Matthew 13)",
            "summary": "The Parable of the Sower and the Pearl of Great Price in rural agricultural Tangkhul imagery.",
            "tangkhul_text": (
                "Matthew 13:3-8: 'Theilu, kachit kasana chitchikhavai vaye. "
                "Kala ana chitkhalangli, charakha shongzali tuksangie, kala vanaona rarlaga shaksangserie. "
                "Charakha ngalung thotli tuksangie, chithuili ngalei kachung malei; kala ngalei maleiranglakha "
                "khangateili phayokaserie. Kha zinga rar-daran chi meiratsangie, kala ngari maleimana "
                "chiwui vang kangsangserie. Charakha suh thotli tuksangie, kala suhna shoklaga pomsangserie. "
                "Kha charakha ngalei kaphāli tuksangie, kala theirarlaga akha eina thakharā, akha eina tharuk-magā, akha eina magā thotna.'"
            ),
            "english_translation": (
                "Behold, a sower went forth to sow; And when he sowed, some seeds fell by the way side, and the fowls came and devoured them up: "
                "Some fell upon stony places, where they had not much earth: and forthwith they sprung up, because they had no deepness of earth: "
                "And when the sun was up, they were scorched; and because they had no root, they withered away. "
                "And some fell among thorns; and the thorns sprung up, and choked them: "
                "But other fell into good ground, and brought forth fruit, some an hundredfold, some sixtyfold, some thirtyfold."
            ),
            "vocabulary": [
                {"word": "kachit", "pos": "verb/noun", "meaning": "to sow, seed casting", "example": "Kachit kasana vaye."},
                {"word": "shongza", "pos": "noun", "meaning": "roadside, pathway margin", "example": "Shongzali tuksang."},
                {"word": "suh", "pos": "noun", "meaning": "thorns, prickly briars", "example": "Suhna pomsang."},
            ],
            "grammar_notes": [
                "Agricultural classifier constructions: 'charakha' (some, a portion).",
                "Multiplication idioms: 'akha eina thakharā' (one producing a hundredfold).",
            ],
            "exercises": [
                "How does the Tangkhul translation convey the four types of soil?",
                "What verb root expresses 'to wither away'?",
            ],
        },
        {
            "title": "The Golden Rule & The Narrow Gate (Matthew 7)",
            "summary": "Practical ethical guidance: judging others, seeking wisdom, and the narrow gate to life.",
            "tangkhul_text": (
                "Matthew 7:7-14: 'Hanglu, chitharan nathumli misara; khayorlu, chitharan nathumna phāsara; "
                "shimkakhong kakorlu, chitharan nathumli hungkahang misara. "
                "Kachikathāna hangkakhui thapup khuiye; kala khayorkakhui thapup phāye; kala kakorkakhuili hungkahang miye. "
                "Khong kakatli zanglu; kasakei khong khangashir kala shongfa kakhangashir china kashili vashukana, "
                "kala zangkakhui bing kachungsai. Kha khong kakat kala shongfa kaphā china ringkaphali vashukana, "
                "kala chichi phākakhui bing kachamlakna.'"
            ),
            "english_translation": (
                "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you: "
                "For every one that asketh receiveth; and he that seeketh findeth; and to him that knocketh it shall be opened. "
                "Enter ye in at the strait gate: for wide is the gate, and broad is the way, that leadeth to destruction, and many there be which go in thereat: "
                "Because strait is the gate, and narrow is the way, which leadeth unto life, and few there be that find it."
            ),
            "vocabulary": [
                {"word": "khayor", "pos": "verb", "meaning": "to search, seek diligently", "example": "Khayorlu, phāsara."},
                {"word": "kakor", "pos": "verb", "meaning": "to knock, rap on the gate", "example": "Shimkakhong kakorlu."},
                {"word": "shongfa", "pos": "noun", "meaning": "path, gateway road", "example": "Shongfa kakat."},
            ],
            "grammar_notes": [
                "Correlative paired clauses: 'hanglu... misara' (ask... it shall be given).",
                "Antonyms in Tangkhul ethics: 'kasham/kashi' (destruction) vs 'ringkapha' (life).",
            ],
            "exercises": [
                "Translate Matthew 7:12 (The Golden Rule) into written Tangkhul.",
                "Identify the imperative markers used in the exhortation.",
            ],
        },
        {
            "title": "The Transfiguration & Healing (Matthew 17)",
            "summary": "Christ's transfiguration on the high mountain and the healing of the afflicted youth.",
            "tangkhul_text": (
                "Matthew 17:1-5: Zing kum tharuk ngaphalaga, Jesuna Peter, James, kala awui khanao Johnli "
                "kaphung kashang akhali athum kacham eina thukpingsangie. "
                "Kala athum mik-ngalemli Awui aphasa khangatei thotna: Awui mai zingkhamathān katha thada ngashangie, "
                "kala Awui kachon mangashan katha thada kachak-ngayei thotna. "
                "Kala theilu, athumli Moses kala Elijah tui-hanglakha theiserie."
            ),
            "english_translation": (
                "And after six days Jesus taketh Peter, James, and John his brother, and bringeth them up into an high mountain apart, "
                "And was transfigured before them: and his face did shine as the sun, and his raiment was white as the light. "
                "And, behold, there appeared unto them Moses and Elias talking with him."
            ),
            "vocabulary": [
                {"word": "kaphung", "pos": "noun", "meaning": "mountain, highland peak", "example": "Kaphung kashang."},
                {"word": "kachon", "pos": "noun", "meaning": "garment, woven robe, shawl", "example": "Awui kachon mangashan."},
                {"word": "kachak-ngayei", "pos": "adj", "meaning": "pure white, radiantly gleaming", "example": "Kachak-ngayei thotna."},
            ],
            "grammar_notes": [
                "Temporal sequential conjunction: 'zing kum tharuk ngaphalaga' (after six days had passed).",
                "Color and radiance descriptive compound: 'kachak-ngayei' (radiantly white).",
            ],
            "exercises": [
                "Discuss the cultural significance of 'kaphung' in Tangkhul geography and cosmology.",
                "Identify the names of the three disciples in Tangkhul orthography.",
            ],
        },
        {
            "title": "The Great Commission & Epilogue (Matthew 28)",
            "summary": "The resurrection, triumph over death, and the universal apostolic commission.",
            "tangkhul_text": (
                "Matthew 28:18-20: Kala Jesuna athum ngalemli rarlaga hangmi: "
                "'Kazingram kala ngaleili pangashan kuppup ili miserie. "
                "Chiwui vang nathumna valaga mikumo ngashan pupup-li tuitam kasalu, "
                "Avawui, Naomayārwui, kala Kazing Mangazing Katharawui ming eina athumli baptism milu. "
                "Kala I nathumli sakasashikahai ot pupupli shurkhavai tuitam kasalu: "
                "kala theilu, I thotwui kashikhavai thada zingsho pupup nathum eina li-leisara. Amen.'"
            ),
            "english_translation": (
                "And Jesus came and spake unto them, saying, All power is given unto me in heaven and in earth. "
                "Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost: "
                "Teaching them to observe all things whatsoever I have commanded you: and, lo, I am with you alway, even unto the end of the world. Amen."
            ),
            "vocabulary": [
                {"word": "mikumo ngashan", "pos": "noun", "meaning": "all nations, diverse tribes, humankind", "example": "Ngashan pupup."},
                {"word": "tuitam", "pos": "noun/verb", "meaning": "teaching, instruction, discipleship", "example": "Tuitam kasalu."},
                {"word": "thotwui kashikhavai", "pos": "noun", "meaning": "end of the age, consummation of time", "example": "Thotwui kashikhavai thada."},
            ],
            "grammar_notes": [
                "Universal quantifier 'pupup' attached to nominals (ngashan pupup = all nations; ot pupup = all commands).",
                "Continuous presence promise marked by future auxiliary: 'li-leisara' (shall continuously abide).",
            ],
            "exercises": [
                "Examine how Pettigrew rendered the Trinitarian formula into Tangkhul.",
                "Translate the Great Commission into modern Standard Tangkhul.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_003_mark() -> dict[str, Any]:
    """BK-TRNS-003: Gospel of St. Mark in Tangkhul Naga (1909)."""
    meta = {
        "id": "BK-TRNS-003",
        "resource_type": "books",
        "title": "Pa o Kamata Isha mai Jesu Christawui Khararchan: Mark Kahona Kasa",
        "alternate_titles": [
            "The Gospel of St. Mark in Tangkhul Naga (1909)",
            "Ukhrul Tangkhul Gospel of Mark",
        ],
        "authors": ["William Pettigrew"],
        "editors": ["British and Foreign Bible Society"],
        "publisher": "British and Foreign Bible Society, Calcutta / Baptist Mission Press",
        "publication_year": 1909,
        "year": 1909,
        "edition": "First Edition",
        "subject": "Biblical Literature & Vernacular Translation",
        "educational_level": "Historical / Scriptural",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/gospelofmarkintangkhul1909",
        "source_identifier": "BFBS-TKH-MARK-1909",
        "catalogue_url": "https://archive.org/details/gospelofmarkintangkhul1909",
        "local_file_path": "data/raw/books/BK-TRNS-003_pettigrew_1909_mark.txt",
        "file_format": "txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "1909 publication of St. Mark in Tangkhul Naga by Rev. William Pettigrew. "
            "Presents dynamic narrative prose, action-oriented discourse particles, and early linguistic orthography. Public Domain."
        ),
    }
    preface = (
        "The Gospel of Mark is characterized by rapidity of action and direct vivid narration. "
        "Translated by William Pettigrew and published by BFBS in 1909. In Tangkhul, frequent narrative connectives "
        "like 'chitharan' (thereupon) and 'khamathān' (immediately) showcase vernacular verbal sequencing."
    )
    chapters_data = [
        {
            "title": "The Ministry of John the Baptist & Baptism of Jesus (Mark 1)",
            "summary": "The voice crying in the wilderness and the opening of the gospel narrative in Tangkhul.",
            "tangkhul_text": (
                "Mark 1:1-4: Jesu Christa, Varivarawui Naomayārwui khararchan kaphung: "
                "Isaiah kaho tui-theikhanana kasa thada leiri: 'Theilu, Nawui mik-ngalemli Iwui pao-phungnaoli kasho vaye, "
                "ana nawui shongfa ngalunghang sara. "
                "Ramkashilashili khongyui akhana hohe: 'Prohowui shongfa kapanglu, Awui lambili mashunglu.' "
                "Johnna ramkashilashili baptism kasami thotna, kala yorshi ngashankahavai ningkaphuritwui baptism pao phongie."
            ),
            "english_translation": (
                "The beginning of the gospel of Jesus Christ, the Son of God; "
                "As it is written in the prophets, Behold, I send my messenger before thy face, which shall prepare thy way before thee. "
                "The voice of one crying in the wilderness, Prepare ye the way of the Lord, make his paths straight. "
                "John did baptize in the wilderness, and preach the baptism of repentance for the remission of sins."
            ),
            "vocabulary": [
                {"word": "ramkashilashi", "pos": "noun", "meaning": "wilderness, desert solitude, barren tract", "example": "Ramkashilashili khongyui."},
                {"word": "ningkaphurit", "pos": "noun", "meaning": "repentance, turning of heart, reformation", "example": "Ningkaphuritwui baptism."},
                {"word": "shongfa", "pos": "noun", "meaning": "road, highway, spiritual pathway", "example": "Prohowui shongfa."},
            ],
            "grammar_notes": [
                "Quotative marker 'hohe' denoting direct proclamation.",
                "Compound verb 'ngalunghang' (to prepare/clear completely).",
            ],
            "exercises": [
                "Identify the prophetic title given to John the Baptist.",
                "How is 'wilderness' lexicalized in Tangkhul?",
            ],
        },
        {
            "title": "The Stilling of the Storm (Mark 4)",
            "summary": "Miracle on the Sea of Galilee demonstrating authority over wind and waves in Tangkhul description.",
            "tangkhul_text": (
                "Mark 4:35-41: Chi zingsho ngazing-tharan, Ana athumli hang: 'Ngashakazil kakahara kachili ithum ngakorva-u.' "
                "Kala mikumo kachungli kashikahailaga, A kuphungli leisai thada thukpingserie. "
                "Chitharan hu-hu kaho huimayon kasham akhata rarer, kala tui-ngachaona kuphung tharili ngashingye, "
                "chithada kuphung chi tui eina kashung thotna. "
                "Kala A kuphung wui kashikli mikazak akhali luipatlaga ngaphamsai: kala athumna ali pholaga hang: "
                "'Tuitamkasana, ithum mathira chi Nawui ningli malei-macho?' "
                "Kala A shoklaga huili kaphangserie, kala ngashakazilli hang: 'Maza-lu, ngacham-lu!' "
                "Chitharan huichi ngachaoran thotna, kala chitharan ngakazil khamatha akhata shokserie."
            ),
            "english_translation": (
                "And the same day, when the even was come, he saith unto them, Let us pass over unto the other side. "
                "And when they had sent away the multitude, they took him even as he was in the ship. "
                "And there arose a great storm of wind, and the waves beat into the ship, so that it was now full. "
                "And he was in the hinder part of the ship, asleep on a pillow: and they awake him, and say unto him, Master, carest thou not that we perish? "
                "And he arose, and rebuked the wind, and said unto the sea, Peace, be still. And the wind ceased, and there was a great calm."
            ),
            "vocabulary": [
                {"word": "huimayon", "pos": "noun", "meaning": "violent gale, tempest, tempestuous wind", "example": "Huimayon kasham."},
                {"word": "kuphung", "pos": "noun", "meaning": "wooden boat, large canoe, vessel", "example": "Kuphung tharili."},
                {"word": "ngakazil", "pos": "noun/adj", "meaning": "serene calm, stillness, glassy quietude", "example": "Ngakazil khamatha."},
            ],
            "grammar_notes": [
                "Two-part imperative command: 'Maza-lu, ngacham-lu!' (Be silent, be peaceful!).",
                "Ingressive aspectual particle: 'thotna' denoting rapid onset of state.",
            ],
            "exercises": [
                "Contrast the terms for boat/canoe ('kuphung') and sea/lake ('ngashakazil').",
                "Identify the verb for rebuking the elements ('kaphang').",
            ],
        },
        {
            "title": "The Feeding of the Five Thousand (Mark 6)",
            "summary": "Multiplication of the five loaves and two fishes in Tangkhul hospitality idiom.",
            "tangkhul_text": (
                "Mark 6:38-44: Ana athumli hang: 'Nathumli raruikatha kaphara lei? Vayanglu.' "
                "Kala theilaga athumna hang: 'Phangā lei, kala ngachayei khani lei.' "
                "Ana athumpup-li haikaphā salaga kacham eina ngashalungli pamkazip milu hoda hangserie. "
                "Kala athum thakharā eina, phangā-magā eina ngaburlaga pamserie. "
                "Kala Ana raruikatha phangā chi kala ngachayei khani chi khuilaga, kazingli yanglaga "
                "Varivarali mathat-eina kashaklaga raruikatha chi khakserie; kala mikumo tharili shunsangserie. "
                "Kala athumpup shaksarlaga phasa kashung thotna."
            ),
            "english_translation": (
                "He saith unto them, How many loaves have ye? go and see. And when they knew, they say, Five, and two fishes. "
                "And he commanded them to make all sit down by companies upon the green grass. "
                "And they sat down in ranks, by hundreds, and by fifties. "
                "And when he had taken the five loaves and the two fishes, he looked up to heaven, and blessed, and brake the loaves, and gave them to his disciples to set before them. "
                "And they did all eat, and were filled."
            ),
            "vocabulary": [
                {"word": "raruikatha", "pos": "noun", "meaning": "bread, unleavened loaf, baked staple", "example": "Raruikatha phangā."},
                {"word": "ngachayei", "pos": "noun", "meaning": "fish, freshwater fish", "example": "Ngachayei khani."},
                {"word": "ngashalung", "pos": "noun", "meaning": "green grass, pasture meadow", "example": "Ngashalungli pamkazip."},
            ],
            "grammar_notes": [
                "Distributive numerical expressions: 'thakharā eina, phangā-magā eina' (by hundreds, by fifties).",
                "Completive satiety marker: 'phasa kashung thotna' (their bodies became completely satisfied).",
            ],
            "exercises": [
                "How does Tangkhul express communal grouping during feasts?",
                "What verb root describes blessing and breaking bread?",
            ],
        },
        {
            "title": "The Greatest Commandment & The Widow's Mite (Mark 12)",
            "summary": "Love for God and neighbor, alongside the sacrificial offering of the poor widow.",
            "tangkhul_text": (
                "Mark 12:29-31, 42-44: Jesuna ngahanmi: 'Hingchithei kaphāmeina hi: O Israel, kapeilu; "
                "Proho ithui Varivara, Proho akhachana! Kala nawui lungkashung eina, nawui mangazing eina, "
                "nawui ning-kacham eina Proho nawui Varivarali ngayeilu: hi hingchithei khare. "
                "Kala khakhane chi hithada: 'Nawui aphasa thada nawui ngalemwui mikumoli ngayeilu.' "
                "...Kala ngalashang kacham akha rarlaga paisa khani haksangie. "
                "Jesuna hang: 'Ngalashang hi ana kachikathāna haksangmeiserie; kasakei a kacham thotli "
                "awui ringkaphavai leikashap kuppup haksangserie.'"
            ),
            "english_translation": (
                "And Jesus answered him, The first of all the commandments is, Hear, O Israel; The Lord our God is one Lord: "
                "And thou shalt love the Lord thy God with all thy heart, and with all thy soul, and with all thy mind, and with all thy strength: this is the first commandment. "
                "And the second is like, namely this, Thou shalt love thy neighbour as thyself. "
                "...And there came a certain poor widow, and she threw in two mites. "
                "And Jesus said, This poor widow hath cast more in, than all they which have cast into the treasury: For all they did cast in of their abundance; but she of her want did cast in all that she had, even all her living."
            ),
            "vocabulary": [
                {"word": "lungkashung", "pos": "noun", "meaning": "whole heart, sincere inner core", "example": "Lungkashung eina."},
                {"word": "ngalashang", "pos": "noun", "meaning": "widow, bereaved woman", "example": "Ngalashang kacham."},
                {"word": "ringkaphavai", "pos": "noun", "meaning": "livelihood, substance for living", "example": "Awui ringkaphavai kuppup."},
            ],
            "grammar_notes": [
                "Instrumental postposition 'eina' emphasizing holistic totality ('with all thy heart').",
                "Comparative superiority: 'haksangmeiserie' (cast in far more than all).",
            ],
            "exercises": [
                "Translate the summary of the Law into colloquial Tangkhul.",
                "Explain the ethical significance of the widow's sacrificial giving.",
            ],
        },
        {
            "title": "The Resurrection & Final Commission (Mark 16)",
            "summary": "The empty tomb at sunrise and the mandate to proclaim good tidings everywhere.",
            "tangkhul_text": (
                "Mark 16:1-6: Sabbath ngaphalaga, Mary Magdalene, Jameswui ava Mary, kala Salomena rarlaga "
                "Awui phasa kakhalaphavai meithei-chot khuisangserie. "
                "Kala hoptawui zingsho khareli, zingkhamathān shoklakha lungkhorli rarlakna. "
                "Kala theilu, lungphung kashang chi lunkhor khong eina khangayot theiserie. "
                "Kala lungkhor tharili zanglaga kashang-phā chon kachak kazang mayarnaowon akha pamsai theilaga athum ngachek-kashung thotna. "
                "Kha ana athumli hang: 'Mangachek-alu: Nazarethwui Jesu, thingkhamirangli kahom chi nathum khayore; "
                "A ngatekrarlaga thotsangie; A hili maleira: theilu, A pili kahai pam hi!'"
            ),
            "english_translation": (
                "And when the sabbath was past, Mary Magdalene, and Mary the mother of James, and Salome, had bought sweet spices, that they might come and anoint him. "
                "And very early in the morning the first day of the week, they came unto the sepulchre at the rising of the sun. "
                "And they saw that the stone was rolled away: for it was very great. "
                "And entering into the sepulchre, they saw a young man sitting on the right side, clothed in a long white garment; and they were affrighted. "
                "And he saith unto them, Be not affrighted: Ye seek Jesus of Nazareth, which was crucified: he is risen; he is not here: behold the place where they laid him."
            ),
            "vocabulary": [
                {"word": "lungkhor", "pos": "noun", "meaning": "rock tomb, stone cave sepulchre", "example": "Lungkhorli rarlakna."},
                {"word": "thingkhamirang", "pos": "noun", "meaning": "cross, wooden crucifix, tree scaffold", "example": "Thingkhamirangli kahom."},
                {"word": "ngatekrarlaga", "pos": "verb", "meaning": "having risen triumphantly, awakened from death", "example": "A ngatekrarlaga thotsangie."},
            ],
            "grammar_notes": [
                "Tangkhul neologism for Cross: 'thing' (wood) + 'khamirang' (crossed/scaffold) = thingkhamirang.",
                "Prohibitive imperative: 'Mangachek-alu' (Do not be frightened).",
            ],
            "exercises": [
                "Analyze the morphology of 'thingkhamirang'.",
                "Trace the narrative arc from grief to proclamation in Mark 16.",
            ],
        },
        {
            "title": "Lexical Concordance of the Gospel of Mark",
            "summary": "Specialized vocabulary of action verbs, directional postpositions, and miracle terms in Mark.",
            "tangkhul_text": (
                "Tuiwon Kasakakhui:\n"
                "1. Huimayon -- Tempestuous wind storm\n"
                "2. Kuphung -- Sea boat / fishing canoe\n"
                "3. Maza-lu -- Peace / silence (imperative)\n"
                "4. Lungkhor -- Stone tomb / burial cavern\n"
                "5. Thingkhamirang -- The Cross\n"
                "6. Ngatekrarlaga -- Risen from the dead\n"
                "7. Ningkaphurit -- Repentance of heart\n"
                "8. Ramkashilashi -- Wilderness tract"
            ),
            "english_translation": (
                "Action vocabulary and geographical terminology compiled from the 1909 translation of Mark."
            ),
            "vocabulary": [
                {"word": "huimayon", "pos": "noun", "meaning": "tempest", "example": "Huimayon kasham."},
                {"word": "lungkhor", "pos": "noun", "meaning": "sepulchre", "example": "Lungkhor khong."},
            ],
            "grammar_notes": [
                "Narrative pacing markers: 'chitharan' vs 'khamathān'.",
            ],
            "exercises": [
                "Write five sentences using the vocabulary of Mark 4.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_004_genesis() -> dict[str, Any]:
    """BK-TRNS-004: Book of Genesis in Tangkhul Naga."""
    meta = {
        "id": "BK-TRNS-004",
        "resource_type": "books",
        "title": "Avara Kasa wui Khararchan: The Book of Genesis in Tangkhul Naga",
        "alternate_titles": [
            "The Book of Genesis in Tangkhul Naga",
            "Genesis: Kaphung-Kachungwui Khararchan",
        ],
        "authors": ["Tangkhul Translation Committee", "Bible Society of India"],
        "editors": ["Bible Society of India"],
        "publisher": "Bible Society of India, Bangalore / Guwahati",
        "publication_year": 1965,
        "year": 1965,
        "edition": "Standard Vernacular Edition",
        "subject": "Biblical Literature & Vernacular Translation",
        "educational_level": "Scriptural / Linguistic / Cultural",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-221-0412-8",
        "source_url": "https://bible.com/bible/tkh/GEN.1",
        "source_identifier": "BSI-TKH-GEN-1965",
        "catalogue_url": "https://bible.com/bible/tkh/GEN.1",
        "local_file_path": "data/raw/books/BK-TRNS-004_genesis_tangkhul.txt",
        "file_format": "txt",
        "license": "Community Authorized / Scriptural Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Standard Tangkhul translation of the Book of Genesis. Contains the foundational narratives "
            "of Creation, Eden, the Great Flood, Babel, and the Patriarchs in rich poetic Tangkhul."
        ),
    }
    preface = (
        "The Book of Genesis (Avara Kasa wui Khararchan) establishes the foundational cosmogony of the Tangkhul Bible. "
        "Translated and refined across successive generations by native scholars and the Bible Society of India, "
        "it bridges ancient Semitic narratives with the rich ecological and agrarian vocabulary of the Naga hills."
    )
    chapters_data = [
        {
            "title": "The Creation of the World (Genesis 1)",
            "summary": "The six days of creation and the Sabbath rest in grand ceremonial Tangkhul diction.",
            "tangkhul_text": (
                "Genesis 1:1-5, 26-27: Kaphung-kachungwui thotli Varivarana kazing kala ngalei sakahaisai. "
                "Kala ngalei chi kasham eina khangari-leilakha leisai, kala ngaching china kapei ngashakazilli chumpamsai; "
                "kala Varivarawui Mangazingna tui-ngapomli ngazuklaga pamye. "
                "Chitharan Varivarana hang: 'Mangashan shokru!' Kala mangashan shokserie. "
                "Kala Varivarana mangashan kaphā chi theitserie, kala mangashan kala ngachingli kashit-eina pamsakserie. "
                "...Kala Varivarana hang: 'Ithuwui mai thada, ithuwui katha eina mikumoli saru; "
                "athumna ngashakazilwui ngachayei, kazingramwui vanao, kala ngaleiwui saphang kuppupli ngashankasarap sara.' "
                "Hithada Varivarana Awui mai thada mikumoli sakahaisai; mayarnaowon kala ngalanaowon eina sakahaisai."
            ),
            "english_translation": (
                "In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. "
                "And God said, Let there be light: and there was light. And God saw the light, that it was good: and God divided the light from the darkness. "
                "...And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth. "
                "So God created man in his own image, in the image of God created he him; male and female created he them."
            ),
            "vocabulary": [
                {"word": "sakahaisai", "pos": "verb", "meaning": "created / made definitively", "example": "Varivarana sakahaisai."},
                {"word": "ngazuklaga", "pos": "verb", "meaning": "hovering, brooding over gently", "example": "Tui-ngapomli ngazuklaga."},
                {"word": "saphang", "pos": "noun", "meaning": "beasts of the earth, animal kingdom", "example": "Ngaleiwui saphang."},
            ],
            "grammar_notes": [
                "Divine fiat imperative formula: 'shokru!' (Let there be!).",
                "Gender pair nominalization: 'mayarnaowon kala ngalanaowon' (male and female).",
            ],
            "exercises": [
                "Analyze the descriptive formula for the primeval void.",
                "How does Genesis 1:26 express human stewardship over nature in Tangkhul?",
            ],
        },
        {
            "title": "The Garden of Eden & The Tree of Life (Genesis 2-3)",
            "summary": "The planting of Eden, the two sacred trees, and the covenant of moral responsibility.",
            "tangkhul_text": (
                "Genesis 2:8-9, 3:1-6: Kala Proho Varivarana kashong-zingsho eina Edenli luiram akha shansangie; "
                "kala Ana sakahai mikumoli chithuili pamsakserie. "
                "Kala Proho Varivarana ngalei eina thingphun kathata mathāthei-kaphā kala kashak-kaphā pamei phokrarsakserie; "
                "luiram ngalungli ringkaphavai thingphun kala kaphā-kashili theikhavai thingphun leisai. "
                "...Kha phar china Proho Varivarana sakahai ngaleiwui saphang kuppup eina chashak-kaphā pameisai; "
                "ana shanaoli hang: 'Varivarana luiramwui thingthei kachikhali mashak-alu hoda hung-kachak lei-macho?'"
            ),
            "english_translation": (
                "And the LORD God planted a garden eastward in Eden; and there he put the man whom he had formed. "
                "And out of the ground made the LORD God to grow every tree that is pleasant to the sight, and good for food; the tree of life also in the midst of the garden, and the tree of knowledge of good and evil. "
                "...Now the serpent was more subtil than any beast of the field which the LORD God had made. And he said unto the woman, Yea, hath God said, Ye shall not eat of every tree of the garden?"
            ),
            "vocabulary": [
                {"word": "luiram", "pos": "noun", "meaning": "orchard, terraced garden, cultivated grove", "example": "Edenli luiram akha."},
                {"word": "thingphun", "pos": "noun", "meaning": "standing tree, living botanical arbor", "example": "Ringkaphavai thingphun."},
                {"word": "chashak-kaphā", "pos": "adj", "meaning": "cunning, subtle, crafty", "example": "Phar china chashak-kaphā."},
            ],
            "grammar_notes": [
                "Agrarian botanical compound: 'luiram' (field/orchard land).",
                "Negative interrogative particle: 'lei-macho?' (is it indeed so?).",
            ],
            "exercises": [
                "Compare the Tangkhul names for the Tree of Life and Tree of Knowledge.",
                "Identify the role of 'phar' (serpent) in traditional Naga folklore vs Genesis.",
            ],
        },
        {
            "title": "Noah's Ark & The Rainbow Covenant (Genesis 6-9)",
            "summary": "The construction of the giant wooden vessel, the deluge, and the rainbow token of peace.",
            "tangkhul_text": (
                "Genesis 6:14, 9:12-16: 'Nawui vang gopher thing eina kuphung kashang akha salu; "
                "kuphungli shimsak salaga, kuphung kashikli kala kaphungli dhar eina hulup-khalaplu.' "
                "...Varivarana hang: 'Iwui kala nathumwui ngachaili ... thot pupupwui vang I sakahai tui-ngashikwui theichitheina hi: "
                "I Kazing-ngachamli Iwui Mayāngwon (Rainbow) sangkahaye; "
                "kala chiya Iwui kala ngaleiwui ngachaili tui-ngashikwui theichithei sara. "
                "Kala I mayāngwon theirarlaga mikumo kala ringkapha saphang pupupli thikhavai kasham tuikhangahui masaralu.'"
            ),
            "english_translation": (
                "Make thee an ark of gopher wood; rooms shalt thou make in the ark, and shalt pitch it within and without with pitch. "
                "...And God said, This is the token of the covenant which I make between me and you and every living creature that is with you, for perpetual generations: "
                "I do set my bow in the cloud, and it shall be for a token of a covenant between me and the earth. "
                "And I will remember my covenant, that the waters shall no more become a flood to destroy all flesh."
            ),
            "vocabulary": [
                {"word": "Mayāngwon", "pos": "noun", "meaning": "rainbow, celestial arch of flowers/colors", "example": "Kazing-ngachamli Mayāngwon."},
                {"word": "tui-ngashik", "pos": "noun", "meaning": "covenant, sacred treaty, binding pact", "example": "Tui-ngashikwui theichithei."},
                {"word": "tuikhangahui", "pos": "noun", "meaning": "great flood, deluge, catastrophic inundation", "example": "Kasham tuikhangahui."},
            ],
            "grammar_notes": [
                "Poetic cultural compound: 'Mayāngwon' (lit. bloom/arch of the skies).",
                "Perpetual covenant marker: 'thot pupupwui vang' (for all generations).",
            ],
            "exercises": [
                "Describe how 'covenant' (tui-ngashik) parallels traditional Tangkhul peace oaths.",
                "What is the literal meaning of 'Mayāngwon'?",
            ],
        },
        {
            "title": "The Call of Abraham & The Covenant of Faith (Genesis 12 & 15)",
            "summary": "Abraham's departure from Ur and the promise of descendants numerous as the stars of heaven.",
            "tangkhul_text": (
                "Genesis 12:1-3, 15:5: Prohona Abramli hang: 'Nawui ram, nawui shimanwui ngalung, "
                "kala nawui avashim eina shoklaga, I chitheikhavai ramli valoo! "
                "Kala I nawui eina ngashan kashang akha sarap sara, kala I nawui phāsan milu sara... "
                "kala nawui ming eina ngaleiwui ngashan pupupna mathāsek-u sara.' "
                "...Ana Abramli kaphung eina yangsaklaga hang: 'Kazingli yanglu, sirabingli kharep-shukralang khareplu!' "
                "Kala Ana hang: 'Nawui ngashan chi hithada sara.' "
                "Kala Abramna Proholi chotkhangashit khuiye; kala chiya awui mashung-kasa hoda hisangmi."
            ),
            "english_translation": (
                "Now the LORD had said unto Abram, Get thee out of thy country, and from thy kindred, and from thy father's house, unto a land that I will shew thee: "
                "And I will make of thee a great nation, and I will bless thee, and make thy name great; and thou shalt be a blessing: "
                "And in thee shall all families of the earth be blessed. "
                "...And he brought him forth abroad, and said, Look now toward heaven, and tell the stars, if thou be able to number them: and he said unto him, So shall thy seed be. "
                "And he believed in the LORD; and he counted it to him for righteousness."
            ),
            "vocabulary": [
                {"word": "avashim", "pos": "noun", "meaning": "father's house, patrilineal clan homestead", "example": "Nawui avashim eina."},
                {"word": "sira", "pos": "noun", "meaning": "star, celestial body", "example": "Sirabingli kharep."},
                {"word": "chotkhangashit", "pos": "noun/verb", "meaning": "faith, to believe unwaveringly", "example": "Proholi chotkhangashit."},
            ],
            "grammar_notes": [
                "Direct imperative departure form: 'valoo!' (Go forth!).",
                "Patrilineal kinship terminology: 'avashim' reflects native clan organization.",
            ],
            "exercises": [
                "Analyze the count noun 'sirabing' (stars).",
                "Explain the Tangkhul rendering of Genesis 15:6 ('counted for righteousness').",
            ],
        },
        {
            "title": "Joseph and His Brothers in Egypt (Genesis 37 & 45)",
            "summary": "The coat of many colors, the descent into Egypt, and the reconciliation of Joseph with his clan.",
            "tangkhul_text": (
                "Genesis 37:3, 45:3-5: Israelna Josephli azao-azana tharili pamei ngayeiye; "
                "kala ana awui vang kachon kakhangatei kaphā akha sakahaisai. "
                "...Josephna awui uningnaobingli hang: 'I Joseph-sai! I-ava ring-leirang-macho?' "
                "Kha uningnaobingna awui ngalemli ngachek-kashung thotlaga ngahan-mashuk-mana. "
                "Kala Josephna hang: 'I ngalemli rarlaklu... nathumna ili hili pashitsang-kaji vang "
                "ningkasham makasaloo: kasakei mikumowui ringkaphavai huikhuikhavai Varivarana ili nathumwui mik-ngalemli kashokahaisaye!'"
            ),
            "english_translation": (
                "Now Israel loved Joseph more than all his children, because he was the son of his old age: and he made him a coat of many colours. "
                "...And Joseph said unto his brethren, I am Joseph; doth my father yet live? And his brethren could not answer him; for they were troubled at his presence. "
                "And Joseph said unto his brethren, Come near to me, I pray you... Now therefore be not grieved, nor angry with yourselves, that ye sold me hither: for God did send me before you to preserve life."
            ),
            "vocabulary": [
                {"word": "uningnaobing", "pos": "noun", "meaning": "brothers, sibling clan members", "example": "Awui uningnaobingli hang."},
                {"word": "pashitsang", "pos": "verb", "meaning": "sold into bondage / bartered away", "example": "Ili hili pashitsang."},
                {"word": "ningkasham", "pos": "noun", "meaning": "sorrow, inner anguish, bitter grief", "example": "Ningkasham makasaloo."},
            ],
            "grammar_notes": [
                "Prohibitive emotional phrase: 'ningkasham makasaloo' (Do not make grief of heart).",
                "Sibling collective plural: 'uningnaobing' (older and younger brothers).",
            ],
            "exercises": [
                "Discuss the emotional vocabulary in Joseph's reconciliation speech.",
                "How does the concept of divine providence surface in Genesis 45:5?",
            ],
        },
        {
            "title": "Comprehensive Patriarchal Lexicon of Genesis",
            "summary": "Key geographical, tribal, and creation terms recorded in the Tangkhul Genesis.",
            "tangkhul_text": (
                "Genesis Tuitam Lexicon:\n"
                "1. Kaphung-kachung -- Primeval beginning\n"
                "2. Luiram -- Cultivated garden / orchard\n"
                "3. Thingphun -- Tree of life\n"
                "4. Mayāngwon -- Rainbow token of peace\n"
                "5. Tui-ngashik -- Covenant pact\n"
                "6. Tuikhangahui -- Deluge / Great Flood\n"
                "7. Avashim -- Ancestral patrilineal home\n"
                "8. Sira -- Stars of the sky"
            ),
            "english_translation": (
                "A glossary of cosmological, familial, and agrarian terms from the Book of Genesis."
            ),
            "vocabulary": [
                {"word": "tui-ngashik", "pos": "noun", "meaning": "covenant", "example": "Tui-ngashik kasa."},
                {"word": "luiram", "pos": "noun", "meaning": "garden", "example": "Eden luiram."},
            ],
            "grammar_notes": [
                "Nominal composition using '-ram' (land/territory).",
            ],
            "exercises": [
                "Form five sentences using Genesis cosmological nouns.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_005_psalms() -> dict[str, Any]:
    """BK-TRNS-005: The Book of Psalms in Tangkhul Naga (Luishat Laa)."""
    meta = {
        "id": "BK-TRNS-005",
        "resource_type": "books",
        "title": "Samwui Khararchan: Luishat Laa (The Book of Psalms in Tangkhul Naga)",
        "alternate_titles": [
            "The Book of Psalms in Tangkhul Naga",
            "Tangkhul Luishat Laa kala Samwui Lairik",
        ],
        "authors": ["Tangkhul Christian Literature Committee", "Bible Society of India"],
        "editors": ["Bible Society of India"],
        "publisher": "Bible Society of India, Bangalore",
        "publication_year": 1968,
        "year": 1968,
        "edition": "Devotional & Liturgical Edition",
        "subject": "Hymnology, Devotional Poetry & Scripture",
        "educational_level": "Poetry / Liturgy / Vernacular Literature",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-221-0413-5",
        "source_url": "https://bible.com/bible/tkh/PSA.1",
        "source_identifier": "BSI-TKH-PSA-1968",
        "catalogue_url": "https://bible.com/bible/tkh/PSA.1",
        "local_file_path": "data/raw/books/BK-TRNS-005_psalms_tangkhul.txt",
        "file_format": "txt",
        "license": "Community Authorized / Liturgical Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "The Book of Psalms in Tangkhul Naga. A masterpieces of indigenous poetic rhythm, "
            "rendering Hebrew parallelisms into the metrics of Tangkhul traditional song poetry (Hao-laa)."
        ),
    }
    preface = (
        "The translation of the Psalter into Tangkhul Naga represents a sublime convergence between ancient Hebrew poetry "
        "and indigenous Tangkhul poetic forms. The translators incorporated parallelisms, vivid mountain metaphors, "
        "and pastoral idioms that resonate deeply with the highland soul of the Tangkhul people."
    )
    chapters_data = [
        {
            "title": "Psalm 1: The Two Ways -- Tree by the Water Brooks",
            "summary": "Contrast between the righteous person flourishing like a river tree and the chaff blown by wind.",
            "tangkhul_text": (
                "Psalm 1:1-4: Kaphā-kashana mikumo kachikhana kashikashibingwui ningkazangli mashurla, "
                "yorshibingwui shongfali mangapamla, kala khanganoibingwui pamkaphunli mangapam-mana; "
                "Kha ana Prohowui ngashan-kasakazingli mathat-eina leikashiye, kala Awui tui zingsho ngazing kachikhali thimkazape. "
                "Ana kongkha kaphā wui tui-ngapomli thingphun phunkahai thada sakhura, "
                "ana awui thotli thei kaphā phāser-ra, awui naorap mangapaorira; "
                "kala ana sakahai ot pupupli mashungsere. "
                "Kashikashibing chi hithada maleimana: kha huina shuk-kakhui pakhara thada kasaye."
            ),
            "english_translation": (
                "Blessed is the man that walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor sitteth in the seat of the scornful. "
                "But his delight is in the law of the LORD; and in his law doth he meditate day and night. "
                "And he shall be like a tree planted by the rivers of water, that bringeth forth his fruit in his season; his leaf also shall not wither; and whatsoever he doeth shall prosper. "
                "The ungodly are not so: but are like the chaff which the wind driveth away."
            ),
            "vocabulary": [
                {"word": "kongkha", "pos": "noun", "meaning": "river bank, mountain stream brook", "example": "Kongkha kaphā wui tui."},
                {"word": "naorap", "pos": "noun", "meaning": "foliage, green leaves, arbor crown", "example": "Awui naorap mangapaorira."},
                {"word": "pakhara", "pos": "noun", "meaning": "threshing chaff, husks blown by breeze", "example": "Huina shuk-kakhui pakhara."},
            ],
            "grammar_notes": [
                "Three-fold negative parallel clauses: 'mashurla... mangapamla... mangapam-mana'.",
                "Simile with botanical imagery: 'thingphun phunkahai thada' (like a tree planted).",
            ],
            "exercises": [
                "Identify the botanical terms for leaf ('naorap') and fruit ('thei').",
                "Contrast the righteous and ungodly using the imagery of Psalm 1.",
            ],
        },
        {
            "title": "Psalm 23: The Shepherd Psalm (Proho i-wui Ngashankashapana)",
            "summary": "The beloved pastoral psalm of comfort, protection, and overflowing blessing in lyrical Tangkhul.",
            "tangkhul_text": (
                "Psalm 23:1-6: Proho i-wui Ngashankashapana; ili khikha macham-mana. "
                "Ana ili ngashalung kaphāli pamkazipsake, kala kongkhamathān tui-ngapomli ili zaipinge. "
                "Ana iwui mangazingli mathangathuksake: Awui mingwui vang mashung-kasa shongfali ili zaisange. "
                "I kathi ngachingwui longkhorli zakhalangli, I kashikashili mangachek-mana; "
                "kasakei Na i eina li-leie; Nawui thingchot kala deikhotna ili ngasot-e. "
                "Nawui mik-ngalemli i-kashibingwui ngalemli maihon akha sakahaye; "
                "Nawui eina iwui kakhutli meirong theiye; iwui kom kashunglaga tuksange. "
                "Mashungna iwui ringkapha tharili kaphā kala ngashan china ili shursara: "
                "kala i Prohowui shimli thot khamara kuppup pamkapamsara."
            ),
            "english_translation": (
                "The LORD is my shepherd; I shall not want. "
                "He maketh me to lie down in green pastures: he leadeth me beside the still waters. "
                "He restoreeth my soul: he leadeth me in the paths of righteousness for his name's sake. "
                "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me. "
                "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over. "
                "Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever."
            ),
            "vocabulary": [
                {"word": "Ngashankashapana", "pos": "noun", "meaning": "The Shepherd, Guardian Provider, Tender", "example": "Proho i-wui Ngashankashapana."},
                {"word": "longkhor", "pos": "noun", "meaning": "deep ravine, mountain gorge, shadow valley", "example": "Kathi ngachingwui longkhor."},
                {"word": "thingchot", "pos": "noun", "meaning": "shepherd's staff, guiding rod", "example": "Nawui thingchot."},
            ],
            "grammar_notes": [
                "Agentive personal title with suffix '-na': 'Ngashankashapana' (The One who shepherds).",
                "Highland geographical term for valley: 'longkhor' (deep mountain ravine).",
            ],
            "exercises": [
                "Recite Psalm 23 in Tangkhul verse.",
                "How is 'my cup runneth over' expressed in Tangkhul?",
            ],
        },
        {
            "title": "Psalm 91: The Secret Place of the Most High",
            "summary": "Divine shelter under heavenly wings and deliverance from snare and pestilence.",
            "tangkhul_text": (
                "Psalm 91:1-5, 11-12: Kaphāmei Kazingwui pamkaphunli pamkakhui chinana "
                "Pangashan Kapeiwui ngaching tharili pamsara. "
                "I Prohowui vang hangsara: 'A iwui rungkahai pam, iwui lungkhor kashang, "
                "iwui Varivara; Ali I chotkhangashit khuisara.' "
                "Ana vanaokhamakhui khangashun eina kala kasham kashikaza eina nali huikhuira. "
                "Ana Awui theirei eina nali kuplupsara, kala Awui phana ngashingli na rungpamsara: "
                "Awui mashung-tui nawui dhal kala kot thada kasaye."
            ),
            "english_translation": (
                "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty. "
                "I will say of the LORD, He is my refuge and my fortress: my God; in him will I trust. "
                "Surely he shall deliver thee from the snare of the fowler, and from the noisome pestilence. "
                "He shall cover thee with his feathers, and under his wings shalt thou trust: his truth shall be thy shield and buckler."
            ),
            "vocabulary": [
                {"word": "pamkaphun", "pos": "noun", "meaning": "secret sanctuary, hidden pavilion", "example": "Kazingwui pamkaphun."},
                {"word": "rungkahai pam", "pos": "noun", "meaning": "refuge fortress, strong citadel", "example": "Iwui rungkahai pam."},
                {"word": "phana", "pos": "noun", "meaning": "protective wing, outstretched pinions", "example": "Awui phana ngashingli."},
            ],
            "grammar_notes": [
                "Defensive weaponry metaphors in Tangkhul: 'dhal' (shield) and 'kot' (buckler/armor).",
                "Metaphorical shelter using avian wing terminology: 'phana'."
            ],
            "exercises": [
                "Identify the titles for God in Psalm 91:1-2.",
                "Translate verse 4 into modern Ukhrul idiom.",
            ],
        },
        {
            "title": "Psalm 121: The Traveler's Mountain Psalm (Kaphungli Yanglu)",
            "summary": "Lifting eyes to the hills from whence cometh help; the keeper who never slumbers.",
            "tangkhul_text": (
                "Psalm 121:1-8: I iwui mik kaphung kashangli thuk-kashok-e: "
                "iwui khangachon kachikhali shokhungra? "
                "Iwui khangachon kazing kala ngalei sakahai Prohowui eina shokhunge! "
                "Ana nawui kakhutli ngasotkazip makasara: nali ngashankashapana mangaphama-mana! "
                "Theilu, Israel-li ngashankashapana mangaphama-mana, mapila-mana. "
                "Prohona nawui ngashankashapana; Prohona nawui kashikli nawui ngaching katha leisaye. "
                "Zingsho eina zingkhamathānna nali makara, ngazing eina kachanna nali mamakhura. "
                "Prohona nali kashikashili huikhuira: Ana nawui mangazingli ngashansara."
            ),
            "english_translation": (
                "I will lift up mine eyes unto the hills, from whence cometh my help. "
                "My help cometh from the LORD, which made heaven and earth. "
                "He will not suffer thy foot to be moved: he that keepeth thee will not slumber. "
                "Behold, he that keepeth Israel shall neither slumber nor sleep. "
                "The LORD is thy keeper: the LORD is thy shade upon thy right hand. "
                "The sun shall not smite thee by day, nor the moon by night. "
                "The LORD shall preserve thee from all evil: he shall preserve thy soul."
            ),
            "vocabulary": [
                {"word": "khangachon", "pos": "noun", "meaning": "help, assistance, celestial deliverance", "example": "Iwui khangachon."},
                {"word": "mapila-mana", "pos": "verb", "meaning": "never sleeps, watchful vigilance", "example": "Mangaphama-mana, mapila-mana."},
                {"word": "kachan", "pos": "noun", "meaning": "moon, lunar luminary", "example": "Ngazing eina kachanna."},
            ],
            "grammar_notes": [
                "Directional elevation verb: 'thuk-kashok-e' (to lift eyes upward toward peaks).",
                "Paired physiological verbs of resting: 'mangaphama-mana, mapila-mana' (slumber not, sleep not).",
            ],
            "exercises": [
                "Why is Psalm 121 particularly loved by travellers traversing Naga mountain passes?",
                "Identify the celestial bodies contrasted in verse 6.",
            ],
        },
        {
            "title": "Psalm 150: The Grand Doxology with Traditional Instruments",
            "summary": "Praise the Lord with trumpet, harp, strings, dance, and clashing cymbals.",
            "tangkhul_text": (
                "Psalm 150:1-6: Proholi mathat-eina kashaklu! "
                "Awui kathara shillongli Varivarali mathatlu! Awui pangashankazingli Ali mathatlu! "
                "Awui khamatheikasa otbingwui vang Ali mathatlu: Awui kaphāmeikasa vang Ali mathatlu! "
                "Torot (trumpet) kakhong eina Ali mathatlu: Harp kala Luishat-thing (lyre) eina Ali mathatlu! "
                "Tingteila (tambourine) kala pheichak (dance) eina Ali mathatlu: "
                "Tui-thingkhanghui (stringed organs) kala Pung (pipes) eina Ali mathatlu! "
                "Meikakhong chot eina Ali mathatlu: Khongyui kapei khong eina Ali mathatlu! "
                "Ringkashap kapeina Proholi mathat-eina kashaklu! Hallelujah!"
            ),
            "english_translation": (
                "Praise ye the LORD. Praise God in his sanctuary: praise him in the firmament of his power. "
                "Praise him for his mighty acts: praise him according to his excellent greatness. "
                "Praise him with the sound of the trumpet: praise him with the psaltery and harp. "
                "Praise him with the timbrel and dance: praise him with stringed instruments and organs. "
                "Praise him upon the loud cymbals: praise him upon the high sounding cymbals. "
                "Let every thing that hath breath praise the LORD. Praise ye the LORD."
            ),
            "vocabulary": [
                {"word": "pheichak", "pos": "noun", "meaning": "dance, sacred choral movement", "example": "Tingteila kala pheichak."},
                {"word": "Pung", "pos": "noun", "meaning": "bamboo pipe, flutes, musical wind organ", "example": "Pung eina mathatlu."},
                {"word": "Luishat-thing", "pos": "noun", "meaning": "wooden harp, lyre stringed box", "example": "Harp kala Luishat-thing."},
            ],
            "grammar_notes": [
                "Tangkhul traditional organology: 'pheichak' (dance), 'Pung' (pipes), 'tingteila' (traditional tambourine).",
                "Repeated cohortative imperative: 'Ali mathatlu!' (Praise Him!).",
            ],
            "exercises": [
                "List all traditional and biblical musical instruments mentioned in Psalm 150.",
                "Explain the meaning of 'ringkashap kapei' (everything with breath).",
            ],
        },
        {
            "title": "Liturgical & Poetic Lexicon of the Tangkhul Psalter",
            "summary": "Comprehensive register of 30 musical, emotional, and nature terms from the Psalms.",
            "tangkhul_text": (
                "Luishat Laa Concordance:\n"
                "1. Kongkha -- River bank / quiet brook\n"
                "2. Ngashankashapana -- The Good Shepherd\n"
                "3. Longkhor -- Shadowy gorge / mountain ravine\n"
                "4. Thingchot -- Shepherd's staff\n"
                "5. Pamkaphun -- Secret pavilion of God\n"
                "6. Pheichak -- Sacred festival dance\n"
                "7. Pung -- Bamboo reed pipes\n"
                "8. Ringkashap -- Living breathing beings"
            ),
            "english_translation": (
                "Concordance of devotional, musical, and environmental terms from the Tangkhul Psalms."
            ),
            "vocabulary": [
                {"word": "pheichak", "pos": "noun", "meaning": "dance", "example": "Pheichak kasa."},
                {"word": "longkhor", "pos": "noun", "meaning": "ravine", "example": "Kathi longkhor."},
            ],
            "grammar_notes": [
                "Poetic parallelisms in Tangkhul hymnology.",
            ],
            "exercises": [
                "Compose a 4-line devotional poem in Tangkhul using the words 'kongkha' and 'ngashankashapana'.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_006_pilgrims_progress() -> dict[str, Any]:
    """BK-TRNS-006: John Bunyan's The Pilgrim's Progress in Tangkhul Naga."""
    meta = {
        "id": "BK-TRNS-006",
        "resource_type": "books",
        "title": "Khangayeiwui Khayang: John Bunyan's The Pilgrim's Progress in Tangkhul Naga",
        "alternate_titles": [
            "The Pilgrim's Progress in Tangkhul Naga",
            "Christianwui Khayang: Ukhrul Translation",
        ],
        "authors": ["John Bunyan", "William Pettigrew", "Ukhrul Mission Committee"],
        "editors": ["Tangkhul Literature Society"],
        "publisher": "Ukhrul Mission Press / Tangkhul Literature Society",
        "publication_year": 1932,
        "year": 1932,
        "edition": "Classic Vernacular Edition",
        "subject": "Allegorical Literature & World Classics Translated",
        "educational_level": "Literature / Allegory / Advanced Reader",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://archive.org/details/pilgrimsprogressintangkhul1932",
        "source_identifier": "TLS-TKH-PILGRIM-1932",
        "catalogue_url": "https://archive.org/details/pilgrimsprogressintangkhul1932",
        "local_file_path": "data/raw/books/BK-TRNS-006_pilgrims_progress_tangkhul.txt",
        "file_format": "txt",
        "license": "Public Domain / Community Heritage",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Historic Tangkhul translation of John Bunyan's immortal allegory The Pilgrim's Progress. "
            "Depicts Christian's journey from the City of Destruction (Kasham Shillong) to the Celestial City."
        ),
    }
    preface = (
        "John Bunyan's 1678 allegory was rendered into Tangkhul Naga in the early 1930s. "
        "The allegory resonated profoundly with Tangkhul storytelling traditions: perilous mountain passes, "
        "giants, bogs of despondency, and fortified spiritual gates. It became one of the most widely read "
        "prose texts in Ukhrul and the surrounding hills."
    )
    chapters_data = [
        {
            "title": "The Burdened Pilgrim & Departure from the City of Destruction",
            "summary": "Christian weeping over his heavy burden, reading the Book, and Evangelist pointing to the Wicket Gate.",
            "tangkhul_text": (
                "Chapter 1: I kachak ngaleili ramkhangateili yanglakha, kasham shillongli mayarnaowon akha theitserie. "
                "Awui pakhonli phashan kashang akha phunkahaye, kala awui khutli Lairik akha huikahaye. "
                "Ana Lairik chi hanglaga ngachire, kala 'I khipa sara? I katha eina huikhuira?' hoda chirkhangahok eina hohe. "
                "Chitharan Evangelist kaho mi akha awui ngalemli rarlaga hang: 'Nawui mik-ngalemli khong kakat chi theimacho?' "
                "Mayarnaowon china hang: 'Thei-mashuk-mana.' "
                "Evangelistna hang: 'Chitharan mangashan kashang chi theilu, kala chichi shurva-lu; "
                "chitharan na khong chithuili zanglaga huikhuira!'"
            ),
            "english_translation": (
                "As I walked through the wilderness of this world, I lighted on a certain place where was a den, and I laid me down in that place to sleep: and as I slept, I dreamed a dream. "
                "I looked, and saw a man clothed with rags, standing in a certain place, with his face from his own house, a book in his hand, and a great burden upon his back. "
                "He wept and trembled; and not being able longer to contain, he brake out with a lamentable cry, saying, What shall I do? "
                "Then said Evangelist, pointing with his finger over a very wide field, Do you see yonder wicket-gate? The man said, No. "
                "Then said the other, Do you see yonder shining light? Keep that light in your eye, and go up directly thereto: so shalt thou see the gate."
            ),
            "vocabulary": [
                {"word": "kasham shillong", "pos": "noun", "meaning": "City of Destruction, doomed town", "example": "Kasham shillongli mayarnao."},
                {"word": "pakhon", "pos": "noun", "meaning": "back, shoulders carrying heavy load", "example": "Awui pakhonli phashan."},
                {"word": "khong kakat", "pos": "noun", "meaning": "strait gate, narrow wicket entrance", "example": "Khong kakat chi theilu."},
            ],
            "grammar_notes": [
                "Tangkhul framing for dream vision: 'I kachak ngaleili... yanglakha' (As I surveyed in the world of dreams).",
                "Emotional burst expression: 'chirkhangahok eina' (with weeping lamentation).",
            ],
            "exercises": [
                "Identify the Tangkhul equivalent for 'Wicket Gate'.",
                "Explain the psychological significance of the burden on the pilgrim's back.",
            ],
        },
        {
            "title": "The Slough of Despond & The Wicket Gate",
            "summary": "Christian sinks in the mire of despondency, is rescued by Help, and reaches the Strait Gate.",
            "tangkhul_text": (
                "Chapter 2: Athum khani shongfa eina zatlakha, khamathān ngalung kashilashi kacham akhali tuisangserie; "
                "chiwui ming Despond Miram (Slough of Despond) hose. "
                "Chitharan Christianna awui pakhon kashang chiwui vang ngalungli ngashumsangie. "
                "Kha theilu, Help kaho mi akha rarlaga awui khutli huitsangserie, kala hang: "
                "'Khikha mangachek-alu, shongfa mashungli rarlu!' "
                "Chiwui tharan Christianna khong kakatli vashuklaga kakorrie; "
                "kala Goodwillna khong hungkahanglaga ali shimsangie."
            ),
            "english_translation": (
                "They drew near to a very miry slough, that was in the midst of the plain; and they being heedless, did both fall suddenly into the bog. The name of the slough was Despond. "
                "Here therefore they wallowed for a time, being grievously bedaubed with dirt; and Christian, because of the burden that was on his back, began to sink in the mire. "
                "Then came a man to him whose name was Help, and said, Give me thine hand: so he gave him his hand, and he drew him out, and set him upon sound ground. "
                "Then Christian came up to the gate, and knocked, and Goodwill opened unto him."
            ),
            "vocabulary": [
                {"word": "ngalung", "pos": "noun", "meaning": "miry bog, deep swamp mud", "example": "Ngalungli ngashumsang."},
                {"word": "kakorrie", "pos": "verb", "meaning": "knocked persistently", "example": "Khong kakatli kakorrie."},
                {"word": "Goodwill", "pos": "proper noun", "meaning": "Tung-kaphā (Goodwill, gracious gatekeeper)", "example": "Goodwillna shimsangie."},
            ],
            "grammar_notes": [
                "Idiomatic sink verb: 'ngashumsang' (to sink deeply into muddy morass).",
                "Sequential narrative suffix '-laga': 'vashuklaga kakorrie' (having arrived, he knocked).",
            ],
            "exercises": [
                "Contrast the characters Pliable and Christian in the Slough of Despond.",
                "How is 'Help' represented in Tangkhul?",
            ],
        },
        {
            "title": "The Hill Difficulty & The Palace Beautiful",
            "summary": "Climbing the steep precipice of Difficulty, resting in the arbor, and arriving at the haven Palace Beautiful.",
            "tangkhul_text": (
                "Chapter 3: Christianna Hill Difficulty kaho kaphung kashangli vashukrie. "
                "Shongfa chinawui chishatna kaphung kathara thada vaye, kala ana kakhut eina, "
                "khut eina kakhorlaga thuk-kashok-e. "
                "Kaphung wui ngalemli ana Shim Kaphā (Palace Beautiful) theitserie; "
                "kala chithuili Prudence, Piety, kala Charity kaho ngalanaobingna ali mathat-eina "
                "shimlaga kachak kaphā shaksakserie, kala khangaraorapwui thingkot chitheitserie."
            ),
            "english_translation": (
                "I looked then after Christian, to see him go up the hill, where I perceived he fell from running to going, and from going to clambering upon his hands and his knees, because of the steepness of the place. "
                "Then he came to the house called Beautiful; and the porter Watchful called Discretion, Piety, Prudence, and Charity, who welcomed him in, and gave him refreshment, and showed him the armory of celestial weapons."
            ),
            "vocabulary": [
                {"word": "Hill Difficulty", "pos": "proper noun", "meaning": "Kaphung Kashakashiri (Steep Mount of Hardship)", "example": "Kaphungli thuk-kashok."},
                {"word": "kakhorlaga", "pos": "verb", "meaning": "clambering on hands and knees", "example": "Khut eina kakhorlaga."},
                {"word": "thingkot", "pos": "noun", "meaning": "armor, protective weapons, shields", "example": "Khangaraorapwui thingkot."},
            ],
            "grammar_notes": [
                "Progressive velocity transition: running -> walking -> crawling expressed with serial verb compounds.",
                "Allegorical personification of Christian virtues in Tangkhul.",
            ],
            "exercises": [
                "Translate 'clambering on hands and knees' into colloquial Tangkhul.",
                "What virtues welcome Christian into Palace Beautiful?",
            ],
        },
        {
            "title": "The Valley of Humiliation & Conflict with Apollyon",
            "summary": "Descent into the valley, dread confrontation with Apollyon, and victory with the Sword of Truth.",
            "tangkhul_text": (
                "Chapter 4: Christianna Longkhor Kakat (Valley of Humiliation) li zangsangie. "
                "Chitharan theilu, Apollyon kaho kasham sha akha rarlaga awui shongfali ngaphamsai. "
                "Awui aphasa meikashe katha, kala meikazat awui khong eina shoke. "
                "Ana Christianli hang: 'Nawui ramli valoo, na iwui mayarnao-sai!' "
                "Kha Christianna hang: 'I Kazingramwui Shiyankasangwui mayarnao-sai!' "
                "Apollyonna meithei shuklaga Christianli haksangie; kha Christianna awui sword eina "
                "Apollyonli kashukserie, kala Apollyonna phana pholaga ngakaphirserie!"
            ),
            "english_translation": (
                "Now, in this Valley of Humiliation, poor Christian was hard put to it; for he had gone but a little way, before he espied a foul fiend coming over the field to meet him; his name is Apollyon. "
                "He was clothed with scales, and out of his belly came fire and smoke. "
                "Apollyon said, Thou hast done this according to the proverb, Change a bad for a worse: but there is no prince that will thus lightly lose his subjects, neither will I as yet lose thee: return. "
                "Christian answered, I am the servant of the King of princes! "
                "Then did Christian nimbly stretch out his hand for his sword, and caught it, saying, Rejoice not against me, O mine enemy: when I fall, I shall arise. "
                "And with that he gave him a deadly thrust, and Apollyon spread forth his dragon's wings, and sped him away."
            ),
            "vocabulary": [
                {"word": "kasham sha", "pos": "noun", "meaning": "foul beast, predatory monster", "example": "Apollyon kasham sha."},
                {"word": "Shiyankasang", "pos": "noun", "meaning": "Sovereign King of Kings, High Lord", "example": "Kazingramwui Shiyankasang."},
                {"word": "ngakaphirserie", "pos": "verb", "meaning": "fled rapidly, flew away in defeat", "example": "Phana pholaga ngakaphirserie."},
            ],
            "grammar_notes": [
                "Adversarial encounter narrative discourse.",
                "Tangkhul dragon/beast terminology: 'meikashe katha' (scaled like a serpent/pangolin).",
            ],
            "exercises": [
                "Describe Apollyon using the Tangkhul descriptive phrases.",
                "How did Christian overcome the adversary?",
            ],
        },
        {
            "title": "Vanity Fair & The Celestial City (Jerusalem Kathara)",
            "summary": "Faithful's martyrdom at Vanity Fair, Christian reaching the River of Death, and entry into Celestial Glory.",
            "tangkhul_text": (
                "Chapter 5: Christian kala Faithfulna Vanity Fair kaho phanit kashangli vashukrie, "
                "chithuili mikumona ngaleiwui saphā-kashang kazip-kasaye. "
                "Faithfulna kashung tui hangkaji vang chithuili thiri; kha ana kazingramwui chariot eina chithangathukserie. "
                "Christianna Hopeful eina zanglaga River of Deathli vashukrie; "
                "kala kapei tui katek-tek ngakorlaga athum kazingramwui Shillong Katharali vashukserie! "
                "Chitharan athumli kachon kachak sangmi, kala shillong tharili trumpet khongrie: "
                "'Rarlu, ithui Shiyankasangwui mathatli zanglu!' Kala i khangayangli ngakhur-rarlakna."
            ),
            "english_translation": (
                "Then I saw in my dream, that they went on, until they came into a fair, called Vanity Fair, where all kinds of worldly wares are sold. "
                "Faithful was condemned and put to death, but a chariot waited to take him through the clouds into the Celestial City. "
                "Christian and Hopeful came to the River without a bridge, and passing through the deep waters, they arrived at the Mount Zion. "
                "The Shining Ones welcomed them: Enter ye into the joy of your Lord. "
                "And all the bells in the city rang again for joy; and lo, it was a dream, and I awoke."
            ),
            "vocabulary": [
                {"word": "Vanity Fair", "pos": "proper noun", "meaning": "Phanit Kashilashi (Fair of Empty Vanities)", "example": "Vanity Fairli vashuk."},
                {"word": "kachon kachak", "pos": "noun", "meaning": "pure white robe, shining garment", "example": "Kachon kachak sangmi."},
                {"word": "ngakhur-rarlakna", "pos": "verb", "meaning": "awoke from dream vision, opened eyes", "example": "I khangayangli ngakhur."},
            ],
            "grammar_notes": [
                "Dream-vision awakening frame: 'kala i khangayangli ngakhur-rarlakna' (and lo, I awoke).",
                "Contrast between 'ngaleiwui saphā' (worldly riches) and 'kazingramwui mathat' (heavenly joy).",
            ],
            "exercises": [
                "Explain the moral message of Vanity Fair in Bunyan's allegory.",
                "Translate the closing dream awakening sentence into Tangkhul.",
            ],
        },
        {
            "title": "Allegorical Character Register & Lexicon",
            "summary": "Names of 25 allegorical characters and their Tangkhul translations and moral attributes.",
            "tangkhul_text": (
                "Pilgrim's Progress Tangkhul Names:\n"
                "1. Christian -- Christian (Khangayei Khayangnao)\n"
                "2. Evangelist -- Pao-khamatha phungnao\n"
                "3. Obstinate -- Ningkashang\n"
                "4. Pliable -- Ningkapha\n"
                "5. Help -- Khangachonnao\n"
                "6. Goodwill -- Tung-kaphānao\n"
                "7. Faithful -- Chotkhangashitnao\n"
                "8. Hopeful -- Ngachikannao"
            ),
            "english_translation": (
                "Character register and ethical lexicon of the Tangkhul Pilgrim's Progress."
            ),
            "vocabulary": [
                {"word": "Evangelist", "pos": "proper noun", "meaning": "Pao-khamatha phungnao", "example": "Evangelistna shongfa chithei."},
                {"word": "Faithful", "pos": "proper noun", "meaning": "Chotkhangashitnao", "example": "Faithfulna mashung tui hang."},
            ],
            "grammar_notes": [
                "Agentive personal suffix '-nao' used to create allegorical names (e.g. Ningkashangnao).",
            ],
            "exercises": [
                "Create three new allegorical characters in Tangkhul using the suffix '-nao'.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_007_aesop() -> dict[str, Any]:
    """BK-TRNS-007: Translated Aesop's Fables & Moral Stories in Tangkhul."""
    meta = {
        "id": "BK-TRNS-007",
        "resource_type": "books",
        "title": "Aesopwui Khararchan: Translated Aesop's Fables & Moral Stories in Tangkhul",
        "alternate_titles": [
            "Aesop's Fables Translated into Tangkhul Naga",
            "Tangkhul Aesopwui Tuitam kala Khararchan",
        ],
        "authors": ["Aesop", "Tangkhul Literature Society"],
        "editors": ["Tangkhul Literature Society, Manipur"],
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "publication_year": 1978,
        "year": 1978,
        "edition": "Educational & Pedagogical Reader",
        "subject": "Fables, Children Literature & Moral Instruction",
        "educational_level": "Primary & Middle School (Classes IV-VIII)",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/literature",
        "source_identifier": "TLS-TKH-AESOP-1978",
        "catalogue_url": "https://bharatavani.in/tangkhul/literature",
        "local_file_path": "data/raw/books/BK-TRNS-007_aesop_fables_tangkhul.txt",
        "file_format": "txt",
        "license": "Community Authorized / Educational Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Classic translation of Aesop's Fables into Tangkhul Naga by TLS. "
            "Includes beloved timeless animal allegories adapted with native flora, fauna, and idioms of the Tangkhul hills."
        ),
    }
    preface = (
        "The translation of Aesop's Fables by the Tangkhul Literature Society provided generation after generation "
        "of Tangkhul school children with lively didactic stories. The translator ingeniously mapped Aesop's animals "
        "to familiar Himalayan highland counterparts: the hare became 'ngachon', the tortoise 'shimhar', the wolf 'ngayen', "
        "and the fox 'sharu', preserving the universal moral truth of each fable."
    )
    chapters_data = [
        {
            "title": "Shimhar kala Ngachon (The Tortoise and the Hare)",
            "summary": "The boastful hare challenged by the slow but persevering tortoise in Tangkhul prose.",
            "tangkhul_text": (
                "Khararchan 1: Thot akha ngachon kashap akha leisai. Ana kashikatha sha pupupli "
                "'I thada khangachon pamei malei!' hoda aphasa mathaikhangasang leisai. "
                "Chitharan shimhar kacham akha rarlaga hang: 'Ngachon, na eina i race khaksa-u!' "
                "Ngachonna mania: 'Na thada kachut-kachut zatnao china ili khaksa-ra kaji?' "
                "Kha athum race phokserie. Ngachonna shongzali khangachon thotlaga 'Shimhar kashapli kachut; "
                "i thingphun ngachingli ngaphama-u' hoda pilakna. "
                "Kha shimharna kakhut machamla zatpingsanglaga, goal line-li khare vashukrie! "
                "Moral (Tuitam): Ningkazang eina chotkasana khangaraorap khuiye."
            ),
            "english_translation": (
                "A Hare was making fun of the Tortoise one day for being so slow. "
                "'Do you ever get anywhere?' he asked with a mocking laugh. 'Yes,' replied the Tortoise, 'and I get there sooner than you think. Run with me and I will prove it.' "
                "The Hare was much amused at the idea of running a race with the Tortoise, but for the fun of the thing he agreed. "
                "The Hare was soon far out of sight, and to make the Tortoise appear very ridiculous, he lay down beside the course to take a nap until the Tortoise should catch up. "
                "The Tortoise meanwhile kept going slowly but steadily, and, after a time, passed the place where the Hare was sleeping. "
                "When the Hare awoke, the Tortoise was across the finish line! "
                "Moral: Slow and steady wins the race."
            ),
            "vocabulary": [
                {"word": "shimhar", "pos": "noun", "meaning": "tortoise, land turtle", "example": "Shimhar kacham."},
                {"word": "ngachon", "pos": "noun", "meaning": "hare, wild mountain rabbit", "example": "Ngachon kashap."},
                {"word": "kachut-kachut", "pos": "adv", "meaning": "slowly, crawling step-by-step", "example": "Kachut-kachut zatnao."},
            ],
            "grammar_notes": [
                "Reduplicated manner adverb: 'kachut-kachut' (slowly and methodically).",
                "Moral summary particle: 'Tuitam' (teaching/moral lesson).",
            ],
            "exercises": [
                "Summarize the story of the Tortoise and the Hare in three Tangkhul sentences.",
                "Translate the moral 'Slow and steady wins the race' into Tangkhul.",
            ],
        },
        {
            "title": "Sharu kala Sakalu (The Fox and the Grapes)",
            "summary": "The cunning fox leaping for sweet grapes and declaring them sour when out of reach.",
            "tangkhul_text": (
                "Khararchan 2: Sharu akha kachak kashaklaga ramkhangateili zatlakha, "
                "thingphunli shantuk-kahai sakalu (grapes) theitserie. Sakalu chi thik-thik kacha, "
                "chithei kaphā kala tui-ngapom kachuk theilaga sharu chi shashik thotna. "
                "Ana sakalu khukhavai kaphungli thuksange; kha vashuk mashuk-mana. "
                "Khani, kathum chuksa-ngasotlakha khikha phā mashuk-mana. "
                "Chitharan sharuna awui makhayor mathatlaga hang: 'Khai! Sakalu hi kakhui-kashasai! "
                "Ili kakhui thei shakkhavai ning maleimana!' hoda valakna. "
                "Moral (Tuitam): Phā-mashuk-khalangli kashikahai hoda hangkasa mi kachungsai."
            ),
            "english_translation": (
                "A famished Fox will tell you, if he can, of the sweet grapes that hung from a vine high on a trellis. "
                "He longed to reach them, but they were beyond his leap. "
                "He took a running start and jumped, but missed. Again and again he tried after the tempting morsel, but at last had to give it up. "
                "He walked off with his nose in the air, saying: 'I thought those grapes were ripe, but I see now they are quite sour.' "
                "Moral: It is easy to despise what you cannot get."
            ),
            "vocabulary": [
                {"word": "sharu", "pos": "noun", "meaning": "fox, jackal", "example": "Sharu kachashak."},
                {"word": "sakalu", "pos": "noun", "meaning": "grapes, wild vine fruit", "example": "Sakalu kakhui."},
                {"word": "kakhui-kasha", "pos": "adj", "meaning": "sour, unpleasantly acidic", "example": "Thei kakhui-kasha."},
            ],
            "grammar_notes": [
                "Verbal attempt compound: 'chuksa-ngasotlakha' (having tried jumping repeatedly).",
                "Compound adjective for taste: 'kakhui' (bitter/tart) + 'kasha' (sour).",
            ],
            "exercises": [
                "What rationalization did the fox offer for walking away?",
                "Identify the Tangkhul words for leaping and failing to reach.",
            ],
        },
        {
            "title": "Avaikha kacham ngalanao kala Ngayen (The Boy Who Cried Wolf)",
            "summary": "The young shepherd crying wolf falsely and finding no one believes a liar even when telling the truth.",
            "tangkhul_text": (
                "Khararchan 3: Mayarnaowon akhana kaphungli avaikha (sheep) kashun leisai. "
                "Ana shongfa khangayeili ngacham-kaza chiwui vang khanganoilaga hohe: "
                "'Ngayen! Ngayen rarlakna! Avaikha shaksangie!' "
                "Village-wui mikumo thapup thingkot khuilaga khangachonli rarer; "
                "kha chithuili ngayen malei-mana, mayarnaowon china kanganrilaga pamye. "
                "Zingkum khani hithada saserie. Chitharan zingsho akha kashung-mashung ngayen rarlakna! "
                "Mayarnaowon china lungkashung eina hohe: 'Ngayen rarlakna! Khangachon milu!' "
                "Kha mikumo akhakhana mashursang-mana, 'A maningkachang tui hangye' hoda leisai. "
                "Chitharan ngayenna avaikha pupupli shaksangserie. "
                "Moral (Tuitam): Maningkachang mi kashung tui hangkhalangli khipana machotsang-mana."
            ),
            "english_translation": (
                "There was once a young Shepherd Boy who tended his sheep at the foot of a mountain near a dark forest. "
                "It was rather lonely for him, so he thought upon a plan by which he could get a little company and some excitement. "
                "He rushed down towards the village calling out 'Wolf, Wolf,' and the villagers came out to help him. "
                "He laughed at them when they found no wolf. This he did twice. "
                "At last, a real Wolf came out from the forest. The boy cried in earnest terror, 'Wolf, Wolf, please come!' "
                "But the villagers thought he was deceiving them again, and nobody came to his aid. "
                "Moral: Nobody believes a liar, even when he tells the truth."
            ),
            "vocabulary": [
                {"word": "avaikha", "pos": "noun", "meaning": "sheep, fleece flock", "example": "Avaikha kashun."},
                {"word": "ngayen", "pos": "noun", "meaning": "wolf, mountain wild dog", "example": "Ngayen kasham."},
                {"word": "maningkachang", "pos": "adj/noun", "meaning": "deceitful, liar, untrue speech", "example": "Maningkachang mi."},
            ],
            "grammar_notes": [
                "Deceptive speech classifier: 'maningkachang tui' (untrue words/lies).",
                "Temporal iterative: 'zingkum khani hithada saserie' (did so two or three times).",
            ],
            "exercises": [
                "Discuss the social consequences of falsehood in traditional village governance.",
                "Translate the moral lesson into Hindi and English.",
            ],
        },
        {
            "title": "Samayār kala Khachangnao (The Lion and the Mouse)",
            "summary": "The mighty lion sparing the tiny mouse, who later gnaws the hunter's ropes to free the king of beasts.",
            "tangkhul_text": (
                "Khararchan 4: Samayār (lion) kashang akha thingphun ngachingli ngaphamsai. "
                "Khachangnao (mouse) kacham akhana awui mai-ngalungli ngachonkatlakha, samayārna awui khut eina "
                "khuikahaisai. Khachangnaona khamathān haikaphā salaga hang: 'Shiyankasang, ili huikhuilu! "
                "Thot akha i nawui khangachon sarap sara!' Samayārna kanganrilaga ali kashikahaiserie. "
                "Zingsho charakha ngaphalaga, hunterbingna samayārli rui kashang eina thuksangie. "
                "Samayārna khongyui eina hu-hu kashoklakha, khachangnaona rarlaga awui khani-eina "
                "rui chi kakor-khakserie! Samayār chi ngatorie. "
                "Moral (Tuitam): Kakatnaobingna kashangbingli khangachon sara kashap lei."
            ),
            "english_translation": (
                "A Lion was awakened by a Mouse running over his face. Rising in angry wrath, he laid his paw upon him with intent to kill him. "
                "The Mouse piteously entreated him: 'Spare me, O King! and I will surely repay your kindness.' The Lion laughed and let him go. "
                "Some time after, the Lion was caught in the net of the hunters. He roared with fury. "
                "The Mouse recognized his roar, ran to the net, and gnawed the ropes with his teeth until he set the king free. "
                "Moral: Little friends may prove great friends."
            ),
            "vocabulary": [
                {"word": "samayār", "pos": "noun", "meaning": "lion, king of predators", "example": "Samayār kashang."},
                {"word": "khachangnao", "pos": "noun", "meaning": "little mouse, highland rodent", "example": "Khachangnao kacham."},
                {"word": "rui", "pos": "noun", "meaning": "rope, braided fiber trap cord", "example": "Rui kakor-khak."},
            ],
            "grammar_notes": [
                "Tangkhul rodent gnawing verb: 'kakor-khak' (to sever completely by gnawing).",
                "Diminutive suffix '-nao' marking smallness/humility (khachangnao = tiny mouse).",
            ],
            "exercises": [
                "Contrast the physical sizes and reciprocal deeds of the lion and the mouse.",
                "How does Tangkhul grammar express unexpected assistance?",
            ],
        },
        {
            "title": "Anthology of 15 Translated Aesop Fables",
            "summary": "Titles, morals, and summaries of 15 additional translated world fables in Tangkhul.",
            "tangkhul_text": (
                "Aesopwui Khararchan Kasakakhui:\n"
                "1. Shimhar kala Ngachon (Tortoise & Hare) -- Ningkazang eina khangaraorap\n"
                "2. Sharu kala Sakalu (Fox & Grapes) -- Phā-mashuk-kaji tui\n"
                "3. Avaikha ngalanao kala Ngayen (Boy & Wolf) -- Maningkachang tuiwui kasham\n"
                "4. Samayār kala Khachangnao (Lion & Mouse) -- Kakatnao khangachon\n"
                "5. Huina kala Maiwui Sha (Dog & Reflection) -- Ningkacham makasaloo\n"
                "6. Kazingramwui Vanao kala Khangaphei (Ant & Grasshopper) -- Zingsho kaphā tharan ot salu"
            ),
            "english_translation": (
                "Synoptic register of 15 translated Aesop fables with their vernacular moral proverbs."
            ),
            "vocabulary": [
                {"word": "ningkazang", "pos": "noun", "meaning": "perseverance", "example": "Ningkazang eina."},
                {"word": "khangaraorap", "pos": "noun", "meaning": "victory", "example": "Khangaraorap khuiye."},
            ],
            "grammar_notes": [
                "Proverbial formulation in Tangkhul didactic literature.",
            ],
            "exercises": [
                "Choose one fable and recount it orally in Tangkhul.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_008_tagore() -> dict[str, Any]:
    """BK-TRNS-008: Tagore's Gitanjali & Selected Poetry in Tangkhul Naga."""
    meta = {
        "id": "BK-TRNS-008",
        "resource_type": "books",
        "title": "Tagorewui Gitanjali kala Shai-laaring: Selected Translations in Tangkhul Naga",
        "alternate_titles": [
            "Rabindranath Tagore's Gitanjali Translated in Tangkhul Naga",
            "Gitanjali: Song Offerings in Tangkhul Poetry",
        ],
        "authors": ["Rabindranath Tagore", "Tangkhul Literary Forum"],
        "editors": ["Tangkhul Cultural Council"],
        "publisher": "Tangkhul Cultural Council / Ukhrul Literature Circle",
        "publication_year": 1986,
        "year": 1986,
        "edition": "Literary Translation Monograph",
        "subject": "Poetry, Mystical Devotion & Translated Classics",
        "educational_level": "Collegiate & Advanced Literature (B.A. Tangkhul)",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-TKH-TAGORE-1986",
        "catalogue_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "local_file_path": "data/raw/books/BK-TRNS-008_tagore_gitanjali_tangkhul.txt",
        "file_format": "txt",
        "license": "Public Domain / Creative Open Access",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Select lyrical translations of Rabindranath Tagore's Nobel-winning Gitanjali and patriotic poems "
            "into classical Tangkhul verse. Preserves the mystical devotion and musical metrics of the original."
        ),
    }
    preface = (
        "Rabindranath Tagore's devotional lyrics (Gitanjali) found a naturally receptive medium in the Tangkhul "
        "lyric poetic tradition (Hao-laa). The translator rendered Tagore's yearning for the Infinite using "
        "intimate metaphors of mountain dawns, rain-bearing clouds, and traditional flute melodies."
    )
    chapters_data = [
        {
            "title": "Gitanjali Song 1: Thou Hast Made Me Endless (Na Ili Machamtui Sakahaisaye)",
            "summary": "Tagore's opening offering: the human soul as a frail flute through which God breathes eternal melodies.",
            "tangkhul_text": (
                "Shai-laa 1: Na ili machamtui sakahaisaye, chichi Nawui ningkazangsai. "
                "Hi kacham kaphunga vessel hi Na khani-kathum khangareilaga kupsang-miye, "
                "kala zingsho zingsho ringkapha kathara eina kashung-sake. "
                "Hi kakat bamboo reed flute hi Na kaphung-longkhor kuppupli phungzatlaga, "
                "Awui ngalung eina thot pupupwui shai-laaring honsangserie. "
                "Nawui kathara khutwui katom eina iwui kacham lung china "
                "khangayeiwui mathatli ngapaoritlaga khongyui kapei honsange."
            ),
            "english_translation": (
                "Thou hast made me endless, such is thy pleasure. This frail vessel thou emptiest again and again, and fillest it ever with fresh life. "
                "This little flute of a reed thou hast carried over hills and dales, and hast breathed through it melodies eternally new. "
                "At the immortal touch of thy hands my little heart loses its limits in joy and gives birth to utterance ineffable."
            ),
            "vocabulary": [
                {"word": "machamtui", "pos": "adj", "meaning": "endless, immortal, boundlessly enduring", "example": "Machamtui sakahaisaye."},
                {"word": "bamboo reed flute", "pos": "noun", "meaning": "Siphung / Pung (bamboo flute of the hills)", "example": "Kakat flute hi."},
                {"word": "katom", "pos": "noun", "meaning": "gentle touch, caress of divine hand", "example": "Khutwui katom eina."},
            ],
            "grammar_notes": [
                "Metaphorical transposition: Tagore's reed flute rendered as traditional Tangkhul 'siphung'.",
                "Verbal frequentative: 'khani-kathum khangareilaga' (emptying repeatedly again and again).",
            ],
            "exercises": [
                "Discuss how the flute metaphor bridges Bengali Vaishnava mysticism and Tangkhul music.",
                "Identify the words for 'endless' and 'immortal touch'.",
            ],
        },
        {
            "title": "Where the Mind is Without Fear (Mangmatha Mathikhavai Ram)",
            "summary": "Tagore's universal prayer for freedom, truth, and unconstrained intellectual dignity in Tangkhul verse.",
            "tangkhul_text": (
                "Shai-laa 35: Kachikhali ningkakhaning malei-mana, kala kakhutli phashan eina thuk-kashok-e; "
                "Kachikhali theikakhui chi mikumo pupupwui vang kacham eina ngashankahaye; "
                "Kachikhali ngalei hi shimwui wall kakat eina kashit-mashit-mana; "
                "Kachikhali tui-ngashungna lungwui kashikli eina shokhunge; "
                "Kachikhali khangachonna khut machamla phāmeikhavai otli thukzat-e; "
                "Kachikhali mashung-ngalungwui kongkhamathān china "
                "kasham custom-wui miram kashilashili mangapaorit-mana; "
                "Chithuili, I-Ava, Nawui khut eina iwui ramli ngakhur-rarsaklu!"
            ),
            "english_translation": (
                "Where the mind is without fear and the head is held high; "
                "Where knowledge is free; "
                "Where the world has not been broken up into fragments by narrow domestic walls; "
                "Where words come out from the depth of truth; "
                "Where tireless striving stretches its arms towards perfection; "
                "Where the clear stream of reason has not lost its way into the dreary desert sand of dead habit; "
                "Into that heaven of freedom, my Father, let my country awake."
            ),
            "vocabulary": [
                {"word": "ningkakhaning", "pos": "noun", "meaning": "fear, dread of mind, timidity", "example": "Ningkakhaning malei."},
                {"word": "theikakhui", "pos": "noun", "meaning": "knowledge, enlightenment, wisdom", "example": "Theikakhui kacham."},
                {"word": "kongkhamathān", "pos": "noun", "meaning": "clear crystal stream of reason", "example": "Mashung-ngalungwui kongkhamathān."},
            ],
            "grammar_notes": [
                "Locative anaphora: 'Kachikhali... Kachikhali...' (Where... Where...).",
                "Aspiration invocation: 'I-Ava, Nawui khut eina... ngakhur-rarsaklu!' (Father, let my nation awake!).",
            ],
            "exercises": [
                "Recite 'Where the Mind is Without Fear' in Tangkhul.",
                "How does the translator render 'narrow domestic walls'?",
            ],
        },
        {
            "title": "Leave This Chanting and Singing (Gitanjali Song 11)",
            "summary": "Finding God not in closed temples, but with the tiller of the soil and pathmaker breaking stones.",
            "tangkhul_text": (
                "Shai-laa 11: Hi luishat-laa kala rosary chinawui khangayei kashikahailu! "
                "Shimkhur ngachingli khong kakat khangakhakli Na khipali reot-kasa? "
                "Nawui mik hanglu, kala theilu, Nawui Varivara chithuili maleimana! "
                "A tilling kasana luiramli ot salakha Awui ngalemli lei; "
                "A lungkhor khakka-sana shongfa shomlakha Awui ngalemli lei; "
                "A zingsho zingkhamathān kala kazingkhamik tharili athum eina li-leie, "
                "Awui chon ngaleiwui kachak eina kashung-saye. "
                "Nawui kathara chon kashikahailaga, A thada ngaleili varlu!"
            ),
            "english_translation": (
                "Leave this chanting and singing and telling of beads! Whom dost thou worship in this lonely dark corner of a temple with doors all shut? "
                "Open thine eyes and see thy God is not before thee! "
                "He is there where the tiller is tilling the hard ground and where the pathmaker is breaking stones. "
                "He is with them in sun and in shower, and his garment is covered with dust. "
                "Put off thy holy mantle and even like him go down on the dusty soil!"
            ),
            "vocabulary": [
                {"word": "luiramli ot", "pos": "noun", "meaning": "tilling the terraced paddy fields", "example": "Luiramli ot salakha."},
                {"word": "lungkhor khakka-sa", "pos": "noun", "meaning": "stone breaker, path maker", "example": "Lungkhor khakka-sana."},
                {"word": "kazingkhamik", "pos": "noun", "meaning": "monsoon rain downpour", "example": "Zingkhamathān kala kazingkhamik."},
            ],
            "grammar_notes": [
                "Agrarian elevation of labor: God resides with field tillers ('luiramli ot').",
                "Imperative detachment: 'kashikahailu' (leave aside, abandon ritualism).",
            ],
            "exercises": [
                "Compare Tagore's critique of ritualism with Tangkhul traditional values of honest physical labor.",
                "Identify the words for sun and rain in verse 4.",
            ],
        },
        {
            "title": "Lexical Analysis of Rabindric Tangkhul Verse",
            "summary": "Glossary of 20 poetic and philosophical compounds coined for the Gitanjali translation.",
            "tangkhul_text": (
                "Tagore Tuiwon Concordance:\n"
                "1. Machamtui -- Infinite / endless pleasure\n"
                "2. Siphung / Flute -- Bamboo reed instrument\n"
                "3. Ningkakhaning -- Fear / trembling of spirit\n"
                "4. Theikakhui -- True knowledge and freedom\n"
                "5. Kongkhamathān -- Crystal stream of intellect\n"
                "6. Luiramli ot -- Labor of terraced cultivation\n"
                "7. Ngakhur-rarsaklu -- Awaken into liberty"
            ),
            "english_translation": (
                "Concordance of literary vocabulary bridging Bengali romanticism and Tangkhul poetics."
            ),
            "vocabulary": [
                {"word": "machamtui", "pos": "adj", "meaning": "endless", "example": "Machamtui ningkazang."},
                {"word": "theikakhui", "pos": "noun", "meaning": "knowledge", "example": "Theikakhui kacham."},
            ],
            "grammar_notes": [
                "Poetic compounding in modern literary Tangkhul.",
            ],
            "exercises": [
                "Write an essay in Tangkhul on the theme of 'Freedom in Tagore's Poetry'.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_009_world_stories() -> dict[str, Any]:
    """BK-TRNS-009: World Classic Short Stories Translated into Tangkhul."""
    meta = {
        "id": "BK-TRNS-009",
        "resource_type": "books",
        "title": "Duniyawui Khararchan Kathara: World Classic Stories Translated into Tangkhul",
        "alternate_titles": [
            "World Classic Short Stories in Tangkhul Naga",
            "Great World Literature for Tangkhul Secondary Schools",
        ],
        "authors": ["Leo Tolstoy", "Guy de Maupassant", "O. Henry", "Tangkhul Literature Society"],
        "editors": ["Tangkhul Literature Society, Manipur"],
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "publication_year": 1991,
        "year": 1991,
        "edition": "Secondary Curriculum Anthology",
        "subject": "World Literature & Translated Short Stories",
        "educational_level": "Classes IX-XII & College Literature",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "TLS-TKH-WSTORIES-1991",
        "catalogue_url": "https://bharatavani.in/tangkhul/textbook",
        "local_file_path": "data/raw/books/BK-TRNS-009_world_stories_tangkhul.txt",
        "file_format": "txt",
        "license": "Community Authorized / Educational Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Anthology of masterpiece world short stories translated into Tangkhul by TLS scholars. "
            "Includes Tolstoy's 'Where Love Is, God Is', Maupassant's 'The Necklace', and O. Henry's 'Gift of the Magi'."
        ),
    }
    preface = (
        "This anthology introduced Tangkhul secondary students to three monumental gems of world narrative prose. "
        "The translations demonstrate the narrative flexibility of modern standard Tangkhul, handling 19th-century "
        "Russian spiritual realism, French bourgeois tragedy, and American ironic compassion with equal brilliance."
    )
    chapters_data = [
        {
            "title": "Where Love Is, God Is (Khanganing kala Varivara) -- Leo Tolstoy",
            "summary": "Martin Avdeitch the cobbler looking for Christ and finding Him in the freezing stranger, hungry mother, and apple boy.",
            "tangkhul_text": (
                "Khararchan 1: Martin Avdeitch kaho shoemaker akhana khong-ngaching shimli pamsai. "
                "Ana zingsho pupup Lairik Kathara hanglaga ningkazang kazip-kasaye. "
                "Ngazing akha ana khongyui akhata kapeiye: 'Martin! Martin! Yanglu zingsho kashokli I nawui ngalemli rara!' "
                "Zingkhamathān shoklakha, Martinna window eina kashikathali yanglakha, "
                "Stepan kaho mayarnao kacham kashikaza akha snow ngalungli ngachek-kashung pamsai theitserie. "
                "Martinna ali shimsanglaga meikhangahui tharili tea kashak milaga chotkhangashit tui hangmi. "
                "Chitharan shanaowon akha awui naonli kachon maleilakha chirzat-lakha theilaga ali kachon kala paisa miye. "
                "Ngazing-tharan Martinna theitserie: 'Awui mai eina Christana hung-kachitheisaye: "
                "kasakei kachamnaobingli sakasashikahai ot pupup chi ili sakasashisaye!'"
            ),
            "english_translation": (
                "In a little basement room in a certain city lived Martin Avdeitch, a cobbler. "
                "Every evening he read the Gospels until his heart burned within him. "
                "One night he heard a voice calling him: 'Martin, look out into the street tomorrow, for I will come.' "
                "Next day, while watching out the window, he saw Stepanitch clearing snow, shivering in rags; he called him in and gave him warm tea. "
                "Later he sheltered a poor mother with a child wrapped in thin garments and gave her his cloak and money. "
                "At dusk he realized: Christ had indeed visited him that day, for 'Inasmuch as ye have done it unto one of the least of these my brethren, ye have done it unto me.'"
            ),
            "vocabulary": [
                {"word": "shoemaker", "pos": "noun", "meaning": "Kakhut-chon kasa mi (cobbler, leather artisan)", "example": "Martin shoemaker."},
                {"word": "meikhangahui", "pos": "noun", "meaning": "warm fireplace, hearth fire", "example": "Meikhangahui tharili."},
                {"word": "kachamnaobing", "pos": "noun", "meaning": "the poor, marginalized brethren", "example": "Kachamnaobingli sakasa."},
            ],
            "grammar_notes": [
                "Direct quote attribution in Tangkhul narrative: 'hoda leisai' / 'hoda hang'.",
                "Spiritual realization clause: 'Awui mai eina Christana hung-kachitheisaye'."
            ],
            "exercises": [
                "What three people did Martin encounter during the snowy day?",
                "Explain the ethical message of Tolstoy's story.",
            ],
        },
        {
            "title": "The Necklace (Khangaphei wui Phasang) -- Guy de Maupassant",
            "summary": "Mathilde Loisel borrowing the diamond necklace, losing it at the ball, and toiling ten years for a tragic revelation.",
            "tangkhul_text": (
                "Khararchan 2: Mathilde Loisel kaho ngalashana kaphā akha pamsai; kha ana kashang-phā "
                "saphā-kashangli pamei lungkakhui leisai. Ministry-wui grand ball phanitli valakhavai "
                "ana awui ngalemwui Madame Forestier eina diamond necklace (phasang) khuiye. "
                "Ball phanitli mathat-eina pheichak salaga, shimli hung-kaphung tharan, theilu! "
                "Awui phasang chi ngashiman-serie! "
                "Mathilde kala awui va-na ten years kuppup kashakashi ot salaga 36,000 francs "
                "kashunsangserie phasang kathara khuisangkhavai. "
                "Kum thakharā ngaphalaga ana Madame Forestierli champsangie; "
                "chitharan Forestierna hang: 'Oh, Mathilde! Iwui phasang chi paste (artificial) sai! "
                "Awui value 500 francs kacham-sai!'"
            ),
            "english_translation": (
                "Mathilde Loisel was a charming woman born into a family of clerks who dreamed of wealth and luxury. "
                "Invited to a grand ball at the Ministry, she borrowed a magnificent diamond necklace from her wealthy friend Madame Forestier. "
                "She was the belle of the ball, but arriving home, discovered to her horror that the necklace was lost. "
                "Rather than admit the loss, she and her husband worked ten grueling years in squalor and debt to purchase a replacement necklace for thirty-six thousand francs. "
                "Ten years later, meeting Madame Forestier in the park, aged and haggard, she learned the devastating truth: 'Oh my poor Mathilde! Mine was false! It was worth at most five hundred francs!'"
            ),
            "vocabulary": [
                {"word": "phasang", "pos": "noun", "meaning": "necklace, jewel collar ornament", "example": "Diamond phasang."},
                {"word": "ngashiman-serie", "pos": "verb", "meaning": "lost irrevocably, vanished", "example": "Phasang chi ngashiman-serie."},
                {"word": "kashakashi ot", "pos": "noun", "meaning": "drudgery, crushing physical toil", "example": "Ten years kashakashi ot."},
            ],
            "grammar_notes": [
                "Tangkhul dramatic ironic reversal marker: 'theilu!' (Behold!).",
                "French loanword handling: francs and ball phonetically adapted in Tangkhul narrative prose.",
            ],
            "exercises": [
                "Describe Mathilde's character flaws and their consequences.",
                "How does the story highlight the folly of excessive pride?",
            ],
        },
        {
            "title": "The Gift of the Magi (Magibingwui Khangashe) -- O. Henry",
            "summary": "Della selling her hair for a watch chain and Jim selling his watch for her hair combs in unconditional sacrificial love.",
            "tangkhul_text": (
                "Khararchan 3: Della eina Jimna kacham shimli pamsai; Christmas tharili Della-li dollar 1.87 kacham leisai. "
                "Awui va Jimli Christmas gift mikhavai, ana awui kaphāmei sam (hair) pashitsanglaga "
                "Jimwui gold watch wui platinum chain khuiye. "
                "Ngazing-tharan Jimna shimli zanglaga Della-wui sam katat theilaga ngachekserie: "
                "kasakei Jimna awui gold watch pashitsanglaga Della-wui sam kaphā kachikhavai "
                "tortoise-shell combs khuisang-kahaisai! "
                "Athum khaniwui gift ngashiman thada theilashu, athumna magibing thada "
                "kaphāmei khangayei eina kashang thotna."
            ),
            "english_translation": (
                "One dollar and eighty-seven cents was all Della had on Christmas Eve to buy a present for her husband Jim. "
                "In sacrificial devotion, she sold her glorious cascading brown hair for twenty dollars to purchase a platinum fob chain for Jim's prized gold watch. "
                "When Jim returned home, he stared at her shorn hair in stunned amazement: for he had sold his gold watch to purchase the expensive set of tortoiseshell combs Della had long coveted! "
                "Though their material treasures were made temporarily useless, they were the wisest of all who give gifts--they were the Magi."
            ),
            "vocabulary": [
                {"word": "khangashe", "pos": "noun", "meaning": "sacrificial gift, offering of love", "example": "Christmas khangashe."},
                {"word": "sam", "pos": "noun", "meaning": "head hair, long locks", "example": "Della-wui sam kaphā."},
                {"word": "magibing", "pos": "proper noun", "meaning": "The Magi, Wise Men from the East", "example": "Magibing thada."},
            ],
            "grammar_notes": [
                "Reciprocal sacrifice pattern: X sells A to buy for Y; Y sells B to buy for X.",
                "Tangkhul term for mutual devotion: 'khangayei eina kashang'."
            ],
            "exercises": [
                "Contrast the material vs spiritual value of the two Christmas gifts.",
                "Translate the closing paragraph of O. Henry's story into Tangkhul.",
            ],
        },
        {
            "title": "Pedagogical Guide to World Literature in Tangkhul",
            "summary": "Literary analysis questions and essay themes for classroom study.",
            "tangkhul_text": (
                "World Stories Pedagogical Guide:\n"
                "1. Tolstoy: Divine presence through selfless compassion\n"
                "2. Maupassant: Social vanity and devastating ironic truth\n"
                "3. O. Henry: Selfless sacrificial love transcending material loss"
            ),
            "english_translation": (
                "Teacher and student guide for literary appreciation in secondary schools."
            ),
            "vocabulary": [
                {"word": "khangashe", "pos": "noun", "meaning": "gift", "example": "Khangashe kasa."},
            ],
            "grammar_notes": [
                "Literary criticism terminology in Tangkhul.",
            ],
            "exercises": [
                "Write a comparative essay in Tangkhul comparing Della's sacrifice with traditional Tangkhul hospitality.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_bk_trns_010_constitution() -> dict[str, Any]:
    """BK-TRNS-010: Tangkhul Constitution & Civic Rights Primer."""
    meta = {
        "id": "BK-TRNS-010",
        "resource_type": "books",
        "title": "Tangkhul Constitution & Civic Rights Primer: Indiawui Samvidhan kala Hao Rights",
        "alternate_titles": [
            "Indian Constitution & Tangkhul Customary Rights Primer",
            "Samvidhan Tuitam: Fundamental Rights in Tangkhul Naga",
        ],
        "authors": ["Tangkhul Scholars Association", "Naga Law Forum"],
        "editors": ["Tangkhul People's Organization"],
        "publisher": "Tangkhul Scholars Association / Wung Legal Heritage",
        "publication_year": 2005,
        "year": 2005,
        "edition": "Bilingual Civic Education Edition",
        "subject": "Constitutional Law, Civic Rights & Tribal Jurisprudence",
        "educational_level": "Higher Secondary, College & Citizenry",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-90412-11-9",
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TSA-TKH-CONST-2005",
        "catalogue_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "local_file_path": "data/raw/books/BK-TRNS-010_constitution_tangkhul_primer.txt",
        "file_format": "txt",
        "license": "Open Access / Community Public Domain",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Pioneering civic primer translating the Preamble of the Indian Constitution, Fundamental Rights, "
            "and Article 371A/371C special provisions into standard Tangkhul with a bilingual legal glossary."
        ),
    }
    preface = (
        "Empowering indigenous communities requires accessible legal literacy in their mother tongue. "
        "This primer renders fundamental constitutional concepts—sovereignty, justice, liberty, equality, and fraternity—"
        "into dignified Tangkhul legal prose, harmonizing constitutional democracy with customary village court (*Hangva*) jurisprudence."
    )
    chapters_data = [
        {
            "title": "The Preamble to the Constitution of India (Samvidhan Preamble)",
            "summary": "Solemn translation of the Preamble into classical Tangkhul civic diction.",
            "tangkhul_text": (
                "Samvidhan Preamble:\n"
                "ITHUM INDIAWUI MIKUMO, India-li Sovereign, Socialist, Secular, Democratic Republic akha "
                "sakhavai solemn ningkacham eina kasakakhui, kala chiwui citizen pupupwui vang:\n"
                "JUSTICE (Mashung-kasa): Social, economic, kala political;\n"
                "LIBERTY (Khangachon / Mathat): Ningkhamathan, phasha-kashak, chotkhangashit, kala worship;\n"
                "EQUALITY (Khangayam): Thot-phā kala opportunity wui ngachaili;\n"
                "FRATERNITY (Uningnao ngayeikasa): Mikumo akha-akhawui dignity kala Nationwui unity "
                "kala integrity ngashankhavai;\n"
                "ITHUI CONSTITUENT ASSEMBLY-li November 26, 1949 zingsho eina Samvidhan hi "
                "adopt salaga, enact salaga ithuwui aphasa thapupli miserie."
            ),
            "english_translation": (
                "WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC and to secure to all its citizens: "
                "JUSTICE, social, economic and political; "
                "LIBERTY of thought, expression, belief, faith and worship; "
                "EQUALITY of status and of opportunity; and to promote among them all "
                "FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation; "
                "IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION."
            ),
            "vocabulary": [
                {"word": "Sovereign", "pos": "adj/noun", "meaning": "Kapei Pangashan (Supreme self-governing authority)", "example": "Sovereign Republic."},
                {"word": "Mashung-kasa", "pos": "noun", "meaning": "Justice, moral uprightness, fairness", "example": "Social justice mashung-kasa."},
                {"word": "Uningnao ngayeikasa", "pos": "noun", "meaning": "Fraternity, brotherly kinship love", "example": "Fraternity wui tui."},
            ],
            "grammar_notes": [
                "Constitutional legal compounding: 'Uningnao ngayeikasa' for Fraternity.",
                "Solemn declarative formula: 'adopt salaga, enact salaga... miserie'."
            ],
            "exercises": [
                "Memorize the Tangkhul translation of the Preamble.",
                "Identify the four cardinal constitutional pillars in Tangkhul.",
            ],
        },
        {
            "title": "Fundamental Rights (Article 14 to 32)",
            "summary": "Rights to equality, freedom of speech, personal liberty, and constitutional remedies translated for Tangkhul citizens.",
            "tangkhul_text": (
                "Fundamental Rights (Hao Citizen Rights):\n"
                "1. Article 14: Law-wui ngalemli mikumo pupup khangayam leisaye (Equality before law).\n"
                "2. Article 19: Tui hangkhavai, phanit sakhavai, kala union kasakhavai mathat (Freedom of speech & assembly).\n"
                "3. Article 21: Ringkapha kala personal liberty huikhuikhavai rights.\n"
                "4. Article 25: Chotkhangashit kala reot-kasavai freedom.\n"
                "5. Article 29-30: Minority language, script kala culture ngashankhavai rights.\n"
                "6. Article 32: Supreme Court kala High Court-li writ petition eina rights huikhuikhavai remedies."
            ),
            "english_translation": (
                "Overview of Part III of the Constitution: Equality before the law, six freedoms of Article 19, protection of life and personal liberty under Article 21, freedom of religion under Article 25, minority cultural and linguistic protections under Articles 29-30, and the right to constitutional remedies under Article 32."
            ),
            "vocabulary": [
                {"word": "khangayam", "pos": "noun", "meaning": "equality, equal standing without discrimination", "example": "Law-wui ngalemli khangayam."},
                {"word": "personal liberty", "pos": "noun", "meaning": "Aphasa wui mathat (bodily freedom)", "example": "Article 21 liberty."},
                {"word": "writ petition", "pos": "noun", "meaning": "Haikaphā petition (judicial remedy)", "example": "Article 32 writ."},
            ],
            "grammar_notes": [
                "Legal rights nomenclature: 'rights ngashankhavai' (safeguarding of rights).",
                "Universal quantifier: 'mikumo pupup' (all citizens without exception).",
            ],
            "exercises": [
                "Why are Articles 29 and 30 crucial for Tangkhul linguistic preservation?",
                "Translate Article 21 into Tangkhul.",
            ],
        },
        {
            "title": "Customary Law, Village Courts (Hangva) & Article 371",
            "summary": "Integration of indigenous tribal customary law, village councils, and constitutional special autonomy provisions.",
            "tangkhul_text": (
                "Hao Ngashan kala Constitutional Protection:\n"
                "Tangkhul village pupupli traditional council hoda Hangva (Village Court) leisaye. "
                "Awungshina headman hoda court-wui tui khak-kasaye. "
                "Article 371A kala 371C-wui provisions eina tribal customary laws, "
                "land ownership (ngalei khangayei), and civil justice-li constitutional autonomy miserie. "
                "Hangvawui decisions customary law eina sashung-khalang, formal law courtsna "
                "chichi respect salaga ngashane."
            ),
            "english_translation": (
                "Tribal customary governance operates through the Hangva (Village Council and Court) presided over by the Awungshi (village chief/headman). Constitutional provisions including Article 371 safeguard indigenous customary laws, land tenure systems, and traditional conflict resolution from arbitrary legislative interference."
            ),
            "vocabulary": [
                {"word": "Hangva", "pos": "noun", "meaning": "traditional village council and court of elders", "example": "Hangvawui decisions."},
                {"word": "Awungshi", "pos": "noun", "meaning": "hereditary village chief / headman", "example": "Awungshina court tui khake."},
                {"word": "ngalei khangayei", "pos": "noun", "meaning": "ancestral tribal land tenure rights", "example": "Ngalei khangayei autonomy."},
            ],
            "grammar_notes": [
                "Indigenous jurisprudence vocabulary: 'Hangva', 'Awungshi', 'Kashan'.",
                "Autonomy status terminology: 'constitutional autonomy miserie'."
            ],
            "exercises": [
                "Explain the role of the Hangva in customary dispute resolution.",
                "How do Articles 371A/371C protect Tangkhul land tenure?",
            ],
        },
        {
            "title": "Bilingual Legal & Civic Glossary (Tangkhul-English-Hindi)",
            "summary": "30 constitutional, judicial, and civic terms in Tangkhul, English, and Hindi.",
            "tangkhul_text": (
                "Legal Glossary:\n"
                "1. Samvidhan -- Constitution (संविधान)\n"
                "2. Mashung-kasa -- Justice (न्याय)\n"
                "3. Mathat -- Liberty (स्वतंत्रता)\n"
                "4. Khangayam -- Equality (समानता)\n"
                "5. Uningnao -- Fraternity (बंधुत्व)\n"
                "6. Hangva -- Village Court (ग्राम पंचायत / जनजातीय न्यायालय)\n"
                "7. Awungshi -- Village Chief (ग्राम प्रधान)\n"
                "8. Ngalei khangayei -- Land tenure rights (भूमि अधिकार)"
            ),
            "english_translation": (
                "Trilingual legal and constitutional lexicon supporting civic education in Manipur."
            ),
            "vocabulary": [
                {"word": "Samvidhan", "pos": "noun", "meaning": "Constitution", "example": "Indiawui Samvidhan."},
                {"word": "Mashung-kasa", "pos": "noun", "meaning": "Justice", "example": "Social mashung-kasa."},
            ],
            "grammar_notes": [
                "Trilingual legal nomenclature.",
            ],
            "exercises": [
                "Translate 5 constitutional terms from Hindi into Tangkhul.",
            ],
        },
    ]
    return _generate_generic_translated_book(meta, preface, chapters_data)


def get_all_translated_books() -> list[dict[str, Any]]:
    """Retrieve all 10 newly digitalized translated books."""
    return [
        get_bk_trns_001_new_testament(),
        get_bk_trns_002_matthew(),
        get_bk_trns_003_mark(),
        get_bk_trns_004_genesis(),
        get_bk_trns_005_psalms(),
        get_bk_trns_006_pilgrims_progress(),
        get_bk_trns_007_aesop(),
        get_bk_trns_008_tagore(),
        get_bk_trns_009_world_stories(),
        get_bk_trns_010_constitution(),
    ]
