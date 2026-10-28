"""Batch 47, test 47.1 (scripts/x47_atoms.py; x6_routes and x0_necessity --atom-slices): the new parts on synthetic
tensors (the 26-100 slice, the random lens atoms at their own and at the slice's share, the cos^2 with U), the sealed
stages, the rule on planted rows at its bars, and the verdict with its verify-pack view on planted runs. No GPU."""

import json
import sys
from types import SimpleNamespace

import pytest
import torch

from scripts import x0_necessity as X
from scripts import x0_parts as XP
from scripts import x6_routes as R
from scripts import x47_atoms as A

LK, RC = X.LOOKUP, X.RECALL


def _dic(seed: int = 0, atoms: int = 400, d: int = 160) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    dic = torch.randn(atoms, d, generator=g)
    return dic / dic.norm(dim=1, keepdim=True)


def _setup(n: int = 4, seed: int = 1, d: int = 160):
    jdic = _dic(seed, d=d)
    x = torch.randn(n, d, generator=torch.Generator().manual_seed(seed + 1))
    atoms = XP.omp_atoms(jdic, x, 100)
    fits = {k: X.fit(jdic, x, k, "signed") for k in (25, 100)}
    alf, _ = torch.linalg.qr(torch.randn(d, 4, generator=torch.Generator().manual_seed(seed + 2)))
    return jdic, x, atoms, fits, alf, [f"C2-{i:04d}" for i in range(n)]


def _span(cols: torch.Tensor) -> torch.Tensor:
    return R.orthonormal(cols)


# ---- the parts ---------------------------------------------------------------------------------------------------


def test_random_atoms_are_seeded_distinct_and_outside_the_picks():
    picked = list(range(0, 200, 2))
    a = A.random_atoms(400, picked, "C2-0001")
    assert len(a) == 75 == len(set(a)) and not set(a) & set(picked) and all(0 <= i < 400 for i in a)
    assert a == A.random_atoms(400, picked, "C2-0001")  # the same scene: the same draw
    assert a != A.random_atoms(400, picked, "C2-0002") and a != A.random_atoms(400, picked, "C2-0001", seed=1)
    with pytest.raises(AssertionError, match="fewer than 75"):
        A.random_atoms(170, picked, "C2-0001")


def test_atom_slices_decompose_the_k100_fit():
    jdic, x, atoms, fits, alf, scenes = _setup()
    parts, recs = A.atom_slices(jdic, x, scenes, fits[25], fits[100], atoms, alf)
    assert set(parts) == set(A.SLICE_KEYS) and all(v.shape == x.shape and v.dtype == x.dtype for v in parts.values())
    assert torch.allclose(parts["jpp26_100"], fits[100] - fits[25])
    # removing 1-25 and 26-100 removes exactly 1-100
    assert torch.allclose((x - fits[25]) - parts["jpp26_100"], x - fits[100], atol=1e-5)
    for i, r in enumerate(recs):
        q25 = _span(jdic[atoms[i, :25]].T)
        sl = parts["jpp26_100"][i].double()
        assert float((q25.T @ sl).norm()) < 1e-4 * float(sl.norm())  # orthogonal to atoms 1-25: 1-25 kept
        assert r["share_1_25"] + r["share_26_100"] == pytest.approx(r["share_1_100"], abs=1e-5)
        ids = r["ratoms75_atoms"]
        assert ids == A.random_atoms(jdic.shape[0], atoms[i].tolist(), scenes[i]) and r["ratoms_seed"] == A.RATOM_SEED
        rp = jdic[ids].T.double()
        q = _span(rp - q25 @ (q25.T @ rp))  # the random atoms off atoms 1-25
        own = parts["ratoms75own"][i].double()
        assert torch.allclose(own, q @ (q.T @ x[i].double()), atol=1e-4)
        assert float((q25.T @ own).norm()) < 1e-4 * float(own.norm())
        total = float(x[i].norm() ** 2)
        assert r["share_ratoms75own"] == pytest.approx(float(own.norm() ** 2) / total, abs=1e-5)
        scaled = parts["ratoms75"][i].double()
        assert float(scaled.norm() ** 2) / total == pytest.approx(r["share_26_100"], rel=1e-4)  # the slice's share
        assert r["ratoms75_alpha"] == pytest.approx((r["share_26_100"] / r["share_ratoms75own"]) ** 0.5, rel=1e-4)
        assert torch.allclose(scaled, own * r["ratoms75_alpha"], rtol=1e-4, atol=1e-5)  # the same direction
        assert 0.0 <= r["cos2_U_jpp26_100"] <= 1.0 and 0.0 <= r["cos2_U_ratoms75"] <= 1.0
        assert r["slice_off_1_25"] < 1e-5 and r["slice_out_of_1_100"] < 1e-5  # recorded: rounding only


