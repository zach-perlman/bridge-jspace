"""Batch 47, amendment 3, D1 + D2 (scripts/x47_depthmap.py): the token groups (a fake tokenizer; the target's tokenizer
and X0 runs when cached), the arms' prompts, layers and positions, the run stage end to end on the fake causal model of
tests/test_x47_cumulative.py (every cell's edit at its own layer only; the clean design's b margin equals S), the rules,
l_R, the verdict, the view, the figure on planted maps, and the seal (CPU). No real model."""

import json
from types import SimpleNamespace

import pytest
import torch

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x47_cumulative as C
from scripts import x47_depthmap as D
from scripts.exp04_brew_parts import AddRows, SetRows
from tests import test_x47_cumulative as T

LAYERS = [0, 4, 8, 12, 16, 20, 24, 28, 32, 34]  # the fake model's 36 layers, step 4


def fake_item(i: int, tok: T.WordTok, design: str) -> dict:
    """test_x47_cumulative's fake item with each reader's token groups on the fake tokenizer."""
    it = T.fake_item(i, tok, design)
    it["context"], it["cf_context"] = T.CLEAN if design == "clean" else (T.AFTER if i % 2 == 0 else T.FIRST)
    it["entity"], it["read_suffix"] = "frog", " "  # the bridge: its locker sentence is lk_org (one cluster: fine here)
    it["token_groups"] = {w: D.token_groups(tok, it, w) for w in X.READERS}
    it["locker_roles"] = [r for _, r in D.locker_roles(it["context"], it["entity"], it["cf_bridge"])]
    return it


# ---- token groups -------------------------------------------------------------------------------------------------


def test_locker_roles_by_item():
    roles = D.locker_roles(T.CLEAN[0], "frog", "bee")
    assert [r for _, r in roles] == ["lk_org", "lk_cf", "lk_other1"]
    assert roles[0][0] == "The locker of the frog is 5."
    with pytest.raises(AssertionError, match="missing"):
        D.locker_roles(T.CLEAN[0], "frog", "zebra")


def test_token_groups_cover_the_right_words():
    tok = T.WordTok()
    it = fake_item(0, tok, "clean")
    ids = it["readers"][X.LOOKUP]["ids"]["org"]
    g = it["token_groups"][X.LOOKUP]
    word = lambda ps: tok.decode([ids[p] for p in ps]).strip()  # noqa: E731
    assert word(g["bridge"]) == "frog." and word(g["person"]) == "Iris" and word(g["pick_rest"]) == "picked the"
    assert word(g["lk_org_item"]) == "frog" and word(g["lk_org_num"]) == "5."
    assert word(g["lk_cf_item"]) == "bee" and word(g["lk_cf_num"]) == "3."
    assert word(g["lk_other1_item"]) == "tick" and word(g["lk_other1_num"]) == "2."
    assert word(g["question"]).startswith("Which locker") and word(g["question"]).endswith("Answer:")
    assert g["last"] == [len(ids)]  # the appended space token: the read position
    assert set(g) == {x for x in D.TOKEN_GROUPS if not x.startswith("lk_other2")}
    # the recall's question group sits at its own positions (its question differs); the context groups are shared
    it["readers"][X.RECALL]["question"] = "How many legs does Iris's pick have?"
    it["readers"][X.RECALL]["text"]["org"] = T.wrap(T.CLEAN[0], "How many legs does Iris's pick have?")
    it["readers"][X.RECALL]["ids"]["org"] = tok(it["readers"][X.RECALL]["text"]["org"]).input_ids
    rg = D.token_groups(tok, it, X.RECALL)
    assert rg["question"] != g["question"] and all(rg[k] == g[k] for k in g if k not in ("question", "last"))


