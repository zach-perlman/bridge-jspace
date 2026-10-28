"""Batch 48, test 48.5 (scripts/x48_route2.py): the scene selection and the writes, the recall's and the lookup's
answer classes, the write + no-J++ composition on a tiny fake causal model (CPU), the rule on planted numbers, and the
sealed verdict. No real model. The fake tokenizer, model and lens are tests/test_x45p.py's."""

import json
import re
from types import SimpleNamespace

import pytest
from test_x45p import ALT, ORG, FakeLens, FakeModel, WordTok

from scripts import x0_necessity as X
from scripts import x45p as P
from scripts import x48_route2 as Q

# ORG: slots tick (2) / rabbit (1) / bee (3) / frog (5); Iris's pick frog (j = 3) -> bee (slot 2); legs: tick 8,
# rabbit 4, bee 6, frog 4
LEGS = {"tick": 8, "rabbit": 4, "bee": 6, "frog": 4}


# ---- scenes ---------------------------------------------------------------------------------------------------------


def test_lockers_read_digits_and_words():
    assert Q.lockers(ORG) == [("tick", 2), ("rabbit", 1), ("bee", 3), ("frog", 5)]
    assert Q.lockers("The locker of iota is five. Ivan picked iota. The locker of beta is 3.") == [
        ("iota", 5),
        ("beta", 3),
    ]
    assert Q.number_of(" five") == 5 and Q.number_of("0") == 0


def test_writes_every_other_slot_and_informative():
    slots = Q.lockers(ORG)
    w = Q.writes_of(slots, j=3, new_slot=2, attrs=LEGS)
    assert [x["k"] for x in w] == [0, 1, 2]
    by = {x["k"]: x for x in w}
    assert by[0]["informative"] and by[0]["item"] == "tick" and by[0]["attribute"] == 8 and by[0]["locker"] == 2
    assert not by[1]["informative"]  # the rabbit has the frog's legs: the answer could not tell them apart
    assert not by[2]["informative"] and by[2]["is_changed_slot"]  # the bee is the changed item itself


def test_arms_order_and_parse():
    assert Q.arms_of([0, 1, 2]) == ["none", "whole", "a1", "w0", "p0", "r0", "w1", "p1", "r1", "w2", "p2", "r2"]
    assert Q.parse_arm("a1") == ("a1", None) and Q.parse_arm("r2") == ("random", 2)
    assert Q.parse_arm("w0") == ("write", 0) and Q.parse_arm("p1") == ("alone", 1)


def fake_item(i: int, tok: WordTok, org_before: bool = True) -> dict:
    """A 45p item of ORG / ALT (Iris's pick frog -> bee) as x45p.select writes it, with x0_strata's features."""
    it = _x45p_item(i, tok)
    it["features"] = {
        "alt locker vs asked pick": "before",
        "org locker vs asked pick": "before" if org_before else "after",
    }
    it["context"], it["cf_context"] = ORG, ALT
    it["cf_bridge"], it["entity"] = "bee", "frog"
    it["new"]["index"] = 2
    for w, rd in it["readers"].items():
        rd["question"] = (
            "How many legs does Iris's pick have?" if w == X.RECALL else "Which locker belongs to Iris's pick?"
        )
        rd["answer"], rd["cf_answer"] = ("4", "6") if w == X.RECALL else ("5", "3")
    return it


def _x45p_item(i: int, tok: WordTok) -> dict:
    from test_x45p import item_record

    return item_record(i, tok)


