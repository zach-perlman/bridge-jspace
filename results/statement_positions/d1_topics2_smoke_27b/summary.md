# statement_positions / d1_topics2_smoke_27b

Cases: {"tasks": {"tasks_set": "d1_topics_v2", "competence": "d1_topics2_competence_27b", "scenes": 3, "skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.18700000000000028, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 0.3125, "top_is_C_top": 1}}
Read vs greedy: {"n": 316, "agree": 1.0, "read/greedy": {"A/A": 279, "b/b": 36, "other/other": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 32 | 40 | max control |
|---|---|---|---|
| bind_bridge | 33 | 33 | 0 |
| bridge_word | 33 | 33 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 67 | 33 | 0 |
| question | 67 | 67 | 0 |
| q_words | 67 | 33 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 32 | 40 | max control |
|---|---|---|---|
| bind_bridge | 100 | 33 | 0 |
| bridge_word | 67 | 33 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 67 | 0 | 0 |
| question | 67 | 67 | 0 |
| q_words | 67 | 33 | 0 |
| final | 0 | 0 | 0 |

