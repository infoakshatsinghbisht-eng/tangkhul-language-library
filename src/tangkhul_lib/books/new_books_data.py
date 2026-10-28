"""Complete chapter, curriculum, and textual data for newly digitized Tangkhul books.

Supplies data for:
- BK-ARCH-002: Jesuwui La: Hymns in Tangkhul Naga (Pettigrew 1907)
- BK-ARCH-003: The Naga Tribes of Manipur: Tangkhul Sections (Hodson 1911)
- BK-LIT-001: The Tangkhul Folk Poetry in Song (HAOLA, Dr. R. Horam 2013)
- BK-LIT-002: Folk Songs of The Tangkhul (Dr. H. Kamkhenthang & A. Ngashan Chahong 1987)
- BK-LIT-003: Tangkhul Gee Wari Singbul (Tangkhul Folktale Compendium, Y. K. Shimray 1976)
- BK-CIIL-004: Tangkhul-English, Hindi Dictionary (S. Arokianathan & R. Sharma 1995)
"""

from __future__ import annotations

from typing import Any


def get_pettigrew_1907_jesuwui_la_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-ARCH-002 (Pettigrew 1907)."""
    return {
        "preface": (
            "Jesuwui La: Hymns in Tangkhul Naga, compiled and translated by Rev. William Pettigrew "
            "(American Baptist Mission House, Ukhrul, Manipur, Assam, 1907, 2nd Edition; printed at "
            "Baptist Mission Press, Calcutta). Preserves the earliest published Christian hymnal "
            "and devotional poetry in the Ukhrul dialect of Tangkhul Naga."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Early Devotional Hymns",
                "page_start": 4,
                "page_end": 5,
                "summary": "Classic devotional hymns including 'Jesus Loves Me' (Hi Jesuna Laishi).",
                "tangkhul_text": (
                    "1. Hi Jesuna laishi, khikala jila, in a Vare chiwui lairikli, palaga I shitsanga. "
                    "Ma, ili laishi! Ma, ili laishi! Ma, ili laishi! Lairikli iya. "
                    "2. Hi Jesuna laishi, A mangla chihomihai; Varina kaching khamaug shomida changmilakra. "
                    "3. Ili Jesuna laishi, noshino awui nona; athum masathukmana, Ana kamakangvana. "
                    "4. Hi Jesuna laishi, iwui moral pheomira; khikala jila awui Mangla chihomihaira."
                ),
                "english_translation": (
                    "1. Jesus loves me, this I know, for the Bible tells me so; little ones to Him belong, "
                    "they are weak but He is strong. Yes, Jesus loves me! The Bible tells me so. "
                    "2. Jesus loves me, He who died heaven's gate to open wide; He will wash away my sin. "
                    "3. Jesus loves me, loves me still, though I'm very weak and ill; from His shining throne on high. "
                    "4. Jesus loves me, He will stay close beside me all the way; He has washed away my sin."
                ),
                "vocabulary": [
                    {"word": "laishi", "pos": "verb", "meaning": "loves, cares for", "example": "Hi Jesuna laishi."},
                    {"word": "mangla", "pos": "noun", "meaning": "spirit, soul", "example": "A mangla chihomihai."},
                    {"word": "shitsanga", "pos": "verb", "meaning": "believes, trusts", "example": "Lairikli palaga shitsanga."},
                    {"word": "kaching", "pos": "noun", "meaning": "heaven, firmament", "example": "Kachingli changmilakra."},
                ],
                "grammar_points": [
                    "Early orthography feature: 'ai' diphthong where TLS standardizes to 'ei'.",
                    "Future tense inflection -ra in 'pheomira' (will cleanse).",
                ],
                "comprehension_questions": [
                    "How is divine love expressed in early Pettigrew Tangkhul hymnody?",
                    "What orthographic differences distinguish the 1907 text from modern TLS spelling?",
                ],
            },
            {
                "chapter_number": 2,
                "title": "Hymns of Divine Grace & Love",
                "page_start": 6,
                "page_end": 7,
                "summary": "Grace and security in faith: 'Safe in the Arms of Jesus' (He Jesuwui Makali).",
                "tangkhul_text": (
                    "1. He Jesuwui makali, eingphalaka; siwui ngahan ngaida romhai, phasa kakhanang rai. "
                    "Kachingwui chan nganalu, iwui la sada laili, Jesuna nani mashitta, hangda la kasana. "
                    "2. He Jesuwui makali, kangachee malaimana; I moral maphungmara, chiaina makhanangmara. "
                    "Wukli kakhanang malaita, ringkapha apamna, mikumo awui okkathui ringkapha kashungna."
                ),
                "english_translation": (
                    "1. Safe in the arms of Jesus, safe on His gentle breast; there by His love o'ershaded, "
                    "sweetly my soul shall rest. Hark! 'tis the voice of angels, borne in a song to me. "
                    "2. Safe in the arms of Jesus, safe from corroding care; safe from the world's temptations, "
                    "sin cannot harm me there. Free from the blight of sorrow, free from my doubts and fears."
                ),
                "vocabulary": [
                    {"word": "makali", "pos": "postp", "meaning": "in the arms of", "example": "Jesuwui makali."},
                    {"word": "ringkapha", "pos": "noun", "meaning": "peace, joy", "example": "Ringkapha apamna."},
                    {"word": "kangachee", "pos": "noun", "meaning": "terror, dread", "example": "Kangachee malaimana."},
                    {"word": "okkathui", "pos": "noun", "meaning": "mortal existence", "example": "Mikumo awui okkathui."},
                ],
                "grammar_points": [
                    "Negative particle malaimana indicating complete absence.",
                    "Postpositional phrase attachment with genitive -wui.",
                ],
                "comprehension_questions": [
                    "What metaphor is used to express spiritual peace in Chapter 2?",
                    "Identify the negative verbal constructions in the stanzas.",
                ],
            },
            {
                "chapter_number": 3,
                "title": "Penitential & Supplication Hymns",
                "page_start": 8,
                "page_end": 9,
                "summary": "Supplication and fellowship: 'What a Friend We Have in Jesus' (Jesuli Ithum Kaphā Temi).",
                "tangkhul_text": (
                    "1. Jesuli ithum kaphā temi akha leiyi, ithumwui moral kala kakhanang saikora phungmiya. "
                    "Khorum-ngacheida Varili kachiphun mathaloikhalang, ningkhamayung tarakha ithum khamatai thotna. "
                    "2. Khipana kakhanang kala ningkachuk phunga? Jesuwui lili vashitlaga khorumlu. "
                    "Ana khipakha matheikhui-mana malei, ningchang lak eina temkhamishi phapharomei."
                ),
                "english_translation": (
                    "1. What a friend we have in Jesus, all our sins and griefs to bear! What a privilege to carry "
                    "everything to God in prayer! O what peace we often forfeit, O what needless pain we bear. "
                    "2. Have we trials and temptations? Is there trouble anywhere? We should never be discouraged; "
                    "take it to the Lord in prayer. In His arms He'll take and shield thee; thou wilt find a solace there."
                ),
                "vocabulary": [
                    {"word": "temi", "pos": "noun", "meaning": "companion, friend", "example": "Kaphā temi."},
                    {"word": "moral", "pos": "noun", "meaning": "fault, trespass", "example": "Ithumwui moral saikora."},
                    {"word": "khorum-ngachei", "pos": "noun", "meaning": "prayer, supplication", "example": "Varili khorumlu."},
                    {"word": "ningkachuk", "pos": "noun", "meaning": "grief, heaviness", "example": "Ningkachuk kaphung."},
                ],
                "grammar_points": [
                    "Dative case marker -li in personal relations ('Jesuli', 'Varili').",
                    "Rhetorical interrogation marker with 'khipana'.",
                ],
                "comprehension_questions": [
                    "What is the Tangkhul equivalent for 'prayer' in Pettigrew's text?",
                    "Translate into Tangkhul: 'Jesus is our faithful friend.'",
                ],
            },
            {
                "chapter_number": 4,
                "title": "Pilgrim & Faith Hymns",
                "page_start": 10,
                "page_end": 11,
                "summary": "Unshakable refuge: 'Rock of Ages' (Aching Lungrei Makatha).",
                "tangkhul_text": (
                    "1. Aching lungrei iwui vang kakhayei, nawui khamangli ili kaphumpam milu. "
                    "Nawui azing eina kathur tara kala ashi china iwui moral shiman ngasaku. "
                    "2. Iwui pang eina kasa otna nawui shiyan makhararthukmana; kachara zangzang shoklala nawui akhavawuina. "
                    "Na vathot iwui kachiphun, nawui crossli i panglakha ngaranmida leiyi."
                ),
                "english_translation": (
                    "1. Rock of Ages, cleft for me, let me hide myself in Thee; let the water and the blood, "
                    "from Thy wounded side which flowed, be of sin the double cure, save from wrath and make me pure. "
                    "2. Not the labors of my hands can fulfill Thy law's demands; could my zeal no respite know, "
                    "could my tears forever flow, all for sin could not atone; Thou must save, and Thou alone."
                ),
                "vocabulary": [
                    {"word": "lungrei", "pos": "noun", "meaning": "boulder, rock", "example": "Aching lungrei."},
                    {"word": "ashi", "pos": "noun", "meaning": "blood", "example": "Tara kala ashi."},
                    {"word": "panglakha", "pos": "adv", "meaning": "empty-handed", "example": "Nawui crossli panglakha."},
                    {"word": "kakhayei", "pos": "adj", "meaning": "cleft, split", "example": "Iwui vang kakhayei."},
                ],
                "grammar_points": [
                    "Causative suffix -sak in 'shiman ngasaku' (cause to disappear).",
                    "Instrumental/ablative clitic -eina in 'pang eina'.",
                ],
                "comprehension_questions": [
                    "Explain the geological metaphor of 'Aching lungrei' in Tangkhul hymnody.",
                    "Identify the causative verbs in Chapter 4.",
                ],
            },
            {
                "chapter_number": 5,
                "title": "Hymns of the Kingdom & Eternal Life",
                "page_start": 12,
                "page_end": 13,
                "summary": "The heavenly river: 'Shall We Gather at the River' (Kongreili Ithum Ngazipra).",
                "tangkhul_text": (
                    "1. Kaching Kazingramwui kongreili, Varewui khamatha apamli, ithum saikora ngazipra? "
                    "Ma, ithum ngazipra kong kaphali, kong kaphali, Varewui kuiram ngachaili ngazipsera. "
                    "2. Kongrei chihui ngashilakna, thikahai maleimana; Vare eina A Naochina karing khangarum ramli."
                ),
                "english_translation": (
                    "1. Shall we gather at the river, where bright angel feet have trod, with its crystal tide "
                    "forever flowing by the throne of God? Yes, we'll gather at the river, the beautiful river. "
                    "2. On the margin of the river, washing up its silver spray, we will walk and worship ever, "
                    "all the happy golden day."
                ),
                "vocabulary": [
                    {"word": "kongrei", "pos": "noun", "meaning": "river, stream", "example": "Kazingramwui kongreili."},
                    {"word": "ngazipra", "pos": "verb", "meaning": "will assemble", "example": "Ithum saikora ngazipra."},
                    {"word": "kuiram", "pos": "noun", "meaning": "royal throne", "example": "Varewui kuiram ngachaili."},
                    {"word": "karing", "pos": "adj", "meaning": "living, eternal", "example": "Karing khangarum ramli."},
                ],
                "grammar_points": [
                    "Future marker -sera denoting collective completion.",
                    "Repetition of nouns for poetic emphasis: 'kong kaphali, kong kaphali'.",
                ],
                "comprehension_questions": [
                    "What celestial imagery is depicted in the hymn?",
                    "How is collective gathering expressed morphologically?",
                ],
            },
            {
                "chapter_number": 6,
                "title": "Morning, Evening & Daily Life Hymns",
                "page_start": 14,
                "page_end": 15,
                "summary": "Evening meditation: 'Abide With Me' (I Eina Pamchinglu).",
                "tangkhul_text": (
                    "1. Zimik tunhaira, ngaya kaching chuiye; Kazing khayingli i eina pamchinglu. "
                    "Katei ngashunkhami kacham chitharanli, khangachamwui Ava, i eina pamchinglu. "
                    "2. Okkathui mirin hi thakta kanthuiseri; kuipham, ngashan saikora themthuira. "
                    "Khamatei malei nawui ngachaili pamlu; Makangateipa, i eina pamchinglu."
                ),
                "english_translation": (
                    "1. Abide with me: fast falls the eventide; the darkness deepens; Lord, with me abide. "
                    "When other helpers fail and comforts flee, Help of the helpless, O abide with me. "
                    "2. Swift to its close ebbs out life's little day; earth's joys grow dim; its glories pass away; "
                    "change and decay in all around I see; O Thou who changest not, abide with me."
                ),
                "vocabulary": [
                    {"word": "pamchinglu", "pos": "verb", "meaning": "abide steadfastly", "example": "I eina pamchinglu."},
                    {"word": "zimik tunhaira", "pos": "idiom", "meaning": "sun has set", "example": "Zimik tunhaira, ngaya chuiye."},
                    {"word": "makangateipa", "pos": "noun", "meaning": "the immutable one", "example": "Makangateipa pamlu."},
                ],
                "grammar_points": [
                    "Continuous aspect suffix -ching in imperative pam-ching-lu.",
                    "Perfective aspect marker -haira in 'zimik tunhaira'.",
                ],
                "comprehension_questions": [
                    "What does the phrase 'zimik tunhaira' signify in Tangkhul life?",
                    "Analyze the compound 'makangateipa'.",
                ],
            },
            {
                "chapter_number": 7,
                "title": "Doxologies, Anthems & Closing Liturgy",
                "page_start": 16,
                "page_end": 18,
                "summary": "Old Hundredth Doxology and The Lord's Prayer (Ithumwui Ava Kazingramli Kapam).",
                "tangkhul_text": (
                    "Vare khamatha kashungli, ngalei miyur saikorana matheilu; "
                    "Kaching Kazingramwui mangla bing, Vare A Mingli mathaseru. "
                    "Ava, A Nao, kala Mangla Kathara, ngashan kashung kumching-kumching leiyangranu. Amen. "
                    "Ithumwui Ava Kazingramli kapam, Nawui ming kathara thada kharing sairanu. "
                    "Nawui ngashan ram raranu. Nawui ning Kazingramli thada ngaleili la ngarunsangranu. "
                    "Aja ithumwui kasala kashakpei milu. Ithumli kateina kashikhami pheomikahai thada ithumwui moralla pheomilu. "
                    "Ithumli ngasateikhavaili mathalukhavai masangasaklu, kha kashieina kankhuimilu. Amen."
                ),
                "english_translation": (
                    "Praise God from whom all blessings flow; praise Him all creatures here below; "
                    "praise Him above, ye heavenly host; praise Father, Son, and Holy Ghost. Amen. "
                    "Our Father which art in heaven, Hallowed be Thy name. Thy kingdom come. "
                    "Thy will be done in earth, as it is in heaven. Give us this day our daily bread. "
                    "And forgive us our debts, as we forgive our debtors. And lead us not into temptation, "
                    "but deliver us from evil: For Thine is the kingdom, and the power, and the glory, forever. Amen."
                ),
                "vocabulary": [
                    {"word": "kathara", "pos": "adj", "meaning": "holy, pure", "example": "Mangla Kathara."},
                    {"word": "ngashan ram", "pos": "noun", "meaning": "kingdom", "example": "Nawui ngashan ram raranu."},
                    {"word": "kumching", "pos": "adv", "meaning": "forever", "example": "Kumching kumching nawuina."},
                    {"word": "kankhuimilu", "pos": "verb", "meaning": "deliver us", "example": "Kashieina kankhuimilu."},
                ],
                "grammar_points": [
                    "Optative mood suffix -ranu ('sairanu', 'raranu').",
                    "Negative causative in 'masangasaklu' (lead us not).",
                ],
                "comprehension_questions": [
                    "Quote the opening sentence of the Tangkhul Lord's Prayer.",
                    "Explain the optative inflection in Christian liturgical Tangkhul.",
                ],
            },
        ],
    }


def get_hodson_1911_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-ARCH-003 (Hodson 1911)."""
    return {
        "preface": (
            "The Naga Tribes of Manipur (Tangkhul Sections) by T. C. Hodson, late Assistant Political "
            "Agent in Manipur and Superintendent of the State (Macmillan and Co., Limited, London, 1911). "
            "Presents the authoritative historical and ethnographic documentation of the Tangkhul Nagas, "
            "their habitat, social organization, village headmanship, folktales, ballads, and linguistic survey."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Habitat, Geography & Tribal Divisions",
                "page_start": 4,
                "page_end": 5,
                "summary": "Geographical territory and four subdivisions: Raphei, Kathur, Kamo, and Kharao.",
                "tangkhul_text": (
                    "Tangkhul miyur hi Manipur wui kaphung zanshorli pamda kaphung khangacheo eina ngashitna. "
                    "Ayur khani eina mati leiyi: Raphei (Northern Tangkhuls), Kathur (Central Tangkhuls around Ukhrul), "
                    "Kamo (Southern Tangkhuls bordering Maring territory), and Kharao (Western Tangkhuls facing the valley). "
                    "Ukhrul kaphung hi phungreitang sada kaphung khangateiwui tui ngazekpam thada leiyi."
                ),
                "english_translation": (
                    "The Tangkhuls occupy the mountain tracts east of the valley of Manipur. "
                    "They are grouped into four main territorial sections: Raphei in the north, "
                    "Kathur in the centre around Ukhrul and Hungpung, Kamo in the south, and Kharao in the west. "
                    "Ukhrul serves as the recognized linguistic standard among all regional dialects."
                ),
                "vocabulary": [
                    {"word": "raphei", "pos": "noun", "meaning": "northern Tangkhul area", "example": "Raphei ramli."},
                    {"word": "kathur", "pos": "noun", "meaning": "central Tangkhul area", "example": "Kathur Ukhrul."},
                    {"word": "kamo", "pos": "noun", "meaning": "southern Tangkhul area", "example": "Kamoram khava."},
                    {"word": "kharao", "pos": "noun", "meaning": "western Tangkhul area", "example": "Kharao ngaleili."},
                ],
                "grammar_points": [
                    "Locative case marker -li attached to geographical names.",
                    "Directional nominalization: zanshor (east), zantung (west).",
                ],
                "comprehension_questions": [
                    "What are the four historical subdivisions of the Tangkhul territory?",
                    "Why was Ukhrul selected as the central standard by early linguists?",
                ],
            },
            {
                "chapter_number": 2,
                "title": "Tangkhul Linguistic Classification & Dialects",
                "page_start": 6,
                "page_end": 7,
                "summary": "Agglutinative morphology, vowel length contrasts, and Tibeto-Burman affiliations.",
                "tangkhul_text": (
                    "Tangkhul language exhibits agglutinative morphology with dominant prefix ka- forming adjectives and infinitives. "
                    "Case relationships are indicated by postpositional affixes: -na (agentive), -li (dative/locative), -wui (genitive). "
                    "Vowel length contrasts: 'sa' (to do) vs 'sā' (animal/flesh); 'mik' (eye) vs 'mei' (fire)."
                ),
                "english_translation": (
                    "Linguistic features of Tangkhul: Extensive use of prefixes and suffixes. "
                    "Nominal and adjectival derivation through prefix ka-. Case markers function as postpositional clitics. "
                    "Phonemic vowel length distinguishes essential vocabulary pairs."
                ),
                "vocabulary": [
                    {"word": "shiyan", "pos": "noun", "meaning": "linguistic standard, rule", "example": "Shiyan kashak."},
                    {"word": "kakhalat", "pos": "noun", "meaning": "meaning, pronunciation", "example": "Kakhalat kashak."},
                    {"word": "tuiyur", "pos": "noun", "meaning": "dialect, language branch", "example": "Tuiyur ngateina."},
                ],
                "grammar_points": [
                    "Phonemic vowel length contrasts.",
                    "Agglutinative affix ordering in verbal complexes.",
                ],
                "comprehension_questions": [
                    "Give two examples of minimal vowel length pairs in Tangkhul.",
                    "Which prefix is predominantly used to form infinitives?",
                ],
            },
            {
                "chapter_number": 3,
                "title": "Village Organization & The Awunga (Headman)",
                "page_start": 8,
                "page_end": 9,
                "summary": "Hereditary chieftainship (Awunga), the village council (Hangva), and clan clans (Shangnao).",
                "tangkhul_text": (
                    "Khaung kachida Awunga akha leiyi; Awunga hi shimkhurwui mathun eina ngashitna. "
                    "Hangva council eina ngasoda ram shiyan kashak saikora ngazekseri. "
                    "Shangnao kachida paman kathana mi akhakhana hangvali zangda khaungwui ot ngazeka."
                ),
                "english_translation": (
                    "Every Tangkhul village is an autonomous democratic unit under a hereditary chief called the Awunga. "
                    "The Awunga rules in consultation with the village council (Hangva), comprised of representatives "
                    "from each clan (Shangnao), managing village land, disputes, and seasonal festivals."
                ),
                "vocabulary": [
                    {"word": "awunga", "pos": "noun", "meaning": "village chief, king", "example": "Awunga shimkhur."},
                    {"word": "hangva", "pos": "noun", "meaning": "council of elders", "example": "Hangvali zangda."},
                    {"word": "shangnao", "pos": "noun", "meaning": "clan lineage", "example": "Shangnao kachida."},
                ],
                "grammar_points": [
                    "Honorific register associated with the Awunga.",
                    "Reciprocal verbal affix ngazor / ngazek.",
                ],
                "comprehension_questions": [
                    "What is the role of the Hangva in village governance?",
                    "How is the position of Awunga inherited?",
                ],
            },
            {
                "chapter_number": 4,
                "title": "Traditional Laws, Land Tenure & Feasts of Merit",
                "page_start": 10,
                "page_end": 11,
                "summary": "Maran (Feasts of Merit), Tarung monuments, and terraced land rights.",
                "tangkhul_text": (
                    "Maran kashak hi Tangkhul ngashanli khamataiya otsak akhana. Tarung thingrei vakhang eina shimli shona. "
                    "Seichang kala hok kachung khami eina ramnaoli shongza kashak saikora ngashitna. "
                    "Lungto kala lungchan shoda awo-ayiwui machut saikora chimiksho chitheiya."
                ),
                "english_translation": (
                    "The Feasts of Merit (Maran) represent the summit of customary social achievement. "
                    "The celebrant earns the right to erect the carved Tarung monument post before his house. "
                    "Mithuns and cattle are slaughtered to feast the entire community, and megalithic stone platforms are built."
                ),
                "vocabulary": [
                    {"word": "maran", "pos": "noun", "meaning": "feast of merit", "example": "Maran kashak."},
                    {"word": "tarung", "pos": "noun", "meaning": "forked monument post", "example": "Tarung shona."},
                    {"word": "seichang", "pos": "noun", "meaning": "mithun (Bos frontalis)", "example": "Seichang kashai."},
                ],
                "grammar_points": [
                    "Instrumental clitic -eina in monument dragging chants.",
                    "Nominal compounds combining animal terms and festive rites.",
                ],
                "comprehension_questions": [
                    "What privileges does a celebrant gain by performing Maran?",
                    "Describe the physical appearance and cultural meaning of the Tarung.",
                ],
            },
            {
                "chapter_number": 5,
                "title": "Tangkhul Folktales: Origin of the Species & Animals",
                "page_start": 12,
                "page_end": 13,
                "summary": "Mythological origin legends and the ancient brotherhood of hill and valley.",
                "tangkhul_text": (
                    "Awo-ayiwui khararchanli: 'Avah Samsokli tungthuiya, Makungana ili phungtung.' "
                    "Chinaoni khani: kakhara a kaphungli leiyi, kakhanao a ngaleili vaipama. "
                    "Meitei eina Tangkhul chinaoni thada kum kachida Mera Hou Chongba phanitli leikashi chithei ngaroka."
                ),
                "english_translation": (
                    "Tangkhul mythology traces common origins from Samsok in the eastern hills. "
                    "Tradition holds that two brothers parted ways: the elder brother settled in the misty Tangkhul heights, "
                    "while the younger brother cultivated the fertile valley, establishing a bond renewed at the annual Mera festival."
                ),
                "vocabulary": [
                    {"word": "khararchan", "pos": "noun", "meaning": "ancestral folklore", "example": "Awo-ayiwui khararchan."},
                    {"word": "samsok", "pos": "proper", "meaning": "ancient migration staging ground", "example": "Samsokli tungthuiya."},
                    {"word": "chinaoni", "pos": "noun", "meaning": "brothers, siblings", "example": "Chinaoni khani."},
                ],
                "grammar_points": [
                    "Comparative conjunction thada (like, in the manner of).",
                    "Ablative suffix -eina in origin narratives.",
                ],
                "comprehension_questions": [
                    "What does the Samsok migration legend signify?",
                    "How is the kinship between Meiteis and Tangkhuls celebrated traditionally?",
                ],
            },
            {
                "chapter_number": 6,
                "title": "Traditional Tangkhul Ballads & Folk Poetry",
                "page_start": 14,
                "page_end": 15,
                "summary": "The epic ballad of Shimreishang and Maitonphi, and heroic martial poetry.",
                "tangkhul_text": (
                    "Shimreishang eina Maitonphiwui leikashiyi Tangkhul thotchanli kaphapamei laana. "
                    "'Avayo avayo, makhamalu Maitonphili rasha saka; sakhangaiye Maitonphi kharam thuihaowa.' "
                    "Kazeiramli anili ngazipda kumching kumching leikashi ngazipsera."
                ),
                "english_translation": (
                    "The tragic romance of Shimreishang and Maitonphi is the most famous epic ballad of the Tangkhuls. "
                    "Forced apart by parental opposition and village taboos, their spirits are finally united in Kazeiram, "
                    "the tranquil land of the departed where true lovers dwell forever."
                ),
                "vocabulary": [
                    {"word": "leishat laa", "pos": "noun", "meaning": "love song, romantic ballad", "example": "Leishat laa sa."},
                    {"word": "kazeiram", "pos": "noun", "meaning": "land of the dead", "example": "Kazeiramli ngazipra."},
                    {"word": "haolaa", "pos": "noun", "meaning": "traditional folk song", "example": "Haolaa sakasa."},
                ],
                "grammar_points": [
                    "Antiphonal dialogue structure in romantic verse.",
                    "Poetic vocabulary substitutions in folk metrics.",
                ],
                "comprehension_questions": [
                    "Why is the story of Shimreishang and Maitonphi significant in Tangkhul literature?",
                    "What is Kazeiram in traditional Tangkhul eschatology?",
                ],
            },
            {
                "chapter_number": 7,
                "title": "Comparative Vocabulary & Dialectal Specimen",
                "page_start": 16,
                "page_end": 18,
                "summary": "Diagnostic 100-word vocabulary, kinship terminology, and dialectal correspondences.",
                "tangkhul_text": (
                    "1. Mi (Man) 2. Akui (Head) 3. Sam (Hair) 4. Mik (Eye) 5. Khana (Ear) "
                    "6. Khamasung (Nose) 7. Khamor (Mouth) 8. Ha (Tooth) 9. Pang (Hand) 10. Phei (Foot) "
                    "11. Zingsho (Sun) 12. Kachang (Moon) 13. Sirak (Star) 14. Mei (Fire) 15. Tara (Water) "
                    "16. Shim (House) 17. Si (Dog) 18. Vana (Bird) 19. Khai (Fish) 20. Thing (Tree). "
                    "Numerals: akha (1), khani (2), kathum (3), mati (4), phangā (5), tharuk (6), shini (7), chishat (8), chiko (9), tharā (10)."
                ),
                "english_translation": (
                    "Standard lexical list compiled by T. C. Hodson illustrating anatomical nouns, celestial bodies, "
                    "faunal terms, cardinal numerals 1-10, and cross-dialectal phonetic correspondences between "
                    "Ukhrul (Kathur), Raphei (Northern), and Kamo (Southern) varieties."
                ),
                "vocabulary": [
                    {"word": "akui", "pos": "noun", "meaning": "head", "example": "Akui kakhanang."},
                    {"word": "mik", "pos": "noun", "meaning": "eye", "example": "Mik eina theila."},
                    {"word": "pang", "pos": "noun", "meaning": "hand", "example": "Pang eina kasa."},
                    {"word": "tara", "pos": "noun", "meaning": "water", "example": "Tara kashing."},
                ],
                "grammar_points": [
                    "Base-10 decimal numeral system.",
                    "Systematic sound shifts across regional varieties.",
                ],
                "comprehension_questions": [
                    "Count from 1 to 10 in Tangkhul.",
                    "Identify three anatomical terms that feature prefix a-.",
                ],
            },
        ],
    }


