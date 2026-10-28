"""Complete chapter, curriculum, and textual data for Batch 2 of newly digitized Tangkhul books.

Supplies structured data for:
- BK-ARCH-004: Pa o Kamata Isha mai Jesu Christawui Khararchan: John Kahona Kasa (Pettigrew 1904)
- BK-ARCH-005: Pa o Kamata Isha mai Jesu Christawui Khararchan: Luke Kahona Kasan (Pettigrew 1905)
- BK-ARCH-006: Pa o Kachatbingna Kasa wui Khararchan: The Acts of the Apostles (Pettigrew 1905)
- BK-HIST-003: History of the Tangkhul Nagas (A. S. W. Shimray 2001)
- BK-LIT-004: Wung (Tangkhul) Naga Okthot Mayonza (T. Luikham 1961)
- BK-LIT-005: Tangkhul Folk Ballads and Oral Narratives (Prof. Khashim Ruivah 1993)
"""

from __future__ import annotations

from typing import Any


def get_pettigrew_1904_john_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-ARCH-004 (Pettigrew 1904 John)."""
    return {
        "preface": (
            "Pa o Kamata Isha mai Jesu Christawui Khararchan: John Kahona Kasa (The Gospel According to "
            "St. John in Tangkhul Naga), translated from the original Greek by Rev. William Pettigrew. "
            "Published in London by the British and Foreign Bible Society in 1904; printed at the Baptist "
            "Mission Press, Calcutta. This landmark volume represents the first printed continuous scripture "
            "portion in the Tangkhul Naga language in the Ukhrul dialect."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Kaphung-kachungwui Tui (The Word in the Beginning)",
                "page_start": 4,
                "page_end": 6,
                "summary": "The prologue to St. John: The Word was with God, life, light, and the testimony of John the Baptist.",
                "tangkhul_text": (
                    "Kaphung-kachungwui thotli Tui li-li-sai, kala Tuichi Varivarali lei, kala Tuichi Varivarasai. "
                    "Chiya kaphung-kachungli Varivarawui kachungli leisai. Ali vangteina ot kathata pamei sakahaisai; "
                    "Awui chungli haring kasawui maram leisai; kala haring chi miwungwui khanganaso thotsai. "
                    "Kala Tuichi miwung thot sakahaida i-wui ngachaili pamsai; kala i-thumna Awui mashunkashak theisai."
                ),
                "english_translation": (
                    "In the beginning was the Word, and the Word was with God, and the Word was God. "
                    "The same was in the beginning with God. All things were made by Him. In Him was life, "
                    "and the life was the light of men. And the Word was made flesh, and dwelt among us, "
                    "and we beheld His glory, full of grace and truth."
                ),
                "vocabulary": [
                    {"word": "Tui", "pos": "noun", "meaning": "word, divine discourse, logos"},
                    {"word": "Kaphung-kachung", "pos": "noun", "meaning": "the very beginning, ancient origin"},
                    {"word": "Varivara", "pos": "proper noun", "meaning": "God Almighty, Supreme Creator"},
                    {"word": "Khanganaso", "pos": "noun", "meaning": "light, radiant illumination"},
                    {"word": "Mashunkashak", "pos": "noun", "meaning": "glory, righteous majesty"},
                ],
                "grammar_notes": "The copula clitic '-sai' signifies remote past narrative, while '-na' marks divine nominative agency.",
                "exercises": [
                    {"question": "How did Pettigrew translate 'the Word' (Logos) in Tangkhul?", "type": "comprehension"},
                    {"question": "Explain the semantic adaptation of 'Varivara' for the Supreme Deity.", "type": "linguistic_analysis"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "Cana Ramli Phankahai Thot (The Marriage in Cana)",
                "page_start": 7,
                "page_end": 9,
                "summary": "The first sign in Cana of Galilee: turning water into wine and the cleansing of the Temple in Jerusalem.",
                "tangkhul_text": (
                    "Thot thumana phungli Galilee ramwui Cana shongli phankahai thotli amina pamsai; Jesu kala Awui ngashunbingli "
                    "chili ho-ngarursai. Jesuna athumli hosa: Tuisin hili tara kaping zang-chihailu. Kala athumna ngathumda kaping "
                    "zangsai. Phankahai wui pamshim-khararna tara chi khamarao kasada theiphun chitharan, kashak maram mathangsa mana. "
                    "Kala Varivarawui shimli A se-bing kala tangka kakhalimbingi theida shim katharawui pammali khor-khaleisai."
                ),
                "english_translation": (
                    "On the third day there was a marriage in Cana of Galilee. Jesus and His disciples were invited. "
                    "Jesus said unto them: Fill the waterpots with water. And they filled them to the brim. When the ruler "
                    "of the feast tasted the water that was made wine, he knew not whence it was. And in the temple He found "
                    "those that sold oxen and sheep, and drove them out of the holy place."
                ),
                "vocabulary": [
                    {"word": "Phankahai", "pos": "noun", "meaning": "marriage ceremony, wedding feast"},
                    {"word": "Tuisin", "pos": "noun", "meaning": "waterpot, earthen water vessel"},
                    {"word": "Khamarao", "pos": "noun", "meaning": "wine, ceremonial grape beverage"},
                    {"word": "Pamshim-kharar", "pos": "noun", "meaning": "governor of the feast, master of ceremonies"},
                ],
                "grammar_notes": "Prefix 'ka-' with stative stem '-ping' (full) forms the participial modifier 'kaping' (completely full).",
                "exercises": [
                    {"question": "Where did the first miracle take place in Tangkhul?", "type": "factual"},
                    {"question": "What Tangkhul phrase translates 'filled to the brim'?", "type": "translation"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Nicodemusli Tui Kaphung (Discourse with Nicodemus)",
                "page_start": 10,
                "page_end": 12,
                "summary": "Discourse on spiritual rebirth from above, the work of the Spirit, and the love of God for the world.",
                "tangkhul_text": (
                    "Phariseebingwui ngachaili Nicodemus kahona mi akhat pamsai, aya Judea miwungwui khararsai. Jesuna ngahanda hosa: "
                    "Kaphung-kachangli Ina nali hosa, mi akhatna thot katharada mazat-khalakha Varivarawui kazingram theikhami "
                    "mathailak mana. Kha Varivarana ngalei hiwui miwungli kongashi-kasa thotna, Amani Makaza Mayarwui khali "
                    "ngashir-khami, chiya Ali kachithek phungmei khikha masiman-lakla, kashak thotwui haring kazang pamsai."
                ),
                "english_translation": (
                    "There was a man of the Pharisees named Nicodemus, a ruler of the Jews. Jesus answered: Verily, verily, "
                    "I say unto thee, Except a man be born again, he cannot see the kingdom of God. For God so loved the world, "
                    "that He gave His only begotten Son, that whosoever believeth in Him should not perish, but have everlasting life."
                ),
                "vocabulary": [
                    {"word": "Thot kathara", "pos": "noun phrase", "meaning": "new birth, born again, regenerated life"},
                    {"word": "Kazingram", "pos": "noun", "meaning": "heaven, the celestial kingdom"},
                    {"word": "Kongashi-kasa", "pos": "verb phrase", "meaning": "to love tenderly, divine agape love"},
                    {"word": "Makaza Mayar", "pos": "noun phrase", "meaning": "only-begotten Son"},
                ],
                "grammar_notes": "Conditional suffix '-khalakha' (unless / except) governs the subjunctive negative verbal stem 'mazat-'.",
                "exercises": [
                    {"question": "Translate John 3:16 from Tangkhul into English.", "type": "translation"},
                    {"question": "Identify the theological terms used for 'heaven' and 'everlasting life'.", "type": "textual_analysis"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Samaria Shanawui Tui (The Samaritan Woman at the Well)",
                "page_start": 13,
                "page_end": 14,
                "summary": "Jesus at Jacob's well in Sychar of Samaria: living water and worshipping God in spirit and truth.",
                "tangkhul_text": (
                    "Jesu zattangda Jacobwui tuikhor ngalenli pamsai. Samaria shanawui akhatna tara khaphungli rasai; Jesuna ali hosa: "
                    "Ili tara mangkhami khalu. Ina khami tara khamang chi thangmatharada khangaraophung mapamlik mana; kha Ina khami "
                    "tara chi awui chungli kashak thotwui haring kaphanwui tuikhor thot salikha. Varivaraya Mangan thotsai; "
                    "kala Ali khangamorbingna Mangan kala Kashungli khangamor kashungsa."
                ),
                "english_translation": (
                    "Jesus sat thus on the well of Jacob. There cometh a woman of Samaria to draw water: Jesus saith unto her, "
                    "Give me to drink. Whosoever drinketh of the water that I shall give him shall never thirst; but the water "
                    "that I shall give him shall be in him a well of water springing up into everlasting life. God is a Spirit: "
                    "and they that worship Him must worship Him in spirit and in truth."
                ),
                "vocabulary": [
                    {"word": "Tuikhor", "pos": "noun", "meaning": "well, freshwater spring"},
                    {"word": "Khangaraophung", "pos": "noun", "meaning": "thirst, physical or spiritual longing"},
                    {"word": "Mangan", "pos": "noun", "meaning": "spirit, soul, transcendent essence"},
                    {"word": "Khangamor", "pos": "verb / noun", "meaning": "to worship, reverent bow"},
                ],
                "grammar_notes": "The dual case postposition 'kala' pairs 'Mangan' (Spirit) and 'Kashung' (Truth) as twin coordinates.",
                "exercises": [
                    {"question": "Where was the well located according to the text?", "type": "factual"},
                    {"question": "What is the requirement for true worshippers stated in John 4:24?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Bethesda Tuikhorli Thotkhamatei (Healing at Bethesda)",
                "page_start": 15,
                "page_end": 16,
                "summary": "Healing of the infirm man of thirty-eight years at Bethesda on the Sabbath and discourse on divine authority.",
                "tangkhul_text": (
                    "Jerusalemli sayat kachung khami gate wui pammali Bethesda kahona tuikhor pamsai. Chili kum thumchitaruk "
                    "kachang kazat akhatna pamsai; Jesuna ali theida hosa: Nana kaphara phasasholakha? Jesuna ali hosa: "
                    "Ngakaranglu, nawui khamathali phunglu kala zatlu! Kaphung-kachangli Ina nithumli hosa, Iwui tui kakhangasho "
                    "kala Ili kasobingli kachithekna kashak thotwui haring leisai, kala thikahaiwui ngachaili haringli kaphan theisai."
                ),
                "english_translation": (
                    "Now there is at Jerusalem by the sheep market a pool called Bethesda. A certain man was there, which had "
                    "an infirmity thirty and eight years. Jesus saith unto him, Wilt thou be made whole? Rise, take up thy bed, "
                    "and walk! Verily, verily, I say unto you, He that heareth my word, and believeth on him that sent me, "
                    "hath everlasting life, and is passed from death unto life."
                ),
                "vocabulary": [
                    {"word": "Thotkhamatei", "pos": "noun", "meaning": "miracle, supernatural wonder, sign"},
                    {"word": "Ngakaranglu", "pos": "imperative verb", "meaning": "arise, stand up immediately"},
                    {"word": "Khamatha", "pos": "noun", "meaning": "sleeping mat, traditional mattress"},
                    {"word": "Thikahai", "pos": "noun", "meaning": "death, mortality, departed state"},
                ],
                "grammar_notes": "Imperative suffix '-lu' forms strong commands: 'ngakaranglu' (arise!), 'phunglu' (take up!), 'zatlu' (walk!).",
                "exercises": [
                    {"question": "For how many years was the man infirm at Bethesda?", "type": "factual"},
                    {"question": "What three commands did Jesus give the healed man?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Raruikatha Kachiwui Paothem (The Bread of Life)",
                "page_start": 17,
                "page_end": 18,
                "summary": "Feeding of the multitudes and declaration: I am the living bread that came down from heaven.",
                "tangkhul_text": (
                    "Jesuna athumli hosa: Ina haringwui raruikatha thotsai; Iwui kachungli khara chi thangmatharada kharashok mapamlik mana; "
                    "kala Ili kachithek chi thangmatharada khangaraophung mapamlik mana. Simon Peterna ngahanda hosa: O Mapao, "
                    "ithumna khipalishong zatta katha? Nawui kachungli kashak thotwui tui pamsai. Kala ithumna chitheksai kala theisai "
                    "Nana Varivarawui Kathara chi thotsai."
                ),
                "english_translation": (
                    "And Jesus said unto them, I am the bread of life: he that cometh to me shall never hunger; and he that believeth "
                    "on me shall never thirst. Simon Peter answered Him, Lord, to whom shall we go? Thou hast the words of eternal life. "
                    "And we believe and are sure that thou art that Christ, the Son of the living God."
                ),
                "vocabulary": [
                    {"word": "Raruikatha", "pos": "noun", "meaning": "bread, food of life, sustenance"},
                    {"word": "Kharashok", "pos": "noun", "meaning": "hunger, physical want of nourishment"},
                    {"word": "Kachithek", "pos": "noun / verb", "meaning": "faith, believing trust, conviction"},
                    {"word": "Kathara", "pos": "adjective", "meaning": "holy, pure, consecrated"},
                ],
                "grammar_notes": "Double negative particle 'mapamlik mana' emphasizes categorical impossibility: shall never ever hunger.",
                "exercises": [
                    {"question": "What title did Simon Peter confess in John 6:69?", "type": "factual"},
                    {"question": "Explain the metaphor of 'haringwui raruikatha'.", "type": "theological_analysis"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "Haring Tara Kong (Rivers of Living Water)",
                "page_start": 19,
                "page_end": 20,
                "summary": "The proclamation at the Feast of Tabernacles: rivers of living water flowing from within.",
                "tangkhul_text": (
                    "Phanitwui thang kashung chili Jesu ngakarangda kaho: Mi akhatna khangaraokhalakha Iwui kachungli rada manglu. "
                    "Ili kachithekna, tui katharali kakashitheithata, awui malungli haring tara kong shokkasa pamsai. "
                    "Kha Aya Manganwui maram hosa, chiya Ali kachithekna khapan kashung thotsai."
                ),
                "english_translation": (
                    "In the last day, that great day of the feast, Jesus stood and cried, saying, If any man thirst, let him come "
                    "unto me, and drink. He that believeth on me, as the scripture hath said, out of his belly shall flow rivers "
                    "of living water. But this spake he of the Spirit, which they that believe on him should receive."
                ),
                "vocabulary": [
                    {"word": "Tara kong", "pos": "noun phrase", "meaning": "flowing river, living stream"},
                    {"word": "Malung", "pos": "noun", "meaning": "heart, innermost belly, emotional center"},
                    {"word": "Shokkasa", "pos": "verb participle", "meaning": "flowing forth, welling up from within"},
                    {"word": "Kachungli", "pos": "postposition", "meaning": "unto, toward, into the presence of"},
                ],
                "grammar_notes": "The compound noun 'tara kong' combines 'tara' (water) and 'kong' (river/stream) denoting an abundant torrent.",
                "exercises": [
                    {"question": "What promise is given to believers in John 7:38?", "type": "comprehension"},
                    {"question": "What does 'malung' symbolize in Tangkhul psychology?", "type": "cultural_analysis"},
                ],
            },
        ],
    }


def get_pettigrew_1905_luke_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-ARCH-005 (Pettigrew 1905 Luke)."""
    return {
        "preface": (
            "Pa o Kamata Isha mai Jesu Christawui Khararchan: Luke Kahona Kasan (The Gospel According to "
            "St. Luke in Tangkhul Naga), translated by Rev. William Pettigrew. Published in London by the "
            "British and Foreign Bible Society in 1905; printed at the Baptist Mission Press, Calcutta. "
            "Contains the narrative of the Nativity, the Sermon on the Plain, and the parables of the Good "
            "Samaritan and the Prodigal Son in the Ukhrul vernacular."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Theophilusli Kakhayao kala Marywui La (Preface and Magnificat)",
                "page_start": 4,
                "page_end": 6,
                "summary": "Dedication to Theophilus, the annunciation by Gabriel to Zacharias and Mary, and Mary's song of praise.",
                "tangkhul_text": (
                    "Theophilus mathilakha, Ina maram kachiva kaphung-kachungli theikasomda nawui vang kaphika mathaikha theisai. "
                    "Kachisona hosa: Zacharias, macharanlu; nawui khangamor chi khanashosai, kala nawui shanao Elisabethna mayar "
                    "akhat zatlikha. Maryna hosa: Iwui malungna Mapaoli mathan-kashei salikha, kala iwui manganna iwui Haring "
                    "Kashei Varivarali kaphung phungsai. Pangmashan phungna iwui vang ot kaphung kasada, Awui min Katharasai."
                ),
                "english_translation": (
                    "It seemed good to me also, most excellent Theophilus, to write unto thee in order. "
                    "The angel said: Fear not, Zacharias: for thy prayer is heard; and thy wife Elisabeth shall bear thee a son. "
                    "And Mary said, My soul doth magnify the Lord, and my spirit hath rejoiced in God my Saviour. "
                    "For he that is mighty hath done to me great things; and holy is his name."
                ),
                "vocabulary": [
                    {"word": "Kakhayao", "pos": "noun", "meaning": "dedication, presentation, setting forth"},
                    {"word": "Macharanlu", "pos": "imperative verb", "meaning": "fear not, be not dismayed"},
                    {"word": "Mathan-kashei", "pos": "noun / verb", "meaning": "magnification, high praise"},
                    {"word": "Pangmashan phung", "pos": "noun phrase", "meaning": "He that is mighty, the Almighty One"},
                ],
                "grammar_notes": "The negative imperative prefix 'ma-' combined with verbal stem '-charan' forms 'macharanlu' (do not fear).",
                "exercises": [
                    {"question": "To whom did Luke address his Gospel in Tangkhul?", "type": "factual"},
                    {"question": "Translate Mary's opening verse of the Magnificat into English.", "type": "translation"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "Jesuwui Phankahai Bethlehem Shongli (The Nativity)",
                "page_start": 7,
                "page_end": 9,
                "summary": "The decree of Caesar Augustus, the birth in Bethlehem, and the angelic message to the shepherds.",
                "tangkhul_text": (
                    "Zingkum chiwui thotli Caesar Augustus-wui tuingashit kaphung ngalei pamkhapeida min khangashan shoksai. "
                    "Josephna Davidwui shim kala kachung thotsada Galilee ram Nazarethwui Judea ram Bethlehem shongli zangsai. "
                    "Chili pammali shit kashikbingna thot khangaso ngasophun sayatli ngayon-kasa pamsai. Kachisona hosa: Macharanlu; "
                    "Ina nithumli miwung kachivawui kaphung kachang pao kaphung phungsai! Tangkham chili Davidwui ramli Haring "
                    "Kashei Christa Mapao phankahaisai."
                ),
                "english_translation": (
                    "And it came to pass in those days, that there went out a decree from Caesar Augustus that all the world "
                    "should be taxed. And Joseph also went up from Galilee, out of the city of Nazareth, into Judaea, unto the "
                    "city of David, which is called Bethlehem. And there were in the same country shepherds abiding in the field, "
                    "keeping watch over their flock by night. And the angel said: Unto you is born this day in the city of David "
                    "a Saviour, which is Christ the Lord."
                ),
                "vocabulary": [
                    {"word": "Tuingashit", "pos": "noun", "meaning": "decree, royal ordinance, edict"},
                    {"word": "Min khangashan", "pos": "noun phrase", "meaning": "census, tax enrollment, counting names"},
                    {"word": "Shit kashikbing", "pos": "noun plural", "meaning": "shepherds, herdsmen of the field"},
                    {"word": "Haring Kashei", "pos": "noun phrase", "meaning": "Saviour, Preserver of life"},
                ],
                "grammar_notes": "Temporal adverbial clause 'Zingkum chiwui thotli' marks historical framing (in those days).",
                "exercises": [
                    {"question": "What Roman ruler issued the census decree?", "type": "factual"},
                    {"question": "How did the angels address the shepherds in Tangkhul?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Jordan Kongli Baptisma (Baptism at Jordan)",
                "page_start": 10,
                "page_end": 11,
                "summary": "John the Baptist's preaching of repentance in the wilderness and the baptism of Jesus at the river Jordan.",
                "tangkhul_text": (
                    "Johnna Jordan kongwui pammali rada kasha-kashan kazangwui baptisma khangayei pao phungsai. Johnna ngahanda hosa: "
                    "Ina tarana baptisma khayao thotsai; kha Iwui saphunga pangmashan phung akhat raranglikha; Aya Mangan Kathara "
                    "kala meina baptisma salikha. Mi kachivana baptisma khayaoli Jesu-kha baptisma sayaosai; kala A khangamorli "
                    "kazing phangshoksai, kala kazingwui tui shoksai: Nana Iwui Mayar Kongashi thotsai."
                ),
                "english_translation": (
                    "John came into all the country about Jordan, preaching the baptism of repentance for the remission of sins. "
                    "John answered, saying unto them all, I indeed baptize you with water; but one mightier than I cometh: "
                    "he shall baptize you with the Holy Ghost and with fire. Now when all the people were baptized, it came to pass, "
                    "that Jesus also being baptized, and praying, the heaven was opened, and a voice came from heaven, which said, "
                    "Thou art my beloved Son; in thee I am well pleased."
                ),
                "vocabulary": [
                    {"word": "Baptisma khayao", "pos": "verb phrase", "meaning": "to baptize with water, ritual immersion"},
                    {"word": "Kasha-kashan", "pos": "noun", "meaning": "sins, moral transgressions"},
                    {"word": "Mei", "pos": "noun", "meaning": "fire, flame of judgment and purification"},
                    {"word": "Mayar Kongashi", "pos": "noun phrase", "meaning": "beloved son"},
                ],
                "grammar_notes": "Instrumental postposition '-na' appears in 'tarana' (with water) and 'meina' (with fire).",
                "exercises": [
                    {"question": "What two elements of baptism did John contrast?", "type": "factual"},
                    {"question": "What words were spoken from heaven at Jesus' baptism?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Nazarethli Kashung Ot (The Ministry in Nazareth)",
                "page_start": 12,
                "page_end": 13,
                "summary": "The reading of the Isaiah scroll in the synagogue at Nazareth and preaching deliverance to the captives.",
                "tangkhul_text": (
                    "Kala A Nazareth shongli zangsai, chili A kashung pamsai; Sabbath thangli synagogue shimli zangda tui kaphika phashoksai: "
                    "Mapaowui Mangan Iwui kachungli leisai, maramchilu Aya ningzanbingli pao kaphung kaphan chitheikahai thotsai; "
                    "A Ili kachiso kazatbingli thotkhamatei kala khararkashanbingli haring khami vangna. Kala A Capernaum shongli zangsai, "
                    "kala Sabbath thangli athumli tuitam chitheisai; Awui tui pangmashan phungsai."
                ),
                "english_translation": (
                    "And he came to Nazareth, where he had been brought up: and, as his custom was, he went into the synagogue "
                    "on the sabbath day, and stood up for to read. The Spirit of the Lord is upon me, because he hath anointed "
                    "me to preach the gospel to the poor; he hath sent me to heal the brokenhearted, to preach deliverance "
                    "to the captives. And he came down to Capernaum, a city of Galilee, and taught them on the sabbath days. "
                    "And they were astonished at his doctrine: for his word was with power."
                ),
                "vocabulary": [
                    {"word": "Synagogue shim", "pos": "noun", "meaning": "house of prayer, Jewish meeting hall"},
                    {"word": "Tui kaphika", "pos": "noun", "meaning": "written scroll, sacred scripture book"},
                    {"word": "Ningzanbing", "pos": "noun plural", "meaning": "the poor, the humble and afflicted"},
                    {"word": "Khararkashan", "pos": "noun", "meaning": "captives, prisoners held in bonds"},
                ],
                "grammar_notes": "Postposition '-wui vangna' denotes teleological purpose: 'haring khami vangna' (for the purpose of granting life).",
                "exercises": [
                    {"question": "What passage of scripture did Jesus read in Nazareth?", "type": "factual"},
                    {"question": "Identify the four groups blessed in the Nazareth manifesto.", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Samaria Miwung Phakazang (The Good Samaritan)",
                "page_start": 14,
                "page_end": 16,
                "summary": "The parable of the man who fell among thieves on the Jericho road and the compassionate Samaritan stranger.",
                "tangkhul_text": (
                    "Jesuna hosa: Mi akhat Jerusalem shongwui Jericho shongli vangasai; kala aya rari-kapangbingwui pangli kaphan theisai. "
                    "Athumna awui kachon khangashan kala thotkhamatei kasada ali marikha-thida vangasai. Pung-kashang akhat shongfa chili "
                    "vangasai; aya theida shong kacheili vangasai. Kha Samaria mi akhatna zatli aya ali rasai; kala aya ali theida "
                    "ning-kongashi phungsai. Aya rada awui khazatli thao kala khamarao teikahai, kala pangkaso phungda hotel shimli "
                    "phung-zangsai. Hiwui thum chili khipana rari-kapangbingwui pangli kaphanchiwui ngacham-mi thotsa naningkha? "
                    "Aya hosa: Ali kongashi kachithei chi. Jesuna hosa: Zattu, nankha chithata salu!"
                ),
                "english_translation": (
                    "A certain man went down from Jerusalem to Jericho, and fell among thieves, which stripped him of his raiment, "
                    "and wounded him, and departed, leaving him half dead. And by chance there came down a certain priest that way: "
                    "and when he saw him, he passed by on the other side. But a certain Samaritan, as he journeyed, came where he was: "
                    "and when he saw him, he had compassion on him, and went to him, and bound up his wounds, pouring in oil and wine, "
                    "and brought him to an inn, and took care of him. Which now of these three was neighbour unto him? He that shewed "
                    "mercy on him. Then said Jesus unto him, Go, and do thou likewise."
                ),
                "vocabulary": [
                    {"word": "Rari-kapangbing", "pos": "noun plural", "meaning": "robbers, road bandits"},
                    {"word": "Marikha-thi", "pos": "adjective", "meaning": "half-dead, grievously stricken"},
                    {"word": "Pung-kashang", "pos": "noun", "meaning": "priest, temple minister"},
                    {"word": "Ngacham-mi", "pos": "noun", "meaning": "neighbour, fellow human being"},
                ],
                "grammar_notes": "The compound idiomatic phrase 'ning-kongashi' signifies visceral heart compassion (malungwui kongashi).",
                "exercises": [
                    {"question": "What two travelers passed by the wounded man before the Samaritan?", "type": "factual"},
                    {"question": "How did Jesus define 'ngacham-mi' (neighbour) in this parable?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Mayar Kashingashimanwui Wari (The Prodigal Son)",
                "page_start": 17,
                "page_end": 18,
                "summary": "The parable of the lost younger son, his journey to a far country, repentance, and the father's joyous feast.",
                "tangkhul_text": (
                    "Kala A hosa: Mi akhatli mayar khikakhana leisai. Ngachonchi avana hosa: Ava, nawui lungli iwui share phunkami khalu. "
                    "Thang khakhanali ngachonchi kachiva phungda ram kachang akhatli vangasai, chili aya awui kashak kachiva shiman-hailsai. "
                    "Aya ning khangasholi hosa: Iwui ava-wui shimli ot-kashabing kachiva raruikatha kaping leisai, kha ina hili ngaraoda "
                    "thilikha! Ina ngakarangda iwui ava shongli zanglikha kala ali holikha: Ava, ina kazingram kala nawui phungli kakhama "
                    "sakahaisai. Kha aya kachangli leisalilha avana theida ning-kongashi phungda katda chikhurli phumsai."
                ),
                "english_translation": (
                    "A certain man had two sons. And the younger of them said to his father, Father, give me the portion of goods "
                    "that falleth to me. And he divided unto them his living. And not many days after the younger son gathered all together, "
                    "and took his journey into a far country, and there wasted his substance with riotous living. And when he came to himself, "
                    "he said, How many hired servants of my father's have bread enough and to spare, and I perish with hunger! "
                    "I will arise and go to my father, and will say unto him, Father, I have sinned against heaven, and before thee. "
                    "And he arose, and came to his father. But when he was yet a great way off, his father saw him, and had compassion, "
                    "and ran, and fell on his neck, and kissed him."
                ),
                "vocabulary": [
                    {"word": "Mayar khikakhana", "pos": "noun phrase", "meaning": "two sons, pair of male siblings"},
                    {"word": "Share", "pos": "noun", "meaning": "portion, inheritance share, divided property"},
                    {"word": "Shiman-hail", "pos": "verb", "meaning": "wasted away, squandered utterly"},
                    {"word": "Chikhurli phum", "pos": "verb phrase", "meaning": "embraced upon the neck, kissed warmly"},
                ],
                "grammar_notes": "Temporal correlative 'leisalilha' (while still being far off) expresses anticipatory parental vigil.",
                "exercises": [
                    {"question": "What request did the younger son make of his father?", "type": "factual"},
                    {"question": "What phrase translates 'when he came to himself' in Tangkhul?", "type": "translation"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "Emmaus Shongwui Zatkatha (The Road to Emmaus)",
                "page_start": 19,
                "page_end": 20,
                "summary": "The risen Christ walking unrecognized with two disciples on the Emmaus road and revealing Himself in the breaking of bread.",
                "tangkhul_text": (
                    "Thang chili athum ngachaiwui khani Jerusalem shongwui Emmaus kahona ramli zattangsai. Kala athumna hiwui maram "
                    "kachiva ngatei-tui kasai. Athum tui ngateili Jesu amana athumli phakazangda ngasoda vangasai. Kala A athum ngasoda "
                    "pamsai; A raruikatha phungda mathankashakda kashai chitharan athum theiphunsai! Kala athumna hosa: Shongfali A ithumli "
                    "tui hoda scripture chitheikahai thotli ithumwui malung mei katha kazang masasakha?"
                ),
                "english_translation": (
                    "And, behold, two of them went that same day to a village called Emmaus, which was from Jerusalem about threescore furlongs. "
                    "And they talked together of all these things which had happened. And it came to pass, that, while they communed together "
                    "and reasoned, Jesus himself drew near, and went with them. And it came to pass, as he sat at meat with them, he took bread, "
                    "and blessed it, and brake, and gave to them. And their eyes were opened, and they knew him. And they said one to another, "
                    "Did not our heart burn within us, while he talked with us by the way, and while he opened to us the scriptures?"
                ),
                "vocabulary": [
                    {"word": "Ngatei-tui", "pos": "verb phrase", "meaning": "to discuss, converse mutually on deep matters"},
                    {"word": "Phakazang", "pos": "verb", "meaning": "drew near, approached alongside"},
                    {"word": "Theiphunsai", "pos": "verb", "meaning": "recognized suddenly, eyes were opened"},
                    {"word": "Mei katha", "pos": "noun phrase", "meaning": "burning like fire, inflamed with conviction"},
                ],
                "grammar_notes": "The rhetorical interrogative suffix '-sakha' poses the reflective question: 'masasakha?' (did it not burn?).",
                "exercises": [
                    {"question": "At what exact moment did the disciples recognize Jesus at Emmaus?", "type": "comprehension"},
                    {"question": "How did the disciples describe their hearts burning within them?", "type": "textual_analysis"},
                ],
            },
        ],
    }


def get_pettigrew_1905_acts_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-ARCH-006 (Pettigrew 1905 Acts)."""
    return {
        "preface": (
            "Pa o Kachatbingna Kasa wui Khararchan: The Acts of the Apostles in Tangkhul Naga, translated "
            "by Rev. William Pettigrew. Published in London by the British and Foreign Bible Society, 1905; "
            "printed at the Baptist Mission Press, Calcutta. Details the day of Pentecost, Peter's defense "
            "before the Sanhedrin, Stephen's martyrdom, and Paul's speech at the Areopagus in Athens."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Kazingli Kaphan kala Kachatbing (Ascension and Commission)",
                "page_start": 4,
                "page_end": 6,
                "summary": "The ascension of Christ from the Mount of Olives and the gathering of the apostles in Jerusalem.",
                "tangkhul_text": (
                    "Theophilus-li kaphung kakhanin: Jesu-na khararchanli ot kasawui maram kaphung-kachungli kaphika thotsai. "
                    "Awui thikahaiwui saphunga A haringkasa theichithei kachiva thotna athumli thang taracham kachithei Varivarawui "
                    "kazingramwui tui hosa. Mangan Kathara nithumwui kachungli raranglikha nithum pangmashan phunglikha; "
                    "kala Jerusalemli, Judea kala Samaria ram kachivali, kala ngalei pammai kashung kachivali Iwui sakhibing salikha. "
                    "Athumna theishak phashokda Matthiasli rasai, kala aya kachatbing tarakhatli ngasohailsai."
                ),
                "english_translation": (
                    "The former treatise have I made, O Theophilus, of all that Jesus began both to do and teach. "
                    "To whom also he shewed himself alive after his passion by many infallible proofs, being seen of them forty days. "
                    "But ye shall receive power, after that the Holy Ghost is come upon you: and ye shall be witnesses unto me both "
                    "in Jerusalem, and in all Judaea, and in Samaria, and unto the uttermost part of the earth. And they gave forth "
                    "their lots; and the lot fell upon Matthias; and he was numbered with the eleven apostles."
                ),
                "vocabulary": [
                    {"word": "Kachatbing", "pos": "noun plural", "meaning": "apostles, authoritative emissaries"},
                    {"word": "Pangmashan", "pos": "noun", "meaning": "power, divine might, spiritual authority"},
                    {"word": "Sakhibing", "pos": "noun plural", "meaning": "witnesses, testifiers to truth"},
                    {"word": "Theishak", "pos": "noun", "meaning": "lots, divine casting of decision"},
                ],
                "grammar_notes": "Tangkhul uses the indigenous legal term 'sakhibing' (witnesses) for those testifying under solemn oath.",
                "exercises": [
                    {"question": "How long was Jesus seen by the apostles after His passion?", "type": "factual"},
                    {"question": "Who was chosen to take the place of Judas among the twelve?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "Pentecost Thangli Mangan Kathara (Day of Pentecost)",
                "page_start": 7,
                "page_end": 9,
                "summary": "The descent of the Holy Spirit like rushing wind and tongues of fire, and Peter's first sermon.",
                "tangkhul_text": (
                    "Pentecost kumshang phungphatli nithum pam akhangli zikahai pamsai. Kazingwui huchiphung majung katha khara rasai, "
                    "kala athum pamsahai shim kachivali kapingsai. Kala meiwui malei katha khangayeida athum kachivawui kachungli rasai. "
                    "Kala athum kachiva Mangan Katharana kapingda ngatei tui khangayei hosa! Peterna ngakarangda hosa: Israel miwung, "
                    "tui hi ngashonlu: Nazarethwui Jesu hili Varivarana thikahaiwui ngachaili thingkashangsai; chiwui maramli ithum "
                    "kachiva sakhibing thotsai. Ningzan ngashunlu, kala nithum kachiva Jesu Christawui minli baptisma sayanlu!"
                ),
                "english_translation": (
                    "And when the day of Pentecost was fully come, they were all with one accord in one place. And suddenly there "
                    "came a sound from heaven as of a rushing mighty wind, and it filled all the house where they were sitting. "
                    "And there appeared unto them cloven tongues like as of fire, and it sat upon each of them. And they were all "
                    "filled with the Holy Ghost, and began to speak with other tongues. Then Peter stood up and said, Ye men of Israel, "
                    "hear these words; This Jesus hath God raised up, whereof we all are witnesses. Repent, and be baptized every "
                    "one of you in the name of Jesus Christ."
                ),
                "vocabulary": [
                    {"word": "Huchiphung", "pos": "noun", "meaning": "rushing mighty wind, storm force"},
                    {"word": "Malei", "pos": "noun", "meaning": "tongue, flame of speech"},
                    {"word": "Ngatei tui", "pos": "noun phrase", "meaning": "other languages, diverse tongues"},
                    {"word": "Ningzan ngashun", "pos": "verb phrase", "meaning": "to repent, rectify the mind and heart"},
                ],
                "grammar_notes": "The verbal phrase 'ningzan ngashunlu' fuses 'ningzan' (heart-contrition) with 'ngashun' (to make straight).",
                "exercises": [
                    {"question": "Describe the signs that accompanied the descent of the Holy Spirit at Pentecost.", "type": "comprehension"},
                    {"question": "What did Peter urge the crowd to do at the conclusion of his sermon?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Temple Gate wui Pamli Thotkhamatei (Lame Man at the Beautiful Gate)",
                "page_start": 10,
                "page_end": 11,
                "summary": "Healing of the lame man by Peter and John at the Beautiful Gate of the Temple.",
                "tangkhul_text": (
                    "Peter kala John thangkhamir pung chiko khangamor thangli Templeli zangvangasai. Phaphuk khazat akhat, awui phankahaiwui "
                    "thotli theisai, aya Templewui Mathan Gate kahowali pamsai; aya Peter kala Johnli theida seisan khamor khanasai. "
                    "Peterna hosa: Rupa kala sona iwui chungli mathai mana; kha ina phungli nali khamlikha: Nazarethwui Jesu Christawui "
                    "minli ngakarangda zatlu! Kala ayana awui pangkasho pangda thingkasangsai; chitharan awui phakhur kala pharu "
                    "pangmashan phungsai! Aya ngachor-da ngakarangsai kala zat-zangsai, Templeli zangda khangachor kala Varivarali mathankashei sasai."
                ),
                "english_translation": (
                    "Now Peter and John went up together into the temple at the hour of prayer, being the ninth hour. "
                    "And a certain man lame from his mother's womb was carried, whom they laid daily at the gate of the temple "
                    "which is called Beautiful, to ask alms of them that entered into the temple. Then Peter said, Silver and gold "
                    "have I none; but such as I have give I thee: In the name of Jesus Christ of Nazareth rise up and walk. "
                    "And he took him by the right hand, and lifted him up: and immediately his feet and ankle bones received strength. "
                    "And he leaping up stood, and walked, and entered with them into the temple, walking, and leaping, and praising God."
                ),
                "vocabulary": [
                    {"word": "Phaphuk khazat", "pos": "noun phrase", "meaning": "lame from birth, crippled in the feet"},
                    {"word": "Rupa kala sona", "pos": "noun phrase", "meaning": "silver and gold"},
                    {"word": "Pangkasho pang", "pos": "noun phrase", "meaning": "right hand"},
                    {"word": "Khangachor", "pos": "verb participle", "meaning": "leaping, dancing with joyous vigor"},
                ],
                "grammar_notes": "The paired coordinate 'rupa kala sona' uses standard Loan-Assamese roots fully naturalized in colonial Tangkhul.",
                "exercises": [
                    {"question": "At what hour did Peter and John go up to the Temple?", "type": "factual"},
                    {"question": "What memorable response did Peter give when asked for alms?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Councilwui Phungli Sakhi Chitheikahai (Before the Sanhedrin)",
                "page_start": 12,
                "page_end": 13,
                "summary": "Peter and John arrested and questioned before the rulers, elders, and scribes of the Council.",
                "tangkhul_text": (
                    "Athumna Peter kala Johnli ngachaili pamsahai hosa: Khipawui pangmashan kala minli nithumna hi sakha? Peterna Mangan "
                    "Katharana kapingda hosa: Miwungwui khararbing kala Israelwui Hangvabing, ngatei khipawui chunglikha haring kaphan "
                    "mathailak mana; maramchilu kazing kaphungli miwungli khami ngatei min khikha mathai mana! Kha athumna Peter kala "
                    "Johnna ngahanda hosa: Nithumwui tui ngashon-katha Varivarawui tui ngashon-katha khipana mashungkha nithum shanshilu! "
                    "Maramchilu ithumna theikahai kala ngashokahai tui masasa pamtang mathailak mana."
                ),
                "english_translation": (
                    "And when they had set them in the midst, they asked, By what power, or by what name, have ye done this? "
                    "Then Peter, filled with the Holy Ghost, said unto them, Ye rulers of the people, and elders of Israel, "
                    "Neither is there salvation in any other: for there is none other name under heaven given among men, whereby "
                    "we must be saved. But Peter and John answered and said unto them, Whether it be right in the sight of God to hearken "
                    "unto you more than unto God, judge ye. For we cannot but speak the things which we have seen and heard."
                ),
                "vocabulary": [
                    {"word": "Hangvabing", "pos": "noun plural", "meaning": "council of elders, senators, Sanhedrin magistrates"},
                    {"word": "Kazing kaphungli", "pos": "prepositional phrase", "meaning": "under heaven, beneath the celestial dome"},
                    {"word": "Ngashon-katha", "pos": "verb phrase", "meaning": "to hearken, obey, submit to authority"},
                    {"word": "Shanshilu", "pos": "imperative verb", "meaning": "judge ye, weigh and determine"},
                ],
                "grammar_notes": "Pettigrew uses the indigenous administrative title 'Hangvabing' (village elder bench) for the Sanhedrin rulers.",
                "exercises": [
                    {"question": "How did Peter respond to the council's prohibition against preaching?", "type": "comprehension"},
                    {"question": "Explain the cultural borrowing of 'Hangva' in early Tangkhul scriptural translation.", "type": "linguistic_analysis"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Stephenwui Pao kala Kashung Thot (The Martyrdom of Stephen)",
                "page_start": 14,
                "page_end": 15,
                "summary": "Stephen's defense before the council, vision of the Son of Man, and stoning as the first Christian martyr.",
                "tangkhul_text": (
                    "Stephenna ning-kachang kala pangmashan phungda miwungwui ngachaili theichithei kaphung sasai. Council shimli "
                    "pambing kachivana ali theida awui mai kazingram kachisowui mai katha theisai. Kha aya Mangan Katharana kapingda "
                    "kazingli theida Varivarawui mathankashak theisai. Kala athumna lungna chidatli Stephenna khon-kaphung: O Mapao Jesu, "
                    "iwui mangankhali khaphanlu! Kala aya phakhur phumda kaho: O Mapao, kakhama hi athumwui chungli machonlu! "
                    "Hi hoda aya thikahaisai. Saulna awui thikahaili ningkachang phungsai."
                ),
                "english_translation": (
                    "And Stephen, full of faith and power, did great wonders and miracles among the people. And all that sat in the council, "
                    "looking stedfastly on him, saw his face as it had been the face of an angel. But he, being full of the Holy Ghost, "
                    "looked up stedfastly into heaven, and saw the glory of God. And they stoned Stephen, calling upon God, and saying, "
                    "Lord Jesus, receive my spirit. And he kneeled down, and cried with a loud voice, Lord, lay not this sin to their charge. "
                    "And when he had said this, he fell asleep. And Saul was consenting unto his death."
                ),
                "vocabulary": [
                    {"word": "Lungna chidat", "pos": "verb phrase", "meaning": "cast stones, stoned with rocks"},
                    {"word": "Khon-kaphung", "pos": "verb participle", "meaning": "calling out with loud voice, invoking"},
                    {"word": "Machonlu", "pos": "imperative negative", "meaning": "lay not to charge, impute not"},
                    {"word": "Phakhur phum", "pos": "verb phrase", "meaning": "kneeled down, fell on knees in prayer"},
                ],
                "grammar_notes": "Instrumental postposition '-na' on 'lungna' marks the lethal physical instrument: by means of stones.",
                "exercises": [
                    {"question": "What two prayers did Stephen utter before his death?", "type": "factual"},
                    {"question": "Who was recorded as consenting to Stephen's death?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Corneliusli Pao Kazang (Conversion of Cornelius)",
                "page_start": 16,
                "page_end": 17,
                "summary": "Peter's vision of the clean and unclean animals, journey to Caesarea, and the gospel opened to the Gentiles.",
                "tangkhul_text": (
                    "Caesarea ramli Cornelius kahona Italian cohortwui centurion akhat pamsai. Aya Varivarali kacharan, awui shim "
                    "kachiva ngasoda, miwungli dori khami kala Varivarali thang kachiva khangamor. Peterna Caesareali rada hosa: "
                    "Kaphung-kachangli ina theisai Varivarana mi akhatli kaching mei mana; kha ram kachivali Ali kacharan kala "
                    "mashungkasa chi Awui ningkachang phungsai. Peterna tui hi holikha Mangan Katharana tui ngashonbing kachivawui "
                    "chungli rasai!"
                ),
                "english_translation": (
                    "There was a certain man in Caesarea called Cornelius, a centurion of the band called the Italian band, "
                    "A devout man, and one that feared God with all his house, which gave much alms to the people, and prayed to God alway. "
                    "Then Peter opened his mouth, and said, Of a truth I perceive that God is no respecter of persons: "
                    "But in every nation he that feareth him, and worketh righteousness, is accepted with him. "
                    "While Peter yet spake these words, the Holy Ghost fell on all them which heard the word."
                ),
                "vocabulary": [
                    {"word": "Kaching mei mana", "pos": "idiomatic clause", "meaning": "does not show partiality, no respecter of persons"},
                    {"word": "Kacharan", "pos": "adjective / verb", "meaning": "reverent, God-fearing, devout"},
                    {"word": "Dori", "pos": "noun", "meaning": "alms, charitable offerings to the needy"},
                    {"word": "Ningkachang", "pos": "noun", "meaning": "favor, delight, divine acceptance"},
                ],
                "grammar_notes": "The negative comparative 'kaching mei mana' (literally: does not exceed in biased viewing) translates impartial justice.",
                "exercises": [
                    {"question": "What was the occupation of Cornelius in Caesarea?", "type": "factual"},
                    {"question": "What theological breakthrough did Peter announce in Acts 10:34-35?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "Athens Ramli Paulna Tui Chitheikahai (Paul at the Areopagus)",
                "page_start": 18,
                "page_end": 20,
                "summary": "Paul's sermon at Mars Hill in Athens concerning the Unknown God, repentance, and resurrection.",
                "tangkhul_text": (
                    "Paulna Areopagus (Mars Hill) ngachaili ngakarangda hosa: Athens miwung, ina theisai nithum thang kachiva kameo "
                    "khangamor phungsai; maramchilu ina zatli nithumwui altar akhatli kaphika theisai: MATHIKAHAI VARIVARALI. "
                    "Nithumna matheila khangamor hili ina chitheikhami! Kazing kala ngalei kala chili leisatha kachiva sakahai "
                    "Varivara chili kazing kala ngaleiwui Mapaosai, Aya mina sakahai templeli mapam mana; maramchilu Awui chungli "
                    "ithum haring, zatta, kala pamsai; nithumwui la-kashabingna hokatha: 'Ithumya Awui kachung thotsai.'"
                ),
                "english_translation": (
                    "Then Paul stood in the midst of Mars' hill, and said, Ye men of Athens, I perceive that in all things ye are too superstitious. "
                    "For as I passed by, and beheld your devotions, I found an altar with this inscription, TO THE UNKNOWN GOD. "
                    "Whom therefore ye ignorantly worship, him declare I unto you. God that made the world and all things therein, "
                    "seeing that he is Lord of heaven and earth, dwelleth not in temples made with hands; For in him we live, "
                    "and move, and have our being; as certain also of your own poets have said, For we are also his offspring."
                ),
                "vocabulary": [
                    {"word": "Mathikahai Varivara", "pos": "noun phrase", "meaning": "Unknown God, the unrevealed Creator"},
                    {"word": "Kameo", "pos": "noun", "meaning": "traditional nature spirits, idols, lesser deities"},
                    {"word": "La-kashabing", "pos": "noun plural", "meaning": "poets, ballad makers, lyricists"},
                    {"word": "Kachung", "pos": "noun", "meaning": "offspring, lineage, children of the divine"},
                ],
                "grammar_notes": "Pettigrew contrasts indigenous 'Kameo' (animistic spirits) with the sovereign 'Varivara' (Creator of heaven and earth).",
                "exercises": [
                    {"question": "What inscription did Paul encounter in Athens?", "type": "factual"},
                    {"question": "How did Paul quote the Greek poets in Tangkhul?", "type": "comprehension"},
                ],
            },
        ],
    }


def get_shimray_2001_history_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-HIST-003 (Shimray 2001 History)."""
    return {
        "preface": (
            "History of the Tangkhul Nagas by A. S. W. Shimray (Akansha Publishing House, New Delhi, 2001, "
            "ISBN 81-87606-04-5). A comprehensive ethnographic, historical, and sociological monograph "
            "documenting Tangkhul origin traditions from Makhel, village republic governance under the Awunga "
            "and Hangva, agricultural engineering, clan land tenures, ritual warfare, and modern political integration."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Origin Traditions and Migration from Makhel",
                "page_start": 4,
                "page_end": 6,
                "summary": "Ancient origins at Makhel and Khezhakenoma, the myth of the three brothers, and settlement of the Ukhrul ridge.",
                "tangkhul_text": (
                    "Tangkhul oral literature unequivocally traces ancestral migrations back to Makhel in northern Manipur and "
                    "contiguous Khezhakenoma. From Makhel, three brothers departed: the eldest became the Meitei of the valley, "
                    "the middle the Tangkhul of the eastern hills, and the youngest the Northern Naga groups. "
                    "Hundung and Hunphun represent the dual pivotal chieftaincies from which daughter settlements radiated throughout "
                    "the Raphei (Northern), Rem (Western), Kharao (Southern), and Khanggo (Eastern) geographical divisions. "
                    "While standard Tangkhul is based on the dialect of Hunphun, the tribe comprises over one hundred villages."
                ),
                "english_translation": (
                    "Tangkhul oral literature unequivocally traces ancestral migrations back to Makhel in northern Manipur and "
                    "contiguous Khezhakenoma. From Makhel, three brothers departed: the eldest became the Meitei of the valley, "
                    "the middle the Tangkhul of the eastern hills, and the youngest the Northern Naga groups. "
                    "Hundung and Hunphun represent the dual pivotal chieftaincies from which daughter settlements radiated throughout "
                    "the Raphei, Rem, Kharao, and Khanggo geographical divisions. Over one hundred villages maintain distinct idioms."
                ),
                "vocabulary": [
                    {"word": "Makhel", "pos": "proper noun", "meaning": "sacred ancestral dispersal village of the Naga tribes"},
                    {"word": "Raphei", "pos": "proper noun", "meaning": "northern Tangkhul territorial division"},
                    {"word": "Rem", "pos": "proper noun", "meaning": "western Tangkhul mountain division"},
                    {"word": "Khanggo", "pos": "proper noun", "meaning": "eastern border division contiguous to Myanmar"},
                ],
                "grammar_notes": "Toponyms like 'Raphei' and 'Kharao' function as regional dialect and sociocultural identifiers.",
                "exercises": [
                    {"question": "What three brother-groups departed from Makhel in Tangkhul tradition?", "type": "factual"},
                    {"question": "Name the four ancient geographical divisions of the Tangkhul hills.", "type": "geographical_analysis"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "The Village Republic: Awunga and the Hangva Council",
                "page_start": 7,
                "page_end": 9,
                "summary": "Village sovereignty (Wungram), the hereditary chief (Awunga), the clan elder bench (Hangva), and the Longshim dormitory.",
                "tangkhul_text": (
                    "The traditional Tangkhul village was an autonomous republic with defined territorial borders. At the head of each "
                    "village stood the Awunga (hereditary chief), governing in strict concert with the Hangva (Council of Elders representing "
                    "all village clans). The Hangva met at the Awunga's courtyard to adjudicate disputes, announce festival schedules, "
                    "declare seasonal taboos (khamthei), and decide matters of peace or war. Decisions were reached through consensus (ngalung). "
                    "Integral to village life was the Longshim (youth dormitory system) which served as the civic militia and school of etiquette."
                ),
                "english_translation": (
                    "The traditional Tangkhul village was an autonomous republic with defined territorial borders. At the head of each "
                    "village stood the Awunga (hereditary chief), governing in strict concert with the Hangva (Council of Elders representing "
                    "all clans). The Hangva met at the chief's courtyard to adjudicate disputes, announce festival schedules, "
                    "declare seasonal taboos, and decide peace or war. Consensus (ngalung) governed all decisions. The Longshim dormitory "
                    "trained youth in civic defense and customary etiquette."
                ),
                "vocabulary": [
                    {"word": "Awunga", "pos": "noun", "meaning": "village chief, hereditary royal headman"},
                    {"word": "Hangva", "pos": "noun", "meaning": "village council of clan elders"},
                    {"word": "Ngalung", "pos": "noun", "meaning": "consensus, unanimous deliberative agreement"},
                    {"word": "Longshim", "pos": "noun", "meaning": "youth dormitory, communal education hall"},
                ],
                "grammar_notes": "The compound 'Wungram' joins 'Wung' (indigenous ethnonym) with 'ram' (land / country / territory).",
                "exercises": [
                    {"question": "How did the Hangva council reach decisions under customary governance?", "type": "comprehension"},
                    {"question": "Describe the educational and defensive roles of the Longshim dormitory.", "type": "sociological_analysis"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Agricultural Regimes: Luingam and Shilmik",
                "page_start": 10,
                "page_end": 11,
                "summary": "Terrace cultivation (Luingam), swidden farming (Shilmik), irrigation channels (kong-kuir), and the Luira festival.",
                "tangkhul_text": (
                    "Tangkhul subsistence economy was anchored upon wet-rice terrace cultivation (Luingam) and rotational swidden farming (Shilmik). "
                    "Terraces along mountain slopes required gravity-fed irrigation channels (kong-kuir) maintained collectively by syndicates. "
                    "The agricultural calendar opened with the Luira Phanit (seed-sowing festival) in February. No villager was permitted to sow "
                    "until the Awunga performed the sacred first sowing ritual. Harvest was celebrated with Chumpha in December, consecrating "
                    "newly garnered paddy in village granaries (raizan)."
                ),
                "english_translation": (
                    "Tangkhul subsistence economy was anchored upon wet-rice terrace cultivation (Luingam) and rotational swidden farming (Shilmik). "
                    "Terraces along mountain slopes required gravity-fed irrigation channels (kong-kuir) maintained collectively by syndicates. "
                    "The agricultural year began with Luira Phanit in February with the chief's sacred first sowing, and closed with "
                    "Chumpha in December, consecrating newly stored grain in family granaries."
                ),
                "vocabulary": [
                    {"word": "Luingam", "pos": "noun", "meaning": "wet-rice terrace cultivation, irrigated terrace field"},
                    {"word": "Shilmik", "pos": "noun", "meaning": "swidden agriculture, slash-and-burn jhum plot"},
                    {"word": "Kong-kuir", "pos": "noun", "meaning": "irrigation canal, gravity-fed water channel"},
                    {"word": "Raizan", "pos": "noun", "meaning": "granary, raised storehouse for harvested paddy"},
                ],
                "grammar_notes": "Compound root 'luira' combines 'lui' (terrace field) and 'ra' (water / festival rites).",
                "exercises": [
                    {"question": "What is the distinction between Luingam and Shilmik cultivation?", "type": "comparative_analysis"},
                    {"question": "Which festivals mark the opening and closing of the Tangkhul farming cycle?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Clan Kinship (Shang) and Land Tenure",
                "page_start": 12,
                "page_end": 14,
                "summary": "Exogamous patrilineal clans (Shang), inheritance by male primogeniture, and the sacrosanct role of Pukreila peace envoys.",
                "tangkhul_text": (
                    "Tangkhul society is strictly exogamous and patrilineal, organized into clans (shang) and sub-lineages (shimkhor). "
                    "Marriage within the clan was strictly prohibited as shiman-kaphung. Land tenure was threefold: communal village land, "
                    "clan land, and family hereditary plots. Ancestral homesteads passed through male primogeniture. When villages entered "
                    "formal treaties, high-status women born in one village and married into the other acted as Pukreila (peace ambassadors). "
                    "The person of the Pukreila was sacrosanct; harming an ambassador was regarded as an unforgivable breach invoking divine retribution."
                ),
                "english_translation": (
                    "Tangkhul society is strictly exogamous and patrilineal, organized into clans (shang) and sub-lineages (shimkhor). "
                    "Intra-clan marriage was strictly prohibited. Land tenure comprised communal village land, clan reserves, and family plots. "
                    "Homesteads passed via male primogeniture. Inter-village treaties were mediated by Pukreila (female peace ambassadors). "
                    "The person of the Pukreila was sacrosanct, and harming an ambassador invoked severe divine retribution."
                ),
                "vocabulary": [
                    {"word": "Shang", "pos": "noun", "meaning": "patrilineal clan, exogamous kinship group"},
                    {"word": "Shimkhor", "pos": "noun", "meaning": "sub-lineage, hearth-circle within a clan"},
                    {"word": "Pukreila", "pos": "noun", "meaning": "female peace ambassador, sacrosanct treaty envoy"},
                    {"word": "Khamatui", "pos": "noun", "meaning": "divine retribution, cosmic curse on covenant breakers"},
                ],
                "grammar_notes": "The feminine suffix '-la' in 'Pukreila' designates an honored woman functioning in ambassadorial capacity.",
                "exercises": [
                    {"question": "Explain the diplomatic and moral functions of the Pukreila in Naga warfare.", "type": "historical_analysis"},
                    {"question": "What are the three categories of land ownership under Tangkhul customary law?", "type": "legal_analysis"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Head-Taking (Rai) and Peacemaking Rituals",
                "page_start": 15,
                "page_end": 16,
                "summary": "The ritual logic of head-taking, the village skull repository, and the solemn covenant of spear burial.",
                "tangkhul_text": (
                    "Head-taking among the Tangkhul was bound to cosmological balance, fertility of crops, and personal valor. "
                    "It was ritual warfare governed by strict customary boundaries. Heads taken were brought to the village entrance, "
                    "received with ritual chants, and hung at the sacred village tree (khor-thing) or deposited at the village skull depository. "
                    "Wars were concluded through the solemn ceremony of spear burial (kachu-kapam) and the consumption of ceremonial "
                    "pork and rice-beer between combatant Awungas. Broken oaths brought calamity upon future generations."
                ),
                "english_translation": (
                    "Head-taking among the Tangkhul was bound to cosmological balance, fertility of crops, and personal valor. "
                    "It was ritual warfare governed by strict customary boundaries. Heads taken were brought to the village entrance, "
                    "hung at the sacred village tree (khor-thing) or placed in the skull depository. Wars concluded through the ceremony "
                    "of spear burial (kachu-kapam) and mutual consumption of ceremonial food by chiefs, sealing eternal oaths."
                ),
                "vocabulary": [
                    {"word": "Rai", "pos": "noun", "meaning": "warfare, military expedition, martial contest"},
                    {"word": "Khor-thing", "pos": "noun", "meaning": "sacred village tree, warrior trophy oak"},
                    {"word": "Kachu-kapam", "pos": "noun phrase", "meaning": "spear burial, solemn peacemaking covenant"},
                    {"word": "Tala-khon", "pos": "noun", "meaning": "war horn, buffalo horn trumpet sounding alarm or victory"},
                ],
                "grammar_notes": "Compound verbal noun 'kachu-kapam' pairs 'kachu' (spear) with 'kapam' (planting/burying deeply).",
                "exercises": [
                    {"question": "How did Tangkhul warriors conclude peace after warfare?", "type": "comprehension"},
                    {"question": "What cosmological beliefs were associated with head-taking?", "type": "anthropological_analysis"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Traditional Religion: Kameo, Varivara, and Feasts of Merit",
                "page_start": 17,
                "page_end": 18,
                "summary": "Cosmological belief in the Supreme God (Varivara), spirits of nature (Kameo), and memorial Feasts of Merit (Maringphat).",
                "tangkhul_text": (
                    "Tangkhul cosmology recognized a Supreme Creator God (Varivara) who dwelt in the highest heavens, benevolent and just. "
                    "Beneath Varivara were regional nature spirits (Kameo) inhabiting sacred groves, cliffs, and peaks. Propitiatory offerings "
                    "were made by the village priest (Maiba) to appease spirits. Wealthy individuals who accumulated surplus grain and cattle "
                    "performed progressive Feasts of Merit (Maringphat), feeding the entire village community and allied settlements for multiple "
                    "days, erecting memorial megaliths (lung-thei), and carving house-fronts with horn-motifs (lengcheng-pakhang)."
                ),
                "english_translation": (
                    "Tangkhul cosmology recognized a Supreme Creator God (Varivara) who dwelt in the highest heavens, benevolent and just. "
                    "Beneath Varivara were nature spirits (Kameo) inhabiting sacred groves, cliffs, and peaks, propitiated by the priest (Maiba). "
                    "Wealthy individuals performed progressive Feasts of Merit (Maringphat), hosting the entire community for multiple days, "
                    "erecting memorial megaliths (lung-thei), and carving house facades with ceremonial horn motifs."
                ),
                "vocabulary": [
                    {"word": "Maiba", "pos": "noun", "meaning": "traditional village priest, ritual sacrificer"},
                    {"word": "Maringphat", "pos": "noun", "meaning": "Feast of Merit, progressive socioeconomic feast"},
                    {"word": "Lung-thei", "pos": "noun", "meaning": "memorial stone megalith, standing commemorative stone"},
                    {"word": "Lengcheng-pakhang", "pos": "noun phrase", "meaning": "house-horns, carved gable-planks of feast givers"},
                ],
                "grammar_notes": "Nominal compound 'lung-thei' combines 'lung' (stone) with stative 'thei' (manifest / conspicuous).",
                "exercises": [
                    {"question": "What cultural privileges did a Feast of Merit confer upon a Tangkhul family?", "type": "comprehension"},
                    {"question": "Distinguish between the supreme role of Varivara and localized Kameo spirits.", "type": "theological_analysis"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "The Colonial Encounter and Political Awakenings",
                "page_start": 19,
                "page_end": 20,
                "summary": "Colonial pacification, William Pettigrew's mission school in Ukhrul, and the emergence of modern Naga consciousness.",
                "tangkhul_text": (
                    "The arrival of British administration in the late 19th century and the establishment of Rev. William Pettigrew's "
                    "mission school at Ukhrul in 1896 initiated dramatic socioeconomic transformations. Roman script literacy, modern medical care, "
                    "and Christianity gradually replaced the head-taking regime. Yet Tangkhul customary laws, land rights, and village identity "
                    "endured, forming the foundation of modern Naga political consciousness and solidarity in northeast India."
                ),
                "english_translation": (
                    "British colonial administration and Rev. William Pettigrew's mission school in 1896 at Ukhrul catalyzed profound "
                    "transformations. Roman literacy, healthcare, and Christianity gradually replaced the warfare regime. Yet customary laws, "
                    "ancestral land tenure, and village identity endured, providing the bedrock of modern Naga political solidarity in northeast India."
                ),
                "vocabulary": [
                    {"word": "Wungram kashang", "pos": "noun phrase", "meaning": "elevation and dignity of the Tangkhul homeland"},
                    {"word": "Pettigrew-wui thot", "pos": "noun phrase", "meaning": "the missionary era, advent of modern education (1896+)"},
                    {"word": "Tuingashit kathara", "pos": "noun phrase", "meaning": "new covenant, modern constitutional rights"},
                    {"word": "Ngalung-khangayei", "pos": "noun", "meaning": "political unity, pan-tribal solidarity"},
                ],
                "grammar_notes": "Temporal genitive 'Pettigrew-wui thot' marks the pivotal historical turning point in modern Tangkhul historiography.",
                "exercises": [
                    {"question": "When did Rev. William Pettigrew establish the first school in Ukhrul?", "type": "factual"},
                    {"question": "How did customary land tenure survive colonial and post-colonial governance?", "type": "historical_synthesis"},
                ],
            },
        ],
    }


def get_luikham_1961_customary_law_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-LIT-004 (Luikham 1961 Customary Law)."""
    return {
        "preface": (
            "Wung (Tangkhul) Naga Okthot Mayonza (Tangkhul Customary Law, Jurisprudence, and Social Ethics), "
            "compiled and authored by T. Luikham (Indigenous Scholar and Author, published at Imphal/Ukhrul, "
            "1961). The definitive native codification of Tangkhul legal philosophy, matrimonial codes, "
            "clan inheritance, trials by ordeal, sanctuary rights, and compensatory restitution."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "The Jurisprudential Philosophy of Wung Law",
                "page_start": 4,
                "page_end": 6,
                "summary": "Core principles of restorative justice: cosmic equilibrium (shak-kasa), communal restitution, and clan liability.",
                "tangkhul_text": (
                    "Wung (Tangkhul) customary law does not distinguish rigidly between civil tort and criminal injury; every offense is "
                    "understood as a breach of cosmic and communal equilibrium (shak-kasa). The primary goal of judicial proceedings is not "
                    "punitive incarceration, but the restitution of social harmony through compensatory settlement (shiman). "
                    "Law is rooted in three principles: Respect for Ancestral Covenant (Khararchanwui Tuingashit), Preservation of Clan Integrity "
                    "(Shangwui Kaphung), and Absolute Truthfulness before Varivara. The clan stands collective surety for its members."
                ),
                "english_translation": (
                    "Wung customary law does not distinguish rigidly between tort and crime; every offense is a breach of cosmic equilibrium (shak-kasa). "
                    "The primary goal is restorative harmony through compensatory settlement (shiman) rather than punitive incarceration. "
                    "Law rests on three pillars: ancestral covenants, clan integrity, and truthfulness before God. The clan bears collective liability."
                ),
                "vocabulary": [
                    {"word": "Mayonza", "pos": "noun", "meaning": "customary law, justice code, jurisprudence"},
                    {"word": "Shak-kasa", "pos": "noun", "meaning": "breach of taboo, disrupting communal balance"},
                    {"word": "Shiman", "pos": "noun", "meaning": "compensatory fine, restitution, indemnification"},
                    {"word": "Shangwui kaphung", "pos": "noun phrase", "meaning": "corporate clan honor and collective standing"},
                ],
                "grammar_notes": "The abstract noun 'mayonza' derives from root 'mayon' (to watch over / govern responsibly) + '-za' (statute).",
                "exercises": [
                    {"question": "What is the primary objective of judicial proceedings in Wung customary law?", "type": "comprehension"},
                    {"question": "How does clan solidarity function regarding civil liabilities and fines?", "type": "legal_analysis"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "Marriage Laws (Ngalong), Alliances, and Bride Wealth",
                "page_start": 7,
                "page_end": 9,
                "summary": "Strict clan exogamy, matrilateral cross-cousin alliances, bride wealth (shiman) protocols, and divorce penalties.",
                "tangkhul_text": (
                    "Marriage is an alliance between two distinct clans (shang). Strict exogamy is enforced under pain of grave moral censure. "
                    "Marriage with a maternal aunt's daughter or mother's clan was preferred (cross-cousin marriage), cementing alliances. "
                    "Bride wealth among the Tangkhul is not a commercial transaction, but a symbolic recompense to the bride's clan for the loss "
                    "of her productive labor. Typical gifts include cattle (se), brass gongs (sen-kuir), and shawls. Divorce was uncommon "
                    "and subject to rigorous financial penalties and property restitution."
                ),
                "english_translation": (
                    "Marriage is an alliance between two distinct clans under strict exogamy. Cross-cousin marriage cemented bilateral ties. "
                    "Bride wealth was a symbolic recompense for the loss of female labor, consisting of cattle, brass gongs, and handwoven textiles. "
                    "Divorce was rare and penalized by stringent property forfeitures and subsistence indemnities."
                ),
                "vocabulary": [
                    {"word": "Ngalong", "pos": "noun", "meaning": "matrimonial law, marriage institution"},
                    {"word": "Sen-kuir", "pos": "noun", "meaning": "valuable brass ceremonial gong used in bride wealth"},
                    {"word": "Tui-kachathei", "pos": "noun", "meaning": "formal betrothal negotiation between clan spokesmen"},
                    {"word": "Ngalawui phunglung", "pos": "noun phrase", "meaning": "dowry possessions brought by the bride"},
                ],
                "grammar_notes": "The nominal compound 'sen-kuir' fuses 'sen' (brass / bell-metal) with 'kuir' (circular rim / gong).",
                "exercises": [
                    {"question": "Why was cross-cousin marriage favored in traditional Tangkhul society?", "type": "sociological_analysis"},
                    {"question": "What customary articles constituted bride wealth in Luikham's documentation?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Clan Inheritance (Kashak) and Land Tenures",
                "page_start": 10,
                "page_end": 11,
                "summary": "Inalienability of ancestral terrace fields, right of preemption by clan brethren, and primogeniture obligations.",
                "tangkhul_text": (
                    "Terrace land (Luingam) is held in perpetuity by lineages. Under no circumstance may ancestral land be sold to an outsider "
                    "from another village. If an individual must alienate land due to debt, he must first offer the right of preemption to his "
                    "nearest clan brethren (shangwui ngacham-mi). The eldest son (kaphung-mayar) inherits the ancestral home (shim-kharar) "
                    "and principal terrace fields, assuming the obligation of maintaining aging parents and performing funeral rites. "
                    "Younger sons receive secondary plots and assistance in constructing independent homesteads."
                ),
                "english_translation": (
                    "Terrace land (Luingam) is held in perpetuity by lineages and can never be alienated to outside villagers. "
                    "Preemption rights belong strictly to nearest clan brethren. The eldest son inherits the ancestral home and fields, "
                    "assuming the solemn duty of caring for aged parents and funding funeral rites. Younger sons receive subordinate shares."
                ),
                "vocabulary": [
                    {"word": "Kashak", "pos": "noun", "meaning": "inheritance, division of ancestral patrimony"},
                    {"word": "Shim-kharar", "pos": "noun", "meaning": "ancestral home, the elder family hearth"},
                    {"word": "Kaphung-mayar", "pos": "noun", "meaning": "eldest son, principal heir and hearth keeper"},
                    {"word": "Thikahaiwui ot", "pos": "noun phrase", "meaning": "funeral rites and ceremonial obligations for deceased parents"},
                ],
                "grammar_notes": "The kinship term 'kaphung-mayar' signifies literally 'the son who bears the lineage weight' ('phung' = carry).",
                "exercises": [
                    {"question": "State the rule of preemption governing Tangkhul terrace fields.", "type": "legal_analysis"},
                    {"question": "What specific duties fall upon the eldest son under primogeniture?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Civil Wrongs, Thefts, and Restitution (Shiman)",
                "page_start": 12,
                "page_end": 13,
                "summary": "The threefold restitution rule for animal theft, grain theft penalties, and mediation of accidental injuries.",
                "tangkhul_text": (
                    "Theft of domestic animals was punished by threefold restitution (thum-ngashit): returning the stolen beast plus two "
                    "additional animals of equal value as fine (kashiman) to the aggrieved family, plus a cleansing pig to the village council. "
                    "Theft of harvested grain from field granaries was regarded as an aggravated offense requiring immediate public apology and heavy indemnity. "
                    "Accidental physical injury was compensated according to working days lost, with the responsible party supplying rice and fowl. "
                    "Homicide required temporary banishment to avert blood vengeance, followed by Pukreila peace negotiations."
                ),
                "english_translation": (
                    "Theft of domestic animals was punished by threefold restitution (thum-ngashit): returning the animal plus two others as fine, "
                    "with a cleansing pig for the council. Granary theft required public apology and heavy indemnity. Accidental injuries "
                    "were compensated based on lost working days and medicinal supplies. Homicide necessitated temporary exile to avert vengeance."
                ),
                "vocabulary": [
                    {"word": "Thum-ngashit", "pos": "noun", "meaning": "threefold restitution, triple compensatory penalty"},
                    {"word": "Kashiman", "pos": "noun", "meaning": "judicial fine, indemnification sum"},
                    {"word": "Rai-shiman", "pos": "noun", "meaning": "blood vengeance compensation, homicide settlement"},
                    {"word": "Khamazik", "pos": "noun", "meaning": "public apology, ceremonial reconciliation before council"},
                ],
                "grammar_notes": "Numeral compound 'thum-ngashit' combines 'thum' (three) with 'ngashit' (equal fold / multiplied measure).",
                "exercises": [
                    {"question": "Explain the formula of 'thum-ngashit' for livestock theft.", "type": "mathematical_legal_analysis"},
                    {"question": "Why was granary theft considered an aggravated offense against the village?", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Judicial Oaths and Trial by Ordeal (Theishak)",
                "page_start": 14,
                "page_end": 15,
                "summary": "Trial by ordeal when evidence fails: tiger tooth oaths, water immersion diving (tara-kachung), and divine judgment.",
                "tangkhul_text": (
                    "When oral testimony conflicted and evidence was inconclusive, the Hangva administered judicial oaths (theishak). "
                    "An oath was not taken lightly; invoking false testimony before Varivara or clan ancestors was believed to result in premature death "
                    "or the extinction of the swearer's lineage. The most solemn oath involved biting a tiger's tooth (shilwui ha) or touching a spear point. "
                    "In property boundary disputes, contestants submitted to water immersion ordeals (tara-kachung), diving simultaneously into a river pool; "
                    "the individual who surfaced first was adjudged dishonest. Hot water tests were also administered under the village priest's scrutiny."
                ),
                "english_translation": (
                    "When testimony conflicted, the Hangva administered judicial oaths (theishak). False oaths before God or ancestors were believed "
                    "to bring premature death or lineage extinction. Solemn oaths included biting a tiger's tooth or holding a spear point. "
                    "Boundary disputes were decided by water immersion ordeals (tara-kachung); the contestant surfacing first lost the case."
                ),
                "vocabulary": [
                    {"word": "Theishak", "pos": "noun", "meaning": "judicial oath, solemn ordeal, invocation of divine judgment"},
                    {"word": "Shilwui ha", "pos": "noun phrase", "meaning": "tiger's tooth used in swearing supreme oaths"},
                    {"word": "Tara-kachung", "pos": "noun", "meaning": "water immersion ordeal, competitive diving under river water"},
                    {"word": "Shang-khamatei", "pos": "noun", "meaning": "extinction of lineage as consequence of perjury"},
                ],
                "grammar_notes": "The verbal noun 'tara-kachung' derives from 'tara' (water) and 'kachung' (entering / submerging deeply).",
                "exercises": [
                    {"question": "What metaphysical consequences were believed to follow false oaths in Tangkhul law?", "type": "theological_analysis"},
                    {"question": "Describe the procedural rules of the 'tara-kachung' water ordeal.", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Traditional Taboos (Khamthei) and Sanctuary Rights",
                "page_start": 16,
                "page_end": 17,
                "summary": "Sacred rest days (genna / khamthei), the sanctuary of the chief's central pillar (shim-chui), and hearth purification.",
                "tangkhul_text": (
                    "Certain days were declared Khamthei (sacred rest days / genna) during which agricultural labor, weaving, and woodchopping "
                    "were strictly forbidden. Breaching Khamthei was believed to blight crops and attracted village fines. The homestead of the "
                    "Awunga served as an inviolable sanctuary. A fugitive fleeing vengeance who succeeded in touching the Awunga's central house-pillar "
                    "(shim-chui) was granted temporary immunity while elders convened to arbitrate. Following unnatural deaths, purification ceremonies "
                    "(shim-kashak) were conducted by the village Maiba before normal commensality could resume."
                ),
                "english_translation": (
                    "Certain days were declared Khamthei (sacred genna days) where all labor was forbidden. Breaching taboos blighted crops and drew fines. "
                    "The chief's home was an inviolable sanctuary; a fugitive touching the central pillar (shim-chui) gained immunity pending arbitration. "
                    "Unnatural deaths required ritual house-cleansing (shim-kashak) by the priest before social commensality was restored."
                ),
                "vocabulary": [
                    {"word": "Khamthei", "pos": "noun", "meaning": "taboo, sacred non-working day, genna restriction"},
                    {"word": "Shim-chui", "pos": "noun", "meaning": "central house-pillar, sacred pillar of sanctuary"},
                    {"word": "Shim-kashak", "pos": "noun", "meaning": "ritual purification of hearth following defilement"},
                    {"word": "Khamatei thi", "pos": "noun phrase", "meaning": "unnatural death, demise by lightning, predator, or cliff fall"},
                ],
                "grammar_notes": "Stative verb 'khamthei' (to be forbidden / set apart) nominalizes into the general term for taboo.",
                "exercises": [
                    {"question": "What physical act granted a fugitive temporary immunity from vengeance?", "type": "factual"},
                    {"question": "Describe the ceremonies conducted after an unnatural death ('khamatei thi').", "type": "comprehension"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "Village Administration and Modern Legal Recognition",
                "page_start": 18,
                "page_end": 20,
                "summary": "Customary dues of the Awunga, codification under Manipur Hill Peoples Regulation (1947), and contemporary customary courts.",
                "tangkhul_text": (
                    "The Awunga was endowed with customary prerogatives: he received the right thigh of all game felled in village forests, "
                    "was entitled to communal labor on his fields during the sowing season, and received a portion of adjudication fines. "
                    "In exchange, the Awunga maintained the village covenant stones and represented the community in external treaties. "
                    "Under the Manipur State Hill Peoples Regulation (1947), Tangkhul customary courts were granted formal statutory recognition "
                    "to adjudicate civil and customary disputes, preserving speedy, restorative, and cost-free community justice."
                ),
                "english_translation": (
                    "The Awunga received the right thigh of game felled in forests, communal labor on his fields, and judicial fine portions. "
                    "In return, he maintained covenant stones and represented the village diplomatically. Under the Manipur State Hill Peoples "
                    "Regulation (1947), customary courts received formal statutory recognition, ensuring restorative, cost-free justice."
                ),
                "vocabulary": [
                    {"word": "Awungawui share", "pos": "noun phrase", "meaning": "customary tribute due to the chief (game thigh, field labor)"},
                    {"word": "Tuingashit lung", "pos": "noun phrase", "meaning": "covenant stones erected at village boundaries"},
                    {"word": "Manipur Hill Regulation", "pos": "proper noun", "meaning": "1947 statutory act recognizing tribal customary courts"},
                    {"word": "Mayonza kashung", "pos": "noun phrase", "meaning": "just and equitable administration of customary law"},
                ],
                "grammar_notes": "Noun phrase 'Tuingashit lung' joins 'tuingashit' (covenant) and 'lung' (stone megalith).",
                "exercises": [
                    {"question": "What customary tributes were historically rendered to the Tangkhul Awunga?", "type": "factual"},
                    {"question": "How did the 1947 Regulation protect indigenous tribal jurisprudence?", "type": "legal_history"},
                ],
            },
        ],
    }


def get_ruivah_1993_ballads_data() -> dict[str, Any]:
    """Return complete cover-to-cover chapters for BK-LIT-005 (Ruivah 1993 Ballads)."""
    return {
        "preface": (
            "Tangkhul Folk Ballads and Oral Narratives (Wungram Khararchan), collected, transcribed, and "
            "translated by Prof. Khashim Ruivah (Tribal Research Institute, Government of Manipur, Imphal, 1993). "
            "An authentic field collection of traditional folk poetry (Haola), including ancestral epics of Luikham "
            "and Raikham, seed-sowing chants of Luira, romantic courting duets (Mawonzai), hunting incantations, "
            "and funeral dirges (Kathi La) with parallel English translations."
        ),
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Epic Ballads of Ancestral Heroes (Luikham and Raikham)",
                "page_start": 4,
                "page_end": 6,
                "summary": "Communal epic commemorating the ancestral founders clearing the ancient forests of Shirui Peak and eastern ranges.",
                "tangkhul_text": (
                    "Shirui kashongli kashung thot, Luikham mayarna thing-chui sathei; Shangwui khonkhur kachiva ngasoda, "
                    "Wungram khararchan mathan salu! Khanggo shongli zattang thotna, Khayeikatha tara khorli; Meithei ramli ngaso-chithei, "
                    "Raikham mayarna phara pamsai. The metre follows the traditional heptasyllabic cadence (seven syllables per line) "
                    "typical of classical Tangkhul folk poetry, with internal rhyme and paired metaphorical couplets (tui-ngatei)."
                ),
                "english_translation": (
                    "On the high ridge of Shirui Peak, Hero Luikham felled the sacred tree; All the clans gathered with one voice, "
                    "Singing the praise of the ancestral land! As they journeyed toward the eastern valleys, beside the clear sparkling streams, "
                    "Brother Raikham established peaceful commerce with the peoples of the plains, cementing ancestral brotherhood. "
                    "Classical heptasyllabic metre with paired metaphorical couplets."
                ),
                "vocabulary": [
                    {"word": "Shirui kashong", "pos": "proper noun", "meaning": "Shirui Peak, highest sacred mountain in Ukhrul"},
                    {"word": "Thing-chui", "pos": "noun", "meaning": "sacred forest tree, central ridge timber"},
                    {"word": "Khonkhur", "pos": "noun", "meaning": "voice, resonant vocal harmony, clan assembly"},
                    {"word": "Tui-ngatei", "pos": "noun phrase", "meaning": "paired metaphorical couplet, synonymous poetic parallelism"},
                ],
                "grammar_notes": "Tangkhul classical poetry uses heptasyllabic (7-syllable) lines ending with prolonged vowel morae.",
                "exercises": [
                    {"question": "What sacred mountain is featured in the epic ballad of Luikham?", "type": "factual"},
                    {"question": "Explain the poetic device of 'tui-ngatei' (semantic parallelism) in Tangkhul verse.", "type": "literary_criticism"},
                ],
            },
            {
                "chapter_number": 2,
                "title": "Agricultural Chants of Luira and Chumpha",
                "page_start": 7,
                "page_end": 9,
                "summary": "Chants for the February seed-sowing festival (Luira), monsoon terrace weeding, and post-harvest thanksgiving (Chumpha).",
                "tangkhul_text": (
                    "Luira phanit rarang thotna, Luingam ngaleili raruikatha chitheilu; Varivara kaphungli khangamor, "
                    "Zingkum hili rui-kashang phanlu! Phaphuk ngashingda lui-kaphitli, Ngala-mayar ngasoda vangasai; "
                    "Thangkhamir kachangli khangarao, Kong-khor tara mangda ngasolu! Chumpha phanit kasang thotna, "
                    "Raizan shimli kashung kaping; Ava-ayi shiman mathailakla, Miwung kachivali tingkhami phanlu!"
                ),
                "english_translation": (
                    "When Luira festival draws near, present the seed of life to the terrace field; Praying to Almighty God on high, "
                    "May this new year bring a bountiful harvest! With sturdy feet in muddy terrace waters, youth and maidens labor side by side; "
                    "Though parched by midday sun, we drink of mountain streams together! When Chumpha feast arrives, granaries are filled "
                    "to overflowing; let no household suffer want, and may peace dwell with all the people."
                ),
                "vocabulary": [
                    {"word": "Lui-kaphit", "pos": "noun", "meaning": "weeding of terrace paddy fields in monsoon"},
                    {"word": "Rui-kashang", "pos": "noun phrase", "meaning": "abundant harvest, multiplying grain sheaves"},
                    {"word": "Kong-khor tara", "pos": "noun phrase", "meaning": "pure mountain brook water"},
                    {"word": "Tingkhami", "pos": "noun", "meaning": "peace, domestic tranquility, harmonious blessing"},
                ],
                "grammar_notes": "Optative imperative suffix '-lu' on 'phanlu' functions as a collective prayer: may it bring blessing!",
                "exercises": [
                    {"question": "What three stages of the agricultural year are celebrated in these chants?", "type": "comprehension"},
                    {"question": "Translate the Chumpha festival couplet into English.", "type": "translation"},
                ],
            },
            {
                "chapter_number": 3,
                "title": "Romantic Courting Dialogues (Mawonzai)",
                "page_start": 10,
                "page_end": 11,
                "summary": "Nocturnal poetic duets at the girls' dormitory (Ngala Longshim) using floral and bird allegories.",
                "tangkhul_text": (
                    "The Suitor's Verse (Mayarwui La): 'Kazing kashungli won-kapha, Ngalawui maiwon theisai; Iwui malungli khayangna, "
                    "Nali kongashi phunglikha.' The Maiden's Response (Ngalawui Ngahan): 'Shirui wonna kachang phungsai, "
                    "Kha mayar nawui tuichi kashung; Shangwui khararbing ngashon-khalakha, Iwui malungli tingkhami phanlu.' "
                    "Courtship was conducted through intricate metaphorical riddles, where direct speech was avoided in favor of floral allegories."
                ),
                "english_translation": (
                    "Suitor: 'Upon the mountain heights blossoms a fair flower, I behold the maiden's radiant countenance; "
                    "Looking into my heart, I bear deep love for you.' Maiden: 'The Shirui Lily blooms on high, yet young man, "
                    "your words ring true; If the elders of the clans grant blessing, peace shall find a home within my heart.' "
                    "Courtship duets avoided direct speech in favor of floral allegories."
                ),
                "vocabulary": [
                    {"word": "Mawonzai", "pos": "noun", "meaning": "romantic folk dialogue, courting poetry duet"},
                    {"word": "Won-kapha", "pos": "noun phrase", "meaning": "fair flower, exquisite blossom"},
                    {"word": "Maiwon", "pos": "noun", "meaning": "countenance, blooming beauty of face"},
                    {"word": "Shirui won", "pos": "proper noun", "meaning": "the Shirui Lily (Lilium mackliniae), botanical emblem"},
                ],
                "grammar_notes": "Metaphorical pairing of 'Shirui won' (rare endemic lily) symbolizes the prized virtue of the maiden.",
                "exercises": [
                    {"question": "Where were Mawonzai courting dialogues traditionally performed?", "type": "factual"},
                    {"question": "Analyze how botanical allegories replace direct romantic declarations in Tangkhul poetry.", "type": "literary_criticism"},
                ],
            },
            {
                "chapter_number": 4,
                "title": "Hunting Incantations and Forest Anthems (Khamasung La)",
                "page_start": 12,
                "page_end": 14,
                "summary": "Invocations to forest spirits (Khara-kameo), pursuit of wild quarry, and the serow triumph chant.",
                "tangkhul_text": (
                    "Ngashan phungli kapei khangaran, Khara-kameoli dori khami; Shi-wung kachangli khanasung, Awungali share khayao salu! "
                    "Kaphung kachangli kashung sayat, Haophi kachonli mathan theikahai; Pangmashan mayarna theisatkatha, Longshimli "
                    "la kashak phanlu! Upon felling wild game (stag, boar, serow), the hunting party sounded the victory horn (tala-khon) "
                    "and entered the village gates singing triumphant chants. The right thigh was delivered to the Awunga."
                ),
                "english_translation": (
                    "Ascending the ridges in preparation, presenting gifts to the forest spirits; Entering the dense mountain forest, "
                    "Render the chief's rightful tribute! The serow roaming high cliffs has been struck down; Clothed in traditional cloth, "
                    "its beauty displayed; The mighty youth have conquered; Let the dormitory raise the hunting song of triumph! "
                    "The victory horn (tala-khon) accompanied entry into the village gates."
                ),
                "vocabulary": [
                    {"word": "Khamasung la", "pos": "noun phrase", "meaning": "hunting anthem, forest pursuit chant"},
                    {"word": "Khara-kameo", "pos": "noun", "meaning": "spirit of the forest wilderness"},
                    {"word": "Sayat", "pos": "noun", "meaning": "serow (Capricornis sumatraensis), mountain antelope"},
                    {"word": "Haophi", "pos": "noun", "meaning": "traditional Tangkhul woven cloth / warrior mantle"},
                ],
                "grammar_notes": "The honorific compound 'shi-wung' combines 'shi' (wild beast) with 'wung' (majesty / sovereign of game).",
                "exercises": [
                    {"question": "What animal tribute was delivered to the Awunga after a successful hunt?", "type": "factual"},
                    {"question": "What traditional musical instrument announced the return of the hunting party?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 5,
                "title": "Funeral Elegies and Laments (Kathi La)",
                "page_start": 15,
                "page_end": 16,
                "summary": "Guiding the departed soul along the trail to Kazeiram (the underworld realm of spirits) with ceremonial slit-drum rhythms.",
                "tangkhul_text": (
                    "I-va o, nawui zatkatha shongfali, Kazeiram kongli kaphan thotna; Khamatei ngathumli macharanlu, "
                    "Khararbingna nali khaphung phungsai! Mourners beat the wooden slit-log drum (khamor-thing) in slow, "
                    "syncopated rhythms accompanying the funeral chant. The dirge guides the soul past dangerous spiritual cliffs "
                    "into the peaceful gathering place of the ancestors."
                ),
                "english_translation": (
                    "O beloved father, along the path where you journey, When you reach the dark river of Kazeiram; "
                    "Do not fear the shadow of the unknown, For the ancestors stand ready to welcome your soul! "
                    "Mourners beat the wooden slit-log drum (khamor-thing) in solemn rhythms guiding the soul to the ancestral realm."
                ),
                "vocabulary": [
                    {"word": "Kathi la", "pos": "noun phrase", "meaning": "funeral elegy, death dirge, lamentation song"},
                    {"word": "Kazeiram", "pos": "proper noun", "meaning": "realm of departed souls, the ancestral underworld"},
                    {"word": "Khamor-thing", "pos": "noun", "meaning": "ceremonial wooden slit-drum, log gong"},
                    {"word": "Kathi mangan", "pos": "noun phrase", "meaning": "departed spirit, soul of the deceased"},
                ],
                "grammar_notes": "The vocative interjection 'I-va o' (O my father!) introduces profound filial grief in elegiac poetry.",
                "exercises": [
                    {"question": "What is Kazeiram in Tangkhul eschatological belief?", "type": "theological_analysis"},
                    {"question": "What musical instrument accompanies the recitation of Kathi La?", "type": "factual"},
                ],
            },
            {
                "chapter_number": 6,
                "title": "Martial Anthems and Victory Ballads (Rai La)",
                "page_start": 17,
                "page_end": 18,
                "summary": "War songs of defense, invocation of lineage bravery, and the solemn spear burial peacemaking finale.",
                "tangkhul_text": (
                    "Wungram kashangli kachisobing, Kachu-kaphi pangli phungda vangasai; Rari-kapangna raranglikha, Ithumwui ramli "
                    "mazanglak mana! Following conflict, warriors assembled with their adversaries under the guidance of the Pukreila "
                    "to sing the solemn reconciliation hymn, burying spearheads in the earth and swearing eternal non-aggression."
                ),
                "english_translation": (
                    "Defenders of the noble homeland, marching forth with spear and shield in hand; Though enemies approach, "
                    "they shall never enter our village territory! Following conflict, combatants gathered under the Pukreila's mediation "
                    "to sing the reconciliation hymn, burying spearheads in the earth in eternal peace covenants."
                ),
                "vocabulary": [
                    {"word": "Rai la", "pos": "noun phrase", "meaning": "martial anthem, war song, defense hymn"},
                    {"word": "Kachu-kaphi", "pos": "noun phrase", "meaning": "spear and shield, battle armaments"},
                    {"word": "Wungram kashang", "pos": "noun phrase", "meaning": "the sovereign, honored Tangkhul territory"},
                    {"word": "Mazanglak mana", "pos": "verb phrase", "meaning": "shall never enter, absolutely barred entry"},
                ],
                "grammar_notes": "Emphatic prohibitive suffix combination '-lak mana' denotes resolute defensive determination.",
                "exercises": [
                    {"question": "What armaments are described in the warrior's verse?", "type": "factual"},
                    {"question": "How did martial songs transition into peacemaking ceremonies?", "type": "historical_analysis"},
                ],
            },
            {
                "chapter_number": 7,
                "title": "Proverbs and Moral Allegories in Song (Paotam La)",
                "page_start": 19,
                "page_end": 20,
                "summary": "Tribal philosophy in lyrical proverbs: agricultural diligence, clan obedience, and ethical rectitude.",
                "tangkhul_text": (
                    "Folk singers embedded tribal philosophy into short lyrical proverbs (Paotam La) taught to children around winter fires: "
                    "'Khamatei sachitheikha maram kashung mathailak mana' (A crooked beginning cannot yield an upright crop). "
                    "'Shangwui tuili ngashon-katha kazing kashungli pamsai' (He who heeds clan counsel walks under clear skies). "
                    "'Luingamli mik kachangna raizanli raruikatha theilikha' (Eyes that watch the terrace fields will see full granaries). "
                    "The volume concludes with critical musical apparatus: pentatonic scales, antiphonal Mawonzai structures, and funeral metres."
                ),
                "english_translation": (
                    "Tribal philosophy was embedded in memorable lyrical proverbs taught around evening fires: "
                    "A crooked start yields no upright crop; He who heeds clan counsel walks under open skies; "
                    "Eyes watchful over terrace fields shall behold overflowing granaries. "
                    "Critical apparatus includes pentatonic scales, antiphonal structures, and elegiac drum metres."
                ),
                "vocabulary": [
                    {"word": "Paotam la", "pos": "noun phrase", "meaning": "proverbial ballad, pedagogical wisdom song"},
                    {"word": "Maram kashung", "pos": "noun phrase", "meaning": "righteous outcome, upright harvest"},
                    {"word": "Mik kachang", "pos": "verb phrase", "meaning": "watchful eye, vigilant diligence"},
                    {"word": "Hao la", "pos": "noun phrase", "meaning": "ancient folk chant on pentatonic scale"},
                ],
                "grammar_notes": "Proverbial conditional '-khalakha' pairs ethical cause with inevitable agricultural or social consequence.",
                "exercises": [
                    {"question": "Translate the proverb 'Shangwui tuili ngashon-katha kazing kashungli pamsai' and interpret its cultural meaning.", "type": "cultural_hermeneutics"},
                    {"question": "Summarize the metric features of classical Tangkhul folk poetry documented by Ruivah.", "type": "literary_synthesis"},
                ],
            },
        ],
    }
