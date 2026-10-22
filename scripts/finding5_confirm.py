"""finding5_confirm: the pre-registered confirmation of finding 5 on fresh scenes (Dan, 2026-10-22, before the runs).

Finding 5 (README slide 4): with the donor prompt's last two tokens copied into the original prompt, the answer goes to
the original's statement at the same place when the donor asks its 1st or 2nd statement (an order label), and to the
original's statement about the donor's entity from the 3rd on (the bridge's identity). That split was chosen after the
pooled pre-registered test; this run tests it as a rule fixed in advance.

Items: memory -> prompt, the donor's last two tokens copied at one layer (pointer_swap, source dissoc, group last),
split by the place k of the donor's asked statement. Per item: position = the answer is the original's statement at k;
identity = the original's statement about the donor's entity. Shares are over all patched items of the split.
  A  1st and 2nd (k = 1, 2 pooled): position - identity has its 95% lower bound > 0
  B  3rd-5th (k = 3, 4, 5 pooled): identity - position >= 0 (point) and its 95% lower bound >= -0.05
  verdict  confirms iff A and B; partly if one of them; fails if neither
  layer    --layer L, or with --layers the last of them where the donor's own digit ('value') has its Wilson upper bound
           < 0.10 (the fixed rule the other models' layers follow); decided before the split is read
Intervals: entity-cluster bootstrap (the original's queried entity resampled within its topic, 4,000 draws, seed 0).
Reported, not decisive: every k, per topic, named -> prompt.

uv run python scripts/finding5_confirm.py --run R (--layer L | --layers L1 L2 ...)
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import cluster_bootstrap, wilson

PS_RESULTS = pins.RESULTS_DIR / "pointer_swap"
OUT = pins.RESULTS_DIR / "finding5_confirm"
A_LO, B_POINT, B_LO, VALUE_UB = 0.0, 0.0, -0.05, 0.10
N_BOOT, SEED = 4000, 0


def diff(rows: list[dict], a: str, b: str) -> list[float]:
    """mean(1[role a] - 1[role b]) with its entity-cluster bootstrap interval (within topic)."""
    vals = [float(r["role"] == a) - float(r["role"] == b) for r in rows]
    return list(cluster_bootstrap(vals, [r["_entity"] for r in rows], [r["domain"] for r in rows], n_boot=N_BOOT,
                                  seed=SEED))  # fmt: skip


def judge(first2: list[float], rest: list[float]) -> dict:
    a = first2[1] > A_LO
    b = rest[0] >= B_POINT and rest[1] >= B_LO
    return {"A": a, "B": b, "verdict": "confirms" if a and b else "partly" if a or b else "fails"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--layer", type=int)
    g.add_argument("--layers", type=int, nargs="+")
    ap.add_argument("--family", default="RL")
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new verdict folder")
    a = ap.parse_args()
    from scripts import pointer_swap as PS

    m = json.loads((PS_RESULTS / a.run / "manifest.json").read_text())
    items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
    rows = [json.loads(x) for x in (PS_RESULTS / a.run / "outcomes.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["source"] == "dissoc" and r["group"] == "last"]
    for r in rows:
        it = items[r["name"]]
        r["_k"] = it["slots"]["position"] + 1  # 1-based place of the donor's asked statement
        r["_entity"] = f"{it['domain']}:{it['query']}"
    if a.layer is not None:
        layer, value_by_layer = a.layer, {}
    else:
        value_by_layer = {}
        for la in a.layers:
            sel = [r for r in rows if r["family"] == a.family and str(r["layer"]) == str(la)]
            value_by_layer[la] = list(wilson(sum(r["role"] == "value" for r in sel), len(sel)))
        ok = [la for la in a.layers if value_by_layer[la][2] < VALUE_UB]
        assert ok, f"no layer of {a.layers} before the donor's digit arrives"
        layer = max(ok)
    out: dict = {"run": a.run, "layer": layer, "value_by_layer": value_by_layer, "families": {}}
    for fam in sorted({r["family"] for r in rows}):
        sel = [r for r in rows if r["family"] == fam and str(r["layer"]) == str(layer)]
        first2 = [r for r in sel if r["_k"] <= 2]
        rest = [r for r in sel if r["_k"] >= 3]
        block = {"n": len(sel), "first2": {"n": len(first2), "position_minus_identity": diff(first2, "position", "identity")},
                 "rest": {"n": len(rest), "identity_minus_position": diff(rest, "identity", "position")},
                 "by_k": {k: dict(collections.Counter(r["role"] for r in sel if r["_k"] == k)) for k in range(1, 6)},
                 "by_topic": {}}  # fmt: skip
        for dom in sorted({r["domain"] for r in sel}):
            f2 = [r for r in first2 if r["domain"] == dom]
            rs = [r for r in rest if r["domain"] == dom]
            block["by_topic"][dom] = {"first2": [*diff(f2, "position", "identity"), len(f2)],
                                      "rest": [*diff(rs, "identity", "position"), len(rs)]}  # fmt: skip
        block.update(judge(block["first2"]["position_minus_identity"], block["rest"]["identity_minus_position"]))
        out["families"][fam] = block
    d = Path(a.out) / f"{a.run}_{time.strftime('%Y%m%d-%H%M%S')}"
    d.mkdir(parents=True)
    (d / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    lines = [f"# finding5_confirm / {a.run}, layer {layer}", ""]
    for fam, b in out["families"].items():
        f2, rs = b["first2"]["position_minus_identity"], b["rest"]["identity_minus_position"]
        tag = " (decisive)" if fam == a.family else " (reported)"
        lines += [f"**{fam}{tag}: {b['verdict']}** (A {b['A']}, B {b['B']}; n {b['n']})",
                  f"- 1st and 2nd: position - identity {100 * f2[0]:+.0f} [{100 * f2[1]:+.0f}, {100 * f2[2]:+.0f}] points (n {b['first2']['n']})",
                  f"- 3rd-5th: identity - position {100 * rs[0]:+.0f} [{100 * rs[1]:+.0f}, {100 * rs[2]:+.0f}] points (n {b['rest']['n']})",
                  f"- by k: {json.dumps(b['by_k'])}", ""]  # fmt: skip
    (d / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
