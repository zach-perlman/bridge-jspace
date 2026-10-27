"""slot_outcomes: where the last-two-token patch sends the answer, slot by slot (finding 5; Dan's B3, 23 Oct 2026).

Finding 5: two prompts list the same entities in a different order; the donor prompt's last two tokens are copied into
the original at one layer (pointer_swap: source dissoc, group last). Every possible answer is a different digit (a
colour word in the 12-sentence lists), so the answer shows what the copy pointed to. Each patched answer is sorted into
one of five outcomes, per place k of the donor's asked sentence (k = slots.position + 1, as scripts/finding5_confirm.py):
  order      the original's sentence at place k (role position)
  identity   the original's sentence about the donor's entity (role identity)
  unchanged  the original's own answer (role none)
  another    any other sentence of the original's list (role context). Its source: "slot 1" (the list's first sentence),
             "k±1" (a neighbour of place k that is not slot 1: at k = 2 the neighbour k - 1 is slot 1 and counts there),
             or "elsewhere"; next to each, the expected count if the answer picked uniformly among the N - 3 sentences
             no other outcome names (the baseline)
  donor      the donor's own answer, absent from the original's list (role value)
Answers off the list (a recalled digit, any other digit or word: roles recall, other_digit, other) are counted apart as
"off list", so the five shares sum to 100% exactly when a slot has none. Diagnostic only (off_case_n): off-list answers
that name an outcome when case is ignored (' Red' for 'red'); the outcomes keep pointer_swap's roles, as the grid does.

Cells: the finding-5 rows of grid.json (results/cross_model/<stamp>): the run and the layer each grid setting names
(Qwen3.6-27B's draws: layer 50, fixed; every other cell: the donor-digit rule's layer, re-derived here as a check).
Both families of every run: memory -> prompt (RL, the decisive one) and named -> prompt (DL, at RL's layer, as the
saved verdicts report it). Items come from the files each manifest pins (sha256-checked, as
verification/finding5_2026-10-23/recompute.py loads them). Shares with Wilson 95% intervals over items, per draw and
pooled over the three draws of the 5-sentence lists (each draw at its own layer).

Checks (summary.json): the counts of every row sum to its n; RL's counts give the grid's n and point value of both
finding-5 parts (1st-2nd: order - identity, 3rd on: identity - order); the per-k role counts equal the saved verdict's
by_k (both families) where the grid cites one; the layer rule gives the grid's layer; the slot of every on-list answer
agrees with its role.

uv run python scripts/slot_outcomes.py [--grid results/cross_model/<stamp>] [--out results/slot_outcomes]
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.stats import wilson
from scripts import finding5_confirm as FC
from scripts import readme_build as RB

GRID = pins.RESULTS_DIR / "cross_model" / "20261023T105852Z"
OUT = pins.RESULTS_DIR / "slot_outcomes"
PS_RESULTS = Path("results") / "pointer_swap"  # relative to the repo root
OUTCOMES = ("order", "identity", "unchanged", "another", "donor")
ROLE = {"position": "order", "identity": "identity", "none": "unchanged", "context": "another", "value": "donor"}
OFF = ("recall", "other_digit", "other")  # answers off the original's list
SOURCES = ("slot 1", "k±1", "elsewhere")
FAMILIES = ("RL", "DL")
FAMILY_NAME = {"RL": "memory -> prompt (recalled bridge)", "DL": "named -> prompt (named bridge)"}
DRAWS = ("draw 1", "draw 2", "draw 3")
POOLED = "5 sentences, draws pooled"
FIXED = {"27b": 50}  # finding 5's 27B draws: layer 50, chosen after its first runs (recompute.py)
PARTS = {"1st-2nd": ("order", "identity"), "3rd on": ("identity", "order")}  # grid part: (a, b) of a - b


# ---------------------------------------------------------------- the grid's cells


@dataclass
class Cell:
    """One finding-5 grid setting with a run, and the grid's two parts {part: (n, value as a fraction)}."""

    model: str
    setting: str
    run: str
    layer: int
    level: str | None
    sentences: int
    verdict_path: str | None
    parts: dict[str, tuple[int, float]] = field(default_factory=dict)


