"""review_states (batch 53, Dan 11:45; jobs/c3/batch53.yaml `inspector_1145` item 1): the residual states behind the
review dashboard's "Look into J-space" panel (scripts/review_jspace.py). Read-only on results/ except its own run dir;
no rule, no verdict.

Sample items (the dashboard's items, src/bridge_jspace/review/items.py): every tier-1 view of docs/review_views.yaml, for
the target (BJ_TARGET). The seed-29 sample comes from the views file (items.review_sample, the verification pack's);
until it exists a planted one stands in: SEED 29, N 10 per view and model, items.sample's uniform draw. Per item, its
reader's O prompt (the item's own ids) and S prompt (its alt ids), each with the read's suffix (X0's chat read: the
space token; x51 cases store their own), and the tokens Dan lists: the bridge word, every item's mention in the locker
sentences, the asked person's pick sentence, the question's tokens and the last token (the read position).

GPU stage (`run`), one model at a time:
  1. states: one forward of each O / S prompt, every block output (layers 0..n-1) at those tokens, fp16 (asserted
     inside fp16's range) -> cache/review_states/<model>/<view>/<item>.npz.
  2. the change S - O at the tokens O and S share (same token count: every position; else the bridge word and the
     question / last tokens counted from the end), at every layer the lens maps: X0's lens part (25 signed-OMP atoms
     over the J++ letter-token atoms, x52_atoms.omp_atoms: x0_necessity.fit step for step, keeping ids, coefficients and
     energy shares) and X0's random part of the same share (statement_positions.random_subspace_part; basis seed 888 +
     layer, its QR on the CPU at L as the runs, on the GPU elsewhere), stored with the states.
  3. the rank check (inspector_1145 item 3): every item of the conflict test and the routes test (RANK_VIEWS), at L and
     the bridge word: Δ from one forward of each O / S prompt (the lookup's ids, as the runs), its J++ part
     (x0_necessity.fit), the rest and the random part of the same share; their J++ readouts (JLens.readout) and the
     ranks (1 = top, strictly larger logits counted) of S's and O's bridge words (spelling / symbol variants: best) and
     each reader's S answer (digit; number word) -> rank_check.jsonl in the run dir; Δ and the parts (fp16) in
     cache/review_states/<model>/rank/<view>.npz. The J++ share is checked against the run's stored one (checks.json).
  3a. the decisive arms of the sample's conflict-test and routes items (none, whole, without the J++ part, without its
     random part; the coordinator ~12:55: the 9B / 27B / 122B / Muse conflict runs store no top token), re-read with
     X0's code at L -> arms.jsonl: each arm's top token (id, text), switch, role (routes' lookup: route) beside the
     stored row, and whether they agree (checks.json lists every mismatch).
  4. the unembedding (lm_head and final norm, as loaded) -> cache/review_states/<model>/head.safetensors + head.json,
     so the panel reads out on the Mac without the weights; calibration readouts (J++ and logit lens, on the GPU) of 5
     items' vectors at L and the bridge word -> calib.jsonl (the panel's CPU readout is tested against them).

The run dir results/review_states/<run>/ holds manifest.json (written before any model work), plan.json, checks.json,
rank_check.jsonl and calib.jsonl; the states are in cache/ (gitignored; pull them with the rsync line the run prints).

uv run python scripts/review_states.py plan                                   # CPU: BJ_TARGET's sample, tokens, sizes
BJ_TARGET=qwen3.5-9b uv run python scripts/review_states.py run --name qwen35_9b_review_states   # GPU
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.review import items as I

EXP = "review_states"
RESULTS = pins.RESULTS_DIR / EXP
CACHE = pins.REPO_ROOT / "cache" / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
SEED, N = 29, 10  # the planted sample (uniform, per view and model) until items.review_sample exists
K = 25  # X0's lens part
RANK_VIEWS = ("main_swap", "routes")  # the conflict test (X0's main test) and the routes test
TIER1_FALLBACK = ("main_swap", "routes", "x8_writes", "sentence_order")  # until the views file marks tier 1
FP16_MAX = 65504.0
N_CALIB = 5
TOP_CALIB = 50
LOCKER = re.compile(r"[Tt]he locker of (?:the )?([\w-]+) is")
ASKED = re.compile(r"\b([A-Z][a-z]+)'s pick")


# ---- the sample (CPU) ----------------------------------------------------------------------------------------------


def tier1_views() -> list[dict]:
    """The views the sample covers: those the views file marks `tier: 1`, else TIER1_FALLBACK's that exist."""
    views = I.spec()["views"]
    marked = [v for v in views if v.get("tier") == 1]
    return marked or [v for v in views if v["id"] in TIER1_FALLBACK]


def sample_items(v: dict, model: str) -> tuple[list[dict], str]:
    """The view's fixed seed-29 sample for the model (the views file's fixed_sample, read by review.fixed.samples), or,
    for a views file without one, the planted sample."""
    from bridge_jspace.review import fixed as F

    got = F.samples(v, SEED, [model])
    if got is not None:
        return [it for s in got.get(model, []) for it in s["items"]], f"fixed_sample (seed {SEED})"
    pool = I.items(v["id"], model)
    got = I.sample(pool, SEED, N, "uniform", v["id"], model)
    return [it for s in got for it in s["items"]], f"planted: items.sample(seed {SEED}, n {N}, uniform)"


