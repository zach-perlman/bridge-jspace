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
