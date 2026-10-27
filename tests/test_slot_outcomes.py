"""scripts/slot_outcomes.py and scripts/figs/slot_outcomes.py on SYNTHETIC rows: each patched answer lands in its outcome
and (another listed digit) its source with the uniform baseline; off-list answers stay apart (the case diagnostic
aside); a role its slot contradicts, an unknown role or a changed item file is refused; end to end on a synthetic repo,
the checks against the grid, the saved verdict and the layer rule pass, and fail when the grid is off; the figures save
(overlap check), draw every bar as shares of its counts summing to 100, and the FULL caption names the exceptions."""

from __future__ import annotations

import collections
import csv
import hashlib
import json
from pathlib import Path

import pytest

from scripts import readme_build as RB
from scripts import slot_outcomes as SO
from scripts.figs import slot_outcomes as FIG

DIGITS = [4, 1, 2, 6, 5]


def item(name: str, digits: list, query: int, identity: int, position: int, value, family: str = "RL") -> dict:
    ents = [f"e{i}" for i in range(len(digits))]
    preds = {"none": str(digits[query]), "identity": str(digits[identity]), "position": str(digits[position]),
             "value": str(value)}  # fmt: skip
    return {"id": name, "family": family, "domain": "countries", "query": ents[query], "entities": ents,
            "digits": digits, "slots": {"query": query, "identity": identity, "position": position},
            "sources": {"dissoc": {"query_slot": position, "predictions": preds}}}  # fmt: skip


def row(it: dict, top: str, role: str, layer: int = 50, source: str = "dissoc") -> dict:
    return {"family": it["family"], "domain": it["domain"], "level": "e5f0", "name": it["id"], "layer": layer,
            "group": "last", "source": source, "top": top, "role": role}  # fmt: skip


def test_tally_sorts_answers_into_outcomes_and_sources():
    a = item("a", DIGITS, 2, 3, 0, 7)  # k = 1
    b = item("b", [6, 2, 8, 7, 9], 4, 3, 2, 1)  # k = 3; free sentences 1, 2
    c = item("c", [6, 2, 8, 7, 9], 4, 3, 2, 1)
    d = item("d", [1, 2, 3, 4, 5], 0, 1, 4, 9)  # k = 5; free sentences 3 (elsewhere), 4 (k - 1)
    e = item("e", ["red", "blue", "grey", "gold", "pink"], 0, 1, 2, "black")  # k = 3, colour words
    f = item("f", DIGITS, 2, 3, 0, 7)
    g = item("g", DIGITS, 2, 3, 0, 7, family="DL")
    items = {x["id"]: x for x in (a, b, c, d, e, f, g)}
    rows = [row(a, "4", "position"), row(b, "6", "context"), row(c, "2", "context"), row(d, "3", "context"),
            row(e, " Blue", "other"), row(f, "8", "recall"), row(g, "2", "none"),
            row(a, "7", "value", layer=40), row(b, "8", "position", source="same")]  # fmt: skip
    t, check = SO.tally(rows, items, 50, 5)
    assert check == {"agrees": 5, "unresolved": 0}  # a, b, c, d, g: on the list, the slot agrees with the role
    assert set(t) == {("RL", 1), ("RL", 3), ("RL", 5), ("DL", 1)}  # other layers and sources are left out
    assert t[("RL", 1)].count("order") == 1 and t[("RL", 1)].roles["recall"] == 1 and t[("RL", 1)].off() == 1
    k3 = t[("RL", 3)]
    assert k3.n == 3 and k3.count("another") == 2 and k3.off() == 1
    assert k3.sources == {"slot 1": 1, "k±1": 1, "k-1": 1}  # sentence 1 counts as slot 1; sentence 2 is k - 1
    assert k3.expected == {"slot 1": 1.0, "k±1": 1.0, "elsewhere": 0.0}  # b, c: free 1 and 2, half each
    assert k3.case == {"identity": 1}  # ' Blue' names the identity's 'blue' when case is ignored
    k5 = t[("RL", 5)]
    assert k5.sources == {"elsewhere": 1}
    assert k5.expected == {"slot 1": 0.0, "k±1": 0.5, "elsewhere": 0.5}
    assert t[("DL", 1)].count("unchanged") == 1


def test_another_listed_digit_sources():
    assert SO.source_of(0, 2) == "slot 1"  # at k = 2, k - 1 is slot 1: slot 1 wins
    assert SO.source_of(2, 2) == "k±1" and SO.source_of(3, 3) == "k±1" and SO.source_of(3, 2) == "elsewhere"
    it = item("x", ["red", "blue", "grey", "gold", "pink"], 0, 1, 2, "black")
    assert SO.slot_of(" gold", it) == 3 and SO.slot_of(" go", it) == 3  # a word's first token
    assert SO.slot_of(" g", it) is None and SO.slot_of(" Gold", it) is None  # ambiguous; case kept (roles do)


