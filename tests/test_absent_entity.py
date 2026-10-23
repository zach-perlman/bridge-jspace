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
    assert fam["original_asks_1st"]["n"] == 3 * 4 * 4 * 4


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
    rows, checks = [], []
    for it in its[:300]:
        p = it["sources"]["dissoc"]["predictions"]
        base = {"family": "RL", "domain": it["domain"], "name": it["id"], "group": "last", "layer": 50}
        rows += [{**base, "source": "unedited", "layer": -1, "group": "-", "top": p["none"], "role": "none"},
                 {**base, "source": "dissoc", "top": p["position"], "role": "position"},
                 {**base, "source": "rand", "top": p["none"], "role": "none"},
                 {**base, "source": "same", "top": p["none"], "role": "none"}]  # fmt: skip
        checks.append({"name": it["id"], "check": "donor_unedited", "top": p["value"], "correct": True})
    run = tmp_path / "runs" / m["run"]
    (run / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (run / "checks.jsonl").write_text("".join(json.dumps(c) + "\n" for c in checks))
    assert AE.main(["--run", m["run"], "--out", str(tmp_path / "out")]) == 0
    assert "RL (decisive): order" in capsys.readouterr().out
    (d,) = (tmp_path / "out").iterdir()
    out = json.loads((d / "verdict.json").read_text())
    assert out["families"]["RL"]["verdict"] == "order" and out["counts"]["both_right"] == 300


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
