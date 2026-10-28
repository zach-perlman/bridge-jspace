"""jswap_xrel_v3ctx (Zach, 2026-10-28, prereg amendment 58 note 5, item 6): on a v3 cross-context swap run, how often the
answer is the donor's value *in the donor passage* rather than its value in this prompt's relation (CPU).

For an item asking the entity's own attribute (finals K M A N), swap_xrel's donor passage is a made-up-fact passage
(P final) that gives D a made-up value of the same answer words; for a made-up-fact item (PP), swap_xrel's donor passage
states D's true value. Per word and pooled over the memory finals (PM PA PN TM): the share of answers that are D's
value here (`donor`, the run's class) and D's value in the donor passage (`donor_ctx`, when the two differ), for
swap_srel, swap_xrel and their controls.

python scripts/jswap_xrel_v3ctx.py RUN [--set jsuite_v3_test_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

MEMORY = ("PM", "PA", "PN", "TM")


def main(run: str, set_name: str) -> None:
    from transformers import AutoTokenizer

    from scripts import jswap as JS

    d = ROOT / "results" / "jswap" / run
    man = json.loads((d / "manifest.json").read_text())
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data" / "tasks_v2" / set_name / "items.jsonl").open()}
    from bridge_jspace import pins

    pin = pins.model_pin()
    tok = AutoTokenizer.from_pretrained(pin["repo"], revision=pin["revision"])
    assert pins.TARGET == man["target"], (pins.TARGET, man["target"])
    rows = [json.loads(line) for line in (d / "rows.jsonl").open()]

    def value_in(pid: str, e: str) -> str | None:
        it = items[pid]
        t = JS.table(it)
        if it["final"] == "P":
            return JS.pfact_value(t["pfact"][it["wording"]], it["context"], e, it["answer_vocab"], the=True)
        return t["facts"][e][0]

    right = {r["id"] for r in rows if r["condition"] == "none" and r["cls"] == "kept"}  # as jswap.score: items right unedited
    cells = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        if "xsrc" not in r or r["id"] not in right:
            continue
        it = items[r["id"]]
        src = r["ssrc"] if r["condition"] == "swap_srel" else r["xsrc"]
        v = value_in(src, r["donor"])
        ctx = v is not None and v != r["ad"] and r["pick"] in JS.forms(tok, v, it["kind"])
        for f in (r["family"], "memory") if r["family"] in MEMORY else (r["family"],):
            c = cells[(f, r["condition"])]
            c["n"] += 1
            c[r["cls"]] += 1
            c["donor_ctx"] += ctx
            c["ctx_differs"] += v is not None and v != r["ad"]
    out = {f"{f}/{c}": {k: (round(100 * v / n["n"], 1) if k != "n" else v) for k, v in n.items()} for (f, c), n in sorted(cells.items())}
    (d / "v3ctx.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out.items():
        if k.split("/")[0] in ("memory", "PP", "PK"):
            print(f"{k:26s} n {v['n']:4d}  kept {v.get('kept', 0):5.1f}  donor {v.get('donor', 0):5.1f}  donor_ctx {v['donor_ctx']:5.1f}"
                  f"  (ctx value differs on {v['ctx_differs']:5.1f}%)  other {v.get('other', 0):5.1f}")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    a = ap.parse_args()
    main(a.run, a.set)
