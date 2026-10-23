# statement_positions / gemma4itf_d1_topics2_smoke

Cases: {"tasks": {"tasks_set": "d1_topics_v2", "competence": "gemma4itf_d1_topics2_competence", "scenes": 3, "skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.31299999999999883, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 2.9375, "top_is_C_top": 1}}
Read vs greedy: {"n": 332, "agree": 0.9819, "read/greedy": {"A/A": 278, "b/b": 25, "other/other": 23, "A/other": 4, "b/A": 2}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 32 | 36 | max control |
|---|---|---|---|
| bind_bridge | 0 | 0 | 0 |
| bridge_word | 0 | 0 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 100 |
| lookup_x | 0 | 0 | 0 |
| context | 67 | 33 | 100 |
| question | 33 | 33 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 32 | 36 | max control |
|---|---|---|---|
| bind_bridge | 33 | 33 | 33 |
| bridge_word | 33 | 33 | 33 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 33 | 33 | 67 |
| question | 67 | 67 | 33 |
| q_words | 33 | 0 | 67 |
| final | 0 | 0 | 0 |

