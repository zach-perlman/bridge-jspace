"""Each view's item set per model, read from its runs' per-item files only, and deterministic samples of it.

An item is one (scene, reader) read under the view's arms (routes: per condition; x8: one write j -> k at dose s).
Every item carries the rows of all readers of its scene, so a card can show both questions; the sampled reader's rows
decide its class and its checks. Items outside the claim's set (ineligible, beyond the first N, a superseded run) are
loaded only on request and are never mixed into the claim's sample.
"""

from __future__ import annotations

import collections
import json
import random
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parents[3]
VIEWS_FILE = REPO / "docs" / "review_views.yaml"
READERS = ("PP", "PM")  # lookup, recall
READER_NAME = {"PP": "lookup", "PM": "recall"}

Item = dict[str, Any]


@lru_cache(maxsize=1)
def spec() -> dict:
    return yaml.safe_load(VIEWS_FILE.read_text())


def view(view_id: str) -> dict:
    return next(v for v in spec()["views"] if v["id"] == view_id)


def shown() -> list[dict]:
    """The views in the dashboard (status phase1 or phase2); "later" ones are listed in the views file only."""
    return [v for v in spec()["views"] if v.get("status") in ("phase1", "phase2")]


@lru_cache(maxsize=64)
def read_jsonl(path: str) -> tuple[dict, ...]:
    p = REPO / path
    return tuple(json.loads(line) for line in p.read_text().splitlines() if line.strip()) if p.exists() else ()


def read_json(path: str) -> dict:
    p = REPO / path
    return json.loads(p.read_text()) if p.exists() else {}


@lru_cache(maxsize=1)
def legs() -> dict[str, int]:
    """The animals' legs, the recall's answers in the routes and x8 scenes (scripts/tasks_v2.py)."""
    import sys

    sys.path.insert(0, str(REPO))
    from scripts import tasks_v2 as T

    return dict(T.DOMAINS["animals"].values)


def layer_of(v: dict, model: str, run: str) -> int:
    if v["filters"].get("layer") == "run":
        return int(read_json(f"{run}/manifest.json")["layer"])
    return int(spec()["models"][model]["layer"])


def competence_status(run: str, scene: str, rendering: str | None = "chat") -> str:
    """Why a generated case is outside the item set: competence failed (org or alt not said / read right by a reader),
    or eligible but beyond the first N taken."""
    rows = [r for r in read_jsonl(f"{run}/competence.jsonl") if r["scene"] == scene
            and (rendering is None or r.get("rendering", rendering) == rendering)]  # fmt: skip
    if not rows:
        return "not read (no competence row)"
    bad = [f"{r['reader']}/{r['variant']}" for r in rows if not (r["right"] and r["read_right"])]
    return f"ineligible: competence ({', '.join(bad)})" if bad else "eligible, beyond the first N taken"


# ------------------------------------------------------------------------------------------------ the main test (x0)
def x0_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    f = v["filters"]
    layer, rend = layer_of(v, model, run), f.get("rendering", "chat")
    cases = {c["scene"]: c for c in read_jsonl(f"{run}/cases.jsonl") if c.get("rendering", "chat") == rend}
    idx = {(r["scene"], r["reader"], r["arm"], r["dict"], r["k"], r["omp"]): r for r in read_jsonl(f"{run}/outcomes.jsonl")
           if r["layer"] == layer and r.get("rendering", "chat") == rend}  # fmt: skip
    shares = {
        (r["scene"], r["dict"], r["k"], r["omp"]): r for r in read_jsonl(f"{run}/shares.jsonl") if r["layer"] == layer
    }
    arms = {label: tuple(a) for label, a in f["arms"].items()}
    done = sorted({k[0] for k in idx if k[2] == "whole"})
    out = []
    for scene in done if in_set else sorted(set(cases) - set(done)):
        case = cases.get(scene)
        rows = {w: {label: idx.get((scene, w, *a)) for label, a in arms.items()} for w in READERS}
        sh = {}
        for arm, d, k, omp in arms.values():
            s = shares.get((scene, d, k, omp))
            if s and arm == "no_part":  # k = 25 is the main part; the k-curve's others named by k
                sh["jpp" if k == 25 else f"jpp_k{k}"] = s["share"]
                sh["random part" if k == 25 else f"random part_k{k}"] = s["rand_share"]
        for w in f.get("readers", READERS):
            whole = rows[w].get("whole")
            status = "in set" if in_set else competence_status(run, scene, rend)
            out.append(
                _item(v, model, run, layer, scene, w, None, case, rows, sh, whole["role"] if whole else status, status)
            )
    return out


