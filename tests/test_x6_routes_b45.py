"""Batch 45 on x6_routes: 45a (--prepend), 45e (--identity-controls), 45i (--rendering nochat), --sealed and the
examples stage. The rules are read on planted synthetic rows; nothing here needs a GPU."""

import json
import random
import sys

import pytest
import torch

from scripts import x6_routes as R

LK, RC = "PP", "PM"
ORG = ("The locker of the duck is 4. The locker of the frog is 3. The locker of the goose is 2. "
       "Beth picked the frog. Ann picked the duck. Tom picked the goose.")  # fmt: skip


# ---- 45a: the prepended sentences -----------------------------------------------------------------------------------


def _base_case():
    return {
        "scene": "C2-0007",
        "condition": "C2",
        "context": ORG,
        "readers": {LK: {"question": R.LOOKUP_Q.format(p="Ann")}},
    }


def test_prepend_sentences_name_the_right_items():
    animals = ["cat", "cow", "duck", "frog", "goose", "owl"]
    people = ["Ann", "Beth", "JoAnn", "Max", "Tom"]
    fillers = ["A quiet day.", "Rain fell."]
    s = R.prepend_sentences(_base_case(), animals, people, fillers, random.Random(1))
    assert s["V0"] == ""
    new = s["V1"].split(" picked")[0]
    assert new == "Max"  # not in the scene; JoAnn ends with Ann ("Ann picked the duck." would be found inside it)
    assert s["V1"] == "Max picked the duck."  # the item whose locker is first in O
    assert s["V2"] in ("Max picked the frog.", "Max picked the goose.")  # another locker item
    assert s["V3"].removeprefix("Max picked the ").removesuffix(".") in ("cat", "cow", "owl")  # no locker in the scene
    assert s["V4"] in fillers
    assert s == R.prepend_sentences(_base_case(), animals, people, fillers, random.Random(1))  # seeded


def test_asked_of_reads_the_question():
    assert R.asked_of(_base_case()) == "Ann"


def test_prepend_cases_on_the_tokenizer():
    """With the target's tokenizer (skipped where it is not cached): V0 is the base case itself, every variant keeps
    the bridge at one index shared by O and S, the sentence comes first, and the pointer's move is the base's."""
    from scripts import statement_positions as SP

    try:
        tok = SP.load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    cases, _ = R.scenes(tok, 12)
    base = [c for c in cases if c["condition"] == "C2"]
    out, dropped = R.prepend_cases(tok, base, R.PREPEND, R.window_fillers(tok, 10, 12))
    assert len(out) == len(R.PREPEND) * len(base) and not dropped
    by = {(c["base_scene"], c["variant"]): c for c in out}
    for b in base:
        v0 = by[(b["scene"], "V0")]
        assert v0["readers"] == b["readers"] and v0["pos"] == b["pos"] and v0["context"] == b["context"]
        for v in R.PREPEND[1:]:
            c = by[(b["scene"], v)]
            assert c["context"] == c["prepended"] + " " + b["context"]
            assert c["cf_context"] == c["prepended"] + " " + b["cf_context"]
            assert c["move"] == v0["move"] and 0 <= c["move"][0] <= 2
            ids = c["readers"][LK]["ids"]
            assert len(ids["org"]) == len(ids["alt"]) and ids["org"][c["pos"]] != ids["alt"][c["pos"]]
            assert tok.decode(ids["org"][c["pos"]]).strip() == b["bridge"]


def test_nochat_rendering_on_the_tokenizer():
    from scripts import statement_positions as SP

    try:
        tok = SP.load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    chat, _ = R.scenes(tok, 5)
    plain, _ = R.scenes(tok, 5, rendering="nochat")
    assert [c["context"] for c in chat] == [c["context"] for c in plain]  # the same scenes
    c = plain[0]
    text = tok.decode(c["readers"][LK]["ids"]["org"])
    assert c["rendering"] == "nochat" and "<|im_start|>" not in text and text.endswith("Answer:")
    assert tok.decode(c["readers"][LK]["ids"]["org"][c["pos"]]).strip() == c["bridge"]


