# pointer_fair (pointer_v4)

Intervals: entity-cluster bootstrap 95% (asked entity within its topic), widened to Wilson where wider; 'item level': Wilson alone. n items / k entities / t wordings.

Unedited answers = answer org: memory → prompt 100% [76, 100] (n=12); memory → memory 100% [76, 100] (n=12)

## memory → prompt, after the cue, layers 32-40 at once, 1x: **not shown: 0 of 3 topics pass with valid controls (needs 2)**

Flags: {"pointer_at_lens_depth": false, "pointer_later_only": false, "not_lookup_specific": false}

| topic | pointer | item level | lens | random | shuffled | memory → memory changed (pointer) | pointer − lens | pointer − random | pointer 2x | lens 2x | passes / valid | n / k / t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| countries | 75% [25, 100] | 75% [30, 95] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] (n=4) | +75 [+25, +100] | +75 [+25, +100] | 75% [25, 100] | 0% [0, 49] | False / False | 4 / 4 / 3 |
| animals | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] (n=4) | +0 [+0, +0] | +0 [+0, +0] | 0% [0, 49] | 0% [0, 49] | False / False | 4 / 4 / 3 |
| body | 25% [0, 75] | 25% [5, 70] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] (n=4) | -25 [-75, +0] | +25 [+0, +75] | 25% [0, 75] | 0% [0, 49] | False / False | 4 / 4 / 2 |
| pooled | 33% [14, 61] | 33% [14, 61] | 17% [0, 45] | 0% [0, 24] | 0% [0, 24] | 0% [0, 24] (n=12) | +17 [-8, +33] | +33 [+17, +50] | 33% [14, 61] | 0% [0, 24] | False / False | 12 / 12 / 8 |

| held out of the fit | pointer | lens | n / k / t |
|---|---|---|---|
| asked entity held out | 33% [6, 79] | 0% [0, 56] | 3 / 3 / 2 |
| wording held out | 17% [0, 56] | 17% [0, 56] | 6 / 6 / 4 |
| both held out | 67% [21, 94] | 33% [6, 79] | 3 / 3 / 3 |

Overshoot (off-target statement answers beyond the target vs a uniform choice): pooled 3/3 vs 2.0 (+33 [+33, +33] per answer); countries 1/1 vs 0.67 (+33 [+33, +33] per answer); animals 1/1 vs 0.33 (+67 [+67, +67] per answer); body 1/1 vs 1.0 (+0 [+0, +0] per answer)
Shuffled-label direction: pooled 0/0 vs 0.0; countries 0/0 vs 0.0; animals 0/0 vs 0.0; body 0/0 vs 0.0

## memory → prompt, question words (reported, not decisive), layers 32-40 at once, 1x: **not shown: 0 of 3 topics pass with valid controls (needs 2)**

Flags: {"pointer_at_lens_depth": false, "pointer_later_only": false, "not_lookup_specific": true}

| topic | pointer | item level | lens | random | shuffled | memory → memory changed (pointer) | pointer − lens | pointer − random | pointer 2x | lens 2x | passes / valid | n / k / t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| countries | 75% [25, 100] | 75% [30, 95] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] (n=4) | +75 [+25, +100] | +75 [+25, +100] | 75% [25, 100] | 0% [0, 49] | False / False | 4 / 4 / 3 |
| animals | 25% [0, 75] | 25% [5, 70] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | 25% [0, 70] (n=4) | +0 [-75, +75] | +25 [+0, +75] | 25% [0, 75] | 50% [0, 100] | False / False | 4 / 4 / 3 |
| body | 25% [0, 75] | 25% [5, 70] | 75% [25, 100] | 0% [0, 49] | 25% [0, 75] | 50% [0, 100] (n=4) | -50 [-100, +0] | +25 [+0, +75] | 25% [0, 75] | 100% [51, 100] | False / False | 4 / 4 / 2 |
| pooled | 42% [17, 68] | 42% [19, 68] | 33% [14, 61] | 0% [0, 24] | 8% [0, 35] | 33% [10, 61] (n=12) | +8 [-25, +42] | +42 [+17, +67] | 42% [17, 68] | 50% [25, 75] | False / False | 12 / 12 / 8 |

| held out of the fit | pointer | lens | n / k / t |
|---|---|---|---|
| asked entity held out | 67% [21, 100] | 0% [0, 56] | 3 / 3 / 2 |
| wording held out | 17% [0, 56] | 33% [0, 70] | 6 / 6 / 4 |
| both held out | 67% [21, 94] | 67% [21, 94] | 3 / 3 / 3 |

Overshoot (off-target statement answers beyond the target vs a uniform choice): pooled 2/2 vs 1.67 (+17 [+17, +17] per answer); countries 1/1 vs 0.67 (+33 [+33, +33] per answer); animals 0/0 vs 0.0 (- per answer); body 1/1 vs 1.0 (+0 [+0, +0] per answer)
Shuffled-label direction: pooled 0/0 vs 0.0; countries 0/0 vs 0.0; animals 0/0 vs 0.0; body 0/0 vs 0.0

## The transit sweep: C2's kill test, with "in transit" defined before the test

Lens / random = answers that become bridge alt's answer (memory → prompt: its statement digit; memory → memory: its recalled fact); copy = memory → prompt answers changed by pasting the alt prompt's states. In transit: memory → memory lens upper bound <= 2x the random's upper bound, and copy >= 50%.

### 1x the alt-prompt patch's size (primary)

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**countries**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

**animals**: transit layers [48]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 75% [25, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

**body**: transit layers [44, 48]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | +25 [+0, +75] | False | - |
| 40 | 25% [0, 100] | 0% [0, 49] | 75% [25, 100] | 50% [0, 100] | 0% [0, 49] | +50 [+0, +100] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 75% [25, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 48 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

### 4x the alt-prompt patch's size

Flags: {"c2_transit": false, "no_transit": true, "c2_killed": false}

**countries**: transit layers none; C2 **not testable**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 52 | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

**animals**: transit layers [48]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 25% [0, 70] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 32 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 36 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 25% [0, 70] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 48 | 0% [0, 49] | 0% [0, 49] | 75% [25, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

**body**: transit layers [44, 48]; C2 **undecided**

| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |
|---|---|---|---|---|---|---|---|---|
| 28 | 25% [0, 100] | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | +50 [+0, +100] | False | - |
| 32 | 25% [0, 100] | 0% [0, 49] | 0% [0, 49] | 25% [0, 75] | 0% [0, 49] | +25 [+0, +75] | False | - |
| 36 | 25% [0, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 40 | 25% [0, 100] | 0% [0, 49] | 75% [25, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |
| 44 | 0% [0, 49] | 0% [0, 49] | 75% [25, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 48 | 0% [0, 49] | 0% [0, 49] | 50% [0, 100] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | True | unclear |
| 52 | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | +0 [+0, +0] | False | - |

