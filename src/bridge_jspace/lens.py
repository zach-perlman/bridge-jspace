"""The pinned J-lens: per-layer maps J_l from layer l's residual to the final block's, read out as
logits = unembed(h @ J_l.T).

A token's J-lens vector at layer l is v_t = (g * W_U[t]) @ J_l, where g is the final norm's gain: <v_t, h> is the
token's lens logit up to the shared 1/rms scale. (The reference runner omits g; with it, the vector is the exact
direction of the lens logit.)
"""

import json
from pathlib import Path

import torch
from huggingface_hub import hf_hub_download

from . import pins
from .model import Model, to_device


def check_frozen(path: Path) -> None:
    """Assert the target's frozen lens file (pins.FROZEN_LENS: J++ on Qwen, the J-lens on OLMo) is the pinned one.
    Hashing 3.3 GB takes a minute or two, so a passed check is remembered (cache/frozen_lens_checked.json: the file's
    path, size and mtime) and redone only when the file changes."""
    st = path.stat()
    key = {"path": str(path.resolve()), "size": st.st_size, "mtime": st.st_mtime, "sha256": pins.FROZEN_LENS_SHA256}
    marker = pins.CACHE_DIR / "frozen_lens_checked.json"
    if marker.exists() and json.loads(marker.read_text()) == key:
        return
    assert pins.sha256_file(path) == pins.FROZEN_LENS_SHA256, f"{path} is not the frozen {pins.FROZEN_LENS} file"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps(key) + "\n")


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
            if lens == pins.FROZEN_LENS:  # the frozen lens: the exact file (README Decisions, 2026-10-19)
                check_frozen(Path(path))
        blob = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
        self.name, self.file_keys = lens, sorted(blob)
        self.source_layers: list[int] = list(blob["source_layers"])
        self._J_cpu: dict[int, torch.Tensor] = blob["J"]
        self._J_gpu: dict[tuple[int, torch.device], torch.Tensor] = {}
        self.model = model
        self._gain = model.norm_gain()  # home device
        self._w_u = model.hf.lm_head.weight  # [vocab, d] bf16, on the lm_head's GPU

    def J(self, layer: int, device: torch.device | None = None) -> torch.Tensor:
        """J_l [d, d], fp32 on `device` (default: the model's home device), kept per device after first use."""
        key = (layer, device or self.model.device)
        if key not in self._J_gpu:
            self._J_gpu[key] = self._J_cpu[layer].to(key[1], torch.float32)
        return self._J_gpu[key]

    def readout(self, h: torch.Tensor, layer: int) -> torch.Tensor:
        """Lens logits [..., vocab] (home device) for residuals h [..., d] at a layer; J_l is applied on h's device."""
        return self.model.unembed(h.float() @ self.J(layer, h.device).T)

    @torch.no_grad()
    def vectors(self, layer: int, token_ids: torch.Tensor, unit: bool = True, chunk: int = 32768) -> torch.Tensor:
        """J-lens vectors [n, d] fp32 on the home device for token_ids at a layer, unit-normalised by default."""
        home = self.model.device
        out = torch.empty(len(token_ids), self._w_u.shape[1], device=home)
        for s in range(0, len(token_ids), chunk):
            w_u = to_device(self._w_u[to_device(token_ids[s : s + chunk], self._w_u.device)], home)
            rows = (w_u.float() * self._gain) @ self.J(layer, home)
            out[s : s + chunk] = torch.nn.functional.normalize(rows, dim=-1) if unit else rows
        return out
