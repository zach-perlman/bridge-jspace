"""tasks3_ab2: can a rewording rescue planets and Greek letters in three-step questions? (Zach, 2026-10-21; after
tasks3_ab_v1: property-keyed bin rules and clean contexts fix animals, vehicles, instruments, shapes and elements,
but planets and Greek letters stay at 14-69%.) Fresh P-start scenes (planets, Greek letters; elements as the control),
prose, each word's context only what its question needs (the v6 design: picks + bins for P->M->P, picks + one-way
partners for P->P->M), every step also asked alone.
P->M->P rule wordings (question "Which bin does Sam's pick go in?"):
  position   "The planet in position 4 from the Sun goes in bin 5."         (tasks3_ab_v1's property rule)
  ordinal    "The fourth planet from the Sun goes in bin 5."
  whose      "Planets whose position from the Sun is 4 go in bin 5."
P->P->M question wordings: q1 "Counting from the Sun, which position is the partner of Sam's pick?" (tasks_v2's
first wording), q2 "What is the position of the partner of Sam's pick counting from the Sun?" (its second).
Success (fixed before the run): a wording that brings planets and Greek letters to >= 85% on the items whose steps
the model answers right alone is adopted; otherwise they are left out of three-step words.

python scripts/tasks3_ab2.py --name N --why W [--n 24]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import suite_v1 as S
from scripts import tasks_v2 as T

ORD = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
RULES = {
    "position": {"planets": "The planet in position {n} from the Sun goes in bin {b}.",
                 "greek": "The Greek letter in position {n} of the alphabet goes in bin {b}.",
                 "elements": "The element with atomic number {n} goes in bin {b}."},
    "ordinal": {"planets": "The {o} planet from the Sun goes in bin {b}.",
                "greek": "The {o} letter of the Greek alphabet goes in bin {b}.",
                "elements": "The element with atomic number {n} goes in bin {b}."},
    "whose": {"planets": "Planets whose position from the Sun is {n} go in bin {b}.",
              "greek": "Greek letters whose position in the alphabet is {n} go in bin {b}.",
              "elements": "Elements whose atomic number is {n} go in bin {b}."},
}  # fmt: skip
DOMAINS = ("planets", "greek", "elements")


def fresh_scenes(n: int, seed: int) -> list[dict]:
    last: dict = {}
    orig_scene, orig_ms = T.scene, T.make_scene

    def scene(*a, **k):
        last["sc"] = orig_scene(*a, **k)
        return last["sc"]

    def ms(*a, **k):
        its = orig_ms(*a, **k)
        for it in its or []:
            it["_sc"] = json.loads(json.dumps(last["sc"]))
        return its

    T.scene, T.make_scene = scene, ms
    tmp = "_ab2_tmp"
    try:
        T.make(tmp, n, ["PPM", "PMP"], list(DOMAINS), ["prose"], list(T.LEVELS), seed)
        return T.load(tmp)
    finally:
        shutil.rmtree(T.DATA / tmp, ignore_errors=True)
        T.scene, T.make_scene = orig_scene, orig_ms


def context(it: dict, lines: list[str]) -> str:
    sc, dom = it["_sc"], T.DOMAINS[it["domain"]]
    picks = [
        f"{p} picked {T.ref(dom, t)}." for p, t in list(sc["pick"].items()) + [tuple(x) for x in sc["lookalike_picks"]]
    ]
    filler = random.Random(f"filler|{it['scene']}").sample(T.FILLER, T.LEVELS[it["level"]]["filler"])
    out = picks + lines + filler
    random.Random(f"order|{it['scene']}|{len(lines)}").shuffle(out)
    return " ".join(out)


def jobs_for(it: dict) -> list[dict]:
    sc, d = it["_sc"], it["domain"]
    dom = T.DOMAINS[d]
    st = sc["numbers"]
    desc = f"{sc['person']}'s pick"
    x = sc["x"]
    out = []
    step1 = ("step1", f"What did {sc['person']} pick?", x, "word")
    if it["word"] == "PMP":
        bins = {int(k): v for k, v in sc["bin"].items()}
        for name, rules in RULES.items():
            lines = [
                rules[d].format(n=T.num(n, st), o=ORD[n], b=T.num(bins[n], st))
                for n in sorted(set(dom.values.values()))
            ]
            ctx = context(it, lines)
            out.append({"variant": name, "part": "whole", "context": ctx, "question": f"Which bin does {desc} go in?",
                        "answer": it["answer"], "kind": "digit"})  # fmt: skip
            for part, q, a, k in (step1, ("step2", dom.prop_q[0].format(x=T.ref(dom, x)), str(dom.values[x]), "digit")):
                out.append({"variant": name, "part": part, "context": ctx, "question": q, "answer": a, "kind": k})
    else:
        y = dict(sc["partner"])[x]
        lines = []
        for a, b in sc["pairs"]:
            lines += [
                f"{T.cap(T.ref(dom, a))}'s partner is {T.ref(dom, b)}.",
                f"{T.cap(T.ref(dom, b))}'s partner is {T.ref(dom, a)}.",
            ]
        ctx = context(it, lines)
        for name, q in (("q1", dom.prop_q[0]), ("q2", dom.prop_q[1])):
            out.append({"variant": name, "part": "whole", "context": ctx, "question": q.format(x=f"the partner of {desc}"),
                        "answer": it["answer"], "kind": "digit"})  # fmt: skip
            for part, qq, a, k in (step1, ("step2", f"Which {dom.noun} is the partner of {T.ref(dom, x)}?", y, "word"),
                                   ("step3", dom.prop_q[0].format(x=T.ref(dom, y)), str(dom.values[y]), "digit")):  # fmt: skip
                out.append({"variant": name, "part": part, "context": ctx, "question": qq, "answer": a, "kind": k})
    for j in out:
        j.update({"id": it["id"], "word": it["word"], "domain": d, "level": it["level"]})
    return out


def main(args) -> None:
    import torch

    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out = pins.RESULTS_DIR / "tasks_v2" / args.name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"run": args.name, "why": args.why, "git_commit": commit, "n": args.n,
                                                   "seed": args.seed, "model": pins.model_pin(),
                                                   "doc": (__doc__ or "").split("\n\n", 1)[1],
                                                   "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    items = fresh_scenes(args.n, args.seed)
    model = load_model()
    tok = model.tokenizer
    jobs = [j for it in items for j in jobs_for(it)]
    for j in jobs:
        j["ids"] = S.ids(tok, T.render(tok, {"format": "prose", "context": j["context"], "question": j["question"],
                                             "kind": j["kind"]}))  # fmt: skip
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    t0 = time.time()
    for group in by_len.values():
        for start in range(0, len(group), 64):
            chunk = group[start : start + 64]
            texts = model.generate_batch(torch.tensor([j["ids"] for j in chunk], device="cuda"), 8, [{}] * len(chunk))
            for j, text in zip(chunk, texts, strict=True):
                j["text"], j["correct"] = text, T.judge(text, j["answer"], j["kind"])
    rows = [{k: v for k, v in j.items() if k not in ("ids", "context")} for j in jobs]
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    steps_ok = collections.defaultdict(lambda: True)
    for r in rows:
        if r["part"] != "whole":
            steps_ok[(r["id"], r["variant"])] &= r["correct"]
    pct = lambda v: f"{100 * statistics.mean(v):.0f}% ({len(v)})" if v else "-"  # noqa: E731
    lines = [f"# tasks3_ab2 / {args.name}: whole-question accuracy (all items) / on the items whose steps are right alone", "",
             "| word | variant | " + " | ".join(DOMAINS) + " |", "|---|---|" + "---|" * len(DOMAINS)]  # fmt: skip
    summary: dict = {"seconds": round(time.time() - t0), "cells": {}}
    for word, var in dict.fromkeys((r["word"], r["variant"]) for r in rows):
        cells = []
        for d in DOMAINS:
            sel = [
                r
                for r in rows
                if r["word"] == word and r["variant"] == var and r["domain"] == d and r["part"] == "whole"
            ]
            ok = [r["correct"] for r in sel if steps_ok[(r["id"], var)]]
            summary["cells"][f"{word}/{var}/{d}"] = {"all": [r["correct"] for r in sel].count(True) / max(1, len(sel)),
                                                     "steps_ok": statistics.mean(ok) if ok else None, "n": len(sel), "n_ok": len(ok)}  # fmt: skip
            cells.append(f"{pct([r['correct'] for r in sel])} / {pct(ok)}")
        lines.append(f"| {word} | {var} | " + " | ".join(cells) + " |")
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--seed", type=int, default=711)
    main(ap.parse_args())
