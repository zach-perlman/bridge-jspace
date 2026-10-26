"""Batch 45k on x6_routes (--jpp-ks / --jpp-other) and its main-test control (x0_parts --other-k): the geometry on
synthetic tensors, jpp_other's partners, the rule on planted rows (all four outcomes, the 9B clause, Dan's ~22:05
precondition and precedence) and the arm list with the flags off. Nothing here needs a GPU."""

import json
import sys
from typing import Any

import pytest
import torch

from scripts import x0_necessity as X
from scripts import x0_parts as XP
from scripts import x6_routes as R

LK, RC = "PP", "PM"
N = 100


def _unit(d: int, *idx: int) -> torch.Tensor:
    v = torch.zeros(d)
    v[list(idx)] = 1.0
    return v


def _rand_dic(seed: int = 0, atoms: int = 400, d: int = 128) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    dic = torch.randn(atoms, d, generator=g)
    return dic / dic.norm(dim=1, keepdim=True)


def _cases(n_per: int = 4, conds=("C0", "C2")) -> list[dict]:
    """Routes-like cases: scene i of every condition has the bridge pair (a_i, b_i), as the generator makes them."""
    return [{"scene": f"{c}-{i:04d}", "condition": c, "bridge": f"a{i}", "cf_bridge": f"b{i}"}
            for c in conds for i in range(n_per)]  # fmt: skip


# ---- the geometry ----------------------------------------------------------------------------------------------------


def test_mean_cos2_is_one_inside_the_span_and_zero_orthogonal():
    d = 10
    cols = torch.stack([_unit(d, 0), _unit(d, 1), _unit(d, 2)], 1)
    assert R.mean_cos2(cols, torch.stack([_unit(d, 0), _unit(d, 1)], 1)) == pytest.approx(1.0)
    assert R.mean_cos2(cols, torch.stack([_unit(d, 5), _unit(d, 6)], 1)) == pytest.approx(0.0)
    assert R.mean_cos2(cols, torch.stack([_unit(d, 0), _unit(d, 5)], 1)) == pytest.approx(0.5)  # ||P U||_F^2 / rank U
    skew = torch.stack([_unit(d, 0) + _unit(d, 1), _unit(d, 1)], 1)  # not orthonormal, same span as e0, e1: still 1
    assert R.mean_cos2(cols, skew) == pytest.approx(1.0)
    assert R.mean_cos2(cols, 3 * (_unit(d, 0) + _unit(d, 5))) == pytest.approx(0.5)  # ||P u||^2 / ||u||^2
    assert R.mean_cos2(cols, torch.zeros(d)) is None


def test_jpp_geometry_on_coordinate_atoms():
    d = 12
    jdic = torch.eye(d)
    x = torch.tensor([[8.0, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0], [0.0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5]])
    atoms = XP.omp_atoms(jdic, x, 4)
    assert atoms[0].tolist() == [0, 1, 2, 3] and atoms[1].tolist() == [11, 10, 9, 8]
    alf = torch.stack([_unit(d, 2), _unit(d, 9)], 1)
    u = [_unit(d, 0) + _unit(d, 3), None]  # row 1: an entity without a class mean
    fits = {k: X.fit(jdic, x, k, "signed") for k in (2, 4)}
    g = R.jpp_geometry(jdic, atoms, (2, 4), alf, u, fits)
    assert g[0]["cos2_U_jpp2"] == pytest.approx(0.0) and g[0]["cos2_U_jpp4"] == pytest.approx(0.5)
    assert g[1]["cos2_U_jpp2"] == pytest.approx(0.0) and g[1]["cos2_U_jpp4"] == pytest.approx(0.5)
    assert g[0]["cos2_id_jpp2"] == pytest.approx(0.5) and g[0]["cos2_id_jpp4"] == pytest.approx(1.0)
    assert g[1]["cos2_id_jpp2"] is None and g[1]["cos2_id_jpp4"] is None
    with pytest.raises(AssertionError, match="not in its atoms' span"):  # a part that is not the k atoms' fit
        R.jpp_geometry(jdic, atoms, (2,), alf, u, {2: x})


