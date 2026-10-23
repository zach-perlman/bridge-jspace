# C1 on tasks_v2 / qwen35_9b_natural_v2_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 95 [92-98] (n=169) | 92 [88-96] (n=192) | 49 [38-58] (n=169) | 63 [54-72] (n=192) |
| L12-16 | paper10_rot | 88 [82-94] (n=169) | 92 [88-96] (n=192) | 97 [94-99] (n=169) | 98 [96-100] (n=192) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 95 [92-98] (n=169) | 92 [88-96] (n=192) | 49 [38-58] (n=169) | 63 [54-72] (n=192) |
| L12-16 | paper10_rot | 88 [82-94] (n=169) | 92 [88-96] (n=192) | 97 [94-99] (n=169) | 98 [96-100] (n=192) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.50, M->P 3.19, P->M 4.38, M->M 5.25. Loss (points) by quartile of that margin (cuts 2.38, 4.25, 5.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 8 (n=59) | 2 (n=53) | 7 (n=30) | 0 (n=27) |
| M->P | 19 (n=73) | 0 (n=55) | 0 (n=33) | 3 (n=31) |
| P->M | 74 (n=35) | 48 (n=46) | 47 (n=43) | 42 (n=45) |
| M->M | 52 (n=21) | 52 (n=33) | 32 (n=62) | 30 (n=76) |
| prompt-final, pooled | 14 (n=132) | 1 (n=108) | 3 (n=63) | 2 (n=58) |
| memory-final, pooled | 66 (n=56) | 49 (n=79) | 38 (n=105) | 35 (n=121) |

Memory-final minus prompt-final, items pooled per group: raw 37; reweighted to the prompt-final margins 45, to the memory-final margins 40; matched within 0.25-logit margin bins 41 [35-46] (359 of 361 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 5, M->P 8, P->M 51, M->M 37; memory-final minus prompt-final 38 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 23daf0c.
