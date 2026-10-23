# C1 on tasks_v2 / qwen35_122b_full2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 99 | 99 | 99 | 100 | 99 | 99 |
| L39-45 | paper10 | 99 [97-100] (n=143) | 100 [100-100] (n=100) | 87 [79-93] (n=143) | 95 [91-99] (n=100) | 99 [98-100] (n=136) | 91 [84-97] (n=136) |
| L39-45 | paper10_rot | 99 [97-100] (n=143) | 97 [94-100] (n=100) | 99 [96-100] (n=143) | 98 [95-100] (n=100) | 99 [98-100] (n=136) | 99 [97-100] (n=136) |
| L24-30 | paper10 | 98 [95-100] (n=143) | 86 [80-92] (n=100) | 93 [88-97] (n=143) | 99 [97-100] (n=100) | 91 [86-96] (n=136) | 87 [78-94] (n=136) |
| L24-30 | paper10_rot | 99 [98-100] (n=143) | 95 [90-98] (n=100) | 96 [92-99] (n=143) | 100 [100-100] (n=100) | 98 [94-100] (n=136) | 91 [82-98] (n=136) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 98 | 99 | 100 | 98 | 100 |
| L39-45 | paper10 | 100 [100-100] (n=76) | 100 [100-100] (n=58) | 88 [79-96] (n=76) | 93 [87-98] (n=58) | 98 [95-100] (n=65) | 94 [87-99] (n=65) |
| L39-45 | paper10_rot | 100 [100-100] (n=76) | 95 [89-100] (n=58) | 99 [96-100] (n=76) | 97 [92-100] (n=58) | 100 [100-100] (n=65) | 100 [100-100] (n=65) |
| L24-30 | paper10 | 97 [93-100] (n=76) | 88 [80-95] (n=58) | 92 [84-98] (n=76) | 100 [100-100] (n=58) | 91 [84-97] (n=65) | 82 [69-93] (n=65) |
| L24-30 | paper10_rot | 100 [100-100] (n=76) | 95 [87-100] (n=58) | 95 [90-99] (n=76) | 100 [100-100] (n=58) | 95 [86-100] (n=65) | 92 [79-100] (n=65) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 | 100 | 99 |
| L39-45 | paper10 | 99 [94-100] (n=67) | 100 [100-100] (n=42) | 85 [72-94] (n=67) | 98 [92-100] (n=42) | 100 [100-100] (n=71) | 89 [79-97] (n=71) |
| L39-45 | paper10_rot | 99 [94-100] (n=67) | 100 [100-100] (n=42) | 99 [95-100] (n=67) | 100 [100-100] (n=42) | 99 [96-100] (n=71) | 99 [95-100] (n=71) |
| L24-30 | paper10 | 99 [94-100] (n=67) | 83 [73-92] (n=42) | 94 [85-100] (n=67) | 98 [92-100] (n=42) | 92 [85-97] (n=71) | 92 [84-98] (n=71) |
| L24-30 | paper10_rot | 99 [95-100] (n=67) | 95 [88-100] (n=42) | 97 [92-100] (n=67) | 100 [100-100] (n=42) | 100 [100-100] (n=71) | 90 [82-97] (n=71) |


## Margin-matched gap under paper10 at L39-45 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 4.88, M->P 4.31, P->M 3.88, M->M 4.06. Loss (points) by quartile of that margin (cuts 3.50, 4.38, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=14) | 0 (n=25) | 0 (n=49) | 0 (n=55) |
| M->P | -4 (n=24) | 0 (n=29) | 0 (n=24) | 0 (n=23) |
| P->M | 27 (n=56) | 7 (n=44) | 0 (n=23) | 0 (n=20) |
| M->M | 10 (n=31) | 6 (n=35) | 0 (n=16) | 0 (n=18) |
| prompt-final, pooled | -3 (n=38) | 0 (n=54) | 0 (n=73) | 0 (n=78) |
| memory-final, pooled | 21 (n=87) | 6 (n=79) | 0 (n=39) | 0 (n=38) |

Memory-final minus prompt-final, items pooled per group: raw 10; reweighted to the prompt-final margins 5, to the memory-final margins 10; matched within 0.25-logit margin bins 8 [4-11] (234 of 243 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L39-45: losses P->P 0, M->P -1, P->M 13, M->M 5, C->P 0, C->M 8; memory-final minus prompt-final 9 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit b8eb92f.
