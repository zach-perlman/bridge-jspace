"""natural_read: finding 4 (the late read) on natural text, lens-free (Dan, 23 Oct; docs/design_natural_late_read.md).

Items. SQuAD v1.1 dev (pins.SQUAD_DEV_*; CC BY-SA 4.0): a Wikipedia paragraph, a question and the answer's span. The
prompt is the paragraph, a newline, the question and INSTRUCTION as one user turn (chat.chat_text, "Answer:"
prefilled). The paragraph is cut into sentences (split_sentences); "the answer's sentence" is the one holding the
answer's span. Kept (tokenizer-free, so every model gets the same items): the answer (a leading article dropped)
starts with a letter at a word start and has at most MAX_WORDS words; every annotator's answer starts with the same
word; no other word of paragraph and question shares that word's first PREFIX letters (instance / instances), so a
right first token can only come from the answer's sentence; paragraphs of 4 or more sentences and at most MAX_CHARS
characters; an answer's sentence of at least MIN_SENT_WORDS words that a random span of its length fits beside; an
off-path sentence (two or more sentences away, character length within OFF_RATIO of the answer's, the closest, seeded
tie-break); one question per paragraph (seeded); a swap partner (another article's item whose paragraph has no word
with that prefix) for the swapped-paragraph baseline. Items in a seeded order. Per tokenizer (attn_knockout's builder):
an answer whose first token is under 3 characters and not its whole first word is left out (short_first_token).

Prompts per item (competence): full; alone (the answer's sentence alone); deleted (the paragraph without it); swapped
(the partner's paragraph, this question). Read: the answer's first token after "Answer:" is the top token (one
forward); full also greedy (GREEDY_TOKENS), judged right if a gold answer's normalised text is in the first line's.
Eligible for the knockout run (ELIGIBILITY): full right on both reads, alone right, deleted wrong.

Stages:
  make                              data/natural_read_v1/items.json from the pinned raw file (cache/, sha256-checked)
  dryrun [--k 3]                    CPU, tokenizer only (BJ_TARGET): every case built, counts, k examples (seed 0)
  manifest --name N --why W         results/natural_read/<N>/manifest.json, before the competence run
  competence --name N               GPU: items.jsonl (four prompts per item) and summary.json (with eligibility_funnel:
                                    built -> eligible, and why each item is dropped)
  verdict --run R --competence N    CPU: the rule (judge; primary and secondary bar, BARS) on attn_knockout run R -> a
                                    new results/attn_knockout/<R>/analysis-<stamp>-verdict/ (verdict.json, .md, figure)
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import re
import string
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins

EXP = "natural_read"
RESULTS = pins.RESULTS_DIR / EXP
INSTRUCTION = "Answer with a few words copied from the text and nothing else."
FAMILY = "NAT"  # the knockout run's family code: a question naming what to look up in a natural paragraph
MAX_WORDS, MAX_CHARS, MIN_SENTS, MIN_SENT_WORDS = 4, 1200, 4, 5
OFF_RATIO, RANDOM_FIT, PREFIX = (0.75, 1.33), 0.8, 5
SEED, GREEDY_TOKENS = 0, 12
ARTICLES = ("the ", "a ", "an ")
# no sentence ends after these (lower case, without the period); single letters (initials) and words with an inner
# period (U.S., D.C.) never end one either
ABBREV = frozenset({
    "mr", "mrs", "ms", "dr", "prof", "rev", "st", "jr", "sr", "gen", "gov", "sen", "rep", "lt", "col", "capt", "sgt",
    "mt", "no", "nos", "vs", "etc", "inc", "ltd", "co", "corp", "bros", "jan", "feb", "mar", "apr", "jun", "jul", "aug",
    "sep", "sept", "oct", "nov", "dec", "fig", "approx", "est", "ca", "vol", "pp", "ed", "eds", "op", "cf", "al",
})  # fmt: skip
_END = re.compile(r"[.!?][\"')\]]*\s+")


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Char spans [start, end) of the sentences of a paragraph, whitespace excluded: a break after . ! or ? (and
    closing quotes or brackets) followed by whitespace and an upper-case letter, a digit or an opening quote; never
    after an abbreviation (ABBREV), a single letter or a word with an inner period."""
    spans, start = [], 0
    for m in _END.finditer(text):
        nxt = m.end()
        if nxt >= len(text) or not (text[nxt].isupper() or text[nxt].isdigit() or text[nxt] in "\"'(["):
            continue
        if text[m.start()] == ".":
            prev = re.search(r"(\S+)$", text[start : m.start()])
            word = prev.group(1).lower().lstrip("\"'([") if prev else ""
            if word in ABBREV or len(word) == 1 or "." in word:
                continue
        spans.append((start, m.start() + len(m.group().rstrip())))
        start = nxt
    end = len(text.rstrip())
    if start < end:
        spans.append((start, end))
    return spans


