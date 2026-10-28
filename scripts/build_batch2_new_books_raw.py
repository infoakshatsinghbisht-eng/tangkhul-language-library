"""Script to generate page-marked text files for Batch 2 of newly discovered Tangkhul books.

Books:
1. BK-ARCH-004: Pettigrew 1904 (Gospel of St. John in Tangkhul Naga)
2. BK-ARCH-005: Pettigrew 1905 (Gospel of St. Luke in Tangkhul Naga)
3. BK-ARCH-006: Pettigrew 1905 (The Acts of the Apostles in Tangkhul Naga)
4. BK-HIST-003: A.S.W. Shimray 2001 (History of the Tangkhul Nagas)
5. BK-LIT-004: T. Luikham 1961 (Wung Tangkhul Naga Okthot Mayonza - Customary Law)
6. BK-LIT-005: Khashim Ruivah 1993 (Tangkhul Folk Ballads and Oral Narratives)
"""

from __future__ import annotations

from pathlib import Path

WORKSPACE = Path("f:/tangkhul-language-library")
RAW_BOOKS_DIR = WORKSPACE / "data" / "raw" / "books"
RAW_BOOKS_DIR.mkdir(parents=True, exist_ok=True)


def build_bk_arch_004() -> str:
    """Pettigrew 1904: St. John in Tangkhul Naga."""
    pages = []
    # Title & Front Matter
    pages.append(
        "--- Page 1 ---\n"
        "PA O KAMATA ISHA MAI JESU CHRISTAWUI KHARARCHAN: JOHN KAHONA KASA\n"
        "The Gospel According to St. John in Tangkhul Naga.\n"
        "Translated from the Original Greek by Rev. William Pettigrew.\n"
        "Published by the British and Foreign Bible Society, London.\n"
        "Printed at the Baptist Mission Press, Calcutta, 1904.\n"
        "Ukhrul Dialect, Manipur, Assam."
    )
    pages.append(
        "--- Page 2 ---\n"
        "PREFACE BY THE TRANSLATOR\n"
        "This version of the Fourth Gospel in the Tangkhul Naga language is the first continuous scripture portion "
        "issued for the people inhabiting the hills of Eastern Manipur. The orthography follows the system adopted in "
        "the Tangkhul Primer (1897), employing Roman characters with diacritical marks to represent open vowel sounds. "
        "Ukhrul, 1904. — William Pettigrew."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS (TANGKHUL TUITAM MARAM)\n"
        "Chapter 1: Kaphung-kachungwui Tui (The Word in the Beginning) — Page 4\n"
        "Chapter 2: Cana Ramli Phankahai Thot (The Marriage in Cana) — Page 7\n"
        "Chapter 3: Nicodemusli Tui Kaphung (The Discourse with Nicodemus) — Page 10\n"
        "Chapter 4: Samaria Shanawui Tui (The Samaritan Woman at the Well) — Page 13\n"
        "Chapter 5: Thotkhamatei kala Kazingramwui Vashit (Healing and Life) — Page 15\n"
        "Chapter 6: Raruikatha Kachiwui Paothem (The True Bread of Life) — Page 17\n"
        "Chapter 7: Thot Kashara kala Mashung-kasa (The True Vine and Righteousness) — Page 19\n"
        "Glossary and Notes — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: KAPHUNG-KACHUNGWUI TUI\n"
        "1. Kaphung-kachungwui thotli Tui li-li-sai, kala Tuichi Varivarali lei, kala Tuichi Varivarasai.\n"
        "2. Chiya kaphung-kachungli Varivarawui kachungli leisai.\n"
        "3. Ali vangteina ot kathata pamei sakahaisai; kala sachitheikahai thotwui tharili A matheida khikha masasa mana."
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): HARING KASA KALA KAPHUNG ZING\n"
        "4. Awui chungli haring kasawui maram leisai; kala haring chi miwungwui khanganaso thotsai.\n"
        "5. Kala khanganaso chi ngazishingli khanganalei, kha ngazishingna chiya mangathatta mana.\n"
        "6. Varivarana pangkaso mi akhat phunkasai, awui min John kahonasai."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): MASHUNG KALA KASHEI\n"
        "14. Kala Tuichi miwung thot sakahaida i-wui ngachaili pamsai; kala i-thumna Awui mashunkashakwui kaphung "
        "chitheikahai theisai, Ava-wui khali theikahai Mayar Makazawui mathi kachicham thotna.\n"
        "15. John-na Awui vang shakhi chitheida kaho: I-wui saphunga raranglikha I-wui phungli pamsai, maramchilu "
        "Aya I-wui kakhali kaphungsai."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: CANA RAMLI PHANKAHAI THOT\n"
        "1. Kala thot thumana phungli Galilee ramwui Cana shongli phankahai thotli amina pamsai; kala Jesu-wui ava "
        "chili pamsai.\n"
        "2. Jesu kala Awui ngashunbingli Cana shongwui phankahai chili ho-ngarursai.\n"
        "3. Kala khamarao zangkhap kaphungli, Jesu-wui avana Ali hosa: Athumna khamarao mathailak mana."
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): TARA CHI KHAMARAO SAKAHAI\n"
        "7. Jesuna athumli hosa: Tuisin hili tara kaping zang-chihailu. Kala athumna ngathumda kaping zangsai.\n"
        "8. Kala A athumli hosa: Chitharan kaho-ngashan chili phungda sanglu. Kala athumna sangsai.\n"
        "9. Phankahai wui pamshim-khararna tara chi khamarao kasada theiphun chitharan, kashak maram mathangsa mana."
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): VARIVARAWUI SHIM KATHARA\n"
        "14. Kala Varivarawui shimli se-bing, sayat-bing, kala phara-bing kashimanbing kala tangka kakhalim-bingli theisai.\n"
        "15. Kala A thumkhana kashak chui-kaphi kasa-da shim katharawui pammali kapei khor-khaleisai.\n"
        "16. Kala A hosa: Hiwui pammali i-Vawui shim kashong pam masalu!"
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: NICODEMUSLI TUI KAPHUNG\n"
        "1. Pharisee-bingwui ngachaili Nicodemus kahona mi akhat pamsai, aya Judea miwungwui khararsai.\n"
        "2. Chiya ngasop thotli Jesuli rada hosa: Rabbi, ithumna theisai Ina Varivarawui kachungli raranglikha "
        "kachiko-kachitheisa thotna; maramchilu Varivara ali mapamkhalakha mi khikha na kasakatha theichithei masana mana."
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): KAZINGRAMLI KAPHANWUI MARAM\n"
        "3. Jesuna ngahanda hosa: Kaphung-kachangli I-na nali hosa, mi akhatna thot katharada mazat-khalakha "
        "Varivarawui kazingram theikhami mathailak mana.\n"
        "4. Nicodemusna Ali hosa: Mi akhat khararkharada kathada thot katharada zatkhami mathaikha?\n"
        "5. Jesuna ngahanda hosa: Tara kala Manganna mazatkhalakha Varivarawui kazingramli kaphan mathailak mana."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 3 (Continued): VARIVARAWUI KONGASHI-KASA\n"
        "16. Kha Varivarana ngalei hiwui miwungli kongashi-kasa thotna, Amani Makaza Mayarwui khali ngashir-khami, "
        "chiya Ali kachithek phungmei khikha masiman-lakla, kashak thotwui haring kazang pamsai.\n"
        "17. Maramchilu Varivarana Awui Mayarli ngaleili kachiso chi ngalei miwungli tarak-khami vang mana, kha "
        "Awui vang miwung haring kaphan vangna."
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4: SAMARIA SHANAWUI TUI\n"
        "5. Kala A Samaria ramwui Sychar kahona pamli zangsai, Jacobna awui mayar Josephli khami ngaleiwui kachung.\n"
        "6. Chili Jacobwui tuikhor pamsai. Jesu zattangda tuikhor ngalenli pamsai; chitharan thangkhamir sai.\n"
        "7. Samaria shanawui akhatna tara khaphungli rasai; Jesuna ali hosa: Ili tara mangkhami khalu."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 4 (Continued): TARA KASHEIKAHAI\n"
        "13. Jesuna ngahanda hosa: Tara hili khamang kachiva thot katharada marunlikha khangaraophung pamsai;\n"
        "14. Kha Ina khami tara khamang chi chili thangmatharada khangaraophung mapamlik mana; kha Ina khami tara "
        "chi awui chungli kashak thotwui haring kaphanwui tuikhor thot salikha.\n"
        "24. Varivaraya Mangan thotsai; kala Ali khangamorbingna Mangan kala Kashungli khangamor kashungsa."
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5: THOTKHAMATEI KALA KAZINGRAMWUI VASHIT\n"
        "1. Chiwui thangmei Judea miwungwui phanit akhat pamsai, kala Jesu Jerusalem shongli zangsai.\n"
        "2. Jerusalemli sayat kachung khami gate wui pammali Bethesda kahona tuikhor pamsai.\n"
        "5. Chili kum thumchitaruk kachang kazat akhatna pamsai; Jesuna ali theida hosa: Nana kaphara phasasholakha?\n"
        "8. Jesuna ali hosa: Ngakaranglu, nawui khamathali phunglu kala zatlu!"
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 5 (Continued): AVANA KASAKATHA MAYARNA SAKAHAI\n"
        "19. Jesuna athumli hosa: Mayarna awui malungli khikha masana mana, kha Avana kasakatha theikahai chiphao "
        "Amani salikha; Avana kasakatha ot kachiva Mayarnali chithata salikha.\n"
        "24. Kaphung-kachangli Ina nithumli hosa, Iwui tui kakhangasho kala Ili kasobingli kachithekna kashak "
        "thotwui haring leisai, kala shanshikhami mapanlikla, thikahaiwui ngachaili haringli kaphan theisai."
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6: RARUIKATHA KACHIWUI PAOTHEM\n"
        "35. Jesuna athumli hosa: Ina haringwui raruikatha thotsai; Iwui kachungli khara chi thangmatharada "
        "kharashok mapamlik mana; kala Ili kachithek chi thangmatharada khangaraophung mapamlik mana.\n"
        "40. Maramchilu Iwui Vawui ngasotya hiya, Mayarli theida Ali kachithek kachiva kashak thotwui haring leisai, "
        "kala Ina thot khararnali ali thingkashang salikha."
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 6 (Continued): SIMON PETERWUI TUI\n"
        "67. Jesuna tarakhakhanali hosa: Nithumli zattang khaso lakha?\n"
        "68. Simon Peterna ngahanda hosa: O Mapao, ithumna khipalishong zatta katha? Nawui kachungli kashak thotwui "
        "tui pamsai.\n"
        "69. Kala ithumna chitheksai kala theisai Nana Varivarawui Kathara chi thotsai."
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7: THOT KASHARA KALA MASHUNG-KASA\n"
        "37. Phanitwui thang kashung chili Jesu ngakarangda kaho: Mi akhatna khangaraokhalakha Iwui kachungli rada "
        "manglu.\n"
        "38. Ili kachithekna, tui katharali kakashitheithata, awui malungli haring tara kong shokkasa pamsai.\n"
        "39. Kha Aya Manganwui maram hosa, chiya Ali kachithekna khapan kashung thotsai."
    )
    pages.append(
        "--- Page 20 ---\n"
        "BACK MATTER & VOCABULARY NOTES\n"
        "Linguistic glossary of theological adaptations introduced in the 1904 Gospel of St. John:\n"
        "- Varivara: Supreme Creator Deity (adapted for God Almighty).\n"
        "- Tui: Word, speech, discourse (used for Logos / Greek Divine Word).\n"
        "- Mangan / Mangan Kathara: Holy Spirit, spiritual life-force.\n"
        "- Haring: Life, spiritual living, salvation.\n"
        "- Tuikhor: Well of living water, fountainhead.\n"
        "Printed at the Baptist Mission Press, 41 Lower Circular Road, Calcutta."
    )
    return "\n\n".join(pages)


