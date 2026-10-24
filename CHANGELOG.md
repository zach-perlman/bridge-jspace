# Changelog

Newest first. What changed in the claims, the runs and the rules; the README shows only the current state.

## 24 Oct 2026, evening: README rebuilt around X0 (Dan, ~16:40)

- C1 (the late read) and C2 (order, then identity) were removed from the README at Dan's request. The page is now the first experiment of the direction, X0 (C3's pre-registered test), and the plan it led to (X2', X4, X1, X3 under graded rules). The last README with C1-C3 is at 135dc0e (`git show 135dc0e:README.md`). Their numbers, figures and verdicts are unchanged in `results/` and `figures/cross_model/`.
- C3's headline changed:
  - old: post hoc, "lookups 83% → 81%, recalls 78% → 27%" at the 27B's layer 32, on a different position set (every context position);
  - new: X0 at the bridge's word, pre-registered. 27B L32 is not confirmed (lookup excess 0.14, recall J-dependence 0.77); 9B L12 is confirmed (−0.03, 0.53). The graded contrast is 0.60 and 0.53. Figures are in `figures/x0_necessity/`, copied from `results/x0_necessity/figures-20261024T143923Z`.
- The "pre-registered tests" table now lists the X0 rows. The 23 Oct rows are in the README at 135dc0e.

## 24 Oct 2026: the lens pin, the X0 hardware gate

- Lens pin (Dan, 24 Oct): `pins.LENS_REVISION` and the Qwen3.5-0.8B, 2B, 4B and Qwen3.6-27B model configs moved from neuronpedia/jacobian-lens@9fa267f8 (no longer on the Hub: "Invalid rev id") to e166deb5. The 27B J++ file at e166deb5, downloaded into a clean directory, has sha256 bbef480b…f2b58f8f = `FROZEN_LENS_SHA256`: the frozen lens is byte-identical. Every file pinned at the old revision exists at e166deb5; the 27B J-lens's LFS oid (1718c8c5) equals the sha256 `scripts/lens_table.py` recorded at 9fa267f8. The pins are shared with Zach's branch.
- Hardware gate for X0 (2x H100 80GB PCIe box, `jobs/c3/x0_hw_gate_27b.yaml`): one 23 Oct cell (d1_necessity_parts_27b_r2, bridge_word:16) rerun; read-role agreement 0.9898 over 2,744 rows without random draws (bar 0.97): PASS. Lowest arms: jspace_wo_own 0.972, jspace 0.978; the random-draw arms agree on ≥ 0.978 of rows.

## 23 Oct 2026, night: README rebuilt around three claims (Dan's brief, 22:45)

- Seven claims, the band section and the 122B section became C1 (late read; old 1-2), C2 (order, then identity; old 3 and the absent-entity donor) and C3 (lookups let go of the J-space form before recall does; old 5-7, post hoc split depth). 425 → 200 lines. Pinned to grid 20261023T210238Z (new keys lr2, relay, natural, absent, nec, rest_size, late_switch); the size and dose runs are quoted from their summaries.
- Numbers changed, old → new: C1 holds on "8 of 8 (old rule), relay; v2 pending" → late-read v2 share on 8 of 8, relay by digit swap +20 [+16, +25] (Gemma) and +24 [+18, +29] (27B long text), SQuAD 4.7-7.6% (9B, 32B, OLMo-3) and 30% [26, 34] (27B). Old claim 6's "1% of lookups" headline → dropped (the rest at the lens part's size moves 1% (27B) and 3% (9B): a size result). The band's "lens push → lookups 0%" → C3's J-dependence: 27B 0.95 / 0.44 / 0.25 / 0.31 at layers 16-28, 0.03 at 32 (recalls 0.92 / 0.42 / 0.22 / 0.69, 0.65); 9B 0.87 → 0.09 over layers 6-14. The 122B "lens part moves 29% of lookups at layer 24" → J-dependence 0.62 / 0.84 / 0.46 at 24 / 27 / 30, 0.17 at 33; its late switch inconclusive (recalls 26%, 21%, 8% against 30%). Claim 5's "32B (still running)" → holds (word, layer 24: recalls 59%, lookups 5%); Gemma → no valid cell.
- Corrected against the rows (Dan's brief → data): the 32B's 3% → 10% is blind guessing over 1-9, not guessing with the visible digits excluded; the 27B's same-place shares at sentences 3-5 pooled over three sets are 28 / 13 / 19% (29 / 12 / 26% is the third set alone); Gemma's copy leaves 56-69% unchanged (not 60-95%); the projection on the two animals' lens vectors moves 0% of lookups but 24-27% of recalls (27B layer 16), so "≤ 6% of either family" does not hold.
- Not done in this rebuild: the late-read figure (every-later-token lines on the other panels, the SQuAD panel, the relay labels), the heatmap rebuilt on C1-C3, the layer-gap figure's dose arms, F2's absent-entity row in FULL; the size and dose runs as grid rows.
- Choices moved out of the README (21-22 Oct): claim 3 split by the asked sentence (pooled test mixed; confirmed by a fixed rule on fresh sets); claim 3's layer 50 on the 27B (chosen after its first runs; repeated on two more sets); claim 5's second rule from about a third of the depth (the first picked an early layer; both reported); claim 1's first scene set judged by the rule fixed for the second (accepted by Dan); the lens gate after the word (v2; added before any v2 run).

## 23 Oct 2026, evening: README fixes for the TA call (Dan's brief)

- Claim 1: a new rule, late-read v2, beside the old late-read rule: with the sentence hidden and no other route the null is near zero, not the guessing rate (20%). Gemma's and the 27B's long-text cells read "relay; v2 pending", not "fails", until v2 is in the grid; the relay evidence recomputed from raw rows: Gemma scene set 1 23% (last tokens), 15% (and the question), 2% (every token after the sentence), gemma4it_d2_v4_late_read_v3_r2; the 27B's long text 26%, then 11% with the question, DeltaNet layers blocked instead 100%, d2_late_read_long_27b_r3.
- Claim 5: "never the lookup" became "from layer 20 on (27B), 6 (9B, OLMo-3), 33 (122B)": on the 122B two valid, selected cells move lookups (sentence, layer 27, 8x: 26%, recall 84%; layer 30, 8x: 18%, recall 83%; qwen35_122b_d4_where, decision.selected under rule v2, checked with early_push_where.cell_valid). A per-layer table of every sweep, valid cells only, added.
- New section, the band at the word (Dan's main J-space claim): full patch at the word vs the lens push, valid cells only, the position marked per row; maps and pushes recomputed from raw rows; caveats: different scene sets except the 27B's layer gap, the patch not size-matched; an earlier draft's invalid cell (OLMo-3, word, layer 12, 8x, recall 89%) named.
- The 122B section: "The open counter-example" became "The 122B difference" (the lookup follows the J-space form through layer 30, not at 33); "late binding" became "late switch"; layer 30 already measured in qwen35_122b_d1_topics2_parts (the lens part moves 16% of lookups at the sentence, 19% over the whole prompt); the mixture-of-experts caveat added beside the FP8 one; the test runs today on a rented 2x H100.
- Claim 4 (the lens gate) became a methods note: no logit-lens or embedding baseline at the same cells. The J-space part without the bridge's own word added (parts runs, claim 6's test points): lookups 0-2% on the 27B, 9B and 122B; recalls 6-14% (27B), 17-18% (9B), 1-2% (122B); the same-share random part 0-7%.
- Confidence rule: the README now says the "Holds on" counts include cells under 30 items (the builder counts every judged cell); Olmo-Hybrid's tables fail claim 1 by one item (21 of 24 kept with the DeltaNet layers blocked, 87.5% against the 90% bar).
- Claim 7: Zach's 9B, 32B and Muse numbers (and "lookups lose at most 13 points") marked "quoted, not reproducible from this repo until Zach pushes"; only the 27B's run is on origin/zach/v8-breadth-1021. STATUS.md lists it under "Waiting on Zach".
- One prior-work line per claim, pointing to docs/prior_art.md (ec2011a), and a Links entry.

## 23 Oct 2026, day

- README rewritten for newcomers (Dan's guide): six main claims, a summary figure, one section per claim, generated from `docs/README.template.md` and the grid by `scripts/readme_build.py`. The run table moved to RUNS.md, the code mapping to docs/mapping.md, the datasets to docs/datasets.md, the night's notes here.
- Pre-registered before running: the 122B late-binding test (d40f14f, Dan's amendment 98df575), the 27B dose control and layer-16 split (bedbb9a; the split's copy with a same-share random part, 14ef0df), predictions batches 16-17 (e2da840, c3eb3b2).
- The 27B dose control started at 10:20 UTC, before Dan's batch-16 answers; kept by Dan, results closed until he says open. The layer-16 split was cancelled before running and waits for his answers.
- Gemma 4's stated-bridge maps rerun as `_r3` (347b40c): the `_r2` copies reused run names whose partial results were on the box. They keep 167 / 169 of 180 scenes (73c4a69 skips misaligned scenes): a recorded deviation.
- OLMo-3's stated-bridge test in tables and JSON with our J++: not testable (one topic with enough usable scenes); its dependents cancelled.
- Finding 1 now cites Zach's C1 on four models (his Day 3 plan) next to our descriptive removal (b987cd8, 67bfaca).
- `drafts/` taken out of the repo and ignored (2f7d9ea, 5bc2a0f).

## 23 Oct 2026, morning

- Dan's predictions for batches 13-15 committed (a135a54); the night's results opened and scored (ab8f9f9: 8 right, 7 partly, 4 wrong, 1 not decidable of 20).
- The cross-model grid (`scripts/cross_model_grid.py`), merged figures (`scripts/cross_model_figures.py`), the run table (`scripts/run_table.py`) and the lens quality table with our J++ fits.
- The rented 2x H200 deleted at 08:12 UTC after a verified pull (a0cb92d).

## What changed on the night of 22-23 Oct

182 jobs started from 22 Oct 19:30 UTC: 148 on the 4x A100, 34 on a rented 2x H200 (deleted after a verified pull); 67.2 GPU-hours ([runs](#runs)).

- **Qwen3.5-122B-A10B, every experiment (34 jobs):** findings 3, 4 (two draws, tables, JSON, long context), 5 and 6 hold; the lens push holds (lookups 0%, recall 89%); the stated-bridge test fails (lens part 29% of lookups; tables 49%, JSON 34%) and so does the lens write at that cell (29%).
- **Lens gate v2 fails on all seven lensed models** (3-13%; v1 72-100%): the lens names the bridge at its word only.
- **Our J++ lenses for Qwen3-32B and OLMo-3** (fit with the published recipe on 64 prompts; [danorel/Qwen3-32B-jpp-lens](https://huggingface.co/danorel/Qwen3-32B-jpp-lens), [danorel/Olmo-3-7B-Instruct-jpp-lens](https://huggingface.co/danorel/Olmo-3-7B-Instruct-jpp-lens)): pass@10 0.55 and 0.47, +0.43 and +0.15 over the logit lens; gate v1 72% and 100%. With them: the 32B stated-bridge test is not interpretable (recall control fails), OLMo-3's lens push holds (0% vs 51%), OLMo-3's stated-bridge test is not testable (no transit cell), its J-space removal is not interpretable (a control removal keeps 80%).
- **Third draws** on 9B, 32B, OLMo-3, Muse, Gemma: findings 3, 4 and 5 hold on all five (Gemma's late read 19%). **Lists of 8 and 12 sentences:** finding 5 holds on seven models.
- **Long context (~2000 tokens of filler):** the late read holds on 9B (1%), 32B (2%), OLMo-3 (5%), Muse (17%), 122B (7%); the 27B drops to chance (26%; the DeltaNet layers blocked instead keep 100%); Gemma ran out of memory twice.
- **Two new models.** Olmo-Hybrid-7B (no lens): findings 3, 4 and 5 hold on two draws; in tables the DeltaNet layers blocked instead keep 88% (n=24), under the 90% bar. Muse 30B (Zach's J++): findings 4, 5 and 6 hold, finding 3 on three draws (prose fails on 5 items); its lens push has no valid cell; it answers too few table, JSON and stated-bridge scenes.
- **The stated-bridge test in tables and JSON:** holds on 27B (2-3%) and 9B (0%), fails on 122B.
- **The 27B layer-gap test:** the lens push stops moving lookups at layer 20, the full patch at 28 (pre-registered "gap"). The input-embedding push moves nothing, recall included, so it cannot say whether the layer-16 lookup movement is an input edit.

## Choices made after seeing the data, full wording


Kept from the README of 22 Oct:

| Choice | What happened since |
|---|---|
| Finding 5: the split by the asked sentence (the pooled pre-registered test was mixed) | Confirmed as a rule fixed in advance on fresh scenes |
| Finding 5: layer 50 on Qwen3.6-27B (the other models follow a fixed rule) | Repeated on two more draws of scenes |
| Finding 2: counting a topic only when its own recall control passes | Stricter than the pre-registered pooled rule |
| Finding 3: animals on Qwen3-32B's second draw, which missed the competence gate by a rounding margin | Run post hoc with the gate lowered; same verdicts. The gate now rounds to two decimals |
| Finding 7: reading the cells that pass the off-path check | The decisive cell fixed in advance failed that check. The main rule (the off-path check before the maximum) was fixed after seeing these data; the amendment (from layer 20 on) was added knowing them, before the rerun's results were opened. The main rule stays main; both verdicts are reported |
| Finding 2, the doubled run: the cell fixed in advance (the first map's choice); on Qwen3.5-9B the 27B's layers scaled by depth | Fixed before those runs |
| Finding 4: the first-sentence bias as a fall-back to the order label | Dropped from the story; its control was not testable |
| Batch 12 opened before Dan's predictions (his request, 22 Oct) | His answers count as written after the results |
| Finding 8: the position code's natural-size test allowed 1x or 2x | Passes only at 2x; we read it as an override |
| Finding 2's rule: one decisive cell, chosen from the lens-free map | Amended on 22 Oct, after the runs started and before any result was opened |

Added on the night of 22-23 Oct (decisions, not results):

- **Lens gate v2, where the lens is read**: only where the bridge's word is not: after the word in the bridge's own sentence (in prose, its closing period; decisive) and over the context without any mention of either bridge (reported); the same bars as v1. Set after seeing that v1's read sat on the bridge's own word, before any v2 run. v1 still opens the stated-bridge test; v2 is informational: if it fails, 'the lens reads the bridge' becomes 'the lens reads the bridge's word where it stands' (Dan, 22 Oct 23:20; 2b0701f, c2add04).
- **When an arm of the layer-gap test 'stops'**: at a layer where every valid cell's Wilson upper bound is below 5% of lookups (it keeps moving while some cell's lower bound is above 5%); the gap holds if the full patch stops at least six layers after the lens push and still moves lookups where the lens push stopped. Four arms on the same scenes (lens push, full patch, input-embedding push, random push), each with its own off-path check; set before the rerun, which replaced a first version stopped part-way (c2add04).
- **The keep-answer gate on Gemma and Muse**: in the stated-bridge test the lookups must keep their answer under the lens-part patch on at least 80% of items, else the cell is not interpretable. Added because a random patch of the same size breaks most of Gemma's answers (finding 5's control); set before any Gemma or Muse stated-bridge run (c2add04).
- **The primary lens**: where we fit our own J++ with the published recipe (Qwen3-32B, OLMo-3-7B-I; 64 prompts), every claim is judged on it; Zach's fits and the plain J-lens are listed beside it, never switched in silently. Decided by Dan (23 Oct ~00:30) after the plain J-lens results on Qwen3-32B were seen, before the J++ pins and any J++ run (e50b1dc, 193c060, 2f3c320).
- **The stated-bridge verdict's layer grid (a fix)**: its decisive cell is searched on the map's coarse grid (every sixteenth of the depth), not on every 4th layer, which never met the parts run's layers on Muse, met them at one layer on Gemma and skipped half the grid on the 32-layer models (the 64-layer models are unchanged). Found before any Muse, Gemma or OLMo J++ stated-bridge verdict ran; those runs were requeued (076edbb, 65f8dba).
- **OLMo-3-7B-I's lens push in raw prompts**: the chat format leaves too few fresh scenes OLMo answers right, so the raw-prompt run was fixed as OLMo's decisive cell before any OLMo J++ result, behind a short smoke check that stops it if the raw prompts' unedited answers differ from its competence run; the chat copy is not run (fe8f12f, f9f06b8).
- **Qwen3.5-122B at batch 16**: its read-heavy steps run 16 prompts per batch (J-space removal 8), to fit the night on the rented H200s (Dan, 23 Oct ~01:20); the originals queued at batch 4 were cancelled before running and requeued as copies; no rule, layer or item changed (d286f2c, cc02033).
- **Seven verdict words**: holds, fails, inconclusive (the rule itself says so; no control failed), not interpretable (a control failed: which), not testable (no lens, the gate or competence failed), missing (did not run, failed, or no saved verdict: why), open (values shown under no committed rule). 'Open' is its own word for the descriptive cells (the animal-suite J-space removal, the last-token lens arm), never 'missing' for that reason; the lens push's main rule keeps its own 'inconclusive' where the lookup moves between 10% and 30% (Dan, 23 Oct; 3b8e3cc, 978cbdc).
- **Finding 1's interval**: the animal-suite removal has no committed rule, so its cell is descriptive: the share of lookups right minus the share of recalls right with the J-space removed (clean question). Its 95% interval: the bridge animals drawn with replacement, separately for the lookups and the recalls (unpaired), 4000 times with seed 0; the interval is the 2.5th to 97.5th percentile of the differences. Chosen after seeing the data; accepted by Dan (23 Oct; 978cbdc).
- **Finding 8, stated bridge, in the grid**: the cell holds iff the lens push writes recall and not the lookup at the stated-bridge cell; recall not written means no positive control (not interpretable). Written by the grid agent, accepted by Dan (23 Oct).
- **Finding 6's decisive layers** on Qwen3.5-9B, Qwen3-32B, Muse, Gemma and Qwen3.5-122B: the swept layers where the donor's digit is still rare (Wilson upper bound below 10%), the specs' rule applied by the grid. Accepted by Dan (23 Oct).
- **Finding 4, first draws**: judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under an older rule); a late read that fails with its interval around chance is footnoted 'at chance' (Dan, 23 Oct).
- **Gemma's stated-bridge runs, n**: 167 scenes (topics) and 169 (tables and JSON) instead of the pre-registered 180: 73c4a69 skips scenes whose token positions fail the alignment check (the first attempts stopped on them). A deviation from the specs, recorded in the grid; accepted by Dan (23 Oct 12:30).
- **Reading finding 6 by setting** (a filler sentence moved vs one sentence more or fewer) in the overview and the conclusions, instead of only the per-model state: chosen after seeing the grid (23 Oct).
- **The layer-gap and embedding analyses** were run once each with the committed `analyze --rule v2`, into new folders; they reproduce the runs' own summaries. The embedding test's committed verdict ("no lead") stands; that it pools scales where the lens push moves nothing is our reading after the data.