def test_tally_refuses_a_contradicting_slot_and_an_unknown_role():
    a = item("a", DIGITS, 2, 3, 0, 7)
    with pytest.raises(ValueError, match="slot 2, role position"):
        SO.tally([row(a, "1", "position")], {"a": a}, 50, 5)
    with pytest.raises(ValueError, match="unexpected role"):
        SO.tally([row(a, "1", "end")], {"a": a}, 50, 5)
    with pytest.raises(ValueError, match="slot 1, role context"):  # another digit must not be a named outcome
        SO.tally([row(a, "4", "context")], {"a": a}, 50, 5)


# ---------------------------------------------------------------- a synthetic repo, end to end


def roles_for(i: int, family: str, k: int, layer: int, value_layer: int | None) -> str:
    if layer == value_layer:
        return "value"
    if family == "DL":
        return "none"
    return "position" if k <= 2 else ("identity" if i % 2 == 0 else "none")


def make_run(repo: Path, run: str, n: int, layers: list[int], value_layer: int | None = None) -> dict:
    """Items, manifest and outcomes of one run; returns {family: {k: Counter(role)}} at the first layer."""
    items, rows = [], []
    by_k: dict[str, dict[int, collections.Counter]] = {f: collections.defaultdict(collections.Counter)
                                                       for f in ("RL", "DL")}  # fmt: skip
    for i in range(n):
        k = i % 5 + 1
        digits = [(i + j) % 9 + 1 for j in range(5)]
        value = next(v for v in range(1, 10) if v not in digits)
        p = k - 1
        for fam in ("RL", "DL"):
            it = item(f"{run}-{fam}-{i}", digits, (p + 1) % 5, (p + 2) % 5, p, value, fam)
            items.append(it)
            preds = it["sources"]["dissoc"]["predictions"]
            for la in layers:
                role = roles_for(i, fam, k, la, value_layer)
                rows.append(row(it, preds[role], role, layer=la))
                if la == layers[0]:
                    by_k[fam][k][role] += 1
    raw = json.dumps({"items": items}).encode()
    (repo / "data").mkdir(exist_ok=True)
    (repo / "data" / f"{run}.json").write_bytes(raw)
    d = repo / "results" / "pointer_swap" / run
    d.mkdir(parents=True)
    m = {"items": {"x": {"file": f"data/{run}.json", "sha256": hashlib.sha256(raw).hexdigest()}},
         "families": ["RL", "DL"], "layers": layers}  # fmt: skip
    (d / "manifest.json").write_text(json.dumps(m))
    (d / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return by_k


def grid_rows(model: str, run: str, layer: int, by_k: dict, path: str) -> list[dict]:
    out = []
    for part, ks, (a, b) in (("1st-2nd", (1, 2), ("position", "identity")), ("3rd on", (3, 4, 5),
                                                                              ("identity", "position"))):  # fmt: skip
        cs = [by_k["RL"][k] for k in ks]
        n = sum(sum(c.values()) for c in cs)
        v = (sum(c[a] for c in cs) - sum(c[b] for c in cs)) / n
        out.append({"model": model, "finding": "f5", "setting": f"draw 1, {part}", "n": n, "value": v, "run": run,
                    "control": f"x; layer {layer} (y)", "path": path, "verdict": "holds"})  # fmt: skip
    return out


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r27 = make_run(tmp_path, "r27", 40, [50])
    r9 = make_run(tmp_path, "r9", 40, [20, 21], value_layer=21)  # the rule: 21 has the donor's digit, so 20
    vpath = "results/finding5_confirm/r9_20261022-000000/verdict.json"
    (tmp_path / vpath).parent.mkdir(parents=True)
    fams = {f: {"by_k": {str(k): dict(c) for k, c in r9[f].items()}} for f in ("RL", "DL")}
    (tmp_path / vpath).write_text(json.dumps({"layer": 20, "families": fams}))
    rows = grid_rows("27b", "r27", 50, r27, "results/pointer_swap/r27/outcomes.jsonl") + grid_rows("9b", "r9", 20,
                                                                                                 r9, vpath)  # fmt: skip
    rows.append({"model": "gemma", "finding": "f5", "setting": "8 sentences", "n": None, "value": None, "run": "g",
                 "control": "", "path": "", "verdict": "missing (no spec)"})  # fmt: skip
    g = tmp_path / "grid"
    g.mkdir()
    (g / "grid.json").write_text(json.dumps({"rows": rows}))
    return tmp_path


def test_collect_checks_pass_and_write_the_three_files(repo: Path):
    res = SO.collect(repo / "grid", repo)
    assert all(x["ok"] for k in ("grid", "verdict", "layer") for x in res["checks"][k])
    assert [x["layer"] for x in res["checks"]["layer"]] == [50, 20]  # fixed 50 (27B draws); the rule's 20
    assert len(res["checks"]["verdict"]) == 1 and res["missing"] == ["Gemma 8 sentences: missing (no spec)"]
    assert all(x["counts_sum_to_n"] and x["five_sum_pct"] == 100.0 for x in res["checks"]["sum"])
    by = {(r["model"], r["family"], r["setting"], r["k"]): r for r in res["rows"]}
    assert by[("27b", "RL", "draw 1", 1)]["order_n"] == 8 and by[("27b", "RL", "draw 1", 1)]["order_pct"] == 100.0
    assert by[("27b", "RL", "draw 1", 3)]["identity_pct"] == 50.0 and by[("27b", "DL", "draw 1", 4)]["unchanged_n"] == 8
    assert by[("9b", "RL", SO.POOLED, 2)]["n"] == 8  # one draw pooled: the same counts
    d = SO.write(res, repo / "grid", repo / "out", ["--grid", "grid"])
    assert sorted(p.name for p in d.iterdir()) == ["summary.json", "table.csv", "table.md"]
    with (d / "table.csv").open() as fh:
        assert tuple(csv.DictReader(fh).fieldnames or ()) == SO.COLUMNS
    summary = json.loads((d / "summary.json").read_text())
    assert summary["check_failures"] == {} and summary["checks_line"].startswith("grid n and point value 4/4")
    assert "## Qwen3.6-27B, memory -> prompt (recalled bridge), draw" not in (d / "table.md").read_text()  # pooled only


def test_collect_flags_a_grid_cell_it_does_not_reproduce(repo: Path):
    g = json.loads((repo / "grid" / "grid.json").read_text())
    g["rows"][0]["value"] += 0.01
    (repo / "grid" / "grid.json").write_text(json.dumps(g))
    res = SO.collect(repo / "grid", repo)
    assert [x["ok"] for x in res["checks"]["grid"]] == [False, True, True, True]


def test_load_refuses_a_changed_item_file(repo: Path):
    (repo / "data" / "r27.json").write_text('{"items": []}')
    with pytest.raises(ValueError, match="sha256"):
        SO.collect(repo / "grid", repo)


# ---------------------------------------------------------------- the figure, on a synthetic table


def synth_tally(model: str, fam: str, setting: str, k: int) -> SO.Tally:
    t = SO.Tally(n=40)
    if k <= 2:
        t.roles.update(position=30, none=6, identity=2, context=2)
    elif model == "muse" and fam == "RL" and setting == "12 sentences":
        t.roles.update(other=24, identity=12, position=2, none=2)  # 10 bars x 24 of 12 x 40 answers: 50% off
    elif model == "32b" and fam == "DL" and setting == SO.POOLED:
        t.roles.update(identity=6, position=6, none=26, context=2)  # entity ties order
    else:
        t.roles.update(identity=18, position=6, none=8, context=4, value=2, other=2)
    return t


@pytest.fixture
def table(tmp_path: Path) -> Path:
    rows = []
    for m in RB.ORDER:
        for fam in SO.FAMILIES:
            for setting, n in FIG.LISTS:
                if m == "gemma" and n != 5:
                    continue
                runs = ["a", "b"] if m == "olmo_hybrid" and n == 5 else ["a", "b", "c"]
                for k in range(1, n + 1):
                    rows.append(SO.table_row(m, fam, setting, n, k, synth_tally(m, fam, setting, k), [50], runs))
    d = tmp_path / "table"
    d.mkdir()
    with (d / "table.csv").open("w") as fh:
        w = csv.DictWriter(fh, fieldnames=SO.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return d


def records(out: Path, kind: str) -> list[dict]:
    return json.loads((out / "data" / f"slot_outcomes_{kind}.json").read_text())


def bars_sum_to_100(recs: list[dict]) -> None:
    bars: dict[tuple, float] = collections.defaultdict(float)
    for d in recs:
        bars[(d["model"], d["extra"]["family"], d["setting"], d["extra"]["k"])] += d["value"]
    assert all(abs(v - 100) < 1e-9 for v in bars.values())


def test_figures_save_and_draw_shares_of_the_counts(table: Path, tmp_path: Path):
    out = tmp_path / "out"
    assert [p.name for p in FIG.draw_main(table, out)] == ["slot_outcomes_main.png", "slot_outcomes_main.svg"]
    main = records(out, "main")
    assert {d["model"] for d in main} == set(FIG.MAIN_MODELS)
    assert {(d["extra"]["family"], d["setting"]) for d in main} == {("RL", SO.POOLED)}
    first = next(d for d in main if d["model"] == "27b" and d["extra"]["k"] == 1 and d["extra"]["outcome"] == "order")
    assert first["value"] == 75.0 and first["n"] == 40  # 30 of 40
    bars_sum_to_100(main)
    FIG.draw_full(table, out)
    full = records(out, "full")
    bars = {(d["model"], d["extra"]["family"], d["setting"], d["extra"]["k"]) for d in full}
    assert len(bars) == 7 * 2 * (5 + 8 + 12) + 2 * 5  # Gemma: 5 sentences only
    assert not any(d["model"] == "gemma" and d["setting"] != SO.POOLED for d in full)
    bars_sum_to_100(full)


def test_full_caption_names_the_exceptions(table: Path):
    rows = FIG.read_table(table)
    cap = FIG.full_caption(rows, list(rows))
    assert cap.count("\n") <= 1
    assert "Olmo-Hybrid two" in cap and "Not run: Gemma 8 and 12 sentences." in cap
    assert "Off the list: Muse 50% (recalled, 12)." in cap  # the others' 3-4% stay below the 20% bar
    assert "Entity ≈ order from sentence 3: 32B (named, 5; +0.0 pts)." in cap


def test_figure_words_are_plain():
    texts = [FIG.TITLE, FIG.SUBTITLE, FIG.HOW, FIG.HOW_FULL, FIG.XLABEL, *FIG.FAMILY.values(),
             *(s.label for s in FIG.SEGS)]  # fmt: skip
    assert len(FIG.TITLE.split()) <= 12
    for word in ("donor", "patched", "swapped", "RL", "DL", "identity"):
        assert all(word not in t for t in texts)


def test_command_line(table: Path, tmp_path: Path):
    out = tmp_path / "cli"
    assert FIG.main(["--table", str(table), "--only", "main", "--out", str(out)]) == 0
    assert {p.name for p in out.glob("*.png")} == {"slot_outcomes_main.png"}


def absent_verdict(tmp_path: Path) -> Path:
    """A synthetic absent-entity verdict.json: k = 1 has no decisive item; k = 2-5 shares of n."""
    by_k = {"1": {"all": {}, "decisive": {"n": 0}}}
    for k, (n, order, fallback, other, unchanged) in {2: (100, 0.9, 0.0, 0.02, 0.08), 3: (80, 0.5, 0.0125, 0.2, 0.2875),
                                                      4: (50, 0.2, 0.0, 0.4, 0.4), 5: (40, 0.3, 0.025, 0.25, 0.425)}.items():  # fmt: skip
        d = {"n": n, "order": [order, order - 0.05, order + 0.05], "other_digit": [other, 0.0, other + 0.1],
             "unchanged": [unchanged, 0.0, unchanged + 0.1]}  # fmt: skip
        if fallback:
            d["fallback"] = [fallback, 0.0, 0.05]
        by_k[str(k)] = {"all": {}, "decisive": d}
    p = tmp_path / "absent" / "verdict.json"
    p.parent.mkdir()
    p.write_text(json.dumps({"families": {"RL": {"by_k": by_k}}}))
    return p


def test_absent_panel_reads_the_decisive_shares_and_draws_beside_the_models(table: Path, tmp_path: Path):
    path = absent_verdict(tmp_path)
    rows = FIG.read_absent(path)
    assert [r["k"] for r in rows] == ["2", "3", "4", "5"]  # k = 1: not tested
    assert rows[1]["order_n"] == "40" and rows[1]["fallback_n"] == "1" and rows[1]["another_n"] == "16"
    assert all("identity_n" not in r and r["donor_n"] == "0" for r in rows)  # the entity is not in the original
    out = tmp_path / "out"
    FIG.draw_main(table, out, path)
    main = records(out, "main")
    absent = [d for d in main if d["setting"] == FIG.ABSENT_KEY[2]]
    assert {d["extra"]["k"] for d in absent} == {2, 3, 4, 5}
    assert next(d for d in absent if d["extra"]["k"] == 3 and d["extra"]["outcome"] == "fallback")["value"] == 1.25
    bars_sum_to_100(main)


def test_absent_shares_that_do_not_sum_to_n_are_refused(tmp_path: Path):
    path = absent_verdict(tmp_path)
    d = json.loads(path.read_text())
    d["families"]["RL"]["by_k"]["2"]["decisive"]["order"][0] = 0.5
    path.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="do not sum"):
        FIG.read_absent(path)


def test_unchanged_range_rounds_the_pooled_bars(table: Path):
    rows = FIG.read_table(table)
    us = [FIG.shares(r)["unchanged"] for r in rows[("gemma", "RL", SO.POOLED)]]
    lo, hi = round(min(us)), round(max(us))
    assert FIG.unchanged_range(rows, "gemma") == (f"{lo}%" if lo == hi else f"{lo}–{hi}%")