def normalise(s: str) -> str:
    """SQuAD's answer normalisation: lower case, no punctuation, no articles, single spaces."""
    s = "".join(ch for ch in s.lower() if ch not in set(string.punctuation))
    return " ".join(w for w in s.split() if w not in ("a", "an", "the"))


def content(passage: str, question: str) -> str:
    """The user turn: the paragraph, a newline, the question and INSTRUCTION."""
    return f"{passage}\n{question} {INSTRUCTION}"


def deleted_passage(item: dict) -> str:
    """The paragraph without the answer's sentence (the text-level counterpart of hiding it)."""
    a, b = item["sentences"][item["answer_sentence"]]
    p = item["passage"]
    return f"{p[:a].rstrip()} {p[b:].lstrip()}".strip()


def short_first_token(tok, item: dict) -> bool:
    """The answer's first token (after 'Answer:', with its space) has under 3 characters and is not its whole first
    word: a token that many other words begin with, so a wrong answer could score right on it."""
    first = tok.decode(tok(" " + item["answer"], add_special_tokens=False).input_ids[:1]).strip()
    return len(first) < 3 and first.lower() != item["first_word"].lower()


KINDS = ("full", "alone", "deleted", "swapped")


def prompt_contents(item: dict, by_id: dict[str, dict]) -> dict[str, str]:
    """The user turns of an item's competence prompts: the paragraph (full), the answer's sentence alone (alone), the
    paragraph without it (deleted), another article's paragraph (swapped), each with the item's question."""
    a, b = item["sentences"][item["answer_sentence"]]
    return {"full": content(item["passage"], item["question"]),
            "alone": content(item["passage"][a:b], item["question"]),
            "deleted": content(deleted_passage(item), item["question"]),
            "swapped": content(by_id[item["swap_partner"]]["passage"], item["question"])}  # fmt: skip


def greedy_right(text: str, answers: list[str]) -> bool:
    """A gold answer's normalised text inside the normalised first non-empty line of a greedy continuation."""
    line = next((ln for ln in text.split("\n") if ln.strip()), "")
    said = normalise(line)
    return any(g and g in said for g in map(normalise, answers))


ELIGIBILITY = ("full: first token right and greedy right; alone: first token right (the answer's sentence suffices); "
               "deleted: first token wrong (the answer needs that sentence)")  # fmt: skip


def eligible_ids(rows: list[dict]) -> set[str]:
    """Items eligible for the knockout run, from a competence run's items.jsonl rows (ELIGIBILITY)."""
    by: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        by[r["id"]][r["kind"]] = r
    return {i for i, k in by.items() if k["full"]["right"] and k["full"]["greedy_right"] and k["alone"]["right"]
            and not k["deleted"]["right"]}  # fmt: skip


COVERAGE = ("Not covered: items whose answer needs a neighbouring sentence (a pronoun's antecedent, a subject named "
            "earlier) fail 'the answer's sentence alone' and are dropped, so the verdict is about answers that one "
            "sentence gives on its own.")  # fmt: skip
CRITERIA = (  # the knockout run's eligibility, in the order the funnel applies it: (why an item is dropped, its test)
    ("the answer's first token is under 3 characters and not its whole first word", lambda k: not k["short"]),
    ("with the paragraph, the answer's first token is not on top", lambda k: k["full"]["right"]),
    ("with the paragraph, the greedy answer is wrong", lambda k: k["full"]["greedy_right"]),
    ("the answer's sentence alone is not enough (first token not on top)", lambda k: k["alone"]["right"]),
    ("without the answer's sentence the first token is still on top (answered without it)",
     lambda k: not k["deleted"]["right"]),
)  # fmt: skip


