"""cross_model_figures on SYNTHETIC data only: fake grid rows (every model, every cell a figure reads, with
not-interpretable, not-testable and missing cells) and a fake source of the extra numbers and curves. No result file
is opened here: the night's runs stay unread until Dan's predictions are in.

Checks: every figure renders at 16:9 to PNG and SVG under the names the brief asks for; every model appears in every
figure (none dropped silently); the three label kinds are drawn; the decisive comparison (the contrast panel, the
joined pair, the layer gap) with small differences beside large ones; no text below 14 pt, no internal code, a halo on
every printed value; zero overlapping texts, also with longer model names; the overlap check itself and its masking;
the status log prints no value; the pure helpers (roles by layer, the best valid push cell per layer). The summary
heatmap on a synthetic grid.csv: its states and counts (readme_draft's rule, findings 2 and 8 merged, the beside lens
and breakdown rows ignored), its title, the figure without overlaps, and the command line."""

from __future__ import annotations

import csv
import dataclasses
import io
import random
import re
from typing import Any

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pytest
from matplotlib.patches import Rectangle
from matplotlib.text import Text

from bridge_jspace import plot_style as S
from scripts import cross_model_figures as F
from scripts import cross_model_grid as G
from scripts import readme_draft as RD

EXPECTED = {
    "f_late_read_all_models", "f_digit_not_name_all_models", "f_order_then_identity_all_models",
    "f_counts_list_order_not_text_all_models", "f_patch_outcomes_by_depth_all_models",
    "f_lookup_ignores_lens_part_all_models", "f_lens_push_recall_not_lookup_all_models",
    "f_layer_gap_lens_vs_patch_27b",
}  # fmt: skip
CODES = re.compile(r"\b(D[1-9]|C[1-9]|D3b|v2\.1|pointer_v\d|BL|BR|RL|RR|PP|PM|MP|H-gap|H-around)\b")

# ---------------------------------------------------------------- the synthetic fixture

SETTINGS = {  # finding -> grid.md settings the figures read
    "f4": ("prose", "table", "JSON", "long context"),
    "f3": ("prose", "table", "JSON"),
    "f5": ("draw 1", "8 sentences", "12 sentences"),
    "f6": ("filler moved", "one statement more", "one statement fewer"),
    "f2": ("draw 1", "draw 2"),
    "gate": ("v1 (at the word)", "v2 (after the word)"),
    "f7": ("main rule", "amended rule"),
}
LENS_FINDINGS = ("f2", "gate", "f7")
# (model, finding, setting) -> (verdict, status): the label cases, real verdict wordings of cross_model_grid
SPECIAL = {
    ("muse", "f5", "draw 1"): ("not interpretable (the random-patch control breaks 41% of answers, above 30%)", "has-run"),
    ("muse", "f6", "filler moved"): ("not interpretable (the random-patch control breaks 41% of answers, above 30%)",
                                     "has-run"),
    ("gemma", "f4", "long context"): ("missing (spec gemma4it_d2_late_read_long not run (not in the queue or the "
                                      "ledger))", "not enqueued"),
    ("122b", "f7", "main rule"): ("not interpretable (the off-path check failed at the decisive cell; reading there: "
                                  "H-around)", "has-run"),
    ("122b", "f2", "draw 1"): ("missing (no spec)", "no spec"),
    ("32b", "f2", "draw 2"): ("missing (no spec)", "no spec"),
    ("olmo", "f3", "JSON"): ("not interpretable (the off-path control: an off-path sentence's part hidden keeps < 90%)",
                             "has-run"),
    ("olmo", "gate", "v1 (at the word)"): ("fails", "has-run"),
    ("9b", "f5", "12 sentences"): ("missing (job qwen35_9b_d3v5_len12_swap failed at the run stage (exit 1))",
                                   "failed"),
    ("32b", "f6", "one statement fewer"): ("not testable (no swept layer before the donor's digit arrives)", "has-run"),
    ("27b", "f4", "table"): ("fails (more than 20% right, or the upper bound above 30%)", "has-run"),
    # two labelled cells in adjacent rows of one panel
    ("32b", "f4", "JSON"): ("missing (spec qwen3_32b_d2_formats not run (not in the queue or the ledger))",
                            "not enqueued"),
    ("olmo", "f4", "JSON"): ("missing (job olmo3_7b_instruct_d2_formats failed at the run stage (exit 1))", "failed"),
    ("gemma", "f2", "draw 2"): ("not interpretable (lookups keep their answer under the lens-part patch on < 80%)",
                                "has-run"),
    ("olmo", "f7", "main rule"): ("inconclusive (the rule's reading: the lookup moves between 10% and 30%)", "has-run"),
    ("muse", "f7", "main rule"): ("missing (muse30b_d4_where is pending in the queue)", "pending"),
    ("muse", "f7", "amended rule"): ("missing (muse30b_d4_where is pending in the queue)", "pending"),
}  # fmt: skip
VALUE_AT = {"f4": 0.08, "f3": 0.22, "f5": 0.4, "f6": 0.55, "f2": 0.04, "gate": 0.7, "f7": 0.03}
# small differences beside the large ones, so that both are checked to read clearly (grid value; the other arm in
# FakeSource): 6% vs 10%, 34% vs 40%, 6% vs 2%, 2% vs 6%, 12% vs 8%
SMALL = {("olmo_hybrid", "f4", "JSON"): 0.06, ("muse", "f3", "prose"): 0.34, ("olmo", "f6", "filler moved"): 0.06,
         ("9b", "f2", "draw 2"): 0.02, ("32b", "gate", "v2 (after the word)"): 0.12}  # fmt: skip
