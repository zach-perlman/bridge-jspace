# figures/deck: captions and n

Built by scripts/deck_figures.py.

- **c0_setup_a**: figures/shared/j0_setup.png, the two datasets (cut at half height; no content change).
- **c0_setup_b**: figures/shared/j0_setup.png, the tools (cut at half height; no content change).
- **c1_controls**: docs/breadth/data.csv ko.{q27,q9,nl}.{mk,pc,u,rot} (27B n = 892; 9B n = 563; Lightning n = 563); figures/story/data.csv fig02 rows (main test at L; Lightning has no fig02 row: left out). Whiskers 95%.
- **c2_pointer**: docs/breadth/data.csv ptr.{q27,q9,nl}.{swap,neutral,noown,rot} and probe.*.{probe,swap}; the neutral-sentence and own-word rows are the same-passage swap times their stored ratios (computed here, no CI); the probe rows are on probe-valid relations. figures/story/data.csv 52 A rows (50 main-test scenes per model; the 122B: no 52 A row, left out; Lightning hatched).
- **c3_address**: figures/story/data.csv: fig07 (probe 657-758 scenes, swap 600 per dose and model; Lightning hollow; the 122B hollow in (B): its gate lowered after the data), fig21_code_tool (the 27B's code 682 and tool 1,500 scenes), fig07b_verbal (200 cases; the 122B has no 47.0 row in the depth README: left out). Random vector at s = 4: the grey band in (B).
- **c4_readable**: figures/story/data.csv fig17_jspace_last_token rows (locker-first items; the 122B not run in the depth README: left out; Lightning hatched); docs/shared/grid.csv, breadth study cells of the two claims. 'Readable at the mention' (all nine) has no row in the CSVs: not drawn.
- **c9_breaks**: figures/story/data.csv fig02b (main test, 200 scenes) and ledger_zach_named (his named passages; Lightning's gate chosen after its pre-check; Muse and Lightning missed the made-up-fact gate: descriptive). The question-order panel moved to the appendix (A18).
