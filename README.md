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

## Contents
| Section | The question it answers |
|---|---|
| [Setup](#setup-shared-by-all-experiments) | On which model, prompts and questions everything is measured, and how to read the figures |
| [Method, part A](#method-part-a-can-any-reader-see-the-bridge-exp10) | Which experiments ask "can any reader see the bridge?" |
| [Method, part B](#method-part-b-is-the-bridge-used-outside-the-j-space-exp01-09) | Which experiments ask "does the bridge act through the J-space?" |
| [Status](#status) | What we know so far, and where the final figures are |
| [exp10](#exp10_lens_sanity-does-the-lens-work-on-qwen-at-all) | Does a lens read two-hop bridges on Qwen at all? |
| [exp11](#exp11_bridge_vs_answer_by_layer-where-is-the-bridge-readable-and-where-the-answer) | At the last prompt token, at which layers are the bridge and the answer readable? |
| [exp12](#exp12_position_map-where-in-the-prompt-and-how-deep) | Where in the prompt, and from which layer, are they readable? |
| [exp14](#exp14_cue_answer_swaps-on-the-cue-phrase-is-it-the-bridge-or-already-the-answer) | On the cue phrase, does swapping the answer change it as often as swapping the bridge? |
| [exp15](#exp15_oracle_lens-where-the-lenses-miss-the-bridge-does-the-oracle-lens-name-it) | Where the J-lens and J++ miss the bridge, does a reader that puts the activation into words name it? |
| [exp16](#exp16_nla-does-a-second-verbalizer-the-nla-see-the-same) | Does a second verbalizer, the NLA, trained for another objective, see the same? |
| [exp02](#exp02_swaps-part-b-does-the-bridge-act-through-the-j-space-and-where) | Does swapping the bridge's J-space part change the answer, and where in the prompt? |
| [exp03](#exp03_brew_swaps-part-b-an-in-context-two-step-lookup) | Do the same swaps work on a two-step lookup whose answer is read off the prompt? |
| [exp04](#exp04_brew_patch-part-b-where-brew-carries-its-intermediate-without-a-lens) | Where does that lookup carry its intermediate, found without a lens? |
| [exp06](#exp06_sigma_writes-part-b-read-with-the-lens-write-along-the-covariance) | Do edits shaped by the activation covariance (Σv) act more than the lens's own directions? |
| [exp07](#exp07_step_code-part-b-a-code-for-brews-intermediate-fit-on-other-items-writes-the-step-the-lenss-direction-does-not) | Does a code for brew's intermediate, fit on other items, write the step where the lens direction does not? |
| [exp08](#exp08_brew_read-part-b-the-lens-reads-brews-intermediate-at-a-few-positions-writing-along-its-direction-does-nothing) | Do the lenses read brew's intermediate where the step is carried? |
| [exp09](#exp09_bind_recall-part-b-is-a-bridge-bound-in-context-outside-the-j-space-like-brews-no) | Holding the question fixed, is a bridge bound in context outside the J-space, as brew's intermediate is? |
| [Pitfalls](#pitfalls-found-so-far) | What went wrong along the way, and how each is handled |
| [Decisions](#decisions), [open decisions](#open-decisions-humans) | What was decided, and what is still for the humans to decide |
| [Next steps, part A](#next-steps-part-a), [part B](#next-steps-part-b) | What comes next |
| [DEVELOPER.md](DEVELOPER.md) | How to run, re-analyse and publish: layout, commands, GPU box, figures, examples |

## Setup (shared by all experiments)
- **Model.** Qwen3.6-27B (pinned revision, bf16). Qwen3.5-4B only in exp10's check that the lenses work.
- **Prompts.** The published prompts end in a space, which Qwen's tokenizer keeps as a lone `" "` token: after it
  the model answers far fewer questions (lens-eval: 21 of 93 vs 61 with the space removed) and a reader at the last
  token reads that space instead of the last word. Every experiment, part A and part B (from its v4), removes the
  trailing space. Runs on the prompts as published are kept only as a check and say so.
- **Which questions count.** The probe-swap set has 90 two-hop questions (bridge Brazil, answer Portuguese). A
  question counts as answered correctly when the model's greedy continuation contains the answer (exp13's
  criterion, used by part B from v4): 77 of the 90. exp10 instead uses the lens-eval multihop set: the 84 questions
  whose bridge is a single token, answered correctly or not.
- **Readers.** At a given layer and prompt position each reader scores every token of the vocabulary: the logit lens
  (the model's own unembedding; the baseline), the J-lens and J++ (two fits of the average-Jacobian lens).
- **"Ranked first among its candidates" (exp11, exp12).** For the bridge (Brazil) we ask whether the reader scores it
  above every other entity of the set: the **97 entities** are all distinct bridges and swap targets of the 90
  questions (70 bridges and 68 swap targets, overlapping), each a single Qwen token. For the answer (Portuguese) the
  candidates are the **112 answers**: all distinct answers and swap answers of the 90 questions that are a single
  token (120 in all; the 8 multi-token ones cannot be ranked, so 5 of the 77 questions drop out of the answer lines).
  Restricting the ranking to these pools asks "of the entities these questions are about, which one does the reader
  pick?", the same choice part B's swaps change; chance is 1 in 97 (about 1%). The full-vocabulary rank is used only
  for the comparison with the distractor.
- **Single-token words only.** Every headline number is on bridges that are one Qwen token: the probe-swap set's 97
  entities are each a single token (exp11-16), and exp10 keeps the 84 of 93 lens-eval questions whose bridge is one
  token. Answers are ranked only where they are a single token (72 of the 77 questions; the verbalizers' answer lines
  61, numbers left out). How the lenses and the verbalizers do on bridges spread over several tokens ("New Zealand",
  most numbers above 9) is not measured.
- **Control.** Each question has a same-category distractor (Mexico for Brazil, Spanish for Portuguese; part B's swap
  target). If the distractor came first as often as the bridge, the reader would be reading the category, not the
  entity.
- **Layers.** Summaries average over layers 32-48, fixed before exp11; layers 24-40, the band part B's main swaps use,
  are reported alongside. Both are part B's swap bands.
- **Positions (exp12)** are counted back from the last word of the prompt: 0 = the last word (usually "is"), -1 the
  word before ("located", "ends"), and so on; each position's label is its most common token.
- **Shading.** 95% intervals: a bootstrap over questions (10,000 resamples) for averages over layers or positions,
  Wilson for the share of questions at one layer.

## Method, part A: can any reader see the bridge? (exp10+)
1. `exp10_lens_sanity`: the lens works on this model. Sanity gate (known fact, HF parity, our readout == jlens's
   `apply`), then `lens-eval-multihop` pass@k for the J-lens and J++ against the logit lens, plus a bridge vs
   same-category distractor control. Debugged on Qwen3.5-0.8B (CPU), run on Qwen3.5-4B (same `qwen3_5` hybrid
   architecture as the target), then Qwen3.6-27B.
2. `exp11_bridge_vs_answer_by_layer`: on part B's questions and labels, at the last prompt token, at which layers each
   reader ranks the bridge (and, separately, the answer) first among its candidates.
3. `exp12_position_map`: the same readout at every prompt position x layer: where in the prompt, and how deep, each
   word is readable; the best position per reader, chosen on half the questions and checked on the other half.
4. `exp13_greedy_answers`: which questions the model answers correctly, judged on its greedy continuation (the
   criterion part B adopted in v4).
5. `exp14_cue_answer_swaps`: on the cue phrase, does swapping the answer's lens direction change the answer as often
   as swapping the bridge's?
6. `exp15_oracle_lens`: where the J-lens and J++ miss the bridge (or the answer), does the oracle lens (a LoRA on the
   model that puts one activation into words) name it; and after the bridge swap, does it name the swap target?
7. `exp16_nla`: the same with the NLA, a second 27B verbalizer (another training objective, built on the same model)
   trained on layer 42, compared with every reader at layer 42.

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
6. `exp04_brew_patch`: lens-free activation patching of brew from a counterfactual table, by layer and prompt
   position (where the intermediate is carried), then the copy split into its J-space part and the rest, and the copy
   restricted to subsets of positions; bank and held-out fresh items.
7. `exp06_sigma_writes`: exp02's matched control with a covariance-shaped rest, and steering along Σ_λ v.
8. `exp07_step_code`, `exp08_brew_read`: a code for brew's intermediate fit on other items and written at exp04's
   window; and whether the lenses read the intermediate there (part A's top-1 protocol with a distractor).
9. `exp09_bind_recall`: the same question with its bridge recalled or bound in the prompt, through exp04's patching
   and exp02's probe swaps.

## Status
Draft, UNVERIFIED: nothing is in `VERIFIED.md` yet. The STATE block in `AGENTS.md` tracks what is in flight.
Final figures, numbers and examples per experiment: [results/README.md](results/README.md). Every part A number below
is recomputed from the raw run files by `uv run python scripts/verify_headlines.py`.

**Where things stand (2026-10-15).** On Qwen3.6-27B, for bridges that are a single token, the J-lens and J++ do read
the bridge, once read at the right place: one word before the end from about layer 23, 19 layers before the answer appears at the last word (exp12). It
acts on the answer from the cue phrase, the words that point to it, and does so apart from the answer's own direction
(exp14). Readers that put an activation into words, the oracle lens and the NLA, see the bridge and the answer a
little more often than the lenses at the same place and layer, including about a third to a half of the readings
where neither lens has the bridge first, and they follow the model's state when a swap changes its answer (exp15,
exp16). Whether, on those lens-blind readings, they read the state or solve the question themselves is the open
question; the next experiment (exp17, Next steps) is designed to settle it and has not been run. Part B (exp01-04)
asks the original question with probe swaps; on brew, an in-context lookup, it finds the intermediate carried at four
positions after the start line at layers 36-50 outside the J-space: the lenses read it there at a few positions,
but writing along their direction does not take the step, while a code fit on other items does (exp04, exp07, exp08).
A bridge bound in the prompt and used by a recalled fact stays inside the J-space (exp09), so it is not being in the
context that moves brew's intermediate out.

**Final figures (Qwen3.6-27B).**
| Figure | What it shows |
|---|---|
| [exp12 `two_step.png`](figures/exp12_position_map/two_step.png) | **Headline.** Where in the prompt each word is read (left) and from which layer (right): the bridge one word before the end from layer 23, the answer at the last word from layer 44 |
| [exp12 `layers_at_positions_jlens.png`](figures/exp12_position_map/layers_at_positions_jlens.png) | The same, one line per position for the last four words: which positions carry the bridge, and the answer, at which layers |
| [exp12 `cue_phrase.png`](figures/exp12_position_map/cue_phrase.png) | On the cue phrase (the words that point to the bridge): the bridge is read there as often as at the read sites, and earlier; the answer only weakly |
| [exp12 `cue_phrase_lenses.png`](figures/exp12_position_map/cue_phrase_lenses.png) | J-lens vs J++ on the cue phrase: they read the same bridge; their swaps differ |
| [exp12 `by_offset.png`](figures/exp12_position_map/by_offset.png) | The "where in the prompt" panel for all three readers, logit lens included |
| [exp12 `position_layer.png`](figures/exp12_position_map/position_layer.png) | Reference heatmaps: every position x layer, all three readers |
| [exp14 `flip_rates_by_overlap.png`](figures/exp14_cue_answer_swaps/flip_rates_by_overlap.png) | On the cue phrase, swapping the answer changes it only where the swap also moves the bridge |
| [exp14 `flip_rates.png`](figures/exp14_cue_answer_swaps/flip_rates.png) | Bridge vs answer swaps on the cue phrase and at the last token, with random-direction controls |
| [exp14 `flip_rates_pinned.png`](figures/exp14_cue_answer_swaps/flip_rates_pinned.png) | The same swaps with the other pair held: on the cue phrase the bridge swap still works, the answer swap does not |
| [exp15 `readers_by_layer.png`](figures/exp15_oracle_lens/readers_by_layer.png) | J-lens, J++ and the oracle lens side by side on the same activations, layers 20-60: the oracle has the bridge a little more often, the answer much more often early on (with more false alarms) |
| [exp15 `oracle_vs_lenses.png`](figures/exp15_oracle_lens/oracle_vs_lenses.png) | The less the lenses see the word, the less often the oracle names it: about 85% where both rank it 1st, 20% where they have it 11th or lower; false alarms 4-8% |
| [exp15 `after_swap.png`](figures/exp15_oracle_lens/after_swap.png) | After the bridge swap, the oracle names the swap target where the model's answer changes (67%), rarely where it does not (10%) |
| [exp15 `by_layer.png`](figures/exp15_oracle_lens/by_layer.png) | By layer (20-60): the oracle names the lens-blind bridge at every layer; the swap's effect reaches the last words between layers 32 and 40 |
| [exp16 `methods_at_42.png`](figures/exp16_nla/methods_at_42.png) | Every reader at layer 42: the NLA and the oracle lens have the bridge and the answer more often than the J-lens and J++, at the same 3-9% false alarms |
| [exp16 `after_swap.png`](figures/exp16_nla/after_swap.png) | The NLA too names the swap target where the model's answer changes (59%), rarely where it does not (11%) |
| [exp16 `by_swap_label.png`](figures/exp16_nla/by_swap_label.png) | By part B's swap labels: where the J-space swap does not change the answer the lenses see the bridge less, the verbalizers as often |
| [exp11 `pool_top1_by_layer.png`](figures/exp11_bridge_vs_answer_by_layer/pool_top1_by_layer.png) | Last token only: bridge and answer ranked first, by layer, three readers |
| [exp11 `advantage_by_layer.png`](figures/exp11_bridge_vs_answer_by_layer/advantage_by_layer.png) | Last token only: how many times higher than its distractor each word ranks |
| [exp10 `pass_at_10_by_model.png`](figures/exp10_lens_sanity/20261015-135537/pass_at_10_by_model.png) | Does each lens find the bridge at all (pass@10), 4B and 27B |
| [exp10 `pass_at_10_by_bridge_kind.png`](figures/exp10_lens_sanity/20261015-135537/pass_at_10_by_bridge_kind.png) | pass@10 by kind of bridge (27B), best layer anywhere and within 32-48: the logit lens's numbers come from the last layers |
| [exp10 `27b_by_layer.png`](figures/exp10_lens_sanity/20261015-135537/27b_by_layer.png) | Why the J-lens looks no better than the logit lens on pass@10 |

Worked examples with lens tables: `make examples-serve` opens [examples/index.html](examples/index.html) (exp10-12,
exp15, exp16); the exp12 page is also published at https://claude.ai/artifact/TXLZH6WxuxSQDhoK5YHTj9 (anyone with the
link can open it). Each page groups sampled questions by what the readers do with them; exp10's also by what the bridge
is: a number ('6', 'four'), a letter (a chemical symbol), or named in the prompt (`scripts/exp10_lens_sanity/examples.py`;
a bridge counts as found if any of its listed forms is). The exp10 page shows these groups from its next examples run.
The exp15 and exp16 pages show every question with the J-lens and J++ ranks next to the oracle lens's (exp15) or the
NLA's (exp16) words at each position and layer, before and after the bridge swap; the exp10-12 cards show both under
each question.

**What we know so far (Qwen3.6-27B, the 77 two-hop questions it answers correctly).**
1. The J-lens and J++ can read the bridge in the middle layers; the plain logit lens mostly only near the output
   (exp10, exp11). Over all layers the logit lens catches up, mostly on number bridges ('6', 'four') at layers 54-60;
   within layers 32-48 the lenses lead for every kind of bridge (exp10). The one lens-eval question that names its
   bridge in the prompt changes none of this (the earlier count of 5 such questions was a substring artifact).
2. The bridge is readable earlier than the answer, both in the prompt and in depth: one word before the end from about
   layer 23, while the answer appears only at the last word from about layer 44, 19 layers later [15, 27] (exp12).
3. Where the bridge is readable, part B's swaps tend to work: questions whose J-space swap flips the answer have the
   bridge ranked first more often (J-lens 73% vs 50%, J++ 70% vs 41% of layers 32-48), but the groups are small and
   the intervals overlap.
4. The original "J-lens cannot see the bridge" is mostly where and how we looked: of the 30 questions where it does not
   have the bridge first at the last word, 73% have it first at an earlier word (distractor, same search: 33%).
5. Where the bridge is readable is not where it is used. It reads about as well on the cue phrase (the words that
   point to it, "Amazon River ends") as one word before the end, and earlier on the cue phrase; but swapping it changes
   the answer on the cue phrase (part B: 31% with J++) and hardly at -1 (9%) (exp12, exp02).
6. The J-lens and J++ read the same bridge in the same questions (r = 0.92), yet swaps along J++'s directions change
   the answer more often (31% vs 19% on the cue phrase): J++'s advantage is in its directions, not in what it sees.
7. On the cue phrase, swapping the answer's direction changes the answer only where it also moves the bridge (0-1
   of about 35 questions otherwise), and less often than the bridge swap: no sign that the answer itself sits there.
   With the answer's coordinates held, the bridge swap on the cue phrase still changes the answer (18% of questions;
   24-28% where the two swaps overlap most), at the same edit size; held the other way round, the answer swap
   hardly does (1-6%). The cue phrase carries the bridge apart from the answer's direction. Whether it carries the
   answer too stays open: the held answer swap is weak even at the last token (17-26%), so its low rate on the cue
   phrase is not evidence of absence (exp14).
8. A reader that puts the activation into words, the oracle lens, sees a little more than the lenses at a given
   position and layer (exp15). Where neither the J-lens nor J++ ranks the bridge 1st it names it in 37% of readings
   (false alarms 4%), mostly where the lenses nearly have it (54% at 2nd-3rd, 22% at 11th or lower). Read at all 11
   layers both find the bridge somewhere in every question (the distractor in a third), so there it adds no question;
   at one layer it adds a few. After the bridge swap it names the swap target where the model's answer changes (67% vs
   10% where it does not), so it follows the state; but it mostly writes the question out with the bridge filled in,
   so on the lens-blind readings it may be solving the question rather than reading the state, which only a cleaner
   test can tell.
9. A second verbalizer with another training objective, the NLA (exp16, layer 42), agrees: it names the bridge in
   46% of the readings where neither lens has it first (false alarms 10%), and the swap target where the swap changes
   the answer (59% vs 11%). At layer 42 both verbalizers have the bridge and the answer more often than either lens (bridge: NLA 75%,
   oracle 65-70%, lenses 62-65%; answer: 57%, 54-55%, 34-38%). Both are built on Qwen3.6-27B, so agreeing does not
   rule out that both solve the question; the NLA's own comments often do.
10. Three checks on the verbalizers. Our code gives the same texts as WorkspaceBench's reference code path, so the
    oracle's fragmentary format is its own. On the cue phrase they name the answer no more often than a lens ranks it
    first there (NLA 23% vs 30%, oracle 30% vs 27%): no sign of extra solving where the answer is not yet formed. Of
    the NLA's lens-blind namings, 63% are inside its quotation of the prompt with the bridge filled in (a hint of the
    state), 37% in its own comments (likely solving).
11. The verbalizers' edge over the lenses sits in the questions where part B's J-space swap does not change the
    answer (neither: +5 to +12 points; J-mediated: -1 to -9; difference -14 [-28, -1] and -14 [-26, -1]): there the
    lenses see the bridge less, the verbalizers as often. That is the pattern of a reader of a non-J-space part, and
    also of a reader that solves the question regardless; exp17 separates them (exp16).

![exp12: where and how deep](figures/exp12_position_map/two_step.png)

*The headline figure (exp12): left, where in the prompt the bridge (blue) and the answer (orange) are ranked first;
right, from which layer, the bridge at -1 and the answer at the last word, 19 layers apart. How to read it in detail:
under exp12 below.*

### exp10_lens_sanity: does the lens work on Qwen at all?
**What we measure.** We give the model a two-hop question, e.g. "The language spoken in the country where the Amazon
River ends is" (answer Portuguese, bridge Brazil). At the last prompt token we ask each *reader* for its ranked word
list at every layer, and count how often the bridge is in the top 10 at some layer (pass@10). Three readers: the
**logit lens** (simplest; the baseline), the **J-lens**, and **J++** (an improved J-lens).

**In short.**
- **Qwen3.5-4B:** the J-lens finds the bridge more often than the baseline (44% vs 25% of questions).
- **Qwen3.6-27B:** J++ clearly beats the baseline (77% vs 54%). The J-lens is only slightly ahead (58%), within the
  error bars.
- **Number bridges and the last layers are what hide the J-lens's lead.** On the 63 questions whose bridge is a word
  (Brazil, iron), the J-lens finds it in 67% against the logit lens's 52% (+14 points [+2, +27]) and J++ in 89%. On
  the 17 whose bridge is a number ('6', 'four', 'third'), the logit lens does better (65%) than the J-lens (41%) and
  J++ (53%), but only through the last layers: within layers 32-48 it finds 6% of the number bridges, the J-lens 18%
  and J++ 41%, and 3% / 30% / 59% of the word bridges. The 4 single-letter bridges (chemical symbols) no lens
  finds.
- **The bridge is often invisible at the last token.** On the 61 questions where 27B's top next token is the answer,
  J++ misses the bridge in 1 of 3 and the J-lens in 1 of 2. This is Zach's observation. The next experiments check
  other ways of reading it.

![pass@10 by model and reader](figures/exp10_lens_sanity/20261015-135537/pass_at_10_by_model.png)

*How to read it: each bar is the share of the 84 questions whose bridge is in that reader's top 10 at its best layer,
read at the last prompt token; a bridge listed in several forms ('5', 'five') counts as found if any form is. Error
bars are 95% bootstrap intervals; grey is the baseline. On 27B, J++ (orange) is clearly above the logit lens; the
J-lens (blue) is within its error bars.*

**Why the J-lens looks no better than the baseline on 27B.** In the middle layers only the J-lens and J++ see the
bridge; near the output the logit lens catches up. pass@10 takes the *best* layer, so the late layers hide the
difference.

![27B by layer](figures/exp10_lens_sanity/20261015-135537/27b_by_layer.png)

*How to read it: x is the layer, y the share of the 84 questions with the bridge in the reader's top 10 at that
layer. Inside layers 32-48 (grey) J++ has it for up to 35% of the questions, the J-lens up to 18%, the logit lens at
most 2%; only from about layer 55 does the logit lens join them.*

![pass@10 by kind of bridge](figures/exp10_lens_sanity/20261015-135537/pass_at_10_by_bridge_kind.png)

*How to read it: the bars of the first figure, split by what the bridge is (27B). Left, the best layer anywhere (as
pass@10): for word bridges both lenses are above the logit lens and J++ finds almost all; for number bridges the
logit lens is on top; letter bridges (n = 4) no lens finds. Right, the best layer only within layers 32-48: the logit
lens finds almost nothing of any kind, and both lenses lead for words and numbers alike. So the logit lens's numbers
come from the last layers (it finds them at layers 54-60), where the model is close to its output.*

<details><summary>Full numbers</summary>

pass@10 on the 84 questions with a single-token bridge, 95% percentile bootstrap CI over questions (n_boot=10000,
seed 0); a bridge listed in several forms counts as found if any form is in the top 10. Runs under
`results/exp10_lens_sanity/`, re-aggregated in each run's `analysis-20261015-1351*/`. All sanity checks pass on both
models (HF parity and our readout vs `jlens.apply`: max abs diff 0.0).

| Model | Top next token = answer | Logit lens | J-lens | J++ | J-lens - logit | J++ - logit | Run |
|---|---|---|---|---|---|---|---|
| Qwen3.5-4B | 50/93 | 0.25 [0.15, 0.35] | 0.44 [0.33, 0.55] | - | +0.19 [+0.10, +0.29] | - | `20261013-205057` |
| Qwen3.6-27B | 61/93 | 0.54 [0.43, 0.64] | 0.58 [0.48, 0.69] | 0.77 [0.68, 0.86] | +0.05 [-0.06, +0.17] | +0.24 [+0.13, +0.36] | `20261013-205936` |

- On the 61 questions where 27B's top next token is the answer: J++ 0.69 [0.57, 0.80], J-lens 0.51 [0.38, 0.64].
- By kind of bridge, 27B: words (n = 63) logit lens 0.52 [0.40, 0.65], J-lens 0.67 [0.56, 0.78], J++ 0.89 [0.81,
  0.95]; numbers (n = 17) 0.65 [0.41, 0.88], 0.41 [0.18, 0.65], 0.53 [0.29, 0.76]; letters (n = 4) 0.25, 0, 0. 4B,
  words: logit lens 0.32, J-lens 0.54; numbers 0.06, 0.18.
- One question names its bridge in the prompt ("the time of day ..." -> "day"); without it the headlines move by
  under a point (27B: J++ 0.77, J-lens 0.59, logit lens 0.54).
- With the paper's rule (each listed form scores its share of the question), 27B: J++ 0.75, J-lens 0.57, logit lens
  0.51 (`pass_at_k_fraction` in the same summaries).
- Check on the prompts as published (lone trailing space): the model answers 18/93 (4B) and 21/93 (27B); 27B logit
  lens 0.60, J-lens 0.62, J++ 0.87; 4B logit lens 0.40, J-lens 0.62 (runs `20261013-205029`, `-205736`).
- Controls (27B, rank at the last token): Brazil 0 vs distractor Mexico 57 (J-lens) / 45 (J++); Hungary 1 / 0 vs
  Poland 16 / 18. Figures: `uv run python -m scripts.exp10_lens_sanity.plot --summary`.
</details>

### exp11_bridge_vs_answer_by_layer: where is the bridge readable, and where the answer?
**What we measure.** Part B's 90 two-hop questions; the headline uses the 77 the model answers correctly (see
Setup). At the last prompt token, at every layer, we ask each reader: is the bridge (Brazil) ranked
first among the 97 entities of the set, and is the answer (Portuguese) ranked first among the 112 answers? The
same-category distractors (Mexico, Spanish) are the controls. Chance is about 1%.

**In short.**
- **J-lens and J++ read the bridge in the middle layers; the logit lens only near the output.** Averaged over
  layers 32-48 the bridge is ranked first in 57% of questions (J-lens), 56% (J++), 25% (logit lens); its distractor
  in 5%. This reproduces part B's `gate_debug` (0.55-0.70).
- **At the last token the bridge comes first, the answer later, but they overlap.** Half the questions have the
  bridge first by layer 35; the answer gets there by layer 44 (J-lens, 8 layers later [3, 16]) or 43 (J++, 8 [3, 20]).
  There is no clean hand-off: the bridge stays first until about layer 60, and per question the bridge settles first
  before the answer in only 52% [39, 64] of cases (J-lens).
- **Where the bridge is readable, it is also used.** On the questions where part B's J-space swap flips the answer,
  the bridge is first in 73% [58, 86] of layers 32-48 (J-lens, n=25) and 70% [59, 81] (J++, n=39); on those where no
  swap works, 50% [38, 62] (n=49) and 41% [29, 54] (n=37). Suggestive: the intervals overlap (J-lens) or nearly touch
  (J++). Each lens is split by its own swaps.

![exp11: ranked first by layer](figures/exp11_bridge_vs_answer_by_layer/pool_top1_by_layer.png)

*How to read it: one panel per reader; x is the layer, y the share of the 77 questions in which the reader ranks the
word first among its candidates, at the last prompt token (shaded: 95% Wilson interval). Blue = bridge among the 97
entities, orange = answer among the 112 answers, grey = their distractors, dotted = chance. In the J-lens and J++
panels the blue line leaves the grey control from about layer 20 and stays above the orange one until layers 55-60:
the bridge is readable here, and ahead of the answer. The logit lens picks either word mostly after layer 50.*

**What this does not show.** A lens shows what can be read out at a layer, not when it was computed. And this is
one token: the first hop may happen earlier in the prompt (at "Amazon River ends"), which exp11 does not look at.
About 40% of questions do not have the bridge first at the last token; exp12 looks at the earlier tokens.

<details><summary>Full numbers</summary>

Run `20261015-100110` (Qwen3.6-27B, labels `exp02_swaps/main_v4_jlens`); its `summary.json` is
current; figures re-rendered in `analysis-20261015-125327/`. Eligible n=77 (answer columns: the 72 with a
single-token answer), layers 32-48, 95% percentile bootstrap CI over questions (n_boot=10000, seed 0).

| Reader | Bridge first | Answer first | Bridge's distractor first | Bridge above its distractor (full vocabulary) | Half the questions: bridge / answer (lag) |
|---|---|---|---|---|---|
| logit lens | 0.25 [0.18, 0.33] | 0.14 [0.09, 0.20] | 0.04 | 0.80 [0.73, 0.87] | L50 / L51 (1 [-2, 4]) |
| J-lens | 0.57 [0.48, 0.66] | 0.41 [0.32, 0.50] | 0.05 | 0.83 [0.76, 0.90] | L35 / L44 (8 [3, 16]) |
| J++ | 0.56 [0.46, 0.64] | 0.38 [0.29, 0.47] | 0.05 | 0.84 [0.78, 0.90] | L36 / L43 (8 [3, 20]) |

![exp11: advantage over the distractor](figures/exp11_bridge_vs_answer_by_layer/advantage_by_layer.png)

*How to read it: y is how many times higher than its same-category distractor the reader ranks the word in the full
vocabulary (log scale; 1x = no better). Line: the median question; shaded: the middle half. Within layers 32-48 the
median question has the bridge 4-24 times above its distractor with the J-lens and J++, 2-11 times with the logit
lens; the gaps pass 100x only near the output (from about layer 55).*

Bridge first, split by which questions part B's J-space swap flips (labels `exp02_swaps/main_v4_jlens` in run
`20261015-100110`, `main_v4_jpp` in run `20261015-100426`; the two runs' ranks are identical row for row, only the
split differs):

| Reader | Swaps by | Eligible | J-mediated (swap flips) | Neither (no swap flips) |
|---|---|---|---|---|
| J-lens | J-lens | 0.57 [0.48, 0.66] (n=77) | 0.73 [0.58, 0.86] (n=25) | 0.50 [0.38, 0.62] (n=49) |
| J++ | J++ | 0.56 [0.46, 0.64] (n=77) | 0.70 [0.59, 0.81] (n=39) | 0.41 [0.29, 0.54] (n=37) |
| J-lens | J++ | 0.57 [0.48, 0.66] | 0.73 [0.62, 0.83] | 0.41 [0.28, 0.55] |
| logit lens | J-lens | 0.25 [0.18, 0.33] | 0.28 [0.15, 0.42] | 0.25 [0.16, 0.35] |

- In layers 24-40, the band part B's main swaps use, the bridge is first in 44% [35, 53] of the questions (J-lens),
  45% [36, 53] (J++), 15% [10, 21] (logit lens); the answer in 28% (both lenses), 9% (logit lens); distractor 6-7%.
- The 22 questions whose published prompt ended in a space read worse even with the space removed (J-lens
  bridge 0.40 [0.23, 0.59] vs 0.64 [0.53, 0.74]; answer 0.29 vs 0.47).
- Earlier run, prompts as published with part B's earlier labels (`20261014-092835`, 67 eligible): the same picture
  (J-lens bridge 0.59, lag 8 [4, 18]); J-mediated 79% [66, 89] vs neither 49% [35, 62].
</details>

### exp12_position_map: where in the prompt, and how deep?
**What we measure.** The exp11 readout (is the word ranked first among its candidates?) at every token of the prompt,
not just the last. Prompts differ in length, so tokens are aligned by their distance from the last word: 0 is the
last word (usually "is"), -1 the word before it (e.g. "located", "ends"), and so on. The best position for each
reader is picked on a random half of the questions and checked on the other half, because the best of 15 positions
looks better than it is on the data that picked it; the same search for the distractor (Mexico) shows how high noise
alone gets.

**In short.**
- **The bridge is read best one word before the end; the answer only at the end.** J-lens: the bridge is first in 65%
  [54, 74] of layers 32-48 at position -1 (57% at the last word); the answer in 41% at the last word and at most 25%
  anywhere earlier. Both halves of the data pick -1 for the bridge (held out: 67%, 62%). Noise ceiling: 11%.
- **The bridge comes about 20 layers before the answer.** Read where each is strongest, half the questions have the
  bridge first by layer 23 and the answer by layer 44: 19 layers later [15, 27] (J++: 22 vs 43, 22 [17, 30]).
  Read at a single token (exp11) the two overlapped; this is the step that one token hides.
- **Most last-token misses are a read-site effect.** Of the 30 questions where the J-lens does not have the bridge
  first at the last word, 73% [57, 90] have it first at an earlier word (distractor, same search: 33% [17, 50]).
- **On the cue phrase the bridge is read as often as at the read sites, and earlier; the answer only weakly.** On the
  words that point to the bridge ("Amazon River ends"), where swapping the bridge changes the answer, an average cue
  token has the bridge first in 56% [48, 64] of layers 32-48 (J-lens), like one word before the end (65%) and the
  last word (57%); its distractor 7%. It rises there earlier: a quarter of the questions by layer 8, against layer 18
  at -1 (J++: 3 vs 8), though both reach half near layer 23. The answer is first at an average cue token in 17%
  [11, 23] (swap answer 2%), against 41% at the last word.
- **The J-lens and J++ read the same bridge; they differ in what their swaps do.** Per question their readings on the
  cue phrase correlate at r = 0.92. On the 9 questions whose cue-phrase swap flips the answer with J++ only, both
  read the bridge equally (67% and 67%). Where the swap flips, the bridge reads better (both lenses flip: 79%;
  neither: 48%).

![exp12: where and how deep](figures/exp12_position_map/two_step.png)

*How to read it. Left: x is the position in the prompt, counted back from the last word; y is in what share of layers
32-48 the reader ranks the word first, averaged over the questions. The blue bridge line rises toward the end of the
prompt and peaks one word before it (-1): the bridge is there before the last word. The orange answer line stays at
the level of the grey control until the last two words. Right: x is the layer, y the share of questions with the word
ranked first, the bridge read at -1 and the answer at the last word; the dots mark the layer at which each reaches
half of the questions, the arrow the 19-layer lag. Thick: J-lens with 95% intervals; thin: J++.*

![exp12: layers at each of the last positions](figures/exp12_position_map/layers_at_positions_jlens.png)

*How to read it: one line per prompt position (J-lens), y the share of questions with the word ranked first at each
layer. Bridge (left): one word before the end (thick) reaches half of the questions at layer 23, the two words before
it at layers 24-25, the last word only at layer 35; earlier words (grey, averaged) stay at or below 30%. Answer
(right): the last word (thick) reaches half of the questions at layer 44, the word before it at layer 55; the two
words before that stay at or below 25%, earlier words at or below 10%.*

![exp12: the cue phrase](figures/exp12_position_map/cue_phrase.png)

*How to read it. Left: for each place in the prompt, in what share of layers 32-48 the J-lens ranks the word first,
averaged over the questions; each place counts as one position (an average token of the cue phrase or of the other
earlier words), so the bars compare like with like. Black ticks: the same share in layers 0-4, what the words' own
associations give ("Munich" already points to Germany at layer 0). Right: by layer, the bridge on the cue phrase
(solid blue) rises from about layer 5, before it does at -1 (dashed blue), and levels off near 60% while at -1 it
keeps rising; the answer on the cue phrase (solid orange) stays near 15-20%, while at the last word (dashed orange) it
climbs from layer 20 to over 80%.*

![exp12: J-lens vs J++ on the cue phrase](figures/exp12_position_map/cue_phrase_lenses.png)

*How to read it. Left: two different measures, each for both lenses. "Reads the bridge": in what share of layers
32-48 the lens ranks the bridge first on the cue phrase (56% J-lens, 58% J++: the same). "Swapping it changes the
answer": in what share of questions exchanging the bridge's J-space part for the distractor's on the cue phrase,
built from that lens's directions, makes the model give the distractor's answer (19% J-lens, 31% J++). Right: each
dot is one question, the J-lens's reading against J++'s; the dots follow the diagonal (r = 0.92), so the two lenses
see the bridge in the same questions. J++'s stronger swaps therefore come from its directions, not from seeing the
bridge where the J-lens does not (on the 9 questions only J++'s swap flips, both read it at 67%).*

**What this does not show.** Positions are aligned by distance from the end, not by meaning: in the 46 prompts that
end in "is" the bridge peaks on the word before it (76% [64, 87]); in the 31 others it has no clear peak (46-59% over
positions -3..0). The ordering holds for the group of questions, not reliably for each one. A lens shows what is
readable, not what is computed. On the cue phrase, the best token per question (a search over about 5) reaches 80% for
the bridge but also 19% for its distractor, which is why the figures use an average token. The cue words' own
associations can be carried into the middle layers, so layers 0-4 bound them from below only. Whether the answer read
there is used is exp14's question (it finds no sign of it apart from the bridge).

<details><summary>Full numbers and checks</summary>

Run `20261015-100735` (Qwen3.6-27B, labels `exp02_swaps/main_v4_jlens`); its `summary.json` is
current; figures re-rendered in `analysis-20261015-125333-position-map/`, the cue phrase in
`analysis-20261015-132744-cue-phrase/` (`uv run python -m scripts.exp12_position_map.cue <run>`). Eligible n=77 (answer: 72); positions -14..0 analysed
(reached by at least half the questions; -11..0 by 76-77).

| Reader | Bridge: best position | Share of layers 32-48 [95% CI] | Held-out halves (position: share) | Answer: best position | Share | Distractor ceiling |
|---|---|---|---|---|---|---|
| logit lens | -1 | 0.37 [0.28, 0.46] | -1: 0.36, -3: 0.36 | 0 | 0.14 [0.09, 0.20] | 0.06 |
| J-lens | -1 | 0.65 [0.54, 0.74] | -1: 0.67, -1: 0.62 | 0 | 0.41 [0.32, 0.50] | 0.11 |
| J++ | -1 | 0.64 [0.54, 0.73] | -1: 0.67, -1: 0.61 | 0 | 0.38 [0.29, 0.47] | 0.11 |

- In layers 24-40 the bridge at -1 is first in 0.61 [0.50, 0.71] (J-lens) and 0.63 [0.53, 0.73] (J++) of the layers,
  almost as often as in 32-48: one word before the end it is readable from the early layers on.
- Depth (half the questions first, bridge at -1 vs answer at the last word): J-lens L23 vs L44, lag 19 [15, 27];
  J++ L22 vs L43, 22 [17, 30]; logit lens L40 vs L51, 11 [-4, 14].
- Same optimum on the balanced panel (the 76 questions that reach every position -11..0), so prompt length does not
  drive it.
- Read at position -1, the questions whose J-space swap flips the answer have the bridge first in 0.73 [0.56, 0.88]
  of layers 32-48, the others in 0.60 [0.47, 0.73] (J-lens, split by the J-lens swaps, n=25 / 49); J++ split by its own
  swaps (run `20261015-100947`): 0.75 [0.63, 0.86] vs 0.51 [0.36, 0.65] (n=39 / 37).
- Missed at the last word: J-lens 30 questions, bridge first earlier in 73% [57, 90] (distractor 33% [17, 50]);
  J++ 31, 77% [61, 90] (distractor 26% [13, 42]).
- Earlier run, prompts as published with part B's earlier labels (`20261014-095358`, 67 eligible): the same picture
  (J-lens bridge at -1: 0.66; lag 21 [16, 28]).

![exp12: reference heatmaps](figures/exp12_position_map/position_layer.png)

*Reference: every position x layer for all three readers, colour = share of questions with the word ranked first; the
box marks the best position over layers 32-48. The line figure above shows the J-lens rows that matter.*
</details>

### exp14_cue_answer_swaps: on the cue phrase, is it the bridge or already the answer?
**What we measure.** Swapping the bridge changes the answer when the swap edits the cue phrase ("Amazon River ends"),
and exp12 reads a little of the answer there too. If that phrase already held the answer (a shortcut: Amazon River ->
Portuguese), swapping the answer's direction there should change the answer as often as swapping the bridge's. Both
swaps exchange two words' coordinates along their lens vectors (J-lens or J++), as part B's lens-vector swap does:
the bridge pair (Brazil -> Mexico) or the answer pair (Portuguese -> Spanish), on the cue phrase at layers 24-40. The
answer swap's positive control is the same swap at the last token, where the answer is written (layers 24-40, and
40-56 where exp12 reads it). Every swap has a random direction of the same edit size. The decision rule
was fixed in the config before the run.

**In short.**
- **Both swaps change the answer on the cue phrase, the bridge's more often.** Bridge 30% [21, 41] of the questions
  (J++) / 22% [14, 33] (J-lens), answer 17% [10, 27] / 11% [6, 20], random directions 0%; bridge minus answer +14
  points [+3, +25] / +12 [+3, +22]. The answer swap's positive control works: at the last token, layers 40-56, it
  flips 40% / 39%. By the rule fixed before the run that is "both", so the overlap between the two swaps decides.
- **On the cue phrase the answer swap works only where it is also a bridge swap.** Split at the median overlap (the
  cosine between the bridge pair's and the answer pair's difference vectors): where the two swaps overlap little,
  the answer swap flips 0 of 35 questions (J++) / 1 of 36 (J-lens) on the cue phrase, the bridge swap 14% / 6%.
  Almost every answer-swap flip is a question whose answer is tied to its bridge in J-space (Spain -> Madrid,
  Japan -> Tokyo, Russia -> Russian; cosine 0.6-0.9). The lens data show no answer on the cue phrase apart from the
  bridge.
- **But the questions that separate the two are weak tests.** Where the overlap is low, the answer swap also rarely
  works at the last token (14%), and the bridge swap rarely on the cue phrase. Most swap effects live in the place
  questions, where bridge and answer cannot be pulled apart along their token directions.

![exp14: bridge vs answer swaps](figures/exp14_cue_answer_swaps/flip_rates.png)

*How to read it: one panel per lens; each pair of bars is the share of questions whose answer changes to the swap
target's, when the bridge (blue) or the answer (orange) is swapped at the given positions and layers; the grey bars
(right of each, mostly at 0%) are random directions of the same edit size. On the cue phrase blue is above orange; at
the last token, layers 24-40, neither works; at layers 40-56 both do, the answer more.*

![exp14: split by overlap](figures/exp14_cue_answer_swaps/flip_rates_by_overlap.png)

*How to read it: the same swaps, for the 72 questions where both swaps are possible (single-token answers), split
in two halves of about 36: those whose bridge and answer swaps overlap little (left of each pair of groups) or much. On the cue phrase the orange bar is near 0 where the overlap is low: the answer swap only works where
it moves the bridge too.*

**What this does not show.** The median split was chosen after seeing the results. The swaps move only the two words'
token directions, so an answer held in other directions on the cue phrase would be missed. The answer swap's edits
are a little smaller than the bridge's (median 0.010 vs 0.012 of the residual norm, J++). One seed.

**Pinned run: the other pair held.** In the place questions the two swaps move nearly the same direction, so the
plain swaps cannot tell bridge from answer there. The pinned swaps exchange one pair's coordinates while the other
pair's stay at their clean values: what still works moves only what its pair does not share with the other. Run
`pinned.yaml` (the 72 questions where both swaps are possible); decision rule fixed in the config before the run.
- **On the cue phrase the bridge swap still works with the answer held; the answer swap with the bridge held hardly
  does.** Bridge swap, answer held: 18% [11, 28] of the questions with either lens; answer swap, bridge held: 6%
  [2, 13] (J-lens) / 1% [0, 7] (J++); random directions 0%. Difference +12 points [+3, +24] (J-lens) / +17 [+8, +26]
  (J++); in the half where the two swaps overlap most, where the plain swaps could not separate them, the held bridge
  swap flips 28% / 24% against 8% / 3%: +19 [0, +39] / +22 [+5, +38]. Holding a pair does not shrink the edit (the
  held swap's edit is 0.95-1.05 times the plain one's, median per question; none under 30%), so this is content, not
  dose. By the rule fixed before the run: "bridge". The cue phrase carries the bridge apart from the answer's
  direction.
- **Whether the cue phrase also carries the answer is not decided.** The held answer swap's positive control falls
  short: at the last token (layers 40-56) it flips 26% [18, 38] / 17% [10, 27] of questions, below the 30% the rule
  asked for, so its low rate on the cue phrase says nothing by itself.
- **Most questions move under neither held swap.** On the cue phrase 55 (J-lens) / 58 (J++) of 72 questions flip
  under neither; 13 only under the held bridge swap, 4 / 1 only under the held answer swap.
- Not in the rule, read afterwards: at the last token, holding the answer cuts the bridge swap from 29% / 28% to
  11% / 10%; there the bridge swap works mostly through the direction it shares with the answer.

![exp14: swaps with the other pair held](figures/exp14_cue_answer_swaps/flip_rates_pinned.png)

*How to read it: as the first exp14 figure, with two more bars per group: the bridge swapped while the answer's
coordinates are held (dark blue, hatched) and the answer swapped while the bridge's are held (dark orange, hatched).
On the cue phrase the dark blue bar stays near the plain bridge swap and the dark orange one falls to near 0.*

<details><summary>Full numbers and checks</summary>

Run `results/exp14_cue_answer_swaps/20261015-111137` (Qwen3.6-27B, part B's model loader, prompts and scoring as part
B v4; the answer rows are the 72 questions with single-token answers); overlap split in
`analysis-20261015-134641-overlap/`. Checks: the eligible questions equal part B's v4 ones (77 of 77); the bridge
swaps reproduce part B's lens-vector swaps (`exp02_swaps/main_v4_*_pos-cue`, `_pos-last`) question by question:
J++ 154 of 154 outcomes (cue phrase 23/77 = 29.9% in both, last token 1/77), J-lens 152 of 154 (cue phrase 17/77 =
22.1% here vs 16/77 = 20.8%; last token 1/77 in both). The two J-lens differences are borderline greedy
continuations, likely bf16 differences between GPUs (part B ran on an H200, exp14 on an A100):
`city-state-Philadelphia` (real swap: "Pennsylvania" there, "Washington" here) and `etym-saturn-position` (random
direction: "5" there, "4 from the Sun" here).

| Swap, flip rate [95% Wilson CI] | J-lens bridge | J-lens answer | J++ bridge | J++ answer |
|---|---|---|---|---|
| cue phrase, layers 24-40 | 22% [14, 33] | 11% [6, 20] | 30% [21, 41] | 17% [10, 27] |
| last token, layers 24-40 | 1% [0, 7] | 1% [0, 7] | 1% [0, 7] | 4% [1, 12] |
| last token, layers 40-56 | 29% [20, 39] | 39% [28, 50] | 27% [19, 38] | 40% [30, 52] |
| random direction, any cell | 0% | 0% | 0% | 0% |

- Overlap (median over questions of the mean cosine over layers 24-40): 0.26 (J-lens), 0.28 (J++); up to 0.93-0.97.
  The share of the bridge swap's edit that lies in the answer pair's span: median 0.30.
- At the last token, layers 40-56, the bridge swap's 27-29% is also mostly overlap: 44-49% where it is high, 9-11%
  where it is low.

Pinned run `results/exp14_cue_answer_swaps/20261015-114825` (`pinned.yaml`; 72 questions with single-token answers),
analysis in `analysis-20261015-143152-pinned/`. Checks: the 1192 outcomes it shares with run 20261015-111137 (plain
swaps and their nulls) agree, all of them; eligible questions 77 of 77 as part B's.

| Flip rate [95% Wilson CI], 72 questions | J-lens bridge held-answer | J-lens answer held-bridge | J++ bridge held-answer | J++ answer held-bridge |
|---|---|---|---|---|
| cue phrase, layers 24-40 | 18% [11, 28] | 6% [2, 13] | 18% [11, 28] | 1% [0, 7] |
| cue phrase, high-overlap half (36 / 37) | 28% [16, 44] | 8% [3, 22] | 24% [13, 40] | 3% [0, 14] |
| last token, layers 40-56 | 11% [6, 20] | 26% [18, 38] | 10% [5, 19] | 17% [10, 27] |
| random direction, any cell | 0% | 0% | 0% | 0% |

- Plain minus held (paired bootstrap, same 72 questions): bridge on the cue phrase +6 [-1, +14] (J-lens) / +12 [+4,
  +21] (J++); answer on the cue phrase +6 [+1, +11] / +15 [+7, +24]; at the last token bridge +18 [+10, +26] / +18
  [+8, +28], answer +12 [+4, +22] / +24 [+14, +33].
- Held bridge minus held answer on the cue phrase, low-overlap half: +6 [-3, +17] / +11 [+3, +23].
</details>

### exp15_oracle_lens: where the lenses miss the bridge, does the oracle lens name it?
**What we measure.** The J-lens and J++ read one token direction at a time. Where neither ranks the bridge first, is it
absent from the activation, or held in a form no single token direction names? The oracle lens is a LoRA on
Qwen3.6-27B trained to put one residual vector into words (`neuronpedia/jacobian-lens`, `qwen3.6-27b/oracle`; its
published read contract: the vector replaces a marker token's embedding in a fixed prompt; trained on layers 20-60 in
steps of 4). It reads the 77 questions at the last word, -1 and the cue phrase's last token: in "...the country where
the Amazon River ends is" these are "is", "ends" and "River". One reading = the oracle's words for the activation at
one question, position and layer. Layers: 28, 36 and 44 first (the run the decision rule was fixed for, 693
readings), then the rest of the oracle's grid in two more runs with the same config (24/32/40/48 and 20/52/56/60):
2541 readings in all. Each reading is grouped by exp12's lens readings at the same question, position and layer: both
lenses rank the word first among its candidates, one does, or neither. A word counts as named if it appears in the
oracle's text (whole word, case and a plural ending ignored). Controls: the word's distractor (Mexico for Brazil),
other questions' bridges, the mean activation over questions read instead, and the activation after exp14's J++
bridge swap on the cue phrase (if the oracle re-solved the question instead of reading the activation's state, it
would keep naming Brazil). The decision rule was fixed in the config before the first run. Greedy decoding, 64 tokens.

**In short.**
- **The oracle is loaded and reads.** Before any reading, in every run, it named the answer of 6 of 6 short facts ("The
  capital of France is" -> Paris), a random vector named none of them, and switching the adapter off left the model's
  logits unchanged.
- **The run the rule was fixed for (layers 28/36/44): "the oracle reads the bridge where the lenses miss it, and
  follows the state the answer uses".** Where both lenses have the bridge first it names it in 82% of readings
  (distractor 4%); where neither does, in 37% (distractor 4.5%; +32 points [+22, +43], 250 readings of 59
  questions). After the bridge swap, on the 23 questions whose answer it changes, it names the swap target at layer 44
  in 67% [54, 80] of them (last word and -1; before the swap 4%); on the 54 whose answer stays, 10% [4, 18].
- **Side by side on the same activations (all 11 layers), the oracle has the bridge a little more often than either
  lens, and the answer much more often early on.** The bridge: J-lens / J++ / oracle 34% / 42% / 47% at layer 20,
  59% / 59% / 69% at 36, 82% / 78% / 82% at 60. The answer: 11% / 21% / 40% at layer 20, 26% / 25% / 49% at 36,
  65% / 63% / 67% at 60, but the oracle also names the answer's distractor more often (7-13% of readings, the lenses
  1-6%).
- **Where neither lens ranks the bridge first, the oracle names it in 37% of readings** (distractor 4%; +33
  [+25, +41]; 862 readings of 68 questions), at every layer (29-58%). Mostly where the lenses nearly have it: 54% when
  the better lens ranks it 2nd-3rd, 29% at 4th-10th, 22% [12, 33] at 11th or lower (215 readings, 38 questions). The
  answer: 34% vs its distractor's 8%.
- **The swap reaches the last words between layers 32 and 40.** After the swap, on the questions whose answer it
  changes, the oracle names the swap target at the last word or -1 in 2-7% of them at layers 20-32, 39% at 36, 67-74%
  at 40-48 and 83-89% at 52-60; on the questions whose answer stays, 0-13% up to layer 48, but 24-25% at 52-60, where
  it is less specific.

![exp15: three readers by layer](figures/exp15_oracle_lens/readers_by_layer.png)

*How to read it: one line per reader on the same activations; y: the share of readings where the reader has the word
(J-lens, J++: rank it 1st among the candidates; oracle: name it), by layer. Dashed: the same reader has the word's
distractor instead, its own false-alarm baseline. The two criteria differ, so read each solid line against its own
dashed one.*

![exp15: oracle vs lenses](figures/exp15_oracle_lens/oracle_vs_lenses.png)

*How to read it (all 11 layers): left to right, readings where the lenses see the word less and less (both rank it
1st, one does, then neither, by how far down the better lens has it). Bars: how often the oracle names the bridge
(blue) or the answer (orange) there. Dashed lines: how often it names the word's distractor where the lenses miss the
word, its false-alarm baseline. The bars fall from about 85% to about 20%, and stay above the dashed lines.*

![exp15: after the swap](figures/exp15_oracle_lens/after_swap.png)

*How to read it: the share of questions whose oracle words name the swap target (e.g. Mexico) at the last word and -1,
layer 44. Left: before the swap, on the 23 questions whose answer the swap changes. Middle: after the swap, the same
questions. Right: after the swap, the 54 questions whose answer stays. If the oracle only re-solved the question from
the activation, the middle bar would stay as low as the left one.*

![exp15: by layer](figures/exp15_oracle_lens/by_layer.png)

*How to read it: left, where neither lens ranks the bridge 1st, the share of readings naming it (blue) and its
distractor (grey dashed), by layer. Right, the swap target named after the swap, by layer; grey band: the layers the
swap edits.*

**Is the oracle an extra monitor where the lenses miss the bridge?** At one position and layer, partly; for a
question read at many layers, no, because both already find the bridge somewhere in every question.
- Per reading (2541): the lenses (either one ranking it 1st) and the oracle both have the bridge in 54%, only the
  lenses in 12%, only the oracle in 14%, neither in 20%. Where the lenses miss it, the oracle names the distractor in
  5%. The answer: both 32%, lenses only 11%, oracle only 21%, neither 36%; distractor 9%.
- Per question: across all 33 readings of a question (3 positions x 11 layers) both reach the ceiling: the lenses rank
  the bridge 1st somewhere in all 77 questions and the oracle names it somewhere in all 77 (the answer: 61 of 61),
  while the distractor is found somewhere in only 30 (lenses) and 24 (oracle). With one layer's 3 readings there is
  room to differ, and the verbalizers add a few questions at equal false alarms: the bridge in 73 vs 69 questions
  (oracle, layer 40; distractor 9 vs 12), 71 vs 71 (oracle, 44), 75 vs 71 (NLA, 42; distractor 10 vs 10); the answer
  in 58 vs 44 (NLA, 42; distractor 11 vs 10).
- What it adds is mostly a weaker version of the same signal (the lenses have the word 2nd-10th), not a different
  one: where the lenses have it 11th or lower it names the bridge in 22% of readings (38 questions), the case most open
  to re-solving (next point).

**How the oracle names the bridge.** It rarely lists the bridge as a concept: mostly it re-tells the question with the
bridge filled in ("The Vatican is located on the continent of" for "the smallest country"; no prompt names its
bridge). Each naming sorted by a rule fixed before counting: a bullet that is the bridge itself ("- Brazil",
"- 巴西 (Brazil)"), an answer phrase ("The answer is carbon", "(Answer: Brazil)"), or inside a sentence:

| Readings that name the bridge | bullet = the bridge | "the answer is ..." | inside a sentence |
|---|---|---|---|
| both lenses have the bridge 1st (1222) | 22% | 6% | 71% |
| neither lens has it 1st (345) | 8% | 5% | 87% |
| after the swap, the swap target, answer changed (241) | 33% | 0% | 67% |

So most of the 37% is the oracle writing out the question with the bridge resolved, and the text cannot say whether
the bridge came from the activation's state or from the oracle (the model itself) solving the question it reads off
the activation. The swap test says the state, but only on questions the lenses mostly see (5 of the 23 have lens-blind
readings at -1 or the last word in layers 36-44), and 17 of those 23 are one template ("the capital / continent /
currency / language of the country where X is"), with a country as the bridge. A fixed-seed sample of 30 lens-blind readings with their types is in
`mention_sample.json` for a human to check; the rule has known misses ("Swan Lake" counted as the bird).

Worked examples: [examples/exp15_oracle_lens/index.html](examples/exp15_oracle_lens/index.html): every question, with
the model's own answer before and after the swap, the lens ranks and the oracle's words in each row; filters by group
(lenses miss · oracle sees, lenses miss · oracle misses, lenses always see, swap changes the answer) and by layer. The
exp11 and exp12 pages show the same oracle words under each card ("Oracle lens (exp15)").

**What this does not show.**
- That the oracle reads the lens-blind bridge from the state rather than re-solving it (above).
- Its output format is its own, not our pipeline's: its bullets often open mid-sentence or with a Chinese token
  ("- , USA, was invented?", "- 奶牛 (cow)"), and WorkspaceBench's reference code path (peft's PeftModel, its
  sampling) gives the same texts on the same activations (`results/checks/reference_readers-20261015-145931.json`:
  greedy texts identical for their first 68-726 characters, then bf16 noise; sampled texts with one seed nearly
  identical; the same for the NLA). Sampling does not turn them into clean concept lists either.
- Layers other than 28/36/44 come from runs made after seeing the first; the decision rule applies to the first run
  only. The lens-blind readings differ from layer to layer, so the by-layer curves mix changing sets of readings.
- String matching: a bridge named only in another script (e.g. 巴西 for Brazil, without "(Brazil)") is missed, for
  the bridge and the distractor alike. One seed; positions pooled.
- Multi-token words: every bridge here is a single token (the probe-swap set's 97 entities); the answer lines use the
  61 questions whose answer is a single-token word (5 multi-token and 11 numeric answers left out).

<details><summary>Full numbers and checks</summary>

Runs (Qwen3.6-27B, part B's model loader, the 77 questions of part B's v4 labels, trailing space stripped; oracle
adapter pinned by sha256 in `pins.py`): `results/exp15_oracle_lens/20261015-123226` (layers 28/36/44, the decision
rule's run; analysis `analysis-20261015-160336/`), `20261015-134316` (24/32/40/48) and `20261015-140424`
(20/52/56/60); all three pooled in `20261015-140424/analysis-20261015-171154-combined/` (summary.json with the
monitoring split and the mention types, mention_sample.json, the README's figures). Checks, every run: the sanity gate
(`sanity.json`: 6 of 6 facts, random vector 0 of 6, base-logit drift 0.0; 496 LoRA modules, r 16, scale 2); the
swapped forward's top word equals exp14's for 77 of 77 questions.

| Readings (clean, 11 layers), by the lenses | readings / questions | bridge named | distractor named |
|---|---|---|---|
| both lenses have the bridge 1st | 1429 / 77 | 83% | 5% |
| one lens | 250 / 64 | 61% | 3% |
| neither lens | 862 / 68 | 37% | 4% |

Each question weighted equally. Another question's bridge is named in 0.1-0.4% of readings; the bridge from the mean
activation in 4%. The answer (61 questions whose answer is a single-token word; the 11 numeric answers are left out,
since the oracle's numbered bullets "2. ..." would count as naming them): both lenses 87% (distractor 12%), one lens
64% (7%), neither 34% (8%).
</details>

### exp16_nla: does a second verbalizer, the NLA, see the same?
**What we measure.** exp15 with another reader: the NLA (natural-language autoencoder), a separate 27B model trained
to describe layer-42 activations of Qwen3.6-27B (`ceselder/qwen3.6-27b-nla-rl`: `av_base` plus the GRPO adapter
`iter_000400`, WorkspaceBench's choice; its read contract: the vector added, norm-matched, after its block 1 at a
marker token; the explanation between `<explanation>` tags). It has its own weights and another training objective
than the oracle lens, but it is built on Qwen3.6-27B (`av_base` is the model fine-tuned) and so knows what the model
knows: the two can agree by solving the question the same way. Same 77 questions, positions, controls and scoring as exp15, at layer 42 only, the
NLA's one layer; 693 readings. Two phases on one GPU: Qwen3.6-27B captures every vector and unloads, then the NLA loads.
Greedy, 160 tokens. The decision rule (exp15's, at layer 42) was fixed in the config before the run.

**In short.**
- **The NLA is loaded and reads.** Before any reading it named the answer of 6 of 6 short facts from their layer-42
  activations, a random vector named none, and its logits are unchanged once the adapter is off again. Its output
  is in its trained format (2-3 short notes on what the text sets up), unlike the oracle's fragments.
- **By the rule fixed before the run: "the NLA reads the bridge where the lenses miss it, and follows the state the
  answer uses".** Where both lenses have the bridge first it names it in 91% of readings (distractor 2%); where
  neither does, in 46% (distractor 10%; +36 points [+20, +50], 76 readings of 46 questions). After the bridge swap,
  on the 23 questions whose answer it changes, it names the swap target at the last word or -1 in 59% [46, 72] of them
  (before the swap 4%); on the 54 whose answer stays, 11% [5, 18]. The answer, where neither lens has it first: 36%
  vs its distractor's 7%.
- **Every reader at layer 42: the two verbalizers agree, and both have the words more often than the lenses.** The
  bridge: J-lens 65%, J++ 62%, NLA 75%, the oracle lens 70% / 65% at its nearest layers 40 / 44; false alarms 3-5%
  for all. The answer: 38%, 34%, 57%, 54% / 55%; false alarms 4-9%. Where neither lens has the bridge first: NLA 46%,
  oracle 54% (40) / 38% (44).

![exp16: every reader at layer 42](figures/exp16_nla/methods_at_42.png)

*How to read it: one row per reader, at layer 42 (the oracle lens at 40 and 44, its trained layers nearest 42).
Filled dot: the share of readings where the reader has the word (a lens ranks it 1st; a verbalizer names it); hollow
dot: where it has the word's distractor instead, its false alarms. Right panel: the readings where neither lens ranks
the bridge 1st (the lenses are at 0% there by definition, so only the verbalizers are shown).*

![exp16: after the swap](figures/exp16_nla/after_swap.png)

*How to read it: as exp15's: the share of questions whose NLA explanation names the swap target at the last word and
-1, before and after the swap.*

**By part B's swap labels: is what the verbalizers add the part outside the J-space?** Part B labels each question
by which swap changes its answer: J-mediated (the bridge's J-space part; 25 questions with J-lens swaps) or neither
(no swap; 49; non-J has 1 question and both 2, too few). Where the J-space swap does not move the answer, the lenses
rank the bridge 1st less often (62% vs 75% of readings), while the verbalizers name it about as often as in the
J-mediated questions (oracle, layers 32-48: 67% vs 66%; NLA, 42: 76% vs 75%). Their edge over the lenses is in the
neither questions (+5 and +12 points) and not in the J-mediated ones (-9 and -1): a difference of -14 points
[-28, -1] (oracle) and -14 [-26, -1] (NLA); J++ labels give the same (-20, -19). On the lens-blind readings, too,
they name the bridge more in the neither questions (43-56% vs 23-39%). This is what a reader of a part the J-lens
cannot see would show, and was the question this project set out with; but the verbalizers' rate is flat across the
two groups and only the lenses' changes, which a reader that solves the question whatever the state holds would show
too. exp17 is what tells the two apart.

![exp16: by swap label](figures/exp16_nla/by_swap_label.png)

*How to read it: per verbalizer, the questions split by part B's label (J-lens swaps); grey: the share of readings
where the J-lens or J++ ranks the bridge 1st; colour: where the verbalizer names it, on the same readings. In the
title: the verbalizer's edge over the lenses, J-mediated minus neither, with its 95% CI.*

Worked examples: [examples/exp16_nla/index.html](examples/exp16_nla/index.html) (every question, the NLA's
explanations before and after the swap next to the lens ranks); the exp10-12 pages show them under each card ("NLA
(exp16, layer 42)"), next to the oracle lens's.

**Reading or solving, in the NLA's own words.** The NLA quotes the text it decodes from the activation and comments on
it, and its comments often solve the question outright: "The phrase 'the sport invented in the city of Springfield'
is a well-known reference to basketball", "a multi-step reasoning chain: identify Rome's country (Italy)" (the prompt
says Naples), and it invents context the prompt does not have ("Multiple Choice Question" headers, "The answer is
2"). Two cheap measures, with rules fixed before counting:
- *Quoted or commented.* No prompt contains its bridge, so a bridge inside the NLA's quotation of the prompt means it
  recalls the prompt with the bridge already filled in ("The fruit that ... the drink wine is made from" for "the
  alcoholic drink served at communion"), a hint that the bridge is in the state; a bridge only in its comments is more
  likely its own solving. Of its lens-blind namings, 63% are quoted and 37% comments (35 namings); where the lenses
  see the bridge, 54% / 46%; the swap target after the swap, 70% / 30%. The rule misfires on titles ("The Swan Lake"
  counted as quoting the bird): a fixed-seed sample of 30 is in `quote_sample.json` for a human check. (The oracle
  lens rarely quotes, 3%, so this split does not apply to it.)
- *A solving calibrator: the answer by position.* Where the lenses rarely have the answer, a reader naming it is most
  likely solving. On the cue phrase the readers name the answer no more often than a lens ranks it first there (NLA
  23% vs 30%; oracle, all layers, 30% vs 27%): no sign of extra solving there. At the last word they name it far more
  often (NLA 93% vs 62%; oracle 82% vs 59%), but that is where the model writes its answer, so they may be reading
  its next-token prediction rather than solving.

**What this does not show.** That the NLA reads the lens-blind bridge from the state: its texts show it solving, and
the quoted share is a hint, not a test. Agreement with the oracle lens does not rule out solving either (both know
the facts). Its false alarms are higher where the lenses miss the bridge (10% vs the oracle's 4-5%). The swap test
covers the same 23 questions, 17 of them one country template. One layer, so the lens-blind groups are small (46
questions, CI [+20, +50]). Greedy decoding; the reference reader samples. One seed.

<details><summary>Full numbers and checks</summary>

Run `results/exp16_nla/20261015-144540` (Qwen3.6-27B through part B's loader for the capture; the NLA pinned in
`pins.py`: repo revision and the adapter's sha256); analysis with exp15's tools in `analysis-20261015-171150/`; every
reader at layer 42 in `analysis-20261015-170413-compare/` (`scripts/exp16_nla/compare.py`, with exp15's runs
20261015-123226 and 20261015-134316 for the oracle at 44 and 40). Checks: the NLA's gate (`sanity.json`: 6 of 6
facts, random vector 0 of 6, logit drift 0.0, the adapter moves its logits by up to 6.6; 496 LoRA modules, rsLoRA
r 64, scale 2); the swapped forward's top word equals exp14's for 77 of 77 questions. A pilot on 3 questions
(`cache/smoke/`, not kept) ran before the full run.
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

### exp09_bind_recall (part B): is a bridge bound in context outside the J-space, like brew's? No
**What we measure.** Part B's two settings point opposite ways: the recalled bridge acts through its J-space part
(exp02), brew's intermediate is carried outside the J-space (exp04, exp07). They differ in much more than where the
bridge comes from, so this run holds the question, the countries and the second hop fixed and changes only that.
Every prompt first binds three people to three countries; then R asks "The capital of the country where {city} is
located is" (the bridge recalled from the city) and B "The capital of the country where {person} lives is" (the bridge
bound in the prompt). 13 countries (those with exp01 probes), 760 items (`data/bind_recall.json`, made by
`scripts/exp09_make_items.py`); 65 R and 80 B items are token-aligned, answered correctly and sampled. Both part B
methods run on both families, with decision rules fixed in the manifests:
- *exp04's pipeline, lens-free.* The counterfactual C sets the bridge to X while keeping every country in the prompt
  (R: the city becomes a city of X; B: the queried person and X's holder swap countries); the control O swaps two
  off-path holders. A map copies C's activation into the original, one layer at a time, at the question's tokens after
  the change or at the last token; at the window it finds, below the layer where the last token alone carries the
  answer, the copy is split into its J-space part and the rest (J++), and into its I/X lens coordinates and the rest.
- *exp02's probe swaps.* exp01's J++ probes of I and X swapped at the cue phrase (the city to "located"; the person and
  "lives"), layers 24-40: the J-part, the full probe, the remainder and the matched-alignment control.

**In short.**
- **A bound bridge is carried inside the J-space, so the pre-registered hypothesis (recalled inside, bound outside)
  is refuted.** At B's window (layer 40) the copy of the question's tokens gives X's capital for 70% of items; its
  J-space part alone for 12.5% and the rest for 0% (rest minus J-space part: -12.5 [-20, -6] pts); its I/X lens
  coordinates 7.5%, the rest 0%. The J-space part holds 29% of the copied difference's variance (a random
  direction's: 7%). Brew's intermediate, also in the prompt, gave the opposite (exp04).
- **For the recalled bridge, exp02's swap replicates strongly; the split is inconclusive.** The J-part swap flips 82%
  [70, 89] of R items, the matched-alignment control 3% (+78 [+68, +88] pts), the full probe 18%, the remainder 2%. At
  R's window (layers 36-40) the copy gives 44%, but its J-space part 4% and the rest 7% ("both or neither").
- **Where the bridge arrives.** Copying the question's tokens moves the answer from layer 36 in R (29%, 60% at 40)
  and from layer 40 in B (5% at 36, 70% at 40); the last token alone from 44-48 in both. The off-path copy changes at
  most 5% of answers anywhere (R, last token, layer 52).
- **The probe swap does not move the bound bridge at all** (0% for every condition, the full probe included), so by
  its rule B's swaps are not interpreted: the swap edits layers 24-40 at the cue phrase, while the map has B's bridge
  arriving at the question only at layer 40.

Read together with brew: being in the context is not what puts a variable outside the J-space. A bound bridge here is
retrieved as a word of the prompt and then used by a recalled fact; brew's intermediate is the output of a lookup in
an in-context table, read by a second in-context lookup. Which of those differences matters is open (Next steps).

![exp09: recalled vs bound](figures/exp09_bind_recall/v1/bind_recall.png)

**What this does not show.** The split recovers little of the copy in either family (12.5% of B's 70%, 4-7% of R's
44%): pieces of the copied difference act much less than the whole, so "inside" rests on small effects, and B's window
is one layer. In B the bridge is a word in the prompt, so its J-space part may be the copied word's identity. The
second hop is a recalled fact in both families, so a copy can carry the bridge or its capital; the window stops where
the last token alone carries the answer (from 48 in B, 52 in R, capped at exp12's 44). One seed for the counterfactual
cities and the sample.

<details><summary>Full numbers and checks</summary>

Runs under `results/exp09_bind_recall/`: `map_v1` (layers 0-60 every 4th, the question's tokens and the last token,
C and O), `parts_v1` (its window), `swaps_v1` (exp02's conditions and nulls), each with its manifest written before
the run; parts and swaps reuse the map's eligibility and sample. Probes: `exp01_probes/v3_jpp_b200`, the `more_jpp`
variant rebuilt on the B200 box (v3_jpp's cache stayed on the old box): 2261 of 2673 prompts kept as before, 7 filter
decisions differ, the J-space share by layer within 0.001 of v3_jpp. Items are identified by family and file index:
the item file's `name` field repeats (Pitfalls). Generation is batched per item (`Model.generate_batch`, checked
against single runs: identical but for degenerate continuations). Figure: `uv run python scripts/exp09_figures.py
<new folder>`. Headlines are recomputed by `scripts/verify_headlines.py`.
</details>

### Pitfalls found so far
1. **Trailing space.** Most original prompts end in a space (83/93), which Qwen's tokenizer leaves as a lone `" "`
   token. The model then answers far worse (27B: 21/93 correct vs 61/93 with the space removed) and the lens reads a
   different token. Every experiment now removes it (Setup).
2. **Numbers split into digits.** Qwen splits `" 26"` into `" "`, `"2"`, `"6"`, so scoring "26" by its first token
   gave fake hits (fixed in `d068538`; the two runs before the fix, `20261013-204427` and `-204551`, are superseded
   and not committed). Headlines use only single-token bridges.
3. **"The bridge is visible somewhere" is too weak.** Across all layers x tokens, a same-category distractor (Mexico
   for Brazil) also reaches the top somewhere. The read-site map must compare the bridge against a distractor.
4. **Best-of-all-layers favours the logit lens on deep models** (see the layer plot). exp11/exp12 average over the
   middle-layer band 32-48 instead.
5. **Token positions differ between prompts.** exp12 aligns them by distance from the last word, which mixes roles
   ("-1" is "ends" in one prompt, "is" in another); checked by splitting on the last word.
6. **The bridge named in the prompt.** Checked: one lens-eval question names its bridge ("the time of day ..." ->
   "day"); an earlier substring count of 5 also matched single-letter bridges inside other words (H in "The"). It
   does not move exp10's numbers.
7. **Number bridges and best-of-all-layers.** Over all layers the logit lens finds number bridges ('6', 'four') more
   often than the lenses, at layers 54-60; within layers 32-48 the lenses lead for numbers too. Mixing number and word
   bridges, and taking the best of all layers, both hide the J-lens's lead (exp10 reports both splits).
8. **Numeric answers in a verbalizer's text.** "2" matches the oracle's list numbering ("2. ..."), so the 11 numeric
   answers are left out of every verbalizer answer rate; word matching treats digits as part of a word.
9. **A pre-commit hook rewrote pinned data.** `end-of-file-fixer` added newlines to `data/` and `results/` files,
   which changes their sha256 pins; reverted, and the hooks now skip `data/`, `results/` and `examples/`.
10. **"Found somewhere in the question" saturates.** Read at 33 positions and layers, both the lenses and the oracle
    find every question's bridge somewhere, so question-level coverage can only be compared at one layer, against the
    distractor (exp15).
11. **A verbalizer can solve instead of read.** The oracle re-tells the question with the bridge filled in, the NLA
    comments on it; naming the bridge is not by itself evidence that the state holds it (exp15, exp16).
12. **Repeated item names.** `scripts/exp09_make_items.py` numbered each list comprehension from one length, so
    `data/bind_recall.json` has 61 distinct names for 760 items; exp09 identifies items by family and file index, and
    its map, which only counts outcomes per cell, was unaffected.
13. **Kernel launches bound generation.** On the B200 box a greedy 8-token continuation spends 0.65 s of CPU against
    0.15 s of GPU (~28k small kernels): batching an item's edited runs (`Model.generate_batch`) is 12-26x faster.

### Decisions
- **Trailing space: removed in every experiment, part A and part B** (2026-10-13 for part A; part B followed in its
  v4, which also judges answers on the greedy continuation). Runs on the prompts as published are kept only as a
  check. Why:
  - The protocol reads "the token right before `target`". In natural text that is `" is"`; the lone `" "` exists only
    because the prompts were written for another tokenizer, and after it the answer becomes a fragment (`"Port"`).
  - We study reasoning the model actually does: 27B answers 61/93 stripped vs 21/93 as published. 21 items is also
    too few for swap rates with useful CIs.
  - The lone `" "` invites digits, which produced fake hits (pitfall 2): 6 at layer 0 on 4B vs 0 when stripped.
  - Part B uses the same prompts (29/90 probe-swap prompts end in a space), so both parts must treat them the same.
  Against: numbers are not 1:1 with the paper (hence the check on the published prompts). The J-lens reads the bridge
  more often on the lone `" "` (4B: 0.62 vs 0.44), but that is confounded with the digit artifact and with the model
  mostly failing there.
- **pass@k counts a bridge found if any of its listed forms is** ('5' or 'five'; 9 lens-eval questions list several),
  not the paper's share of forms (2026-10-15). The paper's rule is still reported (`pass_at_k_fraction`).
- **Layer bands: 32-48 primary, 24-40 alongside**, both part B's swap bands, named by their range (2026-10-15).
- **Keep the lens-eval question that names its bridge** ("the time of day ..." -> "day"; 2026-10-15): it is 1 of 93,
  moves no exp10 headline by more than a point, and the earlier count of 5 such questions came from a substring
  search that also matched single-letter bridges inside other words. This closes the open decision about them.
- **Next steps are written as question, why, test, cost** (2026-10-15), so each says what it would settle before it
  asks for GPU time.
- **The swap experiments end with exp14's pinned run** (2026-10-15): part A turned to the verbalizers.
- **Verbalizers are read only on their contract** (2026-10-15): the oracle lens on its trained layers 20-60 in steps
  of 4 (layer 42 is compared through 40 and 44), the NLA at 42 with WorkspaceBench's adapter `iter_000400`; greedy
  decoding for determinism, checked against the reference code path's sampled texts.
- **exp17 is brought as a design, not run** (2026-10-15): too few aligned pairs exist yet for a clean result, and the
  design is better reviewed first (the critic's recommendation).
- **Torch on the CUDA 12.8 wheels** (2026-10-15): the B200 box has no kernels in the cu126 build; the same torch
  2.11.0, its cu128 build and NVIDIA libraries (`uv.lock`), drivers >= 570.

### Open decisions (humans)
- Which headline numbers go into `VERIFIED.md` after a human recomputes them (`verify_headlines.py` lists every
  one with its source file).
- exp17: run it as designed below, change it, or drop it.

## Next steps (part A)
In order. Each item: the question, why it matters now, the test, and its cost. Every GPU run needs human sign-off.
exp14's pinned run closed the swap experiments; exp15 and exp16 showed two verbalizers naming the bridge where the
lenses miss it and following the model's state under a swap. What is left is whether that is reading or solving.

1. **On the lens-blind readings, do the verbalizers read the state or solve the question?** (exp17; designed, not
   run; design from the critic)
   - *Why:* 87% of the oracle's lens-blind namings are the question re-told with the bridge filled in, and the NLA's
     comments often solve it outright; both readers know the facts. exp15's swap test covers only 5 questions with
     lens-blind readings, and 17 of its 23 are one country template.
   - *Design:* pairs of questions in one template whose tokens line up and differ only in the cue entity, e.g. the
     recipient "...the country where Cairo is located is" and the donor "...where Lima is located is". Run the
     recipient with the donor's residual copied in at the cue tokens, layers 24-40 (exp14's swap band), and read the
     oracle lens (layers 36-48) and the NLA (42) at the recipient's last word and -1, downstream of the patch.
     - *Pairs:* the ~18 aligned pairs in the probe-swap set (nearly all places), plus pairs generated from the
       place templates (capital / continent / currency / language of the country where X is located) over cities with
       single-token names; built and token-checked without GPU first. Kept: both questions answered correctly.
     - *A patch counts* only if the model's own answer follows the donor (Spanish for Lima's language template).
     - *Controls:* the recipient unpatched (the reader's baseline: Egypt); the donor prompt itself (its ceiling: Peru);
       the same patch at as many non-cue tokens (the answer and the reader should not move).
   - *What each result means:* the reader names the donor's bridge (Peru) where the patch took: it reads the state
     the answer uses, also where the lenses miss it. It names the recipient's (Egypt) while the model answers like
     the donor: it solves the question from text it reconstructs, and its lens-blind readings say nothing about the
     state. Mixed: report both shares by layer; the swap test predicts more Peru from layer 36 on.
   - *Prediction:* mostly Peru at layers 40-48 (exp15's swap test: 67-74% there), a minority of Egypt where the
     reader re-tells the question from the prompt's early-layer tokens.
   - *Decision rule (draft, fixed before any run):* "reads the state" if, among pairs where the patch took, the
     reader names the donor's bridge at least 30 points more often than the recipient's (paired CI above 0) and the
     non-cue control moves neither; "solves" if it names the recipient's more often.
   - *Cost:* pair generation without GPU; then about an hour of GPU (Qwen captures and patches; the oracle reads in the
     same process; the NLA in a second phase).
2. **Brew, where the bridge is never named in the prompt** (after 1 shows the verbalizers read states)
   - *Why:* in brew's in-context lookup the intermediate is not an entity of the question, so a reader cannot recall
     it from world knowledge; exp04 locates it after the start line at layers 36-50.
   - *Test:* read those positions with the lenses first (done: exp08; J++ reads I at four of the 21 positions,
     the same four that carry the step in exp04's `positions_window`), then with the oracle and the NLA on the
     lens-blind cells, with a counterfactual context as the control.

Not measured yet, and worth a line in any write-up: **bridges of several tokens.** Every result above is on
single-token bridges (Setup). A multi-token bridge has no single lens direction to rank, so the lenses would need a
first-token or summed reading, while the verbalizers can name it as is; this is where they could differ most.

Parked: these were next steps; part A does not pursue them now.
- *Is the bridge at -1 a copy the answer does not use?* Patching -1 from a question with another bridge needs prompt
  pairs whose tokens line up: only 18 questions have one, nearly all places, so it would not separate copy from use.
- *Why do J++'s swaps flip more than the J-lens's, when both read the same bridge?* A question about the lenses, not
  about the bridge.
- *Reproduce J++'s published Recall@10; repeat on Gemma 4 31B.*

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
7. **What puts brew's intermediate outside the J-space** (exp09): a bound bridge used by a recalled fact stays inside.
   A family that binds in the prompt and then looks up an in-context table ("Alice lives in France. ... France's
   colour is red. What colour is the country where Alice lives?") separates a computed second step from the binding.
6. **Σ-aware writes** (exp06, exp07): writing along Σv lost to writing along v at the start line, and did no better
   than v at exp04's window. Dropped unless a human wants a Mahalanobis-matched version.
