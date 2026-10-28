"""scripts/x51_travel.py (batch 51, test 51.4): items on a fake tokenizer, the last-token fit, the arms and their
random twins, the rule on planted numbers (every label and the bars), the entity-held-out probe on planted states, a
planted run through the CPU verdict, and the seal (no download)."""

from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x51_travel as T


class FakeTok:
    """' ' -> [1]; a digit d -> [100 + d]; anything else -> one id per character."""

    def __call__(self, text: str, add_special_tokens: bool = False):
        if text == " ":
            return SimpleNamespace(input_ids=[1])
        if text.isdigit():
            return SimpleNamespace(input_ids=[100 + int(c) for c in text])
        return SimpleNamespace(input_ids=[200 + ord(c) % 50 for c in text])


def case(scene: str = "C0-0001", bridge: str = "goat") -> dict:
    ctx = ("The locker of the beetle is 2. The locker of the tiger is 4. The locker of the goat is 9. Leo picked the "
           "tiger. Amy picked the beetle. Ivan picked the goat.")  # fmt: skip
    readers = {X.LOOKUP: {"question": "Which locker belongs to Ivan's pick?", "answer": "9", "tok_A": 109,
                          "ids": {"org": list(range(20)), "alt": list(range(20))}},
               X.RECALL: {"question": "How many legs does Ivan's pick have?", "answer": "4", "tok_A": 104,
                          "ids": {"org": list(range(23)), "alt": list(range(23))}}}  # fmt: skip
    return {"scene": scene, "bridge": bridge, "context": ctx, "pos": 12, "space": [1], "readers": readers}


def test_layers_and_last_position():
    assert T.layers_of("qwen3.5-9b") == (12, 16)
    assert T.layers_of("qwen3.6-27b") == (32, 36)
    assert T.layers_of("muse-glimmer-30b") == (26, 30)
    assert T.last_position(list(range(20)), [1]) == 20  # the appended read token


def test_item_record_slots_and_read_positions():
    it = T.item_record(FakeTok(), case(), "read")
    assert it["j"] == 2 and it["ks"] == [0, 1]
    assert it["slots"] == [["beetle", 2], ["tiger", 4], ["goat", 9]]
    assert it["digit_tokens"] == [102, 104, 109]
    assert it["readers"][X.LOOKUP]["last"] == 20 and it["readers"][X.RECALL]["last"] == 23
    assert it["half"] == "read" and it["space"] == [1]
    marked = T.marked(lambda ids: "".join(f"<{t}>" for t in ids), it)
    assert marked.startswith("<0>") and "⟦bridge:<12>⟧" in marked and marked.endswith("⟦last:<1>⟧")


def test_class_means_fit_half_only_and_every_slot_required():
    states = np.arange(12, dtype=np.float32).reshape(6, 2)
    j = np.array([0, 1, 2, 0, 1, 2])
    fit = np.array([True, True, True, False, False, False])
    mu = T.class_means(states, j, fit)
    assert np.allclose(mu[0], [0, 1]) and np.allclose(mu[2], [4, 5])  # the read half's rows are not used
    with pytest.raises(AssertionError, match="slot 2"):
        T.class_means(states, j, np.array([True, True, False, True, True, False]))


def test_arm_specs_order_and_halves():
    it = {"ks": [0, 2]}
    fit_specs = T.arm_specs(it, (12, 16), has_last=False)
    read_specs = T.arm_specs(it, (12, 16), has_last=True)
    assert len(fit_specs) == 2 * 2 * 2 * 2 and len(read_specs) == 2 * 2 * 2 * 4
    assert {a for a, *_ in fit_specs} == {"bridge_swap", "bridge_random"}
    assert read_specs[:4] == [("bridge_swap", 12, 0, 1.0), ("bridge_random", 12, 0, 1.0), ("last_swap", 12, 0, 1.0),
                              ("last_random", 12, 0, 1.0)]  # fmt: skip


def test_arm_vectors_swap_and_matched_random():
    d = 16
    g = torch.Generator().manual_seed(0)
    mu = {(f, la): {k: torch.randn(d, generator=g) for k in range(3)} for f in T.FITS for la in (12, 16)}
    specs = T.arm_specs({"ks": [0, 2]}, (12, 16), has_last=True)
    vecs = T.arm_vectors(specs, 1, mu, torch.Generator().manual_seed(4401))
    again = T.arm_vectors(specs, 1, mu, torch.Generator().manual_seed(4401))
    for (arm, la, k, s), v, w in zip(specs, vecs, again, strict=True):
        assert torch.equal(v, w)  # seeded
        fit, kind = arm.split("_")
        if kind == "swap":
            assert torch.allclose(v, s * (mu[(fit, la)][k] - mu[(fit, la)][1]))
            swap = v
        else:
            assert torch.isclose(v.norm(), swap.norm()) and abs(float(v @ swap / v.norm() / swap.norm())) < 0.9


