"""x0_necessity (X0, jobs/c3/X0.md): is C3's split real at a layer fixed in advance, and is it about the J++-space?

At the bridge's word and layer L, Δ = h_alt - h_org (one row). Arms on the org run: whole (Δ), and per dictionary D
(J++, W_U, W_E, random; k-atom OMP over the target's letter-token atoms) no_part (Δ - D(Δ)) and no_rand (Δ minus a
random subspace's part of D(Δ)'s share). A lookup (PP) and a recall (PM) read the identical patched context. Switch =
the top token over the vocabulary at the read step is the alt answer's first token (Dan, 24 Oct: the verdict's read;
chat: the prompt with a digit's space token appended, as on 23 Oct; raw: the first non-whitespace token of the greedy
continuation of a prompt ending 'Answer:'). The cand read (alt first among the digit tokens) is logged, descriptive.

Per cell (rendering, layer, reader, dictionary, k): S_x = share switched by arm x; Jdep = 1 - S_no_part / S_whole;
Rdep = 1 - S_no_rand / S_whole; excess = Jdep - Rdep; 95% percentile CIs from a cluster bootstrap over the org bridge
entity (10,000 resamples, seed 0). Valid iff S_whole >= 0.30 and >= 30 items switched by the whole edit. Labels:
around (excess <= 0.10, upper bound <= 0.20), through (Jdep >= 0.30, excess >= 0.20, lower bound >= 0.10), else mixed.
Rule (23 Oct, at the predicted layer, chat rendering, J++): confirmed iff lookup excess <= 0.10 and recall Jdep >=
0.30; killed iff lookup excess >= 0.20 or recall Jdep < 0.20; else not confirmed; can't tell if either cell is invalid.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson

EXP = "x0_necessity"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "X0.md"
DICTS = ("jpp", "wu", "we", "rand")  # J++ (main arm), the logit lens's W_U, the input embeddings W_E, Gaussian
K_MAIN = 25
K_CURVE = (10, 50, 100)  # at the predicted layer only, for CURVE_DICTS
CURVE_DICTS = ("jpp", "we")
ARMS = ("whole", "no_part", "no_rand")
READERS = ("PP", "PM")  # lookup, recall
LOOKUP, RECALL = READERS
RAND_DICT_SEED, SUBSPACE_SEED = 777, 888  # + layer, as on 23 Oct
BOOT_SEED, N_BOOT = 0, 10_000
VALID_S, VALID_N = 0.30, 30
AROUND_EXCESS, AROUND_HI = 0.10, 0.20
THROUGH_JDEP, THROUGH_EXCESS, THROUGH_LO = 0.30, 0.20, 0.10
CONFIRM_LOOKUP_EXCESS, CONFIRM_RECALL_JDEP = 0.10, 0.30
KILL_LOOKUP_EXCESS, KILL_RECALL_JDEP = 0.20, 0.20
H_TOKEN_EXCESS = 0.20
PREDICTED = {"qwen3.6-27b": 32, "qwen3.5-9b": 12, "qwen3.5-122b-a10b": 33}


# ---- cells (CPU) --------------------------------------------------------------------------------------------------


def resampled_rates(
    switched: dict[str, list[int]], entities: list[str], n_boot: int = N_BOOT, seed: int = BOOT_SEED
) -> dict[str, np.ndarray]:
    """Per arm, the switched share in each cluster-bootstrap resample [n_boot]: whole entities drawn with replacement,
    the same draws for every arm (so ratios of arms are paired)."""
    keys = sorted(set(entities))
    index = {e: i for i, e in enumerate(keys)}
    ent = np.array([index[e] for e in entities])
    counts = np.bincount(ent, minlength=len(keys)).astype(float)
    pick = np.random.default_rng(seed).integers(0, len(keys), size=(n_boot, len(keys)))
    n_r = counts[pick].sum(1)
    out = {}
    for arm, s in switched.items():
        assert len(s) == len(entities), f"{arm}: {len(s)} outcomes for {len(entities)} items"
        sums = np.bincount(ent, weights=np.asarray(s, dtype=float), minlength=len(keys))
        out[arm] = sums[pick].sum(1) / n_r
    return out


def dependence(s_whole: float | np.ndarray, s_removed: float | np.ndarray) -> np.ndarray:
    """1 - S_removed / S_whole (nan where nothing switched with the whole edit); a 0-d array for scalars."""
    whole = np.asarray(s_whole, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return 1.0 - np.asarray(s_removed, dtype=float) / np.where(whole > 0, whole, np.nan)


def interval(x: np.ndarray) -> tuple[float, float]:
    lo, hi = np.nanpercentile(x, [2.5, 97.5])
    return float(lo), float(hi)


def cell(switched: dict[str, list[int]], entities: list[str], n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """One cell's numbers from per-item 0/1 outcomes of the three arms (whole, no_part, no_rand), with its label."""
    assert set(switched) == set(ARMS), f"arms {sorted(switched)}"
    n = len(entities)
    hits = {a: int(sum(switched[a])) for a in ARMS}
    s = {a: hits[a] / n for a in ARMS}
    r = resampled_rates(switched, entities, n_boot, seed)
    jdep_r, rdep_r = dependence(r["whole"], r["no_part"]), dependence(r["whole"], r["no_rand"])
    jdep, rdep = float(dependence(s["whole"], s["no_part"])), float(dependence(s["whole"], s["no_rand"]))
    out = {
        "n": n,
        "entities": len(set(entities)),
        **{f"S_{a}": [round(v, 4) for v in wilson(hits[a], n)] for a in ARMS},
        "switched_whole": hits["whole"],
        "valid": s["whole"] >= VALID_S and hits["whole"] >= VALID_N,
        "Jdep": [jdep, *interval(jdep_r)],
        "Rdep": [rdep, *interval(rdep_r)],
        "excess": [jdep - rdep, *interval(jdep_r - rdep_r)],
    }
    out["label"] = label(out)
    return out


