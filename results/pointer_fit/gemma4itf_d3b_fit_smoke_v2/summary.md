# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule (controls failed: not interpretable)**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": false, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 40, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 10% [0, 40] (n=10) |
| lens | 0% [-0, 28] (n=10) |
| random | 0% [-0, 28] (n=10) |
| shuffled | 0% [-0, 28] (n=10) |
| rr_slot | 0% [0, 30] (n=9) |
| span_only | 10% [0, 40] (n=10) |
| rest_only | 0% [-0, 28] (n=10) |
| held_out_entities | 0% [0, 49] (n=4) |
| seen_entities | 17% [0, 56] (n=6) |
| patch | 20% [6, 51] (n=10) |
| sub4 | 10% [2, 40] (n=10) |

slot - lens +10 [+0, +30] pts; slot - random +10 [+0, +30] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 10% [2, 40] (n=10) | 10 / 10 / 10 |
| lens | 0% [-0, 28] (n=10) | 10 / 10 / 10 |
| random | 0% [-0, 28] (n=10) | 10 / 10 / 10 |
| shuffled | 0% [-0, 28] (n=10) | 10 / 10 / 10 |
| rr_slot | 0% [0, 30] (n=9) | 9 / 8 / 7 |
| slot - lens | +10 [+0, +30] pts | |
| slot - random | +10 [+0, +30] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 0% [0, 49] (n=4) | 4 / 4 / 4 |
| animals | 0% [0, 56] (n=3) | 0% [0, 56] (n=3) | 0% [0, 56] (n=3) | 3 / 3 / 3 |
| body | 33% [0, 100] (n=3) | 0% [0, 56] (n=3) | 0% [0, 56] (n=3) | 3 / 3 / 3 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 0% [0, 56] (n=3) | 3 / 3 / 3 |
| template | 17% [0, 56] (n=6) | 6 / 6 / 6 |
| both | 0% [0, 79] (n=1) | 1 / 1 / 1 |
