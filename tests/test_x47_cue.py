"""Batch 47, test 47.3 (scripts/x47_cue.py): the cue list, the scenes on the target's tokenizer (the cue one token, the
change at the cue token, no slot word in the description, the elimination and P_cf prompts), the rule on planted
outcomes, the sealed verdict and its view, and the run stage end to end on a tiny fake model (CPU). No real model."""

import json
import math
import re
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x47_cue as C


@pytest.fixture(scope="module")
def tok():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


# ---- cues ---------------------------------------------------------------------------------------------------------


def test_cue_candidates_are_unique_and_name_no_animal_slot_or_number():
    words = [w for cands in C.CUES.values() for w in cands]
    assert len(words) == len(set(words))
    for w in words:
        assert C.named(w) is None, w  # no cue is an animal word
        assert w.lower() not in C.SLOT_WORDS and not re.search(r"\d", w), w
    frame = set(re.findall(r"[a-z]+", C.FRAME.format(p="", cue="").lower()))
    assert not frame & C.SLOT_WORDS


def test_named_reads_the_first_animal_of_the_first_line():
    assert C.named("Frog.") == "frog" and C.named("Spiders\n") == "spider" and C.named("A honeybee") == "bee"
    assert C.named("Hens, of course") == "chicken" and C.named("the cat\nnot the dog") == "cat"
    assert C.named("7") is None and C.named("") is None and C.named("\nfrog") == "frog"  # suite_v1's first line


def test_cue_table_keeps_cues_at_the_bar():
    rows = [{"animal": a, "right": i < k, "named": a if i < k else "x"} for a, k in (("bee", 9), ("ant", 8))
            for i in range(10)]  # fmt: skip
    table, kept = C.cue_table(rows, {"bee": "honey", "ant": "colonies"})
    assert kept == {"bee": "honey"} and table["ant"]["share"] == 0.8 and not table["ant"]["kept"]


def test_feasible_needs_three_animals_and_two_leg_counts():
    assert not C.feasible({"bee": "honey", "ant": "colonies"})[0]
    assert not C.feasible({"cow": "milk", "dog": "loyalty", "pig": "bacon"})[0]  # all four-legged
    assert C.feasible({"cow": "milk", "dog": "loyalty", "bee": "honey"})[0]


def test_cue_list_on_the_tokenizer(tok):
    cues, dropped = C.cue_list(tok)
    for a, cue in cues.items():
        assert cue == next(c for c in C.CUES[a] if len(tok(" " + c, add_special_tokens=False).input_ids) == 1)
    assert all(a not in cues for a in dropped)
    assert C.feasible(cues)[0]


# ---- scenes on the tokenizer ----------------------------------------------------------------------------------------


