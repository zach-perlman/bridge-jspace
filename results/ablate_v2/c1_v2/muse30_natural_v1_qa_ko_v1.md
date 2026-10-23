# C1 on tasks_v2 / muse30_natural_v1_qa_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 96 [93-99] (n=176) | 95 [91-98] (n=225) | 15 [10-22] (n=176) | 20 [13-29] (n=225) |
| L36-42 | paper10_rot | 97 [94-99] (n=176) | 97 [94-99] (n=225) | 99 [98-100] (n=176) | 98 [96-100] (n=225) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L36-42 | paper10 | 96 [93-99] (n=176) | 95 [91-98] (n=225) | 15 [10-22] (n=176) | 20 [13-29] (n=225) |
| L36-42 | paper10_rot | 97 [94-99] (n=176) | 97 [94-99] (n=225) | 99 [98-100] (n=176) | 98 [96-100] (n=225) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.16, M->P 2.62, P->M 4.62, M->M 4.50. Loss (points) by quartile of that margin (cuts 2.50, 3.75, 4.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 9 (n=64) | 0 (n=44) | 0 (n=41) | 0 (n=27) |
| M->P | 10 (n=111) | 0 (n=78) | 0 (n=31) | 0 (n=5) |
| P->M | 100 (n=17) | 79 (n=24) | 81 (n=59) | 86 (n=76) |
| M->M | 93 (n=15) | 82 (n=49) | 85 (n=80) | 70 (n=81) |
| prompt-final, pooled | 10 (n=175) | 0 (n=122) | 0 (n=72) | 0 (n=32) |
| memory-final, pooled | 97 (n=32) | 81 (n=73) | 83 (n=139) | 78 (n=157) |

Memory-final minus prompt-final, items pooled per group: raw 78; reweighted to the prompt-final margins 84, to the memory-final margins 81; matched within 0.25-logit margin bins 81 [77-85] (393 of 401 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 3, M->P 5, P->M 85, M->M 80; memory-final minus prompt-final 78 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 07f486e.
