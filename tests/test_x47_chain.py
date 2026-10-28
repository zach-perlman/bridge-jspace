"""x47_chain (batch 47, test 47.14): the chain scenes, their checks, the fake end-to-end run (sealed), the rule on
planted cells, and the verify-pack view."""

import json
import random
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x47_chain as C

LK, HL = X.LOOKUP, C.HALL
ANIMALS = ["ant", "bee", "cat", "cow", "crow", "duck", "fox", "frog", "goat", "hen", "owl", "pig", "yak", "eel"]
PEOPLE = ["Ann", "Ben", "Cara", "Dan", "Eve", "Finn", "Gus"]
HALLS = ["B", "C", "D", "E", "F", "G", "H", "J"]


# ---- the scenes (texts) ---------------------------------------------------------------------------------------------


def test_scene_text_moves_the_bridge_numbers_hall_sentence():
    rng = random.Random(1)
    for _ in range(50):
        t = C.scene_text(rng, ANIMALS, PEOPLE, HALLS)
        assert C.text_checks(t) == []
        i, j = t["hall_slot"], t["target_slot"]
        assert i != j and t["halls_o"][i] == (t["digit"], t["expect"]["identity"])
        assert t["halls_s"][j] == (t["digit"], t["new"]) and t["halls_s"][i] == t["halls_o"][j]
        assert t["expect"]["position"] == t["halls_o"][j][1] and t["expect"]["value"] == t["new"]
        assert t["o"].index("The locker of") > t["o"].rindex("is in hall")
        assert f"The locker of the {t['bridge']} is {t['digit']}." in t["o"]
        assert t["o"].split(". ")[6:] == t["s"].split(". ")[6:]  # the locker and pick layers are O's


def test_text_checks_catch_leaks():
    t = C.scene_text(random.Random(2), ANIMALS, PEOPLE, HALLS)
    assert C.text_checks(t) == []
    leak = {**t, "o": t["o"].replace(f"hall {t['expect']['position']}.", f"hall {t['new']}.", 1)}
    assert any("new letter" in b for b in C.text_checks(leak))
    swapped = {**t, "s": t["o"]}
    assert any("differ in sentences" in b for b in C.text_checks(swapped))
    after = {**t, "o": " ".join(t["o"].split(". ")[3:4]) + ". " + ". ".join(t["o"].split(". ")[:3]) + ". "
             + ". ".join(t["o"].split(". ")[4:])}  # fmt: skip
    assert C.text_checks(after)


def test_said_letter_reads_a_standalone_capital():
    assert C.said_letter("B") == "B" and C.said_letter(" Hall C.\nmore") == "C" and C.said_letter("hall b") is None
    assert C.said_letter("A") == "A" and C.said_letter("In hall D") == "D" and C.said_letter("BC") is None


# ---- fakes (the tokenizer and the model, as tests/test_x47_six.py) -------------------------------------------------


class WordTok:
    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids, skip_special_tokens=False) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


class FakeModel:
    def __init__(self, tok: WordTok, vocab: int, n_layers: int = 33, d: int = 32):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.n_layers, self.device = tok, n_layers, torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

    def forward(self, ids, edits):
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
        rows = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1)
        logits = torch.stack([self.forward(r.tolist(), e)[0] for r, e in zip(rows, edits, strict=True)])
        texts = [self.tokenizer.decode([int(lg.argmax())]) for lg in logits]
        return (texts, logits) if first_logits else texts


def wrap(ctx: str, question: str, kind: str) -> str:
    return (
        f"<|im_start|>user\n{ctx}\n{question} {'digit' if kind == 'digit' else C.HALL_INSTRUCTION}<|im_end|>\nAnswer:"
    )


def fake_cases(tok: WordTok, n: int) -> list[dict]:
    rng = random.Random(7)
    out = []
    while len(out) < n:
        case, why = C.encode(tok, C.scene_text(rng, ANIMALS, PEOPLE, HALLS), f"H-{len(out) + 1:04d}")
        assert case is not None, why
        out.append(case)
    return out


