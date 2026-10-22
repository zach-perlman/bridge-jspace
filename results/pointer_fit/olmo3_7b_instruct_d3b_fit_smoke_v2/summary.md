# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule (controls failed: not interpretable)**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": false, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 18, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 0% [0, 24] (n=12) |
| lens | 0% [0, 24] (n=12) |
| random | 0% [0, 24] (n=12) |
| shuffled | 0% [0, 24] (n=12) |
| rr_slot | 0% [0, 24] (n=12) |
| span_only | 0% [0, 24] (n=12) |
| rest_only | 0% [0, 24] (n=12) |
| held_out_entities | 0% [-0, 43] (n=5) |
| seen_entities | 0% [0, 35] (n=7) |
| patch | 8% [1, 35] (n=12) |
| sub4 | 0% [0, 24] (n=12) |

slot - lens +0 [+0, +0] pts; slot - random +0 [+0, +0] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 0% [0, 24] (n=12) | 12 / 11 / 10 |
| lens | 0% [0, 24] (n=12) | 12 / 11 / 10 |
| random | 0% [0, 24] (n=12) | 12 / 11 / 10 |
| shuffled | 0% [0, 24] (n=12) | 12 / 11 / 10 |
| rr_slot | 0% [0, 24] (n=12) | 12 / 9 / 10 |
| slot - lens | +0 [+0, +0] pts | |
| slot - random | +0 [+0, +0] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 3 / 2 |
| animals | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 4 |
| body | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 4 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | nan% [nan, nan] (n=0) | 0 / 0 / 0 |
| template | 0% [0, 35] (n=7) | 7 / 6 / 6 |
| both | 0% [-0, 43] (n=5) | 5 / 5 / 5 |
