"""Batch 49, test 49.6 (scripts/x49_report.py): the reworded report prompts and answers (a fake tokenizer; the target's
cached tokenizer: 47.10's scenes, both wordings rendered as X0's chat prompt, one answer token each), the run stage on
a fake model (reads per scene and wording, sealed), accuracy by true slot and the rule on planted reads, 47.10's
reference from its competence rows, the seal, and the verdict and view on the fake run. No real model."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from scripts import x0_necessity as X
from scripts import x47_report as Q
from scripts import x49_report as V
from tests import test_x47_report as TQ


def test_answers_follow_the_slot_in_each_wording(monkeypatch):
    monkeypatch.setattr(Q, "prompt", TQ.fake_prompt)
    tok = TQ.WordTok()
    for slot, digit, word in ((0, "1", "first"), (1, "2", "second"), (2, "3", "third")):
        pos = V.build_reader(tok, TQ.ORG, "Iris", slot, "position", "last")
        sen = V.build_reader(tok, TQ.ORG, "Iris", slot, "sentence", "last")
        assert (pos["answer"], pos["kind"]) == (digit, "digit") and (sen["answer"], sen["kind"]) == (word, "word")
        assert sen["tok_A"] == tok(" " + word).input_ids[0] and pos["tok_A"] == tok(digit).input_ids[0]
    rd = V.build_reader(tok, TQ.ORG, "Iris", 0, "position", "last")
    assert "Was the locker of Iris's pick listed in position 1, 2 or 3 of the list?" in rd["text"]
    rd = V.build_reader(tok, TQ.ORG, "Iris", 0, "sentence", "first")
    q = "Which of the three locker sentences - the first, the second or the third - gives the locker of Iris's pick?"
    assert rd["question"] == q and rd["text"].index(q) < rd["text"].index(TQ.ORG)  # question-first


def test_prompts_on_the_targets_tokenizer():
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    tok = TQ._real_tokenizer()
    items, counts = V.build_items(tok, n_gen=40)
    base, _ = Q.build_items(tok, 40, V.ORDERS)
    assert [it["scene"] for it in items] == [it["scene"] for it in base]  # 47.10's scenes and drops
    assert counts["true_slot"] and sum(counts["true_slot"].values()) == len(items)
    cands = V.candidates(tok)
    assert [tok.decode([t]) for t in cands["digit"]] == ["1", "2", "3"]
    assert [tok.decode([t]) for t in cands["word"]] == [" first", " second", " third"]
    for it in items:
        for w, rd in it["orders"]["last"].items():
            assert rd["text"] == T.render(tok, {"format": "prose", "kind": V.KIND[w], "context": it["context"],
                                                "question": rd["question"]})  # fmt: skip
            assert rd["text"].count(it["context"]) == 1 and rd["text"].endswith("Answer:")
            assert (T.DIGIT_INSTRUCTION if V.KIND[w] == "digit" else S.INSTRUCTION) in rd["text"]
            assert rd["tok_A"] == cands[rd["kind"]][it["slot"]]
            assert rd["ids"] == tok(rd["text"], add_special_tokens=False).input_ids
        assert it["locker"] == base[items.index(it)]["orders"]["last"]["readers"]["lookup"]["answer"]


def test_the_two_qwen_tokenizers_read_the_answers_alike():
    from bridge_jspace.review import checks as RC

    try:
        toks = [RC.tokenizer(t) for t in V.MODELS]
    except Exception as e:
        pytest.skip(f"tokenizer.json not cached: {e}")
    for text in ("1", "2", "3", " first", " second", " third", " "):
        assert len({tuple(t.encode(text, add_special_tokens=False).ids) for t in toks}) == 1, text


# ---- the rule on planted reads ----------------------------------------------------------------------------------------


def planted_rows(acc: dict[str, dict[int, float]], n: int = 60, order: str = "last") -> list[dict]:
    """Reads per wording: n scenes per true slot (entities e0-e5), said right in the share acc[wording][slot]."""
    rows = []
    for w, by in acc.items():
        for slot, a in by.items():
            for i in range(n):
                ok = int(i < round(a * n))
                rows.append({"scene": f"s{slot}-{i}", "entity": f"e{i % 6}", "order": order, "wording": w, "slot": slot,
                             "said_right": ok, "read_right": ok, "cand_right": ok, "said_locker": 1 - ok,
                             "cand_slot": slot if ok else slot % 3 + 1})  # fmt: skip
    return rows


def test_by_slot_and_confusion_on_planted_reads():
    rows = planted_rows({"position": {1: 0.1, 2: 0.9, 3: 0.5}})
    c = V.by_slot(rows, (*V.MEASURES, "locker"), n_boot=200)
    assert [round(c[s]["said"][0], 3) for s in V.SLOTS] == [0.1, 0.9, 0.5] and c["all"]["n"] == 180
    assert abs(c["1"]["locker"][0] - 0.9) < 1e-9 and c["1"]["said"][1] <= 0.1 <= c["1"]["said"][2]
    conf = V.confusion(rows)
    assert conf["1"] == {"1": 6, "2": 54, "3": 0} and conf["3"] == {"1": 30, "2": 0, "3": 30}


def cells(s1: dict[str, float]) -> dict[str, dict]:
    return {w: {"1": {V.RULE_MEASURE: [v, 0, 1]}} for w, v in s1.items()}


def test_rule_stays_only_under_both_wordings():
    assert V.label_of(cells({"position": 0.2, "sentence": 0.2}))["label"] == "stays"  # the bar is inclusive
    r = V.label_of(cells({"position": 0.21, "sentence": 0.05}))
    assert r["label"] == "recovers" and r["recovers_under"] == ["position"]
    assert V.label_of(cells({"position": 0.0, "sentence": 0.9}))["label"] == "recovers"


def test_decide_reads_the_9b_question_last():
    def model(target: str, label: str) -> dict:
        return {"target": target, "status": "tested", "orders": {"last": {"rule": {"label": label}}}}

    v = V.decide([model("qwen3.6-27b", "recovers"), model("qwen3.5-9b", "stays")])
    assert v["action"] == "keep as an appendix curiosity" and v["Q49.6"] == "no"
    assert V.decide([model("qwen3.6-27b", "stays"), model("qwen3.5-9b", "recovers")])["action"] == "drop"
    assert V.decide([model("qwen3.6-27b", "stays")])["label"] == "pending"


def test_reference_reads_47_10s_question_last_o_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(Q, "RESULTS", tmp_path)
    src = tmp_path / V.REFERENCE["qwen3.5-9b"]
    src.mkdir()
    X.write_jsonl(src / "cases.jsonl", [{"scene": f"s{i}", "entity": f"e{i % 4}"} for i in range(30)])
    comp = [{"scene": f"s{i}", "order": o, "reader": w, "variant": v, "slot": i % 3, "right": i % 3 != 0,
             "read_right": i % 3 == 1, "cand_right": True}
            for i in range(30) for o in ("last", "first") for w in Q.READERS for v in ("org", "alt")]  # fmt: skip
    X.write_jsonl(src / "competence.jsonl", comp)
    ref = V.reference("qwen3.5-9b", n_boot=50)
    assert ref is not None and set(ref) == set(V.OLD)
    assert ref["report"]["1"]["n"] == 10 and ref["report"]["1"]["said"][0] == 0.0 and ref["report"]["2"]["said"][0] == 1
    assert ref["report"]["2"]["read"][0] == 1.0 and ref["report"]["3"]["read"][0] == 0.0
    assert V.reference("qwen3.6-27b", n_boot=50) is None  # not here


def test_dan_answer_reads_only_the_q49_6_block(monkeypatch):
    blocks = "**Q49.3** x\n\nDan: (a)\n\n**Q49.6** The report ...\n\nDan:{}\n\n**Q49.7** y\n\nDan: (a) · 60%\n"
    monkeypatch.setattr(V.subprocess, "run", TQ.fake_git(blocks.format("")))
    assert V.dan_answer() == ""
    monkeypatch.setattr(V.subprocess, "run", TQ.fake_git(blocks.format(" 9B 20%; 27B 70%")))
    assert V.dan_answer() == "9B 20%; 27B 70%"


def test_the_committed_predictions_file_has_the_q49_6_block():
    from bridge_jspace import pins

    text = (pins.REPO_ROOT / V.PREDICTIONS).read_text()
    assert "**Q49.6**" in text and "Slot 1 is reported right" in text


# ---- the run stage on a fake model --------------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = TQ.WordTok()
    fake = TQ.FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(Q, "prompt", TQ.fake_prompt)
    monkeypatch.setattr(V, "RESULTS", tmp_path / "x49_report")
    monkeypatch.setattr(Q, "RESULTS", tmp_path / "x47_report")  # no 47.10 reference: hermetic
    monkeypatch.setattr(pins, "TARGET", "qwen3.5-9b")
    monkeypatch.setattr(pins, "RUN_PREFIX", "qwen35_9b_")
    for w in (" first", " second", " third", "first", "second", "third", "First", "Second", "Third", " First",
              " Second", " Third", "1", "2", "3", " "):  # fmt: skip
        tok.vocab.setdefault(w, len(tok.vocab))

    def fake_items(tok_, n_gen, orders):
        items = []
        for i in range(n_gen):
            c = TQ.fake_case(tok_)
            c["scene"] = f"C0-{i:04d}"
            it, why = Q.build_item(tok_, c, orders)
            assert it is not None, why
            it["entity"] = f"e{i % 6}"
            items.append(it)
        return items, {"generated_C0": n_gen, "items": n_gen, "dropped": {}}

    monkeypatch.setattr(Q, "build_items", fake_items)
    out = V.stage_run("qwen35_9b_fake_run", "test", orders=("last", "first"), n_gen=12)
    return SimpleNamespace(tok=tok, fake=fake, out=out, n=12)


def test_run_stage_on_a_fake_model(fake_run):
    out, n = fake_run.out, fake_run.n
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "49.6" and "sealed" in m and set(m["wordings"]) == set(V.WORDINGS)
    assert m["switches"]["target"] == "qwen3.5-9b" and set(m["orders"]) == {"last", "first"}
    assert not any(p.name.startswith(("view", "x49_6")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == n * 2 * len(V.WORDINGS)
    assert {(r["order"], r["wording"]) for r in rows} == {(o, w) for o in ("last", "first") for w in V.WORDINGS}
    assert all(r["slot"] == 1 and r["cand_slot"] in (1, 2, 3) for r in rows)  # the fake case: frog in slot 1
    items = X.read_jsonl(out / "cases.jsonl")
    assert items[0]["locker"] == "5" and items[0]["orders"]["last"]["position"]["answer"] == "1"
    # the read: X0's chat read of the wording's own prompt with 47.10's suffix for its kind
    it, ws = items[0], X.whitespace_mask(fake_run.fake)
    for w in V.WORDINGS:
        rd = it["orders"]["last"][w]
        lg = X.read_logits(fake_run.fake, rd["ids"], [{}], "chat", Q.suffix(fake_run.tok, V.KIND[w]), ws)[0][0]
        r = next(r for r in rows if r["scene"] == it["scene"] and r["order"] == "last" and r["wording"] == w)
        assert r["top"] == int(lg.argmax())


def test_verdict_and_view_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(V, "dan_answer", lambda: "9B 20%; 27B 70%")
    out = V.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x49_6.json").read_text())
    mm = blob["models"][0]
    assert mm["target"] == "qwen3.5-9b" and set(mm["orders"]) == {"last", "first"}
    assert mm["orders"]["last"]["cells"]["position"]["1"]["n"] == fake_run.n
    assert mm["orders"]["last"]["cells"]["position"]["2"]["n"] == 0
    assert blob["verdict"]["label"] in ("stays", "recovers") and blob["models"][1]["status"] == "pending"
    md = (out / "x49_6.md").read_text()
    assert "UNVERIFIED" in md and "Verdict" in md and "confusion" in md
    view = V.stage_view(fake_run.out.name, decode=fake_run.tok.decode)
    text = (view / "examples.md").read_text()
    assert text.count("```") == 2 * min(X.K_EXAMPLES, fake_run.n) * 2 * len(V.WORDINGS)


def test_verdict_and_view_are_sealed(fake_run, monkeypatch):
    monkeypatch.setattr(V, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        V.stage_verdict([fake_run.out.name], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        V.stage_view(fake_run.out.name, decode=fake_run.tok.decode)
