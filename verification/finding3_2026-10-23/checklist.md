# Finding 3: what to check by hand (30-60 minutes)

Run everything from the repo root. No GPU. Nothing here writes to `results/`.

## Checks

1. **The recompute (5 min).** `python3 verification/finding3_2026-10-23/recompute.py`. Expect the last line "45 cells recomputed, 45 match grid.csv, 0 mismatch", and 3 "no run" lines (27B, Olmo-Hybrid, 122B draw 3). The same with `--grid=20261023T104743Z` (the newer grid; this finding's rows are unchanged there). The script uses only the standard library; read `counts` and `judge` (20 lines) against the rule quoted in claim.md.
2. **One cell by hand (10 min).** Qwen3.6-27B, draw 1, run `results/attn_knockout/d2_parts_v2_27b/`. In `rows.jsonl`, take `family == "RL"`, `layers == "all"`, `source == "lookup_noname"`, `dest == "final"` (300 rows; every RL item is right unedited) and count rows with `correct == true`. It should be 33 of 300 = 11.0%, Wilson [7.9, 15.0]. The same with `lookup_nodigit` should be 263 of 300 = 88%. The plain-python snippet in `verification/finding3_name_vs_digit.md`, section 3, does this in 15 lines.
3. **The worked example (5 min).** `grep '"body-RL-e5f0-0103"' results/attn_knockout/d2_parts_v2_27b/rows.jsonl | grep '"RL"'`. Unedited `top` is 20 (the token "5"); `lookup_noname`/`final` has `top` 22 ("7"); `lookup_nodigit`/`final` has `top` 20. Token ids: in that item's `cases.jsonl` line, `tok_A` = 20 and `conf_toks` holds the other four digits.
4. **What exactly is hidden (5 min).** In the same `cases.jsonl` line, `sources.lookup` = positions 12-20 (the sentence, 9 tokens), `sources.lookup_name` = [13] ("ankle"), `sources.lookup_digit` = [19] ("5"); `lookup_noname` = 12-20 without 13, `lookup_nodigit` = 12-20 without 19. Both conditions hide 8 of the sentence's 9 tokens: the asymmetry is not the size of the hole (names of several tokens make the no-name hole a little smaller).
5. **The hook did nothing when nothing is hidden (2 min).** `check.json` of any run: `passed: true` and `noop_empty_source_max_abs: 0.0`. Checked by script on all 57 runs of findings 3 and 4: all pass.
6. **The grid's control text for the not-interpretable cells (5 min).** grid.csv, Olmo-Hybrid-7B, prose: the text says "off-path parts hidden: lowest 100%", yet the verdict is not interpretable. The recompute shows why: the off-path parts hidden from the question's tokens keep 86% (from the last tokens 100%). The grid's text reports the last tokens only (`scripts/cross_model_grid.py` `parts_row`: the dict of off-path rates is keyed by source, so the question destination is overwritten). The verdicts are right; the text is incomplete. Same for Olmo-Hybrid JSON (86% / 93%).
7. **Chance in prose, tables and JSON (5 min).** Those scenes (Zach's generator, `data/tasks_v2/d2_formats_v1`) have 3 facts, not 5: every memory -> prompt line of `d2_formats_27b/cases.jsonl` has 2 `conf_answers`, so guessing is 33%, not 20%. The 35% bar is then at chance. Gemma prose (34%, n=35) holds by 1 point; read the format cells as "the digit hidden drops the lookup to about guessing, the name hidden does not".
8. **Gemma (5 min).** 27-29% right with the digit hidden on all three draws (bar 35%), against 86-89% with the name hidden. It holds, but less sharply than the other seven models (0-11%).
9. **Qwen3-32B draws 2 and 3: n = 199 (2 min).** Animals missed the memory -> prompt competence gate (by 0.0005 on draw 2), so only countries and body parts count. A post-hoc animals run (`qwen3_32b_d2_parts_seed2_animals`) is not in the grid. Check `cases_report.json` of `qwen3_32b_d2_parts_seed2`.

## Three dumbest ways this could be wrong

1. **Any hole of that size in the answer's sentence breaks the read.** Checked: the same parts of another sentence hidden keep 99-100% on every draw cell, and the two decisive conditions hide almost the same number of tokens (check 4).
2. **"Right" is mislabelled, or the digit is read from elsewhere in the prompt.** Checked by script: `correct` equals (`top == tok_A`) on all 1,089,871 rows of the 56 runs of findings 3-4. The answer's digit occurs once in every sentence-list prompt except on Muse, whose system prompt carries dates ("2026-10-23"); there about 10% of prompts contain the answer digit twice, and Muse's rates with the digit hidden are still 1-3%. In the format scenes written with number words the digit token never occurs (the model converts "seven" to 7): by design.
3. **The rule was fitted after seeing the data.** The decisive pair (sentence without name / without digit) was added at 5cb6a87 before any of these results were read (the commit message and spec say so; check `git show 5cb6a87 --stat`). The format rule is in `jobs/d2/d2_formats_27b.yaml` at 444500e, before those runs; its scoring script `scripts/d2_formats.py` was committed later (42e0fdd, 22 Oct 22:27 +0200), after the 27B and 32B format runs had finished (README, "Runs": 18:44 and 18:56 UTC).

## Known deviations

- Draw 3 does not exist for the 27B, Olmo-Hybrid and 122B (no spec).
- Small n in prose, tables and JSON on the OLMos and Muse (5-24 items per cell); three of those cells are not interpretable and Muse prose fails on 5 items (2 of 5 right).
- Muse answers no table or JSON scene right: not testable.
- Gemma is weaker (27-34%) than every other model.
- Only memory -> prompt decides; named -> prompt and the question's tokens are reported, not decisive (the grid's control text says "the question's tokens read the name: holds / fails / not testable" per cell; on Olmo-Hybrid it fails).