OTHER_ARM = {("olmo_hybrid", "f4", "JSON"): 0.10, ("muse", "f3", "prose"): 0.40, ("olmo", "f6", "filler moved"): 0.02,
             ("9b", "f2", "draw 2"): 0.06, ("32b", "gate", "v2 (after the word)"): 0.08}  # fmt: skip


def other_arm(row: dict) -> float | None:
    return OTHER_ARM.get((row["model"], row["finding"], row["setting"]))


def fake_rows(seed: int = 0) -> list[dict]:
    """grid.json rows as cross_model_grid writes them (main lens, one per grid.md cell), all synthetic."""
    rng = random.Random(seed)
    rows = []
    for m in S.MODELS:
        for f, settings in SETTINGS.items():
            for s in settings:
                verdict, status = SPECIAL.get((m.key, f, s), ("holds", "has-run"))
                if m.key == "olmo_hybrid" and f in LENS_FINDINGS:
                    verdict, status = "not testable (no lens)", "no lens"
                row: dict[str, Any] = {"model": m.key, "finding": f, "setting": s, "md_setting": s, "role": "main",
                                       "run": f"fake_{m.key}_{f}", "verdict": verdict, "status": status,
                                       "path": "results/fake/summary.json", "n": None, "value": None, "ci": None,
                                       "control": ""}  # fmt: skip
                if status == "has-run" and not verdict.startswith("not testable"):
                    v = SMALL.get((m.key, f, s), min(0.98, max(0.0, VALUE_AT[f] + rng.uniform(-0.05, 0.08))))
                    w = 0.02 if (m.key, f, s) in SMALL else 0.06
                    row.update(n=rng.choice((80, 150, 300)), value=v, ci=[max(0.0, v - w), min(1.0, v + w)])
                    row["control"] = "position - identity +40, A: True; layer 50 (saved verdict)" if f == "f5" else ""
                rows.append(row)
        # the finding-5 grid row of the 3rd-on part: csv only (md_setting None), never read by the figures
        rows.append({"model": m.key, "finding": "f5", "setting": "draw 1, 3rd on", "md_setting": None,
                     "role": "main", "verdict": "holds", "status": "has-run", "value": -0.9})  # fmt: skip
    rows.append({**rows[0], "role": "plain J-lens", "value": 0.99})  # a lens listed beside: ignored by the figures
    return rows


def t(p: float, w: float = 0.06) -> tuple[float, float, float]:
    return (p, max(0.0, p - w), min(1.0, p + w))


