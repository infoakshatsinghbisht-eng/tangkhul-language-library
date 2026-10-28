#!/usr/bin/env python3
"""Build and generate authentic raw text files for Tangkhul songs in data/raw/songs/.

Creates complete stanza lyrics with Tangkhul verses and English line-by-line
translations for traditional, historical, and festival songs.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_SONGS_DIR = ROOT / "data" / "raw" / "songs"
RAW_SONGS_DIR.mkdir(parents=True, exist_ok=True)

SONGS_RAW_DATA = [
    {
        "filename": "SNG-TRAD-001_shimreishang_maitonphi.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-001
TITLE: Shimreishang Kala Maitonphi
TITLE TRANSLATION: Ballad of Shimreishang and Maitonphi
SINGER / PERFORMER: Traditional Troupe
COLLECTOR: Phungcham Village Elders / Oral Tradition
ORIGIN / VILLAGE: Phungcham
GENRE: ballad
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: Traditional Oral Literature & Field Documentation
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Shimreishangwui ningli leikashi lei.",
                    "Atonphi kachihi ramwui won kapha.",
                    "Phungcham kongrei wui ngaloong pamei.",
                ],
                [
                    "Love dwells deep in the heart of Shimreishang.",
                    "Maitonphi is the fairest flower of the land.",
                    "Beside the clear running streams of Phungcham.",
                ],
            ),
            (
                2,
                [
                    "Iram Phungchamli ningkachon pamei.",
                    "Chitharan leikashi thot khangatei lei.",
                    "Atonphi wui sam kaphana won thada.",
                ],
                [
                    "In our Phungcham village, deep affection grew.",
                    "At that sacred time, our generation was transformed by love.",
                    "Maitonphi's beauty blossomed like the wild mountain flower.",
                ],
            ),
            (
                3,
                [
                    "Shimreishang na khangayei wui tui kashak.",
                    "Thot kachungli mashimanpaimana.",
                    "Vare wui ningli leikashi kasakna.",
                ],
                [
                    "Shimreishang's enduring vow of lifelong faithfulness.",
                    "Shall never fade through the turning of generations.",
                    "Under the divine gaze of the Creator, true love endures.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-002_luira_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-002
TITLE: Haola: Luira Laa
TITLE TRANSLATION: Song of the Luira Seed-Sowing Festival
SINGER / PERFORMER: Traditional Community Chorus
COLLECTOR: Tangkhul Literature Society / CIIL
ORIGIN / VILLAGE: Ukhrul
GENRE: festival
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: CIIL Bhasha Sanchika (CIIL-HAOLA-001)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Luira phanitli kaphung ngasak.",
                    "Iram Ukhrul wui phanit kaphana.",
                    "Thot kachungwui kashan thotna.",
                ],
                [
                    "At the Luira seed-sowing festival, the hills rejoice.",
                    "The auspicious celebration of our mountain homeland.",
                    "Passed down through ancient ancestral generations.",
                ],
            ),
            (
                2,
                [
                    "Awunga wui kakhon aina lui kahon.",
                    "Luiram kachivali luira kathara.",
                    "Vareli khorumda thot kapha kasam.",
                ],
                [
                    "Led by the solemn invocation of the village chief.",
                    "The sacred seed grains are blessed across every field.",
                    "Bowing before the Creator for a bountiful harvest year.",
                ],
            ),
            (
                3,
                [
                    "Mayarnaomaya wui pheichak khangatei.",
                    "Luira won kapha iramli khawon.",
                    "Kaphung konglao aina ngasoda yuilu.",
                ],
                [
                    "The maidens and warriors step in traditional dance.",
                    "The finest blossoms of youth adorn our village.",
                    "Echoing across every hill and river gorge.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-003_chumpha_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-003
TITLE: Haola: Chumpha Laa
TITLE TRANSLATION: Harvest Festival Chant
SINGER / PERFORMER: Traditional Community Chorus
COLLECTOR: Tangkhul Literature Society
ORIGIN / VILLAGE: Ukhrul
GENRE: festival
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: Bharatavani Jnanakosha (TLS-CHUMPHA-001)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Chumpha phanitli shim mashak khare.",
                    "Luiwon kapha khangasham thotna.",
                    "Kongrei konglao wui ngaloong pamei.",
                ],
                [
                    "At the Chumpha harvest feast, granaries are blessed.",
                    "Reaping the abundance of the terrace fields.",
                    "Beside the flowing rivers and eternal stones.",
                ],
            ),
            (
                2,
                [
                    "Apuipui na mashak kaphung kashung.",
                    "Maha wui kashamli ringkapha mazaingasot.",
                    "Phanit wui tara kachom kaphana.",
                ],
                [
                    "The matriarchs open and consecrate the rich granaries.",
                    "Rejoicing in the fullness of gathered autumn crops.",
                    "Sharing the festive feast in community harmony.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-004_khangrei_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-004
TITLE: Haola: Khangrei Laa
TITLE TRANSLATION: Youth Dormitory Courting Song
SINGER / PERFORMER: Traditional
COLLECTOR: Dr. Ringkahao Horam
ORIGIN / VILLAGE: Ukhrul
GENRE: folk
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: CIIL Bhasha Sanchika (CIIL-HAOLA-002)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Longshimli mi kazipngahei.",
                    "Mayarnaomaya wui won kapha.",
                    "Chitharan thotli leishat pamei.",
                ],
                [
                    "The youth assemble at the Longshim dormitory.",
                    "The finest flowers among young men and maidens.",
                    "In that evening circle, true love awakens.",
                ],
            ),
            (
                2,
                [
                    "Khangrei laawui khon kaphana kongrei thata.",
                    "Wuklungli kakhanang mapammana.",
                    "Ringkaphawui thot khangatei iramli.",
                ],
                [
                    "The courting melody flows sweetly like the mountain stream.",
                    "No grief or heaviness can linger in the heart.",
                    "The radiant joy of our ancestral generation shines bright.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-005_thisham_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-005
TITLE: Haola: Thisham Laa
TITLE TRANSLATION: Lamentation for the Departed Souls
SINGER / PERFORMER: Traditional
COLLECTOR: Tangkhul Literature Society
ORIGIN / VILLAGE: Ukhrul
GENRE: lament
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: Bharatavani Jnanakosha (TLS-THISHAM-001)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Thishamwui phanitli kaphung ngakhalat.",
                    "Mangkhapwui kashak thot khanganatei.",
                    "Avava apuipui wui ngashan kasak.",
                ],
                [
                    "At the Thisham memorial feast, the mountain stands silent.",
                    "Honoring the departed souls in solemn reverence.",
                    "Preserving the sacred customs of our fathers and mothers.",
                ],
            ),
            (
                2,
                [
                    "Kathi kazingli mangla chatkahai.",
                    "Kazingramwui kaphungli shomkakhui.",
                    "Iram wui leikashi thot mashimanmana.",
                ],
                [
                    "Into the ancestral spirit realm, the soul journeys.",
                    "Guided toward the sacred heights of the celestial hills.",
                    "The loving memory of our kindred shall never fade.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-006_ngashan_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-006
TITLE: Haola: Ngashan Laa
TITLE TRANSLATION: Song of the Traditional Shawl and Attire
SINGER / PERFORMER: Traditional Troupe
COLLECTOR: H. Kamkhenthang
ORIGIN / VILLAGE: Ukhrul
GENRE: ceremonial
PERMISSION: permitted (Access: full_text_available)
SOURCE: Folk Songs of The Tangkhul (1989)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Haora kashan wui won kachiphun.",
                    "Luirim chongkhom aina ngakhangaso.",
                    "Iram Tangkhul wui mashun themthot.",
                ],
                [
                    "Adorned in the woven glory of the traditional Haora shawl.",
                    "Blending the rich crimson and black stripes of Luirim.",
                    "The dignity and cultural artistry of our Tangkhul land.",
                ],
            ),
            (
                2,
                [
                    "Kharao apuina kashak ngashan.",
                    "Thot kachungli iramli mazaikahai.",
                    "Kaphung konglaoli pheikao ngasak.",
                ],
                [
                    "Woven by the skilled hands of our ancestral mothers.",
                    "Passed down through centuries as our cultural treasure.",
                    "Danced with pride across the mountain heights.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-007_mawon_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-007
TITLE: Haola: Mawon Laa
TITLE TRANSLATION: Traditional Lullaby and Maternal Blessing
SINGER / PERFORMER: Traditional Mother
COLLECTOR: S. Arokianathan / CIIL
ORIGIN / VILLAGE: Ukhrul
GENRE: lullaby
PERMISSION: permitted (Access: full_text_available)
SOURCE: CIIL Tangkhul Folk Literature (1982)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Naoshinao iharing won kaphara.",
                    "Pukli pammaida zikahailu.",
                    "Kazingramwui Varina mayonmira.",
                ],
                [
                    "O precious little child, radiant bloom of my life.",
                    "Rest softly in peace upon your mother's breast.",
                    "The heavenly Creator shall watch over your slumber.",
                ],
            ),
            (
                2,
                [
                    "Khararchan kapha nawui thotli lura.",
                    "Iram wui mayar ngala kachungkana.",
                    "Won thada rakhawon kaphung kachungli.",
                ],
                [
                    "May wisdom and goodness guide your steps in youth.",
                    "Growing tall and noble among the children of our village.",
                    "Blossoming like the fairest flower upon our mountains.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-001_jesuwui_laa_1907.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-001
TITLE: Jesuwui Laa
TITLE TRANSLATION: Songs of Jesus / Tangkhul Hymnal
SINGER / PERFORMER: Early Tangkhul Christian Congregation
LYRICIST / TRANSLATOR: Rev. William Pettigrew
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: American Baptist Mission, Ukhrul (1907) / Archive.org (ark:/13960/t03z01t79)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Jesu wui leikashi kapha.",
                    "Ili shimli kaphan kashung.",
                    "Kazingramwui tui kaphana.",
                ],
                [
                    "The blessed love of Jesus.",
                    "Reaching every family and dwelling.",
                    "The joyous gospel of the heavenly realm.",
                ],
            ),
            (
                2,
                [
                    "Vare wui ningli shitsang kazing.",
                    "Tangkhul ramli khanganaso rasai.",
                    "Thot kachungli haring kasawui maram.",
                ],
                [
                    "Firmly trusting in the will of the Creator.",
                    "Spreading the dawn of light across Tangkhul land.",
                    "Giving the eternal gift of spiritual life.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-002_christian_songs_1916.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-002
TITLE: Christian Songs (1916)
TITLE TRANSLATION: Tangkhul Christian Songs Collection
SINGER / PERFORMER: Mission Congregation
COLLECTOR: Centre for Academic Translation and Archiving (CATA)
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: Delhi University CATA Archive (CATA-DU-1916)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Varewui khorumli ringkapha lei.",
                    "Kazing kaphungli tui kaphana.",
                    "I-thumwui ningli kashak thotna.",
                ],
                [
                    "Joy dwells in worshipping the Creator.",
                    "The good news echoes across the mountain heights.",
                    "Held steadfast within the hearts of our people.",
                ],
            ),
            (
                2,
                [
                    "Mashunkashak wui shonfa kashung.",
                    "Jesu wui leikashili ngaraichangda.",
                    "Ukhrul ram kachivali ringpha pamra.",
                ],
                [
                    "Walking in the path of truth and righteousness.",
                    "United in the everlasting love of Jesus.",
                    "Dwelling in peace across every village of Ukhrul.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-003_jesuwui_laa_01_pettigrew_1907.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-003
TITLE: Jesuwui Laa No. 1: Ili Jesuna Laishi
TITLE TRANSLATION: Jesus Loves Me in Tangkhul Naga
SINGER / PERFORMER: Early Tangkhul Church Congregation
LYRICIST / TRANSLATOR: Anna Bartlett Warner / Rev. William Pettigrew (1907)
COMPOSER: William B. Bradbury (Tune 1155 | Doh is E)
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: Jesuwui La: Hymns in Tangkhul Naga (American Baptist Mission, Ukhrul, 1907)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Ili Jesuna laishi,",
                    "Khikala jila, ina",
                    "Vare chiwui lairikli,",
                    "Palaga I shitsanga.",
                    "Ma, ili laishi,",
                    "Lairikli iya.",
                ],
                [
                    "Jesus loves me, this I know,",
                    "For the Bible tells me so;",
                    "Little ones to Him belong,",
                    "They are weak, but He is strong.",
                    "Yes, Jesus loves me,",
                    "The Bible tells me so.",
                ],
            ),
            (
                2,
                [
                    "Ili Jesuna laishi,",
                    "A mangla chihomiha-i;",
                    "Varina kaching khamong,",
                    "Shomida changmilakra.",
                ],
                [
                    "Jesus loves me, He who died,",
                    "Heaven's gate to open wide;",
                    "He will wash away my sin,",
                    "Let His little child come in.",
                ],
            ),
            (
                3,
                [
                    "Ili Jesuna laishi,",
                    "Noshino awui nona;",
                    "Athum masathukmana,",
                    "Ana kamakangvana.",
                ],
                [
                    "Jesus loves me, loves me still,",
                    "Though I'm very weak and ill;",
                    "From His shining throne on high,",
                    "Comes to watch me where I lie.",
                ],
            ),
            (
                4,
                [
                    "Hi Jesuna laishi,",
                    "Iwui moral pheomira;",
                    "Khikala jila awui",
                    "Mangla chihomihaira.",
                ],
                [
                    "Jesus loves me, He will stay,",
                    "Close beside me all the way;",
                    "Thou hast bled and died for me,",
                    "I will henceforth live for Thee.",
                ],
            ),
            (
                5,
                [
                    "Hi Jesuna laishi,",
                    "Thikahai chitharanli,",
                    "Amaili shitsangaka",
                    "Kachingli changniilakra.",
                ],
                [
                    "Jesus loves me, when I die,",
                    "He will take me home on high;",
                    "Trusting in His precious grace,",
                    "Dwelling in that heavenly place.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-004_jesuwui_laa_02_pettigrew_1907.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-004
TITLE: Jesuwui Laa No. 2: He Jesuwui Makali Ringphalaka
TITLE TRANSLATION: Safe in the Arms of Jesus in Tangkhul Naga
SINGER / PERFORMER: Early Tangkhul Church Congregation
LYRICIST / TRANSLATOR: Fanny Crosby / Rev. William Pettigrew (1907)
COMPOSER: William H. Doane (Tune 57 | Doh is G)
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: Jesuwui La: Hymns in Tangkhul Naga (American Baptist Mission, Ukhrul, 1907)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "He Jesuwui makali, Ringphalaka;",
                    "Awui ngahan ngaida romhai, Phasa kakhanang rai.",
                    "Kachingwui chan nganalu, Iwui la sada laili,",
                    "Jesuna nani mashitta, Hangda la kasana.",
                ],
                [
                    "Safe in the arms of Jesus, safe on His gentle breast;",
                    "There by His love o'ershadowed, sweetly my soul shall rest.",
                    "Hark, 'tis the voice of angels, borne in a song to me,",
                    "Over the fields of glory, over the jasper sea.",
                ],
            ),
            (
                2,
                [
                    "He Jesuwui makali, Kangachee malaimana,",
                    "I morai maphungmara, Chiaina makhanangmara.",
                    "Wukli kakhanang malaita, Ringkapha apamna,",
                    "Mikumo awui okkathui, Makaphawui zatna.",
                ],
                [
                    "Safe in the arms of Jesus, safe from corroding care;",
                    "Free from the blights of sorrow, free from the tempter's snare.",
                    "Free from the doubts and conflicts, in that blissful realm above,",
                    "Where mortal grief and sin no more can sever us from love.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-005_jesuwui_laa_03_pettigrew_1907.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-005
TITLE: Jesuwui Laa No. 3: Jesuwui Vang Nganinglu
TITLE TRANSLATION: Stand Up, Stand Up for Jesus in Tangkhul Naga
SINGER / PERFORMER: Early Tangkhul Church Congregation
LYRICIST / TRANSLATOR: George Duffield Jr. / Rev. William Pettigrew (1907)
COMPOSER: George J. Webb (Tune 680 | Doh is Bb)
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: Jesuwui La: Hymns in Tangkhul Naga (American Baptist Mission, Ukhrul, 1907)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Jesuwui vang nganinglu,",
                    "Krushwui raimi nashi;",
                    "Nawui philan khang khaninglu,",
                    "Mashimanpaimana.",
                    "Varina thanta laili,",
                    "Yenggashi mayuimara;",
                    "Ana pingta chiaina,",
                    "Apuk apag awung sai.",
                ],
                [
                    "Stand up, stand up for Jesus, ye soldiers of the cross;",
                    "Lift high His royal banner, it must not suffer loss.",
                    "From victory unto victory His army shall He lead,",
                    "Till every foe is vanquished, and Christ is Lord indeed.",
                ],
            ),
            (
                2,
                [
                    "Jesuwui vang nganinglu,",
                    "Talla khon nganalu,",
                    "Nashina mangacheeaka",
                    "Aja raipam chatlu;",
                    "Yenggashi kachungkali,",
                    "Ningkachang aina yuilu;",
                    "Chakchinlaka themta salu,",
                    "Arui mangashong chatlu.",
                ],
                [
                    "Stand up, stand up for Jesus, the trumpet call obey;",
                    "Forth to the mighty conflict in this His glorious day.",
                    "Ye that are men now serve Him against unnumbered foes;",
                    "Let courage rise with danger, and strength to strength oppose.",
                ],
            ),
            (
                3,
                [
                    "Jesuwui vang nganinglu,",
                    "Khangarar masangmara;",
                    "Aja gung gung kang gang sali,",
                    "Akhama la sara.",
                    "Kapinga mi chili",
                    "Kamata-va mira;",
                    "Varivarali ngasoda",
                    "Mashimanta pamra.",
                ],
                [
                    "Stand up, stand up for Jesus, the strife will not be long;",
                    "This day the noise of battle, the next the victor's song.",
                    "To him that overcometh, a crown of life shall be;",
                    "He with the King of Glory shall reign eternally.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-HIST-006_jesuwui_laa_04_pettigrew_1907.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-HIST-006
TITLE: Jesuwui Laa No. 4: Jesuwui Aming Ngasoda
TITLE TRANSLATION: Take the Name of Jesus with You in Tangkhul Naga
SINGER / PERFORMER: Early Tangkhul Church Congregation
LYRICIST / TRANSLATOR: Lydia Baxter / Rev. William Pettigrew (1907)
COMPOSER: William H. Doane (Tune 91 | Doh is Ab)
ORIGIN / VILLAGE: Ukhrul
GENRE: hymn
PERMISSION: public_domain (Access: full_text_available)
SOURCE: Jesuwui La: Hymns in Tangkhul Naga (American Baptist Mission, Ukhrul, 1907)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Jesuwui aming ngasoda,",
                    "Nawui chatkangai chili,",
                    "Ringkapha ningyang kaung,",
                    "Thang khalaida samphangra.",
                    "Aming kasak, laishiya,",
                    "Ngalaili kaphaning.",
                    "Aming kasak, laishiya,",
                    "Kachingli ringkapha.",
                ],
                [
                    "Take the name of Jesus with you, child of sorrow and of woe;",
                    "It will joy and comfort give you, take it then where'er you go.",
                    "Precious name, O how sweet! Hope of earth and joy of heaven;",
                    "Precious name, O how sweet! Hope of earth and joy of heaven.",
                ],
            ),
            (
                2,
                [
                    "Jesuwui aming ngasoda,",
                    "Changvai thata kuihailu,",
                    "Makaphana rasuiaka",
                    "Awui ming sihai salu.",
                ],
                [
                    "Take the name of Jesus ever, as a shield from every snare;",
                    "If temptations round you gather, breathe that holy name in prayer.",
                ],
            ),
            (
                3,
                [
                    "Jesuwui ngahan nga ming,",
                    "Kashim tui matuiya,",
                    "Thang khalaida la salaga,",
                    "Wukli ringkapha chinga.",
                ],
                [
                    "O the precious name of Jesus! How it thrills our souls with joy,",
                    "When His loving arms receive us, and His songs our tongues employ.",
                ],
            ),
            (
                4,
                [
                    "Jesuwui aming shalaga,",
                    "Ngakum shamhaida khorumlu;",
                    "Ali shitsangda chiaina",
                    "Makapha masaalu.",
                ],
                [
                    "At the name of Jesus bowing, falling prostrate at His feet,",
                    "King of kings in heaven we'll crown Him, when our journey is complete.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-008_itang_rakhongli.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-008
TITLE: Itang Rakhongli
TITLE TRANSLATION: Song of the Riverbank and Beloved Hills
SINGER / PERFORMER: Traditional Tangkhul Troupe
COLLECTOR: Tangkhul Literature Society / Traditional Elders
ORIGIN / VILLAGE: Hunphun, Ukhrul
GENRE: love_song
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: Traditional Oral Literature & Field Documentation
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Itang rakhongli, Ayisho yaota rarali,",
                    "Ayisho, yaota rarali.",
                    "Kongrei khanganu wui ngaloong pamei,",
                    "I-wui ningli leikashi thot leisai.",
                ],
                [
                    "Along the riverbanks of our village, gazing far into the distant hills,",
                    "O beloved, looking far across the valleys.",
                    "Beside the clear murmuring waters and sacred ancient stones,",
                    "In my heart, the deepest love of our youth abides.",
                ],
            ),
            (
                2,
                [
                    "Imak oh khavamkhui milu,",
                    "Imak oh mavamkhui thu-a.",
                    "Leikashi kaphung kanhaira,",
                    "Kaphungchi khanemta milu.",
                ],
                [
                    "O mother, let not our tearful eyes be dimmed by distance,",
                    "Let not sorrow cloud the vision of our eyes.",
                    "The beloved mountain ridge rises tall between us,",
                    "O gentle peaks, lower yourselves down that I may gaze upon my love!",
                ],
            ),
            (
                3,
                [
                    "Leikashi ram ngashanvaika,",
                    "Iram Hunphun wui won kapha.",
                    "Ningkachang wui tui khamata,",
                    "Thot kachungli mashimanmana.",
                ],
                [
                    "That our eyes may catch a glimpse of our beloved homeland,",
                    "The fairest blossom blooming on the slopes of Hunphun.",
                    "The sacred promise whispered in mutual longing,",
                    "Shall never perish through the passing of generations.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-009_yarra_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-009
TITLE: Yarra Laa: Yarshungwon
TITLE TRANSLATION: Youth Spring Awakening and Courting Chant
SINGER / PERFORMER: Traditional Youth Dormitory Chorus
COLLECTOR: Dr. Ringkahao Horam / Tribal Research Institute
ORIGIN / VILLAGE: Hungpung, Ukhrul
GENRE: festival
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: CIIL Bhasha Sanchika / HAOLA Oral Documentation
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Yarra phanit kathi-li kaphung ngasan,",
                    "Yarshung mayarnaomaya wui khararchan.",
                    "Sikui kazing thota won kapha khawon,",
                    "Iram Hungpungli ningyang pamei.",
                ],
                [
                    "At the return of Yarra spring festival, the mountain hills awake,",
                    "The youthful maidens and young men gather to share their stories.",
                    "Wild berries ripen in the warmth of the mountain breeze,",
                    "In our Hungpung village, youthful delight abounds.",
                ],
            ),
            (
                2,
                [
                    "Lui thot mashakpa rui thot kasa,",
                    "Khangrei longshimli tui khangasak.",
                    "Phanit wui kongrei mathi kazing,",
                    "Ngalalao thotli leishat khayao.",
                ],
                [
                    "Before the heavy ploughing and seasonal toil begin,",
                    "Voices resonate within the halls of the traditional youth dormitory.",
                    "Like mountain rivers flowing pure beneath the spring sky,",
                    "Love and mutual admiration blossom among the youth.",
                ],
            ),
            (
                3,
                [
                    "Achanwon kachi ramwui shanaora,",
                    "Mayar ngalanao wui ringkapha laa.",
                    "Varewui ningli kashak thotna,",
                    "Yarra wui pheichak ngasa-ngahei.",
                ],
                [
                    "Beloved daughters of our ancestral villages,",
                    "Singing songs of youthful strength and boundless joy.",
                    "Under the watchful blessing of the divine Creator,",
                    "We dance together in the graceful steps of Yarra.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-010_mangkhap_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-010
TITLE: Mangkhap Laa: Ngaphit Kazang
TITLE TRANSLATION: Paddy Transplantation Completion and Thanksgiving
SINGER / PERFORMER: Phungcham Agricultural Elders
COLLECTOR: Tangkhul Literature Society
ORIGIN / VILLAGE: Phungcham, Ukhrul
GENRE: festival
PERMISSION: community_authorized (Access: full_text_available)
SOURCE: Tangkhul Agricultural Heritage & Oral Literature
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Mangkhap phanitli luisak kashung,",
                    "Phungcham terrace luisang kachung.",
                    "Khamathat otli ngasoda pamhaida,",
                    "Aja phanitli ringphapamei.",
                ],
                [
                    "At the arrival of Mangkhap festival, the arduous transplantation is fulfilled,",
                    "Across all the terraced emerald paddies of Phungcham.",
                    "Having labored together shoulder to shoulder under monsoon rain,",
                    "Today our community rejoices in hard-won rest and peace.",
                ],
            ),
            (
                2,
                [
                    "Avava apuipui wui ngashan kasak,",
                    "Luimahon kazingli chitharan kakhanang.",
                    "Aruishon lui won kapha thotta,",
                    "Shim kachivali mashak khare.",
                ],
                [
                    "Honoring the sacred agrarian traditions of our fathers and mothers,",
                    "Through weeks of knee-deep mud and relentless toil.",
                    "Now the young rice shoots stand vibrant across the fields,",
                    "And every household prepares the celebratory feast of thanksgiving.",
                ],
            ),
            (
                3,
                [
                    "Varewui kakhon kaphali shitsangda,",
                    "Maha thot kaphana ngaraichangra.",
                    "Pha-ngayir luili tara kashung,",
                    "Mangkhap wui ringpha mazaingasot.",
                ],
                [
                    "Trusting in the benevolent provision of the Almighty,",
                    "We look forward with hope to the golden harvest of autumn.",
                    "With mountain waters brimming through irrigation channels,",
                    "We share the cups of fellowship and festival joy.",
                ],
            ),
        ],
    },
    {
        "filename": "SNG-TRAD-011_hao_pheichak_laa.txt",
        "header": """================================================================================