def hf_tokenizer(model: str):
    """The model's pinned tokenizer.json as a transformers fast tokenizer (encode / decode as the runs' tokenizer)."""
    from huggingface_hub import hf_hub_download
    from transformers import PreTrainedTokenizerFast

    t = pins.TARGETS[model]
    try:
        path = hf_hub_download(t["repo"], "tokenizer.json", revision=t["revision"], local_files_only=True)
    except Exception:
        path = hf_hub_download(t["repo"], "tokenizer.json", revision=t["revision"])
    return PreTrainedTokenizerFast(tokenizer_file=path)


def space_suffix(tok) -> list[int]:
    """X0's chat read appends a digit's space token (suite_v1.ids(tok, " "))."""
    return list(tok(" ", add_special_tokens=False).input_ids)


def item_prompts(it: dict, tok) -> dict:
    """The item's reader's O and S prompts as read (ids + the read's suffix), the bridge word's position in each and the
    question each asks. x51 cases carry pos / suffix per reader and Zach's passages a pos per reader and no suffix (no
    "Answer:", no space: x50_zach's read); X0 / routes / 51.10 cases one pos and the chat read's space token (stored as
    "space" in 51.10's, appended by X0.read_logits otherwise)."""
    case, w = it["case"], it["reader"]
    if not case:
        raise ValueError(f"{it['id']}: no case (prompts) for this item")
    rd = case["readers"][w]
    pos = int(rd.get("pos", case.get("pos")))
    if "suffix" in rd:
        suffix = list(rd["suffix"])
    elif it["kind"] == "zach":
        suffix = []
    elif "space" in case:
        suffix = list(case["space"])
    else:
        suffix = space_suffix(tok) if case.get("rendering", "chat") == "chat" else []
    q = rd.get("question", "")
    span = rd.get("span") or case.get("span")
    return {"O": list(rd["ids"]["org"]) + suffix, "S": list(rd["ids"]["alt"]) + suffix, "pos": pos,
            "suffix": suffix, "question": {"O": q, "S": rd.get("cf_question", q)},
            "span": list(range(int(span[0]), int(span[1]) + 1)) if span else []}  # fmt: skip


def offsets(tok, ids: list[int]) -> list[tuple[int, int]]:
    """Each token's character span in the decoded prompt: by re-encoding the decode when it gives the same ids, else by
    decoding prefixes."""
    text = tok.decode(ids, skip_special_tokens=False)
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    if list(enc.input_ids) == list(ids):
        return [tuple(o) for o in enc.offset_mapping]
    out, prev = [], 0
    for i in range(len(ids)):
        n = len(tok.decode(ids[: i + 1], skip_special_tokens=False))
        out.append((prev, n))
        prev = n
    return out


def tokens_in(spans: list[tuple[int, int]], a: int, b: int) -> list[int]:
    return [i for i, (s, e) in enumerate(spans) if s < b and e > a and e > s]


def roles(tok, ids: list[int], pos: int, question: str, span: list[int] | None = None) -> dict[int, list[str]]:
    """Token position -> its roles in one prompt: bridge, bridge span (Zach's multi-token names), mention: <item> (in a
    locker sentence), pick sentence (the asked person's), question, last."""
    text = tok.decode(ids, skip_special_tokens=False)
    spans = offsets(tok, ids)
    out: dict[int, list[str]] = collections.defaultdict(list)
    out[pos].append("bridge")
    for p in span or []:
        if p != pos:
            out[p].append("bridge span")
    q_at = text.rfind(question) if question else -1
    scene_end = q_at if q_at >= 0 else len(text)
    for m in LOCKER.finditer(text[:scene_end]):
        for i in tokens_in(spans, m.start(1), m.end(1)):
            out[i].append(f"mention: {m.group(1)}")
    asked = ASKED.search(question or "")
    if asked:
        pick = re.compile(rf"\b{re.escape(asked.group(1))} picked (?:the )?[\w-]+\.")
        for m in pick.finditer(text[:scene_end]):
            for i in tokens_in(spans, m.start(), m.end()):
                out[i].append("pick sentence")
    if q_at >= 0:
        for i in tokens_in(spans, q_at, q_at + len(question)):
            out[i].append("question")
    out[len(ids) - 1].append("last")
    return {p: sorted(set(r), key=r.index) for p, r in sorted(out.items())}


