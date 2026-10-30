"""sd_build (2026-10-30, the silent-dissent necessity test; CPU only). Two subcommands.

facts   TwoHopFact (Yang et al. 2024, CC-BY-4.0; HF soheeyang/TwoHopFact @ 59a84cd, TwoHopFact.csv, sha256 522d3764...) and Ni &
        Zou's hand-made capital items (read with ast.literal_eval, never executed, from their silent_dissent/entity_facts.py
        @ fe78a9f) -> data/sd_v1/facts.jsonl: every fact of the chosen categories, in their load order (the CSV's, then the
        hand-made ones), with their fields and their bridge split (sd_prompts.split_of: dev share 0.3, seed 0).
check   (tokenizer only, BJ_TARGET picks it; no model, no GPU) a seeded sample of each split x category paired as if all
        were known (the known check needs the model): first-token collisions, and for every conversation and item the
        positions the runner relies on: the prompt's tokens are a prefix of prompt + " " + answer's (the answer's
        first token is the next token), the subject's last token is inside the final statement, the visible own
        statement holds the round-0 answer and no condition names the bridge; prints two rendered prompts per conversation.
        Amendment 73 note 56's keys (instr_vis, hyp_vis, prem_vis, prem_hid) also: e3' (their target) is the next token,
        the inserted lines are the registered wording with mu and e2' (or e3') exactly once, and e2' / e3' appear nowhere
        else after the worked examples (n56_check).

python scripts/sd_build.py facts --csv /workspace/data_sd/TwoHopFact.csv --handmade /workspace/data_sd/entity_facts_fe78a9f.py
       --categories landmark-cntry-capital person-birthcity-cntry person-uguniv-hqcity --out data/sd_v1/facts.jsonl
BJ_TARGET=qwen3.6-27b python scripts/sd_build.py check --facts data/sd_v1/facts.jsonl [--show 2]
"""

from __future__ import annotations

import argparse
import ast
import collections
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import sd_prompts as SP  # noqa: E402

CSV_SHA256 = "522d3764eba5c297f9fc630073ce5e897eac134e1d04824fed4d5349e605e338"
HANDMADE_PHRASES = {  # their HANDMADE: category -> (list name in entity_facts.py, r1 phrase)
    "landmark-cntry-capital": ("LANDMARKS", "the country where {s} is located"),
    "person-birthcntry-capital": ("PEOPLE", "the country where {s} was born"),
    "company-hqcntry-capital": ("COMPANIES", "the country where {s} is headquartered"),
}


def _aliases(raw: str, value: str) -> list[str]:
    out = [value]
    try:
        parsed = ast.literal_eval(raw) if raw else ()
    except (ValueError, SyntaxError):
        parsed = ()
    stack = list(parsed) if isinstance(parsed, (tuple, list)) else [parsed]
    while stack:
        x = stack.pop(0)
        if isinstance(x, (tuple, list)):
            stack = list(x) + stack
        elif isinstance(x, str) and x not in out:
            out.append(x)
    return out


def load_twohopfact(path: str) -> list[dict]:
    csv.field_size_limit(10**8)
    facts = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            facts.append({"uid": f"thf:{r['uid']}", "source": "twohopfact", "category": r["category"],
                          "e1": r["e1.value"], "e2": r["e2.value"], "e3": r["e3.value"],
                          "r1_prompt": r["r1(e1).prompt"], "r2_template": r["r2.template"], "composed": r["r2(r1(e1)).prompt"],
                          "e2_aliases": _aliases(r["e2.aliases"], r["e2.value"]), "e3_aliases": _aliases(r["e3.aliases"], r["e3.value"]),
                          "e2_type": r["e2.rough_category"], "e3_type": r["e3.rough_category"]})  # fmt: skip
    return facts


