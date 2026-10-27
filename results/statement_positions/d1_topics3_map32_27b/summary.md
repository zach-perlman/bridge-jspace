# statement_positions / d1_topics3_map32_27b

Cases: {"tasks": {"tasks_set": "d1_topics_v3", "competence": "d1_topics3_competence_27b", "scenes": 180, "skipped": {}, "position_check_skipped": {}}}
Sanity: {"identity": {"n": 720, "max_abs_ld_minus_clean": 0.25, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 360, "max_abs_ld_minus_C": 2.375, "top_is_C_top": 0.9972222222222222}}
Read vs greedy: {"n": 566, "agree": 1.0, "read/greedy": {"A/A": 493, "b/b": 69, "other/other": 4}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"PP": {"context": [32]}, "PM": {"bind_bridge": [32], "bridge_word": [32], "context": [32]}}
Handoff: {"PP": {"last_statement_transit": {"context": 32}, "first_question_transit": null}, "PM": {"last_statement_transit": {"bind_bridge": 32, "bridge_word": 32, "context": 32}, "first_question_transit": null}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 32 | max control |
|---|---|---|
| bind_bridge | 44 | 1 |
| bridge_word | 43 | 0 |
| bind_other | 0 | 1 |
| lookup_bridge | 8 | 0 |
| lookup_x | 9 | 0 |
| context | 84* | 1 |
| question | 24 | 0 |
| q_words | 19 | 1 |
| final | 0 | 0 |

## PM

| set | 32 | max control |
|---|---|---|
| bind_bridge | 76* | 1 |
| bridge_word | 74* | 1 |
| bind_other | 1 | 1 |
| lookup_bridge | 3 | 1 |
| lookup_x | 1 | 0 |
| context | 77* | 1 |
| question | 22 | 1 |
| q_words | 22 | 0 |
| final | 0 | 0 |

