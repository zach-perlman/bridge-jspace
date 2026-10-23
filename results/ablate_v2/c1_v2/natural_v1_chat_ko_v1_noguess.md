# C1 on tasks_v2 / natural_v1_chat_ko_v1 WITHOUT guessable items (robustness split) (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 98 [95-99] (n=201) | 89 [84-94] (n=173) | 43 [35-51] (n=209) | 41 [32-51] (n=205) |
| L32-40 | paper10_rot | 97 [95-99] (n=201) | 94 [89-97] (n=173) | 96 [92-99] (n=209) | 100 [98-100] (n=205) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 98 [95-99] (n=201) | 89 [84-94] (n=173) | 43 [35-51] (n=209) | 41 [32-51] (n=205) |
| L32-40 | paper10_rot | 97 [95-99] (n=201) | 94 [89-97] (n=173) | 96 [92-99] (n=209) | 100 [98-100] (n=205) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.75, M->P 5.38, P->M 6.25, M->M 6.00. Loss (points) by quartile of that margin (cuts 4.50, 6.12, 7.25), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=37) | 3 (n=39) | 2 (n=54) | 1 (n=71) |
| M->P | 23 (n=66) | 5 (n=39) | 8 (n=26) | 0 (n=42) |
| P->M | 80 (n=60) | 61 (n=44) | 46 (n=67) | 37 (n=38) |
| M->M | 68 (n=44) | 66 (n=70) | 47 (n=59) | 53 (n=32) |
| prompt-final, pooled | 15 (n=103) | 4 (n=78) | 4 (n=80) | 1 (n=113) |
| memory-final, pooled | 75 (n=104) | 64 (n=114) | 47 (n=126) | 44 (n=70) |

Memory-final minus prompt-final, items pooled per group: raw 52; reweighted to the prompt-final margins 52, to the memory-final margins 52; matched within 0.25-logit margin bins 53 [47-58] (413 of 414 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 1, M->P 11, P->M 57, M->M 59; memory-final minus prompt-final 52 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 95f5897.
