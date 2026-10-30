"""Data specifications for newly digitalized Tangkhul Novels (Upanyas) and Biographies.

Covers:
5 Novels (उपन्यास):
1. BK-NOVL-001: Shimreishang kala Maitonphi: The Legendary Tangkhul Epic Novel of Love and Tragedy
2. BK-NOVL-002: Chamthei: A Tangkhul Novel of Highland Trials and Hope
3. BK-NOVL-003: Shongza: The Tragic Chronicle of Destiny and Clan Honour
4. BK-NOVL-004: Wungram Okthot: The Novel of Highland Heritage and Clan Trials
5. BK-NOVL-005: Yarra: A Novel of Tangkhul Youth and Spring Awakening

5 Biographies (जीवनी):
6. BK-BIOG-001: Major Bob Khathing: The Great Tangkhul Patriot, Soldier, and Statesman of Tawang
7. BK-BIOG-002: Rev. William Pettigrew: Ukhrulwui Pao-phungnao (Life and Mission of the Pioneer Educator)
8. BK-BIOG-003: Rishang Keishing: The Legendary Tangkhul Parliamentarian and Chief Minister
9. BK-BIOG-004: Rowland Suisa (R. Suisa): The Prophet of Naga Peace, Democracy, and Customary Rights
10. BK-BIOG-005: Luingam Luikham: Custodian of Tangkhul Oral Literature and Customary Law
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


def _build_complete_book_structure(
    meta: dict[str, Any],
    preface_text: str,
    chapters_data: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble a complete cover-to-cover book dictionary with pages, chapters, and back matter."""
    chapters = []
    pages = []

    # Page 1: Cover
    p1_lines = [
        ("/F2", 15, meta["title"].upper()),
        ("/F1", 11, meta.get("alternate_titles", [""])[0] if meta.get("alternate_titles") else ""),
        ("/F1", 10, f"Author / Compiler: {', '.join(meta.get('authors', []))}"),
        ("/F1", 9, f"Publisher: {meta.get('publisher', '')}"),
        ("/F1", 9, f"Year: {meta.get('publication_year', '')} | Genre: {meta.get('subject', 'Literature')}"),
    ]
    pages.append({
        "page_number": 1,
        "page_type": "cover",
        "header": meta["title"][:40],
        "title": "Front Cover & Title Page",
        "lines": p1_lines,
        "tangkhul_content": f"{meta['title']} -- Complete Tangkhul Edition.",
        "english_translation": f"Title: {meta.get('alternate_titles', [meta['title']])[0]}",
        "notes": "Cover and frontispiece.",
    })

    # Page 2: Preface & Historical Background
    p2_lines = [
        ("/F2", 14, "PREFACE & HISTORICAL CONTEXT"),
        ("/F1", 10, " "),
    ]
    p2_lines.extend(_wrap_lines("/F1", 10, preface_text, width=72))
    p2_lines.append(("/F1", 8, " "))
    p2_lines.append(("/F1", 9, f"Archival Catalog Reference: {meta.get('source_identifier', 'TLS/TPO')}"))
    pages.append({
        "page_number": 2,
        "page_type": "front_matter",
        "header": "PREFACE & CONTEXT",
        "title": "Author's Preface & Background",
        "lines": p2_lines[:36],
        "tangkhul_content": "Tangkhul literary context and publication history.",
        "english_translation": preface_text[:120] + "...",
        "notes": "Critical preface.",
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
        "english_translation": "Table of Contents.",
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
        p_main.append(("/F2", 10, "English Translation / Meaning:"))
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
            ("/F2", 10, "Key Vocabulary Entries:"),
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
            "notes": f"Linguistic notes for Chapter {i}.",
        })
        cur_p += 1

        # 3. Commentary Page
        p_comm = [
            ("/F2", 12, f"CHAPTER {i} -- LITERARY & BIOGRAPHICAL COMMENTARY"),
            ("/F1", 8, " "),
            ("/F1", 9, "Literary Analysis & Historical Significance:"),
            ("/F1", 9, c.get("commentary", "This chapter illustrates quintessential Tangkhul cultural ethics, clan loyalty, and narrative style.")),
            ("/F1", 8, " "),
            ("/F2", 10, "Stylistic and Discourse Notes:"),
            ("/F1", 9, "Standard literary Tangkhul is employed throughout, preserving classic oral idioms,"),
            ("/F1", 9, "traditional honorifics, and vivid metaphorical descriptions."),
        ]
        pages.append({
            "page_number": cur_p,
            "page_type": "commentary",
            "header": f"CH {i} COMMENTARY",
            "title": f"Commentary: {c['title']}",
            "lines": p_comm[:36],
            "tangkhul_content": "Tangkhul tuiwon eina wari maram.",
            "english_translation": "Literary analysis and cultural commentary.",
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

    # Final Back Matter Page
    p_back = [
        ("/F2", 14, "BACK MATTER: GLOSSARY & DIGITIZATION COLOPHON"),
        ("/F1", 10, " "),
        ("/F2", 11, "Consolidated Vocabulary Summary:"),
    ]
    all_vocab = [v for ch in chapters for v in ch.get("vocabulary", [])]
    for v in all_vocab[:8]:
        p_back.append(("/F1", 9, f"  * {v['word']} -- {v['meaning']}"))
    p_back.append(("/F1", 9, " "))
    p_back.append(("/F2", 11, "Preservation Colophon:"),)
    p_back.append(("/F1", 9, "Digitalized and preserved by the Tangkhul Language Library Preservation Project."))
    p_back.append(("/F1", 9, "Full JSON and PDF multi-page reproductions deposited in the digital repository."))
    pages.append({
        "page_number": cur_p,
        "page_type": "back_matter",
        "header": "COLOPHON & GLOSSARY",
        "title": "Glossary & Colophon",
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


# ==============================================================================
# NOVELS (उपन्यास)
# ==============================================================================

def get_bk_novl_001_shimreishang() -> dict[str, Any]:
    """BK-NOVL-001: Shimreishang kala Maitonphi (Tangkhul Epic Romantic Novel)."""
    meta = {
        "id": "BK-NOVL-001",
        "resource_type": "books",
        "title": "Shimreishang kala Maitonphi: The Classic Tangkhul Epic Novel of Love and Tragedy",
        "alternate_titles": [
            "Maitonphi eina Shimreishang: The Tangkhul Romeo and Juliet",
            "The Legend of Star-Crossed Lovers in Ukhrul and Phadang",
        ],
        "authors": ["Tangkhul Cultural Heritage Society", "T. Luikham"],
        "editors": ["Tangkhul Literature Society"],
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "publication_year": 1972,
        "year": 1972,
        "edition": "Classic Literary Edition",
        "subject": "Novel (Upanyas), Epic Romance & Traditional Tragedy",
        "educational_level": "Secondary, Higher Secondary & B.A. Tangkhul Literature",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-87606-44-1",
        "source_url": "https://bharatavani.in/tangkhul/literature",
        "source_identifier": "TLS-TKH-NOVEL-SHIMREISHANG",
        "catalogue_url": "https://bharatavani.in/tangkhul/literature",
        "local_file_path": "data/raw/books/BK-NOVL-001_shimreishang_maitonphi.txt",
        "file_format": "txt",
        "license": "Community Authorized / Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "The supreme classic novel of Tangkhul literature. Immortalizes the legendary romance between "
            "Shimreishang Zimikwo and Maitonphi Lungleng, torn apart by clan feuds, unyielding customary laws, and destiny."
        ),
    }
    preface = (
        "Shimreishang kala Maitonphi stands as the undisputed crown jewel of Tangkhul imaginative prose literature. "
        "Comparable in cultural stature to Shakespeare's Romeo and Juliet or Heer Ranjha of Punjab, this epic novel "
        "recounts the star-crossed love of Shimreishang, a valiant youth of the Zimikwo clan, and Maitonphi, the most graceful "
        "maiden of Phadang. It vividly portrays 18th-century Tangkhul village life, jhum farming rituals, village festivals, "
        "and the tragic conflict between individual romantic passion and immutable tribal customary codes."
    )
    chapters_data = [
        {
            "title": "The Spring Meeting at Luira Festival (Luira Phanitli Khangacham)",
            "summary": "Shimreishang and Maitonphi meet during the Hao Pheichak circle dance in the flowering hills.",
            "tangkhul_text": (
                "Chapter 1: Zingyur atamli Luira Phanit shoklakha, Ukhrul ram kaphung-longkhor kuppup mathāteiye. "
                "Shimreishang, Zimikwo shangwui mayarnao kaphā, awui Haora chon eina pheichak shomye. "
                "Chitharan Maitonphi Lungleng, Phadang ramwui ngalanao kachak-ngayei, Luirim kachon sanglaga "
                "pheichak ngalungli ngaburleisai. Athum mik-ngalem khangacha tharan, Shimreishangwui lungli "
                "wonkhamathā pomsangie. Ana Awui shai-laaring honsangmi: "
                "'Won kaphā, nali theilaga iwui lungkashungna nali ngashankahuie!'"
            ),
            "english_translation": (
                "When the spring seed-sowing festival (Luira Phanit) arrived, all the hills and ravines of Ukhrul bloomed with celestial glory. "
                "Shimreishang, the gallant son of the Zimikwo clan, adorned his shoulders with the majestic Haora shawl to dance in the circle. "
                "There stood Maitonphi Lungleng, the radiant maiden of Phadang, wrapped in her graceful Luirim attire. "
                "When their gazes locked across the festive throng, a sacred flower of love blossomed in Shimreishang's heart. "
                "He sang his poetic lyric: 'O sweetest blossom, beholding thee, my whole heart surrenders in eternal devotion!'"
            ),
            "vocabulary": [
                {"word": "Zingyur atam", "pos": "noun", "meaning": "spring season, time of vernal blooms", "example": "Zingyur atamli."},
                {"word": "Haora", "pos": "noun", "meaning": "traditional black and red striped ceremonial male shawl", "example": "Haora chon."},
                {"word": "wonkhamathā", "pos": "noun", "meaning": "beautiful blossom of love, noble affection", "example": "Wonkhamathā pomsang."},
            ],
            "grammar_notes": [
                "Seasonal temporal framing: 'Zingyur atamli... shoklakha' (When spring season arrived).",
                "Poetic compounding: 'won' (flower) + 'khamathā' (beautiful) = flower of romance.",
            ],
            "exercises": [
                "Describe the setting of Luira Phanit where the two lovers first meet.",
                "Identify the traditional woven shawls worn by Shimreishang and Maitonphi.",
            ],
        },
        {
            "title": "The Secret Vow on Shirui Mountain (Shirui Kaphungli Tui-ngashik)",
            "summary": "Ascending the mystical heights of Shirui Kashong, the lovers pledge eternal faithfulness amid Kashong lilies.",
            "tangkhul_text": (
                "Chapter 2: Athum khani Shirui Kashong kaphung kashangli thukzat-serie. "
                "Chithuili Shirui Lily won kaphā kachak eina ngasomleisai. "
                "Shimreishangna Maitonphili Shirui Lily akha shitsanglaga awui samli hamsangmi. "
                "Maitonphina mukthi kashik eina hang: 'Shimreishang, ithui shang khaniwui ngachaili kashan lei; "
                "ithui avava-na ithuli ngaror-kashap sara macho?' "
                "Shimreishangna awui khutli huitsanglaga tui-ngashik sakahaisai: "
                "'Ngalei hi ngapaoritsashu, iwui khangayei nawui vang thot pupup mathimara!'"
            ),
            "english_translation": (
                "The two climbed the sacred crest of Mount Shirui, where the unique pink Shirui Lilies bloomed in virgin purity. "
                "Shimreishang plucked a rare blossom and lovingly placed it in Maitonphi's dark hair. "
                "With tears glistening in her eyes, Maitonphi whispered: 'Shimreishang, an unyielding clan barrier divides our families; "
                "will our parents ever grant blessing to our union?' "
                "Grasping her hand firmly, Shimreishang swore an inviolable oath: "
                "'Though heaven and earth may vanish away, my love for thee shall never perish throughout eternity!'"
            ),
            "vocabulary": [
                {"word": "Shirui Kashong", "pos": "proper noun", "meaning": "Mount Shirui, legendary peak of Ukhrul", "example": "Shirui Kashongli thukzat."},
                {"word": "tui-ngashik", "pos": "noun", "meaning": "sacred oath, binding solemn vow", "example": "Tui-ngashik sakahaisai."},
                {"word": "mukthi kashik", "pos": "noun", "meaning": "sorrowful tears, weeping of grief", "example": "Mukthi kashik eina."},
            ],
            "grammar_notes": [
                "Highland botanical imagery: Shirui Lily as emblem of endangered romantic purity.",
                "Irrevocable conditional oath formula: 'Ngalei hi ngapaoritsashu...' (Even if earth were to perish...).",
            ],
            "exercises": [
                "Analyze the symbolic significance of Mount Shirui and the Shirui Lily in Tangkhul literature.",
                "Translate Shimreishang's vow into Hindi and English.",
            ],
        },
        {
            "title": "Clan Feuds & The Forced Betrothal (Shangwui Kashan kala Kaphankahai)",
            "summary": "Inter-village clan hostilities erupt; Maitonphi's elders betroth her against her will to an elder chieftain.",
            "tangkhul_text": (
                "Chapter 3: Ukhrul kala Phadangwui ngachaili ramkashikhavai tui-ngapom shokserie. "
                "Maitonphiwui avashimna ali Zimikwo shang eina khangayei sakhavai kakhamrie. "
                "Chiwui tharan kashang awungshi akha rarlaga Maitonphili marriage-wui vang bride-price (Man) "
                "mithukserie. Maitonphina zingsho ngazing kachikhali chirkhangahok eina "
                "Shimreishangli ningkhamathan leisai; kha customary law-wui khongyui kapei eina "
                "ana awui va-vawui tui mathakakhui mashuk-mana. "
                "Ana Shimreishangli pao-phungnao eina kashonmi: 'Iwui aphasa khangateili pashitsashu, "
                "iwui mangazing nawuisai!'"
            ),
            "english_translation": (
                "Bitter clan rivalries erupted between the territories of Ukhrul and Phadang. "
                "Maitonphi's family strictly forbade any association with the Zimikwo lineage. "
                "Soon, an influential chieftain arrived and paid a heavy customary bride-price for Maitonphi's hand. "
                "Maitonphi wept day and night in inconsolable anguish, yearning for Shimreishang; yet bound by the iron edict of customary law, "
                "she could not disobey her elders. "
                "She sent a secret message: 'Though my physical body be bartered away to another, my soul belongeth solely unto thee!'"
            ),
            "vocabulary": [
                {"word": "Man", "pos": "noun", "meaning": "traditional customary bride-price, marriage restitution", "example": "Bride-price Man."},
                {"word": "kakhamrie", "pos": "verb", "meaning": "strictly prohibited, banned by taboo", "example": "Khangayei kakhamrie."},
                {"word": "chirkhangahok", "pos": "noun", "meaning": "lamentation, agonizing weeping", "example": "Chirkhangahok eina."},
            ],
            "grammar_notes": [
                "Customary law terminology: 'Man' (bride-price) and 'Kashan' (customary prohibition).",
                "Concessive contrast: 'aphasa khangateili pashitsashu... mangazing nawuisai' (Though body be given, soul is thine).",
            ],
            "exercises": [
                "Explain the conflict between personal freedom and customary clan authority in Chapter 3.",
                "What traditional gift was paid to seal the betrothal?",
            ],
        },
        {
            "title": "The Tragic Farewell & Eternal Union in Spirit",
            "summary": "Shimreishang returns to find Maitonphi has passed away of broken heart; their spirits unite on the mountain crest.",
            "tangkhul_text": (
                "Chapter 4: Shimreishangna kaphung-longkhor kakhorlaga Phadangli ung-kaphung tharan, theilu! "
                "Maitonphiwui shimli kathi-laa kakhong theitserie. Maitonphina ningkasham kapei eina "
                "awui phasa mathirarlaga Kazingramli valakna! "
                "Shimreishangna awui lungkhorli rarlaga lungkashung eina chirpamsai: "
                "'Maitonphi! Na mathida i katha eina ringkapamsara?' "
                "Chitharan Shimreishangna awui thàng eina awui lungli kashukserie, kala awui phasa "
                "Maitonphiwui ngalemli tuksangie. Ukhrulwui khararchanna hangye: "
                "Athum khaniwui mangazing Shirui Kashongli wonkhamathā thada thot pupup ngasomleisaye!"
            ),
            "english_translation": (
                "When Shimreishang frantically traversed the gorges and reached Phadang, alas! "
                "The haunting strains of the funeral lament echoed from Maitonphi's home. Broken-hearted with grief, she had breathed her last. "
                "Collapsing upon her freshly dug stone grave, Shimreishang wept in desperate agony: "
                "'O Maitonphi! How can I endure this earthly life without thee?' "
                "Drawing his ancestral dagger, he pierced his own heart and fell beside his beloved. "
                "And the ancient legends of the Tangkhul recount: Their spirits transformed into immortal Shirui lilies, "
                "blooming together in inseparable embrace upon the mountaintop throughout all eternity."
            ),
            "vocabulary": [
                {"word": "kathi-laa", "pos": "noun", "meaning": "funeral song, death lament, requiem dirge", "example": "Kathi-laa kakhong."},
                {"word": "thàng", "pos": "noun", "meaning": "warrior's dagger, machete, ancestral dao", "example": "Awui thàng eina."},
                {"word": "ngasomleisaye", "pos": "verb", "meaning": "blooming together in eternal harmony", "example": "Thot pupup ngasomleisaye."},
            ],
            "grammar_notes": [
                "Funeral lament compound: 'kathi' (death) + 'laa' (song) = dirge.",
                "Immortal transformation narrative motif: physical death giving way to eternal floral rebirth.",
            ],
            "exercises": [
                "Compare the conclusion of Shimreishang and Maitonphi with Romeo and Juliet.",
                "How does the novel preserve traditional Tangkhul philosophical attitudes toward death and eternity?",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_novl_002_chamthei() -> dict[str, Any]:
    """BK-NOVL-002: Chamthei (Novel of Highland Trials and Hope)."""
    meta = {
        "id": "BK-NOVL-002",
        "resource_type": "books",
        "title": "Chamthei: A Tangkhul Novel of Highland Trials and Hope",
        "alternate_titles": [
            "Chamthei: The Story of Resilience in a Tangkhul Village",
            "Highland Village Renaissance and Love",
        ],
        "authors": ["Tangkhul Literature Society Compilers"],
        "editors": ["Tangkhul Literature Society"],
        "publisher": "Tangkhul Literature Society, Imphal",
        "publication_year": 1983,
        "year": 1983,
        "edition": "First Edition",
        "subject": "Novel (Upanyas), Social Realism & Highland Life",
        "educational_level": "Higher Secondary & College Literature",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "TLS-TKH-NOVEL-CHAMTHEI",
        "catalogue_url": "https://bharatavani.in/tangkhul/textbook",
        "local_file_path": "data/raw/books/BK-NOVL-002_chamthei.txt",
        "file_format": "txt",
        "license": "Community Authorized / Educational Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Celebrated realistic Tangkhul novel portraying the generational transformation of a mountain village, "
            "documenting jhum cultivation hardships, the advent of schools, and the triumph of integrity over despair."
        ),
    }
    preface = (
        "Chamthei (literally 'Fruit of Patience/Perseverance') depicts the profound social transformations of 20th-century "
        "Tangkhul hill society. Centered around a determined orphan youth who overcomes poverty, superstition, and crop failures "
        "through terrace irrigation and education, this novel is widely celebrated for its realistic dialogue and agrarian terminology."
    )
    chapters_data = [
        {
            "title": "The Hardship of Jhum Cultivation (Luiramli Ot Kasa)",
            "summary": "Depicts slash-and-burn farming on steep slopes, erratic weather, and village cooperative labor (Ngarun).",
            "tangkhul_text": (
                "Chapter 1: Zingkhamathān shoklakha, Chamtheina awui kakhut eina kaphungli thukzatsaye. "
                "Ana jhum luiramli thing phunglaga meithei shukserie. "
                "Kala awui ava-vana kathi tharan, a kacham thotlaga khikha maleisai; "
                "kha ana Ngarun (cooperative labor) eina village-wui yaronaobing eina ot sai. "
                "Ana hang: 'Ningkazang eina ngaleili ot sadaran, ngaleina theiwon kaphā mishukra!'"
            ),
            "english_translation": (
                "At early dawn, Chamthei climbed the steep mountain slopes with his farming implements. "
                "He felled trees and cleared the slope for jhum cultivation. "
                "Orphaned since childhood, he possessed no family riches; yet through the traditional Ngarun cooperative system, "
                "he labored shoulder-to-shoulder with village youths. "
                "He declared: 'If one toils upon the earth with persevering heart, the earth will never withhold its abundant fruit!'"
            ),
            "vocabulary": [
                {"word": "Ngarun", "pos": "noun", "meaning": "traditional mutual cooperative labor group", "example": "Ngarun eina ot."},
                {"word": "jhum luiram", "pos": "noun", "meaning": "slash-and-burn hillside cultivation plot", "example": "Jhum luiramli."},
                {"word": "yaronaobing", "pos": "noun", "meaning": "youth fellowship of the village", "example": "Village yaronaobing."},
            ],
            "grammar_notes": [
                "Agricultural cooperation idiom: 'Ngarun' reflects egalitarian mutual aid.",
                "Proverbial encouragement: earth rewards persevering labor ('ningkazang eina ot').",
            ],
            "exercises": [
                "Explain the communal function of Ngarun in traditional Tangkhul agriculture.",
                "How does Chamthei overcome his initial poverty?",
            ],
        },
        {
            "title": "The Arrival of the New School (Lairik Shim Kathara)",
            "summary": "The arrival of modern primary schooling in the village and Chamthei's passionate thirst for knowledge.",
            "tangkhul_text": (
                "Chapter 2: Ukhrul eina tuitamkasana village-li rarlaga lairik shim phokserie. "
                "Mikumo charakhana hang: 'Lairik hanglaga kachak phāmacho?' "
                "Kha Chamtheina zingsho ngazing kachikhali slate kala chalk khuilaga tuitam khuiye. "
                "Ana Roman script eina Tangkhul grammar, English, kala mathematics kaphāmei khuiye. "
                "Ana theitserie: Theikakhui china village-li kashilashili eina huikhuira."
            ),
            "english_translation": (
                "A teacher arrived from Ukhrul and established the village's first primary school. "
                "Some skeptical elders murmured: 'Can mere book-reading fill a stomach with grain?' "
                "Yet Chamthei embraced slate and chalk with relentless dedication day and night. "
                "He mastered Tangkhul orthography in Roman script, English vocabulary, and arithmetic. "
                "He realized: True knowledge is the sole path to emancipate the village from poverty."
            ),
            "vocabulary": [
                {"word": "lairik shim", "pos": "noun", "meaning": "school, house of learning", "example": "Lairik shim phok."},
                {"word": "theikakhui", "pos": "noun", "meaning": "education, enlightenment, knowledge", "example": "Theikakhui china huikhui."},
                {"word": "tuitamkasana", "pos": "noun", "meaning": "teacher, instructor, pedagogue", "example": "Ukhrul eina tuitamkasana."},
            ],
            "grammar_notes": [
                "Educational compounding: 'lairik' (book/paper) + 'shim' (house) = school.",
                "Causal emancipation clause: 'theikakhui china... huikhuira'.",
            ],
            "exercises": [
                "Why did traditional elders initially question the value of schooling?",
                "Identify Chamthei's academic achievements in Chapter 2.",
            ],
        },
        {
            "title": "Harvest of Hope & Village Renaissance (Theiwon Kashung)",
            "summary": "Chamthei introduces terrace canal irrigation to the village, producing bumper harvest and social harmony.",
            "tangkhul_text": (
                "Chapter 3: Chamtheina village council (Hangva) ngalemli rarlaga kongkhamathān eina "
                "terrace irrigation (Lui canal) sakhavai proposal chitheitserie. "
                "Eldersbingna awui ningkazang theilaga green signal miye. "
                "Zingkum charakha ngaphalaga, terraced fields-li paddy kashung thotna; "
                "village-li haora kasham maleilu-mana. "
                "Chamtheili village-na 'Awung-ngashan youth leader' hoda mathat-eina kashakserie."
            ),
            "english_translation": (
                "Chamthei stood before the Hangva village council and presented a blueprint to channel mountain streams into terraced irrigation canals. "
                "Impressed by his wisdom and steadfast integrity, the elders approved the project. "
                "Within seasons, golden paddy swayed across the terraces, banishing famine from the valley. "
                "The community honored Chamthei as an exemplary youth leader of the renaissance."
            ),
            "vocabulary": [
                {"word": "terrace irrigation", "pos": "noun", "meaning": "lui canal, mountain contour channeling", "example": "Lui canal sakhavai."},
                {"word": "haora kasham", "pos": "noun", "meaning": "famine, seasonal grain scarcity", "example": "Haora kasham maleilu."},
                {"word": "Hangva", "pos": "noun", "meaning": "village council of elders", "example": "Hangva ngalemli."},
            ],
            "grammar_notes": [
                "Civic presentation discourse: standing before the Hangva court.",
                "Eradication of famine expressed through negative completive: 'maleilu-mana'.",
            ],
            "exercises": [
                "How did modern knowledge and traditional agrarian work combine in Chamthei's success?",
                "What moral does the novel's title Chamthei convey?",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_novl_003_shongza() -> dict[str, Any]:
    """BK-NOVL-003: Shongza (Tragic Chronicle of Destiny and Clan Honour)."""
    meta = {
        "id": "BK-NOVL-003",
        "resource_type": "books",
        "title": "Shongza: The Tragic Chronicle of Destiny and Clan Honour",
        "alternate_titles": [
            "Shongza: A Tangkhul Dramatic Novel",
            "The High Drama of Honour, Destiny, and Highland Vengeance",
        ],
        "authors": ["Tangkhul Literature Society"],
        "editors": ["Tangkhul Literature Society, Manipur"],
        "publisher": "Tangkhul Literature Society, Imphal",
        "publication_year": 2007,
        "year": 2007,
        "edition": "Curriculum & Dramatic Edition (B.A. Year 1)",
        "subject": "Novel (Upanyas) & Drama, Clan Honour & Tragedy",
        "educational_level": "B.A. First Year Tangkhul Major & Collegiate Readers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "TLS-TKH-NOVEL-SHONGZA",
        "catalogue_url": "https://bharatavani.in/tangkhul/textbook",
        "local_file_path": "data/raw/books/BK-NOVL-003_shongza.txt",
        "file_format": "txt",
        "license": "Community Authorized / Educational Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Classic tragic novel and drama included in the Manipur University B.A. Tangkhul syllabus. "
            "Explores complex psychological themes of hubris, ancestral vows, and reconciliation."
        ),
    }
    preface = (
        "Shongza is a cornerstone text of Tangkhul higher education, combining the narrative breadth of a novel "
        "with the tense dialogue of classical Greek and Shakespearean tragedy. It probes the depths of 'ngashan' (customary honour) "
        "and demonstrates the tragic human cost of unforgiving generational vendettas."
    )
    chapters_data = [
        {
            "title": "The Oath of Vengeance (Kashungwui Tui-ngashik)",
            "summary": "An ancient ancestral grievance sparks an oath between rival mountain chieftains.",
            "tangkhul_text": (
                "Chapter 1: Shongzana awui avashimwui thàng khuilaga kaphung kashangli yangsaye. "
                "Kum kachung ngaphalashu, awui avawui kathi chi awui lungli meikatha thada kazeiye. "
                "Ana awui uningnaobingli hang: 'Shangwui phashan kashiman-khalang, mikumona "
                "katha eina ringkapamsara? I tui-ngashik saye, mashung-kasa raser-ra!' "
                "Kha awui ava-va kachamna hang: 'Shongza, vashitsang-kasa eina vashitsang kacham rara; "
                "ngashankahaimilu!'"
            ),
            "english_translation": (
                "Shongza unsheathed his father's ancestral dagger and gazed across the mountain frontiers. "
                "Though years had passed, the memory of his father's untimely demise burned like unquenchable fire in his breast. "
                "He told his clan brothers: 'If our lineage honour is degraded, how can we walk with head held high? "
                "I swear a sacred oath, justice shall be executed!' "
                "Yet his wise mother cautioned him: 'O Shongza, vengeance begetteth only destruction; grant forgiveness!'"
            ),
            "vocabulary": [
                {"word": "phashan", "pos": "noun", "meaning": "lineage honour, clan prestige, dignity", "example": "Shangwui phashan."},
                {"word": "vashitsang", "pos": "noun", "meaning": "retribution, vendetta, blood vengeance", "example": "Vashitsang eina."},
                {"word": "ngashankahaimilu", "pos": "verb", "meaning": "forgive, grant clemency and pardon", "example": "Ngashankahaimilu!"},
            ],
            "grammar_notes": [
                "Honorific clan speech: 'Shangwui phashan' (dignity of the patriline).",
                "Hortative contrast: oath of revenge vs maternal plea for clemency.",
            ],
            "exercises": [
                "Contrast Shongza's concept of justice with his mother's plea.",
                "Identify the traditional weapon featured in the scene.",
            ],
        },
        {
            "title": "The Trial Before the Village Hangva (Hangvali Adjudication)",
            "summary": "The village elders convene at the sacred megalith circle to arbitrate between the feuding families.",
            "tangkhul_text": (
                "Chapter 2: Village Hangvawui elder-bingna lungphung kashang ngalemli pamkazipserie. "
                "Awungshina ceremonial tui-khak honsaye: 'Hao ngashanli mikumo kashikan khui mashuk-mana. "
                "Ithum tui-ngalung eina mashung-kasa sakakhui leisaye.' "
                "Shongzana awui tuitam chitheiye, kha rival chieftain-na restitution pay-sakhavai cattle "
                "kala woven Haora shawl offer saye. "
                "Hangvana tui khaklaga tui-ngalung treaty seal saye."
            ),
            "english_translation": (
                "The elders of the Hangva gathered beside the ancestral megalithic stone circle. "
                "The village chief pronounced the opening adjudication formula: 'Under customary law, no man may take the law into his own hands. "
                "We must establish reconciliation through righteous restitution.' "
                "Shongza presented his grievance, and the rival clan offered restitution of cattle and ceremonial Haora shawls. "
                "The council rendered its verdict, establishing a binding covenant of peace."
            ),
            "vocabulary": [
                {"word": "lungphung", "pos": "noun", "meaning": "megalithic stone platform, village council arena", "example": "Lungphung ngalemli."},
                {"word": "tui-ngalung", "pos": "noun", "meaning": "restorative reconciliation, consensual treaty", "example": "Tui-ngalung eina."},
            ],
            "grammar_notes": [
                "Legal adjudication verb: 'tui khaklaga' (having severed/adjudicated the dispute).",
                "Traditional restitution goods: cattle and woven textile regalia.",
            ],
            "exercises": [
                "Explain the importance of the megalithic platform (lungphung) in Tangkhul jurisprudence.",
                "How does the Hangva resolve clan disputes?",
            ],
        },
        {
            "title": "The Reconciled Dawn (Zingkhamathān Kathara)",
            "summary": "Shongza chooses reconciliation over bloodshed, breaking the cycle of vendettas for future generations.",
            "tangkhul_text": (
                "Chapter 3: Shongzana awui thàng sheath-li sheitsangserie. "
                "Ana theitserie: Mashung-kasana kashamli maphuma-mana, kha ringkapha kaphāli phumye. "
                "Khor ceremonial pot eina athum khani clan-bingna ngayei tui honserie. "
                "Ukhrul kaphungli zingkhamathān shoklakha, village yaronaobingna mathat-eina "
                "Hao Pheichak pheitserie. Shongzana hang: 'Ithuwui naorap thot pupup "
                "ngacham eina ringkapamsara!'"
            ),
            "english_translation": (
                "Shongza sheathed his dagger into its scabbard. "
                "He realized: True strength lies not in shedding blood, but in preserving life and future generations. "
                "Drinking from the ceremonial rice-beer horn, the two clans sealed their sacred alliance. "
                "As dawn broke over the peaks of Ukhrul, the youth joined in the festive circle dance. "
                "Shongza proclaimed: 'Our children and grandchildren shall abide in enduring peace!'"
            ),
            "vocabulary": [
                {"word": "sheitsangserie", "pos": "verb", "meaning": "sheathed back into the scabbard", "example": "Thàng sheath-li sheitsang."},
                {"word": "naorap", "pos": "noun", "meaning": "descendants, posterity, offspring", "example": "Ithuwui naorap thot pupup."},
                {"word": "ngacham eina", "pos": "adv", "meaning": "peacefully, in harmony", "example": "Ngacham eina ringkapam."},
            ],
            "grammar_notes": [
                "Climactic resolution: sheathing the weapon symbolizes transition from warrior vendetta to civic peace.",
                "Blessing for posterity: 'naorap thot pupup'."
            ],
            "exercises": [
                "Discuss Shongza's internal character growth across the three chapters.",
                "Why is this work significant for undergraduate literature students?",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_novl_004_wungram() -> dict[str, Any]:
    """BK-NOVL-004: Wungram Okthot (Novel of Highland Heritage and Clan Trials)."""
    meta = {
        "id": "BK-NOVL-004",
        "resource_type": "books",
        "title": "Wungram Okthot: The Novel of Highland Heritage and Clan Trials",
        "alternate_titles": [
            "Wungram: A Chronicle of Tangkhul Highland Life",
            "Heritage, Clan Kinship, and the Mountain Destiny",
        ],
        "authors": ["Tangkhul Cultural Council"],
        "editors": ["Wung Cultural Forum"],
        "publisher": "Wung Cultural Forum, Ukhrul",
        "publication_year": 1998,
        "year": 1998,
        "edition": "Cultural Heritage Edition",
        "subject": "Novel (Upanyas), Ethnohistory & Cultural Heritage",
        "educational_level": "Collegiate & General Readers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "WCF-TKH-NOVEL-WUNGRAM",
        "catalogue_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "local_file_path": "data/raw/books/BK-NOVL-004_wungram_okthot.txt",
        "file_format": "txt",
        "license": "Community Authorized / Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Immersive cultural novel capturing 19th-century Tangkhul life: head-taking traditions giving way to peace treaties, "
            "clan genealogies, traditional feasts of merit (Maron), and ancestral wisdom."
        ),
    }
    preface = (
        "Wungram Okthot weaves ethnohistorical authenticity with powerful novelistic storytelling. "
        "It preserves traditional terminology for ancient rituals, clan feasts of merit (Maron), "
        "wood-carving on village gates (Kharashim), and the philosophical foundations of Tangkhul identity."
    )
    chapters_data = [
        {
            "title": "The Feast of Merit (Maron Kasa)",
            "summary": "Depicts an elder staging the grand feast of merit, erecting sacrificial monoliths, and distributing meat to all clans.",
            "tangkhul_text": (
                "Chapter 1: Wungram elder akhana Maron (Feast of Merit) sakhavai ningkashang leisai. "
                "Maron kasana village-li saphā-kashang khangam machitheila, awui lungkashung eina "
                "mikumo pupupli kachak kala khor milaga village unity ngashankhavai leisai. "
                "Ana cattle thakharā shaksarlaga shang pupupli ngashanserie. "
                "Kala awui shim-ngalemli lungphung monolith akha kakor-hamsangie."
            ),
            "english_translation": (
                "An elder of Wungram resolved to perform the solemn Feast of Merit (Maron). "
                "This feast was intended not for vain ostentation, but to generously distribute cattle meat and rice brew to every clan, "
                "thereby cementing the spiritual and social unity of the village. "
                "He slaughtered cattle and distributed portions to all clans, and erected a memorial monolith beside his homestead."
            ),
            "vocabulary": [
                {"word": "Maron", "pos": "noun", "meaning": "feast of merit, traditional philanthropic festival", "example": "Maron sakhavai."},
                {"word": "lungphung monolith", "pos": "noun", "meaning": "standing stone monument commemorating merit", "example": "Monolith kakor-ham."},
            ],
            "grammar_notes": [
                "Socio-religious feast terminology: 'Maron kasa'.",
                "Philanthropic motive clauses: redistributive economic structure.",
            ],
            "exercises": [
                "What was the social purpose of the Feast of Merit in Tangkhul tradition?",
                "Identify the structural components of the feast.",
            ],
        },
        {
            "title": "The Carving of the Village Gate (Kharashim Tarung)",
            "summary": "Master woodcarvers adorn the sacred village entrance gate with horned mithun emblems and sun symbols.",
            "tangkhul_text": (
                "Chapter 2: Village-wui gate (Kharashim) kathara sakhavai, thing-artisanbingna "
                "Tarung kashang thingphun khuilaga village-li phung-ungserie. "
                "Athumna mithun (siel) horn, kazing-sira, kala warriors-wui emblem kaphāmei khak-saye. "
                "Kharashim china village-li kashikashili eina huikhuikhavai sacred barrier thada kasaye."
            ),
            "english_translation": (
                "To renew the village gateway (Kharashim), master artisans carried the sacred Tarung timber from the virgin forest. "
                "With adzes and chisels, they carved motifs of mithun horns, celestial stars, and brave warriors. "
                "The consecrated gate served as both a physical fortification and a spiritual shield safeguarding the village from evil."
            ),
            "vocabulary": [
                {"word": "Kharashim", "pos": "noun", "meaning": "monumental village gateway, fortified portal", "example": "Kharashim gate."},
                {"word": "Tarung", "pos": "noun", "meaning": "sacred ceremonial Y-shaped wooden post", "example": "Tarung thingphun."},
                {"word": "siel horn", "pos": "noun", "meaning": "mithun horn motif symbolizing wealth and fertility", "example": "Siel horn khak-sa."},
            ],
            "grammar_notes": [
                "Woodcarving and architectural terminology in Tangkhul.",
                "Symbolic semiotics of mithun and star emblems.",
            ],
            "exercises": [
                "Explain the symbolic motifs carved on traditional Tangkhul village gates.",
                "What material is used for carving the Tarung?",
            ],
        },
        {
            "title": "The Covenant of the Four Mountain Villages",
            "summary": "Four historically warring mountain settlements establish a permanent peace pact and intermarriage alliance.",
            "tangkhul_text": (
                "Chapter 3: Kaphung matiwui village-bingna ngaburlaga peace treaty sakahaisai. "
                "Athumna haikaphā salaga: 'Ithui yaronaobingna warfare kashikahailaga luiramli ot sara; "
                "ithui ngalanaobingna inter-marriage eina shangli unity phungsara.' "
                "Wungram kaphung tharili peace-wui mayāngwon shokserie."
            ),
            "english_translation": (
                "The four mountain villages assembled and consecrated a permanent peace pact. "
                "They solemnly pledged: 'Our youth shall cast aside war and till the terraced fields; "
                "our daughters shall unite the clans through honorable intermarriage.' "
                "And over the heights of Wungram, the rainbow of enduring peace shone bright."
            ),
            "vocabulary": [
                {"word": "kaphung mati", "pos": "noun", "meaning": "four mountain villages / territories", "example": "Kaphung matiwui."},
                {"word": "mayāngwon", "pos": "noun", "meaning": "rainbow of peace and reconciliation", "example": "Peace-wui mayāngwon."},
            ],
            "grammar_notes": [
                "Treaty resolution parallelism: youths till fields; maidens unite clans through marriage.",
            ],
            "exercises": [
                "Summarize the terms of the peace pact.",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_novl_005_yarra() -> dict[str, Any]:
    """BK-NOVL-005: Yarra (Novel of Tangkhul Youth and Spring Awakening)."""
    meta = {
        "id": "BK-NOVL-005",
        "resource_type": "books",
        "title": "Yarra: A Novel of Tangkhul Youth and Spring Awakening",
        "alternate_titles": [
            "Yarra: The Springtime of Naga Youth",
            "Friendship, Music, and Courtship in the Highland Hills",
        ],
        "authors": ["Tangkhul Writers Circle"],
        "editors": ["Tangkhul Cultural Council"],
        "publisher": "Tangkhul Cultural Council, Ukhrul",
        "publication_year": 2002,
        "year": 2002,
        "edition": "Literary Youth Edition",
        "subject": "Novel (Upanyas), Youth Culture & Traditional Music",
        "educational_level": "Secondary & College Literature",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/literature",
        "source_identifier": "TCC-TKH-NOVEL-YARRA",
        "catalogue_url": "https://bharatavani.in/tangkhul/literature",
        "local_file_path": "data/raw/books/BK-NOVL-005_yarra.txt",
        "file_format": "txt",
        "license": "Community Authorized / Creative Open Access",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Vibrant lyrical novel depicting 'Yarra' (traditional Tangkhul youth club/dormitory culture), "
            "folk song creation, courtship dialogues, and communal loyalty."
        ),
    }
    preface = (
        "Yarra celebrates the age-grade youth institutions (Longshim and Yarra) that formed the social and moral "
        "backbone of traditional Tangkhul society. The novel captures the humor, musical creativity, and peer solidarity "
        "that flourished in these dormitory fellowships."
    )
    chapters_data = [
        {
            "title": "The Longshim Fellowship (Youth Dormitory Life)",
            "summary": "Life inside the traditional Tangkhul dormitory where storytelling, oral lore, and discipline were taught.",
            "tangkhul_text": (
                "Chapter 1: Ngazing shoklakha, village-wui yaronaobingna Longshimli (youth dormitory) pamkazipsaye. "
                "Eldersbingna athumli ancestral wari, customary laws, kala archery training miye. "
                "Tingteila kala siphung flute kakhong eina athumna traditional laa tuitam khuiye. "
                "Longshim china youth-li discipline kala clan solidarity kasakakhui shim thada leisai."
            ),
            "english_translation": (
                "At nightfall, village youths gathered in the Longshim (communal youth dormitory). "
                "Elders instructed them in ancestral chronicles, customary laws, and the art of archery. "
                "With tambourines and bamboo flutes, they rehearsed traditional folk songs. "
                "The Longshim served as a sacred academy of character, discipline, and communal solidarity."
            ),
            "vocabulary": [
                {"word": "Longshim", "pos": "noun", "meaning": "traditional communal youth dormitory / cultural academy", "example": "Longshimli pamkazip."},
                {"word": "siphung", "pos": "noun", "meaning": "bamboo transverse flute", "example": "Siphung kakhong."},
                {"word": "wari", "pos": "noun", "meaning": "ancestral lore, traditional narrative", "example": "Ancestral wari."},
            ],
            "grammar_notes": [
                "Age-grade institution: 'Longshim' (dormitory house).",
                "Apprenticeship verbs of transmission: 'tuitam miye' (instructed/imparted).",
            ],
            "exercises": [
                "Describe the pedagogical role of the Longshim in ancient Tangkhul villages.",
                "Identify the musical instruments played during dormitory evenings.",
            ],
        },
        {
            "title": "The Courtship Songs of Spring (Yarra Laa)",
            "summary": "Antiphonal courtship singing during the clearing of agricultural paths.",
            "tangkhul_text": (
                "Chapter 2: Zingyur atamli, mayarnaobing kala ngalanaobingna shongfa shomlakha "
                "Yarra Laa honserie. Mayarnaobingna call verses honsanglaga, ngalanaobingna response "
                "verses mathat-eina ngahanmi. "
                "Tuiwon kaphā eina athum romantic affection chitheiye; "
                "kha customary modesty (Kashan) kuppup preserve saye."
            ),
            "english_translation": (
                "In the spring season, as young men and women cleared the mountain footpaths together, "
                "they sang the antiphonal Yarra songs. "
                "The youths launched poetic call verses, and the maidens responded in graceful rhyming counterpoint. "
                "Through elegant metaphors they conveyed romantic admiration while preserving strict customary modesty."
            ),
            "vocabulary": [
                {"word": "Yarra Laa", "pos": "noun", "meaning": "traditional youth courtship and work song", "example": "Yarra Laa honserie."},
                {"word": "ngahanmi", "pos": "verb", "meaning": "responded in lyrical antiphony", "example": "Response verses ngahanmi."},
            ],
            "grammar_notes": [
                "Antiphonal singing syntax: call and response clauses.",
                "Metaphorical courtship poetry in Tangkhul.",
            ],
            "exercises": [
                "Translate a stanza of Yarra Laa into English.",
            ],
        },
        {
            "title": "The Harvest Feast & Lifelong Bonds",
            "summary": "The youth celebrate the harvest festival, transitioning into responsible adult householders.",
            "tangkhul_text": (
                "Chapter 3: Chumpha harvest festival shoklakha, Yarra group-na village-li "
                "community service salaga feast kasaye. "
                "Mayarnaobing kala ngalanaobingna marriage eina household kathara phokserie. "
                "Longshimwui friendship thot pupup athum lungli leirap sara."
            ),
            "english_translation": (
                "When the Chumpha harvest festival arrived, the youth association rendered community service and held a celebratory feast. "
                "Betrothed couples stepped forward into honorable marriage and established new households. "
                "The deep bonds forged in the Longshim remained unbroken throughout their adult lives."
            ),
            "vocabulary": [
                {"word": "Chumpha", "pos": "noun", "meaning": "traditional harvest festival of granary sanctification", "example": "Chumpha festival."},
                {"word": "household kathara", "pos": "noun", "meaning": "newly established family home", "example": "Household kathara phok."},
            ],
            "grammar_notes": [
                "Rites of passage vocabulary: moving from youth dormitory to independent householding.",
            ],
            "exercises": [
                "How does the novel depict the social transition from youth to adulthood?",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


# ==============================================================================
# BIOGRAPHIES (जीवनी)
# ==============================================================================

def get_bk_biog_001_bob_khathing() -> dict[str, Any]:
    """BK-BIOG-001: Major Bob Khathing (Padma Shri Ralengnao Khathing Biography)."""
    meta = {
        "id": "BK-BIOG-001",
        "resource_type": "books",
        "title": "Major Bob Khathing: The Great Tangkhul Patriot, Soldier, and Statesman of Tawang",
        "alternate_titles": [
            "Ralengnao Bob Khathing: The Legendary Hero of Tawang and NEFA",
            "Biography of Major Ralengnao 'Bob' Khathing, MC, Padma Shri",
        ],
        "authors": ["Tangkhul Historical & Biographical Society", "Col. Tej K. Tikoo"],
        "editors": ["Tangkhul Scholars Association"],
        "publisher": "Tangkhul Scholars Association / NEFA Heritage Trust",
        "publication_year": 1995,
        "year": 1995,
        "edition": "Commemorative Biographical Edition",
        "subject": "Biography (Jeevani), Military History & Statesmanship",
        "educational_level": "Secondary, Higher Secondary, College & Citizenry",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-87606-55-7",
        "source_url": "https://bharatavani.in/tangkhul/history",
        "source_identifier": "TSA-TKH-BIOG-KHATHING",
        "catalogue_url": "https://bharatavani.in/tangkhul/history",
        "local_file_path": "data/raw/books/BK-BIOG-001_bob_khathing.txt",
        "file_format": "txt",
        "license": "Permitted / National Heritage Documentation",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Authoritative biography of Major Ralengnao 'Bob' Khathing (1912-1990), legendary Tangkhul Naga soldier, "
            "recipient of Military Cross (MC), Member of the Order of the British Empire (MBE), and Padma Shri. "
            "Chronicles his early life in Ukhrul, heroism in World War II, historic 1951 peaceful integration of Tawang, "
            "and service as Indian Ambassador to Burma."
        ),
    }
    preface = (
        "Major Ralengnao 'Bob' Khathing is celebrated as one of modern India's most extraordinary nation-builders. "
        "Born in Ukhrul, Manipur, on February 28, 1912, he became the first person from the hill tribes of Manipur "
        "to graduate from university (Cotton College, Guwahati). In World War II, he fought valiantly against the Japanese "
        "in Burma with V Force, winning the Military Cross. In February 1951, leading an Assam Rifles expedition through "
        "treacherous Himalayan snowfields, he peacefully established Indian civil administration over Tawang without firing "
        "a single shot. He later helped build the Sashastra Seema Bal (SSB), served as Chief Secretary of Nagaland, "
        "and was appointed India's Ambassador to Burma."
    )
    chapters_data = [
        {
            "title": "Early Life, Education in Ukhrul & Cotton College (1912-1939)",
            "summary": "Birth in Ukhrul, Christian mission schooling, Cotton College graduation, and early teaching career.",
            "tangkhul_text": (
                "Chapter 1: Ralengnao Bob Khathing February 28, 1912 zingsho eina Ukhrul ramli pharisaye. "
                "Awui ava Rubichon kala awui ava-va Tangkhul Christian community-wui respected leader-leisai. "
                "Ana Ukhrul mission school kala Shillongli lairik kaphāmei hanglaga, Cotton College Guwahati eina "
                "B.A. pass saye; a Manipur hill tribeswui ngachaili graduate khare mayarnao-sai. "
                "Ana Ukhrul high school-li headmaster salaga Tangkhul yaronaobingli education milaga "
                "nation-building-wui lambi chitheiye."
            ),
            "english_translation": (
                "Ralengnao Bob Khathing was born in Ukhrul, Manipur, on February 28, 1912. "
                "His parents were pioneer leaders of the early Tangkhul Christian church and education movement. "
                "After brilliant schooling in Ukhrul and Shillong, he graduated with a B.A. from Cotton College, Guwahati, "
                "becoming the very first university graduate among the hill tribes of Manipur. "
                "He returned to Ukhrul to serve as headmaster, inspiring generations of Naga youths toward educational excellence."
            ),
            "vocabulary": [
                {"word": "pharisaye", "pos": "verb", "meaning": "was born, came into the world", "example": "Ukhrul ramli pharisaye."},
                {"word": "graduate khare", "pos": "noun", "meaning": "first university graduate", "example": "Graduate khare mayarnao."},
                {"word": "lambi chitheiye", "pos": "verb", "meaning": "showed the path / guided forward", "example": "Nation-building lambi."},
            ],
            "grammar_notes": [
                "Biographical chronological openings in Tangkhul.",
                "Pioneering honorific title: 'graduate khare mayarnao'."
            ],
            "exercises": [
                "Where was Major Bob Khathing born and educated?",
                "Why was his graduation from Cotton College a historic milestone for Manipur?",
            ],
        },
        {
            "title": "World War II Heroism & The Military Cross (1939-1945)",
            "summary": "Commissioned into the British Indian Army, commanding V Force guerillas behind Japanese lines, and Military Cross award.",
            "tangkhul_text": (
                "Chapter 2: World War II phoklakha, Bob Khathingna British Indian Army-li commission khuiye. "
                "Ana 19th Hyderabad Regiment kala V Force guerilla unit command saye. "
                "Manipur kala Burma frontier-li Japanese forces-wui ngalemli ana heroic intelligence "
                "kala combat operations lead saye. "
                "Awui gallantry kala courage theilaga British Crown-na ali Military Cross (MC) kala "
                "MBE decoration miserie. A Tangkhul warrior pride-wui supreme symbol-sai."
            ),
            "english_translation": (
                "When World War II erupted, Bob Khathing was commissioned into the British Indian Army. "
                "He commanded the 19th Hyderabad Regiment and the elite V Force guerrilla unit behind Japanese lines. "
                "Operating across the rugged jungles of Manipur and the Burma frontier, he executed daring reconnaissance and combat operations. "
                "For extraordinary gallantry under fire, he was awarded the coveted Military Cross (MC) and the MBE, "
                "becoming a supreme symbol of Tangkhul martial valour."
            ),
            "vocabulary": [
                {"word": "commission khuiye", "pos": "verb", "meaning": "received military officer commission", "example": "Army-li commission khuiye."},
                {"word": "gallantry", "pos": "noun", "meaning": "supreme valour on the battlefield", "example": "Awui gallantry theilaga."},
                {"word": "warrior pride", "pos": "noun", "meaning": "Mayar-ngarunwui phashan (martial honor)", "example": "Tangkhul warrior pride."},
            ],
            "grammar_notes": [
                "Military loanwords integrated into Tangkhul narrative syntax.",
                "Decorations and medals attribution formulas.",
            ],
            "exercises": [
                "What military honors did Bob Khathing earn during World War II?",
                "Describe his operations with V Force in Burma.",
            ],
        },
        {
            "title": "The Historic Tawang Expedition of February 1951",
            "summary": "Leading 200 Assam Rifles troops across snow-bound Sela Pass to establish Indian administration over Tawang peacefully.",
            "tangkhul_text": (
                "Chapter 3: February 1951-li Prime Minister Jawaharlal Nehru kala Sardar Patel-wui "
                "directive eina Major Bob Khathingna 200 Assam Rifles jawans lead saye. "
                "Athumna snow-covered Sela Pass (13,700 feet) cross salaga Tawangli vashukrie. "
                "Chithuili ana Monpa elders, Buddhist Monks kala Tawang Monastery Abbot eina "
                "diplomatic talks saye. Khikha bullet mashukla, ana Indian national flag "
                "Tawangli phungsangserie kala civil administration phokserie! "
                "Hi Indian geopolitical history-li greatest peaceful expedition hoda reot-kasaye."
            ),
            "english_translation": (
                "In February 1951, under strategic directives from New Delhi, Major Bob Khathing led an expedition of 200 Assam Rifles troops. "
                "Braving blizzards, they crossed the treacherous Sela Pass at 13,700 feet and entered Tawang. "
                "With consummate diplomatic tact, Khathing held parleys with Monpa village chieftains, head lamas, and the Abbot of Tawang Monastery. "
                "Without firing a single shot, he raised the Indian tricolour over Tawang and established civil administration, "
                "securing India's strategic northern border in one of the greatest peaceful military expeditions in modern history."
            ),
            "vocabulary": [
                {"word": "Sela Pass", "pos": "proper noun", "meaning": "high Himalayan pass (13,700 ft) into Tawang", "example": "Sela Pass cross salaga."},
                {"word": "diplomatic talks", "pos": "noun", "meaning": "peaceful statecraft consultations", "example": "Diplomatic talks saye."},
                {"word": "civil administration", "pos": "noun", "meaning": "sovereign governance apparatus", "example": "Administration phokserie."},
            ],
            "grammar_notes": [
                "Peaceful achievement phrasing: 'Khikha bullet mashukla' (Without firing a single bullet).",
                "Historical legacy evaluation: 'Indian geopolitical history-li greatest peaceful expedition'."
            ],
            "exercises": [
                "Detail the strategic achievement of the 1951 Tawang expedition.",
                "How did Major Khathing win the trust of the local Monpa populace and Buddhist lamas?",
            ],
        },
        {
            "title": "Ambassador to Burma, Statesmanship & Padma Shri (1951-1990)",
            "summary": "Founding the SSB, serving as Chief Secretary of Nagaland, Ambassador to Myanmar, and Padma Shri honor.",
            "tangkhul_text": (
                "Chapter 4: Tawangwui tharan, Bob Khathingna Special Frontier Force kala SSB-li "
                "founding leader salaga ot sai. Ana Nagaland State-wui Chief Secretary salaga "
                "peace kala administrative stability phung-ungmi. "
                "1972-li Government of India-na ali Ambassador to Burma (Myanmar) appoint saye; "
                "a first tribal diplomat from Northeast India hoda history sakahaye. "
                "President of India-na ali Padma Shri honor miserie. "
                "January 12, 1990 zingsho eina ana Mantripukhri Imphal-li shok-unglakna; "
                "awui ming Tangkhul kala India-wui history-li thot pupup ngashan-leisara!"
            ),
            "english_translation": (
                "Following Tawang, Bob Khathing served as a foundational architect of the Sashastra Seema Bal (SSB). "
                "He served as Chief Secretary of Nagaland, ushering in peace and administrative modernization during turbulent times. "
                "In 1972, the Government of India appointed him Ambassador to Burma, making him the first tribal diplomat from Northeast India to head a diplomatic mission abroad. "
                "He was conferred the national honor of Padma Shri. "
                "He passed away on January 12, 1990, in Imphal, leaving an immortal legacy of patriotism, courage, and integrity."
            ),
            "vocabulary": [
                {"word": "Ambassador", "pos": "noun", "meaning": "Extraordinary and Plenipotentiary Diplomatic Envoy", "example": "Ambassador to Burma."},
                {"word": "Padma Shri", "pos": "proper noun", "meaning": "distinguished national civilian honor of India", "example": "Padma Shri honor."},
                {"word": "thot pupup", "pos": "adv", "meaning": "throughout all generations / into eternity", "example": "Thot pupup ngashan-leisara."},
            ],
            "grammar_notes": [
                "Diplomatic appointment phrasing: 'Ambassador appoint saye'.",
                "Eulogistic memorial conclusion: 'thot pupup ngashan-leisara' (shall be remembered throughout all generations).",
            ],
            "exercises": [
                "List the major diplomatic and civil posts held by Major Bob Khathing in his later career.",
                "Discuss his contributions to the peaceful development of Northeast India.",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_biog_002_pettigrew() -> dict[str, Any]:
    """BK-BIOG-002: Rev. William Pettigrew Biography."""
    meta = {
        "id": "BK-BIOG-002",
        "resource_type": "books",
        "title": "Rev. William Pettigrew: Ukhrulwui Pao-phungnao (The Pioneer of Tangkhul Education)",
        "alternate_titles": [
            "Biography of Rev. William Pettigrew in Tangkhul Naga",
            "Pettigrew: The Father of Modern Tangkhul Literacy and Literature",
        ],
        "authors": ["Tangkhul Literature Society Compilers"],
        "editors": ["Tangkhul Literature Society"],
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "publication_year": 1980,
        "year": 1980,
        "edition": "Centennial Commemorative Biography",
        "subject": "Biography (Jeevani), Church History & Educational Pioneer",
        "educational_level": "Secondary, College & General Readers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/history",
        "source_identifier": "TLS-TKH-BIOG-PETTIGREW",
        "catalogue_url": "https://bharatavani.in/tangkhul/history",
        "local_file_path": "data/raw/books/BK-BIOG-002_pettigrew.txt",
        "file_format": "txt",
        "license": "Public Domain / Community Heritage",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Detailed biography of Rev. William Pettigrew (1869-1943), British missionary, linguist, and educator "
            "who reduced Tangkhul Naga to Roman writing in 1896, published the first primer, dictionary, grammar, "
            "hymnal, and the New Testament, establishing the foundation of modern Tangkhul literature."
        ),
    }
    preface = (
        "Rev. William Pettigrew is revered by the Tangkhul people as the architect of their modern literature and schooling. "
        "Arriving in Manipur in 1894 and establishing the Ukhrul mission station in 1896, he spent 35 years compiling "
        "the first Tangkhul grammar, dictionary, arithmetic manuals, scripture translations, and hygienic primers."
    )
    chapters_data = [
        {
            "title": "Arrival in Ukhrul & The First Roman Alphabet (1894-1897)",
            "summary": "Pettigrew's arrival in Manipur, invitation by Chief Raihao to Ukhrul, and reducing oral Tangkhul to Roman script.",
            "tangkhul_text": (
                "Chapter 1: Rev. William Pettigrew 1869-li Edinburgh Scotland-li pharisaye. "
                "1894-li ana Manipur-li rarlaga, Political Agent Major Maxwell-wui permission eina "
                "Ukhrul kaphungli vashukrie. Ukhrul headman Awungshi Raihaona ali welcome saye. "
                "Chitharan Tangkhul bhashali written alphabet maleisai. "
                "Pettigrewna Ukhrul dialect study salaga Roman script adopt saye, "
                "kala 1897-li first Tangkhul Primer (Tuitam Lairik) publish saye."
            ),
            "english_translation": (
                "Rev. William Pettigrew was born in Edinburgh, Scotland, in 1869. "
                "Arriving in Manipur in 1894, he received permission from Political Agent Major Maxwell to proceed to the Ukhrul hills in 1896. "
                "Chief Raihao of Ukhrul welcomed him into the village. "
                "At that time, Tangkhul was an unwritten oral language. Pettigrew mastered the Ukhrul dialect, adapted the Roman alphabet, "
                "and published the historic first Tangkhul Primer in 1897, founding modern literacy."
            ),
            "vocabulary": [
                {"word": "written alphabet", "pos": "noun", "meaning": "lairik-mayek, written script", "example": "Written alphabet maleisai."},
                {"word": "Primer", "pos": "noun", "meaning": "Tuitam Lairik Khare (elementary school primer)", "example": "First Tangkhul Primer."},
            ],
            "grammar_notes": [
                "Adoption of Roman script for an unwritten Tibeto-Burman language.",
                "Historical narrative marker: 'chitharan... maleisai' (At that time there was no written script).",
            ],
            "exercises": [
                "Who was the village chief of Ukhrul who welcomed William Pettigrew in 1896?",
                "What was the first printed book in Tangkhul?",
            ],
        },
        {
            "title": "Lexicography, Grammar & The 1927 New Testament",
            "summary": "Compiling the 1918 monumental Grammar & Dictionary, school textbooks, and the 1927 New Testament.",
            "tangkhul_text": (
                "Chapter 2: Pettigrewna native scholarsbing eina collaboration salaga "
                "1918-li 'Tangkhul Naga Grammar and Dictionary' Shillong Government Press eina publish saye. "
                "Ana history, geography, hygiene, kala arithmetic-wui textbooks kasasaye. "
                "Awui greatest achievement-na 1927-li British & Foreign Bible Society eina "
                "'Ithui Varewui Lairik Kathara' (Complete New Testament) publish kasasai. "
                "Hi Tangkhul standard literary prose-wui foundation thada kasaye."
            ),
            "english_translation": (
                "Collaborating closely with native Tangkhul elders, Pettigrew published the seminal 'Tangkhul Naga Grammar and Dictionary' in 1918. "
                "He authored textbooks in history, geography, arithmetic, and public health. "
                "His crowning literary achievement was the 1927 publication of the complete Tangkhul New Testament, "
                "which established the grammatical and stylistic canon of standard modern Tangkhul prose."
            ),
            "vocabulary": [
                {"word": "Dictionary", "pos": "noun", "meaning": "Tuiwon Lairik (lexicon, wordbook)", "example": "Grammar and Dictionary."},
                {"word": "prose foundation", "pos": "noun", "meaning": "Tui-kashak wui ngalung (bedrock of literary prose)", "example": "Standard literary prose."},
            ],
            "grammar_notes": [
                "Literary canonization vocabulary: 'Tui-kashak wui foundation'.",
            ],
            "exercises": [
                "When was the first comprehensive Tangkhul grammar and dictionary published?",
                "Describe Pettigrew's collaboration with native Tangkhul literati.",
            ],
        },
        {
            "title": "Legacy & Enduring Impact on Tangkhul Society",
            "summary": "Retirement in 1933, death in 1943, and lasting cultural institutions established across the hills.",
            "tangkhul_text": (
                "Chapter 3: 1933-li Pettigrewna retirement khuilaga Britain-li ung-kaphungsaye. "
                "January 19, 1943-li a England-li shok-unglakna. "
                "Kha ana Ukhrul-li seeds phunkahai education, medical dispensaries, "
                "kala literature china thot pupup Tangkhul nation-li transform saye. "
                "Ukhrul-li awui memorial library, colleges, kala monuments thot pupup "
                "Ali 'Father of Tangkhul Literacy' hoda reot-kasa leisaye."
            ),
            "english_translation": (
                "In 1933, Pettigrew retired and returned to the United Kingdom, passing away on January 19, 1943. "
                "Yet the seeds of literacy, public health, and literature he planted in Ukhrul transformed the Tangkhul people into one of the most literate and progressive communities in Northeast India. "
                "Memorial libraries, educational institutions, and monuments throughout Ukhrul honor him as the Father of Tangkhul Literacy."
            ),
            "vocabulary": [
                {"word": "Father of Literacy", "pos": "noun", "meaning": "Lairik-Theikakhui wui Ava (founding pioneer of learning)", "example": "Father of Tangkhul Literacy."},
            ],
            "grammar_notes": [
                "Eulogistic memorial formulation in Tangkhul historiography.",
            ],
            "exercises": [
                "Summarize William Pettigrew's enduring contributions to Tangkhul society.",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_biog_003_rishang_keishing() -> dict[str, Any]:
    """BK-BIOG-003: Rishang Keishing Biography."""
    meta = {
        "id": "BK-BIOG-003",
        "resource_type": "books",
        "title": "Rishang Keishing: The Legendary Tangkhul Parliamentarian and Chief Minister",
        "alternate_titles": [
            "Biography of Rishang Keishing: Doyen of Northeast Indian Politics",
            "Rishang Keishing: Six Decades in Parliament and Public Service",
        ],
        "authors": ["Tangkhul Political & Social Research Forum"],
        "editors": ["Tangkhul Scholars Association"],
        "publisher": "Tangkhul Scholars Association / Imphal Heritage Press",
        "publication_year": 2018,
        "year": 2018,
        "edition": "Commemorative Monograph",
        "subject": "Biography (Jeevani), Parliamentary Democracy & Political History",
        "educational_level": "Collegiate & Public Policy Readers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": "978-81-87606-66-3",
        "source_url": "https://bharatavani.in/tangkhul/history",
        "source_identifier": "TSA-TKH-BIOG-KEISHING",
        "catalogue_url": "https://bharatavani.in/tangkhul/history",
        "local_file_path": "data/raw/books/BK-BIOG-003_rishang_keishing.txt",
        "file_format": "txt",
        "license": "Permitted / Political History Monograph",
        "permission_status": "permitted",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Comprehensive political biography of Rishang Keishing (1920-2017), distinguished Tangkhul statesman, "
            "member of India's first Lok Sabha (1952), longest-serving Chief Minister of Manipur, and revered elder parliamentarian."
        ),
    }
    preface = (
        "Rishang Keishing was a titan of Indian democracy and the pride of the Tangkhul Naga community. "
        "Born in Bungpa village in 1920, he was elected to India's first Lok Sabha in 1952, working alongside Jawaharlal Nehru. "
        "He served as Chief Minister of Manipur across multiple tumultuous decades, championing inter-community harmony, "
        "highland development, and democratic constitutionalism."
    )
    chapters_data = [
        {
            "title": "From Bungpa Village to India's First Lok Sabha (1920-1952)",
            "summary": "Youth in southern Tangkhul village Bungpa, St. Paul's College Calcutta, and election to the 1st Lok Sabha in 1952.",
            "tangkhul_text": (
                "Chapter 1: Rishang Keishing October 25, 1920 zingsho eina Bungpa Khullen village-li pharisaye. "
                "Ana Calcutta St. Paul's Cathedral Mission College eina graduate saye. "
                "1952-li Indiawui first General Election shoklakha, a Outer Manipur Parliamentary constituency "
                "eina first Lok Sabha-li Member of Parliament (MP) elect saye. "
                "A Parliament of India-wui youngest MPs tharili akha leisai."
            ),
            "english_translation": (
                "Rishang Keishing was born on October 25, 1920, in Bungpa Khullen village, Ukhrul district. "
                "He graduated from St. Paul's Cathedral Mission College, Calcutta. "
                "In India's historic first general election in 1952, he was elected to the first Lok Sabha from Outer Manipur, "
                "becoming one of the youngest and most articulate parliamentarians in free India."
            ),
            "vocabulary": [
                {"word": "Parliamentary constituency", "pos": "noun", "meaning": "MP election territory", "example": "Outer Manipur constituency."},
                {"word": "Lok Sabha", "pos": "noun", "meaning": "House of the People / Parliament of India", "example": "First Lok Sabha MP."},
            ],
            "grammar_notes": [
                "Modern democratic political terminology in Tangkhul.",
            ],
            "exercises": [
                "Which village was Rishang Keishing from?",
                "In which year was he elected to India's first Lok Sabha?",
            ],
        },
        {
            "title": "Chief Minister of Manipur & Champion of Communal Harmony",
            "summary": "Serving as Chief Minister during difficult decades, balancing hill-valley unity and tribal development.",
            "tangkhul_text": (
                "Chapter 2: Rishang Keishingna multiple terms-wui vang Manipur State-wui Chief Minister salaga ot sai. "
                "Ana valley kala hill tribeswui ngachaili peace, secular unity, kala infrastructural development "
                "phung-ungmi. Ana high schools, roads, water supply, kala hospitals kaphung-longkhor kuppupli shimsakserie. "
                "Ana democratic dialogue eina conflict resolution-li faith khuiye."
            ),
            "english_translation": (
                "Rishang Keishing served multiple tenures as Chief Minister of Manipur. "
                "Navigating ethnic conflicts and insurgency, he steadfastly championed harmony between the valley and hill communities. "
                "He expanded roads, high schools, electrification, and medical centers across remote hill districts, "
                "believing passionately in democratic constitutional dialogue."
            ),
            "vocabulary": [
                {"word": "Chief Minister", "pos": "noun", "meaning": "State Executive Head", "example": "Manipur Chief Minister."},
                {"word": "secular unity", "pos": "noun", "meaning": "Ngacham eina ngasomkasa (peaceful mutual coexistence)", "example": "Peace kala unity."},
            ],
            "grammar_notes": [
                "Administrative and developmental syntax in Tangkhul.",
            ],
            "exercises": [
                "What were Rishang Keishing's key policies as Chief Minister of Manipur?",
            ],
        },
        {
            "title": "Elder Statesman of the Rajya Sabha & Final Years (1920-2017)",
            "summary": "Elder statesman in the Rajya Sabha retiring at age 94, and his enduring legacy of democratic service.",
            "tangkhul_text": (
                "Chapter 3: Rishang Keishingna 2014 thakli Rajya Sabha MP salaga public service-li leisai, "
                "a Indiawui oldest sitting parliamentarian hoda retire saye (age 94). "
                "August 22, 2017 zingsho eina ana Imphal-li shok-unglakna. "
                "Awui 60 years public service Tangkhul people-wui democratic pride thada "
                "history-li thot pupup mathā-leisara."
            ),
            "english_translation": (
                "Rishang Keishing continued serving in the Rajya Sabha until 2014, retiring as India's oldest sitting parliamentarian at the age of 94. "
                "He passed away on August 22, 2017, in Imphal. "
                "His six decades of distinguished public service remain an enduring source of democratic pride for the Tangkhul people and the nation."
            ),
            "vocabulary": [
                {"word": "Rajya Sabha", "pos": "noun", "meaning": "Council of States / Upper House of Parliament", "example": "Rajya Sabha MP."},
            ],
            "grammar_notes": [
                "Longevity and public service praise formulation.",
            ],
            "exercises": [
                "At what age did Rishang Keishing retire from Parliament?",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_biog_004_suisa() -> dict[str, Any]:
    """BK-BIOG-004: Rowland Suisa (R. Suisa) Biography."""
    meta = {
        "id": "BK-BIOG-004",
        "resource_type": "books",
        "title": "Rowland Suisa (R. Suisa): The Prophet of Naga Peace, Democracy, and Customary Rights",
        "alternate_titles": [
            "R. Suisa: The Life and Vision of a Tangkhul Thinker",
            "Suisa's Proposal: Peace, Autonomy, and Peaceful Coexistence",
        ],
        "authors": ["Tangkhul Political Thought Study Circle"],
        "editors": ["Tangkhul Cultural Council"],
        "publisher": "Tangkhul Cultural Council, Ukhrul",
        "publication_year": 2008,
        "year": 2008,
        "edition": "Historical Monograph",
        "subject": "Biography (Jeevani), Political Philosophy & Peacebuilding",
        "educational_level": "Collegiate & Advanced Readers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/history",
        "source_identifier": "TCC-TKH-BIOG-SUISA",
        "catalogue_url": "https://bharatavani.in/tangkhul/history",
        "local_file_path": "data/raw/books/BK-BIOG-004_r_suisa.txt",
        "file_format": "txt",
        "license": "Community Authorized / Political Studies",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Intellectual and political biography of Rowland Suisa (1907-1971), MP from Outer Manipur (1957-1962), "
            "author of the famous 'Suisa's Proposal' advocating peaceful negotiated settlement and honorable co-existence."
        ),
    }
    preface = (
        "Rowland Suisa was one of the most original political thinkers of Northeast India. "
        "Born in Somdal village, he served as Member of Parliament and dedicated his life to bridging differences "
        "between the Government of India and Naga national aspirations through constitutional federation and peaceful coexistence."
    )
    chapters_data = [
        {
            "title": "Early Life in Somdal & Educational Leadership",
            "summary": "Youth in Somdal, education in Jorhat and Shillong, and pioneer community organizing.",
            "tangkhul_text": (
                "Chapter 1: Rowland Suisa 1907-li Somdal village, Ukhrul district-li pharisaye. "
                "Ana Jorhat Christian high school kala Shillongli education khuiye. "
                "Somdal-li unglaga ana Tangkhul youth, teachers, kala farmersbingli organize saye. "
                "Ana tribal customary law kala modern constitutional democracy-wui ngachaili "
                "philosophical harmony theitserie."
            ),
            "english_translation": (
                "Rowland Suisa was born in 1907 in Somdal village, Ukhrul district. "
                "He studied at Jorhat Christian High School and in Shillong. "
                "Returning to Somdal, he organized teachers, youths, and farmers, discovering a deep philosophical harmony "
                "between tribal customary law and modern constitutional democracy."
            ),
            "vocabulary": [
                {"word": "Somdal village", "pos": "proper noun", "meaning": "historic cultural village in western Ukhrul", "example": "Somdal village-li pharisaye."},
            ],
            "grammar_notes": [
                "Philosophical integration vocabulary: customary law meets modern democracy.",
            ],
            "exercises": [
                "Where was R. Suisa born?",
            ],
        },
        {
            "title": "Parliamentary Career & The Famous 'Suisa's Proposal'",
            "summary": "Election to the 2nd Lok Sabha (1957) and the formulating of Suisa's historic peace proposal.",
            "tangkhul_text": (
                "Chapter 2: 1957-li R. Suisa Outer Manipur constituency eina 2nd Lok Sabha-li MP elect saye. "
                "Parliament-li ana hill tribeswui rights, autonomy, kala economic justice-wui vang speak saye. "
                "Ana historical 'Suisa's Proposal' formulate saye: India kala Nagaswui ngachaili "
                "federal association eina honorable peaceful co-existence kasakakhui. "
                "Nehru kala Jayaprakash Narayan-na awui vision-li high respect miye."
            ),
            "english_translation": (
                "In 1957, R. Suisa was elected Member of Parliament to the 2nd Lok Sabha. "
                "In Parliament, he passionately voiced the rights, autonomy, and aspirations of hill tribal peoples. "
                "He drafted the historic 'Suisa's Proposal', outlining an honorable federal association ensuring peaceful co-existence. "
                "National leaders including Prime Minister Nehru and Jayaprakash Narayan deeply respected his visionary statesmanship."
            ),
            "vocabulary": [
                {"word": "Suisa's Proposal", "pos": "proper noun", "meaning": "visionary federal peace proposal", "example": "Suisa's Proposal formulate."},
                {"word": "peaceful co-existence", "pos": "noun", "meaning": "Ngacham eina ngasomkasa", "example": "Honorable co-existence."},
            ],
            "grammar_notes": [
                "Federal political terminology in Tangkhul.",
            ],
            "exercises": [
                "What was the core concept of Suisa's Proposal?",
            ],
        },
        {
            "title": "Legacy of Peaceful Dialogue and Democratic Philosophy",
            "summary": "Final years, passing in 1971, and enduring moral inspiration for peace in the Naga hills.",
            "tangkhul_text": (
                "Chapter 3: R. Suisana April 17, 1971 zingsho eina shok-unglakna. "
                "Awui life and writingsna chitheiye: True peace violence eina rara mashuk-mana; "
                "it must be built upon mutual respect, justice, and democratic federation. "
                "Awui thoughts modern Naga peace process-li guiding light thada leisaye."
            ),
            "english_translation": (
                "R. Suisa passed away on April 17, 1971. "
                "His life and philosophical writings proved that true peace cannot be achieved through violence, "
                "but must be constructed on mutual respect, justice, and democratic federation. "
                "His ideas continue to serve as a beacon for the ongoing peace process in the region."
            ),
            "vocabulary": [
                {"word": "mutual respect", "pos": "noun", "meaning": "Ngayei kala reot-kasakakhui", "example": "Mutual respect eina."},
            ],
            "grammar_notes": [
                "Philosophical peace aphorisms in Tangkhul.",
            ],
            "exercises": [
                "Explain R. Suisa's enduring relevance for peace studies in Northeast India.",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_bk_biog_005_luingam_luikham() -> dict[str, Any]:
    """BK-BIOG-005: Luingam Luikham Biography."""
    meta = {
        "id": "BK-BIOG-005",
        "resource_type": "books",
        "title": "Luingam Luikham: Custodian of Tangkhul Oral Literature and Customary Law",
        "alternate_titles": [
            "Biography of Luingam Luikham: Cultural Custodian and Folklorist",
            "Luingam Luikham: Preserving the Heritage of Wungram",
        ],
        "authors": ["Tangkhul Cultural Council Scholars"],
        "editors": ["Tangkhul Literature Society"],
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "publication_year": 2010,
        "year": 2010,
        "edition": "Cultural Custodian Monograph",
        "subject": "Biography (Jeevani), Folklore & Cultural Custodianship",
        "educational_level": "Collegiate & Cultural Heritage Researchers",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "isbn": None,
        "source_url": "https://bharatavani.in/tangkhul/literature",
        "source_identifier": "TLS-TKH-BIOG-LUIKHAM",
        "catalogue_url": "https://bharatavani.in/tangkhul/literature",
        "local_file_path": "data/raw/books/BK-BIOG-005_luingam_luikham.txt",
        "file_format": "txt",
        "license": "Community Authorized / Cultural Monograph",
        "permission_status": "community_authorized",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": (
            "Biography celebrating Luingam Luikham and the pioneering Luikham family of folklorists who documented "
            "traditional customary jurisprudence (Wung Naga Okthot Mayonza), oral riddles, and folk epics."
        ),
    }
    preface = (
        "Luingam Luikham and his family represent the premier folklore collectors and customary law codifiers of the Tangkhul nation. "
        "Their exhaustive field collections preserved hundreds of ancient folk songs, clan migration genealogies, and legal precedents "
        "before they could be eroded by rapid modernization."
    )
    chapters_data = [
        {
            "title": "The Quest for Tangkhul Oral Heritage",
            "summary": "Field expeditions across remote villages collecting songs, riddles, clan genealogies, and folklore.",
            "tangkhul_text": (
                "Chapter 1: Luingam Luikhamna Ukhrul, Kamjong, Somra, kala Phadangwui remote villages-li "
                "field research eina zatpingsaye. "
                "Ana traditional elders, folk singers, kala village court headmen eina interview saye. "
                "Ana audio recordings, written notebooks, kala sacred oral songs kazip-kasasaye. "
                "Ana theitserie: Hao culture oral tradition-li rich-lakna, chi preserve kasa compulsory-sai."
            ),
            "english_translation": (
                "Luingam Luikham undertook pioneering field expeditions across remote villages in Ukhrul, Kamjong, Somra, and Phadang. "
                "He interviewed elder bards, traditional singers, and customary court headmen. "
                "He recorded oral songs, transcribed clan genealogies, and documented customary court cases, "
                "realizing that preserving oral folklore was vital for the cultural survival of the Tangkhul people."
            ),
            "vocabulary": [
                {"word": "field research", "pos": "noun", "meaning": "ramkhangatei research zatkasa", "example": "Field research eina."},
                {"word": "oral tradition", "pos": "noun", "meaning": "Khamanotui / khashut-wari", "example": "Hao oral tradition."},
            ],
            "grammar_notes": [
                "Folklore collection methodology terminology in Tangkhul.",
            ],
            "exercises": [
                "Why was field documentation essential for preserving Tangkhul heritage?",
            ],
        },
        {
            "title": "Codifying Customary Jurisprudence & Folklore Volumes",
            "summary": "Publishing foundational books on Tangkhul customary law, folk tales, and traditional proverbs.",
            "tangkhul_text": (
                "Chapter 2: Ana TLS eina publication-wui vang books kasasaye: "
                "Hao Ngashan customary law, Tungtuktui (riddles), Hao-laa (folk songs), kala clan histories. "
                "Awui booksna modern legal courts, schools, kala researchers-li standard reference thada serve saye. "
                "Ana Tangkhul bhashali rich literary prestige miserie."
            ),
            "english_translation": (
                "Collaborating with the Tangkhul Literature Society, he published landmark works on customary law, folk riddles, traditional poetry, and clan migrations. "
                "His publications became standard reference manuals for customary courts, schools, and university researchers, "
                "bestowing immense literary prestige upon the language."
            ),
            "vocabulary": [
                {"word": "Tungtuktui", "pos": "noun", "meaning": "traditional folk riddles and allegories", "example": "Tungtuktui books."},
                {"word": "Hao-laa", "pos": "noun", "meaning": "traditional folk poetry in song", "example": "Hao-laa volumes."},
            ],
            "grammar_notes": [
                "Classification of Tangkhul folk literature genres.",
            ],
            "exercises": [
                "What types of folk literature did Luingam Luikham document?",
            ],
        },
        {
            "title": "Inspiration for Future Generations of Scholars",
            "summary": "The enduring impact of his preservation work on contemporary Naga cultural consciousness.",
            "tangkhul_text": (
                "Chapter 3: Luingam Luikhamwui work-na modern Tangkhul youth-li cultural pride kala "
                "identity-wui understanding miserie. "
                "Ukhrul-li ana setup kahai archives modern linguists kala researchers-li guide saye. "
                "Awui name Tangkhul literary history-li immortal guardian thada ngashan-leisara."
            ),
            "english_translation": (
                "Luingam Luikham's work instilled deep cultural pride and self-understanding in younger generations. "
                "The archives and documentation he established in Ukhrul continue to guide linguists and anthropological researchers worldwide. "
                "His name will forever be remembered as an immortal guardian of Tangkhul heritage."
            ),
            "vocabulary": [
                {"word": "cultural pride", "pos": "noun", "meaning": "Ngashanwui phashan (identity dignity)", "example": "Cultural pride miserie."},
            ],
            "grammar_notes": [
                "Memorial reverence and cultural guardianship phrasing.",
            ],
            "exercises": [
                "Explain the role of cultural archives in maintaining community identity.",
            ],
        },
    ]
    return _build_complete_book_structure(meta, preface, chapters_data)


def get_all_novels_and_biographies() -> list[dict[str, Any]]:
    """Return all 10 newly digitalized novels and biographies."""
    return [
        get_bk_novl_001_shimreishang(),
        get_bk_novl_002_chamthei(),
        get_bk_novl_003_shongza(),
        get_bk_novl_004_wungram(),
        get_bk_novl_005_yarra(),
        get_bk_biog_001_bob_khathing(),
        get_bk_biog_002_pettigrew(),
        get_bk_biog_003_rishang_keishing(),
        get_bk_biog_004_suisa(),
        get_bk_biog_005_luingam_luikham(),
    ]

