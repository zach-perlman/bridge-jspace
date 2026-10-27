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


BOTHOFF_ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "no_both", "no_both_rand")


def test_extra_losses_without_the_control_arm():
    """Runs before --bothoff-ctrl have no no_alf_jrand rows; the extra losses still read."""
    rows = [{"scene": f"s{i}", "condition": "C0", "entity": f"e{i % 30}", "reader": w, "arm": a, "switched": 1}
            for i in range(60) for w in ("PP", "PM") for a in BOTHOFF_ARMS]  # fmt: skip
    assert {e["part"] for e in R.extra_losses(rows, ["C0"], 100)} == {"jpp", "alf", "both", "both - alf"}


def test_extra_losses_of_an_identity_run_read_planted_effects():
    """--identity runs (D1) have no union arm: the identity parts read, no 'both - alf' row."""
    arms = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "no_id", "no_id_rand", "no_idout",
            "no_idout_rand", "no_alfidout", "no_alfidout_rand", "no_jppalfidout", "no_jppalfidout_rand")  # fmt: skip
    rows, norms = [], []
    for i in range(80):
        for w in ("PP", "PM"):
            for a in arms:
                lost = (a == "no_jppalfidout" and w == "PP") or (a == "no_id" and w == "PM" and i % 4 == 0)
                rows.append({"scene": f"s{i}", "condition": "C0", "entity": f"e{i % 20}", "reader": w, "arm": a,
                             "switched": int(not lost)})  # fmt: skip
        norms.append({"condition": "C0", "share_id": 0.05, "share_jpp+alf+idout": 0.3})
    ex = {(e["reader"], e["part"]): e for e in R.extra_losses(rows, ["C0"], 100, norms)}
    assert {p for _, p in ex} == {"jpp", "alf", "id", "idout", "alf+idout", "jpp+alf+idout"}
    assert ex[("PP", "jpp+alf+idout")]["excess"][0] == 1.0 and ex[("PM", "id")]["excess"][0] == 0.25
    assert ex[("PP", "jpp+alf+idout")]["share"] == 0.3 and ex[("PP", "id")]["share"] == 0.05


def test_identity_direction_and_its_part_outside_jpp():
    jdic, _, x = _setup(4, n=5, d=40)
    g = torch.Generator().manual_seed(5)
    means = {e: torch.randn(40, generator=g) for e in ("frog", "tick", "duck")}
    pairs = [("frog", "tick"), ("tick", "duck"), ("duck", "frog"), ("frog", "duck"), ("tick", "frog")]
    u, u_out, atoms = R.identity_dirs(means, pairs, jdic, x, 5)
    assert torch.allclose(u.norm(dim=1), torch.ones(5), atol=1e-5)
    assert torch.allclose(u_out.norm(dim=1), torch.ones(5), atol=1e-5)
    d = means["tick"] - means["frog"]
    assert torch.allclose(u[0], d / d.norm(), atol=1e-5)  # mu_alt - mu_org
    for i in range(5):
        assert torch.allclose(jdic[atoms[i]] @ u_out[i], torch.zeros(5), atol=1e-4)  # nothing left along its atoms
    part = R.rank1_part(x, u)
    assert torch.allclose(x - part, x - (x @ u.T).diagonal()[:, None] * u, atol=1e-5)
    assert torch.allclose(((x - part) * u).sum(1), torch.zeros(5), atol=1e-4)


def test_span_part_projects_each_row_on_its_own_columns():
    _, alf, x = _setup(6, n=4, d=30, r=2)
    cols = [torch.cat([alf, x[i : i + 1].T], 1) for i in range(4)]
    part = R.span_part(x, cols)
    assert torch.allclose(part, x, atol=1e-4)  # each row lies in its own span
    assert torch.allclose(R.span_part(x, [alf] * 4), (x @ alf) @ alf.T, atol=1e-4)


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


def test_verdict_reports_keep_only_arms(tmp_path, monkeypatch):
    """--keeponly runs: the verdict gives route shares for the arms that add only one part of the change."""
    import json

    monkeypatch.setattr(R, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "fake"}, "layer": 12, "conditions": ["C2"]}))
    arms = ("whole", "keep_alf", "keep_alf_rand", "keep_jpp", "keep_jpp_rand")
    rows, norms = [], []
    for i in range(40):
        for a in arms:
            route = {"keep_alf": "position", "keep_jpp": "identity"}.get(a, "original")
            rows.append(
                {"scene": f"s{i}", "condition": "C2", "entity": f"e{i % 10}", "reader": "PP", "arm": a, "route": route}
            )
            rows.append(
                {"scene": f"s{i}", "condition": "C2", "entity": f"e{i % 10}", "reader": "PM", "arm": a, "switched": 0}
            )
        norms.append({"condition": "C2", "norm": 1.0})
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (src / "norms.jsonl").write_text("".join(json.dumps(r) + "\n" for r in norms))
    blob = json.loads((R.stage_verdict("fake", 100) / "verdict.json").read_text())
    share = {r["arm"]: r["share"] for r in blob["rows"]}
    assert share["keep_alf"]["position"][0] == 1.0 and share["keep_alf_rand"]["original"][0] == 1.0
    assert share["keep_jpp"]["identity"][0] == 1.0 and not blob["extra"] and not blob["ctrl"]