def grid_cells(grid_dir: Path) -> tuple[list[Cell], list[str]]:
    """The grid's finding-5 settings with a run (model order, then setting), and the ones without (their verdict)."""
    rows = json.loads((grid_dir / "grid.json").read_text())["rows"]
    cells: dict[tuple[str, str], Cell] = {}
    missing = []
    for r in rows:
        if r["finding"] != "f5":
            continue
        if r["value"] is None:
            missing.append(f"{RB.SHORT[r['model']]} {r['setting']}: {r['verdict']}")
            continue
        setting, part = r["setting"].rsplit(", ", 1)
        layer = int(re.search(r"\blayer (\d+)\b", r["control"]).group(1))  # type: ignore[union-attr]
        lv = re.search(r"_(e\d+-[a-z]+)_\d{8}-\d{6}/", r["path"])
        sentences = int(setting.split()[0]) if setting.endswith(" sentences") else 5
        verdict = r["path"] if r["path"].endswith("verdict.json") else None
        c = cells.setdefault((r["model"], setting), Cell(r["model"], setting, r["run"], layer, lv and lv.group(1),
                                                         sentences, verdict))  # fmt: skip
        if (c.run, c.layer) != (r["run"], layer):
            raise ValueError(f"{r['model']} {setting}: the two parts name different runs or layers")
        c.parts[part] = (int(r["n"]), float(r["value"]))
    order = {k: i for i, k in enumerate(RB.ORDER)}
    settings = [*DRAWS, "8 sentences", "12 sentences"]
    return sorted(cells.values(), key=lambda c: (order[c.model], settings.index(c.setting))), missing


# ---------------------------------------------------------------- one run's rows


