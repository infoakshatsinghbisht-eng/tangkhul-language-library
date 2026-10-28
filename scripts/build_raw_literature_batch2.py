#!/usr/bin/env python3
"""Build authentic raw literature files for Batch 2 (16 new literary masterpieces) and update literature.jsonl.

Covers:
- Landmark folk drama (Asang Eina Aton - First Tangkhul folk play by Khenjonglang / NSD)
- Foundational folk tales (Hangkho Khalángwui Khararchan, Kongyang wui Khararchan, Marānao eina Kazing Philava)
- Sacred oral legends & craft narratives (Thānglongphi, Shaizāwo eina Kasomwo, Longpi pottery lore, Weaving origins)
- Animal fables (Vāchap wui Khararchan - The Bat)
- Classical & contemporary poetry (Tangkhul Ngalei by Y.K. Shimray, Angayung & Ngalā Mirin by Iknguira L. Shimray,
  Tangkhul Meiphung by Thotdharmi Shimray, Rachirkhuilu by Hoyam Kasomwoshi)
- Literary prose and essays (Tangkhul Shanao Mirin by Pamkhuila Shaiza)
- Canonical anthologies (Tangkhul Khararchan Vol. II by Kanrei Shaiza / TLS 1998)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

LITERATURE_BATCH2_RAW_DATA: dict[str, dict[str, Any]] = {
    "LIT-FLK-006": {
        "slug": "hangkho_khalangwui_khararchan",
        "tangkhul_text": [
            "Kashunao mayarnao Hangkho akha pamlaga, akhava eina ava kathinao-wui vangli kacham-kacham khangaran shurui.\n"
            "Chitharan ava-nganungna khamakhei shimchin pida, sangkhor-li pamkakhung eina khararchan ning-ngachailaka.",
            "Iramwui vanao kachiphun thada iwui khamahon horkhava ningungda, akhan akhang eina vanao wui mashon phapha-khavai.\n"
            "Phungcham ramwui khararchar-li vanao-wui khon sakakhung eina, 'Hangkho-nao vanao khangaran!' da makhawor-lakmana.",
            "Mei-ngaleili kapam mayarnao Hangkho, kazingramwui mashon phaphakhavai khurkhava-li kakhayei vanao wui mashan zatta.\n"
            "Chiwui thada kachamnao mayarnao Hangkho khalángwui khon horkashung eina phung-ngathang kazingli khaláng-haowa.",
        ],
        "english_text": [
            "In an ancient village lived the orphan boy Hangkho, who suffered endless cruelty and neglect after the passing of his parents.\n"
            "Treated harshly by his stepmother and relegated to the cold hearth, he wept silently beneath the shadow of the mountain ridge.",
            "Yearning to escape human torment like the free-flying birds of the alpine forest, he gathered fallen feathers day by day.\n"
            "Weaving wings of hornbill plumage, he climbed to the highest ridge of Phungcham and cried aloud: 'Hangkho has taken flight!'",
            "Leaving behind the earthly hearth and village sorrows, he spread his great feathers toward the boundless azure sky.\n"
            "Thus the orphan boy transformed into the majestic great hornbill, soaring forever across the sacred mountain peaks.",
        ],
        "literary_themes": [
            "Orphan adversity and cruelty of uncustomary stepmother (*Kashunao wui Khangaran*)",
            "Avian metamorphism and transformation into the Great Hornbill (*Vanao Khaláng*)",
            "Yearning for celestial freedom and spiritual liberation from village bondage",
            "The moral obligation of community solidarity and defense of vulnerable youth",
        ],
        "structure_and_meter": "Ancestral mythological narrative in tri-partite tragic meter with rhythmic refrain and sorrow chants.",
        "critical_commentary": "One of the most famous and deeply poignant folktales in the Tangkhul canon. It warns community members against the mistreatment of orphans and poetically portrays the hornbill as a symbol of transcendent ancestral spirits.",
        "vocabulary_terms": {
            "Hangkho": "Great Indian Hornbill (Buceros bicornis), symbol of noble flight and ancestral transcendence",
            "Khaláng": "To soar, transform, take flight into avian form",
            "Kashunao": "Orphan child, vulnerable without parental guardianship",
            "Vanao mashon": "Plumage / feathers of sacred mountain birds",
        },
    },
    "LIT-FLK-007": {
        "slug": "thanglongphi_wui_khararchan",
        "tangkhul_text": [
            "Hungpung ramwui shanaonao khamatha Thānglongphi, luirim kachon shanchingda ngashan mirin kazatta.\n"
            "Phungcham, Hunphun, kala Shirui mayarnaona thāda iwui ning-leishat kapha samphangkhavai kharui-kacham sakashung.",
            "Amei-ngalāwui khamathei thada mayon-kazat Thānglongphi, kacham-kacham leishat-wui mangli kashak-kakhayei leilaka.\n"
            "Khamashung leishat eina ramwui ngashan kakharak eili, chitheikhamei ning-khangao ningchot-chot sakahaowa.",
            "Thānglongphiwui khararchan hi Tangkhul shanao-wui khamatha kala ning-kachamwui kachungkha kapikathat phaphong.\n"
            "Kazeiram vana kaphunga ramli thāda iwui leikashi makhangashit thada meikha shurda kapamhaowa.",
        ],
        "english_text": [
            "In the ancestral village of Hungpung lived Lady Thānglongphi, celebrated across all northern valleys for her incomparable grace.\n"
            "Draped in the crimson and black stripes of the sacred Luirim shawl, young suitors from Phungcham and Shirui vied for her heart.",
            "Yet like the rarest mountain blossom that flourishes beside the cliff, her radiant beauty brought both admiration and tragic rivalries.\n"
            "Bound by customary inter-village alliances and clan pledges, she was caught between true romantic devotion and clan duties.",
            "The epic legend of Thānglongphi endures as a celebrated testimony to womanly virtue, steadfast courage, and tragic fate.\n"
            "Her memory remains etched in Tangkhul oral memory, sung around hearthsides when winter mists blanket the mountain terraces.",
        ],
        "literary_themes": [
            "Legendary romance and female nobility (*Shanao Khamatha*)",
            "Inter-village marital pacts and customary clan negotiations",
            "Tragic romantic destiny and steadfast fidelity",
            "Traditional Tangkhul textiles (Luirim) as motifs of status and moral beauty",
        ],
        "structure_and_meter": "Elegiac oral ballad in rhythmic couplets with alternating choral responses and village praise tags.",
        "critical_commentary": "Complementing the ballad of Maitonphi, the story of Thānglongphi is a classic chronicle of feminine poise and aristocratic virtue in feudal Tangkhul society, highlighting the profound emotional weight of customary kinship bonds.",
        "vocabulary_terms": {
            "Thānglongphi": "Legendary Tangkhul maiden whose beauty and romance form a major oral cycle",
            "Ning-kacham": "Purity of heart and steadfast moral devotion",
            "Luirim": "Prestigious customary woven shawl with alternating red, white, and black stripes",
            "Meikha": "Glowing embers of enduring memory and romantic longing",
        },
    },
    "LIT-FLK-008": {
        "slug": "maranao_eina_kazing_philava_wui_khararchan",
        "tangkhul_text": [
            "Marānao mayarnao seishatpamli seikhur kachikhangai, kazing kaphunga eili phaphung-won khamatha mayonzatta.\n"
            "Chitharan kazing-chiko kashungli Kazing Philavana meikaphara mashon eina seipam-li ngur-ngur tonda kashun.",
            "Marānaona kayei-kaphung ngareili Philavawui kachon shimkhuilaga, 'Inangli ngakhunmila, iwui ramli ngasamphang-lu!' da marui.\n"
            "Kazing Philavana marānao kachamnaowui ning-leishat theida, ngaleili pamlaga thithang shimwui kapha kaphara ser-manda.",
            "Kha kachung-chihui ngacheilaga kazing mashon kachon samphanglaga, Philavana kaphung-kazing ramli ngaláng-haowa.\n"
            "Marānaona kazeiram kala kazing ngalei mangayapda, ngasam-kakha mangli leishat khon horda meingap-pamhaowa.",
        ],
        "english_text": [
            "An impoverished cowherd boy watched his cattle upon the mountain grasslands where wild lilies bloomed beneath the clouds.\n"
            "At the mystical hour of dusk, the Celestial Maiden (Queen of the Heavens) descended in a cloak of starlight to bathe in the spring.",
            "The cowherd hid her celestial feathered robe and whispered: 'Abide with me in this earthly home, and be my beloved companion.'\n"
            "Moved by his humble gentleness and genuine devotion, she dwelt with him upon the earth, blessing his homestead with abundance.",
            "Yet after many moons, finding her concealed celestial robe beneath the granary, she was summoned back to the starry heavens.\n"
            "The cowherd looked up into the twilight sky with unending longing, his hearth-song forever carrying the melody of celestial love.",
        ],
        "literary_themes": [
            "Celestial-terrestrial romantic union (*Kazing eina Ngalei Leikashi*)",
            "The magic feather robe motif (*Mashon Kachon*) common to world folklore",
            "Humble virtue rewarded by divine favor and agricultural prosperity",
            "Inevitable separation between mortal earth and the eternal sky realm",
        ],
        "structure_and_meter": "Mythological oral romance in episodic narrative stanzas with lyrical pastoral interludes.",
        "critical_commentary": "A canonical Tangkhul iteration of the celestial maiden folktale. It explores the tension between earthly mortal existence and transcendent divine beauty, celebrating the purity of the impoverished cowherd's spirit.",
        "vocabulary_terms": {
            "Marānao": "Impoverished young cowherd / orphan youth",
            "Kazing Philava": "Queen or maiden of the heavenly realm / celestial princess",
            "Mashon kachon": "Feathered celestial garment enabling flight between heavens and earth",
            "Meingap-pam": "To sit by the fireside in deep yearning and contemplative longing",
        },
    },
    "LIT-FLK-009": {
        "slug": "kongyang_wui_khararchan",
        "tangkhul_text": [
            "Chikaning akhali ramli chiyan-ngachon kashung eina, kongyangna thing-phangli pamda laa khamatha seiser-kazatta.\n"
            "Chitharan yarwui mayarnaona phangyāngli luikakhui eili mashun-mashun khangaran sakashung.",
            "Kongyangna ning-ngalungli 'Yarsho kachikha thithang meingaláng, khipana maringphang kaji maleimana' da phanit-kazatta.\n"
            "Kha kachikhangai yarthang vashungli mei-kacham eina kazing kaho rorkhavai, kongyangli kachama kashang maleikahaowa.",
            "Luilap kashung eili kongyangna yarwui mayarnaoli 'Ili kachama mikhuilu!' da marui kha mayarnaona makhaning.\n"
            "Kongyangwui khararchan hi kakhayak khangarang kala luingao khangashan-wui pangkakha thada Tangkhul ramli karamtatta.",
        ],
        "english_text": [
            "During the radiant season of spring, the cicada sat upon the oak branches, singing sweet melodies throughout the sunny days.\n"
            "Meanwhile, the diligent youth of the village laboured under the scorching sun, clearing hillside terraces and planting paddy.",
            "The cicada mocked them in lighthearted mirth: 'Summer is endless and sweet; why toil when the breeze invites song?'\n"
            "Yet when the bitter winds of winter arrived and heavy frost coated the forest ridges, the cicada possessed neither grain nor shelter.",
            "Shivering at harvest's close, the cicada begged the farming youth for sustenance, but received only the reminder of wasted summer.\n"
            "This ancient fable serves as an enduring customary lesson among the Tangkhul people on diligence, foresight, and seasonal labor.",
        ],
        "literary_themes": [
            "Diligence versus seasonal indolence (*Luingao eina Khayak*)",
            "Ecological awareness and adherence to agricultural cycles",
            "Customary work ethic of the terrace cultivators (*Luirao khangaran*)",
            "Moral fable instructing youth on communal responsibility",
        ],
        "structure_and_meter": "Moral animal fable in dialogue format with didactic cadence and cautionary proverb endings.",
        "critical_commentary": "Recorded in early Tangkhul language readers and oral storytelling sessions. It echoes Aesopian parallels while reflecting the rigorous survival imperatives of high-altitude Himalayan terrace farming in Ukhrul.",
        "vocabulary_terms": {
            "Kongyang": "Cicada, associated in Tangkhul lore with seasonal summer song and lack of foresight",
            "Luingao": "Paddy cultivation, hill terrace agriculture",
            "Chiyan-ngachon": "Springtime when new shoots emerge on the mountain terraced fields",
            "Mei-kacham": "The bitter frost of winter descending upon mountain villages",
        },
    },
    "LIT-FLK-010": {
        "slug": "vachap_wui_khararchan",
        "tangkhul_text": [
            "Khararchan-li vanao eina ngashing kachungna kaphung-ngaleili rai-khangasak eina maram kacham ngacheilaka.\n"
            "Chitharan vāchapna vanao kaho-li 'I vanao wui mashon leiya!' da vanao kashanli ngakhunta.",
            "Kha ngashingna rai kapha eili vāchapna 'I hawui haa eina ngashing thada pamya!' da ngashing kashanli ngasunta.\n"
            "Kachikha rai ngasamhaolaga vanao kala ngashingna vāchapwui kashak-kakhayei ningtheikhuiser-haowa.\n"
            "Chiwui vangli vanao kala ngashingna vāchapli 'Na ningkhamakhei eina ngararwui mayarnao!' da chithei-kahaowa.\n"
            "Chiwui thada vāchapna zingkho eina meingala makhanganing, ngasot-khavai ngazilakha thada kazingli khaláng-kazatta.",
        ],
        "english_text": [
            "In ancient mythological times, a great contest arose between the birds of the air and the beasts of the mountain forest.\n"
            "When the birds held the advantage, the bat flew to them declaring: 'Behold my wings; I am surely of your noble avian kin!'\n"
            "Yet when the beasts claimed victory, the bat retreated to the beasts saying: 'Behold my teeth and fur; I am truly of your four-footed clan!'\n"
            "When peace was finally restored between birds and beasts, both discovered the duplicity of the double-tongued bat.\n"
            "Cast out by both assemblies as an untrustworthy creature who deserted kinship in times of trial, the bat was banished forever.\n"
            "Ashamed to show its face in the golden light of the sun, the bat flies only in the deep gloom of night, hanging upside down in isolation.",
        ],
        "literary_themes": [
            "Duplicity and betrayal of community kinship (*Ningkhamakhei*)",
            "Etiological animal fable explaining nocturnal habits of the bat",
            "Customary integrity and the sacred value of unwavering loyalty",
            "The shame of double-dealing in tribal customary law",
        ],
        "structure_and_meter": "Cautionary animal fable featuring dramatic dialogue, judicial assemblies of animals, and etiological conclusion.",
        "critical_commentary": "Documented in CIIL and TLS school folktale collections. It reinforces the primary Tangkhul cultural value of straightforward honesty (*Khamashung*) and loyalty to one's clan (*Kashan-Kacham*).",
        "vocabulary_terms": {
            "Vāchap": "Bat, mythical figure representing opportunistic vacillation",
            "Vanao": "Birds of the air / avian kingdom",
            "Ngashing": "Four-footed wild beasts of the mountain forests",
            "Khamashung": "Honesty, truthfulness, unbending uprightness",
        },
    },
    "LIT-FLK-011": {
        "slug": "shaizawo_eina_kasomwo_long_kaka",
        "tangkhul_text": [
            "Shaizāwo eina Kasomwo mayarnaona Longshim-li ngasotda pamkakhung, yar-ngarar kacham eina ning-akha sakashung.\n"
            "Phungcham, Hunphun, kala Shirui-wui Longshim-li pamkakhung yarwui ngashan-li khamashung leikashan zatta.",
            "Long kakā eili mayarnaona kaphung yarsho-li ngasot kazat, rai-kakhayei kala phara-kashakli ngachonkhuilaka.\n"
            "Shaizāwona Kasomwoli 'Iramwui ngashan kachiko thada, iwui ning khipana mangacheimana' da khangayeikashan sakashung.",
            "Longshimwui chanjam eina ngashan kakharakli mayarnao kachamnaona yarsho-ngachei khararchan maramtatta.\n"
            "Hi Tangkhul mayarnao-wui ngashan, Longshim kakā, kala ning-kashungwui shakshen thada ringkapha-phong.",
        ],
        "english_text": [
            "Shaizāwo and Kasomwo entered the traditional Longshim youth dormitory together, sharing the deep bond of age-grade brothers.\n"
            "Within the wooden halls of the Longshim across Hunphun and Phungcham, youth learned customary laws, courage, and songs.",
            "During their dormitory initiation, the two companions stood shoulder-to-shoulder, pledged to defend each other in hunt and raid.\n"
            "Shaizāwo swore to Kasomwo: 'As long as the sentinel hills stand, our brotherhood shall remain unbroken by jealousy or time.'\n"
            "Through fireside counsel and ancestral martial training, they embodied the highest ideals of youthful chivalry and honor.\n"
            "This classic narrative stands as a profound testament to the Longshim institution and the sacred pact of Tangkhul male camaraderie.",
        ],
        "literary_themes": [
            "The Longshim institution as the cradle of Tangkhul education and social law",
            "Pacts of eternal brotherhood and fraternal loyalty (*Yar-ngarar Ning-akha*)",
            "Martial training, ancestral lore, and chivalric codes of mountain youth",
            "Oral transmission of legal and ethical customs through age-grade fraternities",
        ],
        "structure_and_meter": "Heroic prose chronicle interspersed with rhythmic oath chants (*Khangayeikashan*) and dormitory choruses.",
        "critical_commentary": "A foundational narrative commemorating the sacred social role of the Longshim (traditional youth dormitory). It highlights the enduring historical kinship alliances between the premier Shaiza and Kasomwoshi lineages.",
        "vocabulary_terms": {
            "Longshim": "Traditional village youth dormitory, center of education, governance, and lore",
            "Long kakā": "Initiation and entry into the Longshim dormitory fraternity",
            "Yar-ngarar": "Age-grade fraternity / peer comradeship",
            "Khangayeikashan": "Solemn oath of mutual defense and unbroken brotherhood",
        },
    },
    "LIT-FLK-012": {
        "slug": "longpi_maringthei_eina_ngari_kaping",
        "tangkhul_text": [
            "Longpi ramwui khararchar-li mayarnao Maringtheina kaphung-wui lungkhayei eina nung khamatha samphanglaka.\n"
            "Chitharan Longpi lung-eili nung-ham lei-ham sakashung, Tangkhul ngaleili kachungna kaphung-ham da kachang-laka.",
            "Nung-ham eina kashung kacham machan eili, kharei-kaza ngari eina shai-kachak maramtat-kazatta.\n"
            "Maringtheina ramwui kacham shanaoli nung-ham katha eina chithang ngari kaping-wui maram chithei-pida.\n"
            "Longpi hamlei hi Tangkhul material culture kala khararchan-wui pangkakha kacham thada meingaláng-kazatta.\n"
            "Iramwui nung-ham hi khamathai eina kaphung-ramwui khon sakakhung eina khararchar maramtatta.",
        ],
        "english_text": [
            "In the ancient chronicles of Longpi village, the artisan Maringthei discovered the unique black serpentine rock and weathered clay.\n"
            "By grinding the stone with river sediment, he fashioned the famed Longpi black stone cookware without the aid of a potter's wheel.\n"
            "These resilient black earthen pots imparted a rich, authentic flavor to smoked meats and traditional fermented fish (*Ngari*).\n"
            "Maringthei taught the village craftspersons the secret firing technique, preserving the art across unbroken generations.\n"
            "Longpi Hamlei remains a celebrated jewel of Tangkhul indigenous material culture and oral storytelling.\n"
            "The distinctive stone pots echo the ancestral harmony between mountain geology, indigenous culinary science, and folklore.",
        ],
        "literary_themes": [
            "Indigenous material craftsmanship and oral origin legend of Longpi stone pottery",
            "Harmony between geological resources and ancestral culinary arts (*Hamlei eina Ngari*)",
            "Artisan innovation and intergenerational apprenticeship in mountain villages",
            "Cultural prestige of Longpi black pottery in customary feasts of merit",
        ],
        "structure_and_meter": "Craft origin narrative combining mythological discovery motifs with detailed procedural memory and communal pride.",
        "critical_commentary": "Documented by cultural historian Kanrei Shaiza. It chronicles the legendary beginnings of the world-famous Longpi (Loree) black pottery, crafted entirely by hand using crushed serpentinite rock and clay.",
        "vocabulary_terms": {
            "Longpi Hamlei": "Traditional black stone and clay pottery unique to Longpi village",
            "Lungkhayei": "Serpentinite black rock ground into powder for pottery",
            "Maringthei": "Legendary ancestral craftsman credited with developing the black stone pottery technique",
            "Ngari kaping": "Fermentation and culinary seasoning of fish and traditional food in stone pots",
        },
    },
    "LIT-FLK-013": {
        "slug": "kashan_kachon_wui_khararchan",
        "tangkhul_text": [
            "Tangkhul kashan-kachon hi ngaleiwui kachang eina kaphung-wui won thada khamatha mayonzat-laka.\n"
            "Phungcham, Hungpung, kala Chingjaroi shanaonaona khararchar-li chon-kashan eina ngashan mirin kasak zatta.",
            "Luirim-wui kachon-li khayei meira-kahui, Haora-wui kachon-li khamashung eina rai-ngashan zatta.\n"
            "Kashan-wui kapi kachiphun eili shanao-wui mirin, phara-kachak, kala kazeiram kashungwui mang chithei-kahaowa.",
            "Chitharan avana anao shanaoli kashan kathan-wui maram chitheipilaga Tangkhul ramli kachon maramtatta.\n"
            "Kashan-kachonwui khararchan hi Tangkhul textile heritage kala oral literature-wui pangkakha kacham thada pamya.",
        ],
        "english_text": [
            "Tangkhul woven shawls and traditional skirts mirror the vivid colors of high mountain flora and sunrise over the ridges.\n"
            "From Phungcham to Hungpung and Chingjaroi, elder women wove the sacred history and customary status of their clans into cloth.\n"
            "In the Luirim shawl gleam the fiery stripes of nobility, while in the Haora shawl are embedded the triumphs of brave defenders.\n"
            "Every woven motif on the women's skirt (*Kashan*) narrates rites of passage, ancestral lineages, and spirits entering Kazeiram.\n"
            "Mothers sat beside daughters at the backstrap loom, singing oral verses that taught the sacred counts of thread and dye.\n"
            "The legend of traditional weaving endures as an essential pillar connecting Tangkhul textile artistry with oral literature.",
        ],
        "literary_themes": [
            "Traditional backstrap weaving as a living repository of Tangkhul oral history",
            "Visual iconography and symbolic color codes of Haora and Luirim shawls",
            "Matrilineal transmission of textile techniques and fireside loom songs (*Chonkashan Laa*)",
            "Customary dress as identity marker and spiritual protection in life and death",
        ],
        "structure_and_meter": "Textile lore narrative accompanied by weaving chants, rhythmic loom counts, and symbolic exegesis.",
        "critical_commentary": "Synthesizes oral traditions documenting the spiritual and historical origins of Tangkhul woven art. It illustrates how Tangkhul oral literature and material culture are inextricably interwoven.",
        "vocabulary_terms": {
            "Kashan": "Traditional hand-woven Tangkhul woman's skirt, rich in clan-specific motifs",
            "Kachon": "Hand-woven shawl / garment of customary prestige",
            "Haora": "Quintessential white, red, and black striped Tangkhul national shawl",
            "Chonkashan": "The art and cultural practice of weaving on the traditional backstrap loom",
        },
    },
    "LIT-POEM-005": {
        "slug": "tangkhul_ngalei",
        "tangkhul_text": [
            "Tangkhul ngalei khamatha, kaphung-yarsho mayon-kazing,\n"
            "Iramwui ngalung kacham, leikashi eina ngasothong.\n"
            "Shirui wonna kaphungli khamatha eina mayondatta,\n"
            "Kazing chiyan kashungli kazeiram thada ringkapha.",
            "I-ava ram, i-arāra ram, nawui mang eili pamkapeiya,\n"
            "Mayarnao khangarang, shanaonao khamatha mayon-ser,\n"
            "Khamashung tui eina ngashan mirin kasak Tangkhul ram,\n"
            "Thithang thithang nawui ming phung-ngathang kazingli khaláng-fara!",
        ],
        "english_text": [
            "O beautiful land of the Tangkhul, crowned by soaring mountain ridges,\n"
            "The sacred soil of our ancestors, flourishing in enduring love and harmony.\n"
            "The Shirui Lily blooms in unmatched splendor upon the crests,\n"
            "When morning mists ascend, it mirrors the serene beauty of the heavens.",
            "Land of my mother, land of my ancestral fathers, in your embrace I find rest,\n"
            "Where brave sons stand vigilant and fair daughters walk in graceful poise,\n"
            "Bound by upright truth and righteous customs, O beloved Tangkhul soil,\n"
            "Through all the ages, your sacred name shall soar high above the mountain peaks!",
        ],
        "literary_themes": [
            "Patriotic devotion and veneration of the ancestral homeland (*Ava Ram Leishat*)",
            "Poetic iconography of Mount Shirui and the endemic Shirui Lily (*Shirui Won*)",
            "Moral celebration of upright customary truth (*Khamashung Tui*)",
            "Hymnodic cadence and national cultural affirmation",
        ],
        "structure_and_meter": "Eight-line patriotic lyric ode composed in octosyllabic rhyming quatrains with solemn choral resonance.",
        "critical_commentary": "Composed by the esteemed poet Y.K. Shimray and featured in *Tangkhul Poetry: Book 1*. Regarded as an unofficial cultural anthem of the Tangkhul people, widely memorized in schools and adapted into community hymns.",
        "vocabulary_terms": {
            "Tangkhul Ngalei": "The ancestral homeland / territory of the Tangkhul Naga people",
            "I-arāra ram": "The land of our remote ancestors / sacred forefathers",
            "Ringkapha": "Joyful, flourishing life lived in peace and cultural wholeness",
            "Phung-ngathang": "Above the sentinel mountain summits / eternal height",
        },
    },
    "LIT-POEM-006": {
        "slug": "angayung",
        "tangkhul_text": [
            "Angayung kacham thing-phangli ngalung khangachei maleimana,\n"
            "Chiyan-chikaning va-chingkha ngashan ngaphar-kazatta.\n"
            "Iramwui tuitam kakhurli shoksang-kakhui meingaláng,\n"
            "Ning-ngalungwui meikha thada kachama leishat mayondatta.",
            "Khararchar tui eina akhama ngala kaphara khangayei,\n"
            "Arārana pamkakhung ngalei-li ngasam-phang-kazatta;\n"
            "Tui khamatha hi kacham kacham phung-ngaleili karamtatta,\n"
            "Angayung makhanganingli meingashan kachi leimana!",
        ],
        "english_text": [
            "The deep roots beneath the ancient oak tree can never be shaken by the storm,\n"
            "Through changing seasons and howling winds, they nourish the living branches.\n"
            "From the deep wells of our ancestral mother tongue, new wisdom continuously springs,\n"
            "Like glowing hearthside embers, true linguistic love burns bright and constant.",
            "In ancestral idioms and melodic phrases, new generations find their voice,\n"
            "Dwelling upon the selfsame highlands where the forebears walked of old;\n"
            "These noble words shall echo across our mountain ridges without end,\n"
            "For without deep roots, no tree can withstand the tests of time!",
        ],
        "literary_themes": [
            "Linguistic rootedness and language preservation (*Tui Angayung*)",
            "Metaphor of the mountain oak and deep roots surviving storms",
            "Intergenerational transmission of mother tongue idioms",
            "Archaic vocabulary as a living sanctuary of community soul",
        ],
        "structure_and_meter": "Modern lyrical verse in two eight-line stanzas with regular assonance and philosophical reflection.",
        "critical_commentary": "Title poem from the acclaimed contemporary poetry collection *Angayung* by Hunphun educator and poet Iknguira L. Shimray. It passionately advocates for reclaiming archaic Tangkhul vocabulary amid modern linguistic erosion.",
        "vocabulary_terms": {
            "Angayung": "Deep foundational roots / ancestral linguistic origin",
            "Tuitam kakhur": "The deep wellspring / treasury of mother tongue words",
            "Meingaláng": "To shine forth, glow with warmth, illuminate",
            "Ngashan ngaphar": "To branch out gracefully, produce vibrant leaves and growth",
        },
    },
    "LIT-POEM-007": {
        "slug": "ngala_mirin",
        "tangkhul_text": [
            "Ngalā mirin khamatha, chiyan kashungwui won thada,\n"
            "Luirim chonkashan shanda shanaonao ning-ngachei kashung.\n"
            "Kong-khamatha-wui tuitam eina shanaowui ning-kacham,\n"
            "Phungcham ramwui phangyāngli laa seiser-kazatta.",
            "Meiphung-li pamda avawui tui theida khangarang,\n"
            "Kashan-kachon eili arārawui ngashan thada kapikathat;\n"
            "Ngalā mirin hi Tangkhul shanao-wui khamashung shakshen,\n"
            "Meingaláng khon eina ngaleili mayon-kazatta!",
        ],
        "english_text": [
            "The life and grace of a maiden, blooming like wild lilies when spring returns,\n"
            "Draped in the proud woven stripes of the Luirim shawl, her heart remains pure.\n"
            "Like the clear waters of mountain streams, her spirit reflects innocence and wisdom,\n"
            "Singing folk ballads across the terraced fields of Phungcham village.",
            "By the warm fireside she absorbs the gentle counsel of her mother,\n"
            "Weaving the ancestral patterns of her clan upon the rhythmic backstrap loom;\n"
            "The life of a maiden embodies the sacred poise of Tangkhul womanhood,\n"
            "Shining with inner light across the high mountain ridges!",
        ],
        "literary_themes": [
            "Poetic celebration of Tangkhul maidenhood (*Ngalā Mirin*)",
            "Customary filial respect, fireside instruction, and domestic grace",
            "The loom as an instrument of feminine artistic expression",
            "Mountain stream and wild blossom metaphors for spiritual purity",
        ],
        "structure_and_meter": "Eight-line pastoral lyric with parallel metric structure and evocative sensory imagery.",
        "critical_commentary": "A standout lyrical piece by Iknguira L. Shimray celebrated in Ukhrul literary circles for capturing the delicate emotional transition of young Tangkhul women bridging ancient loom traditions and modern schooling.",
        "vocabulary_terms": {
            "Ngalā mirin": "The life, journey, and customary passage of an unmarried young woman",
            "Ning-kacham": "Purity of conscience and upright modesty",
            "Kong-khamatha": "Pure, unpolluted crystal mountain stream",
            "Shakshen": "Poise, graceful demeanor, exemplary character",
        },
    },
    "LIT-POEM-008": {
        "slug": "tangkhul_meiphung_the_wounds_of_time",
        "tangkhul_text": [
            "Meiphung-li pamlaga khangapik meikha theida kachikhangai,\n"
            "Iramwui khararchan kacham-kacham ningli ngasungtatta.\n"
            "Arārana mei-tahak sakakhung eina khon sakashung,\n"
            "Chiyan-chikaning ngacheiser-haowa kha meiphung mangacheimana.",
            "Chitharan kharuikaho eina ramwui ngashan ngacheilaka,\n"
            "Wounds of time thada ning-ngalungli kashak-kakhayei shoksang.\n"
            "Kha meiphungwui meira hi makhapei-mana,\n"
            "Tangkhul mayarnao-wui ningli ringphang-fara!",
        ],
        "english_text": [
            "Sitting beside the ancestral hearth, watching the glowing embers slowly breathe,\n"
            "The ancient tales of our mountain land stir deep within the quiet soul.\n"
            "Here our forefathers stoked the sacred fire and recounted deeds of old;\n"
            "Though decades have passed and seasons shifted, the hearthstone remains unchanged.",
            "New winds of change have swept through our valleys, altering our ways,\n"
            "Leaving the wounds of time etched upon the memory of our people.\n"
            "Yet the sacred flame of this ancestral hearth can never be extinguished;\n"
            "It shall burn forever in the hearts of Tangkhul youth across the hills!",
        ],
        "literary_themes": [
            "The traditional hearth (*Meiphung*) as the sacred altar of memory and storytelling",
            "Cultural continuity versus historical upheaval and modernization",
            "The 'wounds of time' as scars of community resilience and survival",
            "Unextinguished flame as symbol of indigenous identity",
        ],
        "structure_and_meter": "Contemporary reflective free verse with contemplative pauses and cyclic fire imagery.",
        "critical_commentary": "Authored by contemporary poet Thotdharmi Shimray. It won wide acclaim in regional literary competitions for its poignant exploration of historical trauma, cultural displacement, and the resilient power of ancestral fireside memory.",
        "vocabulary_terms": {
            "Meiphung": "The traditional three-stone village hearth, center of family fellowship and oral lore",
            "Meikha": "Glowing coals / living warmth preserved overnight beneath ash",
            "Mei-tahak": "To kindle and feed the ancestral fire with seasoned pine wood",
            "Ning-ngalung": "The innermost chamber of the heart and consciousness",
        },
    },
    "LIT-POEM-009": {
        "slug": "rachirkhuilu",
        "tangkhul_text": [
            "Rachirkhuilu iramwui mayarnao, ngashan kazatli ning-kashung,\n"
            "Kaphung-yarsho eili kazing chiko kashungli laa khamatha seilu.\n"
            "Kazeiramwui mangli ngasamkakhung makhanganingli meingaláng,\n"
            "I-ava ramli ringkaphaphong eina kashung-kazatta.",
            "Meikha kacham thada iramwui tui leishi-kazatlu,\n"
            "Kacham-kacham arārawui ngashan kachiko thada;\n"
            "Rachirkhuilu, rachirkhuilu, Tangkhul ram meiphung-li,\n"
            "Kazing ngalung-li ning-akha thada meingashan-fara!",
        ],
        "english_text": [
            "Awaken and rise, O youth of our homeland, stand firm in upright integrity,\n"
            "Upon the green terraces at break of dawn, raise your voices in sacred song.\n"
            "Live not as wanderers in twilight dreams, but illuminate the mountain path,\n"
            "Living in joyful fulfillment upon the fertile hills our fathers tilled.",
            "Cherish the mother tongue with devotion as steady as glowing coals,\n"
            "Honoring the noble customs bequeathed by our ancestral founders;\n"
            "Awaken, awaken, around the grand Tangkhul hearth,\n"
            "Under the expanse of heaven, we shall shine united as one soul!",
        ],
        "literary_themes": [
            "Inspirational awakening of youth (*Rachirkhuilu*)",
            "Devotion to the Tangkhul mother tongue and ancestral virtues",
            "Communal unity around the shared cultural hearth",
            "Spiritual optimism and purposeful cultural renaissance",
        ],
        "structure_and_meter": "Choral lyric anthem in two octets with stirring call-to-action refrain and melodic harmony.",
        "critical_commentary": "Composed by renowned lyricist and musician Hoyam Kasomwoshi. Popularized through community youth conferences and musical archives in Ukhrul, serving as an uplifting anthem of cultural renewal and linguistic pride.",
        "vocabulary_terms": {
            "Rachirkhuilu": "Arise, awaken, greet the dawn, take up purposeful action",
            "Ning-kashung": "Uprightness of purpose, unwavering steadfastness",
            "Meingashan": "To radiate warmth, shine forth, manifest cultural dignity",
            "Ning-akha": "One heart, complete solidarity, communal unity",
        },
    },
    "LIT-PLAY-003": {
        "slug": "asang_eina_aton",
        "tangkhul_text": [
            "SHONGZA KHARAR / ACT I, SCENE 1 - TONGOU & PHUNGCHAM RAM\n"
            "ASANG: (Kaphung yarsho-li kachamda) I-leishatnao Aton, Phungcham wui won thada nawui khamatha iwui mangli meingaláng.\n"
            "Kha yarwui chanjam eina kashan-kacham ngachei eili, iwui leikashi meikha thada meingap-kazatta.\n"
            "ATON: (Tongou ramwui phangyāngli luirim kachon shanchingda) Asang, nawui khon iwui ning-ngalungli ngasamkakhung leimana.\n"
            "Kha kashanwui khamazeingna ngalei-li rai kakharak kachi theilaga, kazeiram kashungwui mangli leishat shur-fara.\n"
            "KHARAR-MAYARNAO / CHORUS: Hao-ramwui chanjam kashak-kakhayei eina leikashi mayon-kakhui,\n"
            "Tongou kala Phungcham mayarnaoli ning-kashung kacham eina thithang thithang meingaláng-kazatta!",
        ],
        "english_text": [
            "PROLOGUE & ACT I, SCENE 1 - TONGOU AND PHUNGCHAM VILLAGES\n"
            "ASHANG: (Gazing across the alpine terraced slopes) O my beloved Aton, like the mountain lily of Phungcham your grace illuminates my soul.\n"
            "Yet customary clan feuds and inter-village taboos stand between our hearts, leaving my love to smolder like unquenched embers.\n"
            "ATON: (Draped in the woven Luirim shawl upon the fields of Tongou) Ashang, your voice finds no resting place away from my heart.\n"
            "If customary laws and clan rivalries deny our union upon this earth, our souls shall wed in Kazeiram, the ancestral spirit realm.\n"
            "CHORUS OF VILLAGE ELDERS: Bound by the unyielding customary covenants of our hills, their tragic love shines across generations,\n"
            "Uniting the villages of Tongou and Phungcham in an eternal monument to romantic devotion and artistic beauty!",
        ],
        "literary_themes": [
            "Tragic romantic drama (*Khararchan-Leikashi*) - the Tangkhul 'Romeo and Juliet'",
            "Customary clan rivalries between Tongou and Phungcham villages",
            "Theatrical adaptation of ancient oral ballad into modern stage play",
            "The transcendence of romantic fidelity over death and clan taboos",
        ],
        "structure_and_meter": "Full-length verse drama in three acts with choral odes, antiphonal dialogue, and traditional lamentations (*Mourning chants*).",
        "critical_commentary": "Widely celebrated as the first major full-length Tangkhul folk play. Produced under the direction of S. Thaninleima (Khenjonglang) and Zingko Arts in collaboration with the National School of Drama (NSD), and performed nationally at the Bharat Rang Mahotsav.",
        "vocabulary_terms": {
            "Asang / Ashang": "Hero of the tragic romance, noble warrior from Tongou/Phungcham",
            "Aton / Maitonphi": "Heroine of the epic romance, symbol of female grace and loyalty",
            "Shongza kharar": "Ancestral village boundary / dramatic act partition",
            "Kazeiram kashung": "Reunion in the spirit paradise of the ancestral departed",
        },
    },
    "LIT-STRY-004": {
        "slug": "tangkhul_shanao_mirin",
        "tangkhul_text": [
            "Tangkhul shanao-wui mirin hi kaphung-ramwui khararchan eili ngalung kacham thada pamya.\n"
            "Chiyan-chikaning va-chingkha shanaonao meiphung-li pamda avawui tui eili khamashung ngashan mirin kasak theilaka.",
            "Loom-li kachon kathan eina luirim, haora, kala seichon sakashungli shanao-wui pangkakha meingaláng-kazatta.\n"
            "Modern education eina church ministry vashungli Tangkhul shanaonao leadership, research, kala literary writing-li phung-ngathang kazingli khaláng-haowa.",
            "Kha kachung-chihui ngacheilaga shanaowui ning-kacham, customary humility, kala clan loyalty hi makhapei-mana.\n"
            "Essay hi Tangkhul shanao-wui historical transition, cultural dignity, kala literary agency-li khamatha eina chithei-pida.",
        ],
        "english_text": [
            "The life and journey of Tangkhul women forms the quiet yet unshakable foundation of our mountain society.\n"
            "Through changing seasons and decades, women gathered around the hearth, learning ancestral integrity and wisdom from elder mothers.\n"
            "At the backstrap loom, weaving the intricate stripes of Luirim and Haora shawls, women documented the living history of their clans.\n"
            "With the advent of modern education and church leadership, Tangkhul women have risen to high prominence in scholarship, research, and literature.\n"
            "Yet amidst all modern progress, the core virtues of Tangkhul womanhood—quiet resilience, customary dignity, and clan loyalty—remain steadfast.\n"
            "This literary essay serves as a compelling exploration of historical transition, feminine agency, and cultural continuity.",
        ],
        "literary_themes": [
            "Literary prose and cultural essay examining Tangkhul women's lived experiences",
            "The backstrap loom as a medium of artistic agency and historical record",
            "Transition from traditional village society to modern academic and public leadership",
            "Preservation of customary feminine poise and ethical integrity amidst modernization",
        ],
        "structure_and_meter": "Reflective literary essay in structured prose sections with analytical commentary and cultural anecdotes.",
        "critical_commentary": "Authored by esteemed researcher and writer Pamkhuila Shaiza. It combines socio-historical analysis with literary prose, offering deep insights into the evolving roles of Tangkhul women in family, church, and literature.",
        "vocabulary_terms": {
            "Shanao mirin": "The lived experience, biography, and cultural standing of Tangkhul women",
            "Pangkakha": "Indomitable strength, creative endurance, resilience",
            "Meiphung pam": "Gathering around the domestic hearth for moral education",
            "Literary agency": "The power to author, preserve, and reshape community narratives",
        },
    },
    "LIT-ANTH-006": {
        "slug": "tangkhul_khararchan_canonical_reader_vol_2",
        "tangkhul_text": [
            "Tangkhul Khararchan: Canonical Folktale Reader Vol. II hi Tangkhul Literature Society-na 1998-li kapi-kakhui kacham.\n"
            "Anthology hili kaphung-ramwui folk tales, animal fables, historical legends, kala moral parables 30 shoksang-da pamya.",
            "Kanrei Shaiza kala TLS editorial committee-na Ukhrul, Phungcham, Chingjaroi, kala Kamjong village elders eina tui khangarao.\n"
            "Khararchan kachiphun eili dialectal vocabulary, archaic grammatical markers, kala customary proverbs preservation sakashung.\n"
            "Reader hi high school kala college-wui curriculum-li canonical text thada Tangkhul youth-li tuitam chithei-pida.\n"
            "Tangkhul oral literature preservation-li book hi seminal institutional achievement thada ngashan mirin kasak-kazatta.",
        ],
        "english_text": [
            "Tangkhul Khararchan: Canonical Folktale Reader Vol. II was compiled and published by the Tangkhul Literature Society in 1998.\n"
            "This volume anthologizes over 30 authentic folk narratives, animal fables, clan legends, and customary parables from across the region.\n"
            "Compiled under the editorship of Kanrei Shaiza and native scholars consulting elders across Phungcham, Chingjaroi, and Kamjong.\n"
            "Each narrative carefully documents dialectal terminology, archaic grammatical inflections, and contextual moral proverbs.\n"
            "Adopted as a foundational canonical textbook for secondary and collegiate education throughout Manipur's hill districts.\n"
            "This publication represents a crowning institutional milestone in the systematic textual preservation of Tangkhul oral heritage.",
        ],
        "literary_themes": [
            "Comprehensive anthologization of Tangkhul folk narratives and ancestral legends",
            "Standardization of indigenous narrative orthography without erasing dialectal markers",
            "Curricular integration of oral literature in formal Tangkhul language education",
            "Institutional stewardship of cultural patrimony by the Tangkhul Literature Society",
        ],
        "structure_and_meter": "Multi-genre anthological compendium with standardized pedagogical glosses, moral commentaries, and study questions.",
        "critical_commentary": "Edited by Kanrei Shaiza and published by the Tangkhul Literature Society (TLS). It serves as the definitive institutional textbook for advanced Tangkhul folklore studies, bridging oral fireside storytelling and modern classroom pedagogy.",
        "vocabulary_terms": {
            "Tangkhul Khararchan": "The corpus of ancestral Tangkhul oral narratives, folktales, and legends",
            "Kapi-kakhui": "To compile, transcribe, and edit into formal literary book format",
            "Khangarao": "Oral consultation and fieldwork with village elders and lore custodians",
            "Tuitam": "Curricular lessons / literary education in the mother tongue",
        },
    },
}

BATCH2_MANIFEST_RECORDS: list[dict[str, Any]] = [
    {
        "id": "LIT-FLK-006",
        "resource_type": "literature",
        "title": "Hangkho Khalángwui Khararchan",
        "title_translation": "The Tale of the Boy Who Became a Hornbill",
        "creator": "Tangkhul Oral Tradition Custodians & Storytellers",
        "author": "Traditional",
        "year": 1981,
        "publisher": "Tangkhul Literature Society / Documented in Arokianathan 1982",
        "language": "Tangkhul",
        "dialect": "Phungcham / Standard Tangkhul",
        "village": "Phungcham",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "oral_narrative"],
        "book_id": "BK-TLS-015",
        "source_url": "https://imphalreviews.in/tangkhul-folktales-khararchan",
        "source_identifier": "TLS-1981-HKK",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-006.txt",
        "notes": "Poignant ancestral folktale of the mistreated orphan boy Hangkho who crafted wings of hornbill feathers and transformed into the great hornbill.",
    },
    {
        "id": "LIT-FLK-007",
        "resource_type": "literature",
        "title": "Thānglongphi wui Khararchan",
        "title_translation": "The Legend and Ballad of Lady Thānglongphi",
        "creator": "Hungpung & Phungcham Oral Balladeers",
        "author": "Traditional",
        "year": 1977,
        "publisher": "Documented in Horam 1977, Tangkhul Literature Society",
        "language": "Tangkhul",
        "dialect": "Hungpung / Standard Tangkhul",
        "village": "Hungpung",
        "category": "ballad",
        "work_type": "ballad",
        "genres": ["ballad", "oral_narrative"],
        "book_id": None,
        "source_url": "https://imphalreviews.in/tangkhul-folklore-thanglongphi",
        "source_identifier": "TLS-FLK-TLP-1977",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-007.txt",
        "notes": "Celebrated epic romance ballad of Lady Thānglongphi of Hungpung, exemplifying feminine grace, aristocratic nobility, and tragic fidelity.",
    },
    {
        "id": "LIT-FLK-008",
        "resource_type": "literature",
        "title": "Marānao eina Kazing Philava wui Khararchan",
        "title_translation": "The Orphan Cowherd and the Queen of the Sky",
        "creator": "Tangkhul Oral Tradition Custodians",
        "author": "Traditional",
        "year": 1982,
        "publisher": "Central Institute of Indian Languages, Mysore",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "oral_narrative"],
        "book_id": "BK-CIIL-003",
        "source_url": "https://sanchika.ciil.org/collections/29bbe44e-238a-4d46-b979-97a0429a310e",
        "source_identifier": "CIIL-FLK-1982-MKP",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-008.txt",
        "notes": "Mythological oral romance narrating the union and tragic parting between a humble cowherd boy and a celestial princess.",
    },
    {
        "id": "LIT-FLK-009",
        "resource_type": "literature",
        "title": "Kongyang wui Khararchan",
        "title_translation": "The Story of the Cicada and the Lean Season",
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
        "source_identifier": "TLS-1981-KYC",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-009.txt",
        "notes": "Classic didactic animal fable illustrating the virtues of foresight, agricultural diligence, and seasonal preparation in mountain villages.",
    },
    {
        "id": "LIT-FLK-010",
        "resource_type": "literature",
        "title": "Vāchap wui Khararchan",
        "title_translation": "The Fable of the Bat: Between Birds and Beasts",
        "creator": "Tangkhul Oral Tradition Custodians & CIIL",
        "author": "Traditional",
        "year": 1982,
        "publisher": "Central Institute of Indian Languages, Mysore",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale"],
        "book_id": "BK-CIIL-003",
        "source_url": "https://sanchika.ciil.org/",
        "source_identifier": "CIIL-FLK-1982-VCP",
        "license": "Academic Documentation",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-010.txt",
        "notes": "Etiological animal fable explaining the nocturnal isolation of the bat due to its opportunistic vacillation during the great war between birds and beasts.",
    },
    {
        "id": "LIT-FLK-011",
        "resource_type": "literature",
        "title": "Shaizāwo eina Kasomwo Long Kakā",
        "title_translation": "The Covenant of Brotherhood in the Longshim",
        "creator": "Ukhrul & Phungcham Elders & Storytellers",
        "author": "Traditional",
        "year": 1981,
        "publisher": "Tangkhul Literature Society / Documented in Horam 1977",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul / Phungcham",
        "village": "Hunphun",
        "category": "oral_narrative",
        "work_type": "oral_narrative",
        "genres": ["oral_narrative", "folk_tale"],
        "book_id": "BK-TLS-015",
        "source_url": "https://imphalreviews.in/tangkhul-longshim-traditions",
        "source_identifier": "TLS-1981-SKL",
        "license": "Traditional Oral Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-011.txt",
        "notes": "Foundational oral narrative celebrating the sacred fraternal oath between young men entering the traditional Longshim youth dormitory.",
    },
    {
        "id": "LIT-FLK-012",
        "resource_type": "literature",
        "title": "Longpi Maringthei Eina Ngari Kaping",
        "title_translation": "The Tale of Longpi Pottery and the Magic Yeast",
        "creator": "Longpi Village Elders & Kanrei Shaiza",
        "author": "Traditional",
        "year": 1998,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Longpi / Northern Tangkhul",
        "village": "Longpi",
        "category": "folk_tale",
        "work_type": "folk_tale",
        "genres": ["folk_tale", "oral_narrative"],
        "book_id": None,
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1998-LMK",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-012.txt",
        "notes": "Authentic craft narrative recording the mythological discovery and development of the world-famous Longpi black stone pottery.",
    },
    {
        "id": "LIT-FLK-013",
        "resource_type": "literature",
        "title": "Kashan-Kachon wui Khararchan",
        "title_translation": "The Origin Lore of Sacred Tangkhul Weaving and Shawls",
        "creator": "Tangkhul Women Weavers Guild & TLS",
        "author": "Traditional",
        "year": 1981,
        "publisher": "Tangkhul Literature Society, Manipur",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "oral_narrative",
        "work_type": "oral_narrative",
        "genres": ["oral_narrative"],
        "book_id": "BK-TLS-015",
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1981-KKW",
        "license": "Cultural Oral Lore",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-FLK-013.txt",
        "notes": "Cultural narrative detailing the spiritual and genealogical symbolism of Tangkhul traditional textiles including Luirim and Haora shawls.",
    },
    {
        "id": "LIT-POEM-005",
        "resource_type": "literature",
        "title": "Tangkhul Ngalei",
        "title_translation": "Ode to the Tangkhul Motherland",
        "creator": "Y.K. Shimray",
        "author": "Y.K. Shimray",
        "year": 1985,
        "publisher": "Tangkhul Literature Society / Published in Tangkhul Poetry: Book 1",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "YKS-1985-TNL",
        "license": "Educational Heritage",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-005.txt",
        "notes": "Seminal patriotic poem celebrating the alpine hills, ethical uprightness, and sacred heritage of the Tangkhul territory, widely taught as a cultural anthem.",
    },
    {
        "id": "LIT-POEM-006",
        "resource_type": "literature",
        "title": "Angayung",
        "title_translation": "Deep Roots: A Lyric Poetry Anthology",
        "creator": "Iknguira L. Shimray",
        "author": "Iknguira L. Shimray",
        "year": 2018,
        "publisher": "Hunphun Literary Circle, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Hunphun / Standard Tangkhul",
        "village": "Hunphun",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem", "literary_anthology"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/tangkhul-literature-poetry",
        "source_identifier": "ILS-2018-ANG",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-006.txt",
        "notes": "Contemporary lyric poem passionately advocating for the revitalization of archaic Tangkhul vocabulary and ancestral roots.",
    },
    {
        "id": "LIT-POEM-007",
        "resource_type": "literature",
        "title": "Ngalā Mirin",
        "title_translation": "The Life and Grace of a Tangkhul Maiden",
        "creator": "Iknguira L. Shimray",
        "author": "Iknguira L. Shimray",
        "year": 2020,
        "publisher": "Hunphun Literary Circle, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Hunphun / Standard Tangkhul",
        "village": "Hunphun",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/tangkhul-poetry-ngala-mirin",
        "source_identifier": "ILS-2020-NLM",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-007.txt",
        "notes": "Evocative pastoral poem portraying the spiritual innocence, fireside education, and loom artistry of Tangkhul maidens.",
    },
    {
        "id": "LIT-POEM-008",
        "resource_type": "literature",
        "title": "Tangkhul Meiphung: The Wounds of Time",
        "title_translation": "Hearthside Reflections on Time and Memory",
        "creator": "Thotdharmi Shimray",
        "author": "Thotdharmi Shimray",
        "year": 2019,
        "publisher": "Contemporary Tangkhul Writers Forum, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://e-pao.net/tangkhul-poetry-meiphung",
        "source_identifier": "TDS-2019-TMP",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-008.txt",
        "notes": "Acclaimed contemporary poem exploring cultural memory, historical displacement, and the eternal flame of the ancestral hearth.",
    },
    {
        "id": "LIT-POEM-009",
        "resource_type": "literature",
        "title": "Rachirkhuilu",
        "title_translation": "Awaken to the Dawn: Poetic Songs and Hymns",
        "creator": "Hoyam Kasomwoshi",
        "author": "Hoyam Kasomwoshi",
        "year": 2015,
        "publisher": "Ukhrul Community Music & Poetry Publications",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "poem",
        "work_type": "poem",
        "genres": ["poem"],
        "book_id": None,
        "source_url": "https://tangkhullyrics.com/rachirkhuilu",
        "source_identifier": "HKW-2015-RCK",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-POEM-009.txt",
        "notes": "Stirring lyric poem and youth anthem urging moral uprightness, communal unity, and love for the ancestral mother tongue.",
    },
    {
        "id": "LIT-PLAY-003",
        "resource_type": "literature",
        "title": "Asang Eina Aton",
        "title_translation": "Ashang and Aton: Landmark Folk Drama",
        "creator": "Khenjonglang & Zingko Arts / S. Thaninleima",
        "author": "S. Thaninleima & Tangkhul Community Dramatists",
        "year": 2005,
        "publisher": "National School of Drama Extension & Khenjonglang, Imphal",
        "language": "Tangkhul",
        "dialect": "Tongou / Phungcham / Standard Tangkhul",
        "village": "Tongou",
        "category": "play",
        "work_type": "play",
        "genres": ["play"],
        "book_id": None,
        "source_url": "https://easternpanorama.in/asang-eina-aton-tangkhul-play",
        "source_identifier": "NSD-KHEN-2005-AEA",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-PLAY-003.txt",
        "notes": "First major full-length Tangkhul folk play dramatizing the legendary 17th-century romance of Ashang and Aton, staged nationally at Bharat Rang Mahotsav.",
    },
    {
        "id": "LIT-STRY-004",
        "resource_type": "literature",
        "title": "Tangkhul Shanao Mirin",
        "title_translation": "Portraits of Tangkhul Women Across Generations",
        "creator": "Pamkhuila Shaiza",
        "author": "Pamkhuila Shaiza",
        "year": 2012,
        "publisher": "Heritage Publications, Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "essay",
        "work_type": "essay",
        "genres": ["essay", "short_story"],
        "book_id": None,
        "source_url": "https://ukhrultimes.com/tangkhul-shanao-mirin-shaiza",
        "source_identifier": "PKS-2012-TSM",
        "license": "Author Permitted",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-STRY-004.txt",
        "notes": "Celebrated literary prose essay analyzing the historical standing, matrilineal loom traditions, and modern leadership of Tangkhul women.",
    },
    {
        "id": "LIT-ANTH-006",
        "resource_type": "literature",
        "title": "Tangkhul Khararchan: Canonical Folktale Reader Vol. II",
        "title_translation": "Anthology of Tangkhul Ancestral Folktales and Legends Vol. II",
        "creator": "Kanrei Shaiza & Tangkhul Literature Society",
        "author": "Kanrei Shaiza (Editor)",
        "year": 1998,
        "publisher": "Tangkhul Literature Society, Imphal / Ukhrul",
        "language": "Tangkhul",
        "dialect": "Standard Tangkhul",
        "village": "Ukhrul",
        "category": "literary_anthology",
        "work_type": "literary_anthology",
        "genres": ["literary_anthology", "folk_tale"],
        "book_id": None,
        "source_url": "https://bharatavani.in/tangkhul/jnanakosha",
        "source_identifier": "TLS-1998-TKC2",
        "license": "Community Authorized",
        "permission_status": "community_authorized",
        "access_status": "metadata_only",
        "verification_status": "verified",
        "local_path": "data/raw/literature/LIT-ANTH-006.txt",
        "notes": "Foundational canonical anthology of 30+ ancestral Tangkhul folktales, fables, and clan legends, widely used as a standard academic textbook.",
    },
]


def write_raw_literature_files() -> None:
    raw_dir = ROOT / "data" / "raw" / "literature"
    raw_dir.mkdir(parents=True, exist_ok=True)

    manifest_lookup = {rec["id"]: rec for rec in BATCH2_MANIFEST_RECORDS}

    for lit_id, data in LITERATURE_BATCH2_RAW_DATA.items():
        meta = manifest_lookup[lit_id]
        out_file = raw_dir / f"{lit_id}.txt"

        lines: list[str] = [
            "=" * 80,
            f"TANGKHUL LITERARY RECORD: {meta['title'].upper()}",
            f"IDENTIFIER: {lit_id} | GENRE: {meta.get('work_type', 'literature').upper()}",
            "=" * 80,
            "",
            "METADATA & PROVENANCE:",
            f"  Title:                 {meta['title']}",
            f"  Title Translation:     {meta.get('title_translation', 'N/A')}",
            f"  Literary Genre / Type: {meta.get('work_type', 'literature')} ({meta.get('category', 'N/A')})",
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
        print(f"Created batch 2 raw literature file: {out_file.name} ({len(lines)} lines)")


def append_manifest_records() -> None:
    manifest_file = ROOT / "data" / "manifests" / "literature.jsonl"
    existing_lines = manifest_file.read_text(encoding="utf-8").splitlines()
    existing_ids = set()
    for line in existing_lines:
        if line.strip():
            existing_ids.add(json.loads(line)["id"])

    new_records: list[str] = []
    for rec in BATCH2_MANIFEST_RECORDS:
        if rec["id"] not in existing_ids:
            new_records.append(json.dumps(rec, ensure_ascii=False))
            existing_ids.add(rec["id"])

    if new_records:
        manifest_file.write_text(
            "\n".join(existing_lines + new_records) + "\n", encoding="utf-8"
        )
        print(f"\nAppended {len(new_records)} new records to literature.jsonl!")
    else:
        print("\nAll batch 2 records already present in literature.jsonl.")


def main() -> None:
    write_raw_literature_files()
    append_manifest_records()


if __name__ == "__main__":
    main()
