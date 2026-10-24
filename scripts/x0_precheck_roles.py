"""x0_precheck_roles (Dan, 24 Oct, before X0): on the 23 Oct necessity rows, where do the answers go?

Per run, cell (set, layer, reader) and arm (part; real rows of C's copy, and their random-direction nulls apart), the
shares of the read's role: alt (b, the other bridge's answer), org (A, the clean answer) and other. J-dependence counts
only the switches to alt; this shows whether an arm that switches fewer answers sends them back to org or breaks them.
Descriptive, no rule. Writes results/x0_precheck_roles/<UTC>/{roles.csv, roles.md, roles_<run>.png}.

  uv run python scripts/x0_precheck_roles.py [--runs RUN ...]
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of

PARTS_DIR = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "x0_precheck_roles"
RUNS = ("d1_necessity_parts_27b_r2", "qwen35_9b_d1_necessity_parts_r2", "olmo3_7b_instruct_jpp_d1_necessity_parts_r2")
ROLES = (("b", "alt"), ("A", "org"), ("other", "other"))
FIGURE_ARMS = ("full", "not_jspace", "not_rand_sub", "jspace", "rand_sub", "rand_omp")  # the X0 arms and their parts
READER = {"PP": "lookup", "PM": "recall"}


def role_shares(rows: list[dict]) -> dict[tuple, dict]:
    """(set, layer, reader, part, null) -> n and the share of each role, over rows of C's copy (source cf)."""
    count: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["source"] == "cf":
            count[(r["set"], r["layer"], r["family"], r["part"], r["null"])][r["role"]] += 1
    return {k: {"n": sum(c.values()), **{name: c[role] / sum(c.values()) for role, name in ROLES}}
            for k, c in sorted(count.items())}  # fmt: skip


def figure(run: str, shares: dict[tuple, dict], folder: Path) -> Path:
    """One panel per (set, reader): stacked alt / org / other bars per arm, layers side by side."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    sets = sorted({k[0] for k in shares})
    layers = sorted({k[1] for k in shares})
    fig, axes = plt.subplots(len(sets), 2, figsize=(13, 3.2 * len(sets)), squeeze=False, sharey=True)
    colors = {"alt": F.LOOKUP, "org": F.CONTROL, "other": "#e31a1c"}
    width = 0.8 / len(FIGURE_ARMS)
    for i, s in enumerate(sets):
        for j, fam in enumerate(READER):
            ax = axes[i][j]
            for a, arm in enumerate(FIGURE_ARMS):
                xs = [li + (a - (len(FIGURE_ARMS) - 1) / 2) * width for li in range(len(layers))]
                bottom = [0.0] * len(layers)
                for _, name in ROLES:
                    v = [shares.get((s, la, fam, arm, False), {}).get(name, 0.0) for la in layers]
                    ax.bar(xs, v, width * 0.92, bottom=bottom, color=colors[name],
                           label=name if (a == 0 and i == 0 and j == 0) else None)  # fmt: skip
                    bottom = [b + x for b, x in zip(bottom, v, strict=True)]
                if i == len(sets) - 1:
                    for x in xs:
                        ax.text(x, -0.04, arm.replace("not_", "−").replace("_sub", ""), rotation=90, fontsize=6,
                                ha="center", va="top")  # fmt: skip
            ax.set_xticks(range(len(layers)), [f"L{la}" for la in layers])
            ax.tick_params(axis="x", pad=42 if i == len(sets) - 1 else 4)
            ax.set_title(f"{s}, {READER[fam]} ({fam})", fontsize=9)
            ax.set_ylim(0, 1)
    axes[0][0].legend(fontsize=8, ncol=3, loc="lower left")
    fig.suptitle(f"{run}: where the answers go per arm (alt = switched; org = clean answer kept; other = neither). "
                 "Arms left to right: " + ", ".join(FIGURE_ARMS), fontsize=9)  # fmt: skip
    fig.tight_layout()
    path = folder / f"roles_{run}.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", default=list(RUNS))
    a = ap.parse_args()
    folder = OUT / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    folder.mkdir(parents=True)
    table, lines = [], ["# Where the answers go: role shares per cell and arm (23 Oct necessity rows)", "",
                        "Rows of C's copy (source cf); `null` = the arm's random-direction null. alt = the other "
                        "bridge's answer (switched), org = the clean answer, other = neither. Descriptive.", ""]  # fmt: skip
    for run in a.runs:
        path = PARTS_DIR / run / "outcomes.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        shares = role_shares(rows)
        table += [{"run": run, "set": s, "layer": la, "reader": fam, "part": part, "null": null, **v}
                  for (s, la, fam, part, null), v in shares.items()]  # fmt: skip
        lines += [f"## {run} (outcomes.jsonl sha256 {sha256_of(path)[:16]})", "",
                  "| set | layer | reader | arm | n | alt | org | other |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for (s, la, fam, part, null), v in shares.items():
            if part in FIGURE_ARMS and not null:
                lines.append(f"| {s} | {la} | {READER[fam]} | {part} | {v['n']} | {v['alt']:.2f} | {v['org']:.2f} | "
                             f"{v['other']:.2f} |")  # fmt: skip
        lines += ["", f"![{run}](roles_{run}.png)", ""]
        print(figure(run, shares, folder))
    with (folder / "roles.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    (folder / "roles.md").write_text("\n".join(lines) + "\n")
    print(folder / "roles.md")


if __name__ == "__main__":
    main()