def load_items(m: dict, repo: Path = pins.REPO_ROOT) -> dict[str, dict]:
    """{item id: item} of the files the manifest pins, each checked against its sha256."""
    items: dict[str, dict] = {}
    for pin in m["items"].values():
        raw = (repo / pin["file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin["sha256"]:
            raise ValueError(f"{pin['file']}: sha256 differs from the manifest's pin")
        items |= {it["id"]: it for it in json.loads(raw)["items"]}
    return items


def load_run(run: str, level: str | None, repo: Path = pins.REPO_ROOT) -> tuple[dict, list[dict], dict[str, dict]]:
    """(manifest, the dissoc rows at the last two tokens of `level` (every row's if None), the run's items)."""
    d = repo / PS_RESULTS / run
    m = json.loads((d / "manifest.json").read_text())
    rows = []
    with (d / "outcomes.jsonl").open() as fh:
        for line in fh:
            r = json.loads(line)
            if r["source"] == "dissoc" and r["group"] == "last" and (level is None or r["level"] == level):
                rows.append(r)
    levels = {r["level"] for r in rows}
    if len(levels) != 1:
        raise ValueError(f"{run}: rows of {sorted(levels)} levels; name one")
    return m, rows, load_items(m, repo)


def slot_of(answer: str, item: dict) -> int | None:
    """0-based place of a decoded answer token in the original's list: the value it equals, else the one value it
    begins (a word split into tokens); None for no or several."""
    a = answer.strip()
    vals = [str(v) for v in item["digits"]]
    if a in vals:
        return vals.index(a)
    hits = [i for i, v in enumerate(vals) if a and v.startswith(a)]
    return hits[0] if len(hits) == 1 else None


def source_of(j: int, k: int) -> str:
    """Where another listed answer at 0-based place j comes from, for the donor's asked place k (1-based)."""
    if j == 0:
        return "slot 1"
    return "k±1" if abs(j - (k - 1)) == 1 else "elsewhere"


def expected_sources(item: dict, k: int) -> dict[str, float]:
    """The source shares if another listed answer were a uniform pick among the sentences no other outcome names."""
    taken = {item["slots"][s] for s in ("query", "identity", "position")}
    cands = [j for j in range(len(item["digits"])) if j not in taken]
    out: dict[str, float] = dict.fromkeys(SOURCES, 0.0)
    for j in cands:
        out[source_of(j, k)] += 1 / len(cands)
    return out


@dataclass
class Tally:
    """Counts of one (family, k) cell: raw roles, the sources of another listed answer, their uniform expectation."""

    n: int = 0
    roles: collections.Counter = field(default_factory=collections.Counter)
    sources: collections.Counter = field(default_factory=collections.Counter)
    expected: dict[str, float] = field(default_factory=lambda: dict.fromkeys(SOURCES, 0.0))
    case: collections.Counter = field(default_factory=collections.Counter)  # off-list answers = an outcome, any case

    def add(self, other: Tally) -> None:
        self.n += other.n
        self.roles.update(other.roles)
        self.sources.update(other.sources)
        self.case.update(other.case)
        for s in SOURCES:
            self.expected[s] += other.expected[s]

    def count(self, outcome: str) -> int:
        return sum(self.roles[r] for r, o in ROLE.items() if o == outcome)

    def off(self) -> int:
        return sum(self.roles[r] for r in OFF)


def tally(rows: list[dict], items: dict[str, dict], layer: int, sentences: int) -> tuple[dict, dict[str, int]]:
    """{(family, k): Tally} of RL and DL dissoc rows at the last two tokens at `layer`, and the slot check: on-list
    answers whose slot was found and agrees with the role ('agrees') or could not be found from the token
    ('unresolved'). Raises on a disagreement."""
    out: dict[tuple[str, int], Tally] = {}
    check = collections.Counter({"agrees": 0, "unresolved": 0})
    seen = set()
    for r in rows:
        cell = (r["source"], r["group"], str(r["layer"]))
        if r["family"] not in FAMILIES or cell != ("dissoc", "last", str(layer)):
            continue
        key = (r["family"], r["name"])
        if key in seen:
            raise ValueError(f"{key}: two rows at layer {layer}")
        seen.add(key)
        it = items[r["name"]]
        slots = it["slots"]
        if len(it["entities"]) != sentences or it["sources"]["dissoc"]["query_slot"] != slots["position"]:
            raise ValueError(f"{r['name']}: not a {sentences}-sentence item asking the donor at slots.position")
        if len({str(v) for v in it["digits"]}) != sentences:
            raise ValueError(f"{r['name']}: repeated values in the list")
        role = r["role"]
        if role not in ROLE and role not in OFF:
            raise ValueError(f"{r['name']}: unexpected role {role!r}")
        k = slots["position"] + 1
        t = out.setdefault((r["family"], k), Tally())
        t.n += 1
        t.roles[role] += 1
        if role in ("none", "identity", "position", "context"):
            j = slot_of(r["top"], it)
            want = {"none": slots["query"], "identity": slots["identity"], "position": slots["position"]}.get(role)
            if j is None:
                check["unresolved"] += 1
            elif (want is not None and j != want) or (want is None and j in (slots["query"], slots["identity"],
                                                                              slots["position"])):  # fmt: skip
                raise ValueError(f"{r['name']}: answer {r['top']!r} at slot {j + 1}, role {role}")
            else:
                check["agrees"] += 1
            if role == "context":
                t.sources["unresolved" if j is None else source_of(j, k)] += 1
                if j is not None and j != 0 and abs(j - (k - 1)) == 1:  # k±1's direction (reported, not a source)
                    t.sources["k-1" if j < k - 1 else "k+1"] += 1
                for s, e in expected_sources(it, k).items():
                    t.expected[s] += e
        elif role == "other" and (o := case_outcome(r["top"], it)) is not None:
            t.case[o] += 1
    return out, dict(check)


def case_outcome(answer: str, item: dict) -> str | None:
    """The outcome an off-list answer names when case is ignored (' Red' for 'red'), else None. Diagnostic only: the
    outcomes keep pointer_swap's roles, which finding 5 and the grid use."""
    a = answer.strip().lower()
    preds = item["sources"]["dissoc"]["predictions"]
    for role in ("none", "identity", "position", "value"):
        if str(preds[role]).lower() == a:
            return ROLE[role]
    return "another" if a in {str(v).lower() for v in item["digits"]} else None


# ---------------------------------------------------------------- checks against the grid and the saved verdicts


def grid_check(c: Cell, t: dict[tuple[str, int], Tally]) -> list[dict[str, Any]]:
    """RL's 1st-2nd (order - identity) and 3rd-on (identity - order) n and point value against the grid's."""
    out = []
    for part, (a, b) in PARTS.items():
        sel = [x for (fam, k), x in t.items() if fam == "RL" and (k <= 2) == (part == "1st-2nd")]
        n = sum(x.n for x in sel)
        v = (sum(x.count(a) for x in sel) - sum(x.count(b) for x in sel)) / n
        gn, gv = c.parts[part]
        out.append({"model": c.model, "setting": c.setting, "part": part, "n": n, "grid_n": gn, "value": v,
                    "grid_value": gv, "ok": n == gn and abs(v - gv) < 1e-9})  # fmt: skip
    return out


def verdict_check(c: Cell, t: dict[tuple[str, int], Tally], repo: Path = pins.REPO_ROOT) -> dict[str, Any] | None:
    """The saved verdict's per-k role counts (every family it has) against ours, where the grid cites a verdict."""
    if c.verdict_path is None:
        return None
    v = json.loads((repo / c.verdict_path).read_text())
    ok, fams = v["layer"] == c.layer, []
    for fam, block in v["families"].items():
        fams.append(fam)
        for k, counts in block["by_k"].items():
            mine = t.get((fam, int(k)))
            ok &= dict(mine.roles if mine else {}) == counts
    return {"model": c.model, "setting": c.setting, "verdict": c.verdict_path, "families": fams, "ok": ok}


def layer_check(c: Cell, m: dict, rows: list[dict]) -> dict[str, Any]:
    """The layer the rule gives (the last swept layer with RL's donor-digit Wilson upper bound < 10%), or the 27B's
    fixed 50 on its draws, against the grid's."""
    if c.model in FIXED and c.setting in DRAWS:
        return {"model": c.model, "setting": c.setting, "rule": f"fixed {FIXED[c.model]}", "layer": c.layer,
                "ok": c.layer == FIXED[c.model]}  # fmt: skip
    got, _ = FC.pick_layer(rows, m["layers"], "RL")
    return {"model": c.model, "setting": c.setting, "rule": f"donor-digit rule over {m['layers']}", "layer": got,
            "ok": got == c.layer}  # fmt: skip


# ---------------------------------------------------------------- the table


COLUMNS = (
    "model", "model_name", "family", "setting", "sentences", "k", "n", "layers", "runs",
    *(f"{o}_{x}" for o in OUTCOMES for x in ("n", "pct", "lo", "hi")),
    "off_list_n", "off_list_pct", "off_recall_n", "off_other_digit_n", "off_other_n", "off_case_n", "five_sum_pct",
    "another_slot1_n", "another_kpm1_n", "another_elsewhere_n", "another_unresolved_n",
    "another_slot1_expected", "another_kpm1_expected", "another_elsewhere_expected", "another_km1_n", "another_kp1_n",
)  # fmt: skip
SRC_COL = {"slot 1": "slot1", "k±1": "kpm1", "elsewhere": "elsewhere"}


def pct(x: float) -> float:
    """A share in percent, 2 decimals, clamped to [0, 100] (Wilson's bounds can miss 0 by a rounding error)."""
    return round(min(100.0, max(0.0, 100 * x)), 2)


def table_row(model: str, fam: str, setting: str, sentences: int, k: int, t: Tally, layers: list[int],
              runs: list[str]) -> dict[str, Any]:  # fmt: skip
    r: dict[str, Any] = {"model": model, "model_name": RB.NAME[model], "family": fam, "setting": setting,
                         "sentences": sentences, "k": k, "n": t.n, "layers": " ".join(map(str, layers)),
                         "runs": " ".join(runs)}  # fmt: skip
    for o in OUTCOMES:
        p, lo, hi = wilson(t.count(o), t.n)
        r |= {f"{o}_n": t.count(o), f"{o}_pct": pct(p), f"{o}_lo": pct(lo), f"{o}_hi": pct(hi)}
    r |= {"off_list_n": t.off(), "off_list_pct": pct(t.off() / t.n), "off_recall_n": t.roles["recall"],
          "off_other_digit_n": t.roles["other_digit"], "off_other_n": t.roles["other"],
          "off_case_n": sum(t.case.values()), "five_sum_pct": pct(sum(t.count(o) for o in OUTCOMES) / t.n)}  # fmt: skip
    for s, col in SRC_COL.items():
        r[f"another_{col}_n"] = t.sources[s]
        r[f"another_{col}_expected"] = round(t.expected[s], 2)
    r |= {"another_unresolved_n": t.sources["unresolved"], "another_km1_n": t.sources["k-1"],
          "another_kp1_n": t.sources["k+1"]}  # fmt: skip
    return r


def collect(grid_dir: Path, repo: Path = pins.REPO_ROOT) -> dict[str, Any]:
    """Every grid cell's tallies, the per-draw and pooled table rows, and the checks."""
    cells, missing = grid_cells(grid_dir)
    rows_out: list[dict[str, Any]] = []
    checks: dict[str, list] = {"grid": [], "verdict": [], "layer": [], "slots": [], "sum": []}
    runs: list[dict[str, Any]] = []
    pooled: dict[tuple[str, str, int], Tally] = {}
    pooled_meta: dict[str, tuple[list[int], list[str]]] = {}
    for c in cells:
        m, rows, items = load_run(c.run, c.level, repo)
        t, slot_check = tally(rows, items, c.layer, c.sentences)
        fams = sorted({f for f, _ in t})
        outcomes = repo / PS_RESULTS / c.run / "outcomes.jsonl"
        runs.append({"model": c.model, "setting": c.setting, "run": c.run, "layer": c.layer, "level": c.level,
                     "sentences": c.sentences, "manifest_families": m["families"], "families": fams,
                     "n": {f: sum(x.n for (ff, _), x in t.items() if ff == f) for f in fams},
                     "outcomes_sha256": hashlib.sha256(outcomes.read_bytes()).hexdigest()})  # fmt: skip
        checks["grid"] += grid_check(c, t)
        if (v := verdict_check(c, t, repo)) is not None:
            checks["verdict"].append(v)
        checks["layer"].append(layer_check(c, m, rows))
        checks["slots"].append({"model": c.model, "setting": c.setting, **slot_check})
        for (fam, k), x in sorted(t.items()):
            rows_out.append(table_row(c.model, fam, c.setting, c.sentences, k, x, [c.layer], [c.run]))
            if c.setting in DRAWS:
                pooled.setdefault((c.model, fam, k), Tally()).add(x)
        if c.setting in DRAWS:
            meta = pooled_meta.setdefault(c.model, ([], []))
            meta[0].append(c.layer)
            meta[1].append(c.run)
    for (model, fam, k), x in pooled.items():
        rows_out.append(table_row(model, fam, POOLED, 5, k, x, *pooled_meta[model]))
    for r in rows_out:
        total = sum(r[f"{o}_n"] for o in OUTCOMES) + r["off_list_n"]
        checks["sum"].append({"model": r["model"], "family": r["family"], "setting": r["setting"], "k": r["k"],
                              "counts_sum_to_n": total == r["n"], "five_sum_pct": r["five_sum_pct"]})  # fmt: skip
    order = {k: i for i, k in enumerate(RB.ORDER)}
    settings = [*DRAWS, POOLED, "8 sentences", "12 sentences"]
    rows_out.sort(key=lambda r: (order[r["model"]], FAMILIES.index(r["family"]), settings.index(r["setting"]), r["k"]))
    return {"cells": cells, "missing": missing, "rows": rows_out, "checks": checks, "runs": runs}


# ---------------------------------------------------------------- writing


def sources_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per model, family and list (5 pooled, 8, 12), over every k: another listed answer's sources and baseline."""
    out = []
    groups: dict[tuple[str, str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        if r["setting"] not in DRAWS:
            groups[(r["model"], r["family"], r["setting"])].append(r)
    for (model, fam, setting), rs in groups.items():
        n = sum(r["another_n"] for r in rs)
        d: dict[str, Any] = {"model": model, "family": fam, "setting": setting, "answers": sum(r["n"] for r in rs),
                             "another_n": n}  # fmt: skip
        for s, col in SRC_COL.items():
            obs, exp = sum(r[f"another_{col}_n"] for r in rs), sum(r[f"another_{col}_expected"] for r in rs)
            d[s] = {"n": obs, "pct": pct(obs / n) if n else None, "uniform_pct": pct(exp / n) if n else None}
        d |= {"unresolved": sum(r["another_unresolved_n"] for r in rs), "k-1_n": sum(r["another_km1_n"] for r in rs),
              "k+1_n": sum(r["another_kp1_n"] for r in rs)}  # fmt: skip
        out.append(d)
    return out


def off_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per model, family and list (5 pooled, 8, 12) with any answer off the list: how many, of which kind, the largest
    share at one k, and how many name an outcome when case is ignored."""
    groups: dict[tuple[str, str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        if r["setting"] not in DRAWS:
            groups[(r["model"], r["family"], r["setting"])].append(r)
    out = []
    for (model, fam, setting), rs in groups.items():
        off = sum(r["off_list_n"] for r in rs)
        if off:
            n = sum(r["n"] for r in rs)
            out.append({"model": model, "family": fam, "setting": setting, "n": n, "off_list_n": off,
                        "off_list_pct": pct(off / n), "max_pct_at_one_k": max(r["off_list_pct"] for r in rs),
                        **{c: sum(r[f"off_{c}_n"] for r in rs) for c in ("recall", "other_digit", "other", "case")}})  # fmt: skip
    return out


def fmt_share(r: dict[str, Any], o: str) -> str:
    return f"{r[f'{o}_pct']:.0f}% [{r[f'{o}_lo']:.0f}, {r[f'{o}_hi']:.0f}]"


def markdown(res: dict[str, Any], summary: dict[str, Any]) -> str:
    rows = [r for r in res["rows"] if r["setting"] not in DRAWS]
    head = ("| k | n | order | identity | unchanged | another digit | donor's digit | off list | five sum |",
            "|---:|---:|---|---|---|---|---|---:|---:|")  # fmt: skip
    out = [f"# Patched-answer outcomes per asked slot (finding 5), {summary['stamp']}", "",
           f"Source: `scripts/slot_outcomes.py` at {summary['commit']}, grid `{summary['grid']}`. k = the place of the "
           "donor's asked sentence; order = the original's sentence at k; identity = the original's sentence about "
           "the donor's entity; unchanged = the original's own answer; another digit = any other sentence of the "
           "original's list; donor's digit = the donor's own answer (absent from the original's list); off list = "
           "any other answer. Shares with Wilson 95% intervals over items; 5-sentence lists pooled over the three "
           "draws (each at its own layer); the per-draw rows are in table.csv.", "",
           f"Checks: {summary['checks_line']}", ""]  # fmt: skip
    groups: dict[tuple[str, str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        groups[(r["model"], r["family"], r["setting"])].append(r)
    for (model, fam, setting), rs in groups.items():
        out += [f"## {RB.NAME[model]}, {FAMILY_NAME[fam]}, {setting} (layers {rs[0]['layers']})", "", *head]
        for r in rs:
            out.append(f"| {r['k']} | {r['n']} | " + " | ".join(fmt_share(r, o) for o in OUTCOMES)
                       + f" | {r['off_list_pct']:.1f}% | {r['five_sum_pct']:.1f}% |")  # fmt: skip
        out.append("")
    out += ["## Where another listed digit comes from (every k pooled)", "",
            "Observed % of the another-digit answers (uniform-pick baseline in brackets); slot 1 = the list's first "
            "sentence; k±1 = a neighbour of the asked place that is not slot 1 (its answers split into k-1 / k+1).",
            "", "| model | family | list | answers | another digit | slot 1 | k±1 | k-1 / k+1 | elsewhere | unresolved |",
            "|---|---|---|---:|---:|---|---|---:|---|---:|"]  # fmt: skip
    for d in summary["another_sources"]:
        cells = [f"{d[s]['pct']:.0f}% ({d[s]['uniform_pct']:.0f}%)" if d["another_n"] else "-" for s in SOURCES]
        cells.insert(2, f"{d['k-1_n']} / {d['k+1_n']}")
        out.append(f"| {RB.SHORT[d['model']]} | {d['family']} | {d['setting']} | {d['answers']} | {d['another_n']} | "
                   + " | ".join(cells) + f" | {d['unresolved']} |")  # fmt: skip
    out += ["", "## Answers off the list (where the five shares fall short of 100%)", "",
            "recall = a digit the model recalls about a listed entity; other digit = a digit no outcome names; other = "
            "anything else (a word, the end-of-turn token); same word, other case = off-list answers that name one of "
            "the five outcomes if case is ignored (' Red' for 'red'; pointer_swap's roles, which the grid uses, count "
            "them off the list).", "",
            "| model | family | list | answers | off list | largest at one k | recall | other digit | other | same word, "
            "other case |", "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for d in summary["off_list"]:
        out.append(f"| {RB.SHORT[d['model']]} | {d['family']} | {d['setting']} | {d['n']} | {d['off_list_n']} "
                   f"({d['off_list_pct']:.1f}%) | {d['max_pct_at_one_k']:.1f}% | {d['recall']} | {d['other_digit']} | "
                   f"{d['other']} | {d['case']} |")  # fmt: skip
    return "\n".join(out) + "\n"


def checks_line(checks: dict[str, list]) -> str:
    g, v, la, s, su = (checks[k] for k in ("grid", "verdict", "layer", "slots", "sum"))
    off = [x for x in su if x["five_sum_pct"] != 100.0]
    return (f"grid n and point value {sum(x['ok'] for x in g)}/{len(g)} parts match; saved verdicts' per-k counts "
            f"{sum(x['ok'] for x in v)}/{len(v)} match; layer {sum(x['ok'] for x in la)}/{len(la)} match; counts sum "
            f"to n in {sum(x['counts_sum_to_n'] for x in su)}/{len(su)} rows; the five shares sum to 100% in "
            f"{len(su) - len(off)}/{len(su)} rows (the rest: answers off the list); on-list answers whose slot agrees "
            f"with the role: {sum(x['agrees'] for x in s)}, not resolvable from the token: "
            f"{sum(x['unresolved'] for x in s)}.")  # fmt: skip


def commit() -> str:
    try:
        sha = subprocess.run(["git", "-C", str(pins.REPO_ROOT), "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()  # fmt: skip
        dirty = subprocess.run(["git", "-C", str(pins.REPO_ROOT), "status", "--porcelain", "--", "scripts/slot_outcomes.py"],
                               capture_output=True, text=True, check=True).stdout.strip()  # fmt: skip
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return sha + (" (scripts/slot_outcomes.py modified)" if dirty else "")


def write(res: dict[str, Any], grid_dir: Path, out_root: Path, argv: list[str]) -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d = out_root / stamp
    d.mkdir(parents=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(res["rows"])
    (d / "table.csv").write_text(buf.getvalue())
    try:
        grid = str(grid_dir.resolve().relative_to(pins.REPO_ROOT))
    except ValueError:
        grid = str(grid_dir)
    fails = {k: [x for x in v if not x.get("ok", x.get("counts_sum_to_n", True))] for k, v in res["checks"].items()}
    summary: dict[str, Any] = {
        "stamp": stamp, "commit": commit(), "grid": grid, "command": "uv run python scripts/slot_outcomes.py "
        + " ".join(argv), "definitions": __doc__.split("Cells:")[0].strip(),  # type: ignore[union-attr]
        "families": {fam: FAMILY_NAME[fam] for fam in FAMILIES}, "pooled_setting": POOLED,
        "missing_cells": res["missing"], "runs": res["runs"],
        "checks_line": checks_line(res["checks"]), "check_failures": {k: v for k, v in fails.items() if v},
        "checks": res["checks"], "another_sources": sources_summary(res["rows"]), "off_list": off_summary(res["rows"]),
    }  # fmt: skip
    (d / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    (d / "table.md").write_text(markdown(res, summary))
    return d


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=str(GRID), help="a results/cross_model/<stamp> folder with grid.json")
    ap.add_argument("--out", default=str(OUT), help="parent of the new <UTC stamp> folder")
    a = ap.parse_args(argv)
    res = collect(Path(a.grid))
    d = write(res, Path(a.grid), Path(a.out), argv)
    summary = json.loads((d / "summary.json").read_text())
    print(summary["checks_line"])
    if summary["check_failures"]:
        print("CHECK FAILURES:", json.dumps(summary["check_failures"], indent=1))
    print("wrote", d)
    return 1 if summary["check_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
