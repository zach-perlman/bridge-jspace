# Examples: exp10_lens_sanity (lens-eval multihop, space stripped), Qwen3.6-27B

Source run `results/exp10_lens_sanity/20261013-205936`, model Qwen/Qwen3.6-27B. Examples are drawn at random with seed 0, up to 3 per group; groups can overlap. Marks in the tables: **bridge**, *answer*, [distractor]. Ranks are word ranks (1 = top; spaces and punctuation removed) of the bridge (B) and the answer (A). Readers: logit lens (baseline), J-lens, J++.

| Group | Definition | Items in group | Shown |
|---|---|---|---|
| [All readers see it](#all_see) | Logit lens, J-lens and J++ all have the intermediate in their top 10. | 32 | 3 |
| [Only the lenses see it](#lenses_only) | J-lens or J++ in their top 10, the logit lens not. | 24 | 3 |
| [J++ sees it, the J-lens does not](#jpp_not_jlens) | J++ in its top 10, the J-lens not. | 16 | 3 |
| [No reader sees it](#none_see) | No reader has the intermediate in its top 10 at any layer. | 19 | 3 |
| [Model answers wrong](#model_wrong) | The model's greedy next token is not the target's first token. | 25 | 3 |

<a id="all_see"></a>
## All readers see it

Logit lens, J-lens and J++ all have the intermediate in their top 10.

### `holiday-independence-monthnum`

> Fact: The US Independence Day holiday is celebrated in month number

Bridge **July** -> answer *7*. other intermediates: -, model's top word: seven.
Why this group: best rank over layers at the last token: logit 1, jlens 0, jpp 2 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/holiday-independence-monthnum__jlens.html) · [J++](slices/holiday-independence-monthnum__jpp.html)

**Last token** `number`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | T, S, p, C, M | the, 's, th, 1, h | the, people, and, small, about | 10784 / 183 · 2972 / 117 · 781 / 242143 |
| 4 | T, S, T, a, 1 | number, number, cash, umber, stants | number, numbering, number, numbers, numbers | 8150 / 180 · 98598 / 117088 · 11683 / 32781 |
| 8 | A, A, a, I, er | 数, Nº, 一, ered, 一数 | numbers, numbering, number, numbered, numbers | 13641 / 531 · 16076 / 44 · 173 / 184615 |
| 12 | A, U, ing, i, U | NUMBER, Nummer, Number, 一数, number | Number, Nummer, (NUM, NUMBER, NM | 6721 / 307 · 37060 / 97 · 728 / 33354 |
| 16 | ing, U, A, U, y | number, Number, NUMBER, number, Nº | Number, Nummer, NUMBER, Numbers, Numero | 6726 / 239 · 12433 / 88 · 2230 / 25368 |
| 20 | 性的, ly, F, 第, U | 什么, NUMBER, Number, number, number | numbers, number, month, of, months | 5958 / 545 · 9557 / 102 · 449 / 15200 |
| 24 | F, N, 性的, H, h | 什么, NUMBER, number, Number, 哪 | number, month, numbers, of, number | 3857 / 590 · 857 / 7 · 34 / 9183 |
| 28 | number, M, M, N, F | NUMBER, number, Number, 什么, -number | Number, number, Numbers, NUMBER, -number | 7126 / 242 · 1413 / 67 · 90 / 236 |
| 32 | number, P, N, number, g | number, NUMBER, Number, 什么, number | Number, number, Numbers, -number, Number | 4714 / 152 · 155 / 16 · 85 / 41 |
| 36 | number, -number, 序号, number, M | NUMBER, number, Number, 什么, number | Number, number, NUMBER, -number, Number | 5570 / 80 · 181 / 132 · 66 / 116 |
| 40 | N, number, M, 序号, ordinal | NUMBER, Number, number, number, -number | number, month, number, numbers, numbered | 3446 / 9 · 159 / 81 · 46 / 235 |
| 44 | number, 1, -number, N, M | number, NUMBER, -number, Number, 编号 | number, numbered, -number, numbers, number | 2488 / 15 · 246 / 85 · 70 / 68 |
| 48 | number, 序号, 相对于, -number, number | number, -number, NUMBER, Number, number | number, Number, -number, numbered, number | 12025 / 33 · 221 / 53 · 216 / 398 |
| 52 | number, unner, -number, 的第, number | number, -number, Number, number, NUMBER | Number, number, -number, NUMBER, Num | 826 / 280 · 58 / 336 · 213 / 125451 |
| 56 | number, 序号, -number, ordinal, ingu | -number, number, NUMBER, Number, number | Number, number, -number, NUMBER, numbered | 127 / 1058 · 65 / 623 · 141 / 48815 |
| 60 | seven, six, 七, four, Seven | seven, six, four, eight, five | seven, **July**, month, seventh, US | 11 / 22 · 11 / 101 · 2 / 84195 |
| 62 | seven, Seven, seven, **July**, six | seven, Seven, seven, six, eight | seven, *7*, six, five, four | 4 / 8 · 9 / 13 · 49 / 2 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `Independence` | avour (1092) | whilst (1505) | Independence (109) | America (59) | Independence (73) | Independence (84) | Declaration (817) | Day (691) |
| `Day` | celebrations (25) | honour (173) | celebrations (8) | celebration (15) | celebration (25) | celebration (22) | celebration (49) | is (23) |
| `holiday` | ‘s (34391) | holiday (10824) | holiday (233) | holiday (82) | holiday (108) | holiday (57) | celebrates (122) | is (43) |
| `is` | uken (202336) | whilst (65477) | amongst (15543) | 什么意思 (10399) | birthdays (34) | celebration (16) | celebrated (2) | **July** (1) |
| `celebrated` | ’s (9946) | throughout (5663) | celebrations (515) | celebrations (406) | celebrations (70) | celebration (34) | annually (3) | on (2) |
| `in` | ighbour (60946) | areas (15274) | Americans (340) | America (194) | America (6) | September (3) | September (3) | **July** (1) |
| `month` | iest (6064) | of (26436) | of (98) | 什么 (103) | month (21) | month (15) | number (19) | seven (2) |
| `number` | 数 (16062) | number (12436) | 什么 (855) | number (156) | NUMBER (160) | -number (222) | number (65) | seven (9) |

### `inv-roots-opposite`

> Fact: The direction opposite to the one tree roots grow is "

Bridge **down** -> answer *up*. other intermediates: -, model's top word: up.
Why this group: best rank over layers at the last token: logit 5, jlens 5, jpp 1 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/inv-roots-opposite__jlens.html) · [J++](slices/inv-roots-opposite__jpp.html)

**Last token** `"`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | s, I, A, A, S | s, ness, -color, ization, tures | the, and, New, one, many | 1829 / 220 · 8313 / 21125 · 944 / 393 |
| 4 | s, a, b, S, A | anceled, ynec, Canceled, canceled, schluss | 南国, someday, Ее, 篇二, airplanes | 2529 / 207 · 111721 / 221893 · 34424 / 104474 |
| 8 | s, M, R, P, H | Shemale, Blowjob, anceled, celed, schluss | harbor, ANCELED, utoff, "s, jewelry | 1687 / 197 · 183711 / 202182 · 20916 / 1969 |
| 12 | s, R, P, R, S | Shemale, Blowjob, eness, ness, pornstar | s, Legend, Los, Arizona, Earth | 1648 / 83 · 163207 / 172388 · 2979 / 892 |
| 16 | P, S, able, E, y | s, eness, anyways, ness, niest | Big, s, Trick, Mystic, Magic | 2198 / 195 · 23937 / 27358 · 1608 / 971 |
| 20 | S, ug, eres, J, s | s, ness, m, eness, su | s, stuff, and, eye, old | 4335 / 205 · 1934 / 379 · 330 / 125 |
| 24 | S, J, s, R, B | s, ness, eness, anyways, way | direction, s, sea, wo, ocean | 1460 / 56 · 6288 / 690 · 811 / 167 |
| 28 | M, y, S, g, R | ness, s, m, whats, freaking | s, Earth, m, arrow, <br | 9725 / 606 · 4097 / 394 · 893 / 276 |
| 32 | y, ute, ing, l, un | whats, WRONG, ness, freaking, scary | m, Earth, arrow, Arrow, s | 15427 / 174 · 22668 / 2468 · 3545 / 1480 |
| 36 | X, S, opp, 竖直, 的方向 | whats, 什么, 什么意思, science, freaking | Earth, m, s, science, water | 122162 / 157 · 31636 / 2069 · 6010 / 836 |
| 40 | 垂直, X, 竖直, S, 的方向 | Earth, vertical, vertical, upward, vertically | direction, vertical, sky, upward, north | 11542 / 106 · 1190 / 492 · 88 / 92 |
| 44 | X, ward, S, x, H | direction, Earth, direction, Direction, sky | sky, direction, north, Earth, â | 23004 / 73 · 1607 / 1404 · 102 / 157 |
| 48 | X, opp, S, 加拿大, H | &quot, \n, <u, sky, \u | sky, direction, Earth, earth, directions | 10858 / 67 · 2127 / 474 · 425 / 282 |
| 52 | upward, 的方向, direction, 向上, upwards | upward, upwards, 向上, direction, direction | direction, upward, upwards, 的方向, directional | 797 / 30 · 372 / 117 · 310 / 87 |
| 56 | upward, upwards, 向上, *up*, toward | upward, upwards, 向上, 向上的, downward | upward, upwards, *up*, 向上, Up | 31 / 4 · 65 / 14 · 16 / 3 |
| 60 | *up*, *up*, Up, Up, upward | *up*, Up, *up*, upward, Up | *up*, sky, Up, upward, *up* | 6 / 1 · 10 / 1 · 6 / 1 |
| 62 | *up*, *up*, Up, Up, upward | *up*, *up*, Up, Up, **down** | *up*, **down**, Up, sky, *up* | 9 / 1 · 6 / 1 · 2 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `to` | rhythm (50495) | the (1589) | direction (1144) | direction (8854) | direction (3177) | direction (949) | east (174) | west (24) |
| `the` | Tire (5303) | of (211) | of (463) | Earth (21527) | weather (4458) | winter (1364) | direction (1795) | direction (140) |
| `one` | slaught (69178) | in (299) | that (537) | 是什么意思 (6459) | direction (6344) | direction (2619) | toward (1585) | that (367) |
| `tree` | /tree (68587) | amongst (6539) | tree (1051) | trees (13967) | trees (5872) | trees (5373) | shadows (59563) | grows (4153) |
| `roots` | eness (2834) | s (218) | trees (4696) | trees (35136) | roots (5860) | roots (1302) | grows (3536) | grow (1268) |
| `grow` | ings (41) | amongst (22) | though (138) | 什么 (1098) | downward (318) | downwards (69) | is (173) | is (12) |
| `is` | avour (4406) | though (270) | farther (2050) | 什么意思 (23615) | direction (5861) | direction (5348) | upward (65) | *up* (6) |
| `"` | Shemale (183705) | s (23944) | s (6291) | whats (22670) | Earth (1193) | &quot (2129) | upward (66) | *up* (6) |

### `rhyme-fix-halved`

> Fact: Half of the number whose name rhymes with fix is

Bridge **six** -> answer *3*. other intermediates: -, model's top word: six.
Why this group: best rank over layers at the last token: logit 0, jlens 0, jpp 0 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/rhyme-fix-halved__jlens.html) · [J++](slices/rhyme-fix-halved__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, P, A | –and, The, It, the, For | <unk, <data, \xc, Counseling, Connecticut | 15528 / 78 · 7082 / 11970 · 1409 / 242149 |
| 4 | S, a, p, P, A | MIS, (IS, CIS, IS, miser | the, and, little, in, only | 34215 / 134 · 3246 / 242152 · 7928 / 82523 |
| 8 | S, S, P, P, H | luckily, thankfully, avour, ness, chance | thanks, only, the, also, even | 78259 / 174 · 158533 / 242144 · 1688 / 83716 |
| 12 | s, P, p, B, S | really, luckily, anyways, amongst, quite | Texas, AIS, BIS, the, Kansas | 62318 / 194 · 44181 / 242005 · 7240 / 32740 |
| 16 | B, B, w, F, M | really, pretty, bigger, kinda, though | Kais, Fairy, the, Texas, a | 128663 / 232 · 61317 / 148649 · 18564 / 9085 |
| 20 | nam, E, b, uge, m | though, nearer, actually, 跟, utterly | half, now, to, in, and | 205094 / 37 · 105562 / 82223 · 3501 / 10987 |
| 24 | nam, m, IT, B, m | nearer, though, just, likewise, ought | the, in, to, half, more | 130512 / 82 · 15312 / 59040 · 988 / 29838 |
| 28 | f, m, a, (s, m | likewise, just, nearer, utterly, similarly | the, number, a, in, word | 99257 / 231 · 12717 / 123445 · 1151 / 612 |
| 32 | A, A, E, E, (s | \u, 什么意思, &nbsp, \n, 怎么 | the, to, 1, number, name | 146726 / 39 · 39288 / 799 · 1078 / 9 |
| 36 | numer, onda, number, 在了地上, 提起 | number, 什么意思, what, NUMBER, math | number, Number, numbers, Numbers, math | 100562 / 1544 · 208 / 3372 · 131 / 1304 |
| 40 | number, 数量的, 是多少, number, numer | number, numbers, Number, math, NUMBER | number, numbers, Number, math, Numbers | 89436 / 194 · 57 / 692 · 41 / 31485 |
| 44 | number, 等于, 叫做, 合, adge | number, numbers, Number, fifty, math | number, numbers, half, five, one | 46567 / 290 · 14 / 15838 · 6 / 264 |
| 48 | otyp, 禁, 叫做, multiplied, ths | number, eight, seven, forty, five | number, numbers, mathematical, math, numer | 11623 / 377 · 10 / 5033 · 11 / 82273 |
| 52 | 等于, equal, onex, เท่ากับ, equals | **six**, sixty, fifty, forty, five | number, math, **six**, gold, hex | 77 / 51433 · 1 / 8823 · 3 / 242139 |
| 56 | equal, 等于, **six**, 六, equals | **six**, sixty, seven, eight, five | equal, number, **six**, thirty, called | 3 / 217 · 1 / 1557 · 3 / 27887 |
| 60 | **six**, equal, five, eight, seven | **six**, seven, five, eight, nine | equal, fifteen, **six**, thirty, ten | 1 / 1607 · 1 / 12841 · 3 / 235700 |
| 62 | **six**, equal, five, ten, eight | **six**, seven, five, eight, sixty | equal, **six**, five, seven, nine | 1 / 3423 · 1 / 4200 · 2 / 80 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `number` | ings (47895) | of (1264) | of (5021) | 什么意思 (25519) | number (854) | number (134) | represented (743) | of (59) |
| `whose` | ся (167917) | ся (16288) | utter (24197) | 是什么意思 (91084) | arithmetic (1096) | whose (34) | half (806) | square (174) |
| `name` | urname (22263) | called (4517) | name (18220) | name (75449) | name (1373) | name (117) | begins (1378) | starts (3012) |
| `rh` | ellow (79774) | s (35912) | rh (63175) | rhyme (223818) | rhyme (191249) | rhyme (184452) | rh (154025) | ymes (31001) |
| `ymes` | &quot (33641) | with (6096) | with (8773) | whats (187068) | math (16412) | rhyme (3599) | with (1980) | with (287) |
| `with` | s (8124) | s (2862) | words (11590) | rhyme (180421) | rhyme (12143) | rhyme (5609) | eighty (22) | eight (7) |
| `fix` | er (43003) | er (2771) | er (541) | er (2044) | er (204) | is (18) | is (5) | is (15) |
| `is` | luckily (158531) | really (61326) | nearer (15575) | \u (39291) | number (57) | number (10) | **six** (1) | **six** (1) |


<a id="lenses_only"></a>
## Only the lenses see it

J-lens or J++ in their top 10, the logit lens not.

### `greatwall-ocean`

> Fact: The ocean east of the country that built the Great Wall is the

Bridge **China** -> answer *Pacific*. other intermediates: -, model's top word: Yellow.
Why this group: best rank over layers at the last token: logit 11, jlens 1, jpp 1 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/greatwall-ocean__jlens.html) · [J++](slices/greatwall-ocean__jpp.html)

**Last token** `the`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, S, A, in | The, –and, It, For, Or | New, many, Connecticut, the, Arkansas | 10181 / 14665 · 20180 / 24785 · 1634 / 3712 |
| 4 | a, for, to, in, s | CSL, 데미, Celebrity, .Pro, セレ | egasus, 情人节, 碧, ensburg, _pcm | 5027 / 21869 · 4883 / 103281 · 136508 / 198790 |
| 8 | a, s, s, c, M | 大金, Vorte, VERY, ustralian, igan | Colorado, Kans, color, Colorado, colors | 6102 / 14522 · 205269 / 202483 · 77906 / 328 |
| 12 | A, a, M, to, M | biggest, chance, fame, ´s, asian | and, ocean, Ocean, *Pacific*, The | 3208 / 47196 · 38752 / 12585 · 551 / 4 |
| 16 | w, H, c, Y, H | biggest, best, one, one, bigger | and, the, The, as, for | 16024 / 53363 · 4067 / 2018 · 1772 / 76 |
| 20 | ough, enc, Enc, 陆, 海 | Ocean, Ocean, ocean, 海域, oceans | ocean, marine, maritime, sea, 海域 | 2060 / 1343 · 40 / 6 · 1276 / 193 |
| 24 | g, 陆, ense, 海, sea | Ocean, ocean, oceans, Ocean, Atlantic | ocean, sea, marine, Ocean, maritime | 1096 / 5761 · 50 / 11 · 256 / 71 |
| 28 | b, g, 陆, 怎, l | ocean, Ocean, coastal, oceans, Atlantic | ocean, Ocean, coastal, Sea, sea | 9138 / 4997 · 59 / 20 · 415 / 60 |
| 32 | b, iro, 休, 限定, unge | ocean, Ocean, coastal, oceans, Atlantic | ocean, Ocean, coastal, Sea, marine | 4562 / 4679 · 79 / 16 · 421 / 50 |
| 36 | 限定, 边的, -facing, 拉克, addy | ocean, Ocean, coastal, Ocean, oceans | ocean, coastal, Ocean, Sea, sea | 1298 / 33135 · 16 / 27 · 97 / 47 |
| 40 | -facing, 边的, alis, 沿岸, 海洋 | ocean, Ocean, Ocean, oceans, 海洋 | ocean, sea, Ocean, marine, Sea | 385 / 2380 · 49 / 28 · 75 / 18 |
| 44 | 边的, -facing, name, reeze, called | Ocean, ocean, oceans, Ocean, Atlantic | ocean, Ocean, sea, Atlantic, Sea | 179 / 19967 · 22 / 7 · 26 / 8 |
| 48 | ses, sea, called, 叫做, ocratic | Ocean, ocean, Ocean, oceans, Maritime | ocean, Ocean, Sea, sea, oceans | 645 / 9385 · 29 / 10 · 32 / 12 |
| 52 | 太平洋, acific, Asian, 亚洲, 中国的 | Ocean, Asian, Asia, Sea, **China** | Ocean, Sea, ocean, sea, Asian | 30 / 48 · 6 / 6 · 17 / 12 |
| 56 | 太平洋, 黄海, *Pacific*, 东海, *Pacific* | *Pacific*, 太平洋, *Pacific*, 东海, Asian | *Pacific*, 太平洋, Asian, Chinese, 东海 | 25 / 3 · 10 / 1 · 8 / 1 |
| 60 | Yellow, Yellow, 黄海, yellow, 黄 | Yellow, *Pacific*, Sea, yellow, Yellow | Yellow, 黄海, yellow, Huang, *Pacific* | 59 / 7 · 23 / 2 · 8 / 5 |
| 62 | Yellow, *Pacific*, East, yellow, Sea | Yellow, *Pacific*, Sea, East, yellow | *Pacific*, Yellow, East, Sea, yellow | 13 / 3 · 8 / 2 · 11 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `country` | 's (5284) | 's (127) | country (25) | countries (31) | countries (16) | countries (14) | Canada (7) | of (4) |
| `that` | aveled (86308) | bigger (228) | nations (9) | 什么 (49) | countries (7) | countries (3) | contains (128) | borders (79) |
| `built` | rastructure (66235) | big (50) | Britain (7) | 造船 (72) | 建造 (25) | 建造 (31) | Statue (218) | the (156) |
| `the` | .But (76595) | big (223) | Britain (3) | 什么意思 (13) | ships (21) | famous (23) | Statue (525) | Statue (592) |
| `Great` | s (2145) | s (614) | Great (2) | civilizations (4) | **China** (1) | **China** (2) | Barrier (65) | Wall (68) |
| `Wall` | a (386) | of (21) | of (2) | **China** (1) | **China** (1) | **China** (1) | is (2) | of (13) |
| `is` | anyways (130734) | bigger (162) | **China** (1) | **China** (1) | **China** (1) | **China** (1) | **China** (1) | **China** (1) |
| `the` | 大金 (205269) | biggest (4066) | Ocean (50) | ocean (79) | ocean (49) | Ocean (30) | *Pacific* (10) | Yellow (8) |

### `month-1-godof`

> Fact: The first month of the year is named after the Roman god of

Bridge **January** -> answer *beginnings*. other intermediates: -, model's top word: beginnings.
Why this group: best rank over layers at the last token: logit 23, jlens 86, jpp 6 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/month-1-godof__jlens.html) · [J++](slices/month-1-godof__jpp.html)

**Last token** `of`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, I, and, S | –and, a, the, The, or | people, niest, everyone, Truman, itian | 8797 / 128234 · 13611 / 71542 · 70216 / 96695 |
| 4 | 1, and, a, p, a | @g, Guta, 芷, bed, .Pro | goddess, 女神, _legend, gods, 神 | 14660 / 126813 · 197372 / 141470 · 50843 / 67899 |
| 8 | p, c, M, P, C | -E, -W, …I, -g, -L | gods, goddess, mythology, 神话, 祭祀 | 18907 / 133429 · 117139 / 160106 · 84409 / 114179 |
| 12 | P, s, c, i, p | land, religion, ness, ding, gods | gods, goddess, Gods, mythology, Goddess | 20547 / 128353 · 232890 / 16734 · 104516 / 21285 |
| 16 | B, P, D, g, s | god, -esque, idol, gods, fighting | Gods, mythology, gods, God, and | 25083 / 120487 · 218501 / 4544 · 56547 / 17189 |
| 20 | g, d, 示, Apollo, ose | god, d, gods, idol, worship | Rome, Roman, gods, 罗马, goddess | 3631 / 110920 · 27833 / 11669 · 1487 / 6548 |
| 24 | P, g, o, T, 衔 | Roman, gods, Rome, god, worship | Roman, Rome, Romans, Latin, рим | 19068 / 38829 · 19872 / 7154 · 563 / 14264 |
| 28 | P, c, g, C, 草 | gods, mythology, deity, god, worship | Roman, Rome, Gods, deity, god | 25831 / 8229 · 52590 / 12282 · 1870 / 6817 |
| 32 | P, c, g, the, C | gods, uranus, mythology, deity, god | Roman, Rome, Gods, mythology, gods | 17719 / 9123 · 55605 / 42298 · 2681 / 9981 |
| 36 | uis, vice, g, uego, 万物 | gods, 罗马, Zeus, mythology, Apollo | Roman, Rome, рим, Romans, 罗马 | 6408 / 23 · 2943 / 5010 · 363 / 2240 |
| 40 | ogne, 掌管, 新旧, *beginnings*, 槐 | gods, god, ancient, Apollo, Roman | Roman, Jupiter, ancient, Saturn, god | 3988 / 4 · 423 / 956 · 77 / 782 |
| 44 | g, T, alm, \n, 占 | \n, <br, <span, <u, underworld | ancient, Roman, underworld, mythology, father | 4649 / 612 · 970 / 875 · 11 / 524 |
| 48 | T, \n, g, 占, alm | underworld, gods, evil, civilization, friendships | mythology, underworld, gods, ancient, aging | 2420 / 1444 · 1327 / 272 · 4980 / 447 |
| 52 | 老年, 什么的, 瓮, 老人, 翁 | honesty, mischief, underworld, gods, friendships | Jupiter, Saturn, 瓮, Rome, Pluto | 463 / 30 · 2489 / 29 · 3192 / 186 |
| 56 | *beginnings*, beginning, initiation, thresholds, 老年 | *beginnings*, gates, endings, 开端, openings | *beginnings*, beginning, gates, Beginning, boundaries | 360 / 1 · 2102 / 1 · 1152 / 1 |
| 60 | *beginnings*, door, Begin, beginning, begin | *beginnings*, gates, doors, door, beginning | gates, door, doors, Begin, beginning | 174 / 1 · 345 / 1 · 298 / 7 |
| 62 | door, *beginnings*, doors, beginning, Jan | *beginnings*, gates, doors, thresholds, door | *beginnings*, doors, gates, beginning, door | 23 / 2 · 89 / 1 · 1724 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `year` | 's (51) | in (36) | year (2) | year (2) | year (5) | year (6) | is (2) | is (2) |
| `is` | therefore (14652) | only (1650) | only (31) | <u (6) | month (3) | month (2) | **January** (1) | **January** (1) |
| `named` | ighbor (54222) | –and (4699) | because (32) | <u (342) | 命名 (95) | named (162) | after (3) | **January** (1) |
| `after` | ments (22806) | famous (23080) | Roman (28) | 什么 (1095) | Roman (57) | goddess (141) | Saturn (16) | Jan (2) |
| `the` | .L (66095) | o (19348) | Roman (3) | &nbsp (18) | Roman (8) | Roman (30) | Roman (395) | Roman (144) |
| `Roman` | Roman (97366) | Roman (175166) | Roman (11845) | Roman (32631) | Roman (4049) | Roman (12784) | goddess (5116) | god (469) |
| `god` | ness (124737) | god (133203) | god (50756) | god (72437) | gods (40223) | <u (69432) | Saturn (100) | Jan (7) |
| `of` | -E (117175) | god (218510) | Roman (19872) | gods (55606) | gods (424) | underworld (1323) | *beginnings* (2101) | *beginnings* (89) |

### `spider-legs`

> Fact: The number of legs on the animal that spins webs is

Bridge **spider** -> answer *8*. other intermediates: -, model's top word: greater.
Why this group: best rank over layers at the last token: logit 32, jlens 2, jpp 0 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/spider-legs__jlens.html) · [J++](slices/spider-legs__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, S, s, P | –and, The, the, It, For | <unk, <data, <b, Connecticut, \xc | 24826 / 161 · 160440 / 3118 · 156078 / 242146 |
| 4 | a, P, S, A, T | Краси, 률은, 港币, cristi, 률 | OpenGL, 优秀共产党员, Wichita, europé, 文艺演出 | 32710 / 151 · 76488 / 242142 · 237238 / 198875 |
| 8 | s, S, a, m, t | ner, athon, name, luckily, lucky | animal, biologist, 绵阳, Animal, 博物 | 3987 / 347 · 32789 / 175943 · 25 / 128610 |
| 12 | s, m, a, M, s | though, quite, merely, truly, really | animal, and, the, beast, animals | 2096 / 377 · 6729 / 48144 · 90 / 159033 |
| 16 | B, R, B, M, E | though, truly, amongst, just, really | the, Woods, in, and, a | 5897 / 2023 · 15937 / 24804 · 372 / 91248 |
| 20 | nam, m, B, M, R | though, Though, 怎样, 跟, truly | animals, animal, often, many, creature | 6004 / 9628 · 44559 / 28755 · 41 / 124825 |
| 24 | nam, m, B, P, B | \uff, 怎样, 哪一个, 什么, &nbsp | many, animal, often, spiders, much | 2144 / 471 · 2800 / 14587 · 6 / 159879 |
| 28 | m, M, M, m, P | 哪一个, —that, eldom, 什么, truly | **spider**, Spider, spiders, the, insect | 2138 / 2108 · 147 / 31566 · 1 / 22702 |
| 32 | un, utton, in, Un, A | 什么, 什么意思, 是什么, <u, 怎么 | known, to, in, insect, and | 11751 / 1137 · 296 / 722 · 24 / 4259 |
| 36 | 陆, nte, MO, 纲, 的是 | 什么, 什么意思, 是什么, 是什么意思, 怎么 | animal, insect, animals, insects, 昆虫 | 1852 / 4460 · 43 / 32701 · 10 / 17259 |
| 40 | 捕, T, 门的, E, 尊 | spiders, insects, 昆虫, animals, **spider** | **spider**, animal, insect, insects, animals | 108 / 2198 · 5 / 48436 · 1 / 45105 |
| 44 | (s, typically, compared, T, 类 | spiders, insects, **spider**, animals, insect | insect, **spider**, number, animal, insects | 330 / 967 · 3 / 19922 · 2 / 861 |
| 48 | compared, 比, greater, 相较于, 乎 | compared, spiders, insects, **spider**, animals | **spider**, number, animal, spiders, insect | 41 / 915 · 4 / 5632 · 1 / 58207 |
| 52 | greater, 大于, typically, usually, 小于 | greater, fewer, 大于, bigger, number | **spider**, number, greater, insect, four | 205 / 892 · 80 / 15713 · 1 / 225187 |
| 56 | greater, 偶, 大于, greater, equal | greater, greater, equal, Greater, larger | greater, number, **spider**, less, equal | 88 / 356 · 45 / 2128 · 3 / 54686 |
| 60 | greater, eight, less, four, greater | greater, eight, four, less, larger | greater, less, Greater, equal, larger | 196 / 56 · 93 / 864 · 10 / 29661 |
| 62 | greater, eight, four, less, usually | eight, greater, four, less, equal | greater, equal, larger, more, less | 214 / 75 · 177 / 133 · 674 / 20 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `legs` | Legs (71681) | s (16521) | in (3499) | animals (192) | legs (105) | legs (119) | humans (13) | of (15) |
| `on` | &nbsp (131445) | though (21264) | &nbsp (7259) | kids (321) | animals (153) | animals (36) | spiders (2) | a (8) |
| `the` | &nbsp (73277) | s (17650) | amongst (5166) | kids (917) | animals (227) | animals (80) | legs (4) | **spider** (1) |
| `animal` | ’s (35427) | animal (17608) | Animal (3067) | animals (851) | animals (699) | animals (310) | is (237) | is (34) |
| `that` | raries (146401) | got (28001) | nearer (67989) | 什么 (8788) | animals (451) | animals (2075) | humans (485) | eats (410) |
| `spins` | spinning (238) | just (421) | **spider** (1) | spiders (2) | spiders (2) | spiders (2) | webs (2) | webs (3) |
| `webs` | ing (377) | ing (65) | **spider** (1) | spiders (2) | spiders (2) | spiders (2) | **spider** (1) | is (16) |
| `is` | ner (32765) | though (15943) | \uff (2798) | 什么 (296) | spiders (5) | compared (4) | greater (45) | eight (177) |


<a id="jpp_not_jlens"></a>
## J++ sees it, the J-lens does not

J++ in its top 10, the J-lens not.

### `func-filters-count`

> Fact: In humans, the number of organs that filter blood to make urine is

Bridge **kidney** -> answer *2*. other intermediates: -, model's top word: two.
Why this group: best rank over layers at the last token: logit 192, jlens 25, jpp 0 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/func-filters-count__jlens.html) · [J++](slices/func-filters-count__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, 1 | –and, The, the, It, For | <unk, Connecticut, \xc, <b, <data | 35826 / 30 · 50219 / 1173 · 170104 / 242153 |
| 4 | a, S, S, T, s | 港币, 专栏收录该内容, 률은, 认认真, Hidal | OpenGL, 孔雀, 优秀共产党员, 凤凰, _SDK | 31640 / 80 · 168520 / 242149 · 67497 / 142099 |
| 8 | a, l, A, m, l | colour, avour, avourite, Colour, favour | _SDK, 湿地公园, 绵阳, **kidney**, 肾脏 | 14172 / 122 · 129227 / 201982 · 4 / 218319 |
| 12 | a, A, s, l, I | amongst, only, quite, even, much | IS, healthy, the, nis, just | 6389 / 112 · 171282 / 37079 · 622 / 163886 |
| 16 | a, A, M, I, B | just, even, basically, only, actually | IS, the, and, in, a | 7210 / 167 · 74592 / 169 · 3902 / 132515 |
| 20 | A, o, 器官, I, m | \uff, actually, chiefly, merely, many | organs, **kidney**, hospitals, kidneys, organ | 604 / 550 · 54911 / 2031 · 2 / 201754 |
| 24 | l, L, m, o, l | 哪一个, \uff, &nbsp, vastly, uniquely | **kidney**, kidneys, organs, 肾脏, water | 680 / 460 · 2219 / 51493 · 1 / 82249 |
| 28 | M, m, A, M, l | 什么, 是什么, <u, what, What | **kidney**, kidneys, organs, hospitals, 肾脏 | 1690 / 401 · 428 / 3928 · 1 / 29308 |
| 32 | m, A, M, in, a | 什么, 是什么, 什么意思, 是什么意思, <u | only, in, **kidney**, known, kidneys | 12499 / 2137 · 4537 / 1476 · 3 / 10286 |
| 36 | 叫做, 只有一个, distinct, A, 数量 | 什么, 是什么, 什么意思, 是什么意思, ONLY | only, number, organs, **kidney**, one | 1589 / 280 · 1403 / 2984 · 4 / 3691 |
| 40 | 叫做, one, singular, 只有一个, distinct | kidneys, ONLY, 什么, 只有一个, 肾脏 | only, number, one, **kidney**, kidneys | 292 / 385 · 9 / 22064 · 4 / 55269 |
| 44 | 数量, one, at, 1, L | 数量, number, 的数量, count, kidneys | one, number, count, two, single | 1509 / 15 · 37 / 1719 · 16 / 754 |
| 48 | one, 的数量, 数量, 叫做, 数量为 | number, TWO, number, <br, \n | number, one, count, two, only | 1944 / 55 · 189 / 591 · 13 / 31080 |
| 52 | typically, 俩, two, usually, equal | number, TWO, two, equals, NUMBER | number, count, two, pair, 的数量 | 2774 / 49 · 785 / 956 · 19 / 234992 |
| 56 | two, equal, greater, typically, usually | two, TWO, equal, two, number | number, number, two, one, Number | 755 / 32 · 381 / 472 · 40 / 30669 |
| 60 | two, one, equal, Two, greater | two, one, equal, TWO, Two | equal, one, less, exactly, usually | 374 / 150 · 198 / 1204 · 43 / 218546 |
| 62 | two, one, equal, greater, less | two, one, TWO, equal, greater | two, one, equal, greater, known | 214 / 114 · 200 / 155 · 714 / 54 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `organs` | ة (8019) | o (2003) | organs (87) | organs (170) | organs (18) | organs (98) | organs (141) | is (1451) |
| `that` | raries (71427) | people (11058) | people (10795) | is (3360) | organs (40) | organs (184) | organs (130) | produce (308) |
| `filter` | er (11058) | er (3712) | /filter (86) | 什么 (275) | 过滤 (55) | /filter (56) | blood (77) | toxins (41) |
| `blood` | s (22736) | s (8223) | -blood (860) | blood (571) | 血液 (44) | blood (42) | is (119) | is (240) |
| `to` | verage (194501) | dicip (164084) | cleanse (34824) | 什么 (6952) | 过滤 (16) | cleanse (37) | remove (64) | remove (114) |
| `make` | sure (132093) | bigger (54362) | bigger (9563) | 什么 (7410) | urine (20) | urine (9) | urine (13) | urine (9) |
| `urine` | urine (3781) | urine (1216) | urine (9) | urine (55) | urine (5) | urine (5) | is (5) | is (48) |
| `is` | colour (129222) | just (74590) | 哪一个 (2217) | 什么 (4534) | kidneys (9) | number (190) | two (382) | two (200) |

### `inv-balloon-opposite`

> Fact: The direction opposite to the one a helium balloon floats toward is "

Bridge **up** -> answer *down*. other intermediates: -, model's top word: down.
Why this group: best rank over layers at the last token: logit 7, jlens 19, jpp 7 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/inv-balloon-opposite__jlens.html) · [J++](slices/inv-balloon-opposite__jpp.html)

**Last token** `"`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | s, I, a, S, A | ness, s, ization, -color, tures | the, and, New, one, new | 236 / 1678 · 15031 / 8959 · 336 / 994 |
| 4 | a, A, A, s, S | anceled, ynec, Canceled, canceled, ങ്ങള് | someday, 南国, harbor, Ее, longtime | 174 / 2353 · 217498 / 95480 · 60596 / 16613 |
| 8 | s, M, A, S, P | anceled, Shemale, Blowjob, celed, ynec | harbor, ANCELED, utoff, 大阪市, jewelry | 152 / 3595 · 208592 / 183722 · 2603 / 13244 |
| 12 | s, R, A, R, P | Shemale, Blowjob, anceled, ness, eness | s, Oklahoma, Legend, Color, Honor | 85 / 3138 · 174236 / 158384 · 1370 / 5417 |
| 16 | P, che, S, able, E | spez, siz, niest, 水里, eness | Big, Trick, Mystic, Zach, Color | 228 / 5547 · 111399 / 52547 · 1435 / 2391 |
| 20 | S, J, eres, ug, R | s, ness, m, loud, su | s, and, sea, something, ot | 117 / 10580 · 1076 / 1701 · 64 / 181 |
| 24 | S, J, R, M, R | ness, s, loud, m, way | s, direction, wo, sea, ocean | 32 / 1075 · 633 / 3178 · 198 / 775 |
| 28 | S, M, R, g, a | ness, s, m, freaking, cean | s, Earth, m, <br, a | 749 / 10943 · 1173 / 5118 · 340 / 1060 |
| 32 | y, X, S, ing, un | whats, ness, WRONG, 是什么意思, scary | m, Earth, Yellow, World, S | 96 / 6529 · 5732 / 29013 · 1441 / 2394 |
| 36 | X, S, M, 陆, O | ness, whats, science, cean, space | Earth, m, s, wind, physics | 204 / 3380 · 1933 / 2244 · 1105 / 274 |
| 40 | X, 岸, S, R, y | Earth, Earth, downward, earth, gravity | Earth, downward, direction, gravity, earth | 169 / 259 · 625 / 99 · 108 / 14 |
| 44 | ward, wards, R, ground, X | downward, Earth, Earth, downwards, earth | downward, Earth, direction, earth, bottom | 115 / 330 · 2250 / 75 · 182 / 14 |
| 48 | H, R, X, opp, M | &quot, downward, \n, <u, earthly | Earth, direction, earth, downward, sky | 118 / 632 · 992 / 109 · 352 / 49 |
| 52 | downward, downwards, 向下, *down*, toward | downward, downwards, 向下, DOWN, *down* | downward, downwards, direction, *down*, ground | 224 / 4 · 768 / 5 · 414 / 4 |
| 56 | *down*, downward, downwards, 向下, toward | downwards, downward, 向下, *down*, *down* | *down*, downward, downwards, *down*, 向下 | 22 / 1 · 175 / 4 · 18 / 1 |
| 60 | *down*, *down*, Down, Down, downward | *down*, *down*, Down, DOWN, Down | *down*, *down*, Down, Down, downward | 17 / 1 · 20 / 1 · 31 / 1 |
| 62 | *down*, *down*, Down, Down, downward | *down*, *down*, Down, Down, downward | *down*, Down, ground, *down*, DOWN | 23 / 1 · 22 / 1 · 84 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `one` | slaught (72773) | in (80) | that (248) | 是什么意思 (2319) | direction (4590) | direction (2275) | toward (7406) | that (402) |
| `a` | ught (163470) | gotten (4200) | 别人 (3679) | people (11582) | direction (10823) | direction (38702) | person (130945) | person (26076) |
| `helium` | s (179674) | sium (204845) | helium (215103) | helium (205544) | helium (115418) | helium (112236) | balloons (88287) | balloon (28555) |
| `balloon` | 써 (15457) | bigger (412) | balloon (77373) | balloon (2711) | balloon (30338) | balloons (6765) | floated (6815) | floats (5708) |
| `floats` | heet (884) | bigger (27) | Fortal (19812) | 什么意思 (6875) | upward (7257) | upward (821) | upward (274) | is (11) |
| `toward` | ًا (170005) | toward (120742) | toward (149118) | toward (57984) | toward (120401) | direction (7013) | is (3171) | is (88) |
| `is` | eness (1795) | truly (1691) | farther (131333) | 什么意思 (83963) | downward (67494) | downward (38696) | downward (649) | *down* (120) |
| `"` | anceled (208606) | spez (111406) | ness (631) | whats (5727) | Earth (625) | &quot (996) | downward (175) | *down* (22) |

### `nhop-week-element`

> Count the items in a dozen. The element at that position on the periodic table is magnesium. Count the days in a week. The element at that position on the periodic table is

Bridge **7** -> answer *nitrogen*. other intermediates: -, model's top word: nitrogen.
Why this group: best rank over layers at the last token: logit 7, jlens 145, jpp 9 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/nhop-week-element__jlens.html) · [J++](slices/nhop-week-element__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, A, T | –and, The, It, the, For | <unk, <b, Connecticut, \xc, <data | 184 / 17749 · 10240 / 140797 · 242139 / 142054 |
| 4 | a, s, S, S, p | 农村商业银行, Zer, ness, 률은, zer | OpenGL, 王菲, 优秀共产党员, .SQL, MySQL | 254 / 14590 · 242149 / 104781 · 231080 / 212929 |
| 8 | a, s, s, m, i | .L, .The, ness, .W, .And | Wichita, 王菲, iebe, aminer, mỏ | 373 / 13277 · 241896 / 77700 · 241853 / 183533 |
| 12 | a, s, A, p, S | ation, also, ness, aurus, Junior | AIS, BIS, CIS, AIS, Eis | 430 / 13306 · 242139 / 42408 · 128060 / 46411 |
| 16 | S, S, a, A, A | because, also, just, Met, Will | AIS, CIS, AIS, Eis, BIS | 1050 / 13677 · 128469 / 20678 · 89928 / 49644 |
| 20 | T, A, A, M, T | because, John, Black, King, Charles | sulfur, Texas, Copper, 锌, 锂 | 3371 / 1563 · 17416 / 19765 · 234524 / 597 |
| 24 | A, M, A, e, w | \u, John, because, Charles, Green | mineral, chemical, minerals, chemistry, metals | 1747 / 959 · 82957 / 3963 · 228072 / 86 |
| 28 | e, ment, 素, H, s | \u, \n, John, Black, Green | the, chemical, metal, chemistry, mineral | 623 / 5312 · 3890 / 3232 · 77281 / 332 |
| 32 | ing, c, T, ment, a | \n, What, \u, Is, Y | the, mineral, Mineral, metal, St | 350 / 65925 · 150 / 6836 · 15161 / 3148 |
| 36 | atomic, 原子, assa, 第, H | Chemical, chemical, chemistry, Earth, Science | chemical, Chemical, atomic, chemistry, atom | 47 / 1326 · 1319 / 414 · 10691 / 80 |
| 40 | H, lim, assa, 第, E | Chemical, chemical, Chem, atomic, chemistry | atomic, chemical, Chemical, Atomic, atom | 192 / 4992 · 6395 / 161 · 17880 / 187 |
| 44 | 第, 什么呢, K, bes, 对应 | Chemical, chemical, atomic, chemistry, Chem | atomic, chemical, Atomic, Chemical, metal | 1093 / 21842 · 40704 / 175 · 8045 / 150 |
| 48 | m, 什么呢, 第, atomic, end | Atomic, Chemical, Chem, atomic, Chemistry | atomic, chemical, atom, 原子, Chemical | 1953 / 18476 · 140452 / 216 · 213742 / 67 |
| 52 | 第七, seventh, 原子, 第八, 七 | seventh, 第七, atomic, 原子, *nitrogen* | atom, 原子, atomic, atoms, Atom | 47 / 20 · 53246 / 5 · 148612 / 6 |
| 56 | seventh, 第七, Seven, 第七条, Seven | seventh, 第七, 第七条, Seven, seven | seventh, copper, 第七条, atomic, 第七 | 10 / 64 · 199 / 22 · 2777 / 10 |
| 60 | *nitrogen*, 氮, lithium, Nit, nit | *nitrogen*, 氮, Nit, lithium, chlorine | *nitrogen*, 氮, Nit, nit, Nit | 544 / 1 · 5642 / 1 · 9908 / 1 |
| 62 | *nitrogen*, Nit, 氮, Nit, nit | *nitrogen*, Nit, nit, 氮, nit | *nitrogen*, Nit, nit, nit, 氮 | 523 / 1 · 19300 / 1 · 10 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `at` | ting (242139) | ting (242135) | ting (214576) | ’s (256) | number (24619) | this (280) | position (437) | that (81) |
| `that` | ness (236687) | ness (240619) | though (7223) | number (1971) | number (124) | seven (93) | week (11) | position (19) |
| `position` | ally (241072) | in (242151) | in (195041) | in (3957) | numbered (169273) | number (19716) | is (3397) | on (619) |
| `on` | ­ing (180605) | shire (242144) | &nbsp (202053) | \n (16803) | 表格 (214706) | \n (67475) | periodic (72228) | the (26948) |
| `the` | -pre (238214) | though (241902) | though (1075) | just (76670) | twelve (17061) | birthdays (241955) | items (145114) | periodic (147431) |
| `periodic` | ity (84355) | ity (241230) | ity (241913) | science (822) | chemistry (19399) | numbered (8713) | element (80181) | atomic (7670) |
| `table` | 's (80503) | itself (242074) | is (133265) | ’s (143) | symbol (70759) | is (46081) | is (46) | is (591) |
| `is` | .L (241895) | because (128461) | \u (82961) | \n (149) | Chemical (6393) | Atomic (140202) | seventh (199) | *nitrogen* (19292) |


<a id="none_see"></a>
## No reader sees it

No reader has the intermediate in its top 10 at any layer.

### `nhop-compass-planet`

> Count the legs on a spider. The planet at that position from the Sun is Neptune. Count the cardinal directions on a compass. The planet at that position from the Sun is

Bridge **4** -> answer *Mars*. other intermediates: four, model's top word: Saturn.
Why this group: best rank over layers at the last token: logit 181, jlens 262, jpp 11 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/nhop-compass-planet__jlens.html) · [J++](slices/nhop-compass-planet__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, A | –and, The, the, It, For | <unk, \xc, <b, <data, Connecticut | 130 / 14669 · 2643 / 13964 · 242151 / 170187 |
| 4 | a, s, S, S, P | ness, 률은, 农村商业银行, zer, 港币 | OpenGL, 优秀共产党员, _SDK, tiful, 王菲 | 144 / 13084 · 242153 / 14466 · 214875 / 208366 |
| 8 | a, m, s, s, e | ness, .The, .But, .W, .L | 王菲, 德州, Wichita, iebe, _wp | 155 / 5199 · 242151 / 244 · 241965 / 135906 |
| 12 | a, s, s, p, e | also, ness, Sunny, anyways, ation | AIS, CIS, the, MIS, AIS | 186 / 11525 · 242149 / 149 · 18860 / 15 |
| 16 | S, a, S, b, A | also, just, whilst, amongst, Met | CIS, Jupiter, Stars, *Mars*, Meteor | 136 / 17160 · 237721 / 3424 · 64337 / 4 |
| 20 | M, able, M, T, v | King, also, God, The, because | Jupiter, Earth, Texas, celestial, 地球的 | 477 / 2517 · 20185 / 325 · 236968 / 237 |
| 24 | L, A, A, M, H | \u, though, \n, amongst, King | Earth, the, name, Jupiter, astronomical | 212 / 4335 · 28615 / 516 · 219632 / 75 |
| 28 | ment, 乎, (s, ly, f | \n, \u, &nbsp, \r, What | the, The, Jupiter, name, a | 496 / 23968 · 72 / 262 · 79245 / 48 |
| 32 | S, \n, 喜, t, S | \n, \u, 什么, 什么意思, What | the, also, Uran, Venus, St | 531 / 34068 · 31 / 302 · 23998 / 36 |
| 36 | 答, perm, 第, ree, 奥 | \n, 什么, <u, XXXX, <br | Vancouver, name, Canada, Jupiter, the | 1164 / 47295 · 523 / 262 · 14870 / 12 |
| 40 | ystem, 答, otope, A, a | \n, 什么, What, What, what | the, what, a, A, first | 3797 / 11797 · 25993 / 58 · 44269 / 550 |
| 44 | 乎, \n, obar, 什么, neither | \n, What, what, 什么, Name | the, second, th, a, name | 701 / 71526 · 40545 / 124 · 55 / 1193 |
| 48 | 什么呢, null, 喜, another, 末 | \n, \u, Jupiter, Saturn, \t | Jupiter, planet, Saturn, another, Venus | 3155 / 25499 · 4543 / 12 · 116296 / 13 |
| 52 | fourth, 第四, 第四个, 天王, cuarto | Earth, Jupiter, Venus, Neptune, fourth | Jupiter, 木星, planet, Neptune, Venus | 931 / 9458 · 15822 / 10 · 234772 / 19 |
| 56 | planet, planet, 地球, planets, Planet | Planet, planet, Jupiter, Earth, planet | planet, Planet, planet, Jupiter, planets | 51000 / 34 · 201990 / 13 · 82592 / 16 |
| 60 | Earth, Saturn, Uran, 地球, Jupiter | Saturn, Earth, Uran, Jupiter, *Mars* | Saturn, Jupiter, planet, *Mars*, Earth | 70197 / 8 · 167839 / 5 · 183290 / 4 |
| 62 | Uran, Saturn, Earth, Mercury, Jupiter | Uran, Saturn, Mercury, Jupiter, Earth | Saturn, Uran, *Mars*, Earth, Jupiter | 32453 / 6 · 228800 / 6 · 10 / 3 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `planet` | Planet (25843) | Planet (28444) | Planet (95791) | \n (101) | planet (186075) | planet (187358) | closest (237760) | at (199965) |
| `at` | ting (242150) | ting (241883) | ting (59287) | 的 (165) | 位置 (19457) | this (51697) | position (122635) | that (112344) |
| `that` | ly (239357) | ness (241892) | though (15735) | \n (777) | number (1113) | four (16) | cardinal (331) | position (451) |
| `position` | ally (241720) | whilst (242139) | in (119601) | \n (3147) | 序号 (239572) | position (54292) | from (92265) | from (122278) |
| `from` | ness (242140) | ness (242151) | nearer (230189) | 的 (336) | 地球 (217431) | \n (202258) | Jupiter (236924) | the (93422) |
| `the` | 大金 (242133) | o (136423) | though (301) | \u (240303) | spiders (77114) | eight (34088) | spider (173256) | Sun (212020) |
| `Sun` | aries (211119) | Saturn (241378) | Saturn (34205) | \n (146) | 太阳系 (47542) | Jupiter (4512) | Jupiter (63077) | is (5866) |
| `is` | ness (242151) | also (237729) | \u (28608) | \n (31) | \n (25997) | \n (4539) | Planet (202006) | Uran (228799) |

### `nhop-guitar-planet`

> Count the legs on a spider. The planet at that position from the Sun is Neptune. Count the strings on a standard guitar. The planet at that position from the Sun is

Bridge **6** -> answer *Saturn*. other intermediates: six, model's top word: Saturn.
Why this group: best rank over layers at the last token: logit 263, jlens 288, jpp 27 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/nhop-guitar-planet__jlens.html) · [J++](slices/nhop-guitar-planet__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, s, A, S | –and, The, the, It, For | <unk, \xc, <b, <data, Connecticut | 171 / 30454 · 6385 / 20729 · 242141 / 80159 |
| 4 | a, S, s, S, P | 률은, zer, ness, 农村商业银行, 港币 | OpenGL, 优秀共产党员, _SDK, tiful, 王菲 | 192 / 30219 · 242146 / 32108 · 228182 / 230990 |
| 8 | a, s, m, s, e | ness, .The, .W, .But, .L | 王菲, 德州, Wichita, iebe, _wp | 281 / 25006 · 241797 / 7242 · 241198 / 54370 |
| 12 | a, s, s, p, e | also, ness, ation, anyways, Sunny | AIS, CIS, the, meteor, IS | 623 / 28252 · 242142 / 691 · 33423 / 1654 |
| 16 | S, a, S, A, b | also, just, only, again, Met | Venus, Jupiter, CIS, Stars, Earth | 1228 / 59805 · 237703 / 812 · 83387 / 169 |
| 20 | T, M, M, able, T | also, King, God, Green, because | Jupiter, Earth, celestial, planet, Venus | 3116 / 20049 · 17215 / 206 · 190676 / 13 |
| 24 | A, A, L, M, H | \u, King, \n, God, because | Earth, the, Jupiter, Venus, name | 772 / 9507 · 26115 / 209 · 164582 / 11 |
| 28 | 乎, ment, f, A, D | \n, \u, King, &nbsp, What | the, Jupiter, Earth, Venus, a | 9097 / 16831 · 284 / 238 · 69816 / 24 |
| 32 | T, T, S, S, t | \n, 什么意思, \u, 什么, What | Uran, the, Jupiter, Venus, S | 9001 / 81696 · 50 / 386 · 54426 / 17 |
| 36 | 答, 层, perm, ree, 第 | 什么, \n, <u, XXXX, 什么意思 | Jupiter, planet, Vancouver, *Saturn*, Planet | 39108 / 39108 · 709 / 196 · 47582 / 5 |
| 40 | A, S, a, A, 末 | \n, 什么, What, What, .What | the, planet, A, C, a | 12500 / 14141 · 45228 / 26 · 63146 / 12 |
| 44 | \n, 乎, what, A, f | \n, What, 什么, what, <u | the, a, Earth, th, second | 13701 / 38719 · 124742 / 30 · 728 / 18 |
| 48 | what, 什么呢, 是什么, SCO, 什么 | \n, <u, \u, 什么, What | planet, Jupiter, *Saturn*, Planet, asteroid | 27556 / 22896 · 5064 / 6 · 135173 / 4 |
| 52 | 天王, 太阳系, 木星, planets, 第七 | *Saturn*, Jupiter, Venus, Pluto, Planet | planet, Jupiter, Planet, asteroid, 太阳系 | 161748 / 12 · 63449 / 1 · 241655 / 8 |
| 56 | planet, planet, planets, 行星, Planet | Planet, *Saturn*, Jupiter, planet, planet | planet, Planet, planet, Jupiter, planets | 6199 / 7 · 42383 / 2 · 120069 / 8 |
| 60 | *Saturn*, Jupiter, Uran, Earth, Venus | *Saturn*, Jupiter, Uran, Mars, Venus | *Saturn*, Jupiter, planet, Mars, Venus | 183161 / 1 · 189925 / 1 · 213412 / 1 |
| 62 | *Saturn*, Uran, Jupiter, Earth, 天王 | *Saturn*, Uran, Jupiter, Mercury, Mars | *Saturn*, Uran, Jupiter, Venus, Mars | 94092 / 1 · 238942 / 1 · 18 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `planet` | Planet (31808) | Planet (198123) | Planet (107656) | \n (238) | planet (185372) | planet (193418) | closest (241890) | at (192883) |
| `at` | ting (242118) | ting (242109) | ting (56798) | 的 (241) | 位置 (29755) | this (85076) | position (198706) | that (131924) |
| `that` | ly (222520) | ness (242049) | though (6750) | \n (630) | number (676) | seventh (66) | planet (34589) | position (30158) |
| `position` | ally (241581) | in (242149) | in (207790) | \n (6529) | 序号 (210061) | position (75726) | from (166763) | from (167219) |
| `from` | ness (241840) | ness (242154) | nearer (180534) | \n (1113) | 地球 (225830) | nearest (201161) | Earth (240899) | the (116565) |
| `the` | -pre (241688) | 部份 (241960) | though (224) | \u (239913) | spiders (161729) | eight (43473) | spider (144230) | Sun (206331) |
| `Sun` | aries (217931) | Sun (241395) | *Saturn* (6242) | \n (559) | planets (66015) | Jupiter (2047) | *Saturn* (55784) | is (18422) |
| `is` | ness (241795) | also (237698) | \u (26119) | \n (50) | \n (45339) | \n (5059) | Planet (42665) | *Saturn* (239123) |

### `nhop-rings-planet`

> Count the legs on a spider. The planet at that position from the Sun is Neptune. Count the Olympic rings. The planet at that position from the Sun is

Bridge **5** -> answer *Jupiter*. other intermediates: five, model's top word: Saturn.
Why this group: best rank over layers at the last token: logit 238, jlens 235, jpp 18 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/nhop-rings-planet__jlens.html) · [J++](slices/nhop-rings-planet__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | S, a, s, S, A | –and, The, the, It, For | <unk, <b, \xc, <data, Connecticut | 156 / 31279 · 3646 / 17090 · 242145 / 142858 |
| 4 | a, S, s, S, A | ness, 률은, 农村商业银行, zer, 港币 | OpenGL, 优秀共产党员, _SDK, tiful, 王菲 | 182 / 24653 · 242151 / 7463 · 229602 / 160704 |
| 8 | a, m, s, s, e | .The, ness, .W, .But, .And | 王菲, iebe, 德州, Wichita, _wp | 150 / 12226 · 241910 / 19246 · 241485 / 2695 |
| 12 | a, s, p, s, e | also, Sunny, ation, ness, anyways | AIS, CIS, the, and, IS | 182 / 17165 · 242142 / 1513 · 14115 / 61 |
| 16 | a, S, S, A, P | also, again, really, Star, just | CIS, Venus, Stars, Earth, Meteor | 329 / 9766 · 241421 / 920 · 30385 / 6 |
| 20 | T, M, T, M, t | also, King, The, God, because | *Jupiter*, Earth, planet, celestial, Venus | 1993 / 6556 · 14874 / 348 · 211840 / 1 |
| 24 | A, H, A, M, L | \n, amongst, \u, King, though | Earth, the, *Jupiter*, Venus, astronomical | 1044 / 5249 · 31600 / 354 · 196619 / 3 |
| 28 | f, ment, d, s, O | \n, \u, &nbsp, What, King | the, *Jupiter*, The, and, a | 2192 / 9673 · 184 / 348 · 127942 / 2 |
| 32 | t, O, X, T, S | \n, \u, What, \t, What | the, Uran, also, S, *Jupiter* | 1285 / 32795 · 23 / 501 · 97317 / 5 |
| 36 | 答, ree, 第, oma, assa | 什么, \n, <u, XXXX, 什么意思 | Vancouver, Canada, Planet, planet, *Jupiter* | 20792 / 20255 · 713 / 374 · 55153 / 5 |
| 40 | A, 末, a, ree, A | \n, 什么, What, What, Answer | the, A, C, a, what | 10516 / 16972 · 35049 / 49 · 74628 / 30 |
| 44 | 乎, \n, H, 加上, A | \n, What, 什么, what, Which | the, th, a, second, fourth | 3515 / 75827 · 36111 / 66 · 327 / 147 |
| 48 | 什么呢, what, SCO, gì, 是什么 | \n, What, <u, 什么, \u | planet, third, *Jupiter*, fourth, Saturn | 8380 / 25685 · 1715 / 10 · 73725 / 3 |
| 52 | 第五, 太阳系, 木星, fim, fifth | *Jupiter*, Saturn, Venus, Neptune, Earth | *Jupiter*, planet, 木星, asteroid, 太阳系 | 34471 / 14 · 70886 / 1 · 238810 / 1 |
| 56 | planet, 地球, planet, Earth, planets | *Jupiter*, Planet, planet, Saturn, Earth | planet, *Jupiter*, Planet, planet, planets | 78437 / 9 · 211466 / 1 · 134730 / 2 |
| 60 | Earth, Saturn, 地球, *Jupiter*, Uran | Saturn, Earth, *Jupiter*, Mars, Uran | Saturn, *Jupiter*, planet, Mars, Earth | 26594 / 4 · 94118 / 3 · 176176 / 2 |
| 62 | Saturn, Earth, Uran, *Jupiter*, Mars | Saturn, Uran, *Jupiter*, Earth, Mars | Saturn, Earth, Uran, *Jupiter*, Mars | 19706 / 4 · 217638 / 3 · 13 / 4 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `planet` | Planet (4826) | Planet (118052) | Planet (59333) | \n (253) | planet (173156) | planet (216796) | closest (231740) | at (148577) |
| `at` | ting (242144) | ting (242082) | ting (113258) | 的 (169) | 位置 (5203) | this (8843) | position (125020) | that (55770) |
| `that` | ly (228959) | ly (242140) | though (41471) | \n (178) | number (1047) | number (72) | position (881) | position (621) |
| `position` | ally (237840) | in (242135) | in (185600) | \n (3101) | 序号 (199974) | position (13303) | from (76703) | from (41467) |
| `from` | ness (241518) | s (242153) | nearer (177057) | 的 (1742) | 地球 (224223) | nearest (106720) | Earth (217707) | the (73774) |
| `the` | -pre (237460) | o (217772) | though (870) | 怎么 (223841) | 数 (113457) | &nbsp (211129) | spider (235280) | Sun (225747) |
| `Sun` | 's (158995) | ed (238780) | Saturn (15412) | \n (540) | 太阳系 (76122) | \n (1638) | Saturn (134229) | is (10908) |
| `is` | .The (241908) | also (241422) | \n (31364) | \n (23) | \n (35050) | \n (1713) | *Jupiter* (211476) | Saturn (217626) |


<a id="model_wrong"></a>
## Model answers wrong

The model's greedy next token is not the target's first token.

### `inv-balloon-opposite`

> Fact: The direction opposite to the one a helium balloon floats toward is "

Bridge **up** -> answer *down*. other intermediates: -, model's top word: down.
Why this group: best rank over layers at the last token: logit 7, jlens 19, jpp 7 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/inv-balloon-opposite__jlens.html) · [J++](slices/inv-balloon-opposite__jpp.html)

**Last token** `"`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | s, I, a, S, A | ness, s, ization, -color, tures | the, and, New, one, new | 236 / 1678 · 15031 / 8959 · 336 / 994 |
| 4 | a, A, A, s, S | anceled, ynec, Canceled, canceled, ങ്ങള് | someday, 南国, harbor, Ее, longtime | 174 / 2353 · 217498 / 95480 · 60596 / 16613 |
| 8 | s, M, A, S, P | anceled, Shemale, Blowjob, celed, ynec | harbor, ANCELED, utoff, 大阪市, jewelry | 152 / 3595 · 208592 / 183722 · 2603 / 13244 |
| 12 | s, R, A, R, P | Shemale, Blowjob, anceled, ness, eness | s, Oklahoma, Legend, Color, Honor | 85 / 3138 · 174236 / 158384 · 1370 / 5417 |
| 16 | P, che, S, able, E | spez, siz, niest, 水里, eness | Big, Trick, Mystic, Zach, Color | 228 / 5547 · 111399 / 52547 · 1435 / 2391 |
| 20 | S, J, eres, ug, R | s, ness, m, loud, su | s, and, sea, something, ot | 117 / 10580 · 1076 / 1701 · 64 / 181 |
| 24 | S, J, R, M, R | ness, s, loud, m, way | s, direction, wo, sea, ocean | 32 / 1075 · 633 / 3178 · 198 / 775 |
| 28 | S, M, R, g, a | ness, s, m, freaking, cean | s, Earth, m, <br, a | 749 / 10943 · 1173 / 5118 · 340 / 1060 |
| 32 | y, X, S, ing, un | whats, ness, WRONG, 是什么意思, scary | m, Earth, Yellow, World, S | 96 / 6529 · 5732 / 29013 · 1441 / 2394 |
| 36 | X, S, M, 陆, O | ness, whats, science, cean, space | Earth, m, s, wind, physics | 204 / 3380 · 1933 / 2244 · 1105 / 274 |
| 40 | X, 岸, S, R, y | Earth, Earth, downward, earth, gravity | Earth, downward, direction, gravity, earth | 169 / 259 · 625 / 99 · 108 / 14 |
| 44 | ward, wards, R, ground, X | downward, Earth, Earth, downwards, earth | downward, Earth, direction, earth, bottom | 115 / 330 · 2250 / 75 · 182 / 14 |
| 48 | H, R, X, opp, M | &quot, downward, \n, <u, earthly | Earth, direction, earth, downward, sky | 118 / 632 · 992 / 109 · 352 / 49 |
| 52 | downward, downwards, 向下, *down*, toward | downward, downwards, 向下, DOWN, *down* | downward, downwards, direction, *down*, ground | 224 / 4 · 768 / 5 · 414 / 4 |
| 56 | *down*, downward, downwards, 向下, toward | downwards, downward, 向下, *down*, *down* | *down*, downward, downwards, *down*, 向下 | 22 / 1 · 175 / 4 · 18 / 1 |
| 60 | *down*, *down*, Down, Down, downward | *down*, *down*, Down, DOWN, Down | *down*, *down*, Down, Down, downward | 17 / 1 · 20 / 1 · 31 / 1 |
| 62 | *down*, *down*, Down, Down, downward | *down*, *down*, Down, Down, downward | *down*, Down, ground, *down*, DOWN | 23 / 1 · 22 / 1 · 84 / 1 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `one` | slaught (72773) | in (80) | that (248) | 是什么意思 (2319) | direction (4590) | direction (2275) | toward (7406) | that (402) |
| `a` | ught (163470) | gotten (4200) | 别人 (3679) | people (11582) | direction (10823) | direction (38702) | person (130945) | person (26076) |
| `helium` | s (179674) | sium (204845) | helium (215103) | helium (205544) | helium (115418) | helium (112236) | balloons (88287) | balloon (28555) |
| `balloon` | 써 (15457) | bigger (412) | balloon (77373) | balloon (2711) | balloon (30338) | balloons (6765) | floated (6815) | floats (5708) |
| `floats` | heet (884) | bigger (27) | Fortal (19812) | 什么意思 (6875) | upward (7257) | upward (821) | upward (274) | is (11) |
| `toward` | ًا (170005) | toward (120742) | toward (149118) | toward (57984) | toward (120401) | direction (7013) | is (3171) | is (88) |
| `is` | eness (1795) | truly (1691) | farther (131333) | 什么意思 (83963) | downward (67494) | downward (38696) | downward (649) | *down* (120) |
| `"` | anceled (208606) | spez (111406) | ness (631) | whats (5727) | Earth (625) | &quot (996) | downward (175) | *down* (22) |

### `nhop-primary-planet`

> Count the legs on a spider. The planet at that position from the Sun is Neptune. Count the primary colors of light. The planet at that position from the Sun is

Bridge **3** -> answer *Earth*. other intermediates: three, third, model's top word: Jupiter.
Why this group: best rank over layers at the last token: logit 88, jlens 357, jpp 17 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/nhop-primary-planet__jlens.html) · [J++](slices/nhop-primary-planet__jpp.html)

**Last token** `is`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | a, S, s, S, A | –and, The, the, It, For | <unk, <b, \xc, <data, Connecticut | 89 / 5056 · 6557 / 4855 · 242149 / 88605 |
| 4 | a, S, s, S, P | ness, 률은, 农村商业银行, zer, 港币 | OpenGL, 优秀共产党员, 王菲, _SDK, tiful | 108 / 2988 · 242152 / 36266 · 212746 / 158350 |
| 8 | a, s, m, s, e | ness, .W, .The, .L, .But | 王菲, 德州, iebe, Wichita, _wp | 101 / 3738 · 242107 / 21009 · 241556 / 75489 |
| 12 | a, s, s, p, e | anyways, also, ness, Sunny, 률은 | AIS, CIS, the, and, IS | 83 / 2749 · 242137 / 7226 · 9646 / 54 |
| 16 | a, S, S, A, b | also, again, just, going, Star | CIS, Stars, Venus, Meteor, Crescent | 124 / 2179 · 241746 / 7648 · 45590 / 16 |
| 20 | T, M, T, able, t | also, King, Green, because, God | Texas, Jupiter, Alabama, *Earth*, Venus | 476 / 1612 · 31556 / 486 · 226352 / 4 |
| 24 | A, A, J, M, L | \u, \n, though, King, amongst | the, *Earth*, name, Venus, Jupiter | 119 / 408 · 36240 / 237 · 220496 / 2 |
| 28 | f, s, 乎, A, ment | \n, \u, &nbsp, \uff, \r | the, and, The, a, St | 187 / 7190 · 128 / 75 · 62265 / 36 |
| 32 | S, S, t, X, T | \n, 什么意思, 什么, \u, \t | the, also, St, a, S | 83 / 13621 · 58 / 222 · 29189 / 45 |
| 36 | 是什么, 答, perm, omba, ynam | 什么, \n, 什么意思, 是什么, <u | name, the, Vancouver, Canada, St | 3703 / 67903 · 757 / 1267 · 22140 / 533 |
| 40 | S, ha, a, A, A | 什么, \n, What, 是什么, What | the, A, a, what, B | 1017 / 40490 · 72110 / 173 · 72247 / 596 |
| 44 | \n, A, f, S, H | What, what, \n, 什么, What | the, a, th, second, an | 214 / 42685 · 22176 / 91 · 252 / 213 |
| 48 | A, H, what, Hau, 是什么 | \n, What, <u, \u, \t | another, planet, third, second, the | 721 / 66890 · 942 / 43 · 66893 / 27 |
| 52 | third, 第三条, 第三个, ثالث, Third | Third, Saturn, Jupiter, Venus, THIRD | Jupiter, planet, 太阳系, 木星, Planet | 4043 / 776 · 14315 / 18 · 232636 / 98 |
| 56 | planet, 地球, planet, *Earth*, planets | Jupiter, Saturn, Planet, planet, *Earth* | planet, Jupiter, planet, Planet, 木星 | 48127 / 4 · 201892 / 6 · 20869 / 15 |
| 60 | *Earth*, Saturn, Jupiter, Mars, Venus | Saturn, Jupiter, Mars, Mercury, *Earth* | Saturn, Jupiter, Mars, planet, Venus | 22310 / 1 · 140390 / 6 · 168644 / 11 |
| 62 | Saturn, Jupiter, Uran, *Earth*, Mars | Uran, Jupiter, Saturn, Mercury, Mars | Jupiter, Saturn, Uran, Mars, Venus | 33816 / 4 · 237407 / 8 · 11 / 7 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `planet` | Planet (9300) | Planet (129203) | Planet (88324) | \n (480) | planet (227569) | planet (189762) | closest (239264) | at (172308) |
| `at` | ting (242137) | ting (241797) | ting (20606) | 的 (515) | 位置 (90084) | this (66054) | THAT (183303) | that (137261) |
| `that` | ly (233689) | ness (242146) | though (52280) | \n (6210) | number (5515) | number (356) | position (3137) | position (12112) |
| `position` | ally (240855) | in (242079) | in (132149) | \n (10660) | 序号 (208319) | position (32082) | from (95918) | from (118194) |
| `from` | ness (240243) | ness (242151) | nearer (203688) | \n (7983) | 地球 (238931) | nearest (203908) | *Earth* (235127) | the (103943) |
| `the` | 旳 (234321) | o (235873) | though (368) | 怎么 (241961) | 数 (217993) | eight (192627) | spider (225905) | Sun (193588) |
| `Sun` | aries (183921) | 's (240505) | Saturn (13183) | \n (189) | 太阳系 (93215) | Jupiter (1146) | Jupiter (162689) | is (12979) |
| `is` | ness (242107) | also (241746) | \u (36245) | \n (58) | 什么 (72126) | \n (942) | Jupiter (201889) | Uran (237410) |

### `rhyme-door-doubled`

> Fact: Take the number whose name rhymes with the word door. Doubling it gives the number

Bridge **four** -> answer *8*. other intermediates: -, model's top word: of.
Why this group: best rank over layers at the last token: logit 14, jlens 5, jpp 26 (0 = top).
Interactive layer x position view (jlens, pinned words; open locally): [J-lens](slices/rhyme-door-doubled__jlens.html) · [J++](slices/rhyme-door-doubled__jpp.html)

**Last token** `number`: top-5 words per layer

| layer | logit lens | J-lens | J++ | B / A rank: logit lens · J-lens · J++ |
|---|---|---|---|---|
| 0 | I, of, a, T, p | 's, the, The, –and, to | the, people, that, about, one | 9880 / 231 · 1507 / 662 · 56 / 242148 |
| 4 | I, a, A, e, of | number, Number, 一数, number, called | OpenGL, number, numbers, number, (numbers | 11485 / 309 · 12976 / 239745 · 61575 / 229451 |
| 8 | a, I, M, of, er | 一数, ´s, 's, -number, .number | numbers, number, (numbers, numbers, numbering | 15241 / 337 · 50430 / 125799 · 2148 / 204493 |
| 12 | er, a, M, 1, p | number, 一数, Number, -number, .number | Number, NUMBER, Numbers, .Number, Number | 20042 / 247 · 4000 / 221175 · 1139 / 20938 |
| 16 | a, er, I, the, 's | number, Number, 一数, called, of | Number, NUMBER, Numbers, (NUM, Numer | 16719 / 1234 · 1155 / 216194 · 2087 / 44323 |
| 20 | er, that, numbers, 之, M | number, NUMBER, that, number, Number | numbers, of, that, number, numbers | 26176 / 224 · 1320 / 105 · 635 / 24692 |
| 24 | er, numbers, ing, 's, that | number, NUMBER, number, Number, Number | numbers, number, of, that, the | 38053 / 699 · 2247 / 682 · 247 / 29960 |
| 28 | (s, er, that, 's, whose | number, NUMBER, Number, which, -number | Number, number, numbers, of, Numbers | 28457 / 123 · 517 / 938 · 120 / 527 |
| 32 | that, (s, in, of, er | 什么, NUMBER, 为什么, 是什么, 是什么意思 | Number, number, Numbers, numbers, of | 9224 / 419 · 4860 / 169 · 116 / 590 |
| 36 | number, (s, 数字, numer, digits | number, NUMBER, Number, Number, what | number, Number, numbers, of, Numbers | 11682 / 250 · 715 / 50 · 55 / 982 |
| 40 | whose, number, (s, that, numer | number, Number, NUMBER, numbers, Number | number, numbers, Number, Numbers, number | 32065 / 255 · 1034 / 393 · 87 / 4337 |
| 44 | whose, (s, number, 本身, numer | number, numbers, Number, NUMBER, Numbers | number, numbers, of, that, digits | 49647 / 765 · 692 / 898 · 60 / 607 |
| 48 | whose, (s, oger, that, whose | whose, number, numbers, which, that | number, numbers, whose, Number, numer | 96638 / 1689 · 309 / 8943 · 113 / 33892 |
| 52 | whose, whose, cuyo, cuya, -number | whose, number, which, Number, that | number, whose, Number, who, numer | 81372 / 24484 · 100 / 10357 · 251 / 239310 |
| 56 | whose, whose, cuyo, represented, cuyos | whose, represented, whose, associated, name | whose, whose, of, name, who | 6611 / 11855 · 53 / 2719 · 477 / 21228 |
| 60 | whose, whose, of, _of, cuyo | whose, of, twelve, whose, eleven | of, whose, -of, whose, _of | 30 / 14574 · 15 / 7750 · 326 / 234892 |
| 62 | of, whose, that, whose, -of | of, whose, that, represented, -of | whose, of, that, whose, represented | 14 / 5202 · 6 / 13013 · 37 / 120 |

**J-lens, last 8 tokens x layers**: top word (bridge rank)

| token | L8 | L16 | L24 | L32 | L40 | L48 | L56 | L62 |
|---|---|---|---|---|---|---|---|---|
| `door` | er (145830) | er (22336) | er (8742) | er (19886) | er (6341) | er (157) | Door (370) | and (97) |
| `.` | really (19489) | really (11737) | though (4410) | 什么意思 (26131) | number (601) | number (35) | Multiply (13309) | Add (6101) |
| `Dou` | 我 (200684) | OU (32582) | OU (16920) | yo (10635) | dou (1820) | doubled (131) | Dou (2107) | bling (8214) |
| `bling` | 叁 (134288) | –and (1441) | —and (1143) | DOUBLE (6384) | doubling (568) | doubled (85) | this (871) | it (109) |
| `it` | ting (14364) | just (291) | just (470) | maybe (1734) | number (120) | would (19) | gives (159) | gives (57) |
| `gives` | colour (26337) | nice (834) | nearer (865) | 什么 (36300) | maths (604) | another (21) | you (23) | you (8) |
| `the` | ´s (70531) | own (406) | nearer (1019) | what (370) | number (34) | number (30) | number (1169) | number (380) |
| `number` | 一数 (50428) | number (1154) | number (2250) | 什么 (4856) | number (1032) | whose (310) | whose (53) | of (7) |

