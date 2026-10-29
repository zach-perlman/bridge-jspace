"""Each view's item set per model, read from its runs' per-item files only, and deterministic samples of it.

An item is one (scene, reader) read under the view's arms (routes: per condition; x8: one write j -> k at dose s; 45a:
one base scene in every variant). Every item carries the rows of all readers of its scene, so a card can show both
questions; the sampled reader's rows decide its class and its checks. Items outside the claim's set (ineligible, beyond the first N, a superseded run) are
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
CODE_ROOT = REPO  # where scripts/ is imported from (REPO, where the runs are read, is moved in the tests)
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


def scripts_on_path() -> None:
    import sys

    if str(CODE_ROOT) not in sys.path:
        sys.path.insert(0, str(CODE_ROOT))


def layer_of(v: dict, model: str, run: str) -> int:
    """The view's layer: the model's fixed layer, or ("run") the run's own (x0b_generalize stores it as "predicted")."""
    if v["filters"].get("layer") == "run":
        m = read_json(f"{run}/manifest.json")
        return int(m["layer"] if "layer" in m else m["predicted"])
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


@lru_cache(maxsize=64)
def competence_by_scene(repo: str, run: str) -> dict[str, list[dict]]:
    """A run's competence.jsonl rows by scene (keyed by the repo root too: the tests move it)."""
    out = collections.defaultdict(list)
    for r in read_jsonl(f"{run}/competence.jsonl"):
        out[r["scene"]].append(r)
    return dict(out)


def competence_status(run: str, scene: str, rendering: str | None = "chat") -> str:
    """Why a generated case is outside the item set: competence failed (org or alt not said / read right by a reader),
    or eligible but beyond the first N taken."""
    rows = [r for r in competence_by_scene(str(REPO), run).get(scene, [])
            if rendering is None or r.get("rendering", rendering) == rendering]  # fmt: skip
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
    scripts_on_path()
    from scripts import x45m

    return x45m.group_of(case)


