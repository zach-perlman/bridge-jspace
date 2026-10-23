"""scripts/figs/late_read and digit_not_name (findings 4 and 3) on a SYNTHETIC grid.csv: every figure saves without an
overlap error, and every number in its data file matches the grid (a cell's value: common.check_numbers; a control's
number from the cell's control text: late_read.control_mismatches). The exception sentences, the caption packing and
the control parsing on their own. On the real newest grid, the committed data files match it."""

from __future__ import annotations

import csv
import io
import json
import random
from pathlib import Path

import pytest

from bridge_jspace import plot_style as PS
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import digit_not_name as DN
from scripts.figs import late_read as LR

LENS = "none (lens-free)"
NI = "not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)"
OVER = "fails (more than 20% right, or the upper bound above 30%)"
DELTANET_FAIL = "fails (the DeltaNet layers matter: blocking them instead keeps < 90%)"
NOT_TESTABLE = "not testable (competence: no memory -> prompt item the model answers right unedited here)"
MISSING = "missing (no spec)"


def chance_of(setting: str) -> tuple[int, int]:
    return (33, 3) if setting in ("prose", "table", "JSON") else (20, 5)


def f4_control(model: str, setting: str, off: int = 100, dn: int = 100) -> str:
    ch, k = chance_of(setting)
    text = f"chance {ch}% ({k} listed answers); blocked in every attention layer; the off-path sentence hidden instead keeps {off}% [95, 100]"  # fmt: skip
    return text + (f"; hidden in every DeltaNet layer instead: {dn}%" if C.MODEL[model].hybrid else "")


def f3_control(setting: str, digit: int = 90, off: int = 99) -> str:
    ch, k = chance_of(setting)
    return (f"the digit left visible (the sentence without its digit hidden): {digit}% [{digit - 6}, {min(digit + 4, 100)}]; "
            f"off-path parts hidden (needs >= 90% at both places): lowest {off}%, the off-path sentence without its digit "
            f"hidden from the question's tokens; the question's tokens read the name: holds; chance {ch}% ({k} listed answers)")  # fmt: skip


# (model, finding, setting) -> (value, CI, n, verdict, control); every other cell of f3 / f4: holds, a value under
# chance with the interval [value - 5, value + 6]
SPECIAL = {
    ("gemma", "f4", "draw 1"): (24.0, "[19.0, 30.0]", 300, OVER, None),  # over the bar, covers chance 20: "≈ chance"
    ("gemma", "f4", "JSON"): (21.4, "[12.7, 33.8]", 56, OVER, None),  # covers chance 33
    ("27b", "f4", "long context"): (25.8, "[20.0, 32.7]", 178, OVER, None),
    ("olmo_hybrid", "f4", "table"): (0.0, "[0.0, 13.8]", 24, DELTANET_FAIL, f4_control("olmo_hybrid", "table", dn=88)),
    ("olmo", "f4", "prose"): (0.0, "[0.0, 17.6]", 18, NI, f4_control("olmo", "prose", off=89)),
    ("muse", "f4", "table"): (None, "", 0, NOT_TESTABLE, ""),
    ("gemma", "f4", "long context"): (None, "", None, MISSING, ""),
    ("27b", "f4", "draw 3"): (None, "", None, MISSING, ""),
    ("gemma", "f3", "draw 1"): (27.7, "[22.9, 33.0]", 300, "holds", None),  # holds, above chance
    ("muse", "f3", "prose"): (40.0, "[11.8, 76.9]", 5, "fails", None),
    ("olmo_hybrid", "f3", "JSON"): (0.0, "[0.0, 21.5]", 14, NI, f3_control("JSON", off=86)),
    ("muse", "f3", "table"): (None, "", 0, NOT_TESTABLE, ""),
}