def layout(tok, it: dict) -> dict:
    """The positions saved per prompt and the pairs (O index, S index) where the change S - O is defined: with the same
    token count, every saved position of either prompt (both prompts saved there); otherwise the bridge word and the
    tail (question, last) counted from the end where the tokens agree."""
    p = item_prompts(it, tok)
    ro = roles(tok, p["O"], p["pos"], p["question"]["O"], p["span"])
    rs = roles(tok, p["S"], p["pos"], p["question"]["S"], p["span"])
    lo, ls = len(p["O"]), len(p["S"])
    if lo == ls:
        pos = sorted(set(ro) | set(rs))
        pos_o, pos_s, pairs = pos, pos, [(i, i) for i in range(len(pos))]
    else:
        pos_o, pos_s = sorted(ro), sorted(rs)
        shift = ls - lo
        pairs = []
        for i, q in enumerate(pos_o):
            j = q + shift if q != p["pos"] else p["pos"]
            if j in pos_s and (q == p["pos"] or p["O"][q] == p["S"][j]):
                pairs.append((i, pos_s.index(j)))
    return {"ids_O": p["O"], "ids_S": p["S"], "pos": p["pos"], "suffix": p["suffix"], "pos_O": pos_o, "pos_S": pos_s,
            "roles_O": {str(q): ro.get(q, []) for q in pos_o}, "roles_S": {str(q): rs.get(q, []) for q in pos_s},
            "pairs": pairs}  # fmt: skip


def item_file(view_id: str, item_id: str) -> str:
    """The item's states file under cache/review_states/<model>/: <view>/<item id, path-safe>.npz."""
    return f"{view_id}/{re.sub(r'[^A-Za-z0-9_.-]+', '_', item_id)}.npz"


# ---- the rank check's items and tokens (CPU) -----------------------------------------------------------------------


def variant_tokens(tok, name: str, domain: str | None) -> dict[str, list[int]]:
    """A bridge word's tokens. "word": its spellings that are one token (as is, leading space, capitalised, both;
    x51_answer.variants) and, as whole tokens, its symbol (x52_atoms.ELEMENT_SYMBOL, not SYMBOL_DROPPED's: "He" is the
    pronoun) or Greek letter (x52_atoms.GREEK_CHAR). "pieces": those and the first token of every spelling the
    tokenizer splits (x51_answer.variant_ids: 51.12's bridge tokens)."""
    from scripts import x51_answer as A
    from scripts import x52_atoms as AT

    word = set()
    for v in A.variants(name):
        ids = tok(v, add_special_tokens=False).input_ids
        if len(ids) == 1:
            word.add(int(ids[0]))
    alias: list[str] = []
    low = name.lower()
    if domain in (None, "elements") and low in AT.ELEMENT_SYMBOL and low not in AT.SYMBOL_DROPPED:
        alias.append(AT.ELEMENT_SYMBOL[low])
    if domain in (None, "greek") and low in AT.GREEK_CHAR:
        alias += list(AT.GREEK_CHAR[low])
    for a in alias:
        for v in (a, " " + a):
            ids = tok(v, add_special_tokens=False).input_ids
            if len(ids) == 1:
                word.add(int(ids[0]))
    return {"word": sorted(word), "pieces": sorted(word | set(A.variant_ids(tok, [name])))}


def answer_tokens(tok, answer: str, read_id: int | None) -> dict[str, list[int]]:
    """An answer's tokens: digit (the read's token and the first token of its spellings) and, for a single digit, its
    number word (x51_answer.word_ids, one-token letter variants)."""
    from scripts import x51_answer as A

    a = str(answer).strip()
    digit = set(A.variant_ids(tok, [a])) | ({int(read_id)} if read_id is not None else set())
    word = A.word_ids(tok, [A.number_word(a)], True) if len(a) == 1 and a.isdigit() else []
    return {"digit": sorted(digit), "word": sorted(word)}


def rank_items(model: str, tok) -> dict[str, list[dict]]:
    """Per rank view, one row per (run, scene, condition) of its item set (both readers share Δ: the lookup's prompts,
    identical through the bridge word): the lookup's O / S ids, the bridge position, the tokens to rank."""
    out: dict[str, list[dict]] = {}
    for vid in RANK_VIEWS:
        try:
            v = I.view(vid)
        except StopIteration:
            continue
        rows, seen = [], set()
        for it in I.items(vid, model):
            case = it["case"]
            key = (it["run"], it["scene"], it["condition"])
            if case is None or key in seen:
                continue
            seen.add(key)
            rd = case["readers"][I.READERS[0]]
            dom = case.get("domain")
            toks = {f"{who}_bridge_{kind}": ids for who, name in (("S", case["cf_bridge"]), ("O", case["bridge"]))
                    for kind, ids in variant_tokens(tok, name, dom).items()}  # fmt: skip
            for w, r in case["readers"].items():
                for kind, ids in answer_tokens(tok, r["cf_answer"], r.get("tok_b")).items():
                    toks[f"{w}_S_answer_{kind}"] = ids
            rows.append({"view": vid, "key": "|".join(str(k) for k in key if k), "run": it["run"], "scene": it["scene"],
                         "condition": it["condition"], "layer": it["layer"], "bridge": case["bridge"],
                         "cf_bridge": case["cf_bridge"], "domain": dom, "pos": int(case["pos"]),
                         "ids_O": list(rd["ids"]["org"]), "ids_S": list(rd["ids"]["alt"]), "tokens": toks,
                         "answers": {w: [r["answer"], r["cf_answer"]] for w, r in case["readers"].items()}})  # fmt: skip
        out[vid] = rows
        assert len({r["layer"] for r in rows}) <= 1, f"{vid}: items at several layers"
        del v
    return out


