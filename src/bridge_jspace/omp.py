"""Non-negative orthogonal matching pursuit over a dictionary of unit atoms."""

import numpy as np
import torch
from scipy.optimize import nnls


@torch.no_grad()
def nonneg_omp(dictionary: torch.Tensor, x: torch.Tensor, k: int) -> tuple[torch.Tensor, torch.Tensor]:
    """Greedy non-negative sparse code of x [d] in the rows of `dictionary` [n, d] (unit rows).

    Each step adds the atom most positively correlated with the current residual, then refits all chosen atoms by
    non-negative least squares. Stops after k atoms or when no atom correlates positively. Returns
    (atom indices [m], coefficients [m]) with m <= k and every coefficient > 0, so x ~ coefs @ dictionary[indices].
    """
    x = x.float()
    chosen: list[int] = []
    coefs = np.zeros(0)
    residual = x.clone()
    for _ in range(k):
        scores = dictionary @ residual
        if chosen:
            scores[chosen] = -torch.inf
        best = int(scores.argmax())
        if scores[best] <= 0:
            break
        chosen.append(best)
        atoms = dictionary[chosen].double().cpu().numpy()  # [m, d]
        coefs, _ = nnls(atoms.T, x.double().cpu().numpy())
        residual = x - torch.from_numpy(coefs @ atoms).to(x)
    keep = [i for i, c in enumerate(coefs) if c > 0]
    indices = torch.tensor([chosen[i] for i in keep], dtype=torch.long, device=dictionary.device)
    return indices, torch.tensor(coefs[keep], dtype=torch.float32, device=dictionary.device)
