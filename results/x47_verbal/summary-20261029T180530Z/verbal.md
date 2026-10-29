# 47.0: is the pointer verbalizable? (descriptive)

J++ lens at the layer fixed in advance; the write h + 2 (mu_k - mu_j) at the bridge word of the routes test's original prompts (x8_write's items); null: 200 random directions of the same norm (seed 4701); statistics are medians over cases against the null's medians (scripts/x47_verbal.py). UNVERIFIED.

| | Qwen3.5-122B (L33) |
|---|---|
| items / cases (write to each other locker) | 100 / 200 |
| x8's lookup on these writes at s = 2: to the written locker | 0.48 |
| (a) best ordinal-token rank, h alone (median) | 966 |
| (a) best ordinal-token rank, h + write (median) | 993 (null 5th pct 523) |
| (a) best digit rank, h + write (median) | 34736 (null 5th pct 20180) |
| (a) the written locker's digit, rank (median) | 56322 (null 5th pct 33474) |
| (a) cases with the ordinal rank beyond their own null | 0.00 [0.00, 0.00] |
| (a) positive control: new item's name rank, h + identity | 2 (null 5th pct 1137) beyond |
| (b) share reconstructed, k = 25, every token: writes / U± / identity / random | 0.019 / 0.029 / 0.148 / 0.025 |
| (b) pointer / random, k = 25 (every token; letters) | 1.14x; 1.12x |
| (b) pointer / random, k = 100 (every token; letters) | 1.13x; 1.12x |
| (b) identity / random, k = 25 (every token) | 5.82x |
| (c) KL(h || h + write) (median) | 0.022 (null 95th pct 0.053) |
| (c) KL(h || h + identity, same norm) (median) | 4.586 (null 95th pct 0.053) beyond |
| (c) cases with KL beyond their own null | 0.02 [0.00, 0.06] |
| reading | not verbalizable |

Over the models: **not verbalizable**.

Sanity swap (the other reading of Neel's question, augmenting the lens with the pointer): with J++ and U removed together the lookup still switches in 0.45 / 0.53 / 0.74 / 0.50 of the sanity-swap scenes (Qwen3.5-9B / Qwen3.6-27B / Muse Glimmer 30B / Qwen3.5-122B; a random part of the same size: 0.88 / 0.94 / 1.05 / 0.85; figures/story/data.csv, fig10, runs qwen35_9b_x6_routes_bothoff, x6_routes_bothoff_27b, muse30b_x6_routes, qwen35_122b_x6_routes_bothoff_g75).

- Qwen3.5-122B: not verbalizable: ordinal median rank 993 (null 5th pct 523); digits 34736 (null 20180); reconstruction at k = 25 1.14x the null; KL median 0.0217 (null 95th pct 0.0534).

Atoms the OMP picks first (every token, k = 25; the 5 largest coefficients):
- Qwen3.5-122B, U0+: '/graphql', ' ;;^', '小鸭', ' squirrel', '/slick'
- Qwen3.5-122B, U0-: '\r\n\r\n\r\n', '\x0f', ' Tina', 'emar', '.*'
- Qwen3.5-122B, U1+: '�', '卉', 'БА', '並沒有', ' Tan'
- Qwen3.5-122B, U1-: ' ;;^', ' \n\n\n\n', '_rhs', '柳', '。,'
- Qwen3.5-122B, U2+: '\n\n\n\n\n\n', '或', '及', '지요', 'isesti'
- Qwen3.5-122B, U2-: '百', '.Tick', '\\Mail', '��', ' BM'
- Qwen3.5-122B, U3+: 'กาญ', ' ;;^', ' Afinal', '干燥机', '�'
- Qwen3.5-122B, U3-: '(theta', '晓彤', '及', ' DefaultValue', ' serde'
- Qwen3.5-122B, mu1-mu0: '.|', '\x1c', '。', '_rhs', '\r\n    \r\n'
- Qwen3.5-122B, mu2-mu0: '\r\n\r\n\r\n', '.|', '或', '。', 'ViewInit'
- Qwen3.5-122B, mu0-mu1: '大衣', '/Dk', '/graphql', ' nitrogen', '�'
- Qwen3.5-122B, mu2-mu1: '\r\n\r\n\r\n', '等', '或', '╝', '\xa0'
- Qwen3.5-122B, mu0-mu2: '/graphql', ' squirrel', '杏花', '/Dk', '大衣'
- Qwen3.5-122B, mu1-mu2: '\\Mail', '迎春', ' сме', '的动物', ' ;;^'

Draft sentence for the README's monitoring bullet (for Dan to edit): Read through the J++ lens, a pointer write that sends the lookup to the written locker in 0.48 of cases leaves the best ordinal word at rank 993 (median), the lens's own directions rebuild it no better than random ones (1.1x the random share at 25 directions), and the lens's readout moves no more than under a random vector of the same size: a lens monitor would not see the pointer.

Qwen3.5-122B: adapted design: lookup-only gate; the recall (0.797) is not part of this test.
