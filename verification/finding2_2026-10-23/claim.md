# Finding 2 on Qwen3.6-27B: a lookup ignores the lens-readable part of a stated bridge

Packet for the hand check of 23 Oct 2026 (Dan, Zach), Qwen3.6-27B only (Dan's request). UNVERIFIED until a human adds it to VERIFIED.md. Every number here comes from `recompute.py` in this folder, run on the saved outcomes; it matched all 11 Qwen3.6-27B cells of this finding in `results/cross_model/20261023T091847Z/grid.csv` (the main J++ lens and the plain J-lens listed beside it).

## The claim in plain words

The scene states the bridge in the prompt ("Tom picked iota.") and asks either for a fact stated in the prompt about it (a lookup: "Which locker belongs to Tom's pick?", answer from "The locker of iota is three.") or for a fact from memory (a recall: "Which position in the Greek alphabet does Tom's pick have?"). A second prompt changes the bridge (Tom picked delta), which changes both answers. We take the change of the hidden states between the two prompts at the context's positions at layer 32, split it into the part the lens can read (its J-space part: a 25-atom fit over the J++ lens's token directions) and the rest, and add one part at a time to the original run. The lens-readable part alone switches about 0-3% of lookups but 36-42% of recalls; the rest switches 81-96% of lookups. So the lookup uses the stated bridge through a part of the representation the lens does not read, while recall does use the lens-readable part.

## The rule, fixed before the runs

`scripts/d1_verdict.py` (replication rule, amended 22 Oct 17:36 +0200 before any of these results was opened). The second draw's spec, `jobs/d1/d1_topics2_parts_27b.yaml` (committed at a786b36, 22 Oct 20:18 +0200, before the run):

> scripts/d1_verdict.py with --cell context:32 (fixed 2026-10-22 evening, before these runs: the cell d1_topics_map_27b chose by the lens-free rule). At that cell, pooled over the three topics: replicates iff the lens-readable part alone switches <= 0.10 of PP lookups and everything else >= 0.50, while PM's lens-readable part switches >= 0.30 (the positive control); a failing control: not interpretable. Per topic, the same verdict on the topic's own rows (topic_verdicts); a topic counts only if its own control passes.

First draw (`jobs/d1/d1_topics_parts_27b.yaml`, 3e90959): the same split, with the cell chosen from the lens-free map by the amended rule (the context at layer 32). Tables and JSON (`jobs/d1/d1_formats_parts_27b.yaml`, dbc4527, 22 Oct 22:57 +0200): the same rule pooled and per format; "holds in tables and JSON iff the pooled verdict and both format verdicts replicate".

"Switched" = the read's top token is the changed bridge's answer (role `b`). The grid calls "replicates" holds.

## Headline (recomputed; % of items switched; lookups = PP, recalls = PM; all at the context, layer 32)

| Setting | n per family | Lookups: lens part | rest | whole change | same-share random part | Recalls: lens part | rest | whole change | same-share random part | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| draw 1 | 120 | 0% [0, 3] | 87% | 84% | 0% | 36% [28, 45] | 38% | 82% | 2% | holds |
| draw 2 | 180 | 1% [0, 3] | 81% | 83% | 0% | 38% [32, 46] | 27% | 78% | 0% | holds |
| tables | 83 | 2% [1, 8] | 96% | 96% | 0% | 42% [32, 53] | 28% | 93% | 0% | holds |
| JSON | 97 | 3% [1, 9] | 95% | 98% | 0% | 37% [28, 47] | 46% | 92% | 1% | holds |

- Draw 2 per topic (animals 43, elements 74, Greek letters 63 items): all three hold (lookups 0-1%, recalls 32-53%).
- Plain J-lens, listed beside (draw 2): lookups 0%, but its recall control fails (18% < 30%): not interpretable pooled; per topic only animals holds (37%), elements and Greek letters are not interpretable (15%, 8%).
- 11 cells: 8 holds, 3 not interpretable (all plain J-lens), 0 mismatches with grid.csv.
- "Same-share random part" = `jspace_matched` (grid.csv's name since 20261023T104743Z): a random direction matched to the lens part's alignment with the change (`scripts/statement_positions.py`: "exp02's matched-alignment pieces"). It switches 0-2% of recalls against 36-42% for the lens part, so the recall control is not a size effect. The newer grid prints these values; `recompute.py --grid=20261023T104743Z` checks them too (11 of 11 match).

## Worked example (random scene, `random.Random(0)` over the sorted lookup ids of the second draw)

Reproduce with `python3 verification/finding2_2026-10-23/recompute.py --example`. Scene `P2-L0-0150`, run `results/statement_positions/d1_topics2_parts_27b/`, items in `data/tasks_v2/d1_topics_v2/items.jsonl`:

Context: "Kyle picked gamma. Victor picked delta. The locker of gamma is four. The locker of iota is three. Tom picked iota. The locker of delta is five." Changed context: "... Victor picked iota. ... Tom picked delta. ..." (the bridge changes from iota to delta).

| Patch added at the context, layer 32 | Lookup "Which locker belongs to Tom's pick?" (3; changed: 5) | Recall "Which position in the Greek alphabet does Tom's pick have?" (9; changed: 4) |
|---|---|---|
| the whole change | 5 (switched) | 4 (switched) |
| the lens-readable part | 3 (kept) | 9 (kept) |
| the rest | 5 (switched) | 9 (kept) |
| same-share random part | 3 (kept) | 9 (kept) |

This scene's recall is one of the 62% that the lens part does not switch; the lookup shows the claimed pattern.

## Where the numbers come from

- `results/statement_positions/<run>/outcomes.jsonl`: one row per item, cell and part, with `family` (PP lookup, PM recall), `name`, `set`, `layer`, `part`, `source` ("cf" = the changed bridge, "off" = the off-path control), `null` (true = the random-direction null at the row's norm), `role`, `top_text`. Decisive rows: `source == "cf"`, `null == false`, `set == "context"`, `layer == 32`.
- Topic and format per item: `data/tasks_v2/<set>/items.jsonl` (`domain`, `format`).
- Runs: draw 1 `d1_topics_parts_27b` (set `d1_topics_v1`, seed 22), draw 2 `d1_topics2_parts_27b` (`d1_topics_v2`, seed 23), plain J-lens `qwen36_27b_jlens_d1_topics2_parts`, tables and JSON `d1_formats_parts_27b` (`d1_formats_v1`, seed 41). Saved verdicts: `results/d1_verdict/<run>_<stamp>/verdict.json`.
