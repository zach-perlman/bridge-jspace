"""An independent recount of the README's conflict-test and routes numbers (Dan 29 Oct 11:40 / 11:45, jobs/c3/batch53.yaml
additions_1140 item 1 and verify_prep_1145 item 2), written from scratch: standard library only, no import of the
pipeline's scoring code (scripts/x0_necessity.py, scripts/x6_routes.py, ...) or of the review code
(src/bridge_jspace/review/). It reads the raw per-item files and the README, and reports every difference.

What it recomputes, per model (the 9B is the brief's; the others the same way, as their files allow):
  the item set     from cases.jsonl + competence.jsonl: a scene is eligible if both readers said and read both answers
                   right (original and changed prompt); the first N eligible in case order (N = the run's manifest; the
                   routes test per condition; Lightning's excluded dev scenes left out), checked against the scenes
                   the run's outcomes.jsonl holds at the layer
  conflict test    switches lost beyond a random part = (switches kept without the random part - switches kept without
                   the lens part) / switches with the whole change, per reader, at the layer fixed in advance; the gap
                   = recall - lookup. The X0 runs store the switched flag (the 9B's stores no top token), so this
                   counts the stored flags
  routes (C2)      the lookup's route under each arm from the raw top-token id against the case's route_tokens (the
                   token each route predicts), not from the stored route label; the share of the C2 items per route;
                   the stored label is compared on the side
Each number is compared with what the README shows (docs/depth/README.md, the number before its <!-- src --> comment,
2 decimals) and with its source (docs/depth/x0_numbers.json, or data/figures/depth/data.csv by model and quantity).

uv run python scripts/verify_independent.py             # all models -> review/verify_independent.json
uv run python scripts/verify_independent.py --models 9b
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = "docs/depth/README.md"
NUMBERS = "docs/depth/x0_numbers.json"
DATA_CSV = "data/figures/depth/data.csv"
OUT = "review/verify_independent.json"
READERS = ("PP", "PM")  # lookup, recall
ROUTES = ("identity", "position", "value", "original")
ROUTE_ARMS = (
    "whole",
    "no_alf",
    "no_alf_rand",
    "keep_alf",
    "keep_alf_rand",
)  # C2, the README's routes and address claims
MODEL_COL = {"9b": "qwen3.5-9b", "27b": "qwen3.6-27b", "122b": "qwen3.5-122b-a10b", "muse": "muse-glimmer-30b",
             "lightning": "nemotron-3.5-lightning"}  # fmt: skip
# Lightning has no x0_numbers keys: its README numbers are data.csv rows (model column, quantity); its runs:
LIGHTNING = {"conflict": "results/x0_necessity/nem35l_x52_conflict", "routes": "results/x6_routes/nem35l_x52_routes"}


def jsonl(root: Path, rel: str) -> list[dict]:
    p = root / rel
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def num(text: str) -> float | None:
    m = re.match(r"\s*([−-]?\d+(?:\.\d+)?)", text)
    return float(m.group(1).replace("−", "-")) if m else None


def decimals(text: str) -> int:
    m = re.match(r"\s*[−-]?\d+(?:\.(\d+))?", text)
    return len(m.group(1) or "") if m else 0


# ------------------------------------------------------------------------------------------------- what is claimed
def readme_numbers(root: Path) -> dict[str, list[str]]:
    """Every number the README shows before a <!-- src: ... | key --> comment: {"x0:<key>" | "csv:<quantity>": [shown]}."""
    text = (root / README).read_text()
    out: dict[str, list[str]] = defaultdict(list)
    pat = re.compile(r"([−-]?\d+(?:\.\d+)?)(%?)(?:\s*\[[^\]]*\])?<!-- src: ([^|]+?) \\?\| (.+?) -->")
    for m in pat.finditer(text):
        src, key = m.group(3).strip(), m.group(4).strip()
        tag = "x0" if src == NUMBERS else "csv" if src == DATA_CSV else src
        out[f"{tag}:{key}"].append(m.group(1) + m.group(2))
    out.update(csv_by_model(root, text))
    return dict(out)


TEMPLATE = "docs/depth/README.template.md"
MODEL_OF = {"9b": "qwen3.5-9b", "27b": "qwen3.6-27b", "muse": "muse-glimmer-30b", "122b": "qwen3.5-122b-a10b",
            "lightning": "nemotron-3.5-lightning", "nemotron-3.5-lightning": "nemotron-3.5-lightning"}  # fmt: skip


def csv_by_model(root: Path, text: str) -> dict[str, list[str]]:
    """A multi-model line shows one number per model under one src comment (the data.csv quantity), so the comment alone
    does not say whose number it is. The template's {{d|figure|model|quantity}} / {{dp|...}} markers do, and they render,
    in order, to the data.csv src comments of the page: {"csvm:<model column>:<quantity>": [shown]}. Empty when the
    template is absent or its markers and the page's comments do not line up (the old per-quantity list then applies)."""
    tpl = root / TEMPLATE
    if not tpl.exists():
        return {}
    marks = re.findall(r"\{\{(?:d|dp)\|[^|}]*\|([^|}]*)\|([^}]*)\}\}", tpl.read_text())
    comment = re.compile(r"<!-- src: " + re.escape(DATA_CSV) + r" \\?\| (.+?) -->")
    found = list(comment.finditer(text))
    if len(found) != len(marks) or any(m.group(1).strip() != q.strip() for m, (_, q) in zip(found, marks, strict=True)):
        return {}
    before = re.compile(r"([−-]?\d+(?:\.\d+)?)(%?)(?:\s*\[[^\]]*\])?$")
    out: dict[str, list[str]] = defaultdict(list)
    for m, (model, quantity) in zip(found, marks, strict=True):
        n = before.search(text[max(0, m.start() - 60) : m.start()])
        col = MODEL_OF.get(model.strip())
        if n and col:
            out[f"csvm:{col}:{quantity.strip()}"].append(n.group(1) + n.group(2))
    return dict(out)


