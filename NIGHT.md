# Night 29-30 Oct: 122B coverage (Dan 18:20)

Plan verbatim: [jobs/c3/batch53.yaml](jobs/c3/batch53.yaml) `coverage_122b_1820` (and `decisions_1810`). Box: mats (`sesterce-h100x2`, 2x H100) only. Every run: rule verbatim from its spec, no prediction, UNVERIFIED, "coverage, not hand-checked"; the README is not touched by these results until after the 30 Oct check.

## Before launch

- Pull (Dan 18:10 item 4), report `cache/box_backup/pull_20261029T172050Z.md`: no new run dirs were missing on the Mac (the report's "5 new run dirs" lines are a stale listing from the 18:00 pull, not new); box files missing or differing locally (mats 9 new + 1,415 differing, mostly mtime; another 3 new + 3 differing; speedup none) copied to `cache/box_backup/<box>/results/`; inspector states, full copies in `cache/box_backup/<box>/review_states/` (mats: 122B; speedup: Lightning; another: 9B, 27B, Muse) and missing files added to `cache/review_states/`; monitor states are inside `results/x53_monitor/` (all local).
- speedup and another: queues empty, pulled; ready to stop (cannot hold the 122B in FP8). Not stopped by me: no API on the Mac; Dan stops them in the Sesterce console.

## Queue on mats (in Dan's order)

| # | Test | Job | Status | Results |
|---|---|---|---|---|
| 1 | conflict test, every 4th layer L1-L45, decided at L33 | x53c_conflict_sweep_122b | running (started 18:22) | results/x0_necessity/qwen35_122b_x53c_conflict/ |
| 2 | 47.0 lens readout of an address swap; adapted design: lookup-only gate (Dan 18:45; the recall 0.797 not part of this test; not hollow) | x47_0_122b | queued right after 52 A | results/x47_verbal/qwen35_122b_x47_verbal/ + summary-<UTC>/ |
| 3 | 52 A atoms of the lens part (E1 only; Z2 not run: no Z2 run on the 122B) | x52_atoms_122b | queued | results/x52_atoms/qwen35_122b_x52_atoms_fwd/ |
| 4 | 53.2 verdict for the 122B (CPU, Mac) | probes (cache/x53_monitor/qwen35_122b_x53_monitor/) + verdict | done 18:52, de7354c7; ledger 53.2 addendum | results/x53_monitor/x53_monitor_122b-20261029T175223Z/ |
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
- 18:3x x45m_122b (input of 49.2 / 45p) and x49_2_122b queued.
- 18:45 Dan: 47.0 option (b), lookup-only gate; x47_0_122b queued and moved right after 52 A (pending file renamed on the box). speedup and another stopped by Dan. Wakes every 2 h (21:13, 23:13, 01:13, 03:13, 05:13, 07:13): enqueue only if buffer < 2 or a job failed; one line here per wake.
- 21:00 queue on mats empty since 20:29 (all 8 jobs exit 0; pulled and committed 138c671d, not yet in the ledger); deck brief done (7b68b910); next 122B specs (47.1, Z1/Z1-P, 47.2, 45p, 53.7) at the next wake.
- 21:49 wake: queue was empty; queued x47_1_122b (running), x50_z1_122b, x47_2_122b; night runs (8) + 53.2 into the ledger section 'The 122B coverage, night 29-30 Oct' (check_ledger 0 problems); conflict sweep: split only at L33, lookup 'through' at L13-L21.
- 23:29 Dan asked to write the last two now: x45p_122b and x53_7_probe_122b queued (behind Z1 running, 47.2 pending); every item of Dan's 18:20 list is now queued or done.
- 23:33 deck figures + outline committed (4f85f28e); queue: see make queue-status (Z1 then 47.2, 45p, 53.7).
- 23:44 wake: running x47_2_122b; pending x45p_122b, x53_7_probe_122b; done x47_1_122b (routes part not tested: recall 0.797 < 0.80; main slices descriptive), x50_z1_122b (Z1 in between at L33, Z1-P split holds); pulled, ledger lines added.
- 00:22 x45p_122b failed at its first line (my bug: stage_run's assert knew RUN_45M only); fixed, requeued as x45p_122b_r2 behind x53_7_probe_122b (running). x47_2_122b done (exit 0), not yet pulled.