def _item(
    v, model, run, layer, scene, reader, condition, case, rows, shares, cls, status, extra=None, more=None, facet=None
) -> Item:
    """more: what the card shows beside the shares (routes 45k: norms.jsonl's geometry; the sweep: its layers); facet:
    the item's value of each of the view's facets (filters.facets, a select on the page: 45a's move, 45d's format)."""
    tail = f"|{condition}" if condition else ""
    tail += f"|{extra['kind']}|{extra['j']}-{extra['k']}|s{extra['s']}" if extra else ""
    return {"id": f"{model}|{run.split('/')[-1]}|{scene}|{reader}{tail}", "view": v["id"], "kind": v["kind"],
            "model": model, "run": run, "layer": layer, "scene": scene, "reader": reader, "condition": condition,
            "case": case, "rows": rows, "shares": shares, "cls": cls, "status": status, "in_set": status == "in set",
            "x8": extra or {}, "more": more or {}, "group": fresh_group(case), "facet": facet or {},
            "order": sentence_order(case) if v["kind"] in ("x0", "massmean", "x0_parts", "x45g")
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
    manifest = read_json(f"{first}/manifest.json")
    bothoff = manifest.get("bothoff", True)
    done = sorted({(k[0], k[1]) for k in by_run[first] if k[3] == "whole" and k[1] in conds})
    taken = routes_taken(first, cases, manifest.get("n_per_condition")) if not in_set else set()
    gate = read_json(f"{first}/gate.json").get("gate", {})
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
        if not bothoff:  # x6_routes stores share_both = 0 when the union was not computed
            sh.pop("both", None)
        if "norm" in nm:
            sh["norm"] = nm["norm"]
        # 45k: the atoms' geometry and jpp_other's partner (its bridge pair, to see that it shares no bridge)
        geo = {k: val for k, val in nm.items() if k.startswith("cos2_")}
        if nm.get("jpp_other_partner"):
            pc = cases.get((nm["jpp_other_partner"], cond))
            geo["jpp_other_partner"] = nm["jpp_other_partner"] + (
                f" ({pc['bridge']} → {pc['cf_bridge']})" if pc else ""
            )
        # 45e: the controls' directions (k_wrong, k_pca) and the same-domain pairs the wrong-pair control drew from
        ctl = {k: nm[k] for k in ("k_wrong", "k_pca", "n_wrong_pool") if k in nm}
        if ctl:
            geo["controls"] = ctl
        facet = {"control": wrong_reached(sh, ctl.get("k_wrong"))} if "wrong" in sh and "idout" in sh else None
        case = cases.get(key)
        if case is not None:
            case = {**case, "_joined": {run.split("/")[-1]: joined_cases[run].get(key) for run in runs[1:]}}
        if in_set:
            status = "in set"
        elif gate.get(cond, {}).get("pass") is False:
            status = f"{cond}'s read gate failed"
        elif key in taken:  # among the first N eligible, but no reads: --identity drops entities without a class mean
            status = ("eligible and taken, dropped before the reads (an entity without a class mean: identity arms)"
                      if manifest.get("identity_dropped") else "eligible and taken, not read")  # fmt: skip
        else:
            status = competence_status(first, scene, None)
        for w in f.get("readers", READERS):
            whole = rows[w].get("whole")
            cls = (
                (route_class(whole, cond) if w == "PP" else ("follows S" if whole["switched"] else "stays"))
                if whole
                else status
            )
            out.append(
                _item(v, model, first, layer, scene, w, cond, case, rows, sh, cls, status, more=geo, facet=facet)
            )
    return out


def routes_taken(run: str, cases: dict, n: int | None) -> set[tuple[str, str]]:
    """The (scene, condition) keys x6_routes took: per condition the first n in case order whose readers said and read
    O's and S's answers right (competence.jsonl)."""
    if not n:
        return set()
    ok: dict[str, list] = collections.defaultdict(list)
    for r in read_jsonl(f"{run}/competence.jsonl"):
        ok[r["scene"]].append(bool(r["right"] and r["read_right"]))
    per: dict[str, list] = collections.defaultdict(list)
    for key in cases:  # cases.jsonl's order
        if ok.get(key[0]) and all(ok[key[0]]):
            per[key[1]].append(key)
    return {k for keys in per.values() for k in keys[:n]}


WRONG_SHORT = 0.9  # x6_routes.wrong_share_report: a control below 0.9 of identity outside J++'s share is "short"


def wrong_reached(shares: dict, k_wrong: int | None = None) -> str:
    """45e: whether the wrong-pair control reached identity outside J++'s share in this scene: "empty" (it took no
    direction, so its arm removes nothing), "short" (below WRONG_SHORT of the target: a same-domain pool too small to
    reach it), else "reached"."""
    t = shares["idout"]
    if k_wrong == 0:
        return "empty"
    return "short" if t > 0 and shares["wrong"] < WRONG_SHORT * t else "reached"


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


# ------------------------------------------------------------------------- 45a: a sentence before the scene (x6_routes)
PREPEND_WHAT = {
    "V0": "nothing (the control: the routes scene, rerun)",
    "V1": "a new person's pick of the item whose locker is first in O",
    "V2": "the same new person's pick of another locker item",
    "V3": "the same new person's pick of an item with no locker in the scene",
    "V4": "a neutral filler sentence",
}  # x6_routes.prepend_sentences
SEP = " · "  # a 45a row's label: "<variant> · <arm label>"


def first_locker(move: list[int]) -> bool:
    """45a's rule reads the moves to or from the first locker (x6_routes.first_locker_rule: slot 0 in the move)."""
    return 0 in move


def prepend_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x6_routes --prepend: one item per (base scene, reader) holding every variant (V0 none, V1-V3 a new person's pick,
    V4 a filler; manifest "prepend"), so a card shows one base scene in all of them. case: the first variant's (V0);
    more["variants"]: each variant's case (prompts, pos, the prepended sentence); rows keyed "<variant> · <arm label>";
    more["norms"] / more["beta"]: each variant's shares and the code's shift vs V0 (beta.jsonl). Class: the stored
    route (lookup) or follows S / stays (recall) under the view's class_arm in the first variant. Outside the set: the
    base scenes not read, with each variant's competence."""
    f = v["filters"]
    m = read_json(f"{run}/manifest.json")
    variants = list(m.get("prepend") or [])
    if not variants:  # the manifest is written before the reads: none means the run is not there
        return []
    cases: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for c in read_jsonl(f"{run}/cases.jsonl"):
        cases[c["base_scene"]][c["variant"]] = c
    got = {(r["base_scene"], r["variant"], r["reader"], r["arm"]): r for r in read_jsonl(f"{run}/outcomes.jsonl")}
    norms = {(r["base_scene"], r["variant"]): r for r in read_jsonl(f"{run}/norms.jsonl")}
    beta = {(r["base_scene"], r["variant"]): r for r in read_jsonl(f"{run}/beta.jsonl")}
    layer = layer_of(v, model, run)
    class_label = f.get("class_arm", "whole")
    done = sorted({k[0] for k in got if k[3] == "whole"})
    out = []
    for base in done if in_set else sorted(set(cases) - set(done)):
        per = {x: cases[base][x] for x in variants if x in cases[base]}
        case = next(iter(per.values()), None)
        rows = {w: {f"{x}{SEP}{label}": got.get((base, x, w, arm)) for x in per for label, arm in f["arms"].items()}
                for w in READERS}  # fmt: skip
        move = list(case["move"]) if case else []
        more = {"variants": per, "norms": {x: norms.get((base, x)) for x in per},
                "beta": {x: beta.get((base, x)) for x in per}, "move": move, "class_arm": class_label}  # fmt: skip
        facet = {"move": "to or from the first locker" if first_locker(move) else "other moves"}
        for w in f.get("readers", READERS):
            first = rows[w].get(f"{variants[0]}{SEP}{class_label}")
            if in_set:
                status = "in set"
                cls = (
                    (route_class(first, "C2") if w == "PP" else "follows S" if first["switched"] else "stays")
                    if first
                    else "-"
                )
            else:
                status = prepend_status(run, per)
                cls = status
            out.append(_item(v, model, run, layer, base, w, "C2", case, rows, {}, cls, status, more=more, facet=facet))
    return out


def prepend_status(run: str, per: dict[str, dict]) -> str:
    """Why a base scene is outside 45a's paired set: a variant in which it is ineligible (or not read), else eligible
    in every variant but beyond the first N."""
    bad = [
        f"{x}: {s}"
        for x, c in per.items()
        if not (s := competence_status(run, c["scene"], None)).startswith("eligible")
    ]
    return "; ".join(bad) if bad else "eligible in every variant, beyond the first N taken"


def variant_item(it: Item, x: str) -> Item:
    """45a: one variant of an item as a routes item (that variant's case and rows), for the checks and the card."""
    rows = {w: {label.split(SEP, 1)[1]: r for label, r in got.items() if label.split(SEP, 1)[0] == x}
            for w, got in it["rows"].items()}  # fmt: skip
    return {**it, "kind": "routes", "condition": "C2", "case": it["more"]["variants"][x], "rows": rows}


# ------------------------------------------------------------- 45d: varied formats, the refit basis (x0b_generalize)
CELL = ("domain", "format", "level")  # x0b_generalize.CELL: the gate's cell


def x45d_order(case: dict | None) -> dict[str, str]:
    """45d: whether the bridge's locker statement comes before the asked pick (the case's "order", as
    x0b_generalize.order_of; sentence_order reads prose only), and the changed bridge's in the changed prompt, from the
    format's own statements (prose sentence, JSON object, table row)."""
    if not case:
        return {}
    scripts_on_path()
    from scripts import x0b_generalize as XB

    out = {"original": case.get("order", "not found")}
    try:
        pick, lock = XB.statements(case, case["facts"]["person"], case["cf_bridge"])
        ctx = case["cf_context"]
        out["changed"] = "before" if ctx.index(lock) < ctx.index(pick) else "after"
    except (KeyError, ValueError):
        out["changed"] = "not found"
    return out


def split_half(halves: dict, entity: str | None) -> str:
    """Which half of a format's split.json an entity is in: test (held out), fit, or neither."""
    return "test" if entity in halves.get("test", ()) else "fit" if entity in halves.get("fit", ()) else "neither"


def x45d_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x0b_generalize --pcf-from (45d): X0's rows (top token stored) on the held-out half of the varied scenes, read by
    x0's loader at the run's layer. On top: the format as a facet; the bridge's and the changed bridge's half of the fit
    run's split.json (the manifest's pcf_from); the sentence order from the case; each part's share and its random
    part's from shares.jsonl (dict, k, omp of the view's arms); outside the set, a cell (domain / format / level) whose
    read gate failed before competence."""
    m = read_json(f"{run}/manifest.json")
    if not m.get("pcf_from"):  # not a 45d run, or the manifest of a run not there
        return []
    split = read_json(f"results/{m['pcf_from']}/split.json").get("formats", {})
    gate = read_json(f"{run}/gate.json").get("gate", {})
    layer = layer_of(v, model, run)
    parts = [(d, k, omp) for arm, d, k, omp in v["filters"]["arms"].values() if arm == "no_part"]  # the view's order
    shares = {(r["scene"], r["dict"]): r for r in read_jsonl(f"{run}/shares.jsonl")
              if r.get("layer", layer) == layer and (r["dict"], r["k"], r["omp"]) in parts}  # fmt: skip
    got = x0_items(v, model, run, in_set)
    for it in got:
        c = it["case"] or {}
        fmt = c.get("format")
        halves = split.get(fmt, {})
        it["facet"] = {"format": fmt}
        it["order"] = x45d_order(it["case"])
        it["shares"] = {}
        for d, _, _ in parts:
            s = shares.get((it["scene"], d))
            if s:
                it["shares"][d] = s["share"]
                it["shares"][f"{d}_rand"] = s["rand_share"]
        it["more"] = {"split": {"fit_run": f"results/{m['pcf_from']}", "format": fmt, "n_fit": len(halves.get("fit", ())),
                                "bridge": split_half(halves, c.get("bridge")), "cf_bridge": split_half(halves, c.get("cf_bridge"))}}  # fmt: skip
        if not in_set and c:
            cell = "/".join(str(c[k]) for k in CELL)
            if gate.get(cell, {}).get("pass") is False:
                it["status"] = it["cls"] = f"the cell's read gate failed ({cell})"
    return got


# --------------------------------------------------------------- 45g: two routes for the recall (x0_massmean)
SCENE_SET = {"cf": "two people swap", "single": "only the asked pick"}  # x0_massmean.stage_score45g's names


def x45g_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x0_massmean --mode two_routes (45g): massmean's rows (no top token, no cases of their own) on every item of the
    run the manifest names ("single": the main test, two people swap, or the one-pick set, by its "alt"); the prompts
    are that run's cases.jsonl, the cases x0_massmean.examples_blob rebuilds (X.build_cases on the manifest's set with
    its alt). Each item keeps the stored sentence order (org_order / alt_order: the 45g rule's groups), the stored
    entity (checked against the case) and its scene set (a facet)."""
    m = read_json(f"{run}/manifest.json")
    if not m.get("single"):
        return []
    got = massmean_items(v, model, run, in_set)
    first = {}
    for r in read_jsonl(f"{run}/outcomes.jsonl"):
        first.setdefault(r["scene"], r)
    scene_set = SCENE_SET.get(m.get("alt", "single"), str(m.get("alt")))
    for it in got:
        r = first[it["scene"]]
        it["more"] = {"stored_order": {"org_order": r.get("org_order"), "alt_order": r.get("alt_order")},
                      "entity": r.get("entity"), "scene_set": scene_set,
                      "cases_from": f"results/x0_necessity/{m['single']}/cases.jsonl"}  # fmt: skip
        it["facet"] = {"scenes": scene_set}
    return got


