# 47.0: is the pointer verbalizable? (descriptive)

J++ lens at the layer fixed in advance; the write h + 2 (mu_k - mu_j) at the bridge word of the routes test's original prompts (x8_write's items); null: 200 random directions of the same norm (seed 4701); statistics are medians over cases against the null's medians (scripts/x47_verbal.py). UNVERIFIED.

| | Qwen3.5-9B (L12) | Qwen3.6-27B (L32) | Muse Glimmer 30B (L26) |
|---|---|---|---|
| items / cases (write to each other locker) | 100 / 200 | 100 / 200 | 100 / 200 |
| x8's lookup on these writes at s = 2: to the written locker | 0.42 | 0.24 | 0.56 |
| (a) best ordinal-token rank, h alone (median) | 26 | 31 | 84 |
| (a) best ordinal-token rank, h + write (median) | 27 (null 5th pct 20) | 30 (null 5th pct 22) | 94 (null 5th pct 58) |
| (a) best digit rank, h + write (median) | 5647 (null 5th pct 1961) | 592 (null 5th pct 148) | 13611 (null 5th pct 8193) |
| (a) the written locker's digit, rank (median) | 14812 (null 5th pct 6057) | 2334 (null 5th pct 698) | 44148 (null 5th pct 30094) |
| (a) cases with the ordinal rank beyond their own null | 0.03 [0.01, 0.06] | 0.13 [0.08, 0.19] | 0.18 [0.14, 0.24] |
| (a) positive control: new item's name rank, h + identity | 50 (null 5th pct 2220) beyond | 14 (null 5th pct 5014) beyond | 25 (null 5th pct 3636) beyond |
| (b) share reconstructed, k = 25, every token: writes / U± / identity / random | 0.043 / 0.059 / 0.225 / 0.051 | 0.034 / 0.038 / 0.210 / 0.041 | 0.008 / 0.009 / 0.062 / 0.007 |
| (b) pointer / random, k = 25 (every token; letters) | 1.16x; 1.15x | 0.94x; 0.93x | 1.22x; 1.21x |
| (b) pointer / random, k = 100 (every token; letters) | 1.12x; 1.12x | 0.94x; 0.93x | 1.22x; 1.20x |
| (b) identity / random, k = 25 (every token) | 4.42x | 5.16x | 8.62x |
| (c) KL(h || h + write) (median) | 0.139 (null 95th pct 0.254) | 0.066 (null 95th pct 0.197) | 0.069 (null 95th pct 0.070) |
| (c) KL(h || h + identity, same norm) (median) | 0.160 (null 95th pct 0.254) | 0.349 (null 95th pct 0.197) beyond | 3.746 (null 95th pct 0.070) beyond |
| (c) cases with KL beyond their own null | 0.15 [0.09, 0.23] | 0.01 [0.00, 0.05] | 0.28 [0.19, 0.39] |
| reading | not verbalizable | not verbalizable | not verbalizable |

Over the models: **not verbalizable**.

