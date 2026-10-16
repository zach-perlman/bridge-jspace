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