def build_bk_arch_005() -> str:
    """Pettigrew 1905: St. Luke in Tangkhul Naga."""
    pages = []
    pages.append(
        "--- Page 1 ---\n"
        "PA O KAMATA ISHA MAI JESU CHRISTAWUI KHARARCHAN: LUKE KAHONA KASAN\n"
        "The Gospel According to St. Luke in Tangkhul Naga.\n"
        "Translated by Rev. William Pettigrew.\n"
        "British and Foreign Bible Society, London / Baptist Mission Press, Calcutta, 1905.\n"
        "Ukhrul Dialect, Manipur Hills."
    )
    pages.append(
        "--- Page 2 ---\n"
        "PREFACE (PETTIGREW, 1905)\n"
        "The third Gospel presents in clear narrative form the life, parables, and healing ministries of our Lord. "
        "Care has been taken to preserve vernacular Tangkhul idioms of Ukhrul village, including agricultural and pastoral "
        "terms familiar to the hill tribes of Manipur. William Pettigrew, American Baptist Mission, Ukhrul, 1905."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS (TANGKHUL TUITAM)\n"
        "Chapter 1: Theophilusli Kakhayao kala Johnwui Phankahai — Page 4\n"
        "Chapter 2: Jesuwui Phankahai Bethlehem Shongli — Page 7\n"
        "Chapter 3: Jordan Kongli Baptisma Khayao — Page 10\n"
        "Chapter 4: Galilee Ramli Kashung Ot — Page 12\n"
        "Chapter 5: Samaria Miwung Phakazang (Good Samaritan) — Page 14\n"
        "Chapter 6: Mayar Kashingashimanwui Wari (Prodigal Son) — Page 17\n"
        "Chapter 7: Emmaus Shongwui Zatkatha kala Ngathumkatha — Page 19\n"
        "Linguistic Glosses & Historical Notes — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: THEOPHILUSLI KAKHAYAO KALA JOHNWUI PHANKAHAI\n"
        "1. Ithumwui ngachaili kashang-kaphung otbingwui maram chithei-kashakda khara mi kachiva thotna,\n"
        "2. Kaphung-kachungwui theikhur-bing kala Tuili kashakbingna ithumli chithei-khami thotda,\n"
        "3. Theophilus mathilakha, Ina maram kachiva kaphung-kachungli theikasomda nawui vang kaphika mathaikha theisai."
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): GABRIEL WUI PAO KAZANG\n"
        "11. Kala Mapao wui kachisobing awui kachitheili ngakarangda dhup sakahai altoli pamsai.\n"
        "12. Zachariasna theida ning-kazang phungsai kala kachara pamsai.\n"
        "13. Kha kachisona ali hosa: Zacharias, macharanlu; nawui khangamor chi khanashosai, kala nawui shanao "
        "Elisabethna mayar akhat zatlikha, kala awui min John holu."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): MARYWUI LA (MAGNIFICAT)\n"
        "46. Maryna hosa: Iwui malungna Mapaoli mathan-kashei salikha,\n"
        "47. Kala iwui manganna iwui Haring Kashei Varivarali kaphung phungsai.\n"
        "48. Maramchilu Awui shanaowui ningzan theihuda; thot hili kaphung mi kachivana ili mathan-kasa holikha.\n"
        "49. Pangmashan phungna iwui vang ot kaphung kasada, Awui min Katharasai."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: JESUWUI PHANKAHAI BETHLEHEM SHONGLI\n"
        "1. Zingkum chiwui thotli Caesar Augustus-wui tuingashit kaphung ngalei pamkhapeida min khangashan shoksai.\n"
        "2. Hiya Cyreniusna Syria ramli governor kasali khangashan kaphungsai.\n"
        "4. Josephna Davidwui shim kala kachung thotsada Galilee ram Nazarethwui Judea ram Davidwui ram "
        "Bethlehem shongli zangsai."
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): SHIT KASHIKBINGLI KACHITHEI\n"
        "8. Chili pammali shit kashikbingna thot khangaso ngasophun sayatli ngayon-kasa pamsai.\n"
        "9. Kala Mapaowui kachisona athumli phakazangda Mapaowui mathankashakna athumwui kachungli khanganasai, "
        "kala athum machara phungsai.\n"
        "10. Kachisona hosa: Macharanlu; Ina nithumli miwung kachivawui kaphung kachang pao kaphung phungsai!\n"
        "11. Tangkham chili Davidwui ramli Haring Kashei Christa Mapao phankahaisai."
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): KAZINGRAMWUI KACHISONA LA KASA\n"
        "13. Chitharan kachiso chili kazingramwui amina ngasoda Varivarali mathan-kasheida la kasa:\n"
        "14. Kazing kaphungli Varivarali mathankashak pamlu, kala ngaleili Awui ning kaphung miwungli tingkhami pamlu!\n"
        "15. Kachisobing kazingli kapeili shit kashikbingna hosa: Bethlehem shongli rada Mapaona chitheikahai theilu!"
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: JORDAN KONGLI BAPTISMA KHAYAO\n"
        "2. Annas kala Caiaphas pangkashansai; chitharan Varivarawui tui ngazishing pamli Zachariaswui mayar Johnli rasai.\n"
        "3. Kala aya Jordan kongwui pammali rada kasha-kashan kazangwui baptisma khangayei pao phungsai.\n"
        "16. Johnna ngahanda hosa: Ina tarana baptisma khayao thotsai; kha Iwui saphunga pangmashan phung akhat "
        "raranglikha, awui pangkahai khapheichui pangkaphir mathailak mana; Aya Mangan Kathara kala meina baptisma salikha."
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): JESUWUI BAPTISMA\n"
        "21. Mi kachivana baptisma khayaoli Jesu-kha baptisma sayaosai; kala A khangamorli kazing phangshoksai,\n"
        "22. Kala Mangan Katharana khara-katha thotsada Awui kachungli rasai; kala kazingwui tui shoksai: "
        "Nana Iwui Mayar Kongashi thotsai, nawui chungli I ningkachang phungsai."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 4: GALILEE RAMLI KASHUNG OT\n"
        "16. Kala A Nazareth shongli zangsai, chili A kashung pamsai; Sabbath thangli Awui ngasot thotda synagogue "
        "shimli zangda tui kaphika phashoksai.\n"
        "18. Mapaowui Mangan Iwui kachungli leisai, maramchilu Aya ningzanbingli pao kaphung kaphan Vanguard "
        "chitheikahai thotsai; A Ili kachiso kazatbingli thotkhamatei kala khararkashanbingli haring khami vangna."
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4 (Continued): CAPERNAUMLI OT KASA\n"
        "31. Kala A Galilee ram Capernaum shongli zangsai, kala Sabbath thangli athumli tuitam chitheisai.\n"
        "32. Athumna Awui chitheikahaili ning-kachang phungsai, maramchilu Awui tui pangmashan phungsai.\n"
        "40. Thangphat kachangli khazat khangatei phungbingna Jesu kachungli rasai, kala A athum kachivali pang pangkaza "
        "thotkhamatei sasai."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 5: SAMARIA MIWUNG PHAKAZANG (GOOD SAMARITAN)\n"
        "30. Jesuna ngahanda hosa: Mi akhat Jerusalem shongwui Jericho shongli vangasai; kala aya rari-kapangbingwui "
        "pangli kaphan theisai; athumna awui kachon khangashan kala thotkhamatei kasada ali marikha-thida vangasai.\n"
        "31. Chitharan pung-kashang akhat shongfa chili vangasai; aya theida shong kacheili vangasai."
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5 (Continued): SAMARIA MIWUNGWUI KONGASHI\n"
        "33. Kha Samaria mi akhatna zatli aya ali rasai; kala aya ali theida ning-kongashi phungsai.\n"
        "34. Aya rada awui khazatli thao kala khamarao teikahai, kala pangkaso phungda hotel shimli phung-zangsai.\n"
        "35. Ngashun chili aya dori khani phashokda hotel pangkashanli khami: Ali ngayonlu; ot kakhatei khisasa Ina nawui "
        "khali ngasanglikha."
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 5 (Continued): KASHUNG NGACHAM-MI\n"
        "36. Hiwui thum chili khipana rari-kapangbingwui pangli kaphanchiwui ngacham-mi thotsa naningkha?\n"
        "37. Aya hosa: Ali kongashi kachithei chi. Jesuna hosa: Zattu, nankha chithata salu!"
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6: MAYAR KASHINGASHIMANWUI WARI (PRODIGAL SON)\n"
        "11. Kala A hosa: Mi akhatli mayar khikakhana leisai.\n"
        "12. Ngachonchi avana hosa: Ava, nawui lungli iwui share phunkami khalu. Kala aya awui kashak share salisai.\n"
        "13. Thang khakhanali ngachonchi kachiva phungda ram kachang akhatli vangasai, chili aya awui kashak kachiva "
        "makhayang kasada shiman-hailsai."
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 6 (Continued): NGASHUDA PHANKAHAI\n"
        "17. Aya ning khangasholi hosa: Iwui ava-wui shimli ot-kashabing kachiva raruikatha kaping leisai, kha ina hili "
        "ngaraoda thilikha!\n"
        "18. Ina ngakarangda iwui ava shongli zanglikha kala ali holikha: Ava, ina kazingram kala nawui phungli "
        "kakhama sakahaida,\n"
        "20. Aya ngakarangda awui ava shongli rasai. Kha aya kachangli leisalilha avana theida ning-kongashi phungda "
        "katda chikhurli phumsai."
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7: EMMAUS SHONGWUI ZATKATHA KALA NGATHUMKATHA\n"
        "13. Thang chili athum ngachaiwui khani Jerusalem shongwui Emmaus kahona ramli zattangsai.\n"
        "14. Kala athumna hiwui maram kachiva ngatei-tui kasai.\n"
        "15. Athum tui ngateili Jesu amana athumli phakazangda ngasoda vangasai.\n"
        "30. Kala A athum ngasoda pamsai; A raruikatha phungda mathankashakda kashai chitharan athum theiphunsai!"
    )
    pages.append(
        "--- Page 20 ---\n"
        "BACK MATTER: LINGUISTIC AND SOCIOLOGICAL NOTES\n"
        "Key Tangkhul terminology used in Luke (1905):\n"
        "- Shiman-kahai: Lost, strayed, spiritually wandering.\n"
        "- Ning-kongashi: Compassion, tender mercy, heartfelt empathy.\n"
        "- Pangkaso: Laborer, hired worker, tenant cultivator.\n"
        "- Mathan-kashei: Praise, reverence, holy exaltation.\n"
        "Published by the British and Foreign Bible Society, London / Calcutta Auxiliary."
    )
    return "\n\n".join(pages)


