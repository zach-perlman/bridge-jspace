"""tasks3_ab: why do tasks_v2's three-step questions fail when the suite's work? (Zach, 2026-10-21; decided with Zach:
diagnose, then rewrite.) The same P-start scenes as calibration (calib_v5, levels 0 and 2, all domains), re-rendered
in prose with one factor changed at a time; the questions' answers are the scenes' own (the bin mapping, partners and
lockers are unchanged).

P->M->P (the bin step), 3 phrasings x 2 contexts:
  abstract      rules "Things numbered 4 go in bin 5." (1-9); question "Which bin holds things numbered the same as
                the number of legs of Sam's pick?" (calib_v5 as is)
  prop_nested   rules keyed by the property, for the domain's numbers only ("Animals with 4 legs go in bin 5.");
                question still nested ("Which bin goes with the number of legs of Sam's pick?")
  prop_natural  the same rules; question "Which bin does Sam's pick go in?" (the suite's BRL style)
P->P->M (the partner step), 2 wordings x 2 contexts:
  pairs         "The cow and the spider are partners." (calib_v5 as is)
  one_way       "The cow's partner is the spider. The spider's partner is the cow." (the suite's BLR style)
Contexts: full (picks, partners, lockers, bins: calib_v5) or relevant (picks and only the relation the question uses);
filler and look-alike picks as the scene's level has them. Success (fixed before the run): >= 85% on the items whose
steps the model answered right alone in calibration.

python scripts/tasks3_ab.py --name N --why W
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

RULE = {"animals": "Animals with {n} legs go in bin {b}.", "vehicles": "Vehicles with {n} wheels go in bin {b}.",
        "instruments": "Instruments with {n} strings go in bin {b}.", "shapes": "Shapes with {n} sides go in bin {b}.",
        "planets": "The planet in position {n} from the Sun goes in bin {b}.",
        "elements": "The element with atomic number {n} goes in bin {b}.",
        "greek": "The Greek letter in position {n} of the alphabet goes in bin {b}."}  # fmt: skip


def scenes_of(set_name: str, seed: int, n: int) -> list[dict]:
    """calib_v5 regenerated with each item's scene attached (checked identical to the committed file)."""
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
    tmp = "_ab_tmp"
    try:
        T.make(tmp, n, list(T.WORDS2 + T.WORDS3), list(T.DOMAINS), list(T.FORMATS), list(T.LEVELS), seed)
        items = T.load(tmp)
    finally:
        shutil.rmtree(T.DATA / tmp, ignore_errors=True)
        T.scene, T.make_scene = orig_scene, orig_ms
    assert [{k: v for k, v in it.items() if k != "_sc"} for it in items] == T.load(set_name), "did not regenerate"
    return items


def context(dom_name: str, sc: dict, *, rules: str, partners: str, keep: set[str], filler: list[str], seed: str) -> str:
    dom = T.DOMAINS[dom_name]
    ref = lambda t: T.ref(dom, t)  # noqa: E731
    st = sc["numbers"]
    lines = [f"{p} picked {ref(t)}." for p, t in list(sc["pick"].items()) + [tuple(x) for x in sc["lookalike_picks"]]]
    if "partner" in keep:
        for a, b in sc["pairs"]:
            if partners == "pairs":
                lines.append(f"{T.cap(ref(a))} and {ref(b)} are partners.")
            else:
                lines += [f"{T.cap(ref(a))}'s partner is {ref(b)}.", f"{T.cap(ref(b))}'s partner is {ref(a)}."]
    if "locker" in keep:
        lines += [f"The locker of {ref(t)} is {T.num(n, st)}." for t, n in sc["locker"].items()]
    if "bin" in keep:
        bins = {int(k): v for k, v in sc["bin"].items()}
        if rules == "abstract":
            lines += [f"Things numbered {T.num(n, st)} go in bin {T.num(b, st)}." for n, b in bins.items()]
        else:
            lines += [
                RULE[dom_name].format(n=T.num(n, st), b=T.num(bins[n], st)) for n in sorted(set(dom.values.values()))
            ]
    lines += filler
    random.Random(seed).shuffle(lines)
    return " ".join(lines)


