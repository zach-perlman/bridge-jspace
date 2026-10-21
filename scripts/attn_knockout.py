"""attn_knockout (D2, Dan's depth track; Zach's sprint plan, 2026-10-20): which positions must read which statement
directly, and at which layers, for an in-prompt lookup to work, compared with a recall from memory?

Question. Block the direct reads of a statement span S by a set of destination positions D at a set of layers
(bridge_jspace.knockout: exact edge knock-out; full attention: the (D, S) logits at -inf; Gated DeltaNet: D's output
from a second run of the token mixer with S's values zeroed and S's conv taps dropped from the value channels, every
key, beta and decay kept, i.e. exactly the s -> t terms of o_t = sum_j w_tj v_j removed; indirect routes through other
positions stay open; the first token is never blocked). Does RL (recalled bridge -> in-prompt lookup) break while RR (recalled bridge -> recall from memory)
survives? At which layers and to which destinations must the lookup statement be visible, compared with where the
bridge is in transit (suite_split on Qwen3.6-27B: copying C's question-group residual flips RL 98-100% at layers 44-52)
and where the J-lens cannot write it (read_write: RL never written at 32-52)?

Items. suite_v1 wording A: BL, BR, RL, RR (the same scenes), BLR, BRL (the same scenes), countries R and B
(data/bind_recall.json, exp09's chat_prefill). Eligibility (default): the first n cases per family of suite_split's
map_A8_v1 and control_split's map_v1 (every competence prompt right; seed-0 samples), so the scenes are those of the
copy-split runs. An item counts only if its unedited read is right (its 'none' row). --no-eligibility (smokes): the
first n items per family, all counted.

Sources (the token span of one sentence; seeded choices per scene, seed recorded):
  lookup       the path's lookup statement: "The cow's locker is 5." (BL/BR/RL/RR), "The cow's friend is a spider."
               (BLR), "Animals with 4 legs use locker 7." (BRL). On the path of BL, RL, BLR, BRL; off it for BR, RR
  binding      the bridge's binding statement "Jack's pet is a cow." (countries: "Emma lives in Egypt."). On the path of
               BL, BR, BLR, BRL, country-B; off it for RL, RR and country-R (there it only names the bridge)
  lookup_off   control: another statement of the lookup's kind with the same token length
  binding_off  control: another binding statement with the same token length
  random       control: a contiguous context span of the lookup's length (countries: the binding's), overlapping
               neither path statement
  trailing     control: the up-to-3 context tokens right after the lookup statement (countries: the binding), the
               conv's reach: what blocking those alone does (the DeltaNet conv mixes S into their keys and values)
Destinations: question (the question sentence and the instruction), final (everything after the user turn:
  <|im_end|>, the assistant header, the empty think block, 'Answer:' and a digit answer's space), both, after (every
  position after the source: the positive control; the statement then reaches the answer by no direct route).
Layer sets (manifest --layers): all; win8 / win4 (8-layer windows at stride 8 / 4: 2 full-attention + 6 DeltaNet
  layers each); win8k (each stride-8 window, and its 2 full-attention layers alone (:attn) and its 6 DeltaNet layers
  alone (:gdn)); pre ([0, L)) and suf ([L, N)) for L in steps of 8; kind (full-attention layers only; DeltaNet only).
Grid: every source x every destination at all layers (DeltaNet mode 'value'), plus with --absent every source x
  {both, after} in DeltaNet mode 'absent' (S removed from the recurrence: no write, erase or decay; S then has no
  direct influence at all: the positive control); for every other layer set,
  the sweep sources (--sweep path: each family's path sources and their same-kind controls, RR with RL's; path+random:
  those and the random span; --sweep all:
  every source) x the sweep destinations (default question, final, both).

Read: suite_split's (one forward of the prompt, a digit answer's space appended, at the answer's first token). Per row:
correct (top token = the answer's), kept (top token = the item's unedited top token in the same batch; each batch has
its own unedited row), the DeltaNet output-norm ratio at D (||o_d|| knocked / normal before the per-head RMSNorm,
mean over knocked DeltaNet layers and heads: how much the norm will scale the rest back up), confusion (top token = another entity's answer in the same prompt: another locker / another
pet's legs / another friend's legs / another row's locker / another country's capital), the answer token's log-prob
and its change from the unedited row.

Decision rule (fixed before any 27B run; jobs/d2/*.yaml): on items whose unedited read is right, a cell (family,
source, destination, layer set, DeltaNet mode) is NEEDED if accuracy drops >= 20 points and the paired bootstrap 95% lower bound
of acc(matched control) - acc(cell) is >= 10 points (control: lookup_off for lookup, binding_off for binding, same
destination, layers, mode); NOT NEEDED if the Wilson 95% lower bound of its accuracy is >= 90%; otherwise PARTIAL.
Positive control: each family's path sources at (after, all, mode absent) must be NEEDED, or that family is not
interpreted. Claims: C1a "RL breaks, RR survives" if RL (lookup, both, all) is NEEDED and RR (lookup, both, all) NOT
NEEDED; C1b "the answer site reads the lookup statement directly" if (lookup, final, all) is NEEDED for BL and RL and
(lookup, question, all) is not; "relay" if the reverse; the band where the lookup must be visible from the final
positions: the largest L with suf L NEEDED and the smallest L with pre L NEEDED.

Stages (write-once; the manifest is written before the run):
  manifest --name N --why W [--families ..] [--n K] [--layers all win8k ..] [--sweep path|all] [--absent]
           [--dests ..] [--sweep-dests ..] [--no-eligibility]
  run --name N          check.json (no-op, positive control, kernel paths, timing) first, then rows.jsonl
  summarise --name N    analysis-<UTC stamp>/summary.json and summary.md (verdicts, claims, layer profiles)
  examples --name N [--k 3]   examples.json (job-page schema, src/bridge_jspace/job_pages.py)
  figures --name N      analysis-<stamp>-figures/ (figures, summary.json, report.md; replaces the previous one)

Batch 3 grids (manifest --grid; pointer sets). heads (pointer_v1): attention only, one unit at a time, the statement
  giving the answer (and its off-path control) blocked from a range's destination: late range (last quarter of
  depth; the last tokens; memory → prompt and named → prompt), early range (first half; the question words; named →
  prompt, plus whole layers and the whole range from the name tokens only), mid range (third quarter; question words
  and last tokens together; memory → prompt). Units: one query head (GQA: its key/value partners still read), one
  key/value group's query heads, one layer, the whole range; memory → memory gets whole layers and ranges only.
  attention.jsonl: the unedited attention of each head to each statement (pointer readout). code_readers
  (code_pointer_v1): the answer's dict entry hidden from one code line or a union of lines, all layers. Rules and
  intervals: BATCH3_RULES, INTERVALS (entity-cluster bootstrap within domain; written into the manifest).
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.knockout import FULL, LINEAR, kernel_path, knock_out, layer_kinds, reference_chunk_rule
from bridge_jspace.stats import bootstrap_mean, cluster_bootstrap, paired_bootstrap_diff, wilson
from bridge_jspace.tokens import raw_encoding
from bridge_jspace.utils import progress
from scripts import exp09_bind_recall as E
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl

EXP = "attn_knockout"
# BJ_D2_RESULTS: a local smoke writes outside the repo's results/ (inputs such as competence runs stay read from there)
RESULTS = Path(os.environ.get("BJ_D2_RESULTS", str(pins.RESULTS_DIR / EXP)))
SUITE = ("BL", "BR", "RL", "RR", "BLR", "BRL")
COUNTRIES = ("country-R", "country-B")
FAMILIES = SUITE + COUNTRIES
SOURCES = ("lookup", "binding", "lookup_off", "binding_off", "random", "trailing")
CONV_REACH = 3  # the DeltaNet conv's kernel is 4: a token's input reaches the next 3 tokens' queries, keys, values
DESTS = ("question", "final", "both", "after")
CONTROL_OF = {"lookup": "lookup_off", "binding": "binding_off"}
PATH = {  # sources on each family's path
    "BL": ("lookup", "binding"),
    "BR": ("binding",),
    "RL": ("lookup",),
    "RR": (),
    "BLR": ("lookup", "binding"),
    "BRL": ("lookup", "binding"),
    "country-R": (),
    "country-B": ("binding",),
}
SWEEP = {  # --sweep path: path sources and their controls; RR and country-R mirror RL and country-B
    "BL": ("lookup", "lookup_off", "binding", "binding_off"),
    "BR": ("binding", "binding_off"),
    "RL": ("lookup", "lookup_off"),
    "RR": ("lookup", "lookup_off"),
    "BLR": ("lookup", "lookup_off", "binding", "binding_off"),
    "BRL": ("lookup", "lookup_off", "binding", "binding_off"),
    "country-R": ("binding", "binding_off"),
    "country-B": ("binding", "binding_off"),
}
SUITE_MAP, COUNTRY_MAP = "map_A8_v1", "map_v1"  # suite_split's and control_split's case samples
SPAN_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 0, 2000, 0
NEEDED_DROP, CONTROL_MARGIN, NOT_NEEDED_LO = 0.20, 0.10, 0.90
BATCH = int(os.environ.get("BJ_BATCH", "64"))  # rows per forward, the item's unedited row included
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # CPU: local smokes on the 0.8B only (load_target)


# ---- items: prompts, spans, positions ------------------------------------------------------------------------------


def token_span(offsets: list[tuple[int, int]], a: int, b: int) -> list[int]:
    return [i for i, (s, e) in enumerate(offsets) if e > s and s < b and e > a]


def encode(tok, text: str, digit: bool) -> tuple[list[int], list[tuple[int, int]], str]:
    """Token ids and char offsets of the prompt as fed: the rendered text, plus a digit answer's space token."""
    enc = raw_encoding(tok, text, offsets=True)
    ids, offsets = list(enc["input_ids"]), [tuple(o) for o in enc["offset_mapping"]]
    prompt = text
    if digit:
        ids += S.ids(tok, " ")
        offsets.append((len(text), len(text) + 1))
        prompt = text + " "
    assert tok.decode(ids) == prompt, "decoded ids differ from the prompt text"
    return ids, offsets, prompt


def finish_case(base: dict, tok, text: str, statements: dict, alts: dict, q_start: int, ctx: tuple[int, int]) -> dict:
    """Positions of the sources (seeded same-length controls and random span), destinations and the context."""
    ids, offsets, prompt = encode(tok, text, base["answer_kind"] == "digit")
    rng = random.Random(
        f"{SPAN_SEED}:{base['family'][:2] if base['family'] in SUITE[:4] else base['family']}:{base['scene']}"
    )

    def span_of(sentence: str) -> list[int]:
        assert text.count(sentence) == 1, f"{base['id']}: {sentence!r} not once in the prompt"
        a = text.index(sentence)
        return token_span(offsets, a, a + len(sentence))

    sources, texts, flags = {}, {}, {}
    for name, sentence in statements.items():
        sources[name], texts[name] = span_of(sentence), sentence
    for name, cands in alts.items():
        target = len(sources[name.removesuffix("_off")])
        same = [c for c in cands if len(span_of(c)) == target]
        pick = rng.choice(same) if same else cands[0]
        flags[name] = "same_length" if same else "length_mismatch"
        sources[name], texts[name] = span_of(pick), pick
    ctx_tok = token_span(offsets, *ctx)
    forbidden = set(sources["binding"]) | set(sources.get("lookup", []))
    return _complete_case(base, tok, text, (ids, offsets, prompt), (sources, texts, flags), rng, ctx_tok, forbidden,
                          q_start, ctx_tok)  # fmt: skip


def _complete_case(
    base: dict, tok, text: str, enc: tuple, named_sources: tuple, rng: random.Random, region: list[int],
    forbidden: set[int], q_start: int, ctx_tok: list[int],
) -> dict:  # fmt: skip
    """The shared tail of a case: the random span (inside `region`, of the main statement's length, overlapping no
    `forbidden` token and never exactly a named statement), the trailing tokens, the destinations and checks."""
    ids, offsets, prompt = enc
    sources, texts, flags = named_sources
    length = len(sources.get("lookup", sources.get("binding", [])))
    named = list(sources.values())
    starts = [
        p
        for p in range(region[0], region[-1] - length + 2)
        if not forbidden & set(range(p, p + length)) and list(range(p, p + length)) not in named
    ]
    p = rng.choice(starts)
    sources["random"], texts["random"] = list(range(p, p + length)), tok.decode(ids[p : p + length])
    content_end = chat.content_end(text, q_start)  # the template's turn end (chat) or "\nAnswer:" (raw) begins here
    question = token_span(offsets, q_start, content_end)
    anchor = max(sources.get("lookup", sources.get("binding", [])))
    trailing = [t for t in range(anchor + 1, anchor + 1 + CONV_REACH) if t < min(question)]
    if trailing:
        sources["trailing"], texts["trailing"] = trailing, tok.decode(ids[trailing[0] : trailing[-1] + 1])
    final = [i for i, (s, _) in enumerate(offsets) if s >= content_end]
    assert question
    assert final
    assert max(question) < min(final)
    assert final[-1] == len(ids) - 1
    assert all(max(v) < min(question) for v in sources.values()), f"{base['id']}: a source after the question"
    return {**base, "prompt": prompt, "ids": ids, "offsets": offsets, "sources": sources, "source_text": texts,
            "source_flags": flags, "dests": {"question": question, "final": final, "both": question + final},
            "context": [ctx_tok[0], ctx_tok[-1]], "q_start": q_start}  # fmt: skip


# ---- pointer-style item sets (D2 batch 2): pointer_v1, code_pointer_v1, alias_pointer_v1 -----------------------------

POINTER_SETS = ("pointer_v1", "code_pointer_v1", "alias_pointer_v1", "pointer_v4")
POINTER_COMPETENCE = {"pointer_v1": "d3_competence_27b", "code_pointer_v1": "code_competence_27b",
                      "alias_pointer_v1": "alias_competence_27b", "pointer_v4": "d3v4_competence_27b"}  # fmt: skip
# pointer_v1's cell gate: a (domain, family[, condition]) cell enters iff its clean Wilson lower bound >= GATE_LO;
# alias_pointer_v1's other surface forms use its own 0.80 (its docstring; English keeps 0.85).
GATE_LO, ALIAS_GATE_LO = 0.85, 0.80
CONDITION = {"e5f0": "same", "e5f0-xlang": "xlang", "e5f0-syn": "syn"}  # alias_pointer_v1's levels -> conditions


def pointer_family(item: dict, dataset: str) -> str:
    """The family key a run reports by: the item's family, with the statements' surface form for alias_pointer_v1."""
    return f"{item['family']}-{CONDITION[item['level']]}" if dataset == "alias_pointer_v1" else item["family"]


def pointer_statement_spans(item: dict, dataset: str) -> list[tuple[int, int]]:
    """Char spans [start, end) of the statements (dict entries for code) in slot order, in the user-turn content
    context + "\\n" + question + " " + instruction. pointer_v1 has no spans: its context is the statements alone,
    one sentence per slot (main and e*f0 levels: no filler, asserted)."""
    if dataset == "code_pointer_v1":
        return [tuple(s) for s in item["spans"]["entries"]]
    if dataset == "alias_pointer_v1":
        return [tuple(s) for s in item["spans"]["statements"]]
    assert item["n_filler"] == 0, f"{item['id']}: pointer_v1 spans are derived for scenes without filler only"
    if dataset == "pointer_v4":  # its statements are listed (3 wordings): located in order in the context
        ctx, out, start = item["context"], [], 0
        for sent in item["statements"]:
            a = ctx.index(sent, start)
            out.append((a, a + len(sent)))
            start = a + len(sent)
        assert len(out) == item["n_entities"], f"{item['id']}: {len(out)} statements for {item['n_entities']} entities"
        assert out[-1][1] == len(ctx), f"{item['id']}: the statements do not cover the context"
        return out
    ctx, out, start = item["context"], [], 0
    for _ in range(item["n_entities"]):
        end = ctx.index(".", start) + 1
        while end < len(ctx) and ctx[end] != " ":  # a period inside a token (none in these domains): keep scanning
            end = ctx.index(".", end) + 1
        out.append((start, end))
        start = end + 1
    assert out[-1][1] == len(ctx), f"{item['id']}: the statements do not cover the context"
    for (a, b), ent, dig in zip(out, item["entities"], item["digits"], strict=True):
        assert ent in ctx[a:b], f"{item['id']}: slot statement {ctx[a:b]!r} does not name {ent}"
        assert str(dig) in ctx[a:b], f"{item['id']}: slot statement {ctx[a:b]!r} does not give {dig}"
    return out


def pointer_case(item: dict, tok, dataset: str) -> dict:
    """A pointer-style item as a case: the statement giving the answer (the queried slot's), a same-kind statement
    off the path (another slot, same token length, seeded per scene), a random span inside the statements' region
    (no overlap with the answer's statement or, in code, the selector lines), the trailing tokens, destinations."""
    text = S.render(tok, item["context"], item["question"])
    content = f"{item['context']}\n{item['question']} {S.INSTRUCTION}"
    shift = text.index(content)
    ids, offsets, prompt = encode(tok, text, item["answer_kind"] == "digit")
    spans = pointer_statement_spans(item, dataset)
    tok_spans = [token_span(offsets, a + shift, b + shift) for a, b in spans]
    q = item["slots"]["query"]
    fam = pointer_family(item, dataset)
    rng = random.Random(f"{SPAN_SEED}:{dataset}:{item['scene']}:{item.get('level', '')}")
    sources = {"lookup": tok_spans[q]}
    texts = {"lookup": content[slice(*spans[q])]}
    same = [i for i, s in enumerate(tok_spans) if i != q and len(s) == len(tok_spans[q])]
    off = rng.choice(same) if same else next(i for i in range(len(spans)) if i != q)
    sources["lookup_off"], texts["lookup_off"] = tok_spans[off], content[slice(*spans[off])]
    flags = {"lookup_off": "same_length" if same else "length_mismatch"}
    region = list(range(min(min(s) for s in tok_spans), max(max(s) for s in tok_spans) + 1))
    forbidden = set(sources["lookup"])
    for key in ("list", "chain"):  # code selectors (IX's list, CH's chains): on the path, never a random control
        for a, b in (item.get("spans") or {}).get(key, []):
            forbidden |= set(token_span(offsets, a + shift, b + shift))
    q_start = shift + len(item["context"]) + 1
    ctx_tok = token_span(offsets, shift, shift + len(item["context"]))
    if item["family"] == "RR":  # the answer is recalled: confusions are other entities' recalled facts
        conf = {str(v) for e, v in item["recalled"].items() if e != item["query"]}
    else:
        conf = {str(d) for e, d in zip(item["entities"], item["digits"], strict=True) if e != item["query"]}
    conf.discard(item["answer"])
    tpl = item.get("templates") or {}  # pointer_v4: one statement and one question template per scene
    base = {"id": item["id"], "family": fam, "scene": item["scene"], "domain": item["domain"], "level": item["level"],
            "question_text": item["question"], "wording": f"s{tpl.get('statement', 0)}q{tpl.get('question', 0)}",
            "cut": item.get("cut"),
            "bridge": item["query"], "cue": item["cue"], "answer": item["answer"], "answer_kind": item["answer_kind"],
            "conf_answers": sorted(conf), "tok_A": S.answer_token(tok, item["answer"], item["answer_kind"]),
            "conf_toks": sorted({S.answer_token(tok, c, item["answer_kind"]) for c in conf}),
            "statements": tok_spans, "query_slot": q}  # fmt: skip
    case = _complete_case(base, tok, text, (ids, offsets, prompt), (sources, texts, flags), rng, region, forbidden,
                          q_start, ctx_tok)  # fmt: skip
    if dataset == "code_pointer_v1":
        case["dests"].update(code_line_dests(item, content, shift, offsets, case["dests"]["final"]))
    if dataset in ("pointer_v1", "pointer_v4") and item["question"].count(item["cue"]) == 1:  # the name / cue tokens
        a = q_start + item["question"].index(item["cue"])
        case["dests"]["cue"] = token_span(offsets, a, a + len(item["cue"]))
        assert set(case["dests"]["cue"]) <= set(case["dests"]["question"]), f"{item['id']}: cue outside the question"
    return case


def code_line_dests(item: dict, content: str, shift: int, offsets: list, final: list[int]) -> dict[str, list[int]]:
    """Batch 3 (b): the code lines that may read the answer's dict entry, one destination each, and the unions that
    test whether they relay it: the names list (list position), each chain line by role (target1 is the chain's
    head, distractor lines the other chain), the print line, the rest of the question (closing fence, the English
    question, the instruction), and combinations with the last tokens before the answer."""
    sp = item["spans"]

    def toks(a: int, b: int) -> list[int]:
        return token_span(offsets, a + shift, b + shift)

    out: dict[str, list[int]] = {}
    if sp.get("list"):  # the whole `names = [...]` line
        out["list"] = toks(content.rfind("\n", 0, sp["list"][0][0]) + 1, content.find("\n", sp["list"][-1][1]))
    for (a, b), (role, i) in zip(sp.get("chain", []), (item.get("code") or {}).get("order", []), strict=True):
        out[f"chain_{role}{i + 1}"] = toks(a, b)
    selector = out.get("list", []) + [t for k, v in out.items() if k.startswith("chain_target") for t in v]
    if item["family"] != "RK":  # RK has no print line: its question is English
        out["print"] = toks(*sp["query"])
        out["nl"] = toks(sp["query"][1], len(content))
    else:
        out["nl"] = toks(sp["question"][0], len(content))
    print_ = out.get("print", [])
    if print_:
        out["final+print"] = sorted(set(final) | set(print_))
    if selector:
        out["final+selector"] = sorted(set(final) | set(selector))
        out["final+print+selector"] = sorted(set(final) | set(print_) | set(selector))
    out["final+print+selector+nl"] = sorted(set(final) | set(print_) | set(selector) | set(out["nl"]))
    dict_end = content.find("\n", sp["entries"][-1][1])  # every token after the dict line
    out["after_dict"] = token_span(offsets, dict_end + shift, len(offsets) and offsets[-1][1])
    return out


def pointer_files(dataset: str, families: list[str], domains: list[str] | None, set_name: str = "main") -> list[Path]:
    folder = pins.DATA_DIR / dataset / set_name
    out = []
    for path in sorted(folder.glob("*.json")):
        domain, fam = path.stem.split("_")[:2]
        if fam in families and (not domains or domain in domains):
            out.append(path)
    return out


def pointer_competence(dataset: str, run: str) -> tuple[dict[str, bool], dict[str, tuple]]:
    """From the dataset's competence run, main set only (main and dev reuse item ids): item id -> every prompt right;
    and per file label ("main/<domain>_<family>_<level>") the clean Wilson bound."""
    rows = [json.loads(line) for line in (pins.RESULTS_DIR / dataset / run / "items.jsonl").read_text().splitlines()]
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    clean: dict[str, list[bool]] = collections.defaultdict(list)
    for r in rows:
        if not r["label"].startswith("main/"):
            continue
        ok[r["id"]].append(r["correct"])
        if r["kind"] == "clean":
            clean[r["label"]].append(r["correct"])
    return {i: all(v) for i, v in ok.items()}, {k: wilson(sum(v), len(v)) for k, v in clean.items()}


def build_pointer_cases(tok, dataset: str, families: list[str], domains: list[str] | None, n: int,
                        eligibility: str, competence: str | None) -> tuple[list[dict], dict]:  # fmt: skip
    """Per domain (and alias condition), the scenes eligible in every requested family (paired), first n by scene
    id; a (domain, condition) group enters only if every family's cell passes the competence gate."""
    files = pointer_files(dataset, families, domains)
    items: dict[tuple[str, str], dict[str, dict]] = collections.defaultdict(dict)  # (domain, level) -> id -> item
    for path in files:
        for it in json.loads(path.read_text())["items"]:
            items[(it["domain"], it["level"])][it["id"]] = it
    report: dict[str, Any] = {}
    elig, gate = pointer_competence(dataset, competence) if eligibility == "map" and competence else ({}, {})
    groups: dict[tuple[str, str], tuple[dict[str, dict[str, dict]], list[str]]] = {}
    for (domain, level), by_id in sorted(items.items()):
        by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
        for it in by_id.values():
            by_scene[it["scene"]][it["family"]] = it
        key = f"{domain}/{level}"
        kept = list(families)
        if eligibility == "map":
            lo_needed = ALIAS_GATE_LO if dataset == "alias_pointer_v1" and level != "e5f0" else GATE_LO
            lows = {f: gate.get(f"main/{domain}_{f}_{level}", (0.0, 0.0, 0.0))[1] for f in families}
            kept = [f for f in families if lows[f] >= lo_needed]
            report[key] = {"gate_lower_bounds": lows, "gate": lo_needed, "families": kept,
                           "entered": any(path_sources(f) for f in kept)}  # fmt: skip
            if not report[key]["entered"]:
                continue
            scenes = [s for s, fams in sorted(by_scene.items())
                      if all(f in fams and elig.get(fams[f]["id"], False) for f in kept)]  # fmt: skip
        else:
            report[key] = {"entered": True, "families": kept}
            scenes = [s for s, fams in sorted(by_scene.items()) if all(f in fams for f in kept)]
        groups[(domain, level)] = (by_scene, scenes)
    if dataset == "alias_pointer_v1":  # pair the surface forms: a domain's scenes eligible in every entered condition
        for domain in {d for d, _ in groups}:
            levels = [lv for d, lv in groups if d == domain]
            if len(levels) < 2:  # the English baseline or the alias form failed the gate: no pair to compare
                for lv in levels:
                    report[f"{domain}/{lv}"]["entered"] = False
                    groups.pop((domain, lv))
                continue
            common = set.intersection(*(set(groups[(domain, lv)][1]) for lv in levels))
            for lv in levels:
                by_scene, scenes = groups[(domain, lv)]
                groups[(domain, lv)] = (by_scene, [s for s in scenes if s in common])
    cases = []
    for (domain, level), (by_scene, scenes) in sorted(groups.items()):
        picked = scenes[:n]
        rep = report[f"{domain}/{level}"]
        rep.update({"eligible_scenes": len(scenes), "picked": len(picked)})
        for s in picked:
            cases += [pointer_case(by_scene[s][f], tok, dataset) for f in rep["families"]]
    return cases, report