class FakeSource:
    """The extra numbers and curves, synthetic, in the shapes FileSource returns."""

    def __init__(self, seed: int = 0, gap: bool = True):
        self.rng = random.Random(seed)
        self.gap = gap

    def late_arms(self, row: dict) -> dict[str, tuple[float, float, float] | None]:
        hybrid = S.MODEL[row["model"]].hybrid
        small = other_arm(row)
        dn = small if small is not None else 0.55 if (row["model"], row["setting"]) == ("9b", "prose") else 0.95
        return {"off": t(0.94, 0.03), "deltanet": t(dn, 0.02 if small else 0.04) if hybrid else None}

    def name_digit(self, row: dict) -> dict[str, tuple[float, float, float]]:
        small = other_arm(row)
        digit = small if small is not None else 0.86 + self.rng.uniform(-0.1, 0.08)
        return {"name": t(row["value"]), "digit": t(digit, 0.02 if small else 0.06)}

    def order_by_k(self, row: dict) -> dict[str, Any]:
        n_sent = {"draw 1": 5, "8 sentences": 8, "12 sentences": 12}[row["setting"]]
        ks = list(range(1, n_sent + 1))
        diff = [t((0.45 if k <= 2 else -0.35) + self.rng.uniform(-0.12, 0.12), 0.15) for k in ks]
        return {"k": ks, "diff": diff, "n": 60 * n_sent, "first2": row["value"]}

    def counting(self, row: dict) -> dict[str, tuple[float, float, float]]:
        rivals = next(rv for s, _, _, rv in G.V4X if s == row["setting"])
        small = other_arm(row)
        if small is not None:
            return {G.RIVAL[r]: t(small, 0.015) for r in rivals}
        return {G.RIVAL[r]: t(0.08 + self.rng.uniform(0, 0.12)) for r in rivals}

    def stated_bridge(self, row: dict) -> dict[str, Any]:
        small = other_arm(row)
        recall = t(small, 0.02) if small is not None else t(0.63)
        return {"lookup_lens": (row["value"], *row["ci"]), "lookup_rest": t(0.72), "lookup_n": row["n"],
                "recall_lens": recall, "recall_n": 80, "lookup_null": t(0.01, 0.01), "recall_null": t(0.03, 0.02)}  # fmt: skip

    def gate_other(self, row: dict) -> tuple[float, float, float]:
        small = other_arm(row)
        return t(small, 0.02) if small is not None else t(0.09)

    def outcomes_by_depth(self, row: dict) -> dict[str, Any]:
        nl = F.n_layers(row["model"])
        layers = list(range(0, nl - 3, 2))
        pos, ide, val = [], [], []
        for la in layers:
            d = la / nl
            pos.append(t(max(0.0, 0.6 - 4 * (d - 0.65) ** 2 * 6), 0.05))
            ide.append(t(max(0.0, 0.25 - 3 * (d - 0.72) ** 2 * 6), 0.04))
            val.append(t(min(1.0, max(0.0, (d - 0.78) * 4)), 0.04))
        return {"layers": layers, "position": pos, "identity": ide, "value": val, "n": 300, "n_layers": nl,
                "used": round(0.75 * nl)}  # fmt: skip

    def push_by_layer(self, row: dict) -> dict[str, Any]:
        nl = F.n_layers(row["model"])
        layers = [round(nl * x / 64) for x in (12, 16, 20, 24, 28, 32, 36, 40, 44)]
        lookup, recall, rnd = [], [], []
        edge = row["model"] == "gemma"  # values at the axis ends at the main cell: 0% and 99%
        for i, _ in enumerate(layers):
            valid = i != 2  # one layer without a valid cell
            lookup.append((t(0.0, 0.01) if edge else t(0.25, 0.03)) if i == 1 else t(0.02, 0.03) if valid else None)
            recall.append((t(0.99, 0.01) if edge and i == 1 else t(0.85 - 0.08 * i, 0.06)) if valid else None)
            rnd.append(t(0.01, 0.01) if valid else None)
        return {"layers": layers, "lookup": lookup, "recall": recall, "random": rnd, "n_layers": nl,
                "main": layers[1], "amended": layers[3]}  # fmt: skip

    def layer_gap(self) -> dict[str, Any] | None:
        if not self.gap:
            return None
        layers = list(range(12, 35, 2))
        out: dict[str, Any] = {"n": 100, "subsets": {}}
        for sub, shift in (("w", 0), ("s", 2)):
            out["subsets"][sub] = {
                "layers": layers,
                "lens": [t(0.3 if la < 18 + shift else 0.01, 0.04) for la in layers],
                "patch": [t(0.9 if la < 28 + shift else 0.02, 0.05) for la in layers],
                "embed": [t(0.25 if la < 18 + shift else 0.0, 0.04) if la != 24 else None for la in layers],
                "random": [t(0.01, 0.01) for _ in layers],
                "stops": {"lens": 18 + shift, "patch": 28 + shift, "embed": 18 + shift},
                "verdict": "H-gap" if sub == "w" else "inconclusive",
            }
        return out


@pytest.fixture(scope="module")
def rendered():
    grid, src = F.Grid(fake_rows()), FakeSource()
    out = {name: F.render(name, grid, src) for name in F.FIGURES}
    yield out
    for r in out.values():
        plt.close(r.fig)


