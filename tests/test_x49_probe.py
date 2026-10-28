"""Batch 49, test 49.3 (scripts/x49_probe.py): the locker sentence's token set and keys (a fake tokenizer; the target's
cached tokenizer), the run stage on a fake causal model (every token's state at L // 2 and L, the sentence mean), the
binary label and the probes on planted states (a person mark spread over the tokens is read pooled, not per token; a
picked-flag is read by (ii) and not (i); nothing before the pick), the rule on planted numbers, the seal, and the
verdict and view on the fake run. No real model."""

from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x49_probe as P
from tests import test_x48_bind as TB

# ---- token sets and keys --------------------------------------------------------------------------------------------


def test_token_keys_name_every_word_of_the_sentence():
    tok = TB.WordTok()
    text = "x. The locker of the frog is 5. Iris"
    enc = tok(text, return_offsets_mapping=True)
    start = text.index("The locker")
    sent = "The locker of the frog is 5."
    pos = [j for j, (a, b) in enumerate(enc.offset_mapping) if a < start + len(sent) and b > start]
    keys = P.token_keys(enc.offset_mapping, pos, start, sent)
    assert keys == ["w:The", "w:locker", "w:of", "w:the", "item", "w:is", "number", "w:."]
    assert [text[slice(*enc.offset_mapping[p])].strip() for p in pos] == ["The", "locker", "of", "the", "frog", "is",
                                                                          "5", "."]  # fmt: skip
    # a two-token item: its earlier token is item_pre; no article: no w:the
    text = "The locker of sea lion is seven."
    enc = tok(text, return_offsets_mapping=True)
    keys = P.token_keys(enc.offset_mapping, list(range(len(enc.input_ids))), 0, text)
    assert keys == ["w:The", "w:locker", "w:of", "item_pre", "item", "w:is", "number", "w:."]
    with pytest.raises(AssertionError, match="not a locker sentence"):
        P.token_keys(enc.offset_mapping, [0], 0, "Iris picked the frog.")


def test_token_keys_on_the_targets_tokenizer():
    from scripts import statement_positions as SP

    try:
        tok = SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")
    for sent, item, number in (("The locker of the frog is 5.", " frog", "5"),
                               ("The locker of hydrogen is nine.", " hydrogen", " nine")):  # fmt: skip
        text = f"Iris picked the frog. {sent}\nWhich locker?"
        enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
        start = text.index(sent)
        pos = SP.tokens_in(enc["offset_mapping"], start, start + len(sent))
        keys = P.token_keys(enc["offset_mapping"], pos, start, sent)
        got = {k: tok.decode([enc["input_ids"][p]]) for k, p in zip(keys, pos, strict=True)}
        assert got["item"] == item and got["number"].strip() == number.strip() and got["w:locker"] == " locker"
        assert keys[0] == "w:The" and keys[-1] == "w:." and len(set(keys)) == len(keys)
        assert "".join(got.values()).strip() == sent  # every token of the sentence, nothing else


# ---- fake clean-design scenes ----------------------------------------------------------------------------------------

ITEMS = TB.ITEMS


def fake_scene(i: int, after: bool) -> tuple[str, dict, str, str, str]:
    """A 45m-like scene i: the asked person picks the bridge; two others pick an item each; the added item (the cf
    bridge) has a locker sentence and no picker. Locker-after: the bridge's and the added item's lockers follow the
    asked pick; locker-first: both precede it."""
    a, j, p = TB.NAMES[i % 6], TB.NAMES[(i + 1) % 6], TB.NAMES[(i + 2) % 6]
    bridge, other, third, cf = ITEMS[i % 8], ITEMS[(i + 3) % 8], ITEMS[(i + 5) % 8], ITEMS[(i + 6) % 8]
    if after:
        ctx = (f"The locker of the {third} is 1. {p} picked the {third}. {a} picked the {bridge}. The locker of the "
               f"{bridge} is 5. {j} picked the {other}. The locker of the {other} is 2. The locker of the {cf} is 7.")  # fmt: skip
    else:
        ctx = (f"The locker of the {bridge} is 5. The locker of the {cf} is 7. {p} picked the {third}. The locker of the "
               f"{third} is 1. {a} picked the {bridge}. {j} picked the {other}. The locker of the {other} is 2.")  # fmt: skip
    facts = {"pick": {p: third, a: bridge, j: other}, "locker": {third: 1, bridge: 5, other: 2, cf: 7}}
    return ctx, facts, bridge, a, cf