def test_slices_with_geometry_adds_the_spans_cos2_and_they_add_up():
    jdic, x, _, fits, alf, scenes = _setup(seed=3)
    _, recs = A.slices_with_geometry(jdic, x, scenes, fits[25], fits[100], alf)
    for r in recs:
        assert {"cos2_U_jpp25", "cos2_U_jpp100", "cos2_U_jpp26_100", "cos2_U_ratoms75"} <= set(r)
        assert not any(k.startswith("cos2_id") for k in r)
        # span(1-100) = span(1-25) + (26-100 off 1-25), orthogonally: the cos^2 with U add up
        assert r["cos2_U_jpp25"] + r["cos2_U_jpp26_100"] == pytest.approx(r["cos2_U_jpp100"], abs=1e-5)


def test_cos2_of_a_slice_inside_u_is_one():
    d = 200
    jdic = torch.eye(d)[:180]  # coordinate atoms
    x = torch.zeros(1, d)
    x[0, :100] = torch.linspace(10, 1, 100)
    atoms = XP.omp_atoms(jdic, x, 100)
    assert atoms[0].tolist() == list(range(100))
    fits = {k: X.fit(jdic, x, k, "signed") for k in (25, 100)}
    alf = torch.eye(d)[:, 30:34]  # U inside atoms 26-100
    parts, recs = A.atom_slices(jdic, x, ["s0"], fits[25], fits[100], atoms, alf)
    assert recs[0]["cos2_U_jpp26_100"] == pytest.approx(1.0) and recs[0]["share_ratoms75own"] == pytest.approx(0.0)
    assert recs[0]["ratoms75_alpha"] is None and torch.equal(parts["ratoms75"], torch.zeros_like(x))  # nothing to scale
    assert recs[0]["cos2_U_ratoms75"] == pytest.approx(0.0)  # random atoms from 100-179: off U


def test_slice_check_catches_a_part_outside_atoms_1_100():
    jdic, x, atoms, fits, alf, scenes = _setup(seed=5)
    bad = fits[100] + 0.5 * torch.randn(x.shape, generator=torch.Generator().manual_seed(9))
    with pytest.raises(AssertionError, match="26-100 slice"):
        A.atom_slices(jdic, x, scenes, fits[25], bad, atoms, alf)


def test_the_routes_arms_are_named_in_arms():
    jdic, x, _, fits, alf, scenes = _setup(seed=7)
    parts, _ = A.slices_with_geometry(jdic, x, scenes, fits[25], fits[100], alf)
    basis, _ = torch.linalg.qr(torch.randn(x.shape[1], x.shape[1], generator=torch.Generator().manual_seed(8)))
    arms, sh = R.removal_arms(x, parts, basis)
    assert set(arms) == {f"no_{p}{s}" for p in A.SLICE_KEYS for s in ("", "_rand")} and set(arms) <= set(R.ARMS)
    assert set(A.ROUTE_ARMS) <= {"whole", *R.ARMS}
    assert torch.allclose(sh["ratoms75"], sh["jpp26_100"], rtol=1e-4)  # same share, so the same random part
    assert torch.allclose(arms["no_ratoms75_rand"], arms["no_jpp26_100_rand"], atol=1e-5)


# ---- the run flags -----------------------------------------------------------------------------------------------