def handmade(path: str) -> list[dict]:
    """Their hand-made capital facts, rebuilt from the literals in entity_facts.py (ast.literal_eval: no code runs)."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    lit = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("CAPITALS", "ARTICLE", "LANDMARKS", "PEOPLE", "COMPANIES"):
                lit[name] = ast.literal_eval(node.value)
    facts = []
    for category, (list_name, phrase) in HANDMADE_PHRASES.items():
        for subject, country in lit[list_name]:
            mu = phrase.format(s=subject)
            e2 = lit["ARTICLE"].get(country, country)
            facts.append({"uid": f"hand:{category}:{subject}", "source": "handmade", "category": category, "e1": subject,
                          "e2": e2, "e3": lit["CAPITALS"][country], "r1_prompt": f"{mu[0].upper()}{mu[1:]} is",
                          "r2_template": "The capital city of {} is", "composed": f"The capital city of {mu} is",
                          "e2_aliases": list(dict.fromkeys([e2, country])), "e3_aliases": [lit["CAPITALS"][country]],
                          "e2_type": "country", "e3_type": "city"})  # fmt: skip
    return facts


def cmd_facts(a) -> None:
    sha = hashlib.sha256(Path(a.csv).read_bytes()).hexdigest()
    assert sha == CSV_SHA256, f"{a.csv}: sha256 {sha}, expected the pinned TwoHopFact.csv"
    facts = load_twohopfact(a.csv) + handmade(a.handmade)
    facts = [f for f in facts if f["category"] in a.categories]
    for f in facts:
        f["split"] = SP.split_of(f, 0.3, 0)
    no_subj = [f["uid"] for f in facts if f["e1"].lower() not in f["composed"].lower()]
    assert not no_subj, f"subject not in the composed statement: {no_subj[:5]}"
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in facts))
    c = collections.Counter((f["split"], f["category"]) for f in facts)
    (out.parent / "manifest.json").write_text(json.dumps({
        "built_by": "scripts/sd_build.py facts", "csv": "soheeyang/TwoHopFact@59a84cd883f71641a03fb6fa50da92a9603e7845 TwoHopFact.csv",
        "csv_sha256": sha, "handmade": "ziangni-sys/silent-dissent@fe78a9f9240efd334b9c3482e08b2c9c028ace18 silent_dissent/entity_facts.py (literals)",
        "handmade_sha256": hashlib.sha256(Path(a.handmade).read_bytes()).hexdigest(), "categories": a.categories,
        "split": "their split_of: md5('0-' + norm(e2)) % 10000 < 3000 -> dev", "license": "TwoHopFact CC-BY-4.0; silent-dissent MIT",
        "counts": {f"{s}/{k}": v for (s, k), v in sorted(c.items())}, "n": len(facts)}, indent=2) + "\n")  # fmt: skip
    print(f"{len(facts)} facts -> {out}")
    for (s, k), v in sorted(c.items()):
        print(f"  {s:4s} {k:28s} {v}")


def _count(hay: str, needle: str) -> int:
    """Occurrences of `needle` in `hay` as a whole word sequence after sd_prompts.norm (case, accents, punctuation)."""
    n = SP.norm(needle)
    return f" {SP.norm(hay)} ".count(f" {n} ") if n else 0


def n56_check(tok, f: dict, p: dict, tg: dict, conv: str, text: str, spans: list, ids: list[int], fails, seen) -> None:
    """Amendment 73 note 56's keys: (a) the peers' answer e3' (the target) is the next token too: the prompt's ids are a
    prefix of prompt + " " + e3''s and the next id is e3''s main first token; (b) the inserted lines are the registered
    wording and hold mu and e2' (hyp_vis), e2' (each prem peer line) or e3' (instr_vis) exactly once (as written); (c) after
    the worked examples e2' appears exactly once (hyp_vis), once per peer line (prem), never (instr_vis), and e3' only in
    the order (instr_vis: once; elsewhere never). Failures count in `fails` (the check exits 1)."""
    from bridge_jspace import tokens

    cond, style, n_peers, _ = SP.CONVS[conv]
    full = tokens.raw_encoding(tok, text + " " + p["e3"].strip())["input_ids"]
    if full[: len(ids)] != ids or full[len(ids)] != tg["main"]["peer"]:
        fails[f"{conv}: peer answer boundary"] += 1
    lines = {lab: text[s:e] for lab, s, e in spans}
    e2p, e3p, m = p["e2"].strip(), p["e3"].strip(), SP.mu(f)
    tail = text[len(SP.PLAIN_HEADER) + len(SP.PLAIN_SHOTS) :]
    if cond == "hypothetical":
        line = lines["moderator"]
        if line != SP.HYPOTHETICAL.format(mu=m, bridge=e2p) or line.count(m) != 1 or line.count(e2p) != 1:
            fails[f"{conv}: mu / e2' once in the supposition"] += 1
        if text.count(f"Moderator: Suppose that {m} were {e2p}.") != 1:
            fails[f"{conv}: supposition once"] += 1
        want_e2p, want_e3p = 1, 0
    elif cond == "instructed":
        line = lines["moderator"]
        if line != SP.INSTRUCTED.format(answer=e3p) or line.count(e3p) != 1 or f"\nCoordinator: {line}\n" not in text:
            fails[f"{conv}: e3' once in the order"] += 1
        want_e2p, want_e3p = 0, 1
    else:  # prem: premise-only pressure
        peer_ls = [v for k, v in lines.items() if k.startswith("peer")]
        if len(peer_ls) != n_peers or any(x != SP.statement(f["r1_prompt"], e2p) or x.count(e2p) != 1 for x in peer_ls):
            fails[f"{conv}: e2' once per peer line"] += 1
        if lines["moderator"] != SP.AGAIN:
            fails[f"{conv}: moderator line"] += 1
        want_e2p, want_e3p = n_peers, 0
    if _count(tail, e2p) != want_e2p:
        fails[f"{conv}: e2' count after the worked examples"] += 1
    inside = _count(e2p, e3p) * want_e2p  # e3' written inside e2' (the peers' bridge names their answer: the reader drops these)
    if inside:
        seen[f"{conv}: e2' names e3' (dropped by the reader)"] += 1
    if _count(tail, e3p) != want_e3p + inside:
        fails[f"{conv}: e3' count after the worked examples"] += 1
    seen[conv] += 1


def cmd_check(a) -> None:
    from bridge_jspace import pins, tokens

    tok = tokens.load_tokenizer()
    facts = [json.loads(line) for line in Path(a.facts).read_text().splitlines()]
    print(f"BJ_TARGET={pins.TARGET}: tokenizer {type(tok).__name__}, bos needed: {pins.TARGETS[pins.TARGET]['bos']}")
    import random

    # pairing is quadratic in a category's size (their assign_partners), so the check pairs a seeded sample of each
    # split x category (the runner pairs only the model's known facts, about a tenth)
    triples = []
    for split in ("dev", "test"):
        for cat in sorted({f["category"] for f in facts}):
            pool = [f for f in facts if f["split"] == split and f["category"] == cat]
            if len(pool) > a.per_category:
                keep = set(id(f) for f in random.Random(f"0:{split}:{cat}").sample(pool, a.per_category))
                pool = [f for f in pool if id(f) in keep]  # their load order kept
            triples += [(split, *t) for t in SP.assign_partners(pool, pool, seed=0)]
    by = collections.Counter((s, f["category"]) for s, f, _, _ in triples)
    print(f"facts per split and category: {dict(collections.Counter((f['split'], f['category']) for f in facts))}")
    print(f"items paired in the check's sample (up to {a.per_category} facts per split x category; the model's known check decides "
          "the real items; their 27B test split had 514):")
    for (s, k), v in sorted(by.items()):
        print(f"  {s:4s} {k:28s} {v}")
    collide = collections.Counter()
    fails: collections.Counter = collections.Counter()
    named: collections.Counter = collections.Counter()
    lengths: dict[str, list[int]] = collections.defaultdict(list)
    examples: dict[str, list[str]] = collections.defaultdict(list)
    n56: collections.Counter = collections.Counter()
    for t in triples:
        collide[t[1]["category"]] += SP.answer_targets(tok, t[1], t[2], t[3])["collide"]
    print(f"position checks on every sampled item: {len(triples)} items x {len(SP.CONVS)} conversations")
    for split, f, p, c in triples:
        tg = SP.answer_targets(tok, f, p, c)
        own = f["e3"]  # a stand-in round-0 answer (the runner uses the model's own)
        for conv in SP.CONVS:
            text, spans = SP.render(f, p, conv, own_answer=own)
            ids = tokens.raw_encoding(tok, text)["input_ids"]
            lengths[conv].append(len(ids))
            # 1. the answer's first token is the next token: prompt ids are a prefix of prompt + " " + e3's
            full = tokens.raw_encoding(tok, text + " " + f["e3"].strip())["input_ids"]
            if full[: len(ids)] != ids or full[len(ids)] != tg["main"]["orig"]:
                fails[f"{conv}: answer boundary"] += 1
            # 2. the final span is the composed statement and ends the prompt; the subject's last token lies in it
            lab = {s[0]: (s[1], s[2]) for s in spans}
            fs, fe = lab["final"]
            if text[fs:fe] != f["composed"] or fe != len(text):
                fails[f"{conv}: final span"] += 1
            enc = tokens.raw_encoding(tok, text, offsets=True)
            sub_end = text.lower().rfind(f["e1"].lower()) + len(f["e1"]) - 1  # case-insensitive (one TwoHopFact row differs in case)
            pos = [i for i, (x, y) in enumerate(enc["offset_mapping"]) if x <= sub_end < y]
            if not pos or not (fs <= sub_end < fe):
                fails[f"{conv}: subject position"] += 1
            # 3. the bridge is never written (their design), except where a condition writes it (hop1 / hop2)
            cond, style, n_peers, own_mode = SP.CONVS[conv]
            names_bridge = any(SP.norm(x) and f" {SP.norm(x)} " in f" {SP.norm(text[len(SP.PLAIN_HEADER) + len(SP.PLAIN_SHOTS):])} "
                               for x in f["e2_aliases"])  # fmt: skip
            if names_bridge and style not in ("hop1", "hop2"):
                named[conv] += 1  # descriptive: an alias of the bridge appears in the question or transcript
            # 4. own statement: visible -> the round-0 answer, hidden -> the placeholder, absent -> none
            if own_mode == "vis" and text[lab["own"][0] : lab["own"][1]] != SP.statement(f["composed"], own):
                fails[f"{conv}: own statement"] += 1
            if own_mode == "hid" and text[lab["own"][0] : lab["own"][1]] != SP.WITHHELD:
                fails[f"{conv}: own hidden"] += 1
            if own_mode == "abs" and "own" in lab:
                fails[f"{conv}: own absent"] += 1
            n_peer_spans = sum(k.startswith("peer") for k in lab)
            if n_peer_spans != n_peers:
                fails[f"{conv}: peers"] += 1
            if cond in ("instructed", "hypothetical") or style == "bridge":
                n56_check(tok, f, p, tg, conv, text, spans, ids, fails, n56)
            if len(examples[conv]) < a.show and f["category"] == ("landmark-cntry-capital", "person-birthcity-cntry")[len(examples[conv]) % 2]:
                examples[conv].append(f"[{f['uid']} | e2={f['e2']} e3={f['e3']} | peer e2'={p['e2']} e3'={p['e3']} | "
                                      f"control e2={c['e2']} | {len(ids)} tokens, last token {tok.decode(ids[-1:])!r}, "
                                      f"answer token {tok.decode([tg['main']['orig']])!r}, peer token {tok.decode([tg['main']['peer']])!r}]\n{text}")  # fmt: skip
    print("first-token collisions (items left out of the edited reads):", dict(collide), "of", dict(collections.Counter(f["category"] for _, f, _, _ in triples)))
    print("prompt tokens per conversation (min / median / max):",
          {k: (min(v), sorted(v)[len(v) // 2], max(v)) for k, v in lengths.items()})  # fmt: skip
    print("position checks failed:", dict(fails) or "none")
    print("prompts where an alias of the bridge appears after the worked examples (descriptive; hop1/hop2 excluded):", dict(named) or "none")
    if n56:
        print("note 56 keys (instr_vis, hyp_vis, prem_vis, prem_hid), prompts checked:", {k: v for k, v in sorted(n56.items())})
    for conv, ex in examples.items():
        for e in ex:
            print(f"\n===== {conv} {e}")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("facts")
    f.add_argument("--csv", required=True)
    f.add_argument("--handmade", required=True)
    f.add_argument("--categories", nargs="+", required=True)
    f.add_argument("--out", default="data/sd_v1/facts.jsonl")
    c = sub.add_parser("check")
    c.add_argument("--facts", default="data/sd_v1/facts.jsonl")
    c.add_argument("--show", type=int, default=2)
    c.add_argument("--per-category", type=int, default=120, help="facts per split x category paired and checked (a seeded sample)")
    a = ap.parse_args()
    {"facts": cmd_facts, "check": cmd_check}[a.cmd](a)
