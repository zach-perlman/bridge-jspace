<!-- grid: results/cross_model/20261023T105852Z -->
# bridge-jspace

**The question.** A two-step question makes a model find an entity in between, the **bridge**, and then use it. A **J-lens** reads hidden states as words. Does the model use the bridge in the form the lens reads, or by another route?

> "Which locker belongs to the animal known for oinking?" The bridge is *pig*. The answer is the pig's locker number, stated in the prompt.

**How to read this page.** Confidence words follow one fixed rule ([below](#confidence-and-verification)): strong, medium, open. "Verified" says who recomputed a number: a person, an independent agent, or nobody yet. Every number comes from the cross-model grid ([grid.md]({{grid}}/grid.md)) unless a run is named next to it; every run is in [RUNS.md](RUNS.md).

> **Status, 23 Oct 2026.** Built at {{head}} from `{{grid}}`. Exploration phase: no main claim is hand-verified yet. An independent agent recomputed claims 1-3, and claim 6 on the 27B, from raw rows: every cell matches. The hand check is today. Running on the A100: Gemma 4's lens tests, Qwen3-32B's tables and JSON, the 27B dose control. On the 122B the lookup follows the J-space form to a later layer than on the other models ([below](#the-122b-difference)); its test runs today on a rented 2x H100.

Eight models. Hybrids, which mix attention with DeltaNet layers: Qwen3.6-27B (27B), Qwen3.5-9B (9B), Olmo-Hybrid-7B (Olmo-Hybrid), Qwen3.5-122B (122B). Attention-only: Qwen3-32B (32B), OLMo-3-7B (OLMo-3), Muse 30B (Muse), Gemma 4 31B (Gemma).

## Words

| Word | Meaning |
|---|---|
| bridge | The entity found in the first step: "the animal known for oinking" → pig |
| lookup / recall | The answer comes from a sentence in the prompt / from the model's memory |
| J-lens, J-space | A tool that reads hidden states as words ([Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/index.html)) / the part of a hidden state it reads |
| lens-readable part | The part of a change in hidden states that lies in the J-space |
| lens push | Adding the lens's direction from one word to another (pig → cow) to a hidden state |
| patch | Copying hidden states from another prompt into this one, at chosen tokens and one layer |
| valid cell | A test point where the push or patch leaves questions off the bridge's path almost unchanged (at most 10% of them change) |
| blocking | Stopping chosen tokens from attending to one sentence |
| last tokens | The chat-template tokens after the user's text, up to the answer: 11 on the Qwen models, 7 on OLMo-3, as in every blocking run. Claim 3's patch copies only the last two |
| relay | A route around a block: the answer reaches the last tokens through other tokens that still see the sentence |
| positive control | A place where a method is known to work, so that a null result elsewhere means something |
| scene set | A fresh batch of generated prompts with new lists and entities, drawn with a fixed seed |

## Main claims

| Claim | Evidence | Holds on | Confidence | Verified | Details |
|---|---|---|---|---|---|
| **How a lookup works** | | | | | |
| The last tokens read the answer's sentence late, through attention, and take its digit | Blocking that read leaves {{v|f4|27b|draw 2}} right on the 27B; with no other route the right null is near zero, not the guessing rate | {{holds|f4}} models under the old bar; Gemma and the 27B's long text: relay, v2 pending; Olmo-Hybrid's tables miss by one item | medium | [agent re-check](verification/agent_check_finding4.md), [and](verification/agent_check_finding3.md) | [1](#1-the-last-tokens-read-the-answer-late-through-attention) · [2](#2-they-take-the-answers-digit-not-the-entitys-name) |
| An order label picks the 1st and 2nd sentence; the bridge's identity picks the rest | On the 27B the label leads by {{v|f5|27b|draw 2}} (1st-2nd / later) | {{holds|f5}} models; 32B mixed | medium | [agent re-check](verification/agent_check_finding5.md) | [3](#3-an-order-label-picks-the-1st-and-2nd-sentence-the-bridges-identity-the-rest) |
| **What the J-space does and doesn't carry** | | | | | |
| *Methods note, not a finding:* the lens reads a stated bridge at its own word | On the 27B: {{v|gate|27b|v1 (at the word)}} at the word, {{v|gate|27b|v2 (after the word)}} right after it; no logit-lens or embedding baseline yet | {{count|gate|v1 (at the word)|holds}} lensed models at the word, {{count|gate|v2 (after the word)|holds}} after it | – | none | [4](#4-methods-note-the-lens-reads-a-stated-bridge-at-its-own-word) |
| A lens push at the bridge's word writes recall; the lookup ignores it from layer {{q|20}} on (27B), {{q|6}} (9B, OLMo-3), {{q|33}} (122B) | On the 122B at layer 33: {{v|f7|122b|main rule}} of lookups move, {{ctl|f7|recall|122b|main rule}} of recalls; at layer 27, {{q|26%}} of lookups ([per layer](#5-a-lens-push-writes-recall-the-lookup-ignores-it-from-a-models-own-layer-on)) | {{holds|f7}} models with a valid test | medium | none | [5](#5-a-lens-push-writes-recall-the-lookup-ignores-it-from-a-models-own-layer-on) |
| The lens-readable part of a stated bridge moves recall, not the lookup | On the 27B it moves {{ctl|f2|recall|27b|draw 2}} of recalls and {{v|f2|27b|draw 2}} of lookups; taken out of the change, it costs recalls {{q|51}} points and lookups {{q|2}}; on the 122B it moves {{v|f2|122b|draw 2}} of lookups | {{holds|f2}} models; fails on the 122B at layer 24 ([why](#the-122b-difference)) | medium | [agent re-check](verification/agent_check_finding2.md) (27B) | [6](#6-the-lens-readable-part-of-a-stated-bridge-moves-recall-not-the-lookup) |
| Lookups don't need the J-space; how much recall needs it varies | Zach's rule on the 27B: recall loses {{v|f1|27b|tasks, Zach's rule}} more than lookups | {{q|4 of 4}} in Zach's runs, three of them quoted and not yet in this repo; ours descriptive | medium | none | [7](#7-lookups-dont-need-the-j-space-recall-does-to-a-varying-degree) |

![Every claim on every model](figures/cross_model/f_summary_heatmap.png)

Every cell, its n and its interval: [grid.md]({{grid}}/grid.md).

## A band where the lookup needs the word but not its J-space form

Dan's main J-space claim, read from runs already opened (not yet a grid rule): *at the stated bridge's word there is a band of layers where the lookup still depends on that position (the full patch at the word moves it), but not on the bridge's J-space form (the lens push moves no lookups), while a lens push there still writes recall.*

| Model | Band (layers) | Full patch at the word → lookups | Lens push → lookups (valid cells; where, size) | Lens push → recalls (the same cells) | Runs |
|---|---|---|---|---|---|
| 27B | {{q|20-26}} | {{q|65% at layer 20 → 24% at 26}} | {{q|0%}} (word 4x; sentence 8x); at the word the 8x push fails the off-path check at every band layer | {{q|6-41%}} (word 4x), {{q|65-93%}} (sentence 8x) | [patch and push, same scenes](results/early_push_where/d4_layer_gap_v2_27b/summary.json) |
| 9B | {{q|6-16}} (the sweep starts at 6) | {{q|74% → 17%}} | {{q|0%}} at every valid cell, word and sentence; the 8x push is valid only at layer 6 | up to {{ctl|f7|recall|9b|main rule, draw 2}} (sentence, layer 12, 4x, scene set 2); scene set 1 stays under the recall bar | [map](results/statement_positions/qwen35_9b_d1_topics2_map/summary.md) · [push 1](results/early_push_where/qwen35_9b_d4_where/summary.json) · [push 2](results/early_push_where/qwen35_9b_d4_where_fresh_seed2/summary.json) |
| OLMo-3 | {{q|6-14}} | {{q|53% → 16%}} | {{q|0%}} at the word (8x valid at 6, 8, 14), at most {{q|2%}} at the sentence | up to {{ctl|f7|recall|olmo|main rule}} (word, layer 14, 8x) | [map](results/statement_positions/olmo3_7b_instruct_jpp_d1_topics2_map/summary.md) · [push](results/early_push_where/olmo3_7b_instruct_jpp_d4_where_raw/summary.json) |
| 122B | {{q|33}} (the last layer swept) | {{q|44%}} | {{v|f7|122b|main rule}} (word 8x); {{q|1%}} (sentence 8x) | {{ctl|f7|recall|122b|main rule}} (word 8x) | [map](results/statement_positions/qwen35_122b_d1_topics2_map/summary.md) · [push](results/early_push_where/qwen35_122b_d4_where/summary.json) |

- **Different scenes.** The maps use one kind of scene set (several topics), the pushes another (animals), except on the 27B, where the patch and the push ran on the same scenes. On the 27B's map the full patch at the word still moves {{q|48%}} of lookups at layer 28 ([map](results/statement_positions/d1_topics2_map_27b/summary.md)), where it moves {{q|0%}} on the push's scenes: where the band ends depends on the scenes.
- **Size.** The full patch is not size-matched to the push, and in the 27B's band only the smaller push passes the off-path check at the word, so the push may stop because it is weak. Size-matched tests are pending (their predictions are committed).
- **The 122B at layer 30.** At the word the push moves {{q|0%}} of lookups there too (recalls {{q|74%}}), but at the sentence it still moves {{q|18%}}, and so does the lens-readable part ([next section](#the-122b-difference)); only layer 33 is clean on both.
- **Valid cells only.** An earlier draft used cells that fail the off-path check (OLMo-3's {{q|89%}} of recalls at the word, layer 12, 8x).
- Prior work: the workspace paper (Gurnee et al. 2026) and two-hop recall resolving its bridge early (Biran et al., EMNLP 2024): [docs/prior_art.md](docs/prior_art.md#3-a-band-of-layers-where-the-lookup-ignores-the-lens-readable-form).

## The 122B difference

- **What we saw.** On the 122B the lookup follows the bridge's J-space form through layer 30 and not at 33. The lens push at the bridge's sentence moves {{q|26%}} of lookups at layer 27 and {{q|18%}} at 30 (recalls {{q|84%}}, {{q|83%}}; valid cells, [run](results/early_push_where/qwen35_122b_d4_where/summary.json)); at layer 33 it moves {{v|f7|122b|main rule}} at the word. The lens-readable part of a stated bridge moves {{v|f2|122b|draw 2}} of lookups at layer 24 (the grid's test point, the whole prompt) and still {{q|16%}} (sentence) and {{q|19%}} (whole prompt) at layer 30 ([run](results/statement_positions/qwen35_122b_d1_topics2_parts/outcomes.jsonl)).
- **Reading.** A difference in how long the lookup uses the J-space form, not a counter-example to the band above: the 122B's band starts later.
- **The late-switch test** (rule fixed before the run; called "late binding" until 23 Oct, logic unchanged): the lens-readable part at the bridge's sentence and the whole prompt at layers 30, 33 and 36, with a random part of the same share as a control. Layer 30 is already measured (above), so 33 and 36 decide. The late switch holds if the lens part goes quiet on lookups (upper bound ≤ 5%), stays quiet later, and still moves recalls. Claim 6 fails on the 122B if the lens part moves at least 20% of lookups at every later point. It runs today on a rented 2x H100.
- **Also possible.** The 122B runs in FP8, while its lens was fit on bf16 weights. It is also the only mixture-of-experts model here (about 10B parameters active per token), so a difference may come from its experts rather than its size.

## Findings

### 1. The last tokens read the answer late, through attention

**Confidence:** medium under the old rule (holds {{holds|f4}}); Gemma and the 27B's long text read as a relay, v2 pending; Olmo-Hybrid's tables miss by one item. **Verified:** [agent re-check](verification/agent_check_finding4.md), every cell matches; hand check pending.

**What we did**
- Stopped the last tokens from attending to the answer's sentence, in every attention layer.
- Counted the answers still right.

**Rules.** Old (late-read, fixed 22 Oct): at most 20% right with an upper bound of at most 30% (the guessing rate of a five-item list), while hiding another sentence keeps at least 90%. New (late-read v2, beside the old rule, being added to the grid): with the sentence hidden and no other route, the right null is near zero, not the guessing rate. Until v2 is in the grid, a cell above the old bar reads "relay; v2 pending".

{{table|f4|draw 2|draw 1|draw 3|table}}

Gemma's and the 27B's long-text "fails" above are the old rule's; read them as a relay, v2 pending.

**The relay.** Blocking more tokens leaves fewer answers right:
- Gemma, scene set 1: {{v|f4|gemma|draw 1}} with the last tokens blocked, {{q|15%}} with the question's tokens blocked too, {{q|2%}} with every token after the sentence blocked ([run](results/attn_knockout/gemma4it_d2_v4_late_read_v3_r2/rows.jsonl)). Gemma's other runs have no such arms.
- The 27B's long text: {{v|f4|27b|long context}}, then {{q|11%}} with the question's tokens blocked too ([run](results/attn_knockout/d2_late_read_long_27b_r3/rows.jsonl)); blocking the DeltaNet layers instead keeps {{ctl|f4|DeltaNet|27b|long context}}.

**Controls**
- Another sentence blocked instead keeps {{ctl|f4|another sentence}} right.
- On the hybrids, blocking the DeltaNet layers instead keeps {{ctl|f4|DeltaNet}} right.

**Weak spots**
- The long text is neutral filler, not a real document. A natural-text test is designed and waits for approval.
- The 27B's long text keeps {{q|11%}} even with the question blocked; no run blocks every token after the sentence there.

**What it means.** On every model the lookup ends in an ordinary attention read of the answer's sentence; where some answers survive the block, they come through other tokens.

Prior work: retrieval heads (Wu et al., ICLR 2025), the recall gap of recurrent layers (Zoology, Arora et al., ICLR 2024; Bick et al., ICML 2025): [docs/prior_art.md](docs/prior_art.md#1-a-lookup-ends-with-a-late-attention-read-of-the-answers-sentence).

![Blocking the read](figures/cross_model/f_late_read_all_models.png)

### 2. They take the answer's digit, not the entity's name

**Confidence:** {{conf|f3}}. **Verified:** [agent re-check](verification/agent_check_finding3.md), every cell matches; hand check pending.

**What we did**
- Hid part of the answer's sentence from the last tokens: everything except its name, or everything except its digit.

{{table|f3|draw 2|draw 1|draw 3|table}}

**Controls**
- With the digit left visible instead, the 27B keeps {{ctl|f3|digit visible|27b|draw 2}} right.
- Hiding the same parts of another sentence keeps {{ctl|f3|another sentence}} right.

**Weak spots**
- Gemma's split is weaker than the others'.
- Why the question's words read the name is not tested.

**What it means.** The last tokens fetch the answer's digit; the name is looked up earlier.

Prior work: lookbacks, an address then a payload (Prakash et al., ICLR 2026): [docs/prior_art.md](docs/prior_art.md#1-a-lookup-ends-with-a-late-attention-read-of-the-answers-sentence).

![Digit, not name](figures/cross_model/f_digit_not_name_all_models.png)

### 3. An order label picks the 1st and 2nd sentence, the bridge's identity the rest

**Confidence:** {{conf|f5}}. **Verified:** [agent re-check](verification/agent_check_finding5.md), every cell matches; hand check pending.

**What we did**
- Two prompts list the same entities in a different order. We patched the last tokens from one into the other at one layer.
- Each possible answer is a different digit, so the answer shows what the patched tokens pointed to.
- Rule fixed in advance: the place must win for the 1st and 2nd sentence; the identity must tie or win after that.

{{table|f5|draw 2|draw 1|draw 3|8 sentences}}

The numbers are two leads in points: place over identity for the 1st-2nd sentence, identity over place for the rest.

**How the label counts (open).** With a filler sentence moved, the label follows the order in the list on {{count|f6|filler moved|holds}} models. With one sentence more or fewer, it does so on {{count|f6|one statement more|holds}}.

**Weak spots**
- One layer per model; the 27B's was chosen after its first runs.
- The identity lead is modest on the larger Qwens.

**What it means.** This matches lookback work in the middle of the list and differs at its end. It also holds when the bridge is recalled.

Prior work: binding IDs (Feng & Steinhardt, ICLR 2024), ordering IDs (Dai et al., EMNLP 2024); Mixing Mechanisms (Gur-Arieh et al., ICLR 2026) finds a last-position peak that we do not see: [docs/prior_art.md](docs/prior_art.md#2-which-sentence-is-read-an-order-label-then-the-entitys-identity).

![Order, then identity](figures/cross_model/f_order_then_identity_all_models.png)

### 4. Methods note: the lens reads a stated bridge at its own word

**Not a finding.** The lens names the stated bridge at its own word on {{count|gate|v1 (at the word)|holds}} lensed models (v1) and right after it on {{count|gate|v2 (after the word)|holds}} (v2). Without a logit-lens or embedding baseline at the same cells, this describes the tool, not the model. **Verified:** none.

How it was read: the bridge must be in the lens's top 10 on at least half of the items, the other bridge (which reaches it on {{ctl|gate|other bridge}} of items) on at most a fifth. Every lens is a J++ fit (published, Zach's, or ours for the 32B and OLMo-3); per-model numbers and other lenses: [grid.md]({{grid}}/grid.md).

**The J-space without the bridge's own word.** In claim 6's runs we also pasted the lens-readable part with the bridge's own word (and the other bridge's) taken out first. At claim 6's test points:

| Model | Lookups moved | Recalls moved | Same-share random part: lookups / recalls | Runs (scene set 1, scene set 2, tables and JSON) |
|---|---|---|---|---|
| 27B | {{q|0-2%}} | {{q|6-14%}} | {{q|0% / 0-2%}} | [1](results/statement_positions/d1_topics_parts_27b/outcomes.jsonl) · [2](results/statement_positions/d1_topics2_parts_27b/outcomes.jsonl) · [3](results/statement_positions/d1_formats_parts_27b/outcomes.jsonl) |
| 9B | {{q|0%}} | {{q|17-18%}} | {{q|0-1% / 2-7%}} | [2](results/statement_positions/qwen35_9b_d1_topics2_parts/outcomes.jsonl) · [3](results/statement_positions/qwen35_9b_d1_formats_parts/outcomes.jsonl) |
| 122B | {{q|0-1%}} | {{q|1-2%}} | {{q|1% / 2%}} | [2](results/statement_positions/qwen35_122b_d1_topics2_parts/outcomes.jsonl) · [3](results/statement_positions/qwen35_122b_d1_formats_parts/outcomes.jsonl) |

The whole lens-readable part moves {{ctl|f2|recall}} of recalls across models and settings (claim 6).

Prior work: the J-lens and the workspace (Gurnee et al. 2026): [docs/prior_art.md](docs/prior_art.md#3-a-band-of-layers-where-the-lookup-ignores-the-lens-readable-form).

### 5. A lens push writes recall; the lookup ignores it from a model's own layer on

**Confidence:** {{conf|f7}}. **Verified:** none.

**What we did**
- Pushed the hidden state at the stated bridge's word or sentence toward another animal's word, over layers and sizes.
- Picked the test point on recall alone, then read the lookups there.

{{table|f7|main rule, draw 2|main rule|amended rule}}

**Per layer.** The lookup stops following the push from layer {{q|20}} on the 27B, from {{q|6}} (the first layer swept) on the 9B and OLMo-3, and at {{q|33}} on the 122B, where it still follows at 27-30 (table below).

<details><summary>Lookups and recalls the push moves, per layer (valid cells only)</summary>

Each entry: the layer, then the largest share of lookups / of recalls switched over that layer's valid cells (the word or its sentence, any size), in %. † some cells at that layer fail the off-path check and are left out; – no valid cell; bold: a valid cell moves lookups (lower bound over 5%).

| Model, run | Per layer: lookups / recalls |
|---|---|
| 27B, scene set 1 ([run](results/early_push_where/d4_where_fresh_27b/summary.json)) | {{q|L12 0/14 · **L16 30/84** · L20 0/69† · L24 0/47† · L28 0/70† · L32 0/40† · L36 0/65 · L40 0/4 · L44 0/7}} |
| 27B, scene set 2 ([run](results/early_push_where/d4_where_fresh_seed2_27b/summary.json)) | {{q|L12 0/18 · **L16 19/83** · L20 0/65† · L24 0/84† · L28 0/65† · L32 0/34† · L36 0/59 · L40 0/1 · L44 0/2}} |
| 27B, layer gap, 4x and 8x ([run](results/early_push_where/d4_layer_gap_v2_27b/summary.json)) | {{q|L12 0/18 · L14 9/67 · **L16 19/83** · **L18 11/76** · L20 0/65† · L22 0/10† · L24 0/84† · L26 0/93† · L28 0/65† · L30 –† · L32 –† · L34 –†}} |
| 9B, scene set 1 ([run](results/early_push_where/qwen35_9b_d4_where/summary.json)) | {{q|L6 0/26 · L8 0/5† · L10 0/7† · L12 0/2† · L14 0/10† · L16 0/18† · L18 0/14† · L20 0/2† · L22 0/13†}} |
| 9B, scene set 2 ([run](results/early_push_where/qwen35_9b_d4_where_fresh_seed2/summary.json)) | {{q|L6 0/27† · L8 0/4† · L10 0/6† · L12 0/40† · L14 0/9† · L16 0/19† · L18 0/10† · L20 0/2† · L22 0/2†}} |
| OLMo-3 ([run](results/early_push_where/olmo3_7b_instruct_jpp_d4_where_raw/summary.json)) | {{q|L6 2/4 · L8 0/11 · L10 1/32† · L12 0/34† · L14 0/51 · L16 0/27 · L18 0/5 · L20 0/0 · L22 0/0}} |
| 122B ([run](results/early_push_where/qwen35_122b_d4_where/summary.json)) | {{q|L9 0/1 · L12 0/1 · L15 0/1 · L18 0/6 · L21 0/27 · L24 0/32 · **L27 26/84** · **L30 18/83** · L33 1/89}} |
| Muse, 23 items ([run](results/early_push_where/muse30b_d4_where/summary.json)) | {{q|L10 0/4 · L13 0/9 · L16 0/30 · L20 0/35† · L23 0/4† · L26 0/26† · L29 0/13† · L33 0/35 · L36 0/0}} |

</details>

**Controls**
- A random push of the same size moves {{ctl|f7|random}} of lookups.
- Questions whose bridge is not on that sentence must not move (at most 10%).

**Weak spots**
- One topic and strong pushes, up to eight times a typical change.
- On the 27B's first scene set the rule picked an early layer, where the lookup moved too.
- On the 9B the strong pushes fail the off-path check at most layers; its valid cells move at most {{ctl|f7|recall|9b|main rule, draw 2}} of recalls.

**What it means.** The lens writes a stated bridge for recall on every model with a valid test. Whether the lookup follows depends on depth: it does around layer 16 on the 27B and at 27-30 on the 122B, and not after that (per layer above).

Prior work: the J-space carries multi-step reasoning from about a third of the depth on (Gurnee et al. 2026): [docs/prior_art.md](docs/prior_art.md#3-a-band-of-layers-where-the-lookup-ignores-the-lens-readable-form).

![Lens push](figures/cross_model/f_lens_push_recall_not_lookup_all_models.png)

### 6. The lens-readable part of a stated bridge moves recall, not the lookup

**Confidence:** {{conf|f2}}. **Verified:** [agent re-check](verification/agent_check_finding2.md) on the 27B, every cell matches; hand check pending.

**What we did**
- Changed the stated bridge (Jack's pet: cow → pig) and pasted back one part of the change: the lens-readable part, or the rest.
- The test point comes from a lens-free map. The lens-readable part must move recall there, or the test can't tell.

{{table|f2|draw 2|draw 1|table|JSON}}

**Controls**
- The lens-readable part moves recall ({{ctl|f2|recall}} across models and settings): it is not inert.
- The rest moves {{ctl|f2|rest}} of lookups.
- A random part of the same size moves {{ctl|f2|random lookups}} of lookups and {{ctl|f2|random recalls}} of recalls.

**Also:** a lens push at the same point writes {{v|f8|27b|stated bridge, draw 2}} of lookups on the 27B, and {{v|f8|122b|stated bridge, draw 2}} on the 122B.

![The lens-readable part](figures/cross_model/stated_bridge_main.png)

**What each answer needs.** The same runs, read the other way: paste the whole change, then the whole change without its lens-readable part, and count what is lost (% switched, n = {{q|180}} per family, the whole prompt; values only, no rule yet).

| Model, layer | Whole change: lookups / recalls | Without the lens-readable part | Lost: lookups / recalls |
|---|---|---|---|
| 27B, {{q|32}} | {{q|83% / 78%}} | {{ctl|f2|rest|27b|draw 2}} / {{q|27%}} | {{q|2 / 51 points}} |
| 9B, {{q|16}} | {{q|56% / 64%}} | {{ctl|f2|rest|9b|draw 2}} / {{q|11%}} | {{q|3 / 53 points}} |
| 122B, {{q|24}} | {{q|99% / 97%}} | {{ctl|f2|rest|122b|draw 2}} / {{q|57%}} | {{q|24 / 40 points}} |
| 122B, {{q|27}} | {{q|99% / 97%}} | {{q|51% / 19%}} | {{q|48 / 78 points}} |
| 122B, {{q|30}} | {{q|98% / 97%}} | {{q|86% / 57%}} | {{q|12 / 39 points}} |

Runs: [27B](results/statement_positions/d1_topics2_parts_27b/outcomes.jsonl) · [9B](results/statement_positions/qwen35_9b_d1_topics2_parts/outcomes.jsonl) · [122B](results/statement_positions/qwen35_122b_d1_topics2_parts/outcomes.jsonl); every cell recomputed from the raw rows. Against the bars fixed today for the band runs (lookups lose at most {{q|10}} points, recalls at least {{q|20}}), the 27B and 9B fit, and the 122B's lookups lose {{q|12-48}} points: on the 122B the lookup needs the lens-readable part too.

![What each answer needs](figures/cross_model/necessity_main.png)

All three 122B layers: [necessity_full.png](figures/cross_model/necessity_full.png).

**Weak spots**
- The 122B fails at layer 24; see [the 122B difference](#the-122b-difference).
- On the 27B and 9B a random part of the same size moves lookups as little as the lens part does. So the claim is the contrast, not "the lens part is special for lookups".
- What recall loses is not yet compared with taking out a random part of the same share: a large enough cut might cost recall {{q|50}} points whatever it removes. That comparison is the rule of today's band runs (at the bridge's word, layers 16-28 on the 27B and 6-14 on the 9B and OLMo-3; predictions committed, not yet run).

**What it means.** On the 27B and 9B, the lens-readable part moves recall far beyond its size, and lookups not at all; taking it out of the change costs recall most of its switches ({{q|78% → 27%}} on the 27B) and the lookup almost none. The lookup takes the stated bridge from the rest. On the 122B the lookup needs both.

Prior work: the workspace paper and two-hop recall (Gurnee et al. 2026; Biran et al., EMNLP 2024): [docs/prior_art.md](docs/prior_art.md#3-a-band-of-layers-where-the-lookup-ignores-the-lens-readable-form).

### 7. Lookups don't need the J-space; recall does, to a varying degree

**Confidence:** {{conf|f1}}. **Verified:** none.

**What we did**
- Zach's test: knock out the lens's top directions at a middle band of layers. His rule: chains ending in a recall must lose more than chains ending in a lookup.
- Our test, descriptive: remove the whole J-space while the bridge forms; count recalls and lookups still right.

{{table|f1|tasks, Zach's rule|animal suite}}

**Zach's runs, quoted from his plan, not reproducible from this repo until Zach pushes them** (one scene set): the recall-minus-lookup gaps are {{q|36}}, {{q|38}}, {{q|22}} and {{q|7}} points on 27B, 9B, 32B and Muse. Lookups lose at most {{q|13}} points. Only the 27B's run is on his pushed branch (the grid cell above).

**Why the two tests differ.** His cut is smaller and chosen on held-out items; ours removes the whole J-space. His tasks score points lost; ours score answers still right.

**What it means.** On Zach's quoted numbers, lookups don't need the J-space on any model tested, and recall needs it on the hybrid Qwens, less on the 32B, barely on Muse.

Prior work: the workspace paper lists one-step factual recall as bypassing the J-space, while our recall is two-hop, their multi-step case (Gurnee et al. 2026): [docs/prior_art.md](docs/prior_art.md#3-a-band-of-layers-where-the-lookup-ignores-the-lens-readable-form).

## Confidence and verification

**Confidence rule** (fixed before the grid was opened). Strong: holds on three or more models of both kinds, on two scene sets for two of them, with no failing cell. Open: fails on as many models as it holds on. Medium: everything else. Cells with fewer than 30 items are marked "too few items"; their verdicts are unchanged, and the "Holds on" counts leave them out. Example: Olmo-Hybrid's tables fail claim 1 by one item, the DeltaNet layers blocked keeping {{q|21 of 24}} ({{ctl|f4|DeltaNet|olmo_hybrid|table}}) against a bar of at least 90% ([run](results/attn_knockout/olmo_hybrid_7b_d2_formats/rows.jsonl)).

**Verification marks.** Hand: a person recomputed it from raw rows ([VERIFIED.md](VERIFIED.md)). Agent re-check: an independent agent recomputed it ([verification/](verification/)). None: agent analysis only.

## Boring explanations we checked

| Explanation | Test | Result | Status |
|---|---|---|---|
| The lens-readable part is just small | Paste a random part of the same size instead | It moves {{ctl|f2|random lookups}} of lookups and {{ctl|f2|random recalls}} of recalls, so the lens part's effect on recall is not its size | checked |
| FP8 weights vs a lens fit on bf16 (122B) | None yet | – | open |
| The 122B is the only mixture-of-experts model | None yet | – | open |
| A weak lens | Lens gate and held-out word-reading score per lens ([lens table]({{grid}}/grid.md)) | A better fit passes the gate on the 32B, but the 32B's recall control still fails | partly checked |
| The patch only shifts position | A random patch of the same size | Clean on all models but Gemma, in runs before 23 Oct (not in the grid) | checked, outside the grid |
| The patch copies any digit | Each answer is a different digit; the test layer is where the patched prompt's own digit is still rare | By design | checked |
| Some lookups avoid the late read (answers survive the block) | Block more tokens | Fewer survive: a relay through other tokens ([claim 1](#1-the-last-tokens-read-the-answer-late-through-attention)). Tables and JSON list three facts, so the old bar's guessing rate there is {{ctl|f4|chance|27b|table}} | relay; v2 pending |
| One scene set | Claims 1-3 on three scene sets; the lens push on two | Same verdicts across sets | partly checked |

## Choices made after seeing the data

| Choice | When | Why | What we did |
|---|---|---|---|
| Claim 3: split by the asked sentence | 21 Oct | The pooled test was mixed | Confirmed as a fixed rule on fresh scene sets |
| Claim 3: layer 50 on the 27B | 21 Oct | Chosen after its first runs | Repeated on two more scene sets |
| Claim 5: a second rule from about a third of the depth on | 22 Oct | The first rule picked an early layer | Both rules reported; the first stays the main one |
| Claim 1: the first scene set judged by the rule fixed for the second | 22 Oct | The first runs used an older rule | Accepted by Dan |
| Claim 1: "at chance" for a lookup that drops to guessing, not below; then the null near zero, not the guessing rate (late-read v2, beside the old rule) | 23 Oct | The bar is the guessing rate; blocking more tokens leaves fewer right (a relay) | Footnoted first; now "relay; v2 pending" until v2 is in the grid |
| The lens gate after the word (v2) | 22 Oct | v1 read sat on the bridge's own word | Added before any v2 run |
| Claim 4 becomes a methods note | 23 Oct | No logit-lens or embedding baseline at the same cells | Numbers kept; the J-space without the own word added |
| Claim 5: "never" becomes "from a model's own layer on" | 23 Oct | Two valid cells on the 122B move lookups | Per-layer table, valid cells only |
| The band at the word (new section) | 23 Oct | Read from runs already opened, on two kinds of scene sets | Descriptive; size-matched tests pending |
| The 122B: "counter-example" becomes "difference"; "late binding" becomes "late switch" | 23 Oct | Its lookup uses the J-space form longer, then stops | The test's rule unchanged |
| Our J++ fits as the main lens (32B, OLMo-3) | 23 Oct | The plain J-lens fails the 32B's gate | Other lenses listed beside, never switched in |
| Claim 7: our removal shown with an interval | 23 Oct | It has no committed rule | Shown as descriptive |
| Claim 7: Zach's unpushed numbers marked "quoted" | 23 Oct | Not on his pushed branch | Reproducible once he pushes |
| Gemma's stated-bridge runs: fewer scenes than planned | 23 Oct | Misaligned scenes are skipped | Recorded as a deviation |
| "Too few items" for cells under 30 | 23 Oct | Small cells decided labels | Display only; verdicts unchanged |
| The label's counting read by setting | 23 Oct | The settings disagree | Both reported |

Older choices and the full wording: [CHANGELOG.md](CHANGELOG.md).

## Next steps

Only steps that change a claim or its confidence.

| Step | What it decides | Rule fixed? | Cost | Status | Owner |
|---|---|---|---|---|---|
| Hand check of claims 1-3 and 6 (27B) | Their "verified" mark | – | 1-2 hours | Packets ready: [verification/](verification/) (claim, recompute script, checklist) | Dan, Zach |
| The late-read v2 rule in the grid | Claim 1 on Gemma and the 27B's long text | being written | CPU | Being added to the grid | agent |
| The 122B late-switch test | Claim 6 on the largest model | yes | 1.5 GPU-hours, a rented 2x H100 | Runs today | agent |
| Size-matched patch, with and without its J-space part | Whether the band is the form or the size | yes | – | Predictions committed; results pending | agent |
| Claim 1 on natural text | Whether the late read holds beyond generated lists | being written | ~4 GPU-hours | Design waits for approval | agent |
| The layer gap on the 9B | Whether claim 5's gap is general | yes | ~1 GPU-hour | Waits for Dan's predictions | agent |
| Slides | – | – | – | After the checks | Dan |

Timeline: update to Neel on Sat 24 Oct; write-up Wed-Fri 28-30 Oct.

## Links

[grid.md]({{grid}}/grid.md) · [RUNS.md](RUNS.md) · [CHANGELOG.md](CHANGELOG.md) · [STATUS.md](STATUS.md) · [prior work](docs/prior_art.md) · [predictions and scorecard](predictions/) · [VERIFIED.md](VERIFIED.md) · [docs/mapping.md](docs/mapping.md) · [docs/datasets.md](docs/datasets.md) · [DEVELOPER.md](DEVELOPER.md) · [run log](EXPERIMENTS.md) · [plan (Google Doc)](https://docs.google.com/document/d/1bqqdXePTUXQGlowVjk73sPfJkbV_tsu0RNNX-BiTYUc/edit?usp=drivesdk) · [HISTORY.md: the older README with every number](HISTORY.md) · [ONEPAGER_dan.md](ONEPAGER_dan.md)
