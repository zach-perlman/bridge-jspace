"""absent_entity (Dan's B4): the absent-entity donor, the outcome classes, the decisive pool and the proposed rule, on
synthetic cases."""

import math

import pytest

from scripts import absent_entity as AE
from scripts import pointer_v4 as PV4

POOL = ["France", "Italy", "Spain", "Germany", "Japan", "Egypt", "Peru", "Norway"]


def _split(cue: dict[str, int] | None = None) -> dict:
    return {"domains": {"countries": {"pool": POOL, "cue_tokens": cue or dict.fromkeys(POOL, 1)}}}


def _item(fam: str = "RL", a: int = 2, k: int = 3, scene: str = "countries-e5f0-0000") -> dict:
    """A pointer_v4 item: the original lists POOL[:5] with digits 1-5 and asks slot a; the dissoc donor asks the
    entity at the original's slot c (France or Italy) with the digit 9 at slot k."""
    order, digits = POOL[:5], [1, 2, 3, 4, 5]
    c = next(s for s in range(5) if s not in (a, k))
    q_s = order[c]
    s_order = [e for e in order if e != q_s]
    s_order.insert(k, q_s)
    s_digits = [6, 7, 8, 1]
    s_digits.insert(k, 9)
    d = {"entities": s_order, "digits": s_digits, "query": q_s, "answer": "9"}
    return {"id": f"countries-{fam}-e5f0-0000", "family": fam, "domain": "countries", "scene": scene,
            "entities": order, "digits": digits, "query": order[a], "answer": str(digits[a]),
            "slots": {"query": a, "identity": c, "position": k}, "templates": {"statement": 0, "question": 0},
            "sources": {"dissoc": d, "same": {}}}  # fmt: skip


def test_the_donor_asks_an_entity_absent_from_the_original():
    it = _item()
    out = AE.absent_donor(it, _split())
    d = out["sources"]["dissoc"]
    x = d["query"]
    assert x not in it["entities"] and x in POOL[5:]
    assert d["entities"][3] == x and d["entities"][:3] == it["sources"]["dissoc"]["entities"][:3]
    assert d["digits"] == it["sources"]["dissoc"]["digits"] and d["answer"] == "9" and d["replaced"] == "France"
    assert PV4.cue_of("countries", x) in d["question"]
    assert d["context"] == " ".join(PV4.statements("countries", 0, d["entities"], d["digits"]))
    assert d["predictions"] == {"none": "3", "identity": "-", "position": "4", "first": "1", "value": "9"}
    assert out["entities"] == it["entities"] and out["slots"]["identity"] is None
    assert it["sources"]["dissoc"]["query"] == "France"  # the input item is not modified


def test_both_families_of_a_scene_get_the_same_absent_entity():
    rl = AE.absent_donor(_item("RL"), _split())["sources"]["dissoc"]
    dl = AE.absent_donor(_item("DL"), _split())["sources"]["dissoc"]
    assert rl["query"] == dl["query"]
    assert PV4.name_of("countries", dl["query"]) in dl["question"]
    xs = {AE.absent_donor(_item(scene=f"countries-e5f0-{i:04d}"), _split())["sources"]["dissoc"]["query"]
          for i in range(40)}  # fmt: skip
    assert xs == set(POOL[5:])  # seeded per scene, every candidate drawn


def test_the_absent_entity_has_the_asked_entitys_cue_length():
    cue = dict.fromkeys(POOL, 1) | {"Egypt": 2, "Peru": 2}
    for i in range(20):
        x = AE.absent_donor(_item(scene=f"countries-e5f0-{i:04d}"), _split(cue))["sources"]["dissoc"]["query"]
        assert x == "Norway"
    none_left = dict.fromkeys(POOL, 1) | dict.fromkeys(POOL[5:], 2)
    kept, dropped = AE.with_absent({"f": [_item()]}, _split(none_left))
    assert kept == {"f": []} and dropped == {"countries": 1}


def test_classify_names_coinciding_outcomes():
    p = {"none": "3", "position": "4", "first": "1", "value": "9"}
    assert [AE.classify(t, p) for t in ("4", "1", "3", "9", "7", " 4", "x")] == [
        "order", "fallback", "unchanged", "donor", "other_digit", "order", "other"]  # fmt: skip
    assert AE.classify("1", {"none": "3", "position": "1", "first": "1", "value": "9"}) == "order=fallback"
    assert AE.classify("1", {"none": "1", "position": "4", "first": "1", "value": "9"}) == "fallback=unchanged"


