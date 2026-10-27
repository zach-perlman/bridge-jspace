# pointer_fair (pointer_v4)

Intervals: entity-cluster bootstrap 95% (asked entity within its topic), widened to Wilson where wider; 'item level': Wilson alone. n items / k entities / t wordings.

Unedited answers = answer org: memory → prompt 100% [99, 100] (n=523); memory → memory 100% [99, 100] (n=520)

## memory → prompt, after the cue, layers 32-40 at once, 1x: **not shown: 1 of 3 topics pass with valid controls (needs 2)**

Flags: {"pointer_at_lens_depth": false, "pointer_later_only": false, "not_lookup_specific": false}

| topic | pointer | item level | lens | random | shuffled | memory → memory changed (pointer) | pointer − lens | pointer − random | pointer 2x | lens 2x | passes / valid | n / k / t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| countries | 37% [31, 44] | 37% [31, 44] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] (n=211) | +37 [+31, +43] | +37 [+31, +43] | 41% [34, 47] | 0% [0, 2] | True / True | 212 / 36 / 9 |
| animals | 26% [20, 32] | 26% [20, 32] | 9% [3, 16] | 1% [0, 3] | 0% [0, 2] | 4% [1, 8] (n=192) | +17 [+9, +25] | +25 [+19, +31] | 33% [26, 41] | 2% [0, 5] | False / True | 191 / 34 / 9 |
| body | 43% [35, 52] | 43% [35, 52] | 20% [10, 31] | 1% [0, 5] | 2% [0, 7] | 10% [3, 21] (n=117) | +23 [+11, +37] | +42 [+34, +51] | 41% [32, 50] | 2% [0, 7] | True / False | 120 / 15 / 9 |
| pooled | 34% [30, 39] | 34% [30, 39] | 8% [5, 11] | 0% [0, 1] | 1% [0, 2] | 4% [1, 6] (n=520) | +27 [+22, +32] | +34 [+30, +38] | 38% [34, 42] | 1% [0, 2] | True / True | 523 / 85 / 27 |

| held out of the fit | pointer | lens | n / k / t |
|---|---|---|---|
| asked entity held out | 30% [21, 39] | 9% [2, 17] | 116 / 28 / 12 |
| wording held out | 36% [31, 42] | 9% [5, 14] | 272 / 57 / 15 |
| both held out | 35% [27, 43] | 5% [0, 12] | 135 / 28 / 15 |

Overshoot (off-target statement answers beyond the target vs a uniform choice): pooled 57/73 vs 34.0 (+32 [+24, +39] per answer); countries 14/16 vs 8.0 (+38 [+22, +53] per answer); animals 26/35 vs 15.67 (+30 [+19, +41] per answer); body 17/22 vs 10.33 (+30 [+20, +44] per answer)
Shuffled-label direction: pooled 13/19 vs 13.33; countries 0/0 vs 0.0; animals 6/9 vs 6.33; body 7/10 vs 7.0

## memory → prompt, question words (reported, not decisive), layers 32-40 at once, 1x: **not shown: 0 of 3 topics pass with valid controls (needs 2)**

Flags: {"pointer_at_lens_depth": false, "pointer_later_only": false, "not_lookup_specific": true}

| topic | pointer | item level | lens | random | shuffled | memory → memory changed (pointer) | pointer − lens | pointer − random | pointer 2x | lens 2x | passes / valid | n / k / t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| countries | 59% [53, 66] | 59% [53, 66] | 0% [0, 2] | 0% [0, 2] | 0% [0, 3] | 15% [10, 21] (n=211) | +59 [+54, +64] | +59 [+54, +64] | 56% [49, 62] | 4% [1, 7] | True / False | 212 / 36 / 9 |
| animals | 48% [41, 55] | 48% [41, 55] | 31% [20, 43] | 1% [0, 3] | 3% [0, 7] | 20% [13, 28] (n=192) | +17 [+4, +30] | +47 [+40, +55] | 38% [31, 45] | 43% [32, 55] | False / False | 191 / 34 / 9 |
| body | 40% [29, 52] | 40% [32, 49] | 48% [28, 67] | 1% [0, 5] | 2% [0, 7] | 17% [7, 29] (n=117) | -8 [-27, +14] | +39 [+28, +51] | 28% [18, 41] | 52% [34, 70] | False / False | 120 / 15 / 9 |
| pooled | 51% [46, 55] | 51% [46, 55] | 22% [16, 28] | 0% [0, 1] | 2% [1, 4] | 18% [13, 22] (n=520) | +28 [+21, +36] | +50 [+46, +55] | 43% [39, 48] | 29% [23, 36] | True / False | 523 / 85 / 27 |

| held out of the fit | pointer | lens | n / k / t |
|---|---|---|---|
| asked entity held out | 51% [42, 60] | 14% [7, 21] | 116 / 28 / 12 |
| wording held out | 53% [47, 59] | 26% [18, 34] | 272 / 57 / 15 |
| both held out | 45% [37, 54] | 21% [7, 36] | 135 / 28 / 15 |

Overshoot (off-target statement answers beyond the target vs a uniform choice): pooled 121/150 vs 78.33 (+28 [+23, +34] per answer); countries 49/55 vs 30.0 (+35 [+27, +42] per answer); animals 46/62 vs 32.0 (+23 [+13, +32] per answer); body 26/33 vs 16.33 (+29 [+17, +41] per answer)
Shuffled-label direction: pooled 8/26 vs 6.67; countries 2/4 vs 1.0; animals 3/10 vs 3.33; body 3/12 vs 2.33

## The transit sweep: C2's kill test, with "in transit" defined before the test

