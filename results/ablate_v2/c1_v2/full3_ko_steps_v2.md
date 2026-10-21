# C1 on tasks_v2 / full3_ko_steps_v2 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## secondary stratum (planets, three-step words), all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 87 | 89 | 78 |
| L32-40 | paper10 | 95 | 95 | 94 | 88 | 88 | 80 |
| L32-40 | paper10_rot | 99 | 100 | 98 | 93 | 91 | 85 |

## step2 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 96 | 95 | 100 | 99 | 97 | 100 |
| L32-40 | paper10 | 96 | 94 | 86 | 96 | 97 | 85 |
| L32-40 | paper10_rot | 96 | 95 | 99 | 97 | 95 | 100 |

## step3 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 | 76 | 100 | 100 | 57 | 100 |
| L32-40 | paper10_rot | 100 | 98 | 100 | 100 | 99 | 100 |

Rule at L32-40: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 228b09a.