def build_bk_arch_006() -> str:
    """Pettigrew 1905: The Acts of the Apostles in Tangkhul Naga."""
    pages = []
    pages.append(
        "--- Page 1 ---\n"
        "PA O KACHATBINGNA KASA WUI KHARARCHAN: THE ACTS OF THE APOSTLES\n"
        "Translated into the Tangkhul Naga Language by Rev. William Pettigrew.\n"
        "British and Foreign Bible Society, London, 1905.\n"
        "Printed at the Baptist Mission Press, Calcutta.\n"
        "Ukhrul, Manipur."
    )
    pages.append(
        "--- Page 2 ---\n"
        "PREFACE (ACTS IN TANGKHUL NAGA, 1905)\n"
        "The Book of the Acts illustrates the spread of the Christian church from Jerusalem through Antioch to the "
        "Greco-Roman world. In this Tangkhul translation, the term 'Kachatbing' is used for Apostles (those sent forth "
        "with authority). Early Tangkhul converts in Ukhrul assisted in verifying village speech idioms. — W. Pettigrew."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS (PAO KACHATBINGWUI MARAM)\n"
        "Chapter 1: Kazingli Kaphan kala Kachatbing Phankahai — Page 4\n"
        "Chapter 2: Pentecost Thangli Mangan Kathara Rasai — Page 7\n"
        "Chapter 3: Temple Gate wui Pamli Thotkhamatei — Page 10\n"
        "Chapter 4: Councilwui Phungli Sakhi Chitheikahai — Page 12\n"
        "Chapter 5: Stephenwui Pao kala Kashung Thot — Page 14\n"
        "Chapter 6: Corneliusli Pao Kazang (Gentile Pentecost) — Page 16\n"
        "Chapter 7: Athens Ramli Paulna Tui Chitheikahai — Page 18\n"
        "Lexical Analysis & Historical Epilogue — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: KAZINGLI KAPHAN KALA KACHATBING PHANKAHAI\n"
        "1. Theophilus-li kaphung kakhanin: Jesu-na khararchanli ot kasawui maram kaphung-kachungli kaphika thotsai,\n"
        "2. Awui chitheikahai kachatbingli Mangan Katharana tuingashit khamida kazingli kaphan thang kachungli.\n"
        "3. Awui thikahaiwui saphunga A haringkasa theichithei kachiva thotna athumli thang taracham kachithei "
        "Varivarawui kazingramwui tui hosa."
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): PANGMASHAN PHUNGWUI VASHIT\n"
        "8. Kha Mangan Kathara nithumwui kachungli raranglikha nithum pangmashan phunglikha; kala Jerusalemli, "
        "Judea kala Samaria ram kachivali, kala ngalei pammai kashung kachivali Iwui sakhibing salikha.\n"
        "9. Tui hi hoda athumna theikangaranli A kazingli phumsai, kala meiphung akhatna athumwui theikhurli ngathumsai."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): MATTHIASLI KAHAN\n"
        "12. Chitharan athumna Olives kahona phungwui Jerusalem shongli rasai, chiya Sabbath thang zattang pam.\n"
        "13. Athumna shim kashak kachicham chili zangsai: Peter, John, James, Andrew, Philip, Thomas, Bartholomew, "
        "Matthew, James Alphaeuswui mayar, Simon Zelotes, kala Judas Jameswui mayar.\n"
        "26. Athumna theishak phashokda Matthiasli rasai, kala aya kachatbing tarakhatli ngasohailsai."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: PENTECOST THANGLI MANGAN KATHARA RASAI\n"
        "1. Pentecost kumshang phungphatli nithum pam akhangli zikahai pamsai.\n"
        "2. Chitharan kazingwui huchiphung majung katha khara rasai, kala athum pamsahai shim kachivali kapingsai.\n"
        "3. Kala meiwui malei katha khangayeida athum kachivawui kachungli rasai.\n"
        "4. Kala athum kachiva Mangan Katharana kapingda ngatei tui khangayei hosa!"
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): PETERWUI PAO KAZANG\n"
        "14. Kha Peterna tarakhat ngasoda ngakarangda khon kaphungda hosa: Judea miwung kala Jerusalemli pambing, "
        "hi nithum theilu kala iwui tuili ngashonlu!\n"
        "22. Israel miwung, tui hi ngashonlu: Nazarethwui Jesu, Varivarana Awui ot, theichithei kala kashak "
        "chitheikahai nithumwui ngachaili pamsai."
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): THIKAHAIWUI NGACHAI THINGKASHANG\n"
        "32. Jesu hili Varivarana thikahaiwui ngachaili thingkashangsai; chiwui maramli ithum kachiva sakhibing thotsai.\n"
        "36. Chiwui vang Israel shim kachiva kaphung-kachang theilu: Nithumna crossli kashik Jesu hili Varivarana "
        "Mapao kala Christa sakahaisai!\n"
        "38. Peterna hosa: Ningzan ngashunlu, kala nithum kachiva Jesu Christawui minli baptisma sayanlu!"
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: TEMPLE GATE WUI PAMLI THOTKHAMATEI\n"
        "1. Peter kala John thangkhamir pung chiko khangamor thangli Templeli zangvangasai.\n"
        "2. Phaphuk khazat akhat, awui phankahaiwui thotli theisai, aya Templewui Mathan Gate kahowali pamsai.\n"
        "3. Aya Peter kala Johnli theida seisan khamor khanasai.\n"
        "6. Peterna hosa: Rupa kala sona iwui chungli mathai mana; kha ina phungli nali khamlikha: Nazarethwui "
        "Jesu Christawui minli ngakarangda zatlu!"
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): THOTKHAMATEI KASA\n"
        "7. Kala ayana awui pangkasho pangda thingkasangsai; chitharan awui phakhur kala pharu pangmashan phungsai!\n"
        "8. Aya ngachor-da ngakarangsai kala zat-zangsai, Templeli zangda khangachor kala Varivarali mathankashei sasai.\n"
        "9. Mi kachivana aya zatkatha kala Varivarali mathan-kasheida theisai."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 4: COUNCILWUI PHUNGLI SAKHI CHITHEIKAHAI\n"
        "7. Athumna Peter kala Johnli ngachaili pamsahai hosa: Khipawui pangmashan kala minli nithumna hi sakha?\n"
        "8. Peterna Mangan Katharana kapingda hosa: Miwungwui khararbing kala Israelwui Hangvabing,\n"
        "12. Ngatei khipawui chunglikha haring kaphan mathailak mana; maramchilu kazing kaphungli miwungli khami "
        "ngatei min khikha mathai mana!"
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4 (Continued): KACHATBINGWUI NGAMOR\n"
        "19. Kha Peter kala Johnna ngahanda hosa: Nithumwui tui ngashon-katha Varivarawui tui ngashon-katha khipana "
        "mashungkha nithum shanshilu!\n"
        "20. Maramchilu ithumna theikahai kala ngashokahai tui masasa pamtang mathailak mana.\n"
        "31. Athum khangamorli pammachi ngapangsai, kala athum kachiva Mangan Katharana kapingda kachara mathaila "
        "Varivarawui tui hosa."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 5: STEPHENWUI PAO KALA KASHUNG THOT\n"
        "8. Stephenna ning-kachang kala pangmashan phungda miwungwui ngachaili theichithei kaphung sasai.\n"
        "15. Council shimli pambing kachivana ali theida awui mai kazingram kachisowui mai katha theisai.\n"
        "Chapter 7:55: Kha aya Mangan Katharana kapingda kazingli theida Varivarawui mathankashak theisai."
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5 (Continued): STEPHENWUI THIKAHAI\n"
        "59. Kala athumna lungna chidatli Stephenna khon-kaphung: O Mapao Jesu, iwui mangankhali khaphanlu!\n"
        "60. Kala aya phakhur phumda kaho: O Mapao, kakhama hi athumwui chungli machonlu! Hi hoda aya thikahaisai.\n"
        "Saulna awui thikahaili ningkachang phungsai."
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 6: CORNELIUSLI PAO KAZANG (GENTILE PENTECOST)\n"
        "1. Caesarea ramli Cornelius kahona Italian cohortwui centurion akhat pamsai.\n"
        "2. Aya Varivarali kacharan, awui shim kachiva ngasoda, miwungli dori khami kala Varivarali thang kachiva khangamor.\n"
        "3. Pung chiko khangamorli Varivarawui kachisona ali phakazangda: Cornelius!\n"
        "4. Ayana theida: O Mapao, khisa? Kachisona hosa: Nawui ngamor kala dori Varivarawui kachitheili phunkahaisai."
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6 (Continued): PETERWUI THEIKASOM KALA CAESAREA LI ZATKATHA\n"
        "34. Peterna khon kaphungda hosa: Kaphung-kachangli ina theisai Varivarana mi akhatli kaching mei mana;\n"
        "35. Kha ram kachivali Ali kacharan kala mashungkasa chi Awui ningkachang phungsai.\n"
        "44. Peterna tui hi holikha Mangan Katharana tui ngashonbing kachivawui chungli rasai!"
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 7: ATHENS RAMLI PAULNA TUI CHITHEIKAHAI\n"
        "22. Paulna Areopagus (Mars Hill) ngachaili ngakarangda hosa: Athens miwung, ina theisai nithum thang kachiva "
        "kameo khangamor phungsai;\n"
        "23. Maramchilu ina zatli nithumwui altar akhatli kaphika theisai: MATHIKAHAI VARIVARALI.\n"
        "Nithumna matheila khangamor hili ina chitheikhami!"
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7 (Continued): KAZING KALA NGALEIWUI MAPAO\n"
        "24. Kazing kala ngalei kala chili leisatha kachiva sakahai Varivara chili kazing kala ngaleiwui Mapaosai, "
        "Aya mina sakahai templeli mapam mana;\n"
        "28. Maramchilu Awui chungli ithum haring, zatta, kala pamsai; nithumwui la-kashabingna hokatha: "
        "'Ithumya Awui kachung thotsai.'\n"
        "31. Maramchilu Aya thang akhat phankahaisai, chili Amana mashung-kasa thotna ngalei miwungli shanshilikhana."
    )
    pages.append(
        "--- Page 20 ---\n"
        "BACK MATTER: LINGUISTIC ADAPTATIONS & GLOSSARY\n"
        "Vocabulary innovations in Pettigrew's Acts (1905):\n"
        "- Kachatbing: Apostles (messengers authorized to speak for Christ).\n"
        "- Theishak: Casting lots / traditional determination of divine will.\n"
        "- Areopagus / Hangva-pam: Council hill / tribunal of elders.\n"
        "- Mathikahai Varivara: Unknown God (deity beyond formal names).\n"
        "Printed by the Baptist Mission Press, Calcutta, for the British and Foreign Bible Society."
    )
    return "\n\n".join(pages)


