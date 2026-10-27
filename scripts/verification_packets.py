"""verification_packets: the raw-row and recount sections of the hand-verification packets for findings 3-5
(verification/finding3_name_vs_digit.md, finding4_late_read.md, finding5_label_identity.md). Reads saved runs only
(no GPU, no model weights; the tokenizer from the local Hugging Face cache) and writes nothing: the markdown goes to
stdout and is pasted into the packets.

Stages:
  rows --finding 3|4|5 --run RUN [--n 20] [--seed 0] [--layer 50]
      random.Random(seed).sample(population, n) of the rows behind the finding's decisive cells, in rows.jsonl /
      outcomes.jsonl file order; each with its prompt, condition, top answer token, correct answer and label.
  headline --finding 3|4 --run RUN
      the decisive cells recounted from rows.jsonl alone (Wilson 95%), independent of d2_parts.py / attn_knockout.py:
      3  families RL and DL, layers all, the five sources of the population below, dest question and final
      4  every family, dest final, mode value, source lookup and lookup_off, layers all, attn and gdn (where run)

Populations (memory -> prompt, family RL; findings 3 and 4: items whose unedited row, source "none", is right):
  3  layers "all", dest question or final, source lookup, lookup_nodigit, lookup_noname, lookup_off_nodigit,
     lookup_off_noname (results/attn_knockout/RUN/rows.jsonl)
  4  dest final, DeltaNet mode "value", (source, layers) = (lookup or lookup_off, all or attn) or (lookup, gdn) (attn
     and gdn on the hybrid models only) (results/attn_knockout/RUN/rows.jsonl)
  5  source dissoc, group last, the layer --layer (results/pointer_swap/RUN/outcomes.jsonl; prompts from the item files
     the run's manifest pins)
Labels: findings 3-4 right (top token = the answer's, case tok_A) / list (another digit of the list, case conf_toks) /
off (anything else), as scripts/d2_parts.py; finding 5 the run's own role (none / identity / position / value /
context / ...).

uv run python scripts/verification_packets.py rows --finding 3 --run d2_parts_v2_27b
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.stats import wilson

D2 = pins.RESULTS_DIR / "attn_knockout"
PS = pins.RESULTS_DIR / "pointer_swap"
F3_SOURCES = ("lookup", "lookup_nodigit", "lookup_noname", "lookup_off_nodigit", "lookup_off_noname")
# (source, layers): every layer, every attention layer (the second draw's pre-registered cell on the hybrid), and the
# DeltaNet layers instead; attn and gdn exist on the hybrid models only
F4_CELLS = (("lookup", "all"), ("lookup_off", "all"), ("lookup", "attn"), ("lookup_off", "attn"), ("lookup", "gdn"))
F4_LAYERS = ("all", "attn", "gdn")
PROMPT_CHARS = 300
INSTRUCTION = " Answer with a single word and nothing else."  # ends every attn_knockout question line; not shown
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th"}


def jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def tokenizer_of(manifest: dict):
    """The run's own tokenizer (manifest model repo and revision), from the local cache only (a tokenizer-only cache
    is enough; snapshot_download would refuse it as incomplete)."""
    from transformers import AutoTokenizer

    m = manifest["model"]
    return AutoTokenizer.from_pretrained(m["repo"], revision=m["revision"], local_files_only=True)


def md(s: str) -> str:
    """One markdown table cell: newlines shown as ' / ', pipes escaped."""
    return s.replace("\n", " / ").replace("|", "\\|")


def short(context: str, question: str, limit: int = PROMPT_CHARS) -> str:
    """The user's text: the context cut at `limit` characters, then the question without the fixed instruction."""
    ctx = context if len(context) <= limit else context[:limit].rstrip() + " …"
    return f"{ctx} / {question.removesuffix(INSTRUCTION)}"


