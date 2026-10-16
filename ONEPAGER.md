# bridge-jspace — one-pager (draft, 2026-10-16)

Dan Orel & Zach Perlman · Qwen3.6-27B · VERIFIED.md @ 8bc7a4f. **Verified** = in VERIFIED.md: a human recomputed it
from the raw files and read the examples. Everything else is marked *unverified*.

## Question
Gurnee et al. 2026: in Claude, the bridge entity of a two-hop question acts on the answer through the J-space (swap
the J-part 61%, the remainder 28%, the remainder with J held 6%). On open models the J-lens often fails to show the
bridge. Is the bridge acting outside the J-space there, or is the lens miss an artifact of how we read?

## Short answer so far (one model, one run, single-token bridges)
The lens miss is mostly how we read: the lenses do see the bridge, at the last word or at an earlier word. A bridge
recalled from memory acts on the answer through its J-space part, as in Claude, mostly for places and people. An
intermediate looked up in the prompt (brew) is carried outside the J-space: the lens reads it, but writing along the
lens's direction does nothing. Verbalizers (oracle lens, NLA) cannot tell a direction the model uses from one it
ignores, so their readings are not evidence of use.

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

## What is still under question (unverified)
- **Association or computation (A3).** The lens often has the bridge first before the prompt determines it: "oxygen"
  at "...the gas" (only two gases among the 97 entities), "Napoleon" at "...whose army was led by", before
  "Waterloo". "First among 97" is easy on a vague word. To count: only positions from the word that determines the
  bridge, and with the vocabulary rank instead of the closed list.
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
- **What uses the bridge, not where it comes from (exp09):** across four families, a bridge used by a recalled fact
  acts through its J-part, and one used by a lookup in the prompt, recalled or bound, through the rest. Recomputes;
  not yet human-verified.

## What we can conclude so far
1. "The J-lens cannot see the bridge" on Qwen is not evidence that the bridge lives outside the J-space: at the last
   word the lenses rank it first far above the distractor (A2), and most misses are found at earlier words (A3).
   What they read there may be the cue word's association rather than a computed bridge.
2. For a bridge recalled from memory, Claude's result reproduces on Qwen: the J-part carries the swap and the rest
   barely does (B1), and the bridge acts from the cue phrase apart from the answer's direction (A4). Both effects
   sit mostly on places and people.
3. For an intermediate looked up in the prompt, the J-space account fails: the step is carried outside it (B2), and
   readable is not writable (B3).
4. Verbalizer readings, after an edit or on lens-blind cells, are not evidence of what the model uses (B4).

## Directions that would strengthen this
| # | Direction | What it settles | Cost |
|---|---|---|---|
| 1 | Re-score A3 from the determining word on, with vocabulary rank; human review of the 77 cue spans | association vs computed bridge | hours, no GPU |
| 2 | B1 ablation: J-part minus the bridge's own-token atom; the atom alone; matched dose | whether "J-space" reduces to "the token direction" | GPU-hours |
| 3 | A stronger lens-free bridge direction (in-context contrast or DAS 1-d on held-out items), then re-decompose | whether the remainder matters once the reference is strong | ~1 day |
| 4 | Verbalizers: exp17 (two-hop patch, reading vs solving); downstream reads at matched edit size; Chinese-aware scoring; rank > 10 subset with its distractor | whether verbalizers add anything the lenses cannot read | ~1 day + hours |
| 5 | Generality: a second model with a working positive control (Gemma 4 31B fails the gate), a second seed, categories balanced beyond country templates, multi-token bridges, brew for part A | whether any of this is about Qwen and places only | days |

## Questions for Neel
- Which story to sharpen for the final presentation: (a) the lens miss is reading, not absence (A1-A3, with
  direction 1); (b) recalled bridges act through the J-space as in Claude (B1, A4, with directions 2-3); or (c) lookup
  variables live outside the J-space, and verbalizers cannot tell used from written (B2-B4)?
- Is "first among a closed list of candidates" an acceptable reading measure, or should every reading claim use the
  vocabulary rank?
- Is a learned (DAS-style) bridge direction an acceptable lens-free reference, or does it bias toward whatever
  subspace is easiest to steer?