def test_select_keeps_locker_first_originals_and_builds_the_writes(monkeypatch):
    tok = WordTok()
    base = [fake_item(i, tok, org_before=(i % 3 != 0)) for i in range(9)]
    monkeypatch.setattr(P, "select", lambda *_: (base, {"items": 9, "dropped": {}}))
    items, counts = Q.select(tok, "run", 12)
    assert counts["45p_items"] == 9 and counts["items"] == len(items) == 6
    assert counts["org locker vs asked pick"] == {"before": 6, "after": 3}
    assert counts["writes"] == 18 and counts["informative_writes"] == 6
    assert counts["uninformative_by_reason"] == {"the changed item's slot": 6,
                                                 "the same attribute as the original's or the changed item's": 6}  # fmt: skip
    it = items[0]
    assert it["j"] == 3 and it["new_slot"] == 2 and it["slots"] == [["tick", 2], ["rabbit", 1], ["bee", 3], ["frog", 5]]
    assert it["attributes"] == LEGS and [w["k"] for w in it["writes"]] == [0, 1, 2]
    assert "stored" in it and "new" not in it and list(it["marks"]) == ["bridge"]


def test_select_refuses_an_answer_that_is_not_the_fact(monkeypatch):
    tok = WordTok()
    it = fake_item(0, tok)
    it["readers"][X.RECALL]["answer"] = "2"
    monkeypatch.setattr(P, "select", lambda *_: ([it], {"items": 1, "dropped": {}}))
    with pytest.raises(AssertionError, match="recall answer is not the fact"):
        Q.select(tok, "run", 12)


# ---- classes --------------------------------------------------------------------------------------------------------


def item_for_classes() -> dict:
    return {"slots": [["tick", 2], ["rabbit", 1], ["bee", 3], ["frog", 5]], "j": 3, "new_slot": 2, "entity": "frog",
            "cf_bridge": "bee", "attributes": LEGS}  # fmt: skip


def test_recall_class_first_match_in_order_and_every_match():
    it = item_for_classes()
    assert Q.recall_class("8", it, 0) == ("slot_k", ["slot_k"])
    assert Q.recall_class("4", it, 0) == ("original", ["original"])
    assert Q.recall_class("6", it, 0) == ("changed", ["changed"])
    assert Q.recall_class("2", it, 0) == ("other", [])
    # k = 1 (the rabbit, 4 legs as the frog): slot k first, both matches recorded
    assert Q.recall_class("4", it, 1) == ("slot_k", ["slot_k", "original"])
    # k = 2 (the changed item's own slot): slot k first, 'changed' recorded too
    assert Q.recall_class("6", it, 2) == ("slot_k", ["slot_k", "changed"])


def test_lookup_class_by_locker_number():
    it = item_for_classes()
    assert Q.lookup_class("2", it, 0) == "slot_k"
    assert Q.lookup_class("5", it, 0) == "original"
    assert Q.lookup_class("3", it, 0) == "changed"
    assert Q.lookup_class("1", it, 0) == "other_slot"
    assert Q.lookup_class("9", it, 0) == "other"


# ---- the run stage on a fake model (CPU) ------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    tok = WordTok()
    base = [fake_item(i, tok) for i in range(12)]
    fake = FakeModel(tok)
    g = torch.Generator().manual_seed(7)
    mu = {k: torch.randn(32, generator=g).numpy() for k in range(5)}
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(MM, "pointer_means", lambda run: mu)
    monkeypatch.setattr(P, "select", lambda *_: (base, {"items": 12, "dropped": {}}))
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x48")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Q, "SPEC", tmp_path / "batch48.yaml")
    Q.SPEC.write_text("")
    src = tmp_path / "x0" / Q.RUN_45M[pins.TARGET]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    out = Q.stage_run(f"{pins.RUN_PREFIX}fake_run", "test")
    return SimpleNamespace(tok=tok, fake=fake, mu=mu, out=out, items=X.read_jsonl(out / "cases.jsonl"))


