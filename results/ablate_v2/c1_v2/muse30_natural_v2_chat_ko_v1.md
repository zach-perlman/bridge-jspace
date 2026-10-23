# C1 on tasks_v2 / muse30_natural_v2_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 92 [87-96] (n=152) | 99 [96-100] (n=134) | 11 [6-17] (n=152) | 9 [4-16] (n=134) |
| L36-42 | paper10_rot | 96 [93-99] (n=152) | 96 [92-99] (n=134) | 95 [91-99] (n=152) | 98 [94-100] (n=134) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 92 [87-96] (n=152) | 99 [96-100] (n=134) | 11 [6-17] (n=152) | 9 [4-16] (n=134) |
| L36-42 | paper10_rot | 96 [93-99] (n=152) | 96 [92-99] (n=134) | 95 [91-99] (n=152) | 98 [94-100] (n=134) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.75, M->P 1.91, P->M 2.25, M->M 2.78. Loss (points) by quartile of that margin (cuts 1.38, 2.12, 2.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 21 (n=57) | 0 (n=46) | 0 (n=34) | 0 (n=15) |
| M->P | 2 (n=53) | 4 (n=24) | 0 (n=34) | 0 (n=23) |
| P->M | 90 (n=29) | 88 (n=43) | 83 (n=48) | 97 (n=32) |
| M->M | 100 (n=18) | 81 (n=21) | 91 (n=34) | 92 (n=61) |
| prompt-final, pooled | 12 (n=110) | 1 (n=70) | 0 (n=68) | 0 (n=38) |
| memory-final, pooled | 94 (n=47) | 86 (n=64) | 87 (n=82) | 94 (n=93) |

Memory-final minus prompt-final, items pooled per group: raw 85; reweighted to the prompt-final margins 85, to the memory-final margins 88; matched within 0.25-logit margin bins 88 [84-92] (281 of 286 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 8, M->P 1, P->M 89, M->M 91; memory-final minus prompt-final 85 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 23daf0c.
