# code_positions / d1code_map_27b

Cases: {"code": {"n": 80, "eligible": 198, "unaligned_skipped": 0, "competence": "d1code_competence_27b"}}
Sanity: {"identity": {"n": 320, "max_abs_ld_minus_clean": 0.2505000000000006, "max_abs_ld_minus_unedited_same_batch": 0.0, "top_is_clean_top": 1}, "all0": {"n": 160, "max_abs_ld_minus_C": 0.3752499999999994, "top_is_C_top": 1}}
Read vs greedy: {"n": 3500, "agree": 1.0, "read/greedy": {"A/A": 2973, "b/b": 526, "other/other": 1}}
Causality violations (predicted-zero cells with a non-zero delta): 0

Transit (C flips >= 50%, above the controls): {"KL": {"bind_bridge": [28, 30, 32, 34, 36, 38, 40, 42, 44], "bridge_word": [28, 30, 32, 34, 36, 38, 40, 42, 44], "context": [28, 30, 32, 34, 36, 38, 40, 42, 44]}, "KR": {"bind_bridge": [28, 30, 32, 34, 36, 38, 40, 42], "bridge_word": [28, 30, 32, 34, 36, 38, 40, 42], "context": [28, 30, 32, 34, 36, 38, 40, 42], "question": [44]}}
Handoff: {"KL": {"last_statement_transit": {"bind_bridge": 44, "bridge_word": 44, "context": 44}, "first_question_transit": null}, "KR": {"last_statement_transit": {"bind_bridge": 42, "bridge_word": 42, "context": 42}, "first_question_transit": 44}}

C's copy: X's answer (flips, %) by set and layer; '*' transit, '.' exact no-op (zero delta in every case); max control change rate (O or random) per row

## KL

| set | 28 | 30 | 32 | 34 | 36 | 38 | 40 | 42 | 44 | max control |
|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 100* | 100* | 100* | 96* | 95* | 72* | 0 |
| bridge_word | 100* | 100* | 100* | 100* | 100* | 100* | 96* | 95* | 70* | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | . | . | . | . | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | . | . | . | . | 0 |
| context | 100* | 100* | 100* | 100* | 100* | 100* | 96* | 95* | 72* | 0 |
| question | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## KR

| set | 28 | 30 | 32 | 34 | 36 | 38 | 40 | 42 | 44 | max control |
|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge | 100* | 100* | 100* | 99* | 81* | 80* | 69* | 64* | 22 | 0 |
| bridge_word | 100* | 100* | 100* | 96* | 79* | 78* | 68* | 64* | 22 | 0 |
| bind_other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lookup_bridge | . | . | . | . | . | . | . | . | . | 0 |
| lookup_x | . | . | . | . | . | . | . | . | . | 0 |
| context | 100* | 100* | 100* | 99* | 82* | 80* | 70* | 65* | 20 | 1 |
| question | 0 | 0 | 0 | 4 | 24 | 24 | 32 | 36 | 82* | 0 |
| q_words | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| final | 0 | 0 | 0 | 2 | 15 | 15 | 21 | 24 | 45 | 0 |

