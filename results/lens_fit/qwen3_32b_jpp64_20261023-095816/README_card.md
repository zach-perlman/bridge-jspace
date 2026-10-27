---
license: apache-2.0
base_model: Qwen/Qwen3-32B
tags:
  - interpretability
  - jacobian-lens
  - logit-lens
---

# J++ lens for Qwen3-32B (source layers 16-51)

A J++ (Jacobian) lens for [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) at revision
`9216db5781bf21249d130ec9da846c4624c16137`, fit at source layers 16-51. The final block (layer 63) is
the target.

The published lens for this model ([neuronpedia/jacobian-lens](https://huggingface.co/neuronpedia/jacobian-lens),
`qwen3-32b/jlens`) is a plain J-lens; this is a J++ fit with the published recipe on 64 prompts.

## Limitations (read these first)

- **Not every layer.** Only source layers 16-51 (36 of 63) have a J. Read other layers with
  another lens.
- **Fit in two shards.** The 64 prompts were fit as 2 shards x 32 prompts (one per GPU) with one shared router (seed 0,
  fit once on all 64 prompts), then merged with the recipe's `merge-experts`. On Qwen3.5-0.8B the same procedure (2 x 2
  prompts vs 1 x 4) gave identical experts and pooled lens (max relative difference 0).
- **One fit, one seed.** No second fit or seed has been compared.

## Recipe

[safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) @ `93f02cd`, unpatched:

- router: 64 WikiText prompts, seed 0
- J++ fit: 64 WikiText prompts x 128 tokens (2 shards x 32); the first 16 positions are skipped
- target = the final block; LRP rules (rlens); 8 experts; Jacobian rows per pass 10
- readout weights fit on the `fit:0` items, graded on this model

## File

`Qwen3-32B_jpp_lens.pt`, sha256 `7d6856b60c958ee7a088f4afed3ed39ffbc8b88b69ad5a7a3c7e33290e64e781`

A `torch.save` dict in the same layout as neuronpedia's published lenses:

```python
{
  "J": {layer: Tensor[d, d] fp16, ...},  # layers 16..51, d = d_model
  "source_layers": [16, ..., 51],
  "d_model": int,
  "n_prompts": 64,
  "provenance": {...},  # source config and fit note
}
```

To read out the residual stream `h` at `layer`, map it to the final layer and then apply the model's final norm and
unembedding:

```python
lens = torch.load("Qwen3-32B_jpp_lens.pt", map_location="cpu", weights_only=True)
h_final = h.float() @ lens["J"][layer].float().T
logits = lm_head(final_norm(h_final))  # the model's final RMSNorm, then lm_head
```

The jacobians were cast to fp16 for export; each layer's relative (Frobenius) error from the cast was printed at
export time.

## Evaluation (held-out items)

pass@10 on the recipe's held-out items (`evaluate --items held-out:0`), averaged within each item first (`pass_at_k_over_layers`), against the pooled lens fit in the same run:

| eval | Qwen3-32B_jpp_lens | pooled_lens |
|---|---|---|
| association | 0.40 | 0.11 |
| multihop | 0.64 | 0.38 |
| multilingual | 0.67 | 0.34 |
| poetry | 0.11 | 0.05 |
| typo | 0.94 | 0.69 |
| **macro** | **0.55** | **0.31** |

One fit (seed 0) evaluated once; no intervals.

## Provenance

J++ for Qwen/Qwen3-32B: safety-research/jpp_lens@93f02cd, 64 WikiText prompts x 128 tokens (2 shards x 32, one router, seed 0), skip 16, target = the last block, rlens LRP, 8 experts, source layers 16-51; fit 2026-10-22 on 2x H200. Fit for the bridge-jspace project (Dan Orel, MATS).
