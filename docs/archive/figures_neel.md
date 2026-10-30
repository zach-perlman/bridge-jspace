# The breadth half in 12 figures (draft, 2026-10-26 night)

Figures: `F01-F12.png` and `all.pdf` in `/workspace/scratch/neel_figures/` on the box (copy on the VPS: `/home/zach/scratch/neel_figures/`), made by `scripts/fig_neel.py`; kept out of the repo. Every number is read
from result files; none is copied by hand. F10, and parts of F06 and F12, fill in when amendment 54 (running tonight)
lands.

## The question

**Proposal (10/19): which intermediates live in the J-space?**
- H0: the J-space carries recalled words, not computed variables.
- Neel thought H0 was probably false, and asked for diverse, non-toy settings and larger models.

**Zach's half (10/20): does the memory-vs-prompt split hold beyond our setup?** The test:
- Take a two-hop question whose bridge entity is reached from a passage (read, tracked) or from memory.
- Ask for an attribute of the bridge that is either **stated** in the passage (K) or **recalled** (M).
- Remove the 10 directions the J++ lens reads most, at every token, across one mid-depth band.
- Measure M − K: recall answers lost minus stated-fact answers lost.

## The story, figure by figure

| # | Question it answers | What it shows |
|---|---|---|
| F01 | What is the test? | jsuite_v2: one scene across its 5 finals (K, M, A, N, P) and 4 starts (P read, M recalled, T tracked, R never named); 8 relations, 179 test facts, 5,370 items; eligibility per model; the intervention and its 3 controls. |
| F02 | Is the attribute *there*? | At the bridge's mention, the J++ lens reads the attribute at the band in all 6 v2 models (mostly 70-95%; chance ~8%). The logit lens lags in the Qwens and Ministral. Readable everywhere: that alone says nothing about use. |
| F03 | Is it *needed*? | M − K under the top-10 removal: **+51 / +43 / +53** in Qwen 27B / 9B / Nemotron Lightning. Stated facts lose 3-5. Rotated ≤ 4, logit lens ≤ 9, size-matched 0.15-0.24 of the effect. The other 6 models are weak (DeepSeek, Ministral), spread (Bolt), not needed (OLMo), shared with the logit lens (Muse) or not robust (122B). B: losses order by where the answer is (K 3 < P < A < N < M 54). |
| F04 | Is it one dataset? | The two Qwens on every dataset since day 1: toy puzzles x3 seeds (27B 36/34/40), natural chains x3, natplus, jsuite v1 (+50/+42), v2. J-specific wherever the logit-lens arm ran. Other models fail there too, or their gap is shared with the logit lens (Muse) or not robust (122B). C: rare bridges lose as much or more (Neel's narrow-concept prediction not supported); about 4/5 of the 9B's effect is in its base model; the plain J-lens finds half the J++ effect. |
| F05 | Is it robust within v2? | All 8 relations (animals weakest), all starts, R (never named: extra loss in the 27B and 9B), test halves A/B, 3 renderings, by probability. Clean-checkout reruns: row-identical for both Qwens. |
| F06 | Where? | Depth profiles: a broad J-specific mid-depth region in the Qwens and Lightning; little at any depth in Ministral (late only) and Bolt (at K = 10). Positions: at mid depth the removal must hit the **bridge's own mention**; late, the **question**. This is a depth effect: the 27B shows both, Ministral and the 122B only the late one. |
| F07 | Does the mention's J-part *carry* it? | Swapping the mention's top-10 J-part for another entity's moves the answer to that entity's attribute: +63 / +64 / +45 (Qwens / Lightning), rotated and logit-lens swaps 0. Not Neel's answer swap: removing D's answer direction from the swapped J-part keeps 100% of it. OLMo: carried (+41) but not needed (+5). Bolt carries only with ~100 directions. Ministral: readable, not carried. |
| F08 | What does it carry? | A **pointer to the entity**: a J-part from one neutral sentence about D works as well as one from D's passage (1.01-1.10; 8/8 relations in the Qwens, 7/7 read in Lightning), and so does one from a passage on another relation (0.98-0.99). Beyond the name's own directions: Qwens 0.83-0.84, Lightning 0.62. A supervised probe decodes the attribute there as well as J++, but its subspace barely moves the answer (+2 to +8 vs +62 to +80). |
| F09 | When is the fact looked up? | At the answer position, the lens reads the attribute only after the band (Qwens: 7-10 layers later), for a swapped entity just as for the original. |
| F10 | How much J-space? | Dose K = 1-300 against removal size, with rotated, size-matched and logit-lens controls at every K; plateau and specificity limit pre-registered (amendment 54). **Running tonight.** |
| F11 | Beyond two hops? | Three hops (27B, v1): a memory hop is J-dependent when its output never appears in the prompt (MMM +35, PMM +33 vs MPP/PMP −3). Numbers: a recalled number needs J (9B +26, 27B +15), a counted or computed one does not (0-7). Under the knock-out the Qwens answer a lure or another valid answer, rarely the bridge: the entity is known, its attribute is not. |
| F12 | Where does every model stand? | Model x test scorecard: holds / weak / fails / untestable / not run. The gaps are the to-do list. |

## What we have shown

1. **Recall needs J-space; reading doesn't.** This holds in 3 models from 2 families (Qwen 3.5/3.6 hybrids, Nemotron
   Lightning). It is J-specific against 3 controls, robust within v2, and replicated across every dataset we built
   (Qwens).
2. **What J-space carries at the mention is the entity, as a context-free pointer.** It is not the recalled attribute,
   and not the answer token. The attribute is computed later, at the question.
3. **Generality is graded.**
   - Of 9 models testable on v2: 3 strong, 2 weak, 1 spread over about 100 directions, 1 carried but not needed, 1 not
     J-specific, 1 not robust.
   - 3 more models are untestable (any lens removal wrecks them): Gemma 4, gpt-oss, Kolibri.
   - 3 failed on the earlier datasets and were never run on v2: Qwen3-32B, Olmo-Hybrid 7B, Olmo-3 7B.
   - Removal size differs by model, so fixed-K comparisons mislead (F10).

## Have we answered the research question?

**Zach's breadth question: mostly yes, in a reframed form.** The split holds beyond our setup, across 5 datasets, 8
relations and 2 families. But not in every model, and what lives in J-space is "which entity", not "the recalled
fact".

**The proposal's H0 was never tested head-on on v2.**
- The old toy suite says computed bridges are carried in J (H0 false there).
- On v1, computed numbers don't need J to be reported.

## Gaps for days 9-12 (the · cells in F12)

1. **Amendment 54 tonight:** the dose plateau and matched-size comparison (F10); Lightning's position split and clean
   rerun; Bolt's position split.
2. **Lightning, the only non-Qwen strong model,** has v2 only:
   - no natural or natplus replication;
   - no R start;
   - no keep-own-word test;
   - its lens is our own fit (the Qwens use published ones).
3. **Pointer, probe and size-matched tests stop at 3-5 models.** Missing: Bolt (at K = 100), DeepSeek, OLMo.
4. **DeepSeek and OLMo** (the likeliest under-dosed) are out of the dose grid until their caches return.
5. **Three-hop and numbers on v2** (amendment 37B, never run), and **H0 head-on on v2** (computed bridges).
6. **No human verification yet** (`docs/breadth/verify_kit.md`).
