"""write_max_report: the dose-response behind write_max v2's best cells (Zach, 2026-10-21). summary.md reports one
best gated cell per write; this shows, per family, how the flip rate to C's answer grows with strength at each site,
next to the matched-norm random control's keep rate (the breakage gate) and the mean fraction of the way to C's logit
difference (frac: 0 = the clean run, 1 = C's run). Figure: flips vs strength for lens_add and dom_add on every band
layer at once (joint), one panel per position set; hollow markers = cells failing the gate (control keeps < 95%).

python scripts/write_max_report.py RUN [RUN ...]   (writes results/write_max/RUN/report.md and report.png)
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.write_max import KEEP_GATE, RESULTS

NAMES = {"BL": "P->P", "RL": "M->P", "BR": "P->M", "RR": "M->M", "R": "countries, recalled", "B": "countries, given",
         "PP": "P->P", "MP": "M->P", "PM": "P->M", "MM": "M->M"}  # fmt: skip
COLOR = {"BL": "#2a78d6", "RL": "#2a78d6", "BR": "#eb6834", "RR": "#eb6834", "R": "#1baf7a", "B": "#1baf7a",
         "PP": "#2a78d6", "MP": "#2a78d6", "PM": "#eb6834", "MM": "#eb6834"}  # fmt: skip
STYLE = {
    "BL": "-",
    "RL": "--",
    "BR": "-",
    "RR": "--",
    "R": "--",
    "B": "-",
    "PP": "-",
    "MP": "--",
    "PM": "-",
    "MM": "--",
}
LENS = ("lens_add", "lens_swap", "lens_transpl")
DOM = ("dom_add", "dom_natural")


def pct(v: float | None) -> str:
    return "-" if v is None else f"{100 * v:.0f}"


def report(run: str) -> None:
    out = RESULTS / run
    rows = [json.loads(line) for line in (out / "outcomes.jsonl").read_text().splitlines()]
    summary = json.loads((out / "summary.json").read_text())
    cells: dict = collections.defaultdict(list)
    for r in rows:
        cells[(r["family"], r["write"], r["pos"], str(r["layer"]), r["strength"], r["control"])].append(r)
    fams = list(dict.fromkeys(r["family"] for r in rows))
    possets = list(dict.fromkeys(r["pos"] for r in rows if not r["write"].startswith("early")))

    def stat(fam, write, pos, layer, s) -> dict | None:
        os_ = cells.get((fam, write, pos, layer, s, False))
        if not os_:
            return None
        ctrl = cells.get((fam, write, pos, layer, s, True))
        keep = statistics.mean(o["role"] == "A" for o in ctrl) if ctrl else None
        return {"flips": statistics.mean(o["role"] == "b" for o in os_), "keep": keep,
                "ctrl_flips": statistics.mean(o["role"] == "b" for o in ctrl) if ctrl else None,
                "frac": statistics.median(o["frac"] for o in os_), "other": statistics.mean(o["role"] == "other" for o in os_),
                "gated": write == "copy" or (keep is not None and keep >= KEEP_GATE), "n": len(os_)}  # fmt: skip

    lines = [f"# write_max report / {run}", "",
             "Cells: flips to C's answer % (its random control keeps the clean answer %; median frac). "
             f"`*` = fails the breakage gate (control keeps < {KEEP_GATE:.0%}). Layer \"joint\" = every band layer at once.",
             ""]  # fmt: skip
    # headline: best gated lens / dom / copy per family, from summary.json, with the early injection pair
    lines += ["## Best gated cell per write group (from summary.json) [95% CI over bridge entities]", "",
              "| family | n | lens (best of add/swap/transplant) | its control flips | dom (best of add/natural) | copy | "
              "early lens_add | early embed_add |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for fam in fams:
        best = summary["families"][fam]["best"]

        def top(writes, best=best):
            got = [(w, best[w]) for w in writes if best.get(w)]
            return max(got, key=lambda x: x[1]["flips"]) if got else (None, None)

        def show(wb):
            w, b = wb
            if not b:
                return "-"
            return f"{pct(b['flips'])} [{pct(b['ci'][0])}-{pct(b['ci'][1])}] ({w}, {b['pos']}, {b['layer']}, {b['strength']:g})"

        lw, lb = top(LENS)
        lines.append(f"| {NAMES.get(fam, fam)} | {summary['families'][fam]['n']} | {show((lw, lb))} | "
                     f"{pct(lb['control']) if lb else '-'} | {show(top(DOM))} | {show(top(('copy',)))} | "
                     f"{show(top(('early_lens_add',)))} | {show(top(('early_embed_add',)))} |")  # fmt: skip
    if "rule" in summary:
        lines += ["", f"Rules: `{json.dumps(summary['rule'])}`"]
    lines.append("")
    # dose tables: joint layer, each write's strengths
    for write in ("lens_add", "lens_swap", "lens_transpl", "dom_add", "dom_natural"):
        strengths = sorted({k[4] for k in cells if k[1] == write})
        if not strengths:
            continue
        for pos in possets:
            lines += [f"## {write}, {pos} positions, joint", "",
                      "| family | " + " | ".join(f"{s:g}" for s in strengths) + " |", "|---" * (len(strengths) + 1) + "|"]  # fmt: skip
            for fam in fams:
                cs = []
                for s in strengths:
                    st = stat(fam, write, pos, "joint", s)
                    cs.append("-" if not st else f"{pct(st['flips'])}{'' if st['gated'] else '*'} ({pct(st['keep'])}; "
                              f"{st['frac']:.2f})")  # fmt: skip
                lines.append(f"| {NAMES.get(fam, fam)} | " + " | ".join(cs) + " |")
            lines.append("")
    # where along the band: best gated flips over strength, single layers, lens_add / dom_add / copy
    singles = sorted({int(k[3]) for k in cells if k[3] != "joint" and not k[1].startswith("early")})
    for write in ("lens_add", "dom_add", "copy"):
        for pos in possets:
            lines += [f"## {write}, {pos} positions, single layers: best gated flips % over strength", "",
                      "| family | " + " | ".join(f"L{la}" for la in singles) + " |", "|---" * (len(singles) + 1) + "|"]  # fmt: skip
            for fam in fams:
                cs = []
                for la in singles:
                    sts = [st for s in sorted({k[4] for k in cells if k[1] == write})
                           if (st := stat(fam, write, pos, str(la), s)) and st["gated"]]  # fmt: skip
                    cs.append(pct(max(st["flips"] for st in sts)) if sts else "-")
                lines.append(f"| {NAMES.get(fam, fam)} | " + " | ".join(cs) + " |")
            lines.append("")
    # injection control
    early = sorted({k[3] for k in cells if k[1].startswith("early")}, key=int)
    if early:
        strengths = sorted({k[4] for k in cells if k[1] == "early_lens_add"})
        lines += ["## Injection control (question positions): early lens_add vs embed_add, flips % (control keeps %)", "",
                  "| family | layer | " + " | ".join(f"lens {s:g} / embed {s:g}" for s in strengths) + " |",
                  "|---|---|" + "---|" * len(strengths)]  # fmt: skip
        for fam in fams:
            for la in early:
                cs = []
                for s in strengths:
                    a, b = (
                        stat(fam, "early_lens_add", "question", la, s),
                        stat(fam, "early_embed_add", "question", la, s),
                    )
                    cs.append(f"{pct(a and a['flips'])}{'' if a and a['gated'] else '*'} / "
                              f"{pct(b and b['flips'])}{'' if b and b['gated'] else '*'}")  # fmt: skip
                lines.append(f"| {NAMES.get(fam, fam)} | L{la} | " + " | ".join(cs) + " |")
        lines.append("")
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    # figure
    fig, axes = plt.subplots(2, len(possets), figsize=(4.6 * len(possets), 7.6), sharey=True, squeeze=False,
                             facecolor="#fcfcfb")  # fmt: skip
    for row, write in enumerate(("lens_add", "dom_add")):
        strengths = sorted({k[4] for k in cells if k[1] == write})
        for col, pos in enumerate(possets):
            ax = axes[row][col]
            for fam in fams:
                pts = [(s, st) for s in strengths if (st := stat(fam, write, pos, "joint", s))]
                if not pts:
                    continue
                xs, ys = [s for s, _ in pts], [100 * st["flips"] for _, st in pts]
                ax.plot(xs, ys, color=COLOR.get(fam, "#555"), ls=STYLE.get(fam, "-"), lw=1.8, label=NAMES.get(fam, fam))
                for (s, st), y in zip(pts, ys, strict=True):
                    ax.plot([s], [y], marker="o", ms=5, color=COLOR.get(fam, "#555"),
                            mfc=COLOR.get(fam, "#555") if st["gated"] else "#fcfcfb")  # fmt: skip
            ax.set_xscale("log")
            if strengths:
                ax.set_xticks(strengths, [f"{s:g}" for s in strengths])
            ax.minorticks_off()
            ax.set_ylim(-3, 103)
            ax.set_title(f"{write}, {pos} positions, all band layers", loc="left", fontweight="bold", fontsize=9)
            ax.set_xlabel("strength (alpha x |h|)")
            ax.grid(color="#e6e5e0")
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
        axes[row][0].set_ylabel("flips to C's answer (%)")
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="lower center", ncol=len(labels), frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.03)
    )
    fig.subplots_adjust(hspace=0.38)
    fig.suptitle(f"{run}: can a write along the lens (top) or a difference of means (bottom) move the bridge? "
                 "Hollow = random control breaks the model", x=0.01, ha="left", fontweight="bold", fontsize=10)  # fmt: skip
    fig.savefig(out / "report.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    for run in ap.parse_args().runs:
        report(run)