def test_omp_atoms_prefix_is_the_fit_at_each_k():
    """The geometry reads the first k of the k = 100 picks; signed OMP is greedy, so they span X.fit's part at k."""
    jdic = _rand_dic()
    x = torch.randn(5, jdic.shape[1], generator=torch.Generator().manual_seed(1))
    atoms = XP.omp_atoms(jdic, x, 100)
    assert torch.equal(atoms[:, :25], XP.omp_atoms(jdic, x, 25))
    fits = {k: X.fit(jdic, x, k, "signed") for k in (25, 50, 100)}
    alf, _ = torch.linalg.qr(torch.randn(jdic.shape[1], 3, generator=torch.Generator().manual_seed(2)))
    g = R.jpp_geometry(jdic, atoms, (25, 50, 100), alf, [None] * 5, fits)  # passes the span check
    assert all(r["cos2_U_jpp25"] <= r["cos2_U_jpp50"] + 1e-9 <= r["cos2_U_jpp100"] + 2e-9 for r in g)  # nested spans


# ---- jpp_other -------------------------------------------------------------------------------------------------------


def test_partners_within_the_condition_share_no_bridge():
    cases = _cases(5)
    pj = XP.partners(cases, group="condition")
    for i, j in enumerate(pj):
        assert j != i and cases[j]["condition"] == cases[i]["condition"]
        assert not ({cases[j]["bridge"], cases[j]["cf_bridge"]} & {cases[i]["bridge"], cases[i]["cf_bridge"]})


def test_partners_without_a_group_are_unchanged():
    """x0_parts' existing runs: the partner rule without a group is the one they used."""
    import random

    cases = _cases(5)
    order = list(range(len(cases)))
    random.Random(XP.OTHER_SEED).shuffle(order)
    old = [next(j for j in order if j != i and not ({cases[j]["bridge"], cases[j]["cf_bridge"]} &
                                                    {c["bridge"], c["cf_bridge"]})) for i, c in enumerate(cases)]  # fmt: skip
    assert XP.partners(cases) == old


def test_jpp_other_at_100_uses_another_scenes_atoms():
    jdic = _rand_dic(3)
    cases = _cases(3)
    x = torch.randn(len(cases), jdic.shape[1], generator=torch.Generator().manual_seed(4))
    atoms = XP.omp_atoms(jdic, x, 100)
    part, pj = XP.other_part(jdic, x, cases, 100, atoms, group="condition")
    for i, j in enumerate(pj):
        assert j != i and cases[j]["condition"] == cases[i]["condition"]
        q, _ = torch.linalg.qr(jdic[atoms[j]].T.double())
        want = q @ (q.T @ x[i].double())  # least squares on the partner's 100 atoms = the projection on their span
        assert torch.allclose(part[i].double(), want, atol=1e-3)
        q_own, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        assert not torch.allclose(part[i].double(), q_own @ (q_own.T @ x[i].double()), atol=1e-2)  # not its own
    again, _ = XP.other_part(jdic, x, cases, 100, None, group="condition")  # atoms computed inside: the same part
    assert torch.allclose(again, part, atol=1e-4)
    default, _ = XP.other_part(jdic, x, cases)  # x0_parts' default stays K = 25 atoms
    q, _ = torch.linalg.qr(jdic[atoms[XP.partners(cases)[0], :25]].T.double())
    assert torch.allclose(default[0].double(), q @ (q.T @ x[0].double()), atol=1e-3)