def eligibility_funnel(rows: list[dict], short: set[str]) -> dict:
    """Built -> eligible on one model (Dan, 23 Oct): the items left after each criterion in CRITERIA's order, how many
    each drops there, and how many fail each criterion on its own; `short` the items short_first_token drops."""
    by: dict[str, dict[str, Any]] = collections.defaultdict(lambda: {"short": False})
    for r in rows:
        by[r["id"]][r["kind"]] = r
    for i in short & set(by):
        by[i]["short"] = True
    left = set(by)
    steps, alone = [], {}
    for why, keep in CRITERIA:
        dropped = {i for i in left if not keep(by[i])}
        left -= dropped
        steps.append({"dropped_by": why, "dropped": len(dropped), "left": len(left)})
        alone[why] = sum(not keep(k) for k in by.values())
    return {"built": len(by), "eligible": len(left), "steps": steps, "failing_each_criterion_alone": alone,
            "coverage": COVERAGE}  # fmt: skip


def competence_rows(run: str) -> list[dict]:
    return [json.loads(x) for x in (RESULTS / run / "items.jsonl").read_text().splitlines()]


def strip_article(s: str) -> str:
    s = s.strip()
    for art in ARTICLES:
        if s.lower().startswith(art):
            return s[len(art) :].lstrip()
    return s


def word_key(word: str) -> str:
    """A word's first PREFIX letters, lower case: words sharing it count as one (instance / instances)."""
    return word.lower()[:PREFIX]


def candidate(passage: str, sents: list[tuple[int, int]], q: dict, rng: random.Random) -> dict | None:
    """One SQuAD question as an item (without id and swap partner), or None if a filter drops it (module docstring)."""
    gold = q["answers"][0]
    ans = strip_article(gold["text"])
    start = gold["answer_start"] + gold["text"].index(ans)
    if not ans or not ans[0].isalpha() or len(ans.split()) > MAX_WORDS or passage[start : start + len(ans)] != ans:
        return None
    if start > 0 and passage[start - 1].isalnum():  # the span starts inside a word
        return None
    first = re.match(r"\w+", ans)
    assert first
    key = word_key(first.group())
    golds = [re.match(r"\w+", strip_article(x["text"])) for x in q["answers"]]
    if not all(g and word_key(g.group()) == key for g in golds):  # every annotator's answer starts with that word
        return None
    if sum(word_key(w) == key for w in re.findall(r"\w+", passage + " " + q["question"])) != 1:
        return None
    i = next((k for k, (a, b) in enumerate(sents) if a <= start and start + len(ans) <= b), None)
    if i is None:
        return None
    a, b = sents[i]
    if len(passage[a:b].split()) < MIN_SENT_WORDS or b - a > RANDOM_FIT * max(a, len(passage) - b):
        return None
    size = b - a
    offs = [k for k, (c, d) in enumerate(sents) if abs(k - i) >= 2 and OFF_RATIO[0] <= (d - c) / size <= OFF_RATIO[1]]
    if not offs:
        return None
    best = min(abs((sents[k][1] - sents[k][0]) - size) for k in offs)
    j = rng.choice([k for k in offs if abs((sents[k][1] - sents[k][0]) - size) == best])
    return {"squad_id": q["id"], "question": q["question"].strip(), "answer": ans, "answer_char": [start, start + len(ans)],
            "first_word": first.group(), "answers": sorted({x["text"].strip() for x in q["answers"]}),
            "answer_sentence": i, "off_sentence": j}  # fmt: skip


def build(raw: dict, seed: int = SEED) -> tuple[list[dict], dict]:
    """The items from SQuAD's JSON (module docstring) and the count left after each filter."""
    rng = random.Random(seed)
    counts: collections.Counter = collections.Counter()
    items = []
    for art in raw["data"]:
        for k, par in enumerate(art["paragraphs"]):
            passage = par["context"].strip()
            counts["paragraphs"] += 1
            counts["questions"] += len(par["qas"])
            sents = split_sentences(passage)
            if len(sents) < MIN_SENTS or len(passage) > MAX_CHARS or "\n" in passage:
                continue
            counts["paragraphs_kept"] += 1
            kept = [c for q in par["qas"] if (c := candidate(passage, sents, q, rng))]
            counts["questions_kept"] += len(kept)
            if kept:
                items.append({"article": art["title"], "paragraph": k, "passage": passage,
                              "sentences": [list(s) for s in sents], **rng.choice(kept)})  # fmt: skip
    rng.shuffle(items)
    for n, it in enumerate(items):
        it["id"] = f"NAT-{n:04d}"
    for it in items:  # the swapped-paragraph baseline: another article's paragraph without the answer's first word
        key = word_key(it["first_word"])
        pool = [o["id"] for o in items if o["article"] != it["article"]
                and not any(word_key(w) == key for w in re.findall(r"\w+", o["passage"]))]  # fmt: skip
        it["swap_partner"] = rng.choice(pool)
    counts["items"] = len(items)
    counts["articles"] = len({it["article"] for it in items})
    return items, dict(counts)


