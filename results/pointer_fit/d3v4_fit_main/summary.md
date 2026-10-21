# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": true, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 48, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 31% [27, 36] (n=420) |
| lens | 0% [0, 1] (n=420) |
| random | 0% [0, 1] (n=420) |
| shuffled | 0% [0, 1] (n=420) |
| rr_slot | 1% [0, 4] (n=150) |
| span_only | 12% [9, 16] (n=420) |
| rest_only | 6% [4, 9] (n=420) |
| held_out_entities | 31% [25, 37] (n=203) |
| seen_entities | 31% [24, 39] (n=217) |
| patch | 26% [22, 31] (n=420) |
| sub4 | 26% [22, 31] (n=420) |

slot - lens +31 [+27, +35] pts; slot - random +31 [+27, +35] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 31% [27, 36] (n=420) | 420 / 85 / 27 |
| lens | 0% [0, 1] (n=420) | 420 / 85 / 27 |
| random | 0% [0, 1] (n=420) | 420 / 85 / 27 |
| shuffled | 0% [0, 1] (n=420) | 420 / 85 / 27 |
| rr_slot | 1% [0, 4] (n=150) | 150 / 66 / 26 |
| slot - lens | +31 [+26, +35] pts | |
| slot - random | +31 [+26, +35] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 29% [22, 37] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 36 / 9 |
| animals | 36% [29, 44] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 34 / 9 |
| body | 27% [18, 36] (n=120) | 0% [-0, 3] (n=120) | 0% [-0, 3] (n=120) | 120 / 15 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 28% [19, 38] (n=89) | 89 / 27 / 12 |
| template | 31% [24, 39] (n=217) | 217 / 57 / 15 |
| both | 32% [25, 42] (n=114) | 114 / 28 / 15 |
