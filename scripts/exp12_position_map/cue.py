"""exp12 add-on: is the bridge, or already the answer, readable on the cue phrase, where swapping the bridge acts?

Reads a finished exp12 run's grids (no model). The cue phrase's positions are part B's `cue` regime (exp02): the
tokens of the phrase in data/cue_spans.json ("Amazon River ends"), without the prompt's last two positions (-1 and 0,
part A's read sites). Per question and reader, for each layer band, the share of band layers with the word ranked
first among its candidates at:
  cue_mean     an average cue token (the mean over the cue tokens): one position, comparable with -1 and 0
  cue_best     the best cue token: a search over ~5 tokens, so the same search for the same-category control
               (distractor / swap answer) gives its noise ceiling
  noncue_mean  an average other earlier token (part B's `earlier_noncue` positions)
  -1, 0        one word before the end and the last word (exp12's read sites)
and per layer, the share of questions with the word first at an average cue token, at -1 and at 0. 95% bootstrap CI
over questions. Layers 0-4 are the lexical baseline: a cue word's own associations ("Munich" -> Germany, "Romeo" ->
Shakespeare) already rank the bridge first there.
    uv run python -m scripts.exp12_position_map.cue <exp12 run dir>   # -> <run>/analysis-<timestamp>-cue-phrase/
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from bridge_jspace.pins import DATA_DIR
from bridge_jspace.stats import bootstrap_mean

ROLES = (("bridge", "distractor"), ("answer", "swap_answer"))
BANDS = {"32-48": (32, 48), "24-40": (24, 40), "0-4": (0, 4)}  # 0-4: lexical baseline, before much is computed
N_BOOT, SEED = 10000, 0


def cue_positions(tokens: list[str], cue: str) -> list[int]:
    """Token indices of `cue` inside the prompt the tokens spell, without position 0 and the last two positions
    (part B's `cue` regime: the cue phrase among the earlier words)."""
    text = "".join(tokens)
    start = text.index(cue)
    end, pos, out = start + len(cue), 0, []
    for i, t in enumerate(tokens):
        if pos < end and pos + len(t) > start:
            out.append(i)
        pos += len(t)
    last = len(tokens) - 1
    return [i for i in out if 1 <= i <= last - 2]


def band_share(grid: np.ndarray, rows: list[int], col: int) -> float:
    """Share of the band's layer rows with rank 1 at one position (grid: [layers, positions] pool ranks)."""
    return float(np.mean(grid[rows, col] == 1))


def analyze_cue(grids: dict, meta: list[dict], layers: list[int], cues: dict[str, str]) -> dict[str, Any]:
    eligible = [m for m in meta if m["status"] == "eligible" and m["name"] in cues and m["name"] in grids]
    out: dict[str, Any] = {"n": len(eligible), "layers": list(layers), "bands": {}, "by_layer": {}}
    sites: dict[str, dict[str, list[int]]] = {}
    for m in eligible:
        last = len(m["tokens"]) - 1
        cue = cue_positions(m["tokens"], cues[m["name"]])
        sites[m["name"]] = {
            "cue": cue,
            "noncue": [i for i in range(1, last - 1) if i not in cue],
            "-1": [last - 1],
            "0": [last],
        }
    for band, (lo, hi) in BANDS.items():
        rows = [i for i, layer in enumerate(layers) if lo <= layer <= hi]
        res: dict[str, Any] = {}
        for role, control in ROLES:
            for word in (role, control):
                vals: dict[str, list[float]] = {k: [] for k in ("cue_mean", "cue_best", "noncue_mean", "-1", "0")}
                for m in eligible:
                    g, at = grids[m["name"]].get(f"{word}_pool"), sites[m["name"]]
                    if g is None or not at["cue"]:
                        continue
                    cue_shares = [band_share(g, rows, c) for c in at["cue"]]
                    vals["cue_mean"].append(float(np.mean(cue_shares)))
                    vals["cue_best"].append(max(cue_shares))
                    if at["noncue"]:
                        vals["noncue_mean"].append(float(np.mean([band_share(g, rows, c) for c in at["noncue"]])))
                    vals["-1"].append(band_share(g, rows, at["-1"][0]))
                    vals["0"].append(band_share(g, rows, at["0"][0]))
                res[word] = {k: _ci(bootstrap_mean(v, N_BOOT, SEED)) | {"n": len(v)} for k, v in vals.items() if v}
        out["bands"][band] = res
    for role, control in ROLES:
        for word in (role, control):
            out["by_layer"][word] = {}
            for site in ("cue", "-1", "0"):
                per_q = [
                    (g[:, sites[m["name"]][site]] == 1).mean(axis=1)  # [layers]: an average token of the site
                    for m in eligible
                    if (g := grids[m["name"]].get(f"{word}_pool")) is not None and sites[m["name"]]["cue"]
                ]
                share = np.mean(per_q, axis=0)
                reached = np.flatnonzero(share >= 0.5)
                out["by_layer"][word][site] = {
                    "share": [round(float(x), 4) for x in share],
                    "max": round(float(share.max()), 4),
                    "first_layer_half": int(layers[reached[0]]) if reached.size else None,
                }
    n_cue = [len(at["cue"]) for at in sites.values()]
    out["cue_tokens_per_question"] = {"median": float(np.median(n_cue)), "min": min(n_cue), "max": max(n_cue)}
    return out


def analyze(run_dir: str | Path) -> Path:
    from .experiment import load_grids

    run_dir = Path(run_dir)
    meta = [json.loads(x) for x in (run_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    layers = json.loads((run_dir / "layers.json").read_text())
    cues = json.loads((DATA_DIR / "cue_spans.json").read_text())["cues"]
    summary = {
        "source_run": str(run_dir),
        "cue_spans": "data/cue_spans.json",
        "readers": {r: analyze_cue(load_grids(run_dir / f"grids_{r}.npz"), meta, layers[r], cues) for r in layers},
        "ci": f"95% percentile bootstrap over questions, n_boot={N_BOOT}, seed={SEED}",
    }
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-cue-phrase"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    manifest = json.loads((run_dir / "manifest.json").read_text())
    plot_cue(out / "cue_phrase.png", summary["readers"]["jlens"], manifest)
    per_q = {r: bridge_on_cue(load_grids(run_dir / f"grids_{r}.npz"), meta, layers[r], cues) for r in ("jlens", "jpp")}
    flips = {lens: swap_flips(run) for lens, run in SWAP_RUNS.items()}
    summary["lens_comparison"] = lens_comparison(per_q, flips)
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    plot_lenses(out / "cue_phrase_lenses.png", per_q, flips, summary["lens_comparison"], manifest)
    return out


# Part B's swap of the bridge's J-space part on the cue phrase (layers 24-40), each lens's own decomposition.
SWAP_RUNS = {"jlens": "main_v4_jlens_pos-cue", "jpp": "main_v4_jpp_pos-cue"}
GROUPS = (("both", "flips with both lenses"), ("jpp_only", "flips with J++ only"), ("neither", "flips with neither"))


def bridge_on_cue(grids: dict, meta: list[dict], layers: list[int], cues: dict[str, str]) -> dict[str, float]:
    """Per eligible question: the share of layers 32-48 with the bridge first at an average cue token."""
    rows = [i for i, layer in enumerate(layers) if 32 <= layer <= 48]
    out = {}
    for m in meta:
        if m["status"] == "eligible" and m["name"] in cues and m["name"] in grids:
            cue = cue_positions(m["tokens"], cues[m["name"]])
            if cue:
                out[m["name"]] = float(np.mean([band_share(grids[m["name"]]["bridge_pool"], rows, c) for c in cue]))
    return out


def swap_flips(run: str) -> dict[str, bool]:
    from bridge_jspace.pins import RESULTS_DIR

    path = RESULTS_DIR / "exp02_swaps" / run / "outcomes.jsonl"
    rows = (json.loads(x) for x in path.read_text().splitlines() if x.strip())
    return {o["name"]: bool(o["flip"]) for o in rows if o["condition"] == "jpart" and not o["null"]}


def swap_group(name: str, flips: dict[str, dict[str, bool]]) -> str | None:
    if name not in flips["jlens"] or name not in flips["jpp"]:
        return None
    j, p = flips["jlens"][name], flips["jpp"][name]
    return "both" if j and p else "jpp_only" if p else "neither" if not j else "jlens_only"


def lens_comparison(per_q: dict[str, dict[str, float]], flips: dict[str, dict[str, bool]]) -> dict[str, Any]:
    """How alike the two lenses read the bridge per question, and the reading by how the cue-phrase swap went."""
    names = sorted(set(per_q["jlens"]) & set(per_q["jpp"]))
    a, b = [per_q["jlens"][n] for n in names], [per_q["jpp"][n] for n in names]
    out: dict[str, Any] = {"n": len(names), "pearson_r": round(float(np.corrcoef(a, b)[0, 1]), 4), "groups": {}}
    for key in (*(k for k, _ in GROUPS), "jlens_only"):
        members = [n for n in names if swap_group(n, flips) == key]
        out["groups"][key] = (
            {"n": len(members)}
            | {lens: _ci(bootstrap_mean([per_q[lens][n] for n in members], N_BOOT, SEED)) for lens in ("jlens", "jpp")}
            if members
            else {"n": 0}
        )
    return out


def plot_lenses(path: Path, per_q, flips, comparison, manifest) -> None:
    """Left: per lens, how often it reads the bridge on the cue phrase vs how often swapping along its directions there
    changes the answer; right: per question, the two lenses' readings against each other."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import INK, MUTED, SURFACE, finish, percent_axis, run_note, style_axes
    from bridge_jspace.stats import wilson

    lens_color = {"jlens": "#2a78d6", "jpp": "#eb6834"}
    lens_label = {"jlens": "J-lens", "jpp": "J++"}
    names = sorted(set(per_q["jlens"]) & set(per_q["jpp"]))
    fig, (ax_b, ax_s) = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=SURFACE, gridspec_kw={"width_ratios": [1.2, 1]})
    measures = []
    for lens in ("jlens", "jpp"):
        m, lo, hi = bootstrap_mean([per_q[lens][n] for n in names], N_BOOT, SEED)
        k = [flips[lens][n] for n in names if n in flips[lens]]
        f = wilson(sum(k), len(k))
        measures.append((lens, (m, lo, hi), f))
    width = 0.36
    for li, (lens, read, flip) in enumerate(measures):
        for gi, (m, lo, hi) in enumerate((read, flip)):
            x = gi + (li - 0.5) * width
            ax_b.bar(x, m, width * 0.9, color=lens_color[lens], zorder=2)
            ax_b.errorbar(x, m, yerr=[[max(m - lo, 0)], [max(hi - m, 0)]], color=INK, lw=1, capsize=2.5, zorder=3)
            ax_b.annotate(f"{m:.0%}", (x, hi), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9,
                          color=INK)  # fmt: skip
    ax_b.set_xticks(
        [0, 1],
        ["reads the bridge on the cue phrase\n(% of layers 32-48, average token)",
         "swapping it there changes the answer\n(% of questions, layers 24-40)"],
        fontsize=9,
    )  # fmt: skip
    ax_b.set_ylim(0, 1)
    ax_b.set_title("Same reading, different effect", color=INK, fontsize=11, loc="left")
    ax_s.scatter([per_q["jlens"][n] for n in names], [per_q["jpp"][n] for n in names], s=24, color=MUTED,
                 edgecolor=SURFACE, lw=0.6, zorder=3)  # fmt: skip
    ax_s.plot([0, 1], [0, 1], color=INK, lw=0.8, ls=":", zorder=1)
    ax_s.annotate(f"each dot: one question\nr = {comparison['pearson_r']:.2f} (n = {comparison['n']})", (0.03, 0.97),
                  xycoords="axes fraction", va="top", fontsize=9, color=INK)  # fmt: skip
    ax_s.set_xlim(-0.03, 1.03)
    ax_s.set_ylim(-0.03, 1.03)
    ax_s.set_xlabel("J-lens reads the bridge (% of layers 32-48)", color=MUTED)
    ax_s.set_ylabel("J++ reads the bridge\n(% of layers 32-48)", color=MUTED)
    ax_s.set_title("Question by question, the two readings agree", color=INK, fontsize=11, loc="left")
    for ax in (ax_b, ax_s):
        style_axes(ax)
        percent_axis(ax, "y")
    percent_axis(ax_s, "x")
    ax_b.grid(axis="x", visible=False)
    handles = [Patch(color=lens_color[lens], label=lens_label[lens]) for lens in ("jlens", "jpp")]
    finish(
        fig,
        path,
        "The J-lens and J++ read the bridge on the cue phrase equally, but swapping along J++'s directions works more often",
        f"{run_note(manifest, comparison['n'])} Reading: the share of layers 32-48 with the bridge first among the 97 "
        "entities at an average cue-phrase token. Swap: on the cue phrase (layers 24-40), the bridge's J-space part, "
        "built from each lens's own directions, is exchanged for the distractor's; a flip = the answer changes to the "
        "distractor's. Error bars: 95% CI (reading: bootstrap over questions; swap: Wilson).",
        handles,
    )


def plot_cue(path: Path, res: dict[str, Any], manifest: dict[str, Any], reader: str = "jlens") -> None:
    """Left: where the words are readable (layers 32-48, one average token per place), with layers 0-4 as the
    lexical baseline; right: by layer, the bridge on the cue phrase vs one word before the end, and the answer on the
    cue phrase vs the last word."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import (
        GRID,
        INK,
        MUTED,
        READER_TITLE,
        SURFACE,
        finish,
        percent_axis,
        run_note,
        style_axes,
    )

    colors = {"bridge": "#2a78d6", "answer": "#eb6834", "distractor": "#b4b2a9", "swap_answer": "#d6d4cc"}
    sites = (("cue_mean", "cue phrase\n(average token)"), ("noncue_mean", "other\nearlier words"),
             ("-1", "word before\nthe end (-1)"), ("0", "last word\n(0)"))  # fmt: skip
    words = ("bridge", "distractor", "answer", "swap_answer")
    fig, (ax_w, ax_l) = plt.subplots(1, 2, figsize=(13, 4.8), facecolor=SURFACE, gridspec_kw={"width_ratios": [1, 1.1]})
    band, lexical = res["bands"]["32-48"], res["bands"]["0-4"]
    width = 0.2
    for si, (site, _) in enumerate(sites):
        for wi, word in enumerate(words):
            v = band[word].get(site)
            if v is None:
                continue
            x = si + (wi - 1.5) * width
            ax_w.bar(x, v["mean"], width * 0.9, color=colors[word], zorder=2)
            ax_w.errorbar(x, v["mean"], yerr=[[max(v["mean"] - v["lo"], 0)], [max(v["hi"] - v["mean"], 0)]],
                          color=INK, lw=1, capsize=2, zorder=3)  # fmt: skip
            base = lexical[word].get(site)
            if base is not None:
                ax_w.plot([x - width * 0.45, x + width * 0.45], [base["mean"]] * 2, color=INK, lw=2, zorder=4)
    ax_w.set_xticks(range(len(sites)), [label for _, label in sites], fontsize=9)
    ax_w.set_ylim(0, 1)
    ax_w.set_ylabel("word ranked first in\n% of layers 32-48", color=MUTED)
    ax_w.set_title("Where in the prompt (layers 32-48)", color=INK, fontsize=11, loc="left")
    layers = res["layers"]
    ax_l.axvspan(32, 48, color=GRID, alpha=0.7, lw=0, zorder=0)
    ax_l.axhline(0.5, color=MUTED, lw=0.8, ls=":")
    by = res["by_layer"]
    for word, site, ls in (
        ("bridge", "cue", "-"),
        ("bridge", "-1", "--"),
        ("answer", "cue", "-"),
        ("answer", "0", "--"),
    ):
        ax_l.plot(layers, by[word][site]["share"], color=colors[word], lw=2.4, ls=ls)
    for word in ("distractor", "swap_answer"):
        ax_l.plot(layers, by[word]["cue"]["share"], color=colors[word], lw=1.2)
    ax_l.set_ylim(0, 1)
    ax_l.set_xlabel("model layer (0 = first)", color=MUTED)
    ax_l.set_ylabel("% of questions with the word\nranked first among its candidates", color=MUTED)
    ax_l.set_title("How deep: the cue phrase vs the read sites", color=INK, fontsize=11, loc="left")
    for ax in (ax_w, ax_l):
        style_axes(ax)
        percent_axis(ax)
    ax_w.grid(axis="x", visible=False)
    handles = [
        Patch(color=colors["bridge"], label="bridge (e.g. Brazil), among 97 entities"),
        Patch(color=colors["answer"], label="answer (e.g. Portuguese), among 112 answers"),
        Patch(color=colors["distractor"], label="controls: their same-category distractors"),
        Line2D([], [], color=INK, lw=2, label="left: layers 0-4 (the words' own associations)"),
        Line2D([], [], color=MUTED, lw=2.4, label="right: on the cue phrase (average token)"),
        Line2D([], [], color=MUTED, lw=2.4, ls="--", label="right: bridge at -1, answer at the last word"),
    ]
    best = band["bridge"]["cue_best"]["mean"], band["distractor"]["cue_best"]["mean"]
    finish(
        fig,
        path,
        f"{READER_TITLE.get(reader, reader)}: is the bridge, or already the answer, readable on the cue phrase?",
        f'{run_note(manifest, res["n"])} The cue phrase is the words that point to the bridge ("Amazon River ends"), '
        "where swapping the bridge changes the model's answer. Each place counts as one position (an average token "
        "of the cue phrase or of the other earlier words), so the bars compare like with like; the best cue token per "
        f"question (a search over ~5) reaches {best[0]:.0%} for the bridge and {best[1]:.0%} for its distractor. "
        "Error bars: 95% bootstrap CI over questions.",
        handles,
        ncols=3,
    )


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[1]))
