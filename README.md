# bridge-jspace

**Question.** In a two-hop question ("the language spoken in the country where the Amazon River ends is ..."), the
model has to compute a bridge entity (Brazil) before it can answer (Portuguese). On Qwen3.6-27B and Gemma 4 31B the
J-lens often cannot read that bridge. Does the bridge still act on the answer through the J-space, or through a part
of the representation the J-lens cannot read?

**Reference result (Claude, Gurnee et al. 2026,
[Verbalizable Representations Form a Global Workspace](https://transformer-circuits.pub/2026/workspace/index.html)).**
Swapping the bridge's probe for another entity's flips the answer in 61% of items when only the J-space part of the
probe is swapped, 28% for the remainder, and 6% for the remainder when the J-space coordinates are clamped.

**Reading.** If on open models the remainder flips about as often as the J-space part and survives the clamp, the
bridge works outside the workspace. If the numbers look like Claude's, the J-lens misses on open models are a read-site
or tokenization artifact.

## Method, part A: can any reader see the bridge? (exp10+)
1. `exp10_lens_sanity`: the lens works on this model. Sanity gate (known fact, HF parity, our readout == jlens's
   `apply`), then `lens-eval-multihop` pass@k for the J-lens and J++ against the logit lens, plus a bridge vs
   same-category distractor control. Debugged on Qwen3.5-0.8B (CPU), run on Qwen3.5-4B (same `qwen3_5` hybrid
   architecture as the target), then Qwen3.6-27B. Results under Status.
2. `exp11_bridge_vs_answer_by_layer`: on part B's items and labels, at the last prompt token, at which layers each
   reader has the bridge (and, separately, the answer) on top of its candidate pool. Results under Status.
3. `exp12_position_map`: the same readout at every prompt position x layer: where in the prompt, and how deep, each
   word is readable; the best position per reader, chosen on half the items and checked on the other half.
4. Oracle lens and NLA on the same items, split by part B's J-mediated / non-J labels (planned).

## Method, part B: is the bridge used outside the J-space? (exp01-09)
1. `data/entity_prompts.json`: about 8 prompts per entity that imply the entity without naming it, for the 97
   entities in `data/probe_swap.json` (bridges and swap targets). Qwen keeps the ones it answers correctly.
2. Probe per entity and layer: mean final-token residual over its kept prompts minus the mean over all entities.
3. Decomposition per layer: non-negative OMP (k=25) over J-lens (or J++) token directions gives the J-space part; the
   remainder is the rest. From v4, both lenses decompose the same probes (`exp01_probes redecompose`).
4. Swaps on the 90 two-hop items, at every band layer and prompt position, under five conditions: raw J-lens vectors,
   full probe, J-space part, remainder, remainder with the J-space coordinates clamped. Each has a random-direction
   control of the same edit norm. Metric: rate at which the swap answer becomes the top word, with Wilson 95% CIs.
   From v4: prompts with the trailing space stripped, and eligibility and flips judged on the greedy continuation
   (exp13's criterion C), which makes 77 items eligible; swaps can be restricted to some prompt positions.
5. `exp03_brew_swaps`: the same swaps and graded steering along lens directions on an in-context two-step lookup
   (WorkspaceBench's brew bank), where the counterfactual answer is read straight off a table in the prompt.

## Layout
```
src/bridge_jspace/
  config.py       typed YAML configs + dotted CLI overrides (model=<yaml> swaps the whole model)
  models.py       pinned HF model -> jlens LensModel; lens / J++ files (same format) moved to GPU once
  readout.py      rank-only readouts (J-lens, J++, logit lens), word -> token ids
  sanity.py       checks every new model/pod must pass before any readout is trusted
  stats.py        Wilson and bootstrap CIs
  experiment.py   Experiment base: results/<exp id>/<timestamp>/, manifest.json before run()
  pins.py         pinned upstream data, sha256-checked on load
configs/models/   one YAML per model: HF revision + lens files (qwen3.5-0.8b / 2b / 4b, qwen3.6-27b)
scripts/          experiment code: part A expNN_name/ (config.yaml + experiment.py), part B expNN_*.py
scripts/run.sh    experiment in a detached tmux session, log in log/
scripts/prefetch.py  download a model YAML's snapshot + lenses, retrying on HF rate limits
examples/         rendered worked-example pages per experiment (make examples-render; slices/ not committed)
infra/            pod bootstrap
```
`AGENTS.md`: rules for running experiments. `VERIFIED.md`: results a human has checked. `data/README.md`: what
data we use and what the lenses were fitted on (`make data-report`).

## Running
```bash
make install                 # uv sync + pre-commit hooks
make check                   # ruff + pyright + unit tests (no download)
make test-model              # integration on Qwen3.5-0.8B + its lenses (CPU ok)

# GPU box: bash infra/setup_pod.sh, then any experiment = one config, run in tmux:
make run CONFIG=scripts/exp10_lens_sanity/config.yaml                      # Qwen3.5-4B
make run CONFIG=scripts/exp10_lens_sanity/config.yaml ARGS="model=configs/models/qwen3.6-27b.yaml"
tmux attach -t <session>     # or: tail -f log/<session>.log

# Worked examples (lens tables for sampled questions; the examples run needs the GPU, rendering does not):
make run CONFIG=scripts/exp12_position_map/examples.yaml   # results/<exp>/<stamp>/examples.json + slices/
make examples-render                                       # examples/<exp>/ from the latest examples run of each exp
make examples-serve                                        # render, serve examples/ on localhost:8000, open browser
```
On a pod, `make examples-serve` plus `ssh -L 8000:localhost:8000 sesterce-a100` shows the pages locally. To update the
published exp12 page, publish `examples/exp12_position_map/artifact.html` with `slices/*` as files to its URL.
GPU memory: Qwen3.5-4B fits a 24 GB card; Qwen3.6-27B needs 1x 80 GB (bf16 weights ~54 GB + two fp32 lens maps
~13 GB).

To fetch a model and its lenses ahead of a run (retries on HF 429s; put `HF_TOKEN` in `.env`):
`uv run python scripts/prefetch.py configs/models/qwen3.6-27b.yaml`.

## Status
Draft, UNVERIFIED: nothing is in `VERIFIED.md` yet. The STATE block in `AGENTS.md` tracks what is in flight.
Final figures, numbers and examples per experiment: [results/README.md](results/README.md).

**Final figures (Qwen3.6-27B).**
| Figure | What it shows |
|---|---|
| [exp12 `two_step.png`](figures/exp12_position_map/two_step.png) | **Headline.** Where in the prompt and how deep the bridge and the answer are readable; the ~21-layer lag |
| [exp12 `position_layer_jlens.png`](figures/exp12_position_map/position_layer_jlens.png) | J-lens heatmaps, prompt position x layer, for the bridge and the answer |
| [exp12 `by_offset.png`](figures/exp12_position_map/by_offset.png) | Share of layers 32-48 with each word on top, per prompt position, all three readers |
| [exp12 `position_layer.png`](figures/exp12_position_map/position_layer.png) | The heatmaps for all three readers |
| [exp11 `pool_top1_by_layer.png`](figures/exp11_bridge_vs_answer_by_layer/pool_top1_by_layer.png) | Last token only: bridge and answer on top, by layer, three readers |
| [exp11 `advantage_by_layer.png`](figures/exp11_bridge_vs_answer_by_layer/advantage_by_layer.png) | Last token only: how far each word ranks above its same-category distractor |
| [exp10 `pass_at_10_by_model.png`](figures/exp10_lens_sanity/20261013-230247/pass_at_10_by_model.png) | Does each lens read the intermediate at all (pass@10, 4B and 27B) |
| [exp10 `27b_by_layer.png`](figures/exp10_lens_sanity/20261013-230247/27b_by_layer.png) | Why the J-lens looks no better than the logit lens on pass@10 |

Worked examples with lens tables: `make examples-serve` opens [examples/index.html](examples/index.html) (all three
experiments); the exp12 page is also published at https://claude.ai/artifact/TXLZH6WxuxSQDhoK5YHTj9 (private; share it
from the page).

**What we know so far (Qwen3.6-27B, the 67 two-hop questions it answers correctly).**
1. The J-lens and J++ can read the bridge; the plain logit lens mostly cannot before the last layers (exp10, exp11).
2. The bridge is readable earlier than the answer, both in the prompt and in depth: it builds up on the last words
   before "is" from about layer 20, while the answer appears only at the last token from about layer 44 (exp12).
3. Where the bridge is readable, part B's swaps also show it is used (J-mediated questions read better), but the
   groups are small.
4. The original "J-lens cannot see the bridge" is mostly where and how we looked: compared with the whole vocabulary
   at the last token it is often missed; compared with other entities, or one word earlier, it is usually there.

### exp10_lens_sanity: does the lens work on Qwen at all?
**What we measure.** We give the model a two-hop question, e.g. "The language spoken in the country where the Amazon
River ends is" (answer Portuguese, bridge Brazil). At the last prompt token we ask each *reader* for its ranked word
list at every layer, and count how often the bridge is in the top 10 at some layer (pass@10). Three readers: the
**logit lens** (simplest; the baseline), the **J-lens**, and **J++** (an improved J-lens).

**In short.**
- **Qwen3.5-4B:** the J-lens sees the bridge more often than the baseline.
- **Qwen3.6-27B:** J++ clearly beats the baseline (0.75 vs 0.51 with the space stripped). The J-lens is only slightly
  ahead, within the error bars.
- **The bridge is often invisible at the last token.** On the 61 items 27B answers correctly, J++ misses the bridge in
  1 of 3 and the J-lens in 1 of 2. This is Zach's observation. The next experiment checks earlier tokens.

![pass@10 by model and reader](figures/exp10_lens_sanity/20261013-230247/pass_at_10_by_model.png)

*Share of two-hop questions where each reader has the bridge in its top 10 at the last prompt token (84 questions
with single-token bridges; bars are 95% CIs). Qwen3.5-4B has no J++ lens. "Prompt as published" keeps the trailing
space of the original prompts; "space stripped" removes it (pitfall 1).*

**Why the J-lens looks no better than the baseline on 27B.** In the middle layers (shaded) only the J-lens and J++
see the bridge; near the output the logit lens catches up. pass@10 takes the *best* layer, so the late layers hide
the difference.

![27B by layer](figures/exp10_lens_sanity/20261013-230247/27b_by_layer.png)

*Same questions, Qwen3.6-27B, space stripped: share of bridges in each reader's top 10, layer by layer.*

<details><summary>Full numbers</summary>

pass@10 on the 84 single-token items, 95% percentile bootstrap CI over items (n_boot=10000, seed 0). Runs are under
`results/exp10_lens_sanity/`. All sanity checks pass on both models (HF parity and our readout vs `jlens.apply`:
max abs diff 0.0).

| Model | Prompt end | Model correct | Logit lens | J-lens | J++ | J-lens - logit | J++ - logit | Run |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-4B | as published (`" "`) | 18/93 | 0.40 [0.30, 0.50] | 0.57 [0.47, 0.67] | - | +0.17 [+0.08, +0.27] | - | `20261013-205029` |
| Qwen3.5-4B | stripped (`" is"`) | 50/93 | 0.24 [0.15, 0.34] | 0.43 [0.33, 0.54] | - | +0.19 [+0.10, +0.29] | - | `20261013-205057` |
| Qwen3.6-27B | as published (`" "`) | 21/93 | 0.60 [0.49, 0.70] | 0.59 [0.49, 0.69] | 0.83 [0.75, 0.90] | -0.01 [-0.08, +0.07] | +0.23 [+0.14, +0.33] | `20261013-205736` |
| Qwen3.6-27B | stripped (`" is"`) | 61/93 | 0.51 [0.40, 0.61] | 0.57 [0.46, 0.67] | 0.75 [0.65, 0.84] | +0.06 [-0.05, +0.17] | +0.24 [+0.13, +0.35] | `20261013-205936` |

On the items the model answers correctly (27B, stripped, n=61): J++ 0.67 [0.56, 0.79], J-lens 0.48 [0.36, 0.61].
Controls (27B, stripped, rank at the last token): Brazil 0 vs distractor Mexico 57 (J-lens) / 45 (J++); Hungary 1 / 0
vs Poland 16 / 18. Figures: `uv run python -m scripts.exp10_lens_sanity.plot --summary`.
</details>

### exp11_bridge_vs_answer_by_layer: where is the bridge readable, and where the answer?
**What we measure.** The 90 probe-swap questions of part B, prompts as published; the headline uses the 67 the model
answers correctly (part B's `eligible`; our check agrees on all 83 items with a single-token answer). At the last
prompt token, at every layer, we ask each reader: is the bridge (Brazil) the top candidate among all 97 entities of
the set, and is the answer (Portuguese) the top candidate among all 112 answers? The same-category distractors
(Mexico, Spanish) are the controls. Chance is about 1%.

**In short.**
- **J-lens and J++ read the bridge in the middle layers; the logit lens only near the output.** Averaged over
  layers 32-48 the bridge is top-1 among entities in 59% of questions (J-lens), 56% (J++), 26% (logit lens);
  its distractor in 6%. This reproduces part B's `gate_debug` (0.55-0.70).
- **The bridge comes first, the answer later, but they overlap.** Half the questions have the bridge on top by
  layer 34; the answer gets there by layer 43 (J-lens, 8 layers later [4, 18]) or 47 (J++, 11 [5, 18]). There is
  no clean hand-off: the bridge stays on top until about layer 60, and per question the bridge settles on top
  before the answer in only 57% [45, 70] of cases (J-lens).
- **Where the bridge is readable, it is also used.** On the 25 questions where part B's J-space swap flips the
  answer, the J-lens has the bridge on top in 79% [66, 89] of layers 32-48; on the 40 where no swap works, 49%
  [35, 62]. Suggestive: the intervals nearly touch.

![exp11: top-1 share by layer](figures/exp11_bridge_vs_answer_by_layer/pool_top1_by_layer.png)

*Last prompt token, 67 questions the model answers correctly. Blue: share of questions where the bridge is the top
entity; orange: where the answer is the top answer; grey: the same for their distractors (controls); dotted:
chance. Shaded: the layer bands the summary averages over (32-48 fixed in advance from part B; 28-52 exploratory,
which changes nothing: 58% vs 59%).*

**What this does not show.** A lens shows what can be read out at a layer, not when it was computed. And this is
one token: the first hop may happen earlier in the prompt (at "Amazon River ends"), which exp11 does not look at.
About 40% of questions do not have the bridge on top at the last token; exp12 looks at the earlier tokens.

<details><summary>Full numbers</summary>

Run `20261014-092835` (prompts as published, Qwen3.6-27B @ `192d8cb`), re-aggregated in
`results/exp11_bridge_vs_answer_by_layer/20261014-092835/analysis-20261014-113947/summary.json` (`analyze`; the run's own `summary.json` predates the bands and order metrics).
Eligible n=67, band 32-48, 95% percentile bootstrap CI over questions (n_boot=10000, seed 0).

| Reader | Bridge top-1 | Answer top-1 | Bridge distractor top-1 | Bridge above distractor (vocab) | 50% crossing: bridge / answer (lag) |
|---|---|---|---|---|---|
| logit lens | 0.26 [0.17, 0.35] | 0.13 [0.08, 0.20] | 0.04 | 0.80 [0.72, 0.87] | L49 / L52 (2 [-4, 4]) |
| J-lens | 0.59 [0.49, 0.68] | 0.41 [0.32, 0.50] | 0.06 | 0.84 [0.76, 0.91] | L34 / L43 (8 [4, 18]) |
| J++ | 0.56 [0.46, 0.65] | 0.38 [0.29, 0.47] | 0.06 | 0.85 [0.78, 0.92] | L34 / L47 (11 [5, 18]) |

Space-stripped prompts (run `20261014-093050`) give the same picture (J-lens bridge 0.56, lag 8 [3, 16]). On the 21
eligible questions whose prompt ends in a space the answer is read less often (J-lens 0.24 vs 0.49 without the
space); the bridge less so (0.53 vs 0.62).
</details>

### exp12_position_map: where in the prompt, and how deep?
**What we measure.** The exp11 readout (is the word the top candidate in its pool?) at every token of the prompt, not
just the last. Prompts differ in length, so tokens are aligned by their distance from the last word: 0 is the last
word (usually "is"), -1 the word before it (e.g. "located", "ends"), and so on. The best position for each reader is
picked on a random half of the questions and checked on the other half, because the best of 15 positions looks better
than it is on the data that picked it; the same search for the distractor (Mexico) shows how high noise alone gets.

**In short.**
- **The bridge is read best one word before the end; the answer only at the end.** J-lens: the bridge is on top in
  66% of layers 32-48 at position -1 (56% at the last word); the answer in 41% at the last word and at most 24%
  anywhere earlier. Both halves of the data pick the same positions. Noise ceiling: 12%.
- **The bridge comes about 20 layers before the answer.** Read where each is strongest, half the questions have the
  bridge on top by layer 23 and the answer by layer 44: 21 layers later [16, 28] (J++: 20 vs 43, 23 [18, 32]).
  Read at a single token (exp11) the two overlapped; this is the step that one token hides.
- **Most last-token misses are a read-site effect.** Of the 26 questions where the J-lens does not have the bridge on
  top at the last token, 73% [54, 88] have it on top at an earlier token (distractor, same search: 35% [15, 54]).

![exp12: where and how deep](figures/exp12_position_map/two_step.png)

*Left: share of layers 32-48 in which the word is the top candidate, at each prompt position (label: the most common
token there). Right: share of questions with the word on top at each layer, the bridge read at position -1 and the
answer at the last word; dots and arrow: where each reaches half the questions. Thick: J-lens (shaded 95% CI); thin:
J++. Grey band: layers 32-48.*

**What this does not show.** Positions are aligned by distance from the end, not by meaning: in the 44 prompts that
end in "is" the bridge peaks on the word before it (75%), in the 23 others it has no clear peak. The ordering holds
for the group of questions, not reliably for each one. A lens shows what is readable, not what is computed.

<details><summary>Full numbers and checks</summary>

Run `20261014-095358` (Qwen3.6-27B @ `c373821`, prompts as published), analysed in `results/exp12_position_map/20261014-095358/analysis-20261014-121341/summary.json`.
Eligible n=67; positions -14..0 analysed (reached by at least half the questions; -11..0 by 66-67).

| Reader | Bridge: best position | Share of layers 32-48 [95% CI] | Held-out halves (position: share) | Answer: best position | Share | Distractor ceiling |
|---|---|---|---|---|---|---|
| logit lens | -3 | 0.40 [0.30, 0.51] | -1: 0.31, -3: 0.37 | 0 | 0.14 [0.09, 0.21] | 0.05 |
| J-lens | -1 | 0.66 [0.55, 0.76] | -1: 0.62, -1: 0.70 | 0 | 0.41 [0.32, 0.51] | 0.12 |
| J++ | -1 | 0.66 [0.56, 0.76] | -1: 0.62, -3: 0.63 | 0 | 0.40 [0.30, 0.49] | 0.10 |

- Depth (half the questions on top, bridge at its best position vs answer at the last word): J-lens L23 vs L44, lag
  21 [16, 28]; J++ L20 vs L43, 23 [18, 32]; logit lens L24 vs L51, 27 [-5, 30].
- Same optimum on the balanced panel (the 66 questions that reach every position -11..0), so prompt length does not
  drive it.
- Read at position -1, part B's J-mediated questions have the bridge on top in 0.79 [0.63, 0.92] of layers 32-48,
  "neither" questions in 0.60 [0.46, 0.74] (J-lens).
- Missed at the last token: J-lens 26 questions, bridge on top earlier in 73% [54, 88] (distractor 35% [15, 54]);
  J++ 26, 81% [65, 96] (distractor 31% [15, 50]).

![exp12: J-lens heatmaps](figures/exp12_position_map/position_layer_jlens.png)
</details>

### exp02_swaps (part B): does the bridge act through the J-space, and where?
**What we measure.** In "The capital of the country where Naples is located is" the model answers Rome through the
bridge Italy. We swap the bridge's representation for another entity's (Italy -> Spain) at layers 24-40 and count how
often the answer becomes the other entity's (Madrid). The swap uses one part of the bridge's probe at a time: its
J-space part, its remainder, or the remainder with the J-space coordinates held fixed. Each swap has a control: a
random direction of the same edit size. v4 runs the swaps with the J-lens and with J++ on the same probes, on the 77
questions the model answers correctly (stripped prompts, answers judged on the greedy continuation).

<img width="1768" height="663" alt="image" src="https://github.com/user-attachments/assets/dd0a772d-d752-4fa7-9035-4611339735e4" />

**In short.**
- **The bridge acts through the J-space.** Swapping only the J-space part flips 52% of answers with J++ and 35% with
  the J-lens; the remainder flips 8% / 12%, and 1% / 4% with the J-space held fixed. Controls flip at most 3%. Claude
  (Gurnee et al. 2026): 61% / 28% / 6%.
- **J++ closes most of the gap to Claude.** On identical probes, J++'s J-space part carries much more of the swap
  than the J-lens's (52% vs 35%), so the J-lens's smaller effect is largely the lens, not a route outside the
  workspace.
- **It is the lens's direction, not how much of the probe it carries.** Directions with the same cosine to each probe
  as its J-space part, but random otherwise, flip 14% (J++) / 10% (J-lens) against the J-space part's 52% / 35%
  (paired difference +38 [+27, +49] / +25 [+16, +34] pts), although their edits are three times larger. Within each
  lens, edit size does not predict which questions flip, and J++ flips more than the J-lens at every edit size.
- **The swap acts at the cue phrase, not where the bridge is read.** Swapped only at the words that name the bridge's
  cue ("Naples", "emperor defeated at Waterloo"; `data/cue_spans.json`), the J-space part flips 31% (J++) / 19%
  (J-lens); at the other earlier words ("The capital of the country where"), 1% / 1%; only at offset -1, where exp12
  reads the bridge best, 9% / 3%; only at the last token, 8% / 4%.
- **It works when the bridge is a place or a person.** J++: 88% of questions whose bridge is a country or place,
  86% for people (n=7), 25% for everything else (elements, organs, animals, dates). The J-lens matches J++ on places
  (85%) but not on people (14%).

![exp02 v4: J-space part vs remainder](figures/exp02_swaps/v4b/jpart_vs_remainder.png)

![exp02 v4: where in the prompt the swap acts](figures/exp02_swaps/v4b/swap_position.png)

<img width="1360" height="612" alt="image" src="https://github.com/user-attachments/assets/54ba8646-a9f5-4676-ab9b-0bfb1510cf55" />


**What this does not show.** The runs are exploratory, one seed, n=77. The control matches each layer's edit size,
not the total over layers (the real swap's later edits shrink, the control's do not), so it is stricter for flips and
overstates collateral damage. Positions are counted back from the last token, as in exp12, so offset -1 is a
different word in different prompts.

<details><summary>Full numbers and checks</summary>

Runs under `results/exp02_swaps/`: `gate_v4`, `main_v4_{jlens,jpp}` (layers 24-40, the gate's pick),
`main_v4_{jlens,jpp}_32-48` (part A's band, set by hand),
`main_v4_{jlens,jpp}_pos-{prev,last,last_two,earlier,cue,earlier_noncue}`.
Probes: `exp01_probes/v3_jpp` (v3's prompts rebuilt on the H200: 11 of 2673 filter decisions differ from v3) and
`v3_jlens` (the same probes, decomposed over the J-lens). Flip rate, Wilson 95% CI, n=77:

| Swap (all positions) | J-lens 24-40 | J++ 24-40 | J-lens 32-48 | J++ 32-48 |
|---|---|---|---|---|
| raw lens vectors | 40% [30, 51] | 49% [38, 60] | 48% [37, 59] | 55% [43, 65] |
| full probe | 27% [19, 38] | 27% [19, 38] | 25% [16, 35] | 25% [16, 35] |
| J-space part | 35% [25, 46] | 52% [41, 63] | 34% [24, 45] | 44% [34, 55] |
| remainder | 12% [6, 21] | 8% [4, 16] | 12% [6, 21] | 10% [5, 19] |
| remainder, J-space held | 4% [1, 11] | 1% [0, 7] | 1% [0, 7] | 3% [1, 9] |

| J-space part swapped only at | J-lens | J++ |
|---|---|---|
| the cue phrase (median 5 tokens) | 19% [12, 30] | 31% [22, 42] |
| the other earlier words (median 7 tokens) | 1% [0, 7] | 1% [0, 7] |
| the earlier words (both of the above) | 23% [15, 34] | 35% [25, 46] |
| offset -1 | 3% [1, 9] | 9% [4, 18] |
| offset 0 | 4% [1, 11] | 8% [4, 16] |
| offsets -1 and 0 | 10% [5, 19] | 17% [10, 27] |
| every position | 35% [25, 46] | 52% [41, 63] |

| Bridge is | n | J-lens | J++ |
|---|---|---|---|
| a country or place | 26 | 85% [66, 94] | 88% [71, 96] |
| a person | 7 | 14% [3, 51] | 86% [49, 97] |
| anything else | 44 | 9% [4, 21] | 25% [15, 39] |

- Paired bootstrap, J-space part minus remainder: J-lens +23 pts [+13, +35], J++ +44 [+32, +56] (layers 24-40).
- Matched-alignment control (`matched_v4_{jpp,jlens}`, layers 24-40; decision rule fixed in the manifests): per entity
  and layer, a unit direction with the J-space part's cosine to the probe, the rest random. Flips: J++ 14% [8, 24]
  (J-space part 52% [41, 63]), J-lens 10% [5, 19] (35% [25, 46]); random-direction nulls 0%. Median edit: 0.049 /
  0.044 of the norm vs the J-space part's 0.016 / 0.014. The J-space part's rates reproduce `main_v4` item for item.
- Edit size (`exp02_swaps/analysis/edit_size_v1/report.md`, from `main_v4` outcomes): the J-space part's edit is the
  smallest of the probe swaps (median 0.016 / 0.014 vs 0.074-0.090) and flips most; within a lens, a flipped
  question's edit is no larger than a kept one's (AUC 0.48 J++, 0.49 J-lens); J++'s edits are 21% larger per
  question, but J++ flips more in every edit-size quartile, and flips every question the J-lens flips (13 vs 0,
  exact McNemar p = 0.0002).
- The full probe uses no lens: its outcomes are identical item by item in the J-lens and J++ runs.
- Every run's report (`results/exp02_swaps/analysis/<run>/REPORT_auto.md`) lists edit sizes, collateral damage and
  the files to recompute from. Supplementary figures in `figures/exp02_swaps/v4b/` (`v4/` is the same set before
  the cue runs): `lens_comparison.png`,
  `positions.png`, `outcomes.png`, `dose.png`, `per_question.png`, `examples.png`, `by_bridge_type.png`.
</details>

### exp03_brew_swaps (part B): an in-context two-step lookup
**What we measure.** In brew the prompt gives a colour table and a start colour; the answer is two lookups away
(blue -> green -> black), so the counterfactual answer of any edit can be read off the table and no prior knowledge is
involved. 100 items from WorkspaceBench's `brew_intermediates` bank, gated on Qwen3.6-27B; 99 have a valid swap
target, 94 a valid alternative start. We swap and steer along the colours' J-lens and J++ vectors and read which
colour the model answers after the bank's "Answer:" prefill.

**In short.**
- **Swapping the start colour redirects the computation; swapping the intermediate does not.** exp02's coordinate swap
  as is moves no answer here, positive controls included (0-1% at every band). Amplified 3x at layers 8-24, swapping
  the start colour S for S' makes the model answer f(f(S')) for 61% [51, 70] of items with J++ (J-lens 17% [11, 26];
  random direction 0-1%), while swapping the intermediate I for X, at the same layers and strength, gives f(X) for 0%
  [0, 4] after the start line and 3% [1, 9] at every position (random direction 0%). With the positive control
  working, this is a null: where and how we edit, the intermediate is not carried along its lens direction (or is
  recomputed downstream of the edit).
- **Steering the start line redirects the whole computation, and replicates on fresh items.** Adding 3% of the
  residual norm along J++'s S' - S at the start line (layers 8-24), the model answers f(f(S')), both lookups from the
  new start, for 56% [46, 66] of the bank's items (J-lens 20%); one lookup, f(S'), for a further 19%; S' itself for
  5%. The layers and sizes were picked on these items, so the same steering was rerun on 200 fresh items in the bank's
  format (164 usable): 63% [55, 70] at 3% (J-lens 30% [24, 38]), random direction 0% [0, 2]. The effect needs about 2%
  of the norm, peaks at 3-5% and fades above (larger edits break the answer), is weaker at layers 16-32 and absent at
  36-52.
- **Steering after the start colour only ever makes the model say X.** Along X - I at the positions after the start
  line, the answer becomes X itself (100% at 20% of the norm, layers 36-52) and almost never f(X) (1 item of 99 at one
  setting, 0 at every other size, band and lens). There, where the J-lens reads the intermediate, its direction acts as a candidate answer, not as a step:
  consistent with WorkspaceBench's caveat that the brew intermediate is usually the model's runner-up answer.

![exp03: swaps, amplified](figures/exp03_brew_swaps/v2_swaps/swaps_amplified.png)

![exp03: steering the start line](figures/exp03_brew_swaps/v1/steering_start_line.png)

**What this does not show.** That the model does not compute the intermediate serially: the intermediate swap is
tested at layers 8-24 only, and steering after the start line only produces an output; neither reaches an
intermediate held in another direction or at other layers. The amplified swaps' random directions edit more than the
real swaps (median 0.05-0.1 of the norm vs 0.02-0.03), since they are re-added at every layer while the real clamp
settles; that makes the nulls stronger, not weaker. Steering is not dose-matched to exp02's swaps (about 1% of the
norm). One seed, one model; S' and X are drawn per item with a fixed seed.

<details><summary>Full numbers and checks</summary>

Runs under `results/exp03_brew_swaps/`: `sweep` and `main` (intermediate swaps, all regimes), `followup` (positive
controls, swaps at 16-32 and 36-52, steering after the start), `start_steer` and `start_steer_low` (steering the start
line), `swap_amp` (start and intermediate swaps at 8-24, amplified 1x/3x/5x), `fresh_steer` (start-line steering on
`data/brew_fresh.json`, from `exp03_make_items.py`; decision rule fixed in its manifest). `swap_early` is `swap_amp`
with a bug: its amplification multiplied the edit at every layer, which compounded (edits of 1.4-3.9x the residual
norm), so its 3x and 5x rows are void. Our render puts the start line and the last token on the bank's labelled cells for every item
(`render_matches_bank` in `items.jsonl`). Figures: `figures/exp03_brew_swaps/v1/`, `v2_swaps/`, `v2_fresh/` (`exp03_figures.py`; categories are
read off each item's table, and an unchanged answer counts as "original" even where one lookup from S' lands on it).

| Start line steered along S' - S, layers 8-24, n=94 | 1% | 2% | 3% | 5% | 10% | 20% |
|---|---|---|---|---|---|---|
| J++: f(f(S')) | 0% | 40% | 56% [46, 66] | 48% [38, 58] | 27% | 14% |
| J-lens: f(f(S')) | 0% | 9% | 20% | 30% [21, 40] | 17% | 11% |
| random direction: answer changed | | | 0% | 0% | | 12% |
| fresh items (n=164), J++: f(f(S')) | | | 63% [55, 70] | 49% [42, 57] | | |
| fresh items, J-lens: f(f(S')) | | | 30% [24, 38] | 35% [28, 43] | | |
| fresh items, random direction: answer changed | | | 0% [0, 2] | 0% [0, 2] | | |

| Swaps at layers 8-24, predicted answer reached | 1x | 3x | 5x |
|---|---|---|---|
| start S -> S' (start line, n=94), J++ / J-lens | 0% / 0% | 61% / 17% | 51% / 32% |
| random direction | 0% / 0% | 1% / 0% | 3% / 2% |
| intermediate I -> X (after the start line, n=99), J++ / J-lens | 0% / 0% | 0% / 0% | 1% / 0% |
| intermediate I -> X (every position), J++ / J-lens | 0% / 0% | 3% / 1% | 3% / 0% |
| random direction (every position) | 0% / 0% | 0% / 2% | 18% / 5% |
</details>

### exp04_brew_patch (part B): where brew carries its intermediate, without a lens
**What we measure.** exp03's lens edits of the intermediate moved no answer. To see whether there is anything there to
edit, we copy activations from a counterfactual prompt into the original run, one layer and one group of positions at a
time, with no lens involved. In the counterfactual the start colour's rule gives exp03's X instead of I, and X's rule
gives a new colour c. If the copied positions carry X as the intermediate, the second lookup still reads the original
table and the answer becomes f(X); if they already carry the answer, it becomes c. A control copies from a prompt whose
two changed rules are off the path. 82 of exp03's 99 bank items are eligible (the model answers the original, the
counterfactual and the control correctly); every second layer.

**In short.**
- **The intermediate is carried after the start line, at layers 36-50.** Copying the positions after the start line
  (the question, the chat scaffolding, "Answer:") gives f(X) for 11% of items at layer 36, rising to 48% [37, 58] at
  layers 46-50; from layer 52 the same copy gives c (71%, then 93-99% from layer 56). The start line itself carries
  neither at any layer. The window fixed before the run (f(X) above c and above the control, Wilson intervals not
  overlapping) is layers 36-50 for the positions after the start line and 46 and 50 for the last token alone. The
  control changes at most 2% of answers anywhere.
- **The rules are read at layers 28-36.** Copying the two changed rule lines gives c up to layer 28 (87-100%) and the
  start colour's rule alone gives f(X) (78-89% to layer 24); both stop working by layers 36-40.
- **Lens edits in the same window write the answer, not the step.** exp03's steering along v_X - v_I at these positions
  and layers (36-52) made the model say X itself (33-100% of items) and never f(X) (0 of 99 at every size, both
  lenses), at sizes like the copy's (it changes 7-14% of the norm there). The intermediate is there to be edited, but
  not along the colour's lens direction.
- **The step is carried outside the J-space** (`parts_window`, decision rule fixed in its manifest). At the window,
  copying only a part of the difference δ = h_C - h_B: its projection onto the lens vectors of I and X gives f(X) at
  0% of window layers (0.2% of δ's variance), the rest 31%, the same as the whole copy (31%); its J-space part (a
  25-atom signed decomposition over the lens's vectors) gives 0%, the rest 26% (J++) / 24% (J-lens). Paired
  difference, rest minus part: +31 [+24, +38] and +26 [+20, +32] pts with J++, alike with the J-lens; every part's
  random-direction null 0%. The J-space part holds 8% of δ's variance, what it holds of a random direction (7%).
- **Both replicate on 154 held-out items** (`patch_map_fresh`, `parts_window_fresh`: exp03's fresh items, the same
  seeds and decision rules; the rule lines patched at layer 0 only, as positive controls). The same rule again puts
  the window after the start line at layers 36-50 (f(X) 10% at layer 36, 52% [44, 60] at layer 48; from layer 52 c,
  68%, then 88-100% from layer 56) and at 44-50 for the last token; the control changes at most 6% of answers (layer
  50). At that window the whole copy scores 31%; the I/X lens coordinates 0%, the rest 31% (+31 [+26, +36] pts with
  both lenses); the J-space part 0%, the rest 28% (J++, +28 [+24, +33]) and 26% (J-lens, +26 [+22, +31]); every null
  0%. The J-space part again holds about what it holds of a random direction (8% of δ's variance; chance 7%).
- **Before the step shows, the copy often stops the model at the first lookup.** At layers 36-46 the copy after the
  start line makes the model answer the original intermediate I (f(S), one lookup instead of two) for 20-29% of bank
  items and 27-43% of fresh items; at layers 48-50, where f(X) peaks, for 16% and 6-7%. Neither decision rule counts
  this; we saw it after the fact. It goes with the same part of δ as the step: on the fresh items the rest gives I in
  28-30% of item x layer cells at the window, the J-space part in 1-2%, the I/X lens coordinates in under 1%, the
  nulls in under 2%.
- **The step is read from 4 of the 21 positions: the ones where the lens reads I** (`positions_window`, run after
  exp08). Copying C's activations only at " the", the newline after "assistant", the "\n\n" after "</think>" and
  the final ":" gives f(X) at 33% of window layers (fresh; bank 31%), as much as all 21 (31%, 31%); the other 17
  give 0%, and O's copy at the 4 gives 0%. No single one does it alone: the newline after "assistant" 3%, the
  "\n\n" 0% (the last token alone peaked at 36% at layer 50 in the map).

![exp04: patching map](figures/exp04_brew_patch/v1/patch_map.png)

![exp04: parts of the copy](figures/exp04_brew_patch/v2_parts/parts.png)

![exp04: patching map, fresh items, with I](figures/exp04_brew_patch/v3_fresh_map/patch_map.png)

![exp04: which positions carry the step](figures/exp04_brew_patch/v5_positions/positions.png)

**What this does not show.** Which direction carries the step, beyond "not the J-space": the copy replaces whole block
outputs at about 21 positions. 48-52% is the best single-layer copy, not a ceiling: information held at several layers
at once is missed by every single-layer copy. The J-space part is small (8% of δ's variance) and was not tried
amplified; it is a decomposition of the difference δ, not of each activation. Within each item set the window and the
parts test use the same items; the fresh map found the bank's window, so the fresh parts test also runs at a window
found on other items. One seed for c and the control's colours, the same in both sets. What the I answers mean is
open.

<details><summary>Full numbers and checks</summary>

Runs: `results/exp04_brew_patch/patch_map` (manifest written before the run; layers 0-62 in steps of 2, chosen by the
human) and `parts_window` (the window read from `patch_map`'s decision; its full copy reproduces `patch_map` in all
656 item x layer cells; variance shares in `fve.jsonl`). Per-layer rates of every role for each group, and the off-path control, are in `summary.md`; the first answer
token's log-probabilities in `figures/exp04_brew_patch/v1/patch_logp.png`. Eligibility: 13 items fail on the
counterfactual and 4 on the control prompt. 52 of the 82 items give f(X) at one window layer or more. Headlines are
recomputed by `scripts/verify_headlines.py`.

Fresh items: `patch_map_fresh` (manifest written before the run; after the start line and the last token at every
second layer, the two rule-line positive controls at layer 0, chosen by the human) and `parts_window_fresh` (its
manifest written from `patch_map_fresh`'s decision; its full copy reproduces the map in all 1232 item x layer cells).
Of the 200 fresh items, 154 are eligible: they are not gated, so 25 fail on the original prompt, 18 on the
counterfactual, 2 on the control, and 1 has no X. Positive controls at layer 0: the rule lines give c for 100% and the
start colour's rule gives f(X) for 92%, the control changes at most 1%. 97 of the 154 give f(X) at one window layer or
more. Figures: `figures/exp04_brew_patch/v3_fresh_map/` (the map figure draws I from this version on) and
`v4_fresh_parts/parts.png`.

Positions: `positions_window` (manifest written before the run; the human chose the run; bank and fresh items as
exp04): C's copy at subsets of the 21 positions after the start line, O's copy at the same positions as the control.
Its 'all' copy reproduces exp04's full copy item for item (1232/1232 fresh, 656/656 bank). The groups came from
exp08's readouts on the same items. Figure: `figures/exp04_brew_patch/v5_positions/`.
</details>

### exp06_sigma_writes (part B): read with the lens, write along the covariance?
**What we measure.** A lens vector is a gradient, roughly a whitened direction (Stein's lemma: Σ⁻¹ Cov(h, logit)). If
so, the edit that moves the lens's reading most naturally, in units of how activations vary, runs along Σv, not v.
Two tests, with Σ the covariance of block outputs over 100,156 WikiText-103 test positions (the lens's own kind of
text): (1) exp02's matched-alignment control again, with the matched direction's rest drawn from N(0, Σ) instead of
isotropically: does the J-part's lead come from how natural its direction is? (2) exp03's fresh-item steering of the
start colour (S to S', layers 8-24) along Σ_λ (v_S' - v_S), from λ = 1 (the lens's own direction) to λ = 0 (pure Σv),
at the same Euclidean size.

**In short.**
- **The J-part's lead in exp02 is not about how natural the matched direction is.** With the rest drawn from the
  covariance, the matched swaps flip 12% [6, 21] (J++) and 14% [8, 24] (J-lens) of 77 items, no more than the isotropic
  version (14% and 10%; difference -3 [-12, +6] and +4 [-4, +12] pts), against the J-part's 52% and 35% (J-part minus
  covariance-shaped: +40 [+27, +53] and +21 [+9, +32]). The covariance-shaped swaps move the activation about ten times
  as much as the J-part's (median 17% of the residual norm vs 1.6%) and keep the original answer for only 44% of items:
  bigger, more damaging edits, not more flips. By the manifest's rule, the gap is the lens's direction.
- **Writing along Σv is worse than writing along v.** At 3% of the residual norm, J++ steering gives f(f(S')) for 63%
  [55, 70] of 164 fresh items along the lens's own direction, 13% at λ = 0.5 and 3-4% at λ = 0.1 and 0 (-50 to -60
  pts); at 5%, 49% against 34%, 23% and 21%. The J-lens: 30% against 1% at 3%. Random directions: 0%. The
  covariance-shaped directions are far from the lens's (median cosine 0.29-0.44) and at 3% leave the original answer
  for 54-77% of items, against 7-18% along the lens's direction.

![exp06: writing along the covariance](figures/exp06_sigma_writes/v1/sigma_writes.png)

**What this does not show.** Σ is WikiText's covariance, not that of the two-hop or brew prompts. Sizes are Euclidean:
at a matched Mahalanobis size the covariance-shaped edits would be larger. The steering is at the start line, where
the lens's own direction already works; at exp04's window, where it does not, exp07 tries Σ-shaped and fitted
directions.

<details><summary>Full numbers and checks</summary>

Run: `results/exp06_sigma_writes/sigma_v1` (manifest written before the run, with the decision rules; the human chose
the run). Its J-part and isotropic rows reproduce exp02's `matched_v4` item for item (77/77 per lens), and λ = 1
reproduces exp03's `fresh_steer` for 162-164 of 164 items. The covariance-shaped condition's random null flips 4% [1,
11] (the others 0-1%), with edits as large as the condition's. Figure: `uv run python scripts/exp06_figures.py <new
folder> sigma_v1`. Headlines are recomputed by `scripts/verify_headlines.py`.
</details>

### exp07_step_code (part B): a code for brew's intermediate, fit on other items, writes the step; the lens's direction does not
**What we measure.** exp04's "outside the J-space" rests on splitting the copy δ, which carries everything that differs
between the two prompts; its J-space part held only chance-level variance, so the split could have missed a small
J-space component of the intermediate. Here the intermediate gets its own direction, as exp01's probe gave the bridge
one for exp02: on 883 new brew items the model answers (`data/brew_fit.json`, never a test prompt), a ridge fit of the
activations after the start line (each of the 21 positions, layers 36-50) on the start, intermediate and answer
colours. The intermediate's coefficients E_I[k] are its code; E_I[X] - E_I[I] moves an item's intermediate from I to X
with the start and the answer held fixed. On exp04's eligible items we add it at one window layer at a time, at the
copy's size, next to the copy itself, a random direction, the lens direction v_X - v_I, two Σ-shaped versions of it
(exp06), and the code's J-space part and the rest.

**In short.**
- **The code writes the step as well as the copy does; the lens direction does not.** On the 154 fresh items, adding
  E_I[X] - E_I[I] at the copy's size gives f(X) at 34% of window layers (the copy 31%, random 0%); the lens direction
  at the same size 1% (code minus lens: +33 [+27, +38] pts with J++, alike with the J-lens). Bank items (n=82): code
  25%, copy 31%, lens 1%. At its own size (median 0.45 of the copy's) the code gives 4% (+4 [+2, +6] over random).
- **The code is outside the J-space.** Its J-space part (25 atoms) gives 0%; the rest gives 29% (J++) and 27% (J-lens)
  on fresh items, 20% and 18% on the bank: "outside" by exp04's rule, both lenses, both item sets. The code is nearly
  orthogonal to the lens direction (median cosine 0.02), and its J-space part holds 9-11% of its squared norm, about
  what it holds of a random direction (7%).
- **The code reads the intermediate.** Decoded from each held-out item's own activations, it names the intermediate for
  76-93% of items per layer (chance 8%).
- **Σ-shaping does not rescue the lens.** Σ_λ (v_X - v_I) at λ = 0.5 and 0 gives 1%, like the lens direction
  (differences within [-2, +1] pts); the code's cosine to them is 0.02-0.03.
- Like the copy, the code also makes the model answer I (one lookup) in 25% of fresh item x layer cells (the copy 29%,
  the lens directions 2-6%).

![exp07: a code for the intermediate](figures/exp07_step_code/v1/step_code.png)

**What this does not show.** Whether the lens can read the intermediate at these positions: the code is orthogonal to
the lens's direction for X - I, which says the lens cannot write the step, not that it cannot see I (the lens's
readout of I there is not measured yet). The code works at about twice its own size; at its own size it writes the
step for 4%. One layer at a time (exp03's steering, which made the model say X, edited all window layers at once). One
fit (883 items, ridge 1.0); the decoding check uses each item's start and answer.

<details><summary>Full numbers and checks</summary>

Run: `results/exp07_step_code/code_v1` (manifest written before the run; the human approved the design and decision
rules; the code and Σ caches' sha256 in `summary.json`). Eligibility as exp04 (154 fresh, 82 bank items); the copy
reproduces exp04's full-copy rows item for item (1232/1232 fresh, 656/656 bank). 117 of the 1000 fit items were
answered wrongly and left out of the fit. Every comparison and verdict per item set is in `summary.md`; per-layer
rates in `summary.json`; diagnostics in `diagnostics.jsonl`. Figure: `uv run python scripts/exp07_figures.py <new
folder> code_v1`. Headlines are recomputed by `scripts/verify_headlines.py`.
</details>

### exp08_brew_read (part B): the lens reads brew's intermediate at a few positions; writing along its direction does nothing
**What we measure.** exp07's code writes the step and is nearly orthogonal to the lens direction. Is the lens blind to
the intermediate there, or does it read it without being able to write it? Part A's protocol: at each of the 21
positions after the start line and every second layer, is I the top-1 of the 12 palette colours in the reader's
readout (J++, the J-lens, the logit lens as baseline), against the distractor X, a rule-table colour equally present
in the prompt? exp07's code serves as a lens-free reader. Clean prompts, exp07's 236 items, no edits.

**In short.**
- **Averaged over the window's positions, the lenses barely read I.** At layers 36-50 J++ ranks I first in 15% of
  (layer, position) cells, the distractor in 8% (+7 [+5, +9] pts; chance 8%); the J-lens and the logit lens 12% (+5
  each); exp07's code 41% (+36 [+33, +40]). Bank items alike (J++ 13% vs 8%; the logit lens no better than the
  distractor). By the manifest's rule J++ and the J-lens read I, weakly.
- **At a few positions they read it well, from the window's first layer.** At layer 36 J++ ranks I first for 61% of
  fresh items at the newline after "assistant" (the J-lens 47%; bank 55% and 54%), and for about half at the "\n\n"
  after "</think>" (layers 40-44); X is first there for 2-6%, and the same search over the window's cells finds X at
  most 13-16%. The code reads I best at the same position (88%). Before layer 36 no position reads I above chance.
- **The readers work on these prompts.** At the last token at layer 62 all three put the answer first (J++ 95%, the
  J-lens 92%, the logit lens 86%; X 0-1%).

With exp07: the lens sees the intermediate where brew carries it, at a few scaffold tokens, but writing along its
direction (v_X - v_I) moves the step for 1% of window layers, while a fitted code nearly orthogonal to it moves it for
34%. The direction the lens reads I along is not one that takes the step when written.

![exp08: reading the intermediate](figures/exp08_brew_read/v1/brew_read.png)

**What this does not show.** Top-1 among 12 colours, not among the vocabulary: in the window the median vocabulary
rank of I is about 9,600 (J++), 25,000 (logit lens) and 182,000 (J-lens), so the lens ranks the colour above other
colours without saying it. The best cells were found after the fact (a search over 168 cells), checked against the
same search for X. exp04's `positions_window`, run after this, finds that the second lookup reads the intermediate
from these positions: copying C's activations at the 4 alone gives the whole copy's effect, at the other 17 nothing.

<details><summary>Full numbers and checks</summary>

Run: `results/exp08_brew_read/read_v1` (manifest written before the run; the human chose the run; part A's controls:
the distractor and the logit lens). Every read is in `reads.jsonl` (colour ranks per position for I, X, S, A; the
vocabulary rank of I at the window layers); per reader, layer and position in `summary.json`. Positions are the same 21
tokens in every item (exp07's check). Figure: `uv run python scripts/exp08_figures.py <new folder> read_v1` (loads the
tokenizer for the position labels). Headlines are recomputed by `scripts/verify_headlines.py`.
</details>

### Pitfalls found so far
1. **Trailing space.** Most original prompts end in a space (83/93), which Qwen's tokenizer leaves as a lone `" "`
   token. The model then answers far worse (27B: 21/93 correct vs 61/93 with the space stripped) and the lens reads a
   different token. Switch: `params.strip_trailing_space`.
2. **Numbers split into digits.** Qwen splits `" 26"` into `" "`, `"2"`, `"6"`, so scoring "26" by its first token
   gave fake hits (fixed in `d068538`; the two runs before the fix, `20261013-204427` and `-204551`, are superseded
   and not committed). Headlines use only single-token bridges.
3. **"The bridge is visible somewhere" is too weak.** Across all layers x tokens, a same-category distractor (Mexico
   for Brazil) also reaches the top somewhere. The read-site map must compare the bridge against a distractor.
4. **Best-of-all-layers favours the logit lens on deep models** (see the layer plot). exp11/exp12 average over the
   middle-layer band 32-48 instead.
5. **Token positions differ between prompts.** exp12 aligns them by distance from the last word, which mixes roles
   ("-1" is "ends" in one prompt, "is" in another); checked by splitting on the last word.
6. **Not yet checked:** in 5/93 lens-eval questions the bridge word appears in the prompt itself.

### Decisions
- **Trailing space: stripped is primary; prompts as published are kept as the paper-literal replication**
  (2026-10-13, Danyil; to confirm with Zach since part B's correct-answer filter depends on it). Why:
  - The protocol reads "the token right before `target`". In natural text that is `" is"`; the lone `" "` exists only
    because the prompts were written for another tokenizer, and after it the answer becomes a fragment (`"Port"`).
  - We study reasoning the model actually does: 27B answers 61/93 stripped vs 21/93 as published. 21 items is also
    too few for swap rates with useful CIs.
  - The lone `" "` invites digits, which produced fake hits (pitfall 2): 6 at layer 0 on 4B vs 0 when stripped.
  - Part B uses the same prompts (29/90 probe-swap prompts end in a space), so both parts must treat them the same.
  Against: numbers are not 1:1 with the paper (hence the replication variant). The J-lens reads the bridge more often
  on the lone `" "` (4B: 0.57 vs 0.43), but that is confounded with the digit artifact and with the model mostly
  failing there; the all-positions map will test it directly.

### Open decisions (humans)
- Whether to drop the 5 questions whose bridge appears in the prompt.
- Band for part A headlines: 32-48 (part B's) is used as primary; 28-52 is reported as exploratory.

## Next steps (part A)
In order; designs need human sign-off before GPU runs.
1. **Tell part B where the bridge is:** strongest on the last words before "is", from about layer 20. Part B already
   swaps at every prompt position, and its earlier bands (16-32, 24-40) did not pass its gate either, so this is
   information for reading its results, not a fix for the gate.
2. **Per question, not just per group:** for how many questions is the bridge on top at an earlier position and
   layer than the answer? Align positions by role (the words that cue the bridge) instead of distance from the end.
3. **The 5 lens-eval questions whose bridge appears in the prompt:** check whether they drive any exp10 headline.
4. **Oracle lens** on the same items: the Qwen3.6-27B adapter is on HF (`neuronpedia/jacobian-lens`,
   `qwen3.6-27b/oracle`); its reference read code may not be public, so check that first, then propose a design.
   This is the only long GPU job in sight.
5. **NLA:** source and weights still to identify.
6. Optional: reproduce J++'s published Recall@10 (55.2% on Qwen3.6-27B) over all six lens-eval sets.
7. Stretch: repeat on Gemma 4 31B (J-lens and J++ exist on HF).

## Next steps (part B)
1. **Verify v4:** `scripts/verify_headlines.py` now recomputes exp02 v4's, exp03's and exp04's headlines from the raw
   files (one DIFF: the fresh items' random-direction row says "answer changed 0%"; 1 of 164 changed, and 0% is
   its f(f(S')) rate); a human recomputes the headlines.
2. **The gate:** decide whether 30% on the full probe is still the right go/no-go now that the J-space part and the raw
   lens vectors carry the effect.
3. **Why "anything else" bridges rarely flip:** probe quality vs how those bridges are represented.
4. **A control matched in total edit size** across layers.
5. **Brew:** exp04 maps the lookup (the intermediate is carried after the start line at layers 36-50) and finds the
   step outside the J-space, on the bank items and again on 154 fresh ones; exp07 finds a code for the intermediate,
   fit on other items, that writes the step as well as the copy, outside the J-space and orthogonal to the lens
   direction; exp08 finds the lens reads the intermediate there only at a few scaffold tokens (J++ 61% at the newline
   after "assistant", layer 36), along a direction that does not write the step; and copying only the 4 positions
   where the lens reads I carries the whole step (33%; the other 17: 0%). Next: split the code at those positions into
   the lens-read part and the rest; what the I answers at layers 36-46 are; and steering at the cue phrase in exp02
   at the same sizes.
6. **Σ-aware writes** (exp06, exp07): writing along Σv lost to writing along v at the start line, and did no better
   than v at exp04's window. Dropped unless a human wants a Mahalanobis-matched version.
