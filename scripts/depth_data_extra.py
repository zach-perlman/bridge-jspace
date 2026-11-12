"""Add to data/figures/depth/data.csv the card numbers the depth README quotes whose rows its old builders never wrote:
the answer-arm check's shift beyond K random directions (one run per model) and the made-up-fact passages' F4 / F4b
splits, and the two bridge words' share of 52 A's rebuilt energy with its interval. Each row is read by key from its
run file; a row already present is checked, not rewritten (a different value
stops the script), so a second run changes nothing.

uv run python scripts/depth_data_extra.py
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "figures" / "depth" / "data.csv"
FIELDS = ["figure", "model", "quantity", "value", "lo", "hi", "n", "source"]
KRAND = "answer arms: recall, the all-language shift beyond the same count of random directions (b_beyond_K_random)"
# the run each model's README value comes from (the 27B's is the rerun with batch 8)
KRAND_RUNS = {"qwen3.5-9b": "runs/answer_arms_krand/qwen3.5-9b/krand/summary.json",
              "qwen3.6-27b": "runs/answer_arms_krand/qwen3.6-27b/krand_b8/summary.json",
              "muse-glimmer-30b": "runs/answer_arms_krand/muse-glimmer-30b/krand/summary.json"}  # fmt: skip
KRAND_FIRST_27B = "runs/answer_arms_krand/qwen3.6-27b/krand/summary.json"
Z1P = "results/z1p_checks/20261030T222158Z/tables.json"
# (table key, path inside it, the row's quantity); n is read from the path's parent
Z1P_ROWS = (
    ("F4", ("without", "lookup_excess"), "made-up facts F4, without the 23 passages: lookup, switches lost beyond a random part"),
    ("F4", ("without", "recall_excess"), "made-up facts F4, without the 23 passages: recall, switches lost beyond a random part"),
    ("F4", ("without", "gap"), "made-up facts F4, without the 23 passages: the gap"),
    ("F4b", ("without_those_items", "lookup_excess"), "made-up facts F4b, without the 54 items: lookup, switches lost beyond a random part"),
    ("F4b", ("without_those_items", "recall_excess"), "made-up facts F4b, without the 54 items: recall, switches lost beyond a random part"),
    ("F4b", ("without_those_items", "gap"), "made-up facts F4b, without the 54 items: the gap"),
)  # fmt: skip


# x52_atoms part A, E1 lookup view: the old and the new bridge word's shares of the rebuilt energy together, with the
# reader's own 95% cluster bootstrap over bridge entities (x52_atoms.per_item, x0_necessity.resampled_rates, its seed);
# the single classes reproduce each report's tables.json (Dan, 12 Nov: the README's 05_atoms caption cites them)
ATOMS_BOTH = "52 A: share of the rebuilt energy, both bridge words (old and new), 95% interval over bridge entities"
ATOMS_REPORTS = {"qwen3.5-9b": "report-20261029T000125Z", "qwen3.6-27b": "report-20261029T000125Z",
                 "muse-glimmer-30b": "report-20261029T000125Z", "nemotron-3.5-lightning": "report-20261029T010648Z",
                 "qwen3.5-122b-a10b": "report-20261030T094628Z"}  # fmt: skip


def atoms_rows() -> list[dict]:
    sys.path[:0] = [str(REPO), str(REPO / "src")]
    from scripts import x0_necessity as X
    from scripts import x52_atoms as A

    out = []
    for model, rep in ATOMS_REPORTS.items():
        path = f"results/x52_atoms/{rep}/labelled.jsonl"
        recs = [r for r in map(json.loads, (REPO / path).open())
                if r["target"] == model and r["set"] == "e1" and r["view"] == "PP"]  # fmt: skip
        stored = json.loads((REPO / path).with_name("tables.json").read_text())["summary"][model]["e1"]["PP"]
        assert A.summarise(recs)["energy"]["bridge"] == stored["energy"]["bridge"], model  # the reader's numbers
        both = {"both": [v["energy"]["bridge"] + v["energy"]["new_bridge"] for v in map(A.per_item, recs)]}
        lo, hi = X.interval(X.resampled_rates(both, [r["entity"] for r in recs], X.N_BOOT, X.BOOT_SEED)["both"])
        out.append({"figure": "fig18_atoms", "model": model, "quantity": ATOMS_BOTH,
                    "value": round(sum(both["both"]) / len(recs), 4), "lo": round(lo, 4), "hi": round(hi, 4),
                    "n": len(recs), "source": f"{path} (scripts/depth_data_extra.py atoms_rows)"})  # fmt: skip
    return out


def rows() -> list[dict]:
    out = atoms_rows()
    for model, path in KRAND_RUNS.items():
        rec = json.loads((REPO / path).read_text())["readers"]["recall"]
        v, lo, hi = rec["b_beyond_K_random"]
        out.append({"figure": "cards", "model": model, "quantity": KRAND, "value": v, "lo": lo, "hi": hi,
                    "n": rec["n"], "source": path})  # fmt: skip
    # the 27B's first run (14 rows per batch) missed the arms check's count gate and was rerun as krand_b8; the card
    # names both, so its value is a row too
    rec = json.loads((REPO / KRAND_FIRST_27B).read_text())["readers"]["recall"]
    v, lo, hi = rec["b_beyond_K_random"]
    out.append({"figure": "cards", "model": "qwen3.6-27b", "quantity": KRAND + ", first run (14 rows per batch; "
                "missed the count gate, rerun as krand_b8)", "value": v, "lo": lo, "hi": hi, "n": rec["n"],
                "source": KRAND_FIRST_27B})  # fmt: skip
    tables = json.loads((REPO / Z1P).read_text())
    model = json.loads((REPO / Z1P).with_name("manifest.json").read_text())["model"]
    for key, (part, field), quantity in Z1P_ROWS:
        block = tables[key][part]
        v, lo, hi = block[field]
        out.append({"figure": "cards", "model": model, "quantity": quantity, "value": v, "lo": lo, "hi": hi,
                    "n": block["n"], "source": f"{Z1P} | {key}"})  # fmt: skip
    return out


def main() -> int:
    with DATA.open(newline="") as f:  # keep the file's own line endings (csv's default \r\n)
        text = f.read()
    eol = "\r\n" if "\r\n" in text else "\n"
    have = {(r["figure"], r["model"], r["quantity"]): r for r in csv.DictReader(io.StringIO(text))}
    new = []
    for r in rows():
        old = have.get((r["figure"], r["model"], r["quantity"]))
        if old is None:
            new.append(r)
        elif any(str(old[k]) != str(r[k]) for k in ("value", "lo", "hi", "n", "source")):
            print(f"data.csv row differs from its source: {old} vs {r}", file=sys.stderr)
            return 1
    if new:
        buf = io.StringIO()
        csv.DictWriter(buf, fieldnames=FIELDS, lineterminator=eol).writerows(new)
        with DATA.open("w", newline="") as f:
            f.write(text + buf.getvalue())
    print(f"data/figures/depth/data.csv: {len(new)} rows added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