def test_decisive_needs_k_from_2_and_an_original_not_asking_its_first():
    assert AE.decisive(_item(a=2, k=3))
    assert not AE.decisive(_item(a=2, k=0))  # k_d = 1: order = fallback
    assert not AE.decisive(_item(a=0, k=3))  # the original asks its 1st: fallback = unchanged


def _run(order_share: float, fallback_share: float, rand_order: float = 0.0, n_per: int = 4):
    """Rows, checks and absent items over 3 topics x 4 entities x n_per scenes x every (a, k). Within each entity's
    decisive (and, separately, other) items, item j's dissoc read is the order digit if j % 10 < 10 * order_share, the
    fallback digit if below 10 * (order_share + fallback_share), else another digit; the random push gives the order
    digit if j % 10 < 10 * rand_order, else the original's answer."""
    rows, checks, items = [], [], {}
    cells = [(a, k) for a in range(5) for k in range(5) if a != k]
    for dom in ("animals", "body", "countries"):
        for e in "wxyz":
            seen = {True: 0, False: 0}
            for rep in range(n_per):
                for a, k in cells:
                    name = f"{dom}-RL-{e}-{rep}-{a}{k}"
                    digits = [1, 2, 3, 4, 5]
                    preds = {"none": str(digits[a]), "identity": "-", "position": str(digits[k]),
                             "first": str(digits[0]), "value": "9"}  # fmt: skip
                    items[name] = {"id": name, "domain": dom, "query": e, "slots": {"query": a, "position": k},
                                   "sources": {"dissoc": {"predictions": preds}}}  # fmt: skip
                    dec = AE.decisive(items[name])
                    j, seen[dec] = seen[dec] % 10, seen[dec] + 1
                    p = preds
                    top = (p["position"] if j < 10 * order_share else
                           p["first"] if j < 10 * (order_share + fallback_share) else "7")  # fmt: skip
                    r_top = p["position"] if j < 10 * rand_order else p["none"]
                    base = {"family": "RL", "domain": dom, "name": name, "group": "last", "layer": 50}
                    rows += [{**base, "source": "unedited", "layer": -1, "group": "-", "top": p["none"], "role": "none"},
                             {**base, "source": "dissoc", "top": top, "role": "position"},
                             {**base, "source": "rand", "top": r_top, "role": "none"},
                             {**base, "source": "same", "top": p["none"], "role": "none"}]  # fmt: skip
                    checks.append({"name": name, "check": "donor_unedited", "correct": True})
    return rows, checks, items


def test_rule_order_fallback_neither():
    for shares, expect in (((0.6, 0.1), "order"), ((0.1, 0.6), "fallback"), ((0.3, 0.3), "neither")):
        rows, checks, items = _run(*shares)
        fam = AE.verdict(rows, checks, items, 50)["families"]["RL"]
        assert fam["verdict"] == expect, (shares, fam["D_order_minus_fallback"])
        assert fam["n_decisive"] == 3 * 4 * 4 * 12  # k_d 2-5 and a != 1st: 12 of the 20 (a, k) cells


def test_the_random_push_can_block_order():
    rows, checks, items = _run(0.6, 0.1, rand_order=0.6)
    fam = AE.verdict(rows, checks, items, 50)["families"]["RL"]
    assert fam["D_order_minus_fallback"][1] > 0 and fam["verdict"] == "neither"


def test_k1_and_first_asked_are_reported_not_tested():
    rows, checks, items = _run(0.6, 0.1)
    fam = AE.verdict(rows, checks, items, 50)["families"]["RL"]
    assert set(fam["by_k"]) == {1, 2, 3, 4, 5} and "D" not in fam["by_k"][1] and "D" in fam["by_k"][2]
    assert any("=" in o for o in fam["by_k"][1]["all"])  # k_d = 1: order and fallback are one digit
    f1 = fam["original_asks_1st"]  # their own table: the patch and the random push, per k_d 2-5
    assert f1["patch"]["n"] == f1["random_push"]["n"] == 3 * 4 * 4 * 4
    assert set(f1["by_k"]) == {2, 3, 4, 5} and all(c["patch"]["n"] == 3 * 4 * 4 for c in f1["by_k"].values())
    assert any("fallback=unchanged" in o for o in f1["random_push"])  # the push leaves the 1st statement's answer
    text = AE.report({"run": "r", **AE.verdict(rows, checks, items, 50)}, "RL")
    assert (
        "Originals asking their 1st statement" in text and "| 2 | patch |" in text and "| all | random push |" in text
    )


