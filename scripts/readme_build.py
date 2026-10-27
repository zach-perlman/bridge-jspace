"""readme_build: docs/depth/README.md rendered from docs/README.template.md and the cross-model grid, and RUNS.md from
the runs. Since the merge into main (27 Oct) the root README.md is a hand-written index of docs/depth/ and docs/breadth/.

The prose is hand-written in the template; every result number comes from grid.csv through a marker, so the README
never carries a typed result. A number quoted from elsewhere (Zach's plan) goes through {{q|...}} and is labelled
in the text. The template's first line pins the grid: <!-- grid: results/cross_model/<stamp> -->.

Markers (f = finding key f1-f8 / gate; m = model key 27b, 9b, olmo_hybrid, 122b, 32b, olmo, muse, gemma):
  {{v|f|m|setting}}            the cell's key number: "29%", "+36 points"; finding 5: "+94 / +18 points"
  {{ci|f|m|setting}}           its 95% interval: "[23, 36]"
  {{n|f|m|setting}}            its n
  {{ctl|f|name}}               a control's range over the finding's main cells: "98-100%" (CONTROLS below)
  {{ctl|f|name|m|setting}}     that control in one cell: "38%"
  {{holds|f}}                  "7 of 8": models where it holds / models where a rule judged it
  {{count|f|setting|word}}     "7 of 7": models whose cell in that setting has that verdict word / models judged there
  {{conf|f}}                   "medium (holds 7 of 8; Muse: prose fails, 5 items)"
  {{table|f|setting,...}}      one row per judged model (its first listed setting with a value), the rest below
  {{q|text}}                   a number quoted from outside the grid, rendered as is
  {{num|key}}                  an X0 number from docs/x0_numbers.json (scripts/x0_details.py, from the run files)
  {{pt|key}}                   the same number's point estimate, without its interval (for ranges in prose)
  {{grid}}                     the grid folder
  {{head}}                     the commit the README is built at

uv run python scripts/readme_build.py [--grid DIR] [--runs]   # writes docs/depth/README.md (and RUNS.md with --runs)
uv run python scripts/readme_build.py --out OTHER.md   # the same page elsewhere, its links rewritten to resolve there
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import cross_model_grid as G
from scripts import readme_draft as RD
from scripts import run_table as RT

REPO = G.REPO
TEMPLATE = REPO / "docs" / "README.template.md"
PAGE = REPO / "docs" / "depth" / "README.md"  # the built page (the root README.md is an index since the merge)
ORDER = ("27b", "9b", "olmo_hybrid", "122b", "32b", "olmo", "muse", "gemma")  # hybrids first, then attention-only
NAME = {"27b": "Qwen3.6-27B", "9b": "Qwen3.5-9B", "olmo_hybrid": "Olmo-Hybrid-7B", "122b": "Qwen3.5-122B",
        "32b": "Qwen3-32B", "olmo": "OLMo-3-7B", "muse": "Muse 30B", "gemma": "Gemma 4 31B"}  # fmt: skip
SHORT = {"27b": "27B", "9b": "9B", "olmo_hybrid": "Olmo-Hybrid", "122b": "122B", "32b": "32B", "olmo": "OLMo-3",
         "muse": "Muse", "gemma": "Gemma"}  # fmt: skip
FEW = 30  # a cell with fewer items is shown as "too few items" (display only; the verdict does not change)
JUDGED = ("holds", "fails", "mixed", "unclear")
# a control's number inside grid.csv's "chance or control level" text, per finding
CONTROLS: dict[str, dict[str, str]] = {
    "f2": {"recall": r"the control, needs >= 30%\): (\d+(?:\.\d+)?)%", "rest": r"the rest \(needs >= 50%\): (\d+)%",
           "random lookups": r"same-share random part[^:]*: lookups (\d+(?:\.\d+)?)%",
           "random recalls": r"same-share random part[^:]*: lookups .*?\bn=\d+, recalls (\d+(?:\.\d+)?)%"},
    "f3": {"digit visible": r"the digit left visible \(the sentence without its digit hidden\): (\d+)%",
           "another sentence": r"off-path parts hidden[^:]*: lowest (\d+)%"},
    "f4": {"chance": r"chance (\d+)%", "another sentence": r"off-path sentence hidden instead keeps (\d+)%",
           "DeltaNet": r"DeltaNet layer instead: (\d+)%"},
    "f6": {"place in text": r"the same place in the text (\d+)%"},
    "f7": {"recall": r"recall switched (\d+)%", "random": r"random push on lookups (\d+)%"},
    "f8": {"recall": r"recall written: (\d+)%", "fitted code": r"the fitted code \(slot direction\) (\d+)%"},
    "gate": {"other bridge": r"the other bridge in the top 10: (\d+)%"},
}  # fmt: skip
WORD = {"not interpretable": "can't tell (a control failed)", "inconclusive": "can't tell (the rule's own)",
        "open": "no rule (values only)"}  # fmt: skip
SETTING = (("draw ", "scene set "), ("v1 (at the word)", "at its word"), ("v2 (after the word)", "after its word"),
           ("tasks, Zach's rule", "Zach's tasks, his rule"), ("statement", "sentence"))  # fmt: skip
MARK = re.compile(r"\{\{([a-z]+)\|?([^{}]*)\}\}")


def show(setting: str) -> str:
    for a, b in SETTING:
        setting = setting.replace(a, b)
    return setting


def word(c: RD.Cell) -> str:
    w = WORD.get(c.word, c.word)
    return f"{w} (too few items)" if c.n is not None and c.n < FEW and c.word != "holds" else w


class Book:
    """The grid's main-lens cells, looked up by finding, model and setting (finding 5: both parts)."""

    def __init__(self, grid_dir: Path, head: str | None = None):
        self.grid_dir = grid_dir
        self.head = head  # the commit named on the page; None: HEAD when rendered
        self.cells, _ = RD.read_grid((grid_dir / "grid.csv").read_text())

    def of(self, f: str, m: str | None = None) -> list[RD.Cell]:
        return [c for c in self.cells if c.finding == f and (m is None or c.model == m)]

    def get(self, f: str, m: str, setting: str) -> list[RD.Cell]:
        cs = [c for c in self.of(f, m) if c.setting == setting]
        if not cs:
            raise KeyError(f"no grid cell {f} / {m} / {setting}")
        return sorted(cs, key=lambda c: c.part)  # "1st-2nd" before "3rd on"

    def value(self, f: str, m: str, setting: str) -> str:
        cs = [c for c in self.get(f, m, setting) if c.value is not None]
        if not cs:
            raise ValueError(f"no value in {f} / {m} / {setting}")
        if cs[0].unit == "%":
            return f"{RD.r0(cs[0].value)}%"  # type: ignore[arg-type]
        return " / ".join(f"{RD.r0(c.value):+d}" for c in cs) + " points"  # type: ignore[arg-type]

    def ci(self, f: str, m: str, setting: str) -> str:
        c = self.get(f, m, setting)[0]
        return RD.fmt_ci(c.ci, c.unit)

    def n(self, f: str, m: str, setting: str) -> str:
        return " / ".join(str(c.n) for c in self.get(f, m, setting))

    def control(self, f: str, name: str, cells: Iterable[RD.Cell]) -> list[float]:
        pat = re.compile(CONTROLS[f][name])
        return [float(x.group(1)) for c in cells if (x := pat.search(c.control))]

    def ctl(self, f: str, name: str, m: str | None = None, setting: str | None = None) -> str:
        cells = self.get(f, m, setting) if m and setting else self.of(f)
        xs = self.control(f, name, cells)
        if not xs:
            raise ValueError(f"no control '{name}' in {f} {m or ''} {setting or ''}")
        lo, hi = RD.r0(min(xs)), RD.r0(max(xs))
        return f"{lo}%" if lo == hi else f"{lo}-{hi}%"

    def states(self, f: str) -> dict[str, str]:
        return RD.states(self.of(f))

    def holds(self, f: str) -> str:
        """'7 of 8' over cells with at least FEW items (Dan, 23 Oct): a cell of 5 or 24 items does not decide a count."""
        st = RD.states([c for c in self.of(f) if c.n is None or c.n >= FEW])
        judged = [m for m in ORDER if st[m] in JUDGED]
        return f"{sum(st[m] == 'holds' for m in judged)} of {len(judged)}"

    def count(self, f: str, setting: str, w: str) -> str:
        cs = [c for c in self.of(f) if c.setting == setting and c.part in ("", "1st-2nd")]
        judged = {c.model for c in cs if c.word in ("holds", "fails", "not interpretable", "inconclusive")}
        return f"{len({c.model for c in cs if c.word == w})} of {len(judged)}"

    def exceptions(self, f: str, limit: int = 3) -> list[str]:
        st, out = self.states(f), []
        for m in ORDER:
            if st[m] not in ("fails", "mixed", "unclear"):
                continue
            fail, unclear = [], []
            for c in self.of(f, m):
                s = show(c.setting) + (f" ({c.n} items)" if c.n is not None and c.n < FEW else "")
                into = (
                    fail if c.word == "fails" else unclear if c.word in ("not interpretable", "inconclusive") else None
                )
                if into is not None and s not in into:
                    into.append(s)
            parts = ([f"{', '.join(fail)} fail{'s' if len(fail) == 1 else ''}"] if fail else []) + (
                [f"{', '.join(unclear)} can't tell" if not fail else f"{len(unclear)} can't tell"] if unclear else []
            )
            out.append(f"{SHORT[m]}: {', '.join(parts)}")
        return out if len(out) <= limit else [*out[:limit], f"{len(out) - limit} more in the table"]

    def conf(self, f: str) -> str:
        j = RD.judge(G.FINDING[f], self.cells)
        ex = self.exceptions(f)
        return f"{j.level} (holds {self.holds(f)}" + (f"; {'; '.join(ex)})" if ex else ")")

    def table(self, f: str, settings: list[str]) -> list[str]:
        rows = ["| Model | Setting | Result [95% CI] | n | Verdict | All settings |", "|---|---|---|---|---|---|"]
        untested = []
        for m in ORDER:
            cs = self.of(f, m)
            judged = [c for c in cs if c.word in ("holds", "fails", "not interpretable", "inconclusive", "open")]
            if not judged:
                untested.append(f"{SHORT[m]} ({reason(cs)})")
                continue
            main = next((s for s in settings if any(c.setting == s and c.value is not None for c in cs)), None)
            if main is None:  # judged, but no number (e.g. no valid test point): the row says why
                c = judged[0]
                rows.append(f"| {NAME[m]} | {show(c.setting)} | – | – | {word(c)} | {summary(judged)} |")
                continue
            head = self.get(f, m, main)
            ci = self.ci(f, m, main) if len([c for c in head if c.value is not None]) == 1 else ""
            rows.append(f"| {NAME[m]} | {show(main)} | {self.value(f, m, main)}{' ' + ci if ci else ''} | "
                        f"{self.n(f, m, main)} | {word(head[0])} | {summary(judged)} |")  # fmt: skip
        if untested:
            rows += ["", "Not tested: " + ", ".join(untested) + "."]
        return rows


