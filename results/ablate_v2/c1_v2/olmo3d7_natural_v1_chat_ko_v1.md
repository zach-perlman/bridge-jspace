# C1 on tasks_v2 / olmo3d7_natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 91 [84-97] (n=75) | 89 [78-96] (n=62) | 68 [56-79] (n=75) | 77 [65-89] (n=62) |
| L10-14 | paper10_rot | 88 [81-96] (n=75) | 95 [89-100] (n=62) | 80 [69-89] (n=75) | 94 [87-98] (n=62) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 91 [84-97] (n=75) | 89 [78-96] (n=62) | 68 [56-79] (n=75) | 77 [65-89] (n=62) |
| L10-14 | paper10_rot | 88 [81-96] (n=75) | 95 [89-100] (n=62) | 80 [69-89] (n=75) | 94 [87-98] (n=62) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L10-14 | paper10 | - | - | - | - |
| L10-14 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.38, M->P 5.38, P->M 3.69, M->M 4.81. Loss (points) by quartile of that margin (cuts 2.12, 4.25, 6.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 12 (n=24) | 18 (n=22) | 0 (n=13) | 0 (n=16) |
| M->P | 43 (n=14) | 0 (n=10) | 0 (n=16) | 5 (n=22) |
| P->M | 62 (n=24) | 30 (n=23) | 8 (n=13) | 7 (n=15) |
| M->M | 62 (n=8) | 44 (n=16) | 0 (n=26) | 17 (n=12) |
| prompt-final, pooled | 24 (n=38) | 12 (n=32) | 0 (n=29) | 3 (n=38) |
| memory-final, pooled | 62 (n=32) | 36 (n=39) | 3 (n=39) | 11 (n=27) |

Memory-final minus prompt-final, items pooled per group: raw 18; reweighted to the prompt-final margins 19, to the memory-final margins 18; matched within 0.25-logit margin bins 18 [10-27] (133 of 137 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L10-14: losses P->P 9, M->P 11, P->M 32, M->M 23; memory-final minus prompt-final 17 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit c34be5d.
