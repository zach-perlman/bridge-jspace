# VERIFIED

Results a human has checked (recomputed the headline from the raw files). Agents never edit this file.

## A1. exp10: the J-lens and J++ read the bridge in the middle layers; the logit lens does not (verified 2026-10-16, Danyil)

- **Claim**: We took the 63 two-hop questions of the lens-eval set whose bridge is one word-token (e.g. "spider" in "the number of legs on the animal that spins webs is"). At the prompt's last word we asked each reader for its 10 most likely words at every layer from 32 to 48, and counted the bridge as found if it was among them at any of those layers. J++ found it in 37 of the 63 questions (59%; 95% CI 46-70%), the J-lens in 19 (30%; 20-42%), the logit lens in 2 (3%; 1-11%). The model answers 44 of the 63 correctly; counting only those 44 gives the same picture (59%, 27%, 2%), so the result does not come from questions the model gets wrong.
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run.
  - *Data*: 63 questions from one set (lens-eval multihop); other sets, including brew, not tested.
  - *Words*: single-token word bridges only; numbers, letters and multi-token bridges not covered.
  - *Control*: no same-category distractor in exp10 (A2 adds one, on another set).
  - *Measure*: lenient: the bridge counts as found if it is in the top 10 at any one of 17 layers.

## A2. exp11: at the last word the lenses find the bridge, and at shallower layers than the answer (verified 2026-10-16, Danyil)

- **Claim**: We took the 77 two-hop questions of the probe-swap set that Qwen3.6-27B answers correctly (e.g. "the language spoken in the country where the Amazon River ends is": bridge=Brazil, answer=Portuguese). At the prompt's last word we asked each lens, at every layer, which of the set's 97 entities it scores highest. Over layers 32 to 48 the J-lens puts the bridge first at 57% of layers (95% CI 48-66%) and its distractor (Mexico for Brazil) at 5%; J++ 56% vs 5%. The bridge also comes first earlier in depth than the answer: the first layer at which half of the questions have the bridge first is 35 (J-lens; J++ 36), for the answer (ranked among the set's 112 answers) it is 44 (J++ 43), about 9 layers later (95% CI 3-16; J++ 7, 4-21).
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run.
  - *Data*: 77 questions from one set (probe-swap); the answer comparison on the 72 with a single-token answer; brew not tested.
  - *Words*: single-token bridges only.
  - *Control*: same-category distractor included.
  - *Measure*: ranks are within each list (bridge among 97 entities, answer among 112 answers), so both can be first at once; "earlier" compares the first layer at which half of the questions have each word first.