def stage_make() -> None:
    out = pins.NATURAL_READ_FILE
    assert not out.exists(), f"{out} exists; data files are written once"
    blob = pins.SQUAD_DEV_FILE.read_bytes() if pins.SQUAD_DEV_FILE.exists() else b""
    got = hashlib.sha256(blob).hexdigest()
    assert got == pins.SQUAD_DEV_SHA256, (
        f"{pins.SQUAD_DEV_FILE}: sha256 {got}; download {pins.SQUAD_DEV_URL} there first"
    )
    items, counts = build(json.loads(blob))
    meta = {"source": {"url": pins.SQUAD_DEV_URL, "sha256": pins.SQUAD_DEV_SHA256, "license": "CC BY-SA 4.0",
                       "citation": "Rajpurkar et al. 2016, SQuAD: 100,000+ Questions for Machine Comprehension of Text"},
            "generator": f"scripts/natural_read.py make (seed {SEED})", "doc": (__doc__ or "").split("\n\n")[1],
            "instruction": INSTRUCTION, "counts": counts}  # fmt: skip
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "items": items}, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out, json.dumps(counts))


def cached_tokenizer():
    """The target's tokenizer at its pinned revision; on a machine holding only the tokenizer files of that revision
    (a partial snapshot, which snapshot_download refuses offline), loaded from those files."""
    from huggingface_hub import try_to_load_from_cache
    from transformers import AutoTokenizer

    from bridge_jspace.tokens import load_tokenizer

    try:
        return load_tokenizer()
    except Exception as e:  # any snapshot error: fall back to the cached files of the same revision
        hit = try_to_load_from_cache(pins.MODEL_REPO, "tokenizer_config.json", revision=pins.MODEL_REVISION)
        if not isinstance(hit, str):
            raise FileNotFoundError(f"{pins.MODEL_REPO}@{pins.MODEL_REVISION}: no cached tokenizer") from e
        print(f"tokenizer from the cached files of {pins.MODEL_REPO}@{pins.MODEL_REVISION[:8]} (partial snapshot)")
        return AutoTokenizer.from_pretrained(Path(hit).parent)


def stage_dryrun(k: int) -> None:
    """Tokenizer only: every item as an attn_knockout case and every competence prompt, with counts and k examples."""
    import statistics

    from bridge_jspace.tokens import raw_encoding
    from scripts import attn_knockout as AK

    tok = cached_tokenizer()
    items = pins.natural_read_items()
    by_id = {it["id"]: it for it in items}
    cases, report = AK.build_natural_cases(tok, len(items), "none", None)
    lens = {kind: [len(raw_encoding(tok, chat.chat_text(tok, c))["input_ids"]) for it in items
                   for kd, c in prompt_contents(it, by_id).items() if kd == kind] for kind in KINDS}  # fmt: skip
    n_ans = [len(c["sources"]["lookup"]) for c in cases]
    ratio = [len(c["sources"]["lookup_off"]) / len(c["sources"]["lookup"]) for c in cases]
    final = cases[0]["dests"]["final"]
    out = {"target": pins.TARGET, "items": len(items), "cases": len(cases), "report": report,
           "articles": len({it["article"] for it in items}),
           "prompt_tokens(min,median,max)": {kd: (min(v), statistics.median(v), max(v)) for kd, v in lens.items()},
           "answer_sentence_tokens(min,median,max)": (min(n_ans), statistics.median(n_ans), max(n_ans)),
           "off/answer_token_ratio(quartiles)": [round(x, 3) for x in statistics.quantiles(ratio, n=4)],
           "off_same_token_length": sum(c["source_flags"]["lookup_off"] == "same_length" for c in cases),
           "last_tokens": {"n": len(final), "text": [tok.decode([cases[0]["ids"][i]]) for i in final]},
           "answer_sentence_position": dict(collections.Counter(
               "first" if c["query_slot"] == 0 else "last" if c["query_slot"] == len(c["statements"]) - 1 else "middle"
               for c in cases))}  # fmt: skip
    print(json.dumps(out, indent=1, ensure_ascii=False))
    for c in random.Random(SEED).sample(cases, k):
        it = by_id[c["id"]]
        print(f"\n--- {c['id']} ({it['article']}), {len(c['ids'])} tokens")
        print("question:", it["question"], "| answer:", it["answer"], "| gold:", it["answers"],
              f"| first token {tok.decode([c['tok_A']])!r}")  # fmt: skip
        print(f"answer's sentence ({len(c['sources']['lookup'])} tokens):", c["source_text"]["lookup"])
        print(f"off-path sentence ({len(c['sources']['lookup_off'])} tokens):", c["source_text"]["lookup_off"])
        print("deleted paragraph:", deleted_passage(it))
        print("swapped paragraph (start):", by_id[it["swap_partner"]]["passage"][:120], "...")
        print("prompt:", repr(c["prompt"]))


