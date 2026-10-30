# bridge-jspace: Day 3 plan

Dan Orel & Zach Perlman · Wed 21 Oct 2026 · Run log: EXPERIMENTS.md (one line per run: question, n, seeds, result, W&B, verdict). **Since 16 Oct nothing is human-verified yet**: every number below from the sprint is *unverified* until one of us recomputes it into VERIFIED.md.

---

## 0. Where we are

**Before the sprint** (one-pager, 16 Oct, verified, Qwen3.6-27B):
- **B1:** a bridge recalled from memory acts through the J-space, as in Claude. Swapping its J-space part flips 52% of answers (Claude: 61%).
- **B2–B3:** a variable looked up in the prompt (brew) doesn't. The lens reads it but can't write it (1%), while a direction nearly orthogonal to the lens writes it (34%).

**Neel's feedback on our proposal (19 Oct):**
- H0 ("the J-space carries only recalled words") is probably false.
- The suite is too toy; we need diverse settings.
- Try a larger model early.
- No MoE-routing or verbalizer side checks.

**The split (20 Oct).** North Star: map what goes through the J-space and what goes around it, across model families, and explain the "around" route.
- **Zach, breadth:** does the memory-vs-prompt split hold beyond our setup?
- **Dan, depth:** what is the "around" route?

---

# Zach's half: does the split hold beyond our setup?

## 1. The question

When a model chains facts (e.g. *a pet named in the prompt → its locker number*, or *"the animal known for mooing" → cow → its number of legs*):
- Do the steps that **retrieve from memory** need the J-space?
- Do the steps that **look something up in the prompt** not need it?
- Is that a property of LLMs, or of one model and one templated task set?

**Notation.** Each step retrieves from the **P**rompt or from **M**emory, or is **C**omputed (a typo repaired, a word translated). A chain is written step by step, e.g. P→M = a pet named in the prompt, then its number of legs recalled from memory.

### Claims (pre-registered 20–21 Oct) and their status on the 27B

| | Claim | Test | Status (27B) |
|---|---|---|---|
| **C1** | Memory steps need the J-space; prompt lookups don't (graded) | The paper's knock-out (top-10 J-lens directions removed at every position, answer protected) vs a same-size rotated control. Holds if memory-final chains lose ≥30 points more than lookup-final ones at the middle band, with controls within 10. | **Holds** (gap 36; see §1a). The strict version ("lookups lose ≤10 in *every* band") **fails**: early layers hit lookups too. |
| **C2** | The lens reads lookup-used bridges but can't write them | The strongest fair write (lens add/swap/transplant, layers 28–40, question/final positions) vs a random-norm control. Graded: memory-used ≥3× and ≥+30 points over lookup-used. | **Fails as pre-registered.** Categorical on the suite: a J-space transplant moves the lookup-used bridge. Graded on v2: M→M 45 vs M→P 30, intervals overlap. Kept as descriptive only. |
| C3 (side) | Computed bridges that feed a recall sit in the J-space beyond their own word, so H0 is false | Copy split and read/write on typo- and translation-repaired bridges | **In hand on the 27B** (old suite). Not yet replicated. |

### 1a. What we found since the split (27B; unverified; one data seed)

