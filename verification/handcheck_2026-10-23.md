# Hand-check sheet, 23 Oct 2026: one number per claim in 10 minutes

For Dan, tonight's TA call. Three checks: claims 1-2 of the README (the late read and the digit), claim 3 (order label, then identity) and the Qwen3.6-27B part of claim 6 (the lens-readable part moves recall, not the lookup). Each uses the run behind the README's number for that claim, on Qwen3.6-27B. For each: 10 rows drawn with a fixed seed, what to grep, what the model answered, and which count the row adds to; then one recompute command and the headline with its n. Everything comes from runs already opened (grid `results/cross_model/20261023T105852Z`, the one README cites); nothing new was run. The longer packets are `verification/finding{2,3,4,5}_2026-10-23/`. Nothing here is verified until a person adds it to VERIFIED.md.

Seed: `random.Random(1023)`, drawing from the sorted item ids (details per check). Run commands from the repo root.

How to use it in 10 minutes: for each check, grep two or three rows and compare with the table (1-2 minutes), then run the recompute command and read the one line named (1-2 minutes).

## 1. The last tokens read the answer's sentence late, through attention, and take its digit (README claims 1-2)

Runs (Qwen3.6-27B, second draw of scenes; both rules were fixed before these runs): `results/attn_knockout/d2_late_read_seed2_27b/` (claim 1) and `results/attn_knockout/d2_parts_seed2_27b/` (claim 2). Items: memory -> prompt (the bridge is recalled from a cue), answered right unedited, present in both runs (294 of each run's 300); 10 drawn with `random.Random(1023).sample(sorted(ids), 10)`, listed in the order drawn.

What to grep (replace ID):

- Claim 1: `grep -E '"id": "ID".*"source": "(none|lookup)", "dest": "(-|final)", "layers": "(-|attn)"' results/attn_knockout/d2_late_read_seed2_27b/rows.jsonl` gives 2 lines: unedited (`"source": "none"`) and the answer's sentence blocked from the last tokens in every attention layer (`"source": "lookup"`).
- Claim 2: `grep -E '"id": "ID".*"source": "lookup_no(name|digit)", "dest": "final"' results/attn_knockout/d2_parts_seed2_27b/rows.jsonl` gives 2 lines: `lookup_noname` (the sentence hidden except its name, so the digit is hidden) and `lookup_nodigit` (the sentence hidden except its digit).
- Read `"correct"` (true = right) and `"top"` (the answer token; on the Qwen models the digit d is token id 15 + d, so 18 = "3").

| Item | Answer's sentence | Unedited | Read blocked (claim 1) | adds to 22/300 | Digit hidden, name visible (claim 2) | adds to 30/300 | Name hidden, digit visible | adds to 263/300 |
|---|---|---|---|---|---|---|---|---|
| `countries-RL-e5f0-0056` | The Lebanon file is in drawer 7. | 7 | 4 (wrong) | 0 | 4 (wrong) | 0 | 7 (right) | 1 |
| `countries-RL-e5f0-0037` | The file on Germany is kept in drawer 1. | 1 | 1 (right) | 1 | 1 (right) | 1 | 1 (right) | 1 |
| `countries-RL-e5f0-0050` | The file on Canada is kept in drawer 7. | 7 | 4 (wrong) | 0 | 4 (wrong) | 0 | 7 (right) | 1 |
| `animals-RL-e5f0-0066` | The cow keeps its things in locker 3. | 3 | 1 (wrong) | 0 | 1 (wrong) | 0 | 3 (right) | 1 |
| `countries-RL-e5f0-0022` | Drawer 5 holds the Canada file. | 5 | 2 (wrong) | 0 | 2 (wrong) | 0 | 2 (wrong) | 0 |
| `body-RL-e5f0-0065` | The chart on the eye is kept in folder 9. | 9 | 9 (right) | 1 | 9 (right) | 1 | 9 (right) | 1 |
| `animals-RL-e5f0-0002` | Locker 5 belongs to the mosquito. | 5 | 1 (wrong) | 0 | 1 (wrong) | 0 | 5 (right) | 1 |
| `countries-RL-e5f0-0020` | The Russia file is in drawer 6. | 6 | 4 (wrong) | 0 | 4 (wrong) | 0 | 6 (right) | 1 |
| `body-RL-e5f0-0083` | The chart on the tongue is kept in folder 3. | 3 | 1 (wrong; token 16, not a digit of the list) | 0 | 3 (right) | 1 | 3 (right) | 1 |
| `body-RL-e5f0-0092` | The knee chart is in folder 5. | 5 | 8 (wrong) | 0 | 8 (wrong) | 0 | 5 (right) | 1 |

These 10 rows: 2, 3 and 9 right in the three columns.

Recompute:

- `python3 verification/finding4_2026-10-23/recompute.py --grid=20261023T105852Z`, line "Qwen3.6-27B draw 2": **claim 1: 22 of 300 right = 7.3% [4.9, 10.9]** with the read blocked (chance 20%: 5 digits per list). Controls on the same line: another sentence blocked keeps 300/300, the DeltaNet layers blocked instead keep 300/300. Verdict holds.
- `python3 verification/finding3_2026-10-23/recompute.py --grid=20261023T105852Z`, line "Qwen3.6-27B draw 2": **claim 2: 30 of 300 right = 10.0% [7.1, 13.9]** with the digit hidden (name visible), against 263 of 300 = 88% with the name hidden (digit visible). Verdict holds.

## 2. An order label picks the 1st and 2nd sentence; the bridge's identity picks the rest (README claim 3)

Run: `results/pointer_swap/d3v4_seed2_swap_27b/` (Qwen3.6-27B, second draw; the README's "+94 / +18"), the donor's last two tokens copied into the original at layer 50. Prompts: `data/pointer_v4/seed2/<topic>_RL_e5f0.json`. Items: memory -> prompt; 5 with the donor asking its 1st or 2nd sentence (k = 1-2), then 5 with k = 3-5, drawn with one `random.Random(1023)`: `sample(sorted(ids with k <= 2), 5)` then `sample(sorted(ids with k >= 3), 5)`.

What to grep (replace ID):

- `grep -E '"name": "ID".*"layer": (50|-1), "group": "(last|-)", "source": "(dissoc|unedited)"' results/pointer_swap/d3v4_seed2_swap_27b/outcomes.jsonl` gives 2 lines: unedited (`"source": "unedited"`) and the patched run (`"source": "dissoc"`): read `"top"` and `"role"`.
- The four possible digits: `grep '"id": "ID"' data/pointer_v4/seed2/<topic>_RL_e5f0.json`, then `"sources"` -> `"dissoc"` -> `"predictions"` (none / identity / position / value); k = `"slots"` -> `"position"` + 1.

| Item | k | Asked: original / donor | Unedited | Digits: position / identity / donor's own | Patched answer (role) | Adds to |
|---|---|---|---|---|---|---|
| `countries-RL-e5f0-0157` | 1 | Greece / Philippines | 8 | 4 / 2 / 1 | 4 (position) | position, k 1-2 |
| `countries-RL-e5f0-0109` | 2 | Belgium / Pakistan | 1 | 6 / 7 / 2 | 6 (position) | position, k 1-2 |
| `countries-RL-e5f0-0148` | 2 | Lebanon / Greece | 6 | 4 / 5 / 7 | 4 (position) | position, k 1-2 |
| `animals-RL-e5f0-0167` | 2 | lion / goose | 9 | 7 / 1 / 3 | 8 (another list digit) | neither |
| `countries-RL-e5f0-0074` | 1 | Indonesia / Austria | 9 | 7 / 2 / 1 | 7 (position) | position, k 1-2 |
| `animals-RL-e5f0-0268` | 3 | cow / snake | 9 | 7 / 5 / 8 | 7 (position) | position, k 3-5 |
| `animals-RL-e5f0-0005` | 3 | bear / moth | 1 | 9 / 5 / 8 | 9 (position) | position, k 3-5 |
| `countries-RL-e5f0-0085` | 5 | Canada / Germany | 7 | 2 / 8 / 5 | 6 (another list digit) | neither |
| `countries-RL-e5f0-0242` | 5 | Venezuela / Germany | 7 | 9 / 8 / 1 | 7 (unchanged) | neither |
| `body-RL-e5f0-0064` | 5 | tongue / eyebrow | 6 | 4 / 7 / 5 | 4 (position) | position, k 3-5 |

These 10 rows: k 1-2: 4 position, 0 identity of 5; k 3-5: 3 position, 0 identity of 5. The 3rd-on rows drawn here happen to show no identity answer; over all 460 such items identity leads (173 vs 88, below), and 0 of 5 happens by chance about 10% of the time at that rate. Worth seeing, not a contradiction: from the 3rd sentence on, position answers stay common (19%) and many answers do not move.

Full counts (k 1-2: position 295, identity 5 of 307; k 3-5: identity 173, position 88 of 460), from the same rows.

Recompute: `uv run python verification/finding5_2026-10-23/recompute.py --grid=20261023T105852Z` (numpy needed), line "Qwen3.6-27B draw 2": **k 1-2: position minus identity = +94.5 points [+91.3, +97.3], n = 307; k 3-5: identity minus position = +18.5 [+11.6, +25.2], n = 460**; layer 50; verdict holds. This draw ran before the rule was written (spec d3315bc, 21 Oct); the line "Qwen3.6-27B draw 3" is the fresh draw judged by a rule fixed in advance: +95.5 (n 310) / +14.5 (n 456).

## 3. The lens-readable part of a stated bridge moves recall, not the lookup (README claim 6, Qwen3.6-27B)

Run: `results/statement_positions/d1_topics2_parts_27b/` (Qwen3.6-27B, second draw; the README's "38% of recalls and 1% of lookups"), each part of the change added at the context, layer 32 (fixed before the run). Prompts: `data/tasks_v2/d1_topics_v2/items.jsonl`; on each scene `P2-L0-NNNN` a lookup `PP-L0-NNNN` ("Which locker belongs to Tom's pick?") and a recall `PM-L0-NNNN` ("Which position in the Greek alphabet does Tom's pick have?"). 10 scenes: `random.Random(1023).sample(sorted(lookup ids), 10)`. Unedited: the parts stage ran only on scenes the model answers right, so the unedited answer is the item's `answer`; the changed bridge's answer is `cf_answer`.

What to grep (replace NNNN): `grep -E '"name": "P(P|M)-L0-NNNN".*"set": "context", "layer": 32, "part": "(jspace|not_jspace)", "source": "cf", "null": false' results/statement_positions/d1_topics2_parts_27b/outcomes.jsonl` gives 4 lines: lookup (PP) and recall (PM), each with the lens-readable part (`jspace`) and the rest (`not_jspace`). `"role": "b"` = switched to the changed bridge's answer, `"A"` = kept; `"top_text"` is the answer.

| Scene | Bridge -> changed | Lookup: answer -> changed | Lookup, lens part | Lookup, the rest | Recall: answer -> changed | Recall, lens part | Adds to 1/180, 145/180, 69/180 |
|---|---|---|---|---|---|---|---|
| `P2-L0-0193` | horse -> bee | 7 -> 1 | 7 (kept) | 7 (kept) | 4 -> 6 | 4 (kept) | 0 / 0 / 0 |
| `P2-L0-0174` | delta -> iota | 6 -> 7 | 6 (kept) | 7 (switched) | 4 -> 9 | 4 (kept) | 0 / 1 / 0 |
| `P2-L0-0188` | hydrogen -> lithium | 6 -> 4 | 6 (kept) | 4 (switched) | 1 -> 3 | 1 (kept) | 0 / 1 / 0 |
| `P2-L0-0054` | alpha -> beta | 6 -> 4 | 6 (kept) | 4 (switched) | 1 -> 2 | 1 (kept) | 0 / 1 / 0 |
| `P2-L0-0164` | helium -> carbon | 6 -> 8 | 6 (kept) | 8 (switched) | 2 -> 6 | 2 (kept) | 0 / 1 / 0 |
| `P2-L0-0116` | carbon -> lithium | 1 -> 9 | 1 (kept) | 9 (switched) | 6 -> 3 | 6 (kept) | 0 / 1 / 0 |
| `P2-L0-0003` | delta -> alpha | 3 -> 9 | 3 (kept) | 9 (switched) | 4 -> 1 | 1 (switched) | 0 / 1 / 1 |
| `P2-L0-0254` | helium -> oxygen | 6 -> 2 | 6 (kept) | 6 (kept) | 2 -> 8 | 2 (kept) | 0 / 0 / 0 |
| `P2-L0-0162` | epsilon -> theta | 3 -> 1 | 3 (kept) | 1 (switched) | 5 -> 8 | 5 (kept) | 0 / 1 / 0 |
| `P2-L0-0129` | gamma -> iota | 9 -> 7 | 9 (kept) | 7 (switched) | 3 -> 9 | 3 (kept) | 0 / 1 / 0 |

These 10 scenes: the lens part switches 0 lookups and 1 recall; the rest switches 8 lookups. About 4 of 10 recalls would be expected at 38%; 1 or fewer happens by chance about 6% of the time, so this draw is on the low side.

Recompute: `python3 verification/finding2_2026-10-23/recompute.py --grid=20261023T105852Z`, line "draw 2 main": **the lens part switches 1 of 180 lookups = 0.6% [0.1, 3.1] and 69 of 180 recalls = 38.3% [31.5, 45.6]** (the control, needs >= 30%); the rest switches 145 of 180 lookups = 81%; a random part of the same share switches 0% of lookups and 0% of recalls. Verdict holds. Per the README, the claim is the lookup/recall contrast: the random part moves lookups as little as the lens part does.

## What this sheet does not cover

- Other models, draws and formats: the packets' `recompute.py` print every cell (findings 3-5: every model; finding 2: Qwen3.6-27B only). Against this grid all cells match: 45, 51, 37 and 11.
- The checklists' "three dumbest ways" and known deviations: `verification/finding{2,3,4,5}_2026-10-23/checklist.md`.
- Choices made after the data (claim 1's first draws judged by a later rule; claim 3's split chosen on the first draws): README, "Choices made after seeing the data".
