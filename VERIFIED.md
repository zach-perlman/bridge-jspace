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

## B1. exp02: swapping only the J-space part of a recalled bridge's probe flips the answer; the remainder barely does (verified 2026-10-16, Zach)

- **Claim**: We took the 77 two-hop questions of the probe-swap set that Qwen3.6-27B answers correctly (e.g. "The
  capital of the country where Munich is located is": bridge Germany, answer Berlin). At layers 24-40 and every
  prompt position we swapped the bridge's probe (mean activation difference for the entity) with another entity's
  (Japan) and counted a flip when the greedy continuation gave the other entity's answer (Tokyo) and not the
  original. Swapping only the probe's J-space part flips 52% of answers with J++ (95% CI 41-63%) and 35% with the
  J-lens (25-46%); the remainder 8% and 12%; the remainder with the J-space part held fixed 1% and 4%; random
  directions of the same size at most 3%. J-part minus remainder on the same questions: +44 points (+32 to +56)
  with J++, +23 (+12 to +35) with the J-lens. A control direction with the same cosine to the probe as the J-space
  part but otherwise random flips 14% (J++) and 10% (J-lens), although its edits are about three times larger
  (J-part minus it: +38 [+27, +48] and +25 [+16, +35]).
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run, one seed. (On Gemma 4 31B-it this experiment's gate and positive control
    fail; unverified, not committed.)
  - *Data*: 77 questions from one set (probe-swap); the band 24-40 was picked by a gate run that failed its own
    rule (full probe 27% < 30%), and main was run anyway by the human's choice.
  - *Words*: bridges with an exp01 probe; places and people flip far more often than other bridges (J++ 88% and
    86% vs 25%).
  - *Control*: matched-size random-direction nulls per layer, and the matched-alignment control. Collateral: the
    J++ J-part swap leaves neither answer for 9% of questions; the full probe's random null for 10%.
  - *Measure*: flips judged on an 8-token greedy continuation (criterion C). The swap acts mainly at the cue
    phrase, not at the last word (README position runs; not recomputed by the script).

## B2. exp04: without a lens, brew's step is carried after the start line at layers 36-50, outside the J-space (verified 2026-10-16, Zach)

- **Claim**: Brew prompts give a colour table and a start colour; the answer is two lookups away (blue -> green ->
  black). We copied the activations of a counterfactual prompt, whose start leads to another intermediate X, into
  the original run, one layer at a time, at the positions after the start line, with no lens involved. From layer
  36 to 50 the copy makes the model answer f(X), the second lookup applied to X in the original table: up to 48%
  [37-58%] of the 82 bank items (layers 46-50) and 52% [44-60%] of 154 fresh items (layer 48); from layer 52 it
  carries the counterfactual's answer instead (68-71%). A copy from a prompt whose changes are off the path changes
  at most 2% (bank) and 6% (fresh) of answers. At that window, the part of the copy inside the J-space (a 25-atom
  decomposition over J++'s token vectors) gives f(X) at 0% of window layers and the rest 26% (bank; +26 points
  [+20, +32]) and 28% (fresh; +28 [+24, +33]); the whole copy 31%. The copy's projection on the two colours' lens
  vectors also gives 0%, the rest 31%. Random directions of the same size give 0%. The J-lens gives the same
  picture (0% vs 24% and 26%).
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run, one seed for the counterfactual and control colours.
  - *Data*: brew only: 82 of WorkspaceBench's 100 bank items and 154 of 200 fresh items in the same format; the
    window was found on the same items it was tested on (the fresh map found the same window independently).
  - *Words*: single-token colour words from a 12-colour palette.
  - *Control*: the off-path copy, and a random direction of the same size for every part; the J-space part holds
    about the variance a random direction would (8% vs 7%), so it is a small part of the copy.
  - *Measure*: single-layer copies of about 21 positions; the best single-layer copy reaches about half of items,
    so the 31% full-copy step score is a weak positive control. At layers 36-46, 20-43% of copies instead make the
    model stop after one lookup (it answers the intermediate), which no decision rule counts.

## B3. exp07/exp08: on brew, the lens reads the intermediate but writing along its direction does not take the step; a code fit on other items does (verified 2026-10-16, Zach)

- **Claim**: In brew (start gold -> intermediate brown -> answer blue), we take Qwen3.6-27B's 154 fresh items (82
  bank items as replication) and edit at layers 36-50, at the 21 positions after the start line, where B2's
  lens-free copy moves the intermediate. Changing the intermediate from I to X along a code fit on 883 other brew
  items makes the model answer f(X) at 34% of window layers (the copy itself 31%, a random direction 0%); writing
  along J++'s direction v_X - v_I at the same size gives 1% (paired difference +33 [+28, +38] points; the J-lens
  alike). The code is nearly orthogonal to the lens direction (median cosine 0.02). Yet the lens reads I there: at
  layer 36, at the newline after "assistant", J++ ranks I first among the 12 palette colours for 61% [53, 68] of
  items, the distractor X for 2% (J-lens 47%). Copying the counterfactual only at the 4 positions where the lens
  reads I gives the full step (33%); the other 17 positions give 0%. The bank items replicate (code 25%, copy 31%,
  lens 1%; J++ reads I for 55%).
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run, one code fit (ridge 1.0).
  - *Data*: one synthetic task (brew), 154 fresh and 82 bank items. The 4 positions and the best read cell were
    chosen after the fact; the same search over 168 cells finds X first for at most 15%.
  - *Words*: the 12 palette colours, all single tokens. Reads are top-1 among those 12, not among the vocabulary
    (the median vocabulary rank of I is about 9,600 for J++).
  - *Control*: a random direction at the same size; the off-path copy at the same positions; the distractor X for
    reads; the answer at layer 62 as the readers' positive control. Σ-shaped lens directions also give 1%.
  - *Measure*: writing is the share of 8 window layers, one layer edited at a time, at which the continuation's
    first palette colour is f(X); edits at the copy's size (the code is about twice its own norm; at its own size it
    gives 4%). The copy's 31% is a weak ceiling (it also makes the model stop at I for 29%).

