# VERIFIED

Results a human has checked (recomputed the headline from the raw files). Agents never edit this file.

## A1. exp10: the J-lens and J++ read the bridge in the middle layers; the logit lens does not (verified 2026-10-16, Danyil)

- **Claim**: We took the 63 two-hop questions of the lens-eval set whose bridge is one word-token (e.g. "spider" in "the number of legs on the animal that spins webs is"). At the prompt's last word we asked each reader for its 10 most likely words at every layer from 32 to 48, and counted the bridge as found if it was among them at any of those layers. J++ found it in 37 of the 63 questions (59%; 95% CI 46-70%), the J-lens in 19 (30%; 20-42%), the logit lens in 2 (3%; 1-11%). The model answers 44 of the 63 correctly; counting only those 44 gives the same picture (59%, 27%, 2%), so the result does not come from questions the model gets wrong.
- **Limits**: one model; 63 questions from one set (lens-eval multihop), single-token word bridges; no distractor control here (see A2). To check on other sets, including brew.


## A2. exp11: at the last word the lenses pick out the bridge, and do so layers before the answer (verified 2026-10-16, Danyil)

- **Claim**: We took the 77 two-hop questions of the probe-swap set that Qwen3.6-27B answers correctly (e.g. "the language spoken in the country where the Amazon River ends is": bridge Brazil, answer Portuguese). At the prompt's last word we asked each lens, at every layer, which of the 97 entities of the set it scores highest (all the set's bridges and their same-category distractors). Over layers 32 to 48 the J-lens puts the bridge first at 57% of layers (95% CI 48-66%) and its distractor (Mexico for Brazil) at 5%; J++ 56% vs 5%. Doing the same for the answer among the set's 112 answers: in half of the questions the bridge is first from layer 35 (J-lens; 36 for J++), the answer only from layer 44 (43 for J++). So at the same position the answer comes about 9 layers after the bridge (95% CI 3-16; J++ 7, 4-21).
- **Limits**: one model, single-token bridges (answer: 72 questions). Ranks are within each list, so bridge and answer can both be first; the claim compares when half the questions have each word first.