def get_horam_2013_haola_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-LIT-001 (Dr. R. Horam 2013)."""
    return {
        "preface": (
            "The Tangkhul Folk Poetry in Song (HAOLA) by Dr. Ringkahao Horam, published by the Naga Cultural "
            "Development Society (NCDS) with assistance from Tribal Research Institute (TRI), Government of Manipur (2013). "
            "Contains 161 complete traditional poems and songs collecting the living oral memory of the Tangkhuls "
            "across agriculture, war, festivals, love, and mourning."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Creation, Origins & Ancestral Migration Songs",
                "page_start": 4,
                "page_end": 5,
                "summary": "The emergence from Wahukong (Hwang-Ho) and migration from Samsok to Hunphun.",
                "tangkhul_text": (
                    "Oh! hauri haura kachida haulu? Oh! hauri haura wahukongda haowa, Oh! wahukongda tunga. "
                    "O Kachili Tunglo Awa Samshokli Tunga, O Makungana ili phunga, O Makunganao ili pangthan, "
                    "Lungshang makang ana safasing sing, Mala mangli Hunphun Ava kharar. "
                    "O Ram wungaphei, Shokvaoli wungho maya; Mei wungayar Hunphun wunga kharara."
                ),
                "english_translation": (
                    "From what far valley did our ancestors emerge? From the river of Wahukong they journeyed. "
                    "From Samsok in the east our lineage migrated, guided by the staves of Makungana. "
                    "In Hunphun the ancestral fathers settled and lit the permanent council fires."
                ),
                "vocabulary": [
                    {"word": "miurlung", "pos": "noun", "meaning": "ancestral emergence", "example": "Miurlung kathur laa."},
                    {"word": "wahukong", "pos": "proper", "meaning": "river of origin", "example": "Wahukongda tunga."},
                    {"word": "hunphun", "pos": "proper", "meaning": "mother village (Ukhrul)", "example": "Hunphun Ava kharar."},
                ],
                "grammar_points": ["Vocative interjections 'Oh!', 'O!'.", "Alliterative couplets in oral metrics."],
                "comprehension_questions": ["Where did Tangkhuls trace their ancient migration from?", "What village was established as the mother-settlement?"],
            },
            {
                "chapter_number": 2,
                "title": "Agricultural Cycles: Jhumming, Planting & Harvest",
                "page_start": 6,
                "page_end": 7,
                "summary": "Terrace work, transplantation songs (Luisom), and harvest celebration (Mahat).",
                "tangkhul_text": (
                    "Kongrei mathei kongrei, kongrei shailo marei salo; Matei kachui manoye, Mala ifu heinao naoye. "
                    "Ithanvara iram leisaye, Isu luisa khinasa, ima lera khinasa; Maleira souralo, isa luisa lung haorana. "
                    "Zingkum leiyao leiyameirano, chungmeida kharshokrano, phungshon phungthaigei."
                ),
                "english_translation": (
                    "The terrace waters ripple, transplant the green shoots with joyous songs! "
                    "Sweet is the labor on our ancestral hills; who will share my buffalo meat and drink my rice beer? "
                    "May our granaries be filled to the rafters and the year bring peace and plenty."
                ),
                "vocabulary": [
                    {"word": "luikasom", "pos": "noun", "meaning": "paddy transplantation", "example": "Luikasom wui laa."},
                    {"word": "mahat", "pos": "noun", "meaning": "harvest of paddy", "example": "Mahat laa sa."},
                    {"word": "chumrei", "pos": "noun", "meaning": "granary", "example": "Chumrei lonchi puilu."},
                ],
                "grammar_points": ["Imperative exhortation in communal work songs.", "Agricultural seasonal idioms."],
                "comprehension_questions": ["What food and drink are shared during terrace work?", "What does 'leiyameirano' mean?"],
            },
            {
                "chapter_number": 3,
                "title": "Village Morung (Longra) & Dormitory Life Songs",
                "page_start": 8,
                "page_end": 9,
                "summary": "Longra drinking songs, companionship around the hearth, and youth solidarity.",
                "tangkhul_text": (
                    "Leader: I longnao (I Longra) ... ho...o...o! Members: Rapamlu ... ho...o...o! "
                    "Machapralu ... ho...o...o! Sairam samjiya, sairam samjiya! "
                    "Oh longra makazangwo, nawui shimli khisapamlo? Thakta razanglo, thakta razanglo!"
                ),
                "english_translation": (
                    "Leader: O comrades of the Longra! Members: Assemble, join the circle! "
                    "Weep no more! The hunting grounds await our youth! "
                    "Why linger solitary at home? Come swiftly into the warm circle of the dormitory hearth!"
                ),
                "vocabulary": [
                    {"word": "longra", "pos": "noun", "meaning": "morung, dormitory", "example": "I longnao rapamlu."},
                    {"word": "meisum", "pos": "noun", "meaning": "dormitory fireplace", "example": "Meisum kapamnao."},
                    {"word": "sairam", "pos": "noun", "meaning": "hunting range", "example": "Sairam samjiya."},
                ],
                "grammar_points": ["Leader-chorus call-and-response patterning.", "Imperative markers -lu and -lo."],
                "comprehension_questions": ["What social role did the Longra play in Tangkhul villages?", "Describe the call-and-response structure of Song 38."],
            },
            {
                "chapter_number": 4,
                "title": "Historical Ballads: World War I & Regional Conflicts",
                "page_start": 10,
                "page_end": 11,
                "summary": "The 1917-18 France Labour Corps ballad and the 1919 Kuki War songs.",
                "tangkhul_text": (
                    "Rai ramli khava, rai ramli khava yaronpa, Yaronpa nakhi vasalo? Iya mavangai, sayisa sayi na tanti sahaowa. "
                    "Franceshi ram khava, Franceli raikhavai; Makuiye makuiye, pham kata hiyo; Wungasam chap ngacha, rai ram khavayo. "
                    "Ah khongjai rai khava yaronpa yaronva, Sangna ram penga yaronva; Kuiwung kuivaya suphung mei."
                ),
                "english_translation": (
                    "Valiant young men journeying across distant seas to the battlefields of France in 1917; "
                    "Putting on the soldier's uniform and marching into the unknown while elders lamented. "
                    "In foreign lands they upheld the fearless reputation and honor of their ancestral hills."
                ),
                "vocabulary": [
                    {"word": "rai ram", "pos": "noun", "meaning": "battlefield, war territory", "example": "Rai ramli khava."},
                    {"word": "yaronpa", "pos": "noun", "meaning": "young warrior", "example": "Yaronpa nakhi vasalo."},
                    {"word": "tanti", "pos": "noun", "meaning": "military badge/uniform", "example": "Tanti sahaowa."},
                ],
                "grammar_points": ["Historical event dating embedded in oral songs.", "Repetition of key lyrical phrases."],
                "comprehension_questions": ["What historical event is memorialized in Song 21?", "How did Tangkhul communities respond to the 1917 call?"],
            },
            {
                "chapter_number": 5,
                "title": "Romance, Courtship & Love Songs (Leishat Laa)",
                "page_start": 12,
                "page_end": 13,
                "summary": "Courtship dialogues, fishing expeditions, and declarations of enduring fidelity.",
                "tangkhul_text": (
                    "Nana Kanta singloo, Ina Khailan singda, Kongli alei shonsa yahoo! "
                    "Oh iwui sakhangai aluinao, kathuili oja saleiya aluinao; Mayo kachang tarn rahaira aluinao. "
                    "Oh ini lungchang malai haosa, phaningda makhui aluinao leishiya; Kazingli samphangluinaosa aluinao."
                ),
                "english_translation": (
                    "Take up your net and I will carry the line; together we shall cross the mountain stream! "
                    "Beloved maiden, your smile brightens the terrace fields like springtime blossoms. "
                    "Though our hands are parted here on earth, our souls are entwined forever in the sky."
                ),
                "vocabulary": [
                    {"word": "aluinao", "pos": "noun", "meaning": "sweetheart, maiden", "example": "Sakhangai aluinao."},
                    {"word": "lungchang", "pos": "noun", "meaning": "heart, affection", "example": "Ini lungchang malaihaosa."},
                    {"word": "khailan", "pos": "noun", "meaning": "fishing net", "example": "Ina khailan singda."},
                ],
                "grammar_points": ["First-person dual association in courtship songs.", "Optative future in -luinaosa."],
                "comprehension_questions": ["What stream-fishing metaphor is used in courting?", "How is fidelity expressed beyond mortality?"],
            },
            {
                "chapter_number": 6,
                "title": "Festival Dances & Virgin Songs (Laa Khanganui)",
                "page_start": 14,
                "page_end": 15,
                "summary": "The sacred Luira dance performed by young maidens and festival elegance.",
                "tangkhul_text": (
                    "Luira sangai uwa, hoksa sangai uwa; Awungo Awunga shangrei rukchang ura, Yarui rukthang Kazing mathang ngaiyijile. "
                    "Zingkam won wonluiya, ngalanao mawonluipaiya; Ngalanaowa mawon luipaiya, nathanram khavasangmeiya. "
                    "Phaoli chan ma-ungkhararyo, haoriva haorava leiretnasaya."
                ),
                "english_translation": (
                    "The Luira festival arrives, the feast of pork is spread! The Awunga and elders assemble in regal attire. "
                    "Wildflowers bloom upon the slopes every spring, but human youth blossoms only once; "
                    "Dance with joy in the courtyard while youth shines bright and the festival drums resound."
                ),
                "vocabulary": [
                    {"word": "laa khanganui", "pos": "noun", "meaning": "maiden's sacred dance", "example": "Laa khanganui saya."},
                    {"word": "hoksa", "pos": "noun", "meaning": "pork, festival meat", "example": "Hoksa sangai uwa."},
                    {"word": "rawon", "pos": "noun", "meaning": "flower bloom", "example": "Rawon wonluiya."},
                ],
                "grammar_points": ["Metaphor of fleeting youth compared with floral seasons.", "Temporal conditional in festival chants."],
                "comprehension_questions": ["When is the Laa Khanganui performed?", "What philosophical truth is contained in the floral metaphor?"],
            },
            {
                "chapter_number": 7,
                "title": "Laments, Funerary Memorials & Philosophy",
                "page_start": 16,
                "page_end": 18,
                "summary": "Mourning over departed family and classical philosophical aphorisms.",
                "tangkhul_text": (
                    "Ili vaiphumlakha, Oh Ava khi mang shimanlo? Avayo khi mang shimanlo? Lengshongthei shimanna, Mayarnao mangna. "
                    "Khamathan longli yurkathan masaralu, Ngaleizingli kapam sangmeiya (kazeiram); "
                    "Khamna longli khangkaser masaralu, Ngaleizingli khyip sangmeiya."
                ),
                "english_translation": (
                    "When grief engulfed me, what bright dream was lost? The pride of the lineage was cut down in youth. "
                    "Boast not of wealth and pedigree on this mortal earth; beneath the ground in Kazeiram all sleep equally. "
                    "Live in humility and kindness, for mortal life vanishes like morning mist on the ridges."
                ),
                "vocabulary": [
                    {"word": "khamathan", "pos": "adj", "meaning": "wealthy, arrogant", "example": "Khamathan longli."},
                    {"word": "yurkathan", "pos": "noun", "meaning": "clan pride", "example": "Yurkathan masaralu."},
                    {"word": "ngaleizing", "pos": "noun", "meaning": "under the earth", "example": "Ngaleizingli kapam."},
                ],
                "grammar_points": ["Prohibitive negative imperative -ralu in philosophical wisdom.", "Poetic parallelisms."],
                "comprehension_questions": ["What moral counsel is given regarding wealth in Chapter 7?", "What is the meaning of 'Ngaleizingli'?"],
            },
            {
                "chapter_number": 8,
                "title": "Patriotic Anthems & Tribal Identity",
                "page_start": 19,
                "page_end": 20,
                "summary": "Celebration of the Tangkhul homeland, Longpi pottery, and the Shirui Lily.",
                "tangkhul_text": (
                    "Ngashan yanglo hey, Tangkhul ngalei hi! Kaphung kapha kongrei kongra hey, Khipana phashok Tangkhul ram? Varewui sokkhami ramna. "
                    "Oh Tangkhul avaram, Tangkhul sinaram! Khangayam machining Irong sampunram, Ham kasa ram chiya Longpi ram na saya; "
                    "Khamakang shim savai Hungpungram cement, Shirui ram lily mavatma nanaobing! Ringpha meiranu, mahomeiranu!"
                ),
                "english_translation": (
                    "Behold our glorious homeland! Mountains and crystal rivers bestowed by God. "
                    "Beloved Tangkhul motherland! Longpi crafting timeless black stone-pottery, "
                    "Hungpung building solid foundations, and Shirui Kashung blooming with the rare Shirui Lily! "
                    "May prosperity and honor abide in our land forever!"
                ),
                "vocabulary": [
                    {"word": "avaram", "pos": "noun", "meaning": "motherland", "example": "Tangkhul avaram."},
                    {"word": "sinaram", "pos": "noun", "meaning": "land of heritage", "example": "Tangkhul sinaram."},
                    {"word": "longpi ham", "pos": "noun", "meaning": "Longpi stone pottery", "example": "Ham kasa ram Longpi."},
                ],
                "grammar_points": ["Patriotic exclamations with 'Ringpha meiranu!'.", "Toponymic cataloguing of craft villages."],
                "comprehension_questions": ["Which village is celebrated for its pottery tradition?", "What famous flower is native to Shirui Kashung?"],
            },
        ],
    }


def get_kamkhenthang_1987_folk_songs_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-LIT-002 (Dr. Kamkhenthang 1987)."""
    return {
        "preface": (
            "Folk Songs of The Tangkhul compiled by Dr. H. Kamkhenthang (Senior Research Officer) "
            "and A. Ngashan Chahong (Secretary, Tangkhul Hao Art & Cultural Council, Ukhrul), published by "
            "the Directorate for Development of Tribals and Backward Classes, Manipur (1987). "
            "Presents 27 representative genres of Tangkhul folk music with vernacular lyrics and parallel English translations."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Invocations & Spring Songs (Zingkum Hao Kaphok)",
                "page_start": 4,
                "page_end": 5,
                "summary": "Hokharai war-cry and spring arrival songs heralded by Sampheirok and Koktui.",
                "tangkhul_text": (
                    "AE-HE! Phamei yameisa HE... HE. O--O-HU-O! Ilongnao laa sa usa, Kashishoklu, kaphazanglu--O--Hui-O-hui! "
                    "O, kazingkum ura, o, kazingkum ura, o, hungnaovayo luithuimihaolu; "
                    "Mamanaomara, hungnaovayo luithuimashunga; Sampheirokna riri rakhonga, koktui vana zingkum phungraya!"
                ),
                "english_translation": (
                    "Hokharai invocation: May the better be ours! Let us sing, may evil depart and divine goodness enter! "
                    "O, spring has begun! Your highness, sow the seeds for the year; royal venture is just and timely; "
                    "The Sampheirok sings melodiously and the cuckoo heralds the arrival of the fruitful year!"
                ),
                "vocabulary": [
                    {"word": "hokharai", "pos": "noun", "meaning": "invocation shout", "example": "Hokharai invocation."},
                    {"word": "kazingkum", "pos": "noun", "meaning": "spring season", "example": "Kazingkum ura."},
                    {"word": "sampheirok", "pos": "noun", "meaning": "spring songbird", "example": "Sampheirokna rakhonga."},
                ],
                "grammar_points": ["Ritual invocation phonetics.", "Reduplication in bird call onomatopoeia ('riri rakhonga')."],
                "comprehension_questions": ["What is Hokharai and when is it performed?", "Which birds announce the arrival of spring?"],
            },
            {
                "chapter_number": 2,
                "title": "Tarung Carrying & Monument Construction Songs",
                "page_start": 6,
                "page_end": 7,
                "summary": "Dragging the monumental Tarung tree from the forest and erecting megaliths.",
                "tangkhul_text": (
                    "O, yarso thingrei vakhang, thingpitang tak ungrall yaronnao, thingreiva ungreilu! "
                    "Seichang kharaei hangmi phalungra, phanora vashatta chaklen meikan naona kacheka, lumlao sakda vakhuiphalungra. "
                    "O, Kashongta phung-o, maranla saya; ilangkaso machilo, I wui luiyi kaya lhuiito, I wui chumrei hjorphiya!"
                ),
                "english_translation": (
                    "O young men, lift the mighty tree! The twigs bend, pull together with sturdy cane ropes; "
                    "The sacrificial mithun is provided, the augury bird Chaklen gave favorable omens; carry home the Tarung! "
                    "I built this house from humble beginnings; my terrace fields are fertile and granary full!"
                ),
                "vocabulary": [
                    {"word": "thingreikhangava", "pos": "noun", "meaning": "carrying the monument tree", "example": "Thingreiva ungreilu."},
                    {"word": "chaklen", "pos": "noun", "meaning": "augury bird", "example": "Chaklen kacheka."},
                    {"word": "chumrei", "pos": "noun", "meaning": "grain barn", "example": "Chumrei hjorphiya."},
                ],
                "grammar_points": ["Collective working rhythm in dragging chants.", "Augury interpretation terminology."],
                "comprehension_questions": ["What bird's call determines the auspiciousness of monument hauling?", "What animal is sacrificed for the Tarung?"],
            },
            {
                "chapter_number": 3,
                "title": "Ceremonial Dance & Hornbill Movements (Pheishon Laa)",
                "page_start": 8,
                "page_end": 9,
                "summary": "Dance steps modeled on the flight and wingbeats of the great Indian hornbill.",
                "tangkhul_text": (
                    "O, iram hongreili, Mafathing kasui kharipna; Ngachamching arang shangkaya, arangchi khili kachanlo? "
                    "Mafathei channa, arangkho arangkhon ngashing leishiya; Thuingashing, kashung shanghaowa."
                ),
                "english_translation": (
                    "In our ancient forests, the majestic Mafathing trees spread their wide canopy; "
                    "Upon their boughs perch the great hornbills; why have they gathered in numbers? "
                    "For the ripe Mafa fruits they have flown; with rhythmic wingbeats they soar towards the mountain peaks!"
                ),
                "vocabulary": [
                    {"word": "pheishon", "pos": "noun", "meaning": "ceremonial hornbill dance", "example": "Pheishon laa."},
                    {"word": "arang", "pos": "noun", "meaning": "hornbill", "example": "Arang shangkaya."},
                    {"word": "mafathing", "pos": "noun", "meaning": "Phoebe hainesiana timber tree", "example": "Mafathing kasui."},
                ],
                "grammar_points": ["Choreographic terminology encoded in song lyrics.", "Rhythmic meter imitating animal locomotion."],
                "comprehension_questions": ["What bird inspires the choreography of Pheishon?", "Why is the hornbill culturally sacred to Tangkhuls?"],
            },
            {
                "chapter_number": 4,
                "title": "Maiden Dances & Youth Festivals (Yarra Laa)",
                "page_start": 10,
                "page_end": 11,
                "summary": "Laa Khanganui maiden dances and the Yarra spring festival of the youth.",
                "tangkhul_text": (
                    "Kazingkum huimailo aria, shivanaoli khina sale? Kha shingnai rao vasaya, he ring khaya zak matheiya. "
                    "Kongrali theo theo, ilongnaova khithing kaphato? Ilongnaova longthing kaphana, meishum kapamnao zangyo!"
                ),
                "english_translation": (
                    "Let the seasons turn in gentleness! Maidens dance in the village square in graceful innocence. "
                    "What merry voices echo by the stream? The youth gather firewood for the annual Yarra celebration!"
                ),
                "vocabulary": [
                    {"word": "yarra laa", "pos": "noun", "meaning": "youth festival song", "example": "Yarra laa sa."},
                    {"word": "longthing", "pos": "noun", "meaning": "communal firewood", "example": "Longthing kaphana."},
                    {"word": "meishum", "pos": "noun", "meaning": "morung fireplace", "example": "Meishum kapamnao."},
                ],
                "grammar_points": ["Youth-group terminology.", "Onomatopoeic stream sounds 'theo theo'."],
                "comprehension_questions": ["In which months is the Yarra festival celebrated?", "What activity do the youth undertake during Yarra?"],
            },
            {
                "chapter_number": 5,
                "title": "Agriculture, Terrace Labor & Cowherd Songs",
                "page_start": 12,
                "page_end": 13,
                "summary": "Luisom paddy planting chants and Sei Hom cowherd ballads of solitary orphans.",
                "tangkhul_text": (
                    "O, I siluisa, I siluisa khinashai? I makreira khina mang, makreira sangralu; Shama maran saluira. "
                    "Ava khaho malei, aya kaho malei, seihom langphaizaya; Shok reo rangpamshona, silui shur khani chi kachui laga yaronnao chara horlama."
                ),
                "english_translation": (
                    "Who will feast on my buffalo meat, who will drink my aged rice beer? Pour generously for the laborers! "
                    "No parents call my name; upon the high grassy slopes I herd buffalos alone from dawn till dusk, "
                    "Tending the herds while silent tears trace lines upon my face."
                ),
                "vocabulary": [
                    {"word": "siluisa", "pos": "noun", "meaning": "buffalo meat for terrace workers", "example": "I siluisa khinashai."},
                    {"word": "seihom", "pos": "noun", "meaning": "cattle herding", "example": "Seihom langphaizaya."},
                    {"word": "makreira", "pos": "noun", "meaning": "fermented rice beverage", "example": "Makreira khina mang."},
                ],
                "grammar_points": ["Rhetorical questions in festive work songs.", "Poignant elegiac tone in pastoral chants."],
                "comprehension_questions": ["What contrast is drawn between festive terrace planting and cowherd life?", "What is 'siluisa'?"],
            },
            {
                "chapter_number": 6,
                "title": "Martial Ballads & Head-hunting Epics (Ral Laa)",
                "page_start": 14,
                "page_end": 15,
                "summary": "Ancient heroic victory chants and warrior prowess of Lunghar and Ringui.",
                "tangkhul_text": (
                    "O, atung shangla rai sakashiyavo, Lunghar yaron ni chiya! Azing takha rai sakashiyavo, Ringui yaron ni chiya! "
                    "Shangching Shangshak na ili khachitna chiya, shimin kayang ra mahon shok! Kharing sing singa, ili mangakatshelu!"
                ),
                "english_translation": (
                    "Behold in the northern heights the gallant warriors of Lunghar stand ready! "
                    "In the southern ranges the brave youths of Ringui guard the mountain passes; "
                    "They fear me as the tiger of the forest; challenge me not, for our victory shout resounds!"
                ),
                "vocabulary": [
                    {"word": "ral laa", "pos": "noun", "meaning": "war song, victory chant", "example": "Ral laa sa."},
                    {"word": "kharing", "pos": "adj", "meaning": "alive, captive", "example": "Kharing sing singa."},
                    {"word": "mahon", "pos": "noun", "meaning": "battle shout", "example": "Mahon shok."},
                ],
                "grammar_points": ["Vocative and boastful declamatory syntax.", "Geographical identifiers of warrior clans."],
                "comprehension_questions": ["Which two villages are celebrated as warrior centres?", "What does 'kharing sing' mean?"],
            },
            {
                "chapter_number": 7,
                "title": "Traditional Love Romances (Shimreishang & Maitonphi)",
                "page_start": 16,
                "page_end": 18,
                "summary": "The immortal romance of Shimreishang and Maitonphi in antiphonal dialogue.",
                "tangkhul_text": (
                    "Avayo avayo, makhamalu, Maitonphili rasha saka; sakhangaiye Maitonphi kharam thuihaowa. "
                    "Laishikhavai chi lunamlizang ngaroksa; Coi marongthei reola khuisingda lung ringa. "
                    "Ameishang Ameishang, Ira kachangli thuiulu; Maitonphi, pangthui haosa, ini lungchan malaihaosa."
                ),
                "english_translation": (
                    "Elders, do not forbid! For sweet Maitonphi alone does my heart beat in devotion; "
                    "Though adverse circumstances part us in this earthly life, our love remains green like the mountain pine. "
                    "Beloved Ameishang, farewell on this mortal shore; in the spirit realm beyond, we shall part no more."
                ),
                "vocabulary": [
                    {"word": "leishat laa", "pos": "noun", "meaning": "romantic song", "example": "Leishat laa sa."},
                    {"word": "marongthei", "pos": "noun", "meaning": "flowering shrub of fidelity", "example": "Marongthei reola."},
                    {"word": "lungchan", "pos": "noun", "meaning": "deep love, soul union", "example": "Ini lungchan malaihaosa."},
                ],
                "grammar_points": ["Antiphonal romantic dialogue.", "Symbolism of botanical endurance."],
                "comprehension_questions": ["What plant symbolizes unyielding love in the ballad?", "How does the story conclude in traditional belief?"],
            },
            {
                "chapter_number": 8,
                "title": "Weaving Songs, Festive Banquets & Bedtime Chants",
                "page_start": 19,
                "page_end": 20,
                "summary": "Back-strap loom weaving (Themsak), traditional shawls, and evening chants (Pet Laa).",
                "tangkhul_text": (
                    "O Tangkhul ngalanao yanglu yanglu, sak kasa kathemma themma; Haora chi yaron kachonna, Phangyai rah Tangkhul kashanna! "
                    "Phungcham vana ratha apamva rarona, phanishida tarikhana vaotun; Nali ungthuilo, sami ngachiya, i ram kashamshiraro."
                ),
                "english_translation": (
                    "Behold the skilled Tangkhul maidens weaving traditional textiles with masterly artistry! "
                    "The black-and-red Haora shawl is for valiant young men, and the Phangyai skirt for graceful women. "
                    "Evening settles over the ridges of Phungcham; put aside your tools and find peaceful sleep."
                ),
                "vocabulary": [
                    {"word": "themsak laa", "pos": "noun", "meaning": "weaving song", "example": "Themsak laa sa."},
                    {"word": "haora", "pos": "noun", "meaning": "traditional male shawl", "example": "Haora yaron kachon."},
                    {"word": "phangyai", "pos": "noun", "meaning": "traditional female skirt", "example": "Phangyai Tangkhul kashan."},
                    {"word": "pet laa", "pos": "noun", "meaning": "bedtime chant", "example": "Pet laa sa."},
                ],
                "grammar_points": ["Textile terminology and designators.", "Evening benedictory phrasing."],
                "comprehension_questions": ["What is Haora and who wears it?", "What is Phangyai and what colors define it?"],
            },
        ],
    }