def stored_shares(model: str, rows: list[dict]) -> dict[str, float]:
    """The runs' own J++ share (k 25, signed) per rank row, where stored: X0's shares.jsonl at the layer, routes'
    norms.jsonl share_jpp."""
    out: dict[str, float] = {}
    for run in sorted({r["run"] for r in rows}):
        mine = [r for r in rows if r["run"] == run]
        layer = mine[0]["layer"]
        for s in I.read_jsonl(f"{run}/shares.jsonl"):
            if (s.get("dict"), s.get("k"), s.get("omp")) == ("jpp", K, "signed") and s.get("layer", layer) == layer \
                    and s.get("rendering", "chat") == "chat":  # fmt: skip
                out[f"{run}|{s['scene']}"] = s["share"]
        for s in I.read_jsonl(f"{run}/norms.jsonl"):
            if "share_jpp" in s:
                out[f"{run}|{s['scene']}|{s['condition']}"] = s["share_jpp"]
    return out


# ---- the plan (CPU) ------------------------------------------------------------------------------------------------


def model_layer(model: str) -> int:
    return int(I.spec()["models"][model]["layer"])


def build_plan(model: str, tok=None, with_rank: bool = True) -> dict:
    """Everything the GPU stage reads: the sample items with their prompts and positions, the rank rows."""
    tok = tok or hf_tokenizer(model)
    assert model in I.spec()["models"], f"{model} is not in docs/review_views.yaml's models"
    sample, sources, dropped = [], {}, collections.Counter()
    for v in tier1_views():
        got, src = sample_items(v, model)
        sources[v["id"]] = src
        for it in got:
            try:
                lay = layout(tok, it)
            except (KeyError, ValueError, TypeError) as e:
                dropped[f"{v['id']}: {type(e).__name__}: {e}"] += 1
                continue
            sample.append({"view": v["id"], "item": it["id"], "kind": v["kind"], "reader": it["reader"],
                           "scene": it["scene"], "condition": it["condition"], "run": it["run"], "layer": it["layer"],
                           "file": item_file(v["id"], it["id"]), **lay})  # fmt: skip
    rank = rank_items(model, tok) if with_rank else {}
    return {"model": model, "layer": model_layer(model), "sample": sample, "sample_sources": sources,
            "dropped": dict(dropped), "rank": rank}  # fmt: skip


def plan_summary(plan: dict, n_layers: int, d: int) -> dict:
    """Counts and the cache size the run will write (fp16 states and random parts, atoms)."""
    s = plan["sample"]
    pos = sum(len(x["pos_O"]) + len(x["pos_S"]) for x in s)
    pairs = sum(len(x["pairs"]) for x in s)
    states_gb = pos * n_layers * d * 2 / 1e9
    rand_gb = pairs * n_layers * d * 2 / 1e9
    rank_n = {v: len(r) for v, r in plan["rank"].items()}
    rank_gb = sum(rank_n.values()) * 3 * d * 2 / 1e9
    return {"model": plan["model"], "layer": plan["layer"], "items": len(s),
            "per_view": dict(collections.Counter(x["view"] for x in s)), "sources": plan["sample_sources"],
            "dropped": plan["dropped"], "positions_saved": pos, "change_pairs": pairs,
            "median_positions_per_prompt": float(np.median([len(x["pos_O"]) for x in s])) if s else 0,
            "rank_rows": rank_n, "cache_gb": {"states": round(states_gb, 2), "random_parts": round(rand_gb, 2),
                                              "rank": round(rank_gb, 3)}}  # fmt: skip


def stage_plan(model: str, with_rank: bool = True, out: Path | None = None) -> dict:
    t = pins.TARGETS[model]
    cfg = model_config(model)
    plan = build_plan(model, with_rank=with_rank)
    summary = plan_summary(plan, t["n_layers"], cfg["d"])
    print(json.dumps(summary, indent=1), flush=True)
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / "plan.json").write_text(json.dumps(plan) + "\n")
        print("wrote", out / "plan.json")
    return summary


def model_config(model: str) -> dict:
    """d_model and vocab from the pinned config.json (text config), for sizes."""
    from huggingface_hub import hf_hub_download

    t = pins.TARGETS[model]
    try:
        path = hf_hub_download(t["repo"], "config.json", revision=t["revision"], local_files_only=True)
    except Exception:
        path = hf_hub_download(t["repo"], "config.json", revision=t["revision"])
    c = json.loads(Path(path).read_text())
    c = c.get("text_config", c.get("llm_config", c))
    return {"d": int(c["hidden_size"]), "vocab": int(c.get("vocab_size", 0))}


# ---- GPU -----------------------------------------------------------------------------------------------------------


