# Per-model setup grid (2026-10-21, Zach)

Legend: ✅ identical · ≈ identical at matched relative depth · ⚠️ differs, explained · ❌ gap (fixable; unfair as it stands)

## 1. Model and lens

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | |
|---|---|---|---|---|
| Role | headline | second family | dense control (architecture) | |
| Layers | 64 | 60 | 64 | |
| Attention | hybrid linear + full | sliding + global | full, every layer | ⚠️ by design |
| Post-trained chat model | yes | yes | yes | ✅ |
| Lens | J++, published (Neuronpedia) | J++, our fit, layers 0-58 | J++, our fit, layers 0-62 | ⚠️ who fit it |
| Lens fit data | WikiText (count not recorded) | WikiText, 64 prompts | WikiText, **32 prompts** | ❌ |
| Lens quality gate | none (published) | held-out pass@10 >= 0.48, layers 24-45 | held-out pass@10 >= 0.45 | ⚠️ |
| Model's loss on the lens-fit text | 2.33 nats | **7.66 nats** (not our harness) | to come (text-loss run) | ⚠️ Gemma off-distribution |

## 2. Data

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | |
|---|---|---|---|---|
| Items | full_v8 (two-step), full_v8b (three-step) | same files | same files | ✅ |
| Eligibility | own competence, every check right | same rule | same rule | ✅ |
| Two-step pools PP/PM, MP/MM, CP/CM | 152, 101, 144 | 141, 92, 128 | after its competence | ✅ by ability |
| Three-step pools per word | 48-133 | 74-183 | after its competence | ✅ by ability |
| Guess prompts (guessable split) | yes | yes | yes | ✅ |
| Prompts | raw text + own chat template, thinking off | same (+ BOS) | same | ✅ |
| Data seeds | 1 | 1 | 1 | ✅ (all single) |

## 3. C1: knock-out

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | |
|---|---|---|---|---|
| Removal | paper10 + rotated, same code | same | same | ✅ |
| Bands | 12-20, 20-28, 32-40, 0-62 | 11-19, 19-27, 30-38, 0-58 | as 27B | ≈ |
| Rule band | 32-40 | 30-38 | 32-40 | ≈ |
| Two-step C1 | done (B200) | queued | queued | ⚠️ hardware |
| Margin-matched gap | done | automatic | automatic | ✅ |
| Specificity (unembed10), narrow bands | queued | queued | queued | ✅ |
| Keep-own kill test | queued | queued | queued | ✅ |
| Two more control seeds | queued | queued | queued | ✅ |
| Position split | queued | queued | queued | ✅ |
| Each step alone, two-step | done (B200) | queued | queued | ✅ |
| Three-step: whole, each step | done | queued | queued | ✅ |
| Dose curve K = 1-100 (full_v8) | **missing** (old suite only) | queued | queued | ❌ |
| Single-layer small doses | **missing** | queued (34, 15) | queued (36, 16) | ❌ |
| Rotated control draw | B200 GPU RNG (headline); CPU since | CPU | CPU | ⚠️ benign |

## 4. C2: steering

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | |
|---|---|---|---|---|
| Band / single layers / early | 28-40 / every 2nd / 16, 20, 24 | 26-38 / every 2nd / 15, 19, 23 | as 27B | ≈ |
| Positions | question, final | same | same | ✅ |
| Two-step steering | full pools | full pools | full pools | ✅ |
| Ceiling (joint copy) | stacked; paste re-measure queued | paste | paste | ✅ once it runs |
| C2-relative rule | designed after seeing 27B data: clean test = fresh cases only | clean | clean | ⚠️ |
| Positive control | suite run passes (R, B, M->M 100%); reported | queued; **binding** | queued; binding not set | ⚠️ decide |
| Three-step steering | n = 40/word, **no ceiling** (older code) | n = 40/word + paste ceiling | same | ❌ |
| Copy sweep | v1 withdrawn; band v2 queued | band | band | ✅ once it runs |

## 5. Other checks and execution

| | Qwen3.6-27B | Gemma 4 31B-it | Qwen3-32B | |
|---|---|---|---|---|
| Plain-text loss under knock-out | 3 layers (32, 36, 40) | 9 layers (30-38) | 9 layers (32-40) | ❌ |
| Hardware | B200 + H200 (gate: 98.6% unedited, 100% at 32-40) | H200 | H200 | ⚠️ |

Not on this pipeline: Qwen3.5-9B and Qwen3.5-122B-A10B ran only the older suite pipeline (2026-10-19/20); their results are not comparable with these.