def test_arm_names_and_arm_of():
    names = D.arm_names(["bridge", "person", "question", "last"], [0, 4])
    assert names[:4] == list(D.FIXED_ARMS)
    assert names[4:7] == ["gbridge@emb", "gbridge@0", "gbridge@4"] and names[-4:] == ["b0", "b4", "w0", "w4"]
    assert D.arm_of("gbridge@emb") == ("cell", "bridge", "emb") and D.arm_of("glk_cf_item@12") == (
        "cell",
        "lk_cf_item",
        12,
    )
    assert (
        D.arm_of("b4") == ("b", "bridge", 4)
        and D.arm_of("w8") == ("w", "bridge", 8)
        and D.arm_of("a") == ("fixed", None, None)
    )


def test_sampled_layers():
    assert D.sampled_layers(32, 2) == list(range(0, 31, 2))
    assert D.sampled_layers(52, 4) == [*range(0, 49, 4), 50] and D.sampled_layers(64, 4) == [*range(0, 61, 4), 62]


def test_layer_grid_holds_the_layer_fixed_in_advance():
    # Muse's L26 is off the every-4th grid: the run read arms[f"b{layer}"] and failed (x47_d1_muse, 28 Oct)
    assert D.layer_grid(52, 4, 26) == [*range(0, 25, 4), 26, *range(28, 49, 4), 50]
    assert D.layer_grid(36, 2, 12) == D.sampled_layers(36, 2) and D.layer_grid(64, 4, 32) == D.sampled_layers(64, 4)
    for target, step in D.STEP.items():
        assert X.PREDICTED[target] in D.layer_grid(pins.TARGETS[target]["n_layers"], step, X.PREDICTED[target])


def _real_tokenizer():
    from scripts import x45m

    try:
        return x45m.tokenizer()
    except Exception as e:
        pytest.skip(f"target tokenizer not cached: {e}")


@pytest.mark.parametrize("design", D.DESIGNS)
def test_select_on_the_targets_runs(design):
    from bridge_jspace import pins

    run = C.SOURCES[design].get(pins.TARGET)
    if run is None or not (X.RESULTS / run / "cases.jsonl").exists():
        pytest.skip(f"no {design} run of the target here")
    tok = _real_tokenizer()
    items, counts = D.select(tok, design, run, X.PREDICTED[pins.TARGET])
    assert counts["items"] == len(items) > 0
    assert (counts["mixed_left_out"] == 0) == (design == "main")
    for it in items:
        for w in X.READERS:
            ids = it["readers"][w]["ids"]["org"]
            g = it["token_groups"][w]
            assert g["bridge"] == [it["pos"]] and g["last"] == [len(ids)]
            assert tok.decode([ids[p] for p in g["lk_org_item"]]).strip() == it["entity"]
            assert tok.decode([ids[p] for p in g["lk_cf_item"]]).strip() == it["cf_bridge"]
            assert tok.decode([ids[p] for p in g["question"]]).startswith(it["readers"][w]["question"][:5].strip())
            flat = sorted(p for ps in g.values() for p in ps)
            assert len(flat) == len(set(flat))


# ---- the arms ------------------------------------------------------------------------------------------------------


def test_arm_edits_prompts_layers_and_positions():
    n, layer, layers = 10, 4, [0, 2, 4, 6, 8]
    groups = {"bridge": [6], "pick_rest": [4, 5, 7], "person": [3], "question": [8, 9], "last": [10]}
    h_o, h_s = T.states(n, 11, 4, 0), T.states(n, 11, 4, 1)
    arms = D.arm_edits(AddRows, SetRows, h_o, h_s, groups, [3, 4, 5, 6, 7], layer, layers, n)
    assert list(arms) == D.arm_names(list(groups), layers)
    assert arms["none"] == ("org", {}) and arms["S"] == ("alt", {}) and arms["gbridge@emb"] == ("swap", {})
    assert sorted(arms["d"][1]) == list(range(n)) and arms["d"][0] == "swap"
    assert all(e.positions == [3, 4, 5, 6, 7] for e in arms["d"][1].values())
    for g, ps in groups.items():
        for la in layers:
            prompt, edits = arms[f"g{g}@{la}"]
            assert prompt == "org" and list(edits) == [la] and edits[la].positions == ps
            assert torch.equal(edits[la].values, h_s[la][ps])
    assert arms["b4"][0] == "swap" and sorted(arms["b4"][1]) == [0, 1, 2, 3, 4]
    assert arms["w4"][0] == "org" and sorted(arms["w4"][1]) == list(range(4, n))
    assert all(e.positions == [6] for e in {**arms["b4"][1], **arms["w4"][1]}.values())
    ((la, e),) = arms["a"][1].items()
    assert la == layer and isinstance(e, AddRows) and torch.equal(e.delta[0], h_s[4][6] - h_o[4][6])


