# pointer_fit

Verdict: **not shown: the slot direction does not steer the lookup by the rule**

Checks: {"a_lower_bound_ge_0.30": false, "b_20_points_above_lens_and_random": false, "controls_valid": true, "illusion_flag": false, "unedited_answer_org": 1}

Primary cell (memory → prompt, layer 18, 1x): % answers that become the answer at slot j

| condition | rate |
|---|---|
| slot | 2% [1, 5] (n=257) |
| lens | 0% [0, 1] (n=257) |
| random | 0% [0, 1] (n=257) |
| shuffled | 0% [0, 1] (n=257) |
| rr_slot | 0% [0, 5] (n=77) |
| span_only | 2% [1, 5] (n=257) |
| rest_only | 0% [0, 1] (n=257) |
| held_out_entities | 2% [0, 6] (n=119) |
| seen_entities | 3% [1, 7] (n=138) |
| patch | 1% [0, 3] (n=257) |
| sub4 | 2% [1, 4] (n=257) |

slot - lens +2 [+1, +4] pts; slot - random +2 [+1, +4] pts

Intervals above: entity-cluster bootstrap (asked entity within each topic), widened to Wilson where wider. Item level and n items / k entities / t wordings:

| condition | item level | n / k / t |
|---|---|---|
| slot | 2% [1, 5] (n=257) | 257 / 71 / 27 |
| lens | 0% [0, 1] (n=257) | 257 / 71 / 27 |
| random | 0% [0, 1] (n=257) | 257 / 71 / 27 |
| shuffled | 0% [0, 1] (n=257) | 257 / 71 / 27 |
| rr_slot | 0% [0, 5] (n=77) | 77 / 32 / 18 |
| slot - lens | +2 [+1, +4] pts | |
| slot - random | +2 [+1, +4] pts | |

| topic | slot | lens | random | n / k / t |
|---|---|---|---|---|
| countries | 1% [0, 5] (n=136) | 0% [0, 3] (n=136) | 0% [0, 3] (n=136) | 136 / 32 / 9 |
| animals | 2% [0, 8] (n=84) | 0% [0, 4] (n=84) | 0% [0, 4] (n=84) | 84 / 30 / 9 |
| body | 5% [0, 18] (n=37) | 0% [0, 9] (n=37) | 0% [0, 9] (n=37) | 37 / 9 / 9 |

| held out of the fit | slot | n / k / t |
|---|---|---|
| entity | 2% [0, 10] (n=52) | 52 / 21 / 12 |
| template | 3% [1, 7] (n=138) | 138 / 47 / 15 |
| both | 1% [0, 8] (n=67) | 67 / 23 / 14 |