def manifest(name: str, model: str, layer: int) -> dict:
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state
    from scripts import x0_necessity as X

    return {"exp": EXP, "run": name, "spec": "jobs/c3/batch53.yaml (inspector_1145, item 1)",
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
            "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "k": K,
            "views_file": {"path": "docs/review_views.yaml", "sha256": pins.sha256_file(I.VIEWS_FILE)},
            "cache": f"cache/{EXP}/{model}",
            "seeds": {"sample": SEED, "random_subspace": "888 + layer (X0's; CPU QR at L, GPU QR elsewhere)"},
            "verdict": "none (inputs for the review dashboard's J-space panel)"}  # fmt: skip


def record_states(model, ids: list[int], positions: list[int], layers: tuple[int, ...]):
    """[len(positions), len(layers), d] fp32 on the CPU: the block outputs of one forward at those positions."""
    import torch

    _, rec = model.run(torch.tensor([ids], device=model.device), record=layers)
    return torch.stack([rec[la][positions].float().cpu() for la in layers], dim=1)


def random_part_at(x, share, layer: int, exact: bool):
    """X0's random part of each row of x at its share: basis seed 888 + layer; exact (L): the CPU QR the runs use."""
    import torch

    from scripts import statement_positions as SP
    from scripts import x0_necessity as X

    g = torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)
    if exact:
        basis = SP.random_basis(x.shape[1], g).to(x.device)
    else:
        q, r = torch.linalg.qr(torch.randn(x.shape[1], x.shape[1], generator=g).to(x.device))
        basis = q * torch.sign(torch.diagonal(r))
    return SP.random_subspace_part(x, share, basis)


def head_record(model) -> tuple[dict, dict]:
    """The unembedding as the model applies it (Model.unembed): lm_head weight, final norm weight, the norm's kind and
    eps, Muse's multiplier and softcap."""
    import torch

    cfg = model.hf.config.get_text_config()
    norm = model.final_norm
    w = model.hf.lm_head.weight
    if w.dtype not in (torch.bfloat16, torch.float16, torch.float32):
        raise TypeError(f"lm_head is {w.dtype}: not stored")
    eps = getattr(norm, "eps", getattr(norm, "variance_epsilon", None))
    kinds = {"Qwen3_5RMSNorm": "one_plus_weight_fp32", "Qwen3_5MoeRMSNorm": "one_plus_weight_fp32",
             "MuseGlimmerRMSNorm": "weight_fp32_pow", "NemotronHRMSNorm": "weight_after_cast"}  # fmt: skip
    rec = {"norm_class": type(norm).__name__, "norm_kind": kinds.get(type(norm).__name__, "unknown"), "eps": eps,
           "gain": pins.TARGETS[pins.TARGET]["norm_gain"], "lm_head_dtype": str(w.dtype),
           "output_multiplier": getattr(cfg, "output_multiplier", None),
           "final_logit_softcapping": getattr(cfg, "final_logit_softcapping", None),
           "vocab": int(w.shape[0]), "d": int(w.shape[1]), "target": pins.TARGET}  # fmt: skip
    tensors = {"lm_head.weight": w.detach().to("cpu").contiguous(),
               "norm.weight": norm.weight.detach().to("cpu").contiguous()}  # fmt: skip
    return tensors, rec


ARM_KINDS = ("x0", "routes")  # views whose decisive arms are re-read for the sample (the coordinator, ~12:55)
ARMS = ("none", "whole", "no_part", "no_rand")
POINTER_ARMS = ("no_alf", "no_alf_rand")  # routes: without the pointer directions U / without their random part
ROUTES_ARM = {"none": "none", "whole": "whole", "no_jpp": "no_part", "no_jpp_rand": "no_rand", "no_alf": "no_alf",
              "no_alf_rand": "no_alf_rand"}  # fmt: skip


def pointer_basis(run: str):
    """The routes run's pointer directions U [d, r]: its manifest's alf_from (x6_routes records `alf_from or
    STATES[target]`): a refit's pcf.npz (batch 43) where that dir has one, else x0_massmean.subspaces of that probe run."""
    from scripts import x0_massmean as MM
    from scripts import x6_routes as R

    src = I.read_json(f"{run}/manifest.json").get("alf_from") or R.STATES[pins.TARGET]
    pcf = pins.RESULTS_DIR / src / "pcf.npz"
    return np.load(pcf)["P"] if pcf.exists() else MM.subspaces(src)[0]["Alf"]


def arm_labels(v: dict) -> dict[str, str]:
    """Our arm name -> the view's label for it: none, whole, without the J++ part (k 25, signed) and without its random
    part (X0's no_part / no_rand; routes' no_jpp / no_jpp_rand)."""
    out = {}
    for label, a in v["filters"]["arms"].items():
        if v["kind"] == "x0":
            name = a[0]
            if name in ("none", "whole") or (name in ("no_part", "no_rand") and tuple(a[1:]) == ("jpp", K, "signed")):
                out[name] = label
        elif a in ROUTES_ARM:
            out[ROUTES_ARM[a]] = label
    return out


