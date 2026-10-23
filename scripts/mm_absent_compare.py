"""mm_absent_compare (Zach, 2026-10-23, prereg amendment 10A): M->M under the knock-out with the bridge in the context
(the model's C1 run of record on full_v8 / full_v8_two) vs absent (its run on full_v8_mmabs), on the M->M items it gets
right unedited in both, by band. Accuracy % [95% CI over bridge entities] for paper10 and its rotation; "lost" is
unedited minus edited (100 minus the edited accuracy on these items). Descriptive. Writes
results/ablate_v2/mm_absent/PRESENT__ABSENT.json and prints a table.

python scripts/mm_absent_compare.py PRESENT_RUN ABSENT_RUN
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.c1_v2 import ci  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"


def rows(run: str) -> list[dict]:
    return [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]


def main(present: str, absent: str) -> None:
    rp, ra = rows(present), rows(absent)
    ok = lambda rs: {r["id"] for r in rs if r["family"] == "MM" and r["kind"] == "clean" and r["condition"] == "none" and r["correct"]}  # noqa: E731
    both = ok(rp) & ok(ra)
    bands = [b for b in dict.fromkeys(r["band"] for r in ra if r["condition"] != "none") if any(r["band"] == b for r in rp)]
    out = {"present": present, "absent": absent, "n_items": len(both), "bands": {}}
    print(f"M->M right unedited in both: {len(both)} items ({present} vs {absent})")
    for b in bands:
        cell = {}
        for cond in ("paper10", "paper10_rot"):
            for label, rs in (("present", rp), ("absent", ra)):
                sel = [r for r in rs if r["family"] == "MM" and r["kind"] == "clean" and r["band"] == b and r["condition"] == cond
                       and r["id"] in both]  # fmt: skip
                acc = 100 * sum(r["correct"] for r in sel) / len(sel) if sel else float("nan")
                lo, hi = ci(sel)
                cell[f"{cond}/{label}"] = {"acc": round(acc, 1), "ci": [round(100 * lo), round(100 * hi)], "n": len(sel)}
        out["bands"][b] = cell
        p, a = cell["paper10/present"], cell["paper10/absent"]
        pr, ar = cell["paper10_rot/present"], cell["paper10_rot/absent"]
        print(f"{b}: knock-out M->M accuracy present {p['acc']:.0f} [{p['ci'][0]}-{p['ci'][1]}] vs absent {a['acc']:.0f} "
              f"[{a['ci'][0]}-{a['ci'][1]}] (lost {100 - p['acc']:.0f} vs {100 - a['acc']:.0f}); rotated {pr['acc']:.0f} vs {ar['acc']:.0f}")  # fmt: skip
    (RES / "mm_absent").mkdir(exist_ok=True)
    (RES / "mm_absent" / f"{present}__{absent}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
