"""nn_ko89_read (Zach, 2026-10-30, prereg amendment 89 note 69): note 37 / 57's answer-direction battery at the description tokens only.

Run (scripts/queues/h200_n89c_1030.sh): {P}jsuite_v4_test_chat_ko69desc_cand2_v1 (v4 draw 4001, note 37's gate / band / batch / cand2,
--positions desc). Readings, as registered:
  D0 (gate): paper10's gap - paper10_rot's gap >= 10 points and paper10's gap CI lower end > paper10_rot's gap; else "not readable at
     the description" and nothing else is read.
  K-desc: note 37's rule, verbatim (nn_ko37_read.measures).  S1-desc, A1-desc: note 57's rules, verbatim (nn_ko57_read.main --run-dir).
  D1 / T1 are not run; the stored check nn_ko57_read prints compares with the all-position run and is not a reading.
Writes results/ablate_v2/nn_ko_read/{P}note69.json (+ note 57's json under nn_ko_read/note69_desc/).
python scripts/nn_ko89_read.py PREFIX
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts import nn_ko57_read as N  # noqa: E402

SET = "jsuite_v4_test_chat"
CONDS = K.CONDS + ("paper10_onlyA", "paper10_onlyA_rot", "paper10_onlyRperp", "paper10_onlyRperp_rot", "ansRe", "ansRe_rot")


def main(P: str) -> dict:
    run = f"{P}{SET}_ko69desc_cand2_v1"
    d = K.RES / "ablate_v2" / run
    tag = P or "27b_"
    out: dict = {"prefix": P, "run": run}
    if not (d / "rows.jsonl").exists():
        print(f"note 69 {tag}: {run} missing")
        return out
    items = {json.loads(l)["id"]: json.loads(l) for l in (K.DATA / SET / "items.jsonl").open()}
    acc = K.rows_of(run)
    m = K.measures(acc, items, lambda it: True, CONDS)
    cs = m["conditions"]
    out["measures"] = m
    lines = K.table(f"note 69 (description tokens only) {tag}", m)
    g, gr = cs["paper10"]["gap"], cs["paper10_rot"]["gap"]
    ci = cs["paper10"]["gap_ci"]
    d0 = (g - gr) >= 10 and ci is not None and ci[0] > gr
    out["D0"] = {"paper10_gap": g, "paper10_gap_ci": ci, "paper10_rot_gap": gr, "net": round(g - gr, 1), "met": d0}
    lines.append(f"reading note69 D0 {tag}: {'gate met' if d0 else 'not readable at the description'!r} | " + json.dumps(out["D0"]))
    lines.append("  MP loss per arm (beside): " + json.dumps({c: v["loss_MP"] for c, v in cs.items()}))
    if d0:
        out["K_desc"] = {"reading": m.get("reading"), **m.get("ratio", {})}
        lines.append(f"reading note69 K-desc {tag}: {m.get('reading')!r} | " + json.dumps(m.get("ratio", {})))
        od = K.RES / "ablate_v2" / "nn_ko_read" / "note69_desc"
        n57 = N.main(P, run_dir=d, out_dir=od, set_name=SET)
        R = n57.get("readings", {})
        for k in ("S1", "A1"):
            if k in R:
                out[f"{k}_desc"] = R[k]
                lines.append(f"reading note69 {k}-desc {tag}: {R[k]['label']!r}")
        out["matching"] = n57.get("matching")
    o = K.RES / "ablate_v2" / "nn_ko_read" / f"{P}note69.json"
    o.write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