def test_jppk_parts_and_their_arms():
    jdic = _rand_dic(5)
    cases = _cases(3)
    d = jdic.shape[1]
    x = torch.randn(len(cases), d, generator=torch.Generator().manual_seed(6))
    alf, _ = torch.linalg.qr(torch.randn(d, 3, generator=torch.Generator().manual_seed(7)))
    means = {e: torch.randn(d, generator=torch.Generator().manual_seed(10 + i))
             for i, e in enumerate(["a0", "b0", "a1", "b1", "a2"])}  # b2 has no class mean  # fmt: skip
    jpp = X.fit(jdic, x, X.K_MAIN, "signed")
    parts, recs = R.jppk_parts(jdic, x, cases, (25, 50, 100), True, jpp, alf, means)
    assert set(parts) == {"jpp50", "jpp100", "jppother100"}
    assert torch.allclose(parts["jpp100"], X.fit(jdic, x, 100, "signed"))
    for c, r in zip(cases, recs, strict=True):
        assert r["jpp_other_partner"] != c["scene"] and r["jpp_other_partner"][:2] == c["condition"]
        assert {f"cos2_{w}_jpp{k}" for w in ("U", "id") for k in (25, 50, 100)} <= set(r)
        assert (r["cos2_id_jpp100"] is None) == (c["bridge"] == "a2")  # its pair has no mean for b2: kept, None
    u = means["b0"] - means["a0"]
    q, _ = torch.linalg.qr(jdic[XP.omp_atoms(jdic, x, 100)[0]].T.double())
    assert recs[0]["cos2_id_jpp100"] == pytest.approx(float((q.T @ u.double()).norm() ** 2 / u.norm() ** 2), abs=1e-5)
    basis, _ = torch.linalg.qr(torch.randn(d, d, generator=torch.Generator().manual_seed(8)))
    arms, sh = R.removal_arms(x, parts, basis)
    names = R.jppk_arm_names((25, 50, 100), True)
    assert set(arms) == {a for k, pair in names.items() if k != "jpp25" for a in pair}
    assert set(arms) <= set(R.ARMS) and torch.allclose(arms["no_jpp100"], x - parts["jpp100"])
    share = parts["jppother100"].norm(dim=1) ** 2 / x.norm(dim=1) ** 2
    assert torch.allclose(sh["jppother100"], share)


# ---- the flags off ---------------------------------------------------------------------------------------------------

OLD_ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand", "no_both", "no_both_rand", "no_alf_jrand",
            "keep_alf", "keep_alf_rand", "keep_jpp", "keep_jpp_rand", "no_id", "no_id_rand", "no_idout", "no_idout_rand",
            "no_alfidout", "no_alfidout_rand", "no_jppalfidout", "no_jppalfidout_rand", "keep_id", "keep_id_rand",
            "no_idsub", "no_wrong", "no_wrong_rand", "no_pca", "no_pca_rand", "no_jppalfwrong", "no_jppalfwrong_rand",
            "no_jppalfpca", "no_jppalfpca_rand")  # fmt: skip


def test_flags_off_add_no_arm():
    assert R.ARMS[: len(OLD_ARMS)] == OLD_ARMS  # the verdict tables of earlier runs keep their order
    assert R.jppk_arm_names((), False) == {}
    jdic = _rand_dic(9, atoms=60, d=40)
    x = torch.randn(4, 40, generator=torch.Generator().manual_seed(9))
    parts, recs = R.jppk_parts(jdic, x, _cases(2), (), False, None, None, {})
    assert parts == {} and recs == [{}] * 4
    assert R.removal_arms(x, parts, torch.eye(40)) == ({}, {})
    assert {a for pair in R.jppk_arm_names(R.JPP_KS, True).values() for a in pair} == set(R.JPPK_ARMS) - {"whole"}
    assert R.jppk_arm_names((25,), False) == {"jpp25": ("no_jpp", "no_jpp_rand")}  # k = 25 is the existing arm


@pytest.mark.parametrize(
    ("flags", "ks", "other"), [([], (), False), (["--jpp-ks", "25", "50", "100", "--jpp-other"], (25, 50, 100), True)]
)
def test_main_passes_the_45k_flags(monkeypatch, flags, ks, other):
    called = {}
    monkeypatch.setattr(R, "stage_run", lambda *a, **k: called.setdefault("run", k))
    monkeypatch.setattr(R, "stage_verdict", lambda *a, **k: None)
    monkeypatch.setattr(sys, "argv", ["x6_routes.py", "run", "--name", "x", *flags])
    R.main()
    assert called["run"]["jpp_ks"] == ks and called["run"]["jpp_other"] is other


def test_x0_parts_takes_the_main_run_and_keeps_single_runs(tmp_path, monkeypatch):
    """x0_parts run --single <main run>: a run with no "alt" (written before 24 Oct) is the cf; a single-change run
    stays single. Stopped at the model load (no GPU)."""
    import bridge_jspace.model as BM

    class Loaded(Exception):
        pass

    def stop():
        raise Loaded

    monkeypatch.setattr(XP, "RESULTS", tmp_path / "x0_parts")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0_necessity")
    monkeypatch.setattr(X, "ALT", X.ALT)
    monkeypatch.setattr(BM, "load_model", stop)
    for run, alt in (("main", None), ("single", "single")):
        src = tmp_path / "x0_necessity" / run
        src.mkdir(parents=True)
        (src / "manifest.json").write_text(json.dumps({"set": "s", "predicted": 32, "code": {}, **({"alt": alt} if alt
                                                                                                  else {})}))  # fmt: skip
        (src / "outcomes.jsonl").write_text(json.dumps({"scene": "P2-0000", "rendering": "chat"}) + "\n")
        with pytest.raises(Loaded):
            XP.stage_run(f"x0_test_{run}", run, used=("jpp_other", "jpp"), other_k=100)
        assert (alt or "cf") == X.ALT
    with pytest.raises(AssertionError, match="run jpp_other"):
        XP.stage_run("x0_test_bad", "main", used=("jpp",), other_k=100)