def test_read_row_is_x0s_decisive_read():
    lg = torch.zeros(10)
    lg[3] = 2.0
    assert D.read_row(lg, {"tok_A": 5, "tok_b": 3}) == [1, "b", 2.0]
    assert D.read_row(lg, {"tok_A": 3, "tok_b": 5}) == [0, "A", -2.0]
    assert D.read_row(lg, {"tok_A": 1, "tok_b": 2})[1] == "other"


# ---- the run stage on the fake model -------------------------------------------------------------------------------


@pytest.fixture
def fake_run(tmp_path, monkeypatch):
    from bridge_jspace import model as M
    from bridge_jspace import pins

    tok = T.WordTok()
    items = {d: [fake_item(i, tok, d) for i in range(12)] for d in D.DESIGNS}
    fake = T.FakeModel(tok)
    monkeypatch.setattr(M, "load_model", lambda: fake)
    counts = {d: {"design": d, "source": C.SOURCES[d][pins.TARGET], "items_at_L": 12, "items": 12, "dropped": {},
                  "entities": 5, "groups": {"locker-first": 8, "locker-after": 4}, "mixed_left_out": 0}
              for d in D.DESIGNS}  # fmt: skip
    monkeypatch.setattr(D, "select", lambda tok, design, run, layer: (items[design], counts[design]))
    monkeypatch.setattr(D, "RESULTS", tmp_path / "x47d")
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pins, "N_LAYERS", fake.n_layers)
    monkeypatch.setattr(D, "STEP", {pins.TARGET: 4})
    monkeypatch.setattr(D, "SPEC", tmp_path / "batch47.yaml")
    D.SPEC.write_text("")
    for d in D.DESIGNS:
        src = tmp_path / "x0" / C.SOURCES[d][pins.TARGET]
        src.mkdir(parents=True)
        for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl"):
            (src / f).write_text("")
    out = D.stage_run(f"{pins.RUN_PREFIX}fake_depthmap", "test")
    return SimpleNamespace(tok=tok, items=items, fake=fake, out=out)