## B4. exp18 v3: on brew, the NLA and the oracle lens report the colour written into the vector, whether or not the model uses it (verified 2026-10-16, Zach)

- **Claim**: On 680 brew items Qwen3.6-27B answers correctly (e.g. start red -> intermediate brown -> answer pink;
  swap target X gold, whose rule gives f(X) blue), we add one of three edits after the start line at layers 36-40,
  each at the size of the lens-free copy: exp07's code for "the intermediate is X instead of I", which the model
  computes with (it answers f(X) for 57% of items, 390/680; 95% CI 54-61%); J++'s direction v_X - v_I, which the
  model ignores (4%, 28/680; it loses the clean answer for 24%); and a random direction (0.6%). On the 390 items
  where the code took, the NLA (layer 42) names X for 68% under the code and 99% under J++'s direction (as written:
  29%); the oracle lens (layer 44) 64% and 99% (as written: 24%). [names X] - [names I] is lower under the code than
  under J++'s direction by 29 points for the NLA (paired bootstrap 95% CI 24-34) and 36 for the oracle (31-41).
  Where the code did not make the model take the step (a seeded sample of 100) they still name X for 60% and 61%
  (as written: 14%, 15%). Neither names the edited model's answer f(X) more under the code than under J++'s
  direction (NLA 9% vs 12%).
- **Limits** (what the claim does not yet cover):
  - *Model*: Qwen3.6-27B only, one run, greedy decoding.
  - *Data*: brew only (84 bank, 155 fresh, 441 held-out test items); X is a colour already written in the table.
  - *Words*: English colour words matched as whole words (plural allowed); Chinese colour names, which the oracle
    often writes, are not counted.
  - *Control*: a random direction at the same size (+0 to +1 points over the clean prompt); each reader compared
    with its own clean reading, since the readers recite the table's colours.
  - *Measure*: the edits are at the read positions themselves, and J++'s direction is a large direct push along X's
    token direction there. So this shows the readers cannot tell a direction the model uses from one it ignores,
    not that they never read the computed state; a read downstream of edits made elsewhere would test that. A
    colour counts as named if either of the two read positions names it.
    Where X is gray, some namings are the binary sense ('gray code': 38 of the NLA's 956 namings under J++'s
    direction); they are counted, as the token written into the vector.