def label(c: dict) -> str:
    """around / through / mixed (section 2 of the brief); can't tell for an invalid cell."""
    if not c["valid"]:
        return "can't tell"
    ex, ex_lo, ex_hi = c["excess"]
    if ex <= AROUND_EXCESS and ex_hi <= AROUND_HI:
        return "around"
    if c["Jdep"][0] >= THROUGH_JDEP and ex >= THROUGH_EXCESS and ex_lo >= THROUGH_LO:
        return "through"
    return "mixed"


def verdict(lookup: dict, recall: dict) -> str:
    """The 23 Oct rule at the predicted layer (point estimates): confirmed / killed / not confirmed / can't tell."""
    if not (lookup["valid"] and recall["valid"]):
        return "can't tell"
    lk_excess, rc_jdep = lookup["excess"][0], recall["Jdep"][0]
    if lk_excess <= CONFIRM_LOOKUP_EXCESS and rc_jdep >= CONFIRM_RECALL_JDEP:
        return "confirmed"
    if lk_excess >= KILL_LOOKUP_EXCESS or rc_jdep < KILL_RECALL_JDEP:
        return "killed"
    return "not confirmed"


def h_token(jpp_lookup: dict, we_lookup: dict) -> str:
    """H-token at the predicted layer: does W_E removal make the lookup need its part while J++ removal leaves it
    around?"""
    if not (jpp_lookup["valid"] and we_lookup["valid"]):
        return "can't tell"
    if jpp_lookup["label"] != "around":
        return "not applicable (the J++ lookup is not around)"
    if we_lookup["excess"][0] >= H_TOKEN_EXCESS:
        return "token identity: W_E removal costs the lookup, J++ removal does not"
    if we_lookup["label"] == "around":
        return "neither: the lookup is around W_E as well as J++"
    return "mixed"


def split(lookup: dict, recall: dict) -> bool:
    """The split at a layer: the lookup around and the recall through, on the same items."""
    return lookup["label"] == "around" and recall["label"] == "through"


def nan_round(x: float, nd: int = 3) -> float | None:
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(x, nd)


# ---- cases (tokenizer only) ---------------------------------------------------------------------------------------

RENDERINGS = ("chat", "raw", "nochat")  # nochat: amendment 2 (no chat template, thinking off)
EMPTY_THINK = "<think>\n\n</think>\n\n"  # what the template inserts with thinking off, before the 'Answer:' prefill
LAYERS = {"qwen3.6-27b": tuple(range(16, 41, 2)), "qwen3.5-9b": tuple(range(6, 21, 2))}
N_ITEMS, N_MIN, GATE = 200, 150, 0.80
K_EXAMPLES, EXAMPLES_SEED, GEN_TOKENS = 10, 0, 8
RAW_STEPS = 4  # raw read: at most RAW_STEPS - 1 whitespace-only tokens skipped before the read
READ = "first"  # non-chat read: the first non-whitespace token (amendment 1) or "digit" (amendment 3, descriptive)
DESCRIPTIVE = False  # amendment 3: run on the items each reader gets right even if the gate fails (labeled)
DIGIT_IDS: set[int] = set()  # the digit tokens, set by stage_run (the digit read)
ALT = "cf"  # the alt: the generator's cf (two picks swap; X0) or "single" (only the asked pick changes; after data)
CURVE_ALL = False  # the k curve at every layer, not only the predicted one (after data)
Arm = tuple[str, int, str, str]  # (dictionary, k, fit, arm)
WHOLE: Arm = ("-", 0, "-", "whole")
MAIN = ("jpp", K_MAIN, "signed")  # the decisive dictionary, k and fit
EXAMPLE_ARMS: tuple[Arm, ...] = (WHOLE, ("jpp", K_MAIN, "signed", "no_part"), ("jpp", K_MAIN, "signed", "no_rand"))


def render(tok, item: dict, rendering: str, context: str) -> str:
    """chat: tasks_v2's prompt as on 23 Oct (the template, the digit instruction, thinking off, 'Answer:' prefilled);
    raw: no template and no instruction, '<context>\\nQuestion: <q>\\nAnswer:'; nochat: raw with the template's empty
    think block before 'Answer:', no roles and no instruction (jobs/c3/X0.md, amendment 2)."""
    from scripts import tasks_v2 as T

    if rendering == "chat":
        return T.render(tok, {**item, "context": context})
    think = EMPTY_THINK if rendering == "nochat" else ""
    return f"{context}\nQuestion: {item['question']}\n{think}Answer:"


def alt_context(item: dict) -> str:
    """The alt context: the generator's cf (two picks swap), or with ALT == "single" the org context with only the asked
    person's pick changed to the cf bridge, which another person already picks; every other sentence as in org."""
    if ALT == "cf":
        return item["cf_context"]
    from scripts import statement_positions as SP

    sent = SP.tasks_statements(item)["bind_bridge"]
    i = sent.rindex(item["bridge"])
    assert item["context"].count(sent) == 1, f"{item['id']}: the asked pick sentence is not once in the context"
    return item["context"].replace(sent, sent[:i] + item["cf_bridge"] + sent[i + len(item["bridge"]) :])


