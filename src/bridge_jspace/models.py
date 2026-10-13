"""Load a pinned HF model wrapped for jlens, and its pinned lenses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import jlens
import torch
from jlens import JacobianLens, LensModel
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel

from bridge_jspace.config import LensConfig, ModelConfig
from bridge_jspace.utils import resolve_dtype


@dataclass
class LoadedModel:
    hf: PreTrainedModel  # plain HF model, for parity checks against `lm`
    lm: LensModel  # jlens view of the same weights (residual blocks, unembed)

    @property
    def tokenizer(self):
        return self.lm.tokenizer

    @property
    def device(self) -> torch.device:
        return cast(nn.Embedding, self.hf.get_input_embeddings()).weight.device


def load_model(cfg: ModelConfig) -> LoadedModel:
    # Qwen3.5/3.6 checkpoints are *ForConditionalGeneration; AutoModelForCausalLM loads the
    # text-only *ForCausalLM from them, which is what the lenses were fitted on.
    tok = AutoTokenizer.from_pretrained(cfg.name, revision=cfg.revision)
    hf = AutoModelForCausalLM.from_pretrained(
        cfg.name, revision=cfg.revision, dtype=resolve_dtype(cfg.dtype), device_map=cfg.device_map
    )
    # HFLensModel implements LensModel at runtime; pyright rejects it only because the protocol
    # declares `layers` a mutable Sequence and nn.ModuleList is not a registered Sequence.
    return LoadedModel(hf=hf, lm=cast(LensModel, jlens.from_hf(hf, tok)))


def load_lens(cfg: LensConfig, n_layers: int, d_model: int, device: torch.device | str) -> JacobianLens:
    """Load a J-lens or J++ file (same format) and move its maps to `device` once.

    `JacobianLens.transport` otherwise copies J_l to the residual's device on every call.
    """
    lens = JacobianLens.from_pretrained(cfg.repo, filename=cfg.filename, revision=cfg.revision)
    if lens.d_model != d_model or not set(lens.source_layers) <= set(range(n_layers - 1)):
        raise ValueError(
            f"{cfg.filename} (d_model={lens.d_model}, layers={lens.source_layers[0]}..{lens.source_layers[-1]}) "
            f"does not fit a {n_layers}-layer model with d_model={d_model}"
        )
    lens.jacobians = {layer: J.to(device) for layer, J in lens.jacobians.items()}
    return lens
