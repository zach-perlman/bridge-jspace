# statement_positions / olmo3_7b_instruct_jpp_d1_topics2_smoke

Cases: {"tasks": {"tasks_set": "d1_topics_v2", "competence": "olmo3_7b_instruct_d1_topics2_competence", "scenes": 3, "skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.125, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 25.28075, "top_is_C_top": 0.5}}
Read vs greedy: {"n": 324, "agree": 0.9691, "read/greedy": {"A/A": 286, "other/other": 24, "A/other": 5, "other/A": 5, "b/b": 4}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 16 | 20 | max control |
|---|---|---|---|
| bind_bridge | 0 | 0 | 0 |
| bridge_word | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 33 | 0 | 0 |
| question | 0 | 0 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 16 | 20 | max control |
|---|---|---|---|
| bind_bridge | 0 | 0 | 33 |
| bridge_word | 0 | 0 | 0 |
| bind_other | 0 | 0 | 33 |
| lookup_bridge | 0 | 0 | 33 |
| lookup_x | 0 | 0 | 33 |
| context | 0 | 0 | 33 |
| question | 0 | 0 | 33 |
| q_words | 0 | 0 | 33 |
| final | 0 | 0 | 33 |

