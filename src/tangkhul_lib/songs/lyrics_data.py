"""Centralized lyrics repository and bilingual translations for Tangkhul songs.

Provides structured stanzas, Tangkhul poetic verses, and English line glosses
for traditional folk melodies, historical hymns, festival chants, and modern songs.
"""

from __future__ import annotations

from typing import Any

# Comprehensive dictionary mapping song IDs to stanzas with Tangkhul lines and English glosses
SONGS_LYRICS_REGISTRY: dict[str, list[dict[str, Any]]] = {
    # -------------------------------------------------------------------------
    # TRADITIONAL FOLK BALLADS & FESTIVAL SONGS (SNG-TRAD)
    # -------------------------------------------------------------------------
    "SNG-TRAD-001": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Shimreishangwui ningli leikashi lei.",
                "Atonphi kachihi ramwui won kapha.",
                "Phungcham kongrei wui ngaloong pamei.",
            ],
            "lines_translation": [
                "Love dwells deep in the heart of Shimreishang.",
                "Maitonphi is the fairest flower of the land.",
                "Beside the clear running streams of Phungcham.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Iram Phungchamli ningkachon pamei.",
                "Chitharan leikashi thot khangatei lei.",
                "Atonphi wui sam kaphana won thada.",
            ],
            "lines_translation": [
                "In our Phungcham village, deep affection grew.",
                "At that sacred time, our generation was transformed by love.",
                "Maitonphi's beauty blossomed like the wild mountain flower.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Shimreishang na khangayei wui tui kashak.",
                "Thot kachungli mashimanpaimana.",
                "Vare wui ningli leikashi kasakna.",
            ],
            "lines_translation": [
                "Shimreishang's enduring vow of lifelong faithfulness.",
                "Shall never fade through the turning of generations.",
                "Under the divine gaze of the Creator, true love endures.",
            ],
        },
    ],
    "SNG-TRAD-002": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Luira phanitli kaphung ngasak.",
                "Iram Ukhrul wui phanit kaphana.",
                "Thot kachungwui kashan thotna.",
            ],
            "lines_translation": [
                "At the Luira seed-sowing festival, the hills rejoice.",
                "The auspicious celebration of our mountain homeland.",
                "Passed down through ancient ancestral generations.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Awunga wui kakhon aina lui kahon.",
                "Luiram kachivali luira kathara.",
                "Vareli khorumda thot kapha kasam.",
            ],
            "lines_translation": [
                "Led by the solemn invocation of the village chief.",
                "The sacred seed grains are blessed across every field.",
                "Bowing before the Creator for a bountiful harvest year.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Mayarnaomaya wui pheichak khangatei.",
                "Luira won kapha iramli khawon.",
                "Kaphung konglao aina ngasoda yuilu.",
            ],
            "lines_translation": [
                "The maidens and warriors step in traditional dance.",
                "The finest blossoms of youth adorn our village.",
                "Echoing across every hill and river gorge.",
            ],
        },
    ],
    "SNG-TRAD-003": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Chumpha phanitli shim mashak khare.",
                "Luiwon kapha khangasham thotna.",
                "Kongrei konglao wui ngaloong pamei.",
            ],
            "lines_translation": [
                "At the Chumpha harvest feast, granaries are blessed.",
                "Reaping the abundance of the terrace fields.",
                "Beside the flowing rivers and eternal stones.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Apuipui na mashak kaphung kashung.",
                "Maha wui kashamli ringkapha mazaingasot.",
                "Phanit wui tara kachom kaphana.",
            ],
            "lines_translation": [
                "The matriarchs open and consecrate the rich granaries.",
                "Rejoicing in the fullness of gathered autumn crops.",
                "Sharing the festive feast in community harmony.",
            ],
        },
    ],
    "SNG-TRAD-004": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Longshimli mi kazipngahei.",
                "Mayarnaomaya wui won kapha.",
                "Chitharan thotli leishat pamei.",
            ],
            "lines_translation": [
                "The youth assemble at the Longshim dormitory.",
                "The finest flowers among young men and maidens.",
                "In that evening circle, true love awakens.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Khangrei laawui khon kaphana kongrei thata.",
                "Wuklungli kakhanang mapammana.",
                "Ringkaphawui thot khangatei iramli.",
            ],
            "lines_translation": [
                "The courting melody flows sweetly like the mountain stream.",
                "No grief or heaviness can linger in the heart.",
                "The radiant joy of our ancestral generation shines bright.",
            ],
        },
    ],
    "SNG-TRAD-005": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Thishamwui phanitli kaphung ngakhalat.",
                "Mangkhapwui kashak thot khanganatei.",
                "Avava apuipui wui ngashan kasak.",
            ],
            "lines_translation": [
                "At the Thisham memorial feast, the mountain stands silent.",
                "Honoring the departed souls in solemn reverence.",
                "Preserving the sacred customs of our fathers and mothers.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Kathi kazingli mangla chatkahai.",
                "Kazingramwui kaphungli shomkakhui.",
                "Iram wui leikashi thot mashimanmana.",
            ],
            "lines_translation": [
                "Into the ancestral spirit realm, the soul journeys.",
                "Guided toward the sacred heights of the celestial hills.",
                "The loving memory of our kindred shall never fade.",
            ],
        },
    ],
    "SNG-TRAD-006": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Haora kashan wui won kachiphun.",
                "Luirim chongkhom aina ngakhangaso.",
                "Iram Tangkhul wui mashun themthot.",
            ],
            "lines_translation": [
                "Adorned in the woven glory of the traditional Haora shawl.",
                "Blending the rich crimson and black stripes of Luirim.",
                "The dignity and cultural artistry of our Tangkhul land.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Kharao apuina kashak ngashan.",
                "Thot kachungli iramli mazaikahai.",
                "Kaphung konglaoli pheikao ngasak.",
            ],
            "lines_translation": [
                "Woven by the skilled hands of our ancestral mothers.",
                "Passed down through centuries as our cultural treasure.",
                "Danced with pride across the mountain heights.",
            ],
        },
    ],
    "SNG-TRAD-007": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Naoshinao iharing won kaphara.",
                "Pukli pammaida zikahailu.",
                "Kazingramwui Varina mayonmira.",
            ],
            "lines_translation": [
                "O precious little child, radiant bloom of my life.",
                "Rest softly in peace upon your mother's breast.",
                "The heavenly Creator shall watch over your slumber.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Khararchan kapha nawui thotli lura.",
                "Iram wui mayar ngala kachungkana.",
                "Won thada rakhawon kaphung kachungli.",
            ],
            "lines_translation": [
                "May wisdom and goodness guide your steps in youth.",
                "Growing tall and noble among the children of our village.",
                "Blossoming like the fairest flower upon our mountains.",
            ],
        },
    ],
    "SNG-TRAD-008": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Itang rakhongli, Ayisho yaota rarali,",
                "Ayisho, yaota rarali.",
                "Kongrei khanganu wui ngaloong pamei,",
                "I-wui ningli leikashi thot leisai.",
            ],
            "lines_translation": [
                "Along the riverbanks of our village, gazing far into the distant hills,",
                "O beloved, looking far across the valleys.",
                "Beside the clear murmuring waters and sacred ancient stones,",
                "In my heart, the deepest love of our youth abides.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Imak oh khavamkhui milu,",
                "Imak oh mavamkhui thu-a.",
                "Leikashi kaphung kanhaira,",
                "Kaphungchi khanemta milu.",
            ],
            "lines_translation": [
                "O mother, let not our tearful eyes be dimmed by distance,",
                "Let not sorrow cloud the vision of our eyes.",
                "The beloved mountain ridge rises tall between us,",
                "O gentle peaks, lower yourselves down that I may gaze upon my love!",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Leikashi ram ngashanvaika,",
                "Iram Hunphun wui won kapha.",
                "Ningkachang wui tui khamata,",
                "Thot kachungli mashimanmana.",
            ],
            "lines_translation": [
                "That our eyes may catch a glimpse of our beloved homeland,",
                "The fairest blossom blooming on the slopes of Hunphun.",
                "The sacred promise whispered in mutual longing,",
                "Shall never perish through the passing of generations.",
            ],
        },
    ],
    "SNG-TRAD-009": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Yarra phanit kathi-li kaphung ngasan,",
                "Yarshung mayarnaomaya wui khararchan.",
                "Sikui kazing thota won kapha khawon,",
                "Iram Hungpungli ningyang pamei.",
            ],
            "lines_translation": [
                "At the return of Yarra spring festival, the mountain hills awake,",
                "The youthful maidens and young men gather to share their stories.",
                "Wild berries ripen in the warmth of the mountain breeze,",
                "In our Hungpung village, youthful delight abounds.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Lui thot mashakpa rui thot kasa,",
                "Khangrei longshimli tui khangasak.",
                "Phanit wui kongrei mathi kazing,",
                "Ngalalao thotli leishat khayao.",
            ],
            "lines_translation": [
                "Before the heavy ploughing and seasonal toil begin,",
                "Voices resonate within the halls of the traditional youth dormitory.",
                "Like mountain rivers flowing pure beneath the spring sky,",
                "Love and mutual admiration blossom among the youth.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Achanwon kachi ramwui shanaora,",
                "Mayar ngalanao wui ringkapha laa.",
                "Varewui ningli kashak thotna,",
                "Yarra wui pheichak ngasa-ngahei.",
            ],
            "lines_translation": [
                "Beloved daughters of our ancestral villages,",
                "Singing songs of youthful strength and boundless joy.",
                "Under the watchful blessing of the divine Creator,",
                "We dance together in the graceful steps of Yarra.",
            ],
        },
    ],
    "SNG-TRAD-010": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Mangkhap phanitli luisak kashung,",
                "Phungcham terrace luisang kachung.",
                "Khamathat otli ngasoda pamhaida,",
                "Aja phanitli ringphapamei.",
            ],
            "lines_translation": [
                "At the arrival of Mangkhap festival, the arduous transplantation is fulfilled,",
                "Across all the terraced emerald paddies of Phungcham.",
                "Having labored together shoulder to shoulder under monsoon rain,",
                "Today our community rejoices in hard-won rest and peace.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Avava apuipui wui ngashan kasak,",
                "Luimahon kazingli chitharan kakhanang.",
                "Aruishon lui won kapha thotta,",
                "Shim kachivali mashak khare.",
            ],
            "lines_translation": [
                "Honoring the sacred agrarian traditions of our fathers and mothers,",
                "Through weeks of knee-deep mud and relentless toil.",
                "Now the young rice shoots stand vibrant across the fields,",
                "And every household prepares the celebratory feast of thanksgiving.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Varewui kakhon kaphali shitsangda,",
                "Maha thot kaphana ngaraichangra.",
                "Pha-ngayir luili tara kashung,",
                "Mangkhap wui ringpha mazaingasot.",
            ],
            "lines_translation": [
                "Trusting in the benevolent provision of the Almighty,",
                "We look forward with hope to the golden harvest of autumn.",
                "With mountain waters brimming through irrigation channels,",
                "We share the cups of fellowship and festival joy.",
            ],
        },
    ],
    "SNG-TRAD-011": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Hao pheichakli pheikao kazing,",
                "Longpi rammayong wui khangara.",
                "Kashan kuiphop aina ngathatta,",
                "Kaphung kachungli khangaso laa.",
            ],
            "lines_translation": [
                "In the ceremonial circle of Hao Pheichak, the rhythmic footwork echoes,",
                "The valiant defenders and sons of Longpi village step forth.",
                "Adorned in ceremonial headgear and traditional woven shawls,",
                "Their anthems of bravery resound through the mountain ridges.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Arai a-wung wui ngashan kashak,",
                "Changvai pheishak aina ngachee.",
                "Khamatei raipam ngatei kazingli,",
                "Iram wui mashun themthot pamei.",
            ],
            "lines_translation": [
                "Bearing the regal customs and nobility of our ancestral chiefs,",
                "Shield and spear gleaming in ceremonial defense.",
                "Against all adversities and neighboring perils,",
                "The honor and righteousness of our people stand unshakable.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Meithei kachiphun laa kashak,",
                "Phanit kazingli ngasoda yuilu.",
                "Tangkhul wui shonfa mashimanmana,",
                "Thot kachungli haring kazing.",
            ],
            "lines_translation": [
                "Singing the shared historical ballads and martial chants,",
                "Joining together as one voice during the festival season.",
                "The sacred heritage of the Tangkhul people shall never fade,",
                "Enduring through countless generations into eternity.",
            ],
        },
    ],

    # -------------------------------------------------------------------------
    # HISTORICAL HYMNS & SCRIPTURAL SONGS (SNG-HIST)
    # -------------------------------------------------------------------------
    "SNG-HIST-001": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesu wui leikashi kapha.",
                "Ili shimli kaphan kashung.",
                "Kazingramwui tui kaphana.",
            ],
            "lines_translation": [
                "The blessed love of Jesus.",
                "Reaching every family and dwelling.",
                "The joyous gospel of the heavenly realm.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Vare wui ningli shitsang kazing.",
                "Tangkhul ramli khanganaso rasai.",
                "Thot kachungli haring kasawui maram.",
            ],
            "lines_translation": [
                "Firmly trusting in the will of the Creator.",
                "Spreading the dawn of light across Tangkhul land.",
                "Giving the eternal gift of spiritual life.",
            ],
        },
    ],
    "SNG-HIST-002": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Varewui khorumli ringkapha lei.",
                "Kazing kaphungli tui kaphana.",
                "I-thumwui ningli kashak thotna.",
            ],
            "lines_translation": [
                "Joy dwells in worshipping the Creator.",
                "The good news echoes across the mountain heights.",
                "Held steadfast within the hearts of our people.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Mashunkashak wui shonfa kashung.",
                "Jesu wui leikashili ngaraichangda.",
                "Ukhrul ram kachivali ringpha pamra.",
            ],
            "lines_translation": [
                "Walking in the path of truth and righteousness.",
                "United in the everlasting love of Jesus.",
                "Dwelling in peace across every village of Ukhrul.",
            ],
        },
    ],
    "SNG-HIST-003": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ili Jesuna laishi,",
                "Khikala jila, ina",
                "Vare chiwui lairikli,",
                "Palaga I shitsanga.",
                "Ma, ili laishi,",
                "Lairikli iya.",
            ],
            "lines_translation": [
                "Jesus loves me, this I know,",
                "For the Bible tells me so;",
                "Little ones to Him belong,",
                "They are weak, but He is strong.",
                "Yes, Jesus loves me,",
                "The Bible tells me so.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Ili Jesuna laishi,",
                "A mangla chihomiha-i;",
                "Varina kaching khamong,",
                "Shomida changmilakra.",
            ],
            "lines_translation": [
                "Jesus loves me, He who died,",
                "Heaven's gate to open wide;",
                "He will wash away my sin,",
                "Let His little child come in.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Ili Jesuna laishi,",
                "Noshino awui nona;",
                "Athum masathukmana,",
                "Ana kamakangvana.",
            ],
            "lines_translation": [
                "Jesus loves me, loves me still,",
                "Though I'm very weak and ill;",
                "From His shining throne on high,",
                "Comes to watch me where I lie.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Hi Jesuna laishi,",
                "Iwui moral pheomira;",
                "Khikala jila awui",
                "Mangla chihomihaira.",
            ],
            "lines_translation": [
                "Jesus loves me, He will stay,",
                "Close beside me all the way;",
                "Thou hast bled and died for me,",
                "I will henceforth live for Thee.",
            ],
        },
        {
            "stanza_number": 5,
            "lines_tangkhul": [
                "Hi Jesuna laishi,",
                "Thikahai chitharanli,",
                "Amaili shitsangaka",
                "Kachingli changniilakra.",
            ],
            "lines_translation": [
                "Jesus loves me, when I die,",
                "He will take me home on high;",
                "Trusting in His precious grace,",
                "Dwelling in that heavenly place.",
            ],
        },
    ],
    "SNG-HIST-004": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "He Jesuwui makali, Ringphalaka;",
                "Awui ngahan ngaida romhai, Phasa kakhanang rai.",
                "Kachingwui chan nganalu, Iwui la sada laili,",
                "Jesuna nani mashitta, Hangda la kasana.",
            ],
            "lines_translation": [
                "Safe in the arms of Jesus, safe on His gentle breast;",
                "There by His love o'ershadowed, sweetly my soul shall rest.",
                "Hark, 'tis the voice of angels, borne in a song to me,",
                "Over the fields of glory, over the jasper sea.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "He Jesuwui makali, Kangachee malaimana,",
                "I morai maphungmara, Chiaina makhanangmara.",
                "Wukli kakhanang malaita, Ringkapha apamna,",
                "Mikumo awui okkathui, Makaphawui zatna.",
            ],
            "lines_translation": [
                "Safe in the arms of Jesus, safe from corroding care;",
                "Free from the blights of sorrow, free from the tempter's snare.",
                "Free from the doubts and conflicts, in that blissful realm above,",
                "Where mortal grief and sin no more can sever us from love.",
            ],
        },
    ],
    "SNG-HIST-005": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesuwui vang nganinglu,",
                "Krushwui raimi nashi;",
                "Nawui philan khang khaninglu,",
                "Mashimanpaimana.",
                "Varina thanta laili,",
                "Yenggashi mayuimara;",
                "Ana pingta chiaina,",
                "Apuk apag awung sai.",
            ],
            "lines_translation": [
                "Stand up, stand up for Jesus, ye soldiers of the cross;",
                "Lift high His royal banner, it must not suffer loss.",
                "From victory unto victory His army shall He lead,",
                "Till every foe is vanquished, and Christ is Lord indeed.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Jesuwui vang nganinglu,",
                "Talla khon nganalu,",
                "Nashina mangacheeaka",
                "Aja raipam chatlu;",
                "Yenggashi kachungkali,",
                "Ningkachang aina yuilu;",
                "Chakchinlaka themta salu,",
                "Arui mangashong chatlu.",
            ],
            "lines_translation": [
                "Stand up, stand up for Jesus, the trumpet call obey;",
                "Forth to the mighty conflict in this His glorious day.",
                "Ye that are men now serve Him against unnumbered foes;",
                "Let courage rise with danger, and strength to strength oppose.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Jesuwui vang nganinglu,",
                "Khangarar masangmara;",
                "Aja gung gung kang gang sali,",
                "Akhama la sara.",
                "Kapinga mi chili",
                "Kamata-va mira;",
                "Varivarali ngasoda",
                "Mashimanta pamra.",
            ],
            "lines_translation": [
                "Stand up, stand up for Jesus, the strife will not be long;",
                "This day the noise of battle, the next the victor's song.",
                "To him that overcometh, a crown of life shall be;",
                "He with the King of Glory shall reign eternally.",
            ],
        },
    ],
    "SNG-HIST-006": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesuwui aming ngasoda,",
                "Nawui chatkangai chili,",
                "Ringkapha ningyang kaung,",
                "Thang khalaida samphangra.",
                "Aming kasak, laishiya,",
                "Ngalaili kaphaning.",
                "Aming kasak, laishiya,",
                "Kachingli ringkapha.",
            ],
            "lines_translation": [
                "Take the name of Jesus with you, child of sorrow and of woe;",
                "It will joy and comfort give you, take it then where'er you go.",
                "Precious name, O how sweet! Hope of earth and joy of heaven;",
                "Precious name, O how sweet! Hope of earth and joy of heaven.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Jesuwui aming ngasoda,",
                "Changvai thata kuihailu,",
                "Makaphana rasuiaka",
                "Awui ming sihai salu.",
            ],
            "lines_translation": [
                "Take the name of Jesus ever, as a shield from every snare;",
                "If temptations round you gather, breathe that holy name in prayer.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Jesuwui ngahan nga ming,",
                "Kashim tui matuiya,",
                "Thang khalaida la salaga,",
                "Wukli ringkapha chinga.",
            ],
            "lines_translation": [
                "O the precious name of Jesus! How it thrills our souls with joy,",
                "When His loving arms receive us, and His songs our tongues employ.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Jesuwui aming shalaga,",
                "Ngakum shamhaida khorumlu;",
                "Ali shitsangda chiaina",
                "Makapha masaalu.",
            ],
            "lines_translation": [
                "At the name of Jesus bowing, falling prostrate at His feet,",
                "King of kings in heaven we'll crown Him, when our journey is complete.",
            ],
        },
    ],
    "SNG-HIST-007": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesu nawui ming phaningda",
                "Iwukli laikashi;",
                "Kala nachak thaiaka",
                "Kamataida laishi.",
            ],
            "lines_translation": [
                "Jesus, the very thought of Thee",
                "With sweetness fills my breast;",
                "But sweeter far Thy face to see,",
                "And in Thy presence rest.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Nawui mingli kapha akhon,",
                "Katai malaimana;",
                "Shalaga ningkachanglakai,",
                "Phaning kavai malai.",
            ],
            "lines_translation": [
                "Nor voice can sing, nor heart can frame,",
                "Nor can the memory find",
                "A sweeter sound than Thy blest name,",
                "O Savior of mankind!",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Malung kanimwui kaphaning,",
                "Vahongnowui kamana;",
                "Moral kasali laikashi,",
                "He Jesu! namangna.",
            ],
            "lines_translation": [
                "O hope of every contrite heart,",
                "O joy of all the meek,",
                "To those who fall, how kind Thou art!",
                "How good to those who seek!",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Nali samkaphanga mi chi,",
                "Ringkapha samphanga;",
                "Na kathata laishikala,",
                "Nawui laikashi thai.",
            ],
            "lines_translation": [
                "But what to those who find? Ah, this",
                "Nor tongue nor pen can show;",
                "The love of Jesus, what it is,",
                "None but His loved ones know.",
            ],
        },
        {
            "stanza_number": 5,
            "lines_tangkhul": [
                "Arui Jesu naming thaida,",
                "Noda nachak thaira;",
                "Jesula ithumwui mina,",
                "Chiaina kapha sara.",
            ],
            "lines_translation": [
                "Jesus, our only joy be Thou,",
                "As Thou our prize wilt be;",
                "Jesus, be Thou our glory now,",
                "And through eternity.",
            ],
        },
    ],
    "SNG-HIST-008": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesuwui krushwui pamli",
                "Ina nganing ngaiya;",
                "Khikala jila chili",
                "Khaya thata laiya.",
                "Khaya chili pamchinglaka,",
                "Chinghamli makachat thai;",
                "Ot phungla makaphung thaiya,",
                "Chiaina ringphaya.",
            ],
            "lines_translation": [
                "Beneath the cross of Jesus",
                "I fain would take my stand,",
                "The shadow of a mighty rock",
                "Within a weary land;",
                "A home within the wilderness,",
                "A rest upon the way,",
                "From the burning of the noontide heat,",
                "And the burden of the day.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Yamsang kava chipamli",
                "Ithum pamchingaka;",
                "Mashunglak aina samida,",
                "Laishila laishira.",
                "Ishamaiwui krush chili",
                "Shairon katatana;",
                "Shairon chili yakkalaga",
                "Kachingli changpaira.",
            ],
            "lines_translation": [
                "Upon that cross of Jesus",
                "Mine eye at times can see",
                "The very dying form of One",
                "Who suffered there for me;",
                "And from my smitten heart with tears",
                "Two wonders I confess:",
                "The wonders of redeeming love",
                "And all my unworthiness.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Krushwui khanuk aparali",
                "Chikhur kathala lai,",
                "Chili kathukla thuklaka,",
                "Tangmangla tangmanga.",
                "Mata kachang vang aina",
                "Ithumli kanmiya;",
                "Jesuna pangthai katingda,",
                "Angachaili pamda lai.",
            ],
            "lines_translation": [
                "I take, O cross, thy shadow",
                "For my abiding place;",
                "I ask no other sunshine than",
                "The sunshine of His face;",
                "Content to let the world go by,",
                "To know no gain nor loss,",
                "My sinful self my only shame,",
                "My glory all the cross.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Krush chiwui atungli",
                "Jesu kathi mikna thai;",
                "Iwui vang aina Ishamai",
                "Kkanang mataimiya.",
                "Iwukli hi phaningungda",
                "Matak khak kahai khani thai,",
                "Ishamaiwui lukamashen,",
                "Hi makapha chi thai.",
            ],
            "lines_translation": [
                "O Christ, who bore the bitter agony",
                "Upon the shameful tree,",
                "To pay the debt of all my sins",
                "And set my spirit free;",
                "Bearing the sorrows of the world",
                "That we may live in light,",
                "Lord, in Thy grace let me abide,",
                "Made holy in Thy sight.",
            ],
        },
    ],
    "SNG-HIST-009": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Arui chimik tunra,",
                "Ngayakijura,",
                "Kachingram atungli",
                "Mamachahora.",
            ],
            "lines_translation": [
                "Now the day is over,",
                "Night is drawing nigh;",
                "Shadows of the evening",
                "Steal across the sky.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Arui tangmanghowa,",
                "Sirala shokra,",
                "Vano, sa, awonla,",
                "Piyukijura.",
            ],
            "lines_translation": [
                "Now the darkness gathers,",
                "Stars begin to peep;",
                "Birds and beasts and flowers",
                "Soon will be asleep.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Jesu kakhanangli,",
                "Laishiri aina,",
                "Pi ngasak miluda,",
                "Kharai ngasaklu.",
            ],
            "lines_translation": [
                "Jesus, give the weary",
                "Calm and sweet repose;",
                "With Thy tenderest blessing",
                "May our eyelids close.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Noshino mangshongli",
                "Nali thairanu;",
                "Makapha kasali",
                "Lumashenrailu.",
            ],
            "lines_translation": [
                "Grant to little children",
                "Visions bright of Thee;",
                "Guard the wandering travelers",
                "And shelter them with peace.",
            ],
        },
        {
            "stanza_number": 5,
            "lines_tangkhul": [
                "Ngaya sailung hili",
                "Ishamaiwui rao,",
                "Iwui pet ngalemli",
                "Kamayonmilu.",
            ],
            "lines_translation": [
                "Through the long night watches",
                "May Thine angels spread",
                "Their white wings above me,",
                "Watching round my bed.",
            ],
        },
        {
            "stanza_number": 6,
            "lines_tangkhul": [
                "Kaching kahor aina",
                "I angkar thuida,",
                "Nali kamataida",
                "Otram ngathara.",
            ],
            "lines_translation": [
                "When the morning wakens,",
                "Then may I arise",
                "Pure, and fresh, and sinless",
                "In Thy holy eyes.",
            ],
        },
        {
            "stanza_number": 7,
            "lines_tangkhul": [
                "Varivara aina",
                "Ano Jesula,",
                "Mangla katharala,",
                "Masot chikatsa.",
            ],
            "lines_translation": [
                "Glory to the Father,",
                "Glory to the Son,",
                "And to Thee, blest Spirit,",
                "Whilst all ages run.",
            ],
        },
    ],
    "SNG-HIST-010": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesuwui mi chatsa,",
                "Rai ngarargida;",
                "Amaina rituwa,",
                "Ithumla pingsa.",
                "Jesu akavana,",
                "Ithumli thana;",
                "Chiaina pinglakta,",
                "Ngararda yuisa.",
            ],
            "lines_translation": [
                "Onward, Christian soldiers,",
                "Marching as to war,",
                "With the cross of Jesus",
                "Going on before.",
                "Christ the royal Master,",
                "Leads against the foe;",
                "Forward into battle",
                "See His banners go!",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Jesuwui ming shada,",
                "Chipeena ngachee;",
                "Arola yamthuida",
                "Ithumna yuira.",
                "Ithum kavao aina",
                "Ngalai chingshong chi,",
                "Miwui shim chithata",
                "Shimanhorali.",
            ],
            "lines_translation": [
                "At the sign of triumph",
                "Satan's host doth flee;",
                "On then, Christian soldiers,",
                "On to victory!",
                "Hell's foundations quiver",
                "At the shout of praise;",
                "Brothers, lift your voices,",
                "Loud your anthems raise!",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Jesuwui miyurna",
                "Mi kakazip thai;",
                "Kakharar malaima,",
                "Ning kangarum thai.",
                "Chipeena yuigida",
                "Ning ngapailu ji,",
                "Ka ning ngarumaka",
                "Mayuirarmara.",
            ],
            "lines_translation": [
                "Like a mighty army",
                "Moves the Church of God;",
                "Brothers, we are treading",
                "Where the saints have trod.",
                "We are not divided,",
                "All one body we,",
                "One in hope and doctrine,",
                "One in charity.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Awung aina ngalai",
                "Shimanhaila pai,",
                "Ka Jesuwui miyur",
                "Kashiman mavai.",
                "Amai tui nganada,",
                "Kapha sachingra;",
                "Awui yurli changda",
                "Kachingli kara.",
            ],
            "lines_translation": [
                "Crowns and thrones may perish,",
                "Kingdoms rise and wane,",
                "But the Church of Jesus",
                "Constant will remain.",
                "Gates of hell can never",
                "'Gainst that Church prevail;",
                "We have Christ's own promise,",
                "And that cannot fail.",
            ],
        },
        {
            "stanza_number": 5,
            "lines_tangkhul": [
                "Chiaina achangsa,",
                "Awui yur kaphai;",
                "Ithum aina nathum",
                "La sa ngaroksa.",
                "Ithum akavali,",
                "Masot chikatsa;",
                "A awor sathaida",
                "Makaphali yui.",
            ],
            "lines_translation": [
                "Onward then, ye people,",
                "Join our happy throng,",
                "Blend with ours your voices",
                "In the triumph song.",
                "Glory, laud, and honor",
                "Unto Christ the King,",
                "This through countless ages",
                "Men and angels sing.",
            ],
        },
    ],
    "SNG-HIST-011": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ringkapha tui Jesu Amai!",
                "Arui ithumli laishida lai;",
                "Kahui samida ithum mahaira,",
                "Mangla kathara wukli changra.",
                "Chan hi iwaina, la hi phamei,",
                "Jesu amangli sochikatsa.",
            ],
            "lines_translation": [
                "Blessed assurance, Jesus is mine!",
                "Oh, what a foretaste of glory divine!",
                "Heir of salvation, purchase of God,",
                "Born of His Spirit, washed in His blood.",
                "This is my story, this is my song,",
                "Praising my Savior all the day long.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Ali shitsangda ringphamaithui,",
                "Hili ringshilala noda thaikui.",
                "Kachingli kada kachama malai,",
                "Makhanangmada ringphamang lai.",
            ],
            "lines_translation": [
                "Perfect submission, perfect delight,",
                "Visions of rapture now burst on my sight;",
                "Angels, descending, bring from above",
                "Echoes of mercy, whispers of love.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Tui hi nganada kameo horhaisa,",
                "Vari raimaida, ali changthasa.",
                "Miwui vang aina thimaloda,",
                "Ali shitsangda ya jilakra.",
            ],
            "lines_translation": [
                "Perfect submission, all is at rest,",
                "I in my Savior am happy and blest,",
                "Watching and waiting, looking above,",
                "Filled with His goodness, lost in His love.",
            ],
        },
    ],
    "SNG-HIST-012": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Arui ngayali ili ngachonlu,",
                "Tangmangtinghoda machihoalu.",
                "Kataina mangachonlala Amai,",
                "Nana ngachonrada, ithumna thai.",
            ],
            "lines_translation": [
                "Abide with me, fast falls the eventide;",
                "The darkness deepens, Lord, with me abide.",
                "When other helpers fail and comforts flee,",
                "Help of the helpless, oh, abide with me.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Okkathui hi kashanaka pamli,",
                "Ringkapha teoda thakta shimanli.",
                "Mikumo pamli kashiman mang lai,",
                "Na makashiman ishachaina.",
            ],
            "lines_translation": [
                "Swift to its close ebbs out life's little day;",
                "Earth's joys grow dim, its glories pass away;",
                "Change and decay in all around I see;",
                "O Thou who changest not, abide with me.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Kharargida ili maraahi,",
                "Lumashenda ili kharamihi;",
                "Kakhanang thaida laishimaikapa,",
                "Ishamai nana phamaikaplaka.",
            ],
            "lines_translation": [
                "Not a brief glance I beg, a passing word,",
                "But as Thou dwell'st with Thy disciples, Lord,",
                "Familiar, condescending, patient, free.",
                "Come not to sojourn, but abide with me.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Minute kachida ngachon phalungra,",
                "Chipeena ili yuipaishinada;",
                "Ringkashi pamli ringkaphahla;",
                "Jesu namang ithumli huishapa.",
            ],
            "lines_translation": [
                "I need Thy presence every passing hour;",
                "What but Thy grace can foil the tempter's power?",
                "Who like Thyself my guide and stay can be?",
                "Through cloud and sunshine, Lord, abide with me.",
            ],
        },
        {
            "stanza_number": 5,
            "lines_tangkhul": [
                "Hi ngasoda laichinghaiaka,",
                "Yenggashibingli ina yuishapra.",
                "Kathila raok kangachee malai,",
                "Kachingli nali thaira Ishamai.",
            ],
            "lines_translation": [
                "I fear no foe, with Thee at hand to bless;",
                "Ills have no weight, and tears no bitterness.",
                "Where is death's sting? Where, grave, thy victory?",
                "I triumph still, if Thou abide with me.",
            ],
        },
        {
            "stanza_number": 6,
            "lines_tangkhul": [
                "Ina piki kachiurana,",
                "Iwui ngalemli pamda mayonra.",
                "Kahor khara aina angkar thuida,",
                "Einda thihaila Amaina huira.",
            ],
            "lines_translation": [
                "Hold Thou Thy cross before my closing eyes;",
                "Shine through the gloom and point me to the skies.",
                "Heaven's morning breaks, and earth's vain shadows flee;",
                "In life, in death, O Lord, abide with me.",
            ],
        },
    ],
    "SNG-HIST-013": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Jesuna ili laishi,",
                "Nawui ngalemli pamga.",
                "Kangachee chitharanli,",
                "Ili huimilu ara.",
                "Ina mathairanglaka,",
                "Nawui pangli laichingga,",
                "Chiaina iwui mangla,",
                "Mashimanpailakmara.",
            ],
            "lines_translation": [
                "Jesus, Lover of my soul,",
                "Let me to Thy bosom fly,",
                "While the nearer waters roll,",
                "While the tempest still is high.",
                "Hide me, O my Savior, hide,",
                "Till the storm of life is past;",
                "Safe into the haven guide,",
                "Oh, receive my soul at last.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Hui kashapa namanga,",
                "Kangataili changshara.",
                "Ili machihoalu,",
                "Kamayonla mayonlu.",
                "Namangli shitsangrali,",
                "Namangna ngachon kami,",
                "Chiaina ili yengda,",
                "Kakhanang raichomira.",
            ],
            "lines_translation": [
                "Other refuge have I none,",
                "Hangs my helpless soul on Thee;",
                "Leave, ah! leave me not alone,",
                "Still support and comfort me.",
                "All my trust on Thee is stayed,",
                "All my help from Thee I bring;",
                "Cover my defenseless head",
                "With the shadow of Thy wing.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Jesuna lan kathana,",
                "Ina kuikangai chili",
                "Nana mirada kapha,",
                "Chiaina sochingrali.",
                "Kagazali raikami,",
                "Kangapeoli thai kami,",
                "Ina moral phungda lai,",
                "Na kathar mang sai, Amai.",
            ],
            "lines_translation": [
                "Thou, O Christ, art all I want;",
                "More than all in Thee I find:",
                "Raise the fallen, cheer the faint,",
                "Heal the sick, and lead the blind.",
                "Just and holy is Thy name,",
                "I am all unrighteousness;",
                "False and full of sin I am;",
                "Thou art full of truth and grace.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Lumashenda laishida,",
                "Moraili pheomisara.",
                "Kapha ari mimungda,",
                "Phasa thar kavai saiya.",
                "Manglawui rakhonglaka,",
                "Mungkangaila mungngaiya,",
                "Iwui wukli pamchingda,",
                "Noda nashili kara.",
            ],
            "lines_translation": [
                "Plenteous grace with Thee is found,",
                "Grace to cover all my sin;",
                "Let the healing streams abound,",
                "Make and keep me pure within.",
                "Thou of life the fountain art,",
                "Freely let me take of Thee;",
                "Spring Thou up within my heart,",
                "Rise to all eternity.",
            ],
        },
    ],
    "SNG-HIST-014": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Makashiman lungkhuri,",
                "Ina nali thumhaiga;",
                "Na phasali runghoda,",
                "Ashi shok kahai chili,",
                "Chiaina iwui moral,",
                "Pheomida kahui Amai.",
            ],
            "lines_translation": [
                "Rock of Ages, cleft for me,",
                "Let me hide myself in Thee;",
                "Let the water and the blood,",
                "From Thy riven side which flowed,",
                "Be of sin the double cure,",
                "Cleanse me from its guilt and power.",
            ],
        },
        {
            "stanza_number": 2,
            "lines_tangkhul": [
                "Nawui ningkami chili,",
                "Sarada mararmana.",
                "Ot sachinglala Amai,",
                "Kachapla chapchinglala,",
                "Iwui moral pheokavai,",
                "Namangna pheoshaplakra.",
            ],
            "lines_translation": [
                "Not the labors of my hands",
                "Can fulfill Thy law's demands;",
                "Could my zeal no respite know,",
                "Could my tears forever flow,",
                "All for sin could not atone;",
                "Thou must save, and Thou alone.",
            ],
        },
        {
            "stanza_number": 3,
            "lines_tangkhul": [
                "Ipangli khika masing,",
                "Krush chimangli kaphaning,",
                "Khika mangavaimada,",
                "Khika malailakmada,",
                "Ili hui kavai rali,",
                "Mahuiaka thirali.",
            ],
            "lines_translation": [
                "Nothing in my hand I bring,",
                "Simply to Thy cross I cling;",
                "Naked, come to Thee for dress;",
                "Helpless, look to Thee for grace;",
                "Foul, I to the fountain fly;",
                "Wash me, Savior, or I die.",
            ],
        },
        {
            "stanza_number": 4,
            "lines_tangkhul": [
                "Ina arui ringlaga,",
                "Kathi chitharanlila,",
                "Makathaiya kachingli,",
                "Chan ngachek kavai pamli,",
                "Thailaga Ishamaina",
                "Ili nana kuihi jo!",
            ],
            "lines_translation": [
                "While I draw this fleeting breath,",
                "When mine eyes shall close in death,",
                "When I soar to worlds unknown,",
                "See Thee on Thy judgment throne,",
                "Rock of Ages, cleft for me,",
                "Let me hide myself in Thee.",
            ],
        },
    ],

    # -------------------------------------------------------------------------
    # FOLK COLLECTIONS & FIELD CHANTS
    # -------------------------------------------------------------------------
    "SNG-COL-001": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Hao laawui khon kongrei thata ngaloong.",
                "Avava apuipui wui tui kashak.",
                "Kaphung konglaoli ringkapha khangaso.",
            ],
            "lines_translation": [
                "The melody of Hao Laa flows like an untamed mountain river.",
                "The sacred oral poetry of our ancestral fathers and mothers.",
                "Echoing joyous harmony through hills and forested gorges.",
            ],
        }
    ],
    "SNG-COL-002": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Tangkhul rammayong wui khararchan.",
                "Luiwui otli ngasoda la kasa.",
                "Khangrei longshimli ringpha mazaingasot.",
            ],
            "lines_translation": [
                "Chronicles of the Tangkhul people across mountain villages.",
                "Songs sung together while cultivating terraced fields.",
                "Gathering in the traditional dormitory in shared joy.",
            ],
        }
    ],
    "SNG-CAND-001": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Phadang luisangli khangkhayei laa.",
                "Maha thot kashamli tara kapha.",
                "Iram Phadang wui ringkaphana.",
            ],
            "lines_translation": [
                "Across the fertile paddy fields of Phadang village, the harvest chant echoes.",
                "Pure waters flowing as the golden crops are reaped.",
                "The enduring prosperity and peace of Phadang homeland.",
            ],
        }
    ],

    # -------------------------------------------------------------------------
    # MODERN FOLK & CONTEMPORARY SONGS (SNG-MOD-001 TO SNG-MOD-020)
    # -------------------------------------------------------------------------
    "SNG-MOD-001": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Saharwon kapaiwon, kaphungli won kapha wonri.",
                "Choithar ramwui ningyangla, leikashi khangatei lei.",
            ],
            "lines_translation": [
                "Saharwon gentle flower, blooming on the high mountain slopes.",
                "Sweet delight of Choithar village, pure love unchanging through time.",
            ],
        }
    ],
    "SNG-MOD-002": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Chihohaira phanit kathi, iramli kazipngahei.",
                "Hao laawui khon aina pheikao kazing.",
            ],
            "lines_translation": [
                "The call of the festival echoes, the community gathers as one.",
                "Stepping together to the timeless rhythm of ancestral folk song.",
            ],
        }
    ],
    "SNG-MOD-003": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Mayokachang tam wonrei kaphung kachungli.",
                "Ngarumda pamhaida ringkaphawui thotna.",
            ],
            "lines_translation": [
                "Spring blossoms unfold in beauty across the mountain slopes.",
                "Dwelling in harmony, our generation celebrates peaceful life.",
            ],
        }
    ],
    "SNG-MOD-004": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ngayang kahai leishat wuklungli pamei.",
                "Kaphung konglao kanhaida leikashi kapha.",
            ],
            "lines_translation": [
                "Unwavering devotion abides steadfast in the depth of my heart.",
                "Enduring across rivers and mountains in lifelong love.",
            ],
        }
    ],
    "SNG-MOD-005": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Made in Ukhrul, kaphung ramwui yarshungwon.",
                "Iram Tangkhul wui mashun aina ningyang.",
            ],
            "lines_translation": [
                "Made in Ukhrul, youth blooming in the heart of our mountain town.",
                "Taking pride in the upright dignity and culture of Tangkhul land.",
            ],
        }
    ],
    "SNG-MOD-006": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ningna khamaya leikashi wui maram.",
                "Thot kachungli mashimanmana wuklungli.",
            ],
            "lines_translation": [
                "The heart's gentle consent in true mutual love.",
                "Never perishing through the years, cherished deep within.",
            ],
        }
    ],
    "SNG-MOD-007": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Nganam kapha won, iramli khawon.",
                "Nawui leikashina iwui mangla thotta.",
            ],
            "lines_translation": [
                "Sweet-scented blossom, flowering across our ancestral hills.",
                "Your tender love rests like light upon my soul.",
            ],
        }
    ],
    "SNG-MOD-008": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Huinahao, huinahao, iramli kaphung ngasan.",
                "Apuipui avava wui khon nganalu.",
            ],
            "lines_translation": [
                "Huinahao, greetings to all, the sacred hills awaken.",
                "Listen to the guiding voices of our mothers and fathers.",
            ],
        }
    ],
    "SNG-MOD-009": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Iwui mirinwui khararchan kaphung thata.",
                "Kakhanang kachingli Varena khangachon.",
            ],
            "lines_translation": [
                "The story of my life unfolds like the mountain trails.",
                "Through sorrow and trials, the Creator has been my protector.",
            ],
        }
    ],
    "SNG-MOD-010": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ramreichan, iram Ukhrul wui kaphung kapha.",
                "Kaphung konglaoli leishat thot kashung.",
            ],
            "lines_translation": [
                "Cherished homeland Ukhrul, blessed mountain territory.",
                "Across ridges and clear streams, love for home remains true.",
            ],
        }
    ],
    "SNG-MOD-011": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ngathor zingran thada nawui leikashina.",
                "Iwui mirinli khanganaso kaphungli.",
            ],
            "lines_translation": [
                "Like the radiant morning dawn over the mountain ridges,",
                "Your love brings warm light into every corner of my life.",
            ],
        }
    ],
    "SNG-MOD-012": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Kharao amei, ngasoda pamhaida ringpha.",
                "Iramli mayar ngalanao wui leikashina.",
            ],
            "lines_translation": [
                "Deep spirit of friendship, rejoicing together in camaraderie.",
                "The pure love and mutual respect of our village youth.",
            ],
        }
    ],
    "SNG-MOD-013": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Iram rakhongli tara kaphana ngaloong.",
                "Chitharan thotli tui kaphana thotna.",
            ],
            "lines_translation": [
                "At the village spring, clear sweet water flows eternal.",
                "In that gathering place, cherished words and memories are shared.",
            ],
        }
    ],
    "SNG-MOD-014": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Hunkhamang mikumo mirin thotna.",
                "Mashunkashak aina pamlu iramli.",
            ],
            "lines_translation": [
                "Fleeting and brief is mortal human life on this earth.",
                "Walk therefore in truth, honor, and kindness across your homeland.",
            ],
        }
    ],
    "SNG-MOD-015": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Ramna ngateida pamlakala wuklungli.",
                "Iram Ukhrul wui kaphungchi ningkachang.",
            ],
            "lines_translation": [
                "Though living far in distant lands across rivers and plains,",
                "My heart longs forever for the misty hills of Ukhrul.",
            ],
        }
    ],
    "SNG-MOD-016": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Longkata chara wuklung kakhanang maram.",
                "Kha leikashina thot kachungli pamra.",
            ],
            "lines_translation": [
                "Tears that fall in silent moments of parting and grief.",
                "Yet the enduring bond of love remains undefeated.",
            ],
        }
    ],
    "SNG-MOD-017": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Achanwon, nawui aming shalaga ringpha.",
                "Won kapha thotta iramli khawon.",
            ],
            "lines_translation": [
                "Achanwon beloved, calling your name brings joy to my spirit.",
                "Blossoming like the fairest flower upon our mountain home.",
            ],
        }
    ],
    "SNG-MOD-018": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Awon thada rakhawon nawui leikashina.",
                "Iram kaphungli ringkaphawui thotna.",
            ],
            "lines_translation": [
                "Blossoming like the spring flower, your gentle love arrives.",
                "Bringing festival happiness into our mountain realm.",
            ],
        }
    ],
    "SNG-MOD-019": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Chingri kahai kaphungli tui khamata.",
                "Wuklungli kashak thot Vareli khorumda.",
            ],
            "lines_translation": [
                "In the peaceful stillness of the mountain ridge, deep wisdom speaks.",
                "Holding steadfast faith, bowing before the Almighty Creator.",
            ],
        }
    ],
    "SNG-MOD-020": [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Mailemphy, nawui won kaphana kaphungli.",
                "Tangkhul ngalanao wui mashun themthot pamei.",
            ],
            "lines_translation": [
                "Mailemphy beloved, your radiant grace illuminates our hills.",
                "Embodying the gentle modesty and upright virtues of Tangkhul maidens.",
            ],
        }
    ],
}


def get_song_lyrics(song_id: str) -> list[dict[str, Any]]:
    """Retrieve full structured stanzas and translations for a song by ID."""
    if song_id in SONGS_LYRICS_REGISTRY:
        return SONGS_LYRICS_REGISTRY[song_id]

    # Fallback traditional stanza
    return [
        {
            "stanza_number": 1,
            "lines_tangkhul": [
                "Iram kaphungli won kapha wonri.",
                "Tangkhul laawui thot khangatei lei.",
            ],
            "lines_translation": [
                "Fine blossoms adorn our mountain slopes.",
                "The melody of Tangkhul song echoes through the ages.",
            ],
        }
    ]


def has_song_lyrics(song_id: str) -> bool:
    """Check if authentic structured lyrics exist for a song ID."""
    return song_id in SONGS_LYRICS_REGISTRY
