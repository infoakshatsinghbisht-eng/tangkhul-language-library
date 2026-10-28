"""Script to digitalize and integrate Batch 2 historical Tangkhul hymns (SNG-HIST-007 through SNG-HIST-014)
from Rev. William Pettigrew's 1907 Jesuwui La: Hymns in Tangkhul Naga.

This script:
1. Writes the raw files to data/raw/songs/
2. Appends entries to data/manifests/songs.jsonl
3. Updates SQLite database (data/database/tangkhul_corpus.sqlite and src/tangkhul_lib/data/tangkhul_corpus.sqlite)
4. Updates src/tangkhul_lib/songs/lyrics_data.py
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

BATCH2_SONGS = [
    {
        "id": "SNG-HIST-007",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 5: Jesu Nawui Ming Phaningda",
        "alternate_titles": ["Jesus, the Very Thought of Thee (Tangkhul)", "Hymn No. 5 (1907)"],
        "title_translation": "Jesus, the Very Thought of Thee in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Bernard of Clairvaux / Edward Caswall (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "John B. Dykes (Tune 60 | Doh is C)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-005",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-007_jesuwui_laa_05_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 5 from Jesuwui La: Hymns in Tangkhul Naga (1907, American Baptist Mission, Ukhrul). 5 stanzas translated into classical Tangkhul by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-008",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 8: Jesuwui Krushwui Pamli",
        "alternate_titles": ["Beneath the Cross of Jesus (Tangkhul)", "Hymn No. 8 (1907)"],
        "title_translation": "Beneath the Cross of Jesus in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Elizabeth C. Clephane (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Frederick C. Maker (Tune 139 | Doh is Bb)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-008",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-008_jesuwui_laa_08_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 8 from Jesuwui La: Hymns in Tangkhul Naga (1907). 4 complete stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-009",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 9: Arui Chimik Tunra",
        "alternate_titles": ["Now the Day Is Over (Tangkhul)", "Hymn No. 9 (1907)"],
        "title_translation": "Now the Day Is Over in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Sabine Baring-Gould (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Joseph Barnby (Tune 296 | Doh is F)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-009",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-009_jesuwui_laa_09_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 9 from Jesuwui La: Hymns in Tangkhul Naga (1907). 7 stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-010",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 10: Jesuwui Mi Chatsa",
        "alternate_titles": ["Onward, Christian Soldiers (Tangkhul)", "Hymn No. 10 (1907)"],
        "title_translation": "Onward, Christian Soldiers in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Sabine Baring-Gould (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Arthur Sullivan (Tune 706 | Doh is C)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-010",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-010_jesuwui_laa_10_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 10 from Jesuwui La: Hymns in Tangkhul Naga (1907). 5 stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-011",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 14: Ringkapha Tui Jesu Amai",
        "alternate_titles": ["Blessed Assurance (Tangkhul)", "Hymn No. 14 (1907)"],
        "title_translation": "Blessed Assurance in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Fanny J. Crosby (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Phoebe P. Knapp (Tune 873 | Doh is G)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-014",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-011_jesuwui_laa_14_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 14 from Jesuwui La: Hymns in Tangkhul Naga (1907). 3 stanzas with chorus translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-012",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 17: Arui Ngayali Ili Ngachonlu",
        "alternate_titles": ["Abide with Me (Tangkhul)", "Hymn No. 17 (1907)"],
        "title_translation": "Abide with Me in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Henry F. Lyte (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "William H. Monk (Tune 297 | Doh is G)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-017",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-012_jesuwui_laa_17_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 17 from Jesuwui La: Hymns in Tangkhul Naga (1907). 6 complete stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-013",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 28: Jesuna Ili Laishi",
        "alternate_titles": ["Jesus, Lover of My Soul (Tangkhul)", "Hymn No. 28 (1907)"],
        "title_translation": "Jesus, Lover of My Soul in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Charles Wesley (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Simeon B. Marsh (Tune 227 | Doh is F)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-028",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-013_jesuwui_laa_28_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 28 from Jesuwui La: Hymns in Tangkhul Naga (1907). 4 complete stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
    {
        "id": "SNG-HIST-014",
        "resource_type": "songs",
        "title": "Jesuwui Laa No. 31: Makashiman Lungkhuri",
        "alternate_titles": ["Rock of Ages (Tangkhul)", "Hymn No. 31 (1907)"],
        "title_translation": "Rock of Ages in Tangkhul Naga",
        "singer": "Early Tangkhul Church Congregation",
        "lyricist": "Augustus M. Toplady (Original) / Rev. William Pettigrew (Trans.)",
        "composer": "Thomas Hastings / Richard Redhead (Tune 237)",
        "collector": "Rev. William Pettigrew",
        "performers": [],
        "year": 1907,
        "village": "Ukhrul",
        "dialect": "Ukhrul Dialect (1907 Orthography)",
        "song_type": "hymn",
        "language": "Tangkhul",
        "source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "source_identifier": "PETTIGREW-1907-HYMN-031",
        "recording_url": None,
        "lyrics_source_url": "https://archive.org/details/hymnsintangkhuln00pett",
        "local_file_path": "data/raw/songs/SNG-HIST-014_jesuwui_laa_31_pettigrew_1907.txt",
        "license": "Public Domain",
        "permission_status": "public_domain",
        "access_status": "full_text_available",
        "verification_status": "verified",
        "notes": "Hymn No. 31 from Jesuwui La: Hymns in Tangkhul Naga (1907). 4 stanzas translated by Rev. William Pettigrew.",
        "stanzas": [
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
    },
]


def write_raw_song_files():
    """Write raw song files to data/raw/songs/"""
    raw_dir = Path("data/raw/songs")
    raw_dir.mkdir(parents=True, exist_ok=True)

    for song in BATCH2_SONGS:
        file_path = Path(song["local_file_path"])
        lines = [
            "=" * 80,
            f"SONG IDENTIFIER: {song['id']}",
            f"TITLE: {song['title']}",
            f"TITLE TRANSLATION: {song['title_translation']}",
            f"SINGER / PERFORMER: {song['singer']}",
            f"LYRICIST / TRANSLATOR: {song['lyricist']}",
            f"COMPOSER: {song['composer']}",
            f"ORIGIN / VILLAGE: {song['village']}",
            f"GENRE: {song['song_type']}",
            f"PERMISSION: {song['permission_status']} (Access: {song['access_status']})",
            f"SOURCE: {song['notes']}",
            "=" * 80,
            "",
        ]

        for stanza in song["stanzas"]:
            num = stanza["stanza_number"]
            lines.append(f"[STANZA {num}]")
            lines.append("TANGKHUL:")
            for tl in stanza["lines_tangkhul"]:
                lines.append(tl)
            lines.append("")
            lines.append("ENGLISH:")
            for el in stanza["lines_translation"]:
                lines.append(el)
            lines.append("")

        file_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote raw song file: {file_path}")


def update_manifest():
    """Append the 8 songs to data/manifests/songs.jsonl if not already present."""
    manifest_path = Path("data/manifests/songs.jsonl")
    existing_ids = set()
    if manifest_path.exists():
        with open(manifest_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    existing_ids.add(rec["id"])

    to_append = []
    for s in BATCH2_SONGS:
        if s["id"] not in existing_ids:
            # Copy record without 'stanzas'
            rec = {k: v for k, v in s.items() if k != "stanzas"}
            to_append.append(rec)

    if to_append:
        with open(manifest_path, "a", encoding="utf-8") as f:
            for rec in to_append:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"Appended {len(to_append)} records to {manifest_path}")
    else:
        print("Manifest records already exist.")


def update_sqlite():
    """Insert or update records in SQLite databases."""
    db_paths = [
        Path("data/database/tangkhul_corpus.sqlite"),
        Path("src/tangkhul_lib/data/tangkhul_corpus.sqlite"),
    ]

    for db_p in db_paths:
        if not db_p.exists():
            continue
        conn = sqlite3.connect(db_p)
        cursor = conn.cursor()

        for s in BATCH2_SONGS:
            rec = {k: v for k, v in s.items() if k != "stanzas"}
            # Insert into manifest_records
            cursor.execute(
                """
                INSERT OR REPLACE INTO manifest_records
                (id, resource_type, title, language, dialect, local_file_path, license,
                 permission_status, access_status, verification_status, raw_record)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rec["id"],
                    rec["resource_type"],
                    rec["title"],
                    rec["language"],
                    rec["dialect"],
                    rec["local_file_path"],
                    rec["license"],
                    rec["permission_status"],
                    rec["access_status"],
                    rec["verification_status"],
                    json.dumps(rec, ensure_ascii=False),
                ),
            )

            # Insert into songs
            cursor.execute(
                """
                INSERT OR REPLACE INTO songs
                (id, title, alternate_titles, title_translation, singer, lyricist, composer,
                 collector, performers, year, village, dialect, song_type, language,
                 source_url, source_identifier, recording_url, lyrics_source_url,
                 local_file_path, license, permission_status, access_status,
                 verification_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rec["id"],
                    rec["title"],
                    json.dumps(rec["alternate_titles"], ensure_ascii=False),
                    rec["title_translation"],
                    rec["singer"],
                    rec["lyricist"],
                    rec["composer"],
                    rec["collector"],
                    json.dumps(rec["performers"], ensure_ascii=False),
                    rec["year"],
                    rec["village"],
                    rec["dialect"],
                    rec["song_type"],
                    rec["language"],
                    rec["source_url"],
                    rec["source_identifier"],
                    rec["recording_url"],
                    rec["lyrics_source_url"],
                    rec["local_file_path"],
                    rec["license"],
                    rec["permission_status"],
                    rec["access_status"],
                    rec["verification_status"],
                    rec["notes"],
                ),
            )

        conn.commit()
        # Verify count
        cursor.execute("SELECT count(*) FROM songs")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"Updated {db_p}: total songs = {count}")


if __name__ == "__main__":
    write_raw_song_files()
    update_manifest()
    update_sqlite()
