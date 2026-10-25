"""x6_routes --bothoff: the union of the J++ atoms and the pointer directions, and the extra losses read planted effects."""

import torch

from scripts import x6_routes as R
from scripts.exp04_brew_parts import signed_omp


def _setup(seed=0, n=6, d=40, atoms=60, r=3):
    g = torch.Generator().manual_seed(seed)
    jdic = torch.randn(atoms, d, generator=g)
    jdic = jdic / jdic.norm(dim=1, keepdim=True)
    alf, _ = torch.linalg.qr(torch.randn(d, r, generator=g))
    return jdic, alf, torch.randn(n, d, generator=g)


def test_union_holds_both_parts():
    jdic, alf, x = _setup()
    both = R.union_part(jdic, alf, x, 5)
    share = lambda p: p.norm(dim=1) ** 2 / x.norm(dim=1) ** 2  # noqa: E731
    ptr = (x @ alf) @ alf.T
    jpp = signed_omp(jdic, x, 5)
    assert (share(both) >= share(ptr) - 1e-5).all() and (share(both) >= share(jpp) - 1e-5).all()
    assert (share(both) <= 1 + 1e-5).all()
    assert torch.allclose(((x - both) @ alf), torch.zeros(x.shape[0], alf.shape[1]), atol=1e-4)  # nothing left in Alf


def test_union_without_pointer_directions_is_the_jpp_part():
    jdic, alf, x = _setup(1)
    zero = torch.zeros_like(alf)
    assert torch.allclose(R.union_part(jdic, zero, x, 5), signed_omp(jdic, x, 5), atol=1e-4)


def test_extra_losses_read_planted_effects():
    rows, norms = [], []
    for i in range(120):
        for w in ("PP", "PM"):
            for a in R.ARMS:
                lost = (w == "PP" and a == "no_both") or (w == "PP" and a == "no_alf" and i % 2 == 0)
                rows.append({"scene": f"s{i}", "condition": "C0", "entity": f"e{i % 30}", "reader": w, "arm": a,
                             "switched": int(not lost)})  # fmt: skip
        norms.append({"condition": "C0", "share_jpp": 0.1, "share_alf": 0.02, "share_both": 0.12})
    ex = {(e["reader"], e["part"]): e for e in R.extra_losses(rows, ["C0"], 200, norms)}
    assert ex[("PP", "both")]["excess"][0] == 1.0 and ex[("PP", "alf")]["excess"][0] == 0.5
    assert abs(ex[("PP", "both - alf")]["excess"][0] - 0.5) < 1e-9
    assert ex[("PM", "both - alf")]["excess"][0] == 0.0 and ex[("PP", "jpp")]["excess"][0] == 0.0
    assert ex[("PP", "both")]["share"] == 0.12


def test_extra_losses_without_the_control_arm():
    """Runs before --bothoff-ctrl have no no_alf_jrand rows; the extra losses still read."""
    rows = [{"scene": f"s{i}", "condition": "C0", "entity": f"e{i % 30}", "reader": w, "arm": a, "switched": 1}
            for i in range(60) for w in ("PP", "PM") for a in R.ARMS if a != "no_alf_jrand"]  # fmt: skip
    assert {e["part"] for e in R.extra_losses(rows, ["C0"], 100)} == {"jpp", "alf", "both", "both - alf"}


def test_random_union_holds_the_pointer_and_the_share():
    _, alf, x = _setup(2, n=8, d=40)
    basis, _ = torch.linalg.qr(torch.randn(40, 40, generator=torch.Generator().manual_seed(3)))
    share = torch.full((8,), 0.3)
    part = R.union_rand_part(alf, x, share, basis)
    assert torch.allclose(((x - part) @ alf), torch.zeros(8, alf.shape[1]), atol=1e-4)  # nothing left in the pointer
    k = R.random_k(x, share, basis)
    rand = (x @ basis[:, : int(k[0])]) @ basis[:, : int(k[0])].T
    assert part[0].norm() ** 2 >= rand[0].norm() ** 2 - 1e-4  # holds at least the random part's energy


def test_ctrl_losses_read_planted_effects():
    rows = []
    for i in range(100):
        for w in ("PP", "PM"):
            for a in ("whole", "no_alf", "no_both", "no_alf_jrand"):
                lost = w == "PP" and (a == "no_both" or (a == "no_alf_jrand" and i % 4 == 0))
                rows.append({"scene": f"s{i}", "condition": "C0", "entity": f"e{i % 25}", "reader": w, "arm": a,
                             "switched": int(not lost)})  # fmt: skip
    c = {(r["reader"], r["arm"]): r["lost"][0] for r in R.ctrl_losses(rows, ["C0"], 100)}
    assert c[("PP", "alf + J++")] == 1.0 and c[("PP", "alf + random (J++ share)")] == 0.25
    assert abs(c[("PP", "alf + J++ - alf + random")] - 0.75) < 1e-9 and c[("PM", "alf + J++ - alf + random")] == 0.0
