# statement_positions / d1_map_n80_v1

Cases: {"suite": {"suite_map": "map_A8_v1", "n": {"BL": 80, "BR": 80, "RL": 80, "RR": 80, "BLR": 80, "BRL": 80}, "unaligned_skipped": {}}, "countries": {"country_map": "map_v1", "n": {"R": 80, "B": 80}, "unaligned_skipped": {}}}
Sanity: {"identity": {"n": 1280, "max_abs_ld_minus_clean": 0.5, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 640, "max_abs_ld_minus_C": 2.0, "top_is_C_top": 1}, "noop_statements": {"n": 640, "families": ["R", "RL", "RR"], "max_abs_ld_minus_identity": 0.0, "top_is_clean_top": 1}}
Read vs greedy: {"n": 13000, "agree": 0.9993, "read/greedy": {"A/A": 12135, "b/b": 838, "other/other": 18, "A/b": 6, "b/A": 3}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"BL": {"context": [32, 34, 36, 38, 40, 44], "question": [52], "final": [52]}, "BR": {"bind_bridge": [32, 34, 36, 38], "bridge_word": [32, 34, 36, 38], "context": [32, 34, 36, 38]}, "RL": {"question": [36, 38, 40, 44, 48, 52], "final": [48, 52]}, "BLR": {"context": [32, 34, 38]}, "BRL": {"context": [32, 34]}, "R": {"question": [36, 38, 40, 44, 48, 52], "final": [48, 52]}, "B": {"bind_bridge": [32, 34, 36, 38], "bridge_word": [32, 34, 36, 38], "context": [32, 34, 36, 38], "question": [40, 44, 48, 52], "final": [48, 52]}}
Handoff: {"BL": {"last_statement_transit": {"context": 44}, "first_question_transit": 52}, "BR": {"last_statement_transit": {"bind_bridge": 38, "bridge_word": 38, "context": 38}, "first_question_transit": null}, "RL": {"last_statement_transit": {}, "first_question_transit": 36}, "BLR": {"last_statement_transit": {"context": 38}, "first_question_transit": null}, "BRL": {"last_statement_transit": {"context": 34}, "first_question_transit": null}, "R": {"last_statement_transit": {}, "first_question_transit": 36}, "B": {"last_statement_transit": {"bind_bridge": 38, "bridge_word": 38, "context": 38}, "first_question_transit": 40}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## BL

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| bridge_word | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 4 | 2 | 11 | 11 | 12 | 8 | 4 | 0 | 0 |
| lookup_x | 8 | 11 | 1 | 2 | 0 | 2 | 0 | 0 | 0 |
| context | 90* | 94* | 86* | 86* | 84* | 79* | 39 | 0 | 0 |
| question | 14 | 4 | 6 | 6 | 11 | 18 | 39 | 86* | 0 |
| q_words | 12 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 78* | 0 |

## BR

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 98* | 94* | 50* | 50* | 1 | 1 | 0 | 0 | 0 |
| bridge_word | 98* | 94* | 50* | 50* | 1 | 1 | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 95* | 95* | 60* | 56* | 2 | 0 | 0 | 0 | 0 |
| question | 4 | 2 | 19 | 19 | 31 | 22 | 22 | 21 | 0 |
| q_words | 1 | 1 | 4 | 4 | 6 | 1 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 1 | 4 | 2 | 12 | 10 | 0 |

## RL

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | . | . | . | 0 |
| lookup_bridge | . | . | . | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | . | . | . | 0 |
| context | . | . | . | . | . | . | . | . | 0 |
| question | 24 | 41 | 57* | 64* | 69* | 98* | 100* | 100* | 0 |
| q_words | 5 | 1 | 1 | 1 | 4 | 9 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 1 | 4 | 68* | 96* | 0 |

## RR

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | . | . | . | 0 |
| lookup_bridge | . | . | . | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | . | . | . | 0 |
| context | . | . | . | . | . | . | . | . | 0 |
| question | 1 | 8 | 9 | 15 | 12 | 14 | 25 | 19 | 0 |
| q_words | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## BLR

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| bridge_word | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 15 | 20 | 6 | 8 | 4 | 0 | 0 | 0 | 1 |
| lookup_x | 10 | 9 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| context | 78* | 79* | 49 | 50* | 24 | 6 | 1 | 0 | 0 |
| question | 15 | 8 | 19 | 19 | 28 | 26 | 26 | 16 | 0 |
| q_words | 14 | 8 | 15 | 14 | 18 | 9 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 1 | 6 | 16 | 10 | 1 |

## BRL

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 41 | 35 | 18 | 16 | 2 | 0 | 0 | 0 | 2 |
| bridge_word | 36 | 32 | 15 | 14 | 2 | 0 | 0 | 0 | 1 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_bridge | 4 | 4 | 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| lookup_x | 5 | 8 | 2 | 4 | 2 | 5 | 0 | 0 | 0 |
| context | 65* | 66* | 24 | 22 | 11 | 9 | 1 | 0 | 2 |
| question | 32 | 9 | 24 | 18 | 38 | 39 | 40 | 14 | 0 |
| q_words | 29 | 5 | 9 | 5 | 5 | 1 | 0 | 0 | 0 |
| final | 1 | 1 | 2 | 2 | 2 | 15 | 34 | 10 | 0 |

## R

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | . | . | . | 0 |
| context | . | . | . | . | . | . | . | . | 0 |
| question | 1 | 36 | 62* | 80* | 94* | 99* | 100* | 100* | 0 |
| q_words | 1 | 2 | 8 | 19 | 28 | 11 | 1 | 1 | 0 |
| final | 1 | 1 | 1 | 1 | 1 | 8 | 71* | 100* | 0 |

## B

| set | 32 | 34 | 36 | 38 | 40 | 44 | 48 | 52 | max control |
|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 100* | 45 | 40 | 38 | 9 | 0 |
| bridge_word | 100* | 100* | 100* | 100* | 45 | 42 | 38 | 9 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 100* | 100* | 85* | 85* | 18 | 11 | 9 | 2 | 0 |
| question | 0 | 0 | 12 | 12 | 82* | 89* | 91* | 100* | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 10 | 21 | 55* | 96* | 0 |