# ---- 45a: the code's shift -------------------------------------------------------------------------------------------


def test_code_shift_is_x8_writes_beta():
    g = torch.Generator().manual_seed(0)
    alf, _ = torch.linalg.qr(torch.randn(30, 4, generator=g))
    step = alf @ torch.randn(4, generator=g)  # mu_j+1 - mu_j lies in the pointer span
    assert abs(R.code_shift(0.7 * step, alf, step)["beta"] - 0.7) < 1e-5
    dh = torch.randn(30, generator=g)
    d = (dh @ alf) @ alf.T
    got = R.code_shift(dh, alf, step)
    assert abs(got["beta"] - float(d @ step / (step @ step))) < 1e-5 and abs(got["norm_d"] - float(d.norm())) < 1e-5
    off = dh - alf @ (alf.T @ dh)  # a change outside the pointer span shifts nothing
    assert abs(R.code_shift(off, alf, step)["beta"]) < 1e-5


def test_prepend_betas_pair_each_variant_with_its_v0():
    g = torch.Generator().manual_seed(2)
    alf, _ = torch.linalg.qr(torch.randn(20, 4, generator=g))
    mu = {k: alf @ torch.randn(4, generator=g) for k in range(5)}
    chosen, h = [], []
    for b, j in (("C2-0001", 0), ("C2-0002", 2)):
        for v in R.PREPEND:
            chosen.append({"scene": f"{b}-{v}", "base_scene": b, "variant": v, "bridge": "duck", "move": [j, 1]})
            h.append(torch.randn(20, generator=g))
    got = R.prepend_betas(chosen, h, alf, mu)
    assert len(got) == 8 and {r["variant"] for r in got} == set(R.PREPEND[1:])
    r = next(r for r in got if r["scene"] == "C2-0002-V3")
    want = R.code_shift(h[8] - h[5], alf, mu[3] - mu[2])  # C2-0002's V3 against its own V0, slot 2 -> 3
    assert r["j"] == 2 and abs(r["beta"] - want["beta"]) < 1e-6
    assert R.prepend_betas([c for c in chosen if c["variant"] != "V0"], h[1:5] + h[6:], alf, mu) == []  # no V0


def test_control_parts_hold_idouts_share_and_the_union():
    from scripts.x0_parts import omp_atoms

    g = torch.Generator().manual_seed(5)
    d, n = 40, 6
    jdic = torch.randn(80, d, generator=g)
    jdic = jdic / jdic.norm(dim=1, keepdim=True)
    alf, _ = torch.linalg.qr(torch.randn(d, 3, generator=g))
    pca, _ = torch.linalg.qr(torch.randn(d, d, generator=g))
    pca = pca.T.contiguous()  # unit rows
    x = torch.randn(n, d, generator=g)
    means = {e: torch.randn(d, generator=g) for e in ("a", "b", "c", "e", "f", "h", "k", "m", "p", "q")}
    chosen = [{"scene": f"C0-{i:04d}", "bridge": "a", "cf_bridge": "b"} for i in range(n)]
    u = torch.randn(n, d, generator=g)
    u = u / u.norm(dim=1, keepdim=True)
    idout = R.rank1_part(x, u)
    atoms = omp_atoms(jdic, x, 5)
    parts, k = R.control_parts(x, idout, means, chosen, jdic, atoms, alf, pca)
    share = lambda p: p.norm(dim=1) ** 2 / x.norm(dim=1) ** 2  # noqa: E731
    target = share(idout)
    one_step = (x.norm(dim=1) ** -2)[:, None] * (x @ pca.T) ** 2  # one PCA atom's share
    assert ((share(parts["pca"]) - target).abs() <= one_step.max(dim=1).values / 2 + 1e-5).all()  # closest k
    assert len(k["k_wrong"]) == n and all(kw <= len(means) - 3 for kw in k["k_wrong"])
    for i in range(n):  # the union holds nothing left along the scene's atoms, the pointer or the control
        rest = x[i] - parts["jpp+alf+wrong"][i]
        assert (jdic[atoms[i]] @ rest).abs().max() < 1e-4 and (alf.T @ rest).abs().max() < 1e-4
        assert float((parts["wrong"][i] @ rest).abs()) < 1e-3
        rest = x[i] - parts["jpp+alf+pca"][i]
        top = (x[i] @ pca.T).abs().argsort(descending=True)[: k["k_pca"][i]]
        assert torch.cat([pca[top] @ rest, alf.T @ rest]).abs().max() < 1e-4  # k_pca may be 0: the pointer alone
    assert (share(parts["jpp+alf+wrong"]) >= share(parts["wrong"]) - 1e-5).all()


