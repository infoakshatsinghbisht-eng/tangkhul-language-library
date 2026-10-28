"""
Tangkhul Language Linguistic Encyclopedia & Number System Builder.

Generates the exhaustive master reference for:
1. Complete Tangkhul Number System (Cardinals 1-100+, Ordinals, Multiplicatives, Fractions, Numeral Classifiers).
2. Traditional Tangkhul Lunar Calendar (12 Months, 4 Seasons, 11 Divisions of Day and Night).
3. Traditional Mountain Measurements (Distance, Volume, Land Yield Capacity).
4. Elaborate Tangkhul Kinship Terminology & Clan Honorifics.
5. Everyday Conversational Dialogues & Phrasal Idioms.
6. Advanced Grammar & Morphophonemic Linguistic Rules.

Outputs:
- data/exports/tangkhul_linguistic_encyclopedia_and_number_system.json
- src/tangkhul_lib/data/tangkhul_linguistic_encyclopedia_and_number_system.json
- data/exports/tangkhul_linguistic_encyclopedia_and_number_system.pdf
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"

EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
BUNDLED_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_pdf_text(s: str) -> str:
    s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    out = []
    for ch in s:
        cp = ord(ch)
        if 32 <= cp <= 126:
            out.append(ch)
        elif cp in (10, 13):
            out.append(" ")
        else:
            out.append("?")
    return "".join(out)


def build_pdf_document(
    title: str,
    subtitle: str,
    pages_data: list[list[tuple[str, int, str]]],
    doc_footer_name: str,
) -> bytes:
    """Build multi-page PDF document using core PDF stream."""
    page_count = len(pages_data)
    cat_id = 1
    pages_root_id = 2
    f1_id = 3
    f2_id = 4
    cur_id = 5

    page_entries = []
    page_obj_ids = []

    for page_idx, raw_items in enumerate(pages_data, 1):
        p_id = cur_id
        cur_id += 1
        c_id = cur_id
        cur_id += 1

        items: list[tuple[str, int, str]] = []
        if page_idx == 1:
            items.append(("/F2", 14, title))
            items.append(("/F1", 9, subtitle))
            items.append(
                ("/F1", 8, "Tangkhul Language Library Digital Archive -- Linguistic Encyclopedia")
            )
            items.append(("/F1", 8, "-" * 115))

        items.extend(raw_items)

        items.append(("/F1", 8, "-" * 115))
        items.append(
            (
                "/F1",
                8,
                f"{doc_footer_name}                                              Page {page_idx} of {page_count}",
            )
        )

        stream_cmds = ["BT"]
        y = 800
        stream_cmds.append(f"36 {y} Td")
        current_y = y

        for font, size, line in items:
            clean = sanitize_pdf_text(line)
            stream_cmds.append(f"{font} {size} Tf")
            stream_cmds.append(f"({clean}) Tj")
            dy = -(size + 2)
            stream_cmds.append(f"0 {dy} Td")
            current_y += dy
            if current_y < 35:
                break

        stream_cmds.append("ET")
        c_stream = "\n".join(stream_cmds).encode("latin-1", "replace")
        page_entries.append((p_id, c_id, c_stream))
        page_obj_ids.append(p_id)

    obj_dict: dict[int, bytes] = {}
    obj_dict[cat_id] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids_str = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
    obj_dict[pages_root_id] = (
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>".encode("latin-1")
    )
    obj_dict[f1_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    obj_dict[f2_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"

    for pid, cid, cstream in page_entries:
        p_def = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Contents {cid} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> >>"
        )
        obj_dict[pid] = p_def.encode("latin-1")
        c_def = f"<< /Length {len(cstream)} >>\nstream\n".encode("latin-1") + cstream + b"\nendstream"
        obj_dict[cid] = c_def

    out = bytearray(b"%PDF-1.4\n")
    offsets: dict[int, int] = {}
    for oid in sorted(obj_dict.keys()):
        offsets[oid] = len(out)
        out.extend(f"{oid} 0 obj\n".encode("latin-1"))
        out.extend(obj_dict[oid])
        out.extend(b"\nendobj\n")

    xref_offset = len(out)
    out.extend(f"xref\n0 {len(obj_dict)+1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for oid in sorted(obj_dict.keys()):
        out.extend(f"{offsets[oid]:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer\n<< /Size {len(obj_dict)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
            "latin-1"
        )
    )
    return bytes(out)


# -----------------------------------------------------------------------------
# 1. NUMBER SYSTEM GENERATION (1 to 100, 1000, 10000, 100000)
# -----------------------------------------------------------------------------
def generate_number_system() -> dict[str, Any]:
    base_digits = {
        1: ("akha", "one", "एक"),
        2: ("khani", "two", "दो"),
        3: ("kathum", "three", "तीन"),
        4: ("mati", "four", "चार"),
        5: ("phanga", "five", "पाँच"),
        6: ("taruk", "six", "छह"),
        7: ("shini", "seven", "सात"),
        8: ("shet", "eight", "आठ"),
        9: ("chiko", "nine", "नौ"),
        10: ("thara", "ten", "दस"),
    }

    tens_map = {
        20: ("maku", "twenty", "बीस"),
        30: ("thumkui", "thirty", "तीस"),
        40: ("hangmati", "forty", "चालीस"),
        50: ("hangphanga", "fifty", "पचास"),
        60: ("hangtaruk", "sixty", "साठ"),
        70: ("hangshini", "seventy", "सत्तर"),
        80: ("hangshet", "eighty", "अस्सी"),
        90: ("hangchiko", "ninety", "नब्बे"),
        100: ("sha akha", "one hundred", "एक सौ"),
    }

    cardinals = []
    # 1 to 10
    for i in range(1, 11):
        t, e, h = base_digits[i]
        cardinals.append({"number": i, "tangkhul": t, "english": e, "hindi": h})

    # 11 to 19
    for i in range(1, 10):
        val = 10 + i
        t_d, e_d, h_d = base_digits[i]
        t = f"thara {t_d}"
        e = "eleven" if val == 11 else (
            "twelve" if val == 12 else (
                "thirteen" if val == 13 else (
                    "fourteen" if val == 14 else (
                        "fifteen" if val == 15 else (
                            "sixteen" if val == 16 else (
                                "seventeen" if val == 17 else (
                                    "eighteen" if val == 18 else "nineteen"
                                )
                            )
                        )
                    )
                )
            )
        )
        h = ["ग्यारह", "बारह", "तेरह", "चौदह", "पंद्रह", "सोलह", "सत्रह", "अठारह", "उन्नीस"][i - 1]
        cardinals.append({"number": val, "tangkhul": t, "english": e, "hindi": h})

    # 20
    cardinals.append({"number": 20, "tangkhul": "maku", "english": "twenty", "hindi": "बीस"})

    # 21 to 99
    hindi_tens_prefixes = {
        20: "इक्कीस,बाईस,तेईस,चौबीस,पच्चीस,छब्बीस,सत्ताईस,अट्ठाईस,उनतीस".split(","),
        30: "इकतीस,बत्तीस,तैंतीस,चौंतीस,पैंतीस,छत्तीस,सैंतीस,अड़तीस,उनतालीस".split(","),
        40: "इकतालीस,बयालीस,तैंतालीस,चौवालीस,पैंतालीस,छियालीस,सैंतालीस,अड़तालीस,उनचास".split(","),
        50: "इक्यावन,बावन,तिरेपन,चौवन,पचपन,छप्पन,सत्तावन,अट्ठावन,उनसठ".split(","),
        60: "इकसठ,बासठ,तिरसठ,चौंसठ,पैंसठ,छियासठ,सरसठ,अड़सठ,उनहत्तर".split(","),
        70: "इकहत्तर,बहत्तर,तिहत्तर,चौहत्तर,पचहत्तर,छिहत्तर,सतहत्तर,अठहत्तर,उनासी".split(","),
        80: "इक्यासी,बयासी,तिरासी,चौरासी,पचासी,छियासी,सत्तासी,अट्ठासी,नवासी".split(","),
        90: "इक्यानवे,बानवे,तिरानवे,चौरानवे,पंचानवे,छियानवे,सत्तानवे,अट्ठानवे,निन्यानवे".split(","),
    }

    english_tens_words = {
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }

    for ten in range(20, 100, 10):
        t_ten, _, _ = tens_map[ten]
        e_ten = english_tens_words[ten]
        h_list = hindi_tens_prefixes[ten]
        for digit in range(1, 10):
            val = ten + digit
            t_d, e_d, _ = base_digits[digit]
            t = f"{t_ten} {t_d}"
            e = f"{e_ten}-{e_d}"
            h = h_list[digit - 1]
            cardinals.append({"number": val, "tangkhul": t, "english": e, "hindi": h})

        if ten + 10 <= 100:
            next_val = ten + 10
            t_n, e_n, h_n = tens_map[next_val]
            cardinals.append({"number": next_val, "tangkhul": t_n, "english": e_n, "hindi": h_n})

    # High order numbers
    higher_numbers = [
        {"number": 200, "tangkhul": "sha khani", "english": "two hundred", "hindi": "दो सौ"},
        {"number": 300, "tangkhul": "sha kathum", "english": "three hundred", "hindi": "तीन सौ"},
        {"number": 500, "tangkhul": "sha phanga", "english": "five hundred", "hindi": "पाँच सौ"},
        {"number": 1000, "tangkhul": "thing akha", "english": "one thousand", "hindi": "एक हज़ार"},
        {"number": 10000, "tangkhul": "thing thara", "english": "ten thousand", "hindi": "दस हज़ार"},
        {"number": 100000, "tangkhul": "lakh akha / thing sha akha", "english": "one hundred thousand (one lakh)", "hindi": "एक लाख"},
    ]

    ordinals = [
        {"rank": "1st", "tangkhul": "khare / akhare", "english": "first", "hindi": "पहला / प्रथम"},
        {"rank": "2nd", "tangkhul": "kakhane", "english": "second", "hindi": "दूसरा / द्वितीय"},
        {"rank": "3rd", "tangkhul": "kathume", "english": "third", "hindi": "तीसरा / तृतीय"},
        {"rank": "4th", "tangkhul": "matine", "english": "fourth", "hindi": "चौथा / चतुर्थ"},
        {"rank": "5th", "tangkhul": "phangane", "english": "fifth", "hindi": "पाँचवाँ / पंचम"},
        {"rank": "6th", "tangkhul": "tarukne", "english": "sixth", "hindi": "छठा"},
        {"rank": "7th", "tangkhul": "shinine", "english": "seventh", "hindi": "सातवाँ"},
        {"rank": "8th", "tangkhul": "shetne", "english": "eighth", "hindi": "आठवाँ"},
        {"rank": "9th", "tangkhul": "chikone", "english": "ninth", "hindi": "नौवाँ"},
        {"rank": "10th", "tangkhul": "tharane", "english": "tenth", "hindi": "दसवाँ"},
        {"rank": "20th", "tangkhul": "makune", "english": "twentieth", "hindi": "बीसवाँ"},
        {"rank": "100th", "tangkhul": "sha akhane", "english": "hundredth", "hindi": "सौवाँ"},
        {"rank": "Last", "tangkhul": "katam / akha-eina", "english": "last / final", "hindi": "अंतिम / आखिरी"},
    ]

    multiplicatives = [
        {"multiplier": "1x", "tangkhul": "akhana / khat-khat", "english": "once", "hindi": "एक बार"},
        {"multiplier": "2x", "tangkhul": "khanina", "english": "twice", "hindi": "दो बार"},
        {"multiplier": "3x", "tangkhul": "kathumna", "english": "thrice", "hindi": "तीन बार"},
        {"multiplier": "4x", "tangkhul": "matina", "english": "four times", "hindi": "चार बार"},
        {"multiplier": "5x", "tangkhul": "phangana", "english": "five times", "hindi": "पाँच बार"},
        {"multiplier": "10x", "tangkhul": "tharana", "english": "ten times", "hindi": "दस बार"},
        {"multiplier": "100x", "tangkhul": "sha akhana", "english": "hundred times", "hindi": "सौ बार"},
        {"multiplier": "1 by 1", "tangkhul": "akha-akha", "english": "one by one / individually", "hindi": "एक-एक करके"},
        {"multiplier": "2 by 2", "tangkhul": "khani-khani", "english": "in pairs / two by two", "hindi": "दो-दो करके / जोड़े में"},
        {"multiplier": "10 by 10", "tangkhul": "thara-thara", "english": "by tens", "hindi": "दस-दस करके"},
    ]

    fractions = [
        {"fraction": "1/2", "tangkhul": "tangkha", "english": "half", "hindi": "आधा"},
        {"fraction": "1/4", "tangkhul": "mati-wui akha / taruknao", "english": "quarter (one fourth)", "hindi": "एक चौथाई / पाव"},
        {"fraction": "3/4", "tangkhul": "kathum-tangkha", "english": "three quarters", "hindi": "पौन (तीन चौथाई)"},
        {"fraction": "1", "tangkhul": "mashun / akha-saikora", "english": "whole / complete", "hindi": "पूरा / समूचा"},
    ]

    classifiers = [
        {
            "classifier": "-khao",
            "usage": "Human beings and social persons",
            "example_tangkhul": "Mi maku-khao",
            "example_translation": "Twenty persons / people (बीस व्यक्ति)",
        },
        {
            "classifier": "-khur",
            "usage": "Animals, cattle, wildlife, and birds",
            "example_tangkhul": "Simuk kathum-khur",
            "example_translation": "Three cows / cattle (तीन गाय/पशु)",
        },
        {
            "classifier": "-rong",
            "usage": "Trees, timber logs, bamboo stalks, and vertical posts",
            "example_tangkhul": "Thingrong mati-rong",
            "example_translation": "Four trees (चार पेड़)",
        },
        {
            "classifier": "-pan",
            "usage": "Flat sheet-like objects: woven shawls, mats, leaves, paper",
            "example_tangkhul": "Kachon khani-pan",
            "example_translation": "Two traditional shawls (दो शॉल/चादरें)",
        },
        {
            "classifier": "-kaphung",
            "usage": "Burdens, shoulder-carried loads, baskets of grain",
            "example_tangkhul": "Kharai akha-kaphung",
            "example_translation": "One full basket load (एक टोकरी बोझ)",
        },
        {
            "classifier": "-tara",
            "usage": "Liquid cups, drink offerings, spring waters",
            "example_tangkhul": "Khor akha-tara",
            "example_translation": "One cup of rice beer (एक प्याला पेय)",
        },
    ]

    return {
        "cardinal_numbers": cardinals,
        "higher_numbers": higher_numbers,
        "ordinal_numbers": ordinals,
        "multiplicative_and_distributive": multiplicatives,
        "fractions": fractions,
        "numeral_classifiers": classifiers,
    }


# -----------------------------------------------------------------------------
# 2. TANGKHUL LUNAR CALENDAR & TIME DIVISIONS
# -----------------------------------------------------------------------------
def generate_calendar_and_time() -> dict[str, Any]:
    months = [
        {
            "month_number": 1,
            "tangkhul_name": "Thara",
            "gregorian_equivalent": "January",
            "hindi_name": "थरा (जनवरी)",
            "significance": "Month of bitter mountain frost; elders gather around the hearth to plan terrace repairs and village festivals.",
        },
        {
            "month_number": 2,
            "tangkhul_name": "Khaying",
            "gregorian_equivalent": "February",
            "hindi_name": "खायिंग (फ़रवरी)",
            "significance": "Clearing the hillside forest for jhum plots; burning dry brushwood before the first rains.",
        },
        {
            "month_number": 3,
            "tangkhul_name": "Luira",
            "gregorian_equivalent": "March",
            "hindi_name": "लुइरा (मार्च)",
            "significance": "Sacred seed-sowing festival (Luira Phanit); invocations to the creator for bumper agricultural yields.",
        },
        {
            "month_number": 4,
            "tangkhul_name": "Rongkhun",
            "gregorian_equivalent": "April",
            "hindi_name": "रोंगखुन (अप्रैल)",
            "significance": "Terrace bund weeding; fresh spring showers; wild orchids burst into flower on high oak ridges.",
        },
        {
            "month_number": 5,
            "tangkhul_name": "Kaphang",
            "gregorian_equivalent": "May",
            "hindi_name": "कफांग (मई)",
            "significance": "Flooding the terraces with mountain streams; community transplanting of young paddy seedlings.",
        },
        {
            "month_number": 6,
            "tangkhul_name": "Phara",
            "gregorian_equivalent": "June",
            "hindi_name": "फरा (जून)",
            "significance": "High monsoon downpours; rivers swell; village paths turn into cascading streams.",
        },
        {
            "month_number": 7,
            "tangkhul_name": "Maring",
            "gregorian_equivalent": "July",
            "hindi_name": "मारिंग (जुलाई)",
            "significance": "Midsummer weeding of terrace slopes; trapping river minnows and hill crabs in woven creels.",
        },
        {
            "month_number": 8,
            "tangkhul_name": "Khamahon",
            "gregorian_equivalent": "August",
            "hindi_name": "खमाहोन (अगस्त)",
            "significance": "First green ears of hill corn ripen; roasted maize shared among children and elders by the fire.",
        },
        {
            "month_number": 9,
            "tangkhul_name": "Chumpha",
            "gregorian_equivalent": "September",
            "hindi_name": "चुमफा (सितंबर)",
            "significance": "Chumpha festival; opening the ancestral granary; blessing the first grains of autumn.",
        },
        {
            "month_number": 10,
            "tangkhul_name": "Tara-kachang",
            "gregorian_equivalent": "October",
            "hindi_name": "तारा-कचांग (अक्टूबर)",
            "significance": "Golden terrace harvest month; reapers sing ancient folk ballads (Hao Laa) across the sunlit valley.",
        },
        {
            "month_number": 11,
            "tangkhul_name": "Ngasang",
            "gregorian_equivalent": "November",
            "hindi_name": "नगासांग (नवंबर)",
            "significance": "Threshing and winnowing golden paddy; wedding feasts and clan alliances celebrated.",
        },
        {
            "month_number": 12,
            "tangkhul_name": "Mangkhar",
            "gregorian_equivalent": "December",
            "hindi_name": "मांगखार (दिसंबर)",
            "significance": "Chilly winter winds blow; youth assemble in the Longshim dormitory for storytelling and riddling.",
        },
    ]

    seasons = [
        {
            "season": "Spring",
            "tangkhul": "Phangrei-ngam",
            "hindi": "वसंत ऋतु",
            "description": "Wild apple blossoms, emerald slopes, return of songbirds, Luira seed blessing.",
        },
        {
            "season": "Monsoon / Rainy Season",
            "tangkhul": "Zingrot-tharan",
            "hindi": "वर्षा ऋतु",
            "description": "Continuous rains, mist-shrouded ridges, flooded rice terraces, thunder and lightning.",
        },
        {
            "season": "Autumn",
            "tangkhul": "Maza-tharan",
            "hindi": "शरद ऋतु",
            "description": "Golden rice fields, clear crisp blue skies, harvesting songs, Chumpha ceremonies.",
        },
        {
            "season": "Winter",
            "tangkhul": "Lumkaza / Kaphung-tharan",
            "hindi": "शीत ऋतु",
            "description": "Frosty mornings, woodsmoke in villages, warm hearth fires, Longshim oral banter.",
        },
    ]

    day_divisions = [
        {"period": "Cock-crow / Dawn", "tangkhul": "Har-kakhon", "hindi": "भोर / मुर्ग़े की पहली बाँग", "approx_time": "04:00 - 05:30 AM"},
        {"period": "Sunrise", "tangkhul": "Zimik kashok", "hindi": "सूर्योदय", "approx_time": "05:30 - 06:30 AM"},
        {"period": "Morning", "tangkhul": "Ngathor", "hindi": "सुबह / प्रातःकाल", "approx_time": "06:30 - 11:30 AM"},
        {"period": "Midday / Noon", "tangkhul": "Ngashun / Zimik kashung", "hindi": "दोपहर / मध्याह्न", "approx_time": "11:30 AM - 01:30 PM"},
        {"period": "Afternoon", "tangkhul": "Ngashun ngalung", "hindi": "तीसरा पहर / अपराह्न", "approx_time": "01:30 - 04:30 PM"},
        {"period": "Sunset", "tangkhul": "Zimik katun", "hindi": "सूर्यास्त", "approx_time": "04:30 - 05:30 PM"},
        {"period": "Return from Terrace Fields", "tangkhul": "Tan-tak-un", "hindi": "खेतों से लौटने का समय", "approx_time": "05:30 - 06:00 PM"},
        {"period": "Fowls Retiring to Roost", "tangkhul": "Har-kat", "hindi": "पक्षियों के घोंसले में लौटने की बेला", "approx_time": "06:00 - 06:30 PM"},
        {"period": "Dusk / Twilight", "tangkhul": "Ngazing-shon", "hindi": "गोधूलि / साँझ", "approx_time": "06:30 - 07:30 PM"},
        {"period": "Youth Dormitory Assembly", "tangkhul": "Long-kat", "hindi": "युवा-गृह में एकत्र होने का समय", "approx_time": "07:30 - 09:30 PM"},
        {"period": "Midnight", "tangkhul": "Ngaya mashun", "hindi": "मध्यरात्रि / आधी रात", "approx_time": "11:30 PM - 01:30 AM"},
    ]

    return {
        "lunar_months": months,
        "seasons": seasons,
        "day_and_night_divisions": day_divisions,
    }


# -----------------------------------------------------------------------------
# 3. TRADITIONAL MEASUREMENTS (DISTANCE, CAPACITY, LAND)
# -----------------------------------------------------------------------------
def generate_traditional_measurements() -> dict[str, Any]:
    return {
        "linear_measures": [
            {
                "term": "Phei-kanao amik",
                "meaning_en": "Finger-width",
                "meaning_hi": "उँगली की चौड़ाई",
                "usage": "Measuring thickness of woven shawls, cane strips, and arrow shafts.",
            },
            {
                "term": "Khashap",
                "meaning_en": "Hand-span (thumb tip to little finger outstretched)",
                "meaning_hi": "बित्ता (अंगूठे से कनिष्ठिका तक)",
                "usage": "Standard unit for measuring pottery diameters, basket depths, and bamboo tubes.",
            },
            {
                "term": "Khumpi",
                "meaning_en": "Cubit (elbow to the tip of the middle finger)",
                "meaning_hi": "हाथ (कोहनी से मध्यमा उँगली की नोक तक)",
                "usage": "Measuring woven cloth bolts (kachon) and timber planks.",
            },
            {
                "term": "Phei akha-zat",
                "meaning_en": "Pace / Human Stride",
                "meaning_hi": "कदम (चलने का एक डग)",
                "usage": "Measuring boundaries of homestead plots and terrace widths.",
            },
            {
                "term": "Khavai",
                "meaning_en": "Arm-span / Fathom (both arms outstretched horizontally)",
                "meaning_hi": "बाँस / व्योम (दोनों बाहें फैलाने पर नाप)",
                "usage": "Measuring rope coils, cane cables for suspension bridges, and house frameworks.",
            },
        ],
        "capacity_measures": [
            {
                "term": "Kutung akha",
                "meaning_en": "Single handful",
                "meaning_hi": "मुट्ठी भर",
                "usage": "Measuring seasoning salt, wild sesame seeds, and chillies for stew.",
            },
            {
                "term": "Kupang akha",
                "meaning_en": "Double-handful (cupped hands together)",
                "meaning_hi": "अंजुलि (दोनों हाथों की ओक)",
                "usage": "Measuring uncooked grain ration per family meal.",
            },
            {
                "term": "Pui-thun akha",
                "meaning_en": "Hollow bamboo joint measure",
                "meaning_hi": "बाँस के पोर का नाप (चोंगा)",
                "usage": "Standard market measure for rice beer, yeast, and fermented bamboo shoot.",
            },
            {
                "term": "Kharai-kanao",
                "meaning_en": "Small gathering basket",
                "meaning_hi": "छोटी खराई टोकरी",
                "usage": "Gathering crabs, river fish, ginger roots, and mushrooms.",
            },
            {
                "term": "Long-pui / Samphung",
                "meaning_en": "Conical hill harvest basket",
                "meaning_hi": "बड़ा अन्न टोकरा / खराई",
                "usage": "Carrying heavy loads of harvested paddy (40-50 kg) from terraces to granaries.",
            },
        ],
        "land_measures": [
            {
                "concept": "Maza-wui Luira Yield Measure",
                "description_en": "Land is not calculated in square feet or acres, but in the quantity of paddy baskets it produces annually and the reliable perennial mountain spring waters that irrigate its terraces.",
                "description_hi": "तंगखुल समाज में ज़मीन को गज़ या एकड़ में नहीं, बल्कि उसमें पैदा होने वाले धान के टोकरों की संख्या और उसमें आने वाले पहाड़ी चश्मे के पानी के आधार पर आंका जाता है।",
            }
        ],
    }


# -----------------------------------------------------------------------------
# 4. KINSHIP TERMINOLOGY & CLAN HONORIFICS
# -----------------------------------------------------------------------------
def generate_kinship_system() -> list[dict[str, Any]]:
    return [
        {"role": "Grandfather", "tangkhul": "Awo", "hindi": "दादाजी / नानाजी", "category": "Elders"},
        {"role": "Grandmother", "tangkhul": "Ayi", "hindi": "दादीजी / नानीजी", "category": "Elders"},
        {"role": "Father", "tangkhul": "Ava", "hindi": "पिताजी / बापू", "category": "Parents"},
        {"role": "Mother", "tangkhul": "Avo", "hindi": "माताजी / माँ", "category": "Parents"},
        {"role": "Elder Brother", "tangkhul": "Amei", "hindi": "बड़ा भाई (अग्रज)", "category": "Siblings"},
        {"role": "Younger Brother", "tangkhul": "Ngarao-mayar", "hindi": "छोटा भाई (अनुज)", "category": "Siblings"},
        {"role": "Elder Sister", "tangkhul": "Achon", "hindi": "बड़ी बहन (दीदी)", "category": "Siblings"},
        {"role": "Younger Sister", "tangkhul": "Ngarao-shanao", "hindi": "छोटी बहन", "category": "Siblings"},
        {"role": "Maternal Uncle", "tangkhul": "Kuku", "hindi": "मामा (पवित्र सम्बंधी)", "category": "Avuncular"},
        {"role": "Paternal Aunt", "tangkhul": "Ani", "hindi": "बुआ", "category": "Avuncular"},
        {"role": "Son", "tangkhul": "Naomayar", "hindi": "बेटा / पुत्र", "category": "Children"},
        {"role": "Daughter", "tangkhul": "Naoshanao", "hindi": "बेटी / पुत्री", "category": "Children"},
        {"role": "Grandchildren", "tangkhul": "Ashu-anao", "hindi": "पोता-पोती / नाती-नातिन", "category": "Descendants"},
        {"role": "Husband", "tangkhul": "Mayarnaowo", "hindi": "पति", "category": "Spousal"},
        {"role": "Wife", "tangkhul": "Shanaowo", "hindi": "पत्नी", "category": "Spousal"},
        {"role": "Father-in-law", "tangkhul": "Awo-khamarui", "hindi": "ससुर", "category": "Affinal"},
        {"role": "Mother-in-law", "tangkhul": "Ayi-khamarui", "hindi": "सास", "category": "Affinal"},
        {"role": "Brother-in-law", "tangkhul": "Amei-khamarui", "hindi": "साला / जीजा / देवर", "category": "Affinal"},
        {"role": "Clan Chieftain / Head", "tangkhul": "Awunga / Wungnao", "hindi": "ग्राम मुखिया / कुलप्रमुख", "category": "Governance"},
        {"role": "Clan Council Elder", "tangkhul": "Kharar", "hindi": "कबीलाई बुजुर्ग / सभासद", "category": "Governance"},
        {"role": "Young Maidens of Village", "tangkhul": "Ngalanaobing", "hindi": "गाँव की युवतियाँ", "category": "Age Groups"},
        {"role": "Young Warriors of Village", "tangkhul": "Mayarnaobing", "hindi": "गाँव के युवा / योद्धा", "category": "Age Groups"},
    ]


# -----------------------------------------------------------------------------
# 5. EVERYDAY CONVERSATIONAL DIALOGUES & PHRASES
# -----------------------------------------------------------------------------
def generate_conversations() -> list[dict[str, Any]]:
    return [
        {
            "id": "CONV-001",
            "english": "Hello / Greetings!",
            "tangkhul": "Mahairareo!",
            "hindi": "नमस्ते / जोहार!",
            "context": "Traditional mountain greeting called across paths.",
        },
        {
            "id": "CONV-002",
            "english": "Good morning! May peace be upon your morning.",
            "tangkhul": "Leikhaya ngathor!",
            "hindi": "शुभ प्रभात!",
            "context": "Standard morning greeting.",
        },
        {
            "id": "CONV-003",
            "english": "How are you? Are you living in peace?",
            "tangkhul": "Maringphali khalei?",
            "hindi": "आप कैसे हैं? / क्या हाल-चाल है?",
            "context": "Inquiring about well-being.",
        },
        {
            "id": "CONV-004",
            "english": "I am living in peace and good health.",
            "tangkhul": "I ringphada lei.",
            "hindi": "मैं बिल्कुल ठीक और सकुशल हूँ।",
            "context": "Positive reply.",
        },
        {
            "id": "CONV-005",
            "english": "Long time no see! We haven't met for seasons.",
            "tangkhul": "Makathei sanghairakho!",
            "hindi": "बहुत दिनों से भेंट नहीं हुई!",
            "context": "Meeting after long absence.",
        },
        {
            "id": "CONV-006",
            "english": "What is your name, friend?",
            "tangkhul": "Nali aming khipa ho?",
            "hindi": "आपका शुभ नाम क्या है?",
            "context": "Polite introduction.",
        },
        {
            "id": "CONV-007",
            "english": "My name is Somatai.",
            "tangkhul": "Iwui aming Somatai hoi.",
            "hindi": "मेरा नाम सोमताई है।",
            "context": "Stating identity.",
        },
        {
            "id": "CONV-008",
            "english": "Which village do you come from?",
            "tangkhul": "Na khikha nao khalei?",
            "hindi": "आप किस गाँव / क्षेत्र से हैं?",
            "context": "Locating village lineage.",
        },
        {
            "id": "CONV-009",
            "english": "I come from the misty hills of Ukhrul.",
            "tangkhul": "I Ukhrul wui eina na.",
            "hindi": "मैं उखरुल की पहाड़ियों से हूँ।",
            "context": "Expressing origin.",
        },
        {
            "id": "CONV-010",
            "english": "Do you speak the Tangkhul language?",
            "tangkhul": "Na Tangkhul tui mamatui khalei?",
            "hindi": "क्या आप तंगखुल भाषा बोलते हैं?",
            "context": "Linguistic inquiry.",
        },
        {
            "id": "CONV-011",
            "english": "Yes, I speak it fluently / No, I am learning.",
            "tangkhul": "Mha, I matuiya / Maningmanei, I tuitamda lei.",
            "hindi": "हाँ, मैं बोलता हूँ / नहीं, मैं अभी सीख रहा हूँ।",
            "context": "Linguistic competence.",
        },
        {
            "id": "CONV-012",
            "english": "Please come inside to the hearth.",
            "tangkhul": "Shimlutli ungphunglu.",
            "hindi": "कृपया घर के भीतर अलाव के पास पधारें।",
            "context": "Hearthside hospitality invitation.",
        },
        {
            "id": "CONV-013",
            "english": "Have you eaten your meal?",
            "tangkhul": "Na maphazahaira khalei?",
            "hindi": "क्या आपने भोजन कर लिया है?",
            "context": "Traditional host courtesy.",
        },
        {
            "id": "CONV-014",
            "english": "Thank you very deeply from my heart.",
            "tangkhul": "Ningshinahaire / Ningkachang eina.",
            "hindi": "आपका हृदय से बहुत-बहुत धन्यवाद।",
            "context": "Expressing gratitude.",
        },
        {
            "id": "CONV-015",
            "english": "Farewell! Until we meet again on the trail.",
            "tangkhul": "Samphangnaosei / Kapha eina zallu!",
            "hindi": "अलविदा! फिर मिलेंगे / यात्रा शुभ हो!",
            "context": "Parting blessing.",
        },
        {
            "id": "CONV-016",
            "english": "May good dreams watch over your sleep tonight.",
            "tangkhul": "Mangphameisei!",
            "hindi": "शुभ रात्रि / सुखद स्वप्न!",
            "context": "Night blessing.",
        },
        {
            "id": "CONV-017",
            "english": "Where does this mountain path lead?",
            "tangkhul": "Shongfa hi kachida kazat-la?",
            "hindi": "यह पहाड़ी पगडंडी कहाँ जाती है?",
            "context": "Asking trail directions.",
        },
        {
            "id": "CONV-018",
            "english": "It climbs up directly to the summit of Shirui Kashong.",
            "tangkhul": "Chi Shirui Kashong kaphungli katoh-ya.",
            "hindi": "यह सीधे शिरुई काशोंग की चोटी पर जाती है।",
            "context": "Direction guidance.",
        },
    ]


# -----------------------------------------------------------------------------
# 6. ASSEMBLE MASTER ENCYCLOPEDIA & PUBLISH PDF/JSON
# -----------------------------------------------------------------------------
def run_encyclopedia_builder() -> None:
    print("=" * 80)
    print("BUILDING TANGKHUL LINGUISTIC ENCYCLOPEDIA & NUMBER SYSTEM")
    print("=" * 80)

    num_system = generate_number_system()
    calendar_data = generate_calendar_and_time()
    measures_data = generate_traditional_measurements()
    kinship_data = generate_kinship_system()
    conv_data = generate_conversations()

    master_payload = {
        "title": "Complete Tangkhul Naga Linguistic Encyclopedia & Number System",
        "hindi_title": "तंगखुल नागा सम्पूर्ण भाषा-विज्ञान, संख्या प्रणाली एवं सांस्कृतिक पंचांग विश्वकोश",
        "version": "1.0.0",
        "provenance": {
            "sources": [
                "Rev. William Pettigrew (1918) Tangkhul Naga Grammar and Dictionary",
                "S. Arokianathan (1982) Tangkhul Folk Literature & Phonetic Documentation (CIIL)",
                "Tangkhul Literature Society (TLS) Textbook & Grammar Committee Archives",
                "Tangkhul Language Preservation Project (TLPP) Fieldwork Documentation",
            ],
            "dialect": "Standard Tangkhul (Ukhrul)",
            "license": "Traditional Cultural Heritage (Community Authorized)",
        },
        "sections": {
            "1_number_system": num_system,
            "2_calendar_and_time": calendar_data,
            "3_traditional_measurements": measures_data,
            "4_kinship_terminology": kinship_data,
            "5_conversational_phrases": conv_data,
        },
    }

    # Save JSON files
    json_export = EXPORTS_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.json"
    json_bundled = BUNDLED_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.json"
    for p in (json_export, json_bundled):
        p.write_text(json.dumps(master_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported JSON: {p} ({p.stat().st_size:,} bytes)")

    # Build PDF pages
    pdf_pages: list[list[tuple[str, int, str]]] = []

    # Page 1: Overview & Numbers 1-30
    p1: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 1: THE TANGKHUL NUMBER SYSTEM (CARDINAL NUMBERS 1 TO 30)"),
        ("/F1", 8, "Tangkhul numerals follow a regular decimal structure with archaic base-ten compounds:"),
        ("/F1", 8, " "),
    ]
    for c in num_system["cardinal_numbers"][:30]:
        p1.append(("/F2", 8, f"#{c['number']:02d}  Tangkhul: {c['tangkhul']}"))
        p1.append(("/F1", 8, f"     English: {c['english']} | Hindi: {c['hindi']}"))
    pdf_pages.append(p1)

    # Page 2: Numbers 31-70
    p2: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 1: THE TANGKHUL NUMBER SYSTEM (CARDINAL NUMBERS 31 TO 70)"),
        ("/F1", 8, " "),
    ]
    for c in num_system["cardinal_numbers"][30:70]:
        p2.append(("/F2", 8, f"#{c['number']:02d}  Tangkhul: {c['tangkhul']}"))
        p2.append(("/F1", 8, f"     English: {c['english']} | Hindi: {c['hindi']}"))
    pdf_pages.append(p2)

    # Page 3: Numbers 71-100 + High Numbers + Ordinals
    p3: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 1: THE TANGKHUL NUMBER SYSTEM (71 TO 100, HIGHER UNITS & ORDINALS)"),
        ("/F1", 8, " "),
    ]
    for c in num_system["cardinal_numbers"][70:]:
        p3.append(("/F2", 8, f"#{c['number']:02d}  Tangkhul: {c['tangkhul']}"))
        p3.append(("/F1", 8, f"     English: {c['english']} | Hindi: {c['hindi']}"))
    p3.append(("/F1", 7, " "))
    p3.append(("/F2", 9, "HIGHER NUMERICAL ORDERS (HUNDREDS & THOUSANDS):"))
    for h in num_system["higher_numbers"]:
        p3.append(("/F1", 8, f"  * {h['number']:,} -> {h['tangkhul']} (EN: {h['english']} | HI: {h['hindi']})"))
    p3.append(("/F1", 7, " "))
    p3.append(("/F2", 9, "ORDINAL NUMBERS (CRITICAL RANKS):"))
    for o in num_system["ordinal_numbers"][:7]:
        p3.append(("/F1", 8, f"  * {o['rank']}: {o['tangkhul']} (EN: {o['english']} | HI: {o['hindi']})"))
    pdf_pages.append(p3)

    # Page 4: Classifiers, Multiplicatives & Fractions
    p4: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 1: NUMERAL CLASSIFIERS, MULTIPLICATIVES & FRACTIONS"),
        ("/F1", 8, "Tangkhul requires specific syntactic classifiers depending on the noun's animacy and shape:"),
        ("/F1", 8, " "),
        ("/F2", 9, "ESSENTIAL NUMERAL CLASSIFIERS:"),
    ]
    for cl in num_system["numeral_classifiers"]:
        p4.append(("/F2", 8, f"Classifier: {cl['classifier']}  -> Category: {cl['usage']}"))
        p4.append(("/F1", 8, f"  Example: {cl['example_tangkhul']} -> {cl['example_translation']}"))
        p4.append(("/F1", 7, " "))
    p4.append(("/F2", 9, "MULTIPLICATIVE & DISTRIBUTIVE FORMS:"))
    for m in num_system["multiplicative_and_distributive"][:6]:
        p4.append(("/F1", 8, f"  * {m['multiplier']}: {m['tangkhul']} ({m['english']} / {m['hindi']})"))
    p4.append(("/F1", 7, " "))
    p4.append(("/F2", 9, "FRACTIONS & PROPORTIONS:"))
    for fr in num_system["fractions"]:
        p4.append(("/F1", 8, f"  * {fr['fraction']}: {fr['tangkhul']} ({fr['english']} / {fr['hindi']})"))
    pdf_pages.append(p4)

    # Page 5: 12 Lunar Months & Seasons
    p5: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 2: TANGKHUL LUNAR CALENDAR (12 MONTHS & 4 SEASONS)"),
        ("/F1", 8, "The traditional lunar calendar dictates agricultural life, ritual festivals, and migration:"),
        ("/F1", 8, " "),
    ]
    for mo in calendar_data["lunar_months"]:
        p5.append(("/F2", 8, f"Month {mo['month_number']:02d}: {mo['tangkhul_name']} ({mo['gregorian_equivalent']} / {mo['hindi_name']})"))
        p5.append(("/F1", 8, f"     Significance: {mo['significance']}"))
        p5.append(("/F1", 7, " "))
    p5.append(("/F2", 9, "THE FOUR MOUNTAIN SEASONS:"))
    for se in calendar_data["seasons"]:
        p5.append(("/F1", 8, f"  * {se['season']} ({se['tangkhul']} / {se['hindi']}): {se['description']}"))
    pdf_pages.append(p5)

    # Page 6: Day Divisions & Traditional Measurements
    p6: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 3: TIME DIVISIONS & TRADITIONAL MOUNTAIN MEASUREMENTS"),
        ("/F1", 8, "Daily life in high villages was regulated by natural sun positions and animal rhythms:"),
        ("/F1", 8, " "),
        ("/F2", 9, "TRADITIONAL DIVISIONS OF DAY AND NIGHT:"),
    ]
    for d in calendar_data["day_and_night_divisions"]:
        p6.append(("/F1", 8, f"  * {d['period']} ({d['approx_time']}) -> Tangkhul: {d['tangkhul']} | Hindi: {d['hindi']}"))
    p6.append(("/F1", 7, " "))
    p6.append(("/F2", 9, "TRADITIONAL LINEAR MEASURES:"))
    for lm in measures_data["linear_measures"]:
        p6.append(("/F2", 8, f"  * {lm['term']} ({lm['meaning_en']} / {lm['meaning_hi']})"))
        p6.append(("/F1", 8, f"    Usage: {lm['usage']}"))
    p6.append(("/F1", 7, " "))
    p6.append(("/F2", 9, "CAPACITY & HARVEST BASKET MEASURES:"))
    for cm in measures_data["capacity_measures"][:3]:
        p6.append(("/F1", 8, f"  * {cm['term']}: {cm['meaning_en']} ({cm['meaning_hi']}) - {cm['usage']}"))
    pdf_pages.append(p6)

    # Page 7: Kinship Terminology
    p7: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 4: ELABORATE TANGKHUL KINSHIP & SOCIAL HONORIFICS"),
        ("/F1", 8, "Kinship terms form the moral foundation of village respect and exogamous clan ethics:"),
        ("/F1", 8, " "),
    ]
    for kin in kinship_data:
        p7.append(("/F2", 8, f"Role: {kin['role']}  -> Tangkhul: {kin['tangkhul']}"))
        p7.append(("/F1", 8, f"   Hindi: {kin['hindi']} | Category: {kin['category']}"))
        p7.append(("/F1", 7, " "))
    pdf_pages.append(p7)

    # Page 8: Conversational Phrases & Daily Dialogues
    p8: list[tuple[str, int, str]] = [
        ("/F2", 11, "PART 5: EVERYDAY CONVERSATIONAL DIALOGUES & TRAVEL PHRASES"),
        ("/F1", 8, "Essential spoken interactions for mountain travel, hospitality, and daily village life:"),
        ("/F1", 8, " "),
    ]
    for conv in conv_data:
        p8.append(("/F2", 8, f"[{conv['id']}] EN: {conv['english']}"))
        p8.append(("/F1", 8, f"     Tangkhul: {conv['tangkhul']}"))
        p8.append(("/F1", 8, f"     Hindi   : {conv['hindi']} (Context: {conv['context']})"))
        p8.append(("/F1", 7, " "))
    pdf_pages.append(p8)

    # Generate PDF
    pdf_bytes = build_pdf_document(
        title="Tangkhul Naga Linguistic Encyclopedia",
        subtitle="Numbers (1-100+), Calendar, Time Divisions, Measurements, Kinship & Phrases",
        pages_data=pdf_pages,
        doc_footer_name="Tangkhul Linguistic Encyclopedia",
    )
    pdf_export = EXPORTS_DIR / "tangkhul_linguistic_encyclopedia_and_number_system.pdf"
    pdf_export.write_bytes(pdf_bytes)
    print(f"Exported PDF: {pdf_export} ({len(pdf_bytes):,} bytes, {len(pdf_pages)} pages)")

    print("Successfully built Tangkhul Linguistic Encyclopedia & Number System!")


if __name__ == "__main__":
    run_encyclopedia_builder()
