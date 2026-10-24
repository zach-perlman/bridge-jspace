"""x0_atoms: the ordered OMP and the atom marks (no model)."""

import torch

from scripts import x0_atoms as A

CASE = {"context": "Peter picked the rabbit. The locker of the tick is 2. Noah picked the tick. Iris picked the frog.",
        "cf_context": "Peter picked the rabbit. The locker of the tick is 2. Noah picked the frog. Iris picked the tick.",
        "bridge": "frog", "cf_bridge": "tick"}  # fmt: skip


def test_marks():
    assert [A.mark(t, CASE) for t in (" frog", "tick", " Noah", "Iris", " Peter", " locker", " zebra", " ", "2", " five")] == [
        "bridge_org", "bridge_alt", "other_person", "asked_person", "name", "context", "other", "other", "digit",
        "number_word"]  # fmt: skip


def test_ordered_omp_recovers_a_sparse_signal():
    g = torch.Generator().manual_seed(0)
    dic = torch.nn.functional.normalize(torch.randn(200, 64, generator=g), dim=-1)
    x = 3.0 * dic[7] - 2.0 * dic[42] + 0.5 * dic[3]
    sel, fits = A.ordered_omp(dic, x, 5, (3, 5))
    assert sel[:3] == [7, 42, 3]
    coef3, share3 = fits[3]
    assert torch.allclose(torch.tensor(coef3), torch.tensor([3.0, -2.0, 0.5]), atol=1e-4) and abs(share3 - 1) < 1e-5
