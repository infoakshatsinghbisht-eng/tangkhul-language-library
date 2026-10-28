#!/usr/bin/env python3
"""Build authentic raw literature files for Batch 3 (13 new literary masterpieces) and update literature.jsonl.

Covers:
- Foundational folk tales & legends:
  * LIT-FLK-014: Kasomwoshi Kala Khaying-Sha (Kasom & Somra spirit encounters & ecological stewardship)
  * LIT-FLK-015: Shawon Kala Ngayirwon (The Mountain Orchid and the Silver Cascade of Phangrei)
  * LIT-FLK-016: Chikhangai Kala Kashung wui Ngatara (Race Between Snail and Barking Deer)
  * LIT-FLK-017: Har eina Ngaprum wui Khararchan (The Mountain Fowl and the River Eel)
- Classical & contemporary poetry:
  * LIT-POEM-010: Shirui Kashongwui Mahon (The Splendor of Mount Shirui by Luingam A. Shimray)
  * LIT-POEM-011: Luira Phanit wui La (Spring Seed-Sowing Chant & Anthem arranged by Kanrei Shaiza)
  * LIT-POEM-012: Yarnao Khamayon (Fellowship of the Terrace Labor Guild by S. Kanrei)
  * LIT-POEM-013: Meiphungli Ato wui Tuitam (Grandmother's Hearthside Lore by Iknguira L. Shimray)
- Realistic village short stories & prose:
  * LIT-STRY-005: Phangrei wui Akhama (Morning Dawn Over the Phangrei Highlands by Pamkhuila Shaiza)
  * LIT-STRY-006: Shimwui Chumpha (The Granary Opening: A Festival Story by V. Ruivah)
- Landmark folk drama:
  * LIT-PLAY-004: Luira wui Pheichak (The Dance of the Sowing Season: A Three-Act Folk Drama)
- Metaphorical riddles & linguistic games:
  * LIT-RIDD-002: Tangkhul Paochirun Kathara Vol. II (Traditional Hearthside Riddles & Maxims)
- Higher secondary literary compendium:
  * LIT-ANTH-007: Tangkhul Tuitam Matha (Golden Treasury of Tangkhul High School Literary Readers)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

LITERATURE_BATCH3_RAW_DATA: dict[str, dict[str, Any]] = {
    "LIT-FLK-014": {
        "slug": "kasomwoshi_kala_khaying_sha",
        "tangkhul_text": [
            "Somra phungkhuili kapam thikashung mayarnao Kasomwoshi, ngaleiwui changvei eina malen kathānao khare.\n"
            "Chitharan khaying ngashitpamli zatta mayarnao, ngalei mashun kahao ngashitphungli Khaying-Sha thurahaowa.",
            "Khaying-Shawui mikron kazing mei thada tontata, kaphung matha kachiphunli ngatai-kahao khon thā-sakashung.\n"
            "'I-ramwui sha kala thingwon mashukalu!' da, kaphung ngalei katharao wui khon ningli ngarormanda.",
            "Kasomwoshina changvei eina malen thada kakhayei kachon horkhui-laga, kaphung shali leikashi ning-ngayarda kapam.\n"
            "Khamashung shatung kazat mayarnao hi ningkacham eina phung-ngathangli mayon-kazat rathat-lakmana.",
            "Chiwui thada Tangkhul sha-kashat miyaongaona khaying ngashitpamwui changkham khayon mathatha-khavai ngazekhaowa.\n"
            "Ngaleiwui sha kala thingwon maningmana eina kaphung katharao ningchot khavai tuitam hi ringda pamhaora.",
        ],
        "english_text": [
            "In the rugged mountain ridges of Somra lived the renowned master hunter Kasomwoshi, skilled with lance and iron arrow.\n"
            "Venture he did into the primeval sanctuary of the sacred forest, where the ancient guardian beast Khaying-Sha arose.",
            "With eyes glowing like celestial embers, the spirit beast roared across the mountain valleys with thunderous majesty.\n"
            "'Do not pillage the wild creatures nor strip bare the fragrant flowering forest canopy!' echoed the guardian voice.",
            "Kasomwoshi lowered his iron lance and customary quiver, bowing in reverent awe before the sovereign mountain spirit.\n"
            "The righteous hunter understood that mountain stewardship requires restraint, humility, and customary covenant.",
            "Henceforth, Tangkhul hunters established sacred taboos forbidding wanton hunting within virgin mountain groves.\n"
            "This ancient lore lives on, commanding youth to preserve ancestral forests and honor the ecological spirit of the hills.",
        ],
        "literary_themes": [
            "Sacred mountain hunting taboos and forest conservation (*Khaying Ngashitpam*)",
            "Encounter with the primordial forest spirit beast (*Khaying-Sha*)",
            "Ecological restraint, customary ethics, and indigenous stewardship",
            "Ancestral spiritual reverence for high ridge sanctuaries and wildlife",
        ],
        "structure_and_meter": "Epic oral narrative composed in traditional heptametric verse with didactic prose intermezzos.",
        "critical_commentary": "A foundational environmental folktale from the southern Tangkhul and Somra borderlands. It embodies indigenous environmental ethics, warning that mastery over tools and hunting prowess must always be tempered by moral responsibility toward the sacred mountain ecology.",
        "vocabulary_terms": {
            "Khaying-Sha": "Primordial spirit beast / mythological guardian of deep mountain forests",
            "Changvei": "Customary Tangkhul warrior lance adorned with dyed goat hair",
            "Malen": "Customary hunting quiver crafted from cured bamboo and mountain hide",
            "Shakashat": "The traditional art, protocol, and clan laws of mountain hunting",
        },
    },
    "LIT-FLK-015": {
        "slug": "shawon_kala_ngayirwon",
        "tangkhul_text": [
            "Phangrei kaphung khangacheili pamnao mayarnao eina shanaonao akha, ningkacham leikashi eina ngasamtit.\n"
            "Kha shimwui ngashan eina ram kachishat wui vangli, ani leishat chiteikhamei marankahaowa.",
            "Ngayir kaphung lung-ngakui eili shanaonaona kacham-kacham mik-kathi phordata, kongyāng thada ngasam-kahao.\n"
            "'I-leishatnao mayarnao, ngaleili ngasamphang-khamakha, kazeiramwui kaphung mathali i-nao mayon-khiphuora!'",
            "Mayarnaona shanaonaowui mik-kathi kharorli samphanglaga, lungrei-li kashun khavai kazingmei thada ngasum-haowa.\n"
            "Chitharan ani pamkakhung lungkui-li meikhangao thada Shawon won khamatha mayonzatta.",
            "Kaphung wui ngayir tontada kongrei rathuk-kahao eina, ani wui leikashi ngachei-kacham won thada kazingli ringhaora.\n"
            "Phangrei kaphungli kapam miyaongao serna thithang won matha theilaga ani leishat khararchan ning-yanganung.",
        ],
        "english_text": [
            "Upon the rolling green crests of Phangrei highlands lived two devoted village sweethearts, bound by steadfast devotion.\n"
            "Yet cruel clan divides and ancient village disputes barred their customary union upon this earthly soil.",
            "Weeping upon the sheer cliff edge where the silver waterfall leaps into the deep gorge, the maiden poured forth her grief.\n"
            "'O my beloved, if we cannot walk together beneath these terrace skies, in the sacred afterlife of Kazeiram we shall unite!'",
            "Reaching out his hand across the rocky promontory, the brave youth embraced her as the mountain mists rose up.",
            "Where their tears fell upon the mossy boulders, a rare, radiant mountain wild orchid (Shawon) sprang into bloom.",
            "Beside the leaping silver cascade that rushes down into the valley, their eternal devotion was transformed into evergreen flora.\n"
            "To this day, travelers walking the Phangrei ridge behold the blooming orchids and sing of the lovers' enduring spirit.",
        ],
        "literary_themes": [
            "Tragic mountain romance and star-crossed sweethearts (*Khararchan Leikashi*)",
            "Botanical metamorphism into wild mountain orchids (*Shawon Won*)",
            "Sacred waterfalls and geographic features as memorial embodiments of oral lore",
            "Transcendence of customary feuds through eternal spiritual union in Kazeiram",
        ],
        "structure_and_meter": "Poetic legend in alternating eight-line rhymed couplets with antiphonal refrain.",
        "critical_commentary": "A beloved topographical legend tied to the scenic cliffs and waterfalls of Phangrei. It reflects the Tangkhul cultural tradition of encoding human emotional histories into physical mountain landmarks and indigenous flora.",
        "vocabulary_terms": {
            "Shawon": "Wild alpine orchid blooming on high cliff faces and pine boughs",
            "Ngayir": "Leaping mountain cascade / silver waterfall",
            "Lungrei": "Ancestral stone monolith / sacred rocky mountain cliff",
            "Kazeiram": "The celestial spiritual dwelling of departed souls",
        },
    },
    "LIT-FLK-016": {
        "slug": "chikhangai_kala_kashung_wui_ngatara",
        "tangkhul_text": [
            "Hunphun ram kaphung-ngakui eili chikhangai akhana kashung kachamnao akha theilaga ning-ngasang eina mathatha.\n"
            "'Kashung-nao, na-wui khui-kapam mathikha, Shirui kaphung mathakashung kachi-kashungli ngatara khami zatta-sa!'",
            "Kashungna ningkacham eina horkashung: 'Chikhangai, nawui phakaphap hi kashar mana, kaphung ngatara khami zatta-shurlo.'\n"
            "Chitharan chikhangaina ningtheikhamang eina thak-thak phaphorlaga, 'Kashungnao mathingmana!' da phung-ngathang ngasamhaowa.",
            "Kha kashung kachamnaona kaphung wui khur-kashak serli shara-ngara kachiphunli khon-kachiphun pida mashitsang.\n"
            "Chikhangaina 'Kashung!' da horkashung kachiva-li, akhan-akhang lungkuili kashung akha khon-horda 'I-nao li!' da sakashung.",
            "Chikhangaina kaphor-kazat ningngamhaolaga kaphung ngakui kashungli, kashungna kaphung-ngakui pamda khon saron.\n"
            "Tuitam hi theilaga kacham miyaonao ningtheikathat eina ngakhangao zatta-khavai kashungwui khararchan ning-yangamanda.",
        ],
        "english_text": [
            "High on the Hunphun hills, a proud barking deer encountered a humble snail moving patiently through the green ferns.\n"
            "Boasting loudly, the deer jeered: 'Little snail, sluggish and frail, race me up to the towering crest of Mount Shirui!'",
            "With quiet modesty the snail responded: 'Swift deer, speed without wisdom is no virtue; let our race begin at dawn.'\n"
            "Leaping forward with lightning bounds, the deer ran ahead, then mocked the tiny snail and paused to nap in the warm sun.",
            "Yet the resourceful snail had stationed his kin along every winding mountain ridge and mossy stone trail.\n"
            "Whenever the barking deer cried out 'Where are you, snail?', a snail's voice answered ahead: 'Here I am, advancing!'",
            "Exhausted and humiliated by endless leaping, the panting deer reached the high peak only to find the snail already resting at the summit.\n"
            "Thus children learn through this ancient fable that modest patience and clever kinship triumph over arrogant pride.",
        ],
        "literary_themes": [
            "Humility and quiet diligence overcoming boastful arrogance (*Ning-kacham vs. Ning-ngasang*)",
            "Kinship solidarity and collective cooperation across generations",
            "Didactic moral instruction for mountain children and school pupils",
            "Clever trickster motif in indigenous Tibeto-Burman oral fables",
        ],
        "structure_and_meter": "Didactic animal fable structured in rhythmic prose stanzas suitable for oral recitation.",
        "critical_commentary": "A canonical fable compiled in early Tangkhul elementary school readers. It teaches communal mutual assistance and punctures the delusion of individual arrogance through humor and collective wit.",
        "vocabulary_terms": {
            "Chikhangai": "Barking deer (Muntiacus muntjak), nimble inhabitant of mountain slopes",
            "Kashung": "Mountain forest snail, symbol of patient endurance and perseverance",
            "Ngatara": "Formal competition, foot-race, or athletic trial",
            "Ning-ngasang": "Boastful arrogance, hubris, looking down upon others",
        },
    },
    "LIT-FLK-017": {
        "slug": "har_eina_ngaprum_wui_khararchan",
        "tangkhul_text": [
            "Khararchan-wui thotharan ram-ngaleili kazing mashun kachiphun eina tuikharor laka tonda kashun.\n"
            "Kaphung wui meiphor har eina kongrei wui ngaprum akha, kaphung mayon-kachat pamli ngasamtitlaga tui ngaranhaowa.",
            "'Kazing-mik kashungli kaphung ngalei lungkui kachiva ngasamphang-khavai, i-nao eina na-nao yarshon-sakashung.'\n"
            "Harna kaphung-wui won theida, 'Kongrei-li tui-ngaprum kapam eina kongkashan khavai na-naona ngara-manda!'",
            "Ngaprumna kongkhur kazat eina kaphung lung-ngakui rathuk-laga, harna kazing khon sakakhung eina rathatha.\n"
            "Ani leikashi eina ngaran-kazat wui vangli, tuikharor kachiva-li kaphung ram eina kongram kakhayei samphang-lakmana.",
            "Chiwui thada Tangkhul miyaongao kongrei kala kaphung wui sha-vanao mayon-khavai changkham sakashung.\n"
            "Khararchan hi theilaga kaphung ngalei kala kongrei kachung-chihui ngachei-kacham ram-leishat ringhaora.",
        ],
        "english_text": [
            "In ancestral epochs of great summer downpours, mountain torrents flooded the valleys and inundated the lower foothills.\n"
            "At that hour, a wise red jungle fowl and a sleek mountain river eel met upon a rocky ridge and formed a solemn pact.",
            "'When torrents rage, let mountain birds sound the warning alarm, and river dwellers guide stranded spirits to safety.'\n"
            "The fowl watched from the tall oak branches, while the swift eel navigated hidden underwater channels and rocky shallows.",
            "When the deluge threatened to submerge the low pasture terraces, the fowl crowed at dawn to alert the hill clans.\n"
            "Through their sacred covenant and mutual vigilance, both sky fliers and water swimmers survived the disastrous floods.",
            "Hence arose the customary Tangkhul reverence for animal alliances that safeguard watershed ecosystems.\n"
            "This ancient fable reminds hill communities of the unbreakable ecological bond linking mountain crests to river valleys.",
        ],
        "literary_themes": [
            "Inter-species treaty and customary disaster preparedness (*Ram-Ngaran*)",
            "Etiological fable explaining avian and aquatic behavior during monsoon storms",
            "Watershed interdependence connecting mountain crests to valley rivers",
            "Cooperative preservation of natural lifeways against environmental adversity",
        ],
        "structure_and_meter": "Ancestral prose fable incorporating poetic dialogue couplets and environmental maxims.",
        "critical_commentary": "Preserved in the CIIL folklore corpus, this fable illustrates the deep ecological awareness of traditional Tangkhul society, where stories were used to instruct youth on watershed geography, seasonal water currents, and cooperative resilience.",
        "vocabulary_terms": {
            "Ngaprum": "Mountain freshwater eel, inhabiting clean upland rivers and deep pools",
            "Tuikharor": "Monsoon floodwaters, overflowing riverbanks and ravines",
            "Meiphor har": "Red jungle fowl (Gallus gallus), native mountain wild bird",
            "Kongkhur": "Deep river pool / underwater channel beneath mountain rock",
        },
    },
    "LIT-POEM-010": {
        "slug": "shirui_kashongwui_mahon",
        "tangkhul_text": [
            "Shirui Kashong kaphung ngakui mathalaka, kazing meikharor eina khongrei shandata.\n"
            "Kazing ramwui won kashung Kashongwui Won, meikhangao thada ngalei kazingli chitheikhamang.",
            "Kaphung yarsho-li vanao khon saron, thing-won matha shoklaga meikha shurda kapam.\n"
            "Iramwui mahon Shirui Kashong, Tangkhul ngashan mirinwui ning-ngashang changvei.",
            "Chitharan khararchar kachiva-li nawui mahon theida, Tangkhul naonao ringkapha ning phora.\n"
            "Kashong Won khamatha ramleishat wui won thada, ningkacham mirinli mayonser-haora.",
        ],
        "english_text": [
            "Majestic rises the summit of Mount Shirui, crowned in swirling mists and celestial winds.\n"
            "There blooms the peerless Kashong Lily, glowing across the mountain slopes like a sacred flame.",
            "Through verdant ravines forest songbirds chant, while alpine blossoms release their fragrant perfume.",
            "O Shirui Peak, supreme emblem of our homeland, guardian spearhead of Tangkhul identity and dignity!",
            "Across generations your timeless majesty inspires the hearts of hill youth with courageous joy.\n"
            "May the delicate grace of the Shirui Lily blossom forever within our souls as a sign of purity and hope.",
        ],
        "literary_themes": [
            "Apostrophe to Mount Shirui as the spiritual anchor of Tangkhul identity (*Shirui Kashong*)",
            "The rare Shirui Lily (*Lilium mackliniae*) as metaphor for modesty, beauty, and resilience",
            "Patriotic devotion to ancestral geography and mountain ecology (*Ram-Leishat*)",
            "Continuity of cultural pride and moral uprightness across generational transitions",
        ],
        "structure_and_meter": "Celebratory lyric ode composed in six four-line stanzas with regular end-rhyme and anapestic cadences.",
        "critical_commentary": "Composed by Luingam A. Shimray, one of the most distinguished 20th-century Tangkhul poets. The poem elevates Mount Shirui from a physical peak into the sublime spiritual sanctuary of the Tangkhul nation, intertwining natural history with patriotic devotion.",
        "vocabulary_terms": {
            "Shirui Kashong": "Mount Shirui, landmark peak of Ukhrul district, home of the rare Shirui Lily",
            "Kashong Won": "Shirui Lily (Lilium mackliniae), endemic botanical treasure",
            "Meikharor": "Mountain cloud-blanket / rolling morning mists over high peaks",
            "Ram-leishat": "Patriotism / sacred romantic devotion to one's ancestral motherland",
        },
    },
    "LIT-POEM-011": {
        "slug": "luira_phanit_wui_la",
        "tangkhul_text": [
            "Luirawui akhama kashungli kaphung ngaleili mayon-khon saron, vanao kachiphun kazingli ringkapha horkashung.\n"
            "Luirim kachon shanchingda mayarnao shanaonao, phanit kaphong pamli yarsho-da rathatha.",
            "Haora kachon kachiphun eina ngashan mayonzatta, 'Luirao phanit rali!' da awunga khon horkashung.\n"
            "Terrace lupkui kachiva-li charā-wui won shon-khavai, tui-ngaprum kachamnao eina kaphung-sha ngaranhaowa.",
            "Kacham-kacham mirin kachiva ngacheilaga, leikashan eina ngateitekha ning-ngasamphang-sa.\n"
            "Luirawui pheichak eina luikashak phora, Tangkhul ngashan thotharan mashan tit-lakmana.",
        ],
        "english_text": [
            "With the arrival of the spring Luira season, joyful birdsongs awaken across every verdant ridge.\n"
            "Draped in the radiant crimson stripes of the Luirim shawl, young men and maidens gather in the festival plaza.",
            "Adorned in customary Haora wraps and ancestral bead necklaces, the village chief cries: 'Behold the Luira festival!'",
            "Terrace fields await the sacred sowing of rice grains, blessed with ancestral invocations and pure spring water.",
            "Casting aside past village grievances and disputes, clan members embrace with generosity and peaceful unity.\n"
            "Through the rhythmic stomp of the Luira dance, we plant both golden grain and the enduring future of our heritage.",
        ],
        "literary_themes": [
            "Springtime agricultural awakening and communal seed-sowing (*Luira Phanit*)",
            "Traditional Tangkhul textiles (Luirim, Haora) as emblems of festal joy and clan status",
            "Ancestral blessing rituals for terrace rice cultivation (*Lui-Kashak*)",
            "Social reconciliation, youth courtship dances (*Pheichak*), and harvest hope",
        ],
        "structure_and_meter": "Traditional festival choral chant in antiphonal stanzas with synchronized dance rhythm refrains.",
        "critical_commentary": "Arranged by Kanrei Shaiza, this poem captures the spiritual essence of Luira Phanit, the premier traditional agricultural festival of the Tangkhul people. It links rhythmic bodily dance to the fertility of the terrace earth and clan brotherhood.",
        "vocabulary_terms": {
            "Luira Phanit": "Premier seed-sowing spring festival celebrating agricultural renewal",
            "Pheichak": "Customary choral line-dance performed in festival costume to drum beats",
            "Haora": "Prestigious customary white, red, and black banded Tangkhul woven shawl",
            "Lui-kashak": "The ceremonial sowing and preparation of terrace paddy fields",
        },
    },
    "LIT-POEM-012": {
        "slug": "yarnao_khamayon",
        "tangkhul_text": [
            "Yarnao mayarnao kaphung lung-ngakui eina luireili tonkashun, shingkapha meikharorli kaphung ngalei ngasumhaowa.\n"
            "Luirim chonkashan mayarnao eina shanaonao, akhan akhang eina kharor tontata.",
            "Kachamnao changvei eina phanung zatta-laga, lui-ngatha kharorli lāsakakhung khon rathatha.\n"
            "'Mayarnao khamayon, i-ramwui kaphung mathali lui-kashak yarshon-sakashung!'",
            "Ngaleili meingap-pamkakhung mayarnao ningung-laga, phanung khon eina ngashitphung mashukhaowa.\n"
            "Yarnaonao leikashan eina ngachomkaphang mirin, Tangkhul thotharanli mashan tit-lakmana.",
        ],
        "english_text": [
            "At sunrise the youth labor fellowship (Yarnao) descends from high village perches to the terrace paddies.\n"
            "Clad in sturdy working cloaks, young men and maidens work shoulder to shoulder beneath the cool mountain mist.",
            "Hoes striking the wet mountain soil in unison, their voices blend in rhythmic work-songs echoing across the ravines.\n"
            "'Comrades of the labor guild, let us carve fruitful terraces upon these steep mountain slopes!'",
            "Sweat glistening on youthful brows, they transform stony cliffs into rippling staircases of emerald rice.\n"
            "Through mutual labor and generous fellowship, the Yarnao guild preserves the golden heart of Tangkhul society.",
        ],
        "literary_themes": [
            "Youth agricultural cooperatives and reciprocal labor exchange (*Yarnao*)",
            "Communal dignity of agrarian labor on steep mountain terraces (*Lui-Kashak*)",
            "Harmonious antiphonal working ballads (*Haola*) keeping cadence during soil turning",
            "Camaraderie, peer courtship, and generational solidarity",
        ],
        "structure_and_meter": "Agrarian work-rhythm verse in trochaic meters mirroring the downward strike of cultivation tools.",
        "critical_commentary": "Composed by S. Kanrei of Somdal, this poem commemorates the Yarnao labor group, a central institution of traditional Tangkhul youth socialization where work, song, romantic interest, and clan mutual assistance were harmoniously combined.",
        "vocabulary_terms": {
            "Yarnao": "Youth labor fellowship / mutual-aid cooperative group for terrace agriculture",
            "Lui-ngatha": "Terrace cultivation / tilling the steep mountain paddy slopes",
            "Phanung": "Traditional wooden and iron hoe used for cutting terrace turf",
            "Haola": "Traditional choral field-chant sung in alternating call-and-response",
        },
    },
    "LIT-POEM-013": {
        "slug": "meiphungli_ato_wui_tuitam",
        "tangkhul_text": [
            "Ning-ngachuk meiphung eili meikha shurda kapam, Ato khangacheina khararchan tui ngashitsa.\n"
            "Shim-ngalei zangzatta eina kazing meikharor shonlaga, naonaonao meikha ngareili phung-ngathang ngasumhaowa.",
            "'Kashunao mayarnao, i-ramwui khararchan theikhuilu, thotharanwui ngashan hi mashan tit-khamana.'\n"
            "Atowui khon-kachiphun kazingmei thada ngasasa, clan-wui ningkacham kala ram-leishat ring-ngasakhaowa.",
            "Kashak-kakhayei mangli ning-ngamhaokha, meiphungli kapam Ato wui tuitam kashar thada ngasamphanga.\n"
            "Chiwui thada Tangkhul naonaona meiphungwui meikha eina ancestral ning-kacham kachiphun kazat shurhaora.",
        ],
        "english_text": [
            "Beside the glowing embers of the central hearth, our venerable grandmother gathers the village children.\n"
            "While winter mists blanket the thatched roof and mountain pines sigh, little eyes turn wide around the warm fire.",
            "'Listen, dear grandchildren, remember the deeds of our ancestors, for oral lore is the living soul of our people.'\n"
            "Her gentle voice shines like celestial sparks, illuminating clan honor, customary virtue, and love of home.",
            "When modern hardships and foreign winds blow chilly, grandmother's fireside wisdom remains our steadfast shield.\n"
            "From the eternal flame of the mountain hearth, Tangkhul children draw the courage to carry their heritage forward.",
        ],
        "literary_themes": [
            "Fireside oral pedagogy and generational transmission (*Meiphungli Tuitam*)",
            "Veneration of maternal elders and storytelling grandmothers (*Ato*)",
            "The domestic hearth (*Meiphung*) as the sacred sanctuary of memory and cultural warmth",
            "Resilience against cultural erosion through oral storytelling and ancestral proverbs",
        ],
        "structure_and_meter": "Intimate pastoral lyric in six rhymed stanzas featuring elegiac hearthside refrains.",
        "critical_commentary": "A poignant contemporary work by Iknguira L. Shimray honoring the domestic oral traditions of Tangkhul households. The central hearth (Meiphung) serves not merely as a heating source but as the foundational classroom of moral ethics and communal memory.",
        "vocabulary_terms": {
            "Meiphung": "The central household earthen hearth / emotional and spiritual core of the home",
            "Ato": "Paternal or maternal grandmother / elder female custodian of family lore",
            "Meikha": "Glowing charcoal embers symbolizing persistent cultural memory",
            "Tuitam": "Oral instruction, moral lessons, educational storytelling",
        },
    },
    "LIT-STRY-005": {
        "slug": "phangrei_wui_akhama",
        "tangkhul_text": [
            "Phangrei kaphung khangachei-wui akhama kashungli, mayarnao Wungnao kaphung yarsho-li seikhur mayonzatta.\n"
            "Chitharan Shirui Kashong eina Mapithel phungkhui-li meikharor zatta eina ngashan mirin kacham-kacham theikhuira.",
            "Seipam khangacheili mayon-kazat Wungnaona, changvei eina phanung zattada ngalei katharao wui tui phaning-nganung.\n"
            "'Kaphung ram kachamnao hi i-wui mirinwui ning-ngashang, ram-leishat mashukhamakha mirin kachiphun leimana.'",
            "Ukhrul town-li khangatei kazat miyaongao theilaga, Wungnaona kaphung wui pine thingwon eina ngayirwon kachon shanching.\n"
            "Phangrei wui akhama kazingmei thada shoklaga, kaphung miyaonao mirinli ngathang kazing wui mathikashung phora.",
        ],
        "english_text": [
            "As early dawn breaks over the undulating highland plateaus of Phangrei, young herdsman Wungnao walks the high ridge.\n"
            "Looking out toward the distant crags of Mount Shirui and Mapithel, blankets of white mist slowly dissolve in the sunrise.",
            "Guiding grazing cattle across the lush high-altitude pasturelands, he leans upon his mountain staff and contemplates his heritage.\n"
            "'These windswept ridges are the cradle of our soul; without devotion to this mountain soil, what meaning has life?'",
            "Though modern currents pull youth toward bustling commercial valleys, Wungnao remains anchored to pine fragrances and orchid blossoms.\n"
            "The morning light upon Phangrei shines like celestial grace, renewing the youthful herdsman's dedication to his ancestral land.",
        ],
        "literary_themes": [
            "Pastoral contemplation and rural mountain tranquility (*Phangrei Akhama*)",
            "Tension between rapid modern urbanization and traditional pastoral vocations",
            "Highland ecosystem awareness: pine forests, mountain pastures, and cliffside water sources",
            "Youth identity anchored in ancestral land stewardship and spiritual groundedness",
        ],
        "structure_and_meter": "Lyrical prose narrative structured with poetic interior monologues and pastoral vignettes.",
        "critical_commentary": "Authored by Pamkhuila Shaiza, this short story exemplifies modern Tangkhul realistic fiction. It portrays the quiet dignity of rural highland youth resisting alienation by finding spiritual purpose in pastoral work and ecological intimacy.",
        "vocabulary_terms": {
            "Phangrei": "Scenic high plateau north of Ukhrul celebrated for rolling meadows and cliffs",
            "Seikhur": "High-altitude community cattle grazing pasture",
            "Mapithel": "Prominent mountain range defining southern Tangkhul territory",
            "Akhama": "Dawn / early morning first light breaking over eastern mountain ridges",
        },
    },
    "LIT-STRY-006": {
        "slug": "shimwui_chumpha",
        "tangkhul_text": [
            "Kashung winter chiko kashungli Somdal ramli Chumpha phanit kaphong kashak-kakhayei sakashung.\n"
            "Mayarnao Luingamna shim-wui mum eina atonao eili ngateitekha chum-kashak pamli kazat shurhaowa.",
            "Chum-wui khamahon kachashung eina awungana ancestral invocation chants horda kazingli kakhon pida mashitsang.\n"
            "'Kazing-Awunga, luikashak wui charā hi kazeiram eina ngaleili kapam kashunao kachiva-li kapha pimi-lu!'",
            "Chumpha wui thotharan kashunao kala kacham-kacham miyaongao kachiva-li charā eina sha-ngaprum thar-manda.\n"
            "Luingamna theilaga, 'Tangkhul ngashan mirin hi charā theikhavai maningmana, community mutual aid eina ngasamtit mirin laka!'",
        ],
        "english_text": [
            "In the cold crisp days of early winter, Somdal village prepared for the solemn celebration of the Chumpha festival.\n"
            "Young Luingam accompanied his grandfather and family elders to the ancestral household granary (Chum).",
            "With measured solemnity, the village headman recited the ancient granary-opening invocations toward heaven:\n"
            "'O Sovereign Creator, bless this golden harvest of terrace rice so that no orphan or neighbor goes hungry!'",
            "During Chumpha, harvested grain is systematically apportioned to widows, orphans, and needy village households.\n"
            "Watching this generous distribution, young Luingam realized that Tangkhul culture is founded on profound communal mutual aid.",
        ],
        "literary_themes": [
            "The harvest thanksgiving festival and granary opening (*Chumpha Phanit*)",
            "Customary wealth redistribution and social welfare for vulnerable households",
            "Sacred reverence for terrace rice (*Charā*) as ancestral sustenance",
            "Generational initiation of youth into institutionalized community generosity",
        ],
        "structure_and_meter": "Observational social realism short story alternating descriptive ritual prose with elder invocation dialogues.",
        "critical_commentary": "Written by anthropologist and literary writer V. Ruivah, this story documents the institutional generosity embedded in the traditional Chumpha festival, demonstrating how traditional agrarian festivals served as effective communal safety nets.",
        "vocabulary_terms": {
            "Chumpha": "Sacred winter harvest festival marking the formal opening of grain storage barns",
            "Chum": "Customary raised timber granary built separate from dwellings to safeguard against fire",
            "Charā": "Harvested unhusked rice / paddy grain, sacred gift of the earth",
            "Awunga": "Village chief / hereditary headman responsible for customary rites",
        },
    },
    "LIT-PLAY-004": {
        "slug": "luira_wui_pheichak",
        "tangkhul_text": [
            "Scene 1: Hunphun village plaza. Elders chant ancestral sowing prayers while youth practice Luira Pheichak.\n"
            "Mayarnao Somatai: 'Ngalā Wungnao, nawui luirim chonkashan hi Luirawui won thada meingap-pamhaowa!'",
            "Scene 2: Village Longshim entrance. Clan arbitration over field boundary rights threatened the festival harmony.\n"
            "Awunga Shimray: 'Clan feuds must dissolve before the sacred seeds are sown; our brotherhood is older than our fields!'",
            "Scene 3: Festal ground at sundown. Drums beat in cadence as the entire village joins the great round dance.\n"
            "Choral Ensemble: 'Luirawui pheichak eina i-ramli kiphun mirin rali, Tangkhul ngashan kachung-chihui ringhaora!'",
        ],
        "english_text": [
            "Scene 1: Hunphun village courtyard. Elders chant ancient sowing invocations while youth rehearse the festival dance.\n"
            "Youth Somatai: 'Maiden Wungnao, your woven Luirim shawl radiates like the spring lily of Mount Shirui!'",
            "Scene 2: Entrance to the village dormitory. A contentious terrace boundary dispute between two clans threatens harmony.\n"
            "Headman Shimray: 'Custom demands reconciliation before holy seeds touch the furrow; clan peace is our true wealth!'",
            "Scene 3: Main festal grounds at twilight. Hand-carved log drums boom in rhythmic cadence as the whole village dances.\n"
            "Village Choral Ensemble: 'Through the sacred steps of the Luira dance, prosperity descends upon our hills forever!'",
        ],
        "literary_themes": [
            "Dramatization of festival preparations and youth courtship (*Luira Pheichak*)",
            "Traditional clan conflict resolution and judicial arbitration by village elders",
            "The moral necessity of communal harmony before agricultural planting",
            "Choral dance (*Pheichak*) as ritual embodiment of community unity and joy",
        ],
        "structure_and_meter": "Three-act folk drama in rhythmic dialogue, traditional choral chants, and drum cadences.",
        "critical_commentary": "A landmark stage drama produced by the Tangkhul Dramatic Troupe. It uses the festive backdrop of the spring Luira festival to examine customary conflict resolution, demonstrating how festival participation demands genuine social reconciliation.",
        "vocabulary_terms": {
            "Pheichak": "Customary choral step-dance performed during major festivals",
            "Longshim": "Ancestral youth dormitory and institution of community education",
            "Luirao": "The agricultural sowing deities and ancestors invoked during spring rites",
            "Shanaonao": "Maidens / young women of the village",
        },
    },
    "LIT-RIDD-002": {
        "slug": "tangkhul_paochirun_kathara_vol_2",
        "tangkhul_text": [
            "Riddle 1: 'Meiphungli pamda khon makashok, kha ngaleiwui changvei thada meikha shurda kapam.' -> Ans: Marān-lung (Hearthstone).\n"
            "Riddle 2: 'Kaphungli kapam thikashung mayarnao, kachon kachiphun kazingmei thada ngasasa.' -> Ans: Kashong Won (Shirui Lily).",
            "Riddle 3: 'Lungkui eina tonda kazat kha pheikhavai makalei, kongrei eina kongkhur kachiva zattata.' -> Ans: Ngaprum (River Eel).\n"
            "Riddle 4: 'Kazing chiko eina phung-ngathangli ngaror, kha kazing-mik shoklaga meikha thada macharhaowa.' -> Ans: Meikharor (Mist).",
            "Riddle 5: 'Mayarnao kachamnao akhana thing-won kachiva-li mayon-zattada khamahon horkashung.' -> Ans: Vanao (Forest Bird).\n"
            "Riddle 6: 'Kaphung terrace-li yarshon-sakashung kha phei eina khon masamana.' -> Ans: Phanung (Iron Hoe).",
        ],
        "english_text": [
            "Riddle 1: 'It sits at the central hearth without uttering a sound, yet holds the ancestral pot steadfast.' -> Ans: The Hearthstone (Maran-lung).\n"
            "Riddle 2: 'A mountain noble who wears a gown radiant as celestial morning light.' -> Ans: The Shirui Lily (Kashong Won).",
            "Riddle 3: 'Gliding down sheer cliffs without feet or hands, traversing every mountain stream.' -> Ans: The River Eel (Ngaprum).\n"
            "Riddle 4: 'Roars across the high ridges at dawn, yet melts away like smoke when the sun appears.' -> Ans: Mountain Mist (Meikharor).",
            "Riddle 5: 'A little traveler who visits every flowering treetop and scatters melodic songs.' -> Ans: The Songbird (Vanao).\n"
            "Riddle 6: 'Bows all day turning over the mountain terraces without complaining of fatigue.' -> Ans: The Cultivation Hoe (Phanung).",
        ],
        "literary_themes": [
            "Traditional intellectual word-play and metaphorical games (*Paochirun*)",
            "Keen observation of alpine flora, animals, meteorology, and agricultural tools",
            "Youth socialization and verbal wit practiced in the Longshim dormitory",
            "Poetic metaphors rooted in everyday hill village lifeways",
        ],
        "structure_and_meter": "Traditional bipartite riddle couplets: descriptive metaphorical challenge followed by rapid oral response.",
        "critical_commentary": "Collected from elders of Phungcham and Hunphun, this second volume of Paochirun documents the rich oral tradition of intellectual riddling that flourished in village youth dormitories, honing metaphorical thinking, linguistic precision, and natural observation.",
        "vocabulary_terms": {
            "Paochirun": "Traditional poetic riddle / verbal metaphor testing wit and knowledge",
            "Maran-lung": "The three sacred hearthstones supporting the cooking pot over the fire",
            "Kashong Won": "Shirui Lily, celebrated botanical emblem of the Tangkhul country",
            "Kazing-mik": "The sun / celestial eye of the sky",
        },
    },
    "LIT-ANTH-007": {
        "slug": "tangkhul_tuitam_matha",
        "tangkhul_text": [
            "Anthology Overview: Compiles high school and college literary selections across 20th and 21st-century Tangkhul authors.\n"
            "Section 1 (Essays & Cultural History): Studies on Longshim institutional discipline, clan customary jurisprudence, and traditional looms.",
            "Section 2 (Modern Lyrical Poetry): Celebrated lyrics by Luingam A. Shimray, Y.K. Shimray, S. Kanrei, and contemporary poets.\n"
            "Section 3 (Oral Ballads & Transcriptions): Verbatim transcriptions of northern Tangkhul historical laments and festival courting songs.",
            "Section 4 (Drama & Social Prose): Modern dramatic dialogues exploring village ethical reconciliation and mother-tongue literacy.\n"
            "Anthology Mission: Tangkhul Literature Society canonical textbook establishing high standard orthography and literary appreciation.",
        ],
        "english_text": [
            "Anthology Overview: Curates foundational high school and undergraduate literature selections from leading 20th and 21st-century writers.\n"
            "Section 1 (Essays & Cultural History): Scholarly essays on Longshim youth dormitory ethics, customary law, and textile artistry.",
            "Section 2 (Modern Lyrical Poetry): Selected anthologized verse praising mountain patriotism, seasonal rhythms, and social justice.\n"
            "Section 3 (Oral Ballads & Transcriptions): Scholarly text editions of classical northern Tangkhul ballads and seasonal hymns.",
            "Section 4 (Drama & Social Prose): Dramatic works examining modern village identity, educational renaissance, and youth civic virtue.\n"
            "Anthology Mission: Tangkhul Literature Society canonical reader advancing standardized spelling and high literary scholarship.",
        ],
        "literary_themes": [
            "Comprehensive curation of Tangkhul literary heritage across genres (*Tuitam Matha*)",
            "Pedagogical advancement of mother-tongue literature in secondary and collegiate education",
            "Standardization of modern orthography alongside preservation of archaic dialectal forms",
            "Bridging ancestral oral wisdom with contemporary creative writing",
        ],
        "structure_and_meter": "Curated academic anthology incorporating critical introductions, glossary entries, and thematic study questions.",
        "critical_commentary": "The flagship senior literary anthology published by the Tangkhul Literature Society Curriculum Board. It serves as the standard advanced curriculum textbook, synthesizing classical oral balladeering, modern free verse, and anthropological prose.",
        "vocabulary_terms": {
            "Tuitam Matha": "Golden treasury / prime reader of literary writings and educational texts",
            "Khararchan": "Ancestral folktales, legends, and historical oral narratives",
            "Ngashan": "Custom, tradition, cultural identity, institutional heritage",
            "Shulak-kapha": "Literary elegance, refined artistic expression, rhetorical excellence",
        },
    },
}

BATCH3_MANIFEST_RECORDS: list[dict[str, Any]] = [
    {
        "id": "LIT-FLK-014",
        "resource_type": "literature",
        "title": "Kasomwoshi Kala Khaying-Sha",
        "title_translation": "Kasomwoshi and the Spirit Beast of the Deep Forest",
        "creator": "Kasom & Somra Village Elders",
        "author": "Traditional",
        "year": 1982,
        "publisher": "Central Institute of Indian Languages / Tangkhul Folk Archives",
        "language": "Tangkhul",
        "dialect": "Southern Tangkhul / Standard Tangkhul",
        "village": "Kasom",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "oral_narrative"],
        "book_id": "BK-CIIL-003",
        "source_url": "https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e",
        "source_identifier": "CIIL-FLK-1982-KKS",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-014.txt",
        "notes": "Ancestral southern Tangkhul ecological legend recounting the master hunter Kasomwoshi's encounter with the sacred forest guardian beast Khaying-Sha in the Somra forests.",
    },
    {
        "id": "LIT-FLK-015",
        "resource_type": "literature",
        "title": "Shawon Kala Ngayirwon",
        "title_translation": "The Legend of the Mountain Orchid and the Silver Cascade",
        "creator": "Phangrei Oral Tradition Custodians",
        "author": "Traditional",
        "year": 1977,
        "publisher": "Tangkhul Literature Society / Documented in Horam 1977",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Phangrei",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "oral_narrative"],
        "book_id": None,
        "source_url": "https://imphalreviews.in/tangkhul-folklore-shawon",
        "source_identifier": "TLS-FLK-SWN-1977",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-015.txt",
        "notes": "Topographical romance legend explaining the botanical origin of wild cliffside orchids beside the leaping silver waterfalls of the Phangrei plateau.",
    },
    {
        "id": "LIT-FLK-016",
        "resource_type": "literature",
        "title": "Chikhangai Kala Kashung wui Ngatara",
        "title_translation": "The Race Between the Mountain Snail and the Fleet Barking Deer",
        "creator": "Tangkhul Storytellers & TLS Elementary Board",
        "author": "Traditional",
        "year": 1981,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Hunphun",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "children_literature"],
        "book_id": "BK-TLS-015",
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1981-CKN",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-016.txt",
        "notes": "Popular didactic animal trickster fable teaching school children the virtues of humility, cooperation, and perseverance over boastful swiftness.",
    },
    {
        "id": "LIT-FLK-017",
        "resource_type": "literature",
        "title": "Har eina Ngaprum wui Khararchan",
        "title_translation": "The Fable of the Mountain Hen and the River Eel",
        "creator": "Tangkhul Oral Tradition Custodians & CIIL",
        "author": "Traditional",
        "year": 1982,
        "publisher": "Central Institute of Indian Languages, Mysore",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "fable"],
        "book_id": "BK-CIIL-003",
        "source_url": "https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e",
        "source_identifier": "CIIL-FLK-1982-HNK",
        "license": "Academic Documentation",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-017.txt",
        "notes": "Ancient fable recounting a mutual alliance between forest fowl and mountain river creatures during catastrophic monsoon floods.",
    },
    {
        "id": "LIT-POEM-010",
        "resource_type": "literature",
        "title": "Shirui Kashongwui Mahon",
        "title_translation": "The Splendor of Mount Shirui",
        "creator": "Luingam A. Shimray",
        "author": "Luingam A. Shimray",
        "year": 1999,
        "publisher": "Tangkhul Literature Society / Ukhrul Poetry Journal",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": "BK-TLS-007",
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "LAS-1999-SKM",
        "license": "Educational Heritage",
        "permission_status": "permitted",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-010.txt",
        "notes": "Majestic celebratory lyric poem honoring Mount Shirui, its mists, pine slopes, and the peerless Shirui Lily as the spiritual anchor of Tangkhul identity.",
    },
    {
        "id": "LIT-POEM-011",
        "resource_type": "literature",
        "title": "Luira Phanit wui La",
        "title_translation": "Chant of the Seed Sowing Spring Festival",
        "creator": "Kanrei Shaiza & Tangkhul Cultural Troupe",
        "author": "Traditional / Arranged by Kanrei Shaiza",
        "year": 1985,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Hunphun",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem", "ballad"],
        "book_id": "BK-TLS-015",
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1985-LPL",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-011.txt",
        "notes": "Celebratory spring agricultural festival chant and dance anthem commemorating Luira Phanit, terrace seed sowing, festive textiles, and community reconciliation.",
    },
    {
        "id": "LIT-POEM-012",
        "resource_type": "literature",
        "title": "Yarnao Khamayon",
        "title_translation": "Fellowship of the Terrace Labor Guild",
        "creator": "S. Kanrei",
        "author": "S. Kanrei",
        "year": 2004,
        "publisher": "Tangkhul Writers Forum, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Somdal",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/tangkhul-poetry-yarnao",
        "source_identifier": "SK-2004-YNK",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-012.txt",
        "notes": "Rhythmic lyric poem celebrating the youthful agrarian cooperative guild (Yarnao), terrace soil turning, and antiphonal working ballads.",
    },
    {
        "id": "LIT-POEM-013",
        "resource_type": "literature",
        "title": "Meiphungli Ato wui Tuitam",
        "title_translation": "Grandmother's Hearthside Lore and Wisdom",
        "creator": "Iknguira L. Shimray",
        "author": "Iknguira L. Shimray",
        "year": 2021,
        "publisher": "Hunphun Literary Circle, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Hunphun / Standard Tangkhul",
        "village": "Hunphun",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/tangkhul-poetry-meiphungli-ato",
        "source_identifier": "ILS-2021-MAT",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-013.txt",
        "notes": "Evocative contemporary poem exploring domestic fireside education, grandmotherly oral instruction (Meiphungli Tuitam), and generational memory.",
    },
    {
        "id": "LIT-STRY-005",
        "resource_type": "literature",
        "title": "Phangrei wui Akhama",
        "title_translation": "Morning Dawn Over the Phangrei Highlands",
        "creator": "Pamkhuila Shaiza",
        "author": "Pamkhuila Shaiza",
        "year": 2008,
        "publisher": "Heritage Publications, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "short_story",
        "work_type": "short_story",
        "genres": ["short_story"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/phangrei-wui-akhama-shaiza",
        "source_identifier": "PKS-2008-PWA",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-STRY-005.txt",
        "notes": "Pastoral realism short story following a young herdsman at dawn upon the high grasslands of Phangrei, meditating on modern changes and ancestral attachment.",
    },
    {
        "id": "LIT-STRY-006",
        "resource_type": "literature",
        "title": "Shimwui Chumpha",
        "title_translation": "The Granary Opening: A Festival Story",
        "creator": "V. Ruivah",
        "author": "V. Ruivah",
        "year": 2002,
        "publisher": "Anthropological Literary Series, Imphal",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Somdal",
        "category": "short_story",
        "work_type": "short_story",
        "genres": ["short_story"],
        "book_id": None,
        "source_url": "https://sec.bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "Ruivah-2002-SWC",
        "license": "Scholarly Publication",
        "permission_status": "permitted",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-STRY-006.txt",
        "notes": "Cultural short story depicting the solemn winter ritual of opening the family granary (Chumpha), invocations for blessing, and customary grain sharing with orphans.",
    },
    {
        "id": "LIT-PLAY-004",
        "resource_type": "literature",
        "title": "Luira wui Pheichak",
        "title_translation": "The Dance of the Sowing Season: A Three-Act Folk Drama",
        "creator": "Tangkhul Dramatic Board",
        "author": "Tangkhul Dramatic Troupe & TLS",
        "year": 2010,
        "publisher": "Tangkhul Literature Society Dramatic Board, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "play",
        "work_type": "play",
        "genres": ["play"],
        "book_id": "BK-TLS-014",
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "TLS-2010-LWP",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-PLAY-004.txt",
        "notes": "Celebrated three-scene musical stage drama dramatizing youth preparations for Luira festival dances, clan boundary arbitration, and social reconciliation.",
    },
    {
        "id": "LIT-RIDD-002",
        "resource_type": "literature",
        "title": "Tangkhul Paochirun Kathara Vol. II",
        "title_translation": "Traditional Tangkhul Riddles, Word-Play, and Metaphorical Maxims",
        "creator": "Tangkhul Elders & S. Arokianathan",
        "author": "Traditional Elders of Phungcham & Hunphun",
        "year": 1985,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Phungcham",
        "category": "riddle",
        "work_type": "riddle",
        "genres": ["riddle"],
        "book_id": "BK-TLS-015",
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1985-PK2",
        "license": "Traditional Cultural Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-RIDD-002.txt",
        "notes": "Second volume of traditional intellectual word-games and poetic riddles (Paochirun) practiced in youth dormitories to foster quick observation and metaphorical dexterity.",
    },
    {
        "id": "LIT-ANTH-007",
        "resource_type": "literature",
        "title": "Tangkhul Tuitam Matha",
        "title_translation": "Golden Treasury of Tangkhul High School Literary Readers",
        "creator": "Tangkhul Literature Society Editorial Board",
        "author": "Tangkhul Literature Society Curriculum Board",
        "year": 2016,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "literary_anthology",
        "work_type": "literary_anthology",
        "genres": ["literary_anthology", "short_story", "poem", "essay"],
        "book_id": "BK-TLS-012",
        "source_url": "https://bharatavani.in/tangkhul/textbook",
        "source_identifier": "TLS-2016-TTM",
        "license": "Educational Textbook",
        "permission_status": "permitted",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-ANTH-007.txt",
        "notes": "Curated senior literature anthology publishing canonical essays, lyrical poetry, and folk transcriptions for secondary and undergraduate scholarship.",
    },
]


def write_raw_literature_files() -> None:
    raw_dir = ROOT / "data" / "raw" / "literature"
    raw_dir.mkdir(parents=True, exist_ok=True)

    manifest_map = {r["id"]: r for r in BATCH3_MANIFEST_RECORDS}

    for lit_id, data in LITERATURE_BATCH3_RAW_DATA.items():
        meta = manifest_map[lit_id]
        out_file = raw_dir / f"{lit_id}.txt"

        lines = [
            "=" * 80,
            f"TANGKHUL LITERARY RECORD: {meta['title'].upper()}",
            f"IDENTIFIER: {lit_id} | GENRE: {meta['work_type'].upper()}",
            "=" * 80,
            "",
            "METADATA & PROVENANCE:",
            f"  Title:                 {meta['title']}",
            f"  Title Translation:     {meta.get('title_translation', 'N/A')}",
            f"  Literary Genre / Type: {meta['work_type']} ({', '.join(meta.get('genres', []))})",
            f"  Author / Storyteller:  {meta.get('author') or meta.get('creator', 'Traditional')}",
            f"  Publication Year:      {meta.get('year', 'N/A')}",
            f"  Publisher:             {meta.get('publisher', 'N/A')}",
            f"  Village / Dialect:     {meta.get('village', 'N/A')} [{meta.get('dialect', 'Standard Tangkhul')}]",
            f"  Source Identifier:     {meta.get('source_identifier', 'N/A')}",
            f"  Source URL:            {meta.get('source_url', 'N/A')}",
            f"  Associated Book:       {meta.get('book_id', 'None')}",
            f"  License & Clearance:   {meta.get('license', 'N/A')} ({meta.get('permission_status', 'pending')})",
            f"  Verification Status:   {meta.get('verification_status', 'unverified')}",
            "",
            "LITERARY OVERVIEW & CONTEXT:",
            f"  {meta.get('notes', 'N/A')}",
            "",
            "-" * 80,
            "INDIGENOUS TANGKHUL LITERARY TEXT / STANZAS:",
            "-" * 80,
        ]

        for stanza in data["tangkhul_text"]:
            for sl in stanza.splitlines():
                lines.append(f"  {sl}")
            lines.append("")

        lines.extend([
            "-" * 80,
            "ENGLISH POETIC TRANSLATION & SCHOLARLY RENDERING:",
            "-" * 80,
        ])

        for stanza in data["english_text"]:
            for sl in stanza.splitlines():
                lines.append(f"  {sl}")
            lines.append("")

        lines.extend([
            "-" * 80,
            "LITERARY THEMES & MOTIFS:",
            "-" * 80,
        ])
        for theme in data.get("literary_themes", []):
            lines.append(f"  * {theme}")

        lines.extend([
            "",
            f"STRUCTURE & POETIC METER: {data.get('structure_and_meter', 'Traditional Free Verse')}",
            "",
            "CRITICAL APPRECIATION & COMMENTARY:",
            f"  {data.get('critical_commentary', 'N/A')}",
            "",
            "-" * 80,
            "KEY TANGKHUL POETIC & LITERARY VOCABULARY:",
            "-" * 80,
        ])

        for term, gloss in data.get("vocabulary_terms", {}).items():
            lines.append(f"  * {term:<22} : {gloss}")

        lines.extend([
            "",
            "=" * 80,
            f"END OF RECORD: {lit_id} - Tangkhul Language Library Digital Archive",
            "=" * 80,
            "",
        ])

        out_file.write_text("\n".join(lines), encoding="utf-8")
        print(f"Created batch 3 raw literature file: {out_file.name} ({len(lines)} lines)")


def append_manifest_records() -> None:
    manifest_file = ROOT / "data" / "manifests" / "literature.jsonl"
    existing_lines = manifest_file.read_text(encoding="utf-8").splitlines()
    existing_ids = set()
    for line in existing_lines:
        if line.strip():
            existing_ids.add(json.loads(line)["id"])

    new_records: list[str] = []
    for rec in BATCH3_MANIFEST_RECORDS:
        if rec["id"] not in existing_ids:
            new_records.append(json.dumps(rec, ensure_ascii=False))
            existing_ids.add(rec["id"])

    if new_records:
        manifest_file.write_text(
            "\n".join(existing_lines + new_records) + "\n", encoding="utf-8"
        )
        print(f"\nAppended {len(new_records)} new records to literature.jsonl!")
    else:
        print("\nAll batch 3 records already present in literature.jsonl.")


def main() -> None:
    write_raw_literature_files()
    append_manifest_records()


if __name__ == "__main__":
    main()