def stage_manifest(name: str, why: str) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    f = pins.NATURAL_READ_FILE
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "items": {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)},
         "format": f"{chat.format_note()}; the user turn: paragraph, newline, question, '{INSTRUCTION}'",
         "prompts": {"full": "the paragraph", "alone": "the answer's sentence alone", "deleted": "the paragraph "
                     "without the answer's sentence", "swapped": "another article's paragraph (the item's swap_partner)"},
         "read": "one forward per prompt: right iff the answer's first token (after 'Answer:', with its space) is the "
         "top token (suite_v1.read_answers' margin > 0)",
         "greedy": f"full only: {GREEDY_TOKENS} new tokens; right iff a gold answer's normalised text (SQuAD's "
         "normalisation) is inside the normalised first non-empty line",
         "eligibility": ELIGIBILITY}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    import os

    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.stats import wilson
    from bridge_jspace.tokens import raw_encoding
    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "items.jsonl").exists(), f"{out_dir} has results; runs are written once"
    chat.check_format(m)
    assert sha256_of(pins.REPO_ROOT / m["items"]["file"]) == m["items"]["sha256"], "items changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    items = pins.natural_read_items()
    by_id = {it["id"]: it for it in items}
    prompts = [{"id": it["id"], "kind": kind, "expected": it["answer"], "answer_kind": "word", "answers": it["answers"],
                "ids": raw_encoding(tok, chat.chat_text(tok, c))["input_ids"]}
               for it in items for kind, c in prompt_contents(it, by_id).items()]  # fmt: skip
    S.read_answers(model, tok, prompts)
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        p["right"] = p["margin"] > 0
        if p["kind"] == "full":
            by_len[len(p["ids"])].append(p)
    step = int(os.environ.get("BJ_GEN_BATCH", "64"))
    chunks = [g[s : s + step] for g in by_len.values() for s in range(0, len(g), step)]
    for chunk in progress(chunks, desc="greedy"):
        texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), GREEDY_TOKENS, [{}] * len(chunk))  # fmt: skip
        for p, text in zip(chunk, texts, strict=True):
            p["continuation"], p["greedy_right"] = text, greedy_right(text, p["answers"])
    rows = [
        {k: v for k, v in p.items() if k not in ("ids", "forced", "answers")} | {"tokens": len(p["ids"])}
        for p in prompts
    ]
    write_jsonl(out_dir / "items.jsonl", rows)
    short = {it["id"] for it in items if short_first_token(tok, it)}
    ok = eligible_ids(rows) - short
    summary = {"run": name, "items": len(items), "seconds": round(time.time() - t0),
               "first_token_right": {kd: wilson(sum(r["right"] for r in rows if r["kind"] == kd), len(items)) for kd in KINDS},
               "greedy_right_full": wilson(sum(bool(r.get("greedy_right")) for r in rows), len(items)),
               "eligible": len(ok), "eligibility": ELIGIBILITY, "eligibility_funnel": eligibility_funnel(rows, short),
               "swapped_right_on_eligible": wilson(sum(r["right"] for r in rows if r["kind"] == "swapped" and r["id"] in ok), len(ok))}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


# ---- verdict (CPU, saved rows only) ----------------------------------------------------------------------------------

