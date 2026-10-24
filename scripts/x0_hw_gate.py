"""x0_hw_gate (jobs/c3/x0_hw_gate_27b.yaml): does the new box reproduce a 23 Oct cell?

A parts run of one cell of d1_necessity_parts_27b_r2 (bridge_word:16, both readers), rerun on the new hardware, is
compared row by row with the 23 Oct rows: same item, set, layer, part, source and null flag. Gate (hardware addendum
v2): per-item agreement of the read's role (b / A / other) >= 97% over the rows whose arm draws no random tensor (the
whole change and its lens parts); the arms that draw random tensors (on CUDA in that code) are reported beside, not
gated. Exit code 3 on a failed gate, so the queue's dependent X0 jobs do not start. With --drift-floor F (the 122B,
Dan 24 Oct): agreement >= 0.97 is PASS; in [F, 0.97) DRIFT (exit 0: the dependent run goes ahead, every number of
it labelled 'hardware drift', the per-part disagreement reported); below F FAIL (exit 3).

  uv run python scripts/x0_hw_gate.py --new RUN [--ref d1_necessity_parts_27b_r2] [--cell bridge_word:16]
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of

PARTS_DIR = pins.RESULTS_DIR / "statement_positions"
OUT = pins.RESULTS_DIR / "x0_hw_gate"
# statement_positions.run_parts: these arms are deterministic given the model's activations
DETERMINISTIC = ("full", "lens2", "not_lens2", "jspace", "not_jspace", "jspace_wo_own", "not_jspace_matched")
MIN_AGREEMENT = 0.97
KEY = ("family", "name", "set", "layer", "part", "source", "null")


def rows_of(run: str, s: str, layer: int) -> dict[tuple, dict]:
    rows = [json.loads(line) for line in (PARTS_DIR / run / "outcomes.jsonl").read_text().splitlines()]
    return {tuple(r[k] for k in KEY): r for r in rows if r["set"] == s and r["layer"] == layer}


def status(agreement: float, rows: int, floor: float | None) -> str:
    """PASS (>= MIN_AGREEMENT), DRIFT (in [floor, MIN_AGREEMENT) when a floor is given) or FAIL."""
    if rows and agreement >= MIN_AGREEMENT:
        return "PASS"
    if rows and floor is not None and agreement >= floor:
        return "DRIFT"
    return "FAIL"


def compare(new: dict[tuple, dict], ref: dict[tuple, dict], floor: float | None = None) -> dict:
    shared = sorted(set(new) & set(ref))
    by: dict[str, list[int]] = collections.defaultdict(list)
    ld: dict[str, list[float]] = collections.defaultdict(list)
    for k in shared:
        r = dict(zip(KEY, k, strict=True))
        group = "gated" if r["part"] in DETERMINISTIC and not r["null"] else "random draws (reported)"
        same = int(new[k]["role"] == ref[k]["role"])
        for g in (group, f"part {r['part']}{' null' if r['null'] else ''}", f"reader {r['family']}"):
            by[g].append(same)
            ld[g].append(abs(new[k]["ld"] - ref[k]["ld"]))
    table = {g: {"rows": len(v), "agreement": round(sum(v) / len(v), 4), "median_abs_ld_diff": round(
        statistics.median(ld[g]), 3)} for g, v in sorted(by.items())}  # fmt: skip
    gated = table.get("gated", {"rows": 0, "agreement": 0.0})
    return {"shared_rows": len(shared), "only_new": len(set(new) - set(ref)), "only_ref": len(set(ref) - set(new)),
            "groups": table, "gate": {"rows": gated["rows"], "agreement": gated["agreement"], "min": MIN_AGREEMENT,
                                      "pass": gated["rows"] > 0 and gated["agreement"] >= MIN_AGREEMENT,
                                      "drift_floor": floor,
                                      "status": status(gated["agreement"], gated["rows"], floor)}}  # fmt: skip


def figure(run: str) -> Path:
    """Agreement per part (real and null rows), the gate's bar marked, in a new analysis-*-figures/ folder."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    res = json.loads((OUT / run / "verdict.json").read_text())
    parts = {g.removeprefix("part "): v for g, v in res["groups"].items() if g.startswith("part ")}
    names = sorted(parts, key=lambda p: (p.endswith(" null"), p))
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(names) + 1.4))
    gated = [p in DETERMINISTIC for p in names]
    ax.barh(range(len(names)), [parts[p]["agreement"] for p in names],
            color=["#6A3D9A" if g else "#a6a6a6" for g in gated])  # fmt: skip
    ax.set_yticks(range(len(names)), names, fontsize=8)
    ax.invert_yaxis()
    ax.axvline(MIN_AGREEMENT, color="red", lw=1, ls="--")
    ax.set_xlim(0.9, 1.0)
    ax.set_xlabel("share of rows whose read role matches the 23 Oct row")
    ax.set_title(f"Hardware gate {res['gate'].get('status', 'PASS' if res['gate']['pass'] else 'FAIL')}: "
                 f"{res['gate']['agreement']:.4f} over "
                 f"{res['gate']['rows']} gated rows (purple; grey = random draws, reported)", fontsize=9)  # fmt: skip
    fig.tight_layout()
    folder = OUT / run / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-figures"
    folder.mkdir()
    fig.savefig(folder / "agreement_by_part.png", dpi=150)
    plt.close(fig)
    print(folder / "agreement_by_part.png")
    return folder


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", required=True)
    ap.add_argument("--ref", default="d1_necessity_parts_27b_r2")
    ap.add_argument("--cell", default="bridge_word:16")
    ap.add_argument("--figures", action="store_true", help="the figure of an existing verdict of --new")
    ap.add_argument("--drift-floor", type=float, default=None, help="DRIFT (exit 0) between this and 0.97")
    a = ap.parse_args()
    if a.figures:
        figure(a.new)
        return 0
    s, la = a.cell.split(":")
    res = compare(rows_of(a.new, s, int(la)), rows_of(a.ref, s, int(la)), a.drift_floor)
    res = {"new": a.new, "ref": a.ref, "cell": a.cell, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "inputs": {r: sha256_of(PARTS_DIR / r / "outcomes.jsonl") for r in (a.new, a.ref)}, **res}  # fmt: skip
    out = OUT / a.new
    out.mkdir(parents=True, exist_ok=False)
    (out / "verdict.json").write_text(json.dumps(res, indent=2) + "\n")
    lines = [f"# Hardware gate: {a.new} vs {a.ref} at {a.cell}", "",
             f"Gate: {res['gate']['status']}: agreement {res['gate']['agreement']:.4f} over "
             f"{res['gate']['rows']} rows without random draws (bar {MIN_AGREEMENT}"
             f"{f'; drift floor {a.drift_floor}' if a.drift_floor is not None else ''}). Rows only in the new run: "
             f"{res['only_new']}; only in the reference: {res['only_ref']}.", "",
             "| group | rows | agreement | median abs ld diff |", "|---|---|---|---|",
             *(f"| {g} | {v['rows']} | {v['agreement']:.4f} | {v['median_abs_ld_diff']} |"
               for g, v in res["groups"].items())]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 3 if res["gate"]["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
