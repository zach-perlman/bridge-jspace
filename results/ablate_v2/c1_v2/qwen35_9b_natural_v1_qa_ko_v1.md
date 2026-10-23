# C1 on tasks_v2 / qwen35_9b_natural_v1_qa_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 98 | 100 |
| L12-16 | paper10 | 60 [51-69] (n=129) | 52 [45-60] (n=160) | 30 [20-40] (n=129) | 35 [25-45] (n=160) |
| L12-16 | paper10_rot | 88 [83-93] (n=129) | 81 [75-87] (n=160) | 91 [86-96] (n=129) | 96 [91-99] (n=160) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 98 | 100 |
| L12-16 | paper10 | 60 [51-69] (n=129) | 52 [45-60] (n=160) | 30 [20-40] (n=129) | 35 [25-45] (n=160) |
| L12-16 | paper10_rot | 88 [83-93] (n=129) | 81 [75-87] (n=160) | 91 [86-96] (n=129) | 96 [91-99] (n=160) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.12, M->P 1.12, P->M 1.38, M->M 2.00. Loss (points) by quartile of that margin (cuts 0.75, 1.38, 2.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 76 (n=46) | 39 (n=31) | 11 (n=35) | 6 (n=17) |
| M->P | 70 (n=57) | 47 (n=49) | 28 (n=39) | 7 (n=15) |
| P->M | 87 (n=31) | 86 (n=37) | 56 (n=27) | 41 (n=34) |
| M->M | 85 (n=13) | 72 (n=32) | 67 (n=42) | 58 (n=73) |
| prompt-final, pooled | 73 (n=103) | 44 (n=80) | 20 (n=74) | 6 (n=32) |
| memory-final, pooled | 86 (n=44) | 80 (n=69) | 62 (n=69) | 52 (n=107) |

Memory-final minus prompt-final, items pooled per group: raw 22; reweighted to the prompt-final margins 31, to the memory-final margins 38; matched within 0.25-logit margin bins 38 [31-45] (272 of 289 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 40, M->P 47, P->M 68, M->M 65; memory-final minus prompt-final 23 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 3bc4e9e.
