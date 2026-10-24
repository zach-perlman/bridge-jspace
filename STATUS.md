# Overnight 24-25 Oct (Dan's ~21:50-22:05 instructions; agent). All numbers UNVERIFIED

95% CIs: cluster bootstrap over bridge entities (10,000 resamples, seed 0). Excess = flips lost without the part minus flips lost without a random part of its own share. Lookup = PP, recall = PM.

| Test (run) | Pre-stated reading | Branch that happened | Numbers [95% CI] | n |
|---|---|---|---|---|
| X0b verdict, pooled rule (`x0b_v2`; check, item 5) | holds iff lookup excess ≤ 0.10 (upper CI ≤ 0.20) and C ≥ 0.20 (lower CI ≥ 0.10) | holds on both (brief's C ≥ 0.30: 27B only) | 27B lookup 0.08 [0.06, 0.10], C 0.47 [0.42, 0.53]; 9B lookup 0.01 [−0.01, 0.03], C 0.22 [0.14, 0.31] | 1,635 / 1,010 scenes; 61 / 53 entities |
| Mass-mean A / V / A+V, main arms (`x0_massmean`; check, item 4) | lookup loses under A (or V), recall not → "uses the address (value)"; no arm changes the lookup → "not a low-rank linear readout" | for Dan (Q28.6 and the reading) | 9B lookup: A 0.31 [0.18, 0.44], V 0.00 [0.00, 0.00], A+V 0.46 [0.35, 0.58], keep A+V 0.40 [0.29, 0.53]; 9B recall: A 0.11 [0.04, 0.19], V 0.01 [0.00, 0.05], A+V 0.19 [0.10, 0.30], keep 0.11 [0.04, 0.19]. 27B lookup: A 0.04 [0.00, 0.09], V −0.01 [−0.05, 0.00], A+V 0.14 [0.06, 0.24], keep 0.04 [0.00, 0.10]; 27B recall: A 0.10 [0.00, 0.19], V 0.00 [−0.08, 0.08], A+V 0.20 [0.06, 0.37], keep −0.02 [−0.06, 0.00]. Median share of ‖Δ‖²: A 0.151 / 0.160, V 0.127 / 0.150, A+V 0.229 / 0.233 (9B / 27B) | 73 / 70 items |
| jw orthogonality (`x0_parts` states; check, item 3) | — (report the word's energy inside jw if jw was not fit on Δ − w) | jw was fit on the whole Δ | jw holds a median 0.67 (27B) and 0.66 (9B) of the word part's energy, ((jw·w)/‖w‖²)² | 200 items each |
| Word, J++ without the word, J++ on X0b's items (`x0b_parts_r2`; Q28.10) | recall's loss mostly in w → the word; mostly in jw with PCA inert → J++ beyond the word; PCA ≈ J++ → aligned with the layer's geometry | mostly in jw (PCA not run on X0b's items, so "PCA inert" is untested there) | recall: w 0.12 [0.08, 0.15], jw 0.55 [0.49, 0.60], J++ 0.56 [0.50, 0.62] (27B); w 0.05 [0.03, 0.09], jw 0.24 [0.16, 0.34], J++ 0.23 [0.15, 0.33] (9B). Lookup ≤ 0.08 everywhere. Q28.10: wrong (Brier 0.64) | 1,635 / 1,010 scenes |
| PCA at J++'s share, k per item (`x0_pcaeq_mmlf`; Q30.1 committed before the run) | recall-specific like J++ → "J++-specific" means "aligned with the layer's main directions"; hurts both → J++ is the only dictionary that separates the readers; inert → J++ is special at equal share | none of the three, on either model (Q30.1 (d) "mixed": right, Brier 0.04) | 27B lookup 0.02 [0.00, 0.05], recall 0.16 [0.08, 0.23]; 9B lookup 0.08 [0.02, 0.15], recall 0.13 [0.06, 0.19]. J++ on the same items: recall 0.61 [0.51, 0.69] / 0.37 [0.29, 0.43]. Atoms per item: median 5 (27B, range 1-95), 8 (9B, 3-54) | 200 items each |
| Word-orthogonal J++ without the word (`x0_pcaeq_mmlf`; no prediction committed) | recall still loses ≥ 0.20 with the word intact → "recall needs J++ components beyond the word"; ≤ 0.10 → "redundant: either suffices" | neither, on either model | recall 0.199 [0.10, 0.29] (27B), 0.115 [0.06, 0.18] (9B); lookup 0.03 [0.00, 0.07], 0.00 [−0.03, 0.02]. Share of ‖Δ‖²: 0.11 / 0.16 | 200 items each |
| Layout-free mass-mean address Alf (`x0_pcaeq_mmlf`; no prediction committed) | if the 9B lookup effect disappears with Alf → "position information", not "address" | does not disappear (lower CI > 0), so the stated reading does not apply | 9B lookup: remove Alf 0.49 [0.38, 0.59] (A 0.31 [0.18, 0.44]), keep only Alf 0.36 [0.25, 0.48] (A 0.25 [0.15, 0.36]); recall: remove Alf 0.12 [0.05, 0.21]. 27B lookup: remove Alf 0.14 [0.07, 0.22] (A 0.04 [0.00, 0.09]), keep Alf 0.07 [0.02, 0.14]; recall remove Alf 0.16 [0.02, 0.31]. A-Alf overlap 0.72 / 0.71 | 73 / 70 items; Alf from 758 states, 31 layout groups |
| X4 probe (`x4_probe`; batch 29) | (X4.md: descriptive) the bridge's locker statement readable within each form and as a transfer | readable in every form, both models (Q29.2, Q29.3: right) | within translated: 0.99 [0.99, 1.00] (27B), 0.93 [0.90, 0.96] (9B); transfer from verbatim: 0.94 [0.90, 0.97], 0.84 [0.79, 0.90]; symbol: 0.97 [0.90, 1.00], 0.89 [0.83, 0.95]; chance 0.20 | 400 scenes per form; 8 / 6 entities |
| X4 patch test (`x4_patch`; batch 29) | D_translated ≥ 0.20 → needs a verbatim match; ≤ 0.10 → it does not. D_symbol ≥ 0.20: control passes; else "the method may not see a lookup that needs J++" | D_translated ≤ 0.10 on both: does not need a verbatim match. Control fails on both | D_translated 0.01 [−0.01, 0.04] (27B, D > 0 for 3 of 8 entities), −0.02 [−0.05, −0.00] (9B, 2 of 8); D_symbol 0.15 [0.10, 0.19] (27B, 6 of 6), −0.05 [−0.08, −0.02] (9B, 0 of 6). Entity bootstrap unreliable below 10 clusters. Q29.1-Q29.5 right, Q29.6 wrong | lookup 341-400 items per form |

**Failed or odd**
- No job failed; nothing was rerun. Jobs run tonight: `x0b_parts_r2`, `x0_pcaeq_mmlf` (equal-share PCA, word-orthogonal jw, layout-free mass-mean), `x4_probe`, `x4_patch`. X4 was held in the queue for ~5 min so that `x0_pcaeq_mmlf` ran first, as ordered.
- X4: the box's results had no probe-fit or verdict folders although both jobs exited 0; recomputed locally on CPU (`probe_fit`, `verdict`) from files whose checksums match the box.
- Word-orthogonal jw on the 27B: 0.199, 0.0014 under the 0.20 bar.
- J++ rerun beside the new parts differs slightly from `x0_parts` on the same items and seeds (27B recall 0.61 vs 0.63, S_whole 0.73 vs 0.725; 9B lookup −0.02 vs −0.01): about one item flips between GPU runs.
- Alf (layout-free) costs the lookup more than A on both models (9B 0.49 vs 0.31; 27B 0.14 vs 0.04).
- X4, 27B: the recall's random-part dependence is 0.18 [0.09, 0.30] in animals/verbatim, and the symbol recall's excess interval reaches 1.03 (the ratio's bootstrap). The 9B recall barely needs J++ in animals/verbatim (0.04 [0.00, 0.09]; X0: 0.37-0.50).
- Calibration table: Q28.7 and Q28.8 had been binned at 20% (the first % in the answer) instead of 50% (the top option); fixed. Now 58 answers, mean Brier 0.37.
- Q28.6 left to Dan: scored once from his chat reply, then reverted before any commit, per his ~21:55 note.

# Status, 20 Oct 2026 (Zach)

**Plan:** [Google Doc](https://docs.google.com/document/d/1bqqdXePTUXQGlowVjk73sPfJkbV_tsu0RNNX-BiTYUc/edit?usp=drivesdk) ·
**Run log:** [EXPERIMENTS.md](EXPERIMENTS.md) (one line per run: question, n, seeds, result, W&B link, verdict) ·
**Nothing below is in [VERIFIED.md](VERIFIED.md) yet:** every number is unverified until one of us checks it.

## Waiting on Zach (23 Oct)
- Claim 7's C1 runs on the 9B, 32B and Muse (gaps 38, 22 and 7 points; lookups lose at most 13): quoted in the README from his Day 3 plan, not on origin/zach/v8-breadth-1021 (only the 27B's `results/ablate_v2/c1_v2/` is); reproducible from this repo once he pushes them.

## Where things stand
- **Memory vs prompt (Qwen3.6-27B, controlled suite).** A bridge that feeds a recall from memory goes through the J-space; the same bridge feeding a lookup in the prompt goes around it. Three measures agree:
  - **Copy split:** lookup-used bridges get 0.3–0.4× their fair share of the copy in the J-space, recall-used 1.4–1.9× (random null 0.15–0.4).
  - **Lens write:** RL is read 95% but written ≤3%; RR is written 36%.
  - **Knock-out:** lookups stay at 99%, recall chains drop to 19–22%; random and same-size controls stay at 98–100%.
  - It also holds in JSON tool outputs and in real facts (TwoHopFact).
- **Generality is the gap.** All positive evidence comes from two Qwen hybrid-attention models.
  - **122B:** read-but-not-written holds at every depth; the knock-out effect is 4–6× weaker.
  - **9B:** mostly untested.
  - **Gemma 4 31B-it:** untestable. Our own J++ reads well, but the lens can't write even the countries check, and any J-space removal wrecks the model, plain text included.
- **Open confounds in the knock-out:**
  - It also removes word answers (name answers −35% even in a pure lookup).
  - It may be erasing the subject's identity rather than the workspace.

![The 27B families under three measures](figures/overview_1020/story_2x2.png)
*The suite's families under the three measures (27B).*

![Lens write by depth](figures/overview_1020/story_depth.png)
*Where the lens can write the bridge, by depth: 27B vs 122B.*

![Settings and models](figures/overview_1020/overnight_1020.png)
*Read vs write and the knock-out across settings and models.*

![Evidence by model](figures/overview_1020/evidence_by_model.png)
*Which claims each model supports, contradicts or can't test.*

## Where things are
| What | Code | Results |
|---|---|---|
| Suite: 2×2 (given/recalled × lookup/recall), tie-breakers, NAMES, CODE, computed bridges, tool-output set | `scripts/suite_v1.py` | `data/suite_v1*`, `data/computed_v1`, `results/suite_v1/` |
| Copy-and-split (J-space share of a lens-free copy) | `scripts/suite_split.py`, `scripts/control_split.py` | `results/suite_split/`, `results/control_split/` |
| Lens read vs write (strength and layer sweeps) | `scripts/read_write.py`, `scripts/rw_per_layer.py` | `results/read_write/` |
| J-space knock-out (random and same-size rotated controls) | `scripts/ablate_pilot.py`, `scripts/tool_answer_type.py` | `results/ablate_pilot/`, `results/tool_answer_type/` |
| Real facts (TwoHopFact): screening, natural lookup, per-step knock-out | `scripts/twohop_pilot.py`, `scripts/natural_rw.py`, `scripts/natural_hops_ablate.py` | `results/twohop_pilot/`, `results/natural_rw/` |
| Gemma 4 31B-it J++ fit (jpp_lens recipe) and removal diagnostics | `scripts/lens_fit/`, `scripts/removal_norms.py`, `scripts/removal_textloss.py`, `scripts/gemma_ref_loss.py` | `results/lens_fit/`, `results/removal_norms/`, `results/removal_textloss/`, `results/harness_checks/` |
| Figures | `scripts/story_figures.py`, `scripts/overnight_figure.py`, `scripts/coverage_figure.py` | `figures/overview_1020/` |
| Job scripts exactly as run | `scripts/queues/`, `scripts/quick_*.sh` | — |

**Other models** are set with `BJ_TARGET` (see `src/bridge_jspace/pins.py`):
- `qwen3.5-9b`, `qwen3.5-122b-a10b` (FP8; needs `BJ_BATCH=16`);
- `gemma-4-31b-it-baselens` (the base model's published J++);
- `gemma-4-31b-it-refit` (our J++, layers 24–45, sha256-pinned; the file sits in `cache/`, so re-export it with `scripts/lens_fit/export_jpp_lens.py`).

**Failed runs, recorded in EXPERIMENTS.md and not pushed:**
- `results/ablate_pilot/qwen35_122b_abl_depth_v1`: out of memory; rerun as `_v2`.
- `results/removal_norms/norms_v1`: empty WikiText rows; rerun as `norms_v2`.
