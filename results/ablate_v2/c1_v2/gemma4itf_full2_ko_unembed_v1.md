# C1 on tasks_v2 / gemma4itf_full2_ko_unembed_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | unembed10 | 9 [5-12] (n=141) | 12 [6-18] (n=92) | 16 [5-29] (n=141) | 12 [4-24] (n=92) | 18 [10-26] (n=128) | 11 [3-21] (n=128) |
| L11-19 | unembed10_rot | 6 [3-10] (n=141) | 8 [2-15] (n=92) | 5 [1-10] (n=141) | 10 [0-23] (n=92) | 4 [1-8] (n=128) | 7 [2-14] (n=128) |
| L19-27 | unembed10 | 100 [100-100] (n=141) | 95 [89-99] (n=92) | 85 [77-92] (n=141) | 93 [89-98] (n=92) | 97 [93-100] (n=128) | 85 [78-92] (n=128) |
| L19-27 | unembed10_rot | 8 [5-11] (n=141) | 10 [4-16] (n=92) | 14 [7-23] (n=141) | 41 [25-57] (n=92) | 16 [10-21] (n=128) | 29 [19-39] (n=128) |
| L48-56 | unembed10 | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=128) | 0 [0-0] (n=128) |
| L48-56 | unembed10_rot | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=128) | 0 [0-0] (n=128) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | unembed10 | 10 [4-17] (n=68) | 11 [2-20] (n=47) | 22 [8-37] (n=68) | 17 [5-35] (n=47) | 15 [6-27] (n=52) | 15 [4-31] (n=52) |
| L11-19 | unembed10_rot | 6 [1-13] (n=68) | 9 [2-19] (n=47) | 4 [0-10] (n=68) | 13 [0-30] (n=47) | 4 [0-9] (n=52) | 8 [2-17] (n=52) |
| L19-27 | unembed10 | 100 [100-100] (n=68) | 94 [86-100] (n=47) | 81 [68-92] (n=68) | 91 [84-98] (n=47) | 98 [93-100] (n=52) | 69 [55-83] (n=52) |
| L19-27 | unembed10_rot | 6 [1-11] (n=68) | 9 [2-17] (n=47) | 13 [4-26] (n=68) | 36 [18-53] (n=47) | 15 [7-24] (n=52) | 27 [14-43] (n=52) |
| L48-56 | unembed10 | 0 [0-0] (n=68) | 0 [0-0] (n=47) | 0 [0-0] (n=68) | 0 [0-0] (n=47) | 0 [0-0] (n=52) | 0 [0-0] (n=52) |
| L48-56 | unembed10_rot | 0 [0-0] (n=68) | 0 [0-0] (n=47) | 0 [0-0] (n=68) | 0 [0-0] (n=47) | 0 [0-0] (n=52) | 0 [0-0] (n=52) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | unembed10 | 7 [2-14] (n=73) | 13 [5-24] (n=45) | 10 [1-21] (n=73) | 7 [0-17] (n=45) | 20 [11-29] (n=76) | 8 [1-17] (n=76) |
| L11-19 | unembed10_rot | 7 [2-12] (n=73) | 7 [0-16] (n=45) | 5 [1-11] (n=73) | 7 [0-17] (n=45) | 4 [0-8] (n=76) | 7 [2-13] (n=76) |
| L19-27 | unembed10 | 100 [100-100] (n=73) | 96 [90-100] (n=45) | 89 [83-95] (n=73) | 96 [89-100] (n=45) | 96 [90-100] (n=76) | 96 [91-100] (n=76) |
| L19-27 | unembed10_rot | 10 [4-18] (n=73) | 11 [2-23] (n=45) | 15 [8-25] (n=73) | 47 [29-65] (n=45) | 16 [8-24] (n=76) | 30 [19-43] (n=76) |
| L48-56 | unembed10 | 0 [0-0] (n=73) | 0 [0-0] (n=45) | 0 [0-0] (n=73) | 0 [0-0] (n=45) | 0 [0-0] (n=76) | 0 [0-0] (n=76) |
| L48-56 | unembed10_rot | 0 [0-0] (n=73) | 0 [0-0] (n=45) | 0 [0-0] (n=73) | 0 [0-0] (n=45) | 0 [0-0] (n=76) | 0 [0-0] (n=76) |


## Margin-matched gap under unembed10 at L48-56 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 16.50, M->P 15.38, P->M 14.44, M->M 14.59. Loss (points) by quartile of that margin (cuts 13.75, 15.50, 16.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 100 (n=4) | 100 (n=26) | 100 (n=45) | 100 (n=66) |
| M->P | 100 (n=24) | 100 (n=26) | 100 (n=27) | 100 (n=15) |
| P->M | 100 (n=55) | 100 (n=41) | 100 (n=30) | 100 (n=15) |
| M->M | 100 (n=37) | 100 (n=23) | 100 (n=17) | 100 (n=15) |
| prompt-final, pooled | 100 (n=28) | 100 (n=52) | 100 (n=72) | 100 (n=81) |
| memory-final, pooled | 100 (n=92) | 100 (n=64) | 100 (n=47) | 100 (n=30) |

Memory-final minus prompt-final, items pooled per group: raw 0; reweighted to the prompt-final margins 0, to the memory-final margins 0; matched within 0.25-logit margin bins 0 [0-0] (193 of 233 memory-final items have a same-bin partner) points.

Rule at L48-56: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 1249d90.