@pytest.mark.parametrize(("flags", "on"), [([], False), (["--jpp-ks", "25", "100", "--atom-slices"], True)])
def test_routes_main_passes_atom_slices(monkeypatch, flags, on):
    called = {}
    monkeypatch.setattr(R, "stage_run", lambda *a, **k: called.setdefault("run", k))
    monkeypatch.setattr(R, "stage_verdict", lambda *a, **k: None)
    monkeypatch.setattr(sys, "argv", ["x6_routes.py", "run", "--name", "x", "--sealed", *flags])
    R.main()
    assert called["run"]["atom_slices"] is on


def test_routes_atom_slices_needs_k_25_and_100(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    with pytest.raises(AssertionError, match="--jpp-ks 25 100"):
        R.stage_run("x47_test", False, conds=("C2",), jpp_ks=(25, 50), atom_slices=True)
    assert not any(tmp_path.iterdir())  # refused before writing anything


def test_x0_atom_slices_flag_and_its_assert(monkeypatch, tmp_path):
    called = {}
    monkeypatch.setattr(X, "stage_run", lambda *a: called.setdefault("slices", X.SLICES))
    monkeypatch.setattr(X, "SLICES", X.SLICES)
    for g in (
        "CURVE_DICTS",
        "K_CURVE",
        "READ",
        "DESCRIPTIVE",
        "ALT",
        "CURVE_ALL",
        "DICTS",
        "READOUT",
        "NONNEG",
        "N_ITEMS",
    ):
        monkeypatch.setattr(X, g, getattr(X, g))
    monkeypatch.setattr(sys, "argv", ["x0_necessity.py", "run", "--name", "x", "--sealed", "--dicts", "jpp",
                                      "--curve-dicts", "jpp", "--curve-k", "100", "--atom-slices"])  # fmt: skip
    X.main()
    assert called["slices"] is True
    monkeypatch.undo()
    monkeypatch.setattr(X, "RESULTS", tmp_path)
    monkeypatch.setattr(X, "SLICES", True)
    monkeypatch.setattr(X, "K_CURVE", (50,))
    with pytest.raises(AssertionError, match="atom-slices"):
        X.stage_run("x47_test", "", "s", (32,), 32, ["chat"])
    assert not any(tmp_path.iterdir())


# ---- sealed ------------------------------------------------------------------------------------------------------


BLOCKS = ("**Q47.1** (47.1) Where ...\n- (a) ...\n\nAnswer per model: 27B; 9B; Muse.\n\nDan:{}\n\n"
          "**Q47.2** (47.2) ...\n\nDan: ordinal · 60%\n\n**Q47.10** x\n\nDan: y\n")  # fmt: skip


def test_answer_in_reads_only_its_own_block():
    assert A.answer_in(BLOCKS.format(""), "Q47.1") == ""
    assert A.answer_in(BLOCKS.format(" 27B (a) 60%; 9B (c) 70%; Muse (c) 60%"), "Q47.1").startswith("27B (a)")
    assert A.answer_in(BLOCKS.format(""), "Q47.2") == "ordinal · 60%"
    assert A.answer_in(BLOCKS.format(""), "Q47.10") == "y" and A.answer_in("no such", "Q47.1") == ""
    assert A.answer_in("See **Q47.1** above.\n\nDan: z\n", "Q47.1") == ""  # a mention is not its block


def test_require_answer_reads_the_committed_file(monkeypatch):
    seen = {}

    def fake_run(cmd, **k):
        seen["cmd"] = cmd
        return SimpleNamespace(stdout=BLOCKS.format(""))

    monkeypatch.setattr(A.subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="sealed"):
        A.require_answer("Q47.1")
    assert seen["cmd"] == ["git", "show", f"HEAD:{A.PREDICTIONS}"]
    monkeypatch.setattr(A.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=BLOCKS.format(" (c) 70%")))
    assert A.require_answer("Q47.1") == "(c) 70%"


