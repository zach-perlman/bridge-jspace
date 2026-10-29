"""Automatic checks over every item of every tier-1 (and tier-2) review view (Dan 29 Oct 11:45, jobs/c3/batch53.yaml
verify_prep_1145 item 2), CPU only, read-only on results/. Results: review/verify_checks.json, summarised at the top of
docs/verify_pack.md (scripts/verify_pack_tier1.py). A failure is a finding: it is listed with its file and line, never fixed
here, and no check is changed to pass.

Per item (src/bridge_jspace/review/checks.py, over every item, not the sample):
  the edit position decodes to the bridge token in O and S (Zach: the bridge's span; 51.10: P3 = the last token)
  the answers decode to the stated answers (Zach: the answer word's first token)
  the label equals "top token == S's answer" recomputed from the stored ids (n/a where no top token is stored)
  only the scene's words differ; the probabilities agree with the label; a second run has the same prompts
Per run (here):
  gate and eligibility recomputed from competence.jsonl (the item set = the first N eligible in case order)
  duplicates: item ids, outcome rows with one key, items with identical prompts
  Z1-P: the made-up value differs from the true one; the true value is absent from the lookup's passage
  conflict test: the random part's share matches the lens part's (shares.jsonl at L)
  the headline numbers recounted from the per-item files against x0_numbers.json / figures/story/data.csv

uv run python scripts/verify_checks.py            # all tier-1 views -> review/verify_checks.json
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I
from bridge_jspace.review import recount as RC

OUT = I.REPO / "review" / "verify_checks.json"
SHARE_TOL = 0.01  # |share - rand_share|: the random part is drawn to the lens part's share
PASS, FAIL, NA = "pass", "fail", "n/a"


def rows(path: str) -> list[dict]:
    return list(I.read_jsonl(path))


def line_of(path: str, pred) -> int | None:
    """The 1-based line of the first row of a jsonl file that satisfies pred (for findings: file and line)."""
    p = I.REPO / path
    if not p.exists():
        return None
    with p.open() as f:
        for n, line in enumerate(f, 1):
            if line.strip() and pred(json.loads(line)):
                return n
    return None


def where(it: dict) -> str:
    """An item's row in its run's outcomes.jsonl (Zach's scenes are '<set>/<passage>'; his readers K / M)."""
    scene, w = it["scene"], it["reader"]
    if it["kind"] == "zach":
        st, sc = scene.split("/", 1)
        zw = {"PP": "K", "PM": "M"}[w]
        n = line_of(f"{it['run']}/outcomes.jsonl", lambda r: r["set"] == st and r["scene"] == sc and r["reader"] == zw)
    else:
        n = line_of(f"{it['run']}/outcomes.jsonl", lambda r: r.get("scene") == scene and r.get("reader") == w)
    return f"{it['run']}/outcomes.jsonl:{n}"


# ------------------------------------------------------------------------------------------- gate and eligibility
def competence(run: str, key=lambda r: r["scene"]) -> dict:
    out: dict = collections.defaultdict(dict)
    for r in rows(f"{run}/competence.jsonl"):
        if r.get("rendering", "chat") == "chat":
            out[key(r)][(r["reader"], r["variant"])] = r
    return out


def ok_scene(comp: dict, readers=I.READERS) -> bool:
    return all((x := comp.get((w, v))) and x["right"] and x["read_right"] for w in readers for v in ("org", "alt"))


def org_acc(comp: dict, keys: list, reader: str) -> float:
    got = [bool(comp[k][(reader, "org")]["read_right"]) for k in keys if (reader, "org") in comp.get(k, {})]
    return sum(got) / len(got) if got else float("nan")


def gate_x0(run: str, items: list[dict]) -> list[dict]:
    m, g = I.read_json(f"{run}/manifest.json"), I.read_json(f"{run}/gate.json").get("gate", {}).get("chat", {})
    bar, n = float(m.get("gate", 0.8)), int((m.get("n") or {}).get("items", 200))
    cases = [c["scene"] for c in rows(f"{run}/cases.jsonl") if c.get("rendering", "chat") == "chat"]
    comp = competence(run)
    acc = {w: org_acc(comp, cases, w) for w in I.READERS}
    ok = [s for s in cases if ok_scene(comp[s])]
    excl = set(m.get("excluded_scenes") or [])
    chosen = [s for s in ok if s not in excl][:n]
    got = {it["scene"] for it in items}
    out = [{"check": "gate recomputed from competence.jsonl", "status": PASS if (all(a >= bar for a in acc.values()) == bool(g.get("pass"))) else FAIL,
            "detail": f"org read accuracy {', '.join(f'{w} {a:.4f}' for w, a in acc.items())} vs bar {bar} (gate.json: "
                      f"{g.get('org_accuracy')}, pass {g.get('pass')})"},
           {"check": "eligibility and the item set recomputed", "status": PASS if (len(ok) == g.get("eligible") and set(chosen) == got) else FAIL,
            "detail": f"eligible {len(ok)} (gate.json {g.get('eligible')}); excluded {len(excl & set(ok))} dev scenes; the first {n}"
                      f" = the item set: {set(chosen) == got} ({len(got)} items; only in the recount {sorted(set(chosen) - got)[:5]},"
                      f" only in the items {sorted(got - set(chosen))[:5]})"}]  # fmt: skip
    return out


def gate_routes(run: str, items: list[dict]) -> list[dict]:
    m = I.read_json(f"{run}/manifest.json")
    gj = I.read_json(f"{run}/gate.json").get("gate", {})
    bar, n = float(m.get("gate", 0.8)), int(m.get("n_per_condition") or 300)
    comp = competence(run)
    out = []
    for cond in sorted({it["condition"] for it in items}):
        cases = [c["scene"] for c in rows(f"{run}/cases.jsonl") if c["condition"] == cond]
        acc = {w: org_acc(comp, cases, w) for w in I.READERS}
        ok = [s for s in cases if ok_scene(comp[s])]
        got = {it["scene"] for it in items if it["condition"] == cond}
        g = gj.get(cond, {})
        fixed = m.get("gate_fixed_in_advance")
        out.append({"check": f"{cond}: gate recomputed", "status": PASS if all(a >= bar for a in acc.values()) == bool(g.get("pass")) else FAIL,
                    "detail": f"org read accuracy {', '.join(f'{w} {a:.4f}' for w, a in acc.items())} vs bar {bar}"
                              + (f" (fixed in advance {fixed}: lowered after the data)" if fixed and float(fixed) != bar else "")})  # fmt: skip
        out.append({"check": f"{cond}: eligibility and the item set", "status": PASS if (len(ok) == g.get("eligible") and set(ok[:n]) == got) else FAIL,
                    "detail": f"eligible {len(ok)} (gate.json {g.get('eligible')}); the first {n} = the item set: {set(ok[:n]) == got}"})  # fmt: skip
    return out


def gate_zach(run: str, items: list[dict]) -> list[dict]:
    g = I.read_json(f"{run}/gate.json")
    key = lambda r: f"{r['set']}/{r['scene']}"  # noqa: E731
    comp = competence(run, key)
    cases = [f"{c['set']}/{c['scene']}" for c in rows(f"{run}/cases.jsonl")]
    zr = ("K", "M")
    acc = {w: org_acc(comp, cases, w) for w in zr}
    ok = [s for s in cases if ok_scene(comp[s], zr)]
    order = {f"{a}/{b}" for a, b in g.get("order", [])}
    got = {it["scene"] for it in items}
    bar = float(g.get("gate", 0.8))
    return [{"check": "gate recomputed from competence.jsonl", "status": PASS if (acc["K"] >= bar - 1e-12) == bool(g.get("pass")) else FAIL,
             "detail": f"the lookup's (K) org read accuracy {acc['K']:.4f} vs bar {bar}; recall (M) {acc['M']:.4f} (gate.json "
                       f"{g.get('org_read_accuracy')}, pass {g.get('pass')})"},
            {"check": "eligibility and the item set", "status": PASS if (len(ok) == g.get("eligible") and got == order and got <= set(ok)) else FAIL,
             "detail": f"eligible {len(ok)} (gate.json {g.get('eligible')}); items = gate.json order: {got == order}; every item "
                       f"eligible: {got <= set(ok)} ({len(got)} items; chosen {g.get('chosen')} by set / stratum, gate.json)"}]  # fmt: skip


def gate_joined(v: dict, m: str, run: str, items: list[dict]) -> list[dict]:
    """51.12 E1 and 51.10 read the X0 run's items (gate.json source): the item set is that run's (51.10: its locker-first
    items); the source run's own gate and eligibility are checked in view a."""
    g = I.read_json(f"{run}/gate.json")
    src_scenes = {it["scene"] for it in I.items("main_swap", m)}
    got = {it["scene"] for it in items}
    src = g.get("source") or I.read_json(f"{run}/plan.json").get("source")  # 53.3 stores it in plan.json
    same_src = src == I.view("main_swap")["runs"][m][0].split("/")[-1]
    if v["kind"] == "x51_answer":
        order = set(g.get("order") or [])
        ok = same_src and got == src_scenes == order
        return [{"check": "the item set is the source X0 run's", "status": PASS if ok else FAIL,
                 "detail": f"source {src} (view a's run: {same_src}); items = its {len(src_scenes)} items: {got == src_scenes}; "
                           f"= gate.json order: {got == order}"}]  # fmt: skip
    # 51.10: locker-first = both bridges' locker sentences before the asked pick (x51_jread's group), re-derived here
    first = {it["scene"] for it in I.items("main_swap", m) if it["reader"] == "PP"
             and it["order"].get("original") == "before" and it["order"].get("changed") == "before"}  # fmt: skip
    ok = same_src and got == first
    return [{"check": "the item set is the source X0 run's locker-first items", "status": PASS if ok else FAIL,
             "detail": f"source {src} (view a's run: {same_src}); {len(got)} items; locker-first re-derived from the X0 cases "
                       f"(both bridges' locker sentences before the asked pick): {len(first)}; equal: {got == first}"}]  # fmt: skip


def gate_x8(v: dict, m: str, items: list[dict]) -> list[dict]:
    routes = {it["scene"] for it in I.items("routes", m) if it["condition"] == "C2"}
    got = {it["scene"] for it in items}
    cf = v["cases_from"][m].split("/")[-1]
    same = cf == I.view("routes")["runs"][m][0].split("/")[-1]
    return [{"check": "the item set is the routes run's C2 items", "status": PASS if (same and got == routes) else FAIL,
             "detail": f"cases from {cf} (view c's run: {same}); {len(got)} scenes, routes C2 {len(routes)}; equal: {got == routes}"}]  # fmt: skip


# ------------------------------------------------------------------------------------------------------- duplicates
KEYS = {"x0": ("scene", "rendering", "layer", "reader", "dict", "k", "omp", "arm"), "routes": ("scene", "condition", "reader", "arm"),
        "x8": ("scene", "reader", "kind", "j", "k", "s"), "x51_answer": ("scene", "reader", "arm"),
        "zach": ("set", "scene", "layer", "reader", "arm"), "jread": ("scene", "reader", "pos", "layer", "arm"),
        "lastconflict": ("scene", "reader", "layer", "arm"), "identity_address": ("scene", "reader", "arm"),
        "x5": ("scene", "rendering", "layer", "reader", "dict", "k", "omp", "arm")}  # fmt: skip


def duplicates(v: dict, items: list[dict]) -> dict:
    ids = collections.Counter(it["id"] for it in items)
    out = {"item ids": sorted(k for k, c in ids.items() if c > 1)}
    for run in sorted({it["run"] for it in items}):
        keys = KEYS[v["kind"]]
        seen = collections.Counter(tuple(r.get(k) for k in keys) for r in rows(f"{run}/outcomes.jsonl"))
        out[f"{run}/outcomes.jsonl rows with one key"] = [list(k) for k, c in seen.items() if c > 1][:5]
    prompts = collections.defaultdict(list)
    for it in items:  # one pair of prompts (O and S) per condition and reader; routes' C0 / C1 / C2 share O by design
        if it["case"] is not None and not it["x8"]:
            ids = it["case"]["readers"][it["reader"]]["ids"]
            prompts[(it["condition"], it["reader"], tuple(ids["org"]), tuple(ids["alt"]))].append(it["scene"])
    out["items with identical prompts"] = [s for s in prompts.values() if len(s) > 1][:5]
    return out


# -------------------------------------------------------------------------------------- per-view content checks
def zach_facts(items: list[dict]) -> list[dict]:
    lk = [it for it in items if it["reader"] == "PP" and (it.get("more") or {}).get("facts")]
    same = [
        it["scene"]
        for it in lk
        if str(it["more"]["facts"]["made_up"]).lower() == str(it["more"]["facts"]["true"]).lower()
    ]
    there = [it["scene"] for it in lk if it["more"]["facts"]["true_in_lookup_passage"]]
    cf_there = [it["scene"] for it in lk if it["more"]["facts"]["cf_true_in_changed_lookup_passage"]]
    return [{"check": "Z1-P: the made-up value differs from the true one", "status": FAIL if same else PASS,
             "detail": f"{len(same)} of {len(lk)} passages give the made-up value = the true one" + (f": {same[:5]}" if same else "")},
            {"check": "Z1-P: the true value is absent from the lookup's passage", "status": FAIL if there else PASS,
             "detail": f"{len(there)} of {len(lk)} lookup passages (original) contain the original bridge's true value"
                       + (f": {there[:5]}" if there else "")},
            {"check": "Z1-P (beside, not Dan's check): the changed bridge's true value in the changed lookup passage", "status": "info",
             "detail": f"{len(cf_there)} of {len(lk)} (the made-up values are drawn from the relation's own answer words, so "
                       "another passage entity's made-up value can be the changed bridge's true one)"}]  # fmt: skip


def conflict_shares(v: dict, m: str, items: list[dict]) -> list[dict]:
    run = items[0]["run"]
    layer = items[0]["layer"]
    scenes = {it["scene"] for it in items}
    sh = [r for r in rows(f"{run}/shares.jsonl") if r["scene"] in scenes and r.get("rendering", "chat") == "chat"
          and r.get("layer", layer) == layer and (r["dict"], r["k"], r["omp"]) == ("jpp", 25, "signed")]  # fmt: skip
    if not sh:
        return [
            {
                "check": "the random part's share matches the lens part's",
                "status": NA,
                "detail": "no shares.jsonl rows at L",
            }
        ]
    d = [abs(r["share"] - r["rand_share"]) for r in sh]
    bad = [r["scene"] for r in sh if abs(r["share"] - r["rand_share"]) > SHARE_TOL]
    return [{"check": "the random part's share matches the lens part's", "status": FAIL if bad or len(sh) != len(scenes) else PASS,
             "detail": f"{len(sh)} scenes at L{layer} (of {len(scenes)}): max |share - rand_share| {max(d):.5f}, mean {sum(d) / len(d):.5f};"
                       f" beyond {SHARE_TOL}: {len(bad)}" + (f" {bad[:5]}" if bad else "")}]  # fmt: skip


E1_PAIRS = {"unedited": "unedited", "whole": "whole", "without J++": "arm 1: without the lens part",
            "without its random part": "arm 1's random part"}  # fmt: skip


def label_crosscheck(m: str, items: list[dict]) -> list[dict]:
    """X0 runs before batch 45 store no top token, so their labels cannot be re-derived from it. 51.12 E1 re-read the
    same items (same prompts: view b's check) under the same arms with the top token stored, and its labels are
    re-derived from that token in view b. Here: X0's stored label (role) against E1's, arm by arm. The random parts are
    redrawn in E1, so only the unedited and whole arms must agree exactly; the two removal arms are reported beside."""
    e1 = {(it["scene"], it["reader"]): it for it in I.items("answer_control", m)}
    if not e1:
        return [
            {
                "check": "labels against the 51.12 E1 rerun (top token stored)",
                "status": NA,
                "detail": "no E1 run for this model",
            }
        ]
    agree, n, diff = collections.Counter(), collections.Counter(), collections.defaultdict(list)
    for it in items:
        other = e1.get((it["scene"], it["reader"]))
        if other is None:
            continue
        for a, b in E1_PAIRS.items():
            ra, rb = it["rows"][it["reader"]].get(a), other["rows"][it["reader"]].get(b)
            if ra is None or rb is None:
                continue
            n[a] += 1
            if ra["role"] == rb["role"]:
                agree[a] += 1
            else:
                diff[a].append(
                    f"{it['scene']}|{it['reader']}: X0 {ra['role']} / E1 {rb['role']} (E1 top {C.top_text(m, rb['top'])!r})"
                )
    exact = all(agree[a] == n[a] for a in ("unedited", "whole"))
    detail = "; ".join(f"{a}: {agree[a]} of {n[a]} agree" for a in E1_PAIRS if n[a])
    ex = [d for a in ("unedited", "whole") for d in diff[a][:3]]
    return [{"check": "labels against the 51.12 E1 rerun (top token stored)", "status": PASS if exact else FAIL,
             "detail": detail + (f"; unedited / whole disagreements: {ex}" if ex else ""),
             "counts": {a: {"agree": agree[a], "n": n[a]} for a in E1_PAIRS if n[a]}}]  # fmt: skip


# ---------------------------------------------------------------------------------------------------------- runner
def check_view(v: dict) -> dict:
    out: dict = {"title": v["title"], "order": v.get("order"), "models": {}}
    for m in I.spec()["models"]:
        items = I.items(v["id"], m)
        if not items:
            nl = I.not_landed(v, m)
            if nl or m in v.get("runs", {}):
                out["models"][m] = {"n": 0, "not_landed": nl}
            continue
        per_check = collections.Counter()
        na = collections.Counter()
        fails = []
        for it in items:
            for name, (st, d) in C.run_checks(it).items():
                if st == C.FAIL:
                    per_check[name] += 1
                    if len(fails) < 20:
                        fails.append({"item": it["id"], "check": name, "detail": d, "where": where(it)})
                elif st == C.NA:
                    na[name] += 1
        run = items[0]["run"]
        if v["kind"] == "x0" and "/x0_necessity/" in run:
            runc = gate_x0(run, items) + (
                conflict_shares(v, m, items) + label_crosscheck(m, items) if v["id"] == "main_swap" else []
            )
        elif v["kind"] == "routes":
            runc = gate_routes(run, items)
        elif v["kind"] == "zach":
            runc = gate_zach(run, items) + zach_facts(items)
        elif v["kind"] in ("x51_answer", "jread", "lastconflict"):
            runc = gate_joined(v, m, run, items)
        elif v["kind"] == "x8":
            runc = gate_x8(v, m, items)
        else:  # varied scenes (a gate per cell), natural passages, 53.6: not recomputed here
            runc = [{"check": "gate and eligibility", "status": NA,
                     "detail": f"not recomputed for this kind ({v['kind']}; tier 2): the run's gate.json as stored"}]  # fmt: skip
        dup = duplicates(v, items)
        runc.append({"check": "duplicates", "status": FAIL if any(dup.values()) else PASS,
                     "detail": "; ".join(f"{k}: {x}" for k, x in dup.items() if x) or "none (item ids, outcome keys, prompts)"})  # fmt: skip
        out["models"][m] = {"n": len(items), "runs": sorted({it["run"] for it in items}), "item_fail": dict(per_check),
                            "item_na": dict(na), "item_fail_examples": fails, "run_checks": runc}  # fmt: skip
    rc = RC.recount(v["id"])
    out["recount"] = {"match": sum(r["status"] == "match" for r in rc), "mismatch": [r for r in rc if r["status"] == "mismatch"],
                      "no_source": sum(r["status"] == "no source" for r in rc), "rows": rc}  # fmt: skip
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--views", nargs="*", default=None)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()
    views = [v for v in I.spec()["views"] if v.get("tier") in (1, 2) and (not a.views or v["id"] in a.views)]
    t = time.time()
    res = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "commit": git_commit(), "views": {}}
    for v in views:
        res["views"][v["id"]] = check_view(v)
        r = res["views"][v["id"]]
        nf = sum(sum(x.get("item_fail", {}).values()) for x in r["models"].values())
        rf = sum(c["status"] == FAIL for x in r["models"].values() for c in x.get("run_checks", []))
        print(f"{v['id']}: {sum(x['n'] for x in r['models'].values())} items, item-check failures {nf}, run-check failures "
              f"{rf}, recount {r['recount']['match']} match / {len(r['recount']['mismatch'])} mismatch ({time.time() - t:.0f}s)")  # fmt: skip
    res["summary"] = summarize(res, {v["id"]: v.get("tier") for v in views})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"wrote {a.out}: {json.dumps(res['summary']['tier1'])}")


