# pointer_swap / d3_start_or_end_smoke_27b

Checks: {"self_noop": {"n": 8, "same_top": 8, "max_abs_dlogit_max": 0.2734}, "layer0_all_reproduces_source": {"n": 8, "same_top": 8, "max_abs_dlogit_max": 0.3125}, "unedited_base_answer_read": {"n": 8, "base_answer": 8}}

Primary (RL, final, transit window): {"RL|e5fewer|final": "damage", "RL|e5more|final": "damage"}

## Verdicts (dissoc, pooled over domains), per layer / window

- RL|e5fewer|final: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- RL|e5fewer|last: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- DL|e5fewer|final: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- DL|e5fewer|last: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- RL|e5more|final: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- RL|e5more|last: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- DL|e5more|final: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage
- DL|e5more|last: 44: damage, 48: damage, 52: damage, 56: damage, early: damage, mid: damage, transit: damage

## Shares (pooled over domains): role rate [95% CI]

| family | level | group | layer | source | n | none | identity | position | value | context | other |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | e5fewer | final | 44 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 44 | other | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 48 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 48 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 52 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| RL | e5fewer | final | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 52 | other | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 52 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| RL | e5fewer | last | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 52 | other | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | 56 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| RL | e5fewer | final | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | 56 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| RL | e5fewer | last | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | mid | dissoc | 2 | 50% [9,91] | 50% [9,91] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | final | transit | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| RL | e5fewer | final | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5fewer | last | transit | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| RL | e5fewer | last | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 48 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 48 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 52 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5fewer | final | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 52 | other | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 52 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5fewer | last | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 52 | other | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | 56 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| DL | e5fewer | final | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | 56 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| DL | e5fewer | last | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | final | transit | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5fewer | final | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5fewer | last | transit | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5fewer | last | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 44 | other | 2 | 0% [0,66] | 0% [0,66] | 100% [34,100] | 0% [0,66] | - | 0% |
| RL | e5more | last | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 48 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 50% [9,91] | 0% [0,66] | - | 0% |
| RL | e5more | final | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 48 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 52 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 52 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 52 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 52 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | 56 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| RL | e5more | final | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | 56 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| RL | e5more | last | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | transit | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | final | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | transit | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| RL | e5more | last | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 44 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 44 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 44 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 44 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 48 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 48 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 48 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 52 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5more | final | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 52 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 52 | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 52 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 52 | rand | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 52 | other | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | 56 | dissoc | 2 | 50% [9,91] | 0% [0,66] | 0% [0,66] | 50% [9,91] | - | 0% |
| DL | e5more | final | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | 56 | dissoc | 2 | 0% [0,66] | 0% [0,66] | 0% [0,66] | 100% [34,100] | - | 0% |
| DL | e5more | last | 56 | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | early | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | early | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | mid | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | mid | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | final | transit | dissoc | 2 | 0% [0,66] | 0% [0,66] | 50% [9,91] | 50% [9,91] | - | 0% |
| DL | e5more | final | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | transit | dissoc | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
| DL | e5more | last | transit | same | 2 | 100% [34,100] | 0% [0,66] | 0% [0,66] | 0% [0,66] | - | 0% |
