# C1 on tasks_v2 / muse30_natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 91 [85-96] (n=136) | 97 [92-100] (n=142) | 9 [4-15] (n=136) | 11 [5-18] (n=142) |
| L36-42 | paper10_rot | 98 [95-100] (n=136) | 94 [89-98] (n=142) | 96 [92-99] (n=136) | 97 [93-100] (n=142) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 91 [85-96] (n=136) | 97 [92-100] (n=142) | 9 [4-15] (n=136) | 11 [5-18] (n=142) |
| L36-42 | paper10_rot | 98 [95-100] (n=136) | 94 [89-98] (n=142) | 96 [92-99] (n=136) | 97 [93-100] (n=142) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.62, M->P 1.69, P->M 2.16, M->M 2.75. Loss (points) by quartile of that margin (cuts 1.25, 2.06, 2.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 19 (n=52) | 2 (n=50) | 0 (n=25) | 0 (n=9) |
| M->P | 7 (n=60) | 0 (n=23) | 0 (n=37) | 0 (n=22) |
| P->M | 95 (n=19) | 92 (n=39) | 89 (n=54) | 92 (n=24) |
| M->M | 94 (n=16) | 100 (n=20) | 97 (n=36) | 81 (n=70) |
| prompt-final, pooled | 12 (n=112) | 1 (n=73) | 0 (n=62) | 0 (n=31) |
| memory-final, pooled | 94 (n=35) | 95 (n=59) | 92 (n=90) | 84 (n=94) |

Memory-final minus prompt-final, items pooled per group: raw 85; reweighted to the prompt-final margins 87, to the memory-final margins 88; matched within 0.25-logit margin bins 89 [85-92] (272 of 278 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 8, M->P 3, P->M 91, M->M 89; memory-final minus prompt-final 85 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit fbf95f2.
