# C1 on tasks_v2 / muse30_natural_v1_chat_ko_v1 WITHOUT guessable items (robustness split) (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 90 [83-96] (n=109) | 96 [90-100] (n=106) | 8 [3-14] (n=120) | 8 [3-15] (n=126) |
| L36-42 | paper10_rot | 97 [94-100] (n=109) | 93 [89-98] (n=106) | 96 [92-99] (n=120) | 97 [92-100] (n=126) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 90 [83-96] (n=109) | 96 [90-100] (n=106) | 8 [3-14] (n=120) | 8 [3-15] (n=126) |
| L36-42 | paper10_rot | 97 [94-100] (n=109) | 93 [89-98] (n=106) | 96 [92-99] (n=120) | 97 [92-100] (n=126) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.50, M->P 1.72, P->M 2.16, M->M 2.72. Loss (points) by quartile of that margin (cuts 1.25, 2.06, 2.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 20 (n=45) | 2 (n=40) | 0 (n=16) | 0 (n=8) |
| M->P | 9 (n=45) | 0 (n=19) | 0 (n=26) | 0 (n=16) |
| P->M | 100 (n=14) | 92 (n=36) | 90 (n=48) | 95 (n=22) |
| M->M | 93 (n=15) | 100 (n=20) | 97 (n=33) | 86 (n=58) |
| prompt-final, pooled | 14 (n=90) | 2 (n=59) | 0 (n=42) | 0 (n=24) |
| memory-final, pooled | 97 (n=29) | 95 (n=56) | 93 (n=81) | 89 (n=80) |

Memory-final minus prompt-final, items pooled per group: raw 86; reweighted to the prompt-final margins 88, to the memory-final margins 90; matched within 0.25-logit margin bins 90 [86-94] (230 of 246 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 9, M->P 4, P->M 92, M->M 92; memory-final minus prompt-final 86 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 95f5897.