def test_run_stage_end_to_end_on_a_fake_model(fake_run):
    from bridge_jspace import pins

    out, items = fake_run.out, fake_run.items
    rows = X.read_jsonl(out / "outcomes.jsonl")
    assert len(rows) == 2 * 12 * len(X.READERS)
    assert {p.name for p in out.iterdir()} == {"manifest.json", "plan.json", "cases.jsonl", "outcomes.jsonl",
                                               "checks.jsonl", "examples_greedy.jsonl"}  # fmt: skip
    m = json.loads((out / "manifest.json").read_text())
    la = X.PREDICTED[pins.TARGET]
    assert m["layers"] == LAYERS and m["layer"] == la and "sealed" in m
    by = {(r["design"], r["scene"], r["reader"]): r["reads"] for r in rows}
    for it in items["clean"]:
        for w in X.READERS:
            r = by[("clean", it["scene"], w)]
            assert set(r) == set(D.arm_names(list(it["token_groups"][w]), LAYERS))
            # the clean design: the bridge swapped up to any l >= 0, or the whole pick sentence, is S's own run; so is
            # w0 (every block output); the emb cell too (the only changed token)
            for a in ("d", "w0", "gbridge@emb", *(f"b{la}" for la in LAYERS)):
                assert r[a][:2] == r["S"][:2] and abs(r[a][2] - r["S"][2]) < 0.05, a  # the margin: fp32 rounding
            # a cell at one layer only: S's state at the last token at the last sampled layer is read directly
            assert r["glast@34"][:2] == r["S"][:2] and abs(r["glast@34"][2] - r["S"][2]) < 0.05
    for it in items["main"]:
        r = by[("main", it["scene"], X.LOOKUP)]
        if it["prefix_same"]:
            assert r["b34"][:2] == r["d"][:2] and abs(r["b34"][2] - r["d"][2]) < 0.05  # Noah's pick after Iris's
    checks = X.read_jsonl(out / "checks.jsonl")
    assert len(checks) == 24 and all(c["gap_max"] == 0.0 for c in checks if c["prefix_same"])
    greedy = X.read_jsonl(out / "examples_greedy.jsonl")
    assert len(greedy) == 2 * X.K_EXAMPLES * len(X.READERS) * (len(D.GREEDY_ARMS) + 2)
    assert set(rows[0]["top"]) == {*D.GREEDY_ARMS, f"b{la}", f"w{la}"}


def test_run_fails_loudly_when_the_patch_does_not_propagate(monkeypatch, fake_run):
    from bridge_jspace import pins

    real = D.arm_edits

    def shifted(*args, **kwargs):
        arms = real(*args, **kwargs)
        la = X.PREDICTED[pins.TARGET]
        prompt, edits = arms[f"b{la}"]
        arms[f"b{la}"] = (prompt, {k + 1: e for k, e in edits.items()})
        return arms

    monkeypatch.setattr(D, "arm_edits", shifted)
    with pytest.raises(SystemExit, match="BUG"):
        D.stage_run(f"{pins.RUN_PREFIX}fake_depthmap_bug", "test")


def test_verdict_view_and_figures_on_the_fake_run(fake_run, monkeypatch):
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "D1 yes yes no · 60%")
    out = D.stage_verdict([fake_run.out.name], n_boot=100)
    blob = json.loads((out / "depth.json").read_text())
    assert blob["flags"] == [] and blob["dan"].startswith("D1")
    m = blob["models"][0]
    assert m["status"] == "tested" and {x["status"] for x in blob["models"][1:]} == {"pending"}
    clean = m["cells"]["clean"]["all"]["lookup"]
    assert clean["n"] == 12 and clean["cells"]["d"][0] == clean["cells"]["S"][0]
    assert set(m["rules"]["clean"]) == {"a", "b", "c", "d2"}
    md = (out / "depth.md").read_text()
    assert "## Maps" in md and "BUG FLAG" not in md
    view = D.stage_view([fake_run.out.name])
    text = (view / "view.md").read_text()
    assert "⟦lk_cf_item:" in text and "⟦last:" in text and text.count("```") == 2 * 2 * X.K_EXAMPLES * len(X.READERS)
    figs = D.stage_figures(out)
    assert len(figs) == 2 and all(f.exists() for f in figs)


# ---- rules and the verdict on planted maps -------------------------------------------------------------------------


def planted_cells(bridge: dict[int | str, float], lockers: dict[str, float] | None = None, w: dict[int, float] | None = None,
                  layers=LAYERS) -> dict[str, list]:  # fmt: skip
    """Point-estimate cells: the bridge group per layer (emb and the sampled layers; missing = 0), the locker groups'
    peak (every layer the same), the w curve (missing = 1), the rest 0."""
    cells = {"none": [0.0, 0, 0], "a": [0.5, 0.4, 0.6], "d": [0.9, 0.8, 1.0], "S": [1.0, 1, 1]}
    for la in (D.EMB, *layers):
        cells[f"gbridge@{la}"] = [bridge.get(la, 0.0), 0, 1]
    for g in D.TOKEN_GROUPS[1:]:
        if g.startswith("lk_other2"):
            continue
        for la in layers:
            cells[f"g{g}@{la}"] = [(lockers or {}).get(g, 0.0), 0, 1]
    for la in layers:
        cells[f"b{la}"] = [0.5, 0, 1]
        cells[f"w{la}"] = [(w or {}).get(la, 1.0), 0, 1]
    return cells


