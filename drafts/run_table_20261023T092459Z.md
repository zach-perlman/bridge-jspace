<!-- DRAFT written by scripts/run_table.py from results/cross_model/20261023T091847Z/sources.txt, grid.csv and results/jobq/ledger_*.jsonl; links resolve from the repo root -->

# Runs behind the cross-model grid

Each table is one finding of the grid ([grid.md](results/cross_model/20261023T091847Z/grid.md)), in its order and words. A row is a setting, a column a model; a cell names the run behind the grid cell, linked to the folder the grid read, with the grid's verdict (✓ holds · ✗ fails · ≈ inconclusive · ⚠ not interpretable · ⊘ not testable · · missing · ○ open). A second line in a cell is a run with another lens, or another run listed beside the main one. A run that never ran is named without a link, with the reason. Under each table, the job that wrote each run, from the queue ledgers; a job that failed at its figures step had finished its run step (exit 0). Nothing here is human-verified.

Night of 22-23 Oct, from the queue ledgers: the jobs started from 22 Oct 19:30 UTC to the last record (23 Oct 09:15 UTC). sesterce-a100x4 (NVIDIA A100 80GB PCIe): 148 jobs, 132 done, 16 failed, 50.6 GPU-hours; sesterce-h200x2 (NVIDIA H200): 34 jobs, 34 done, 0 failed, 16.6 GPU-hours. In all 182 jobs, 166 done, 16 failed, 67.2 GPU-hours (wall time x GPUs, failed jobs included; without a wall time in the ledger, not counted: d4_layer_gap_27b (worker died during the run (found on worker restart))).

## Finding 1: Removing the J-space breaks recall, not the lookup

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| tasks, Zach's rule | ✓ `full2_ko_v1` (on origin/zach/v8-breadth-1021) | · no spec | ⊘ no lens | · no spec | · no spec | · no spec | · no spec | · `gemma4itf_full_ko_v1` (not on Zach's branch) |
| animal suite | ○ [`abl_rot_v1`](results/ablate_pilot/abl_rot_v1/) | ○ [`qwen35_9b_abl_rot_v1`](results/ablate_pilot/qwen35_9b_abl_rot_v1/) | ⊘ no lens | ○ [`qwen35_122b_abl_rot_v1`](results/ablate_pilot/qwen35_122b_abl_rot_v1/)<br>Zach's pilot: ○ [`qwen35_122b_abl_v1`](results/ablate_pilot/qwen35_122b_abl_v1/) | ○ [`qwen3_32b_jpp_abl_rot_v1`](results/ablate_pilot/qwen3_32b_jpp_abl_rot_v1/) | ⚠ [`olmo3_7b_instruct_jpp_abl_rot_raw_v1`](results/ablate_pilot/olmo3_7b_instruct_jpp_abl_rot_raw_v1/)<br>plain J-lens: ⚠ [`olmo3_7b_instruct_abl_rot_raw_v1`](results/ablate_pilot/olmo3_7b_instruct_abl_rot_raw_v1/) | ○ [`muse30b_abl_rot_v1`](results/ablate_pilot/muse30b_abl_rot_v1/) | · `gemma4itf_abl_rot_v1` (blocked)<br>refit J++: ○ [`gemma4itr_abl_rot_v1`](results/ablate_pilot/gemma4itr_abl_rot_v1/) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `qwen35_9b_abl_rot_v1` | `qwen35_9b_abl_rot_v1` | sesterce-a100x4 | 23 Oct 03:10 | 0.78 | 0a8820d |
| `qwen3_32b_jpp_abl_rot_v1` | `qwen3_32b_jpp_abl_rot_v1` | sesterce-a100x4 | 23 Oct 08:59 | 0.43 | 193c060 |
| `olmo3_7b_instruct_jpp_abl_rot_raw_v1` | `olmo3_7b_instruct_jpp_abl_rot_raw_v1` | sesterce-a100x4 | 23 Oct 09:14 | 0.28 | 2f3c320 |
| `olmo3_7b_instruct_abl_rot_raw_v1` | `olmo3_7b_instruct_abl_rot_raw_v1` | sesterce-a100x4 | 21 Oct 20:30 | 0.29 | 1eec3a3 |
| `muse30b_abl_rot_v1` | `muse30b_abl_rot_v1` | sesterce-a100x4 | 23 Oct 04:35 | 0.89 | 0a8820d |
| `qwen35_122b_abl_rot_v1` | `qwen35_122b_abl_rot_v1_b16` | sesterce-h200x2 | 23 Oct 07:54 | 0.37 | 54e7edd |

