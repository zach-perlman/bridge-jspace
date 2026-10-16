# bridge-jspace — one-pager (draft, 2026-10-16)

Dan Orel & Zach Perlman · Qwen3.6-27B · VERIFIED.md @ 8bc7a4f. **Verified** = in VERIFIED.md: a human recomputed it
from the raw files and read the examples. Everything else is marked *unverified*. Part B in more detail:
[ONEPAGER_partB.md](ONEPAGER_partB.md).

**TL;DR.** On Qwen3.6-27B, a bridge recalled from memory acts on the answer through its J-space part, as in Claude
(B1: J-part 52%, remainder with J held 1%). An intermediate looked up in the prompt does not: it acts along a
direction nearly orthogonal to the lens's, which the lens can read but not write; along the lens's direction the
model does not take the step, and at large size says the word instead (B2-B3). The lenses do find the
bridge, at the last word or at an earlier one (A2-A3), but neither their readings nor the verbalizers' show what the
model uses (B3-B4).

## Question
Gurnee et al. 2026: in Claude, the bridge entity of a two-hop question acts on the answer through the J-space (swap
the J-part 61%, the remainder 28%, the remainder with J held 6%). On open models the J-lens often fails to show the
bridge. Is the bridge acting outside the J-space there, or is the lens miss an artifact of how we read?

## What we checked and found (verified)
| | Experiment | Finding | Main limit |
|---|---|---|---|
| A1 | exp10, lens-eval, 63 q | At layers 32-48 the bridge is in the top 10: J++ 59% [46-70%], J-lens 30%, logit lens 3% | lenient (one layer is enough); no distractor |
| A2 | exp11, probe-swap, 77 q | At the last word the bridge is first among 97 entities at 57% [48-66%] of layers 32-48, its distractor at 5%; first from layer 35, the answer from 44 (9 layers later [3-16]) | "first" in a closed list |
| A3 | exp12, 30 last-word misses | 22/30 have the bridge first at an earlier word, all at a cue word; the distractor 10/30 (bridge +40 points [13-67]) | cannot tell a cue word's association from a computed bridge |
| A4 | exp14, cue phrase, 72 q | Swapping the bridge with the answer held changes the answer in 18% [11-28%]; the answer swap with the bridge held 1% (J++) / 6% (J-lens); random 0% | mostly place bridges (12/25 vs 1/41 other); the answer swap's positive control failed |
| B1 | exp02, 77 q | Swapping only the J-part of a recalled bridge's probe flips 52% [41-63%] (J++), the remainder 8%, the remainder with J held 1%, random ≤3% | places 88% and people 86% vs 25% for the rest; the gate failed its own rule |
| B2 | exp04, brew | A lens-free copy carries the step after the start line at layers 36-50 (up to 48-52%); its J-part 0%, the rest 26-28% | brew only; weak positive control (31%) |
| B3 | exp07/08, brew | A code fit on other items writes the step (34%); the lens direction at the same size does not (1%), though the lens reads the intermediate (61% at one position) | positions and read cell picked after the fact |
| B4 | exp18 v3, brew | A J++ direction the model ignores (step 4%) is named by both verbalizers on 99% of items; the code the model uses (57%) on 64-68% | edits at the read positions themselves |

## Key figures (verified claims)
![exp12: where in the prompt, and how deep, the bridge and the answer are readable](figures/exp12_position_map/two_step.png)
*A2-A3.* Left: where in the prompt each word is ranked first among its candidates (layers 32-48). The bridge (blue)
is readable over the last few words and its distractor (grey) nowhere; the answer (orange) mainly at the last word.
Right: the "19 layers later" compares two positions (the bridge at -1, the answer at the last word). At the same
position the lag is 9 layers (A2), and -1 reads no better than the last word (unverified).

![exp14: swaps on the cue phrase with the other pair held](figures/exp14_cue_answer_swaps/flip_rates_pinned.png)
*A4.* On the cue phrase (left group in each panel), the bridge swap with the answer held (dark blue, hatched) still
changes the answer; the answer swap with the bridge held (dark orange, hatched) hardly does; random directions 0%.

![exp02: J-space part vs remainder](figures/exp02_swaps/v4b/jpart_vs_remainder.png)
*B1.* Swapping only the J-space part of a recalled bridge's probe flips the answer; the remainder barely does, the
same shape as Claude's result (black, from the paper).

![exp18 v3: what the verbalizers name under each edit](figures/exp18_brew_verbalizers/v3/code_vs_lens.png)
*B4.* Brew: both verbalizers name X on about 99% of items under J++'s direction, which the model ignores (grey: it
takes the step on 4%), and less under the code it computes with (57%).

## Lead (unverified): what uses the bridge decides, not where it comes from (exp09)
Four families hold the question, the countries and the second hop fixed and change only where the bridge comes from
and what uses it. Each cell: the lens-free copy's J-space part vs the rest, or exp02's swap where the split is
inconclusive.

| | used by a recalled fact | used by a lookup in the prompt |
|---|---|---|
| **recalled bridge** | R: J-part swap 82% vs 3% (matched control) | RL: outside (J-part 0% vs rest 20%) |
| **bound in the prompt** | B: inside (12.5% vs 0%) | L: outside (0% vs 6%); brew (B2) |