def synth_csv(seed: int = 0, special: dict | None = None) -> str:
    rng = random.Random(seed)
    special = SPECIAL if special is None else special
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for f in ("f3", "f4"):
        for m in C.MODELS:
            for s in G.FINDING[f].settings:
                if f == "f3" and s == "long context":
                    continue
                v = round(rng.uniform(0, 12), 1)
                default = (v, f"[{max(v - 5, 0):.1f}, {v + 6:.1f}]", rng.choice((24, 53, 100, 300)), "holds", None)
                value, ci, n, verdict, control = special.get((m.key, f, s), default)
                if control is None:
                    control = f4_control(m.key, s) if f == "f4" else f3_control(s, digit=rng.randint(82, 100))
                w.writerow([G.MODEL[m.key].label, G.FINDING[f].name, s, LENS, "" if n is None else n,
                            "" if value is None else f"{value} %", ci, control, verdict, "", "-",
                            f"results/fake/{m.key}_{f}_{s}/rows.jsonl"])  # fmt: skip
    return out.getvalue()


@pytest.fixture
def book(tmp_path: Path) -> RB.Book:
    (tmp_path / "grid.csv").write_text(synth_csv())
    return RB.Book(tmp_path)


def build_all(b: RB.Book, out: Path) -> list[Path]:
    paths = []
    for kind in ("main", "full"):
        paths += LR.late_read(b, kind, out) + DN.digit_not_name(b, kind, out)
    return paths + LR.deltanet(b, out)


def test_every_figure_saves_and_its_numbers_match_the_grid(book, tmp_path):
    out = tmp_path / "out"
    paths = build_all(book, out)  # common.save raises on overlapping or clipped text
    stems = {
        "late_read_main",
        "late_read_full",
        "digit_not_name_main",
        "digit_not_name_full",
        "late_read_deltanet_main",
    }
    assert {p.stem for p in paths} == stems
    assert {p.suffix for p in paths} == {".png", ".svg"}
    for stem in stems:
        data = out / "data" / f"{stem}.json"
        assert C.check_numbers(data, book) == []
        assert LR.control_mismatches(data, book) == []
        records = json.loads(data.read_text())
        assert records and all(r["finding"] in ("f3", "f4") for r in records)


def test_the_data_file_holds_the_drawn_cells_and_controls(book, tmp_path):
    LR.late_read(book, "main", tmp_path)
    records = json.loads((tmp_path / "data" / "late_read_main.json").read_text())
    cells = {(r["model"], r["setting"]) for r in records if r["source"] == "grid.csv"}
    assert ("27b", "long context") in cells and ("gemma", "draw 1") in cells
    assert ("olmo", "prose") not in cells  # prose is not a MAIN panel
    assert ("muse", "table") not in cells and ("27b", "draw 3") not in cells  # no value: blank, named in the caption
    controls = {(r["model"], r["setting"], r["extra"]["control"]) for r in records if r["source"] == LR.CONTROL_TEXT}
    assert ("27b", "table", "another sentence") in controls and ("27b", "table", "chance") in controls
    chance = {(r["setting"], r["value"]) for r in records if r["source"] == LR.CONTROL_TEXT and r["extra"]["control"] == "chance"}  # fmt: skip
    assert ("table", 33.0) in chance and ("draw 1", 20.0) in chance  # chance per cell, from its control text


def test_full_draws_the_not_interpretable_cells_main_does_not(book, tmp_path):
    for kind in ("main", "full"):
        DN.digit_not_name(book, kind, tmp_path)
    main = json.loads((tmp_path / "data" / "digit_not_name_main.json").read_text())
    full = json.loads((tmp_path / "data" / "digit_not_name_full.json").read_text())
    key = ("olmo_hybrid", "JSON")
    assert key not in {(r["model"], r["setting"]) for r in main}
    assert key in {(r["model"], r["setting"]) for r in full if r["source"] == "grid.csv"}
    ticks = {r["extra"]["control"] for r in full if r["source"] == LR.CONTROL_TEXT}
    assert ticks == {"chance", "digit visible", "another sentence"}  # FULL: the off-path tick too
    assert {r["extra"]["control"] for r in main if r["source"] == LR.CONTROL_TEXT} == {"chance", "digit visible"}


