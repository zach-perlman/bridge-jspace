# Pre-registration: the attention-sink diagnostic (Zach, 2026-10-21 ~22:20 UTC)

Written before Gemma's test-set C1 (`gemma4itf_full2_ko_v1`, running) was opened. Seen so far: Gemma's held-out
ctrl_v8 band sweep (`gemma4itf_ctrl_sweep_v1`) and the 27B's partial ctrl_v8 sweep (`ctrl_sweep_v1`).

**Observation.** On Gemma 4 31B-it, the paper10 knock-out breaks lookup-final and memory-final words alike from
layer 24 on (ctrl_v8), while the same-size rotated control keeps 98-100%. On the 27B, lookups survive at 32-40.

**Hypothesis (H_sink).** The knock-out edits every position, including position 0, Gemma's BOS token, where Gemma keeps
the massive activations that act as an attention sink. Removing the top lens directions there can destroy the sink,
while a same-size rotated removal leaves it. Then Gemma's breakage is a property of the tool, not of its lookups.

**Variant ("nosink").** At every edited layer, the knock-out (and its rotated control) leaves untouched position 0 and
every position whose residual norm at that layer exceeds 10 times the median norm of that prompt's positions. Condition
names carry `_nosink` (`paper10_nosink`, `paper10_nosink_rot`, `unembed10_nosink`, ...). Everything else is unchanged.

**Diagnostic runs** (descriptive unless stated):
1. Gemma, ctrl_v8 (held-out; P->P, M->P, P->M, M->M, up to 100 each), layers 30-38, 40-48, 48-56: `paper10_nosink` and
   `paper10_nosink_rot`. **This run decides (rule below).**
2. Gemma plain-text loss (16 WikiText rows) at layers 30-38: top-1 and top-10 removal, with and without `_nosink`, and
   their rotated controls.
3. Gemma dose at layers 30-38 on ctrl_v8: top-1, top-2, top-5 and their rotated controls (no `_nosink`).
4. The 27B, ctrl_v8, layers 12-20 and 32-40: `paper10_nosink` and `paper10_nosink_rot` (does early-layer lookup damage
   on the 27B come from the sink too?).

**Decision rule (run 1).**
- **ARTIFACT** if at one or more of the three windows: P->P and M->P each keep >= 80% accuracy, every word's
  `paper10_nosink_rot` keeps >= 90%, and the memory-final words' mean loss exceeds the lookup-final words' by >= 30
  points.
- **NOT ARTIFACT** if P->P and M->P are both below 50% at all three windows.
- **MIXED** otherwise.

**What follows.**
- ARTIFACT: every model's C1 uses `_nosink` from here on (band choice on ctrl_v8 and every middle-band run). Gemma's
  band is re-chosen and its C1 core rerun under `_nosink`. The 27B's existing results stand if its test-set C1 gap at
  32-40 under `_nosink` is within 5 points of paper10's (36); otherwise its middle-band runs are redone under `_nosink`.
  Both protocols are reported for every model.
- NOT ARTIFACT or MIXED: the protocol stays paper10; Gemma's results are reported as they are, read with its plain-text
  and unembedding checks.
