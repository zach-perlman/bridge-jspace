# C1 on tasks_v2 / natural_v1_qa_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 96 [93-99] (n=193) | 84 [79-89] (n=270) | 37 [30-44] (n=193) | 51 [43-60] (n=270) |
| L32-40 | paper10_rot | 98 [97-100] (n=193) | 95 [92-98] (n=270) | 98 [96-100] (n=193) | 99 [98-100] (n=270) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 96 [93-99] (n=193) | 84 [79-89] (n=270) | 37 [30-44] (n=193) | 51 [43-60] (n=270) |
| L32-40 | paper10_rot | 98 [97-100] (n=193) | 95 [92-98] (n=270) | 98 [96-100] (n=193) | 99 [98-100] (n=270) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P -5.75, M->P -5.50, P->M -5.12, M->M -2.88. Loss (points) by quartile of that margin (cuts -5.88, -5.00, -3.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 4 (n=93) | 4 (n=53) | 2 (n=44) | 0 (n=3) |
| M->P | 13 (n=105) | 17 (n=83) | 14 (n=76) | 33 (n=6) |
| P->M | 69 (n=42) | 64 (n=80) | 58 (n=64) | 71 (n=7) |
| M->M | 67 (n=3) | 83 (n=6) | 60 (n=53) | 44 (n=208) |
| prompt-final, pooled | 9 (n=198) | 12 (n=136) | 10 (n=120) | 22 (n=9) |
| memory-final, pooled | 69 (n=45) | 65 (n=86) | 59 (n=117) | 45 (n=215) |

Memory-final minus prompt-final, items pooled per group: raw 44; reweighted to the prompt-final margins 54, to the memory-final margins 39; matched within 0.25-logit margin bins 46 [35-55] (339 of 463 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 4, M->P 15, P->M 63, M->M 49; memory-final minus prompt-final 46 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 6ba91f2.
