"""jswap_by_relation (Zach, 2026-10-24, amendment 34 B's per-relation prediction): a v2 J-swap run's transfer per
relation, on the memory finals pooled (M, A, N: the passage never states the bridge's attribute) with jswap.score
(items right unedited, donor - third, 95% bootstrap over bridges), per condition. Writes
results/jswap/by_relation/RUN.json.

python scripts/jswap_by_relation.py RUN --set jsuite_v2_test_chat
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.jswap import score  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main(run: str, set_name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data" / "tasks_v2" / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (ROOT / "results" / "jswap" / run / "rows.jsonl").read_text().splitlines()]
    mem = [{**r, "family": "MEM"} for r in rows if r["family"][1] in "MAN" and items[r["id"]].get("relation")]
    rels = sorted({items[r["id"]]["relation"] for r in mem})
    out = {"run": run, "set": set_name, "finals": "M A N pooled", "by_relation": {}}
    for rel in rels:
        s = score([r for r in mem if items[r["id"]]["relation"] == rel])
        out["by_relation"][rel] = s
        print(f"{rel:10s} " + "  ".join(f"{c} {s[f'MEM/{c}']['transfer']:+5.1f} {s[f'MEM/{c}']['ci']} (n {s[f'MEM/{c}']['n_third']})"
                                       for c in ("swap", "swap_rot", "swap_u") if f"MEM/{c}" in s))  # fmt: skip
    pos = sum(out["by_relation"][r]["MEM/swap"]["transfer"] > 0 for r in rels)
    out["swap_positive"] = f"{pos} of {len(rels)}"
    print(f"swap transfer > 0 in {pos} of {len(rels)} relations")
    (ROOT / "results" / "jswap" / "by_relation").mkdir(exist_ok=True)
    (ROOT / "results" / "jswap" / "by_relation" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", required=True)
    a = ap.parse_args()
    main(a.run, a.set)
