"""pointer_mechanism: the axis statistic, the dose-path landing classes, the subspace removal and the pre-registered
verdicts from fake rows."""

import torch

from scripts import pointer_mechanism as M


def test_axis_rho_orders_a_line_and_not_a_shuffle():
    line = torch.stack([torch.full((3, 4), float(i)) for i in range(5)])  # slots on a line
    rho, dist = M.axis_rho(line)
    assert rho > 0.99 and dist[0][4] > dist[0][1]
    perm = line[[0, 3, 1, 4, 2]]
    assert M.axis_rho(perm)[0] < 0.5


def test_landing_classes():
    assert M.landing(0, 3, 3) == "target"
    assert M.landing(0, 3, 1) == "between" and M.landing(0, 3, 2) == "between"
    assert M.landing(0, 3, 4) == "beyond"
    assert M.landing(2, 4, 1) == "other side" and M.landing(4, 1, 2) == "between"


def test_remove_deviation_only_inside_the_basis():
    basis = torch.eye(6)[:2]
    m = torch.zeros(1, 6)
    h = torch.arange(6, dtype=torch.float).reshape(1, 6)
    out = M.remove_deviation(h, m, basis)
    assert torch.equal(out[0, :2], torch.zeros(2)) and torch.equal(out[0, 2:], h[0, 2:])
    m2 = torch.ones(1, 6)
    assert torch.equal(M.remove_deviation(h, m2, basis)[0, :2], torch.ones(2))  # set to the grand mean's component


def row(test, **kw):
    base = {
        "id": kw.pop("id", "i0"),
        "family": kw.pop("family", "RL"),
        "asked": 0,
        "test": test,
        "heads": {h: 0 for h in M.HEADS},
    }
    return base | kw


def test_verdicts_from_fake_rows():
    geo = {"layers": {"48": {"rho": 0.9, "perm_p": 0.01}}, "words": {}}
    rows = []
    for i in range(40):
        rid = f"i{i}"
        rows.append(row("unedited", id=rid))
        for al, ans in ((0.25, 0), (0.5, 0), (1.0, 1), (1.5, 2), (2.0, 3), (3.0, 3)):  # passes 1, 2 on the way to 3
            rows.append(row("T2", id=rid, alpha=al, target=3, answered=ans))
        for al in (1.0, 2.0):
            rows.append(row("T3", id=rid, alpha=al, dir="slot", target=2, answered=2, heads={h: 2 for h in M.HEADS}))
            rows.append(row("T3", id=rid, alpha=al, dir="random", target=2, answered=0))
        for fam, kept_slot in (("RL", False), ("RR", True)):
            for b in ("slot4", "rand4", "var4"):
                rows.append(row("T4", id=f"{fam}{i}", family=fam, removed=b, kept=(b != "slot4") or kept_slot))
    a = M.analyse(rows, geo, 48)
    assert a["H-axis"]["holds"] and a["H-path"] and not a["H-jump"]
    assert a["T2"]["first_landing"] == {"between": 40}
    assert a["H-natural"] and a["H-reader"] and a["H-necessary"]
