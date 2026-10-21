"""J-space removal for knock-out experiments (Zach, 2026-10-21; used by scripts/ablate_v2.py).

Every removal acts on a batch of residuals at one layer, h [B, T, d], with per-row settings, and leaves the positions
it is told to skip unchanged. Decided with Zach before the first run (2026-10-21):

  omp25     each position's 25-atom signed OMP fit over the unit J-lens vectors of letter tokens (ablate_pilot v1)
  paper10   Gurnee et al. 2026 §3.5.2 as we read it: at each position, the projection onto the span of the 10 unit
            J-lens vectors with the highest lens logits there, among letter tokens, never a protected token (the
            row's clean top-10 at the answer position)
  keep_own  omp25 with the row's own-word atoms never chosen: the bridge's surface tokens and every lens vector with
            cosine >= 0.5 to its concept vector at that layer (Phase 2c's definition)
Controls, for any removal:
  rotated removal     the same removal vector turned by a fixed random rotation (same size at every position)
  rotated dictionary  the same procedure over the lens dictionary turned by another fixed rotation: same atoms and
                      similarities between them, random orientation to the model

The lens dictionary is never materialised. With Wg = W_u[letters] * gain (shared by all layers), the unit lens vector
of token t at layer l is v_t = Wg[t] J_l / n_t, so v_t . x = Wg[t] . (J_l x) / n_t: two matmuls per score. The caller
enables TF32 for these (5.1x faster than fp32 on an H200, the same OMP atoms at the median; benchmarked 2026-10-21).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import torch

K_OMP = 25
K_PAPER = 10
SINK_RATIO = (
    10.0  # 2026-10-21 (docs/prereg_sink_1021.md): a position whose residual norm exceeds 10x the prompt's median
)
OWN_COS = 0.5


class LensDictionary:
    """Unit J-lens vectors of letter tokens at one layer, never materialised (see the module docstring)."""

    def __init__(self, wg: torch.Tensor, J: torch.Tensor, chunk: int = 32768):
        self.wg, self.J = wg, J  # wg [n, d] fp32, J [d, d] fp32, same device
        self.norms = torch.cat([(wg[s : s + chunk] @ J).norm(dim=-1) for s in range(0, wg.shape[0], chunk)])

    @property
    def n(self) -> int:
        return self.wg.shape[0]

    def logits(self, x: torch.Tensor) -> torch.Tensor:
        """[m, d] -> [m, n]: the lens logits up to a positive per-row factor (the final norm), so their ranking."""
        return (x @ self.J.T) @ self.wg.T

    def scores(self, x: torch.Tensor) -> torch.Tensor:
        """[m, d] -> [m, n]: dot products with the unit lens vectors."""
        return self.logits(x) / self.norms

    def atoms(self, idx: torch.Tensor) -> torch.Tensor:
        """Unit lens vectors for dictionary rows idx [...] -> [..., d]."""
        return (self.wg[idx] @ self.J) / self.norms[idx].unsqueeze(-1)


class RotatedDictionary:
    """A dictionary turned by a fixed orthogonal R: atoms v_t R, so x . v_t R = (x R^T) . v_t."""

    def __init__(self, base, R: torch.Tensor):
        self.base, self.R = base, R

    @property
    def n(self) -> int:
        return self.base.n

    def logits(self, x: torch.Tensor) -> torch.Tensor:
        return self.base.logits(x @ self.R.T)

    def scores(self, x: torch.Tensor) -> torch.Tensor:
        return self.base.scores(x @ self.R.T)

    def atoms(self, idx: torch.Tensor) -> torch.Tensor:
        return self.base.atoms(idx) @ self.R


class MatrixDictionary:
    """An explicit dictionary of unit rows [n, d] (v1's Gaussian control, and tests)."""

    def __init__(self, D: torch.Tensor):
        self.D = D

    @property
    def n(self) -> int:
        return self.D.shape[0]

    def logits(self, x: torch.Tensor) -> torch.Tensor:
        return x @ self.D.T

    def scores(self, x: torch.Tensor) -> torch.Tensor:
        return x @ self.D.T

    def atoms(self, idx: torch.Tensor) -> torch.Tensor:
        return self.D[idx]


Groups = list[tuple[torch.Tensor, torch.Tensor]]  # (row positions in the chunk, dictionary rows) pairs


def _mask(values: torch.Tensor, groups: Groups | None, fill: float) -> None:
    for pos, idx in groups or []:
        if pos.numel() and idx.numel():
            values[pos[:, None], idx[None, :]] = fill


def omp_fit(dic, x: torch.Tensor, k: int, banned: Groups | None = None, return_chosen: bool = False):
    """Signed OMP over dic for each row of x [m, d]: the least-squares fit on k atoms chosen greedily by |correlation|
    with the residual (exp04's signed_omp, batched, with per-row banned atoms)."""
    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    for _ in range(k):
        scores = dic.scores(x - approx).abs()
        _mask(scores, banned, -1.0)
        if chosen.shape[1]:
            scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dic.atoms(chosen).double()
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
    return (approx, chosen) if return_chosen else approx


def top_span_removal(dic, x: torch.Tensor, k: int, protected: Groups | None = None, return_chosen: bool = False):
    """The projection of each row of x [m, d] onto the span of the k unit atoms with the highest logits there, never a
    protected atom (paper10)."""
    logits = dic.logits(x.float())
    _mask(logits, protected, float("-inf"))
    top = logits.topk(k, dim=1).indices
    Q, _ = torch.linalg.qr(dic.atoms(top).transpose(1, 2).double())  # [m, d, k], orthonormal columns
    proj = (Q @ (Q.transpose(1, 2) @ x.double().unsqueeze(2))).squeeze(2).float()
    return (proj, top) if return_chosen else proj


@dataclass
class RowSettings:
    """Per batch row: positions left unedited, dictionary rows never removed (paper10: protected; keep_own: banned)."""

    skip: list[int] = field(default_factory=list)
    protected: torch.Tensor | None = None
    banned: torch.Tensor | None = None


def removal_edit(method: str, dic, rows: list[RowSettings], rotation: torch.Tensor | None = None,
                 k: int | None = None, chunk: int = 4096, skip_sinks: bool = False) -> Callable[[torch.Tensor], torch.Tensor]:  # fmt: skip
    """An edit h [B, T, d] -> h minus its removal, for method 'omp' (k atoms, rows' banned atoms never chosen) or 'top'
    (span of the k highest-logit atoms, rows' protected atoms never chosen); with rotation, the removal vector is turned
    by it before subtraction (the same-size control). Skipped positions are unchanged. With skip_sinks (2026-10-21,
    docs/prereg_sink_1021.md) position 0 and every position whose residual norm exceeds SINK_RATIO x the row's median
    are also left unchanged (attention sinks); edit.sinks counts [sink positions, positions] over calls."""
    k = k or (K_OMP if method == "omp" else K_PAPER)
    counts = [0, 0]

    def edit(h: torch.Tensor) -> torch.Tensor:
        B, T, d = h.shape
        x = h.reshape(B * T, d).float()
        keep = torch.ones(B * T, dtype=torch.bool, device=h.device)
        for b, row in enumerate(rows):
            if row.skip:
                keep[torch.tensor([b * T + p for p in row.skip], device=h.device)] = False
        if skip_sinks:
            norms = h.float().norm(dim=-1)  # [B, T]
            sink = norms > SINK_RATIO * norms.median(dim=1, keepdim=True).values
            sink[:, 0] = True
            keep &= ~sink.reshape(-1)
            counts[0] += int(sink.sum())
            counts[1] += B * T
        idx = keep.nonzero().squeeze(1)
        r = torch.zeros_like(x)
        for s in range(0, idx.numel(), chunk):
            sel = idx[s : s + chunk]
            owner = sel // T
            groups: Groups = []
            for b in owner.unique().tolist():
                ids = rows[b].banned if method == "omp" else rows[b].protected
                if ids is not None and ids.numel():
                    groups.append(((owner == b).nonzero().squeeze(1), ids))
            if method == "omp":
                r[sel] = omp_fit(dic, x[sel], k, banned=groups)
            elif method == "top":
                r[sel] = top_span_removal(dic, x[sel], k, protected=groups)
            else:
                raise ValueError(method)
        if rotation is not None:
            r = r @ rotation.T
        return (x - r).reshape(B, T, d)

    edit.sinks = counts
    return edit


def rotation(d: int, seed: int, device: str = "cuda") -> torch.Tensor:
    """A Haar-random orthogonal matrix [d, d], fixed by seed. 2026-10-21 (Zach): the Gaussian is drawn on the CPU, then
    moved: GPU random streams depend on the GPU type (the B200 and the H200 drew different rotations from one seed)."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    q, r = torch.linalg.qr(torch.randn(d, d, generator=g).to(device))
    return q * torch.sign(torch.diagonal(r))


@torch.no_grad()
def first_token_logits(
    model, ids: torch.Tensor, edits: dict[int, Callable[[torch.Tensor], torch.Tensor]], last: torch.Tensor | None = None
) -> torch.Tensor:
    """Final-position logits [B, vocab] (fp32) of one forward of ids [B, T] (one length), with each edit applied to
    its layer's block output for the whole batch. The same numbers as generate_batch's first step, up to kernel
    rounding; one call per batch instead of one edit call per row. With `last` ([B], 2026-10-21: right-padded batches
    of different lengths) each row's logits are read at its own last real position; the models are causal (attention,
    linear attention, causal conv), so padding after a prompt cannot change its earlier positions."""
    from bridge_jspace.model import _forward_hooks

    def hook_for(layer: int):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            new = edits[layer](h.float()).to(h.dtype)
            return (new, *out[1:]) if isinstance(out, tuple) else new

        return hook

    if last is None:
        with _forward_hooks([(model.layers[layer], hook_for(layer)) for layer in sorted(edits)]):
            out = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
        return out.logits[:, -1].float()
    keep = last.unique()  # sorted positions to keep; each row reads its own
    with _forward_hooks([(model.layers[layer], hook_for(layer)) for layer in sorted(edits)]):
        out = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=keep)
    col = torch.searchsorted(keep, last)
    return out.logits[torch.arange(ids.shape[0], device=ids.device), col].float()
