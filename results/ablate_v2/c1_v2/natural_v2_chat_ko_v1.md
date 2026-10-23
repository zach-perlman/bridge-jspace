# C1 on tasks_v2 / natural_v2_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 96 [94-99] (n=224) | 86 [81-91] (n=242) | 50 [41-58] (n=224) | 45 [35-55] (n=242) |
| L32-40 | paper10_rot | 98 [96-100] (n=224) | 97 [94-99] (n=242) | 96 [92-99] (n=224) | 100 [99-100] (n=242) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 96 [94-99] (n=224) | 86 [81-91] (n=242) | 50 [41-58] (n=224) | 45 [35-55] (n=242) |
| L32-40 | paper10_rot | 98 [96-100] (n=224) | 97 [94-99] (n=242) | 96 [92-99] (n=224) | 100 [99-100] (n=242) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 7.00, M->P 5.88, P->M 6.38, M->M 6.12. Loss (points) by quartile of that margin (cuts 4.75, 6.38, 7.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 14 (n=42) | 2 (n=48) | 0 (n=44) | 0 (n=90) |
| M->P | 34 (n=77) | 10 (n=62) | 2 (n=43) | 2 (n=60) |
| P->M | 86 (n=56) | 54 (n=57) | 31 (n=70) | 27 (n=41) |
| M->M | 61 (n=61) | 61 (n=83) | 52 (n=61) | 38 (n=37) |
| prompt-final, pooled | 27 (n=119) | 6 (n=110) | 1 (n=87) | 1 (n=150) |
| memory-final, pooled | 73 (n=117) | 59 (n=140) | 41 (n=131) | 32 (n=78) |

Memory-final minus prompt-final, items pooled per group: raw 44; reweighted to the prompt-final margins 42, to the memory-final margins 44; matched within 0.25-logit margin bins 42 [36-48] (461 of 466 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 3, M->P 14, P->M 50, M->M 55; memory-final minus prompt-final 44 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 23daf0c.
