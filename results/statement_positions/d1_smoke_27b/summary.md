# statement_positions / d1_smoke_27b

Cases: {"suite": {"suite_map": "map_A8_v1", "n": {"BL": 4, "BR": 4, "RL": 4, "RR": 4, "BLR": 4, "BRL": 4}, "unaligned_skipped": {}}, "countries": {"country_map": "map_v1", "n": {"R": 4, "B": 4}, "unaligned_skipped": {}}}
Sanity: {"identity": {"n": 64, "max_abs_ld_minus_clean": 0.25, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 32, "max_abs_ld_minus_C": 0.25, "top_is_C_top": 1}, "noop_statements": {"n": 320, "families": ["R", "RL", "RR"], "max_abs_ld_minus_identity": 0.0, "top_is_clean_top": 1}}
Read vs greedy: {"n": 3478, "agree": 0.9991, "read/greedy": {"A/A": 3186, "b/b": 282, "other/other": 7, "A/b": 2, "b/A": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"BL": {"bind_bridge": [0], "bridge_word": [0], "context": [0, 16, 36, 40]}, "BR": {"bind_bridge": [0, 16, 32], "bridge_word": [0, 16, 32], "context": [0, 16, 32]}, "RL": {"question": [36, 40]}, "BLR": {"bind_bridge": [0], "bridge_word": [0], "context": [0, 16, 32, 36]}, "BRL": {"bind_bridge": [0, 16, 32], "bridge_word": [0, 16, 32], "context": [0, 16]}, "B": {"bind_bridge": [0, 16, 32, 36], "bridge_word": [0, 16, 32, 36], "context": [0, 16, 32, 36], "question": [40]}}
Handoff: {"BL": {"last_statement_transit": {"bind_bridge": 0, "bridge_word": 0, "context": 40}, "first_question_transit": null}, "BR": {"last_statement_transit": {"bind_bridge": 32, "bridge_word": 32, "context": 32}, "first_question_transit": null}, "RL": {"last_statement_transit": {}, "first_question_transit": 36}, "BLR": {"last_statement_transit": {"bind_bridge": 0, "bridge_word": 0, "context": 36}, "first_question_transit": null}, "BRL": {"last_statement_transit": {"bind_bridge": 32, "bridge_word": 32, "context": 16}, "first_question_transit": null}, "B": {"last_statement_transit": {"bind_bridge": 36, "bridge_word": 36, "context": 36}, "first_question_transit": 40}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## BL

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | 100* | 75 | 0 | 0 | 0 | 0 |
| bridge_word | 100* | 75 | 0 | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 100* | 100* | 75 | 100* | 100* | 0 |
| question | 0 | 0 | 50 | 0 | 0 | 0 |
| q_words | 0 | 0 | 50 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## BR

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 25 | 0 | 0 |
| bridge_word | 100* | 100* | 100* | 50 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 100* | 100* | 100* | 75 | 0 | 0 |
| question | 0 | 0 | 0 | 25 | 25 | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## RL

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | 0 |
| lookup_bridge | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | 0 |
| context | . | . | . | . | . | 0 |
| question | 0 | 0 | 25 | 100* | 100* | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## RR

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | 0 |
| lookup_bridge | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | 0 |
| context | . | . | . | . | . | 0 |
| question | 0 | 0 | 0 | 0 | 25 | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## BLR

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | 100* | 75 | 0 | 0 | 0 | 0 |
| bridge_word | 100* | 75 | 0 | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 25 | 25 | 25 | 0 |
| lookup_x | 0 | 0 | 25 | 0 | 0 | 0 |
| context | 100* | 100* | 100* | 100* | 75 | 0 |
| question | 0 | 0 | 25 | 25 | 50 | 0 |
| q_words | 0 | 0 | 25 | 25 | 50 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## BRL

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 50 | 0 | 0 |
| bridge_word | 100* | 100* | 100* | 50 | 0 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 25 | 0 | 0 | 0 |
| context | 100* | 100* | 75 | 75 | 50 | 0 |
| question | 0 | 0 | 0 | 0 | 75 | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## R

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | . | . | . | . | . | 0 |
| bridge_word | . | . | . | . | . | 0 |
| bind_other | . | . | . | . | . | 0 |
| context | . | . | . | . | . | 0 |
| question | 0 | 0 | 0 | 75 | 75 | 0 |
| q_words | 0 | 0 | 0 | 0 | 25 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

## B

| set | 0 | 16 | 32 | 36 | 40 | max control |
|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 100* | 75 | 0 |
| bridge_word | 100* | 100* | 100* | 100* | 75 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 100* | 100* | 100* | 100* | 50 | 0 |
| question | 0 | 0 | 0 | 0 | 100* | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 |

