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
import re
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


def run_flags(run: str, keys: set[str] | None = None) -> list[str]:
    """What stopped a run or voids its items: a read gate failed or too few eligible items (gate.json, per condition or
    rendering; keys: only these, e.g. a view's rendering; x5: one gate for the run), or the routes test's C0 check failed
    (c0_check.json; x6_routes writes its outcomes before the check)."""
    gate = read_json(f"{run}/gate.json")
    out = ["read gate failed"] if gate.get("pass") is False else []
    for k, g in gate.get("gate", {}).items():
        if keys is not None and k not in keys:
            continue
        if isinstance(g, dict) and g.get("pass") is False:
            out.append(f"read gate failed: {k}")
        elif isinstance(g, dict) and g.get("enough") is False:
            out.append(f"too few eligible items: {k}")
    if read_json(f"{run}/c0_check.json").get("ok") is False:
        out.append("C0 check failed (c0_check.json)")
    return out


def run_state(run: str) -> str:
    """Whether a run has landed: "not run yet" (no run dir), "no outcomes.jsonl" with why (a gate that failed, or still
    running / stopped before its reads), or "landed"."""
    p = REPO / run
    if not p.exists():
        return "not run yet"
    if (p / "outcomes.jsonl").exists():
        return "landed"
    flags = run_flags(run)
    return (
        f"no outcomes.jsonl: {'; '.join(flags)}"
        if flags
        else "no outcomes.jsonl yet (running, or stopped before its reads)"
    )


def not_landed(v: dict, model: str) -> list[tuple[str, str]]:
    """The view's runs for the model (and the runs joined to them) that have not landed, with their state."""
    runs = [*v.get("runs", {}).get(model, []), *v.get("join_runs", {}).get(model, [])]
    return [(r, s) for r in runs if (s := run_state(r)) != "landed"]


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
def x0_items(
    v: dict, model: str, run: str, in_set: bool = True, cases_run: str | None = None, joined: tuple[str, ...] = ()
) -> list[Item]:
    """cases_run: the run whose cases.jsonl holds the prompts (default: this run); joined: runs whose rows give the
    arms this run does not have, by scene (marked "_run"; their prompts kept in the case's "_joined" for the check)."""
    f = v["filters"]
    layer, rend = layer_of(v, model, run), f.get("rendering", "chat")
    src = cases_run or run
    cases = {c["scene"]: c for c in read_jsonl(f"{src}/cases.jsonl") if c.get("rendering", "chat") == rend}
    idx = {jr: {(r["scene"], r["reader"], r["arm"], r["dict"], r["k"], r["omp"]): r for r in read_jsonl(f"{jr}/outcomes.jsonl")
                if r["layer"] == layer and r.get("rendering", "chat") == rend} for jr in (run, *joined)}  # fmt: skip
    shares = {(r["scene"], r["dict"], r["k"], r["omp"]): r for jr in (*joined[::-1], run)  # this run's own win
              for r in read_jsonl(f"{jr}/shares.jsonl") if r.get("layer", layer) == layer}  # fmt: skip
    joined_cases = {jr: {c["scene"]: c for c in read_jsonl(f"{jr}/cases.jsonl") if c.get("rendering", "chat") == rend}
                    for jr in joined}  # fmt: skip
    arms = {label: tuple(a) for label, a in f["arms"].items()}
    done = sorted({k[0] for k in idx[run] if k[2] == "whole"})

    def row(scene: str, w: str, a: tuple) -> dict | None:
        for jr, got in idx.items():
            r = got.get((scene, w, *a))
            if r is not None:
                return r if jr == run else {**r, "_run": jr.split("/")[-1]}
        return None

    out = []
    for scene in done if in_set else sorted(set(cases) - set(done)):
        case = cases.get(scene)
        if case is not None and joined:
            case = {**case, "_joined": {jr.split("/")[-1]: joined_cases[jr].get(scene) for jr in joined}}
        rows = {w: {label: row(scene, w, a) for label, a in arms.items()} for w in READERS}
        sh = {}
        for arm, d, k, omp in arms.values():
            s = shares.get((scene, d, k, omp))
            if s and arm == "no_part":  # J++ at k = 25 is the main part; the k-curve's others named by k
                sh[("jpp" if k == 25 else f"jpp_k{k}") if d == "jpp" else f"{d}_k{k}"] = s["share"]
                if "rand_share" in s:  # x0_parts stores none
                    sh["random part" if k == 25 else f"random part_k{k}"] = s["rand_share"]
        for w in f.get("readers", READERS):
            whole = rows[w].get("whole")
            status = "in set" if in_set else competence_status(src, scene, rend)
            out.append(
                _item(
                    v,
                    model,
                    run,
                    layer,
                    scene,
                    w,
                    None,
                    case,
                    rows,
                    sh,
                    whole_class(whole, case, w) if whole else status,
                    status,
                )
            )
    return out


