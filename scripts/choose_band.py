"""choose_band: each model's middle band for C1, by the procedure that picked the 27B's 32-40 (Zach, 2026-10-21,
decided with Zach before any non-27B tasks_v2 knock-out ran). On the model's suite depth sweep (ablate_v2, paper10 and
paper10_rot, BL BR RL RR whole questions, windows 9/64 of the depth wide sliding by 4/64): the window where the
memory-final families (BR, RR) are most broken under paper10 (lowest mean accuracy), among windows whose rotated
control keeps every family >= 90%; ties go to the earlier window. Lookup families (BL, RL) play no part in the choice,
and the suite is not the tasks_v2 test set, so the C1 test on full_v8 is not biased by it.

python scripts/choose_band.py SWEEP_RUN   (prints the band as "lo-hi"; writes results/ablate_v2/band_choice/SWEEP_RUN.json)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins

RES = pins.RESULTS_DIR / "ablate_v2"
MEMORY_FINAL, ALL = ("BR", "RR"), ("BL", "BR", "RL", "RR")
CONTROL_MIN = 0.90


def choose(cells: dict) -> tuple[str | None, list[dict]]:
    table = []
    widths = [int(b.split("-")[1]) - int(b.removeprefix("L").split("-")[0]) + 1 for b in cells]
    window = max(set(widths), key=widths.count)  # the sweep's window width; the whole-depth band is not a candidate
    for band, fams in cells.items():
        if int(band.split("-")[1]) - int(band.removeprefix("L").split("-")[0]) + 1 != window:
            continue

        def acc(f: str, cond: str, fams: dict = fams) -> float | None:
            return (fams.get(f"{f}/clean", {}).get(cond) or {}).get("accuracy")

        mem = [acc(f, "paper10") for f in MEMORY_FINAL]
        ctrl = [acc(f, "paper10_rot") for f in ALL]
        if any(v is None for v in mem + ctrl):
            continue
        lo = int(band.removeprefix("L").split("-")[0])
        table.append({"band": band, "start": lo, "memory_final_acc": sum(mem) / len(mem), "control_min": min(ctrl),
                      "eligible": min(ctrl) >= CONTROL_MIN})  # fmt: skip
    ok = [r for r in table if r["eligible"]]
    best = min(ok, key=lambda r: (r["memory_final_acc"], r["start"])) if ok else None
    return (best["band"].removeprefix("L") if best else None), sorted(table, key=lambda r: r["start"])


def main(run: str) -> None:
    summary = json.loads((RES / run / "summary.json").read_text())
    cells = {b: c for b, c in summary["cells"].items() if b.count("-") == 1}
    band, table = choose(cells)
    out = {"sweep": run, "band": band, "rule": __doc__.split("\n\n")[0], "table": table}
    (RES / "band_choice").mkdir(exist_ok=True)
    (RES / "band_choice" / f"{run}.json").write_text(json.dumps(out, indent=2) + "\n")
    for r in table:
        print(f"# {r['band']}: memory-final {100 * r['memory_final_acc']:.0f}%, control min {100 * r['control_min']:.0f}%",
              file=sys.stderr)  # fmt: skip
    if band is None:
        sys.exit("no window passes the control check")
    print(band)


if __name__ == "__main__":
    main(sys.argv[1])
