# statement_positions / qwen3_32b_d1_topics_smoke

Cases: {"tasks": {"tasks_set": "d1_topics_v1", "competence": "qwen3_32b_d1_topics_competence", "scenes": 3, "skipped": {}}}
Sanity: {"identity": {"n": 12, "max_abs_ld_minus_clean": 0.25, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 6, "max_abs_ld_minus_C": 0.125, "top_is_C_top": 1}}
Read vs greedy: {"n": 304, "agree": 0.9967, "read/greedy": {"A/A": 262, "b/b": 37, "other/other": 4, "other/b": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## PP

| set | 32 | 40 | max control |
|---|---|---|---|
| bind_bridge | 67 | 67 | 0 |
| bridge_word | 67 | 67 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | . | . | 0 |
| context | 100 | 100 | 33 |
| question | 0 | 0 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

## PM

| set | 32 | 40 | max control |
|---|---|---|---|
| bind_bridge | 100 | 100 | 0 |
| bridge_word | 67 | 100 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | 0 | 0 | 0 |
| lookup_x | . | . | 0 |
| context | 100 | 100 | 0 |
| question | 0 | 0 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