def test_the_routes_and_x0_stages_refuse_a_sealed_47_run(tmp_path, monkeypatch):
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "")
    monkeypatch.setattr(R, "RESULTS", tmp_path / "x6_routes")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0_necessity")
    for d in (tmp_path / "x6_routes" / "r", tmp_path / "x0_necessity" / "m"):
        d.mkdir(parents=True)
        (d / "manifest.json").write_text(json.dumps({"x47_1": {"test": "47.1"}}))
    for call in (lambda: R.stage_verdict("r"), lambda: R.stage_examples("r", decode=str), lambda: X.write_verdict("m")):
        with pytest.raises(SystemExit, match="sealed"):
            call()
    assert sorted(p.name for p in (tmp_path / "x6_routes" / "r").iterdir()) == ["manifest.json"]


# ---- the rule on planted rows ------------------------------------------------------------------------------------

N = 100


def _routes_rows(fall: float = 0.0, n: int = N, base_id: int = 60, fall_atoms: float = 0.0) -> list[dict]:
    """C2 rows: identity in the first id[arm] scenes, position in the next 20, original after. Without 26-100 identity
    answers fall by `fall` more than without its random part; the random atoms at its share cut `fall_atoms`."""
    ident = {a: base_id for a in A.ROUTE_ARMS} | {"no_jpp26_100": base_id - round(n * fall),
                                                  "no_ratoms75": base_id - round(n * fall_atoms)}  # fmt: skip
    rows = []
    for i in range(n):
        for a in A.ROUTE_ARMS:
            route = "identity" if i < ident[a] else "position" if i < ident[a] + 20 else "original"
            base = {"scene": f"C2-{i:04d}", "condition": "C2", "entity": f"e{i % 25}", "arm": a, "top": 7}
            rows += [{**base, "reader": LK, "route": route, "switched": int(route == "identity")},
                     {**base, "reader": RC, "route": None, "switched": 1}]  # fmt: skip
    return rows