def _ordinary(items: dict[str, dict], identity_share: float = 1.0) -> tuple[list[dict], dict[str, dict]]:
    """Finding 5's donor on the same items: its entity at slot 0 for entity 'w', else the last free slot; every read
    the identity digit for the first identity_share of each entity's items (j % 10 rule as _run), else the order digit."""
    o_items, rows, seen = {}, [], {}
    for name, it in items.items():
        a, k = it["slots"]["query"], it["slots"]["position"]
        c = next(s for s in ((0, 1, 2, 3, 4) if it["query"] == "w" else (4, 3, 2, 1, 0)) if s not in (a, k))
        digits = [1, 2, 3, 4, 5]
        preds = {"none": str(digits[a]), "identity": str(digits[c]), "position": str(digits[k]),
                 "first": str(digits[0]), "value": "9"}  # fmt: skip
        o_items[name] = {**it, "slots": {**it["slots"], "identity": c}, "sources": {"dissoc": {"predictions": preds}}}
        key = (it["domain"], it["query"])
        j, seen[key] = seen.get(key, 0) % 10, seen.get(key, 0) + 1
        top = preds["identity"] if j < 10 * identity_share else preds["position"]
        rows.append({"family": "RL", "domain": it["domain"], "name": name, "group": "last", "layer": 50,
                     "source": "dissoc", "top": top, "role": "identity"})  # fmt: skip
    return rows, o_items


def test_the_ordinary_donor_is_reported_beside_and_does_not_change_the_verdict():
    rows, checks, items = _run(0.6, 0.1)
    plain = AE.verdict(rows, checks, items, 50)["families"]["RL"]
    fam = AE.verdict(rows, checks, items, 50, _ordinary(items))["families"]["RL"]
    o = fam.pop("ordinary")
    assert fam == plain  # reported only
    assert o["n"] == fam["n_decisive"] and o["missing"] == 0 and set(o["by_k"]) == {2, 3, 4, 5}
    # every ordinary read is the identity digit: on entity w's items that is the 1st statement's digit (fallback)
    assert o["n_entity_first"] == 3 * 4 * 12
    assert o["D_order_minus_fallback"][0] == pytest.approx(-0.25) and o["D_without_entity_first"][0] == 0
    o2 = AE.verdict(rows, checks, items, 50, _ordinary(items, 0.0))["families"]["RL"]["ordinary"]
    assert o2["D_order_minus_fallback"][0] == 1.0  # every read the order digit


def test_classify_names_the_ordinary_identity():
    p = {"none": "3", "identity": "1", "position": "4", "first": "1", "value": "9"}
    assert AE.classify("1", p) == "fallback=identity"
    assert (
        AE.classify("1", {**p, "identity": "2"}) == "fallback"
        and AE.classify("2", {**p, "identity": "2"}) == "identity"
    )


def _smoke_inputs():
    rows, checks, items = _run(0.6, 0.1, n_per=1)
    ids = sorted(items)
    checks += [{"name": i, "check": kind, "same_top": True} for i in ids
               for kind in ("self_noop", "layer0_all_reproduces_source")]  # fmt: skip
    return rows, checks, ids


