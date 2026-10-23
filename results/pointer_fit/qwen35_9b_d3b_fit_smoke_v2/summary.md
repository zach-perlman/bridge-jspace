# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule (controls failed: not interpretable)**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": false, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 21, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 17% [0, 45] (n=12) |
| lens | 0% [0, 24] (n=12) |
| random | 0% [0, 24] (n=12) |
| shuffled | 0% [0, 24] (n=12) |
| rr_slot | 0% [0, 24] (n=12) |
| span_only | 17% [0, 45] (n=12) |
| rest_only | 0% [0, 24] (n=12) |
| held_out_entities | 0% [0, 32] (n=8) |
| seen_entities | 50% [15, 85] (n=4) |
| patch | 8% [1, 35] (n=12) |
| sub4 | 17% [5, 45] (n=12) |

slot - lens +17 [+0, +40] pts; slot - random +17 [+0, +40] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 17% [5, 45] (n=12) | 12 / 10 / 11 |
| lens | 0% [0, 24] (n=12) | 12 / 10 / 11 |
| random | 0% [0, 24] (n=12) | 12 / 10 / 11 |
| shuffled | 0% [0, 24] (n=12) | 12 / 10 / 11 |
| rr_slot | 0% [0, 24] (n=12) | 12 / 10 / 9 |
| slot - lens | +17 [+0, +42] pts | |
| slot - random | +17 [+0, +42] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 3 / 3 |
| animals | 25% [0, 75] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 4 |
| body | 25% [0, 100] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 3 / 4 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 0% [0, 66] (n=2) | 2 / 2 / 2 |
| template | 50% [15, 85] (n=4) | 4 / 4 / 4 |
| both | 0% [0, 39] (n=6) | 6 / 5 / 6 |
