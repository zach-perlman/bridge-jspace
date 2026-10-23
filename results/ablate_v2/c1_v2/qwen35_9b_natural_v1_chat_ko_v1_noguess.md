# C1 on tasks_v2 / qwen35_9b_natural_v1_chat_ko_v1 WITHOUT guessable items (robustness split) (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 83 [76-89] (n=128) | 95 [90-98] (n=131) | 43 [33-53] (n=162) | 58 [47-69] (n=161) |
| L12-16 | paper10_rot | 88 [81-94] (n=128) | 94 [89-98] (n=131) | 98 [96-100] (n=162) | 99 [98-100] (n=161) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 83 [76-89] (n=128) | 95 [90-98] (n=131) | 43 [33-53] (n=162) | 58 [47-69] (n=161) |
| L12-16 | paper10_rot | 88 [81-94] (n=128) | 94 [89-98] (n=131) | 98 [96-100] (n=162) | 99 [98-100] (n=161) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.81, M->P 3.25, P->M 3.88, M->M 5.38. Loss (points) by quartile of that margin (cuts 2.25, 4.25, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 30 (n=54) | 14 (n=29) | 0 (n=25) | 5 (n=20) |
| M->P | 12 (n=41) | 0 (n=33) | 9 (n=22) | 0 (n=35) |
| P->M | 78 (n=40) | 62 (n=56) | 38 (n=37) | 45 (n=29) |
| M->M | 73 (n=11) | 53 (n=43) | 28 (n=47) | 38 (n=60) |
| prompt-final, pooled | 22 (n=95) | 6 (n=62) | 4 (n=47) | 2 (n=55) |
| memory-final, pooled | 76 (n=51) | 59 (n=99) | 32 (n=84) | 40 (n=89) |

Memory-final minus prompt-final, items pooled per group: raw 39; reweighted to the prompt-final margins 46, to the memory-final margins 42; matched within 0.25-logit margin bins 41 [33-48] (321 of 323 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 16, M->P 5, P->M 57, M->M 42; memory-final minus prompt-final 39 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 95f5897.