def test_the_smoke_gate_passes_a_complete_run_and_names_each_failure():
    rows, checks, ids = _smoke_inputs()
    assert AE.smoke_gate(rows, checks, ids, ids, 50) == []
    assert AE.smoke_gate(rows, checks, [], [], 50) == ["no sampled items"]
    donors_wrong = [{**c, "correct": i % 4 != 0} if c["check"] == "donor_unedited" else c for i, c in enumerate(checks)]
    assert any("donors read right" in w for w in AE.smoke_gate(rows, donors_wrong, ids, ids, 50))  # 75% < 80%
    no_rand = [r for r in rows if not (r["source"] == "rand" and r["name"] == ids[0])]
    assert any(w.startswith("rand rows") for w in AE.smoke_gate(no_rand, checks, ids, ids, 50))
    hook = [{**c, "same_top": False} if c["check"] == "self_noop" and c["name"] == ids[1] else c for c in checks]
    assert any(w.startswith("self_noop") for w in AE.smoke_gate(rows, hook, ids, ids, 50))
    base_wrong = [{**r, "role": "context"} if r["source"] == "unedited" and r["name"] == ids[2] else r for r in rows]
    assert any(w.startswith("originals read right") for w in AE.smoke_gate(base_wrong, checks, ids, ids, 50))
    assert any(w.startswith("donors.jsonl") for w in AE.smoke_gate(rows, checks, ids, ids[1:], 50))
    no_check = [c for c in checks if not (c["check"] == "donor_unedited" and c["name"] == ids[3])]
    assert any(w.startswith("donor_unedited checks") for w in AE.smoke_gate(rows, no_check, ids, ids, 50))


def test_wrong_donor_or_original_reads_are_left_out():
    rows, checks, items = _run(0.6, 0.1)
    bad = {c["name"] for c in checks[::2]}
    for c in checks[::2]:
        c["correct"] = False
    wrong_base = next(r["name"] for r in rows if r["source"] == "unedited" and r["name"] not in bad)
    for r in rows:
        if r["source"] == "unedited" and r["name"] == wrong_base:
            r["role"] = "context"
    out = AE.verdict(rows, checks, items, 50)
    assert out["counts"]["both_right"] == out["counts"]["items"] - len(bad) - 1
    assert out["families"]["RL"]["n"] == out["counts"]["both_right"]


def test_no_decisive_items_is_not_testable():
    nan3 = [math.nan] * 3
    assert AE.judge(nan3, nan3).startswith("not testable")
    assert AE.judge([0.3, 0.1, 0.5], nan3) == "not testable (no random-push rows)"  # no verdict without the control
    assert AE.judge([0.3, 0.1, 0.5], [0.0, -0.05, 0.05]) == "order"
    assert AE.judge([-0.3, -0.5, -0.1], [0.0, -0.05, 0.05]) == "fallback"


def test_rule_text_is_the_proposal():
    t = AE.rule_text()
    assert t.startswith("(the agent's proposal") and "order iff" in t and "random push" in t


def _manifest(tmp_path, monkeypatch, donor: str) -> dict:
    import json
    from types import SimpleNamespace

    from scripts import pointer_swap as PS

    monkeypatch.setattr(PS, "RESULTS", tmp_path)
    args = SimpleNamespace(name=f"d3_t_{donor}", why="test", data="pointer_v4", set="seed3", families=["RL", "DL"],
                           domains=None, levels=None, competence="d3v4_seed3_competence_27b", no_eligibility=False,
                           layers=[50], layer_step=2, family_roles=None, n=100, control_stride=2, groups=["last"],
                           question_max_layer=None, control_levels=None, primary_layers=None, donor=donor)  # fmt: skip
    PS.stage_manifest(args)
    return json.loads((tmp_path / args.name / "manifest.json").read_text())


def test_the_manifest_records_the_donor_only_when_absent(tmp_path, monkeypatch):
    if not (PV4.RESULTS / "d3v4_seed3_competence_27b" / "items.jsonl").exists():
        pytest.skip("seed3 competence run not present")
    m = _manifest(tmp_path, monkeypatch, "absent")
    assert m["donor"] == "absent" and m["donor_rule"] == AE.rule_text()
    plain = _manifest(tmp_path, monkeypatch, "dissoc")
    assert "donor" not in plain and "donor_rule" not in plain


