"""d2_parts (D2 follow-up; rule fixed 2026-10-22 before any run): what do the question's tokens and the last tokens
take from the answer's statement, the entity's name or its digit?

Background (UNVERIFIED; README slide 2): hiding the answer's statement from the question's tokens leaves 90-98% of
lookups right on Qwen3.6-27B and Gemma 4 but 61%, 32% and 14% on Qwen3.5-9B, Qwen3-32B and OLMo-3-7B, and the wrong
answers are then mostly off the list (Qwen3-32B 50%, OLMo 57%), not another statement's digit. Hypothesis (project
doc): on those models the question's tokens read the entity's NAME (to resolve the bridge from the candidates in the
list) while the last tokens read the DIGIT.

Run: attn_knockout on pointer_v4 with --sources lookup lookup_off lookup_name lookup_digit lookup_off_name
lookup_off_digit --dests question final --layers all: the whole statement, only its entity's name tokens, or only its
digit token is hidden from the destination tokens in every layer; the same for an off-path statement as the control.

Decision rule, per model, memory -> prompt (RL), topics pooled, items answered right unedited, Wilson 95% intervals:
  valid        the off-path controls (lookup_off_name, lookup_off_digit, at both destinations) keep >= 0.90 right
  question     testable iff the whole statement hidden from the question's tokens leaves <= 0.70 right; then
               H-name-q   right(name, question) <= right(statement, question) + 0.15 and right(digit, question) >= 0.85
               H-digit-q  right(digit, question) <= right(statement, question) + 0.15 and right(name, question) >= 0.85
               (neither: both parts matter, or the read is spread over the statement)
  last tokens  H-digit-final  right(digit, final) <= 0.35 and right(name, final) >= 0.70
               H-name-final   right(name, final) <= 0.35 and right(digit, final) >= 0.70
Reported, not decisive: the error type of every cell (another digit of the list vs off the list), named -> prompt,
memory -> memory, per topic.

uv run python scripts/d2_parts.py --name RUN
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import wilson

D2 = pins.RESULTS_DIR / "attn_knockout"
PARTS = ("lookup", "lookup_name", "lookup_digit", "lookup_off", "lookup_off_name", "lookup_off_digit")
CONTROL_MIN, Q_TESTABLE, SAME_MARGIN, PART_KEEP, BROKEN, KEPT = 0.90, 0.70, 0.15, 0.85, 0.35, 0.70


def outcome(r: dict, case: dict) -> str:
    """right / list (another digit of the list) / off (anything else), from the top token id."""
    if r["top"] == case["tok_A"]:
        return "right"
    return "list" if r["top"] in case["conf_toks"] else "off"


def cells(rows: list[dict], cases: dict[str, dict]) -> dict[tuple, dict]:
    """(family, source, dest) -> counts of right / list / off, layers all, items right unedited."""
    ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
    cnt: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        if (r["family"], r["id"]) in ok and r["source"] in PARTS and r["layers"] == "all":
            cnt[(r["family"], r["source"], r["dest"])][outcome(r, cases[r["id"]])] += 1
    out = {}
    for k, c in cnt.items():
        n = sum(c.values())
        out[k] = {"n": n, "right": wilson(c["right"], n), "list": c["list"] / n, "off": c["off"] / n}
    return out


def verdicts(cl: dict[tuple, dict], fam: str = "RL") -> dict:
    def right(src: str, dest: str) -> float:
        return cl[(fam, src, dest)]["right"][0]

    valid = all(
        right(s, d) >= CONTROL_MIN for s in ("lookup_off_name", "lookup_off_digit") for d in ("question", "final")
    )
    testable = right("lookup", "question") <= Q_TESTABLE
    whole_q = right("lookup", "question")
    return {
        "valid": valid,
        "question_testable": testable,
        "H-name-q": testable
        and right("lookup_name", "question") <= whole_q + SAME_MARGIN
        and right("lookup_digit", "question") >= PART_KEEP,
        "H-digit-q": testable
        and right("lookup_digit", "question") <= whole_q + SAME_MARGIN
        and right("lookup_name", "question") >= PART_KEEP,
        "H-digit-final": right("lookup_digit", "final") <= BROKEN and right("lookup_name", "final") >= KEPT,
        "H-name-final": right("lookup_name", "final") <= BROKEN and right("lookup_digit", "final") >= KEPT,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    d = D2 / a.name
    cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
    rows = [json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()]
    cl = cells(rows, cases)
    fams = sorted({k[0] for k in cl})
    out = {"run": a.name, "cells": {"|".join(k): v for k, v in sorted(cl.items())},
           "verdicts": {f: verdicts(cl, f) for f in fams if all((f, s, dd) in cl for s in PARTS
                                                                  for dd in ("question", "final"))}}  # fmt: skip
    (d / "parts_summary.json").write_text(json.dumps(out, indent=1))
    lines = [f"# d2_parts / {a.name}", "", "| family | hidden | from | n | right [95%] | another list digit | off the list |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for (f, s, dd), v in sorted(cl.items()):
        p, lo, hi = v["right"]
        lines.append(f"| {f} | {s} | {dd} | {v['n']} | {100 * p:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}] | "
                     f"{100 * v['list']:.0f}% | {100 * v['off']:.0f}% |")  # fmt: skip
    lines += ["", "Verdicts: " + json.dumps(out["verdicts"])]
    (d / "parts_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