def data_csv(root: Path) -> dict[tuple[str, str], list[str]]:
    out: dict[tuple[str, str], list[str]] = defaultdict(list)
    with (root / DATA_CSV).open() as f:
        for r in csv.DictReader(f):
            out[(r["model"], r["quantity"])].append(r["value"])
    return dict(out)


def compare(value: float, shown: list[str]) -> str:
    """match if every shown number equals the value at its own precision (2 decimals: within 0.005)."""
    if not shown:
        return "not shown"
    bad = [s for s in shown if (x := num(s.rstrip("%"))) is None
           or abs(value * (100 if s.endswith("%") else 1) - x) > 0.5 * 10 ** -decimals(s.rstrip("%")) + 1e-9]  # fmt: skip
    return "mismatch" if bad else "match"


# ------------------------------------------------------------------------------------------------------- item sets
def competence_ok(root: Path, run: str, key=lambda r: r["scene"]) -> dict:
    ok: dict = defaultdict(lambda: defaultdict(bool))
    for r in jsonl(root, f"{run}/competence.jsonl"):
        if r.get("rendering", "chat") == "chat":
            ok[key(r)][(r["reader"], r["variant"])] = bool(r["right"]) and bool(r["read_right"])
    return ok


def eligible(ok: dict, scenes: list[str]) -> list[str]:
    return [s for s in scenes if all(ok[s][(w, v)] for w in READERS for v in ("org", "alt"))]


