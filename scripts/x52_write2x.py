"""x52_write2x (Dan, 29 Oct morning brief, CPU): batch 52 B's write on the main test, read again. Writing S's answer
word directions at the write cell moves the recall to S's answer at gain 1 (9B 0.37 / Muse 0.70 / Lightning 0.65) but
hardly at gain 2 (0.03 / 0.09 / 0.01). What does the model output at 2x?

Per model, reader and arm, the top token of every written prompt (x52_answer_map's outcomes.jsonl, full-vocabulary
argmax) is put in one class:
  target    S's answer token (the decisive read; tok_b)
  original  O's answer token (tok_A)
  written   one of the written answer word's own letter tokens (norms.jsonl's A_ids: the write's directions)
  digit     another digit
  other     anything else
with the most frequent decoded 'written' / 'digit' / 'other' tokens. Descriptive, after the data, no rule; UNVERIFIED.
Writes results/x52_answer_map/x52_write2x-<UTC>/ (write2x.md, write2x.json). Keep B out of the README (Dan)."""

from __future__ import annotations

import collections
import json
import time
from pathlib import Path

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts.x52_atoms import tokenizer_of

RESULTS = pins.RESULTS_DIR / "x52_answer_map"
RUNS = {"qwen3.5-9b": "qwen35_9b_x52_write_main", "qwen3.6-27b": "x52_write_main_27b",
        "muse-glimmer-30b": "muse30_x52_write_main", "nemotron-3.5-lightning": "nem35l_x52_write_main"}  # fmt: skip
ARMS = ("none", "whole", "ans1", "ans2", "rand1", "rand2", "freq1", "freq2")
READERS = {"PP": "lookup", "PM": "recall"}
CLASSES = ("target", "original", "written", "digit", "other")
N_TOP = 5


def classify(row: dict, written: set[int], digit_ids: set[int]) -> str:
    """The class of one outcome row's top token (see the module docstring)."""
    if row["role"] == "b":
        return "target"
    if row["role"] == "A":
        return "original"
    if row["top"] in written:
        return "written"
    return "digit" if row["top"] in digit_ids else "other"


def summarise(rows: list[dict], norms: dict, digit_ids: set[int], decode) -> dict:
    """Per (reader, arm): n, the share of each class, and the most frequent decoded tokens of the non-answer classes."""
    out: dict = {}
    for (reader, arm), group in sorted(_groups(rows).items()):
        written = {k: set(norms.get((k, reader), [])) for k in {r["key"] for r in group}}
        cls = [classify(r, written[r["key"]], digit_ids) for r in group]
        n = len(group)
        tops = {c: collections.Counter(decode(r["top"]) for r, k in zip(group, cls, strict=True) if k == c)
                for c in ("written", "digit", "other")}  # fmt: skip
        out[f"{reader}|{arm}"] = {"n": n, "share": {c: round(cls.count(c) / n, 3) for c in CLASSES},
                                  "top": {c: tops[c].most_common(N_TOP) for c in tops}}  # fmt: skip
    return out


def _groups(rows: list[dict]) -> dict[tuple[str, str], list[dict]]:
    g: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        g[(r["reader"], r["arm"])].append(r)
    return g


def main() -> Path:
    out = RESULTS / f"x52_write2x-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    blob: dict = {"exp": "x52_write2x", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "code": pins.git_state(), "runs": RUNS, "classes": CLASSES, "models": {}}  # fmt: skip
    for target, run in RUNS.items():
        src = RESULTS / run
        rows = X.read_jsonl(src / "outcomes.jsonl")
        norms = {(n["key"], n["reader"]): n.get("A_ids", []) for n in X.read_jsonl(src / "norms.jsonl")}
        tok = tokenizer_of(target)
        digit_ids = {i for d in "0123456789" for i in tok.encode(d, add_special_tokens=False)[:1]}
        blob["models"][target] = {"run": f"results/x52_answer_map/{run}",
                                  "summary": summarise(rows, norms, digit_ids, lambda t, tok=tok: tok.decode([t]))}  # fmt: skip
    out.mkdir(parents=True)
    (out / "write2x.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = ["# x52_write2x: what the model outputs under 52 B's write, at 1x and 2x (descriptive; UNVERIFIED)", "",
             "Dan, 29 Oct morning brief (CPU): the recall's write moves 0.37 / 0.70 / 0.65 to S's answer at gain 1 but "
             "0.03 / 0.09 / 0.01 at gain 2 (9B / Muse / Lightning). Classes of the top token (full vocabulary): target = "
             "S's answer token, original = O's, written = one of the written answer word's own tokens, digit = another "
             "digit, other = anything else. Main test, write cell per reader as in 52 B. Keep out of the README (Dan).",
             ""]  # fmt: skip
    for target, m in blob["models"].items():
        lines += [f"## {target} ({m['run']})", "", "| reader | arm | n | " + " | ".join(CLASSES) + " | top written / "
                  "digit / other tokens |", "|" + "---|" * (4 + len(CLASSES))]  # fmt: skip
        for key, s in m["summary"].items():
            reader, arm = key.split("|")
            tops = "; ".join(f"{c}: " + ", ".join(f"{t!r} {k}" for t, k in s["top"][c]) for c in s["top"] if s["top"][c])
            lines.append(f"| {READERS[reader]} | {arm} | {s['n']} | " + " | ".join(f"{s['share'][c]:.2f}" for c in CLASSES)
                         + f" | {tops} |")  # fmt: skip
        lines.append("")
    (out / "write2x.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


if __name__ == "__main__":
    main()
