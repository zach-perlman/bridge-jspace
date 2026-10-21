# bridge-jspace

Does a model use the words a lens can read in its hidden state, or something else? We test this on two-hop
questions in open models (Qwen3.6-27B first).

**Status: exploration.** Only the rows marked *verified* have been checked by a human ([VERIFIED.md](VERIFIED.md)).
Everything else is an agent's recount of raw outputs on one model, and may change.

[Full write-up and old tables](README_archive.md) · [run log](EXPERIMENTS.md) ·
[Dan's predictions vs results](jobs/predictions/) · [plan (Google Doc)](https://docs.google.com/document/d/1bqqdXePTUXQGlowVjk73sPfJkbV_tsu0RNNX-BiTYUc/edit?usp=drivesdk)
· [how to run](DEVELOPER.md)

## The question

In a two-hop question the model first finds a **bridge**, then uses it to get the **answer**:

> "Which locker belongs to the animal known for oinking?" → bridge: *pig* → answer: *the pig's locker number*.

The **J-lens** (Gurnee et al. 2026, [Verbalizable Representations Form a Global Workspace](https://transformer-circuits.pub/2026/workspace/index.html))
reads hidden states as words. The part of the hidden state it reads is the **J-space**. In Claude, the bridge acts
on the answer through the J-space. **Is that also true in open models, and if not, what carries the bridge instead?**

## Words used on this page

We name each kind of question by **where the bridge comes from → where the answer comes from**:

| Name | Example (context: "Jack's pet is a cow. … The cow's locker is 5.") | Bridge | Answer |
|---|---|---|---|
| prompt → prompt | Which locker belongs to Jack's pet? | stated | stated |
| memory → prompt | Which locker belongs to the animal known for mooing? | recalled | stated |
| prompt → memory | How many legs does Jack's pet have? | stated | recalled |
| memory → memory | How many legs does the animal known for mooing have? | recalled | recalled |
| named → prompt | Which locker belongs to the cow? | named in the question | stated |

- **Lookup** = the answer comes from the prompt. **Recall** = the answer comes from the model's memory.
- **Org / alt prompt**: two versions of a prompt that differ in the bridge. We copy hidden states from the alt prompt
  into the org prompt ("patching") and see which answer comes out.
- **Lens-readable part** of a hidden-state change: the piece made of J-lens word directions.
- **Slot**: the place of a statement in the list (1st, 2nd, …).

## What we see so far

| # | Pattern | How sure | Evidence |
|---|---|---|---|
| 1 | **Recall goes through the J-space; a lookup in the prompt goes around it.** | **High** on Qwen3.6-27B (partly *verified*); low for other models | Verified B1-B3; Zach's three measures (fig. 1) |
| 2 | **The lens reads what the model has, not what it uses.** A stated bridge is read by the lens, but its lens-readable part does nothing for a lookup. | **High** (partly *verified*) | Verified B4; D1 (fig. 2) |
| 3 | **An early lens push changes *which entity is recalled*, not the lookup.** | **Medium-high**: pre-registered, one dataset, 2 wordings | D4 (fig. 3) |
| 4 | **A lookup reads the answer's statement late (layers 48-63), from the last tokens, through attention layers** (not DeltaNet), spread over many heads. | **High** on Qwen3.6-27B: 5 datasets, ~120 entities, code, 3 languages | D2 (fig. 4) |
| 5 | **Just before that, the last tokens carry an address: "the Nth statement, counted from the start of the list".** It is neither the bridge word nor a place in the text. | **Medium-high**: strong at layer 50 in every topic, and "counted from the start" passed its pre-registered test; an earlier pre-registered window (layers 44-52) failed per topic because the answer digit already arrives at 52 | D3 (figs. 5, 6) |
| 6 | **That address can be written.** A learned ~4-dimensional direction moves the lookup to another statement; the lens direction does nothing. | **Medium**: 42% on fresh scenes; 31% on new entities and wording, but its lower bound (27%) misses the pre-registered 30% bar | D3b (fig. 7) |
| 7 | "Around the lens" *is* this address. | **Open**: the fair test failed its control on one topic; rerun on 3 topics finished, not analysed yet | D3b fair test |
| 8 | The same holds in another model (OLMo-3-7B). | **Open**: first test looked at the wrong layers; layer-placed rerun queued | D3 on OLMo |

**The working picture** (Qwen3.6-27B, a hypothesis):

| Layers (of 64) | In a lookup from the prompt |
|---|---|
| 0-31 | A *named* entity's question words read its statement. |
| 16-28 | A *recalled* bridge is formed, as a word the lens can read and rewrite (pattern 3). |
| 28-44 | A *stated* bridge is spread over the context; its lens-readable part is not used (pattern 2). |
| 44-50 | The last tokens carry the address "the Nth statement" (patterns 5, 6). |
| 48-63 | The last tokens read that statement through the 16 attention layers (pattern 4). |
| 52+ | The last tokens carry the answer digit itself. |

## The evidence, one figure per pattern

Bars show the share of items; whiskers are 95% intervals. Each figure is built from saved runs by
[scripts/readme_figures.py](scripts/readme_figures.py).

### 1. Recall uses the J-space, a lookup does not

![Lens push and J-space removal, by kind of question](figures/readme_1021/f1_two_routes.png)

**Left:** pushing a hidden state along the lens direction of another animal switches recalled answers (36-51%), but
lookups no more than a random push of the same size does (3% and 19%; ticks = random push). **Right:** removing the
J-space leaves lookups right (99%) and breaks recall (19-22%); removing a random subspace of the same size changes
nothing (ticks). Animal suite, layers 32-40, 80 (push) and 100 (removal) scenes per kind.
*Zach, 20 Oct.* The 122B shows the same direction but weaker; Gemma 4 cannot be tested this way.

### 2. A stated bridge: the lens-readable part is not what the lookup uses

![Which part of a stated bridge's change switches the answer](figures/readme_1021/f2_stated_bridge.png)

We take the change in hidden state that swapping the stated bridge causes (org vs alt prompt) and paste only one part
of it into the org prompt. **For a lookup** (left), the whole change switches 87% of answers, the lens-readable part
alone 0%, everything except it 83%. **For a recall from the same stated bridge** (right) it is the other way round:
the lens-readable part does the work (66%). The lens still names the stated bridge as its top word on 90% of items.
80 scenes × 3 layers (32, 36, 40) per kind. Run `d1_parts_n80_v1`.

### 3. An early lens push acts on recall, not on the lookup

![Early lens push by kind of question](figures/readme_1021/f3_early_push.png)

At layer 20 we push the words that name the bridge ("the animal known for mooing", or "Jack's pet") toward another
animal's lens word. When the bridge is **recalled**, the answer switches (73%, 84%); when it is **stated**, it does
not (1%, 2%). A random push of the same size: 0%. Pre-registered, 100 scenes per kind (second wording; the first gave
the same picture). Run `d4_push_wording_b_v1`.

### 4. The lookup reads its statement late, through attention

![Answer statement hidden from the last tokens](figures/readme_1021/f4_late_read.png)

Qwen3.6-27B has 16 attention layers and 48 DeltaNet layers. Blocking the last tokens from seeing the answer's
statement **in the attention layers** breaks the lookup (2-13% still right); blocking it **in the DeltaNet layers**
changes nothing (100%). Same in 5 datasets (also Python code and other languages). No single head or layer is needed:
the read is spread out. 85 entities, 3 topics, 9 wordings (`pointer_v4`). Run `d2_v4_late_read`.

### 5. The last tokens carry an address to a statement

![Word, slot or digit after patching the last two tokens](figures/readme_1021/f5_slot_by_layer.png)

We copy the alt prompt's last two tokens into the org prompt at one layer. Three answers are possible, each a
different digit: the digit of **the same slot** in the org list (an address), the org digit of **the alt bridge's own
statement** (the word), or **the alt prompt's answer** (the digit itself). Around layer 50 the address wins (50% vs 21%
for the word, in each of 3 topics); from layer 52 the digit itself takes over. 450-760 items, 85 entities.
Runs `d3v4_swap_main`, `d3v4_swap_topics`.

![How the address counts](figures/readme_1021/f6_slot_counts.png)

**How does the address count?** We make the alt list differ from the org list so that "the same number in the list",
"the same number from the end" and "the same place in the text" point to different statements. The address follows
**the number counted from the start of the list** (31-39%), not the place in the text (9-16%) or the count from the
end (10-12%). Pre-registered, layer 50, ~435 items per panel; holds pooled and in at least 2 of 3 topics in every
panel. Run `d3v4x_swap_main`.

### 6. The address can be written; the lens direction cannot

![Pointer direction vs lens direction](figures/readme_1021/f7_pointer_push.png)

We fit a small (~4-dimensional) "pointer" direction from the slot labels and push along it at layer 48. It moves the
lookup to the target statement on 42% of fresh scenes and 31% of scenes with new entities and an unseen wording. A
push of the same size along the lens's word direction, or a random one, moves nothing (0%). Runs
`d3b_replicate_fresh_27b`, `d3v4_fit_main`.

## What is not shown yet

- **One model.** All of patterns 2-6 are on Qwen3.6-27B, a hybrid of attention and DeltaNet layers. OLMo-3-7B runs
  are queued.
- **Simple scenes.** 3-5 short statements, one-digit answers, the question right after the list.
- **Moderate effects.** Patches and pushes move 30-50% of answers; many patches change nothing.
- **The link between patterns 2 and 5** ("the lookup uses the address, which the lens does not read") is a candidate
  explanation, not a result.
- A late attention head (layer 51, head 22) looks at the right statement on every unedited scene, but after a patch
  it follows the new address only 58% of the time (the bar was 60%).

## Next steps

| Step | Question | Status |
|---|---|---|
| OLMo-3-7B: the address, at layers placed by when the digit arrives (17-19) | Is the address a Qwen property or how lookups work? | queued |
| OLMo-3-7B: does its address count by order, from the start? | Same pattern as fig. 6? (Dan: yes) | queued |
| Absolute vs relative position; long statements (`pointer_v6`) | Is the address "the Nth statement" or "N tokens back"? (Dan: relative shifts matter more; long statements give more errors) | being built |
| Fair "around the lens" test on 3 topics | Pattern 7 | finished, to analyse |
| Stated bridge in code (D1 in code) | Is pattern 2 general? | running |
| Word answers, longer lists (`pointer_v5`) | Is the address a digit trick? Does it count past 5? | designed |
| Natural carriers (chat turn, table, document), open- vs closed-book | Does any of this survive real layouts? | with Zach |

## Datasets

All are generated by us from templates with fixed seeds. A model is only tested on items it answers correctly
unedited (a competence gate per run). Sizes and files: [data/README.md](data/README.md). Examples below are real items
(random, seed 0).

**Animal suite** (`suite_v1`, Zach): pets and lockers, every kind of question. Used for patterns 1-3.
```
Tara's pet is a pig. Jack's pet is a cow. Dan's pet is a chicken.
The cow's locker is 5. The pig's locker is 3. The chicken's locker is 7.
Which locker belongs to the animal known for oinking?                        → 3
```

**Locker lists** (`pointer_v1`): five statements, an org and an alt prompt; each possible outcome of a patch is a
different digit. Used for patterns 4-6.
```
org: The bee's locker is 3. The chicken's locker is 1. The spider's locker is 7. The lion's locker is 9.
     The cat's locker is 2.  Which locker belongs to the animal known for making honey?        → 3
alt: The chicken's locker is 3. The spider's locker is 7. The lion's locker is 5. The cat's locker is 1.
     The bee's locker is 9.  Which locker belongs to the animal known for its roar?             → 5
after patching alt into org: 9 = the word (lion's statement in org), 7 = the same slot (3rd), 5 = alt's digit
```

**Many entities and wordings** (`pointer_v4`): the same design on 85 entities in 3 topics (countries, animals, body
parts), 9 sentence wordings per topic, some entities and one wording held out. Used for patterns 4-6.
```
The file on Greece is kept in drawer 1. The file on China is kept in drawer 9. The file on Hungary is kept in
drawer 7. The file on Venezuela is kept in drawer 2. The file on Sweden is kept in drawer 6.
Which drawer holds the file on the country whose capital is Athens?          → 1
```

**Moved filler, one statement more or fewer** (`pointer_v2`, `pointer_v3`, and `pointer_v4x` on the 85 entities):
a filler sentence of the same length moves, or the alt list gets one statement more or fewer, so "the Nth
statement", "the Nth from the end" and "the same place in the text" name different statements. Used for fig. 6.
```
org: The forehead chart is in folder 6. The skull chart is in folder 3. The wind picked up late in the evening.
     The tongue chart is in folder 5. The eye chart is in folder 9. The eyebrow chart is in folder 4.
alt: (the same charts reshuffled; the filler sentence is now 5th instead of 3rd)
```

**Python code** (`code_pointer_v1`): the same lookup as a dict, with list indices and variable chains.
```
lockers = {"dog": 7, "owl": 9, "cat": 5, "bee": 8, "frog": 3}
What number does lockers store for the animal known for making honey?      → 8
```

**Other languages** (`alias_pointer_v1`): statements in French, Spanish and German, question in English.
```
Le cheval a le casier 5. El perro tiene la taquilla 6. Die Kuh hat den Spind 7. El pollo tiene la taquilla 8.
La souris a le casier 3.  Which locker belongs to the animal known for clucking?          → 8
```

## Where things are

| What | Code | Results |
|---|---|---|
| Animal suite; Zach's copy split, lens push, knock-out | `scripts/suite_v1.py`, `suite_split.py`, `read_write.py`, `ablate_pilot.py` | `results/suite_split/`, `read_write/`, `ablate_pilot/` |
| Pattern 2 (D1): paste parts of a stated bridge | `scripts/statement_positions.py` | `results/statement_positions/` |
| Pattern 3 (D4): early lens push | `scripts/early_push.py` | `results/early_push/` |
| Pattern 4 (D2): hide a statement from chosen tokens and layers | `scripts/attn_knockout.py` | `results/attn_knockout/` |
| Patterns 5-6 (D3, D3b): patching, pointer direction | `scripts/pointer_v*.py`, `pointer_swap.py`, `pointer_fit.py` | `results/pointer_swap/`, `pointer_fit/` |
| Job queue (4×A100), pre-registered job specs | `scripts/jobq.py`, `jobs/` | `results/jobq/` |
| Figures on this page | `scripts/readme_figures.py` | `figures/readme_1021/` |

Every run's spec in `jobs/` states its hypotheses, decision rule and controls before it runs. The old README, with
every number, the generality audit, the hand checks of the controls and the long-shot designs, is in
[README_archive.md](README_archive.md#readme-before-the-rewrite-21-oct-2230-claims-table-audit-batch-4-plan-d5-design).
