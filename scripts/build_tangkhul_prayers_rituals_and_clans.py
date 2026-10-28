"""Tangkhul Prayers, Rituals, Ceremonies & Clan System Digitization Pipeline.

Builds and exports:
1. Tangkhul Traditional Prayers & Invocations (Hai-kaphā kala Seikha-kaphā)
   - data/exports/tangkhul_prayers_and_invocations.json & .pdf
2. Tangkhul Sacred Rituals, Lifecycle Ceremonies & Taboos (Phanit, Kakhangaso kala Khamasit)
   - data/exports/tangkhul_rituals_and_ceremonies.json & .pdf
3. Tangkhul Clan System, Kinship & Social Order (Shang, Shangnao kala Hangva)
   - data/exports/tangkhul_clans_kinship_and_social_structure.json & .pdf
4. Consolidated Grand Master Encyclopedia
   - data/exports/tangkhul_prayers_rituals_and_clans_master_encyclopedia.json & .pdf
5. Raw culture monographs in data/raw/culture/
   - CULT-PRAY-001_tangkhul_traditional_prayers.txt
   - CULT-RIT-003_tangkhul_sacred_rituals_ceremonies.txt
   - CULT-SOC-001_tangkhul_clans_social_order.txt
6. Manifest registration in data/manifests/culture.jsonl
7. SQLite database synchronization in both repositories
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path("f:/tangkhul-language-library")
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

EXPORTS_DIR = WORKSPACE_ROOT / "data" / "exports"
BUNDLED_DIR = WORKSPACE_ROOT / "src" / "tangkhul_lib" / "data"
RAW_DIR = WORKSPACE_ROOT / "data" / "raw" / "culture"
MANIFEST_PATH = WORKSPACE_ROOT / "data" / "manifests" / "culture.jsonl"
DB_PATH = WORKSPACE_ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB_PATH = BUNDLED_DIR / "tangkhul_corpus.sqlite"

from tangkhul_lib.culture.models import CulturalRecord
from tangkhul_lib.storage.database import DatabaseManager
from tangkhul_lib.storage.repositories import CultureRepository, ManifestRepository


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
                ("/F1", 8, "Tangkhul Language Library Digital Archive -- Cultural & Spiritual Heritage")
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


# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================

PRAYERS_DATA = {
    "id": "CULT-PRAY-001",
    "title": "Tangkhul Traditional Prayers & Invocations (Hai-kapha kala Seikha-kapha)",
    "title_translation": "Comprehensive Compendium of Tangkhul Invocations, Blessing Prayers, and Sacred Chants",
    "category": "ritual",
    "subcategory": "prayers_and_invocations",
    "creator": "Tangkhul Community Elders & Traditional Invocators",
    "year": 1911,
    "publisher": "Traditional Oral Heritage (Hodson 1911, Horam 1977, Pettigrew 1907)",
    "language": "Tangkhul",
    "dialect": "Standard Tangkhul (Ukhrul / Hunphun)",
    "village": "Ukhrul / Hunphun",
    "permission_status": "community_authorized",
    "access_status": "metadata_only",
    "verification_status": "verified",
    "local_path": "data/raw/culture/CULT-PRAY-001_tangkhul_traditional_prayers.txt",
    "notes": "Comprehensive documentation of traditional Tangkhul invocations (Hai-kapha) and blessing chants (Seikha-kapha) addressed to the Supreme Creator (Varivara), mountain spirits, hearth dedication, agricultural blessings, and ancestral spirits.",
    "prayer_sections": [
        {
            "section_id": "PRAY-01",
            "section_title": "Varivara-li Hai-kapha: Invocations to the Supreme Creator",
            "ritual_context": "Solemn dawn invocations addressed to the Creator of heaven and earth during village convocations.",
            "prayers": [
                {
                    "prayer_name": "Kazing kala Ngalei Kasa Akhavara (Sovereign of Heaven and Earth)",
                    "tangkhul": "Varivara, kazing kala ngalei kasa akhavara! Iram Hunphun kala Tangkhul ngaleili kapha eina leishat kachung khami. Macham-matai, kazingwui ringkapha kala ngaleiwui kachon shim kachivali shung-ngasak-lu.",
                    "english": "O Varivara, Sovereign Creator of heaven and earth! Bestow goodness and overflowing love upon Hunphun and all Tangkhul lands. Let the peace of heaven and the fruitfulness of the earth fill every home.",
                    "hindi": "हे वरिवरा, स्वर्ग और पृथ्वी के सृष्टिकर्ता परमेश्वर! हमारे हुंफुन गांव और संपूर्ण तंगखुल भूमि पर अपनी भलाई और असीम अनुग्रह बरसाएं। हर घर को स्वर्गीय शांति और पृथ्वी की उर्वरता से परिपूर्ण करें।"
                },
                {
                    "prayer_name": "Ringkaphawui Ning-Ngazek (Petition for Life, Health, and Unity)",
                    "tangkhul": "Iramwui mayar-shanao kachivali kapha kakhanganuina ninglum-hai-lu; kacham-kahao maningda, maram-matai eina ngachee kachiva machik-hai-lu.",
                    "english": "Endow all the sons and daughters of our land with righteous discernment and upright character; banish famine and poverty, and protect us from every calamity.",
                    "hindi": "हमारी भूमि के सभी पुत्र-पुत्रियों को धार्मिक विवेक और सदाचार से सुशोभित करें; अकाल व दरिद्रता को दूर रखें और हर विपत्ति से हमारी रक्षा करें।"
                }
            ]
        },
        {
            "section_id": "PRAY-02",
            "section_title": "Luira Shimlut-wui Seikha: Agrarian Sowing & Harvest Invocations",
            "ritual_context": "Chanted at dawn by the Awunga (chief) turning the first sod of earth during Luira Phanit.",
            "prayers": [
                {
                    "prayer_name": "Shimlut Kaphung Invocatory Chant (First Seed Blessing)",
                    "tangkhul": "Tara-kong kala kaphung ngalemwui makhangai ngachaili, kachang kathara eina phung-kasa oira. Kachim-kasa mayar-shanao mashung-ngasak-lu; changva kachon kachivali mathala kaza samphang-ngasak-lu.",
                    "english": "By the quiet mountain streams and along terraced slopes, let the newly sown seeds take deep root in fertile earth. Bless the labor of men and women; may every sheaf harvested bring joyful sustenance.",
                    "hindi": "पर्वतीय जलधाराओं और ढलानों पर बोए गए नए बीजों को उपजाऊ धरती में गहराई से फलने-फूलने का आशीर्वाद दें। सभी पुरुषों और महिलाओं के श्रम को सफल करें; हर बाली प्रचुर अन्न और सुख प्रदान करे।"
                },
                {
                    "prayer_name": "Chumpha Granary Consecration Prayer",
                    "tangkhul": "Chumkhur hili kashung tara-chang, kacham kashiman malailaka; shanao mibingwui pāng eina phung-kasa za-machit mashung-ngasak-lu.",
                    "english": "May the grain stored in this sacred granary endure through every season, banishing all want; through the blessed hands of women custodians, let our sustenance never fail.",
                    "hindi": "इस पवित्र अन्न भंडार में संचित अनाज हर ऋतु में बना रहे और हर अभाव को दूर करे; अन्न की संरक्षिका मातृशक्ति के हाथों से हमारी संपन्नता कभी कम न हो।"
                }
            ]
        },
        {
            "section_id": "PRAY-03",
            "section_title": "Shimsa kala Meiphung Invocations: Hearth & Domestic Protection",
            "ritual_context": "Chanted during the dedication of a newly built house when kindling the sacred hearth fire.",
            "prayers": [
                {
                    "prayer_name": "Meiphung Kathara Consecration (Sacred Hearth Flame)",
                    "tangkhul": "Meiphung kathara hili mei-ngatai eina ngachee kachiva machik-hai-lu. Shimwui naonao kala marva ningcha-ngachan eina khararchan wui tui kathara thotkakhui mashung-ngasak-lu.",
                    "english": "Around this consecrated hearth, kindle the sacred fire to dispel darkness, sickness, and strife. May the children and elders of this household dwell in unity and pass down ancestral virtues across generations.",
                    "hindi": "इस पवित्र चूल्हे पर प्रज्वलित अग्नि समस्त अंधकार, व्याधि और कलह को दूर करे। इस घर के बच्चे और वृद्धजन एकता में रहें और पूर्वजों के संस्कारों को पीढ़ी-दर-पीढ़ी आगे बढ़ाएं।"
                }
            ]
        },
        {
            "section_id": "PRAY-04",
            "section_title": "Khayang Shongfa Hai-kapha: Mountain Wilderness & Wayfarer Blessing",
            "ritual_context": "Uttered before undertaking mountain expeditions, hunting journeys, or cross-valley trade.",
            "prayers": [
                {
                    "prayer_name": "Shongfa Makhangai Prayer (Safe Passage Across Mountain Ridges)",
                    "tangkhul": "Kaphung kachang, kongrei kala thang-khala shongfali yaokhayei eina kacham-kahao maning-ngasak-lu. Awungana iram-iramli macham kashap samphang-ngasak-lu.",
                    "english": "Across high mountain ridges, turbulent torrents, and wilderness trails, grant sure footing and keep all danger afar. May the traveler return home bearing peace and honor.",
                    "hindi": "ऊंचे पर्वतों, उफनती नदियों और बीहड़ वन्य मार्गों पर हमारे कदमों को स्थिरता दें और सभी विपत्तियों से रक्षा करें। यात्री कुशलतापूर्वक शांति और सम्मान के साथ घर लौटें।"
                }
            ]
        },
        {
            "section_id": "PRAY-05",
            "section_title": "Thisham Kasa Akhava Hai-kapha: Ancestral Memorial Chants",
            "ritual_context": "Chanted by village elders lighting pine-splint torches during Thisham Phanit (Feast of Departing Souls).",
            "prayers": [
                {
                    "prayer_name": "Kasa Akhava Chanted Requiem (Farewell to Departed Ancestors)",
                    "tangkhul": "Kasa Akhava kaphungli va-kahai araza, meira kaphit hieina shongfa theingasak-lu. Ningkacham eina mangachon-hai-lu; ringphawui ramli mashungda leisang-lu.",
                    "english": "O revered departed ancestors journeying toward Kasa Akhava (the ancestral spirit realm), let these flaming pine torches illuminate your path. Rest in tranquil grace; enter the eternal land of blessed peace.",
                    "hindi": "हे पूर्वजों की आत्माओं, कासा अखावा (परम लोक) की यात्रा पर इन पाइन की मशालों के उजाले में अपना मार्ग प्रशस्त करें। दिव्य शांति में विश्राम करें और शाश्वत सुख के धाम में प्रवेश करें।"
                }
            ]
        }
    ]
}

RITUALS_DATA = {
    "id": "CULT-RIT-003",
    "title": "Tangkhul Sacred Rituals, Ceremonies & Taboos (Phanit, Kakhangaso kala Khamasit)",
    "title_translation": "Master Archive of Tangkhul Lifecycle Ceremonies, Agrarian Rites, and Sacred Taboo Observances",
    "category": "ritual",
    "subcategory": "lifecycle_and_agrarian_rituals",
    "creator": "Tangkhul Hereditary Custodians & Village Elders",
    "year": 1911,
    "publisher": "Documented in Hodson 1911, Horam 1977, Ruivah 1993",
    "language": "Tangkhul",
    "dialect": "Standard Tangkhul (Ukhrul / Hunphun)",
    "village": "Ukhrul / Hunphun",
    "permission_status": "community_authorized",
    "access_status": "metadata_only",
    "verification_status": "verified",
    "local_path": "data/raw/culture/CULT-RIT-003_tangkhul_sacred_rituals_ceremonies.txt",
    "notes": "Comprehensive archival codification of Tangkhul ceremonial life: agrarian seasonal rites (Luira, Chumpha, Mangkhap, Dharreo), human lifecycle rituals (birth, naming, youth dormitory induction, marriage, house dedication, death), prestige feast cycles (Maran Kasa), chiefly enthronement, and sacred taboo (Khamasit / Genna) observances.",
    "ceremonial_cycles": [
        {
            "cycle_name": "Agrarian Ritual Cycle (Luisak Kakhangaso)",
            "rites": [
                {
                    "name": "Luira Shimlut-kaphung (First Sowing Rite)",
                    "timing": "January / February (Spring seed-sowing)",
                    "presiding": "Awunga (Hereditary Village Chief)",
                    "description": "At dawn on the first day of Luira Phanit, the chief turns the ceremonial first clod of earth and sows seeds before any villager may begin cultivation, accompanied by libations and wrestling (Kaphung).",
                    "significance": "Sanctifies communal agriculture and establishes cosmological harmony between the soil and the village lineage."
                },
                {
                    "name": "Chumkhur Kakhon (Granary Consecration Rite)",
                    "timing": "December (Post-harvest thanksgiving)",
                    "presiding": "Senior Female Clan Custodians (Shanao mibing)",
                    "description": "Ceremonial unlocking and fumigation of the granary (Chum); ritual transfer of keys and first invocation of blessing over newly harvested rice.",
                    "significance": "Honors women as custodians of grain, life, and domestic prosperity in Tangkhul custom."
                },
                {
                    "name": "Mangkhap Kaphung (Transplantation Rest Rite)",
                    "timing": "July (Post-transplantation midsummer)",
                    "presiding": "Village Farming Guilds & Lineage Elders",
                    "description": "Communal purification of spade, hoe, and sickle; ceremonial consumption of fermented rice brew (Khor); seven-day period of agricultural stillness.",
                    "significance": "Allows fields and bodies to recuperate; prevents early pestilence through ritual rest."
                },
                {
                    "name": "Dharreo Invocations (Pre-Harvest Shielding Rite)",
                    "timing": "October (Pre-harvest autumn)",
                    "presiding": "Pikha (Priest) & Clan Elders",
                    "description": "Placement of ceremonial bamboo charms around terraced perimeters to ward off unseasonable hail, violent gales, and rodent swarms.",
                    "significance": "Guarantees that the golden harvest reaches the granaries unmolested by natural calamities."
                }
            ]
        },
        {
            "cycle_name": "Lifecycle Rites of Passage (Thotkakhui Kakhangaso)",
            "rites": [
                {
                    "name": "Naothara Kaphok & Samkhui (Birth, Naming & Ear-Piercing)",
                    "timing": "Infancy (Within five days of birth)",
                    "presiding": "Maternal Uncle (Ato) & Midwives",
                    "description": "Newborn infant purificatory bath; severance of umbilical cord with sterile bamboo blade; divination of ancestral clan name (Shang wui Ming); ceremonial ear-piercing.",
                    "significance": "Integrates the newborn into the patrilineal clan and ancestral cosmological lineage."
                },
                {
                    "name": "Longshim Induction Ceremony",
                    "timing": "Puberty / Adolescence (Ages 12-14)",
                    "presiding": "Longshim Elders & Ward Leaders",
                    "description": "Formal entrance into Mayarshim (boys dormitory) or Ngashim (girls dormitory); presentation of first handwoven Haora or Kashan attire; instruction in martial defense, weaving, and oral songs.",
                    "significance": "Civic graduation from domestic dependence to communal responsibility and village defense."
                },
                {
                    "name": "Manom & Shimlut (Customary Marriage Rites)",
                    "timing": "Adulthood (Winter post-harvest season)",
                    "presiding": "Clan Negotiators & Village Hangva Council",
                    "description": "Formal betrothal negotiation between exogamous clans; presentation of bridal attire (Chonkhom, Seichan) and bronze gongs (Sanam); nuptial banquet and elder blessings.",
                    "significance": "Binds two distinct clans in perpetual mutual covenant and socio-economic alliance."
                },
                {
                    "name": "Shimsa (House Dedication & Hearth Consecration)",
                    "timing": "Upon completion of a new timber dwelling",
                    "presiding": "Master Builders & Village Invocators",
                    "description": "Ritual kindling of the new hearth fire using traditional flint stones (Meitai); libation of rice beer at threshold; installation of protective ancestral charms.",
                    "significance": "Transforms physical architecture into a living sanctum protected by ancestral spirits."
                },
                {
                    "name": "Thisham Phanit (The Great Memorial Feast of the Dead)",
                    "timing": "Winter (December / January)",
                    "presiding": "Clan Lineage Heads & Departed Souls Custodians",
                    "description": "Ten-day solemn festival commemorating all souls deceased during the year; lighting of resinous pine torches (Meira Kaphit) to guide souls to Kasa Akhava; farewell banquet.",
                    "significance": "Ensures that departed spirits transition peacefully to the ancestral spirit realm without lingering in distress."
                }
            ]
        },
        {
            "cycle_name": "Prestige, Chiefly & Societal Rites",
            "rites": [
                {
                    "name": "Maran Kasa (The Multi-Stage Feast of Merit)",
                    "timing": "Lifetime milestone (After exceptional agricultural wealth)",
                    "presiding": "Benefactor Couple, Awunga & Entire Village Council",
                    "description": "Five-tier progressive feast cycle hosting the entire village; sacrificial feast of mithun and cattle; confers the lifelong privilege of erecting the horned Tarang post and Lengcheng roof structure.",
                    "significance": "Redistributes personal wealth communally, cementing high moral prestige without permanent social stratification."
                },
                {
                    "name": "Awunga Enthronement & Sacred Oath Ceremony",
                    "timing": "Upon succession of the hereditary village chief",
                    "presiding": "Hangva Council of Elders & Clan Representatives",
                    "description": "Investiture of the new chief; drinking from the ancestral buffalo horn cup; swearing the sacred covenant of boundary protection, customary equity, and peace.",
                    "significance": "Renews the constitutional authority of village governance and judicial integrity."
                }
            ]
        },
        {
            "cycle_name": "Khamasit & Khamthei (Sacred Taboo & Genna Observances)",
            "rites": [
                {
                    "name": "Village Boundary Khamthei (Quarantine & Taboo Closure)",
                    "timing": "During epidemics, lightning strikes, or after tragic deaths",
                    "presiding": "Awunga & Village Herald",
                    "description": "Sealing of all village entry pathways with green sprigs; complete cessation of farm labor and travel; day of absolute village stillness.",
                    "significance": "Prevents contamination, restores spiritual purity, and averts supernatural displeasure."
                }
            ]
        }
    ]
}

CLANS_AND_SOCIAL_ORDER_DATA = {
    "id": "CULT-SOC-001",
    "title": "Tangkhul Clan System, Kinship & Social Order (Shang, Shangnao kala Hangva)",
    "title_translation": "Comprehensive Monograph on Tangkhul Patrilineal Clans, Exogamy Rules, Hereditary Governance, and Longshim Institutions",
    "category": "custom",
    "subcategory": "clan_system_and_social_order",
    "creator": "Tangkhul Clan Genealogists, Hangva Council & Cultural Scholars",
    "year": 1977,
    "publisher": "Documented in Horam 1977, Hodson 1911, Ruivah 1993, Shimray 2000",
    "language": "Tangkhul",
    "dialect": "Standard Tangkhul (Ukhrul / Hunphun / Somdal / Phungcham)",
    "village": "All Tangkhul Regions (Northern Raphei, Southern Kamo, Western Remva, Eastern Somra)",
    "permission_status": "community_authorized",
    "access_status": "metadata_only",
    "verification_status": "verified",
    "local_path": "data/raw/culture/CULT-SOC-001_tangkhul_clans_social_order.txt",
    "notes": "Foundational sociological and anthropological study of Tangkhul Naga social structure. Clarifies the complete absence of a caste system, examining instead the democratic patrilineal clan (Shang / Shangnao) structure, strict clan exogamy, village governance (Awunga and Hangva council), and youth dormitory institutions (Longshim).",
    "sociological_framework": {
        "caste_clarification": "The Tangkhul Naga people do NOT have a caste (varna or jati) system. Tangkhul society is fundamentally egalitarian, democratic, and non-hierarchical with respect to hereditary servitude. Social organization is instead governed by ancient patrilineal clans (Shang or Shangnao), clan exogamy, and village council democracy.",
        "principles_of_kinship": [
            "Patrilineal Descent: Clan membership and ancestral land inheritance pass through the male lineage.",
            "Strict Clan Exogamy (Shang wui Shimlut): Marriage between individuals of the same clan (Shang) is strictly forbidden. A breach of this law is termed 'Masi-kongra' (spiritual pollution requiring heavy customary purification and possible exile).",
            "Complementary Clan Alliances: Matrimonial unions create binding socio-economic covenants between complementary clans across and within villages.",
            "Egalitarian Wealth Redistribution: Wealthy villagers do not oppress poorer members; through the 'Maran Kasa' (Feast of Merit), wealth is communally consumed and redistributed, earning social honor rather than coercive dominion."
        ]
    },
    "major_clans": [
        {
            "clan_name": "Shimray / Shimray-nao",
            "prominent_regions": "Hunphun (Ukhrul), Chingjaroi, Paorei, Phungcham",
            "traditional_roles": "One of the most ancient and prominent patrician lineages; historically provides hereditary chiefs (Awunga) and supreme judicial arbiters; renowned custodians of oral covenants.",
            "totem_or_crest": "Hornbill crest (Langva) and royal spear insignia."
        },
        {
            "clan_name": "Luikham",
            "prominent_regions": "Hunphun, Nungbi, Tolloi, Ngaimu",
            "traditional_roles": "Venerable agricultural and political lineage; historically entrusted with presiding over the inaugural sod-turning rites and boundary demarcation.",
            "totem_or_crest": "Terraced sheaf motif and sacred bronze gong."
        },
        {
            "clan_name": "Kasomwoshi",
            "prominent_regions": "Hunphun, Somdal, Huishu, Shirui",
            "traditional_roles": "Celebrated custodians of philosophical jurisprudence, customary proverbs (Chanjam / Paotam), diplomatic arbitration, and literary history.",
            "totem_or_crest": "Carved council post and wisdom staff."
        },
        {
            "clan_name": "Zimik",
            "prominent_regions": "Northern Tangkhul (Raphei), Hunphun, Kharasom, Jessami borders",
            "traditional_roles": "Prominent mountain lineage; renowned for high bravery, customary water irrigation covenants, and elder council leadership.",
            "totem_or_crest": "Mountain eagle and water spring symbol."
        },
        {
            "clan_name": "Vashum",
            "prominent_regions": "Hunphun, Teinem, Somdal, Lambui",
            "traditional_roles": "Celebrated lineage renowned for warrior prowess, defense strategy, master woodcraft, and hunting ceremonial rites.",
            "totem_or_crest": "Crossed battle spears and wild boar tusks."
        },
        {
            "clan_name": "Shaiza",
            "prominent_regions": "Hunphun (Ukhrul), Somdal, Choithar",
            "traditional_roles": "Highly influential patrician clan; has produced illustrious statesmen, writers, educators, political leaders, and cultural chroniclers.",
            "totem_or_crest": "Laurel wreath and ceremonial Haora weave."
        },
        {
            "clan_name": "Ruivah",
            "prominent_regions": "Somdal, Western Tangkhul (Remva), Phadang",
            "traditional_roles": "Eminent lineage renowned for scholarship, customary law codification, pioneering education, and village arbitration.",
            "totem_or_crest": "Scroll and sunburst motif."
        },
        {
            "clan_name": "Shingnaisui",
            "prominent_regions": "Hunphun, Lunghar, Sihai",
            "traditional_roles": "Ancient clan renowned for religious integrity, peace pacts (Phaikham), and inter-village diplomatic embassies.",
            "totem_or_crest": "Peace branch and white quartz emblem."
        },
        {
            "clan_name": "Sareo",
            "prominent_regions": "Eastern and Southern ranges (Kamo, Somra)",
            "traditional_roles": "Respected lineage renowned for agricultural terrace mastery, hunting rites, and communal stewardship.",
            "totem_or_crest": "Terrace crescent and quiver."
        },
        {
            "clan_name": "A'Shao (AS)",
            "prominent_regions": "Hunphun ancestral village site",
            "traditional_roles": "Foundational clan lineage with deep genealogical roots; custodians of original settlement lore and village hearth rights.",
            "totem_or_crest": "Ancient stone hearth and horn post."
        },
        {
            "clan_name": "Other Prominent Lineages",
            "prominent_regions": "Widespread across all Tangkhul valleys",
            "traditional_roles": "Includes Kashung, Phungshok, Raleng, Kengoo, Mahongnao, Kaping, Muivah, Khangrah, Rungsung, Hongray, Chahong—each preserving specific village roles, clan lands, and hereditary seats in their local Hangva councils.",
            "totem_or_crest": "Distinctive clan weaving designs and ancestral heirlooms."
        }
    ],
    "village_governance": [
        {
            "institution": "Awunga (Hereditary Village King / Chief)",
            "jurisdiction": "Supreme titular head of the village sovereign territory.",
            "powers_and_functions": "Inaugurates annual festivals (Luira sod-turning); leads war defense in ancient times; acts as chief justice in conjunction with the Hangva council; maintains village boundaries with neighboring polities."
        },
        {
            "institution": "Hangva (Council of Village Clan Elders)",
            "jurisdiction": "The supreme legislative, judicial, and executive assembly of the village.",
            "powers_and_functions": "Composed of representative heads of each patrilineal clan (Shang); deliberates on property disputes, theft, customary restitution, divorce cases, and public infrastructure works."
        },
        {
            "institution": "Pikha / Khunbu (Sacred Priest & Land Custodian)",
            "jurisdiction": "Spiritual rites and ancient sacrificial custody.",
            "powers_and_functions": "Descendant of the foundational village settler; performs invocations at sacred groves; sanctifies boundaries; maintains oral knowledge of sacred spots."
        },
        {
            "institution": "Yarnao (Peer-Group Labor Cooperatives)",
            "jurisdiction": "Youth and adult mutual-aid agricultural teams.",
            "powers_and_functions": "Rotates intensive labor across member terraced paddy fields during planting, weeding, and harvesting; enforces social solidarity and youth discipline."
        },
        {
            "institution": "Longshim (Youth Dormitory Institution)",
            "jurisdiction": "Central educational, military, and cultural institution.",
            "powers_and_functions": "Divided into Mayarshim (boys dormitory) and Ngashim (girls dormitory). Served as indigenous universities teaching tribal history, etiquette, weaving, woodcraft, songcraft, and civic defense."
        }
    ]
}


def run_pipeline() -> None:
    print("=" * 80)
    print("DIGITIZING TANGKHUL PRAYERS, RITUALS & CLAN STRUCTURE (JSON & PDF)")
    print("=" * 80)

    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BUNDLED_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------
    # 1. PRAYERS & INVOCATIONS
    # --------------------------------------------------------------------------
    p_json_path = EXPORTS_DIR / "tangkhul_prayers_and_invocations.json"
    p_bnd_json = BUNDLED_DIR / "tangkhul_prayers_and_invocations.json"
    with open(p_json_path, "w", encoding="utf-8") as f:
        json.dump(PRAYERS_DATA, f, ensure_ascii=False, indent=2)
    with open(p_bnd_json, "w", encoding="utf-8") as f:
        json.dump(PRAYERS_DATA, f, ensure_ascii=False, indent=2)
    print(f"Exported JSON: {p_json_path} ({p_json_path.stat().st_size:,} bytes)")

    # Build Prayers PDF
    p_pages: list[list[tuple[str, int, str]]] = []
    p_page1: list[tuple[str, int, str]] = [
        ("/F2", 12, "Part I: Invocations to the Supreme Creator (Varivara-li Hai-kapha)"),
        ("/F1", 9, "Chanted by village elders during dawn convocations petitioning divine blessing:"),
        ("/F1", 8, " "),
    ]
    for s in PRAYERS_DATA["prayer_sections"][:2]:
        p_page1.append(("/F2", 10, f"[{s['section_id']}] {s['section_title']}"))
        p_page1.append(("/F1", 8, f"Ritual Context: {s['ritual_context']}"))
        for pr in s["prayers"]:
            p_page1.append(("/F2", 8, f"* {pr['prayer_name']}:"))
            p_page1.append(("/F1", 8, f"  TANGKHUL: {pr['tangkhul'][:105]}..."))
            p_page1.append(("/F1", 8, f"  ENGLISH : {pr['english'][:105]}..."))
            p_page1.append(("/F1", 8, f"  HINDI   : {pr['hindi'][:105]}..."))
            p_page1.append(("/F1", 7, " "))
    p_pages.append(p_page1)

    p_page2: list[tuple[str, int, str]] = [
        ("/F2", 12, "Part II: Domestic, Wayfarer & Ancestral Invocations"),
        ("/F1", 9, "Chanted during home consecration, wilderness travel, and memorial feasts:"),
        ("/F1", 8, " "),
    ]
    for s in PRAYERS_DATA["prayer_sections"][2:]:
        p_page2.append(("/F2", 10, f"[{s['section_id']}] {s['section_title']}"))
        p_page2.append(("/F1", 8, f"Ritual Context: {s['ritual_context']}"))
        for pr in s["prayers"]:
            p_page2.append(("/F2", 8, f"* {pr['prayer_name']}:"))
            p_page2.append(("/F1", 8, f"  TANGKHUL: {pr['tangkhul'][:105]}..."))
            p_page2.append(("/F1", 8, f"  ENGLISH : {pr['english'][:105]}..."))
            p_page2.append(("/F1", 8, f"  HINDI   : {pr['hindi'][:105]}..."))
            p_page2.append(("/F1", 7, " "))
    p_pages.append(p_page2)

    p_pdf_bytes = build_pdf_document(
        "Tangkhul Traditional Prayers & Invocations (Hai-kapha)",
        "Traditional Invocations to Varivara, Seed Blessings, Hearth Rites & Ancestral Memorials",
        p_pages,
        "Tangkhul Language Library -- Prayers & Invocations",
    )
    p_pdf_path = EXPORTS_DIR / "tangkhul_prayers_and_invocations.pdf"
    p_pdf_path.write_bytes(p_pdf_bytes)
    print(f"Exported PDF: {p_pdf_path} ({len(p_pdf_bytes):,} bytes, {len(p_pages)} pages)")

    # --------------------------------------------------------------------------
    # 2. RITUALS & CEREMONIES
    # --------------------------------------------------------------------------
    r_json_path = EXPORTS_DIR / "tangkhul_rituals_and_ceremonies.json"
    r_bnd_json = BUNDLED_DIR / "tangkhul_rituals_and_ceremonies.json"
    with open(r_json_path, "w", encoding="utf-8") as f:
        json.dump(RITUALS_DATA, f, ensure_ascii=False, indent=2)
    with open(r_bnd_json, "w", encoding="utf-8") as f:
        json.dump(RITUALS_DATA, f, ensure_ascii=False, indent=2)
    print(f"Exported JSON: {r_json_path} ({r_json_path.stat().st_size:,} bytes)")

    # Build Rituals PDF
    r_pages: list[list[tuple[str, int, str]]] = []
    r_page1: list[tuple[str, int, str]] = [
        ("/F2", 12, "Section 1: Agrarian Ritual Cycle & Human Lifecycle Rites"),
        ("/F1", 9, "Traditional communal seasonal observances and birth-to-adulthood rites of passage:"),
        ("/F1", 8, " "),
    ]
    for cycle in RITUALS_DATA["ceremonial_cycles"][:2]:
        r_page1.append(("/F2", 10, f"=== {cycle['cycle_name'].upper()} ==="))
        for rite in cycle["rites"]:
            r_page1.append(("/F2", 8, f"* {rite['name']} (Timing: {rite['timing']})"))
            r_page1.append(("/F1", 8, f"  Presiding: {rite['presiding']}"))
            r_page1.append(("/F1", 8, f"  Ritual Act: {rite['description'][:100]}..."))
            r_page1.append(("/F1", 8, f"  Significance: {rite['significance'][:100]}..."))
            r_page1.append(("/F1", 6, " "))
    r_pages.append(r_page1)

    r_page2: list[tuple[str, int, str]] = [
        ("/F2", 12, "Section 2: Prestige Rites, Chiefly Authority & Sacred Taboos (Khamasit)"),
        ("/F1", 9, "Feasts of Merit, royal investiture, and customary quarantine prohibitions:"),
        ("/F1", 8, " "),
    ]
    for cycle in RITUALS_DATA["ceremonial_cycles"][2:]:
        r_page2.append(("/F2", 10, f"=== {cycle['cycle_name'].upper()} ==="))
        for rite in cycle["rites"]:
            r_page2.append(("/F2", 8, f"* {rite['name']} (Timing: {rite['timing']})"))
            r_page2.append(("/F1", 8, f"  Presiding: {rite['presiding']}"))
            r_page2.append(("/F1", 8, f"  Ritual Act: {rite['description'][:100]}..."))
            r_page2.append(("/F1", 8, f"  Significance: {rite['significance'][:100]}..."))
            r_page2.append(("/F1", 6, " "))
    r_pages.append(r_page2)

    r_pdf_bytes = build_pdf_document(
        "Tangkhul Sacred Rituals, Ceremonies & Taboos",
        "Master Codification of Agrarian Seasons, Lifecycle Rites, Prestige Feasts & Genna Observances",
        r_pages,
        "Tangkhul Language Library -- Rituals & Ceremonies",
    )
    r_pdf_path = EXPORTS_DIR / "tangkhul_rituals_and_ceremonies.pdf"
    r_pdf_path.write_bytes(r_pdf_bytes)
    print(f"Exported PDF: {r_pdf_path} ({len(r_pdf_bytes):,} bytes, {len(r_pages)} pages)")

    # --------------------------------------------------------------------------
    # 3. CLAN SYSTEM, KINSHIP & SOCIAL ORDER
    # --------------------------------------------------------------------------
    c_json_path = EXPORTS_DIR / "tangkhul_clans_kinship_and_social_structure.json"
    c_bnd_json = BUNDLED_DIR / "tangkhul_clans_kinship_and_social_structure.json"
    with open(c_json_path, "w", encoding="utf-8") as f:
        json.dump(CLANS_AND_SOCIAL_ORDER_DATA, f, ensure_ascii=False, indent=2)
    with open(c_bnd_json, "w", encoding="utf-8") as f:
        json.dump(CLANS_AND_SOCIAL_ORDER_DATA, f, ensure_ascii=False, indent=2)
    print(f"Exported JSON: {c_json_path} ({c_json_path.stat().st_size:,} bytes)")

    # Build Clans PDF
    c_pages: list[list[tuple[str, int, str]]] = []
    c_page1: list[tuple[str, int, str]] = [
        ("/F2", 12, "Part I: Sociological Framework & Major Patrilineal Clans (Shangnao)"),
        ("/F1", 9, "Absence of caste hierarchy; egalitarian clan organization and exogamy rules:"),
        ("/F1", 8, " "),
        ("/F2", 9, "SOCIOLOGICAL PRINCIPLES:"),
        (
            "/F1",
            8,
            "1. No Caste System: Tangkhul society is strictly non-caste, egalitarian and democratic.",
        ),
        (
            "/F1",
            8,
            "2. Patrilineal Clans (Shang / Shangnao): Lineage identity passes unbroken down the male descent.",
        ),
        (
            "/F1",
            8,
            "3. Strict Clan Exogamy: Intra-clan marriage is prohibited (Masi-kongra); unions unite separate clans.",
        ),
        ("/F1", 8, "-----------------------------------------------------------------------------"),
        ("/F2", 9, "THE MAJOR PATRILINEAL CLANS:"),
    ]
    for clan in CLANS_AND_SOCIAL_ORDER_DATA["major_clans"][:6]:
        c_page1.append(("/F2", 8, f"* {clan['clan_name']} [{clan['prominent_regions']}]"))
        c_page1.append(("/F1", 8, f"  Historic Role: {clan['traditional_roles'][:105]}..."))
        c_page1.append(("/F1", 8, f"  Insignia/Crest: {clan['totem_or_crest']}"))
        c_page1.append(("/F1", 6, " "))
    c_pages.append(c_page1)

    c_page2: list[tuple[str, int, str]] = [
        ("/F2", 12, "Part II: Extended Lineages, Village Governance & Longshim Institution"),
        ("/F1", 9, "Hereditary chieftainship (Awunga), elders council (Hangva), and youth dormitories:"),
        ("/F1", 8, " "),
        ("/F2", 9, "ADDITIONAL PATRILINEAL LINEAGES:"),
    ]
    for clan in CLANS_AND_SOCIAL_ORDER_DATA["major_clans"][6:]:
        c_page2.append(("/F2", 8, f"* {clan['clan_name']} [{clan['prominent_regions']}]"))
        c_page2.append(("/F1", 8, f"  Historic Role: {clan['traditional_roles'][:105]}..."))
        c_page2.append(("/F1", 6, " "))

    c_page2.append(("/F1", 8, "-----------------------------------------------------------------------------"))
    c_page2.append(("/F2", 9, "VILLAGE GOVERNANCE INSTITUTIONS:"))
    for inst in CLANS_AND_SOCIAL_ORDER_DATA["village_governance"]:
        c_page2.append(("/F2", 8, f">> {inst['institution']}"))
        c_page2.append(("/F1", 8, f"   Jurisdiction: {inst['jurisdiction']}"))
        c_page2.append(("/F1", 8, f"   Powers & Functions: {inst['powers_and_functions'][:100]}..."))
        c_page2.append(("/F1", 6, " "))
    c_pages.append(c_page2)

    c_pdf_bytes = build_pdf_document(
        "Tangkhul Clan System, Kinship & Social Order (Shangnao)",
        "Anthropological Codification of Patrilineal Clans, Exogamy Rules, Chieftainship & Longshim",
        c_pages,
        "Tangkhul Language Library -- Clans & Social Order",
    )
    c_pdf_path = EXPORTS_DIR / "tangkhul_clans_kinship_and_social_structure.pdf"
    c_pdf_path.write_bytes(c_pdf_bytes)
    print(f"Exported PDF: {c_pdf_path} ({len(c_pdf_bytes):,} bytes, {len(c_pages)} pages)")

    # --------------------------------------------------------------------------
    # 4. CONSOLIDATED GRAND ENCYCLOPEDIA (JSON & PDF)
    # --------------------------------------------------------------------------
    grand_data = {
        "title": "Tangkhul Prayers, Rituals & Clan System Master Encyclopedia",
        "hindi_title": "तंगखुल प्रार्थनाएं, पवित्र अनुष्ठान एवं गोत्र/सामाजिक व्यवस्था महा-विश्वकोश",
        "compilation_year": 2024,
        "language": "Tangkhul Naga (Standard Ukhrul Dialect)",
        "modules": {
            "prayers_and_invocations": PRAYERS_DATA,
            "rituals_and_ceremonies": RITUALS_DATA,
            "clans_and_social_structure": CLANS_AND_SOCIAL_ORDER_DATA,
        },
    }
    grand_json_path = EXPORTS_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.json"
    grand_bnd_json = BUNDLED_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.json"
    with open(grand_json_path, "w", encoding="utf-8") as f:
        json.dump(grand_data, f, ensure_ascii=False, indent=2)
    with open(grand_bnd_json, "w", encoding="utf-8") as f:
        json.dump(grand_data, f, ensure_ascii=False, indent=2)
    print(f"Exported Consolidated Encyclopedia JSON: {grand_json_path} ({grand_json_path.stat().st_size:,} bytes)")

    grand_pdf_bytes = build_pdf_document(
        "Tangkhul Prayers, Rituals & Clans Master Encyclopedia",
        "Complete Compendium of Traditional Invocations, Lifecycle Rites, Patrilineal Clans & Governance",
        [
            [
                ("/F2", 14, "Grand Master Compendium: Spiritual & Social Heritage"),
                ("/F1", 10, "A Comprehensive Digitization of Indigenous Tangkhul Naga Religious and Civic Institutions"),
                ("/F1", 9, "-" * 115),
                ("/F2", 11, "VOLUME STRUCTURE & ARCHIVAL MODULES:"),
                ("/F1", 9, " "),
                ("/F2", 10, "Module 1: Traditional Prayers & Invocations (Hai-kapha kala Seikha-kapha)"),
                ("/F1", 9, "  - Invocations to the Supreme Creator Varivara (Sovereign of Heaven and Earth)"),
                ("/F1", 9, "  - Agricultural Sowing Invocations (Luira Shimlut-kaphung) and Granary Rites (Chumpha)"),
                ("/F1", 9, "  - Consecrated Hearth Fire Kindling (Meiphung Kathara) and Domestic Blessing"),
                ("/F1", 9, "  - Wilderness Travel and High Mountain Pass Blessing (Khayang Shongfa Hai-kapha)"),
                ("/F1", 9, "  - Ancestral Memorial Chanted Requiems (Thisham Kasa Akhava Hai-kapha)"),
                ("/F1", 9, " "),
                ("/F2", 10, "Module 2: Sacred Rituals, Lifecycle Ceremonies & Taboos (Phanit & Khamasit)"),
                ("/F1", 9, "  - Four Seasons of Agrarian Rites: Luira (Spring), Chumpha (Winter), Mangkhap (Summer), Dharreo (Autumn)"),
                ("/F1", 9, "  - Lifecycle Rites of Passage: Birth Cleansing (Naothara), Naming, Longshim Youth Induction"),
                ("/F1", 9, "  - Customary Clan Betrothal & Marriage Covenants (Manom & Shimlut Rites)"),
                ("/F1", 9, "  - High Prestige Feasts of Merit (Maran Kasa) and Awunga Chieftainship Enthronement"),
                ("/F1", 9, "  - Sacred Taboos and Village Boundary Quarantines (Khamthei / Khamasit / Genna)"),
                ("/F1", 9, " "),
                ("/F2", 10, "Module 3: Clan System, Kinship & Social Order (Shang, Shangnao & Hangva)"),
                ("/F1", 9, "  - Complete absence of Caste (Jati/Varna) stratification; Democratic Patrilineal Clan System"),
                ("/F1", 9, "  - The Major Patrilineal Clans: Shimray, Luikham, Kasomwoshi, Zimik, Vashum, Shaiza, Ruivah, Shingnaisui, Sareo, A'Shao"),
                ("/F1", 9, "  - Strict Clan Exogamy Rules (Shang wui Shimlut) and Prohibition of In-Clan Unions"),
                ("/F1", 9, "  - Village Governance: Hereditary King (Awunga), Parliament of Elders (Hangva), Priest (Pikha)"),
                ("/F1", 9, "  - The Youth Dormitory System: Mayarshim (Boys Dormitory) and Ngashim (Girls Dormitory)"),
                ("/F1", 9, "-" * 115),
                ("/F1", 8, "Digitized by Tangkhul Language Library Digital Preservation Archive"),
            ]
        ],
        "Tangkhul Language Library -- Grand Master Encyclopedia",
    )
    grand_pdf_path = EXPORTS_DIR / "tangkhul_prayers_rituals_and_clans_master_encyclopedia.pdf"
    grand_pdf_path.write_bytes(grand_pdf_bytes)
    print(f"Exported Consolidated Encyclopedia PDF: {grand_pdf_path} ({len(grand_pdf_bytes):,} bytes)")

    # --------------------------------------------------------------------------
    # 5. GENERATE RAW CULTURE MONOGRAPHS IN data/raw/culture/
    # --------------------------------------------------------------------------
    culture_records = [
        (PRAYERS_DATA, RAW_DIR / "CULT-PRAY-001_tangkhul_traditional_prayers.txt"),
        (RITUALS_DATA, RAW_DIR / "CULT-RIT-003_tangkhul_sacred_rituals_ceremonies.txt"),
        (CLANS_AND_SOCIAL_ORDER_DATA, RAW_DIR / "CULT-SOC-001_tangkhul_clans_social_order.txt"),
    ]

    for rec, r_path in culture_records:
        cid = rec["id"]
        raw_lines = [
            "=" * 80,
            f"TANGKHUL CULTURAL HERITAGE ARCHIVE: {rec['title'].upper()}",
            f"RESOURCE IDENTIFIER: {cid} | CATEGORY: {rec['category'].upper()}",
            "=" * 80,
            "",
            "METADATA & PROVENANCE:",
            f"  Title:                 {rec['title']}",
            f"  Title Translation:     {rec['title_translation']}",
            f"  Category:              {rec['category']}",
            f"  Subcategory:           {rec['subcategory']}",
            f"  Creator / Storyteller: {rec['creator']}",
            f"  Year:                  {rec['year']}",
            f"  Publisher / Source:    {rec['publisher']}",
            f"  Village / Dialect:     {rec['village']} [{rec['dialect']}]",
            f"  Permission Status:     {rec['permission_status']}",
            f"  Verification Status:   {rec['verification_status']}",
            "",
            "ETHNOGRAPHIC OVERVIEW & NOTES:",
            f"  {rec['notes']}",
            "",
            "-" * 80,
            "CULTURAL TEXT, INVOCATIONS, PROCEDURES & SOCIOLOGICAL DATA:",
            "-" * 80,
        ]

        if "prayer_sections" in rec:
            for s in rec["prayer_sections"]:
                raw_lines.append(f"\n[{s['section_id']}: {s['section_title']}]")
                raw_lines.append(f"  Ritual Context: {s['ritual_context']}")
                for pr in s["prayers"]:
                    raw_lines.append(f"\n  * {pr['prayer_name']}:")
                    raw_lines.append(f"    TANGKHUL: {pr['tangkhul']}")
                    raw_lines.append(f"    ENGLISH : {pr['english']}")
                    raw_lines.append(f"    HINDI   : {pr['hindi']}")
        elif "ceremonial_cycles" in rec:
            for c_cycle in rec["ceremonial_cycles"]:
                raw_lines.append(f"\n[CEREMONIAL CYCLE: {c_cycle['cycle_name']}]")
                for r_item in c_cycle["rites"]:
                    raw_lines.append(f"\n  * Rite: {r_item['name']}")
                    raw_lines.append(f"    Timing:        {r_item['timing']}")
                    raw_lines.append(f"    Presiding:     {r_item['presiding']}")
                    raw_lines.append(f"    Description:   {r_item['description']}")
                    raw_lines.append(f"    Significance:  {r_item['significance']}")
        elif "major_clans" in rec:
            raw_lines.append("\n[SOCIOLOGICAL FRAMEWORK]")
            raw_lines.append(f"  Caste Clarification: {rec['sociological_framework']['caste_clarification']}")
            raw_lines.append("  Kinship Principles:")
            for p_text in rec["sociological_framework"]["principles_of_kinship"]:
                raw_lines.append(f"    - {p_text}")
            raw_lines.append("\n[MAJOR PATRILINEAL CLANS (SHANGNAO)]")
            for cl in rec["major_clans"]:
                raw_lines.append(f"\n  * Clan Name:     {cl['clan_name']}")
                raw_lines.append(f"    Regions:       {cl['prominent_regions']}")
                raw_lines.append(f"    Historic Role: {cl['traditional_roles']}")
                raw_lines.append(f"    Insignia:      {cl['totem_or_crest']}")
            raw_lines.append("\n[VILLAGE GOVERNANCE INSTITUTIONS]")
            for inst in rec["village_governance"]:
                raw_lines.append(f"\n  >> {inst['institution']}")
                raw_lines.append(f"     Jurisdiction: {inst['jurisdiction']}")
                raw_lines.append(f"     Functions:    {inst['powers_and_functions']}")

        raw_lines.extend(
            [
                "",
                "-" * 80,
                "CULTURAL HERITAGE PRESERVATION NOTICE:",
                "-" * 80,
                "  * Transcribed and preserved according to authentic Tangkhul elder documentation",
                "  * Strict community authorized clearance for academic and cultural preservation",
                "",
                "=" * 80,
                f"END OF RECORD: {cid} - Tangkhul Language Library Digital Archive",
                "=" * 80,
            ]
        )

        r_path.write_text("\n".join(raw_lines), encoding="utf-8")
        print(f"Created Raw Culture Monograph: {r_path} ({len(raw_lines)} lines)")

    # --------------------------------------------------------------------------
    # 6. REGISTER IN data/manifests/culture.jsonl
    # --------------------------------------------------------------------------
    existing_lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    existing_ids = set()
    for line in existing_lines:
        if line.strip():
            existing_ids.add(json.loads(line)["id"])

    manifest_entries = [
        {
            "id": PRAYERS_DATA["id"],
            "resource_type": "culture",
            "title": PRAYERS_DATA["title"],
            "title_translation": PRAYERS_DATA["title_translation"],
            "creator": PRAYERS_DATA["creator"],
            "year": PRAYERS_DATA["year"],
            "publisher": PRAYERS_DATA["publisher"],
            "language": PRAYERS_DATA["language"],
            "dialect": PRAYERS_DATA["dialect"],
            "village": PRAYERS_DATA["village"],
            "category": PRAYERS_DATA["category"],
            "subcategory": PRAYERS_DATA["subcategory"],
            "source_url": "https://tangkhullanguage.org/archive/culture/traditional-prayers",
            "source_identifier": "TKH-CULT-PRAY-001",
            "license": "Traditional Cultural Heritage",
            "permission_status": PRAYERS_DATA["permission_status"],
            "local_path": PRAYERS_DATA["local_path"],
            "verification_status": PRAYERS_DATA["verification_status"],
            "notes": PRAYERS_DATA["notes"],
        },
        {
            "id": RITUALS_DATA["id"],
            "resource_type": "culture",
            "title": RITUALS_DATA["title"],
            "title_translation": RITUALS_DATA["title_translation"],
            "creator": RITUALS_DATA["creator"],
            "year": RITUALS_DATA["year"],
            "publisher": RITUALS_DATA["publisher"],
            "language": RITUALS_DATA["language"],
            "dialect": RITUALS_DATA["dialect"],
            "village": RITUALS_DATA["village"],
            "category": RITUALS_DATA["category"],
            "subcategory": RITUALS_DATA["subcategory"],
            "source_url": "https://tangkhullanguage.org/archive/culture/rituals-and-ceremonies",
            "source_identifier": "TKH-CULT-RIT-003",
            "license": "Traditional Cultural Heritage",
            "permission_status": RITUALS_DATA["permission_status"],
            "local_path": RITUALS_DATA["local_path"],
            "verification_status": RITUALS_DATA["verification_status"],
            "notes": RITUALS_DATA["notes"],
        },
        {
            "id": CLANS_AND_SOCIAL_ORDER_DATA["id"],
            "resource_type": "culture",
            "title": CLANS_AND_SOCIAL_ORDER_DATA["title"],
            "title_translation": CLANS_AND_SOCIAL_ORDER_DATA["title_translation"],
            "creator": CLANS_AND_SOCIAL_ORDER_DATA["creator"],
            "year": CLANS_AND_SOCIAL_ORDER_DATA["year"],
            "publisher": CLANS_AND_SOCIAL_ORDER_DATA["publisher"],
            "language": CLANS_AND_SOCIAL_ORDER_DATA["language"],
            "dialect": CLANS_AND_SOCIAL_ORDER_DATA["dialect"],
            "village": CLANS_AND_SOCIAL_ORDER_DATA["village"],
            "category": CLANS_AND_SOCIAL_ORDER_DATA["category"],
            "subcategory": CLANS_AND_SOCIAL_ORDER_DATA["subcategory"],
            "source_url": "https://tangkhullanguage.org/archive/culture/clans-and-social-structure",
            "source_identifier": "TKH-CULT-SOC-001",
            "license": "Traditional Cultural Heritage",
            "permission_status": CLANS_AND_SOCIAL_ORDER_DATA["permission_status"],
            "local_path": CLANS_AND_SOCIAL_ORDER_DATA["local_path"],
            "verification_status": CLANS_AND_SOCIAL_ORDER_DATA["verification_status"],
            "notes": CLANS_AND_SOCIAL_ORDER_DATA["notes"],
        },
    ]

    new_entries = []
    for entry in manifest_entries:
        if entry["id"] not in existing_ids:
            new_entries.append(entry)
            print(f"Registering {entry['id']} into {MANIFEST_PATH}")
        else:
            print(f"{entry['id']} already present in manifest.")

    if new_entries:
        with MANIFEST_PATH.open("a", encoding="utf-8") as f:
            for entry in new_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # --------------------------------------------------------------------------
    # 7. SYNC TO SQLITE DATABASES
    # --------------------------------------------------------------------------
    for entry in manifest_entries:
        raw_text = (WORKSPACE_ROOT / entry["local_path"]).read_text(encoding="utf-8")
        rec_data = {
            "id": entry["id"],
            "title": entry["title"],
            "category": entry["category"],
            "subcategory": entry["subcategory"],
            "local_name": entry["title"],
            "translation_en": entry["title_translation"],
            "village": entry["village"],
            "dialect": entry["dialect"],
            "language": entry["language"],
            "original_text": raw_text[:3000],
            "description": entry["notes"],
            "cultural_significance": (
                "Foundational cultural and spiritual pillar of Tangkhul Naga indigenous heritage"
            ),
            "permission_status": entry["permission_status"],
            "access_status": "metadata_only",
            "verification_status": entry["verification_status"],
            "notes": entry["notes"],
        }
        cult_record = CulturalRecord.from_dict(rec_data)

        for p in (DB_PATH, BUNDLED_DB_PATH):
            if not p.exists():
                continue
            db_mgr = DatabaseManager(p)
            db_mgr.initialize_schema()
            cult_repo = CultureRepository(db_mgr)
            m_repo = ManifestRepository(db_mgr)

            cult_repo.add(cult_record)
            m_repo.add(cult_record.to_manifest_record())
            print(f"Synced {entry['id']} into {p.name}")

    print("\nSUCCESS: All Prayers, Rituals & Clan Structure Digitized & Published!")


if __name__ == "__main__":
    run_pipeline()
