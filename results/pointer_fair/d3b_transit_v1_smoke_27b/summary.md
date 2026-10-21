# pointer_fair

## The transit sweep: C2's kill test, with "in transit" defined before the test

Lens / random = answers that become bridge alt's answer (memory → prompt: its statement digit; memory → memory: its recalled fact); copy = memory → prompt answers changed by pasting the alt prompt's states. In transit: memory → memory lens upper bound <= 2x the random's upper bound, and copy >= 50%.

### 1x the alt-prompt patch's size (primary)

Flags: {"c2_transit": false, "no_transit": false, "c2_killed": false}

**animals**: transit layers [48, 52]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 25% [0, 75] | 0% [0, 49] | +25 [+0, +75] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 25% [0, 75] | 0% [0, 49] | +25 [+0, +75] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |

**elements**: transit layers [36, 40, 44]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 25% [0, 100] | 25% [0, 100] | 0% [0, 49] | +25 [+0, +100] | False | - |
| 32 | 25% [0, 100] | 0% [0, 49] | 25% [0, 100] | 25% [0, 100] | 0% [0, 49] | +25 [+0, +100] | False | - |
| 36 | 25% [0, 70] | 0% [0, 49] | 50% [0, 100] | 50% [0, 100] | 0% [0, 49] | +50 [+0, +100] | True | unclear |
| 40 | 50% [0, 85] | 0% [0, 49] | 50% [0, 100] | 50% [0, 100] | 0% [0, 49] | +50 [+0, +100] | True | unclear |
| 44 | 50% [0, 85] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 48 | 50% [0, 85] | 0% [0, 49] | 25% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 52 | 25% [0, 70] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

### 4x the alt-prompt patch's size

Flags: {"c2_transit": false, "no_transit": false, "c2_killed": false}

**animals**: transit layers [48, 52]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | +25 [+0, +75] | False | - |
| 36 | 50% [0, 100] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |

**elements**: transit layers [36, 40, 44]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 75% [0, 100] | 0% [0, 49] | 25% [0, 100] | 25% [0, 100] | 0% [0, 49] | +25 [+0, +100] | False | - |
| 32 | 50% [0, 85] | 0% [0, 49] | 25% [0, 100] | 25% [0, 100] | 0% [0, 49] | +25 [+0, +100] | False | - |
| 36 | 50% [0, 85] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 40 | 25% [0, 70] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 25% [0, 100] | -25 [-100, +0] | True | holds |
| 44 | 25% [0, 70] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 25% [0, 100] | -25 [-100, +0] | True | holds |
| 48 | 25% [0, 70] | 0% [0, 49] | 25% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