def stage_arms(model, jdic, layer: int, tok, out: Path) -> dict:
    """The decisive arms of the sample's conflict-test and routes items, re-read with X0's own code at L (Δ from the
    lookup's prompts, x0_necessity.fit, X0's random part, exp04_brew_parts.AddRows at the bridge word, X0.read_logits /
    read_row; routes' lookup route by x6_routes.classify): each arm's top token and label beside the stored one."""
    import torch

    from scripts import x0_necessity as X
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    dev = model.device
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    n, bad = 0, []
    with (out / "arms.jsonl").open("w") as f, torch.no_grad():
        for v in tier1_views():
            if v["kind"] not in ARM_KINDS:
                continue
            labels = arm_labels(v)
            items, _ = sample_items(v, pins.TARGET)
            for it in items:
                case, w = it["case"], it["reader"]
                rd, lk, pos = case["readers"][w], case["readers"][X.LOOKUP]["ids"], int(case["pos"])
                h = {x: model.run(torch.tensor([lk[x]], device=dev), record=(layer,))[1][layer][pos].float()
                     for x in ("org", "alt")}  # fmt: skip
                x = (h["alt"] - h["org"])[None]
                part = X.fit(jdic, x, K, "signed")
                share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                vec = {"whole": x, "no_part": x - part, "no_rand": x - random_part_at(x, share, layer, exact=True)}
                names = list(ARMS)
                if v["kind"] == "routes":  # the routes card's decisive arms: without the pointer directions U
                    u = torch.tensor(pointer_basis(it["run"]), dtype=torch.float32, device=dev)
                    ptr = (x @ u) @ u.T
                    psh = ptr.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                    vec |= {"no_alf": x - ptr, "no_alf_rand": x - random_part_at(x, psh, layer, exact=True)}
                    names += list(POINTER_ARMS)
                edits = [{}] + [{layer: AddRows(vec[a], [pos])} for a in names[1:]]
                space = list(case.get("space") or space_suffix(tok))
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, case.get("rendering", "chat"), space, ws)
                for a, lg in zip(names, logits, strict=True):
                    r = X.read_row(lg, rd, digits)
                    route = R.classify(r["top"], case) if v["kind"] == "routes" and w == X.LOOKUP else None
                    label = labels.get(a)
                    st = it["rows"][w].get(label) if label else None
                    same = None
                    if st is not None:
                        same = int(st["switched"]) == r["switched"] and st.get("role", r["role"]) == r["role"]
                        if "top" in st:
                            same = same and int(st["top"]) == r["top"]
                        if route is not None and "route" in st:
                            same = same and st["route"] == route
                    rec = {"view": v["id"], "item": it["id"], "reader": w, "arm": a, "label": label, "layer": layer,
                           "top": r["top"], "top_text": tok.decode([r["top"]]), "switched": r["switched"],
                           "role": r["role"], "route": route, "p_org": r["p_org"], "p_alt": r["p_alt"],
                           "share": round(float(share[0]), 6),
                           "stored": {k: st.get(k) for k in ("top", "role", "switched", "route")} if st else None,
                           "match": same}  # fmt: skip
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n += 1
                    if same is False:
                        bad.append(f"{it['id']} {a}: stored {rec['stored']}, now top {r['top']} {r['role']} {route}")
    return {"rows": n, "mismatches": bad}


def ranks_of(logits, sets: dict[str, list[int]]) -> dict[str, int | None]:
    """Per token set: the best rank (1 + tokens with a strictly larger logit) among its ids (x51_answer.rank_of)."""
    out: dict[str, int | None] = {}
    for k, ids in sets.items():
        out[k] = min((int((logits > logits[t]).sum()) + 1 for t in ids), default=None)
    return out