def fake_items(tok, n: int = 24) -> list[dict]:
    from scripts import tasks_v2 as T

    items = []
    for i in range(n):
        ctx, facts, bridge, asked, cf = fake_scene(i, after=i % 2 == 0)
        case, by_id = TB.fake_case(tok, ctx, f"s{i:03d}", bridge, asked, cf)
        for w in case["readers"]:
            by_id[f"{w}-s{i:03d}"]["scene_facts"] = facts
            case["readers"][w]["answer"] = "5" if w == "PP" else str(T.DOMAINS["animals"].values[bridge])
        it = P.W.scene_item(tok, case, "45m", by_id)
        for s, t in zip(it["sentences"], P.scene_tokens(tok, it), strict=True):
            s["tokens"] = t
        items.append(it)
    return items


def test_fake_scenes_have_both_groups_and_the_sentence_tokens(render_fake):
    tok = TB.WordTok()
    items = fake_items(tok, 4)
    assert [it["group"] for it in items] == ["after", "before", "after", "before"]
    rows = P.probe_rows(items)
    assert len(rows) == 4 * 3  # the added item has no picker: no row
    mine = [r for r in rows if r["asked"]]
    assert [r["stratum"] for r in mine] == ["after", "before", "after", "before"]
    assert all(r["picker"] == r["asked_person"] for r in mine) and all(len(r["scene_items"]) == 4 for r in rows)
    it = items[0]
    ids = it["readers"]["PP"]["ids"]["org"]
    s = next(s for s in it["sentences"] if s["asked"])
    assert tok.decode([ids[p] for p in s["tokens"]["positions"]]).strip() == s["sentence"]
    assert s["tokens"]["keys"] == ["w:The", "w:locker", "w:of", "w:the", "item", "w:is", "number", "w:."]
    assert "⟦item: " + it["entity"] + "⟧" in P.keyed_prompt(tok, it) and "⟦bridge:" in P.keyed_prompt(tok, it)
    assert P.rule_keys(rows) == sorted(s["tokens"]["keys"])


@pytest.fixture
def render_fake(monkeypatch):
    monkeypatch.setattr(P.W.X, "render", lambda tok, item, rendering, context: TB.wrap(context, item["question"]))


# ---- the binary label, the probes on planted states -----------------------------------------------------------------


def planted(n_scenes: int, mark: str, d: int = 16, seed: int = 0, n_tok: int = 8, noise: float = 1.0,
            signal: float = 1.0) -> tuple[list[dict], dict[str, np.ndarray]]:  # fmt: skip
    """Probe rows of planted scenes (3 pickers of 9 names, items of 12; half the scenes locker-after) and per-row token
    states [n_tok, d]. mark 'person': in the after stratum every token carries the picker's name vector plus noise;
    'flag': the asked person's sentence carries one flag vector; before-stratum rows are noise alone."""
    rng = np.random.default_rng(seed)
    names = [f"N{i}" for i in range(9)]
    vec = {n: rng.normal(size=d) * signal for n in names}
    flag = rng.normal(size=d) * 3
    rows, toks = [], []
    for s in range(n_scenes):
        people = [names[j] for j in rng.choice(9, 3, replace=False)]
        group = "after" if s % 2 == 0 else "before"
        items = [f"it{(s * 3 + k) % 12}" for k in range(3)]
        for k, who in enumerate(people):
            stratum = group if k == 0 else ("after" if (s + k) % 2 == 0 else "before")
            rows.append({"item": s, "scene": f"s{s}", "entity": items[0], "domain": "animals", "group": group, "k": k,
                         "locker_item": items[k], "picker": who, "stratum": stratum, "asked": k == 0,
                         "asked_person": people[0], "names": people, "scene_items": items,
                         "keys": [f"w:{t}" for t in range(n_tok)]})  # fmt: skip
            base = np.zeros(d)
            if stratum == "after":
                base = vec[who] if mark == "person" else flag * (k == 0)
            toks.append(base + rng.normal(size=(n_tok, d)) * noise)
    return rows, {"tokens": np.stack(toks)}


