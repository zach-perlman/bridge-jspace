"""depth_verdict: Phase 1a's rule on an ablate_v2 depth run, partial or complete (Zach, 2026-10-20; rule fixed in the
breadth plan v2 before the run). C1 survives if every prompt-final family (BL = P->P, RL = M->P) loses <= 10 points
in every band and at whole depth under the knock-out, with each control (rotated removal, rotated dictionary) keeping
every family >= 90%. Memory-final families (BR, RR, countries) are shown for contrast. Also: for the countries, does
the protected set (the clean top-10 at the answer position) contain the bridge (rows' bridge_protected), and does the
knock-out's effect differ between the rows where it does and the rows where it doesn't?

python scripts/depth_verdict.py RUN [--method paper10]      (reads results/ablate_v2/RUN/rows.jsonl)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins

PROMPT_FINAL = ("BL", "RL")
MEMORY_FINAL = ("BR", "RR", "country-R", "country-B")
MAX_LOSS, MIN_CONTROL = 0.10, 0.90


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if not n:
        return (float("nan"), float("nan"))
    p = k / n
    centre, half = (
        (p + z * z / (2 * n)) / (1 + z * z / n),
        z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n),
    )
    return (centre - half, centre + half)


def bridges_of() -> dict[tuple[str, str], str]:
    """(family, id) -> the bridge entity, for the suite families and the countries (rows before 2026-10-20 evening do
    not carry it)."""
    from scripts import exp09_bind_recall as E
    from scripts import suite_v1 as S

    out = {}
    for fam in ("BL", "BR", "RL", "RR", "BLR", "BRL", "TYPO", "TRANS", "TBL", "TBR"):
        try:
            out.update({(fam, it["id"]): it["bridge"] for it in S.load(fam)})
        except FileNotFoundError:
            continue
    for i, it in enumerate(E.ITEM_SETS["bind_recall"][2]()):
        out[(f"country-{it['family']}", E.uid(it, i))] = it["bridge"]
    return out


def cluster_ci(rs: list[dict], bridge: dict, reps: int = 2000, seed: int = 0) -> tuple[float, float]:
    """95% bootstrap interval of accuracy resampling bridge entities (items sharing a bridge are not independent)."""
    by = collections.defaultdict(list)
    for r in rs:
        by[r.get("bridge") or bridge.get((r["family"], r["id"]), r["id"])].append(r["correct"])
    groups = list(by.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(reps):
        draw = [g for _ in groups for g in [groups[rng.randrange(len(groups))]]]
        stats.append(sum(sum(g) for g in draw) / sum(len(g) for g in draw))
    stats.sort()
    return stats[int(0.025 * reps)], stats[int(0.975 * reps) - 1]


def band_key(band: str) -> tuple[int, int]:
    a, b = band[1:].split("-")
    return (int(b) - int(a) > 20, int(a))  # sliding bands by start, whole depth last


def main(run: str, method: str, clustered: bool) -> None:
    rows = [json.loads(line) for line in (pins.RESULTS_DIR / "ablate_v2" / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean"]
    none = {(r["family"], r["id"]): r["correct"] for r in rows if r["condition"] == "none"}
    cell: dict = collections.defaultdict(list)
    for r in rows:
        if r["condition"] != "none":
            cell[(r["band"], r["family"], r["condition"])].append(r)
    bands = sorted({b for b, _, _ in cell}, key=band_key)
    fams = [f for f in PROMPT_FINAL + MEMORY_FINAL if any(k[1] == f for k in cell)]
    controls = (f"{method}_rot", f"{method}_rdict")
    bridge = bridges_of() if clustered else {}

    def acc(rs: list[dict]) -> float:
        return sum(r["correct"] for r in rs) / len(rs)

    def loss(rs: list[dict]) -> float:  # unedited minus edited, on the same items
        return sum(none[(r["family"], r["id"])] for r in rs) / len(rs) - acc(rs)

    print(f"# {run}: {method}, {len(none)} items, {len(bands)} bands with rows\n")
    ci = "bootstrap over bridge entities" if clustered else "Wilson, items independent"
    print(f"Accuracy (%) with the J-space removed [95% CI, {ci}]; loss = unedited - edited on the same items.\n")
    print("| band | " + " | ".join(fams) + " | controls' lowest |")
    print("|---" * (len(fams) + 2) + "|")
    verdict = {"prompt_final_max_loss": 0.0, "worst": None, "control_min": 1.0}
    for band in bands:
        cells = []
        for f in fams:
            rs = cell.get((band, f, method), [])
            if not rs:
                cells.append("-")
                continue
            lo, hi = cluster_ci(rs, bridge) if clustered else wilson(sum(r["correct"] for r in rs), len(rs))
            cells.append(f"{100 * acc(rs):.0f} [{100 * lo:.0f}-{100 * hi:.0f}] (-{100 * loss(rs):.0f})")
            if f in PROMPT_FINAL and loss(rs) > verdict["prompt_final_max_loss"]:
                verdict["prompt_final_max_loss"], verdict["worst"] = loss(rs), f"{f} at {band}"
        ctrl = [acc(cell[(band, f, c)]) for f in fams for c in controls if cell.get((band, f, c))]
        if ctrl:
            verdict["control_min"] = min(verdict["control_min"], min(ctrl))
        print(f"| {band} | " + " | ".join(cells) + (f" | {100 * min(ctrl):.0f} |" if ctrl else " | - |"))
    verdict["c1_survives"] = verdict["prompt_final_max_loss"] <= MAX_LOSS and verdict["control_min"] >= MIN_CONTROL
    print(f"\nRule (prompt-final loss <= {100 * MAX_LOSS:.0f} points everywhere; controls >= {100 * MIN_CONTROL:.0f}%): "
          f"{json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in verdict.items()})}")  # fmt: skip

    print("\n## Countries: is the bridge in the protected set (clean top-10 at the answer position)?\n")
    print("| band | family | n protected / n | accuracy if protected | accuracy if not |")
    print("|---|---|---|---|---|")
    for band in bands:
        for f in ("country-R", "country-B"):
            rs = cell.get((band, f, method), [])
            if not rs:
                continue
            yes, no = [r for r in rs if r.get("bridge_protected")], [r for r in rs if not r.get("bridge_protected")]
            print(f"| {band} | {f} | {len(yes)}/{len(rs)} | {f'{100 * acc(yes):.0f}' if yes else '-'} | "
                  f"{f'{100 * acc(no):.0f}' if no else '-'} |")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--method", default="paper10", choices=["paper10", "omp25"])
    ap.add_argument("--items-independent", action="store_true", help="Wilson intervals instead of the entity bootstrap")
    a = ap.parse_args()
    main(a.run, a.method, not a.items_independent)