Caveat: "used by a lookup" also means "the answer is read from the prompt"; B's "inside" rests on 12.5% of a copy
that gives 70%; R's own split is inconclusive (4% vs 7%). Recomputes from the raw files; not yet human-verified.

## What is still under question (unverified)
- **Association or computation (A3).** The lens often has the bridge first before the prompt determines it: "oxygen"
  at "...the gas" (only two gases among the 97 entities), "Napoleon" at "...whose army was led by", before
  "Waterloo". "First among 97" is easy on a vague word. To count: only positions from the word that determines the
  bridge, and with the vocabulary rank instead of the closed list.

  ![exp12: is the bridge, or already the answer, readable on the cue phrase](figures/exp12_position_map/cue_phrase.png)
  *Unverified.* On the cue phrase the J-lens has the bridge first about as often as at the last two words (56%), and
  from earlier layers (right, solid), while the answer stays low there (17%). At layers 0-4 (black ticks) the bridge is
  rarely first on the cue phrase, so it is not the words' raw embeddings; but a cue word can still pull the bridge up
  by association in the middle layers ("gas" → oxygen), and the cue spans were written by the coding agent.
- **Is the J-part just the bridge token's own direction (B1)?** The J-part is 17-20% of the probe's variance, and the
  bridge's own token is among its atoms for 37-53% of entities; the full lens-free probe flips only 27%, the raw lens
  vector 49%. "J-part ≫ remainder" may reduce to "the bridge token's lens vector is causal and the probe is weak".
- **Verbalizers on lens-blind cells** (oracle 37%, NLA 46%, distractor 4-10%): mostly where the lenses nearly have
  the bridge (median rank 4-5); the oracle's rates are lower bounds (64% of its texts are partly Chinese); one country
  template dominates; reading the state vs solving the question is open (exp17, designed, not run).
- **Verbalizers after a swap** (oracle names the swap target in 67% of the questions whose answer changes vs 10%):
  read downstream of the edit, the test B4 asks for, but this may only track how much of the edit reached the read
  position.
- **"-1 is the read site":** -1 reads no better than the last word (+7 points [-3, +17]); the split by how the prompt
  ends was found after the fact.

## What we can conclude so far
1. The lens miss is mostly where we read: the lenses find the bridge at the last word, far above its distractor
   (A2), or at an earlier word (A3). Whether what they find there is the computed bridge or the cue word's
   association is open.
2. For a bridge recalled from memory, Claude's result reproduces on Qwen: the J-part carries the swap and the rest
   barely does (B1), and the bridge acts from the cue phrase apart from the answer's direction (A4). Both effects
   sit mostly on places and people.
3. For an intermediate looked up in the prompt, the J-space account fails: the step is carried outside it (B2), and
   readable is not writable (B3): along the lens's direction the model does not take the step, and at large size it
   says the word instead.
4. Verbalizer readings, after an edit or on lens-blind cells, are not evidence of what the model uses (B4).

## Directions
| Stage | Direction | What it settles | Cost |
|---|---|---|---|
| Before the sprint (hygiene) | Re-score A3 from the determining word on, with vocabulary rank; human review of the 77 cue spans | association vs computed bridge | hours, no GPU |
| | B1 ablation: J-part minus the bridge's own-token atom; the atom alone; matched dose | whether "J-space" reduces to "the token direction" | GPU-hours |
| Sprint core: pick one with Neel | (a) Separate "use" from "answer source": a family where a lookup in the prompt uses the variable but the answer comes from memory | whether exp09's lead is about use or about where the answer is read | new items + GPU, days |
| | (b) Is the part outside the J-space a binding-ID-like pointer? Move exp07's code into a prompt whose table rows are permuted: a pointer follows the row, a colour code the colour | what the outside part is | new items + GPU, days |
| | (c) A stronger lens-free bridge direction (in-context contrast or DAS 1-d on held-out items), then re-decompose | whether the remainder matters once the reference is strong | ~1 day |
| Generality (after the core) | Verbalizers: exp17 (reading vs solving); downstream reads at matched edit size; Chinese-aware scoring; the rank > 10 subset with its distractor | whether verbalizers add anything the lenses cannot read | ~1 day + hours |
| | A second model with a working positive control (Gemma 4 31B: lens-free results replicate; its lens-based measures are not yet trustworthy), a second seed, categories beyond country templates, multi-token bridges, brew for part A | whether any of this is about Qwen and places only | days |

## Questions for Neel
- Which story to sharpen for the final presentation: (a) the lens miss is where we read, not absence (A1-A3); (b)
  recalled bridges act through the J-space as in Claude (B1, A4); (c) lookup variables live outside the J-space, and
  readers cannot tell used from written (B2-B4); or (d) what uses a variable decides whether it lives in the J-space
  (exp09, with sprint directions a-b)?
- Does "lookup variables live outside the J-space" sound new to you, or like binding IDs (Feng & Steinhardt 2023)
  seen through a lens?
- Is "first among a closed list of candidates" an acceptable reading measure, or should every reading claim use the
  vocabulary rank?
- Is a learned (DAS-style) bridge direction an acceptable lens-free reference, given the interpretability illusion
  for subspace patching (Makelov et al. 2023), or does it bias toward whatever subspace is easiest to steer?
