"""early_push (D4): on Qwen3.6-27B, is a hard early lens push the same as editing the input word?

read_write layers_v1 (EXPERIMENTS row 52): at layers 16-28, where copying C's question-token residual does nothing (0%
flips), lens pushes v_X - v_I at 8-16x the copy's norm flip RL 35-61%, RR 46-78% and BL 24-44%, though the lens barely
reads BL's bridge there. Two readings:
  H-inject  the push acts like putting X's word into the question (an input edit); the early 'RL is writable' result
            then does not contradict C2 (the lens cannot write a lookup-used bridge where the model carries it)
  H-write   the push writes the intermediate variable itself, early; then RL is writable and C2 is wrong as stated

Items: suite_split map_A8_v1's cases (BL, BR, RL, RR on the same scenes, the first n per family in the map's order;
layers_v1 used the first 80) and control_split map_v1's countries R, B (a bridge the lens reads and writes at 44-52).
Read: suite_split's (one forward, a digit's space appended; top token's role, ld = logit(b) - logit(A), frac).

Position subsets of the clean prompt (the question region = the question sentence and the instruction):
  r   read_write's own: suite_split's question group (after C's changed tokens: for R* items after the cue), per-position
      norms s x C's copy delta there (layers_v1's push exactly: the replication anchor)
  a   the question region and the chat template after it (= r's positions for B* items)
  b   the subject phrase ("Peter's pet", "the animal known for clucking", "the country where Lyon is located")
  nb  a minus b;   d  the template after the user turn (<|im_end|> ... Answer:)
  a, b, nb, d get one per-token norm: s x the scene's reference, the RMS of C's copy delta over r pooled over the
  scene's families at that layer (BL and RL on one scene get the same physical push).
Conditions per item:
  push   lens v_X - v_I (unit J++ vectors at that layer) at each layer of L and all at once ('band'), scales S, each subset;
         a random direction at the same per-position norms for every one
  embed  at the input embedding (the 'edit the input word' limit): s_e x (e_X - e_I) and s_e x e_X at b; random controls
  copy   C's residual copied at r at L (the 0% anchor) and at the write layers (the graded 'write' reference W-copy*)
  edits  text edits, then a normal forward: E-name (subject phrase -> 'the X': 'Which locker belongs to the sheep?' in
         BL and RL alike), E-insert (', the X' after the subject phrase), E-head (head noun -> X: "Peter's sheep", 'the
         sheep known for clucking'; animals only), E-cue (the C prompt), E-unrelated (an unrelated sentence naming X at
         the end of the context)
  O      the off-path prompt under the lens push at a (collateral: O keeps its answer, follows X in O's context, other)
  text   next-token loss on removal_textloss's WikiText rows, the push at every position from 4 (a stress version)
Measures: answer read over the candidates (A, b = X's answer, other in-context answers); flips, frac; per-item flip
agreement (Cohen's kappa, Jaccard, item bootstrap); full-vocabulary JS divergence at the answer position, push vs each
edit; downstream deltas (push - clean vs edit - clean) at the down layers: cosine per position over the final positions
shared by every edit (text edits shift what precedes them, so only the common token suffix is compared, aligned by
being last), with the pushed vectors projected out of both deltas (they persist in the residual stream); at the transit
layers the projection of that delta on C's copy delta (final positions and r).
Decision rule (fixed before the 27B run; RL is the family in question, BL the comparison):
  P*  the lens push at a whose RL flip rate is nearest 50% over L+band x S (ties: lower scale, earlier layer);
      W-copy* per family the write-layer copy nearest 50%; emb* the embedding push nearest 50% on RL
  K1  dk = kappa(P*, E-insert) - kappa(P*, W-copy*), item bootstrap 95% CI: inject-like above 0, write-like below 0
      (E-name and E-cue flip ~every eligible item, so they cannot carry a per-item test; reported)
  K2  at P*'s layer and scale: inject-like if flips(nb) - flips(a)/2 has its CI above 0; write-like if that CI is below
      0 and flips(b) - flips(nb) has its CI above 0
  K3  flips(BL) - flips(RL) at P* (same scenes, same per-token norm): inject-like if the CI's lower bound is above
      -0.15, write-like if its upper bound is below -0.15
  verdict  'like an input-word edit' if >= 2 of K1-K3 inject-like and none write-like; 'writes the intermediate' if >= 2
      write-like and none inject-like; otherwise mixed. Gate: K1 counts only if kappa(emb*, E-insert) -
      kappa(emb*, W-copy*) has its CI above 0 on RL (the measure calls an input edit by construction inject-like)
  secondary  K4 cos(P*_b, E-name) - cos(P*_b, E-cue) at the final positions below the answer onset (P*_b: subset b at
      P*'s layer and scale, so the final positions are not pushed); K5 transit projection of P*_b vs E-name's
Predictions: H-inject dk > 0, flips(nb) >= flips(a)/2, BL within 15 points of RL, K4 > 0. H-write dk < 0, b >> nb,
BL < RL - 15 points, K4 < 0.

Stages:  run --name N --why W [--n ...]  (manifest.json first, then the run)   analyze --name N   examples --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.plotting import TERM as PLOT_TERM
from bridge_jspace.run_switches import switches
from bridge_jspace.stats import wilson
from bridge_jspace.tokens import raw_encoding
from scripts import control_split as CS
from scripts import exp09_bind_recall as E
from scripts import read_write as RW
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp04_brew_parts import AddRows, null_rows

EXP = "early_push"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {
    "n": 100, "families": ["BL", "BR", "RL", "RR"], "countries": True, "map": "map_A8_v1", "country_map": "map_v1",
    "wording": "A", "layers": [16, 20, 24, 28], "scales": [4.0, 8.0, 16.0], "embed_scales": [1.0, 4.0],
    "write_layers": [32, 36, 40, 44, 48], "down": [32, 40, 48, 56], "transit": [44, 48, 52], "textloss_pairs": 4,
}  # fmt: skip
SUBSETS = ("r", "a", "b", "nb", "d")
STATE_SUBSETS = ("a", "b")
EDITS = ("E-name", "E-insert", "E-head", "E-cue", "E-unrelated")
SUBJECT = {"A": {"B": "{p}'s pet", "R": "the animal known for {cue}"},
           "B": {"B": "the animal that {p} owns", "R": "the animal famous for {cue}"}}  # fmt: skip
COUNTRY_SUBJECT = {"R": "the country where {cue} is located", "B": "the country where {cue} lives"}
UNRELATED = {"animal": "Someone drew a picture of a {x}.", "country": "Someone read a book about {x}."}
NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 0, 2000, 0
EQUIV = 0.15  # K3's margin: BL 'moved about as much as RL' within 15 points
BATCH = P.BATCH


# ---- pure helpers (tested in tests/test_early_push.py) ---------------------------------------------------------------


def overlapping(offsets: list, start: int, end: int) -> list[int]:
    return [i for i, (s, e) in enumerate(offsets) if e > start and s < end]


def position_subsets(offsets: list, q0: int, s0: int, s1: int, c_end: int, rw: list[int]) -> dict[str, list[int]]:
    """Token sets of the clean prompt: q0 = the question's first char, [s0, s1) the subject phrase, c_end the end of
    the user content (after the instruction); rw = suite_split's question group."""
    qreg = overlapping(offsets, q0, c_end)
    subj = overlapping(offsets, s0, s1)
    tmpl = [i for i, (s, _) in enumerate(offsets) if s >= c_end]
    a = sorted(set(qreg) | set(tmpl))
    return {"r": list(rw), "a": a, "b": subj, "nb": sorted(set(a) - set(subj)), "d": tmpl, "qreg": qreg}


def head_swap(subject: str, x: str) -> str | None:
    m = re.search(r"\b(pet|animal)\b", subject)
    return None if m is None else subject[: m.start()] + x + subject[m.end() :]


def edit_contents(
    content: str, question: str, subject: str, x_name: str, unrelated: str, head: str | None
) -> dict[str, str | None]:
    """The user turn under each text edit (E-cue is the C prompt, built elsewhere)."""
    q0 = content.rindex(question)
    s0 = q0 + question.index(subject)
    before, after = content[:s0], content[s0 + len(subject) :]
    closes = after.startswith("?")
    return {
        "E-name": before + x_name + after,
        "E-insert": before + subject + ", " + x_name + ("" if closes else ",") + after,
        "E-head": None if head is None else before + head + after,
        "E-unrelated": content[: q0 - 1] + " " + unrelated + content[q0 - 1 :],
    }


def common_suffix(a: list[int], b: list[int]) -> int:
    k = 0
    while k < min(len(a), len(b)) and a[-1 - k] == b[-1 - k]:
        k += 1
    return k


def char_diff(a: str, b: str) -> tuple[int, int]:
    """The span of b that differs from a (common prefix and suffix removed)."""
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while j < min(len(a), len(b)) - i and a[-1 - j] == b[-1 - j]:
        j += 1
    return i, len(b) - j


def push_rows(direction: torch.Tensor, norms: torch.Tensor) -> torch.Tensor:
    """[P, d]: the unit direction at each position, scaled to that position's norm."""
    return norms[:, None] * torch.nn.functional.normalize(direction, dim=-1)[None, :]


def kappa(a, b) -> float:
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    if a.size == 0 or a.all() or not a.any() or b.all() or not b.any():  # a constant rater: no agreement test
        return float("nan")
    pa, pb = a.mean(), b.mean()
    pe = pa * pb + (1 - pa) * (1 - pb)
    return float("nan") if pe >= 1 - 1e-12 else float(((a == b).mean() - pe) / (1 - pe))


def jaccard(a, b) -> float:
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    union = (a | b).sum()
    return float("nan") if union == 0 else float((a & b).sum() / union)


def boot(fn, arrays: list, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> list[float]:
    """[point, 2.5th, 97.5th]: fn over items resampled with replacement (arrays aligned by item)."""
    arrays = [np.asarray(x, float) for x in arrays]
    n = len(arrays[0]) if arrays else 0
    if n == 0:
        return [math.nan] * 3
    idx = np.random.default_rng(seed).integers(0, n, size=(n_boot, n))
    vals = np.array([fn(*(x[i] for x in arrays)) for i in idx], float)
    if np.isnan(vals).all():
        return [float(fn(*arrays)), math.nan, math.nan]
    return [float(fn(*arrays)), float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))]


def js_divergence(logp: torch.Tensor, logq: torch.Tensor) -> torch.Tensor:
    """JS divergence (nats) between rows of log-probabilities [B, V] and one [V] (or [B, V])."""
    logq = logq.expand_as(logp)
    logm = torch.logaddexp(logp, logq) - math.log(2)
    js = 0.5 * ((logp.exp() * (logp - logm)).sum(-1) + (logq.exp() * (logq - logm)).sum(-1))
    return js.clamp_min(0)


def basis(vectors: torch.Tensor) -> torch.Tensor:
    """[P, k, d] added vectors per position -> [P, d, k] orthonormal basis of their span (QR)."""
    q, _ = torch.linalg.qr(vectors.transpose(1, 2))
    return q