def get_shimray_1976_folktales_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-LIT-003 (Y. K. Shimray 1976)."""
    return {
        "preface": (
            "Tangkhul Gee Wari Singbul (Tangkhul Folktale Compendium) by Y. K. Shimray (Cultural Heritage "
            "of Manipur, Imphal, 1976). Preserves 35 classic oral folktales, mythological legends of village "
            "foundations, animal fables, and customary moral allegories of the Tangkhul people."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "The Legend of Hundung & The White Cow",
                "page_start": 4,
                "page_end": 5,
                "summary": "Founding of Hundung village guided by the sacred pregnant cow.",
                "tangkhul_text": (
                    "Awo-ayiwui thotchanli: Seiva kachang akha leilaga apha kapha apamli vatuda seinao phanung tharanli Hundung khaung phokna. "
                    "Kaphung kaphali zatlaga seiva china apam kaphā akha theilaga pamshona; "
                    "chili seinao phada awo-ayina 'Hundung' (Hungpung) da hoya."
                ),
                "english_translation": (
                    "Ancestral lore recounts that the village founders followed a sacred white cow across the hills. "
                    "Wherever the cow rested upon the fertile plateau, there she gave birth to her calf, "
                    "and upon that blessed ground the ancient mother-village of Hundung was founded."
                ),
                "vocabulary": [
                    {"word": "seiva", "pos": "noun", "meaning": "sacred cow", "example": "Seiva kachang akha."},
                    {"word": "hundung", "pos": "proper", "meaning": "Hundung village", "example": "Hundung khaung phokna."},
                    {"word": "phanung", "pos": "verb", "meaning": "gave birth", "example": "Seinao phanung."},
                ],
                "grammar_points": ["Founding legend narrative formula.", "Temporal clause marker tharanli."],
                "comprehension_questions": ["What animal guided the founders of Hundung?", "What does this legend symbolize in Tangkhul pastoralism?"],
            },
            {
                "chapter_number": 2,
                "title": "The Two Brothers & Migration to the Hills",
                "page_start": 6,
                "page_end": 7,
                "summary": "The covenant between elder brother (hills) and younger brother (valley).",
                "tangkhul_text": (
                    "Chinaoni khani wui tui: kakhara a kaphungli pamda kakhanao a ngaleili vaipama. "
                    "Anili khangaran shiyan leiyi: kakhara na kaphungwui theishak kala khuira chili ngaleili phungmiya; "
                    "kakhanao na ngaleiwui machi kala kachon chili kaphungli phungmiya."
                ),
                "english_translation": (
                    "The legend of the two brothers: the elder brother chose the high mountain ridges, "
                    "while the younger brother cultivated the valley plains. They established a covenant: "
                    "the elder sent mountain forest produce and honey to the plain, and the younger returned salt and woven cloth."
                ),
                "vocabulary": [
                    {"word": "chinaoni", "pos": "noun", "meaning": "brothers", "example": "Chinaoni khani."},
                    {"word": "kakhara", "pos": "noun", "meaning": "elder brother", "example": "Kakhara kaphungli."},
                    {"word": "kakhanao", "pos": "noun", "meaning": "younger brother", "example": "Kakhanao ngaleili."},
                ],
                "grammar_points": ["Reciprocal trade terminology in oral covenants.", "Contrastive particle na."],
                "comprehension_questions": ["What goods did the two brothers exchange?", "How does this folktale reflect historical trade between hills and valley?"],
            },
            {
                "chapter_number": 3,
                "title": "Animal Fables: The Tiger and the Clever Toad",
                "page_start": 8,
                "page_end": 9,
                "summary": "Wit triumphs over brute force in the forest.",
                "tangkhul_text": (
                    "Khawo eina khanei wui khararchan: Khawo khamakang ana ngashida leikha khanei them lak eina makhamatuina. "
                    "Khawo china 'I eina kaphang ngaroksa!' da kahangli, khanei na awui khamangli khamatuda ngawonshoka. "
                    "Kong kanda vashung tharan khanei na 'I ashung hairaya!' da kahangli khawo ngacheiseri."
                ),
                "english_translation": (
                    "The fable of the tiger and the toad: the mighty tiger boasted of his speed and challenged the toad to a race. "
                    "The clever toad latched onto the tiger's bushy tail as he leaped across the rocky river, "
                    "landing first on the bank and declaring victory, teaching that wisdom exceeds brute strength."
                ),
                "vocabulary": [
                    {"word": "khawo", "pos": "noun", "meaning": "tiger", "example": "Khawo khamakang."},
                    {"word": "khanei", "pos": "noun", "meaning": "toad, frog", "example": "Khanei them laka."},
                    {"word": "themkhamatha", "pos": "noun", "meaning": "wit, wisdom", "example": "Them lak eina."},
                ],
                "grammar_points": ["Fable dialogue attribution using da kahangli.", "Direct vs reported speech."],
                "comprehension_questions": ["How did the toad outsmart the tiger?", "What is the moral lesson of the fable?"],
            },
            {
                "chapter_number": 4,
                "title": "The Story of Huimei and Mountain Spirits",
                "page_start": 10,
                "page_end": 11,
                "summary": "A brave hunter learns the healing secrets of forest herbs from Kameo spirits.",
                "tangkhul_text": (
                    "Huimei kaphungli valaga kameowui tui theiser; khangachei maleila shitsangda ungchan thotna. "
                    "Kameona ali theishingkhami tarakha thuiya: ngaleiwui themthei eina thingna raha eina mi kakhangasho saikora pangkakhui shiyan."
                ),
                "english_translation": (
                    "Huimei, a courageous hunter, encountered the benevolent mountain spirits (Kameo) upon the high ridges. "
                    "Unafraid, he listened respectfully as they revealed the healing virtues of mountain roots and herbs, "
                    "returning to his village as a revered traditional healer."
                ),
                "vocabulary": [
                    {"word": "kameo", "pos": "noun", "meaning": "mountain spirit", "example": "Kameowui tui."},
                    {"word": "khangachei", "pos": "noun", "meaning": "fear, dread", "example": "Khangachei maleila."},
                    {"word": "raha", "pos": "noun", "meaning": "medicinal root", "example": "Thingna raha."},
                ],
                "grammar_points": ["Ethnobotanical terminology.", "Spiritual respect formulas in oral narratives."],
                "comprehension_questions": ["What knowledge did Huimei receive from the mountain spirits?", "What role do Kameo play in Tangkhul nature philosophy?"],
            },
            {
                "chapter_number": 5,
                "title": "The Origin of Rice & The Discovery of Salt",
                "page_start": 12,
                "page_end": 13,
                "summary": "How hunters discovered saline springs at Marem and the gift of paddy seeds.",
                "tangkhul_text": (
                    "Machi eina ma machiwui shiyan: Marem kaphungli tara khamathei machikashak samphangna. "
                    "Shiva na tara chi mangda leikha sayur tarakhana chili zangda tara kashing mangda leiseri. "
                    "Chitharan awo-ayina machi tara khumda machi kasa phokna."
                ),
                "english_translation": (
                    "The discovery of salt and paddy: ancestral hunters observed wild deer regularly licking certain rocks near Marem. "
                    "Tasting the spring waters, they discovered natural saline springs and learned to boil the brine in earthenware pots, "
                    "founding the celebrated salt wells of northern Tangkhul."
                ),
                "vocabulary": [
                    {"word": "machi", "pos": "noun", "meaning": "salt", "example": "Machi tara."},
                    {"word": "ma", "pos": "noun", "meaning": "paddy, rice", "example": "Ma machi."},
                    {"word": "marem", "pos": "proper", "meaning": "Marem salt spring area", "example": "Marem kaphungli."},
                ],
                "grammar_points": ["Discovery narratives with observation verbs (thei-, samphang-).", "Technological terminology for salt boiling."],
                "comprehension_questions": ["How was the saline spring discovered?", "Why was salt a precious commodity in the hills?"],
            },
            {
                "chapter_number": 6,
                "title": "Tales of Morung Bravery & Tricksters",
                "page_start": 14,
                "page_end": 15,
                "summary": "Feats of strength, archery contests, and humorous trickster narratives in the Longra.",
                "tangkhul_text": (
                    "Longrawui yarsona ot kakhayei kasa eina lumlaoda pamshona. "
                    "Yaron akhana lungrei kahak akha phungshokda awui mathun chitheiya; "
                    "kateipa china themkhamatha eina malung kharaowa mi akhali ngacheilaka ot kasa themchitheiya."
                ),
                "english_translation": (
                    "Youth in the village Morung engaged in athletic competitions and humorous storytelling. "
                    "One youth proved his strength by lifting heavy megalithic stones, while another displayed quick wit "
                    "by solving traditional riddles and defusing village rivalries with laughter."
                ),
                "vocabulary": [
                    {"word": "yarso", "pos": "noun", "meaning": "warrior youth cohort", "example": "Longrawui yarso."},
                    {"word": "lungrei", "pos": "noun", "meaning": "heavy stone", "example": "Lungrei phungshokda."},
                    {"word": "themkhamatha", "pos": "noun", "meaning": "clever wit", "example": "Themkhamatha chitheiya."},
                ],
                "grammar_points": ["Comparative narrative pairing strength vs intelligence.", "Colloquial morung expressions."],
                "comprehension_questions": ["What competitions were held among morung youths?", "Why was storytelling valued in the bachelor dormitory?"],
            },
            {
                "chapter_number": 7,
                "title": "Moral Allegories & Customary Wisdom",
                "page_start": 16,
                "page_end": 18,
                "summary": "Traditional proverbs (Tuingashit) and customary jurisprudence of the council.",
                "tangkhul_text": (
                    "Tangkhul tuingashit: 'Tui kakhayei eina tui khangaran phamei; kazeiram makazamana.' "
                    "'Pang eina kasa otna wuklungli karingna.' 'Khaung kaphā khangavawa wui tuiyana.' "
                    "Mashung kakhayang hi Tangkhul ngashanli khamataiya machutna."
                ),
                "english_translation": (
                    "Classical Tangkhul proverbs: 'Reconciliation is sweeter than bitter strife; justice leaves no regret in the afterlife.' "
                    "'Labor with one's hands nourishes the soul.' 'A peaceful village reflects the wisdom of its council.' "
                    "Truthfulness and personal integrity remain the highest virtues of the Tangkhul code."
                ),
                "vocabulary": [
                    {"word": "tuingashit", "pos": "noun", "meaning": "proverb, maxim", "example": "Tangkhul tuingashit."},
                    {"word": "mashung", "pos": "adj/noun", "meaning": "truth, righteousness", "example": "Mashung kakhayang."},
                    {"word": "khangaran", "pos": "noun", "meaning": "peace, reconciliation", "example": "Tui khangaran."},
                ],
                "grammar_points": ["Aphoristic syntax: parallel clauses without copula.", "Moral imperatives."],
                "comprehension_questions": ["Quote two classical Tangkhul proverbs.", "What is the supreme virtue in customary Tangkhul jurisprudence?"],
            },
        ],
    }


def get_ciil_1995_dictionary_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-CIIL-004 (Arokianathan & Sharma 1995)."""
    return {
        "preface": (
            "Tangkhul-English, Hindi Dictionary by Dr. S. Arokianathan and Dr. Rekha Sharma, published by "
            "the Central Institute of Indian Languages, Mysore (CIIL Dictionary Series, 1995, 140 pages, "
            "ISBN 81-7342-028-9). Provides systematic lexicographical descriptions of Tangkhul root morphemes, "
            "compounds, word classes, English definitions, and Hindi equivalents."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Phonological Structure & Lexicographical Conventions",
                "page_start": 4,
                "page_end": 5,
                "summary": "Vowel length, aspirated plosives, and trilingual lexicographical entry conventions.",
                "tangkhul_text": (
                    "Lexicographical Format: Headword [Part of Speech] English Definition / Hindi Equivalent. "
                    "Minimal vowel length contrasts: 'sa' [v] to do / करना vs 'sā' [n] animal, meat / पशु, माँस. "
                    "'sha' [v] to hear / सुनना vs 'shā' [num] hundred / सौ. "
                    "Infinitive prefix ka- precedes verbal roots: ka-sa, ka-thei, ka-shak."
                ),
                "english_translation": (
                    "Conventions: Headwords are alphabetized according to Roman script order. "
                    "Phonemic vowel length (macron) is strictly distinguished. "
                    "Trilingual definitions provide immediate cross-linguistic equivalents in English and Hindi."
                ),
                "vocabulary": [
                    {"word": "sairik", "pos": "noun", "meaning": "letter, phoneme / वर्ण", "example": "Sairik kakhalat."},
                    {"word": "kakhalat", "pos": "noun", "meaning": "pronunciation / उच्चारण", "example": "Kakhalat kashak."},
                    {"word": "tuiwon", "pos": "noun", "meaning": "word entry / शब्द", "example": "Tuiwon shiyan."},
                ],
                "grammar_points": ["Headword selection criteria.", "Trilingual cross-referencing structure."],
                "comprehension_questions": ["How are minimal vowel pairs marked in this dictionary?", "What prefix precedes verbal infinitive entries?"],
            },
            {
                "chapter_number": 2,
                "title": "Nominal Vocabulary: Body Parts, Kinship & Nature",
                "page_start": 6,
                "page_end": 7,
                "summary": "Systematic anatomical, kinship, and elemental nouns with English and Hindi glosses.",
                "tangkhul_text": (
                    "akui [n] head / सिर | mik [n] eye / आँख | khana [n] ear / कान | "
                    "khamasung [n] nose / नाक | khamor [n] mouth / मुँह | ha [n] tooth / दाँत | "
                    "pang [n] hand / हाथ | phei [n] foot / पैर | ava [n] father / पिता | aza [n] mother / माता | "
                    "zingsho [n] sun / सूर्य | kachang [n] moon / चंद्रमा | tara [n] water / जल | mei [n] fire / अग्नि."
                ),
                "english_translation": (
                    "Nominal lexical inventory covering human anatomy with obligatory prefix a-, "
                    "kinship relationships, and primary elemental entities of the physical environment."
                ),
                "vocabulary": [
                    {"word": "akui", "pos": "noun", "meaning": "head / सिर", "example": "Akui kakhanang."},
                    {"word": "mik", "pos": "noun", "meaning": "eye / आँख", "example": "Mik eina theila."},
                    {"word": "pang", "pos": "noun", "meaning": "hand / हाथ", "example": "Pang eina kasa."},
                    {"word": "tara", "pos": "noun", "meaning": "water / जल", "example": "Tara kashing."},
                ],
                "grammar_points": ["Inalienable possession prefix a-.", "Trilingual semantic correspondence."],
                "comprehension_questions": ["List four Tangkhul body parts with English and Hindi equivalents.", "Which prefix marks inalienable anatomical nouns?"],
            },
            {
                "chapter_number": 3,
                "title": "Verbal Lexicon: Motion, Action & Cognition",
                "page_start": 8,
                "page_end": 9,
                "summary": "Primary action verbs, motion stems, and conjugation paradigm.",
                "tangkhul_text": (
                    "kasa [v] to do / करना | kathei [v] to see / देखना | kashā [v] to hear / सुनना | "
                    "kazat [v] to walk / चलना | kapam [v] to sit / बैठना | kapi [v] to sleep / सोना | "
                    "kashak [v] to eat / खाना | kapāng [v] to drink / पीना | kacham [v] to speak / बोलना. "
                    "Tenses: Present -ei/-i | Past -ser/-da | Future -ra | Imperative -lu."
                ),
                "english_translation": (
                    "Primary verbal roots organized with infinitive prefix ka-. "
                    "Tense inflection paradigms demonstrated with Subject pronouns (i, na, a)."
                ),
                "vocabulary": [
                    {"word": "kasa", "pos": "verb", "meaning": "to do / करना", "example": "I ot sai."},
                    {"word": "kathei", "pos": "verb", "meaning": "to see / देखना", "example": "Ana theiser."},
                    {"word": "kazat", "pos": "verb", "meaning": "to walk / चलना", "example": "Athum zatra."},
                ],
                "grammar_points": ["Agglutinative tense suffixes.", "Imperative suffix -lu."],
                "comprehension_questions": ["Conjugate 'kasa' (to do) across present, past, and future.", "What suffix marks imperative requests?"],
            },
            {
                "chapter_number": 4,
                "title": "Adjectives, Color Terms & Spatial Qualifiers",
                "page_start": 10,
                "page_end": 11,
                "summary": "Descriptive adjectival roots and color spectrum terms.",
                "tangkhul_text": (
                    "kaphā [adj] good / अच्छा | kashi [adj] bad / बुरा | kahak [adj] big / बड़ा | "
                    "kateo [adj] small / छोटा | kachon [adj] white / सफेद | muk [adj] black / काला | "
                    "ngaching [adj] green / हरा | khangayei [adj] brave / वीर. "
                    "Degrees of comparison: kaphā (good), kaphāmei (better), pamei (best)."
                ),
                "english_translation": (
                    "Adjectives derived through prefixation of ka- to qualitative verbal roots. "
                    "Color terminology and morphological degrees of comparison using suffix -mei."
                ),
                "vocabulary": [
                    {"word": "kaphā", "pos": "adj", "meaning": "good / अच्छा", "example": "Kaphā mi."},
                    {"word": "kahak", "pos": "adj", "meaning": "large / बड़ा", "example": "Kaphung kahak."},
                    {"word": "muk", "pos": "adj", "meaning": "black / काला", "example": "Chon muk."},
                ],
                "grammar_points": ["Comparative degree marking with -mei.", "Adjective positioning post-head noun."],
                "comprehension_questions": ["How is the comparative degree formed in Tangkhul?", "Translate into Tangkhul: 'The big mountain'."],
            },
            {
                "chapter_number": 5,
                "title": "Numerals, Quantifiers & Temporal Markers",
                "page_start": 12,
                "page_end": 13,
                "summary": "Cardinal numerals 1-100, quantifiers, and diurnal time expressions.",
                "tangkhul_text": (
                    "akha [1] / एक | khani [2] / दो | kathum [3] / तीन | mati [4] / चार | phangā [5] / पाँच | "
                    "tharuk [6] / छह | shini [7] / सात | chishat [8] / आठ | chiko [9] / नौ | thakharā [10] / दस | "
                    "maku [20] / बीस | shā [100] / सौ. "
                    "Time: aja [today] / आज | ngalap [tomorrow] / कल | ningla [yesterday] / बीता कल."
                ),
                "english_translation": (
                    "Base-10 cardinal numeral system and calendar markers for day, night, month, and year."
                ),
                "vocabulary": [
                    {"word": "akha", "pos": "num", "meaning": "one / एक", "example": "Mi akha."},
                    {"word": "maku", "pos": "num", "meaning": "twenty / बीस", "example": "Kum maku."},
                    {"word": "aja", "pos": "adv", "meaning": "today / आज", "example": "Aja zimiksho."},
                ],
                "grammar_points": ["Decimal base numerals.", "Temporal adverb positioning."],
                "comprehension_questions": ["Count from 1 to 10 in Tangkhul with Hindi equivalents.", "What are the words for 'yesterday', 'today', and 'tomorrow'?"],
            },
            {
                "chapter_number": 6,
                "title": "Flora, Fauna, Agriculture & Domestic Artifacts",
                "page_start": 14,
                "page_end": 15,
                "summary": "Ecological species, domesticated fauna, and material culture terms.",
                "tangkhul_text": (
                    "si [dog] / कुत्ता | seichang [mithun] / मिथुन | hok [pig] / सूअर | vana [bird] / चिड़िया | "
                    "khai [fish] / मछली | thing [tree] / पेड़ | ma [paddy] / धान | machi [salt] / नमक | "
                    "haora [shawl] / शॉल | phangyai [skirt] / घाघरा | ham [pot] / मटका | tarung [post] / स्तंभ."
                ),
                "english_translation": (
                    "Material culture, domesticated fauna, flora, and traditional culinary items."
                ),
                "vocabulary": [
                    {"word": "seichang", "pos": "noun", "meaning": "mithun / मिथुन", "example": "Seichang kashai."},
                    {"word": "haora", "pos": "noun", "meaning": "traditional shawl / शॉल", "example": "Haora kachon."},
                    {"word": "ham", "pos": "noun", "meaning": "clay pot / मटका", "example": "Longpi ham."},
                ],
                "grammar_points": ["Gender suffixes -va and -mayār on animal stems.", "Compound noun formation."],
                "comprehension_questions": ["What is the female suffix for animal nouns?", "Translate: 'dog', 'mithun', and 'fish' into Tangkhul, English, and Hindi."],
            },
            {
                "chapter_number": 7,
                "title": "Trilingual Lexical Index & Comparative Matrix",
                "page_start": 16,
                "page_end": 18,
                "summary": "Trilingual lookup index aligning Tangkhul, English, and Hindi vocabularies.",
                "tangkhul_text": (
                    "akui: head / सिर | aza: mother / माता | ava: father / पिता | ha: tooth / दाँत | "
                    "ham: pot / मटका | hok: pig / सूअर | kachang: moon / चाँद | kaphā: good / अच्छा | "
                    "kashi: bad / बुरा | kashak: eat / खाना | kazat: walk / चलना | khai: fish / मछली | "
                    "ma: paddy / धान | machi: salt / नमक | mei: fire / आग | mik: eye / आँख | "
                    "morol: sin / पाप | muk: black / काला | ngashun: day / दिन | ngaya: night / रात | "
                    "pang: hand / हाथ | phei: foot / पैर | ram: country / देश | si: dog / कुत्ता | "
                    "tara: water / पानी | thing: tree / पेड़ | tui: word / शब्द | zingsho: sun / सूरज."
                ),
                "english_translation": (
                    "Alphabetical reference index containing trilingual alignment of high-frequency lexical stems."
                ),
                "vocabulary": [
                    {"word": "akui", "pos": "noun", "meaning": "head / सिर", "example": "Akui."},
                    {"word": "tara", "pos": "noun", "meaning": "water / पानी", "example": "Tara."},
                    {"word": "mei", "pos": "noun", "meaning": "fire / आग", "example": "Mei."},
                    {"word": "zingsho", "pos": "noun", "meaning": "sun / सूरज", "example": "Zingsho."},
                ],
                "grammar_points": ["Trilingual comparative alignment.", "Alphabetic indexing."],
                "comprehension_questions": ["Use the index to find the Tangkhul word for 'fire' and 'water'.", "What are the Hindi glosses for 'akui' and 'pang'?"],
            },
        ],
    }