def test_rule_a_locker_after():
    ok = D.rule_a(planted_cells({4: 0.25, D.EMB: 0.1}, {"lk_org_item": 0.5}), LAYERS, [])
    assert ok["holds"] and ok["locker_best"]["arm"] == "glk_org_item@0"
    assert not D.rule_a(planted_cells({4: 0.26}, {"lk_org_item": 0.9}), LAYERS, [])["holds"]  # the bridge too hot
    assert not D.rule_a(planted_cells({D.EMB: 0.3}, {"lk_org_item": 0.9}), LAYERS, [])["holds"]  # the emb cell counts
    r = D.rule_a(planted_cells({4: 0.1}, {"lk_cf_num": 0.49, "pick_rest": 0.9}), LAYERS, [])
    assert not r["holds"] and r["bridge_ok"] and not r["locker_ok"]  # the pick sentence is not a locker sentence


def test_rule_b_locker_first():
    lk = planted_cells({0: 0.9, 4: 0.5, 8: 0.3})
    rc = planted_cells({0: 0.9, 4: 0.5, 8: 0.5, 12: 0.31})
    r = D.rule_b(lk, rc, LAYERS, 4)
    assert r["holds"] and r["lookup_last"] == 8 and r["recall_last"] == 12 and r["lead"] == 4
    assert not D.rule_b(lk, rc, LAYERS, 5)["holds"]
    assert not D.rule_b(rc, lk, LAYERS, 2)["holds"]  # the recall ends first
    r = D.rule_b(planted_cells({0: 0.2}), rc, LAYERS, 2)
    assert not r["holds"] and r["lookup_last"] is None and r["lead"] is None


def test_rule_c_second_hot_token():
    first, after = planted_cells({}, {"lk_cf_item": 0.3}), planted_cells({}, {"lk_cf_item": 0.29})
    assert D.rule_c(first, after, LAYERS)["holds"]
    assert not D.rule_c(after, first, LAYERS)["holds"]
    assert not D.rule_c(first, first, LAYERS)["holds"]
    assert D.rule_c(first, None, LAYERS) == {"holds": False, "locker_first_peak": 0.3, "locker_after_peak": None}


def test_l_r_and_rule_d2():
    cells = planted_cells({}, w={0: 0.9, 4: 0.5, 8: 0.1, 12: 0.0, 16: 0.2, 20: 0.0, 24: 0.0, 28: 0.0, 32: 0.0, 34: 0.0})
    assert D.l_r(cells, LAYERS) == 8
    assert D.l_r(planted_cells({}), LAYERS) is None
    assert D.rule_d2(8, 26)["holds"] and D.rule_d2(26, 26)["holds"] and not D.rule_d2(28, 26)["holds"]
    assert not D.rule_d2(None, 26)["holds"] and D.rule_d2(8, None)["holds"] is None


def test_rates_pair_the_arms_and_handle_a_group_some_items_lack():
    rows = [{"entity": f"e{i % 4}", "reads": {"x": [int(i < 6), "b", 0.0], "y": [int(i < 3), "b", 0.0],
                                              **({"z": [1, "b", 0.0]} if i < 4 else {})}} for i in range(12)]  # fmt: skip
    r = D.rates(rows, ["x", "y", "z"], n_boot=200)
    assert r["x"][0] == pytest.approx(0.5) and r["y"][0] == pytest.approx(0.25)
    assert r["z"][:3] == [1.0, 1.0, 1.0] and r["z"][3] == 4  # over the 4 rows that have it, with its n
    for v in r.values():
        assert v[1] <= v[0] + 1e-12 <= v[2] + 2e-12