def encode_bridge(tok, item: dict, rendering: str, alt: bool) -> tuple[list[int], list[int]]:
    """The rendered org (alt) prompt's ids and the token positions of the asked person's bridge word in it."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    context, bridge = (alt_context(item), item["cf_bridge"]) if alt else (item["context"], item["bridge"])
    text = render(tok, item, rendering, context)
    assert text.count(context) == 1, f"{item['id']}: the context is not once in the prompt"
    enc = raw_encoding(tok, text, offsets=True)
    sentence = SP.tasks_statements({**item, "context": context, "bridge": bridge})["bind_bridge"]
    w0 = text.index(context) + SP.find_sentence(context, sentence) + sentence.rindex(bridge)
    return list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(bridge))


def scene_case(tok, pair: dict[str, dict], rendering: str) -> tuple[dict | None, str | None]:
    """One scene in one rendering, both readers, or the reason it is dropped: the bridge one token at the same
    position in org and alt, both readers' prompts identical through it (one Δ for both), distinct answer tokens."""
    from scripts import suite_v1 as S

    readers, pos = {}, None
    for w in READERS:
        it = pair[w]
        ids_org, p_org = encode_bridge(tok, it, rendering, alt=False)
        ids_alt, p_alt = encode_bridge(tok, it, rendering, alt=True)
        if len(p_org) != 1 or p_alt != p_org:
            return None, "the bridge is not one token at one position in org and alt"
        diff = S.changed(ids_org, ids_alt)
        if not diff or p_org[0] not in diff:
            return None, "org and alt do not align at the bridge"
        if pos is not None and p_org[0] != pos:
            return None, "the readers' bridge positions differ"
        pos = p_org[0]
        tok_a, tok_b = (S.answer_token(tok, a, "digit") for a in (it["answer"], it["cf_answer"]))
        if tok_a == tok_b:
            return None, "the org and alt answers share their first token"
        readers[w] = {"id": it["id"], "question": it["question"], "answer": it["answer"], "cf_answer": it["cf_answer"],
                      "ids": {"org": ids_org, "alt": ids_alt}, "tok_A": tok_a, "tok_b": tok_b,
                      "upstream": min(diff) < pos}  # fmt: skip
    assert pos is not None
    for v in ("org", "alt"):
        if readers[LOOKUP]["ids"][v][: pos + 1] != readers[RECALL]["ids"][v][: pos + 1]:
            return None, "the readers' prompts differ before the bridge"
    it = pair[LOOKUP]
    return {"scene": it["scene"], "rendering": rendering, "domain": it["domain"], "bridge": it["bridge"],
            "cf_bridge": it["cf_bridge"], "context": it["context"], "cf_context": alt_context(it), "pos": pos,
            "upstream": readers[LOOKUP]["upstream"], "space": S.ids(tok, " "), "readers": readers}, None  # fmt: skip


def build_cases(tok, set_name: str) -> tuple[list[dict], dict]:
    """Every scene of the set with both readers, in scene order, per rendering; drops counted by reason."""
    from scripts import tasks_v2 as T

    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in T.load(set_name):
        if it["word"] in READERS:
            by_scene[it["scene"]][it["word"]] = it
    cases, dropped = [], collections.Counter()
    for scene in sorted(by_scene):
        pair = by_scene[scene]
        if set(pair) != set(READERS):
            dropped["a reader is missing"] += 1
            continue
        if any(pair[LOOKUP][k] != pair[RECALL][k] for k in ("context", "cf_context", "bridge", "cf_bridge")):
            dropped["the readers' scenes differ"] += 1
            continue
        for r in RENDERINGS:
            c, why = scene_case(tok, pair, r)
            if c is None:
                dropped[f"{r}: {why}"] += 1
            else:
                cases.append(c)
    counts = collections.Counter(c["rendering"] for c in cases)
    return cases, {"scenes": len(by_scene), "cases": dict(counts), "dropped": dict(dropped)}


# ---- GPU ----------------------------------------------------------------------------------------------------------


def digit_ids(tok) -> list[int]:
    from scripts import suite_v1 as S

    return [S.answer_token(tok, str(d), "digit") for d in range(10)]


def first_among(lg, t: int, digits) -> bool:
    """Token t's logit strictly above every other digit token's (the cand read; a tie is not first)."""
    others = lg[digits[digits != t]]
    return bool(lg[t] > others.max())


def read_row(lg, rd: dict, digits) -> dict:
    """The decisive read (the top token is the alt answer's first token), the cand read for alt and org
    (descriptive), the top token's role, p(org), p(alt) and logit(alt) - logit(org)."""
    import torch

    top = int(lg.argmax())
    p = torch.softmax(lg.float(), -1)
    return {"switched": int(top == rd["tok_b"]), "cand_switched": int(first_among(lg, rd["tok_b"], digits)),
            "cand_org_first": int(first_among(lg, rd["tok_A"], digits)),
            "role": "b" if top == rd["tok_b"] else "A" if top == rd["tok_A"] else "other",
            "p_org": round(float(p[rd["tok_A"]]), 4), "p_alt": round(float(p[rd["tok_b"]]), 4),
            "ld": round(float(lg[rd["tok_b"]] - lg[rd["tok_A"]]), 3)}  # fmt: skip


def whitespace_mask(model):
    """[vocab] bool on the home device: the tokens whose decode is whitespace only (special tokens excluded)."""
    import torch

    return torch.tensor([i not in model.special_ids and not s.strip() for i, s in enumerate(model.decoded)],
                        device=model.device)  # fmt: skip


