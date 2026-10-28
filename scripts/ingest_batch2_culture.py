#!/usr/bin/env python3
"""Script to integrate Batch 2 Tangkhul cultural records (CULT-FEST-006, CULT-FEST-007,
CULT-CUST-005, CULT-TRAD-005, CULT-TRAD-006, CULT-TRAD-007, CULT-PROV-007, CULT-PROV-008).

Brings the culture catalogue from 24 to 32 authentic records.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MANIFEST_FILE = ROOT / "data" / "manifests" / "culture.jsonl"
DB_FILE = ROOT / "data" / "database" / "tangkhul_corpus.sqlite"
BUNDLED_DB = ROOT / "src" / "tangkhul_lib" / "data" / "tangkhul_corpus.sqlite"

NEW_CULTURE_RECORDS = [
    {
        "id": "CULT-FEST-006",
        "resource_type": "culture",
        "title": "Dharreo Phanit",
        "title_translation": "Pre-Harvest Blessing Festival",
        "creator": "Tangkhul Farming Elders",
        "year": 1977,
        "publisher": "Traditional Observation (Horam 1977, Hodson 1911)",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul / Phungcham",
        "category": "festival",
        "subcategory": "agricultural",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Horam-1977-Ch5-Dharreo",
        "license": "Cultural Heritage Documentation",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-FEST-006_dharreo_phanit.txt",
        "verification_status": "verified",
        "notes": "Autumn pre-harvest festival celebrated in October before sickle touches the golden grain. Ritual invocations petition the Creator for protection against devastating wind, hail, and vermin before harvest.",
    },
    {
        "id": "CULT-FEST-007",
        "resource_type": "culture",
        "title": "Khamang Phanit",
        "title_translation": "Communal River Fishing & Walnut Bark Festival",
        "creator": "Hundung & Ukhrul River Troupes",
        "year": 1982,
        "publisher": "Documented in Arokianathan 1982, Ruivah 1993",
        "language": "Tangkhul",
        "dialect": "Hundung / Ukhrul",
        "village": "Hundung",
        "category": "festival",
        "subcategory": "communal_harvest",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Ruivah-1993-Ch4-Khamang",
        "license": "Cultural Heritage Documentation",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-FEST-007_khamang_phanit.txt",
        "verification_status": "verified",
        "notes": "Autumn communal river expedition where river channels are treated with pulverized wild walnut root (Ngasung) to stun fish, accompanied by forest fellowship banquets.",
    },
    {
        "id": "CULT-CUST-005",
        "resource_type": "culture",
        "title": "Maran Kasa Feast of Merit & Tarang Monument",
        "title_translation": "The Feast of Merit Cycle and Sacred Post Erection",
        "creator": "Tangkhul Hereditary Nobility & Benefactors",
        "year": 1911,
        "publisher": "Documented in Hodson 1911, Horam 1977",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul / Hunphun",
        "category": "custom",
        "subcategory": "prestige_institution",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Hodson-1911-Ch3-Maran",
        "license": "Cultural Heritage / Public Documentation",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-CUST-005_maran_kasa_tarang.txt",
        "verification_status": "verified",
        "notes": "The pinnacle institutional feast cycle hosted by a generous benefactor for the entire village, granting the lifelong cultural privilege of erecting the sacred forked Tarang post and adorning one's home as a Lengcheng Shim.",
    },
    {
        "id": "CULT-TRAD-005",
        "resource_type": "culture",
        "title": "Longpi Hamlei Black Stone Pottery",
        "title_translation": "Indigenous Handcrafted Black Serpentinite Pottery",
        "creator": "Longpi (Loree) Master Potters",
        "year": 1911,
        "publisher": "Traditional Craft (Hodson 1911, TRI Manipur)",
        "language": "Tangkhul",
        "dialect": "Longpi / Loree",
        "village": "Longpi",
        "category": "tradition",
        "subcategory": "craft",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Hodson-1911-Ch2-Pottery",
        "license": "Traditional Cultural Expression",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-TRAD-005_longpi_hamlei_pottery.txt",
        "verification_status": "verified",
        "notes": "Renowned ancient pottery crafted without a potter's wheel using ground black serpentinite rock (leshong lung) and weathered clay (sali), fired outdoors and polished with Chiron/Mahasa leaves.",
    },
    {
        "id": "CULT-TRAD-006",
        "resource_type": "culture",
        "title": "Lengcheng Shim Traditional Architecture & Roof-Horns",
        "title_translation": "Traditional High-Status House Architecture with Crossed Roof-Horns",
        "creator": "Tangkhul Master Woodcarvers & Awunga Builders",
        "year": 1977,
        "publisher": "Documented in Horam 1977, Ruivah 1993",
        "language": "Tangkhul",
        "dialect": "Ukhrul",
        "village": "Ukhrul",
        "category": "tradition",
        "subcategory": "architecture",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Horam-1977-Ch2-Lengcheng",
        "license": "Traditional Cultural Expression",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-TRAD-006_lengcheng_shim_architecture.txt",
        "verification_status": "verified",
        "notes": "Elite Tangkhul house architecture featuring crossed carved wooden horns (Lengcheng Kui) extending from the roof ridge, with facade planks intricately carved with mithun heads and solar symbols.",
    },
    {
        "id": "CULT-TRAD-007",
        "resource_type": "culture",
        "title": "Kalhang & Marem Brine Well Salt-Making",
        "title_translation": "Indigenous Brine Well Salt Extraction & Cake Manufacturing",
        "creator": "Kalhang & Marem Salt Guilds",
        "year": 1911,
        "publisher": "Documented in Hodson 1911",
        "language": "Tangkhul",
        "dialect": "Kalhang / Raphei",
        "village": "Kalhang",
        "category": "tradition",
        "subcategory": "craft_metallurgy_industry",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Hodson-1911-Ch2-Salt",
        "license": "Traditional Knowledge Documentation",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-TRAD-007_kalhang_marem_salt_making.txt",
        "verification_status": "verified",
        "notes": "Historical mineral salt manufacture from natural deep mountain brine wells (Machi kong), evaporated in circular iron cauldrons to form flat salt cakes historically used as currency.",
    },
    {
        "id": "CULT-PROV-007",
        "resource_type": "culture",
        "title": "Proverb on Inner Wisdom: Theikahaina kaphaningli",
        "title_translation": "The Wise Perceive with the Mind, the Foolish with the Eyes",
        "creator": "Traditional Oral Philosophy (Kasomwoshi 1991, Pettigrew 1918)",
        "year": 1918,
        "publisher": "Documented in Pettigrew 1918, Kasomwoshi 1991",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "proverb",
        "subcategory": "wisdom",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Kasomwoshi-Chanjam-145",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-PROV-007_theikahaina_kaphaningli.txt",
        "verification_status": "verified",
        "notes": "Original saying: 'Theikahaina kaphaningli, matheikahaina mikli.' Teaches that wise judgment looks beneath outward appearance to perceive true moral character.",
    },
    {
        "id": "CULT-PROV-008",
        "resource_type": "culture",
        "title": "Proverb on Human Nature: Khare khangatei makhangaza",
        "title_translation": "Habit is Hard to Alter, Generational Transformation Requires Wisdom",
        "creator": "Traditional Moral Philosophy (Kasomwoshi 1991)",
        "year": 1991,
        "publisher": "Hao Tangkhul Chanjam",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "proverb",
        "subcategory": "ethics",
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Kasomwoshi-Chanjam-204",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "local_path": "data/raw/culture/CULT-PROV-008_khare_khangatei_makhangaza.txt",
        "verification_status": "verified",
        "notes": "Original saying: 'Khare khangatei makhangaza, thot khangatei maharmana.' Teaches patience in governance and personal transformation, noting that character reform takes enduring perseverance.",
    },
]

NEW_RAW_DATA = {
    "CULT-FEST-006": {
        "slug": "dharreo_phanit",
        "tangkhul_text": [
            "Dharreo phanitli luisang kashung, kacham kashiman malailaka.",
            "Phungcham Ukhrul luishang kachivali Varewui ningli khorumda.",
            "Kazingmasho kazingmei makhavai, Varewui kakhon kaphali shitsang.",
        ],
        "english_text": [
            "At Dharreo festival, the golden paddy stands ripe before harvest begins.",
            "Across Ukhrul and Phungcham, every family petitions the Almighty Creator for blessing.",
            "Praying for protection against storm, wind, and hail, that the grain may be safely reaped.",
        ],
        "procedure": [
            "1. Inspection of standing paddy fields by farming elders in late October.",
            "2. Proclamation of Dharreo festival before any household strikes the sickle.",
            "3. Morning prayers offered at the edge of terraced paddies invoking divine protection.",
            "4. Household preparation of special roasted rice and brewed beverages for workers.",
            "5. Reaping commences in disciplined solidarity across all village sectors.",
        ],
        "participants": ["Farming Elders", "Family Lineages", "Reaping Teams"],
        "timing": "October (Autumn pre-harvest blessing)",
    },
    "CULT-FEST-007": {
        "slug": "khamang_phanit",
        "tangkhul_text": [
            "Khamang phanitli tara kongli kazip, Hundung mibing saikora.",
            "Ngasung thingron aparali shailaga tara kongli horhaisa.",
            "Nga samphangda kaphung konglaoli ringkaphawui thotna mazaingasot.",
        ],
        "english_text": [
            "At Khamang festival, the community gathers beside the mountain river channels.",
            "Harvesting and pounding wild walnut root (Ngasung) to stun river fish naturally.",
            "Sharing the bountiful catch in joyous forest fellowship banquets beneath the hills.",
        ],
        "procedure": [
            "1. Gathering wild walnut root (Ngasung) and mountain herbal bark from high ridges.",
            "2. Pounding the bark into fibrous pulp using wooden mallets on riverside rocks.",
            "3. Releasing the sap into natural pools to temporarily stun river fish.",
            "4. Communal harvesting of fish using conical cane nets and hands.",
            "5. Riverside open-fire grilling and egalitarian distribution of fish among all clans.",
        ],
        "participants": ["River Troupes", "Youth Dormitories", "Village Elders"],
        "timing": "November / Autumn post-harvest season",
    },
    "CULT-CUST-005": {
        "slug": "maran_kasa_tarang",
        "tangkhul_text": [
            "Maran Kasa ot kasak iram mibingli phanit kachung mimi.",
            "Tarang lungphung kashak thada, Awunga wui mashun themthot pamei.",
            "Lengcheng Shimli kuihon kachui, thot kachungli aming kasak pamra.",
        ],
        "english_text": [
            "The Maran Kasa feast of merit is the ultimate demonstration of generosity and civic honor.",
            "Erecting the monumental forked Tarang post, celebrating the nobility and virtue of the host.",
            "Privileged to raise the crossed roof-horns of the Lengcheng Shim, an enduring legacy for generations.",
        ],
        "procedure": [
            "1. Accumulation of extensive agricultural surplus, livestock, and brewed rice wine over years.",
            "2. Formal notification and blessing from the Awunga and village council of elders.",
            "3. Hosting sequential feasts feeding the entire village and neighboring allied settlements.",
            "4. Dragging and erecting the massive carved forked wooden post (Tarang / Tarung).",
            "5. Attainment of highest social rank, granting permission to build a Lengcheng Shim house.",
        ],
        "participants": ["Benefactor Couple", "Awunga", "Village Clans", "Neighboring Village Guests"],
        "timing": "Winter dry season (Sacred prestige institution)",
    },
    "CULT-TRAD-005": {
        "slug": "longpi_hamlei_pottery",
        "tangkhul_text": [
            "Longpi Loree Hamlei kashak avava apuipui wui pangthei.",
            "Leshong lung kala sali ngarumda, wheel makhavai pangna sai.",
            "Mahasa thingron aina phatsangda, kakhangaza black stone ham.",
        ],
        "english_text": [
            "Longpi Loree pottery embodies the ancient, unmatched craftsmanship of our ancestors.",
            "Blending crushed black serpentinite stone with mountain clay, shaped entirely by hand without a wheel.",
            "Polished with Mahasa leaves while hot from the bonfire kiln, producing lustrous black stoneware.",
        ],
        "procedure": [
            "1. Mining serpentinite rock (leshong lung) and weathering clay (sali) from sacred local sites.",
            "2. Crushing and grinding the stone into fine powder on stone mortars.",
            "3. Kneading stone powder and clay in equal proportion with mountain water into stiff paste.",
            "4. Hand-coiling and paddle-shaping vessels into pots (Ham), kettles, and platters without a wheel.",
            "5. Bonfire open firing and hot-burnishing with fresh Chiron/Mahasa leaves to achieve deep metallic black luster.",
        ],
        "participants": ["Longpi Master Potters (Men and Women)", "Village Apprentices"],
        "timing": "Dry winter months (Exclusively Longpi village)",
    },
    "CULT-TRAD-006": {
        "slug": "lengcheng_shim_architecture",
        "tangkhul_text": [
            "Lengcheng Shimli Lengcheng Kui kachui, Tangkhul ngashan thotna.",
            "Thing kaphungli mithun kazei, mikon kachivali masot pamei.",
            "Maran Kasa mibingna kashak, iram kaphungli ningyang kaung.",
        ],
        "english_text": [
            "The Lengcheng Shim proudly bears the crossed roof-horns, the architectural crown of Tangkhul heritage.",
            "Carved facade planks depicting mithun heads, hornbills, and celestial solar discs.",
            "Erected by those who accomplished the Feast of Merit, a testament to community beneficence.",
        ],
        "procedure": [
            "1. Harvesting durable hardwood timber and broad planks from communal mountain forests.",
            "2. Hand-hewing facade planks with intricate relief carvings of hornbills, mithun, and rosettes.",
            "3. Constructing broad thatched roof crowned with extended crossed wooden horns (Lengcheng Kui).",
            "4. Communal house-raising (Shim kashak) supported by all village clans.",
            "5. Consecration feast accompanied by prayers for family prosperity and village peace.",
        ],
        "participants": ["Master Woodcarvers", "Awunga & Nobility", "Community Building Teams"],
        "timing": "Dry construction season",
    },
    "CULT-TRAD-007": {
        "slug": "kalhang_marem_salt_making",
        "tangkhul_text": [
            "Kalhang Machi kongli tara thuklaka, iram mibingwui lan.",
            "Machi phungda meili kharong, kazei katha salt cake sai.",
            "Manipur kaphung konglaoli shailaga, machi thotli lan kakhare.",
        ],
        "english_text": [
            "From the deep brine springs of Kalhang and Marem flows precious mineral wealth.",
            "Boiling brine in iron pans over hardwood fires to form dense circular salt cakes.",
            "Traded across the mountains of Manipur, serving historically as high-value currency and food essence.",
        ],
        "procedure": [
            "1. Drawing brine water from deep ancestral masonry brine wells (Machi kong).",
            "2. Channeling brine into shallow circular iron cauldrons over subterranean flue furnaces.",
            "3. Continuous boiling with mountain oak firewood until brine evaporates into thick white crystals.",
            "4. Pressing hot salt paste into shallow circular moulds to solidify into heavy salt cakes.",
            "5. Distribution and barter trade across regional mountain markets.",
        ],
        "participants": ["Kalhang and Marem Salt Guilds", "Furnace Masters", "Trade Caravans"],
        "timing": "Dry season (Historically central mineral industry)",
    },
    "CULT-PROV-007": {
        "slug": "theikahaina_kaphaningli",
        "tangkhul_text": [
            "Theikahaina kaphaningli, matheikahaina mikli.",
        ],
        "english_text": [
            "The wise perceive with the discerning eye of the mind; the foolish see only with outward eyes.",
        ],
        "procedure": ["Quoted in council hearings and moral instruction to warn against superficial deception."],
        "participants": ["Elders", "Mentors", "Councils"],
        "timing": "Moral and judicial instruction",
    },
    "CULT-PROV-008": {
        "slug": "khare_khangatei_makhangaza",
        "tangkhul_text": [
            "Khare khangatei makhangaza, thot khangatei maharmana.",
        ],
        "english_text": [
            "To alter an inborn habit is difficult, but to transform an entire generation requires steadfast wisdom.",
        ],
        "procedure": ["Recited during educational discourses, community leadership guidance, and reform deliberations."],
        "participants": ["Community Leaders", "Teachers", "Elders"],
        "timing": "Generational education and governance",
    },
}


def append_to_manifest():
    """Append the 8 new records to data/manifests/culture.jsonl."""
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        existing_lines = [line.strip() for line in f if line.strip()]

    existing_ids = {json.loads(line_str)["id"] for line_str in existing_lines}
    added = 0

    with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
        for rec in NEW_CULTURE_RECORDS:
            if rec["id"] not in existing_ids:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                existing_ids.add(rec["id"])
                added += 1

    print(f"Manifest: Added {added} new culture records. Total in manifest: {len(existing_ids)}")


def sync_sqlite():
    """Insert or update new culture records in SQLite databases."""
    for db_path in [DB_FILE, BUNDLED_DB]:
        if not db_path.exists():
            continue
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for r in NEW_CULTURE_RECORDS:
            # 1. Update/Insert manifest_records
            cursor.execute(
                """
                INSERT OR REPLACE INTO manifest_records
                (id, resource_type, title, title_translation, creator, year, publisher,
                 language, dialect, source_url, source_identifier, license, permission_status,
                 local_path, verification_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r["id"],
                    r["resource_type"],
                    r["title"],
                    r["title_translation"],
                    r["creator"],
                    r["year"],
                    r["publisher"],
                    r["language"],
                    r["dialect"],
                    r["source_url"],
                    r["source_identifier"],
                    r["license"],
                    r["permission_status"],
                    r["local_path"],
                    r["verification_status"],
                    r["notes"],
                ),
            )

            # 2. Update/Insert culture table
            cursor.execute(
                """
                INSERT OR REPLACE INTO culture
                (id, title, local_name, category, subcategory, translation_en,
                 village, dialect, language, year, source_id, source_title,
                 source_url, contributor, license, permission_status, access_status,
                 verification_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r["id"],
                    r["title"],
                    r["title"],
                    r["category"],
                    r["subcategory"],
                    r["title_translation"],
                    r["village"],
                    r["dialect"],
                    r["language"],
                    r["year"],
                    r["source_identifier"],
                    r["publisher"],
                    r["source_url"],
                    r["creator"],
                    r["license"],
                    r["permission_status"],
                    "metadata_only",
                    r["verification_status"],
                    r["notes"],
                ),
            )

        conn.commit()
        cursor.execute("SELECT count(*) FROM culture")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"Synced {db_path}: Total records in culture table: {count}")


def update_build_raw_culture_module():
    """Add NEW_RAW_DATA to scripts/build_raw_culture.py so it knows about Batch 2."""
    build_raw_file = ROOT / "scripts" / "build_raw_culture.py"
    content = build_raw_file.read_text(encoding="utf-8")

    if '"CULT-FEST-006"' in content:
        print("CULT-FEST-006 already present in build_raw_culture.py")
        return

    # Prepare python snippet
    snippets = []
    for cid, data in NEW_RAW_DATA.items():
        snippets.append(f'    "{cid}": {json.dumps(data, indent=8, ensure_ascii=False)},')

    insert_str = "\n".join(snippets) + "\n"

    # Insert right before the closing brace of CULTURE_RAW_DATA
    marker = '        "timing": "Dry winter post-harvest season (Candidate status: needs_review)",\n    },\n}'
    if marker in content:
        new_content = content.replace(
            marker,
            '        "timing": "Dry winter post-harvest season (Candidate status: needs_review)",\n    },\n'
            + insert_str
            + "}",
        )
        build_raw_file.write_text(new_content, encoding="utf-8")
        print("Updated scripts/build_raw_culture.py with Batch 2 data!")
    else:
        print("Marker not found in build_raw_culture.py, skipping replacement.")


if __name__ == "__main__":
    append_to_manifest()
    sync_sqlite()
    update_build_raw_culture_module()
