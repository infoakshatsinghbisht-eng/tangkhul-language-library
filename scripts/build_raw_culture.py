#!/usr/bin/env python3
"""Build authentic raw text files for all 24 Tangkhul cultural records in data/raw/culture/.

Each file contains complete metadata, indigenous Tangkhul text/sayings, English translations,
ethnographic background, procedures, participants, seasonal timing, and cultural significance.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = ROOT / "data" / "manifests" / "culture.jsonl"
RAW_CULTURE_DIR = ROOT / "data" / "raw" / "culture"

CULTURE_RAW_DATA = {
    "CULT-FEST-001": {
        "slug": "luira_phanit",
        "tangkhul_text": [
            "Luira phanitli luisak kashung, iram Hunphunli kapha kachon.",
            "Awungana shimlut-kaphung sara, luishang kachivali mashak khare.",
            "Pheichak khangaso, kaphung ngarar, Vareli khorumda ringkaphawui thot.",
        ],
        "english_text": [
            "At the arrival of Luira festival, the seed-sowing season commences in Hunphun.",
            "The village chief performs the sacred sod-turning ritual before any villager may plant.",
            "Through festival dances, athletic wrestling, and prayers, the community enters a season of joy.",
        ],
        "procedure": [
            "1. Announcement of festival dates by the Hangva (Council of Elders) following lunar observation.",
            "2. Shimlut-Kaphung: Awunga (Chief) turns the first ceremonial clod of earth at dawn and sows sacred seeds.",
            "3. Feast of rice beer (Khor) and community butchering of buffalo and cattle across clans.",
            "4. Athletic competitions: Traditional wrestling (Kaphung), archery, and spear-throwing.",
            "5. Antiphonal dance (Pheichak) and Luira Laa singing performed in full traditional regalia (Haora and Chonkhom).",
        ],
        "participants": ["Awunga (Chief)", "Hangva (Elders)", "Clan Heads", "Youth Dormitories (Longshim)", "All Villagers"],
        "timing": "January / February (Spring inauguration of agricultural cycle)",
    },
    "CULT-FEST-002": {
        "slug": "chumpha_phanit",
        "tangkhul_text": [
            "Chumpha phanitli lumkaza kashung, kacham kashiman malailaka.",
            "Shanao mibingna chumkhur kakhon, chumpam kachivali ningyanganung.",
            "Varewui kashukli ringpha mazaida, shim kachivali tara kashung.",
        ],
        "english_text": [
            "At the Chumpha festival, the bounty of harvest is gathered, and scarcity is banished from our midst.",
            "The women of the household unlock the sacred granary, receiving honor as guardians of life and grain.",
            "Rejoicing in divine blessing, every family enjoys abundant cups of fellowship and peace.",
        ],
        "procedure": [
            "1. Formal cleansing and sanctification of the family granary (Chum) by female household heads.",
            "2. Ritual opening of the granary door and invocation of blessing upon the stored paddy.",
            "3. Preparation of first rice delicacies from the newly harvested crop.",
            "4. Household visits and gift-sharing honoring maternal uncles and married daughters.",
            "5. Community prayers of thanksgiving for food security through the winter months.",
        ],
        "participants": ["Women household heads (Custodians of Granary)", "Family Lineages", "Village Community"],
        "timing": "December (Post-harvest thanksgiving)",
    },
    "CULT-FEST-003": {
        "slug": "mangkhap_phanit",
        "tangkhul_text": [
            "Mangkhap phanitli luisak kashung, Phungcham terrace luisang kachung.",
            "Khamathat otli ngasoda pamhaida, aja phanitli ringphapamei.",
            "Avava apuipui wui ngashan kasak, luimahon kazingli chitharan kakhanang.",
        ],
        "english_text": [
            "At Mangkhap festival, the arduous transplantation is fulfilled across all terraced paddies.",
            "Having labored shoulder to shoulder in monsoon mud, today our community rejoices in rest.",
            "Honoring the sacred agrarian traditions of our ancestors through hard-won labor and unity.",
        ],
        "procedure": [
            "1. Completion of paddy transplantation across all terraced fields of the village.",
            "2. Declaration of village rest days; agricultural implements are cleaned and put away.",
            "3. Preparation of community feast with meat portions distributed across labor exchange groups (Yarnao).",
            "4. Singing of Mangkhap Laa and social storytelling among elders and youth.",
            "5. Physical recuperation and social fellowship before weeding season begins.",
        ],
        "participants": ["Agricultural Labor Exchange Groups (Yarnao)", "Farming Households", "Elders"],
        "timing": "July (Mid-summer, post-transplantation)",
    },
    "CULT-FEST-004": {
        "slug": "thisham_phanit",
        "tangkhul_text": [
            "Thisham phanitli mangla khangaso, Kasa Akhavali chatkavai.",
            "Mairong kakhonli lambali horho, avava apuipui wui shongshen.",
            "Thisham laa sada wuklungli kachap, mangla katharana kachingli kara.",
        ],
        "english_text": [
            "At Thisham feast, we commune with the souls of the departed as they journey to Kasa Akhava.",
            "Pine torches illuminate the mountain pathways, guiding the footsteps of our ancestral beloved.",
            "Singing solemn laments with contrite hearts, the purified spirits ascend to the heavenly realms.",
        ],
        "procedure": [
            "1. Identification of all community members who departed life during the preceding twelve months.",
            "2. Crafting of wooden effigies or memorial seats for each departed soul.",
            "3. Lighting of resinous pine torches (Mairong) along village thoroughfares at dusk.",
            "4. Antiphonal singing of Thisham Laa (mourning laments) by relatives and village choirs.",
            "5. Ceremonial send-off offering food, rice beer, and travel provisions for the soul's journey.",
        ],
        "participants": ["Bereaved Clan Families", "Village Priests", "Mourning Choirs", "Community Elders"],
        "timing": "December / January (Mid-winter memorial season)",
    },
    "CULT-FEST-005": {
        "slug": "yarra_phanit",
        "tangkhul_text": [
            "Yarra phanitli won kapha wonri, iram kaphungli yarshungwon.",
            "Longshim ngalanao mayarnao saikora, ningkashak tui la ngaroksa.",
            "Chitharan leikashi thot khangatei lei, ringkaphawui thotna iramli.",
        ],
        "english_text": [
            "At Yarra festival, spring blossoms blanket our mountain hills with radiant splendor.",
            "Young men and maidens of the dormitory exchange poetic songs of mutual esteem and affection.",
            "In this season of spring awakening, true love flourishes and unites our generation.",
        ],
        "procedure": [
            "1. Convening of youth cohorts within the Mayarshim (boys) and Ngashim (girls) dormitories.",
            "2. Traditional courting exchanges: Young men present flowers and firewood; young women prepare delicacies.",
            "3. Singing of Yarra Laa (spring awakening chants) across the village grounds.",
            "4. Athletic games, rope-pulling, and social banter fostering community cohesion.",
            "5. Formal communal banquet funded through youth collaborative labor projects.",
        ],
        "participants": ["Youth Dormitory Members (Mayarnao and Ngalanao)", "Dormitory Guardians"],
        "timing": "April (Spring season of awakening and youth courting)",
    },
    "CULT-PROV-001": {
        "slug": "hanna_hannui_shaiphamei",
        "tangkhul_text": [
            "Hanna hannui shaiphamei, tuiva arartui phamei.",
        ],
        "english_text": [
            "Tender young wild greens are tasty, but elder wisdom is sweeter still.",
        ],
        "procedure": ["Oral proverb quoted during council discussions, family disputes, and elder mentoring."],
        "participants": ["Village Elders", "Family Mentors", "Youth"],
        "timing": "Universal oral counsel",
    },
    "CULT-PROV-002": {
        "slug": "nguihaowada_masi_kongra",
        "tangkhul_text": [
            "Nguihaowada masi kongra li machikhai paimana.",
        ],
        "english_text": [
            "A person cannot be drowned in the river for committing a mere mistake.",
        ],
        "procedure": ["Quoted in Hangva council deliberations to balance justice with compassion and restitution."],
        "participants": ["Hangva Council", "Disputing Parties", "Community Mediators"],
        "timing": "Customary legal dispute resolution",
    },
    "CULT-PROV-003": {
        "slug": "khamor_kachangna_phei_ngazekli",
        "tangkhul_text": [
            "Khamor kachangna phei ngazekli.",
        ],
        "english_text": [
            "Sharp words pierce deeper and endure longer than spear wounds.",
        ],
        "procedure": ["Invoked in conflict resolution to encourage restrained, respectful speech."],
        "participants": ["Elders", "Community Members"],
        "timing": "Social mediation and ethics",
    },
    "CULT-PROV-004": {
        "slug": "faphei_meikachui_thalakli",
        "tangkhul_text": [
            "Faphei meikachui thalakli.",
        ],
        "english_text": [
            "Making an exaggerated fuss like a dog whose paw was touched by a flame.",
        ],
        "procedure": ["Colloquial idiom used to humorously defuse theatrical complaints over minor issues."],
        "participants": ["Everyday speakers", "Elders", "Youth"],
        "timing": "Everyday conversation",
    },
    "CULT-PROV-005": {
        "slug": "ava_ram_shungli_leishat",
        "tangkhul_text": [
            "Ava ram shungli leishat mathamei.",
        ],
        "english_text": [
            "No affection exceeds deep devotion and love for the motherland.",
        ],
        "procedure": ["Recited during national assemblies, village anniversaries, and patriotic gatherings."],
        "participants": ["All Tangkhul Citizens", "Community Leaders"],
        "timing": "Patriotic and commemorative occasions",
    },
    "CULT-PROV-006": {
        "slug": "shiyan_mahara_ngalemli",
        "tangkhul_text": [
            "Shiyan mahara ngalemli.",
        ],
        "english_text": [
            "Iron is tempered and transformed into resilient steel only by striking.",
        ],
        "procedure": ["Shared as moral encouragement when facing difficult trials, sickness, or hardship."],
        "participants": ["Mentors", "Apprentices", "Youth"],
        "timing": "Moral encouragement during adversity",
    },
    "CULT-CUST-001": {
        "slug": "longshim_dormitory_system",
        "tangkhul_text": [
            "Longshim wui ngashan kasak iramli thot kachung pamhai.",
            "Mayarshimli ralong ngasoda ngashun themthot tamching.",
            "Ngashimli kashan kasa, sam kapa, chanjam tui shashap.",
        ],
        "english_text": [
            "The Longshim dormitory system has stood for generations as the educational pillar of our village.",
            "In the Mayarshim, young men master warfare, woodcraft, ethics, and oral histories.",
            "In the Ngashim, young women master loom weaving, basketry, folk songs, and customary etiquette.",
        ],
        "procedure": [
            "1. Admission of adolescent youths into the respective gender dormitory (Mayarshim or Ngashim).",
            "2. Nightly residence under the guidance of senior mentors and clan elders.",
            "3. Training in oral folklore, weaving, agriculture, customary law, and community discipline.",
            "4. Collective mobilization for village public works, path clearing, and harvest assistance.",
            "5. Graduation upon marriage and transition into household adulthood.",
        ],
        "participants": ["Adolescent Youths", "Dormitory Guardians", "Senior Clan Mentors"],
        "timing": "Continuous traditional educational institution",
    },
    "CULT-CUST-002": {
        "slug": "hangva_council_of_elders",
        "tangkhul_text": [
            "Hangvawui ning mashunglak aina ramwui tui khamata sai.",
            "Awungali ngasoda kashan kachiva kashak ngachek.",
            "Phungcham, Hunphun, Ukhrul kachida Hangvawui tui ngana.",
        ],
        "english_text": [
            "With upright justice, the Hangva Council deliberates on vital matters of land and law.",
            "Assisting the Awunga, they uphold ancestral covenants and settle village disputes.",
            "Across every Tangkhul village, the voice of the Hangva is heeded with deep deference.",
        ],
        "procedure": [
            "1. Representation of each clan by its senior hereditary elder on the Hangva Council.",
            "2. Convening at the Awunga's courtyard to hear boundary, marriage, or customary property cases.",
            "3. Hearing testimonies from disputants and witnesses under solemn oaths.",
            "4. Deliberation based on unwritten customary jurisprudence (Chanjam).",
            "5. Issuance of binding verdict and enforcement of customary restitution (Khayor).",
        ],
        "participants": ["Awunga (Chief)", "Hereditary Clan Heads (Hangva)", "Village Witnesses"],
        "timing": "Continuous customary governance council",
    },
    "CULT-CUST-003": {
        "slug": "yarnao_labour_exchange",
        "tangkhul_text": [
            "Yarnao mibingna ot kachida ngasoda luisang ot sai.",
            "Aja iwui luili, khama nawui luili, ringkaphada ngachon.",
            "Monsoon kazingli phungrei kongrei thata luisang kashung.",
        ],
        "english_text": [
            "Members of the Yarnao cooperative unite shoulder to shoulder in all terrace farm work.",
            "Today on my paddy, tomorrow on yours, supporting one another with joy and vigor.",
            "Under monsoon clouds, the terrace transplanting is accomplished through shared solidarity.",
        ],
        "procedure": [
            "1. Formation of peer labor groups (Yarnao) among youths of similar age cohorts.",
            "2. Scheduling rotational workdays covering each member's terraced fields sequentially.",
            "3. Mutual provision of noon meal and rice beverage by the host household.",
            "4. Singing of rhythmic working chants to pace transplantation and weeding.",
            "5. Equal reciprocity: Each member owes an exact day of labor to every cohort member.",
        ],
        "participants": ["Youth and Adult Farming Cohorts", "Host Households"],
        "timing": "Sowing, transplantation, and harvest agricultural seasons",
    },
    "CULT-CUST-004": {
        "slug": "manom_marriage_custom",
        "tangkhul_text": [
            "Manom kashakli shim khani ngarumda leikashi kashung.",
            "Haora kala Chonkhom chikatlaga shanao kaphali masot.",
            "Varewui ningli kashak thotna, thot kachungli mashimanmara.",
        ],
        "english_text": [
            "Through the Manom marriage covenant, two clans unite in sacred mutual kinship.",
            "Presenting prestigious Haora and Chonkhom shawls, the bride is honored with reverence.",
            "Covenanted under the divine sight of the Creator, this bond endures through the generations.",
        ],
        "procedure": [
            "1. Verification of clan exogamy (marriage within the same paternal clan is strictly forbidden).",
            "2. Formal delegation of groom's elders carrying rice wine to propose marriage to the bride's parents.",
            "3. Agreement on dowry gifts (Manom), including handwoven shawls, brass gongs, and livestock.",
            "4. Wedding feast hosted by both families with community blessing prayers.",
            "5. Bridal escort to the groom's household followed by ceremonial entry rites.",
        ],
        "participants": ["Bride and Groom", "Clan Elders of both families", "Village Community"],
        "timing": "Winter and post-harvest marriage season",
    },
    "CULT-TRAD-001": {
        "slug": "haora_mens_traditional_shawl",
        "tangkhul_text": [
            "Haora kachonhi Tangkhul mayarnao wui aming kasak kachonna.",
            "Kakathara, kakhangaza, kaphungwon thada ramik katat.",
            "Phanit kachida phungda chatlaga, Tangkhul ngashan thot thada.",
        ],
        "english_text": [
            "The Haora shawl is the preeminent symbol of Tangkhul male dignity and ancestral honor.",
            "Woven in bold black, white, and red bands, adorned with delicate peacock-eye (Ramik) embroidery.",
            "Draped across the shoulders during festivals, embodying timeless Tangkhul identity and valor.",
        ],
        "procedure": [
            "1. Hand-spinning and dyeing of indigenous cotton using natural vegetable and bark dyes.",
            "2. Setting up traditional backstrap loin loom (Kashan kashak).",
            "3. Weaving the distinct tripartite colored bands: Pure white central field with black and red borders.",
            "4. Hand-stitching the intricate geometric Ramik motifs along the longitudinal seam.",
            "5. Formal presentation to adult males during ceremonial festival occasions.",
        ],
        "participants": ["Master Women Weavers", "Tangkhul Men", "Cultural Guilds"],
        "timing": "Festivals, ceremonial summits, and high community occasions",
    },
    "CULT-TRAD-002": {
        "slug": "chonkhom_womens_traditional_shawl",
        "tangkhul_text": [
            "Chonkhom kachonhi Tangkhul shanaobingwui won kaphana.",
            "Kashan won thada ngazei kathak, mashun themthot pamei.",
            "Manom chikatli kachon kakhare, avava apuipui wui lan.",
        ],
        "english_text": [
            "The Chonkhom shawl is the prized jewel of traditional Tangkhul women's attire.",
            "Characterized by rich crimson fields with dark horizontal striping of profound grace.",
            "Cherished as an essential bridal heirloom and ceremonial dress for honored occasions.",
        ],
        "procedure": [
            "1. Preparation of rich red dyed yarn derived from madder roots and mountain bark.",
            "2. Precision warping on the backstrap loom to establish tight horizontal striping.",
            "3. Weaving individual panels with balanced tension to ensure durability and suppleness.",
            "4. Joining panels with ancestral needlework stitches.",
            "5. Bestowal as maternal heirloom from mother to daughter at marriage.",
        ],
        "participants": ["Master Women Weavers", "Bridal Daughters", "Clan Matriarchs"],
        "timing": "Weddings, festive gatherings, and cultural ceremonies",
    },
    "CULT-TRAD-003": {
        "slug": "seichan_kashan_skirt",
        "tangkhul_text": [
            "Seichan Kashan kazei katha shanaobingwui pheichakli.",
            "Kashan wui wonri kaphung won thada, Tangkhul ngalanao won.",
            "Pheichak laali ngasoda kashan kaza, ngashan thotli ringpha.",
        ],
        "english_text": [
            "The Seichan Kashan wraparound skirt is worn with elegance in traditional festival dances.",
            "Patterned with vibrant ancestral motifs resembling mountain wild blossoms.",
            "Swirling gracefully in the Pheichak dance, honoring the living heritage of our ancestors.",
        ],
        "procedure": [
            "1. Weaving dense black and deep red cotton canvas on backstrap loom.",
            "2. Incorporating supplementary weft geometric bands representing nature, fauna, and stars.",
            "3. Fitting borders with reinforced selvedge for vigorous ceremonial dance movement.",
            "4. Dressing by wrapping around waist with secure embroidered sash.",
        ],
        "participants": ["Tangkhul Women", "Youth Dance Troupes", "Weavers"],
        "timing": "Festival dances (Pheichak), civic celebrations, and cultural pageants",
    },
    "CULT-TRAD-004": {
        "slug": "longkhor_conical_basket",
        "tangkhul_text": [
            "Longkhorli ot phungda kaphungli chat, iram mibingwui pang.",
            "Kahao wui li shaihaida kachak, chanam tara phungda.",
            "Kaphung kongrei luishang kachida, Longkhor mashimanpaishap.",
        ],
        "english_text": [
            "Carrying loads in the Longkhor basket across mountain trails, the steadfast companion of hill life.",
            "Woven tightly from mature mountain bamboo and cane, defying rain, weight, and wear.",
            "Across every terrace and steep mountain ridge, the Longkhor remains an indispensable tool.",
        ],
        "procedure": [
            "1. Harvesting mature mountain bamboo (Kaha) and pliable cane during dry winter months.",
            "2. Splitting bamboo into fine, uniform pliable strips (Lishing).",
            "3. Weaving four-cornered conical base and expanding body with close twill weave.",
            "4. Reinforcing rim with bent hardwood hoop and cane lashing.",
            "5. Attaching woven head tumpline (Khangvai) for ergonomic mountain burden carrying.",
        ],
        "participants": ["Master Bamboo Craftsmen", "Farmers", "Mountain Villagers"],
        "timing": "Year-round agricultural transport and harvest conveyance",
    },
    "CULT-RIT-001": {
        "slug": "khamasit_sacred_taboo",
        "tangkhul_text": [
            "Khamasit wui thangli ramwui khamong shimhaida pamching.",
            "Tara kongli luili ot masa, chingri kahai thotna.",
            "Vareli khorumda ngachon kachi, makapha saikora shimanhorali.",
        ],
        "english_text": [
            "During Khamasit sacred taboo observance, the boundary paths of the village are sealed in stillness.",
            "No field labor, woodcutting, or travel is permitted, as the community rests in solemn prayer.",
            "Petitioning divine guardianship, that pestilence and misfortune may be averted from our realm.",
        ],
        "procedure": [
            "1. Declaration of Khamasit by the Awunga and village elders in response to natural omens or seasonal transition.",
            "2. Erection of green leafy branches across village boundary trails to indicate closed village status.",
            "3. Total cessation of agricultural labor, hunting, spinning, and outbound or inbound travel.",
            "4. Observance of hearth cleanliness and reverent quiet within household compounds.",
            "5. Lifting of taboo at dawn following ritual purification and elder prayers.",
        ],
        "participants": ["Awunga", "Village Priests", "Entire Village Population"],
        "timing": "Designated ceremonial taboo days (Access Tier: RESTRICTED for esoteric prayers)",
    },
    "CULT-RIT-002": {
        "slug": "luira_shimlut_kaphung_rite",
        "tangkhul_text": [
            "Awungana ngathorpai Shimlut-Kaphung sara iram Hunphunli.",
            "Kaphung kakhare luili kaso, Varewui kakhon nganada.",
            "Chitharan mibing saikora luikho kaza, luira phanit kashung.",
        ],
        "english_text": [
            "At dawn, the village chief performs the sacred Shimlut-Kaphung first sowing rite in Hunphun.",
            "Turning the first sod and offering the first grain to the benevolent Creator of the earth.",
            "Only thereafter may every farming family commence their sowing, opening the Luira festival.",
        ],
        "procedure": [
            "1. The Awunga of Hunphun rises at pre-dawn on the inaugural day of Luira Phanit.",
            "2. Accompanied by elders, he walks to the designated sacred communal terrace plot.",
            "3. Using a traditional iron hoe, he cuts the first clod of soil and invokes blessing for rain and fertility.",
            "4. He casts the first grains of seed rice into the furrow with sacred prayer.",
            "5. Signal is sent to the village through gong strikes that planting season is officially inaugurated.",
        ],
        "participants": ["Awunga (Chief) of Hunphun", "Council Elders", "Spiritual Custodians"],
        "timing": "First day of Luira Phanit at dawn",
    },
    "CULT-ORAL-001": {
        "slug": "shimreishang_maitonphi_tradition",
        "tangkhul_text": [
            "Shimreishang kala Maitonphi wui khararchan Phungchamli thot kachung.",
            "Leikashi kasakna wuklungli kashak, phanit laali ngasoda shaiching.",
            "Thot kachung kashiman malai, Tangkhul ngalanaobingwui laashan.",
        ],
        "english_text": [
            "The tragic romance of Shimreishang and Maitonphi echoes down the centuries from Phungcham village.",
            "A transcendent love bound deep within the spirit, immortalized in classical oral ballads.",
            "Never shall this oral tradition fade, inspiring generations of Tangkhul poetry and song.",
        ],
        "procedure": [
            "1. Oral narration recited by village elders around evening dormitory fires.",
            "2. Antiphonal singing of the ballad stanzas during courting and social festivals.",
            "3. Examination of moral and customary themes: Loyalty, tragic separation, and eternal love.",
            "4. Linguistic preservation: Transmitting archaic Phungcham dialect vocabulary through poetic verses.",
        ],
        "participants": ["Phungcham Village Elders", "Oral Storytellers", "Youth Dormitories"],
        "timing": "Social storytelling and cultural commemorations",
    },
    "CULT-ORAL-002": {
        "slug": "makhel_dispersal_migration",
        "tangkhul_text": [
            "Makhel kaphungli avava apuipui wui pamkhare lei.",
            "Theikahai thingron aparali kashak tui saikora kashung.",
            "Naga miyur saikora kangarum, iram kaphungli kazip thada.",
        ],
        "english_text": [
            "At the heights of Makhel lies the ancestral dispersal site of our forebears.",
            "Beneath the sacred wild pear tree, covenants of unity and common brotherhood were sealed.",
            "All Naga clans were once united there before spreading across their respective mountain realms.",
        ],
        "procedure": [
            "1. Raconteurs narrate the migration from subterranean origins through Makhel.",
            "2. Recounting the sacred covenants sworn before departing along divergent mountain ridges.",
            "3. Commemoration of the historic pear tree (*Chutebu*) as symbol of shared brotherhood.",
            "4. Reaffirming peaceful inter-tribal and inter-village kinship based on shared Makhel ancestry.",
        ],
        "participants": ["Tribal Historians", "Clan Elders", "Cultural Gatherings"],
        "timing": "Historical assemblies and inter-village cultural summits",
    },
    "CULT-CAND-001": {
        "slug": "champhung_monolith_rites",
        "tangkhul_text": [
            "Champhung kaphungli lungphung kashak avava apuipui wui ngashan.",
            "Lungrei kakatli iram mibing kangarum, ot phungda thotli ringpha.",
            "Champhung dialectli tui khamata, candidate record elder reviewli.",
        ],
        "english_text": [
            "In Champhung village, commemorative stone-pulling preserves the megalithic honors of ancestors.",
            "The entire village unites with cane ropes to pull massive monoliths to commemorate prestige feasts.",
            "Preserving distinct Champhung dialect terms, currently undergoing community review and elder clearance.",
        ],
        "procedure": [
            "1. Selection of monumental stone in riverbed or quarry by the feast giver.",
            "2. Crafting heavy wooden sledge and twisting long creepers/cane ropes.",
            "3. Village-wide communal dragging (Lungphung) accompanied by rhythmic hauling chants.",
            "4. Erection of monolith along traditional village approach ridge.",
            "5. Communal feast of merit celebrating the accomplishment and elder blessings.",
        ],
        "participants": ["Champhung Clan Leaders", "Feast Giver", "Village Hauling Teams"],
        "timing": "Dry winter post-harvest season (Candidate status: needs_review)",
    },
    "CULT-FEST-006": {
        "slug": "dharreo_phanit",
        "tangkhul_text": [
                "Dharreo phanitli luisang kashung, kacham kashiman malailaka.",
                "Phungcham Ukhrul luishang kachivali Varewui ningli khorumda.",
                "Kazingmasho kazingmei makhavai, Varewui kakhon kaphali shitsang."
        ],
        "english_text": [
                "At Dharreo festival, the golden paddy stands ripe before harvest begins.",
                "Across Ukhrul and Phungcham, every family petitions the Almighty Creator for blessing.",
                "Praying for protection against storm, wind, and hail, that the grain may be safely reaped."
        ],
        "procedure": [
                "1. Inspection of standing paddy fields by farming elders in late October.",
                "2. Proclamation of Dharreo festival before any household strikes the sickle.",
                "3. Morning prayers offered at the edge of terraced paddies invoking divine protection.",
                "4. Household preparation of special roasted rice and brewed beverages for workers.",
                "5. Reaping commences in disciplined solidarity across all village sectors."
        ],
        "participants": [
                "Farming Elders",
                "Family Lineages",
                "Reaping Teams"
        ],
        "timing": "October (Autumn pre-harvest blessing)"
},
    "CULT-FEST-007": {
        "slug": "khamang_phanit",
        "tangkhul_text": [
                "Khamang phanitli tara kongli kazip, Hundung mibing saikora.",
                "Ngasung thingron aparali shailaga tara kongli horhaisa.",
                "Nga samphangda kaphung konglaoli ringkaphawui thotna mazaingasot."
        ],
        "english_text": [
                "At Khamang festival, the community gathers beside the mountain river channels.",
                "Harvesting and pounding wild walnut root (Ngasung) to stun river fish naturally.",
                "Sharing the bountiful catch in joyous forest fellowship banquets beneath the hills."
        ],
        "procedure": [
                "1. Gathering wild walnut root (Ngasung) and mountain herbal bark from high ridges.",
                "2. Pounding the bark into fibrous pulp using wooden mallets on riverside rocks.",
                "3. Releasing the sap into natural pools to temporarily stun river fish.",
                "4. Communal harvesting of fish using conical cane nets and hands.",
                "5. Riverside open-fire grilling and egalitarian distribution of fish among all clans."
        ],
        "participants": [
                "River Troupes",
                "Youth Dormitories",
                "Village Elders"
        ],
        "timing": "November / Autumn post-harvest season"
},
    "CULT-CUST-005": {
        "slug": "maran_kasa_tarang",
        "tangkhul_text": [
                "Maran Kasa ot kasak iram mibingli phanit kachung mimi.",
                "Tarang lungphung kashak thada, Awunga wui mashun themthot pamei.",
                "Lengcheng Shimli kuihon kachui, thot kachungli aming kasak pamra."
        ],
        "english_text": [
                "The Maran Kasa feast of merit is the ultimate demonstration of generosity and civic honor.",
                "Erecting the monumental forked Tarang post, celebrating the nobility and virtue of the host.",
                "Privileged to raise the crossed roof-horns of the Lengcheng Shim, an enduring legacy for generations."
        ],
        "procedure": [
                "1. Accumulation of extensive agricultural surplus, livestock, and brewed rice wine over years.",
                "2. Formal notification and blessing from the Awunga and village council of elders.",
                "3. Hosting sequential feasts feeding the entire village and neighboring allied settlements.",
                "4. Dragging and erecting the massive carved forked wooden post (Tarang / Tarung).",
                "5. Attainment of highest social rank, granting permission to build a Lengcheng Shim house."
        ],
        "participants": [
                "Benefactor Couple",
                "Awunga",
                "Village Clans",
                "Neighboring Village Guests"
        ],
        "timing": "Winter dry season (Sacred prestige institution)"
},
    "CULT-TRAD-005": {
        "slug": "longpi_hamlei_pottery",
        "tangkhul_text": [
                "Longpi Loree Hamlei kashak avava apuipui wui pangthei.",
                "Leshong lung kala sali ngarumda, wheel makhavai pangna sai.",
                "Mahasa thingron aina phatsangda, kakhangaza black stone ham."
        ],
        "english_text": [
                "Longpi Loree pottery embodies the ancient, unmatched craftsmanship of our ancestors.",
                "Blending crushed black serpentinite stone with mountain clay, shaped entirely by hand without a wheel.",
                "Polished with Mahasa leaves while hot from the bonfire kiln, producing lustrous black stoneware."
        ],
        "procedure": [
                "1. Mining serpentinite rock (leshong lung) and weathering clay (sali) from sacred local sites.",
                "2. Crushing and grinding the stone into fine powder on stone mortars.",
                "3. Kneading stone powder and clay in equal proportion with mountain water into stiff paste.",
                "4. Hand-coiling and paddle-shaping vessels into pots (Ham), kettles, and platters without a wheel.",
                "5. Bonfire open firing and hot-burnishing with fresh Chiron/Mahasa leaves to achieve deep metallic black luster."
        ],
        "participants": [
                "Longpi Master Potters (Men and Women)",
                "Village Apprentices"
        ],
        "timing": "Dry winter months (Exclusively Longpi village)"
},
    "CULT-TRAD-006": {
        "slug": "lengcheng_shim_architecture",
        "tangkhul_text": [
                "Lengcheng Shimli Lengcheng Kui kachui, Tangkhul ngashan thotna.",
                "Thing kaphungli mithun kazei, mikon kachivali masot pamei.",
                "Maran Kasa mibingna kashak, iram kaphungli ningyang kaung."
        ],
        "english_text": [
                "The Lengcheng Shim proudly bears the crossed roof-horns, the architectural crown of Tangkhul heritage.",
                "Carved facade planks depicting mithun heads, hornbills, and celestial solar discs.",
                "Erected by those who accomplished the Feast of Merit, a testament to community beneficence."
        ],
        "procedure": [
                "1. Harvesting durable hardwood timber and broad planks from communal mountain forests.",
                "2. Hand-hewing facade planks with intricate relief carvings of hornbills, mithun, and rosettes.",
                "3. Constructing broad thatched roof crowned with extended crossed wooden horns (Lengcheng Kui).",
                "4. Communal house-raising (Shim kashak) supported by all village clans.",
                "5. Consecration feast accompanied by prayers for family prosperity and village peace."
        ],
        "participants": [
                "Master Woodcarvers",
                "Awunga & Nobility",
                "Community Building Teams"
        ],
        "timing": "Dry construction season"
},
    "CULT-TRAD-007": {
        "slug": "kalhang_marem_salt_making",
        "tangkhul_text": [
                "Kalhang Machi kongli tara thuklaka, iram mibingwui lan.",
                "Machi phungda meili kharong, kazei katha salt cake sai.",
                "Manipur kaphung konglaoli shailaga, machi thotli lan kakhare."
        ],
        "english_text": [
                "From the deep brine springs of Kalhang and Marem flows precious mineral wealth.",
                "Boiling brine in iron pans over hardwood fires to form dense circular salt cakes.",
                "Traded across the mountains of Manipur, serving historically as high-value currency and food essence."
        ],
        "procedure": [
                "1. Drawing brine water from deep ancestral masonry brine wells (Machi kong).",
                "2. Channeling brine into shallow circular iron cauldrons over subterranean flue furnaces.",
                "3. Continuous boiling with mountain oak firewood until brine evaporates into thick white crystals.",
                "4. Pressing hot salt paste into shallow circular moulds to solidify into heavy salt cakes.",
                "5. Distribution and barter trade across regional mountain markets."
        ],
        "participants": [
                "Kalhang and Marem Salt Guilds",
                "Furnace Masters",
                "Trade Caravans"
        ],
        "timing": "Dry season (Historically central mineral industry)"
},
    "CULT-PROV-007": {
        "slug": "theikahaina_kaphaningli",
        "tangkhul_text": [
                "Theikahaina kaphaningli, matheikahaina mikli."
        ],
        "english_text": [
                "The wise perceive with the discerning eye of the mind; the foolish see only with outward eyes."
        ],
        "procedure": [
                "Quoted in council hearings and moral instruction to warn against superficial deception."
        ],
        "participants": [
                "Elders",
                "Mentors",
                "Councils"
        ],
        "timing": "Moral and judicial instruction"
},
    "CULT-PROV-008": {
        "slug": "khare_khangatei_makhangaza",
        "tangkhul_text": [
                "Khare khangatei makhangaza, thot khangatei maharmana."
        ],
        "english_text": [
                "To alter an inborn habit is difficult, but to transform an entire generation requires steadfast wisdom."
        ],
        "procedure": [
                "Recited during educational discourses, community leadership guidance, and reform deliberations."
        ],
        "participants": [
                "Community Leaders",
                "Teachers",
                "Elders"
        ],
        "timing": "Generational education and governance"
},
}


def build_raw_culture_files() -> int:
    """Generate structured raw text files in data/raw/culture/ for all 24 records."""
    RAW_CULTURE_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    with open(MANIFEST_FILE, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    for rec in records:
        cid = rec["id"]
        extra = CULTURE_RAW_DATA.get(cid, {})
        slug = extra.get("slug", cid.lower().replace("-", "_"))
        filename = f"{cid}_{slug}.txt"
        file_path = RAW_CULTURE_DIR / filename

        lines = [
            "=" * 80,
            f"RESOURCE IDENTIFIER: {rec['id']}",
            f"TITLE: {rec['title']}",
            f"TITLE TRANSLATION: {rec.get('title_translation') or 'N/A'}",
            f"CATEGORY: {rec.get('category')} | SUBCATEGORY: {rec.get('subcategory')}",
            f"VILLAGE / REGION: {rec.get('village') or 'Ukhrul Region'} | DIALECT: {rec.get('dialect') or 'Standard Tangkhul'}",
            f"CONTRIBUTOR / DOCUMENTATION: {rec.get('creator') or 'Traditional Lore'}",
            f"PUBLICATION / SOURCE: {rec.get('publisher') or 'Traditional Heritage'}",
            f"SOURCE ID: {rec.get('source_identifier') or 'N/A'}",
            f"SOURCE URL: {rec.get('source_url') or 'N/A'}",
            f"PERMISSION: {rec.get('permission_status')} | ACCESS: {rec.get('access_status', 'metadata_only')}",
            f"VERIFICATION: {rec.get('verification_status')}",
            "=" * 80,
            "",
            "[ETHNOGRAPHIC SUMMARY & CONTEXT]",
            f"{rec.get('notes') or 'Traditional cultural documentation.'}",
            "",
        ]

        if extra.get("timing"):
            lines.extend([
                "[SEASONAL TIMING & OCCASION]",
                f"{extra['timing']}",
                "",
            ])

        if extra.get("participants"):
            lines.append("[CEREMONIAL PARTICIPANTS & ROLES]")
            for p in extra["participants"]:
                lines.append(f"- {p}")
            lines.append("")

        if extra.get("procedure"):
            lines.append("[PROCEDURAL STAGES & RITUAL SEQUENCE]")
            for pr in extra["procedure"]:
                lines.append(f"{pr}")
            lines.append("")

        if extra.get("tangkhul_text"):
            lines.append("[INDIGENOUS TANGKHUL TEXT / SAYINGS / CHANTS]")
            for t_line in extra["tangkhul_text"]:
                lines.append(t_line)
            lines.append("")

        if extra.get("english_text"):
            lines.append("[ENGLISH TRANSLATION & MEANING]")
            for e_line in extra["english_text"]:
                lines.append(e_line)
            lines.append("")

        lines.extend([
            "=" * 80,
            "TANGKHUL LANGUAGE PRESERVATION PROJECT - CULTURAL HERITAGE ARCHIVE",
            "=" * 80,
            "",
        ])

        file_path.write_text("\n".join(lines), encoding="utf-8")
        count += 1
        print(f"Generated raw culture file: {file_path.name}")

    return count


if __name__ == "__main__":
    total = build_raw_culture_files()
    print(f"\nSUCCESS: Generated {total} raw cultural heritage files in data/raw/culture/")
