# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule (controls failed: not interpretable)**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": false, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 50, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 0% [0, 24] (n=12) |
| lens | 0% [0, 24] (n=12) |
| random | 0% [0, 24] (n=12) |
| shuffled | 0% [0, 24] (n=12) |
| rr_slot | 0% [-0, 28] (n=10) |
| span_only | 0% [0, 24] (n=12) |
| rest_only | 0% [0, 24] (n=12) |
| held_out_entities | 0% [0, 39] (n=6) |
| seen_entities | 0% [0, 39] (n=6) |
| patch | 0% [0, 24] (n=12) |
| sub4 | 0% [0, 24] (n=12) |

slot - lens +0 [+0, +0] pts; slot - random +0 [+0, +0] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 0% [0, 24] (n=12) | 12 / 12 / 9 |
| lens | 0% [0, 24] (n=12) | 12 / 12 / 9 |
| random | 0% [0, 24] (n=12) | 12 / 12 / 9 |
| shuffled | 0% [0, 24] (n=12) | 12 / 12 / 9 |
| rr_slot | 0% [-0, 28] (n=10) | 10 / 9 / 8 |
| slot - lens | +0 [+0, +0] pts | |
| slot - random | +0 [+0, +0] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 3 |
| animals | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 2 |
| body | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 4 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 0% [0, 66] (n=2) | 2 / 2 / 2 |
| template | 0% [0, 39] (n=6) | 6 / 6 / 5 |
| both | 0% [0, 49] (n=4) | 4 / 4 / 3 |
