"""summary_states and summary_heatmap on a SYNTHETIC grid.csv (no result file is read).

States: ≈ chance (a miss of the late read's bar with chance inside the interval, the bound included), the majority
rule without "mixed" (a tie is not a hold; a setting whose parts disagree does not hold), the two finding-6 rows,
findings 2 and 8 merged (the worse), the lens gate's descriptive values, finding 7's main rule with † where the amended
rule differs, "holds (Zach)" only where the grid has no verdict under his rule, why a cell can't tell or was not tested,
the lens listed beside and the breakdown rows ignored. Figure: both versions save (common.save's overlap check) at
their sizes, every model and row drawn, the caption lists the failing cells and the untested ones, the data file."""

from __future__ import annotations

import csv
import io
import json

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pytest
from matplotlib.text import Text

from bridge_jspace import plot_style as PS
from scripts import cross_model_grid as G
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import summary_heatmap as SH
from scripts.figs import summary_states as SS

MAIN_LENS = "J++, synthetic, 00000000"
BAR = "fails (more than 20% right, or the upper bound above 30%)"
DEFAULT = (("f3", "draw 1", "holds"), ("f4", "draw 1", "holds"), ("f5", "draw 1, 1st-2nd", "holds"),
           ("f5", "draw 1, 3rd on", "holds"), ("f6", "filler moved", "holds"), ("f6", "one statement more", "holds"),
           ("f6", "one statement fewer", "holds"), ("gate", "v1 (at the word)", "holds"),
           ("gate", "v2 (after the word)", "fails"), ("f7", "main rule", "holds"), ("f7", "amended rule", "holds"),
           ("f2", "draw 1", "holds"), ("f8", "stated bridge, draw 1", "holds"), ("f1", "tasks, Zach's rule", "holds"),
           ("f1", "animal suite", "open (descriptive, no committed rule)"))  # fmt: skip
NO_LENS = "not testable (no lens)"
# (model, finding, setting) -> (verdict, n, value, ci, control); a verdict of None drops the default row
OVERRIDE: dict[tuple[str, str, str], tuple[str | None, int | None, float | None, tuple[float, float] | None, str]] = {
    ("27b", "f4", "draw 2"): ("holds", 300, 7.0, (5.0, 10.0), "chance 20% (5 listed answers)"),
    ("27b", "f4", "long context"): (BAR, 178, 25.8, (20.0, 32.7), "chance 20% (5 listed answers)"),  # bound = chance
    ("gemma", "f4", "draw 1"): (BAR, 300, 22.7, (18.3, 27.7), "chance 20% (5 listed answers)"),
    ("gemma", "f4", "draw 2"): (BAR, 300, 21.7, (17.4, 26.7), "chance 20% (5 listed answers)"),
    ("gemma", "f4", "draw 3"): ("holds", 300, 19.3, (15.3, 24.2), "chance 20% (5 listed answers)"),
    ("olmo", "f4", "table"): (BAR, 40, 45.0, (35.0, 55.0), "chance 33% (3 listed answers)"),  # above chance: fails
    ("muse", "f3", "draw 2"): ("holds", 300, 2.0, (1.0, 4.0), ""),
    ("muse", "f3", "prose"): ("fails", 5, 40.0, (11.8, 76.9), ""),  # few items
    ("32b", "f5", "draw 2, 1st-2nd"): ("holds", 170, 80.0, (70.0, 90.0), ""),
    ("32b", "f5", "draw 2, 3rd on"): ("fails (partly: A True, B False)", 270, 2.0, (-5.0, 10.0), ""),
    ("9b", "f6", "one statement more"): ("fails", 391, 14.1, (11.0, 17.9), ""),
    ("9b", "f6", "one statement fewer"): ("fails", 405, 23.2, (19.2, 27.6), ""),
    ("32b", "gate", "v2 (after the word)"): ("holds", 60, 40.0, (30.0, 50.0), ""),
    ("olmo", "gate", "v1 (at the word)"): ("fails", 60, 10.0, (5.0, 20.0), ""),
    ("27b", "f7", "main rule"): ("inconclusive (the lookup moves between 10% and 30%)", 100, 29.0, (21.0, 38.5), ""),
    ("27b", "f7", "main rule, draw 2"): ("holds", 100, 0.0, (0.0, 3.7), ""),
    ("27b", "f7", "amended rule, draw 2"): ("holds", 100, 0.0, (0.0, 3.7), ""),
    ("32b", "f7", "main rule"): ("missing (qwen3_32b_jpp_d4_where is running in the queue)", None, None, None, ""),
    ("32b", "f7", "amended rule"): ("missing (qwen3_32b_jpp_d4_where is running in the queue)", None, None, None, ""),
    ("gemma", "f7", "main rule"): ("missing (x_where waits on x_map, which failed)", None, None, None, ""),
    ("gemma", "f7", "amended rule"): ("missing (x_where waits on x_map, which failed)", None, None, None, ""),
    ("122b", "f2", "draw 1"): ("fails", 180, 29.4, (23.3, 36.5), ""),
    ("9b", "f8", "stated bridge, draw 1"): ("not interpretable (the lookup write is inconclusive)", 120, 0.0, None, ""),
    ("9b", "f1", "tasks, Zach's rule"): ("missing (no spec)", None, None, None, ""),
    ("32b", "f1", "tasks, Zach's rule"): ("missing (no spec)", None, None, None, ""),
    ("muse", "f1", "tasks, Zach's rule"): ("missing (no spec)", None, None, None, ""),
    ("122b", "f1", "tasks, Zach's rule"): ("missing (no spec)", None, None, None, ""),
}
NOISE = (  # rows the rule must not read: another lens (listed beside), a breakdown row
    ("27b", "f3", "draw 1", "fails", "plain J-lens (synthetic, listed beside)"),
    ("27b", "f1", "animal suite · lookup, bridge stated", "fails", MAIN_LENS),
)


