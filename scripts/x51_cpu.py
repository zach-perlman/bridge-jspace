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


# ---- main ---------------------------------------------------------------------------------------------------------

ITEMS = {"z1": item_z1}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("item", choices=list(ITEMS))
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    a = ap.parse_args()
    print(ITEMS[a.item](a.n_boot))


if __name__ == "__main__":
    main()
