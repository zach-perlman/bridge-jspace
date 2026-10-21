# Per-model setup grid (2026-10-21, updated after Zach's decisions)

Legend: ✅ identical · ≈ identical at matched relative depth · ⚠️ differs, explained · ❌ gap (fixable; unfair as it stands)

Decisions (Zach, 2026-10-21):
- **27B fills:** the plain-text check at all 9 layers, the three-step ceiling, and the same lens check for every model.
- **Qwen3-32B lens:** stays at 32 fit prompts.
- **Positive control:** reported for every model, binding for none.
- **9B:** rerun on this pipeline after Qwen3-32B.
- **Dose curves:** wait until every model's core runs are done. The 27B's and 9B's are not queued; decide later.
- **Middle band:** every model's comes from its own suite depth sweep by the rule that gave the 27B's 32-40 (`scripts/choose_band.py`), fixed before its v2 data. Every model also gets a v2 depth profile.

## 1. Model and lens

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | Qwen3.5-9B | |
|---|---|---|---|---|---|
| Role | headline | second family | dense control | smaller model | |
| Layers | 64 | 60 | 64 | 32 | |
| Attention | hybrid linear + full | sliding + global | full | hybrid linear + full | ⚠️ by design |
| Post-trained chat model | yes | yes | yes | yes | ✅ |
| Lens | J++, published | J++, our fit (0-58) | J++, our fit (0-62) | J++, published | ⚠️ who fit it |
| Lens fit data | WikiText (count not recorded) | WikiText, 64 prompts | WikiText, **32 prompts** | WikiText, 64 prompts | ⚠️ kept (Zach) |
| Lens check (same for all) | queued (exp19: J++ 0.714 vs logit 0.433, all layers) | queued | queued | queued | ✅ |
| Model's loss on the lens-fit text | 2.33 nats | **7.66 nats** (not our harness) | from its text-loss run | from its text-loss run | ⚠️ Gemma off-distribution |

## 2. Data

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | Qwen3.5-9B | |
|---|---|---|---|---|---|
| Items | full_v8, full_v8b | same | same | same | ✅ |
| Eligibility | own competence, every check right | same | same | same | ✅ |
| Two-step pools PP/PM, MP/MM, CP/CM | 152, 101, 144 | 141, 92, 128 | after competence | after competence | ✅ by ability |
| Guess prompts | yes | yes | yes | yes | ✅ |
| Prompts | raw + own chat template | same (+ BOS) | same | same | ✅ |
| Suite competence (positive control) | own (2026-10-19) | first 150 per family | first 150 per family | all items (2026-10-19) | ✅ (first 60 used) |
| Data seeds | 1 | 1 | 1 | 1 | ✅ (all single) |

## 3. C1: knock-out

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | Qwen3.5-9B | |
|---|---|---|---|---|---|
| Bands | 12-20, 20-28, 32-40, 0-62 | 11-19, 19-27, 30-38, 0-58 | as 27B | 6-10, 10-14, 16-20, whole | ≈ (9B bands are 5 layers wide) |
| Rule (middle) band | 32-40, chosen on its suite depth sweep (2026-10-20) | chosen on its own suite sweep, same rule (fallback 30-38) | same (fallback 32-40) | same, 5-layer windows (fallback 16-20) | ✅ same procedure |
| Depth profile on the v2 rule words | queued (tonight) | queued | queued | queued | ✅ |
| Two-step C1, margin-matched gap | done (B200) | queued | queued | queued | ⚠️ 27B hardware |
| Specificity (unembed10), keep-own, control seeds, position split, steps | queued / done | queued | queued | queued | ✅ |
| Three-step whole + steps | done | queued | queued | queued | ✅ |
| Dose curves | not queued | after everything, at its chosen band | after everything, at its chosen band | not queued | ⚠️ deferred |
| Rotated-control draw | B200 GPU (headline); CPU since | CPU | CPU | CPU | ⚠️ benign |

## 4. C2: steering

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | Qwen3.5-9B | |
|---|---|---|---|---|---|
| Band / singles / early | 28-40 / every 2nd / 16,20,24 | 26-38 / every 2nd / 15,19,23 | as 27B | 14-20 / every layer / 8,10,12 | ≈ |
| Two-step steering, question + final | full pools | full pools | full pools | full pools | ✅ |
| Ceiling | paste re-measure queued | paste | paste | paste | ✅ |
| C2-relative rule | after seeing its data: fresh cases clean | clean | clean | clean | ⚠️ |
| Positive control | reported | reported | reported | reported | ✅ |
| Three-step steering + ceiling | ceiling queued | yes | yes | yes | ✅ |
| Copy sweep (band paste) | queued | queued | queued | queued (window 6) | ≈ |

## 5. Other

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | Qwen3.5-9B | |
|---|---|---|---|---|---|
| Plain-text loss under knock-out | 9 layers (32-40) queued | 9 layers (30-38) | 9 layers (32-40) | 5 layers (16-20) | ≈ |
| Hardware | B200 + H200 (gate: 98.6% unedited, 100% at 32-40) | H200 | H200 | H200 | ⚠️ |

Not on this pipeline: Qwen3.5-122B-A10B (old suite pipeline only; no MoE side checks, per Neel).
