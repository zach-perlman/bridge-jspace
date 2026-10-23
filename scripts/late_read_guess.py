"""late_read_guess (23 Oct; CPU re-analysis of finished late-read runs): when the answer's sentence is hidden, what
does the model answer instead?

Finding 1's paradox: on Qwen3-32B, hiding the answer's sentence from the last tokens (the chat-template tokens after the
user's text) in every layer leaves 3% right, hiding it from every token after it (all layers) 10%: blocking more leaves
more right. Dan's hypothesis: under the second block the model guesses while excluding the digits it can still see in
the list.

Runs: each model's first scene set late-read run (the grid's late-read-v2 rows "draw 1 · last tokens' share"), memory
-> prompt items (family RL: five "The <thing>'s locker is <digit>." sentences, the asked one's digit is the answer).
Arms, as the grid's late_read_v2 picks them (scripts/cross_model_grid.py): the unedited prompt (all items); the answer's
sentence hidden from the last tokens ("final"; every attention layer on a hybrid, every layer otherwise); hidden from
every token after it ("after"; all layers in these runs); on a hybrid also the last tokens in all layers (not in the
grid: the same layers as "after"). Blocked arms: items right unedited, DeltaNet mode "value" (the grid's items).
Each answer (the top next token, decoded with the run's pinned tokenizer, whitespace stripped) is one of: hidden = the
hidden sentence's digit (= right; checked against the run's own `correct`), visible = another sentence's digit (still
in the list), outside = a digit in no sentence (0 counted apart too), non-digit = anything else.
P(right | outside the visible list) = hidden / (hidden + outside), Wilson 95%, against the exclusion chance: the mean of
1 / (digits not in the visible list, the hidden one included) over those answers, with 10 digits (0-9) and, since the
data draws digits 1-9 only, again with 0 left out (hidden / (hidden + outside - zeros) against 1 / (9 - visible)).
Visible share against a blind guess: the mean of visible / 10 (or / 9). Visible answers: their sentence's place minus the
hidden sentence's place (-1 = the sentence just before it).

Gate: the right share per blocked arm must round to the grid's late-read-v2 numbers (grid.csv control text), else
nothing is written. No decision rule: a descriptive table.

uv run python scripts/late_read_guess.py [--out DIR] [--grid GRID_CSV]
Writes <DIR>/<YYYYmmddTHHMMSSZ>/table.csv, table.md, summary.json (DIR: results/late_read_guess).
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import re
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.stats import wilson
from bridge_jspace.utils import git_state

KO = pins.RESULTS_DIR / "attn_knockout"
OUT = pins.RESULTS_DIR / "late_read_guess"
GRID = pins.RESULTS_DIR / "cross_model" / "20261023T121807Z" / "grid.csv"
GRID_SETTING, GRID_RULE = "draw 1 · last tokens' share", "late-read-v2"
FAMILY = "RL"
DIGITS = "0123456789"
CLASSES = ("hidden", "visible", "outside", "non-digit")
# the grid's model names -> the first scene set's late-read run
RUNS = {
    "Qwen3.6-27B": "d2_v4_late_read",
    "Qwen3.5-9B": "qwen35_9b_d2_v4_late_read_r2",
    "Olmo-Hybrid-7B": "olmo_hybrid_7b_d2_v4_late_read_v3",
    "Qwen3-32B": "qwen3_32b_d2_v4_late_read_v2_r2",
    "OLMo-3-7B-I": "olmo3_7b_instruct_d2_v4_late_read_v3",
    "Gemma 4 31B-it": "gemma4it_d2_v4_late_read_v3_r2",
}
ARM_TEXT = {
    "unedited": "nothing hidden (all items)",
    "last tokens": "hidden from the last tokens",
    "after": "hidden from every token after it",
    "last tokens, all layers": "hidden from the last tokens, all layers (not in the grid)",
}


def jl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def arms(rows: list[dict]) -> list[tuple[str, tuple[str, str, str], str]]:
    """(arm, (source, dest, layers), its layers in words), picked as cross_model_grid.late_read_v2 picks them."""
    labels = {(r["source"], r["dest"], r["layers"]) for r in rows}
    hybrid = ("lookup", "final", "attn") in labels
    lab = "attn" if hybrid else "all"
    after_lab = "attn" if ("lookup", "after", "attn") in labels else "all"
    words = {"attn": "every attention layer", "all": "all layers"}
    out = [("unedited", ("none", "-", "-"), "-"), ("last tokens", ("lookup", "final", lab), words[lab]),
           ("after", ("lookup", "after", after_lab), words[after_lab])]  # fmt: skip
    if hybrid and ("lookup", "final", "all") in labels:
        out.append(("last tokens, all layers", ("lookup", "final", "all"), words["all"]))
    return out


def classify(answer_text: str, hidden: str, visible: set[str]) -> str:
    """One answer token's class (CLASSES); its text with whitespace stripped."""
    s = answer_text.strip()
    if len(s) != 1 or s not in DIGITS:
        return "non-digit"
    return "hidden" if s == hidden else "visible" if s in visible else "outside"