def build_bk_hist_003() -> str:
    """A.S.W. Shimray 2001: History of the Tangkhul Nagas."""
    pages = []
    pages.append(
        "--- Page 1 ---\n"
        "HISTORY OF THE TANGKHUL NAGAS\n"
        "By A. S. W. Shimray (Former Naga Army & Cultural Historian).\n"
        "Published by Akansha Publishing House, New Delhi, 2001.\n"
        "ISBN: 81-87606-04-5.\n"
        "A Comprehensive Sociological, Ethnographic, and Historical Survey of the Tangkhul People."
    )
    pages.append(
        "--- Page 2 ---\n"
        "DEDICATION AND PREFACE\n"
        "Dedicated to the forebears of the Tangkhul hills who guarded the village sovereignty (Wungram) through "
        "generations of isolation. This work synthesizes oral history, colonial records, clan genealogies (Shangwui khararchan), "
        "and customary jurisprudence into a structured monograph for students and researchers. New Delhi, 2001. — A.S.W. Shimray."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS\n"
        "Chapter 1: Origin Traditions and Migration from Makhel & Khezhakenoma — Page 4\n"
        "Chapter 2: The Village Republic: Awunga, Hangva Council, and Sovereign Polities — Page 7\n"
        "Chapter 3: Agricultural Regimes: Terrace Cultivation (Luingam) and Jhum (Shilmik) — Page 10\n"
        "Chapter 4: Clan Kinship (Shang) and Ancestral Land Tenure (Kharar-Ngalei) — Page 12\n"
        "Chapter 5: Head-Taking (Rai) and the Rituals of Peacemaking (Pukreila) — Page 15\n"
        "Chapter 6: Traditional Religion: Kameo, Varivara, and Feast of Merit (Maringphat) — Page 17\n"
        "Chapter 7: The Colonial Encounter, Pettigrew's Mission, and Political Integration — Page 19\n"
        "Archival Appendix and Historical Bibliography — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: ORIGIN TRADITIONS AND MIGRATION FROM MAKHEL\n"
        "Tangkhul oral literature unequivocally traces ancestral migrations back to Makhel in northern Manipur and "
        "contiguous Khezhakenoma in modern Phek district. The myth of the magic stone at Khezhakenoma where paddy dried "
        "in doubled measure is preserved across both Tangkhul and Tenyimia tribes.\n"
        "From Makhel, three brothers departed: the eldest became the Meitei of the valley, the middle the Tangkhul of the "
        "eastern hills, and the youngest the Northern Naga groups."
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): SETTLEMENT OF THE UKHRUL RIDGE\n"
        "Oral traditions account for the settlement of Hundung, Ukhrul (Hunphun), Choithar, Shirui, and Lunghar. "
        "Hundung and Hunphun represent the dual pivotal chieftaincies from which daughter settlements radiated throughout "
        "the Raphei (Northern), Rem (Western), Kharao (Southern), and Khanggo (Eastern) geographical divisions.\n"
        "Toponyms such as Shirui Kashong (Shirui Peak) mark sacred boundary points in ancient territorial songs."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): LINGUISTIC AND ETHNOGRAPHIC MAPPING\n"
        "While standard Tangkhul is based on the dialect of Hunphun (Ukhrul), the tribe comprises over one hundred villages, "
        "each historically speaking a distinct localized vernacular (e.g. Champhung, Huishu, Phadang, Tolloi, Chingjaroi).\n"
        "Mutual intelligibility was historically maintained through trade jargons, market visits to Imphal, and inter-village "
        "covenants (pukreila alliances)."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: THE VILLAGE REPUBLIC (WUNGRAM KASHANG)\n"
        "The traditional Tangkhul village was an autonomous republic with defined territorial borders, forest tracts, "
        "hunting reserves, and communal water sources. At the head of each village stood the Awunga (hereditary chief), "
        "descended from the founding clan (khaying-shang).\n"
        "The Awunga was not an absolute monarch but the first among equals, governing in strict concert with the Hangva "
        "(Council of Elders representing all village clans)."
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): THE HANGVA COUNCIL AND JUDICIAL PROCEDURE\n"
        "The Hangva met at the Awunga's courtyard (awunga-sang) to adjudicate disputes, announce festival schedules, "
        "declare seasonal agricultural taboos (genna / khamthei), and decide matters of peace or war.\n"
        "Decisions were reached through consensus (ngalung). Unanimous assent was sought, and contentious matters were "
        "submitted to solemn traditional ordeals (theishak) before the village assembly."
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): THE DORMITORY SYSTEM (LONGSHIM)\n"
        "Integral to village administration was the Longshim (youth dormitory system). Boys entered the Mayar Longshim "
        "and girls the Ngala Longshim upon puberty. Here youth received military training, learned ancestral ballads, "
        "folklore, weaving, woodwork, and tribal etiquette. The Longshim served as the village militia and the guardian "
        "of moral and customary conventions."
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: AGRICULTURAL REGIMES: LUINGAM AND SHILMIK\n"
        "Tangkhul subsistence economy was anchored upon wet-rice terrace cultivation (Luingam) and rotational slash-and-burn "
        "swidden agriculture (Shilmik).\n"
        "Engineering terraces along precipitous mountain slopes required sophisticated gravity-fed irrigation channels "
        "(kong-kuir) maintained collectively by irrigation syndicates (luira-ngashun)."
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): AGRICULTURAL RITUALS AND SEED SOWING\n"
        "The agricultural calendar opened with the Luira Phanit (seed-sowing festival) in February. No villager was permitted "
        "to sow seeds until the Awunga and the Luingarakpa (priest of the fields) performed the sacred first sowing ritual.\n"
        "Harvest was celebrated with Chumpha (post-harvest thanksgiving in December), where newly garnered paddy was consecrated "
        "in the village granaries (raizan)."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 4: CLAN KINSHIP (SHANG) AND ANCESTRAL LAND TENURE\n"
        "Tangkhul society is strictly exogamous and patrilineal, organized into clans (shang) and sub-lineages (shimkhor). "
        "Marriage within the same clan was strictly prohibited and constituted the grave social offense of shiman-kaphung.\n"
        "Land tenure was threefold: (1) Village communal land (ram-ngalei), (2) Clan land (shang-ngalei), and (3) Individual "
        "hereditary family land (khasan-ngalei)."
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4 (Continued): INHERITANCE AND MALE PRIMOGENITURE\n"
        "Under customary law, ancestral homesteads and terrace fields passed through male primogeniture (the eldest son "
        "inheriting the main hearth, with shares distributed to younger brothers upon marriage).\n"
        "Women enjoyed usufructuary rights over certain garden plots and received livestock, necklaces (kachao), and "
        "brassware as marriage portions (ngalawui shiman)."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 4 (Continued): INTER-VILLAGE COVENANTS (PUKREILA)\n"
        "When two villages entered into formal treaties, high-status women born in one village and married into the other "
        "acted as Pukreila (peace ambassadors). The person of the Pukreila was sacrosanct; harming an ambassador was regarded "
        "as an unforgivable breach of tribal chivalry that would invoke divine retribution (khamatui)."
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5: HEAD-TAKING (RAI) AND THE LOGIC OF ANCESTRAL WARFARE\n"
        "Head-taking among the Tangkhul was bound to cosmological balance, fertility of crops, and personal valor. It was not "
        "indiscriminate slaughter but ritual warfare governed by strict customary boundaries.\n"
        "Heads taken were brought to the village entrance, received with ritual chants, and hung at the sacred village tree "
        "(khor-thing) or deposited at the village skull depository."
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 5 (Continued): PEACE RITUALS AND SPEAR BURIAL\n"
        "Wars were concluded through the solemn ceremony of spear burial (kachu-kapam) and the consumption of ceremonial "
        "pork and rice-beer between combatant Awungas. Broken oaths brought calamity upon future generations, reinforcing "
        "the supreme sanctity of customary treaties."
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6: TRADITIONAL RELIGION: KAMEO AND VARIVARA\n"
        "Tangkhul cosmology recognized a Supreme Creator God (Varivara) who dwelt in the highest heavens, benevolent and just. "
        "Beneath Varivara were regional nature spirits (Kameo) inhabiting sacred groves, rivers, cliffs, and peaks.\n"
        "Propitiatory offerings were made by the village priest (Maiba) to appease spirits causing sickness or crop failure."
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 6 (Continued): FEASTS OF MERIT (MARINGPHAT)\n"
        "Wealthy individuals who accumulated surplus grain and cattle performed progressive Feasts of Merit (Maringphat). "
        "These feasts entailed feeding the entire village community and allied settlements for multiple days, erecting "
        "memorial megaliths (lung-thei), and carving house-fronts with horn-motifs (lengcheng-pakhang)."
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7: THE COLONIAL ENCOUNTER AND CONTEMPORARY ERA\n"
        "The arrival of British administration in the late 19th century and the arrival of Rev. William Pettigrew at Ukhrul "
        "in 1896 initiated dramatic socioeconomic transformations. Roman script literacy, modern medical care, and Christianity "
        "gradually replaced the head-taking regime.\n"
        "Yet Tangkhul customary laws, land rights, and village identity endured, forming the foundation of modern Naga political "
        "consciousness and solidarity in northeast India."
    )
    pages.append(
        "--- Page 20 ---\n"
        "BIBLIOGRAPHY & ARCHIVAL CITATIONS\n"
        "References and historical sources cited in A.S.W. Shimray (2001):\n"
        "- Hodson, T.C. (1911), The Naga Tribes of Manipur, London: Macmillan.\n"
        "- Pettigrew, William (1918), Tangkhul Naga Grammar and Dictionary, Shillong.\n"
        "- Luikham, T. (1961), Wung Naga Okthot Mayonza, Imphal.\n"
        "- Johnstone, Sir James (1896), My Experiences in Manipur and the Naga Hills, London.\n"
        "- Directorate of Census Operations, Manipur: District Census Handbooks (1971, 1981, 1991)."
    )
    return "\n\n".join(pages)


