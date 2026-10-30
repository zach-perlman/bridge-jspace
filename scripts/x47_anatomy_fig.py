"""The 47.8 figure (jobs/c3/batch47.yaml, 47.8 "figure"): one column per model, x = layer as a fraction of depth,
'not interpretable' shading where the whole change switches < 30% of a reader, five rows: (1) the lookup under the whole
change, stacked identity / position / value / original; (2) what carries each route: position share with only U_l,
identity share with only J++ and with only I_l, thin grey lines the random keep-only parts of the same share; (3) what
each route needs: the lookup's extra loss without J++ / U_l / I_l; (4) the recall: its switch under the whole change,
its extra loss without J++ and without I_l, the share of recalls naming the slot item; (5) the probes at the bridge word
(identity, slot, digit dotted) with the J++ share of U_l and of I_l beside. story_style's look.

Data contract (x47_anatomy.figure_data; preview_models builds the same from the Fig 6 runs): per model a dict with
target, n_layers, L, layers, ni {"lookup": [layers], "recall": [layers]}, rows {quantity: {layer: [v, lo, hi]}}
(lo / hi None where there is no interval), status. Quantities: lookup.whole.<route>; keep_U.position,
keep_U_rand.position, keep_J.identity, keep_J_rand.identity, keep_I.identity, keep_I_rand.identity; loss.lookup.<P>,
loss.recall.<P> for P in J, U, I; recall.whole.switch, recall.whole.slot; probe.identity, probe.slot, probe.digit;
jpp_share.U, jpp_share.I; lens_top10. A quantity absent from a model is skipped (the preview has only some).

uv run python scripts/x47_anatomy.py preview      # results/x47_anatomy/preview-<UTC>/x47_anatomy_preview.png
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from bridge_jspace import pins
from scripts import story_style as S
from scripts import x0_necessity as X

MODELS = (("qwen3.5-9b", "9b", "Qwen3.5-9B", 32), ("qwen3.6-27b", "27b", "Qwen3.6-27B", 64),
          ("muse-glimmer-30b", "muse", "Muse Glimmer 30B", 52))  # fmt: skip
NAME = {t: n for t, _, n, _ in MODELS}
KEEP_RUNS = {"9b": "qwen35_9b_x6_routes_keeponly", "27b": "x6_routes_keeponly_27b"}  # keep-only arms at L (Muse: none)
PROBE_RUNS = {"9b": "qwen35_9b_x0_probe_v4", "27b": "x0_probe_v4_27b", "muse": "muse30b_x0_probe_v4"}
ROWS = ("lookup under the whole change", "what carries each route (keep-only)", "what each route needs (extra loss)",
        "the recall", "probes at the bridge word")  # fmt: skip
ROUTE_COL = {"identity": S.COL["identity"], "position": S.COL["position"], "value": S.COL["value"],
             "original": S.COL["original"]}  # fmt: skip
I_COL = "#7fb3d5"  # identity outside the lens: a lighter identity blue
NI = "#e6e6e6"  # not interpretable


def _xy(rows: dict[str, dict], key: str, n_layers: int):
    pts = sorted((int(la), v) for la, v in rows.get(key, {}).items())
    x = [la / n_layers for la, _ in pts]
    return x, [v[0] for _, v in pts], [v[1] for _, v in pts], [v[2] for _, v in pts]


def _line(ax, rows, key, n_layers, color, ls="-", lw=1.8, marker: str | None = "o", band=True, ms=4, label=None):
    x, y, lo, hi = _xy(rows, key, n_layers)
    if not x:
        return False
    if band and all(v is not None for v in lo):
        ax.fill_between(x, lo, hi, color=color, alpha=0.12, lw=0)
    ax.plot(
        x, y, ls=ls, lw=lw, color=color, marker=marker, ms=ms, mfc="white" if marker else None, mew=1.2, label=label
    )
    return True


def _shade(ax, m: dict, reader: str) -> None:
    layers = sorted(m["layers"])
    half = (layers[1] - layers[0]) / 2 / m["n_layers"] if len(layers) > 1 else 0.02
    for la in m["ni"].get(reader, []):
        ax.axvspan(la / m["n_layers"] - half, la / m["n_layers"] + half, color=NI, lw=0, zorder=0)


def figure(models: list[dict], path: Path, preview: bool = False) -> Path:
    plt = S.setup()
    cols = max(1, len(models))
    fig, axes = plt.subplots(5, cols, figsize=(S.WIDTH, 12.5), sharex="col", squeeze=False)
    fig.subplots_adjust(left=0.1, right=0.99, top=0.80, bottom=0.06, wspace=0.12, hspace=0.22)
    S.title(fig, "Layer anatomy of the switch: what the bridge word's change moves, through which part"
            + (" (PREVIEW)" if preview else ""),
            ("PREVIEW from the Fig 6 runs (main-test depth cells; routes runs where they exist): the code path, not the data.\n"
             if preview else "47.8 sweep, test half (another item moved, locker-first).\n")
            + "x = layer / depth. Grey columns: the whole change switches < 30% of the reader (not read). Dotted line = L.\n"
            "Thin grey = a random part of the same share. UNVERIFIED.", limit=100)  # fmt: skip
    for j, m in enumerate(models):
        n, rows, L = m["n_layers"], m["rows"], m["L"]
        layers = sorted(m["layers"])
        w = (layers[1] - layers[0]) / n * 0.8 if len(layers) > 1 else 0.02
        ax = axes[0, j]
        ax.set_title(f"{NAME.get(m['target'], m['target'])}\nL{L} of {n}", fontsize=S.FONT, weight="bold")
        _shade(ax, m, "lookup")
        bottom = {la: 0.0 for la in layers}
        for rt in ("identity", "position", "value", "original"):
            pts = rows.get(f"lookup.whole.{rt}", {})
            for la_s, v in pts.items():
                la = int(la_s)
                ax.bar(la / n, v[0], width=w, bottom=bottom.get(la, 0.0), color=ROUTE_COL[rt], lw=0)
                bottom[la] = bottom.get(la, 0.0) + v[0]
        ax.set_ylim(0, 1)
        ax = axes[1, j]
        _shade(ax, m, "lookup")
        _line(ax, rows, "keep_U_rand.position", n, S.COL["control"], lw=1, marker=None)
        _line(ax, rows, "keep_J_rand.identity", n, S.COL["control"], lw=1, marker=None)
        _line(ax, rows, "keep_I_rand.identity", n, S.COL["control"], lw=1, marker=None, ls="--")
        _line(ax, rows, "keep_U.position", n, S.COL["position"])
        _line(ax, rows, "keep_J.identity", n, S.COL["identity"])
        _line(ax, rows, "keep_I.identity", n, I_COL, ls="--", marker="s")
        ax.set_ylim(0, 1)
        ax = axes[2, j]
        _shade(ax, m, "lookup")
        ax.axhspan(S.XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
        ax.axhline(0, color="#999999", lw=0.8)
        _line(ax, rows, "loss.lookup.J", n, S.COL["identity"])
        _line(ax, rows, "loss.lookup.U", n, S.COL["position"])
        _line(ax, rows, "loss.lookup.I", n, I_COL, ls="--", marker="s")
        ax.set_ylim(*S.XLIM)
        ax = axes[3, j]
        _shade(ax, m, "recall")
        ax.axhspan(S.XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
        ax.axhline(0, color="#999999", lw=0.8)
        _line(ax, rows, "recall.whole.switch", n, S.COL["recall"], marker="D", band=False)
        _line(ax, rows, "loss.recall.J", n, S.COL["identity"])
        _line(ax, rows, "loss.recall.I", n, I_COL, ls="--", marker="s")
        _line(ax, rows, "recall.whole.slot", n, S.COL["position"], ls=":", marker=None, band=False)
        ax.set_ylim(*S.XLIM)
        ax = axes[4, j]
        _line(ax, rows, "probe.identity", n, S.COL["identity"], band=False)
        _line(ax, rows, "probe.slot", n, S.COL["position"], band=False)
        _line(ax, rows, "probe.digit", n, S.COL["value"], ls=":", band=False)
        _line(ax, rows, "jpp_share.U", n, S.COL["position"], lw=1, marker="x", band=False)
        _line(ax, rows, "jpp_share.I", n, S.COL["identity"], lw=1, marker="x", band=False)
        _line(ax, rows, "lens_top10", n, S.COL["muted"], lw=1, marker=None, ls="-.", band=False)
        ax.axhline(0.8, color="#bbbbbb", lw=0.8, ls=":")
        ax.set_ylim(0, 1)
        for i in range(5):
            axes[i, j].axvline(L / n, color="#555555", lw=0.8, ls=":")
            axes[i, j].set_xlim(0, 1)
            axes[i, j].grid(axis="y", color="#eeeeee")
            if j:
                axes[i, j].tick_params(labelleft=False)
        axes[4, j].set_xlabel("layer / depth")
        axes[4, j].set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", ".25", ".5", ".75", "1"])
    labels = ("lookup answers\n(whole change)", "keep-only share", "lookup extra loss", "recall", "probe accuracy")
    for i, lab in enumerate(labels):
        axes[i, 0].set_ylabel(lab)
    hs = [Rectangle((0, 0), 1, 1, color=ROUTE_COL[rt]) for rt in ("identity", "position", "value", "original")]
    ls = ["identity", "position", "value", "original (unchanged)"]
    hs += [Line2D([], [], color=S.COL["identity"], marker="o", mfc="white"), Line2D([], [], color=I_COL, ls="--", marker="s", mfc="white"),
           Line2D([], [], color=S.COL["position"], marker="o", mfc="white"), Line2D([], [], color=S.COL["recall"], marker="D", mfc="white"),
           Line2D([], [], color=S.COL["position"], ls=":"), Line2D([], [], color=S.COL["value"], ls=":", marker="o", mfc="white"),
           Line2D([], [], color="#888888", marker="x", lw=1), Line2D([], [], color=S.COL["muted"], ls="-.", lw=1)]  # fmt: skip
    ls += ["J++ part / identity probe", "identity outside the lens (I_l)", "address (U_l) / slot probe", "recall switch (whole)",
           "recalls naming the slot item", "digit probe", "J++ share of U_l (orange) / I_l (blue)", "lens top-10 (bridge token)"]  # fmt: skip
    fig.legend(hs, ls, loc="upper left", bbox_to_anchor=(0.01, 0.905), ncol=3, frameon=False, fontsize=S.FONT - 1,
               handlelength=1.6, columnspacing=1.2)  # fmt: skip
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)
    return path


# ---- the CPU preview from the Fig 6 runs ----------------------------------------------------------------------------


def _latest(path: Path, pattern: str):
    found = sorted(path.glob(pattern))
    return json.loads(found[-1].read_text()) if found else None


def preview_models() -> list[dict]:
    """The contract's dicts from what exists: the main test's depth cells (readme_story_figures.depth_run; J++ extra
    loss and the whole change's switch per reader), the routes verdicts at ROUTE_LAYERS (C2 whole shares), the keep-only
    runs at L (keep_jpp / keep_alf), x0_probe v4 at L (locker-before stratum)."""
    from scripts import readme_story_figures as RF
    from scripts import x0_figures as XF

    out = []
    for target, m, _, n_layers in MODELS:
        rows: dict[str, dict] = {}
        ni: dict[str, list[int]] = {"lookup": [], "recall": []}
        L = X.PREDICTED[target]
        run = RF.depth_run(m)
        layers: set[int] = set()
        if (X.RESULTS / run / "outcomes.jsonl").exists():
            cells = XF.Run(run).cells("chat")
            for (_rend, la, w, dic, k, omp), c in cells.items():
                if (dic, k, omp) != X.MAIN:
                    continue
                name = "lookup" if w == X.LOOKUP else "recall"
                layers.add(la)
                rows.setdefault(f"loss.{name}.J", {})[la] = c["excess"]
                if name == "recall":
                    rows.setdefault("recall.whole.switch", {})[la] = list(c["S_whole"])
                if c["S_whole"][0] < 0.30:
                    ni[name].append(la)
        for run, la, _ in RF.ROUTE_LAYERS.get(m, ()):
            v = _latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
            r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == "whole"), None)
            if r is None:
                continue
            layers.add(la)
            for rt in ("identity", "position", "value", "original"):
                rows.setdefault(f"lookup.whole.{rt}", {})[la] = r["share"][rt]
        if m in KEEP_RUNS:
            v = _latest(pins.RESULTS_DIR / "x6_routes" / KEEP_RUNS[m], "verdict-*/verdict.json")
            for r in (v or {}).get("rows", []):
                if r["condition"] != "C2":
                    continue
                for arm, key, rt in (
                    ("keep_alf", "keep_U", "position"),
                    ("keep_alf_rand", "keep_U_rand", "position"),
                    ("keep_jpp", "keep_J", "identity"),
                    ("keep_jpp_rand", "keep_J_rand", "identity"),
                ):
                    if r["arm"] == arm:
                        rows.setdefault(f"{key}.{rt}", {})[L] = r["share"][rt]
        p = _latest(pins.RESULTS_DIR / "x0_probe" / PROBE_RUNS[m], "probe-*/probe.json")
        for r in (p or {}).get("rows", []):
            if r["subset"] == "all" and r["stratum"] == "before":
                key = {"bridge identity": "identity", "locker sentence": "slot", "answer digit": "digit"}[r["target"]]
                rows.setdefault(f"probe.{key}", {})[L] = r["probe"]
        out.append({"target": target, "n_layers": n_layers, "L": L, "layers": sorted(layers) or [L], "ni": ni,
                    "rows": rows, "status": "preview from the Fig 6 runs", "sources": {"depth": run,
                    "routes": [r for r, _, _ in RF.ROUTE_LAYERS.get(m, ())], "keep": KEEP_RUNS.get(m), "probe": PROBE_RUNS[m]}})  # fmt: skip
    return out