def test_run_stage_composes_the_write_on_the_no_jpp_change(fake_run):
    import torch

    from bridge_jspace import pins

    out, items, fake, mu = fake_run.out, fake_run.items, fake_run.fake, fake_run.mu
    arms = Q.arms_of([0, 1, 2])
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {(it["scene"], w, a) for it in items
                                                                    for w in X.READERS for a in arms}  # fmt: skip
    assert not any(p.name.startswith(("verdict", "x48_route2-")) for p in out.iterdir())  # sealed
    m = json.loads((out / "manifest.json").read_text())
    assert (
        m["s"] == 2
        and m["k"] == 25
        and "sealed" in m
        and m["write_norms"]["3-0"]
        == pytest.approx(2 * float(torch.linalg.norm(torch.tensor(mu[0] - mu[3]))), abs=1e-3)
    )
    la = X.PREDICTED[pins.TARGET]
    it, (seq, edits) = items[0], fake.calls[0]
    ids = it["readers"][X.LOOKUP]["ids"]
    assert seq == len(ids["org"]) + 1 and edits[0] == {} and len(edits) == len(arms)
    e = {arm: edit[la] for arm, edit in zip(arms[1:], edits[1:], strict=True)}
    assert all(x.positions == [it["pos"]] for x in e.values())  # every arm at the bridge token
    h = {v: fake.run(torch.tensor([ids[v]]), record=(la,))[1][la] for v in ("org", "alt")}
    jdic = FakeLens(None, "jpp").vectors(la, list(range(64)))
    whole = h["alt"][it["pos"]] - h["org"][it["pos"]]
    base = whole - X.fit(jdic, whole[None], 25, "signed")[0]
    assert torch.allclose(e["whole"].delta[0], whole) and torch.allclose(e["a1"].delta[0], base, atol=1e-5)
    j = it["j"]
    gen = torch.Generator().manual_seed(Q.RAND_SEED)
    for k in (0, 1, 2):
        step = 2 * torch.tensor(mu[k] - mu[j], dtype=torch.float32)
        assert torch.allclose(e[f"w{k}"].delta[0], base + step, atol=1e-5)
        assert torch.allclose(e[f"p{k}"].delta[0], step, atol=1e-5)
        rand = e[f"r{k}"].delta[0] - base
        assert float(rand.norm()) == pytest.approx(float(step.norm()), abs=1e-4)
        r = torch.randn(32, generator=gen)  # x8_write's draw, one per write in slot order
        assert torch.allclose(rand, r / r.norm() * step.norm(), atol=1e-4)
    # the next scene's random vectors continue the same generator (reads: the space token appended; the examples'
    # greedy calls are the others)
    reads = [ed for s, ed in fake.calls if s == len(ids["org"]) + 1]
    assert len(reads) == 2 * len(items)
    e2 = reads[2][arms.index("r0")][la].delta[0] - reads[2][arms.index("a1")][la].delta[0]
    r = torch.randn(32, generator=gen)
    assert torch.allclose(e2, r / r.norm() * e2.norm(), atol=1e-4)
    # rows: classes on the write arms only, informative as the item's writes say
    by = {(r["scene"], r["reader"], r["arm"]): r for r in rows}
    assert "class" not in by[(it["scene"], X.RECALL, "a1")]
    for k, inf in ((0, True), (1, False), (2, False)):
        rr = by[(it["scene"], X.RECALL, f"w{k}")]
        assert rr["informative"] is inf and rr["class"] in Q.RECALL_CLASSES and rr["k"] == k and rr["kind"] == "write"
        assert by[(it["scene"], X.LOOKUP, f"r{k}")]["class"] in Q.LOOKUP_CLASSES
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == 12 and set(norms[0]["write_norm"]) == {"0", "1", "2"}
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == X.K_EXAMPLES * len(X.READERS) * len(arms)