def read_logits(
    model, ids: list[int], edits: list[dict], rendering: str, space: list[int], ws
) -> tuple[Any, list[int]]:
    """The logits [len(edits), vocab] at the read step of one prompt under each edit set, and the whitespace tokens
    skipped per row. chat: one forward with a digit's space token appended (23 Oct). raw: the prompt ends at
    'Answer:' with no trailing space; a row whose top token is whitespace only gets it appended and is read again,
    so the read is the first non-whitespace token of the greedy continuation (at most RAW_STEPS forwards; a row still
    on whitespace then is read there and switches nothing)."""
    import torch

    from scripts import suite_split as P

    def forward(prompts: list[list[int]], row_edits: list[dict]):
        return torch.cat([model.generate_batch(torch.tensor(prompts[s : s + P.BATCH], device=model.device), 1,
                                               row_edits[s : s + P.BATCH], first_logits=True)[1]
                          for s in range(0, len(row_edits), P.BATCH)])  # fmt: skip

    if rendering == "chat":
        return forward([ids + space] * len(edits), edits), [0] * len(edits)
    if READ == "digit":  # amendment 3: the step of the first digit token in GEN_TOKENS greedy tokens (none: step 0)
        rows, skipped_d = [], []
        for s in range(0, len(edits), P.BATCH):
            chunk = edits[s : s + P.BATCH]
            prompt = torch.tensor([ids] * len(chunk), device=model.device)
            _, step_logits, new = model.generate_batch(prompt, GEN_TOKENS, chunk, steps=True)
            for r in range(len(chunk)):
                j = next((i for i, t in enumerate(new[r].tolist()) if t in DIGIT_IDS), None)
                rows.append(step_logits[r, j if j is not None else 0])
                skipped_d.append(j if j is not None else -1)
        return torch.stack(rows), skipped_d
    out: list[Any] = [None] * len(edits)
    skipped = [0] * len(edits)
    prompts = [list(ids) for _ in edits]
    todo = list(range(len(edits)))
    for step in range(RAW_STEPS):
        logits = forward([prompts[i] for i in todo], [edits[i] for i in todo])  # every row in todo: one length
        nxt = []
        for i, lg in zip(todo, logits, strict=True):
            top = int(lg.argmax())
            if bool(ws[top]) and step < RAW_STEPS - 1:
                prompts[i].append(top)
                nxt.append(i)
            else:
                out[i], skipped[i] = lg, step
        todo = nxt
        if not todo:
            break
    return torch.stack(out), skipped


def competence(model, cases: list[dict], digits, ws) -> list[dict]:
    """Unedited org and alt prompts of both readers: 8 greedy tokens (what the model says), the decisive read and the
    cand read."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import suite_v1 as S

    rows = []
    with torch.no_grad():
        for c in progress(cases, "competence (case)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device="cuda")
                texts = model.generate_batch(ids, GEN_TOKENS, [{}, {}])
                for i, (v, gold, tok_gold) in enumerate(
                    (("org", rd["answer"], rd["tok_A"]), ("alt", rd["cf_answer"], rd["tok_b"]))
                ):
                    logits, skipped = read_logits(model, rd["ids"][v], [{}], c["rendering"], c["space"], ws)
                    said = S.said(texts[i], "digit")
                    rows.append({"scene": c["scene"], "rendering": c["rendering"], "reader": w, "variant": v,
                                 "greedy": texts[i], "said": said, "right": said == gold,
                                 "read_right": int(logits[0].argmax()) == tok_gold, "ws_skipped": skipped[0],
                                 "cand_right": first_among(logits[0], tok_gold, digits)})  # fmt: skip
    return rows


def org_rate(right: dict[tuple, dict], cases: list[dict], rend: str, key: str) -> dict[str, float]:
    """Per reader, the share of the cases' unedited org prompts with `key` true ({} when there are no cases)."""
    if not cases:
        return {}
    return {w: round(statistics.mean(right[(c["scene"], rend, w, "org")][key] for c in cases), 4) for w in READERS}


def gate_and_eligible(cases: list[dict], comp: list[dict]) -> tuple[dict, dict[str, list[dict]]]:
    """Per rendering: the gate (unedited org accuracy under the decisive read >= GATE for both readers, all cases; the
    greedy text's and the cand read's accuracy beside it) and the eligible cases (org and alt said right and right
    under the decisive read, both readers), the first N_ITEMS in scene order."""
    right = {(r["scene"], r["rendering"], r["reader"], r["variant"]): r for r in comp}
    gate, eligible = {}, {}
    for rend in RENDERINGS:
        mine = [c for c in cases if c["rendering"] == rend]  # empty for a rendering not run
        acc = org_rate(right, mine, rend, "read_right")
        ok = [c for c in mine
              if all(right[(c["scene"], rend, w, v)]["right"] and right[(c["scene"], rend, w, v)]["read_right"]
                     for w in READERS for v in ("org", "alt"))]  # fmt: skip
        gate[rend] = {"cases": len(mine), "org_accuracy": acc, "said_accuracy": org_rate(right, mine, rend, "right"),
                      "cand_accuracy": org_rate(right, mine, rend, "cand_right"),
                      "pass": bool(acc) and all(a >= GATE for a in acc.values()),
                      "eligible": len(ok), "enough": len(ok) >= N_MIN}  # fmt: skip
        gate[rend]["descriptive"] = DESCRIPTIVE
        eligible[rend] = ok[:N_ITEMS] if DESCRIPTIVE or (gate[rend]["pass"] and gate[rend]["enough"]) else []
    return gate, eligible