def write_planted(root, name: str, target: str, layers=LAYERS, n: int = 40) -> None:
    """A planted D1 run on the clean design (locker-first / locker-after halves) and the main test (same): the lookup's
    bridge cells hot up to layer 8 locker-first and cold locker-after (with the lk_org item hot there); the recall's
    bridge cells hot up to 16 and its lk_cf item hot locker-first only; the w curve falls under 0.1 at 12 (recall) and
    at 24 (lookup)."""
    src = root / name
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12, "n_layers": 36,
                                                   "layers": layers, "sources": {"main": "m", "clean": "c"}}))  # fmt: skip
    (src / "plan.json").write_text(json.dumps({d: {"items": n, "items_at_L": n, "source": d, "dropped": {},
                                                   "mixed_left_out": 0, "groups": {}, "entities": 8}
                                               for d in D.DESIGNS}))  # fmt: skip
    groups = [g for g in D.TOKEN_GROUPS if not g.startswith("lk_other2")]
    rows, checks, cases = [], [], []
    for design in D.DESIGNS:
        for i in range(n):
            first = i < n // 2
            order = "locker-first" if first else "locker-after"
            scene = f"{design}{i}"
            cases.append({"scene": scene, "design": design})
            checks.append({"scene": scene, "design": design, "prefix_same": True, "gap_max": 0.0})
            for w in X.READERS:
                lookup = w == X.LOOKUP
                reads = {
                    "none": [0, "A", 0.0],
                    "a": [int(i % 2 == 0), "b", 0.0],
                    "d": [1, "b", 0.0],
                    "S": [1, "b", 0.0],
                }
                for g in groups:
                    if g == "bridge":
                        reads[f"g{g}@{D.EMB}"] = [int(first and i % 5 == 0), "b", 0.0]
                    for la in layers:
                        on = 0
                        if g == "bridge" and first:
                            on = int(la <= (8 if lookup else 16))
                        elif g == "lk_org_item" and not first and lookup:
                            on = int(la >= 8)
                        elif g == "lk_cf_item" and first and not lookup:
                            on = int(la in (4, 8))
                        reads[f"g{g}@{la}"] = [on, "b" if on else "A", 0.0]
                for la in layers:
                    reads[f"b{la}"] = [1, "b", 0.0]
                    reads[f"w{la}"] = [int(la < (24 if lookup else 12)), "b", 0.0]
                rows.append({"scene": scene, "entity": f"e{i % 8}", "design": design, "group": order, "upstream": False,
                             "prefix_same": True, "reader": w, "reads": reads, "top": {}})  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "checks.jsonl", checks)
    X.write_jsonl(src / "examples_greedy.jsonl", [])


