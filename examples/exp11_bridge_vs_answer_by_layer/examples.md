# Examples: exp11_bridge_vs_answer_by_layer (last token, trailing space stripped), Qwen3.6-27B

Source run `results/exp11_bridge_vs_answer_by_layer/20261015-100110`, model Qwen/Qwen3.6-27B. Examples are drawn at random with seed 0, up to 3 per group; groups can overlap. Marks in the tables: **bridge**, *answer*, [distractor]. Ranks are word ranks (1 = top; spaces and punctuation removed) of the bridge (B) and the answer (A). Readers: logit lens (baseline), J-lens, J++.

| Group | Definition | Items in group | Shown |
|---|---|---|---|
| [Seen at the last token](#seen_last) | Answered correctly; the J-lens has the bridge ranked first among the entities in >= 50% of layers 32-48 at the last token. | 47 | 3 |
| [Missed at the last token](#missed_last) | Answered correctly; the J-lens has the bridge ranked first among the entities in < 50% of layers 32-48 at the last token. | 30 | 3 |
| [Distractor above the bridge](#distractor_wins) | Answered correctly; the same-category distractor is ranked first among the entities in more band layers than the bridge. | 6 | 3 |
| [J-lens and J++ disagree](#readers_disagree) | Answered correctly; the two lenses' band shares for the bridge differ by >= 0.5. | 1 | 1 |
| [Model answers wrong](#model_wrong) | The model does not give the answer. Does the lens still see the bridge? | 13 | 3 |

<a id="seen_last"></a>
## Seen at the last token

Answered correctly; the J-lens has the bridge ranked first among the entities in >= 50% of layers 32-48 at the last token.

### `ex2-city-language-Cairo`

> Fact: The language spoken in the country where Cairo is located is

Cue phrase: "Cairo"

Bridge **Egypt** -> answer *Arabic*; controls [Russia] / [Russian]. category: city-language, model answers correctly: yes, swapping flips the answer: the J-space part, model's top word: Arabic.
Why this group: J-lens bridge ranked first among the entities in 100% of band layers at the last token, distractor 0%; J++ 100%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/ex2-city-language-Cairo__jlens.html) · [J++](slices/ex2-city-language-Cairo__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, 1 | –and, The, It, the, For | <unk, Counseling, Connecticut, <data, -www | 25824 / 20281 · 8562 / 25366 · 88417 / 87565 |
| 4 | a, T, S, S, T | 专栏收录该内容, 률은, 률, 港币, 认认真 | OpenGL, _php, europé, 优秀共产党员, _SDK | 25783 / 24607 · 148043 / 15932 · 221055 / 2142 |
| 8 | a, s, t, S, b | ´t, avour, 学金, Busty, VERY | 语言, languages, language, _languages, languages | 70481 / 27235 · 186500 / 1849 · 107607 / 6 |
| 12 | s, b, a, t, b | nowadays, 砼, favour, whilst, ´t | Language, 国语, ISA, IS, CIS | 77936 / 39125 · 41006 / 306 · 41293 / 17 |
| 16 | b, S, S, B, M | basically, nowadays, very, also, actually | ISA, CIS, IS, Language, Israel | 76454 / 20791 · 10330 / 430 · 32022 / 278 |
| 20 | b, predominantly, languages, IT, flu | basically, actually, also, nowadays, generally | language, languages, country, countries, foreign | 126412 / 30027 · 1235 / 50 · 162 / 300 |
| 24 | predominantly, b, v, a, M | *Arabic*, countries, English, Islam, Muslim | countries, country, foreign, *Arabic*, language | 50652 / 33116 · 9 / 1 · 7 / 4 |
| 28 | M, (s, a, S, U | *Arabic*, English, countries, Islam, Muslim | country, countries, national, *Arabic*, nationality | 95530 / 17243 · 14 / 1 · 15 / 4 |
| 32 | (s, U, to, N, a | 什么, 什么意思, 是什么意思, <u, 是什么 | country, countries, Country, ethnic, nationality | 54310 / 16273 · 86 / 7 · 12 / 10 |
| 36 | primarily, 该国, predominantly, (s, dominant | *Arabic*, 什么, 语言, English, 什么意思 | country, countries, language, nationality, *Arabic* | 78784 / 7448 · 30 / 1 · 6 / 5 |
| 40 | language, languages, (s, language, 该国 | *Arabic*, Egyptian, languages, Urdu, Arab | *Arabic*, language, English, Egyptian, languages | 6626 / 44 · 11 / 1 · 11 / 1 |
| 44 | (s, primarily, predominantly, 该国, predominant | *Arabic*, languages, Urdu, Arab, Egyptian | *Arabic*, Egyptian, language, languages, country | 3208 / 148 · 16 / 1 · 8 / 1 |
| 48 | primarily, 叫做, (s, predominantly, called | *Arabic*, languages, Arab, Urdu, Islam | *Arabic*, language, languages, lingua, Egyptian | 19055 / 690 · 20 / 1 · 14 / 1 |
| 52 | primarily, predominantly, spoken, lingua, mainly | *Arabic*, Language, Languages, languages, language | *Arabic*, language, Egyptian, arab, Cairo | 13223 / 15 · 36 / 1 · 11 / 1 |
| 56 | *Arabic*, primarily, predominantly, mainly, mostly | *Arabic*, Egyptian, Arab, arab, English | *Arabic*, Egyptian, 埃及, arab, Cairo | 31 / 1 · 8 / 1 · 6 / 1 |
| 60 | *Arabic*, primarily, Arab, Egyptian, arab | *Arabic*, Arab, Egyptian, arab, Arabian | *Arabic*, Egyptian, arab, Arab, 埃及 | 21 / 1 · 7 / 1 · 7 / 1 |
| 62 | *Arabic*, primarily, Egyptian, called, predominantly | *Arabic*, Arab, Egyptian, arab, spoken | *Arabic*, Arab, Egyptian, arab, primarily | 36 / 1 · 14 / 1 · 37 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `in` | 专栏收录该内容 (233289) | the (7669) | languages (2573) | countries (448) | countries (281) | countries (103) | India (53) | India (41) |
| `the` | 五颜六色的 (161440) | of (11189) | many (2557) | British (418) | countries (194) | countries (262) | country (521) | United (2360) |
| `country` | 's (616) | 's (185) | countries (90) | countries (94) | countries (85) | countries (54) | Argentina (56) | of (67) |
| `where` | 最新发布 (143456) | 最新发布 (12179) | countries (381) | Country (182) | Country (174) | countries (120) | Barack (802) | the (756) |
| `Cairo` (cue) | Cairo (2) | Cairo (2) | Cairo (2) | Cairo (3) | Cairo (3) | Cairo (2) | Cairo (2) | is (21) |
| `is` | ´s (100320) | ´s (20222) | city (13) | <u (116) | cities (290) | located (110) | located (344) | located (38) |
| `located` | .The (10079) | in (2837) | **Egypt** (1) | 是什么意思 (6) | **Egypt** (1) | is (2) | is (2) | is (4) |
| `is` | ´t (186491) | basically (10329) | *Arabic* (9) | 什么 (86) | *Arabic* (11) | *Arabic* (22) | *Arabic* (8) | *Arabic* (14) |

### `ex2-language-capital-Swedish`

> Fact: The capital of the country where Swedish is the primary language is

Cue phrase: "Swedish is the primary language"

Bridge **Sweden** -> answer *Stockholm*; controls [Hungary] / [Budapest]. category: language-capital, model answers correctly: yes, swapping flips the answer: the J-space part, model's top word: Stockholm.
Why this group: J-lens bridge ranked first among the entities in 88% of band layers at the last token, distractor 0%; J++ 82%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/ex2-language-capital-Swedish__jlens.html) · [J++](slices/ex2-language-capital-Swedish__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, P | The, –and, It, For, the | <unk, <b, <data, Connecticut, \xc | 38441 / 41439 · 52553 / 48429 · 18759 / 79320 |
| 4 | S, s, a, T, S | 专栏收录该内容, (IS, 认认真, Краси, 률은 | OpenGL, Ураль, _SDK, 优秀共产党员, Airport | 38195 / 16350 · 149553 / 101935 · 97278 / 19310 |
| 8 | S, H, T, a, S | ustralian, pornstar, Shemale, ilian, inerary | 周杰伦, 绵阳, _SDK, Airport, Reuters | 46268 / 29054 · 176882 / 21778 · 109099 / 17726 |
| 12 | B, M, s, B, b | ёл, also, therefore, colour, 砼 | city, Capitals, cities, capitals, City | 53479 / 10072 · 17992 / 6919 · 73968 / 7374 |
| 16 | B, M, R, F, U | also, basically, actually, only, amongst | CIS, Canada, Capital, Sovere, City | 32971 / 17725 · 7182 / 9387 · 4390 / 2796 |
| 20 | b, T, M, itom, 且 | actually, nonetheless, indeed, also, 这座城市 | cities, city, capitals, countries, country | 32676 / 39548 · 7020 / 11898 · 12478 / 12478 |
| 24 | M, M, T, b, G | cities, countries, city, country, Canada | cities, city, country, countries, north | 80565 / 62249 · 3768 / 4680 · 3740 / 9209 |
| 28 | M, M, (s, either, b | countries, cities, country, UNESCO, city | country, city, cities, countries, Country | 65056 / 72541 · 824 / 1206 · 8488 / 9171 |
| 32 | (s, U, ellite, ind, M | 什么意思, 是什么意思, 什么, 是什么, UNESCO | country, countries, cities, city, Country | 47399 / 26658 · 1470 / 1823 · 2405 / 4621 |
| 36 | U, 所在, M, Y, entin | 瑞典, **Sweden**, Scandinavian, Swedish, Finland | Swedish, **Sweden**, 瑞典, Scandinavian, *Stockholm* | 1929 / 1159 · 2 / 11 · 2 / 5 |
| 40 | borg, o, M, 瑞典, 国 | **Sweden**, 瑞典, *Stockholm*, Swedish, Scandinavian | Swedish, **Sweden**, *Stockholm*, 瑞典, Scandinavian | 69 / 128 · 1 / 3 · 2 / 3 |
| 44 | (s, IT, o, G, located | *Stockholm*, **Sweden**, 瑞典, Finland, Sweden | Swedish, *Stockholm*, **Sweden**, Scandinavian, 瑞典 | 262 / 262 · 2 / 1 · 3 / 2 |
| 48 | NOT, 叫做, unta, not, located | **Sweden**, *Stockholm*, Finland, 瑞典, Sweden | **Sweden**, 瑞典, *Stockholm*, Swedish, Finland | 21 / 144 · 2 / 2 · 1 / 4 |
| 52 | *Stockholm*, capital, 瑞典, located, called | *Stockholm*, **Sweden**, Helsinki, Oslo, Swedish | Swedish, 瑞典, *Stockholm*, **Sweden**, Sweden | 6 / 1 · 2 / 1 · 4 / 3 |
| 56 | *Stockholm*, **Sweden**, 瑞典, Swedish, Sweden | *Stockholm*, **Sweden**, Oslo, Swedish, 瑞典 | *Stockholm*, 瑞典, Swedish, **Sweden**, Sweden | 2 / 1 · 2 / 1 · 4 / 1 |
| 60 | *Stockholm*, Stock, Stock, 斯, Сто | *Stockholm*, **Sweden**, Oslo, Stock, Stock | *Stockholm*, **Sweden**, Swedish, 瑞典, Oslo | 22 / 1 · 2 / 1 · 2 / 1 |
| 62 | *Stockholm*, Stock, Stock, stock, not | *Stockholm*, Stock, Stock, STOCK, stock | *Stockholm*, Stock, Stock, STOCK, stock | 34 / 1 · 11 / 1 · 14 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `country` | 's (4609) | countries (2634) | countries (145) | countries (133) | countries (81) | countries (89) | where (22) | is (51) |
| `where` | 最新发布 (120911) | 最新发布 (33934) | countries (238) | Country (216) | Country (134) | Country (169) | Mount (3981) | Mount (2674) |
| `Swedish` (cue) | 瑞典 (22) | Swedish (7) | Swedish (3) | Swedish (3) | Swedish (7) | Swedish (4) | Swedish (3) | is (66) |
| `is` (cue) | colour (73665) | really (3872) | Swedish (4) | 瑞典 (10) | languages (130) | language (69) | spoken (938) | spoken (301) |
| `the` (cue) | ighbour (161188) | ´t (50873) | lingua (2051) | 什么 (16202) | 语言 (1416) | primary (1756) | official (5013) | official (4221) |
| `primary` (cue) | ulatory (237895) | utilizing (225492) | language (14023) | language (11700) | language (1494) | language (1503) | language (46631) | language (9329) |
| `language` (cue) | .L (4527) | in (3204) | Swedish (2) | 是什么意思 (19) | 瑞典 (3) | **Sweden** (1) | **Sweden** (1) | is (6) |
| `is` | ustralian (176808) | also (7179) | cities (3772) | 什么意思 (1470) | **Sweden** (1) | **Sweden** (1) | *Stockholm* (2) | *Stockholm* (11) |

### `person-firstname-shakespeare`

> Fact: The first name of the playwright who wrote Romeo and Juliet was

Cue phrase: "playwright who wrote Romeo and Juliet"

Bridge **Shakespeare** -> answer *William*; controls [Mozart] / [Wolfgang]. category: person-firstname, model answers correctly: yes, swapping flips the answer: neither part, model's top word: William.
Why this group: J-lens bridge ranked first among the entities in 100% of band layers at the last token, distractor 0%; J++ 100%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/person-firstname-shakespeare__jlens.html) · [J++](slices/person-firstname-shakespeare__jpp.html)

**Last token** `was`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, T, S | er, –and, en, u, o | <unk, Inglés, 就像一个, -toolbar, -www | 21979 / 7857 · 31686 / 673 · 11449 / 117847 |
| 4 | a, S, s, P, P | er, ’t, هى, трёх, 砼 | _php, _mysql, MySQL, 碧, 西班牙语 | 23182 / 9812 · 41564 / 36431 · 52154 / 65031 |
| 8 | l, A, l, A, a | Colour, colour, 的, Colour, ёл | 威尼斯, 苗木, 状元, TPL, _sentence | 8962 / 13742 · 44298 / 14569 · 884 / 59823 |
| 12 | A, s, S, l, B | colour, favourite, colour, favour, Colour | WAS, Alexandra, Australian, fame, famous | 16335 / 27960 · 566 / 282 · 109 / 280 |
| 16 | B, b, a, un, s | amongst, 1, though, 2, l | History, WAS, FA, First, the | 46285 / 28350 · 701 / 346 · 85 / 90 |
| 20 | name, P, udge, S, y | Actually, actually, <b, name, What | names, name, the, Alexandria, and | 22499 / 34159 · 924 / 131 · 63 / 3637 |
| 24 | name, names, Name, 不详, s | name, famously, *William*, name, actually | names, name, Name, named, Names | 14006 / 21321 · 27 / 3 · 47 / 302 |
| 28 | F, L, C, L, F | famous, famously, *William*, name, John | name, names, nickname, father, Name | 25862 / 10280 · 8 / 4 · 13 / 70 |
| 32 | g, born, op, IP, X | famous, Famous, <u, famously, name | name, names, Name, surname, famous | 15862 / 43839 · 8 / 12 · 7 / 42 |
| 36 | name, names, X, name, 名字 | Name, Famous, name, *William*, name | name, names, Name, famous, Names | 36196 / 28991 · 15 / 5 · 8 / 23 |
| 40 | name, name, 名字, /name, names | name, 名字, Name, name, /name | name, names, surname, Name, named | 10376 / 7234 · 26 / 22 · 24 / 38 |
| 44 | G, L, A, \n, b | /name, 名字, Name, 姓名, surname | name, surname, names, 姓氏, urname | 14291 / 7225 · 28 / 14 · 26 / 16 |
| 48 | L, 什么, H, /is, <u | <u, 叫什么, *William*, 名字, 姓 | 姓氏, surname, 姓, 原名, name | 3814 / 9705 · 14 / 3 · 7 / 27 |
| 52 | /is, **Shakespeare**, genius, actually, 什么 | **Shakespeare**, *William*, Richard, Christopher, Robert | **Shakespeare**, 莎士比亚, genius, poet, 才子 | 2 / 973 · 1 / 2 · 1 / 20 |
| 56 | **Shakespeare**, playwright, 莎士比亚, 剧团, theatre | **Shakespeare**, Romeo, playwright, 莎士, *William* | **Shakespeare**, playwright, 莎士比亚, theatre, Romeo | 1 / 246 · 1 / 5 · 1 / 30 |
| 60 | *William*, 威廉, *William*, **Shakespeare**, WILL | *William*, *William*, 威廉, **Shakespeare**, WILL | *William*, **Shakespeare**, *William*, 威廉, Shakespe | 4 / 1 · 4 / 1 · 2 / 1 |
| 62 | *William*, W, Will, **Shakespeare**, *William* | *William*, **Shakespeare**, Will, WILL, Wil | *William*, *William*, **Shakespeare**, WILL, _W | 4 / 1 · 2 / 1 · 3 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `the` | Them (4385) | of (2581) | people (489) | famous (225) | famous (22) | famous (100) | president (345) | person (658) |
| `playwright` (cue) | s (1335) | s (175) | s (3) | playwright (2) | playwright (2) | playwright (2) | playwright (2) | Arthur (4) |
| `who` (cue) | ‘s (2617) | ‘s (91) | whom (37) | Famous (2) | **Shakespeare** (1) | famous (2) | wrote (91) | wrote (272) |
| `wrote` (cue) | ся (208) | Writer (27) | Writer (2) | books (2) | **Shakespeare** (1) | **Shakespeare** (1) | Ham (5) | The (9) |
| `Romeo` (cue) | Romeo (29) | Romeo (5) | Romeo (3) | Romeo (2) | Romeo (2) | Romeo (2) | Romeo (8) | and (27) |
| `and` (cue) | -old (314) | amongst (240) | **Shakespeare** (1) | **Shakespeare** (1) | **Shakespeare** (1) | **Shakespeare** (1) | Romeo (4) | Juliet (15) |
| `Juliet` (cue) | an (57) | an (32) | **Shakespeare** (2) | **Shakespeare** (1) | **Shakespeare** (1) | **Shakespeare** (1) | was (3) | is (3) |
| `was` | Colour (44296) | amongst (682) | name (27) | famous (8) | name (26) | <u (15) | **Shakespeare** (1) | *William* (2) |


<a id="missed_last"></a>
## Missed at the last token

Answered correctly; the J-lens has the bridge ranked first among the entities in < 50% of layers 32-48 at the last token.

### `holiday-month-christmas2`

> Fact: The month of the holiday celebrated with a decorated evergreen tree and gift-giving is

Cue phrase: "holiday celebrated with a decorated evergreen tree and gift-giving"

Bridge **Christmas** -> answer *December*; controls [Easter] / [April]. category: holiday-month, model answers correctly: yes, swapping flips the answer: neither part, model's top word: December.
Why this group: J-lens bridge ranked first among the entities in 29% of band layers at the last token, distractor 0%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/holiday-month-christmas2__jlens.html) · [J++](slices/holiday-month-christmas2__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, s, S, A | –and, The, It, For, the | <unk, \xc, Connecticut, <data, -www | 14980 / 10004 · 7105 / 21029 · 12733 / 59489 |
| 4 | a, T, T, S, P | 률은, 专栏收录该内容, 률, 认认真, 률이 | OpenGL, Wichita, Birmingham, _php, _SDK | 19470 / 12117 · 205170 / 192540 · 2429 / 14055 |
| 8 | P, H, B, H, M | 률은, uréat, ilian, 大金, quel | Wichita, 德州, Arizona, _SDK, Arkansas | 33901 / 16886 · 235247 / 129001 · 4316 / 127 |
| 12 | B, B, u, b, M | surely, idencia, 广大的, presently, 清楚的 | Kais, Oz, AZ, Bris, 吉斯 | 23318 / 17045 · 208656 / 88094 · 1026 / 956 |
| 16 | nam, R, M, R, B | Though, folks, neighbor, –and, truly | CIS, Wisconsin, Washington, 吉斯, Season | 10450 / 9992 · 118456 / 14342 · 635 / 1032 |
| 20 | M, F, T, R, otope | 什么, 哪, —that, 那一, 哪一个 | months, year, month, season, Kansas | 34695 / 12946 · 124289 / 565 · 201 / 13 |
| 24 | M, F, T, R, S | —that, 什么, —which, —even, 哪一个 | season, year, month, months, annually | 13017 / 5409 · 11777 / 79 · 57 / 6 |
| 28 | M, M, anim, F, (s | —that, —but, —which, —and, —even | year, March, season, the, month | 12861 / 6024 · 79 / 88 · 120 / 8 |
| 32 | M, U, enda, X, also | 什么, 什么意思, 是什么, 是什么意思, 请问 | year, season, Year, the, also | 1749 / 24802 · 378 / 475 · 20 / 11 |
| 36 | also, calendar, M, ли, indeed | year, **Christmas**, month, winter, *December* | *December*, winter, year, November, month | 1578 / 698 · 2 / 5 · 16 / 1 |
| 40 | also, M, indeed, calendar, 尽 | month, *December*, Month, winter, January | month, *December*, winter, November, January | 2773 / 128 · 10 / 2 · 17 / 2 |
| 44 | M, not, 叫做, also, 1 | month, Month, *December*, winter, January | month, *December*, winter, months, year | 19842 / 1397 · 15 / 3 · 20 / 2 |
| 48 | not, 叫做, NOT, nam, also | month, *December*, Month, November, January | month, *December*, calendar, winter, Month | 36482 / 491 · 13 / 2 · 16 / 2 |
| 52 | typically, preceded, often, months, usually | *December*, month, January, October, November | month, Month, *December*, winter, November | 53253 / 31 · 23 / 1 · 16 / 3 |
| 56 | *December*, *December*, January, typically, preceded | *December*, January, November, *December*, February | *December*, *December*, January, November, February | 710 / 1 · 17 / 1 · 19 / 1 |
| 60 | *December*, *December*, Dec, .Dec, Dec | *December*, *December*, Dec, *december*, November | *December*, *December*, *december*, Dec, called | 77 / 1 · 9 / 1 · 8 / 1 |
| 62 | *December*, *December*, Dec, the, typically | *December*, Dec, *december*, *December*, January | *December*, *December*, known, *december*, called | 52 / 1 · 13 / 1 · 111 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `ever` (cue) | 我 (210421) | l (177487) | trees (1183) | 树 (436) | trees (32) | trees (50) | tree (91) | green (208) |
| `green` (cue) | pine (37) | hardwood (629) | trees (4) | **Christmas** (1) | **Christmas** (1) | **Christmas** (1) | tree (56) | tree (24) |
| `tree` (cue) | famous (8) | Tree (18) | **Christmas** (1) | **Christmas** (1) | **Christmas** (1) | is (2) | is (4) | is (97) |
| `and` (cue) | 大金 (142382) | well (7349) | **Christmas** (1) | 什么 (8) | **Christmas** (1) | **Christmas** (1) | gifts (10) | gifts (23) |
| `gift` (cue) | gift (6600) | gift (5080) | gift (7) | gift (11) | gifts (9) | gifts (13) | gifts (145) | -g (1194) |
| `-g` (cue) | ing (10637) | ing (9426) | ing (19) | gift (13) | Christmas (5) | gifts (18) | traditions (13) | iving (148) |
| `iving` (cue) | gifts (2986) | toward (5665) | Christmas (2) | **Christmas** (1) | **Christmas** (1) | **Christmas** (1) | is (11) | is (78) |
| `is` | 률은 (235251) | Though (118466) | —that (11770) | 什么 (379) | month (10) | month (13) | *December* (17) | *December* (13) |

### `month-3-godof`

> Fact: The third month of the year is named after the Roman god of

Cue phrase: "third month of the year"

Bridge **Mars** -> answer *war*; controls [Venus] / [love]. category: multihop, model answers correctly: yes, swapping flips the answer: neither part, model's top word: war.
Why this group: J-lens bridge ranked first among the entities in 6% of band layers at the last token, distractor 0%; J++ 18%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/month-3-godof__jlens.html) · [J++](slices/month-3-godof__jpp.html)

**Last token** `of`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, I, and, S | –and, a, the, The, or | people, niest, everyone, Truman, itian | 11500 / 3284 · 19404 / 271 · 78538 / 82346 |
| 4 | 1, and, p, a, S | @g, Guta, 芷, bed, @d | goddess, 女神, _legend, gods, 神 | 3639 / 2894 · 93588 / 18664 · 132019 / 88508 |
| 8 | p, c, P, M, C | -E, -W, …I, -g, -L | gods, goddess, mythology, 神话, 祭祀 | 1726 / 3310 · 406 / 1241 · 8130 / 61551 |
| 12 | P, s, i, c, p | land, religion, ness, ding, gods | gods, goddess, Gods, mythology, Goddess | 2447 / 4996 · 664 / 56 · 1242 / 194 |
| 16 | B, P, D, g, s | -esque, god, idol, gods, fighting | Gods, mythology, gods, God, and | 30333 / 4089 · 25605 / 20 · 3892 / 69 |
| 20 | d, 示, g, Apollo, ose | god, d, gods, idol, God | Rome, Roman, gods, 罗马, goddess | 462 / 7559 · 1557 / 25 · 83 / 171 |
| 24 | o, 三, g, P, 一手 | gods, god, Roman, Rome, worship | Roman, Rome, Latin, Romans, Saturn | 4517 / 85 · 240 / 58 · 49 / 88 |
| 28 | c, P, g, 草, C | gods, mythology, god, deity, worship | Roman, Rome, Gods, deity, gods | 4618 / 1204 · 112 / 188 · 14 / 105 |
| 32 | c, P, g, 性, M | gods, uranus, mythology, deity, god | Roman, Rome, Gods, mythology, gods | 5820 / 6898 · 335 / 1622 · 9 / 107 |
| 36 | itos, g, 掌管, 监察, axy | Zeus, gods, Apollo, 罗马, Rome | Roman, Rome, 罗马, рим, Roman | 2539 / 727 · 30 / 404 · 13 / 102 |
| 40 | 掌管, oso, sky, acia, yno | gods, Zeus, Apollo, goddess, deity | Roman, Jupiter, Saturn, Rome, [Venus] | 784 / 4179 · 24 / 620 · 14 / 36 |
| 44 | T, g, 占, S, V | gods, earthly, underworld, deity, god | Roman, healing, weather, ancient, Earth | 155 / 1178 · 42 / 286 · 6 / 36 |
| 48 | T, S, N, N, V | gods, /weather, deity, healing, earthly | healing, gods, deity, mythology, weather | 1051 / 259 · 68 / 460 · 20 / 127 |
| 52 | 什么的, 瓮, 农业, g, 俊 | gods, agriculture, underworld, **Mars**, agriculture | Jupiter, **Mars**, [Venus], Saturn, Rome | 256 / 36 · 4 / 185 · 2 / 41 |
| 56 | *war*, 地下, underworld, 什么的, 战争 | underworld, agriculture, *war*, warfare, underground | *war*, Rome, underworld, underground, 罗马 | 429 / 1 · 126 / 3 · 21 / 1 |
| 60 | *war*, spring, *War*, springs, 战争 | *war*, agriculture, gates, wars, warfare | *war*, spring, *War*, *war*, gates | 152 / 1 · 80 / 1 · 12 / 1 |
| 62 | *war*, the, *War*, spring, agriculture | *war*, agriculture, gates, doors, wars | *war*, agriculture, warfare, wars, gates | 56 / 1 · 119 / 1 · 401 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `year` (cue) | 's (461) | in (2556) | year (2258) | January (1331) | month (3654) | year (4441) | is (446) | is (82) |
| `is` | therefore (22) | just (9243) | perhaps (2565) | <u (732) | month (820) | month (835) | March (229) | March (8) |
| `named` | ighbor (37953) | –and (24653) | because (2401) | <u (1196) | 命名 (912) | named (692) | after (80) | March (3) |
| `after` | ments (11351) | er (10557) | Roman (817) | 什么 (605) | Roman (74) | goddess (59) | March (2) | **Mars** (1) |
| `the` | .L (259) | o (16557) | March (98) | 什么 (74) | Roman (58) | Latin (159) | Roman (13) | Roman (17) |
| `Roman` | Roman (95) | Roman (2410) | Roman (427) | Roman (529) | Roman (176) | Roman (366) | goddess (63) | goddess (74) |
| `god` | ness (583) | god (755) | god (151) | god (92) | gods (77) | <u (121) | **Mars** (2) | **Mars** (1) |
| `of` | -E (416) | -esque (25605) | gods (240) | gods (335) | gods (24) | gods (69) | underworld (126) | *war* (119) |

### `person-country-napoleon`

> Fact: The country whose army was led by the emperor defeated at Waterloo is

Cue phrase: "emperor defeated at Waterloo"

Bridge **Napoleon** -> answer *France*; controls [Lincoln] / [America]. category: person-country, model answers correctly: yes, swapping flips the answer: neither part, model's top word: France.
Why this group: J-lens bridge ranked first among the entities in 0% of band layers at the last token, distractor 0%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/person-country-napoleon__jlens.html) · [J++](slices/person-country-napoleon__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, P | –and, The, It, For, the | <unk, \xc, <b, <data, ermen | 31272 / 9404 · 16083 / 4803 · 1099 / 3770 |
| 4 | a, T, S, T, V | 专栏收录该内容, 률은, Hidal, 률, 港币 | OpenGL, ーブ, Opera, 文艺演出, jni | 74393 / 9942 · 174433 / 47442 · 77533 / 6617 |
| 8 | a, H, u, B, f | avour, uréat, VERY, américa, ilename | 巴黎, 法国, ébastien, _countries, countries | 48713 / 5384 · 173009 / 1086 · 2239 / 55 |
| 12 | a, b, the, f, v | 砼, ёл, avourite, avour, Whilst | *France*, country, Paris, Country, countries | 50837 / 7349 · 104362 / 3899 · 118 / 1 |
| 16 | M, b, B, B, G | amongst, notably, –and, arguably, Whilst | London, Britann, Britain, British, Paris | 93254 / 5260 · 92662 / 824 · 21 / 18 |
| 20 | erne, 邻, m, U, w | Britain, 什么, whose, chiefly, 同样 | country, *France*, countries, French, England | 40500 / 1506 · 83346 / 42 · 8 / 2 |
| 24 | anim, 亡, erne, now, 的那个 | 什么, Britain, \uff, <u, <b | French, *France*, European, country, British | 50741 / 1402 · 13588 / 10 · 8 / 2 |
| 28 | B, anim, 亡, \n, m | 什么, Britain, 哪一个, famously, 哪 | *France*, French, country, British, European | 67256 / 12988 · 203 / 10 · 9 / 1 |
| 32 | A, U, B, 亡, 噜 | 什么, 什么意思, 是什么, 请问, 哪个 | British, French, *France*, country, England | 87818 / 23180 · 1225 / 186 · 7 / 3 |
| 36 | 亡, U, ident, still, 陷 | *France*, Britain, 英国, 法国, French | French, *France*, **Napoleon**, British, 法国 | 23380 / 7849 · 11 / 1 · 3 / 2 |
| 40 | still, 亡, also, U, so | *France*, French, *France*, 法国, Britain | French, *France*, British, European, **Napoleon** | 1781 / 187 · 8 / 1 · 5 / 2 |
| 44 | a, U, G, \n, 1 | *France*, French, *France*, 法国, French | French, *France*, British, European, country | 10137 / 2062 · 9 / 1 · 11 / 2 |
| 48 | NOT, amas, nam, hereby, ox | *France*, French, *France*, 法国, Germany | French, *France*, European, German, British | 27213 / 5259 · 13 / 1 · 12 / 2 |
| 52 | located, 位于, also, /w, NOT | *France*, French, Belgium, Germany, *France* | *France*, French, 法国, Belgium, Germany | 5994 / 91 · 27 / 1 · 31 / 1 |
| 56 | known, now, currently, *France*, located | *France*, Germany, Belgium, *France*, French | *France*, French, 法国, *France*, Germany | 120 / 4 · 33 / 1 · 66 / 1 |
| 60 | *France*, known, *France*, located, 法国 | *France*, *France*, Belgium, Germany, French | *France*, *France*, French, 法国, *france* | 57 / 1 · 24 / 1 · 57 / 1 |
| 62 | *France*, known, now, not, located | *France*, Belgium, Germany, known, Austria | *France*, known, *France*, Belgium, now | 97 / 1 · 22 / 1 · 66 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `led` | 莱德 (200829) | 专栏收录该内容 (34927) | commander (511) | commander (63) | commander (111) | commander (39) | by (8) | by (14) |
| `by` | King (1323) | King (386) | military (47) | military (15) | military (8) | **Napoleon** (1) | **Napoleon** (1) | General (2) |
| `the` | ­t (36339) | of (5480) | whom (1043) | famous (341) | President (13) | famous (6) | commander (16) | Duke (53) |
| `emperor` (cue) | emperor (32) | emperor (13) | emperor (4) | emperor (3) | emperor (5) | emperor (3) | **Napoleon** (1) | **Napoleon** (1) |
| `defeated` (cue) | 貅 (30835) | 貅 (7272) | ussia (1073) | 的 (646) | defeated (147) | defeated (41) | Germany (7) | the (5) |
| `at` (cue) | ting (237099) | ting (128958) | Though (3559) | 失败 (439) | defeat (15) | Battle (4) | Battle (3) | least (66) |
| `Waterloo` (cue) | Waterloo (18984) | Waterloo (440) | Waterloo (3) | Waterloo (2) | **Napoleon** (1) | **Napoleon** (1) | was (18) | was (12) |
| `is` | avour (173005) | amongst (92667) | 什么 (13578) | 什么 (1227) | *France* (8) | *France* (13) | *France* (33) | *France* (22) |


<a id="distractor_wins"></a>
## Distractor above the bridge

Answered correctly; the same-category distractor is ranked first among the entities in more band layers than the bridge.

### `ex-element-state-26-80`

> Fact: The state of matter at room temperature of the element with atomic number 26 is

Cue phrase: "element with atomic number 26"

Bridge **iron** -> answer *solid*; controls [mercury] / [liquid]. category: element-state, model answers correctly: yes, swapping flips the answer: neither part, model's top word: solid.
Why this group: J-lens bridge ranked first among the entities in 0% of band layers at the last token, distractor 18%; J++ 29%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/ex-element-state-26-80__jlens.html) · [J++](slices/ex-element-state-26-80__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, T, S | –and, The, It, the, For | <unk, \xc, Connecticut, Counseling, <b | 17920 / 781 · 15538 / 2800 · 77881 / 12436 |
| 4 | a, S, S, n, A | amente, 률은, 港币, きっ, 港台 | OpenGL, 孔雀, 仙人掌, _SDK, Phoenix | 4153 / 525 · 105881 / 34057 · 223177 / 52066 |
| 8 | S, S, s, a, T | avour, colour, ilian, amente, ély | 海口, additionally, furthermore, _LOCK, also | 9299 / 730 · 188590 / 5786 · 59849 / 3314 |
| 12 | S, S, s, A, B | nevertheless, 砼, furthermore, avour, favour | AIS, BIS, Eis, Bris, GIS | 5788 / 1261 · 142770 / 11275 · 23493 / 3470 |
| 16 | S, B, B, S, b | also, nevertheless, indeed, nonetheless, therefore | State, Eis, JS, Meteor, JavaScript | 8213 / 2219 · 72012 / 5184 · 33345 / 3091 |
| 20 | 状态, state, S, T, 常温 | merely, presently, nonetheless, likewise, wholly | state, states, temperature, 常温, mineral | 23937 / 2655 · 108014 / 6325 · 4407 / 875 |
| 24 | T, S, P, state, R | presently, \u, \uff, merely, \n | temperature, temperatures, Fahrenheit, mineral, temperature | 14595 / 420 · 66639 / 2972 · 722 / 138 |
| 28 | M, M, at, 常温, 1 | \u, presently, likewise, \uff, notably | mineral, temperature, State, Mineral, state | 22538 / 965 · 29180 / 1030 · 1256 / 129 |
| 32 | (s, M, O, X, MO | 什么意思, 什么, 是什么, 是什么意思, XXXX | mineral, temperature, State, chemical, Mineral | 68285 / 2923 · 114780 / 18876 · 2145 / 263 |
| 36 | 常温, MO, MO, SO, (s | \n, 什么, chemical, [a, 什么意思 | chemical, Chemical, mineral, chemistry, temperature | 17190 / 404 · 3281 / 749 · 62 / 91 |
| 40 | 固态, state, 状态, 固体, 的状态 | 液态, chemical, metallic, 固态, metal | metal, metallic, [liquid], state, metals | 3843 / 11 · 168 / 39 · 19 / 9 |
| 44 | 固态, (s, 0, T, G | \n, <u, <br, 固态, metallic | state, temperature, metallic, *solid*, chemical | 8462 / 41 · 476 / 36 · 85 / 4 |
| 48 | 固态, 的状态, 常温, 状态的, 状态 | \n, <u, \u, <br, \t | metallic, metal, state, chemical, mol | 12421 / 119 · 1857 / 372 · 31 / 11 |
| 52 | 固态, 固体, 液态, 固, solids | <u, 固态, 液态, \n, solids | 液态, [liquid], state, 固态, metal | 3039 / 7 · 2385 / 10 · 120 / 10 |
| 56 | 固态, 固体, *solid*, 固, [liquid] | 固态, [liquid], *solid*, 固体, [Liquid] | [liquid], *solid*, 固态, 固体, 液态 | 998 / 3 · 448 / 3 · 181 / 2 |
| 60 | *solid*, 固, 固态, 固体, *Solid* | *solid*, *Solid*, 固态, *solid*, *Solid* | *solid*, [liquid], *Solid*, *solid*, solids | 68 / 1 · 50 / 1 · 29 / 1 |
| 62 | *solid*, *Solid*, [liquid], 固, a | *solid*, *Solid*, [liquid], 固态, solids | *solid*, -solid, *Solid*, [liquid], *solid* | 22 / 1 · 21 / 1 · 83 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `element` (cue) | ally (67712) | which (37628) | which (1088) | sulfur (381) | chemistry (94) | Chemical (142) | chlorine (62) | chlorine (40) |
| `with` (cue) | ness (112398) | dicip (88525) | hium (24477) | <u (5637) | atomic (202) | name (872) | atomic (8065) | atomic (802) |
| `atomic` (cue) | ity (105569) | ity (11896) | atomic (17167) | atomic (8215) | atomic (1243) | atomic (5378) | number (10624) | number (1433) |
| `number` (cue) | 's (35385) | of (9818) | number (2791) | number (2655) | number (1321) | number (1053) | Atomic (299) | eighty (468) |
| `␣` (cue) | ´s (9649) | ´s (1272) | amongst (218) | XXXX (1284) | 1 (158) | \n (677) | 元素 (218) | 8 (231) |
| `2` (cue) | -old (119593) | o (6006) | 2 (17362) | 原子 (82514) | 原子 (23475) | 2 (109038) | is (324) | 6 (360) |
| `6` (cue) | aveled (35039) | in (3280) | in (3) | 6 (16) | **iron** (1) | 钢铁 (2) | is (2) | is (2) |
| `is` | avour (188597) | also (72015) | presently (65862) | 什么意思 (114660) | 液态 (168) | \n (1912) | 固态 (459) | *solid* (21) |

### `mars-color`

> Fact: The color of the planet fourth from the Sun is

Cue phrase: "planet fourth from the Sun"

Bridge **Mars** -> answer *red*; controls [Earth] / [blue]. category: multihop, model answers correctly: yes, swapping flips the answer: neither part, model's top word: red.
Why this group: J-lens bridge ranked first among the entities in 0% of band layers at the last token, distractor 100%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/mars-color__jlens.html) · [J++](slices/mars-color__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, A | –and, The, It, the, For | <unk, <b, \xc, <data, Connecticut | 16190 / 1010 · 12015 / 418 · 148466 / 53679 |
| 4 | a, S, S, s, P | 률은, 认认真, きっ, 港币, 专栏收录该内容 | OpenGL, _SDK, 王菲, 优秀共产党员, Wichita | 14989 / 768 · 24409 / 46531 · 145097 / 143368 |
| 8 | y, P, a, R, S | 大金, icate, 득, avian, amente | colors, colors, color, 颜色, Colors | 2739 / 813 · 256 / 12111 · 43152 / 14604 |
| 12 | S, S, a, s, M | colors, color, coloring, favor, /colors | COLOR, Color, COLOR, Colors, /colors | 7678 / 1174 · 4355 / 3225 · 964 / 5919 |
| 16 | S, M, S, R, B | actually, basically, just, even, also | Color, COLOR, Colors, COLOR, Color | 13611 / 2838 · 37278 / 634 · 257 / 11804 |
| 20 | B, M, R, ly, b | just, though, much, actually, that | planet, colors, planets, 行星, 木星 | 170 / 136 · 11127 / 286 · 76 / 333 |
| 24 | M, R, P, B, S | much, just, sometimes, farther, because | planet, colors, color, planets, Jupiter | 1490 / 345 · 802 / 205 · 17 / 183 |
| 28 | M, S, (s, P, m | <u, \n, \u, 什么, color | planet, asteroid, color, [Earth], planets | 29939 / 319 · 916 / 1288 · 25 / 908 |
| 32 | U, g, un, ano, S | 什么意思, 是什么意思, 什么, 是什么, <u | planet, [Earth], asteroid, planets, Planet | 55281 / 2790 · 1939 / 12882 · 31 / 1467 |
| 36 | 寡, planets, ixo, orbits, photos | planet, 地球, planets, NASA, [Earth] | planet, planets, planetary, 行星, Planet | 8994 / 13442 · 36 / 6140 · 21 / 3921 |
| 40 | 拥有丰富的, 如火, facts, ummer, สื่อ | planet, [Earth], 地球, Jupiter, Venus | planet, Planet, planetary, Jupiter, [Earth] | 7440 / 3884 · 16 / 311 · 10 / 41 |
| 44 | 橘, aceous, gos, redd, nam | color, colors, planet, color, Color | [Earth], planet, color, orange, *red* | 3235 / 147 · 49 / 32 · 21 / 5 |
| 48 | nam, 火, 橘, color, known | color, [Earth], planet, colors, earth | planet, color, [Earth], earth, planets | 1198 / 92 · 25 / 44 · 10 / 9 |
| 52 | [Earth], 地球, redd, 橘, earth | [Earth], planet, Planet, redd, earth | planet, planets, 金星, Planet, Venus | 30 / 10 · 10 / 13 · 11 / 21 |
| 56 | [Earth], 地球, planet, 火星, 红色 | planet, [Earth], Planet, redd, yellow | planet, planetary, planets, Planet, 金星 | 11 / 41 · 7 / 15 · 8 / 24 |
| 60 | *red*, redd, 橘, orange, *Red* | *red*, redd, orange, *Red*, Orange | *red*, redd, orange, *Red*, -red | 34 / 1 · 22 / 1 · 8 / 1 |
| 62 | *red*, orange, called, redd, yellow | *red*, orange, redd, yellow, [blue] | *red*, redd, orange, [blue], known | 11 / 1 · 9 / 1 · 53 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `of` | colors (7976) | colors (10772) | color (4621) | color (3264) | color (2207) | color (1355) | sky (150) | clouds (291) |
| `the` | colors (194) | colors (4328) | color (1735) | color (816) | color (496) | color (229) | sky (314) | sky (806) |
| `planet` (cue) | **Mars** (1) | Planet (8) | Planet (11) | planet (17) | planet (17) | planet (8) | Jupiter (2) | **Mars** (1) |
| `fourth` (cue) | 了 (158972) | s (231194) | 了 (112036) | uranus (8239) | 地球 (344) | planet (148) | planet (80) | from (100) |
| `from` (cue) | ς (12934) | s (27565) | planet (53) | 地球 (352) | 地球 (57) | NASA (60) | Sun (37) | the (20) |
| `the` (cue) | 旳 (91) | farther (57702) | colors (2042) | colors (1294) | color (79) | color (72) | stars (64) | sun (135) |
| `Sun` (cue) | aries (64) | —not (134) | Saturn (35) | Earth (20) | [Earth] (28) | [Earth] (23) | is (7) | is (4) |
| `is` | 大金 (255) | actually (37281) | much (802) | 什么意思 (1937) | planet (16) | color (25) | planet (7) | *red* (9) |

### `person-firstname-newton`

> Fact: The first name of the scientist on whose head an apple is said to have fallen was

Cue phrase: "scientist on whose head an apple is said to have fallen"

Bridge **Newton** -> answer *Isaac*; controls [Shakespeare] / [William]. category: person-firstname, model answers correctly: yes, swapping flips the answer: neither part, model's top word: Isaac.
Why this group: J-lens bridge ranked first among the entities in 6% of band layers at the last token, distractor 94%; J++ 12%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/person-firstname-newton__jlens.html) · [J++](slices/person-firstname-newton__jpp.html)

**Last token** `was`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, T, s, a, S | er, en, –and, a, u | <unk, -www, illions, 就像一个, Cherokee | 7937 / 26280 · 55209 / 23470 · 14413 / 58011 |
| 4 | S, T, a, A, M | er, трёх, 图象, en, 砼 | SQLite, 泉州市, .SQLite, Greek, Venice | 4124 / 31578 · 211601 / 139181 · 241359 / 217499 |
| 8 | B, A, T, S, H | 的, Colour, 其它, colour, 在 | afterwards, 绵阳市, 绵阳, rvine, famous | 2810 / 14919 · 204505 / 131002 · 101530 / 94203 |
| 12 | nt, s, A, b, B | er, colour, favourite, colour, recognised | WW, WAS, Wah, WW, (W | 2612 / 12625 · 108765 / 34580 · 42839 / 34432 |
| 16 | B, B, E, 其实, A | indeed, 其它, ещё, فى, Whilst | WW, Gaw, WW, awa, W | 1731 / 22776 · 134711 / 27447 · 14710 / 5523 |
| 20 | name, 先, B, b, E | 哪, chiefly, indeed, ещё, 什么 | quite, famous, names, invented, perhaps | 6568 / 34439 · 201387 / 62935 · 8241 / 3097 |
| 24 | name, 名字, name, Name, names | chiefly, merely, famously, actually, indeed | names, name, named, 姓名, quite | 779 / 23701 · 96794 / 8694 · 872 / 1176 |
| 28 | W, name, B, them, A | famously, 哪一个, —who, whom, 哪 | name, famous, names, his, named | 1721 / 5538 · 9077 / 533 · 1379 / 353 |
| 32 | 心上, B, 和其, 皿, U | 什么, 请问, 是什么, 是什么意思, 什么意思 | name, famous, named, names, Alexander | 5862 / 5335 · 4391 / 1431 · 791 / 101 |
| 36 | name, A, X, 名字, \n | famously, name, famous, ’t, 名称 | name, famous, names, Name, named | 5766 / 7026 · 226 / 193 · 76 / 73 |
| 40 | name, name, 名字, in, names | name, 名字, name, Name, 姓名 | name, names, named, surname, Name | 579 / 2600 · 107 / 78 · 33 / 36 |
| 44 | \n, G, S, A, T | name, Name, surname, name, 名字 | British, name, surname, English, names | 2728 / 4596 · 73 / 84 · 33 / 34 |
| 48 | \n, 叫什么, borne, <u, 英国 | <u, 叫什么, NAME, 名字, \n | surname, name, Nobel, 姓氏, English | 915 / 8666 · 23 / 38 · 10 / 40 |
| 52 | **Newton**, 姓, /is, borne, obel | <u, **Newton**, *Isaac*, [William], Robert | **Newton**, apple, physicist, Apple, 英国的 | 1 / 97 · 2 / 4 · 1 / 60 |
| 56 | **Newton**, 牛顿, Newton, 苹果, apple | **Newton**, Newton, 牛顿, *Isaac*, Apple | apple, Apple, 苹果, **Newton**, Apple | 1 / 12 · 1 / 4 · 4 / 22 |
| 60 | *Isaac*, **Newton**, 牛顿, /is, Iss | *Isaac*, **Newton**, 牛顿, Newton, Isa | *Isaac*, **Newton**, /is, -is, Apple | 2 / 1 · 2 / 1 · 2 / 1 |
| 62 | *Isaac*, Sir, Iss, **Newton**, Is | *Isaac*, Iss, Sir, **Newton**, Isa | *Isaac*, Is, Is, Isa, Iss | 4 / 1 · 4 / 1 · 24 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `an` (cue) | uminium (233755) | ely (83784) | supposedly (1520) | xxxxxxxx (583) | Einstein (3) | supposedly (27) | supposedly (42) | apple (221) |
| `apple` (cue) | apple (6858) | apple (2286) | apple (23) | apple (4) | apple (6) | supposedly (36) | supposedly (352) | fell (330) |
| `is` (cue) | colour (169507) | colour (37137) | supposedly (14380) | 什么 (5657) | famous (405) | supposedly (2275) | supposed (3229) | said (2052) |
| `said` (cue) | edly (138691) | edly (122949) | reputed (46356) | 什么 (38215) | 传说 (2252) | allegedly (1552) | have (1197) | to (55) |
| `to` (cue) | ‘s (128623) | er (45390) | \u (10) | famously (4) | 牛顿 (3) | 牛顿 (3) | discovered (4) | have (4) |
| `have` (cue) | recognised (27174) | favoured (9153) | reputed (3063) | 的 (518) | 砸 (12) | \n (114) | fallen (729) | fallen (310) |
| `fallen` (cue) | avourite (40110) | avourite (1151) | —or (70) | supposedly (4) | 据说 (37) | was (158) | was (159) | is (48) |
| `was` | 的 (204502) | indeed (134749) | chiefly (96279) | 什么 (4392) | name (107) | <u (23) | **Newton** (1) | *Isaac* (4) |


<a id="readers_disagree"></a>
## J-lens and J++ disagree

Answered correctly; the two lenses' band shares for the bridge differ by >= 0.5.

### `organ-location-heart`

> Fact: The part of the body that contains the organ that pumps blood is the

Cue phrase: "organ that pumps blood"

Bridge **heart** -> answer *chest*; controls [brain] / [head]. category: organ-location, model answers correctly: yes, swapping flips the answer: neither part, model's top word: chest.
Why this group: J-lens bridge ranked first among the entities in 6% of band layers at the last token, distractor 0%; J++ 82%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/organ-location-heart__jlens.html) · [J++](slices/organ-location-heart__jpp.html)

**Last token** `the`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, S, s, I | –and, The, o, It, a | many, New, the, several, some | 4389 / 5400 · 10380 / 21289 · 1294 / 299 |
| 4 | a, s, a, I, in | 데미, CSL, セレ, 加拿大的, CIF | OpenGL, 泉水, Wichita, 翼, ResourceManager | 5660 / 7771 · 115921 / 6624 · 37324 / 66645 |
| 8 | s, a, u, and, L | 大金, 旳, igan, 点击上方, .cat | parts, ワクチン, 颜料, افر, injured | 5437 / 10043 · 121767 / 23180 · 928 / 1737 |
| 12 | is, K, L, c, s | er, organisation, neighbour, 部份, colour | and, The, the, of, in | 16778 / 13543 · 1935 / 1034 · 684 / 521 |
| 16 | J, S, B, l, L | amongst, whilst, Whilst, 部份, Whilst | and, the, The, in, of | 7715 / 7383 · 11026 / 554 · 2823 / 498 |
| 20 | X, 最, a, a, l | 什么地方, 哪一个, 哪儿, 全部的, actually | parts, Baptist, Kansas, Texas, Tex | 8119 / 40449 · 10696 / 47839 · 95 / 1901 |
| 24 | B, X, B, G, J | 哪一个, 什么地方, 什么人, 哪儿, what | the, place, part, very, only | 14917 / 39048 · 22919 / 26895 · 282 / 436 |
| 28 | C, M, B, A, G | 哪一个, 什么, 什么地方, what, 哪里 | the, The, part, and, body | 3070 / 19567 · 8679 / 12576 · 125 / 890 |
| 32 | C, A, to, M, X | 什么, 什么意思, <u, 是什么, YOU | The, the, in, Medical, A | 885 / 37036 · 16438 / 5581 · 214 / 1301 |
| 36 | X, body, M, <u, 间接 | 什么, 什么意思, 是什么, 是什么意思, 哪里 | medical, body, the, Medical, health | 144 / 38003 · 2351 / 3221 · 36 / 648 |
| 40 | body, body, <u, organs, S | body, anatom, Body, 人体, anatomy | body, medical, health, human, **heart** | 23 / 10757 · 183 / 142 · 5 / 202 |
| 44 | body, <u, body, 户, IT | body, torso, Body, humans, bodily | body, torso, human, center, area | 39 / 5347 · 159 / 73 · 10 / 52 |
| 48 | body, 叫做, <u, called, umb | torso, body, abdomen, /body, Body | body, torso, **heart**, humans, human | 9 / 517 · 43 / 21 · 3 / 9 |
| 52 | **heart**, torso, *chest*, body, lungs | torso, lungs, **heart**, body, abdomen | **heart**, body, *chest*, torso, Heart | 1 / 3 · 3 / 7 · 1 / 4 |
| 56 | *chest*, 胸腔, torso, thor, 胸 | *chest*, torso, 胸腔, thor, *Chest* | *chest*, 胸腔, torso, *Chest*, **heart** | 14 / 1 · 12 / 1 · 5 / 1 |
| 60 | *chest*, thor, 胸, 胸腔, 胸部 | *chest*, thor, torso, *Chest*, *chest* | *chest*, thor, *Chest*, Thor, 胸 | 18 / 1 · 16 / 1 · 14 / 1 |
| 62 | *chest*, thor, torso, **heart**, Thor | *chest*, torso, thor, trunk, **heart** | *chest*, torso, thor, *chest*, trunk | 4 / 1 · 5 / 1 · 6 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `contains` | жё (168137) | s (565) | parts (215) | 的 (4041) | organs (139) | organs (28) | organs (7) | blood (32) |
| `the` | 大金 (137041) | s (202) | people (14) | what (87) | organs (4) | organs (3) | organs (3) | [brain] (2) |
| `organ` (cue) | er (137896) | er (1646) | organs (243) | 的 (2082) | organs (28) | organs (6) | called (13) | that (6) |
| `that` (cue) | raries (111087) | got (2322) | is (658) | 是什么 (62012) | humans (354) | humans (19) | organ (166) | pumps (581) |
| `pumps` (cue) | Watts (13679) | big (319) | pumps (14) | <u (730) | pumps (21) | pumps (17) | blood (141) | blood (44) |
| `blood` (cue) | s (12324) | s (336) | to (11) | \n (62) | blood (41) | blood (15) | throughout (28) | is (40) |
| `is` | colour (176981) | basically (2024) | 什么 (1475) | 什么 (6841) | 心脏 (4) | located (5) | called (36) | the (20) |
| `the` | 大金 (121865) | amongst (11030) | 哪一个 (22920) | 什么 (16440) | body (183) | torso (43) | *chest* (12) | *chest* (5) |


<a id="model_wrong"></a>
## Model answers wrong

The model does not give the answer. Does the lens still see the bridge?

### `greatwall-ocean`

> Fact: The ocean east of the country that built the Great Wall is the

Bridge **China** -> answer *Pacific*; controls [Brazil] / [Atlantic]. category: multihop, model answers correctly: no, swapping flips the answer: -, model's top word: Yellow.
Why this group: J-lens bridge ranked first among the entities in 12% of band layers at the last token, distractor 0%; J++ 6%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/greatwall-ocean__jlens.html) · [J++](slices/greatwall-ocean__jpp.html)

**Last token** `the`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, S, A, in | The, –and, It, For, Or | New, many, Connecticut, the, Arkansas | 10181 / 14665 · 20180 / 24785 · 1634 / 3712 |
| 4 | a, for, to, in, s | CSL, 데미, Celebrity, .Pro, セレ | egasus, 情人节, 碧, ensburg, _pcm | 5027 / 21869 · 4883 / 103281 · 194384 / 198790 |
| 8 | a, s, s, c, M | 大金, Vorte, VERY, ustralian, igan | Colorado, Kans, color, Colorado, colors | 6102 / 14522 · 214205 / 202483 · 77906 / 328 |
| 12 | A, a, M, to, M | biggest, chance, fame, ´s, asian | and, ocean, Ocean, *Pacific*, The | 3208 / 47196 · 38752 / 12585 · 551 / 4 |
| 16 | w, H, c, Y, H | biggest, best, one, one, bigger | and, the, The, as, for | 16024 / 53363 · 4067 / 2018 · 1772 / 76 |
| 20 | ough, enc, Enc, 陆, 海 | Ocean, Ocean, ocean, 海域, oceans | ocean, marine, maritime, sea, 海域 | 2272 / 1343 · 128 / 6 · 1276 / 193 |
| 24 | g, 陆, ense, 海, sea | Ocean, ocean, oceans, Ocean, [Atlantic] | ocean, sea, marine, Ocean, maritime | 1469 / 5761 · 50 / 11 · 256 / 71 |
| 28 | b, g, 陆, 怎, l | ocean, Ocean, coastal, oceans, [Atlantic] | ocean, Ocean, coastal, Sea, sea | 9138 / 4997 · 59 / 20 · 415 / 60 |
| 32 | b, iro, 休, 限定, unge | ocean, Ocean, coastal, oceans, [Atlantic] | ocean, Ocean, coastal, Sea, marine | 4562 / 4679 · 79 / 16 · 421 / 50 |
| 36 | 限定, 边的, -facing, 拉克, addy | ocean, Ocean, coastal, Ocean, oceans | ocean, coastal, Ocean, Sea, sea | 1298 / 33135 · 16 / 27 · 97 / 47 |
| 40 | -facing, 边的, alis, 沿岸, 海洋 | ocean, Ocean, Ocean, oceans, 海洋 | ocean, sea, Ocean, marine, Sea | 385 / 2380 · 49 / 28 · 75 / 18 |
| 44 | 边的, -facing, name, reeze, called | Ocean, ocean, oceans, Ocean, [Atlantic] | ocean, Ocean, sea, [Atlantic], Sea | 179 / 19967 · 22 / 7 · 26 / 8 |
| 48 | ses, sea, called, 叫做, ocratic | Ocean, ocean, Ocean, oceans, Maritime | ocean, Ocean, Sea, sea, oceans | 645 / 9385 · 29 / 10 · 32 / 12 |
| 52 | 太平洋, acific, Asian, 亚洲, 中国的 | Ocean, Asian, Asia, Sea, **China** | Ocean, Sea, ocean, sea, Asian | 30 / 48 · 6 / 6 · 17 / 12 |
| 56 | 太平洋, 黄海, *Pacific*, 东海, *Pacific* | *Pacific*, 太平洋, *Pacific*, 东海, Asian | *Pacific*, 太平洋, Asian, Chinese, 东海 | 25 / 3 · 10 / 1 · 8 / 1 |
| 60 | Yellow, Yellow, 黄海, yellow, 黄 | Yellow, *Pacific*, Sea, yellow, Yellow | Yellow, 黄海, yellow, Huang, *Pacific* | 59 / 7 · 23 / 2 · 8 / 5 |
| 62 | Yellow, *Pacific*, East, yellow, Sea | Yellow, *Pacific*, Sea, East, yellow | *Pacific*, Yellow, East, Sea, yellow | 13 / 3 · 8 / 2 · 11 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `country` | 's (6566) | 's (127) | country (25) | countries (32) | countries (16) | countries (14) | Canada (7) | of (4) |
| `that` | aveled (130482) | bigger (228) | nations (12) | 什么 (60) | countries (7) | countries (3) | contains (128) | borders (79) |
| `built` | rastructure (134120) | big (50) | Britain (7) | 造船 (113) | 建造 (25) | 建造 (31) | Statue (218) | the (156) |
| `the` | .But (76595) | big (223) | Britain (3) | 什么意思 (13) | ships (21) | famous (23) | Statue (525) | Statue (592) |
| `Great` | s (2145) | s (614) | Great (2) | civilizations (5) | **China** (1) | **China** (2) | Barrier (65) | Wall (68) |
| `Wall` | a (386) | of (21) | of (2) | **China** (1) | **China** (1) | **China** (1) | is (2) | of (13) |
| `is` | anyways (207146) | bigger (456) | China (3) | China (6) | **China** (1) | **China** (1) | **China** (1) | **China** (1) |
| `the` | 大金 (214022) | biggest (4066) | Ocean (50) | ocean (79) | ocean (49) | Ocean (30) | *Pacific* (10) | Yellow (8) |

### `instr-body-trumpet`

> Fact: The part of the body a player buzzes to play the valved brass instrument heard in jazz solos is the

Bridge **trumpet** -> answer *lips*; controls [drums] / [hands]. category: instr-played, model answers correctly: no, swapping flips the answer: -, model's top word: mouth.
Why this group: J-lens bridge ranked first among the entities in 100% of band layers at the last token, distractor 0%; J++ 94%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/instr-body-trumpet__jlens.html) · [J++](slices/instr-body-trumpet__jpp.html)

**Last token** `the`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, A, I, in | The, –and, o, Or, a | New, many, Connecticut, Telegram, Arkansas | 80413 / 20628 · 19444 / 14738 · 60234 / 55372 |
| 4 | a, A, I, to, s | 데미, セレ, 加拿大的, CSL, -CS | 碧, ーブ, 周杰伦, 小鸟, _pcm | 68593 / 21322 · 170523 / 102000 · 76391 / 6599 |
| 8 | u, a, b, a, G | 旳, 大金, attery, quel, igan | musical, Wichita, music, 乐器, brass | 45214 / 26910 · 83432 / 20309 · 155 / 3773 |
| 12 | K, G, c, k, u | er, 部份, -C, chance, u | and, The, Kansas, Wichita, Dallas | 61638 / 18226 · 47348 / 1200 · 26609 / 1702 |
| 16 | B, A, N, A, G | amongst, Though, o, a, though | Wichita, Kansas, and, the, Bates | 52333 / 11948 · 73505 / 31579 · 57740 / 303 |
| 20 | parts, 拢, 衔, 触, RequestBody | Though, Aside, though, Though, Something | **trumpet**, brass, musicians, musical, music | 1675 / 3385 · 7997 / 8755 · 1 / 69 |
| 24 | 喉, soft, 虫, 触, 领 | Voice, Music, Though, Sound, What | **trumpet**, brass, vocal, musical, pipe | 3895 / 22058 · 109 / 725 · 1 / 28 |
| 28 | \n, 附件, end, 吹, F | **trumpet**, vocal, brass, 乐器, Music | **trumpet**, brass, Brass, nipple, musicians | 15051 / 6221 · 1 / 18 · 1 / 26 |
| 32 | \n, R, end, o, an | 什么, \n, What, <u, What | **trumpet**, brass, Brass, mouth, nipple | 5687 / 2223 · 30 / 42 · 1 / 35 |
| 36 | 口, 吹, 口腔, 嘴巴, 嘴 | What, \n, 什么, **trumpet**, How | brass, **trumpet**, Brass, mouth, pipe | 88 / 763 · 4 / 41 · 2 / 29 |
| 40 | 嘴巴, ToArray, 芦, 叫做, 嘴 | 嘴唇, **trumpet**, *lips*, 乐器, Mouth | **trumpet**, mouth, brass, *lips*, pipe | 251 / 147 · 2 / 3 · 1 / 4 |
| 44 | iet, 直接与, \n, 人的, rim | 嘴唇, *lips*, mouth, Mouth, cheeks | mouth, brass, metal, *lips*, Mouth | 15681 / 503 · 17 / 2 · 17 / 4 |
| 48 | ress, 直接接触, 接口, ses, interface | 嘴唇, Mouth, *lips*, mouth, brass | mouth, brass, *lips*, metal, 嘴唇 | 38573 / 938 · 10 / 3 · 10 / 4 |
| 52 | 口腔, 嘴唇, mouth, 嘴巴, *lips* | *lips*, mouth, Mouth, 嘴唇, lungs | mouth, Mouth, *lips*, metal, 嘴唇 | 2494 / 5 · 22 / 1 · 6 / 3 |
| 56 | mouth, mouth, Mouth, *lips*, 口 | mouth, *lips*, Mouth, mouth, 嘴唇 | mouth, Mouth, *lips*, mouth, 嘴唇 | 57 / 4 · 22 / 2 · 26 / 3 |
| 60 | *lips*, mouth, 嘴唇, 唇, *Lips* | *lips*, mouth, *Lips*, 嘴唇, lip | mouth, *lips*, lip, 嘴唇, *Lips* | 69 / 1 · 19 / 1 · 31 / 2 |
| 62 | *lips*, mouth, *Lips*, lip, player | *lips*, mouth, *Lips*, lip, player | mouth, *lips*, lip, *Lips*, *lips* | 47 / 1 · 13 / 1 · 25 / 2 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `brass` | s (19) | s (24) | brass (4) | brass (3) | **trumpet** (1) | brass (3) | instruments (5) | instrument (3) |
| `instrument` | —a (1142) | which (4447) | which (301) | 什么 (246) | instrument (39) | called (40) | called (2) | **trumpet** (1) |
| `heard` | edly (6203) | edly (2397) | heard (1117) | 什么 (1012) | music (168) | music (119) | playing (3) | in (16) |
| `in` | ners (61579) | popular (11883) | music (65) | music (46) | music (37) | music (36) | orchestra (3) | jazz (25) |
| `jazz` | s (1192) | jazz (4234) | jazz (129) | jazz (126) | jazz (62) | jazz (110) | music (32) | bands (30) |
| `solos` | 써 (5091) | and (3757) | jazz (180) | jazz (15) | jazz (14) | jazz (24) | is (28) | is (35) |
| `is` | Shemale (157040) | notably (19150) | 什么 (61608) | 什么 (12926) | anatom (34) | anatom (557) | mouth (18) | *lips* (24) |
| `the` | 旳 (83431) | amongst (73508) | Voice (108) | 什么 (24) | 嘴唇 (2) | 嘴唇 (10) | mouth (22) | *lips* (13) |

### `osu-rival-mascot`

> Fact: The mascot of the college football rival of Ohio State is a

Bridge **Michigan** -> answer *wolverine*; controls [Wisconsin] / [badger]. category: multihop, model answers correctly: no, swapping flips the answer: -, model's top word: buck.
Why this group: J-lens bridge ranked first among the entities in 71% of band layers at the last token, distractor 0%; J++ 94%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/osu-rival-mascot__jlens.html) · [J++](slices/osu-rival-mascot__jpp.html)

**Last token** `a`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, s, 1, a, s | –and, The, the, It, a | <unk, Connecticut, children, <data, everyone | 27122 / 105045 · 16198 / 56318 · 16772 / 98318 |
| 4 | to, S, a, T, s | 翡, جدًا, Academia, Counseling, Celebrity | 优秀共产党员, 雷诺, 灵儿, 周杰伦, 李克 | 26314 / 81912 · 1731 / 125090 · 5086 / 54035 |
| 8 | S, S, H, T, p | جدًا, ilee, htar, ustralian, jewelry | Garland, famous, Colorado, hometown, flying | 38683 / 90896 · 86477 / 114363 · 5599 / 91193 |
| 12 | H, H, T, p, 1 | big, lucky, favorite, nice, beautiful | mascot, Bea, ADA, Hollywood, AAA | 36882 / 79770 · 12264 / 13686 · 3472 / 90906 |
| 16 | T, S, P, F, s | favorite, big, folks, famous, bigger | mascot, and, Fantasy, Bair, a | 52637 / 143516 · 888 / 6029 · 2856 / 98497 |
| 20 | aw, mascot, 丑, T, 叫做 | mascot, favorite, goofy, Mickey, humor | mascot, Kentucky, college, animal, university | 104630 / 175732 · 596 / 1591 · 2138 / 4293 |
| 24 | 廷, 系, 傍, 系的, ත | mascot, Mickey, college, sports, athletic | mascot, sports, college, athletic, university | 28589 / 188105 · 10 / 1604 · 43 / 3065 |
| 28 | 系, 爪, 毛, associated, 殷 | mascot, sports, Mickey, masc, famous | mascot, masc, animal, 吉祥物, sports | 58619 / 157357 · 76 / 821 · 60 / 1031 |
| 32 | 毛, 弄, 系, aug, 系的 | mascot, masc, famous, NASCAR, goofy | mascot, masc, 吉祥物, animal, animals | 98661 / 215474 · 73 / 1218 · 32 / 731 |
| 36 | mascot, 年至今, ych, 毛, INU | mascot, NCAA, Ohio, NASCAR, Baseball | mascot, Ohio, **Michigan**, masc, Ohio | 31079 / 159897 · 9 / 255 · 3 / 207 |
| 40 | emory, plies, mascot, 形象的, 爪 | mascot, Ohio, NCAA, Ohio, **Michigan** | mascot, Ohio, **Michigan**, college, university | 5037 / 145258 · 5 / 432 · 3 / 488 |
| 44 | 叫做, mascot, 名叫, 芒, 帚 | mascot, 吉祥物, masc, symbol, Symbol | mascot, 吉祥物, masc, Ohio, **Michigan** | 5524 / 178048 · 49 / 998 · 5 / 3722 |
| 48 | 叫做, 名叫, mascot, named, 叫 | mascot, 吉祥物, masc, symbol, warriors | mascot, 吉祥物, masc, symbol, university | 10512 / 217974 · 80 / 1639 · 27 / 6943 |
| 52 | mascot, 吉祥物, spirit, 是一只, 加斯 | mascot, masc, 吉祥物, Masc, Ohio | mascot, 吉祥物, Ohio, Ohio, **Michigan** | 3272 / 198698 · 25 / 782 · 5 / 1380 |
| 56 | buck, Buck, Ohio, mascot, Ohio | mascot, Buck, Ohio, Ohio, buck | Ohio, Buck, buck, Ohio, mascot | 3306 / 56476 · 163 / 136 · 10 / 375 |
| 60 | Buck, buck, cardinal, eyes, Fighting | buck, Buck, bulld, mascot, hawk | Ohio, buck, Buck, Ohio, **Michigan** | 540 / 493 · 53 / 21 · 5 / 67 |
| 62 | buck, Buck, block, Block, mean | buck, bulld, Buck, mascot, hawk | buck, bob, bulld, mascot, buzz | 184 / 345 · 419 / 46 · 2418 / 683 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `college` | college (13567) | college (2103) | college (556) | college (149) | college (192) | college (94) | basketball (181) | basketball (200) |
| `football` | s (11584) | s (977) | football (315) | NCAA (98) | NCAA (141) | Football (88) | team (153) | team (234) |
| `rival` | icious (219238) | ing (33699) | matchup (28275) | rivalry (688) | rivalry (242) | rivalry (131) | ry (232) | ry (85) |
| `of` | iance (200350) | milfs (8715) | 对手的 (43827) | 什么意思 (11231) | 竞争对手 (231) | rival (34) | University (24) | University (15) |
| `Ohio` | Ohio (170) | Ohio (15) | Ohio (6) | Ohio (10) | Ohio (5) | Ohio (7) | Ohio (26) | State (215) |
| `State` | Ohio (3) | Ohio (4) | Ohio (7) | Ohio (6) | Ohio (6) | Ohio (5) | University (23) | University (167) |
| `is` | mascot (117909) | actually (1882) | mascot (1392) | 什么意思 (1156) | mascot (41) | mascot (90) | Buck (36) | the (20) |
| `a` | جدًا (86479) | favorite (885) | mascot (10) | mascot (76) | mascot (5) | mascot (80) | mascot (167) | buck (419) |

