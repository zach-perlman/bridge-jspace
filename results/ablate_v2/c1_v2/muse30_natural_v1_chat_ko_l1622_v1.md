# C1 on tasks_v2 / muse30_natural_v1_chat_ko_l1622_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L16-22 | paper10 | 91 [86-96] (n=136) | 89 [82-95] (n=142) | 96 [92-99] (n=136) | 95 [91-98] (n=142) |
| L16-22 | paper10_rot | 85 [77-91] (n=136) | 79 [72-86] (n=142) | 98 [95-100] (n=136) | 96 [92-99] (n=142) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L16-22 | paper10 | 91 [86-96] (n=136) | 89 [82-95] (n=142) | 96 [92-99] (n=136) | 95 [91-98] (n=142) |
| L16-22 | paper10_rot | 85 [77-91] (n=136) | 79 [72-86] (n=142) | 98 [95-100] (n=136) | 96 [92-99] (n=142) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L16-22 | paper10 | - | - | - | - |
| L16-22 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L16-22 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.62, M->P 1.69, P->M 2.16, M->M 2.75. Loss (points) by quartile of that margin (cuts 1.25, 2.06, 2.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 19 (n=52) | 0 (n=50) | 4 (n=25) | 0 (n=9) |
| M->P | 27 (n=60) | 0 (n=23) | 0 (n=37) | 0 (n=22) |
| P->M | 11 (n=19) | 3 (n=39) | 2 (n=54) | 4 (n=24) |
| M->M | 31 (n=16) | 5 (n=20) | 0 (n=36) | 1 (n=70) |
| prompt-final, pooled | 23 (n=112) | 0 (n=73) | 2 (n=62) | 0 (n=31) |
| memory-final, pooled | 20 (n=35) | 3 (n=59) | 1 (n=90) | 2 (n=94) |

Memory-final minus prompt-final, items pooled per group: raw -5; reweighted to the prompt-final margins -0, to the memory-final margins 1; matched within 0.25-logit margin bins 1 [-2-4] (272 of 278 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L16-22: losses P->P 8, M->P 11, P->M 4, M->M 5; memory-final minus prompt-final -5 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 23daf0c.
