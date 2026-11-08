# Experiments ledger (depth)

*Every opened test of the depth report, on five models (the 122B where its source files hold a verdict), in the README's order: what was asked, what the rule fixed in advance said on each model, and where the README uses it.*

## In one minute

- **What it holds:** 63 sections in the README's Parts I-VI (the test cards, one check, one withdrawn card and one batch not completed in the sprint; counted by scripts/check_ledger.py), batch 53 (29 Oct) among them, on five models (the 9B, the 27B, Muse, Lightning, and the 122B, FP8, where it has a verdict), each tagged by how the README uses it; the one-model rows. VERIFIED.md (human recomputation) is not filled for any card; † marks what is not in the hand-checked sample (How to read).
- **The lookup goes around the lens part on every model run:** on Lightning at L14 it is blocked at 0.03 [-0.01, 0.08]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.45 :: 0.03 [-0.01, 0.08] --> of its switches beyond a random part while the recall is blocked at 0.34 [0.25, 0.44]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.94 :: 0.34 [0.25, 0.44] -->; on the 122B at L33, 0.00 [-0.06, 0.06]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PP :: 0.00 [-0.06, 0.06] --> against 0.32 [0.22, 0.41]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PM :: 0.32 [0.22, 0.41] --> ([conflict test](#lightning-conflict)). It reads an address a probe finds at the bridge word ([probe](#probe)) and a swap at dose 2 moves ([swap](#swap)); the swap's rule fixed in advance (dose 1) said no on every model. At the last token a probe on the lens part reads that address worse than random directions of the same energy, on all four models it ran on: the address is under-represented in the lens directions ([53.2](#b53-2)).
- **The recall follows the item, not its answer:** the answer control finds the item, or the answer word not read, on every model it ran on ([51.12](#t51-12)); pulled two ways by the lens part and the address, every model reads "both", the 27B and Muse barely ([53.6](#b53-6)).
- **Question order:** a small order effect on the 27B (lower bound +0.01<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: +0.01 -->, of the order of the 122B's rerun noise), none on the 122B; the other three missed the question-first gate ([53.1](#b53-1)).
- **Open questions:** near the output the last-token test is uninformative ([53.3](#b53-3), [53.3b](#b53-3b)); the pre-specified identity code says no on the 9B and the 27B and in between on Muse ([53.8](#b53-8)); two attention blocks carry part of Lightning's lookup, in between ([53.4](#b53-4)).
- **Withdrawn and rechecked:** The fact passages' described bridge is withdrawn ([Z2](#z2)); the named fact passages with made-up facts split on the 9B, also without the 60 passages that state the bridge's true value ([Z1](#z1)).

**Which test ran on which model, and what its rule said.** One table per Part, a row per test card, in the README's order; "in part" covers in between or in part; "–": not tested on that model (not run, not designed, or below its gate: the coverage table below says which). Lightning ○: its gate chosen after the 60-scene pre-check; ○ in a cell: post hoc (the 122B's gate lowered to 0.75, or its lookup-only gate, Dan 30 Oct). The 122B's cells from its coverage runs (FP8; MoE, ~10B active; L33), the agent's reading †.

<!-- verdicts:start (scripts/ledger_coverage.py verdicts; do not edit by hand) -->
**Part I. The two readers**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [Conflict test, main test](#lightning-conflict) | holds | in part: not confirmed | holds | holds | holds | yes | yes (view a) |
| [Item or answer, main test](#t51-12) | holds: the entity | holds: the entity | holds: answer not read | holds: answer not read | holds: answer not read | yes | yes (view b) |
| [Item or answer, the fact passages' true facts](#t51-12) | in part: mixed | in part: mixed | – | in part: mixed | – | yes | yes (view b) |
| [Item or answer, the fact passages' made-up facts](#t51-12) | in part: mixed | in part: mixed | – | – | – | yes | yes (view b) |
| [Split in prose, JSON, tables](#x0b) | holds | holds | holds | holds | in part: mixed | yes | no |
| [Split in natural passages](#x5) | holds ○ | in part: mixed | holds | – | holds | yes | no |
| [Each part added by itself](#t51-1) | holds: (i), (ii) yes | in part: (i) no | holds: (i), (ii) yes | in part: (ii) no | holds: (i), (ii) yes | yes | no |
| [Zeroing at one layer](#t47-5) | holds: not needed | holds: not needed | holds: not needed | holds: not needed | holds: not needed | yes | no |
| [The lens part removed step by step (more layers, the earlier mention)](#t49-2) | in part: (b) no | in part: (a), (b) no | in part: (a), (b) no | – | in part: (a), (b) no | yes | no |
| [The item's earlier mention](#t45p) | holds: yes | holds: yes | holds: yes | – | **fails: no** | yes | no |
| [Lens identity vs address](#b53-6) | in part: both | in part: both | in part: both | in part: both | – | yes | no |
| [Question order, number answer](#b53-1) | – | **fails: order matters** | – | – | holds: order-free | yes | no |
| [Gain map: weight or route](#t49-1) | **fails: neither** | **fails: neither** | **fails: neither** | **fails: neither** | **fails: neither** | yes | no |
| [Two learned subspaces](#t48-1) | **fails: no** | **fails: no** | **fails: no** | – | – | yes | no |
| [Inside the lens part](#b52-a) | descriptive: bridge words | descriptive: bridge words | descriptive: bridge words | descriptive: bridge words | descriptive: bridge words | descriptive | no |
| [Answer readable, usable](#b52-b) | descriptive | descriptive | descriptive | descriptive: ours only | descriptive | yes | no |

**Part II. Identity**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [Identity route outside the lens](#t47-1) | holds: outside | holds: outside | holds: outside | holds: outside | – | yes | no |
| [Routes test and the address](#routes) | holds: both routes | in part: adding: no | holds: both routes | holds: both routes | – | yes | yes (view c) |
| [Never the value, by format](#t47-7c) | in part: incomplete | in part: incomplete | in part: incomplete | in part: incomplete | – | yes | no |
| [Learned subspaces at scale](#t51-3) | in part: (iii) no | in part: (iii) no | in part: (iii) no | – | – | yes (part descriptive) | no |
| [Shared identity code](#b53-8) | **fails: no** | **fails: no** | in part: in between | – | – | yes | no |

**Part III. The address**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [Address probe](#probe) | descriptive: readable | descriptive: readable | descriptive: readable | descriptive: readable | descriptive: readable | post hoc | no |
| [Address swap, rule at dose 1](#swap) | **fails: no** | **fails: no** | **fails: no** | **fails: no** | – | yes | yes (view d) |
| [Swap after neutral sentences](#t47-16) | holds: robust | holds: robust | holds: robust | holds: robust | **fails: none of three ○** | yes | no |
| [Six lockers, own code each](#six) | holds: own code | **fails: none of three** | holds: own code | holds: own code | holds: own code | yes | no |
| [What the address is](#t51-11) | in part: in between | in part: part 2 only | in part: mixed | – | – | yes | no |
| [Address, 27B position scenes](#b53-5) | holds: pattern holds | **fails: differs** | – | – | – | yes | no |
| [Lens readout of the swap](#t47-0) | holds: lens blind | holds: lens blind | holds: lens blind | holds: lens blind | holds: lens blind ○ | descriptive | no |
| [Probes on the lens subspace](#b53-2) | holds: lens blind | in part: in between | holds: lens blind | in part: in between | holds: lens blind | yes | no |
| [Report prompt](#t47-10) | – | **fails: neither** | – | – | – | yes | no |
| [Report of slot 1, reworded](#t49-6) | **fails: recovers** | **fails: recovers** | – | **fails: recovers** | – | yes | no |
| [A few heads take the swap](#t51-2) | **fails: distributed** | **fails: distributed** | **fails: distributed** | **fails: distributed** | – | yes | no |
| [Attention follows the swap](#t49-7) | **fails: neither** | **fails: neither** | **fails: neither** | **fails: neither** | – | yes | no |
| [Chained addresses](#t47-14) | **fails: no** | **fails: no** | **fails: no** | – | **fails: no** | yes | no |
| [Address refit per format](#x45d) | holds: refit works | in part: neither | holds: refit works | holds: refit works | – | yes | no |
| [Address in code, tool output](#b53-7) | in part | in part | – | – | descriptive: readable ○ | yes (part descriptive) | no |

**Part IV. Where and when**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [Split by sentence order](#order) | descriptive: by order | descriptive: by order | descriptive: by order | descriptive: by order | descriptive: by order | post hoc | yes (view g) |
| [Copy test, locker after](#t45q) | holds: yes | holds: yes | holds: yes | – | – | yes | no |
| [Token-by-layer map](#d1) | **fails: (a)-(c) no** | **fails: (a)-(c) no** | **fails: (a)-(c) no** | **fails: (a)-(c) no** | – | yes | no |
| [Lookups read before L](#t47-4) | descriptive: before L | descriptive: before L | descriptive: before L | descriptive: before L | descriptive: before L | descriptive | no |
| [Anatomy by depth, handoff](#t47-8) | holds: (a) yes | **fails: (a) no** | holds: (a) yes | holds: (a) yes | holds: (a) yes ○ | yes | no |
| [Address at the last token](#t51-4) | **fails: not there** | **fails: not there** | holds: travels | in part: in between | – | yes | no |
| [Entity at the last token](#t51-10) | in part: read, not used | in part: read, not used | in part: read, not used | in part: read, not used | in part: read, not used | yes | yes (view f) |
| [Last token: the lookup's read](#b53-3) | descriptive: in between | descriptive: in between | descriptive: outside | descriptive: outside | descriptive: in between | yes | no |
| [Last token, word answers](#b53-3b) | in part: in between | in part: in between | – | – | – | yes | no |
| [Lightning's attention blocks](#b53-4) | – | – | – | in part: in between | – | yes | no |

**Part V. Other datasets**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [The fact passages, true facts](#z1) | **fails: lookup follows** | **fails: lookup follows** | **fails: follows, few** | in part: in between | in part: in between | yes | yes (view e) |
| [The fact passages, made-up facts](#z1) | holds | in part: in between | – | – | holds | yes | yes (view e) |
| [Named vs described bridge](#b53-1b) | – | descriptive: mixed / answer | – | – | – | yes | no |
| [Full carrier up to L](#t51-7) | in part: in between | in part: in between | – | in part: in between | – | yes | no |
| [Position route, the fact passages](#z3) | in part: in between | **fails: no position** | in part: in between | in part: in between | **fails: no position** | yes | no |
| [Read window, the fact passages](#t51-5) | holds: same window | **fails: not the same** | – | holds: same window | – | yes | no |

**Part VI. What did not hold**

| test | 9B | 27B | Muse | Lightning ○ | 122B | rule fixed in advance? | hand-checked? |
|---|---|---|---|---|---|---|---|
| [Described bridge](#t47-3) | holds | **fails: through lens** | holds | – | – | yes | no |
| [One question, two instructions](#t47-15) | – | **fails: neither** | – | – | – | yes | no |
| [Errors are address errors](#t47-13) | **fails: no** | – | **fails: no** | **fails: no** | – | yes | no |
| [Lens part keys the attribute](#t48-2) | **fails: no** | **fails: no** | **fails: no** | **fails: no** | – | yes | no |
| [Person mark at the locker](#t48-3) | **fails: no** | **fails: no** | **fails: no** | – | – | yes | no |
| [Pooled person probe](#t49-3) | **fails: neither** | in part: in between | **fails: neither** | – | – | yes | no |
| [Copying heads pass the rest](#t48-4) | **fails: no** | **fails: no** | **fails: no** | **fails: no** | – | yes | no |
| [Address as the recall's route](#t48-5) | **fails: no** | **fails: no** | **fails: no** | – | – | yes | no |
| [Blocking the pick sentence](#t47-6) | **fails: no** | **fails: no** | **fails: no** | – | – | yes | no |
| [Same address, any item](#t47-11) | **fails: no** | **fails: no** | **fails: no** | **fails: no** | – | yes | no |
<!-- verdicts:end -->

## How to read

The README's [methods, measures and figure marks](README.md#how-to-read-this-page) hold here unchanged: the change, the lens part, a random part, switches blocked beyond a random part, L, the identity and position routes, the address, whiskers 95%, hollow = after the data. Each card follows the README's card template (Question, Why we asked, Data, Method, the figure, Rule fixed in advance quoted, Result with one column per model, Read, Caveats), with no interpretation beyond the verdict. Internal test ids appear in the card headings only. Opened times are the opening commit's time (Paris, 28 Oct unless stated); box times are UTC.

New in this ledger:

- **Tags** on the line under each heading (the sprint's `changes README` tag is retired: its README changes were applied or are listed in [the operations log](../review/ledger_ops_2026-10.md#readme-changes)): `in README` (a README card or claim uses it as is), `ledger only` (not in the README), `below gate: <model>` (that model's readers missed the test's gate, so its column is not tested, or later an exploratory run shown hollow).
- **†**: not in the hand-checked sample (the README's mark). VERIFIED.md (human recomputation) is not filled for any card.
- **Terms**: the **ladder** (49.2) takes the lens part out step by step (more layers, the earlier mention, the question, every token), each step (rung) against a random part; the **full carrier** (51.7) changes the bridge token at every layer up to L on the fact passages. In verbatim rules and their verdict words, each "J-space" or "pointer" carries a bracketed gloss: [the lens's directions] or [pointer: the address].
- **Below gate**: a test runs on a model only if both readers answer the original prompts right often enough (usually 0.80); a failed gate is not lowered after the data (the spec's rule). Lightning's below-gate runs (Dan, 29 Oct morning) are exploratory: hollow marks, never in claims or grades.
- **Adapted design**: where a model needed a changed design (Lightning: attention blocks only after L14, no per-block MLP; the 27B's grids), the card's Data or Method says so.
- **The 122B** (Qwen3.5-122B-A10B; FP8; MoE, ~10B active): a fifth column where a verdict exists, from its source files, no reruns (Dan, 29 Oct 11:30); "not run" elsewhere; a fifth slot only in the figures of those cards. Its L33 is the 27B's relative depth carried over (33/48), not the other models' rule; its J++ lens was fit on the bf16 weights; FP8; MoE, ~10B active.
- **Coverage run**: a test run on a model it was not designed for (the 27B or Lightning, 28-29 Oct), on the same rule fixed in advance, with no prediction committed.
- **Lightning's gate**: the main test's gate on all 516 scenes, chosen after the 60-scene pre-check was seen (○ in the tables; hollow marks on its figures); layer L14 ([Lightning's layer](#lightning-layer)). Nemotron 3.5 Bolt is out of scope (only a J-lens exists, no J++ lens).

`uv run python scripts/check_ledger.py` checks every cited path, anchor, field, tag, figure position and the coverage table, and that every sourced number stands on one line of its file (tests/test_experiments_ledger.py).

## Part I. The two readers: lookup and recall

### Does the conflict test hold on Lightning? <a id="lightning-conflict"></a>

`in README` *Used in: README Part I card "In a conflict, which part of the bridge word does each reader follow?" (Lightning's and the 122B's columns).*

Test Lightning conflict test · opened 29 Oct · status: rule fixed in advance · hand-check: in sample (view a) · files: `results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md` · recompute: `scripts/x0_necessity.py` (the command in its docstring) · also: UTC

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On Nemotron 3.5 Lightning, at its committed layer L14, does the recall follow the lens part while the lookup goes around it?
- **Why we asked.** A fourth model, of another family, under the main test's rule unchanged. The 122B (FP8; MoE, ~10B active) beside: the largest model, its conflict test from its r2 run (24 Oct; Dan 11:30, the 122B as a fifth model).
- **Data.** Main test, 200 scenes (the 60 scenes used to pick the layer excluded); ○ gate chosen after the 60-scene pre-check was seen: the main test's gate on all 516 scenes passed (lookup 0.957, recall 0.816). The 122B: the main test at L33, 200 scenes, its gate passed.
- **Method.** The conflict test at the bridge word at each of 13 swept layers (L2 to L50), decided at L14: without the lens part, against without a random part of the same share.

![On Lightning the recall follows the lens part; the lookup does not](../../figures/depth/readme/02_one_layer_split.png)

*Switches blocked without the lens part beyond a random part, lookup and recall per model, main test at L (the 122B's L33: the 27B's relative depth carried over); right: the gap, recall minus lookup, with its 95% interval; grey band: within 0.10 of random (the lookup's bar).*

- **Rule, fixed in advance.** The main test's: "confirmed if the lookup has at most 0.10 blocked beyond random and the recall has at least 0.30 blocked of its switches without the lens part; killed if the lookup has at least 0.20 blocked or the recall under 0.20." Coverage run on an already-scored rule: no prediction.

</details>

- **Result.** (L14)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recall: switches blocked beyond a random part | see the README | | | 0.34 [0.25, 0.44]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.94 :: 0.34 [0.25, 0.44] --> | 0.32 [0.22, 0.41]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PM :: 0.32 [0.22, 0.41] --> (L33) |
  | recall: switches blocked, not net of random | | | | 0.41 [0.32, 0.50]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.94 :: 0.41 [0.32, 0.50] --> | 0.40 [0.30, 0.49]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PM :: 0.40 [0.30, 0.49] --> |
  | lookup: switches blocked beyond a random part | | | | 0.03 [-0.01, 0.08]<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.45 :: 0.03 [-0.01, 0.08] --> | 0.00 [-0.06, 0.06]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PP :: 0.00 [-0.06, 0.06] --> |
  | lookup: switches under the whole change | | | | 0.45<!-- src: results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md \| 0.03 [-0.01, 0.08] :: 0.45 --> | 0.45<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| 33 :: PP :: 200 :: 0.45 --> |
  | the rule | | | | **confirmed** (lookup around, recall through) | **CONFIRMED at layer 33<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| chat :: CONFIRMED at layer 33 -->** (lookup around, recall through) |
  | lookup with the lens part at k = 25 / 50 / 100 directions (descriptive) | | | | | 0.00 [-0.06, 0.06]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| jpp :: signed :: PP :: 0.00 [-0.06, 0.06] --> / -0.02 [-0.09, 0.05]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| jpp :: signed :: PP :: -0.02 [-0.09, 0.05] --> / -0.12 [-0.22, -0.04]<!-- src: results/x0_necessity/qwen35_122b_x0_necessity_r2/verdict-20261024T171509Z/verdict.md \| jpp :: signed :: PP :: -0.12 [-0.22, -0.04] --> |

- **Read.**
  - The rank check (range per model; every item of the conflict test and the routes test, docs/review/verify_pack_jspace.md; no flag): what the lens can read about the item sits in the lens part; the rest puts the new bridge word in the lens's top 50 on 0.00-0.14 of items (conflict test: 9B 0.00<!-- src: docs/review/verify_pack_jspace.md \| Qwen3.5-9B :: S's bridge (word or symbol) :: 0.00 -->, 27B 0.02<!-- src: docs/review/verify_pack_jspace.md \| Qwen3.6-27B :: S's bridge (word or symbol) :: 0.02 -->, Muse 0.01, Lightning 0.06, 122B 0.05; the routes test's highest condition, Lightning C0: 0.14), against about 0.5 for a random part (0.52 / 0.53 / 0.66 / 0.65 / 0.83) and about 0.8 for the lens part (0.81 / 0.81 / 0.89 / 0.93 / 0.93); the random part reads the bridge because it keeps part of Δ itself.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  On the clean one-pick scenes Lightning misses the gate (recall 0.751<!-- src: results/x0_necessity/nem35l_x52_fresh/coverage.txt | (recall 0.751 :: 0.751 --> < 0.80), so it is not tested there; the below-gate run on the eligible scenes (295 at L14; the source of Lightning's below-gate runs) is descriptive only, hollow ○: recall ○ 0.39 [0.33, 0.45]<!-- src: results/x0_necessity/nem35l_x52_fresh/verdict-20261029T083122Z/verdict.md | PM | 295 :: 0.39 [0.33, 0.45] -->, lookup ○ 0.03 [-0.02, 0.08]<!-- src: results/x0_necessity/nem35l_x52_fresh/verdict-20261029T083122Z/verdict.md | PP | 295 :: 0.03 [-0.02, 0.08] --> blocked beyond a random part, the pattern the rule calls confirmed.

More from the reading:

  - On the 122B, at its L33, the lookup has nothing blocked beyond random and the recall has about a third blocked: confirmed; with more lens directions (k = 50, 100) the lookup still has nothing blocked beyond random.
  - At L14 the recall follows the lens part and the lookup does not; the same split stands at L18 and L22.

- **Caveats.**
  - The 122B: its L33 is the 27B's relative depth carried over (33/48), not the other models' rule; its J++ lens was fit on the bf16 weights; FP8; MoE, ~10B active.
  - The clean one-pick numbers are below gate, exploratory: never in claims or grades (Dan, 09:15 and 09:50).
  - The gate was chosen after the 60-scene pre-check had failed (accepted by Dan 01:10).
  - From L26 on the lookup switches on 0.02 of scenes or fewer, so those layers cannot tell.

</details>

### Is it the bridge item or its answer that moves through the lens? <a id="t51-12"></a>

`in README` *Used in: README Part I card "In a conflict, which part of the bridge word does each reader follow?" (the specificity rows); README "Tested and dropped" ("The described bridge on the fact passages").*

Test 51.12 · opened 28 Oct · status: rule fixed in advance · hand-check: in sample (view b) · files: `results/x51_answer/x52_answer-20261029T082417Z/verdict.md` · recompute: `scripts/x51_answer.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the main test, is the recall's drop without the lens part about the bridge item or about its answer word?
- **Why we asked.** At a described bridge the lens reads the answer about as well as the item; the same could hold at our bridge word.
- **Data.** Main test, 200 per model (Lightning at L14: a coverage run, no prediction; the 122B (FP8; MoE, ~10B active) at L33: a coverage run on the same rule, Dan 11:30, no prediction).
- **Method.** At the bridge word at L: (1) without the lens part; (2) without the lens part but keeping its directions for both readers' answer words (number words); (3) without those answer directions only; each against a random part of its share; the lens's rank of the answer word at the bridge word first.

- **Rule, fixed in advance.** (Amended 20:20, before opening.) "The lens effect is the entity: arm 2 keeps >= 0.7 of arm 1's extra drop and arm 3 costs <= 0.10 beyond random. The lens effect is the answer: arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed." First: "the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)".

The three arms side by side, per model:

![The recall's drop without the lens part is the item, not its answer](../../figures/depth/ledger/01_item_not_answer.png)

*The answer control, main test: the recall's switches blocked beyond a random part of the same size without the lens part, with the lens part removed but the answer word's directions kept, and with only the answer word's directions removed, one lane each per model. Whiskers 95% intervals; Lightning and the 122B hollow ○ (after the data).*

</details>

- **Result.** (recall)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (1) switches blocked beyond a random part | 0.50 [0.41, 0.57]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.50 [0.41, 0.57] --> | 0.74 [0.66, 0.80]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.74 [0.66, 0.80] --> | 0.76 [0.62, 0.88]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| arms beside: the lens effect is the entity :: 0.76 [0.62, 0.88] --> | 0.34 [0.25, 0.44]<!-- src: results/x51_answer/x52_answer-20261029T002056Z/verdict.md \| nemotron-3.5-lightning :: 0.34 [0.25, 0.44] --> | 0.27 [0.17, 0.38]<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 0.27 [0.17, 0.38] --> (L33) |
  | (2) / (1): effect remaining with the answer directions retained | 0.95 [0.90, 0.99]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.95 [0.90, 0.99] --> | 0.93 [0.85, 0.99]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| the lens effect is the entity :: 0.93 [0.85, 0.99] --> | 0.93 [0.85, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| arms beside: the lens effect is the entity :: 0.93 [0.85, 1.00] --> | 0.92 [0.83, 1.03]<!-- src: results/x51_answer/x52_answer-20261029T002056Z/verdict.md \| nemotron-3.5-lightning :: 0.92 [0.83, 1.03] --> | 0.98 [0.86, 1.18]<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 0.98 [0.86, 1.18] --> |
  | (3) without the answer directions only, beyond random | 0.00 [0.00, 0.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.47 [0.39, 0.55] :: 0.00 [0.00, 0.00] --> | 0.03 [0.01, 0.05]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.69 [0.59, 0.77] :: 0.03 [0.01, 0.05] --> | -0.01 [-0.05, 0.03]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.71 [0.56, 0.84] :: -0.01 [-0.05, 0.03] --> | 0.00 [-0.02, 0.01]<!-- src: results/x51_answer/x52_answer-20261029T002056Z/verdict.md \| nemotron-3.5-lightning :: 0.00 [-0.02, 0.01] --> | 0.01 [-0.01, 0.04]<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 0.01 [-0.01, 0.04] --> |
  | answer word outside the lens's top 50 | 0.56 [0.47, 0.66]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.50 [0.41, 0.57] :: 0.56 [0.47, 0.66] --> | 0.79 [0.72, 0.86]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.74 [0.66, 0.80] :: 0.79 [0.72, 0.86] --> | 0.99 [0.98, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| 0.76 [0.62, 0.88] :: 0.99 [0.98, 1.00] --> | 0.95 [0.90, 0.99]<!-- src: results/x51_answer/x52_answer-20261029T002056Z/verdict.md \| nemotron-3.5-lightning :: 0.95 [0.90, 0.99] --> | 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 1.00 [1.00, 1.00] --> |
  | the rule | **the entity** | **the entity** (post hoc: mixed, (a) +0.040 [0.006, 0.082]<!-- src: results/answer_control_translated/20261030T222840Z/tables.md \| qwen3.6-27b :: arm3 any language :: +0.040 [0.006, 0.082] -->) | **the answer word is not read** (arms beside, post hoc: mixed; answer in any language (single-token translations); 9B, 27B, Muse; Lightning and 122B not run; (a) +0.085 [0.018, 0.154]<!-- src: results/answer_control_translated/20261030T222840Z/tables.md \| muse-glimmer-30b :: arm3 any language :: +0.085 [0.018, 0.154] -->) | **the answer word is not read** (arms beside: the entity) | **the answer word is not read at the bridge word<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: recall :: the answer word is not read at the bridge word -->** (arms beside: the entity; the lookup's answer word not read either, its effect 0.01 [-0.06, 0.08]<!-- src: results/x51_answer/x52_answer-20261029T112359Z/verdict.md \| qwen3.5-122b-a10b :: lookup :: 0.01 [-0.06, 0.08] -->) |

- **Read.**
  - On the 122B, as on Lightning and Muse, the recall's answer word is not read at the bridge word, so that is its label; the arms beside give the entity pattern (post hoc, with the answer directions in any language: mixed on the 27B and Muse, the item on the 9B; the shift of the retained-directions arm is explained by the number of directions).

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The recall's drop without the lens part is the item's: keeping the answer's lens directions keeps almost all of it, and those directions alone cost nothing.
  - On Lightning the answer word is not read at the bridge word for either reader; its lookup has too little blocked without the lens part to split into arms.
  - On the named fact passages with true facts (coverage runs, no prediction) the same arms say mixed for both readers on the 9B, the 27B and Lightning: keeping the answer's directions keeps 0.21<!-- src: results/x51_answer/x52_answer-20261029T081754Z/verdict.md | z1k :: qwen3.5-9b :: recall :: 0.21 --> (9B), 0.29<!-- src: results/x51_answer/x52_answer-20261029T081240Z/verdict.md | z1k :: qwen3.6-27b :: recall :: 0.29 --> (27B) and 0.29<!-- src: results/x51_answer/x52_answer-20261029T081239Z/verdict.md | z1k :: nemotron-3.5-lightning :: recall :: 0.29 --> (Lightning) of the recall's drop. On the made-up-fact passages the 9B's lookup cannot tell (no extra drop beyond random) and its recall is mixed; on the 27B the answer word is not read at the bridge word for the lookup (rank above 50 on 0.91 [0.86, 0.94]<!-- src: results/x51_answer/x52_answer-20261029T082432Z/verdict.md | z1p :: qwen3.6-27b :: lookup :: 0.91 [0.86, 0.94] --> of items) and the recall is mixed (results/x51_answer/x52_answer-20261029T082417Z/verdict.md). Muse not run; the made-up-fact half on Lightning is not tested (its source run missed the gate; results/x51_answer/x52_answer-20261029T081355Z/verdict.md).

- **Caveats.**
  - The 122B: a coverage run (results/x51_answer/x52_answer-20261029T112359Z), no prediction; its L33 carried over from the 27B's relative depth, FP8 weights, its J++ lens fit in bf16 (see How to read).
  - Digits are not in the lens dictionary, so the answer directions are number words; the pre-amendment runs are kept, superseded.
  - On the fact passages' described bridge the same control finds the answer, not the item (see [Z2](#z2)).

</details>

### At which layer does Lightning get the conflict test? <a id="lightning-layer"></a>

`in README` *Used in: README "The question and the setup" (Lightning's layer).*

Test Lightning's layer · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_lightning/nem35l_x52_layer_r2/prereq.md` · recompute: `scripts/x51_lightning.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At which layer does Nemotron 3.5 Lightning get the conflict test?
- **Why we asked.** A new model needs its layer L fixed before any scored run.
- **Data.** 60 dev scenes of the main test (excluded from the conflict test).
- **Method.** The whole change at the bridge word at every 4th layer (L2 to L50); each reader's switch rate; the bridge word's lens readability recorded as the tie-break.

- **Rule, fixed in advance.** Batch 52 amendment 1 (Dan ~00:50, before the sweep): "earliest layer passing the gate at relative depth ≥ 0.25; tie-break = highest lens readability of the bridge word." Passing = both readers switch on at least 0.3 (the published rule). ○ Gate chosen after the 60-scene pre-check was seen.

The sweep that picked the layer:

![Lightning's layer sweep and the conflict test by layer](../../figures/depth/ledger/02_lightning_layers.png)

*Lightning's layer sweep on the pre-check scenes: the share of each reader's answers switched by the whole change at the bridge word, lookup (violet) and recall (black), at every swept layer; dashed: the bar both readers must reach. All estimates post hoc (the gate was chosen after the pre-check).*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | the layer | L12 | L32 | L26 | **L14** (depth 0.27) | L33 (the 27B's relative depth carried over, 33/48; its conflict test per layer in the figure's bottom panel) |
  | lookup switch at L14 | | | | 0.58 [0.45, 0.73]<!-- src: results/x51_lightning/nem35l_x52_layer_r2/prereq.md \| L14 (pick) :: 0.58 [0.45, 0.73] --> | |
  | recall switch at L14 | | | | 0.98 [0.94, 1.00]<!-- src: results/x51_lightning/nem35l_x52_layer_r2/prereq.md \| L14 (pick) :: 0.98 [0.94, 1.00] --> | |

- **Read.**
  - L14 is the earliest layer at depth 0.25 or more where both readers switch on at least 0.3 of scenes.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 60-scene pre-check failed (lookup 0.883, recall 0.783); the main test's gate on all 516 scenes decided (accepted by Dan 01:10).
  - `layer.json`'s "rule" field holds the prerequisite text, not amendment 1's pick rule.

</details>

### Does the split hold in prose, JSON and tables? <a id="x0b"></a>

`in README` *Used in: README Part I card "Does the split hold in other texts?" (the varied scenes).*

Test x0b · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md` · recompute: `scripts/x0b_generalize.py` (the command in its docstring) · also: varied scenes; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** In scenes written as prose, JSON or a table, at three nesting levels and in several domains, does the lookup let go of the lens part while the recall follows it?
- **Why we asked.** The main test is one template; the split could belong to that layout rather than to the two readers.
- **Data.** Varied scenes, at most 40 per cell, only cells that pass the gate: 36 of 51<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| Gate per cell :: 36 of 51 --> / 49 of 51<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| Gate per cell :: 49 of 51 --> / 44 of 57<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| Gate per cell :: 44 of 57 --> / 42 of 57<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| Gate per cell :: 42 of 57 --> cells, 1010<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| Gate per cell :: 1010 --> / 1635<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| Gate per cell :: 1635 --> / 1388<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| Gate per cell :: 1388 --> / 1105<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| Gate per cell :: 1105 --> scenes (9B / 27B / Muse / Lightning).
- **Method.** The conflict test unchanged, at L: without the lens part (25 directions), against without a random part of the same share; pooled over the cells.

![The split carries over to other texts](../../figures/depth/readme/s01_split_all_scene_sets.png)

*Every scene set, one panel per model (the 9B, the 27B, Muse, the 122B): per set (rows), the switches blocked without the lens part beyond a random part of the same size, lookup (violet) and recall (black), joined in each row. Whiskers: 95% intervals. All estimates post hoc.*

- **Rule, fixed in advance.** "Holds iff lookup excess <= 0.1 (upper CI <= 0.2) and C >= 0.2 (lower CI >= 0.1); fails iff lookup excess >= 0.2 or C's upper CI < 0.1." (C: the recall's extra drop minus the lookup's.) Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.** (pooled over the cells, at L)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup: switches blocked beyond a random part | 0.01 [-0.01, 0.03]<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| 1010 :: around :: 0.01 [-0.01, 0.03] --> | 0.08 [0.06, 0.10]<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| 1635 :: around :: 0.08 [0.06, 0.10] --> | 0.06 [0.03, 0.10]<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| 1388 :: around :: 0.06 [0.03, 0.10] --> | 0.03 [0.00, 0.05]<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| 1105 :: around :: 0.03 [0.00, 0.05] --> | -0.02 [-0.03, -0.00]<!-- src: results/x0b_generalize/qwen35_122b_x0b_v2/verdict-20261025T015139Z/verdict.md \| 33 :: PP :: 852 :: -0.02 [-0.03, -0.00] --> |
  | recall: the same | 0.23 [0.14, 0.33]<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| 1010 :: mixed :: 0.23 [0.14, 0.33] --> | 0.56 [0.50, 0.61]<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| 1635 :: through :: 0.56 [0.50, 0.61] --> | 0.56 [0.48, 0.66]<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| 1388 :: through :: 0.56 [0.48, 0.66] --> | 0.26 [0.20, 0.34]<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| 1105 :: mixed :: 0.26 [0.20, 0.34] --> | 0.13 [0.11, 0.16]<!-- src: results/x0b_generalize/qwen35_122b_x0b_v2/verdict-20261025T015139Z/verdict.md \| 33 :: PM :: 852 :: 0.13 [0.11, 0.16] --> |
  | the gap, recall minus lookup | 0.22 [0.14, 0.31]<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| pooled: HOLDS :: 0.22 [0.14, 0.31] --> | 0.47 [0.42, 0.53]<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| pooled: HOLDS :: 0.47 [0.42, 0.53] --> | 0.50 [0.40, 0.61]<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| pooled: HOLDS :: 0.50 [0.40, 0.61] --> | 0.24 [0.17, 0.32]<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| pooled: HOLDS :: 0.24 [0.17, 0.32] --> | 0.15 [0.12, 0.18]<!-- src: results/x0b_generalize/qwen35_122b_x0b_v2/verdict-20261025T015139Z/verdict.md \| 33 :: PM :: 852 :: 0.15 [0.12, 0.18] --> |
  | the rule, pooled | **HOLDS<!-- src: results/x0b_generalize/qwen35_9b_x0b_v2/verdict-20261024T182331Z/verdict.md \| pooled :: HOLDS -->** | **HOLDS<!-- src: results/x0b_generalize/x0b_v2_27b/verdict-20261024T192113Z/verdict.md \| pooled :: HOLDS -->** | **HOLDS<!-- src: results/x0b_generalize/muse30b_x0b_v2/verdict-20261026T022534Z/verdict.md \| pooled :: HOLDS -->** | **HOLDS<!-- src: results/x0b_generalize/nem35l_x52_x0b/verdict-20261029T014520Z/verdict.md \| pooled :: HOLDS -->** (no prediction) | **MIXED<!-- src: results/x0b_generalize/qwen35_122b_x0b_v2/verdict-20261025T015139Z/verdict.md \| X0b's rule at layer 33, pooled :: MIXED -->** (852 scenes) |

- **Read.**
  - The 122B (FP8; MoE, ~10B active; its L33 carried over from the 27B): mixed, its recall's drop beyond random small (the rule's C under 0.2).

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - In prose, JSON and tables the recall follows the lens part and the lookup does not, on all four models, Lightning included.

- **Caveats.**
  - Only cells that pass the gate count; about a quarter of Lightning's and Muse's cells fail it.
  - Muse's scene count is 1,388 here and 1,389 in the README (Flagged 6).

</details>

### Does the split hold in natural passages? <a id="x5"></a>

`in README` `below gate: Lightning` *Used in: README Part I card "Does the split hold in other texts?" (the natural passages).*

Test x5 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md` · recompute: `scripts/x5_natural.py` (the command in its docstring) · also: natural passages, opened 25-26 Oct; Lightning's gate 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** In natural passages, where a fact sentence names the bridge, does the lookup let go of the lens part while the recall follows it?
- **Why we asked.** Our scenes are templates; natural passages test the split outside them.
- **Data.** Natural passages: 83<!-- src: results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md \| 83 items :: 83 --> / 137<!-- src: results/x5_natural/x5_natural_27b/verdict-20261024T232738Z/verdict.md \| 137 items :: 137 --> / 60<!-- src: results/x5_natural/muse30b_x5_natural/verdict-20261026T023226Z/verdict.md \| 60 items :: 60 --> items (9B / 27B / Muse); the 9B's gate was lowered after the data. Lightning not tested: its gate failed, and by the spec's rule there is no lowered rerun.
- **Method.** The conflict test unchanged, at L: without the lens part, against without a random part of its share; the gap is the recall's drop minus the lookup's.

![The split carries over to other texts](../../figures/depth/readme/s01_split_all_scene_sets.png)

*Every scene set, one panel per model (the 9B, the 27B, Muse, the 122B): per set (rows), the switches blocked without the lens part beyond a random part of the same size, lookup (violet) and recall (black), joined in each row. Whiskers: 95% intervals. All estimates post hoc.*

- **Rule, fixed in advance.** "gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup: switches blocked beyond a random part | 0.03 [-0.08, 0.15]<!-- src: results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md \| Lookup excess :: 0.03 [-0.08, 0.15] --> | 0.32 [0.20, 0.45]<!-- src: results/x5_natural/x5_natural_27b/verdict-20261024T232738Z/verdict.md \| Lookup excess :: 0.32 [0.20, 0.45] --> | -0.20 [-0.55, 0.00]<!-- src: results/x5_natural/muse30b_x5_natural/verdict-20261026T023226Z/verdict.md \| Lookup excess :: -0.20 [-0.55, 0.00] --> | ○ -0.08 [-0.27, 0.00]<!-- src: results/x5_natural/nem35l_x52_natural_below/verdict-20261029T082128Z/verdict.md \| Lookup excess :: -0.08 [-0.27, 0.00] --> | -0.11 [-0.20, -0.03]<!-- src: results/x5_natural/qwen35_122b_x5_natural/verdict-20261025T005420Z/verdict.md \| Lookup excess :: -0.11 [-0.20, -0.03] --> |
  | recall: the same | 0.56 [0.45, 0.66]<!-- src: results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md \| recall excess :: 0.56 [0.45, 0.66] --> | 0.59 [0.50, 0.67]<!-- src: results/x5_natural/x5_natural_27b/verdict-20261024T232738Z/verdict.md \| recall excess :: 0.59 [0.50, 0.67] --> | 0.75 [0.62, 0.86]<!-- src: results/x5_natural/muse30b_x5_natural/verdict-20261026T023226Z/verdict.md \| recall excess :: 0.75 [0.62, 0.86] --> | ○ 0.49 [0.31, 0.67]<!-- src: results/x5_natural/nem35l_x52_natural_below/verdict-20261029T082128Z/verdict.md \| recall excess :: 0.49 [0.31, 0.67] --> | 0.34 [0.24, 0.43]<!-- src: results/x5_natural/qwen35_122b_x5_natural/verdict-20261025T005420Z/verdict.md \| recall excess :: 0.34 [0.24, 0.43] --> |
  | the gap | 0.52 [0.36, 0.68]<!-- src: results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md \| Rule:  :: 0.52 [0.36, 0.68] --> | 0.27 [0.13, 0.41]<!-- src: results/x5_natural/x5_natural_27b/verdict-20261024T232738Z/verdict.md \| Rule:  :: 0.27 [0.13, 0.41] --> | 0.95 [0.64, 1.33]<!-- src: results/x5_natural/muse30b_x5_natural/verdict-20261026T023226Z/verdict.md \| Rule:  :: 0.95 [0.64, 1.33] --> | ○ 0.56 [0.35, 0.82]<!-- src: results/x5_natural/nem35l_x52_natural_below/verdict-20261029T082128Z/verdict.md \| Rule: HOLDS :: 0.56 [0.35, 0.82] --> | 0.44 [0.32, 0.58]<!-- src: results/x5_natural/qwen35_122b_x5_natural/verdict-20261025T005420Z/verdict.md \| Rule :: gap :: 0.44 [0.32, 0.58] --> |
  | the rule | **HOLDS<!-- src: results/x5_natural/qwen35_9b_x5_natural_g75/verdict-20261025T135050Z/verdict.md \| Rule:  :: HOLDS -->** | **MIXED<!-- src: results/x5_natural/x5_natural_27b/verdict-20261024T232738Z/verdict.md \| Rule:  :: MIXED -->** | **HOLDS<!-- src: results/x5_natural/muse30b_x5_natural/verdict-20261026T023226Z/verdict.md \| Rule:  :: HOLDS -->** | not tested (gate 0.77<!-- src: results/x5_natural/nem35l_x52_natural/gate.json \| "PP" :: 0.77 --> < 0.80); below gate, descriptive only: HOLDS<!-- src: results/x5_natural/nem35l_x52_natural_below/verdict-20261029T082128Z/verdict.md \| Rule: HOLDS :: HOLDS --> (36 passages) | **HOLDS<!-- src: results/x5_natural/qwen35_122b_x5_natural/verdict-20261025T005420Z/verdict.md \| Rule :: gap :: HOLDS -->** (114 passages, 68 bridge entities) |

- **Read.**
  - The 122B (FP8; MoE, ~10B active): holds, at its L33.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - In natural passages the recall follows the lens part on all three tested models; the 27B's lookup follows it too, so its split is mixed.

- **Caveats.**
  - Lightning: its gate failed, so it is not tested; the below-gate run (29 Oct; 36 eligible passages) is exploratory, hollow ○, never in claims or grades.
  - The 9B's gate was lowered after the data; Muse's lookup switches rarely under the whole change, so its lookup effect is wide.
  - Few items (60 to 137).

</details>

### Does each part, added by itself, move its reader? <a id="t51-1"></a>

`ledger only` *Used in: README Part I, a one-line link to this card (the dose curves).*

Test 51.1 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_dose/x52_dose-20261029T011635Z/verdict.md` · recompute: `scripts/x51_dose.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Added by itself at a dose, does the lens part move the recall more than a random part of its share, and leave the lookup?
- **Why we asked.** The conflict test takes a part away; a reader that follows a part should also move when only that part is added.
- **Data.** Main test, the scenes whose locker sentences come first: 75 / 69 / 68 / 59<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| nem35l_x52_dose :: 59 --> (9B / 27B / Muse / Lightning; Lightning at L14, a coverage run on the same rule, no prediction).
- **Method.** At the bridge word at L: the lens part alone at doses 0.5 to 3, against a random part of the same share at the same dose; the rest alone at doses 0.25 to 1.5, with and without the address.

![By itself the lens part moves the recall; the rest moves the lookup](../../figures/depth/readme/16_dose_lens.png)

*The lens part added by itself at the bridge word, one column per dose: per model, the switches beyond a random part of the same size, lookup (violet) and recall (black). Whiskers: 95% intervals; Lightning hollow (○, post hoc). The rest of the change added by itself is in 17_dose_rest.*

- **Rule, fixed in advance.** "(i) the lookup is blind to the J++ part: switch minus random <= 0.10 at every α whose plain-text cross-entropy stays under 2x the whole change's, on all three. (ii) the recall reads the J++ part above its share: at the first α where the J++ part alone switches >= 0.3, J minus random >= 0.2, per model. (iii) together only (Muse): (1,1) >= 0.8 while the best single-part dose under the cross-entropy bar stays <= 0.3."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recall: lens part alone minus random, dose 1.5 | 0.31 [0.20, 0.42]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.31 [0.20, 0.42] --> | 0.12 [0.05, 0.19]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.12 [0.05, 0.19] --> | 0.13 [0.04, 0.24]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.13 [0.04, 0.24] --> | 0.19 [0.08, 0.31]<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.19 [0.08, 0.31] --> | 0.30 [0.15, 0.45]<!-- src: results/x51_dose/x52_dose-20261029T181109Z/verdict.md \| J(1.5,0) - R(1.5,0) :: -0.02 [-0.07, 0.00] :: 0.30 [0.15, 0.45] --> |
  | recall: the same at dose 3 | -0.05 [-0.16, 0.05]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.05 [-0.16, 0.05] --> | 0.42 [0.28, 0.54]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.42 [0.28, 0.54] --> | 0.22 [0.07, 0.37]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.22 [0.07, 0.37] --> | -0.10 [-0.21, 0.00]<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| J(3,0) - R(3,0) :: -0.10 [-0.21, 0.00] --> | -0.02 [-0.13, 0.09]<!-- src: results/x51_dose/x52_dose-20261029T181109Z/verdict.md \| J(3,0) - R(3,0) :: -0.60 [-0.77, -0.47] :: -0.02 [-0.13, 0.09] --> |
  | lookup: lens part alone minus random, dose 3 | -0.63 [-0.72, -0.52]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.63 [-0.72, -0.52] --> | 0.13 [0.00, 0.26]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: 0.13 [0.00, 0.26] --> | -0.22 [-0.32, -0.13]<!-- src: results/x51_dose/x51_1-20261028T170335Z/verdict.md \| J(3,0) - R(3,0) :: -0.22 [-0.32, -0.13] --> | -0.46 [-0.64, -0.28]<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| J(3,0) - R(3,0) :: -0.46 [-0.64, -0.28] --> | -0.60 [-0.77, -0.47]<!-- src: results/x51_dose/x52_dose-20261029T181109Z/verdict.md \| J(3,0) - R(3,0) :: -0.60 [-0.77, -0.47] --> |
  | rule (i) / (ii) | yes / yes | **no** / yes | yes / yes; (iii) no | yes<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| lookup blind :: yes --> / **no** (first dose 1.5<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| nem35l_x52_dose :: **no** (1.5) :: 1.5 -->: 0.19<!-- src: results/x51_dose/x52_dose-20261029T011635Z/verdict.md \| J(1.5,0) - R(1.5,0) :: 0.19 --> against 0.2); (iii) is Muse's rule, not read; no prediction | yes<!-- src: results/x51_dose/x52_dose-20261029T181109Z/verdict.md \| qwen35_122b_x51_1 :: yes --> / yes (no prediction) |

- **Read.**
  - Added by itself, the lens part moves the recall more than a random part on all three models, and the 9B's and Muse's lookups no more than random; the 27B's lookup moves at the highest dose.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Lightning's lookup is blind to the lens part as on the 9B and Muse; its recall misses rule (ii)'s bar by a hair at the first dose that switches 0.3 of recalls.

- **Caveats.**
  - At high doses random parts switch readers too (the 9B's random part at dose 3 switches most lookups).
  - Scenes with the lockers first only.

</details>

### Does the recall need the lens part, or only follow it? <a id="t47-5"></a>

`in README` *Used in: README Part I card "Does the recall need the lens part, or only follow it?" (zeroing).*

Test 47.5 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_zero/x47_5-20261028T113106Z/x47_5.md` · recompute: `scripts/x47_zero.py` (the command in its docstring) · also: zeroing at one layer; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Taking the lens part out of the changed prompt's own state at the bridge word, does the recall drop the changed answer (needed) or leave it unchanged (followed)?
- **Why we asked.** The conflict test removes the lens part from the change; zeroing it in the changed prompt's own state asks whether the recall needs it there.
- **Data.** Main test, 200 per model.
- **Method.** In the changed prompt's state at the bridge word: its projection on the change's 25 lens directions removed at L (and at L to L+3), against a random subspace of the same share of the state.

*No figure: on every model 0.94-0.97 of its recall answers stay unchanged, so the four numbers per model are the Result's table (the zeroing figure drew every dot near 1.0).*

- **Rule, fixed in advance.** ""followed, not needed at one layer" if 0.80 or more of the recall's answers stay unchanged under the zeroing, within 0.10 of the random arm; "needed" if it has >= 0.30 blocked beyond random. The lookup reported beside." Lightning and the 122B: coverage runs on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recall: answers unchanged, the lens part zeroed at L (bar >= 0.80) | 0.97 [0.95, 0.99]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| qwen35_9b_x47_5 :: 0.97 [0.95, 0.99] --> | 0.97 [0.94, 0.99]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| x47_5_27b :: 0.97 [0.94, 0.99] --> | 0.94 [0.89, 0.98]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| muse30_x47_5 :: 0.94 [0.89, 0.98] --> | 0.97 [0.95, 0.99]<!-- src: results/x47_zero/x52_zero-20261029T032056Z/x47_5.md \| nem35l_x52_zero :: 0.97 [0.95, 0.99] --> | 0.95 [0.91, 0.99]<!-- src: results/x47_zero/x52_zero-20261029T183120Z/x47_5.md \| qwen35_122b_x47_5 :: 0.95 [0.91, 0.99] --> |
  | recall: blocked beyond a random part, at L (bar for needed >= 0.30) | 0.03 [0.01, 0.05]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| qwen35_9b_x47_5 :: 0.03 [0.01, 0.05] --> | 0.03 [0.01, 0.06]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| x47_5_27b :: 0.03 [0.01, 0.06] --> | 0.06 [0.02, 0.11]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| muse30_x47_5 :: 0.06 [0.02, 0.11] --> | 0.03 [0.01, 0.05]<!-- src: results/x47_zero/x52_zero-20261029T032056Z/x47_5.md \| nem35l_x52_zero :: 0.03 [0.01, 0.05] --> | 0.04 [0.00, 0.09]<!-- src: results/x47_zero/x52_zero-20261029T183120Z/x47_5.md \| qwen35_122b_x47_5 :: 0.04 [0.00, 0.09] --> |
  | recall: blocked beyond a random part, at L to L+3 (descriptive) | 0.25 [0.17, 0.32]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| qwen3.5-9b :: recall :: 0.25 [0.17, 0.32] --> | 0.11 [0.06, 0.16]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| qwen3.6-27b :: recall :: 0.11 [0.06, 0.16] --> | 0.08 [0.04, 0.13]<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| muse-glimmer-30b :: recall :: 0.08 [0.04, 0.13] --> | 0.18 [0.12, 0.24]<!-- src: results/x47_zero/x52_zero-20261029T032056Z/x47_5.md \| nemotron-3.5-lightning :: recall :: 0.18 [0.12, 0.24] --> | 0.08 [0.04, 0.14]<!-- src: results/x47_zero/x52_zero-20261029T183120Z/x47_5.md \| qwen3.5-122b-a10b :: recall :: 0.08 [0.04, 0.14] --> |
  | the rule | **followed, not needed at one layer<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| qwen35_9b_x47_5 :: followed, not needed at one layer -->** | **followed, not needed at one layer<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| x47_5_27b :: followed, not needed at one layer -->** | **followed, not needed at one layer<!-- src: results/x47_zero/x47_5-20261028T113106Z/x47_5.md \| muse30_x47_5 :: followed, not needed at one layer -->** | **followed, not needed at one layer<!-- src: results/x47_zero/x52_zero-20261029T032056Z/x47_5.md \| nem35l_x52_zero :: followed, not needed at one layer -->** (no prediction) | **followed, not needed at one layer<!-- src: results/x47_zero/x52_zero-20261029T183120Z/x47_5.md \| qwen35_122b_x47_5 :: followed, not needed at one layer -->** (no prediction) |

- **Read.**
  - Zeroing the lens part in the changed prompt's own state at L costs the recall at most 0.06 of its answers beyond random on all five models: the recall follows the lens part but does not need it at one layer.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Over L to L+3 the recall has more blocked (0.08 to 0.25 beyond random), between the bars (descriptive).
  - The lookup's answers stay unchanged in every arm on all five.
  - The 122B: a coverage run (FP8, L33; no prediction †).

</details>

### Does the recall need the lens part once its other copies are gone? <a id="t49-2"></a>

`in README` `below gate: Lightning` *Used in: README Part I card "Does the recall need the lens part, or only follow it?" (the ladder).*

Test 49.2 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x49_ladder/x49_2-20261028T161612Z/x49_2.md` · recompute: `scripts/x49_ladder.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Taking the lens part out of the changed prompt step by step (more layers, the earlier mention, the question, every token), when does the recall start to need it, and does the lookup ever?
- **Why we asked.** At one layer the recall barely needs the lens part; it may have copies elsewhere.
- **Data.** Clean one-pick scenes: 417 / 574 / 409. The 27B: its full ladder (x52_ladder_27b_a; the first run had steps 1-2 only); Muse: the first run (step 6 at L23-29) and a rerun with step 6 inside the breadth track's band (L36-42).
- **Method.** In the changed prompt's own run, the lens part's 25 directions taken out at each step's tokens and layers, against a random subspace of the same share of the state; step 6 is the breadth track's definition (each token's own top-10 lens directions over his band).

- **Rule, fixed in advance.** "second_copy: rung (3) costs the recall >= 0.3 more than rung (2) in locker-first scenes (paired CI excluding 0) and rung (2) already costs >= 0.3 in locker-after scenes; only_everything: rungs (1)-(4) each <= 0.2 and rung (5) or (6) >= 0.5; lookup: <= 0.1 beyond random at every rung." The 27B's full ladder and Muse's rerun: coverage runs on this rule, no prediction.

The two rungs the rule compares, per reader and scene order:

![The recall needs the lens part once its other copies go; the lookup never](../../figures/depth/ledger/03_ladder.png)

*The ladder at the two rungs its rule compares: the answers turned wrong beyond a random part of the same share when the lens part is taken out step by step, the recall in locker-first and in locker-after scenes and the lookup over every scene. Whiskers 95% intervals; Lightning and the 122B hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recall, locker first: step 3 minus step 2 | 0.32 [0.24, 0.39]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-first :: 0.32 [0.24, 0.39] --> | 0.13 [0.08, 0.19]<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| qwen3.6-27b :: locker-first :: 0.13 [0.08, 0.19] --> | 0.10 [0.05, 0.15]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-first :: 0.10 [0.05, 0.15] --> | ○ step 3: 0.33 [0.24, 0.42]<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| recall :: locker-first :: 0.03 [0.00, 0.07] :: 0.33 [0.24, 0.42] -->, step 2: 0.09 [0.04, 0.15]<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| recall :: locker-first :: 0.03 [0.00, 0.07] :: 0.09 [0.04, 0.15] --> | 0.07 [0.02, 0.13]<!-- src: results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.md \| qwen3.5-122b-a10b :: locker-first :: 0.82 / 0.92 / 0.10 [0.01, 0.21] :: 0.07 [0.02, 0.13] --> |
  | recall, all scenes: step 5, accuracy drop beyond random | 0.44 [0.37, 0.52]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| 0.51 / 0.95 / 0.44 [0.37, 0.52] :: 0.44 [0.37, 0.52] --> | 0.25 [0.20, 0.32]<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| qwen3.6-27b :: 0.74 / 0.99 / 0.25 [0.20, 0.32] :: 0.25 [0.20, 0.32] --> | 0.21 [0.15, 0.26]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| 0.78 / 0.99 / 0.21 [0.15, 0.26] :: 0.21 [0.15, 0.26] --> | ○ 0.49 [0.41, 0.56]<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| recall :: all :: 0.03 [0.01, 0.05] :: 0.49 [0.41, 0.56] --> | 0.77 / 0.94 / 0.17 [0.12, 0.22]<!-- src: results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.md \| qwen3.5-122b-a10b :: recall :: all :: 0.77 / 0.94 / 0.17 [0.12, 0.22] --> |
  | recall, locker after: step 2 | 0.40 [0.31, 0.51]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-after :: 0.40 [0.31, 0.51] --> | 0.24 [0.17, 0.32]<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| qwen3.6-27b :: locker-after :: 0.76 / 1.00 / 0.24 [0.17, 0.32] :: 0.24 [0.17, 0.32] --> | 0.15 [0.10, 0.22]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| locker-after :: 0.15 [0.10, 0.22] --> | ○ 0.36 [0.27, 0.45]<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| recall :: locker-after :: 0.02 [0.00, 0.06] :: 0.36 [0.27, 0.45] --> | 0.85 / 0.98 / 0.13 [0.08, 0.19]<!-- src: results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.md \| qwen3.5-122b-a10b :: locker-after :: 0.85 / 0.98 / 0.13 [0.08, 0.19] --> |
  | recall, all scenes: step 6 (the breadth track's definition), accuracy drop beyond random | 0.30 [0.25, 0.37]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| qwen3.5-9b :: 0.66 / 0.96 / 0.30 [0.25, 0.37] :: 0.30 [0.25, 0.37] --> | 0.45 [0.37, 0.55]<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| qwen3.6-27b :: 0.51 / 0.95 / 0.45 [0.37, 0.55] :: 0.45 [0.37, 0.55] --> | -0.00 [-0.03, 0.03]<!-- src: results/x49_ladder/x49_2-20261028T161612Z/x49_2.md \| muse-glimmer-30b :: 0.97 / 0.97 / -0.00 [-0.03, 0.03] :: -0.00 [-0.03, 0.03] --> at L23-29; 0.09 [0.05, 0.14]<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| muse-glimmer-30b :: 0.84 / 0.93 / 0.09 [0.05, 0.14] :: 0.09 [0.05, 0.14] --> in the breadth track's band, L36-42 | ○ 0.36 [0.29, 0.46]<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| recall :: all :: 0.03 [0.01, 0.05] :: 0.36 [0.29, 0.46] --> in the breadth track's band (L27-33) | 0.87 / 0.92 / 0.06 [0.00, 0.13]<!-- src: results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.md \| qwen3.5-122b-a10b :: recall :: all :: 0.87 / 0.92 / 0.06 [0.00, 0.13] --> (in the breadth track's band L39-45) |
  | rules: second copy / only everything / lookup never | yes / no / yes | no<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| x52_ladder_27b_a :: 574 :: no --> / no / yes (no prediction) | no / no / yes; in the breadth track's band no<!-- src: results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.md \| muse30_x52_ladder :: 409 :: no --> / no / yes | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80); below gate, descriptive only: no<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| nem35l_x52_ladder_below :: 295 :: no --> / no / yes<!-- src: results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.md \| nem35l_x52_ladder_below :: 295 :: yes --> | no<!-- src: results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.md \| qwen35_122b_x49_2 :: no --> / no / yes (no prediction) |

- **Read.**
  - The recall needs the lens part once its copies over four layers and at the earlier mention go (9B); on Muse every step costs less. The lookup never needs it, on all three.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The 27B's recall has most blocked at step 6 (the breadth track's definition over its band); neither the earlier mention as its second copy (a) nor "only when everything goes" (b) holds there, and its lookup never needs the lens part (c).

- **Caveats.**
  - Lightning: below the clean one-pick gate, so not tested; its below-gate run (295 eligible scenes, step 6 in the breadth track's band L27-33) is exploratory, hollow ○, never in claims or grades.
  - The reruns redraw every step: shared steps move by up to 0.02 against the first runs (Flagged 20); Muse's column keeps the first run, as the README.
  - Lightning: not tested, the clean one-pick design's gate fails there (recall 0.751).

</details>

### Does the recall also read the item's earlier mention? <a id="t45p"></a>

`in README` `below gate: Lightning` *Used in: README Part I card "Does the recall also read the item's earlier mention?".*

Test 45p · opened 27 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x45p/x45p-20261027T012017Z/x45p.md` · recompute: `scripts/x45p.py` (the command in its docstring) · also: the earlier mention, opened 27 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the new item's locker sentence comes before the asked pick, does the recall also read the item's lens part at that earlier mention, beyond the bridge word?
- **Why we asked.** The ladder's third step points to a second copy where the locker sentence comes first; the earlier mention is the item's own word there.
- **Data.** Clean one-pick scenes whose new item's locker sentence comes before the asked pick: 186<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| qwen35_9b_x45p :: 186 --> / 254<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| x45p_27b :: 254 --> / 178<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| muse30b_x45p :: 178 --> (9B / 27B / Muse). Lightning not tested: the clean one-pick design's gate fails on it.
- **Method.** On the original prompt, the switches' drop loss_k = 1 - S_k / S_1 under: (1) the base edit, the whole change at the bridge word minus its lens part; (2) (1), and the new item's tokens in its locker sentence without their own lens part; (3) (1), and the same tokens without a random part of the same share; (4) (1), and another item's tokens without their own lens part.

![The recall also reads the item at its earlier mention](../../figures/depth/readme/36_earlier_mention.png)

*Claim 3: the recall's switches blocked against the change at the bridge word alone (arm 1) when the new item's tokens at its earlier mention also have their own lens part removed (left), and when another item's tokens have theirs removed (right); grey dot, joined to the item's: the same tokens with a random part of the same share removed. Clean one-pick scenes with the item's locker sentence before the pick; whiskers 95% intervals; Lightning hollow ○ (below its gate, descriptive), the 122B hollow ○ (a coverage run, no prediction).*

- **Rule, fixed in advance.** "the recall reads the earlier mention if the recall's switch drop in (2) exceeds (3) by at least 0.2 and (4) by at least 0.15 (loss_k = 1 - S_k / S_1, point estimates), on at least 2 of 3 models; a model whose base edit switches fewer than 30 recalls is not tested."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recalls switched by the base edit (1) | 0.74 [0.66, 0.82]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| qwen35_9b_x45p :: 0.74 [0.66, 0.82] --> | 0.30 [0.23, 0.37]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| x45p_27b :: 0.30 [0.23, 0.37] --> | 0.31 [0.21, 0.40]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| muse30b_x45p :: 0.31 [0.21, 0.40] --> | ○ 0.75 [0.68, 0.82]<!-- src: results/x45p/x52_45p_below-20261029T090351Z/x45p.md \| nem35l_x52_45p_below :: 119 :: 0.75 [0.68, 0.82] --> | 0.75 [0.66, 0.83]<!-- src: results/x45p/x53_45p_coverage-20261030T002915Z/x45p.md \| qwen35_122b_x45p_r2 :: 0.75 [0.66, 0.83] --> |
  | extra drop at the earlier mention: (2) minus (3) (bar >= 0.2) | 0.25 [0.16, 0.34]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| qwen35_9b_x45p :: 0.25 [0.16, 0.34] --> | 0.41 [0.32, 0.53]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| x45p_27b :: 0.41 [0.32, 0.53] --> | 0.42 [0.26, 0.63]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| muse30b_x45p :: 0.42 [0.26, 0.63] --> | ○ 0.22 [0.15, 0.30]<!-- src: results/x45p/x52_45p_below-20261029T090351Z/x45p.md \| nem35l_x52_45p_below :: 119 :: 0.22 [0.15, 0.30] --> | 0.15 [0.10, 0.22]<!-- src: results/x45p/x53_45p_coverage-20261030T002915Z/x45p.md \| qwen35_122b_x45p_r2 :: 0.15 [0.10, 0.22] --> |
  | (2) minus (4) (bar >= 0.15) | 0.26 [0.18, 0.35]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| qwen35_9b_x45p :: 0.26 [0.18, 0.35] --> | 0.49 [0.38, 0.64]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| x45p_27b :: 0.49 [0.38, 0.64] --> | 0.49 [0.31, 0.69]<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| muse30b_x45p :: 0.49 [0.31, 0.69] --> | ○ 0.21 [0.14, 0.29]<!-- src: results/x45p/x52_45p_below-20261029T090351Z/x45p.md \| nem35l_x52_45p_below :: 119 :: 0.21 [0.14, 0.29] --> | 0.20 [0.15, 0.27]<!-- src: results/x45p/x53_45p_coverage-20261030T002915Z/x45p.md \| qwen35_122b_x45p_r2 :: 0.20 [0.15, 0.27] --> |
  | holds | **yes<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| qwen35_9b_x45p :: 186 :: yes -->** | **yes<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| x45p_27b :: 254 :: yes -->** | **yes<!-- src: results/x45p/x45p-20261027T012017Z/x45p.md \| muse30b_x45p :: 178 :: yes -->** | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80); below gate, descriptive only: yes (119 items) | **no<!-- src: results/x45p/x53_45p_coverage-20261030T002915Z/x45p.md \| qwen35_122b_x45p_r2 :: 0.20 [0.15, 0.27] :: no -->** (no prediction) |

- **Read.**
  - On all three models the recall has more blocked switches when the lens part also goes at the item's earlier mention than when a random part or another item's lens part goes: the recall reads the earlier mention too.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning: below the clean one-pick gate, so not tested; its below-gate run (119 locker-first items) is exploratory, hollow ○, never in claims or grades.
  - The base edit switches few recalls on the 27B and Muse (75 and 55 switches), so the losses rest on few switches there.
  - Only scenes with the locker first; after the pick there is no earlier mention.

</details>

### When the lens part points the recall to one item and the address to another, which does it follow? <a id="b53-6"></a>

`in README` *Used in: README Part I card "When the lens part points the recall to one item and the address to another, which does it follow?".*

Test 53.6 · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_identity_address/x53_identity_address-20261029T105132Z` · recompute: `scripts/x53_identity_address.py` (the command in its docstring) · also: joint four-model verdict

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the lens part of the change points the recall to one item and the address points it to another, which does the recall follow?
- **Why we asked.** The address swap redirects part of the recall ([swap](#swap)); the lens part carries the item's identity to the recall. Set against each other, the two show which the recall weights.
- **Data.** Routes scenes of the condition without a move whose three items have distinct leg counts: 300 per model (9B at L12, the 27B at L32, Muse at L26, Lightning at L14); all four pass the gate.
- **Method.** At the bridge word: the lens part of the change toward item B plus the address swap toward item C's slot (dose 2); read the recall's answer: B's, C's or the original; each part alone beside, and the lens part with a random direction of the address's norm.

- **Rule, fixed in advance.** "Rule: "the recall follows the lens identity" if B's share >= 2x C's; "follows the address" if C's >= 2x B's; else both." (jobs/c3/batch53.yaml, Dan 29 Oct 09:30; no prediction) Across models: "the recall's pointer [pointer: the address] use tracks the swap's collateral" if the models whose recall the address swap moved (9B, Lightning) give "both" and the others give "follows the lens identity". (jobs/c3/batch53.yaml, critic_1125, Dan 11:25; no prediction)

Which item the recall follows when the lens part and the address disagree:

![Every recall follows both; on the 27B and Muse it mostly stays put](../../figures/depth/ledger/04_follows_both.png)

*The lens part from one scene (item B) and the address from another (item C) swapped in together (left) or alone (right): the share of the recall's answers that are B's (the lens part's item, teal) and C's (the address's item, orange), per model. Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | both parts: the recall answers B's / C's / the original | 0.25 [0.20, 0.32]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: 300 :: 0.25 [0.20, 0.32] --> / 0.30 [0.25, 0.35]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: 300 :: 0.30 [0.25, 0.35] --> / 0.39 [0.31, 0.46]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: 300 :: 0.39 [0.31, 0.46] --> | 0.11 [0.07, 0.16]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: 0.11 [0.07, 0.16] --> / 0.06 [0.04, 0.08]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: 0.06 [0.04, 0.08] --> / 0.81 [0.75, 0.86]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: 0.81 [0.75, 0.86] --> | 0.07 [0.04, 0.11]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: 300 :: 0.07 [0.04, 0.11] --> / 0.05 [0.02, 0.08]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: 300 :: 0.05 [0.02, 0.08] --> / 0.85 [0.77, 0.90]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: 300 :: 0.85 [0.77, 0.90] --> | 0.25 [0.19, 0.32]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: 300 :: 0.25 [0.19, 0.32] --> / 0.27 [0.21, 0.34]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: 300 :: 0.27 [0.21, 0.34] --> / 0.45 [0.39, 0.52]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: 300 :: 0.45 [0.39, 0.52] --> | not tested (gate: the recall reads 0.73<!-- src: results/x53_identity_address/qwen35_122b_x53_6/gate.json \| "PM": 0.732421875 :: 0.73 --> < 0.80) |
  | each part alone: the lens part, B's / the address, C's | 0.05 [0.03, 0.08]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: recall :: lens :: 0.05 [0.03, 0.08] --> / 0.21 [0.16, 0.27]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: recall :: addr :: 0.21 [0.16, 0.27] --> | 0.00 [0.00, 0.01]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: recall :: lens :: 0.00 [0.00, 0.01] --> / 0.03 [0.01, 0.05]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: recall :: addr :: 0.03 [0.01, 0.05] --> | 0.00 [0.00, 0.00]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: recall :: lens :: 0.00 [0.00, 0.00] --> / 0.03 [0.01, 0.05]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: recall :: addr :: 0.03 [0.01, 0.05] --> | 0.04 [0.01, 0.06]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: recall :: lens :: 0.04 [0.01, 0.06] --> / 0.24 [0.19, 0.30]<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: recall :: addr :: 0.24 [0.19, 0.30] --> | |
  | the rule | **both<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.5-9b :: 300 :: both -->** | **both<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: both -->** | **both<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| muse-glimmer-30b :: 300 :: both -->** | **both<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| nemotron-3.5-lightning :: 300 :: both -->** | |
  | across models: wanted | both | follows the lens identity | follows the lens identity | both | |
  | across models | **does not hold<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| Across models :: does not hold --> as written (every model "both")**; beside, descriptive: the recall moves under both levers on the 9B and Lightning (0.25-0.30<!-- src: jobs/c3/batch53.yaml \| Lightning (0.25-0.30 each) :: 0.25-0.30 --> each), barely on the 27B and Muse (<= 0.11<!-- src: jobs/c3/batch53.yaml \| barely on the 27B and Muse (<= 0.11) :: 0.11 -->), the same split as the address swap's collateral | | | | |

- **Read.**
  - By the rule all four models give both. On the 9B and Lightning the recall splits between B's and C's answers, about a quarter each; on the 27B and Muse it mostly stays on the original answer, and the little that moves goes slightly more to B than to C.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Across models: does not hold as written (every model "both"). The 9B and Lightning give both as wanted; the 27B and Muse give both where the rule wanted the lens identity. Descriptive, beside: the recall moves under both levers on the 9B and Lightning (0.25-0.30<!-- src: jobs/c3/batch53.yaml \| Lightning (0.25-0.30 each) :: 0.25-0.30 --> each), barely on the 27B and Muse (<= 0.11<!-- src: jobs/c3/batch53.yaml \| barely on the 27B and Muse (<= 0.11) :: 0.11 -->), the same split as the address swap's collateral.
  - Each part alone moves the recall little on the 27B and Muse; on the 9B and Lightning the address alone moves about a fifth to C.

- **Caveats.**
  - The 27B sits just under the identity bar: B's share 0.11<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: 0.11 --> against twice C's 0.06<!-- src: results/x53_identity_address/x53_identity_address-20261029T105132Z/verdict.md \| qwen3.6-27b :: 300 :: 0.06 -->.
  - On the 27B and Muse the recall mostly stays on the original answer, so their "both" rests on small shares. The labels ignore magnitude (flag [30](../review/ledger_ops_2026-10.md#flagged)).
  - One joint verdict (results/x53_identity_address/x53_identity_address-20261029T105132Z); exploratory (batch 53), no prediction.

</details>

### Does the lens effect follow the question's position or the answer's type? <a id="b53-1"></a>

`in README` *Used in: README Part I card "Does asking the question before the scene change how the lookup uses the lens part?"; README "Tested and dropped" ("The question's position decides item or answer").*

Test 53.1 · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_2x2/qwen35_122b_x53_2x2/qa_num/agreement.json` · recompute: `scripts/x53_2x2.py` (the command in its docstring) · also: five models, combined verdict 29 Oct; the word cells not tested

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On our locker scenes, does the recall's lens effect (the item or its answer, by 51.12's arms) change when the question comes before the scene instead of after it, or when the recall's answer is a word instead of a number?


- **Why we asked.** On the fact passages the answer word is readable and usable through the lens ([52 B](#b52-b)); on our scenes it is not. His questions and answers differ from ours in two ways at once: where the question sits and what kind of answer it asks for.

- **Data.** Our locker scenes (the main test), four cells: the question after the scene with a number answer (the main test as is), the question before the scene with a number answer, and the same two with a word answer: the animal's class (mammal, bird, insect, ...), the only relation that passed the 9B's coverage rule, on 191<!-- src: jobs/c3/x53_2x2_words_9b.yaml | Animal class passes coverage on the 9B :: 191 --> animal scenes, not the 600 of the number cells. Lightning: 516 scenes (84 dropped: the bridge word is not one token at one position), its word cells stopped (Dan 11:10: the wording fails). The 122B (FP8; MoE, ~10B active) at L33: 200 scenes in each number cell, its gate passed in both (lookup / recall 0.9917 / 0.85<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 --> and 0.9983 / 0.84<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 -->); its word cells stopped too.

- **Method.** Per cell: the main gate; the conflict test at L; 51.12's arms with the readout check first (without the lens part; without it but keeping the answer's directions; without the answer directions only, each beyond random); the inventory of the lens part's directions on 50 items.

- **Rule, fixed in advance.** "Rule per cell: 51.12's labels (entity / answer / mixed / answer word not read). Rule across cells: "position": (Q-before, number) is answer or mixed and (Q-after, word) is entity; "readability": (Q-after, word) is answer or mixed and (Q-before, number) is entity; "both": each single change gives mixed and (Q-before, word) gives answer; "neither": all four entity. Cross-check, decisive for the story: the conflict test's lookup has <= 0.10 blocked beyond random in all four cells ("the pointer [pointer: the address] does not depend on the question"); report per cell." Models: 9B, then 27B, then Lightning if its gate passes. Dan 11:10, across the number cells: "the pointer [pointer: the address] does not depend on the question's position" if the lookup has <= 0.10 blocked in both cells on a model. Dan 11:25: the paired difference (Q-before minus Q-after) with its cluster-bootstrap CI; "order dependence" only if that CI excludes 0. (jobs/c3/batch53.yaml, next_1110 and critic_1125; no prediction)


Both readers with a number answer, the question after and before the scene:

![With a number answer the recall follows the entity](../../figures/depth/ledger/05_number_answer.png)

*A number as the answer: the switches blocked without the lens part beyond a random part, the recall (left) and the lookup (right), with the question after the scene and, on the 27B and the 122B, before it. Whiskers 95% intervals; Lightning and the 122B hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | question after, number: the recall's label | **the lens effect is the entity<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: the lens effect is the entity -->** | **the lens effect is the entity<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: the lens effect is the entity -->** | **the answer word is not read at the bridge word<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: the answer word is not read at the bridge word :: the answer word is not read at the bridge word -->** (not read on 0.99 [0.98, 1.00]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.99 [0.98, 1.00] :: 0.99 [0.98, 1.00] --> of items; the arms beside say entity) | **the answer word is not read at the bridge word<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: the answer word is not read at the bridge word :: the answer word is not read at the bridge word -->** (not read on 0.95 [0.90, 0.99]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.95 [0.90, 0.99] :: 0.95 [0.90, 0.99] --> of items; the arms beside say entity) | **the answer word is not read at the bridge word<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 :: the answer word is not read at the bridge word -->** (not read on 1.00 [1.00, 1.00]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 :: 1.00 [1.00, 1.00] --> of items; the arms beside say entity) |
  | question after, number: recall blocked without the lens part, beyond random / share remaining with the answer directions retained / without the answer directions only | 0.50 [0.41, 0.57]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.50 [0.41, 0.57] --> / 0.95 [0.90, 0.99]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.95 [0.90, 0.99] --> / 0.00 [0.00, 0.00]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.00 [0.00, 0.00] --> | 0.74 [0.66, 0.80]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.74 [0.66, 0.80] --> / 0.93 [0.85, 0.99]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.93 [0.85, 0.99] --> / 0.03 [0.01, 0.05]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.03 [0.01, 0.05] --> | 0.76 [0.62, 0.88]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.76 [0.62, 0.88] --> / 0.93 [0.85, 1.01]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.93 [0.85, 1.01] --> / -0.01 [-0.05, 0.03]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: -0.01 [-0.05, 0.03] --> (beside the label) | 0.34 [0.25, 0.44]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.34 [0.25, 0.44] --> / 0.92 [0.83, 1.03]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.92 [0.83, 1.03] --> / 0.00 [-0.02, 0.01]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.00 [-0.02, 0.01] --> (beside the label) | 0.27 [0.17, 0.38]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 :: 0.27 [0.17, 0.38] --> / 0.98 [0.86, 1.18]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 :: 0.98 [0.86, 1.18] --> / 0.01 [-0.01, 0.04]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.9917 / 0.85 :: 0.01 [-0.01, 0.04] --> (beside the label) |
  | question after, number: the conflict test's lookup, blocked beyond random | -0.05 [-0.09, 0.00]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: -0.05 [-0.09, 0.00] --> (around; its 51.12 label: can't tell) | 0.14 [0.08, 0.20]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.14 [0.08, 0.20] --> (mixed; its 51.12 label: the entity) | -0.10 [-0.15, -0.04]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: -0.10 [-0.15, -0.04] --> (around; its 51.12 label: the answer word is not read at the bridge word) | 0.02 [-0.03, 0.07]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.02 [-0.03, 0.07] --> (around; its 51.12 label: the answer word is not read at the bridge word) | 0.01 [-0.06, 0.08]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, number) :: 0.01 [-0.06, 0.08] --> (around; its 51.12 label: the answer word is not read at the bridge word) |
  | question before, number: the recall's label | not tested (gate 0.763<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.7633 :: 0.763 --> < 0.80: the recall's read on the original prompts) | **the lens effect is the entity<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: the lens effect is the entity -->** | not tested (gate 0.7189<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.7189 --> < 0.80: the recall's read on the original prompts) | not tested (gate 0.647<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.6473 :: 0.647 --> < 0.80: the recall's read on the original prompts) | **the answer word is not read at the bridge word<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 :: the answer word is not read at the bridge word -->** (not read on 1.00 [1.00, 1.00]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 :: 1.00 [1.00, 1.00] --> of items; the arms beside say entity) |
  | question before, number: recall switches blocked / share remaining with the answer directions retained / answer directions only | | 0.56 [0.46, 0.65]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.56 [0.46, 0.65] --> / 0.91 [0.81, 0.98]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.91 [0.81, 0.98] --> / 0.01 [0.00, 0.02]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.01 [0.00, 0.02] --> | | | 0.31 [0.22, 0.39]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 :: 0.31 [0.22, 0.39] --> / 0.87 [0.73, 1.02]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 :: 0.87 [0.73, 1.02] --> / 0.03 [0.00, 0.06]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.9983 / 0.84 :: 0.03 [0.00, 0.06] --> (beside the label) |
  | question before, number: the conflict test's lookup, blocked beyond random | | 0.22 [0.15, 0.31]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.22 [0.15, 0.31] --> (through; its 51.12 label: the answer word is not read at the bridge word) | | | -0.03 [-0.11, 0.05]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: -0.03 [-0.11, 0.05] --> (around; its 51.12 label: the answer word is not read at the bridge word) |
  | across the number cells (the lookup <= 0.10 in both) | can't tell: (Q-before, number) not tested | **does not hold<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Across the number cells (Dan 11:10) :: (Q-after, number) (0.14), (Q-before, number) (0.22) :: does not hold -->** (0.14 and 0.22 > 0.10) | can't tell: (Q-before, number) not tested | can't tell: (Q-before, number) not tested | **"the pointer does not depend on the question's position<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Across the number cells (Dan 11:10) :: the pointer does not depend on the question's position -->"** [pointer: the address] (the lookup <= 0.10 beyond random in both number cells) |
  | the lookup, question before minus after (paired, cluster CI; "order dependence" only if the CI excludes 0) | can't tell: a number cell not tested | **order dependence<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: order dependence -->**: +0.11 [+0.01, +0.22]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: +0.11 [+0.01, +0.22] --> on the 162<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: 162 --> scenes both number cells read | can't tell: a number cell not tested | can't tell: a number cell not tested | **the CI includes 0<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: the CI includes 0 -->**: -0.05 [-0.17, +0.05]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: -0.05 [-0.17, +0.05] --> on the 148<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: 148 scenes :: 148 --> scenes both number cells read; no order dependence claimed |
  | across models (the denominator: the models where both number cells passed their gates) | **order dependence on 1 of the 2<!-- src: jobs/c3/batch53.yaml \| order dependence on 1 of the 2 :: 1 of the 2 --> models where both number cells passed their gates**: 27B yes (+0.11 [+0.01, +0.22]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Muse: can't tell :: +0.11 [+0.01, +0.22] -->), 122B no (the CI includes 0: -0.05 [-0.17, +0.05]<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Muse: can't tell :: -0.05 [-0.17, +0.05] -->); 9B / Muse / Lightning: Q-before gate failed (the verdict counts order dependence on 1 of 3 models<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Muse: can't tell :: order dependence on 1 of 3 models -->) | | | | |
  | question after / before, word (the animal's class) | not tested (the relation's 9B accuracy 0.382<!-- src: results/x53_2x2/qwen35_9b_x53_2x2_words/relation.json \| accuracy_recall_qa_word :: 0.382 --> < 0.80) | not tested (the same rule: the relation is chosen on the 9B) | not run: stopped (the wording fails) | not run: stopped (the wording fails) | not run: stopped (the wording fails) |
  | the word cells' gates beside (descriptive): question after / before, lookup / recall read on the original prompts | 0.9476<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, word) :: 0.9476 --> / 0.3822<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, word) :: 0.3822 -->; 0.9686<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, word) :: 0.9686 --> / 0.9162<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, word) :: 0.9162 --> | 1.0<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, word) :: 1.0 --> / 0.7592<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-after, word) :: 0.7592 -->; 1.0<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, word) :: 1.0 --> / 0.9895<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, word) :: 0.9895 --> | not run | not run | not run |
  | across cells; the cross-check (the lookup <= 0.10 in all four) | **can't tell<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Rule across cells :: position, readability, both, neither :: can't tell -->** (no label in three cells; all four patterns left open); cross-check **can't tell (a cell without numbers; the tested ones <= 0.10)<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: can't tell (a cell without numbers; the tested ones <= 0.10) -->** | **can't tell<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Rule across cells :: leave open: readability, neither :: can't tell -->** (no label in the two word cells; left open: readability, neither); cross-check **does not hold<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: (Q-after, number) (0.14), (Q-before, number) (0.22) :: does not hold -->** (the lookup has more than 0.10 blocked beyond random in both number cells) | **can't tell<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Rule across cells :: position, readability, both) :: can't tell -->** (no label in three cells; left open: position, readability, both); cross-check **can't tell (a cell without numbers; the tested ones <= 0.10)<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: can't tell (a cell without numbers; the tested ones <= 0.10) -->** | **can't tell<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Rule across cells :: position, readability, both) :: can't tell -->** (no label in three cells; left open: position, readability, both); cross-check **can't tell (a cell without numbers; the tested ones <= 0.10)<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: can't tell (a cell without numbers; the tested ones <= 0.10) -->** | **can't tell<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Rule across cells :: leave open: none :: can't tell -->** (both number cells "not read": no pattern left open); cross-check **can't tell (a cell without numbers; the tested ones <= 0.10)<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: can't tell (a cell without numbers; the tested ones <= 0.10) -->** |

- **Read.**
  - With a number answer the recall follows the entity wherever the question sits: on the 9B with the question after the scene, on the 27B with it after and before; keeping the answer's directions keeps almost all of the recall's drop, and the answer directions alone cost little. On Lightning and Muse (question after) and on the 122B (both cells) the recall's answer word is not read at the bridge word, so that is their label; the arms beside give the entity pattern.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The conflict test's lookup has nothing blocked beyond random on the 9B, Lightning and Muse (question after) and on the 122B in both cells, so on the 122B the lookup's route does not depend on the question's position by the decided rule; on the 27B it has some blocked with the question after the scene and more with it before. On the 27B the decided rule ("the pointer [pointer: the address] does not depend on the question's position") and the cross-check do not hold, and the paired difference on the scenes both cells read excludes 0: order dependence by the decided wording. On the 9B, Lightning and Muse the question-before cell missed its gate, so they read can't tell.
  - Order dependence: a small order effect on the 27B (lower bound +0.01<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Paired difference (Dan 11:25) :: +0.01 -->, of the order of the 122B's rerun noise), none on the 122B.


- Across models : order dependence on 1 of the 2 models where both number cells passed their gates: 27B yes, 122B no (the paired difference's CI includes 0); 9B / Muse / Lightning: Q-before gate failed.
- Across cells no model gets a label: the word cells have none. On the 27B the question-before number cell is the entity, which rules out "position" and "both"; "readability" and "neither" stay open and only the word cells could decide between them. On the 9B all four patterns stay open; on Lightning and Muse "position", "readability" and "both" (their question-after label is not the entity, so "neither" is out); on the 122B none (both number cells "not read"). The word cells are not tested: the animal-class relation's recall reads too few of the 9B's answers with the question after the scene (the decided rule); with the question before the scene the 9B's recall misses the number cell's gate.

- **Caveats.**
  - The word cells used the animal-class relation on 191 animal scenes, the only relation that passed the coverage rule (Dan's 10:20 decision: words read by their first token); it then missed the accuracy bar, so neither word cell is tested.
  - The question-after word prompt mostly gets the animal's name, not its class (236<!-- src: results/x53_2x2/diag_words-20261029T095338Z/note.md | the asked pick itself (the animal) 236 :: 236 --> of 382), so the 0.382 reflects the answer format; the cells stay not tested under the decided rule (a CPU check, descriptive).
  - The (question after, number) cell repeats our main test (on the 9B the rerun agrees with the stored run on the recall's whole change, 200 of 200; the 122B below).
  - The evaluation logic was clarified after the data (3dae749f): the cross-check reads "does not hold" once a tested cell exceeds 0.10, and a "can't tell" across cells lists the patterns still open. Dan (11:25) confirmed it as the correct reading of "in all four cells"; on the 27B it changes nothing, since the Q-after cell is the main test (0.14<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| Cross-check :: (Q-after, number) (0.14) :: 0.14 -->, already failing) (record line [29](../review/ledger_ops_2026-10.md#flagged)).
  - Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones (the 9B's question-before cell, 0.763<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| (Q-before, number) :: 0.7633 :: 0.763 -->).
  - The 122B, the verdict's flags: L33 carried over (relative depth 0.69); FP8 weights (MoE, ~10B active); the J++ lens fit in bf16.
  - The 122B: the rerun of its main cells matches the stored run on 193<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| qwen35_122b_x0_necessity_r2 :: recall: whole 193/200 :: 193 -->-194<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| qwen35_122b_x0_necessity_r2 :: lookup: whole 194/200 :: 194 --> of 200 items and arm 1's recall effect moves 0.315<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| qwen35_122b_x0_necessity_r2 :: vs stored 0.315 :: 0.315 --> → 0.270<!-- src: results/x53_2x2/x53_2x2-20261029T113335Z/verdict.md \| qwen35_122b_x0_necessity_r2 :: arm 1 extra loss rerun 0.270 :: 0.270 --> (likely FP8 / MoE numerics, unchecked); its numbers carry ~±0.04<!-- src: jobs/c3/batch53.yaml \| run-to-run noise beyond the bootstrap :: 0.04 --> run-to-run noise beyond the bootstrap (per item: results/x53_2x2/qwen35_122b_x53_2x2/qa_num/agreement.json).
  - Exploratory (batch 53): no prediction.

</details>

### Does each reader follow the lens part by weight, or by route? <a id="t49-1"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 49.1 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x49_gain/x49_1-20261028T154510Z/x49_1.md` · recompute: `scripts/x49_gain.py` (the command in its docstring) · also: gain map; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Scaling the lens part and the rest of the change separately, does the recall move with either part at enough gain (weights), or only with one of them (routes), and does the lookup ignore the lens part?
- **Why we asked.** Removing a part shows what a reader needs; adding each part at several gains shows whether it reads that part at all.
- **Data.** Main test, locker first: 75<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 75 --> / 69<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 69 --> / 68<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 68 --> / 59<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 59 --> (9B / 27B / Muse / Lightning). The 122B (coverage, 30 Oct; FP8, L33): 53<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md | qwen35_122b_gain :: 53 --> scenes.
- **Method.** At the bridge word at L: the lens part times α plus the rest times β, α and β from 0 to 2; the rest also without the address; random parts of the lens part's share at the same gains.

*No figure: five cells per model, each against its bar: the Result's table (the bars-and-ticks figure carried the verdict "(c) neither" on every model).*

- **Rule, fixed in advance.** "(a) "weights, not routes": the recall's switch at (2,0) >= 0.5 and at (0,2, no U) >= 0.5, random corners <= 0.15; the lookup's switch at (2,0) <= 0.10 and at (0,1) >= 0.6. (b) "routes": the recall's switch at (0,2) <= 0.2 while (2,0) >= 0.5. (a') "the rest moves the recall only through the address": (0,2) >= 0.5 but (0,2, no U) <= 0.2. (c) "neither": report the two heatmaps." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.** (switch rates)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | recall, the lens part alone at twice its size (bar >= 0.5) | 0.55 [0.42, 0.67]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.55 [0.42, 0.67] --> | 0.23 [0.13, 0.35]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.23 [0.13, 0.35] --> | 0.24 [0.10, 0.37]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.24 [0.10, 0.37] --> | 0.64 [0.51, 0.78]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.64 [0.51, 0.78] --> | 0.55 [0.38, 0.69]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.55 [0.38, 0.69] --> |
  | recall, the rest alone at twice its size | 0.97 [0.93, 1.00]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.97 [0.93, 1.00] --> | 0.64 [0.54, 0.74]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.64 [0.54, 0.74] --> | 0.18 [0.08, 0.29]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.18 [0.08, 0.29] --> | 0.90 [0.81, 0.97]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.90 [0.81, 0.97] --> | 0.87 [0.76, 0.95]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.87 [0.76, 0.95] --> |
  | recall, the same without the address (bar >= 0.5) | 0.76 [0.66, 0.86]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.76 [0.66, 0.86] --> | 0.45 [0.34, 0.56]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.45 [0.34, 0.56] --> | 0.21 [0.09, 0.34]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.21 [0.09, 0.34] --> | 0.73 [0.60, 0.84]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.73 [0.60, 0.84] --> | 0.85 [0.73, 0.94]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.85 [0.73, 0.94] --> |
  | recall, a random part at the lens part's share, twice (bar <= 0.15) | 0.24 [0.14, 0.34]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.24 [0.14, 0.34] --> | 0.01 [0.00, 0.05]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.01 [0.00, 0.05] --> | 0.01 [0.00, 0.05]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.01 [0.00, 0.05] --> | 0.42 [0.31, 0.54]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.42 [0.31, 0.54] --> | 0.23 [0.13, 0.34]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.23 [0.13, 0.34] --> |
  | lookup, the lens part alone at twice its size (bar <= 0.10) | 0.03 [0.00, 0.07]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.03 [0.00, 0.07] --> | 0.07 [0.02, 0.13]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.07 [0.02, 0.13] --> | 0.00 [0.00, 0.00]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.00 [0.00, 0.00] --> | 0.10 [0.04, 0.18]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.10 [0.04, 0.18] --> | 0.09 [0.00, 0.19]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.09 [0.00, 0.19] --> |
  | lookup, the rest alone (bar >= 0.6) | 0.91 [0.82, 0.97]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: 0.91 [0.82, 0.97] --> | 0.80 [0.70, 0.90]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: 0.80 [0.70, 0.90] --> | 0.81 [0.71, 0.91]<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: 0.81 [0.71, 0.91] --> | 0.93 [0.86, 0.98]<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: 0.93 [0.86, 0.98] --> | 0.81 [0.66, 0.94]<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: 0.81 [0.66, 0.94] --> |
  | the rule | **(c) neither<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| qwen35_9b_x49_1 :: (c) neither -->** | **(c) neither<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| x49_1_27b :: (c) neither -->** | **(c) neither<!-- src: results/x49_gain/x49_1-20261028T154510Z/x49_1.md \| muse30_x49_1 :: (c) neither -->** | **(c) neither<!-- src: results/x49_gain/x52_gain-20261029T021814Z/x49_1.md \| nem35l_x52_gain :: (c) neither -->** (no prediction) | **(c) neither<!-- src: results/x49_gain/x52_gain-20261030T094553Z/x49_1.md \| qwen35_122b_gain :: (c) neither -->** (no prediction) |

- **Read.**
  - The gain map fits neither reading fixed in advance on any model: on the 9B and Lightning a random part at the lens part's share also moves the recall; on the 27B and Muse the lens part alone moves the recall little even at twice its size. The rest alone moves the lookup on all five; the 122B (coverage †) reads like the 9B: a random part at the lens part's share moves its recall too.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning's lookup with the lens part at twice its size sits at the rule's 0.10 bar, its point estimate just above it.
  - Locker-first main-test scenes only.

</details>

### Do the two readers read two separate learned subspaces? <a id="t48-1"></a>

`ledger only` *Used in: README Appendix A, a figure link ("Muse's learned subspaces", figures/depth/readme/s14_das_muse.png).*

Test 48.1 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x48_das/x52_das-20261029T040955Z/verdict.md` · recompute: `scripts/x48_das.py` (the command in its docstring) · also: DAS at the bridge word; the 27B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At the bridge word at L, does each reader's switch run through its own small learned subspace, the recall's inside the lens part and the lookup's holding the address or a third identity code?
- **Why we asked.** Our parts are hand-built; a subspace trained for each reader tests the two-reader picture without that choice.
- **Data.** Pairs from the main test's locker-first scenes the whole change switches, split by bridge entity 60 / 20 / 20; the 27B's test pairs: lookup 10<!-- src: results/x48_das/x52_das-20261029T040955Z/verdict.md \| 10 (7) :: 10 -->, recall 8<!-- src: results/x48_das/x52_das-20261029T040955Z/verdict.md \| 8 (4) :: 8 -->.
- **Method.** Distributed alignment search per reader at k = 1, 4, 16, 64 directions; k chosen on the select split; own and cross interchange accuracy (IIA) on the test entities' pairs, against random and shuffled-target subspaces; the subspaces' energy inside the lens part, the address and the embedding directions.

![Neither reader has a learned subspace of its own](../../figures/depth/readme/s14_das_muse.png)

*Learned subspaces (DAS) at the bridge word on the 9B and Muse, per subspace size k (rows): the share of each reader's switches carried by its own learned subspace, the lookup's (violet) and the recall's (black), against a shuffled and a random subspace of the same size (grey). Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "(a) "two readers, two subspaces": own-IIA >= 0.7 at some k <= 16 for both readers, and cross-IIA <= 0.25 in both directions (paired CI excluding overlap with own-IIA). (b) "the recall's subspace is the lens's part": R_recall's energy inside the J++-25 part >= 0.5 (random R <= 0.15); R_lookup's <= 0.2. (c) "the address is part of the lookup's subspace": ||R_lookup^T U||_F^2 / 4 >= 0.5 (random R ~ k/d). (d) "a third identity code": R_lookup's energy outside (J++-25 u U u W_E-25) >= 0.5 while its own-IIA >= 0.7, and R_lookup alone gives identity answers >= 0.3 in the routes read." The 27B: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | the lookup's learned subspace: k chosen, held-out own-IIA (bar >= 0.7 at k <= 16) | k 1: 0.39 [0.08, 0.56]<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| 1 (chosen) :: 0.39 [0.08, 0.56] --> | k 16: 0.30 [0.07, 0.62]<!-- src: results/x48_das/x52_das-20261029T040955Z/verdict.md \| 16 (chosen) :: 0.30 [0.07, 0.62] --> | k 16: 0.62 [0.38, 1.00]<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| 16 (chosen) :: 0.62 [0.38, 1.00] --> | not run | not run |
  | the recall's learned subspace: k chosen, held-out own-IIA | k 4: 0.16 [0.00, 0.29]<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| 4 (chosen) :: 0.16 [0.00, 0.29] --> | k 16: 0.12 [0.00, 0.23]<!-- src: results/x48_das/x52_das-20261029T040955Z/verdict.md \| 16 (chosen) :: 0.12 [0.00, 0.23] --> | k 16: 0.00 [0.00, 0.00]<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| 16 (chosen) :: 0.00 [0.00, 0.00] --> | | |
  | the rules (a) / (b) / (c) / (d) | (a) no, (b) no, (c) no, (d) no<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| qwen35_9b_x48_das_r2 :: (a) no, (b) no, (c) no, (d) no --> | (a) no, (b) no, (c) no, (d) no<!-- src: results/x48_das/x52_das-20261029T040955Z/verdict.md \| x48_das_27b :: (a) no, (b) no, (c) no, (d) no --> | (a) no, (b) no, (c) no, (d) no<!-- src: results/x48_das/verdict-20261028T134153Z/verdict.md \| muse30_x48_das :: (a) no, (b) no, (c) no, (d) no --> | | |

- **Read.**
  - On none of the three models does each reader run through its own small learned subspace: at the chosen k neither reader's subspace carries 0.7 of its switches on held-out pairs, and (a) to (d) all fail.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 27B's run (r2) used BJ_DAS_GDN=torch, a run fix for the backward pass, as in 51.3 on the 27B.
  - Few test pairs (the 27B: 10 lookup, 8 recall).

</details>

### What is inside the lens part's 25 directions? <a id="b52-a"></a>

`in README` *Used in: README Part I card "What do the lens part's 25 directions stand for?".*

Test batch 52 A · opened 29 Oct · status: descriptive · hand-check: not in sample · files: `results/x52_atoms/report-20261029T000125Z/verdict.md` · recompute: `scripts/x52_atoms.py` (the command in its docstring) · also: Lightning's

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Which words do the 25 lens directions of the change stand for: the two bridge items, the answer words, or other words?
- **Why we asked.** The answer control tests the answer words only; the rest of the lens part was never looked at.
- **Data.** Main test, 50 locker-first items per model (Lightning at L14, main test only); the fact passages, 50 per model (9B, 27B, Muse).
- **Method.** Each of the 25 lens directions labelled by a word classifier (the bridge words with their spellings, the answer words, other classes); the share of the rebuilt energy per class, against a chance baseline.

![The lens part holds the two bridge words, almost never the answer](../../figures/common/readme/05_atoms.png)

*One bar per model: the lens part's directions, each counted by the word it decodes to, as shares of the energy they rebuild. The old and the new bridge word are the two teal segments, named above them; another scene word and no scene word are grey. The answer word (brick) has no visible segment: its share is printed at the right. Lightning hollow (○, post hoc).*

- **Rule, fixed in advance.** None: descriptive inventory, no rule.

</details>

- **Result.** (main test, recall's view)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | rebuilt energy in the original bridge word | 0.111 [0.091, 0.130]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.111 [0.091, 0.130] --> | 0.101 [0.075, 0.126]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.101 [0.075, 0.126] --> | 0.184 [0.165, 0.198]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.184 [0.165, 0.198] --> | 0.090 [0.073, 0.104]<!-- src: results/x52_atoms/report-20261029T010648Z/verdict.md \| Lightning e1 (recall's view :: 0.090 [0.073, 0.104] --> | 0.152 [0.128, 0.176]<!-- src: results/x52_atoms/report-20261030T094628Z/verdict.md \| 122B e1 (recall's view :: 0.152 [0.128, 0.176] --> |
  | in the new bridge word | 0.110 [0.093, 0.124]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.110 [0.093, 0.124] --> | 0.113 [0.096, 0.134]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.113 [0.096, 0.134] --> | 0.190 [0.168, 0.212]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.190 [0.168, 0.212] --> | 0.111 [0.089, 0.131]<!-- src: results/x52_atoms/report-20261029T010648Z/verdict.md \| Lightning e1 (recall's view :: 0.111 [0.089, 0.131] --> | 0.153 [0.130, 0.179]<!-- src: results/x52_atoms/report-20261030T094628Z/verdict.md \| 122B e1 (recall's view :: 0.153 [0.130, 0.179] --> |
  | in the recall's answer word | 0.001 [0.000, 0.002]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.001 [0.000, 0.002] --> | 0.001 [0.000, 0.002]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.001 [0.000, 0.002] --> | 0.001 [0.000, 0.003]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.001 [0.000, 0.003] --> | 0.000 [0.000, 0.000]<!-- src: results/x52_atoms/report-20261029T010648Z/verdict.md \| Lightning e1 (recall's view :: 0.000 [0.000, 0.000] --> | 0.000 [0.000, 0.000]<!-- src: results/x52_atoms/report-20261030T094628Z/verdict.md \| 122B e1 (recall's view :: 0.000 [0.000, 0.000] --> |
  | in other words | 0.765 [0.739, 0.796]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 9B e1 (recall's view :: 0.765 [0.739, 0.796] --> | 0.774 [0.739, 0.808]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| 27B e1 (recall's view :: 0.774 [0.739, 0.808] --> | 0.609 [0.584, 0.642]<!-- src: results/x52_atoms/report-20261029T000125Z/verdict.md \| Muse e1 (recall's view :: 0.609 [0.584, 0.642] --> | 0.787 [0.758, 0.818]<!-- src: results/x52_atoms/report-20261029T010648Z/verdict.md \| Lightning e1 (recall's view :: 0.787 [0.758, 0.818] --> | 0.688 [0.651<!-- src: results/x52_atoms/report-20261030T094628Z/verdict.md \| 122B e1 (recall's view :: 0.688 [0.651 --> |

- **Read.**
  - On the main test the two bridge words carry about a fifth (9B, 27B, Lightning) to two fifths (Muse) of the rebuilt energy, the answer words almost none (none at all on Lightning).

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The classifier was hand-checked on 5 items per model (blind on Muse's main test only) and misses non-English answer words.
  - On the fact passages the bridge names carry 0.02-0.03 and the descriptions' words dominate (see the report).

</details>

### Where is the answer readable through the lens, and can it be written there? <a id="b52-b"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test batch 52 B · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md` · recompute: `scripts/x52_answer_map.py` (the command in its docstring) · also: Lightning's main set 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** For each reader, on our scenes and on the fact passages, is the answer word readable through the lens before the answer is computed, and does writing its lens directions change the answer?
- **Why we asked.** The answer control found the answer word not read at our bridge word but read at the fact passages' description; where else is it readable, and is it used there?
- **Data.** Our main test, 200 per model (Lightning at L14, a coverage run, no prediction); the fact passages, 158 / 166 / 157 (Lightning's read pending).
- **Method.** Read: the answer word's rank in the lens readout at the bridge word, its earlier mention, the question and the last token, every second layer before the answer layer. Write: at the most readable cell, the answer word's lens directions at one and two times a real change's size, against a random part and a frequency-matched part of the same size; the whole change at that cell as the reference.

- **Rule, fixed in advance.** "“Readable”: the answer word in the lens top-5 on ≥ 0.5 of items at some layer before the answer layer. “Usable”: writing its directions changes the answer on ≥ 0.3 of items with the random control ≤ 0.10. Report the four combinations per reader, per dataset." No prediction.

Readable and usable, per reader and data set:

![On the fact passages the answer is readable and usable; on ours rarely](../../figures/depth/ledger/06_answer_map.png)

*Where the answer word is readable through the lens (left: the share of items with it in the lens top 5 at the best layer before the answer; one value, no interval) and whether adding its lens directions there changes the answer (right; at the size the run chose), lookup (violet) and recall (black), on our scenes and on the fact passages. Whiskers 95% intervals; Lightning and the 122B hollow ○ (coverage runs).*

</details>

- **Result.** (the combination; answers changed by the write at one / two times a real change's size)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | ours, lookup | **readable, not usable**: 0.01 [0.00, 0.02] / 0.01 [0.00, 0.02]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L24 0.69 :: 0.01 [0.00, 0.02] / 0.01 [0.00, 0.02] --> | **neither**: 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L0 0.10 :: 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] --> (cannot tell) | **neither**: 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L34 0.00 :: 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] --> (cannot tell) | **readable, not usable**: 0.01 [0.00, 0.02] / 0.10 [0.05, 0.14]<!-- src: results/x52_answer_map/x52cov-20261029T005848Z/verdict.md \| best T L38 0.91 :: 0.01 [0.00, 0.02] / 0.10 [0.05, 0.14] --> | **readable, not usable<!-- src: results/x52_answer_map/x52cov-20261030T045919Z/verdict.md \| qwen3.5-122b-a10b :: main :: lookup :: readable, not usable -->**: best top-5 0.95 at the last token, L44 |
  | ours, recall | **usable, not readable**: 0.37 [0.25, 0.51] / 0.03 [0.01, 0.06]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L28 0.32 :: 0.37 [0.25, 0.51] / 0.03 [0.01, 0.06] --> | **neither**: 0.08 [0.04, 0.14] / 0.20 [0.12, 0.31]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L46 0.15 :: 0.08 [0.04, 0.14] / 0.20 [0.12, 0.31] --> | **usable, not readable**: 0.70 [0.59, 0.84] / 0.09 [0.03, 0.15]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L36 0.05 :: 0.70 [0.59, 0.84] / 0.09 [0.03, 0.15] --> | **usable, not readable**: 0.65 [0.57, 0.74] / 0.01 [0.00, 0.03]<!-- src: results/x52_answer_map/x52cov-20261029T005848Z/verdict.md \| best T L46 0.41 :: 0.65 [0.57, 0.74] / 0.01 [0.00, 0.03] --> | **usable, not readable<!-- src: results/x52_answer_map/x52cov-20261030T045919Z/verdict.md \| qwen3.5-122b-a10b :: main :: recall :: usable, not readable -->** |
  | the fact passages, described, lookup | **readable and usable**: 0.63 [0.55, 0.72] / 0.55 [0.46, 0.64]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| ['E', 10] :: 0.63 [0.55, 0.72] / 0.55 [0.46, 0.64] --> | **readable and usable**: 0.17 [0.11, 0.23] / 0.80 [0.73, 0.86]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L62 1.00 :: 0.17 [0.11, 0.23] / 0.80 [0.73, 0.86] --> | **readable and usable**: 0.97 [0.94, 0.99] / 0.92 [0.87, 0.96]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L48 1.00 :: 0.97 [0.94, 0.99] / 0.92 [0.87, 0.96] --> | read pending | – |
  | the fact passages, described, recall | **readable and usable**: 0.61 [0.53, 0.69] / 0.55 [0.46, 0.64]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| ['E', 16] :: 0.61 [0.53, 0.69] / 0.55 [0.46, 0.64] --> | **readable and usable**: 0.86 [0.79, 0.91] / 0.84 [0.78, 0.90]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L60 1.00 :: 0.86 [0.79, 0.91] / 0.84 [0.78, 0.90] --> | **readable and usable**: 0.99 [0.97, 1.00] / 0.85 [0.79, 0.91]<!-- src: results/x52_answer_map/x52-20261029T004559Z/verdict.md \| best T L48 0.99 :: 0.99 [0.97, 1.00] / 0.85 [0.79, 0.91] --> | read pending | – |

- **Read.**
  - On the fact passages the answer word is readable and writing it changes the answer, for both readers on all three models.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  The recall's write at twice a real change's size, what the model outputs (a CPU check after the data, descriptive; results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md): the table counts the changed prompt's answer token, but at twice the size the recall's top token is mostly one of the written answer word's own tokens ("Four", "Six", ...), on 0.76<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 35 :: 0.76 --> / 0.84<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 39 :: 0.84 --> / 0.96<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 40 :: 0.96 --> of items (9B / Muse / Lightning); the changed prompt's answer token on 0.03<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 35 :: 0.03 --> / 0.09<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 39 :: 0.09 --> / 0.01<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 40 :: 0.01 -->, the original answer on 0.04<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 35 :: 0.04 --> / 0.03<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 39 :: 0.03 --> / 0.00<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | 'Four' 40 :: 0.00 -->. The 27B differs: its top token stays the original answer on 0.74<!-- src: results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md | recall | ans2 | 200 | 0.20 | 0.74 :: 0.74 -->.

More from the reading:

  - On our scenes the recall's answer is never readable before the answer layer, yet writing it at the last token moves the 9B's, Muse's and Lightning's recall; the lookup's is readable only on the 9B and Lightning, where writing it moves a tenth of answers or fewer.

- **Caveats.**
  - The 27B's and Muse's lookup cells on our scenes were written where nothing was readable and where the whole change itself switches nothing, so their "not usable" cannot tell (see the flags in the operations log).
  - Only the most readable cell was written; writing at the most readable cell other than the last token waits for Dan.
  - The output classes at twice the size are a CPU check read after the data; B stays out of the README (Dan).

</details>

## Part II. Identity: which item the lookup reads

### Does the lookup's identity route run outside the lens, or in lens directions beyond the recall's 25? <a id="t47-1"></a>

`in README` *Used in: README Part II card "Does the lookup's identity route run outside the lens?".*

Test 47.1 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_atoms/x47_1-20261028T113101Z/x47_1.md` · recompute: `scripts/x47_atoms.py` (the command in its docstring) · also: identity route outside the lens; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** The lookup barely needs the lens part's 25 directions; does its identity route sit in the next 75 lens directions, or outside the lens altogether?
- **Why we asked.** On the 27B, taking out 100 lens directions cut identity answers far more than a random part, so "outside the lens" might only mean "outside the recall's 25".
- **Data.** Routes scenes (another item moved), 300 per model, for identity answers; the main test, 200 per model, for the readers' switches.
- **Method.** The change's 100 best lens directions in order; directions 1-25, 26-100 or all 100 taken out at the bridge word at L, each against a random part of the same share.

![The lookup's identity route runs outside the lens; the position route never touches it](../../figures/depth/readme/18_identity_outside.png)

*Claim 5: switches blocked beyond a random part of the same size, lookup (violet) and recall (black), per model and per part taken out at the bridge word: the lens part, lens directions 26–100 (fixed in advance, filled), PCA directions of the same size, logit-lens directions and random lens directions (run after the data, hollow ○); grey band: within 0.10 of random; whiskers 95% intervals.*

- **Rule, fixed in advance.** "(a) "the lookup's identity route sits in lens atoms beyond the recall's 25": without 26-100, identity answers fall >= 0.30 beyond the random part (paired CI excluding 0) and the recall's extra drop without 26-100 is <= 0.10, on >= 2 of 3 models; (b) "continuum": both readers has >= 0.20 blocked beyond random without 26-100; (c) "outside the lens": without 26-100, identity answers fall < 0.10 beyond random." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | identity answers blocked without lens directions 1-25, beyond random | 0.06 [0.02, 0.09]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.5-9b :: 1-25 :: 0.06 [0.02, 0.09] --> | 0.25 [0.21, 0.29]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.6-27b :: 1-25 :: 0.25 [0.21, 0.29] --> | 0.00 [-0.02, 0.02]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| muse-glimmer-30b :: 1-25 :: 0.00 [-0.02, 0.02] --> | 0.04 [0.01, 0.06]<!-- src: results/x47_atoms/x52_atoms47-20261029T011717Z/x47_1.md \| nemotron-3.5-lightning :: 1-25 :: 0.04 [0.01, 0.06] --> | not tested (routes gate: the recall reads 0.797<!-- src: results/x6_routes/qwen35_122b_routes_x47_1/gate.json \| "PM": 0.7971428571428572 :: 0.797 --> < 0.80) |
  | the same without directions 26-100 | 0.05 [0.02, 0.08]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.5-9b :: 26-100 :: 0.05 [0.02, 0.08] --> | 0.05 [0.03, 0.08]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.6-27b :: 26-100 :: 0.05 [0.03, 0.08] --> | 0.02 [-0.00, 0.04]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| muse-glimmer-30b :: 26-100 :: 0.02 [-0.00, 0.04] --> | 0.05 [0.01, 0.08]<!-- src: results/x47_atoms/x52_atoms47-20261029T011717Z/x47_1.md \| nemotron-3.5-lightning :: 26-100 :: 0.05 [0.01, 0.08] --> | |
  | the same without directions 1-100 | 0.09 [0.05, 0.13]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.5-9b :: 1-100 :: 0.09 [0.05, 0.13] --> | 0.55 [0.50, 0.60]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen3.6-27b :: 1-100 :: 0.55 [0.50, 0.60] --> | 0.02 [0.00, 0.03]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| muse-glimmer-30b :: 1-100 :: 0.02 [0.00, 0.03] --> | -0.08 [-0.12, -0.04]<!-- src: results/x47_atoms/x52_atoms47-20261029T011717Z/x47_1.md \| nemotron-3.5-lightning :: 1-100 :: -0.08 [-0.12, -0.04] --> | |
  | recall: switches blocked without 26-100, beyond random (main test) | 0.03 [0.00, 0.06]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen35_9b_x47_1_main :: 0.03 [0.00, 0.06] --> | 0.05 [0.01, 0.10]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| x47_1_main_27b :: 0.05 [0.01, 0.10] --> | 0.01 [-0.05, 0.08]<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| muse30_x47_1_main :: 0.01 [-0.05, 0.08] --> | 0.01 [-0.02, 0.04]<!-- src: results/x47_atoms/x52_atoms47-20261029T011717Z/x47_1.md \| nem35l_x52_x47_1_main :: 0.01 [-0.02, 0.04] --> | – |
  | the rule's label | **(c) outside the lens<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| qwen35_9b_x47_1_main :: (c) outside the lens -->** | **(c) outside the lens<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| x47_1_main_27b :: (c) outside the lens -->** | **(c) outside the lens<!-- src: results/x47_atoms/x47_1-20261028T113101Z/x47_1.md \| muse30_x47_1_main :: (c) outside the lens -->** | **(c) outside the lens<!-- src: results/x47_atoms/x52_atoms47-20261029T011717Z/x47_1.md \| nem35l_x52_x47_1_main :: (c) outside the lens -->** (no prediction) | not tested (gate) |

- **Read.**
  - On all four models the lookup's identity answers survive taking out lens directions 26-100 (under 0.10 beyond random): its identity route runs outside the lens, not in the lens beyond the recall's 25.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Only the 27B drops identity answers to directions 1-25 or to all 100 (redundant copies); on Lightning taking out all 100 costs less than a random part of their share.

- **Caveats.**
  - The 122B (coverage, 30 Oct): the routes part not tested at its gate; on the main test without lens directions 26-100 its recall is blocked at 0.00 [-0.03, 0.03]<!-- src: results/x0_necessity/qwen35_122b_x47_1_main/verdict-20261029T212308Z/verdict.md | jpp26_100 :: PM :: 0.00 [-0.03, 0.03] --> and its lookup -0.02 [-0.09, 0.04]<!-- src: results/x0_necessity/qwen35_122b_x47_1_main/verdict-20261029T212308Z/verdict.md | jpp26_100 :: PP :: -0.02 [-0.09, 0.04] --> beyond random (both around the lens part; descriptive).
  - Lightning's verdict prints "(a) for the batch: does not hold (0 of 1 models; at least 2 needed)": that applies the across-models clause to one model and is not a result; the per-model label is the result.
  - Identity is read on routes scenes, the recall's switches on the main test: two scene sets.

</details>

### Which route does the lookup take, and does the address carry the position route? <a id="routes"></a>

`in README` `below gate: 122B` *Used in: README Part II card "Which route does the lookup take: the item's identity, its locker's position, or the number?"; README Part III card "Can the address be read, removed, added and swapped?" (removing and adding the address).*

Test routes test · opened 29 Oct · status: rule fixed in advance · hand-check: in sample (view c) · files: `results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z/verdict.md` · recompute: `scripts/x6_routes.py` (the command in its docstring) · also: Lightning's coverage run

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When another item's locker sentence moves and takes a new number, does the lookup follow the item's identity, its locker's position, or the number, and is the position route carried by the address?
- **Why we asked.** The conflict test says the lookup follows the rest of the bridge word; the routes test says what in it the lookup reads.
- **Data.** Routes scenes, 300 per model (Lightning at L14, its gate chosen after the 60-scene pre-check was seen, ○).
- **Method.** The change from a prompt where another item's locker sentence moved and took a new number; each route predicts a different locker. Arms: the whole change; without the address, against without a random part of its share; the address added by itself, against a random part. A sanity swap (two picks swap, no move) first.

![Every model's lookup takes identity or position, never the value](../../figures/common/readme/08_routes.png)

*Shares of the lookup's answers by route when another item moves, per model: identity, position, other; 95% intervals over bridge entities, n = 300 scenes per model; Lightning and the 122B hollow ○ (post hoc gates). The routes scenes are not among the hand-checked views.*

- **Rule, fixed in advance.** "A route counts as used if its share is >= 0.20 with lower CI >= 0.10." The sanity swap must reproduce the one-pick lookup switch rate within 0.10; Lightning has no one-pick reference, so it takes Muse's rule (switch rate >= 0.50).

</details>

- **Result.** (another item moved)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | whole change: identity | 0.48 [0.43, 0.53]<!-- src: results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z/verdict.md \| 0.51 [0.46, 0.56] :: 0.48 [0.43, 0.53] --> | 0.66 [0.60, 0.71]<!-- src: results/x6_routes/x6_routes_27b/verdict-20261025T105901Z/verdict.md \| 0.34 [0.28, 0.39] :: 0.66 [0.60, 0.71] --> | 0.44 [0.38, 0.49]<!-- src: results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z/verdict.md \| 0.54 [0.49, 0.60] :: 0.44 [0.38, 0.49] --> | 0.44 [0.38, 0.51]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| 0.55 [0.49, 0.62] :: 0.44 [0.38, 0.51] --> | ○ 0.61 [0.56, 0.67]<!-- src: results/x6_routes/qwen35_122b_x6_routes_g75/verdict-20261025T134214Z/verdict.md \| C2 :: whole :: 300 :: 0.61 [0.56, 0.67] --> |
  | whole change: position | 0.51 [0.46, 0.56]<!-- src: results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z/verdict.md \| 0.48 [0.43, 0.53] :: 0.51 [0.46, 0.56] --> | 0.34 [0.28, 0.39]<!-- src: results/x6_routes/x6_routes_27b/verdict-20261025T105901Z/verdict.md \| 0.66 [0.60, 0.71] :: 0.34 [0.28, 0.39] --> | 0.54 [0.49, 0.60]<!-- src: results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z/verdict.md \| 0.44 [0.38, 0.49] :: 0.54 [0.49, 0.60] --> | 0.55 [0.49, 0.62]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| 0.44 [0.38, 0.51] :: 0.55 [0.49, 0.62] --> | ○ 0.38 [0.33, 0.44]<!-- src: results/x6_routes/qwen35_122b_x6_routes_g75/verdict-20261025T134214Z/verdict.md \| C2 :: whole :: 300 :: 0.38 [0.33, 0.44] --> |
  | position without the address | 0.08 [0.05, 0.12]<!-- src: results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z/verdict.md \| 0.55 [0.50, 0.61] :: 0.08 [0.05, 0.12] --> | 0.06 [0.03, 0.09]<!-- src: results/x6_routes/x6_routes_27b/verdict-20261025T105901Z/verdict.md \| 0.21 [0.18, 0.25] :: 0.06 [0.03, 0.09] --> | 0.27 [0.23, 0.32]<!-- src: results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z/verdict.md \| 0.29 [0.25, 0.35] :: 0.27 [0.23, 0.32] --> | 0.10 [0.07, 0.14]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| 0.58 [0.53, 0.64] :: 0.10 [0.07, 0.14] --> | ○ 0.05 [0.02, 0.07]<!-- src: results/x6_routes/qwen35_122b_x6_routes_g75/verdict-20261025T134214Z/verdict.md \| C2 :: no_alf :: 300 :: 0.05 [0.02, 0.07] --> |
  | the same without a random part | 0.54 [0.49, 0.59]<!-- src: results/x6_routes/qwen35_9b_x6_routes/verdict-20261025T104535Z/verdict.md \| 0.06 [0.03, 0.08] :: 0.54 [0.49, 0.59] --> | 0.25 [0.19, 0.31]<!-- src: results/x6_routes/x6_routes_27b/verdict-20261025T105901Z/verdict.md \| 0.70 [0.64, 0.76] :: 0.25 [0.19, 0.31] --> | 0.55 [0.50, 0.60]<!-- src: results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z/verdict.md \| 0.41 [0.36, 0.46] :: 0.55 [0.50, 0.60] --> | 0.56 [0.49, 0.63]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| 0.42 [0.35, 0.48] :: 0.56 [0.49, 0.63] --> | ○ 0.36 [0.31, 0.41]<!-- src: results/x6_routes/qwen35_122b_x6_routes_g75/verdict-20261025T134214Z/verdict.md \| C2 :: no_alf_rand :: 300 :: 0.36 [0.31, 0.41] --> |
  | position, the address alone | 0.26 [0.20, 0.32]<!-- src: results/x6_routes/qwen35_9b_x6_routes_keeponly/verdict-20261025T152603Z/verdict.md \| 0.72 [0.65, 0.78] :: 0.26 [0.20, 0.32] --> | 0.09 [0.06, 0.12]<!-- src: results/x6_routes/x6_routes_keeponly_27b/verdict-20261025T153505Z/verdict.md \| 0.88 [0.84, 0.91] :: 0.09 [0.06, 0.12] --> | 0.29 [0.25, 0.34]<!-- src: results/x6_routes/muse30b_x6_routes/verdict-20261026T004455Z/verdict.md \| 0.66 [0.61, 0.71] :: 0.29 [0.25, 0.34] --> | 0.40 [0.35, 0.45]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| 0.53 [0.48, 0.58] :: 0.40 [0.35, 0.45] --> | ○ 0.21 [0.16, 0.26]<!-- src: results/x6_routes/qwen35_122b_x6_routes_keeponly_g75/verdict-20261025T202506Z/verdict.md \| C2 :: keep_alf :: 300 :: 0.21 [0.16, 0.26] --> |

- **Read.**
  - On all four models the lookup answers by the item's identity or its locker's position, never by the new number; removing the address takes the position route away beyond a random part of its share.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  Lightning's sanity swap switches 0.99<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| | C0 | PP | jpp | 300 | :: 0.99 --> of lookups (rule: at least 0.50); removing the lens part there costs the lookup -0.00 [-0.02, 0.01]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| | C0 | PP | jpp | 300 | 0.99 | :: -0.00 [-0.02, 0.01] --> beyond random, removing the address 0.54 [0.48, 0.61]<!-- src: results/x6_routes/nem35l_x52_routes/verdict-20261029T004324Z/verdict.md \| | C0 | PP | alf | 300 | 0.99 | :: 0.54 [0.48, 0.61] -->; the value: 0.00 on every model.

- **Caveats.**
  - The 122B (FP8; MoE, ~10B active): not tested (gate 0.797<!-- src: results/x6_routes/qwen35_122b_x6_routes_c0/gate.json \| "PM" :: 0.797 --> < 0.80) on the routes scenes; its g75 runs lowered the gate to 0.75 after the data (the README's °): below gate, exploratory, hollow ○, never in claims or grades. Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones.
  - Added by itself, the address brings position answers back on the 9B, Muse and Lightning, not on the 27B.
  - Lightning's gate was chosen after the 60-scene pre-check was seen; its sanity swap uses Muse's rule.

</details>

### Does the lookup never take the value, in prose, JSON and tables too? <a id="t47-7c"></a>

`ledger only` `below gate: 9B, Muse, Lightning` *Used in: not in the README (its rebuild).*

Test 47.7 (c) · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_value/x47_7c-20261028T123632Z/x47_7c.md` · recompute: `scripts/x47_value.py` (the command in its docstring) · also: never the value by format; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** In varied scenes (prose, JSON, tables) where another item moved and took a new number, does the lookup's answer ever follow the number (the value route)?
- **Why we asked.** On simple scenes the lookup never takes the value; "in any format" needs the formats.
- **Data.** Varied scenes, locker first, question last, per format that passes the gate (the recall right on at least 0.80 of the original prompts); n per cell in the verdicts.
- **Method.** The routes test's whole change at the bridge word at L, per format; the lookup's answer sorted into identity, position, value and original; the per-format refit address taken out against a random part (9B, Muse, Lightning).

- **Rule, fixed in advance.** "never the value generalizes if value <= 0.05 in every format on every model; a position route in JSON / table if the position share >= 0.2 and the refit pointer's [pointer: the address] removal cuts it >= 0.3 beyond random." Lightning: a coverage run on this rule, no prediction.

The position and value routes per format:

![In prose, JSON and tables the lookup never takes the value](../../figures/depth/ledger/07_value_formats.png)

*The routes test in prose, JSON and a table: the share of the lookup's answers that follow the moved item's position (orange) and its new value (slate), per model and format run. Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | value share, prose (bar <= 0.05) | 0.01 [0.00, 0.03]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.5-9b :: prose :: 119 :: 0.01 [0.00, 0.03] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.6-27b :: prose :: 300 :: 0.00 [0.00, 0.00] --> | not tested (gate 0.74<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| muse-glimmer-30b :: prose :: 0.74 --> < 0.80) | not tested (gate 0.786<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| nemotron-3.5-lightning :: prose :: 0.786 --> < 0.80) | not run |
  | value share, JSON (bar <= 0.05) | not tested (gate 0.7857<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.5-9b :: json :: 0.7857 --> < 0.80) | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.6-27b :: json :: 155 :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| muse-glimmer-30b :: json :: 75 :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| nemotron-3.5-lightning :: json :: 56 :: 0.00 [0.00, 0.00] --> | |
  | value share, table (bar <= 0.05) | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.5-9b :: table :: 118 :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| qwen3.6-27b :: table :: 300 :: 0.00 [0.00, 0.00] --> | not tested (gate 0.776978<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| muse-glimmer-30b :: table :: 0.776978 --> < 0.80) | not tested (gate 0.788<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| nemotron-3.5-lightning :: table :: 0.788 --> < 0.80) | |
  | the verdict | **incomplete<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| Verdict :: incomplete -->** | **incomplete<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| Verdict :: incomplete -->** | **incomplete<!-- src: results/x47_value/x47_7c-20261028T123632Z/x47_7c.md \| Verdict :: incomplete -->** | **incomplete<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| Verdict :: incomplete -->** (no prediction) | |

- **Read.**
  - Wherever a format passes the gate, the lookup never takes the value, on all four models; the verdict stays incomplete because some formats fail the gate.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The gate reads the recall on question-last prompts: prose and tables fail it on Muse and Lightning, JSON on the 9B.
  - Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones (Muse's and Lightning's table gates).
  - No format shows a position route by the rule: Lightning's JSON position share 0.36 [0.27, 0.44]<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| nemotron-3.5-lightning :: json :: 56 :: 0.36 [0.27, 0.44] --> is cut by 0.18 [0.11, 0.26]<!-- src: results/x47_value/x52_valuec-20261029T040037Z/x47_7c.md \| nemotron-3.5-lightning :: json :: 56 :: 0.18 [0.11, 0.26] --> by the refit address, under 0.3.

</details>

### Does a learned subspace carry the readers' codes, and is the learned address ours? <a id="t51-3"></a>

`ledger only` *Used in: README Appendix A, a figure link ("learned subspaces", figures/depth/readme/33_learned.png).*

Test 51.3 · opened 28 Oct · status: rule fixed in advance (part descriptive) · hand-check: not in sample · files: `results/x51_das/verdict-20261028T194630Z/verdict.md` · recompute: `scripts/x51_das.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Does a learned (DAS) subspace of at most 128 directions carry the recall's identity switch, where does the lookup's learned subspace lie, and does the learned 4-direction address overlap ours?
- **Why we asked.** Our parts are hand-built (lens directions, slot means); a trained subspace tests them without that choice.
- **Data.** Identity pairs from the main, clean and routes scenes (9B: 514 recall pairs; 27B 374; Muse 300), test entities held out; routes position pairs for the address.
- **Method.** Distributed alignment search: a subspace trained to carry the switch, its own interchange accuracy on test pairs, against a random subspace and a shuffled-target subspace of the same size.

![Learned subspaces carry each reader's item switch; random ones none](../../figures/depth/readme/33_learned.png)

*A small address subspace learned on the address test's pairs (its size in the figure's note), on the 9B, the 27B and Muse: the share of position switches it carries (amber) against a random subspace (grey); the recalls it moves; the whole change and the hand-built address's energy inside it in their own columns. Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "Q51.3 (i) 'found' = >= 300 recall pairs and test own-IIA >= 0.5 at some k <= 128; (ii) the lookup subspace (R_lookup at its chosen k) on the test pairs: the share of R R^T Delta inside U, the J++-25 atoms, the W_E-25 atoms and outside their union, each part >= 0.5 named 'mostly' (descriptive; the parts overlap); (iii) U's energy in R_pos at k = 4 = ||R_pos^T U||_F^2 / rank U >= 0.6" (verdict.md, as computed)

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (i) recall, test own-IIA at k = 128 | 0.96 [0.91, 0.99]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 514 :: 0.96 [0.91, 0.99] --> | 0.80 [0.67, 0.91]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 374 :: 0.80 [0.67, 0.91] --> | 0.80 [0.64, 0.96]<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| recall pairs 300 :: 0.80 [0.64, 0.96] --> | not run | not run |
  | (ii) the lookup subspace (k = 4) outside our parts | 0.62<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| in U 0.36 :: in outside 0.62 :: 0.62 --> | 0.62<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| U's energy in R_lookup 0.2509 :: 0.62 --> | 0.72<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| in outside 0.72 :: 0.72 --> | | |
  | (iii) our address's energy in the learned address | 0.246<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.246 --> | 0.226<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.226 --> | 0.193<!-- src: results/x51_das/verdict-20261028T194630Z/verdict.md \| overlaps U >= 0.6: no :: 0.193 --> | | |
  | the rule (i) / (ii) / (iii) | found / mostly outside / no | found / mostly outside / no | found / mostly outside / no | | |

- **Read.**
  - A learned subspace carries the recall's identity on all three; the lookup's lies mostly outside our parts, and the learned address holds about a quarter of ours.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Few test entities (9 on the 9B's identity pairs).
  - (ii) and (iii) have no interval in the verdict's summary lines.

</details>

### Is the item's identity at its locker sentence the code the lookup reads at the bridge word? <a id="b53-8"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 53.8 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md` · recompute: `scripts/x53_bindid.py` (the command in its docstring) · also: a binding-ID test; the 9B, the 27B and Muse, 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Is the item's identity at its mention in its locker sentence a code the lookup reads at the bridge word: added there, does it send lookups to that item's locker?


- **Why we asked.** The lookup reads an identity code outside the lens part beside the address ([47.1](#t47-1), [routes](#routes)); a binding-ID code would be one vector shared by the item's mention and the bridge word.

- **Data.** Routes scenes without a move, 300 test scenes per model (the 9B at L12, 31 bridge items; the 27B at L32, 32; Muse at L26, 32), every gate passed; the vectors from 300 held-out scenes. Lightning not designed.

- **Method.** At L, the state at item X's mention in its locker sentence minus X's token embedding (mean over the held-out scenes, X fixed by slot), added at the bridge word at 1x and 2x the size of a real identity change; controls: a random vector of the same norm, and Y's version (another item's mention). Read: lookups sent to X's locker. Beside (Dan 12:10, before any run): a centered arm, each slot's vector minus the mean over slots, same doses and controls; and (Dan 13:15, CPU) how much of each centered slot vector lies in the address U.

- **Rule, fixed in advance.** "Rule: "a shared identity code" if X's share minus random >= 0.25 at 2x and minus Y's version >= 0.15; "no" if <= 0.05; else in between." (jobs/c3/batch53.yaml, critic_1125 item 6, Dan 11:25; no prediction) The centered arm (decisions_1210b item 1, Dan 12:10, before any run): "the same rule thresholds reported for it beside"; the headline stays the uncentered arm's (Dan 13:15).


The identity code against another item's version and a random vector:

![Centered, the code moves lookups beyond random; raw, little or none](../../figures/depth/ledger/08_identity_code.png)

*The item's identity code from its locker sentence added at the bridge word: the share of lookups moved by the item's own code (blue), by another item's version of it (slate) and by a random vector (grey), with the code as fit in advance and centered. Whiskers 95% intervals.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | pre-specified (uncentered), at 2x: X's locker under X's vector / Y's version / random | 0.02 [0.01, 0.03]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: 0.02 [0.01, 0.03] --> / 0.01 [0.01, 0.02]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: 0.01 [0.01, 0.02] --> / 0.02 [0.01, 0.03]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: 0.02 [0.01, 0.03] --> | 0.11 [0.09, 0.13]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: 0.11 [0.09, 0.13] --> / 0.07 [0.05, 0.10]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: 0.07 [0.05, 0.10] --> / 0.08 [0.06, 0.09]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: 0.08 [0.06, 0.09] --> | 0.33 [0.30, 0.36]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.33 [0.30, 0.36] --> / 0.27 [0.25, 0.30]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.27 [0.25, 0.30] --> / 0.18 [0.16, 0.20]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.18 [0.16, 0.20] --> | not designed | not run |
  | the same: X minus random / X minus Y | 0.00 [-0.01, 0.01]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: 0.00 [-0.01, 0.01] --> / 0.00 [-0.00, 0.01]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: 0.00 [-0.00, 0.01] --> | 0.03 [0.01, 0.05]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: 0.03 [0.01, 0.05] --> / 0.04 [0.02, 0.05]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: 0.04 [0.02, 0.05] --> | 0.15 [0.12, 0.18]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.15 [0.12, 0.18] --> / 0.06 [0.03, 0.08]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.06 [0.03, 0.08] --> | | |
  | the rule (the headline) | **no<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.00 [-0.00, 0.01] :: no -->** | **no<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.02, 0.05] :: no -->** | **in between<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: in between -->** | | |
  | centered (beside), at 2x: X / Y's version / random | 0.25 [0.21, 0.29]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: 0.25 [0.21, 0.29] --> / 0.12 [0.09, 0.15]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: 0.12 [0.09, 0.15] --> / 0.02 [0.01, 0.03]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: 0.02 [0.01, 0.03] --> | 0.18 [0.15, 0.21]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: 0.18 [0.15, 0.21] --> / 0.14 [0.12, 0.16]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: 0.14 [0.12, 0.16] --> / 0.08 [0.06, 0.09]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: 0.08 [0.06, 0.09] --> | 0.45 [0.41, 0.48]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: 0.45 [0.41, 0.48] --> / 0.28 [0.26, 0.31]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: 0.28 [0.26, 0.31] --> / 0.18 [0.16, 0.20]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: 0.18 [0.16, 0.20] --> | | |
  | the same: X minus random / X minus Y | 0.23 [0.19, 0.27]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: 0.23 [0.19, 0.27] --> / 0.13 [0.08, 0.17]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: 0.13 [0.08, 0.17] --> | 0.10 [0.08, 0.13]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: 0.10 [0.08, 0.13] --> / 0.04 [0.00, 0.07]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: 0.04 [0.00, 0.07] --> | 0.27 [0.24, 0.29]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: 0.27 [0.24, 0.29] --> / 0.16 [0.13, 0.19]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: 0.16 [0.13, 0.19] --> | | |
  | centered, by the same thresholds | in between<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 31 items) :: 0.13 [0.08, 0.17] :: in between --> | in between<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: 0.04 [0.00, 0.07] :: in between --> | a shared identity code<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.16 [0.13, 0.19] :: a shared identity code --> | | |
  | the centered slot vectors in U: cos² per slot / a random vector's mean (99th percentile) | 0.0036<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| qwen35_9b_x0_probe_v4 :: 4 / 4096 :: 0.0036 --> / 0.0336<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| qwen35_9b_x0_probe_v4 :: 4 / 4096 :: 0.0336 --> / 0.0054<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| qwen35_9b_x0_probe_v4 :: 4 / 4096 :: 0.0054 --> / 0.00100<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| qwen35_9b_x0_probe_v4 :: 4 / 4096 :: 0.00100 --> (0.00330<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| qwen35_9b_x0_probe_v4 :: 4 / 4096 :: 0.00330 -->) | 0.0047<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| x0_probe_v4_27b :: 4 / 5120 :: 0.0047 --> / 0.0044<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| x0_probe_v4_27b :: 4 / 5120 :: 0.0044 --> / 0.0078<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| x0_probe_v4_27b :: 4 / 5120 :: 0.0078 --> / 0.00080<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| x0_probe_v4_27b :: 4 / 5120 :: 0.00080 --> (0.00257<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| x0_probe_v4_27b :: 4 / 5120 :: 0.00257 -->) | 0.0449<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| muse30b_x0_probe_v4 :: 4 / 6656 :: 0.0449 --> / 0.0186<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| muse30b_x0_probe_v4 :: 4 / 6656 :: 0.0186 --> / 0.0455<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| muse30b_x0_probe_v4 :: 4 / 6656 :: 0.0455 --> / 0.00061<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| muse30b_x0_probe_v4 :: 4 / 6656 :: 0.00061 --> (0.00197<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| muse30b_x0_probe_v4 :: 4 / 6656 :: 0.00197 -->) | | |
  | the raw slot vectors' cosines / the slot-specific part's share of the norm | 0.8656<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - 9B: cosines between slot vectors :: 0.8656 --> to 0.9743<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - 9B: cosines between slot vectors :: 0.9743 --> / 0.178<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 33.65 :: 5.98 :: 0.178 --> to 0.315<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 34.16 :: 10.75 :: 0.315 --> | 0.8554<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - 27B: cosines between slot vectors :: 0.8554 --> to 0.9587<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - 27B: cosines between slot vectors :: 0.9587 --> / 0.206<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 79.42 :: 16.40 :: 0.206 --> to 0.331<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 79.37 :: 26.24 :: 0.331 --> | 0.8169<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - Muse: cosines between slot vectors :: 0.8169 --> to 0.9632<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| - Muse: cosines between slot vectors :: 0.9632 --> / 0.196<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 305.67 :: 60.04 :: 0.196 --> to 0.447<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 246.33 :: 110.15 :: 0.447 --> | | |

- **Read.**
  - The pre-specified vectors: no on the 9B and the 27B (about as many lookups to X's locker as a random vector); in between on Muse, where X's vector beats random but Y's version comes close.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The slot vectors are nearly parallel on both models: a shared component dominates them. Centered, the slot-specific part sends lookups to X's locker: in between on the 9B and the 27B, a shared identity code by the same thresholds on Muse.
  - The centered slot vectors lie in the address U above a random vector's 99th percentile on every slot of the three models, but at most a few percent of their energy (cos² at most 0.0455 on Muse): "not high" (decisions_1810 item 1).


- In the decision's words: the centered arm moves lookups in between (X 0.25, Y 0.12, random 0.02; the 9B's cells) and its vector lies mostly outside the address U, consistent with [51.3](#t51-3) (the lookup's code mostly outside U); the uncentered pre-specified arm says no.

- **Caveats.**
  - The centered arm was added by Dan (12:10) before any run; the headline is the uncentered arm.
  - On Muse a random vector alone sends 0.18 [0.16, 0.20]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 600 (300 scenes, 32 items) :: 0.06 [0.03, 0.08] :: 0.18 [0.16, 0.20] --> of lookups to X's locker at 2x.
  - Whether "the centered arm re-finds the address" ("if high") waits for a decided bar; the cos² are reported as they are.
  - Centered at 2x, the clean answers suffer: the lookup's answer stays unchanged on 0.63 [0.58, 0.69]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 9B :: ccode_x2 :: 600 :: 0.63 [0.58, 0.69] --> of scenes on the 9B and 0.27 [0.22, 0.32]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| Muse :: ccode_x2 :: 600 :: 0.27 [0.22, 0.32] --> on Muse; on the 27B the lookup keeps it on 0.68 [0.64, 0.71]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: ccode_x2 :: 600 :: 0.68 [0.64, 0.71] --> and the recall on 0.98 [0.95, 1.00]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: ccode_x2 :: 600 :: 0.98 [0.95, 1.00] -->, where a real identity change sends the lookup to B's locker 0.98 [0.96, 1.00]<!-- src: results/x53_bindid/x53_bindid-20261029T122650Z/verdict.md \| 27B :: whole: lookup sent to B :: 0.98 [0.96, 1.00] -->.
  - Exploratory (batch 53), no prediction.

</details>

## Part III. The address: where the item's locker sits

### Is the address readable at the bridge word? <a id="probe"></a>

`in README` *Used in: README Part III card "Can the address be read, removed, added and swapped?" (the probe).*

Test x0_probe v4 · opened not stated · status: post hoc (descriptive) · hand-check: not in sample · files: `results/x0_probe/qwen35_9b_x0_probe_v4/probe-20261024T172340Z/probe.md` · recompute: `scripts/x0_probe.py` (the command in its docstring) · also: the address probe; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At the bridge word at L, can a probe read which locker sentence holds the item's locker, beyond what the layout of the scene gives away, and does it read the answer digit itself?
- **Why we asked.** If the bridge word stores an address rather than the answer, the locker sentence should be readable and the digit should not.
- **Data.** Every scene of the topic scenes, split by whether the item's locker sentence comes before or after the asked pick (see the table's n in the verdicts).
- **Method.** Probes on the bridge word's state at L, cross-validated by bridge entity: the locker sentence's place, the answer digit and the bridge's identity; baselines: the majority class, the pick's sentence index, the visible layout.

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/06_address_read_remove.png)

*Left: a probe at the bridge word reads which locker sentence holds the item's locker (the address, amber), against a probe trained on the layout only (grey). Right: the lookups that still answer by position when the address is removed from the patch (amber), against a random part of the same size removed instead (grey); lower means more blocked. Whiskers: 95% intervals. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/07_address_swap_lens.png)

*Left: the lookups sent to the new locker when another locker's address is swapped in at about a real change's size (amber), against a random vector of the same size (grey). Right: how far above 200 random vectors the lens's 25 directions rebuild that swap (amber), against a change of item of the same size (blue, the positive control), in z; grey band: the range of the 200 random vectors. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

This card is the figure's first column.

- **Rule, fixed in advance.** None: descriptive, added after the data (Dan, 24 Oct evening). The reading stated beside: "(b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction." Lightning: a coverage run, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | which locker sentence, locker before the pick (chance 0.20) | 0.97 [0.96, 0.98]<!-- src: results/x0_probe/qwen35_9b_x0_probe_v4/probe-20261024T172340Z/probe.md \| before :: locker sentence :: 758 :: 0.97 [0.96, 0.98] --> | 0.99 [0.98, 1.00]<!-- src: results/x0_probe/x0_probe_v4_27b/probe-20261024T172424Z/probe.md \| before :: locker sentence :: 758 :: 0.99 [0.98, 1.00] --> | 0.97 [0.95, 0.98]<!-- src: results/x0_probe/muse30b_x0_probe_v4/probe-20261026T000115Z/probe.md \| before :: locker sentence :: 657 :: 0.97 [0.95, 0.98] --> | 0.85 [0.81, 0.88]<!-- src: results/x0_probe/nem35l_x52_probe/probe-20261029T002432Z/probe.md \| before :: locker sentence :: 636 :: 0.85 [0.81, 0.88] --> | 0.92 [0.90, 0.94]<!-- src: results/x0_probe/qwen35_122b_x0_probe_v4/probe-20261024T230718Z/probe.md \| before :: locker sentence :: 0.92 [0.90, 0.94] --> |
  | the same from the layout alone (best baseline) | 0.53 [0.50, 0.56]<!-- src: results/x0_probe/qwen35_9b_x0_probe_v4/probe-20261024T172340Z/probe.md \| before :: locker sentence :: 758 :: 0.53 [0.50, 0.56] --> | 0.53 [0.50, 0.56]<!-- src: results/x0_probe/x0_probe_v4_27b/probe-20261024T172424Z/probe.md \| before :: locker sentence :: 758 :: 0.53 [0.50, 0.56] --> | 0.53 [0.49, 0.56]<!-- src: results/x0_probe/muse30b_x0_probe_v4/probe-20261026T000115Z/probe.md \| before :: locker sentence :: 657 :: 0.53 [0.49, 0.56] --> | 0.52 [0.49, 0.54]<!-- src: results/x0_probe/nem35l_x52_probe/probe-20261029T002432Z/probe.md \| before :: locker sentence :: 636 :: 0.52 [0.49, 0.54] --> | 0.53 [0.50, 0.56]<!-- src: results/x0_probe/qwen35_122b_x0_probe_v4/probe-20261024T230718Z/probe.md \| before :: locker sentence :: 0.53 [0.50, 0.56] --> |
  | which locker sentence, locker after the pick (the control) | 0.34 [0.30, 0.37]<!-- src: results/x0_probe/qwen35_9b_x0_probe_v4/probe-20261024T172340Z/probe.md \| after :: locker sentence :: 742 :: 0.34 [0.30, 0.37] --> | 0.34 [0.31, 0.37]<!-- src: results/x0_probe/x0_probe_v4_27b/probe-20261024T172424Z/probe.md \| after :: locker sentence :: 742 :: 0.34 [0.31, 0.37] --> | 0.34 [0.31, 0.37]<!-- src: results/x0_probe/muse30b_x0_probe_v4/probe-20261026T000115Z/probe.md \| after :: locker sentence :: 669 :: 0.34 [0.31, 0.37] --> | 0.36 [0.33, 0.39]<!-- src: results/x0_probe/nem35l_x52_probe/probe-20261029T002432Z/probe.md \| after :: locker sentence :: 658 :: 0.36 [0.33, 0.39] --> | 0.33 [0.31, 0.35]<!-- src: results/x0_probe/qwen35_122b_x0_probe_v4/probe-20261024T230718Z/probe.md \| after :: locker sentence :: 0.33 [0.31, 0.35] --> |
  | the answer digit, locker before (chance 0.11) | 0.27 [0.24, 0.31]<!-- src: results/x0_probe/qwen35_9b_x0_probe_v4/probe-20261024T172340Z/probe.md \| before :: answer digit :: 758 :: 0.27 [0.24, 0.31] --> | 0.40 [0.36, 0.44]<!-- src: results/x0_probe/x0_probe_v4_27b/probe-20261024T172424Z/probe.md \| before :: answer digit :: 758 :: 0.40 [0.36, 0.44] --> | 0.33 [0.28, 0.37]<!-- src: results/x0_probe/muse30b_x0_probe_v4/probe-20261026T000115Z/probe.md \| before :: answer digit :: 657 :: 0.33 [0.28, 0.37] --> | 0.25 [0.21, 0.28]<!-- src: results/x0_probe/nem35l_x52_probe/probe-20261029T002432Z/probe.md \| before :: answer digit :: 636 :: 0.25 [0.21, 0.28] --> | 0.25 [0.21, 0.28]<!-- src: results/x0_probe/qwen35_122b_x0_probe_v4/probe-20261024T230718Z/probe.md \| before :: answer digit :: 0.25 [0.21, 0.28] --> |

- **Read.**
  - The 122B reads the locker sentence at its bridge word too (locker first), near chance with the locker after.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - With the locker before the pick, the bridge word holds which locker sentence the item's locker sits in, far above the layout baseline, on all four models; with the locker after, it does not (the control). The answer digit itself is read only weakly.

- **Caveats.**
  - Descriptive, chosen after the data.
  - Lightning's probe reads the place less well than the other three.

</details>

### Does swapping the address send the lookup to the swapped-in locker? <a id="swap"></a>

`in README` `below gate: 122B` *Used in: README Part III card "Can the address be read, removed, added and swapped?" (the swap).*

Test address swap by dose · opened 29 Oct · status: rule fixed in advance · hand-check: in sample (view d) · files: `results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md` · recompute: `scripts/x8_write.py` (the command in its docstring) · also: Lightning's coverage run

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Adding the difference between two slots' address codes at the bridge word, does the lookup go to the locker of the slot swapped in, and how much does the recall change with it?
- **Why we asked.** Removing the address stops position answers; a swap tests whether the address is read as a reference to a place.
- **Data.** Routes scenes without a move, 300 per model, each swapped to two target lockers (600 swaps); Lightning at L14 (gate chosen after the 60-scene pre-check, ○).
- **Method.** At the bridge word at L: the difference of two slot means, at one, two and four times its size; control: a random vector of the same size. Read: the lookup's answer (target locker, original, the third), and whether the recall's answer changes (the collateral).

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/06_address_read_remove.png)

*Left: a probe at the bridge word reads which locker sentence holds the item's locker (the address, amber), against a probe trained on the layout only (grey). Right: the lookups that still answer by position when the address is removed from the patch (amber), against a random part of the same size removed instead (grey); lower means more blocked. Whiskers: 95% intervals. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/07_address_swap_lens.png)

*Left: the lookups sent to the new locker when another locker's address is swapped in at about a real change's size (amber), against a random vector of the same size (grey). Right: how far above 200 random vectors the lens's 25 directions rebuild that swap (amber), against a change of item of the same size (blue, the positive control), in z; grey band: the range of the 200 random vectors. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

This card is the figure's third column.

- **Rule, fixed in advance.** "at s = 1 the target share minus the random direction's >= 0.15 with lower CI > 0; [...] among writes that move the lookup to another locker target / (target + third) >= 0.80, a model counting only with >= 30 such writes, fewer than two counting = can't tell; [...] target minus random >= 0.10 in each of the 6 (j, k) pairs" (jobs/c3/x8_a_9b.yaml; each over the 9B, the 27B, the 122B and Muse). Lightning: a coverage run on that rule, no prediction.

</details>

- **Result.** (all 600 swaps pooled; README E6 quotes the mean over the six slot pairs at s = 2 instead; a random vector sends 0.00 to 0.01 at every dose on every model)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookups sent to the swapped-in locker, dose 1 | 0.02 [0.01, 0.03]<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.98 [0.97, 0.99] :: 0.02 [0.01, 0.03] --> | 0.01 [0.00, 0.01]<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.99 [0.98, 1.00] :: 0.01 [0.00, 0.01] --> | 0.05 [0.03, 0.07]<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.94 [0.91, 0.96] :: 0.05 [0.03, 0.07] --> | 0.03 [0.01, 0.04]<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.96 [0.94, 0.98] :: 0.03 [0.01, 0.04] --> | ○ 0.01 [0.00, 0.01]<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 1 :: all :: 600 :: 0.01 [0.00, 0.01] --> |
  | lookups sent to the swapped-in locker, dose 2 | 0.46 [0.42, 0.50]<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.06 [0.04, 0.08] :: 0.46 [0.42, 0.50] --> | 0.24 [0.20, 0.29]<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.71 [0.66, 0.76] :: 0.24 [0.20, 0.29] --> | 0.52 [0.48, 0.55]<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.38 [0.33, 0.42] :: 0.52 [0.48, 0.55] --> | 0.50 [0.46, 0.54]<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.43 [0.38, 0.47] :: 0.50 [0.46, 0.54] --> | ○ 0.50 [0.46, 0.54]<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 2 :: all :: 600 :: 0.50 [0.46, 0.54] --> |
  | lookups sent to the swapped-in locker, dose 4 | 0.73 [0.70, 0.77]<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.17 [0.13, 0.21] :: 0.73 [0.70, 0.77] --> | 0.50 [0.47, 0.53]<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.37 [0.34, 0.40] :: 0.50 [0.47, 0.53] --> | 0.52 [0.50, 0.54]<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.23 [0.20, 0.26] :: 0.52 [0.50, 0.54] --> | 0.69 [0.66, 0.71]<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.25 [0.22, 0.28] :: 0.69 [0.66, 0.71] --> | ○ 0.66 [0.63, 0.69]<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 4 :: all :: 600 :: 0.66 [0.63, 0.69] --> |
  | recalls changed by the swap, dose 1 / 2 / 4 | 0.04<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.02 [0.01, 0.03] :: 0.04 --> / 0.21<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.46 [0.42, 0.50] :: 0.21 --> / 0.43<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| 0.73 [0.70, 0.77] :: 0.43 --> | 0.01<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.01 [0.00, 0.01] :: 0.01 --> / 0.04<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.24 [0.20, 0.29] :: 0.04 --> / 0.11<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| 0.50 [0.47, 0.53] :: 0.11 --> | 0.01<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.05 [0.03, 0.07] :: 0.01 --> / 0.06<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.52 [0.48, 0.55] :: 0.06 --> / 0.11<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| 0.52 [0.50, 0.54] :: 0.11 --> | 0.02<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.03 [0.01, 0.04] :: 0.02 --> / 0.27<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.50 [0.46, 0.54] :: 0.27 --> / 0.40<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md \| 0.69 [0.66, 0.71] :: 0.40 --> | ○ 0.03<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 1 :: all :: 600 :: 0.03 --> / 0.23<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 2 :: all :: 600 :: 0.23 --> / 0.45<!-- src: results/x8_write/qwen35_122b_x8_write_g75/verdict-20261026T125705Z/verdict.md \| write :: 4 :: all :: 600 :: 0.45 --> |

- **Read.**
  - At s = 1, the dose fixed in advance, the rule says no on the 9B, 27B and Muse (target minus random 0.02 [0.01, 0.03]<!-- src: results/x8_write/qwen35_9b_x8_write/verdict-20261026T110254Z/verdict.md \| Q44.1: target minus random at s = 1 :: 0.02 [0.01, 0.03] --> / 0.00 [0.00, 0.01]<!-- src: results/x8_write/x8_write_27b/verdict-20261026T125548Z/verdict.md \| Q44.1: target minus random at s = 1 :: 0.00 [0.00, 0.01] --> / 0.05 [0.03, 0.07]<!-- src: results/x8_write/muse30b_x8_write/verdict-20261026T141141Z/verdict.md \| Q44.1: target minus random at s = 1 :: 0.05 [0.03, 0.07] -->; bar 0.15): s = 1 is below a real change's size, a design error (docs/shared/joint_story_draft.md). Lightning's coverage run says no there too (target minus random 0.03 [0.01, 0.04]<!-- src: results/x8_write/nem35l_x52_write/verdict-20261029T005021Z/verdict.md | Q44.1 :: 0.03 [0.01, 0.04] -->).

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  What the recall changes to (a CPU check after the data, descriptive; results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md): of the recalls the swap changes at dose 2, 0.84<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | write | 2 | 600 | 0.21 | 129 | 0.84 :: 0.84 --> (9B) / 0.85<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | write | 2 | 600 | 0.27 | 164 | 0.85 :: 0.85 --> (Lightning) name the swapped-in item's legs, 0.09<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 129 | 0.84 | 0.09 :: 0.09 --> / 0.07<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 164 | 0.85 | 0.07 :: 0.07 --> the third item's, 0.06<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 129 | 0.84 | 0.09 | 0.06 :: 0.06 --> / 0.08<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 164 | 0.85 | 0.07 | 0.08 :: 0.08 --> another digit, 0.00<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 129 | 0.84 | 0.09 | 0.06 | 0.00 :: 0.00 --> / 0.00<!-- src: results/x8_write/x52_swaprecall-20261029T080538Z/swaprecall.md | 164 | 0.85 | 0.07 | 0.08 | 0.00 :: 0.00 --> a non-answer.

More from the reading:

  - At s = 2 (about a real change's size) and s = 4 the swap sends a quarter to three quarters of lookups to the swapped-in locker on every model, Lightning included, against none for a random vector.

- **Caveats.**
  - The 122B (FP8; MoE, ~10B active): not tested (gate 0.797<!-- src: results/x6_routes/qwen35_122b_x6_routes_c0/gate.json \| "PM" :: 0.797 --> < 0.80) on the routes scenes; its g75 runs lowered the gate to 0.75 after the data (the README's °): below gate, exploratory, hollow ○, never in claims or grades. Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones.
  - The swap also changes the recall's answer, most on the 9B and Lightning (the collateral).
  - Pooled over pairs: some pairs move no lookup at all (Lightning: two of six at dose 2).
  - The recall's collateral is mostly the recall following the swapped-in item (the CPU check above; 9B and Lightning only).

</details>

### Does the address survive neutral sentences between the lockers and the picks? <a id="t47-16"></a>

`in README` *Used in: README Part III card "Can the address be read, removed, added and swapped?" (the swap with no / 50 neutral sentences: the 9B, 27B, Muse (its rerun r2) and Lightning).*

Test 47.16 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_distance/x47_16-20261028T131501Z/x47_16.md` · recompute: `scripts/x47_distance.py` (the command in its docstring) · also: the swap after neutral sentences; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** With 5, 20 or 50 neutral sentences between the lockers and the picks, does the address still carry position answers, and does the address swap still work?
- **Why we asked.** An address read at the bridge word could be a short-range effect of the sentences next to it.
- **Data.** Routes scenes (another item moved), the same base scenes at every distance: 218<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: 218 --> / 300<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: 300 --> / 199<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: 199 --> (9B / 27B / Lightning); Muse: its rerun r2 (Dan, 09:05), 279<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse-glimmer-30b :: 0.98 :: 279 --> scenes.
- **Method.** At each distance, at the bridge word at L: the routes test's whole change, and without the address against a random part of its share; the address swap at dose 2 against a random vector of its size; a slot probe beside.

![The address survives fifty neutral sentences](../../figures/depth/readme/s10_pointer_moves_and_neutral_sentence.png)

*Top: the position answers when only the address is kept, for moves to or from the first locker and between the second and the third (amber), per model, with the whole change's share beside. Bottom: the code's shift, in positions, with a neutral sentence before the first locker or between the lockers and the picks (amber). Whiskers: 95% intervals. All estimates post hoc.*

- **Rule, fixed in advance.** "breaks = the gate failed at some k (the test stops there); distance-robust = position share and probe within 0.1 of k = 0 at every k, swap success within 0.15; address near, identity far = position falls >= 0.2 and identity rises >= 0.2 by k = 50 with accuracy >= 0.8". The 27B and Lightning: coverage runs on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | position under the whole change, 0 / 50 sentences | 0.55 [0.48, 0.62]<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: 218 :: 0.55 [0.48, 0.62] --> / 0.57 [0.51, 0.63]<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: 218 :: 0.57 [0.51, 0.63] --> | 0.33 [0.28, 0.39]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: 300 :: 0.33 [0.28, 0.39] --> / 0.24 [0.19, 0.28]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: 300 :: 0.24 [0.19, 0.28] --> | 0.54 [0.48, 0.59]<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse-glimmer-30b :: 0.44 [0.39, 0.50] :: 0.54 [0.48, 0.59] --> / 0.51 [0.45, 0.57]<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse-glimmer-30b :: 0.47 [0.41, 0.53] :: 0.51 [0.45, 0.57] --> | 0.48 [0.40, 0.56]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: 199 :: 0.48 [0.40, 0.56] --> / 0.44 [0.36, 0.52]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: 199 :: 0.44 [0.36, 0.52] --> | 0.39 [0.33, 0.44]<!-- src: results/x47_distance/x52_distance-20261030T094552Z/x47_16.md \| qwen3.5-122b-a10b :: 0.61 [0.55, 0.67] :: 0.39 [0.33, 0.44] --> / 0.33 [0.27, 0.39]<!-- src: results/x47_distance/x52_distance-20261030T094552Z/x47_16.md \| qwen3.5-122b-a10b :: 0.66 [0.60, 0.72] :: 0.33 [0.27, 0.39] --> ○ |
  | the swap: lookups sent to the target, 0 / 50 sentences | 0.42 [0.38, 0.47]<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: 218 :: 0.42 [0.38, 0.47] --> / 0.35 [0.31, 0.40]<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: 218 :: 0.35 [0.31, 0.40] --> | 0.24 [0.20, 0.28]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: 300 :: 0.24 [0.20, 0.28] --> / 0.20 [0.17, 0.25]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: 300 :: 0.20 [0.17, 0.25] --> | 0.50 [0.46, 0.54]<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse-glimmer-30b :: 0.44 [0.39, 0.50] :: 0.50 [0.46, 0.54] --> / 0.52 [0.49, 0.55]<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse-glimmer-30b :: 0.47 [0.41, 0.53] :: 0.52 [0.49, 0.55] --> | 0.53 [0.47, 0.59]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: 199 :: 0.53 [0.47, 0.59] --> / 0.48 [0.43, 0.53]<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: 199 :: 0.48 [0.43, 0.53] --> | 0.48 [0.44, 0.52]<!-- src: results/x47_distance/x52_distance-20261030T094552Z/x47_16.md \| qwen3.5-122b-a10b :: 0.38 [0.33, 0.43] :: 0.48 [0.44, 0.52] --> / 0.27 [0.23, 0.31]<!-- src: results/x47_distance/x52_distance-20261030T094552Z/x47_16.md \| qwen3.5-122b-a10b :: 0.31 [0.26, 0.37] :: 0.27 [0.23, 0.31] --> ○ |
  | the rule | **distance-robust address<!-- src: results/x47_distance/x47_16-20261028T131501Z/x47_16.md \| qwen3.5-9b :: distance-robust address -->** | **distance-robust address<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| qwen3.6-27b :: distance-robust address -->** (no prediction) | **distance-robust address<!-- src: results/x47_distance/x52_distance-20261029T090323Z/x47_16.md \| muse30_x47_16_r2 :: distance-robust address -->** (no prediction) | **distance-robust address<!-- src: results/x47_distance/x52_distance-20261029T023426Z/x47_16.md \| nemotron-3.5-lightning :: distance-robust address -->** (no prediction) | **none of the three<!-- src: results/x47_distance/x52_distance-20261030T094552Z/x47_16.md \| qwen35_122b_distance :: none of the three -->** (no prediction; lookup-only gate) |

- **Read.**
  - On the 9B, 27B and Lightning the address keeps carrying position answers and the swap keeps working with up to 50 neutral sentences before the picks.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 122B (coverage, 30 Oct; the lookup-only gate, ○ †) reads "none of the three": its swap sends fewer lookups to the target with 50 neutral sentences than with none.
  - Muse's first run had no outcomes (Flagged 22); its rerun r2 (29 Oct, a coverage run on the same rule, no prediction) gives the column here.
  - The 27B's position share falls by 0.09 at 50 sentences, just inside the rule's 0.1.

</details>

### With six lockers, does each locker have its own code? <a id="six"></a>

`in README` *Used in: README Part III card "With six lockers, does each locker have its own code?".*

Test six lockers · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_six/x47_2-20261028T113102Z/x47_2.md` · recompute: `scripts/x47_six.py` (the command in its docstring) · also: the 27B's coverage run , Lightning's 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** With six locker sentences, is the address a line over slots (one shift steps the lookup one slot), a first-versus-rest marker, or one code per slot?
- **Why we asked.** With three lockers a line and a first-versus-rest marker look the same.
- **Data.** Six-locker scenes: the test half, 300 per model (9B, 27B, Muse, Lightning at L14, the 122B at L33 as a coverage run, 30 Oct), the other 300 fit the slot means.
- **Method.** At the bridge word at L: one fixed shift (the mean step between neighbouring slot means) from each start slot, and swaps between given slots, each at doses 1 and 2, against a random vector of the same size; the slot means' first principal component beside.

*No figure: two counts per model (one shift: 0 of 5 start slots everywhere; given-slot swaps of 30) and a label: the Result's table.*

- **Rule, fixed in advance.** "Ordinal: the first PCA component is monotone in slot (|Spearman| >= 0.9) and v sends >= 0.25 of lookups to slot k+1 from >= 4 of 5 start slots, the random vector <= 0.05; Categorical, first vs rest: v works only from slot 1 (others < 0.10) and U's removal on 2-6 moves is within 0.10 of random; Slot-specific: pairwise writes reach >= 0.25 on most pairs but no single v does." Dose 2 decides. The 27B and Lightning: coverage runs on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | position share under the whole change | 0.32 [0.28, 0.37]<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| qwen35_9b_x47_2 :: 0.32 [0.28, 0.37] --> | 0.25 [0.19, 0.31]<!-- src: results/x47_six/x52_six-20261029T004919Z/x47_2.md \| 0.70 [0.64, 0.76] :: 0.25 [0.19, 0.31] --> | 0.37 [0.31, 0.43]<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| muse30_x47_2 :: 0.37 [0.31, 0.43] --> | 0.40 [0.33, 0.46]<!-- src: results/x47_six/x52_six-20261029T011006Z/x47_2.md \| nem35l_x52_six :: whole :: 0.40 [0.33, 0.46] --> | 0.32 [0.26, 0.38]<!-- src: results/x47_six/x52_six-20261029T231821Z/x47_2.md \| qwen35_122b_x47_2 :: whole :: 0.32 [0.26, 0.38] --> |
  | first component monotone in slot (Spearman) | 1.00<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| 8.15, 5.59, 3.08 :: 1.00 --> | 1.00<!-- src: results/x47_six/x52_six-20261029T004919Z/x47_2.md \| 26.79, 16.42, 11.83 :: 1.00 --> | 1.00<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| 84.27, 58.15, 38.31 :: 1.00 --> | 1.00<!-- src: results/x47_six/x52_six-20261029T011006Z/x47_2.md \| 6.40, 4.93, 2.50 :: 1.00 --> | 1.00<!-- src: results/x47_six/x52_six-20261029T231821Z/x47_2.md \| 1.75, 1.28, 0.74 :: 1.00 --> |
  | given-slot swaps reaching 0.25 at dose 2 | 18 of 30<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| -0.025 :: 18 of 30 --> | 13 of 30<!-- src: results/x47_six/x52_six-20261029T004919Z/x47_2.md \| 0.004 :: 13 of 30 --> | 21 of 30<!-- src: results/x47_six/x47_2-20261028T113102Z/x47_2.md \| -0.055 :: 21 of 30 --> | 21 of 30<!-- src: results/x47_six/x52_six-20261029T011006Z/x47_2.md \| -0.020 :: 21 of 30 --> | 21 of 30<!-- src: results/x47_six/x52_six-20261029T231821Z/x47_2.md \| qwen3.5-122b-a10b :: 0 of 5 :: 21 of 30 --> |
  | the rule at dose 2 | **slot-specific** | **none of the three** | **slot-specific** | **slot-specific** (no prediction) | **slot-specific<!-- src: results/x47_six/x52_six-20261029T231821Z/x47_2.md \| qwen35_122b_x47_2 :: tested :: slot-specific -->** (no prediction) |

- **Read.**
  - No single shift moves the lookup on any model; given-slot swaps work on most pairs on the 9B, Muse, Lightning and the 122B †, so each slot is its own target there; on the 27B neither the line nor the per-slot pattern holds.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 27B's shift writes move 0.00 at every start slot, though its slot means lie in order.
  - A different test of the code's size (see [51.11](#t51-11)) does not find one dimension per slot on the 9B.

</details>

### What is the address, independent of how we built it? <a id="t51-11"></a>

`in README` *Used in: README Part III card "With six lockers, does each locker have its own code?" (the held-out code); README "Tested and dropped" ("One code per locker").*

Test 51.11 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_addr/verdict-20261028T215138Z/verdict.md` · recompute: `scripts/x51_addr.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Is the address one code per locker, one shared code, or an order line, by methods that do not use our construction?
- **Why we asked.** Our address was built from means of four slots; its size and shape could be an artefact of that build.
- **Data.** Routes-style scenes with 3, 4, 6 and 8 lockers; held-out entities only (9B and Muse, all three parts; 27B part 2 only).
- **Method.** Part 1: the smallest learned subspace dimension d* that carries the position switch, per number of lockers, against random subspaces. Part 2: the address swap through our code, a probe's code and a learned code, each with the others removed, against a random direction. Part 3: swaps to the midpoint between two slots, against a random vector of the same norm.

*No figure: the code's shape per number of lockers is supplementary (figure); the table has the rule's numbers.*

- **Rule, fixed in advance.** Part 1: "One dimension per slot: d*(S) ≥ S − 2 for every S and d*(8) ≥ 5"; "An ordinal (low-dimensional) code: d*(S) ≤ 2 for every S up to 8"; else in between. Part 2: "One code, three bases: every projected swap reaches ≥ 0.6 of the whole swap's effect, and each cross-removal cuts the other's swap by ≥ 0.6." Part 3: "Categories: midpoint swaps send < 0.1 to the midpoint slot while the full swaps reach ≥ 0.4 of the target"; "A metric order: midpoint swaps send ≥ 0.3 of lookups to the midpoint slot, from both ends." (jobs/c3/batch51.yaml, addendum 3)

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | part 1, d* at 3 / 4 / 6 / 8 lockers | 2<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'train': 213, 'select': 95, 'test': 50} :: 2 --> / 2<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'select': 59, 'train': 191, 'test': 56} :: 2 --> / > 7<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'select': 61, 'train': 200, 'test': 42} :: > 7 --> / 2<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'train': 174, 'select': 73, 'test': 57} :: 2 -->: **in between** | not designed | 2<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'train': 200, 'test': 91, 'select': 82} :: 2 --> / 2<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'select': 72, 'train': 191, 'test': 84} :: 2 --> / 7<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'select': 60, 'train': 192, 'test': 76} :: 7 --> / > 7<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| {'train': 169, 'select': 64, 'test': 82} :: > 7 -->: **one dimension per slot** | not run | not run |
  | part 2: swap through the learned code with ours removed | 0.39 [0.37, 0.40]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 0.03 [0.01, 0.05] :: 0.39 [0.37, 0.40] --> | **in between** | **in between** | | |
  | part 2: the whole swap with ours removed | 0.03 [0.01, 0.05]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 0.39 [0.37, 0.40] :: 0.03 [0.01, 0.05] --> | | | | |
  | part 3: midpoint swap from slot 1 lands on the midpoint | 0.06 [0.03, 0.09]<!-- src: results/x51_addr/verdict-20261028T215138Z/verdict.md \| 9.0243 :: 0.06 [0.03, 0.09] --> (none of the three) | not designed | none of the three | | |

- **Read.**
  - No row of the wording table matches the labels; the methods agree only in part, and midpoint swaps do not land between slots.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 9B's d* at 6 lockers was not found below 8; Muse's "one per slot" rests on the literal rule (d*(8) not found counts as > 7).
  - The 27B ran part 2 only.

</details>

### On the scenes where the 27B's lookup goes by position, does the address work as on the 9B? <a id="b53-5"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 53.5 · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md` · recompute: `scripts/x53_subset27b.py` (the command in its docstring) · also: CPU, existing outcomes

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the scenes where the 27B's lookup goes by position, does the address work as it does on the 9B?
- **Why we asked.** Added by itself, the 27B's address brings few position answers back overall ([routes](#routes)); the 27B takes the position route less often, so its address could be the same mechanism, used less.
- **Data.** Routes scenes of the two conditions that have a position answer, selected where the lookup answers by position under the whole change: 232 on the 27B (31 bridge items), 340 on the 9B beside; the swap on those scenes of the second condition (101 / 153).
- **Method.** On existing outcomes (CPU): position answers without the address against without a random part of its share; the address alone against a random part alone; the address swap at dose 2.

- **Rule, fixed in advance.** "Rule: "same mechanism, used less" if the address alone brings >= 0.25 of position answers back and its removal leaves <= 0.10 (the 9B's pattern); "the 27B differs" otherwise. Same subset on the 9B beside." (jobs/c3/batch53.yaml, Dan 29 Oct 09:30; no prediction)

The address removed and added alone on the 27B's position scenes, beside the 9B:

![On its position scenes the 27B's address brings fewer answers back](../../figures/depth/ledger/09_subset27b.png)

*The 27B's scenes where its lookup goes by position, beside the 9B: the position answers left without the address and without a random part (grey), and brought back by the address alone and by a random part alone (grey). Whiskers 95% intervals.*

</details>

- **Result.**

  | | 9B (beside) | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | position answers back with the address alone (bar >= 0.25) | 0.46 [0.39, 0.53]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.5-9B :: C1 + C2 :: 0.46 [0.39, 0.53] --> | 0.22 [0.15, 0.29]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.6-27B :: C1 + C2 :: 0.22 [0.15, 0.29] --> | not designed | not designed | not run |
  | position answers left without the address (bar <= 0.10) | 0.06 [0.04, 0.09]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.5-9B :: C1 + C2 :: 0.06 [0.04, 0.09] --> | 0.08 [0.04, 0.11]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.6-27B :: C1 + C2 :: 0.08 [0.04, 0.11] --> | | | |
  | the same without a random part of its share | 0.45 [0.41, 0.50]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.5-9B :: C1 + C2 :: 0.45 [0.41, 0.50] --> | 0.37 [0.30, 0.42]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.6-27B :: C1 + C2 :: 0.37 [0.30, 0.42] --> | | | |
  | the swap at dose 2: lookups sent to the target | 0.40 [0.36, 0.43]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.5-9B :: position-route subset :: 0.40 [0.36, 0.43] --> | 0.23 [0.18, 0.29]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| Qwen3.6-27B :: position-route subset :: 0.23 [0.18, 0.29] --> | | | |
  | the rule | the pattern holds | **the 27B differs<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md \| 27B: the 27B differs :: the 27B differs -->** | | | |

- **Read.**
  - On its own position-route scenes the 27B's address, added by itself, brings back fewer position answers than the rule's bar, and its removal leaves few: by the rule the 27B differs; the 9B's subset shows its pattern.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 27B's interval for the address alone ([0.15, 0.29]) contains the 0.25 bar.
  - The 9B's pattern holds only with the two conditions pooled: per condition, the first holds and the second does not, on both models.
  - In the first condition, removing a random part of the address's share also leaves few position answers (0.07 [0.03, 0.11]<!-- src: results/x53_subset27b/x53_subset27b-20261029T085435Z/verdict.md | Without a random part of the address's share, C1 keeps :: 0.07 [0.03, 0.11] --> on the 27B), so there the removal clause cannot tell the address from a random part.
  - CPU on existing outcomes; exploratory (batch 53); no prediction.

</details>

### Can the lens read the address? <a id="t47-0"></a>

`in README` *Used in: README Part III card "Can the lens read the address?" (the lens readout of the swap).*

Test 47.0 · opened not stated · status: descriptive · hand-check: not in sample · files: `results/x47_verbal/summary-20261028T033646Z/verbal.md` · recompute: `scripts/x47_verbal.py` (the command in its docstring) · also: lens readout of an address swap; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Read through the lens, does an address swap at a real change's size show up as a position word, get rebuilt by the lens's own directions, or move the lens's readout more than a random vector of the same size?
- **Why we asked.** Neel's question: is the address verbalizable? A lens monitor would have to see it.
- **Data.** Routes scenes, 100 items per model, each swapped to both other lockers (200 cases); null: 200 random vectors of the same size.
- **Method.** At the bridge word at L, the swap h + 2 (mu_k - mu_j): (a) the best rank of a position word (first, second, third, 1, 2, 3, ...) in the lens readout; (b) the share the lens's 25 best directions rebuild; (c) how far the readout moves (KL). Positive control: an item change of the same size.

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/06_address_read_remove.png)

*Left: a probe at the bridge word reads which locker sentence holds the item's locker (the address, amber), against a probe trained on the layout only (grey). Right: the lookups that still answer by position when the address is removed from the patch (amber), against a random part of the same size removed instead (grey); lower means more blocked. Whiskers: 95% intervals. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

![The address: a probe reads it, a swap moves the lookup, the lens cannot see it](../../figures/common/readme/07_address_swap_lens.png)

*Left: the lookups sent to the new locker when another locker's address is swapped in at about a real change's size (amber), against a random vector of the same size (grey). Right: how far above 200 random vectors the lens's 25 directions rebuild that swap (amber), against a change of item of the same size (blue, the positive control), in z; grey band: the range of the 200 random vectors. Hollow (○): Lightning, and the 122B where its gate was lowered (post hoc).*

This card is the figure's fourth column.

- **Rule, fixed in advance.** Descriptive, with the reading fixed in advance: ""Not verbalizable": reconstruction at k = 25 within 2x the random null's share, no ordinal token in the top-20 beyond the null's 5th-percentile rank, and the KL under the write within the null's 95th percentile, on all three models." Lightning: a coverage run on that reading, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | best position-word rank after the swap, median (random's 5th percentile) | 27 (null 5th pct 20)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) best ordinal-token rank, h + write (median) :: 27 (null 5th pct 20) --> | 30 (null 5th pct 22)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) best ordinal-token rank, h + write (median) :: 30 (null 5th pct 22) --> | 94 (null 5th pct 58)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) best ordinal-token rank, h + write (median) :: 94 (null 5th pct 58) --> | 220 (null 5th pct 49)<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| (a) best ordinal-token rank, h + write (median) :: 220 (null 5th pct 49) --> | 993 (null 5th pct 523)<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| (a) best ordinal-token rank, h + write (median) :: 993 (null 5th pct 523) --> ○ |
  | cases whose rank beats their own null | 0.03 [0.01, 0.06]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) cases with the ordinal rank beyond their own null :: 0.03 [0.01, 0.06] --> | 0.13 [0.08, 0.19]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) cases with the ordinal rank beyond their own null :: 0.13 [0.08, 0.19] --> | 0.18 [0.14, 0.24]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) cases with the ordinal rank beyond their own null :: 0.18 [0.14, 0.24] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| (a) cases with the ordinal rank beyond their own null :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| (a) cases with the ordinal rank beyond their own null :: 0.00 [0.00, 0.00] --> ○ |
  | share rebuilt by 25 lens directions, swap over random | 1.16x<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (b) pointer / random, k = 25 (every token; letters) :: 1.16x --> | 0.94x<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (b) pointer / random, k = 25 (every token; letters) :: 0.94x --> | 1.22x<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (b) pointer / random, k = 25 (every token; letters) :: 1.22x --> | 1.44x<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| (b) pointer / random, k = 25 (every token; letters) :: 1.44x --> | 1.14x<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| (b) pointer / random, k = 25 (every token; letters) :: 1.14x --> ○ |
  | cases whose readout moves beyond their own null (KL) | 0.15 [0.09, 0.23]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (c) cases with KL beyond their own null :: 0.15 [0.09, 0.23] --> | 0.01 [0.00, 0.05]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (c) cases with KL beyond their own null :: 0.01 [0.00, 0.05] --> | 0.28 [0.19, 0.39]<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (c) cases with KL beyond their own null :: 0.28 [0.19, 0.39] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| (c) cases with KL beyond their own null :: 0.00 [0.00, 0.00] --> | 0.02 [0.00, 0.06]<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| (c) cases with KL beyond their own null :: 0.02 [0.00, 0.06] --> ○ |
  | control: the new item's name rank after an item change | 50 (null 5th pct 2220)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) positive control: new item's name rank, h + identity :: 50 (null 5th pct 2220) --> | 14 (null 5th pct 5014)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) positive control: new item's name rank, h + identity :: 14 (null 5th pct 5014) --> | 25 (null 5th pct 3636)<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| (a) positive control: new item's name rank, h + identity :: 25 (null 5th pct 3636) --> | 19 (null 5th pct 4844)<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| (a) positive control: new item's name rank, h + identity :: 19 (null 5th pct 4844) --> | 2 (null 5th pct 1137)<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| (a) positive control: new item's name rank, h + identity :: 2 (null 5th pct 1137) --> ○ |
  | reading | not verbalizable<!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md \| reading :: not verbalizable --> | not verbalizable | not verbalizable | not verbalizable<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| reading :: not verbalizable --> | not verbalizable<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| reading :: not verbalizable --> ○ (lookup-only gate) |

- **Read.**
  - On all four models the address swap reads through the lens like a random vector of its size, while an item change of the same size stands far outside the random range.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Lightning's swap moves its lookup to the written locker in 0.50<!-- src: results/x47_verbal/summary-20261029T005548Z/verbal.md \| x8's lookup on these writes at s = 2: to the written locker :: 0.50 --> of these cases, yet none of the lens's three readings leaves the null.

- **Caveats.**
  - Descriptive: the reading is the spec's, not a pre-registered claim.
  - The reading uses medians; per case, some readouts do move beyond their own null on the 9B and Muse.

</details>

### What can a probe on the lens subspace decode, against the full state? <a id="b53-2"></a>

`in README` *Used in: README Part III card "Can a monitor on the lens part read the address where the lookup uses it?".*

Test 53.2 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md` · recompute: `scripts/x53_monitor.py` (the command in its docstring) · also: the monitor test; four models, 29 Oct; the 122B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** What can a probe on the lens subspace decode, against the full state: the bridge item's locker slot (the address) and the lookup's answer digit, with which item and the recall's answer as positive controls?

![The address is decodable but under-represented in the lens directions](../../figures/common/readme/11_monitor.png)

*The locker probe's accuracy for the address at the last token, per model, for the lens part as used throughout (left) and with four times as many directions (right): the lens part (teal) against a random part of the same energy (grey), with 95% intervals; the lens part's value and interval, and the full state's accuracy, in their own columns. Lightning hollow (○, post hoc).*


- **Why we asked.** The lens readout does not show the address ([47.0](#t47-0)); a trained probe on the lens part's coordinates asks whether the address is there but not verbalized, or absent from the lens directions.

- **Data.** The main test (400 rows, 43 to 45 bridge entities per model) and the JSON scenes (620 to 830 rows), the bridge word and the last token, every second layer; the 9B, the 27B, Muse and Lightning; the 122B not completed in the sprint.

- **Method.** Logistic probes (5 seeds of 5-fold CV, held-out entities) on the full state, on the lens part's coordinates (k = 25 and 100), on a random subspace of the same k, on a fixed lens subspace, and on an energy-matched random subspace (Dan 11:25, 13:15, before the verdict); the lens readout (top words) cited from 47.0, unchanged.

- **Rule, fixed in advance.** "Rule (verbatim): "J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every layer while the full residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above random; else in between." (jobs/c3/batch53.yaml, 53.2; no prediction) Before scoring (Dan 11:25, 11:40, 13:15, verbatim in the verdict): the headline targets are the slot and the lookup's digit; "random reads it too" is worded "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it"; and "if J++ is >= 0.10 below the energy-matched random while the full state is >= 0.8, the label is "the address is under-represented in the lens directions" (stronger than blind)".

</details>

- **Result.** (main test, the last token, at the layer where the full state peaks)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (a) the lens readout (47.0) | not verbalizable | not verbalizable | not verbalizable | not verbalizable | not verbalizable<!-- src: results/x47_verbal/summary-20261029T180530Z/verbal.md \| reading :: not verbalizable --> ○ (lookup-only gate) |
  | the locker slot, k = 25: lens part / random / energy-matched random | 0.60 [0.56, 0.64]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 25 :: L20 :: 0.60 [0.56, 0.64] --> / 0.65 [0.62, 0.68]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 25 :: L20 :: 0.65 [0.62, 0.68] --> / 0.83 [0.80, 0.86]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 25 :: L20 :: 0.83 [0.80, 0.86] --> | 0.77 [0.73, 0.80]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 25 :: L48 :: 0.77 [0.73, 0.80] --> / 0.81 [0.79, 0.84]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 25 :: L48 :: 0.81 [0.79, 0.84] --> / 0.95 [0.94, 0.96]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 25 :: L48 :: 0.95 [0.94, 0.96] --> | 0.68 [0.65, 0.71]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.68 [0.65, 0.71] --> / 0.69 [0.66, 0.72]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.69 [0.66, 0.72] --> / 0.89 [0.86, 0.91]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.89 [0.86, 0.91] --> | 0.65 [0.61, 0.69]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.65 [0.61, 0.69] --> / 0.64 [0.61, 0.66]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.64 [0.61, 0.66] --> / 0.88 [0.86, 0.90]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.88 [0.86, 0.90] --> | 0.73 [0.69, 0.77]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 25 :: L40 :: 0.73 [0.69, 0.77] --> / 0.71 [0.69, 0.73]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 25 :: L40 :: 0.71 [0.69, 0.73] --> / 0.91 [0.89, 0.93]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 25 :: L40 :: 0.91 [0.89, 0.93] --> |
  | the locker slot, k = 100: the same | 0.72 [0.69, 0.76]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 100 :: L20 :: 0.72 [0.69, 0.76] --> / 0.77 [0.74, 0.81]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 100 :: L20 :: 0.77 [0.74, 0.81] --> / 0.86 [0.83, 0.89]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 100 :: L20 :: 0.86 [0.83, 0.89] --> | 0.85 [0.82, 0.88]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 100 :: L48 :: 0.85 [0.82, 0.88] --> / 0.92 [0.90, 0.94]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 100 :: L48 :: 0.92 [0.90, 0.94] --> / 0.98 [0.96, 0.99]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 100 :: L48 :: 0.98 [0.96, 0.99] --> | 0.80 [0.76, 0.83]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.80 [0.76, 0.83] --> / 0.83 [0.80, 0.86]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.83 [0.80, 0.86] --> / 0.92 [0.90, 0.94]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.92 [0.90, 0.94] --> | 0.79 [0.75, 0.83]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.79 [0.75, 0.83] --> / 0.80 [0.78, 0.84]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.80 [0.78, 0.84] --> / 0.94 [0.92, 0.95]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 100 :: L34 :: 0.94 [0.92, 0.95] --> | 0.85 [0.83, 0.88]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 100 :: L40 :: 0.85 [0.83, 0.88] --> / 0.85 [0.83, 0.87]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 100 :: L40 :: 0.85 [0.83, 0.87] --> / 0.94 [0.93, 0.96]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 100 :: L40 :: 0.94 [0.93, 0.96] --> |
  | the locker slot: the full state | 0.88 [0.84, 0.91]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 25 :: L20 :: 0.88 [0.84, 0.91] --> (L20) | 0.99 [0.98, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 25 :: L48 :: 0.99 [0.98, 1.00] --> (L48) | 0.94 [0.92, 0.95]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.94 [0.92, 0.95] --> (L34) | 0.96 [0.94, 0.97]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 25 :: L34 :: 0.96 [0.94, 0.97] --> (L34) | 0.96 [0.95, 0.98]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 25 :: L40 :: 0.96 [0.95, 0.98] --> (L40) |
  | the rule, k = 25 / k = 100 | **J-space blind to X<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (b) its locker slot :: 25 :: L20 :: J-space blind to X -->** / in between | **in between<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (b) its locker slot :: 25 :: L48 :: in between -->** / in between | **J-space blind to X<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (b) its locker slot :: 25 :: L34 :: J-space blind to X -->** / in between | **in between<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (b) its locker slot :: 25 :: L34 :: in between -->** / in between | **J-space blind to X<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 25 :: L40 :: J-space blind to X -->** / in between<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (b) its locker slot :: 100 :: L40 :: in between --> |
  | the decided energy rule, k = 25 and 100 | the address is under-represented in the lens directions | the address is under-represented in the lens directions | the address is under-represented in the lens directions | the address is under-represented in the lens directions | the address is under-represented in the lens directions |
  | the locker slot at the bridge word, and on JSON scenes | in between (the full state under 0.8) | in between (the full state under 0.8) | in between (the full state under 0.8) | in between (the full state under 0.8) | in between at the bridge word; on JSON scenes J-space blind at the last token |
  | the lookup's digit at the last token, k = 100: lens part / random | 0.99 [0.98, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (c) lookup's digit :: 100 :: L30 :: 0.99 [0.98, 1.00] --> / 0.99 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: T :: (c) lookup's digit :: 100 :: L30 :: 0.99 [0.99, 1.00] --> (L30; many subspaces) | 1.00 [1.00, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (c) lookup's digit :: 100 :: L52 :: 1.00 [1.00, 1.00] --> / 1.00 [1.00, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.6-27B :: main :: T :: (c) lookup's digit :: 100 :: L52 :: 1.00 [1.00, 1.00] --> (L52; in between) | 1.00 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (c) lookup's digit :: 100 :: L40 :: 1.00 [0.99, 1.00] --> / 0.99 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Muse-Glimmer-30B :: main :: T :: (c) lookup's digit :: 100 :: L40 :: 0.99 [0.99, 1.00] --> (L40; many subspaces) | 1.00 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (c) lookup's digit :: 100 :: L34 :: 1.00 [0.99, 1.00] --> / 0.99 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Nemotron-3.5-Lightning :: main :: T :: (c) lookup's digit :: 100 :: L34 :: 0.99 [0.99, 1.00] --> (L34; many subspaces) | 1.00 [1.00, 1.00]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (c) lookup's digit :: 100 :: L46 :: 1.00 [1.00, 1.00] --> / 1.00 [0.99, 1.00]<!-- src: results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md \| Qwen3.5-122B-A10B :: main :: T :: (c) lookup's digit :: 100 :: L46 :: 1.00 [0.99, 1.00] --> |

- **Read.**
  - The lens readout does not show the address (47.0). At the last token the full state reads the locker slot, and at that layer a probe on the lens part's coordinates reads it no better than a random subspace of the same size on all four models. The rule, over every layer: "J-space blind" on the 9B and Muse at k = 25; in between on the 27B and Lightning, and on all four at k = 100.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Against random directions of the same energy the lens part reads the slot worse on all four models, at both sizes: the address is under-represented in the lens directions, not an energy artefact.
  - At the bridge word and on JSON scenes the full state reads the slot under 0.8, so the rule can't tell there. The lookup's answer digit at the last token, k = 100, is decodable from many subspaces, the lens part included (7 of the 8 model and dataset cells; the 27B's main test in between); at the bridge word even the full state reads it near chance (the 9B: 0.13 [0.11, 0.16]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: B :: (c) lookup's digit :: 25 :: L0 :: 0.13 [0.11, 0.16] --> vs chance 0.12 [0.09, 0.15]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: B :: (c) lookup's digit :: 25 :: L0 :: 0.12 [0.09, 0.15] -->).


- The positive controls work: at the bridge word the full state reads which item is the bridge and the recall's answer at 0.99 or more at its best layer, on every model and dataset. The recall's answer there is "J-space carries X" at k = 25 on 7 of the 8 cells (the 9B: lens part 0.98 [0.96, 0.99]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: B :: (d) recall's answer :: 25 :: L14 :: 0.98 [0.96, 0.99] --> vs random 0.68 [0.63, 0.71]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: B :: (d) recall's answer :: 25 :: L14 :: 0.68 [0.63, 0.71] -->), but no different from random directions of the same energy (0.97 [0.95, 0.98]<!-- src: results/x53_monitor/x53_monitor-20261029T124428Z/verdict.md \| Qwen3.5-9B :: main :: B :: (d) recall's answer :: 25 :: L14 :: 0.97 [0.95, 0.98] -->). The controls' full labels are in the verdict, under their own heading.

- **Caveats.**
  - The verdict flags its readings of the rule's wordings: "while" read as at some layer where the full state reaches 0.8, "within 0.10" as at every layer, "random is under 0.8" as at every layer, and the target named in the "many subspaces" wording for the digit.
  - The lens part is fit to each state and keeps more of its energy than a fixed random subspace of the same k; the energy-matched random subspace and a fixed lens subspace are the verdict's check on that.
  - One regularisation for every probe (the brief's): a low ceiling for the full state, as for the slot at the bridge word, can be the probe rather than the state (not checked). The positive controls are probed on held-out scenes, not held-out entities, so the recall's answer at the bridge word can be the bridge's identity mapped to its answer (not checked).
  - Exploratory (batch 53), no prediction.
- **The 122B (addendum; coverage, not hand-checked; Dan 12:20 / 18:20).** [verdict](../../results/x53_monitor/x53_monitor_122b-20261029T175223Z/verdict.md), L33 carried over, FP8, the same rule, not part of the four models' verdict. At the last token, main test: the locker slot "J-space blind to X" at k = 25 (in between at k = 100), and under the energy rule "the address is under-represented in the lens directions" at both sizes, as on the four models. JSON scenes, last token: the slot "J-space blind to X" at both sizes and under-represented by the energy rule (the full state reaches 0.80 there, at the bar). The lookup's digit at the last token, both datasets, k = 25 and 100: decodable from many subspaces, J++ included (random reads it too; energy rule: no different from random directions of the same energy). At the bridge word the full state reads the slot and the digit under 0.8: can't tell.

</details>

### Asked for the position, does the address surface in the lens? <a id="t47-10"></a>

`in README` `below gate: 9B, Muse, Lightning` *Used in: README Part III card "Can the lens read the address?" (the report prompt).*

Test 47.10 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_report/x47_10-20261028T113109Z/x47_10.md` · recompute: `scripts/x47_report.py` (the command in its docstring) · also: the report prompt, opened 28 Oct; Lightning's gate 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the prompt asks which locker sentence holds the item (a report reader), does the lens at the bridge word show the right ordinal, and does the report need the lens part or the address?
- **Why we asked.** The lens cannot read the address under the lookup's prompt; asked for it directly, the model might surface it into the lens.
- **Data.** Routes scenes without a move, four readers as separate prompts over the same context, question last or first: the 27B, question last, 200<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen3.6-27b :: last :: 200 --> scenes. Every other cell failed its gate (the report reader below 0.80): the 9B, Muse, the 27B with the question first, and Lightning (its report right on 0.488<!-- src: results/x47_report/x52_report-20261029T023828Z/x47_10.md \| last: gate :: 0.488 --> with the question last).
- **Method.** At the bridge word at L: the lens readout's top five under the report prompt and under the lookup prompt; the report's switches blocked without the lens part and without the address, each beyond a random part.

*No figure: one model tested (the 27B), three numbers: the Result's table.*

- **Rule, fixed in advance.** ""Surfaced on demand": under the report prompt the lens ranks the correct ordinal in its top-5 in >= 0.4 of items (under the lookup prompt <= 0.1), and the report has >= 0.3 blocked of its switches without J++ beyond random, while the lookup on the same scenes has <= 0.10 blocked (as before). "Reported late, not surfaced": the lens stays <= 0.1 at the bridge word under the report prompt and the report has <= 0.1 blocked without J++ but >= 0.3 without U [...]"

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lens top-5 holds the right ordinal, under the report prompt (bar >= 0.4) | not tested (gate 0.568<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen35_9b_x47_report, L12), last :: 0.568 --> < 0.80) | 0.00 [0.00, 0.00]<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen3.6-27b :: last :: 200 :: 0.00 [0.00, 0.00] --> | not tested (gate 0.498<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| muse30_x47_report, L26), last :: 0.498 --> < 0.80) | not tested (gate 0.488<!-- src: results/x47_report/x52_report-20261029T023828Z/x47_10.md \| nem35l_x52_report, L14), last :: 0.488 --> < 0.80) | not run |
  | the report: switches blocked without the lens part, beyond random | | 0.06 [0.02, 0.11]<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen3.6-27b :: last :: 200 :: 0.06 [0.02, 0.11] --> | | | |
  | the report: switches blocked without the address, beyond random | | 0.28 [0.21, 0.34]<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen3.6-27b :: last :: 200 :: 0.28 [0.21, 0.34] --> | | | |
  | the label (question last) | | **neither<!-- src: results/x47_report/x47_10-20261028T113109Z/x47_10.md \| qwen3.6-27b :: last :: 200 :: neither -->** | | | |

- **Read.**
  - Asked for the position, the 27B's lens never shows the right ordinal at the bridge word, and the report needs the address more than the lens part, but not by the 0.3 the rule asks: neither reading holds.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - One cell tested (the 27B, question last); every other cell failed its gate.
  - The report is blocked at 0.28 without the address, just under the rule's 0.3.

</details>

### Reworded, does the report read slot 1? <a id="t49-6"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 49.6 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x49_report/x49_6-20261028T154511Z/x49_6.md` · recompute: `scripts/x49_report.py` (the command in its docstring) · also: the report of slot 1 reworded, opened 28 Oct; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Asked for the position of the asked item's locker, the report reads slot 1 badly ([47.10](#t47-10)); asked in other words, does it read slot 1?
- **Why we asked.** If slot 1 stays unread under any wording, the report's gap is about slot 1 itself; if it recovers, it was the wording.
- **Data.** The report prompt's scenes without a move, the original prompt only, question last: 500 scenes, 147 with the asked item in slot 1 on the 9B and the 27B, 168 on Lightning.
- **Method.** Two new wordings of the report question: position (a digit: "Was the locker of <p>'s pick listed in position 1, 2 or 3 of the list?") and sentence (a word: "Which of the three locker sentences - the first, the second or the third - gives the locker of <p>'s pick?"); the share of scenes whose asked item sits in slot 1 that the report reads right, with the earlier report wording beside.

- **Rule, fixed in advance.** "if slot 1 stays <= 0.2 on the 9B under both wordings, keep as an appendix curiosity; if it recovers, drop." (results/x49_report/x49_6-20261028T154511Z/x49_6.md; Q49.6, Dan: 60%; Lightning a coverage run, no prediction)

The report under each wording:

![Reworded, the report reads slot 1 on every model tested](../../figures/depth/ledger/10_report_first_position.png)

*The model's report of where the item sits, reworded: the share of reports naming the first position under the earlier wording, when a digit is asked for and when a word is asked for, per model. Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | slot 1 read right, the earlier report wording | 0.03 [0.01, 0.05]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.5-9b :: 47.10 report :: read :: 0.03 [0.01, 0.05] --> | 0.71 [0.63, 0.79]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.6-27b :: 47.10 report :: read :: 0.71 [0.63, 0.79] --> | not designed | 0.29 [0.22, 0.35]<!-- src: results/x49_report/x52_report49-20261029T082508Z/x49_6.md \| nemotron-3.5-lightning :: 47.10 report :: read :: 0.29 [0.22, 0.35] --> | not run |
  | slot 1 read right, the position wording (bar 0.2) | 0.18 [0.11, 0.25]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.5-9b :: position :: read :: 0.18 [0.11, 0.25] --> | 0.68 [0.59, 0.76]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.6-27b :: position :: read :: 0.68 [0.59, 0.76] --> | | 0.29 [0.21, 0.37]<!-- src: results/x49_report/x52_report49-20261029T082508Z/x49_6.md \| nemotron-3.5-lightning :: position :: read :: 0.29 [0.21, 0.37] --> | |
  | slot 1 read right, the sentence wording (bar 0.2) | 0.61 [0.51, 0.70]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.5-9b :: sentence :: read :: 0.61 [0.51, 0.70] --> | 0.99 [0.96, 1.00]<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.6-27b :: sentence :: read :: 0.99 [0.96, 1.00] --> | | 0.46 [0.37, 0.55]<!-- src: results/x49_report/x52_report49-20261029T082508Z/x49_6.md \| nemotron-3.5-lightning :: sentence :: read :: 0.46 [0.37, 0.55] --> | |
  | the label | **recovers<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| ['sentence'] :: recovers -->** (decides: drop) | **recovers<!-- src: results/x49_report/x49_6-20261028T154511Z/x49_6.md \| qwen3.6-27b :: recovers -->** | | **recovers<!-- src: results/x49_report/x52_report49-20261029T082508Z/x49_6.md \| nemotron-3.5-lightning :: recovers -->** (no prediction) | |

- **Read.**
  - Under the sentence wording the 9B reads slot 1 right on most slot-1 scenes, against almost none under the earlier wording; by the rule, slot 1 recovers and the test is dropped. The 27B and Lightning recover under both new wordings.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - On the 9B the position wording stays just under the bar (0.18); the recovery rests on the sentence wording.
  - The 06:29 coverage matrix named this row "One question, two instructions" and marked the 9B's cell as a gate miss; the verdict scores the 9B. Fixed in the 09:45 matrix (fb9667eb; Appendix A, flag 28).
  - Lightning: a coverage run with the 9B / 27B design, no prediction.

</details>

### Do a few heads read the swapped address? <a id="t51-2"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 51.2 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_heads/x52_heads-20261029T015136Z/verdict.md` · recompute: `scripts/x51_heads.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Does a small set of attention heads carry the address swap's effect at the last token, or is it spread over heads?
- **Why we asked.** Attention follows the swapped address; a few heads could be the readers.
- **Data.** The attention test's items and swap (routes scenes): read pairs 330 / 300 / 284 / 250<!-- src: results/x51_heads/x52_heads-20261029T015136Z/verdict.md \| read pairs 250 :: 250 --> (9B / 27B / Muse / Lightning, at L14).
- **Method.** Heads ranked by their attention move on the fit half, mean-ablated together on the read half at the last token (and the question tokens), against random head sets of the same size in the same layers.

![No small set of heads carries the swapped address](../../figures/depth/readme/30_heads.png)

*The heads that pass the most of each part under the swap, on the 9B (top) and Muse (bottom), rows read from the run: what each head passes (median ‖W_OV x‖ / ‖x‖) of the lens part (teal), the rest (slate) and the address (amber), against a random part and twice the lens part (grey). Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "small_set: some top-k set, k in {1, 3, 5, 10}, cuts >= 0.5 while the identity answers (...) change <= 0.10 and the recall's answer changes <= 0.10 (...), and the matched random sets of k heads (same layers) cut <= 0.15 (mean over the draws). distributed: every head of the best layer together cuts < 0.3." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.** (last token)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | the best layer's heads together: share of the swap's switch cut | 0.027 [0.008, 0.044]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.448 -> 0.436 :: 0.027 [0.008, 0.044] --> | -0.061 [-0.283, 0.095]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.220 -> 0.233 :: -0.061 [-0.283, 0.095] --> | 0.020 [-0.007, 0.048]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.539 -> 0.528 :: 0.020 [-0.007, 0.048] --> | -0.008 [-0.061, 0.035]<!-- src: results/x51_heads/x52_heads-20261029T015136Z/verdict.md \| 0.500 -> 0.504 :: -0.008 [-0.061, 0.035] --> | not run |
  | the top 10 heads: cut | 0.007 [-0.065, 0.060]<!-- src: results/x51_heads/x51_2-20261028T190358Z/verdict.md \| 0.448 -> 0.445 :: 0.007 [-0.065, 0.060] --> | | | 0.040 [0.015, 0.071]<!-- src: results/x51_heads/x52_heads-20261029T015136Z/verdict.md \| 0.500 -> 0.480 :: 0.040 [0.015, 0.071] --> | |
  | the rule | **distributed** | **distributed** | **distributed** | **distributed<!-- src: results/x51_heads/x52_heads-20261029T015136Z/verdict.md \| Question tokens beside: distributed :: distributed -->** (the question tokens too; no prediction) | |

- **Read.**
  - No small set of heads carries the swap's effect on any of the four models; even all heads of the best layer together cut almost none of it.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Linear-attention layers have no heads: Gated DeltaNet on the 9B and 27B, Mamba-2 on Lightning (its verdict says Gated DeltaNet, a wording inherited from Muse's run).
  - Mean ablation at the last token and the question tokens only.

</details>

### Do attention heads follow the swapped address to its locker? <a id="t49-7"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 49.7 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x49_attn/x49_7-20261028T154511Z/verdict.md` · recompute: `scripts/x49_attn.py` (the command in its docstring) · also: attention under the swap; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the address swap sends the lookup to another locker, does some attention head at the last token move its weight to that locker on the pairs that switched, and only there?
- **Why we asked.** A head that reads the address should move with the swap where the lookup switches and stay put where it does not.
- **Data.** The address swap's routes items at dose 2, heads chosen on one half and read on the other: 330<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 330, switched 148 :: 330 --> / 300<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 300, switched 66 :: 300 --> / 286<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 286, switched 149 :: 286 --> / 250<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| Read pairs 250, switched 125 :: 250 --> read pairs, of which 148<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 330, switched 148 :: 148 --> / 66<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 300, switched 66 :: 66 --> / 149<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| Read pairs 286, switched 149 :: 149 --> / 125<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| Read pairs 250, switched 125 :: 125 --> switched (9B / 27B / Muse / Lightning).
- **Method.** At every full-attention layer after L, every head: the attention mass moved from the original locker to the swapped-in one at the last token (the question tokens beside), on switched and non-switched pairs and under a random vector of the swap's size; the best head zeroed as a necessity check.

![Heads move with the swap even where the lookup did not switch](../../figures/depth/readme/32_attention.png)

*The last token's attention on the old and the new locker sentence under the address swap (amber), on the scenes where the answer switched and where it stayed, against no change and a random vector (grey), per model. Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "follows: on read-half pairs where the lookup switched to slot k's locker under the swap, >= 1 of the five candidate heads has mean move >= 0.30 (cluster-bootstrap CI excluding 0), its mean move under the random vector on the same pairs <= 0.05, and its mean move on the non-switched swap pairs <= 0.10. elsewhere: the lookup switches to slot k on >= 0.3 of the read-half swap pairs and no recorded head [...] reaches a mean move of 0.15 on the switched pairs. distributed: the summed mean move over the five candidate heads, or over every head of the best head's layer, is >= 0.30 while no single candidate head reaches 0.30." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | best head (chosen on the fit half) | L27:h1<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 1.301 [1.237, 1.370] :: L27:h1 --> | L51:h20<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 1.412 [1.334, 1.507] :: L51:h20 --> | L39:h1<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 1.710 [1.670, 1.748] :: L39:h1 --> | L33:h7<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| 1.779 [1.746, 1.812] :: L33:h7 --> | not run |
  | its attention moved, pairs that switched | 1.301 [1.237, 1.370]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L27:h1 :: 1.301 [1.237, 1.370] --> | 1.412 [1.334, 1.507]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L51:h20 :: 1.412 [1.334, 1.507] --> | 1.710 [1.670, 1.748]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L39:h1 :: 1.710 [1.670, 1.748] --> | 1.779 [1.746, 1.812]<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| L33:h7 :: 1.779 [1.746, 1.812] --> | |
  | the same, pairs that did not switch (bar 0.10) | 0.196 [0.154, 0.247]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L27:h1 :: 0.196 [0.154, 0.247] --> | 0.183 [0.135, 0.237]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L51:h20 :: 0.183 [0.135, 0.237] --> | 0.409 [0.334, 0.473]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L39:h1 :: 0.409 [0.334, 0.473] --> | 0.312 [0.233, 0.394]<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| L33:h7 :: 0.312 [0.233, 0.394] --> | |
  | the same under a random vector, switched pairs (bar 0.05) | 0.004 [0.000, 0.008]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L27:h1 :: 0.004 [0.000, 0.008] --> | -0.010 [-0.018, -0.000]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L51:h20 :: -0.010 [-0.018, -0.000] --> | 0.015 [0.007, 0.021]<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| L39:h1 :: 0.015 [0.007, 0.021] --> | -0.001 [-0.005, 0.003]<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| L33:h7 :: -0.001 [-0.005, 0.003] --> | |
  | the head zeroed: lookups switched, swap -> zeroed | 0.448 -> 0.448<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 330 :: 0.448 -> 0.448 --> | 0.220 -> 0.217<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 300 :: 0.220 -> 0.217 --> | 0.535 -> 0.517<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| 286 :: 0.535 -> 0.517 --> | 0.500 -> 0.516<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| 250 :: 0.500 -> 0.516 --> | |
  | the rule | **neither<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| distributed: no :: neither -->** | **neither<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| distributed: no :: neither -->** | **neither<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| distributed: no :: neither -->** | **neither<!-- src: results/x49_attn/x52_attn-20261029T013321Z/verdict.md \| distributed: no :: neither -->** (no prediction) | |

- **Read.**
  - On all four models the best head moves its attention to the swapped-in locker where the lookup switched, but also, above the 0.10 bar, where it did not; zeroing it leaves the switch in place. No head follows the address by the rule: neither, on all four.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Only full-attention layers after L are recorded. Lightning's verdict calls its skipped blocks "Gated DeltaNet", a wording inherited from Muse's run; on Lightning they are Mamba-2 blocks.
  - The 27B's lookup switches on 0.220<!-- src: results/x49_attn/x49_7-20261028T154511Z/verdict.md \| switch share 0.220 :: 0.220 --> of read pairs, under the 0.3 that "elsewhere" needs.

</details>

### Does the second hop, hall to locker, run through an address too? <a id="t47-14"></a>

`in README` `below gate: Lightning` *Used in: README Part VI, one line with a link ("the second hop's key token").*

Test 47.14 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_chain/x47_14-20261028T115841Z/x47_14.md` · recompute: `scripts/x47_chain.py` (the command in its docstring) · also: chained addresses; the 27B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** With hall sentences before the locker sentences, is the hall of the pick's locker read through an address at the locker digit, as the locker is read through one at the bridge word?
- **Why we asked.** If the address is a general reference to a place, the next hop (locker to hall) should use one too.
- **Data.** Hall scenes, the test half: 147<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: 147 --> / 146<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: 146 --> / 153<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: 153 --> (9B / 27B / Muse). Lightning not tested: its gate failed (the hall question right on 0.736<!-- src: results/x47_chain/nem35l_x52_chain/gate.json \| "PPP" :: 0.736 --> of 500<!-- src: results/x47_chain/nem35l_x52_chain/gate.json \| "cases" :: 500 --> cases, under 0.80).
- **Method.** The change at the digit token of the bridge's locker sentence at L: the hall address (U_num) taken out or retained alone, against random parts of its share; the hall question's answers sorted into identity, position and value; the locker question's answer as the collateral.

![The hall is readable at the locker digit, yet a random part cuts nearly as much](../../figures/depth/readme/25_chain.png)

*Chained addresses, the hall before the locker: a probe for the hall address (amber) against a random part and a layout-only probe (grey); the hall answers by position without the hall address and with only the hall address kept; the whole change in its own column. Lightning not tested. Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "probe >= 0.8 with the layout baseline <= 0.6; without U_num the hall question's position share falls >= 0.3 below the share without its random part; only U_num gives position >= 0.15; the locker question's unchanged share within 0.05 of unedited under every arm; on both models." The 27B: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | the hall readable at the locker digit: slot probe (layout baseline) | 1.00 [1.00, 1.00]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: 1.00 [1.00, 1.00] --> (0.33 [0.28, 0.38]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: 0.33 [0.28, 0.38] -->) | 1.00 [1.00, 1.00]<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: 1.00 [1.00, 1.00] --> (0.34 [0.29, 0.40]<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: 0.34 [0.29, 0.40] -->) | 1.00 [1.00, 1.00]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: 1.00 [1.00, 1.00] --> (0.34 [0.28, 0.41]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: 0.34 [0.28, 0.41] -->) | not tested (gate 0.736<!-- src: results/x47_chain/nem35l_x52_chain/gate.json \| "PPP" :: 0.736 --> < 0.80) | 1.00 [1.00, 1.00]<!-- src: results/x47_chain/x52_chain-20261030T094553Z/x47_14.md \| qwen35_122b_chain :: 1.00 [1.00, 1.00] --> (0.34 [0.29, 0.39]<!-- src: results/x47_chain/x52_chain-20261030T094553Z/x47_14.md \| qwen35_122b_chain :: 0.34 [0.29, 0.39] -->) |
  | hall answers cut by taking out the hall address, beyond random (bar >= 0.3) | 0.05 [0.02, 0.08]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: 0.05 [0.02, 0.08] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: 0.00 [0.00, 0.00] --> | | 0.07 [0.02, 0.13]<!-- src: results/x47_chain/x52_chain-20261030T094553Z/x47_14.md \| qwen35_122b_chain :: 0.07 [0.02, 0.13] --> |
  | position answers with only the hall address retained (bar >= 0.15) | 0.39 [0.32, 0.46]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: 0.39 [0.32, 0.46] --> | 0.23 [0.17, 0.28]<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: 0.23 [0.17, 0.28] --> | 0.05 [0.01, 0.08]<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: 0.05 [0.01, 0.08] --> | | 0.37 [0.28, 0.47]<!-- src: results/x47_chain/x52_chain-20261030T094553Z/x47_14.md \| qwen35_122b_chain :: 0.37 [0.28, 0.47] --> |
  | the rule, per model | **no<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| qwen35_9b_x47_14 :: no -->** | **no<!-- src: results/x47_chain/x52_chain-20261029T023424Z/x47_14.md \| x47_14_27b :: no -->** | **no<!-- src: results/x47_chain/x47_14-20261028T115841Z/x47_14.md \| muse30_x47_14 :: no -->** | | **no** (no prediction) |

- **Read.**
  - On the 9B, 27B and Muse the hall is readable at the locker digit, but taking out the hall address cuts no more hall answers than a random part: the second hop does not run through an address the way the first does.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The verdicts' batch line ("0 of 2 models hold; the rule needs both") applies the across-models clause; the per-model labels are the result.
  - Retained alone, the hall address gives position answers above the 0.15 bar on the 9B and 27B; only its removal fails.

</details>

### Must the address be refit for each text format? <a id="x45d"></a>

`in README` *Used in: README Part III card "Must the address be refit for each text format?".*

Test x45d · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md` · recompute: `scripts/x0b_generalize.py` (the command in its docstring) · also: address refit per format; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On varied scenes (prose, JSON, tables), does an address refit on each format's own scenes carry the lookup's position answers, where the address fit on simple scenes does little?
- **Why we asked.** The address was fit on one template; in other formats the code may sit elsewhere.
- **Data.** The held-out half of the varied scenes per format, the bridge items not used for the fit; Lightning prose / JSON / table: 191<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| prose :: the refit basis (rank 4, the other half) :: lookup :: 191 --> / 40<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| json :: the refit basis (rank 4, the other half) :: lookup :: 40 --> / 187<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| table :: the refit basis (rank 4, the other half) :: lookup :: 187 --> (the other models' n in the verdicts).
- **Method.** The address refit per format on one half (rank 4) and taken out of the change at the bridge word at L on the other half, against a random part of its share; the address fit on simple scenes beside.

- **Rule, fixed in advance.** ""Pointer elsewhere" [pointer: the address] if the refit basis gives a lookup extra drop of at least 0.2, with lower CI above 0.1, in 2 of 3 formats; "No linear pointer found" [pointer: the address] if all three formats are below 0.1 (point estimate); otherwise neither." Added after the first results (Dan, 26 Oct ~21:20): a format whose lookup has fewer than 30 switches under the whole change does not count. Lightning: a coverage run, no prediction.

The fitted address against one refit per format:

![The address must be refit for each text format](../../figures/depth/readme/34_transfer.png)

*Top, after the data: the switches blocked beyond a random part without the lens part (teal) and without the address fit on simple scenes (orange), per model and setting, all hollow ○. Bottom, rule 45d: per format, without the address fit on simple scenes (left) and refit on that format (right); a cell under its switch bar says so. Whiskers 95% intervals.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | prose: lookup blocked without the refit address, beyond random | 0.24 [0.16, 0.32]<!-- src: results/x0b_generalize/qwen35_9b_x45d/x45d-20261026T202025Z/verdict.md \| prose :: the refit basis (rank 4, the other half) :: lookup :: 223 :: 0.24 [0.16, 0.32] --> | 0.08 [0.04, 0.13]<!-- src: results/x0b_generalize/x45d_27b/x45d-20261026T202026Z/verdict.md \| prose :: the refit basis (rank 4, the other half) :: lookup :: 383 :: 0.08 [0.04, 0.13] --> | 0.23 [0.16, 0.31]<!-- src: results/x0b_generalize/muse30b_x45d/x45d-20261026T202027Z/verdict.md \| prose :: the refit basis (rank 4, the other half) :: lookup :: 270 :: 0.23 [0.16, 0.31] --> | 0.16 [0.11, 0.21]<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| prose :: the refit basis (rank 4, the other half) :: lookup :: 191 :: 0.16 [0.11, 0.21] --> | not run |
  | json: lookup blocked without the refit address, beyond random | 0.24 [0.16, 0.30]<!-- src: results/x0b_generalize/qwen35_9b_x45d/x45d-20261026T202025Z/verdict.md \| json :: the refit basis (rank 4, the other half) :: lookup :: 70 :: 0.24 [0.16, 0.30] --> | 0.09 [0.05, 0.12]<!-- src: results/x0b_generalize/x45d_27b/x45d-20261026T202026Z/verdict.md \| json :: the refit basis (rank 4, the other half) :: lookup :: 143 :: 0.09 [0.05, 0.12] --> | 0.38 [0.16, 0.65]<!-- src: results/x0b_generalize/muse30b_x45d/x45d-20261026T202027Z/verdict.md \| json :: the refit basis (rank 4, the other half) :: lookup :: 89 :: 0.38 [0.16, 0.65] --> (29 switches: does not count) | 0.26 [0.20, 0.40]<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| json :: the refit basis (rank 4, the other half) :: lookup :: 40 :: 0.26 [0.20, 0.40] --> | |
  | table: lookup blocked without the refit address, beyond random | 0.18 [0.13, 0.24]<!-- src: results/x0b_generalize/qwen35_9b_x45d/x45d-20261026T202025Z/verdict.md \| table :: the refit basis (rank 4, the other half) :: lookup :: 138 :: 0.18 [0.13, 0.24] --> | 0.13 [0.09, 0.17]<!-- src: results/x0b_generalize/x45d_27b/x45d-20261026T202026Z/verdict.md \| table :: the refit basis (rank 4, the other half) :: lookup :: 322 :: 0.13 [0.09, 0.17] --> | 0.47 [0.34, 0.60]<!-- src: results/x0b_generalize/muse30b_x45d/x45d-20261026T202027Z/verdict.md \| table :: the refit basis (rank 4, the other half) :: lookup :: 238 :: 0.47 [0.34, 0.60] --> | 0.25 [0.19, 0.32]<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| table :: the refit basis (rank 4, the other half) :: lookup :: 187 :: 0.25 [0.19, 0.32] --> | |
  | the outcome | **"pointer elsewhere<!-- src: results/x0b_generalize/qwen35_9b_x45d/x45d-20261026T202025Z/verdict.md \| Outcome :: pointer elsewhere -->"** [pointer: the address] | **neither<!-- src: results/x0b_generalize/x45d_27b/x45d-20261026T202026Z/verdict.md \| Outcome :: neither -->** | **"pointer elsewhere<!-- src: results/x0b_generalize/muse30b_x45d/x45d-20261026T202027Z/verdict.md \| Outcome :: pointer elsewhere -->"** [pointer: the address] | **"pointer elsewhere<!-- src: results/x0b_generalize/nem35l_x52_x45d/x45d-20261029T035250Z/verdict.md \| Outcome :: pointer elsewhere -->"** [pointer: the address] (no prediction) | |

- **Read.**
  - Refit on each format, the address carries the lookup again on the 9B, Muse and Lightning ("pointer elsewhere" [pointer: the address]); on the 27B it stays under 0.2 in every format (neither).

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 30-switch bar was set after the first results; it drops Muse's JSON (29 switches).
  - Lightning's JSON rests on 40 scenes from 4 bridge items.

</details>

### Does the address carry over to code and tool output? <a id="b53-7"></a>

`in README` *Used in: README Part III card "Is the address readable, and used, in Python code and tool output?"; adapted design: lookup-only gate, the recall is not part of this test.*

Test 53.7 · opened not stated · status: rule fixed in advance (part descriptive) · hand-check: not in sample · files: `results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md` · recompute: `scripts/x0_probe.py` (the command in its docstring) · also: adapted design; the 9B and the 27B, code and tool output, 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Does the address carry over to code and tool output: does a probe read it at the bridge word, and does the routes test find the lookup using it, when the scene is rendered as Python or as a tool's response?

![In code and tool output the address carries the position route](../../figures/depth/readme/04_code_tool.png)

*Python code and tool output on the 9B and the 27B (rows): the locker probe's accuracy for the address (amber) against a random part and a layout-only probe (grey); the lookups left on position without the address, and brought back with only the address kept. The 9B's code probe is below its gate. Whiskers: 95% intervals.*


- **Why we asked.** The address is found in prose, JSON and tables ([probe](#probe), [routes](#routes), [refit](#x45d)); code and tool output are where an address would matter in practice.

- **Data.** Our locker scenes rendered as Python (one assignment per statement) and as the response of a declared tool (the scene's text verbatim). Routes test: 300 scenes per condition and format on the 9B (L12) and the 27B (L32), every gate passed. Probe: the 9B in tool output, 1500 scenes; the 27B in code (682 scenes) and in tool output (1500); the 9B in code is not tested (gate 0.669<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: code :: lookup says and reads O and S right :: 0.669 --> < 0.80). Monitor (53.2's probes): the 9B in tool output, 400 rows; the 9B in code not tested (gate 0.702<!-- src: results/x53_monitor/x53_7_monitor-20261029T130113Z/verdict.md \| Qwen3.5-9B :: code :: d1_topics_v3 (272 scenes) :: 0.702 --> < 0.80); the 27B not completed in the sprint.

- **Method.** The routes test's arms (the whole change, without the address against a random part of its share, the address alone) at the bridge word at L, as in prose; the address probe (x0_probe v4) at the bridge word at L, which locker sentence holds the item's locker, locker first and locker after (the control); the monitor test (53.2's probes on the lens part, a random subspace, an energy-matched random subspace and the full state) in tool output. The address U is carried over from prose, not refit: the same layout-free mass-mean of the bridge word's prose probe states at L in every format (the verdict says so; each run's manifest records it as alf_from).

- **Rule, fixed in advance.** The routes test's, verbatim: "A route counts as used if its share is >= 0.2 with lower CI >= 0.1." The probe: none (descriptive, as x0_probe v4). The gate (Dan 12:10, decisions_1210, before any routes or probe result was opened): "use a lookup-only gate (the lookup says and reads O and S right, >= 0.80) [...] label "adapted design: lookup-only gate; the recall is not part of this test". The recall columns are reported descriptively." (jobs/c3/batch53.yaml; no prediction)

</details>

- **Result.** (condition C2, another item moved; each cell code; tool output)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | routes, the whole change: position | 0.54 [0.50, 0.59]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: code :: C2 :: the whole change :: 0.54 [0.50, 0.59] -->; 0.46 [0.41, 0.51]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C2 :: the whole change :: 0.46 [0.41, 0.51] --> | 0.20 [0.16, 0.25]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: code :: C2 :: the whole change :: 0.20 [0.16, 0.25] -->; 0.27 [0.22, 0.32]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C2 :: the whole change :: 0.27 [0.22, 0.32] --> | not designed | not designed | not designed (adapted design: the probe only, lookup-only gate) |
  | routes, the whole change: identity | 0.38 [0.32, 0.43]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: code :: C2 :: the whole change :: 0.38 [0.32, 0.43] -->; 0.50 [0.45, 0.54]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C2 :: the whole change :: 0.50 [0.45, 0.54] --> | 0.77 [0.73, 0.82]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: code :: C2 :: the whole change :: 0.77 [0.73, 0.82] -->; 0.72 [0.67, 0.77]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C2 :: the whole change :: 0.72 [0.67, 0.77] --> | | | |
  | routes: position without the address | 0.31 [0.27, 0.35]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: code :: C2 :: without the address :: 0.31 [0.27, 0.35] -->; 0.09 [0.05, 0.12]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C2 :: without the address :: 0.09 [0.05, 0.12] --> | 0.09 [0.06, 0.12]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: code :: C2 :: without the address :: 0.09 [0.06, 0.12] -->; 0.09 [0.06, 0.13]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C2 :: without the address :: 0.09 [0.06, 0.13] --> | | | |
  | routes: the same without a random part of its share | 0.53 [0.49, 0.58]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: code :: C2 :: without a random part (the address's share) :: 0.53 [0.49, 0.58] -->; 0.48 [0.42, 0.53]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C2 :: without a random part (the address's share) :: 0.48 [0.42, 0.53] --> | 0.16 [0.13, 0.20]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: code :: C2 :: without a random part (the address's share) :: 0.16 [0.13, 0.20] -->; 0.21 [0.17, 0.26]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C2 :: without a random part (the address's share) :: 0.21 [0.17, 0.26] --> | | | |
  | routes: position, the address alone | 0.03 [0.01, 0.04]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: code :: C2 :: the address alone :: 0.03 [0.01, 0.04] -->; 0.08 [0.05, 0.12]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C2 :: the address alone :: 0.08 [0.05, 0.12] --> | 0.01 [0.00, 0.02]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: code :: C2 :: the address alone :: 0.01 [0.00, 0.02] -->; 0.06 [0.04, 0.08]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C2 :: the address alone :: 0.06 [0.04, 0.08] --> | | | |
  | routes used: the whole change / the address alone | identity, position / original | identity, position / original | | | |
  | probe in code: which locker sentence, locker first / the layout alone / locker after (the control) | ○ not tested (gate 0.669<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: code :: lookup says and reads O and S right :: 0.669 --> < 0.80; gate changed after the data) | 0.95 [0.92, 0.98]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: code :: before :: locker sentence :: 0.95 [0.92, 0.98] --> / 0.48 [0.42, 0.53]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: code :: before :: locker sentence :: 0.95 [0.92, 0.98] :: 0.48 [0.42, 0.53] --> / 0.38 [0.34, 0.43]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: code :: after :: locker sentence :: 0.38 [0.34, 0.43] --> (the prose probe beside: 0.99 [0.98, 1.00]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: code :: before :: locker sentence :: 0.95 [0.92, 0.98] :: 0.48 [0.42, 0.53] :: 0.99 [0.98, 1.00] -->) | | | 0.92 [0.88, 0.95]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: code :: before :: locker sentence :: 0.92 [0.88, 0.95] --> / 0.44 [0.38, 0.50]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: code :: before :: locker sentence :: 0.44 [0.38, 0.50] --> / 0.40 [0.36, 0.44]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: code :: after :: locker sentence :: 0.40 [0.36, 0.44] --> ○ |
  | probe in tool output: which locker sentence, locker first / the layout alone / locker after (the control) | 0.97 [0.95, 0.98]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: before :: locker sentence :: 0.97 [0.95, 0.98] --> / 0.53 [0.50, 0.56]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: before :: locker sentence :: 0.53 [0.50, 0.56] --> / 0.31 [0.28, 0.34]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: after :: locker sentence :: 0.31 [0.28, 0.34] --> (the prose probe beside: 0.97 [0.96, 0.98]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: before :: locker sentence :: 0.97 [0.96, 0.98] -->) | 0.99 [0.98, 0.99]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: tool :: before :: locker sentence :: 0.99 [0.98, 0.99] --> / 0.53 [0.50, 0.56]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: tool :: before :: locker sentence :: 0.99 [0.98, 0.99] :: 0.53 [0.50, 0.56] --> / 0.34 [0.31, 0.37]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: tool :: after :: locker sentence :: 0.34 [0.31, 0.37] --> (the prose probe beside: 0.99 [0.98, 1.00]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: tool :: before :: locker sentence :: 0.99 [0.98, 0.99] :: 0.53 [0.50, 0.56] :: 0.99 [0.98, 1.00] -->) | | | 0.93 [0.91, 0.95]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: tool :: before :: locker sentence :: 0.93 [0.91, 0.95] --> / 0.40 [0.37, 0.44]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: tool :: before :: locker sentence :: 0.40 [0.37, 0.44] --> / 0.34 [0.32, 0.37]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: tool :: after :: locker sentence :: 0.34 [0.32, 0.37] --> ○ |
  | probe: the answer digit, locker first, code; tool output (chance 0.11<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: before :: answer digit :: 0.26 [0.23, 0.30] :: 0.11 -->) | ○ not tested; 0.26 [0.23, 0.30]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.5-9B :: tool :: before :: answer digit :: 0.26 [0.23, 0.30] --> | 0.30 [0.23, 0.35]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: code :: before :: answer digit :: 0.30 [0.23, 0.35] -->; 0.40 [0.37, 0.43]<!-- src: results/x0_probe/x53_7_probe-20261029T130251Z/verdict.md \| Qwen3.6-27B :: tool :: before :: answer digit :: 0.40 [0.37, 0.43] --> | | | 0.19 [0.15, 0.23]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: code :: before :: answer digit :: 0.19 [0.15, 0.23] -->; 0.25 [0.21, 0.28]<!-- src: results/x0_probe/x53_7_probe-20261030T002257Z/verdict.md \| qwen3.5-122b-a10b :: tool :: before :: answer digit :: 0.25 [0.21, 0.28] --> ○ |
  | monitor in tool output: the slot at the last token, k = 25 / 100 (53.2's rule) | in between / in between: the full state 0.93<!-- src: results/x53_monitor/x53_7_monitor-20261029T130113Z/verdict.md \| Qwen3.5-9B :: tool_l (n 400 rows, 46 entities) :: T :: (b) the bridge item's locker slot (the address) :: 0.93 -->, the lens part 0.62<!-- src: results/x53_monitor/x53_7_monitor-20261029T130113Z/verdict.md \| Qwen3.5-9B :: tool_l (n 400 rows, 46 entities) :: T :: (b) the bridge item's locker slot (the address) :: 0.93 :: 0.62 --> at k = 25; against energy-matched random: under-represented in the lens directions (code: not tested, gate 0.702<!-- src: results/x53_monitor/x53_7_monitor-20261029T130113Z/verdict.md \| Qwen3.5-9B :: code :: d1_topics_v3 (272 scenes) :: 0.702 --> < 0.80) | not completed in the sprint | | | |
  | monitor in tool output: the lookup's digit at the bridge word | not decodable: the full state 0.12<!-- src: results/x53_monitor/x53_7_monitor-20261029T130113Z/verdict.md \| Qwen3.5-9B :: tool_l (n 400 rows, 46 entities) :: B :: (c) the lookup's answer digit :: 0.12 --> | not completed in the sprint | | | |

- **Read.**
  - In code and in tool output the lookup takes the item's identity or its locker's position, never the value, on the 9B and the 27B; removing the address cuts position answers beyond a random part of its share in both formats on both models.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Added by itself, the address brings few position answers back in either format (in prose it brought them back on the 9B, [routes](#routes)); the only route it uses is the original answer.
  - The probe reads which locker sentence holds the item's locker, locker first, as in prose: the 9B in tool output and the 27B in code and in tool output; locker after it reads no better than the baselines. The answer digit, locker first, reads above chance but far below the locker sentence.


- On the 9B in tool output the monitor test reads as in prose: the full state reads the slot at the last token, the lens part in between, and worse than random directions of the same energy (under-represented in the lens directions); the lookup's digit at the bridge word is not decodable even from the full state.

- **Caveats.**
  - Dan (12:10b), verbatim: tool output as prose (JSON is covered by x0b_v2), and the bridge ~250 tokens later in the tool format, not separated from the format (47.16's distance robustness beside). The probe only shows the address is readable; the routes test decides whether the lookup uses it.
  - In condition C1 (two picks swap) in tool output a random part of the address's share already cuts position to 0.06 [0.03, 0.08]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.5-9B :: tool :: C1 :: without a random part (the address's share) :: 0.06 [0.03, 0.08] --> on the 9B and 0.02 [0.01, 0.04]<!-- src: results/x6_routes/x53_7_routes-20261029T122509Z/verdict.md \| Qwen3.6-27B :: tool :: C1 :: without a random part (the address's share) :: 0.02 [0.01, 0.04] --> on the 27B: there the removal cannot tell the address from a random part.
  - Adapted design: the lookup-only gate replaces X0's two-reader gate; the recall's rates are descriptive. The 27B's probes and the 9B tool probe pass either gate or were computed after the decision; the 9B code probe is not tested (hollow: its gate was changed after the data).
  - U is carried over from prose, not refit in code or tool output (Dan 13:15 asked): the address fit on prose scenes is the one removed and added. The monitor on the 27B was not completed in the sprint; the CH2 add-on on the code's address (descriptive) is left out.
  - Exploratory (batch 53): no prediction.

</details>

## Part IV. Where and when the link is made

### Does the bridge word redirect most lookups when its locker sentence came first, and few when after? <a id="order"></a>

`in README` *Used in: README Part IV card "Does the bridge word redirect most lookups when its locker sentence came first, and few when after?" (the split).*

Test the split by sentence order · opened 29 Oct · status: post hoc (descriptive) · hand-check: in sample (view g) · files: `results/x0_composition/split-by-order-20261026T173323Z/split.md` · recompute: `scripts/x0_composition.py` (the command in its docstring) · also: Lightning's

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the main test, does the change at the bridge word switch the lookup when the item's locker sentence came before the asked pick, and when it came after?

![The bridge word switches the lookup when its locker came first](../../figures/common/readme/09_sentence_order.png)

*Lookups switched by the whole change when the locker sentence comes first and when it comes after the pick, per model, and (post hoc, hollow ○) with the changed prompt's locker sentence before or after the pick, for each original order. Whiskers: 95% cluster-bootstrap intervals over bridge entities; n per cell in the depth README; Lightning ○ (gate chosen after its pre-check). The sentence order is view g of the hand-checked sample; the 2 × 2 is post hoc and was not hand-checked.*


- **Why we asked.** The bridge word can only point back: if the locker sentence comes after it, the link must be made elsewhere.

- **Data.** Main test, 200 per model, split by where the item's locker sentence sits: before the pick 100 / 101 / 92 / 85 / 85, after it 100 / 99 / 108 / 115 / 115 (9B / 27B / Muse / Lightning / the 122B, FP8; MoE, ~10B active, at its L33).

- **Method.** The conflict test's cells, split by sentence order: the lookup's switch under the whole change, and each reader's switches blocked without the lens part beyond a random part.

- **Rule, fixed in advance.** None: the split was read after the data (descriptive); Lightning's is a coverage run, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookups switched by the whole change, locker first | 0.86<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.35 [0.26, 0.43] :: 0.86 --> | 0.76<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.67 [0.58, 0.76] :: 0.76 --> | 0.65<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.68 [0.46, 0.88] :: 0.65 --> | 0.86<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.12 [0.04, 0.20] :: 0.86 --> | 0.89<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: before :: 0.89 --> |
  | lookups switched by the whole change, locker after | 0.19<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.65 [0.57, 0.73] :: 0.19 --> | 0.09<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.81 [0.71, 0.91] :: 0.09 --> | 0.09<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.80 [0.65, 0.92] :: 0.09 --> | 0.15<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.53 [0.40, 0.65] :: 0.15 --> | 0.11<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: after :: 0.11 --> |
  | lookup: switches blocked beyond a random part, locker first | 0.01 [-0.04, 0.07]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.35 [0.26, 0.43] :: 0.01 [-0.04, 0.07] --> | 0.14 [0.07, 0.22]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.67 [0.58, 0.76] :: 0.14 [0.07, 0.22] --> | -0.07 [-0.12, -0.02]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.68 [0.46, 0.88] :: -0.07 [-0.12, -0.02] --> | 0.01 [-0.03, 0.07]<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.12 [0.04, 0.20] :: 0.01 [-0.03, 0.07] --> | -0.01 [-0.08, 0.06]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: before :: -0.01 [-0.08, 0.06] --> |
  | lookup: switches blocked beyond a random part, locker after (under 30 switches on every model: not usable) | -0.21 [-0.43, -0.05]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.65 [0.57, 0.73] :: -0.21 [-0.43, -0.05] --> | 0.11 [0.00, 0.40]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.81 [0.71, 0.91] :: 0.11 [0.00, 0.40] --> | -0.30 [-0.44, 0.00]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.80 [0.65, 0.92] :: -0.30 [-0.44, 0.00] --> | 0.12 [0.00, 0.29]<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.53 [0.40, 0.65] :: 0.12 [0.00, 0.29] --> | 0.08 [0.00, 0.23]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: after :: 0.08 [0.00, 0.23] --> |
  | recall: switches blocked beyond a random part, locker first | 0.35 [0.26, 0.43]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.01 [-0.04, 0.07] :: 0.35 [0.26, 0.43] --> | 0.67 [0.58, 0.76]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.14 [0.07, 0.22] :: 0.67 [0.58, 0.76] --> | 0.68 [0.46, 0.88]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| -0.07 [-0.12, -0.02] :: 0.68 [0.46, 0.88] --> | 0.12 [0.04, 0.20]<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.01 [-0.03, 0.07] :: 0.12 [0.04, 0.20] --> | 0.20 [0.10, 0.30]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: before :: 0.20 [0.10, 0.30] --> |
  | recall: switches blocked beyond a random part, locker after | 0.65 [0.57, 0.73]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| -0.21 [-0.43, -0.05] :: 0.65 [0.57, 0.73] --> | 0.81 [0.71, 0.91]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| 0.11 [0.00, 0.40] :: 0.81 [0.71, 0.91] --> | 0.80 [0.65, 0.92]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| -0.30 [-0.44, 0.00] :: 0.80 [0.65, 0.92] --> | 0.53 [0.40, 0.65]<!-- src: results/x0_composition/split-by-order-20261029T005451Z/split.md \| 0.12 [0.00, 0.29] :: 0.53 [0.40, 0.65] --> | 0.41 [0.26, 0.54]<!-- src: results/x0_composition/split-by-order-20261026T173323Z/split.md \| qwen3.5-122b-a10b :: two people swap :: after :: 0.41 [0.26, 0.54] --> |

- **Read.**
  - On every model, Lightning included, the change at the bridge word switches most lookups when the locker sentence came first and few when it came after.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The recall has more blocked switches without the lens part when the locker came after, on every model.

- **Caveats.**
  - Locker after, the whole change switches 0.09 to 0.19 of 99 to 115 lookups, under the 30 switches a cell needs; the lookup's drop there is not usable (the split's own note: measurable only where switches are many).
  - Descriptive: the split was chosen after the data.
  - Post hoc, both orders: the changed prompt's locker sentence matters as well. The table splits the 200 lookups per model by where the original bridge's locker sentence sits and where the changed bridge's sits, relative to the same pick sentence (n: switch rate, 95% interval over bridge entities; the two effects are rate differences averaged over the other order). Both orders matter; the original order's effect is larger on 4 of 5 models (Muse: about equal). The rule fixed for this check (the changed order matters more on at least 3 of 5 models with separate intervals) was not met on any model, so the claim above stands.

  | | original before, changed before | original before, changed after | original after, changed before | original after, changed after | changed order's effect | original order's effect |
  |---|---|---|---|---|---|---|
  | 9B | 75: 0.960 [0.915, 1.000]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 75: 0.960 [0.915, 1.000] --> | 25: 0.560 [0.333, 0.762]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 25: 0.560 [0.333, 0.762] --> | 32: 0.469 [0.333, 0.593]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 32: 0.469 [0.333, 0.593] --> | 68: 0.059 [0.013, 0.128]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 68: 0.059 [0.013, 0.128] --> | 0.405 [0.267, 0.544]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| changed order's effect :: 0.405 [0.267, 0.544] --> | 0.496 [0.374, 0.618]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original order's effect :: 0.496 [0.374, 0.618] --> |
  | 27B | 69: 0.957 [0.911, 1.000]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 69: 0.957 [0.911, 1.000] --> | 32: 0.344 [0.182, 0.517]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 32: 0.344 [0.182, 0.517] --> | 38: 0.210 [0.087, 0.349]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 38: 0.210 [0.087, 0.349] --> | 61: 0.016 [0.000, 0.061]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 61: 0.016 [0.000, 0.061] --> | 0.404 [0.285, 0.515]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| changed order's effect :: 0.404 [0.285, 0.515] --> | 0.537 [0.435, 0.645]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original order's effect :: 0.537 [0.435, 0.645] --> |
  | Muse | 68: 0.809 [0.719, 0.897]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 68: 0.809 [0.719, 0.897] --> | 24: 0.208 [0.062, 0.400]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 24: 0.208 [0.062, 0.400] --> | 39: 0.256 [0.097, 0.390]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 39: 0.256 [0.097, 0.390] --> | 69: 0.000 [0.000, 0.000]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 69: 0.000 [0.000, 0.000] --> | 0.428 [0.301, 0.520]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| changed order's effect :: 0.428 [0.301, 0.520] --> | 0.380 [0.297, 0.491]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original order's effect :: 0.380 [0.297, 0.491] --> |
  | Lightning ○ | 59: 0.983 [0.941, 1.000]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 59: 0.983 [0.941, 1.000] --> | 26: 0.577 [0.385, 0.769]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 26: 0.577 [0.385, 0.769] --> | 36: 0.361 [0.222, 0.500]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 36: 0.361 [0.222, 0.500] --> | 79: 0.051 [0.012, 0.102]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 79: 0.051 [0.012, 0.102] --> | 0.358 [0.235, 0.489]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| changed order's effect :: 0.358 [0.235, 0.489] --> | 0.574 [0.453, 0.681]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original order's effect :: 0.574 [0.453, 0.681] --> |
  | 122B ○ | 53: 0.962 [0.902, 1.000]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 53: 0.962 [0.902, 1.000] --> | 32: 0.781 [0.633, 0.938]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original before :: 32: 0.781 [0.633, 0.938] --> | 33: 0.364 [0.200, 0.565]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 33: 0.364 [0.200, 0.565] --> | 82: 0.012 [0.000, 0.042]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original after :: 82: 0.012 [0.000, 0.042] --> | 0.266 [0.157, 0.375]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| changed order's effect :: 0.266 [0.157, 0.375] --> | 0.684 [0.557, 0.802]<!-- src: results/x0_order_2x2/20261030T224216Z/tables.md \| original order's effect :: 0.684 [0.557, 0.802] --> |

</details>

### When the locker comes after the pick, is the link made in the locker sentences? <a id="t45q"></a>

`in README` `below gate: Lightning` *Used in: README Part IV card "Does the bridge word redirect most lookups when its locker sentence came first, and few when after?" (the copy).*

Test 45q · opened 27 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x45b_binding/x45q-20261027T005345Z/x45q.md` · recompute: `scripts/x45b_binding.py` (the command in its docstring) · also: the copy test, opened 27 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** In clean scenes whose locker sentence comes after the asked pick, does copying the changed prompt's states into the locker sentences switch the lookup, while the change at the bridge word does not?
- **Why we asked.** With the locker after the pick the bridge word cannot point back; the link must be made where the locker sentence is read.
- **Data.** Clean one-pick scenes (only the bridge token differs), locker after the pick: 201<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| qwen35_9b_x45q :: 201 / 0 / 201 / 201 :: 201 --> / 288<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| x45q_27b :: 288 / 0 / 288 / 288 :: 288 --> / 205<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| muse30b_x45q :: 205 / 0 / 205 / 205 :: 205 --> (9B / 27B / Muse). Lightning not tested: the clean one-pick design's gate fails on it.
- **Method.** On the original prompt: (a) the change at the bridge word at L; (c) the changed prompt's states copied into every locker-sentence token at L; (d) the same at L/2; each read as a share of the lookups the changed prompt itself switches.

![Locker after the pick: the link is made in the locker sentences](../../figures/depth/readme/06_link_layers.png)

*With the locker sentence after the pick, by layer (x: the layer as a share of the model's depth): the lookups switched by the change at the bridge word and by the same change copied into the locker sentences, each line named at its end; dots: the cells fixed in advance, with their values; shading 95% intervals; the layer sweeps after the data (post hoc); the 9B, 27B and Muse.*

- **Rule, fixed in advance.** ""the link is made in the locker sentences" if (c) or (d) switches at least half of the lookups S switches while (a) stays at or below 0.25, on at least 2 of 3 models."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (a) lookups switched by the change at the bridge word at L (bar <= 0.25) | 0.17 [0.12, 0.22]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| qwen35_9b_x45q :: 0.17 [0.12, 0.22] --> | 0.01 [0.00, 0.03]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| x45q_27b :: 0.01 [0.00, 0.03] --> | 0.01 [0.00, 0.03]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| muse30b_x45q :: 0.01 [0.00, 0.03] --> | ○ 0.10 [0.06, 0.15]<!-- src: results/x45b_binding/x52_45q_below-20261029T085135Z/x45q.md \| nem35l_x52_45q_below :: 0.10 [0.06, 0.15] --> | not run |
  | (c) the changed states copied into the locker sentences at L, share of S's switches (bar >= 0.5) | 0.70 [0.65, 0.74]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| qwen35_9b_x45q :: 0.70 [0.65, 0.74] --> | 0.74 [0.68, 0.80]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| x45q_27b :: 0.74 [0.68, 0.80] --> | 0.76 [0.70, 0.81]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| muse30b_x45q :: 0.76 [0.70, 0.81] --> | ○ 0.75 [0.69, 0.81]<!-- src: results/x45b_binding/x52_45q_below-20261029T085135Z/x45q.md \| nem35l_x52_45q_below :: 0.75 [0.69, 0.81] --> | |
  | (d) the same at L/2 | 0.07 [0.05, 0.10]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| qwen35_9b_x45q :: 0.07 [0.05, 0.10] --> | 0.05 [0.02, 0.09]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| x45q_27b :: 0.05 [0.02, 0.09] --> | 0.47 [0.41, 0.53]<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| muse30b_x45q :: 0.47 [0.41, 0.53] --> | ○ 0.12 [0.07, 0.18]<!-- src: results/x45b_binding/x52_45q_below-20261029T085135Z/x45q.md \| nem35l_x52_45q_below :: 0.12 [0.07, 0.18] --> | |
  | holds | **yes<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| qwen35_9b_x45q :: tested (holds) :: yes -->** | **yes<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| x45q_27b :: tested (holds) :: yes -->** | **yes<!-- src: results/x45b_binding/x45q-20261027T005345Z/x45q.md \| muse30b_x45q :: tested (holds) :: yes -->** | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80); below gate, descriptive only: yes (163<!-- src: results/x45b_binding/x52_45q_below-20261029T085135Z/x45q.md \| nem35l_x52_45q_below :: 163 / 0 / 163 / 163 :: 163 --> locker-after items) | |

- **Read.**
  - With the locker after the pick, copying the changed states into the locker sentences at L carries about three quarters of the lookup's switches on all three models, while the change at the bridge word carries almost none: the link is made in the locker sentences.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning: below the clean one-pick gate, so not tested; the below-gate run (eligible items only) is exploratory, hollow ○, never in claims or grades.
  - At L/2 the copy carries little on the 9B and 27B and about half on Muse.
  - Clean scenes only; the main test's locker-after lookups are in the order-split card.

</details>

### Which token and layer carry each reader's switch, and when does the bridge word stop being read? <a id="d1"></a>

`in README` `below gate: Lightning` *Used in: README Part IV card "Which token and layer carry the lookup when the locker sentence comes after the pick?".*

Test D1 / D2 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md` · recompute: `scripts/x47_depthmap.py` (the command in its docstring) · also: token-by-layer map and window patching; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** With the changed prompt's state placed in one token group at one layer, which cell switches each reader, and after which layer does nothing downstream read the bridge word?
- **Why we asked.** With the locker sentence after the pick the bridge word cannot point back; the map says where the link sits instead.
- **Data.** Clean one-pick scenes (the main test beside them), split by sentence order: locker first 151 / 202 / 143, locker after 166 / 236 / 170 (9B / 27B / Muse). Lightning: the main test only, locker first 59<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-first :: 59 -->, locker after 79<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-after :: 79 -->; its clean design is not tested (the clean one-pick gate fails on it).
- **Method.** D1: the changed state placed at one token group (the bridge word, the rest of the pick sentence, the asked person, each locker sentence's item and number, the question, the last token) at one layer, every 2nd (9B) or 4th (27B, Muse). D2: the changed state at the bridge word at every layer from l on; the read-out layer l_R is the first where this switches 0.1 or fewer.

*No figure: the token-by-layer heat strips are supplementary (figure); the table has the rule's numbers.*

- **Rule, fixed in advance.** D1: "(a) In locker-after scenes the lookup's mass sits at the locker sentences, not at the bridge word, at every layer (bridge-word cells <= 0.25 everywhere; some locker-sentence cell >= 0.5). (b) In locker-first scenes the lookup's bridge-word mass ends before the recall's does (the last layer with bridge-word switch >= 0.3 is earlier for the lookup, by >= 2 layers on the 9B, >= 4 on Muse). (c) The recall's map has a second hot token, the item's earlier mention, in locker-first scenes (>= 0.3 at some layer), absent in locker-after." D2: ""The handover from the mention to the question" if l_R(recall) lies at or below the start of his late band on the 9B and 27B." The 27B and Lightning: coverage runs on these rules, no prediction.

</details>

- **Result.** (clean design; the main test gives the same D1 and D2 answers on the 9B, 27B and Muse; Lightning: the main test)

  | | 9B | 27B | Muse | Lightning (main; ○ clean, below gate) | 122B |
  |---|---|---|---|---|---|
  | D1 (a) locker after: a locker-sentence cell carries the lookup | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: glk_org_num@18 :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: glk_cf_item@28 :: no --> | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: glk_cf_item@16 :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: glk_cf_item@12 :: no -->; ○ clean: no<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| nemotron-3.5-lightning :: clean :: no (bridge max :: no --> | not run |
  | D1 (b) locker first: the lookup leaves the bridge word first | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: lead -2 of 2 :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: lead -4 of 4 :: no --> | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: lead 0 of 4 :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: lead 0 of 4 :: no -->; ○ clean: no<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| nemotron-3.5-lightning :: clean :: no (lookup last 24 :: no --> | |
  | D1 (c) the recall's second hot token, locker first only | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: peaks first :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: peaks first :: no --> | no<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: peaks first :: no --> | no<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: peaks first 0.0169 :: no -->; ○ clean: no<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| nemotron-3.5-lightning :: clean :: no (peaks first :: no --> | |
  | read-out layer l_R, lookup / recall, locker first | L18<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: locker-first :: 151 :: 18 --> / L20<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: locker-first :: 151 :: 20 --> | L44<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: locker-first :: 202 :: 44 --> / L40<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: locker-first :: 202 :: 40 --> | L32<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: locker-first :: 143 :: 32 --> / L32<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: locker-first :: 143 :: 32 --> | L28<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-first :: 59 :: 28 --> / L28<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-first :: 59 :: 28 -->; ○ clean: L28<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| clean :: locker-first :: 28 --> / L28<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| clean :: locker-first :: 28 --> | |
  | read-out layer l_R, lookup / recall, locker after | L12<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: locker-after :: 166 :: 12 --> / L24<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: locker-after :: 166 :: 24 --> | L28<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: locker-after :: 236 :: 28 --> / L52<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: locker-after :: 236 :: 52 --> | L16<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: locker-after :: 170 :: 16 --> / L36<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: locker-after :: 170 :: 36 --> | L12<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-after :: 79 :: 12 --> / L36<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: locker-after :: 79 :: 36 -->; ○ clean: L12<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| clean :: locker-after :: 12 --> / L36<!-- src: results/x47_depthmap/x52_depthmap_below-20261029T092524Z/depth.md \| clean :: locker-after :: 36 --> | |
  | D2: the recall's read-out layer at or below the start of the breadth track's late band | yes<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| qwen3.5-9b :: clean :: l_R recall 24, band 26 :: yes --> (band from L26) | yes<!-- src: results/x47_depthmap/x52_depthmap-20261029T010426Z/depth.md \| qwen3.6-27b :: clean :: l_R recall 52, band 52 :: yes --> (band from L52) | not designed: band None<!-- src: results/x47_depthmap/depth-20261028T120525Z/depth.md \| muse-glimmer-30b :: clean :: band None --> | not designed: band None<!-- src: results/x47_depthmap/x52_depthmap-20261029T011452Z/depth.md \| nemotron-3.5-lightning :: main :: l_R recall 36, band None :: band None -->; ○ clean: no band (l_R recall L36) | |

- **Read.**
  - On the 27B as on the 9B and Muse, all three D1 readings fail on both designs (Lightning: on the main test): no locker-sentence cell carries the locker-after lookup, the lookup does not leave the bridge word before the recall by the margin fixed in advance, and the recall has no second hot token.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - With the locker after the pick, the lookup stops reading the bridge word far earlier than the recall on all four; the 27B's recall reads it up to the start of the breadth track's late band, as on the 9B.

- **Caveats.**
  - Lightning's clean design is below its gate (recall 0.751 < 0.80): its ○ entries are exploratory, never in claims or grades.
  - The 27B, Muse and Lightning were sampled every 4th layer, so their read-out layers are known to 4 layers; Lightning's in-job verdict crashed on a missing margin for rule (b), added after the run (Flagged 19).
  - Muse and Lightning have no late band in the breadth track, so D2 is scored on the 9B and 27B only.

</details>

### When the change at L misses a lookup, where is the rest read? <a id="t47-4"></a>

`in README` `below gate: Lightning` *Used in: README Part IV card "Which token and layer carry the lookup when the locker sentence comes after the pick?" (the cumulative patches).*

Test 47.4 · opened not stated · status: descriptive · hand-check: not in sample · files: `results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md` · recompute: `scripts/x47_cumulative.py` (the command in its docstring) · also: cumulative patches; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the change at the bridge word at L leaves a lookup unswitched, is the rest read from the bridge word before L, from the pick sentence's other tokens, or from outside the pick sentence?
- **Why we asked.** The conflict test changes one layer; the lookups it misses may read the bridge word earlier.
- **Data.** The main test and clean one-pick scenes, by sentence order: locker first 75 / 69 / 68 (main) and 151 / 202 / 143 (clean), locker after 68 / 61 / 69 (main) (9B / 27B / Muse). Lightning, main design: locker first 59<!-- src: results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md \| nemotron-3.5-lightning :: main :: lookup :: locker-first :: 59 -->, locker after 79<!-- src: results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md \| nemotron-3.5-lightning :: main :: lookup :: locker-after :: 79 -->; its clean design not tested (gate).
- **Method.** Four arms on the original prompt: (a) the change at the bridge word at L; (b) the bridge word replaced at every layer up to L; (c) at every layer; (d) the whole asked pick sentence at every layer. The lookups (a) leaves unswitched split into before L (b minus a), the pick sentence's other tokens (d minus c) and outside the pick sentence (1 minus d).

![Lookups the change misses are read at the bridge word before L](../../figures/depth/readme/s07_cumulative.png)

*Claim 11: where each reader's switches under the change are carried, as shares of the switches (a term may be negative): the bridge word at L, the bridge word before L, every layer after L, the pick sentence's other tokens, and outside the pick sentence; lookup violet, recall black; the main test and the clean one-pick scenes; whiskers 95% intervals; Lightning hollow ○, its clean one-pick scenes below gate. The split by sentence order behind claim 11 is in the key numbers per claim and in the ledger card.*

- **Rule, fixed in advance.** None: descriptive, no bar; the verdict reads which part is largest in locker-first scenes. The 27B and Lightning: coverage runs, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | locker first: lookups the change at L leaves unswitched (main) | 0.04 [0.00, 0.09]<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| qwen3.5-9b :: main :: 75 :: 0.04 [0.00, 0.09] --> | 0.04 [0.00, 0.09]<!-- src: results/x47_cumulative/x52_cumulative-20261029T023427Z/x47_4.md \| qwen3.6-27b :: main :: 69 :: 0.04 [0.00, 0.09] --> | 0.19 [0.10, 0.28]<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| muse-glimmer-30b :: main :: 68 :: 0.19 [0.10, 0.28] --> | 0.02 [0.00, 0.06]<!-- src: results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md \| nemotron-3.5-lightning :: main :: 59 :: 0.02 [0.00, 0.06] --> | 0.04 [0.00, 0.10]<!-- src: results/x47_cumulative/x52_cumulative-20261030T010712Z/x47_4.md \| qwen3.5-122b-a10b :: main :: 53 :: 0.04 [0.00, 0.10] --> |
  | locker first: where most of that rest is read, main / clean | outside<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| qwen3.5-9b :: main :: 75 :: outside --> / before_L<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| qwen3.5-9b :: clean :: 151 :: before_L --> | outside<!-- src: results/x47_cumulative/x52_cumulative-20261029T023427Z/x47_4.md \| qwen3.6-27b :: main :: 69 :: outside --> / before_L<!-- src: results/x47_cumulative/x52_cumulative-20261029T023427Z/x47_4.md \| qwen3.6-27b :: clean :: 202 :: before_L --> | before_L<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| muse-glimmer-30b :: main :: 68 :: before_L --> / before_L<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| muse-glimmer-30b :: clean :: 143 :: before_L --> | outside<!-- src: results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md \| nemotron-3.5-lightning :: main :: 59 :: outside --> / ○ before_L<!-- src: results/x47_cumulative/x52_cumulative_below-20261029T085952Z/x47_4.md \| clean :: 89 :: before_L --> | outside<!-- src: results/x47_cumulative/x52_cumulative-20261030T010712Z/x47_4.md \| qwen3.5-122b-a10b :: main :: 53 :: outside --> / before_L<!-- src: results/x47_cumulative/x52_cumulative-20261030T010712Z/x47_4.md \| qwen3.5-122b-a10b :: clean :: 134 :: before_L --> |
  | locker after: lookups carried by the bridge word before L (main) | 0.93 [0.85, 0.98]<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| qwen3.5-9b :: main :: lookup :: locker-after :: 68 :: 0.93 [0.85, 0.98] --> | 1.00 [1.00, 1.00]<!-- src: results/x47_cumulative/x52_cumulative-20261029T023427Z/x47_4.md \| qwen3.6-27b :: main :: lookup :: locker-after :: 61 :: 1.00 [1.00, 1.00] --> | 0.99 [0.95, 1.00]<!-- src: results/x47_cumulative/x47_4-20261028T113105Z/x47_4.md \| muse-glimmer-30b :: main :: lookup :: locker-after :: 69 :: 0.99 [0.95, 1.00] --> | 0.92 [0.86, 0.98]<!-- src: results/x47_cumulative/x52_cumulative-20261029T044453Z/x47_4.md \| nemotron-3.5-lightning :: main :: lookup :: locker-after :: 0.92 [0.86, 0.98] --> | 1.00 [1.00, 1.00]<!-- src: results/x47_cumulative/x52_cumulative-20261030T010712Z/x47_4.md \| qwen3.5-122b-a10b :: main :: lookup :: locker-after :: 82 :: 1.00 [1.00, 1.00] --> |

- **Read.**
  - With the locker first the change at L misses few lookups on every model, the 27B included; with the locker after, almost all lookups are carried by the bridge word before L, on the 27B and Lightning too.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  Lightning's clean design is below its gate (recall 0.751 < 0.80), so it is not tested there; the below-gate run (exploratory, hollow ○) finds the rest read mostly at the bridge word before L in locker-first scenes, and, with the locker after the pick, the bridge word before L carries the lookup on ○ 0.94 [0.89, 0.98]<!-- src: results/x47_cumulative/x52_cumulative_below-20261029T085952Z/x47_4.md | lookup :: locker-after :: 0.94 [0.89, 0.98] --> of scenes.

- **Caveats.**
  - Lightning's clean-design numbers are below gate, exploratory: never in claims or grades.
  - Descriptive: no rule fixed in advance.
  - In the main test the rest of a locker-first miss sits outside the pick sentence on the 9B, 27B and Lightning (the other person's pick also changes there); in clean scenes it is before L on all three.

</details>

### Does the lookup drop the lens part before it takes up the address? <a id="t47-8"></a>

`in README` *Used in: README Part IV card "Does the lookup drop the lens part before it takes up the address?".*

Test 47.8 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md` · recompute: `scripts/x47_anatomy.py` (the command in its docstring) · also: anatomy by layer; Lightning's coverage run and the 27B's full grid 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Layer by layer, when does the lookup stop needing the lens part, when does it start using the address, when is the address readable, and is the value ever used?

![The address is readable before the lookup uses it](../../figures/depth/readme/07_depth.png)

*By depth (x: the layer as a share of the model's depth), on the three models whose gates were fixed in advance: the locker probe's accuracy and the position answers under the whole change when another item moves (orange, named at their ends), and the lookup's switches blocked without the lens part beyond a random part of the same size (teal); shading 95% intervals; grey band: the layers that pass the gate. The 9B in its own block: its interval runs below zero outside its gate.*

![The address is readable before the lookup uses it](../../figures/depth/readme/08_depth_more.png)

*As the figure above, on Lightning and the 122B, whose gates were chosen after the data (all estimates post hoc); Lightning in its own block: its interval runs far below zero outside its gate.*


- **Why we asked.** At L the lookup takes an identity route and a position route; depth says which comes first and whether the address is written before it is read.

- **Data.** Routes scenes (another item moved), locker first, the test half: 200 per model (27B 150, on its full grid: every 4th layer); the fit half for the per-layer refits and probes.

- **Method.** At each sampled layer, the whole change and its parts (the lens part; the address part refit at that layer; the identity outside the lens), each added alone or taken out, against random parts of the same share; a slot probe at the bridge word. A layer counts only where the whole change switches 0.30 or more. D4: the angles between the address subspaces (and the identity subspaces) refit at every pair of layers in the probe's window.

- **Rule, fixed in advance.** "Define l_J = the first layer from which the lookup's extra drop without J++ stays <= 0.10; l_P = the first layer where the position share under the whole change is >= 0.20; l_probe = the first layer where the slot probe is >= 0.80. (a) "Handoff": l_P >= l_J [...] (b) "The address forms before it is used": l_probe <= l_P on every model [...] (c) "Identity leaves the lens": identity share with only-J++ is >= 0.5 at the earliest interpretable layer and <= 0.1 by L, while identity with only-I_l rises to >= 0.3 by L, on >= 2 of 3 models [...] (d) "Never the value, at any depth": value <= 0.05 at every interpretable layer." D4: "persistent if the mean cos^2 of the principal angles >= 0.5 across the window where the slot probe is >= 0.8; re-encoded if it drops below 0.2 between adjacent sampled layers." The 27B's full grid and Lightning: coverage runs on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | l_J: the lookup no longer needs the lens part | L12<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: 0 (<= 2) :: 12 --> | L40<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: -12 (<= 2) :: 40 --> | L2<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: 20 (> 6) :: 2 --> | L14<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: 0 (<= 2) :: 14 --> | L33<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| qwen3.5-122b-a10b :: yes (max 0.00) :: 33 --> ○ |
  | l_P: position answers begin | L12<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: 0 (<= 2) :: 12 --> | L28<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: -12 (<= 2) :: 28 --> | L22<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: 20 (> 6) :: 22 --> | L14<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: 0 (<= 2) :: 14 --> | L33 ○ |
  | l_probe: the address is readable | L4<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: 0 (<= 2) :: 4 --> | L8<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: -12 (<= 2) :: 8 --> | L6<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: 20 (> 6) :: 6 --> | L6<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: 0 (<= 2) :: 6 --> | L13<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| qwen3.5-122b-a10b :: 0 (<= 2) :: 13 --> ○ |
  | (a) handoff, l_P >= l_J (gap) | yes, gap 0 (<= 2)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| (a) qwen3.5-9b :: yes, gap 0 (<= 2) --> | no, gap -12 (<= 2)<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| Q47.8 :: no, gap -12 (<= 2) --> (full grid) | yes, gap 20 (> 6)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| Q47.8 :: yes, gap 20 (> 6) --> | yes, gap 0 (<= 2)<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| Q47.8 :: yes, gap 0 (<= 2) --> (no prediction) | yes, gap 0 (<= 2)<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| (a) qwen3.5-122b-a10b :: yes, gap 0 (<= 2) --> (no prediction; lookup-only gate) |
  | (b) the address readable before it is used | yes<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: (cross :: yes --> | yes<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: (cross :: yes --> | yes<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: (cross :: yes --> | yes<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: (cross :: yes --> | yes |
  | (c) identity leaves the lens (crossing layer) | no (cross 12)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: no (cross 12) :: no (cross 12) --> | no (cross 4)<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: no (cross 4) :: no (cross 4) --> | no (cross 2)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: no (cross 2) :: no (cross 2) --> | no (cross 2)<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: no (cross 2) :: no (cross 2) --> | no (cross 1)<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| qwen3.5-122b-a10b :: no (cross 1) --> |
  | (d) never the value | yes (max 0.00)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: yes (max 0.00) :: yes (max 0.00) --> | yes (max 0.00)<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: yes (max 0.00) :: yes (max 0.00) --> | yes (max 0.00)<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: yes (max 0.00) :: yes (max 0.00) --> | yes (max 0.00)<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: yes (max 0.00) :: yes (max 0.00) --> | yes (max 0.00)<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| qwen3.5-122b-a10b :: yes (max 0.00) --> |
  | the recall switches 0.5 or more (window) | L2-L14<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| qwen3.5-9b :: L2-L14 :: L2-L14 --> | L4-L32<!-- src: results/x47_anatomy/x52_anatomy-20261029T013405Z/x47_8.md \| qwen3.6-27b :: L4-L32 :: L4-L32 --> | L2-L22<!-- src: results/x47_anatomy/x47_8-20261028T154518Z/x47_8.md \| muse-glimmer-30b :: L2-L22 :: L2-L22 --> | L2-L22<!-- src: results/x47_anatomy/x52_anatomy-20261029T010517Z/x47_8.md \| nemotron-3.5-lightning :: L2-L22 :: L2-L22 --> | L1-L33<!-- src: results/x47_anatomy/x52_anatomy-20261030T032402Z/x47_8.md \| qwen3.5-122b-a10b :: L1-L33 --> |
  | D4: the address code across depth, mean cos^2 (label) | 0.279<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| qwen3.5-9b :: U :: 0.279 -->, re-encoded<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| qwen3.5-9b :: U :: 0.279 :: re-encoded --> | 0.256<!-- src: results/x47_depth_cpu/persistence-20261029T013614Z/persistence.md \| qwen3.6-27b :: U :: 0.256 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261029T013614Z/persistence.md \| qwen3.6-27b :: U :: 0.256 :: mixed --> | 0.213<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| muse-glimmer-30b :: U :: 0.213 -->, re-encoded<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| muse-glimmer-30b :: U :: 0.213 :: re-encoded --> | 0.341<!-- src: results/x47_depth_cpu/persistence-20261029T015607Z/persistence.md \| nemotron-3.5-lightning :: U :: 0.341 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261029T015607Z/persistence.md \| nemotron-3.5-lightning :: U :: 0.341 :: mixed --> | |
  | D4: the identity code across depth, mean cos^2 (label) | 0.432<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| qwen3.5-9b :: Id :: 0.432 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| qwen3.5-9b :: Id :: 0.432 :: mixed --> | 0.386<!-- src: results/x47_depth_cpu/persistence-20261029T013614Z/persistence.md \| qwen3.6-27b :: Id :: 0.386 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261029T013614Z/persistence.md \| qwen3.6-27b :: Id :: 0.386 :: mixed --> | 0.365<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| muse-glimmer-30b :: Id :: 0.365 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261028T115530Z/persistence.md \| muse-glimmer-30b :: Id :: 0.365 :: mixed --> | 0.419<!-- src: results/x47_depth_cpu/persistence-20261029T015607Z/persistence.md \| nemotron-3.5-lightning :: Id :: 0.419 -->, mixed<!-- src: results/x47_depth_cpu/persistence-20261029T015607Z/persistence.md \| nemotron-3.5-lightning :: Id :: 0.419 :: mixed --> | |

- **Read.**
  - On the 9B, Muse and Lightning the lookup stops needing the lens part no later than position answers begin; on the 27B's full grid it still needs it after they begin, so (a) fails there. On all four the address is readable before position answers begin and the value is never used; (c) fails on every model.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Lightning's handoff and first position answers fall at L14 (L), as on the 9B. The address code does not persist across depth on any of the four (re-encoded on the 9B and Muse, mixed on the 27B and Lightning).

- **Caveats.**
  - The 27B's column is its full grid. The reduced grid behind README E12 (9 layers) gave l_J L16, l_P L30, (a) yes; l_J needs the effect to stay under the bar at every later sampled layer, and the full grid samples L36, which the reduced grid skipped (Flagged, top).
  - Each layer's address part and probe are refit on the fit half; early-layer refits read less well (the verdicts give their held-out accuracy).

</details>

### Does the address travel to the last token? <a id="t51-4"></a>

`in README` *Used in: README claims table, claim 12 (whether the address travels to the last token).*

Test 51.4 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_travel/x52_travel-20261029T012517Z/verdict.md` · recompute: `scripts/x51_travel.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Does the address swap work at the last token, with the bridge word's slot means or with means refit there?
- **Why we asked.** The answer is read at the last token; the address could be copied there or re-encoded.
- **Data.** Routes scenes without a move, 300 per model (read half 145 / 150 / 144 / 132<!-- src: results/x51_travel/x52_travel-20261029T012517Z/verdict.md \| nem35l_x52_travel :: 300 (132) :: 132 -->; Lightning at L14 and L18).
- **Method.** The address swap added at the last token at L and L+4, at doses 1 and 2, with the bridge word's means and with last-token means; each against a random vector of its norm; a slot probe at the last token beside.

- **Rule, fixed in advance.** "The code travels: the bridge-fit swap sends >= 0.3 of lookups to slot k (random <= 0.05). Re-encoded on copy: bridge-fit <= 0.10 while last-token-fit >= 0.3. Not at the last token: both <= 0.10 while the probe reads the slot there >= 0.8. Otherwise in between." Lightning: a coverage run on this rule, no prediction.

The swap at the last token, per model:

![The bridge word's code works at the last token only on Muse](../../figures/depth/ledger/11_last_token_swap.png)

*The address fit at the bridge word swapped in at the last token, a few layers after L at twice a real change's size: the share of lookups sent to the target item, per model. Whiskers 95% intervals; Lightning hollow ○ (a coverage run).*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | bridge-fit swap at L+4, dose 2: lookups sent to the target | 0.00 [0.00, 0.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| bridge_swap :: 1.00 [1.00, 1.00] :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.01]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| 0.99 [0.99, 1.00] :: 0.00 [0.00, 0.01] --> | 0.45 [0.43, 0.48]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| bridge_swap :: 0.45 [0.43, 0.48] --> | 0.00 [0.00, 0.00]<!-- src: results/x51_travel/x52_travel-20261029T012517Z/verdict.md \| bridge_swap :: L+4 :: 600 :: 1.00 [1.00, 1.00] :: 0.00 [0.00, 0.00] --> | not run |
  | slot probe at the last token, L / L+4 | 0.55 [0.50, 0.61]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| qwen35_9b_x51_4 :: 0.55 [0.50, 0.61] --> / 0.93 [0.89, 0.96]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| qwen35_9b_x51_4 :: 0.93 [0.89, 0.96] --> | 0.85 [0.80, 0.89]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| x51_4_27b :: 0.85 [0.80, 0.89] --> / 1.00 [1.00, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| x51_4_27b :: 1.00 [1.00, 1.00] --> | 0.99 [0.97, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| muse30_x51_4 :: 0.99 [0.97, 1.00] --> / 0.99 [0.98, 1.00]<!-- src: results/x51_travel/x51_4-20261028T173333Z/verdict.md \| muse30_x51_4 :: 0.99 [0.98, 1.00] --> | 0.28 [0.24, 0.33]<!-- src: results/x51_travel/x52_travel-20261029T012517Z/verdict.md \| nem35l_x52_travel :: 0.28 [0.24, 0.33] --> / 0.31 [0.27, 0.35]<!-- src: results/x51_travel/x52_travel-20261029T012517Z/verdict.md \| nem35l_x52_travel :: 0.31 [0.27, 0.35] --> | |
  | the rule | **not at the last token** | **not at the last token** | **the code travels** | **(d) in between<!-- src: results/x51_travel/x52_travel-20261029T012517Z/verdict.md \| nem35l_x52_travel :: (d) in between -->**, at L14 and L18 (no prediction) | |

- **Read.**
  - On the 9B and 27B the slot is readable at the last token but the bridge word's code does not work there; on Muse it does.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - On Lightning the slot is not yet readable at the last token at L and L+4 (the probe sits near the majority slot) and the swap moves nothing there, so the rule says in between; the probe reads the slot only after L+4.

- **Caveats.**
  - "Not at the last token" means not usable there by this swap, not absent: the probe reads the slot there.
  - Doses 1 and 2 only.

</details>

### Is the recall's bridge entity read through the lens at the last token? <a id="t51-10"></a>

`in README` *Used in: README Part IV card "At the last token, is the bridge entity in the lens part of the state, and does the model use it there?".*

Test 51.10 · opened 28 Oct · status: rule fixed in advance · hand-check: in sample (view f) · files: `results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md` · recompute: `scripts/x51_jread.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At the last token and at the question's pick token, is the bridge entity readable through the lens, and does writing it through the lens move the answer?
- **Why we asked.** The bridge word's lens part is followed by the recall; the answer is computed later, at the last token.
- **Data.** Main test, the scenes whose locker sentences come first: 75 / 69 / 68 / 59<!-- src: results/x51_jread/x52_jread-20261029T005707Z/verdict.md \| n = 59 locker-first :: 59 --> (9B / 27B / Muse / Lightning; Lightning at L14, a coverage run on the same rule, no prediction).
- **Method.** Read: a probe on the lens part of the state, layer by layer, against the full state and chance. Write: at the read peak, the breadth track's swap or the lens part of the change (gain up to 2), against a random part and his rotated control; the whole-state patch as reference.

![At the last token the entity is in the lens, but the answer is not computed through it](../../figures/common/readme/12_last_token.png)

*Per model, at the layer where the read peaks (under the name). Left: a probe's accuracy for the recall's entity on the lens part of the last token's state, with its 95% interval; dashed: chance. Right: the recalls switched when only the lens part is swapped in (teal) against the whole state swapped in (grey); the lens part's value in the last column. Lightning hollow (○, post hoc).*

- **Rule, fixed in advance.** "read: through-the-lens probe >= 0.8 and lens top-5 >= 0.5 at some layer before the answer digit's layer, while the full-residual probe >= 0.9 there. write: at the layer of the read peak, his swap or the J++ part of the change (gain <= 2) switches >= 0.5 of what the whole-state patch switches at that layer, with the random part <= 0.10."

</details>

- **Result.** (recall, last token)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | read peak layer (answer layer) | L24 (L29) | L56 (L61) | L40 (L46) | L36<!-- src: results/x51_jread/x52_jread-20261029T005707Z/verdict.md \| recall :: answer L49 :: 36 --> (L49<!-- src: results/x51_jread/x52_jread-20261029T005707Z/verdict.md \| recall :: answer L49 :: L36: 0.14 / 0.97 :: 49 -->) | 44<!-- src: results/x51_jread/x53_jread-20261029T140044Z/verdict.md \| recall :: answer L46 :: 44 --> (answer L46) |
  | through-the-lens probe at the peak | 0.97 [0.94, 0.99]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.87 :: 0.97 [0.94, 0.99] --> | 0.95 [0.89, 0.99]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.80 :: 0.95 [0.89, 0.99] --> | 0.95 [0.91, 0.98]<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| 0.73 :: 0.95 [0.91, 0.98] --> | 0.98 [0.96, 1.00]<!-- src: results/x51_jread/x52_jread-20261029T005707Z/verdict.md \| 0.82 :: 0.98 [0.96, 1.00] --> | 0.91 [0.81, 0.96]<!-- src: results/x51_jread/x53_jread-20261029T140044Z/verdict.md \| 0.32 :: 0.91 [0.81, 0.96] --> |
  | swap / whole-state patch, switches | 0.00 / 0.95<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L24: 0.00 / 0.95 :: 0.00 / 0.95 --> | 0.01 / 0.97<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L56: 0.01 / 0.97 :: 0.01 / 0.97 --> | 0.01 / 1.00<!-- src: results/x51_jread/x51_10-20261028T190608Z/verdict.md \| L40: 0.01 / 1.00 :: 0.01 / 1.00 --> | 0.14 / 0.97<!-- src: results/x51_jread/x52_jread-20261029T005707Z/verdict.md \| L36: 0.14 / 0.97 :: 0.14 / 0.97 --> | 0.00 / 0.79<!-- src: results/x51_jread/x53_jread-20261029T140044Z/verdict.md \| L44: 0.00 / 0.79 :: 0.00 / 0.79 --> |
  | the rule (recall, last token) | **readable, not used** | **readable, not used** | **readable, not used** | **readable, not used** (no prediction) | **(b) readable, not used<!-- src: results/x51_jread/x53_jread-20261029T140044Z/verdict.md \| qwen3.5-122b-a10b :: recall :: (b) readable, not used -->** (no prediction) |

- **Read.**
  - At the last token the recall's bridge entity is readable through the lens on all four models, Lightning included, but writing it through the lens does not switch it to the swapped-in entity's answer.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  What the model outputs under the writes at the last token (a CPU check after the data, descriptive; results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md): the recall never outputs the bridge entity's name or a number word, on any of the four models. Under the lens swap its original answer stays unchanged on 0.95<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | swap | 75 |  :: 0.95 --> / 0.97<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | swap | 69 |  :: 0.97 --> / 0.94<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | swap | 68 |  :: 0.94 --> / 0.78<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | swap | 59 |  :: 0.78 --> of items (9B / 27B / Muse / Lightning); the lens part of the change at gain 2 gives the changed prompt's answer on 0.15<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | jpp2 | 75 | 0.65 :: 0.15 --> / 0.03<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | jpp2 | 69 | 0.91 :: 0.03 --> / 0.38<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | jpp2 | 68 | 0.38 :: 0.38 --> / 0.56<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | jpp2 | 59 | 0.15 :: 0.56 -->, a random part at the same gain on 0.04<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | rand2 | 75 | 0.84 :: 0.04 --> / 0.03<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | rand2 | 69 | 0.93 :: 0.03 --> / 0.04<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | rand2 | 68 | 0.90 :: 0.04 --> / 0.19<!-- src: results/x51_jread/x52_lenswrite-20261029T080535Z/lenswrite.md | recall | rand2 | 59 | 0.61 :: 0.19 -->.

- **Caveats.**
  - The lookup's cells: routes around J-space (9B) or none of the four (27B, Muse, Lightning); the question's pick token: not represented or none of the four on almost every cell.
  - Locker-first scenes only.

</details>

### At the last token, does each reader compute its answer through the lens part or outside it? <a id="b53-3"></a>

`in README` *Used in: README "Tested and dropped" ("The copy bypasses the lens"), the reading dropped (its link goes to 53.3b).*

Test 53.3 · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md` · recompute: `scripts/x53_lastconflict.py` (the command in its docstring) · also: four models

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At the last token, does each reader compute its answer through the lens part of the last token's change, or outside it?


- **Why we asked.** At the last token the recall's bridge entity is readable through the lens, yet writing it there does not switch it to the swapped-in entity's answer ([51.10](#t51-10)); the conflict test at that token asks which part of the change each reader follows there.

- **Data.** Main test, the locker-first scenes of 51.10: 75 / 69 / 68 / 59 (9B / 27B / Muse / Lightning; 32 / 34 / 29 / 30 bridge entities).

- **Method.** The change at the last token (the changed prompt's last-token state minus the original's) at 51.10's read-peak layer and two layers before the answer layer, per reader; the lens part = its 25 J++ directions; arms: the whole change, without the lens part, without a random part of the same share, the lens part alone, the rest alone.

- **Rule, fixed in advance.** "Rule per reader: "computes outside the lens at the last token" if the effect without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the effect is >= 0.30 beyond random; else in between." (jobs/c3/batch53.yaml, Dan 29 Oct 09:30; no prediction)


Both readers at the last token:

![At the read peak no lookup goes through the lens part](../../figures/depth/ledger/12_last_conflict.png)

*The conflict test at the last token: the switches blocked without the lens part beyond a random part, lookup (left) and recall (right), at the two layers tested for each reader (its own layers, earlier first; the 122B at one). Whiskers 95% intervals; Lightning and the 122B hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup at the read peak (L24 / L60 / L32 / L32): blocked beyond a random part / the rest alone over the whole | 0.12 [0.00, 0.23]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: 0.12 [0.00, 0.23] --> / 0.35 [0.19, 0.52]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: 0.35 [0.19, 0.52] --> | 0.13 [0.03, 0.25]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.13 [0.03, 0.25] --> / 0.19 [0.07, 0.33]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.19 [0.07, 0.33] --> | 0.00 [0.00, 0.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: 0.00 [0.00, 0.00] --> / 1.00 [1.00, 1.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: 1.00 [1.00, 1.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: 0.00 [0.00, 0.00] --> / 0.98 [0.95, 1.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: 0.98 [0.95, 1.00] --> | not tested (L12: the whole change switches no item<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T140437Z/verdict.md \| qwen3.5-122b-a10b :: lookup :: 12 (read peak) :: the whole change switches no item -->) |
  | lookup two layers before the answer (L27 / L59 / L33 / L43): the same (the 9B's and the 27B's descriptive, uninformative near the output (dictionary); Muse's and Lightning's keep their labels) | 0.16 [0.08, 0.26]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 27 (answer L29 - 2) :: 0.16 [0.08, 0.26] --> / 0.16 [0.04, 0.29]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 27 (answer L29 - 2) :: 0.16 [0.04, 0.29] --> | 0.14 [0.00, 0.29]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 59 (answer L61 - 2) :: 0.14 [0.00, 0.29] --> / 0.10 [0.00, 0.25]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 59 (answer L61 - 2) :: 0.10 [0.00, 0.25] --> (too few switches: not valid by X0's bar) | 0.00 [0.00, 0.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 33 (answer L35 - 2) :: 0.00 [0.00, 0.00] --> / 1.00 [1.00, 1.00]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 33 (answer L35 - 2) :: 1.00 [1.00, 1.00] --> | 0.29 [0.18, 0.39]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 43 (answer L45 - 2) :: 0.29 [0.18, 0.39] --> / 0.63 [0.50, 0.76]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 43 (answer L45 - 2) :: 0.63 [0.50, 0.76] --> | L44: 0.06 [0.00, 0.14]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T140437Z/verdict.md \| qwen3.5-122b-a10b :: lookup :: 44 (answer L46 - 2) :: 0.06 [0.00, 0.14] --> |
  | recall at the read peak (L24 / L56 / L40 / L36): the same | 0.07 [-0.03, 0.18]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 24 (read peak) :: 0.07 [-0.03, 0.18] --> / 0.79 [0.67, 0.90]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 24 (read peak) :: 0.79 [0.67, 0.90] --> | 0.03 [-0.09, 0.14]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 56 (read peak) :: 0.03 [-0.09, 0.14] --> / 0.79 [0.64, 0.93]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 56 (read peak) :: 0.79 [0.64, 0.93] --> | 0.10 [0.02, 0.22]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 40 (read peak) :: 0.10 [0.02, 0.22] --> / 0.85 [0.72, 0.96]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 40 (read peak) :: 0.85 [0.72, 0.96] --> | 0.38 [0.22, 0.53]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 36 (read peak) :: 0.38 [0.22, 0.53] --> / 0.46 [0.29, 0.63]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 36 (read peak) :: 0.46 [0.29, 0.63] --> | L44: 0.75 [0.66, 0.85]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T140437Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 44 (read peak) :: 0.75 [0.66, 0.85] --> |
  | recall two layers before the answer (L27 / L59 / L44 / L47): the same, descriptive (uninformative near the output (dictionary)) | 0.20 [0.06, 0.33]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 27 (answer L29 - 2) :: 0.20 [0.06, 0.33] --> / 0.59 [0.45, 0.73]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 27 (answer L29 - 2) :: 0.59 [0.45, 0.73] --> | 0.63 [0.54, 0.73]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 59 (answer L61 - 2) :: 0.63 [0.54, 0.73] --> / 0.25 [0.15, 0.37]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 59 (answer L61 - 2) :: 0.25 [0.15, 0.37] --> | 0.34 [0.20, 0.49]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 44 (answer L46 - 2) :: 0.34 [0.20, 0.49] --> / 0.62 [0.46, 0.76]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 44 (answer L46 - 2) :: 0.62 [0.46, 0.76] --> | 0.66 [0.57, 0.75]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 47 (answer L49 - 2) :: 0.66 [0.57, 0.75] --> / 0.22 [0.12, 0.31]<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 47 (answer L49 - 2) :: 0.22 [0.12, 0.31] --> | |
  | the labels: lookup at the read peak / two before the answer; recall at the read peak / two before the answer | **in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: in between -->** / uninformative near the output (dictionary) (the verdict's: in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: lookup :: 27 (answer L29 - 2) :: in between -->); **computes outside the lens at the last token<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 24 (read peak) :: computes outside the lens at the last token -->** / uninformative near the output (dictionary) (the verdict's: in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.5-9b :: recall :: 27 (answer L29 - 2) :: in between -->) | **in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: in between -->** / uninformative near the output (dictionary) (the verdict's: in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: lookup :: 59 (answer L61 - 2) :: in between -->); **computes outside the lens at the last token<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 56 (read peak) :: computes outside the lens at the last token -->** / uninformative near the output (dictionary) (the verdict's: through the lens<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| qwen3.6-27b :: recall :: 59 (answer L61 - 2) :: through the lens -->) | **computes outside the lens at the last token<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: computes outside the lens at the last token -->** / **computes outside the lens at the last token<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: lookup :: 33 (answer L35 - 2) :: computes outside the lens at the last token -->** (restored); **in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 40 (read peak) :: in between -->** / uninformative near the output (dictionary) (the verdict's: through the lens<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| muse-glimmer-30b :: recall :: 44 (answer L46 - 2) :: through the lens -->) | **computes outside the lens at the last token<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: computes outside the lens at the last token -->** / **in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 43 (answer L45 - 2) :: in between -->** (restored); **through the lens<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 36 (read peak) :: through the lens -->** / uninformative near the output (dictionary) (the verdict's: through the lens<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T090326Z/verdict.md \| nemotron-3.5-lightning :: recall :: 47 (answer L49 - 2) :: through the lens -->) | not tested / in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T140437Z/verdict.md \| qwen3.5-122b-a10b :: lookup :: 44 (answer L46 - 2) :: in between -->; in between<!-- src: results/x53_lastconflict/x53_lastconflict-20261029T140437Z/verdict.md \| qwen3.5-122b-a10b :: recall :: 44 (read peak) :: in between --> |

- **Read.**
  - At the read peak: the lookup is in between on the 9B and the 27B and computes outside the lens part on Muse and Lightning; the recall computes outside the lens part on the 9B and the 27B, is in between on Muse and goes through the lens on Lightning.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Two layers before the answer the cells are uninformative near the output (dictionary): close to the output the letter-token dictionary decides "through" vs "outside", and digits have no atoms. Their numbers stay in the table as descriptive, the verdict's labels beside. Muse's lookup at L33 and Lightning's at L43 keep their own labels ("the last layers" does not hold there): Muse's computes outside the lens part, Lightning's is in between.

- **Caveats.**
  - 59 to 75 scenes per model over 29 to 34 bridge entities; the 27B's lookup two layers before the answer switches too rarely under the whole change for X0's validity bar.
  - Here the rest alone and the change without the lens part are the same arm (the verdict's table gives them the same shares).
  - The cells two layers before the answer sit at L27 of 32<!-- src: src/bridge_jspace/pins.py \| "n_layers" :: 32 --> (9B), L59 of 64<!-- src: configs/models/qwen3.6-27b.yaml \| Target model :: 64 --> (27B), L33 / L44 of 52<!-- src: configs/models/muse-glimmer-30b.yaml \| decoder layers :: 52 --> (Muse's lookup / recall) and L43 / L47 of 52<!-- src: src/bridge_jspace/pins.py \| hybrid :: 52 --> (Lightning's): on these digit answers the answer layer is earlier than on words ([53.3b](#b53-3b)). Muse's and Lightning's lookup cells keep their labels: near the reader's answer layer; the lens dictionary has no digit atoms, but the recall's digits were captured under the same conditions, so this asymmetry is unresolved. The 27B's lookup read peak L60 is also its answer layer minus 1; it keeps its read-peak label.
  - Exploratory (batch 53): no prediction.

</details>

### Does the last-token conflict test change when the answers are words? <a id="b53-3b"></a>

`in README` `below gate: Muse, Lightning` *Used in: README "Tested and dropped" ("The copy bypasses the lens").*

Test 53.3b · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md` · recompute: `scripts/x53_lastconflict.py` (the command in its docstring) · also: four models, joint verdict 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** At the last token, does the lookup compute its answer through the lens part when the answer is a word the passage states, as the recall does, or outside it as with digits?


- **Why we asked.** On our locker scenes (digit answers) the lookup computes outside the lens part at the last token on two models while the recall goes through it near the answer ([53.3](#b53-3)); the asymmetry could belong to digits or to copying. (53.3's near-answer recall cells are now labelled uninformative near the output, Dan 11:25; its Muse and Lightning digit lookups keep their labels, Dan 11:55.)

- **Data.** the fact passages with made-up facts (Z1-P's items): the lookup copies a made-up word the passage states; the recall answers from memory, the same answer vocabulary. The 9B: 112 passages (86 bridge entities) and the 27B: 200 passages (118 entities), at their gates; Muse: 120 passages (85 entities) and Lightning: 129 passages (100 entities), their eligible passages only, below their gates.

- **Method.** 53.3's conflict test at the last token, per reader at its own answer layer minus 1, 2 and 3 and at 51.10's read peak: the whole change, without the lens part, without a random part of the same share, the lens part alone; and 53.3's lookup again on our locker scenes at its answer layer minus 1 and 3. A cell under 53.3's validity bar (whole change >= 0.30, >= 30 switches) is invalid and counts for neither clause.

- **Rule, fixed in advance.** "Rule per reader and layer: 53.3's labels. Across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between." (jobs/c3/batch53.yaml, test_53_3b, Dan ~10:05; no prediction)


Both readers at the last token, with words as answers:

![Near the output the test is uninformative; read peaks differ](../../figures/depth/ledger/13_last_conflict_words.png)

*As the figure above with words as the answers: per model, three, two and one layers before the answer and at the read peak (the rule counts the two layers nearest the answer as uninformative). Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | words, lookup: blocked beyond random at answer - 1 / - 2 (descriptive: uninformative near the output) / - 3 | 0.55 [0.44, 0.64]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 30 (answer L31 - 1) :: 0.55 [0.44, 0.64] --> / 0.37 [0.23, 0.53]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 29 (answer L31 - 2) :: 0.37 [0.23, 0.53] --> / 0.16 [0.05, 0.29]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 28 (answer L31 - 3) :: 0.16 [0.05, 0.29] --> (L30 / L29 / L28) | 0.88 [0.84, 0.92]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 62 (answer L63 - 1) :: 0.88 [0.84, 0.92] --> / 0.74 [0.68, 0.80]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 61 (answer L63 - 2) :: 0.74 [0.68, 0.80] --> / 0.58 [0.51, 0.65]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.58 [0.51, 0.65] --> (L62 / L61 / L60) | ○ 0.79 [0.71, 0.87]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 48 (answer L49 - 1) :: 0.79 [0.71, 0.87] --> / 0.66 [0.56, 0.74]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 47 (answer L49 - 2) :: 0.66 [0.56, 0.74] --> / 0.66 [0.58, 0.75]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 46 (answer L49 - 3) :: 0.66 [0.58, 0.75] --> (L48 / L47 / L46) | ○ 0.82 [0.75, 0.89]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 49 (answer L50 - 1) :: 0.82 [0.75, 0.89] --> / 0.85 [0.79, 0.91]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 48 (answer L50 - 2) :: 0.85 [0.79, 0.91] --> / 0.76 [0.68, 0.83]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 47 (answer L50 - 3) :: 0.76 [0.68, 0.83] --> (L49 / L48 / L47) | not run |
  | words, lookup at its read peak: blocked beyond random / the rest alone over the whole | 0.03 [-0.06, 0.12]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: 0.03 [-0.06, 0.12] --> / 0.61 [0.44, 0.77]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: 0.61 [0.44, 0.77] --> (L24) | 0.58 [0.51, 0.65]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.58 [0.51, 0.65] --> / 0.27 [0.21, 0.33]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.27 [0.21, 0.33] --> (L60, its answer - 3) | ○ invalid at L32 (whole change 0.27<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: 0.27 --> < 0.30) | ○ -0.05 [-0.12, 0.02]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: -0.05 [-0.12, 0.02] --> / 0.84 [0.73, 0.93]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: 0.84 [0.73, 0.93] --> (L32) | |
  | words, recall: blocked beyond random at answer - 1 / - 2 (descriptive: uninformative near the output) / - 3 | 0.65 [0.55, 0.75]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: recall :: 30 (answer L31 - 1) :: 0.65 [0.55, 0.75] --> / 0.49 [0.37, 0.62]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: recall :: 29 (answer L31 - 2) :: 0.49 [0.37, 0.62] --> / 0.47 [0.29, 0.65]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: recall :: 28 (answer L31 - 3) :: 0.47 [0.29, 0.65] --> | 0.96 [0.94, 0.99]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: recall :: 62 (answer L63 - 1) :: 0.96 [0.94, 0.99] --> / 0.88 [0.84, 0.93]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: recall :: 61 (answer L63 - 2) :: 0.88 [0.84, 0.93] --> / 0.64 [0.56, 0.71]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: recall :: 60 (answer L63 - 3) :: 0.64 [0.56, 0.71] --> | ○ 0.75 [0.66, 0.83]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: recall :: 48 (answer L49 - 1) :: 0.75 [0.66, 0.83] --> / 0.67 [0.57, 0.76]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: recall :: 47 (answer L49 - 2) :: 0.67 [0.57, 0.76] --> / 0.69 [0.60, 0.78]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: recall :: 46 (answer L49 - 3) :: 0.69 [0.60, 0.78] --> | ○ 0.88 [0.81, 0.93]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: recall :: 49 (answer L50 - 1) :: 0.88 [0.81, 0.93] --> / 0.87 [0.80, 0.93]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: recall :: 48 (answer L50 - 2) :: 0.87 [0.80, 0.93] --> / 0.74 [0.66, 0.82]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: recall :: 47 (answer L50 - 3) :: 0.74 [0.66, 0.82] --> | |
  | words, recall at its read peak: blocked beyond random | invalid at L24 (whole change 0.18<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: recall :: 24 (read peak) :: 0.18 --> < 0.30) | 0.62 [0.54, 0.70]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: recall :: 56 (read peak) :: 0.62 [0.54, 0.70] --> (L56) | ○ 0.78 [0.70, 0.86]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: recall :: 40 (read peak) :: 0.78 [0.70, 0.86] --> (L40) | ○ invalid at L36 (whole change 0.26<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: recall :: 36 (read peak) :: 0.26 --> < 0.30) | |
  | words, the labels (uninformative = uninformative near the output (dictionary)): lookup at answer - 1, - 2 / - 3 / read peak; recall at answer - 1, - 2 / - 3 / read peak | uninformative / in between / in between; uninformative / through the lens / invalid | uninformative / through the lens / through the lens (L60 is both); uninformative / through the lens / through the lens | ○ uninformative / through the lens / invalid; uninformative / through the lens / through the lens | ○ uninformative / through the lens / computes outside the lens; uninformative / through the lens / invalid | |
  | our locker scenes, lookup at answer - 1 / - 3 (a read-peak cell keeps its label) | 0.19 [0.11, 0.26]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 28 (answer L29 - 1) :: 0.19 [0.11, 0.26] --> (L28): uninformative / 0.05 [-0.02, 0.13]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 26 (answer L29 - 3) :: 0.05 [-0.02, 0.13] --> (L26): in between | 0.13 [0.03, 0.25]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 60 (read peak) :: 0.13 [0.03, 0.25] --> (L60, its read peak and answer - 1): in between / invalid at L58 (whole change 0.29<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 58 (answer L61 - 3) :: 0.29 --> < 0.30) | -0.02 [-0.05, 0.00]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 34 (answer L35 - 1) :: -0.02 [-0.05, 0.00] --> (L34): uninformative / 0.00 [0.00, 0.00]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: 0.00 [0.00, 0.00] --> (L32, its read peak and answer - 3): computes outside the lens | 0.19 [0.09, 0.29]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 44 (answer L45 - 1) :: 0.19 [0.09, 0.29] --> (L44): uninformative / 0.14 [0.05, 0.22]<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 42 (answer L45 - 3) :: 0.14 [0.05, 0.22] --> (L42): in between | |
  | per model, from the answer - 1 / - 2 cells (uninformative): copy bypasses the lens / digits only | no / yes | no / yes | ○ no / yes (not counted) | ○ no / yes (not counted) | |
  | across readers | **in between (only 2 of 4 models above their gate: neither clause can reach 3 of 4)<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| Across readers :: in between (only 2 of 4 models above their gate: neither clause can reach 3 of 4) -->** (copy bypasses on 0 and digits only on 2 of the 2 models counted<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| Across readers :: copy bypasses on 0 and digits only on 2 of the 2 models counted -->: the 9B and the 27B); the "digits only" pattern sits in cells labelled uninformative near the output (dictionary) | | | | |

- **Read.**
  - By the rule, across readers: in between. Only the 9B and the 27B are at their gates, so neither clause can reach 3 of 4.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - The "digits only" pattern under the label (the lookup through the lens part like the recall at answer - 1 and - 2 on all four models; copy bypasses on none) sits in cells labelled uninformative near the output (dictionary): at those layers the lens is close to the output and the letter-token dictionary decides "through" vs "outside", while digits have no atoms. Their numbers stay beside, descriptive.
  - Away from the output: three layers before the answer the lookup is in between on the 9B and goes through the lens on the 27B (and on Muse and Lightning, below gate); the recall goes through it on all four. At the read peak the lookup is weak (whole change 0.34<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.5-9b :: lookup :: 24 (read peak) :: 0.34 --> on the 9B, 0.27<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| muse-glimmer-30b :: lookup :: 32 (read peak) :: 0.27 --> on Muse, 0.47<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| nemotron-3.5-lightning :: lookup :: 32 (read peak) :: 0.47 --> on Lightning) and in between or outside the lens; on the 27B the read peak is its answer layer minus 3 and goes through. Three read-peak cells are under the validity bar: the 9B's recall, Muse's lookup, Lightning's recall.


- On our locker scenes, away from the output: the 9B in between at L26, the 27B in between at its read peak L60 (L58 invalid), Muse outside at its read peak L32, Lightning in between at L42.

- **Caveats.**
  - Muse (Z1-P's lookup right on 0.781<!-- src: results/x50_zach/x52_z1p-20261029T094820Z/z1p.md | 'K': 0.78125 :: 0.781 --> < 0.80) and Lightning (0.794<!-- src: jobs/c3/batch52.yaml | Z1-P on Lightning :: 0.794 --> < 0.80) are below their gates on these passages: exploratory, hollow ○, never in claims or grades, and they do not count toward "3 of 4". With two models at gate, "in between" follows from the gates; the pattern under it is descriptive.
  - Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones.
  - On word answers the answer layer sits at the end of the model: the last layer on the 9B (L31 of 32<!-- src: src/bridge_jspace/pins.py \| "n_layers" :: 32 -->) and the 27B (L63 of 64<!-- src: configs/models/qwen3.6-27b.yaml \| Target model :: 64 -->), the second-to-last on Lightning (L50 of 52<!-- src: src/bridge_jspace/pins.py \| hybrid :: 52 -->) and the third-to-last on Muse (L49 of 52<!-- src: configs/models/muse-glimmer-30b.yaml \| decoder layers :: 52 -->). Answer - 1 and - 2 are among the final layers.
  - The 27B's check at L58 is invalid (whole change 0.29<!-- src: results/x53_lastconflict/x53_lastconflict_words-20261029T100850Z/verdict.md \| qwen3.6-27b :: lookup :: 58 (answer L61 - 3) :: 0.29 --> < 0.30), so its locker label rests on L60 alone.
  - Exploratory (batch 53): no prediction.

</details>

### On Lightning, does the lookup read the bridge word through attention blocks 19 and 26? <a id="b53-4"></a>

`in README` *Used in: README Part IV card "On Lightning, does the lookup read the bridge word through its attention blocks?".*

Test 53.4 · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x53_attnblock/x53_attnspan-20261029T102727Z` · recompute: `scripts/x53_attnblock.py` (the command in its docstring) · also: a follow-up with a later control

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On Lightning, does the lookup read the bridge word through its attention blocks 19 and 26?


- **Why we asked.** Lightning's attention heads move with the address swap in blocks 19 and 26 ([attention under the swap](#t49-7)); its other blocks are Mamba-2 state, so the bridge word could reach the lookup through two attention blocks.

- **Data.** Main test at L14, 200 scenes (37 bridge entities); the whole change switches the lookup on 88 of them. The follow-up (a later control): the same 200 scenes; its rule reads the 83 scenes (35 bridge entities) where the control fits; the 117 where none fits (median span 28 tokens) are dropped from the rule and read beside.

- **Method.** The whole change at the bridge word at L14, with attention from every later position to the bridge word's position blocked in (i) block 19, (ii) block 26, (iii) both, (iv) every attention block after L14 (19, 26, 33, 42), and (v) the control: both blocks, attention to a random other token of the same sentence; the share of the whole change's lookup switches cut; the recall beside. The follow-up: in blocks 19 and 26 every position after the scene's last token cannot attend to the span from the bridge word to the scene's end (median 9 tokens on the rule's scenes); the control: a span of the same length ending at the last token before the bridge's sentence, one placement: a later control.

- **Rule, fixed in advance.** "Rule: "read through two blocks" if (iii) cuts the lookup's switches by >= 0.6 of the whole change's and (v) by <= 0.15; "one block" if (i) or (ii) alone cuts >= 0.6; "not through attention at the bridge" if (iv) cuts < 0.3 (the Mamba state carries it); else in between." (jobs/c3/batch52.yaml, lightning_attn_block, Dan ~10:05; no prediction) Follow-up (span): "the pointer [pointer: the address] is read by attention after the Mamba state spreads it" if the span cuts the lookup's switches by >= 0.6 and the control by <= 0.15; else as 53.4. (jobs/c3/batch53.yaml, next_1110, Dan 11:10; no prediction)


Each block or span cut on Lightning:

![Two attention blocks carry a third of Lightning's lookup switch](../../figures/depth/ledger/14_attention_blocks.png)

*Lightning: the switches blocked when attention blocks are cut, lookup (left) and recall (right), per block or span cut (rows), with a control block and a control span. Whiskers 95% intervals; all estimates post hoc.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup switches cut: (i) block 19 / (ii) block 26 | not applicable | not applicable | not applicable | 0.114 [0.039, 0.189]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| (i) block 19 only: S 0.390 :: 0.114 [0.039, 0.189] --> / 0.136 [0.060, 0.216]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| (ii) block 26 only: S 0.380 :: 0.136 [0.060, 0.216] --> | not applicable |
  | lookup: (iii) both blocks / (iv) every attention block after L / (v) control | | | | 0.341 [0.253, 0.420]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| (iii) blocks 19 and 26: S 0.290 :: 0.341 [0.253, 0.420] --> / 0.352 [0.272, 0.423]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| every attention block after L: S 0.285 :: 0.352 [0.272, 0.423] --> / 0.000 [-0.056, 0.054]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| random non-bridge token of the bridge :: 0.000 [-0.056, 0.054] --> | |
  | the clean answer unchanged, (iii) / (iv) | | | | 0.770<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| (iii) blocks 19 and 26: S 0.290 :: 0.770 --> / 0.760<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| every attention block after L: S 0.285 :: 0.760 --> | |
  | recall (beside): (iv) every attention block after L | | | | 0.555 [0.441, 0.647]<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| every attention block after L: S 0.425 :: 0.555 [0.441, 0.647] --> | |
  | the rule (lookup) | | | | **in between<!-- src: results/x53_attnblock/x53_attnblock-20261029T091303Z/verdict.md \| Label (lookup) :: in between -->** | |
  | follow-up (a later control; one placement): lookup switches cut by the span / the control span, on the 83 scenes where the control fits (S_whole 0.831<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| lookup (the rule's scenes) :: S_whole 0.831 :: 0.831 -->) | | | | 0.522 [0.411, 0.617]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| cannot attend to any position from the bridge word :: 0.522 [0.411, 0.617] --> / -0.015 [-0.050, 0.000]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| the control: blocks 19 and 26 :: -0.015 [-0.050, 0.000] --> | |
  | follow-up, beside (descriptive): the span / the control on the 37<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| survives the span block :: 37 of 83 :: 37 --> rule scenes where the lookup's clean answer survives the span block | | | | 0.538 [0.333, 0.708]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| survives the span block :: the span's cut 0.538 [0.333, 0.708] :: 0.538 [0.333, 0.708] --> / 0.000 [0.000, 0.000]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| survives the span block :: the control's 0.000 [0.000, 0.000] :: 0.000 [0.000, 0.000] --> | |
  | follow-up: (iii) rerun on the same scenes, lookup cut | | | | 0.333 [0.243, 0.418]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| (iii) of 53.4, rerun here :: 0.333 [0.243, 0.418] --> | |
  | follow-up: the clean answer unchanged, span / control / (iii) rerun | | | | 0.446<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| cannot attend to any position from the bridge word :: clean kept 0.446 :: 0.446 --> / 1.000<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| the control: blocks 19 and 26 :: clean kept 1.000 :: 1.000 --> / 0.578<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| (iii) of 53.4, rerun here :: clean kept 0.578 :: 0.578 --> | |
  | follow-up: lookup cut by the span on all 200 scenes / on the 117 without a control (S_whole 0.188<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| no control fits, lookup :: S_whole 0.188 :: 0.188 -->: mostly not switching, uninformative) | | | | 0.407 [0.262, 0.538]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| all, lookup :: span cut 0.407 [0.262, 0.538] :: 0.407 [0.262, 0.538] --> / 0.045 [-0.571, 0.423]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| no control fits, lookup :: span cut 0.045 [-0.571, 0.423] :: 0.045 [-0.571, 0.423] --> | |
  | follow-up: recall (beside), span / control | | | | 0.293 [0.198, 0.385]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| cannot attend to any position from the bridge word :: 0.293 [0.198, 0.385] --> / -0.012 [-0.042, 0.000]<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| the control: blocks 19 and 26 :: -0.012 [-0.042, 0.000] --> | |
  | follow-up: the rule (lookup) | | | | **in between<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| Label (lookup) :: in between -->** (decided on the 83 scenes) | |
  | follow-up, first run, control placement superseded (results/x53_attnblock/x53_attnspan-20261029T102727Z): span / control, 95 scenes | | | | 0.527 [0.412, 0.627]<!-- src: results/x53_attnblock/x53_attnspan-20261029T102727Z/verdict.md \| cannot attend to any position from the bridge word :: 0.527 [0.412, 0.627] --> / 0.000 [-0.039, 0.041]<!-- src: results/x53_attnblock/x53_attnspan-20261029T102727Z/verdict.md \| the control: blocks 19 and 26 :: 0.000 [-0.039, 0.041] --> | |

- **Read.**
  - Blocking the bridge word in attention blocks 19 and 26 cuts about a third of Lightning's lookup switches, as much as blocking every attention block after L; either block alone cuts little, and the control cuts nothing. By the rule this is in between: the lookup is partly read through those two blocks.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - Follow-up (a later control): blocking the whole span from the bridge word to the scene's end in blocks 19 and 26 cuts about half of the lookup's switches on the 83 scenes where the control fits, the control span nothing; under 0.6, so in between by the rule. The span also costs the clean answer on more than half of those scenes. The first run, with the superseded control, gave the same picture.
  - On the scenes the span block leaves readable (the lookup's clean answer survives), the span still cuts about the same share: the cut is not just general damage (descriptive, the label stays as computed on all 83).

- **Caveats.**
  - The block also costs the clean answer on about a quarter of items (collateral), and blocking every attention block after L cuts more than half of the recall's switches.
  - The follow-up's control is one placement, ending at the last token before the bridge's sentence: a later control (same length, same distance to the question, inside the scene, not touching the bridge's sentence). It cannot match the span's distance to the question: the span reaches the scene's end, and the control ends further from the question (median 12.0<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| Distance to the question's first token :: the control's end 12.0 :: 12.0 --> tokens against the span's 1.0<!-- src: results/x53_attnblock/x53_attnspan_c-20261029T121412Z/verdict.md \| Distance to the question's first token :: the span's end 1.0 :: 1.0 -->).
  - The span's collateral is large: the clean answer is unchanged on less than half of the rule's scenes under the span, on all of them under the control. On the 117 scenes without a control the lookup mostly does not switch, so the span's cut there is uninformative.
  - One model by design; exploratory (batch 53), no prediction.

</details>

## Part V. Other datasets and operations

### Does the split hold on the fact passages with a named bridge? <a id="z1"></a>

`in README` *Used in: README Part V card "Does the split hold on the fact passages, and do the two operations agree?" (the named fact passages and the recheck); README "Tested and dropped" ("The lookup follows the lens part on the fact passages").*

Test Z1 · opened 28 Oct · status: rule fixed in advance · hand-check: in sample (view e) · files: `results/x50_zach/z1-20261028T161649Z/z1.md` · recompute: `scripts/x50_zach.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages with a named bridge, does the lookup let go of the lens part while the recall follows it?

![On the named fact passages the lookup follows the lens part too](../../figures/common/readme/15_facts.png)

*The lookup on passages with true and with made-up facts, per model; whiskers: intervals on the true-fact values (Muse: too few lookup switches, not drawn).*


- **Why we asked.** Our scenes are short lists; the fact passages scatter the facts in prose.

- **Data.** His passages (named bridge; the lookup's passage states the true final fact, the recall's leaves it out): 200 per model (Lightning at L14, which decides, and L27 beside). Z1-P: the fact passages with made-up facts, 200 each on the 9B, 27B, Muse (L26) and Lightning.

- **Method.** The conflict test at the bridge name's last token at L: without the lens part, against without a random part; each reader gets its own change.

- **Rule, fixed in advance.** "Per model: gap >= 0.3 and lookup extra drop <= 0.10 → the split holds on his passages; lookup >= 0.20 → the lookup follows the lens here; else in between. The order pattern replicates if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs)." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse (L26) | Lightning (L14) | 122B |
  |---|---|---|---|---|---|
  | lookup: switches blocked beyond a random part | 0.26 [0.18, 0.36]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| qwen35_9b_x50_z1 :: 0.26 [0.18, 0.36] --> | 0.28 [0.18, 0.38]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| x50_z1_27b :: 0.28 [0.18, 0.38] --> | 0.60 [0.38, 0.81]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| muse30_x50_z1 :: 0.60 [0.38, 0.81] --> | 0.15 [0.07, 0.25]<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| nem35l_x52_z1 :: 0.48 [0.40, 0.55] :: 0.15 [0.07, 0.25] --> | 0.12 [0.05, 0.20]<!-- src: results/x50_zach/x52_z1-20261029T215701Z/z1.md \| qwen35_122b_z1 :: 200 (115) :: 0.12 [0.05, 0.20] --> (L33) |
  | recall: switches blocked beyond a random part | 0.64 [0.56, 0.71]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| qwen35_9b_x50_z1 :: 0.64 [0.56, 0.71] --> | 0.58 [0.49, 0.66]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| x50_z1_27b :: 0.58 [0.49, 0.66] --> | 0.81 [0.72, 0.90]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| muse30_x50_z1 :: 0.81 [0.72, 0.90] --> | 0.48 [0.40, 0.55]<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| nem35l_x52_z1 :: 0.15 [0.07, 0.25] :: 0.48 [0.40, 0.55] --> | 0.41 [0.33, 0.49]<!-- src: results/x50_zach/x52_z1-20261029T215701Z/z1.md \| qwen35_122b_z1 :: 200 (115) :: 0.41 [0.33, 0.49] --> |
  | lookups switched, fact-first / fact-after | 0.78 [0.68, 0.86]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L12 order :: 0.78 [0.68, 0.86] --> / 0.36 [0.27, 0.46]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L12 order :: 0.36 [0.27, 0.46] --> | 0.67 [0.57, 0.76]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L32 order :: 0.67 [0.57, 0.76] --> / 0.11 [0.05, 0.17]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L32 order :: 0.11 [0.05, 0.17] --> | 0.20 [0.12, 0.29]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L26 order :: 0.20 [0.12, 0.29] --> / 0.05 [0.01, 0.10]<!-- src: results/x50_zach/z1-20261028T161649Z/z1.md \| L26 order :: 0.05 [0.01, 0.10] --> | 0.71 [0.61, 0.80]<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| L14 order :: 0.71 [0.61, 0.80] --> / 0.38 [0.27, 0.49]<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| L14 order :: 0.38 [0.27, 0.49] --> | |
  | the rule | **the lookup follows the lens here** | **the lookup follows the lens here** | **the lookup follows the lens here** | **in between<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| nem35l_x52_z1 :: 0.32 [0.21, 0.44] :: in between -->** (gap 0.32 [0.21, 0.44]<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| nem35l_x52_z1 :: 0.32 [0.21, 0.44] -->; no prediction) | **in between<!-- src: results/x50_zach/x52_z1-20261029T215701Z/z1.md \| qwen35_122b_z1 :: 200 (115) :: in between -->** (no prediction; L39: can't tell) |
  | made-up facts (Z1-P): lookup, switches blocked beyond a random part | -0.05 [-0.13, 0.03]<!-- src: results/x50_zach/x52_z1p-20261029T081112Z/z1p.md \| qwen35_9b_x52_z1p :: -0.05 [-0.13, 0.03] --> | 0.15 [0.06, 0.25]<!-- src: results/x50_zach/x52_z1p-20261029T081323Z/z1p.md \| x52_z1p_27b :: 0.15 [0.06, 0.25] --> | ○ 0.04 [0.00, 0.14]<!-- src: results/x50_zach/x52_z1p-20261029T094820Z/z1p.md \| muse30_x53_z1p :: 0.04 [0.00, 0.14] --> | ○ 0.03 [-0.10, 0.15]<!-- src: results/x50_zach/x52_z1p-20261029T080731Z/z1p.md \| nem35l_x52_z1p :: 0.03 [-0.10, 0.15] --> | 0.02 [-0.07, 0.10]<!-- src: results/x50_zach/x52_z1p-20261029T223420Z/z1p.md \| qwen35_122b_z1p :: 0.02 [-0.07, 0.10] --> |
  | made-up facts: recall, the same | 0.59 [0.51, 0.67]<!-- src: results/x50_zach/x52_z1p-20261029T081112Z/z1p.md \| qwen35_9b_x52_z1p :: 0.59 [0.51, 0.67] --> | 0.62 [0.53, 0.70]<!-- src: results/x50_zach/x52_z1p-20261029T081323Z/z1p.md \| x52_z1p_27b :: 0.62 [0.53, 0.70] --> | ○ 0.81 [0.72, 0.90]<!-- src: results/x50_zach/x52_z1p-20261029T094820Z/z1p.md \| muse30_x53_z1p :: 0.81 [0.72, 0.90] --> | ○ 0.48 [0.41, 0.55]<!-- src: results/x50_zach/x52_z1p-20261029T080731Z/z1p.md \| nem35l_x52_z1p :: 0.48 [0.41, 0.55] --> | 0.35 [0.28, 0.42]<!-- src: results/x50_zach/x52_z1p-20261029T223420Z/z1p.md \| qwen35_122b_z1p :: 0.35 [0.28, 0.42] --> |
  | made-up facts: the gap | 0.64 [0.51, 0.76]<!-- src: results/x50_zach/x52_z1p-20261029T081112Z/z1p.md \| qwen35_9b_x52_z1p :: 0.64 [0.51, 0.76] --> | 0.47 [0.36, 0.58]<!-- src: results/x50_zach/x52_z1p-20261029T081323Z/z1p.md \| x52_z1p_27b :: 0.47 [0.36, 0.58] --> | ○ 0.77 [0.63, 0.89]<!-- src: results/x50_zach/x52_z1p-20261029T094820Z/z1p.md \| muse30_x53_z1p :: 0.77 [0.63, 0.89] --> | ○ 0.45 [0.30, 0.60]<!-- src: results/x50_zach/x52_z1p-20261029T080731Z/z1p.md \| nem35l_x52_z1p :: 0.45 [0.30, 0.60] --> | 0.33 [0.23, 0.44]<!-- src: results/x50_zach/x52_z1p-20261029T223420Z/z1p.md \| qwen35_122b_z1p :: 0.33 [0.23, 0.44] --> |
  | made-up facts: the rule | **the split holds on his passages<!-- src: results/x50_zach/x52_z1p-20261029T081112Z/z1p.md \| qwen35_9b_x52_z1p :: the split holds on his passages --> [the fact passages]** | **in between<!-- src: results/x50_zach/x52_z1p-20261029T081323Z/z1p.md \| x52_z1p_27b :: in between -->** | not tested (gate 0.781<!-- src: results/x50_zach/x52_z1p-20261029T094820Z/z1p.md \| 'K': 0.78125 :: 0.781 --> < 0.80); numbers descriptive only | not tested (gate 0.794<!-- src: jobs/c3/batch52.yaml \| Z1-P on Lightning :: 0.794 --> < 0.80); numbers descriptive only | **the split holds on his passages<!-- src: results/x50_zach/x52_z1p-20261029T223420Z/z1p.md \| qwen35_122b_z1p :: the split holds on his passages --> [the fact passages]** |
  | made-up facts, the 9B rechecked: the full set (200 passages, 129 entities) / without the 60 passages whose lookup passage holds the bridge's true value (140, 100): lookup / recall / gap | -0.05 [-0.13, 0.03]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| full :: 200 (129) :: -0.05 [-0.13, 0.03] --> / 0.59 [0.51, 0.67]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| full :: 200 (129) :: 0.59 [0.51, 0.67] --> / 0.64 [0.51, 0.76]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| full :: 200 (129) :: 0.64 [0.51, 0.76] -->; -0.07 [-0.17, 0.03]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| without the 60 :: 140 (100) :: -0.07 [-0.17, 0.03] --> / 0.56 [0.46, 0.67]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| without the 60 :: 140 (100) :: 0.56 [0.46, 0.67] --> / 0.63 [0.49, 0.78]<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| without the 60 :: 140 (100) :: 0.63 [0.49, 0.78] --> | | | | |
  | the same: the rule, full set / without the 60 | **the split holds on his passages<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| full :: 200 (129) :: the split holds on his passages --> [the fact passages]** / **the split holds on his passages<!-- src: results/x50_zach/x53_z1p_clean-20261029T115708Z/verdict.md \| without the 60 :: 140 (100) :: the split holds on his passages --> [the fact passages]** | | | | |

- **Read.**
  - Rechecked on the 9B without the 60 passages where the bridge's true value stands in the lookup's passage as another entity's value: the split holds on the remaining 140 as on the full set, with the same gap.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - On the named-bridge fact passages the lookup follows the lens part too on the 9B and 27B; Muse's lookup switches too rarely to tell (see the flags in the operations log). The order pattern replicates on all three.
  - On Lightning at L14 the split is in between: the lookup has more blocked than the 0.10 bar but far less than the recall; its order pattern does not replicate (fact-first under twice fact-after).


- On the fact passages with made-up facts (Z1-P) the 9B's split holds and the 27B's is in between; Muse and Lightning missed the gate there, so their numbers are descriptive only.

- **Caveats.**
  - The fact passages' true-fact lookups (the first four rows) state facts the model may know; the made-up-fact rerun (Z1-P, 29 Oct) ran on the 9B, 27B (L32) and Lightning (L14): coverage runs on the same rule, no prediction, 200 passages each; Muse not run.
  - Hollow ○: below the gate, numbers descriptive only, never in claims or grades.
  - Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones (Muse's and Lightning's made-up-fact gates).
  - Muse's lookup switches under the whole change on 0.12 of passages; at L36 it cannot tell. Lightning's L27 (beside) likewise: its lookup switches on 1<!-- src: results/x50_zach/x52_z1-20261029T013035Z/z1.md \| L27: routes :: "original": 198, "switch": 1 :: 1 --> of 200 passages there, so the verdict's "follows the lens here" at L27 is not valid (Flagged 13).

</details>

### On the fact passages, does the answer control read the same with the bridge named and described? <a id="b53-1b"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 53.1b · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md` · recompute: `scripts/x51_answer.py` (the command in its docstring) · also: the 9B and the 27B

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages with made-up facts, what do 51.12's arms (is it the bridge item or its answer that moves through the lens?) say when the passage names the bridge (PP: the lookup reads the made-up value the passage states; PM: the recall answers from memory) and when it describes the bridge instead (MP: the lookup; MM: the recall)? In his codes the first letter is how the bridge enters, the second where the answer comes from; the made-up fact is stated in every cell, so PP against MP is a named against a described bridge, for the lookup.
- **Why we asked.** A priority of 29 Oct ("jsuite PP vs MP, 51.12's arms + readout"): on the fact passages the cells exist already, no new scenes.
- **Data.** the fact passages with made-up facts: the named bridge (Z1-P's items) and the described bridge (Z2's design, the change at the description's last token); 200 per cell where tested; the 9B at L12, the 27B at L32.
- **Method.** 51.12's arms per cell: the readout check first (is the answer word in the lens's top 50 at the bridge word?), then the change without the lens part, without the lens part but keeping the answer's directions, and without the answer directions only, each beyond a random part.

- **Rule, fixed in advance.** 51.12's rule per cell: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1's extra drop and arm 3 costs <= 0.10 beyond random; "the lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1; else mixed; the readout check first ("the answer word is not read at the bridge word" if its lens rank is above 50 on >= 90% of items). (results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md; no prediction)

The answer control per chain:

![Named: both recalls mixed; described: the 27B's reads as the answer](../../figures/depth/ledger/15_fact_answer_control.png)

*The answer control on the fact passages with the bridge named, per chain (P: read in the passage, M: recalled; the last letter is the hop the reader answers): the switches blocked without the lens part and with only the answer word's directions removed, lookup (violet) and recall (black). Whiskers 95% intervals.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | PP (lookup, named bridge): blocked without the lens part, beyond random | -0.05 [-0.13, 0.05]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.5-9b :: lookup :: -0.05 [-0.13, 0.05] --> | 0.16 [0.06, 0.26]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.6-27b :: lookup :: 0.16 [0.06, 0.26] --> | not designed | not designed | not run |
  | PP: the label | **can't tell<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.5-9b :: lookup :: can't tell -->** | **the answer word is not read at the bridge word<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.6-27b :: lookup :: the answer word is not read at the bridge word -->** | | | |
  | PM (recall, named bridge): blocked without the lens part, beyond random | 0.59 [0.51, 0.67]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.5-9b :: recall :: 0.59 [0.51, 0.67] --> | 0.63 [0.54, 0.72]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.6-27b :: recall :: 0.63 [0.54, 0.72] --> | | | |
  | PM: the label | **mixed<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.5-9b :: recall :: mixed -->** | **mixed<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z1p :: qwen3.6-27b :: recall :: mixed -->** | | | |
  | MP (lookup, described bridge): blocked without the lens part, beyond random | MP and MM (described bridge) | 0.38 [0.19, 0.56]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: lookup :: 0.38 [0.19, 0.56] --> | | | |
  | MP: the label | | **the answer word is not read at the bridge word<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: lookup :: the answer word is not read at the bridge word -->** (95% of 140 items; the arms beside: mixed) | | | |
  | MM (recall, described bridge): blocked without the lens part, beyond random / share remaining with the answer directions retained / the answer directions alone over the effect | | 0.64 [0.46, 0.83]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: recall :: 0.64 [0.46, 0.83] --> / 0.06 [-0.18, 0.27]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: recall :: 0.06 [-0.18, 0.27] --> / 0.75 [0.42, 1.22]<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: recall :: 0.75 [0.42, 1.22] --> | | | |
  | MM: the label | | **the lens effect is the answer<!-- src: results/x51_answer/x53_jsuite-20261029T095443Z/verdict.md \| z2p :: qwen3.6-27b :: recall :: the lens effect is the answer -->** | | | |

- **Read.**
  - On the named-bridge passages both recalls read as mixed: keeping the answer's directions keeps only part of the recall's drop, and the answer directions alone cost some of it; the 9B's lookup has nothing blocked beyond random (cannot tell), and the 27B's answer word is not read at the bridge word.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - On the described bridge the 27B's recall reads as the answer: keeping the answer's directions keeps little of its drop, and the answer directions alone cost most of it; its lookup's answer word is not read at the bridge word.

- **Caveats.**
  - The 9B's described-bridge passages missed the gate (lookup right on 0.757 of 169 cases), so its MP and MM cells are not tested and have no numbers; the 27B's passed theirs (read right on 0.940, 140 chosen of 184).
  - Gates just under 0.80 stay not tested: on the harder variants the eligible items are the easier ones (the 9B's described-bridge passages).
  - Exploratory (batch 53): no prediction.

</details>

### Does the split survive when the bridge is changed at every layer up to L? <a id="t51-7"></a>

`in README` *Used in: README Part V card "Does the split hold on the fact passages, and do the two operations agree?" (the full carrier).*

Test 51.7 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md` · recompute: `scripts/x51_carrier.py` (the command in its docstring) · also: Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages, does changing the bridge token at every layer up to L (the full carrier) explain the one-layer result, and does the split hold there?
- **Why we asked.** At one layer his fact-after lookups barely switch; the link may be carried by the bridge token over several layers.
- **Data.** Z1's passages: 200 per model (9B: 100 fact-first, 100 fact-after; 27B: 97 / 103; Lightning, at L14: 103<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| fact-first :: 103 (87) :: 103 --> / 97<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| fact-after :: 97 (80) :: 97 -->); 9B, 27B and Lightning.
- **Method.** The change at the bridge name's last token at every block output up to L; the conflict test on it: without the lens part, against without a random part of the same share; the one-layer change beside.

- **Rule, fixed in advance.** "(i) "The slice explanation": the whole before-L raises the lookup's switch on fact-after items by >= 0.3 over the one-layer whole, and on fact-first brings the lookup within 0.10 of the recall. (ii) On the full carrier, per model and reported per stratum with fact-first decisive: recall extra drop - lookup extra drop >= 0.3 and lookup <= 0.10 -> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on the full carrier"; else in between." (verdict.md) Lightning: a coverage run on this rule, no prediction.

One layer against every layer up to L:

![Over every layer up to L, fact-after lookups follow the lens part](../../figures/depth/ledger/16_every_layer.png)

*The change at the bridge word at one layer (left) and at every layer up to L (right): the switches blocked without the lens part beyond a random part, lookup (violet) and recall (black), with the fact sentence before the pick and after it. Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | fact-after lookups switched: one layer → full carrier, rise | 0.54 [0.44, 0.64]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| qwen35_9b_x51_7 :: 0.54 [0.44, 0.64] --> | 0.73 [0.64, 0.81]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| x51_7_27b :: 0.73 [0.64, 0.81] --> | not run | 0.49 [0.39, 0.60]<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| nem35l_x52_carrier :: 0.49 [0.39, 0.60] --> | not run |
  | fact-first: lookup switches blocked beyond a random part | 0.10 [0.05, 0.17]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.10 [0.05, 0.17] --> | 0.16 [0.07, 0.25]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.16 [0.07, 0.25] --> | | 0.14 [0.05, 0.23]<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| in between :: 0.14 [0.05, 0.23] --> | |
  | fact-first: recall switches blocked beyond a random part | 0.41 [0.31, 0.52]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.41 [0.31, 0.52] --> | 0.28 [0.18, 0.38]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| in between :: 0.28 [0.18, 0.38] --> | | 0.37 [0.27, 0.48]<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| in between :: 0.37 [0.27, 0.48] --> | |
  | fact-after: lookup switches blocked beyond a random part | 0.51 [0.41, 0.61]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| the lookup follows the lens on the full carrier :: 0.51 [0.41, 0.61] --> | 0.51 [0.42, 0.61]<!-- src: results/x51_carrier/x51_7-20261028T171646Z/verdict.md \| the lookup follows the lens on the full carrier :: 0.51 [0.42, 0.61] --> | | 0.41 [0.31, 0.52]<!-- src: results/x51_carrier/x52_carrier-20261029T014338Z/verdict.md \| the lookup follows the lens on the full carrier :: 0.41 [0.31, 0.52] --> | |
  | rule (i) / (ii), fact-first | holds / in between | holds / in between | | holds / in between; (iii) no (no prediction) | |

- **Read.**
  - Carried over every layer up to L, the fact-after lookups switch as often as the fact-first ones, so the one-layer result was a slice; the same on Lightning.

<details><summary>The result in full, more reading and caveats</summary>

More from the reading:

  - On the full carrier the fact-first split is in between; fact-after lookups follow the lens part.

- **Caveats.**
  - The fact passages' lookups state true facts (see [Z1](#z1)).
  - Muse not run (designed for the 9B and 27B).

</details>

### Does the lookup take a position route on the fact passages? <a id="z3"></a>

`in README` *Used in: README Part V card "Does the split hold on the fact passages, and do the two operations agree?" (the routes test on the fact passages).*

Test Z3 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x50_zach/x52_z3-20261029T024151Z/z3.md` · recompute: `scripts/x50_zach.py` (the command in its docstring) · also: the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages with scattered facts, does the lookup take a position route besides the identity route?
- **Why we asked.** The address codes where a locker sentence sits in a list; the fact passages have no list.
- **Data.** His level-0 passages with all three facts before the sentence that names the bridge: 60 (9B), 81<!-- src: results/x50_zach/x52_z3-20261029T024151Z/z3.md \| x50_z3_27b :: 81 (72) :: 81 --> (27B, at L32: X0's layer and the start of the breadth track's band), 48 (Muse), 52<!-- src: results/x50_zach/x52_z3-20261029T013329Z/z3.md \| nem35l_x52_z3 :: 52 (47) :: 52 --> (Lightning, at L14 and L27).
- **Method.** The routes test: the change comes from a passage where another item's fact sentence moved and took a new value; the lookup's answer is sorted into identity, position, value or original.

- **Rule, fixed in advance.** "Value <= 0.05; if position >= 0.2: the address exists in scattered-fact passages; if position <= 0.05: no position route in his layout." The 27B and Lightning: coverage runs on this rule, no prediction.

The three routes on the fact passages:

![On the fact passages the lookup rarely takes the position route](../../figures/depth/ledger/17_fact_routes.png)

*The routes test on the fact passages: the share of the lookup's answers by identity (blue), by position (orange) and by value (slate), at each model's layer tested and, where run, a later one. Whiskers 95% intervals; the 27B, Lightning and the 122B hollow ○ (coverage runs, or after the data).*

</details>

- **Result.**

  | | 9B | 27B (L32) | Muse (L26) | Lightning (L14) | 122B |
  |---|---|---|---|---|---|
  | identity | 0.43 [0.30, 0.56]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.43 [0.30, 0.56] --> | 0.47 [0.35, 0.59]<!-- src: results/x50_zach/x52_z3-20261029T024151Z/z3.md \| x50_z3_27b :: 0.47 [0.35, 0.59] --> | 0.19 [0.08, 0.31]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.19 [0.08, 0.31] --> | 0.52 [0.37, 0.66]<!-- src: results/x50_zach/x52_z3-20261029T013329Z/z3.md \| nem35l_x52_z3 :: 52 (47) :: 0.52 [0.37, 0.66] --> | 0.57 [0.43, 0.70]<!-- src: results/x50_zach/x52_z3-20261030T035019Z/z3.md \| qwen35_122b_z3 :: 0.57 [0.43, 0.70] --> (L33) |
  | position | 0.10 [0.02, 0.19]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.10 [0.02, 0.19] --> | 0.04 [0.00, 0.09]<!-- src: results/x50_zach/x52_z3-20261029T024151Z/z3.md \| x50_z3_27b :: 0.04 [0.00, 0.09] --> | 0.06 [0.00, 0.14]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.06 [0.00, 0.14] --> | 0.10 [0.02, 0.19]<!-- src: results/x50_zach/x52_z3-20261029T013329Z/z3.md \| nem35l_x52_z3 :: 0.52 [0.37, 0.66] :: 0.10 [0.02, 0.19] --> | 0.02 [0.00, 0.06]<!-- src: results/x50_zach/x52_z3-20261030T035019Z/z3.md \| qwen35_122b_z3 :: 0.57 [0.43, 0.70] :: 0.02 [0.00, 0.06] --> |
  | value | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| qwen35_9b_x50_z3 :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/x52_z3-20261029T024151Z/z3.md \| x50_z3_27b :: 0.04 [0.00, 0.09] :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/z3-20261028T163053Z/z3.md \| muse30_x50_z3 :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/x52_z3-20261029T013329Z/z3.md \| nem35l_x52_z3 :: 0.52 [0.37, 0.66] :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x50_zach/x52_z3-20261030T035019Z/z3.md \| qwen35_122b_z3 :: 0.57 [0.43, 0.70] :: 0.00 [0.00, 0.00] --> |
  | the rule | **in between** | **no position route in his layout<!-- src: results/x50_zach/x52_z3-20261029T024151Z/z3.md \| x50_z3_27b :: no position route in his layout --> [the fact passages' layout]** (no prediction) | **in between** (L36: no position route) | **in between<!-- src: results/x50_zach/x52_z3-20261029T013329Z/z3.md \| nem35l_x52_z3 :: 0.10 [0.02, 0.19] :: in between -->** (L27: no position route; no prediction) | **no position route in his layout<!-- src: results/x50_zach/x52_z3-20261030T035019Z/z3.md \| qwen35_122b_z3 :: 0.57 [0.43, 0.70] :: no position route in his layout --> [the fact passages' layout]** (L39 too; no prediction) |

- **Read.**
  - On the fact passages the lookup rarely takes the position route: in between on the 9B, Muse and Lightning at L, and almost none on the 27B (no position route in the fact passages' layout); it never takes the value.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Small n (60 / 81 / 48 / 52); the lookup only.
  - The 27B is read at L32 only (X0's layer and the start of the breadth track's band).

</details>

### Does the breadth track's read window match ours? <a id="t51-5"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test 51.5 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x51_depth/x51_5-20261028T181100Z/verdict.md` · recompute: `scripts/x51_depth.py` (the command in its docstring)

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages, does each reader's read window end within 4 layers of ours?
- **Why we asked.** His swap works up to about L20; ours up to L16 on the 9B; the windows decide where the two operations can be compared.
- **Data.** Z1's passages, 200 per model (9B, 27B; Lightning: a coverage run with the design taken from the 9B / 27B spec, adapted to its layers, no prediction).
- **Method.** The whole change at the bridge name's last token, one layer at a time; the window's end is the last layer where a reader switches on at least 0.3.

- **Rule, fixed in advance.** "The same read window as ours if the last layer where each reader's switch >= 0.3 lies within 4 layers of ours."

Each reader's switches by layer on the fact passages:

![On the 9B the fact passages are read over our layers; on the 27B not](../../figures/depth/ledger/18_read_window.png)

*The fact passages' read window: the share of each reader's answers switched by the whole change at the bridge name, one layer at a time, lookup (violet) and recall (black); dashed: the bar fixed in advance. Lightning post hoc (a coverage run).*

</details>

- **Result.** (window ends, his / ours)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup | L14 / L16 (-2)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| qwen35_9b_x51_5 :: L14 / L16 (-2) --> | L34 / L40 (-6)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| x51_5_27b :: L34 / L40 (-6) --> | not designed | L18 / L22 (-4)<!-- src: results/x51_depth/x52_depth51-20261029T083500Z/verdict.md \| nem35l_x52_depth51 :: L18 / L22 (-4) --> | not run |
  | recall | L18 / L14 (4)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| qwen35_9b_x51_5 :: L18 / L14 (4) --> | L34 / L32 (2)<!-- src: results/x51_depth/x51_5-20261028T181100Z/verdict.md \| x51_5_27b :: L34 / L32 (2) --> | | L22 / L22 (0)<!-- src: results/x51_depth/x52_depth51-20261029T083500Z/verdict.md \| nem35l_x52_depth51 :: L22 / L22 (0) --> | |
  | the rule | **the same window** | **not the same** | | **the same read window as ours<!-- src: results/x51_depth/x52_depth51-20261029T083500Z/verdict.md \| nem35l_x52_depth51 :: the same read window as ours -->** (no prediction) | |

- **Read.**
  - On the 9B the fact passages are read over the same layers as our scenes; on the 27B the lookup's window ends 6 layers earlier.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning's run uses the 9B / 27B design (adapted design, coverage run); its own window from its anatomy run (L22 for both readers).
  - Our 27B window comes from a coarser grid (every 8th layer with L30-34).
  - Layer ends carry no interval.

</details>

## Part VI. What did not hold

### Does the split hold for a described bridge? <a id="t47-3"></a>

`in README` `below gate: Lightning` *Used in: README Part VI, one line with a link ("A described bridge in our scenes").*

Test 47.3 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_cue/x47_3-20261028T113104Z/x47_3.md` · recompute: `scripts/x47_cue.py` (the command in its docstring) · also: described bridge, opened 28 Oct; Lightning's gate 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When the asked pick describes the item instead of naming it ("picked the one known for honey"), does the lookup still let go of the lens part at the description's word while the recall follows it?
- **Why we asked.** A described bridge must be computed first; the computed item could travel through the lens.
- **Data.** Routes scenes with the asked pick described: 300 per model (15 / 15 / 9 bridge items). Lightning not tested: its gate failed. The answer control on these scenes (51.12's cue r2, 9B and 27B, 300 each) in the table; Lightning's was cancelled with 47.3.
- **Method.** The change at the description's word at L, another item moved (C2); without the lens part against a random part of its share; value answers; the refit address's cut beside.

![A described bridge: the split holds on two of the three models](../../figures/depth/readme/19_described_bridge.png)

*A described bridge ("the one known for …") instead of a named one, per model: the switches blocked without the lens part beyond a random part, lookup (violet) and recall (black), over the grey band; the gap (slate) with its interval; the position answers cut beyond random without the address (amber). Lightning hollow (○, post hoc). Whiskers: 95% intervals.*

- **Rule, fixed in advance.** "(a) "the split holds for a recalled bridge": gap >= 0.3 and lookup extra drop <= 0.10; (a') "a recalled bridge is handed through the lens": lookup extra drop >= 0.20 [...]; (b) "never the value": value <= 0.05; (c) "a pointer [pointer: the address] at the cue token": U' removal cuts position answers >= 0.30 beyond random."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | lookup: switches blocked beyond a random part | 0.07 [0.01, 0.16]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| qwen35_9b_x47_cue :: 0.07 [0.01, 0.16] --> | 0.39 [0.32, 0.45]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| x47_cue_27b :: 0.39 [0.32, 0.45] --> | -0.02 [-0.12, 0.08]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| muse30_x47_cue :: -0.02 [-0.12, 0.08] --> | ○ 0.17 [0.10, 0.22]<!-- src: results/x47_cue/x52_cue_below-20261029T083221Z/x47_3.md \| nem35l_x52_cue_below :: 0.17 [0.10, 0.22] --> | not run |
  | recall: the same | 0.39 [0.31, 0.47]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| qwen35_9b_x47_cue :: 0.39 [0.31, 0.47] --> | 0.48 [0.37, 0.60]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| x47_cue_27b :: 0.48 [0.37, 0.60] --> | 0.33 [0.12, 0.60]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| muse30_x47_cue :: 0.33 [0.12, 0.60] --> | ○ 0.48 [0.37, 0.57]<!-- src: results/x47_cue/x52_cue_below-20261029T083221Z/x47_3.md \| nem35l_x52_cue_below :: 0.48 [0.37, 0.57] --> | |
  | the gap | 0.32 [0.20, 0.41]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| qwen35_9b_x47_cue :: 0.32 [0.20, 0.41] --> | 0.09 [-0.02, 0.20]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| x47_cue_27b :: 0.09 [-0.02, 0.20] --> | 0.36 [0.06, 0.66]<!-- src: results/x47_cue/x47_3-20261028T113104Z/x47_3.md \| muse30_x47_cue :: 0.36 [0.06, 0.66] --> | ○ 0.31 [0.21, 0.42]<!-- src: results/x47_cue/x52_cue_below-20261029T083221Z/x47_3.md \| nem35l_x52_cue_below :: 0.31 [0.21, 0.42] --> | |
  | the rule | **the split holds** | **handed through the lens** | **the split holds** | not tested (gate 0.72<!-- src: results/x47_cue/x52_cue-20261029T023827Z/x47_3.md \| nem35l_x52_cue :: 0.72 --> < 0.80); below gate, descriptive only: (a) no, (a') no | |
  | answer control (51.12 cue r2): the answer word not read at the cue word, lookup / recall | 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.5-9b :: lookup :: 1.00 [1.00, 1.00] --> / 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.5-9b :: recall :: 1.00 [1.00, 1.00] --> | 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.6-27b :: lookup :: 1.00 [1.00, 1.00] --> / 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.6-27b :: recall :: 1.00 [1.00, 1.00] --> | not run | cancelled with 47.3 | not run |
  | answer control: the recall's arms beside, remaining with the answer directions retained / the answer directions alone | 1.00 [0.95, 1.07]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.5-9b :: recall :: 1.00 [0.95, 1.07] --> / 0.01 [0.00, 0.03]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.5-9b :: recall :: 0.01 [0.00, 0.03] --> | 0.97 [0.92, 1.03]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.6-27b :: recall :: 0.97 [0.92, 1.03] --> / 0.05 [0.02, 0.09]<!-- src: results/x51_answer/x51_12-20261028T201842Z/verdict.md \| cue :: qwen3.6-27b :: recall :: 0.05 [0.02, 0.09] --> (the entity) | | | |

- **Read.**
  - The answer control: on the 9B and the 27B the answer word is not read at the cue word on every item, and the recall's arms beside say the item.

<details><summary>The result in full, more reading and caveats</summary>

The result in full:

  Lightning, below its gate (exploratory, hollow ○): the answer control (51.12's arms on these scenes) finds the answer word not read at the bridge word for either reader, on 1.00 [1.00, 1.00]<!-- src: results/x51_answer/x52_answer_below-20261029T083454Z/verdict.md | cue :: nemotron-3.5-lightning :: recall :: 1.00 [1.00, 1.00] --> of items (the arms beside say the entity).

More from the reading:

  - For a described bridge the split holds on the 9B and Muse; on the 27B the lookup follows the lens part too (the bridge is handed through the lens there). The lookup never takes the value, and no address sits at the description's word.

- **Caveats.**
  - Lightning's columns are below its gate (the lookup right on 0.72): exploratory, hollow ○, never in claims or grades.
  - Few bridge items (9 to 15).
  - Muse's recall effect is wide.

</details>

### Under one question with two instructions, does the lens part follow the source or the question? <a id="t47-15"></a>

`in README` `below gate: 9B, Muse, Lightning` *Used in: README Part VI, one line with a link ("One question under two instructions").*

Test 47.15 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_source/x47_15-20261028T142722Z/x47_15.md` · recompute: `scripts/x47_source.py` (the command in its docstring) · also: one question, two sources; the 27B

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** When one question asks for the answer "from the passage" or "from what you know", does each part of the change follow the source of the answer or the question?
- **Why we asked.** The lookup answers from the passage and the recall from memory: the split could follow the source, or the question the reader is asked.
- **Data.** Routes scenes (locker first) with a false-legs sentence per item, one question under two instructions (from the text / from memory) and none; 300 scenes per condition on the 27B at L32. Muse's gate failed with the fact after (memory 0.746<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| muse-glimmer-30b (muse30_x47_15_r2, L26) :: memory :: 0.746 -->); the 9B's rerun and Lightning's coverage run failed their gates too.
- **Method.** The change at the bridge word at L: without the lens part, and without the address and identity parts (U + I), each against a random part of its share; per condition (the text, memory), the fact placed after.

*No figure: one model tested (the 27B), three numbers per instruction: the Result's table.*

- **Rule, fixed in advance.** "a condition is like a lookup if without J++ <= 0.10 and without U + I >= 0.30, like a recall if without J++ >= 0.30 and without U + I <= 0.10, can't tell if its whole cell is invalid (S_whole < 0.30 or < 30 switches), else neither; the part follows the source if text is like a lookup and memory like a recall; follows the question if both give the same label (lookup or recall); each on the batch on >= 2 of 3 models; a model whose gate (0.80 per instruction) fails is not tested." (results/x47_source/x47_15-20261028T142722Z/x47_15.md; Dan's Q47.15 prediction)

</details>

- **Result.** (the fact placed after)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | from the text: blocked without the lens part / without U + I, beyond random | not tested (gate) | 0.54 [0.43, 0.66]<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| x47_15_27b_r2 :: tested :: 0.54 [0.43, 0.66] --> / 0.39 [0.30, 0.49]<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| x47_15_27b_r2 :: tested :: 0.39 [0.30, 0.49] --> | not tested (gate) | not tested (gate) | not run |
  | from memory: the same | | 0.55 [0.40, 0.68]<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| x47_15_27b_r2 :: tested :: 0.55 [0.40, 0.68] --> / 0.31 [0.20, 0.44]<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| x47_15_27b_r2 :: tested :: 0.31 [0.20, 0.44] --> | | | |
  | the labels: text / memory | | **neither<!-- src: results/x47_source/x47_15-20261028T142722Z/x47_15.md \| x47_15_27b_r2 :: tested :: neither -->** / **can't tell** | | | |

- **Read.**
  - On the 27B both instructions have most of their switches blocked without the lens part and many without the address and identity parts: neither instruction reads like a lookup or a recall, so the part follows neither the source nor the question. With no instruction the 27B answers from the passage.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - One model; the 9B, Muse and Lightning missed the gate (Lightning's coverage rerun: results/x47_source/x52_source-20261029T062807Z).
  - The coverage matrix named this test "the second hop's key token" until its 12:20 build; that is another failure ([47.14](#t47-14)).

</details>

### Are the lookup's errors address errors? <a id="t47-13"></a>

`in README` *Used in: README Part VI, one line with a link ("The lookup's errors are not address errors").*

Test 47.13 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_errors/x47_13-20261028T113107Z/x47_errors.md` · recompute: `scripts/x47_errors.py` (the command in its docstring) · also: the address probe on the lookup's errors; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Where the lookup answers wrong on unedited varied scenes, does the address probe read the slot of the wrong answer, while the lens still names the right item?
- **Why we asked.** If the address carries the position route, some of the lookup's errors could come from a wrong address.
- **Data.** Unedited varied scenes where the lookup answers wrong (see the table).
- **Method.** A slot probe trained on the scenes the lookup gets right (per format and locker order, the wrong item's entity held out), read on the wrong ones against the wrong answer's slot; the lens's top item at the bridge word beside.

*No figure: one or two numbers per model against chance: the Result's table (the two-panel figure was mostly text).*

- **Rule, fixed in advance.** ""The address predicts the error" if the probe's slot matches the wrong answer's slot in >= 0.5 of wrong items (chance ~ 0.33 with three lockers; the layout baseline beside), and the lens's top item at the bridge word is still the right item in >= 0.8 of those." Lightning: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | the lookup's wrong answers, with a probe | 100<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| qwen35_9b_x47_errors :: 100 (91 / 100; 40) :: 100 --> | 5<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| x47_errors_27b :: 5 (5 / 5; 5) :: 5 --> | 32<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| muse30_x47_errors :: 32 (32 / 32; 25) :: 32 --> | 105<!-- src: results/x47_errors/x47_13-20261029T035254Z/x47_errors.md \| nem35l_x52_errors :: 105 (100 / 105; 40) :: 105 --> | 7 (coverage, 30 Oct) |
  | the probe matches the wrong answer's slot (bar >= 0.5) | 0.07 [0.02, 0.12]<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| qwen35_9b_x47_errors :: 0.07 [0.02, 0.12] --> | 0.00 [0.00, 0.00]<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| x47_errors_27b :: 0.00 [0.00, 0.00] --> | 0.06 [0.00, 0.16]<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| muse30_x47_errors :: 0.06 [0.00, 0.16] --> | 0.05 [0.01, 0.09]<!-- src: results/x47_errors/x47_13-20261029T035254Z/x47_errors.md \| nem35l_x52_errors :: 0.05 [0.01, 0.09] --> | |
  | chance | 0.20<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| qwen35_9b_x47_errors :: 100 (91 / 100; 40) :: 0.20 --> | 0.14<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| x47_errors_27b :: 5 (5 / 5; 5) :: 0.14 --> | 0.20<!-- src: results/x47_errors/x47_13-20261028T113107Z/x47_errors.md \| muse30_x47_errors :: 32 (32 / 32; 25) :: 0.20 --> | 0.19<!-- src: results/x47_errors/x47_13-20261029T035254Z/x47_errors.md \| nem35l_x52_errors :: 105 (100 / 105; 40) :: 0.19 --> | |
  | the rule | **no** | not tested (5 errors, under 30) | pending (no lens read): no | **no** (no prediction) | not tested (7 errors, under 30) |

- **Read.**
  - On the 9B and Lightning the probe matches the wrong answer's slot in under a tenth of errors, below chance: the lookup's errors are not address errors. The 27B makes too few errors to test, and Muse's lens read never landed.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning's verdict header prints "Q47.13, Dan: 65%", but this is a coverage run with no prediction (Flagged 23).
  - Errors are few: about 100 per model over 40 bridge items.

</details>

### Does the lens part key the item's attribute, and do late MLPs at the bridge word carry the recall? <a id="t48-2"></a>

`in README` *Used in: README "Tested and dropped" ("Four mechanisms for the split").*

Test 48.2 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x48_enrich/x48_2-20261028T113111Z/x48_2.md` · recompute: `scripts/x48_enrich.py` (the command in its docstring) · also: enrichment; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** (A) After L, does a probe for the item's attribute at the bridge word move with the lens part and not without it? (B) Does mean-ablating the bridge word's MLPs after L cost the recall its answer while the lookup's own is unchanged?
- **Why we asked.** The recall could fetch the item's attribute at the bridge word, keyed by the lens part, through late MLPs.
- **Data.** Main test, 200 per model for design B; the attribute probe on animal items, entities held out, for design A. Lightning: design A only (it has no per-block MLP to ablate for design B).
- **Method.** (A) At every probed layer from L+4 where the attribute probe reads above twice chance: its move under the whole change, without the lens part and without a random part. (B) The bridge word's MLP writes mean-ablated at layers after L; controls: the asked person's token after L, and the bridge word up to L/2.

*No figure: one deciding number per model against its bar: the Result's table (the five-panel mechanism figure is retired).*

- **Rule, fixed in advance.** A: "J++ keys the enrichment if, at every probed layer >= L + 4 where the legs probe (animals, entities held out) reads the attribute (held-out accuracy >= 2x chance), the probe moves >= 0.6 of the way under whole and under no_rand and <= 0.3 under no_jpp (the paired CI of no_rand - no_jpp excluding 0), on both models". B: "the recall's retrieval runs through the bridge token's late MLPs if recall accuracy falls >= 0.4 under bridge_late while lookup accuracy stays within 0.1, and both controls stay within 0.1 for both readers." The 27B and Lightning: coverage runs on these rules, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | A: the lens part keys the attribute probe (layers after L+4) | does not hold at the bridge token<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| qwen35_9b_x48_2a :: does not hold at the bridge token --> | does not hold at the bridge token<!-- src: results/x48_enrich/x52_enrich-20261029T044139Z/x48_2.md \| x48_2a_27b :: does not hold at the bridge token --> | does not hold at the bridge token<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| muse30_x48_2a :: does not hold at the bridge token --> | does not hold at the bridge token<!-- src: results/x48_enrich/x52_enrich-20261029T044514Z/x48_2.md \| nem35l_x52_enrich_a :: does not hold at the bridge token --> | not run |
  | B: recall accuracy drop, the bridge word's MLPs after L mean-ablated (bar >= 0.4) | 0.13 [0.08, 0.19]<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| qwen35_9b_x48_2b :: 1.00 [1.00, 1.00] :: 0.13 [0.08, 0.19] --> | 0.03 [0.01, 0.06]<!-- src: results/x48_enrich/x52_enrich-20261029T044139Z/x48_2.md \| x48_2b_27b :: 1.00 [1.00, 1.00] :: 0.03 [0.01, 0.06] --> | 0.01 [0.00, 0.03]<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| muse30_x48_2b :: 1.00 [1.00, 1.00] :: 0.01 [0.00, 0.03] --> | not run (no per-block MLP) | |
  | B: lookup accuracy drop the same way (bar: within 0.1) | 0.02 [0.00, 0.04]<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| qwen35_9b_x48_2b :: 0.13 [0.08, 0.19] :: 0.02 [0.00, 0.04] --> | 0.00 [0.00, 0.00]<!-- src: results/x48_enrich/x52_enrich-20261029T044139Z/x48_2.md \| x48_2b_27b :: 0.03 [0.01, 0.06] :: 0.00 [0.00, 0.00] --> | 0.00 [0.00, 0.00]<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| muse30_x48_2b :: 0.01 [0.00, 0.03] :: 0.00 [0.00, 0.00] --> | | |
  | the verdicts A / B | does not hold<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| Verdict A :: does not hold --> / does not hold<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| Verdict B :: does not hold --> | does not hold<!-- src: results/x48_enrich/x52_enrich-20261029T044139Z/x48_2.md \| Verdict A :: does not hold --> / does not hold<!-- src: results/x48_enrich/x52_enrich-20261029T044139Z/x48_2.md \| Verdict B :: does not hold --> | does not hold<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| Verdict A :: does not hold --> / does not hold<!-- src: results/x48_enrich/x48_2-20261028T113111Z/x48_2.md \| Verdict B :: does not hold --> | does not hold<!-- src: results/x48_enrich/x52_enrich-20261029T044514Z/x48_2.md \| Verdict A :: does not hold --> / not run (no prediction) | |

- **Read.**
  - On the 9B, 27B and Muse neither holds, and design A fails on Lightning too: the lens part does not key the attribute probe at the bridge word, and the bridge word's late MLPs are not needed for the recall.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Design B's early-MLP control moves answers on all three, so the controls do not stay within 0.1 either.
  - The verdicts read that the recall survives because the attribute is fetched at the last token; that reading is the verdict's, not tested here.

</details>

### Is the person who picked an item marked at its locker sentence? <a id="t48-3"></a>

`in README` `below gate: Lightning` *Used in: README "Tested and dropped" ("Four mechanisms for the split").*

Test 48.3 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md` · recompute: `scripts/x48_bind.py` (the command in its docstring) · also: person mark; the 27B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Is the person who picked an item written into the item's locker sentence, readable by a probe there, outside the lens, and able to move the lookup when written?
- **Why we asked.** A forward binding at the locker sentence would let the lookup find the pick's locker without reading the bridge word through the lens.
- **Data.** Main-test scenes split by sentence order; the probe's rule cell, locker after: 266<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| qwen3.5-9b :: item :: 266 --> / 335<!-- src: results/x48_bind/x52_bind-20261029T023827Z/x48_bind.md \| qwen3.6-27b :: item :: 335 --> / 278<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| muse-glimmer-30b :: item :: 278 --> sentences (9B / 27B / Muse).
- **Method.** A probe for which of the scene's three people picked the item, at the item and number tokens of the locker sentence; the person contrast's share in the lens part against random directions; the contrast written at both tokens at doses 1 and 2, against a random vector of its size.

*No figure: one deciding number per model against its bar: the Result's table (the five-panel mechanism figure is retired).*

- **Rule, fixed in advance.** "forward binding at the locker sentence, outside the lens: probe >= 0.85 in locker-after and <= 0.5 in locker-first; the person contrast's J++ share (k = 25) <= 2x a random direction's; the write sends >= 0.3 of lookups to the written item's locker (random <= 0.05); on both models." The 27B: a coverage run on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | probe for who picked it, locker after, item token (bar >= 0.85) | 0.36 [0.30, 0.42]<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| qwen3.5-9b :: item :: 0.36 [0.30, 0.42] --> | 0.50 [0.43, 0.56]<!-- src: results/x48_bind/x52_bind-20261029T023827Z/x48_bind.md \| qwen3.6-27b :: item :: 0.50 [0.43, 0.56] --> | 0.36 [0.31, 0.42]<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| muse-glimmer-30b :: item :: 0.36 [0.31, 0.42] --> | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80) | not run |
  | the same, number token | 0.33 [0.27, 0.39]<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| qwen3.5-9b :: number :: 0.33 [0.27, 0.39] --> | 0.31 [0.26, 0.35]<!-- src: results/x48_bind/x52_bind-20261029T023827Z/x48_bind.md \| qwen3.6-27b :: number :: 0.31 [0.26, 0.35] --> | 0.39 [0.34, 0.44]<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| muse-glimmer-30b :: number :: 0.39 [0.34, 0.44] --> | | |
  | the write: lookups sent to the written item's locker, dose 2 (bar >= 0.3) | 0.000<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| qwen35_9b_x48_bind :: s = 2: target 0.000 :: 0.000 --> | 0.010<!-- src: results/x48_bind/x52_bind-20261029T023827Z/x48_bind.md \| x48_bind_27b :: s = 2: target 0.010 :: 0.010 --> | 0.015<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| muse30_x48_bind :: s = 2: target 0.015 :: 0.015 --> | | |
  | the rule | **does not hold<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| Verdict :: does not hold -->** | **does not hold<!-- src: results/x48_bind/x52_bind-20261029T023827Z/x48_bind.md \| Verdict :: does not hold -->** (no prediction) | **does not hold<!-- src: results/x48_bind/x48_bind-20261028T113120Z/x48_bind.md \| Verdict :: does not hold -->** | | |

- **Read.**
  - On all three models the person who picked an item cannot be read at its locker sentence (near the 0.33 chance, far under 0.85), and writing a person contrast there moves almost no lookup.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The 27B's item-token probe reads 0.50, above chance but far under the bar.
  - The lens-share clause holds on the 27B and Muse and fails on the 9B; it does not decide alone.

</details>

### Is the person mark spread over the locker sentence? <a id="t49-3"></a>

`ledger only` `below gate: Lightning` *Used in: not in the README (its rebuild).*

Test 49.3 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x49_probe/x49_3-20261028T154604Z/x49_3.md` · recompute: `scripts/x49_probe.py` (the command in its docstring) · also: pooled person probe; the 27B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** In locker-after scenes, is who picked an item readable from the item's whole locker sentence pooled, though no single token holds it, or as a flag "picked by the asked person"?
- **Why we asked.** The single-token probe (48.3) reads chance; a mark spread over the sentence would escape it.
- **Data.** Clean one-pick scenes, the lookup's original prompt; the rule reads locker-after scenes, locker-first ones are the control.
- **Method.** Ridge probes (48.3's) on every token of each locker sentence and on the sentence mean, at L/2 and L: (i) which of the scene's three people picked the item; (ii) whether the asked person picked it.

- **Rule, fixed in advance.** ""Distributed person mark": pooled (i) >= 0.85 with every per-token (i) <= 0.6. "A picked-flag, not a person": (ii) >= 0.85 pooled or at some token while (i) <= 0.5. "Neither at the sentence": both at chance; the link is made elsewhere." The 27B: a coverage run on this rule, no prediction.

The pooled probe against the best single token:

![No probe reads who picked an item at its locker sentence](../../figures/depth/ledger/19_person_probe.png)

*Who picked the item, read by a probe at its locker sentence: the accuracy pooled over the sentence (with its 95% interval) and at the best single token, at half the test layer and at it. The 27B and Lightning hollow ○ (a coverage run; below its gate).*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (i) who picked it, pooled / best single token, at L/2 | L6: 0.29<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L6 :: (i) pooled 0.29 :: 0.29 --> / 0.37<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L6 :: per-token max 0.37 :: 0.37 --> | L16: 0.35<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L16 :: (i) pooled 0.35 :: 0.35 --> / 0.38<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L16 :: per-token max 0.38 :: 0.38 --> | L13: 0.25<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L13 :: (i) pooled 0.25 :: 0.25 --> / 0.31<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L13 :: per-token max 0.31 :: 0.31 --> | ○ L7: 0.26<!-- src: results/x49_probe/x52_probe49_below-20261029T085547Z/x49_3.md \| L7 :: (i) pooled 0.26 :: 0.26 --> / 0.33<!-- src: results/x49_probe/x52_probe49_below-20261029T085547Z/x49_3.md \| L7 :: per-token max 0.33 :: 0.33 --> | not run |
  | the same at L (rule's bar: pooled >= 0.85) | L12: 0.32<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L12 :: (i) pooled 0.32 :: 0.32 --> / 0.38<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L12 :: per-token max 0.38 :: 0.38 --> | L32: 0.36<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L32 :: (i) pooled 0.36 :: 0.36 --> / 0.47<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L32 :: per-token max 0.47 :: 0.47 --> | L26: 0.29<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L26 :: (i) pooled 0.29 :: 0.29 --> / 0.41<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L26 :: per-token max 0.41 :: 0.41 --> | ○ L14: 0.28<!-- src: results/x49_probe/x52_probe49_below-20261029T085547Z/x49_3.md \| L14 :: (i) pooled 0.28 :: 0.28 --> / 0.35<!-- src: results/x49_probe/x52_probe49_below-20261029T085547Z/x49_3.md \| L14 :: per-token max 0.35 :: 0.35 --> | |
  | (ii) picked by the asked person, pooled at L (chance 0.50) | 0.50<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L12 :: (ii) pooled 0.50 :: 0.50 --> | 0.50<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L32 :: (ii) pooled 0.50 :: 0.50 --> | 0.50<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L26 :: (ii) pooled 0.50 :: 0.50 --> | ○ 0.50<!-- src: results/x49_probe/x52_probe49_below-20261029T085547Z/x49_3.md \| L14 :: (ii) pooled 0.50 :: 0.50 --> | |
  | the label at L/2; at L | neither<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L6 :: neither at the sentence (neither) :: neither -->; neither<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| qwen35_9b_x49_3 :: L12 :: neither at the sentence (neither) :: neither --> | neither<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L16 :: neither at the sentence (neither) :: neither -->; in between<!-- src: results/x49_probe/x52_probe49-20261029T044135Z/x49_3.md \| x49_3_27b :: L32 :: in between (between) :: in between --> | neither<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L13 :: neither at the sentence (neither) :: neither -->; neither<!-- src: results/x49_probe/x49_3-20261028T154604Z/x49_3.md \| muse30_x49_3 :: L26 :: neither at the sentence (neither) :: neither --> | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80); below gate, descriptive only: neither; neither | |

- **Read.**
  - No probe reads who picked an item from its locker sentence, pooled or at one token, on any of the three models: the 9B and Muse sit at chance at both layers ("neither at the sentence"); the 27B's best token at L comes out "in between", far under 0.85; the picked-flag probe is at chance everywhere.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning: below the clean one-pick gate, so not tested; its below-gate run (eligible items, L7 and L14) is exploratory, hollow ○, never in claims or grades.
  - "In between" at the 27B's L does not contradict "did not hold": neither reading fixed in advance holds there.
  - The locker-first control is at chance on all three, as the rule requires.

</details>

### Do the copying heads pass the rest of the change at twice the lens part? <a id="t48-4"></a>

`in README` *Used in: README "Tested and dropped" ("Four mechanisms for the split").*

Test 48.4 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md` · recompute: `scripts/x48_heads.py` (the command in its docstring) · also: copying heads; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Do the five heads that copy most from the bridge word to the last token pass the rest of the change at least twice as strongly as the lens part?
- **Why we asked.** The lookup follows the rest of the change; heads that copy the rest would be its path.
- **Data.** Main-test items, locker first: 75<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| qwen35_9b_x48_heads :: 75 --> / 69<!-- src: results/x48_heads/x52_heads48-20261029T044138Z/x48_heads.md \| x48_heads_27b :: 69 --> / 68<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| muse30_x48_heads :: 68 --> / 59<!-- src: results/x48_heads/x52_heads48-20261029T044514Z/x48_heads.md \| nem35l_x52_heads48 :: 59 --> (9B / 27B / Muse / Lightning).
- **Method.** For the five heads with the most attention from the last token to the bridge word, each part of the change (the lens part, the rest, the address, a random part) read through the head's output-value map; medians over items.

*No figure: one deciding number per model against its bar: the Result's table (the five-panel mechanism figure is retired).*

- **Rule, fixed in advance.** "a head reads the rest if r(rest) >= 2 r(J++) with r(random) between them or below both (r(random) <= r(rest)), medians over items, W_OV = W_O W_V; a model holds on at least 3 of its 5 heads; the batch holds if both models hold." The 27B and Lightning: coverage runs on this rule, no prediction.

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | heads that pass the rest at twice the lens part (of 5; bar: 3) | 0 of 5<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| qwen35_9b_x48_heads :: 75 :: 0 of 5 --> | 0 of 5<!-- src: results/x48_heads/x52_heads48-20261029T044138Z/x48_heads.md \| x48_heads_27b :: 69 :: 0 of 5 --> | 1 of 5<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| muse30_x48_heads :: 68 :: 1 of 5 --> | 0 of 5<!-- src: results/x48_heads/x52_heads48-20261029T044514Z/x48_heads.md \| nem35l_x52_heads48 :: 59 :: 0 of 5 --> | not run |
  | heads with r(address) >= r(rest) | 4 of 5<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| qwen35_9b_x48_heads :: 75 :: 4 of 5 --> | 1 of 5<!-- src: results/x48_heads/x52_heads48-20261029T044138Z/x48_heads.md \| x48_heads_27b :: 69 :: 1 of 5 --> | 3 of 5<!-- src: results/x48_heads/x48_heads-20261028T113126Z/x48_heads.md \| muse30_x48_heads :: 68 :: 3 of 5 --> | 2 of 5<!-- src: results/x48_heads/x52_heads48-20261029T044514Z/x48_heads.md \| nem35l_x52_heads48 :: 59 :: 2 of 5 --> | |
  | the rule, per model | **no** | **no** (no prediction) | **no** | **no** (no prediction) | |

- **Read.**
  - On all four models at most one of the five heads that copy most passes the rest at twice the lens part; the rule fails.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The coverage verdicts print "0 of 1" or "0 of 2 models hold (both needed)": the across-models clause read on the given runs; the per-model labels are the result. Lightning's heads are read on its attention layers (the attention port).
  - Five heads per model, chosen by attention from the last token to the bridge word.

</details>

### Is the address the recall's second route? <a id="t48-5"></a>

`in README` `below gate: Lightning` *Used in: README "Tested and dropped" ("Four mechanisms for the split").*

Test 48 route2 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md` · recompute: `scripts/x48_route2.py` (the command in its docstring) · also: the address as the recall's second route, opened 28 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Writing another slot's address at the bridge word, does the recall then name the item in that slot (slot k's item), as a second route besides the lens part?
- **Why we asked.** The recall has some blocked switches without the address; the address might be a route into the recall too.
- **Data.** Clean one-pick scenes with both items' lockers before the asked pick, informative writes: 224<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| qwen35_9b_x48_route2 :: 224 (34) :: 224 --> / 316<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| x48_route2_27b :: 316 (36) :: 316 --> / 208<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| muse30_x48_route2 :: 208 (36) :: 208 --> (9B / 27B / Muse). Lightning not tested: the clean one-pick design's gate fails on it.
- **Method.** At the bridge word at L: (i) the change without its lens part alone; (ii) the address of slot k written; (iii) the write alone; (iv) a random vector of the write's size; the recall's answer sorted by the attribute it matches.

*No figure: one deciding number per model against its bar: the Result's table (the five-panel mechanism figure is retired).*

- **Rule, fixed in advance.** "the recall's second route is the address if under (ii) the recall names slot k's item in >= 0.3 of the informative writes with the random vector (iv) <= 0.05 (point estimates), on >= 2 of 3 models."

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | (ii) the address written: recalls naming slot k's item (bar >= 0.3) | 0.10 [0.06, 0.15]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| qwen35_9b_x48_route2 :: 224 (34) :: 0.10 [0.06, 0.15] --> | 0.04 [0.02, 0.07]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| x48_route2_27b :: 316 (36) :: 0.04 [0.02, 0.07] --> | 0.07 [0.03, 0.12]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| muse30_x48_route2 :: 208 (36) :: 0.07 [0.03, 0.12] --> | ○ 0.11 [0.06, 0.17]<!-- src: results/x48_route2/x52_route2_below-20261029T084835Z/x48_route2.md \| nem35l_x52_route2_below :: 0.11 [0.06, 0.17] --> | not run |
  | (iv) a random vector of its size (bar <= 0.05) | 0.01 [0.00, 0.02]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| qwen35_9b_x48_route2 :: 224 (34) :: 0.01 [0.00, 0.02] --> | 0.02 [0.01, 0.04]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| x48_route2_27b :: 316 (36) :: 0.02 [0.01, 0.04] --> | 0.05 [0.02, 0.09]<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| muse30_x48_route2 :: 208 (36) :: 0.05 [0.02, 0.09] --> | ○ 0.04 [0.01, 0.09]<!-- src: results/x48_route2/x52_route2_below-20261029T084835Z/x48_route2.md \| nem35l_x52_route2_below :: 0.04 [0.01, 0.09] --> | |
  | holds | **no<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| qwen35_9b_x48_route2 :: 224 (34) :: no -->** | **no<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| x48_route2_27b :: 316 (36) :: no -->** | **no<!-- src: results/x48_route2/x48_route2-20261028T113127Z/x48_route2.md \| muse30_x48_route2 :: 208 (36) :: no -->** | not tested (gate 0.751<!-- src: results/x52_coverage/matrix-20261029T062909Z/matrix.json \| clean one-pick design's gate fails on Lightning (recall 0.751 :: 0.751 --> < 0.80); below gate, descriptive only: no (122<!-- src: results/x48_route2/x52_route2_below-20261029T084835Z/x48_route2.md \| nem35l_x52_route2_below :: 122 --> informative writes) | |

- **Read.**
  - Writing another slot's address makes the recall name that slot's item in at most a tenth of writes on all three models: the address is not the recall's second route.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning: below the clean one-pick gate, so not tested; the below-gate run (eligible items only) is exploratory, hollow ○, never in claims or grades.
  - Muse's random vector reaches 0.05, at the rule's bar.
  - Clean scenes with both lockers first only.

</details>

### Is the address formed by the pick sentence reading the lockers? <a id="t47-6"></a>

`in README` *Used in: README Part VI, one line with a link ("Blocking the pick sentence from the lockers").*

Test 47.6 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_edges/x47_6-20261028T113107Z/verdict.md` · recompute: `scripts/x47_edges.py` (the command in its docstring) · also: blocking the pick sentence; the 27B's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Blocking the pick sentence from reading the locker sentences at every layer up to L, are only the position answers blocked, with identity answers and the recall's switch still there?
- **Why we asked.** If the pick token forms the address by reading the lockers, blocking those reads should remove position answers alone.
- **Data.** Routes scenes (another item moved, a filler sentence first): 300 per model (9B / 27B / Muse).
- **Method.** Attention from the pick sentence to the locker sentences blocked at layers 0 to L, in both forward passes that make the change; control: the same number of edges to the filler sentence; the lookup's routes and the recall's switch.

*No figure: one deciding number per model against its bar: the Result's table (the five-panel mechanism figure is retired).*

- **Rule, fixed in advance.** ""the pointer [pointer: the address] is formed by the pick token reading the lockers" if position answers fall to <= 0.10 (from 0.51 / 0.54) while identity answers stay within 0.10 and the recall's switch within 0.10, on Muse and the 9B; the control within 0.10 of none." The 27B: a coverage run on this rule, no prediction.

</details>

- **Result.** (paired, the block minus no block)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | position answers, block minus none | -0.43 [-0.48, -0.37]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.43 [-0.48, -0.37] --> | -0.25 [-0.30, -0.21]<!-- src: results/x47_edges/x52_edges-20261029T023820Z/verdict.md \| block/sentence/all :: -0.25 [-0.30, -0.21] --> | -0.39 [-0.44, -0.33]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.39 [-0.44, -0.33] --> | not run | not run |
  | identity answers, block minus none (bar: within 0.10) | -0.32 [-0.37, -0.27]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.32 [-0.37, -0.27] --> | -0.30 [-0.34, -0.24]<!-- src: results/x47_edges/x52_edges-20261029T023820Z/verdict.md \| block/sentence/all :: -0.30 [-0.34, -0.24] --> | -0.25 [-0.31, -0.19]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.25 [-0.31, -0.19] --> | | |
  | the recall's switch, block minus none (bar: within 0.10) | -0.23 [-0.29, -0.18]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.23 [-0.29, -0.18] --> | -0.22 [-0.27, -0.17]<!-- src: results/x47_edges/x52_edges-20261029T023820Z/verdict.md \| block/sentence/all :: -0.22 [-0.27, -0.17] --> | -0.15 [-0.20, -0.09]<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| block/sentence/all :: -0.15 [-0.20, -0.09] --> | | |
  | the rule | **does not hold<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| Formation :: does not hold -->** | **does not hold<!-- src: results/x47_edges/x52_edges-20261029T023820Z/verdict.md \| Formation :: does not hold -->** (no prediction) | **does not hold<!-- src: results/x47_edges/x47_6-20261028T113107Z/verdict.md \| Formation :: does not hold -->** | | |

- **Read.**
  - On all three models the block removes position answers, but identity answers and the recall's switch fall too, by more than 0.10: blocking the pick sentence does not single out the address.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Part (c), blocking the question's reads, was dropped before any run.
  - The control (edges to the filler sentence) stays within 0.10 of no block on all three.

</details>

### Is the address the same for any kind of item? <a id="t47-11"></a>

`in README` *Used in: README Part VI, one line with a link ("the address for other kinds of item").*

Test 47.11 · opened not stated · status: rule fixed in advance · hand-check: not in sample · files: `results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md` · recompute: `scripts/x47_agnostic.py` (the command in its docstring) · also: other kinds of item; the 27B's and Lightning's coverage runs 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** With fruits or names as the items instead of animals, does the address fit on animal scenes still carry the lookup's position answers?
- **Why we asked.** An address, not an animal code, should work for any kind of item.
- **Data.** Routes scenes (another item moved) with animals, fruits and names as the items, matched digits, people and slots: 300 per kind per model (9B / 27B / Muse / Lightning).
- **Method.** At the bridge word at L: the address fit on animal scenes, not refit, taken out of the change against a random part of its share, and retained alone; where that fails, the address refit per kind on a fit half and read on the other half.

- **Rule, fixed in advance.** ""An address, not an animal code" if without U cuts position answers >= 0.3 beyond random on both new item types (within 0.1 of the animal result), and only-U gives position >= 0.15. If it fails, refit U per item type and report both: the code is slot x type." The 27B and Lightning: coverage runs on this rule, no prediction.

The address fit on animals against one refit on each kind:

![The animal-fit address does not carry over to other items as ruled](../../figures/depth/ledger/20_any_item.png)

*The address on other kinds of item: the position answers cut beyond random without the address fit on animals (left) and refit on each kind (right), per model and kind. Whiskers 95% intervals; Lightning hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | position blocked without the animal-fit address, beyond random: animals / fruits / names (bar >= 0.3) | 0.44 [0.39, 0.48]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: animals :: 0.44 [0.39, 0.48] --> / 0.56 [0.51, 0.61]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: fruits :: 0.56 [0.51, 0.61] --> / 0.54 [0.48, 0.60]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: names :: 0.54 [0.48, 0.60] --> | 0.22 [0.18, 0.26]<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: animals :: 0.22 [0.18, 0.26] --> / 0.27 [0.21, 0.34]<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: fruits :: 0.27 [0.21, 0.34] --> / 0.29 [0.25, 0.34]<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: names :: 0.29 [0.25, 0.34] --> | 0.28 [0.23, 0.32]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: animals :: 0.28 [0.23, 0.32] --> / 0.39 [0.33, 0.46]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: fruits :: 0.39 [0.33, 0.46] --> / 0.25 [0.20, 0.30]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: names :: 0.25 [0.20, 0.30] --> | 0.45 [0.38, 0.51]<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: animals :: 0.45 [0.38, 0.51] --> / 0.61 [0.52, 0.70]<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: fruits :: 0.61 [0.52, 0.70] --> / 0.48 [0.43, 0.54]<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: names :: 0.48 [0.43, 0.54] --> | not run |
  | only the address retained, position: fruits / names (bar >= 0.15) | 0.35 [0.30, 0.40]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: fruits :: 0.35 [0.30, 0.40] --> / 0.35 [0.30, 0.41]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: names :: 0.35 [0.30, 0.41] --> | 0.08 [0.04, 0.11]<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: fruits :: 0.08 [0.04, 0.11] --> / 0.14 [0.10, 0.18]<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: names :: 0.14 [0.10, 0.18] --> | 0.29 [0.24, 0.35]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: fruits :: 0.29 [0.24, 0.35] --> / 0.27 [0.21, 0.32]<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: names :: 0.27 [0.21, 0.32] --> | 0.54 [0.48, 0.59]<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: fruits :: 0.54 [0.48, 0.59] --> / 0.41 [0.35, 0.47]<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: names :: 0.41 [0.35, 0.47] --> | |
  | label: fruits / names | slot x type<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: fruits :: slot x type --> / slot x type<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| qwen3.5-9b :: names :: slot x type --> | neither U nor the refit<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: fruits :: neither U nor the refit --> / slot x type<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| qwen3.6-27b :: names :: slot x type --> | slot x type<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: fruits :: slot x type --> / slot x type<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| muse-glimmer-30b :: names :: slot x type --> | slot x type<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: fruits :: slot x type --> / an address (U transfers)<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| nemotron-3.5-lightning :: names :: an address (U transfers) --> | |
  | the rule | **no<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| Q47.11 per model :: no -->** | **no<!-- src: results/x47_agnostic/x52_agnostic-20261029T023820Z/x47_11.md \| Q47.11 per model :: no -->** (no prediction) | **no<!-- src: results/x47_agnostic/x47_11-20261028T143952Z/x47_11.md \| Q47.11 per model :: no -->** | **no<!-- src: results/x47_agnostic/x52_agnostic-20261029T031638Z/x47_11.md \| Q47.11 per model :: no -->** (no prediction) | |

- **Read.**
  - On all three models the animal-fit address does not carry over as the rule asks: on the 9B it cuts fruits and names more than animals, on Muse names fall short, and on the 27B it cuts no kind by 0.3 and retained alone gives few position answers. Refit per kind, it passes for names on all three and for fruits on the 9B and Muse. On Lightning the rule also says no, though its names take the animal-fit address as it is (an address); its fruits need the refit.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Lightning's column comes from a later verdict folder that re-reads the 27B with the same rows.
  - The refit is read on half the scenes (150 per kind).

</details>

## Also failed (one line each) <a id="also-failed"></a>

The README's Part VI "Also failed" line (its cards move here); each with its verdict, no card.

- **The positive control (the 27B, chemical symbols).** The alias test's difference for the elements is 0.15 [0.10, 0.19]<!-- src: results/x4_alias/x4_patch_27b/verdict-20261024T215021Z/verdict.md \| elements :: excess (syn) - excess (same) :: 0.15 [0.10, 0.19] -->, under its bar of 0.20: it "fails: the method may not see a lookup that needs J++" (the interval rests on 6 entities).
- **A second-versus-third address.** Only the address part moves lookups between slots 1 and 2 on no model to speak of: 1 → 2 / 2 → 1, the 9B 0.00<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| qwen3.5-9b :: 1 → 2 :: 47 :: 0.00 --> / 0.00<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| qwen3.5-9b :: 2 → 1 :: 49 :: 0.00 -->, the 27B 0.00<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| qwen3.6-27b :: 1 → 2 :: 54 :: 0.00 --> / 0.00<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| qwen3.6-27b :: 2 → 1 :: 50 :: 0.00 -->, Muse 0.04<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| muse-glimmer-30b :: 1 → 2 :: 45 :: 0.04 --> / 0.16<!-- src: results/x8_write/pairs-20261026T151225Z/pairs.md \| muse-glimmer-30b :: 2 → 1 :: 51 :: 0.16 -->; the mean-difference write at twice a real change reaches 0.78<!-- src: results/x8_write/score45c-20261026T211201Z/score.md \| qwen35_9b_x8_write12 :: 2 → 1 :: 0.78 --> on the 9B (2 → 1) and 0.39<!-- src: results/x8_write/score45c-20261026T211201Z/score.md \| muse30b_x8_write12 :: 1 → 2 :: 0.39 --> on Muse (1 → 2).
- **The 9B in the clean design.** Locker first, the gap is 0.23 [0.14, 0.31]<!-- src: results/x0_necessity/x45m-20261026T230628Z/x45m.md \| qwen3.5-9b :: locker-before :: 0.23 [0.14, 0.31] -->, under the rule's 0.3.
- **The 9B's replication.** The recall is blocked at 0.12 [0.06, 0.19]<!-- src: results/x0_replicate/qwen35_9b_x0_replicate/verdict-20261024T223149Z/verdict.md \| J++ (k = 25) :: recall :: 0.12 [0.06, 0.19] --> beyond a random part: mixed.
- **The 27B's strict bar.** Its lookup is blocked at 0.14 [0.08, 0.20]<!-- src: docs/depth/x0_details.md \| 32 :: lookup :: 200 :: 0.14 [0.08, 0.20] --> beyond a random part at L32, over the rule's 0.10: not confirmed (the rule in docs/depth/x0_details.md).

## How we checked

### Do the 9B's headline runs reproduce from a clean checkout? <a id="t49-5"></a>

`in README` *Used in: README "How we checked" ("Clean-checkout reruns").*

Test 49.5 · opened 28 Oct · status: descriptive · hand-check: not in sample · files: `results/checks/clean49_9b.json` · recompute: not stated

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** Run again from one committed, clean tree, do the 9B's headline runs give the same stored answers?
- **Why we asked.** Every run of record ran from a dirty tree.
- **Data.** The 9B's main test (200), routes (300), only-U (300), zeroing (200) and the depth anatomy at L10 and L12 (200).
- **Method.** The same five commands in a fresh checkout; the stored per-item answers compared row by row.

*No figure: the record and the clean rerun side by side are the table's columns.*

- **Rule, fixed in advance.** None: descriptive, no prediction.

</details>

- **Result.** (9B; record / clean rerun)

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | main-test gap | 0.53<!-- src: docs/depth/notes/handcheck_clean49.md \| Main test gap :: 0.53 --> / 0.53<!-- src: docs/depth/notes/handcheck_clean49.md \| Main test gap :: 0.53 --> | not run | not run | not run | not run |
  | depth anatomy: position share at L12 | 0.51<!-- src: docs/depth/notes/handcheck_clean49.md \| position share under the whole change at L12 :: 0.51 --> / 0.52<!-- src: docs/depth/notes/handcheck_clean49.md \| position share under the whole change at L12 :: 0.52 --> | | | | |
  | rows compared, record / clean | main test 37600<!-- src: docs/depth/notes/handcheck_clean49.md \| qwen35_9b_clean49_x0_necessity :: 37600 -->, routes 10800<!-- src: docs/depth/notes/handcheck_clean49.md \| qwen35_9b_clean49_x6_routes` :: 10800 -->, only-U 12000<!-- src: docs/depth/notes/handcheck_clean49.md \| qwen35_9b_clean49_x6_routes_keeponly :: 12000 -->, zeroing 2000<!-- src: docs/depth/notes/handcheck_clean49.md \| qwen35_9b_clean49_x47_5 :: 2000 -->: all identical; anatomy: 38<!-- src: docs/depth/notes/handcheck_clean49.md \| route 36, switched 18, top 38 :: 38 --> of 11988<!-- src: docs/depth/notes/handcheck_clean49.md \| qwen35_9b_clean49_x47_anatomy :: 11988 --> differ | | | | |

- **Read.**
  - Four of the five runs reproduce row for row; the anatomy differs on a few rows.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The clean runs' own commit is marked dirty in the pack (90210687).
  - Source: docs/depth/notes/handcheck_clean49.md and results/checks/clean49_9b.json (point values, no intervals).

</details>

## Run on one model only (one line each)

Rows of the coverage matrix whose result exists on one model only, by design or because the other models failed the gate; no card.

- **DAS for the address (49.8, DAS by position), the 9B only by design.** A learned 4-direction position subspace carries 0.94<!-- src: results/x49_das_pos/verdict-20261028T154510Z/verdict.md \| k = 4: own-IIA 0.94 :: 0.94 --> of the position switches on held-out pairs, but holds only 0.247<!-- src: results/x49_das_pos/verdict-20261028T154510Z/verdict.md \| U's energy in R_pos 0.247 :: 0.247 --> of our address's energy and moves the recall too (cross-IIA 0.44<!-- src: results/x49_das_pos/verdict-20261028T154510Z/verdict.md \| the recall's cross-IIA 0.44 :: 0.44 -->): "(d) in between". Its figure: [the verdict folder](../../results/x49_das_pos/verdict-20261028T154510Z/qwen35_9b_x49_das_pos.png).

## Withdrawn

### Does the split hold when the fact passages' bridge is described? <a id="z2"></a>

`in README` *Used in: README "Tested and dropped" ("The described bridge on the fact passages").*

Test Z2 · opened 28 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x52_coverage/matrix-20261029T122040Z/matrix.json` · recompute: `scripts/x52_coverage.py` (the command in its docstring) · also: withdrawn; Lightning's coverage run 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** On the fact passages with a described (never named) bridge, does the lookup let go of the lens part?
- **Why we asked.** A described bridge must be computed before it can be used; the computed item could travel through the lens.
- **Data.** His described-bridge passages: 158 / 166 / 157 (below the 200 aimed for) / 200<!-- src: results/x50_zach/x52_z2-20261029T025625Z/z2.md \| nem35l_x52_z2 :: 200 (124) :: 200 --> (Lightning, at L14; L27 beside).
- **Method.** The conflict test at the description's last token at L, each reader its own change, against a random part.

- **Rule, fixed in advance.** "Per model, the 47.3 rule: (a) the split holds: gap >= 0.3, lookup <= 0.10; (a') the computed bridge is handed through the lens: lookup >= 0.20; (d) in between." Withdrawn by the answer control's rule ([51.12](#t51-12)): the lens effect there is the answer or mixed in all four cells.

Both operations' gaps on the described bridge:

![The breadth track's removal everywhere hits the recall more; the depth track's gap is unclear](../../figures/depth/ledger/21_described_gap.png)

*The fact passages with the bridge described: the gap, recall minus lookup, under the change at one layer (left, a share of switches) and under removal everywhere (right, a share of answers); the 122B not run at one layer. Whiskers 95% intervals; Lightning and the 122B hollow ○.*

</details>

- **Result.**

  | | 9B | 27B | Muse (L26) | Lightning (L14) | 122B |
  |---|---|---|---|---|---|
  | lookup: switches blocked beyond a random part | 0.54 [0.43, 0.66]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| qwen35_9b_x50_z2 :: 0.54 [0.43, 0.66] --> | 0.69 [0.52, 0.87]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| x50_z2_27b :: 0.69 [0.52, 0.87] --> | 0.67 [0.00, 1.00]<!-- src: results/x50_zach/z2-20261028T162710Z/z2.md \| muse30_x50_z2 :: 0.67 [0.00, 1.00] --> | 0.51 [0.38, 0.63]<!-- src: results/x50_zach/x52_z2-20261029T025625Z/z2.md \| nem35l_x52_z2 :: 0.51 [0.40, 0.62] :: 0.51 [0.38, 0.63] --> | 0.48 [0.36, 0.60]<!-- src: results/x50_zach/x52_z2-20261030T045145Z/z2.md \| qwen35_122b_z2 :: 192 (121) :: 0.48 [0.36, 0.60] --> (L33) |
  | the rule (before withdrawal) | (a') through the lens | (a') through the lens | (a') through the lens | (a') through the lens (no prediction) | (a') through the lens (no prediction; L39: can't tell) |

- **Read.**
  - Withdrawn: at the description's last token the lens part moves the answer, so removing it is not a test of the bridge.

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - Muse's lookup switches under the whole change on 0.02 of passages; Lightning's L27 cell rests on 15<!-- src: results/x50_zach/x52_z2-20261029T025625Z/z2.md \| L27: routes :: "original": 184, "switch": 15 :: 15 --> lookup switches (under 30) and is not valid.
  - n below the 200 aimed for on the first three models. Lightning's run reads the design the README withdrew (Part VI) and stands under the same withdrawal; its own answer control (coverage run, no prediction) says mixed for both readers: without the answer directions only, the lookup is blocked at 0.29 [0.16, 0.44]<!-- src: results/x51_answer/x52_answer-20261029T080050Z/verdict.md | z2 :: nemotron-3.5-lightning :: lookup :: 0.29 [0.16, 0.44] --> and the recall 0.38 [0.26, 0.52]<!-- src: results/x51_answer/x52_answer-20261029T080050Z/verdict.md | z2 :: nemotron-3.5-lightning :: recall :: 0.38 [0.26, 0.52] --> beyond a random part.

</details>

## Operations during the sprint <a id="operations"></a>

Moved to [docs/review/ledger_ops_2026-10.md](../review/ledger_ops_2026-10.md) on 7 Nov, verbatim: the 122B coverage runs of the night of 29-30 Oct; the runs not completed in the sprint (batch 52 C); the items flagged for a decision during the sprint (old Appendix A); the README changes proposed during the sprint (old Appendix B); the checks of the retired ledger figures (old Appendix D).

## Appendix C. Coverage table <a id="coverage"></a>

<details><summary>Coverage table</summary>

Which test ran on which model, from the committed coverage matrix (results/x52_coverage/matrix-20261029T122040Z/matrix.json, built 12:20 UTC 29 Oct; each cell's source is in that file). Rows in the README's order, under their Part; a linked test has a card above. Each cell is a symbol (legend under the table) and, where the matrix has a note for it, a number pointing to that note. Lightning's gate (all its cells): the main test's gate on all 516 scenes, chosen after the 60-scene pre-check was seen (its cells are read as hollow); layer L14 (see [Lightning's layer](#lightning-layer)). Nemotron 3.5 Bolt: out of scope, only a J-lens exists, no J++ lens.

As of the matrix at 12:20 UTC (13:20 Paris; 8e2ef0cb: 47.15's row renamed "One question, two sources"; otherwise as b8a24aab: 161 done, 20 not tested, 9 not designed, 6 partial, none missing; 47.15 on the 9B and 47.7 (a) on the 9B and Muse now read "not tested" from their r2 reruns' failed gates, as flag 26). The 122B is not in the matrix; its cells are in the cards and the heatmap. Results opened since then are in their cards and the heatmap; the matrix has no rows for batch 53 or for the fact passages.

<!-- coverage:start (scripts/ledger_coverage.py; do not edit by hand) -->
| test | 9B | 27B | Muse | Lightning |
|---|---|---|---|---|
| **Part I. The two readers** | | | | |
| [1. Conflict test (main test, at L)](#lightning-conflict) | ✓ <sup>1</sup> | ✓ <sup>2</sup> | ✓ <sup>1</sup> | ✓ <sup>3</sup> |
| [2. Answer control (51.12 E1)](#t51-12) | ✓ <sup>4</sup> | ✓ <sup>4</sup> | ✓ <sup>5</sup> | ✓ |
| [Split in other texts: varied scenes (x0b)](#x0b) | ✓ | ✓ | ✓ | ✓ |
| [Split in other texts: natural passages (x5)](#x5) | ✓ <sup>6</sup> | ✓ | ✓ | ○ <sup>7</sup> |
| [Dose curves, a part alone (51.1)](#t51-1) | ✓ | ✓ | ✓ | ✓ |
| [Zeroing at one layer (47.5)](#t47-5) | ✓ | ✓ | ✓ | ✓ <sup>8</sup> |
| [7. Ladder (49.2, rungs 1-6)](#t49-2) | ✓ | ✓ <sup>9</sup> | ✓ <sup>10</sup> | ○ <sup>11</sup> |
| [Earlier mention (45p)](#t45p) | ✓ | ✓ | ✓ | ○ <sup>11</sup> |
| [Gain map (49.1)](#t49-1) | ✓ | ✓ | ✓ | ✓ |
| **Part II. Identity** | | | | |
| [E3: identity route outside the lens (47.1 atom slices)](#t47-1) | ✓ | ✓ | ✓ | ✓ |
| [3. Routes test (identity / position / value; no address; address alone)](#routes) | ✓ | ✓ <sup>12</sup> | ✓ | ✓ |
| [What is left of the route; the value (47.7)](#t47-7c) | ○ <sup>13</sup> | ✓ | ○ <sup>13</sup> | ◐ <sup>14</sup> |
| [Learned subspaces (48 DAS; 51.3 DAS at scale)](#t51-3) | ✓ | ✓ <sup>15</sup> | ✓ | – <sup>16</sup> |
| **Part III. The address** | | | | |
| [E6: the address probe (x0_probe v4)](#probe) | ✓ | ✓ | ✓ | ✓ |
| [4. Address swap by dose (x8_write, s = 1 / 2 / 4)](#swap) | ✓ <sup>17</sup> | ✓ <sup>18</sup> | ✓ <sup>19</sup> | ✓ <sup>20</sup> |
| [E6: the swap after neutral sentences (47.16 distance)](#t47-16) | ✓ | ✓ | ✓ <sup>21</sup> | ✓ |
| [E7: six lockers, one code per slot (47.2)](#six) | ✓ | ✓ | ✓ | ✓ |
| [What is the address: dimension, methods, geometry (51.11)](#t51-11) | ✓ | ◐ <sup>22</sup> | ✓ | – <sup>16</sup> |
| [8. Lens readout with the item-change control (47.0)](#t47-0) | ✓ | ✓ | ✓ | ✓ |
| [E8: the report prompt (47.10)](#t47-10) | ○ <sup>23</sup> | ✓ | ○ <sup>24</sup> | ○ <sup>25</sup> |
| [Report of slot 1, reworded (49.6)](#t49-6) | ✓ <sup>26</sup> | ✓ | ✗ <sup>27</sup> | ✓ <sup>28</sup> |
| [Joint head ablation under the swap (51.2)](#t51-2) | ✓ | ✓ | ✓ | ✓ |
| [10. Attention under the swap (49.7)](#t49-7) | ✓ | ✓ | ✓ | ✓ <sup>29</sup> |
| [Chained addresses (47.14)](#t47-14) | ✓ | ✓ | ✓ | ○ <sup>30</sup> |
| [Address refit per text format (x45d)](#x45d) | ✓ | ✓ | ✓ | ✓ |
| **Part IV. Where and when** | | | | |
| [5a. Order split (descriptive)](#order) | ✓ | ✓ | ✓ | ✓ <sup>31</sup> |
| [5b. Copy test (45q)](#t45q) | ✓ <sup>32</sup> | ✓ <sup>32</sup> | ✓ <sup>32</sup> | ○ <sup>11</sup> |
| [E11: token by layer map (47.D1)](#d1) | ✓ | ✓ | ✓ | ◐ <sup>33</sup> |
| [E11: lookups carried before L (47.4 cumulative)](#t47-4) | ✓ | ✓ | ✓ | ◐ <sup>34</sup> |
| [6. Anatomy by layer (47.8)](#t47-8) | ✓ | ✓ <sup>35</sup> | ✓ | ✓ <sup>36</sup> |
| [E12: address persistence across depth (D4, CPU)](#t47-8) | ✓ | ✓ <sup>37</sup> | ✓ | ✓ <sup>38</sup> |
| [The address at the last token (51.4)](#t51-4) | ✓ | ✓ | ✓ | ✓ |
| [9. Last-token read / write (51.10)](#t51-10) | ✓ | ✓ | ✓ | ✓ |
| **Part V. Other datasets** | | | | |
| [Part V: the fact passages Z1 / Z2 (x50)](#z1) | ✓ | ✓ | ✓ | ✓ <sup>39</sup> |
| [Z1 on the full carrier (51.7)](#t51-7) | ✓ | ✓ | ✗ <sup>27</sup> | ✓ |
| [Part V: the fact passages Z3 (routes on the fact passages)](#z3) | ✓ | ✓ <sup>40</sup> | ✓ | ✓ <sup>41</sup> |
| [Anatomy on the fact passages (51.5)](#t51-5) | ✓ | ✓ | ✗ <sup>27</sup> | ✗ <sup>42</sup> |
| **Part VI. What did not hold** | | | | |
| [Described bridge (47.3, and 51.12's cue r2)](#t47-3) | ✓ | ✓ | ◐ <sup>43</sup> | ○ <sup>44</sup> |
| [One question, two sources (47.15)](#t47-15) | ○ <sup>13</sup> | ✓ | ○ <sup>45</sup> | ○ <sup>13</sup> |
| [The lookup's errors are not address errors (47.13)](#t47-13) | ✓ | ✓ | ✓ | ✓ <sup>46</sup> |
| [Failed: the lens part keys the attribute; late MLPs (48.2 enrichment)](#t48-2) | ✓ | ✓ <sup>47</sup> | ✓ | ◐ <sup>48</sup> |
| [Failed: a person mark at the locker sentence (48.3 bind)](#t48-3) | ✓ | ✓ | ✓ | ○ <sup>49</sup> |
| [Pooled person probe (49.3)](#t49-3) | ✓ | ✓ | ✓ | ○ <sup>50</sup> |
| [Failed: copying heads pass the rest (48 heads)](#t48-4) | ✓ | ✓ | ✓ | ✓ <sup>51</sup> |
| [Failed: the address as the recall's second route (48 route2)](#t48-5) | ✓ | ✓ | ✓ | ○ <sup>52</sup> |
| [Failed: blocking the pick sentence (47.6 edges)](#t47-6) | ✓ | ✓ | ✓ | – <sup>53</sup> |
| [Failed: the address is the same for any kind of item (47.11 agnostic)](#t47-11) | ✓ | ✓ | ✓ | ✓ |
| **Withdrawn, or run on one model only** | | | | |
| DAS by position (49.x das_pos) | ✓ | ✗ <sup>54</sup> | ✗ <sup>54</sup> | ✗ <sup>54</sup> |
| [Answer-direction control on the fact passages' Z2 (51.12 Z2)](#z2) | ✓ | ✓ | ✗ <sup>27</sup> | ✗ <sup>42</sup> |

✓ done, ◐ partial, ○ below the model's gate (not tested; a below-gate run is exploratory), – not tested (including missing, not completed or queued), ✗ not designed for that model; a number points to the matrix's note for that cell, listed under the table.

1. confirmed
2. not confirmed (lookup 0.14 > 0.10; recall 0.74)
3. decided at L14; 3 arms at all 13 swept layers
4. recall: the entity
5. answer word not read
6. gate lowered after the data
7. its gate failed ({'PP': 0.7701149425287356, 'PM': 0.896551724137931}, eligible 36); no lowered rerun (the spec's rule)
8. L14 and L14..17; the 60 dev scenes kept out
9. rungs 1-6, rung 6 at the breadth track's L32-40
10. rung 6 in the breadth track's L36-42 (49.2 ran it at L23-29)
11. the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change)
12. 0.66 / 0.34 / 0.00; alone fails
13. its gate failed (no placement / condition passed; see gate.json); no lowered rerun (the spec's rule)
14. (a) not tested (its gate failed (no placement / condition passed; see gate.json); no lowered rerun (the spec's rule)); (c) done
15. 51.3 done; 48.1 done
16. DAS trains through the model's backward, unverified through NemotronH's Mamba-2 kernels; its recall half needs the clean design (gate fails)
17. target share at s = 1 / 2 / 4: 0.02 / 0.46 / 0.73
18. target share at s = 1 / 2 / 4: 0.01 / 0.24 / 0.50
19. target share at s = 1 / 2 / 4: 0.05 / 0.52 / 0.52
20. target share at s = 1 / 2 / 4: 0.03 / 0.50 / 0.69
21. x47_16_muse was cancelled by Dan mid-run (batch 49 amendment 1; no outcomes); r2 re-opens it under amendment 2 (flagged)
22. part 2 only by design (parts 1, 3 not designed for the 27B)
23. the cited verdict lists 9B as not tested (results/x47_report/x47_10-20261028T113109Z)
24. the cited verdict lists Muse as not tested (results/x47_report/x47_10-20261028T113109Z)
25. the cited verdict lists Lightning as not tested (results/x47_report/x52_report-20261029T023828Z)
26. the deciding model
27. designed for the 9B and 27B (conservative, Dan 01:10)
28. the 9B / 27B design; read per model, the action is the 9B's
29. attention blocks 19 / 26 / 33 / 42 after L14 (6 of 52 blocks)
30. the cited verdict lists Lightning as not tested (the gate missed (see gate.json); results/x47_chain/x52_chain-20261029T023424Z)
31. CPU from the conflict test's outcomes
32. holds
33. the main design only; the clean design (the decisive cell) not tested: gate fails
34. the main design only; the clean design not tested: gate fails
35. full grid
36. every 4th layer L2-L50
37. CPU from x47_anatomy_27b's cache
38. CPU from Lightning's anatomy cache (on its box)
39. Z1 done; Z2 done
40. at L32 (X0's layer = the start of his band L32-40)
41. at L14 and L27
42. the test was designed for the 9B and 27B; amendment 2's grid adds no new design
43. 47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design)
44. the cited verdict lists Lightning as not tested (gate: O's read accuracy {'PP': 0.7228571428571429, 'PM': 0.87} (bar 0.8), eligible 301; results/x47_cue/x52_cue-20261029T023827Z); was: 47.3 done; 51.12 cue r2 queued (x52_lightning_cue_answer (not completed in the sprint; no ledger entry here))
45. the cited verdict lists Muse as not tested (the gate failed; results/x47_source/x47_15-20261028T142722Z)
46. count (CPU) then the verdict
47. A and B
48. A only; B not tested: it ablates each block's MLP and NemotronH has none (MoE blocks are separate)
49. the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (48.3 reads the 45m scenes too)
50. the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (49.3 reads the 45m scenes)
51. attention blocks after L14 (NemotronH port)
52. the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (route2 reads the 45m scenes)
53. the edge knock-out (knockout.py) is not ported to NemotronH's Mamba-2 blocks
54. 9B only by design
<!-- coverage:end -->

</details>
