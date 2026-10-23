# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 38, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 13% [10, 16] (n=418) |
| lens | 0% [-0, 1] (n=418) |
| random | 0% [-0, 1] (n=418) |
| shuffled | 0% [-0, 1] (n=418) |
| rr_slot | 1% [0, 4] (n=150) |
| span_only | 6% [4, 9] (n=418) |
| rest_only | 1% [0, 2] (n=418) |
| held_out_entities | 13% [9, 18] (n=209) |
| seen_entities | 12% [8, 18] (n=209) |
| patch | 2% [1, 3] (n=418) |
| sub4 | 11% [8, 14] (n=418) |

slot - lens +13 [+10, +16] pts; slot - random +13 [+10, +16] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 13% [10, 16] (n=418) | 418 / 84 / 27 |
| lens | 0% [-0, 1] (n=418) | 418 / 84 / 27 |
| random | 0% [-0, 1] (n=418) | 418 / 84 / 27 |
| shuffled | 0% [-0, 1] (n=418) | 418 / 84 / 27 |
| rr_slot | 1% [0, 4] (n=150) | 150 / 66 / 26 |
| slot - lens | +13 [+10, +16] pts | |
| slot - random | +13 [+10, +16] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 9% [5, 15] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 36 / 9 |
| animals | 20% [14, 27] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 33 / 9 |
| body | 8% [4, 14] (n=118) | 0% [0, 3] (n=118) | 0% [0, 3] (n=118) | 118 / 15 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 13% [6, 21] (n=94) | 94 / 28 / 12 |
| template | 12% [8, 18] (n=209) | 209 / 56 / 15 |
| both | 13% [8, 20] (n=115) | 115 / 28 / 15 |