def user_parts(case: dict) -> tuple[str, str]:
    """(context, question line) of an attn_knockout case, from the chat prompt's user turn (the case's 'context' field
    is a character span, not text)."""
    m = re.search(r"<\|im_start\|>user\n(.*?)<\|im_end\|>", case["prompt"], re.S)
    text = m.group(1) if m else case["prompt"]
    ctx, _, q = text.rpartition("\n")
    return ctx, q


def outcome(r: dict, case: dict) -> str:
    if r["top"] == case["tok_A"]:
        return "right"
    return "list" if r["top"] in case["conf_toks"] else "off"


def unedited_right(rows: list[dict]) -> set[tuple[str, str]]:
    return {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}


def in_population(finding: int, r: dict) -> bool:
    if finding == 3:
        return r["layers"] == "all" and r["dest"] in ("question", "final") and r["source"] in F3_SOURCES
    return r["dest"] == "final" and r["mode"] == "value" and (r["source"], r["layers"]) in F4_CELLS


def d2_population(finding: int, rows: list[dict]) -> list[dict]:
    ok = unedited_right(rows)
    return [r for r in rows if r["family"] == "RL" and (r["family"], r["id"]) in ok and in_population(finding, r)]


def rows_d2(finding: int, run: str, n: int, seed: int) -> str:
    d = D2 / run
    manifest = json.loads((d / "manifest.json").read_text())
    cases = {c["id"]: c for c in jsonl(d / "cases.jsonl")}
    rows = jsonl(d / "rows.jsonl")
    pop = d2_population(finding, rows)
    pick = random.Random(seed).sample(pop, min(n, len(pop)))
    tok = tokenizer_of(manifest)
    cells = collections.Counter((r["source"], r["dest"], r["layers"]) for r in pop)
    lines = [
        f"Run `{run}` ({manifest['model']['repo']}), rows.jsonl: population {len(pop)} rows "
        f"({', '.join(f'{s}/{de}/{la} {k}' for (s, de, la), k in sorted(cells.items()))}); "
        f"`random.Random({seed}).sample(population, {n})` in file order. The prompt column is the user turn: the "
        f"list (cut at {PROMPT_CHARS} characters), then the question; the instruction {json.dumps(INSTRUCTION.strip())} "
        f"after the question and the chat template around the turn are left out. "
        f"Regenerate: `uv run python scripts/verification_packets.py rows --finding {finding} --run {run}`.",
        "",
        "| # | item id | prompt (list / question) | hidden span | from | layers | top token | answer | label | "
        "row `correct` |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(pick, 1):
        c = cases[r["id"]]
        ctx, q = user_parts(c)
        span = c["source_text"].get(r["source"], "?")
        lines.append(
            f"| {i} | {r['id']} | {md(short(ctx, q))} | `{r['source']}`: {md(json.dumps(span))} | {r['dest']} | "
            f"{r['layers']} | {md(json.dumps(tok.decode([r['top']])))} (id {r['top']}) | {c['answer']} | "
            f"{outcome(r, c)} | {str(r['correct']).lower()} |"
        )
    return "\n".join(lines)


def rows_f5(run: str, n: int, seed: int, layer: int) -> str:
    d = PS / run
    manifest = json.loads((d / "manifest.json").read_text())
    items = {it["id"]: it for pin in manifest["items"].values()
             for it in json.loads((pins.REPO_ROOT / pin["file"]).read_text())["items"]}  # fmt: skip
    pop = [r for r in jsonl(d / "outcomes.jsonl")
           if r["family"] == "RL" and r["source"] == "dissoc" and r["group"] == "last" and str(r["layer"]) == str(layer)]  # fmt: skip
    pick = random.Random(seed).sample(pop, min(n, len(pop)))
    lines = [
        f"Run `{run}` ({manifest['model']['repo']}), outcomes.jsonl: population {len(pop)} rows (family RL, source "
        f"dissoc, group last, layer {layer}); `random.Random({seed}).sample(population, {n})` in file order; prompts "
        f"from the item files pinned in the run's manifest (list cut at {PROMPT_CHARS} characters / question; the "
        f"run adds the instruction {json.dumps(INSTRUCTION.strip())} and the chat template, scripts/suite_v1.py "
        f"render). k = the place of the donor's asked statement "
        f"(item `slots.position` + 1). Regenerate: "
        f"`uv run python scripts/verification_packets.py rows --finding 5 --run {run} --layer {layer}`.",
        "",
    ]
    for i, r in enumerate(pick, 1):
        it = items[r["name"]]
        dn = it["sources"]["dissoc"]
        p = dn["predictions"]
        k, j = it["slots"]["position"] + 1, it["slots"]["identity"] + 1

        def listing(ents: list[str], digs: list[int]) -> str:
            return ", ".join(f"{e} {g}" for e, g in zip(ents, digs, strict=True))

        lines += [
            f"**{i}. {r['name']}** (topic {it['domain']}, wording {r.get('template', '-')}), k = {k}",
            f"- original: {json.dumps(short(it['context'], it['question']))} → right answer {it['answer']}; "
            f"list: {listing(it['entities'], it['digits'])}",
            f"- donor: {json.dumps(short(dn['context'], dn['question']))} → asks {dn['query']} (its {ORD[k]} "
            f"statement), answer {dn['answer']}; list: {listing(dn['entities'], dn['digits'])}",
            f"- predicted digits: none {p['none']} · position {p['position']} (the original's {ORD[k]} statement) · "
            f"identity {p['identity']} (the original's statement about {dn['query']}, its {ORD[j]}) · "
            f"value {p['value']}",
            f"- patched read (last two tokens, layer {r['layer']}): top token {json.dumps(r['top'])} → role "
            f"**{r['role']}**",
            "",
        ]
    return "\n".join(lines).rstrip()


def headline(finding: int, run: str) -> str:
    d = D2 / run
    cases = {c["id"]: c for c in jsonl(d / "cases.jsonl")}
    rows = jsonl(d / "rows.jsonl")
    ok = unedited_right(rows)
    cnt: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
    disagree = 0
    for r in rows:
        if (r["family"], r["id"]) not in ok:
            continue
        if finding == 3:
            hit = (r["family"] in ("RL", "DL") and r["layers"] == "all" and r["source"] in F3_SOURCES
                   and r["dest"] in ("question", "final"))  # fmt: skip
        else:
            hit = (r["dest"] == "final" and r["mode"] == "value" and r["source"] in ("lookup", "lookup_off")
                   and r["layers"] in F4_LAYERS)  # fmt: skip
        if hit:
            o = outcome(r, cases[r["id"]])
            disagree += (o == "right") != bool(r["correct"])
            cnt[(r["family"], r["source"], r["dest"], r["layers"])][o] += 1
    none = collections.Counter(r["family"] for r in rows if r["source"] == "none")
    lines = [
        f"Run `{run}`: items per family {dict(sorted(none.items()))}, right unedited "
        f"{dict(sorted(collections.Counter(f for f, _ in ok).items()))}; rows where right (top = tok_A) and the row's `correct` "
        f"disagree: {disagree}.",
        "",
        "| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for (f, s, de, la), c in sorted(cnt.items()):
        k = sum(c.values())
        p, lo, hi = wilson(c["right"], k)
        lines.append(f"| {f} | {s} | {de} | {la} | {k} | {c['right']} | {100 * p:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}] | "
                     f"{100 * c['list'] / k:.0f}% | {100 * c['off'] / k:.0f}% |")  # fmt: skip
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["rows", "headline"])
    ap.add_argument("--finding", type=int, choices=[3, 4, 5], required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--layer", type=int, default=50, help="finding 5: the layer the run's verdict used")
    a = ap.parse_args()
    if a.stage == "headline":
        assert a.finding in (3, 4), "finding 5's recount is scripts/finding5_confirm.py (with --out)"
        print(headline(a.finding, a.run))
    elif a.finding == 5:
        print(rows_f5(a.run, a.n, a.seed, a.layer))
    else:
        print(rows_d2(a.finding, a.run, a.n, a.seed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
