"""Batch 48, test 48.2 (scripts/x48_enrich.py): the probe's entity split, the fraction-of-the-way measure on planted
probabilities, the ablation hooks' positions and layers, the controls' module counts, rules A and B on planted
numbers, the sealed verdict, and both run stages end to end on a tiny fake causal model (CPU). No real model."""

import json
import re
from types import SimpleNamespace

import numpy as np
import pytest
import torch
from torch import nn

from scripts import x0_necessity as X
from scripts import x0_probe as PR
from scripts import x48_enrich as E

ORG = ("Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. "
       "Noah picked the tick. Iris picked the frog.")  # fmt: skip
ALT = ORG.replace("Iris picked the frog.", "Iris picked the tick.")
QUESTIONS = {X.LOOKUP: "Which locker belongs to Iris's pick?", X.RECALL: "How many legs does Iris's pick have?"}


def wrap(context: str, question: str) -> str:
    return f"<|im_start|>user\n{context}\n{question}<|im_end|>\nAnswer:"


class WordTok:
    """Words with their leading whitespace as tokens, ids from a shared vocab (copied from tests/test_x45p.py)."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        ids = [self.vocab.setdefault(text[a:b], len(self.vocab)) for a, b in spans]
        return SimpleNamespace(input_ids=ids, offset_mapping=spans if return_offsets_mapping else None)

    def decode(self, ids) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"<{int(i)}>") for i in ids)


# ---- layers, folds, probes, the fraction ----------------------------------------------------------------------------


def test_probe_layers_step_two_and_the_last_block():
    assert E.probe_layers(12, 32) == [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 31]
    assert E.probe_layers(26, 52) == [26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 51]
    assert E.probe_layers(3, 8) == [3, 5, 7]  # the step lands on the last block


def test_entity_folds_hold_whole_entities_and_are_seeded():
    ents = [f"e{i % 13}" for i in range(130)] + ["big"] * 40
    f = E.entity_folds(ents)
    assert len(set(f.values())) == 5 and set(f) == set(ents)
    assert f == E.entity_folds(ents)  # seed 0: deterministic
    assert E.entity_folds(ents, seed=1) != f
    sizes = [sum(f[e] == k for e in ents) for k in range(5)]
    assert max(sizes) - min(sizes) <= 40  # dealt to the smallest fold: the big entity cannot stack on another


def planted(n_ent=20, per=6, d=40, classes=("2", "4", "6", "8"), seed=0, signal=4.0):
    """Entities with one attribute class each; states = noise + signal on the class's own dimension."""
    rng = np.random.default_rng(seed)
    x, y, ents = [], [], []
    for e in range(n_ent):
        c = classes[e % len(classes)]
        for _ in range(per):
            v = rng.normal(size=d)
            v[int(c)] += signal
            x.append(v)
            y.append(c)
            ents.append(f"e{e}")
    return np.array(x), y, ents


def test_ridge_scores_agree_with_x0_probes_ridge():
    x, y, _ = planted()
    classes, sc = E.ridge_scores(x[:80], y[:80], x[80:], 1.0)
    assert classes == sorted(set(y)) and sc.shape == (len(y) - 80, 4)
    assert [classes[j] for j in sc.argmax(1)] == PR.ridge(x[:80], y[:80], x[80:], (1.0,))[0]


def test_probe_reads_a_planted_attribute_across_held_out_entities_and_not_noise():
    x, y, ents = planted()
    fold = [E.entity_folds(ents)[e] for e in ents]
    probe = E.Probe(x, y, fold)
    assert probe.held_out > 0.9 and probe.rel in PR.RELS
    x0, _, _ = planted(signal=0.0, seed=1)
    assert E.Probe(x0, y, fold).held_out < 0.5  # 4 classes: chance 0.25
    classes, sc = probe.scores(x[:3], frozenset({fold[0]}))
    assert sc.shape == (3, 4) and classes[int(sc[0].argmax())] == y[0]