def dictionary(name: str, layer: int, model, lens, letters):
    """[letters, d] unit atoms on the GPU: J++ (the lens's vectors at the layer), W_U (the same with J = identity),
    W_E (input embeddings), or Gaussian rows drawn on the CPU (seed RAND_DICT_SEED + layer)."""
    import torch

    norm = torch.nn.functional.normalize
    if name == "jpp":
        return lens.vectors(layer, letters)
    if name == "wu":
        return norm(model.hf.lm_head.weight[letters].float() * model.norm_gain(), dim=-1)
    if name == "we":
        return norm(model.hf.get_input_embeddings().weight[letters].float(), dim=-1)
    assert name == "rand", name
    g = torch.Generator().manual_seed(RAND_DICT_SEED + layer)
    d = model.hf.lm_head.weight.shape[1]
    return norm(torch.randn((len(letters), d), generator=g), dim=-1).to("cuda")


def fit(dic, x, k: int, omp: str):
    """The k-atom OMP part of each row of x [n, d] over dic: signed (as on 23 Oct) or non-negative."""
    import torch

    from bridge_jspace.omp import nonneg_omp
    from scripts.exp04_brew_parts import signed_omp

    if omp == "signed":
        return signed_omp(dic, x, k)
    out = torch.zeros_like(x, dtype=torch.float32)
    for r in range(x.shape[0]):
        idx, coefs = nonneg_omp(dic, x[r], k)
        if len(idx):
            out[r] = coefs.to(dic.device) @ dic[idx.to(dic.device)]
    return out


