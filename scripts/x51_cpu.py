"""x51_cpu (batch 51, section "2. CPU tonight" of jobs/c3/batch51.yaml; Dan 28 Oct 17:10): five descriptive analyses
of stored outcomes, no GPU, no new forward pass. Each item writes results/x51_cpu/<item>-<UTC>/: manifest.json first
(inputs' sha256, code state, this script's sha256, seeds), then the table(s) as .md and .json and a figure where one
helps. Cluster bootstrap: 10,000 resamples, seed 0, 95% percentile intervals (x0_necessity.resampled_rates: whole
clusters drawn with replacement, the same draws for every arm of a cell, so differences are paired).

  z1      Z1 table (batch 50; results/x50_zach/<run>/outcomes.jsonl): reader x arm x stratum (fact-first / fact-after),
          clusters = passages; per-relation split; the 9B's v2nb rows separate from v2. Sealed with Z1: refuses unless
          Q50.1's Dan line is committed at HEAD.
  routes  The lookup's J++ dependence split by route (results/x6_routes main runs, the 47.1 runs, the 47.8 / 49.4
          anatomy): on C2 items whose lookup takes the identity route (resp. the position route) under the whole change,
          the extra loss without J++ beyond the matched random part = share keeping that route without the random part
          minus share keeping it without J++ (X0's excess with S_whole = 1 on these items); clusters = bridge items.
  recall  The recall under the address swap (pointer swap, x8_write runs) by dose s in {1, 2, 4}: share of recalls
          that change and share naming the swapped-in slot's item (x8_write.recall_item); random vectors of the same
          norm beside (s = 1, 4); clusters = bridge items.
  concat  49.3's probes on all tokens of the locker sentence concatenated (token roles as x49_probe's keys, zero for a
          role a sentence lacks), with x49_probe.probe_view unchanged (48.3's ridge, 5 folds by the sentence's item,
          inner-CV penalty, seed 0): (i) the picker, (ii) picked by the asked person; locker-after cell and the
          locker-first control.
  fit     49.1's gain grid: logit P(switch) = a·α + b·β (+ c·αβ) per model and reader on the item-level J(α,β) rows
          (scripts/x51_fit.py), b/a, the likelihood-ratio test for c, cluster-bootstrap CIs over bridge items.

uv run python scripts/x51_cpu.py z1        # likewise routes / recall / concat / fit
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X

EXP = "x51_cpu"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch51.yaml (brief, section 2)"
N_BOOT, BOOT_SEED = X.N_BOOT, X.BOOT_SEED
EPS = 1e-9
COLORS = {"blue": "#2a78d6", "orange": "#eb6834", "gray": "#8c8b86", "aqua": "#1baf7a"}


# ---- common -------------------------------------------------------------------------------------------------------


def rel(p: Path) -> str:
    p = Path(p).resolve()
    try:
        return str(p.relative_to(pins.REPO_ROOT))
    except ValueError:
        return str(p)


def start(item: str, inputs: list[Path], extra: dict[str, Any]) -> Path:
    """The item's new folder with manifest.json, written before any computation."""
    from bridge_jspace.utils import git_state

    out = RESULTS / f"{item}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    me = Path(__file__).resolve()
    m = {"exp": EXP, "item": item, "spec": SPEC, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "code": git_state(), "switches": switches(), "script": {"path": rel(me), "sha256": hashlib.sha256(me.read_bytes()).hexdigest()},
         "inputs": {rel(p): sha256_of(p) for p in inputs}, "n_boot": N_BOOT,
         "seeds": {"bootstrap": BOOT_SEED}, **extra}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    return out