def project_out(x: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
    """x [P, d] minus its projection on each position's basis q [P, d, k]."""
    return x - (q @ (q.transpose(1, 2) @ x.unsqueeze(-1))).squeeze(-1)


def pos_cos(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    den = x.norm(dim=-1) * y.norm(dim=-1)
    out = (x * y).sum(-1) / den.clamp_min(1e-12)
    return torch.where(den > 1e-9, out, torch.full_like(out, float("nan")))


def nanmean(t) -> float | None:
    t = torch.as_tensor(t, dtype=torch.float32)
    t = t[~torch.isnan(t)]
    return round(float(t.mean()), 4) if t.numel() else None


# ---- cases ------------------------------------------------------------------------------------------------------------


def augment(c: dict, tok, wording: str = "A") -> dict:
    """A read_write case (suite or country) with its user turn, subject phrase, position subsets, text edits (prompts
    and read ids) and candidate answer tokens."""
    fam = c["family"]
    if "prompt" in c and fam in ("R", "B"):  # a country item (exp09's chat_prefill rendering)
        question = chat.as_question(chat.split_context(c["prompt"])[1])
        content = chat.question_content(c["prompt"])
        subject = COUNTRY_SUBJECT[fam].format(cue=c["cue"])
        x = c["cf_bridge"]
        x_name, head, unrelated = x, None, UNRELATED["country"].format(x=x)
        cf_text, off_text = tok.decode(c["ids"]["cf"]), tok.decode(c["ids"]["off"])
        others, b_off = [E.CAPITALS[c["third"]]], c["cf_answer"]
    else:
        question = c["question"]
        content = f"{c['context']}\n{question} {S.INSTRUCTION}"
        subject = SUBJECT[wording][fam[0]].format(p=c["cue"], cue=c["cue"])
        x = c["cf_bridge"]
        x_name, head, unrelated = f"the {x}", head_swap(subject, x), UNRELATED["animal"].format(x=x)
        cf_text = S.render(tok, c["cf_context"], c["cf_question"])
        off_text = S.render(tok, c["off_context"], question)
        if fam.endswith("L"):  # a locker lookup: the scene's third locker; O swaps X's and Z's lockers
            others = [str(d) for d in c["lockers"].values() if str(d) not in (c["answer"], c["cf_answer"])]
            b_off = str(c["lockers"][c["third"]])
        else:
            others = [str(k) for k in S.LEG_COUNTS if str(k) not in (c["answer"], c["cf_answer"])]
            b_off = c["cf_answer"]
    assert subject in question, f"{c['id']}: subject {subject!r} not in {question!r}"
    rendered = chat.chat_text(tok, content)
    enc = raw_encoding(tok, rendered, offsets=True)
    assert enc["input_ids"] == c["ids"]["clean"], f"{c['id']}: the user turn does not render to the clean prompt"
    cstart = rendered.index(content)
    q0 = cstart + content.rindex(question)
    s0 = q0 + question.index(subject)
    subsets = position_subsets(enc["offset_mapping"], q0, s0, s0 + len(subject), cstart + len(content),
                               c["groups"]["question"])  # fmt: skip
    edits = edit_contents(content, question, subject, x_name, unrelated, head)
    prompts = {"clean": rendered, **{k: chat.chat_text(tok, v) for k, v in edits.items() if v is not None},
               "E-cue": cf_text, "off": off_text}  # fmt: skip
    ids = {k: list(raw_encoding(tok, p)["input_ids"]) for k, p in prompts.items()}
    assert ids["E-cue"] == c["ids"]["cf"], f"{c['id']}: C text mismatch"
    assert ids["off"] == c["ids"]["off"], f"{c['id']}: O text mismatch"
    space = S.ids(tok, " ") if c["answer_kind"] == "digit" else []
    kind = c["answer_kind"]
    cand = {"A": c["tok_A"], "b": c["tok_b"], "oc": [S.answer_token(tok, o, kind) for o in others],
            "bO": S.answer_token(tok, b_off, kind)}  # fmt: skip
    return {**c, "content": content, "subject": subject, "prompts": prompts, "read": {k: v + space for k, v in ids.items()},
            "read_suffix": tok.decode(space), "subsets": subsets, "offsets": [list(o) for o in enc["offset_mapping"]],
            "subject_span": [s0, s0 + len(subject)], "cand": cand,
            "cand_text": {"A": c["answer"], "b": c["cf_answer"], "oc": others, "bO": b_off}}  # fmt: skip


def build_cases(tok, cfg: dict) -> list[dict]:
    cases = RW.suite_cases(tok, cfg["n"], cfg["map"], cfg["wording"], cfg["families"]) if cfg["families"] else []
    if cfg["countries"]:
        cases += RW.country_cases(tok, cfg["n"], cfg["country_map"])
    return [augment(c, tok, cfg["wording"]) for c in cases]


# ---- model ------------------------------------------------------------------------------------------------------------


@torch.no_grad()
def forward_rows(model, ids: torch.Tensor, edits: list[dict], record: tuple[int, ...] = (), full: bool = False):
    """One batched forward, one row per edit set ({layer: Edit}; layer -1 = the input embedding's output). Returns the
    last position's logits [B, V] fp32 (all positions' with full) and {layer: [B, T, d] fp32} after the edits."""
    from bridge_jspace.model import _forward_hooks

    n = len(edits)
    batch = ids if ids.shape[0] == n else ids.expand(n, -1).contiguous()
    recorded: dict[int, torch.Tensor] = {}

    def hook_for(layer: int):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            edited = any(layer in e for e in edits)
            if edited:
                h = h.clone()
                for row, e in enumerate(edits):
                    if layer in e:
                        h[row] = e[layer](h[row].float()).to(h.dtype)
            if layer in record:
                recorded[layer] = h.float()
            if not edited:
                return None
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    layers = sorted({la for e in edits for la in e} | set(record))
    mods = [(model.text.embed_tokens if la == -1 else model.layers[la], hook_for(la)) for la in layers]
    with _forward_hooks(mods):
        out = model.hf(input_ids=batch, use_cache=False, logits_to_keep=0 if full else 1).logits
    return (out if full else out[:, -1].float()), recorded


def role_of(top: int, cand: dict, off: bool = False) -> str:
    if off:
        for r in ("A", "bO", "b"):
            if top == cand[r]:
                return r
    elif top in (cand["b"], cand["A"]):
        return "b" if top == cand["b"] else "A"
    return "oc" if top in cand["oc"] else "other"


def outcome(model, c: dict, tags: dict, logits: torch.Tensor, js_refs: dict | None) -> dict:
    cand, off = c["cand"], tags.get("prompt") == "off"
    logp = logits.log_softmax(-1)
    p = logp.exp()
    top = int(logits.argmax())
    ld = float(logits[cand["b"]] - logits[cand["A"]])
    o = {"family": c["family"], "name": c["id"], **tags, "role": role_of(top, cand, off),
         "top": model.decoded[top].strip(), "ld": round(ld, 3),
         "p": [round(float(p[cand["A"]]), 4), round(float(p[cand["bO" if off else "b"]]), 4),
               round(float(p[cand["oc"]].sum()) if cand["oc"] else 0.0, 4)]}  # fmt: skip
    if not off:
        o["frac"] = round((ld - c["ld_clean"]) / (c["ld_cf"] - c["ld_clean"]), 4)
    if js_refs:
        o["js"] = {k: round(float(js_divergence(logp[None], q)[0]), 4) for k, q in js_refs.items()}
    return o


def row_basis(edits: dict) -> tuple[torch.Tensor, torch.Tensor] | None:
    """The positions a push edits and an orthonormal basis of what it added there (all its layers share positions)."""
    adds = [e for e in edits.values() if isinstance(e, AddRows)]
    if not adds:
        return None
    pos = adds[0].positions
    assert all(e.positions == pos for e in adds), "a push's layers must share positions"
    vec = torch.stack([e.delta.float() for e in adds], dim=1)  # [P, k, d]
    if float(vec.norm()) < 1e-6:
        return None
    return torch.tensor(pos, device=vec.device), basis(vec)


def perp(x: torch.Tensor, b, lo: int) -> torch.Tensor:
    """x [K, d] over positions lo.. with the push's added directions projected out where it pushed."""
    if b is None:
        return x
    pos, q = b
    keep = (pos >= lo) & (pos < lo + x.shape[0])
    if not bool(keep.any()):
        return x
    x = x.clone()
    idx = pos[keep] - lo
    x[idx] = project_out(x[idx], q[keep])
    return x


def flat_proj(x: torch.Tensor, c: torch.Tensor) -> list[float | None]:
    cc = float((c * c).sum())
    if cc < 1e-12:
        return [None, None]
    dot = float((x * c).sum())
    return [round(dot / cc, 4), round(dot / max(1e-12, float(x.norm() * c.norm())), 4)]


def state_metrics(rec, j, h, hc, info, b, k_min, qreg, rw, cfg) -> dict:
    t = h[cfg["down"][0]].shape[0]
    out: dict[str, Any] = {"cos": {}, "transit": []}
    for e, inf in info.items():
        lo = t - inf["K"]
        qidx = [p - lo for p in qreg if p >= lo]
        cells: dict[str, list] = {"final": [], "final_raw": [], "q": [], "last": []}
        for la in cfg["down"]:
            dp, de = rec[la][j, lo:] - h[la][lo:], inf["delta"][la]
            cells["final_raw"].append(nanmean(pos_cos(dp, de)[-k_min:]))
            cs = pos_cos(perp(dp, b, lo), perp(de, b, lo))
            cells["final"].append(nanmean(cs[-k_min:]))
            cells["q"].append(nanmean(cs[qidx]) if qidx else None)
            cells["last"].append(nanmean(cs[-1:]))
        out["cos"][e] = cells
    for la in cfg["transit"]:
        dp, cd = perp(rec[la][j] - h[la], b, 0), perp(hc[la] - h[la], b, 0)
        out["transit"].append(flat_proj(dp[t - k_min :], cd[t - k_min :]) + flat_proj(dp[rw], cd[rw]))
    return out


@torch.no_grad()
def run_scene(model, lens, scene: list[dict], cfg: dict, case_index: int, out: dict) -> None:
    layers = cfg["layers"]
    state_layers = tuple(sorted(set(cfg["down"]) | set(cfg["transit"])))
    rec_layers = tuple(sorted(set(layers) | set(cfg["write_layers"]) | set(state_layers)))
    base = {}
    for c in scene:
        ids = torch.tensor([c["read"]["clean"], c["read"]["E-cue"]], device="cuda")
        logits, rec = forward_rows(model, ids, [{}, {}], rec_layers)
        c["ld_clean"], c["ld_cf"] = (float(lg[c["cand"]["b"]] - lg[c["cand"]["A"]]) for lg in logits)
        base[c["id"]] = {
            "logits": logits,
            "h": {la: rec[la][0] for la in rec_layers},
            "hc": {la: rec[la][1] for la in rec_layers},
        }
        r = c["subsets"]["r"]
        c["ref_item"] = {la: float((rec[la][1][r] - rec[la][0][r]).norm(dim=-1).pow(2).mean().sqrt()) for la in layers}
    ref = {la: math.sqrt(statistics.mean(c["ref_item"][la] ** 2 for c in scene)) for la in layers}
    for k, c in enumerate(scene):
        run_item(model, lens, c, base[c["id"]], ref, cfg, case_index + k, state_layers, out)


def run_item(model, lens, c, base, ref, cfg, k, state_layers, out) -> None:
    layers, scales, sub = cfg["layers"], cfg["scales"], c["subsets"]
    h, hc = base["h"], base["hc"]
    t = len(c["read"]["clean"])
    pair = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])], device="cuda")
    dirs = {}
    for la in layers:
        v = lens.vectors(la, pair)
        dirs[la] = torch.nn.functional.normalize(v[1] - v[0], dim=-1)
    emb = model.text.embed_tokens(pair).float()
    copy_norms = {la: (hc[la][sub["r"]] - h[la][sub["r"]]).norm(dim=-1) for la in layers}
    resid = {la: float(h[la][sub["a"]].norm(dim=-1).median()) for la in layers}
    # text edits (E-cue = the C run): read, and their deltas at the aligned final positions
    info: dict[str, dict] = {}
    clean_logp = base["logits"][0].log_softmax(-1)
    out["outcomes"].append(outcome(model, c, {"kind": "none"}, base["logits"][0], None))
    for e in EDITS:
        if e not in c["read"]:
            continue
        if e == "E-cue":
            lg, rec_e = base["logits"][1], hc
        else:
            lg1, r1 = forward_rows(model, torch.tensor([c["read"][e]], device="cuda"), [{}], state_layers)
            lg, rec_e = lg1[0], {la: r1[la][0] for la in state_layers}
        kk = common_suffix(c["read"]["clean"], c["read"][e])
        te = len(c["read"][e])
        info[e] = {"K": kk, "logp": lg.log_softmax(-1),
                   "delta": {la: rec_e[la][te - kk :] - h[la][t - kk :] for la in state_layers}}  # fmt: skip
        out["outcomes"].append(outcome(model, c, {"kind": "edit", "edit": e}, lg, {"clean": clean_logp}))
    k_min = min(v["K"] for v in info.values())
    assert k_min >= len(sub["d"]), f"{c['id']}: an edit changed the template"
    for e, inf in info.items():  # the edits' own downstream states: vs each other and on C's delta
        cos = {}
        for e2, inf2 in info.items():
            if e2 != e:
                cos[e2] = {
                    "final": [
                        nanmean(pos_cos(inf["delta"][la][-k_min:], inf2["delta"][la][-k_min:])) for la in cfg["down"]
                    ]
                }
        tr = [
            [*flat_proj(inf["delta"][la][-k_min:], (hc[la] - h[la])[t - k_min :]), None, None] for la in cfg["transit"]
        ]
        out["states"].append(
            {"family": c["family"], "name": c["id"], "kind": "edit", "edit": e, "cos": cos, "transit": tr}
        )
    js_refs = {"clean": clean_logp, **{e: v["logp"] for e, v in info.items()}}
    # pushes, random controls, embedding pushes, copies
    gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_003 * k)
    rows: list[tuple[dict, dict, bool]] = []
    o_rows: list[tuple[dict, dict, bool]] = []
    for key in [*layers, "band"]:
        group = layers if key == "band" else [key]
        for s in scales:
            for sname in SUBSETS:
                pos = sub[sname]
                if not pos:
                    continue
                lens_e, rand_e = {}, {}
                for la in group:
                    norms = s * copy_norms[la] if sname == "r" else torch.full((len(pos),), s * ref[la], device="cuda")
                    vec = push_rows(dirs[la], norms)
                    lens_e[la], rand_e[la] = AddRows(vec, pos), AddRows(null_rows(vec, gen), pos)
                tags = {"kind": "push", "layer": key, "scale": s, "subset": sname}
                state = sname in STATE_SUBSETS
                rows.append(({**tags, "dir": "lens"}, lens_e, state))
                rows.append(({**tags, "dir": "random"}, rand_e, state))
                if sname == "a":
                    o_rows.append(({**tags, "dir": "lens", "prompt": "off"}, lens_e, False))
    for s in cfg["embed_scales"]:
        for kind, vec0 in (("emb_diff", emb[1] - emb[0]), ("emb_add", emb[1])):
            pos = sub["b"]
            vec = s * vec0[None, :].expand(len(pos), -1).contiguous()
            tags = {"kind": kind, "layer": -1, "scale": s, "subset": "b"}
            rows.append(({**tags, "dir": "lens"}, {-1: AddRows(vec, pos)}, True))
            rows.append(({**tags, "dir": "random"}, {-1: AddRows(null_rows(vec, gen), pos)}, False))
    for la in sorted(set(layers) | set(cfg["write_layers"])):
        r = sub["r"]
        rows.append(({"kind": "copy", "layer": la, "subset": "r"}, {la: AddRows(hc[la][r] - h[la][r], r)}, True))
    a = sub["a"]
    for la in layers:  # edited-input patch (Biran et al. 2024): the C run's residual at a (cue included), raw and at
        delta = hc[la][a] - h[la][a]  # the push's per-token norm (C is token-aligned with the clean prompt)
        rows.append(({"kind": "patch", "layer": la, "subset": "a"}, {la: AddRows(delta, a)}, True))
        for s in scales:
            vec = torch.nn.functional.normalize(delta, dim=-1) * (s * ref[la])
            rows.append(({"kind": "patch", "layer": la, "scale": s, "subset": "a"}, {la: AddRows(vec, a)}, True))
    diag = out["diag"]
    for prompt, todo in (("clean", rows), ("off", o_rows)):
        ids = torch.tensor([c["read"][prompt]], device="cuda")
        for start in range(0, len(todo), BATCH - 1):
            chunk = todo[start : start + BATCH - 1]
            need = any(st for _, _, st in chunk)
            logits, rec = forward_rows(model, ids, [{}] + [e for _, e, _ in chunk], state_layers if need else ())
            if prompt == "clean":
                diag["none_vs_clean"].append(float((logits[0] - base["logits"][0]).abs().max()))
            else:
                out["outcomes"].append(outcome(model, c, {"kind": "none", "prompt": "off"}, logits[0], None))
            for j, (tags, e, st) in enumerate(chunk, start=1):
                o = outcome(model, c, tags, logits[j], js_refs if prompt == "clean" else None)
                if tags.get("scale") == 0:
                    o["dl_none"] = float((logits[j] - logits[0]).abs().max())
                    diag["zero_scale"].append(o["dl_none"])
                out["outcomes"].append(o)
                if st:
                    b = None if tags["kind"] == "copy" else row_basis(e)
                    m = state_metrics(rec, j, h, hc, info, b, k_min, sub["qreg"], sub["r"], cfg)
                    out["states"].append({"family": c["family"], "name": c["id"], **tags, **m})
    out["cases"].append({
        "id": c["id"], "family": c["family"], "scene": c.get("scene", c["id"]), "bridge": c["bridge"],
        "cf_bridge": c["cf_bridge"], "answer": c["answer"], "cf_answer": c["cf_answer"], "ld_clean": round(c["ld_clean"], 3),
        "ld_cf": round(c["ld_cf"], 3), "subject": c["subject"], "subject_span": c["subject_span"],
        "prompts": c["prompts"], "read_suffix": c["read_suffix"], "subsets": {k2: v for k2, v in sub.items()},
        "offsets": c["offsets"], "K": {e: v["K"] for e, v in info.items()}, "K_min": k_min, "cand_text": c["cand_text"],
        "norms": {str(la): {"ref_scene": round(ref[la], 3), "ref_item": round(c["ref_item"][la], 3),
                            "resid_median": round(resid[la], 2)} for la in layers},
        "emb_norms": {"diff": round(float((emb[1] - emb[0]).norm()), 4), "x": round(float(emb[1].norm()), 4)},
    })  # fmt: skip