def sentence_order(case: dict | None) -> dict[str, str]:
    """Whether a prompt's bridge's locker sentence comes before or after the asked person's pick sentence, in the
    original prompt (its bridge) and the changed one (its bridge): the README's "locker-first" is the original's
    "before" (x0_strata's "org locker vs asked pick")."""
    if not case:
        return {}
    asked = re.search(r"([A-Z][a-z]+)'s pick", case["readers"]["PP"]["question"])
    out = {}
    for name, ctx, bridge in (
        ("original", case["context"], case["bridge"]),
        ("changed", case["cf_context"], case["cf_bridge"]),
    ):
        sents = re.split(r"(?<=\.)\s+", ctx)
        pick = next((i for i, s in enumerate(sents) if asked and s.startswith(f"{asked.group(1)} picked")), None)
        lock = next(
            (
                i
                for i, s in enumerate(sents)
                if s.startswith("The locker of") and re.search(rf"\b{re.escape(bridge)}\b", s)
            ),
            None,
        )
        out[name] = "not found" if pick is None or lock is None else "before" if lock < pick else "after"
    return out


def whole_class(row: dict, case: dict | None, reader: str) -> str:
    """The stored class under the whole change: the main test's role (b / A / other); natural passages store the top
    word instead (switched = it is the changed answer)."""
    if "role" in row:
        return row["role"]
    rd = (case or {}).get("readers", {}).get(reader, {})
    return "b" if row["switched"] else "A" if row.get("top") == rd.get("answer") else "other"


def fact_order(case: dict | None) -> dict[str, str]:
    """Natural passages: whether the original bridge's fact sentence (and the changed bridge's) comes before or after
    the bridge's mention, as x5_natural_split.placement (the README's natural-passage split)."""
    if not case:
        return {}
    import sys

    sys.path.insert(0, str(REPO))
    from scripts import x5_natural_split as NS

    pl = NS.placement(case)
    return {"original": pl["original"], "changed": pl["new"]}


def fresh_group(case: dict | None) -> str | None:
    """45m (a case with "fresh"): locker-before / locker-after / mixed, by the score's own rule (x45m.group_of)."""
    if not case or "fresh" not in case:
        return None
    import sys

    root = str(Path(__file__).resolve().parents[3])  # the code's root (REPO is where the runs are read)
    if root not in sys.path:
        sys.path.insert(0, root)
    from scripts import x45m

    return x45m.group_of(case)


def _item(
    v, model, run, layer, scene, reader, condition, case, rows, shares, cls, status, extra=None, more=None
) -> Item:
    """more: what the card shows beside the shares (routes 45k: norms.jsonl's geometry; the sweep: its layers)."""
    tail = f"|{condition}" if condition else ""
    tail += f"|{extra['kind']}|{extra['j']}-{extra['k']}|s{extra['s']}" if extra else ""
    return {"id": f"{model}|{run.split('/')[-1]}|{scene}|{reader}{tail}", "view": v["id"], "kind": v["kind"],
            "model": model, "run": run, "layer": layer, "scene": scene, "reader": reader, "condition": condition,
            "case": case, "rows": rows, "shares": shares, "cls": cls, "status": status, "in_set": status == "in set",
            "x8": extra or {}, "more": more or {}, "group": fresh_group(case),
            "order": sentence_order(case) if v["kind"] in ("x0", "massmean", "x0_parts")
            else fact_order(case) if v["kind"] == "x5" else {}}  # fmt: skip


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
        # 45k: the atoms' geometry and jpp_other's partner (its bridge pair, to see that it shares no bridge)
        geo = {k: val for k, val in nm.items() if k.startswith("cos2_")}
        if nm.get("jpp_other_partner"):
            pc = cases.get((nm["jpp_other_partner"], cond))
            geo["jpp_other_partner"] = nm["jpp_other_partner"] + (
                f" ({pc['bridge']} → {pc['cf_bridge']})" if pc else ""
            )
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
            out.append(_item(v, model, first, layer, scene, w, cond, case, rows, sh, cls, status, more=geo))
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