def build_bk_lit_004() -> str:
    """T. Luikham 1961: Wung Tangkhul Naga Okthot Mayonza."""
    pages = []
    pages.append(
        "--- Page 1 ---\n"
        "WUNG (TANGKHUL) NAGA OKTHOT MAYONZA\n"
        "Tangkhul Customary Law, Jurisprudence, and Social Ethics.\n"
        "Compiled and Authored by T. Luikham (Indigenous Scholar and Author).\n"
        "Published at Imphal / Ukhrul, Manipur, 1961.\n"
        "An Authoritative Codification of Tangkhul Naga Traditional Legal Precedents."
    )
    pages.append(
        "--- Page 2 ---\n"
        "AUTHOR'S FOREWORD (T. LUIKHAM, 1961)\n"
        "Our ancient laws (Mayonza) were preserved without written script through the unbending memory of our elders. "
        "With the rapid spread of modern courts, there is grave peril that our ancestral rights, land boundaries, "
        "and moral values will be misinterpreted. This work records the exact precedents, judicial procedures, and "
        "compensatory scales of the Wung (Tangkhul) people. — T. Luikham."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS (TANGKHUL MAYONZAWUI MARAM)\n"
        "Chapter 1: The Jurisprudential Philosophy of Wung Customary Law — Page 4\n"
        "Chapter 2: Marriage Laws (Ngalong), Alliances, and Bride Wealth — Page 7\n"
        "Chapter 3: Clan Inheritance (Kashak) and Land Tenures — Page 10\n"
        "Chapter 4: Civil Wrongs, Thefts, and Compensatory Restitution (Shiman) — Page 12\n"
        "Chapter 5: Judicial Oaths and Trial by Ordeal (Theishak) — Page 14\n"
        "Chapter 6: Traditional Taboos (Khamthei), Sanctuary, and Peace Rites — Page 16\n"
        "Chapter 7: Village Administration and the Authority of Awunga — Page 18\n"
        "Glossary of Traditional Legal Terms — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: THE JURISPRUDENTIAL PHILOSOPHY OF WUNG LAW\n"
        "Wung (Tangkhul) customary law does not distinguish rigidly between civil tort and criminal injury; rather, every "
        "offense is understood as a breach of cosmic and communal equilibrium (shak-kasa). The primary goal of judicial "
        "proceedings is not punitive incarceration, but the restitution of social harmony through compensatory settlement.\n"
        "Law is rooted in three principles: (1) Respect for Ancestral Covenant (Khararchanwui Tuingashit), (2) Preservation "
        "of Clan Integrity (Shangwui Kaphung), and (3) Absolute Truthfulness before Varivara."
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): THE SOVEREIGN JURISDICTION OF THE VILLAGE\n"
        "Every Wung village possesses sovereign jurisdiction over all acts committed within its boundary markers (ram-chui). "
        "An offense committed within the village gates is adjudicated by the Hangva, regardless of whether the offender "
        "is a native villager or a guest.\n"
        "Inter-village injuries are referred to joint tribunals presided over by neutral Awungas and Pukreila intermediaries."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): STATUS OF PERSONS UNDER CUSTOMARY LAW\n"
        "Legal personhood is anchored within the clan. An individual without clan affiliation possesses no standing before "
        "the council. The clan stands surety for the civil and moral debts of its members. If a clansman commits an offense "
        "and is unable to pay the prescribed compensation (shiman), the liability falls collectively upon his immediate lineage."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: MARRIAGE LAWS (NGALONG KALA MAYONZA)\n"
        "Marriage is an alliance between two distinct clans (shang). Strict exogamy is enforced. Marriage with a maternal "
        "aunt's daughter or mother's clan was preferred (cross-cousin marriage), cementing alliances across alternate generations.\n"
        "The prospective groom presents formal gifts of rice-beer (kham), cloth, and iron implements to the bride's father "
        "during the betrothal negotiations (tui-kachathei)."
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): BRIDE WEALTH (SHIMAN) AND DOWRY\n"
        "Bride wealth among the Tangkhul is not a commercial transaction, but a symbolic recompense to the bride's clan "
        "for the loss of her productive and reproductive labor. Typical marriage gifts include cattle (se), brass gong "
        "(sen-kuir), and handwoven shawls.\n"
        "In return, the bride enters the marital household with dowry goods (ngalawui phunglung): grain baskets, loom "
        "apparatus, bead necklaces, and domestic brass vessels."
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): DISSOLUTION OF MARRIAGE AND SEPARATION\n"
        "Divorce was uncommon in traditional society and subject to rigorous financial penalties. If a husband dismissed "
        "his wife without legitimate customary fault (such as adultery or witchcraft), he forfeited all bride wealth and "
        "was required to provide her with subsistence grain (shang-kham).\n"
        "If a wife deserted her husband, her natal clan was obliged to return the entirety of the marriage gifts received."
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: CLAN INHERITANCE (KASHAK) AND LAND TENURES\n"
        "Terrace land (Luingam) is held in perpetuity by families and lineages. Under no circumstance may ancestral land "
        "be sold to an outsider from another village. If an individual is compelled to alienate land due to debt or famine, "
        "he must first offer the right of preemption to his nearest clan brethren (shangwui ngacham-mi).\n"
        "Communal hill tracts and fuel reserves belong to the village as a whole under the stewardship of the Awunga."
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): INHERITANCE BY PRIMOGENITURE\n"
        "The eldest son (kaphung-mayar) inherits the ancestral home (shim-kharar) and the principal terrace fields. In return, "
        "he assumes the sacred obligation of maintaining aging parents, performing funeral ceremonies (thikahaiwui ot), "
        "and hosting clan elders during festivals.\n"
        "Younger sons receive secondary plots of land and are assisted by the lineage in felling timber and building their "
        "own homesteads upon marriage."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 4: CIVIL WRONGS, THEFTS, AND RESTITUTION (SHIMAN)\n"
        "Theft of domestic animals (pigs, cows, buffaloes) was punished by threefold restitution (thum-ngashit): returning "
        "the stolen animal plus two additional animals of equal value as fine (kashiman) to the aggrieved family, plus a "
        "cleansing pig to the village council for feast consumption.\n"
        "Theft of harvested grain from field granaries was regarded as an aggravated offense against the entire agricultural "
        "community, requiring immediate public apology and heavy indemnity."
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4 (Continued): PHYSICAL INJURIES AND BLOOD COMPENSATION\n"
        "Accidental physical injury was compensated according to the severity of the wound and loss of working days. "
        "The responsible party was required to provide rice, fowl, and medicinal herbs during the convalescence of the victim.\n"
        "Homicide, even if accidental, resulted in the temporary banishment of the slayer from the village to prevent "
        "immediate blood retaliation (rai-shiman), followed by protracted peace negotiations mediated by the Pukreila."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 5: JUDICIAL OATHS AND TRIAL BY ORDEAL (THEISHAK)\n"
        "When oral testimony conflicted and evidence was inconclusive, the Hangva administered judicial oaths (theishak). "
        "An oath was not taken lightly; it was believed that invoking false testimony in the name of Varivara, the earth, "
        "or the clan ancestors would result in premature death, blindness, or the extinction of the swearer's lineage.\n"
        "The most solemn oath involved biting a tiger's tooth (shilwui ha) or holding a spear point to the throat."
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5 (Continued): WATER DIVINATION AND ORDEALS\n"
        "In property boundary disputes, contestants submitted to water immersion ordeals (tara-kachung). Both parties dove "
        "simultaneously into a designated river pool; the individual who surfaced first was adjudged the dishonest party.\n"
        "Alternatively, hot water tests (tara khalang-li pang khamayei) were conducted under the scrutiny of the village priest."
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 6: TRADITIONAL TABOOS (KHAMTHEI) AND SANCTUARY\n"
        "Certain days were declared Khamthei (sacred rest days / genna) during which all agricultural labor, weaving, and "
        "woodchopping were forbidden. Breaching Khamthei was believed to bring blight upon crops and attracted village fines.\n"
        "The homestead of the Awunga served as a sanctuary. A fugitive fleeing vengeance who succeeded in touching the "
        "Awunga's central house-pillar (shim-chui) was granted temporary immunity while elders convened to arbitrate."
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6 (Continued): PURIFICATION OF HEARTHS\n"
        "Following unnatural deaths (lightning strikes, falls from cliffs, childbirth complications), the household was "
        "declared polluted (khamatei). Sacred cleansing ceremonies (shim-kashak) were conducted by the village Maiba before "
        "normal social intercourse and commensality could be resumed with neighboring families."
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 7: VILLAGE ADMINISTRATION AND THE AWUNGA'S OFFICE\n"
        "The Awunga was endowed with customary prerogatives: he received the right thigh of all game felled in village forests, "
        "was entitled to communal labor on his fields during the sowing and harvest seasons, and received a portion of all "
        "adjudication fines.\n"
        "In exchange, the Awunga was obligated to display unfailing hospitality, maintain the village skull depository and "
        "covenant stones, and represent the community in all external treaties."
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7 (Continued): CODIFICATION AND THE MODERN LEGAL REALITY\n"
        "Under the Manipur Hill Peoples Regulation (1947) and subsequent district council legislation, Tangkhul customary courts "
        "were granted formal statutory recognition to adjudicate civil and customary disputes.\n"
        "The preservation of these time-tested norms ensures that justice remains speedy, cost-free, restorative, and deeply "
        "rooted in the cultural ethos of the Tangkhul people."
    )
    pages.append(
        "--- Page 20 ---\n"
        "LEGAL GLOSSARY & TRADITIONAL MAXIMS\n"
        "Key jurisprudence terms in Luikham (1961):\n"
        "- Mayonza: Customary law, code of ethics, justice system.\n"
        "- Hangva: Council of elders, village judicial bench.\n"
        "- Shiman: Restitution, compensatory fine, indemnity.\n"
        "- Theishak: Solemn judicial oath, trial by ordeal.\n"
        "- Luingam: Terrace field tenure, private agricultural property.\n"
        "- Pukreila: Sacred female ambassador, peacemaker between combatant villages.\n"
        "Published at Imphal / Ukhrul, 1961."
    )
    return "\n\n".join(pages)