# ---- the rule on planted rows ----------------------------------------------------------------------------------------


def _run(d_id=0.0, d_pos=0.0, ex100=0.6, ex_other=0.0, cos2=0.3, n=N):
    """Lookup rows (and recall rows) of one 45k run with planted effects. C2: identity in the first id[arm] scenes,
    position in the next pos[arm], original after; from k = 25 to 100 the identity answers fall by d_id and the
    position answers by d_pos more than with the random part (whose shares stay put). C0: every scene switches with
    the whole change and without the random parts; without J++ at 25 / 50 / 100 and jpp_other 12 / 30 / 100 ex100 /
    100 ex_other scenes stop switching. Norms: the k = 100 span's cos^2 with U = cos2 on every item."""
    ident = {a: 50 for a in R.JPPK_ARMS} | {"no_jpp100": 50 - round(100 * d_id)}
    pos = {a: 30 for a in R.JPPK_ARMS} | {"no_jpp100": 30 - round(100 * d_pos)}
    lost = {"no_jpp": 12, "no_jpp50": 30, "no_jpp100": round(100 * ex100), "no_jppother100": round(100 * ex_other)}
    rows, norms = [], []
    for i in range(n):
        e = f"e{i % 20}"
        for a in R.JPPK_ARMS:
            route = "identity" if i < ident[a] else "position" if i < ident[a] + pos[a] else "original"
            for cond, rt, sw in (("C2", route, 0), ("C0", "other", int(i >= lost.get(a, 0)))):
                base = {"scene": f"{cond}-{i:04d}", "condition": cond, "entity": e, "arm": a}
                rows += [{**base, "reader": LK, "route": rt, "switched": sw},
                         {**base, "reader": RC, "route": None, "switched": 1}]  # fmt: skip
        for cond in ("C0", "C2"):
            norms.append({"scene": f"{cond}-{i:04d}", "condition": cond, "norm": 1.0, "share_jpp": 0.1,
                          "share_jpp50": 0.2, "share_jpp100": 0.3, "share_jppother100": 0.25,
                          **{f"cos2_U_jpp{k}": cos2 * k / 100 for k in (25, 50, 100)},
                          **{f"cos2_id_jpp{k}": None if i % 10 == 0 else 0.4 for k in (25, 50, 100)}})  # fmt: skip
    return rows, norms


def _rule(n_boot=200, **kw):
    return R.jppk_rule(*_run(**kw), R.JPP_KS, n_boot)


def test_jppk_rule_reads_d_geometry_and_c0_losses():
    r = _rule(d_id=0.3, d_pos=-0.05, ex100=0.6, ex_other=0.45, cos2=0.3)
    assert r["d"]["identity"][0] == pytest.approx(0.3) and r["d"]["position"][0] == pytest.approx(-0.05)
    assert r["d"]["identity"][1] <= 0.3 <= r["d"]["identity"][2]
    assert r["shares"]["C2"]["arms"]["no_jpp100"]["identity"][0] == pytest.approx(0.2)
    assert r["shares"]["C2"]["n"] == N and r["shares"]["C0"]["n"] == N
    loss = {p: c["excess"][0] for p, c in r["c0_loss"].items()}
    assert loss == pytest.approx({"jpp25": 0.12, "jpp50": 0.30, "jpp100": 0.60, "jpp_other100": 0.45})
    assert r["c0_loss"]["jpp100"]["median_share"] == pytest.approx(0.3)
    assert r["c0_loss"]["jpp_other100"]["median_share"] == pytest.approx(0.25)
    g = r["geometry"]["C2"]["jpp100"]
    assert g["U"]["mean"] == pytest.approx(0.3) and g["U"]["n"] == N
    assert g["id"]["n"] == 90 and g["id"]["of"] == N and g["id"]["median"] == pytest.approx(0.4)  # None left out
    assert r["cos2_U_jpp100_C2"] == pytest.approx(0.3)
    assert r["precondition"] == {"c0_extra_loss_jpp100": pytest.approx(0.6), "holds": True}
    assert r["routes_generic"]["holds"] and r["routes_generic"]["other_minus_bar"][0] == pytest.approx(0.05)
    assert r["clauses"] == {"identity_falls": True, "neither_falls": False, "pointer": False}


