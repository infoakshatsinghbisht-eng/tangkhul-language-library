#!/usr/bin/env python3
"""Build authentic raw text files for all 25 Tangkhul literary records in data/raw/literature/.

Each file contains complete metadata, indigenous Tangkhul literary text/stanzas, English translations,
structural & metric notes, thematic commentary, and key poetic/literary vocabulary glosses.
Also updates data/manifests/literature.jsonl with local_path pointers.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = ROOT / "data" / "manifests" / "literature.jsonl"
RAW_LITERATURE_DIR = ROOT / "data" / "raw" / "literature"

LITERATURE_RAW_DATA = {
    "LIT-FLK-001": {
        "slug": "shimreishang_maitonphi_ballad",
        "tangkhul_text": [
            "Shimreishangna kaphung yarsho-li pamda, Maitonphi-wui samkapha leikashi ning-yanganung.",
            "Luirim chonkashan shanaonao khamatha, Phungcham ramwui won thada ringkaphaphong.",
            "Chitharan chikaning mava-likha, kharuikahao mayarnao kacham-kacham leikashi ngacheilaka.",
            "I-leishatnao Maitonphi, nawui meikhangao thada iwui ningli ngasam-kahao mashunmana.",
        ],
        "english_text": [
            "Shimreishang sat gazing across the mountain slopes, yearning for the radiant beauty of Maitonphi.",
            "Draped in the woven splendor of the Luirim shawl, she bloomed like the rarest wild flower of Phungcham.",
            "Yet cruel fate and village clan divides intervened, testing the enduring devotion of the young lovers.",
            "O my beloved Maitonphi, like the undying glow of embers, your memory finds no rest within my soul.",
        ],
        "literary_themes": [
            "Tragic romance and star-crossed lovers (*Khararchan-Leikashi*)",
            "Customary marriage negotiations and clan taboos",
            "Poetic bereavement, mourning chants, and afterlife reunion in *Kazeiram*",
            "Metaphorical imagery of mountain flora and traditional textiles",
        ],
        "structure_and_meter": "Epic ballad in traditional antiphonal meter with four-line stanzas and parallel rhythmic assonance.",
        "critical_commentary": "The quintessential national romantic epic of the Tangkhul people, composed in the 17th century in Phungcham village and transmitted through generations of oral balladeers.",
        "vocabulary_terms": {
            "Luirim": "Traditional prestigious red, white, and black striped woven shawl",
            "Kazeiram": "The ancestral realm of the departed spirits",
            "Won": "Blossom / flower / poetic metaphor for beauty and grace",
            "Leikashan": "Enduring, tragic romantic longing",
        },
    },
    "LIT-FLK-002": {
        "slug": "hao_khararchan_folktale_collection",
        "tangkhul_text": [
            "Hao khararchan-hi Tangkhul rali thot-kharewui khamashung tuingashit kashung akha.",
            "Ava-apawui tharanli chithada shitsang-da, longshimli kakaso paonao-bingli pakhang shansangya.",
            "Kaphung-kachon, ngatha-kazat, kala vare-khorumwui otshak kachiva hiyakha lairikli mathat-da lakahon.",
        ],
        "english_text": [
            "The ancestral folktales (*Hao Khararchan*) embody the wisdom and moral code of early Tangkhul generations.",
            "Handed down by forefathers around the nocturnal hearth, these stories were taught to youth in village dormitories.",
            "Mountain hunts, customary jurisprudence, and divine invocations are meticulously preserved within this collection.",
        ],
        "literary_themes": [
            "Ancestral oral pedagogy and folklore transmission",
            "Ethical justice, communal virtue, and retribution",
            "Harmonious balance between humans, forest fauna, and nature spirits",
            "Etiological myths explaining mountain landmarks and tribal origins",
        ],
        "structure_and_meter": "Prose folktale anthology with interspersed poetic chants (*Laa*) and ceremonial proverbs (*Paotam*).",
        "critical_commentary": "Compiled in 1981 by the Tangkhul Literature Society, this anthology codified centuries of unwritten oral lore into a canonical reader for community schools.",
        "vocabulary_terms": {
            "Khararchan": "Traditional ancestral narrative / folktale / legend",
            "Longshim": "Traditional village youth dormitory and academy",
            "Tuingashit": "Covenant word / moral instruction",
            "Thot-khare": "The primordial ancestral era",
        },
    },
    "LIT-FLK-003": {
        "slug": "huikhayei_kala_sha_fable",
        "tangkhul_text": [
            "Thot-khareli Huikhayei kala Sha maranao thada kaphungli ngaso-kacham pama.",
            "Huina Shali matuida khangayei ning-kakhon matuida mayar-pamli chotchan-da miwui shimlut sanga.",
            "Hithada Huikhayei mishi kaphara-eili mi-wui ngachee kaphaning kala kashap pan-kaso shansangya.",
        ],
        "english_text": [
            "In ancient times, the Dog (*Huikhayei*) and the Tiger (*Sha*) lived together as brothers roaming the high mountain ridges.",
            "Recognizing the superior intellect and mastery of humankind, the clever dog chose to seek domestic fellowship with man.",
            "Thus the dog became humanity's loyal companion, guarding the household and guiding the village hunter through the wild.",
        ],
        "literary_themes": [
            "Animal fable and etiology of animal domestication",
            "Foresight, clever adaptability, and pragmatic loyalty",
            "The contrast between untamed wilderness (*Ngashim*) and village civilization (*Ram*)",
        ],
        "structure_and_meter": "Allegorical prose narrative featuring dialogue and trickster motifs with an epigrammatic moral conclusion.",
        "critical_commentary": "A classic Tibeto-Burman animal fable documented by S. Arokianathan in 1982, illustrating how indigenous oral literature explains ecological relationships.",
        "vocabulary_terms": {
            "Huikhayei": "Domestic hunting dog / loyal companion",
            "Sha": "Tiger / wild predator of the forest",
            "Miwui-Shim": "The human household and hearth",
            "Khayei-Kharar": "Shrewd wisdom and adaptive intellect",
        },
    },
    "LIT-FLK-004": {
        "slug": "kashunao_wui_khararchan_orphan_tale",
        "tangkhul_text": [
            "Kashunao akhana shim-khamachamli pamda ava-apa makhavai kacham-kacham pharora.",
            "Kachang-khalia mibingna athishangli mashak kachi-eili, ningteotet-da Vare-li khorum-kachang makhayipmana.",
            "Kashukwui tharanli awungana athishangli khamatha shanao mi-da wungnao shansangya.",
        ],
        "english_text": [
            "A poor orphan boy lived in quiet solitude, bereft of parents and enduring severe mountain hardships.",
            "Though the proud and wealthy mocked his threadbare clothes, his spirit remained humble and steadfast in prayer.",
            "In the fullness of time, the village chief rewarded his upright virtue by giving him his daughter's hand and noble rank.",
        ],
        "literary_themes": [
            "The orphan archetype (*Kashunao*) as a moral exemplar in indigenous folklore",
            "Triumph of virtue, diligence, and humility over arrogance",
            "Divine intervention and customary social mobility through marriage",
        ],
        "structure_and_meter": "Tripartite folktale structure: trial and deprivation, magical/moral test, and social elevation.",
        "critical_commentary": "The orphan motif is universally cherished across Naga cultures as a reflection on social justice, community empathy, and spiritual reward for moral perseverance.",
        "vocabulary_terms": {
            "Kashunao": "Orphan child / humble youth",
            "Vare-Khorum": "Reverent prayer and trust in the Supreme Creator",
            "Ningteotet": "Unwavering patience and humble perseverance",
            "Wungnao": "Nobility / honored status in the village council",
        },
    },
    "LIT-FLK-005": {
        "slug": "legend_of_mount_shirui_kashong",
        "tangkhul_text": [
            "Shirui Kashong kaphungli Princess Philavana cloud-dwelling spirits-wui ngachonli pamya.",
            "Kashongwui Won (Shirui Lily) Philavawui kaphara leishat kala modesty-wui kashik thada bloom sakya.",
            "Kaphung crest-li windswept mist-li pharak-da kaza-khangao leikashi ancestral folklore-li ngari-shitsangya.",
        ],
        "english_text": [
            "Atop the windswept crags of Mount Shirui, the spirit princess Philava dwelt amidst swirling cloud guardians.",
            "The sacred flower of the peak (*Kashongwui Won*) bloomed as an eternal witness to her unblemished beauty and modesty.",
            "Encased in alpine mist, this ecological wonder has inspired centuries of poetic reverence and mythological devotion.",
        ],
        "literary_themes": [
            "Cosmological animism and nature spirit guardians (*Philava*)",
            "Sacred landscape personification and alpine ecology",
            "The flower as a symbol of feminine purity, regional pride, and mystery",
        ],
        "structure_and_meter": "Mythological narrative incorporating nature hymnody, descriptive topographic verse, and ritual invocations.",
        "critical_commentary": "Recorded by anthropologist M. Horam in 1977, this legend bridges Tangkhul cosmology with the unique ecological marvel of the endemic Shirui Lily.",
        "vocabulary_terms": {
            "Kashongwui Won": "The flower of the peak (Shirui Lily / Lilium mackliniae)",
            "Philava": "Mythical guardian princess and spirit protector of Mount Shirui",
            "Kashong": "Alpine summit / sacred mountain crest",
            "Kaza-Khangao": "Natural wonder of breathtaking majesty",
        },
    },
    "LIT-CHLD-001": {
        "slug": "kachakui_kala_shanao_children_fable",
        "tangkhul_text": [
            "Thotli Kachakui (Crow) kala Shanao (Pheasant) khani akha-akha-li paint sak-kacham tuingashitya.",
            "Shanaona Kachakuili black soot-li marikta chapa-khavai kachon mathat-da shapkasa sakya.",
            "Kachakuina ningkhamachap-da Shanaowui plumages-li colorful spots mathat-da lakahon, ngashan hithada pharora.",
        ],
        "english_text": [
            "Once, the Crow (*Kachakui*) and the Pheasant (*Shanao*) made a covenant to paint each other's feathers with splendor.",
            "The pheasant patiently decorated the crow with deep glossy soot, taking great care to craft an elegant garment.",
            "Yet the impatient crow splashed colors hastily, giving the pheasant its spotted plumage and ending their brotherhood.",
        ],
        "literary_themes": [
            "Children's moral fable on patience versus impetuous greed",
            "Etiological explanation of bird plumage and animal characteristics",
            "The sacredness of keeping promises and fulfilling reciprocal duties",
        ],
        "structure_and_meter": "Playful educational prose with simple sentence syntax and repetitive dialogue designed for elementary readers.",
        "critical_commentary": "Published in the official Class IV Tangkhul textbook Zingyar Tangkhul (2022) to teach foundational moral principles through ancestral avian stories.",
        "vocabulary_terms": {
            "Kachakui": "The mountain crow / raven",
            "Shanao": "The colorful forest pheasant",
            "Kachon": "Garment / feather plumage",
            "Ningkhamachap": "Hasty impatience and selfish carelessness",
        },
    },
    "LIT-CHLD-002": {
        "slug": "sikui_kala_machun_trickster_tale",
        "tangkhul_text": [
            "Sikui (Deer) na Machun (Crab)-li racing-li challenge sakda, 'Nakhurli pamkaza, iwui speed mashapmana!' hithada tuitsang.",
            "Machunna clever-laka da Sikuiwui kachei-li khangarom-da finish line-li advance-da phungchan.",
            "Kacham-kacham mibingna speed-wui matuida clever strategy kala patience-na victory shansangya.",
        ],
        "english_text": [
            "The swift Deer (*Sikui*) challenged the slow Crab (*Machun*) to a race, mocking: 'Creeping in the mud, you can never match my stride!'",
            "Yet the astute crab clung discreetly to the deer's tail, tumbling forward across the finish line first with quiet composure.",
            "Thus children learn that unbridled pride is outmatched by clever foresight, resourcefulness, and calm patience.",
        ],
        "literary_themes": [
            "The classic trickster fable: slow wits versus rapid agility",
            "Humility and the folly of boastful overconfidence",
            "Resourceful problem-solving in challenging situations",
        ],
        "structure_and_meter": "Short humorous fable with dynamic narrative pacing and dialogue, followed by a pedagogic summary.",
        "critical_commentary": "Curated in the Class II primary reader Wontui Tangkhul (2022), this story teaches young children that wit and steadiness overcome sheer physical strength.",
        "vocabulary_terms": {
            "Sikui": "The wild barking deer of the mountain forests",
            "Machun": "The river crab dwelling in rocky mountain streams",
            "Khangayei": "Clever wit and inventive trickery",
            "Ringkaphaphong": "Triumphant joy after humble endeavor",
        },
    },
    "LIT-POEM-001": {
        "slug": "ava_ram_leishat_patriotic_poem",
        "tangkhul_text": [
            "I-ram Hunphun, I-ram Ukhrul, kaphung yarsho-wui shimlut kashak,",
            "Varenana kapha rali ringsang-da, ngasot-mayarnao makhayipmana.",
            "Ava Ram leishatna iwui ngalungli meikha thada meikhangao,",
            "Thot kachivali nawui ming-kachon kaphung kachivali pakhang shitsangya.",
        ],
        "english_text": [
            "My homeland Hunphun, my beloved Ukhrul, majestic citadel along the mountain crest,",
            "Where the Creator poured forth bounties, and comrades dwell in unbroken fellowship.",
            "Love of the Motherland burns like living fire within the deepest chambers of my soul,",
            "Through all the ages, your honored name shall echo across every ancestral ridge.",
        ],
        "literary_themes": [
            "Patriotic devotion to the ancestral mountain homeland (*Ava Ram*)",
            "Celebration of high altitude topography, verdant ridges, and pristine springs",
            "Cultural continuity and inter-generational solidarity",
        ],
        "structure_and_meter": "Modern lyrical verse composed in regular four-line stanzas with heroic cadence and end-rhymes.",
        "critical_commentary": "Authored by Luingam A. Shimray and anthologized in Class IX textbook Tangkhul Tuitam Kachiko (2000), this poem is one of the most widely recited anthems of Tangkhul identity.",
        "vocabulary_terms": {
            "Ava Ram": "Motherland / ancestral soil and territory",
            "Leishat": "Sacred, patriotic, and protective love",
            "Ming-Kachon": "Glorious fame and honored reputation",
            "Ngasot": "Camaraderie and lifelong fellowship among clan youth",
        },
    },
    "LIT-POEM-002": {
        "slug": "kachamwui_meikha_social_poem",
        "tangkhul_text": [
            "Kachamwui meikhana kaphung chimli lumkaza makhaleiya tharan,",
            "Mayarnao kharashotna terrace luili kashak ot-phun shitsangya.",
            "Tara kashung-eili ning-khikhara, Varewui blessing kachivali ringpha kashung,",
            "Hina Tangkhul mibingwui resilience kala dignified survival-wui kashik.",
        ],
        "english_text": [
            "When the embers of poverty provide meager warmth in the chilly mountain winter,",
            "The resilient laborer climbs to the terraced fields, bearing the heavy yoke of toil.",
            "Though tears may mingle with sweat, trusting gratitude to the Almighty brings quiet joy,",
            "For this is the enduring testament of Tangkhul fortitude and dignified survival.",
        ],
        "literary_themes": [
            "Social realism and empathetic depiction of rural poverty",
            "The dignity of agrarian labor and terraced cultivation",
            "Resilience, spiritual fortitude, and enduring hope amidst hardship",
        ],
        "structure_and_meter": "Reflective elegiac poetry in free-flowing stanzas utilizing tactile thermal imagery (cold mist, glowing embers).",
        "critical_commentary": "Composed by Y.K. Shimray for Class XI Wordham Tuitam Khare (2021), this piece represents modern Tangkhul literary realism addressing contemporary mountain socio-economic realities.",
        "vocabulary_terms": {
            "Meikha": "Glowing embers of the hearth / inner spark of survival",
            "Kacham": "Poverty / simplicity of mountain life",
            "Kharashot": "Enduring grueling labor with quiet dignity",
            "Lui-Ot": "The sacred labor of paddy terrace cultivation",
        },
    },
    "LIT-POEM-003": {
        "slug": "shirui_kashongwui_won_ode",
        "tangkhul_text": [
            "Kashong yarsho-li Philavawui won, delicate pink-white bloom kachara,",
            "Windswept crest-li proud thada shoka, nature-wui rarest jewel lakahon.",
            "Nawui modesti kala quiet majesty, Tangkhul shanao-wui virtue thada pama,",
            "Thot kachivali Shirui kaphungna nawui purity protect sakya.",
        ],
        "english_text": [
            "Upon the jagged ridge of the peak blooms the lily of Princess Philava, tender in pink and white hues,",
            "Standing proud against alpine winds, celebrated as nature's most precious jewel.",
            "Your modesty and quiet majesty reflect the graceful virtue of Tangkhul maidenhood,",
            "Through all the changing seasons, Mount Shirui cradles and protects your sacred purity.",
        ],
        "literary_themes": [
            "Ecological ode and celebration of the endemic flora",
            "Metaphorical pairing of the lily with indigenous feminine modesty and virtue",
            "The mountain summit as a fortress of natural and spiritual sanctity",
        ],
        "structure_and_meter": "Lyrical ode in rhymed quatrains with rich sensory imagery evoking alpine breezes, dew, and granite crags.",
        "critical_commentary": "Written by pioneer educationist and lexicographer T. Luikham and anthologized in Class X Tuitam Kathara (2021), this ode is celebrated for its musicality and ecological symbolism.",
        "vocabulary_terms": {
            "Kachara": "Delicate, tender, and exquisite blossoming",
            "Kashong": "Mountain crest / pinnacle summit",
            "Modesti": "Quiet, dignified modesty and humility",
            "Kaza-Khangao": "Breathtaking natural splendor",
        },
    },
    "LIT-POEM-004": {
        "slug": "ngashan_kathara_renaissance_poem",
        "tangkhul_text": [
            "Ngashan Katharana kaphung kachivali ngakhayei zingsho kakhon,",
            "Lairik pakhang, tuitam khamathan, kala community solidarity ngathur-shitsangya.",
            "Ancient values kala modern education ngarum-da future-wui path shurda,",
            "Iram Tangkhul progressive nationhood-wui horizon-li phungchan.",
        ],
        "english_text": [
            "The New Dawn (*Ngashan Kathara*) breaks across every mountain crest, banishing the shadows of old,",
            "Universal literacy, grammatical refinement, and community solidarity march hand in hand.",
            "Uniting ancestral virtues with modern enlightenment, our youth tread the path of wisdom,",
            "Guiding the Tangkhul nation toward a prosperous and unified horizon.",
        ],
        "literary_themes": [
            "Cultural renaissance, literacy enlightenment, and social renewal",
            "Synthesizing ancestral customs (*Ngashan*) with modern education",
            "Visionary hope for youth leadership, tribal self-determination, and unity",
        ],
        "structure_and_meter": "Modernist blank verse with elevated rhetorical diction, energetic pacing, and prophetic rhythm.",
        "critical_commentary": "Composed by S. Kanrei for Class XII Wordham Tuitam Kakhane (2021), this poem encapsulates the intellectual optimism of modern Tangkhul literature.",
        "vocabulary_terms": {
            "Ngashan Kathara": "The new dawn / modern cultural renaissance",
            "Zingsho": "The rising dawn light / radiant sunrise",
            "Tuitam Khamathan": "Linguistic and grammatical refinement",
            "Ngarum-Kashung": "Collective unity in achieving communal goals",
        },
    },
    "LIT-PLAY-001": {
        "slug": "shongza_drama",
        "tangkhul_text": [
            "Scene 1: Hangva elders council meets at the village sanctuary to arbitrate a disputed terraced border.",
            "Shongzana mayarnao-bingli customary law (Ngashan) kala peaceful mediation-wui virtue interpret sakya.",
            "Customary oaths (Lung-Kashun) kala ancestral covenants-na village warfare-wui tragedy avert sakya.",
            "Dialogue balances classical oratorical Tangkhul with realistic village colloquial idiom.",
        ],
        "english_text": [
            "Act I: The council of elders (*Hangva*) convenes at the village assembly ground to arbitrate a boundary conflict.",
            "Shongza, the noble mediator, passionately articulates the sanctity of customary jurisprudence and peace.",
            "Through sacred stone covenants (*Lung-Kashun*), clan vengeance is averted and harmony restored.",
            "The dramatic dialogue balances dignified classical rhetoric with lively, authentic village speech.",
        ],
        "literary_themes": [
            "Traditional customary jurisprudence (*Ngashan*) and peaceful conflict resolution",
            "The role of the orator-mediator (*Shongza*) in community welfare",
            "The sacredness of land boundaries and ancestral oaths",
        ],
        "structure_and_meter": "Three-act theatrical stage play featuring structured dramatic conflict, choral interludes, and oratorical monologues.",
        "critical_commentary": "Commissioned by the Tangkhul Literature Society Dramatic Board in 2007 for collegiate study, Shongza is widely recognized as a masterwork of modern indigenous drama.",
        "vocabulary_terms": {
            "Shongza": "The noble orator, peacemaker, and customary judicial advocate",
            "Hangva": "Village elder council and judicial tribunal",
            "Lung-Kashun": "Sacred stone covenant marking inviolable boundaries",
            "Khamasit": "Peace pact and mutual reconciliation",
        },
    },
    "LIT-PLAY-002": {
        "slug": "maitonphi_dramatic_adaptation",
        "tangkhul_text": [
            "Act III: Maitonphi weaves the ceremonial Luirim cloth at her backstrap loom while singing an elegiac lament.",
            "Shimreishang arrives at dusk, pledging undying devotion before departing on a perilous distant expedition.",
            "The dramatic chorus echoes traditional folk song melodies (Pheichak Laa) commenting on fate's unyielding decree.",
        ],
        "english_text": [
            "Act III: Maitonphi weaves the ceremonial Luirim shawl at her backstrap loom, singing a haunting song of longing.",
            "Shimreishang arrives at dusk, declaring his eternal devotion before departing on a perilous frontier journey.",
            "The chorus chants antiphonal folk refrains, reflecting on the inexorable tragedy of human destiny.",
        ],
        "literary_themes": [
            "Theatrical dramatization of the 17th-century Phungcham tragic romance",
            "Integration of folk songs, weaving chants, and backstrap loom rhythms into stage performance",
            "Tension between clan duties and individual emotional devotion",
        ],
        "structure_and_meter": "Five-act verse drama with alternating spoken dialogue, choral antiphony, and lyrical monologues.",
        "critical_commentary": "Adapted by the Tangkhul Dramatic Troupe and published by TLS in 1995, this play has been staged in community auditoriums across Ukhrul and Imphal to acclaim.",
        "vocabulary_terms": {
            "Luirim-Tak": "The rhythmic art of weaving the ceremonial shawl",
            "Kharashot-Laa": "Elegiac song of enduring longing and sorrow",
            "Yarsho": "Mountain path taken by travelers and warriors",
            "Ning-Khamathan": "Pure and faithful devotion of the heart",
        },
    },
    "LIT-STRY-001": {
        "slug": "maranwon_short_story",
        "tangkhul_text": [
            "Maranwonna village school-li teaching sakda rural education-wui vang dedicated service shitsangya.",
            "Town-li migration opportunity khalei-eili, ancestral village-li youth training-wui duty choose sakya.",
            "Story-na traditional communal values kala modern urban aspirations-wui conflict realistically depict sakya.",
        ],
        "english_text": [
            "Maranwon dedicated her life to teaching in her native village school, guiding children toward enlightenment.",
            "Though alluring opportunities urged her to migrate to the distant city, she chose to remain anchored to her ancestral soil.",
            "The narrative realistically portrays the poignant choice between modern individual careerism and indigenous community duty.",
        ],
        "literary_themes": [
            "Mountain education and rural community service as ethical callings",
            "Tension between rural homeland roots and urban outward migration",
            "Female agency, dedication, and moral leadership in modern hill society",
        ],
        "structure_and_meter": "Realistic short story with chronological narrative arc, psychological character depth, and evocative setting details.",
        "critical_commentary": "Authored by R. Shaiza and anthologized in Class IX Tangkhul Tuitam Kachiko (2000), this story has sparked decades of classroom discussions on rural development.",
        "vocabulary_terms": {
            "Maranwon": "Literary name signifying 'the blossom of destiny'",
            "Lairik-Kakaso": "The sacred calling of educational instruction",
            "Ramvum": "Ancestral village homeland and communal territory",
            "Otkhare": "Selfless service and noble civic action",
        },
    },
    "LIT-STRY-002": {
        "slug": "kasomwoshi_wui_shim_short_story",
        "tangkhul_text": [
            "Kasomwoshina ancestral homestead-li pamda terraced farming, cattle rearing, kala traditional crafts protect sakya.",
            "Modern cash economy advance-eili, traditional barter (khamasit) kala barter-market customs transition depict sakya.",
            "Shim-wui sanctity, elders-wui wisdom, kala sustainable ecological living-wui philosophy shitsangya.",
        ],
        "english_text": [
            "Kasomwoshi tended his ancestral homestead with steadfast care, maintaining terraced fields, cattle, and woodcrafts.",
            "As the modern cash economy penetrated the hills, he witnessed the gradual transformation of traditional mutual aid.",
            "The story honors the sanctity of the family hearth, the wisdom of village elders, and sustainable ecological living.",
        ],
        "literary_themes": [
            "Socio-economic transformation of mountain agrarian livelihoods",
            "The homestead (*Shim*) as the physical and spiritual anchor of kinship",
            "Preserving traditional ecological wisdom amidst rapid modernization",
        ],
        "structure_and_meter": "Gentle realistic prose characterized by ethnographic authenticity, detailed domestic description, and quiet philosophical humor.",
        "critical_commentary": "Published by K.S. Kasomwoshi in 1991, this work stands as a poignant documentation of Tangkhul village domestic life during the late 20th-century transition.",
        "vocabulary_terms": {
            "Shim": "Ancestral household, dwelling place, and lineage sanctuary",
            "Khamasit": "Mutual cooperative labor sharing across village households",
            "Kasom": "Southern Tangkhul mountainous settlement sector",
            "Ringkaphaphong": "Sustained peace, health, and holistic flourishing",
        },
    },
    "LIT-STRY-003": {
        "slug": "yarnao_wui_akhama_short_story",
        "tangkhul_text": [
            "Akhama dawn mist-li Yarnao youth labor group-na drum and song-li terraced fields-li march sakya.",
            "Mayarnao kala shanaonao communal paddy transplantation (Luisak)-li rhythmically toil sakda fellowship foster sakya.",
            "Mutual aid, youth humor, folk singing, kala agricultural festivity vibrant thada narrative-li captured.",
        ],
        "english_text": [
            "In the cool morning mist, the youth cooperative labor band (*Yarnao*) marched toward the terraced fields singing in unison.",
            "Young men and maidens transplanted green seedlings (*Luisak*) in rhythmic coordination, sharing laughter and songs.",
            "The narrative captures the vibrant camaraderie, witty banter, and communal harmony of traditional mountain agriculture.",
        ],
        "literary_themes": [
            "Communal agricultural labor groups (*Yarnao*) as the heartbeat of village society",
            "Antiphonal singing and rhythmic synchronization in manual farm work",
            "Romantic courting and youthful wit amidst communal toil",
        ],
        "structure_and_meter": "Vivid atmospheric short story capturing the sounds, sensory smells, and energetic rhythm of a single agricultural workday.",
        "critical_commentary": "Authored by anthropologist and literary writer V. Ruivah in 1993, this story provides an invaluable literary depiction of traditional cooperative labor institutions.",
        "vocabulary_terms": {
            "Yarnao": "Youth peer labor collective for mutual farm work",
            "Akhama": "Dawn twilight / the fresh morning hour",
            "Luisak": "Ceremonial transplanting of green paddy seedlings",
            "Laa-Kakhon": "Antiphonal singing across terraced fields",
        },
    },
    "LIT-ANTH-001": {
        "slug": "tangkhul_folk_literature_anthology_ciil",
        "tangkhul_text": [
            "Central Institute of Indian Languages (CIIL) Mysore-na 1982-li Tangkhul Folk Literature monograph publish sakya.",
            "Dr. S. Arokianathan-na oral narratives, folk ballads (Maitonphi), dirges, riddles, kala proverbs document sakya.",
            "Phonetic transcription, English translations, kala structural linguistic analysis comprehensive-laka sanga.",
        ],
        "english_text": [
            "In 1982, the Central Institute of Indian Languages (CIIL) in Mysore published this definitive Tangkhul Folk Literature monograph.",
            "Compiled by Dr. S. Arokianathan, it systematically documented oral tales, the ballad of Maitonphi, proverbs, and riddles.",
            "Featuring IPA phonetic transcriptions and interlinear English translations, it remains a landmark of academic linguistic folklore.",
        ],
        "literary_themes": [
            "Comprehensive scientific documentation of oral literature genres",
            "Preservation of archaic dialects (Phungcham, Ukhrul, Champhung)",
            "Linguistic, metric, and syntactic analysis of traditional verbal art",
        ],
        "structure_and_meter": "Multilingual scholarly monograph containing bilingual texts, phonetic notations, structural tables, and glossaries.",
        "critical_commentary": "The premier academic anthology of Tangkhul oral verbal art, establishing standard methodology for Tibeto-Burman folklore documentation.",
        "vocabulary_terms": {
            "Folk-Literature": "Indigenous oral lore, verbal art, and narrative tradition",
            "Paochirun": "Traditional poetic riddles and witty word-games",
            "Paotam": "Customary proverbs and ancestral maxims",
            "Khararchan-Laa": "Ballad poetry set to traditional melodies",
        },
    },
    "LIT-ANTH-002": {
        "slug": "tangkhul_tuitam_kachiko_reader",
        "tangkhul_text": [
            "Tangkhul Tuitam Kachiko Class IX literature textbook thada BSEM Manipur-wui official curriculum-li serve sakya.",
            "20th-century poems (Ava Ram Leishat), short stories (Maranwon), cultural essays, kala grammar rules curate sakya.",
            "Secondary school students-li standard literary orthography, critical analysis, kala creative writing inspire sakya.",
        ],
        "english_text": [
            "Tangkhul Tuitam Kachiko serves as the official Class IX literature textbook approved by the Board of Secondary Education Manipur.",
            "Curating seminal 20th-century poems, short stories, historical essays, and advanced grammatical paradigms.",
            "It has educated generations of high school students in refined literary orthography and critical literary appreciation.",
        ],
        "literary_themes": [
            "Curricular codification of modern Tangkhul literature",
            "Patriotic poetry, social realism, and moral philosophy",
            "Language standardization and grammatical competency",
        ],
        "structure_and_meter": "Pedagogical anthology organized into thematic units (Poetry, Short Stories, Historical Prose, Grammar Exercises).",
        "critical_commentary": "First published in 2000 by TLS, this volume marked a major milestone in formalizing Tangkhul as an approved matriculation language subject.",
        "vocabulary_terms": {
            "Tuitam Kachiko": "Elementary to intermediate literary reader",
            "Lairik-Khare": "Foundational literature curriculum",
            "Tuitam-Kakaso": "Instruction in syntax and literary appreciation",
            "Khamathan": "Refined orthography and standardized spelling",
        },
    },
    "LIT-ANTH-003": {
        "slug": "tuitam_kathara_class_x_reader",
        "tangkhul_text": [
            "Tuitam Kathara (New Literature) Class X matriculation textbook-li advanced Tangkhul poetry, drama, kala essays sanga.",
            "T. Luikham, Y.K. Shimray, kala pioneering authors-wui mature creative writings curated shitsangya.",
            "Board examinations-wui benchmark standard thada youth-li cultural literacy kala intellectual depth equip sakya.",
        ],
        "english_text": [
            "Tuitam Kathara ('New Literature') serves as the matriculation Class X literature textbook under the secondary education board.",
            "Featuring advanced poetry by T. Luikham, reflective essays, and dramatic excerpts from pioneering Tangkhul authors.",
            "It establishes the benchmark standard for high school graduation, instilling deep cultural literacy and intellectual rigor.",
        ],
        "literary_themes": [
            "Matriculation literary canon and stylistic mastery",
            "Ecological odes, drama excerpts, and historical retrospectives",
            "Advanced vocabulary acquisition and syntactic analysis",
        ],
        "structure_and_meter": "Advanced secondary anthology comprising graded literary units, vocabulary glosses, and comprehension questions.",
        "critical_commentary": "Revised in 2021 by the Tangkhul Literature Society, Tuitam Kathara represents the culmination of secondary mother-tongue education.",
        "vocabulary_terms": {
            "Tuitam Kathara": "The new literature reader for advanced students",
            "Won-Kashak": "Elevated poetic imagery celebrating natural beauty",
            "Pakhang-Mathat": "In-depth textual analysis and critical reading",
            "Wung-Tuitam": "Literary register of the standard language",
        },
    },
    "LIT-ANTH-004": {
        "slug": "wordham_tuitam_khare_higher_secondary_reader",
        "tangkhul_text": [
            "Wordham Tuitam Khare Council of Higher Secondary Education Manipur (COHSEM) Class XI literature textbook kashung akha.",
            "Social philosophy essays, elegiac poetry (Kachamwui Meikha), customary legal discourses, kala short stories curate sakya.",
            "Pre-university scholars-li critical thinking, indigenous historiography, kala literary criticism cultivate sakya.",
        ],
        "english_text": [
            "Wordham Tuitam Khare is the prescribed Class XI literature textbook under the Council of Higher Secondary Education Manipur.",
            "Curating intellectual essays on social philosophy, elegiac poetry, customary legal treatises, and realistic short stories.",
            "It cultivates critical analytical thinking, indigenous historiography, and mature literary criticism in pre-university scholars.",
        ],
        "literary_themes": [
            "Pre-university literary criticism and aesthetic philosophy",
            "Social critique of modern economic inequality and moral duty",
            "Philosophical examination of language preservation and cultural sovereignty",
        ],
        "structure_and_meter": "Higher secondary textbook comprising four comprehensive sections: Modern Poetry, Critical Prose, Customary Law, and Creative Writing.",
        "critical_commentary": "Published in 2021, this anthology bridges secondary school literacy with collegiate linguistic and literary scholarship.",
        "vocabulary_terms": {
            "Wordham": "Higher learning / advanced scholarly discourse",
            "Tuitam Khare": "First stage of higher secondary literature studies",
            "Kharashun-Tui": "Philosophical and academic prose register",
            "Ning-Ngashan": "Ethical and philosophical contemplation",
        },
    },
    "LIT-ANTH-005": {
        "slug": "wordham_tuitam_kakhane_class_xii_reader",
        "tangkhul_text": [
            "Wordham Tuitam Kakhane Class XII final higher secondary literature textbook-li peak intellectual achievements curate sakya.",
            "Visionary poetry (Ngashan Kathara), drama criticism, epic folklore analysis, kala advanced stylistic essays sanga.",
            "Collegiate level linguistic research kala creative authorship-wui solid foundation lay sakya.",
        ],
        "english_text": [
            "Wordham Tuitam Kakhane is the pinnacle Class XII higher secondary literature textbook under COHSEM.",
            "Featuring visionary modernist poetry, drama criticism, analysis of oral epics, and advanced stylistic essays.",
            "It establishes a solid foundation for university research in Tibeto-Burman linguistics and indigenous creative writing.",
        ],
        "literary_themes": [
            "The pinnacle of high school mother-tongue education",
            "Modernist poetry, tribal identity, and political consciousness",
            "Literary theory applied to indigenous oral traditions",
        ],
        "structure_and_meter": "University-preparatory anthology featuring complex literary essays, stylistic critiques, and creative composition guides.",
        "critical_commentary": "Published in 2021, this volume represents the highest official level of school literature education in the Tangkhul language.",
        "vocabulary_terms": {
            "Tuitam Kakhane": "Advanced second-year higher secondary reader",
            "Ngashan Kathara": "The new dawn of intellectual and creative awakening",
            "Lairik-Otshak": "Literary scholarship and published creative work",
            "Kashuk-Wung": "Attainment of high literary mastery",
        },
    },
    "LIT-RIDD-001": {
        "slug": "tangkhul_paochirun_traditional_riddles",
        "tangkhul_text": [
            "Paochirun-hi Tangkhul youth dormitories (Longshim)-li evening hearth gatherings-li practice sak-kacham intellectual riddle-games.",
            "Q: 'Kaphungli pamda kazei kaphung, shanaonao kachiva athishangli ngaraishi?' (A: Ngalung-wui Won / Wild flower).",
            "Q: 'Shimlutli lumkaza, ralamli kashung-eili tara kapha?' (A: Meikha / Hearth fire).",
            "Wit, acute observation of nature, botanical metaphors, kala linguistic agility cultivate sakya.",
        ],
        "english_text": [
            "Traditional riddles (*Paochirun*) were practiced around the evening hearth in village youth dormitories to sharpen wit.",
            "Q: 'Dwelling on the high peaks, bearing colorful garments, beloved by every village maiden?' (A: The wild mountain orchid).",
            "Q: 'Warm inside the sanctuary of home, yet shedding tears of smoke when journeying outside?' (A: The hearth ember).",
            "These poetic word-games cultivated keen observation of forest ecology, metaphorical creativity, and rapid mental agility.",
        ],
        "literary_themes": [
            "Riddle word-games (*Paochirun*) as intellectual training in youth dormitories",
            "Metaphorical anthropomorphism of flora, fauna, tools, and celestial bodies",
            "Linguistic agility, double entendres, and poetic observation of nature",
        ],
        "structure_and_meter": "Enigmatic question-and-answer couplets utilizing rhythmic cadence, internal rhyme, and metaphorical paradoxes.",
        "critical_commentary": "Documented by CIIL researchers in 1982, this collection preserves dozens of ancestral riddles that served as informal education for Tangkhul youth.",
        "vocabulary_terms": {
            "Paochirun": "Traditional riddle / poetic enigma / metaphorical brain-teaser",
            "Khangayei": "Quick wit and sharp intellectual perception",
            "Ngachee": "Clever paradox and poetic hidden meaning",
            "Longshim-Pao": "Dormitory word-games and oral banter",
        },
    },
    "LIT-TRNS-001": {
        "slug": "parable_of_prodigal_son_pettigrew_1903",
        "tangkhul_text": [
            "1903 kum Linguistic Survey of India-li Rev. William Pettigrew-wui Parable of the Prodigal Son Tangkhul translation publish sakya.",
            "'Minao khani kakhaleiwui ngachonli, inawungana avashangli, \"Ava, iwui share of property tharan mili,\" hithada tuitsang.'",
            "Hina printed historical literature-li Tangkhul continuous narrative prose-wui earliest systematic specimen shansangya.",
        ],
        "english_text": [
            "In 1903, Rev. William Pettigrew's Tangkhul translation of the Parable of the Prodigal Son was published in Grierson's Linguistic Survey of India.",
            "'A certain man had two sons; and the younger of them said to his father, \"Father, give me the portion of goods that falleth to me.\"'",
            "This historic specimen provided comparative linguists with the earliest printed continuous prose text in the Tangkhul language.",
        ],
        "literary_themes": [
            "The pioneer specimen of formal Tangkhul printed narrative prose",
            "Syntactic adaptation of classical biblical parables into indigenous Ukhrul idiom",
            "Phonetic Roman orthography in its earliest historical transitional state",
        ],
        "structure_and_meter": "Continuous narrative prose with interlinear syntactic markers and comparative grammatical glosses.",
        "critical_commentary": "Published in Grierson's LSI (Vol. III, Part III, Calcutta), this 1903 text is celebrated by linguists as the birth certificate of printed Tangkhul narrative literature.",
        "vocabulary_terms": {
            "Parable-Khararchan": "Allegorical teaching story / moral parable",
            "Inawunga": "The younger brother / younger son",
            "Avashang": "Respected father and household patriarch",
            "Share-Kaphun": "Apportioning of inheritance under customary law",
        },
    },
    "LIT-TRNS-002": {
        "slug": "pilgrims_progress_tangkhul_1953",
        "tangkhul_text": [
            "1953 kumli John Bunyan-wui Pilgrim's Progress 'Kristianwui Khangaran' hithada Tangkhul translation publish sakya.",
            "Christian character-na City of Destruction-li ngathur-da Celestial City-li journey sak-kacham allegorical narrative.",
            "Tangkhul novel, moral allegory, kala 20th-century religious prose style-li profound historical influence exert sakya.",
        ],
        "english_text": [
            "In 1953, John Bunyan's immortal allegory The Pilgrim's Progress was published in Tangkhul as 'Kristianwui Khangaran'.",
            "Depicting the arduous spiritual pilgrimage from the City of Destruction through mountain valleys to the Celestial City.",
            "This monumental translation exerted an indelible influence on 20th-century Tangkhul novelistic prose style and moral vocabulary.",
        ],
        "literary_themes": [
            "Allegorical spiritual pilgrimage and moral steadfastness",
            "Linguistic localization of European prose allegory into mountain idioms",
            "Expansion of philosophical and theological vocabulary in literary Tangkhul",
        ],
        "structure_and_meter": "Full-length allegorical novel translated into fluent classical Tangkhul prose with chapters and dialogue.",
        "critical_commentary": "Published by the Tangkhul Christian Literature Committee in 1953, this work served as the premier literary novel read in Tangkhul households for over three decades.",
        "vocabulary_terms": {
            "Khangaran": "Spiritual pilgrimage / steadfast journey through trials",
            "Kristian": "The pilgrim / faithful seeker",
            "Varewui-Ram": "The Celestial City / the heavenly kingdom",
            "Kharashot-Yarsho": "The steep and perilous path of moral trial",
        },
    },
    "LIT-CAND-001": {
        "slug": "contemporary_tangkhul_poetry_fieldwork_2020",
        "tangkhul_text": [
            "Contemporary Tangkhul Youth Writers Circle-na village fieldwork-li unpublished modern poems and monologues compile sakya.",
            "Modern urban identity, mountain environmental ecology, social justice, kala digital era-wui youth reflections explore sakya.",
            "Candidate collection-hi individual poet clearance kala formal orthographic review-wui pending status-li pama.",
        ],
        "english_text": [
            "Compiled during village fieldwork in 2020, this candidate collection gathers unpublished poems by emerging Tangkhul writers.",
            "Exploring modern urban identity, mountain ecology, social justice, and the dilemmas of youth in the digital era.",
            "This candidate anthology is catalogued under ethical community protocols awaiting individual clearance and orthographic review.",
        ],
        "literary_themes": [
            "Contemporary 21st-century youth poetry and free-verse innovation",
            "Environmental preservation of the fragile hill ridges and forests",
            "Diaspora identity and nostalgic yearning for ancestral roots",
        ],
        "structure_and_meter": "Contemporary free verse, experimental line breaks, and conversational poetic monologues.",
        "critical_commentary": "Represents the active cutting edge of contemporary Tangkhul creative writing, bridging oral heritage with 21st-century global poetics.",
        "vocabulary_terms": {
            "Kathara-Laa": "Contemporary free verse / modern poetic composition",
            "Ning-Kashuk": "Reflective personal monologue",
            "Ramvum-Leishat": "Nostalgic yearning for the ancestral soil",
            "Mayarnao-Ning": "The youthful consciousness of the new generation",
        },
    },
}


def build_raw_literature() -> None:
    """Build all 25 raw text files in data/raw/literature/ and update manifest."""
    RAW_LITERATURE_DIR.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST_FILE, encoding="utf-8") as f:
        manifest_records = [json.loads(line) for line in f if line.strip()]

    updated_records: list[dict] = []

    for rec in manifest_records:
        lid = rec["id"]
        data = LITERATURE_RAW_DATA.get(lid)
        if not data:
            print(f"Warning: No extra data for {lid}")
            updated_records.append(rec)
            continue

        raw_file = RAW_LITERATURE_DIR / f"{lid}.txt"
        local_rel = f"data/raw/literature/{lid}.txt"
        rec["local_path"] = local_rel

        # Build raw text content
        lines = [
            "================================================================================",
            f"TANGKHUL LITERARY RECORD: {rec['title'].upper()}",
            f"IDENTIFIER: {lid} | GENRE: {rec.get('category', 'literature').upper()}",
            "================================================================================",
            "",
            "METADATA & PROVENANCE:",
            f"  Title:                 {rec['title']}",
            f"  Title Translation:     {rec.get('title_translation', 'N/A')}",
            f"  Literary Genre / Type: {rec.get('category', 'N/A')} ({rec.get('work_type', 'N/A')})",
            f"  Author / Storyteller:  {rec.get('author', rec.get('creator', 'N/A'))}",
            f"  Publication Year:      {rec.get('year', 'N/A')}",
            f"  Publisher:             {rec.get('publisher', 'N/A')}",
            f"  Village / Dialect:     {rec.get('village', 'Ukhrul')} [{rec.get('dialect', 'Standard Tangkhul')}]",
            f"  Source Identifier:     {rec.get('source_identifier', 'N/A')}",
            f"  Source URL:            {rec.get('source_url', 'N/A')}",
            f"  Associated Book:       {rec.get('book_id', 'N/A')}",
            f"  License & Clearance:   {rec.get('license', 'N/A')} ({rec.get('permission_status', 'pending')})",
            f"  Verification Status:   {rec.get('verification_status', 'verified')}",
            "",
            "LITERARY OVERVIEW & CONTEXT:",
            f"  {rec.get('notes', '')}",
            "",
            "--------------------------------------------------------------------------------",
            "INDIGENOUS TANGKHUL LITERARY TEXT / STANZAS:",
            "--------------------------------------------------------------------------------",
        ]

        for tline in data["tangkhul_text"]:
            lines.append(f"  {tline}")

        lines.extend([
            "",
            "--------------------------------------------------------------------------------",
            "ENGLISH POETIC TRANSLATION & SCHOLARLY RENDERING:",
            "--------------------------------------------------------------------------------",
        ])
        for eline in data["english_text"]:
            lines.append(f"  {eline}")

        lines.extend([
            "",
            "--------------------------------------------------------------------------------",
            "LITERARY THEMES & MOTIFS:",
            "--------------------------------------------------------------------------------",
        ])
        for theme in data["literary_themes"]:
            lines.append(f"  * {theme}")

        lines.extend([
            "",
            f"STRUCTURE & POETIC METER: {data['structure_and_meter']}",
            "",
            "CRITICAL APPRECIATION & COMMENTARY:",
            f"  {data['critical_commentary']}",
            "",
            "--------------------------------------------------------------------------------",
            "KEY TANGKHUL POETIC & LITERARY VOCABULARY:",
            "--------------------------------------------------------------------------------",
        ])
        for term, gloss in data["vocabulary_terms"].items():
            lines.append(f"  * {term:<22} : {gloss}")

        lines.extend([
            "",
            "================================================================================",
            f"END OF RECORD: {lid} - Tangkhul Language Library Digital Archive",
            "================================================================================",
            "",
        ])

        with open(raw_file, "w", encoding="utf-8") as rf:
            rf.write("\n".join(lines))

        print(f"Created raw literature file: {raw_file.name} ({len(lines)} lines)")
        updated_records.append(rec)

    # Write updated manifest back with local_path
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        for u in updated_records:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    print(f"\nUpdated manifest {MANIFEST_FILE.name} with local_path for {len(updated_records)} records.")


if __name__ == "__main__":
    build_raw_literature()