def cells(bs: float, br: float, ls: float, lr: float = 0.0, where=None) -> dict:
    """Every cell at the given values; where = (layer tag, s): only that cell gets them, the rest 0."""
    out = {}
    for la in ("L", "L+4"):
        for s in T.DOSES:
            on = where is None or where == (la, s)
            for arm, v in (("bridge_swap", bs), ("bridge_random", br), ("last_swap", ls), ("last_random", lr)):
                out[(arm, la, s)] = v if on else 0.0
    return out


def test_rule_labels_and_bars():
    hi_probe, lo_probe = {"L": 0.95, "L+4": 0.6}, {"L": 0.5, "L+4": 0.5}
    r = T.rule(cells(0.30, 0.05, 0.0, where=("L+4", 2.0)), lo_probe)
    assert r["key"] == "travels" and r["travel_cells"] == ["L+4 s=2"]  # both bars exactly met count
    assert T.rule(cells(0.45, 0.06, 0.0, where=("L", 1.0)), lo_probe)["key"] == "between"  # random above 0.05
    r = T.rule(cells(0.10, 0.0, 0.30, where=("L", 2.0)), lo_probe)
    assert r["key"] == "reencoded" and r["last_high_cells"] == ["L s=2"]
    assert T.rule(cells(0.11, 0.0, 0.5), lo_probe)["key"] == "between"  # bridge-fit above 0.10, under 0.30
    assert T.rule(cells(0.05, 0.0, 0.10), hi_probe)["key"] == "not_last"
    assert T.rule(cells(0.05, 0.0, 0.10), {"L": 0.79, "L+4": 0.5})["key"] == "between"  # the probe misses 0.8
    assert T.rule(cells(0.05, 0.0, 0.2), hi_probe)["key"] == "between"  # last-fit between the bars
    assert T.rule(cells(0.0, 0.0, 0.0), {"L": 0.3, "L+4": 0.80})["key"] == "not_last"  # the probe at L + 4 counts
    assert T.rule(cells(0.5, 0.0, 0.5), lo_probe)["label"] == T.LABELS["travels"]


def test_probe_rows_entity_held_out_on_planted_states():
    rng = np.random.default_rng(0)
    n, d = 120, 24
    ents = [f"e{i % 12}" for i in range(n)]
    j = [int(x) for x in rng.integers(0, 3, n)]
    noise = rng.normal(size=(n, 2, d))
    code = np.zeros((n, 2, d))
    for i, t in enumerate(j):
        code[i, 0, t] = 4.0  # layer 0 carries the slot, layer 1 is noise
    rows = T.probe_rows((noise + code).astype(np.float16), j, ents, [f"s{i}" for i in range(n)], [3, 7])
    acc = {la: np.mean([r["right"] for r in rows if r["layer"] == la]) for la in (3, 7)}
    assert acc[3] > 0.9 and acc[7] < 0.6
    fold = {}
    for r in rows:
        assert fold.setdefault((r["layer"], r["entity"]), r["fold"]) == r["fold"]  # whole entities per fold