def test_the_binary_label_is_the_asked_persons_sentence():
    rows, _ = planted(6, "person")
    y, cands, groups = P.labels_of(rows, "asked")
    assert y == ["yes" if r["picker"] == r["asked_person"] else "no" for r in rows] and y.count("yes") == 6
    assert cands[0] == ["no", "yes"] and groups == [r["locker_item"] for r in rows]
    y, cands, groups = P.labels_of(rows, "identity")
    assert y == [r["locker_item"] for r in rows] and groups == [r["picker"] for r in rows]  # the person held out


def test_balanced_accuracy_and_its_interval():
    b = P.balanced([1, 1, 1, 0, 1, 0], [True, True, False, False, False, False], ["a", "b", "c", "a", "b", "c"], 200)
    assert b["balanced"][0] == pytest.approx((1.0 + 0.5) / 2) and b["pos"][0] == 1.0 and b["neg"][0] == 0.5
    assert b["balanced"][1] <= b["balanced"][0] <= b["balanced"][2] and b["n_pos"] == 2
    assert np.isnan(P.balanced([1, 1], [True, True], ["a", "b"], 50)["balanced"][0])  # one class: no score


def test_a_spread_person_mark_is_read_pooled_not_per_token():
    rows, z = planted(160, "person", noise=2.5, signal=1.0)
    pooled = P.probe_view(z["tokens"].mean(1), rows, "picker", n_boot=100)
    token = P.probe_view(z["tokens"][:, 0], rows, "picker", n_boot=100)
    assert pooled["after"]["accuracy"][0] >= 0.85 > token["after"]["accuracy"][0] + 0.2
    assert pooled["before"]["accuracy"][0] <= 0.5  # nothing before the pick
    assert pooled["after"]["n"] == 80 and pooled["after_others"]["n"] > 0
    flag = P.probe_view(z["tokens"].mean(1), rows, "asked", n_boot=100)
    assert flag["after"]["accuracy"][0] <= 0.65  # a person, not the asked one


def test_a_picked_flag_is_read_by_the_binary_probe_not_the_picker():
    rows, z = planted(160, "flag")
    flag = P.probe_view(z["tokens"].mean(1), rows, "asked", n_boot=100)
    assert flag["after"]["accuracy"][0] >= 0.9 and flag["after"]["n_pos"] == 80
    assert flag["before"]["accuracy"][0] <= 0.65
    pick = P.probe_view(z["tokens"].mean(1), rows, "picker", n_boot=100)
    assert pick["after"]["accuracy"][0] <= 0.5
    ident = P.probe_view(z["tokens"].mean(1), rows, "identity", n_boot=100)
    assert ident["chance"] == pytest.approx(1 / 3)  # three items per planted scene (four on the clean design)


# ---- the rule on planted numbers ------------------------------------------------------------------------------------


def res(i_pool, i_tok, ii_pool, ii_tok, ctrl=(0.33, 0.5)) -> dict:
    """A layer result with the given points: (i) pooled and per token key (k0, k1), (ii) likewise; the locker-first
    control at ctrl."""

    def c(after, before):
        return {"after": {"accuracy": [after, 0, 1]}, "before": {"accuracy": [before, 0, 1]}}

    return {"probes": {"picker": {P.POOLED: c(i_pool, ctrl[0]), **{f"k{j}": c(v, ctrl[0]) for j, v in enumerate(i_tok)}},
                       "asked": {P.POOLED: c(ii_pool, ctrl[1]), **{f"k{j}": c(v, ctrl[1]) for j, v in enumerate(ii_tok)}}}}  # fmt: skip


KEYS = ["k0", "k1"]


