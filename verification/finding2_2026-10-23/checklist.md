# Finding 2 on Qwen3.6-27B: what to check by hand (30-45 minutes)

Run everything from the repo root. No GPU. Nothing here writes to `results/`.

## Checks

1. **The recompute (5 min).** `python3 verification/finding2_2026-10-23/recompute.py`. Expect "11 cells recomputed, 11 match grid.csv, 0 mismatch"; the same with `--grid=20261023T104743Z` (the newer grid, which also prints the same-share random part). Read `load`, `block` and `judge` (20 lines) against the rule in claim.md.
2. **One cell by hand (10 min).** `results/statement_positions/d1_topics2_parts_27b/outcomes.jsonl`, rows with `source == "cf"`, `null == false`, `set == "context"`, `layer == 32`. Family PP, part `jspace`: 180 rows, 1 with `role == "b"` (0.6%). PP `not_jspace`: 145 of 180 (81%). PM `jspace`: 69 of 180 (38%), the positive control (needs >= 30%).
3. **The worked example (5 min).** `grep '"PP-L0-0150"' results/statement_positions/d1_topics2_parts_27b/outcomes.jsonl | grep '"context"' | grep '"layer": 32'`: part `full` and `not_jspace` give `top_text` "5" (role b), `jspace` and `jspace_matched` give "3" (role A). Then the same for `"PM-L0-0150"`. The prompts are the `PP-L0-0150` and `PM-L0-0150` lines of `data/tasks_v2/d1_topics_v2/items.jsonl` (`context`, `cf_context`, `answer`, `cf_answer`).
4. **The decisive cell was not chosen with the lens (5 min).** Draw 2 and the plain J-lens run: `--cell context:32` is in the specs (`jobs/d1/d1_topics2_parts_27b.yaml`, a786b36), fixed before they ran. Draw 1 and the formats: chosen from the lens-free map by the amended rule; the saved `verdict.json` `cell` field shows `context`, 32, and the map's whole-copy flips (85% on draw 1, 97% on the formats). The recompute takes the cell as given; re-deriving it needs the map runs' `summary.json` (`d1_topics_map_27b`).
5. **Only items the model answers right (2 min).** The parts stage ran only on scenes right on every prompt (spec `n:` and the competence runs named in each manifest's `tasks`). Every PP row at the cell under `full` that does not switch is a scene where even the whole change did not move the lookup (16-17% on the draws).
6. **The lens (2 min).** `results/statement_positions/d1_topics2_parts_27b/manifest.json`, field `lens`: the published J++ for Qwen3.6-27B, sha256 starting bbef480b (README, Lens table). The plain J-lens run uses 1718c8c5.
7. **The plain J-lens (5 min).** Same lookups result (0%), but its lens part switches only 18% of recalls (elements 15%, Greek letters 8%; animals 37%): without a working positive control a 0% on lookups says nothing. The grid lists it beside the main lens, never in its place.

## Three dumbest ways this could be wrong

1. **The lens part is too small to switch anything.** Checked with the recall control: the same lens part switches 36-42% of recalls, while the same-share random part switches 0-2%. Not checked here: the share of the change's norm the lens part carries (`fve.jsonl` in the run folder, `what == "jspace"`).
2. **The lookup is simply hard to move at that cell.** Checked: the whole change switches 83-98% of lookups and the rest alone 81-96%.
3. **A choice after the data.** The cell rule was amended (17:36 +0200, 22 Oct) after the map stages started and before any parts result was opened (spec text); draw 2 fixed the cell in advance; the formats rule was written before those runs. "Counting a topic only when its own recall control passes" is stricter than the pre-registered pooled rule (README, "Choices made after seeing the data").

## Known deviations

- Qwen3.6-27B only in this packet. On Qwen3.5-122B this finding fails (29% of lookups switched; tables 49%, JSON 34%) and on Qwen3-32B its control fails (README, finding 2).
- One cell (the context at layer 32) per run; other transit cells are reported in the run's summary, not decisive.
- The draw-1 topic split has no per-topic verdict (that run predates the per-topic rule).
- `scripts/d1_verdict.py` has uncommitted edits in the working tree today; this packet read the committed version (HEAD) for the rule.
