"""The coordinate clamp swap (the reference runner's intervention), as a residual edit at one layer.

Atoms are rows A [K, d], generally non-orthogonal. A residual's coordinates are c = h @ pinv(A) [K]. The clamp sets
them to targets c* and changes nothing orthogonal to span(A):  h <- h + (c* - c) @ A.  The swap's targets are the
clean pass's coordinates with atoms 0 (source) and 1 (target) exchanged; any further atoms keep their clean values,
which is how J-space coordinates are held fixed.

By default every position except 0 is edited (position 0 is the attention sink, whose large-norm residual makes the
coordinates unstable); `positions` restricts the edit to some of them.
"""

import torch

NEAR_PARALLEL = 0.999  # |cos| of the two swapped atoms above which the layer is skipped (ill-conditioned pinv)


def near_parallel(a: torch.Tensor, b: torch.Tensor) -> bool:
    return abs(float(torch.nn.functional.cosine_similarity(a, b, dim=0))) > NEAR_PARALLEL


class SwapClamp:
    """Edit for one layer: swap atoms 0 and 1, pin atoms 2.. at their clean coordinates. With swap=False every atom
    is pinned at its clean value (a no-op on the clean pass; used as a check).

    With `null_direction` (unit [d]), the edit at each position is replaced by that direction scaled to the edit's
    own norm: the matched-norm random-direction control. `positions` (indices into the sequence, none of them 0)
    restricts the edit to those positions; None edits every position from 1.
    """

    def __init__(
        self,
        atoms: torch.Tensor,
        clean_h: torch.Tensor,
        null_direction: torch.Tensor | None = None,
        swap: bool = True,
        positions: list[int] | None = None,
    ):
        self.atoms = atoms.float()  # [K, d]
        self.pinv = torch.linalg.pinv(self.atoms)  # [d, K]
        clean_coords = clean_h[1:].float() @ self.pinv  # [P, K]
        self.targets = clean_coords.clone()
        if swap:
            self.targets[:, [0, 1]] = clean_coords[:, [1, 0]]
        self.null_direction = null_direction
        self.mask = torch.ones(len(clean_h) - 1, dtype=torch.bool, device=clean_h.device)  # over positions 1..
        if positions is not None:
            assert positions, "positions must be non-empty"
            assert 0 not in positions, "position 0 is never edited"
            self.mask[:] = False
            self.mask[[p - 1 for p in positions]] = True
        self.edit_ratio_last = float("nan")  # |edit| / |h| at the final position, from the latest call
        self.edit_ratio_edited = float("nan")  # mean |edit| / |h| over the edited positions, from the latest call

    def delta(self, h: torch.Tensor) -> torch.Tensor:
        """The edit [P, d] for positions 1.. of h [seq, d]."""
        delta = (self.targets - h[1:] @ self.pinv) @ self.atoms
        if self.null_direction is not None:
            delta = delta.norm(dim=-1, keepdim=True) * self.null_direction
        return delta * self.mask[:, None]

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        delta = self.delta(h)
        self.edit_ratio_last = float(delta[-1].norm() / h[-1].norm())
        ratios = delta.norm(dim=-1) / h[1:].norm(dim=-1)
        self.edit_ratio_edited = float(ratios[self.mask].mean())
        out = h.clone()
        out[1:] += delta
        return out