def texts(fig) -> list[Text]:
    return [x for x in fig.findobj(Text) if x.get_visible() and x.get_text().strip()]


# ---------------------------------------------------------------- the figures


def test_file_names_say_the_claim():
    assert set(F.FIGURES) == EXPECTED
    for name in F.FIGURES:
        assert re.fullmatch(r"f_[a-z0-9_]+", name), name
        assert not re.search(r"(^|_)(fig\d|d\d|v\d)(_|$)", name), name


def test_every_figure_renders_png_and_svg_at_16_9(tmp_path, rendered):
    for name, r in rendered.items():
        paths = S.save(r.fig, tmp_path, name)
        assert [p.name for p in paths] == [f"{name}.png", f"{name}.svg"]
        h, w = mpimg.imread(paths[0]).shape[:2]
        assert abs(w / h - 16 / 9) < 0.01, (name, w, h)
        assert w >= 1920, (name, w)
        assert paths[1].read_text().lstrip().startswith("<?xml"), name


def test_every_model_appears_in_every_figure(rendered):
    for name, r in rendered.items():
        if name in F.ONE_MODEL:  # the 27B's layer-gap test: one model by design
            assert "Qwen3.6-27B" in F.FIGURES[name].spec.subtitle
            continue
        drawn = {x.get_text() for x in texts(r.fig)}
        for m in S.MODELS:
            assert m.label in drawn, (name, m.label)
        if isinstance(r.data, F.DotData):  # a mark (value or label) for every model in every panel
            assert {(p, m.key) for p in r.data.panels for m in S.MODELS} <= set(r.data.marks), name
        else:
            assert set(r.data.panels) == {m.key for m in S.MODELS}, name


def test_label_kinds_are_drawn(rendered):
    late = rendered["f_late_read_all_models"]
    assert late.data.marks[("long context", "gemma")].status == "missing"
    assert late.data.marks[("long context", "gemma")].reason == "not run"
    assert late.data.marks[("table", "27b")].status == "value"  # a failing cell is drawn with its value
    assert set(late.data.marks[("prose", "27b")].points) == {"attn", "deltanet", "off"}  # the hybrids' DeltaNet arm
    assert set(late.data.marks[("prose", "32b")].points) == {"attn", "off"}
    drawn = {x.get_text() for x in texts(late.fig)}

    def labelled(texts_: set[str], status: str, reason: str) -> bool:  # "status: reason" or "status" over "reason"
        return any(t.replace("\n", ": ") == f"{status}: {reason}" for t in texts_)

    assert labelled(drawn, "missing", "not run")
    assert labelled(drawn, "missing", "run failed")  # the row next to it: both labels on one line each
    assert "6 vs 10%" in drawn  # the small gap (Olmo-Hybrid, JSON): both arms in one label beside the pair
    nd = rendered["f_digit_not_name_all_models"]
    assert nd.data.marks[("JSON", "olmo")].status == "not interpretable"
    # a hatched cell: "not interpretable: reason" where it fits, else the reason alone (the hatch says the rest)
    assert any(t.endswith("off-path control") for t in {x.get_text() for x in texts(nd.fig)})
    assert any(isinstance(p, Rectangle) and p.get_hatch() for ax in nd.fig.axes for p in ax.patches)
    lens = rendered["f_lookup_ignores_lens_part_all_models"]
    for panel in lens.data.panels:
        assert lens.data.marks[(panel, "olmo_hybrid")].status == "not testable"
    assert "not testable: no lens" in {x.get_text() for x in texts(lens.fig)}  # once across the row
    push = rendered["f_lens_push_recall_not_lookup_all_models"].data
    assert push.panels["olmo_hybrid"].status == "not testable"
    assert push.panels["muse"].status == "missing" and push.panels["muse"].reason == "queued"
    assert push.panels["122b"].status == "not interpretable" and push.panels["122b"].series  # hatched, curves kept


def test_stated_bridge_draw_is_chosen_by_the_plan_not_the_result(rendered):
    lens = rendered["f_lookup_ignores_lens_part_all_models"].data
    assert lens.marks[("contrast", "32b")].note == "draw 1"  # no draw 2 planned
    assert lens.marks[("contrast", "122b")].note == ""  # draw 2 planned
    gemma = lens.marks[("contrast", "gemma")]  # draw 2 not interpretable: never replaced by draw 1
    assert gemma.status == "not interpretable"
    assert lens.marks[("lens part", "gemma")].status == "value"  # the failed control's own numbers stay visible


