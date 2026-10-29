"""x52_cpu_checks (Dan, 29 Oct ~09:05, CPU; descriptive, after the data, no rule; UNVERIFIED): two reads of stored runs,
like x52_write2x.

  lenswrite  51.10's writes at the last token (P3), at each model's recall read peak: what the model outputs per arm
             (the lens swap, the J++ part at gain 1 / 2, the whole-state patch, the random controls). Classes of the top
             token: original (O's answer), new (S's answer), digit (another digit), entity (the start of the original or
             the new bridge entity's name), number_word (a number word), other. From results/x51_jread/<run>/outcomes.jsonl.
  swaprecall The address swap at s = 2 (x8_write): when the recall's answer changes, what to: the swapped-in item's
             answer (the legs of slot k's item), the third item's answer, another digit, or a non-answer. 9B and
             Lightning. The scenes are rebuilt on CPU from x6_routes.scenes (the tokenizer only) and matched by scene id.

Writes results/x51_jread/x52_lenswrite-<UTC>/ and results/x8_write/x52_swaprecall-<UTC>/ (md + json)."""

from __future__ import annotations

import argparse
import collections
import json
import time
from pathlib import Path

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts.x52_atoms import tokenizer_of

JREAD = {"qwen3.5-9b": "qwen35_9b_x51_10", "qwen3.6-27b": "x51_10_27b", "muse-glimmer-30b": "muse30_x51_10",
         "nemotron-3.5-lightning": "nem35l_x52_jread"}  # fmt: skip
WRITE = {"qwen3.5-9b": "qwen35_9b_x8_write", "nemotron-3.5-lightning": "nem35l_x52_write"}
LENS_ARMS = ("none", "swap", "swap_rand", "jpp1", "rand1", "jpp2", "rand2", "whole")
LENS_CLASSES = ("original", "new", "digit", "entity", "number_word", "other")
SWAP_CLASSES = ("unchanged", "swapped_in", "third", "digit", "non_answer")
NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"}
N_TOP = 5


def lens_class(row: dict, word: str, names: tuple[str, ...]) -> str:
    """The class of one 51.10 outcome row's top token (decoded as `word`); `names`: the original and new entities."""
    if row["role"] == "A":
        return "original"
    if row["role"] == "b":
        return "new"
    w = word.strip().lower()
    if w.isdigit():
        return "digit"
    if len(w) >= 2 and any(n.lower().startswith(w) for n in names):
        return "entity"
    return "number_word" if w in NUMBER_WORDS else "other"


def swap_class(row: dict, tok_id, legs: list[int]) -> str:
    """The class of one recall row under a swap: `legs` per slot, `tok_id(d)` a digit's token; j / k from the row."""
    if not row["changed"]:
        return "unchanged"
    third = next(s for s in range(len(legs)) if s not in (row["j"], row["k"]))
    if row["top"] == tok_id(legs[row["k"]]):
        return "swapped_in"
    if row["top"] == tok_id(legs[third]):
        return "third"
    return "digit" if row["top"] in {tok_id(d) for d in range(10)} else "non_answer"


def shares(classes: list[str], order: tuple[str, ...]) -> dict:
    n = len(classes)
    return {"n": n, **{c: round(classes.count(c) / n, 3) if n else None for c in order}}