def variants(it: dict) -> list[tuple[str, str, str, str]]:
    """(word, variant, context, question) for one P-start scene's PMP and PPM items."""
    sc, d = it["_sc"], it["domain"]
    dom = T.DOMAINS[d]
    desc = f"{sc['person']}'s pick"
    filler = it["context_filler"]
    out = []
    for ctx_name, keep_pmp, keep_ppm in (("full", {"partner", "locker", "bin"}, {"partner", "locker", "bin"}),
                                         ("relevant", {"bin"}, {"partner"})):  # fmt: skip
        seed = f"{it['scene']}|{ctx_name}"
        for name, rules, q in (
            ("abstract", "abstract", T.Q_BIN[0].format(n=dom.prop_phrase.format(x=desc))),
            ("prop_nested", "prop", f"Which bin goes with {dom.prop_phrase.format(x=desc)}?"),
            ("prop_natural", "prop", f"Which bin does {desc} go in?"),
        ):
            c = context(d, sc, rules=rules, partners="pairs", keep=keep_pmp, filler=filler, seed=seed)
            out.append(("PMP", f"{name}/{ctx_name}", c, q))
        for name in ("pairs", "one_way"):
            c = context(d, sc, rules="abstract", partners=name, keep=keep_ppm, filler=filler, seed=seed)
            out.append(("PPM", f"{name}/{ctx_name}", c, dom.prop_q[0].format(x=f"the partner of {desc}")))
    full = context(d, sc, rules="abstract", partners="pairs", keep={"partner", "locker", "bin"}, filler=filler,
                   seed=f"{it['scene']}|full")  # fmt: skip
    out += [
        ("PP", "reference/full", full, T.Q_LOCKER[0].format(d=desc)),
        ("PM", "reference/full", full, dom.prop_q[0].format(x=desc)),
    ]
    return out


def main(args) -> None:
    import torch

    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out = pins.RESULTS_DIR / "tasks_v2" / args.name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"run": args.name, "why": args.why, "git_commit": commit,
                                                   "model": pins.model_pin(), "set": "calib_v5", "levels": [0, 2],
                                                   "doc": (__doc__ or "").split("\n\n", 1)[1],
                                                   "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    items = scenes_of("calib_v5", 705, 48)
    comp = collections.defaultdict(dict)
    for line in (pins.RESULTS_DIR / "tasks_v2" / "calib_v5_competence_v1" / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        comp[r["id"]][r["part"]] = r["correct"]
    model = load_model()
    tok = model.tokenizer
    jobs = []
    for it in items:
        if it["word"] not in ("PMP", "PPM") or it["level"] not in (0, 2):
            continue
        it["context_filler"] = random.Random(f"filler|{it['scene']}").sample(T.FILLER, T.LEVELS[it["level"]]["filler"])
        steps_ok = all(v for p, v in comp[it["id"]].items() if p.startswith("step"))
        twins = {x["word"]: x for x in items if x["scene"] == it["scene"]}
        for word, var, ctx, q in variants(it):
            if word != it["word"] and not (it["word"] == "PMP" and word in ("PP", "PM")):
                continue
            ref = twins[word]
            ids = S.ids(tok, T.render(tok, {**ref, "format": "prose", "context": ctx, "_question": q}))
            jobs.append({"id": ref["id"], "word": word, "variant": var, "level": it["level"], "domain": it["domain"],
                         "answer": ref["answer"], "kind": ref["kind"], "steps_ok": steps_ok if word == it["word"] else True,
                         "ids": ids, "question": q})  # fmt: skip
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
    rows = [{k: v for k, v in j.items() if k != "ids"} for j in jobs]
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    acc = lambda sel: round(statistics.mean(r["correct"] for r in sel), 3) if sel else None  # noqa: E731
    summary: dict = {"seconds": round(time.time() - t0), "variants": {}}
    lines = [f"# tasks3_ab / {args.name}", "", "| word | variant | all | steps right alone | L0 | L2 | many-to-one domains |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    for word, var in dict.fromkeys((r["word"], r["variant"]) for r in rows):
        sel = [r for r in rows if r["word"] == word and r["variant"] == var]
        cell = {"n": len(sel), "all": acc(sel), "steps_ok": acc([r for r in sel if r["steps_ok"]]),
                "L0": acc([r for r in sel if r["level"] == 0]), "L2": acc([r for r in sel if r["level"] == 2]),
                "many_to_one": acc([r for r in sel if r["domain"] in ("animals", "vehicles", "instruments")])}  # fmt: skip
        summary["variants"][f"{word}/{var}"] = cell
        lines.append(f"| {word} | {var} | {cell['all']} | {cell['steps_ok']} | {cell['L0']} | {cell['L2']} | "
                     f"{cell['many_to_one']} |")  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    main(ap.parse_args())
