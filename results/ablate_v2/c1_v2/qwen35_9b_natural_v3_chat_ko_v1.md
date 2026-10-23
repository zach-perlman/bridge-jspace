# C1 on tasks_v2 / qwen35_9b_natural_v3_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [88-96] (n=186) | 89 [84-93] (n=187) | 42 [34-51] (n=186) | 65 [56-74] (n=187) |
| L12-16 | paper10_rot | 92 [89-95] (n=186) | 97 [94-99] (n=187) | 97 [95-99] (n=186) | 99 [98-100] (n=187) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [88-96] (n=186) | 89 [84-93] (n=187) | 42 [34-51] (n=186) | 65 [56-74] (n=187) |
| L12-16 | paper10_rot | 92 [89-95] (n=186) | 97 [94-99] (n=187) | 97 [95-99] (n=186) | 99 [98-100] (n=187) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.50, M->P 2.75, P->M 3.88, M->M 5.62. Loss (points) by quartile of that margin (cuts 2.25, 4.12, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 19 (n=64) | 2 (n=54) | 5 (n=40) | 0 (n=28) |
| M->P | 24 (n=70) | 5 (n=55) | 3 (n=29) | 0 (n=33) |
| P->M | 73 (n=48) | 67 (n=57) | 49 (n=43) | 37 (n=38) |
| M->M | 67 (n=12) | 45 (n=31) | 29 (n=69) | 32 (n=75) |
| prompt-final, pooled | 22 (n=134) | 4 (n=109) | 4 (n=69) | 0 (n=61) |
| memory-final, pooled | 72 (n=60) | 59 (n=88) | 37 (n=112) | 34 (n=113) |

Memory-final minus prompt-final, items pooled per group: raw 37; reweighted to the prompt-final margins 46, to the memory-final margins 41; matched within 0.25-logit margin bins 41 [35-47] (366 of 373 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 8, M->P 11, P->M 58, M->M 35; memory-final minus prompt-final 37 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit fd32325.