# ---- 45a: the rule ---------------------------------------------------------------------------------------------------


def _prepend_rows(pos_keep: dict[str, float], n: int = 120, variants=R.PREPEND) -> list[dict]:
    """n base scenes, every other one a first-locker move; on first-locker moves the only-pointer arm answers position
    in the first pos_keep[v] share of the scenes (spread over the 20 entities); other arms and moves: original."""
    rows = []
    for i in range(n):
        move = [0, 2] if i % 2 == 0 else [1, 2]
        for v in variants:
            for a in R.PREPEND_ARMS:
                k = i // 2
                pos = move[0] == 0 and a == "keep_alf" and k < pos_keep[v] * (n // 2)
                base = {"scene": f"C2-{i:04d}-{v}", "base_scene": f"C2-{i:04d}", "condition": "C2", "variant": v,
                        "move": move, "entity": f"e{i % 20}", "arm": a}  # fmt: skip
                rows += [{**base, "reader": LK, "route": "position" if pos else "original", "switched": 0},
                         {**base, "reader": RC, "route": None, "switched": 0}]  # fmt: skip
    return rows


def test_first_locker_rule_says_first_locker():
    r = R.first_locker_rule(_prepend_rows({"V0": 0.8, "V1": 0.1, "V2": 0.2, "V3": 0.0, "V4": 0.75}), [], 300)
    assert r["verdict"] == "First locker stated before any item"
    assert r["cut"] == {"V1": True, "V2": True, "V3": True, "V4": False} and not r["order_of_lockers"]
    assert r["moves"]["first_locker"]["n"] == 60 and r["moves"]["all"]["n"] == 120
    assert abs(r["pos_keep_alf"]["V1"] - 0.1) < 1e-9


def test_first_locker_rule_says_order_of_lockers():
    r = R.first_locker_rule(_prepend_rows({"V0": 0.6, "V1": 0.55, "V2": 0.7, "V3": 0.6, "V4": 0.2}), [], 300)
    assert r["verdict"] == "Order of lockers, picks ignored" and not r["first_locker"]
    assert r["near"]["V2"]  # exactly 0.10 from V0 counts as within


def test_first_locker_rule_says_mixed():
    # V1 and V2 cut, V3 only to 0.6 of V0 (neither half nor within 0.10)
    r = R.first_locker_rule(_prepend_rows({"V0": 0.8, "V1": 0.1, "V2": 0.2, "V3": 0.5, "V4": 0.8}), [], 300)
    assert r["verdict"] == "mixed"
    # V4 also cut: not "first locker" either
    r = R.first_locker_rule(_prepend_rows({"V0": 0.8, "V1": 0.1, "V2": 0.2, "V3": 0.0, "V4": 0.1}), [], 300)
    assert r["verdict"] == "mixed" and r["cut"]["V4"]


def test_first_locker_rule_flags_both_rules():
    """V0's only-pointer share small enough that a cut to half is also within 0.10: the first rule is reported."""
    r = R.first_locker_rule(_prepend_rows({"V0": 0.1, "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.1}), [], 300)
    assert r["first_locker"] and r["order_of_lockers"] and r["both_rules_hold"]
    assert r["verdict"] == "First locker stated before any item"


def test_first_locker_rule_needs_every_variant_and_a_ci():
    rows = _prepend_rows({"V0": 0.8, "V1": 0.1, "V2": 0.2, "V3": 0.0}, variants=R.PREPEND[:4])
    assert R.first_locker_rule(rows, [], 200)["verdict"] == "not tested (gate missed: V4)"
    # a cut that rests on one entity's scenes: half of V0 on the point, but the CI of the cut includes 0
    rows = _prepend_rows({v: 0.0 for v in R.PREPEND})
    for r in rows:
        if r["reader"] == LK and r["arm"] == "keep_alf" and r["move"][0] == 0 and r["entity"] == "e0":
            r["route"] = "position" if r["variant"] == "V0" else "original"
    res = R.first_locker_rule(rows, [], 300)
    assert res["pos_keep_alf"]["V0"] > 0 and res["moves"]["first_locker"]["keep_alf_cut_vs_V0"]["V1"][1] <= 0
    assert not res["cut"]["V1"] and res["verdict"] != "First locker stated before any item"


def test_first_locker_rule_reads_beta_per_slot():
    beta = [{"variant": "V4", "j": i % 3, "entity": f"e{i % 10}", "beta": 1.0 if i % 3 == 0 else 0.0,
             "norm_d": 1.0, "norm_step": 2.0} for i in range(90)]  # fmt: skip
    r = R.first_locker_rule(_prepend_rows({v: 0.5 for v in R.PREPEND}), beta, 200)
    assert r["beta"]["V4|0"]["beta"][0] == 1.0 and r["beta"]["V4|1"]["beta"][0] == 0.0
    assert abs(r["beta"]["V4|all"]["beta"][0] - 1 / 3) < 1e-9 and r["beta"]["V4|all"]["norm_ratio_median"] == 0.5


# ---- 45e: the wrong-pair control and the rule -------------------------------------------------------------------------


def _means(d=30, ents=("org", "alt", "c", "d", "e", "f", "g"), seed=0):
    g = torch.Generator().manual_seed(seed)
    return {e: torch.randn(d, generator=g) for e in ents}


def test_wrong_pair_basis_spans_other_pairs_only():
    means = _means()
    x = torch.randn(30, generator=torch.Generator().manual_seed(1))
    q, share = R.wrong_pair_basis(means, ("org", "alt"), x, 1.0, random.Random(0))
    others = [e for e in means if e not in ("org", "alt")]
    diffs = torch.stack([means[b] - means[a] for a in others for b in others if a < b], 1)
    assert q.shape[1] == len(others) - 1  # target 1: every independent difference of the other entities
    assert torch.allclose(q.T @ q, torch.eye(q.shape[1]), atol=1e-5)
    resid = q - diffs @ torch.linalg.lstsq(diffs, q).solution
    assert resid.norm() < 1e-3  # inside the span of the other pairs' differences
    assert abs(share - float((q.T @ x).norm() ** 2 / x.norm() ** 2)) < 1e-5
    own = means["alt"] - means["org"]
    assert float((q.T @ own).norm() / own.norm()) < 0.999  # the scene's own identity direction is not in it


def test_wrong_pair_basis_stops_at_the_closest_share():
    e1 = torch.zeros(10)
    e1[0] = 1.0
    means = {"org": torch.ones(10), "alt": -torch.ones(10), "c": torch.zeros(10), "d": e1}  # one other pair: e1
    x = torch.zeros(10)
    x[0], x[1] = 0.4**0.5, 0.6**0.5  # e1 holds 0.4 of ||x||^2
    assert R.wrong_pair_basis(means, ("org", "alt"), x, 0.15, random.Random(0))[0].shape[1] == 0  # 0 is closer
    q, share = R.wrong_pair_basis(means, ("org", "alt"), x, 0.25, random.Random(0))
    assert q.shape[1] == 1 and abs(share - 0.4) < 1e-6
    assert R.wrong_pair_basis(means, ("org", "alt"), x, 0.0, random.Random(0))[0].shape[1] == 0


def test_wrong_pair_basis_is_seeded():
    means, x = _means(seed=3), torch.randn(30, generator=torch.Generator().manual_seed(4))
    a = R.wrong_pair_basis(means, ("org", "alt"), x, 0.3, random.Random("4505|C0-0001"))[0]
    b = R.wrong_pair_basis(means, ("org", "alt"), x, 0.3, random.Random("4505|C0-0001"))[0]
    assert torch.equal(a, b)


def _identity_rows(left_idout: float, left_wrong: float, id_idout: float, id_wrong: float, n: int = 100):
    """C0: every scene switches with the whole change, the given shares without J++ + pointer + idout / + wrong pair;
    C2: the identity answers' share under the whole change 0.8, without idout / the wrong pair as given."""
    rows = []
    for i in range(n):
        e = f"e{i % 25}"
        frac = i / n
        for a, sw in (("whole", True), ("no_jppalfidout", frac < left_idout), ("no_jppalfwrong", frac < left_wrong),
                      ("no_jppalfpca", frac < 0.5)):  # fmt: skip
            rows += [{"scene": f"C0-{i:04d}", "condition": "C0", "entity": e, "reader": LK, "arm": a, "route": "other",
                      "switched": int(sw)},
                     {"scene": f"C0-{i:04d}", "condition": "C0", "entity": e, "reader": RC, "arm": a, "route": None,
                      "switched": 1}]  # fmt: skip
        for a, ident in (("whole", 0.8), ("no_idout", id_idout), ("no_wrong", id_wrong), ("no_pca", 0.7),
                         ("no_idout_rand", 0.8), ("no_wrong_rand", 0.8), ("no_pca_rand", 0.8), ("no_jppalfidout", 0.1),
                         ("no_jppalfwrong", 0.5), ("no_jppalfpca", 0.5)):  # fmt: skip
            rows += [{"scene": f"C2-{i:04d}", "condition": "C2", "entity": e, "reader": LK, "arm": a,
                      "route": "identity" if frac < ident else "position", "switched": 0},
                     {"scene": f"C2-{i:04d}", "condition": "C2", "entity": e, "reader": RC, "arm": a, "route": None,
                      "switched": 0}]  # fmt: skip
    return rows


def test_identity_control_flags_read_planted_rows():
    f = R.identity_control_flags(_identity_rows(0.1, 0.6, 0.2, 0.7), 200)
    assert f["holds_i"] and f["holds_ii"] and f["both"] and f["tested"]
    assert abs(f["c0"]["left"]["no_jppalfidout"][0] - 0.1) < 1e-9 and abs(f["c2"]["idout_vs_wrong"][0] - 0.5) < 1e-9
    f = R.identity_control_flags(_identity_rows(0.1, 0.15, 0.2, 0.7), 200)  # 0.10 > half of 0.15
    assert not f["holds_i"] and f["holds_ii"] and not f["both"]
    f = R.identity_control_flags(_identity_rows(0.1, 0.2, 0.2, 0.35), 200)  # exactly half; cut 0.15 more: both hold
    assert f["holds_i"] and f["holds_ii"]
    f = R.identity_control_flags(_identity_rows(0.1, 0.6, 0.2, 0.3), 200)  # cut only 0.10 more
    assert not f["holds_ii"]


def test_identity_control_flags_without_the_control_arms():
    rows = [r for r in _identity_rows(0.1, 0.6, 0.2, 0.7) if "wrong" not in r["arm"]]
    f = R.identity_control_flags(rows, 100)
    assert f["c0"] is None and f["c2"] is None and not f["both"] and not f["tested"]


def test_identity_specific_counts_two_of_three_models():
    yes, no = {"both": True, "tested": True}, {"both": False, "tested": True}
    assert R.identity_specific({"9b": yes, "27b": yes, "muse": no})["specific"]
    res = R.identity_specific({"9b": yes, "27b": no, "muse": {"both": False, "tested": False}})
    assert not res["specific"] and res["held_on"] == ["9b"] and res["untested"] == ["muse"]


# ---- 45i ------------------------------------------------------------------------------------------------------------


def test_never_value_reads_the_whole_change():
    rows = [{"scene": f"s{i}", "condition": "C2", "entity": f"e{i % 10}", "reader": LK, "arm": a,
             "route": "identity" if i % 2 else "position"} for i in range(40) for a in ("whole", "no_alf")]  # fmt: skip
    nv = R.never_value(rows, 100)
    assert nv["holds"] and nv["value_zero_in_every_arm"] and nv["arms"]["whole"]["identity"][0] == 0.5
    rows[-1]["route"] = "value"  # one value answer without the pointer: still holds on the whole change
    nv = R.never_value(rows, 100)
    assert nv["holds"] and not nv["value_zero_in_every_arm"]
    rows[0]["route"] = "value"  # the whole change
    assert not R.never_value(rows, 100)["holds"]


# ---- the verdict, the summary, the examples, --sealed ----------------------------------------------------------------


def _run_dir(tmp_path, monkeypatch, name, manifest, rows, norms, **files):
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    src = tmp_path / name
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "fake"}, "layer": 12, **manifest}))
    for fname, data in {"outcomes.jsonl": rows, "norms.jsonl": norms, **files}.items():
        (src / fname).write_text("".join(json.dumps(r) + "\n" for r in data))
    return src