def test_the_contrast_is_the_main_panel(rendered):
    r = rendered["f_lookup_ignores_lens_part_all_models"]
    assert r.data.panels[0] == "contrast"
    # recalls 6% minus lookups 2% (the fixture's rates are not k/n, so the counts behind them round a little)
    small = r.data.marks[("contrast", "9b")].points["contrast"]
    assert small[0] == pytest.approx(0.04, abs=0.01) and small[1] < small[0] < small[2]
    drawn = {x.get_text() for x in texts(r.fig)}
    assert {"+4", "2 vs 6%"} <= drawn
    big = r.data.marks[("contrast", "27b")].points["contrast"]
    assert big[1] > 0.3  # recalls 63% vs lookups a few %: the interval far from zero


def test_newcombe_matches_pointer_swap():
    from scripts import pointer_swap as PS

    got = F.newcombe((0.6, 0.5, 0.7), 80, (0.05, 0.02, 0.1), 80)
    assert got == pytest.approx(PS.newcombe(48, 80, 4, 80))


def test_order_curves_note_missing_lists(rendered):
    order = rendered["f_order_then_identity_all_models"].data
    nine = order.panels["9b"]
    assert nine.status == "value"
    assert "12: missing (run failed)" in nine.notes
    assert [s.key for s in nine.series if s.y] == ["5", "8"]
    muse = order.panels["muse"]
    assert muse.series[0].status == "not interpretable" and muse.series[0].y  # drawn faded, with a note
    assert any(n.startswith("5: not interpretable") for n in muse.notes)


def test_layer_gap_shows_the_gap_or_a_label():
    r = F.render("f_layer_gap_lens_vs_patch_27b", F.Grid(fake_rows()), FakeSource())
    assert "+10 layers" in {x.get_text() for x in texts(r.fig)}  # the stops 18 and 28, the decisive comparison
    plt.close(r.fig)
    r = F.render("f_layer_gap_lens_vs_patch_27b", F.Grid(fake_rows()), FakeSource(gap=False))
    assert isinstance(r.data, F.CurveData)
    assert {p.status for p in r.data.panels.values()} == {"missing"}
    assert "missing\nnot run or not pulled" in {x.get_text() for x in texts(r.fig)}
    plt.close(r.fig)


def test_text_is_slide_sized_and_plain(rendered):
    for name, r in rendered.items():
        for x in texts(r.fig):
            assert float(x.get_fontsize()) >= S.FONT, (name, x.get_text(), x.get_fontsize())
            assert not CODES.search(x.get_text()), (name, x.get_text())
            if x.get_gid() == "value":  # a white halo keeps every printed value legible over lines and hatching
                assert x.get_path_effects(), (name, x.get_text())
        for ax in r.fig.axes:
            assert ax.get_legend() is None
        for leg in r.fig.legends:
            for x in leg.get_texts():
                assert float(x.get_fontsize()) >= S.FONT, (name, x.get_text())


def test_zero_overlaps_on_the_synthetic_figures(rendered):
    for name, r in rendered.items():
        assert r.overlaps == [], (name, r.overlaps)
        assert S.overlaps(r.fig) == [], name


def test_zero_overlaps_with_long_names_and_close_values(monkeypatch):
    """Longer model names (" Instruct" added) and the fixture's close pairs (6 vs 10%, 2 vs 6%, 12 vs 8%): the
    layout steps still end with no text on another."""
    long = tuple(dataclasses.replace(m, label=f"{m.label} Instruct") for m in S.MODELS)
    monkeypatch.setattr(S, "MODELS", long)
    monkeypatch.setattr(S, "MODEL", {m.key: m for m in long})
    grid, src = F.Grid(fake_rows()), FakeSource()
    for name in F.FIGURES:
        r = F.render(name, grid, src)
        assert r.overlaps == [], (name, r.step, r.overlaps)
        plt.close(r.fig)


def test_overlap_check_finds_collisions_and_masks_values():
    fig = plt.figure(figsize=S.FIGSIZE)
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.5, 0.5, "a title", fontsize=20)
    ax.text(0.5, 0.5, "37%", fontsize=20, gid="value")
    ax.text(0.98, 0.5, "far too long a label for its place", gid="status")
    ax.plot([0.2], [0.2], marker="o", markersize=10, gid="mark")  # a value label on its own marker
    ax.text(0.2, 0.2, "4%", gid="value")
    ax.plot([0.1, 0.4], [0.8, 0.8], lw=6, gid="gap")  # a value label on the gap bar
    ax.text(0.25, 0.8, "5 vs 9%", gid="value")
    ax.plot([0.7], [0.2], marker="o", markersize=10, gid="mark")  # a free label beside a marker: fine
    ax.text(0.73, 0.2, "8%", gid="value")
    found = S.overlaps(fig, mask=True)
    assert ("'a title'", "<value>") in found
    assert ("<status>", "outside its panel") in found
    assert ("<value>", "a mark") in found and ("<value>", "a gap") in found
    assert sum(b in ("a mark", "a gap") for _, b in found) == 2
    assert not any("37" in a or "37" in b for a, b in found)  # a masked report never prints the value
    plt.close(fig)