def run_rendering(model, lens, cases: list[dict], layers: tuple[int, ...], predicted: int, out: Path, ws) -> None:
    """Δ at the bridge's word (every layer, one forward per prompt), its parts per dictionary (one batched fit per
    layer and dictionary), then every arm read by both readers; outcomes, shares and examples appended to out/."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    tok = model.tokenizer
    digits = torch.tensor(digit_ids(tok), device="cuda")
    letters = model.letter_token_ids()
    rend = cases[0]["rendering"]
    with torch.no_grad():
        deltas = []
        for c in progress(cases, f"{rend}: Δ at the bridge's word (case)"):
            ids = c["readers"][LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=tuple(layers))[1] for v in ("org", "alt")}
            deltas.append(torch.stack([(h["alt"][la][c["pos"]] - h["org"][la][c["pos"]]).cpu() for la in layers]))
        delta = torch.stack(deltas)  # [n, layers, d] fp32, CPU
        examples = set(random.Random(EXAMPLES_SEED).sample(range(len(cases)), min(K_EXAMPLES, len(cases))))
        for li, la in enumerate(layers):
            x = delta[:, li].to("cuda")
            arms: dict[Arm, Any] = {WHOLE: x}
            specs = [(name, K_MAIN, "signed") for name in DICTS]
            if la == predicted or CURVE_ALL:
                specs += [(name, k, "signed") for name in CURVE_DICTS for k in K_CURVE] + [("jpp", K_MAIN, "nonneg")]
            basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(SUBSPACE_SEED + la)).to("cuda")
            shares = []
            for name in dict.fromkeys(s[0] for s in specs):
                dic = dictionary(name, la, model, lens, letters)
                for _, k, omp in (s for s in specs if s[0] == name):
                    part = fit(dic, x, k, omp)
                    share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                    rand = SP.random_subspace_part(x, share, basis)
                    arms[(name, k, omp, "no_part")] = x - part
                    arms[(name, k, omp, "no_rand")] = x - rand
                    rshare = rand.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
                    shares += [{"scene": c["scene"], "rendering": rend, "layer": la, "dict": name, "k": k, "omp": omp,
                                "share": round(float(share[i]), 5), "rand_share": round(float(rshare[i]), 5)}
                               for i, c in enumerate(cases)]  # fmt: skip
                del dic
                torch.cuda.empty_cache()
            keys = list(arms)
            rows, ex_rows = [], []
            for i, c in enumerate(progress(cases, f"{rend}: reads at layer {la} (case)")):
                for w, rd in c["readers"].items():
                    edits = [{}] + [{la: AddRows(arms[key][i : i + 1], [c["pos"]])} for key in keys]
                    logits, skipped = read_logits(model, rd["ids"]["org"], edits, rend, c["space"], ws)
                    base = {"scene": c["scene"], "domain": c["domain"], "entity": c["bridge"], "rendering": rend,
                            "layer": la, "reader": w, "upstream": c["upstream"]}  # fmt: skip
                    for key, lg, sk in zip([("-", 0, "-", "none"), *keys], logits, skipped, strict=True):
                        d_, k_, omp_, arm = key
                        rows.append({**base, "dict": d_, "k": k_, "omp": omp_, "arm": arm, "ws_skipped": sk,
                                     **read_row(lg, rd, digits)})  # fmt: skip
                    if i in examples:
                        gen = torch.tensor([rd["ids"]["org"]], device="cuda")
                        texts = model.generate_batch(gen, GEN_TOKENS, [edits[1 + keys.index(a)] for a in EXAMPLE_ARMS])
                        ex_rows += [{**base, "arm": "/".join(map(str, a)), "greedy": t}
                                    for a, t in zip(EXAMPLE_ARMS, texts, strict=True)]  # fmt: skip
            for fname, part_rows in (("outcomes.jsonl", rows), ("shares.jsonl", shares), ("examples.jsonl", ex_rows)):
                with (out / fname).open("a") as f:
                    f.writelines(json.dumps(r) + "\n" for r in part_rows)


def lens_record() -> dict:
    """The main arm's lens as every manifest and report records it; asserts it is the target's pinned J++."""
    assert pins.FROZEN_LENS == "jpp", f"{pins.TARGET}: the frozen lens is {pins.FROZEN_LENS!r}, not J++"
    source = pins.LENS_SOURCES["jpp"]
    return {"name": "jpp", "source": list(source), "sha256": pins.FROZEN_LENS_SHA256}


def stage_run(
    name: str, why: str, set_name: str, layers: tuple[int, ...], predicted: int, renderings: list[str]
) -> Path:
    from bridge_jspace import chat
    from bridge_jspace.utils import git_state

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "X0 renders its raw prompts itself: run with BJ_FORMAT unset"
    assert predicted in layers, f"the predicted layer {predicted} is not in {layers}"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items = pins.DATA_DIR / "tasks_v2" / set_name / "items.jsonl"
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "lens": lens_record(), "set": set_name,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in (items, SPEC)},
         "layers": list(layers), "predicted": predicted, "renderings": renderings, "dicts": list(DICTS), "k": K_MAIN,
         "k_curve": {"dicts": list(CURVE_DICTS), "k": list(K_CURVE)}, "n": {"items": N_ITEMS, "min": N_MIN},
         "gate": GATE, "position": "bridge_word (the asked person's pick, one token)",
         "read": {"decisive": "the top token over the vocabulary is the alt answer's first token (Dan, 24 Oct)",
                  "chat": "one forward of the prompt with a digit's space token appended (23 Oct)",
                  "raw": f"the first non-whitespace token of the greedy continuation of the prompt ending 'Answer:' "
                         f"(no trailing space; at most {RAW_STEPS} forwards)",
                  "cand": "the alt answer's first token ranks first among the digit tokens (descriptive)",
                  "mode": READ, "digit": f"amendment 3: the step of the first digit token in {GEN_TOKENS} greedy tokens "
                                         "(non-chat renderings, when mode is digit)"},
         "descriptive": DESCRIPTIVE, "alt": ALT, "curve_all_layers": CURVE_ALL,
         "seeds": {"random_dictionary": f"{RAND_DICT_SEED} + layer (CPU)", "random_subspace": f"{SUBSPACE_SEED} + layer (CPU)",
                   "bootstrap": BOOT_SEED, "examples": EXAMPLES_SEED},
         "design": "jobs/c3/X0.md"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    model = load_model()
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    cases, counts = build_cases(model.tokenizer, set_name)
    cases = [c for c in cases if c["rendering"] in renderings]
    import torch

    ws = whitespace_mask(model)
    DIGIT_IDS.update(digit_ids(model.tokenizer))
    comp = competence(model, cases, torch.tensor(digit_ids(model.tokenizer), device="cuda"), ws)
    gate, eligible = gate_and_eligible(cases, comp)
    write_jsonl(out / "competence.jsonl", comp)
    write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    (out / "gate.json").write_text(json.dumps({"counts": counts, "gate": gate}, indent=2) + "\n")
    print(json.dumps(gate, indent=2), flush=True)
    for rend in renderings:
        if eligible[rend]:
            run_rendering(model, lens, eligible[rend], layers, predicted, out, ws)
    return out


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


# ---- verdict and figures (CPU) ------------------------------------------------------------------------------------


def cells_of(rows: list[dict], n_boot: int = N_BOOT) -> dict[tuple, dict]:
    """Every cell (rendering, layer, reader, dict, k, omp) from the outcome rows."""
    by: dict[tuple, dict[str, dict[str, int]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    whole: dict[tuple, dict[str, int]] = collections.defaultdict(dict)
    entity: dict[str, str] = {}
    for r in rows:
        entity[r["scene"]] = r["entity"]
        at = (r["rendering"], r["layer"], r["reader"])
        if r["arm"] == "whole":
            whole[at][r["scene"]] = r["switched"]
        elif r["arm"] in ("no_part", "no_rand"):
            by[(*at, r["dict"], r["k"], r["omp"])][r["arm"]][r["scene"]] = r["switched"]
    cells = {}
    for key, arms in by.items():
        scenes = sorted(whole[key[:3]])
        assert all(sorted(arms[a]) == scenes for a in ("no_part", "no_rand")), f"{key}: arms on different items"
        sw = {"whole": [whole[key[:3]][s] for s in scenes], **{a: [arms[a][s] for s in scenes] for a in arms}}
        cells[key] = cell(sw, [entity[s] for s in scenes], n_boot)
    return cells


def verdict_of(cells: dict[tuple, dict], predicted: int, renderings: tuple[str, ...] = RENDERINGS) -> dict:
    """The rule, H-token and the split per layer, per rendering of the run, J++ (main)."""
    at = lambda rend, la, w, d=MAIN: cells.get((rend, la, w, *d))  # noqa: E731
    out: dict[str, Any] = {"predicted": predicted}
    for rend in renderings:
        lk, rc = at(rend, predicted, LOOKUP), at(rend, predicted, RECALL)
        if lk is None or rc is None:
            out[rend] = {"verdict": "can't test (no rows)"}
            continue
        we = at(rend, predicted, LOOKUP, ("we", K_MAIN, "signed"))
        splits = []
        for la in sorted({k[1] for k in cells if k[0] == rend}):
            lk_la, rc_la = at(rend, la, LOOKUP), at(rend, la, RECALL)
            if lk_la is not None and rc_la is not None and split(lk_la, rc_la):
                splits.append(la)
        out[rend] = {"verdict": verdict(lk, rc), "lookup_label": lk["label"], "recall_label": rc["label"],
                     "h_token": h_token(lk, we) if we else "no W_E rows", "split_layers": splits}  # fmt: skip
    return out


def fmt3(v: list) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def write_verdict(run: str, n_boot: int = N_BOOT) -> Path:
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    rows = read_jsonl(src / "outcomes.jsonl")
    gate = json.loads((src / "gate.json").read_text())
    rends = tuple(m.get("renderings", RENDERINGS))
    gate["gate"] = {r: g for r, g in gate["gate"].items() if r in rends}
    cells = cells_of(rows, n_boot)
    v = verdict_of(cells, m["predicted"], rends)
    upstream_free = cells_of([r for r in rows if not r["upstream"]], n_boot) if rows else {}
    v["asked_first_subset"] = verdict_of(upstream_free, m["predicted"], rends) if upstream_free else None
    agree = [r["switched"] == r["cand_switched"] for r in rows if r["arm"] == "whole"]
    v["reads_agree_on_whole"] = round(statistics.mean(agree), 4) if agree else None
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": run, "lens": m["lens"], "model": m["model"], "gate": gate, "verdict": v,
            "cells": [{"rendering": k[0], "layer": k[1], "reader": k[2], "dict": k[3], "k": k[4], "omp": k[5], **c}
                      for k, c in sorted(cells.items())]}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=2) + "\n")
    lens = m["lens"]
    lines = [f"# X0 verdict: {run}", "",
             f"Model {m['model']['target']} ({m['model']['revision'][:8]}); lens J++ `{lens['source'][1]}` sha256 "
             f"{lens['sha256'][:16]}; set {m['set']}; predicted layer {m['predicted']}; non-chat read "
             f"{m.get('read', {}).get('mode', 'first')}; UNVERIFIED.", "",
             *(["DESCRIPTIVE (amendment 3, after data): run on the items each reader gets right whether or not the "
                "gate passed; not part of the X0 rule.", ""] if m.get("descriptive") else []),
             "Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): " + "; ".join(
                 f"{r}: {g['org_accuracy']} (greedy text {g.get('said_accuracy')}, cand {g.get('cand_accuracy')}) "
                 f"pass={g['pass']}, eligible {g['eligible']}"
                 for r, g in gate["gate"].items()), ""]  # fmt: skip
    for rend in rends:
        if rend not in v or "split_layers" not in v[rend]:
            lines += [f"## {rend}: {v.get(rend, {}).get('verdict', 'not run')}", ""]
            continue
        r = v[rend]
        lines += [f"## {rend}: {r['verdict'].upper()} at layer {m['predicted']} (lookup {r['lookup_label']}, recall "
                  f"{r['recall_label']}); H-token: {r['h_token']}; split at layers {r['split_layers']}", "",
                  "S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct);"
                  " S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).", "",
                  "| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | "
                  "label |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for (rr, la, w, *d), c in sorted(cells.items()):
            if rr == rend and tuple(d) == MAIN:
                null = cells.get((rr, la, w, "rand", K_MAIN, "signed"))
                s_null = f"{null['S_no_part'][0]:.2f}" if null else "-"
                lines.append(f"| {la} | {w} | {c['n']} | {c['S_whole'][0]:.2f} | {c['S_no_part'][0]:.2f} | "
                             f"{c['S_no_rand'][0]:.2f} | {s_null} | {fmt3(c['Jdep'])} | {fmt3(c['Rdep'])} | "
                             f"{fmt3(c['excess'])} | {median_share(src, rend, la, MAIN)} | {c['label']} |")  # fmt: skip
        lines += [
            "",
            f"Dictionaries at layer {m['predicted']}:",
            "",
            "Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².",
            "",
            "| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for (rr, la, w, *d), c in sorted(cells.items()):
            if rr == rend and la == m["predicted"]:
                lines.append(f"| {d[0]} | {d[1]} | {d[2]} | {w} | {median_share(src, rend, la, tuple(d))} | "
                             f"{fmt3(c['Jdep'])} | {fmt3(c['Rdep'])} | {fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
        lines.append("")
    lines += [f"Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on "
              f"the whole edit: {v['reads_agree_on_whole']}.",
              f"Asked-first subset (descriptive): {json.dumps(v['asked_first_subset'])}"]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def median_share(src: Path, rend: str, layer: int, d: tuple) -> str:
    vals = [r["share"] for r in read_jsonl(src / "shares.jsonl")
            if r["rendering"] == rend and r["layer"] == layer and (r["dict"], r["k"], r["omp"]) == d]  # fmt: skip
    return f"{statistics.median(vals):.3f}" if vals else "-"


def figures(verdict_dir: Path) -> list[Path]:
    """Per rendering: Jdep and Rdep by layer for both readers (J++, CIs), and the excess per dictionary at the
    predicted layer; written into a new analysis-*-figures/ folder beside the verdict."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    blob = json.loads((verdict_dir / "verdict.json").read_text())
    pred = blob["verdict"]["predicted"]
    cells = blob["cells"]
    folder = verdict_dir / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-figures"
    folder.mkdir()
    made = []
    color = {LOOKUP: F.LOOKUP, RECALL: F.RECALL}
    CAPTION = F.CAPTION_INK
    for rend in RENDERINGS:
        mine = [c for c in cells if c["rendering"] == rend]
        if not mine:
            continue
        fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [2, 1]})
        for w in READERS:
            cs = sorted((c for c in mine if c["reader"] == w and (c["dict"], c["k"], c["omp"]) == MAIN),
                        key=lambda c: c["layer"])  # fmt: skip
            xs = [c["layer"] for c in cs]
            for what, style in (("Jdep", "-"), ("Rdep", ":")):
                y = [c[what][0] for c in cs]
                ax.plot(xs, y, style, color=color[w], marker="o" if what == "Jdep" else None,
                        label=f"{'lookup' if w == LOOKUP else 'recall'} {what}")  # fmt: skip
                if what == "Jdep":
                    ax.fill_between(xs, [c[what][1] for c in cs], [c[what][2] for c in cs], color=color[w], alpha=0.15)
            for c in cs:
                if not c["valid"]:
                    ax.plot(c["layer"], c["Jdep"][0], "x", color="red", ms=9)
        ax.axvline(pred, color=F.CONTROL, lw=1)
        ax.text(pred, 1.07, " predicted layer", fontsize=8, color=CAPTION, va="top")
        ax.axhline(0, color="black", lw=0.5)
        ax.set_xticks(sorted({c["layer"] for c in mine}))
        ax.set(
            xlabel="layer (patch at the bridge's word)",
            ylabel="share of switches lost",
            ylim=(-0.3, 1.1),
            title=f"{rend}: without J++ (solid) vs without a random part of its share (dotted); x = invalid cell",
        )
        ax.legend(fontsize=8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.14), frameon=False)
        at = [c for c in mine if c["layer"] == pred]
        labels = sorted({(c["dict"], c["k"], c["omp"]) for c in at})
        for j, w in enumerate(READERS):
            vals = [
                next((c for c in at if c["reader"] == w and (c["dict"], c["k"], c["omp"]) == d), None) for d in labels
            ]
            ys = [c["excess"][0] if c else math.nan for c in vals]
            err = [[c["excess"][0] - c["excess"][1] if c else 0 for c in vals],
                   [c["excess"][2] - c["excess"][0] if c else 0 for c in vals]]  # fmt: skip
            bx.errorbar(ys, [i + (0.18 if j else -0.18) for i in range(len(labels))], xerr=err, fmt="o", color=color[w],
                        label="lookup" if w == LOOKUP else "recall")  # fmt: skip
        bx.set_yticks(range(len(labels)), [f"{d} k={k}{'' if o == 'signed' else ' nn'}" for d, k, o in labels])
        bx.axvline(0, color="black", lw=0.5)
        for xv, what in ((AROUND_EXCESS, "around ≤"), (THROUGH_EXCESS, "through ≥")):
            bx.axvline(xv, color=F.CONTROL, lw=0.8, ls="--")
            bx.text(xv, -0.45, f" {what} {xv:.2f}", fontsize=7, color=CAPTION, rotation=90, va="bottom")
        bx.set(xlabel=f"excess = Jdep - Rdep at layer {pred}", title="by dictionary (nn = non-negative OMP)")
        bx.legend(fontsize=8, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.14), frameon=False)
        fig.suptitle(f"X0 {blob['run']} ({blob['model']['target']}): verdict {blob['verdict'][rend]['verdict']} "
                     f"(UNVERIFIED)", fontsize=11)  # fmt: skip
        fig.tight_layout()
        path = folder / f"x0_{rend}.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        made.append(path)
    print("\n".join(map(str, made)))
    return made


