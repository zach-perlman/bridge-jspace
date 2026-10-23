# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": true, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 40, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 24% [20, 30] (n=327) |
| lens | 0% [0, 1] (n=327) |
| random | 0% [0, 1] (n=327) |
| shuffled | 0% [0, 1] (n=327) |
| rr_slot | 0% [-0, 3] (n=124) |
| span_only | 20% [16, 26] (n=327) |
| rest_only | 0% [0, 1] (n=327) |
| held_out_entities | 23% [17, 30] (n=159) |
| seen_entities | 26% [19, 34] (n=168) |
| patch | 31% [26, 36] (n=327) |
| sub4 | 25% [21, 30] (n=327) |

slot - lens +24 [+20, +30] pts; slot - random +24 [+20, +30] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 24% [20, 29] (n=327) | 327 / 75 / 27 |
| lens | 0% [0, 1] (n=327) | 327 / 75 / 27 |
| random | 0% [0, 1] (n=327) | 327 / 75 / 27 |
| shuffled | 0% [0, 1] (n=327) | 327 / 75 / 27 |
| rr_slot | 0% [-0, 3] (n=124) | 124 / 59 / 26 |
| slot - lens | +24 [+20, +29] pts | |
| slot - random | +24 [+20, +29] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 26% [18, 34] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 35 / 9 |
| animals | 22% [15, 31] (n=92) | 0% [-0, 4] (n=92) | 0% [-0, 4] (n=92) | 92 / 27 / 9 |
| body | 25% [13, 40] (n=85) | 0% [0, 4] (n=85) | 0% [0, 4] (n=85) | 85 / 13 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 20% [10, 30] (n=71) | 71 / 22 / 12 |
| template | 26% [19, 34] (n=168) | 168 / 51 / 15 |
| both | 25% [16, 35] (n=88) | 88 / 24 / 15 |
