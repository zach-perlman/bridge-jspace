# How a lookup goes around the J-space

Dan Orel (depth track; Zach Perlman: breadth) · 8 open models · 23 Oct 2026 · exploration phase: no claim below is hand-verified yet; claims 1-3 and the 27B part of claim 4 were recomputed from raw rows by an independent agent (every cell matched). Numbers: the cross-model grid `results/cross_model/20261023T105852Z` and the runs named in [README.md](README.md).

## Question

A two-step question makes a model find a **bridge** entity, then use it: "Which locker belongs to the animal known for oinking?" → *pig* → the pig's locker number, stated in the prompt (a **lookup**). Asked "How many legs does it have?", the answer comes from memory instead (a **recall**). In Claude the bridge acts through the J-space, the part of the hidden state a J-lens reads as words (Gurnee et al. 2026). On open models: does the lookup use the bridge in the form the lens reads, or another route?

Models: Qwen3.6-27B, Qwen3.5-9B, Olmo-Hybrid-7B, Qwen3.5-122B (attention + DeltaNet hybrids); Qwen3-32B, OLMo-3-7B, Muse 30B, Gemma 4 31B (attention only). Lenses: J++ throughout (published, Zach's, and our own fits for Qwen3-32B and OLMo-3).

## What we found

**How a lookup works (lens-free; the strongest part).**

1. **The lookup ends with a late attention read of the answer's sentence by the tokens after the question.** Blocking it leaves 0-7% right on 7 of 8 models (27B 7% of 300, chance 20%), while blocking another sentence keeps 89-100% and, on the hybrids, blocking the same sentence in the DeltaNet layers instead keeps 88-100%. Gemma (22%) and the 27B with ~2000 tokens of filler (26%) look like a relay through other tokens: on Gemma, blocking every token after the sentence leaves 2%.
2. **Those tokens take the answer's digit; the question's tokens take the entity's name** (a lookback: address and payload). With only the name visible, 0-11% right on 7 models (27B 10% of 300); with only the digit visible, 88% on the 27B.
3. **Which sentence they read: an order label for the 1st and 2nd item, the bridge's identity after.** By a rule fixed in advance, on 7 of 8 models over three fresh scene sets and lists of 8 and 12 (27B, third scene set: position leads by +95.5 points for items 1-2, identity by +14.5 from item 3 on). Unlike Mixing Mechanisms (Gur-Arieh et al. 2026), no position peak at the last item.

**What the J-space does and does not carry.**

4. **The lens-readable part of a stated bridge moves recall, not the lookup.** Paste back only the part of a bridge change that lies in the J-space: on the 27B it moves 38% of recalls and 1% of lookups (n=180), the rest of the change 81% of lookups; on the 9B, 56% and 1%. A random part of the same size moves 0-1% of lookups and 0-8% of recalls on every model: the claim is the lookup/recall contrast, not that the lens part is special for lookups.
5. **A lens push at the bridge writes recall, and the lookup ignores it from a model's own layer on:** layer 20 on the 27B (at the sentence, layer 24: recalls 84%, lookups 0%), layer 6 on the 9B and OLMo-3, layer 33 on the 122B (recalls 89%, lookups 0%). Before that the 122B's lookup does follow it (26% at layer 27).
6. **The band (main J-space claim, being tested today):** at the stated bridge's word there are layers where the lookup still depends on that position (the full patch moves it: 27B 65% at layer 20) but not on its J-space form (the lens push moves none), while the push still writes recall. Valid cells only: 27B layers 20-26, OLMo-3 6-14, 9B 6-16 (weak: only small pushes are valid there), 122B layer 33.
7. **Lookups don't need the J-space; recall needs it to a varying degree** (Zach's knock-out, quoted from his runs): recall loses 36, 38, 22 and 7 points more than the lookup on the 27B, 9B, 32B and Muse.

Methods note: the lens names a stated bridge at its own word on 7 of 7 lensed models (27B 95%) and right after it on none (27B 7%): the "lens-readable part" is the word's form at its position.

![Every claim on every model](figures/cross_model/f_summary_heatmap.png)

## The 122B difference

On Qwen3.5-122B the lookup follows the bridge's J-space form through layer 30: the lens-readable part moves 29% of lookups at layer 24 (recalls 38%) and the lens push 18-26% at layers 27-30; at layer 33 the push moves none. Read as a later band, not a counter-example. Caveats: FP8 weights with a lens fit on bf16, mixture of experts. The late-switch test (layers 30, 33, 36, rule fixed before the run) runs today on a rented 2x H100.

## Limits

- Generated scenes: short lists, one-digit answers; tables, JSON and ~2000 tokens of filler so far. A natural-text version (SQuAD paragraphs) is approved and queued.
- The full patch is not size-matched to the lens push, and in the 27B's band only the smaller push is valid at the word: "the push stops" may be dose. Size-matched patches (with and without their J-space part) and the rest at the lens part's size are running today, predictions committed.
- Claims 4-6 rest on the Qwen hybrids and OLMo-3; Gemma's lens tests are running; Qwen3-32B's recall control fails; Muse answers too few scenes.
- One scene set for most lens results; the per-layer pushes and the maps use different scene sets except on the 27B.

## Next

Today: size-matched patches on 4 models; the rest at the lens part's size; the relay floor; the 122B late switch; natural text. Then a hand check with Zach, one natural setting with him (Mon-Tue), write-up and slides (Wed-Fri, 30 Oct).

## Questions

1. Is the band (claim 6) a strong enough main result, or should next week go to natural settings?
2. The 122B: report it as a real difference, or spend compute ruling out FP8 and the mixture of experts?
3. Which natural setting would convince you most?
