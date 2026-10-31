"""sd_gate (2026-10-30, prereg amendment 66 addendum): our dataset practices applied to the silent-dissent items (note 40).

Per model, for every item of its known stage (results/sd_necessity/{P}sd_known_v1/items.jsonl: their known check passed,
paired; both splits, whatever round 0 said), closed book, greedy 12 tokens after their known check's two-line prefix
(sd_prompts.KNOWN_SHOTS), first line, their alias match (sd_prompts.matches), exactly as nn_sd_necessity's known stage:
  guess     the composed question with e1 replaced by a generic noun (GENERIC: "the person" for the person categories,
            "the landmark", "the university"); guess_right = the answer matches e3. The item passes if it does NOT.
  direct    a direct e1 -> e3 question, fixed templates per category (DIRECT; approximations, reported as such);
            shortcut = the answer matches e3 (a shortcut is available).
  name      no model: name_drop if e1 or any alias of e2 contains any alias of e3 as a word, or shares a 4-letter stem
            with it (a word of >= 4 letters, not one of their stopwords, whose first 4 letters equal those of such a word
            of the e3 alias); name_reason records what matched. name_drop_canonical (descriptive, not the registered rule):
            the same on the names as written (e1, e2, e3) without aliases; the reader's --name-rule canonical uses it.
  gated     = known (every item here) and not guess_right and not name_drop; no_shortcut = gated and not shortcut.
The knock-out runs are unchanged; scripts/nn_sd_read.py --gate applies these strata.
Writes results/sd_necessity/{P}sd_gate_v1/{gate.jsonl, manifest.json, summary.json}.

python scripts/sd_gate.py --name {P}sd_gate_v1 --items-run {P}sd_known_v1 [--n 8] [--batch 64]
python scripts/sd_gate.py --cpu-check --facts data/sd_v1/facts.jsonl [--items-run {P}sd_known_v1]   (tokenizer only: example
       prompts, name-filter counts over every fact and, given a known run, over its items)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import sd_prompts as SP  # noqa: E402

GENERIC = {"person-birthcity-cntry": "the person", "person-uguniv-hqcity": "the person",
           "landmark-cntry-capital": "the landmark", "univ-hqcity-cntry": "the university"}  # fmt: skip
DIRECT = {  # the addendum's fixed templates
    "person-birthcity-cntry": "{e1} is a citizen of the country of",
    "person-uguniv-hqcity": "The city most associated with {e1} is",
    "landmark-cntry-capital": "The city most associated with {e1} is",
}


def guess_prompt(f: dict) -> str:
    """The composed statement with e1 (case-insensitive, its last occurrence) replaced by the category's generic noun,
    capitalised at the start of the sentence."""
    c, e1, noun = f["composed"], f["e1"], GENERIC[f["category"]]
    i = c.lower().rfind(e1.lower())
    assert i >= 0, f["uid"]
    if i == 0:
        noun = noun[:1].upper() + noun[1:]
    return c[:i] + noun + c[i + len(e1) :]


def direct_prompt(f: dict) -> str:
    return DIRECT[f["category"]].format(e1=f["e1"])


def name_check(f: dict, canonical: bool = False) -> tuple[bool, str]:
    """(drop, reason): does e1 or an alias of e2 contain an alias of e3 as a word, or share a 4-letter stem with it (the
    addendum's rule, literally: every alias)? canonical=True (descriptive alternative, not the registered rule): the same
    tests on the names as written only (e1, e2, e3), without Wikidata's aliases (which include forms like "Salzburg,
    Austria" for a birth city)."""
    hosts = [("e1", f["e1"])] + [("e2", x) for x in ([f["e2"]] if canonical else f["e2_aliases"])]
    for alias in [f["e3"]] if canonical else f["e3_aliases"]:
        a = SP.norm(alias)
        if len(a) < 2 or a in SP.STOPWORDS:
            continue
        stems = {w[:4] for w in a.split() if len(w) >= 4 and w not in SP.STOPWORDS}
        for role, h in hosts:
            hn = SP.norm(h)
            if f" {a} " in f" {hn} ":
                return True, f"{role} '{h}' contains e3 alias '{alias}'"
            for w in hn.split():
                if len(w) >= 4 and w not in SP.STOPWORDS and w[:4] in stems:
                    return True, f"{role} '{h}' word '{w}' shares a 4-letter stem with e3 alias '{alias}'"
    return False, ""


def cpu_check(a) -> None:
    """Tokenizer only (BJ_TARGET picks it): two guess and two direct prompts per category as the model reads them, and
    the name filter's counts per category over every fact (no model: the filter needs none)."""
    from bridge_jspace import pins, tokens

    tok = tokens.load_tokenizer()
    facts = [json.loads(line) for line in Path(a.facts).read_text().splitlines()]
    facts = [f for f in facts if f["category"] in DIRECT]
    print(f"BJ_TARGET={pins.TARGET}")
    for cat in DIRECT:
        fs = [f for f in facts if f["category"] == cat]
        for f in random.Random(f"0:{cat}").sample(fs, 2):
            for kind, p in (("guess", guess_prompt(f)), ("direct", direct_prompt(f))):
                ids = tokens.raw_encoding(tok, SP.KNOWN_SHOTS + p)["input_ids"]
                assert tok.decode(ids).endswith(p), (kind, f["uid"])
                print(f"  [{cat} | {kind} | e1={f['e1']} e2={f['e2']} e3={f['e3']} | {len(ids)} tokens, last {tok.decode(ids[-1:])!r}]\n    {p!r}")
    if a.full:
        for f in facts:  # every fact renders (case-insensitive e1 found; the template fills)
            guess_prompt(f), direct_prompt(f)
    by: dict = collections.defaultdict(collections.Counter)
    reasons: dict = collections.defaultdict(list)
    for f in facts:
        drop, why = name_check(f)
        c = by[f"{f['split']}/{f['category']}"]
        c["facts"] += 1
        c["name_drop"] += drop
        c["canonical"] += name_check(f, canonical=True)[0]
        if drop and len(reasons[f["category"]]) < 6:
            reasons[f["category"]].append(f"{f['e1']} | {f['e2']} -> {f['e3']}: {why}")
    print("name/stem filter over every fact (the model's known items are a subset): dropped (registered rule, every alias) | "
          "dropped by the canonical-names variant (descriptive) | facts")
    for k in sorted(by):
        print(f"  {k:36s} {by[k]['name_drop']:5d} | {by[k]['canonical']:5d} | {by[k]['facts']}")
    for cat, rs in reasons.items():
        print(f"  examples, {cat}:")
        for r in rs:
            print(f"    {r}")
    if a.items_run:  # the same filter on a model's known items (no model needed)
        from scripts.nn_sd_necessity import RES

        items = [json.loads(line) for line in (RES / a.items_run / "items.jsonl").read_text().splitlines()]
        c2: dict = collections.defaultdict(collections.Counter)
        for it in items:
            for scope in ("all", "test_round0_right") if it["split"] == "test" and it["r0_outcome"] == "original" else ("all",):
                k = f"{a.items_run} {scope}/{it['fact']['category']}"
                c2[k]["items"] += 1
                c2[k]["name_drop"] += name_check(it["fact"])[0]
                c2[k]["canonical"] += name_check(it["fact"], canonical=True)[0]
        print("name/stem filter on the known items: dropped (registered rule) | canonical variant | items")
        for k in sorted(c2):
            print(f"  {k:70s} {c2[k]['name_drop']:4d} | {c2[k]['canonical']:4d} | {c2[k]['items']}")


def main(a) -> None:
    from bridge_jspace import pins
    from bridge_jspace.model import load_model
    from scripts.nn_sd_necessity import RES, generate, manifest_base, new_dir

    out_dir = new_dir(a.name)
    items = [json.loads(line) for line in (RES / a.items_run / "items.jsonl").read_text().splitlines()]
    if a.n and a.n < len(items):  # smoke: a seeded random subset
        items = random.Random(0).sample(items, a.n)
    (out_dir / "manifest.json").write_text(json.dumps({**manifest_base(a, "gate"), "n_items": len(items), "generic": GENERIC,
                                                       "direct": DIRECT, "prefix": SP.KNOWN_SHOTS}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    t0 = time.time()
    facts = [it["fact"] for it in items]
    gp, dp = [guess_prompt(f) for f in facts], [direct_prompt(f) for f in facts]
    ans = generate(model, [SP.KNOWN_SHOTS + p for p in gp + dp], a.gen_tokens, a.batch, "gate")
    ga, da = ans[: len(facts)], ans[len(facts) :]
    rows = []
    for it, f, g, d, gq, dq in zip(items, facts, ga, da, gp, dp, strict=True):
        drop, why = name_check(f)
        drop_c, why_c = name_check(f, canonical=True)
        guess_right, shortcut = SP.matches(g, f["e3_aliases"]), SP.matches(d, f["e3_aliases"])
        gated = not guess_right and not drop
        rows.append({"uid": f["uid"], "split": it["split"], "category": f["category"], "r0_outcome": it["r0_outcome"],
                     "guess_prompt": gq, "guess_answer": g, "guess_right": guess_right, "direct_prompt": dq, "direct_answer": d,
                     "shortcut": shortcut, "name_drop": drop, "name_reason": why, "gated": gated,
                     "no_shortcut": gated and not shortcut, "name_drop_canonical": drop_c, "name_reason_canonical": why_c,
                     "gated_canonical": not guess_right and not drop_c})  # fmt: skip
    (out_dir / "gate.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    summ: dict = {"seconds": round(time.time() - t0), "target": pins.TARGET, "n_items": len(rows), "by": {}}
    keys = ("guess_right", "shortcut", "name_drop", "gated", "no_shortcut", "name_drop_canonical", "gated_canonical")
    for scope, sel in (("all", lambda r: True), ("test_round0_right", lambda r: r["split"] == "test" and r["r0_outcome"] == "original")):
        for cat in sorted({r["category"] for r in rows}) + ["ALL"]:
            rs = [r for r in rows if sel(r) and (cat == "ALL" or r["category"] == cat)]
            summ["by"][f"{scope}/{cat}"] = {"n": len(rs), **{k: sum(r[k] for r in rs) for k in keys}}
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print(json.dumps(summ["by"], indent=1), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name")
    ap.add_argument("--why", default="prereg amendment 66 addendum: guess control, name/stem filter, shortcut flag (note 40)")
    ap.add_argument("--items-run")
    ap.add_argument("--n", type=int, default=0, help="smoke: a seeded random N items")
    ap.add_argument("--gen-tokens", type=int, default=12)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--cpu-check", action="store_true")
    ap.add_argument("--facts", default="data/sd_v1/facts.jsonl")
    ap.add_argument("--full", action="store_true", help="--cpu-check: render every fact's two prompts too")
    args = ap.parse_args()
    if args.cpu_check:
        cpu_check(args)
    else:
        assert args.name and args.items_run, "--name and --items-run"
        main(args)