def finish(out: Path, name: str, blob: dict, lines: list[str]) -> None:
    (out / f"{name}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False, default=float) + "\n")
    (out / f"{name}.md").write_text("\n".join(lines) + "\n")
    print("wrote", out / f"{name}.md", out / f"{name}.json", flush=True)


def ci3(point: float, draws: np.ndarray) -> list[float]:
    """[point, lo, hi]; nan when the point is undefined."""
    if not np.isfinite(point):
        return [math.nan, math.nan, math.nan]
    return [float(point), *X.interval(draws)]


def fmt(v: list | None, nd: int = 2) -> str:
    if v is None or v[0] is None or not np.isfinite(v[0]):
        return "-"
    return f"{v[0]:.{nd}f} [{v[1]:.{nd}f}, {v[2]:.{nd}f}]"


def excess_numbers(sw: dict[str, list[int]], clusters: list[str], whole: str, part: str, rand: str,
                   n_boot: int = N_BOOT) -> dict[str, Any]:  # fmt: skip
    """X0's numbers for one reader on one cell: each arm's share, Jdep = 1 - S_part / S_whole, Rdep = 1 - S_rand /
    S_whole, excess = Jdep - Rdep, each [point, lo, hi] on the same cluster-bootstrap draws (seed 0)."""
    rr = X.resampled_rates(sw, clusters, n_boot, BOOT_SEED)
    pt = {a: float(np.mean(v)) for a, v in sw.items()}
    jd, rd = X.dependence(pt[whole], pt[part]), X.dependence(pt[whole], pt[rand])
    jr, rdr = X.dependence(rr[whole], rr[part]), X.dependence(rr[whole], rr[rand])
    return {"n": len(clusters), "clusters": len(set(clusters)),
            "share": {a: ci3(pt[a], rr[a]) for a in sw}, "switched_whole": int(sum(sw[whole])),
            "Jdep": ci3(float(jd), jr), "Rdep": ci3(float(rd), rdr), "excess": ci3(float(jd - rd), jr - rdr),
            "_excess_draws": jr - rdr}  # fmt: skip


def strip(d: Any) -> Any:
    """Drop the '_'-prefixed draw arrays before writing."""
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if not str(k).startswith("_")}
    if isinstance(d, list):
        return [strip(v) for v in d]
    return d


# ---- 1. Z1 table --------------------------------------------------------------------------------------------------

Z1_RUNS = {"qwen3.5-9b": "qwen35_9b_x50_z1", "qwen3.6-27b": "x50_z1_27b", "muse-glimmer-30b": "muse30_x50_z1"}
Z1_ARMS = ("none", "whole", "no_jpp", "no_jpp_rand")
Z1_READERS = {"K": "lookup", "M": "recall"}
Z1_SETS = {"jsuite_v2_test_chat": "v2", "jsuite_v2nb_test_chat": "v2nb"}
STRATA = ("fact-first", "fact-after")


def z1_cell(rows: list[dict], n_boot: int = N_BOOT) -> dict[str, Any]:
    """One Z1 cell (rows of one layer): per reader every arm's switch share and X0's extra loss, clusters = passages
    (set, scene); the gap = the recall's extra loss minus the lookup's on the same draws."""
    by = {(r["set"], r["scene"], r["reader"], r["arm"]): r for r in rows}
    keys = list(dict.fromkeys((r["set"], r["scene"]) for r in rows))
    keys = [k for k in keys if all((*k, w, a) in by for w in Z1_READERS for a in Z1_ARMS)]
    if not keys:
        return {"n": 0}
    clusters = [f"{s}|{sc}" for s, sc in keys]
    out: dict[str, Any] = {"n": len(keys)}
    for w in Z1_READERS:
        sw = {a: [int(by[(*k, w, a)]["switched"]) for k in keys] for a in Z1_ARMS}
        out[w] = excess_numbers(sw, clusters, "whole", "no_jpp", "no_jpp_rand", n_boot)
    g = out["M"]["excess"][0] - out["K"]["excess"][0]
    out["gap"] = ci3(g, out["M"]["_excess_draws"] - out["K"]["_excess_draws"])
    return out


def z1_groups(rows: list[dict]) -> dict[str, list[dict]]:
    """The set groups: all rows, then each set on its own (v2, v2nb) where the run has more than one."""
    sets = sorted({r["set"] for r in rows})
    out = {"all": rows}
    if len(sets) > 1:
        out |= {Z1_SETS.get(s, s): [r for r in rows if r["set"] == s] for s in sets}
    return out


def z1_model(run: str, n_boot: int = N_BOOT) -> dict[str, Any]:
    src = pins.RESULTS_DIR / "x50_zach" / run
    m = json.loads((src / "manifest.json").read_text())
    gate = json.loads((src / "gate.json").read_text())
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["arm"] in Z1_ARMS]
    res: dict[str, Any] = {"run": run, "target": m["model"]["target"], "gate_pass": gate.get("pass"),
                           "chosen": gate.get("chosen"), "chosen_sets": gate.get("chosen_sets"), "layers": {}}  # fmt: skip
    for la in sorted({r["layer"] for r in rows}):
        lr = [r for r in rows if r["layer"] == la]
        per: dict[str, Any] = {"strata": {}, "relations": {}}
        for g, gr in z1_groups(lr).items():
            per["strata"][g] = {s: z1_cell([r for r in gr if s == "all" or r["stratum"] == s], n_boot)
                                for s in ("all", *STRATA)}  # fmt: skip
            per["relations"][g] = {rl: z1_cell([r for r in gr if r["relation"] == rl], n_boot)
                                   for rl in sorted({r["relation"] for r in gr})}  # fmt: skip
        res["layers"][str(la)] = per
    return res