def test_encode_on_the_word_tokenizer(monkeypatch):
    monkeypatch.setattr(C, "render", lambda tok, ctx, q, kind: wrap(ctx, q, kind))
    tok = WordTok()
    cases = fake_cases(tok, 12)
    for c in cases:
        lk, hl = c["readers"][LK], c["readers"][HL]
        assert lk["kind"] == "digit" and hl["kind"] == "letter" and lk["space"] == [] and hl["space"] == []
        assert tok.decode([lk["ids"]["org"][c["pos"]]]).strip().rstrip(".") == str(c["digit"])
        assert lk["ids"]["org"][c["pos"]] == lk["ids"]["alt"][c["pos"]] and len(lk["ids"]["org"]) == len(
            lk["ids"]["alt"]
        )
        assert hl["ids"]["org"][: c["pos"] + 1] == lk["ids"]["org"][: c["pos"] + 1]
        assert lk["answer"] == lk["cf_answer"] == str(c["digit"]) and hl["cf_answer"] == c["new"]
        assert c["route_tokens"]["value"] == hl["tok_b"] and c["route_tokens"]["identity"] == hl["tok_A"]
        assert len({c["route_tokens"][k] for k in ("identity", "position", "value")}) == 3


def test_split_by_entity_keeps_entities_whole():
    cases = [{"scene": f"s{i}", "bridge": ANIMALS[i % 5]} for i in range(40)]
    fit, test = C.split_by_entity(cases)
    assert len(fit) + len(test) == 40 and abs(len(fit) - len(test)) <= 8
    assert not {c["bridge"] for c in fit} & {c["bridge"] for c in test}


def test_fit_u_recovers_planted_hall_slot_means():
    g = np.random.default_rng(0)
    d, per = 40, 30
    mu = g.normal(size=(3, d)) * 3
    offsets = {"0": g.normal(size=d), "1": g.normal(size=d), "2": g.normal(size=d)}
    h, slots, groups = [], [], []
    for slot in range(3):
        for k in range(per):
            grp = str(k % 3)
            h.append(mu[slot] + offsets[grp] + g.normal(size=d) * 0.05)
            slots.append(slot)
            groups.append(grp)
    h.append(g.normal(size=d))
    slots.append(0)
    groups.append("lonely")
    fit = C.fit_u(np.stack(h), slots, groups)
    assert fit["states"] == 90 and fit["dropped_singletons"] == 1 and fit["U"].shape == (d, 2)
    centred = mu - mu.mean(0)
    for slot in range(3):
        cos = centred[slot] @ fit["mu"][slot] / np.linalg.norm(centred[slot]) / np.linalg.norm(fit["mu"][slot])
        assert cos > 0.99
    proj = fit["U"].T @ centred.T
    assert np.linalg.norm(proj) ** 2 / np.linalg.norm(centred) ** 2 > 0.98


# ---- the run stage on the fake model ---------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    monkeypatch.setattr(C, "render", lambda tok, ctx, q, kind: wrap(ctx, q, kind))
    tok = WordTok()
    for d in range(10):
        tok(str(d))
    cases = fake_cases(tok, 24)
    fake = FakeModel(tok, vocab=len(tok.vocab) + 8)

    def competence(model, cs, ws):
        rows = []
        for k, c in enumerate(cs):
            for w in C.READERS:
                for v in ("org", "alt"):
                    ok = not (k % 6 == 5 and w == HL and v == "alt")  # a few hall answers wrong on S: ineligible
                    rows.append({"scene": c["scene"], "reader": w, "variant": v, "greedy": "", "said": "",
                                 "right": ok, "read_right": ok})  # fmt: skip
        return rows

    g = torch.Generator().manual_seed(3)
    jdic = torch.nn.functional.normalize(torch.randn(40, 32, generator=g), dim=-1)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(C, "competence", competence)
    monkeypatch.setattr(C, "build_cases", lambda tok_, n=C.N_GEN: (cases, {}))
    monkeypatch.setattr(C, "jpp_dictionary", lambda model, layer: jdic)
    monkeypatch.setattr(C, "RESULTS", tmp_path / "x47_chain")
    name = f"{pins.RUN_PREFIX}fake_x47_14"
    return SimpleNamespace(tok=tok, cases=cases, out=C.stage_run(name, "test"), name=name)


