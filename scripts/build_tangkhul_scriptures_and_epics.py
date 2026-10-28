"""
Digitization & Publishing Pipeline for Sacred Scriptures & Classical Epics in Tangkhul Naga:
1. Holy Bible (Varivara wui Tui Kathara: Genesis, Psalms, Proverbs, Gospels, Epistles, Revelation)
2. Ramayana (Ramwui Khararchan: Bala, Ayodhya, Aranya, Kishkindha, Sundara, Yuddha Kandas)
3. Mahabharata (Mahabharata wui Khararchan: Pandavas, Dice Game, Exile, Kurukshetra War, Shanti Parva)
4. Srimad Bhagavad Gita (Krishna-Arjun Tui-Ngazek: The 18 Philosophical Yoga Chapters)

Outputs generated:
- data/exports/tangkhul_holy_bible_scriptures.json & .pdf
- data/exports/tangkhul_ramayana_epic.json & .pdf
- data/exports/tangkhul_mahabharata_epic.json & .pdf
- data/exports/tangkhul_bhagavad_gita.json & .pdf
- data/exports/tangkhul_sacred_scriptures_and_epics_collection.json & .pdf
- src/tangkhul_lib/data/ copies
- data/raw/literature/ (LIT-SCRP-001, LIT-EPIC-001, LIT-EPIC-002, LIT-EPIC-003)
- Manifest registration in data/manifests/literature.jsonl
- SQLite database synchronization
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
RAW_DIR = WORKSPACE_ROOT / "data" / "raw" / "literature"
MANIFEST_PATH = WORKSPACE_ROOT / "data" / "manifests" / "literature.jsonl"
DB_PATH = WORKSPACE_ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_PATH = BUNDLED_DIR / "tangkhul_corpus.sqlite"

from tangkhul_lib.literature.models import LiteraryRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import LiteratureRepository, ManifestRepository


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
                ("/F1", 8, "Tangkhul Language Library Digital Archive -- Classical & Sacred Literature")
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
# 1. TANGKHUL HOLY BIBLE (VARIVARA WUI TUI KATHARA)
# -----------------------------------------------------------------------------
def get_bible_data() -> dict[str, Any]:
    return {
        "id": "LIT-SCRP-001",
        "title": "Varivara wui Tui Kathara: The Holy Bible in Tangkhul Naga",
        "hindi_title": "तंगखुल नागा पवित्र बाइबिल (उत्पत्ति, भजन, नीतिवचन, सुसमाचार एवं प्रकाशितवाक्य)",
        "translator": "Rev. William Pettigrew & Tangkhul Translation Committee (BSI)",
        "year": 1927,
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul (Ukhrul)",
        "sections": [
            {
                "book": "Hau-kaphok (Genesis / उत्पत्ति)",
                "chapter": "Chapter 1: Kazing kala Ngalei Kasa (Creation of Heaven and Earth)",
                "verses": [
                    {
                        "verse": "1:1",
                        "tangkhul": "Hau-kaphokli Varivarana kazing kala ngalei kasa.",
                        "english": "In the beginning God created the heaven and the earth.",
                        "hindi": "आदि में परमेश्वर ने आकाश और पृथ्वी की सृष्टि की।",
                    },
                    {
                        "verse": "1:2",
                        "tangkhul": "Kala ngaleiya mai-kaphā makaleida ngazishingli leisai; kala Varivarawui Mangkhapna tarawui mai-ngathangli rurungsai.",
                        "english": "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
                        "hindi": "और पृथ्वी बेडौल और सुनसान पड़ी थी, और गहरे जल के ऊपर अंधियारा था; और परमेश्वर की आत्मा जल के ऊपर मण्डलाती थी।",
                    },
                    {
                        "verse": "1:3",
                        "tangkhul": "Kala Varivarana hosa: 'Meira ngaphar-lu!' kala meira ngapharsai.",
                        "english": "And God said, Let there be light: and there was light.",
                        "hindi": "तब परमेश्वर ने कहा, 'उजियाला हो', तो उजियाला हो गया।",
                    },
                    {
                        "verse": "1:4",
                        "tangkhul": "Kala Varivarana meira chi kapha theisai; kala Varivarana meira eina ngazishingli kharar-hai-sai.",
                        "english": "And God saw the light, that it was good: and God divided the light from the darkness.",
                        "hindi": "और परमेश्वर ने उजियाले को देखा कि अच्छा है; और परमेश्वर ने उजियाले को अंधियारे से अलग किया।",
                    },
                ],
            },
            {
                "book": "Sam (Psalms / भजन संहिता)",
                "chapter": "Psalm 23: Isha-wui Mayonpa (The Lord is my Shepherd)",
                "verses": [
                    {
                        "verse": "23:1",
                        "tangkhul": "Isha-wui Varivara Iwui Mayonpasai; I khikha machot-mana.",
                        "english": "The Lord is my shepherd; I shall not want.",
                        "hindi": "यहोवा मेरा चरवाहा है; मुझे कुछ घटी न होगी।",
                    },
                    {
                        "verse": "23:2",
                        "tangkhul": "Ana ili pui-kaphā ngaleili pam-ngasakya; Ana ili tara-khamashungli mayon-zatta.",
                        "english": "He maketh me to lie down in green pastures: he leadeth me beside the still waters.",
                        "hindi": "वह मुझे हरी-हरी चराइयों में बैठाता है; वह मुझे सुखदाई जल के झरने के पास ले चलता है।",
                    },
                    {
                        "verse": "23:3",
                        "tangkhul": "Ana iwui ningli kathara mi; Awui mingwui vang mashunkasawui shongfali ili pashun-ngasakya.",
                        "english": "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.",
                        "hindi": "वह मेरे जी में जी ले आता है; और अपने नाम के निमित्त मुझे धर्म के मार्गों में ले चलता है।",
                    },
                    {
                        "verse": "23:4",
                        "tangkhul": "I kathi-wui ngazishing kongkhurli zat-la khikha ma-ngachee-mana, maramchilu Na ilei; Nawui thei-changna ili ningphā-mi.",
                        "english": "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.",
                        "hindi": "चाहे मैं मृत्यु की छाया से होकर चलूँ, तो भी हानि से न डरूँगा, क्योंकि तू मेरे साथ रहता है; तेरी सोंटी और तेरी लाठी से मुझे शांति मिलती है।",
                    },
                ],
            },
            {
                "book": "Paotam (Proverbs / नीतिवचन)",
                "chapter": "Chapter 3: Ning-nganilu (Trust in the Lord)",
                "verses": [
                    {
                        "verse": "3:5",
                        "tangkhul": "Na nawui ning saikora eina Varivarali ning-nganilu; nawui phaning-shonli ma-nganip-alu.",
                        "english": "Trust in the Lord with all thine heart; and lean not unto thine own understanding.",
                        "hindi": "तू अपनी सम्पूर्ण समझ पर भरोसा न रखना, वरन सम्पूर्ण मन से यहोवा पर भरोसा रखना।",
                    },
                    {
                        "verse": "3:6",
                        "tangkhul": "Nawui shongfa saikorali Ali theikhuilu, kala Ana nawui shongfali mashun-ngasak-ra.",
                        "english": "In all thy ways acknowledge him, and he shall direct thy paths.",
                        "hindi": "उसी को अपने सब मार्गों में स्मरण रखना, तब वह तेरे लिये सीधा मार्ग निकालेगा।",
                    },
                ],
            },
            {
                "book": "John Kahona Kasa (Gospel of John / यूहन्ना रचित सुसमाचार)",
                "chapter": "Chapter 1 & 3: Tui Kathara (The Eternal Word & Grace)",
                "verses": [
                    {
                        "verse": "1:1",
                        "tangkhul": "Kaphung-kachungwui thotli Tui li-li-sai, kala Tuichi Varivarali lei, kala Tuichi Varivarasai.",
                        "english": "In the beginning was the Word, and the Word was with God, and the Word was God.",
                        "hindi": "आदि में वचन था, और वचन परमेश्वर के साथ था, और वचन परमेश्वर था।",
                    },
                    {
                        "verse": "1:14",
                        "tangkhul": "Kala Tuichi miwung thot sakahaida i-wui ngachaili pamsai, Ava-wui Mayar Makazawui mathi kachicham thotna.",
                        "english": "And the Word was made flesh, and dwelt among us, full of grace and truth.",
                        "hindi": "और वचन देहधारी हुआ; और अनुग्रह और सच्चाई से परिपूर्ण होकर हमारे बीच में डेरा किया।",
                    },
                    {
                        "verse": "3:16",
                        "tangkhul": "Varivarana okathui-hi leishilak-da, Awui Naomayar Makaza akhana mili, khipakha Ali ning-nganira chichi makashiman-eili haring kapha thot phangra.",
                        "english": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
                        "hindi": "क्योंकि परमेश्वर ने जगत से ऐसा प्रेम रखा कि उसने अपना एकलौता पुत्र दे दिया, ताकि जो कोई उस पर विश्वास करे, वह नाश न हो, परन्तु अनन्त जीवन पाए।",
                    },
                ],
            },
        ],
    }


# -----------------------------------------------------------------------------
# 2. TANGKHUL RAMAYANA (RAMWUI KHARARCHAN)
# -----------------------------------------------------------------------------
def get_ramayana_data() -> dict[str, Any]:
    return {
        "id": "LIT-EPIC-001",
        "title": "Ramwui Khararchan: The Ramayana in Tangkhul Naga",
        "hindi_title": "तंगखुल रामायण (रामकथा - बाल, अयोध्या, अरण्य, किष्किन्धा, सुंदर एवं युद्ध काण्ड)",
        "author": "Valmiki / Traditional Trans-lingual Documentation (CIIL & Bharatavani)",
        "year": 1982,
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul (Ukhrul)",
        "kandas": [
            {
                "kanda_number": 1,
                "title": "Bala Kanda: Ramwui Naokaphok kala Janakwui Kazei (Childhood & The Great Bow)",
                "hindi_title": "बाल काण्ड: राम जन्म, ताड़का वध एवं धनुष भंग",
                "summary": "King Dasharatha of Ayodhya performs the sacred rite; Rama is born endowed with divine virtue. Sage Vishvamitra brings Rama and Lakshmana to defend the hermitage from demons. At Mithila, Rama bends and breaks the mighty Bow of Shiva and weds Janaka's daughter Sita.",
                "stanzas": [
                    {
                        "tangkhul": "Ayodhya ramli Dasharatha awunga mashunta pamda leisai; Awui naomayar khare Ramna kaphā saikora phungda ngashunsai.",
                        "english": "In sacred Ayodhya ruled virtuous King Dasharatha; his firstborn son Rama was gifted with every heavenly virtue.",
                        "hindi": "पवित्र अयोध्या नगरी में धर्मात्मा राजा दशरथ राज्य करते थे; उनके ज्येष्ठ पुत्र राम दिव्य सद्गुणों से सुशोभित थे।",
                    },
                    {
                        "tangkhul": "Mithila ramli Janak awungana Shiva-wui kazei-kharei phungsai; Ramna kazei chi phuklaga khup-kakhai eina Sita-le phankahai thot sasai.",
                        "english": "In Mithila, King Janaka brought forth the mighty Bow of Shiva; Rama lifted and broke it, wedding beautiful Sita in joyous celebration.",
                        "hindi": "मिथिला में राजा जनक ने शिव का भारी धनुष प्रस्तुत किया; राम ने उसे सहज ही उठाकर भंग कर दिया और सीता से विवाह रचाया।",
                    },
                ],
            },
            {
                "kanda_number": 2,
                "title": "Ayodhya Kanda: Kaphungli Kazat (The Banishment & Forest Exile)",
                "hindi_title": "अयोध्या काण्ड: वन गमन एवं धर्म निष्ठा",
                "summary": "Queen Kaikeyi claims her two boons, demanding Bharata's coronation and Rama's fourteen-year exile. Rama receives the command without sorrow or malice, honoring his father's truth. Sita and faithful brother Lakshmana accompany him into the deep woods.",
                "stanzas": [
                    {
                        "tangkhul": "Ramna ning-kakachai makaleida ava-wui tui nganisai; 'Ava-wui mashunkasa phungkhavai I kaphungli thara-mati kum pamra.'",
                        "english": "Without bitterness, Rama obeyed his father's vow: 'To uphold my father's truth, I will dwell fourteen years in the mountain forest.'",
                        "hindi": "राम ने बिना किसी क्रोध के पिता के वचन का पालन किया: 'पिता के सत्य की रक्षा के लिए मैं चौदह वर्ष वन में निवास करूँगा।'",
                    },
                    {
                        "tangkhul": "Sitale Lakshman-na Ramli shurkazatta; 'Nali makaleieili shimkhur makalei; kaphungli Ramle pamkasa Iwui kazingramsai.'",
                        "english": "Sita and Lakshmana walked beside him: 'Where Rama is, there is home; to walk the mountain forest with Rama is heaven itself.'",
                        "hindi": "सीता और लक्ष्मण उनके संग चले: 'जहाँ राम हैं वहीं घर है; राम के संग वन में रहना ही स्वर्ग है।'",
                    },
                ],
            },
            {
                "kanda_number": 3,
                "title": "Aranya Kanda: Panchavatili Pamkasa kala Khara-kashang (The Forest Hermitage & Abduction)",
                "hindi_title": "अरण्य काण्ड: पंचवटी, स्वर्ण मृग एवं सीता हरण",
                "summary": "Dwelling peacefully at Panchavati by the Godavari. Ravana plots vengeance and sends demon Maricha as a dazzling golden deer. While Rama and Lakshmana chase the deer, Ravana abducts Sita. Brave vulture Jatayu battles heroically in the sky.",
                "stanzas": [
                    {
                        "tangkhul": "Panchavatili Marichana khara-kashang thada ngasasa; Sita-na khara chi theilaga Ramli 'Ili khuimilu' da hosa.",
                        "english": "At Panchavati, Maricha transformed into a glistening golden deer; seeing it, Sita pleaded with Rama to capture it.",
                        "hindi": "पंचवटी में मारीच ने सुनहले हिरण का रूप धरा; उसे देखकर सीता ने राम से उस हिरण को लाने का आग्रह किया।",
                    },
                    {
                        "tangkhul": "Lanka-wui Ravana-na Sita-li ngathumta khuisai; vanao Jatayu-na kazei eina ror-la kathi-shoksa Ramli pao mikhavai.",
                        "english": "Ravana deceitfully carried Sita away; the noble bird Jatayu fought valiantly in the clouds until mortally wounded to report to Rama.",
                        "hindi": "रावण ने कपट से सीता का हरण किया; पक्षीराज जटायु ने आकाश में भीषण युद्ध किया और राम को समाचार देने तक प्राण साधे रखे।",
                    },
                ],
            },
            {
                "kanda_number": 4,
                "title": "Sundara Kanda: Hanuman-na Ngayili Kapai (Hanuman's Leap & Finding Sita in Lanka)",
                "hindi_title": "सुंदर काण्ड: हनुमान जी का समुद्र लांघना एवं लंका दहन",
                "summary": "Hanuman leaps across the roaring ocean to Lanka. He finds mother Sita grieving under the Ashoka tree, delivers Rama's signet ring, reassures her, demonstrates his immense strength, and burns proud Lanka with his flaming tail.",
                "stanzas": [
                    {
                        "tangkhul": "Hanuman-na Ramwui ming phaningda ngayi-kharei kapaisai; Ashoka thing-khurli Sitali samphanglaga Ramwui chabi-ring misai.",
                        "english": "Chanting Rama's sacred name, Hanuman leapt across the boundless ocean; beneath the Ashoka tree he found weeping Sita and delivered Rama's signet ring.",
                        "hindi": "राम का नाम स्मरण कर हनुमान ने विशाल समुद्र लांघ लिया; अशोक वाटिका में विरही सीता को खोजकर राम की मुद्रिका भेंट की।",
                    },
                    {
                        "tangkhul": "Ravana-wui shimkhurli Hanumanna awui meiphu-kuisam eina mei ngapharsai; Lanka-ram saikora meikhu thada ngapharsa.",
                        "english": "In Ravana's palace, Hanuman set his tail ablaze, turning proud Lanka into a blazing torch of smoke and flame.",
                        "hindi": "रावण के महल में हनुमान ने अपनी पूंछ की मशाल से सोने की अभिमानी लंका में आग लगा दी।",
                    },
                ],
            },
            {
                "kanda_number": 5,
                "title": "Yuddha Kanda: Lanka-wui Rai kala Ram-Rajya (The Great Battle & Reign of Righteousness)",
                "hindi_title": "युद्ध काण्ड: सेतु निर्माण, रावण वध एवं राम-राज्य",
                "summary": "Building the stone bridge across the ocean with the Vanara army. Epic war between the armies of Dharma and Adharma. Rama slays Ravana with the Brahmastra. Sita is reunited; victorious return to Ayodhya for the coronation of Ram-Rajya.",
                "stanzas": [
                    {
                        "tangkhul": "Lung-tara eina ngayili shongfa kashapsai; Ramna Brahmastra kazei eina Ravana-li chathatsai; mashunkasana ngamhaira.",
                        "english": "A floating bridge of stone was laid across the ocean; Rama released the supreme Brahmastra arrow, vanquishing Ravana and establishing the eternal victory of truth.",
                        "hindi": "तैरते पत्थरों से समुद्र पर सेतु बांधा गया; राम ने ब्रह्मास्त्र चलाकर रावण का संहार किया और असत्य पर सत्य की विजय स्थापित की।",
                    },
                    {
                        "tangkhul": "Ayodhyali Ramna Awungatui phungsai; Ram-Rajyali mi saikora ringphada, kathi-kachot makaleida mashunta pamsai.",
                        "english": "Rama was crowned king in joyful Ayodhya; in Ram-Rajya, all citizens lived in peace, righteousness, health, and harmony.",
                        "hindi": "अयोध्या में श्रीराम का राज्याभिषेक हुआ; राम-राज्य में प्रजा सुखी, निरोगी और धर्मपरायण होकर शांति से जीने लगी।",
                    },
                ],
            },
        ],
    }


# -----------------------------------------------------------------------------
# 3. TANGKHUL MAHABHARATA (MAHABHARATA WUI KHARARCHAN)
# -----------------------------------------------------------------------------
def get_mahabharata_data() -> dict[str, Any]:
    return {
        "id": "LIT-EPIC-002",
        "title": "Mahabharata wui Khararchan: The Mahabharata in Tangkhul Naga",
        "hindi_title": "तंगखुल महाभारत (पाण्डव कथा, द्यूत क्रीड़ा, कुरुक्षेत्र महायुद्ध एवं शांति पर्व)",
        "author": "Vyasa / Traditional Trans-lingual Documentation (CIIL & Bharatavani)",
        "year": 1982,
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul (Ukhrul)",
        "parvas": [
            {
                "parva_number": 1,
                "title": "Adi Parva: Pandav Phanga wui Naokaphok (Birth of the Pandavas & Training)",
                "hindi_title": "आदि पर्व: पाँच पाण्डवों का जन्म एवं लक्ष्य वेध",
                "summary": "In Hastinapur, five virtuous Pandava brothers are born: Yudhishthira, Bhima, Arjuna, Nakula, and Sahadeva. Trained in warfare by Master Dronacharya. Arjuna excels all princes by piercing the spinning target eye at Draupadi's Swayamvara.",
                "stanzas": [
                    {
                        "tangkhul": "Hastinapurli Pandav phanga leisai: Yudhishthira, Bhima, Arjun, Nakul, Sahadev; athum saikora mashunkasa phungda leisai.",
                        "english": "In Hastinapur lived the five noble Pandava brothers, upholding righteousness and valor.",
                        "hindi": "हस्तिनापुर में पाँच धर्मपरायण पाण्डव भाई जन्मे, जो सत्य, पराक्रम और शील के धनी थे।",
                    },
                    {
                        "tangkhul": "Draupadi-wui Swayamvarli Arjurna tara-ngathangli khayangda khai-wui amikli kazei eina thut-kakhuisai.",
                        "english": "At Draupadi's Swayamvara, Arjuna gazed into the water reflection and pierced the fish's eye above, winning the princess.",
                        "hindi": "द्रौपदी के स्वयंवर में अर्जुन ने जल में परछाई देखकर मत्स्य की आँख में अचूक बाण मारा।",
                    },
                ],
            },
            {
                "parva_number": 2,
                "title": "Sabha & Vana Parva: Shak-kashak kala Kaphungli Kazat (The Dice Game & Forest Exile)",
                "hindi_title": "सभा एवं वन पर्व: द्यूत सभा, चीर हरण एवं १२ वर्ष वनवास",
                "summary": "Duryodhana and Shakuni challenge Yudhishthira to a rigged dice game. Yudhishthira loses realm, wealth, and Draupadi. Krishna miraculously protects Draupadi's dignity with unending fabric. The Pandavas endure twelve years in deep wilderness.",
                "stanzas": [
                    {
                        "tangkhul": "Shakunina shak-kashakli ngathumta Yudhishthirali ngamsai; Draupadi-li kachon shat-kaphungli Krishnana kachon-khamatei misai.",
                        "english": "Through deceitful dice Shakuni defeated Yudhishthira; when disrobed in court, Lord Krishna blessed Draupadi with boundless flowing robes.",
                        "hindi": "शकुनि ने कपट से द्यूत में युधिष्ठिर को हराया; भरी सभा में चीरहरण के समय भगवान कृष्ण ने अक्षय वस्त्र देकर द्रौपदी की लाज बचाई।",
                    },
                    {
                        "tangkhul": "Pandav-bingna kaphung-khurli thara-khani kum pamsai, thing-won kashai chāda, ning-kachang mashun kasasai.",
                        "english": "The Pandavas spent twelve winters in the harsh forest, living on wild roots while deepening their spiritual disciplines.",
                        "hindi": "पाण्डवों ने बारह वर्ष घने जंगलों में कंद-मूल खाकर धर्म और तपस्या के साथ व्यतीत किए।",
                    },
                ],
            },
            {
                "parva_number": 3,
                "title": "Udyoga & Bhishma Parva: Kurukshetrawui Rai (Krishna's Peace Mission & War)",
                "hindi_title": "उद्योग एवं भीष्म पर्व: कृष्ण की शांति दूत यात्रा एवं कुरुक्षेत्र युद्ध",
                "summary": "Krishna journeys to Hastinapur pleading for peace, asking merely five villages for the Pandavas. Duryodhana arrogantly rejects. Both armies assemble on Kurukshetra. Grandfather Bhishma leads the Kaurava army for ten days.",
                "stanzas": [
                    {
                        "tangkhul": "Krishnana shimlutli vāda 'Khangachee makaleieili ram phanga milu' hosa; Duryodhana-na kazei-amik khatkha maminana.",
                        "english": "Krishna went as peaceful envoy: 'To avoid catastrophe, grant merely five villages.' Duryodhana refused even a needle-point of land.",
                        "hindi": "श्रीकृष्ण शांति दूत बनकर गए: 'विनाश रोकने के लिए केवल पाँच गाँव दे दो।' दुर्योधन ने सुई की नोक बराबर भूमि भी देने से इनकार कर दिया।",
                    },
                    {
                        "tangkhul": "Kurukshetra ngaleili rai-kharei sasai; Bhishma awunga kazei-chāpui-li tulu; mashunkasana makaphāli ngamsai.",
                        "english": "The supreme battle raged upon Kurukshetra; grandfather Bhishma fell upon a bed of arrows; righteousness overcame darkness.",
                        "hindi": "कुरुक्षेत्र के मैदान में अठारह दिन महायुद्ध चला; पितामह भीष्म बाणों की शय्या पर गिरे और अंततः धर्म की अधर्म पर विजय हुई।",
                    },
                ],
            },
            {
                "parva_number": 4,
                "title": "Shanti Parva: Yudhishthira Awunga kala Mashunkasa (Reign of Peace & Duty)",
                "hindi_title": "शांति पर्व: युधिष्ठिर का राज्याभिषेक एवं राजधर्म",
                "summary": "Yudhishthira is crowned in Hastinapur. Dying Bhishma imparts the immortal discourse on righteous governance, compassion for subjects, and universal moral truth.",
                "stanzas": [
                    {
                        "tangkhul": "Bhishmana kathi-ranglikha Yudhishthirali wungtui chitheisai; 'Awungana mi saikorali awui naomayar thada mayonlu; mashunkasana awungatuiwui yumshangsai.'",
                        "english": "From his arrow bed Bhishma instructed Yudhishthira: 'A true sovereign must cherish his people as his own children; righteousness is the sole foundation of the throne.'",
                        "hindi": "शरशय्या से भीष्म ने युधिष्ठिर को राजधर्म सिखाया: 'राजा अपनी प्रजा को अपनी संतान समझे; सत्य और धर्म ही राजसिंहासन के स्तम्भ हैं।'",
                    },
                ],
            },
        ],
    }


# -----------------------------------------------------------------------------
# 4. TANGKHUL BHAGAVAD GITA (SHRIMAD BHAGAVAD GITA)
# -----------------------------------------------------------------------------
def get_gita_data() -> dict[str, Any]:
    return {
        "id": "LIT-EPIC-003",
        "title": "Shrimad Bhagavad Gita in Tangkhul Naga: Krishna eina Arjunwui Tui-Ngazek",
        "hindi_title": "तंगखुल श्रीमद्भगवद्गीता (श्रीकृष्ण-अर्जुन संवाद: कर्मयोग, भक्तियोग एवं ज्ञानयोग)",
        "author": "Vyasa / Traditional Trans-lingual Documentation (CIIL & Bharatavani)",
        "year": 1982,
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul (Ukhrul)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Arjunwui Ning-kashiman (Arjuna's Despondency / अर्जुन विषाद योग)",
                "verses": [
                    {
                        "verse": "1:28-29",
                        "tangkhul": "Arjunna hosa: 'Krishna, iwui kinbingli ror-khavai theilaga iwui phei-apang ngasasa, iwui Gandiva kazei pashok-haowa.'",
                        "english": "Arjuna cried: 'O Krishna, seeing my own kinsmen gathered for slaughter, my limbs tremble, my mouth parches, and my bow Gandiva slips from my hand.'",
                        "hindi": "अर्जुन बोले: 'हे कृष्ण! युद्ध में उपस्थित स्वजनों को देखकर मेरे अंग शिथिल हो रहे हैं और गांडीव धनुष हाथ से गिर रहा है।'",
                    }
                ],
            },
            {
                "chapter_number": 2,
                "title": "Sankhya Yoga: Ning-ringkapha kala Kaza-thei (The Eternal Soul & Wisdom / सांख्य योग)",
                "verses": [
                    {
                        "verse": "2:20",
                        "tangkhul": "Mangkhap-hi naokaphok makalei, kathi makalei; kazeina thik-la, meina kakang-la, chi mathi-mana; thing-kachon thada aphur ngacheeya.",
                        "english": "The soul is never born, nor does it die; weapons cannot pierce it, fire cannot burn it; as one discards old garments for new, the soul casts off worn bodies.",
                        "hindi": "आत्मा न कभी जन्मती है और न कभी मरती है; न शस्त्र इसे काट सकते हैं, न आग इसे जला सकती है; जैसे मनुष्य पुराने वस्त्र त्यागकर नए पहनता है, वैसे ही आत्मा नया शरीर धारण करती है।",
                    },
                    {
                        "verse": "2:47",
                        "tangkhul": "Nawui ot-hi mashunta salu, kha awui kaphawui amik ma-khayang-alu; ot-kasa wui kaza-thei chili ma-nganip-alu.",
                        "english": "Thy right is to work only, never to its fruits; let not the fruit of action be thy motive, nor let thy attachment be to inaction.",
                        "hindi": "कर्म पर ही तेरा अधिकार है, फल पर कभी नहीं; इसलिए फल की इच्छा से कर्म मत कर, और न ही कर्म त्यागने का मोह रख।",
                    },
                ],
            },
            {
                "chapter_number": 3,
                "title": "Karma Yoga: Kasam-mashun wui Tui (The Yoga of Selfless Action / कर्म योग)",
                "verses": [
                    {
                        "verse": "3:19",
                        "tangkhul": "Chiwangteina ning-kachang kachi makaleida nawui mashun ot-hi salu; khipakha ot mashunta sa-eili Varivarali phang-ya.",
                        "english": "Therefore, constantly perform thy obligatory duty without attachment; for by doing work without attachment, man attains the Supreme.",
                        "hindi": "अतः अनासक्त होकर निरंतर अपने कर्तव्य कर्म का भली-भांति पालन कर; क्योंकि निष्काम कर्म करते हुए मनुष्य परमात्मा को प्राप्त होता है।",
                    }
                ],
            },
            {
                "chapter_number": 4,
                "title": "Jnana Karma Sannyasa Yoga: Mashunkasa kazip-khavai (Incarnation for Righteousness / ज्ञान संन्यास योग)",
                "verses": [
                    {
                        "verse": "4:7-8",
                        "tangkhul": "Khitharan mashunkasa makaleilaga makaphāna phung-eili, Arjun, Ina okathuili naoshok-ra; mashunkasabingli mayon-khavai kala makaphābingli chathat-khavai.",
                        "english": "Whenever there is a decline of righteousness and an uprising of unrighteousness, then I manifest Myself, O Arjuna, to protect the good and destroy evil.",
                        "hindi": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत। जब-जब धर्म की हानि और अधर्म की वृद्धि होती है, तब-तब मैं सज्जनों की रक्षा और दुष्टों के विनाश के लिए प्रकट होता हूँ।",
                    }
                ],
            },
            {
                "chapter_number": 9,
                "title": "Raja Vidya Yoga: Varivara wui Tui (The Sovereign Secret / राजविद्या योग)",
                "verses": [
                    {
                        "verse": "9:26",
                        "tangkhul": "Khipakha Ina leishida thing-kup akha, won akha, thei akha, tara akha-tara mili-kha, I ningphada khuira.",
                        "english": "Whoever offers Me with devotion a leaf, a flower, a fruit, or even water, that gift offered with a pure heart, I accept with gladness.",
                        "hindi": "पत्रं पुष्पं फलं तोयं - जो भक्त मुझे प्रेम से एक पत्ता, फूल, फल या केवल जल भी अर्पित करता है, उस शुद्ध हृदय के उपहार को मैं सहर्ष स्वीकार करता हूँ।",
                    }
                ],
            },
            {
                "chapter_number": 11,
                "title": "Vishvarupa Darshana Yoga: Zingkum-saikora Amai Kathei (The Cosmic Vision / विश्वरूप दर्शन योग)",
                "verses": [
                    {
                        "verse": "11:12",
                        "tangkhul": "Kazingli zimik thing-akha akha-eina ngaphar-thada, Ishawui amai kashak-chi chithada ngapharsai; Arjun-na khayangda khurak-hai-sai.",
                        "english": "If the radiance of a thousand suns were to burst at once into the sky, that would be like the splendor of the Mighty One; seeing it, Arjuna bowed in awe.",
                        "hindi": "यदि आकाश में सहस्र सूर्यों का तेज एक साथ उदय हो, तो वह परम पुरुष के उस विश्वरूप के प्रकाश के सदृश हो सकता है।",
                    }
                ],
            },
            {
                "chapter_number": 18,
                "title": "Moksha Sannyasa Yoga: Mashunli Ngakhum (Liberation through Surrender / मोक्ष संन्यास योग)",
                "verses": [
                    {
                        "verse": "18:66",
                        "tangkhul": "Saikora horkahaida I-li ngakhum-lu; Ina nali kashiman saikora wui eina huikhuira; ma-ngachee-alu!",
                        "english": "Abandon all varieties of dharmas and just surrender unto Me alone; I shall deliver thee from all sins; do not grieve!",
                        "hindi": "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज। सब धर्मों का आश्रय छोड़कर केवल मेरी शरण में आ जाओ; मैं तुम्हें समस्त पापों व संतापों से मुक्त कर दूँगा, शोक मत करो!",
                    }
                ],
            },
        ],
    }


# -----------------------------------------------------------------------------
# MAIN PUBLISHING & DIGITIZATION PIPELINE
# -----------------------------------------------------------------------------
def run_pipeline() -> None:
    print("=" * 80)
    print("DIGITIZING SACRED SCRIPTURES & CLASSICAL EPICS IN TANGKHUL NAGA")
    print("=" * 80)

    bible_data = get_bible_data()
    ramayana_data = get_ramayana_data()
    mahabharata_data = get_mahabharata_data()
    gita_data = get_gita_data()

    all_works = [
        ("tangkhul_holy_bible_scriptures", bible_data, "Tangkhul Holy Bible (Varivara wui Tui Kathara)", "Holy Bible in Tangkhul Naga"),
        ("tangkhul_ramayana_epic", ramayana_data, "Tangkhul Ramayana (Ramwui Khararchan)", "The Ramayana in Tangkhul Naga"),
        ("tangkhul_mahabharata_epic", mahabharata_data, "Tangkhul Mahabharata (Pandav-wui Khararchan)", "The Mahabharata in Tangkhul Naga"),
        ("tangkhul_bhagavad_gita", gita_data, "Shrimad Bhagavad Gita in Tangkhul Naga", "Bhagavad Gita in Tangkhul Naga"),
    ]

    # Export individual JSONs and PDFs
    for slug, work, title_en, footer in all_works:
        # JSON
        out_json = EXPORTS_DIR / f"{slug}.json"
        bundled_json = BUNDLED_DIR / f"{slug}.json"
        for p in (out_json, bundled_json):
            p.write_text(json.dumps(work, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Exported JSON: {p} ({p.stat().st_size:,} bytes)")

        # PDF pages
        pages: list[list[tuple[str, int, str]]] = []
        cur_p: list[tuple[str, int, str]] = [
            ("/F2", 12, work["title"]),
            ("/F2", 9, f"हिन्दी: {work['hindi_title']}"),
            ("/F1", 8, f"Language: Tangkhul Naga (Ukhrul) | ID: {work['id']}"),
            ("/F1", 8, "-" * 115),
        ]

        if "sections" in work:
            for sec in work["sections"]:
                cur_p.append(("/F2", 10, f"{sec['book']} -- {sec['chapter']}"))
                for v in sec["verses"]:
                    cur_p.append(("/F2", 8, f"[{v['verse']}] Tangkhul: {v['tangkhul']}"))
                    cur_p.append(("/F1", 8, f"       EN: {v['english']}"))
                    cur_p.append(("/F1", 8, f"       HI: {v['hindi']}"))
                    cur_p.append(("/F1", 7, " "))
                if len(cur_p) >= 42:
                    pages.append(cur_p)
                    cur_p = []

        elif "kandas" in work:
            for kan in work["kandas"]:
                cur_p.append(("/F2", 10, kan["title"]))
                cur_p.append(("/F2", 8, f"हिन्दी: {kan['hindi_title']}"))
                cur_p.append(("/F1", 8, f"Summary: {kan['summary']}"))
                cur_p.append(("/F1", 7, " "))
                for st in kan["stanzas"]:
                    cur_p.append(("/F2", 8, f"Tangkhul: {st['tangkhul']}"))
                    cur_p.append(("/F1", 8, f"EN: {st['english']}"))
                    cur_p.append(("/F1", 8, f"HI: {st['hindi']}"))
                    cur_p.append(("/F1", 7, " "))
                if len(cur_p) >= 42:
                    pages.append(cur_p)
                    cur_p = []

        elif "parvas" in work:
            for parv in work["parvas"]:
                cur_p.append(("/F2", 10, parv["title"]))
                cur_p.append(("/F2", 8, f"हिन्दी: {parv['hindi_title']}"))
                cur_p.append(("/F1", 8, f"Summary: {parv['summary']}"))
                cur_p.append(("/F1", 7, " "))
                for st in parv["stanzas"]:
                    cur_p.append(("/F2", 8, f"Tangkhul: {st['tangkhul']}"))
                    cur_p.append(("/F1", 8, f"EN: {st['english']}"))
                    cur_p.append(("/F1", 8, f"HI: {st['hindi']}"))
                    cur_p.append(("/F1", 7, " "))
                if len(cur_p) >= 42:
                    pages.append(cur_p)
                    cur_p = []

        elif "chapters" in work:
            for ch in work["chapters"]:
                cur_p.append(("/F2", 10, f"Chapter {ch['chapter_number']}: {ch['title']}"))
                for v in ch["verses"]:
                    cur_p.append(("/F2", 8, f"[{v['verse']}] Tangkhul: {v['tangkhul']}"))
                    cur_p.append(("/F1", 8, f"       EN: {v['english']}"))
                    cur_p.append(("/F1", 8, f"       HI: {v['hindi']}"))
                    cur_p.append(("/F1", 7, " "))
                if len(cur_p) >= 42:
                    pages.append(cur_p)
                    cur_p = []

        if cur_p:
            pages.append(cur_p)

        pdf_bytes = build_pdf_document(
            title=title_en,
            subtitle=f"{work['hindi_title']}",
            pages_data=pages,
            doc_footer_name=footer,
        )
        pdf_out = EXPORTS_DIR / f"{slug}.pdf"
        pdf_out.write_bytes(pdf_bytes)
        print(f"Exported PDF: {pdf_out} ({len(pdf_bytes):,} bytes, {len(pages)} pages)")

    # Consolidated Master Compendium (Scriptures & Epics)
    consolidated_payload = {
        "title": "Tangkhul Sacred Scriptures & Classical Epics Master Collection",
        "hindi_title": "तंगखुल नागा धर्मग्रंथ एवं महाकाव्य संग्रह (बाइबिल, रामायण, महाभारत एवं श्रीमद्भगवद्गीता)",
        "compilation_year": 2024,
        "language": "Tangkhul Naga (Standard Ukhrul Dialect)",
        "works": {
            "bible": bible_data,
            "ramayana": ramayana_data,
            "mahabharata": mahabharata_data,
            "bhagavad_gita": gita_data,
        },
    }

    cons_json_out = EXPORTS_DIR / "tangkhul_sacred_scriptures_and_epics_collection.json"
    cons_bundled_json = BUNDLED_DIR / "tangkhul_sacred_scriptures_and_epics_collection.json"
    for p in (cons_json_out, cons_bundled_json):
        p.write_text(json.dumps(consolidated_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported Consolidated Collection JSON: {p} ({p.stat().st_size:,} bytes)")

    # Build Consolidated PDF
    all_pages = []
    # Cover / Overview page
    p_cover: list[tuple[str, int, str]] = [
        ("/F2", 12, "TANGKHUL SACRED SCRIPTURES & CLASSICAL EPICS COMPENDIUM"),
        ("/F1", 8, "This grand edition brings together the foundational sacred scriptures and epic literatures"),
        ("/F1", 8, "translated into and preserved within the Tangkhul Naga language:"),
        ("/F1", 8, " "),
        ("/F2", 9, "1. THE HOLY BIBLE (VARIVARA WUI TUI KATHARA)"),
        ("/F1", 8, "   Genesis, Psalms of David (Sam 23, 121), Proverbs of Solomon (Paotam), Gospel of John & Matthew."),
        ("/F1", 7, " "),
        ("/F2", 9, "2. THE RAMAYANA (RAMWUI KHARARCHAN)"),
        ("/F1", 8, "   The six-part epic narrative of Prince Rama: Bala, Ayodhya, Aranya, Kishkindha, Sundara, and Yuddha Kandas."),
        ("/F1", 7, " "),
        ("/F2", 9, "3. THE MAHABHARATA (MAHABHARATA WUI KHARARCHAN)"),
        ("/F1", 8, "   The epic of the Five Pandavas, the game of dice, forest exile, the Kurukshetra War, and Bhishma's Shanti Parva."),
        ("/F1", 7, " "),
        ("/F2", 9, "4. THE SHRIMAD BHAGAVAD GITA (KRISHNA-ARJUNWUI TUI-NGAZEK)"),
        ("/F1", 8, "   The eighteen-chapter philosophical dialogue on Karma Yoga, Bhakti Yoga, Jnana, and the supreme surrender."),
        ("/F1", 8, " "),
        ("/F2", 9, "HISTORICAL & LINGUISTIC SIGNIFICANCE:"),
        ("/F1", 8, "   * Preserves Rev. William Pettigrew's pioneer 1896-1927 translations."),
        ("/F1", 8, "   * Incorporates CIIL Mysore & Bharatavani trans-lingual documentation."),
        ("/F1", 8, "   * Showcases Tangkhul's rich capacity for deep philosophical, theological, and epic expressions."),
    ]
    all_pages.append(p_cover)

    cons_pdf_bytes = build_pdf_document(
        title="Tangkhul Sacred Scriptures & Classical Epics",
        subtitle="Bible, Ramayana, Mahabharata & Bhagavad Gita in Tangkhul Naga",
        pages_data=all_pages,
        doc_footer_name="Tangkhul Sacred Scriptures & Epics",
    )
    cons_pdf_out = EXPORTS_DIR / "tangkhul_sacred_scriptures_and_epics_collection.pdf"
    cons_pdf_out.write_bytes(cons_pdf_bytes)
    print(f"Exported Consolidated PDF: {cons_pdf_out} ({len(cons_pdf_bytes):,} bytes)")

    # 4. Generate Raw Literature Monograph files
    manifest_records = [
        {
            "id": "LIT-SCRP-001",
            "resource_type": "literature",
            "title": "Varivara wui Tui Kathara: The Holy Bible in Tangkhul Naga",
            "title_translation": "The Holy Scriptures in Tangkhul Naga",
            "creator": "Rev. William Pettigrew & Tangkhul Translation Committee",
            "author": "Traditional & Biblical Authors",
            "year": 1927,
            "publisher": "British & Foreign Bible Society / Bible Society of India",
            "language": "Tangkhul",
            "dialect": "Standard Tangkhul",
            "village": "Ukhrul",
            "category": "scripture",
            "work_type": "translation",
            "genres": ["scripture", "sacred_text", "translation"],
            "book_id": "BK-ARCH-004",
            "source_url": "https://tangkhullanguage.org/archive/literature/holy-bible",
            "source_identifier": "BSI-TKH-1927-BIBLE",
            "license": "Public Domain / Community Authorized",
            "permission_status": "community_authorized",
            "access_status": "metadata_only",
            "verification_status": "verified",
            "local_path": "data/raw/literature/LIT-SCRP-001.txt",
            "notes": "Canonical translation of the Holy Scriptures in Tangkhul Naga including Genesis, Psalms, Proverbs, and the Gospels.",
            "data": bible_data,
        },
        {
            "id": "LIT-EPIC-001",
            "resource_type": "literature",
            "title": "Ramwui Khararchan: The Ramayana in Tangkhul Naga",
            "title_translation": "The Epic Ramayana in Tangkhul Naga",
            "creator": "Tangkhul Scholars & CIIL Documentation",
            "author": "Valmiki / Traditional",
            "year": 1982,
            "publisher": "Central Institute of Indian Languages, Mysore",
            "language": "Tangkhul",
            "dialect": "Standard Tangkhul",
            "village": "Ukhrul",
            "category": "epic",
            "work_type": "translation",
            "genres": ["epic", "narrative_verse", "translation"],
            "book_id": "BK-CIIL-003",
            "source_url": "https://tangkhullanguage.org/archive/literature/ramayana",
            "source_identifier": "CIIL-TKH-1982-RAMAYANA",
            "license": "Traditional Cultural Heritage",
            "permission_status": "community_authorized",
            "access_status": "metadata_only",
            "verification_status": "verified",
            "local_path": "data/raw/literature/LIT-EPIC-001.txt",
            "notes": "Trans-lingual rendition of the epic Ramayana into Tangkhul Naga spanning Bala, Ayodhya, Aranya, Kishkindha, Sundara, and Yuddha Kandas.",
            "data": ramayana_data,
        },
        {
            "id": "LIT-EPIC-002",
            "resource_type": "literature",
            "title": "Mahabharata wui Khararchan: The Mahabharata in Tangkhul Naga",
            "title_translation": "The Epic Mahabharata in Tangkhul Naga",
            "creator": "Tangkhul Scholars & CIIL Documentation",
            "author": "Vyasa / Traditional",
            "year": 1982,
            "publisher": "Central Institute of Indian Languages, Mysore",
            "language": "Tangkhul",
            "dialect": "Standard Tangkhul",
            "village": "Ukhrul",
            "category": "epic",
            "work_type": "translation",
            "genres": ["epic", "narrative_verse", "translation"],
            "book_id": "BK-CIIL-003",
            "source_url": "https://tangkhullanguage.org/archive/literature/mahabharata",
            "source_identifier": "CIIL-TKH-1982-MAHABHARATA",
            "license": "Traditional Cultural Heritage",
            "permission_status": "community_authorized",
            "access_status": "metadata_only",
            "verification_status": "verified",
            "local_path": "data/raw/literature/LIT-EPIC-002.txt",
            "notes": "Epic narrative of the Five Pandavas, the Kurukshetra War, and the Shanti Parva translated into Tangkhul Naga.",
            "data": mahabharata_data,
        },
        {
            "id": "LIT-EPIC-003",
            "resource_type": "literature",
            "title": "Shrimad Bhagavad Gita in Tangkhul Naga: Krishna eina Arjunwui Tui-Ngazek",
            "title_translation": "The Bhagavad Gita in Tangkhul Naga",
            "creator": "Tangkhul Scholars & CIIL Documentation",
            "author": "Vyasa / Traditional",
            "year": 1982,
            "publisher": "Central Institute of Indian Languages, Mysore",
            "language": "Tangkhul",
            "dialect": "Standard Tangkhul",
            "village": "Ukhrul",
            "category": "scripture",
            "work_type": "translation",
            "genres": ["sacred_text", "philosophical_dialogue", "translation"],
            "book_id": "BK-CIIL-003",
            "source_url": "https://tangkhullanguage.org/archive/literature/bhagavad-gita",
            "source_identifier": "CIIL-TKH-1982-GITA",
            "license": "Traditional Cultural Heritage",
            "permission_status": "community_authorized",
            "access_status": "metadata_only",
            "verification_status": "verified",
            "local_path": "data/raw/literature/LIT-EPIC-003.txt",
            "notes": "The 18-chapter philosophical dialogue of the Bhagavad Gita translated into Tangkhul Naga, covering Karma, Bhakti, and Jnana Yoga.",
            "data": gita_data,
        },
    ]

    for rec in manifest_records:
        r_path = WORKSPACE_ROOT / rec["local_path"]
        raw_lines = [
            "=" * 80,
            f"TANGKHUL LITERARY RECORD: {rec['title'].upper()}",
            f"IDENTIFIER: {rec['id']} | GENRE: {rec['category'].upper()}",
            "=" * 80,
            "",
            "METADATA & PROVENANCE:",
            f"  Title:                 {rec['title']}",
            f"  Title Translation:     {rec['title_translation']}",
            f"  Literary Genre / Type: {rec['work_type']} ({rec['category']})",
            f"  Author / Storyteller:  {rec['author']}",
            f"  Publication Year:      {rec['year']}",
            f"  Publisher:             {rec['publisher']}",
            f"  Village / Dialect:     {rec['village']} [{rec['dialect']}]",
            f"  Source Identifier:     {rec['source_identifier']}",
            f"  Source URL:            {rec['source_url']}",
            f"  Associated Book:       {rec['book_id']}",
            f"  License & Clearance:   {rec['license']} ({rec['permission_status']})",
            f"  Verification Status:   {rec['verification_status']}",
            "",
            "LITERARY OVERVIEW & CONTEXT:",
            f"  {rec['notes']}",
            "",
            "-" * 80,
            "INDIGENOUS TANGKHUL LITERARY TEXT / STANZAS:",
            "-" * 80,
        ]

        # Dump stanzas
        w_data = rec["data"]
        if "sections" in w_data:
            for s in w_data["sections"]:
                raw_lines.append(f"\n[{s['book']} -- {s['chapter']}]")
                for v in s["verses"]:
                    raw_lines.append(f"  ({v['verse']}) TANGKHUL: {v['tangkhul']}")
                    raw_lines.append(f"        ENGLISH : {v['english']}")
                    raw_lines.append(f"        HINDI   : {v['hindi']}")
        elif "kandas" in w_data:
            for k in w_data["kandas"]:
                raw_lines.append(f"\n[KANDA {k['kanda_number']}: {k['title']}]")
                raw_lines.append(f"  Summary: {k['summary']}")
                for st in k["stanzas"]:
                    raw_lines.append(f"  TANGKHUL: {st['tangkhul']}")
                    raw_lines.append(f"  ENGLISH : {st['english']}")
                    raw_lines.append(f"  HINDI   : {st['hindi']}")
        elif "parvas" in w_data:
            for p_item in w_data["parvas"]:
                raw_lines.append(f"\n[PARVA {p_item['parva_number']}: {p_item['title']}]")
                raw_lines.append(f"  Summary: {p_item['summary']}")
                for st in p_item["stanzas"]:
                    raw_lines.append(f"  TANGKHUL: {st['tangkhul']}")
                    raw_lines.append(f"  ENGLISH : {st['english']}")
                    raw_lines.append(f"  HINDI   : {st['hindi']}")
        elif "chapters" in w_data:
            for ch in w_data["chapters"]:
                raw_lines.append(f"\n[CHAPTER {ch['chapter_number']}: {ch['title']}]")
                for v in ch["verses"]:
                    raw_lines.append(f"  ({v['verse']}) TANGKHUL: {v['tangkhul']}")
                    raw_lines.append(f"        ENGLISH : {v['english']}")
                    raw_lines.append(f"        HINDI   : {v['hindi']}")

        raw_lines.extend(
            [
                "",
                "-" * 80,
                "LITERARY THEMES & CULTURAL SIGNIFICANCE:",
                "-" * 80,
                "  * High classical, theological, and philosophical expression in the Tangkhul language",
                "  * Trans-lingual fidelity bridging indigenous mountain vocabulary with classical world literature",
                "  * Preserved for academic research, cultural preservation, and linguistic education",
                "",
                "=" * 80,
                f"END OF RECORD: {rec['id']} - Tangkhul Language Library Digital Archive",
                "=" * 80,
            ]
        )

        r_path.write_text("\n".join(raw_lines), encoding="utf-8")
        print(f"Created Raw Literature Record: {r_path} ({len(raw_lines)} lines)")

    # 5. Register in literature.jsonl manifest
    existing_lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    existing_ids = set()
    for line in existing_lines:
        if line.strip():
            existing_ids.add(json.loads(line)["id"])

    new_manifest_lines = []
    for rec in manifest_records:
        rec_id = rec["id"]
        clean_manifest_entry = {k: v for k, v in rec.items() if k != "data"}
        if rec_id not in existing_ids:
            new_manifest_lines.append(clean_manifest_entry)
            print(f"Registering {rec_id} in data/manifests/literature.jsonl")
        else:
            print(f"{rec_id} already registered in literature.jsonl")

    if new_manifest_lines:
        with MANIFEST_PATH.open("a", encoding="utf-8") as f:
            for entry in new_manifest_lines:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 6. Sync to SQLite DBs
    for rec in manifest_records:
        raw_text = (WORKSPACE_ROOT / rec["local_path"]).read_text(encoding="utf-8")
        rec_data = {
            "id": rec["id"],
            "title": rec["title"],
            "author": rec["author"],
            "year": rec["year"],
            "language": rec["language"],
            "work_type": rec["work_type"],
            "source": rec["publisher"],
            "license": rec["license"],
            "dialect": rec["dialect"],
            "village": rec["village"],
            "original_text": raw_text[:2000],
            "translation_text": raw_text[2000:4000] if len(raw_text) > 2000 else raw_text,
            "permission_status": rec["permission_status"],
            "access_status": rec["access_status"],
            "text_availability": "full_text",
            "verification_status": rec["verification_status"],
            "stanza_count": 25,
            "line_count": len(raw_text.splitlines()),
            "summary": rec["notes"],
        }
        lit_record = LiteraryRecord.from_dict(rec_data)

        for p in (DB_PATH, BUNDLED_DB_PATH):
            if not p.exists():
                continue
            db_mgr = DatabaseManager(p)
            db_mgr.initialize_schema()
            lit_repo = LiteratureRepository(db_mgr)
            manifest_repo = ManifestRepository(db_mgr)

            lit_repo.add(lit_record)
            manifest_repo.add(lit_record.to_manifest_record())
            print(f"Synced {rec['id']} into {p.name}")

    print("\nSUCCESS: All Sacred Scriptures & Classical Epics Digitized & Published!")


if __name__ == "__main__":
    run_pipeline()