def stage_run(name: str) -> Path:
    import os

    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import x0_necessity as X
    from scripts import x52_atoms as AT

    pins.check_run_name(name)
    model_key = pins.TARGET
    layer = model_layer(model_key)
    if os.environ.get("BJ_PREDICTED_LAYER"):  # Lightning: its committed L must be the views file's
        assert int(os.environ["BJ_PREDICTED_LAYER"]) == layer, f"BJ_PREDICTED_LAYER != the views file's L{layer}"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, model_key, layer)
    (out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    tok = hf_tokenizer(model_key)
    plan = build_plan(model_key, tok)
    (out / "plan.json").write_text(json.dumps({**plan, "rank": {v: [{k: x for k, x in r.items() if not k.startswith("ids_")}
                                                                    for r in rows] for v, rows in plan["rank"].items()}})
                                   + "\n")  # fmt: skip
    t0 = time.time()
    model = load_model()
    lens = JLens(model, "jpp")
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    dev = model.device
    n_layers = pins.N_LAYERS
    layers = tuple(range(n_layers))
    lens_layers = [la for la in layers if la in lens.source_layers]
    letters = model.letter_token_ids()
    lt = letters.tolist()
    root = CACHE / model_key
    root.mkdir(parents=True, exist_ok=True)
    checks: dict[str, Any] = {"target": model_key, "layer": layer, "load_s": round(time.time() - t0, 1)}

    # 4. the head first: small, and the panel needs it whatever happens later
    from safetensors.torch import save_file

    try:
        tensors, head = head_record(model)
        save_file(tensors, str(root / "head.safetensors"))
        (root / "head.json").write_text(json.dumps({**head, "run": name}, indent=1) + "\n")
        checks["head"] = {k: head[k] for k in ("norm_class", "norm_kind", "lm_head_dtype", "vocab", "d")}
        del tensors
    except TypeError as e:  # a quantized lm_head: the panel then needs the head from the checkpoint (x52_atoms fetch)
        checks["head"] = f"not stored: {e}"

    # 1. states of the sample's prompts
    sample = plan["sample"]
    states: list[dict] = []
    big = 0.0
    with torch.no_grad():
        for s in progress(sample, f"{model_key}: states at every layer (item)"):
            h_o = record_states(model, s["ids_O"], s["pos_O"], layers)
            h_s = record_states(model, s["ids_S"], s["pos_S"], layers)
            big = max(big, float(h_o.abs().max()), float(h_s.abs().max()))
            states.append({"O": h_o, "S": h_s})
    checks["max_abs_state"] = big
    # fp16 as asked; a state at or past half fp16's range (its change could overflow) is stored in fp32 instead
    store = np.float16 if 2 * big < FP16_MAX else np.float32
    checks["stored_dtype"] = np.dtype(store).name

    # 2. the change's lens part (atoms) and random part at every lens layer
    rows = [(i, a, b) for i, s in enumerate(sample) for a, b in s["pairs"]]
    n_rows = len(rows)
    d = states[0]["O"].shape[-1] if states else 0
    atoms_ids = np.full((n_rows, n_layers, K), -1, dtype=np.int32)
    atoms_coef = np.zeros((n_rows, n_layers, K), dtype=np.float32)
    atoms_gain = np.zeros((n_rows, n_layers, K), dtype=np.float32)
    jshare = np.full((n_rows, n_layers), np.nan, dtype=np.float32)
    rshare = np.full((n_rows, n_layers), np.nan, dtype=np.float32)
    rand = np.zeros((n_rows, n_layers, d), dtype=store)
    if n_rows:
        delta = torch.stack([states[i]["S"][b] - states[i]["O"][a] for i, a, b in rows])  # [R, layers, d]
        with torch.no_grad():
            for la in progress(lens_layers, f"{model_key}: the change's 25 atoms and random part (layer)"):
                x = delta[:, la].to(dev)
                dic = lens.vectors(la, letters)
                chosen, coefs, gains, approx = AT.omp_atoms(dic, x, K)
                sq = (x.double().norm(dim=-1) ** 2).clamp_min(1e-30)
                share = (approx.double().norm(dim=-1) ** 2 / sq).float()
                rp = random_part_at(x, share, la, exact=(la == layer))
                atoms_ids[:, la] = np.asarray(lt)[chosen.cpu().numpy()]
                atoms_coef[:, la] = coefs.float().cpu().numpy()
                atoms_gain[:, la] = gains.float().cpu().numpy()
                jshare[:, la] = share.cpu().numpy()
                rshare[:, la] = ((rp.double().norm(dim=-1) ** 2) / sq).float().cpu().numpy()
                rand[:, la] = rp.cpu().numpy().astype(store)
                if la == layer:  # the runs' own fit at L, for the record
                    ref = X.fit(dic, x, K, "signed")
                    checks["omp_atoms_vs_fit_max_abs_diff_at_L"] = float((approx - ref).abs().max())
                del dic, chosen, coefs, gains, approx, x
                torch.cuda.empty_cache()
    # write one file per item
    for i, s in enumerate(progress(sample, f"{model_key}: writing states (item)")):
        mine = [r for r, (j, _, _) in enumerate(rows) if j == i]
        f = root / s["file"]
        f.parent.mkdir(parents=True, exist_ok=True)
        np.savez(f, h_O=states[i]["O"].numpy().astype(store), h_S=states[i]["S"].numpy().astype(store),
                 pos_O=np.asarray(s["pos_O"], dtype=np.int32), pos_S=np.asarray(s["pos_S"], dtype=np.int32),
                 pairs=np.asarray(s["pairs"], dtype=np.int32).reshape(-1, 2), ids_O=np.asarray(s["ids_O"], dtype=np.int32),
                 ids_S=np.asarray(s["ids_S"], dtype=np.int32), atoms_ids=atoms_ids[mine], atoms_coef=atoms_coef[mine],
                 atoms_gain=atoms_gain[mine], jpp_share=jshare[mine], rand=rand[mine], rand_share=rshare[mine],
                 lens_layers=np.asarray(lens_layers, dtype=np.int32),
                 meta=np.asarray(json.dumps({k: s[k] for k in ("view", "item", "kind", "reader", "scene", "condition",
                                                                "run", "layer", "pos", "suffix", "roles_O", "roles_S")})))  # fmt: skip

    # 3a. the decisive arms of the sample's conflict-test and routes items (their top tokens, for the cards)
    jdic = lens.vectors(layer, letters)
    checks["arms"] = stage_arms(model, jdic, layer, tok, out)
    print("arms:", json.dumps(checks["arms"])[:2000], flush=True)

    # 3b. the rank check at L, every item of the conflict and routes tests
    stored = stored_shares(model_key, [r for rs in plan["rank"].values() for r in rs])
    gaps: dict[str, list[float]] = collections.defaultdict(list)
    with (out / "rank_check.jsonl").open("w") as fout, torch.no_grad():
        for vid, rrows in plan["rank"].items():
            if not rrows:
                continue
            deltas = []
            for r in progress(rrows, f"{model_key}: {vid}: Δ at L{layer} (scene)"):
                h = {v: model.run(torch.tensor([r[f"ids_{v}"]], device=dev), record=(layer,))[1][layer][r["pos"]].float()
                     for v in ("O", "S")}  # fmt: skip
                deltas.append(h["S"] - h["O"])
            x = torch.stack(deltas).to(dev)
            jpp = X.fit(jdic, x, K, "signed")
            sq = (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            share = jpp.norm(dim=-1) ** 2 / sq
            rp = random_part_at(x, share, layer, exact=True)
            parts = {"jpp": jpp, "rest": x - jpp, "rand": rp}
            (root / "rank").mkdir(exist_ok=True)
            np.savez(root / "rank" / f"{vid}.npz", keys=np.asarray([r["key"] for r in rrows]),
                     delta=x.cpu().numpy().astype(store), jpp=jpp.cpu().numpy().astype(store),
                     rand=rp.cpu().numpy().astype(store))  # fmt: skip
            for i0 in range(0, len(rrows), 64):
                lg = {k: lens.readout(v[i0 : i0 + 64], layer).float() for k, v in parts.items()}
                for j, r in enumerate(rrows[i0 : i0 + 64]):
                    i = i0 + j
                    ref = stored.get(f"{r['run']}|{r['scene']}" + (f"|{r['condition']}" if r["condition"] else ""))
                    if ref is not None:
                        gaps[vid].append(abs(float(share[i]) - ref))
                    rec = {"view": vid, "key": r["key"], "run": r["run"], "scene": r["scene"], "condition": r["condition"],
                           "layer": layer, "bridge": r["bridge"], "cf_bridge": r["cf_bridge"], "answers": r["answers"],
                           "share": round(float(share[i]), 6),
                           "rand_share": round(float((rp[i].norm() ** 2 / sq[i]).item()), 6), "stored_share": ref,
                           "ranks": {k: ranks_of(lg[k][j], r["tokens"]) for k in parts}}  # fmt: skip
                    fout.write(json.dumps(rec) + "\n")
            del x, jpp, rp, parts
    checks["rank_share_vs_stored"] = {v: {"n": len(g), "max_abs_gap": max(g) if g else None} for v, g in gaps.items()}

    # 4b. calibration readouts (GPU) for the CPU panel's tests
    with (out / "calib.jsonl").open("w") as fout, torch.no_grad():
        for i, s in enumerate(sample[:N_CALIB]):
            a = s["pos_O"].index(s["pos"])
            b = s["pos_S"].index(s["pos"])
            ho, hs = states[i]["O"][a, layer].to(dev), states[i]["S"][b, layer].to(dev)
            x = (hs - ho)[None]
            jp = X.fit(jdic, x, K, "signed")
            vecs = {"state_O": ho[None], "state_S": hs[None], "change": x, "jpp": jp, "rest": x - jp}
            for k, v in vecs.items():
                for lens_name, lg in (
                    ("jpp", lens.readout(v, layer)[0].float()),
                    ("logit", model.unembed(v)[0].float()),
                ):
                    top = torch.topk(lg, TOP_CALIB)
                    fout.write(json.dumps({"item": s["item"], "view": s["view"], "file": s["file"], "layer": layer,
                                           "vector": k, "lens": lens_name, "top_ids": top.indices.tolist(),
                                           "top_logits": top.values.tolist(),
                                           "ranks": {str(t): int((lg > lg[t]).sum()) + 1 for t in top.indices.tolist()[:10]}})
                               + "\n")  # fmt: skip
    del jdic
    checks["sample_items"] = len(sample)
    checks["change_rows"] = n_rows
    checks["seconds"] = round(time.time() - t0, 1)
    (out / "checks.json").write_text(json.dumps(checks, indent=1) + "\n")
    print(json.dumps(checks, indent=1), flush=True)
    print(
        f"wrote {out} and {root}; pull the states with:\n  rsync -a <box>:bridge-jspace/cache/{EXP}/{model_key}/ "
        f"cache/{EXP}/{model_key}/",
        flush=True,
    )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run"])
    ap.add_argument("--name")
    ap.add_argument("--model", default=None, help="plan: a views-file model key (default BJ_TARGET)")
    ap.add_argument("--no-rank", action="store_true", help="plan: skip the rank check's rows")
    ap.add_argument("--out", type=Path, default=None, help="plan: write plan.json here")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.model or pins.TARGET, not a.no_rank, a.out)
    else:
        assert a.name, "--name"
        stage_run(a.name)


if __name__ == "__main__":
    main()