def test_verdict_of_a_prepend_run(tmp_path, monkeypatch):
    rows = _prepend_rows({"V0": 0.8, "V1": 0.1, "V2": 0.2, "V3": 0.0, "V4": 0.75})
    norms = [{"scene": r["scene"], "condition": "C2", "variant": r["variant"], "norm": 1.0}
             for r in rows if r["reader"] == LK and r["arm"] == "whole"]  # fmt: skip
    beta = [{"variant": "V1", "j": 0, "entity": "e1", "beta": 0.2, "norm_d": 1.0, "norm_step": 1.0}]
    _run_dir(tmp_path, monkeypatch, "fake", {"conditions": ["C2"], "prepend": list(R.PREPEND)}, rows, norms,
             **{"beta.jsonl": beta})  # fmt: skip
    out = R.stage_verdict("fake", 100)
    blob = json.loads((out / "verdict.json").read_text())
    assert blob["x45a"]["verdict"] == "First locker stated before any item"
    assert {(b["variant"], b["arm"]) for b in blob["rows"]} == {(v, a) for v in R.PREPEND for a in R.PREPEND_ARMS}
    assert "First locker stated before any item" in (out / "verdict.md").read_text()


def _stamps(monkeypatch):
    """Analysis folders are stamped by the second: distinct stamps for several in one test."""
    n = iter(range(1000))
    monkeypatch.setattr(R.time, "strftime", lambda fmt, t=None: f"t{next(n):03d}")


