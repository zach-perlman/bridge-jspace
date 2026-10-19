# Part B one-pager

**Question.** When a model computes an intermediate variable (a two-hop bridge, a step of an in-context lookup), does that variable act on the answer through the J-space, the part of the residual stream the J-lens reads? Or through a part the lens cannot write? Qwen3.6-27B, J-lens and J++, lens-free activation patching as ground truth.

**TL;DR.** It depends on the type of variable. A "recalled" bridge ("the country where Naples is" -> Italy) acts through its J-space part, similar to what we saw in the first Anthropic J-space paper. On the other hand, a variable the model computes and uses inside the prompt (e.g., brew's intermediate colour) is carried outside the J-space: the lens can locate it, at the right positions, but writing along the lens's direction does not take the step, while a direction fit on other items writes it. The verbalizers (oracle lens, NLA) share the blind spot: they report the colour written into the vector, whether or not the model actually uses it.

## Results

0. **The model does the tasks, in its chat format** (exp20, *unverified*; every item, unedited, greedy). In the chat template it answers exp09's four families on 99.7-100% of items and each of their steps alone on 100%, brew's steps 100% alone and 87-89% composed (ungated items), and B1's 90 questions 86%. In the raw text B1 and exp09 ran on, it is less sure (median probability of the answer .20-.64 vs .97-.99 in chat), and it answers exp09's R for 76% of items, with half failing exp09's gate: the misses are the model starting its own thinking turn or writing a multiple-choice list, not wrong capitals. Every result below is read against this: the task's base rate, how many items its gate keeps, and the format.

1. **Recalled bridges act through the J-space** (exp02, n=77) [B1]. Swapping only the J++ part of the bridge's probe (Italy -> Spain) flips the answer to Madrid for 52% [41, 63] of questions; the remainder 8%, the remainder with the J-space held 1%; a direction with the same alignment to the probe but random otherwise 14%; random nulls <= 3%. Claude: 61 / 28 / 6%. The swap acts at the cue phrase ("Naples": 31%), not where the lens reads the bridge best (one word before the end: 9%).

2. **Brew's step is carried outside the J-space** (exp03, exp04; 82 bank + 154 fresh items) [B2]. Brew is an in-context two-step lookup (blue -> green -> black from a colour table). Writing along the intermediate's lens direction, at the size of the lens-free copy, takes the step for 1% of window layers and leaves the original answer for 93% (exp07). Lens-free patching from a counterfactual table finds the step after the start line at layers 36-50 (best single layer 48-52%). If we split at that window, we observe that the J-space part of the copy gives the step 0%, the rest 28% (J++; J-lens 26%), the I/X lens coordinates 0%; nulls 0%. Replicates on held-out items.

3. **The lens reads the step where it is used, but cannot write it** (exp07, exp08, exp04 positions) [B3]. A linear code for the intermediate, fit on 883 other items, writes the step at the copy's size for 34% of window layers. The lens direction v_X - v_I at the same size is just 1%, with random at 0% (cosine code vs lens direction 0.02). Yet J++ ranks the intermediate first among the 12 colours at the newline after "assistant", layer 36, for 61% of items (distractor 2%), and copying only the 4 positions where the lens reads it gives the whole step (33% vs the other 17: 0%).

4. **Verbalizers report what is written, not what is used** (exp18 v3, Qwen) [B4]. Along a J++ direction the model usually ignores (i.e., takes the step for 4% of items) both verbalizers name the written colour 99% of the time; along the code the model uses (57%) they name it for 64-68%, and as often where the code did not change the step.

**Where the line falls (weaker, exploratory).** Holding the question's form fixed (exp09), a bridge used by a recalled fact sits inside the J-space and one used by a lookup in the prompt sits outside, whether it was recalled or bound in the prompt. The effects are small (e.g. 12.5% vs 0%), n=80 per family, and "lookup" also means "answer read from the prompt". The families ran on raw text, where R's items are the half the model answers (exp20); in the chat format it answers every item of every family. On Gemma 4 31B-it (unverified) the lens-free results replicate with a stronger positive control (the copy takes brew's step for 56-71% of items, a fitted code for 46-51%), but the lens-based measures there are not yet trustworthy (the J-space parts come out empty and tiny lens edits break the model, likely because of a few very large activation dimensions), so the boundary is untested on Gemma.

5. *Unverified, 2026-10-19 (README).* **B1's J-space part is the entities' own word directions** (Phase 2c): removed
   (and held), the J-part flips 0-1% instead of 52-54%, below a matched random control (14%), in raw text and in chat.
   **B1 replicates in the chat format** (J-part 54%, remainder 5%, held 3%) once the probes are read in the user turn.
   **A second J++ fit gives the same verdicts** (Phase 1; B1's J-part 42% vs 52%). **Contrastive directions built on
   B's own question move the bound bridge** (10%) through the part outside the J-space (11%; J-part 0%), while
   exp09's copy split puts B inside at a later position. **"What uses the bridge" vs "where the answer comes from"
   (Phase 3): neither** - no family with a lookup in the prompt comes out inside. On brew's composition misses the
   intermediate is mostly formed (78% vs 82% of hits).

## What it means
- For recalled entities, J-lens directions are causal levers on open models, nearly as on Claude.
- For variables computed and consumed in context, the lens is a *locator* (which positions) but not a lever for the step: at matched size its direction does nothing, and at large size it makes the model say X rather than use X. It is a lever for the output word, as expected of a Jacobian to the output logits; the direction the model computes with is nearly orthogonal to it. "The lens reads X here" does not necessarily mean "editing X's lens direction tests whether X is used".
- Verbalizer readings after an edit show what was written into the vector, not what the model actually uses for computing answers.

## What we do not know
- Whether the results hold in the format the model takes as a question: B1 and exp09 ran on raw text (exp20); brew ran in the chat template.
- Why the in-context variable sits outside: which consumer (e.g. attention lookups) reads the code, and what it is.
- How general it is beyond brew and the exp09 families; one model verified, one seed, single-token colours/entities.
- Effect sizes are modest: the best single-layer lens-free copy takes brew's step for about half the items, the window average is 31%.

## Questions
1. Which extension has the most upside: coverage across many in-context tasks, the mechanism of the non-J code, or verbalizer faithfulness on unedited states?
2. Open-model swap gap (Claude 61%, Qwen J++ 52%, Gemma 4%): lens fit or model? How much to trust our own J++ fit?