def drawn(b: RB.Book, dots: LR.Dots, panels: tuple[LR.Panel, ...], kind: str):
    """Draw the panels as dot_figure does; what they leave to the caption, the numbers, the grey words drawn."""
    fr = C.frame(kind, "t", "s", ncols=len(panels))
    LR.title_room(fr)
    notes, numbers = LR.Notes(), []
    keys = LR.rows_of(b, dots.finding, panels, kind)
    for i, (ax, p) in enumerate(zip(fr.axes, panels, strict=True)):
        LR.dot_panel(ax, b, dots, p, LR.setup(ax, p.title, keys, first=i == 0), kind, numbers, notes)
    words = {t.get_text() for ax in fr.axes for t in ax.texts if t.get_gid() == "status"}
    C.plt.close(fr.fig)
    return notes, numbers, words


def test_main_leaves_blanks_and_control_failures_to_the_caption(book):
    notes, numbers, words = drawn(book, LR.DOTS, LR.MAIN_PANELS, "main")
    assert words == set()  # no grey words in a MAIN panel
    exceptions = {(c.model, c.setting) for c in notes.labelled + notes.unlabelled}
    assert exceptions == {("gemma", "draw 1"), ("gemma", "JSON"), ("27b", "long context")}
    assert [(c.model, c.setting, ctl.name, n.value) for c, ctl, n in notes.on_control] == [
        ("olmo_hybrid", "table", "DeltaNet", 88.0)
    ]  # failing on its control: no value label, named in the caption
    assert notes.blank == {"too few items", "not run"} and notes.fewer  # Muse's table; Gemma's long context, 27B set 3
    sentences, optional = LR.caption(book, LR.DOTS, "main", LR.RULE, notes, numbers)
    assert sentences[:3] == ["Labelled = fails the rule at ≈ chance.",
                             "Olmo-Hybrid's table fails its DeltaNet-layer control (88% kept).",
                             "Blank or fewer dots: too few items or not run."]  # fmt: skip
    assert sentences[-1] == LR.FILLED and optional == []


def test_full_writes_the_grey_words_and_the_rule(book):
    notes, numbers, words = drawn(book, LR.DOTS, LR.FULL_PANELS, "full")
    assert {"too few items", "not run"} <= words and notes.pale  # Olmo's prose: pale
    sentences, optional = LR.caption(book, LR.DOTS, "full", LR.RULE, notes, numbers)
    assert f"Rule: {LR.RULE}." in sentences and "Pale = control failed." in sentences
    assert optional == ["Fewer dots: not run."]


def test_digit_not_name_says_how_far_below_digit_only(book):
    notes, numbers, _ = drawn(book, DN.dots("main"), DN.MAIN_PANELS, "main")
    gemma = next(c for c in notes.labelled if c.model == "gemma")
    digit = LR.control(gemma, DN.DIGIT_ONLY)
    assert digit is not None
    sentences, _ = LR.caption(book, DN.dots("main"), "main", DN.RULE, notes, numbers, far=True)
    assert sentences[:2] == ["No cell fails the rule.",
                             f"Labelled = holds but stays above chance, far below digit only ({LR.pct(digit.value)})."]  # fmt: skip