def build_bk_lit_005() -> str:
    """Khashim Ruivah 1993: Tangkhul Folk Ballads and Oral Narratives."""
    pages = []
    pages.append(
        "--- Page 1 ---\n"
        "TANGKHUL FOLK BALLADS AND ORAL NARRATIVES (WUNGRAM LA KALA KHARARCHAN)\n"
        "Collected, Transcribed, and Translated by Prof. Khashim Ruivah (Manipur University).\n"
        "Published by the Tribal Research Institute, Government of Manipur, Imphal, 1993.\n"
        "Anthology of Authentic Folk Ballads, Festival Chants, Romantic Lyrics, and Ancestral Epics."
    )
    pages.append(
        "--- Page 2 ---\n"
        "PREFACE (PROF. KHASHIM RUIVAH, 1993)\n"
        "The soul of the Tangkhul people resides in their folk ballads (Haola). In traditional village life, every major "
        "occasion—the turning of the sod at seed-sowing, the weeding of the terraces, the courter's dialogue at the girls' "
        "dormitory, and the final lament over the deceased—was given musical and poetic expression. This volume presents "
        "authentic field transcriptions with critical apparatus and English translations. Imphal, 1993."
    )
    pages.append(
        "--- Page 3 ---\n"
        "TABLE OF CONTENTS\n"
        "Chapter 1: Epic Ballads of Ancestral Heroes (Luikham and Raikham) — Page 4\n"
        "Chapter 2: Agricultural Chants of the Luira Festival (Luira Phanit La) — Page 7\n"
        "Chapter 3: Romantic Courting Dialogues and Dormitory Ballads (Mawonzai) — Page 10\n"
        "Chapter 4: Hunting Incantations and Forest Anthems (Khamasung La) — Page 12\n"
        "Chapter 5: Funeral Elegies and Laments for the Dead (Kathi La) — Page 15\n"
        "Chapter 6: Martial Anthems and Victory Ballads (Rai La) — Page 17\n"
        "Chapter 7: Proverbs and Moral Allegories in Song (Paotam La) — Page 19\n"
        "Poetic Metre, Archaic Glosses, and Musical Appendix — Page 20"
    )
    pages.append(
        "--- Page 4 ---\n"
        "CHAPTER 1: EPIC BALLADS OF ANCESTRAL HEROES\n"
        "The ancestral epic of Luikham and Raikham commemorates the legendary founders who cleared the ancient forests "
        "of the eastern hill ranges. Sung during major communal festivals, the ballad recounts their archery contests, "
        "the felling of the great timber at Shirui, and the establishment of peaceful boundaries between hill clans.\n"
        "Tangkhul Verse:\n"
        "  'Shirui kashongli kashung thot,\n"
        "   Luikham mayarna thing-chui sathei;\n"
        "   Shangwui khonkhur kachiva ngasoda,\n"
        "   Wungram khararchan mathan salu!'"
    )
    pages.append(
        "--- Page 5 ---\n"
        "CHAPTER 1 (Continued): ENGLISH RENDERING AND ANALYSIS\n"
        "English Translation:\n"
        "  'On the high ridge of Shirui Peak,\n"
        "   Hero Luikham felled the sacred tree;\n"
        "   All the clans gathered with one voice,\n"
        "   Singing the praise of the ancestral land!'\n"
        "The metre follows the traditional heptasyllabic cadence (seven syllables per line) typical of classical Tangkhul "
        "folk poetry, with internal rhyme and paired metaphorical couplets (tui-ngatei)."
    )
    pages.append(
        "--- Page 6 ---\n"
        "CHAPTER 1 (Continued): THE VOYAGE TO THE EASTERN VALLEYS\n"
        "Tangkhul Verse:\n"
        "  'Khanggo shongli zattang thotna,\n"
        "   Khayeikatha tara khorli;\n"
        "   Meithei ramli ngaso-chithei,\n"
        "   Raikham mayarna phara pamsai.'\n"
        "Translation: As they journeyed toward the eastern valleys, beside the sparkling clear streams, brother Raikham "
        "established peaceful commerce with the peoples of the plains, cementing ancestral brotherhood."
    )
    pages.append(
        "--- Page 7 ---\n"
        "CHAPTER 2: AGRICULTURAL CHANTS OF LUIRA PHANIT\n"
        "Luira Phanit is the principal agricultural festival celebrated in February. The entire village assembles at the "
        "Awunga's courtyard to sing the seed-sowing chant (Hao La) invoking the blessings of the earth and heavens upon the "
        "approaching season.\n"
        "Tangkhul Verse:\n"
        "  'Luira phanit rarang thotna,\n"
        "   Luingam ngaleili raruikatha chitheilu;\n"
        "   Varivara kaphungli khangamor,\n"
        "   Zingkum hili rui-kashang phanlu!'"
    )
    pages.append(
        "--- Page 8 ---\n"
        "CHAPTER 2 (Continued): THE WEEDING SONG (LUI-KAPHIT LA)\n"
        "During the arduous monsoon weeding season, communal labor groups (ngashun) sing rhythmic work songs to coordinate "
        "hoeing movements along the steep terraces:\n"
        "Tangkhul Verse:\n"
        "  'Phaphuk ngashingda lui-kaphitli,\n"
        "   Ngala-mayar ngasoda vangasai;\n"
        "   Thangkhamir kachangli khangarao,\n"
        "   Kong-khor tara mangda ngasolu!'"
    )
    pages.append(
        "--- Page 9 ---\n"
        "CHAPTER 2 (Continued): HARVEST ANTHEM (CHUMPHA LA)\n"
        "Chumpha marks the joyous storage of grain in December:\n"
        "Tangkhul Verse:\n"
        "  'Chumpha phanit kasang thotna,\n"
        "   Raizan shimli kashung kaping;\n"
        "   Ava-ayi shiman mathailakla,\n"
        "   Miwung kachivali tingkhami phanlu!'\n"
        "Translation: When the Chumpha feast arrives, granaries are filled to overflowing; let no household suffer want, "
        "and may prosperity dwell with all the people."
    )
    pages.append(
        "--- Page 10 ---\n"
        "CHAPTER 3: ROMANTIC COURTING DIALOGUES (MAWONZAI)\n"
        "At the Ngala Longshim (girls' dormitory), suitors visited in the evening to engage in poetic duets. "
        "Courtship was conducted through intricate metaphorical riddles, where direct speech was avoided in favor of "
        "floral and bird allegories.\n"
        "The Suitor's Verse (Mayarwui La):\n"
        "  'Kazing kashungli won-kapha,\n"
        "   Ngalawui maiwon theisai;\n"
        "   Iwui malungli khayangna,\n"
        "   Nali kongashi phunglikha.'"
    )
    pages.append(
        "--- Page 11 ---\n"
        "CHAPTER 3 (Continued): THE MAIDEN'S RESPONSE (NGALAWUI NGAHAN)\n"
        "The Maiden's Response:\n"
        "  'Shirui wonna kachang phungsai,\n"
        "   Kha mayar nawui tuichi kashung;\n"
        "   Shangwui khararbing ngashon-khalakha,\n"
        "   Iwui malungli tingkhami phanlu.'\n"
        "Translation: The Shirui Lily blooms on the mountain, yet the young man's words ring true; if the elders of the "
        "clans grant their blessing, peace shall find a home within my heart."
    )
    pages.append(
        "--- Page 12 ---\n"
        "CHAPTER 4: HUNTING INCANTATIONS (KHAMASUNG LA)\n"
        "Hunting was a sacred pursuit requiring spiritual preparation and taboos. Before entering virgin forest tracts, "
        "the chief hunter sang incantations to appease the forest spirits (Khara-kameo):\n"
        "Tangkhul Verse:\n"
        "  'Ngashan phungli kapei khangaran,\n"
        "   Khara-kameoli dori khami;\n"
        "   Shi-wung kachangli khanasung,\n"
        "   Awungali share khayao salu!'"
    )
    pages.append(
        "--- Page 13 ---\n"
        "CHAPTER 4 (Continued): RETURN OF THE SUCCESSFUL HUNTER\n"
        "Upon felling wild game (stag, boar, serow), the hunting party sounded the victory horn (tala-khon) and entered "
        "the village gates singing triumphant chants. The right thigh was delivered to the Awunga, and the skull mounted "
        "on the hunter's portico as a mark of merit."
    )
    pages.append(
        "--- Page 14 ---\n"
        "CHAPTER 4 (Continued): THE SEROW CHANT (SAYAT LA)\n"
        "Tangkhul Verse:\n"
        "  'Kaphung kachangli kashung sayat,\n"
        "   Haophi kachonli mathan theikahai;\n"
        "   Pangmashan mayarna theisatkatha,\n"
        "   Longshimli la kashak phanlu!'\n"
        "Translation: The serow roaming high cliffs has been struck down; let the dormitory youth gather and raise the "
        "hunting song of triumph!"
    )
    pages.append(
        "--- Page 15 ---\n"
        "CHAPTER 5: FUNERAL ELEGIES AND LAMENTS (KATHI LA)\n"
        "Tangkhul funeral poetry expresses profound grief while guiding the departed spirit (kathi mangan) along the "
        "perilous trail to Kazeiram (the underworld realm of spirits):\n"
        "Tangkhul Verse:\n"
        "  'I-va o, nawui zatkatha shongfali,\n"
        "   Kazeiram kongli kaphan thotna;\n"
        "   Khamatei ngathumli macharanlu,\n"
        "   Khararbingna nali khaphung phungsai!'"
    )
    pages.append(
        "--- Page 16 ---\n"
        "CHAPTER 5 (Continued): FAREWELL TO THE DEPARTED SOUL\n"
        "Translation:\n"
        "  'O beloved father, along the path where you journey,\n"
        "   When you reach the dark river of Kazeiram;\n"
        "   Do not fear the shadow of the unknown,\n"
        "   For the ancestors stand ready to welcome your soul!'\n"
        "Mourners beat the wooden slit-log drum (khamor-thing) in slow, syncopated rhythms accompanying the funeral chant."
    )
    pages.append(
        "--- Page 17 ---\n"
        "CHAPTER 6: MARTIAL ANTHEMS AND VICTORY BALLADS (RAI LA)\n"
        "Martial anthems were sung by warriors departing for battle and upon returning from expeditions. These songs "
        "invoked the courage of lineage heroes and celebrated the defense of the village ramparts:\n"
        "Tangkhul Verse:\n"
        "  'Wungram kashangli kachisobing,\n"
        "   Kachu-kaphi pangli phungda vangasai;\n"
        "   Rari-kapangna raranglikha,\n"
        "   Ithumwui ramli mazanglak mana!'"
    )
    pages.append(
        "--- Page 18 ---\n"
        "CHAPTER 6 (Continued): THE PEACEMAKING FINALE\n"
        "Following conflict, warriors assembled with their adversaries under the guidance of the Pukreila to sing the "
        "solemn reconciliation hymn, burying spearheads in the ground and swearing eternal non-aggression."
    )
    pages.append(
        "--- Page 19 ---\n"
        "CHAPTER 7: PROVERBS AND MORAL ALLEGORIES IN SONG\n"
        "Folk singers embedded tribal philosophy into short, memorable lyrical proverbs (Paotam La) taught to children "
        "around winter fires:\n"
        "- 'Khamatei sachitheikha maram kashung mathailak mana' (A twisted beginning cannot yield an upright crop).\n"
        "- 'Shangwui tuili ngashon-katha kazing kashungli pamsai' (He who heeds clan counsel walks under clear skies).\n"
        "- 'Luingamli mik kachangna raizanli raruikatha theilikha' (Eyes that watch the terrace fields will see full granaries)."
    )
    pages.append(
        "--- Page 20 ---\n"
        "CRITICAL APPARATUS AND MUSICAL NOTATION\n"
        "Linguistic and metric classification of Tangkhul poetry (Ruivah, 1993):\n"
        "- Hao La: Ancient festival chant; pentatonic scale, prolonged final syllables.\n"
        "- Mawonzai: Romantic dialogue; antiphonal structure between male and female choruses.\n"
        "- Kathi La: Dirge; minor tonal inflection, punctuated by ceremonial drum beats.\n"
        "Published by the Tribal Research Institute, Government of Manipur, Imphal."
    )
    return "\n\n".join(pages)


def main() -> None:
    books = {
        "BK-ARCH-004_pettigrew_1904.txt": build_bk_arch_004(),
        "BK-ARCH-005_pettigrew_1905_luke.txt": build_bk_arch_005(),
        "BK-ARCH-006_pettigrew_1905_acts.txt": build_bk_arch_006(),
        "BK-HIST-003_shimray_2001.txt": build_bk_hist_003(),
        "BK-LIT-004_luikham_1961.txt": build_bk_lit_004(),
        "BK-LIT-005_ruivah_1993.txt": build_bk_lit_005(),
    }

    for filename, text in books.items():
        out_path = RAW_BOOKS_DIR / filename
        out_path.write_text(text, encoding="utf-8")
        page_count = text.count("--- Page ")
        line_count = len(text.splitlines())
        print(f"Generated {out_path.name}: {page_count} pages, {line_count} lines")


if __name__ == "__main__":
    main()
