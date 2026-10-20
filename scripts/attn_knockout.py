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
"""

from __future__ import annotations

import argparse
import collections
import json
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
from bridge_jspace.stats import bootstrap_mean, paired_bootstrap_diff, wilson
from bridge_jspace.tokens import raw_encoding
from bridge_jspace.utils import progress
from scripts import exp09_bind_recall as E
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl

EXP = "attn_knockout"
RESULTS = pins.RESULTS_DIR / EXP
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
    length = len(sources.get("lookup", sources["binding"]))
    forbidden = set(sources["binding"]) | set(sources.get("lookup", []))
    named = [v for v in sources.values()]  # a random span is never exactly one of the named statements
    starts = [
        p
        for p in range(ctx_tok[0], ctx_tok[-1] - length + 2)
        if not forbidden & set(range(p, p + length)) and list(range(p, p + length)) not in named
    ]
    p = rng.choice(starts)
    sources["random"], texts["random"] = list(range(p, p + length)), tok.decode(ids[p : p + length])
    content_end = text.index("<|im_end|>", q_start)
    question = token_span(offsets, q_start, content_end)
    anchor = max(sources.get("lookup", sources["binding"]))
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
        else:
            raise ValueError(w)
    return sets


def conditions(case: dict, m: dict) -> list[dict]:
    fam = case["family"]
    srcs = [s for s in m["sources"] if s in case["sources"]]
    out = [{"source": s, "dest": d, "layers": "all", "mode": "value"} for s in srcs for d in m["dests"]]
    if m["absent"]:
        out += [{"source": s, "dest": d, "layers": "all", "mode": "absent"} for s in srcs for d in ("both", "after")]
    sweep = srcs if m["sweep"] == "all" else [s for s in srcs if s in SWEEP[fam]]
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


def model_kinds() -> list[str]:
    from huggingface_hub import hf_hub_download

    cfg = json.loads(Path(hf_hub_download(pins.MODEL_REPO, "config.json", revision=pins.MODEL_REVISION)).read_text())
    return list(cfg.get("text_config", cfg)["layer_types"])


def stage_manifest(args) -> None:
    pins.check_run_name(args.name)
    path = RESULTS / args.name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    kinds = model_kinds()
    sets = layer_sets(kinds, args.layers)
    for label, ls in sets.items():
        if label.startswith("win") and ":" not in label:
            assert sum(kinds[i] == FULL for i in ls) == 2, f"{label}: not 2 full-attention layers"
    inputs = [S.data_dir("A") / f"{f}.json" for f in args.families if f in SUITE]
    if any(f in COUNTRIES for f in args.families):
        inputs.append(pins.BIND_RECALL_FILE)
    if args.eligibility == "map":
        inputs += (
            [pins.RESULTS_DIR / "suite_split" / SUITE_MAP / "cases.jsonl"]
            if any(f in SUITE for f in args.families)
            else []
        )
        inputs += [pins.RESULTS_DIR / "control_split" / COUNTRY_MAP / "cases.jsonl"] if any(f in COUNTRIES for f in args.families) else []  # fmt: skip
    m = {
        "exp": EXP, "run": args.name, "why": args.why,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "families": args.families, "n_per_family": args.n, "eligibility": args.eligibility,
        "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
        "sources": args.sources, "dests": args.dests, "sweep": args.sweep, "sweep_dests": args.sweep_dests,
        "absent": args.absent, "layer_sets": sets, "layer_kinds": kinds,
        "seeds": {"spans": SPAN_SEED, "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
        "knockout": (sys.modules["bridge_jspace.knockout"].__doc__ or "").split("\n\n")[1],
        "decision": {"needed": f"accuracy drop >= {NEEDED_DROP:.0%} and paired bootstrap 95% lower bound of "
                     f"acc(control) - acc(cell) >= {CONTROL_MARGIN:.0%}", "not_needed": f"Wilson 95% lower bound of "
                     f"accuracy >= {NOT_NEEDED_LO:.0%}", "doc": next(p for p in (__doc__ or "").split("\n\n") if p.startswith("Decision rule"))},
        "batch": BATCH,
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def forward_last(model, ids: torch.Tensor) -> torch.Tensor:
    return model.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[:, -1].float()


@torch.no_grad()
def run_check(model, case: dict, kinds: list[str]) -> dict:
    """The gate before the run, on the first case: no-op exactness, batch drift of the unedited row, the positive
    control (context-independence), the DeltaNet kernel path against the torch reference, and timing."""
    ids = torch.tensor([case["ids"]], device="cuda")
    n_layers, length = len(kinds), ids.shape[1]
    every = range(n_layers)
    plain = forward_last(model, ids)
    out: dict[str, Any] = {"kernel_path": kernel_path()}
    with knock_out(model, every, [[]], [case["dests"]["final"]]):
        out["noop_empty_source_max_abs"] = float((forward_last(model, ids) - plain).abs().max())
    src = case["sources"].get("lookup", case["sources"]["binding"])
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
    rows = torch.tensor([case["ids"]] * BATCH, device="cuda")
    for label, ctx in (
        ("plain", None),
        ("all_layers_knocked", (every, [src] * BATCH, [case["dests"]["both"]] * BATCH)),
    ):
        times = []
        for _ in range(3):
            torch.cuda.synchronize()
            t = time.time()
            if ctx is None:
                forward_last(model, rows)
            else:
                with knock_out(model, *ctx):
                    forward_last(model, rows)
            torch.cuda.synchronize()
            times.append(time.time() - t)
        out[f"seconds_batch{BATCH}_{label}"] = round(min(times[1:]), 4)
    out["passed"] = bool(out["noop_empty_source_max_abs"] == 0.0 and out["posctl_last_reads_nothing_same_top"]
                         and out["posctl_last_reads_nothing_max_abs"] < 0.1 and out["posctl_context_erased_absent_max_abs"] < 0.1)  # fmt: skip
    return out


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "rows.jsonl").exists(), f"{out_dir} has results; runs are written once"
    for rel, sha in m["inputs"].items():
        assert sha256_of(pins.REPO_ROOT / rel) == sha, f"{rel} changed since the manifest"
    model = load_model()
    kinds = layer_kinds(model)
    assert kinds == m["layer_kinds"], "the loaded model's layer kinds differ from the manifest's"
    tok = model.tokenizer
    t0 = time.time()
    cases = build_cases(tok, m["families"], m["n_per_family"], m["eligibility"])
    print(json.dumps(collections.Counter(c["family"] for c in cases)), flush=True)
    check = run_check(model, cases[0], kinds)
    check["seconds"] = round(time.time() - t0, 1)
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps(check, indent=1), flush=True)
    assert check["passed"], "the pre-run check failed (check.json); not running"
    sets = m["layer_sets"]
    rows: list[dict] = []
    total = sum(len(conditions(c, m)) for c in cases)
    print(f"{len(cases)} cases, {total} knocked rows", flush=True)
    t_run = time.time()
    for c in progress(cases, desc="items"):
        conds = conditions(c, m)
        ids = torch.tensor([c["ids"]], device="cuda")
        base_top = None
        for mode in ("value", "absent"):
            mine = [x for x in conds if x["mode"] == mode]
            for start in range(0, len(mine), BATCH - 1):
                chunk = [None, *mine[start : start + BATCH - 1]]  # row 0: the unedited row of this batch
                src = [positions(c, x)[0] if x else [] for x in chunk]
                dst = [positions(c, x)[1] if x else [] for x in chunk]
                layers = [sets[x["layers"]] if x else [] for x in chunk]
                norm_log: list[dict] = []
                with knock_out(model, layers, src, dst, mode=mode, norm_log=norm_log):
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
    keep = ("id", "family", "scene", "bridge", "cue", "answer", "answer_kind", "conf_answers", "tok_A", "conf_toks",
            "prompt", "ids", "offsets", "sources", "source_text", "source_flags", "dests", "context")  # fmt: skip
    write_jsonl(out_dir / "cases.jsonl", [{k: c[k] for k in keep} for c in cases])
    timing = {"cases": len(cases), "knocked_rows": total, "forwards_rows_incl_unedited": total + sum(
        -(-len([x for x in conditions(c, m) if x["mode"] == g]) // (BATCH - 1)) for c in cases for g in ("value", "absent")),
        "seconds_run": round(seconds, 1), "rows_per_second": round(total / seconds, 2),
        "seconds_total": round(time.time() - t0, 1), "mean_prompt_tokens": statistics.mean(len(c["ids"]) for c in cases)}  # fmt: skip
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)


# ---- summary --------------------------------------------------------------------------------------------------------


def load_run(name: str) -> tuple[dict, list[dict], dict[str, dict]]:
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
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
    for fam, srcs in PATH.items():
        got = {s: v(fam, s, "after", mode="absent") for s in srcs}
        if any(x is not None for x in got.values()):
            out["positive_control"][fam] = {"sources": got, "passed": all(x == "needed" for x in got.values())}
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
                if layers.startswith("win")
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

    for k, c in sorted(cells.items(), key=lambda kv: (FAMILIES.index(kv[0][0]), kv[0][1:])):
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


# ---- examples (job pages) -------------------------------------------------------------------------------------------

HYPOTHESES = {
    "H_answer_site": "the final positions read the path's lookup statement directly; the question tokens read the "
    "binding statement",
    "H_relay": "the question tokens read both path statements and relay them to the final positions",
}


def predicted_break(h: str, fam: str, source: str, dest: str) -> bool:
    if source not in PATH[fam]:
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
    on_path = [r for r in knocked if r["source"] in PATH[r["family"]]]
    note = " (smoke: 'right' = the unedited top token)" if m["eligibility"] == "none" else ""
    groups = {
        "path_breaks": ("A path statement blocked, the answer lost", "source on the family's path, all layers, "
                        f"unedited read right, edited read wrong{note}",
                        [r for r in on_path if r["layers"] == "all" and not r[measure]]),
        "path_confusion": ("Lost to another statement's answer", "as path_breaks, and the edited top token is another "
                           "entity's answer in the same prompt (another locker, legs, capital)",
                           [r for r in on_path if not r[measure] and r["conf"]]),
        "path_survives": ("A path statement blocked from the answer site, the answer kept", "source on the path, "
                          "destination final or both, all layers, edited read still right",
                          [r for r in on_path if r["layers"] == "all" and r["dest"] in ("final", "both") and r[measure]]),
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
            n_layers = len(m["layer_sets"][r["layers"]])
            dest_words = {"question": "the question tokens", "final": "the final template positions",
                          "both": "the question and final positions", "after": "every position after it"}[r["dest"]]  # fmt: skip
            base = none[r["id"]]
            expected = {}
            if r["layers"] == "all":
                for h in HYPOTHESES:
                    expected[h] = f"not {c['answer']}" if predicted_break(h, r["family"], r["source"], r["dest"]) else c["answer"]  # fmt: skip
            examples.append({
                "group": key, "family": r["family"], "item_id": r["id"], "prompt": prompt, "spans": spans,
                "condition": f"{dest_words} cannot read the {r['source']} span ({c['source_text'][r['source']]!r}) "
                f"directly at layers {r['layers']} ({n_layers} layers); DeltaNet mode {r['mode']} (value: the span's "
                "values zeroed, its keys/betas/decays kept; absent: the span removed from the recurrence)",
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
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--families", nargs="+", choices=list(FAMILIES), default=list(FAMILIES))
    ap.add_argument("--n", type=int, default=100, help="items per family")
    ap.add_argument("--sources", nargs="+", choices=list(SOURCES), default=list(SOURCES))
    ap.add_argument("--dests", nargs="+", choices=list(DESTS), default=list(DESTS))
    ap.add_argument(
        "--layers", nargs="+", choices=["all", "win8", "win8k", "win4", "pre", "suf", "kind"], default=["all"]
    )
    ap.add_argument("--sweep", choices=["path", "path+random", "all"], default="path")
    ap.add_argument("--sweep-dests", nargs="+", choices=["question", "final", "both"], default=["question", "final", "both"])  # fmt: skip
    ap.add_argument("--absent", action="store_true", help="add the DeltaNet mode-absent rows (both, after; all layers)")
    ap.add_argument("--no-eligibility", dest="eligibility", action="store_const", const="none", default="map",
                    help="smokes: the first n items per family, all counted (scored by 'kept')")  # fmt: skip
    ap.add_argument("--k", type=int, default=3, help="examples per group")
    args = ap.parse_args()
    if args.stage == "manifest":
        assert args.why, "manifest needs --why"
        stage_manifest(args)
    elif args.stage == "run":
        stage_run(args.name)
    elif args.stage == "summarise":
        stage_summarise(args.name)
    else:
        load_token_strings()
        stage_examples(args.name, args.k)