@pytest.mark.parametrize(
    ("kw", "clauses"),
    [
        ({"d_id": 0.2, "d_pos": 0.0}, (True, False, False)),  # exactly at the 0.2 bar counts
        ({"d_id": 0.3, "d_pos": 0.1}, (False, False, False)),  # position falls by 0.1: not "less than 0.1"
        ({"d_id": 0.05, "d_pos": 0.09}, (False, True, False)),  # the 9B's clause: neither falls by 0.1
        ({"d_id": 0.1, "d_pos": 0.0}, (False, False, False)),  # identity falls by exactly 0.1: the 9B's clause fails
        ({"d_pos": 0.25, "cos2": 0.6}, (False, False, True)),  # pointer
        ({"d_pos": 0.2, "cos2": 0.5}, (False, False, True)),  # both bars exactly met
        ({"d_pos": 0.25, "cos2": 0.4}, (False, False, False)),  # position falls, the span misses U
        ({"d_id": 0.3, "d_pos": -0.2}, (True, False, False)),  # position rises: "falls by less than 0.1"
    ],
)
def test_jppk_rule_clauses_at_the_bars(kw, clauses):
    c = _rule(**kw)["clauses"]
    assert (c["identity_falls"], c["neither_falls"], c["pointer"]) == clauses


def test_jppk_rule_without_the_45k_arms_is_not_tested():
    rows, norms = _run()
    rows = [r for r in rows if r["arm"] in ("whole", "no_jpp", "no_jpp_rand")]
    r = R.jppk_rule(rows, norms, (), 100)
    assert r["d"] == {} and not any(r["clauses"].values()) and not r["precondition"]["holds"]
    assert r["tested"] == {"d": False, "cos2": False, "precondition": False}


# ---- the labels and Q45.9 (Dan's ~22:05 overrides) -------------------------------------------------------------------

T27, T9, TM = R.TARGET_27B, R.TARGET_9B, "muse-glimmer-30b"
GEN_YES = R.generic_rule({"excess": [0.45, 0.3, 0.6], "n": 200}, {"excess": [0.6, 0.5, 0.7], "n": 200})
GEN_NO = R.generic_rule({"excess": [0.1, 0.0, 0.2], "n": 200}, {"excess": [0.6, 0.5, 0.7], "n": 200})


def _labels(f27: dict, f9: dict | None = None, generic=GEN_NO, muse: dict | None = None):
    flags = {"r27": _rule(**f27), **({"r9": _rule(**f9)} if f9 is not None else {}),
             **({"rm": _rule(**muse)} if muse is not None else {})}  # fmt: skip
    targets = {"r27": T27, "r9": T9, "rm": TM}
    return R.jppk_labels(flags, {k: targets[k] for k in flags}, generic)


def test_generic_rule_at_two_thirds():
    assert GEN_YES["holds"] and GEN_YES["tested"] and GEN_YES["bar"] == pytest.approx(0.4)
    assert R.generic_rule({"excess": [0.4, 0, 1], "n": 1}, {"excess": [0.6, 0, 1], "n": 1})["holds"]  # at the bar
    assert not GEN_NO["holds"]
    missing = R.generic_rule(None, {"excess": [0.6, 0, 1], "n": 1})
    assert not missing["holds"] and not missing["tested"]


def test_q45_9_identity_needs_the_9b_clause():
    res = _labels({"d_id": 0.3}, {"d_id": 0.05})
    assert res["q45_9"]["outcome"] == [R.Q45_9["identity"]] and res["labels"]["r27"] == [R.JPPK_LABELS["identity"]]
    assert res["labels"]["r9"] == ["can't tell"] and res["nine_b_neither_falls"]
    res = _labels({"d_id": 0.3}, {"d_id": 0.15})  # the 9B's identity answers fall too: not the 27B's own route
    assert res["q45_9"]["outcome"] == [R.Q45_9["none"]] and not res["nine_b_neither_falls"]
    res = _labels({"d_id": 0.3})  # no 9B run: the clause cannot hold
    assert res["q45_9"]["outcome"] == [R.Q45_9["none"]] and res["nine_b"] is None