def _main_rows(lost: dict[str, dict[str, int]], n: int = N, layer: int = 32, whole: int = N) -> list[dict]:
    """X0 rows at L: the first `whole` scenes switch with the whole change and without every random part; without
    part p the reader's first lost[reader][p] scenes stop switching."""
    rows = []
    for i in range(n):
        base = {"scene": f"P2-{i:04d}", "entity": f"e{i % 25}", "rendering": "chat", "layer": layer, "top": 7}
        for w in (LK, RC):
            sw = int(i < whole)
            rows.append({**base, "reader": w, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": sw})
            for label, _, (d, k, omp) in A.PARTS:
                gone = lost.get(w, {}).get(label, 0)
                rows.append({**base, "reader": w, "dict": d, "k": k, "omp": omp, "arm": "no_part",
                             "switched": int(sw and i >= gone)})  # fmt: skip
                rows.append({**base, "reader": w, "dict": d, "k": k, "omp": omp, "arm": "no_rand", "switched": sw})
    return rows


def _label(fall: float, recall_lost: int, n_boot: int = 300, **kw) -> dict:
    routes = A.routes_numbers(_routes_rows(fall), n_boot)
    main = A.main_numbers(_main_rows({RC: {"26-100": recall_lost}}, **kw), 32, n_boot)
    return A.model_label(routes, main)


def test_routes_numbers_read_planted_falls():
    r = A.routes_numbers(_routes_rows(0.35, fall_atoms=0.05), 300)
    assert r is not None and r["n"] == N and r["entities"] == 25
    f = r["falls"]["26-100"]["identity"]
    assert f[0] == pytest.approx(0.35) and f[1] <= 0.35 <= f[2]
    assert r["falls"]["1-25"]["identity"][0] == pytest.approx(0.0)
    assert r["falls"]["26-100"]["position"][0] == pytest.approx(0.0)  # the lost identity answers go to original
    assert r["vs_random_atoms"]["identity"][0] == pytest.approx(0.30)
    assert r["shares"]["no_jpp26_100"]["identity"][0] == pytest.approx(0.25)
    assert r["shares"]["whole"]["recall"][0] == pytest.approx(1.0)
    assert A.routes_numbers([r_ for r_ in _routes_rows() if r_["arm"] != "whole"]) is None


def test_main_numbers_read_planted_extra_loss():
    m = A.main_numbers(_main_rows({RC: {"26-100": 15, "random atoms, same share": 5}, LK: {"1-100": 60}}), 32, 300)
    assert m is not None
    assert m["readers"][RC]["26-100"]["excess"][0] == pytest.approx(0.15)
    assert m["readers"][LK]["1-100"]["excess"][0] == pytest.approx(0.60)
    assert m["readers"][LK]["26-100"]["excess"][0] == pytest.approx(0.0)
    assert m["vs_random_atoms"][RC][0] == pytest.approx(0.10)
    assert A.main_numbers(_main_rows({}), 12) is None  # no rows at that layer


@pytest.mark.parametrize(
    ("fall", "recall_lost", "label"),
    [
        (0.30, 10, A.LABELS["a"]),  # both bars exactly met
        (0.45, 0, A.LABELS["a"]),
        (0.30, 11, "none of (a)-(c)"),  # the recall loses a little more than 0.10, less than 0.20
        (0.29, 0, "none of (a)-(c)"),  # identity falls less than 0.30
        (0.20, 20, A.LABELS["b"]),  # continuum at both bars
        (0.50, 40, A.LABELS["b"]),
        (0.19, 40, "none of (a)-(c)"),
        (0.09, 40, A.LABELS["c"]),  # outside the lens, whatever the recall does
        (0.10, 0, "none of (a)-(c)"),  # a fall of exactly 0.10 is not "< 0.10"
        (-0.05, 0, A.LABELS["c"]),
    ],
)
def test_model_label_at_the_bars(fall, recall_lost, label):
    assert _label(fall, recall_lost)["label"] == label


def test_a_needs_the_ci_to_exclude_zero():
    # 10 bridge items; e0 holds 40 of the 100 scenes and all of the fall: the point is 0.40, but about a third of the
    # cluster resamples miss e0 (0.9^10), so the paired interval's lower bound is 0
    rows = []
    for i in range(N):
        e = "e0" if i < 40 else f"e{1 + i % 9}"
        for a in A.ROUTE_ARMS:
            route = "original" if a == "no_jpp26_100" and e == "e0" else "identity"
            base = {"scene": f"C2-{i:04d}", "condition": "C2", "entity": e, "arm": a}
            rows += [{**base, "reader": LK, "route": route, "switched": 0},
                     {**base, "reader": RC, "route": None, "switched": 1}]  # fmt: skip
    routes = A.routes_numbers(rows, 1000)
    assert routes is not None
    fall = routes["falls"]["26-100"]["identity"]
    lab = A.model_label(routes, A.main_numbers(_main_rows({}), 32, 300))
    assert fall[0] == pytest.approx(0.40) and fall[1] == pytest.approx(0.0)
    assert lab["label"] == "none of (a)-(c)" and not lab["clauses"]["a"] and not lab["clauses"]["b"]


def test_without_a_valid_main_test_only_c_is_read():
    routes_c = A.routes_numbers(_routes_rows(0.0), 300)
    routes_a = A.routes_numbers(_routes_rows(0.4), 300)
    invalid = A.main_numbers(_main_rows({}, whole=20), 32, 300)  # 20 of 100 switch: X0's cell is invalid
    assert A.model_label(routes_c, invalid)["label"] == A.LABELS["c"]
    assert A.model_label(routes_a, invalid)["label"] == "can't tell"
    assert A.model_label(routes_a, None)["label"] == "can't tell"
    assert A.model_label(None, invalid)["label"] == "not tested"


def test_batch_rule_counts_a_on_two_models():
    def m(label, status="tested"):
        return {"target": label + status, "label": label, "status": status}

    a, c = A.LABELS["a"], A.LABELS["c"]
    assert A.batch_rule([m(a), m(a), m(c)])["a_holds"] == "holds"
    assert A.batch_rule([m(a), m(c), m(c)])["a_holds"] == "does not hold"
    assert A.batch_rule([m(a), m("pending", "pending"), m(c)])["a_holds"] == "pending"
    assert A.batch_rule([m(c), m("pending", "pending"), m("not tested", "not tested")])["a_holds"] == "does not hold"


def test_share_summary_reads_the_check_and_the_geometry():
    recs = [{"share_1_25": 0.12, "share_26_100": 0.15, "share_1_100": 0.27, "share_ratoms75own": 0.03,
             "ratoms75_alpha": 2.2, "cos2_U_jpp25": 0.01, "cos2_U_jpp100": 0.03, "cos2_U_jpp26_100": 0.02,
             "cos2_U_ratoms75": 0.01},
            {"share_1_25": 0.20, "share_26_100": 0.10, "share_1_100": 0.30, "share_ratoms75own": 0.02,
             "ratoms75_alpha": None, "cos2_U_jpp25": 0.03, "cos2_U_jpp100": 0.05, "cos2_U_jpp26_100": 0.02,
             "cos2_U_ratoms75": None}]  # fmt: skip
    s = A.share_summary(recs)
    assert s["n"] == 2 and s["median_share_26_100"] == pytest.approx(0.125)
    assert s["items_26_100_above_1_25"] == 1 and s["items_per_atom_order_holds"] == 2 and s["alpha_above_1"] == 1
    assert s["median_ratoms75_alpha"] == pytest.approx(2.2) and s["mean_cos2_U_ratoms75"] == pytest.approx(0.01)


# ---- the verdict on planted runs ---------------------------------------------------------------------------------


def _write(path, manifest, **files):
    path.mkdir(parents=True)
    (path / "manifest.json").write_text(json.dumps(manifest))
    for fname, data in files.items():
        if isinstance(data, dict):
            (path / fname).write_text(json.dumps(data))
        else:
            (path / fname).write_text("".join(json.dumps(r) + "\n" for r in data))


def _case(scene: str, pos: int = 3, cond: bool = True) -> dict:
    rd = {"question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
          "ids": {"org": [1, 2, 3, 4, 5, 6], "alt": [1, 2, 3, 9, 5, 6]}}  # fmt: skip
    c = {
        "scene": scene,
        "bridge": "frog",
        "cf_bridge": "bee",
        "pos": pos,
        "readers": {LK: rd, RC: {**rd, "answer": "4"}},
    }
    return {**c, "condition": "C2", "expect": {"identity": 3}} if cond else {**c, "rendering": "chat"}


def _planted(tmp_path, monkeypatch, falls: dict[str, float], skip: tuple[str, ...] = ()):
    monkeypatch.setattr(A.pins, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(A, "RESULTS", tmp_path / "x47_atoms")
    layers = {"qwen3.6-27b": 32, "qwen3.5-9b": 12, "muse-glimmer-30b": 26}
    for t in A.MODELS:
        if t in skip:
            continue
        rows = _routes_rows(falls[t])
        norms = [{"scene": f"C2-{i:04d}", "condition": "C2", "share_1_25": 0.12, "share_26_100": 0.15,
                  "share_1_100": 0.27, "share_ratoms75own": 0.03, "ratoms75_alpha": 2.2, "cos2_U_jpp25": 0.01,
                  "cos2_U_jpp100": 0.03, "cos2_U_jpp26_100": 0.02, "cos2_U_ratoms75": 0.01} for i in range(N)]  # fmt: skip
        _write(tmp_path / "x6_routes" / A.ROUTES_RUNS[t], {"model": {"target": t}, "layer": layers[t], "x47_1": {"test": "47.1"}},
               **{"outcomes.jsonl": rows, "norms.jsonl": norms, "cases.jsonl": [_case(f"C2-{i:04d}") for i in range(N)],
                  "gate.json": {"gate": {"C2": {"pass": True}}}})  # fmt: skip
        main = [{**r, "layer": layers[t]} for r in _main_rows({RC: {"26-100": 5}})]
        _write(tmp_path / "x0_necessity" / A.MAIN_RUNS[t], {"model": {"target": t}, "predicted": layers[t], "x47_1": {"test": "47.1"}},
               **{"outcomes.jsonl": main, "atoms.jsonl": [{"scene": f"P2-{i:04d}", **norms[i]} for i in range(N)],
                  "cases.jsonl": [_case(f"P2-{i:04d}", cond=False) for i in range(N)],
                  "examples.jsonl": [{"scene": "P2-0000", "reader": LK, "arm": "-/0/-/whole", "greedy": " 3"}],
                  "gate.json": {"gate": {"chat": {"pass": True}}}})  # fmt: skip


def test_verdict_is_sealed_until_dans_answer(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, dict.fromkeys(A.MODELS, 0.4))
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "")
    with pytest.raises(SystemExit, match="sealed"):
        A.stage_verdict(100, decode_for=lambda t: str)
    assert not (tmp_path / "x47_atoms").exists()


def test_verdict_on_planted_runs(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, {"qwen3.6-27b": 0.4, "qwen3.5-9b": 0.0, "muse-glimmer-30b": 0.35})
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "27B (a) 60%")

    def decode_for(target):
        return lambda ids: "".join(f"<{int(t)}>" for t in ids)

    out = A.stage_verdict(200, decode_for=decode_for)
    blob = json.loads((out / "x47_1.json").read_text())
    assert blob["dan"] == "27B (a) 60%" and blob["batch"]["a_holds"] == "holds" and blob["batch"]["models_a"] == 2
    labels = {m["target"]: m["label"] for m in blob["models"]}
    assert labels == {"qwen3.6-27b": A.LABELS["a"], "qwen3.5-9b": A.LABELS["c"], "muse-glimmer-30b": A.LABELS["a"]}
    md = (out / "x47_1.md").read_text()
    assert "**(a) for the batch: holds**" in md and "26-100 vs random atoms" in md
    assert len((out / "x47_1_items.csv").read_text().splitlines()) == 1 + 3 * 2 * N
    ex = (out / "examples.md").read_text()
    assert ex.count("#### ") == 3 * 2 * X.K_EXAMPLES  # 10 items per run, two runs per model
    assert "<1><2><3>⟦<4>⟧<5><6>" in ex  # the patch position marked
    assert "| no_jpp26_100 | '<7>' | identity |" in ex  # routes: every arm's answer and route
    assert "| no_part jpp26_100/75/slice | '<7>' |" in ex and "| no_rand ratoms75own/75/own | '<7>' |" in ex  # main


def test_verdict_with_a_missing_model_is_pending(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, {"qwen3.6-27b": 0.4, "qwen3.5-9b": 0.4}, skip=("muse-glimmer-30b",))
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "x")
    blob = json.loads((A.stage_verdict(100, decode_for=lambda t: str) / "x47_1.json").read_text())
    assert blob["batch"]["a_holds"] == "holds"
    assert [m["status"] for m in blob["models"]] == ["tested", "tested", "pending"]