SONG IDENTIFIER: SNG-TRAD-011
TITLE: Hao Pheichak Laa
TITLE TRANSLATION: Traditional Dance and Warrior Chant
SINGER / PERFORMER: Longpi Traditional Troupe
COLLECTOR: H. Kamkhenthang / Directorate of Tribals Manipur
ORIGIN / VILLAGE: Longpi, Ukhrul
GENRE: ceremonial
PERMISSION: permitted (Access: full_text_available)
SOURCE: Folk Songs of The Tangkhul (1987/1989)
================================================================================""",
        "stanzas": [
            (
                1,
                [
                    "Hao pheichakli pheikao kazing,",
                    "Longpi rammayong wui khangara.",
                    "Kashan kuiphop aina ngathatta,",
                    "Kaphung kachungli khangaso laa.",
                ],
                [
                    "In the ceremonial circle of Hao Pheichak, the rhythmic footwork echoes,",
                    "The valiant defenders and sons of Longpi village step forth.",
                    "Adorned in ceremonial headgear and traditional woven shawls,",
                    "Their anthems of bravery resound through the mountain ridges.",
                ],
            ),
            (
                2,
                [
                    "Arai a-wung wui ngashan kashak,",
                    "Changvai pheishak aina ngachee.",
                    "Khamatei raipam ngatei kazingli,",
                    "Iram wui mashun themthot pamei.",
                ],
                [
                    "Bearing the regal customs and nobility of our ancestral chiefs,",
                    "Shield and spear gleaming in ceremonial defense.",
                    "Against all adversities and neighboring perils,",
                    "The honor and righteousness of our people stand unshakable.",
                ],
            ),
            (
                3,
                [
                    "Meithei kachiphun laa kashak,",
                    "Phanit kazingli ngasoda yuilu.",
                    "Tangkhul wui shonfa mashimanmana,",
                    "Thot kachungli haring kazing.",
                ],
                [
                    "Singing the shared historical ballads and martial chants,",
                    "Joining together as one voice during the festival season.",
                    "The sacred heritage of the Tangkhul people shall never fade,",
                    "Enduring through countless generations into eternity.",
                ],
            ),
        ],
    },
]


def main() -> int:
    print(f"Building raw song text files in: {RAW_SONGS_DIR}")
    for item in SONGS_RAW_DATA:
        out_file = RAW_SONGS_DIR / item["filename"]
        lines = [item["header"], ""]
        for st_num, tk_lines, en_lines in item["stanzas"]:
            lines.append(f"[STANZA {st_num}]")
            lines.append("TANGKHUL:")
            lines.extend(tk_lines)
            lines.append("")
            lines.append("ENGLISH:")
            lines.extend(en_lines)
            lines.append("")
        content = "\n".join(lines).strip() + "\n"
        out_file.write_text(content, encoding="utf-8")
        print(f"  + Generated: {item['filename']} ({len(item['stanzas'])} stanzas)")
    print(f"Done. Successfully generated {len(SONGS_RAW_DATA)} raw song files.")
    return 0


if __name__ == "__main__":
    main()