# ------------------------------------------------------------------------------- parts on the main items (x0_parts)
def x0_parts_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x0_parts: X0's rows, but no cases.jsonl of its own (the prompts are the cases of the run its manifest names,
    "single" under "source_exp", as massmean's) and shares without rand_share; the view's join_runs give the arms it
    does not have (45k's control: the kmatch run's J++ at k = 100), by scene, their prompts checked per item."""
    m = read_json(f"{run}/manifest.json")
    if not m.get("single"):  # the manifest is written before the reads: none means the run is not there
        return []
    joined = tuple(r for r in v.get("join_runs", {}).get(model, []) if (REPO / r).exists())
    src = f"results/{m.get('source_exp', 'x0_necessity')}/{m['single']}"
    got = x0_items(v, model, run, in_set, cases_run=src, joined=joined)
    partners = m.get("jpp_other_partners", {})  # jpp_other's partner per scene (x0_parts.partners: no shared bridge)
    cases = {c["scene"]: c for c in read_jsonl(f"{src}/cases.jsonl") if c.get("rendering", "chat") == "chat"}
    for it in got:
        if it["scene"] in partners:
            p = partners[it["scene"]]
            pc = cases.get(p)
            it["more"] = {"jpp_other_partner": p + (f" ({pc['bridge']} → {pc['cf_bridge']})" if pc else "")}
    return got


# ------------------------------------------------------------------------------------------ the 45b layer sweep
SWEEP_KINDS = {
    "bw": "the bridge word",
    "ls": "every locker-sentence token",
    "li": "the items' tokens",
    "lv": "the values' tokens",
    "lf": "the sentence-final tokens",
}  # x45b_binding.SWEEP_ARMS, in its order
SWEEP_ROLE = {"li": "item", "lv": "value", "lf": "final"}  # x45b_binding.ROLE_ARM, by arm


def sweep_arm(arm: str) -> tuple[str, int] | None:
    """A sweep arm's (kind, layer): bw16 -> ("bw", 16); none and S -> None."""
    return (arm[:2], int(arm[2:])) if arm[:2] in SWEEP_KINDS and arm[2:].isdigit() else None


def sweep_positions(case: dict) -> dict[str, list[int]]:
    """The token positions of O each sweep kind patches (the same at every layer): bw the bridge word, ls every
    locker-sentence token (patched), li / lv / lf the item / value / final tokens (roles; absent in runs before them)."""
    out = {"bw": [case["pos"]], "ls": list(case["patched"])}
    for arm, role in SWEEP_ROLE.items():
        if role in case.get("roles", {}):
            out[arm] = list(case["roles"][role]["org"])
    return out


def sweep_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x45b_binding sweep: one item per (scene, reader) with every stored arm (none, <kind><layer>, S) as stored. Every
    case of the run is read (x45b_binding.select's items), so none is outside the set. The case's "entity" is its
    bridge (copied to "bridge" for the shared card and checks). Class: S read on S's role (b = S itself switches)."""
    if not in_set:
        return []
    m = read_json(f"{run}/manifest.json")
    got = read_jsonl(f"{run}/outcomes.jsonl")
    idx = {(r["scene"], r["reader"], r["arm"]): r for r in got}
    arms = list(dict.fromkeys(r["arm"] for r in got))  # the run's order: none, the kinds per layer, S
    cases = {c["scene"]: {**c, "bridge": c["entity"]} for c in read_jsonl(f"{run}/cases.jsonl")}
    parsed = [s for a in arms if (s := sweep_arm(a))]
    layers = sorted({la for _, la in parsed})
    kinds = [k for k in SWEEP_KINDS if k in {kd for kd, _ in parsed}]
    out = []
    for scene in sorted({k[0] for k in idx if k[2] == "none"}):
        rows = {w: {a: idx.get((scene, w, a)) for a in arms} for w in READERS}
        for w in v["filters"].get("readers", READERS):
            s = rows[w].get("S")
            out.append(_item(v, model, run, int(m["layer"]), scene, w, None, cases.get(scene), rows, {},
                             s["role"] if s else "-", "in set", more={"layers": layers, "kinds": kinds}))  # fmt: skip
    return out


LOADERS = {"x0": x0_items, "x5": x0_items, "massmean": massmean_items, "x8": x8_items, "x0_parts": x0_parts_items,
           "x45b_sweep": sweep_items}  # fmt: skip


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
    """The URL's filters beyond model: reader, condition (routes), s and kind (x8), sentence order (the main test:
    "locker first" = the original bridge's locker sentence before the asked pick, as the README's lookup claims), and
    45m's group (locker-before / locker-after / mixed, as x45m scores it)."""
    if params.get("reader") not in (None, "", "all") and it["reader"] != params["reader"]:
        return False
    if params.get("group") not in (None, "", "all") and it.get("group") != params["group"]:
        return False
    order = params.get("order")
    if (
        order not in (None, "", "all")
        and it["order"].get("original")
        != {"locker first": "before", "locker after": "after", "fact first": "before", "fact after": "after"}[order]
    ):
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