def test_model_result_refuses_runs_of_another_kind(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, dict.fromkeys(A.MODELS, 0.0))
    with pytest.raises(AssertionError, match=r"not qwen3\.5-9b's"):
        A.model_result("qwen3.5-9b", A.ROUTES_RUNS["qwen3.6-27b"], A.MAIN_RUNS["qwen3.5-9b"], 100)


def test_main_passes_re_queued_run_names(monkeypatch):
    seen = {}
    monkeypatch.setattr(A, "stage_verdict", lambda n_boot, **k: seen.update(k))
    monkeypatch.setattr(sys, "argv", ["x47_atoms.py", "verdict", "--routes-runs", "a", "qwen35_9b_r2", "c"])
    A.main()
    assert seen["routes_runs"] == {"qwen3.6-27b": "a", "qwen3.5-9b": "qwen35_9b_r2", "muse-glimmer-30b": "c"}
    assert seen["main_runs"] is None


def test_verdict_takes_re_queued_run_names(tmp_path, monkeypatch):
    _planted(tmp_path, monkeypatch, {"qwen3.6-27b": 0.4, "qwen3.5-9b": 0.4, "muse-glimmer-30b": 0.0})
    (tmp_path / "x6_routes" / A.ROUTES_RUNS["qwen3.5-9b"]).rename(tmp_path / "x6_routes" / "r2")
    monkeypatch.setattr(A, "dan_answer", lambda q=A.QUESTION: "x")
    out = A.stage_verdict(100, decode_for=lambda t: str, routes_runs={"qwen3.5-9b": "r2"})
    blob = json.loads((out / "x47_1.json").read_text())
    assert blob["models"][1]["runs"] == ["r2", A.MAIN_RUNS["qwen3.5-9b"]] and blob["batch"]["a_holds"] == "holds"
