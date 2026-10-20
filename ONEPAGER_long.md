# Is the first hop outside the J-space? — one-pager

Dan Orel & Zach Perlman · Qwen3.6-27B · 2026-10-16 · **Verified** = a human recomputed it from the raw files and read
the examples ([VERIFIED.md](VERIFIED.md) @ 8bc7a4f); everything else is marked *unverified*. Part B in more detail:
[ONEPAGER_partB.md](ONEPAGER_partB.md).

## Question
Gurnee et al. (2026): in Claude, the bridge of a two-hop question ("The language spoken in the country where the
Amazon River ends is" → *Brazil* → *Portuguese*) acts on the answer through the J-space: swapping only the bridge's
J-space part flips 61% of answers, the remainder 28%, the remainder with the J-space held fixed 6%. On open models
the J-lens often fails to show the bridge. Is the bridge acting outside the J-space there, or is the miss an
artifact of how we read?

## TL;DR
1. **The lens miss is mostly where we read.** The lenses find the bridge at the last word, far above a distractor,
   or at an earlier word (A2-A3). Whether that is the computed bridge or a cue word's association is open.
2. **A bridge recalled from memory acts through the J-space, as in Claude.** Swapping its J-space part flips 52% of
   answers, the remainder with the J-space held 1% (B1); on the cue phrase it acts apart from the answer (A4).
3. **A variable looked up in the prompt does not.** In brew, an in-context two-step lookup, the step is carried
   outside the J-space (B2): the lens can locate it but not write it, while a code nearly orthogonal to the lens
   direction does (B3).
4. **Readers report what is written into the vector, not what the model uses.** Both verbalizers (oracle lens, NLA)
   name a direction the model ignores more often than the code it computes with (B4).

## Verified results
| | Claim | Result | Main limit |
|---|---|---|---|
| A1 | Lenses see the bridge in the middle layers (exp10, 63 q) | In the top 10 at any of layers 32-48: J++ 59% [46-70], J-lens 30%, logit lens 3% | lenient; no distractor |
| A2 | At the last word, before the answer (exp11, 77 q) | Bridge first among 97 entities at 57% [48-66] of layers 32-48, distractor 5%; half the questions by layer 35, the answer by 44 | closed candidate list |
| A3 | Last-word misses are found earlier (exp12, 30 misses) | 22/30 at an earlier word, all at a cue word; distractor 10/30 (+40 pts [13-67]) | association vs computation |
| A4 | On the cue phrase the bridge acts apart from the answer (exp14, 72 q) | Bridge swap, answer held: 18% [11-28]; answer swap, bridge held: 1% (J++) / 6% (J-lens); random 0% | mostly places; the answer swap's positive control failed |
| B1 | A recalled bridge acts through its J-part (exp02, 77 q) | J-part 52% [41-63]; remainder 8%; remainder with J held 1%; matched-alignment 14%; random ≤3% | mostly places and people; the gate failed its own rule |
| B2 | Brew's step is outside the J-space (exp04, 82 + 154 items) | A lens-free copy at layers 36-50 takes the step; its J-part 0%, the rest 26-28% | brew only; the copy is a weak positive control (31%) |
| B3 | Readable, not writable (exp07/08) | A code fit on 883 other items: 34%; lens direction at the same size: 1% (cosine 0.02); yet J++ ranks the intermediate first at one position for 61% (distractor 2%) | positions picked post hoc; code at ~2x its own size |
| B4 | Verbalizers cannot tell used from written (exp18 v3, 680 items) | J++ direction the model ignores (step 4%): named on 99%; code the model uses (step 57%): named on 64-68% | edits at the read positions |

<img src="figures/exp02_swaps/v4b/jpart_vs_remainder.png" width="49%"> <img src="figures/exp14_cue_answer_swaps/flip_rates_pinned.png" width="49%">
<img src="figures/exp18_brew_verbalizers/v3/code_vs_lens.png" width="49%"> <img src="figures/exp09_bind_recall/v2/source_use.png" width="49%">

- *Top left (B1):* the J-part carries the swap, the remainder barely does; Claude's numbers as the black dashed line.
- *Top right (A4):* on the cue phrase the bridge swap with the answer held (hatched blue) still flips; the answer swap
  with the bridge held (hatched orange) hardly does.
- *Bottom left (B4):* both verbalizers name X under J++'s direction, which the model ignores (grey: step taken),
  more often than under the code it computes with.
- *Bottom right (lead below, unverified):* where a lookup in the prompt uses the bridge (right column), the J-space
  part gives 0% and the rest acts. Where a recalled fact uses it (left), B's J-space part acts (12% vs 0%), but R's
  split is small both ways (4% vs 7%): R's "inside" rests on exp02's swap, not on this panel.

## Lead (unverified): what uses the variable decides, not where it comes from (exp09)
Same question form and countries; only the bridge's source and its user change. Each cell: J-part vs rest of the
lens-free copy (R: exp02's swap, since its split is inconclusive).

| | used by a recalled fact | used by a lookup in the prompt |
|---|---|---|
| **recalled bridge** | R: inside (J-part swap 82% vs matched 3%) | RL: outside (J-part 0% vs rest 20%) |
| **bound in the prompt** | B: inside (12.5% vs 0%) | L: outside (0% vs 6%); brew (B2) |

*Caveats:* "used by a lookup" also means "answer read from the prompt"; B's "inside" is 12.5% of a copy that gives 70%;
n = 65-80 per family.

## Open questions
- **Association or computation (A3)?** The lens often ranks the bridge first before the prompt determines it
  ("oxygen" at "...the gas"). Fix: count only from the determining word on, with the vocabulary rank.
- **Is the J-part just the bridge word's direction (B1)?** The bridge's own lens vector alone flips 49%, the full
  probe 27%. This would narrow "acts through the J-space" to "acts through its own word's direction", not refute it.
- **Use or answer source (exp09)?** In every family so far a lookup user also means the answer is read from the prompt.
- **Why mostly places and people (A4, B1)?** Either the lens is weaker outside them (its Jacobian is averaged over
  WikiText, rich in countries, cities, languages and people) or the model does not carry other bridges the same way.
- **How general is the reference result itself?** Claude's 61 / 28 / 6% rests on 90 two-hop prompts; our probe-swap
  set has the same 90 (77 answered by Qwen) over 36 categories, 29 "multihop" and the rest 1-6 prompts each. Neither
  their result nor ours supports a claim per category yet.
- **Do verbalizers see more than the lens?** Their lens-blind hits sit mostly where the lens has the bridge at rank
  4-5; reading vs solving on unedited states is untested (exp17).

## Directions
| Stage | Direction | Settles | Cost |
|---|---|---|---|
| Before the sprint | Re-score A3 from the determining word, vocabulary rank; human review of the 77 cue spans | association vs computation | hours, no GPU |
| | Split B1 by whether the bridge's own token is among the J-part atoms; then swap the J-part projected off the bridge word's direction (and near-synonym atoms) at matched size | one word direction or a distributed J-space | hours + GPU-hours |
| | Lens or model? Per category, compare the lens-free probe swap with the J-part swap (exp02). Only if lens-free works where the J-part fails: lens vectors from a held-out domain corpus (one vector-Jacobian product per word, not the full J) vs WikiText's, by cosine, then re-swap | whether a WikiText Jacobian limits the lens outside places and people | hours; GPU-hours if needed |
| Sprint core (pick one) | **(a)** Targeted families, as in exp09, not a broad set: a lookup in the prompt uses the variable but the answer comes from memory, and the reverse | use vs answer source; recalled vs computed from the prompt | days |
| | **(b)** Write exp07's code into a prompt with permuted table rows: a pointer follows the row, a colour code the colour | what the outside-J part is | days |
| | **(c)** A stronger lens-free bridge direction, then re-decompose: contrastive pairs (prompts that differ only in the bridge) or DAS (a direction trained so that swapping along it flips the answer) | whether the remainder matters with a strong reference | ~1 day |
| Generality | Gemma 4 31B (started): the lens-free results and exp09's 2×2 first; lens-based measures only after a sanity gate (now not trustworthy: empty J-parts, tiny edits break the model, likely a few very large activation dimensions) | whether this is about Qwen | days |
| | A balanced prompt set: ≥30 questions per category, each with a lens-free reference, recall and compute-from-the-prompt tasks in each; multi-token bridges; reuse WorkspaceBench / nocot-bench families before generating new ones | which tool wins or loses where; whether Claude's and our result hold beyond the 90 prompts and beyond places | days |
| | Verbalizers on unedited states (exp17); a second seed | whether verbalizers add anything the lenses cannot read | ~1 day |

## Questions for Neel
1. Which story should the sprint sharpen: recalled bridges act through the J-space as in Claude (B1, A4); lookup
   variables live outside it and readers cannot tell used from written (B2-B4); or what uses a variable decides
   where it lives (exp09, directions a-b)?
2. Does "lookup variables live outside the J-space" sound new, or like binding IDs (Feng & Steinhardt 2023) seen
   through a lens?
3. Our lens-free bridge probe is weak (the full probe flips only 27%), so B1 may look clean only against a weak
   reference. To build a stronger one, would you trust DAS (a direction trained so that swapping along it flips the
   answer), given that such a direction can work without being one the model uses (Makelov et al. 2023)? Or simple
   contrastive pairs (the mean activation difference between prompts that differ only in the bridge, e.g. Naples vs
   Madrid in the same template)?