def main() -> None:
    global CURVE_DICTS, K_CURVE, READ, DESCRIPTIVE, ALT, CURVE_ALL  # from the command line; the manifest records them
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "figures"])
    ap.add_argument("--name", required=True, help="run name (results/x0_necessity/<name>/)")
    ap.add_argument("--why", default="")
    ap.add_argument("--set", default="d1_topics_v3")
    ap.add_argument("--renderings", nargs="+", default=list(RENDERINGS), choices=list(RENDERINGS))
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--curve-dicts", nargs="+", default=list(CURVE_DICTS), choices=list(DICTS),
                    help="run: dictionaries of the k curve at the predicted layer")  # fmt: skip
    ap.add_argument("--curve-k", nargs="+", type=int, default=list(K_CURVE), help="run: the k curve's atom counts")
    ap.add_argument("--read", choices=("first", "digit"), default=READ,
                    help="run, non-chat renderings: first non-whitespace token, or the first digit token (amendment 3)")  # fmt: skip
    ap.add_argument("--alt", choices=("cf", "single"), default=ALT,
                    help="run: the generator's cf (X0), or only the asked person's pick changed (after data)")  # fmt: skip
    ap.add_argument("--curve-all-layers", action="store_true", help="run: the k curve at every layer")
    ap.add_argument("--descriptive", action="store_true",
                    help="run: amendment 3, run on the items right even if the gate fails (labeled descriptive)")  # fmt: skip
    a = ap.parse_args()
    CURVE_DICTS, K_CURVE = tuple(a.curve_dicts), tuple(a.curve_k)
    READ, DESCRIPTIVE, ALT, CURVE_ALL = a.read, a.descriptive, a.alt, a.curve_all_layers
    if a.stage == "plan":  # tokenizer only
        from scripts import statement_positions as SP

        _, counts = build_cases(SP.load_tokenizer(), a.set)
        print(json.dumps(counts, indent=2))
    elif a.stage == "run":
        layers = tuple(a.layers) if a.layers else LAYERS[pins.TARGET]
        stage_run(a.name, a.why, a.set, layers, PREDICTED[pins.TARGET], a.renderings)
        figures(write_verdict(a.name, a.n_boot))
    elif a.stage == "verdict":
        write_verdict(a.name, a.n_boot)
    else:
        newest = sorted((RESULTS / a.name).glob("verdict-*"))[-1]
        figures(newest)


if __name__ == "__main__":
    main()
