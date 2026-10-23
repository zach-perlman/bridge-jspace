# C1 on tasks_v2 / qwen35_9b_natplus_v1_chat_ko_cand2_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [89-95] (n=302) | 91 [87-93] (n=295) | 50 [43-57] (n=302) | 51 [44-60] (n=295) |
| L12-16 | paper10_rot | 91 [88-94] (n=302) | 92 [88-94] (n=295) | 96 [94-98] (n=302) | 98 [95-99] (n=295) |
| L12-16 | unembed10 | 94 [91-96] (n=302) | 95 [93-98] (n=295) | 99 [98-100] (n=302) | 100 [99-100] (n=295) |
| L12-16 | unembed10_rot | 95 [92-97] (n=302) | 96 [94-98] (n=295) | 97 [94-99] (n=302) | 100 [99-100] (n=295) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [89-95] (n=302) | 91 [87-93] (n=295) | 50 [43-57] (n=302) | 51 [44-60] (n=295) |
| L12-16 | paper10_rot | 91 [88-94] (n=302) | 92 [88-94] (n=295) | 96 [94-98] (n=302) | 98 [95-99] (n=295) |
| L12-16 | unembed10 | 94 [91-96] (n=302) | 95 [93-98] (n=295) | 99 [98-100] (n=302) | 100 [99-100] (n=295) |
| L12-16 | unembed10_rot | 95 [92-97] (n=302) | 96 [94-98] (n=295) | 97 [94-99] (n=302) | 100 [99-100] (n=295) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |
| L12-16 | unembed10 | - | - | - | - |
| L12-16 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.88, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 16 (n=128) | 1 (n=75) | 0 (n=51) | 4 (n=48) |
| M->P | 24 (n=90) | 4 (n=80) | 3 (n=73) | 2 (n=52) |
| P->M | 66 (n=68) | 47 (n=89) | 40 (n=85) | 47 (n=60) |
| M->M | 67 (n=27) | 62 (n=52) | 47 (n=78) | 41 (n=138) |
| prompt-final, pooled | 20 (n=218) | 3 (n=155) | 2 (n=124) | 3 (n=100) |
| memory-final, pooled | 66 (n=95) | 52 (n=141) | 44 (n=163) | 43 (n=198) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 45, to the memory-final margins 44; matched within 0.25-logit margin bins 43 [39-48] (590 of 597 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.88, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 14 (n=128) | 0 (n=75) | 0 (n=51) | 0 (n=48) |
| M->P | 16 (n=90) | 0 (n=80) | 0 (n=73) | 0 (n=52) |
| P->M | 1 (n=68) | 0 (n=89) | 0 (n=85) | 0 (n=60) |
| M->M | 0 (n=27) | 0 (n=52) | 1 (n=78) | 0 (n=138) |
| prompt-final, pooled | 15 (n=218) | 0 (n=155) | 0 (n=124) | 0 (n=100) |
| memory-final, pooled | 1 (n=95) | 0 (n=141) | 1 (n=163) | 0 (n=198) |

Memory-final minus prompt-final, items pooled per group: raw -5; reweighted to the prompt-final margins -5, to the memory-final margins -2; matched within 0.25-logit margin bins -2 [-3--1] (590 of 597 memory-final items have a same-bin partner) points.

Rule at L12-16: losses P->P 8, M->P 9, P->M 49, M->M 49; memory-final minus prompt-final 40 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit a6db0d6.
