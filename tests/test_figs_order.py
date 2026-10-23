"""scripts/figs/order_identity.py and scripts/figs/counting.py (findings 5 and 6) on a SYNTHETIC grid.csv: each figure
saves (the overlap check passes), every grid number it draws matches its cell (check_numbers), the 3rd-on part is drawn
negated, the controls drawn are the control text's, and the captions name the failing, missing and not-run cells. On
the newest real grid (if present), every grid number drawn matches its cell."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts.figs import common as C
from scripts.figs import counting as CT
from scripts.figs import order_identity as OI

LENS = "none (lens-free)"
# finding 5: (1st-2nd: position - identity, 3rd on: identity - position) in points, per model; n per part
F5 = {"27b": (96, 17), "9b": (52, 38), "olmo_hybrid": (60, 30), "122b": (68, 40), "32b": (85, 12), "olmo": (45, 24),
      "muse": (76, 30), "gemma": (30, 28)}  # fmt: skip
F5_SETTINGS = ("draw 1", "draw 2", "draw 3", "8 sentences", "12 sentences")
F5_MISSING = {("olmo_hybrid", "draw 3"): "missing (spec x not run (not in the queue or the ledger))",
              ("gemma", "8 sentences"): "missing (no spec)", ("gemma", "12 sentences"): "missing (no spec)"}  # fmt: skip
F5_FAILS = ("32b", "draw 1")  # B (3rd on) fails
# finding 6: (list order %, place in text %, from the end %) per model
F6 = {"27b": (39, 9, 10), "9b": (22, 5, 7), "olmo_hybrid": (29, 9, 8), "122b": (29, 8, 7), "32b": (13, 3, 4),
      "olmo": (31, 11, 14), "muse": (38, 9, 11), "gemma": (12, 2, 1)}  # fmt: skip
F6_FAILS = {("32b", "filler moved"), ("9b", "one statement more"), ("9b", "one statement fewer")}


def row(m: str, f: str, setting: str, n: int | None, value: str, ci: str, control: str, verdict: str) -> list[str]:
    return [G.MODEL[m].label, G.FINDING[f].name, setting, LENS, "" if n is None else str(n), value, ci, control,
            verdict, "", "-", f"results/fake/{m}_{f}/summary.json"]  # fmt: skip


def synth_rows(
    missing: dict[tuple[str, str], str] = F5_MISSING, unclear: tuple[str, str] | None = None
) -> list[list[str]]:
    out = []
    for m, (a, r) in F5.items():
        for i, s in enumerate(F5_SETTINGS):
            if (m, s) in missing:
                out.append(row(m, "f5", s, None, "", "", "", missing[(m, s)]))
                continue
            bad = (m, s) == F5_FAILS
            r_s = 3.0 if bad else r - i
            verdict = ("fails (partly: A True, B False)" if bad else "not interpretable (the random-patch control "
                       "breaks 40% of answers, above 30%)" if (m, s) == unclear else "holds")  # fmt: skip
            for part, v, txt in (("1st-2nd", a - i, f"position - identity +{a - i}, A: True"),
                                 ("3rd on", r_s, f"identity - position +{r_s:g}, B: {not bad}")):  # fmt: skip
                out.append(row(m, "f5", f"{s}, {part}", 150 + 10 * i, f"{v:.1f} pts", f"[{v - 8:.1f}, {v + 8:.1f}]",
                               f"{txt}; layer 30 (saved verdict)", verdict))  # fmt: skip
    for m, (o, t, e) in F6.items():
        for s in CT.SETTINGS:
            ctl = f"the same place in the text {t}% [{t - 2}, {t + 3}]"
            if s != "filler moved":
                ctl = f"counted from the end {e}% [{max(e - 2, 0)}, {e + 3}]; " + ctl
            verdict = "fails" if (m, s) in F6_FAILS else "holds"
            out.append(row(m, "f6", s, 300, f"{o:.1f} %", f"[{o - 4:.1f}, {o + 4:.1f}]",
                           f"{ctl}; shown at layer 30; decisive layers 28, 30", verdict))  # fmt: skip
    return out


def write_grid(folder: Path, rows: list[list[str]]) -> RB.Book:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(G.COLUMNS)
    w.writerows(rows)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "grid.csv").write_text(buf.getvalue())
    return RB.Book(folder)


@pytest.fixture
def book(tmp_path: Path) -> RB.Book:
    return write_grid(tmp_path, synth_rows())


def records(out: Path, stem: str, kind: str) -> list[dict]:
    return json.loads((out / "data" / f"{stem}_{kind}.json").read_text())


def test_order_identity_saves_and_matches_the_grid(book: RB.Book, tmp_path: Path):
    out = tmp_path / "out"
    for kind, draw in (("main", OI.draw_main), ("full", OI.draw_full)):
        paths = draw(book, out)
        assert [p.name for p in paths] == [f"order_identity_{kind}.png", f"order_identity_{kind}.svg"]
        assert C.check_numbers(out / "data" / f"order_identity_{kind}.json", book) == []
    full = records(out, "order_identity", "full")
    valued = [c for c in book.of("f5") if c.value is not None]
    assert len(full) == len(valued)  # every cell with a value is drawn once, the missing ones nowhere
    for d in full:  # one quantity for both parts: position minus identity
        assert d["extra"]["drawn"] == (d["value"] if d["part"] == "1st-2nd" else -d["value"])
    main = records(out, "order_identity", "main")
    assert {d["model"] for d in main} == set(OI.MAIN_MODELS)
    assert {d["setting"] for d in main} == {"draw 1", "draw 2", "draw 3", "12 sentences"}  # 5 sentences + the inset


def test_order_identity_caption_facts(book: RB.Book):
    keys = [m.key for m in C.MODELS]
    settings = tuple(s for li in OI.LISTS for s in li.settings)
    got = OI.facts(book, keys, settings)
    assert got.fails == ["32B scene set 1, 3rd on"]  # only the part whose half of the rule failed
    assert got.unclear == [] and got.n_range == "150–190"
    assert OI.missing_text(book, keys, settings) == "Not run: Olmo-Hybrid scene set 3; Gemma 8 and 12 sentences."


def test_order_identity_draws_a_failed_control_grey(tmp_path: Path):
    b = write_grid(tmp_path / "grid", synth_rows(missing={}, unclear=("muse", "draw 1")))
    keys = [m.key for m in C.MODELS]
    assert OI.facts(b, keys, ("draw 1",)).unclear == ["Muse scene set 1"]  # the setting, once for both parts
    OI.draw_full(b, tmp_path / "out")
    drawn = {(d["model"], d["setting"]) for d in records(tmp_path / "out", "order_identity", "full")}
    assert ("muse", "draw 1") in drawn  # drawn (grey), not dropped


def test_caption_packs_sentences_into_lines():
    assert OI.pack(["One.", "", "Two."]) == "One. Two."
    assert OI.pack(["x" * 60, "y" * 60, "z" * 10]).count("\n") == 1  # 120 characters do not fit one line


def test_counting_saves_and_matches_the_grid(book: RB.Book, tmp_path: Path):
    out = tmp_path / "out"
    for kind, draw in (("main", CT.draw_main), ("full", CT.draw_full)):
        paths = draw(book, out)
        assert [p.name for p in paths] == [f"counting_{kind}.png", f"counting_{kind}.svg"]
        assert C.check_numbers(out / "data" / f"counting_{kind}.json", book) == []
    main = records(out, "counting", "main")
    assert {d["setting"] for d in main} == {"filler moved"}
    for kind in ("main", "full"):
        for d in records(out, "counting", kind):  # the controls drawn are the control text's
            o, t, e = F6[d["model"]]
            if d["source"] == "grid.csv":
                assert d["value"] == o
            else:
                assert d["value"] == {"place in text": t, "from the end": e}[d["extra"]["control"]]
    full = records(out, "counting", "full")
    assert len(full) == len(F6) * (2 + 3 + 3)  # filler moved: order + place; one more / fewer: + from the end


def test_counting_names_why_the_filler_test_fails(book: RB.Book):
    c = CT.cells(book, "filler moved")["32b"]
    assert CT.control(c, "place in text") == (3.0, 1.0, 6.0)
    assert CT.why_fails(c).startswith("list order is above when pooled")  # 9 > 6: the topics failed


def test_command_line(book: RB.Book, tmp_path: Path):
    out = tmp_path / "cli"
    for mod in (OI, CT):
        assert mod.main(["--grid", str(tmp_path), "--only", "main", "--out", str(out)]) == 0
    assert {p.name for p in out.glob("*.png")} == {"order_identity_main.png", "counting_main.png"}


def newest_grid() -> Path | None:
    grids = sorted((C.REPO / "results" / "cross_model").glob("*/grid.csv"))
    return grids[-1].parent if grids else None


@pytest.mark.skipif(newest_grid() is None, reason="no results/cross_model/<stamp>/grid.csv here")
def test_the_newest_real_grid_matches_every_drawn_number(tmp_path: Path):
    grid = newest_grid()
    assert grid is not None
    b = RB.Book(grid)
    for stem, mod in (("order_identity", OI), ("counting", CT)):
        for kind in ("main", "full"):
            getattr(mod, f"draw_{kind}")(b, tmp_path)
            assert C.check_numbers(tmp_path / "data" / f"{stem}_{kind}.json", b) == []