N_MIN, FLOOR_MAX = 100, 0.10  # fewer eligible items: not testable; the floor above FLOOR_MAX: not interpretable
# The bar on the answer's sentence hidden from the last tokens: (point, Wilson upper bound). Primary (Dan, 23 Oct,
# before any run): 10% / 20%, as the floor here is ~0, not chance. Secondary: finding 4's bar (scripts/d2_formats.py
# LATE_MAX, LATE_HI), reported for comparability with the grid. The controls are the same under both.
BARS = {"primary": (0.10, 0.20), "secondary": (0.20, 0.30)}


def cell(rows: list[dict], ok: set[str], source: str, dest: str, layers: str, mode: str = "value") -> dict:
    """Rate right (first token) on the items in `ok`, with its Wilson interval, per item outcomes and n."""
    from bridge_jspace.stats import wilson

    got = {r["id"]: r["correct"] for r in rows if r["id"] in ok and r["source"] == source and r["dest"] == dest
           and r["layers"] == layers and r["mode"] == mode}  # fmt: skip
    return {"rate": wilson(sum(got.values()), len(got)), "n": len(got), "per_item": got}


def judge(cells: dict[str, dict], n: int, bar: tuple[float, float] = BARS["primary"]) -> str:
    """The pre-registered rule (docs/design_natural_late_read.md) under one bar (BARS); the controls are finding 4's
    (scripts/d2_formats.py: another sentence >= 90% with lower bound >= 85%; the DeltaNet layers instead >= 90%)."""
    from scripts import d2_formats as DF

    late, off, gdn, floor = (cells[k]["rate"] for k in ("late", "off", "deltanet", "floor"))
    if n < N_MIN:
        return f"not testable (competence: {n} < {N_MIN} items right unedited)"
    if floor[0] > FLOOR_MAX:
        return (
            f"not interpretable (the answer's sentence hidden from everything after it leaves > {FLOOR_MAX:.0%} right)"
        )
    if not (off[0] >= DF.OFF_MIN and off[1] >= DF.OFF_LO):
        return "not interpretable (the off-path control: another sentence hidden keeps < 90% or its lower bound < 85%)"
    late_ok = late[0] <= bar[0] and late[2] <= bar[1]
    gdn_ok = cells["deltanet"]["n"] == 0 or gdn[0] >= DF.GDN_MIN
    if late_ok and gdn_ok:
        return "holds"
    if late_ok:
        return "fails (the DeltaNet layers matter: blocking them instead keeps < 90%)"
    return f"fails (more than {bar[0]:.0%} right, or the upper bound above {bar[1]:.0%})"


def verdict(rows: list[dict], cases: dict[str, dict], comp: list[dict]) -> dict:
    """The rule and the reported cells of one attn_knockout run on natural_read items (items right unedited)."""
    from bridge_jspace.stats import cluster_bootstrap, wilson

    ok = {r["id"] for r in rows if r["source"] == "none" and r["correct"]}
    hybrid = any(r["layers"] == "gdn" for r in rows)
    att = "attn" if hybrid else "all"
    cells = {"late": cell(rows, ok, "lookup", "final", att), "off": cell(rows, ok, "lookup_off", "final", att),
             "deltanet": cell(rows, ok, "lookup", "final", "gdn"),
             "floor": cell(rows, ok, "lookup", "after", "all", "absent" if hybrid else "value"),
             "off_floor": cell(rows, ok, "lookup_off", "after", "all", "absent" if hybrid else "value"),
             "question": cell(rows, ok, "lookup", "question", "all")}  # fmt: skip
    swapped = [r["right"] for r in comp if r["kind"] == "swapped" and r["id"] in ok]
    ids = sorted(cells["late"]["per_item"])
    partner = ids[1:] + ids[:1]  # a fixed derangement (sorted ids, shifted by one): the answer key of another item
    late_top = {r["id"]: r["top"] for r in rows if r["id"] in ok and r["source"] == "lookup" and r["dest"] == "final"
                and r["layers"] == att and r["mode"] == "value"}  # fmt: skip
    chance = [late_top[i] == cases[p]["tok_A"] for i, p in zip(ids, partner, strict=True)]
    vals = [float(cells["late"]["per_item"][i]) for i in ids]
    out = {"n_items": len({r["id"] for r in rows if r["source"] == "none"}), "n_right_unedited": len(ok),
           "layers_for_late": att, "hybrid": hybrid,
           "cells": {k: {"rate": v["rate"], "n": v["n"]} for k, v in cells.items()},
           "baselines": {"swapped_paragraph_unedited": wilson(sum(swapped), len(swapped)),
                         "late_scored_against_another_items_answer": wilson(sum(chance), len(chance))},
           "late_article_cluster_ci": cluster_bootstrap(vals, [cases[i]["domain"] for i in ids], n_boot=4000, seed=0) if vals else None}  # fmt: skip
    out["bars"] = BARS
    out["verdict"] = judge(cells, len(ok), BARS["primary"])
    out["verdict_secondary"] = judge(cells, len(ok), BARS["secondary"])
    return out


