# code_positions / d1code_smoke_map_27b

Cases: {"code": {"n": 2, "eligible": null, "unaligned_skipped": 0, "competence": "none"}}
Sanity: {"identity": {"n": 8, "max_abs_ld_minus_clean": 0.1875, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 4, "max_abs_ld_minus_C": 0.1875, "top_is_C_top": 1}}
Read vs greedy: {"n": 168, "agree": 1.0, "read/greedy": {"A/A": 140, "b/b": 28}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {}
Handoff: {}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## KL

| set | 32 | 36 | max control |
|---|---|---|---|
| bind_bridge | 100 | 100 | 0 |
| bridge_word | 100 | 100 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | . | . | 0 |
| lookup_x | . | . | 0 |
| context | 100 | 100 | 0 |
| question | 0 | 0 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

## KR

| set | 32 | 36 | max control |
|---|---|---|---|
| bind_bridge | 100 | 100 | 0 |
| bridge_word | 100 | 100 | 0 |
| bind_other | 0 | 0 | 0 |
| lookup_bridge | . | . | 0 |
| lookup_x | . | . | 0 |
| context | 100 | 100 | 0 |
| question | 0 | 0 | 0 |
| q_words | 0 | 0 | 0 |
| final | 0 | 0 | 0 |

