# C1 on tasks_v2 / qwen35_9b_natural_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 88 [82-93] (n=178) | 93 [88-97] (n=190) | 48 [38-58] (n=178) | 59 [49-69] (n=190) |
| L12-16 | paper10_rot | 88 [83-93] (n=178) | 95 [91-98] (n=190) | 98 [96-99] (n=178) | 99 [98-100] (n=190) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 88 [82-93] (n=178) | 93 [88-97] (n=190) | 48 [38-58] (n=178) | 59 [49-69] (n=190) |
| L12-16 | paper10_rot | 88 [83-93] (n=178) | 95 [91-98] (n=190) | 98 [96-99] (n=178) | 99 [98-100] (n=190) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.12, M->P 3.00, P->M 4.00, M->M 5.25. Loss (points) by quartile of that margin (cuts 2.12, 4.12, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 27 (n=67) | 7 (n=41) | 0 (n=42) | 0 (n=28) |
| M->P | 16 (n=64) | 4 (n=57) | 4 (n=27) | 0 (n=42) |
| P->M | 76 (n=38) | 59 (n=58) | 35 (n=49) | 39 (n=33) |
| M->M | 82 (n=17) | 55 (n=38) | 27 (n=67) | 35 (n=68) |
| prompt-final, pooled | 21 (n=131) | 5 (n=98) | 1 (n=69) | 0 (n=70) |
| memory-final, pooled | 78 (n=55) | 57 (n=96) | 30 (n=116) | 37 (n=101) |

Memory-final minus prompt-final, items pooled per group: raw 37; reweighted to the prompt-final margins 46, to the memory-final margins 41; matched within 0.25-logit margin bins 41 [36-47] (363 of 368 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 12, M->P 7, P->M 52, M->M 41; memory-final minus prompt-final 37 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 6ba91f2.
