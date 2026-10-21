# pointer_fair

## The transit sweep: C2's kill test, with "in transit" defined before the test

Lens / random = answers that become bridge alt's answer (memory → prompt: its statement digit; memory → memory: its recalled fact); copy = memory → prompt answers changed by pasting the alt prompt's states. In transit: memory → memory lens upper bound <= 2x the random's upper bound, and copy >= 50%.

### 1x the alt-prompt patch's size (primary)

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**animals**: transit layers [48]; C2 **holds**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 4] | 0% [0, 4] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 4] | 0% [0, 4] | 1% [0, 5] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 36 | 6% [0, 19] | 0% [0, 4] | 17% [11, 24] | 3% [0, 10] | 0% [0, 2] | +3 [+0, +10] | False | - |
| 40 | 2% [0, 7] | 0% [0, 4] | 41% [33, 49] | 3% [0, 11] | 0% [0, 2] | +3 [+0, +11] | False | - |
| 44 | 0% [0, 4] | 0% [0, 4] | 49% [39, 61] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 4] | 0% [0, 4] | 72% [60, 83] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | True | holds |
| 52 | 0% [0, 4] | 0% [0, 4] | 49% [35, 63] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**elements**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 7% [0, 21] | 0% [0, 4] | 4% [1, 9] | 12% [1, 36] | 0% [0, 2] | +12 [+1, +36] | False | - |
| 32 | 9% [0, 29] | 0% [0, 4] | 7% [1, 20] | 14% [1, 41] | 1% [0, 4] | +13 [+1, +40] | False | - |
| 36 | 29% [9, 54] | 0% [0, 4] | 25% [10, 45] | 28% [8, 55] | 1% [0, 5] | +27 [+7, +53] | False | - |
| 40 | 43% [21, 68] | 0% [0, 4] | 32% [15, 56] | 25% [7, 57] | 2% [0, 6] | +23 [+7, +52] | False | - |
| 44 | 30% [9, 59] | 0% [0, 4] | 49% [36, 67] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 28% [6, 59] | 0% [0, 4] | 27% [15, 39] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 52 | 8% [1, 19] | 0% [0, 4] | 6% [1, 13] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

### 4x the alt-prompt patch's size

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**animals**: transit layers [48]; C2 **holds**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 4% [0, 10] | 0% [0, 4] | 0% [0, 2] | 14% [6, 25] | 0% [0, 2] | +14 [+6, +25] | False | - |
| 32 | 5% [0, 11] | 0% [0, 4] | 1% [0, 5] | 10% [5, 16] | 0% [0, 2] | +10 [+5, +16] | False | - |
| 36 | 26% [11, 43] | 0% [0, 4] | 17% [11, 24] | 1% [0, 5] | 0% [0, 2] | +1 [+0, +3] | False | - |
| 40 | 19% [8, 31] | 0% [0, 4] | 41% [33, 49] | 1% [0, 4] | 0% [0, 2] | +1 [+0, +2] | False | - |
| 44 | 3% [1, 8] | 0% [0, 4] | 49% [39, 61] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 4] | 0% [0, 4] | 72% [60, 83] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | True | holds |
| 52 | 0% [0, 4] | 0% [0, 4] | 49% [35, 63] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**elements**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 67% [51, 84] | 2% [0, 7] | 4% [1, 9] | 23% [6, 53] | 2% [1, 6] | +21 [+5, +49] | False | - |
| 32 | 36% [21, 51] | 1% [0, 5] | 7% [1, 20] | 14% [2, 35] | 5% [1, 12] | +9 [+1, +24] | False | - |
| 36 | 27% [9, 52] | 0% [0, 4] | 25% [10, 45] | 5% [2, 11] | 3% [1, 7] | +3 [+1, +5] | False | - |
| 40 | 25% [10, 45] | 1% [0, 5] | 32% [15, 56] | 8% [1, 21] | 3% [0, 9] | +5 [+0, +12] | False | - |
| 44 | 15% [4, 33] | 1% [0, 5] | 49% [36, 67] | 2% [1, 6] | 1% [0, 4] | +1 [+0, +3] | False | - |
| 48 | 5% [0, 11] | 0% [0, 4] | 27% [15, 39] | 1% [0, 4] | 1% [0, 4] | +0 [+0, +0] | False | - |
| 52 | 1% [0, 5] | 0% [0, 4] | 6% [1, 13] | 1% [0, 4] | 1% [0, 4] | +0 [+0, +0] | False | - |