def test_rule_distributed_flag_neither_between():
    assert P.rule(res(0.85, [0.6, 0.4], 0.5, [0.5, 0.5]), KEYS)["label"] == "distributed"  # inclusive bars
    assert P.rule(res(0.9, [0.61, 0.4], 0.5, [0.5, 0.5]), KEYS)["label"] == "between"  # one token too high
    assert P.rule(res(0.84, [0.4, 0.4], 0.5, [0.5, 0.5]), KEYS)["label"] == "between"
    assert P.rule(res(0.4, [0.4, 0.5], 0.6, [0.85, 0.5]), KEYS)["label"] == "flag"  # at some token
    assert P.rule(res(0.4, [0.4, 0.4], 0.86, [0.5, 0.5]), KEYS)["label"] == "flag"  # pooled
    assert P.rule(res(0.51, [0.4, 0.4], 0.9, [0.5, 0.5]), KEYS)["label"] == "between"  # (i) above 0.5
    assert P.rule(res(0.43, [0.35, 0.3], 0.6, [0.55, 0.5]), KEYS)["label"] == "neither"  # within chance + 0.10
    assert P.rule(res(0.45, [0.35, 0.3], 0.6, [0.55, 0.5]), KEYS)["label"] == "between"
    # the locker-first control above chance: a positive label is not interpretable; neither stays neither
    r = P.rule(res(0.9, [0.4, 0.4], 0.5, [0.5, 0.5], ctrl=(0.5, 0.5)), KEYS)
    assert r["label"] == "uninterpretable" and r["raw"] == "distributed" and not r["control_ok"]
    assert P.rule(res(0.4, [0.4, 0.4], 0.5, [0.5, 0.5], ctrl=(0.33, 0.7)), KEYS)["label"] == "neither"
    # pooled only (the per-token states not here): no 'distributed'
    assert P.rule(res(0.9, [], 0.5, []), KEYS)["label"] == "between"


def test_model_label_over_the_two_layers():
    lab = lambda *ls: {str(i): {"label": x} for i, x in enumerate(ls)}  # noqa: E731
    assert P.model_label(lab("neither", "distributed")) == "distributed"
    assert P.model_label(lab("flag", "between")) == "flag"
    assert P.model_label(lab("neither", "neither")) == "neither"
    assert P.model_label(lab("neither", "between")) == "between"


def test_dan_answer_reads_only_the_q49_3_block(monkeypatch):
    blocks = "**Q49.2** x\n\nDan: (a)\n\n**Q49.3** The locker-after link ...\n\nDan:{}\n\n**Q49.6** y\n\nDan: 30%\n"
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=blocks.format("")))
    assert P.dan_answer() == ""
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=blocks.format(" 9B (c) · 60%")))
    assert P.dan_answer() == "9B (c) · 60%"


def test_the_committed_predictions_file_has_the_q49_3_block():
    from bridge_jspace import pins

    text = (pins.REPO_ROOT / P.PREDICTIONS).read_text()
    assert "**Q49.3**" in text and "distributed person mark" in text


# ---- the run stage on a fake model ------------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch, render_fake):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = TB.WordTok()
    items = fake_items(tok, 24)
    fake = TB.FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    monkeypatch.setattr(P, "select", lambda *_: (items, {"scenes": len(items), "groups": {}, "dropped": {}, "rows": 72,
                                                         "rows_by_stratum": {}, "rule_cell_rows": {}, "names": 6}))  # fmt: skip
    monkeypatch.setattr(P, "RESULTS", tmp_path / "x49")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pins, "TARGET", "qwen3.5-9b")
    monkeypatch.setattr(pins, "RUN_PREFIX", "qwen35_9b_")
    monkeypatch.setattr(P, "SPEC", tmp_path / "batch49.yaml")
    P.SPEC.write_text("")
    src = tmp_path / "x0" / P.B.FRESH_RUN["qwen3.5-9b"]
    src.mkdir(parents=True)
    for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
        (src / f).write_text("")
    return SimpleNamespace(tok=tok, items=items, fake=fake, out=P.stage_run("qwen35_9b_fake_run", "test"))