# --------------------------------------------------------------------------------------------------- the conflict test
def conflict(root: Path, run: str) -> dict:
    man = json.loads((root / run / "manifest.json").read_text())
    layer, n = int(man["predicted"]), int(man["n"]["items"])
    cases = [c["scene"] for c in jsonl(root, f"{run}/cases.jsonl") if c.get("rendering", "chat") == "chat"]
    excl = set(man.get("excluded_scenes") or [])
    want = [s for s in eligible(competence_ok(root, run), cases) if s not in excl][:n]
    rows = [
        r for r in jsonl(root, f"{run}/outcomes.jsonl") if r["layer"] == layer and r.get("rendering", "chat") == "chat"
    ]
    have = sorted({r["scene"] for r in rows if r["arm"] == "whole"})
    sw: dict = defaultdict(dict)  # (scene, reader) -> arm -> switched
    for r in rows:
        if r["arm"] in ("whole", "none") or (r["dict"], r["k"], r["omp"]) == ("jpp", 25, "signed"):
            sw[(r["scene"], r["reader"])][r["arm"]] = int(r["switched"])
    ex = {}
    for w in READERS:
        mine = [sw[(s, w)] for s in want]
        whole = sum(x.get("whole", 0) for x in mine)
        part, rand = sum(x.get("no_part", 0) for x in mine), sum(x.get("no_rand", 0) for x in mine)
        ex[w] = {"n": len(mine), "whole": whole, "no_part": part, "no_rand": rand, "value": (rand - part) / whole}
    return {"run": run, "layer": layer, "items": {"recomputed": len(want), "in outcomes": len(have),
            "same": sorted(want) == have}, "lookup": ex["PP"], "recall": ex["PM"],
            "gap": ex["PM"]["value"] - ex["PP"]["value"]}  # fmt: skip


# ------------------------------------------------------------------------------------------------------------ routes
def routes(root: Path, runs: list[str]) -> dict:
    main = runs[0]
    man = json.loads((root / main / "manifest.json").read_text())
    n = int(man.get("n_per_condition") or 300)
    cases = {c["scene"]: c for c in jsonl(root, f"{main}/cases.jsonl") if c["condition"] == "C2"}
    want = eligible(competence_ok(root, main), list(cases))[:n]
    top: dict = {}
    stored_agree = Counter()
    have = set()
    for run in runs:
        for r in jsonl(root, f"{run}/outcomes.jsonl"):
            if r["condition"] != "C2" or r["reader"] != "PP" or r["arm"] not in ROUTE_ARMS:
                continue
            if run == main and r["arm"] == "whole":
                have.add(r["scene"])
            if (r["scene"], r["arm"]) in top:  # the first run that has the arm (the main run, then the keep-only run)
                continue
            rt = cases[r["scene"]]["route_tokens"]
            mine = next((k for k in ROUTES if rt.get(k) == r["top"]), "other")
            top[(r["scene"], r["arm"])] = mine
            stored_agree["agree" if mine == r.get("route") else "differ"] += 1
    shares = {}
    for arm in ROUTE_ARMS:
        got = [top[(s, arm)] for s in want if (s, arm) in top]
        if got:
            c = Counter(got)
            shares[arm] = {"n": len(got), **{k: c[k] / len(got) for k in (*ROUTES, "other")}}
    return {"runs": runs, "items": {"recomputed": len(want), "in outcomes": len(have), "same": set(want) == have},
            "route label from the top token agrees with the stored label": dict(stored_agree), "shares": shares}  # fmt: skip


# ------------------------------------------------------------------------------------------------------------ runner
def run_dir(source: str) -> str:
    """A run dir from an x0_numbers / data.csv source path (its outcomes.jsonl or a verdict file inside it)."""
    p = source.split("/")
    i = next(k for k, x in enumerate(p) if x.startswith(("outcomes", "verdict-")))
    return "/".join(p[:i])


def model_runs(numbers: dict, mk: str) -> dict:
    if mk == "lightning":
        return {"conflict": LIGHTNING["conflict"], "routes": [LIGHTNING["routes"]]}
    pre = "rtg" if mk == "122b" else "rt"
    main = run_dir(numbers[f"{pre}_C2_whole_identity_{mk}"]["source"])
    keep = run_dir(numbers[f"rtk_C2_keep_alf_position_{mk}"]["source"])
    return {
        "conflict": run_dir(numbers[f"lk_excess_{mk}"]["source"]),
        "routes": [main] + ([keep] if keep != main else []),
    }


