# C1 on tasks_v2 / natural_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 99 [97-100] (n=231) | 89 [85-93] (n=263) | 44 [36-53] (n=231) | 48 [39-57] (n=263) |
| L32-40 | paper10_rot | 97 [94-98] (n=231) | 96 [93-98] (n=263) | 96 [92-99] (n=231) | 99 [98-100] (n=263) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 99 [97-100] (n=231) | 89 [85-93] (n=263) | 44 [36-53] (n=231) | 48 [39-57] (n=263) |
| L32-40 | paper10_rot | 97 [94-98] (n=231) | 96 [93-98] (n=263) | 96 [92-99] (n=231) | 99 [98-100] (n=263) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.75, M->P 6.00, P->M 6.25, M->M 6.00. Loss (points) by quartile of that margin (cuts 4.50, 6.25, 7.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 2 (n=42) | 0 (n=52) | 0 (n=57) | 0 (n=80) |
| M->P | 22 (n=81) | 10 (n=67) | 7 (n=41) | 1 (n=74) |
| P->M | 79 (n=63) | 58 (n=55) | 45 (n=77) | 33 (n=36) |
| M->M | 60 (n=62) | 57 (n=91) | 41 (n=73) | 46 (n=37) |
| prompt-final, pooled | 15 (n=123) | 6 (n=119) | 3 (n=98) | 1 (n=154) |
| memory-final, pooled | 70 (n=125) | 58 (n=146) | 43 (n=150) | 40 (n=73) |

Memory-final minus prompt-final, items pooled per group: raw 48; reweighted to the prompt-final margins 46, to the memory-final margins 47; matched within 0.25-logit margin bins 47 [42-52] (492 of 494 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 11, P->M 56, M->M 52; memory-final minus prompt-final 48 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 6ba91f2.