# ------------------------------------------------------------- 51.12 E1: the answer control on the main test (x51_answer)
def x51_answer_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x51_answer, set e1 (Dan 28 Oct ~20:20): the main test's items (its gate.json "source", an x0_necessity run),
    each read under three arms and their random parts: without the lens part (arm 1), without it but keeping its answer
    directions (arm 2), without the answer directions only (arm 3). The prompts are the source run's cases.jsonl, joined
    by scene (this run's own reader ids kept in "_joined" for the check); more: the answer word's lens rank at the bridge
    word (readout.jsonl, O and S), the parts' shares (norms.jsonl)."""
    if not in_set:  # its items are the source run's first 200 eligible; the source's own view lists the rest
        return []
    gate = read_json(f"{run}/gate.json")
    src = f"results/x0_necessity/{gate.get('source', '')}"
    m = read_json(f"{run}/manifest.json")
    layer = int(m.get("layer") or spec()["models"][model]["layer"])
    cases = {c["scene"]: c for c in read_jsonl(f"{src}/cases.jsonl") if c.get("rendering", "chat") == "chat"}
    own = {c["scene"]: c for c in read_jsonl(f"{run}/cases.jsonl")}
    idx = {(r["scene"], r["reader"], r["arm"]): r for r in read_jsonl(f"{run}/outcomes.jsonl")}
    norms = {r["key"]: r for r in read_jsonl(f"{run}/norms.jsonl")}
    readout = {(r["key"], r["variant"]): r for r in read_jsonl(f"{run}/readout.jsonl")}
    out = []
    for scene in sorted({k[0] for k in idx if k[2] == "whole"}):
        case = cases.get(scene)
        if case is not None:
            case = {**case, "_joined": {run.split("/")[-1]: own.get(scene)}}
        rows = {w: {label: ({**r, "_run": run.split("/")[-1]} if (r := idx.get((scene, w, arm))) else None)
                    for label, arm in v["filters"]["arms"].items()} for w in READERS}  # fmt: skip
        nm = norms.get(scene, {})
        sh = {k.removeprefix("share_"): nm[k] for k in ("share_jpp", "share_jpp_A", "share_A") if k in nm}
        ranks = {var: (readout.get((scene, var)) or {}).get("answer_word_rank") for var in ("org", "alt")}
        more = {"answer_rank": ranks, "answer_words": (own.get(scene) or {}).get("tokens", {}).get("A_words")}
        for w in v["filters"].get("readers", READERS):
            whole = rows[w].get("whole")
            out.append(_item(v, model, run, layer, scene, w, None, case, rows, sh,
                             whole["role"] if whole else "-", "in set", more=more))  # fmt: skip
    return out


# --------------------------------------------------------------- Z1-P: Zach's made-up-fact passages (x50_zach, z1p)
ZACH_READER = {"K": "PP", "M": "PM"}  # x50_zach: K = the lookup (the fact stated in its passage), M = the recall


def word_in(word: str, text: str) -> bool:
    return bool(re.search(rf"\b{re.escape(str(word))}\b", text, flags=re.IGNORECASE))


def zach_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x50_zach part z1p: Zach's passages with a made-up final fact (Z1's rule, Dan 29 Oct morning). Readers K (the
    lookup: the made-up fact is stated in its passage) and M (the recall: its passage leaves the fact out, the true
    value comes from memory) are shown as PP / PM. The two readers read different passages, so each item's case carries
    its own reader's passage and bridge token; more["facts"]: the made-up value (K's answer) beside the true one (M's
    answer), and whether the true value appears in the lookup's passage."""
    if not in_set:
        return []
    # one passage id can be in both of Zach's sets (jsuite_v2 and jsuite_v2nb): an item's scene is "<set>/<passage>"
    raw = {f"{c['set']}/{c['scene']}": c for c in read_jsonl(f"{run}/cases.jsonl")}
    got = read_jsonl(f"{run}/outcomes.jsonl")
    idx = {(f"{r['set']}/{r['scene']}", ZACH_READER[r["reader"]], r["arm"]): r for r in got}
    norms = {(f"{r['set']}/{r['scene']}", ZACH_READER[r["reader"]]): r for r in read_jsonl(f"{run}/norms.jsonl")}
    layer = int(next((r["layer"] for r in got), spec()["models"][model]["layer"]))
    out = []
    for scene in sorted({k[0] for k in idx if k[2] == "whole"}):
        c = raw.get(scene)
        rows = {w: {label: idx.get((scene, w, arm)) for label, arm in v["filters"]["arms"].items()} for w in READERS}
        if c is None:
            case = None
        else:
            rd = {ZACH_READER[k]: x for k, x in c["readers"].items()}
            k_ctx, k_cf = rd["PP"]["context"], rd["PP"]["cf_context"]
            facts = {"made_up": rd["PP"]["answer"], "true": rd["PM"]["answer"], "cf_made_up": rd["PP"]["cf_answer"],
                     "cf_true": rd["PM"]["cf_answer"], "relation": c.get("relation"), "stratum": c.get("stratum"),
                     "true_in_lookup_passage": word_in(rd["PM"]["answer"], k_ctx),
                     "cf_true_in_changed_lookup_passage": word_in(rd["PM"]["cf_answer"], k_cf)}  # fmt: skip
        for w in v["filters"].get("readers", READERS):
            if c is not None:
                case = {"scene": scene, "bridge": c["bridge"], "cf_bridge": c["cf_bridge"], "context": rd[w]["context"],
                        "cf_context": rd[w]["cf_context"], "pos": rd[w]["pos"], "span": rd[w].get("span"), "readers": rd,
                        "relation": c.get("relation"), "order": c.get("order"), "set": c.get("set")}  # fmt: skip
            whole = rows[w].get("whole")
            sh = {"jpp": norms[(scene, w)]["share_jpp"]} if (scene, w) in norms else {}
            out.append(_item(v, model, run, layer, scene, w, None, case, rows, sh, whole["role"] if whole else "-",
                             "in set", more={"facts": facts} if c is not None else {}))  # fmt: skip
    return out


