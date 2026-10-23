# C1 on tasks_v2 / muse30_natural_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 99 [98-100] (n=143) | 98 [95-100] (n=154) | 41 [32-51] (n=143) | 51 [41-61] (n=154) |
| L36-42 | paper10_rot | 97 [95-99] (n=143) | 92 [87-97] (n=154) | 96 [92-99] (n=143) | 97 [93-99] (n=154) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 99 [98-100] (n=143) | 98 [95-100] (n=154) | 41 [32-51] (n=143) | 51 [41-61] (n=154) |
| L36-42 | paper10_rot | 97 [95-99] (n=143) | 92 [87-97] (n=154) | 96 [92-99] (n=143) | 97 [93-99] (n=154) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.56, M->P 1.69, P->M 2.12, M->M 2.78. Loss (points) by quartile of that margin (cuts 1.19, 2.06, 2.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | -2 (n=51) | 0 (n=58) | 0 (n=25) | 0 (n=9) |
| M->P | 3 (n=62) | 3 (n=30) | 0 (n=39) | 0 (n=23) |
| P->M | 90 (n=20) | 65 (n=43) | 51 (n=55) | 40 (n=25) |
| M->M | 88 (n=17) | 52 (n=23) | 68 (n=37) | 30 (n=77) |
| prompt-final, pooled | 1 (n=113) | 1 (n=88) | 0 (n=64) | 0 (n=32) |
| memory-final, pooled | 89 (n=37) | 61 (n=66) | 58 (n=92) | 32 (n=102) |

Memory-final minus prompt-final, items pooled per group: raw 53; reweighted to the prompt-final margins 67, to the memory-final margins 53; matched within 0.25-logit margin bins 53 [47-59] (287 of 297 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P -1, M->P 2, P->M 59, M->M 49; memory-final minus prompt-final 53 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 6ba91f2.