def stage_verdict(run: str, competence: str) -> None:
    from scripts import attn_knockout as AK

    d = AK.RESULTS / run
    rows = [json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()]
    cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
    m = json.loads((d / "manifest.json").read_text())
    funnel = json.loads((RESULTS / competence / "summary.json").read_text())["eligibility_funnel"]
    out = {"run": run, "competence": competence, "model": m["model"], **verdict(rows, cases, competence_rows(competence)),
           "eligibility_funnel": funnel}  # fmt: skip
    dest = d / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-verdict"  # new: the job page's figures
    dest.mkdir(parents=True)
    (dest / "verdict.json").write_text(json.dumps(out, indent=1) + "\n")
    (p1, h1), (p2, h2) = BARS["primary"], BARS["secondary"]
    lines = [f"# natural_read / {run}", "",
             f"Verdict (primary, <= {p1:.0%} right with the upper bound <= {h1:.0%}): **{out['verdict']}**", "",
             f"Verdict (secondary, finding 4's bar <= {p2:.0%} / <= {h2:.0%}): {out['verdict_secondary']}", "",
             f"Items: {funnel['built']} built -> {funnel['eligible']} eligible (competence run {competence}) -> "
             f"{out['n_items']} in the knockout run, {out['n_right_unedited']} right unedited there.", "",
             "| dropped because | dropped at this step | left | failing this criterion on its own |", "|---|---|---|---|",
             *[f"| {s['dropped_by']} | {s['dropped']} | {s['left']} | {funnel['failing_each_criterion_alone'][s['dropped_by']]} |"
               for s in funnel["steps"]],
             "", funnel["coverage"], "", "| cell | right [95% Wilson] | n |", "|---|---|---|"]  # fmt: skip
    for k, v in [*out["cells"].items(), *out["baselines"].items()]:
        r = v["rate"] if isinstance(v, dict) else v
        lines.append(f"| {LABELS.get(k, k)} | {pct(r)} | {v['n'] if isinstance(v, dict) else '-'} |")
    (dest / "verdict.md").write_text("\n".join(lines) + "\n")
    figure(out, dest / "natural_late_read.png")
    print("\n".join(lines))
    print("wrote", dest)


LABELS = {
    "late": "answer's sentence hidden from the last tokens",
    "off": "another sentence hidden from the last tokens (control)",
    "deltanet": "answer's sentence hidden from the last tokens, DeltaNet layers only (control)",
    "floor": "answer's sentence hidden from everything after it (floor)",
    "off_floor": "another sentence hidden from everything after it",
    "question": "answer's sentence hidden from the question words",
    "swapped_paragraph_unedited": "baseline: the question after another article's paragraph",
    "late_scored_against_another_items_answer": "baseline: blocked answers scored against another item's answer",
}


def pct(r: Any) -> str:
    return "-" if r[0] != r[0] else f"{100 * r[0]:.0f}% [{100 * r[1]:.0f}, {100 * r[2]:.0f}]"


