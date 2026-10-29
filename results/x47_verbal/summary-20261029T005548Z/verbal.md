# 47.0: is the pointer verbalizable? (descriptive)

J++ lens at the layer fixed in advance; the write h + 2 (mu_k - mu_j) at the bridge word of the routes test's original prompts (x8_write's items); null: 200 random directions of the same norm (seed 4701); statistics are medians over cases against the null's medians (scripts/x47_verbal.py). UNVERIFIED.

| | Nemotron 3.5 Lightning (L14) |
|---|---|
| items / cases (write to each other locker) | 100 / 200 |
| x8's lookup on these writes at s = 2: to the written locker | 0.50 |
| (a) best ordinal-token rank, h alone (median) | 196 |
| (a) best ordinal-token rank, h + write (median) | 220 (null 5th pct 49) |
| (a) best digit rank, h + write (median) | 1343 (null 5th pct 664) |
| (a) the written locker's digit, rank (median) | 4982 (null 5th pct 2714) |
| (a) cases with the ordinal rank beyond their own null | 0.00 [0.00, 0.00] |
| (a) positive control: new item's name rank, h + identity | 19 (null 5th pct 4844) beyond |
| (b) share reconstructed, k = 25, every token: writes / U± / identity / random | 0.031 / 0.045 / 0.133 / 0.031 |
| (b) pointer / random, k = 25 (every token; letters) | 1.44x; 1.46x |
| (b) pointer / random, k = 100 (every token; letters) | 1.41x; 1.42x |
| (b) identity / random, k = 25 (every token) | 4.30x |
| (c) KL(h || h + write) (median) | 0.034 (null 95th pct 0.429) |
| (c) KL(h || h + identity, same norm) (median) | 2.455 (null 95th pct 0.429) beyond |
| (c) cases with KL beyond their own null | 0.00 [0.00, 0.00] |
| reading | not verbalizable |

Over the models: **not verbalizable**.

Sanity swap (the other reading of Neel's question, augmenting the lens with the pointer): with J++ and U removed together the lookup still switches in 0.45 / 0.53 / 0.74 of the sanity-swap scenes (Qwen3.5-9B / Qwen3.6-27B / Muse Glimmer 30B; a random part of the same size: 0.88 / 0.94 / 1.05; figures/story/data.csv, fig10, runs qwen35_9b_x6_routes_bothoff, x6_routes_bothoff_27b, muse30b_x6_routes).

- Nemotron 3.5 Lightning: not verbalizable: ordinal median rank 220 (null 5th pct 49); digits 1343 (null 664); reconstruction at k = 25 1.44x the null; KL median 0.0344 (null 95th pct 0.429).

Atoms the OMP picks first (every token, k = 25; the 5 largest coefficients):
- Nemotron 3.5 Lightning, U0+: '.', ' infine', '장으로', ' \u200b', ' Noord'
- Nemotron 3.5 Lightning, U0-: ' وال', '.W', 'ovar', '\xa0s', '乗'
- Nemotron 3.5 Lightning, U1+: '/S', ' hermana', ' \u200b', ' המפ', 'lund'
- Nemotron 3.5 Lightning, U1-: '.', ' ألك', 'Album', ' mais', ' infin'
- Nemotron 3.5 Lightning, U2+: 'Tick', '/S', 'lund', 'imon', ' fy'
- Nemotron 3.5 Lightning, U2-: '´s', ' �', '，', 'дро', ' GSH'
- Nemotron 3.5 Lightning, U3+: ' הז', 'aga', ',F', 'RF', ' longitudinal'
- Nemotron 3.5 Lightning, U3-: 'dera', '.\n', '，', ' وص', 'Chan'
- Nemotron 3.5 Lightning, mu1-mu0: '/S', ' التابعة', 'lund', ' \u200b', '.accept'
- Nemotron 3.5 Lightning, mu2-mu0: ' 청', ' \u200b', ' التابعة', ' Munster', ' Kec'
- Nemotron 3.5 Lightning, mu0-mu1: ' ألك', ' �', '.\n\n', '，《', ' mais'
- Nemotron 3.5 Lightning, mu2-mu1: '….', ' Hé', 'osen', '，', '�'
- Nemotron 3.5 Lightning, mu0-mu2: '.\n\n', ' אל', ' mais', ' initializing', ' Nixon'
- Nemotron 3.5 Lightning, mu1-mu2: ' accuse', '乗', ' اضطراب', ',B', 'Tick'

Draft sentence for the README's monitoring bullet (for Dan to edit): Read through the J++ lens, a pointer write that sends the lookup to the written locker in 0.50 of cases leaves the best ordinal word at rank 220 (median), the lens's own directions rebuild it no better than random ones (1.4x the random share at 25 directions), and the lens's readout moves no more than under a random vector of the same size: a lens monitor would not see the pointer.