def rows_for(mk: str, res: dict, numbers: dict, shown: dict, csvd: dict) -> list[dict]:
    """(quantity, recomputed, README shown, source value, status) for one model."""
    col = MODEL_COL[mk]
    out = []

    def add(name: str, val: float, key: str | None, quantity: str | None) -> None:
        if key:
            src = numbers.get(key, {}).get("text", "")
            shown_ = shown.get(f"x0:{key}", [])
            ref = f"x0_numbers.json {key}"
        else:
            src = " / ".join(csvd.get((col, quantity), []))
            shown_ = shown.get(f"csvm:{col}:{quantity}") or shown.get(
                f"csv:{quantity}", []
            )  # the model's own numbers where the template says whose they are
            ref = f"data.csv ({col}) {quantity}"
        src_ok = compare(val, [src]) if src else "no source"
        rd_ok = compare(val, shown_) if shown_ else "not shown"
        status = "mismatch" if "mismatch" in (src_ok, rd_ok) else "match" if src_ok == "match" else src_ok
        out.append({"model": mk, "quantity": name, "value": val, "readme": shown_, "source": src, "ref": ref,
                    "vs source": src_ok, "vs README": rd_ok, "status": status})  # fmt: skip

    c = res["conflict"]
    light = mk == "lightning"
    add(
        "conflict: lookup, switches lost beyond a random part",
        c["lookup"]["value"],
        None if light else f"lk_excess_{mk}",
        "conflict: lookup, switches lost beyond a random part",
    )
    add(
        "conflict: recall, switches lost beyond a random part",
        c["recall"]["value"],
        None if light else f"rc_excess_{mk}",
        "conflict: recall, switches lost beyond a random part",
    )
    add(
        "conflict: the gap (recall - lookup)",
        c["gap"],
        None if light else f"contrast_{mk}",
        "main test (two people swap picks): gap",
    )
    pre = "rtg" if mk == "122b" else "rt"
    for arm, sh in res["routes"]["shares"].items():
        for route in ("identity", "position"):
            if light:
                key, q = None, f"another item moved, {arm}: {route} share"
            else:
                key = f"rtk_C2_{arm}_{route}_{mk}" if arm.startswith("keep") else f"{pre}_C2_{arm}_{route}_{mk}"
                if key not in numbers and arm.startswith("keep"):  # Muse's keep arms are in its main run
                    key = f"rt_C2_{arm}_{route}_{mk}"
                q = None
            if key and key not in numbers:
                continue
            if q and (col, q) not in csvd:
                continue
            add(f"routes C2, {arm}: {route} share", sh[route], key, q)
    return out


def main(argv: list[str] | None = None, root: Path = ROOT) -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=list(MODEL_COL))
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)
    numbers = json.loads((root / NUMBERS).read_text())
    shown, csvd = readme_numbers(root), data_csv(root)
    report: dict = {"what": __doc__.split("\n\n")[0], "models": {}, "rows": []}
    for mk in a.models:
        runs = model_runs(numbers, mk)
        res = {"conflict": conflict(root, runs["conflict"]), "routes": routes(root, runs["routes"])}
        report["models"][mk] = res
        report["rows"] += rows_for(mk, res, numbers, shown, csvd)
    bad = [r for r in report["rows"] if r["status"] == "mismatch"]
    sets = {mk: (r["conflict"]["items"]["same"], r["routes"]["items"]["same"]) for mk, r in report["models"].items()}
    page = {k: sum(r["vs README"] == k for r in report["rows"]) for k in ("match", "mismatch", "not shown")}
    report["summary"] = {"rows": len(report["rows"]), "match": sum(r["status"] == "match" for r in report["rows"]),
                         "mismatch": len(bad), "README": page,
                         "item sets recomputed = the runs' (conflict, routes)": sets}  # fmt: skip
    (root / a.out).parent.mkdir(parents=True, exist_ok=True)
    (root / a.out).write_text(json.dumps(report, indent=1) + "\n")
    for r in report["rows"]:
        print(f"{r['model']:>9} | {r['quantity']:<52} | {r['value']:+.4f} | README {', '.join(r['readme']) or '-':<14} | "
              f"source {r['source'][:22]:<22} | {r['status']}")  # fmt: skip
    print(f"item sets recomputed = the runs' (conflict, routes): {sets}")
    print(f"{report['summary']['match']} match, {len(bad)} mismatch of {len(report['rows'])}; wrote {a.out}")
    return report


if __name__ == "__main__":
    sys.exit(1 if main()["summary"]["mismatch"] else 0)
