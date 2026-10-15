"""exp12 add-on: is the bridge, or already the answer, readable on the cue phrase, where part B's swap acts?

Reads a finished exp12 run's grids (no model). The cue phrase's positions are part B's `cue` regime (exp02): the
tokens of the phrase in data/cue_spans.json ("Amazon River ends"), without the prompt's last two positions (-1 and 0,
part A's read sites). Per question and reader, for each layer band:
  cue    the best share of band layers with the word ranked first among its candidates, over the cue tokens; the
         same search for its same-category control (distractor / swap answer) is the noise ceiling, since several
         tokens are searched
  noncue the same best share over the other earlier tokens (part B's `earlier_noncue` positions)
  -1, 0  the share at one word before the end and at the last word (exp12's read sites), for comparison
and per layer, the share of questions with the word ranked first at some cue token. 95% bootstrap CI over questions.
Layers 0-4 are the lexical baseline: a cue word's own associations ("Munich" -> Germany, "Romeo" -> Shakespeare)
already rank the bridge first there, so a band's share counts as computed only by how far it exceeds 0-4's.
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
    per_q: dict[str, Any] = {}
    for m in eligible:
        cue = cue_positions(m["tokens"], cues[m["name"]])
        noncue = [i for i in range(1, len(m["tokens"]) - 2) if i not in cue]
        per_q[m["name"]] = {"cue": cue, "noncue": noncue, "n_cue_tokens": len(cue)}
    for band, (lo, hi) in BANDS.items():
        rows = [i for i, layer in enumerate(layers) if lo <= layer <= hi]
        res: dict[str, Any] = {}
        for role, control in ROLES:
            for word in (role, control):
                vals: dict[str, list[float]] = {"cue": [], "noncue": [], "-1": [], "0": []}
                for m in eligible:
                    g = grids[m["name"]].get(f"{word}_pool")
                    cue = per_q[m["name"]]["cue"]
                    if g is None or not cue:
                        continue
                    last = len(m["tokens"]) - 1
                    vals["cue"].append(max(band_share(g, rows, c) for c in cue))
                    if per_q[m["name"]]["noncue"]:
                        vals["noncue"].append(max(band_share(g, rows, c) for c in per_q[m["name"]]["noncue"]))
                    vals["-1"].append(band_share(g, rows, last - 1))
                    vals["0"].append(band_share(g, rows, last))
                res[word] = {k: _ci(bootstrap_mean(v, N_BOOT, SEED)) | {"n": len(v)} for k, v in vals.items() if v}
        out["bands"][band] = res
    for role, control in ROLES:
        for word in (role, control):
            hits = []
            for m in eligible:
                g = grids[m["name"]].get(f"{word}_pool")
                cue = per_q[m["name"]]["cue"]
                if g is not None and cue:
                    hits.append((g[:, cue] == 1).any(axis=1))
            share = np.mean(hits, axis=0)
            reached = np.flatnonzero(share >= 0.5)
            out["by_layer"][word] = {
                "share": [round(float(s), 4) for s in share],
                "max": round(float(share.max()), 4),
                "first_layer_half": int(layers[reached[0]]) if reached.size else None,
            }
    out["cue_tokens_per_question"] = {
        "median": float(np.median([q["n_cue_tokens"] for q in per_q.values()])),
        "min": min(q["n_cue_tokens"] for q in per_q.values()),
        "max": max(q["n_cue_tokens"] for q in per_q.values()),
    }
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
    return out


def plot_cue(path: Path, res: dict[str, Any], manifest: dict[str, Any], reader: str = "jlens") -> None:
    """Left: where the words are readable (layers 32-48), with layers 0-4 as the lexical baseline; right: by layer,
    the share of questions with each word ranked first at some cue-phrase token."""
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
    sites = (("cue", "cue phrase\n(best token)"), ("noncue", "other earlier\nwords (best token)"),
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
            if base is not None and site in ("cue", "noncue"):
                ax_w.plot([x - width * 0.45, x + width * 0.45], [base["mean"]] * 2, color=INK, lw=2, zorder=4)
    ax_w.set_xticks(range(len(sites)), [label for _, label in sites], fontsize=9)
    ax_w.set_ylim(0, 1)
    ax_w.set_ylabel("word ranked first in\n% of layers 32-48", color=MUTED)
    ax_w.set_title("Where in the prompt (layers 32-48)", color=INK, fontsize=11, loc="left")
    layers = res["layers"]
    lo, hi = 32, 48
    ax_l.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    ax_l.axhline(0.5, color=MUTED, lw=0.8, ls=":")
    for word in words:
        ax_l.plot(
            layers, res["by_layer"][word]["share"], color=colors[word], lw=2.4 if word in ("bridge", "answer") else 1.2
        )
    ax_l.set_ylim(0, 1)
    ax_l.set_xlabel("model layer (0 = first)", color=MUTED)
    ax_l.set_ylabel("% of questions with the word ranked\nfirst at some cue-phrase token", color=MUTED)
    ax_l.set_title("How deep, on the cue phrase", color=INK, fontsize=11, loc="left")
    for ax in (ax_w, ax_l):
        style_axes(ax)
        percent_axis(ax)
    ax_w.grid(axis="x", visible=False)
    handles = [
        Patch(color=colors["bridge"], label="bridge (e.g. Brazil), among 97 entities"),
        Patch(color=colors["answer"], label="answer (e.g. Portuguese), among 112 answers"),
        Patch(color=colors["distractor"], label="controls: their same-category distractors"),
        Line2D([], [], color=INK, lw=2, label="layers 0-4: the cue words' own associations"),
        Patch(color=GRID, label="layers 32-48"),
    ]
    finish(
        fig,
        path,
        f"{READER_TITLE.get(reader, reader)}: is the bridge, or already the answer, readable on the cue phrase?",
        f'{run_note(manifest, res["n"])} The cue phrase is the words that point to the bridge ("Amazon River ends"), '
        'where swapping the bridge changes the model\'s answer. "Best token": the cue token with the highest share; the same search for the '
        "controls gives the noise ceiling. Error bars: 95% bootstrap CI over questions.",
        handles,
        ncols=3,
    )


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[1]))
