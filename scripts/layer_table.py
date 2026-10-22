"""layer_table (the night brief's T4, CPU): by layer, the full copy of C at the stated bridge's word / sentence (a D1
map run, prompt -> prompt and prompt -> memory) next to the lens push's lookup and recall rates at the word / sentence
(D4 runs, 8x). Descriptive; written to results/layer_table/<stamp>/table.md.

uv run python scripts/layer_table.py --map d1_topics2_map_27b --d4 d4_where_27b d4_where_fresh_27b
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins

SP = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "layer_table"


def main() -> int:
    from scripts import early_push_where as W

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True)
    ap.add_argument("--d4", nargs="+", required=True)
    a = ap.parse_args()
    rates = json.loads((SP / a.map / "summary.json").read_text())["rates"]
    fams = sorted({r["family"] for r in rates} & {"PP", "PM", "BL", "BR"})
    look, rec = ("PP", "PM") if "PP" in fams else ("BL", "BR")
    copy = {(r["family"], r["set"], r["layer"]): r["cf"]["flips"] for r in rates
            if r["set"] in ("bridge_word", "bind_bridge")}  # fmt: skip
    pushes = {}
    for run in a.d4:
        _, cells, _, _ = W.load_cells(run)
        pushes[run] = cells
    layers = sorted({k[2] for k in copy} | {k[2] for c in pushes.values() for k in c})
    head = ["layer", f"copy at word: {look}", f"copy at word: {rec}", f"copy at sentence: {look}"]
    head += [f"{run} lens 8x at word: {f}" for run in a.d4 for f in ("BL", "BR")]
    lines = [
        f"# layer_table: {a.map} vs {', '.join(a.d4)}",
        "",
        "| " + " | ".join(head) + " |",
        "|" + "---|" * len(head),
    ]

    def pct(v) -> str:
        return "-" if v is None else f"{100 * v[0]:.0f}%"

    for la in layers:
        row = [str(la), pct(copy.get((look, "bridge_word", la))), pct(copy.get((rec, "bridge_word", la))),
               pct(copy.get((look, "bind_bridge", la)))]  # fmt: skip
        for run in a.d4:
            for f in ("BL", "BR"):
                cell = pushes[run].get((f, "w", la, 8.0, "lens"))
                row.append(pct(W.cell_rate(cell)) if cell else "-")
        lines.append("| " + " | ".join(row) + " |")
    d = OUT / f"{a.map}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "table.md").write_text("\n".join(lines) + "\n")
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
