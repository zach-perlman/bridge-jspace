# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 0.9881}

Primary cell (memory → prompt, layer 50, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 1% [0, 3] (n=377) |
| lens | 0% [0, 1] (n=377) |
| random | 0% [0, 1] (n=377) |
| shuffled | 0% [0, 1] (n=377) |
| rr_slot | 0% [0, 3] (n=127) |
| span_only | 1% [0, 3] (n=377) |
| rest_only | 0% [0, 1] (n=377) |
| held_out_entities | 1% [0, 4] (n=164) |
| seen_entities | 1% [0, 4] (n=213) |
| patch | 1% [0, 2] (n=377) |
| sub4 | 1% [1, 3] (n=377) |

slot - lens +1 [+0, +2] pts; slot - random +1 [+0, +2] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 1% [1, 3] (n=377) | 377 / 83 / 27 |
| lens | 0% [0, 1] (n=377) | 377 / 83 / 27 |
| random | 0% [0, 1] (n=377) | 377 / 83 / 27 |
| shuffled | 0% [0, 1] (n=377) | 377 / 83 / 27 |
| rr_slot | 0% [0, 3] (n=127) | 127 / 50 / 24 |
| slot - lens | +1 [+0, +3] pts | |
| slot - random | +1 [+0, +3] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 1% [0, 5] (n=139) | 0% [-0, 3] (n=139) | 0% [-0, 3] (n=139) | 139 / 35 / 9 |
| animals | 1% [0, 4] (n=133) | 0% [-0, 3] (n=133) | 0% [-0, 3] (n=133) | 133 / 33 / 9 |
| body | 2% [0, 7] (n=105) | 0% [0, 4] (n=105) | 0% [0, 4] (n=105) | 105 / 15 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 0% [0, 5] (n=72) | 72 / 25 / 12 |
| template | 1% [0, 4] (n=213) | 213 / 57 / 15 |
| both | 2% [0, 8] (n=92) | 92 / 26 / 15 |
