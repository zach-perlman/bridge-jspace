"""Calibration report for a tasks_v2 competence run (Zach, 2026-10-21): per word x domain x level, whole-question
accuracy, accuracy on the items whose every step the model answers alone, median answer margin, guess rate and the
mean chance baseline (chance_same_answer); P->M->P / M->M->P also by number style (their bin rules show the middle
number next to the answer).

python scripts/tasks_calib_report.py RUN [--words W ...] [--out OUT.md]
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import tasks_v2 as T


def main(run: str, words: list[str] | None, out: str | None) -> None:
    run_dir = pins.RESULTS_DIR / "tasks_v2" / run
    manifest = json.loads((run_dir / "manifest.json").read_text())
    items = {it["id"]: it for it in T.load(manifest["set"])}
    rows = [json.loads(line) for line in (run_dir / "items.jsonl").read_text().splitlines()]
    parts = collections.defaultdict(dict)
    margin = {}
    for r in rows:
        parts[r["id"]][r["part"]] = r["correct"]
        if r["part"] == "whole":
            margin[r["id"]] = r.get("margin")
    words = words or list(dict.fromkeys(it["word"] for it in items.values()))
    domains = list(dict.fromkeys(it["domain"] for it in items.values()))
    pct = lambda v: f"{100 * statistics.mean(v):.0f}" if v else "-"  # noqa: E731
    lines = [f"# {run} (set {manifest['set']})", "",
             "Cells: whole-question accuracy % / on items whose steps are all right alone % (n). "
             "Levels L0-L3 pooled per domain; per-level rows below.", ""]  # fmt: skip
    lines += ["| word | " + " | ".join(domains) + " | all |", "|---" * (len(domains) + 2) + "|"]
    for w in words:
        cells = []
        for d in [*domains, None]:
            sel = [i for i, it in items.items() if it["word"] == w and (d is None or it["domain"] == d) and i in parts]
            whole = [parts[i]["whole"] for i in sel]
            ok = [parts[i]["whole"] for i in sel if all(v for p, v in parts[i].items() if p.startswith("step"))]
            cells.append(f"{pct(whole)} / {pct(ok)} ({len(sel)})" if sel else "-")
        lines.append(f"| {w} | " + " | ".join(cells) + " |")
    lines += ["", "| word | level | whole % | steps-ok whole % | median margin | guess % | mean chance | n |",
              "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in words:
        for lv in sorted({it["level"] for it in items.values()}):
            sel = [i for i, it in items.items() if it["word"] == w and it["level"] == lv and i in parts]
            if not sel:
                continue
            ok = [parts[i]["whole"] for i in sel if all(v for p, v in parts[i].items() if p.startswith("step"))]
            guess = [parts[i]["guess"] for i in sel if "guess" in parts[i]]
            mg = [margin[i] for i in sel if margin.get(i) is not None]
            ch = [items[i].get("chance_same_answer", 0) for i in sel]
            lines.append(f"| {w} | L{lv} | {pct([parts[i]['whole'] for i in sel])} | {pct(ok)} | "
                         f"{statistics.median(mg):.2f} | {pct(guess)} | {statistics.mean(ch):.2f} | {len(sel)} |")  # fmt: skip
    for w in ("PMP", "MMP"):
        if w in words:
            by = {s: [parts[i]["whole"] for i, it in items.items() if it["word"] == w and it["numbers"] == s and i in parts]
                  for s in ("digits", "words")}  # fmt: skip
            lines.append(f"\n{w} by number style: digits {pct(by['digits'])}% (n={len(by['digits'])}), "
                         f"words {pct(by['words'])}% (n={len(by['words'])})")  # fmt: skip
    text = "\n".join(lines) + "\n"
    if out:
        Path(out).write_text(text)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--words", nargs="+", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    main(a.run, a.words, a.out)
