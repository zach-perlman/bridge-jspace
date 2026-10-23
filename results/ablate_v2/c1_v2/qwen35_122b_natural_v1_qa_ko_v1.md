# C1 on tasks_v2 / qwen35_122b_natural_v1_qa_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 95 | 89 | 99 | 100 |
| L39-45 | paper10 | 52 [43-63] (n=80) | 36 [27-45] (n=99) | 5 [1-10] (n=80) | 11 [5-18] (n=99) |
| L39-45 | paper10_rot | 89 [82-95] (n=80) | 85 [77-91] (n=99) | 91 [85-96] (n=80) | 100 [100-100] (n=99) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 95 | 89 | 99 | 100 |
| L39-45 | paper10 | 52 [43-63] (n=80) | 36 [27-45] (n=99) | 5 [1-10] (n=80) | 11 [5-18] (n=99) |
| L39-45 | paper10_rot | 89 [82-95] (n=80) | 85 [77-91] (n=99) | 91 [85-96] (n=80) | 100 [100-100] (n=99) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L39-45 | paper10 | - | - | - | - |
| L39-45 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L39-45 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 0.75, M->P 0.75, P->M 0.88, M->M 2.25. Loss (points) by quartile of that margin (cuts 0.50, 1.12, 1.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 60 (n=30) | 48 (n=27) | 17 (n=18) | 0 (n=5) |
| M->P | 63 (n=43) | 61 (n=31) | 30 (n=20) | 0 (n=5) |
| P->M | 94 (n=17) | 97 (n=35) | 90 (n=21) | 86 (n=7) |
| M->M | - (n=0) | 100 (n=10) | 97 (n=30) | 83 (n=59) |
| prompt-final, pooled | 62 (n=73) | 55 (n=58) | 24 (n=38) | 0 (n=10) |
| memory-final, pooled | 94 (n=17) | 98 (n=45) | 94 (n=51) | 83 (n=66) |

Memory-final minus prompt-final, items pooled per group: raw 43; reweighted to the prompt-final margins 47, to the memory-final margins 65; matched within 0.25-logit margin bins 61 [51-69] (141 of 179 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L39-45: losses P->P 42, M->P 53, P->M 94, M->M 89; memory-final minus prompt-final 44 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 07f486e.