def test_scenes_change_only_the_cue_and_the_moved_lockers(tok):
    from bridge_jspace.tokens import raw_encoding

    cues, _ = C.cue_list(tok)
    cases, why = C.scenes(tok, cues, 30)
    assert len(cases) == 30, why
    for c in cases:
        assert c["cue"] == cues[c["bridge"]] and c["cf_cue"] == cues[c["cf_bridge"]]
        assert not C.SLOT_WORDS & set(C.pick_words(c))
        assert f"picked the {c['bridge']}." not in c["context"]  # A is never named in a pick sentence of O
        lk = c["readers"][X.LOOKUP]
        org, alt, pos = lk["ids"]["org"], lk["ids"]["alt"], c["pos"]
        assert tok.decode([org[pos]]).strip() == c["cue"] and tok.decode([alt[pos]]).strip() == c["cf_cue"]
        text = C.render(tok, c["context"], lk["question"], "digit")
        enc = raw_encoding(tok, text, offsets=True)
        lockers = " ".join(f"The locker of the {x} is {d}." for x, d in c["lockers"])
        assert c["context"].startswith(lockers + " ")
        first_pick = text.index(c["context"]) + len(lockers) + 1  # the first pick sentence's first character
        start = next(i for i, (a, b) in enumerate(enc["offset_mapping"]) if b > first_pick)
        changed = [i for i, (p, q) in enumerate(zip(org, alt, strict=True)) if p != q]
        assert pos in changed and all(i < start for i in changed if i != pos)  # else only the locker sentences
        rc = c["readers"][X.RECALL]["ids"]
        assert rc["org"][: pos + 1] == org[: pos + 1] and rc["alt"][: pos + 1] == alt[: pos + 1]
        val, cf = dict(c["lockers"]), dict(c["cf_lockers"])
        e = c["expect"]
        assert (
            e["original"] == val[c["bridge"]]
            and e["identity"] == val[c["cf_bridge"]]
            and e["value"] == cf[c["cf_bridge"]]
        )
        slot = [x for x, _ in c["cf_lockers"]].index(c["cf_bridge"])
        assert e["position"] == c["lockers"][slot][1] and e["value"] not in val.values()
        d = c["decoy"]
        assert d is not None and d["animal"] not in (c["bridge"], c["cf_bridge"], c["third"])
        assert [i for i, (p, q) in enumerate(zip(org, d["ids"], strict=True)) if p != q] == [pos]
    assert {c["half"] for c in cases} == {"fit", "test"}
    assert sum(c["half"] == "fit" for c in cases) == 15


def test_pcf_pairs_move_the_bridges_locker_and_keep_every_digit(tok):
    cues, _ = C.cue_list(tok)
    cases, _ = C.scenes(tok, cues, 6)
    pairs, why = C.pcf_pairs(tok, cases)
    assert why["pairs"] == len(pairs) == 12
    for p in pairs:
        c = next(x for x in cases if x["scene"] == p["scene"])
        assert p["pos"] == c["pos"] and len(p["ids"]["alt"]) == len(p["ids"]["org"])
        assert p["ids"]["alt"][p["pos"]] == p["ids"]["org"][p["pos"]]  # the same cue: no identity change
        moved = re.findall(r"The locker of the (\w+) is (\d)\.", p["context"])
        assert {x: int(d) for x, d in moved} == dict(c["lockers"])  # every item keeps its digit
        i, j = p["slots"]
        assert moved[i][0] == p["partner"] and moved[j][0] == c["bridge"]


def test_split_is_seeded_and_half():
    ids = [f"C2-{i:04d}" for i in range(11)]
    assert C.split(ids) == C.split(list(reversed(ids))) and len(C.split(ids)) == 5


# ---- the rule on planted outcomes -----------------------------------------------------------------------------------


def planted(tmp_path, monkeypatch, *, lookup_loss=0.0, value=0.0, pcf_cut=True, gate_pass=True, cue_ok=True):
    """A planted run: 120 scenes, 30 bridge items, halves alternating. Lookup: identity on even scenes, position on odd
    ones; without J++ it loses `lookup_loss` of them (to original); recall: switches under every arm but without J++
    on even scenes. U' removed: the test half's position answers go to original (if pcf_cut). value: that share of
    the whole change's lookups are the value instead."""
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    src = tmp_path / "run"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.6-27b"}, "layer": 32}))
    kept = {"bee": "honey", "cow": "milk", "owl": "wisdom"}
    (src / "cues.json").write_text(json.dumps({"status": "ok" if cue_ok else "not tested", "why": "planted",
                                               "kept": kept, "one_token": kept, "dropped": {}}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"pass": gate_pass, "chosen": 120, "eligible": 150, "chosen_halves": {},
                                               "org_read_accuracy": {"PP": 0.9 if gate_pass else 0.7, "PM": 0.95}}))  # fmt: skip
    rows, norms, comp, decoys = [], [], [], []
    n_lose, n_val = round(120 * lookup_loss), round(120 * value)
    for i in range(120):
        s, half = f"C2-{i:04d}", ("fit", "test")[i % 2]
        base = {"scene": s, "half": half, "entity": f"e{i % 30}", "cf_entity": "x"}
        for a in ("none", *C.ARMS):
            route = "identity" if i % 2 == 0 else "position"
            if a == "none" or (a == "no_jpp" and i < n_lose) or (a == "no_pcf" and pcf_cut and half == "test"):
                route = "original"
            if a == "whole" and i >= 120 - n_val:
                route = "value"
            rows.append(
                {**base, "reader": X.LOOKUP, "arm": a, "route": route, "switched": int(route == "value"), "top": 1}
            )
            sw = int(a != "none" and not (a == "no_jpp" and i % 2 == 0))
            rows.append({**base, "reader": X.RECALL, "arm": a, "route": None, "switched": sw, "top": 2})
        norms.append({"scene": s, "half": half, "share_jpp": 0.2, "share_alf": 0.1, "share_pcf": 0.05})
        comp.append({"scene": s, "reader": X.LOOKUP, "variant": "org", "greedy": "The bee" if i < 3 else "5"})
        decoys.append({"scene": s, "class": "original" if i < 12 else "other"})
    for f, data in (("outcomes", rows), ("norms", norms), ("competence", comp), ("decoy", decoys)):
        X.write_jsonl(src / f"{f}.jsonl", data)
    return "run"