**New task set** (Neel's "too toy" point):
- 12 chain types: P/M/C starts, 2- and 3-step chains.
- 7 domains; 6 formats (prose, chat, document, JSON, table, code); 4 difficulty levels.
- 3,256 items. Each model is judged only on items it answers right on every step (with a guess prompt for items it could get right by prior).

**C1, whole question** (Fig 1):
- **At layers 32–40:** memory-final chains lose 41 (P→M) and 45 (M→M) points; lookup-final chains lose 0 (P→P) and 13 (M→P).
- **The gap:** 36 [95% CI 26–48] (n = 152/101/152/101 items; 47/35 bridge entities). Rotated controls are within 3 points.
- **It holds:**
  - in text formats (31) and structured formats (42);
  - without the guessable items (34);
  - for computed starts (C→P 6 vs C→M 41).
- **It's depth-specific:**
  - The gap is −6 at layers 12–20 and +11 at 20–28.
  - On the old suite the early dips come from damaging the facts as they're read (position split).
  - On the old suite the memory collapse is sharp: M→M accuracy 41/7/41/85% across bands 20–28/32–40/36–44/40–48.
- **It's partly a confidence effect:** memory items are less confident unedited. The confidence-matched gap is 28–35, and only 14 in the most confident quarter of items.

**Each step asked alone** (layers 32–40; Fig 2):
- Memory steps after the first lose 14–45 points, in both 2- and 3-step chains.
- Lookups lose ≤6.
- First-step recalls in M-start chains barely move here; those chains break at layers 20–28 instead.

**Dose** (old suite, layers 32–40): memory-final chains break with only 5 directions removed (6–8% accuracy left). Lookups survive 100 directions.

**C2, descriptive:**
- Bridges stated in the prompt are written by their own lens direction only when used for recall (P→M 18 vs P→P 2).
- Recalled bridges are written either way.
- All lens writes are much weaker on v2 than on the suite.
- The steering sites carry the bridge only partly: the copy ceiling was 0–60% at one layer.
- I found and fixed a bug in our multi-layer ceiling measure and withdrew one diagnostic built on it.

**Other models (old pipeline, before v2):**
- **Qwen3.5-122B:** direction replicates, but the knock-out effect is 7–14 points vs ~80 on the 27B; read-not-write holds at every depth.
- **Qwen3.5-9B:** read-not-write holds; mostly untested otherwise.
- **Gemma 4 31B-it:** the base-model lens failed, and our first (sparse) lens broke the model on plain text. Refit on every layer, finished and passed its quality check on 21 Oct.

## 2. What success looks like

| Outcome | Criterion |
|---|---|
| **Strong** | C1-graded holds on ≥3 of 4 models, including ≥1 non-Qwen family, each at a band chosen on held-out data. It survives the specificity control (J-lens directions beat plain unembedding directions) and the keep-own-word kill test, and replicates on a fresh data seed. |
| **Medium** | Holds on the Qwen family only (9B, 27B, 32B dense, 122B), with a diagnosed account of why it doesn't transfer. Or it holds, but the specificity control shows it's about token-aligned directions in general, and we reframe ("token-identity subspace"). |
| **Informative negative** | Fails on other models: an atlas of which chains and depths need the J-space, per model. |

## 3. Metrics and gates (fixed in code before each model's data)

| What | Metric |
|---|---|
| **C1 (primary)** | Memory-final minus lookup-final accuracy loss at the model's middle band; ≥30 points with rotated controls within 10. 95% bootstrap over bridge entities. |
| **Middle band** | Chosen per model on **held-out data**: ctrl_v8, the same generator with another seed, sharing no prompts with the test set. Rule: the window where memory-final chains break most, with controls ≥90%. Lookups play no part in the choice. It reproduces the 27B's 32–40. |
| **Kill tests** | Keep-own-word knock-out: ≥75% of the damage restored kills C1. Rotated control within 10. |
| **Reported beside C1** | Every band; strict C1; each step alone; confidence-matched gap; the guessable split; text vs structured formats. |
| **Specificity** | The same knock-out with unembedding (logit-lens) directions instead of J-lens ones, on the same items. Descriptive. |
| **C2** | C2-graded (pre-registered, 27B failed). C2-relative (designed after the 27B data, so a clean test only on fresh cases and new models): lens write relative to a copy ceiling, cross-validated over bridge entities. |
| **Model gates** | Competence (each model judged on items it answers right). Lens check: held-out readout vs the logit lens, scored identically for every model. Plain-text loss under the knock-out (does it just break the model?). Steering positive control (countries; reported, not binding). |

## 4. Key experiments and status

Every model runs the identical pipeline (`docs/archive/setup_grid.md`). Times are Eastern estimates.

| Model | Knock-out (C1 + checks) | Steering (C2) | Lens check | ETA |
|---|---|---|---|---|
| Qwen3.6-27B (published J++) | C1, steps, three-step done; band re-check, keep-own, seeds, position split, specificity tonight | Rerun tonight with the corrected ceiling | Tonight | Wed ~10:30pm |
| Gemma 4 31B-it (our J++, every layer) | Band choice → C1 → checks tonight | Overnight | Overnight | C1 Wed ~8pm; C2 Thu ~4am |
| Qwen3-32B (our J++; dense; separates architecture from family) | Thu | Thu | Thu | C1 Thu ~12pm; C2 ~1:30pm |
| Qwen3.5-9B (published J++) | Overnight | Thu morning | Thu | Thu ~8am |
| All | Dose curves for Gemma and Qwen3-32B (deferred, last) | | | Thu ~9pm |

**Decisions waiting on tonight's results:**
- **C2 steering band:** the copy ceiling peaks at the top of the 28–40 band. If the corrected ceiling clears 0.5 only later, rerun steering for every model at an aligned band; otherwise keep 28–40.
- **Fresh-seed replication:** run it if any model's C1 gap lands within ±10 points of 30, or the models disagree. More items with the same entities wouldn't narrow the interval; the number of distinct bridges limits it.

## 5. Challenges and limitations

- **Depth:** C1 is a middle-layer statement; early layers hurt lookups. We report every band and pick bands on held-out data, but this can't make C1 hold "everywhere".
- **Confidence and answer type:** memory-final answers are facts with few possible values (e.g. legs), lookup-final answers are arbitrary numbers. We have the confidence-matched gap and the guess split; neither removes the confound completely.
- **Specificity unknown** until the unembedding control lands: the claim may be about token-aligned directions, not the J-space as such.
- **C2 failed** on the 27B as pre-registered. Steering on open models is weak in general, consistent with Neel's review and Zeisler's replication (6–11% intermediate-swap flips on Qwen3.6-27B / Gemma 3 vs Anthropic's 54–70%).
- **Generality is the main open question:** so far v2 results exist for one model. Lens provenance differs (published vs our fits; Qwen3-32B fit on 32 prompts vs 64), and Gemma-it is far off-distribution on the WikiText its lens is fit on (7.7 vs 2.3 nats).
- **Data:**
  - synthetic templates, digit answers, one data seed;
  - 35–47 distinct bridges per chain type, which bounds precision (C1 interval about ±11 points);
  - memory-start items skew to easier levels and to animals, elements and planets.

## 6. Key uncertainties and how we resolve them

| Uncertainty | Test (status) | What changes |
|---|---|---|
| Is the damage specific to the J-space? | Unembedding-direction knock-out on every model (tonight → Thu) | If it does as much as the J-lens: reframe as token-aligned directions |
| Is it just the subject's own word? | Keep-own-word knock-out (tonight → Thu) | ≥75% restored: C1 killed; lead with steering descriptives and Dan's mechanism |
| Is it a layer-selection artefact? | Held-out band choice per model; 27B re-check (tonight) | If the 27B's band moves, its middle-band runs redo automatically (pre-stated) |
| Is it confidence? | Confidence-matched gap (automatic) | Reported beside the rule; flag models where it drops below 30 |
| Does it generalize? | Gemma, Qwen3-32B, 9B (by Thu evening) | See fallbacks |
| Is C2 testable at all on open models? | Corrected ceiling + band copy sweep (tonight) | Rerun at an aligned band, or keep C2 descriptive |

## 7. Fallbacks

- **C1 holds on ≥2 families:** lead with a graded, depth-specific C1, plus the step-level result.
- **Qwen only:** scope to Qwen (4 models, including dense Qwen3-32B) and diagnose the others.
- **The specificity control matches the J-lens:** "memory steps need token-aligned directions in the middle layers". That still bears on the paper's ablation results.
- **The keep-own test kills C1:** lead with Dan's mechanism and the descriptive steering pattern.
- **C2 stays failed:** report it as a negative result ("the lens's own direction doesn't separate memory-used from lookup-used bridges on diverse tasks"), with the descriptive pattern.

## 8. Infra and tooling

**In place:**
- A 2× H200 box with job queues.
- W&B project `mats-sprint`; write-once results; a model registry with lens sha256s; one-line-per-run log.

**Ported:** Gemma 4 31B-it, Qwen3-32B, Qwen3.5-9B; all on the same pipeline.

**Our own J++ fitting:** works end to end (Gemma done, Qwen3-32B tomorrow).

**Not done:** DeepSeek-V4-Flash (Neel's larger-model pick) needs 2 GPUs and a port. The 122B covered "larger" on the old pipeline. **Question for Neel:** is a v2 rerun on a larger model worth more than the remaining kill tests?

**Parked until the v2 round:** passage vs closed-book (an item-level SQuAD-vs-TriviaQA test, the most direct answer to "too toy"); Mistral-Small-24B as second-family insurance; more data seeds.

## 9. Next steps

| When | Step |
|---|---|
| Wed night | 27B steering with the corrected ceiling; Gemma C1; specificity and keep-own on the 27B and Gemma; C2 band decision |
| Thu | Qwen3-32B and 9B full pipeline; Gemma steering; replication decision |
| Fri | Cross-model analysis; figures; Dan verifies the headline numbers into VERIFIED.md; passage vs closed-book if time allows |
| Sat (Day 6) | Progress update |

*Figures:* Fig 1, C1 by layer band (27B); Fig 2, each step alone at layers 32–40 (27B). Both are in `figures/archive/slack_1021/`.

---

# Dan's half: what is the "around" route?

*(Dan to fill in. Headings mirror the above.)*

## 1. The question

## 2. What success looks like

## 3. Metrics

## 4. Key experiments and status
*From the 20 Oct split: where the lookup reads the bridge (the positions where it's stated vs the question); attention knock-out (block question→statement attention); pointers (lookback / binding-ID tests, a code that writes M→P and its cosine with the lens direction); the 27B's early writes; the longshot (a pointer readout; the OLMo post-training ladder).*

## 5. Challenges and limitations

## 6. Key uncertainties and how to resolve them

## 7. Fallbacks

---

# Shared

- **Claims freeze:** about a week in; then the write-up together.
- **Verification:** each of us human-verifies the other's headline numbers into VERIFIED.md before they leave "unverified".
- **Joint fallback stories:**
  - holds on ≥2 families → the full claim plus mechanism;
  - Qwen only → scoped claim plus diagnosis;
  - the keep-own test kills the knock-out → lead with read ≠ write plus mechanism;
  - C2 doesn't hold → lead with C1 where it holds.