def test_the_decisive_value_is_labelled_on_every_row(rendered):
    """Every row with a value has its decisive arm's number printed in each panel with a decisive pair (alone, or
    joined with its comparison as '6 vs 10%')."""
    for name, r in rendered.items():
        spec = F.FIGURES[name].spec
        if not isinstance(spec, F.DotSpec):
            continue
        assert isinstance(r.data, F.DotData)
        for ax, ps in zip(r.fig.axes, spec.panels, strict=True):
            rows = sum(r.data.marks[(ps.key, m.key)].status == "value" for m in S.MODELS)
            values = sum(t.get_gid() == "value" for t in ax.texts)
            assert values >= rows, (name, ps.key, values, rows)


def test_titles_state_the_outcome(rendered):
    assert rendered["f_late_read_all_models"].title.endswith("except the 27B (tables)")
    assert "not on" not in rendered["f_lookup_ignores_lens_part_all_models"].title  # every judged model holds
    assert "on the 27B" in rendered["f_lens_push_recall_not_lookup_all_models"].title


def test_status_log_prints_no_values(rendered):
    for name, r in rendered.items():
        lines = F.status_line(name, r)
        assert lines[0].startswith(f"figure {name}: 0 overlaps"), lines[0]
        for line in lines:
            assert "%" not in line and not re.search(r"\d\.\d", line), line
            assert not any(w in line for w in ("holds", "fails", "inconclusive", "interpretable", "testable")), line


def test_short_reasons_from_the_grid_wording():
    cases = {
        "missing (spec x not run (not in the queue or the ledger))": "not run",
        "missing (the parts ran but no saved verdict: scripts/d1_verdict.py not run on it)": "no verdict yet",
        "missing (no amended-rule analysis: early_push_where analyze --rule v2.1 not run)": "not analyzed",
        "missing (x is pending in the queue)": "queued",
        "not testable (gate v1 failed (qwen3_32b_lens_gate))": "lens gate failed",
        "not interpretable (no cell where the lens push writes recall: the positive control fails)": "positive control",
        "not interpretable (G2: a control removal keeps < 90% on BL)": "removal control",
        "not interpretable (something new)": "a control failed",
    }
    for verdict, short in cases.items():
        assert F.short_reason(F.word(verdict), verdict) == short, verdict


# ---------------------------------------------------------------- the pure helpers FileSource uses


def test_roles_by_layer_shares_and_filters():
    rows = [{"source": "dissoc", "group": "last", "family": "RL", "level": "e5f0", "layer": la, "role": role}
            for la, roles in ((10, ("position", "position", "identity", "none")), (12, ("value", "value")))
            for role in roles]  # fmt: skip
    rows += [{"source": "rand", "group": "last", "family": "RL", "level": "e5f0", "layer": 10, "role": "value"},
             {"source": "dissoc", "group": "last", "family": "RL", "level": "e5f0", "layer": "transit", "role": "value"}]  # fmt: skip
    got = F.roles_by_layer(rows)
    assert got["layers"] == [10, 12] and got["n"] == 4
    assert got["position"][0][0] == 0.5 and got["identity"][0][0] == 0.25 and got["value"][1][0] == 1.0


def test_best_valid_by_layer_picks_the_most_recall_among_valid_cells():
    def cell(k: int, n: int = 10) -> dict[str, str]:
        return {f"i{i}": "b" if i < k else "A" for i in range(n)}

    cells: dict[tuple, dict[str, str]] = {}
    for sub, br, valid in (("w", 6, True), ("s", 9, False)):  # the sentence switches more recalls but is not valid
        cells[("BR", sub, 20, 8.0, "lens")] = cell(br)
        cells[("BL", sub, 20, 8.0, "lens")] = cell(1)
        cells[("RL", sub, 20, 8.0, "lens")] = {f"i{i}": "A" if valid or i > 3 else "b" for i in range(10)}
    cells[("BR", "w", 24, 8.0, "lens")] = cell(5)
    cells[("RR", "w", 24, 8.0, "lens")] = cell(5)  # off the path changed 50%: not valid
    got = F.best_valid_by_layer(cells, [20, 24], [8.0])
    assert got["recall"][0][0] == 0.6 and got["lookup"][0][0] == 0.1
    assert got["recall"][1] is None and got["lookup"][1] is None