def figure(out: dict, path: Path) -> None:
    """One row per cell: % right with its Wilson interval; the test cell in the effect colour, controls and baselines
    in greys (attn_knockout's validated SERIES colours); the bars (primary 10%, secondary 20%, controls 90%) as dashed
    lines; both verdicts and built -> eligible in the caption."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace import plotting as P

    keys = [k for k in ("late", "question", "floor", "off", "deltanet", "off_floor") if out["cells"][k]["n"]]
    rows = [(LABELS[k], out["cells"][k]["rate"], out["cells"][k]["n"], k) for k in keys]
    rows += [(LABELS[k], v, None, k) for k, v in out["baselines"].items() if v[0] == v[0]]
    colour = {"late": "#2a78d6", "question": "#2a78d6", "floor": "#2a78d6"}
    fig, ax = plt.subplots(figsize=(8.6, 0.42 * len(rows) + 3.4))
    for y, (_, r, n, k) in enumerate(reversed(rows)):
        c = colour.get(k, "#5f5e59" if k in out["cells"] else "#7f7d77")
        ax.errorbar([r[0]], [y], xerr=[[r[0] - r[1]], [r[2] - r[0]]], fmt="o" if k in out["cells"] else "s", ms=7,
                    color=c, ecolor=c, elinewidth=1.6, capsize=0)  # fmt: skip
        right = r[0] > 0.8  # labels of points near 100% go to their left, inside the panel
        ax.annotate(f"{100 * r[0]:.0f}%" + (f"  n={n}" if n else ""), (r[0], y), xytext=(-8 if right else 8, 6),
                    textcoords="offset points", fontsize=8, color=P.MUTED, ha="right" if right else "left")  # fmt: skip
    ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=8.5)
    ax.set_ylim(-0.6, len(rows) + 0.2)  # headroom above the top row for the bars' labels (two lines)
    (p1, _), (p2, _) = BARS["primary"], BARS["secondary"]
    for x, lab, ha, dy in ((p1, f"primary bar: ≤ {p1:.0%}", "left", -2),
                           (p2, f"secondary (finding 4's) bar: ≤ {p2:.0%}", "left", -13),
                           (0.90, "control bar: ≥ 90%", "right", -2)):  # fmt: skip
        ax.axvline(x, color=P.AXIS, ls="--", lw=1)
        ax.annotate(lab, (x, 1), xycoords=("data", "axes fraction"), xytext=(3 if ha == "left" else -3, dy),
                    textcoords="offset points", fontsize=7.5, color=P.MUTED, va="top", ha=ha)  # fmt: skip
    ax.set_xlim(0, 1.04)
    ax.set_xlabel("% of items still right (the answer's first token)", color=P.MUTED, fontsize=9)
    P.style_axes(ax)
    P.percent_axis(ax, "x")
    model = out["model"]["repo"].split("/")[-1]
    f = out.get("eligibility_funnel")
    built = f"{f['built']} items built, {f['eligible']} eligible; " if f else ""
    P.finish(fig, path, f"{model}: does the answer need a late read of its sentence in a real paragraph?", "",
             explain=[("What we did", "SQuAD paragraphs and questions; stopped the last tokens before the answer (the "
                       "chat template and 'Answer:') from attending to the sentence holding the answer, in every "
                       "attention layer, and counted answers still right."),
                      ("Example", "\"... teachers who have a positive disposition towards the course content tend to "
                       "transfer their passion to receptive students. ...\" What gets transferred to students who are "
                       "receptive to the teacher? Answer: passion (item NAT-0050)"),
                      ("How to read", "blue: the answer's sentence hidden; grey: another sentence of about the same "
                       "length hidden, or the DeltaNet layers instead of attention; squares: baselines with nothing "
                       "hidden. Lines: 95% Wilson intervals."),
                      ("Verdict", f"primary bar ≤ {p1:.0%} (upper bound ≤ {BARS['primary'][1]:.0%}): "
                       f"{out['verdict']}; secondary, finding 4's bar ≤ {p2:.0%} (upper bound ≤ "
                       f"{BARS['secondary'][1]:.0%}), for comparison: {out['verdict_secondary']}."),
                      ("Data", f"{model}; {built}{out['n_right_unedited']} items right unedited of {out['n_items']} "
                       "(one question per paragraph; right from the answer's sentence alone, wrong without it; "
                       "answers that need a neighbouring sentence are not covered).")])  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "dryrun", "manifest", "competence", "verdict"])
    ap.add_argument("--name", help="manifest, competence: the competence run")
    ap.add_argument("--why")
    ap.add_argument("--run", help="verdict: the attn_knockout run")
    ap.add_argument("--competence", help="verdict: the competence run")
    ap.add_argument("--k", type=int, default=3, help="dryrun: examples shown")
    a = ap.parse_args()
    if a.stage == "make":
        stage_make()
    elif a.stage == "dryrun":
        stage_dryrun(a.k)
    elif a.stage == "manifest":
        assert a.name, "manifest needs --name"
        assert a.why, "manifest needs --why"
        stage_manifest(a.name, a.why)
    elif a.stage == "competence":
        assert a.name, "competence needs --name"
        stage_competence(a.name)
    else:
        assert a.run, "verdict needs --run"
        assert a.competence, "verdict needs --competence"
        stage_verdict(a.run, a.competence)