def test_verdict_on_planted_maps(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "yes · 70%")
    write_planted(tmp_path, "r9", "qwen3.5-9b")
    write_planted(tmp_path, "rm", "muse-glimmer-30b")
    out = D.stage_verdict(["r9", "rm"], n_boot=100)
    blob = json.loads((out / "depth.json").read_text())
    by = {m["target"]: m for m in blob["models"]}
    for target, lead_ok in (("qwen3.5-9b", True), ("muse-glimmer-30b", True)):
        r = by[target]["rules"]["clean"]
        assert r["a"]["holds"] and r["a"]["bridge_max"] == 0.0 and r["a"]["locker_best"]["rate"] == 1.0
        assert r["b"]["holds"] == lead_ok and (r["b"]["lookup_last"], r["b"]["recall_last"]) == (8, 16)
        assert r["c"]["holds"] and r["c"]["locker_first_peak"] == 1.0 and r["c"]["locker_after_peak"] == 0.0
    assert by["qwen3.5-9b"]["rules"]["clean"]["d2"] == {"holds": True, "l_R_recall": 12, "band_start": 26}
    assert by["muse-glimmer-30b"]["rules"]["main"]["d2"]["holds"] is None
    cells = by["qwen3.5-9b"]["cells"]["clean"]["locker-first"]
    assert cells["lookup"]["l_R"] == 24 and cells["recall"]["l_R"] == 12 and cells["lookup"]["n"] == 20
    assert by["qwen3.5-9b"]["cells"]["main"]["all"]["recall"]["cells"]["glk_cf_item@4"][0] == pytest.approx(0.5)
    assert by["qwen3.6-27b"]["status"] == "pending"
    md = (out / "depth.md").read_text()
    assert "| qwen3.5-9b | clean | yes (bridge max 0.0" in md and "BUG FLAG" not in md
    figs = D.stage_figures(out)
    assert len(figs) == 4 and {f.name for f in figs} == {f"depthmap_{s}_{g}.png" for s in ("9b", "muse")
                                                        for g in ("locker_first", "locker_after")}  # fmt: skip


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    monkeypatch.setattr(D, "dan_answer", lambda rev="HEAD": "")
    write_planted(tmp_path, "r9", "qwen3.5-9b")
    for stage in (lambda: D.stage_verdict(["r9"], n_boot=10), lambda: D.stage_view(["r9"]),
                  lambda: D.stage_figures(tmp_path)):  # fmt: skip
        with pytest.raises(AssertionError, match="sealed"):
            stage()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r9"]


def test_dan_answer_reads_the_q_depth_block_only(monkeypatch):
    import subprocess

    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q47.8** x\n\nDan: (a) yes\n\n**Q-depth** (amendment 3)\n- D1 ...\n\nDan:{}\n\n## Batch 48\n\n"
              "**Q48.1** y\n\nDan: z\n")  # fmt: skip
    monkeypatch.setattr(subprocess, "run", fake_git(blocks.format("")))
    assert D.dan_answer() == ""
    monkeypatch.setattr(subprocess, "run", fake_git(blocks.format(" D1 yes/no/yes · 60%")))
    assert D.dan_answer() == "D1 yes/no/yes · 60%"


def test_the_committed_predictions_file_has_the_q_depth_block():
    import subprocess

    text = subprocess.run(["git", "show", f"HEAD:{D.PREDICTIONS}"], cwd=D.pins.REPO_ROOT, capture_output=True, text=True,
                          check=False).stdout  # fmt: skip
    if f"**{D.QUESTION}**" not in text:
        pytest.skip("the Q-depth block is not in this checkout's HEAD")
    assert isinstance(D.dan_answer(), str)


def test_lightning_coverage_runs_muses_grid_on_the_main_test(tmp_path, monkeypatch):
    """Batch 52: Lightning takes Muse's step (every 4th layer), a coverage run outside D1's own RUNS, the main-test
    design alone (--designs main), and a coverage verdict without the Q-depth seal."""
    from scripts import x47_depthmap as DM

    lt = "nemotron-3.5-lightning"
    assert (
        DM.STEP[lt] == DM.STEP["muse-glimmer-30b"] and lt not in DM.RUNS and DM.COVERAGE_RUNS[lt].startswith("nem35l_")
    )
    monkeypatch.setattr(DM, "RESULTS", tmp_path)
    monkeypatch.setattr(DM, "DESIGNS", ("main",))
    monkeypatch.setattr(DM, "unsealed", lambda: (_ for _ in ()).throw(AssertionError("sealed")))
    monkeypatch.setattr(DM, "model_result", lambda r, n_boot: {"run": r, "target": lt, "status": "pending", "why": "x"})
    with pytest.raises(AssertionError, match="sealed"):
        DM.stage_verdict(["nem35l_x52_depthmap"], n_boot=10)
    out = DM.stage_verdict(["nem35l_x52_depthmap"], n_boot=10, coverage=True)
    assert out.name.startswith("x52_depthmap-")
    assert any(DM.NO_PREDICTION in p.read_text() for p in out.iterdir() if p.suffix in (".md", ".json"))