Not in the queue ledgers (run by hand, before the queue, or on Zach's branch): `full2_ko_v1`, `abl_rot_v1`, `gemma4itr_abl_rot_v1`, `qwen35_122b_abl_v1`.

## Finding 2: A lookup ignores the lens-readable part of a stated bridge

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| draw 1 | ✓ [`d1_topics_parts_27b`](results/d1_verdict/d1_topics_parts_27b_20261022-185412/) | · no spec | ⊘ no lens | · no spec | ⚠ [`qwen3_32b_jpp_d1_topics_parts`](results/d1_verdict/qwen3_32b_jpp_d1_topics_parts_20261023-084011/)<br>plain J-lens: ⚠ [`qwen3_32b_d1_topics_parts`](results/d1_verdict/qwen3_32b_d1_topics_parts_20261022-193655/) | · no spec | · no spec | · no spec |
| draw 2 | ✓ [`d1_topics2_parts_27b`](results/d1_verdict/d1_topics2_parts_27b_20261022-204445/)<br>plain J-lens: ⚠ [`qwen36_27b_jlens_d1_topics2_parts`](results/d1_verdict/qwen36_27b_jlens_d1_topics2_parts_20261022-214620/) | ✓ [`qwen35_9b_d1_topics2_parts`](results/d1_verdict/qwen35_9b_d1_topics2_parts_20261022-185955/) | ⊘ no lens | ✗ [`qwen35_122b_d1_topics2_parts`](results/d1_verdict/qwen35_122b_d1_topics2_parts_20261023-022547/) | · no spec | · [`olmo3_7b_instruct_jpp_d1_topics2_parts`](results/statement_positions/olmo3_7b_instruct_jpp_d1_topics2_parts/) (failed)<br>plain J-lens: · [`olmo3_7b_instruct_d1_topics2_parts`](results/statement_positions/olmo3_7b_instruct_d1_topics2_parts/) (failed) | · `muse30b_d1_topics2_parts` (not run) | · `gemma4itf_d1_topics2_parts` (blocked)<br>base-model J++: · `gemma4itb_d1_topics2_parts` (not run) |
| table | ✓ [`d1_formats_parts_27b`](results/d1_verdict/d1_formats_parts_27b_20261023-005643/) | ✓ [`qwen35_9b_d1_formats_parts`](results/d1_verdict/qwen35_9b_d1_formats_parts_20261022-220529/) | ⊘ no lens | ✗ [`qwen35_122b_d1_formats_parts`](results/d1_verdict/qwen35_122b_d1_formats_parts_20261023-075315/) | · `qwen3_32b_jpp_d1_formats_parts` (pending) | ⊘ `olmo3_7b_instruct_jpp_d1_formats_parts` (stopped by the precheck: too few eligible scenes, or the gate (blocks olmo3_7b_instruct_jpp_d1_formats_parts)) | · `muse30b_d1_formats_parts` (not run) | · `gemma4itf_d1_formats_parts` (blocked) |
| JSON | ✓ [`d1_formats_parts_27b`](results/d1_verdict/d1_formats_parts_27b_20261023-005643/) | ✓ [`qwen35_9b_d1_formats_parts`](results/d1_verdict/qwen35_9b_d1_formats_parts_20261022-220529/) | ⊘ no lens | ✗ [`qwen35_122b_d1_formats_parts`](results/d1_verdict/qwen35_122b_d1_formats_parts_20261023-075315/) | · `qwen3_32b_jpp_d1_formats_parts` (pending) | ⊘ `olmo3_7b_instruct_jpp_d1_formats_parts` (stopped by the precheck: too few eligible scenes, or the gate (blocks olmo3_7b_instruct_jpp_d1_formats_parts)) | · `muse30b_d1_formats_parts` (not run) | · `gemma4itf_d1_formats_parts` (blocked) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d1_topics_parts_27b` | `d1_topics_parts_27b` | sesterce-a100x4 | 22 Oct 16:48 | 0.29 | 3e90959 |
| `d1_topics2_parts_27b` | `d1_topics2_parts_27b` | sesterce-a100x4 | 22 Oct 20:44 | 0.43 | a786b36 |
| `qwen36_27b_jlens_d1_topics2_parts` | `qwen36_27b_jlens_d1_topics2_parts` | sesterce-a100x4 | 22 Oct 21:46 | 0.43 | b51e964 |
| `qwen35_9b_d1_topics2_parts` | `qwen35_9b_d1_topics2_parts` | sesterce-a100x4 | 22 Oct 18:59 | 0.24 | a786b36 |
| `qwen3_32b_jpp_d1_topics_parts` | `qwen3_32b_jpp_d1_topics_parts` | sesterce-a100x4 | 23 Oct 08:40 | 0.40 | 193c060 |
| `qwen3_32b_d1_topics_parts` | `qwen3_32b_d1_topics_parts` | sesterce-a100x4 | 22 Oct 16:57 | 0.40 | 3e90959 |
| `olmo3_7b_instruct_jpp_d1_topics2_parts` | `olmo3_7b_instruct_jpp_d1_topics2_parts` (failed at run, exit 1) | sesterce-a100x4 | 23 Oct 08:33 | 0.01 | 2f3c320 |
| `olmo3_7b_instruct_d1_topics2_parts` | `olmo3_7b_instruct_d1_topics2_parts_r2` (failed at run, exit 1) | sesterce-a100x4 | 22 Oct 21:05 | 0.01 | 921671d |
| `qwen35_122b_d1_topics2_parts` | `qwen35_122b_d1_topics2_parts_r3` | sesterce-h200x2 | 23 Oct 02:25 | 0.52 | 4a87d79 |
| `d1_formats_parts_27b` | `d1_formats_parts_27b` | sesterce-a100x4 | 23 Oct 00:56 | 0.84 | dbc4527 |
| `qwen35_9b_d1_formats_parts` | `qwen35_9b_d1_formats_parts` | sesterce-a100x4 | 22 Oct 22:05 | 0.36 | dbc4527 |
| `qwen35_122b_d1_formats_parts` | `qwen35_122b_d1_formats_parts_b16` | sesterce-h200x2 | 23 Oct 07:53 | 0.61 | 54e7edd |

## Finding 3: The last tokens read the answer's digit, not the entity's name

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| draw 1 | ✓ [`d2_parts_v2_27b`](results/attn_knockout/d2_parts_v2_27b/) | ✓ [`qwen35_9b_d2_parts_v2`](results/attn_knockout/qwen35_9b_d2_parts_v2/) | ✓ [`olmo_hybrid_7b_d2_parts_v2`](results/attn_knockout/olmo_hybrid_7b_d2_parts_v2/) | ✓ [`qwen35_122b_d2_parts`](results/attn_knockout/qwen35_122b_d2_parts/) | ✓ [`qwen3_32b_d2_parts_v2`](results/attn_knockout/qwen3_32b_d2_parts_v2/) | ✓ [`olmo3_7b_instruct_d2_parts_v2`](results/attn_knockout/olmo3_7b_instruct_d2_parts_v2/) | ✓ [`muse30b_d2_parts`](results/attn_knockout/muse30b_d2_parts/) | ✓ [`gemma4it_d2_parts_v2`](results/attn_knockout/gemma4it_d2_parts_v2/) |
| draw 2 | ✓ [`d2_parts_seed2_27b`](results/attn_knockout/d2_parts_seed2_27b/) | ✓ [`qwen35_9b_d2_parts_seed2`](results/attn_knockout/qwen35_9b_d2_parts_seed2/) | ✓ [`olmo_hybrid_7b_d2_parts_seed2`](results/attn_knockout/olmo_hybrid_7b_d2_parts_seed2/) | ✓ [`qwen35_122b_d2_parts_seed2`](results/attn_knockout/qwen35_122b_d2_parts_seed2/) | ✓ [`qwen3_32b_d2_parts_seed2`](results/attn_knockout/qwen3_32b_d2_parts_seed2/) | ✓ [`olmo3_7b_instruct_d2_parts_seed2`](results/attn_knockout/olmo3_7b_instruct_d2_parts_seed2/) | ✓ [`muse30b_d2_parts_seed2`](results/attn_knockout/muse30b_d2_parts_seed2/) | ✓ [`gemma4it_d2_parts_seed2`](results/attn_knockout/gemma4it_d2_parts_seed2/) |
| draw 3 | · `d2_parts_seed3_27b` (no spec) | ✓ [`qwen35_9b_d2_parts_seed3`](results/attn_knockout/qwen35_9b_d2_parts_seed3/) | · `olmo_hybrid_7b_d2_parts_seed3` (no spec) | · `qwen35_122b_d2_parts_seed3` (no spec) | ✓ [`qwen3_32b_d2_parts_seed3`](results/attn_knockout/qwen3_32b_d2_parts_seed3/) | ✓ [`olmo3_7b_instruct_d2_parts_seed3`](results/attn_knockout/olmo3_7b_instruct_d2_parts_seed3/) | ✓ [`muse30b_d2_parts_seed3`](results/attn_knockout/muse30b_d2_parts_seed3/) | ✓ [`gemma4it_d2_parts_seed3`](results/attn_knockout/gemma4it_d2_parts_seed3/) |
| prose | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ⚠ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ⚠ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ✗ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) | ✓ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |
| table | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ✓ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ✓ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ⊘ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) (competence) | ✓ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |
| JSON | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ⚠ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ✓ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ⊘ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) (competence) | ✓ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d2_parts_v2_27b` | `d2_parts_v2_27b` | sesterce-a100x4 | 22 Oct 14:37 | 0.22 | 5cb6a87 |
| `d2_parts_seed2_27b` | `d2_parts_seed2_27b` | sesterce-a100x4 | 22 Oct 16:01 | 0.21 | d822f6e |
| `d2_formats_27b` | `d2_formats_27b` | sesterce-a100x4 | 22 Oct 18:44 | 0.34 | 444500e |
| `olmo3_7b_instruct_d2_parts_v2` | `olmo3_7b_instruct_d2_parts_v2` | sesterce-a100x4 | 22 Oct 14:26 | 0.03 | 5cb6a87 |
| `olmo3_7b_instruct_d2_parts_seed2` | `olmo3_7b_instruct_d2_parts_seed2` | sesterce-a100x4 | 22 Oct 19:03 | 0.03 | b23c331 |
| `olmo3_7b_instruct_d2_parts_seed3` | `olmo3_7b_instruct_d2_parts_seed3` | sesterce-a100x4 | 23 Oct 07:21 | 0.03 | c07e7cf |
| `olmo3_7b_instruct_d2_formats` | `olmo3_7b_instruct_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:27 | 0.06 | 2dadb64 |
| `olmo_hybrid_7b_d2_parts_v2` | `olmo_hybrid_7b_d2_parts_v2` | sesterce-a100x4 | 23 Oct 05:35 | 0.05 | 51ff150 |
| `olmo_hybrid_7b_d2_parts_seed2` | `olmo_hybrid_7b_d2_parts_seed2` | sesterce-a100x4 | 23 Oct 04:04 | 0.05 | ec3be50 |
| `olmo_hybrid_7b_d2_formats` | `olmo_hybrid_7b_d2_formats` | sesterce-a100x4 | 23 Oct 09:15 | 0.08 | 51ff150 |
| `qwen35_9b_d2_parts_v2` | `qwen35_9b_d2_parts_v2` | sesterce-a100x4 | 22 Oct 14:30 | 0.07 | 5cb6a87 |
| `qwen35_9b_d2_parts_seed2` | `qwen35_9b_d2_parts_seed2` | sesterce-a100x4 | 22 Oct 19:09 | 0.07 | b23c331 |
| `qwen35_9b_d2_parts_seed3` | `qwen35_9b_d2_parts_seed3` | sesterce-a100x4 | 23 Oct 07:12 | 0.07 | c07e7cf |
| `qwen35_9b_d2_formats` | `qwen35_9b_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:27 | 0.09 | 2dadb64 |
| `qwen3_32b_d2_parts_v2` | `qwen3_32b_d2_parts_v2` | sesterce-a100x4 | 22 Oct 14:31 | 0.12 | 5cb6a87 |
| `qwen3_32b_d2_parts_seed2` | `qwen3_32b_d2_parts_seed2` | sesterce-a100x4 | 22 Oct 16:05 | 0.10 | d822f6e |
| `qwen3_32b_d2_parts_seed3` | `qwen3_32b_d2_parts_seed3` | sesterce-a100x4 | 23 Oct 07:06 | 0.10 | c07e7cf |
| `qwen3_32b_d2_formats` | `qwen3_32b_d2_formats` | sesterce-a100x4 | 22 Oct 18:56 | 0.21 | 444500e |
| `muse30b_d2_parts` | `muse30b_d2_parts` | sesterce-a100x4 | 23 Oct 00:47 | 0.18 | 2dadb64 |
| `muse30b_d2_parts_seed2` | `muse30b_d2_parts_seed2` | sesterce-a100x4 | 23 Oct 01:25 | 0.17 | 2dadb64 |
| `muse30b_d2_parts_seed3` | `muse30b_d2_parts_seed3` | sesterce-a100x4 | 23 Oct 07:59 | 0.17 | c07e7cf |
| `muse30b_d2_formats` | `muse30b_d2_formats` | sesterce-a100x4 | 23 Oct 07:40 | 0.02 | 2dadb64 |
| `gemma4it_d2_parts_v2` | `gemma4it_d2_parts_v2` | sesterce-a100x4 | 22 Oct 19:27 | 0.19 | b23c331 |
| `gemma4it_d2_parts_seed2` | `gemma4it_d2_parts_seed2` | sesterce-a100x4 | 22 Oct 19:40 | 0.19 | b23c331 |
| `gemma4it_d2_parts_seed3` | `gemma4it_d2_parts_seed3` | sesterce-a100x4 | 23 Oct 07:39 | 0.19 | c07e7cf |
| `gemma4it_d2_formats` | `gemma4it_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:47 | 0.30 | 2dadb64 |
| `qwen35_122b_d2_parts` | `qwen35_122b_d2_parts` | sesterce-h200x2 | 23 Oct 00:29 | 0.19 | 38eb5d4 |
| `qwen35_122b_d2_parts_seed2` | `qwen35_122b_d2_parts_seed2_b16` | sesterce-h200x2 | 23 Oct 02:26 | 0.17 | 54e7edd |
| `qwen35_122b_d2_formats` | `qwen35_122b_d2_formats` | sesterce-h200x2 | 23 Oct 02:11 | 0.35 | 38eb5d4 |

## Finding 4: A lookup ends in a late attention read of the answer's sentence

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| draw 1 | ✓ [`d2_v4_late_read`](results/attn_knockout/d2_v4_late_read/) | ✓ [`qwen35_9b_d2_v4_late_read_r2`](results/attn_knockout/qwen35_9b_d2_v4_late_read_r2/) | ✓ [`olmo_hybrid_7b_d2_v4_late_read_v3`](results/attn_knockout/olmo_hybrid_7b_d2_v4_late_read_v3/) | ✓ [`qwen35_122b_d2_late_read`](results/attn_knockout/qwen35_122b_d2_late_read/) | ✓ [`qwen3_32b_d2_v4_late_read_v2_r2`](results/attn_knockout/qwen3_32b_d2_v4_late_read_v2_r2/) | ✓ [`olmo3_7b_instruct_d2_v4_late_read_v3`](results/attn_knockout/olmo3_7b_instruct_d2_v4_late_read_v3/) | ✓ [`muse30b_d2_late_read`](results/attn_knockout/muse30b_d2_late_read/) | ✗ [`gemma4it_d2_v4_late_read_v3_r2`](results/attn_knockout/gemma4it_d2_v4_late_read_v3_r2/) |
| draw 2 | ✓ [`d2_late_read_seed2_27b`](results/attn_knockout/d2_late_read_seed2_27b/) | ✓ [`qwen35_9b_d2_late_read_seed2`](results/attn_knockout/qwen35_9b_d2_late_read_seed2/) | ✓ [`olmo_hybrid_7b_d2_late_read_seed2`](results/attn_knockout/olmo_hybrid_7b_d2_late_read_seed2/) | ✓ [`qwen35_122b_d2_late_read_seed2`](results/attn_knockout/qwen35_122b_d2_late_read_seed2/) | ✓ [`qwen3_32b_d2_late_read_seed2`](results/attn_knockout/qwen3_32b_d2_late_read_seed2/) | ✓ [`olmo3_7b_instruct_d2_late_read_seed2`](results/attn_knockout/olmo3_7b_instruct_d2_late_read_seed2/) | ✓ [`muse30b_d2_late_read_seed2`](results/attn_knockout/muse30b_d2_late_read_seed2/) | ✗ [`gemma4it_d2_late_read_seed2`](results/attn_knockout/gemma4it_d2_late_read_seed2/) |
| draw 3 | · `d2_late_read_seed3_27b` (no spec) | ✓ [`qwen35_9b_d2_late_read_seed3`](results/attn_knockout/qwen35_9b_d2_late_read_seed3/) | · `olmo_hybrid_7b_d2_late_read_seed3` (no spec) | · `qwen35_122b_d2_late_read_seed3` (no spec) | ✓ [`qwen3_32b_d2_late_read_seed3`](results/attn_knockout/qwen3_32b_d2_late_read_seed3/) | ✓ [`olmo3_7b_instruct_d2_late_read_seed3`](results/attn_knockout/olmo3_7b_instruct_d2_late_read_seed3/) | ✓ [`muse30b_d2_late_read_seed3`](results/attn_knockout/muse30b_d2_late_read_seed3/) | ✓ [`gemma4it_d2_late_read_seed3`](results/attn_knockout/gemma4it_d2_late_read_seed3/) |
| prose | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ⚠ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ⚠ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ⚠ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) | ✗ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |
| table | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ✗ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ✓ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ⊘ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) (competence) | ✓ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |
| JSON | ✓ [`d2_formats_27b`](results/attn_knockout/d2_formats_27b/) | ✓ [`qwen35_9b_d2_formats`](results/attn_knockout/qwen35_9b_d2_formats/) | ⚠ [`olmo_hybrid_7b_d2_formats`](results/attn_knockout/olmo_hybrid_7b_d2_formats/) | ✓ [`qwen35_122b_d2_formats`](results/attn_knockout/qwen35_122b_d2_formats/) | ✓ [`qwen3_32b_d2_formats`](results/attn_knockout/qwen3_32b_d2_formats/) | ⚠ [`olmo3_7b_instruct_d2_formats`](results/attn_knockout/olmo3_7b_instruct_d2_formats/) | ⊘ [`muse30b_d2_formats`](results/attn_knockout/muse30b_d2_formats/) (competence) | ✗ [`gemma4it_d2_formats`](results/attn_knockout/gemma4it_d2_formats/) |
| long context | ✗ [`d2_late_read_long_27b_r3`](results/attn_knockout/d2_late_read_long_27b_r3/) | ✓ [`qwen35_9b_d2_late_read_long`](results/attn_knockout/qwen35_9b_d2_late_read_long/) | · `olmo_hybrid_7b_d2_late_read_long` (running) | ✓ [`qwen35_122b_d2_late_read_long`](results/attn_knockout/qwen35_122b_d2_late_read_long/) | ✓ [`qwen3_32b_d2_late_read_long`](results/attn_knockout/qwen3_32b_d2_late_read_long/) | ✓ [`olmo3_7b_instruct_d2_late_read_long`](results/attn_knockout/olmo3_7b_instruct_d2_late_read_long/) | ✓ [`muse30b_d2_late_read_long`](results/attn_knockout/muse30b_d2_late_read_long/) | · `gemma4it_d2_late_read_long` (failed) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d2_v4_late_read` | `d2_v4_late_read` | sesterce-a100x4 | 21 Oct 20:04 | 1.06 | c2d5b8e |
| `d2_late_read_seed2_27b` | `d2_late_read_seed2_27b` | sesterce-a100x4 | 22 Oct 17:12 | 0.06 | 6538445 |
| `d2_formats_27b` | `d2_formats_27b` | sesterce-a100x4 | 22 Oct 18:44 | 0.34 | 444500e |
| `d2_late_read_long_27b_r3` | `d2_late_read_long_27b_r3` | sesterce-a100x4 | 23 Oct 04:51 | 1.69 | 326b54a |
| `olmo3_7b_instruct_d2_v4_late_read_v3` | `olmo3_7b_instruct_d2_v4_late_read_v3` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 00:23 | 0.13 | 9ac2657 |
| `olmo3_7b_instruct_d2_late_read_seed2` | `olmo3_7b_instruct_d2_late_read_seed2` | sesterce-a100x4 | 22 Oct 19:01 | 0.01 | b23c331 |
| `olmo3_7b_instruct_d2_late_read_seed3` | `olmo3_7b_instruct_d2_late_read_seed3` | sesterce-a100x4 | 23 Oct 07:19 | 0.01 | c07e7cf |
| `olmo3_7b_instruct_d2_formats` | `olmo3_7b_instruct_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:27 | 0.06 | 2dadb64 |
| `olmo3_7b_instruct_d2_late_read_long` | `olmo3_7b_instruct_d2_late_read_long_r2_q` | sesterce-a100x4 | 23 Oct 07:57 | 0.27 | 2dadb64 |
| `olmo_hybrid_7b_d2_v4_late_read_v3` | `olmo_hybrid_7b_d2_v4_late_read_v3` | sesterce-a100x4 | 23 Oct 05:49 | 0.26 | 51ff150 |
| `olmo_hybrid_7b_d2_late_read_seed2` | `olmo_hybrid_7b_d2_late_read_seed2` | sesterce-a100x4 | 23 Oct 04:01 | 0.02 | ec3be50 |
| `olmo_hybrid_7b_d2_formats` | `olmo_hybrid_7b_d2_formats` | sesterce-a100x4 | 23 Oct 09:15 | 0.08 | 51ff150 |
| `qwen35_9b_d2_v4_late_read_r2` | `qwen35_9b_d2_v4_late_read_r2` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 09:44 | 0.41 | 0c0c675 |
| `qwen35_9b_d2_late_read_seed2` | `qwen35_9b_d2_late_read_seed2` | sesterce-a100x4 | 22 Oct 19:05 | 0.03 | b23c331 |
| `qwen35_9b_d2_late_read_seed3` | `qwen35_9b_d2_late_read_seed3` | sesterce-a100x4 | 23 Oct 07:08 | 0.03 | c07e7cf |
| `qwen35_9b_d2_formats` | `qwen35_9b_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:27 | 0.09 | 2dadb64 |
| `qwen35_9b_d2_late_read_long` | `qwen35_9b_d2_late_read_long` | sesterce-a100x4 | 22 Oct 20:04 | 0.56 | ae5f47f |
| `qwen3_32b_d2_v4_late_read_v2_r2` | `qwen3_32b_d2_v4_late_read_v2_r2` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 12:18 | 0.94 | 0c0c675 |
| `qwen3_32b_d2_late_read_seed2` | `qwen3_32b_d2_late_read_seed2` | sesterce-a100x4 | 22 Oct 17:12 | 0.03 | 6538445 |
| `qwen3_32b_d2_late_read_seed3` | `qwen3_32b_d2_late_read_seed3` | sesterce-a100x4 | 23 Oct 07:00 | 0.02 | c07e7cf |
| `qwen3_32b_d2_formats` | `qwen3_32b_d2_formats` | sesterce-a100x4 | 22 Oct 18:56 | 0.21 | 444500e |
| `qwen3_32b_d2_late_read_long` | `qwen3_32b_d2_late_read_long_r2_q` | sesterce-a100x4 | 23 Oct 09:03 | 1.10 | 2dadb64 |
| `muse30b_d2_late_read` | `muse30b_d2_late_read` | sesterce-a100x4 | 23 Oct 00:37 | 0.03 | 2dadb64 |
| `muse30b_d2_late_read_seed2` | `muse30b_d2_late_read_seed2` | sesterce-a100x4 | 23 Oct 01:16 | 0.04 | 2dadb64 |
| `muse30b_d2_late_read_seed3` | `muse30b_d2_late_read_seed3` | sesterce-a100x4 | 23 Oct 07:48 | 0.03 | c07e7cf |
| `muse30b_d2_formats` | `muse30b_d2_formats` | sesterce-a100x4 | 23 Oct 07:40 | 0.02 | 2dadb64 |
| `muse30b_d2_late_read_long` | `muse30b_d2_late_read_long` | sesterce-a100x4 | 23 Oct 08:16 | 0.21 | 2dadb64 |
| `gemma4it_d2_v4_late_read_v3_r2` | `gemma4it_d2_v4_late_read_v3_r2` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 12:29 | 1.42 | 0c0c675 |
| `gemma4it_d2_late_read_seed2` | `gemma4it_d2_late_read_seed2` | sesterce-a100x4 | 22 Oct 19:29 | 0.03 | b23c331 |
| `gemma4it_d2_late_read_seed3` | `gemma4it_d2_late_read_seed3` | sesterce-a100x4 | 23 Oct 07:29 | 0.03 | c07e7cf |
| `gemma4it_d2_formats` | `gemma4it_d2_formats_r2_q` | sesterce-a100x4 | 23 Oct 07:47 | 0.30 | 2dadb64 |
| `qwen35_122b_d2_late_read` | `qwen35_122b_d2_late_read` | sesterce-h200x2 | 23 Oct 00:18 | 0.08 | 38eb5d4 |
| `qwen35_122b_d2_late_read_seed2` | `qwen35_122b_d2_late_read_seed2_b16` | sesterce-h200x2 | 23 Oct 02:16 | 0.08 | 54e7edd |
| `qwen35_122b_d2_formats` | `qwen35_122b_d2_formats` | sesterce-h200x2 | 23 Oct 02:11 | 0.35 | 38eb5d4 |
| `qwen35_122b_d2_late_read_long` | `qwen35_122b_d2_late_read_long` | sesterce-h200x2 | 23 Oct 01:54 | 0.88 | 38eb5d4 |

## Finding 5: Order label for the 1st and 2nd sentence, the bridge's identity after

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| draw 1 | ✓ [`d3v4_swap_topics`](results/pointer_swap/d3v4_swap_topics/) | ✓ [`qwen35_9b_d3v4_swap_r2`](results/finding5_confirm/qwen35_9b_d3v4_swap_r2_20261022-203850/) | ✓ [`olmo_hybrid_7b_d3v4_swap_fn`](results/finding5_confirm/olmo_hybrid_7b_d3v4_swap_fn_20261023-043737/) | ✓ [`qwen35_122b_d3v4_swap`](results/finding5_confirm/qwen35_122b_d3v4_swap_20261023-010203/) | ✗ [`qwen3_32b_d3v4_swap_r2`](results/pointer_swap/qwen3_32b_d3v4_swap_r2/) | ✓ [`olmo3_7b_instruct_d3v4_swap_fn`](results/finding5_confirm/olmo3_7b_instruct_d3v4_swap_fn_20261022-200354/) | ✓ [`muse30b_d3v4_swap`](results/pointer_swap/muse30b_d3v4_swap/) | ✓ [`gemma4it_d3v4_swap_v2_r2`](results/finding5_confirm/gemma4it_d3v4_swap_v2_r2_20261022-203851/) |
| draw 2 | ✓ [`d3v4_seed2_swap_27b`](results/pointer_swap/d3v4_seed2_swap_27b/) | ✓ [`qwen35_9b_d3v4_seed2_swap`](results/finding5_confirm/qwen35_9b_d3v4_seed2_swap_20261022-191553/) | ✓ [`olmo_hybrid_7b_d3v4_seed2_swap`](results/finding5_confirm/olmo_hybrid_7b_d3v4_seed2_swap_20261023-041610/) | ✓ [`qwen35_122b_d3v4_seed2_swap`](results/finding5_confirm/qwen35_122b_d3v4_seed2_swap_20261023-025906/) | ✓ [`qwen3_32b_d3v4_seed2_swap`](results/finding5_confirm/qwen3_32b_d3v4_seed2_swap_20261022-171026/) | ✓ [`olmo3_7b_instruct_d3v4_seed2_swap`](results/finding5_confirm/olmo3_7b_instruct_d3v4_seed2_swap_20261022-222827/) | ✓ [`muse30b_d3v4_seed2_swap`](results/finding5_confirm/muse30b_d3v4_seed2_swap_20261023-012450/) | ✓ [`gemma4it_d3v4_seed2_swap`](results/finding5_confirm/gemma4it_d3v4_seed2_swap_20261022-200015/) |
| draw 3 | ✓ [`d3v4_seed3_swap_27b`](results/finding5_confirm/d3v4_seed3_swap_27b_20261022-172157/) | ✓ [`qwen35_9b_d3v4_seed3_swap`](results/finding5_confirm/qwen35_9b_d3v4_seed3_swap_20261023-071911/) | · `olmo_hybrid_7b_d3v4_seed3_swap` (no spec) | ✓ [`qwen35_122b_d3v4_seed3_swap`](results/finding5_confirm/qwen35_122b_d3v4_seed3_swap_20261023-032645/) | ✓ [`qwen3_32b_d3v4_seed3_swap`](results/finding5_confirm/qwen3_32b_d3v4_seed3_swap_20261023-071224/) | ✓ [`olmo3_7b_instruct_d3v4_seed3_swap`](results/finding5_confirm/olmo3_7b_instruct_d3v4_seed3_swap_20261023-072419/) | ✓ [`muse30b_d3v4_seed3_swap`](results/finding5_confirm/muse30b_d3v4_seed3_swap_20261023-081705/) | ✓ [`gemma4it_d3v4_seed3_swap`](results/finding5_confirm/gemma4it_d3v4_seed3_swap_20261023-080351/) |
| 8 sentences | ✓ [`d3v5_len8_swap_27b`](results/finding5_confirm/d3v5_len8_swap_27b_e8-digit_20261023-055503/) | ✓ [`qwen35_9b_d3v5_len8_swap`](results/finding5_confirm/qwen35_9b_d3v5_len8_swap_e8-digit_20261023-053233/) | ✓ [`olmo_hybrid_7b_d3v5_len8_swap`](results/finding5_confirm/olmo_hybrid_7b_d3v5_len8_swap_e8-digit_20261023-063242/) | ✓ [`qwen35_122b_d3v5_len8_swap`](results/finding5_confirm/qwen35_122b_d3v5_len8_swap_e8-digit_20261023-051442/) | ✓ [`qwen3_32b_d3v5_len8_swap`](results/finding5_confirm/qwen3_32b_d3v5_len8_swap_e8-digit_20261023-061917/) | ✓ [`olmo3_7b_instruct_d3v5_len8_swap`](results/finding5_confirm/olmo3_7b_instruct_d3v5_len8_swap_e8-digit_20261023-060403/) | ✓ [`muse30b_d3v5_len8_swap`](results/finding5_confirm/muse30b_d3v5_len8_swap_e8-digit_20261023-065433/) | · `gemma4it_d3v5_len8_swap` (no spec) |
| 12 sentences | ✓ [`d3v5_len12_swap_27b`](results/finding5_confirm/d3v5_len12_swap_27b_e12-word_20261023-054540/) | ✓ [`qwen35_9b_d3v5_len12_swap`](results/finding5_confirm/qwen35_9b_d3v5_len12_swap_e12-word_20261023-053329/) | ✓ [`olmo_hybrid_7b_d3v5_len12_swap`](results/finding5_confirm/olmo_hybrid_7b_d3v5_len12_swap_e12-word_20261023-064150/) | ✓ [`qwen35_122b_d3v5_len12_swap`](results/finding5_confirm/qwen35_122b_d3v5_len12_swap_e12-word_20261023-041808/) | ✓ [`qwen3_32b_d3v5_len12_swap`](results/finding5_confirm/qwen3_32b_d3v5_len12_swap_e12-word_20261023-061726/) | ✓ [`olmo3_7b_instruct_d3v5_len12_swap`](results/finding5_confirm/olmo3_7b_instruct_d3v5_len12_swap_e12-word_20261023-101137/) | ✓ [`muse30b_d3v5_len12_swap`](results/finding5_confirm/muse30b_d3v5_len12_swap_e12-word_20261023-064324/) | · `gemma4it_d3v5_len12_swap` (no spec) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d3v4_swap_topics` | `d3v4_swap_topics` | sesterce-a100x4 | 21 Oct 19:28 | 1.58 | d94c169 |
| `d3v4_seed2_swap_27b` | `d3v4_seed2_swap_27b` | sesterce-a100x4 | 21 Oct 22:49 | 0.48 | d3315bc |
| `d3v4_seed3_swap_27b` | `d3v4_seed3_swap_27b` | sesterce-a100x4 | 22 Oct 17:21 | 0.33 | 6538445 |
| `qwen35_9b_d3v4_swap_r2` | `qwen35_9b_d3v4_swap_r2` | sesterce-a100x4 | 22 Oct 09:33 | 0.23 | 0c0c675 |
| `qwen35_9b_d3v4_seed2_swap` | `qwen35_9b_d3v4_seed2_swap` | sesterce-a100x4 | 22 Oct 19:15 | 0.21 | b23c331 |
| `qwen35_9b_d3v4_seed3_swap` | `qwen35_9b_d3v4_seed3_swap` | sesterce-a100x4 | 23 Oct 07:19 | 0.21 | c07e7cf |
| `qwen3_32b_d3v4_swap_r2` | `qwen3_32b_d3v4_swap_r2` | sesterce-a100x4 | 22 Oct 10:03 | 0.58 | 0c0c675 |
| `qwen3_32b_d3v4_seed2_swap` | `qwen3_32b_d3v4_seed2_swap` | sesterce-a100x4 | 22 Oct 17:10 | 0.26 | 6538445 |
| `qwen3_32b_d3v4_seed3_swap` | `qwen3_32b_d3v4_seed3_swap` | sesterce-a100x4 | 23 Oct 07:12 | 0.26 | c07e7cf |
| `olmo3_7b_instruct_d3v4_swap_fn` | `olmo3_7b_instruct_d3v4_swap_fn` | sesterce-a100x4 | 21 Oct 20:40 | 0.18 | dbc3a8d |
| `olmo3_7b_instruct_d3v4_seed2_swap` | `olmo3_7b_instruct_d3v4_seed2_swap` | sesterce-a100x4 | 21 Oct 23:09 | 0.11 | 80880cd |
| `olmo3_7b_instruct_d3v4_seed3_swap` | `olmo3_7b_instruct_d3v4_seed3_swap` | sesterce-a100x4 | 23 Oct 07:24 | 0.12 | c07e7cf |
| `muse30b_d3v4_swap` | `muse30b_d3v4_swap` | sesterce-a100x4 | 23 Oct 00:34 | 0.77 | 2dadb64 |
| `muse30b_d3v4_seed2_swap` | `muse30b_d3v4_seed2_swap` | sesterce-a100x4 | 23 Oct 01:24 | 0.62 | 2dadb64 |
| `muse30b_d3v4_seed3_swap` | `muse30b_d3v4_seed3_swap` | sesterce-a100x4 | 23 Oct 08:17 | 0.60 | c07e7cf |
| `gemma4it_d3v4_swap_v2_r2` | `gemma4it_d3v4_swap_v2_r2` | sesterce-a100x4 | 22 Oct 10:07 | 0.63 | 0c0c675 |
| `gemma4it_d3v4_seed2_swap` | `gemma4it_d3v4_seed2_swap` | sesterce-a100x4 | 22 Oct 20:00 | 0.62 | b23c331 |
| `gemma4it_d3v4_seed3_swap` | `gemma4it_d3v4_seed3_swap` | sesterce-a100x4 | 23 Oct 08:03 | 0.62 | c07e7cf |
| `olmo_hybrid_7b_d3v4_swap_fn` | `olmo_hybrid_7b_d3v4_swap_fn` | sesterce-a100x4 | 23 Oct 04:37 | 0.27 | 77b372b |
| `olmo_hybrid_7b_d3v4_seed2_swap` | `olmo_hybrid_7b_d3v4_seed2_swap` | sesterce-a100x4 | 23 Oct 04:16 | 0.19 | 77b372b |
| `qwen35_122b_d3v4_swap` | `qwen35_122b_d3v4_swap` | sesterce-h200x2 | 23 Oct 01:02 | 0.54 | 38eb5d4 |
| `qwen35_122b_d3v4_seed2_swap` | `qwen35_122b_d3v4_seed2_swap_b16` | sesterce-h200x2 | 23 Oct 02:59 | 0.55 | 54e7edd |
| `qwen35_122b_d3v4_seed3_swap` | `qwen35_122b_d3v4_seed3_swap_b16` | sesterce-h200x2 | 23 Oct 03:26 | 0.55 | 54e7edd |
| `d3v5_len8_swap_27b` | `d3v5_len8_swap_27b` | sesterce-a100x4 | 23 Oct 05:55 | 0.82 | 49c008c |
| `d3v5_len12_swap_27b` | `d3v5_len12_swap_27b` | sesterce-a100x4 | 23 Oct 05:45 | 0.53 | 49c008c |
| `qwen35_9b_d3v5_len8_swap` | `qwen35_9b_d3v5_len8_swap` | sesterce-a100x4 | 23 Oct 05:32 | 0.31 | 49c008c |
| `qwen35_9b_d3v5_len12_swap` | `qwen35_9b_d3v5_len12_swap` | sesterce-a100x4 | 23 Oct 05:33 | 0.20 | 49c008c |
| `qwen3_32b_d3v5_len8_swap` | `qwen3_32b_d3v5_len8_swap` | sesterce-a100x4 | 23 Oct 06:19 | 0.53 | 51ff150 |
| `qwen3_32b_d3v5_len12_swap` | `qwen3_32b_d3v5_len12_swap` | sesterce-a100x4 | 23 Oct 06:17 | 0.39 | 51ff150 |
| `olmo3_7b_instruct_d3v5_len8_swap` | `olmo3_7b_instruct_d3v5_len8_swap` | sesterce-a100x4 | 23 Oct 06:04 | 0.08 | 51ff150 |
| `olmo3_7b_instruct_d3v5_len12_swap` | `olmo3_7b_instruct_d3v5_len12_swap` (failed at figures, exit 1) | sesterce-a100x4 | 23 Oct 06:09 | 0.04 | 51ff150 |
| `muse30b_d3v5_len8_swap` | `muse30b_d3v5_len8_swap` | sesterce-a100x4 | 23 Oct 06:54 | 0.51 | 51ff150 |
| `muse30b_d3v5_len12_swap` | `muse30b_d3v5_len12_swap` | sesterce-a100x4 | 23 Oct 06:43 | 0.27 | 51ff150 |
| `olmo_hybrid_7b_d3v5_len8_swap` | `olmo_hybrid_7b_d3v5_len8_swap` | sesterce-a100x4 | 23 Oct 06:33 | 0.15 | 51ff150 |
| `olmo_hybrid_7b_d3v5_len12_swap` | `olmo_hybrid_7b_d3v5_len12_swap` | sesterce-a100x4 | 23 Oct 06:42 | 0.09 | 51ff150 |
| `qwen35_122b_d3v5_len8_swap` | `qwen35_122b_d3v5_len8_swap_b16` | sesterce-h200x2 | 23 Oct 05:14 | 0.76 | 54e7edd |
| `qwen35_122b_d3v5_len12_swap` | `qwen35_122b_d3v5_len12_swap_b16` | sesterce-h200x2 | 23 Oct 04:18 | 0.43 | 54e7edd |

## Finding 6: The order label counts order in the list, not place in the text

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| filler moved | ✓ [`d3v4x_swap_main`](results/pointer_swap/d3v4x_swap_main/) | ✓ [`qwen35_9b_d3v4x_swap_r2`](results/pointer_swap/qwen35_9b_d3v4x_swap_r2/) | ✓ [`olmo_hybrid_7b_d3v4x_swap`](results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/) | ✓ [`qwen35_122b_d3v4x_swap`](results/pointer_swap/qwen35_122b_d3v4x_swap/) | ✗ [`qwen3_32b_d3v4x_swap_r3`](results/pointer_swap/qwen3_32b_d3v4x_swap_r3/) | ✓ [`olmo3_7b_instruct_d3v4x_swap`](results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/) | ✓ [`muse30b_d3v4x_swap`](results/pointer_swap/muse30b_d3v4x_swap/) | ✓ [`gemma4it_d3v4x_swap_r2`](results/pointer_swap/gemma4it_d3v4x_swap_r2/) |
| one statement more | ✓ [`d3v4x_swap_main`](results/pointer_swap/d3v4x_swap_main/) | ✗ [`qwen35_9b_d3v4x_swap_r2`](results/pointer_swap/qwen35_9b_d3v4x_swap_r2/) | ✗ [`olmo_hybrid_7b_d3v4x_swap`](results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/) | ✓ [`qwen35_122b_d3v4x_swap`](results/pointer_swap/qwen35_122b_d3v4x_swap/) | ✗ [`qwen3_32b_d3v4x_swap_r3`](results/pointer_swap/qwen3_32b_d3v4x_swap_r3/) | ✗ [`olmo3_7b_instruct_d3v4x_swap`](results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/) | ✓ [`muse30b_d3v4x_swap`](results/pointer_swap/muse30b_d3v4x_swap/) | ✗ [`gemma4it_d3v4x_swap_r2`](results/pointer_swap/gemma4it_d3v4x_swap_r2/) |
| one statement fewer | ✓ [`d3v4x_swap_main`](results/pointer_swap/d3v4x_swap_main/) | ✗ [`qwen35_9b_d3v4x_swap_r2`](results/pointer_swap/qwen35_9b_d3v4x_swap_r2/) | ✗ [`olmo_hybrid_7b_d3v4x_swap`](results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/) | ✓ [`qwen35_122b_d3v4x_swap`](results/pointer_swap/qwen35_122b_d3v4x_swap/) | ✗ [`qwen3_32b_d3v4x_swap_r3`](results/pointer_swap/qwen3_32b_d3v4x_swap_r3/) | ✗ [`olmo3_7b_instruct_d3v4x_swap`](results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/) | ✓ [`muse30b_d3v4x_swap`](results/pointer_swap/muse30b_d3v4x_swap/) | ✗ [`gemma4it_d3v4x_swap_r2`](results/pointer_swap/gemma4it_d3v4x_swap_r2/) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d3v4x_swap_main` | `d3v4x_swap_main` | sesterce-a100x4 | 21 Oct 20:23 | 1.54 | 469ad9c |
| `qwen35_9b_d3v4x_swap_r2` | `qwen35_9b_d3v4x_swap_r2` | sesterce-a100x4 | 22 Oct 10:03 | 0.41 | 0c0c675 |
| `qwen3_32b_d3v4x_swap_r3` | `qwen3_32b_d3v4x_swap_r3` | sesterce-a100x4 | 23 Oct 02:23 | 0.96 | a5f0604 |
| `olmo3_7b_instruct_d3v4x_swap` | `olmo3_7b_instruct_d3v4x_swap` | sesterce-a100x4 | 21 Oct 20:57 | 0.29 | 84285f3 |
| `olmo_hybrid_7b_d3v4x_swap` | `olmo_hybrid_7b_d3v4x_swap` | sesterce-a100x4 | 23 Oct 05:10 | 0.54 | 77b372b |
| `muse30b_d3v4x_swap` | `muse30b_d3v4x_swap` | sesterce-a100x4 | 23 Oct 01:15 | 1.52 | 2dadb64 |
| `gemma4it_d3v4x_swap_r2` | `gemma4it_d3v4x_swap_r2` | sesterce-a100x4 | 22 Oct 11:22 | 0.96 | 0c0c675 |
| `qwen35_122b_d3v4x_swap` | `qwen35_122b_d3v4x_swap_b16` | sesterce-h200x2 | 23 Oct 04:24 | 1.19 | 54e7edd |

## The lens names a stated bridge where it is stated (lens gate)

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| v1 (at the word) | ✓ [`lens_gate_27b`](results/lens_gate/lens_gate_27b/)<br>plain J-lens: ✓ [`qwen36_27b_jlens_lens_gate_v2`](results/lens_gate/qwen36_27b_jlens_lens_gate_v2/) | ✓ [`qwen35_9b_lens_gate`](results/lens_gate/qwen35_9b_lens_gate/) | ⊘ no lens | ✓ [`qwen35_122b_lens_gate_v2`](results/lens_gate/qwen35_122b_lens_gate_v2/) | ✓ [`qwen3_32b_jpp_lens_gate`](results/lens_gate/qwen3_32b_jpp_lens_gate/)<br>plain J-lens: ✗ [`qwen3_32b_lens_gate`](results/lens_gate/qwen3_32b_lens_gate/) | ✓ [`olmo3_7b_instruct_jpp_lens_gate`](results/lens_gate/olmo3_7b_instruct_jpp_lens_gate/)<br>plain J-lens: ✓ [`olmo3_7b_instruct_lens_gate_v2`](results/lens_gate/olmo3_7b_instruct_lens_gate_v2/) | ✓ [`muse30b_lens_gate_v2`](results/lens_gate/muse30b_lens_gate_v2/) | ✓ [`gemma4itf_lens_gate_v2`](results/lens_gate/gemma4itf_lens_gate_v2/)<br>base-model J++: ✓ [`gemma4itb_lens_gate_v2_r2`](results/lens_gate/gemma4itb_lens_gate_v2_r2/) |
| v2 (after the word) | ✗ [`lens_gate_v2_27b`](results/lens_gate/lens_gate_v2_27b/)<br>plain J-lens: ✗ [`qwen36_27b_jlens_lens_gate_v2`](results/lens_gate/qwen36_27b_jlens_lens_gate_v2/) | ✗ [`qwen35_9b_lens_gate_v2`](results/lens_gate/qwen35_9b_lens_gate_v2/) | ⊘ no lens | ✗ [`qwen35_122b_lens_gate_v2`](results/lens_gate/qwen35_122b_lens_gate_v2/) | ✗ [`qwen3_32b_jpp_lens_gate`](results/lens_gate/qwen3_32b_jpp_lens_gate/)<br>plain J-lens: ✗ [`qwen3_32b_lens_gate_v2`](results/lens_gate/qwen3_32b_lens_gate_v2/) | ✗ [`olmo3_7b_instruct_jpp_lens_gate`](results/lens_gate/olmo3_7b_instruct_jpp_lens_gate/)<br>plain J-lens: ✗ [`olmo3_7b_instruct_lens_gate_v2`](results/lens_gate/olmo3_7b_instruct_lens_gate_v2/) | ✗ [`muse30b_lens_gate_v2`](results/lens_gate/muse30b_lens_gate_v2/) | ✗ [`gemma4itf_lens_gate_v2`](results/lens_gate/gemma4itf_lens_gate_v2/)<br>base-model J++: ✗ [`gemma4itb_lens_gate_v2_r2`](results/lens_gate/gemma4itb_lens_gate_v2_r2/) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `lens_gate_27b` | `lens_gate_27b` | sesterce-a100x4 | 22 Oct 19:41 | 0.01 | b7ad363 |
| `lens_gate_v2_27b` | `lens_gate_v2_27b` | sesterce-a100x4 | 22 Oct 20:45 | 0.01 | 2b0701f |
| `qwen36_27b_jlens_lens_gate_v2` | `qwen36_27b_jlens_lens_gate_v2` | sesterce-a100x4 | 22 Oct 21:20 | 0.01 | b51e964 |
| `qwen35_9b_lens_gate` | `qwen35_9b_lens_gate` | sesterce-a100x4 | 22 Oct 19:40 | 0.01 | b7ad363 |
| `qwen35_9b_lens_gate_v2` | `qwen35_9b_lens_gate_v2` | sesterce-a100x4 | 22 Oct 20:45 | 0.01 | 2b0701f |
| `qwen3_32b_jpp_lens_gate` | `qwen3_32b_jpp_lens_gate` | sesterce-a100x4 | 23 Oct 08:13 | 0.01 | 193c060 |
| `qwen3_32b_lens_gate` | `qwen3_32b_lens_gate` | sesterce-a100x4 | 22 Oct 19:42 | 0.01 | b7ad363 |
| `qwen3_32b_lens_gate_v2` | `qwen3_32b_lens_gate_v2` | sesterce-a100x4 | 22 Oct 20:45 | 0.01 | 2b0701f |
| `olmo3_7b_instruct_jpp_lens_gate` | `olmo3_7b_instruct_jpp_lens_gate` | sesterce-a100x4 | 23 Oct 08:13 | 0.01 | 2f3c320 |
| `olmo3_7b_instruct_lens_gate_v2` | `olmo3_7b_instruct_lens_gate_v2` | sesterce-a100x4 | 22 Oct 20:45 | 0.01 | 2b0701f |
| `muse30b_lens_gate_v2` | `muse30b_lens_gate_v2` | sesterce-a100x4 | 22 Oct 22:11 | 0.01 | 2dadb64 |
| `gemma4itf_lens_gate_v2` | `gemma4itf_lens_gate_v2` | sesterce-a100x4 | 22 Oct 21:18 | 0.01 | c2add04 |
| `gemma4itb_lens_gate_v2_r2` | `gemma4itb_lens_gate_v2_r2` | sesterce-a100x4 | 22 Oct 21:19 | 0.01 | c2add04 |
| `qwen35_122b_lens_gate_v2` | `qwen35_122b_lens_gate_v2` | sesterce-h200x2 | 22 Oct 23:54 | 0.10 | 38eb5d4 |

## Finding 7: A lens push writes a stated bridge for recall; the lookup does not follow

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| main rule | ≈ [`d4_where_fresh_27b`](results/early_push_where/d4_where_fresh_27b/) | ⚠ [`qwen35_9b_d4_where`](results/early_push_where/qwen35_9b_d4_where/) | ⊘ no lens | ✓ [`qwen35_122b_d4_where`](results/early_push_where/qwen35_122b_d4_where/) | · `qwen3_32b_jpp_d4_where` (running) | ✓ [`olmo3_7b_instruct_jpp_d4_where_raw`](results/early_push_where/olmo3_7b_instruct_jpp_d4_where_raw/) | ⚠ [`muse30b_d4_where`](results/early_push_where/muse30b_d4_where/) | · `gemma4itf_d4_where` (blocked) |
| amended rule | ✓ [`d4_where_fresh_27b`](results/early_push_where/d4_where_fresh_27b/) | ⚠ [`qwen35_9b_d4_where`](results/early_push_where/qwen35_9b_d4_where/) | ⊘ no lens | ✓ [`qwen35_122b_d4_where`](results/early_push_where/qwen35_122b_d4_where/) | · `qwen3_32b_jpp_d4_where` (running) | ✓ [`olmo3_7b_instruct_jpp_d4_where_raw`](results/early_push_where/olmo3_7b_instruct_jpp_d4_where_raw/) | ⚠ [`muse30b_d4_where`](results/early_push_where/muse30b_d4_where/) | · `gemma4itf_d4_where` (blocked) |
| main rule, draw 2 | ✓ [`d4_where_fresh_seed2_27b`](results/early_push_where/d4_where_fresh_seed2_27b/) | ✓ [`qwen35_9b_d4_where_fresh_seed2`](results/early_push_where/qwen35_9b_d4_where_fresh_seed2/) | ⊘ no lens | · `qwen35_122b_d4_where_fresh_seed2` (no spec) | · no spec | · no spec | · no spec | · no spec |
| amended rule, draw 2 | ✓ [`d4_where_fresh_seed2_27b`](results/early_push_where/d4_where_fresh_seed2_27b/) | ✓ [`qwen35_9b_d4_where_fresh_seed2`](results/early_push_where/qwen35_9b_d4_where_fresh_seed2/) | ⊘ no lens | · `qwen35_122b_d4_where_fresh_seed2` (no spec) | · no spec | · no spec | · no spec | · no spec |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d4_where_fresh_27b` | `d4_where_fresh_27b` | sesterce-a100x4 | 22 Oct 19:29 | 1.18 | a786b36 |
| `d4_where_fresh_seed2_27b` | `d4_where_fresh_seed2_27b` | sesterce-a100x4 | 23 Oct 03:46 | 1.15 | c07e7cf |
| `qwen35_9b_d4_where` | `qwen35_9b_d4_where` | sesterce-a100x4 | 22 Oct 21:09 | 0.39 | 2b0701f |
| `qwen35_9b_d4_where_fresh_seed2` | `qwen35_9b_d4_where_fresh_seed2` | sesterce-a100x4 | 23 Oct 03:26 | 0.39 | c07e7cf |
| `olmo3_7b_instruct_jpp_d4_where_raw` | `olmo3_7b_instruct_jpp_d4_where_raw` | sesterce-a100x4 | 23 Oct 08:57 | 0.36 | 2f3c320 |
| `muse30b_d4_where` | `muse30b_d4_where` | sesterce-a100x4 | 23 Oct 03:42 | 0.39 | 2dadb64 |
| `qwen35_122b_d4_where` | `qwen35_122b_d4_where_r2` | sesterce-h200x2 | 23 Oct 01:49 | 0.68 | 38eb5d4 |

## Finding 8: Where the lens writes the bridge, the lookup still does not follow it

| Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3.5-122B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it |
|---|---|---|---|---|---|---|---|---|
| stated bridge, draw 1 | ✓ [`d1_topics_rw_27b`](results/statement_positions/d1_topics_rw_27b/) | · no spec | ⊘ no lens | · no spec | ⚠ [`qwen3_32b_jpp_d1_topics_rw`](results/statement_positions/qwen3_32b_jpp_d1_topics_rw/)<br>plain J-lens: ✓ [`qwen3_32b_d1_topics_rw`](results/statement_positions/qwen3_32b_d1_topics_rw/) | · no spec | · no spec | · no spec |
| stated bridge, draw 2 | ✓ [`d1_topics2_rw_27b`](results/statement_positions/d1_topics2_rw_27b/)<br>plain J-lens: ✓ [`qwen36_27b_jlens_d1_topics2_rw`](results/statement_positions/qwen36_27b_jlens_d1_topics2_rw/) | ✓ [`qwen35_9b_d1_topics2_rw`](results/statement_positions/qwen35_9b_d1_topics2_rw/) | ⊘ no lens | ✗ [`qwen35_122b_d1_topics2_rw`](results/statement_positions/qwen35_122b_d1_topics2_rw/) | · no spec | · `olmo3_7b_instruct_jpp_d1_topics2_rw` (not run)<br>plain J-lens: · `olmo3_7b_instruct_d1_topics2_rw` (not run) | · `muse30b_d1_topics2_rw` (not run) | · `gemma4itf_d1_topics2_rw` (pending)<br>base-model J++: · `gemma4itb_d1_topics2_rw` (not run) |
| last tokens | ○ [`d3v4_fit_main`](results/pointer_fit/d3v4_fit_main/) | ○ [`qwen35_9b_d3b_fit_v2`](results/pointer_fit/qwen35_9b_d3b_fit_v2/) | ⊘ no lens | ○ [`qwen35_122b_d3b_fit_v2`](results/pointer_fit/qwen35_122b_d3b_fit_v2/) | ○ [`qwen3_32b_jpp_d3b_fit_v2`](results/pointer_fit/qwen3_32b_jpp_d3b_fit_v2/) | ○ [`olmo3_7b_instruct_jpp_d3b_fit_v2`](results/pointer_fit/olmo3_7b_instruct_jpp_d3b_fit_v2/)<br>plain J-lens: ○ [`olmo3_7b_instruct_d3b_fit_v2`](results/pointer_fit/olmo3_7b_instruct_d3b_fit_v2/) | · no spec | · `gemma4itf_d3b_fit_v2` (blocked) |

Jobs behind these runs (queue ledgers; finished in UTC; the commit the spec was enqueued at):

| Run | Job | Box | Finished | GPU-hours | Spec commit |
|---|---|---|---|---|---|
| `d1_topics_rw_27b` | `d1_topics_rw_27b` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 16:54 | 0.10 | 3e90959 |
| `d1_topics2_rw_27b` | `d1_topics2_rw_27b` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 20:53 | 0.15 | a786b36 |
| `qwen36_27b_jlens_d1_topics2_rw` | `qwen36_27b_jlens_d1_topics2_rw_q` | sesterce-a100x4 | 23 Oct 01:33 | 0.15 | 2dadb64 |
| `qwen35_9b_d1_topics2_rw` | `qwen35_9b_d1_topics2_rw` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 19:03 | 0.06 | a786b36 |
| `qwen3_32b_jpp_d1_topics_rw` | `qwen3_32b_jpp_d1_topics_rw` | sesterce-a100x4 | 23 Oct 08:51 | 0.19 | 193c060 |
| `qwen3_32b_d1_topics_rw` | `qwen3_32b_d1_topics_rw` (failed at figures, exit 1) | sesterce-a100x4 | 22 Oct 17:08 | 0.19 | 3e90959 |
| `qwen35_122b_d1_topics2_rw` | `qwen35_122b_d1_topics2_rw_r3` | sesterce-h200x2 | 23 Oct 02:41 | 0.26 | 4a87d79 |
| `d3v4_fit_main` | `d3v4_fit_main` | sesterce-a100x4 | 21 Oct 16:06 | 0.40 | a15cd0b |
| `qwen35_9b_d3b_fit_v2` | `qwen35_9b_d3b_fit_v2` | sesterce-a100x4 | 23 Oct 02:25 | 0.10 | 0a8820d |
| `qwen3_32b_jpp_d3b_fit_v2` | `qwen3_32b_jpp_d3b_fit_v2` | sesterce-a100x4 | 23 Oct 08:30 | 0.23 | 193c060 |
| `olmo3_7b_instruct_jpp_d3b_fit_v2` | `olmo3_7b_instruct_jpp_d3b_fit_v2` | sesterce-a100x4 | 23 Oct 08:35 | 0.08 | 2f3c320 |
| `qwen35_122b_d3b_fit_v2` | `qwen35_122b_d3b_fit_v2_b16` | sesterce-h200x2 | 23 Oct 07:24 | 0.23 | 54e7edd |
| `olmo3_7b_instruct_d3b_fit_v2` | `olmo3_7b_instruct_d3b_fit_v2` | sesterce-a100x4 | 21 Oct 22:24 | 0.07 | 6149001 |