def test_verdict_and_summary_of_identity_control_runs(tmp_path, monkeypatch):
    _stamps(monkeypatch)
    for name, (lw, iw, ok) in {"r9": (0.6, 0.7, True), "r27": (0.6, 0.7, True), "rm": (0.15, 0.7, True),
                               "rx": (0.6, 0.7, False)}.items():  # fmt: skip
        rows = _identity_rows(0.1, lw, 0.2, iw)
        norms = [{"condition": c, "norm": 1.0} for c in ("C0", "C2")]
        _run_dir(tmp_path, monkeypatch, name, {"conditions": ["C0", "C2"], "identity_controls": True}, rows, norms)
        (tmp_path / name / "c0_check.json").write_text(json.dumps({"ok": ok}))
    blob = json.loads((R.stage_verdict("r9", 100) / "verdict.json").read_text())
    assert blob["x45e"]["both"]
    s = json.loads(next((R.stage_idctrl_summary(["r9", "r27", "rm"], 100)).glob("x45e.json")).read_text())
    assert s["specific"] and s["held_on"] == ["r9", "r27"]
    s = json.loads(next((R.stage_idctrl_summary(["r9", "rm", "rx"], 100)).glob("x45e.json")).read_text())
    assert not s["specific"] and s["untested"] == ["rx"]  # a failed C0 check: not tested


