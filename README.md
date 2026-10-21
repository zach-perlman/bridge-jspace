# bridge-jspace

**Where things are:** this page = main results and open questions · full write-up of every experiment:
[README_archive.md](README_archive.md) · run log: [EXPERIMENTS.md](EXPERIMENTS.md) · human-checked results:
[VERIFIED.md](VERIFIED.md) · status by Zach (20 Oct): [STATUS.md](STATUS.md) · plan:
[Google Doc](https://docs.google.com/document/d/1bqqdXePTUXQGlowVjk73sPfJkbV_tsu0RNNX-BiTYUc/edit?usp=drivesdk) ·
how to run, queue, figures: [DEVELOPER.md](DEVELOPER.md)

## The question
In a two-hop question the model first finds a **bridge** and then uses it to find the answer: "the language spoken in
the country where the Amazon River ends" → bridge *Brazil* → answer *Portuguese*. In Claude, the bridge acts on the
answer through the **J-space**, the part of the hidden state that the J-lens reads as words (Gurnee et al. 2026,
[Verbalizable Representations Form a Global Workspace](https://transformer-circuits.pub/2026/workspace/index.html)).
On open models (Qwen3.6-27B first): **what goes through the J-space, what goes around it, and what is the "around"
route?**

## Names used on this page
Each family of questions is named **"where the bridge comes from → where the answer comes from"**: *prompt* = stated
in the prompt, *memory* = recalled by the model.
```
Jack's pet is a cow. Mia's pet is a dog. Tom's pet is a pig.
The cow's locker is 5. The dog's locker is 3. The pig's locker is 7.
```
| Name (old code) | Question | Bridge | Answer |
|---|---|---|---|
| prompt → prompt (BL) | Which locker belongs to Jack's pet? | cow, from the prompt | 5, from the prompt |
| prompt → memory (BR) | How many legs does Jack's pet have? | cow, from the prompt | 4, recalled |
| memory → prompt (RL) | Which locker belongs to the animal known for mooing? | cow, recalled | 5, from the prompt |
| memory → memory (RR) | How many legs does the animal known for mooing have? | cow, recalled | 4, recalled |

Edits compare an **org prompt** with an **alt prompt** (the same prompt with another bridge): **bridge org** (cow) vs
**bridge alt** (dog), **answer org** (5) vs **answer alt** (3). The **lens-readable part** of a change is its piece
made of J-lens word directions; the rest is everything else.

## Main results

### Verified by a human ([VERIFIED.md](VERIFIED.md), Qwen3.6-27B)
| | Result |
|---|---|
| Lenses see the bridge (A1-A3) | At the last word the lenses rank the bridge first far more often than a same-kind distractor (57% vs 5% of layers 32-48); most remaining misses are found at an earlier word (22/30). |
| A recalled bridge acts through the J-space (B1) | Swapping only the lens-readable part of the bridge's direction switches 52% of answers (Claude 61%); the rest, with the J-space held fixed, 1% (Claude 6%). |
| A lookup in the prompt does not (B2-B3) | In brew (a two-step lookup in a colour table) the step is carried outside the J-space: the lens reads it but writing along its direction switches 1%; a direction nearly orthogonal to the lens (cosine 0.02) switches 34%. |
| Readers report what is written, not what is used (B4) | Two verbalizers (oracle lens, NLA) name a direction the model ignores on 99% of items. |

### Unverified: memory vs prompt (Zach, 20 Oct; animal suite, 27B)
Recall from memory goes through the J-space; a lookup in the prompt goes around it. Three measures agree:
- **Copy split:** the lens-readable part of the model's own bridge change carries 0.3-0.4× its fair share for lookups
  (memory → prompt, prompt → prompt) and 1.4-1.9× for recalls (random null 0.15-0.4).
- **Read vs write:** the lens reads the bridge of memory → prompt on 95% of items but pushing along it switches ≤ 3%;
  for memory → memory the push switches 36%.
- **Knock-out:** removing the J-space at layers 32/36/40 leaves lookups at 99% and drops recalls to 19-22%; random
  and size-matched controls stay at 98-100%. Also holds with JSON tool outputs and natural facts (TwoHopFact).
- **Generality is the gap:** the 122B shows read-without-write at every depth but a 4-6× weaker knock-out; the 9B is
  mostly untested; Gemma 4 31B-it is untestable (its lens cannot write even the positive control, and any J-space
  removal wrecks the model).

![The suite under three measures](figures/overview_1020/story_2x2.png)

### Unverified: what is the "around" route? (Dan, 21 Oct; depth track D1-D4)
One overnight queue, Qwen3.6-27B, pre-registered rules and controls; headline numbers recounted from the raw files.
Predictions vs results: [jobs/predictions/2026-10-21_dan.md](jobs/predictions/2026-10-21_dan.md).

| | Question | Result |
|---|---|---|
| D1 | Is "lookups go around the lens" an artefact of measuring only at the question? | **No.** For a bridge stated in the prompt (prompt → prompt), at layers 28-44 the bridge is spread over the whole context (pasting there switches 86% [77, 92]); the lens-readable part of that paste switches 0% (concentration 0.14 vs null 0.07), while the same paste's lens-readable part does carry the bridge for the recall question. |
| D2 | From where, and when, does the answer read "The cow's locker is 5."? | Memory → prompt: hide that statement from **the last tokens before the answer** and only 7% [3, 16] stay right (4/60); hide it from the question words: 100%. The read runs through **attention layers** (attention only 8%, DeltaNet only 100%) at **layers 48-63** (blocking 0-47: 100%). Recall questions do not need it (100%). |
| D3 | At that moment, do those tokens carry the **word** (cow), a **pointer to a statement slot**, or the **answer**? | Pasting from an alt prompt with reordered statements at layers 44-52: the answer at the **same statement slot** 29% [21, 39] vs bridge alt's statement 9% [5, 16] vs the alt prompt's own answer 12%; control 0/100. From layer ~52-56 the tokens carry the fetched digit (98-100%). Memory → memory never shows a slot answer. Pooled only: each topic alone is "mixed". |
| D4 | Is the strong early lens push that switched memory → prompt just typing the word in? | It works only on the subject phrase (37% [26, 49]; rest of the question 0%; random 0%). Injection vs writing **not decidable** from this run. |

![Word, slot or answer, by layer (D3)](figures/depth_1021/d3_word_slot_or_answer_by_layer.png)
![From which layer the statement must stay readable (D2)](figures/depth_1021/d2_from_which_layer.png)

**The current picture (a hypothesis, one model).** For a lookup in the prompt: up to ~layer 40 the question words
carry the recalled word; at layers 44-50 the last tokens carry *which statement* to read (a slot pointer) more than
*which entity*; at layers 48-63 they read that statement through attention; from ~52-56 they carry the fetched
answer. The lens can read the word but cannot steer the lookup exactly where the model works with the pointer. The
full D1-D4 write-up (methods and datasets compared, worked examples, every figure, numbers to recompute) is in
[README_archive.md](README_archive.md#depth-track-d1-d4-2026-10-21-what-is-the-around-route).

## Open questions
1. **Pointer to a statement, or to a token position?** In every prompt so far the n-th statement also sits at a fixed
   token offset. *Running next:* D3 v2 with scenes that shift offsets but keep the order (and the converse), and
   >= 35 items per topic and slot.
2. **Is there a pointer to the answer token itself** (the "reflexive" route of Gur-Arieh, Geva & Geiger 2025)? Not
   testable yet: the alt prompt's answer never appears in the org prompt. *Next:* D3 v2 scenes where it does.
3. **Can a fitted pointer direction steer the lookup where the lens cannot?** If yes, it is the seed of a second,
   "pointer" readout next to the J-lens; its angle to the lens directions says how separate the two are. *Next:*
   D3b (difference of means and low-rank subspace, with held-out entities and the dormant-subspace control).
4. **Does it survive harder data?** Python code where the pointer is literal (dict keys, list indices, variable
   chains) and statements in another language than the question (a lookup that must match by meaning, not by token).
   Datasets being built; D2 and D3 to run on them.
5. **Knock-out confounds (Zach):** removing the J-space also costs word answers ~35% even in a pure lookup; does it
   erase the subject's identity rather than the workspace? (control: keep the subject's own word.)
6. **Other models.** 122B weaker, 9B untested, Gemma untestable; planned: Qwen3-32B (full attention in every layer:
   the cleanest version of D2), DeepSeek-V4-Flash, GLM-4.7-Flash, Mistral-Small-24B (Zach's ports).
7. **Before post-training?** The OLMo-3-7B ladder (base, SFT, DPO, Instruct) is ported with verified lenses but not
   run: does the memory/prompt split, and the pointer, exist in the base model?
8. **Early lens writes (D4):** an injected word and a written variable sit on the same tokens for memory → prompt;
   separating them needs a push on a subject phrase that does not name the bridge, and downstream lens readouts.

## Code and data (short map)
| What | Code | Data / results |
|---|---|---|
| Animal suite (all families), competence | `scripts/suite_v1.py` | `data/suite_v1*`, `results/suite_v1/` |
| Copy split, read/write, knock-out (Zach) | `scripts/suite_split.py`, `scripts/read_write.py`, `scripts/ablate_pilot.py` | `results/suite_split/`, `results/read_write/`, `results/ablate_pilot/` |
| D1 patch at one place | `scripts/statement_positions.py` | `results/statement_positions/` |
| D2 blocking reads | `src/bridge_jspace/knockout.py`, `scripts/attn_knockout.py` | `results/attn_knockout/` |
| D3 word / slot / answer | `scripts/pointer_v1.py`, `scripts/pointer_swap.py` | `data/pointer_v1/`, `results/pointer_v1/`, `results/pointer_swap/` |
| D4 early push vs edits | `scripts/early_push.py` | `results/early_push/` |
| Job queue, job pages, plain names | `scripts/jobq.py`, `src/bridge_jspace/job_pages.py`, `jobs/`, `jobs/titles.yaml` | `results/jobq/` (ledger, draft run-log rows) |
| Figures used on this page | | `figures/overview_1020/`, `figures/depth_1021/` |
| Earlier experiments (exp01-exp23, part A readers) | `scripts/exp*` | see [README_archive.md](README_archive.md) |