@torch.no_grad()
def text_loss(model, lens, pairs: list[tuple[str, str]], refs: dict[int, float], cfg: dict, n_texts: int = 16) -> dict:
    """Mean next-token loss (nats, from position 4) on WikiText rows with the push at every position from 4 on."""
    tok = model.tokenizer
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:n_texts]
    gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 7)
    dirs = {}
    for i_w, x_w in pairs:
        pt = torch.tensor([model.concept_token(i_w), model.concept_token(x_w)], device="cuda")
        for la in cfg["layers"]:
            v = lens.vectors(la, pt)
            dirs[(i_w, x_w, la)] = v[1] - v[0]
    losses: dict[str, list[float]] = collections.defaultdict(list)
    for ids in texts:
        x = torch.tensor([ids], device="cuda")
        pos = list(range(4, len(ids)))
        conds: list[tuple[str, dict]] = [("none", {})]
        for key in [*cfg["layers"], "band"]:
            group = cfg["layers"] if key == "band" else [key]
            for s in cfg["scales"]:
                for i_w, x_w in pairs:
                    lens_e, rand_e = {}, {}
                    for la in group:
                        vec = push_rows(dirs[(i_w, x_w, la)], torch.full((len(pos),), s * refs[la], device="cuda"))
                        lens_e[la], rand_e[la] = AddRows(vec, pos), AddRows(null_rows(vec, gen), pos)
                    conds += [(f"lens/{key}/x{s:g}", lens_e), (f"random/{key}/x{s:g}", rand_e)]
        for start in range(0, len(conds), 8):
            chunk = conds[start : start + 8]
            logits, _ = forward_rows(model, x, [e for _, e in chunk], full=True)
            for row, (name, _) in enumerate(chunk):
                nll = torch.nn.functional.cross_entropy(logits[row, 3:-1].float(), x[0, 4:])
                losses[name].append(float(nll))
    return {"n_texts": len(texts), "pairs": pairs, "refs": {str(k): round(v, 3) for k, v in refs.items()},
            "mean_nll": {k: round(statistics.mean(v), 4) for k, v in losses.items()}}  # fmt: skip


# ---- analysis ---------------------------------------------------------------------------------------------------------


def ckey(o: dict) -> tuple:
    return (
        o.get("prompt", "clean"),
        o["kind"],
        o.get("dir"),
        o.get("layer"),
        o.get("scale"),
        o.get("subset"),
        o.get("edit"),
    )