def test_q45_9_pointer_generic_and_cant_tell():
    res = _labels({"d_pos": 0.25, "cos2": 0.6}, {}, muse={"d_pos": 0.3, "cos2": 0.7})
    assert res["q45_9"]["outcome"] == [R.Q45_9["pointer"]]
    assert res["labels"]["rm"] == [R.JPPK_LABELS["pointer"]]  # every model's own labels, reported beside
    res = _labels({}, {}, generic=GEN_YES)
    assert res["q45_9"]["outcome"] == [R.Q45_9["generic"]] and res["q45_9"]["generic_tested"]
    assert res["labels"]["r9"] == ["can't tell"]  # generic fitting is read on the 27B's main test only
    res = _labels({}, {})
    assert res["q45_9"]["outcome"] == [R.Q45_9["none"]] and res["labels"]["r27"] == ["can't tell"]
    assert not _labels({}, {}, generic=None)["q45_9"]["generic_tested"]


def test_q45_9_generic_takes_precedence():
    res = _labels({"d_pos": 0.25, "cos2": 0.6}, {}, generic=GEN_YES)  # pointer and generic both hold
    assert set(res["labels"]["r27"]) == {R.JPPK_LABELS["pointer"], R.JPPK_LABELS["generic"]}
    assert res["q45_9"]["outcome"] == [R.Q45_9["generic"]]
    res = _labels({"d_id": 0.3}, {"d_id": 0.0}, generic=GEN_YES)
    assert res["q45_9"]["outcome"] == [R.Q45_9["generic"]]


@pytest.mark.parametrize(("ex100", "met"), [(0.19, False), (0.2, True), (0.6, True)])
def test_q45_9_precondition_overrides_everything(ex100, met):
    res = _labels({"d_pos": 0.25, "cos2": 0.6, "ex100": ex100}, {}, generic=GEN_YES)
    assert res["q45_9"]["precondition"]["holds"] is met
    assert (res["q45_9"]["outcome"] == [R.Q45_9["precondition"]]) is not met
    if met:
        assert res["q45_9"]["outcome"] == [R.Q45_9["generic"]]


def test_q45_9_not_scored_without_a_tested_27b():
    res = _labels({"d_pos": 0.25, "cos2": 0.6}, {}, generic=GEN_YES)
    assert res["q45_9"]["run"] == "r27"
    flags = {"r27": {**_rule(d_pos=0.25, cos2=0.6), "c0_ok": False}}
    res = R.jppk_labels(flags, {"r27": T27}, GEN_YES)
    assert res["q45_9"]["outcome"] == ["not scored: the 27B's C0 check failed"] and res["labels"]["r27"] == [
        "can't tell"
    ]
    res = R.jppk_labels({"r9": _rule()}, {"r9": T9}, GEN_YES)
    assert res["q45_9"]["outcome"] == ["not scored: no 27B run"]
    with pytest.raises(AssertionError, match="one run per model"):
        R.jppk_labels({"a": _rule(), "b": _rule()}, {"a": T27, "b": T27})


# ---- the verdict, the main-test runs and the summary -----------------------------------------------------------------


def _write(path, manifest, **files):
    path.mkdir(parents=True)
    (path / "manifest.json").write_text(json.dumps(manifest))
    for fname, data in files.items():
        (path / fname).write_text("".join(json.dumps(r) + "\n" for r in data))