def synth_rows() -> list[tuple[str, str, str, str, int | None, float | None, tuple[float, float] | None, str, str]]:
    rows = []
    for m in G.MODELS:
        keys = [(f, s) for f, s, _ in DEFAULT] + [(f, s) for (mm, f, s) in OVERRIDE if mm == m.key]
        for f, s in dict.fromkeys(keys):
            default = next((w for ff, ss, w in DEFAULT if (ff, ss) == (f, s)), None)
            verdict, n, value, ci, control = OVERRIDE.get((m.key, f, s), (default, 100, 5.0, (2.0, 9.0), ""))
            if m.key == "olmo_hybrid" and G.FINDING[f].lens:
                verdict, n, value, ci, control = NO_LENS, None, None, None, ""
            if verdict is not None:
                rows.append((m.key, f, s, verdict, n, value, ci, control, MAIN_LENS))
    rows += [(m, f, s, v, 100, 50.0, (40.0, 60.0), "", lens) for m, f, s, v, lens in NOISE]
    return rows


def synth_csv() -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for m, f, s, verdict, n, value, ci, control, lens in synth_rows():
        unit = "pts" if f in ("f1", "f5") else "%"
        w.writerow([G.MODEL[m].label, G.FINDING[f].name, s, lens, "" if n is None else n,
                    "" if value is None else f"{value} {unit}", "" if ci is None else f"[{ci[0]}, {ci[1]}]", control,
                    verdict, "", "-", f"results/fake/{m}_{f}/summary.json"])  # fmt: skip
    return out.getvalue()


@pytest.fixture(scope="module")
def tab() -> dict[tuple[str, str], SS.Cell]:
    cells, _ = RD.read_grid(synth_csv())
    return SS.table(cells)


def miss(c: SS.Cell) -> list[tuple[str, str, int | None]]:
    return [(s.setting, s.state, s.n) for s in c.misses]


# ---------------------------------------------------------------- states


def test_rows_cover_every_finding_and_state():
    assert {f for r in SS.ROWS for f in r.findings} == {f.key for f in G.FINDINGS}
    assert set(SS.SHOWN) == set(RD.STATES) and set(SS.SHOWN.values()) < set(SS.STATES)
    assert [r.key for r in SS.MAIN_ROWS] == ["f3", "f4", "f5", "f6a", "lens", "f7", "f28", "f1"]  # <= 8 rows
    assert [SS.GROUPS[r.group] for r in SS.MAIN_ROWS] == ["How a lookup works"] * 4 + ["What the J-space carries"] * 4
    assert set(PS.VERDICT_COLOR) == {"holds", "fails", "≈ chance", "can't tell", "not tested", "descriptive"}
    assert C.VERDICT_COLOR is PS.VERDICT_COLOR


def test_at_chance(tab):
    c = tab[("f4", "27b")]  # 2 settings hold, the long context misses the bar at chance (its lower bound = chance)
    assert (c.state, c.held, c.judged) == ("holds", 2, 3)
    assert miss(c) == [("long context", "≈ chance", 178)]
    g = tab[("f4", "gemma")]  # two at chance, one holds: the cell is at chance, not "fails"
    assert (g.state, g.held, g.judged) == ("≈ chance", 1, 3)
    o = tab[("f4", "olmo")]  # misses the bar above chance: a real fail; one holds, one fails: a tie is not a hold
    assert (o.state, o.held, o.judged) == ("fails", 1, 2)
    assert SH.full_text(c)[1] == "long ctx ≈ chance"


def test_majority_without_mixed(tab):
    m = tab[("f3", "muse")]  # 2 of 3 hold; the failing prose has 5 items
    assert (m.state, m.held, m.judged) == ("holds", 2, 3) and miss(m) == [("prose", "fails", 5)]
    assert SH.full_text(m) == ["holds 2/3", "prose fails (5 items)"]
    f5 = tab[("f5", "32b")]  # draw 2's parts disagree: that setting does not hold; 1 of 2: a tie, fails
    assert (f5.state, f5.held, f5.judged) == ("fails", 1, 2)
    assert tab[("f3", "27b")].state == "holds"  # the beside lens's "fails" is not read