def summarize(res: dict, tiers: dict[str, int]) -> dict:
    """The citable totals (stable keys): per tier, the views, items, per-item check failures (by check), run-check
    failures (by check), the headline recount (match / mismatch); and the X0 labels against the 51.12 E1 rerun, per
    model and arm (agree of n). The README cites summary.tier1.*, and summary.e1_label_agreement."""
    out: dict = {}
    for tier in sorted(set(tiers.values())):
        vids = [vid for vid, t in tiers.items() if t == tier]
        by_item, by_run = collections.Counter(), collections.Counter()
        items = match = mismatch = 0
        for vid in vids:
            r = res["views"][vid]
            for x in r["models"].values():
                items += x.get("n", 0)
                by_item.update(x.get("item_fail", {}))
                by_run.update(c["check"] for c in x.get("run_checks", []) if c["status"] == FAIL)
            match += r["recount"]["match"]
            mismatch += len(r["recount"]["mismatch"])
        out[f"tier{tier}"] = {"views": vids, "items": items, "item_check_failures": sum(by_item.values()),
                              "item_check_failures_by_check": dict(by_item), "run_check_failures": sum(by_run.values()),
                              "run_check_failures_by_check": dict(by_run),
                              "recount": {"match": match, "mismatch": mismatch, "numbers": match + mismatch}}  # fmt: skip
    agree = {}
    for m, x in (res["views"].get("main_swap") or {}).get("models", {}).items():
        c = next((c for c in x.get("run_checks", []) if c["check"].startswith("labels against the 51.12 E1")), None)
        if c and c.get("counts"):
            agree[m] = c["counts"]
    out["e1_label_agreement"] = agree
    return out


def git_commit() -> str:
    import subprocess

    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=I.REPO, capture_output=True, text=True
    ).stdout.strip()


if __name__ == "__main__":
    main()