def _x0_rows(parts: dict[tuple[str, int, str], int], n=N, layer=32):
    """X0-style lookup and recall rows: every scene switches with the whole change and without the random part;
    without part p the first parts[p] scenes stop switching (lookup only)."""
    rows = []
    for i in range(n):
        base = {"scene": f"P2-{i:04d}", "entity": f"e{i % 20}", "rendering": "chat", "layer": layer}
        for w in (LK, RC):
            rows.append({**base, "reader": w, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
            for (d, k, omp), lost in parts.items():
                rows.append({**base, "reader": w, "dict": d, "k": k, "omp": omp, "arm": "no_part",
                             "switched": int(not (w == LK and i < lost))})  # fmt: skip
                rows.append({**base, "reader": w, "dict": d, "k": k, "omp": omp, "arm": "no_rand", "switched": 1})
    return rows


def _main_test_runs(tmp_path, other_lost: int):
    _write(tmp_path / "x0_parts" / "gen", {"model": {"target": T27}, "layer": 32, "parts": ["jpp_other", "jpp"],
                                           "other_k": 100, "single": "x0_necessity_27b_chat"},
           **{"outcomes.jsonl": _x0_rows({("jpp_other", 100, "other"): other_lost, ("jpp", 25, "signed"): 12})})  # fmt: skip
    _write(tmp_path / "x0_necessity" / "km", {"model": {"target": T27}, "predicted": 32},
           **{"outcomes.jsonl": _x0_rows({("jpp", 100, "signed"): 60, ("jpp", 25, "signed"): 12,
                                          ("we", 100, "signed"): 5})})  # fmt: skip


def test_main_test_generic_reads_the_two_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(R.pins, "RESULTS_DIR", tmp_path)
    _main_test_runs(tmp_path, other_lost=45)
    g = R.main_test_generic("x0_parts/gen", "x0_necessity/km", 200)
    assert g["jpp_other100"][0] == pytest.approx(0.45) and g["jpp100"][0] == pytest.approx(0.6)
    assert g["holds"] and g["tested"] and g["same_items"] and g["n"] == [N, N]
    assert R.main_test_cell(_x0_rows({}), ("jpp", 100, "signed"), 32, 100) is None


def test_verdict_and_summary_of_45k_runs(tmp_path, monkeypatch):
    n = iter(range(1000))
    monkeypatch.setattr(R.time, "strftime", lambda fmt, t=None: f"t{next(n):03d}")
    monkeypatch.setattr(R, "RESULTS", tmp_path / "x6_routes")
    monkeypatch.setattr(R.pins, "RESULTS_DIR", tmp_path)
    _main_test_runs(tmp_path, other_lost=45)
    m = {"layer": 32, "conditions": ["C0", "C2"], "x45k": {"ks": [25, 50, 100], "other": True}}
    runs: list[tuple[str, str, dict[str, Any]]] = [
        ("r27", T27, {"d_pos": 0.25, "cos2": 0.6}),
        ("r9", T9, {"ex100": 0.0}),
    ]
    for name, target, kw in runs:
        rows, norms = _run(**kw)
        _write(tmp_path / "x6_routes" / name, {**m, "model": {"target": target}},
               **{"outcomes.jsonl": rows, "norms.jsonl": norms})  # fmt: skip
        (tmp_path / "x6_routes" / name / "c0_check.json").write_text(json.dumps({"ok": True}))
    out = R.stage_verdict("r27", 100)
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["x45k"]["clauses"]["pointer"] and {r["arm"] for r in blob["rows"]} == set(R.JPPK_ARMS)
    assert "## 45k" in (out / "verdict.md").read_text()
    s = json.loads(
        (R.stage_jppk_summary(["r27", "r9"], "x0_parts/gen", "x0_necessity/km", 100) / "x45k.json").read_text()
    )
    assert s["q45_9"]["outcome"] == [R.Q45_9["generic"]] and s["q45_9"]["generic"]["holds"]
    s = json.loads((R.stage_jppk_summary(["r27", "r9"], n_boot=100) / "x45k.json").read_text())
    assert s["q45_9"]["outcome"] == [R.Q45_9["pointer"]] and not s["q45_9"]["generic_tested"]
    (tmp_path / "x6_routes" / "r27" / "c0_check.json").write_text(json.dumps({"ok": False}))
    s = json.loads((R.stage_jppk_summary(["r27", "r9"], n_boot=100) / "x45k.json").read_text())
    assert s["q45_9"]["outcome"] == ["not scored: the 27B's C0 check failed"]


def test_orthonormal_spans_the_columns_and_keeps_the_device():
    a = torch.tensor([[1.0, 1.0, 2.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])  # rank 2
    q = R.orthonormal(a)
    assert q.shape == (4, 2) and q.device == a.device and q.dtype == torch.float64
    assert torch.allclose(q.T @ q, torch.eye(2, dtype=torch.float64), atol=1e-10)
    assert torch.allclose(q @ (q.T @ a.double()), a.double(), atol=1e-10)  # spans every column
    assert R.orthonormal(torch.zeros(4, 2)).shape == (4, 0)