def index(rows: list[dict]) -> dict[str, dict[tuple, dict[str, dict]]]:
    out: dict[str, dict[tuple, dict[str, dict]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    for o in rows:
        out[o["family"]][ckey(o)][o["name"]] = o
    return out


def push_key(layer, scale, subset, d="lens", prompt="clean") -> tuple:
    return (prompt, "push", d, layer, scale, subset, None)


def edit_key(e: str) -> tuple:
    return ("clean", "edit", None, None, None, None, e)


def rate(cell: dict[str, dict]) -> float:
    return statistics.mean(o["role"] == "b" for o in cell.values()) if cell else math.nan


def nearest_half(idx_f: dict, keys: list[tuple]) -> tuple | None:
    have = [k for k in keys if idx_f.get(k)]
    return min(have, key=lambda k: (abs(rate(idx_f[k]) - 0.5), keys.index(k))) if have else None


def paired(c1: dict, c2: dict, measure=lambda o: float(o["role"] == "b")) -> tuple[np.ndarray, np.ndarray]:
    names = sorted(set(c1) & set(c2))
    return np.array([measure(c1[n]) for n in names]), np.array([measure(c2[n]) for n in names])


def call(ci: list[float], inject_if: str) -> str:
    lo, hi = ci[1], ci[2]
    if math.isnan(lo):
        return "untestable"
    return {"pos": "inject" if lo > 0 else "write" if hi < 0 else "inconclusive"}[inject_if]


def summarize(cases: list[dict], outcomes: list[dict], states: list[dict], cfg: dict, extra: dict) -> dict:
    idx = index(outcomes)
    fams = list(dict.fromkeys(c["family"] for c in cases))
    layer_keys = [*cfg["layers"], "band"]
    focus = "RL" if "RL" in fams else fams[0]
    cands = [push_key(la, s, "a") for s in cfg["scales"] if s > 0 for la in layer_keys]
    p_star = nearest_half(idx[focus], cands)
    emb_keys = [
        ("clean", kd, "lens", -1, s, "b", None) for s in cfg["embed_scales"] if s > 0 for kd in ("emb_diff", "emb_add")
    ]
    emb_star = nearest_half(idx[focus], emb_keys)
    sm: dict[str, Any] = {"P*": p_star, "emb*": emb_star, "families": {}, **extra}
    for fam in fams:
        f = idx[fam]
        wkeys = [("clean", "copy", None, la, None, "r", None) for la in cfg["write_layers"]]
        w_star = nearest_half(f, wkeys)
        cells = {"|".join(map(str, k)): {"n": len(v), "flips": wilson(sum(o["role"] == "b" for o in v.values()), len(v)),
                                         "frac": statistics.mean(o.get("frac", math.nan) for o in v.values()),
                                         "roles": dict(collections.Counter(o["role"] for o in v.values()))}
                 for k, v in f.items()}  # fmt: skip
        fs: dict[str, Any] = {"W-copy*": w_star, "cells": cells}
        if p_star:
            pc = f[p_star]
            refs = {e: f[edit_key(e)] for e in EDITS if f.get(edit_key(e))}
            if w_star:
                refs["W-copy*"] = f[w_star]
            if emb_star:
                refs["emb*"] = f[emb_star]
            patch_m = ("clean", "patch", None, p_star[3], p_star[4], "a", None)
            if p_star[3] != "band" and f.get(patch_m):
                refs["patch_matched"] = f[patch_m]  # the edited-input patch at P*'s layer and per-token norm
            agree = {}
            for name, cell in refs.items():
                a, b = paired(pc, cell)
                agree[name] = {"n": len(a), "rate_ref": float(b.mean()) if len(b) else None,
                               "kappa": boot(kappa, [a, b]), "jaccard": boot(jaccard, [a, b])}  # fmt: skip
            med = statistics.median(o["ld_clean"] for o in cases if o["family"] == fam)
            ldc = {c["id"]: {"role": "b" if c["ld_clean"] > med else "A"} for c in cases if c["family"] == fam}
            a, b = paired(pc, ldc)
            agree["low_margin"] = {"n": len(a), "kappa": boot(kappa, [a, b])}
            fs["agreement"] = agree
            if f.get(edit_key("E-insert")) and w_star:
                a, b = paired(pc, f[edit_key("E-insert")])
                _, w = paired(pc, f[w_star])
                fs["K1"] = boot(lambda x, y, z: kappa(x, y) - kappa(x, z), [a, b, w])
                fs["K1_call"] = call(fs["K1"], "pos")
            if emb_star and f.get(emb_star) and f.get(edit_key("E-insert")) and w_star:
                em = f[emb_star]
                a, b = paired(em, f[edit_key("E-insert")])
                _, w = paired(em, f[w_star])
                fs["gate"] = boot(lambda x, y, z: kappa(x, y) - kappa(x, z), [a, b, w])
            la_s, sc_s = p_star[3], p_star[4]
            ca, cb, cn = (f.get(push_key(la_s, sc_s, s)) or {} for s in ("a", "b", "nb"))
            names = sorted(set(ca) & set(cb) & set(cn))
            if names:
                fa, fb, fnb = (np.array([float(cc[n]["role"] == "b") for n in names]) for cc in (ca, cb, cn))
                fs["K2_nb_minus_half_a"] = boot(lambda x, y: x.mean() - 0.5 * y.mean(), [fnb, fa])
                fs["K2_b_minus_nb"] = boot(lambda x, y: x.mean() - y.mean(), [fb, fnb])
                lo1, hi1 = fs["K2_nb_minus_half_a"][1:]
                fs["K2_call"] = ("inject" if lo1 > 0 else "write" if hi1 < 0 and fs["K2_b_minus_nb"][1] > 0
                                 else "inconclusive")  # fmt: skip
            fs["js"] = {e: boot(lambda x: x.mean(), [np.array([o["js"][e] for o in pc.values() if e in o.get("js", {})])])
                        for e in ["clean", *EDITS] if any(e in o.get("js", {}) for o in pc.values())}  # fmt: skip
            st = [s_ for s_ in states if s_["family"] == fam and s_["kind"] == "push" and s_.get("dir") == "lens"
                  and s_["layer"] == la_s and s_["scale"] == sc_s]  # fmt: skip
            onset = [i for i, la in enumerate(cfg["down"]) if la < P.ANSWER_ONSET]
            for sname in STATE_SUBSETS:
                rows = [s_ for s_ in st if s_["subset"] == sname]
                cos_tab = {}
                for e in EDITS:
                    vals = [r_["cos"][e]["final"] for r_ in rows if e in r_["cos"]]
                    if vals:
                        cos_tab[e] = [
                            nanmean([v[i] if v[i] is not None else math.nan for v in vals])
                            for i in range(len(cfg["down"]))
                        ]
                fs[f"cos_final_{sname}"] = cos_tab
                if sname == "b" and "E-name" in cos_tab and "E-cue" in cos_tab and onset:
                    diffs = []
                    for r_ in rows:
                        a1 = [r_["cos"]["E-name"]["final"][i] for i in onset]
                        a2 = [r_["cos"]["E-cue"]["final"][i] for i in onset]
                        if None not in a1 and None not in a2:
                            diffs.append(statistics.mean(a1) - statistics.mean(a2))
                    fs["K4"] = boot(lambda x: x.mean(), [np.array(diffs)])
                fs[f"transit_{sname}"] = [nanmean([r_["transit"][i][0] if r_["transit"][i][0] is not None else math.nan
                                                    for r_ in rows]) for i in range(len(cfg["transit"]))]  # fmt: skip
            ename = [s_ for s_ in states if s_["family"] == fam and s_["kind"] == "edit"]
            fs["transit_edits"] = {e: [nanmean([r_["transit"][i][0] if r_["transit"][i][0] is not None else math.nan
                                                 for r_ in ename if r_["edit"] == e]) for i in range(len(cfg["transit"]))]
                                   for e in EDITS if any(r_["edit"] == e for r_ in ename)}  # fmt: skip
        sm["families"][fam] = fs
    if p_star and "BL" in idx and "RL" in idx:
        scene = {c["id"]: c["scene"] for c in cases}
        bl = {scene[n]: o for n, o in idx["BL"][p_star].items()}
        rl = {scene[n]: o for n, o in idx["RL"][p_star].items()}
        a, b = paired(bl, rl)
        sm["K3"] = boot(lambda x, y: x.mean() - y.mean(), [a, b])
        lo, hi = sm["K3"][1:]
        sm["K3_call"] = "inject" if lo > -EQUIV else "write" if hi < -EQUIV else "inconclusive"
    rl_s = sm["families"].get("RL", {})
    calls = [
        c_
        for c_ in (
            rl_s.get("K1_call") if (rl_s.get("gate") or [0, -1])[1] > 0 else "gate failed",
            rl_s.get("K2_call"),
            sm.get("K3_call"),
        )
        if c_
    ]
    n_in, n_wr = calls.count("inject"), calls.count("write")
    sm["calls"] = calls
    sm["verdict"] = ("push behaves like an input-word edit" if n_in >= 2 and n_wr == 0 else
                     "push writes the intermediate" if n_wr >= 2 and n_in == 0 else "mixed")  # fmt: skip
    return sm


def fmt_ci(x) -> str:
    return "-" if not x or x[0] is None or math.isnan(x[0]) else f"{x[0]:+.2f} [{x[1]:+.2f}, {x[2]:+.2f}]"


def write_md(path: Path, sm: dict, cfg: dict) -> None:
    lines = [f"# {EXP}", "", f"P* = {sm['P*']}; emb* = {sm['emb*']}", "",
             f"Verdict (manifest rule): **{sm['verdict']}**; calls (K1 RL, K2 RL, K3) {sm['calls']}; "
             f"K3 BL - RL flips {fmt_ci(sm.get('K3'))}", ""]  # fmt: skip
    for fam, fs in sm["families"].items():
        lines += [f"## {fam} (W-copy* = {fs.get('W-copy*')})", ""]
        lines.append("| condition | n | flips [95% CI] | frac | roles |")
        lines.append("|---|---|---|---|---|")
        for k, v in fs["cells"].items():
            if ("|push|" in k and "|b|" not in k and "|a|" not in k and "|r|" not in k) or k.startswith("off|none"):
                continue
            fl = v["flips"]
            lines.append(f"| {k} | {v['n']} | {100 * fl[0]:.0f}% [{100 * fl[1]:.0f}, {100 * fl[2]:.0f}] | "
                         f"{v['frac']:.2f} | {v['roles']} |")  # fmt: skip
        lines.append("")
        if "agreement" in fs:
            lines.append("Agreement with P* (kappa / Jaccard, item bootstrap): " + "; ".join(
                f"{e}: k {fmt_ci(a['kappa'])}" + (f", J {fmt_ci(a['jaccard'])}" if "jaccard" in a else "")
                + (f" (ref rate {a['rate_ref']:.2f})" if a.get("rate_ref") is not None else "")
                for e, a in fs["agreement"].items()))  # fmt: skip
            lines.append(f"K1 {fmt_ci(fs.get('K1'))} -> {fs.get('K1_call')}; gate {fmt_ci(fs.get('gate'))}; "
                         f"K2 nb - a/2 {fmt_ci(fs.get('K2_nb_minus_half_a'))}, b - nb {fmt_ci(fs.get('K2_b_minus_nb'))} "
                         f"-> {fs.get('K2_call')}; K4 {fmt_ci(fs.get('K4'))}")  # fmt: skip
            lines.append(f"JS(P*, .) {json.dumps({e: round(v[0], 3) for e, v in fs.get('js', {}).items()})}")
            lines.append(f"cos final (b, per down layer {cfg['down']}): {json.dumps(fs.get('cos_final_b'))}")
            lines.append(f"transit proj on C's delta {cfg['transit']}: P*_b {fs.get('transit_b')}, P* {fs.get('transit_a')}, "
                         f"edits {json.dumps(fs.get('transit_edits'))}")  # fmt: skip
            lines.append("")
    if "textloss" in sm:
        lines += ["## Plain-text loss under the push (nats)", "", json.dumps(sm["textloss"]["mean_nll"]), ""]
    lines += ["## Diagnostics", "", json.dumps(sm.get("diag", {}))]
    path.write_text("\n".join(lines) + "\n")


# ---- stages -----------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    inputs = [P.RESULTS / cfg["map"] / "cases.jsonl"] + (
        [CS.RESULTS / cfg["country_map"] / "cases.jsonl"] if cfg["countries"] else []
    )
    inputs += [S.data_dir(cfg["wording"]) / f"{f}.json" for f in cfg["families"]]
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs},
                "seeds": {"null": f"{NULL_SEED} + 1000003 x case index (one generator per item, rows in a fixed order)",
                          "bootstrap": BOOT_SEED, "n_boot": N_BOOT, "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    cases = build_cases(model.tokenizer, cfg)
    scenes: dict[str, list[dict]] = {}
    for c in cases:
        scenes.setdefault(c.get("scene", c["id"]), []).append(c)
    out: dict[str, Any] = {"outcomes": [], "states": [], "cases": [], "diag": {"none_vs_clean": [], "zero_scale": []}}
    k = 0
    done = {f: 0 for f in ("cases", "outcomes", "states")}
    for scene in progress(list(scenes.values()), desc="scenes"):  # suite scenes first, countries last
        run_scene(model, lens, scene, cfg, k, out)
        k += len(scene)
        for f in done:  # appended scene by scene: a run stopped early keeps every finished scene
            with open(out_dir / f"{f}.jsonl", "a") as fh:
                fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in out[f][done[f] :])
            done[f] = len(out[f])
    t_main = time.time() - t0
    refs = {la: statistics.median(c["norms"][str(la)]["ref_scene"] for c in out["cases"]) for la in cfg["layers"]}
    seen, pairs = set(), []
    for c in out["cases"]:
        if c["scene"] not in seen and len(pairs) < cfg["textloss_pairs"]:
            seen.add(c["scene"])
            pairs.append((c["bridge"], c["cf_bridge"]))
    tl = text_loss(model, lens, pairs, refs, cfg) if cfg["textloss_pairs"] else {}
    (out_dir / "textloss.json").write_text(json.dumps(tl, indent=2) + "\n")
    d = out["diag"]
    extra = {"textloss": tl, "seconds": {"main": round(t_main), "textloss": round(time.time() - t0 - t_main)},
             "n_cases": len(cases), "n_outcomes": len(out["outcomes"]),
             "diag": {"max_none_vs_clean_logit": max(d["none_vs_clean"], default=None),
                      "max_zero_scale_vs_none_logit": max(d["zero_scale"], default=None), "n_zero_scale": len(d["zero_scale"])}}  # fmt: skip
    extra["replication"] = replication(out["outcomes"])
    sm = summarize(out["cases"], out["outcomes"], out["states"], cfg, extra)
    (out_dir / "summary.json").write_text(json.dumps(sm, indent=2, default=str) + "\n")
    write_md(out_dir / "summary.md", sm, cfg)
    print((out_dir / "summary.md").read_text())


