# statement_positions / qwen35_9b_d1_topics2_map

Cases: {"tasks": {"tasks_set": "d1_topics_v2", "competence": "qwen35_9b_d1_topics2_competence", "scenes": 180, "skipped": {}}}
Sanity: {"identity": {"n": 720, "max_abs_ld_minus_clean": 0.375, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 360, "max_abs_ld_minus_C": 0.25, "top_is_C_top": 0.9972222222222222}}
Read vs greedy: {"n": 9600, "agree": 0.9982, "read/greedy": {"A/A": 8816, "b/b": 646, "other/other": 121, "b/A": 5, "other/A": 5, "A/b": 4, "A/other": 2, "b/other": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"PP": {"bind_bridge": [0, 2, 4, 6, 8, 10], "bridge_word": [0, 2, 4, 6, 8, 10], "context": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18]}, "PM": {"bind_bridge": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18], "bridge_word": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18], "context": [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18]}}
Handoff: {"PP": {"last_statement_transit": {"bind_bridge": 10, "bridge_word": 10, "context": 18}, "first_question_transit": null}, "PM": {"last_statement_transit": {"bind_bridge": 18, "bridge_word": 18, "context": 18}, "first_question_transit": null}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 28 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 99* | 94* | 89* | 78* | 57* | 56* | 46 | 47 | 19 | 11 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| bridge_word | 99* | 92* | 89* | 74* | 55* | 52* | 47 | 38 | 17 | 8 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| bind_other | 1 | 3 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_bridge | 0 | 1 | 1 | 1 | 5 | 6 | 8 | 8 | 11 | 11 | 11 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 0 | 1 |
| lookup_x | 0 | 0 | 1 | 2 | 5 | 4 | 16 | 12 | 8 | 7 | 8 | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 1 |
| context | 100* | 100* | 100* | 100* | 100* | 99* | 97* | 97* | 56* | 55* | 54* | 14 | 15 | 15 | 15 | 1 | 1 | 1 | 1 | 0 | 3 |
| question | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 37 | 17 | 12 | 28 | 27 | 31 | 24 | 36 | 32 | 32 | 31 | 28 | 1 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 27 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 4 | 9 | 27 | 28 | 28 | 23 | 35 | 33 | 30 | 29 | 28 | 0 |

## PM

| set | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 28 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 98* | 97* | 97* | 98* | 98* | 99* | 99* | 99* | 64* | 62* | 58* | 30 | 28 | 29 | 26 | 0 | 0 | 0 | 0 | 0 | 1 |
| bridge_word | 97* | 98* | 98* | 97* | 98* | 97* | 99* | 94* | 62* | 61* | 58* | 29 | 29 | 29 | 26 | 0 | 0 | 0 | 0 | 0 | 1 |
| bind_other | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_x | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| context | 100* | 100* | 100* | 100* | 100* | 100* | 99* | 99* | 64* | 62* | 62* | 31 | 30 | 30 | 29 | 0 | 0 | 0 | 0 | 0 | 2 |
| question | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 29 | 13 | 3 | 6 | 3 | 3 | 3 | 7 | 6 | 6 | 6 | 6 | 1 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 26 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 6 | 4 | 4 | 2 | 7 | 6 | 6 | 6 | 7 | 1 |

