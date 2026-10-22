# statement_positions / olmo3_7b_instruct_d1_topics2_map

Cases: {"tasks": {"tasks_set": "d1_topics_v2", "competence": "olmo3_7b_instruct_d1_topics2_competence", "scenes": 116, "skipped": {}}}
Sanity: {"identity": {"n": 464, "max_abs_ld_minus_clean": 0.4380000000000006, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 0.9956896551724138}, "all0": {"n": 232, "max_abs_ld_minus_C": 1.625, "top_is_C_top": 1}}
Read vs greedy: {"n": 8648, "agree": 0.9916, "read/greedy": {"A/A": 8009, "b/b": 342, "other/other": 224, "A/other": 42, "other/A": 30, "b/A": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"PP": {"bind_bridge": [0, 3, 6, 9], "bridge_word": [0, 3, 6], "context": [0, 3, 6, 9, 12]}, "PM": {"bind_bridge": [0, 3, 6, 9, 12, 15], "bridge_word": [0, 3, 6, 9, 12, 15], "context": [0, 3, 6, 9, 12, 15]}}
Handoff: {"PP": {"last_statement_transit": {"bind_bridge": 9, "bridge_word": 6, "context": 12}, "first_question_transit": null}, "PM": {"last_statement_transit": {"bind_bridge": 15, "bridge_word": 15, "context": 15}, "first_question_transit": null}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 0 | 3 | 6 | 9 | 12 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 98* | 84* | 66* | 50* | 37 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| bridge_word | 97* | 84* | 53* | 41 | 34 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| bind_other | 4 | 8 | 9 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_bridge | 0 | 0 | 1 | 6 | 6 | 8 | 9 | 9 | 8 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lookup_x | 0 | 0 | 1 | 7 | 18 | 5 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| context | 100* | 100* | 100* | 100* | 97* | 47 | 41 | 34 | 29 | 15 | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| question | 0 | 0 | 0 | 0 | 3 | 17 | 14 | 5 | 2 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| q_words | 0 | 0 | 0 | 0 | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| final | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 4 | 3 | 2 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## PM

| set | 0 | 3 | 6 | 9 | 12 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | max control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 90* | 88* | 89* | 86* | 84* | 52* | 47 | 41 | 15 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| bridge_word | 90* | 88* | 82* | 84* | 83* | 52* | 49 | 40 | 16 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| bind_other | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 5 |
| lookup_bridge | 0 | 0 | 1 | 3 | 2 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| lookup_x | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| context | 100* | 98* | 99* | 97* | 93* | 53* | 48 | 38 | 16 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 9 |
| question | 1 | 0 | 0 | 0 | 3 | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| q_words | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 3 |
| final | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