def test_margin_and_fraction_on_planted_probabilities():
    classes = ["2", "4", "8"]
    sc = np.array([[0.1, 0.8, 0.1], [0.7, 0.2, 0.1], [0.4, 0.5, 0.1]])
    m = E.margin(classes, sc, changed="2", original="4")
    assert m.tolist() == pytest.approx([-0.7, 0.5, -0.1])
    assert E.margin(classes, sc, changed="6", original="4").tolist() == pytest.approx([-0.8, -0.2, -0.5])  # unseen: 0
    assert E.fraction(-0.1, -0.7, 0.5) == pytest.approx(0.5)  # half way from O (-0.7) to S (0.5)
    assert E.fraction(0.5, -0.7, 0.5) == 1.0 and E.fraction(-0.7, -0.7, 0.5) == 0.0
    assert E.fraction(0.9, -0.7, 0.5) == 1.0 and E.fraction(-2.0, -0.7, 0.5) == 0.0  # clipped
    assert E.fraction(0.0, 0.5, 0.5) is None and E.fraction(0.0, 0.6, 0.5) is None  # no positive unedited gap


def readings(fracs: dict[str, float], n=40, gap=1.0):
    return [{"scene": f"s{i}", "entity": f"e{i % 8}", "domain": "animals", "position": "bridge", "layer": 16,
             "gap": gap if i % 10 else -0.1, "fraction": {a: v for a, v in fracs.items()}} for i in range(n)]  # fmt: skip


def test_layer_numbers_skip_items_without_a_gap_and_rule_a():
    rows = readings({"whole": 0.9, "no_jpp": 0.1, "no_rand": 0.8})
    num = E.layer_numbers(rows, n_boot=200)
    assert (num["n"], num["n_read"]) == (40, 36) and num["whole"][0] == pytest.approx(0.9)
    assert num["diff"][0] == pytest.approx(0.7) and num["diff"][1] > 0
    assert E.rule_a_layer(num)["holds"]
    assert (
        E.rule_a_layer(E.layer_numbers(readings({"whole": 0.9, "no_jpp": 0.5, "no_rand": 0.8}), n_boot=200))["holds"]
        is False
    )
    assert (
        E.rule_a_layer(E.layer_numbers(readings({"whole": 0.5, "no_jpp": 0.1, "no_rand": 0.8}), n_boot=200))["holds"]
        is False
    )
    assert E.rule_a_layer(E.layer_numbers(readings({"whole": 0.6, "no_jpp": 0.3, "no_rand": 0.6}), n_boot=200))[
        "holds"
    ]  # bars inclusive
    assert (
        E.rule_a_layer(E.layer_numbers(readings({"whole": 0.9, "no_jpp": 0.1, "no_rand": 0.8}, gap=-1.0), n_boot=20))[
            "holds"
        ]
        is False
    )


# ---- design B: layers, modules, hooks, the rule ---------------------------------------------------------------------