def test_the_verdict_stage_end_to_end(tmp_path, monkeypatch, capsys):
    """A synthetic run on the spec's manifest: every patched read gives the order digit, the random push nothing."""
    import json

    from scripts import pointer_swap as PS

    if not (PV4.RESULTS / "d3v4_seed3_competence_27b" / "items.jsonl").exists():
        pytest.skip("seed3 competence run not present")
    m = _manifest(tmp_path / "runs", monkeypatch, "absent")
    kept, _ = AE.with_absent(PS.load_items(m))
    its = [it for it in AE.absent_cases([i for v in kept.values() for i in v]) if it["family"] == "RL"]
    rows, checks, o_rows = [], [], []
    for it in its[:300]:
        p = it["sources"]["dissoc"]["predictions"]
        base = {"family": "RL", "domain": it["domain"], "name": it["id"], "group": "last", "layer": 50}
        rows += [{**base, "source": "unedited", "layer": -1, "group": "-", "top": p["none"], "role": "none"},
                 {**base, "source": "dissoc", "top": p["position"], "role": "position"},
                 {**base, "source": "rand", "top": p["none"], "role": "none"},
                 {**base, "source": "same", "top": p["none"], "role": "none"}]  # fmt: skip
        checks += [{"name": it["id"], "check": "donor_unedited", "top": p["value"], "correct": True},
                   *({"name": it["id"], "check": k, "same_top": True}
                     for k in ("self_noop", "layer0_all_reproduces_source"))]  # fmt: skip
        o_rows.append({**base, "source": "dissoc", "top": p["first"], "role": "context"})  # the ordinary: fallback
    run = tmp_path / "runs" / m["run"]
    (run / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (run / "checks.jsonl").write_text("".join(json.dumps(c) + "\n" for c in checks))
    (run / "cases.jsonl").write_text("".join(json.dumps({"id": it["id"]}) + "\n" for it in its[:300]))
    # a smoke stops (exit 3) without the donors file, goes on (exit 0) with it; it writes nothing
    assert AE.main(["--run", m["run"], "--smoke", "--out", str(tmp_path / "out")]) == 3
    assert "STOP: donors.jsonl has 0 of 300" in capsys.readouterr().out
    (run / "donors.jsonl").write_text("".join(json.dumps(AE.donor_record(it)) + "\n" for it in its[:300]))
    assert AE.main(["--run", m["run"], "--smoke", "--out", str(tmp_path / "out")]) == 0
    assert "RUN" in capsys.readouterr().out and not (tmp_path / "out").exists()
    # finding 5's run on the same item files, reported beside
    o_run = tmp_path / "runs" / "d3_t_ordinary"
    o_run.mkdir()
    (o_run / "manifest.json").write_text(json.dumps({**m, "run": "d3_t_ordinary"}))
    (o_run / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in o_rows))
    (o_run / "checks.jsonl").write_text("")
    args = ["--run", m["run"], "--ordinary", "d3_t_ordinary", "--out", str(tmp_path / "out")]
    assert AE.main(args) == 0
    text = capsys.readouterr().out
    assert "RL (decisive): order" in text and "ordinary donor (finding 5's)" in text
    (d,) = (tmp_path / "out").iterdir()
    out = json.loads((d / "verdict.json").read_text())
    fam = out["families"]["RL"]
    assert fam["verdict"] == "order" and out["counts"]["both_right"] == 300 and out["ordinary"] == "d3_t_ordinary"
    assert fam["ordinary"]["n"] == fam["n_decisive"] and fam["ordinary"]["D_order_minus_fallback"][0] == -1.0


def test_every_seed3_scene_sampled_has_an_aligned_absent_donor():
    """Tokenizer: the spec's draw (seed3, RL and DL) gets a token-aligned absent-entity donor (pointer_swap.prepare's
    asserts), with four distinct predicted digits on the decisive items."""
    from scripts import pointer_swap as PS
    from scripts import pointer_v1 as PV

    try:
        tok = PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer")
    files = {f"seed3/{lab}": f for lab, f in PV4.set_files("seed3").items() if lab.split("_")[1] in ("RL", "DL")}
    if not all(f.exists() for f in files.values()):
        pytest.skip("pointer_v4 seed3 not present")
    items, _ = AE.with_absent({k: PV.load_file(f) for k, f in files.items()})
    for its in items.values():
        for it in AE.absent_cases(its[:40]):
            PS.prepare(it, tok)
            p = it["sources"]["dissoc"]["predictions"]
            if AE.decisive(it):
                assert len({p["none"], p["position"], p["first"], p["value"]}) == 4


@pytest.mark.parametrize("k", [0, 4])
def test_donor_record(k):
    out = AE.absent_donor(_item(a=2 if k else 1, k=k), _split())
    rec = AE.donor_record(out)
    assert rec["k_d"] == k + 1 and rec["absent_entity"] == out["sources"]["dissoc"]["query"]