def stage_lenswrite() -> Path:
    out = pins.RESULTS_DIR / "x51_jread" / f"x52_lenswrite-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    blob: dict = {"exp": "x52_cpu_checks/lenswrite", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "code": pins.git_state(), "classes": LENS_CLASSES, "models": {}}  # fmt: skip
    for target, run in JREAD.items():
        src = pins.RESULTS_DIR / "x51_jread" / run
        peak = json.loads((src / "peak.json").read_text())["peaks"]
        cf = {c["scene"]: c.get("cf_bridge", "") for c in X.read_jsonl(src / "cases.jsonl")}
        tok = tokenizer_of(target)
        rows = X.read_jsonl(src / "outcomes.jsonl")
        m: dict = {"run": f"results/x51_jread/{run}", "peaks": peak, "cells": {}}
        for reader, w in (("recall", "PM"), ("lookup", "PP")):
            for arm in LENS_ARMS:
                sel = [r for r in rows if r["reader"] == w and r["arm"] == arm
                       and (arm == "none" or (r["pos"] == "P3" and r["layer"] == peak[reader]))]  # fmt: skip
                words = [tok.decode([r["top"]]) for r in sel]
                cls = [lens_class(r, wd, (r["entity"], cf.get(r["scene"], ""))) for r, wd in zip(sel, words, strict=True)]
                tops = collections.Counter(wd for wd, c in zip(words, cls, strict=True) if c not in ("original", "new"))
                m["cells"][f"{reader}|{arm}"] = {**shares(cls, LENS_CLASSES), "top_other": tops.most_common(N_TOP)}
        blob["models"][target] = m
    out.mkdir(parents=True)
    (out / "lenswrite.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = ["# 51.10's writes at the last token: what the model outputs (descriptive; UNVERIFIED)", "",
             "Dan, 29 Oct ~09:05 (CPU). Main-test locker-first items of each 51.10 run; the write at P3 (the appended last "
             "token) at the reader's read peak; 'none' = unedited. Classes of the top token (full vocabulary): original = "
             "O's answer, new = S's answer, digit = another digit, entity = the start of the original or new bridge "
             "entity's name, number_word, other. Arms: swap = his swap through the lens; jpp1 / jpp2 = the J++ part of the "
             "change at gain 1 / 2; whole = the whole-state patch; *_rand / rand* = the random controls.", ""]  # fmt: skip
    for target, m in blob["models"].items():
        lines += [f"## {target} ({m['run']}; peaks {m['peaks']})", "",
                  "| reader | arm | n | " + " | ".join(LENS_CLASSES) + " | top non-answer tokens |",
                  "|" + "---|" * (4 + len(LENS_CLASSES))]  # fmt: skip
        for key, c in m["cells"].items():
            reader, arm = key.split("|")
            tops = ", ".join(f"{t!r} {k}" for t, k in c["top_other"])
            lines.append(f"| {reader} | {arm} | {c['n']} | " + " | ".join(f"{c[k]:.2f}" for k in LENS_CLASSES) + f" | {tops} |")
        lines.append("")
    (out / "lenswrite.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def stage_swaprecall() -> Path:
    from scripts import x6_routes as R
    from scripts import x8_write as W

    out = pins.RESULTS_DIR / "x8_write" / f"x52_swaprecall-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    blob: dict = {"exp": "x52_cpu_checks/swaprecall", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "code": pins.git_state(), "classes": SWAP_CLASSES, "models": {}}  # fmt: skip
    for target, run in WRITE.items():
        tok = tokenizer_of(target)
        legs_of, _, _ = R.pools(tok)
        cases = {c["scene"]: c for c in R.scenes(tok, R.N_GEN)[0] if c["condition"] == "C2"}

        def tok_id(d: int, tok=tok) -> int:
            return tok.encode(str(d), add_special_tokens=False)[0]

        rows = [r for r in X.read_jsonl(pins.RESULTS_DIR / "x8_write" / run / "outcomes.jsonl") if r["reader"] == "PM"]
        checked = 0
        cells: dict = {}
        for kind in ("write", "random"):
            for s in sorted({r["s"] for r in rows if r["kind"] == kind}):
                cls = []
                for r in (r for r in rows if r["kind"] == kind and r["s"] == s):
                    c = cases[r["scene"]]
                    assert c["bridge"] == r["entity"], (r["scene"], c["bridge"], r["entity"])
                    legs = [legs_of[item] for item, _ in W.slots_of(c["context"])]
                    assert legs[r["j"]] == int(c["readers"]["PM"]["answer"]), (r["scene"], legs, r["j"])
                    checked += 1
                    cls.append(swap_class(r, tok_id, legs))
                changed = [c for c in cls if c != "unchanged"]
                cells[f"{kind}|{s}"] = {"all": shares(cls, SWAP_CLASSES),
                                        "of_changed": shares(changed, SWAP_CLASSES[1:])}  # fmt: skip
        blob["models"][target] = {"run": f"results/x8_write/{run}", "rows_checked": checked, "cells": cells}
    out.mkdir(parents=True)
    (out / "swaprecall.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = ["# The address swap: when the recall changes, what to (descriptive; UNVERIFIED)", "",
             "Dan, 29 Oct ~09:05 (CPU). x8_write's recall rows (the swap s (mu_k - mu_j) at the bridge word at L; random = "
             "a random vector of the same norm). Scenes rebuilt on CPU (x6_routes.scenes, matched by scene id; every row's "
             "bridge and original answer checked). Of the changed recalls: swapped_in = the legs of slot k's item (the "
             "item the swap points to), third = the third item's legs, digit = another digit, non_answer = anything else. "
             "Items with equal legs make classes overlap (swapped_in is checked first).", ""]  # fmt: skip
    for target, m in blob["models"].items():
        lines += [f"## {target} ({m['run']}; {m['rows_checked']} rows checked)", "",
                  "| arm | s | n | changed | of changed: n | " + " | ".join(SWAP_CLASSES[1:]) + " |",
                  "|" + "---|" * (5 + len(SWAP_CLASSES) - 1)]  # fmt: skip
        for key, c in m["cells"].items():
            kind, s = key.split("|")
            a, ch = c["all"], c["of_changed"]
            lines.append(f"| {kind} | {s} | {a['n']} | {1 - a['unchanged']:.2f} | {ch['n']} | "
                         + " | ".join("-" if ch[k] is None else f"{ch[k]:.2f}" for k in SWAP_CLASSES[1:]) + " |")  # fmt: skip
        lines.append("")
    (out / "swaprecall.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("stage", choices=("lenswrite", "swaprecall"))
    a = ap.parse_args()
    stage_lenswrite() if a.stage == "lenswrite" else stage_swaprecall()


if __name__ == "__main__":
    main()
