# Experiments ledger (depth)

Every opened test, so nothing is lost (Dan, 29 Oct ~01:10), written to be read without the runs, like the README's Part I (Dan, 01:15). Internal doc: test ids in the card headings only. Sections by status; inside each, the story's order (two readers → identity → address → where and when → other datasets). Each card follows the README's template: Question, Why we asked, Data, Method, Rule fixed in advance (quoted), one figure, Result (one column per model, 95% intervals, every number with its source), Read, Caveats. No interpretation beyond the verdict. Opened times are the opening commit's time (Paris, 28 Oct unless stated); box times are UTC. Every result here is UNVERIFIED until a human adds it to VERIFIED.md (said once, here). `uv run python scripts/check_ledger.py` checks every cited path, anchor, field and the coverage table (tests/test_experiments_ledger.py).

Restructure in progress (Dan 01:15): the coverage table and the order are in; the entries below move to the card template next, then their figures.

## Flagged for Dan

1. Lightning's gate (○ gate chosen after the 60-scene pre-check was seen): the main test's gate on all 516 scenes decides; the 60-scene pre-check had failed (lookup 0.883, recall 0.783) before the choice. Accepted by Dan 01:10; layer L14 stands. See [Lightning's layer](#lightning-layer).
2. Lightning's `layer.json` "rule" field (and prereq.md's "Pick rule" line) holds the prerequisite rule text, not the amendment-1 pick rule; the pick itself follows amendment 1 (earliest passing layer at relative depth >= 0.25): prereq.md lists the candidates at depth >= 0.25 and marks L14 as the pick.
3. 51.11's wording: no row of Dan's wording table matches the labels (9B: in between / in between / none of the three; Muse: one per slot / in between / none of the three; 27B: part 2 in between only). The README claim waits for Dan. See [51.11](#t51-11).
4. Z1 is not the made-up-fact rerun: Z1 ran Zach's K passages, which state true facts; the P-item reruns were never specced or run. See [Z1](#z1).
5. Bolt is out of scope: only a J-lens exists, no J++ lens (batch 52 amendment 2); the Bolt row in docs/digest.md is a J-lens result and is not cited on the depth side.
6. The varied-scene count for Muse: Fig. 9a's per-format n sum to 1389, docs/x0_numbers.json's `x0b_n_muse` says 1,388 (not traced).

## README changes waiting for Dan

Overnight rule (Dan 01:10): no README edits until Dan returns. One line each:

- "In one minute" and claim 8: "one code per locker" is not what 51.11 supports on the 9B (d* 2/2/>7/2, in between; the methods agree only in part; midpoint swaps fail); reword and regrade claim 8 ([51.11](#t51-11)).
- Status line: 51.11 is opened, not sealed; add Lightning's layer L14 and its rule (amendment 1, Dan ~00:50: earliest passing layer at relative depth >= 0.25; tie-break the bridge word's lens readability) ([Lightning's layer](#lightning-layer)).
- Part V: replace "reruns with made-up-fact passages are queued" by the truth: Z1 ran the true-fact K passages; no P-item rerun was specced or run ([Z1](#z1)).
- New card, Part IV next to the address at the last token: the recall's entity at the last token is readable but not used, all three models; figure figures/story/fig17_jspace_last_token.png ([51.10](#t51-10)).
- Claim 1: add the full-carrier limit (fact-after lookups follow the lens, 0.51 on the 9B and 27B) ([51.7](#t51-7)).
- Claim 12: add the last-token result (the address is not at the last token on the 9B and 27B; it travels on Muse) ([51.4](#t51-4)).

## Coverage

Which test ran on which model, from the committed coverage matrix (results/x52_coverage/matrix-20261029T000836Z/matrix.json, built 00:08 UTC 29 Oct; each cell's source is in that file). A linked test has a card below. Status words are the matrix's: done / partial / running / queued / missing / not tested (reason) / not designed. Lightning's gate (all cells): the main test's gate on all 516 scenes, ○ chosen after the 60-scene pre-check was seen; layer L14 (see [Lightning's layer](#lightning-layer)). Nemotron 3.5 Bolt: out of scope, only a J-lens exists, no J++ lens.

<!-- coverage:start (scripts/ledger_coverage.py; do not edit by hand) -->
| test | 27B | Lightning | 9B | Muse |
|---|---|---|---|---|
| 1. Conflict test (main test, at L) | **done**: not confirmed (lookup 0.14 > 0.10; recall 0.74) | **queued**: x52_lightning_conflict, speedup first: 3 arms at all 13 swept layers, decided at L14 | **done**: confirmed | **done**: confirmed |
| [2. Answer control (51.12 E1)](#t51-12) | **done**: recall: the entity | **missing**: Lightning chain, spec in Dan's order (reads the committed L14) | **done**: recall: the entity | **done**: answer word not read |
| 3. Routes test (identity / position / value; no address; address alone) | **done**: 0.66 / 0.34 / 0.00; alone fails | **missing**: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| 4. Address swap by dose (x8_write, s = 1 / 2 / 4) | **done**: 0.01 / 0.24 / 0.50 | **missing**: Lightning chain, spec in Dan's order (reads the committed L14); needs the routes test's items | **done**: 0.05 / 0.52 / 0.52 | **done**: 0.02 / 0.46 / 0.73 |
| 5a. Order split (descriptive) | **done** | **missing**: CPU from the conflict test's outcomes once it lands | **done** | **done** |
| 5b. Copy test (45q) | **done**: holds | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done**: holds | **done**: holds |
| 6. Anatomy by layer (47.8) | **queued**: on record a reduced grid (9 of 15 layers); full grid x47_8_27b on mats (run x47_anatomy_27b) | **missing**: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| [7. Ladder (49.2, rungs 1-6)](#t49-2) | **queued**: on record rungs 1-2 only; rungs 1-6 (rung 6 at Zach's L32-40) x52_ladder_27b on another (the speedup copy was stopped after 2 min) | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **queued**: on record, rung 6 at L23-29; rung 6 in Zach's L36-42: x52_ladder_muse on mats (behind part B) |
| 8. Lens readout with the item-change control (47.0) | **done** | **missing**: Lightning chain, spec in Dan's order (reads the committed L14); needs x8_write's items | **done** | **done** |
| [9. Last-token read / write (51.10)](#t51-10) | **done** | **missing**: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| 10. Attention under the swap (49.7) | **done** | **missing**: Lightning chain, spec in Dan's order (reads the committed L14); full attention at 6 of 52 blocks only | **done** | **done** |
| Split in other texts: varied scenes (x0b) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Split in other texts: natural passages (x5) | **done** | **missing**: Lightning, after the 10 key rows | **done**: gate lowered after the data | **done** |
| [Dose curves, a part alone (51.1)](#t51-1) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Zeroing at one layer (47.5) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Earlier mention (45p) | **done** | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** |
| E3: identity route outside the lens (47.1 atom slices) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E6: the address probe (x0_probe v4) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E6: the swap after neutral sentences (47.16 distance) | **missing**: 27B gap: spec to write (mats) | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E7: six lockers, one code per slot (47.2) | **queued**: x47_2_27b on another (behind part B and the 27B ladder) | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E8: the report prompt (47.10) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E11: token by layer map (47.D1) | **queued**: x47_d1_27b on mats (run x47_depthmap_27b) | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** |
| E11: lookups carried before L (47.4 cumulative) | **missing**: 27B gap: spec to write (mats) | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| E12: address persistence across depth (D4, CPU) | **missing**: CPU from x47_anatomy_27b's cache once it lands | **missing**: CPU after Lightning's anatomy | **done** | **done** |
| [Part V: Zach's passages Z1 / Z2 (x50)](#z1) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| [Part V: Zach's passages Z3 (routes on his passages)](#z3) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Described bridge (47.3, and 51.12's cue r2) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **partial**: 47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design) |
| One question, two instructions (49.6) | **done** | **missing**: Lightning, after the 10 key rows | **not tested**: ran; the gate failed (README: the others miss the gate) | **missing**: 9B / Muse gap: not run on Muse |
| Address refit per text format (x45d) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| The lookup's errors are not address errors (47.13) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: a person mark at the locker sentence (48.3 bind) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: copying heads pass the rest (48 heads) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the address as the recall's second route (48 route2) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: blocking the pick sentence (47.6 edges) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the second hop's key token (47.15 source) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the address is the same for any kind of item (47.11 agnostic) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Chained addresses (47.14) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| What is left of the route; the value (47.7) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Gain map (49.1) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| Pooled person probe (49.3) | **missing**: 27B gap: spec to write | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| DAS by position (49.x das_pos) | **not designed**: 9B only by design | **not designed**: 9B only by design | **done** | **not designed**: 9B only by design |
| [Learned subspaces (48 DAS; 51.3 DAS at scale)](#t51-3) | **partial**: 51.3 done; 48's DAS not run on the 27B (51.3 supersedes it) | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| [Joint head ablation under the swap (51.2)](#t51-2) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| [The address at the last token (51.4)](#t51-4) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| [Anatomy on Zach's passages (51.5)](#t51-5) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (51.5 designed for the 9B and 27B) |
| [Z1 on the full carrier (51.7)](#t51-7) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (51.7 designed for the 9B and 27B) |
| [What is the address: dimension, methods, geometry (51.11)](#t51-11) | **partial**: part 2 only by design (parts 1, 3 not designed for the 27B) | **missing**: Lightning, after the 10 key rows | **done** | **done** |
| [Answer-direction control on Zach's Z2 (51.12 Z2)](#z2) | **done** | **missing**: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (Z2 designed for the 9B and 27B) |
<!-- coverage:end -->

## Changes a README claim (README must be updated)

### What the address is apart from how we built it (51.11, opened 28 Oct 22:51) <a id="t51-11"></a>

- Question: is the address one code per locker, a single shared code, or an order line, judged by methods that do not use our construction?
- Verdict (rule fixed in advance): part 1 (dimension by the number of slots): 9B in between (d* = 2 / 2 / >7 / 2 at S = 3 / 4 / 6 / 8), Muse one dimension per slot (2 / 2 / 7 / >7, the literal rule counts d*(8) not found as > 7), 27B not run; part 2 (do three methods find the same code, S = 6): in between on all three; part 3 (midpoint swaps): none of the three on the 9B and Muse.
- Key numbers, from `results/x51_addr/verdict-20261028T215138Z/verdict.md`: 9B part 2, the swap through the learned code R with our code U removed 0.39 [0.37, 0.40], the whole swap with U removed 0.03 [0.01, 0.05]; 9B part 3, the midpoint swap from slot 1 lands on the midpoint 0.06 [0.03, 0.09].
- Where used: README "In one minute", claims table row 8 and the Status line (waiting for Dan).
- Caveats: part 4 (the finding's wording) matches no row of Dan's table; the 27B ran part 2 only.

### The recall's entity at the last token (51.10, opened 28 Oct 20:06) <a id="t51-10"></a>

- Question: does the intermediate (the bridge entity) pass through J-space at the last token and at the question's pick token, per reader?
- Verdict (rule fixed in advance): last token, recall: (b) readable, not used on the 9B, 27B and Muse; last token, lookup: (c) routes around J-space on the 9B, none of the four on the 27B and Muse; the question's pick token: (d) not represented or none of the four on every cell, except the 27B's lookup, (c) routes around J-space.
- Key numbers, from `results/x51_jread/x51_10-20261028T190608Z/verdict.md`: the recall's through-the-lens probe at the read peak 0.97 [0.94, 0.99] (9B, L24); the lens swap's switches over the whole-state patch's at the read peak 0.00 / 0.01 / 0.01 (9B / 27B / Muse; intervals in figures/story/data.csv, rows fig17_jspace_last_token).
- Where used: README new card, Part IV (waiting for Dan); figure figures/story/fig17_jspace_last_token.png.
- Caveats: decided on 49.1's locker-first items (75 / 69 / 68); the swap is his operation or the J++ part at gain <= 2.

### The split on the full carrier (51.7, opened 28 Oct 18:21) <a id="t51-7"></a>

- Question: on Zach's named-bridge passages, does changing the bridge token at every layer up to L (the full carrier) explain the one-layer result, and does the split hold there?
- Verdict (rule fixed in advance): (i) the slice explanation holds on the 9B and 27B; (ii) fact-first (decisive): in between on both; fact-after: the lookup follows the lens on the full carrier on both; (iii) not triggered.
- Key numbers, from `results/x51_carrier/x51_7-20261028T171646Z/verdict.md`: fact-after lookup extra loss on the full carrier 0.51 [0.41, 0.61] (9B), 0.51 [0.42, 0.61] (27B); fact-first lookup 0.10 [0.05, 0.17] (9B).
- Where used: README claims table row 1, its limit (waiting for Dan).
- Caveats: 9B and 27B only; Z1's passages state true facts (see [Z1](#z1)).

### Does the address travel to the last token? (51.4, opened 28 Oct 18:36) <a id="t51-4"></a>

- Question: does the address swap work at the last (read) token, with the bridge word's means or with means refit there?
- Verdict (rule fixed in advance): 9B (c) not at the last token; 27B (c) not at the last token; Muse (a) the code travels.
- Key numbers, from `results/x51_travel/x51_4-20261028T173333Z/verdict.md`: the bridge-fit swap at L+4, s = 2, lookups sent to the target 0.00 [0.00, 0.00] (9B), 0.00 [0.00, 0.01] (27B), 0.45 [0.43, 0.48] (Muse).
- Where used: README claims table row 12 (waiting for Dan); planned Part IV card "the address at the last token".
- Caveats: routes C0 scenes; the probe reads the slot at the last token at L+4 (0.93 9B, 1.00 27B), so "not at the last token" means not usable there, not absent.

### Our removal on Zach's named-bridge passages (Z1, opened 28 Oct 17:17) <a id="z1"></a>

- Question: does the split hold on Zach's passages (named bridge; the lookup's K passage states the true final fact, the recall's M passage leaves it out)?
- Verdict (rule fixed in advance): the lookup follows the lens here on the 9B, 27B and Muse (L26); Muse L36 can't tell (no lookup switch); the order pattern replicates on the 9B and 27B.
- Key numbers, from `results/x50_zach/z1-20261028T161649Z/z1.md`: lookup extra loss 0.26 [0.18, 0.36] (9B), 0.28 [0.18, 0.38] (27B), 0.60 [0.38, 0.81] (Muse L26).
- Where used: README Part V (Fig. 12's "his passages" cells); the wording about reruns waits for Dan.
- Caveats: not the made-up-fact rerun (never specced or run); Muse's lookup switches under the whole change on 0.12 of passages.

## Supports a README claim

### The removal ladder (49.2, opened 28 Oct 17:16) <a id="t49-2"></a>

- Question: does the recall need the J++ part once its other copies (more layers, the earlier mention, the question, every token) are removed too, and does the lookup ever need it?
- Verdict (rule fixed in advance): the second copy is the earlier mention: 9B yes, Muse no; needed only when everything goes: no on both; the lookup never needs it: yes on both; 27B bridge-word rungs only (not judged).
- Key numbers, from `results/x49_ladder/x49_2-20261028T161612Z/x49_2.md`: 9B locker-first cost(3) − cost(2) 0.32 [0.24, 0.39]; 9B recall, all scenes, rung 5 0.44 [0.37, 0.52]; Muse recall, all scenes, rung 5 0.21 [0.15, 0.26].
- Where used: README Part I card "Does the recall need the lens part, or only follow it?"; claims table row 2.
- Caveats: Muse's rung 6 ran at L23-29, outside Zach's band (rerun queued, see [batch 52 C](#b52-c)); the 27B ran rungs 1-2 only (rungs 3-6 running).

### Dose curves (51.1, opened 28 Oct 18:03) <a id="t51-1"></a>

- Question: added by itself at a dose, does the J++ part move the recall above a random part of its share, and does it leave the lookup?
- Verdict (rule fixed in advance): (i) the lookup is blind to the J++ part: 9B yes, 27B no, Muse yes (on all three: no); (ii) the recall reads it above its share: yes on all three; (iii) together only (Muse): no.
- Key numbers, from `results/x51_dose/x51_1-20261028T170335Z/verdict.md`: recall J − R at the first dose >= 0.3: 0.31 [0.20, 0.42] (9B, α = 1.5), 0.42 [0.28, 0.54] (27B, α = 3); the 27B's lookup J − R at α = 3: 0.13 [0.00, 0.26].
- Where used: README Part I card "Does each part, added by itself, move its reader?" (Fig. 16).
- Caveats: locker-first main-test items only (75 / 69 / 68); random parts at α = 3 switch many readers themselves.

### Is it the bridge or the answer that moves through the lens? (51.12, opened 28 Oct 21:18) <a id="t51-12"></a>

- Question: on the main test and on Zach's described bridge, is the J++ part's effect the bridge entity or the answer word?
- Verdict (rule fixed in advance, amended 20:20 before opening): main test recall: the lens effect is the entity (9B, 27B); Muse: the answer word is not read at the bridge word (arms beside: entity); 47.3's described bridge: not read (9B, 27B); Z2: the answer (9B lookup, 27B recall) or mixed (9B recall, 27B lookup).
- Key numbers, from `results/x51_answer/x51_12-20261028T201842Z/verdict.md`: main test recall, share of the loss kept with the answer directions kept 0.95 [0.90, 0.99] (9B), 0.93 [0.85, 0.99] (27B); answer word outside the lens's top 50 at the bridge word, Muse recall 0.99 [0.98, 1.00].
- Where used: README Part I card "In a conflict, which part of the bridge word does each reader follow?" (specificity line); README Part VI, Withdrawn (Z2).
- Caveats: the answer directions are number words (digits are not in the lens dictionary); the pre-amendment runs are kept as records, superseded.

### Learned subspaces at scale (51.3, opened 28 Oct 20:46) <a id="t51-3"></a>

- Question: does a learned (DAS) subspace carry the recall's identity at k <= 128, where does the lookup's learned subspace lie, and does the learned address overlap ours?
- Verdict (rule fixed in advance): (i) a recall subspace is found on all three; (ii) the lookup subspace lies mostly outside U, the J++-25 and W_E-25 atoms on all three; (iii) the learned address overlaps U >= 0.6: no on all three (U's energy 0.246 / 0.226 / 0.193, 9B / 27B / Muse).
- Key numbers, from `results/x51_das/verdict-20261028T194630Z/verdict.md`: recall test own-IIA at k = 128: 0.96 [0.91, 0.99] (9B), 0.80 [0.67, 0.91] (27B), 0.80 [0.64, 0.96] (Muse).
- Where used: README Appendix (Fig. 14 link); planned Part II / III cards.
- Caveats: test entities are few (9 on the 9B's identity pairs); U's energy in the learned address has no interval in the verdict's summary lines.

## Ledger only (opened, not in README)

### What is inside the lens part's 25 directions (batch 52 A, landed 29 Oct 01:01) <a id="b52-a"></a>

- Question: which words do the 25 lens directions of the change stand for: the two bridge items, the answer words, or other words?
- Verdict (descriptive, no rule): on the main test the original and the new bridge words carry about a fifth to two fifths of the rebuilt energy, the answer words almost none; on Zach's described passages the bridge names carry little and the descriptions' words dominate.
- Key numbers, from `results/x52_atoms/report-20261029T000125Z/verdict.md` (main test, recall's view, n = 50): the original bridge word 0.111 [0.091, 0.130] (9B), 0.184 [0.165, 0.198] (Muse); the recall's answer word 0.001 [0.000, 0.002] (9B).
- Where used: ledger only.
- Caveats: a word classifier labels the directions (hand-checked on 5 items per model, blind on Muse's main test only); it misses non-English answer words.

### The address swap's heads (51.2, opened 28 Oct 20:04) <a id="t51-2"></a>

- Question: does a small set of attention heads at the last token carry the address swap's effect, or is it spread over heads?
- Verdict (rule fixed in advance): distributed on the 9B, 27B and Muse (no top-k set up to 10 heads cuts the swap's switch; all heads of the best layer together cut < 0.3).
- Key numbers, from `results/x51_heads/x51_2-20261028T190358Z/verdict.md`: the best layer's heads together, cut at the last token: 0.027 [0.008, 0.044] (9B), −0.061 [−0.283, 0.095] (27B), 0.020 [−0.007, 0.048] (Muse).
- Where used: ledger only; planned Part III ("who reads it").
- Caveats: Gated DeltaNet layers have no heads (skipped on the 9B and 27B); mean ablation at the last token and the question tokens only.

### The read window on Zach's passages (51.5, opened 28 Oct 19:14) <a id="t51-5"></a>

- Question: on Z1's passages, does each reader's read window (the last layer where the whole change switches >= 0.3) end within 4 layers of ours?
- Verdict (rule fixed in advance): 9B the same read window as ours; 27B not the same.
- Key numbers, from `results/x51_depth/x51_5-20261028T181100Z/verdict.md` (layer ends, no interval): 9B lookup L14 vs ours L16, recall L18 vs L14; 27B lookup L34 vs L40, recall L34 vs L32.
- Where used: ledger only; planned Part V.
- Caveats: our 27B window comes from a coarser grid (every 8th layer with L30-34); Muse not run.

### The routes test on Zach's passages (Z3, opened 28 Oct 17:31) <a id="z3"></a>

- Question: on Zach's scattered-fact passages, does the lookup take a position route as well as the identity route?
- Verdict (rule fixed in advance): in between on the 9B and Muse L26 (0.05 < position < 0.20); Muse L36: no position route in his layout; value 0.00 everywhere; 27B not run.
- Key numbers, from `results/x50_zach/z3-20261028T163053Z/z3.md`: position share 0.10 [0.02, 0.19] (9B, n 60), 0.06 [0.00, 0.14] (Muse L26, n 48); identity 0.43 [0.30, 0.56] (9B).
- Where used: ledger only; planned Part V.
- Caveats: small n (60 / 48); lookup only.

### Clean-checkout reruns of the 9B's headline cells (49.5, landed 28 Oct 17:11) <a id="t49-5"></a>

- Question: run from one committed, clean tree, do the 9B's headline runs (main test, routes, only-U, 47.5, 47.8) give the same stored answers?
- Verdict (descriptive, no rule): identical row for row for the main test, routes, only-U and 47.5; 47.8's anatomy differs on 38 of 11,988 rows.
- Key numbers, from `docs/handcheck_clean49.md` (point values, recomputed from the per-item files): main-test gap 0.53 record / 0.53 clean; 47.8 position share at L12 0.51 / 0.52; at L10 0.02 / 0.01.
- Where used: ledger only (a candidate for "How we checked"); per-cell file `results/checks/clean49_9b.json`.
- Caveats: the runs of record ran from dirty trees; the clean runs' own commit is marked dirty in the pack (90210687).

## Withdrawn

### Our removal on Zach's described-bridge passages (Z2, opened 28 Oct 17:27; withdrawn 21:18) <a id="z2"></a>

- Question: does the split hold when Zach's bridge is described, not named?
- Verdict (rule fixed in advance): (a') the computed bridge is handed through the lens on the 9B, 27B and Muse L26; Muse L36 can't tell. Withdrawn by 51.12's addendum rule: the lens effect at the description's last token is the answer or mixed in all four cells ([51.12](#t51-12)).
- Key numbers, from `results/x50_zach/z2-20261028T162710Z/z2.md`: lookup extra loss 0.54 [0.43, 0.66] (9B), 0.69 [0.52, 0.87] (27B), 0.67 [0.00, 1.00] (Muse L26).
- Where used: README Part VI, Withdrawn.
- Caveats: n 158 / 166 / 157, below the 200 aimed for; Muse's lookup switches under the whole change on 0.02 of passages.

## Running or sealed

Box times UTC, from `make queue-stats QUEUE=all` at 00:06 UTC on 29 Oct (low-high ends of the queue's estimate).

### Lightning's layer (batch 52 C prerequisite, committed 29 Oct 01:02) <a id="lightning-layer"></a>

- Question: at which layer does Nemotron 3.5 Lightning get the conflict test, by the published pick rule?
- Verdict (rule fixed in advance: batch 52 amendment 1, Dan ~00:50, before the sweep): L14 (relative depth 0.27), the earliest passing layer at depth >= 0.25. ○ Gate chosen after the 60-scene pre-check was seen: the main test's gate on all 516 scenes passed (0.957 / 0.816, 315 eligible); the 60-scene pre-check failed (0.883 / 0.783). Accepted by Dan 01:10.
- Key numbers, from `results/x51_lightning/nem35l_x52_layer_r2/prereq.md`: at L14 lookup switch 0.58 [0.45, 0.73], recall switch 0.98 [0.94, 1.00] (60 dev scenes).
- Where used: the Lightning conflict test (below); README Status line (waiting for Dan).
- Caveats: `layer.json`'s "rule" field holds the prerequisite text, not amendment 1's pick rule; the first sweep (`results/x51_lightning/nem35l_x52_layer`) stopped at the failed pre-check.

### Lightning's conflict test (batch 52 C, running) <a id="lightning-conflict"></a>

- Question: X0's three arms at all 13 swept layers, decided at L14.
- Verdict: running on speedup, est. end 00:16-00:35 UTC; spec `jobs/c3/x52_lightning_conflict.yaml`; X0's rule verbatim, no prediction (coverage run).
- Key numbers: none yet.
- Where used: coverage matrix (`scripts/x52_coverage.py`).
- Caveats: the 60 dev scenes used for the layer are excluded.

### Batch 52 B: where the answer is readable and usable (answer map) <a id="b52-b"></a>

- Question: where (bridge word, earlier mention, question, last token; every second layer) are the bridge entity and the answer word lens-readable, and can the answer's lens directions be written there?
- Verdict: 12 jobs queued; CPU plan `results/x52_answer_map/plan-20261028T234836Z`. 27B and Muse read / write on mats (ends 00:28-02:08 UTC), 9B on another (ends 00:40-00:55 UTC).
- Key numbers: none yet.
- Where used: ledger only.
- Caveats: rule fixed in advance in `jobs/c3/batch52.yaml` (B); no prediction.

### Batch 52 C: model coverage <a id="b52-c"></a>

- Question: fill the key rows of the coverage matrix on the 27B, Lightning, 9B and Muse.
- Verdict: running. On mats: the 27B anatomy full grid (`jobs/c3/x47_8_27b.yaml`, ends 00:23-01:17 UTC), the 27B token map (`jobs/c3/x47_d1_27b.yaml`, ends 00:33-01:35 UTC), the Muse ladder with rung 6 inside Zach's band (`jobs/c3/x52_ladder_muse_r2.yaml`, ends 00:58-02:26 UTC). On another: the 27B ladder rungs 3-6 (`jobs/c3/x52_ladder_27b_a.yaml`, ends 00:34 UTC), then the 27B six lockers (`jobs/c3/x47_2_27b_r3.yaml`, ends 01:31 UTC). On speedup: Lightning's conflict test (above). Bolt: out of scope, only a J-lens exists, no J++ lens.
- Key numbers: none yet; matrix in `results/x52_coverage`.
- Where used: coverage matrix.
- Caveats: coverage runs on already-scored rules carry no prediction; `results/x49_ladder/x52_ladder_27b` is a stopped partial run kept as a record.
