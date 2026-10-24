# Hardware gate: qwen35_122b_x0_hw_gate_parts vs qwen35_122b_d1_late_parts at bind_bridge:33

Gate: PASS: agreement 0.9982 over 2736 rows without random draws (bar 0.97; drift floor 0.9). Rows only in the new run: 720; only in the reference: 0.

| group | rows | agreement | median abs ld diff |
|---|---|---|---|
| gated | 2736 | 0.9982 | 0.0 |
| part full | 576 | 1.0000 | 0.0 |
| part jspace | 360 | 1.0000 | 0.0 |
| part jspace null | 360 | 1.0000 | 0.0 |
| part jspace_matched | 360 | 0.9806 | 0.25 |
| part jspace_wo_own | 360 | 1.0000 | 0.0 |
| part jspace_wo_own null | 360 | 1.0000 | 0.0 |
| part lens2 | 360 | 1.0000 | 0.0 |
| part lens2 null | 360 | 1.0000 | 0.0 |
| part lens2_matched | 360 | 0.9806 | 0.25 |
| part not_jspace | 360 | 1.0000 | 0.0 |
| part not_jspace null | 360 | 1.0000 | 0.0 |
| part not_jspace_matched | 360 | 0.9861 | 0.125 |
| part not_jspace_matched null | 360 | 0.9778 | 0.25 |
| part not_lens2 | 360 | 1.0000 | 0.0 |
| part not_lens2 null | 360 | 1.0000 | 0.0 |
| part rand_omp | 360 | 1.0000 | 0.0 |
| part rand_omp null | 360 | 1.0000 | 0.0 |
| part rand_sub | 360 | 1.0000 | 0.0 |
| part rand_sub null | 360 | 1.0000 | 0.0 |
| random draws (reported) | 4320 | 0.9949 | 0.0 |
| reader PM | 3528 | 0.9952 | 0.0 |
| reader PP | 3528 | 0.9972 | 0.0 |
