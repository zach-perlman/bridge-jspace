# C1 on tasks_v2 / muse30_natural_v3_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 89 [84-94] (n=149) | 100 [100-100] (n=142) | 9 [4-16] (n=149) | 9 [4-16] (n=142) |
| L36-42 | paper10_rot | 94 [90-97] (n=149) | 95 [90-99] (n=142) | 98 [95-100] (n=149) | 96 [91-99] (n=142) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 89 [84-94] (n=149) | 100 [100-100] (n=142) | 9 [4-16] (n=149) | 9 [4-16] (n=142) |
| L36-42 | paper10_rot | 94 [90-97] (n=149) | 95 [90-99] (n=142) | 98 [95-100] (n=149) | 96 [91-99] (n=142) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.75, M->P 1.62, P->M 2.25, M->M 2.50. Loss (points) by quartile of that margin (cuts 1.25, 2.12, 2.81), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 31 (n=51) | 0 (n=52) | 0 (n=28) | 0 (n=18) |
| M->P | 0 (n=56) | 0 (n=36) | 0 (n=25) | 0 (n=25) |
| P->M | 95 (n=22) | 90 (n=52) | 83 (n=35) | 95 (n=40) |
| M->M | 94 (n=17) | 97 (n=30) | 86 (n=36) | 90 (n=59) |
| prompt-final, pooled | 15 (n=107) | 0 (n=88) | 0 (n=53) | 0 (n=43) |
| memory-final, pooled | 95 (n=39) | 93 (n=82) | 85 (n=71) | 92 (n=99) |

Memory-final minus prompt-final, items pooled per group: raw 85; reweighted to the prompt-final margins 86, to the memory-final margins 89; matched within 0.25-logit margin bins 89 [85-92] (284 of 291 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 11, M->P 0, P->M 91, M->M 91; memory-final minus prompt-final 85 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit fd32325.
