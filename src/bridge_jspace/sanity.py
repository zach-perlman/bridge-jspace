"""Checks to pass on every new model / pod before trusting any lens readout.

Each check returns {"passed": bool, ...diagnostics}.
"""

from __future__ import annotations

from typing import Any

import torch
from jlens import JacobianLens

from bridge_jspace.models import LoadedModel
from bridge_jspace.readout import readout_logits, residuals


@torch.no_grad()
def check_known_fact(m: LoadedModel, prompt: str, expected: str) -> dict[str, Any]:
    """The model's own top-1 next token after `prompt` decodes to `expected` (weights loaded right)."""
    ids = m.lm.encode(prompt)
    top = int(m.hf(input_ids=ids).logits[0, -1].argmax())
    got = m.tokenizer.decode([top])
    return {"passed": got == expected, "prompt": prompt, "expected": expected, "got": got}


@torch.no_grad()
def check_hf_parity(m: LoadedModel, prompts: list[str], atol: float) -> dict[str, Any]:
    """Final norm + unembed of the hooked last block == the plain HF forward's logits.

    Fails if the hooks sit on the wrong modules or the block output is not the residual.
    """
    final = m.lm.n_layers - 1
    worst, agree = 0.0, []
    for p in prompts:
        ids = m.lm.encode(p)
        ours = m.lm.unembed(residuals(m.lm, ids, [final])[final]).float()
        ref = m.hf(input_ids=ids).logits[0].float().to(ours.device)
        worst = max(worst, (ours - ref).abs().max().item())
        agree.append((ours.argmax(-1) == ref.argmax(-1)).float().mean().item())
    argmax_agreement = min(agree)
    return {
        "passed": worst <= atol and argmax_agreement == 1.0,
        "max_abs_diff": worst,
        "argmax_agreement": argmax_agreement,
    }


@torch.no_grad()
def check_reference_readout(m: LoadedModel, lens: JacobianLens, prompt: str, atol: float = 1e-3) -> dict[str, Any]:
    """Our readout == jlens's own `JacobianLens.apply` at every fitted layer, last position."""
    ref, _, ids = lens.apply(m.lm, prompt, positions=[-1])
    resid = residuals(m.lm, ids, lens.source_layers)
    worst = max(
        (readout_logits(m.lm, lens, resid[layer][[-1]], layer).cpu() - ref[layer]).abs().max().item()
        for layer in lens.source_layers
    )
    return {"passed": worst <= atol, "max_abs_diff": worst}


def run_gate(
    m: LoadedModel,
    lenses: dict[str, JacobianLens],
    fact_prompt: str,
    fact_expected: str,
    parity_prompts: list[str],
    parity_atol: float,
) -> dict[str, dict[str, Any]]:
    """All checks an experiment must pass before trusting a readout; keyed by check name."""
    checks = {
        "known_fact": check_known_fact(m, fact_prompt, fact_expected),
        "hf_parity": check_hf_parity(m, parity_prompts, parity_atol),
    }
    for name, lens in lenses.items():
        checks[f"reference_readout_{name}"] = check_reference_readout(m, lens, parity_prompts[0])
    return checks