def replication(outcomes: list[dict]) -> dict | None:
    """Agreement of the r-subset lens pushes with read_write layers_v1's roles on the same items, layers and scales."""
    path = RW.RESULTS / "layers_v1" / "outcomes.jsonl"
    if pins.TARGET != "qwen3.6-27b" or not path.exists():
        return None
    old = {}
    for line in path.read_text().splitlines():
        o = json.loads(line)
        if o["part"].startswith("lens_x") and o["layer"] != "band":
            old[(o["name"], o["layer"], float(o["part"][6:]))] = o["role"]
    pairs = [(o["role"], old[k]) for o in outcomes if o["kind"] == "push" and o.get("dir") == "lens"
             and o.get("subset") == "r" and o.get("prompt") is None
             and (k := (o["name"], o["layer"], o["scale"])) in old]  # fmt: skip
    return {"n": len(pairs), "role_agreement": statistics.mean(a == b for a, b in pairs) if pairs else None}


def load_run(name: str) -> tuple[dict, list, list, list, dict]:
    d = RESULTS / name
    rd = [
        [json.loads(x) for x in (d / f).read_text().splitlines()]
        for f in ("cases.jsonl", "outcomes.jsonl", "states.jsonl")
    ]
    m = json.loads((d / "manifest.json").read_text())
    tl = json.loads((d / "textloss.json").read_text()) if (d / "textloss.json").exists() else {}
    return m, rd[0], rd[1], rd[2], tl


def stage_analyze(name: str) -> None:
    m, cases, outcomes, states, tl = load_run(name)
    sub = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    sub.mkdir()
    sm = summarize(cases, outcomes, states, m["config"], {"textloss": tl})
    (sub / "summary.json").write_text(json.dumps(sm, indent=2, default=str) + "\n")
    write_md(sub / "summary.md", sm, m["config"])
    print(sub)


def spans_of(positions: list[int], offsets: list, role: str) -> list[dict]:
    """Contiguous token runs as char spans."""
    out: list[dict] = []
    for p in sorted(positions):
        s, e = offsets[p]
        if out and out[-1]["end"] >= s - 1 and out[-1]["_last"] == p - 1:
            out[-1]["end"], out[-1]["_last"] = e, p
        else:
            out.append({"start": s, "end": e, "role": role, "_last": p})
    return [{k: v for k, v in sp.items() if k != "_last"} for sp in out]


def word_spans(text: str, word: str, role: str) -> list[dict]:
    return [{"start": m.start(), "end": m.end(), "role": role} for m in re.finditer(rf"\b{re.escape(word)}\b", text)]


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    _, cases, outcomes, _, _ = load_run(name)
    sm = json.loads((d / "summary.json").read_text())
    idx = index(outcomes)
    p_star = tuple(sm["P*"]) if sm.get("P*") else None
    emb_star = tuple(sm["emb*"]) if sm.get("emb*") else None
    assert p_star, "no P* in the run's summary"
    groups = {"both": "P* and E-insert both give X's answer", "push_only": "P* gives X's answer, E-insert does not",
              "edit_only": "E-insert gives X's answer, P* does not", "neither": "neither gives X's answer"}  # fmt: skip
    members: dict[str, list[dict]] = {g: [] for g in groups}
    for c in cases:
        f = idx[c["family"]]
        pc, ec = f[p_star].get(c["id"]), f[edit_key("E-insert")].get(c["id"])
        if pc is None or ec is None:
            continue
        g = {(True, True): "both", (True, False): "push_only", (False, True): "edit_only", (False, False): "neither"}[
            (pc["role"] == "b", ec["role"] == "b")
        ]
        members[g].append(c)
    rng = np.random.default_rng(seed)
    examples = []
    for g, cs in members.items():
        picked = [cs[i] for i in sorted(rng.choice(len(cs), size=min(k, len(cs)), replace=False))] if cs else []
        for c in picked:
            f = idx[c["family"]]
            ws = sm["families"][c["family"]].get("W-copy*")
            conds = {"P*": p_star, "P*_b": push_key(p_star[3], p_star[4], "b"), **{e: edit_key(e) for e in EDITS}}
            if ws:
                conds["W-copy*"] = tuple(ws)
            if emb_star:
                conds["emb*"] = emb_star
            clean = f[("clean", "none", None, None, None, None, None)][c["id"]]
            ins = f[edit_key("E-insert")][c["id"]]["top"]
            wc = f[tuple(ws)][c["id"]]["top"] if ws else None
            p_top = f[p_star][c["id"]]["top"]
            for cname, key in conds.items():
                o = f.get(key, {}).get(c["id"])
                if o is None:
                    continue
                is_edit = key[1] == "edit"
                prompt = c["prompts"][key[6] if is_edit else "clean"] + c["read_suffix"]
                spans = word_spans(prompt, c["bridge"], "bridge") + word_spans(prompt, c["cf_bridge"], "x")
                if is_edit:
                    s0, s1 = char_diff(c["prompts"]["clean"], c["prompts"][key[6]])
                    spans.append({"start": s0, "end": s1, "role": "edit"})
                else:
                    spans.append({"start": c["subject_span"][0], "end": c["subject_span"][1], "role": "cue"})
                    spans += spans_of(c["subsets"][key[5]], c["offsets"], "pushed" if key[1] != "copy" else "patched")
                what = (f"text edit {key[6]}, then a normal forward" if is_edit else
                        f"{key[1]} ({key[2] or 'C copy'}) at layer {key[3]}, scale {key[4]}, positions {key[5]}")  # fmt: skip
                expected = ({"H-inject": ins, "H-write": wc} if cname.startswith("P*") else
                            {"H-inject": p_top if key[6] in ("E-insert", "E-head") or cname == "emb*" else None,
                             "H-write": p_top if key[6] == "E-cue" or cname == "W-copy*" else None})  # fmt: skip
                examples.append({"group": g, "family": c["family"], "item_id": c["id"], "prompt": prompt, "spans": spans,
                                 "condition": f"{cname}: {what}",
                                 "answers": {"clean": clean["top"], "edited": o["top"], "expected": expected},
                                 "numbers": {"p_A": o["p"][0], "p_b": o["p"][1], "ld": o["ld"], "frac": o.get("frac"),
                                             "flip": o["role"] == "b", "role": o["role"]},
                                 "why": f"{groups[g]} on this item ({c['bridge']} -> {c['cf_bridge']})"})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


# ---- figures (CPU only, from a finished run) --------------------------------------------------------------------------

