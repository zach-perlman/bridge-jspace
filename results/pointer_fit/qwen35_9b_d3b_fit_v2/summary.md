# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 21, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 10% [6, 13] (n=410) |
| lens | 0% [0, 1] (n=410) |
| random | 0% [0, 1] (n=410) |
| shuffled | 0% [0, 2] (n=410) |
| rr_slot | 0% [0, 2] (n=150) |
| span_only | 7% [5, 10] (n=410) |
| rest_only | 0% [0, 1] (n=410) |
| held_out_entities | 9% [5, 13] (n=199) |
| seen_entities | 10% [6, 15] (n=211) |
| patch | 12% [9, 15] (n=410) |
| sub4 | 8% [6, 11] (n=410) |

slot - lens +10 [+6, +13] pts; slot - random +10 [+6, +13] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 10% [7, 13] (n=410) | 410 / 84 / 27 |
| lens | 0% [0, 1] (n=410) | 410 / 84 / 27 |
| random | 0% [0, 1] (n=410) | 410 / 84 / 27 |
| shuffled | 0% [0, 2] (n=410) | 410 / 84 / 27 |
| rr_slot | 0% [0, 2] (n=150) | 150 / 63 / 26 |
| slot - lens | +10 [+7, +12] pts | |
| slot - random | +10 [+7, +12] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 2% [0, 6] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 36 / 9 |
| animals | 17% [10, 23] (n=150) | 0% [0, 2] (n=150) | 0% [0, 2] (n=150) | 150 / 33 / 9 |
| body | 10% [4, 18] (n=110) | 0% [0, 3] (n=110) | 0% [0, 3] (n=110) | 110 / 15 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 8% [4, 15] (n=91) | 91 / 27 / 12 |
| template | 10% [6, 15] (n=211) | 211 / 56 / 15 |
| both | 9% [5, 16] (n=108) | 108 / 27 / 15 |