Sanity swap (the other reading of Neel's question, augmenting the lens with the pointer): with J++ and U removed together the lookup still switches in 0.45 / 0.53 / 0.74 of the sanity-swap scenes (Qwen3.5-9B / Qwen3.6-27B / Muse Glimmer 30B; a random part of the same size: 0.88 / 0.94 / 1.05; figures/story/data.csv, fig10, runs qwen35_9b_x6_routes_bothoff, x6_routes_bothoff_27b, muse30b_x6_routes).

- Qwen3.5-9B: not verbalizable: ordinal median rank 27 (null 5th pct 20); digits 5647 (null 1961); reconstruction at k = 25 1.16x the null; KL median 0.139 (null 95th pct 0.254).
- Qwen3.6-27B: not verbalizable: ordinal median rank 30 (null 5th pct 22); digits 592 (null 148); reconstruction at k = 25 0.94x the null; KL median 0.0657 (null 95th pct 0.197).
- Muse Glimmer 30B: not verbalizable: ordinal median rank 94 (null 5th pct 58); digits 13611 (null 8193); reconstruction at k = 25 1.22x the null; KL median 0.0692 (null 95th pct 0.0698).

Atoms the OMP picks first (every token, k = 25; the 5 largest coefficients):
- Qwen3.5-9B, U0+: '？', '栩', ' Và', "'", '/C'
- Qwen3.5-9B, U0-: '4', ' �', '\x0c\n', '].', '越快'
- Qwen3.5-9B, U1+: '下载地址', ' Z', '\n', ' calci', ' ră'
- Qwen3.5-9B, U1-: '-)', '  \n\n', '这两个', '〜', 'ld'
- Qwen3.5-9B, U2+: ' s', '#####', 'LO', '△', ' �'
- Qwen3.5-9B, U2-: '"""', ' ma', ' Car', ' .*', 'apie'
- Qwen3.5-9B, U3+: '\n\n\n\n', ' Charl', ' Canon', '.C', 'xxxx'
- Qwen3.5-9B, U3-: '�', ' tq', ' （', ' Mae', "'];"
- Qwen3.5-9B, mu1-mu0: '\x0c\n', '〜', 'MM', ' ba', '();)'
- Qwen3.5-9B, mu2-mu0: ' Jon', ' ba', ');', '  \n\n', '显'
- Qwen3.5-9B, mu0-mu1: 'D', '宇宙', ' Be', ' снова', ' ani'
- Qwen3.5-9B, mu2-mu1: '.', ' Leh', '背景', '疲劳', 'Thus'
- Qwen3.5-9B, mu0-mu2: ' Be', '宇宙', ' cip', "?'", 'ws'
- Qwen3.5-9B, mu1-mu2: "'", ' Be', ' ies', '和', ' ../'
- Qwen3.6-27B, U0+: '打', '这三个', ' Sel', ' unt', ' colorful'
- Qwen3.6-27B, U0-: "'", '2', 'acct', '本身的', ' Initialized'
- Qwen3.6-27B, U1+: ' de', ' 나눠', '建', 'ٰ', '热力'
- Qwen3.6-27B, U1-: ' Z', ' triana', ',proto', '                                  ', ' sic'
- Qwen3.6-27B, U2+: ' beaten', ' Kn', ' CB', '**', ' Moose'
- Qwen3.6-27B, U2-: '△', ']];', ' Latino', '/H', ' grapes'
- Qwen3.6-27B, U3+: '�', 'In', '四年', ' BIG', ' Fiona'
- Qwen3.6-27B, U3-: '*C', '~', '—all', ' Operators', ' layak'
- Qwen3.6-27B, mu1-mu0: '建', ' br', ' paras', ' 나눠', ' de'
- Qwen3.6-27B, mu2-mu0: ' tr', ' par', '�', '%.', '被称为'
- Qwen3.6-27B, mu0-mu1: ' San', '*“.', ' Mutual', ' прове', ' lesqu'
- Qwen3.6-27B, mu2-mu1: '这三个', ' frequent', ' Y', '顺序', '◎'
- Qwen3.6-27B, mu0-mu2: ' x', ' Mutual', '*:', ' прове', ' Obs'
- Qwen3.6-27B, mu1-mu2: "'", 'adox', ' Bro', ' ↑', ' Tough'
- Muse Glimmer 30B, U0+: '』の', '\xa0V', '/Gallon', 'roleum', ' Astrophysics'
- Muse Glimmer 30B, U0-: ' Ending', ' etc', ' Osaka', ' ebenfalls', ' Alabama'
- Muse Glimmer 30B, U1+: ' Toxic', '(?:', ' App', ' Fly', ' Afghanistan'
- Muse Glimmer 30B, U1-: 'idenav', ' волн', '==============', ' segni', ' Parma'
- Muse Glimmer 30B, U2+: '’Unione', ' Kush', ']),\n', '\u200cتوانند', ' Provence'
- Muse Glimmer 30B, U2-: ' BPM', ' Maple', ' obese', ' Walk', ' Crab'
- Muse Glimmer 30B, U3+: ' Frog', 'RG', ' Gér', ' 辽宁', '\u2028'
- Muse Glimmer 30B, U3-: ' Theta', ' SSD', 'anel', ' Sha', ' Option'
- Muse Glimmer 30B, mu1-mu0: 'incinnati', ' ramai', 'idenav', ' градострои', ' ricev'
- Muse Glimmer 30B, mu2-mu0: ' Osaka', ' ebenfalls', 'idenav', ' градострои', ' ricev'
- Muse Glimmer 30B, mu0-mu1: ' Little', ' FIRST', '(?:', '\xa0V', ' Military'
- Muse Glimmer 30B, mu2-mu1: ' Plen', ' Nvidia', ' Alabama', 'Reasons', '，南'
- Muse Glimmer 30B, mu0-mu2: '(?:', '\xa0V', ' Tit', ' Little', ' Rabbit'
- Muse Glimmer 30B, mu1-mu2: ' Beet', ' \ufeff', ' Bunny', ' Fitch', ' ruins'

Draft sentence for the README's monitoring bullet (for Dan to edit): Read through the J++ lens, a pointer write that sends the lookup to the written locker in 0.42 / 0.24 / 0.56 of cases leaves the best ordinal word at rank 27 / 30 / 94 (median), the lens's own directions rebuild it no better than random ones (1.2x / 0.9x / 1.2x the random share at 25 directions), and the lens's readout moves no more than under a random vector of the same size: a lens monitor would not see the pointer.
