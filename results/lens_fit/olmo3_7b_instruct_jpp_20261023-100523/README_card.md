---
license: apache-2.0
base_model: allenai/Olmo-3-7B-Instruct
tags:
  - interpretability
  - jacobian-lens
  - logit-lens
---

# J++ lens for Olmo-3-7B-Instruct (every layer)

A J++ (Jacobian) lens for [allenai/Olmo-3-7B-Instruct](https://huggingface.co/allenai/Olmo-3-7B-Instruct) at revision `6e5971d9eba42665f5bd5a0fcf047f299ce1dccc`, fit at every source layer 0-30. The target is the final block (layer 31).

The lens we used for this model before is a plain J-lens at layers 0, 3, ..., 30 ([mhough/olmo3-jacobian-lenses](https://huggingface.co/mhough/olmo3-jacobian-lenses), `lenses/olmo-3-7b-instruct.pt`); this one is J++, fit with the published recipe.

## Limitations (read these first)

- **One fit, one seed.** One fit with router seed 0; no second fit or seed has been compared, so the evaluation below has no intervals.
- **64 prompts, one shard.** The Jacobians were fit on 64 WikiText prompts x 128 tokens (the first 16 positions skipped) in one shard.
- **Only the recipe's held-out evaluation so far.** Our own positive controls had not been run on this lens when this card was written.
- **fp16.** The Jacobians are stored in fp16 (largest per-layer relative (Frobenius) error from the cast 2.2e-04); cast them to fp32 before use.

## Recipe

[safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) @ `93f02cd`, unpatched:

- router: 64 WikiText prompts, 8 clusters, seed 0
- J++ fit (`fit-shard`): 64 WikiText prompts x 128 tokens in one shard; the first 16 positions skipped; target = the final block (layer 31); LRP rules (`rlens`); Jacobian rows per pass 16
- `merge-experts`: 8 experts, and the pooled lens (the baseline below)
- readout weights (`fit-weights`): the recipe's `fit:0` items with this model's correctness grades (55 items)
- evaluation (`evaluate --items held-out:0`): 227 held-out items
- run: 2026-10-22 to 2026-10-23 (UTC), on one NVIDIA A100 80GB PCIe (3.1 h for the whole job)

## File

`Olmo-3-7B-Instruct_jpp_lens.pt` (1.04 GB), sha256 `6847cfb38a14d7cf0049efff80364d051d69ec91998e44177e7fb5b4b9732451`

A `torch.save` dict in the same layout as neuronpedia's published lenses:

```python
{
  "J": {layer: Tensor[d, d] fp16, ...},  # layers 0-30, d = d_model
  "source_layers": [0, ..., 30],
  "d_model": 4096,
  "n_prompts": 64,
  "provenance": {...},  # source config and fit note
}
```

## Usage

To read out the residual stream `h` at `layer`, map it to the final layer, then apply the model's final norm and unembedding:

```python
import torch

lens = torch.load("Olmo-3-7B-Instruct_jpp_lens.pt", map_location="cpu", weights_only=True)
h_final = h.float() @ lens["J"][layer].float().T
logits = lm_head(final_norm(h_final))  # the model's final RMSNorm, then lm_head
```

## Evaluation (held-out items)

pass@10 on the recipe's held-out items (`evaluate --items held-out:0`, with this model's correctness grades), item-weighted, over the same source layers, against the recipe's pooled lens fit in the same run:

| eval | items | this lens | pooled lens |
|---|---|---|---|
| association | 77 | 0.09 | 0.06 |
| multihop | 12 | 0.83 | 0.67 |
| multilingual | 20 | 0.45 | 0.41 |
| poetry | 41 | 0.10 | 0.05 |
| typo | 77 | 0.99 | 0.77 |
| **macro** (mean over evals) | 227 | **0.492** | **0.391** |

One fit (seed 0) evaluated once; no intervals.

## Provenance

J++ for allenai/Olmo-3-7B-Instruct: safety-research/jpp_lens@93f02cd, 64 WikiText prompts x 128 tokens, skip 16, router seed 0, target = the last block, rlens LRP, 8 experts, source layers 0-30; fit 22-23 Oct 2026 on an A100 80GB. Fit for the bridge-jspace project (Dan Orel, MATS) with `scripts/lens_fit/fit_jpp.sh` and exported with `scripts/lens_fit/export_jpp_lens.py` at bridge-jspace commit `9cb180a`. Use it at your own risk: it has been checked only against the evaluation above.
