# C1 on tasks_v2 / qwen35_9b_full3_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - | - | - |

## secondary stratum (planets, three-step words), all formats

| band | condition | P->P->P | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 50 | 71 | 46 |
| L12-16 | paper10 | 98 | 96 | 100 | 86 | 79 | 83 |
| L12-16 | paper10_rot | 96 | 94 | 95 | 41 | 64 | 40 |

## step2 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 89 | 84 | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 91 | 86 | 97 | 100 | 100 | 86 |
| L12-16 | paper10_rot | 79 | 69 | 100 | 77 | 86 | 100 |

## step3 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 94 | 71 | 98 | 100 | 71 | 97 |
| L12-16 | paper10_rot | 100 | 100 | 100 | 100 | 100 | 100 |


Rule at L12-16: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit ad711b6.