def test_fail_kind_and_why():
    cell = RD.Cell("27b", "f4", "draw 1", "", True, "fails", OVER, 24.0, "%", (19.0, 30.0), 300,
                   f4_control("27b", "draw 1"), "x")  # fmt: skip
    assert LR.fail_kind(cell, LR.why_f4) == "≈ chance"
    above = RD.Cell("27b", "f4", "draw 1", "", True, "fails", OVER, 40.0, "%", (32.0, 48.0), 300,
                    f4_control("27b", "draw 1"), "x")  # fmt: skip
    assert LR.fail_kind(above, LR.why_f4) == ""  # the interval misses chance: a plain failure
    dn = RD.Cell("olmo_hybrid", "f4", "table", "", True, "fails", DELTANET_FAIL, 0.0, "%", (0.0, 13.8), 24,
                 f4_control("olmo_hybrid", "table", dn=88), "x")  # fmt: skip
    assert LR.fail_kind(dn, LR.why_f4) == "on DeltaNet"
    n = LR.control(dn, LR.DELTANET)
    assert n is not None and n.value == 88.0 and n.extra["control"] == "DeltaNet"
    name_ok = RD.Cell("27b", "f3", "draw 1", "", True, "fails", "fails", 10.0, "%", (5.0, 15.0), 300,
                      f3_control("draw 1", digit=60), "x")  # fmt: skip
    assert DN.why_f3(name_ok) is DN.DIGIT_ONLY  # the dot passes 35%: the digit-only half failed


def test_controls_parse_value_and_interval():
    c = RD.Cell("27b", "f3", "draw 1", "", True, "holds", "holds", 11.0, "%", (7.9, 15.0), 300,
                f3_control("draw 1", digit=88, off=100), "x")  # fmt: skip
    digit = LR.control(c, DN.DIGIT_ONLY)
    assert digit is not None and (digit.value, digit.ci) == (88.0, (82.0, 92.0))
    off = LR.control(c, DN.OFF_PARTS)
    assert off is not None and off.value == 100.0 and off.ci is None
    assert LR.control(c, LR.DELTANET) is None  # not in the text


def test_setting_words():
    assert LR.setting_words(["draw 1", "draw 2", "JSON"]) == "prompt sets 1-2, JSON"
    assert LR.setting_words(["draw 1", "draw 3"]) == "prompt sets 1, 3"
    assert LR.setting_words(["long context"]) == "long context"


def test_pack_keeps_two_lines_and_refuses_three():
    C.apply()
    fig = C.plt.figure(figsize=C.MAIN_SIZE, dpi=C.DPI)
    room = (0.985 - 0.03) * fig.get_figwidth()

    def sentence(ch: str, share: float) -> str:  # a sentence `share` of the caption's width wide
        s = ch
        while PS.text_width(fig, s + ch + ".", C.CAPTION) < share * room:
            s += ch
        return s + "."

    assert LR.pack(fig, ["One.", "Two."]) == "One. Two."
    a, b, c = sentence("a", 0.5), sentence("b", 0.9), sentence("c", 0.4)
    # in order, no two-line split fits (a | b c, a b | c): c moves up beside a
    assert LR.pack(fig, [a, b, c]) == f"{a} {c}\n{b}"
    assert LR.pack(fig, [a, c, b]) == f"{a} {c}\n{b}"  # in order when that fits
    with pytest.raises(ValueError):
        LR.pack(fig, [b, b, b])
    b8, d = sentence("b", 0.8), sentence("d", 0.1)
    assert LR.pack(fig, [a, b8], [c]) == f"{a}\n{b8}"  # an optional sentence that would cost a move is left out
    assert LR.pack(fig, [a, b8], [d]) == f"{a}\n{b8} {d}"  # one that fits in order is kept
    C.plt.close(fig)


def test_real_grid_matches_the_committed_data_files():
    grids = sorted(p.parent for p in G.OUT.glob("*/grid.csv"))
    files = [C.DATA / f"{s}.json" for s in ("late_read_main", "late_read_full", "late_read_deltanet_main",
                                            "digit_not_name_main", "digit_not_name_full")]  # fmt: skip
    if not grids or not all(f.exists() for f in files):
        pytest.skip("no grid or no committed figure data")
    b = RB.Book(grids[-1])
    for f in files:
        assert C.check_numbers(f, b) == []
        assert LR.control_mismatches(f, b) == []
