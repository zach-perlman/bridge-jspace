"""twohop_pilot: quick experiment L2 (Zach, 2026-10-20, after Neel's "too toy"): can the model chain natural two-hop
facts (TwoHopFact, Yang et al. 2024: Wikidata facts, many relation types) without chain of thought, from memory and
with either fact given in the prompt? Competence only; it decides whether natural facts can carry the sprint's
memory-vs-context test.

Four fact types whose answer is a country (many-to-one, not one-to-one like country -> capital):
  game -> developer -> headquarters country      song -> singer -> birth country
  novel -> author -> birth country               person -> birth city -> country
Per type 100 rows (distinct first entity, at most 15 per answer, seed 401). Versions, in the chat format with the
blank and 'Answer:' (bridge_jspace.chat.blank_content):
  MM  both facts recalled:            "<two-hop statement> ___"
  CM  the first fact in the prompt:   three facts of hop 1 (the item's and two other rows' of the type), then MM
  MC  the second fact in the prompt:  three facts of hop 2 (the item's bridge's and two others'), then MM
  CC  both facts in the prompt:       both sets of three, then MM
  hop1, hop2: each fact alone (blank statements), from memory
Distractor rows have other bridges and other answers. Judge: an alias of the expected answer (TwoHopFact's e3 aliases,
plus 'United States' / 'USA' / 'US' for the United States of America) in the first line of the greedy continuation.

python scripts/twohop_pilot.py make --csv PATH        (data/twohop_pilot/items.json; the CSV's sha256 recorded)
python scripts/twohop_pilot.py competence --name N --why W
"""

from __future__ import annotations

import argparse
import ast
import collections
import csv
import hashlib
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import switches
from bridge_jspace.stats import wilson

DATA = pins.DATA_DIR / "twohop_pilot"
RESULTS = pins.RESULTS_DIR / "twohop_pilot"
TYPES = ("hqcntry of vdgame's dev", "birthcntry of song's singer", "birthcntry of novel's author",
         "cntry of person's birthcity")  # fmt: skip
N_PER_TYPE, SEED, MAX_PER_ANSWER = 100, 401, 15
VERSIONS = ("MM", "CM", "MC", "CC", "hop1", "hop2")
USA = ("United States of America", "United States", "USA", "US", "America")


def aliases(row: dict) -> list[str]:
    try:
        parsed = ast.literal_eval(row["e3.aliases"])
        names = [a for group in parsed for a in group]
    except (ValueError, SyntaxError):
        names = []
    names = [row["e3.value"], *names]
    if row["e3.value"] == "United States of America":
        names += list(USA)
    return sorted(set(names), key=len, reverse=True)


def sentence(template: str, subject: str, obj: str) -> str:
    return template.replace("{}", subject) + f" {obj}."


SCREEN_TYPES = (*TYPES, "birthcntry of person's spouse")  # the screening set adds a fifth person-centred type
SCREEN_SEED, N_SCREEN = 402, 500


def make(csv_path: str, screen: bool = False) -> None:
    """The pilot set (items.json), or with `screen` the screening set (screen.json: 500 rows per type over five types,
    its own seed, for picking facts the model knows on Day 1)."""
    DATA.mkdir(parents=True, exist_ok=True)
    out_path = DATA / ("screen.json" if screen else "items.json")
    types, n_per_type, seed = (SCREEN_TYPES, N_SCREEN, SCREEN_SEED) if screen else (TYPES, N_PER_TYPE, SEED)
    assert not out_path.exists(), f"{out_path} exists; data files are written once"
    raw = Path(csv_path).read_bytes()
    rows = list(csv.DictReader(raw.decode().splitlines()))
    rng = random.Random(seed)
    items = []
    for t in types:
        pool = [r for r in rows if r["fact_comp_type"] == t]
        rng.shuffle(pool)
        picked, seen_e1, per_answer = [], set(), collections.Counter()
        for r in pool:
            if r["e1.value"] in seen_e1 or per_answer[r["e3.value"]] >= MAX_PER_ANSWER:
                continue
            seen_e1.add(r["e1.value"])
            per_answer[r["e3.value"]] += 1
            picked.append(r)
            if len(picked) == n_per_type:
                break
        for k, r in enumerate(picked):
            others = [o for o in pool if o["e2.value"] != r["e2.value"] and o["e3.value"] != r["e3.value"]]
            d1, d2 = rng.sample(others, 2)
            hop1 = [sentence(x["r1.template"], x["e1.value"], x["e2.value"]) for x in (r, d1, d2)]
            hop2 = [sentence(x["r2.template"], x["e2.value"], x["e3.value"]) for x in (r, d1, d2)]
            order1, order2 = rng.sample(range(3), 3), rng.sample(range(3), 3)
            ctx1 = " ".join(hop1[i] for i in order1)
            ctx2 = " ".join(hop2[i] for i in order2)
            two = r["r2(r1(e1)).prompt"]
            items.append({
                "id": f"T{types.index(t)}-{k:03d}", "type": t, "e1": r["e1.value"], "e2": r["e2.value"],
                "e3": r["e3.value"], "aliases": aliases(r), "uid": r["uid"],
                "prompts": {
                    "MM": two, "CM": f"{ctx1} {two}", "MC": f"{ctx2} {two}", "CC": f"{ctx1} {ctx2} {two}",
                    "hop1": r["r1(e1).prompt"], "hop2": r["r2(e2).prompt"],
                },
                "expected": {"MM": r["e3.value"], "CM": r["e3.value"], "MC": r["e3.value"], "CC": r["e3.value"],
                             "hop1": r["e2.value"], "hop2": r["e3.value"]},
                "hop1_aliases": sorted({r["e2.value"], *[a for g in ast.literal_eval(r["e2.aliases"]) for a in g]}
                                       if r["e2.aliases"].startswith("(") else {r["e2.value"]}, key=len, reverse=True),
            })  # fmt: skip
    blob = {"source": {"file": "TwoHopFact.csv (huggingface.co/datasets/soheeyang/TwoHopFact)",
                       "sha256": hashlib.sha256(raw).hexdigest()},
            "generator": f"scripts/twohop_pilot.py make{' --screen' if screen else ''} (seed {seed})", "doc": (__doc__ or "").split("\n\n")[1],
            "items": items}  # fmt: skip
    out_path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out_path, len(items), collections.Counter(it["type"] for it in items))


