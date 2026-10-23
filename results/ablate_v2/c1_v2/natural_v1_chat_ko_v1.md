# C1 on tasks_v2 / natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 97 [95-99] (n=230) | 89 [85-93] (n=241) | 43 [35-52] (n=230) | 42 [33-51] (n=241) |
| L32-40 | paper10_rot | 97 [95-99] (n=230) | 95 [92-98] (n=241) | 96 [92-99] (n=230) | 100 [99-100] (n=241) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 97 [95-99] (n=230) | 89 [85-93] (n=241) | 43 [35-52] (n=230) | 42 [33-51] (n=241) |
| L32-40 | paper10_rot | 97 [95-99] (n=230) | 95 [92-98] (n=241) | 96 [92-99] (n=230) | 100 [99-100] (n=241) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.75, M->P 5.88, P->M 6.25, M->M 6.00. Loss (points) by quartile of that margin (cuts 4.62, 6.25, 7.25), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 2 (n=46) | 2 (n=47) | 2 (n=53) | 1 (n=84) |
| M->P | 20 (n=85) | 9 (n=57) | 9 (n=33) | 2 (n=66) |
| P->M | 78 (n=64) | 62 (n=53) | 45 (n=71) | 38 (n=42) |
| M->M | 70 (n=56) | 61 (n=83) | 48 (n=64) | 50 (n=38) |
| prompt-final, pooled | 14 (n=131) | 6 (n=104) | 5 (n=86) | 1 (n=150) |
| memory-final, pooled | 74 (n=120) | 62 (n=136) | 47 (n=135) | 44 (n=80) |

Memory-final minus prompt-final, items pooled per group: raw 51; reweighted to the prompt-final margins 50, to the memory-final margins 51; matched within 0.25-logit margin bins 51 [46-56] (470 of 471 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 2, M->P 11, P->M 57, M->M 58; memory-final minus prompt-final 51 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit fbf95f2.