def test_run_writes_per_item_outputs_and_no_verdict(fake_run):
    out = fake_run.out
    m = json.loads((out / "manifest.json").read_text())
    assert m["tested"] and m["fit"]["U_rank"] == 2 and m["items"]["chosen"] == 20
    gate = json.loads((out / "gate.json").read_text())
    assert gate["pass"] and gate["eligible"] == 20
    assert not list(out.glob("verdict*")) and not list(out.glob("x47_14*"))  # sealed
    split = json.loads((out / "split.json").read_text())
    assert len(split["fit"]) + len(split["test"]) == 20 and not set(split["fit"]) & set(split["test"])
    cases = {c["scene"]: c for c in fake_run.cases}
    assert not {cases[s]["bridge"] for s in split["fit"]} & {cases[s]["bridge"] for s in split["test"]}
    z = np.load(out / "states.npz")
    assert z["h"].shape == (20, 32) and set(z["half"]) == {"fit", "test"}
    fit = np.load(out / "fit.npz")
    assert fit["mu"].shape == (3, 32) and fit["U"].shape == (32, 2) and len(fit["slot"]) == 2 * len(split["fit"])
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == len(split["test"]) * len(C.READERS) * len(C.ARMS)
    assert {r["arm"] for r in rows} == set(C.ARMS) and {r["scene"] for r in rows} == set(split["test"])
    assert all(r["route"] in C.ROUTES for r in rows if r["reader"] == HL) and all(
        "route" not in r for r in rows if r["reader"] == LK
    )
    norms = X.read_jsonl(out / "norms.jsonl")
    assert len(norms) == len(split["test"]) and all(0 <= r["share_U"] <= 1 + 1e-6 for r in norms)


def test_verdict_pieces_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "9B yes 60%; Muse no 55%")
    res = C.model_result(fake_run.name, n_boot=50)
    assert res["status"] == "tested" and set(res["clauses"]) == {"probe", "layout", "U_cut", "keep_U", "locker_within"}
    assert res["probe"]["n"] == 20 and "layout" in res["probe"] and res["hall"]["n"] == res["locker"]["n"]
    assert isinstance(res["holds"], bool) and isinstance(res["jpp_matters"], bool)
    lines = C.report_lines([res, C.model_result("muse30_x47_14")], "9B yes 60%; Muse no 55%", 50)
    text = "\n".join(lines)
    assert "pending" in text and "## The hall question" in text and "slot probe" in text
    ex = C.examples_lines([fake_run.name], decode=fake_run.tok.decode)
    assert sum(line.startswith("### ") for line in ex) == min(10, res["hall"]["n"]) and any("⟦" in line for line in ex)
    out = C.stage_verdict([fake_run.name], n_boot=50)
    assert (out / "x47_14.md").exists() and (out / "examples.md").exists()


# ---- the rule on planted cells ---------------------------------------------------------------------------------------


def planted(probe: float = 0.9, layout: float = 0.4, cut: float = 0.4, keep: float = 0.3, drift: float = 0.02,
            jpp_cut: float = 0.0, value: float = 0):  # fmt: skip
    hall = {"U_cut_beyond_random": [cut, cut - 0.1, cut + 0.1], "keep_U_position": [keep, keep - 0.1, keep + 0.1],
            "jpp_cut_beyond_random": [jpp_cut, 0, 0], "value_count": {a: value for a in C.ARMS}}  # fmt: skip
    return ({"probe": [probe, 0, 1], "layout": [layout, 0, 1]}, hall, {"max_abs_drift": drift})


def test_rule_holds_only_when_every_clause_does():
    assert C.rule(*planted())["holds"]
    assert C.rule(*planted(probe=0.8, cut=0.3, keep=0.15, drift=0.05, layout=0.6))["holds"]  # at the bars
    for bad in (dict(probe=0.79), dict(layout=0.61), dict(cut=0.29), dict(keep=0.14), dict(drift=0.051)):
        r = C.rule(*planted(**bad))
        assert not r["holds"], bad
    r = C.rule(*planted(jpp_cut=0.3, value=2))
    assert r["jpp_matters"] and r["value_ever"]["whole"] == 2


# ---- sealing ------------------------------------------------------------------------------------------------------


def test_dan_answer_reads_only_q47_14(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = "**Q47.2** x\n\nDan: (a)\n\n**Q47.14** (47.14) y\n\nRule: z.\n\nDan:{}\n\n**Q47.16** w\n\nDan: robust\n"
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format("")))
    assert C.dan_answer() == ""
    monkeypatch.setattr(C.subprocess, "run", fake_git(blocks.format(" 9B yes 60%; Muse yes 55%")))
    assert C.dan_answer() == "9B yes 60%; Muse yes 55%"


def test_verdict_and_examples_refuse_while_sealed(monkeypatch):
    monkeypatch.setattr(C, "dan_answer", lambda rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_verdict(["qwen35_9b_x47_14"])
    with pytest.raises(AssertionError, match="sealed"):
        C.stage_examples(["qwen35_9b_x47_14"])