def test_run_stage_stores_every_token_and_the_mean_at_two_layers(fake_run):
    import torch

    out, items, fake = fake_run.out, fake_run.items, fake_run.fake
    m = json.loads((out / "manifest.json").read_text())
    assert m["layers"] == [6, 12] and m["test"] == "49.3" and "sealed" in m and m["switches"]["target"] == "qwen3.5-9b"
    assert not any(p.name.startswith(("x49_3", "view")) for p in out.iterdir())  # sealed
    rows = X.read_jsonl(out / "probe_rows.jsonl")
    trows = X.read_jsonl(out / "token_rows.jsonl")
    assert len(rows) == 24 * 3 and len(trows) == 24 * 3 * 8
    for la in (6, 12):
        means = np.load(out / f"means_L{la}.npz")["h"]
        toks = np.load(out / f"tokens_L{la}.npz")["h"]
        assert means.shape == (len(rows), 32) and toks.shape == (len(trows), 32)
        # the scene's O states at the sentence's tokens, and their mean
        it = items[1]
        h = fake.run(torch.tensor([it["readers"]["PP"]["ids"]["org"]]), record=(la,))[1][la].numpy()
        first = [j for j, r in enumerate(rows) if r["item"] == 1]
        for j, s in zip(first, [s for s in it["sentences"] if s["picker"]], strict=True):
            mine = [t for t, tr in enumerate(trows) if tr["row"] == j]
            assert [trows[t]["pos"] for t in mine] == s["tokens"]["positions"]
            assert [trows[t]["key"] for t in mine] == s["tokens"]["keys"]
            assert np.allclose(toks[mine], h[s["tokens"]["positions"]], atol=1e-2)
            assert np.allclose(means[j], h[s["tokens"]["positions"]].mean(0), atol=1e-2)
    # views: the pooled view first, then one per key, each aligned with its rows
    vs = P.views(out, 12, rows)
    assert next(iter(vs)) == P.POOLED and set(vs) == {P.POOLED, *{t["key"] for t in trows}}
    ri, h = vs["item"]
    assert len(ri) == len(rows) and np.allclose(h[3], np.load(out / "tokens_L12.npz")["h"][
        next(t for t, tr in enumerate(trows) if tr["row"] == ri[3] and tr["key"] == "item")], atol=1e-6)  # fmt: skip
    (out / "tokens_L12.npz").unlink()
    assert list(P.views(out, 12, rows)) == [P.POOLED]  # the per-token states are not committed


def test_verdict_and_view_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(P, "dan_answer", lambda: "9B (c) · 60%")
    out = P.stage_verdict([fake_run.out.name], n_boot=50)
    blob = json.loads((out / "x49_3.json").read_text())
    mm = blob["models"][0]
    assert mm["target"] == "qwen3.5-9b" and mm["status"] == "tested" and set(mm["rules"]) == {"6", "12"}
    assert mm["label"] in P.LABELS and blob["models"][1]["status"] == "pending"
    res12 = mm["results"]["12"]["probes"]
    assert set(res12) == set(P.PROBES) and list(res12["identity"]) == [P.POOLED]
    assert res12["picker"][P.POOLED]["after"]["n"] == 12 and res12["picker"][P.POOLED]["before"]["n"] == 12
    md = (out / "x49_3.md").read_text()
    assert "UNVERIFIED" in md and "Rule (fixed in advance)" in md
    view = P.stage_view(fake_run.out.name, tok=fake_run.tok)
    assert (view / "examples.md").read_text().count("```") == 2 * min(X.K_EXAMPLES, 12)


def test_verdict_and_view_are_sealed(fake_run, monkeypatch):
    monkeypatch.setattr(P, "dan_answer", lambda: "")
    with pytest.raises(AssertionError, match="sealed"):
        P.stage_verdict([fake_run.out.name], n_boot=50)
    with pytest.raises(AssertionError, match="sealed"):
        P.stage_view(fake_run.out.name, tok=fake_run.tok)
