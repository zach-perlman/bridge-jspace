# statement_positions / qwen35_9b_d1_formats_smoke

Cases: {"tasks": {"tasks_set": "d1_formats_v1", "competence": "qwen35_9b_d1_formats_competence", "scenes": 3, "skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.125, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 0.5, "top_is_C_top": 1}}
Read vs greedy: {"n": 316, "agree": 1.0, "read/greedy": {"A/A": 290, "b/b": 26}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 16 | 20 | max control |
|---|---|---|---|
| bind_bridge | 33 | 0 | 0 |
| bridge_word | 33 | 0 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 33 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 67 | 33 | 0 |
| question | 33 | 0 | 0 |
| q_words | 33 | 0 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 16 | 20 | max control |
|---|---|---|---|
| bind_bridge | 100 | 33 | 0 |
| bridge_word | 100 | 33 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | 0 | 0 | 0 |
| context | 67 | 0 | 0 |
| question | 33 | 0 | 0 |
| q_words | 33 | 0 | 0 |
| final | 0 | 0 | 0 |