def suite_case(item: dict, tok) -> dict:
    fam = item["family"]
    w = S.WORDINGS["A"]
    text = S.render(tok, item["context"], item["question"])
    b, x, z = item["bridge"], item["cf_bridge"], item["third"]
    owner = dict(zip(item["pets"], item["people"], strict=True))
    statements = {"binding": w["own"].format(p=owner[b], a=b)}
    alts = {"binding_off": [w["own"].format(p=owner[a], a=a) for a in (z, x)]}
    legs = {a: n for a, (n, _) in S.ANIMALS.items()}
    if fam == "BLR":
        fr = item["friends"]
        statements["lookup"] = w["friend"].format(a=b, f=fr[b])
        alts["lookup_off"] = [w["friend"].format(a=a, f=fr[a]) for a in (z, x)]
        conf = {str(legs[fr[a]]) for a in item["pets"] if a != b}
    elif fam == "BRL":
        rows = {int(k): v for k, v in item["leg_lockers"].items()}
        statements["lookup"] = w["row"].format(k=legs[b], d=rows[legs[b]])
        alts["lookup_off"] = [w["row"].format(k=k, d=d) for k, d in sorted(rows.items()) if k != legs[b]]
        conf = {str(d) for k, d in rows.items() if k != legs[b]}
    else:
        lk = item["lockers"]
        statements["lookup"] = w["locker"].format(a=b, d=lk[b])
        alts["lookup_off"] = [w["locker"].format(a=a, d=lk[a]) for a in (z, x)]
        conf = {str(lk[a]) for a in (x, z)} if fam.endswith("L") else {str(legs[a]) for a in (x, z)}
    conf.discard(item["answer"])
    ctx_a = text.index(item["context"])
    base = {"id": item["id"], "family": fam, "scene": item["scene"], "bridge": b, "cue": item["cue"],
            "answer": item["answer"], "answer_kind": "digit", "conf_answers": sorted(conf),
            "tok_A": S.answer_token(tok, item["answer"], "digit"),
            "conf_toks": sorted({S.answer_token(tok, c, "digit") for c in conf})}  # fmt: skip
    return finish_case(base, tok, text, statements, alts, text.rindex("\n" + item["question"]) + 1,
                       (ctx_a, ctx_a + len(item["context"])))  # fmt: skip


def country_case(item: dict, uid: str, tok, capitals: dict[str, str]) -> dict:
    text = E.render(item["prompt"], "chat_prefill", tok)
    owner = dict(zip(item["countries"], item["people"], strict=True))

    def stmt(c: str) -> str:
        return f"{owner[c]} lives in {c}."

    clause = " is located" if item["family"] == "R" else " lives"
    q_start = chat.question_span(text, item["cue"], clause)[0]
    context, _ = chat.split_context(item["prompt"])
    ctx_a = text.index(context)
    conf = [capitals[item["target"]], capitals[item["third"]]]
    base = {"id": uid, "family": f"country-{item['family']}", "scene": uid, "bridge": item["bridge"],
            "cue": item["cue"], "answer": item["answer"], "answer_kind": "word", "conf_answers": conf,
            "tok_A": S.answer_token(tok, item["answer"], "word"),
            "conf_toks": sorted({S.answer_token(tok, c, "word") for c in conf})}  # fmt: skip
    return finish_case(base, tok, text, {"binding": stmt(item["bridge"])},
                       {"binding_off": [stmt(item["third"]), stmt(item["target"])]}, q_start,
                       (ctx_a, ctx_a + len(context)))  # fmt: skip


def build_cases(tok, families: list[str], n: int, eligibility: str) -> list[dict]:
    out = []
    suite = [f for f in families if f in SUITE]
    if suite:
        items = {f: {it["id"]: it for it in S.load(f)} for f in suite}
        if eligibility == "map":
            picked = [json.loads(line) for line in (pins.RESULTS_DIR / "suite_split" / SUITE_MAP / "cases.jsonl").read_text().splitlines()]  # fmt: skip
            ids = {f: [r["id"] for r in picked if r["family"] == f][:n] for f in suite}
        else:
            ids = {f: list(items[f])[:n] for f in suite}
        for f in suite:
            out += [suite_case(items[f][i], tok) for i in ids[f]]
    countries = [f for f in families if f in COUNTRIES]
    if countries:
        all_items = pins.bind_recall_items()
        capitals = json.loads(pins.BIND_RECALL_FILE.read_text())["capitals"]
        by_uid = {E.uid(it, i): it for i, it in enumerate(all_items)}
        if eligibility == "map":
            order = [json.loads(line)["id"] for line in (pins.RESULTS_DIR / "control_split" / COUNTRY_MAP / "cases.jsonl").read_text().splitlines()]  # fmt: skip
        else:
            order = list(by_uid)
        for f in countries:
            mine = [u for u in order if f"country-{by_uid[u]['family']}" == f][:n]
            out += [country_case(by_uid[u], u, tok, capitals) for u in mine]
    return out


# ---- conditions -----------------------------------------------------------------------------------------------------


def layer_sets(kinds: list[str], wanted: list[str]) -> dict[str, list[int]]:
    n = len(kinds)
    sets: dict[str, list[int]] = {}
    for w in wanted:
        if w == "all":
            sets["all"] = list(range(n))
        elif w in ("win8", "win4"):
            stride = int(w[3:])
            for a in range(0, n - 8 + 1, stride):
                sets[f"win{a:02d}-{a + 7:02d}"] = list(range(a, a + 8))
        elif w == "win8k":
            for a in range(0, n - 8 + 1, 8):
                window = list(range(a, a + 8))
                sets[f"win{a:02d}-{a + 7:02d}"] = window
                sets[f"win{a:02d}-{a + 7:02d}:attn"] = [i for i in window if kinds[i] == FULL]
                sets[f"win{a:02d}-{a + 7:02d}:gdn"] = [i for i in window if kinds[i] == LINEAR]
        elif w in ("pre", "suf"):
            for cut in range(8, n, 8):
                sets[f"{w}{cut:02d}"] = list(range(cut)) if w == "pre" else list(range(cut, n))
        elif w == "kind":
            sets["attn"] = [i for i, k in enumerate(kinds) if k == FULL]
            sets["gdn"] = [i for i, k in enumerate(kinds) if k == LINEAR]
        elif w == "bands":  # batch 2: the late read band and the two before it, each also by layer kind
            for fa, fb in BANDS:
                a, b = round(fa * n), round(fb * n) - 1  # 64 layers: 0-31, 32-47, 48-63
                band = list(range(a, b + 1))
                sets[f"band{a:02d}-{b:02d}"] = band
                sets[f"band{a:02d}-{b:02d}:attn"] = [i for i in band if kinds[i] == FULL]
                sets[f"band{a:02d}-{b:02d}:gdn"] = [i for i in band if kinds[i] == LINEAR]
        elif w == "band4":  # consecutive 4-layer bands: where the read happens, finer (a model without DeltaNet)
            for a in range(0, n, 4):
                sets[f"band{a:02d}-{min(a + 3, n - 1):02d}"] = list(range(a, min(a + 4, n)))
        else:
            raise ValueError(w)
    # a model with one layer kind (OLMo: full attention in every layer): no empty or duplicate per-kind sets
    return {k: v for k, v in sets.items() if v and not (":" in k and v == sets.get(k.split(":")[0]))}


# D2 (first night): the lookup statement is read at layers 48-63 of Qwen3.6-27B's 64. Bands as fractions of depth, so
# the 27B gets 0-31, 32-47, 48-63 and a smoke model the same thirds of its depth.
BANDS = ((0.0, 0.5), (0.5, 0.75), (0.75, 1.0))


def band_labels(cells: dict) -> list[str]:
    """The run's band labels, earliest first (late band last)."""
    return sorted({k[3].split(":")[0] for k in cells if k[3].startswith("band")}, key=lambda s: int(s[4:6]))


def path_sources(fam: str) -> tuple[str, ...]:
    """Sources on the family's path: the suite's table; a pointer family's lookup statement unless the answer is
    recalled (RR, the null)."""
    if fam in PATH:
        return PATH[fam]
    return () if fam.split("-")[0] == "RR" else ("lookup",)


def sweep_sources(fam: str) -> tuple[str, ...]:
    return SWEEP.get(fam, ("lookup", "lookup_off"))


CODE_DEST_ORDER = ("list", "chain_target1", "chain_target2", "chain_target3", "chain_distractor1", "chain_distractor2",
                   "chain_distractor3", "print", "nl", "final", "final+print", "final+selector", "final+print+selector",
                   "final+print+selector+nl", "after_dict", "after")  # fmt: skip


# Batch 3 (a), the heads grid: per range of depth (fractions of the layers; its full-attention layers), the destination
# blocked there and the families blocked one query head at a time (every unit: head, key/value group, layer, the whole
# range). The memory → memory null gets each range's whole layers and the whole range only. The 27B: late = 51, 55,
# 59, 63 (the last tokens: batch 2's late read); early = 3, 7, ..., 31 (the question words of named → prompt: batch 2's
# early read); mid = 35, 39, 43, 47 (memory → prompt's joint block, question words and last tokens together).
HEAD_RANGES: dict[str, tuple[tuple[float, float], str, tuple[str, ...]]] = {  # in depth order (figures, report)
    "early": ((0.0, 0.5), "question", ("DL",)),
    "mid": ((0.5, 0.75), "both", ("RL",)),
    "late": ((0.75, 1.0), "final", ("RL", "DL")),
}
NARROW_DEST = {"early": "cue"}  # the range's whole layers and whole range again, from the name tokens only


def label_range(label: str, att: dict) -> str:
    """The heads grid range a layer label belongs to ('late', 'L51', 'L51:kv2', 'L51:h07' -> 'late')."""
    if label in att["ranges"]:
        return label
    la = int(label[1:3])
    return next(r for r, v in att["ranges"].items() if la in v["layers"])


def unit_key(r: dict, m: dict) -> str:
    """A heads-grid row's unit: its layer label, with '@<dest>' when the destination is not its range's own (the
    name-token narrowing); a code-readers row's unit is its destination."""
    if m.get("grid") != "heads":
        return r["dest"]
    own = m["attention"]["ranges"][label_range(r["layers"], m["attention"])]["dest"]
    return r["layers"] if r["dest"] == own else f"{r['layers']}@{r['dest']}"


def conditions(case: dict, m: dict) -> list[dict]:
    grid = m.get("grid", "standard")
    if grid == "heads":  # batch 3 (a): one query head (or group, layer, whole range) at a time, per range's destination
        att, fam = m["attention"], case["family"].split("-")[0]
        path = bool(path_sources(case["family"]))
        out = []
        for label in m["layer_sets"]:
            rng = att["ranges"][label_range(label, att)]
            if fam in rng["families"]:
                narrow = rng.get("narrow_dest")
                dests = [rng["dest"]] + ([narrow] if narrow and ":" not in label and narrow in case["dests"] else [])
            elif not path and ":" not in label:
                dests = [rng["dest"]]
            else:
                continue
            out += [{"source": s, "dest": d, "layers": label, "mode": "value"} for d in dests for s in ("lookup", "lookup_off")]  # fmt: skip
        return out
    if grid == "code_readers":  # batch 3 (b): one code line (or union) at a time, every layer
        dests = [d for d in CODE_DEST_ORDER if d in case["dests"] or d == "after"]
        return [
            {"source": s, "dest": d, "layers": "all", "mode": "value"} for d in dests for s in ("lookup", "lookup_off")
        ]
    fam = case["family"]
    srcs = [s for s in m["sources"] if s in case["sources"]]
    out = [{"source": s, "dest": d, "layers": "all", "mode": "value"} for s in srcs for d in m["dests"]]
    if m["absent"]:
        out += [{"source": s, "dest": d, "layers": "all", "mode": "absent"} for s in srcs for d in ("both", "after")]
    sweep = srcs if m["sweep"] == "all" else [s for s in srcs if s in sweep_sources(fam)]
    if m["sweep"] == "path+random" and "random" in srcs:
        sweep.append("random")
    for label in m["layer_sets"]:
        if label != "all":
            out += [{"source": s, "dest": d, "layers": label, "mode": "value"} for s in sweep for d in m["sweep_dests"]]
    return out


def positions(case: dict, cond: dict) -> tuple[list[int], list[int]]:
    src = case["sources"][cond["source"]]
    dst = list(range(max(src) + 1, len(case["ids"]))) if cond["dest"] == "after" else case["dests"][cond["dest"]]
    return src, dst


# ---- stages ---------------------------------------------------------------------------------------------------------


def model_config() -> dict:
    from huggingface_hub import hf_hub_download

    cfg = json.loads(Path(hf_hub_download(pins.MODEL_REPO, "config.json", revision=pins.MODEL_REVISION)).read_text())
    return cfg.get("text_config", cfg)


def model_kinds() -> list[str]:
    return list(model_config()["layer_types"])


def head_sets(
    cfg: dict, ranges: tuple[str, ...] = tuple(HEAD_RANGES)
) -> tuple[dict[str, list[int]], dict[str, list[int] | None], dict]:
    """Batch 3 (a): per range of HEAD_RANGES, its full-attention layers and, per label, the layers and query heads
    blocked: one query head ("L51:h07"), one key/value group's query heads ("L51:kv2"), a whole layer ("L51"), the
    whole range ("late", "early", "mid")."""
    kinds = list(cfg["layer_types"])
    n, n_heads, n_kv = len(kinds), cfg["num_attention_heads"], cfg["num_key_value_heads"]
    group = n_heads // n_kv
    layers: dict[str, list[int]] = {}
    heads: dict[str, list[int] | None] = {}
    info_ranges: dict[str, dict] = {}
    for name in ranges:
        (lo, hi), dest, fams = HEAD_RANGES[name]
        ls = [la for la, k in enumerate(kinds) if k == FULL and round(lo * n) <= la < round(hi * n)]
        assert ls, f"no full-attention layer in range {name}"
        info_ranges[name] = {"layers": ls, "dest": dest, "families": list(fams), "narrow_dest": NARROW_DEST.get(name)}
        layers[name], heads[name] = ls, None
        for la in ls:
            layers[f"L{la:02d}"], heads[f"L{la:02d}"] = [la], None
            for g in range(n_kv):
                layers[f"L{la:02d}:kv{g}"], heads[f"L{la:02d}:kv{g}"] = [la], list(range(g * group, (g + 1) * group))
            for h in range(n_heads):
                layers[f"L{la:02d}:h{h:02d}"], heads[f"L{la:02d}:h{h:02d}"] = [la], [h]
    info = {"ranges": info_ranges, "late_layers": info_ranges.get("late", {}).get("layers", []),
            "query_heads": n_heads, "kv_heads": n_kv, "query_heads_per_kv": group,
            "unit": "query head: its (destination, answer statement) logits masked; its key/value group partners still "
            "read the statement. kv<g> labels block a whole group's query heads (heads g*group .. g*group+group-1)"}  # fmt: skip
    return layers, heads, info