def test_finding_6_is_two_rows(tab):
    assert (tab[("f6a", "9b")].state, tab[("f6a", "9b")].judged) == ("holds", 1)
    assert (tab[("f6b", "9b")].state, tab[("f6b", "9b")].held, tab[("f6b", "9b")].judged) == ("fails", 0, 2)
    assert SS.ROW["f6a"].main and not SS.ROW["f6b"].main


def test_lens_gate_is_descriptive(tab):
    assert tab[("lens", "27b")].state == "at its word only"
    assert tab[("lens", "32b")].state == "at and after its word"
    assert tab[("lens", "olmo")].state == "not at its word"
    nt = tab[("lens", "olmo_hybrid")]
    assert (nt.state, nt.why) == ("not tested", "no lens")
    assert SH.fill(tab[("lens", "27b")]) == PS.VERDICT_COLOR["descriptive"]


def test_finding_7_main_rule_and_dagger(tab):
    c = tab[("f7", "27b")]  # main rule: inconclusive (draw 1) and holds (draw 2); the amended rule holds on draw 1
    assert (c.state, c.held, c.judged, c.amended_differs) == ("holds", 1, 1, True)
    assert SH.full_text(c) == ["holds 1/1 †"] and SH.main_text(c) == ["holds"]
    assert not tab[("f7", "9b")].amended_differs  # both rules agree
    assert (tab[("f7", "32b")].state, tab[("f7", "32b")].why) == ("not tested", "still running")
    assert tab[("f7", "gemma")].why == "still running"  # waits on a run (a failed one is requeued): readme_build


def test_findings_2_and_8_merged_worse(tab):
    c = tab[("f28", "122b")]  # 2 fails, 8 holds: fails, counted over both
    assert (c.state, c.held, c.judged) == ("fails", 1, 2)
    assert tab[("f28", "9b")].state == "holds"  # 8 can't tell: 2's holds stands


def test_zach_only_where_the_grid_has_no_verdict(tab):
    assert (tab[("f1", "9b")].state, tab[("f1", "9b")].zach) == ("holds (Zach)", "holds")
    assert (tab[("f1", "muse")].state, tab[("f1", "muse")].zach) == ("holds (Zach)", "holds-ish")
    assert (tab[("f1", "27b")].state, tab[("f1", "27b")].zach) == ("holds", "")  # his verdict file is in the grid
    c = tab[("f1", "122b")]  # not in his plan: the animal suite has no rule
    assert (c.state, c.why) == ("can't tell", "no rule (values only)")
    assert SH.fill(tab[("f1", "9b")]) == PS.VERDICT_COLOR["holds"]


# ---------------------------------------------------------------- the figure


@pytest.fixture(scope="module")
def drawn(tmp_path_factory):
    d = tmp_path_factory.mktemp("grid_20990101T000000Z")
    (d / "grid.csv").write_text(synth_csv())
    out = d / "out"
    paths = {kind: SH.summary_heatmap(d, kind, out) for kind in ("main", "full")}  # common.save: no overlap or raise
    return d, out, paths


def test_both_versions_save_without_overlap(drawn):
    _, out, paths = drawn
    for kind, (png, svg) in paths.items():
        assert png.name == f"summary_heatmap_{kind}.png" and svg.exists()
        h, w = mpimg.imread(png).shape[:2]
        assert w == 2400 and h == (1350 if kind == "main" else 2100)
        data = json.loads((out / "data" / f"summary_heatmap_{kind}.json").read_text())
        rows = SS.MAIN_ROWS if kind == "main" else SS.ROWS
        assert len(data) == len(rows) * len(C.MODELS)
        assert all(d["source"] == "summary_states" and d["finding"] is None for d in data)  # check_numbers skips


def test_figure_text(drawn):
    d, _, _ = drawn
    cells, _ = RD.read_grid((d / "grid.csv").read_text())
    for kind, rows in (("main", SS.MAIN_ROWS), ("full", SS.ROWS)):
        tab = SS.table(cells, rows)
        fr = SH.draw(tab, rows, kind, d.name)
        texts = {t.get_text().replace("\n", " ") for t in fr.fig.findobj(Text)}
        assert SH.TITLE in texts  # on two lines, broken at a space
        assert {m.short for m in C.MODELS} <= texts
        assert {"How a lookup works", "What the J-space carries", "Hybrids", "Attention-only"} <= texts
        cap = next(t.get_text() for t in fr.fig.texts if t.get_gid() == "caption")
        assert cap.count("\n") <= 1 and f"Grid {d.name}." in cap
        assert "Not tested: Olmo-Hybrid (no lens)" in cap and "(Zach)" in cap and "“holds-ish”" in cap
        if kind == "main":  # three failing claims and their models do not fit two lines with the rest: models only
            assert SH.failures(tab, rows) == ["late read (OLMo-3)", "order label (32B)", "lens part (122B)"]
            assert "Fails: 122B, 32B, OLMo-3." in cap  # in the models' order
            assert not any("†" in t for t in texts)  # MAIN: states only
        else:
            assert any("†" in t for t in texts)
        for t in fr.fig.texts + fr.axes[0].texts:
            assert float(t.get_fontsize()) >= 14, t.get_text()
        plt.close(fr.fig)
