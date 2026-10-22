# write_max --prefix-cache check (2026-10-22): not adopted

The unedited prompt prefix computed once and reused (model.first_logits_prefix), against the full runs, on the same jobs.

| Run | Cases | Role agreement | Max abs dld |
|---|---|---|---|
| Qwen3.5-9B, batch 16 (b) | 6 | 99.57% | 0.375 |
| Qwen3.5-9B, batch 16 (c) | 8 | **99.48% (bar 99.5%)** | 0.375 |

- **Speed (c):** 117 s full vs 100 s prefix (1.17x). The prompts are short (67-138 tokens), so per-batch overhead
  dominates (per-row edit hooks, kernel launches, the generate wrapper), not tokens.
- **Conditions:** the GPU was shared with two other jobs.
- **Decision:** off by default; not used by any run.