def summary(cells: list[RD.Cell]) -> str:
    """'4 of 5 hold; prose: fails (5 items)': one cell per setting (finding 5: the whole row, else its 1st-2nd part)."""
    one: dict[str, RD.Cell] = {}
    for c in sorted(cells, key=lambda c: c.part):  # "" before "1st-2nd" before "3rd on"
        one.setdefault(c.setting, c)
    cells = list(one.values())
    if all(c.word == "open" for c in cells):
        return "no rule"
    held = sum(c.word == "holds" for c in cells)
    rest = []
    for c in cells:
        if c.word != "holds":
            few = f" ({c.n} items)" if c.n is not None and c.n < FEW else ""
            rest.append(f"{show(c.setting)}{few}: {WORD.get(c.word, c.word)}")
    return f"{held} of {len(cells)} hold" + (f"; {'; '.join(rest)}" if rest else "")


def reason(cells: list[RD.Cell]) -> str:
    """Why a model has no judged cell, in a few words."""
    text = " ".join(c.verdict for c in cells)
    for key, why in (("no lens", "no lens"), ("competence", "too few items answered right"),
                     ("precheck", "too few usable scenes"), ("no layer", "no layer to test"),
                     ("running", "still running"), ("pending", "still running"), ("waits on", "still running"),
                     ("blocked", "still running"), ("not on Zach", "not on Zach's branch"), ("failed", "run failed"),
                     ("no spec", "not run"), ("not run", "not run")):  # fmt: skip
        if key in text:
            return why
    return "no result"