Lens / random = answers that become bridge alt's answer (memory → prompt: its statement digit; memory → memory: its recalled fact); copy = memory → prompt answers changed by pasting the alt prompt's states. In transit: memory → memory lens upper bound <= 2x the random's upper bound, and copy >= 50%.

### 1x the alt-prompt patch's size (primary)

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**countries**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 2] | 0% [0, 2] | 0% [0, 3] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 2] | 0% [0, 2] | 2% [0, 5] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 44 | 1% [0, 3] | 0% [0, 2] | 13% [9, 18] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 3] | 0% [0, 2] | 43% [35, 52] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 3] | 0% [0, 2] | 31% [24, 38] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**animals**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 2] | 0% [0, 2] | 1% [0, 3] | 1% [0, 3] | 0% [0, 2] | +1 [+0, +2] | False | - |
| 32 | 0% [0, 2] | 0% [0, 2] | 2% [0, 5] | 2% [0, 5] | 0% [0, 2] | +2 [+0, +5] | False | - |
| 36 | 3% [0, 6] | 1% [0, 3] | 12% [4, 20] | 7% [1, 16] | 0% [0, 2] | +7 [+1, +16] | False | - |
| 40 | 1% [0, 4] | 0% [0, 2] | 21% [13, 31] | 6% [1, 14] | 1% [0, 3] | +6 [+1, +13] | False | - |
| 44 | 1% [0, 3] | 0% [0, 2] | 27% [19, 38] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 1% [0, 3] | 0% [0, 2] | 48% [41, 55] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 2] | 0% [0, 2] | 22% [16, 28] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**body**: transit layers [44]; C2 **holds**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 6% [1, 12] | 1% [0, 5] | 0% [0, 3] | 1% [0, 5] | 0% [0, 3] | +1 [+0, +3] | False | - |
| 32 | 11% [2, 22] | 0% [0, 3] | 1% [0, 5] | 6% [1, 13] | 0% [0, 3] | +6 [+1, +13] | False | - |
| 36 | 23% [10, 39] | 0% [0, 3] | 18% [8, 28] | 20% [12, 29] | 1% [0, 5] | +19 [+11, +27] | False | - |
| 40 | 13% [3, 24] | 1% [0, 5] | 42% [26, 57] | 18% [7, 30] | 1% [0, 5] | +18 [+7, +29] | False | - |
| 44 | 3% [0, 8] | 1% [0, 5] | 58% [44, 70] | 0% [0, 3] | 0% [0, 3] | +0 [+0, +0] | True | holds |
| 48 | 1% [0, 5] | 0% [0, 3] | 38% [27, 48] | 0% [0, 3] | 0% [0, 3] | +0 [+0, +0] | False | - |
| 52 | 1% [0, 5] | 0% [0, 3] | 7% [1, 14] | 0% [0, 3] | 0% [0, 3] | +0 [+0, +0] | False | - |

### 4x the alt-prompt patch's size

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**countries**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 36 | 4% [1, 7] | 0% [0, 2] | 0% [0, 3] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 40 | 6% [2, 11] | 0% [0, 2] | 2% [0, 5] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 44 | 2% [0, 5] | 0% [0, 2] | 13% [9, 18] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 3] | 0% [0, 2] | 43% [35, 52] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 2] | 0% [0, 2] | 31% [24, 38] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**animals**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 11% [6, 18] | 0% [0, 2] | 1% [0, 3] | 18% [11, 26] | 0% [0, 2] | +18 [+11, +26] | False | - |
| 32 | 13% [6, 21] | 0% [0, 2] | 2% [0, 5] | 13% [6, 20] | 1% [0, 3] | +12 [+6, +19] | False | - |
| 36 | 14% [8, 20] | 0% [0, 2] | 12% [4, 20] | 2% [0, 6] | 0% [0, 2] | +2 [+0, +6] | False | - |
| 40 | 14% [8, 20] | 0% [0, 2] | 21% [13, 31] | 2% [0, 5] | 0% [0, 2] | +2 [+0, +5] | False | - |
| 44 | 3% [1, 7] | 1% [0, 3] | 27% [19, 38] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 48 | 3% [0, 6] | 0% [0, 2] | 48% [41, 55] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 2] | 0% [0, 2] | 22% [16, 28] | 0% [0, 2] | 0% [0, 2] | +0 [+0, +0] | False | - |

**body**: transit layers [44]; C2 **holds**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 25% [15, 36] | 8% [2, 16] | 0% [0, 3] | 52% [34, 68] | 1% [0, 5] | +52 [+34, +67] | False | - |
| 32 | 27% [11, 44] | 5% [0, 12] | 1% [0, 5] | 10% [3, 17] | 2% [0, 6] | +8 [+3, +14] | False | - |
| 36 | 19% [8, 31] | 7% [2, 13] | 18% [8, 28] | 3% [0, 8] | 1% [0, 5] | +2 [+0, +5] | False | - |
| 40 | 16% [4, 30] | 9% [2, 18] | 42% [26, 57] | 3% [0, 8] | 1% [0, 5] | +2 [+0, +7] | False | - |
| 44 | 9% [2, 19] | 4% [1, 10] | 58% [44, 70] | 1% [0, 5] | 1% [0, 5] | +0 [+0, +0] | True | holds |
| 48 | 4% [1, 10] | 2% [0, 6] | 38% [27, 48] | 0% [0, 3] | 0% [0, 3] | +0 [+0, +0] | False | - |
| 52 | 2% [0, 6] | 0% [0, 3] | 7% [1, 14] | 0% [0, 3] | 0% [0, 3] | +0 [+0, +0] | False | - |