def test_layers_b_and_matched_module_counts():
    for layer, n in ((12, 32), (26, 52)):
        late, person, early = (E.layers_b(a, layer, n) for a in ("bridge_late", "person_late", "bridge_early"))
        assert late == person == list(range(layer + 1, n))  # control 1 ablates as many modules as the test arm
        assert early == list(range(0, layer // 2 + 1)) and max(early) <= layer / 2
    assert len(E.layers_b("bridge_late", 12, 32)) == 19 and len(E.layers_b("bridge_early", 12, 32)) == 7


class Block(nn.Module):
    """A decoder block: mixes the running mean of the positions so far into every position, then adds its MLP's
    write; `post_ffn` on request (the Muse shape, where the write is scaled after the MLP)."""

    def __init__(self, d: int, seed: int, post_ffn: bool):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.self_attn = nn.Identity()
        self.mlp = nn.Linear(d, d, bias=False)
        with torch.no_grad():
            self.mlp.weight.copy_(0.05 * torch.randn(d, d, generator=g))
        if post_ffn:
            self.post_feedforward_layernorm = nn.Linear(d, d, bias=False)
            with torch.no_grad():
                self.post_feedforward_layernorm.weight.copy_(torch.eye(d) * 0.5)

    def forward(self, h):  # [B, S, d]
        h = h + 0.1 * torch.cumsum(h, 1) / torch.arange(1, h.shape[1] + 1)[None, :, None]
        w = self.mlp(h)
        if hasattr(self, "post_feedforward_layernorm"):
            w = self.post_feedforward_layernorm(w)
        return h + w


class FakeModel:
    """A tiny causal stand-in for bridge_jspace.model.Model with real blocks (forward hooks fire): an edit acts on a
    block's output [seq, d] at its layer, as Model's hooks do; `record` returns the block outputs."""

    def __init__(self, tok: WordTok, n_layers: int, d: int = 32, vocab: int = 128, post_ffn: bool = False):
        g = torch.Generator().manual_seed(0)
        self.emb, self.unemb = torch.randn(vocab, d, generator=g), torch.randn(vocab, d, generator=g)
        self.tokenizer, self.d = tok, d
        self.layers = nn.ModuleList([Block(d, i, post_ffn) for i in range(n_layers)])
        self.device = torch.device("cpu")
        self.decoded = [f"t{i}" for i in range(vocab)]
        self.special_ids: frozenset[int] = frozenset()

    def block(self, i: int) -> Block:
        b = self.layers[i]
        assert isinstance(b, Block)
        return b

    @torch.no_grad()
    def forward(self, ids: list[int], edits: dict):
        h = self.emb[torch.as_tensor(ids)][None]
        states = {}
        for layer, block in enumerate(self.layers):
            h = block(h)
            if layer in edits:
                h = edits[layer](h[0].float())[None]
            states[layer] = h[0].clone()
        return self.unemb @ h[0, -1], states

    def run(self, ids, edits=None, record=()):
        logits, states = self.forward(ids[0].tolist(), edits or {})
        return logits, {la: states[la] for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
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
        v = torch.randn(len(ids), 32, generator=torch.Generator().manual_seed(layer))
        return v / v.norm(dim=1, keepdim=True)


@pytest.mark.parametrize("post_ffn", [False, True])
def test_mlp_write_module_and_record(post_ffn):
    fake = FakeModel(WordTok(), 6, post_ffn=post_ffn)
    name, mod = E.mlp_write_module(fake.layers[0])
    assert name == ("post_feedforward_layernorm" if post_ffn else "mlp") and mod is getattr(fake.layers[0], name)
    rec = E.mlp_record(fake)
    assert rec["module"] == {name: 6} and rec["mlp_class"] == ["Linear"] and rec["block_kinds"] == {"full_attention": 6}


def test_hooks_record_at_positions_and_ablate_only_there_on_the_prompts_forward():
    fake = FakeModel(WordTok(), 8)
    ids = torch.arange(10)[None]
    store: dict = {}
    with E.mlp_hooks(fake, [2, 5], E.recorder(store, {"bridge": 4, "person": 1}, 10)):
        _, clean = fake.run(ids, record=tuple(range(8)))
    assert sorted(store) == [2, 5] and store[2]["bridge"].shape == (32,)
    mixed = lambda h: h + 0.1 * torch.cumsum(h, 0) / torch.arange(1, h.shape[0] + 1)[:, None]  # noqa: E731
    assert torch.allclose(store[2]["bridge"], fake.block(2).mlp(mixed(clean[1]))[4])  # the write at the bridge
    means = {la: torch.zeros(32) for la in (3, 5)}
    with E.mlp_hooks(fake, [3, 5], E.ablator(means, 4, 10)):
        _, abl = fake.run(ids, record=tuple(range(8)))
    assert torch.allclose(abl[2], clean[2])  # nothing before the first ablated layer
    diff3 = (abl[3] - clean[3]).abs().sum(-1)
    assert diff3[4] > 0 and torch.all(diff3[[p for p in range(10) if p != 4]] == 0)  # layer 3: only the position
    assert torch.allclose(abl[3][4], clean[3][4] - fake.block(3).mlp(mixed(clean[2]))[4])  # the write removed
    assert (abl[4] - clean[4]).abs().sum(-1)[5:].sum() > 0  # later layers mix it onward (causal)
    with E.mlp_hooks(fake, [3, 5], E.ablator(means, 4, 10)):
        _, short = fake.run(ids[:, :6], record=(3,))  # a shorter forward (a decoding step) passes through
    _, short_clean = fake.run(ids[:, :6], record=(3,))
    assert torch.allclose(short[3], short_clean[3])
    assert not fake.block(3).mlp._forward_hooks  # removed on exit


def rights(recall: dict[str, float], lookup: dict[str, float], n=50):
    rows = []
    for i in range(n):
        for w, acc in ((X.RECALL, recall), (X.LOOKUP, lookup)):
            for arm in E.ARMS_B:
                rows.append({"scene": f"s{i}", "entity": f"e{i % 10}", "reader": w, "arm": arm,
                             "right": int(i < round(acc[arm] * n))})  # fmt: skip
    return rows


def numbers_from(rows):
    out = {}
    for w in X.READERS:
        ents, right = E.accuracy_table(rows, w)
        out[E.READER_NAME[w]] = E.numbers_b(right, ents, n_boot=200)
    return out


def test_rule_b_on_planted_accuracies():
    good = {"none": 1.0, "bridge_late": 0.5, "person_late": 0.96, "bridge_early": 0.92}
    flat = {"none": 0.96, "bridge_late": 0.9, "person_late": 0.92, "bridge_early": 0.96}
    nb = numbers_from(rights(good, flat))
    assert nb["recall"]["drop"]["bridge_late"][0] == pytest.approx(0.5) and nb["lookup"]["drop"]["bridge_late"][
        0
    ] == pytest.approx(0.06)
    assert E.rule_b(nb["recall"], nb["lookup"])["holds"]
    survives = numbers_from(rights({**good, "bridge_late": 0.7}, flat))
    r = E.rule_b(survives["recall"], survives["lookup"])
    assert not r["holds"] and "survives" in r["why"]
    broken = numbers_from(rights(good, {**flat, "bridge_late": 0.7}))  # the lookup falls too: the input is broken
    assert not E.rule_b(broken["recall"], broken["lookup"])["holds"]
    ctl = numbers_from(rights({**good, "person_late": 0.8}, flat))
    assert not E.rule_b(ctl["recall"], ctl["lookup"])["holds"]
    exact = numbers_from(rights({**good, "bridge_late": 0.6, "bridge_early": 0.9}, flat))
    assert E.rule_b(exact["recall"], exact["lookup"])["holds"]  # bars inclusive


def test_batch_label():
    t = lambda h: {"status": "tested", "holds": h}  # noqa: E731
    p = {"status": "pending", "holds": False}
    assert E.batch_label([t(True), t(True)]) == "holds"
    assert E.batch_label([t(True), p]) == "pending"
    assert E.batch_label([t(False), p]) == "does not hold"


# ---- positions (tokenizer only) --------------------------------------------------------------------------------------


def case_record(tok: WordTok, i: int, label="4", cf_label="8") -> dict:
    """One case as X0's scene_case builds it (fake tokenizer), both readers; the bridge 'frog' one token."""
    readers = {}
    for w, q in QUESTIONS.items():
        t_o, t_s = wrap(ORG, q), wrap(ALT, q)
        enc, enc_s = tok(t_o, return_offsets_mapping=True), tok(t_s, return_offsets_mapping=True)
        pos = next(j for j, (a, b) in enumerate(enc.offset_mapping) if t_o[a:b] == " frog.")
        digit = {d: tok(d).input_ids[0] for d in "0123456789"}
        a, b = ("5", "2") if w == X.LOOKUP else (label, cf_label)
        readers[w] = {"id": f"{w}-{i}", "question": q, "answer": a, "cf_answer": b, "tok_A": digit[a], "tok_b": digit[b],
                      "ids": {"org": enc.input_ids, "alt": enc_s.input_ids}, "text": {"org": t_o}, "offsets": enc.offset_mapping}  # fmt: skip
    return {"scene": f"s{i:03d}", "rendering": "chat", "domain": "animals", "bridge": "frog", "cf_bridge": "tick",
            "context": ORG, "cf_context": ALT, "pos": pos, "upstream": False,
            "space": [tok.vocab.setdefault(" ", len(tok.vocab))],
            "readers": readers, "label": label}  # fmt: skip


def test_person_position_is_the_asked_persons_token_before_the_bridge():
    tok = WordTok()
    c = case_record(tok, 0)
    rd = c["readers"][X.LOOKUP]
    p = E.person_position(tok, rd["text"]["org"], ORG, c, rd["offsets"])
    assert p["person"] == "Iris" and p["sentence"] == "Iris picked the frog."
    assert tok.decode([rd["ids"]["org"][p["pos"]]]) == " Iris" and p["tokens"] == [p["pos"]] and p["pos"] < c["pos"]
    assert rd["text"]["org"][slice(*p["span"])] == "Iris"


def test_marked_prompt():
    assert (
        E.marked("Iris picked the frog.", [(0, 4, "person"), (15, 20, "bridge")])
        == "⟦person:Iris⟧ picked the ⟦bridge:frog⟧."
    )


def test_select_on_the_targets_main_run():
    from bridge_jspace import pins
    from scripts import x45m

    run = E.MAIN_RUN.get(pins.TARGET)
    if run is None or not (X.RESULTS / run / "outcomes.jsonl").exists():
        pytest.skip("no main-test run of the target here")
    try:
        tok = x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")
    items, cases, counts = E.select(tok, run, X.PREDICTED[pins.TARGET])
    assert counts["items"] == len(items) == 200 and len(cases) >= len(items)
    scenes = {c["scene"] for c in cases}
    for it in items:
        assert it["scene"] in scenes and it["label"] != it["cf_label"]
        assert it["person"]["pos"] < it["pos"] and it["stored"]["whole"].keys() == set(X.READERS)
        assert (
            tok.decode([it["readers"][X.LOOKUP]["ids"]["org"][it["person"]["pos"]]]).strip() in it["person"]["person"]
        )
    assert set(counts["training_scenes"]) == {"animals", "elements", "greek"}
    assert counts["training_scenes"]["animals"]["classes"] == ["2", "4", "6", "8"]


# ---- the run stages on the fake model --------------------------------------------------------------------------------


def item_record(tok: WordTok, i: int, label: str, cf_label: str, entity: str) -> dict:
    c = case_record(tok, i, label, cf_label)
    rd = c["readers"][X.LOOKUP]
    person = E.person_position(tok, rd["text"]["org"], ORG, c, rd["offsets"])
    return {"scene": c["scene"], "entity": entity, "cf_entity": "tick", "domain": "animals", "upstream": False,
            "pos": c["pos"], "space": c["space"], "read_suffix": " ", "context": ORG, "cf_context": ALT, "label": label,
            "cf_label": cf_label, "person": person,
            "marks": {"bridge": [list(rd["offsets"][c["pos"]])], "person": [list(rd["offsets"][p]) for p in person["tokens"]]},
            "readers": {w: {k: v for k, v in c["readers"][w].items() if k != "offsets"} for w in X.READERS},
            "stored": {"whole": {w: 1 for w in X.READERS}, "no_jpp": {w: 0 for w in X.READERS}}}  # fmt: skip


PLAN = {"items": 12, "entities": 6, "domains": {"animals": 12}, "person_tokens": {"1": 12},
        "training_scenes": {"animals": {"scenes": 12, "entities": 6, "classes": ["4", "8"]}}}  # fmt: skip


@pytest.fixture
def fake_env(tmp_path, monkeypatch):
    from bridge_jspace import lens as L
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = WordTok()
    labels = [("4", "8"), ("8", "4")]
    items = [item_record(tok, i, *labels[i % 2], f"e{i % 6}") for i in range(12)]
    cases = [{**{k: v for k, v in case_record(tok, i, *labels[i % 2]).items() if k != "readers"},
              "bridge": f"e{i % 6}", "readers": {w: {k: v for k, v in case_record(tok, i, *labels[i % 2])["readers"][w].items()
                                                 if k != "offsets"} for w in X.READERS}} for i in range(12)]  # fmt: skip
    fake = FakeModel(tok, pins.N_LAYERS)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(L, "JLens", FakeLens)
    monkeypatch.setattr(E, "select", lambda *_: (items, cases, dict(PLAN)))
    monkeypatch.setattr(E, "MAIN_RUN", {pins.TARGET: "fake_main"})
    monkeypatch.setattr(E, "RUNS_A", {pins.TARGET: f"{pins.RUN_PREFIX}fake_a"})
    monkeypatch.setattr(E, "RUNS_B", {pins.TARGET: f"{pins.RUN_PREFIX}fake_b"})
    monkeypatch.setattr(E, "RESULTS", tmp_path / "x48_enrich")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(E, "SPEC", tmp_path / "batch48.yaml")
    E.SPEC.write_text("")
    src = tmp_path / "x0" / "fake_main"
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    return SimpleNamespace(tok=tok, items=items, cases=cases, fake=fake, pins=pins)


def test_run_a_end_to_end_on_the_fake_model(fake_env):
    from scripts import statement_positions as SP

    env = fake_env
    out = E.stage_run_a(f"{env.pins.RUN_PREFIX}fake_a", "test")
    assert not any(p.name.startswith("x48_2-") for p in out.iterdir())  # sealed: no verdict in the run
    m = json.loads((out / "manifest.json").read_text())
    la = X.PREDICTED[env.pins.TARGET]
    layers = E.probe_layers(la, env.pins.N_LAYERS)
    assert m["layer"] == la and m["probe_layers"] == layers and m["k"] == 25 and "sealed" in m
    zt, zm = np.load(out / "states_train.npz"), np.load(out / "states_main.npz")
    assert zt["h"].shape == (12, len(layers), 2, 32) and zm["h"].shape == (12, len(E.ARMS_A), len(layers), 2, 32)
    rows = X.read_jsonl(out / "reads.jsonl")
    assert len(rows) == 12 * len(X.READERS) * len(E.ARMS_A)
    # the states: O's and S's unedited states at the bridge token and at the last token (the appended space)
    it = env.items[0]
    rc = it["readers"][X.RECALL]
    h = {v: env.fake.run(torch.tensor([rc["ids"][v] + it["space"]]), record=tuple(layers))[1] for v in ("org", "alt")}
    li = layers.index(la)
    for a, v in (("none", "org"), ("alt", "alt")):
        ai = E.ARMS_A.index(a)
        assert np.allclose(zm["h"][0, ai, li, 0], h[v][la][it["pos"]].numpy(), atol=2e-2)
        assert np.allclose(zm["h"][0, ai, li, 1], h[v][la][-1].numpy(), atol=2e-2)
    assert np.allclose(zt["h"][0, li, 0], h["org"][la][it["pos"]].numpy(), atol=2e-2)
    # the arms: whole = h_S - h_O at L; no_jpp = minus its J++ part; no_rand = minus a random part of the same share
    whole = (h["alt"][la][it["pos"]] - h["org"][la][it["pos"]])[None]
    jdic = FakeLens(None, "jpp").vectors(la, list(range(64)))
    part = X.fit(jdic, whole, 25, "signed")
    assert np.allclose(zm["h"][0, E.ARMS_A.index("whole"), li, 0], h["alt"][la][it["pos"]].numpy(), atol=2e-2)
    got = torch.tensor(zm["h"][0, E.ARMS_A.index("no_jpp"), li, 0].astype(np.float32))
    assert torch.allclose(got, (h["org"][la][it["pos"]] + whole[0] - part[0]), atol=2e-2)
    basis = SP.random_basis(32, torch.Generator().manual_seed(X.SUBSPACE_SEED + la))
    share = part.norm(dim=-1) ** 2 / whole.norm(dim=-1) ** 2
    rand = SP.random_subspace_part(whole, share, basis)
    got = torch.tensor(zm["h"][0, E.ARMS_A.index("no_rand"), li, 0].astype(np.float32))
    assert torch.allclose(got, h["org"][la][it["pos"]] + whole[0] - rand[0], atol=2e-2)
    norms = X.read_jsonl(out / "norms.jsonl")
    assert norms[0]["jpp_share"] == pytest.approx(float(share[0]), abs=1e-4)
    # the probes ran (CPU) and chose a branch; readings for both positions, every layer, arm and item
    probe = json.loads((out / "probe.json").read_text())
    assert probe["branch"] in ("bridge", "last") and probe["rule_domain"] == "animals"
    acc = probe["accuracy"]
    assert {(r["position"], r["layer"]) for r in acc} == {(p, la_) for p in E.POSITIONS for la_ in layers}
    assert all(r["chance"] == 0.5 and r["entities"] == 6 and not r["one_entity_per_class"] for r in acc)
    rd = X.read_jsonl(out / "readings.jsonl")
    assert len(rd) == 12 * 2 * len(layers) and set(rd[0]["fraction"]) == set(E.EDIT_ARMS)
    assert all(r["held_out_folds"] and len(r["held_out_folds"]) <= 2 for r in rd)
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == X.K_EXAMPLES * len(X.READERS) * len(E.EDIT_ARMS)


def test_analyse_a_on_planted_states_reads_the_attribute_and_the_arms(fake_env, monkeypatch):
    """Planted states: the attribute class on its own dimension; O at the original's class, S at the changed one;
    whole and no_rand move all the way, no_jpp not at all -> the bridge branch, readable layers, rule A holds."""
    env = fake_env
    name = f"{env.pins.RUN_PREFIX}fake_a"
    out = E.RESULTS / name
    out.mkdir(parents=True)
    layers = [20, 24, 28]
    monkeypatch.setattr(E, "probe_layers", lambda *_: layers)
    rng = np.random.default_rng(0)
    d = 32

    def state(label: str) -> np.ndarray:
        v = rng.normal(size=d)
        v[int(label)] += 5.0
        return v

    n_train = 60
    # 30 entities, 10 per class, 2 items each: holding two folds out never removes a whole class
    train = [{"scene": f"t{i}", "entity": f"e{i % 30}", "domain": "animals", "label": ("4", "8", "2")[i % 3], "pos": 5}
             for i in range(n_train)]  # fmt: skip
    ht = np.zeros((n_train, len(layers), 2, d))
    for i, t in enumerate(train):
        for li in range(len(layers)):
            ht[i, li, 0] = state(t["label"])
            ht[i, li, 1] = rng.normal(size=d)  # the last token carries nothing: the bridge branch must be chosen
    items = []
    hm = np.zeros((12, len(E.ARMS_A), len(layers), 2, d))
    for k in range(12):  # the main items are training scenes; the changed item's entity holds the changed class
        it = dict(env.items[k], scene=train[k]["scene"], entity=train[k]["entity"], cf_entity=train[k + 1]["entity"],
                  label=train[k]["label"], cf_label=train[k + 1]["label"])  # fmt: skip
        items.append(it)
        for li in range(len(layers)):
            o, s = state(it["label"]), state(it["cf_label"])
            for a, v in (("none", o), ("alt", s), ("whole", s), ("no_jpp", o), ("no_rand", s)):
                hm[k, E.ARMS_A.index(a), li, 0] = v
                hm[k, E.ARMS_A.index(a), li, 1] = rng.normal(size=d)
    (out / "manifest.json").write_text(
        json.dumps({"layer": 16, "probe_layers": layers, "model": {"target": env.pins.TARGET}})
    )
    np.savez_compressed(out / "states_train.npz", h=ht.astype(np.float16), scene=np.array([t["scene"] for t in train]),
                        layers=np.array(layers))  # fmt: skip
    np.savez_compressed(out / "states_main.npz", h=hm.astype(np.float16), scene=np.array([it["scene"] for it in items]),
                        arms=np.array(E.ARMS_A), layers=np.array(layers))  # fmt: skip
    X.write_jsonl(out / "training.jsonl", train)
    X.write_jsonl(out / "cases.jsonl", items)
    (out / "plan.json").write_text(json.dumps(PLAN))
    X.write_jsonl(out / "reads.jsonl", [{"scene": it["scene"], "reader": w, "arm": a, "switched": int(a != "none")}
                                        for it in items for w in X.READERS for a in E.ARMS_A])  # fmt: skip
    E.analyse_a(name)
    probe = json.loads((out / "probe.json").read_text())
    assert (
        probe["branch"] == "bridge"
        and probe["readable_layers"]["bridge"] == layers
        and probe["readable_layers"]["last"] == []
    )
    assert all(r["held_out"] > 0.9 for r in probe["accuracy"] if r["position"] == "bridge")
    rd = [r for r in X.read_jsonl(out / "readings.jsonl") if r["position"] == "bridge"]
    assert all(r["gap"] > 0 for r in rd)
    assert all(
        r["fraction"]["whole"] > 0.9 and r["fraction"]["no_rand"] > 0.9 and r["fraction"]["no_jpp"] < 0.1 for r in rd
    )
    assert all(probe["folds"][r["entity"]] in r["held_out_folds"] for r in rd)  # the original's fold is held out
    res = E.model_result_a(name, n_boot=200)
    assert res["branch"] == "bridge" and res["layers_in_rule"] == [20, 24, 28] and res["holds"]
    assert res["label"] == "J++ keys the enrichment at the bridge token"
    assert res["checks"]["recall whole vs the main run's stored"]["agree"] == 12


def test_run_b_end_to_end_on_the_fake_model(fake_env):
    env = fake_env
    out = E.stage_run_b(f"{env.pins.RUN_PREFIX}fake_b", "test")
    m = json.loads((out / "manifest.json").read_text())
    la, n = X.PREDICTED[env.pins.TARGET], env.pins.N_LAYERS
    assert m["arm_layers"]["bridge_late"] == m["arm_layers"]["person_late"] == list(range(la + 1, n))
    assert m["module_counts"] == {"bridge_late": n - la - 1, "person_late": n - la - 1, "bridge_early": la // 2 + 1}
    assert m["hooked"]["module"] == {"mlp": n} and "sealed" in m
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert {(r["scene"], r["reader"], r["arm"]) for r in rows} == {
        (it["scene"], w, a) for it in env.items for w in X.READERS for a in E.ARMS_B
    }
    means = torch.load(out / "means.pt")
    assert sorted(means["means"]) == list(range(n)) and means["n"] == 12
    # the mean at the bridge: the average MLP write at the bridge token over the items' O prompts
    it = env.items[0]
    writes = []
    for it_ in env.items:
        ids = torch.tensor([it_["readers"][X.LOOKUP]["ids"]["org"] + it_["space"]])
        store: dict = {}
        with E.mlp_hooks(env.fake, [la + 1], E.recorder(store, {"bridge": it_["pos"]}, ids.shape[1])):
            env.fake.run(ids)
        writes.append(store[la + 1]["bridge"])
    assert torch.allclose(means["means"][la + 1]["bridge"], torch.stack(writes).mean(0), atol=1e-5)
    # the none arm is the unedited read; the ablated arms differ from it (the fake's writes are not all equal)
    by = {(r["reader"], r["arm"]): r for r in rows if r["scene"] == it["scene"]}
    ids = torch.tensor([it["readers"][X.RECALL]["ids"]["org"] + it["space"]])
    logits, _ = env.fake.run(ids)
    assert by[(X.RECALL, "none")]["top"] == int(logits.argmax())
    assert len(X.read_jsonl(out / "examples_greedy.jsonl")) == X.K_EXAMPLES * len(X.READERS) * len(E.ARMS_B)
    res = E.model_result_b(out.name, n_boot=100)
    assert (
        res["status"] == "tested"
        and res["readers"]["recall"]["n"] == 12
        and set(res["module_counts"]) == set(E.ARMS_B[1:])
    )


def test_verdict_is_sealed_until_dans_answer(fake_env, monkeypatch):
    monkeypatch.setattr(E, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        E.stage_verdict([], [], n_boot=50)


def test_dan_answer_reads_only_the_q48_2_block(monkeypatch):
    import subprocess

    text = ("**Q48.1** (48.1)\n- (a) yes / no\n\nDan: yes · 70%\n\n**Q48.2** (48.2 A, B)\n- A: ...\n\nDan:\n\n"
            "**Q48.3** (48.3)\n\nDan: no · 60%\n")  # fmt: skip
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=text))
    assert E.dan_answer() == ""
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(stdout=text.replace("Dan:\n\n**Q48.3", "Dan: bridge · 60%\n\n**Q48.3")),
    )
    assert E.dan_answer() == "bridge · 60%"


def test_verdict_stage_on_the_fake_runs(fake_env, monkeypatch):
    env = fake_env
    a = E.stage_run_a(f"{env.pins.RUN_PREFIX}fake_a", "test")
    b = E.stage_run_b(f"{env.pins.RUN_PREFIX}fake_b", "test")
    monkeypatch.setattr(E, "dan_answer", lambda: "bridge · 60%; B yes · 60%")
    out = E.stage_verdict([a.name], [b.name], n_boot=50)
    blob = json.loads((out / "x48_2.json").read_text())
    assert blob["dan"].startswith("bridge") and out.parent == E.RESULTS
    assert blob["A"][0]["status"] == "tested" and blob["B"][0]["status"] == "tested"
    assert blob["verdict"]["A"] in ("holds", "does not hold") and blob["verdict"]["B"] in ("holds", "does not hold")
    md = (out / "x48_2.md").read_text()
    assert "Design A" in md and "Design B" in md and "UNVERIFIED" in md
    ex = (out / "examples.md").read_text()
    # the fake tokenizer's bridge token is " frog." (the period inside); the real one's is the word alone
    assert ex.count("⟦bridge:frog") == X.K_EXAMPLES * (1 + len(X.READERS)) and "⟦person:Iris⟧" in ex


def test_verdict_with_missing_runs_is_pending(fake_env, monkeypatch):
    env = fake_env
    monkeypatch.setattr(E, "dan_answer", lambda: "x")
    out = E.stage_verdict([], [], n_boot=50)
    blob = json.loads((out / "x48_2.json").read_text())
    assert blob["verdict"] == {"A": "pending", "B": "pending"}
    assert blob["A"][0]["run"] == f"({env.pins.RUN_PREFIX}fake_a)" and blob["A"][0]["status"] == "pending"
