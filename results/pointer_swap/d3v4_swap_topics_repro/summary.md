# pointer_swap / d3v4_swap_topics_repro

Checks: {"self_noop": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 2.75}, "layer0_all_reproduces_source": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 6.6875}, "unedited_base_answer_read": {"n": 2286, "base_answer": 2286}}

Primary (RL, final, transit window): {}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5f0|last: 50: position, early: none, mid: none, transit: value
- DL|e5f0|last: 50: position, early: none, mid: none, transit: none
- RR|e5f0|last: 50: identity, early: none, mid: none, transit: identity

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5f0 | last | 50 | dissoc | 762 | 17% [15,20] | 22% [19,25] | 51% [47,54] | 0% [0,0] | 10% [9,13] | 0% |
| RL | e5f0 | last | 50 | same | 762 | 100% [99,100] | 0% [0,1] | 0% [0,0] | 0% [0,0] | 0% [0,1] | 0% |
| RL | e5f0 | last | 50 | rand | 762 | 100% [99,100] | 0% [0,1] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | 50 | other | 762 | 67% [64,71] | 0% [0,0] | 25% [22,28] | 0% [0,0] | 8% [6,10] | 0% |
| RL | e5f0 | last | early | dissoc | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | early | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | mid | dissoc | 762 | 99% [98,100] | 0% [0,1] | 0% [0,1] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | mid | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RL | e5f0 | last | transit | dissoc | 762 | 25% [22,28] | 5% [4,7] | 26% [23,29] | 42% [39,46] | 1% [1,2] | 0% |
| RL | e5f0 | last | transit | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | 50 | dissoc | 762 | 52% [49,56] | 12% [10,14] | 32% [29,36] | 0% [0,0] | 4% [3,5] | 0% |
| DL | e5f0 | last | 50 | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | 50 | rand | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | 50 | other | 762 | 99% [97,99] | 0% [0,0] | 1% [0,2] | 0% [0,0] | 1% [0,1] | 0% |
| DL | e5f0 | last | early | dissoc | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | early | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | mid | dissoc | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | mid | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| DL | e5f0 | last | transit | dissoc | 762 | 84% [81,87] | 1% [1,2] | 10% [8,12] | 5% [3,6] | 0% [0,1] | 0% |
| DL | e5f0 | last | transit | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | 50 | dissoc | 762 | 19% [16,22] | 81% [78,83] | 1% [0,1] | 0% [0,0] | 0% [0,1] | 0% |
| RR | e5f0 | last | 50 | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | 50 | rand | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | 50 | other | 762 | 83% [80,85] | 0% [0,0] | 0% [0,0] | 0% [0,0] | 8% [7,11] | 9% |
| RR | e5f0 | last | early | dissoc | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | early | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | mid | dissoc | 762 | 78% [75,81] | 21% [19,24] | 0% [0,1] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | mid | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
| RR | e5f0 | last | transit | dissoc | 762 | 7% [6,10] | 92% [90,94] | 0% [0,0] | 0% [0,0] | 0% [0,1] | 0% |
| RR | e5f0 | last | transit | same | 762 | 100% [100,100] | 0% [0,0] | 0% [0,0] | 0% [0,0] | - | 0% |