# ---------------------------------------------------------------- the summary heatmap, on a synthetic grid.csv

MAIN_LENS = "J++, synthetic, 00000000"
# (model, finding, grid.csv setting, verdict, n); every other model and finding has no row (missing)
SYNTH = (
    ("27b", "f3", "draw 1", "holds", 300), ("27b", "f3", "draw 2", "holds", 300),
    ("27b", "f3", "prose", "fails (the name hidden leaves > 35% right)", 20),  # mixed; its only failure has n < 30
    ("27b", "f4", "draw 1", "fails", 300), ("27b", "f4", "draw 2", "holds", 300), ("27b", "f4", "table", "fails", 20),
    ("27b", "f5", "draw 1", "holds", 300), ("27b", "f5", "draw 1, 3rd on", "holds", 400),
    ("27b", "f5", "draw 2", "fails", 300), ("27b", "f5", "draw 2, 3rd on", "holds", 400),  # draw 2: mixed parts
    ("27b", "f6", "filler moved", "holds", 400), ("27b", "f6", "one statement more", "holds", 400),
    ("27b", "gate", "v1 (at the word)", "holds", 60), ("27b", "gate", "v2 (after the word)", "fails", 60),
    ("27b", "f7", "main rule", "inconclusive (the lookup moves between 10% and 30%)", 100),
    ("27b", "f7", "amended rule", "holds", 100),
    ("27b", "f2", "draw 1", "holds", 120), ("27b", "f2", "draw 2", "holds", 180),
    ("27b", "f8", "stated bridge, draw 1", "fails", 120),  # findings 2 and 8 disagree: the worse is shown
    ("27b", "f1", "animal suite", "open (descriptive, no committed rule)", 400),
    ("27b", "f1", "animal suite · lookup, bridge stated", "fails", 100),  # a breakdown row: not judged
    ("9b", "f3", "draw 1", "holds", 300),
    ("9b", "f2", "draw 2", "holds", 180),
    ("9b", "f8", "stated bridge, draw 2", "not interpretable (no recall written)", 180),  # holds beats can't tell
    ("9b", "f1", "animal suite", "not testable (no lens)", None),
    ("olmo", "f2", "table", "not testable (gate v1 failed)", None),
    ("olmo", "f8", "last tokens", "open (values only)", 250),  # values only beats not testable
)  # fmt: skip
BESIDE_ROW = ("27b", "f6", "one statement fewer", "fails", 400)  # another lens, listed beside: never read


def synth_csv(rows=SYNTH, beside=(BESIDE_ROW,)) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for (m, f, s, verdict, n), lens in [*((r, MAIN_LENS) for r in rows),
                                        *((r, "plain J-lens (synthetic, listed beside)") for r in beside)]:  # fmt: skip
        w.writerow([G.MODEL[m].label, G.FINDING[f].name, s, lens, "" if n is None else n, "" if n is None else "50.0 %",
                    "" if n is None else "[40.0, 60.0]", "", verdict, "", "-", f"results/fake/{m}_{f}/summary.json"])  # fmt: skip
    return out.getvalue()


def summary_table(rows=SYNTH) -> dict[tuple[int, str], F.SummaryCell]:
    cells, _ = RD.read_grid(synth_csv(rows))
    return F.summary_cells(cells)


def row_of(label: str) -> int:
    return next(i for i, r in enumerate(F.SUMMARY_ROWS) if r.label == label)


def test_summary_shows_every_state_of_the_committed_rule():
    assert set(F.SHOWN) == set(RD.STATES) and set(F.WORSE) == set(RD.STATES)
    assert set(F.SHOWN.values()) == set(S.STATE_FILL)
    assert [m.key for m in S.MODELS] == list(F.SUMMARY_NAMES)  # hybrids first, then attention-only
    assert {f for r in F.SUMMARY_ROWS for f in r.findings} == {f.key for f in G.FINDINGS}  # no finding left out


