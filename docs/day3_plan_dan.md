# Dan's half: what is the "around" route?

*Draft for docs/day3_plan_zach.md (Dan to edit), 22 Oct, morning. Qwen3.6-27B unless named; every number is
**unverified**, one data seed. Each run's hypotheses, rule and controls are in its spec under `jobs/`, written before
it ran; Dan writes predictions before each result is opened (`predictions/`). Figures: README.md.*

## 1. The question

When the answer is looked up in the prompt, the J-lens reads the bridge, but writing along the lens moves almost
nothing (B2-B3; Zach's C2). **What carries the bridge to the answer instead?**

**Working hypothesis.** The lookup runs on an *address*, not on the bridge's word:
- the last tokens carry "the Nth statement, counted from the start of the list";
- attention layers then read that statement late.

The lens shows the word, the content. It does not show the address.

### Claims and their status on the 27B

| | Claim | Test | Status (27B) |
|---|---|---|---|
| **D1** | A bridge stated in the prompt is used through its lens-readable part only when it feeds a recall | Paste parts of the bridge's change into the org prompt (n = 80 x 3 layers per family) | **Holds** on the animal suite. Lookup: the whole change switches 87%, its lens part 0%, the rest 83%. Recall: the lens part switches 66%. The same split as Zach's C2 descriptive result (P→M 18 vs P→P 2) by another method. |
| **D2** | The lookup reads the answer's statement late (layers 48-63), from the last tokens, through attention, not DeltaNet | Hide the statement from the last tokens in every attention layer / every DeltaNet layer | **Holds** in 5 datasets, 85 entities: 2-13% still right vs 100%. No single head or layer is needed. |
| **D3** | Before that, the last tokens carry an address to "the Nth statement, from the start" | Patch the alt prompt's last two tokens: which org statement does the answer come from? | **Holds at layer 50**: slot 50% vs word 21%, in each of 3 topics. Order beats the place in the text (39 vs 9). From the start beats from the end (31-39 vs 10-12). Both pre-registered. A wider pre-registered window (44-52) failed per topic: the digit itself arrives at 52. |
| **D3b** | The address can be written, the word cannot | Push along a fitted ~4-dimensional slot direction vs the lens direction at layer 48 | **Partly.** 42% on fresh scenes. On new entities and wording 31%, but its lower bound (27%) misses the 30% bar. Lens push 0%. |
| **D4** | The early lens push acts on recalling the bridge, not on the lookup | Lens push at layer 20 on the subject phrase | **Holds** (pre-registered): recalled bridge 73% and 84%, stated bridge 1% and 2%, random 0%. |
| D5a | A late head (51/22) reads the address | After a patch, does it look at the statement the new answer comes from? | **Not shown**: 58% (bar 60%), partly built in by the patch. |
| link | "Around the lens" *is* the address | The fair test at layers 32-40 | **Not shown.** The control failed on one topic; the 3-topic rerun is done, analysis today. |

## 2. What success looks like

| Outcome | Criterion |
|---|---|
| **Strong** | The address (D3) and the late read (D2) hold on ≥ 2 architectures, including a non-Qwen family (OLMo-3, Gemma 4). They survive word answers and 8-statement lists (v5). The address is an order index, not a token distance (v6). The address can be written where the lens cannot (D3b) on new entities. |
| **Medium** | The Qwen family only (27B, 9B), with a diagnosed account of why the address does not transfer. |
| **Informative negative** | The address is a property of Qwen3.6-27B. Then report D1 + D2 + D4: a timeline of when the J-space is used (recall, early) and when it is not (the in-context read, late). |

## 3. Metrics

| What | Metric |
|---|---|
| **D3 (address)** | Share of patched answers at the same slot vs bridge alt's own statement vs the alt prompt's answer. Verdict "slot" iff its lower bound beats the rivals' upper bounds and the random-push bar, with the same-entity control ≤ 10%. Entity-cluster bootstrap; pooled and in ≥ 2 of 3 topics; n items / k entities / t wordings per cell. |
| **Layers** | Placed by function per model, not by relative depth: the layers before the fetched digit arrives at the last tokens. Example: OLMo 17-19, fixed from an earlier run. The counterpart of Zach's held-out band. |
| **D2 (late read)** | % still right with the statement hidden from the last tokens, per layer kind and band. Controls: an off-path statement of the same length, a random span, the recall family. |
| **D3b** | Steer rate vs a lens push and a random direction of the same norm, on held-out entities and wording. Bar: lower bound ≥ 30% and ≥ 20 points above both. |
| **Process** | Predictions written before each result is opened, then scored (batch 2: 8 right / 10 partly / 10 wrong of 28). |

## 4. Key experiments and status

| Model | Address (D3) | Late read (D2) | Other | Status |
|---|---|---|---|---|
| **Qwen3.6-27B** | D3 / D3b done. **Overnight:** absolute vs relative position and long statements (v6); colour-word answers and 8 statements (v5); a second draw of scenes | done | **Overnight:** J-space removal at the read layers (44-62); late heads on natural errors; reproduction of the 4 headline runs from a clean checkout | results today |
| **OLMo-3-7B-Instruct** (all attention) | done at the function-placed layers (to score); order vs place done; v5, v6, D3b overnight | overnight (4-layer bands) | Zach's three measures (raw format) done | results today |
| **OLMo ladder** (SFT, DPO) | overnight | overnight | Zach's three measures (raw) overnight | results today |
| **Qwen3.5-9B** | overnight | overnight | | results today |
| **Gemma 4 31B-it** | overnight (no lens needed) | overnight | | results today |
| **Qwen3-32B** (dense) | after Zach's port | after Zach's port | | Thu |

## 5. Challenges and limitations

- **One model for most claims.** "Attention, not DeltaNet" may be specific to the hybrid design.
- **Moderate effects.** Patches move 30-50% of answers, many change nothing, and the word sometimes travels with the address.
- **Synthetic scenes.** 3-8 short statements with digit answers (v5 adds colour words). The chat-template question is answered for D3: raw text gives the same split.
- **Layer placement.** Pre-registered windows placed by relative depth failed twice; we now place them by function.
- **The link to the J-space** ("around = address") is a candidate explanation, not a result. Zach's C2 also failed as pre-registered.

## 6. Key uncertainties and how we resolve them

| Uncertainty | Test (status) | What changes |
|---|---|---|
| Is the address a digit-copying trick, or a 5-item effect? | v5: colour words, 8 statements (overnight) | If it fails: narrow the claim to digit lookups |
| Is it an order index or a token distance (RoPE)? | v6: an extra sentence before the list vs before the question (overnight) | If the distance wins: "positional pointer", still outside the lens |
| Is it Qwen-specific? | OLMo, 9B, Gemma (overnight), Qwen3-32B (Thu) | Scope the claim |
| Is the read itself outside the J-space? | J-space removal at layers 44-62 (overnight) | If lookups survive where they read: direct evidence for "around" |
| Is there a readable address (a provenance monitor)? | Late heads on natural errors (overnight) | A candidate monitor, or "steers but is not readable" |
| Do the numbers reproduce? | Clean-checkout reruns + a second data seed (overnight) | Which numbers go to VERIFIED.md |

## 7. Fallbacks

- **The address does not transfer:** lead with D1 + D2 + D4 on the 27B (recall uses the J-space early, the lookup reads late through attention), with the address as a 27B case study.
- **The address is a token distance:** reframe as a positional pointer; the "outside the lens" part stands.
- **v5 fails for words:** restrict D3 to digit lookups; D1, D2 and D4 stand.
- **Joint result with Zach:** the lens writes a stated bridge only when it feeds a recall. D1 (paste parts) and Zach's C2 descriptive (lens write) show this by two methods.
