"""competence_full_report: what a model can do on a full tasks_v2 set, and what the experiments will use (Zach,
2026-10-21: competence on both models before steering and the knock-out). Per word: whole-question accuracy by level,
by format class and by domain; each step alone; C and O; the guess prompt; then the items each experiment draws:
the knock-out (tasks_v2.eligible: scenes right on every prompt of every word, chance < 0.5, all levels, both strata)
and steering (the same, items with counterfactuals, core stratum).

python scripts/competence_full_report.py RUN [--set full_v8]   (writes results/tasks_v2/RUN/report.md)
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

WORDS = ("PP", "PM", "MP", "MM", "CP", "CM", "PPP", "PPM", "PMP", "MPP", "MPM", "MMP")


def main(run: str, set_name: str) -> None:
    items = {it["id"]: it for it in T.load(set_name)}
    rows = [json.loads(line) for line in (pins.RESULTS_DIR / "tasks_v2" / run / "items.jsonl").read_text().splitlines()]
    parts: dict = collections.defaultdict(dict)
    for r in rows:
        parts[r["id"]][r["part"]] = r["correct"]
    pct = lambda v: f"{100 * statistics.mean(v):.0f}" if v else "-"  # noqa: E731

    def whole(sel) -> str:
        return pct([parts[i]["whole"] for i in sel if "whole" in parts[i]])

    words = [w for w in WORDS if any(it["word"] == w for it in items.values())]
    doms = list(dict.fromkeys(it["domain"] for it in items.values()))
    lines = [f"# {run} on {set_name}: whole-question accuracy %", "",
             "| word | n | L0 | L1 | L2 | L3 | text | structured | each step alone (all right) | C | O | guess right |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for w in words:
        sel = [i for i, it in items.items() if it["word"] == w and i in parts]
        by_lv = [whole([i for i in sel if items[i]["level"] == lv]) for lv in range(4)]
        by_cls = [whole([i for i in sel if T.format_class(items[i]) == c]) for c in ("text", "structured")]
        steps = pct([all(v for p, v in parts[i].items() if p.startswith("step")) for i in sel])
        extra = [pct([parts[i][p] for i in sel if p in parts[i]]) for p in ("cf", "off", "guess")]
        lines.append(f"| {w} | {len(sel)} | " + " | ".join(by_lv + by_cls + [steps] + extra) + " |")
    lines += ["", "## By domain (whole %)", "", "| word | " + " | ".join(doms) + " |", "|---" * (len(doms) + 1) + "|"]
    for w in words:
        cells = [
            whole([i for i, it in items.items() if it["word"] == w and it["domain"] == d and i in parts]) for d in doms
        ]
        lines.append(f"| {w} | " + " | ".join(cells) + " |")
    ko = T.eligible(set_name, run, list(words), 10**9, "all", strata=("core", "secondary"))
    st = [it for it in T.eligible(set_name, run, list(words), 10**9, "all") if "cf_context" in it]
    kc, sc = collections.Counter(it["word"] for it in ko), collections.Counter(it["word"] for it in st)
    kcls = collections.Counter((it["word"], T.format_class(it)) for it in ko)
    lines += ["", "## Items the experiments will use", "",
              "| word | knock-out (all domains) | of which text / structured | steering pool (counterfactual domains, core) |",
              "|---|---|---|---|"]  # fmt: skip
    for w in words:
        lines.append(f"| {w} | {kc[w]} | {kcls[(w, 'text')]} / {kcls[(w, 'structured')]} | {sc[w]} (40 used) |")
    lines.append(f"\nTotal: knock-out {len(ko)} items, steering pool {len(st)} items.")
    text = "\n".join(lines) + "\n"
    (pins.RESULTS_DIR / "tasks_v2" / run / "report.md").write_text(text)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", dest="set_name", default="full_v8")
    a = ap.parse_args()
    main(a.run, a.set_name)