# ------------------------------------------------------------------- 51.10: the bridge entity at the last token (x51_jread)
def jread_items(v: dict, model: str, run: str, in_set: bool = True) -> list[Item]:
    """x51_jread (51.10): the write arms at the last token (P3) at each reader's read peak (peak.json), on the
    locker-first items the swap grid reads: no change, the whole-state patch, the lens swap, its random and rotated
    controls, the J++ part at gain 1 / 2 and a random part of its size. The case is the run's own (the bridge word is
    "pos"; the edit is at the last token, jpos P3); more: the read peak layer, the edit position, and the plain logit
    lens's top token at the last token at that layer (logit_lens.jsonl: O and S). The J++ lens readout per item is not
    stored by the run (read.json holds its rates)."""
    if not in_set:
        return []
    peaks = read_json(f"{run}/peak.json").get("peaks", {})
    peak = {"PP": peaks.get("lookup"), "PM": peaks.get("recall")}
    cases = {c["scene"]: {**c, "bridge": c["entity"]} for c in read_jsonl(f"{run}/cases.jsonl")}
    got = read_jsonl(f"{run}/outcomes.jsonl")
    idx = {(r["scene"], r["reader"], r["arm"]): r for r in got
           if r["arm"] == "none" or (r["pos"] == "P3" and r["layer"] == peak.get(r["reader"]))}  # fmt: skip
    ll = {(r["scene"], r["reader"], r["variant"]): r for r in read_jsonl(f"{run}/logit_lens.jsonl")}
    whole_label = next(label for label, arm in v["filters"]["arms"].items() if arm == "whole")
    out = []
    for scene in sorted({k[0] for k in idx if k[2] == "swap"}):
        case = cases.get(scene)
        rows = {w: {label: idx.get((scene, w, arm)) for label, arm in v["filters"]["arms"].items()} for w in READERS}
        for w in v["filters"].get("readers", READERS):
            whole = rows[w].get(whole_label)
            if whole is None:
                continue
            la = peak[w]
            lens = {var: (r["top"][la] if (r := ll.get((scene, w, var))) and la < len(r["top"]) else None)
                    for var in ("org", "alt")}  # fmt: skip
            more = {"peak": la, "edit_at": (case or {}).get("jpos", {}).get(w, {}).get("P3"), "logit_lens_top": lens}
            out.append(_item(v, model, run, la, scene, w, None, case, rows, {}, whole["role"], "in set", more=more))
    return out