def test_verdict_of_a_nochat_run(tmp_path, monkeypatch):
    rows = [{"scene": f"s{i}", "condition": "C2", "entity": f"e{i % 10}", "reader": w, "arm": "whole",
             "route": "position" if w == LK else None, "switched": 0} for i in range(30) for w in (LK, RC)]  # fmt: skip
    _run_dir(tmp_path, monkeypatch, "fake", {"conditions": ["C2"], "rendering": "nochat", "read": "X0 digit"}, rows,
             [{"condition": "C2", "norm": 1.0}])  # fmt: skip
    out = R.stage_verdict("fake", 100)
    assert json.loads((out / "verdict.json").read_text())["x45i"]["holds"]
    assert "Never the value" in (out / "verdict.md").read_text()


def test_examples_mark_the_patch_and_list_every_arm(tmp_path, monkeypatch):
    _stamps(monkeypatch)
    cases, rows = [], []
    for i in range(30):
        ids = [100 + i, 7, 8, 9, 10]
        rd = {"question": "q", "answer": "4", "cf_answer": "3", "ids": {"org": ids, "alt": [*ids[:2], 99, *ids[3:]]}}
        cases.append({"scene": f"C2-{i:04d}", "condition": "C2", "bridge": "duck", "cf_bridge": "frog", "pos": 2,
                      "expect": {"identity": 3}, "readers": {LK: rd, RC: rd}})  # fmt: skip
        rows += [{"scene": f"C2-{i:04d}", "reader": w, "arm": a, "top": 50 + j, "route": "identity" if w == LK else None,
                  "switched": 1} for w in (LK, RC) for j, a in enumerate(("none", "whole", "no_alf"))]  # fmt: skip
    _run_dir(tmp_path, monkeypatch, "fake", {"conditions": ["C2"]}, rows, [], **{"cases.jsonl": cases})
    out = R.stage_examples("fake", decode=lambda ids: "".join(f"<{t}>" for t in ids))
    blob = json.loads((out / "examples.json").read_text())
    assert blob["k"] == 10 and blob["of"] == 30 and len({e["scene"] for e in blob["examples"]}) == 10
    e = blob["examples"][0]
    assert e["readers"][LK]["prompt_O"].endswith("<7>⟦<8>⟧<9><10>")
    assert e["readers"][LK]["prompt_S"].endswith("<7>⟦<99>⟧<9><10>")
    assert [a["arm"] for a in e["readers"][LK]["arms"]] == ["none", "whole", "no_alf"]
    assert e["readers"][LK]["arms"][1]["answer"] == "<51>"
    again = json.loads((R.stage_examples("fake", decode=lambda ids: "") / "examples.json").read_text())
    assert [x["scene"] for x in again["examples"]] == [x["scene"] for x in blob["examples"]]  # seed 0


@pytest.mark.parametrize(("flags", "verdict"), [(["--sealed"], False), ([], True), (["--smoke"], False)])
def test_sealed_runs_skip_the_verdict(monkeypatch, flags, verdict):
    called = {}
    monkeypatch.setattr(R, "stage_run", lambda *a, **k: called.setdefault("run", k))
    monkeypatch.setattr(R, "stage_verdict", lambda *a, **k: called.setdefault("verdict", True))
    monkeypatch.setattr(sys, "argv", ["x6_routes.py", "run", "--name", "x", *flags])
    R.main()
    assert called["run"]["sealed"] == ("--sealed" in flags) and ("verdict" in called) == verdict