def _item(v, model, run, layer, scene, reader, condition, case, rows, shares, cls, status, extra=None) -> Item:
    tail = f"|{condition}" if condition else ""
    tail += f"|{extra['kind']}|{extra['j']}-{extra['k']}|s{extra['s']}" if extra else ""
    return {"id": f"{model}|{run.split('/')[-1]}|{scene}|{reader}{tail}", "view": v["id"], "kind": v["kind"],
            "model": model, "run": run, "layer": layer, "scene": scene, "reader": reader, "condition": condition,
            "case": case, "rows": rows, "shares": shares, "cls": cls, "status": status, "in_set": status == "in set",
            "x8": extra or {}}  # fmt: skip


# --------------------------------------------------------------------------------------------- routes (x6_routes)
def routes_items(v: dict, model: str, runs: list[str], in_set: bool = True) -> list[Item]:
    f = v["filters"]
    first = runs[0]
    layer = layer_of(v, model, first)
    conds = f.get("conditions", ["C0", "C1", "C2"])
    cases = {(c["scene"], c["condition"]): c for c in read_jsonl(f"{first}/cases.jsonl") if c["condition"] in conds}
    by_run = {run: {(r["scene"], r["condition"], r["reader"], r["arm"]): r for r in read_jsonl(f"{run}/outcomes.jsonl")}
              for run in runs}  # fmt: skip
    joined_cases = {
        run: {(c["scene"], c["condition"]): c for c in read_jsonl(f"{run}/cases.jsonl")} for run in runs[1:]
    }
    norms = {(r["scene"], r["condition"]): r for r in read_jsonl(f"{first}/norms.jsonl")}
    done = sorted({(k[0], k[1]) for k in by_run[first] if k[3] == "whole" and k[1] in conds})
    out = []
    for key in done if in_set else sorted(set(cases) - set(done)):
        scene, cond = key
        rows: dict[str, dict] = {}
        for w in READERS:
            rows[w] = {}
            for label, arm in f["arms"].items():
                for run in runs:
                    r = by_run[run].get((scene, cond, w, arm))
                    if r is not None:
                        rows[w][label] = {**r, "_run": run.split("/")[-1]} if run != first else r
                        break
        nm = norms.get(key, {})
        sh = {k.removeprefix("share_"): val for k, val in nm.items() if k.startswith("share_")}
        if "norm" in nm:
            sh["norm"] = nm["norm"]
        case = cases.get(key)
        if case is not None:
            case = {**case, "_joined": {run.split("/")[-1]: joined_cases[run].get(key) for run in runs[1:]}}
        for w in f.get("readers", READERS):
            whole = rows[w].get("whole")
            status = "in set" if in_set else competence_status(first, scene, None)
            cls = (
                (route_class(whole, cond) if w == "PP" else ("follows S" if whole["switched"] else "stays"))
                if whole
                else status
            )
            out.append(_item(v, model, first, layer, scene, w, cond, case, rows, sh, cls, status))
    return out


def route_class(row: dict, condition: str) -> str:
    """The stored route; C0 stores "other" for a switch (route_tokens has no "switch"), so C0's class takes the stored
    switched flag: switch / original / other."""
    if condition == "C0":
        return "switch" if row["switched"] else "original" if row["route"] == "original" else "other"
    return row["route"]


# --------------------------------------------------------------------------------- pointer on the main items (massmean)
def massmean_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    if not in_set:  # its item rule is applied in the script; no file lists the items it left out
        return []
    f = v["filters"]
    m = read_json(f"{run}/manifest.json")
    single = f"results/x0_necessity/{m['single']}"
    cases = {c["scene"]: c for c in read_jsonl(f"{single}/cases.jsonl") if c.get("rendering", "chat") == "chat"}
    idx = {(r["scene"], r["reader"], r["arm"]): r for r in read_jsonl(f"{run}/outcomes.jsonl")}
    out = []
    for scene in sorted({k[0] for k in idx if k[2] == "whole"}):
        rows = {w: {label: idx.get((scene, w, arm)) for label, arm in f["arms"].items()} for w in READERS}
        any_row = next(r for r in rows["PP"].values() if r)
        sh = {k.removeprefix("share_"): val for k, val in any_row.items() if k.startswith("share_")}
        case = cases.get(scene)
        for w in f.get("readers", READERS):
            whole = rows[w].get("whole")
            out.append(_item(v, model, run, int(m["layer"]), scene, w, None, case, rows, sh, whole["role"] if whole else "-",
                             "in set", None))  # fmt: skip
    return out