LOADERS = {"x0": x0_items, "x5": x0_items, "massmean": massmean_items, "x8": x8_items, "x0_parts": x0_parts_items,
           "x45b_sweep": sweep_items, "x45a_prepend": prepend_items, "x45d": x45d_items, "x45g": x45g_items,
           "x51_answer": x51_answer_items, "zach": zach_items, "jread": jread_items}  # fmt: skip


@lru_cache(maxsize=256)
def _items(view_id: str, model: str, which: str) -> tuple[Item, ...]:
    """which: "set" (the claim's items), "out" (outside it: ineligible / beyond N), "superseded". join: false -> every
    run its own item set (routes: its own chain; other kinds: every run of the model, e.g. 45g's two scene sets)."""
    v = view(view_id)
    runs = v.get("superseded", {}).get(model, []) if which == "superseded" else v.get("runs", {}).get(model, [])
    runs = [r for r in runs if (REPO / r).exists()]
    if not runs:
        return ()
    in_set = which == "set"
    joined = which != "superseded" and v.get("join", True)
    if v["kind"] == "routes":
        got = []
        for chain in [runs] if joined else [[r] for r in runs]:
            got += routes_items(v, model, chain, in_set or which == "superseded")
    else:
        got = [it for run in (runs[:1] if joined else runs)
               for it in LOADERS[v["kind"]](v, model, run, in_set or which == "superseded")]  # fmt: skip
    if which == "superseded":
        for it in got:
            it["status"], it["in_set"] = f"superseded run (by {v['runs'][model][0].split('/')[-1]})", False
    return tuple(got)


def items(view_id: str, model: str, which: str = "set") -> list[Item]:
    return list(_items(view_id, model, which))


def facets(it: Item, params: dict) -> bool:
    """The URL's filters beyond model: reader, condition (routes), s and kind (x8), sentence order (the main test:
    "locker first" = the original bridge's locker sentence before the asked pick, as the README's lookup claims), 45m's
    group (locker-before / locker-after / mixed, as x45m scores it), and the item's own facets (the view's
    filters.facets: 45a's move, 45d's format, 45e's control, 45g's scene set)."""
    if params.get("reader") not in (None, "", "all") and it["reader"] != params["reader"]:
        return False
    if params.get("group") not in (None, "", "all") and it.get("group") != params["group"]:
        return False
    for name, val in it.get("facet", {}).items():
        if params.get(name) not in (None, "", "all") and val != params[name]:
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