def slot_digits(case: dict) -> list[str] | None:
    """Each sentence's digit in list order, from its token span; None unless each holds exactly one digit, the asked
    one holds the answer and the others the visible digits."""
    out = []
    for toks in case["statements"]:
        a, b = case["offsets"][toks[0]][0], case["offsets"][toks[-1]][1]
        ds = re.findall(r"\d", case["prompt"][a:b])
        if len(ds) != 1:
            return None
        out.append(ds[0])
    q = case["query_slot"]
    if out[q] != case["answer"] or sorted(out[:q] + out[q + 1 :]) != sorted(case["conf_answers"]):
        return None
    return out


def record(row: dict, case: dict, decode: Callable[[int], str], slots: list[str] | None) -> dict:
    text = decode(row["top"])
    cls = classify(text, case["answer"], set(case["conf_answers"]))
    digit = text.strip() if cls != "non-digit" else None
    offset = slots.index(digit) - case["query_slot"] if cls == "visible" and slots and digit in slots else None
    return {"id": row["id"], "cls": cls, "text": text, "digit": digit, "correct": bool(row["correct"]),
            "k_visible": len(set(case["conf_answers"])), "offset": offset}  # fmt: skip


def mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def rnd(x: tuple[float, ...]) -> list[float | None]:
    return [None if math.isnan(v) else round(v, 4) for v in x]  # wilson gives nan for n = 0


def places(recs: list[dict]) -> dict[str, int]:
    """Visible answers by their sentence's place minus the hidden one's, in order; 'unparsed' where unknown."""
    c = collections.Counter(r["offset"] for r in recs if r["cls"] == "visible")
    out = {f"{k:+d}": c[k] for k in sorted(k for k in c if k is not None)}
    return out | ({"unparsed": c[None]} if c[None] else {})


def cell(recs: list[dict]) -> dict[str, Any]:
    """The class counts and rates of one arm's answers (see the module docstring)."""
    n = len(recs)
    c = collections.Counter(r["cls"] for r in recs)
    zero = [r for r in recs if r["cls"] == "outside" and r["digit"] == "0"]
    out_all = [r for r in recs if r["cls"] in ("hidden", "outside")]
    out_19 = [r for r in out_all if not (r["cls"] == "outside" and r["digit"] == "0")]
    return {
        "n": n,
        "counts": {k: c[k] for k in CLASSES} | {"outside_zero": len(zero)},
        "right": rnd(wilson(c["hidden"], n)),
        "visible": rnd(wilson(c["visible"], n)),
        "visible_blind_0to9": mean([r["k_visible"] / 10 for r in recs]),
        "visible_blind_1to9": mean([r["k_visible"] / 9 for r in recs]),
        "n_outside": len(out_all),
        "right_given_outside": rnd(wilson(c["hidden"], len(out_all))),
        "chance_given_outside_0to9": mean([1 / (10 - r["k_visible"]) for r in out_all]),
        "n_outside_1to9": len(out_19),
        "right_given_outside_1to9": rnd(wilson(c["hidden"], len(out_19))),
        "chance_given_outside_1to9": mean([1 / (9 - r["k_visible"]) for r in out_19]),
        "digits_outside_list_per_item": dict(collections.Counter(10 - r["k_visible"] for r in recs)),
        "non_digit_answers": dict(collections.Counter(repr(r["text"]) for r in recs if r["cls"] == "non-digit")),
        "visible_by_place": places(recs),
        "hidden_vs_correct_mismatch": sum((r["cls"] == "hidden") != r["correct"] for r in recs),
    }


def analyse(rows: list[dict], cases: list[dict], decode: Callable[[int], str]) -> dict[str, Any]:
    """Every arm's cell on one run's rows (family RL, mode 'value' or unedited) and cases."""
    rows = [r for r in rows if r["family"] == FAMILY and (r["source"] == "none" or r.get("mode", "value") == "value")]
    by_id = {c["id"]: c for c in cases if c["family"] == FAMILY}
    slots = {i: slot_digits(c) for i, c in by_id.items()}
    ok = {r["id"] for r in rows if r["source"] == "none" and r["correct"]}
    out: dict[str, Any] = {"items": len(by_id), "right_unedited": len(ok),
                           "slots_unparsed": sum(v is None for v in slots.values()), "arms": {}}  # fmt: skip
    for arm, lab, layers in arms(rows):
        sel = [r for r in rows if (r["source"], r["dest"], r["layers"]) == lab and (arm == "unedited" or r["id"] in ok)]
        recs = [record(r, by_id[r["id"]], decode, slots[r["id"]]) for r in sel]
        out["arms"][arm] = {"label": list(lab), "layers": layers,
                            "items": "all items" if arm == "unedited" else "items right unedited", **cell(recs)}  # fmt: skip
    return out


