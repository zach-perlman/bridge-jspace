# The split by sentence order (descriptive, after the data)

J++ extra loss per reader and the gap (recall minus lookup, paired resamples) at the layer fixed in advance, by where the original bridge's locker sentence sits relative to the asked pick. Fresh scenes are the README's matched scenes (both locker sentences before the pick by construction). The pre-registered numbers are the main test's 'all' rows. Cluster bootstrap over bridge entities (10000 resamples, seed 0). Lookup switch: the share of lookups the whole change switches (the lookup's extra loss is a share of those switches, so it is measurable only where they are many). UNVERIFIED.

| model | design | locker vs pick | n | lookup switch | lookup extra loss | recall extra loss | gap |
|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | two people swap | all | 200 | 0.45 | 0.03 [-0.01, 0.08] | 0.34 [0.25, 0.44] | 0.31 [0.20, 0.42] |
| nemotron-3.5-lightning | two people swap | before | 85 | 0.86 | 0.01 [-0.03, 0.07] | 0.12 [0.04, 0.20] | 0.10 [0.02, 0.20] |
| nemotron-3.5-lightning | two people swap | after | 115 | 0.15 | 0.12 [0.00, 0.29] | 0.53 [0.40, 0.65] | 0.41 [0.15, 0.63] |