def stage_manifest(args) -> None:
    pins.check_run_name(args.name)
    path = RESULTS / args.name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    cfg = model_config()
    kinds = list(cfg["layer_types"])
    sets = layer_sets(kinds, args.layers)
    hsets: dict[str, list[int] | None] = {}
    att_info = None
    if args.grid == "heads":
        sets, hsets, att_info = head_sets(cfg, tuple(args.head_ranges))
    elif args.grid == "code_readers":
        sets = {"all": list(range(len(kinds)))}
    for label, ls in sets.items():
        if label.startswith("win") and ":" not in label:
            assert sum(kinds[i] == FULL for i in ls) == 2, f"{label}: not 2 full-attention layers"
    pointer = args.dataset in POINTER_SETS
    if pointer:
        inputs = pointer_files(args.dataset, args.families, args.domains)
        assert inputs, f"no {args.dataset} files for families {args.families}, domains {args.domains}"
        if args.eligibility == "map":
            inputs.append(pins.RESULTS_DIR / args.dataset / args.competence / "items.jsonl")
    else:
        inputs = [S.data_dir("A") / f"{f}.json" for f in args.families if f in SUITE]
    if not pointer and any(f in COUNTRIES for f in args.families):
        inputs.append(pins.BIND_RECALL_FILE)
    if not pointer and args.eligibility == "map":
        inputs += (
            [pins.RESULTS_DIR / "suite_split" / SUITE_MAP / "cases.jsonl"]
            if any(f in SUITE for f in args.families)
            else []
        )
        inputs += [pins.RESULTS_DIR / "control_split" / COUNTRY_MAP / "cases.jsonl"] if any(f in COUNTRIES for f in args.families) else []  # fmt: skip
    m = {
        "exp": EXP, "run": args.name, "why": args.why,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "dataset": args.dataset, "domains": args.domains,
        "competence": args.competence if pointer and args.eligibility == "map" else None,
        "gate": f"pointer sets: a (domain, family, condition) cell enters iff its clean Wilson lower bound >= {GATE_LO} "
        f"in the competence run ({ALIAS_GATE_LO} for alias_pointer_v1's other surface forms); a (domain, condition) "
        "group needs at least one family that looks its answer up; items: every competence prompt right; scenes "
        "paired across the group's entered families (and, in alias_pointer_v1, across the surface forms: a domain "
        "enters only with both forms); first n scenes by id" if pointer else None,
        "families": args.families, "n_per_family": args.n, "eligibility": args.eligibility,
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
        "sources": args.sources, "dests": args.dests, "sweep": args.sweep, "sweep_dests": args.sweep_dests,
        "absent": args.absent, "layer_sets": sets, "layer_kinds": kinds,
        "grid": args.grid, "head_sets": hsets, "attention": att_info,
        "seeds": {"spans": SPAN_SEED, "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
        "knockout": (sys.modules["bridge_jspace.knockout"].__doc__ or "").split("\n\n")[1],
        "decision": {"needed": f"accuracy drop >= {NEEDED_DROP:.0%} and paired bootstrap 95% lower bound of "
                     f"acc(control) - acc(cell) >= {CONTROL_MARGIN:.0%}", "not_needed": f"Wilson 95% lower bound of "
                     f"accuracy >= {NOT_NEEDED_LO:.0%}", "doc": next(p for p in (__doc__ or "").split("\n\n") if p.startswith("Decision rule"))},
        "batch3_rules": BATCH3_RULES if args.grid != "standard" else None,
        "intervals": INTERVALS if args.grid != "standard" else None,
        "batch": BATCH,
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def statement_attention(model, ids: torch.Tensor, case: dict, layers: list[int], cue_layers: list[int]) -> dict:
    """Batch 3 (a), the pointer readout: in the unedited forward, each late attention layer's query heads' attention
    from the last token (and averaged over the last tokens before the answer) to each statement, summed over the
    statement's tokens: masses [layer][head][statement] in slot order, and the asked statement's slot; at cue_layers
    (the early range, named → prompt) the same from the name tokens of the question, averaged over them."""
    from bridge_jspace.knockout import attention_probs

    def masses(probs: dict, field: str, mean_field: str | None = None) -> None:
        for la, p in probs.items():
            mass = torch.stack([p[0, :, :, s].sum(-1) for s in case["statements"]], dim=-1)  # [heads, len(q), S]
            out[field][str(la)] = [
                [round(float(x), 4) for x in h] for h in (mass[:, -1] if mean_field else mass.mean(1))
            ]
            if mean_field:
                out[mean_field][str(la)] = [[round(float(x), 4) for x in h] for h in mass.mean(1)]

    out: dict[str, Any] = {"id": case["id"], "family": case["family"], "scene": case["scene"],
                           "query_slot": case["query_slot"], "last": {}, "final_mean": {}, "cue": {}}  # fmt: skip
    if layers:
        masses(attention_probs(model, ids, layers, case["dests"]["final"]), "last", "final_mean")
    if cue_layers and case["dests"].get("cue"):
        masses(attention_probs(model, ids, cue_layers, case["dests"]["cue"]), "cue")
    return out


def forward_last(model, ids: torch.Tensor) -> torch.Tensor:
    return model.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[:, -1].float()


@torch.no_grad()
def run_check(model, case: dict, kinds: list[str]) -> dict:
    """The gate before the run, on the first case: no-op exactness, batch drift of the unedited row, the positive
    control (context-independence), the DeltaNet kernel path against the torch reference, and timing."""
    ids = torch.tensor([case["ids"]], device=DEVICE)
    n_layers, length = len(kinds), ids.shape[1]
    every = range(n_layers)
    plain = forward_last(model, ids)
    out: dict[str, Any] = {"kernel_path": kernel_path()}
    with knock_out(model, every, [[]], [case["dests"]["final"]]):
        out["noop_empty_source_max_abs"] = float((forward_last(model, ids) - plain).abs().max())
    src = case["sources"]["lookup"] if "lookup" in case["sources"] else case["sources"]["binding"]
    with knock_out(model, every, [[], src], [[], case["dests"]["both"]]):
        two = forward_last(model, ids.expand(2, -1).contiguous())
    out["unedited_row_drift_in_knocked_batch_max_abs"] = float((two[0] - plain[0]).abs().max())
    # Positive control: another prompt of the same length, context tokens rolled; the last token is kept.
    other = ids.clone()
    c0, c1 = case["context"]
    other[0, c0 : c1 + 1] = ids[0, c0 : c1 + 1].roll(3)
    pair = torch.cat([ids, other])
    with knock_out(model, every, [list(range(1, length - 1))] * 2, [[length - 1]] * 2, mode="absent"):
        lg = forward_last(model, pair)
    out["posctl_last_reads_nothing_max_abs"] = float((lg[0] - lg[1]).abs().max())
    out["posctl_last_reads_nothing_same_top"] = bool(lg[0].argmax() == lg[1].argmax())
    after = list(range(c1 + 1, length))
    for mode in ("absent", "value"):
        with knock_out(model, every, [list(range(c0, c1 + 1))] * 2, [after] * 2, mode=mode):
            lg = forward_last(model, pair)
        out[f"posctl_context_erased_{mode}_max_abs"] = float((lg[0] - lg[1]).abs().max())
    lg = forward_last(model, pair)
    out["unhooked_rolled_context_max_abs"] = float((lg[0] - lg[1]).abs().max())
    # Kernel path: one DeltaNet layer's actual inputs, the dispatched kernel vs transformers' torch reference.
    layer = next(i for i in range(n_layers // 2, n_layers) if kinds[i] == LINEAR)
    gdn = model.layers[layer].linear_attn
    ns: Any = sys.modules[type(gdn).__module__]
    seen: dict[str, Any] = {}
    rule = ns.torch_chunk_gated_delta_rule

    def capture(*args, **kwargs):
        seen["args"], seen["kwargs"] = args, kwargs
        return rule(*args, **kwargs)

    ns.torch_chunk_gated_delta_rule = capture
    try:
        forward_last(model, ids)
    finally:
        ns.torch_chunk_gated_delta_rule = rule
    ref = reference_chunk_rule(gdn)
    q, k, v = seen["args"][:3]
    g, beta = seen["kwargs"]["g"], seen["kwargs"]["beta"]
    v0 = v.clone()
    v0[:, src] = 0
    for label, vv in (("noop", v), ("v0_at_source", v0)):
        o1, _ = rule(q, k, vv, g=g, beta=beta, use_qk_l2norm_in_kernel=True)
        o2, _ = ref(q, k, vv, g=g, beta=beta, use_qk_l2norm_in_kernel=True)
        rms = float(o2.float().pow(2).mean().sqrt())
        out[f"kernel_{label}_dispatched_vs_torch_max_abs_over_rms"] = float((o1.float() - o2.float()).abs().max()) / rms
        out[f"kernel_{label}_dispatched_vs_torch_rel_fro"] = float((o1.float() - o2.float()).norm() / o2.float().norm())
    out["kernel_layer"] = layer
    # Timing: a full batch unedited vs every row knocked out at every layer (the costliest condition).
    rows = torch.tensor([case["ids"]] * BATCH, device=DEVICE)
    for label, ctx in (
        ("plain", None),
        ("all_layers_knocked", (every, [src] * BATCH, [case["dests"]["both"]] * BATCH)),
    ):
        times = []
        for _ in range(3):
            if DEVICE == "cuda":
                torch.cuda.synchronize()
            t = time.time()
            if ctx is None:
                forward_last(model, rows)
            else:
                with knock_out(model, *ctx):
                    forward_last(model, rows)
            if DEVICE == "cuda":
                torch.cuda.synchronize()
            times.append(time.time() - t)
        out[f"seconds_batch{BATCH}_{label}"] = round(min(times[1:]), 4)
    out["passed"] = bool(out["noop_empty_source_max_abs"] == 0.0 and out["posctl_last_reads_nothing_same_top"]
                         and out["posctl_last_reads_nothing_max_abs"] < 0.1 and out["posctl_context_erased_absent_max_abs"] < 0.1)  # fmt: skip
    return out


def load_target() -> Any:
    """Part B's loader (bf16 on CUDA). Without a GPU (a local smoke on the 0.8B): the pinned target's text model in fp32
    on CPU, with the attributes the run uses (.hf, .tokenizer, .layers)."""
    if DEVICE == "cuda":
        from bridge_jspace.model import load_model

        return load_model()
    from types import SimpleNamespace

    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM

    from bridge_jspace.knockout import decoder_layers
    from bridge_jspace.tokens import load_tokenizer

    path = snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True)
    hf = AutoModelForCausalLM.from_pretrained(path, dtype=torch.float32, attn_implementation="sdpa").eval()
    return SimpleNamespace(hf=hf, tokenizer=load_tokenizer(), layers=decoder_layers(hf))


@torch.no_grad()
def stage_run(name: str) -> None:
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "rows.jsonl").exists(), f"{out_dir} has results; runs are written once"
    for rel, sha in m["inputs"].items():
        assert sha256_of(pins.REPO_ROOT / rel) == sha, f"{rel} changed since the manifest"
    model = load_target()
    kinds = layer_kinds(model)
    assert kinds == m["layer_kinds"], "the loaded model's layer kinds differ from the manifest's"
    tok = model.tokenizer
    t0 = time.time()
    if m.get("dataset", "suite") in POINTER_SETS:
        cases, report = build_pointer_cases(tok, m["dataset"], m["families"], m.get("domains"), m["n_per_family"],
                                            m["eligibility"], m.get("competence"))  # fmt: skip
        (out_dir / "cases_report.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report), flush=True)
    else:
        cases = build_cases(tok, m["families"], m["n_per_family"], m["eligibility"])
    print(json.dumps(collections.Counter(c["family"] for c in cases)), flush=True)
    check = run_check(model, cases[0], kinds)
    check["seconds"] = round(time.time() - t0, 1)
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps(check, indent=1), flush=True)
    assert check["passed"], "the pre-run check failed (check.json); not running"
    sets = m["layer_sets"]
    hsets = m.get("head_sets") or {}
    rows: list[dict] = []
    attention: list[dict] = []
    total = sum(len(conditions(c, m)) for c in cases)
    print(f"{len(cases)} cases, {total} knocked rows", flush=True)
    t_run = time.time()
    for c in progress(cases, desc="items"):
        conds = conditions(c, m)
        ids = torch.tensor([c["ids"]], device=DEVICE)
        if m.get("grid") == "heads" and "statements" in c:  # the pointer readout: where the last / name tokens look
            early = m["attention"]["ranges"].get("early")
            cue_layers = early["layers"] if early and c["family"].split("-")[0] in early["families"] else []
            attention.append(statement_attention(model, ids, c, m["attention"]["late_layers"], cue_layers))
        base_top = None
        for mode in ("value", "absent"):
            mine = [x for x in conds if x["mode"] == mode]
            for start in range(0, len(mine), BATCH - 1):
                chunk = [None, *mine[start : start + BATCH - 1]]  # row 0: the unedited row of this batch
                src = [positions(c, x)[0] if x else [] for x in chunk]
                dst = [positions(c, x)[1] if x else [] for x in chunk]
                layers = [sets[x["layers"]] if x else [] for x in chunk]
                heads = [hsets.get(x["layers"]) if x else None for x in chunk]
                norm_log: list[dict] = []
                with knock_out(model, layers, src, dst, mode=mode, norm_log=norm_log, heads=heads):
                    lg = forward_last(model, ids.expand(len(chunk), -1).contiguous())
                ratios: dict[int, list[float]] = collections.defaultdict(list)
                for entry in norm_log:
                    for r, x in zip(entry["rows"], entry["ratio"], strict=True):
                        ratios[r].append(x)
                logp = lg.log_softmax(-1)
                top = lg.argmax(-1).tolist()
                base_top = top[0] if base_top is None else base_top
                for row, x in enumerate(chunk):
                    if x is None and (start > 0 or mode == "absent"):
                        continue  # one unedited row per item in rows.jsonl; the others serve their batch only
                    rows.append({"family": c["family"], "id": c["id"], "scene": c["scene"],
                                 **(x or {"source": "none", "dest": "-", "layers": "-", "mode": "-"}),
                                 "norm_ratio": round(statistics.mean(ratios[row]), 4) if ratios[row] else None,
                                 "top": top[row], "correct": top[row] == c["tok_A"], "kept": top[row] == top[0],
                                 "conf": top[row] in c["conf_toks"], "logp": round(float(logp[row, c["tok_A"]]), 4),
                                 "dlogp": round(float(logp[row, c["tok_A"]] - logp[0, c["tok_A"]]), 4),
                                 "batch_none_top": top[0]})  # fmt: skip
    seconds = time.time() - t_run
    write_jsonl(out_dir / "rows.jsonl", rows)
    if attention:
        write_jsonl(out_dir / "attention.jsonl", attention)
    keep = ("id", "family", "scene", "bridge", "cue", "answer", "answer_kind", "conf_answers", "tok_A", "conf_toks",
            "prompt", "ids", "offsets", "sources", "source_text", "source_flags", "dests", "context", "domain", "level",
            "question_text", "statements", "query_slot", "wording", "cut")  # fmt: skip
    write_jsonl(out_dir / "cases.jsonl", [{k: c[k] for k in keep if k in c} for c in cases])
    timing = {"cases": len(cases), "knocked_rows": total, "forwards_rows_incl_unedited": total + sum(
        -(-len([x for x in conditions(c, m) if x["mode"] == g]) // (BATCH - 1)) for c in cases for g in ("value", "absent")),
        "seconds_run": round(seconds, 1), "rows_per_second": round(total / seconds, 2),
        "seconds_total": round(time.time() - t0, 1), "mean_prompt_tokens": statistics.mean(len(c["ids"]) for c in cases)}  # fmt: skip
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)


# ---- summary --------------------------------------------------------------------------------------------------------


def load_run(name: str) -> tuple[dict, list[dict], dict[str, dict]]:
    global DATASET
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    DATASET = m.get("dataset", "suite")  # family codes read per item set in every display
    RUN_INFO.update({"model": m["model"]["repo"].split("/")[-1], "n_layers": len(m["layer_kinds"])})
    HEAD_INFO.clear()
    HEAD_INFO.update(m.get("attention") or {})
    rows = [json.loads(line) for line in (out_dir / "rows.jsonl").read_text().splitlines()]
    cases = {c["id"]: c for c in (json.loads(line) for line in (out_dir / "cases.jsonl").read_text().splitlines())}
    return m, rows, cases


def right_items(rows: list[dict], m: dict) -> set[str]:
    """Items that count: unedited read right (any item for a --no-eligibility smoke, scored by 'kept')."""
    return {r["id"] for r in rows if r["source"] == "none" and (r["correct"] or m["eligibility"] == "none")}


def cell_key(r: dict) -> tuple:
    return (r["family"], r["source"], r["dest"], r["layers"], r["mode"])


def summarise_cells(m: dict, rows: list[dict]) -> dict[tuple, dict]:
    ok = right_items(rows, m)
    measure = "kept" if m["eligibility"] == "none" else "correct"
    cells: dict[tuple, dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        if r["source"] != "none" and r["id"] in ok:
            cells[cell_key(r)][r["id"]] = r
    out = {}
    for key, by_id in cells.items():
        vals = [float(r[measure]) for r in by_id.values()]
        n = len(vals)
        acc = wilson(int(sum(vals)), n)
        ratios = [r["norm_ratio"] for r in by_id.values() if r.get("norm_ratio") is not None]
        cell = {"n": n, "acc": acc, "conf": wilson(sum(r["conf"] for r in by_id.values()), n),
                "dlogp": bootstrap_mean([r["dlogp"] for r in by_id.values()], N_BOOT, BOOT_SEED),
                "deltanet_norm_ratio": statistics.mean(ratios) if ratios else None}  # fmt: skip
        fam, source, dest, layers, mode = key
        ctrl = cells.get((fam, CONTROL_OF.get(source, ""), dest, layers, mode))
        verdict = "partial"
        if acc[1] >= NOT_NEEDED_LO:
            verdict = "not_needed"
        elif ctrl:
            names = sorted(set(by_id) & set(ctrl))
            d = paired_bootstrap_diff([float(ctrl[i][measure]) for i in names], [float(by_id[i][measure]) for i in names],
                                      N_BOOT, BOOT_SEED)  # fmt: skip
            cell["vs_control"] = d
            if 1 - acc[0] >= NEEDED_DROP and d[1] >= CONTROL_MARGIN:
                verdict = "needed"
        elif source not in CONTROL_OF and 1 - acc[0] >= NEEDED_DROP:
            verdict = "breaks (control)"
        cell["verdict"] = verdict
        out[key] = cell
    return out


def claims(cells: dict[tuple, dict]) -> dict:
    def v(fam, source, dest, layers="all", mode="value"):
        c = cells.get((fam, source, dest, layers, mode))
        return c["verdict"] if c else None

    out: dict[str, Any] = {"positive_control": {}}
    present = sorted({k[0] for k in cells}, key=fam_order)
    for fam in present:
        got = {s: v(fam, s, "after", mode="absent") for s in path_sources(fam)}
        if any(x is not None for x in got.values()):
            out["positive_control"][fam] = {"sources": got, "passed": all(x == "needed" for x in got.values())}

    def acc(fam, dest, layers):
        c = cells.get((fam, "lookup", dest, layers, "value"))
        return round(c["acc"][0], 3) if c else None

    late = {}  # batch 2: is the answer's statement read by the last tokens, late, through attention?
    blabels = band_labels(cells)
    early, mid, last = (blabels[0], blabels[1], blabels[2]) if len(blabels) == 3 else (None, None, None)
    for fam in present:
        if (fam, "lookup", "final", "all", "value") not in cells:
            continue
        sets = ["all", "attn", "gdn", *[f"{b}{k}" for b in blabels for k in ("", ":attn", ":gdn")]]
        late[fam] = {"path": bool(path_sources(fam)),
                     "final": {s: {"acc": acc(fam, "final", s), "verdict": v(fam, "lookup", "final", s)}
                               for s in sets if acc(fam, "final", s) is not None},
                     "question_all": {"acc": acc(fam, "question", "all"), "verdict": v(fam, "lookup", "question")}}  # fmt: skip
        f = late[fam]["final"]
        late[fam]["late_attention_read"] = (
            bool(
                f.get("all", {}).get("verdict") == "needed"
                and f.get("attn", {}).get("verdict") == "needed"
                and (f.get("gdn", {}).get("acc") or 0) >= NOT_NEEDED_LO
                and f.get(last or "", {}).get("verdict") in ("needed", "partial")
                and all((f.get(b or "", {}).get("acc") or 0) >= NOT_NEEDED_LO for b in (early, mid))
            )
            if last in f
            else None
        )
        late[fam]["bands"] = {"early": early, "middle": mid, "late": last}
    out["late_attention_read"] = late
    out["C1a_RL_breaks_RR_survives"] = {"RL": v("RL", "lookup", "both"), "RR": v("RR", "lookup", "both"),
                                       "holds": v("RL", "lookup", "both") == "needed" and v("RR", "lookup", "both") == "not_needed"}  # fmt: skip
    fin = {f: (v(f, "lookup", "final"), v(f, "lookup", "question")) for f in ("BL", "RL", "BLR", "BRL")}
    out["C1b_answer_site_reads_lookup"] = {f: {"final": a, "question": b} for f, (a, b) in fin.items()}
    out["C1b_holds"] = all(fin[f][0] == "needed" and fin[f][1] != "needed" for f in ("BL", "RL"))
    out["relay_holds"] = all(fin[f][1] == "needed" and fin[f][0] != "needed" for f in ("BL", "RL"))
    out["recall_needs_no_locker"] = {f: {d: v(f, "lookup", d) for d in DESTS} for f in ("BR", "RR")}
    out["binding_BL_vs_BR"] = {f: {d: v(f, "binding", d) for d in DESTS} for f in ("BL", "BR", "BLR", "BRL")}
    bands: dict[str, dict] = {}
    for (fam, source, dest, layers, mode), c in cells.items():
        if source not in CONTROL_OF or mode != "value" or layers == "all":
            continue
        b = bands.setdefault(f"{fam}/{source}/{dest}", {"windows_needed": [], "suf_needed": [], "pre_needed": []})
        if c["verdict"] == "needed":
            kind = (
                "windows_needed"
                if layers.startswith(("win", "band"))
                else f"{layers[:3]}_needed"
                if layers[:3] in ("suf", "pre")
                else "kind_needed"
            )
            b.setdefault(kind, []).append(layers)
    for b in bands.values():
        b["suf_max_needed"] = max((int(x[3:]) for x in b["suf_needed"]), default=None)
        b["pre_min_needed"] = min((int(x[3:]) for x in b["pre_needed"]), default=None)
    out["bands"] = bands
    return out


def stage_summarise(name: str) -> None:
    m, rows, _ = load_run(name)
    out_dir = RESULTS / name / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out_dir.mkdir(parents=True, exist_ok=False)
    cells = summarise_cells(m, rows)
    none = [r for r in rows if r["source"] == "none"]
    by_fam = {f: {"items": sum(r["family"] == f for r in none), "unedited_right": sum(r["family"] == f and r["correct"] for r in none)}
              for f in dict.fromkeys(r["family"] for r in none)}  # fmt: skip
    summary = {"run": name, "measure": "kept" if m["eligibility"] == "none" else "correct", "items": by_fam,
               "claims": claims(cells), "cells": [{"family": k[0], "source": k[1], "dest": k[2], "layers": k[3],
                                                   "mode": k[4], **c} for k, c in cells.items()]}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# {EXP} / {name}", "", f"Measure: {summary['measure']} (items: {json.dumps(by_fam)})", "",
             f"Claims: {json.dumps(summary['claims'], indent=1)}", "",
             "| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip

    def pct(t):
        return f"{100 * t[0]:.0f}% [{100 * t[1]:.0f},{100 * t[2]:.0f}]"

    for k, c in sorted(cells.items(), key=lambda kv: (fam_order(kv[0][0]), kv[0][1:])):
        vs = (
            f"{100 * c['vs_control'][0]:+.0f} [{100 * c['vs_control'][1]:+.0f},{100 * c['vs_control'][2]:+.0f}]"
            if "vs_control" in c
            else "-"
        )
        nr = f"{c['deltanet_norm_ratio']:.2f}" if c["deltanet_norm_ratio"] is not None else "-"
        lines.append(f"| {' | '.join(k)} | {c['n']} | {pct(c['acc'])} | {100 * c['conf'][0]:.0f}% | "
                     f"{c['dlogp'][0]:+.2f} [{c['dlogp'][1]:+.2f},{c['dlogp'][2]:+.2f}] | {nr} | {vs} | {c['verdict']} |")  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out_dir}")
    print("\n".join(lines[:6]))


# ---- figures and report (CPU, saved outputs only) -------------------------------------------------------------------

# Effects in the dataviz reference palette's slots 1-3 (validated: CVD-adjacent dE >= 9.2; contrast relief by marker
# shape + legend); controls in muted greys, told apart by marker shape and labelled as controls (figure_terms.md).
SERIES = {
    "statement": ("#2a78d6", "o", "the statement itself (blocked)"),
    "off": ("#5f5e59", "s", "control: a statement of the same kind off the answer's path"),
    "random": ("#7f7d77", "^", "control: a random span of the prompt, same length"),
    "trailing": ("#a3a199", "D", "control: the up to 3 tokens right after the statement"),
}
KINDS = {
    "": ("#2a78d6", "o", "all 8 layers of the window"),
    ":attn": ("#eb6834", "s", "only its 2 attention layers"),
    ":gdn": ("#1baf7a", "^", "only its 6 DeltaNet layers"),
}
SOURCE_PHRASE = {
    "lookup": "the statement giving the answer",
    "binding": "the statement giving the bridge",
    "lookup_off": "control: a statement like the one giving the answer, off the path",
    "binding_off": "control: a statement like the one giving the bridge, off the path",
    "random": "control: a random span of the same length",
    "trailing": "control: the up to 3 tokens after the statement",
}
EXAMPLE = {  # one org prompt per statement kind, bridge org and answer org marked
    "lookup": "Example (memory → prompt): org prompt \"... The cow's locker is 5. ... Which locker belongs to the animal "
    'known for mooing? Answer:" (bridge org: cow, answer org: 5); hidden: "The cow\'s locker is 5.", the statement '
    "giving the answer.",
    "binding": "Example (prompt → memory): org prompt \"Jack's pet is a cow. ... How many legs does Jack's pet have? "
    'Answer:" (bridge org: cow, answer org: 4); hidden: "Jack\'s pet is a cow.", the statement giving the bridge.',
}
TRANSIT = (44, 52)  # 27B: copying C's question group flips RL 98-100% here, and the lens cannot write RL (rows 27, 52)
FAMILY_HINT = {  # what each family asks, in words (displays never show the family codes)
    "BL": "pet stated, its locker looked up",
    "BR": "pet stated, its legs recalled",
    "RL": "animal recalled, its locker looked up",
    "RR": "animal recalled, its legs recalled",
    "BLR": "pet stated, friend looked up, legs recalled",
    "BRL": "pet stated, legs recalled, locker looked up",
    "country-R": "country recalled from a city, capital recalled",
    "country-B": "country stated, capital recalled",
    "DL": "entity named, its locker looked up",
    "DK": "key named in the code, dict value printed",
    "IX": "key read from a list position, dict value printed",
    "CH2": "key passed through 2 variables, dict value printed",
    "CH3": "key passed through 3 variables, dict value printed",
    "RK": "key recalled from a cue, dict value read",
}
POINTER_HINT = {"RL": "entity recalled from a cue, its locker looked up", "RR": "entity recalled, a fact recalled"}


def fam_hint(code: str) -> str:
    base = code.split("-")[0]
    if DATASET in POINTER_SETS and base in POINTER_HINT:
        return POINTER_HINT[base] if DATASET != "code_pointer_v1" or base != "RR" else "key recalled, a fact recalled"
    return FAMILY_HINT.get(code, FAMILY_HINT.get(base, ""))


STATEMENT_WORDS = {
    "lookup": "hidden: the statement giving the answer",
    "binding": "hidden: the statement giving the bridge",
}
DEST_WORDS = {
    "question": "question\nwords",
    "final": "last tokens\nbefore the\nanswer",
    "both": "both",
    "after": "everything\nafter the\nstatement",
}
DEST_PHRASE = {
    "question": "the question words",
    "final": "the last tokens before the answer",
    "both": "the question words and the last tokens",
    "after": "everything after it",
    "cue": "the name tokens in the question",
}


DATASET = "suite"  # the run being analysed (set from its manifest): family codes read differently per item set
RUN_INFO: dict[str, Any] = {"model": "Qwen3.6-27B", "n_layers": 64}  # the analysed run's model, from its manifest
HEAD_INFO: dict[str, Any] = {}  # the analysed heads-grid run's manifest 'attention' (ranges and their layers)
CODE_LABEL = {  # code_pointer_v1's families (its docstring's plain names)
    "DK": "code: named → prompt",
    "IX": "code: list position → prompt",
    "CH2": "code: 2-variable chain → prompt",
    "CH3": "code: 3-variable chain → prompt",
    "RK": "code: memory → prompt",
    "RR": "code: memory → memory",
}
SURFACE = {"same": "statements in English", "xlang": "statements in French/Spanish/German",
           "syn": "statements name the chemical symbol"}  # fmt: skip


def fam_label(code: str) -> str:
    """The plain family name (bridge_jspace.plotting.FAMILY_LABEL: where the bridge comes from -> where the answer
    comes from); this script's country codes map onto its countries_R / countries_B keys; code_pointer_v1's families
    and alias_pointer_v1's surface forms get their own words."""
    from bridge_jspace.plotting import family_label

    if DATASET == "code_pointer_v1":
        return CODE_LABEL.get(code, code)
    if DATASET == "alias_pointer_v1" and "-" in code:
        fam, cond = code.split("-", 1)
        return f"{family_label(fam)}, {SURFACE.get(cond, cond)}"
    return family_label(code.replace("country-", "countries_"))


def plain(text: str) -> str:
    """Display text with every family code replaced by its plain name (item ids such as RL-0329 stay)."""
    import re

    codes = "RL-same|RL-xlang|RL-syn|DL-same|DL-xlang|DL-syn|RR-same|RR-xlang|RR-syn|country-R|country-B|BLR|BRL|CH2|CH3|BL|BR|RL|RR|DL|DK|IX|RK"
    pattern = rf"(?<![\w-])({codes})(?![\w]|-\d)"
    return re.sub(pattern, lambda mt: fam_label(mt.group(1)), text)


def fam_order(code: str) -> tuple[int, int, str]:
    """Reading order: the suite's families; pointer sets: the lookups first (recalled, named, the code forms), the
    memory → memory null last; English before the other surface forms."""
    if DATASET in POINTER_SETS:
        order = ["RL", "DL", "DK", "IX", "CH2", "CH3", "RK", "RR"]
        base, _, cond = code.partition("-")
        forms = ["", "same", "xlang", "syn"]
        return (order.index(base) if base in order else len(order), forms.index(cond) if cond in forms else 9, code)
    order = [*FAMILIES, "DL", "DK", "IX", "CH2", "CH3", "RK"]
    base = code.split("-")[0] if code not in FAMILIES else code
    return (order.index(base) if base in order else len(order), 0, code)


VERDICT = {"needed": "NEEDED", "not_needed": "NOT NEEDED", "partial": "PARTIAL", "breaks (control)": "control breaks"}


def layers_phrase(label: str, n_layers: int = 64) -> str:
    """A layer set's label in words: 'win48-55:attn' -> 'layers 48-55 (attention layers only)'."""
    if label == "all":
        return f"all {n_layers} layers"
    if label in ("attn", "gdn"):
        return "every attention layer" if label == "attn" else "every DeltaNet layer"
    if label in HEAD_INFO.get("ranges", {}):  # batch 3 heads grid: a whole range
        ls = HEAD_INFO["ranges"][label]["layers"]
        if len(ls) == 1:
            return f"attention layer {ls[0]} (all heads; the only one in its range)"
        return f"every attention layer of layers {ls[0]}-{ls[-1]} ({', '.join(map(str, ls))}; all heads)"
    if label == "late":
        return "every attention layer in the last quarter (all heads)"
    if label.startswith("L") and label[1:3].isdigit():  # batch 3 heads grid
        layer, _, unit = label.partition(":")
        if not unit:
            return f"layer {int(layer[1:])} (all heads)"
        if unit.startswith("kv"):
            return f"layer {int(layer[1:])}, key/value group {int(unit[2:])} (its query heads)"
        return f"layer {int(layer[1:])}, query head {int(unit[1:])}"
    base, _, kind = label.partition(":")
    if base.startswith("win"):
        text = f"layers {int(base[3:5])}-{int(base[6:8])}"
    elif base.startswith("band"):
        text = f"layers {int(base[4:6])}-{int(base[7:9])}"
    elif base.startswith("pre"):
        text = f"layers 0-{int(base[3:]) - 1}"
    elif base.startswith("suf"):
        text = f"layers {int(base[3:])}-{n_layers - 1}"
    else:
        text = base
    return text + {"attn": " (attention layers only)", "gdn": " (DeltaNet layers only)"}.get(kind, "")


def cell_phrase(key: tuple) -> str:
    fam, src, dest, layers, mode = key
    tail = " and removed from the DeltaNet recurrence" if mode == "absent" else ""
    where = DEST_PHRASE.get(dest) or CODE_LINE_WORDS.get(dest, dest)
    return f"{fam_label(fam)}, {SOURCE_PHRASE[src]} hidden from {where} in {layers_phrase(layers)}{tail}"


def band_phrase(key: str, band: dict) -> str:
    fam, src, dest = key.split("/")
    parts = []
    if band.get("suf_max_needed") is not None:
        parts.append(f"hiding it from layer L to the last breaks answer org for L up to {band['suf_max_needed']}")
    if band.get("pre_min_needed") is not None:
        parts.append(f"hiding it in layers 0 to L-1 breaks answer org from L = {band['pre_min_needed']}")
    for kind in ("windows_needed", "kind_needed"):
        if band.get(kind):
            parts.append("NEEDED in " + ", ".join(layers_phrase(x) for x in band[kind]))
    return f"{fam_label(fam)}, {SOURCE_PHRASE[src]} hidden from {DEST_PHRASE[dest]}: " + "; ".join(parts)


def example_phrase(ex: dict) -> str:
    """An examples.json condition in the report's terms."""
    import re

    cond = ex["condition"]
    dest = next((d for d, w in (("question", "the question tokens"), ("final", "the final template positions"),
                                ("both", "the question and final positions"), ("after", "every position after it"))
                 if cond.startswith(w)), "question")  # fmt: skip
    src = re.search(r"the (\w+) span", cond)
    layers = re.search(r"at layers (\S+)", cond)
    mode = re.search(r"DeltaNet mode (\w+)", cond)
    key = (ex["family"], src.group(1) if src else "lookup", dest, layers.group(1) if layers else "all",
           mode.group(1) if mode else "value")  # fmt: skip
    return cell_phrase(key)


DEPTH_PANELS = (
    ("RL", "lookup", "final"),
    ("BL", "lookup", "final"),
    ("RR", "lookup", "final"),
    ("BRL", "lookup", "final"),
    ("BLR", "lookup", "final"),
    ("BR", "binding", "question"),
    ("BL", "binding", "question"),
    ("BLR", "binding", "question"),
    ("BRL", "binding", "question"),
    ("country-B", "binding", "question"),
    ("country-R", "binding", "question"),
)
HEADLINES = (("RL", "lookup", "final"), ("BRL", "lookup", "final"), ("country-B", "binding", "question"))


def _pct(c: dict | None) -> str:
    if not c:
        return "-"
    a = c["acc"]
    return f"{100 * a[0]:.0f}% [{100 * a[1]:.0f}, {100 * a[2]:.0f}] (n={c['n']})"


def _errorbar(ax, xs, cs, color, marker, label=None, ms=5.5, **kw):
    ys = [c["acc"][0] for c in cs]
    err = [  # Wilson bounds at 0% / 100% can cross the estimate by rounding
        [max(0.0, y - c["acc"][1]) for y, c in zip(ys, cs, strict=True)],
        [max(0.0, c["acc"][2] - y) for y, c in zip(ys, cs, strict=True)],
    ]
    line = marker in ("x", "+")  # line markers take their colour from the edge: no surface ring for them
    ax.errorbar(xs, ys, yerr=err, fmt=marker, color=color, ms=ms + (1 if line else 0), lw=1.0, elinewidth=1.0,
                capsize=0, mec=color if line else "#fcfcfb", mew=1.6 if line else 0.8, label=label, zorder=3, **kw)  # fmt: skip


def _save(
    fig, stem: Path, title: str, explain: list[tuple[str, str]], data: str, handles=None, ncols: int | None = None
) -> list[str]:
    """plotting.finish's frame with its caption rows (title; bold-labelled rows "What we did", "Example", "How to
    read", "Control", "Data"; legend under the panels), saved as PNG at 200 dpi and SVG (finish saves one 150-dpi
    file). Rows wrap at ~13.5 characters per inch so no line runs past the right edge."""
    import textwrap

    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, SURFACE

    w = fig.get_figwidth()
    label_w = 1.05  # inches: the bold label column
    wrapped = [(label, textwrap.wrap(text, width=int((w - label_w - 0.2) * 13.5)) or [""])
               for label, text in [*explain, ("Data", data)]]  # fmt: skip
    head = 0.38 + sum(0.155 * len(lines) + 0.05 for _, lines in wrapped) + 0.1
    fig.set_figheight(fig.get_figheight() + head)  # the caption gets its own room; the panels keep theirs
    h = fig.get_figheight()
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=INK)
    y = 0.38
    for label, lines in wrapped:
        fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=INK, fontweight="bold")
        fig.text(label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=MUTED,
                 linespacing=1.4)  # fmt: skip
        y += 0.155 * len(lines) + 0.05
    rows = -(-len(handles) // (ncols or len(handles))) if handles else 0
    foot = 0.2 + 0.25 * rows if handles else 0.05
    if handles:
        fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=8.5,
                   labelcolor=INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    for ext in ("png", "svg"):
        fig.savefig(stem.with_suffix(f".{ext}"), dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return [stem.with_suffix(".png").name, stem.with_suffix(".svg").name]


CONTROL_GREY = "#5f5e59"  # darker than the note text so control markers stay visible on the surface


def _transit(ax) -> None:
    """The layers where the bridge is in transit and the lens cannot write it, shaded (named in the legend)."""
    from bridge_jspace.plotting import GRID

    ax.axvspan(*TRANSIT, color=GRID, alpha=0.9, lw=0, zorder=0)


def _transit_handle():
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import GRID

    return Patch(color=GRID, alpha=0.9, label=f"shaded: layers {TRANSIT[0]}-{TRANSIT[1]}, where the bridge is in "
                 "transit at the question and the lens cannot write it (earlier runs)")  # fmt: skip


def data_row(cells: dict, bars: str = "Wilson 95% CI") -> str:
    """The caption's Data row: model, families, prompts per family, error bars (no run ids)."""
    n = sorted({c["n"] for k, c in cells.items() if k[3] == "all"})
    codes = sorted(dict.fromkeys(k[0] for k in cells), key=fam_order)
    sets = {"pointer_v1": "locker scenes: animals, elements, planets, months", "code_pointer_v1": "Python programs "
            "with a dict of lockers", "alias_pointer_v1": "locker scenes, English vs another surface form",
            "pointer_v4": "file / locker / chart scenes: countries, animals, body parts; 3 x 3 wordings"}.get(
        DATASET, "animal scenes" + (" and country prompts" if any(f.startswith("country") for f in codes) else ""))  # fmt: skip
    count = "-".join(map(str, (n[0], n[-1]))) if len(n) > 1 else str(n[0])
    return (f"{RUN_INFO['model']}; {', '.join(fam_label(f) for f in codes)} ({sets}); {count} prompts per family, "
            f"all giving answer org unedited; error bars: {bars}.")  # fmt: skip


EXAMPLE_CASE: dict[str, Any] = {}  # a pointer run's example (a real case), set by stage_figures
ANSWER_SOURCE = ("the statement giving the answer", "the dict entry giving the answer")  # [code_pointer_v1?]


def example_row(cells: dict, blocked: str | None) -> str:
    """The caption's Example row: a real org prompt (shortened), answer org, and what is blocked (None: nothing is
    blocked, the row names the asked statement instead)."""
    if EXAMPLE_CASE:
        c = EXAMPLE_CASE
        stmt = c["source_text"]["lookup"].strip()
        question = " ".join(c.get("question_text", "").replace("```", " ").split())
        q = "'" if '"' in stmt + question else '"'  # code quotes its keys: wrap in single quotes then
        tail = (f"The asked statement: {q}{stmt}{q}." if blocked is None else
                f"Blocked: {blocked} cannot read {q}{stmt}{q} ({ANSWER_SOURCE[DATASET == 'code_pointer_v1']}).")  # fmt: skip
        lp = c.get("dests", {}).get("list")  # code, list position: the names line sits between the dict and the print
        names = f" {c['prompt'][c['offsets'][lp[0]][0] : c['offsets'][lp[-1]][1]].strip()} ..." if lp else ""
        return f"{q}... {stmt} ...{names} {question} Answer:{q} -> answer org {c['answer']}. {tail}"
    if any(k[1] == "lookup" for k in cells):
        return ('"... The cow\'s locker is 5. ... Which locker belongs to the animal known for mooing? Answer:" -> '
                f'answer org 5. Blocked: {blocked} cannot read "The cow\'s locker is 5." (the statement giving the '
                "answer).")  # fmt: skip
    return (
        '"Emma lives in Egypt. ... What is the capital of the country where Emma lives? Answer:" -> answer org '
        f'Cairo. Blocked: {blocked} cannot read "Emma lives in Egypt." (the statement giving the bridge).'
    )


BLOCK_NOTE = ("Blocked = cannot read it directly: attention to it is masked, and DeltaNet layers lose its values; "
              "other positions may still pass it on.")  # fmt: skip


def fig_all_layers(cells: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    order = {"lookup": ("RL", "RR", "BL", "BR", "BLR", "BRL"), "binding": ("BL", "BR", "RL", "RR", "BLR", "BRL", "country-B", "country-R")}  # fmt: skip
    if DATASET in POINTER_SETS:  # one statement kind; families in reading order
        order = {"lookup": tuple(sorted({k[0] for k in cells}, key=fam_order))}
    rows = [(st, [f for f in fams if (f, st, "final", "all", "value") in cells]) for st, fams in order.items()]
    rows = [(st, fams) for st, fams in rows if fams]
    if not rows:
        return None
    ncols = max(len(f) for _, f in rows)
    fig, axes = plt.subplots(
        len(rows), ncols, figsize=(3.2 * ncols + 0.4, 3.6 * len(rows) + 0.6), squeeze=False, sharey=True
    )
    for r, (st, fams) in enumerate(rows):
        for j in range(ncols):
            ax = axes[r][j]
            if j >= len(fams):
                ax.axis("off")
                continue
            fam = fams[j]
            style_axes(ax)
            for k, (series, src) in enumerate((("statement", st), ("off", f"{st}_off"), ("random", "random"), ("trailing", "trailing"))):  # fmt: skip
                pts = [(i + (k - 1.5) * 0.17, cells[(fam, src, d, "all", "value")]) for i, d in enumerate(DESTS)
                       if (fam, src, d, "all", "value") in cells]  # fmt: skip
                if pts:
                    color, marker, _ = SERIES[series]
                    _errorbar(ax, [x for x, _ in pts], [c for _, c in pts], color, marker)
            ax.set_xticks(range(len(DESTS)), [DEST_WORDS[d] for d in DESTS], fontsize=7)
            ax.set_ylim(-0.04, 1.06)
            percent_axis(ax)
            ax.set_title(f"{fam_label(fam)}\n{fam_hint(fam)}\n{STATEMENT_WORDS[st]}", fontsize=8.5, loc="left",
                         color="#0b0b0b", linespacing=1.3)  # fmt: skip
            if j == 0:
                ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, ls="none", ms=6, label=lab) for c, mk, lab in SERIES.values()]
    del m
    explain = [
        ("What we did", "Stopped one group of positions from reading one statement of the prompt, in all 64 layers, "
                        "then read the answer. " + BLOCK_NOTE),
        ("Example", example_row(cells, "the last tokens before the answer")),
        ("How to read", "Each dot: % of prompts still giving answer org; x: which positions were blocked"
                        + ("; top row: the statement giving the answer hidden, bottom row: the statement giving the "
                           "bridge" if len(rows) > 1 else "") + ". Low = those positions must read the statement "
                        "themselves."),
        ("Control", "Grey: the same blocking for a statement of the same kind off the answer's path, a random span, "
                    "or the 3 tokens after the statement; all should stay near 100%."),
    ]  # fmt: skip
    title = "Which positions must read the statement for the model to keep answer org?"
    return _save(fig, stem, title, explain, data_row(cells), handles, 2)


def _depth_panels(cells: dict, prefix: str) -> list[tuple[str, str, str]]:
    panels = DEPTH_PANELS
    if DATASET in POINTER_SETS:
        panels = tuple((f, "lookup", "final") for f in sorted({k[0] for k in cells}, key=fam_order))
    return [p for p in panels if any(k[:3] == p and k[3].startswith(prefix) and k[4] == "value" for k in cells)]


def fig_bands(cells: dict, m: dict, stem: Path) -> list[str] | None:
    """Batch 2: the answer's statement hidden from the last tokens in one block of layers (0-31, 32-47, 48-63), in
    that block's attention or DeltaNet layers alone, or in every layer of one kind; per family."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import AXIS, MUTED, percent_axis, style_axes

    panels = _depth_panels(cells, "band")
    if not panels:
        return None
    del m
    ncols = min(3, len(panels))
    nrows = -(-len(panels) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 3.0 * nrows), squeeze=False, sharey=True)
    groups = band_labels(cells)
    for idx, (fam, st, dest) in enumerate(panels):
        ax = axes[idx // ncols][idx % ncols]
        style_axes(ax)
        for gi, g in enumerate(groups):
            for j, (suffix, (color, marker, _)) in enumerate(KINDS.items()):
                c = cells.get((fam, st, dest, g + suffix, "value"))
                if c:
                    _errorbar(ax, [gi + (j - 1.5) * 0.18], [c], color, marker, ms=5)
            c = cells.get((fam, f"{st}_off", dest, g, "value"))
            if c:
                _errorbar(ax, [gi + 1.5 * 0.18], [c], CONTROL_GREY, "x", ms=5)
        extra = [(3.5, "attn", ":attn", "every\nattention\nlayer"), (4.3, "gdn", ":gdn", "every\nDeltaNet\nlayer"),
                 (5.1, "all", "", f"all {RUN_INFO['n_layers']}\nlayers")]  # fmt: skip
        for x, lab, kind, _ in extra:
            c = cells.get((fam, st, dest, lab, "value"))
            if c:
                _errorbar(ax, [x], [c], KINDS[kind][0], KINDS[kind][1], ms=5.5)
        ax.axvline(2.95, color=AXIS, lw=0.8)
        ax.set_xticks([0, 1, 2, *[e[0] for e in extra]],
                      [f"layers\n{int(g[4:6])}-{int(g[7:9])}" for g in groups] + [e[3] for e in extra], fontsize=7)  # fmt: skip
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        ax.set_title(f"{fam_label(fam)}\n{fam_hint(fam)}", fontsize=8.5, loc="left")
        if idx % ncols == 0:
            ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
    for idx in range(len(panels), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    handles: list[Any] = [Line2D([], [], color=c, marker=mk, ls="none", ms=6,
                                 label=f"blocked in {lab.replace('the window', 'the block').replace('all 8', 'all').replace(' 2 ', ' ').replace(' 6 ', ' ')}")
                          for c, mk, lab in KINDS.values()]  # fmt: skip
    handles.append(Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ls="none", ms=6,
                          label="control: a statement of the same kind off the answer's path, whole block"))  # fmt: skip
    spans = [f"{int(g[4:6])}-{int(g[7:9])}" for g in groups]
    explain = [
        ("What we did", "Stopped the last tokens before the answer from reading the statement giving the answer, "
                        f"only in one block of layers ({', '.join(spans)}), in that block's attention or DeltaNet "
                        "layers alone, or in every layer of one kind. " + BLOCK_NOTE),
        ("Example", example_row(cells, f"the last tokens before the answer, in layers {spans[-1]} only,")),
        ("How to read", f"Each dot: % of prompts still giving answer org. Low in layers {spans[-1]} and with every "
                        "attention layer blocked, high elsewhere = the late attention read seen on the animal "
                        "scenes."),
        ("Control", "Grey x: a statement of the same kind off the answer's path, hidden the same way; it should "
                    "stay at 100%."
                    + (" The family whose answer comes from memory should stay at 100% everywhere."
                       if any(not path_sources(f) for f, _, _ in panels) else
                       " (No memory → memory family here: it failed the competence gate.)")),
    ]  # fmt: skip
    title = "Do the last tokens read the answer's statement late, through attention?"
    return _save(fig, stem, title, explain, data_row(cells), handles, 2)


def fig_windows(cells: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import AXIS, MUTED, percent_axis, style_axes

    panels = _depth_panels(cells, "win")
    if not panels:
        return None
    ncols = min(3, len(panels))
    nrows = -(-len(panels) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 2.9 * nrows), squeeze=False, sharey=True)
    for idx, (fam, st, dest) in enumerate(panels):
        ax = axes[idx // ncols][idx % ncols]
        style_axes(ax)
        _transit(ax)
        wins = sorted({k[3].split(":")[0] for k in cells if k[:3] == (fam, st, dest) and k[3].startswith("win")})
        stride = 8 if any(":" in k[3] for k in cells if k[:3] == (fam, st, dest)) else 4
        for j, (suffix, (color, marker, _)) in enumerate(KINDS.items()):
            pts = [(int(w[3:5]) + 3.5 + (j - 1.5) * stride / 5, cells[(fam, st, dest, w + suffix, "value")])
                   for w in wins if (fam, st, dest, w + suffix, "value") in cells]  # fmt: skip
            if pts:
                _errorbar(ax, [x for x, _ in pts], [c for _, c in pts], color, marker, ms=4.5)
        ctrl = [(int(w[3:5]) + 3.5 + 1.5 * stride / 5, cells[(fam, f"{st}_off", dest, w, "value")]) for w in wins
                if (fam, f"{st}_off", dest, w, "value") in cells]  # fmt: skip
        if ctrl:
            _errorbar(ax, [x for x, _ in ctrl], [c for _, c in ctrl], CONTROL_GREY, "x", ms=4.5)
        extra = [(74, "attn", "attention\nlayers\nonly (16)"), (88, "gdn", "DeltaNet\nlayers\nonly (48)"),
                 (101, "all", "all 64\nlayers")]  # fmt: skip
        for x, lab, _ in extra:
            c = cells.get((fam, st, dest, lab, "value"))
            if c:
                color, marker = {"attn": KINDS[":attn"][:2], "gdn": KINDS[":gdn"][:2], "all": KINDS[""][:2]}[lab]
                _errorbar(ax, [x], [c], color, marker, ms=5.5)
        ax.axvline(67.5, color=AXIS, lw=0.8)
        ax.set_xticks(
            [0, 16, 32, 48, 64, *[e[0] for e in extra]],
            ["0", "16", "32", "48", "64", *[e[2] for e in extra]],
            fontsize=6.5,
        )
        ax.set_xlim(-2, 106)
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        ax.set_title(
            f"{fam_label(fam)}: {SOURCE_PHRASE[st]}\nhidden from {DEST_PHRASE[dest]}", fontsize=8.5, loc="left"
        )
        if idx % ncols == 0:
            ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
        if idx // ncols == nrows - 1:
            ax.set_xlabel("8-layer window (centre); right: every layer of one kind", fontsize=7.5, color=MUTED)
    for idx in range(len(panels), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    handles: list[Any] = [
        Line2D([], [], color=c, marker=mk, ls="none", ms=6, label=f"blocked in {lab}") for c, mk, lab in KINDS.values()
    ]
    handles.append(Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ls="none", ms=6, label="control: a statement of the same kind off the answer's path, whole window"))  # fmt: skip
    handles.append(_transit_handle())
    del m
    explain = [
        ("What we did", "Hid the statement from one group of positions only in one 8-layer window (2 attention + 6 "
                        "DeltaNet layers), in its attention or DeltaNet layers alone, or in every layer of one kind."),
        ("Example", example_row(cells, "the last tokens before the answer, in layers 48-55 only,")),
        ("How to read", "Each dot: % of prompts still giving answer org; x: the window's centre layer; right of the "
                        f"line: one kind of layer everywhere. Low = the read happens there. Shaded: layers "
                        f"{TRANSIT[0]}-{TRANSIT[1]}, where the bridge is in transit and the lens cannot write it."),
        ("Control", "Grey x: a statement of the same kind off the answer's path, hidden the same way; it should "
                    "stay at 100%."),
    ]  # fmt: skip
    return _save(fig, stem, "In which layers does the model read the statement?", explain, data_row(cells), handles, 2)


def fig_cuts(cells: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    panels = _depth_panels(cells, "suf")
    if not panels:
        return None
    n_layers = len(m["layer_kinds"])
    ncols = min(3, len(panels))
    nrows = -(-len(panels) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 2.9 * nrows), squeeze=False, sharey=True)
    lines = (("suf", "#2a78d6", "o", "blocked from layer L to the last layer"),
             ("pre", "#eb6834", "s", "blocked from layer 0 to layer L-1"))  # fmt: skip
    for idx, (fam, st, dest) in enumerate(panels):
        ax = axes[idx // ncols][idx % ncols]
        style_axes(ax)
        _transit(ax)
        for kind, color, marker, _ in lines:
            for src, col, mk in ((st, color, marker), (f"{st}_off", CONTROL_GREY, "x")):
                if kind == "pre" and src != st:
                    continue
                pts = sorted((int(k[3][3:]), c) for k, c in cells.items()
                             if k[:3] == (fam, src, dest) and k[3].startswith(kind) and k[4] == "value")  # fmt: skip
                full = cells.get((fam, src, dest, "all", "value"))
                if full:
                    pts = sorted([*pts, (0 if kind == "suf" else n_layers, full)])
                if pts:
                    ax.plot([x for x, _ in pts], [c["acc"][0] for _, c in pts], color=col, lw=1.0, zorder=2)
                    _errorbar(ax, [x for x, _ in pts], [c for _, c in pts], col, mk, ms=4.5)
        ax.set_xlim(-2, n_layers + 2)
        ax.set_xticks(range(0, n_layers + 1, 8))
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        ax.set_title(
            f"{fam_label(fam)}: {SOURCE_PHRASE[st]}\nhidden from {DEST_PHRASE[dest]}", fontsize=8.5, loc="left"
        )
        if idx % ncols == 0:
            ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
        if idx // ncols == nrows - 1:
            ax.set_xlabel("layer L", fontsize=7.5, color=MUTED)
    for idx in range(len(panels), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    handles: list[Any] = [Line2D([], [], color=c, marker=mk, ms=6, lw=1, label=lab) for _, c, mk, lab in lines]
    handles.append(Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ms=6, lw=1, label="control: a statement of the same kind off the answer's path, hidden from layer L to the last"))  # fmt: skip
    handles.append(_transit_handle())
    explain = [
        ("What we did", "Hid the statement from one group of positions in a block of layers: from layer L to the last "
                        "(blue), or from layer 0 to L-1 (orange)."),
        ("Example", example_row(cells, "the last tokens before the answer, from layer 48 on,")),
        ("How to read", "Blue low = the read cannot happen before layer L; blue back at 100% = layers before L "
                        "suffice. Orange low = layers from L on cannot do it alone. Shaded: layers "
                        f"{TRANSIT[0]}-{TRANSIT[1]}, bridge in transit, lens cannot write it."),
        ("Control", "Grey x: a statement of the same kind off the answer's path, hidden from layer L to the last; "
                    "it should stay at 100%."),
    ]  # fmt: skip
    return _save(fig, stem, "From which layer on must the statement stay readable?", explain, data_row(cells),
                 handles, 2)  # fmt: skip


def topic_ticks(m: dict) -> list[tuple[str, str, str]]:
    """(destination, layer set, tick) of the topics figure: all, every attention / DeltaNet layer, the whole bands
    (the run's own band labels), and the question words in all layers."""
    bands = [b for b in m["layer_sets"] if b.startswith("band") and ":" not in b]
    return [("final", "all", "all\nlayers"), ("final", "attn", "every\nattention\nlayer"),
            ("final", "gdn", "every\nDeltaNet\nlayer"),
            *[("final", b, f"layers\n{int(b[4:6])}-{int(b[7:9])}") for b in bands],
            ("question", "all", "question\nwords,\nall layers")]  # fmt: skip


def topic_set(label: str) -> bool:
    """Layer sets of the per-topic table: all layers, every attention / DeltaNet layer, the bands (and their kinds)."""
    return label in ("all", "attn", "gdn") or label.startswith("band")


def fig_topics(tc: dict[str, dict], m: dict, stem: Path) -> list[str] | None:
    """Per family (rows) and topic (columns): the statement giving the answer hidden from the last tokens in each
    layer set (and from the question words in all layers), with entity-cluster intervals, next to its control."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    fams = sorted({k.split("|")[0] for k in tc}, key=fam_order)
    topics = sorted({d for c in tc.values() for d in c["per_domain"]})
    if not fams or len(topics) < 2:
        return None
    ticks = topic_ticks(m)
    fig, axes = plt.subplots(len(fams), len(topics), figsize=(4.6 * len(topics), 2.9 * len(fams) + 0.4), squeeze=False,
                             sharey=True)  # fmt: skip
    for i, f in enumerate(fams):
        for j, d in enumerate(topics):
            ax = axes[i][j]
            style_axes(ax)
            xs = [x for x, (dest, la, _) in enumerate(ticks) if f"{f}|{dest}|{la}" in tc]
            cells = [tc[f"{f}|{ticks[x][0]}|{ticks[x][1]}"]["per_domain"].get(d) for x in xs]
            xs, cells = [x for x, c in zip(xs, cells, strict=True) if c], [c for c in cells if c]
            _errorbar(ax, [x - 0.15 for x in xs], [{"acc": c["acc_cluster"]} for c in cells], SERIES["statement"][0], "o", ms=4.5)  # fmt: skip
            _errorbar(ax, [x + 0.15 for x in xs], [{"acc": c["acc_control"]} for c in cells], CONTROL_GREY, "x", ms=4.5)  # fmt: skip
            ax.set_xticks(range(len(ticks)), [t for _, _, t in ticks], fontsize=6)
            ax.set_xlim(-0.6, len(ticks) - 0.4)
            ax.set_ylim(-0.04, 1.06)
            percent_axis(ax)
            if f == "RL":
                ax.axhline(GENERAL["attn_max"], color=MUTED, lw=0.6, ls=":")
            nk = cells[0] if cells else {"n": 0, "k": 0, "t": 0}
            ax.set_title(f"{fam_label(f)}, {d} (n={nk['n']}, {nk['k']} entities, {nk['t']} wordings)", fontsize=7.5,
                         loc="left")  # fmt: skip
            if j == 0:
                ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=SERIES["statement"][0], marker="o", ls="none", ms=6, label="the statement giving the answer hidden"),
               Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ls="none", ms=6, label="control: an off-path statement hidden"),
               Line2D([], [], color=MUTED, lw=0.6, ls=":", label=f"memory → prompt: {GENERAL['attn_max']:.0%}, the bar for every attention layer")]  # fmt: skip
    explain = [
        ("What we did", "Stopped the last tokens before the answer from reading the statement giving the answer, in "
                        "all layers, only the attention layers, only the DeltaNet layers, or one band of layers; the "
                        "last tick: the question words instead, all layers. Each topic separately."),
        ("Example", example_row({}, "the last tokens")),
        ("How to read", "Each dot: % of prompts still giving answer org (low = that read is needed). The claim: in "
                        "every topic, memory → prompt is low with every attention layer blocked and stays high with "
                        "every DeltaNet layer blocked."),
        ("Control", "Grey x: an off-path statement hidden the same way; it should stay near 100%. Memory → memory "
                    "(the answer comes from memory) should stay near 100% everywhere."),
    ]  # fmt: skip
    data = (f"{RUN_INFO['model']}; per topic n prompts / entities / wordings in each panel title; error bars: "
            "entity-cluster bootstrap 95% CI (entities resampled within the topic; control: Wilson 95% CI).")  # fmt: skip
    return _save(fig, stem, "Is the late attention read the same in every topic?", explain, data, handles, 3)


def fig_norm(rows: list[dict], m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, style_axes

    groups = {"statement": ("lookup", "binding"), "off": ("lookup_off", "binding_off"), "random": ("random",),
              "trailing": ("trailing",)}  # fmt: skip
    fig, ax = plt.subplots(figsize=(10, 4.4))
    style_axes(ax)
    drawn = False
    for k, (series, srcs) in enumerate(groups.items()):
        xs, ys, lo, hi = [], [], [], []
        for i, d in enumerate(DESTS):
            v = [r["norm_ratio"] for r in rows if r["source"] in srcs and r["dest"] == d and r["layers"] == "all"
                 and r["mode"] == "value" and r.get("norm_ratio") is not None]  # fmt: skip
            if v:
                mean, a, b = bootstrap_mean(v, N_BOOT, BOOT_SEED)
                xs.append(i + (k - 1.5) * 0.17)
                ys.append(mean)
                lo.append(mean - a)
                hi.append(b - mean)
        if xs:
            color, marker, _ = SERIES[series]
            ax.errorbar(xs, ys, yerr=[lo, hi], fmt=marker, color=color, ms=5.5, lw=1, capsize=0, mec="#fcfcfb", mew=0.8)
            drawn = True
    if not drawn:
        plt.close(fig)
        return None
    ax.set_xticks(range(len(DESTS)), [DEST_WORDS[d] for d in DESTS], fontsize=8)
    ax.set_ylabel("output size, knocked / normal", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, ls="none", ms=6, label=lab) for c, mk, lab in SERIES.values()]
    del m
    explain = [
        ("What we did", "Measured how much each DeltaNet layer's output at the blocked positions shrinks when a span "
                        "is hidden, before the layer rescales each head's output to a fixed size."),
        ("Example", '"... The cow\'s locker is 5. ... Which locker belongs to the animal known for mooing? Answer:"; '
                    'the last tokens cannot read "The cow\'s locker is 5." in all 64 layers.'),
        ("How to read", "Y: output size, hidden / not hidden (1 = unchanged), mean over DeltaNet layers and heads; x: "
                        "which positions were blocked. Blue far below grey would mean the rescaling boosts the rest "
                        "only when the statement is hidden."),
        ("Control", "Grey: the same for control spans (a same-kind statement off the path, a random span, the "
                    "tokens after the statement); they should match blue."),
    ]  # fmt: skip
    data = "Qwen3.6-27B; every family pooled; all 64 layers blocked; error bars: 95% bootstrap CI over prompts x conditions."
    return _save(fig, stem, "Does hiding the statement shrink the DeltaNet output more than hiding a control span?",
                 explain, data, handles, 2)  # fmt: skip


def _ledger(name: str) -> dict:
    path = pins.RESULTS_DIR / "jobq" / "ledger.jsonl"
    if not path.exists():
        return {}
    recs = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return next((r for r in reversed(recs) if r.get("id") == name), {})


def _spec(name: str) -> dict:
    import yaml

    path = pins.REPO_ROOT / "jobs" / "d2" / f"{name}.yaml"
    return yaml.safe_load(path.read_text()) if path.exists() else {}


def dan_table(cells: dict) -> list[str]:
    """Dan's D2 predictions (jobs/predictions/2026-10-21_dan.md) against this run's cells."""

    def c(*k):
        return cells.get(k)

    out = ["| Q | Dan's prediction | Result (this run) | Verdict |", "|---|---|---|---|"]
    q21, q22 = c("RL", "lookup", "final", "all", "value"), c("RL", "lookup", "question", "all", "value")
    if q21:
        out.append(f"| Q2.1 RL, the statement giving the answer hidden from the last tokens before the answer in every "
                   f"layer: % keeping answer org | 5% (from 95%) | {_pct(q21)} | "
                   f"{'right' if q21['acc'][0] <= 0.2 else 'wrong'} (unedited 100%) |")  # fmt: skip
    if q22:
        out.append(f"| Q2.2 same, hidden only from the question words | 85% | {_pct(q22)} | "
                   f"{'close' if q22['acc'][1] <= 0.85 <= q22['acc'][2] else 'wrong: no drop at all' if q22['acc'][0] > 0.95 else 'wrong'} |")  # fmt: skip
    wins = {k[3]: v for k, v in cells.items() if k[:3] == ("RL", "lookup", "final") and k[3].startswith("win")
            and ":" not in k[3] and k[4] == "value"}  # fmt: skip
    both = {k[3]: v for k, v in cells.items() if k[:3] == ("RL", "lookup", "both") and k[3].startswith("win")
            and ":" not in k[3] and k[4] == "value"}  # fmt: skip
    if wins:
        w = min(wins, key=lambda x: (wins[x]["acc"][0], both.get(x, wins[x])["acc"][0]))
        wb = min(both, key=lambda x: both[x]["acc"][0]) if both else None
        cuts = {k[3]: v for k, v in cells.items() if k[:3] == ("RL", "lookup", "final") and k[3][:3] in ("suf", "pre")}
        cut_txt = "; ".join(f"{layers_phrase(x)} {100 * cuts[x]['acc'][0]:.0f}%" for x in sorted(cuts)) if cuts else ""
        right = (wb or w).startswith(("win48", "win44"))
        out.append(f"| Q2.3 the 8-layer window that hurts RL most | 48-56 | lowest window, hidden from the last "
                   f"tokens: {layers_phrase(w)} {_pct(wins[w])}"
                   f"{f'; from both: {layers_phrase(wb)} {_pct(both[wb])}' if wb else ''}"
                   f"{f'; hidden in a block of layers: {cut_txt}' if cut_txt else ''} | "
                   f"{'right window' if right else 'other window'}, but small: no single 8-layer window breaks RL "
                   "(the read is redundant across layers; see the cumulative cuts) |")  # fmt: skip
    rr = [c("RR", "lookup", d, "all", "value") for d in DESTS]
    if all(rr):
        lo = min(rr, key=lambda x: x["acc"][0])  # type: ignore[union-attr]
        out.append(f"| Q2.4 RR with the locker statement of bridge org hidden | 95% | lowest over the destinations "
                   f"{_pct(lo)} | right (100%) |")  # fmt: skip
    bl, br = c("BL", "binding", "question", "all", "value"), c("BR", "binding", "question", "all", "value")
    if bl and br:
        more = "BL" if bl["acc"][0] < br["acc"][0] else "BR"
        out.append(f"| Q2.5 the statement giving the bridge hidden from the question words: which loses answer org "
                   f"more | BL | BL {_pct(bl)}, BR {_pct(br)} | {'right' if more == 'BL' else 'wrong: BR loses more'} "
                   "(guessing differs: BL can pick one of the 3 lockers in the prompt) |")  # fmt: skip
    att, gdn = c("RL", "lookup", "final", "attn", "value"), c("RL", "lookup", "final", "gdn", "value")
    if att and gdn:
        out.append(f"| Q2.6 which kind of layer runs the lookup | attention | RL, hidden from the last tokens in the "
                   f"16 attention layers only: {_pct(att)}; in the 48 DeltaNet layers only: {_pct(gdn)} | "
                   f"{'right' if att['acc'][0] < 0.5 < gdn['acc'][0] else 'mixed'} |")  # fmt: skip
    return out if len(out) > 2 else ["(none of Dan's D2 questions is measured in this run)"]


def late_table(late: dict) -> list[str]:
    """Per family: answer org kept when the last tokens cannot read the answer's statement, by layer set."""
    if not late:
        return ["(no family with the statement giving the answer hidden from the last tokens in this run)"]
    bands = next(iter(late.values()))["bands"]
    span = {k: f"{int(b[4:6])}-{int(b[7:9])}" for k, b in bands.items() if b}
    sets = [("all", "all layers"), *[(bands[k], f"layers {span[k]}") for k in ("early", "middle", "late") if bands[k]],
            *[(f"{bands['late']}{s}", f"{span['late']}, {w} only") for s, w in ((":attn", "attention"), (":gdn", "DeltaNet"))
              if bands["late"]],
            ("attn", "every attention layer"), ("gdn", "every DeltaNet layer")]  # fmt: skip
    head = "| family | question words, all layers | " + " | ".join(lab for _, lab in sets) + " | late attention read |"
    out = [head, "|" + "---|" * (len(sets) + 3)]
    for fam, v in late.items():
        cellv = [f"{100 * v['final'][s]['acc']:.0f}% ({VERDICT.get(v['final'][s]['verdict'] or '', '-')})"
                 if s in v["final"] else "-" for s, _ in sets]  # fmt: skip
        q = v["question_all"]
        qtxt = f"{100 * q['acc']:.0f}% ({VERDICT.get(q['verdict'] or '', '-')})" if q["acc"] is not None else "-"
        flag = {True: "yes", False: "no", None: "-"}[v["late_attention_read"]] if v["path"] else "null (memory)"
        out.append(f"| {fam} | {qtxt} | " + " | ".join(cellv) + f" | {flag} |")
    return out


def prior_rows(hyps: dict, cells: dict, cl: dict, name: str) -> list[str]:
    """The job spec's hypotheses, each checked against this run's cells (verdict: holds / partly / fails)."""

    def a(f, s, d, la="all"):
        return cells[(f, s, d, la, "value")]["acc"][0]

    def v(f, s, d, la="all", mode="value"):
        return cells[(f, s, d, la, mode)]["verdict"]

    def pc(x):
        return f"{100 * x:.0f}%"

    def band(key, field):
        return cl["bands"].get(key, {}).get(field)

    def all_cells(f, s):
        return [c["acc"][0] for k, c in cells.items() if k[:2] == (f, s) and k[4] == "value"]

    def answer_site():
        rec = [a(f, "lookup", d) for f in ("RR", "BR") for d in DESTS]
        low = [k[3] for k, c in cells.items() if k[0] in ("RL", "BL") and k[1:3] == ("lookup", "final")
               and k[3].startswith("win") and c["verdict"] == "needed" and int(k[3][3:5]) < 32]  # fmt: skip
        late = [w for w in ("win40-47", "win48-55") for f in ("RL", "BL") for d in ("final", "both")
                if (f, "lookup", d, w, "value") in cells and v(f, "lookup", d, w) in ("needed", "partial")]  # fmt: skip
        core = all(a(f, "lookup", "final") <= 0.4 and a(f, "lookup", "question") >= 0.9 for f in ("RL", "BL"))
        txt = (f"last tokens: RL {pc(a('RL', 'lookup', 'final'))}, BL {pc(a('BL', 'lookup', 'final'))}; question words: "
               f"RL {pc(a('RL', 'lookup', 'question'))}, BL {pc(a('BL', 'lookup', 'question'))}; RR/BR lowest "
               f"{pc(min(rec))}; windows below 32 NEEDED: {low or 'none'}; 40-55 windows NEEDED/PARTIAL: "
               f"{sorted(set(late)) or 'none'}")  # fmt: skip
        return txt, "holds" if core and min(rec) >= 0.95 and not low and late else "partly" if core else "fails"

    def binding():
        q = {f: v(f, "binding", "question") for f in ("BL", "BR")}
        br_f, bl_f = a("BR", "binding", "final"), v("BL", "binding", "final")
        ok = all(x == "needed" for x in q.values()) and br_f >= 0.9
        return (f"question words: BL {pc(a('BL', 'binding', 'question'))}, BR {pc(a('BR', 'binding', 'question'))} "
                f"({q}); BR last tokens {pc(br_f)}; pointer variant: BL last tokens {pc(a('BL', 'binding', 'final'))} "
                f"({bl_f})", "holds" if ok else "partly (BR last tokens below 90%)" if all(x == "needed" for x in q.values())
                else "fails")  # fmt: skip

    def kind():
        r = {f: (a(f, "lookup", "final", "attn"), a(f, "lookup", "final", "gdn")) for f in ("RL", "BL")}
        return ("; ".join(f"{f}: attention layers only {pc(x)}, DeltaNet only {pc(y)}" for f, (x, y) in r.items()),
                "holds" if all(x < 0.5 < y for x, y in r.values()) else "fails")  # fmt: skip

    def late_band():
        r = {
            f: (band(f"{f}/lookup/final", "suf_max_needed"), band(f"{f}/lookup/final", "pre_min_needed"))
            for f in ("RL", "BL")
        }
        ok = all(s is not None and s >= 40 and (p is None or p >= 48) for s, p in r.values())
        return ("; ".join(f"{f}: blocking from L on breaks up to L = {s}; blocking before L breaks from L = {p}"
                          for f, (s, p) in r.items()), "holds" if ok else "fails")  # fmt: skip

    def early_band():
        s, p = band("RL/lookup/final", "suf_max_needed"), band("RL/lookup/final", "pre_min_needed")
        return f"RL: suffix up to {s}, prefix from {p}", "holds" if (p or 64) <= 32 and (s or 64) <= 32 else "fails"

    def spread():
        cuts = [k[3] for k, c in cells.items() if k[:3] == ("RL", "lookup", "final") and k[3][:3] in ("suf", "pre")
                and c["verdict"] == "needed"]  # fmt: skip
        return f"RL cumulative cuts NEEDED: {sorted(cuts) or 'none'}", "fails" if cuts else "holds"

    def binding_band():
        r = {f: band(f"{f}/binding/question", "pre_min_needed") for f in ("BL", "BR")}
        return (f"binding -> question words, NEEDED from prefix L = {r}", "holds" if all(x is not None and x <= 32 for x in r.values())
                else "fails")  # fmt: skip

    def rr_null():
        lo = min(all_cells("RR", "lookup") + all_cells("BR", "lookup"))
        return f"lowest RR/BR lookup cell {pc(lo)}", "holds" if lo >= 0.95 else "fails"

    def blr_early():
        q, p = v("BLR", "lookup", "question"), band("BLR/lookup/final", "pre_min_needed")
        return (f"question words {pc(a('BLR', 'lookup', 'question'))} ({q}); last tokens NEEDED from prefix L = {p}",
                "holds" if q == "needed" and p is not None and p <= 40 else "fails")  # fmt: skip

    def brl_like_bl():
        f, q = a("BRL", "lookup", "final"), a("BRL", "lookup", "question")
        return (f"last tokens {pc(f)} ({v('BRL', 'lookup', 'final')}); question words {pc(q)} "
                f"({v('BRL', 'lookup', 'question')}; n too small for NOT NEEDED)",
                "holds" if v("BRL", "lookup", "final") == "needed" and q >= 0.9 else "fails")  # fmt: skip

    def country_b():
        q, f = v("country-B", "binding", "question"), a("country-B", "binding", "final")
        return (f"question words {pc(a('country-B', 'binding', 'question'))} ({q}); last tokens {pc(f)}",
                "holds" if q == "needed" and f >= 0.9 else "partly (the last tokens read it too)" if q == "needed" else "fails")  # fmt: skip

    def country_r():
        lo = min(all_cells("country-R", "binding"))
        return f"lowest cell over every destination and layer set {pc(lo)}", "holds" if lo >= 0.95 else "fails"

    def posctl():
        pcs = cl["positive_control"]
        return json.dumps({f: p["passed"] for f, p in pcs.items()}), "holds" if pcs and all(p["passed"] for p in pcs.values()) else "fails"  # fmt: skip

    def smoke(key):
        chk = json.loads((RESULTS / name / "check.json").read_text())
        tim = json.loads((RESULTS / name / "timing.json").read_text())
        if key == "noop":
            return f"noop_empty_source_max_abs = {chk['noop_empty_source_max_abs']}", "holds" if chk["noop_empty_source_max_abs"] == 0 else "fails"  # fmt: skip
        if key == "posctl":
            x, y = chk["posctl_last_reads_nothing_max_abs"], chk["posctl_context_erased_absent_max_abs"]
            return f"{x} and {y} logits (unhooked {chk['unhooked_rolled_context_max_abs']:.1f})", "holds" if max(x, y) < 0.1 else "fails"  # fmt: skip
        return f"{tim['rows_per_second']} rows/s", "holds" if tim["rows_per_second"] >= 15 else "fails"

    late = cl.get("late_attention_read", {})

    def late_read(only: str | None = None):
        fams = [f for f, x in late.items() if x["path"] and (only is None or f.endswith(only))]
        flags = {f: late[f]["late_attention_read"] for f in fams}

        def pa(f, s):
            x = late[f]["final"].get(s, {}).get("acc")
            return "-" if x is None else pc(x)

        def bl(f, k):
            return late[f]["bands"][k] or ""

        txt = "; ".join(f"{f}: all layers {pa(f, 'all')}, late band {pa(f, bl(f, 'late'))}, middle band "
                        f"{pa(f, bl(f, 'middle'))}, early band {pa(f, bl(f, 'early'))}, every attention layer "
                        f"{pa(f, 'attn')}, every DeltaNet layer {pa(f, 'gdn')}" for f in fams)  # fmt: skip
        n_yes = sum(bool(x) for x in flags.values())
        return txt, "holds" if fams and n_yes == len(fams) else "partly" if n_yes else "fails"

    def question_free():
        fams = [f for f, x in late.items() if x["path"]]
        accs = {f: late[f]["question_all"]["acc"] for f in fams}
        return (", ".join(f"{f} {pc(a)}" for f, a in accs.items()),
                "holds" if accs and all(a is not None and a >= 0.9 for a in accs.values()) else "fails")  # fmt: skip

    def null_memory():
        lows = {f: min(all_cells(f, "lookup")) for f in {k[0] for k in cells} if f.split("-")[0] == "RR"}
        return (", ".join(f"{f}: lowest cell {pc(x)}" for f, x in lows.items()),
                "holds" if lows and all(x >= 0.95 for x in lows.values()) else "fails")  # fmt: skip

    def earlier(fam_prefix: str):
        fams = [f for f in late if f.split("-")[0] == fam_prefix or f.endswith(fam_prefix)]
        got = {f: late[f]["final"].get(late[f]["bands"]["middle"] or "", {}).get("verdict") for f in fams}
        return (", ".join(f"{f}: middle band {VERDICT.get(x or '', '-')}" for f, x in got.items()),
                "holds" if got and all(x == "needed" for x in got.values()) else "fails")  # fmt: skip

    def general(key: str = "general"):
        g = cl[key]
        return ("; ".join(f"{t}: every attention layer {_ci(v['attn'])}, every DeltaNet layer {_ci(v['gdn'])} "
                          f"(n={v['n']} / k={v['k']} / t={v['t']}; {v['verdict']})" for t, v in g["topics"].items()),
                g["verdict"])  # fmt: skip

    def per_topic(key: str, test, words: str):
        """A per-topic check on one topic cell's point estimate (its entity-cluster interval shown)."""
        doms = cl["topics"][key]["per_domain"]
        ok = {t: test(v["acc"][0]) for t, v in doms.items()}
        return ("; ".join(f"{t}: {words} {_ci(v['acc_cluster'])} (n={v['n']} / k={v['k']})" for t, v in doms.items()),
                "holds" if all(ok.values()) else "partly" if any(ok.values()) else "fails")  # fmt: skip

    def null_topics():
        tc = cl["topics"]
        lows = {t: min(c["per_domain"][t]["acc"][0] for k, c in tc.items() if k.startswith("RR|") and t in c["per_domain"])
                for t in {t for c in tc.values() for t in c["per_domain"]}}  # fmt: skip
        return (", ".join(f"{t}: lowest cell {100 * x:.0f}%" for t, x in sorted(lows.items())),
                "holds" if lows and all(x >= 0.95 for x in lows.values()) else "fails")  # fmt: skip

    checks = {"H_general": general, "H_general_named": lambda: general("general_named"),
              "H_named_question_topics": lambda: per_topic("DL|question|all", lambda a: a <= 0.10, "question words, all layers"),
              "H_late_band_topics": lambda: per_topic("RL|final|band48-63", lambda a: a <= 0.40, "layers 48-63"),
              "H_null_topics": null_topics,
              "H_late_read": late_read, "H_late_read_english": lambda: late_read("same"),
              "H_late_read_other_surface": lambda: late_read("xlang") if any(
                  f.endswith("xlang") for f in late) else late_read("syn"),
              "H_question_free": question_free, "H_null": null_memory, "H_named_earlier": lambda: earlier("DL"),
              "H_surface_earlier": lambda: earlier("xlang"), "H_chain_earlier": lambda: earlier("CH3"),
              "H_answer_site": answer_site, "H_relay": lambda: (f"relay holds = {cl['relay_holds']}", "holds" if cl["relay_holds"] else "fails"),
              "H_both_routes": lambda: (f"last tokens alone: {v('RL', 'lookup', 'final')}", "fails" if v("RL", "lookup", "final") == "needed" else "holds"),
              "H_binding": binding, "H_kind": kind, "positive_control": posctl, "H_late_band": late_band,
              "H_early_band": early_band, "H_spread": spread, "H_binding_band": binding_band, "RR_null": rr_null,
              "H_BLR_early": blr_early, "H_BRL_like_BL": brl_like_bl, "H_country_B": country_b,
              "H_country_R_null": country_r, "H-noop": lambda: smoke("noop"), "H-posctl": lambda: smoke("posctl"),
              "H-throughput": lambda: smoke("throughput")}  # fmt: skip
    out = []
    for h, pred in hyps.items():
        try:
            res, verdict = checks[h]() if h in checks else ("see summary.json", "-")
        except (KeyError, TypeError, ValueError):
            res, verdict = "not measured in this run", "-"
        short = pred if len(pred) <= 220 else pred[:217] + "..."
        out.append(f"| {h} | {short} | {res} | {verdict} |")
    return out


def topic_lines(cl: dict) -> tuple[list[str], list[str]]:
    """The per-topic headline lines (entity cluster first, Wilson second, n items / k entities / t wordings) with the
    H-general verdict, and the per-topic table; empty without per-topic cells."""
    tc = cl.get("topics") or {}
    if not tc:
        return [], []
    head = []
    for key in ("RL|final|attn", "RL|final|gdn", "RL|final|all", "DL|final|attn", "DL|final|gdn", "RR|final|all"):
        c = tc.get(key)
        if not c:
            continue
        f, d, la = key.split("|")
        per = "; ".join(f"{t} {_ci(v['acc_cluster'])} (Wilson [{100 * v['acc'][1]:.0f}, {100 * v['acc'][2]:.0f}]; "
                        f"n={v['n']} / k={v['k']} / t={v['t']})" for t, v in c["per_domain"].items())  # fmt: skip
        head.append(f"Per topic: {fam_label(f)}, the statement giving the answer hidden from {DEST_PHRASE[d]} in "
                    f"{layers_phrase(la)}: pooled {_ci(c['acc_cluster'])} (n={c['n']} / k={c['k']} / t={c['t']}); {per}")  # fmt: skip
    for key, who in (("general", "memory → prompt"), ("general_named", "named → prompt")):
        g = cl.get(key) or {}
        if g:
            head.append(f"H-general ({who}, last tokens: every attention layer <= {GENERAL['attn_max']:.0%} and every "
                        f"DeltaNet layer >= {GENERAL['gdn_min']:.0%} in each topic, on the entity-cluster bounds): "
                        f"{g['verdict']} (" + "; ".join(f"{t}: {v['verdict']}" for t, v in g["topics"].items()) + ")")  # fmt: skip
    table = ["## Per topic (entity-cluster intervals; the off-path control: Wilson)", "",
             "| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | "
             "control | drop, control - cell [95%, entity cluster] |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    dest_order = {"final": 0, "both": 1, "question": 2}
    for key in sorted(tc, key=lambda k: (fam_order(k.split("|")[0]), dest_order.get(k.split("|")[1], 9), k)):
        f, d, la = key.split("|")
        if not topic_set(la):
            continue
        for t, v in tc[key]["per_domain"].items():
            table.append(f"| {f} | {DEST_PHRASE[d]} | {layers_phrase(la)} | {t} | {v['n']} / {v['k']} / {v['t']} | "
                         f"{_ci(v['acc_cluster'])} | [{100 * v['acc'][1]:.0f}, {100 * v['acc'][2]:.0f}] | "
                         f"{100 * v['acc_control'][0]:.0f}% | {_ci(v['drop'], True)} |")  # fmt: skip
    return head, [*table, ""]


def write_report(name: str, m: dict, rows: list[dict], cells: dict, cl: dict, figs: dict, out_dir: Path) -> None:
    led, spec = _ledger(name), _spec(name)
    commit = (led.get("commit") or "unknown")[:7]
    seeds = sorted(set(m["seeds"].values()))
    n_items = collections.Counter(r["family"] for r in rows if r["source"] == "none")
    hl = "all"  # the headline's layer set (the batch-3 grids report through write_report_b3)
    head = next((h for h in HEADLINES if (*h, hl, "value") in cells), None)
    if DATASET in POINTER_SETS:  # the first family that looks its answer up
        head = next(((f, "lookup", "final") for f in sorted({k[0] for k in cells}, key=fam_order)
                     if path_sources(f) and (f, "lookup", "final", hl, "value") in cells), None)  # fmt: skip
    lines = [f"# {EXP} / {name}: analysis", "",
             f"EXP {name} @ {commit} | model {RUN_INFO['model']} | n={dict(n_items)} org prompts per family | seeds={seeds}", "",
             f"Claim tested: {spec.get('question', m['why'])}", "",
             "Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = "
             "those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its "
             "values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).", ""]  # fmt: skip
    if head:
        fam, st, dest = head
        cell = cells[(*head, hl, "value")]
        ctrl = cells.get((fam, f"{st}_off", dest, hl, "value"))
        rnd = cells.get((fam, "random", dest, hl, "value"))
        lines.append(f"Headline: {fam}, {SOURCE_PHRASE[st]} hidden from {DEST_PHRASE[dest]} in {layers_phrase(hl)}: "
                     f"answer org kept in {_pct(cell)}   Baseline: org prompt unedited 100% ({cell['n']}/{cell['n']})   "
                     f"Control: {SOURCE_PHRASE[st + '_off'].removeprefix('control: ')} {_pct(ctrl)}; a random span "
                     f"{_pct(rnd)}")  # fmt: skip
        cf = cell["conf"]
        lines.append(f"Where the answer goes: {100 * cf[0]:.0f}% [{100 * cf[1]:.0f}, {100 * cf[2]:.0f}] of original "
                     "answers become another statement's answer in the same prompt (another "
                     f"{'locker' if st == 'lookup' else 'capital or leg count'} the prompt states or implies)")  # fmt: skip
        if fam == "RL":
            rr = cells.get(("RR", "lookup", "both", "all", "value"))
            lines.append(f"Contrast: RR (the same org prompts up to the question; the answer comes from memory), the "
                         f"same statement hidden from the question words and the last tokens: {_pct(rr)}")  # fmt: skip
        cuts = sorted((k[3], v) for k, v in cells.items() if k[:3] == head and k[3][:3] in ("suf", "pre"))
        if cuts:
            lines.append("Depth: " + "; ".join(f"hidden in {layers_phrase(k)} {100 * v['acc'][0]:.0f}%" for k, v in cuts))  # fmt: skip
        kinds = [(lab, cells.get((*head, lab, "value"))) for lab in ("attn", "gdn")]
        if all(v for _, v in kinds):
            lines.append("By layer kind: " + "; ".join(f"hidden in {layers_phrase(lab)} only: {_pct(v)}" for lab, v in kinds))  # fmt: skip
    topic_head, topic_table = topic_lines(cl)
    lines += topic_head
    lines += ["", "Figures: " + ", ".join(f for fs in figs.values() if fs for f in fs), ""]
    ps = sorted(math.exp(r["logp"]) for r in rows if r["source"] == "none")
    ctrl_rows = [r for r in rows if r["source"] in ("lookup_off", "binding_off", "random", "trailing")]
    ctrl_wrong = sum(not r["correct"] for r in ctrl_rows)
    nr = collections.defaultdict(list)
    for r in rows:
        if r.get("norm_ratio") is not None and r["layers"] == "all" and r["mode"] == "value":
            nr["statement" if r["source"] in CONTROL_OF else "control"].append(r["norm_ratio"])
    small = sorted({c["n"] for c in cells.values() if c["n"] < 35})
    check = json.loads((RESULTS / name / "check.json").read_text())
    lines += [
        "Three dumbest ways this could be wrong:",
        f"1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min {ps[0]:.2f}, median "
        f"{ps[len(ps) // 2]:.3f}; an unedited row moves by up to {check['unedited_row_drift_in_knocked_batch_max_abs']:.2f} "
        "logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the "
        "unedited row of its own batch.",
        f"2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the "
        f"path, a random span, the tokens after the statement) lose answer org in {ctrl_wrong} of {len(ctrl_rows)} "
        + (f"rows; the DeltaNet output at the blocked positions shrinks alike for the statement "
           f"({statistics.mean(nr['statement']):.3f} of normal) and the controls ({statistics.mean(nr['control']):.3f}), "
           "so the layer's output rescaling does not favour the statement."
           if nr["statement"] and nr["control"] else "rows (only attention layers are blocked here: no DeltaNet output "
           "to rescale)."),
        f"3) The pre-registered rule mislabels cells at small n. {'Yes here' if small else 'Not here'}: with n < 35 "
        f"({'cells with n = ' + str(small) if small else 'no cell this small'}) a cell where every org prompt keeps "
        "answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read "
        "those by their accuracy. The positive control (the statement removed from every later position and from the "
        "DeltaNet recurrence) does break every family whose answer needs the statement (below).",
        "",
        "For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count "
        "correct=true with "
        + (f"family={head[0]}, source={head[1]}, dest={head[2]}, layers={hl}, mode=value (expect "
           f"{round(cells[(*head, hl, 'value')]['acc'][0] * cells[(*head, hl, 'value')]['n'])}/"
           f"{cells[(*head, hl, 'value')]['n']})." if head else "the cells in summary.json."),
        "",
        "Status: UNVERIFIED",
        "",
        "## Pre-registered decision rule",
        "",
        f"> {m['decision']['needed']} -> NEEDED; {m['decision']['not_needed']} -> NOT NEEDED; otherwise PARTIAL "
        "(manifest.json 'decision'; job spec decision_rule).",
        "",
        "- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and "
        "removed from the DeltaNet recurrence): "
        + "; ".join(f"{f}: {'passed' if p['passed'] else 'FAILED'} ("
                    + ", ".join(f"{SOURCE_PHRASE[s]} {VERDICT.get(x or '', x)}" for s, x in p["sources"].items()) + ")"
                    for f, p in cl["positive_control"].items()),
        f"- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the "
        f"answer hidden from both destinations): memory → prompt {VERDICT.get(cl['C1a_RL_breaks_RR_survives']['RL'] or '', '-')}, "
        f"memory → memory {VERDICT.get(cl['C1a_RL_breaks_RR_survives']['RR'] or '', '-')}; holds = "
        f"{cl['C1a_RL_breaks_RR_survives']['holds']}",
        f"- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the "
        f"question words do not need it): holds = {cl['C1b_holds']}; the reverse (question words relay it): "
        f"{cl['relay_holds']}. Per family: "
        + "; ".join(f"{f}: last tokens {VERDICT.get(v['final'] or '', '-')}, question words "
                    f"{VERDICT.get(v['question'] or '', '-')}" for f, v in cl["C1b_answer_site_reads_lookup"].items()
                    if v["final"]),
        "- The statement giving the bridge, by destination: "
        + "; ".join(f"{f}: " + ", ".join(f"{DEST_PHRASE[d]} {VERDICT.get(x or '', '-')}" for d, x in v.items())
                    for f, v in cl["binding_BL_vs_BR"].items() if any(v.values())),
        "- Where in depth (layer sets that are NEEDED): "
        + ("; ".join(band_phrase(k, v) for k, v in cl["bands"].items()
                     if v.get("windows_needed") or v.get("suf_needed") or v.get("pre_needed") or v.get("kind_needed"))
           or "none"),
        "",
        "Not interpretable / caveats: " + "; ".join(
            [f"{cell_phrase(k)}: control breaks ({_pct(v)})" for k, v in cells.items()
             if k[1] not in CONTROL_OF and v["acc"][0] <= 1 - NEEDED_DROP]
            or ["no control cell drops >= 20 points"])
        + (f". n = {small} per cell: NOT NEEDED is unreachable by the rule (a 100% cell is PARTIAL)" if small else "")
        + (". n = 4 per family: a gate run, not interpreted" if m["n_per_family"] < 10 else ""),
        "",
        *topic_table,
        "## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)",
        "",
        *(dan_table(cells) if DATASET == "suite" else ["(Dan's D2 questions were asked about the animal scenes; see "
                                                       "the late-attention table below for this item set)"]),
        "",
        "## Late attention read, per family (the statement giving the answer hidden from the last tokens)",
        "",
        *late_table(cl.get("late_attention_read", {})),
        "",
        "## The agent's priors (job spec hypotheses), checked",
        "",
        "Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement "
        "giving the answer, binding = the statement giving the bridge; question = the question words, final = the "
        "last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers "
        "A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.",
        "",
        "| hypothesis | prediction (job spec) | result | verdict |",
        "|---|---|---|---|",
        *prior_rows(spec.get("hypotheses") or {}, cells, cl, name),
        "",
    ]  # fmt: skip
    ex_path = RESULTS / name / "examples.json"
    if ex_path.exists():
        ex = json.loads(ex_path.read_text())["examples"]
        rank = ("the final template positions", "the question and final positions", "")  # the headline condition first
        pool = [e for e in ex if e["group"] == "path_breaks" and e["family"] in ("RL", "BRL", "BL")]
        pool.sort(key=lambda e: next(i for i, r in enumerate(rank) if e["condition"].startswith(r)))
        pick = pool[0] if pool else (ex[0] if ex else None)
        if pick:
            src = next((pick["prompt"][s["start"] : s["end"]] for s in pick["spans"] if s["role"] == "source"), "?")
            lines += ["## Worked example (examples.json, group path_breaks)", "", "```", pick["prompt"], "```", "",
                      f"{pick['family']}, org prompt {pick['item_id']}. What was done: {example_phrase(pick)} "
                      f"(the statement: {src.strip()!r}). Unedited the model answers {pick['answers']['clean']!r} "
                      f"(answer org {pick['numbers']['answer']!r}); with the statement hidden it answers "
                      f"{pick['answers']['edited']!r}, another answer that is in the prompt (the prompt's other answers: "
                      f"{pick['numbers']['other_answers_in_prompt']}). log p(answer org): "
                      f"{pick['numbers']['logp_answer_unedited']:.3f} -> {pick['numbers']['logp_answer_edited']:.3f}.", ""]  # fmt: skip
    # Displays never show family codes; the verification line keeps the data keys a reader filters on.
    lines = [ln if ln.startswith("For the human to verify") else plain(ln) for ln in lines]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")


# ---- batch 3: head readers, the pointer readout, code line readers ---------------------------------------------------

READER_DROP, READER_LO = 0.10, 0.05  # a reader: >= 10 points below its matched control, cluster 95% lower bound >= 5
D3B_PROBE = 0.39  # D3b's slot probe on these scenes (UNVERIFIED): the bar a head's attention readout is compared with
N_BOOT_CLUSTER = 4000  # the entity-cluster bootstrap's draws (seed BOOT_SEED), as d3b_replicate_fresh_27b's amendment
LATE_REPRO = (0.11, 0.20)  # batch 2: memory → prompt kept 11-19% with the late layers hidden from the last tokens
INTERVALS = (
    f"Headline and rule intervals: entity-cluster bootstrap (the queried entities resampled with replacement within "
    f"each domain, all their items kept; {N_BOOT_CLUSTER} draws, seed {BOOT_SEED}); reported second: the item-level "
    f"Wilson interval (accuracy) and the paired item bootstrap ({N_BOOT} draws). Every number also per domain, with "
    "n items / k entities."
)
BATCH3_RULES = {
    "reader": f"a unit (query head, key/value group, layer, whole range; a code line or union of lines) is a reader if "
    f"acc(control) - acc(unit) >= {100 * READER_DROP:.0f} points and its entity-cluster bootstrap 95% lower bound >= "
    f"{100 * READER_LO:.0f} points (control: the same unit blocked from a statement of the same kind off the answer's "
    "path, the same items)",
    "relay": f"code: a line relays if blocking it together with the last tokens costs >= {100 * READER_DROP:.0f} points "
    f"more than the last tokens alone (entity-cluster lower bound >= {100 * READER_LO:.0f} points)",
    "explained": "code: the lines explain the survivors if the union (last tokens + print + list/chain lines + the "
    "rest of the question) keeps answer org within 10 points of 'every line after the dict' (point estimate)",
    "readout": f"the best head is chosen on even-numbered scenes (pooled over the families that look the answer up) "
    f"and scored on odd-numbered ones; it reads the pointer better than the slot probe if its entity-cluster lower bound > "
    f"{D3B_PROBE:.0%}",
    "reproduction": f"heads grid: memory → prompt with all late attention heads blocked at the last tokens reproduces "
    f"batch 2 if its cluster interval overlaps {LATE_REPRO[0]:.0%}-{LATE_REPRO[1]:.0%}",
    "multiplicity": "single heads are many tests (24 heads x 4-8 layers per range): a single-head reader is read "
    "together with its key/value group and layer cells, never alone",
}
CODE_LINE_WORDS = {
    "list": "the names list line", "chain_target1": "chain line 1 (holds the key)", "chain_target2": "chain line 2",
    "chain_target3": "chain line 3", "chain_distractor1": "other chain, line 1", "chain_distractor2": "other chain, line 2",
    "chain_distractor3": "other chain, line 3", "print": "the print line", "nl": "the rest of the question",
    "final": "the last tokens", "final+print": "last tokens + print line",
    "final+selector": "last tokens + list/chain lines", "final+print+selector": "last tokens + print + list/chain",
    "final+print+selector+nl": "all of the question + list/chain", "after_dict": "every line after the dict",
    "after": "everything after the entry",
}  # fmt: skip


def entity_boot(vals: list[float], ents: list[str], doms: list[str], n_boot: int = N_BOOT_CLUSTER,
                seed: int = BOOT_SEED) -> list[float]:  # fmt: skip
    """Mean of per-item values with its entity-cluster bootstrap 95% interval (bridge_jspace.stats.cluster_bootstrap):
    within each domain the queried entities are resampled with replacement (as many as it has), every item of a drawn
    entity kept: [point, lo, hi]; NaNs when there is no item."""
    if not vals:
        return [math.nan] * 3
    return list(cluster_bootstrap(vals, ents, doms, n_boot=n_boot, seed=seed))


def _clusters(ids: list[str], cases: dict[str, dict]) -> tuple[list[str], list[str]]:
    """The queried entity and domain of each item (the cluster bootstrap's units)."""
    return [cases[i]["bridge"] for i in ids], [cases[i]["domain"] for i in ids]


def compare(a: dict[str, float], b: dict[str, float], cases: dict[str, dict]) -> dict:
    """Paired per-item values a (the cell) and b (its control) on their common items: n items / k entities / t
    wordings, both accuracies (Wilson; the cell's also by entity cluster), the drop b - a (entity cluster; item
    bootstrap second), and the same per domain."""
    names = sorted(set(a) & set(b))
    ents, doms = _clusters(names, cases)
    words = [cases[i].get("wording", "") for i in names]
    x, y = [a[i] for i in names], [b[i] for i in names]
    diff = [q - p for p, q in zip(x, y, strict=True)]
    per_domain = {}
    for d in sorted(set(doms)):
        sel = [j for j, dd in enumerate(doms) if dd == d]
        xs, ds, es = [x[j] for j in sel], [diff[j] for j in sel], [ents[j] for j in sel]
        per_domain[d] = {"n": len(sel), "k": len(set(es)), "t": len({words[j] for j in sel}),
                         "acc": wilson(int(sum(xs)), len(xs)), "acc_cluster": entity_boot(xs, es, [d] * len(sel)),
                         "acc_control": wilson(int(sum(y[j] for j in sel)), len(sel)),
                         "drop": entity_boot(ds, es, [d] * len(sel))}  # fmt: skip
    return {"n": len(names), "k": len(set(zip(doms, ents, strict=True))), "t": len(set(words)),
            "acc": wilson(int(sum(x)), len(x)),
            "acc_cluster": entity_boot(x, ents, doms), "acc_control": wilson(int(sum(y)), len(y)),
            "drop": entity_boot(diff, ents, doms), "drop_items": paired_bootstrap_diff(y, x, N_BOOT, BOOT_SEED),
            "per_domain": per_domain}  # fmt: skip


# ---- per topic, by entity cluster (the batch-2 late-read grid on pointer_v4; README reporting standard) ----------

GENERAL = {"attn_max": 0.20, "gdn_min": 0.90}  # H-general: memory → prompt, last tokens, per topic


def topic_cells(rows: list[dict], m: dict, cases: dict[str, dict]) -> dict[str, dict]:
    """Every (family, statement giving the answer, destination, layer set) cell of the standard grid in DeltaNet mode
    value, against its off-path control on the same items (compare: pooled and per topic, entity-cluster intervals).
    Keys 'family|dest|layers'."""
    ok = right_items(rows, m)
    measure = "kept" if m["eligibility"] == "none" else "correct"
    idx: dict[tuple, dict[str, float]] = collections.defaultdict(dict)
    for r in rows:
        if r["source"] in ("lookup", "lookup_off") and r["mode"] == "value" and r["id"] in ok:
            idx[(r["family"], r["source"], r["dest"], r["layers"])][r["id"]] = float(r[measure])
    return {f"{f}|{d}|{la}": compare(cell, idx[(f, "lookup_off", d, la)], cases)
            for (f, s, d, la), cell in idx.items() if s == "lookup" and (f, "lookup_off", d, la) in idx}  # fmt: skip


def general_claim(tc: dict[str, dict], fam: str = "RL") -> dict:
    """H-general per topic (fam RL: memory → prompt; DL: named → prompt, H_general_named): the statement giving the
    answer hidden from the last tokens in every attention layer keeps <= 20% and in every DeltaNet layer >= 90%.
    'holds' on the entity-cluster bounds (attention upper bound <= 20%, DeltaNet lower bound >= 90%), 'point' on the
    point estimates only, else 'fails'."""
    att, gdn = tc.get(f"{fam}|final|attn"), tc.get(f"{fam}|final|gdn")
    if not att or not gdn:
        return {}
    out: dict[str, Any] = {"topics": {}}
    for d in att["per_domain"]:
        a, g = att["per_domain"][d], gdn["per_domain"][d]
        bounds = a["acc_cluster"][2] <= GENERAL["attn_max"] and g["acc_cluster"][1] >= GENERAL["gdn_min"]
        point = a["acc"][0] <= GENERAL["attn_max"] and g["acc"][0] >= GENERAL["gdn_min"]
        out["topics"][d] = {"attn": a["acc_cluster"], "gdn": g["acc_cluster"], "n": a["n"], "k": a["k"], "t": a["t"],
                            "verdict": "holds" if bounds else "point" if point else "fails"}  # fmt: skip
    v = [x["verdict"] for x in out["topics"].values()]
    out["verdict"] = "holds" if all(x == "holds" for x in v) else "partly" if all(x != "fails" for x in v) else "fails"
    return out


def reader_cells(rows: list[dict], m: dict, cases: dict[str, dict]) -> dict[tuple[str, str], dict]:
    """Per (family, unit: a heads-grid layer label, '@cue' for the name-token narrowing; a code destination): the
    statement's cell against the same blocking of the off-path statement on the same items (compare), the reader
    flag (BATCH3_RULES, on the entity-cluster interval) and the cell's per-item values."""
    ok = right_items(rows, m)
    measure = "kept" if m["eligibility"] == "none" else "correct"
    idx: dict[tuple, dict[str, float]] = collections.defaultdict(dict)
    for r in rows:
        if r["source"] in ("lookup", "lookup_off") and r["id"] in ok:
            idx[(r["family"], r["source"], unit_key(r, m))][r["id"]] = float(r[measure])
    out = {}
    for (fam, src, k), cell in idx.items():
        ctrl = idx.get((fam, "lookup_off", k), {})
        if src != "lookup" or not set(cell) & set(ctrl):
            continue
        c = compare(cell, ctrl, cases)
        c["reader"] = c["drop"][0] >= READER_DROP and c["drop"][1] >= READER_LO
        c["per_item"] = {i: cell[i] for i in sorted(set(cell) & set(ctrl))}
        out[(fam, k)] = c
    return out


def relay_tests(rc: dict[tuple[str, str], dict], cases: dict[str, dict]) -> dict[str, dict]:
    """Code: does adding a line to the last tokens' block cost answer org (a relay), and does the union explain the
    'everything after the dict' block (within 10 points)? Differences by entity cluster (compare)."""
    out: dict[str, dict] = {}
    for fam in sorted({f for f, _ in rc}, key=fam_order):

        def paired(a_key, b_key, fam=fam):
            a, b = rc.get((fam, a_key)), rc.get((fam, b_key))
            return compare(b["per_item"], a["per_item"], cases) if a and b else None

        res: dict[str, Any] = {}
        for union in ("final+print", "final+selector", "final+print+selector", "final+print+selector+nl"):
            d = paired("final", union)
            if d:
                res[union] = {"extra_drop_vs_last_tokens": d["drop"], "per_domain": d["per_domain"],
                              "relay": d["drop"][0] >= READER_DROP and d["drop"][1] >= READER_LO}  # fmt: skip
        d = paired("final+print+selector+nl", "after_dict")
        if d:
            res["explained"] = {"union_minus_after_dict": d["drop"], "per_domain": d["per_domain"],
                                "explained": d["drop"][0] <= 0.10}  # fmt: skip
        out[fam] = res
    return out


READOUT_FIELDS = {"last": ("late", "the last token"), "cue": ("early", "the name tokens")}


def readout_tables(name: str, cases: dict[str, dict]) -> dict:
    """The pointer readout from attention.jsonl, per field (last: the last token at the late layers; cue: the name
    tokens at the early layers, named → prompt): per (family, layer, head) the share of org prompts whose attention
    puts most mass on the asked statement (argmax over the statements); the best head chosen on even-numbered scenes
    (pooled over the families that look the answer up) and scored on odd-numbered ones (Wilson; entity cluster;
    per domain)."""
    import re

    path = RESULTS / name / "attention.jsonl"
    if not path.exists():
        return {}
    recs = [json.loads(line) for line in path.read_text().splitlines()]
    out = {}
    for field in READOUT_FIELDS:
        hits: dict[tuple[str, str, int], list[int]] = collections.defaultdict(list)
        halves: dict[tuple[str, int, int], dict[str, int]] = collections.defaultdict(dict)  # (layer, head, parity)
        n_stat = 0
        for rec in recs:
            if not rec.get(field):
                continue
            parity = int(re.findall(r"\d+", rec["scene"])[-1]) % 2
            for la, heads in rec[field].items():
                for h, masses in enumerate(heads):
                    n_stat = len(masses)
                    hit = int(max(range(len(masses)), key=lambda i, ms=masses: ms[i]) == rec["query_slot"])
                    hits[(rec["family"], la, h)].append(hit)
                    if path_sources(rec["family"]):
                        halves[(la, h, parity)][rec["id"]] = hit
        if not hits:
            continue
        per = {f"{f}|{la}|{h}": wilson(sum(v), len(v)) for (f, la, h), v in hits.items()}
        even = {(la, h): statistics.mean(v.values()) for (la, h, p), v in halves.items() if p == 0 and v}
        best = max(even, key=lambda k: even[k]) if even else None
        held = halves.get((best[0], best[1], 1), {}) if best else {}
        ids = sorted(held)
        ents, doms = _clusters(ids, cases)
        vals = [float(held[i]) for i in ids]
        odd = wilson(int(sum(vals)), len(vals))
        per_domain = {d: {"n": doms.count(d), "k": len({e for e, dd in zip(ents, doms, strict=True) if dd == d}),
                          "acc": wilson(int(sum(v for v, dd in zip(vals, doms, strict=True) if dd == d)), doms.count(d))}
                      for d in sorted(set(doms))}  # fmt: skip
        cl = entity_boot(vals, ents, doms)
        out[field] = {"per_head": per, "chance": 1 / n_stat if n_stat else None, "probe_bar": D3B_PROBE,
                      "best_head": {"layer": int(best[0]), "head": best[1], "even_half": even[best], "odd_half": odd,
                                    "odd_cluster": cl, "n_odd": len(vals),
                                    "k_odd": len(set(zip(doms, ents, strict=True))), "per_domain": per_domain,
                                    "beats_probe": bool(cl[1] > D3B_PROBE)} if best else None}  # fmt: skip
    return out


def _heatmap(ax, grid, layers, n_heads, vmax, marks=None, boxed=None):
    from matplotlib.patches import Rectangle

    from bridge_jspace.plotting import MUTED

    im = ax.imshow(grid, cmap="Blues", vmin=0, vmax=vmax, aspect="auto")
    ax.set_yticks(range(len(layers)), [f"layer {la}" for la in layers], fontsize=7.5)
    ax.set_xticks(range(0, n_heads, 2), [str(h) for h in range(0, n_heads, 2)], fontsize=7)
    ax.set_xlabel("query head", fontsize=7.5, color=MUTED)
    for i, j in marks or []:
        ax.plot(j, i, "o", ms=3.5, color="#0b0b0b")
    if boxed:
        ax.add_patch(Rectangle((boxed[1] - 0.5, boxed[0] - 0.5), 1, 1, fill=False, ec="#eb6834", lw=2))
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    return im


RANGE_WORDS = {  # where each heads-grid range blocks, in words
    "late": "the last tokens before the answer, late attention layers",
    "early": "the question words, early attention layers",
    "mid": "the question words and the last tokens together, middle attention layers",
}


def range_span(r: dict) -> str:
    ls = r["layers"]
    return f"layer {ls[0]}" if len(ls) == 1 else f"layers {ls[0]}-{ls[-1]}"


def head_panels(rc: dict, m: dict, single: bool) -> list[tuple[str, str]]:
    """(range, family) panels in reading order: the families blocked head by head in the range (single=True), or
    also the memory → memory null (whole layers only)."""
    fams = sorted({f for f, _ in rc}, key=fam_order)
    out = []
    for rname, r in m["attention"]["ranges"].items():
        for f in fams:
            mine = f.split("-")[0] in r["families"]
            if (mine or (not single and not path_sources(f))) and any((f, lab) in rc for lab in [rname, *[f"L{la:02d}" for la in r["layers"]]]):  # fmt: skip
                out.append((rname, f))
    return out


def fig_heads(rc: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import FuncFormatter

    if m.get("grid") != "heads":
        return None
    att = m["attention"]
    n_heads = att["query_heads"]
    panels = head_panels(rc, m, single=True)
    if not panels:
        return None

    def grid(rname, f):
        return [[max(0.0, rc.get((f, f"L{la:02d}:h{h:02d}"), {"drop": (0,)})["drop"][0]) for h in range(n_heads)]
                for la in att["ranges"][rname]["layers"]]  # fmt: skip

    drops = {p: grid(*p) for p in panels}
    vmax = max(0.2, max(max(max(r) for r in g) for g in drops.values()))
    heights = [len(att["ranges"][r]["layers"]) + 1.4 for r, _ in panels]
    fig, axes = plt.subplots(len(panels), 1, figsize=(10, 0.42 * sum(heights) + 0.6), squeeze=False,
                             gridspec_kw={"height_ratios": heights})  # fmt: skip
    for i, (rname, f) in enumerate(panels):
        ax, layers = axes[i][0], att["ranges"][rname]["layers"]
        marks = [(li, h) for li, la in enumerate(layers) for h in range(n_heads)
                 if rc.get((f, f"L{la:02d}:h{h:02d}"), {}).get("reader")]  # fmt: skip
        im = _heatmap(ax, drops[(rname, f)], layers, n_heads, vmax, marks)
        ax.set_title(f"{fam_label(f)}: blocked at {RANGE_WORDS[rname]} ({range_span(att['ranges'][rname])})",
                     fontsize=8.5, loc="left")  # fmt: skip
        cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
        cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{100 * v:.0f}"))
        cb.ax.tick_params(labelsize=7)
    handles = [Line2D([], [], color="#0b0b0b", marker="o", ls="none", ms=4,
                      label=f"a reader: >= {100 * READER_DROP:.0f} points below its control, lower bound >= "
                            f"{100 * READER_LO:.0f} points")]  # fmt: skip
    where = {"late": "at the last tokens before the answer in the late layers",
             "early": "for named → prompt at the question words in the early layers",
             "mid": "for memory → prompt at the question words and the last tokens together in the middle layers"}  # fmt: skip
    first = next(iter(att["ranges"]))
    explain = [
        ("What we did", "Stopped ONE query head of one attention layer from reading the statement giving the answer "
                        "(its key/value partners still read it; every other head and layer untouched): "
                        + "; ".join(where[r] for r in att["ranges"]) + "."),
        ("Example", example_row({}, f"one query head at {DEST_PHRASE[att['ranges'][first]['dest']]}")),
        ("How to read", "Colour: points of answer org lost by blocking that head, relative to blocking the same head "
                        "from a statement off the answer's path (darker = the head matters more). Dots: heads that "
                        "pass the reader rule (on the entity-cluster interval)."),
        ("Control", "The same head blocked from an off-path statement of the same kind (subtracted); groups of heads, "
                    "whole layers and whole ranges are in the second figure."),
    ]  # fmt: skip
    data = (f"{RUN_INFO['model']}; {', '.join(dict.fromkeys(fam_label(f) for _, f in panels))}; "
            f"{_span(v['n'] for v in rc.values())} prompts ({_span(v['k'] for v in rc.values())} queried entities) per "
            "family; colour scale in points.")  # fmt: skip
    return _save(fig, stem, "Which attention heads read the answer's statement?", explain, data, handles, 1)


def _span(vals: Any) -> str:
    """'200' when every value is the same, else 'min-max'."""
    v = sorted(set(vals))
    return str(v[0]) if len(v) == 1 else f"{v[0]}-{v[-1]}"


def fig_head_units(rc: dict, m: dict, stem: Path) -> list[str] | None:
    """Per (range, family): key/value groups, whole layers (and, early, the name tokens only) and the whole range,
    each next to its off-path control; intervals by entity cluster (the control: Wilson)."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    if m.get("grid") != "heads":
        return None
    att = m["attention"]
    panels = head_panels(rc, m, single=False)
    if not panels:
        return None

    def units(rname: str) -> list[tuple[str, str]]:
        r, out = att["ranges"][rname], []
        narrow = r.get("narrow_dest")
        for la in r["layers"]:
            out += [(f"L{la:02d}:kv{g}", f"{la}\ng{g}") for g in range(att["kv_heads"])]
            out.append((f"L{la:02d}", f"{la}\nall"))
            if narrow:
                out.append((f"L{la:02d}@{narrow}", f"{la}\nname"))
        out.append((rname, "whole\nrange"))
        if narrow:
            out.append((f"{rname}@{narrow}", "whole\nrange,\nname"))
        return out

    widths = [len(units(r)) for r, _ in panels]
    fig, axes = plt.subplots(len(panels), 1, figsize=(max(11, 0.24 * max(widths) + 2), 2.6 * len(panels) + 0.4),
                             squeeze=False, sharey=True)  # fmt: skip
    for i, (rname, f) in enumerate(panels):
        ax = axes[i][0]
        style_axes(ax)
        us = units(rname)
        xs = [j for j, (lab, _) in enumerate(us) if (f, lab) in rc]
        if xs:
            cs = [{"acc": rc[(f, us[j][0])]["acc_cluster"]} for j in xs]
            cc = [{"acc": rc[(f, us[j][0])]["acc_control"]} for j in xs]
            _errorbar(ax, [x - 0.15 for x in xs], cs, SERIES["statement"][0], "o", ms=4.5)
            _errorbar(ax, [x + 0.15 for x in xs], cc, CONTROL_GREY, "x", ms=4.5)
        ax.set_xticks(range(len(us)), [name for _, name in us], fontsize=5.8)
        ax.set_xlim(-0.6, len(us) - 0.4)
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
        ax.set_title(f"{fam_label(f)}: blocked at {RANGE_WORDS[rname]} ({range_span(att['ranges'][rname])})",
                     fontsize=8.5, loc="left")  # fmt: skip
    handles = [Line2D([], [], color=SERIES["statement"][0], marker="o", ls="none", ms=6, label="the statement giving the answer blocked"),
               Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ls="none", ms=6, label="control: an off-path statement blocked")]  # fmt: skip
    late = att["ranges"].get("late")
    narrow = any(r.get("narrow_dest") for r in att["ranges"].values())
    la0 = next(iter(att["ranges"].values()))["layers"][0]
    first = next(iter(att["ranges"]))
    explain = [
        ("What we did", f"Blocked the statement giving the answer in one key/value group of an attention layer (its "
                        f"query heads; tick 'g2' under layer {la0} = group 2 of layer {la0}), a whole layer ('all'), "
                        "or every attention layer of the range ('whole range')."
                        + (" Early range, named → prompt: also from the name tokens of the question only ('name')."
                           if narrow else "")),
        ("Example", example_row({}, f"{DEST_PHRASE[att['ranges'][first]['dest']]} (one group, one layer or the "
                                    "whole range)")),
        ("How to read", "Each dot: % of prompts still giving answer org. "
                        + (f"Memory → prompt, whole late range ({range_span(late)}) should reproduce the earlier run "
                           f"({LATE_REPRO[0]:.0%}-{LATE_REPRO[1]:.0%}). " if late else "")
                        + ("If 'name' matches 'all', the name tokens alone carry the early read." if narrow else "")),
        ("Control", "Grey x: the same blocking of an off-path statement; it should stay near 100%. Memory → memory "
                    "(the answer comes from memory) should stay at 100% everywhere."),
    ]  # fmt: skip
    data = (f"{RUN_INFO['model']}; {_span(v['n'] for v in rc.values())} prompts ({_span(v['k'] for v in rc.values())} "
            "queried entities) per family; error bars: entity-cluster bootstrap 95% CI (control: Wilson 95% CI).")  # fmt: skip
    return _save(fig, stem, "How much of the read sits in one group of heads, one layer, or a whole range?", explain,
                 data, handles, 2)  # fmt: skip


def fig_readout(ro: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import FuncFormatter

    if not ro:
        return None
    att = m["attention"]
    n_heads = att["query_heads"]
    panels = [
        (field, f) for field in ro for f in sorted({k.split("|")[0] for k in ro[field]["per_head"]}, key=fam_order)
    ]
    heights = [len(att["ranges"][READOUT_FIELDS[fd][0]]["layers"]) + 1.4 for fd, _ in panels]
    fig, axes = plt.subplots(len(panels), 1, figsize=(10, 0.42 * sum(heights) + 0.6), squeeze=False,
                             gridspec_kw={"height_ratios": heights})  # fmt: skip
    for i, (field, f) in enumerate(panels):
        rname, words = READOUT_FIELDS[field]
        layers, best = att["ranges"][rname]["layers"], ro[field]["best_head"]
        grid = [[ro[field]["per_head"].get(f"{f}|{la}|{h}", (0,))[0] for h in range(n_heads)] for la in layers]
        boxed = (layers.index(best["layer"]), best["head"]) if best and path_sources(f) else None
        im = _heatmap(axes[i][0], grid, layers, n_heads, 1.0, boxed=boxed)
        axes[i][0].set_title(f"{fam_label(f)}: attention from {words} ({range_span(att['ranges'][rname])})",
                             fontsize=8.5, loc="left")  # fmt: skip
        cb = fig.colorbar(im, ax=axes[i][0], fraction=0.025, pad=0.01)
        cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{100 * v:.0f}%"))
        cb.ax.tick_params(labelsize=7)

    def chosen(field: str) -> str:
        b = ro[field]["best_head"] or {}
        c = b.get("odd_cluster", (math.nan,) * 3)
        return (f"{READOUT_FIELDS[field][1]}: layer {b.get('layer')}, head {b.get('head')}; other half "
                f"{100 * c[0]:.0f}% [{100 * c[1]:.0f}, {100 * c[2]:.0f}]")  # fmt: skip

    handles = [Line2D([], [], color="#eb6834", marker="s", mfc="none", ls="none", ms=8,
                      label="the head chosen on half the scenes (" + "; ".join(chosen(fd) for fd in ro) + ")")]  # fmt: skip
    chance = next(iter(ro.values()))["chance"] or 0
    explain = [
        ("What we did", "Unedited prompts: for each query head, summed the attention "
                        + " and ".join({"last": "from the last token (late attention layers)",
                                        "cue": "from the name tokens of the question (named → prompt, early attention "
                                               "layers; the name is also written in the asked statement)"}[fd]
                                       for fd in ro)
                        + " to each statement, and asked whether the asked statement gets the most."),
        ("Example", example_row({}, None)),
        ("How to read", f"Colour: % of prompts where that head looks most at the asked statement (chance "
                        f"{100 * chance:.0f}%; the slot probe of the pointer study reached {100 * D3B_PROBE:.0f}%). "
                        "Box: the best head, chosen on even-numbered scenes."),
        ("Control", "Memory → memory: its 'asked statement' is irrelevant to the answer, so a high rate there means "
                    "the head tracks the entity, not the lookup." if any(not path_sources(f) for _, f in panels) else
                    "None in this figure: the name is also written in the asked statement, so looking at it is "
                    "expected; whether that look matters is tested by blocking (the other figures)."),
    ]  # fmt: skip
    data = (f"{RUN_INFO['model']}; the chosen head is scored on odd-numbered scenes only; its interval: entity-cluster "
            "bootstrap 95% CI.")  # fmt: skip
    return _save(fig, stem, "Does any head look at the statement the answer comes from?", explain, data, handles, 1)


def fig_code_readers(rc: dict, m: dict, stem: Path) -> list[str] | None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes

    if m.get("grid") != "code_readers":
        return None
    fams = sorted({f for f, _ in rc}, key=fam_order)
    ncols = min(2, len(fams))
    nrows = -(-len(fams) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(7.2 * ncols, 3.4 * nrows), squeeze=False, sharey=True)
    for idx, f in enumerate(fams):
        ax = axes[idx // ncols][idx % ncols]
        style_axes(ax)
        dests = [d for d in CODE_DEST_ORDER if (f, d) in rc]
        xs = list(range(len(dests)))
        _errorbar(
            ax,
            [x - 0.15 for x in xs],
            [{"acc": rc[(f, d)]["acc_cluster"]} for d in dests],
            SERIES["statement"][0],
            "o",
            ms=5,
        )
        _errorbar(
            ax, [x + 0.15 for x in xs], [{"acc": rc[(f, d)]["acc_control"]} for d in dests], CONTROL_GREY, "x", ms=5
        )
        ax.set_xticks(xs, [CODE_LINE_WORDS[d].replace(" + ", "\n+ ").replace("the ", "") for d in dests], fontsize=6.3,
                      rotation=40, ha="right")  # fmt: skip
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        ax.set_title(f"{fam_label(f)}: {fam_hint(f)}", fontsize=8.5, loc="left")
        if idx % ncols == 0:
            ax.set_ylabel("% still giving answer org", fontsize=8, color=MUTED)
    for idx in range(len(fams), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    handles = [Line2D([], [], color=SERIES["statement"][0], marker="o", ls="none", ms=6, label="the answer's dict entry hidden"),
               Line2D([], [], color=CONTROL_GREY, marker="x", mew=1.6, ls="none", ms=6, label="control: another dict entry hidden")]  # fmt: skip
    explain = [
        ("What we did", f"Hid the dict entry giving the answer from one later code line (in all {RUN_INFO['n_layers']} "
                        "layers), or from several lines together, then read the answer. " + BLOCK_NOTE),
        ("Example", example_row({}, "the names list line")),
        ("How to read", "Each dot: % of programs still giving answer org. A line whose dot drops reads the entry "
                        "itself; a union that drops below the last tokens alone shows a line that passes it on."),
        ("Control", "Grey x: another dict entry hidden from the same lines; it should stay near 100%."),
    ]  # fmt: skip
    data = (f"{RUN_INFO['model']}; Python programs with a dict of lockers; {_span(v['n'] for v in rc.values())} "
            f"programs ({_span(v['k'] for v in rc.values())} queried keys) per family; error bars: entity-cluster "
            "bootstrap 95% CI (control: Wilson 95% CI).")  # fmt: skip
    return _save(fig, stem, "Which code lines read the answer's dict entry?", explain, data, handles, 2)


def _ci(t: Any, signed: bool = False) -> str:
    """'19% [12, 27]' (signed: '+12 [+5, +20]' points); '-' when missing."""
    if not t or any(math.isnan(x) for x in t[:3]):
        return "-"
    if signed:
        return f"{100 * t[0]:+.0f} [{100 * t[1]:+.0f}, {100 * t[2]:+.0f}]"
    return f"{100 * t[0]:.0f}% [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"


def _dom(c: dict, field: str = "acc") -> str:
    """Per domain: 'animals 29% (96/16), elements 8% (79/6)' (n items / k entities); drops in points."""
    return ", ".join(f"{d} {100 * v[field][0]:+.0f} pts ({v['n']}/{v['k']})" if field == "drop" else
                     f"{d} {100 * v[field][0]:.0f}% ({v['n']}/{v['k']})" for d, v in c["per_domain"].items())  # fmt: skip


def unit_phrase(unit: str, m: dict) -> str:
    """A batch-3 unit in words: what the statement is hidden from, where."""
    if m.get("grid") == "code_readers":
        return f"hidden from {CODE_LINE_WORDS.get(unit, unit)} in all {RUN_INFO['n_layers']} layers"
    label, _, dest = unit.partition("@")
    att = m["attention"]
    rng = att["ranges"][label_range(label, att)]
    return f"hidden from {DEST_PHRASE[dest or rng['dest']]} in {layers_phrase(label)}"


def _b3_row(f: str, text: str, c: dict) -> str:
    return (f"| {f} | {text} | {c['n']} / {c['k']} | {_ci(c['acc_cluster'])} | {_dom(c)} | "
            f"{100 * c['acc_control'][0]:.0f}% | {_ci(c['drop'], True)} | {_ci(c['drop_items'], True)} | "
            f"{'yes' if c['reader'] else 'no'} |")  # fmt: skip


B3_HEAD = ("| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | "
           "drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |")  # fmt: skip


def batch3_sections(m: dict, rc: dict, ro: dict, relays: dict) -> list[str]:
    """The report's batch-3 tables (plain words; n items / k entities, entity-cluster intervals, per domain): head
    readers per range and the pointer readout, or code line readers and relays."""
    out: list[str] = []
    if m.get("grid") == "heads":
        att = m["attention"]
        for rname, f in head_panels(rc, m, single=False):
            r = att["ranges"][rname]
            mine = [k for ff, k in rc if ff == f and label_range(k.partition("@")[0], att) == rname]
            heads = sorted([k for k in mine if ":h" in k], key=lambda k: -rc[(f, k)]["drop"][0])
            units = sorted([k for k in mine if ":h" not in k], key=lambda k: (k[0] != "L", k))
            out += [f"## {fam_label(f)}: blocked at {RANGE_WORDS[rname]} ({range_span(r)}: layers "
                    f"{', '.join(map(str, r['layers']))})", "", B3_HEAD, "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
            for k in heads[:8] + units:
                out.append(_b3_row(f, unit_phrase(k, m).removeprefix("hidden from "), rc[(f, k)]))
            if heads:
                n_read = sum(rc[(f, k)]["reader"] for k in heads)
                mirror = sum(
                    rc[(f, k)]["drop"][0] <= -READER_DROP and rc[(f, k)]["drop"][2] <= -READER_LO for k in heads
                )
                out += ["", f"Single heads that are readers: {n_read} of {len(heads)} (the 8 largest drops are listed); "
                        f"mirror image (the off-path block costs >= {100 * READER_DROP:.0f} points more, the noise floor): {mirror} "
                        f"of {len(heads)}."]  # fmt: skip
            out.append("")
        for field, t in ro.items():
            b = t["best_head"]
            if not b:
                continue
            out += [f"## Pointer readout: attention from {READOUT_FIELDS[field][1]}", "",
                    f"Best head chosen on even-numbered scenes (pooled over the families that look the answer up): "
                    f"layer {b['layer']}, query head {b['head']} (even half {100 * b['even_half']:.0f}%). On the "
                    f"odd-numbered scenes it puts the most attention on the asked statement in {_ci(b['odd_cluster'])} "
                    f"(entity cluster; Wilson [{100 * b['odd_half'][1]:.0f}, {100 * b['odd_half'][2]:.0f}]), n={b['n_odd']} "
                    f"/ k={b['k_odd']}; per domain {_dom(b)}; chance {100 * (t['chance'] or 0):.0f}%, the slot probe "
                    f"{100 * D3B_PROBE:.0f}%. Above the probe (entity-cluster lower bound > {100 * D3B_PROBE:.0f}%): "
                    f"{'yes' if b['beats_probe'] else 'no'}.", ""]  # fmt: skip
    if m.get("grid") == "code_readers":
        out += ["## Code line readers", "", B3_HEAD.replace("| unit |", "| hidden from |"),
                "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for f in sorted({f for f, _ in rc}, key=fam_order):
            for d in [x for x in CODE_DEST_ORDER if (f, x) in rc]:
                out.append(_b3_row(f, CODE_LINE_WORDS[d], rc[(f, d)]))
        out += ["", "| family | union | extra loss vs the last tokens alone [95%, entity cluster] | per domain | relays "
                "| union - every line after the dict [95%] | explained |", "|---|---|---|---|---|---|---|"]  # fmt: skip
        for f, res in relays.items():
            ex = res.get("explained", {})
            for u in ("final+print", "final+selector", "final+print+selector", "final+print+selector+nl"):
                if u in res:
                    last = u == "final+print+selector+nl" and ex
                    out.append(f"| {f} | {CODE_LINE_WORDS[u]} | {_ci(res[u]['extra_drop_vs_last_tokens'], True)} | "
                               f"{_dom(res[u], 'drop')} | {'yes' if res[u]['relay'] else 'no'} | "
                               + (f"{_ci(ex['union_minus_after_dict'], True)} | {'yes' if ex['explained'] else 'no'} |"
                                  if last else " | |"))  # fmt: skip
        out.append("")
    return out


def b3_headlines(m: dict, rc: dict, ro: dict, relays: dict) -> tuple[list[str], str]:
    """The batch-3 headline lines (entity-cluster interval first, Wilson second, n items / k entities, per domain)
    and the human's verification line."""
    lines: list[str] = []
    fams = sorted({f for f, _ in rc}, key=fam_order)

    def line(f: str, unit: str) -> str:
        c = rc[(f, unit)]
        return (f"Headline: {fam_label(f)}, {ANSWER_SOURCE[m.get('grid') == 'code_readers']} {unit_phrase(unit, m)}: answer org kept "
                f"{_ci(c['acc_cluster'])} (entity cluster; Wilson [{100 * c['acc'][1]:.0f}, {100 * c['acc'][2]:.0f}]); "
                f"n={c['n']} items / k={c['k']} entities; per domain {_dom(c)}   Baseline: unedited 100% "
                f"({c['n']}/{c['n']})   Control: {'another dict entry' if m.get('grid') == 'code_readers' else 'an off-path statement'}, "
                f"the same blocking {_ci(c['acc_control'])} (Wilson)")  # fmt: skip

    first: tuple[str, str] | None = None
    if m.get("grid") == "heads":
        att = m["attention"]
        for rname, r in att["ranges"].items():
            for f in fams:
                if f.split("-")[0] not in r["families"]:
                    continue
                for unit in [rname] + ([f"{rname}@{r['narrow_dest']}"] if r.get("narrow_dest") else []):
                    if (f, unit) in rc:
                        lines.append(line(f, unit))
                        first = first or (f, unit)
                heads = [k for ff, k in rc if ff == f and ":h" in k and label_range(k, att) == rname]
                if heads:
                    best = max(heads, key=lambda k: rc[(f, k)]["drop"][0])
                    c = rc[(f, best)]
                    lines.append(f"Single heads, {fam_label(f)}, {RANGE_WORDS[rname]}: "
                                 f"{sum(rc[(f, k)]['reader'] for k in heads)} of {len(heads)} are readers; the largest "
                                 f"drop: {layers_phrase(best)}, {_ci(c['drop'], True)} points (entity cluster), per "
                                 f"domain {_dom(c, 'drop')}")  # fmt: skip
        nulls = [x for x in rc if not path_sources(x[0])]
        if nulls:
            lo = min(nulls, key=lambda x: rc[x]["acc"][0])
            lines.append(f"Null: {fam_label(lo[0])}, the lowest cell over every unit: the statement {unit_phrase(lo[1], m)} "
                         f"{_ci(rc[lo]['acc_cluster'])} (n={rc[lo]['n']} / k={rc[lo]['k']})")  # fmt: skip
        for field, t in ro.items():
            b = t["best_head"]
            if b:
                lines.append(f"Pointer readout ({READOUT_FIELDS[field][1]}): layer {b['layer']}, head {b['head']} (chosen "
                             f"on even-numbered scenes) looks most at the asked statement on the odd-numbered ones in "
                             f"{_ci(b['odd_cluster'])} (entity cluster; Wilson [{100 * b['odd_half'][1]:.0f}, "
                             f"{100 * b['odd_half'][2]:.0f}]); n={b['n_odd']} / k={b['k_odd']}; per domain {_dom(b)}; "
                             f"chance {100 * (t['chance'] or 0):.0f}%, the slot probe {100 * D3B_PROBE:.0f}%")  # fmt: skip
    else:
        for f in fams:
            for unit in ("final", "final+print+selector+nl", "after_dict"):
                if (f, unit) in rc:
                    lines.append(line(f, unit))
                    first = first or (f, unit)
            readers = [CODE_LINE_WORDS[d] for d in CODE_DEST_ORDER if rc.get((f, d), {}).get("reader") and "+" not in d
                       and d not in ("final", "after", "after_dict")]  # fmt: skip
            res = relays.get(f, {})
            rel = [CODE_LINE_WORDS[u] for u in res if u != "explained" and res[u]["relay"]]
            ex = res.get("explained")
            lines.append(f"Readers, {fam_label(f)}: {', '.join(readers) or 'no single line'}; relays (with the last "
                         f"tokens): {', '.join(rel) or 'none'}; the lines explain the survivors: "
                         f"{('yes' if ex['explained'] else 'no') + ' (' + _ci(ex['union_minus_after_dict'], True) + ' points)' if ex else '-'}")  # fmt: skip
    verify = "the cells in summary.json."
    if first:
        f, unit = first
        c = rc[first]
        label, _, dest = unit.partition("@")
        if m.get("grid") == "heads":
            dest = dest or m["attention"]["ranges"][label_range(label, m["attention"])]["dest"]
        else:
            dest, label = unit, "all"
        verify = (f"family={f}, source=lookup, dest={dest}, layers={label}, mode=value (expect "
                  f"{round(c['acc'][0] * c['n'])}/{c['n']}; the cluster interval: entity = cases.jsonl 'bridge', "
                  "resampled within 'domain').")  # fmt: skip
    return lines, verify


def b3_prior_rows(hyps: dict, m: dict, rc: dict, ro: dict, relays: dict) -> list[str]:
    """The job spec's batch-3 hypotheses, each checked against this run (holds / partly / fails)."""

    def pc(c: dict) -> str:
        return _ci(c["acc_cluster"])

    def heads_of(f: str, rname: str) -> list[str]:
        att = m["attention"]
        return [k for ff, k in rc if ff == f and ":h" in k and label_range(k, att) == rname]

    def reproduce():
        c = rc[("RL", "late")]
        ok = c["acc_cluster"][1] <= LATE_REPRO[1] and c["acc_cluster"][2] >= LATE_REPRO[0]
        return f"memory → prompt, whole late range: {pc(c)}", "holds" if ok else "fails"

    def late_few():
        hs = heads_of("RL", "late")
        n_read = sum(rc[("RL", k)]["reader"] for k in hs)
        layers = [k for f, k in rc if f == "RL" and k.startswith("L") and ":" not in k and "@" not in k
                  and label_range(k, m["attention"]) == "late" and rc[(f, k)]["reader"]]  # fmt: skip
        return (f"memory → prompt: {n_read} of {len(hs)} single late heads are readers; late layers that are: "
                f"{', '.join(layers_phrase(x) for x in layers) or 'none'}",
                "holds" if n_read == 0 and layers else "partly" if n_read <= 2 else "fails")  # fmt: skip

    def named_early():
        c = rc[("DL", "early")]
        n_read = sum(rc[("DL", k)]["reader"] for k in heads_of("DL", "early"))
        return (f"named → prompt, question words, whole early range: {pc(c)}; {n_read} single early heads are readers",
                "holds" if c["acc"][0] <= 0.10 and n_read >= 1 else "partly" if c["acc"][0] <= 0.10 else "fails")  # fmt: skip

    def name_tokens():
        a, b = rc[("DL", "early")], rc[("DL", "early@cue")]
        return (f"whole early range, question words {pc(a)}, name tokens only {pc(b)}",
                "holds" if abs(a["acc"][0] - b["acc"][0]) <= 0.10 else "fails")  # fmt: skip

    def mid_joint():
        c = rc[("RL", "mid")]
        n_read = sum(rc[("RL", k)]["reader"] for k in heads_of("RL", "mid"))
        return (f"memory → prompt, both destinations, whole middle range: {pc(c)}; {n_read} single middle heads are readers",
                "holds" if 0.30 <= c["acc"][0] <= 0.60 and n_read == 0 else "partly" if 0.30 <= c["acc"][0] <= 0.60 else "fails")  # fmt: skip

    def readout():
        b = ro["last"]["best_head"]
        return (f"layer {b['layer']} head {b['head']}: {_ci(b['odd_cluster'])} on held-out scenes",
                "holds" if b["beats_probe"] else "fails")  # fmt: skip

    def null():
        lows = [rc[x]["acc"][0] for x in rc if not path_sources(x[0])]
        return f"memory → memory, lowest cell {100 * min(lows):.0f}%", "holds" if min(lows) >= 0.95 else "fails"

    def code_reader(dest: str, want: bool, fams: tuple[str, ...]):
        got = {f: rc[(f, dest)]["reader"] for f in fams if (f, dest) in rc}
        txt = "; ".join(
            f"{f}: {_ci(rc[(f, dest)]['drop'], True)} points ({'reader' if v else 'not a reader'})"
            for f, v in got.items()
        )
        hits = sum(v == want for v in got.values())
        return txt, "holds" if got and hits == len(got) else "partly" if hits else "fails"

    def relay():
        res = relays.get("IX", {})
        got = {u: res[u]["relay"] for u in ("final+print", "final+selector") if u in res}
        return (", ".join(f"{CODE_LINE_WORDS[u]}: {_ci(res[u]['extra_drop_vs_last_tokens'], True)}" for u in got),
                "holds" if any(got.values()) else "fails")  # fmt: skip

    def explained():
        got = {f: r["explained"]["explained"] for f, r in relays.items() if "explained" in r}
        return (", ".join(f"{f}: {_ci(relays[f]['explained']['union_minus_after_dict'], True)}" for f in got),
                "holds" if got and all(got.values()) else "partly" if any(got.values()) else "fails")  # fmt: skip

    checks = {"H_reproduce": reproduce, "H_late_few_heads": late_few, "H_named_early": named_early,
              "H_name_tokens": name_tokens, "H_mid_joint": mid_joint, "H_readout": readout, "H_null": null,
              "H_print_reader": lambda: code_reader("print", True, ("DK",)),
              "H_list_not_reader": lambda: code_reader("list", False, ("IX",)),
              "H_relay": relay, "H_explained": explained}  # fmt: skip
    out = []
    for h, pred in hyps.items():
        try:
            res, verdict = checks[h]() if h in checks else ("see summary.json", "-")
        except (KeyError, TypeError, ValueError, IndexError):
            res, verdict = "not measured in this run", "-"
        short = pred if len(pred) <= 220 else pred[:217] + "..."
        out.append(f"| {h} | {short} | {res} | {verdict} |")
    return out


def write_report_b3(name: str, m: dict, rows: list[dict], cases: dict[str, dict], rc: dict, ro: dict, relays: dict,
                    figs: dict, out_dir: Path) -> None:  # fmt: skip
    """report.md for the batch-3 grids (heads, code_readers), in the AGENTS.md report format."""
    led, spec = _ledger(name), _spec(name)
    commit = (led.get("commit") or "unknown")[:7]
    seeds = sorted(set(m["seeds"].values()))
    ok = right_items(rows, m)
    measure = "kept" if m["eligibility"] == "none" else "correct"
    n_items = collections.Counter(r["family"] for r in rows if r["source"] == "none")
    k_ent = {f: max((c["k"] for (ff, _), c in rc.items() if ff == f), default=0) for f in n_items}
    heads, verify = b3_headlines(m, rc, ro, relays)
    ps = sorted(math.exp(r["logp"]) for r in rows if r["source"] == "none")
    check = json.loads((RESULTS / name / "check.json").read_text())
    ctrl = [r for r in rows if r["source"] == "lookup_off" and r["id"] in ok]
    worst = min(rc.items(), key=lambda kv: kv[1]["acc_control"][0]) if rc else None
    singles = [(f, k) for f, k in rc if ":h" in k]
    mirror = sum(rc[x]["drop"][0] <= -READER_DROP and rc[x]["drop"][2] <= -READER_LO for x in singles)
    # cluster / item interval width, over cells not at 0% or 100% (there the cluster interval collapses to a point)
    ratios = [(c["acc_cluster"][2] - c["acc_cluster"][1]) / (c["acc"][2] - c["acc"][1]) for c in rc.values()
              if 0.02 < c["acc"][0] < 0.98 and not math.isnan(c["acc_cluster"][1])]  # fmt: skip
    ratio = (f"{statistics.median(ratios):.1f}x the item-level ones (median over the {len(ratios)} cells between 2% "
             "and 98%)" if ratios else "not comparable here (every cell is at 0% or 100%)")  # fmt: skip
    lines = [f"# {EXP} / {name}: analysis", "",
             f"EXP {name} @ {commit} | model {RUN_INFO['model']} | n={dict(n_items)} org prompts per family, "
             f"k={k_ent} queried entities, domains {sorted({c['domain'] for c in cases.values()})} | seeds={seeds}", "",
             f"Claim tested: {spec.get('question', m['why'])}", "",
             "Terms: org prompt = the unedited prompt; answer org = its answer; 'hidden from' = those positions cannot "
             "read it directly ("
             + ("the attention scores of the named query heads masked; attention layers only, DeltaNet layers untouched"
                if m.get("grid") == "heads" else "attention scores masked and DeltaNet values removed, every layer")
             + "); accuracy = % of org prompts still giving answer org (100% unedited, by selection). " + INTERVALS, "",
             *heads, "",
             "Figures: " + ", ".join(f for fs in figs.values() if fs for f in fs), "",
             "Three dumbest ways this could be wrong:",
             f"1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min {ps[0]:.2f}, median "
             f"{ps[len(ps) // 2]:.3f}; an unedited row moves by up to "
             f"{check['unedited_row_drift_in_knocked_batch_max_abs']:.2f} logits when other rows in its batch are "
             "knocked (check.json), so every knocked row is scored against the unedited row of its own batch.",
             f"2) Hiding any statement there breaks the model. Checked: "
             f"{'another dict entry' if m.get('grid') == 'code_readers' else 'the off-path statement'}, blocked the same way, "
             f"loses answer org in {sum(not r[measure] for r in ctrl)} of {len(ctrl)} rows; the worst control cell: "
             + (f"{plain(worst[0][0])}, {unit_phrase(worst[0][1], m)} keeps {100 * worst[1]['acc_control'][0]:.0f}%."
                if worst else "-"),
             (f"3) With {len(singles)} single heads tested, some readers are noise. Checked: the mirror image of the "
              f"rule (the off-path block costing >= {100 * READER_DROP:.0f} points more than the statement) fires for {mirror} of "
              f"{len(singles)} single heads; single heads are read with their group and layer. Items of one entity are "
              f"correlated (few entities per domain): the entity-cluster intervals are {ratio}." if singles else
              "3) Items of one entity are correlated (few queried keys per domain): every interval is the entity-cluster "
              f"bootstrap; the item-level intervals are next to them (cluster intervals are {ratio}). "
              "The lines are not independent: unions are read against 'every line after the dict', not summed."),
             "",
             "For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count "
             f"correct=true with {verify}",
             "",
             "Status: UNVERIFIED",
             "",
             "## Pre-registered rules (manifest.json 'batch3_rules', 'intervals'; job spec decision_rule)",
             "",
             *[f"- {k}: {v}" for k, v in (m.get("batch3_rules") or BATCH3_RULES).items()],
             "",
             *batch3_sections(m, rc, ro, relays),
             "## The agent's priors (job spec hypotheses), checked",
             "",
             "| hypothesis | prediction (job spec) | result | verdict |",
             "|---|---|---|---|",
             *b3_prior_rows(spec.get("hypotheses") or {}, m, rc, ro, relays),
             ""]  # fmt: skip
    ex_path = RESULTS / name / "examples.json"
    if ex_path.exists():
        ex = json.loads(ex_path.read_text())["examples"]
        pick = next(
            (e for g in ("one_head_breaks", "one_line_breaks", "path_breaks") for e in ex if e["group"] == g), None
        )
        if pick:
            lines += [f"## Worked example (examples.json, group {pick['group']})", "", "```", pick["prompt"], "```", "",
                      f"{pick['family']}, org prompt {pick['item_id']}. What was done: {pick['condition'].split('; DeltaNet')[0]}. "
                      f"Unedited the model answers {pick['answers']['clean']!r} (answer org "
                      f"{pick['numbers']['answer']!r}); blocked it answers {pick['answers']['edited']!r} (the prompt's "
                      f"other answers: {pick['numbers']['other_answers_in_prompt']}). log p(answer org): "
                      f"{pick['numbers']['logp_answer_unedited']:.3f} -> {pick['numbers']['logp_answer_edited']:.3f}.", ""]  # fmt: skip
    lines = [ln if ln.startswith("For the human to verify") else plain(ln) for ln in lines]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")


def stage_figures(name: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    m, rows, cases = load_run(name)
    import shutil

    EXAMPLE_CASE.clear()
    if DATASET in POINTER_SETS:  # the captions' Example row: the first case of a family that looks the answer up
        looks = [c for c in cases.values() if path_sources(c["family"]) and "lookup" in c["sources"]]
        # the other-language figure shows a statement in another language; otherwise the first lookup family's case
        # the code-line figure's example blocks the names line (a list-position program); the heads grid's is a case
        # of the first range's first family (early: named → prompt)
        want = "IX" if m.get("grid") == "code_readers" else None
        if m.get("grid") == "heads":
            want = next(iter(m["attention"]["ranges"].values()))["families"][0]
        pick = (
            next((c for c in looks if c["family"].endswith("xlang")), None)
            or (next((c for c in looks if c["family"] == want), None) if want else None)
            or (min(looks, key=lambda c: fam_order(c["family"])) if looks else None)
        )
        EXAMPLE_CASE.update(pick or {})

    final_dir = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}-figures"
    out_dir = final_dir.with_name(final_dir.name + ".partial")  # renamed when complete: a crash leaves no final folder
    # One figures folder per run (user's rule): drop this stage's earlier output; the job-written analysis-*Z stay.
    for old in (RESULTS / name).glob("analysis-*-figures*"):
        if old.is_dir():
            shutil.rmtree(old)
    out_dir.mkdir(parents=True, exist_ok=False)
    cells = summarise_cells(m, rows)
    cl = claims(cells)
    grid = m.get("grid", "standard")
    rc: dict = {}
    ro: dict = {}
    relays: dict = {}
    if grid in ("heads", "code_readers"):
        rc = reader_cells(rows, m, cases)
        ro = readout_tables(name, cases) if grid == "heads" else {}
        relays = relay_tests(rc, cases) if grid == "code_readers" else {}
        if grid == "heads":
            figs = {"heads": fig_heads(rc, m, out_dir / "heads"), "head_units": fig_head_units(rc, m, out_dir / "head_units"),
                    "readout": fig_readout(ro, m, out_dir / "readout")}  # fmt: skip
        else:
            figs = {"code_readers": fig_code_readers(rc, m, out_dir / "code_readers")}
        cl = {"readers": {f"{f}|{k}": {kk: v for kk, v in c.items() if kk != "per_item"} for (f, k), c in rc.items()},
              "readout": ro, "relays": relays, "rules": m.get("batch3_rules"), "intervals": m.get("intervals")}  # fmt: skip
    else:
        figs = {
            "all_layers": fig_all_layers(cells, m, out_dir / "all_layers"),
            "windows": fig_windows(cells, m, out_dir / "windows"),
            "bands": fig_bands(cells, m, out_dir / "bands"),
            "cuts": fig_cuts(cells, m, out_dir / "cuts"),
            "norm_ratio": fig_norm(rows, m, out_dir / "norm_ratio"),
        }
        if DATASET in POINTER_SETS:  # per topic, by entity cluster (README reporting standard)
            tc = topic_cells(rows, m, cases)
            cl["topics"], cl["general"], cl["general_named"] = tc, general_claim(tc), general_claim(tc, "DL")
            figs["topics"] = fig_topics(tc, m, out_dir / "topics")
    summary = {"run": name, "rule": m["decision"], "claims": cl, "figures": figs,
               "cells": [{"family": k[0], "source": k[1], "dest": k[2], "layers": k[3], "mode": k[4], **c}
                         for k, c in cells.items()]}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if grid in ("heads", "code_readers"):
        write_report_b3(name, m, rows, cases, rc, ro, relays, figs, out_dir)
    else:
        write_report(name, m, rows, cells, cl, figs, out_dir)
    out_dir.rename(final_dir)
    print("wrote", final_dir, {k: v for k, v in figs.items() if v})


# ---- examples (job pages) -------------------------------------------------------------------------------------------

HYPOTHESES = {
    "H_answer_site": "the final positions read the path's lookup statement directly; the question tokens read the "
    "binding statement",
    "H_relay": "the question tokens read both path statements and relay them to the final positions",
}


def predicted_break(h: str, fam: str, source: str, dest: str) -> bool:
    if source not in path_sources(fam):
        return False
    if dest == "after":
        return True
    reads = {"H_answer_site": {"lookup": ("final", "both"), "binding": ("question", "both")},
             "H_relay": {"lookup": ("question", "both"), "binding": ("question", "both")}}[h]  # fmt: skip
    return dest in reads[source]


def merged_spans(offsets: list, positions: list[int], role: str) -> list[dict]:
    out: list[dict] = []
    for p in sorted(positions):
        s, e = offsets[p]
        if out and out[-1]["end"] >= s - 1 and out[-1]["role"] == role:
            out[-1]["end"] = e
        else:
            out.append({"start": s, "end": e, "role": role})
    return out


def stage_examples(name: str, k: int) -> None:
    m, rows, cases = load_run(name)
    path = RESULTS / name / "examples.json"
    assert not path.exists(), f"{path} exists; examples are written once"
    ok = right_items(rows, m)
    measure = "kept" if m["eligibility"] == "none" else "correct"
    none = {r["id"]: r for r in rows if r["source"] == "none"}
    knocked = [r for r in rows if r["source"] != "none" and r["id"] in ok]
    on_path = [r for r in knocked if r["source"] in path_sources(r["family"])]
    note = " (smoke: 'right' = the unedited top token)" if m["eligibility"] == "none" else ""
    broad = ("all", *HEAD_RANGES)  # the headline layer sets (heads grid: every attention layer of a range)
    groups = {
        "path_breaks": ("A path statement blocked, the answer lost", "source on the family's path, all layers (heads "
                        f"grid: every attention layer of a range), unedited read right, edited read wrong{note}",
                        [r for r in on_path if r["layers"] in broad and not r[measure]]),
        "path_confusion": ("Lost to another statement's answer", "as path_breaks, and the edited top token is another "
                           "entity's answer in the same prompt (another locker, legs, capital)",
                           [r for r in on_path if not r[measure] and r["conf"]]),
        "path_survives": ("A path statement blocked from the answer site, the answer kept", "source on the path, "
                          "destination final or both, all layers, edited read still right",
                          [r for r in on_path if r["layers"] in broad and r["dest"] in ("final", "both") and r[measure]]),
        **({"one_head_breaks": ("One query head blocked, the answer lost", "heads grid: a single query head blocked "
                                "from the statement giving the answer (at its range's destination), edited read wrong",
                                [r for r in on_path if ":h" in r["layers"] and not r[measure]])}
           if m.get("grid") == "heads" else {}),
        **({"one_line_breaks": ("One code line blocked, the answer lost", "code grid: the entry hidden from one line "
                                "(not the last tokens), edited read wrong",
                                [r for r in on_path if r["dest"] in CODE_LINE_WORDS and "+" not in r["dest"]
                                 and r["dest"] not in ("final", "after", "after_dict") and not r[measure]])}
           if m.get("grid") == "code_readers" else {}),
        "control_breaks": ("A control span blocked, the answer lost (collateral damage)", "source lookup_off, "
                           "binding_off, random or trailing, any layers, edited read wrong",
                           [r for r in knocked if r["source"] in ("lookup_off", "binding_off", "random", "trailing") and not r[measure]]),
        "positive_control": ("Path statement invisible to everything after it", "source on the path, destination "
                             "after, all layers, DeltaNet mode absent (no write, erase or decay at S): any outcome",
                             [r for r in on_path if r["dest"] == "after" and r["mode"] == "absent"]),
    }  # fmt: skip
    rng = random.Random(EXAMPLE_SEED)
    examples = []
    for key, (_, _, pool) in groups.items():
        for r in rng.sample(pool, min(k, len(pool))):
            c = cases[r["id"]]
            src = c["sources"][r["source"]]
            dst = list(range(max(src) + 1, len(c["ids"]))) if r["dest"] == "after" else c["dests"][r["dest"]]
            spans = merged_spans(c["offsets"], src, "source") + merged_spans(c["offsets"], dst, "destination")
            prompt = c["prompt"]
            cue_at = prompt.rfind(c["cue"])  # in the question
            if cue_at >= 0:
                spans.append({"start": cue_at, "end": cue_at + len(c["cue"]), "role": "cue"})
            at = 0
            while (at := prompt.find(" " + c["bridge"], at)) >= 0:
                spans.append({"start": at + 1, "end": at + 1 + len(c["bridge"]), "role": "bridge"})
                at += 1
            dest_words = {"question": "the question tokens", "final": "the final template positions",
                          "both": "the question and final positions", "after": "every position after it",
                          "cue": "the name tokens in the question"}.get(
                r["dest"], CODE_LINE_WORDS.get(r["dest"], r["dest"]))  # fmt: skip
            base = none[r["id"]]
            expected = {}
            if r["layers"] == "all" and m.get("grid", "standard") == "standard":
                for h in HYPOTHESES:
                    expected[h] = f"not {c['answer']}" if predicted_break(h, r["family"], r["source"], r["dest"]) else c["answer"]  # fmt: skip
            examples.append({
                "group": key, "family": r["family"], "item_id": r["id"], "prompt": prompt, "spans": spans,
                "condition": f"{dest_words} cannot read the {r['source']} span ({c['source_text'][r['source']]!r}) "
                f"directly at {layers_phrase(r['layers'], RUN_INFO['n_layers'])}; DeltaNet mode {r['mode']} (value: "
                "the span's values zeroed, its keys/betas/decays kept; absent: the span removed from the recurrence)",
                "answers": {"clean": TOKENS[r["batch_none_top"]] if TOKENS else str(base["top"]),
                            "edited": TOKENS[r["top"]] if TOKENS else str(r["top"]), "expected": expected},
                "numbers": {"logp_answer_unedited": base["logp"], "logp_answer_edited": r["logp"],
                            "dlogp": r["dlogp"], "correct": r["correct"], "kept": r["kept"], "confusion": r["conf"],
                            "deltanet_norm_ratio_at_D": r.get("norm_ratio"),
                            "answer": c["answer"], "other_answers_in_prompt": c["conf_answers"]},
                "why": groups[key][1],
            })  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": EXAMPLE_SEED, "k": k,
            "groups": [{"key": key, "title": t, "definition": d, "n_total": len(p)} for key, (t, d, p) in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, {g["key"]: g["n_total"] for g in blob["groups"]})


TOKENS: list[str] = []


def load_token_strings() -> None:
    tok = S.tokenizer()
    TOKENS.extend(tok.batch_decode([[i] for i in range(len(tok))]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "analyze", "examples", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--dataset", choices=["suite", *POINTER_SETS], default="suite",
                    help="suite: the animal suite and countries; or a pointer-style item set (batch 2)")  # fmt: skip
    ap.add_argument("--families", nargs="+", default=None,
                    help="suite: BL BR RL RR BLR BRL country-R country-B (default all); pointer sets: the files' "
                    "family codes (pointer_v1 / alias: RL DL RR; code: DK IX CH2 CH3 RK RR)")  # fmt: skip
    ap.add_argument("--domains", nargs="+", default=None, help="pointer sets: the domains to use (default all)")
    ap.add_argument("--competence", default=None, help="pointer sets: the competence run (default the dataset's)")
    ap.add_argument("--n", type=int, default=100, help="items per family")
    ap.add_argument("--sources", nargs="+", choices=list(SOURCES), default=list(SOURCES))
    ap.add_argument("--dests", nargs="+", choices=list(DESTS), default=list(DESTS))
    ap.add_argument(
        "--layers",
        nargs="+",
        choices=["all", "win8", "win8k", "win4", "pre", "suf", "kind", "bands", "band4"],
        default=["all"],
    )
    ap.add_argument("--sweep", choices=["path", "path+random", "all"], default="path")
    ap.add_argument("--sweep-dests", nargs="+", choices=["question", "final", "both"], default=["question", "final", "both"])  # fmt: skip
    ap.add_argument("--absent", action="store_true", help="add the DeltaNet mode-absent rows (both, after; all layers)")
    ap.add_argument("--head-ranges", nargs="+", choices=list(HEAD_RANGES), default=list(HEAD_RANGES),
                    help="heads grid: the ranges of depth to block head by head (HEAD_RANGES)")  # fmt: skip
    ap.add_argument("--grid", choices=["standard", "heads", "code_readers"], default="standard",
                    help="heads: one attention head at a time per range of depth (batch 3a; --head-ranges); "
                    "code_readers: one code line at a time (batch 3b; code_pointer_v1)")  # fmt: skip
    ap.add_argument("--no-eligibility", dest="eligibility", action="store_const", const="none", default="map",
                    help="smokes: the first n items per family, all counted (scored by 'kept')")  # fmt: skip
    ap.add_argument("--k", type=int, default=3, help="examples per group")
    args = ap.parse_args()
    if args.stage == "manifest":
        assert args.why, "manifest needs --why"
        if args.dataset == "suite":
            args.families = args.families or list(FAMILIES)
            assert set(args.families) <= set(FAMILIES), f"suite families are {FAMILIES}"
        else:
            assert args.families, "pointer sets need --families"
            args.competence = args.competence or POINTER_COMPETENCE[args.dataset]
        stage_manifest(args)
    elif args.stage == "run":
        stage_run(args.name)
    elif args.stage in ("summarise", "analyze"):  # analyze: the decision rule re-applied to the saved rows
        stage_summarise(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        load_token_strings()
        stage_examples(args.name, args.k)