# ------------------------------------------------------------------------------------------------ x8 writes (batch 44)
def x8_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    if not in_set or not (REPO / run / "outcomes.jsonl").exists():
        return []
    f = v["filters"]
    m = read_json(f"{run}/manifest.json")
    cases = {c["scene"]: c for c in read_jsonl(f"{v['cases_from'][model]}/cases.jsonl") if c["condition"] == "C2"}
    rows = read_jsonl(f"{run}/outcomes.jsonl")
    none = {(r["scene"], r["reader"]): r for r in rows if r["kind"] == "none"}
    by = collections.defaultdict(dict)
    for r in rows:
        if r["kind"] in f.get("kinds", ["write", "random"]) and r["s"] in f.get("s", [1, 2, 4]):
            by[(r["scene"], r["kind"], r["j"], r["k"], r["s"])][r["reader"]] = r
    out = []
    for (scene, kind, j, k, s), per in sorted(by.items(), key=lambda kv: tuple(map(str, kv[0]))):
        rws = {w: {"unwritten": none.get((scene, w)), f"{kind} s = {s:g}": per.get(w)} for w in READERS}
        extra = {"kind": kind, "j": j, "k": k, "s": s, "norm": next(iter(per.values())).get("norm")}
        for w in f.get("readers", READERS):
            r = per.get(w)
            if r is None:
                continue
            cls = r["class"] if w == "PP" else ("changed" if r["changed"] else "unchanged")
            out.append(_item(v, model, run, int(m["layer"]), scene, w, None, cases.get(scene), rws,
                             {"write norm": extra["norm"]}, cls, "in set", extra))  # fmt: skip
    return out


LOADERS = {"x0": x0_items, "massmean": massmean_items, "x8": x8_items}


@lru_cache(maxsize=256)
def _items(view_id: str, model: str, which: str) -> tuple[Item, ...]:
    """which: "set" (the claim's items), "out" (outside it: ineligible / beyond N), "superseded"."""
    v = view(view_id)
    runs = v.get("superseded", {}).get(model, []) if which == "superseded" else v.get("runs", {}).get(model, [])
    runs = [r for r in runs if (REPO / r).exists()]
    if not runs:
        return ()
    in_set = which == "set"
    if v["kind"] == "routes":
        got = []
        joined = which != "superseded" and v.get("join", True)  # join: false -> every run its own item set
        for chain in [runs] if joined else [[r] for r in runs]:
            got += routes_items(v, model, chain, in_set or which == "superseded")
    else:
        got = [it for run in (runs[:1] if which != "superseded" else runs)
               for it in LOADERS[v["kind"]](v, model, run, in_set or which == "superseded")]  # fmt: skip
    if which == "superseded":
        for it in got:
            it["status"], it["in_set"] = f"superseded run (by {v['runs'][model][0].split('/')[-1]})", False
    return tuple(got)


def items(view_id: str, model: str, which: str = "set") -> list[Item]:
    return list(_items(view_id, model, which))


def facets(it: Item, params: dict) -> bool:
    """The URL's filters beyond model: reader, condition (routes), s and kind (x8)."""
    if params.get("reader") not in (None, "", "all") and it["reader"] != params["reader"]:
        return False
    if params.get("condition") not in (None, "", "all") and it["condition"] != params["condition"]:
        return False
    x8 = it["x8"]
    if x8 and params.get("s") not in (None, "", "all") and float(x8["s"]) != float(params["s"]):
        return False
    return not (x8 and params.get("kind") not in (None, "", "all") and x8["kind"] != params["kind"])


def sample(pool: list[Item], seed: int, n: int, mode: str, view_id: str, model: str, part: str = "set") -> list[dict]:
    """Deterministic samples: uniform over the pool (default), or stratified by reader x stored class, N per stratum;
    random.Random seeded by a string of seed, view, model and stratum. Returns [{stratum, population, items}]."""
    pool = sorted(pool, key=lambda it: it["id"])
    if mode == "stratified":
        groups = collections.defaultdict(list)
        for it in pool:
            groups[(it["reader"], it["cls"])].append(it)
        strata = [(f"{READER_NAME[w]} · {c}", g) for (w, c), g in sorted(groups.items())]
    else:
        strata = [("all", pool)]
    out = []
    for name, g in strata:
        rng = random.Random(f"{seed}|{view_id}|{model}|{mode}|{part}|{name}")
        out.append({"stratum": name, "population": len(g), "items": rng.sample(g, min(n, len(g)))})
    return out