def r100(x: float) -> int:
    """Percent as cross_model_grid.r100 rounds it."""
    return int(f"{100 * x:.0f}") + 0


GRID_RE = re.compile(
    r"hidden from the last tokens \([^)]*\): (\d+)% right; from every token after it \([^)]*\): (\d+)%"
)


def grid_numbers(grid_csv: Path) -> dict[str, tuple[int, int]]:
    """run -> (last tokens % right, after % right) from the grid's late-read-v2 draw 1 rows."""
    out = {}
    with open(grid_csv, newline="") as f:
        for row in csv.DictReader(f):
            m = GRID_RE.search(row["chance or control level"])
            if row["rule id"] == GRID_RULE and row["setting"] == GRID_SETTING and m:
                out[Path(row["result path"]).parent.name] = (int(m[1]), int(m[2]))
    return out


def grid_check(res: dict[str, Any], grid: tuple[int, int] | None) -> list[str]:
    if grid is None:
        return ["no late-read-v2 draw 1 row in the grid"]
    mine = tuple(r100(a["counts"]["hidden"] / a["n"]) for a in (res["arms"]["last tokens"], res["arms"]["after"]))
    return [] if mine == grid else [f"right % last tokens / after {mine} != grid {grid}"]


def tokenizer_decoder(manifest: dict, ids: set[int]) -> Callable[[int], str]:
    """Decode the given token ids with the run's pinned tokenizer (the local cache, else its files downloaded)."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(manifest["model"]["repo"], revision=manifest["model"]["revision"])
    table = {i: tok.decode([i]) for i in sorted(ids)}
    return table.__getitem__


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(x: list[float | None] | None) -> str:
    if not x or x[0] is None or x[1] is None or x[2] is None:
        return "-"
    return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}]"


def p0(x: float | None) -> str:
    return "-" if x is None else f"{100 * x:.0f}%"


CSV_COLS = ["model", "run", "arm", "layers", "items", "n", "hidden", "visible", "outside", "outside_zero", "non_digit",
            "right", "right_lo", "right_hi", "visible_share", "visible_lo", "visible_hi", "visible_blind_0to9",
            "visible_blind_1to9", "n_outside", "right_given_outside", "rgo_lo", "rgo_hi", "chance_given_outside_0to9",
            "n_outside_1to9", "right_given_outside_1to9", "rgo19_lo", "rgo19_hi", "chance_given_outside_1to9",
            "digits_outside_list_per_item", "visible_by_place", "non_digit_answers"]  # fmt: skip


def csv_rows(out: dict) -> list[list]:
    lines = []
    for model, r in out["runs"].items():
        for arm, a in r["arms"].items():
            k = a["counts"]
            lines.append([model, r["run"], arm, a["layers"], a["items"], a["n"], k["hidden"], k["visible"],
                          k["outside"], k["outside_zero"], k["non-digit"], *a["right"], *a["visible"],
                          a["visible_blind_0to9"], a["visible_blind_1to9"], a["n_outside"], *a["right_given_outside"],
                          a["chance_given_outside_0to9"], a["n_outside_1to9"], *a["right_given_outside_1to9"],
                          a["chance_given_outside_1to9"], json.dumps(a["digits_outside_list_per_item"]),
                          json.dumps(a["visible_by_place"]), json.dumps(a["non_digit_answers"], ensure_ascii=False)])  # fmt: skip
    return lines


def table_md(out: dict) -> str:
    g = out["git"]
    lines = [
        "# What the models answer when the answer's sentence is hidden",
        "",
        "Question: finding 1's paradox (Qwen3-32B: hiding the answer's sentence from the last tokens leaves 3% right, hiding it from every token after it 10%). Dan's hypothesis: under the second block the model guesses while excluding the digits it can still see in the list.",
        "",
        f"Runs: each model's first scene set late-read run (the grid's late-read-v2 rows \"draw 1\"), memory → prompt items: five sentences \"The <thing>'s locker is <digit>.\", the asked thing's digit is the answer, so four other digits stay visible in the list. Commit {g['sha'][:7]}{' (uncommitted changes in the tree)' if g['dirty'] else ''}, script scripts/late_read_guess.py; no seeds (deterministic re-analysis of the runs' rows).",
        "",
        "Each answer (the model's top next token after \"Answer: \", whitespace stripped) is one of: right = the hidden sentence's digit; visible = another sentence's digit; outside = a digit in no sentence (0 counted apart: the data draws digits 1 to 9 only); not a digit. Blocked rows: items right unedited (the grid's items); the unedited row: all items. Rates: Wilson 95%.",
        "",
        "\"Right among outside\" = right / (right + outside): how often the answer is the hidden digit when it is not a visible one. Its chance under exclusion (guessing uniformly among the digits not visible) is 1 / (digits not in the visible list, the hidden one included): every item here lists 4 visible digits, so 1/6 with 0 to 9 and 1/5 with 1 to 9 (the \"1-9\" column leaves the zeros out). A blind guess that does not exclude gives the same conditional chance; exclusion shows in the visible share, against a blind guess's 4/10 (0-9) or 4/9 (1-9).",
        "",
        f"Gate: the right share per blocked arm rounds to the grid's numbers ({out['grid']}): {'passed for every run' if out['checks']['grid_ok'] else out['checks']['errors']}. Every row's \"right\" class equals the run's own correct flag: {'yes' if out['checks']['hidden_equals_correct'] else 'no'}.",
        "",
        "| model | hidden | layers | n | right | visible | outside (of which 0) | not a digit | right among outside, 0-9 (n) | chance | right among outside, 1-9 (n) | chance |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]  # fmt: skip
    for model, r in out["runs"].items():
        for arm, a in r["arms"].items():
            k = a["counts"]
            lines.append(
                f"| {model} | {ARM_TEXT[arm]} | {a['layers']} | {a['n']} | {k['hidden']} ({pct(a['right'])}) | "
                f"{k['visible']} ({pct(a['visible'])}) | {k['outside']} ({k['outside_zero']}) | {k['non-digit']} | "
                f"{pct(a['right_given_outside'])} ({a['n_outside']}) | {p0(a['chance_given_outside_0to9'])} | "
                f"{pct(a['right_given_outside_1to9'])} ({a['n_outside_1to9']}) | {p0(a['chance_given_outside_1to9'])} |"
            )
    lines += ["", "Visible answers by their sentence's place relative to the hidden sentence (-1 = the sentence just before it), and the answers that are not a digit:", "",
              "| model | hidden | visible answers by place | not a digit |", "|---|---|---|---|"]  # fmt: skip
    for model, r in out["runs"].items():
        for arm, a in r["arms"].items():
            places = ", ".join(f"{k}: {v}" for k, v in a["visible_by_place"].items()) or "-"
            nd = ", ".join(f"{k} ×{v}" for k, v in a["non_digit_answers"].items()) or "-"
            lines.append(f"| {model} | {ARM_TEXT[arm]} | {places} | {nd} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(OUT), help="parent folder of the new table folder")
    ap.add_argument("--grid", default=str(GRID), help="the grid.csv whose late-read-v2 numbers gate the run")
    a = ap.parse_args()
    grid_csv = Path(a.grid).resolve()
    grid = grid_numbers(grid_csv)
    out: dict[str, Any] = {"written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "script": "scripts/late_read_guess.py", "git": git_state(),
                           "grid": str(grid_csv.relative_to(pins.REPO_ROOT) if grid_csv.is_relative_to(pins.REPO_ROOT)
                                       else grid_csv),
                           "family": FAMILY, "runs": {}}  # fmt: skip
    errors = []
    for model, run in RUNS.items():
        d = KO / run
        m = json.loads((d / "manifest.json").read_text())
        rows, cases = jl(d / "rows.jsonl"), jl(d / "cases.jsonl")
        decode = tokenizer_decoder(m, {r["top"] for r in rows if r["family"] == FAMILY})
        res = analyse(rows, cases, decode)
        errs = grid_check(res, grid.get(run))
        errors += [f"{model}: {e}" for e in errs]
        out["runs"][model] = {"run": run, "model_repo": m["model"]["repo"], "model_revision": m["model"]["revision"],
                              "rows_sha256": sha256(d / "rows.jsonl"), "cases_sha256": sha256(d / "cases.jsonl"),
                              "grid_right_pct_last_after": grid.get(run), **res}  # fmt: skip
        print(f"{model}: {run} decoded, grid check {'FAILED ' + '; '.join(errs) if errs else 'ok'}")
    mismatch = sum(a["hidden_vs_correct_mismatch"] for r in out["runs"].values() for a in r["arms"].values())
    out["checks"] = {"grid_ok": not errors, "errors": errors, "hidden_equals_correct": mismatch == 0}
    if errors or mismatch:
        print("checks failed, nothing written:", errors, f"hidden != correct on {mismatch} rows")
        return 1
    d = Path(a.out) / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    with open(d / "table.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLS)
        w.writerows(csv_rows(out))
    (d / "table.md").write_text(table_md(out))
    print("wrote", d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