def test_verdict_is_sealed_until_dans_answer(fake_run, monkeypatch):
    monkeypatch.setattr(Q, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        Q.stage_verdict([fake_run.out.name], n_boot=50)


def test_verdict_stage_on_the_fake_run(fake_run, monkeypatch):
    from bridge_jspace import pins

    monkeypatch.setattr(Q, "dan_answer", lambda: "no · 60%")
    out = Q.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x48_route2.json").read_text())
    model = blob["models"][0]
    assert model["target"] == pins.TARGET and model["status"] == "tested"
    assert model["readers"]["recall"]["informative"]["n"] == 12 and model["readers"]["recall"]["all"]["n"] == 36
    assert {m["status"] for m in blob["models"][1:]} == {"pending"} and blob["verdict"]["label"] == "pending"
    assert (out / "examples.md").read_text().count("```") == 2 * X.K_EXAMPLES * len(X.READERS)
    assert set(model["checks"]) == {f"{w} {a} vs 45m's stored {s}" for w in ("lookup", "recall")
                                    for a, s in (("whole", "whole"), ("a1", "no_part"))}  # fmt: skip


# ---- the rule on planted numbers ------------------------------------------------------------------------------------


def planted(n: int, write: int, random: int, base: int = 0, alone: int = 0) -> list[dict]:
    """n informative writes: each kind names slot k's item on its first count writes, 'original' otherwise."""
    kinds = {"write": write, "random": random, "base": base, "alone": alone}
    return [{"scene": f"s{i}", "entity": f"e{i % 10}", "k": i % 3, "j": 3, "informative": True,
             **{kd: "slot_k" if i < c else "original" for kd, c in kinds.items()}} for i in range(n)]  # fmt: skip


def test_rule_holds_at_the_bars_inclusive():
    r = Q.rule(Q.numbers(planted(100, write=30, random=5), Q.RECALL_CLASSES, n_boot=200))
    assert r["status"] == "tested" and r["holds"] and r["write_ok"] and r["random_ok"]
    nums = Q.numbers(planted(100, write=60, random=0, base=10), Q.RECALL_CLASSES, n_boot=200)
    assert nums["share"]["write"]["slot_k"][0] == pytest.approx(0.6)
    assert nums["share"]["base"]["slot_k"][0] == pytest.approx(0.1)
    assert nums["share"]["write"]["original"][0] == pytest.approx(0.4)
    assert nums["write_minus_random_slot_k"][0] == pytest.approx(0.6)
    v = nums["write_minus_random_slot_k"]
    assert v[1] <= v[0] + 1e-12 <= v[2] + 1e-12


def test_rule_breaks_on_either_bar():
    r = Q.rule(Q.numbers(planted(100, write=29, random=5), Q.RECALL_CLASSES, n_boot=100))
    assert not r["holds"] and not r["write_ok"] and r["random_ok"]
    r = Q.rule(Q.numbers(planted(100, write=50, random=6), Q.RECALL_CLASSES, n_boot=100))
    assert not r["holds"] and r["write_ok"] and not r["random_ok"]
    assert Q.rule({"n": 0}) == {"status": "not tested", "holds": False, "why": "no informative writes"}


def test_batch_rule():
    def m(target: str, status: str, holds: bool = False) -> dict:
        return {"target": target, "status": status, "holds": holds}

    t = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
    assert Q.batch_verdict([m(t[0], "tested", True), m(t[1], "tested", True), m(t[2], "tested")])["label"] == "holds"
    assert Q.batch_verdict([m(t[0], "tested", True), m(t[1], "tested"), m(t[2], "tested")])["label"] == "does not hold"
    v = Q.batch_verdict([m(t[0], "tested", True), m(t[1], "pending"), m(t[2], "tested")])
    assert v["label"] == "pending" and v["per_model"] == {t[0]: "yes", t[1]: "pending", t[2]: "no"}
    assert Q.batch_verdict([m(t[0], "tested", True), m(t[1], "tested", True), m(t[2], "pending")])["Q48.5"] == "yes"


def test_dan_answer_reads_only_the_q48_5_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q48.4** (48.4) ...\n\nDan: yes · 60%\n\n**Q48.5** (48.5) ...\n\nRule: ...\n\nDan:{}\n"
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format("")))
    assert Q.dan_answer() == ""
    monkeypatch.setattr(Q.subprocess, "run", fake_git(blocks.format(" 9B yes · 60%; 27B no · 55%; Muse yes · 60%")))
    assert Q.dan_answer() == "9B yes · 60%; 27B no · 55%; Muse yes · 60%"
    assert re.match(r"^Dan:\s*$", "Dan:", re.M)  # the committed file's empty line is what seals the verdict