def test_summary_states_and_counts():
    tab = summary_table()

    def got(label: str, model: str) -> tuple[str, str, bool]:
        c = tab[(row_of(label), model)]
        return c.state, F.cell_label(c), c.few

    assert got("The last tokens read the answer's digit", "27b") == ("mixed", "✗ 2/3", True)  # failing only at n < 30
    assert got("The lookup ends in a late attention read", "27b") == ("mixed", "✗ 1/3", False)  # one failure n=300
    assert got("Order label, then the bridge's identity", "27b") == ("mixed", "✗ 1/2", False)  # settings, not parts
    assert got("The label counts list order", "27b") == ("holds", "✓ 2/2", False)  # the beside lens's fail ignored
    assert got("Lens reads the bridge at its word", "27b") == ("holds", "✓ 1/1", False)
    assert got("… after its word", "27b") == ("fails", "✗ 0/1", False)
    # the main rule's inconclusive is not judged
    assert got("A lens push writes recall, not the lookup", "27b") == ("holds", "✓ 1/1", False)
    assert got("The lookup ignores the lens-readable part", "27b") == ("fails", "✗ 2/3", False)  # 8 fails: the worse
    assert got("Removing the J-space spares the lookup", "27b") == ("values only", "?", False)  # breakdown row ignored
    assert got("The last tokens read the answer's digit", "9b") == ("holds", "✓ 1/1", False)
    assert got("The lookup ignores the lens-readable part", "9b") == ("holds", "✓ 1/1", False)
    assert got("Removing the J-space spares the lookup", "9b") == ("not testable", "–", False)
    assert got("The lookup ignores the lens-readable part", "olmo") == ("values only", "?", False)
    assert got("The last tokens read the answer's digit", "gemma") == ("missing", "–", False)
    assert len(tab) == len(F.SUMMARY_ROWS) * len(S.MODELS)


def test_summary_title_states_the_outcome():
    assert F.title_summary(summary_table()) == (
        "The lookup's route holds in 2 of 5 judged cells; the lens claims hold where judged on the 9B, not the 27B; "
        "the lens reads the bridge only at its word"
    )
    only_holds = [r for r in SYNTH if r[3] != "fails" and not r[3].startswith("fails")]
    title = F.title_summary(summary_table(only_holds))
    assert title.startswith("The lookup's route holds on every model tested; the lens claims hold where judged on ")
    assert title.endswith("; the lens reads the bridge at its word on 1 of 1 models")  # the read after: not judged
    assert F.title_summary(summary_table(())) == "The lookup's route is not judged on any model yet"


def test_summary_figure_renders_without_overlaps(tmp_path):
    (tmp_path / "grid.csv").write_text(synth_csv())
    s = F.render_summary(tmp_path)
    assert s.overlaps == [] and S.overlaps(s.fig) == []
    paths = S.save(s.fig, tmp_path / "out", F.SUMMARY)
    h, w = mpimg.imread(paths[0]).shape[:2]
    assert abs(w / h - 16 / 9) < 0.01 and w >= 1920
    drawn = [x for x in texts(s.fig)]
    flat = {re.sub(r"-\n", "-", x.get_text()).replace("\n", " ") for x in drawn}
    assert set(F.SUMMARY_NAMES.values()) <= flat  # every model, also those with no row (missing)
    assert {r.label for r in F.SUMMARY_ROWS} <= flat
    assert sum(x.get_gid() == "value" for x in drawn) == len(s.table)  # a text in every cell
    assert tmp_path.name in s.fig.texts[1].get_text().replace("\n", " ")  # the subtitle names the grid
    for x in drawn:
        assert float(x.get_fontsize()) >= S.FONT, x.get_text()
        assert not CODES.search(x.get_text()), x.get_text()
    for leg in s.fig.legends:
        assert all(float(x.get_fontsize()) >= S.FONT for x in leg.get_texts())
    ax = s.fig.axes[0]
    hatched = sum(bool(p.get_hatch()) for p in ax.patches)
    assert hatched == sum(c.state == "mixed" for c in s.table.values()) == 3
    corners = [ln for ln in ax.get_lines() if ln.get_gid() == "mark"]
    assert len(corners) == sum(c.few for c in s.table.values()) == 1
    plt.close(s.fig)


def test_summary_from_the_command_line(tmp_path):
    (tmp_path / "grid.csv").write_text(synth_csv())
    (tmp_path / "grid.json").write_text('{"rows": []}')
    assert F.main(["--grid", str(tmp_path), "--out", str(tmp_path / "out"), "--only", F.SUMMARY]) == 0
    assert {p.name for p in (tmp_path / "out").iterdir()} == {f"{F.SUMMARY}.png", f"{F.SUMMARY}.svg"}