def z1_table_lines(label: str, cells: dict[str, dict]) -> list[str]:
    lines = [f"| {label} | reader | n | none | whole | no J++ | no random | extra loss (Jdep - Rdep) | gap (M - K) |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for name, c in cells.items():
        if not c.get("n"):
            lines.append(f"| {name} | - | 0 | | | | | | |")
            continue
        for w, wn in Z1_READERS.items():
            s = c[w]["share"]
            lines.append(f"| {name} | {w} ({wn}) | {c['n']} | {fmt(s['none'])} | {fmt(s['whole'])} | "
                         f"{fmt(s['no_jpp'])} | {fmt(s['no_jpp_rand'])} | {fmt(c[w]['excess'])} | "
                         f"{fmt(c['gap']) if w == 'M' else ''} |")  # fmt: skip
    return lines


def z1_figure(models: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    panels = [(mm, la) for mm in models for la in mm["layers"]]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.4 * len(panels), 3.4), sharey=True, squeeze=False)
    arms = ("whole", "no_jpp", "no_jpp_rand")
    for ax, (mm, la) in zip(axes[0], panels, strict=True):
        cells = mm["layers"][la]["strata"]["all"]
        xs = np.arange(len(STRATA) * 2)
        labels = [f"{s}\n{w}" for s in STRATA for w in Z1_READERS]
        for j, (a, col) in enumerate(zip(arms, (COLORS["blue"], COLORS["orange"], COLORS["gray"]), strict=True)):
            v = [cells[s][w]["share"][a] for s in STRATA for w in Z1_READERS]
            pt = np.array([x[0] for x in v])
            err = np.array([[x[0] - x[1], x[2] - x[0]] for x in v]).T
            ax.bar(xs + (j - 1) * 0.26, pt, 0.24, yerr=err, color=col, capsize=2, label=a, error_kw={"lw": 0.8})
        ax.set_xticks(xs, labels, fontsize=7)
        ax.set_title(f"{mm['target']} L{la}", fontsize=9)
        ax.set_ylim(0, 1)
        ax.grid(axis="y", lw=0.3, alpha=0.5)
    axes[0][0].set_ylabel("switch share (95% CI, passages)")
    axes[0][-1].legend(fontsize=7, frameon=False)
    fig.suptitle("Z1: switch by arm, stratum and reader (UNVERIFIED; sealed with Z1)", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def item_z1(n_boot: int = N_BOOT) -> Path:
    from scripts import x50_zach as Z

    answer = Z.dan_answer(Z.QUESTION["z1"])
    assert answer, "sealed: Q50.1 has no committed Dan line at HEAD"
    srcs = [pins.RESULTS_DIR / "x50_zach" / r for r in Z1_RUNS.values()]
    inputs = [s / f for s in srcs for f in ("manifest.json", "gate.json", "outcomes.jsonl")]
    out = start("z1", inputs, {"runs": Z1_RUNS, "question": "Q50.1 (Dan line committed; sealed with Z1: no number of "
                               "this table goes to Zach before the formal opening)",
                               "clusters": "passages: (set, scene)", "arms": list(Z1_ARMS)})  # fmt: skip
    models = [z1_model(r, n_boot) for r in Z1_RUNS.values()]
    lines = ["# Z1 table (batch 51, CPU item 1): reader x arm x stratum", "",
             "SEALED WITH Z1: do not share with Zach before the formal opening (Dan). Descriptive table of the stored "
             "Z1 outcomes (results/x50_zach/<run>/outcomes.jsonl), no verdict. Switch = the top token is the first "
             "token of the other entity's answer; K = the lookup, M = the recall; arms: none (O unedited), whole, "
             "no J++ (signed OMP, k = 25), no random (a random part of J++'s share). Extra loss = X0's excess, "
             "(1 - S_noJ++ / S_whole) - (1 - S_norandom / S_whole); gap = M's extra loss minus K's on the same draws. "
             f"Cluster bootstrap over passages ({n_boot:,} resamples, seed {BOOT_SEED}, 95% intervals). "
             "Strata: the bridge's fact sentence before (fact-first) or after (fact-after) the pointer sentence. "
             "Set groups: 'all' = the run of record's items; on the 9B, v2 and v2nb (the second seed) also on their "
             "own. UNVERIFIED.", ""]  # fmt: skip
    for mm in models:
        lines += [f"## {mm['target']} ({mm['run']}; gate pass {mm['gate_pass']}, {mm['chosen']} passages "
                  f"{mm['chosen_sets']})", ""]  # fmt: skip
        for la, per in mm["layers"].items():
            for g, cells in per["strata"].items():
                lines += [f"### L{la}, set {g}: by stratum", "", *z1_table_lines("stratum", cells), ""]
            for g, cells in per["relations"].items():
                lines += [f"### L{la}, set {g}: by relation (strata pooled)", "",
                          *z1_table_lines("relation", cells), ""]  # fmt: skip
    z1_figure(models, out / "z1.png")
    finish(out, "z1", {"dan_q50_1_committed": True, "models": strip(models)}, lines)
    return out


# ---- 2. route split of the lookup's J++ dependence ----------------------------------------------------------------

MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
ROUTES_MAIN = {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b",
               "muse-glimmer-30b": "muse30b_x6_routes"}  # fmt: skip
ROUTES_471 = {"qwen3.5-9b": "qwen35_9b_x6_routes_x47_1", "qwen3.6-27b": "x6_routes_x47_1_27b",
              "muse-glimmer-30b": "muse30_x6_routes_x47_1"}  # fmt: skip
ANATOMY = {"qwen3.5-9b": "qwen35_9b_x47_anatomy", "qwen3.6-27b": "x49_4_anatomy_27b",
           "muse-glimmer-30b": "muse30_x47_anatomy"}  # fmt: skip
PARTS_471 = {"J++ k = 25": ("no_jpp", "no_jpp_rand"), "J++ k = 100": ("no_jpp100", "no_jpp100_rand"),
             "atoms 26-100": ("no_jpp26_100", "no_jpp26_100_rand")}  # fmt: skip
SPLIT_ROUTES = ("identity", "position")
LOOKUP_CONDITION = "C2"
FIG_MIN_N = 10  # the by-layer figure leaves out a route's point when fewer items take it (the table keeps them)


def route_split(rows: list[dict], part: str, rand: str, n_boot: int = N_BOOT) -> dict[str, Any]:
    """The lookup's rows of one condition and layer (arms whole / part / rand): per route r in SPLIT_ROUTES, the items
    whose whole-change answer takes route r; their share keeping r without the part and without its random twin; the
    extra loss = keep(rand) - keep(part) (X0's excess with S_whole = 1 on these items); identity minus position on the
    same draws (clusters = bridge items, joint over both subsets). Also every route's share under the whole change and
    where the items' answers go without the part."""
    by = {(r["scene"], r["arm"]): r for r in rows}
    scenes = [s for s in dict.fromkeys(r["scene"] for r in rows) if all((s, a) in by for a in ("whole", part, rand))]
    ents = [by[(s, "whole")]["entity"] for s in scenes]
    if not scenes:
        return {"n": 0}
    whole = {s: by[(s, "whole")]["route"] for s in scenes}
    sw: dict[str, list[int]] = {}
    for rt in SPLIT_ROUTES:
        sw[f"{rt}|in"] = [int(whole[s] == rt) for s in scenes]
        for a in (part, rand):
            sw[f"{rt}|{a}"] = [int(whole[s] == rt and by[(s, a)]["route"] == rt) for s in scenes]
    rr = X.resampled_rates(sw, ents, n_boot, BOOT_SEED)
    out: dict[str, Any] = {"n": len(scenes), "entities": len(set(ents)),
                           "whole_routes": dict(collections.Counter(whole.values()))}  # fmt: skip
    draws = {}
    for rt in SPLIT_ROUTES:
        n_rt = sum(sw[f"{rt}|in"])
        with np.errstate(divide="ignore", invalid="ignore"):
            den = np.where(rr[f"{rt}|in"] > 0, rr[f"{rt}|in"], np.nan)
            keep_r = {a: rr[f"{rt}|{a}"] / den for a in (part, rand)}
        keep = {a: sum(sw[f"{rt}|{a}"]) / n_rt if n_rt else math.nan for a in (part, rand)}
        draws[rt] = keep_r[rand] - keep_r[part]
        out[rt] = {"n": n_rt, "entities": len({e for e, x in zip(ents, sw[f"{rt}|in"], strict=True) if x}),
                   "keep_without_part": ci3(keep[part], keep_r[part]), "keep_without_rand": ci3(keep[rand], keep_r[rand]),
                   "extra_loss": ci3(keep[rand] - keep[part], draws[rt]),
                   "without_part_goes_to": dict(collections.Counter(by[(s, part)]["route"] for s in scenes
                                                                    if whole[s] == rt))}  # fmt: skip
    a, b = SPLIT_ROUTES
    out["identity_minus_position"] = ci3(out[a]["extra_loss"][0] - out[b]["extra_loss"][0], draws[a] - draws[b])
    return out


def lookup_rows(path: Path, layer: int | None = None) -> list[dict]:
    return [r for r in X.read_jsonl(path) if r["reader"] == X.LOOKUP and r.get("condition") == LOOKUP_CONDITION
            and (layer is None or r.get("layer") == layer)]  # fmt: skip


def routes_model(target: str, n_boot: int = N_BOOT) -> dict[str, Any]:
    res: dict[str, Any] = {"target": target, "layer": X.PREDICTED[target], "sources": {}}
    main = pins.RESULTS_DIR / "x6_routes" / ROUTES_MAIN[target]
    m = json.loads((main / "manifest.json").read_text())
    assert m["layer"] == X.PREDICTED[target], (main, m["layer"])
    gate = json.loads((main / "gate.json").read_text())["gate"][LOOKUP_CONDITION]
    res["sources"]["main"] = {"run": main.name, "gate_pass": gate["pass"],
                              "J++ k = 25": route_split(lookup_rows(main / "outcomes.jsonl"), "no_jpp", "no_jpp_rand", n_boot)}  # fmt: skip
    s471 = pins.RESULTS_DIR / "x6_routes" / ROUTES_471[target]
    gate = json.loads((s471 / "gate.json").read_text())["gate"][LOOKUP_CONDITION]
    rows = lookup_rows(s471 / "outcomes.jsonl")
    res["sources"]["47.1"] = {"run": s471.name, "gate_pass": gate["pass"],
                              **{p: route_split(rows, a, b, n_boot) for p, (a, b) in PARTS_471.items()}}  # fmt: skip
    an = pins.RESULTS_DIR / "x47_anatomy" / ANATOMY[target]
    am = json.loads((an / "manifest.json").read_text())
    gate = json.loads((an / "gate.json").read_text())["gate"][LOOKUP_CONDITION]
    rows = lookup_rows(an / "outcomes.jsonl")
    res["sources"]["anatomy"] = {"run": an.name, "gate_pass": gate["pass"], "fixed_layer": am["fixed_layer"],
                                 "by_layer": {str(la): route_split([r for r in rows if r["layer"] == la], "no_J", "no_J_rand", n_boot)
                                              for la in sorted({r["layer"] for r in rows if r["layer"] is not None})}}  # fmt: skip
    return res


def routes_line(target: str, src: str, layer: Any, part: str, c: dict) -> str:
    if not c.get("n"):
        return f"| {target} | {src} | {layer} | {part} | 0 | | | | | | |"
    i, p = c["identity"], c["position"]
    return (f"| {target} | {src} | {layer} | {part} | {c['n']} | {i['n']} | {fmt(i['extra_loss'])} | {p['n']} | "
            f"{fmt(p['extra_loss'])} | {fmt(c['identity_minus_position'])} | {c['whole_routes']} |")  # fmt: skip


def routes_figure(models: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 1 + len(models), figsize=(3.6 * (1 + len(models)), 3.4), squeeze=False)
    ax = axes[0][0]
    xs = np.arange(len(models))
    for j, (rt, col) in enumerate(zip(SPLIT_ROUTES, (COLORS["blue"], COLORS["orange"]), strict=True)):
        v = [mm["sources"]["main"]["J++ k = 25"][rt]["extra_loss"] for mm in models]
        pt = np.array([x[0] for x in v])
        err = np.array([[x[0] - x[1], x[2] - x[0]] for x in v]).T
        ax.bar(xs + (j - 0.5) * 0.36, pt, 0.34, yerr=err, color=col, capsize=2, label=f"{rt}-route items",
               error_kw={"lw": 0.8})  # fmt: skip
    ax.set_xticks(xs, [f"{mm['target']}\nL{mm['layer']}" for mm in models], fontsize=7)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel("extra loss without J++ (beyond random)")
    ax.set_title("routes C2, the lookup, at L", fontsize=9)
    ax.legend(fontsize=7, frameon=False)
    for ax, mm in zip(axes[0][1:], models, strict=True):
        bl = mm["sources"]["anatomy"]["by_layer"]
        las = [int(la) for la in bl]
        for rt, col in zip(SPLIT_ROUTES, (COLORS["blue"], COLORS["orange"]), strict=True):
            v = np.array([bl[str(la)][rt]["extra_loss"] if bl[str(la)].get(rt, {}).get("n", 0) >= FIG_MIN_N
                          else [np.nan] * 3 for la in las])  # fmt: skip
            ax.plot(las, v[:, 0], "-o", color=col, ms=4, lw=1.5, label=rt)
            ax.fill_between(las, v[:, 1], v[:, 2], color=col, alpha=0.15, lw=0)
        ax.axvline(mm["sources"]["anatomy"]["fixed_layer"], color=COLORS["gray"], lw=0.8, ls=":")
        ax.axhline(0, color="k", lw=0.6)
        ax.set_xlabel("layer")
        ax.set_title(f"{mm['target']}: anatomy by layer", fontsize=8)
    fig.suptitle(f"The lookup's extra loss without J++ by route (95% CI, bridge items; by layer only routes with >= "
                 f"{FIG_MIN_N} items; UNVERIFIED)", fontsize=9)  # fmt: skip
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def item_routes(n_boot: int = N_BOOT) -> Path:
    srcs = ([pins.RESULTS_DIR / "x6_routes" / r for d in (ROUTES_MAIN, ROUTES_471) for r in d.values()]
            + [pins.RESULTS_DIR / "x47_anatomy" / r for r in ANATOMY.values()])  # fmt: skip
    inputs = [s / f for s in srcs for f in ("manifest.json", "gate.json", "outcomes.jsonl")]
    out = start("routes", inputs, {"runs": {"main": ROUTES_MAIN, "47.1": ROUTES_471, "anatomy": ANATOMY},
                                   "condition": LOOKUP_CONDITION, "reader": X.LOOKUP, "clusters": "bridge items (entity)",
                                   "parts_47_1": PARTS_471, "anatomy_part": ["no_J", "no_J_rand"]})  # fmt: skip
    models = [routes_model(t, n_boot) for t in MODELS]
    head = (
        "| model | source | layer | part | C2 items | identity-route n | identity extra loss | position-route n | "
        "position extra loss | identity - position | routes under the whole change |"
    )
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    lines = ["# Route split of the lookup's J++ dependence (batch 51, CPU item 2)", "",
             "Descriptive, after the data. Routes scenes, condition C2 (Iris picked B; B's and C's locker sentences "
             "swapped, B -> a new digit), the lookup (PP), X0's chat read. An item's route = its lookup answer under the "
             "whole change (x6_routes.classify: identity = B's new locker digit, position = C's digit at B's old slot). "
             "On the items of each route: extra loss = share still taking that route without a random part of the "
             "part's share minus share still taking it without the part (X0's excess with S_whole = 1 on these items). "
             f"Cluster bootstrap over bridge items ({n_boot:,} resamples, seed {BOOT_SEED}, 95% intervals; the two "
             "routes' subsets on the same draws, so identity - position is paired). Sources: the routes run of record "
             "(J++ k = 25 at L), the 47.1 run (C2; J++ at k = 25 and 100, atoms 26-100 with 1-25 kept), the 47.8 / 49.4 "
             "anatomy (its test half, the layer's own 25 atoms, every sampled layer). UNVERIFIED.", "",
             "## At the fixed layer", "", head, sep]  # fmt: skip
    for mm in models:
        s = mm["sources"]
        lines.append(routes_line(mm["target"], f"{s['main']['run']} (gate {s['main']['gate_pass']})", mm["layer"],
                                 "J++ k = 25", s["main"]["J++ k = 25"]))  # fmt: skip
        for p in PARTS_471:
            lines.append(routes_line(mm["target"], f"{s['47.1']['run']} (gate {s['47.1']['gate_pass']})", mm["layer"],
                                     p, s["47.1"][p]))  # fmt: skip
        fl = str(s["anatomy"]["fixed_layer"])
        if fl in s["anatomy"]["by_layer"]:
            lines.append(routes_line(mm["target"], f"{s['anatomy']['run']} (gate {s['anatomy']['gate_pass']})", fl,
                                     "J++ k = 25 (layer's own)", s["anatomy"]["by_layer"][fl]))  # fmt: skip
    lines += ["", "## The anatomy by layer (one-layer removal, the layer's own 25 atoms)", "", head, sep]
    for mm in models:
        a = mm["sources"]["anatomy"]
        for la, c in a["by_layer"].items():
            lines.append(routes_line(mm["target"], a["run"], la, "J++ k = 25", c))
    lines += ["", "Where the identity-route items' answers go without J++ (routes run of record):", ""]
    for mm in models:
        c = mm["sources"]["main"]["J++ k = 25"]
        lines.append(f"- {mm['target']}: identity items -> {c['identity']['without_part_goes_to']}; position items -> "
                     f"{c['position']['without_part_goes_to']}")  # fmt: skip
    routes_figure(models, out / "routes.png")
    finish(out, "routes", {"models": strip(models)}, lines)
    return out


# ---- 3. the recall under the address swap, by dose ----------------------------------------------------------------

X8_MAIN = {"qwen3.5-9b": "qwen35_9b_x8_write", "qwen3.6-27b": "x8_write_27b", "muse-glimmer-30b": "muse30b_x8_write"}
X8_DOSE = {"qwen3.5-9b": "qwen35_9b_x8_write12", "qwen3.6-27b": "x8_write12_27b",
           "muse-glimmer-30b": "muse30b_x8_write12"}  # fmt: skip


def recall_units(rows: list[dict], cases: dict[str, dict], legs: dict[str, int], decode) -> list[dict]:
    """Per write (scene, k, kind, s): the recall changed (top token not O's answer); the changed answer names the
    swapped-in slot's item (x8_write.recall_item == 'target'); informative = the target item's legs differ from the
    original's (else a followed pointer cannot show as a change); the lookup's class beside."""
    from scripts import x8_write as W

    look = {(r["scene"], r["k"], r["kind"], r["s"]): r["class"] for r in rows if r["reader"] == X.LOOKUP}
    out = []
    for r in rows:
        if r["reader"] != X.RECALL or r["kind"] not in ("write", "random"):
            continue
        c = cases[r["scene"]]
        slots = W.slots_of(c["context"])
        assert c["bridge"] == r["entity"], f"{r['scene']}: not the routes case's bridge"
        assert [x for x, _ in slots].index(r["entity"]) == r["j"], f"{r['scene']}: the bridge is not at slot j"
        named = bool(r["changed"]) and W.recall_item(decode(r["top"]).strip(), slots, legs, r["j"], r["k"]) == "target"
        out.append({"scene": r["scene"], "entity": r["entity"], "kind": r["kind"], "s": r["s"], "j": r["j"],
                    "k": r["k"], "changed": int(r["changed"]), "names_target": int(named),
                    "informative": int(legs[slots[r["k"]][0]] != legs[slots[r["j"]][0]]),
                    "lookup_target": int(look[(r["scene"], r["k"], r["kind"], r["s"])] == "target")})  # fmt: skip
    return out


def dose_cells(units: list[dict], n_boot: int = N_BOOT) -> list[dict]:
    """Per (kind, s): over every write and over the informative ones, the share of recalls that change and that name
    the swapped-in slot's item, the lookup's target share beside; clusters = bridge items."""
    out = []
    for kind in ("write", "random"):
        for s in sorted({u["s"] for u in units if u["kind"] == kind}):
            cell: dict[str, Any] = {"kind": kind, "s": s}
            for sub in ("all", "informative"):
                us = [u for u in units if u["kind"] == kind and u["s"] == s and (sub == "all" or u["informative"])]
                if not us:
                    cell[sub] = {"n": 0}
                    continue
                keys = ("changed", "names_target", "lookup_target")
                sw = {k: [u[k] for u in us] for k in keys}
                rr = X.resampled_rates(sw, [u["entity"] for u in us], n_boot, BOOT_SEED)
                cell[sub] = {"n": len(us), "entities": len({u["entity"] for u in us}),
                             **{k: ci3(float(np.mean(sw[k])), rr[k]) for k in keys}}  # fmt: skip
            out.append(cell)
    return out


def recall_model(target: str, n_boot: int = N_BOOT) -> dict[str, Any]:
    from bridge_jspace.review import checks as RC
    from scripts import tasks_v2 as T
    from scripts import x8_write as W

    cases = {c["scene"]: c for c in X.read_jsonl(pins.RESULTS_DIR / "x6_routes" / W.ROUTES_OF[target] / "cases.jsonl")
             if c["condition"] == "C2"}  # fmt: skip
    legs = T.DOMAINS["animals"].values
    res: dict[str, Any] = {"target": target, "cases_from": W.ROUTES_OF[target], "runs": {}}
    for fam, runs in (("pointer swap (s = multiple of mu_k - mu_j)", X8_MAIN), ("dose x s* (pairs 1-2, 2-1)", X8_DOSE)):
        src = W.RESULTS / runs[target]
        m = json.loads((src / "manifest.json").read_text())
        units = recall_units(X.read_jsonl(src / "outcomes.jsonl"), cases, legs, lambda t: RC.piece(target, t))
        res["runs"][runs[target]] = {"family": fam, "layer": m["layer"], "s_star": m.get("s_star"),
                                     "items": m.get("items"), "cells": dose_cells(units, n_boot)}  # fmt: skip
    return res


def recall_figure(models: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(models), figsize=(3.6 * len(models), 3.3), sharey=True, squeeze=False)
    for ax, mm in zip(axes[0], models, strict=True):
        cells = mm["runs"][X8_MAIN[mm["target"]]]["cells"]
        for kind, ls, mk in (("write", "-", "o"), ("random", "none", "s")):
            cs = [c for c in cells if c["kind"] == kind]
            xs = np.array([c["s"] for c in cs], dtype=float)
            for key, col, name in (("changed", COLORS["blue"], "recall changes"),
                                   ("names_target", COLORS["orange"], "names the swapped-in item")):  # fmt: skip
                v = np.array([c["all"][key] for c in cs])
                col = col if kind == "write" else COLORS["gray"]
                ax.errorbar(xs + (0.05 if key == "names_target" else 0), v[:, 0],
                            yerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], color=col, ls=ls, marker=mk, ms=5, lw=1.5,
                            capsize=2, mfc=col if key == "changed" else "white",
                            label=f"{name} ({'swap' if kind == 'write' else 'random, same norm'})")  # fmt: skip
        ax.set_xticks([1, 2, 4])
        ax.set_xlabel("dose s (x mu_k - mu_j)")
        ax.set_title(f"{mm['target']}", fontsize=9)
        ax.set_ylim(0, 1)
        ax.grid(axis="y", lw=0.3, alpha=0.5)
    axes[0][0].set_ylabel("share of writes (95% CI, bridge items)")
    axes[0][-1].legend(fontsize=6, frameon=False)
    fig.suptitle("The recall under the address swap, by dose (pointer-swap runs; UNVERIFIED)", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def recall_lines(models: list[dict]) -> list[str]:
    lines = ["| model | run | arm | s | writes | recall changes | names the swapped-in item | informative writes | "
             "changes (informative) | names it (informative) | lookup to the swapped-in slot |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mm in models:
        for run, rr in mm["runs"].items():
            for c in rr["cells"]:
                a, i = c["all"], c["informative"]
                lines.append(f"| {mm['target']} | {run} | {c['kind']} | {c['s']:g} | {a['n']} | {fmt(a['changed'])} | "
                             f"{fmt(a['names_target'])} | {i['n']} | {fmt(i.get('changed'))} | "
                             f"{fmt(i.get('names_target'))} | {fmt(a['lookup_target'])} |")  # fmt: skip
    return lines


def item_recall(n_boot: int = N_BOOT) -> Path:
    from scripts import x8_write as W

    srcs = [W.RESULTS / r for d in (X8_MAIN, X8_DOSE) for r in d.values()]
    inputs = [s / f for s in srcs for f in ("manifest.json", "outcomes.jsonl")]
    inputs += [pins.RESULTS_DIR / "x6_routes" / W.ROUTES_OF[t] / "cases.jsonl" for t in MODELS]
    out = start("recall", inputs, {"runs": {"main": X8_MAIN, "dose_x_s_star": X8_DOSE}, "clusters": "bridge items",
                                   "unit": "one write (scene, target slot k) per arm and s"})  # fmt: skip
    models = [recall_model(t, n_boot) for t in MODELS]
    lines = ["# The recall under the address swap, by dose (batch 51, CPU item 3)", "",
             "Descriptive, after the data. Pointer-swap runs (x8_write): the routes test's C2 scenes, O unedited, "
             "h + s (mu_k - mu_j) at the bridge word at L for both other slots k (two writes per scene); random = h + a "
             "random vector of the same norm (s = 1, 4). The recall changes = its top token is not O's answer; names "
             "the swapped-in item = the changed answer is the legs of the item at slot k (x8_write.recall_item, first "
             "match target / third / original). Informative writes = the slot-k item's legs differ from the original "
             "item's (elsewhere a followed pointer cannot show). The lookup's share sent to slot k beside. The main "
             "runs' s is the multiple of mu_k - mu_j (1x / 2x / 4x); the x8_write12 runs (beside) write d x s*, s* "
             "the dose at which the swap reaches the median norm of a real pointer change, on the pairs (1, 2), "
             f"(2, 1) only. Cluster bootstrap over bridge items ({n_boot:,} resamples, seed {BOOT_SEED}, 95% "
             "intervals). UNVERIFIED.", "", *recall_lines(models)]  # fmt: skip
    recall_figure(models, out / "recall.png")
    finish(out, "recall", {"models": strip(models)}, lines)
    return out


# ---- main ---------------------------------------------------------------------------------------------------------

ITEMS = {"z1": item_z1, "routes": item_routes, "recall": item_recall}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("item", choices=list(ITEMS))
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    a = ap.parse_args()
    print(ITEMS[a.item](a.n_boot))


if __name__ == "__main__":
    main()
