# Experiments ledger (depth)

Every opened test, so nothing is lost (Dan, 29 Oct ~01:10), written to be read without the runs, like the README's Part I (Dan, 01:15). Internal doc: test ids in the card headings only. Sections by status; inside each, the story's order (two readers → identity → address → where and when → other datasets). Each card follows the README's template: Question, Why we asked, Data, Method, Rule fixed in advance (quoted), one figure, Result (one column per model, 95% intervals, every number with its source), Read, Caveats. No interpretation beyond the verdict. Opened times are the opening commit's time (Paris, 28 Oct unless stated); box times are UTC. Every result here is UNVERIFIED until a human adds it to VERIFIED.md (said once, here). `uv run python scripts/check_ledger.py` checks every cited path, anchor, field and the coverage table (tests/test_experiments_ledger.py).

Restructure in progress (Dan 01:15): the coverage table and the cards are in; the figures come next (step 3).

## Flagged for Dan

1. Lightning's gate (○ gate chosen after the 60-scene pre-check was seen): the main test's gate on all 516 scenes decides; the 60-scene pre-check had failed (lookup 0.883, recall 0.783) before the choice. Accepted by Dan 01:10; layer L14 stands. See [Lightning's layer](#lightning-layer).
2. Lightning's `layer.json` "rule" field (and prereq.md's "Pick rule" line) holds the prerequisite rule text, not the amendment-1 pick rule; the pick itself follows amendment 1 (earliest passing layer at relative depth >= 0.25): prereq.md lists the candidates at depth >= 0.25 and marks L14 as the pick.
3. 51.11's wording: no row of Dan's wording table matches the labels (9B: in between / in between / none of the three; Muse: one per slot / in between / none of the three; 27B: part 2 in between only). The README claim waits for Dan. See [51.11](#t51-11).
4. Z1 is not the made-up-fact rerun: Z1 ran Zach's K passages, which state true facts; the P-item reruns were never specced or run. See [Z1](#z1).
5. Bolt is out of scope: only a J-lens exists, no J++ lens (batch 52 amendment 2); the Bolt row in docs/digest.md is a J-lens result and is not cited on the depth side.
6. The varied-scene count for Muse: Fig. 9a's per-format n sum to 1389, docs/x0_numbers.json's `x0b_n_muse` says 1,388 (not traced).
7. The ladder on Lightning: not tested. It runs on the clean one-pick design, whose gate fails on Lightning (recall 0.751), the same reason as the copy test; no spec.
8. The routes test's sanity swap on Lightning uses Muse's C0 rule (switch rate >= 0.50): Lightning has no one-pick reference.
9. Attention under the swap on Lightning needs a NemotronH port (in progress); if it does not land: "not tested: port missing".
10. Lightning's GPU0 lane (probe, routes, swap, lens readout) now runs on speedup, not mats, so it starts sooner.
11. The previous ledger said Z1's order pattern replicates on the 9B and 27B; its verdict says it replicates on all three (Muse L26 too). Corrected in the Z1 card.

## README changes waiting for Dan

Overnight rule (Dan 01:10): no README edits until Dan returns. One line each:

- "In one minute" and claim 8: "one code per locker" is not what 51.11 supports on the 9B (d* 2/2/>7/2, in between; the methods agree only in part; midpoint swaps fail); reword and regrade claim 8 ([51.11](#t51-11)).
- Status line: 51.11 is opened, not sealed; add Lightning's layer L14 and its rule (amendment 1, Dan ~00:50: earliest passing layer at relative depth >= 0.25; tie-break the bridge word's lens readability) ([Lightning's layer](#lightning-layer)).
- Part V: replace "reruns with made-up-fact passages are queued" by the truth: Z1 ran the true-fact K passages; no P-item rerun was specced or run ([Z1](#z1)).
- New card, Part IV next to the address at the last token: the recall's entity at the last token is readable but not used, all three models; figure figures/story/fig17_jspace_last_token.png ([51.10](#t51-10)).
- Claim 1: add the full-carrier limit (fact-after lookups follow the lens, 0.51 on the 9B and 27B) ([51.7](#t51-7)).
- Claim 12: add the last-token result (the address is not at the last token on the 9B and 27B; it travels on Muse) ([51.4](#t51-4)).
- Claim 1, models: the conflict test is confirmed on Lightning at L14 (coverage run, no prediction; gate chosen after the 60-scene pre-check was seen) ([Lightning's conflict test](#lightning-conflict)).

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

### Does the split survive when the bridge is changed at every layer up to L? (51.7, opened 28 Oct 18:21) <a id="t51-7"></a>

*Used in: README claims table row 1, its limit (waiting for Dan). Story: two readers.*

- **Question.** On Zach's named-bridge passages, does changing the bridge token at every layer up to L (the full carrier) explain the one-layer result, and does the split hold there?
- **Why we asked.** At one layer his fact-after lookups barely switch; the link may be carried by the bridge token over several layers.
- **Data.** Z1's passages: 200 per model (9B: 100 fact-first, 100 fact-after; 27B: 97 / 103); 9B and 27B.
- **Method.** The change at the bridge name's last token at every block output up to L; the conflict test on it: without the lens part, against without a random part of the same share; the one-layer change beside.
- **Rule, fixed in advance.** "(i) "The slice explanation": the whole before-L raises the lookup's switch on fact-after items by >= 0.3 over the one-layer whole, and on fact-first brings the lookup within 0.10 of the recall. (ii) On the full carrier, per model and reported per stratum with fact-first decisive: recall extra loss - lookup extra loss >= 0.3 and lookup <= 0.10 -> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on the full carrier"; else in between." (verdict.md)
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | fact-after lookups switched: one layer → full carrier, rise | 0.54 [0.44, 0.64]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| qwen35_9b_x51_7 :: 0.54 [0.44, 0.64] --> | 0.73 [0.64, 0.81]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| x51_7_27b :: 0.73 [0.64, 0.81] --> | not run | not run |
  | fact-first: lookup switches lost beyond a random part | 0.10 [0.05, 0.17]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.10 [0.05, 0.17] --> | 0.16 [0.07, 0.25]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.16 [0.07, 0.25] --> | | |
  | fact-first: recall switches lost beyond a random part | 0.41 [0.31, 0.52]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.41 [0.31, 0.52] --> | 0.28 [0.18, 0.38]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.28 [0.18, 0.38] --> | | |
  | fact-after: lookup switches lost beyond a random part | 0.51 [0.41, 0.61]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| the lookup follows the lens on the full carrier :: 0.51 [0.41, 0.61] --> | 0.51 [0.42, 0.61]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| the lookup follows the lens on the full carrier :: 0.51 [0.42, 0.61] --> | | |
  | rule (i) / (ii), fact-first | holds / in between | holds / in between | | |

- **Read.**
  - Carried over every layer up to L, the fact-after lookups switch as often as the fact-first ones, so the one-layer result was a slice.
  - On the full carrier the fact-first split is in between; fact-after lookups follow the lens part.
- **Caveats.**
  - Zach's lookup passages state true facts (see [Z1](#z1)).
  - Muse not run (designed for the 9B and 27B).

### What is the address, independent of how we built it? (51.11, opened 28 Oct 22:51) <a id="t51-11"></a>

*Used in: README "In one minute", claims table row 8, Status line (waiting for Dan). Story: the address.*

- **Question.** Is the address one code per locker, one shared code, or an order line, by methods that do not use our construction?
- **Why we asked.** Our address was built from means of four slots; its size and shape could be an artefact of that build.
- **Data.** Routes-style scenes with 3, 4, 6 and 8 lockers; held-out entities only (9B and Muse, all three parts; 27B part 2 only).
- **Method.** Part 1: the smallest learned subspace dimension d* that carries the position switch, per number of lockers, against random subspaces. Part 2: the address swap through our code, a probe's code and a learned code, each with the others removed, against a random direction. Part 3: swaps to the midpoint between two slots, against a random vector of the same norm.
- **Rule, fixed in advance.** Part 1: "One dimension per slot: d*(S) ≥ S − 2 for every S and d*(8) ≥ 5"; "An ordinal (low-dimensional) code: d*(S) ≤ 2 for every S up to 8"; else in between. Part 2: "One code, three bases: every projected swap reaches ≥ 0.6 of the whole swap's effect, and each cross-removal cuts the other's swap by ≥ 0.6." Part 3: "Categories: midpoint swaps send < 0.1 to the midpoint slot while the full swaps reach ≥ 0.4 of the target"; "A metric order: midpoint swaps send ≥ 0.3 of lookups to the midpoint slot, from both ends." (jobs/c3/batch51.yaml, addendum 3)
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | part 1, d* at 3 / 4 / 6 / 8 lockers | 2 / 2 / > 7 / 2: **in between** | not designed | 2 / 2 / 7 / > 7: **one dimension per slot** | not run |
  | part 2: swap through the learned code with ours removed | 0.39 [0.37, 0.40]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 0.03 [0.01, 0.05] :: 0.39 [0.37, 0.40] --> | **in between** | **in between** | |
  | part 2: the whole swap with ours removed | 0.03 [0.01, 0.05]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 0.39 [0.37, 0.40] :: 0.03 [0.01, 0.05] --> | | | |
  | part 3: midpoint swap from slot 1 lands on the midpoint | 0.06 [0.03, 0.09]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 9.0243 :: 0.06 [0.03, 0.09] --> (none of the three) | not designed | none of the three | |

- **Read.**
  - No row of the wording table matches the labels; the methods agree only in part, and midpoint swaps do not land between slots.
- **Caveats.**
  - The 9B's d* at 6 lockers was not found below 8; Muse's "one per slot" rests on the literal rule (d*(8) not found counts as > 7).
  - The 27B ran part 2 only.

### Does the address travel to the last token? (51.4, opened 28 Oct 18:36) <a id="t51-4"></a>

*Used in: README claims table row 12 (waiting for Dan). Story: where and when.*

- **Question.** Does the address swap work at the last token, with the bridge word's slot means or with means refit there?
- **Why we asked.** The answer is read at the last token; the address could be copied there or re-encoded.
- **Data.** Routes scenes without a move, 300 per model (read half 145 / 150 / 144).
- **Method.** The address swap added at the last token at L and L+4, at doses 1 and 2, with the bridge word's means and with last-token means; each against a random vector of its norm; a slot probe at the last token beside.
- **Rule, fixed in advance.** "The code travels: the bridge-fit swap sends >= 0.3 of lookups to slot k (random <= 0.05). Re-encoded on copy: bridge-fit <= 0.10 while last-token-fit >= 0.3. Not at the last token: both <= 0.10 while the probe reads the slot there >= 0.8. Otherwise in between."
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | bridge-fit swap at L+4, dose 2: lookups sent to the target | 0.00 [0.00, 0.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| bridge_swap :: 1.00 [1.00, 1.00] :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.01]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| 0.99 [0.99, 1.00] :: 0.00 [0.00, 0.01] --> | 0.45 [0.43, 0.48]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| bridge_swap :: 0.45 [0.43, 0.48] --> | not run |
  | slot probe at the last token, L / L+4 | 0.55 [0.50, 0.61]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| qwen35_9b_x51_4 :: 0.55 [0.50, 0.61] --> / 0.93 [0.89, 0.96]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| qwen35_9b_x51_4 :: 0.93 [0.89, 0.96] --> | 0.85 [0.80, 0.89]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| x51_4_27b :: 0.85 [0.80, 0.89] --> / 1.00 [1.00, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| x51_4_27b :: 1.00 [1.00, 1.00] --> | 0.99 [0.97, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| muse30_x51_4 :: 0.99 [0.97, 1.00] --> / 0.99 [0.98, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| muse30_x51_4 :: 0.99 [0.98, 1.00] --> | |
  | the rule | **not at the last token** | **not at the last token** | **the code travels** | |

- **Read.**
  - On the 9B and 27B the slot is readable at the last token but the bridge word's code does not work there; on Muse it does.
- **Caveats.**
  - "Not at the last token" means not usable there by this swap, not absent: the probe reads the slot there.
  - Doses 1 and 2 only.

### Is the recall's bridge entity read through the lens at the last token? (51.10, opened 28 Oct 20:06) <a id="t51-10"></a>

*Used in: README new card, Part IV (waiting for Dan). Story: where and when.*

- **Question.** At the last token and at the question's pick token, is the bridge entity readable through the lens, and does writing it through the lens move the answer?
- **Why we asked.** The bridge word's lens part is followed by the recall; the answer is computed later, at the last token.
- **Data.** Main test, the scenes whose locker sentences come first: 75 / 69 / 68 per model.
- **Method.** Read: a probe on the lens part of the state, layer by layer, against the full state and chance. Write: at the read peak, Zach's swap or the lens part of the change (gain up to 2), against a random part and his rotated control; the whole-state patch as reference.
- **Rule, fixed in advance.** "read: through-the-lens probe >= 0.8 and lens top-5 >= 0.5 at some layer before the answer digit's layer, while the full-residual probe >= 0.9 there. write: at the layer of the read peak, his swap or the J++ part of the change (gain <= 2) switches >= 0.5 of what the whole-state patch switches at that layer, with the random part <= 0.10."
- **Result.** (recall, last token)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | read peak layer (answer layer) | L24 (L29) | L56 (L61) | L40 (L46) | not run |
  | through-the-lens probe at the peak | 0.97 [0.94, 0.99]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.87 :: 0.97 [0.94, 0.99] --> | 0.95 [0.89, 0.99]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.80 :: 0.95 [0.89, 0.99] --> | 0.95 [0.91, 0.98]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.73 :: 0.95 [0.91, 0.98] --> | |
  | swap / whole-state patch, switches | 0.00 / 0.95<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L24: 0.00 / 0.95 :: 0.00 / 0.95 --> | 0.01 / 0.97<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L56: 0.01 / 0.97 :: 0.01 / 0.97 --> | 0.01 / 1.00<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L40: 0.01 / 1.00 :: 0.01 / 1.00 --> | |
  | the rule (recall, last token) | **readable, not used** | **readable, not used** | **readable, not used** | |

- **Read.**
  - At the last token the recall's bridge entity is readable through the lens on all three models, but writing it through the lens does not move the answer.
- **Caveats.**
  - The lookup's cells: routes around J-space (9B) or none of the four (27B, Muse); the question's pick token: not represented or none of the four on almost every cell.
  - Locker-first scenes only.

### Does the split hold on Zach's passages with a named bridge? (Z1, opened 28 Oct 17:17) <a id="z1"></a>

*Used in: README Part V (Fig. 12's "his passages" cells); the wording about reruns waits for Dan. Story: other datasets.*

- **Question.** On Zach's passages with a named bridge, does the lookup let go of the lens part while the recall follows it?
- **Why we asked.** Our scenes are short lists; his passages scatter the facts in prose.
- **Data.** His passages (named bridge; the lookup's passage states the true final fact, the recall's leaves it out): 200 per model.
- **Method.** The conflict test at the bridge name's last token at L: without the lens part, against without a random part; each reader gets its own change.
- **Rule, fixed in advance.** "Per model: gap >= 0.3 and lookup extra loss <= 0.10 → the split holds on his passages; lookup >= 0.20 → the lookup follows the lens here; else in between. The order pattern replicates if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs)."
- **Result.**

  | | 9B | 27B | Muse (L26) | Lightning |
  |---|---|---|---|---|
  | lookup: switches lost beyond a random part | 0.26 [0.18, 0.36]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| qwen35_9b_x50_z1 :: 0.26 [0.18, 0.36] --> | 0.28 [0.18, 0.38]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| x50_z1_27b :: 0.28 [0.18, 0.38] --> | 0.60 [0.38, 0.81]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| muse30_x50_z1 :: 0.60 [0.38, 0.81] --> | not run |
  | recall: switches lost beyond a random part | 0.64 [0.56, 0.71]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| qwen35_9b_x50_z1 :: 0.64 [0.56, 0.71] --> | 0.58 [0.49, 0.66]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| x50_z1_27b :: 0.58 [0.49, 0.66] --> | 0.81 [0.72, 0.90]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| muse30_x50_z1 :: 0.81 [0.72, 0.90] --> | |
  | lookups switched, fact-first / fact-after | 0.78 [0.68, 0.86]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L12 order :: 0.78 [0.68, 0.86] --> / 0.36 [0.27, 0.46]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L12 order :: 0.36 [0.27, 0.46] --> | 0.67 [0.57, 0.76]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L32 order :: 0.67 [0.57, 0.76] --> / 0.11 [0.05, 0.17]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L32 order :: 0.11 [0.05, 0.17] --> | 0.20 [0.12, 0.29]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L26 order :: 0.20 [0.12, 0.29] --> / 0.05 [0.01, 0.10]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L26 order :: 0.05 [0.01, 0.10] --> | |
  | the rule | **the lookup follows the lens here** | **the lookup follows the lens here** | **the lookup follows the lens here** | |

- **Read.**
  - On his named-bridge passages the lookup follows the lens part too, on all three models; the order pattern replicates on all three.
- **Caveats.**
  - Not the made-up-fact rerun: his lookup passages state true facts; the P-item reruns were never specced or run.
  - Muse's lookup switches under the whole change on 0.12 of passages; at L36 it cannot tell.

## Supports a README claim

### Is it the bridge item or its answer that moves through the lens? (51.12, opened 28 Oct 21:18) <a id="t51-12"></a>

*Used in: README Part I card "In a conflict, which part of the bridge word does each reader follow?" (specificity); README Part VI, Withdrawn (Z2). Story: two readers.*

- **Question.** On the main test, is the recall's loss without the lens part about the bridge item or about its answer word?
- **Why we asked.** At a described bridge the lens reads the answer about as well as the item; the same could hold at our bridge word.
- **Data.** Main test, 200 per model.
- **Method.** At the bridge word at L: (1) without the lens part; (2) without the lens part but keeping its directions for both readers' answer words (number words); (3) without those answer directions only; each against a random part of its share; the lens's rank of the answer word at the bridge word first.
- **Rule, fixed in advance.** (Amended 20:20, before opening.) "The lens effect is the entity: arm 2 keeps >= 0.7 of arm 1's extra loss and arm 3 costs <= 0.10 beyond random. The lens effect is the answer: arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed." First: "the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)".
- **Result.** (recall)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | (1) switches lost beyond a random part | 0.50 [0.41, 0.57]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.50 [0.41, 0.57] --> | 0.74 [0.66, 0.80]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.74 [0.66, 0.80] --> | 0.76 [0.62, 0.88]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| arms beside: the lens effect is the entity :: 0.76 [0.62, 0.88] --> | queued |
  | (2) / (1): loss kept with the answer directions kept | 0.95 [0.90, 0.99]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.95 [0.90, 0.99] --> | 0.93 [0.85, 0.99]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.93 [0.85, 0.99] --> | 0.93 [0.85, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| arms beside: the lens effect is the entity :: 0.93 [0.85, 1.00] --> | |
  | (3) without the answer directions only, beyond random | 0.00 [0.00, 0.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.47 [0.39, 0.55] :: 0.00 [0.00, 0.00] --> | 0.03 [0.01, 0.05]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.69 [0.59, 0.77] :: 0.03 [0.01, 0.05] --> | -0.01 [-0.05, 0.03]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.71 [0.56, 0.84] :: -0.01 [-0.05, 0.03] --> | |
  | answer word outside the lens's top 50 | 0.56 [0.47, 0.66]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.50 [0.41, 0.57] :: 0.56 [0.47, 0.66] --> | 0.79 [0.72, 0.86]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.74 [0.66, 0.80] :: 0.79 [0.72, 0.86] --> | 0.99 [0.98, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.76 [0.62, 0.88] :: 0.99 [0.98, 1.00] --> | |
  | the rule | **the entity** | **the entity** | **the answer word is not read** | |

- **Read.**
  - The recall's loss without the lens part is the item's: keeping the answer's lens directions keeps almost all of it, and those directions alone cost nothing.
- **Caveats.**
  - Digits are not in the lens dictionary, so the answer directions are number words; the pre-amendment runs are kept, superseded.
  - On Zach's described bridge the same control finds the answer, not the item (see [Z2](#z2)).

### Does the conflict test hold on Lightning? (Lightning conflict test, opened 29 Oct 01:16 UTC) <a id="lightning-conflict"></a>

*Used in: not in the README yet (waiting for Dan). Story: two readers.*

- **Question.** On Nemotron 3.5 Lightning, at its committed layer L14, does the recall follow the lens part while the lookup goes around it?
- **Why we asked.** A fourth model, of another family, under the main test's rule unchanged.
- **Data.** Main test, 200 scenes (the 60 scenes used to pick the layer excluded); ○ gate chosen after the 60-scene pre-check was seen: the main test's gate on all 516 scenes passed (lookup 0.957, recall 0.816).
- **Method.** The conflict test at the bridge word at each of 13 swept layers (L2 to L50), decided at L14: without the lens part, against without a random part of the same share.
- **Rule, fixed in advance.** The main test's: "confirmed if the lookup loses at most 0.10 beyond random and the recall loses at least 0.30 of its switches without the lens part; killed if the lookup loses at least 0.20 or the recall under 0.20." Coverage run on an already-scored rule: no prediction.
- **Result.** (L14)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | recall: switches lost beyond a random part | see the README | | | 0.34 [0.25, 0.44]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.94 :: 0.34 [0.25, 0.44] --> |
  | recall: switches lost, not net of random | | | | 0.41 [0.32, 0.50]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.94 :: 0.41 [0.32, 0.50] --> |
  | lookup: switches lost beyond a random part | | | | 0.03 [-0.01, 0.08]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.45 :: 0.03 [-0.01, 0.08] --> |
  | lookup: switches under the whole change | | | | 0.45<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.03 [-0.01, 0.08] :: 0.45 --> |
  | the rule | | | | **confirmed** (lookup around, recall through) |

- **Read.**
  - At L14 the recall follows the lens part and the lookup does not; the same split stands at L18 and L22.
- **Caveats.**
  - The gate was chosen after the 60-scene pre-check had failed (accepted by Dan 01:10).
  - From L26 on the lookup switches on 0.02 of scenes or fewer, so those layers cannot tell.

### Does each part, added by itself, move its reader? (51.1, opened 28 Oct 18:03) <a id="t51-1"></a>

*Used in: README Part I card of the same name (Fig. 16). Story: two readers.*

- **Question.** Added by itself at a dose, does the lens part move the recall more than a random part of its share, and leave the lookup?
- **Why we asked.** The conflict test takes a part away; a reader that follows a part should also move when only that part is added.
- **Data.** Main test, the scenes whose locker sentences come first: 75 / 69 / 68.
- **Method.** At the bridge word at L: the lens part alone at doses 0.5 to 3, against a random part of the same share at the same dose; the rest alone at doses 0.25 to 1.5, with and without the address.
- **Rule, fixed in advance.** "(i) the lookup is blind to the J++ part: switch minus random <= 0.10 at every α whose plain-text loss stays under 2x the whole change's, on all three. (ii) the recall reads the J++ part above its share: at the first α where the J++ part alone switches >= 0.3, J minus random >= 0.2, per model. (iii) together only (Muse): (1,1) >= 0.8 while the best single-part dose under the loss bar stays <= 0.3."
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | recall: lens part alone minus random, dose 1.5 | 0.31 [0.20, 0.42]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.31 [0.20, 0.42] --> | 0.12 [0.05, 0.19]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.12 [0.05, 0.19] --> | 0.13 [0.04, 0.24]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.13 [0.04, 0.24] --> | not run |
  | recall: the same at dose 3 | -0.05 [-0.16, 0.05]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.05 [-0.16, 0.05] --> | 0.42 [0.28, 0.54]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.42 [0.28, 0.54] --> | 0.22 [0.07, 0.37]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.22 [0.07, 0.37] --> | |
  | lookup: lens part alone minus random, dose 3 | -0.63 [-0.72, -0.52]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.63 [-0.72, -0.52] --> | 0.13 [0.00, 0.26]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.13 [0.00, 0.26] --> | -0.22 [-0.32, -0.13]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.22 [-0.32, -0.13] --> | |
  | rule (i) / (ii) | yes / yes | **no** / yes | yes / yes; (iii) no | |

- **Read.**
  - Added by itself, the lens part moves the recall more than a random part on all three models, and the 9B's and Muse's lookups no more than random; the 27B's lookup moves at the highest dose.
- **Caveats.**
  - At high doses random parts switch readers too (the 9B's random part at dose 3 switches most lookups).
  - Scenes with the lockers first only.

### Does the recall need the lens part once its other copies are gone? (49.2, opened 28 Oct 17:16) <a id="t49-2"></a>

*Used in: README Part I card "Does the recall need the lens part, or only follow it?" (Fig. 1d); claims table row 2. Story: two readers.*

- **Question.** Taking the lens part out of the changed prompt step by step (more layers, the earlier mention, the question, every token), when does the recall start to need it, and does the lookup ever?
- **Why we asked.** At one layer the recall barely needs the lens part; it may have copies elsewhere.
- **Data.** Clean one-pick scenes: 417 / 574 / 409 (27B: steps 1-2 only).
- **Method.** In the changed prompt's own run, the lens part's 25 directions taken out at each step's tokens and layers, against a random subspace of the same share of the state; step 6 is Zach's definition (each token's own top-10 lens directions over his band).
- **Rule, fixed in advance.** "second_copy: rung (3) costs the recall >= 0.3 more than rung (2) in locker-first scenes (paired CI excluding 0) and rung (2) already costs >= 0.3 in locker-after scenes; only_everything: rungs (1)-(4) each <= 0.2 and rung (5) or (6) >= 0.5; lookup: <= 0.1 beyond random at every rung."
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | recall, locker first: step 3 minus step 2 | 0.32 [0.24, 0.39]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-first :: 0.32 [0.24, 0.39] --> | – | 0.10 [0.05, 0.15]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-first :: 0.10 [0.05, 0.15] --> | not tested (gate) |
  | recall, all scenes: step 5, answers lost beyond random | 0.44 [0.37, 0.52]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| 0.51 / 0.95 / 0.44 [0.37, 0.52] :: 0.44 [0.37, 0.52] --> | – | 0.21 [0.15, 0.26]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| 0.78 / 0.99 / 0.21 [0.15, 0.26] :: 0.21 [0.15, 0.26] --> | |
  | recall, locker after: step 2 | 0.40 [0.31, 0.51]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-after :: 0.40 [0.31, 0.51] --> | 0.26 [0.19, 0.34]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-after :: 0.26 [0.19, 0.34] --> | 0.15 [0.10, 0.22]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-after :: 0.15 [0.10, 0.22] --> | |
  | rules: second copy / only everything / lookup never | yes / no / yes | steps 1-2 only | no / no / yes | |

- **Read.**
  - The recall needs the lens part once its copies over four layers and at the earlier mention go (9B); on Muse every step costs less. The lookup never needs it.
- **Caveats.**
  - Muse's step 6 ran at L23-29, outside Zach's band (rerun queued); the 27B's steps 3-6 are running.
  - Lightning: not tested, the clean one-pick design's gate fails there (recall 0.751).

### Does a learned subspace carry the readers' codes, and is the learned address ours? (51.3, opened 28 Oct 20:46) <a id="t51-3"></a>

*Used in: README Appendix (Fig. 14 link); planned Part II / III cards. Story: identity and the address.*

- **Question.** Does a learned (DAS) subspace of at most 128 directions carry the recall's identity switch, where does the lookup's learned subspace lie, and does the learned 4-direction address overlap ours?
- **Why we asked.** Our parts are hand-built (lens directions, slot means); a trained subspace tests them without that choice.
- **Data.** Identity pairs from the main, clean and routes scenes (9B: 514 recall pairs; 27B 374; Muse 300), test entities held out; routes position pairs for the address.
- **Method.** Distributed alignment search: a subspace trained to carry the switch, its own interchange accuracy on test pairs, against a random subspace and a shuffled-target subspace of the same size.
- **Rule, fixed in advance.** "Q51.3 (i) 'found' = >= 300 recall pairs and test own-IIA >= 0.5 at some k <= 128; (ii) the lookup subspace (R_lookup at its chosen k) on the test pairs: the share of R R^T Delta inside U, the J++-25 atoms, the W_E-25 atoms and outside their union, each part >= 0.5 named 'mostly' (descriptive; the parts overlap); (iii) U's energy in R_pos at k = 4 = ||R_pos^T U||_F^2 / rank U >= 0.6" (verdict.md, as computed)
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | (i) recall, test own-IIA at k = 128 | 0.96 [0.91, 0.99]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 514 :: 0.96 [0.91, 0.99] --> | 0.80 [0.67, 0.91]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 374 :: 0.80 [0.67, 0.91] --> | 0.80 [0.64, 0.96]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 300 :: 0.80 [0.64, 0.96] --> | not run |
  | (ii) the lookup subspace (k = 4) outside our parts | 0.62<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| in U 0.36 :: in outside 0.62 :: 0.62 --> | 0.62<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| U's energy in R_lookup 0.2509 :: 0.62 --> | 0.72<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| in outside 0.72 :: 0.72 --> | |
  | (iii) our address's energy in the learned address | 0.246<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.246 --> | 0.226<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.226 --> | 0.193<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.193 --> | |
  | the rule (i) / (ii) / (iii) | found / mostly outside / no | found / mostly outside / no | found / mostly outside / no | |

- **Read.**
  - A learned subspace carries the recall's identity on all three; the lookup's lies mostly outside our parts, and the learned address holds about a quarter of ours.
- **Caveats.**
  - Few test entities (9 on the 9B's identity pairs).
  - (ii) and (iii) have no interval in the verdict's summary lines.

## Ledger only (opened, not in README)

### What is inside the lens part's 25 directions? (batch 52 A, landed 29 Oct 01:01) <a id="b52-a"></a>

*Used in: ledger only. Story: two readers.*

- **Question.** Which words do the 25 lens directions of the change stand for: the two bridge items, the answer words, or other words?
- **Why we asked.** The answer control tests the answer words only; the rest of the lens part was never looked at.
- **Data.** Main test, 50 locker-first items per model; Zach's described passages, 50 per model.
- **Method.** Each of the 25 lens directions labelled by a word classifier (the bridge words with their spellings, the answer words, other classes); the share of the rebuilt energy per class, against a chance baseline.
- **Rule, fixed in advance.** None: descriptive inventory, no rule.
- **Result.** (main test, recall's view)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | rebuilt energy in the original bridge word | 0.111 [0.091, 0.130]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.111 [0.091, 0.130] --> | 0.101 [0.075, 0.126]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.101 [0.075, 0.126] --> | 0.184 [0.165, 0.198]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.184 [0.165, 0.198] --> | not run |
  | in the new bridge word | 0.110 [0.093, 0.124]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.110 [0.093, 0.124] --> | 0.113 [0.096, 0.134]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.113 [0.096, 0.134] --> | 0.190 [0.168, 0.212]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.190 [0.168, 0.212] --> | |
  | in the recall's answer word | 0.001 [0.000, 0.002]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.001 [0.000, 0.002] --> | 0.001 [0.000, 0.002]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.001 [0.000, 0.002] --> | 0.001 [0.000, 0.003]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.001 [0.000, 0.003] --> | |
  | in other words | 0.765 [0.739, 0.796]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.765 [0.739, 0.796] --> | 0.774 [0.739, 0.808]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.774 [0.739, 0.808] --> | 0.609 [0.584, 0.642]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.609 [0.584, 0.642] --> | |

- **Read.**
  - On the main test the two bridge words carry about a fifth (9B, 27B) to two fifths (Muse) of the rebuilt energy, the answer words almost none.
- **Caveats.**
  - The classifier was hand-checked on 5 items per model (blind on Muse's main test only) and misses non-English answer words.
  - On Zach's described passages the bridge names carry 0.02-0.03 and the descriptions' words dominate (see the report).

### At which layer does Lightning get the conflict test? (Lightning's layer, committed 29 Oct 01:02) <a id="lightning-layer"></a>

*Used in: the Lightning conflict test; README Status line (waiting for Dan). Story: two readers.*

- **Question.** At which layer does Nemotron 3.5 Lightning get the conflict test?
- **Why we asked.** A new model needs its layer L fixed before any scored run.
- **Data.** 60 dev scenes of the main test (excluded from the conflict test).
- **Method.** The whole change at the bridge word at every 4th layer (L2 to L50); each reader's switch rate; the bridge word's lens readability recorded as the tie-break.
- **Rule, fixed in advance.** Batch 52 amendment 1 (Dan ~00:50, before the sweep): "earliest layer passing the gate at relative depth ≥ 0.25; tie-break = highest lens readability of the bridge word." Passing = both readers switch on at least 0.3 (the published rule). ○ Gate chosen after the 60-scene pre-check was seen.
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | the layer | L12 | L32 | L26 | **L14** (depth 0.27) |
  | lookup switch at L14 | | | | 0.58 [0.45, 0.73]<!-- src: results/x51_lightning/nem35l_x52_layer_r2/prereq.md \| L14 (pick) :: 0.58 [0.45, 0.73] --> |
  | recall switch at L14 | | | | 0.98 [0.94, 1.00]<!-- src: results/x51_lightning/nem35l_x52_layer_r2/prereq.md \| L14 (pick) :: 0.98 [0.94, 1.00] --> |

- **Read.**
  - L14 is the earliest layer at depth 0.25 or more where both readers switch on at least 0.3 of scenes.
- **Caveats.**
  - The 60-scene pre-check failed (lookup 0.883, recall 0.783); the main test's gate on all 516 scenes decided (accepted by Dan 01:10).
  - `layer.json`'s "rule" field holds the prerequisite text, not amendment 1's pick rule.

### Do a few heads read the swapped address? (51.2, opened 28 Oct 20:04) <a id="t51-2"></a>

*Used in: ledger only; planned Part III ("who reads it"). Story: the address.*

- **Question.** Does a small set of attention heads carry the address swap's effect at the last token, or is it spread over heads?
- **Why we asked.** Attention follows the swapped address; a few heads could be the readers.
- **Data.** The attention test's items and swap (routes scenes): read pairs 330 (9B), 284 (Muse), 220 cases (27B).
- **Method.** Heads ranked by their attention move on the fit half, mean-ablated together on the read half at the last token (and the question tokens), against random head sets of the same size in the same layers.
- **Rule, fixed in advance.** "small_set: some top-k set, k in {1, 3, 5, 10}, cuts >= 0.5 while the identity answers (...) change <= 0.10 and the recall's answer changes <= 0.10 (...), and the matched random sets of k heads (same layers) cut <= 0.15 (mean over the draws). distributed: every head of the best layer together cuts < 0.3."
- **Result.** (last token)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | the best layer's heads together: share of the swap's switch cut | 0.027 [0.008, 0.044]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.448 -> 0.436 :: 0.027 [0.008, 0.044] --> | -0.061 [-0.283, 0.095]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.220 -> 0.233 :: -0.061 [-0.283, 0.095] --> | 0.020 [-0.007, 0.048]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.539 -> 0.528 :: 0.020 [-0.007, 0.048] --> | not run |
  | the top 10 heads: cut | 0.007 [-0.065, 0.060]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.448 -> 0.445 :: 0.007 [-0.065, 0.060] --> | | | |
  | the rule | **distributed** | **distributed** | **distributed** | |

- **Read.**
  - No small set of heads carries the swap's effect; even all heads of the best layer together cut almost none of it.
- **Caveats.**
  - Gated DeltaNet layers have no heads (skipped on the 9B and 27B).
  - Mean ablation at the last token and the question tokens only.

### Does Zach's read window match ours? (51.5, opened 28 Oct 19:14) <a id="t51-5"></a>

*Used in: ledger only; planned Part V. Story: other datasets.*

- **Question.** On Zach's named-bridge passages, does each reader's read window end within 4 layers of ours?
- **Why we asked.** His swap works up to about L20; ours up to L16 on the 9B; the windows decide where the two operations can be compared.
- **Data.** Z1's passages, 200 per model (9B, 27B).
- **Method.** The whole change at the bridge name's last token, one layer at a time; the window's end is the last layer where a reader switches on at least 0.3.
- **Rule, fixed in advance.** "The same read window as ours if the last layer where each reader's switch >= 0.3 lies within 4 layers of ours."
- **Result.** (window ends, his / ours)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | lookup | L14 / L16 (-2)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| qwen35_9b_x51_5 :: L14 / L16 (-2) --> | L34 / L40 (-6)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| x51_5_27b :: L34 / L40 (-6) --> | not designed | not run |
  | recall | L18 / L14 (4)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| qwen35_9b_x51_5 :: L18 / L14 (4) --> | L34 / L32 (2)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| x51_5_27b :: L34 / L32 (2) --> | | |
  | the rule | **the same window** | **not the same** | | |

- **Read.**
  - On the 9B his passages are read over the same layers as our scenes; on the 27B the lookup's window ends 6 layers earlier.
- **Caveats.**
  - Our 27B window comes from a coarser grid (every 8th layer with L30-34).
  - Layer ends carry no interval.

### Does the lookup take a position route on Zach's passages? (Z3, opened 28 Oct 17:31) <a id="z3"></a>

*Used in: ledger only; planned Part V. Story: other datasets.*

- **Question.** On Zach's passages with scattered facts, does the lookup take a position route besides the identity route?
- **Why we asked.** The address codes where a locker sentence sits in a list; his passages have no list.
- **Data.** His level-0 passages with all three facts before the pointer: 60 (9B), 48 (Muse).
- **Method.** The routes test: the change comes from a passage where another item's fact sentence moved and took a new value; the lookup's answer is sorted into identity, position, value or original.
- **Rule, fixed in advance.** "Value <= 0.05; if position >= 0.2: the address exists in scattered-fact passages; if position <= 0.05: no position route in his layout."
- **Result.**

  | | 9B | 27B | Muse (L26) | Lightning |
  |---|---|---|---|---|
  | identity | 0.43 [0.30, 0.56]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.43 [0.30, 0.56] --> | not run | 0.19 [0.08, 0.31]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.19 [0.08, 0.31] --> | not run |
  | position | 0.10 [0.02, 0.19]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.10 [0.02, 0.19] --> | | 0.06 [0.00, 0.14]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.06 [0.00, 0.14] --> | |
  | value | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.00 [0.00, 0.00] --> | | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.00 [0.00, 0.00] --> | |
  | the rule | **in between** | | **in between** (L36: no position route) | |

- **Read.**
  - On his passages the lookup rarely takes the position route; it never takes the value.
- **Caveats.**
  - Small n (60 / 48); the lookup only.
  - 27B not run.

### Do the 9B's headline runs reproduce from a clean checkout? (49.5, landed 28 Oct 17:11) <a id="t49-5"></a>

*Used in: ledger only (a candidate for "How we checked"). Story: checks.*

- **Question.** Run again from one committed, clean tree, do the 9B's headline runs give the same stored answers?
- **Why we asked.** Every run of record ran from a dirty tree.
- **Data.** The 9B's main test (200), routes (300), only-U (300), zeroing (200) and the depth anatomy at L10 and L12 (200).
- **Method.** The same five commands in a fresh checkout; the stored per-item answers compared row by row.
- **Rule, fixed in advance.** None: descriptive, no prediction.
- **Result.** (9B; record / clean rerun)

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | main-test gap | 0.53<!-- src: docs/handcheck_clean49.md \| Main test gap :: 0.53 --> / 0.53<!-- src: docs/handcheck_clean49.md \| Main test gap :: 0.53 --> | not run | not run | not run |
  | depth anatomy: position share at L12 | 0.51<!-- src: docs/handcheck_clean49.md \| position share under the whole change at L12 :: 0.51 --> / 0.52<!-- src: docs/handcheck_clean49.md \| position share under the whole change at L12 :: 0.52 --> | | | |
  | rows identical | main test, routes, only-U, zeroing: all; anatomy: 38 of 11,988 differ | | | |

- **Read.**
  - Four of the five runs reproduce row for row; the anatomy differs on a few rows.
- **Caveats.**
  - The clean runs' own commit is marked dirty in the pack (90210687).
  - Source: docs/handcheck_clean49.md and results/checks/clean49_9b.json (point values, no intervals).

## Withdrawn

### Does the split hold when Zach's bridge is described? (Z2, opened 28 Oct 17:27; withdrawn 21:18) <a id="z2"></a>

*Used in: README Part VI, Withdrawn. Story: other datasets.*

- **Question.** On Zach's passages with a described (never named) bridge, does the lookup let go of the lens part?
- **Why we asked.** A described bridge must be computed before it can be used; the computed item could travel through the lens.
- **Data.** His described-bridge passages: 158 / 166 / 157 (below the 200 aimed for).
- **Method.** The conflict test at the description's last token at L, each reader its own change, against a random part.
- **Rule, fixed in advance.** "Per model, the 47.3 rule: (a) the split holds: gap >= 0.3, lookup <= 0.10; (a') the computed bridge is handed through the lens: lookup >= 0.20; (d) in between." Withdrawn by the answer control's rule ([51.12](#t51-12)): the lens effect there is the answer or mixed in all four cells.
- **Result.**

  | | 9B | 27B | Muse (L26) | Lightning |
  |---|---|---|---|---|
  | lookup: switches lost beyond a random part | 0.54 [0.43, 0.66]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| qwen35_9b_x50_z2 :: 0.54 [0.43, 0.66] --> | 0.69 [0.52, 0.87]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| x50_z2_27b :: 0.69 [0.52, 0.87] --> | 0.67 [0.00, 1.00]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| muse30_x50_z2 :: 0.67 [0.00, 1.00] --> | not run |
  | the rule (before withdrawal) | (a') through the lens | (a') through the lens | (a') through the lens | |

- **Read.**
  - Withdrawn: at the description's last token the lens part moves the answer, so removing it is not a test of the bridge.
- **Caveats.**
  - Muse's lookup switches under the whole change on 0.02 of passages.
  - n below the 200 aimed for.

## Running or sealed

Box times UTC, from `make queue-stats QUEUE=all` at 00:06 UTC on 29 Oct (low-high ends of the queue's estimate); the Lightning lanes follow batch 52 amendment 3.

### Where is the answer readable, and can it be written there? (batch 52 B, running) <a id="b52-b"></a>

- **Question.** At the bridge word, the earlier mention, the question and the last token, every second layer: are the bridge entity and the answer word lens-readable, and does writing the answer's lens directions there move the answer?
- **Status.** 12 jobs (read and write, 9B / 27B / Muse × main test / Zach's described passages); CPU plan `results/x52_answer_map/plan-20261028T234836Z`; the 9B's described-passage read has landed (`results/x52_answer_map/qwen35_9b_x52_read_z2`); the rest on mats and another. Rule fixed in advance in `jobs/c3/batch52.yaml` (B); no prediction.
- **Where used.** Ledger only.

### Batch 52 C: the rest of the coverage grid (running) <a id="b52-c"></a>

- **Question.** Fill the coverage table's missing cells on the 27B, Lightning, 9B and Muse.
- **Status.** Running: the 27B anatomy full grid (`jobs/c3/x47_8_27b.yaml`), the 27B token map (`jobs/c3/x47_d1_27b.yaml`), the 27B ladder steps 3-6 (`jobs/c3/x52_ladder_27b_a.yaml`), the 27B six lockers (`jobs/c3/x47_2_27b_r3.yaml`), the Muse ladder with step 6 inside Zach's band (`jobs/c3/x52_ladder_muse_r2.yaml`); Lightning's lanes per amendment 3 (the probe, routes, swap and lens readout now on speedup). Bolt: out of scope, only a J-lens exists, no J++ lens.
- **Where used.** The coverage table above.
