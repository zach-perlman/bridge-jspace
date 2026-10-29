# Night 29-30 Oct: 122B coverage (Dan 18:20)

Plan verbatim: [jobs/c3/batch53.yaml](jobs/c3/batch53.yaml) `coverage_122b_1820` (and `decisions_1810`). Box: mats (`sesterce-h100x2`, 2x H100) only. Every run: rule verbatim from its spec, no prediction, UNVERIFIED, "coverage, not hand-checked"; the README is not touched by these results until after the 30 Oct check.

## Before launch

- Pull (Dan 18:10 item 4), report `cache/box_backup/pull_20261029T172050Z.md`: no new run dirs were missing on the Mac (the report's "5 new run dirs" lines are a stale listing from the 18:00 pull, not new); box files missing or differing locally (mats 9 new + 1,415 differing, mostly mtime; another 3 new + 3 differing; speedup none) copied to `cache/box_backup/<box>/results/`; inspector states, full copies in `cache/box_backup/<box>/review_states/` (mats: 122B; speedup: Lightning; another: 9B, 27B, Muse) and missing files added to `cache/review_states/`; monitor states are inside `results/x53_monitor/` (all local).
- speedup and another: queues empty, pulled; ready to stop (cannot hold the 122B in FP8). Not stopped by me: no API on the Mac; Dan stops them in the Sesterce console.

## Queue on mats (in Dan's order)

| # | Test | Job | Status | Results |
|---|---|---|---|---|
| 1 | conflict test, every 4th layer L1-L45, decided at L33 | x53c_conflict_sweep_122b | running (started 18:22) | results/x0_necessity/qwen35_122b_x53c_conflict/ |
| 2 | 47.0 lens readout of an address swap | — | held: question to Dan (its items come from the 122B's x8_write run, gated at 0.75; recall read 0.797 < 0.80, lookup 1.00) | — |
| 3 | 52 A atoms of the lens part (E1 only; Z2 not run: no Z2 run on the 122B) | x52_atoms_122b | queued | results/x52_atoms/qwen35_122b_x52_atoms_fwd/ |
| 4 | 53.2 verdict for the 122B (CPU, Mac) | probe passes base / erand / fixed running on the Mac | running | cache/x53_monitor/qwen35_122b_x53_monitor/, then verdict --models qwen3.5-122b-a10b --prefix x53_monitor_122b |
| 5 | 51.1 dose curves | x51_1_122b | queued | results/x51_dose/qwen35_122b_x51_1/ + x52_dose-<UTC>/ |
| 5 | 47.5 zeroing | x47_5_122b | queued | results/x47_zero/qwen35_122b_x47_5/ + x52_zero-<UTC>/ |
| 5 (input) | 45m clean one-pick design, the item source of 49.2 and 45p (none on the 122B yet; its own gate 0.80) | x45m_122b | queued | results/x0_necessity/qwen35_122b_x45m_fresh/ |
| 5 | 49.2 ladder (rung 6 in L39-45), after x45m_122b | x49_2_122b | queued | results/x49_ladder/qwen35_122b_x49_2/ + x52_ladder-<UTC>/ |
| 5 | 47.1 identity outside the lens | — | spec next | — |
| 6 | Z1, Z1-P; 47.2; 45p; 53.7 code probe | — | specs after item 5 | — |

## Log

- 18:20 autonomy window to 08:30; pull started.
- 18:22 item 1 started on mats.
- 18:2x Dan 18:10 decisions 1-3 committed (c7ca2e86): 53.8 card, rank check range (ledger + depth README), fig11 footnote.
- 18:3x items 3, 5 (51.1, 47.5) queued. Helper agents for the remaining specs stopped on the spend limit; specs written in the main session.
