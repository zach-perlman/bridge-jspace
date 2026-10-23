# C1 on tasks_v2 / qwen35_9b_natplus_v1_chat_ko_cand2_L24_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L24-28 | paper10 | 80 [75-84] (n=302) | 72 [67-78] (n=295) | 37 [29-44] (n=302) | 35 [27-43] (n=295) |
| L24-28 | paper10_rot | 97 [96-99] (n=302) | 96 [94-98] (n=295) | 97 [95-99] (n=302) | 98 [96-99] (n=295) |
| L24-28 | unembed10 | 89 [86-92] (n=302) | 87 [83-91] (n=295) | 68 [62-74] (n=302) | 85 [79-90] (n=295) |
| L24-28 | unembed10_rot | 98 [96-99] (n=302) | 97 [95-99] (n=295) | 98 [96-99] (n=302) | 99 [97-100] (n=295) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L24-28 | paper10 | 80 [75-84] (n=302) | 72 [67-78] (n=295) | 37 [29-44] (n=302) | 35 [27-43] (n=295) |
| L24-28 | paper10_rot | 97 [96-99] (n=302) | 96 [94-98] (n=295) | 97 [95-99] (n=302) | 98 [96-99] (n=295) |
| L24-28 | unembed10 | 89 [86-92] (n=302) | 87 [83-91] (n=295) | 68 [62-74] (n=302) | 85 [79-90] (n=295) |
| L24-28 | unembed10_rot | 98 [96-99] (n=302) | 97 [95-99] (n=295) | 98 [96-99] (n=302) | 99 [97-100] (n=295) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L24-28 | paper10 | - | - | - | - |
| L24-28 | paper10_rot | - | - | - | - |
| L24-28 | unembed10 | - | - | - | - |
| L24-28 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L24-28 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.88, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 33 (n=128) | 20 (n=75) | 6 (n=51) | 0 (n=48) |
| M->P | 49 (n=90) | 30 (n=80) | 16 (n=73) | 4 (n=52) |
| P->M | 79 (n=68) | 62 (n=89) | 55 (n=85) | 57 (n=60) |
| M->M | 70 (n=27) | 79 (n=52) | 74 (n=78) | 54 (n=138) |
| prompt-final, pooled | 39 (n=218) | 25 (n=155) | 12 (n=124) | 2 (n=100) |
| memory-final, pooled | 77 (n=95) | 68 (n=141) | 64 (n=163) | 55 (n=198) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 44, to the memory-final margins 48; matched within 0.25-logit margin bins 48 [43-53] (590 of 597 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L24-28 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.88, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 18 (n=128) | 11 (n=75) | 2 (n=51) | 0 (n=48) |
| M->P | 31 (n=90) | 8 (n=80) | 5 (n=73) | 0 (n=52) |
| P->M | 50 (n=68) | 43 (n=89) | 20 (n=85) | 10 (n=60) |
| M->M | 63 (n=27) | 29 (n=52) | 13 (n=78) | 1 (n=138) |
| prompt-final, pooled | 23 (n=218) | 9 (n=155) | 4 (n=124) | 0 (n=100) |
| memory-final, pooled | 54 (n=95) | 38 (n=141) | 17 (n=163) | 4 (n=198) |

Memory-final minus prompt-final, items pooled per group: raw 12; reweighted to the prompt-final margins 22, to the memory-final margins 16; matched within 0.25-logit margin bins 16 [12-20] (590 of 597 memory-final items have a same-bin partner) points.

Rule at L24-28: losses P->P 20, M->P 28, P->M 63, M->M 65; memory-final minus prompt-final 40 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 9e2913b.