def test_rule_says_the_split_holds_never_the_value_and_a_pointer(tmp_path, monkeypatch):
    m = C.model_result(planted(tmp_path, monkeypatch), n_boot=200)
    assert m["status"] == "tested" and m["n"] == 120 and m["entities"] == 30
    assert m["lookup"]["excess"][0] == 0.0 and m["recall"]["excess"][0] == 0.5 and m["gap"][0] == 0.5
    assert m["value"][0] == 0.0 and m["pcf_cut_test"]["n"] == 60 and m["pcf_cut_test"]["cut"][0] == 1.0
    assert m["clauses"] == {"a": True, "a_prime": False, "b": True, "c": True}
    d = m["descriptive"]
    assert d["names_item_instead_of_digit"] == {"n": 120, "count": 3}
    assert d["elimination"]["n"] == 120 and d["elimination"][C.DECOY_CLASS["original"]] == 12
    assert d["pcf_cut_fit_half_in_sample"]["cut"][0] == 0.0 and d["median_share"]["jpp"] == 0.2


def test_rule_says_handed_through_the_lens_and_not_never_the_value(tmp_path, monkeypatch):
    m = C.model_result(planted(tmp_path, monkeypatch, lookup_loss=0.25, value=0.1, pcf_cut=False), n_boot=200)
    assert m["lookup"]["excess"][0] == pytest.approx(0.25) and m["value"][0] == pytest.approx(0.1)
    assert m["clauses"] == {"a": False, "a_prime": True, "b": False, "c": False}


def test_rule_bars_and_undefined_numbers():
    nan = float("nan")
    lk = lambda v: {"excess": [v, v, v]}  # noqa: E731
    assert C.rule(lk(0.10), [0.3, 0, 0], [0.05, 0, 0], [0.3, 0, 0]) == {
        "a": True,
        "a_prime": False,
        "b": True,
        "c": True,
    }
    assert C.rule(lk(0.2), [0.29, 0, 0], [0.06, 0, 0], [0.29, 0, 0]) == {"a": False, "a_prime": True, "b": False,
                                                                         "c": False}  # fmt: skip
    assert C.rule(lk(nan), [nan] * 3, [nan] * 3, [nan] * 3) == {"a": False, "a_prime": False, "b": False, "c": False}


def test_a_failed_gate_or_cue_step_is_not_tested(tmp_path, monkeypatch):
    m = C.model_result(planted(tmp_path, monkeypatch, gate_pass=False), n_boot=50)
    assert m["status"] == "not tested" and "gate" in m["why"]
    (tmp_path / "run").rename(tmp_path / "old")
    m = C.model_result(planted(tmp_path, monkeypatch, cue_ok=False), n_boot=50)
    assert m["status"] == "not tested" and "cue competence" in m["why"]
    assert C.model_result("muse30_x47_cue")["status"] == "pending"