def test_seal(monkeypatch):
    text = "**Q51.4** (51.4) Does the address travel?\n- (a) x\n- (d) In between.\n\nDan:\n\n**Q51.5** x\n\nDan: 60%\n"
    assert T.parse_answer(text) == ""
    filled = text.replace("Dan:\n\n**Q51.5", "Dan (9B): (a) 60%\nDan (27B): (b) 55%\n- if not\n\n**Q51.5")
    assert T.parse_answer(filled) == "(a) 60%\nDan (27B): (b) 55%\n- if not"
    assert T.parse_answer(text.replace("Dan:\n\n**Q51.5", "Dan: (c) 70%\n\n**Q51.5")) == "(c) 70%"
    monkeypatch.setattr(T, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        T.stage_verdict(["qwen35_9b_x51_4"], n_boot=10)
    with pytest.raises(AssertionError, match="sealed"):
        T.stage_view(["qwen35_9b_x51_4"])


def planted_run(root, run: str) -> None:
    """12 items over 6 entities (alternating fit / read by entity); at L the bridge-fit swap sends every lookup to
    slot k at s = 2 and none at s = 1, its random never; the last-token arms never; the probe right everywhere."""
    src = root / run
    src.mkdir(parents=True)
    ents = [f"e{i // 2}" for i in range(12)]
    fit, _ = T.A.split_halves(ents)
    lay = [12, 16]
    rows, norms, probe, items = [], [], [], []
    for i in range(12):
        j = i % 3
        half = "fit" if ents[i] in fit else "read"
        base = {"scene": f"s{i}", "entity": ents[i], "half": half, "j": j}
        items.append({**base, "ks": [k for k in range(3) if k != j], "slots": [["a", 1], ["b", 2], ["c", 3]], "pos": 12,
                      "space": [1], "readers": {w: {"ids": list(range(20)), "last": 20, "answer": "1"} for w in X.READERS}})  # fmt: skip
        rows.append({**base, "reader": X.LOOKUP, "arm": "none", "layer": None, "k": None, "s": 0.0, "top": 1,
                     "class": "slot0", "right": 1})  # fmt: skip
        rows.append(
            {**base, "reader": X.RECALL, "arm": "none", "layer": None, "k": None, "s": 0.0, "top": 7, "changed": 0}
        )
        nr = {
            "scene": f"s{i}",
            "entity": ents[i],
            "half": half,
            "h_last_L12": 100.0,
            "h_last_L16": 120.0,
            "h_bridge_L12": 50.0,
        }
        for arm, la, k, s in T.arm_specs(items[-1], (12, 16), half == "read"):
            hit = arm == "bridge_swap" and la == 12 and s == 2.0
            rows.append({**base, "reader": X.LOOKUP, "arm": arm, "layer": la, "k": k, "s": s, "top": 2,
                         "class": "target" if hit else "original", "right": 0})  # fmt: skip
            rows.append({**base, "reader": X.RECALL, "arm": arm, "layer": la, "k": k, "s": s, "top": 7, "changed": 0,
                         "recall_class": "other"})  # fmt: skip
            nr[f"{arm}|L{la}|k{k}|s{s:g}"] = 5.0 * s
        norms.append(nr)
        probe += [{"layer": la, "scene": f"s{i}", "entity": ents[i], "j": j, "pred": j, "right": 1, "majority_right": 0,
                   "fold": 0} for la in range(20)]  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", items)
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "norms.jsonl", norms)
    X.write_jsonl(src / "probe.jsonl", probe)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"}, "layers": lay}))
    (src / "status.json").write_text(json.dumps({"status": "tested", "items": 12}))


def test_planted_run_through_the_verdict(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "RESULTS", tmp_path)
    planted_run(tmp_path, "qwen35_9b_x51_4")
    (tmp_path / "muse30_x51_4").mkdir()
    (tmp_path / "muse30_x51_4" / "manifest.json").write_text(json.dumps({"model": {"target": "muse-glimmer-30b"}}))
    (tmp_path / "muse30_x51_4" / "status.json").write_text(
        json.dumps({"status": "not tested", "gate": {"pass": False}})
    )
    r = T.analyse("qwen35_9b_x51_4", n_boot=50)
    assert r["key"] == "travels" and r["travel_cells"] == ["L s=2"]
    assert r["cells"]["bridge_swap|L|2.0"] == pytest.approx(1.0) and r["cells"]["bridge_swap|L|1.0"] == 0.0
    assert r["swap_minus_random"]["bridge|all|L|s2"][0] == pytest.approx(1.0)
    assert r["ratio_to_h_last_L"]["bridge_swap|L|s2"] == pytest.approx(0.1)  # 10 / 100
    assert r["bridge_swap_s1_over_h_bridge_L_median"] == pytest.approx(0.1)  # 5 / 50
    assert r["probe"][12]["acc"][0] == 1.0 and r["label_per_layer"] == {
        "L": T.LABELS["travels"],
        "L+4": T.LABELS["not_last"],  # nothing moves at L + 4 while the probe reads the slot
    }
    assert T.analyse("muse30_x51_4")["status"] == "not tested"
    assert T.analyse("x51_4_27b")["status"] == "pending"
    monkeypatch.setattr(T, "dan_answer", lambda rev="HEAD": "Dan (9B): (a) 60%")
    out = T.stage_verdict(["qwen35_9b_x51_4", "muse30_x51_4", "x51_4_27b"], n_boot=50)
    md = (out / "verdict.md").read_text()
    assert "**(a) the code travels**" in md and "not tested" in md and "pending" in md
    assert (out / "travel_qwen3.5-9b.png").exists()
    view = T.stage_view(["qwen35_9b_x51_4", "muse30_x51_4"], decode_for=lambda target: lambda ids: f"<{ids[0]}>")
    text = (view / "view.md").read_text()
    assert text.count("random rows of") == 5 and text.count("⟦last:<1>⟧") == 2 * T.N_PROMPTS
    assert "muse30_x51_4" not in text  # not tested: no view
