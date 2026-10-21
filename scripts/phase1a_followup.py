"""Phase 1a follow-up analysis (Zach, 2026-10-20/21): the dose curve (dose_v1: top-K lens directions removed, answer
kept, K = 5-100, with rotated controls, at L32-40 and L12-20), the position split (pos_context_v1, pos_question_v1:
paper10 at L12-20, L20-28, L32-40 on the facts only or the question and after only, next to all positions from
depth_coarse_v1) and name vs digit answers (answertype_v2: tool_answer_type's JSON scenes under paper10 at L32-40 and
L52-60, on the items right unedited). 95% intervals by bootstrap over bridge entities. Writes OUT.md and OUT_dose.png.

python scripts/phase1a_followup.py OUT      (reads results/ablate_v2/...; CPU only)
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts.depth_verdict import bridges_of, cluster_ci

OUT = Path(sys.argv[1])
RES = pins.RESULTS_DIR / "ablate_v2"
FAMS = ["BL", "RL", "BR", "RR", "country-R", "country-B"]
NAMES = {"BL": "P->P", "RL": "M->P", "BR": "P->M", "RR": "M->M", "country-R": "countries, recalled",
         "country-B": "countries, given"}  # fmt: skip
BRIDGE = bridges_of()


def rows(run: str) -> list[dict]:
    path = RES / run / "rows.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def cell(rs: list[dict]) -> str:
    if not rs:
        return "-"
    acc = statistics.mean(r["correct"] for r in rs)
    lo, hi = cluster_ci(rs, BRIDGE)
    return f"{100 * acc:.0f} [{100 * lo:.0f}-{100 * hi:.0f}]"


def by(rs: list[dict], **kw) -> list[dict]:
    return [r for r in rs if all(r.get(k) == v for k, v in kw.items())]


lines = ["# Phase 1a follow-up (27B)", ""]

# ---- dose curve ----
dose = rows("dose_v1")
ks = sorted({int(m[1]) for r in dose if (m := re.fullmatch(r"top(\d+)", r["condition"]))})
if dose:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True, facecolor="#fcfcfb")
    colors = {"BL": "#2a78d6", "RL": "#2a78d6", "BR": "#eb6834", "RR": "#eb6834", "country-R": "#1baf7a",
              "country-B": "#1baf7a"}  # fmt: skip
    styles = {"BL": "-", "RL": "--", "BR": "-", "RR": "--", "country-R": "--", "country-B": "-"}
    for ax, band in zip(axes, ("L32-40", "L12-20"), strict=True):
        lines += [f"## Dose curve at {band}: accuracy (%) with the top K lens directions removed (answer kept) "
                  "[95% CI over bridge entities]; control = the same removal turned by a random rotation", "",
                  "| family | " + " | ".join(f"K={k}" for k in ks) + " | controls (lowest over K) |",
                  "|---" * (len(ks) + 2) + "|"]  # fmt: skip
        for fam in FAMS:
            accs = []
            row = []
            for k in ks:
                rs = by(dose, band=band, family=fam, condition=f"top{k}", kind="clean")
                row.append(cell(rs))
                accs.append(100 * statistics.mean(r["correct"] for r in rs) if rs else None)
            ctrl = [statistics.mean(r["correct"] for r in by(dose, band=band, family=fam, condition=f"top{k}_rot"))
                    for k in ks if by(dose, band=band, family=fam, condition=f"top{k}_rot")]  # fmt: skip
            lines.append(f"| {NAMES[fam]} | " + " | ".join(row) + (f" | {100 * min(ctrl):.0f} |" if ctrl else " | - |"))
            if any(a is not None for a in accs):
                ax.plot(ks, accs, color=colors[fam], ls=styles[fam], marker="o", lw=1.8, ms=4, label=NAMES[fam])
        ax.set_xscale("log")
        ax.set_xticks(ks, [str(k) for k in ks])
        ax.set_ylim(-3, 103)
        ax.set_title(f"layers {band[1:]}", loc="left", fontweight="bold", fontsize=10)
        ax.set_xlabel("lens directions removed per position (K)")
        ax.grid(color="#e6e5e0")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        lines.append("")
    axes[0].set_ylabel("accuracy (%)")
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Qwen3.6-27B: how many lens directions must be removed before each family breaks?", x=0.01,
                 ha="left", fontweight="bold")  # fmt: skip
    fig.savefig(f"{OUT}_dose.png", dpi=160, bbox_inches="tight")

# ---- position split ----
coarse, ctx, qst = rows("depth_coarse_v1"), rows("pos_context_v1"), rows("pos_question_v1")
if ctx or qst:
    lines += ["## Position split: paper10 accuracy (%) when removing at every position, the facts only (before the "
              "question), or the question and after only", "",
              "| band | family | all positions | facts only | question only | control (facts / question) |",
              "|---|---|---|---|---|---|"]  # fmt: skip
    for band in ("L12-20", "L20-28", "L32-40"):
        for fam in FAMS:
            c_ctl = by(ctx, band=band, family=fam, condition="paper10_rot")
            q_ctl = by(qst, band=band, family=fam, condition="paper10_rot")
            ctl = "/".join(
                f"{100 * statistics.mean(r['correct'] for r in x):.0f}" if x else "-" for x in (c_ctl, q_ctl)
            )
            lines.append(f"| {band} | {NAMES[fam]} | {cell(by(coarse, band=band, family=fam, condition='paper10'))} | "
                         f"{cell(by(ctx, band=band, family=fam, condition='paper10'))} | "
                         f"{cell(by(qst, band=band, family=fam, condition='paper10'))} | {ctl} |")  # fmt: skip
    lines.append("")

# ---- name vs digit ----
at = rows("answertype_v2")
if at:
    ok = {(r["family"], r["id"]) for r in at if r["condition"] == "none" and r["correct"]}
    lines += ["## Name vs digit (same JSON scenes; items right unedited)", "",
              "| band | answer | n | paper10 | rotated control |", "|---|---|---|---|---|"]  # fmt: skip
    for band in ("L32-40", "L52-60"):
        for fam in ("AT-name", "AT-digit"):
            rs = [r for r in by(at, band=band, family=fam, condition="paper10") if (fam, r["id"]) in ok]
            ct = [r for r in by(at, band=band, family=fam, condition="paper10_rot") if (fam, r["id"]) in ok]
            lines.append(f"| {band} | {fam[3:]} | {len(rs)} | {cell(rs)} | {cell(ct)} |")
    lines.append("")
    unedited = {f: statistics.mean(r["correct"] for r in at if r["condition"] == "none" and r["family"] == f)
                for f in ("AT-name", "AT-digit")}  # fmt: skip
    lines.append(f"Unedited accuracy: name {100 * unedited['AT-name']:.0f}%, digit {100 * unedited['AT-digit']:.0f}%")

Path(f"{OUT}.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
