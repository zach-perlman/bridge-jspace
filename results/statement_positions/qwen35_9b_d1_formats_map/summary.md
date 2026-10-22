# statement_positions / qwen35_9b_d1_formats_map

Cases: {"tasks": {"tasks_set": "d1_formats_v1", "competence": "qwen35_9b_d1_formats_competence", "scenes": 180, "skipped": {}}}
Sanity: {"identity": {"n": 720, "max_abs_ld_minus_clean": 0.25, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 360, "max_abs_ld_minus_C": 0.375, "top_is_C_top": 1}}
Read vs greedy: {"n": 9280, "agree": 0.9988, "read/greedy": {"A/A": 8610, "b/b": 607, "other/other": 52, "A/b": 7, "b/A": 2, "A/other": 1, "other/b": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"PP": {"bind_bridge": [0, 2, 4, 6, 8, 10, 12, 14], "bridge_word": [0, 2, 4, 6, 8, 10], "context": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18]}, "PM": {"bind_bridge": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18], "bridge_word": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18], "context": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18]}}
Handoff: {"PP": {"last_statement_transit": {"bind_bridge": 14, "bridge_word": 10, "context": 18}, "first_question_transit": null}, "PM": {"last_statement_transit": {"bind_bridge": 18, "bridge_word": 18, "context": 18}, "first_question_transit": null}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 28 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 96* | 96* | 96* | 94* | 66* | 64* | 51* | 50* | 32 | 31 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| bridge_word | 97* | 96* | 96* | 83* | 58* | 54* | 48 | 45 | 32 | 28 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 9 | 6 | 6 | 8 | 2 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 1 | 11 | 12 | 9 | 10 | 8 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 1 |
| context | 100* | 100* | 100* | 100* | 100* | 100* | 97* | 97* | 60* | 59* | 58* | 19 | 21 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 2 |
| question | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 21 | 8 | 4 | 8 | 6 | 6 | 5 | 13 | 12 | 12 | 12 | 12 | 1 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 20 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 4 | 7 | 6 | 7 | 5 | 12 | 12 | 12 | 12 | 14 | 0 |

## PM

| set | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 28 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 98* | 98* | 97* | 97* | 99* | 99* | 98* | 97* | 74* | 74* | 71* | 31 | 31 | 30 | 29 | 0 | 0 | 0 | 0 | 0 | 5 |
| bridge_word | 98* | 98* | 97* | 97* | 99* | 98* | 97* | 95* | 74* | 74* | 71* | 30 | 29 | 29 | 28 | 0 | 0 | 0 | 0 | 0 | 4 |
| bind_other | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_bridge | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| context | 99* | 99* | 99* | 100* | 100* | 99* | 99* | 97* | 66* | 63* | 64* | 26 | 27 | 26 | 27 | 0 | 0 | 0 | 0 | 0 | 5 |
| question | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 24 | 9 | 2 | 8 | 6 | 6 | 3 | 9 | 7 | 7 | 6 | 6 | 0 |
| q_words | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 20 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 9 | 6 | 7 | 3 | 9 | 7 | 7 | 6 | 4 | 1 |