def judge(text: str, names: list[str]) -> bool:
    line = next((ln for ln in text.split("\n") if ln.strip()), "")
    return any(re.search(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", line) for a in names)


def competence(name: str, why: str, items_file: str = "items.json") -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from scripts.exp03_brew_swaps import write_jsonl

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    items_path = DATA / items_file
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "items": {"file": str(items_path.relative_to(pins.REPO_ROOT)),
                "sha256": sha256_of(items_path)}, "format": "chat, thinking off, 'Answer:' prefilled, blank statement",
                "generation": "greedy, 12 new tokens, batched by length", "judge": "an alias in the first line"}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    items = json.loads(items_path.read_text())["items"]
    model = load_model()
    tok = model.tokenizer
    prompts = []
    for it in items:
        for v in VERSIONS:
            text = chat.chat_text(tok, chat.blank_content(it["prompts"][v]))
            names = it["hop1_aliases"] if v == "hop1" else it["aliases"]
            prompts.append({"id": it["id"], "type": it["type"], "version": v, "names": names,
                            "ids": tok(text, add_special_tokens=False).input_ids})  # fmt: skip
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    t0 = time.time()
    for group in by_len.values():
        for start in range(0, len(group), 64):
            chunk = group[start : start + 64]
            texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 12, [{}] * len(chunk))
            for p, text in zip(chunk, texts, strict=True):
                p["continuation"] = text
                p["correct"] = judge(text, p["names"])
    rows = [{k: v for k, v in p.items() if k != "ids"} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary: dict = {"seconds": round(time.time() - t0), "types": {}}
    lines = ["| type | n | " + " | ".join(VERSIONS) + " | MM given both hops |", "|---" * (len(VERSIONS) + 3) + "|"]
    for t in (*dict.fromkeys(it["type"] for it in items), "all"):
        per: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in rows:
            if t in ("all", r["type"]):
                per[r["id"]][r["version"]] = r["correct"]
        cells = {v: wilson(sum(x[v] for x in per.values()), len(per)) for v in VERSIONS}
        both = [x for x in per.values() if x["hop1"] and x["hop2"]]
        cond = {v: (sum(x[v] for x in both), len(both)) for v in ("MM", "CM", "MC", "CC")}
        summary["types"][t] = {"n": len(per), "cells": cells, "given_both_hops": cond}
        lines.append(f"| {t} | {len(per)} | " + " | ".join(f"{100 * cells[v][0]:.0f}%" for v in VERSIONS)
                     + f" | {cond['MM'][0]}/{cond['MM'][1]} |")  # fmt: skip
    lines += [
        "",
        "Given both hops right alone (MM, CM, MC, CC): " + json.dumps(summary["types"]["all"]["given_both_hops"]),
    ]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "competence"])
    ap.add_argument("--csv")
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--screen", action="store_true", help="make: the screening set; competence: run on it")
    args = ap.parse_args()
    if args.stage == "make":
        assert args.csv, "make needs --csv"
        make(args.csv, args.screen)
    else:
        assert args.name, "competence needs --name"
        assert args.why, "competence needs --why"
        competence(args.name, args.why, "screen.json" if args.screen else "items.json")