# ---- sealed verdict and view --------------------------------------------------------------------------------------


def test_dan_answer_reads_only_the_q47_3_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.2** (47.2) ...\n\nDan: x\n\n**Q47.3** (47.3) ...\n\nAnswer per model.\n\nDan:{}\n"
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format("")))
    assert C.dan_answer() == ""
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format(" (a) 27B 70%") + "\n**Q47.4** y\n\nDan: z\n"))
    assert C.dan_answer() == "(a) 27B 70%"


def test_verdict_and_view_are_sealed_until_dans_answer(tmp_path, monkeypatch):
    run = planted(tmp_path, monkeypatch)
    monkeypatch.setattr(C, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_verdict([run], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_view([run], decode=lambda ids: "")
    assert [p.name for p in tmp_path.iterdir()] == [run]  # nothing written while sealed


def test_verdict_writes_the_table_and_the_view(tmp_path, monkeypatch):
    run = planted(tmp_path, monkeypatch)
    cases = [{"scene": f"C2-{i:04d}", "half": ("fit", "test")[i % 2], "bridge": "bee", "cf_bridge": "cow", "cue": "honey",
              "cf_cue": "milk", "pos": 2, "space": [9], "expect": {"identity": 1},
              "readers": {w: {"answer": "5", "cf_answer": "4", "ids": {"org": [1, 2, 3, 4], "alt": [1, 2, 5, 4]}}
                          for w in X.READERS}} for i in range(120)]  # fmt: skip
    X.write_jsonl(tmp_path / run / "cases.jsonl", cases)
    X.write_jsonl(tmp_path / run / "decoy.jsonl", [{"scene": "C2-0000", "decoy": "owl", "decoy_cue": "wisdom", "top": 1,
                                                    "class": "original"}])  # fmt: skip
    monkeypatch.setattr(C, "dan_answer", lambda: "(a) 60%")
    out = C.stage_verdict([run], n_boot=50, decode=lambda ids: "".join(f"<{i}>" for i in ids))
    md = (out / "x47_3.md").read_text()
    assert "(a) 60%" in md and "| qwen3.6-27b | run | tested | 120 (30) |" in md and "+12 (L32-40" in md
    view = (out / "view.md").read_text()
    assert view.count("### C2-") == C.N_VIEW and "<1><2>⟦<3>⟧<4><9>" in view and "⟦<5>⟧" in view
    blob = json.loads((out / "x47_3.json").read_text())
    assert blob["models"][0]["clauses"]["a"] is True and out.parent == C.RESULTS


# ---- the run stage on a fake model (CPU) --------------------------------------------------------------------------


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model on the real tokenizer (as tests/test_x45p.py's): each block
    mixes the running mean of the positions so far into every position; an edit acts on a block's output."""

    def __init__(self, tok, n_layers: int = 33, d: int = 32):
        import torch

        g = torch.Generator().manual_seed(0)
        vocab = len(tok)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.device = tok, n_layers, torch.device("cpu")
        self.decoded = ["t"] * vocab
        self.special_ids: frozenset[int] = frozenset()
        self.calls: list[tuple[int, list[dict]]] = []

    def forward(self, ids: list[int], edits: dict):
        import torch

        h = self.emb[torch.as_tensor(ids)]
        states = {}
        for layer in range(self.n_layers):
            h = h + 0.1 * torch.cumsum(h, 0) / torch.arange(1, h.shape[0] + 1)[:, None]
            if layer in edits:
                h = edits[layer](h)
            states[layer] = h.clone()
        return self.unemb @ h[-1], states

    def run(self, ids, edits=None, record=()):
        logits, states = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: states[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        import torch

        self.calls.append((ids.shape[1], edits))
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts

    def letter_token_ids(self):
        return list(range(64))


class FakeLens:
    def __init__(self, model, name):
        assert name == "jpp"

    def vectors(self, layer, ids):
        import torch

        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


def test_run_stage_end_to_end_on_a_fake_model(tok, tmp_path, monkeypatch):
    import torch

    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins
    from scripts import x0_massmean as MM

    fake = FakeModel(tok)
    alf, _ = np.linalg.qr(np.random.default_rng(0).standard_normal((32, 4)))
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(MM, "subspaces", lambda run: ({"Alf": alf}, {}))
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    monkeypatch.setattr(C, "N_GEN", 24)
    monkeypatch.setattr(C, "N_ITEMS", 10)
    # the competence steps answer right (a random fake model cannot): every cue named, every scene eligible
    monkeypatch.setattr(C, "cue_competence", lambda model, prompts: [{**{k: p[k] for k in ("animal", "cue", "person",
                        "template")}, "greedy": p["animal"], "named": p["animal"], "right": True} for p in prompts])  # fmt: skip
    monkeypatch.setattr(C, "competence", lambda model, cases, ws: [{"scene": c["scene"], "reader": w, "variant": v,
                        "greedy": "5", "said": "5", "right": True, "read_right": True, "top": 0} for c in cases
                        for w in X.READERS for v in ("org", "alt")])  # fmt: skip
    out = C.stage_run(f"{pins.RUN_PREFIX}fake_x47_cue")
    m = json.loads((out / "manifest.json").read_text())
    assert m["items"] == 10 and m["layer"] == X.PREDICTED[pins.TARGET] and "sealed" in m and m["rule"] == C.RULE
    assert not any(p.name.startswith(("verdict", "x47_3")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(out / "cases.jsonl")}
    chosen = list(dict.fromkeys(r["scene"] for r in rows))
    assert len(chosen) == 10 and len(rows) == 10 * len(X.READERS) * (1 + len(C.ARMS))
    assert all((r["route"] is None) == (r["reader"] == X.RECALL) for r in rows)
    assert len(X.read_jsonl(out / "decoy.jsonl")) == 10 and len(X.read_jsonl(out / "norms.jsonl")) == 10
    pcf = np.load(out / "pcf.npz")["P"]
    assert pcf.shape == (32, C.RANK) and np.allclose(pcf.T @ pcf, np.eye(C.RANK), atol=1e-5)
    pairs = X.read_jsonl(out / "pcf_pairs.jsonl")
    assert pairs and all(cases[p["scene"]]["half"] == "fit" for p in pairs)
    # the first arm read: the lookup's O (the digit's space appended) under none + every arm; whole = h_S - h_O at the cue
    la = X.PREDICTED[pins.TARGET]
    c = cases[chosen[0]]
    ids = c["readers"][X.LOOKUP]["ids"]
    seq, edits = next((s, e) for s, e in fake.calls if len(e) == 1 + len(C.ARMS))
    assert seq == len(ids["org"]) + len(c["space"]) and edits[0] == {}
    whole = edits[1][la]
    assert whole.positions == [c["pos"]]
    h = {v: fake.run(torch.tensor([ids[v]]), record=(la,))[1][la] for v in ("org", "alt")}
    assert torch.allclose(whole.delta[0], h["alt"][c["pos"]] - h["org"][c["pos"]], atol=1e-5)
    nopcf = edits[1 + C.ARMS.index("no_pcf")][la].delta[0]
    pt = torch.tensor(pcf)
    assert torch.allclose(nopcf @ pt, torch.zeros(C.RANK), atol=1e-4)  # nothing left along U'
    noalf = edits[1 + C.ARMS.index("no_alf")][la].delta[0]
    assert torch.allclose(noalf @ torch.tensor(alf, dtype=torch.float32), torch.zeros(4), atol=1e-4)
    assert not math.isnan(json.loads((out / "pcf_fit.json").read_text())["random_mean_cos2"])
