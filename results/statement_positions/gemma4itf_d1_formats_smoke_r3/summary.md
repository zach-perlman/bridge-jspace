# statement_positions / gemma4itf_d1_formats_smoke_r3

Cases: {"tasks": {"tasks_set": "d1_formats_v1", "competence": "gemma4itf_d1_formats_competence_r3", "scenes": 3, "skipped": {}, "position_check_skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.4375, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 8.608875, "top_is_C_top": 1}}
Read vs greedy: {"n": 284, "agree": 0.993, "read/greedy": {"A/A": 257, "b/b": 23, "other/other": 2, "A/other": 2}}
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
| lookup_bridge | 0 | 0 | 33 |
| lookup_x | 0 | 0 | 0 |
| context | 33 | 33 | 33 |
| question | 33 | 67 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 32 | 36 | max control |
|---|---|---|---|
| bind_bridge | 33 | 0 | 0 |
| bridge_word | 33 | 0 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 33 | 0 | 0 |
| question | 67 | 33 | 0 |
| q_words | 33 | 0 | 33 |
| final | 0 | 0 | 0 |

