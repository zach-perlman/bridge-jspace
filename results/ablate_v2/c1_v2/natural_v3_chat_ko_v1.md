# C1 on tasks_v2 / natural_v3_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 97 [95-99] (n=213) | 87 [82-91] (n=248) | 53 [43-62] (n=213) | 46 [36-55] (n=248) |
| L32-40 | paper10_rot | 99 [98-100] (n=213) | 97 [94-99] (n=248) | 97 [94-99] (n=213) | 99 [98-100] (n=248) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 97 [95-99] (n=213) | 87 [82-91] (n=248) | 53 [43-62] (n=213) | 46 [36-55] (n=248) |
| L32-40 | paper10_rot | 99 [98-100] (n=213) | 97 [94-99] (n=248) | 97 [94-99] (n=213) | 99 [98-100] (n=248) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 7.00, M->P 5.38, P->M 6.50, M->M 6.19. Loss (points) by quartile of that margin (cuts 4.75, 6.25, 7.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 6 (n=34) | 5 (n=43) | 2 (n=53) | 1 (n=83) |
| M->P | 25 (n=89) | 9 (n=70) | 12 (n=24) | 3 (n=65) |
| P->M | 82 (n=50) | 45 (n=49) | 36 (n=69) | 29 (n=45) |
| M->M | 69 (n=64) | 59 (n=69) | 42 (n=80) | 40 (n=35) |
| prompt-final, pooled | 20 (n=123) | 7 (n=113) | 5 (n=77) | 2 (n=148) |
| memory-final, pooled | 75 (n=114) | 53 (n=118) | 40 (n=149) | 34 (n=80) |

Memory-final minus prompt-final, items pooled per group: raw 42; reweighted to the prompt-final margins 42, to the memory-final margins 42; matched within 0.25-logit margin bins 41 [36-47] (458 of 461 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 3, M->P 13, P->M 47, M->M 54; memory-final minus prompt-final 42 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit fd32325.