def render(template: str, book: Book) -> str:
    lines = template.splitlines()
    if lines and lines[0].startswith("<!-- grid:"):
        lines = lines[1:]
    out = [
        "<!-- Generated by scripts/readme_build.py from docs/README.template.md and grid.csv; edit the template. -->"
    ]
    for line in lines:
        t = MARK.fullmatch(line.strip())
        if t and t.group(1) == "table":
            f, *settings = t.group(2).split("|")
            out += book.table(f, settings)
            continue
        out.append(MARK.sub(lambda x: one(x, book), line))
    return "\n".join(out).rstrip() + "\n"


def one(x: re.Match[str], book: Book) -> str:
    kind, args = x.group(1), x.group(2).split("|") if x.group(2) else []
    if kind in ("v", "ci", "n"):
        return getattr(book, {"v": "value", "ci": "ci", "n": "n"}[kind])(*args)
    if kind == "ctl":
        return book.ctl(*args)
    if kind == "holds":
        return book.holds(args[0])
    if kind == "count":
        return book.count(*args)
    if kind == "head":
        if book.head is None:
            book.head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True,
                                       text=True, check=True).stdout.strip()  # fmt: skip
        return book.head
    if kind == "conf":
        return book.conf(args[0])
    if kind == "q":
        return "|".join(args)
    if kind in ("num", "pt"):  # an X0 number, recomputed from the run files by scripts/x0_details.py
        numbers = json.loads((REPO / "docs" / "x0_numbers.json").read_text())
        if args[0] not in numbers:
            raise ValueError(f"{x.group(0)}: no such key in docs/x0_numbers.json (run scripts/x0_details.py)")
        text = numbers[args[0]]["text"]
        return text.split(" [")[0] if kind == "pt" else text  # pt: the point estimate, without its interval
    if kind == "grid":
        return str(book.grid_dir.relative_to(REPO))
    raise ValueError(f"unknown marker {x.group(0)}")