SCALE_COLOURS = {4.0: "#86b6ef", 8.0: "#2a78d6", 16.0: "#104281"}  # one hue light -> dark (ordinal; validated)
CALL_COLOURS = {"inject": "#2a78d6", "write": "#eb6834", "inconclusive": "#898781", "untestable": "#898781"}
EDIT_COLOURS = dict(zip(EDITS, ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"), strict=True))  # slot order
ROLE_COLOURS = {"A": "#2a78d6", "bO": "#eb6834", "b": "#1baf7a", "other": "#eda100"}
BAR = "#52514e"
# Plain names for figures and reports (the user's rule, scratchpad figure_terms.md: an outside reader knows only bridge
# org / alt, answer org / alt, org prompt / alt prompt; families via plotting.family_label; no condition codes)
SUBSET_TITLES = {"a": "whole question", "b": "subject phrase only", "nb": "question without\nthe subject phrase",
                 "d": "last tokens\n(chat template)", "r": "after the cue, sized like\nthe alt prompt's change"}  # fmt: skip
EDIT_WORDS = {"E-name": "name bridge alt directly", "E-insert": "add bridge alt next to the cue",
              "E-head": "swap the noun for bridge alt", "E-cue": "alt prompt", "E-unrelated": "mention bridge alt elsewhere"}  # fmt: skip
FLIPS = PLOT_TERM["flips"]  # the user's exact wording for flip rates on every axis and legend


def wrap(text: str, width: int) -> str:
    import textwrap

    return "\n".join(textwrap.wrap(text, width))


def example_line(cases: list[dict], both: bool = False, off: bool = False) -> str:
    """One real prompt pair in the outside reader's terms (org prompt / alt prompt, bridge and answer org / alt)."""
    rl = next((c for c in cases if c["family"] == "RL"), None)
    if rl is None:
        return ""
    bl = next((c for c in cases if c["family"] == "BL" and c["scene"] == rl["scene"]), None)
    cue_alt = re.search(r"known for (.+?)\?", rl["prompts"]["E-cue"])
    out = (f"\"... The {rl['bridge']}'s locker is {rl['answer']}. ... Which locker belongs to the animal known for "
           f"{rl['subject'].split('known for ')[-1]}?\" -> answer org {rl['answer']} (bridge org {rl['bridge']}); alt prompt "
           f"\"... known for {cue_alt[1] if cue_alt else '...'}?\" -> answer alt {rl['cf_answer']} (bridge alt {rl['cf_bridge']}).")  # fmt: skip
    if both and bl:
        out += (f" Same scene, prompt → prompt: \"Which locker belongs to {bl['subject']}?\" (the {bl['bridge']} in the org "
                f"prompt, the {bl['cf_bridge']} in the alt prompt).")  # fmt: skip
    if off:
        ct = rl["cand_text"]
        out += (f" Off-path control: the lockers of the {rl['cf_bridge']} and a third animal swapped, so answer org stays "
                f"{rl['answer']} and its answer alt is {ct['bO']} (not {rl['cf_answer']}).")  # fmt: skip
    return out


def err(v: np.ndarray) -> np.ndarray:
    """[[below], [above]] error-bar lengths from rows (estimate, lo, hi), clipped at 0 (Wilson's float edges)."""
    v = np.asarray(v, float)
    return np.clip(np.stack([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]]), 0, None)


def wilson_of(cell: dict) -> list[float]:
    return list(wilson(sum(o["role"] == "b" for o in cell.values()), len(cell))) if cell else [math.nan] * 3


def scene_diff(idx: dict, key: tuple, scene_of: dict, f1: str = "BL", f2: str = "RL") -> list[float]:
    """flips(f1) - flips(f2) under one condition, paired by scene, item bootstrap."""
    a_ = {scene_of[n]: o for n, o in idx[f1].get(key, {}).items()}
    b_ = {scene_of[n]: o for n, o in idx[f2].get(key, {}).items()}
    x, y = paired(a_, b_)
    return boot(lambda u, v: u.mean() - v.mean(), [x, y]) if len(x) else [math.nan] * 3


def state_rows(states: list[dict], fam: str, **where) -> list[dict]:
    return [s for s in states if s["family"] == fam and all(s.get(k) == v for k, v in where.items())]


def mean_ci(vals) -> list[float]:
    v = np.array([x for x in vals if x is not None and not math.isnan(x)], float)
    return boot(lambda u: u.mean(), [v]) if len(v) else [math.nan] * 3


def stage_figures(name: str) -> None:
    """Figures and the decision rule re-applied, into <run>/analysis-<stamp>-figures/ (summary.json, PNG + SVG)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace import plotting as PL

    m, cases, outcomes, states, tl = load_run(name)
    cfg = {
        **m["config"],
        "scales": [s for s in m["config"]["scales"] if s > 0],
    }  # a smoke's zero scale is a no-op check
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    assert not out.exists(), f"{out} exists"
    idx = index(outcomes)
    scene_of = {c["id"]: c["scene"] for c in cases}
    sm = summarize(cases, outcomes, states, cfg, {"textloss": tl})  # the pre-registered rule, re-applied
    p_star = sm["P*"]
    assert p_star, "no P*"
    la_s, sc_s = p_star[3], p_star[4]
    pb_key = push_key(la_s, sc_s, "b")
    n_of = {f: len({c["id"] for c in cases if c["family"] == f}) for f in idx}
    keys = [*cfg["layers"], "band"]
    xs = np.arange(len(keys))
    xl = [str(k) for k in cfg["layers"]] + ["all 4"]
    figs: list[str] = []

    def save(fig, stem: str, title: str, explain: list[tuple[str, str]], data: str, handles=None, ncols=None,
             manual: dict | None = None) -> None:  # fmt: skip
        """plotting.finish's frame with its labelled caption rows (What we did / Example / How to read / Control / Data),
        legend below; saved as 200-dpi PNG and SVG (finish saves a 150-dpi PNG only)."""
        import textwrap

        h, w = fig.get_figheight(), fig.get_figwidth()
        fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=PL.INK)
        label_w, y = 1.05, 0.38
        for label, text in [*explain, ("Data", data)]:
            lines = textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]
            fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=PL.INK, fontweight="bold")
            fig.text(label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=PL.MUTED,
                     linespacing=1.4)  # fmt: skip
            y += 0.155 * len(lines) + 0.05
        head = y + 0.1
        rows_ = -(-len(handles) // (ncols or len(handles))) if handles else 0
        foot = 0.2 + 0.25 * rows_ if handles else 0.05
        if handles:
            fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=9,
                       handlelength=2.6, labelcolor=PL.INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
        if manual is None:
            fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
        else:  # long tick labels: tight_layout would shrink every panel to fit them
            fig.subplots_adjust(bottom=(foot + 0.45) / h, top=1 - (head + 0.3) / h, **manual)
        out.mkdir(exist_ok=True)  # created at the first figure, so a failed run leaves no empty folder
        for ext in ("png", "svg"):
            fig.savefig(out / f"{stem}.{ext}", dpi=200, facecolor=PL.SURFACE)
        plt.close(fig)
        figs.append(f"{stem}.png")

    # (post hoc, not pre-registered) the K2/K3 statistics on input edits, which inject by construction
    post: dict[str, Any] = {"K3_on_input_edits": {}}
    k3_rows = {
        "the tested push (whole question; pre-registered)": p_star,
        "lens push on the subject phrase only, same layer and size": pb_key,
        f"lens push on the subject phrase only, layer {cfg['layers'][0]}, {max(cfg['scales']):g}x": push_key(cfg["layers"][0], max(cfg["scales"]), "b"),
        "add bridge alt's word to the input (embedding)": ("clean", "emb_add", "lens", -1, 1.0, "b", None),
        "add (bridge alt − bridge org) to the input (embedding)": ("clean", "emb_diff", "lens", -1, 1.0, "b", None),
        "text: swap the noun for bridge alt": edit_key("E-head"),
        "text: add bridge alt next to the cue": edit_key("E-insert"),
        "text: name bridge alt directly": edit_key("E-name"),
    }  # fmt: skip
    for label, key in k3_rows.items():
        post["K3_on_input_edits"][label] = scene_diff(idx, key, scene_of)
    for fam in ("RL", "RR"):
        rows = state_rows(states, fam, kind="push", dir="lens", layer=la_s, scale=sc_s, subset="b")
        rnd = state_rows(states, fam, kind="push", dir="random", layer=la_s, scale=sc_s, subset="b")
        onset = [i for i, la in enumerate(cfg["down"]) if la < P.ANSWER_ONSET]
        alt = [statistics.mean(r_["cos"]["E-head"]["final"][i] for i in onset) - statistics.mean(r_["cos"]["E-cue"]["final"][i] for i in onset)
               for r_ in rows if "E-head" in r_["cos"] and None not in [r_["cos"][e]["final"][i] for e in ("E-head", "E-cue") for i in onset]]  # fmt: skip
        flips = {n: o["role"] == "b" for n, o in idx[fam].get(pb_key, {}).items()}
        tr = {k_: [] for k_ in ("flipped", "kept")}
        for r_ in rows:
            v = [t[0] for t in r_["transit"] if t[0] is not None]
            if v:
                tr["flipped" if flips.get(r_["name"]) else "kept"].append(statistics.mean(v))
        post[fam] = {"K4_alt_E-head_minus_E-cue": mean_ci(alt),
                     "transit_P*_b_by_flip": {k_: mean_ci(v) for k_, v in tr.items()},
                     "n_flipped_P*_b": sum(flips.values()),
                     "random_b_cos_final": {e: [nanmean([r_["cos"][e]["final"][i] if r_["cos"][e]["final"][i] is not None else math.nan
                                                         for r_ in rnd if e in r_["cos"]]) for i in range(len(cfg["down"]))]
                                            for e in EDITS if any(e in r_["cos"] for r_ in rnd)}}  # fmt: skip

    # 1. headline: where must the push land, next to the text edits and controls
    fams = [f for f in ("RL", "BL") if f in idx]
    fig, grid = plt.subplots(len(fams), 7, figsize=(19, 3.6 * len(fams) + 0.4), squeeze=False,
                             gridspec_kw={"width_ratios": [1, 1, 1, 1, 1, 1.3, 1.25]})  # fmt: skip
    for i, fam in enumerate(fams):
        f = idx[fam]
        grid[i][5].axis("off")  # room for the reference panel's labels
        for j, sname in enumerate(("a", "b", "nb", "d", "r")):
            ax = grid[i][j]
            PL.style_axes(ax)
            PL.percent_axis(ax)
            for si, s in enumerate(cfg["scales"]):
                v = np.array([wilson_of(f.get(push_key(k, s, sname), {})) for k in keys])
                ax.errorbar(xs + (si - 1) * 0.13, v[:, 0], yerr=err(v), color=SCALE_COLOURS[s],
                            lw=2, marker="o", ms=4.5, elinewidth=1, capsize=0, zorder=3)  # fmt: skip
            v = np.array([wilson_of(f.get(push_key(k, max(cfg["scales"]), sname, "random"), {})) for k in keys])
            ax.errorbar(xs + 0.3, v[:, 0], yerr=err(v), color=PL.MUTED, ls="--", lw=1.2,
                        marker="o", mfc=PL.SURFACE, ms=4, elinewidth=0.8, capsize=0, zorder=2)  # fmt: skip
            if fam == "RL" and sname == "a":
                ax.plot([keys.index(la_s) + (cfg["scales"].index(sc_s) - 1) * 0.13], [rate(f[p_star])], marker="*", ms=15,
                        color=PL.INK, mfc="none", zorder=4)  # fmt: skip
            ax.set_ylim(-0.04, 1.04)
            ax.set_xticks(xs, xl)
            if i == 0:
                ax.set_title(SUBSET_TITLES[sname], fontsize=9.5, color=PL.INK, loc="left")
            if j == 0:
                ax.set_ylabel(f"{PL.family_label(fam)}\n{wrap(FLIPS, 34)}", fontsize=8.5, color=PL.INK)
            else:
                ax.set_yticklabels([])
            if i == len(fams) - 1:
                ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
        ax = grid[i][6]
        PL.style_axes(ax)
        PL.percent_axis(ax, "x")
        ws = sm["families"][fam].get("W-copy*")
        refs = [(EDIT_WORDS[e], edit_key(e), None) for e in EDITS]
        refs += [("add bridge alt's word to the input (embedding)", ("clean", "emb_add", "lens", -1, 1.0, "b", None),
                  ("clean", "emb_add", "random", -1, 1.0, "b", None)),
                 ("add (bridge alt − bridge org) to the input (embedding)", ("clean", "emb_diff", "lens", -1, 1.0, "b", None),
                  ("clean", "emb_diff", "random", -1, 1.0, "b", None)),
                 (f"patch from the alt prompt after the cue, layer {la_s}", ("clean", "copy", None, la_s, None, "r", None), None),
                 (f"patch from the alt prompt after the cue, layer {ws[3] if ws else '-'}", tuple(ws) if ws else None, None),
                 (f"patch from the alt prompt, whole question, layer {la_s}", ("clean", "patch", None, la_s, None, "a", None), None),
                 (f"  same, rescaled to the push's size ({sc_s:g}x)", ("clean", "patch", None, la_s, sc_s, "a", None), None)]  # fmt: skip
        ys = np.arange(len(refs))[::-1]
        for y, (_, key, ctrl) in zip(ys, refs, strict=True):
            r_ = wilson_of(f.get(key, {})) if key else [math.nan] * 3
            if not math.isnan(r_[0]):
                ax.barh(y, r_[0], height=0.62, color=BAR, zorder=2)
                ax.errorbar(r_[0], y, xerr=err(np.array([r_])), color=PL.INK, elinewidth=0.9, capsize=0, zorder=3)
                ax.text(min(r_[2], 1.0) + 0.03, y, f"{100 * r_[0]:.0f}%", va="center", fontsize=8, color=PL.INK)
            if ctrl and f.get(ctrl):
                c_ = wilson_of(f[ctrl])
                ax.plot(c_[0], y, marker="o", mfc=PL.SURFACE, color=PL.MUTED, ms=5, zorder=4)
        ax.set_yticks(ys, [r[0] for r in refs], fontsize=8, color=PL.INK)
        ax.set_xlim(0, 1.18)
        if i == 0:
            ax.set_title("same items: prompt edits and other controls", fontsize=9.5, color=PL.INK, loc="left")
        if i == len(fams) - 1:
            ax.set_xlabel(wrap(FLIPS, 48), fontsize=8.5, color=PL.MUTED)
    handles = [
        Line2D([], [], color=SCALE_COLOURS[s], lw=2, marker="o", label=f"lens push (bridge alt − bridge org), {s:g}x")
        for s in cfg["scales"]
    ]
    handles += [Line2D([], [], color=PL.MUTED, ls="--", marker="o", mfc=PL.SURFACE, label=f"control: random push (same size, {max(cfg['scales']):g}x)"),
                Patch(color=BAR, label="prompt edit or patch (bar)"),
                Line2D([], [], color=PL.MUTED, ls="", marker="o", mfc=PL.SURFACE, label="control: random embedding push (same size)"),
                Line2D([], [], color=PL.INK, ls="", marker="*", mfc="none", ms=12, label="the push the decision rule tests")]  # fmt: skip
    explain = [
        ("What we did", "Added the lens direction bridge alt − bridge org to the org prompt's hidden state at one early layer "
                        "(or all four), on one set of question tokens (column titles), at 4, 8 or 16 times the size of the "
                        "alt-prompt patch per token."),
        ("Example", example_line(cases, both=True)),
        ("How to read", "Each dot: the share of items whose answer switched, by layer pushed (top row memory → prompt, bottom "
                        "row prompt → prompt). Bars: the same items under prompt edits and patches. At 16x or on all four "
                        "layers the push often yields neither answer."),
        ("Control", "Gray dashed line: a random push of the same size (16x); hollow dots on the embedding bars: a random "
                    "embedding push. Both should stay near 0%."),
    ]  # fmt: skip
    data = f"Qwen3.6-27B; {n_of.get('RL', 0)} items per family on the same scenes; error bars: Wilson 95%."
    save(fig, "fig1_where_the_push_works", "Where must an early lens push land to switch the answer to answer alt, and how does it compare with editing the prompt?",
         explain, data, handles, ncols=4, manual={"left": 0.075, "right": 0.965, "wspace": 0.22, "hspace": 0.38})  # fmt: skip

    # 2. the pre-registered tests, and the same statistics on input edits (which inject by construction)
    rl, rr = sm["families"].get("RL", {}), sm["families"].get("RR", {})
    mp, pp, mm = (PL.family_label(f) for f in ("RL", "BL", "RR"))
    rows_l = [(f"test 2 ({mp}): question without the subject phrase,\nminus half of the whole question", rl.get("K2_nb_minus_half_a"), 0.0, rl.get("K2_call")),
              (f"test 2 ({mp}): subject phrase only,\nminus question without the subject phrase", rl.get("K2_b_minus_nb"), 0.0, None),
              (f"test 3: {pp} minus {mp},\nthe tested push", sm.get("K3"), -EQUIV, sm.get("K3_call"))]  # fmt: skip
    rows_l += [
        (f"{pp} minus {mp},\n{k_}", v, -EQUIV, "control") for k_, v in list(post["K3_on_input_edits"].items())[1:]
    ]
    rows_r = [(f"test 1 ({mp}): agreement with 'add bridge alt next to the cue',\nminus agreement with the patch from the alt prompt (layers 32-48)", rl.get("K1"), 0.0, rl.get("K1_call")),
              (f"validity check ({mp}): the same for the embedding push", rl.get("gate"), 0.0, None),
              (f"later layers ({mp}): like 'name bridge alt directly',\nminus like the alt prompt", rl.get("K4"), 0.0, None),
              (f"post hoc ({mp}): like 'swap the noun for bridge alt',\nminus like the alt prompt", post["RL"]["K4_alt_E-head_minus_E-cue"], 0.0, None),
              (f"later layers ({mm}): like 'name bridge alt directly',\nminus like the alt prompt", rr.get("K4"), 0.0, None),
              (f"post hoc ({mm}): like 'swap the noun for bridge alt',\nminus like the alt prompt", post.get("RR", {}).get("K4_alt_E-head_minus_E-cue"), 0.0, None)]  # fmt: skip
    fig, axes = plt.subplots(1, 2, figsize=(17, 7.2), gridspec_kw={"width_ratios": [1.1, 1]})
    from matplotlib.ticker import FuncFormatter

    for ax, rows, unit, mult in (
        (axes[0], rows_l, "difference, percentage points, in\n" + FLIPS, 100),
        (axes[1], rows_r, "difference (agreement: Cohen's kappa; later layers: cosine)", 1),
    ):
        PL.style_axes(ax)
        ys = np.arange(len(rows))[::-1]
        for y, (_, ci_, _thr, cl) in zip(ys, rows, strict=True):
            ci = list(ci_) if ci_ is not None else [math.nan] * 3
            colour = CALL_COLOURS.get(cl or "", PL.INK) if cl != "control" else PL.MUTED
            if not math.isnan(ci[0]) and not math.isnan(ci[1]):
                ax.errorbar(ci[0], y, xerr=err(np.array([ci])), color=colour, marker="o", ms=7,
                            mfc=colour if cl != "control" else PL.SURFACE, elinewidth=1.6, capsize=0, zorder=3)  # fmt: skip
                p = 0 if mult == 100 else 2
                tag = f"{mult * ci[0]:+.{p}f} [{mult * ci[1]:+.{p}f}, {mult * ci[2]:+.{p}f}]"
                tag += f"  -> {cl}" if cl and cl != "control" else ""
                ax.annotate(
                    tag, (ci[2], y), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8, color=PL.INK
                )
            else:
                ax.annotate("not testable: 'add bridge alt next to the cue'\nswitches every item", (-0.55, y),
                            va="center", fontsize=8, color=PL.MUTED)  # fmt: skip
        if mult == 100:
            ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{100 * v:+.0f}"))
        ax.axvline(0, color=PL.MUTED, lw=1, zorder=1)
        ax.set_yticks(ys, [r[0] for r in rows], fontsize=8.5, color=PL.INK)
        ax.set_xlabel(unit, fontsize=9, color=PL.MUTED)
    axes[0].axvline(-EQUIV, color=PL.MUTED, ls=":", lw=1)
    axes[0].set_xlim(-1.05, 1.0)
    axes[1].set_xlim(-0.6, 0.75)
    handles = [Line2D([], [], color=CALL_COLOURS["inject"], marker="o", ls="", label="rule says: like an input-word edit"),
               Line2D([], [], color=CALL_COLOURS["write"], marker="o", ls="", label="rule says: writes the intermediate"),
               Line2D([], [], color=PL.INK, marker="o", ls="", label="secondary / reported"),
               Line2D([], [], color=PL.MUTED, marker="o", mfc=PL.SURFACE, ls="", label="control: test 3's difference for edits of the input itself (not pre-registered)"),
               Line2D([], [], color=PL.MUTED, ls=":", label="test 3's margin (-15 points)")]  # fmt: skip
    plain_calls = [
        {"gate failed": "not testable", "untestable": "not testable"}.get(c_, c_) or "-" for c_ in sm["calls"]
    ]
    explain = [
        ("What we did", f"Applied the three pre-registered tests to the tested push: the lens push bridge alt − bridge org "
                        f"on the whole question at layer {la_s}, {sc_s:g}x (the setting whose {mp} rate was nearest 50%: "
                        f"{100 * rate(idx['RL'][p_star]):.0f}% for {mp}, {100 * rate(idx['BL'][p_star]):.0f}% for {pp})."),
        ("Example", example_line(cases, both=True)),
        ("How to read", f"Each dot: a difference with its 95% interval; colour: what the rule calls it. Verdict: "
                        f"'{sm['verdict']}' (tests 1, 2, 3: {', '.join(plain_calls)})."),
        ("Control", f"Gray hollow rows: test 3's {pp} minus {mp} difference for edits of the input itself, which inject a "
                    "word by construction; if test 3 can tell injection from writing, they should sit near 0."),
    ]  # fmt: skip
    data = f"Qwen3.6-27B; {n_of.get('RL', 0)} items per family; item-bootstrap 95% CI ({N_BOOT:,} resamples, seed {BOOT_SEED})."
    save(
        fig,
        "fig2_decision_tests",
        "Do the pre-registered tests tell an input-word edit from a write of the intermediate?",
        explain,
        data,
        handles,
        ncols=3,
    )

    # 3. per-item agreement of P* with each reference
    agree_fams = [f for f in ("RL", "RR", "R", "BL", "BR", "B") if "agreement" in sm["families"].get(f, {})
                  and 0 < rate(idx[f][p_star]) < 1]  # P* flipping every item or none leaves no kappa to draw  # fmt: skip
    ref_names = ["E-head", "E-insert", "W-copy*", "emb*", "patch_matched", "low_margin", "E-name", "E-cue"]
    ref_words = {"E-head": "text: swap the noun for bridge alt", "E-insert": "text: add bridge alt next to the cue",
                 "W-copy*": "patch from the alt prompt (layers 32-48)",
                 "emb*": "add bridge alt's word to the input (embedding)",
                 "patch_matched": "patch from the alt prompt, whole question,\nsame layer, rescaled to the push's size",
                 "low_margin": "baseline: small answer-org margin", "E-name": "text: name bridge alt directly",
                 "E-cue": "the alt prompt"}  # fmt: skip
    fig, axes = plt.subplots(1, len(agree_fams), figsize=(6.4 * len(agree_fams), 5.4), sharey=True, squeeze=False)
    for ax, fam in zip(axes[0], agree_fams, strict=True):
        PL.style_axes(ax)
        ag = sm["families"][fam]["agreement"]
        ys = np.arange(len(ref_names))[::-1]
        for y, rn in zip(ys, ref_names, strict=True):
            a = ag.get(rn)
            k_ = a["kappa"] if a else None
            if k_ and not math.isnan(k_[0]) and not math.isnan(k_[1]):
                ax.errorbar(
                    k_[0],
                    y,
                    xerr=err(np.array([k_])),
                    color=PL.INK,
                    marker="o",
                    ms=6,
                    elinewidth=1.4,
                    capsize=0,
                )
                ax.annotate(
                    f"{k_[0]:+.2f}",
                    (k_[2], y),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va="center",
                    fontsize=8,
                    color=PL.INK,
                )
            else:
                rr_ = a.get("rate_ref") if a else None
                why = f"no kappa: it switches {100 * rr_:.0f}% of items" if rr_ is not None else "no kappa"
                ax.annotate(why, (-0.55, y), va="center", fontsize=7.5, color=PL.MUTED)
        ax.axvline(0, color=PL.MUTED, lw=1)
        ax.set_xlim(-0.6, 0.85)
        ax.set_title(
            f"{PL.family_label(fam)}: the push switches {100 * rate(idx[fam][p_star]):.0f}% of {n_of[fam]}",
            fontsize=9.5,
            color=PL.INK,
            loc="left",
        )
        ax.set_xlabel("item-by-item agreement (Cohen's kappa)", fontsize=9, color=PL.MUTED)
    axes[0][0].set_yticks(
        np.arange(len(ref_names))[::-1], [ref_words[r] for r in ref_names], fontsize=8.5, color=PL.INK
    )
    absent = [PL.family_label(f) for f in ("BL", "BR", "B", "R") if f in idx and f not in agree_fams]
    explain = [
        ("What we did", f"For every item, noted whether the tested push (lens push bridge alt − bridge org on the whole "
                        f"question, layer {la_s}, {sc_s:g}x) switches answer org to answer alt, and the same for each other edit."),
        ("Example", example_line(cases)),
        ("How to read", "Each dot: item-by-item agreement (Cohen's kappa) between the push and that edit; 0 = no more "
                        "overlap than chance, 1 = the same items. An edit that switches every item has no kappa."),
        ("Control", "Baseline row: items whose answer org wins by a small margin. Agreement with it is what any edit gets "
                    "just because some items are easy to switch."),
    ]  # fmt: skip
    data = (f"Qwen3.6-27B; {n_of.get('RL', 0)} items per family; item-bootstrap 95% CI. Not shown: {'; '.join(absent)} "
            "(the push switches none or all of their items).")  # fmt: skip
    save(fig, "fig3_item_agreement", "Item by item, which edit does the early push agree with?", explain, data)

    # 4. downstream states: cosine with each edit's change, and the in-transit projection on C's change
    st_fams = [f for f in ("RL", "RR") if f in idx]
    fig, axes = plt.subplots(
        len(st_fams), 2, figsize=(13, 3.8 * len(st_fams)), squeeze=False, gridspec_kw={"width_ratios": [1.2, 1]}
    )
    for i, fam in enumerate(st_fams):
        ax = axes[i][0]
        PL.style_axes(ax)
        rows = state_rows(states, fam, kind="push", dir="lens", layer=la_s, scale=sc_s, subset="b")
        rnd = state_rows(states, fam, kind="push", dir="random", layer=la_s, scale=sc_s, subset="b")
        dl = np.array(cfg["down"], float)
        for k_, e in enumerate(EDITS):
            if not any(e in r_["cos"] for r_ in rows):
                continue
            cis = [mean_ci([r_["cos"][e]["final"][li] for r_ in rows if e in r_["cos"]]) for li in range(len(dl))]
            v = np.array(cis)
            off = (k_ - 2) * 0.35
            ax.errorbar(dl + off, v[:, 0], yerr=err(v), color=EDIT_COLOURS[e], lw=2, marker="o", ms=5,
                        elinewidth=1, capsize=0, label=EDIT_WORDS[e])  # fmt: skip
            rv = [mean_ci([r_["cos"][e]["final"][li] for r_ in rnd if e in r_["cos"]])[0] for li in range(len(dl))]
            ax.plot(dl + off, rv, color=EDIT_COLOURS[e], ls=":", lw=1, alpha=0.8)
        ax.axhline(0, color=PL.MUTED, lw=1)
        ax.set_xticks(dl, [str(int(x)) for x in dl])
        ax.set_xlim(dl[0] - 2, dl[-1] + 2)
        ax.set_ylabel(f"{PL.family_label(fam)}\ncosine of the changes at the last tokens", fontsize=9, color=PL.INK)
        ax.set_xlabel("layer read (downstream of the push)", fontsize=9, color=PL.MUTED)
        if i == 0:
            ax.set_title(
                "push on the subject phrase vs each prompt edit; dotted: random push",
                fontsize=9.5,
                color=PL.INK,
                loc="left",
            )
        ax = axes[i][1]
        PL.style_axes(ax)
        bars = []
        tr_b = post.get(fam, {}).get("transit_P*_b_by_flip", {})
        bars.append(
            (
                f"push on the subject, items it switched (n={post.get(fam, {}).get('n_flipped_P*_b', 0)})",
                tr_b.get("flipped"),
            )
        )
        bars.append(("push on the subject, items it did not switch", tr_b.get("kept")))
        rows_a = state_rows(states, fam, kind="push", dir="lens", layer=la_s, scale=sc_s, subset="a")
        bars.append(
            (
                "push on the whole question (the tested push)",
                mean_ci(
                    [statistics.mean([t[0] for t in r_["transit"] if t[0] is not None] or [math.nan]) for r_ in rows_a]
                ),
            )
        )
        bars.append(
            (
                "random push on the subject (same size)",
                mean_ci(
                    [statistics.mean([t[0] for t in r_["transit"] if t[0] is not None] or [math.nan]) for r_ in rnd]
                ),
            )
        )
        ed = state_rows(states, fam, kind="edit")
        for e in ("E-name", "E-insert", "E-head", "E-unrelated"):
            vals = [
                statistics.mean([t[0] for t in r_["transit"] if t[0] is not None] or [math.nan])
                for r_ in ed
                if r_["edit"] == e
            ]
            if vals:
                bars.append((EDIT_WORDS[e], mean_ci(vals)))
        ys = np.arange(len(bars))[::-1]
        for y, (_, ci) in zip(ys, bars, strict=True):
            if ci and not math.isnan(ci[0]):
                ax.barh(y, ci[0], height=0.62, color=BAR, zorder=2)
                if not math.isnan(ci[1]):
                    ax.errorbar(
                        ci[0],
                        y,
                        xerr=err(np.array([ci])),
                        color=PL.INK,
                        elinewidth=0.9,
                        capsize=0,
                        zorder=3,
                    )
                ax.text(max(ci[0], 0) + 0.03, y + 0.3, f"{ci[0]:.2f}", va="center", fontsize=7.5, color=PL.INK)
        ax.set_yticks(ys, [b_[0] for b_ in bars], fontsize=8, color=PL.INK)
        ax.axvline(1, color=PL.MUTED, ls=":", lw=1)
        ax.set_xlim(-0.1, 1.1)
        ax.set_xlabel(
            f"projection on the alt prompt's change, layers {cfg['transit'][0]}-{cfg['transit'][-1]}",
            fontsize=9,
            color=PL.MUTED,
        )
    explain = [
        ("What we did", f"Pushed only the subject phrase (lens push bridge alt − bridge org, layer {la_s}, {sc_s:g}x) and "
                        "compared how the last tokens change at later layers with how each prompt edit changes them."),
        ("Example", example_line(cases)),
        ("How to read", "Left: cosine between the push's change and an edit's change at the last tokens (pushed vectors "
                        "removed); higher = more alike. Right: projection on the alt prompt's own change at layers "
                        f"{cfg['transit'][0]}-{cfg['transit'][-1]}, where the patch from the alt prompt switches the answer; "
                        "1 = moves like the alt prompt."),
        ("Control", "Dotted lines and the 'random push' bar: a random push of the same size; they should be near 0."),
    ]  # fmt: skip
    note = f"Qwen3.6-27B; {n_of.get('RL', 0)} items per family; item-bootstrap 95% CI."
    handles = [
        Line2D([], [], color=EDIT_COLOURS[e], lw=2, marker="o", label=f"push vs '{EDIT_WORDS[e]}'") for e in EDITS
    ]
    handles.append(
        Line2D([], [], color=PL.MUTED, ls=":", label="control: random push vs the same edit (dotted, its colour)")
    )
    save(
        fig,
        "fig4_downstream_states",
        "Do later layers after the push look like a word edit or like the alt prompt?",
        explain,
        note,
        handles,
        ncols=3,
    )

    # 5. collateral: plain-text loss and the off-path prompt
    fig, axes = plt.subplots(1, 2, figsize=(15, 4.8))
    ax = axes[0]
    PL.style_axes(ax)
    ramp = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", PL.INK]
    sc = np.array(cfg["scales"], float)
    nll = tl.get("mean_nll", {})
    for colour, k_ in zip(ramp, keys, strict=False):
        lab = "all 4 layers" if k_ == "band" else f"layer {k_}"
        ax.plot(sc, [nll.get(f"lens/{k_}/x{s:g}", math.nan) for s in cfg["scales"]], color=colour, lw=2, marker="o",
                ms=5, label=f"lens push, {lab}")  # fmt: skip
        ax.plot(sc, [nll.get(f"random/{k_}/x{s:g}", math.nan) for s in cfg["scales"]], color=colour, lw=1.2, ls="--",
                marker="o", mfc=PL.SURFACE, ms=4, label=f"control: random push, {lab}")  # fmt: skip
    ax.axhline(nll.get("none", math.nan), color=PL.MUTED, lw=1, label="no push")
    ax.set_xscale("log", base=2)
    ax.set_xticks(sc, [f"{s:g}x" for s in sc])
    ax.set_xlim(sc[0] * 0.85, sc[-1] * 1.2)
    ax.set_ylabel("next-token loss on WikiText (nats)", fontsize=9, color=PL.INK)
    ax.set_xlabel("push size per token (x the size of the alt-prompt patch)", fontsize=9, color=PL.MUTED)
    ax.set_title("plain text under the push", fontsize=9.5, color=PL.INK, loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", ncols=2)
    ax = axes[1]
    PL.style_axes(ax)
    PL.percent_axis(ax)
    groups = [(fam, s) for fam in ("RL", "BL") if fam in idx for s in cfg["scales"]]
    xg = np.arange(len(groups))
    bottom = np.zeros(len(groups))
    for role_name, words in (
        ("A", "answer org kept"),
        ("bO", "answer alt of this prompt"),
        ("b", "answer alt of the org prompt"),
        ("other", "anything else"),
    ):
        vals = []
        for fam, s in groups:
            cell = idx[fam].get(push_key(la_s, s, "a", prompt="off"), {})
            roles = [o["role"] for o in cell.values()]
            vals.append(
                sum((r == role_name) if role_name != "other" else r in ("other", "oc") for r in roles)
                / max(1, len(roles))
            )
        ax.bar(
            xg,
            vals,
            bottom=bottom,
            color=ROLE_COLOURS[role_name],
            width=0.7,
            edgecolor=PL.SURFACE,
            linewidth=2,
            label=words,
        )
        bottom += np.array(vals)
    ax.set_xticks(xg, [f"{PL.family_label(fam).replace(' → ', ' →\n')}\n{s:g}x" for fam, s in groups], fontsize=8)
    ax.set_ylabel("share of off-path controls", fontsize=9, color=PL.INK)
    ax.set_title(
        f"lens push on the whole question, layer {la_s}, applied to the off-path control",
        fontsize=9.5,
        color=PL.INK,
        loc="left",
    )
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    explain = [
        ("What we did", "Left: the same lens pushes on plain WikiText, on every token from the 5th (harsher than the ~25 "
                        f"question tokens pushed above). Right: the push on the whole question at layer {la_s}, applied to "
                        "the off-path control."),
        ("Example", example_line(cases, off=True)),
        ("How to read", "Left: next-token loss, lower = text still predicted well. Right: what the off-path control "
                        "answers; taking its own answer alt means the push acts before the locker lookup, not on the "
                        "output digit."),
        ("Control", "Dashed lines: a random push of the same size; it should stay near the 'no push' line."),
    ]  # fmt: skip
    note = (f"Qwen3.6-27B; {tl.get('n_texts', '?')} WikiText rows x {len(tl.get('pairs', []))} (bridge org, bridge alt) "
            f"pairs, no intervals (per-row losses were not saved); {n_of.get('RL', 0)} off-path controls per family.")  # fmt: skip
    save(fig, "fig5_collateral", "What else does the push break?", explain, note)

    summary ={"run": name, "P*": p_star, "P*_b": pb_key, "verdict": sm["verdict"], "calls": sm["calls"], "K3": sm.get("K3"),
               "families": {f: {k_: v for k_, v in fs.items() if k_ != "cells"} for f, fs in sm["families"].items()},
               "post_hoc": post, "textloss": tl.get("mean_nll"), "figures": figs,
               "rates": {f: {"|".join(map(str, k_)): wilson_of(c_) for k_, c_ in idx[f].items()} for f in idx}}  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "examples", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--n", type=int, default=DEFAULTS["n"], help="cases per family (a smoke run: few)")
    ap.add_argument("--families", nargs="*", default=DEFAULTS["families"])
    ap.add_argument("--no-countries", action="store_true")
    ap.add_argument("--map", default=DEFAULTS["map"])
    ap.add_argument("--country-map", default=DEFAULTS["country_map"])
    ap.add_argument("--wording", default=DEFAULTS["wording"], choices=["A", "B"])
    for key in ("layers", "write_layers", "down", "transit"):
        ap.add_argument("--" + key.replace("_", "-"), nargs="+", type=int, default=DEFAULTS[key])
    ap.add_argument("--scales", nargs="+", type=float, default=DEFAULTS["scales"])
    ap.add_argument("--embed-scales", nargs="+", type=float, default=DEFAULTS["embed_scales"])
    ap.add_argument("--textloss-pairs", type=int, default=DEFAULTS["textloss_pairs"])
    ap.add_argument("--k", type=int, default=3, help="examples: per outcome group")
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        config = {"n": args.n, "families": args.families, "countries": not args.no_countries, "map": args.map,
                  "country_map": args.country_map, "wording": args.wording, "layers": args.layers,
                  "scales": args.scales, "embed_scales": args.embed_scales, "write_layers": args.write_layers,
                  "down": args.down, "transit": args.transit, "textloss_pairs": args.textloss_pairs}  # fmt: skip
        stage_run(args.name, args.why, config)
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
