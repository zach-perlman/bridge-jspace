"""Dan's hand check, read back (Dan 29 Oct 11:45, verify_prep_1145 item 5): the verdict marks in review/marks.jsonl on
the fixed sample, per tier-1 view, beside the automatic checks (review/verify_checks.json) and the independent recount
(review/verify_independent.json). Shared by `make review-summary` (docs/review/review_summary.md) and `make review-verified`
(VERIFIED.md's generated section).

A mark counts if it has a verdict (consistent / wrong / unclear): the inspector panel's J-space notes ("kind": "jspace",
no verdict) are skipped. The last verdict per item counts. Stop rule (Dan): two items marked wrong in one view flag it.
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

from bridge_jspace.review import items as I

VERDICTS = ("consistent", "wrong", "unclear")
STOP_WRONG = 2
# the views verify_independent.py recounts (Dan: the conflict test and the routes shares)
INDEPENDENT = {"main_swap": "conflict:", "routes": "routes C2"}


def load_marks(path: Path) -> list[dict]:
    """The verdict rows of a marks file, in file order (J-space notes and rows without a verdict skipped)."""
    if not path.exists():
        return []
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    return [r for r in rows if r.get("kind", "verdict") != "jspace" and r.get("verdict") in VERDICTS]


def per_view(marks: list[dict], seed: int | None = None) -> dict[str, dict]:
    """Per tier-1 view: the last verdict per item of its fixed sample (marks on other items are counted apart)."""
    fs = I.spec().get("fixed_sample") or {}
    seed = fs.get("seed") if seed is None else seed
    out = {}
    for v in (v for v in I.spec()["views"] if v.get("tier") == 1):
        sample = [e["item"] for e in (fs.get("views") or {}).get(v["id"]) or []]
        last = {r["item"]: r for r in marks if r["view"] == v["id"] and r.get("seed") == seed}
        on = {i: last[i] for i in sample if i in last}
        c = collections.Counter(r["verdict"] for r in on.values())
        out[v["id"]] = {"order": v.get("order"), "title": v["title"], "sample": len(sample), "read": len(on),
                        "consistent": c["consistent"], "wrong": c["wrong"], "unclear": c["unclear"],
                        "flagged": c["wrong"] >= STOP_WRONG, "outside_sample": len(set(last) - set(sample)),
                        "notes": [r for r in on.values() if r["verdict"] != "consistent"]}  # fmt: skip
    return out


def auto_status(view_id: str, checks: dict | None, indep: dict | None) -> tuple[str, str]:
    """(automatic checks, independent recount) for a view, in words."""
    if not checks or view_id not in checks.get("views", {}):
        a = "not run (make verify-checks)"
    else:
        r = checks["views"][view_id]
        n = sum(x.get("n", 0) for x in r["models"].values())
        nf = sum(sum(x.get("item_fail", {}).values()) for x in r["models"].values())
        rf = sum(c["status"] == "fail" for x in r["models"].values() for c in x.get("run_checks", []))
        mm = len(r["recount"]["mismatch"])
        bits = (
            [f"{nf} per-item failures"] * bool(nf)
            + [f"{rf} run-check failures"] * bool(rf)
            + [f"{mm} recount mismatches"] * bool(mm)
        )
        a = (f"passed: {n} items, recount {r['recount']['match']} of {r['recount']['match'] + mm} match" if not bits
             else f"{'; '.join(bits)} ({n} items; recount {r['recount']['match']} match): see docs/review/verify_pack.md")  # fmt: skip
    prefix = INDEPENDENT.get(view_id)
    if prefix is None:
        b = "not in the independent recount (the brief's: conflict test, routes)"
    elif not indep:
        b = "not run (make verify-independent)"
    else:
        rows = [x for x in indep["rows"] if x["quantity"].startswith(prefix)]
        bad = [x for x in rows if x["status"] == "mismatch"]
        b = (f"matched: {len(rows)} of {len(rows)} numbers" if rows and not bad else
             f"{len(bad)} of {len(rows)} differ: " + "; ".join(f"{x['model']} {x['quantity']}" for x in bad[:3]))  # fmt: skip
    return a, b


def read_json(path: Path) -> dict | None:
    return json.loads(path.read_text()) if path.exists() else None
