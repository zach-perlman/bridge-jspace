# Examples: exp11_bridge_vs_answer_by_layer (last token, prompts as published), Qwen3.6-27B

Source run `results/exp11_bridge_vs_answer_by_layer/20261014-092835`, model Qwen/Qwen3.6-27B. Examples are drawn at random with seed 0, up to 3 per group; groups can overlap. Marks in the tables: **bridge**, *answer*, [distractor]. Ranks are word ranks (1 = top; spaces and punctuation removed) of the bridge (B) and the answer (A). Readers: logit lens (baseline), J-lens, J++.

| Group | Definition | Items in group | Shown |
|---|---|---|---|
| [Seen at the last token](#seen_last) | Eligible; the J-lens has the bridge top-1 in >= 50% of layers 32-48 at the last token. | 41 | 3 |
| [Missed at the last token](#missed_last) | Eligible; the J-lens has the bridge top-1 in < 50% of layers 32-48 at the last token. | 26 | 3 |
| [Distractor above the bridge](#distractor_wins) | Eligible; the same-category distractor is top-1 in more band layers than the bridge. | 5 | 3 |
| [J-lens and J++ disagree](#readers_disagree) | Eligible; the two lenses' band shares for the bridge differ by >= 0.5. | 1 | 1 |
| [Model answers wrong](#model_wrong) | Part B's clean_wrong: the model's top word is not the answer. Does the lens still see the bridge? | 16 | 3 |

<a id="seen_last"></a>
## Seen at the last token

Eligible; the J-lens has the bridge top-1 in >= 50% of layers 32-48 at the last token.

### `ex2-city-language-Cairo`

> Fact: The language spoken in the country where Cairo is located is

Bridge **Egypt** -> answer *Arabic*; controls [Russia] / [Russian]. category: city-language, status (B): eligible, label (B): J-mediated, model's top word: Arabic.
Why this group: J-lens bridge top-1 in 100% of band layers at the last token, distractor 0%; J++ 100%.
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
| `Cairo` | Cairo (2) | Cairo (2) | Cairo (2) | Cairo (3) | Cairo (3) | Cairo (2) | Cairo (2) | is (21) |
| `is` | ´s (100320) | ´s (20222) | city (13) | <u (116) | cities (290) | located (110) | located (344) | located (38) |
| `located` | .The (10079) | in (2837) | **Egypt** (1) | 是什么意思 (6) | **Egypt** (1) | is (2) | is (2) | is (4) |
| `is` | ´t (186491) | basically (10329) | *Arabic* (9) | 什么 (86) | *Arabic* (11) | *Arabic* (22) | *Arabic* (8) | *Arabic* (14) |

### `ex2-language-capital-Swedish`

> Fact: The capital of the country where Swedish is the primary language is

Bridge **Sweden** -> answer *Stockholm*; controls [Hungary] / [Budapest]. category: language-capital, status (B): eligible, label (B): J-mediated, model's top word: Stockholm.
Why this group: J-lens bridge top-1 in 88% of band layers at the last token, distractor 0%; J++ 82%.
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
| `Swedish` | 瑞典 (22) | Swedish (7) | Swedish (3) | Swedish (3) | Swedish (7) | Swedish (4) | Swedish (3) | is (66) |
| `is` | colour (73665) | really (3872) | Swedish (4) | 瑞典 (10) | languages (130) | language (69) | spoken (938) | spoken (301) |
| `the` | ighbour (161188) | ´t (50873) | lingua (2051) | 什么 (16202) | 语言 (1416) | primary (1756) | official (5013) | official (4221) |
| `primary` | ulatory (237895) | utilizing (225492) | language (14023) | language (11700) | language (1494) | language (1503) | language (46631) | language (9329) |
| `language` | .L (4527) | in (3204) | Swedish (2) | 是什么意思 (19) | 瑞典 (3) | **Sweden** (1) | **Sweden** (1) | is (6) |
| `is` | ustralian (176808) | also (7179) | cities (3772) | 什么意思 (1470) | **Sweden** (1) | **Sweden** (1) | *Stockholm* (2) | *Stockholm* (11) |

### `person-firstname-mozart`

> Fact: The first name of the child-prodigy composer from Salzburg who wrote The Magic Flute was

Bridge **Mozart** -> answer *Wolfgang*; controls [Darwin] / [Charles]. category: person-firstname, status (B): eligible, label (B): J-mediated, model's top word: Wolfgang.
Why this group: J-lens bridge top-1 in 59% of band layers at the last token, distractor 0%; J++ 47%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/person-firstname-mozart__jlens.html) · [J++](slices/person-firstname-mozart__jpp.html)

**Last token** `was`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | T, s, a, S, c | er, –and, en, u, o | <unk, 就像一个, Inglés, -toolbar, -www | 23547 / 80595 · 91102 / 4832 · 45412 / 237736 |
| 4 | a, S, T, s, S | трёх, er, هى, жё, 砼 | _mysql, _php, tiful, 灵儿, 尤文 | 22560 / 73287 · 198890 / 16924 · 93735 / 34980 |
| 8 | P, a, S, l, S | Colour, colour, ёл, ‘s, чёт | 苗木, 王菲, 成都市, 绵阳市, 绵阳 | 24981 / 74350 · 142510 / 7507 · 19671 / 18331 |
| 12 | S, s, s, b, 1 | favourite, colour, colour, Whilst, whilst | WAS, fame, Fame, WM, FW | 18251 / 84280 · 3701 / 3435 · 241 / 18 |
| 16 | s, b, B, M, l | amongst, whilst, Whilst, though, 其它 | GW, FW, WAS, FW, Wizard | 32065 / 39141 · 29590 / 9281 · 246 / 29 |
| 20 | name, P, 姓, S, y | actually, Though, famously, amongst, 仅仅 | names, name, born, famous, fame | 86143 / 12587 · 58187 / 15865 · 36192 / 54197 |
| 24 | name, S, b, Name, l | famously, actually, famed, though, quite | name, names, father, born, famous | 24622 / 24127 · 5706 / 6058 · 1117 / 3083 |
| 28 | F, p, f, C, b | famously, famous, actually, whom, name | father, name, Father, names, famous | 40049 / 20665 · 430 / 3156 · 226 / 917 |
| 32 | b, akes, indeed, X, 尽 | 什么, famous, famously, 叫什么, <u | name, names, surname, famous, Name | 68412 / 40213 · 645 / 3759 · 276 / 240 |
| 36 | name, indeed, X, name, born | name, 原名, 名字, NAME, famously | name, names, famous, Name, name | 57409 / 6608 · 216 / 228 · 155 / 69 |
| 40 | akes, name, indeed, in, born | 名字, name, name, Name, 姓名 | name, names, surname, Name, named | 52213 / 9445 · 155 / 136 · 274 / 193 |
| 44 | G, indeed, nt, 1, u | Name, 名字, name, name, Name | surname, name, names, urname, born | 40657 / 16196 · 84 / 78 · 97 / 122 |
| 48 | nt, 什么, indeed, NOT, 叫什么 | <u, 叫什么, 原名, 名字, NAME | surname, 原名, name, 姓氏, 姓 | 15067 / 5671 · 37 / 31 · 19 / 36 |
| 52 | genius, actually, nt, odom, 什么 | **Mozart**, <u, *Wolfgang*, Johann, Rudolf | **Mozart**, Salzburg, 奥地利, Austrian, Austria | 6 / 132 · 1 / 3 · 1 / 13 |
| 56 | **Mozart**, 奥地利, genius, Austrian, Austria | **Mozart**, Johann, *Wolfgang*, 奥地利, Austria | **Mozart**, 奥地利, Austrian, Austria, Salzburg | 1 / 42 · 1 / 3 · 1 / 12 |
| 60 | **Mozart**, *Wolfgang*, wol, wolf, wolf | *Wolfgang*, **Mozart**, Wolf, Wol, 沃尔 | *Wolfgang*, **Mozart**, Austrian, Salzburg, 奥地利 | 1 / 2 · 2 / 1 · 2 / 1 |
| 62 | *Wolfgang*, W, **Mozart**, Wol, Wolf | *Wolfgang*, **Mozart**, Wol, Wolf, W | *Wolfgang*, Wolf, Wol, **Mozart**, W | 3 / 1 · 2 / 1 · 4 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `Salzburg` | s (264) | s (89) | Salzburg (2) | Salzburg (2) | Salzburg (2) | **Mozart** (1) | Austria (9) | is (7) |
| `who` | ‘s (142757) | amongst (27776) | famed (1063) | famous (126) | **Mozart** (1) | famous (3) | wrote (21) | wrote (75) |
| `wrote` | ся (51260) | many (1783) | **Mozart** (1) | famous (2) | **Mozart** (1) | **Mozart** (1) | **Mozart** (1) | Symphony (3) |
| `The` | 的 (115074) | Whilst (10253) | **Mozart** (1) | 的 (8) | **Mozart** (1) | **Mozart** (1) | Salzburg (3) | Magic (13) |
| `Magic` | Magic (3048) | Magic (505) | Magic (10) | Magic (6) | **Mozart** (1) | **Mozart** (1) | flute (4) | Fl (115) |
| `Fl` | s (66) | a (42) | **Mozart** (1) | **Mozart** (1) | **Mozart** (1) | **Mozart** (1) | **Mozart** (1) | ute (2) |
| `ute` | a (85) | a (11) | **Mozart** (1) | **Mozart** (1) | famous (2) | was (5) | was (3) | is (4) |
| `was` | Colour (142518) | amongst (29140) | famously (5709) | 什么 (644) | 名字 (162) | <u (37) | **Mozart** (1) | *Wolfgang* (2) |


<a id="missed_last"></a>
## Missed at the last token

Eligible; the J-lens has the bridge top-1 in < 50% of layers 32-48 at the last token.

### `ex2-city-continent-Lima`

> Fact: The continent of the country where Lima is located is

Bridge **Peru** -> answer *South*; controls [Egypt] / [Africa]. category: city-continent, status (B): eligible, label (B): J-mediated, model's top word: South.
Why this group: J-lens bridge top-1 in 0% of band layers at the last token, distractor 0%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/ex2-city-continent-Lima__jlens.html) · [J++](slices/ex2-city-continent-Lima__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, P | –and, The, It, the, For | <unk, Connecticut, Counseling, \xc, -www | 47730 / 5718 · 116902 / 1260 · 3283 / 4221 |
| 4 | a, S, T, S, s | 专栏收录该内容, 률은, 港币, 률, 农村商业银行 | _SDK, OpenGL, 仙人掌, _php, Airport | 70252 / 6487 · 19758 / 165784 · 222682 / 644 |
| 8 | a, B, A, S, T | avian, ilian, 大金, rance, unea | continents, _countries, _SDK, countries, 陆地 | 78049 / 5227 · 209418 / 75482 · 190961 / 2820 |
| 12 | B, F, b, a, A | nowadays, mainly, mostly, therefore, neighbouring | ocean, continent, oceans, Planet, continents | 55283 / 4620 · 33132 / 1891 · 1021 / 1108 |
| 16 | B, G, B, S, F | also, basically, nowadays, mainly, actually | Atlantic, continents, Ocean, Planet, ocean | 34018 / 5845 · 5689 / 3274 · 1180 / 1410 |
| 20 | land, 陆, 合, 纪, uto | continent, nowadays, continents, actually, which | continent, continents, continental, nations, countries | 41520 / 3272 · 1599 / 1049 · 175 / 39 |
| 24 | uto, land, g, 纪, 洲 | continent, continents, Europe, Asia, [Africa] | continent, continents, [Africa], countries, Europe | 118983 / 511 · 494 / 254 · 200 / 15 |
| 28 | (s, U, 同一, 际, B | continents, continent, countries, [Africa], Europe | continent, continents, [Africa], continental, Continent | 50714 / 358 · 736 / 392 · 720 / 39 |
| 32 | iro, U, 洲, 摘编, ar | continents, continent, Antarctica, aurus, Countries | continent, continents, Continent, continental, Atlantic | 42606 / 133 · 1684 / 12836 · 645 / 88 |
| 36 | X, known, B, uib, met | continents, continent, [Africa], countries, continent | continent, continents, countries, European, country | 34339 / 370 · 535 / 2155 · 323 / 59 |
| 40 | 洲, 大陆, B, a, continents | continents, continent, [Africa], Americas, Asia | continent, European, Europe, continents, [Africa] | 59676 / 47 · 145 / 577 · 285 / 23 |
| 44 | 洲, a, X, the, name | continents, continent, [Africa], Americas, Asia | continent, continents, Americas, [Africa], Asia | 24210 / 334 · 178 / 379 · 279 / 24 |
| 48 | 叫做, nam, 叫, rove, called | continents, continent, Americas, Asia, [Africa] | continent, continents, continental, Americas, Asia | 27390 / 418 · 93 / 336 · 142 / 43 |
| 52 | Americas, located, 洲, 的名称, 叫做 | Americas, Asia, [Africa], continent, continents | continent, Asia, Continent, [Africa], continents | 2660 / 43 · 9 / 71 · 7 / 73 |
| 56 | called, 洲, Americas, Asia, 美洲 | Americas, Asia, continent, [Africa], Continent | continent, Americas, **Peru**, America, Continent | 43 / 45 · 7 / 49 · 3 / 21 |
| 60 | *South*, 南, *South*, 在南, *south* | *South*, *South*, *south*, SOUTH, 南 | *South*, *South*, 在南, 南美, SOUTH | 44 / 1 · 12 / 1 · 11 / 1 |
| 62 | *South*, called, *South*, *south*, named | *South*, America, *south*, Asia, called | *South*, *south*, *South*, named, called | 32 / 1 · 14 / 1 · 21 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `of` | …and (95604) | a (12402) | [Africa] (2714) | [Africa] (728) | [Africa] (305) | [Africa] (205) | [Africa] (212) | [Africa] (143) |
| `the` | 大金 (204299) | own (24942) | nations (13599) | continents (600) | [Africa] (304) | countries (326) | United (628) | United (1061) |
| `country` | 's (39517) | countries (6516) | countries (743) | (country (504) | countries (330) | countries (207) | where (79) | where (50) |
| `where` | 最新发布 (189040) | 最新发布 (20446) | 最新发布 (989) | Country (810) | Airport (1442) | National (2018) | Mount (1389) | Mount (1060) |
| `Lima` | Lima (11) | Lima (4) | **Peru** (1) | **Peru** (1) | **Peru** (1) | **Peru** (1) | located (2) | is (2) |
| `is` | ´s (112312) | ´t (15355) | city (1602) | 什么意思 (1173) | cities (1467) | is (2571) | located (2719) | located (51) |
| `located` | .The (32307) | in (4303) | in (464) | 是什么意思 (897) | **Peru** (1) | is (11) | is (8) | is (31) |
| `is` | avian (209422) | also (5688) | continent (508) | continents (1685) | continents (145) | continents (93) | Americas (7) | *South* (14) |

### `greatwall-ocean`

> Fact: The ocean east of the country that built the Great Wall is the␣

Bridge **China** -> answer *Pacific*; controls [Brazil] / [Atlantic]. category: multihop, status (B): eligible, label (B): J-mediated, model's top word: Pacific.
Why this group: J-lens bridge top-1 in 35% of band layers at the last token, distractor 0%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/greatwall-ocean__jlens.html) · [J++](slices/greatwall-ocean__jpp.html)

**Last token** `␣`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | I, a, s, A, S | –and, -C, -E, -H, -A | the, one, very, and, in | 8652 / 13037 · 25325 / 154602 · 7895 / 1884 |
| 4 | I, P, A, s, 1 | plorer, maths, ropa, 典礼, otech | Ángeles, 优秀共产党员, ーブ, …the, egasus | 5218 / 21391 · 22201 / 163148 · 171659 / 88864 |
| 8 | I, P, P, i, s | ilee, athon, urette, 典礼, ewater | shot, shots, Hollywood, Nevada, movie | 5070 / 7234 · 219068 / 204280 · 21515 / 64 |
| 12 | ed, P, S, I, a | flix, milfs, ilee, pornstar, veggies | Century, Vegas, Colorado, franchise, Arizona | 4196 / 10666 · 222761 / 155180 · 3799 / 82 |
| 16 | er, ed, w, F, W | veggies, /stats, biggest, -tech, milfs | Century, Arizona, Colorado, World, Vegas | 2609 / 21929 · 211528 / 5306 · 1347 / 125 |
| 20 | ed, ug, 海, az, w | iha, utc, retti, 啥, biggest | ocean, sea, naval, seas, marine | 747 / 55083 · 62218 / 64 · 157 / 144 |
| 24 | U, ed, T, V, U | biggest, Ranked, tallest, amongst, largest | largest, world, ocean, nations, ranking | 2286 / 9900 · 2518 / 222 · 68 / 59 |
| 28 | M, T, I, A, U | 什么, 啥, biggest, 哪一个, -China | World, world, North, nations, Western | 14832 / 22972 · 273 / 59 · 206 / 19 |
| 32 | I, U, A, M, T | 什么, 啥, 什么意思, whats, XXXX | Sea, *Pacific*, World, Western, countries | 3739 / 29922 · 168 / 340 · 65 / 2 |
| 36 | uny, sea, 封, M, X | 什么, 啥, ocean, 世界, 的 | ocean, Sea, sea, marine, Ocean | 5142 / 61653 · 367 / 244 · 130 / 26 |
| 40 | sea, ocean, tallest, major, 世界上最 | ocean, oceans, 海洋, Ocean, Ocean | water, ocean, sea, world, lake | 2788 / 33429 · 76 / 131 · 180 / 49 |
| 44 | 拥有, 摩, igo, tallest, world | ocean, oceans, largest, global, tallest | world, largest, ocean, worldwide, national | 5945 / 6087 · 105 / 341 · 151 / 139 |
| 48 | 世界上最, igo, orld, ikin, largest | ocean, largest, oceans, Largest, tallest | ocean, world, largest, oceans, sea | 4599 / 7859 · 101 / 324 · 133 / 173 |
| 52 | largest, 第二大, ighest, widest, tallest | largest, Ocean, Largest, ocean, oceans | ocean, Ocean, sea, Sea, oceans | 1030 / 2322 · 35 / 63 · 46 / 85 |
| 56 | second, 第二, 第二大, second, 第三 | 第二, second, second, Second, 第三 | second, sea, ocean, Ocean, third | 332 / 82 · 98 / 25 · 15 / 11 |
| 60 | third, 第三, fourth, second, third | *Pacific*, third, fourth, second, Third | *Pacific*, *Pacific*, Chinese, **China**, Asian | 174 / 6 · 29 / 1 · 4 / 1 |
| 62 | *Pacific*, Yellow, pac, yellow, largest | *Pacific*, 3, 4, Yellow, 2 | *Pacific*, Yellow, *Pacific*, East, Ocean | 24 / 1 · 22 / 1 · 10 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `that` | aveled (128583) | bigger (232) | nations (12) | 什么 (57) | countries (7) | countries (4) | contains (132) | borders (91) |
| `built` | rastructure (135201) | big (51) | Britain (7) | 造船 (122) | 建造 (25) | 建造 (31) | Statue (215) | the (153) |
| `the` | .But (76340) | big (223) | America (3) | 什么意思 (12) | ships (21) | famous (23) | Statue (512) | Statue (597) |
| `Great` | s (2130) | s (612) | Great (2) | civilizations (5) | **China** (1) | **China** (1) | Barrier (64) | Wall (62) |
| `Wall` | a (385) | of (20) | of (2) | **China** (1) | **China** (1) | **China** (1) | is (2) | of (13) |
| `is` | anyways (206270) | bigger (456) | China (3) | China (7) | **China** (1) | **China** (1) | **China** (1) | **China** (1) |
| `the` | 大金 (213764) | biggest (4103) | Ocean (48) | ocean (74) | ocean (42) | Ocean (29) | *Pacific* (10) | Yellow (8) |
| `␣` | ilee (219069) | veggies (211520) | biggest (2516) | 什么 (169) | ocean (77) | ocean (101) | 第二 (99) | *Pacific* (22) |

### `organ-location-heart`

> Fact: The part of the body that contains the organ that pumps blood is the

Bridge **heart** -> answer *chest*; controls [brain] / [head]. category: organ-location, status (B): eligible, label (B): neither, model's top word: chest.
Why this group: J-lens bridge top-1 in 6% of band layers at the last token, distractor 0%; J++ 82%.
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
| `organ` | er (137896) | er (1646) | organs (243) | 的 (2082) | organs (28) | organs (6) | called (13) | that (6) |
| `that` | raries (111087) | got (2322) | is (658) | 是什么 (62012) | humans (354) | humans (19) | organ (166) | pumps (581) |
| `pumps` | Watts (13679) | big (319) | pumps (14) | <u (730) | pumps (21) | pumps (17) | blood (141) | blood (44) |
| `blood` | s (12324) | s (336) | to (11) | \n (62) | blood (41) | blood (15) | throughout (28) | is (40) |
| `is` | colour (176981) | basically (2024) | 什么 (1475) | 什么 (6841) | 心脏 (4) | located (5) | called (36) | the (20) |
| `the` | 大金 (121865) | amongst (11030) | 哪一个 (22920) | 什么 (16440) | body (183) | torso (43) | *chest* (12) | *chest* (5) |


<a id="distractor_wins"></a>
## Distractor above the bridge

Eligible; the same-category distractor is top-1 in more band layers than the bridge.

### `ex-element-state-26-80`

> Fact: The state of matter at room temperature of the element with atomic number 26 is

Bridge **iron** -> answer *solid*; controls [mercury] / [liquid]. category: element-state, status (B): eligible, label (B): neither, model's top word: solid.
Why this group: J-lens bridge top-1 in 0% of band layers at the last token, distractor 18%; J++ 29%.
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
| `element` | ally (67712) | which (37628) | which (1088) | sulfur (381) | chemistry (94) | Chemical (142) | chlorine (62) | chlorine (40) |
| `with` | ness (112398) | dicip (88525) | hium (24477) | <u (5637) | atomic (202) | name (872) | atomic (8065) | atomic (802) |
| `atomic` | ity (105569) | ity (11896) | atomic (17167) | atomic (8215) | atomic (1243) | atomic (5378) | number (10624) | number (1433) |
| `number` | 's (35385) | of (9818) | number (2791) | number (2655) | number (1321) | number (1053) | Atomic (299) | eighty (468) |
| `␣` | ´s (9649) | ´s (1272) | amongst (218) | XXXX (1284) | 1 (158) | \n (677) | 元素 (218) | 8 (231) |
| `2` | -old (119593) | o (6006) | 2 (17362) | 原子 (82514) | 原子 (23475) | 2 (109038) | is (324) | 6 (360) |
| `6` | aveled (35039) | in (3280) | in (3) | 6 (16) | **iron** (1) | 钢铁 (2) | is (2) | is (2) |
| `is` | avour (188597) | also (72015) | presently (65862) | 什么意思 (114660) | 液态 (168) | \n (1912) | 固态 (459) | *solid* (21) |

### `mars-color`

> Fact: The color of the planet fourth from the Sun is␣

Bridge **Mars** -> answer *red*; controls [Earth] / [blue]. category: multihop, status (B): eligible, label (B): neither, model's top word: red.
Why this group: J-lens bridge top-1 in 0% of band layers at the last token, distractor 100%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/mars-color__jlens.html) · [J++](slices/mars-color__jpp.html)

**Last token** `␣`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | I, a, A, s, T | –and, -H, -E, -C, -No | the, one, very, and, in | 12990 / 636 · 125971 / 1567 · 8434 / 647 |
| 4 | a, A, S, I, s | maths, 典礼, .nz, 港币, Maths | OpenGL, _angles, Pilar, víde, _SDK | 11148 / 562 · 172172 / 104482 · 164920 / 186315 |
| 8 | a, A, B, M, b | 典礼, VERY, صيد, ilee, canadian | colors, color, colored, colors, planets | 1869 / 807 · 29656 / 177460 · 1609 / 636 |
| 12 | a, A, S, S, B | odiac, ´t, lucky, iedo, pornstar | Colorado, Color, Arizona, stars, colors | 8654 / 466 · 125624 / 122975 · 445 / 572 |
| 16 | S, S, a, A, T | whats, biggest, bigger, english, gotten | Color, Arizona, [Blue], Sky, a | 13405 / 777 · 218934 / 15560 · 792 / 370 |
| 20 | a, ly, 亮, b, R | 啥, bigger, 0, 多少, whats | colors, color, colors, color, 颜色的 | 1449 / 92 · 186713 / 1289 · 652 / 73 |
| 24 | M, H, R, M, etr | bigger, much, totally, biggest, color | planet, colors, color, planetary, NASA | 2404 / 227 · 6756 / 836 · 56 / 359 |
| 28 | H, M, M, S, S | 什么, what, 0, 啥, 1 | planet, [Earth], Planet, NASA, color | 10305 / 84 · 5157 / 720 · 99 / 144 |
| 32 | M, X, C, a, M | whats, blah, colors, 什么, color | 2, 0, 3, 1, 4 | 23725 / 248 · 3052 / 2036 · 221 / 115 |
| 36 | X, M, ption, ict, A | 什么, 是, 什么意思, 是什么意思, 啥 | color, colored, 0, Color, X | 87701 / 528 · 43034 / 5043 · 4894 / 86 |
| 40 | M, B, S, a, H | color, colors, color, colors, Color | color, colored, the, colors, a | 5983 / 28 · 14872 / 393 · 4369 / 31 |
| 44 | ict, irt, H, 洲, ivo | color, colors, colors, color, orange | 1, 0, 2, 3, 4 | 9145 / 306 · 19228 / 129 · 6072 / 31 |
| 48 | either, 喜, 团, just, 火 | <u, \n, <b, <strong, <br | color, 1, white, black, a | 22625 / 138 · 1997 / 78 · 812 / 6 |
| 52 | redd, 红, 红色, 土, *red* | redd, color, Color, *red*, 红色 | *red*, redd, color, planet, orange | 398 / 5 · 62 / 4 · 21 / 1 |
| 56 | redd, 黄色, yellow, 红色, 橘 | orange, redd, yellow, 红色, planet | yellow, planet, *red*, orange, color | 25 / 12 · 19 / 6 · 14 / 3 |
| 60 | *red*, redd, orange, 橘, yellow | orange, *red*, redd, yellow, Orange | *red*, orange, yellow, redd, brown | 27 / 1 · 28 / 2 · 6 / 1 |
| 62 | *red*, redd, orange, yellow, *Red* | *red*, redd, orange, *Red*, yellow | *red*, redd, *Red*, redd, orange | 7 / 1 · 12 / 1 · 36 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `the` | colors (194) | colors (4328) | color (1735) | color (816) | color (496) | color (229) | sky (314) | sky (806) |
| `planet` | **Mars** (1) | Planet (8) | Planet (11) | planet (17) | planet (17) | planet (8) | Jupiter (2) | **Mars** (1) |
| `fourth` | 了 (158972) | s (231194) | 了 (112036) | uranus (8239) | 地球 (344) | planet (148) | planet (80) | from (100) |
| `from` | ς (12934) | s (27565) | planet (53) | 地球 (352) | 地球 (57) | NASA (60) | Sun (37) | the (20) |
| `the` | 旳 (91) | farther (57702) | colors (2042) | colors (1294) | color (79) | color (72) | stars (64) | sun (135) |
| `Sun` | aries (64) | —not (134) | Saturn (35) | Earth (20) | [Earth] (28) | [Earth] (23) | is (7) | is (4) |
| `is` | 大金 (255) | actually (37281) | much (802) | 什么意思 (1937) | planet (16) | color (25) | planet (7) | *red* (9) |
| `␣` | 典礼 (29664) | whats (218942) | bigger (6751) | whats (3114) | color (14870) | <u (1993) | orange (19) | *red* (12) |

### `person-firstname-newton`

> Fact: The first name of the scientist on whose head an apple is said to have fallen was

Bridge **Newton** -> answer *Isaac*; controls [Shakespeare] / [William]. category: person-firstname, status (B): eligible, label (B): neither, model's top word: Isaac.
Why this group: J-lens bridge top-1 in 6% of band layers at the last token, distractor 94%; J++ 12%.
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
| `an` | uminium (233755) | ely (83784) | supposedly (1520) | xxxxxxxx (583) | Einstein (3) | supposedly (27) | supposedly (42) | apple (221) |
| `apple` | apple (6858) | apple (2286) | apple (23) | apple (4) | apple (6) | supposedly (36) | supposedly (352) | fell (330) |
| `is` | colour (169507) | colour (37137) | supposedly (14380) | 什么 (5657) | famous (405) | supposedly (2275) | supposed (3229) | said (2052) |
| `said` | edly (138691) | edly (122949) | reputed (46356) | 什么 (38215) | 传说 (2252) | allegedly (1552) | have (1197) | to (55) |
| `to` | ‘s (128623) | er (45390) | \u (10) | famously (4) | 牛顿 (3) | 牛顿 (3) | discovered (4) | have (4) |
| `have` | recognised (27174) | favoured (9153) | reputed (3063) | 的 (518) | 砸 (12) | \n (114) | fallen (729) | fallen (310) |
| `fallen` | avourite (40110) | avourite (1151) | —or (70) | supposedly (4) | 据说 (37) | was (158) | was (159) | is (48) |
| `was` | 的 (204502) | indeed (134749) | chiefly (96279) | 什么 (4392) | name (107) | <u (23) | **Newton** (1) | *Isaac* (4) |


<a id="readers_disagree"></a>
## J-lens and J++ disagree

Eligible; the two lenses' band shares for the bridge differ by >= 0.5.

### `organ-location-heart`

> Fact: The part of the body that contains the organ that pumps blood is the

Bridge **heart** -> answer *chest*; controls [brain] / [head]. category: organ-location, status (B): eligible, label (B): neither, model's top word: chest.
Why this group: J-lens bridge top-1 in 6% of band layers at the last token, distractor 0%; J++ 82%.
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
| `organ` | er (137896) | er (1646) | organs (243) | 的 (2082) | organs (28) | organs (6) | called (13) | that (6) |
| `that` | raries (111087) | got (2322) | is (658) | 是什么 (62012) | humans (354) | humans (19) | organ (166) | pumps (581) |
| `pumps` | Watts (13679) | big (319) | pumps (14) | <u (730) | pumps (21) | pumps (17) | blood (141) | blood (44) |
| `blood` | s (12324) | s (336) | to (11) | \n (62) | blood (41) | blood (15) | throughout (28) | is (40) |
| `is` | colour (176981) | basically (2024) | 什么 (1475) | 什么 (6841) | 心脏 (4) | located (5) | called (36) | the (20) |
| `the` | 大金 (121865) | amongst (11030) | 哪一个 (22920) | 什么 (16440) | body (183) | torso (43) | *chest* (12) | *chest* (5) |


<a id="model_wrong"></a>
## Model answers wrong

Part B's clean_wrong: the model's top word is not the answer. Does the lens still see the bridge?

### `instr-hit-drums`

> Fact: The pair of wooden objects used to strike the instrument that keeps the beat at the back of a rock band is called

Bridge **drums** -> answer *sticks*; controls [piano] / [keys]. category: instr-played, status (B): clean_wrong, label (B): -, model's top word: drum.
Why this group: J-lens bridge top-1 in 12% of band layers at the last token, distractor 0%; J++ 0%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/instr-hit-drums__jlens.html) · [J++](slices/instr-hit-drums__jpp.html)

**Last token** `called`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | s, a, A, T, S | the, The, u, o, to | the, many, two, one, three | 78674 / 58053 · 8714 / 22147 · 3029 / 3717 |
| 4 | s, a, S, J, A | ed, .hpp, \xc, .jpg, Called | called, called, 媛媛, Рим, _called | 94917 / 62049 · 43950 / 11185 · 35818 / 31232 |
| 8 | s, a, A, A, S | .hpp, ness, everybody, .jpg, Called | called, aiss, 白鹭, famous, everybody | 73220 / 65482 · 10588 / 17277 · 38969 / 10538 |
| 12 | s, a, A, A, 叫做 | &quot, somebody, .hpp, 什麽, everybody | Dallas, Lass, Texas, Cairo, Ludwig | 94922 / 68332 · 45253 / 34771 · 19047 / 40292 |
| 16 | s, a, 叫做, a, B | ed, o, &quot, a, somebody | the, Call, a, Called, Cal | 97488 / 71413 · 42287 / 13172 · 16782 / 25959 |
| 20 | 叫做, 叫, called, 称为, a | a, called, a, &quot, somebody | names, called, something, famous, Raleigh | 131194 / 36207 · 66048 / 37088 · 49063 / 6319 |
| 24 | 叫做, a, called, a, 叫 | &quot, <b, called, a, a | called, the, a, name, an | 87156 / 45879 · 28148 / 29403 · 2574 / 1001 |
| 28 | 叫做, a, called, A, a | <u, <b, <strong, 什么, \xc | the, a, called, named, The | 84731 / 79094 · 21695 / 12668 · 3868 / 3290 |
| 32 | 叫做, called, a, IT, A | <u, 什么, 叫什么, \xc, <b | named, a, the, name, called | 44453 / 72220 · 15959 / 6778 · 9754 / 3597 |
| 36 | 叫做, called, 称为, 叫, a | 叫做, 叫, 叫什么, 称为, 什么 | name, called, the, a, named | 14729 / 29894 · 11440 / 4121 · 1706 / 539 |
| 40 | 叫做, a, called, 叫, a | 叫做, 称为, 叫, 叫什么, called | called, name, the, a, named | 30431 / 2970 · 881 / 1048 · 233 / 393 |
| 44 | 叫做, called, a, a, 称为 | 叫什么, 叫做, 称为, called, 叫 | called, a, name, the, something | 23008 / 2827 · 448 / 698 · 348 / 117 |
| 48 | 叫做, a, a, something, (s | <u, 叫什么, 叫做, <b, 叫 | something, name, called, the, a | 16295 / 3541 · 473 / 1901 · 82 / 348 |
| 52 | 什么呢, 叫做, something, 什么, collectively | 叫什么, <u, percussion, **drums**, “The | drum, instrument, percussion, **drums**, instruments | 1138 / 76 · 4 / 39 · 4 / 11 |
| 56 | 什么呢, percussion, rhythm, drum, what | drum, percussion, **drums**, 鼓, Drum | drum, **drums**, percussion, 鼓, drummer | 39 / 33 · 3 / 17 · 2 / 9 |
| 60 | drum, 鼓, *sticks*, claves, *sticks* | drum, **drums**, *sticks*, Drum, 鼓 | drum, Drum, *sticks*, **drums**, sn | 8 / 3 · 2 / 3 · 4 / 3 |
| 62 | drum, a, what, c, the | drum, **drums**, what, Drum, *sticks* | drum, **drums**, what, Drum, *sticks* | 6 / 7 · 2 / 5 · 2 / 5 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `the` | ­t (716) | folks (1784) | percussion (9) | 什么 (34) | percussion (4) | percussion (7) | rhythm (8) | drum (2) |
| `back` | ighbour (57930) | whilst (50303) | of (2458) | 的 (3930) | backstage (13) | behind (18) | of (34) | of (18) |
| `of` | –and (23222) | the (10865) | much (1586) | 什么意思 (702) | music (28) | orchestra (81) | orchestra (30) | the (13) |
| `a` | 网友评论 (22879) | Though (21973) | wooden (16) | 什么 (98) | 什么 (254) | 叫什么 (90) | orchestra (36) | marching (19) |
| `rock` | stone (11515) | -rock (25957) | -rock (159) | 摇滚 (177) | guitar (77) | music (60) | 乐队 (89) | band (75) |
| `band` | ster (294) | big (620) | music (96) | 什么 (81) | drummer (2) | drummer (2) | is (2) | are (7) |
| `is` | Shemale (141878) | amongst (44702) | 什么 (13197) | 什么 (7076) | 什么 (859) | called (203) | called (28) | called (6) |
| `called` | .hpp (10584) | ed (42292) | &quot (28151) | <u (15957) | 称为 (882) | <u (474) | drum (3) | drum (2) |

### `organ-acid-stomach`

> Fact: The strong liquid inside the organ that breaks down swallowed food is called

Bridge **stomach** -> answer *acid*; controls [heart] / [blood]. category: organ-function, status (B): clean_wrong, label (B): -, model's top word: gastric.
Why this group: J-lens bridge top-1 in 18% of band layers at the last token, distractor 0%; J++ 53%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/organ-acid-stomach__jlens.html) · [J++](slices/organ-acid-stomach__jpp.html)

**Last token** `called`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | s, a, T, S, A | the, u, The, o, For | the, many, two, one, three | 27327 / 3660 · 58645 / 23648 · 6004 / 3032 |
| 4 | s, a, s, S, S | ed, .jpg, .hpp, \xc, everybody | called, called, 媛媛, _called, -called | 43014 / 2713 · 36019 / 124485 · 108964 / 185700 |
| 8 | s, a, A, p, A | .hpp, .jpg, \xc, Famous, Called | called, aiss, famous, everybody, called | 37082 / 9918 · 74655 / 89099 · 127738 / 111541 |
| 12 | s, a, a, A, A | &quot, somebody, ed, everybody, .hpp | Dallas, Texas, the, Lass, Ludwig | 46318 / 7149 · 77339 / 95456 · 27978 / 25387 |
| 16 | s, a, a, 叫做, A | a, ed, o, called, famous | the, Call, a, Called, Castle | 95685 / 13096 · 67013 / 50109 · 50650 / 46143 |
| 20 | 叫做, 叫, called, a, a | a, called, called, o, &quot | medicine, called, Medicine, the, famous | 63397 / 16425 · 94450 / 35759 · 3300 / 103207 |
| 24 | 叫做, a, called, A, a | <b, <strong, <u, &quot, <br | called, name, medicine, the, Medicine | 64014 / 21411 · 81164 / 29360 · 1323 / 23385 |
| 28 | A, a, a, 叫做, R | <u, 什么, <b, <strong, \xc | the, Medicine, medicine, called, Name | 62098 / 18546 · 31116 / 17295 · 2280 / 11366 |
| 32 | 叫做, A, a, called, B | <u, 叫, 叫什么, 什么, \xc | Name, Medicine, name, medicine, named | 52775 / 30032 · 26028 / 21456 · 4640 / 18926 |
| 36 | 叫做, called, 称为, A, 叫 | 叫, 叫做, 称为, 叫什么, 简称 | name, Name, called, named, medical | 15940 / 8868 · 8712 / 6489 · 242 / 1342 |
| 40 | a, 叫做, called, a, A | 叫, 叫做, 称为, 叫什么, called | name, called, the, named, medical | 12801 / 7729 · 660 / 1623 · 83 / 504 |
| 44 | 叫做, called, a, a, 叫 | 叫做, 叫什么, 叫, 称为, called | called, the, name, a, named | 12322 / 6267 · 824 / 1124 · 59 / 411 |
| 48 | 叫做, a, a, called, A | 叫做, 叫什么, 叫, <u, called | name, called, the, medicine, chemical | 12573 / 4978 · 259 / 218 · 30 / 105 |
| 52 | 叫做, digestive, called, 什么呢, a | digestive, digestion, 胃酸, 叫做, saliva | 胃酸, digestive, digestion, *acid*, **stomach** | 21 / 24 · 18 / 16 · 5 / 4 |
| 56 | 胃, gastric, 胃酸, digestive, saliva | saliva, 胃酸, gastric, digestive, digestion | 胃酸, gastric, 胃, *acid*, **stomach** | 6 / 8 · 7 / 9 · 5 / 4 |
| 60 | gastric, digestive, **stomach**, 胃, 消化 | gastric, digestive, **stomach**, digestion, digest | **stomach**, gastric, digestive, 胃酸, 胃 | 3 / 13 · 3 / 13 · 1 / 14 |
| 62 | gastric, **stomach**, *acid*, digestive, bile | gastric, **stomach**, digestive, *acid*, saliva | **stomach**, gastric, digestive, *acid*, 胃酸 | 2 / 3 · 2 / 4 · 1 / 4 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `organ` | er (48534) | er (8983) | ically (3866) | 的 (533) | organs (16) | organs (27) | called (66) | called (56) |
| `that` | aveled (12681) | bigger (2391) | &amp (4736) | fluids (2005) | fluids (101) | brain (551) | protects (1527) | pumps (3261) |
| `breaks` | s (29481) | s (14986) | havoc (14628) | 的 (5865) | digestion (41) | digestion (43) | food (279) | down (277) |
| `down` | s (36306) | s (8092) | s (1026) | chemicals (660) | digestive (28) | foods (42) | food (188) | food (131) |
| `swallowed` | 嚓 (14774) | swallowed (638) | swallowed (49) | eaten (54) | swallowed (28) | foods (27) | food (94) | food (119) |
| `food` | er (21233) | a (7780) | -food (327) | 和 (204) | digestive (23) | digestive (24) | is (22) | is (128) |
| `is` | colour (52594) | 1 (15140) | 什么 (49766) | 什么 (6425) | chemicals (132) | called (119) | called (31) | called (5) |
| `called` | .hpp (74659) | a (67021) | <b (81166) | <u (26024) | 叫 (662) | 叫做 (255) | saliva (7) | gastric (2) |

### `planet-3-moons`

> Fact: The number of natural moons orbiting the planet third from the Sun is␣

Bridge **Earth** -> answer *1*; controls [Mars] / [2]. category: multihop, status (B): clean_wrong, label (B): -, model's top word: 0.
Why this group: J-lens bridge top-1 in 71% of band layers at the last token, distractor 0%; J++ 41%.
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/planet-3-moons__jlens.html) · [J++](slices/planet-3-moons__jpp.html)

**Last token** `␣`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | I, a, A, P, s | –and, -H, -E, -C, -A | the, very, one, and, in | 3911 / 14 · 37766 / 213578 · 2035 / 242145 |
| 4 | a, A, S, s, I | maths, .nz, pornstar, Vinci, Maths | víde, ーブ, OpenGL, …the, _SDK | 3572 / 13 · 172815 / 242153 · 238307 / 27514 |
| 8 | a, A, M, B, S | pornstar, avourite, صيد, maths, Busty | only, maths, stars, thanks, numbers | 866 / 9 · 169585 / 242150 · 1414 / 4096 |
| 12 | a, A, S, M, to | avourite, pornstar, maths, .nr, Maths | stars, Stars, and, star, Number | 772 / 15 · 145649 / 241381 · 25 / 626 |
| 16 | S, S, er, a, A | amongst, whilst, avourite, Whilst, anyways | and, the, in, as, a | 1132 / 12 · 118277 / 161 · 59 / 2115 |
| 20 | b, orbit, ly, 枚, fewer | [2], 3, *1*, 6, 4 | planet, planets, Saturn, moon, lunar | 55 / 478 · 19461 / 3 · 35 / 17561 |
| 24 | orbit, S, altogether, 枚, R | 数目, 6, 7, 3, [2] | asteroid, planet, Saturn, planets, asteroids | 1312 / 239 · 4513 / 12 · 30 / 5272 |
| 28 | number, HD, HD, as, M | 什么, <u, 多少, 有多少, 9 | asteroid, Saturn, planet, Jupiter, planets | 3872 / 47 · 916 / 24 · 40 / 977 |
| 32 | number, N, less, N, record | XXXX, 9, 7, [2], *1* | planet, asteroid, Saturn, Jupiter, planets | 16572 / 78 · 92 / 6 · 24 / 107 |
| 36 | orbit, number, orbits, 继, currently | planet, 地球, 行星, planet, 月球 | planet, asteroid, planetary, planets, Jupiter | 612 / 4644 · 22 / 94 · 24 / 267 |
| 40 | 已知, known, currently, orbit, number | planet, 月球, planet, planets, NASA | planet, planetary, Saturn, asteroid, planets | 592 / 6041 · 23 / 3492 · 15 / 459 |
| 44 | zero, 零, currently, known, orbits | 地球, planet, planet, NASA, asteroid | asteroid, planet, zero, planetary, number | 215 / 504 · 28 / 456 · 13 / 79 |
| 48 | zero, 零, zero, none, two | ZERO, NOTHING, 零, zero, NONE | zero, planet, planets, planetary, asteroid | 210 / 425 · 145 / 600 · 24 / 182 |
| 52 | zero, orbits, orbit, zero, moons | planet, asteroid, planets, planet, asteroids | planet, planets, 月球, planetary, asteroid | 10 / 47770 · 15 / 169874 · 104 / 169020 |
| 56 | moons, 卫星, moon, satellites, 衛星 | moons, 卫星, moon, Moon, Moon | moons, moon, Moon, Moon, 卫星 | 195 / 62105 · 64 / 199458 · 69 / 149237 |
| 60 | zero, 零, zero, two, Zero | zero, zero, two, moons, Zero | moons, moon, zero, Moon, satellites | 142 / 545 · 34 / 44 · 20 / 212108 |
| 62 | [2], 0, zero, two, 零 | [2], 0, *1*, 6, 3 | zero, two, 0, only, one | 32 / 16 · 38 / 3 · 42 / 85 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `the` | 五颜六色的 (3317) | entirety (976) | \u (13) | **Earth** (1) | planet (2) | planet (3) | planet (4) | planet (2) |
| `planet` | Planet (5) | Planet (11) | Planet (7) | planet (4) | planet (4) | planet (5) | Jupiter (2) | [Mars] (7) |
| `third` | 了 (230420) | 了 (227473) | newcom (18129) | uranus (180) | 地球 (12) | planet (15) | planet (45) | from (32) |
| `from` | s (137406) | s (90491) | planet (34) | 地球 (44) | 地球 (7) | **Earth** (1) | Sun (3) | the (4) |
| `the` | 旳 (23879) | entirety (39199) | moons (64) | moons (45) | 月球 (75) | currently (56) | Sun (22) | Sun (4) |
| `Sun` | aries (442) | a (319) | Saturn (2) | **Earth** (1) | **Earth** (1) | **Earth** (1) | planet (3) | is (23) |
| `is` | colour (183112) | amongst (220157) | nearer (90061) | famously (671) | planet (4) | **Earth** (1) | zero (41) | zero (106) |
| `␣` | pornstar (169637) | amongst (118276) | 数目 (4508) | XXXX (92) | planet (23) | ZERO (145) | moons (64) | [2] (39) |

