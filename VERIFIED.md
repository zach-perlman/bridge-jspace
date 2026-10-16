# VERIFIED

Results a human has checked (recomputed the headline from the raw files). Agents never edit this file.

## How to read this file

- *Bridge*: the hidden middle step of a two-hop question.
- *Answer*: what the model must say.
- *Distractor*: a wrong word of the same kind as the bridge, used as a control.
- *Cue word*: a word of the prompt that points to the bridge (e.g., "Lima" points to "Peru").
- *Last word*: the prompt's last token, where the model starts its answer.
- *Readers*: J-lens, J++, logit lens. Results for the J-lens come first; J++ has its own line.
- *Counts*: "19 of 63 (30%, 95% CI 20-42%)" means the bridge is seen in 19 of the 63 questions, which is 30%; the true rate likely lies between 20% and 42%.
- *Limits*: only what keeps a claim from being generalized.

Example: "The language spoken in the country where the Amazon River ends is": bridge "Brazil", distractor "Mexico", answer "Portuguese".

## A1. exp10: lenses vs logit lens at layers 32-48 (verified 2026-10-16, Danyil)

- **Claim**: At layers 32-48 J++ has the bridge among its 10 most likely words in about 6 of 10 questions, the J-lens in about 3 of 10, the logit lens almost never.
- **Setup**:
  - *Questions*: the 63 two-hop questions of the lens-eval set whose bridge is one word-token. Example: "The number of legs on the animal that spins webs is": bridge "spider".
  - *Read*: at the last word, at each of layers 32-48, each reader's 10 most likely words out of the whole vocabulary.
  - *Score*: the bridge is seen if it is among those 10 at any one of these layers.
  - *Control*: the logit lens as the baseline reader.
- **Result**:
  - *J-lens*: 19 of 63 (30%, 95% CI 20-42%).
  - *J++*: 37 of 63 (59%, 95% CI 46-70%).
  - *Logit lens*: 2 of 63 (3%, 95% CI 1-11%).
  - *44 of 63 the model answers correctly*: J-lens 12 of 44 (27%), J++ 26 of 44 (59%), logit lens 1 of 44 (2%). The same picture, so the result does not come from questions the model gets wrong.
- **Limits**:
  - *Model*: Qwen3.6-27B only, one run.
  - *Data*: 63 questions from one set (lens-eval multihop); other sets, including brew, not tested.
  - *Words*: single-token word bridges only; numbers, letters and multi-token bridges not tested.
  - *Control*: no distractor, so a lens that ranks every word of the bridge's kind high would also score well (A2 adds a distractor, on another set).
  - *Measure*: the bridge counts as seen even if it is in the top 10 at only one of the 17 layers.

## A2. exp11: bridge vs distractor and vs answer at the last word (verified 2026-10-16, Danyil)

- **Claim**: At the last word both lenses rank the bridge first far more often than the distractor, and at shallower layers than the answer.
- **Setup**:
  - *Questions*: the 77 two-hop questions of the probe-swap set that the model answers correctly (the example above is one of them).
  - *Read*: at the last word, at every layer. Each lens ranks the set's 97 entities (for the bridge and the distractor) and its 112 answers (for the answer).
  - *Score*: the share of layers 32-48 at which a word is ranked first, averaged over questions; and the first layer at which half of the questions have the word first.
  - *Control*: the distractor, ranked in the same list as the bridge.
- **Result**:
  - *Bridge vs distractor*: the J-lens ranks the bridge first at 57% of layers 32-48 (95% CI 48-66%), the distractor at 5%.
  - *Bridge vs answer*: half of the questions have the bridge first by layer 35, the answer by layer 44: 9 layers later (95% CI 3-16).
  - *J++*: bridge 56% vs distractor 5%; bridge by layer 36, answer by layer 43: 7 layers later (95% CI 4-21).
- **Limits**:
  - *Model*: Qwen3.6-27B only, one run.
  - *Data*: 77 questions from one set (probe-swap); other sets, including brew, not tested.
  - *Words*: single-token bridges only; the answer comparison uses only the 72 questions with a single-token answer; multi-token words not tested.
  - *Measure*: the bridge is ranked among 97 entities and the answer among 112 answers, so first place is not equally hard for both. "Earlier" holds for the questions as a group (the layer where half of them have the word first), not for each question.

## A3. exp12: where the last word misses the bridge, an earlier word shows it (verified 2026-10-16, Danyil)

- **Claim**: Most of the lens's misses at the last word come from where we read: the bridge is seen at an earlier word instead.
- **Setup**:
  - *Questions*: the 77 questions of A2.
  - *Read*: at every word of the prompt, at layers 32-48, ranking the set's 97 entities.
  - *Score*: the bridge is seen at a word if it is ranked first there at half or more of layers 32-48. Where the last word misses it, we search all earlier words.
  - *Control*: the same search for the distractor, since searching many words gives many chances to put something first by luck.
- **Result**:
  - *47 of 77*: seen at the last word. Distractor: 3 of 77.
  - *30 of 77*: not seen at the last word. Of these:
    - *22 of 30* (73%, 95% CI 56-86%): seen at an earlier word, often a cue word.
    - *8 of 30*: not seen at any word.
  - *69 of 77*: seen somewhere in the prompt.
  - *Bridge vs distractor*: the same search over earlier words finds the bridge in 22 of 30 (73%, 95% CI 56-86%) and the distractor in 10 of 30 (33%, 95% CI 19-51%); the ranges do not overlap.
  - *J++*: 46 of 77 at the last word (distractor 3). Of the other 31, the bridge is seen at an earlier word in 24 (77%, 95% CI 60-89%) and at none in 7; the distractor in 8 (26%, 95% CI 14-43%). 70 of 77 in all.
- **Limits**:
  - *Model*: Qwen3.6-27B only, one run.
  - *Data*: 77 questions from one set (probe-swap), the same as A2; other sets, including brew, not tested.
  - *Words*: single-token bridges only; multi-token bridges not tested.
  - *Control*: no word of the prompt points to the distractor, so the control does not rule out that at a cue word the lens reads that word's own association ("Lima" points to "Peru"), not a bridge the model has worked out.
  - *Measure*: one cut-off (first at half or more of layers 32-48); others not tested. Shows where the bridge can be read, not where the model uses it. "Often a cue word" comes from reading examples by hand and is not counted.
