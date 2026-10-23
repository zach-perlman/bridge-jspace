# Finding 4: what to check by hand (30-60 minutes)

Run everything from the repo root. No GPU. Nothing here writes to `results/`.

## Checks

1. **The recompute (5 min).** `python3 verification/finding4_2026-10-23/recompute.py`. Expect "51 cells recomputed, 51 match grid.csv, 0 mismatch" and 5 "no run" lines. The same with `--grid=20261023T104743Z` (the newer grid; this finding's rows are unchanged there). Read `cell` and `judge` (25 lines) against the rule quoted in claim.md.
2. **One cell by hand (10 min).** Qwen3.6-27B, draw 2, `results/attn_knockout/d2_late_read_seed2_27b/rows.jsonl`: `family == "RL"`, `source == "lookup"`, `dest == "final"`, `layers == "attn"`. Count `correct == true`: 22 of 300 = 7.3%, Wilson [4.9, 10.9]. With `source == "lookup_off"`: 300 of 300. With `source == "lookup"`, `layers == "gdn"`: 300 of 300.
3. **The worked example (5 min).** `grep '"body-RL-e5f0-0099"' results/attn_knockout/d2_late_read_seed2_27b/rows.jsonl`: unedited and the three control rows have the answer's token, the `lookup`/`final`/`attn` row has another list digit. In that item's `cases.jsonl` line, `sources.lookup` must decode to "The ankle chart is in folder 8." (`source_text`).
4. **Which layers are "attention" (5 min).** In `results/attn_knockout/d2_late_read_seed2_27b/manifest.json`, the attention layer set must be exactly the layers whose kind is full attention (16 of the 27B's 64), the DeltaNet set the other 48. The older packet (`verification/finding4_late_read.md`, section 4) names the fields.
5. **The hook (2 min).** `check.json`: `passed: true`, `noop_empty_source_max_abs: 0.0`. Checked by script on all 57 runs of findings 3 and 4: all pass.
6. **Chance in prose, tables and JSON (5 min).** grid.csv writes "chance 20%" for every cell, but the format scenes have 3 facts: every memory -> prompt line of `results/attn_knockout/d2_formats_27b/cases.jsonl` has 2 `conf_answers`, so guessing is 33%. The 20% bar is therefore stricter there than on the lists, and Gemma's JSON cell (21% [13, 34], footnoted "at chance" in README) is below chance, not at it; Gemma prose (34%) is at chance. A labelling slip in the grid, not a verdict change. Grid `20261023T105852Z` (30c6418) gives chance per run (33% for these cells); `recompute.py --grid=20261023T105852Z`: 51 of 51 match.
7. **The 27B with a long context (5 min).** `results/attn_knockout/d2_late_read_long_27b_r3/`: 46 of 178 right with the read blocked (25.8%, [20.0, 32.7]); the DeltaNet layers blocked instead keep 178 of 178. The lookup still drops from 100% to about guessing; it fails only the "below chance" bar.
8. **Olmo-Hybrid tables (5 min).** `results/attn_knockout/olmo_hybrid_7b_d2_formats/`, `family == "MP"`, table items (`cases.jsonl` `wording` starts with "table"): attention blocked 0 of 24 right, DeltaNet layers blocked instead 21 of 24 (88%). The one cell where the DeltaNet layers matter at all; 24 items.
9. **The not-interpretable format cells are small-n, not failed controls (2 min).** Olmo-Hybrid prose: the off-path sentence blocked keeps 14 of 14 (100%), but the Wilson lower bound of 14/14 is 78% < 85%. Same pattern for Olmo-Hybrid JSON (13/14), OLMo-3 JSON (16/16), Muse prose (5/5); OLMo-3 prose keeps 16 of 18 (89%).

## Three dumbest ways this could be wrong

1. **Blocking breaks the model in general, not one read.** Checked: another sentence of the same token length blocked at the same layers keeps 98-100% on every draw cell; on the hybrids, the answer's sentence blocked in the DeltaNet layers instead keeps 99-100% (draws).
2. **"Drops to guessing" is a collapse onto one answer or off the list.** Checked by script: 96% of the wrong answers under the block (6,026 of 6,282, all cells) are another digit of the list.
3. **The first draws were judged by a rule written after they ran.** True, and stated: the draw-1 runs ran under the older per-topic rule; the grid applies the 22 Oct rule to them (Dan accepted, 23 Oct). Draws 2 and 3 ran after that rule was fixed and give the same picture (all hold except Gemma draw 2). Check: `git show 6538445 -- jobs/d2/d2_late_read_seed2_27b.yaml`.

## Known deviations

- Draw 1 judged by the rule fixed on 22 Oct for the second draws (README footnotes 11-19).
- Gemma stays near chance (19-23% on the lists) rather than below it: 2 of 3 draws fail the 20% bar; prose and JSON fail too.
- The 27B with a long context: 26%, at chance.
- Small n in the formats on the OLMos and Muse (5-24 items); five not interpretable by the lower-bound part of the off-path control.
- Muse answers no table or JSON scene right: not testable.
- Recall (memory -> memory) stays right under the block by construction (the blocked sentence is not on its path): a control, not part of the finding.
