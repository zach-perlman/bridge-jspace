# Finding 4: a lookup ends in a late attention read of the answer's sentence

Packet for the hand check of 23 Oct 2026 (Dan, Zach). UNVERIFIED until a human adds it to VERIFIED.md. Every number here comes from `recompute.py` in this folder, run on the saved rows; it matched every cell of `results/cross_model/20261023T091847Z/grid.csv` (51 of 51). An earlier, longer packet for the 27B and 32B only is `verification/finding4_late_read.md` (22-23 Oct).

## The claim in plain words

Same scenes as finding 3: a list of five sentences binding entities to digits, a question that names the entity through a cue the model must recall. We stop the last tokens of the prompt from attending to the whole answer's sentence, in every attention layer (on the hybrids, which mix attention and DeltaNet layers, only the attention layers are blocked). The lookup then drops to guessing among the list's digits or below. Blocking another sentence of the same length instead changes nothing, and on the hybrids, blocking the answer's sentence in the DeltaNet layers instead also changes nothing. So the lookup ends in an ordinary attention read of the answer's sentence by the last tokens.

## The rule, fixed before the runs

Draws 2 and 3 and the long context, `jobs/d2/d2_late_read_seed2_27b.yaml` (committed at 6538445, 22 Oct 18:50 +0200, before the second draws ran; copied into every later late-read spec):

> Fixed 2026-10-22 before this run: memory -> prompt, pooled over topics, items right unedited. Replicates iff the answer's statement hidden from the last tokens in every attention layer leaves <= 20% right (point) with the Wilson upper bound <= 0.30, the off-path statement hidden there keeps >= 90% right (Wilson lower bound >= 0.85), and hidden in every DeltaNet layer instead keeps >= 90% right.

Prose, tables and JSON: the same rule per format, `jobs/d2/d2_formats_27b.yaml` at 444500e (22 Oct 20:23 +0200, before those runs).

First draws: they ran under an older rule (per topic, entity-cluster bounds; `jobs/d2/d2_v4_late_read.yaml`, c2d5b8e, 21 Oct). The grid judges them by the rule above (Dan, 23 Oct; README footnotes 11-19). That is a choice made after the data.

The grid's verdict words: not interpretable if the off-path control fails (rate < 90% or lower bound < 85%); fails if the read is not blocked enough, or (hybrids) if blocking the DeltaNet layers instead keeps < 90%; "at chance" is a footnote when a failing interval contains 20%.

## Headline (recomputed)

- Sentence lists, draws 1-3: 0-9% right with the read blocked on seven models (27B 7-9%, 9B 1-3%, Olmo-Hybrid 7-8%, 122B 5%, 32B 1-3%, OLMo-3 0-1%, Muse 1-3%); Gemma 23%, 22% (fails, at chance) and 19% (holds). Another sentence blocked keeps 98-100%; on the hybrids the DeltaNet layers blocked instead keep 99-100%. 19 of 21 draw cells hold.
- Long context (about 2,000 tokens of neutral filler between the list and the question): 9B 1%, 122B 7%, 32B 2%, OLMo-3 5%, Muse 17% hold; the 27B 26% [20, 33] fails at chance, with the DeltaNet layers blocked instead still 100%.
- Prose, tables, JSON: 14 of 24 cells hold; fails: Gemma prose 34% and JSON 21%, Olmo-Hybrid tables (attention blocked 0% right, but the DeltaNet layers blocked instead keep 88%, 21 of 24, under the 90% bar); not interpretable: five cells of 5-18 items whose off-path control keeps 89-100% but has a Wilson lower bound < 85% (Olmo-Hybrid prose and JSON, OLMo-3 prose and JSON, Muse prose); Muse tables and JSON not testable.
- 51 cells: 38 holds, 6 fails, 5 not interpretable, 2 not testable. No run: draw 3 on 27B, Olmo-Hybrid and 122B (no spec); long context on Olmo-Hybrid (running) and Gemma (failed).
- Where the wrong answers go under the block: 6,026 of 6,282 (96%) are another digit of the list, not a collapse off the list.

## Worked example (random item, `random.Random(0)` over the sorted ids of the 27B's second draw, memory -> prompt, right unedited)

Reproduce with `python3 verification/finding4_2026-10-23/recompute.py --example`. Item `body-RL-e5f0-0099`, run `results/attn_knockout/d2_late_read_seed2_27b/`:

Prompt: "The bladder chart is in folder 5. The spine chart is in folder 6. The ankle chart is in folder 8. The wrist chart is in folder 3. The skull chart is in folder 4. Which folder holds the chart on the body part joining foot and leg? Answer with a single word and nothing else." Answer: 8 (ankle).

| Blocked from the last tokens | Layers | Model's answer |
|---|---|---|
| nothing | - | 8 (right) |
| the answer's sentence "The ankle chart is in folder 8." | every attention layer | 6 (the spine chart's digit) |
| another sentence of the same length, "The wrist chart is in folder 3." | every attention layer | 8 (right) |
| the answer's sentence | every DeltaNet layer | 8 (right) |
| the other sentence | every DeltaNet layer | 8 (right) |

## Where the numbers come from

- `results/attn_knockout/<run>/rows.jsonl` and `cases.jsonl`, as in finding 3. Decisive rows: `source == "lookup"` (the answer's sentence) or `"lookup_off"` (the control), `dest == "final"` (the last tokens), `layers == "attn"` on hybrids and `"all"` on attention-only models, plus `layers == "gdn"` (DeltaNet) on hybrids; `family == "RL"` (draws, long context) or `"MP"` (formats), items right unedited; "right" = the row's `correct`.
- Chance: 1 in 5 on the sentence lists (5 digits per scene); the format scenes have 3 facts (1 in 3, see checklist).
- The run behind every cell is in `recompute.py` (`RUNS`) and in README, "Runs", finding 4.
- Seeds: scenes from each data set's draw; the off-path sentence is drawn per scene with seed 0 (manifest `seeds`); the long-context filler as in its manifest.
