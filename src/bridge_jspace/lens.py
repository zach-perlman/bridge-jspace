"""The pinned J-lens: per-layer maps J_l from layer l's residual to the final block's, read out as
logits = unembed(h @ J_l.T).

A token's J-lens vector at layer l is v_t = (g * W_U[t]) @ J_l, where g is the final norm's gain: <v_t, h> is the
token's lens logit up to the shared 1/rms scale. (The reference runner omits g; with it, the vector is the exact
direction of the lens logit.)
"""

import torch
from huggingface_hub import hf_hub_download

from . import pins
from .model import Model


class JLens:
    """`lens` picks the file in pins.LENS_SOURCES: "jlens" (the J-lens), "jpp" (J++), or workspace-lenses' "ws_jlens"
    and "ws_rlens" (same format: one J_l per layer)."""

    def __init__(self, model: Model, lens: str = "jlens"):
        source = pins.LENS_SOURCES[lens]
        if source[0] == "local":  # a lens we fit (pins.TARGETS): a file under the repo, checked by sha256
            _, file, sha256 = source
            path = pins.REPO_ROOT / file
            assert pins.sha256_file(path) == sha256, f"{path} changed"
        else:
            repo, file, revision = source
            path = hf_hub_download(repo, file, revision=revision)
        blob = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
        self.name, self.file_keys = lens, sorted(blob)
        self.source_layers: list[int] = list(blob["source_layers"])
        self._J_cpu: dict[int, torch.Tensor] = blob["J"]
        self._J_gpu: dict[int, torch.Tensor] = {}
        self.model = model
        self._gain = model.norm_gain()
        self._w_u = model.hf.lm_head.weight  # [vocab, d] bf16, cuda

    def J(self, layer: int) -> torch.Tensor:
        """J_l [d, d], fp32 on the GPU (kept after first use)."""
        if layer not in self._J_gpu:
            self._J_gpu[layer] = self._J_cpu[layer].to("cuda", torch.float32)
        return self._J_gpu[layer]

    def readout(self, h: torch.Tensor, layer: int) -> torch.Tensor:
        """Lens logits [..., vocab] for residuals h [..., d] at a layer."""
        return self.model.unembed(h.float() @ self.J(layer).T)

    @torch.no_grad()
    def vectors(self, layer: int, token_ids: torch.Tensor, unit: bool = True, chunk: int = 32768) -> torch.Tensor:
        """J-lens vectors [n, d] fp32 for token_ids at a layer, unit-normalised by default."""
        out = torch.empty(len(token_ids), self._w_u.shape[1], device="cuda")
        for s in range(0, len(token_ids), chunk):
            rows = (self._w_u[token_ids[s : s + chunk]].float() * self._gain) @ self.J(layer)
            out[s : s + chunk] = torch.nn.functional.normalize(rows, dim=-1) if unit else rows
        return out