def pinned_grid(template: str) -> Path:
    m = re.match(r"<!-- grid: (\S+) -->", template)
    if not m:
        raise ValueError("the template's first line must pin the grid: <!-- grid: results/cross_model/<stamp> -->")
    return REPO / m.group(1)


LINK_TARGET = re.compile(r"(\]\(|(?:src|href)=\")([^)\"\s]+)")


def relink(text: str, out: Path) -> str:
    """The rendered page's relative link and image targets, written from the repo root, rewritten to resolve from out's
    folder (docs/depth/README.md: figures/story/x.png -> ../../figures/story/x.png); URLs, anchors and absolute paths
    stay. A no-op for the root README.md."""
    base = out.resolve().parent

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return m.group(0)
        path, sep, frag = target.partition("#")
        rel = Path(os.path.relpath(REPO / path, base)).as_posix() + ("/" if path.endswith("/") else "")
        return m.group(1) + rel + sep + frag

    return LINK_TARGET.sub(fix, text)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="override the grid pinned in the template")
    ap.add_argument("--runs", action="store_true", help="also write RUNS.md (the runs behind every grid cell)")
    ap.add_argument("--out", default=str(PAGE.relative_to(REPO)), help="where to write the page, relative to the repo "
                    "root (default docs/depth/README.md); its relative links are rewritten to resolve from there")  # fmt: skip
    a = ap.parse_args(argv)
    text = TEMPLATE.read_text()
    grid = Path(a.grid).resolve() if a.grid else pinned_grid(text)
    out = REPO / a.out
    readme = relink(render(text, Book(grid)), out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(readme)
    print(f"{out.relative_to(REPO)}: {len(readme.splitlines())} lines from {grid.relative_to(REPO)}")
    if a.runs:
        (REPO / "RUNS.md").write_text(RT.build(grid))
        print("RUNS.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
