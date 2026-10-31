"""nn_provenance (prereg amendment 63, note 34): the provenance probe on jsuite_v5kc2. GPU part: residuals, monitor views, Z, the
claim read's top-20 dump. The probes and the readings are scripts/nn_provenance_read.py (CPU).

Items. CN and DN (plain question, conflict passage), labelled from the model's existing competence run as
nn_v5_read.kc labels them (memory: the unedited answer matches X's real value; passage: X's false value; other: dropped).
TN and TD (X's claim true) are read for the claim read only. Every item is rendered as nn_readout --items v4all renders it
(nn_swap.build_prompt).
Sites (token positions, found by the tokenizer's character offsets in the rendered prompt):
  s1  X in the question: named, the last token of X's name in the question; described, the description's last token there
      (the same token as nn_readout's desc_end; checked by --check)
  s2  the last token of X's passage value in its claim sentence ("The club's notes say X was V."): X's false value on CN /
      DN, its true value on TN / TD (the claim read's "same position")
  s3  the final prompt token
Layers: the band and every 4th lens layer from 0 (block outputs, as nn_readout).
Per probe item (CN / DN labelled), site and layer:
  h      the residual, fp16 (F, the full state)
  J      h's coordinates in an orthonormal basis of the span of the J++ vectors ((g * W_U[t]) @ J_l, lens.vectors) of the
         first tokens of every value of the item's relation's answer_vocab (each value's first token with and without a
         leading space, as nn_readout's candidate reads; deduplicated): m_rel dimensions. The basis is the QR of the vectors
         in vocabulary order with a positive diagonal, so coordinate k follows the same token at every layer.
  R      h's coordinates on the first m_rel columns of rotation(d, 888 + layer) (the repo's seeded rotation)
  U      h's coordinates in an orthonormal basis of the span of the same tokens' unembedding rows, the final norm's gain
         folded in (the logit lens's directions, as unembed10)
  Jall / Rall / Uall   the same over the union of all four relations' tokens (one basis for every item; a beside-check of
         the reader's block layout, not pre-registered)
  Z      the J++ logit (lens.readout) of X's true value minus its false value's (each value's best first token)
Amendment 63 addendum (time course): at s3 and every lens layer, the rank of X's true value and of its false value among
the relation's values by the J++ lens (each value scored by its best first token, as nn_readout; a tie counts against the
value), so the reader finds the first layer where the item's eventual answer is the lens's top-1 (s3_ranks.pt).
The memory-strength baseline B (the addendum's "answer margin"): one closed-book forward per scene over the kc2ctl set's H2
item ("Which nationality was X?", no passage), rendered exactly as competence_variants renders it (its prompt(), variant
"none"); at the final position, the cand2 margin: the best logit among X's true value's first tokens (cand2's ok2, either
case) minus the best among the other candidates (cand2's candidates: every value of the relation, either case). The
controls run records only correctness, so this script computes the margin (h2_margin.jsonl; index.jsonl's h2_margin). The
controls run's correct_cand2 is kept beside it (h2_correct), and this forward's own cand2 pick is checked against it.
Claim read (every CN, DN, TN, TD item): the J++ top-20 over letter tokens (note 26's letters filter; nn_readout --topk's
top_letters) at s2, at every layer read. The 25 control tokens: letter tokens drawn with random.Random(34) (none on the
fixed list after note 26's normalisation, distinct).

Writes results/nn_provenance/<name>/: manifest.json, index.jsonl (probe rows), site_s1.pt / site_s2.pt / site_s3.pt,
s3_ranks.pt, h2_margin.jsonl, claim_index.jsonl, claim_top20.pt, claim_vocab.json, summary.json (last).
Run with the repo's .env sourced (set -a; . ./.env; set +a), as the queues do (the HF cache location).

python scripts/nn_provenance.py --name N --why W --band 12-16 --competence C [--set jsuite_v5kc2_test_chat] [--limit 0]
       [--batch 8] [--check]
--check: no model; build prompts and sites, print counts and decoded sites for 2 items per word (CPU only).
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts.ablate_v2 import bridge_positions  # noqa: E402

RES = pins.RESULTS_DIR / "nn_provenance"
PROBE_WORDS = ("CN", "DN")
CLAIM_WORDS = ("CN", "DN", "TN", "TD")
SITES = ("s1", "s2", "s3")
EVERY = 4  # note 34: every 4th layer from 0 (descriptive)
TOPK = 20
SEED_ROT = JS.SEED_ROT  # 888 (+ layer)
SEED_CTL_TOK = 34
N_CTL_TOK = 25
CLAIM_LIST = ["false", "fake", "wrong", "incorrect", "untrue", "myth", "mistaken", "mistake", "error", "lie", "lies", "fiction",
              "fictional", "hoax", "rumor", "rumour", "misinformation", "inaccurate", "bogus", "not", "actually", "allegedly",
              "supposedly", "claimed", "claims"]  # fmt: skip  # note 34's fixed list


def fold(s: str) -> str:
    """note 26's normalisation (scripts/nn_topk_read.fold): NFKC, non-word characters stripped at both ends, casefold."""
    from scripts.nn_topk_read import fold as f

    return f(s)


def suffix(i: str) -> str:
    return i.split(":")[-1].split("-", 1)[1]


def labels_and_known(items: dict, set_name: str, competence: str, cv: str | None) -> tuple[dict, dict, dict]:
    """nn_v5_read.kc's label() (copied), known() (note 30's eligibility; recorded, not used by note 34's primary) and the
    amendment 63 addendum's B: the scene's closed-book named recall H2 right (correct_cand2; the controls run records no margin)."""
    norm = lambda x: (x or "").strip().lower()  # noqa: E731
    comp: dict = collections.defaultdict(dict)
    for line in (pins.RESULTS_DIR / "tasks_v2" / competence / "items.jsonl").open():
        r = json.loads(line)
        comp[r["id"]][r["part"]] = r

    def label(i):
        it, top = items[i], norm(comp[i]["whole"].get("read_top"))
        match = lambda v: bool(top) and bool(v) and (norm(v).startswith(top) or top.startswith(norm(v)))  # noqa: E731
        return "memory" if match(it["real"]) else "passage" if match(it.get("false_value")) else "other"

    tag = set_name.removeprefix("jsuite_").removesuffix("_test_chat")
    cvr = {}
    if cv and (pins.RESULTS_DIR / "competence_variants" / cv / "rows.jsonl").exists():
        for line in (pins.RESULTS_DIR / "competence_variants" / cv / "rows.jsonl").open():
            r = json.loads(line)
            cvr[r["id"]] = r

    def known(i):
        if not cvr:
            return None
        h2 = cvr.get(f"j3:chat:{tag}:H2-{suffix(i)}", {}).get("correct_cand2")
        h1 = cvr.get(f"j3:chat:{tag}:H1-{suffix(i)}", {}).get("correct_cand2")
        return bool(h2) and (items[i]["named"] or bool(h1))

    lab = {i: label(i) for i in items if i in comp and items[i]["word"] in PROBE_WORDS}
    kn = {i: known(i) for i in items if items[i]["word"] in CLAIM_WORDS}
    h2 = {}
    for i in items:
        if items[i]["word"] in CLAIM_WORDS and cvr:
            c = cvr.get(f"j3:chat:{tag}:H2-{suffix(i)}", {}).get("correct_cand2")
            h2[i] = None if c is None else bool(c)
    return lab, kn, h2


def last_overlap(offsets: list[tuple[int, int]], a: int, b: int) -> int:
    hits = [k for k, (s, e) in enumerate(offsets) if s < b and e > a and e > s]
    assert hits, (a, b)
    return hits[-1]


def find_sites(tok, it: dict, ids: list[int]) -> dict:
    """s1 / s2 / s3 token positions of one rendered item, from the tokenizer's character offsets."""
    text = T.render(tok, {**it, "_question": it["question"], "_kind": it["kind"]})
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    assert enc["input_ids"] == ids, f"{it['id']}: offsets tokenisation differs from build_prompt's ids"
    off = [tuple(o) for o in enc["offset_mapping"]]
    ctx, q, x = it["context"], it["question"], it["bridge"]
    cs = text.find(ctx)
    assert cs >= 0 and text.count(ctx) == 1, it["id"]
    qs = text.rfind(q)
    assert qs >= cs + len(ctx), f"{it['id']}: question not after the passage"
    target = it["start_desc"]
    assert (target == x) == bool(it["named"]), it["id"]
    k = q.rfind(target)
    if k < 0:  # case-insensitive fallback (a description starting a question in capitals)
        m = list(re.finditer(re.escape(target), q, flags=re.I))
        assert m, f"{it['id']}: {target!r} not in the question"
        k = m[-1].start()
    s1 = last_overlap(off, qs + k, qs + k + len(target))
    claim = f"say {x} "
    assert ctx.count(claim) == 1, f"{it['id']}: claim sentence of {x!r} not unique"
    ci = ctx.find(claim)
    v = it["passage_values"][x]
    vi = ctx.find(" " + v + ".", ci + len(claim) - 1)
    assert vi >= 0 and vi - ci < 80 and "." not in ctx[ci + len(claim) : vi].replace(x, ""), f"{it['id']}: value {v!r} not in X's claim"
    s2 = last_overlap(off, cs + vi + 1, cs + vi + 1 + len(v))
    s3 = len(ids) - 1
    assert s1 < s3 and s2 < s1, it["id"]
    return {"s1": s1, "s2": s2, "s3": s3, "value": v}


def value_forms(tok, v: str) -> list[int]:
    """A value's first token without and with a leading space (nn_readout's cand_rows), deduplicated, in that order."""
    out = []
    for t in (S.ids(tok, v)[0], S.ids(tok, " " + v)[0]):
        if t not in out:
            out.append(t)
    return out


def h2_prompts(tok, a, scenes: set) -> dict:
    """The amendment 63 addendum's B: the kc2ctl set's H2 item per scene, as competence_variants renders and reads it."""
    from scripts.competence_variants import prompt

    ctl_set = a.set.replace("_test_chat", "ctl_test_chat")
    out = {}
    for line in (JS.DATA / ctl_set / "items.jsonl").read_text().splitlines():
        it = json.loads(line)
        if it["word"] == "H2" and suffix(it["id"]) in scenes:
            out[suffix(it["id"])] = {"id": it["id"], "answer": it["answer"], "bridge": it["bridge"], **prompt(tok, it, "none", ctl_set)}
    return out


def build_jobs(tok, items: dict, a, lab: dict, kn: dict, h2: dict) -> list[dict]:
    from scripts.nn_swap import build_prompt

    jobs = []
    for w in CLAIM_WORDS:
        ids_w = sorted(i for i, it in items.items() if it["word"] == w)
        if a.limit:
            ids_w = ids_w[: a.limit]
        for i in ids_w:
            it = items[i]
            p = build_prompt(tok, it, a.set)
            st = find_sites(tok, it, p["ids"])
            jobs.append({"id": i, "word": w, "ids": p["ids"], "pos": [st[s] for s in SITES], "value": st["value"], "rel": it["relation"],
                         "bridge": it["bridge"], "scene": suffix(i), "named": bool(it["named"]), "real": it["real"],
                         "false": it.get("false_value"), "label": lab.get(i), "known": kn.get(i), "h2_correct": h2.get(i)})  # fmt: skip
    return jobs


def show(tok, j: dict, width: int = 5) -> str:
    out = []
    for s, p in zip(SITES, j["pos"], strict=True):
        lo, hi = max(0, p - width), min(len(j["ids"]), p + 2)
        win = "".join(("[" + tok.decode([t]) + "]") if k == p else tok.decode([t]) for k, t in zip(range(lo, hi), j["ids"][lo:hi], strict=True))
        out.append(f"    {s} pos {p:4d} token {tok.decode([j['ids'][p]])!r:16s} ...{win!r}")
    return "\n".join(out)


def check(a) -> None:
    from bridge_jspace import tokens

    tok = tokens.load_tokenizer()
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    lab, kn, h2 = labels_and_known(items, a.set, a.competence, a.cv)
    jobs = build_jobs(tok, items, a, lab, kn, h2)
    print(f"{len(jobs)} prompts; by word {dict(collections.Counter(j['word'] for j in jobs))}")
    for w in PROBE_WORDS:
        c = collections.Counter(j["label"] for j in jobs if j["word"] == w)
        ck = collections.Counter(j["label"] for j in jobs if j["word"] == w and j["known"])
        ch = collections.Counter((j["label"], j["h2_correct"]) for j in jobs if j["word"] == w)
        print(f"  {w}: labels {dict(c)}; known (note 30 eligibility, recorded only) {dict(ck)}; (label, H2 right) {dict(ch)}")
    # s1 is nn_readout's desc_end (bridge_positions over start_desc, the last position) wherever that finds the word
    agree = miss = 0
    for j in jobs:
        bp = bridge_positions(tok, j["ids"], items[j["id"]]["start_desc"])
        if not bp:
            miss += 1
        else:
            agree += bp[-1] == j["pos"][0]
    print(f"s1 == nn_readout's desc_end on {agree} of {len(jobs) - miss} prompts ({miss} where bridge_positions finds nothing)")
    hp = h2_prompts(tok, a, {j["scene"] for j in jobs})
    ex = hp[jobs[0]["scene"]]
    print(f"B: {len(hp)} closed-book H2 prompts for {len({j['scene'] for j in jobs})} scenes; e.g. {ex['id']} (answer {ex['answer']!r}, "
          f"{len(ex['cands2'])} cand2 tokens, ok2 {[tok.decode([t]) for t in ex['ok2']]}): ...{tok.decode(ex['ids'][-24:])!r}")
    assert all(hp[j["scene"]]["answer"] == items[j["id"]]["real"] and hp[j["scene"]]["bridge"] == j["bridge"] for j in jobs)
    dec = lambda j, s: tok.decode([j["ids"][j["pos"][SITES.index(s)]]])  # noqa: E731
    for s in SITES:
        print(f"  {s} decoded tokens, most common: {collections.Counter(dec(j, s) for j in jobs).most_common(8)}")
    # s2's token should end X's passage value
    bad2 = [j["id"] for j in jobs if not dec(j, "s2").strip() or not j["value"].endswith(dec(j, "s2").strip())]
    bad1 = [j["id"] for j in jobs if not dec(j, "s1").strip() or not items[j["id"]]["start_desc"].endswith(dec(j, "s1").strip())]
    print(f"  s1 token not the end of X's name / description: {len(bad1)} {bad1[:5]}; s2 token not the end of the value: {len(bad2)} {bad2[:5]}")
    print(f"  s2 value is X's false value on every CN / DN item: {all(j['value'] == j['false'] for j in jobs if j['word'] in PROBE_WORDS)}; "
          f"X's true value on every TN / TD item: {all(j['value'] == j['real'] for j in jobs if j['word'] not in PROBE_WORDS)}")
    for w in CLAIM_WORDS:
        for j in [j for j in jobs if j["word"] == w][:2]:
            it = items[j["id"]]
            print(f"--- {j['id']} {w} label {j['label']} | Q: {it['question']!r} | value in claim {j['value']!r} (real {it['real']!r}, false {it.get('false_value')!r})")
            print(show(tok, j))


@torch.no_grad()
def main(a) -> None:
    from bridge_jspace.ablate import rotation
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import _forward_hooks, load_model

    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    t0 = time.time()
    model = load_model()
    tok = model.tokenizer
    t_load = time.time() - t0
    lens = JLens(model, pins.FROZEN_LENS)
    src = sorted(int(x) for x in lens.source_layers)
    band = list(range(int(a.band.split("-")[0]), int(a.band.split("-")[1]) + 1))
    assert all(la in src for la in band), f"band {band} outside the lens's layers"
    layers = sorted(set(band) | {la for la in src if la % EVERY == 0})
    hooked = src  # every lens layer: the s3 time course (amendment 63 addendum); features only at `layers`
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    lab, kn, h2 = labels_and_known(items, a.set, a.competence, a.cv)
    jobs = build_jobs(tok, items, a, lab, kn, h2)
    probe = [j for j in jobs if j["word"] in PROBE_WORDS and j["label"] in ("memory", "passage")]
    for r, j in enumerate(probe):
        j["row"] = r
    for r, j in enumerate(jobs):
        j["crow"] = r
    print(f"{len(jobs)} prompts {dict(collections.Counter(j['word'] for j in jobs))}; {len(probe)} probe items "
          f"{dict(collections.Counter((j['word'], j['label']) for j in probe))}; layers {layers}; band {band}", flush=True)  # fmt: skip

    # the bases: per relation and the union, at every layer read
    W, g = model.hf.lm_head.weight, model.norm_gain()
    d = W.shape[1]
    rels = sorted({it["relation"] for it in items.values()})
    forms = {}
    for r in rels:
        vocab = next(it["answer_vocab"] for it in items.values() if it["relation"] == r)
        assert all(it["answer_vocab"] == vocab for it in items.values() if it["relation"] == r)
        fs: list[int] = []
        for v in vocab:
            fs += [t for t in value_forms(tok, v) if t not in fs]
        forms[r] = fs
    union: list[int] = []
    for r in rels:
        union += [t for t in forms[r] if t not in union]
    m = {r: len(forms[r]) for r in rels}
    m_max, M = max(m.values()), len(union)
    # the time course's candidates: each relation's values, each scored by its best first token (nn_readout's cand_rows)
    vals = {r: next(it["answer_vocab"] for it in items.values() if it["relation"] == r) for r in rels}
    vforms = {r: [value_forms(tok, v) for v in vals[r]] for r in rels}
    ctoks = {r: torch.tensor(sorted({t for f in vforms[r] for t in f}), device="cuda") for r in rels}
    cidx = {}
    for r in rels:
        pos = {t: k for k, t in enumerate(ctoks[r].tolist())}
        width = max(len(f) for f in vforms[r])
        cidx[r] = torch.tensor([[pos[t] for t in f] + [pos[f[0]]] * (width - len(f)) for f in vforms[r]], device="cuda")
    cW = {r: W[ctoks[r]].float() * g for r in rels}

    def ortho(V: torch.Tensor) -> tuple[torch.Tensor, float]:
        """[k, d] -> an orthonormal basis [d, k] of the rows' span (QR in row order, positive diagonal), and the rows' condition number."""
        Q, R = torch.linalg.qr(V.double().T)
        Q = Q * torch.sign(torch.diagonal(R))
        sv = torch.linalg.svdvals(V.double())
        return Q.float(), float(sv[0] / sv[-1])

    QJ, QR_, QJall, QRall, cond = {}, {}, {}, {}, collections.defaultdict(dict)
    for la in layers:
        for r in rels:
            QJ[(r, la)], cond[r][la] = ortho(lens.vectors(la, torch.tensor(forms[r], device="cuda"), unit=False))
        QJall[la], cond["union"][la] = ortho(lens.vectors(la, torch.tensor(union, device="cuda"), unit=False))
        rot = rotation(d, SEED_ROT + la)  # the repo's seeded rotation; its first m columns are the random m-subspace
        for r in rels:
            QR_[(r, la)] = rot[:, : m[r]].clone()
        QRall[la] = rot[:, :M].clone()
        del rot
    QU, condU = {}, {}
    for r in rels:
        QU[r], condU[r] = ortho(W[torch.tensor(forms[r], device="cuda")].float() * g)
    QUall, condU["union"] = ortho(W[torch.tensor(union, device="cuda")].float() * g)
    worst = max(c for r in cond for c in cond[r].values())
    print(f"bases: m per relation {m}, union {M}; worst J++ condition number {worst:.3g}; unembedding {max(condU.values()):.3g}; "
          f"{time.time() - t0:.0f}s", flush=True)  # fmt: skip
    assert worst < 1e7 and max(condU.values()) < 1e7, "a near-degenerate token basis"

    # the claim read's control tokens: 25 letter tokens, random.Random(34), none on the list (note 26's fold), distinct
    letters = model.letter_token_ids()
    wg = W[letters].float() * g
    pool = letters.tolist()
    random.Random(SEED_CTL_TOK).shuffle(pool)
    ctl, seen = [], set(CLAIM_LIST)
    for t in pool:
        f = fold(model.decoded[t])
        if f and f not in seen:
            ctl.append({"id": t, "decoded": model.decoded[t], "fold": f})
            seen.add(f)
        if len(ctl) == N_CTL_TOK:
            break

    (out_dir / "manifest.json").write_text(json.dumps({
        "run": a.name, "why": a.why, "note": "prereg amendment 63 note 34 (the provenance probe)", "target": pins.TARGET,
        "model": pins.model_pin(), "lens": pins.FROZEN_LENS, "set": a.set, "competence": a.competence, "cv": a.cv,
        "band": band, "layers": layers, "time_course_layers": hooked, "every": EVERY, "sites": SITES, "limit": a.limit, "batch": a.batch,
        "probe_words": PROBE_WORDS, "claim_words": CLAIM_WORDS, "topk": TOPK, "claim_list": CLAIM_LIST,
        "control_tokens": ctl, "control_seed": SEED_CTL_TOK, "rotation_seed": f"{SEED_ROT}+layer", "relations": rels,
        "forms": {r: [[t, tok.decode([t])] for t in forms[r]] for r in rels}, "m": m, "union_m": M,
        "condition_J": {r: {str(la): round(c, 1) for la, c in v.items()} for r, v in cond.items()},
        "condition_U": {r: round(c, 1) for r, c in condU.items()},
        "command": "python " + " ".join(sys.argv), "git_commit": commit, "git_state": pins.git_state()}, indent=1) + "\n")  # fmt: skip

    L = len(layers)
    li_of = {la: k for k, la in enumerate(layers)}
    n = len(probe)
    H = torch.zeros(n, 3, L, d, dtype=torch.float16)
    C = {k: torch.zeros(n, 3, L, m_max) for k in ("J", "R", "U")}
    Call = {k: torch.zeros(n, 3, L, M) for k in ("Jall", "Rall", "Uall")}
    Z = torch.full((n, 3, L), float("nan"))
    RK = torch.zeros(n, 2, len(hooked), dtype=torch.int16)  # s3: rank of X's true value, of its false value, every lens layer
    TOP = torch.zeros(len(jobs), L, TOPK, dtype=torch.int32)
    overflow, maxabs = 0, 0.0
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    t1, done = time.time(), 0
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            B = len(chunk)
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            bi = torch.arange(B, device="cuda").repeat_interleave(3)
            pi = torch.tensor([p for j in chunk for p in j["pos"]], device="cuda")
            rec = {}

            def hook_for(la):
                def hook(_m, _a, out):
                    h = out[0] if isinstance(out, tuple) else out
                    rec[la] = h[bi, pi].float().reshape(B, 3, -1)

                return hook

            with _forward_hooks([(model.layers[la], hook_for(la)) for la in hooked]):
                model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
            pb = [b for b, j in enumerate(chunk) if "row" in j]
            rows = torch.tensor([chunk[b]["row"] for b in pb], dtype=torch.long)
            for hk, la in enumerate(hooked):  # the time course at s3 (probe items)
                for r in rels:
                    sel = [b for b in pb if chunk[b]["rel"] == r]
                    if not sel:
                        continue
                    sc = (rec[la][sel, 2] @ lens.J(la).T) @ cW[r].T  # [b, tokens]
                    v = sc[:, cidx[r]].max(-1).values  # [b, values]
                    ti = torch.tensor([vals[r].index(chunk[b]["real"]) for b in sel], device="cuda")
                    fi = torch.tensor([vals[r].index(chunk[b]["false"]) for b in sel], device="cuda")
                    ar = torch.arange(len(sel), device="cuda")
                    rt = (v >= v[ar, ti][:, None]).sum(-1)  # conservative: a tie counts against the value
                    rf = (v >= v[ar, fi][:, None]).sum(-1)
                    rr = torch.tensor([chunk[b]["row"] for b in sel], dtype=torch.long)
                    RK[rr, 0, hk] = rt.short().cpu()
                    RK[rr, 1, hk] = rf.short().cpu()
            for la in layers:
                X = rec[la]  # [B, 3, d]
                li = li_of[la]
                Jl = lens.J(la)
                lg = (X[:, 1] @ Jl.T) @ wg.T  # the claim read at s2: J++ over letter tokens (nn_readout's top_letters)
                TOP[[j["crow"] for j in chunk], li] = letters[lg.topk(TOPK, dim=-1).indices].int().cpu()
                if not pb:
                    continue
                Xp = X[pb]  # [b, 3, d]
                big = Xp.abs().max().item()
                maxabs = max(maxabs, big)
                overflow += int((Xp.abs() > 65504).sum())
                H[rows, :, li] = Xp.half().cpu()
                for r in rels:
                    sel = [k for k, b in enumerate(pb) if chunk[b]["rel"] == r]
                    if not sel:
                        continue
                    xs, rr = Xp[sel], rows[sel]
                    C["J"][rr, :, li, : m[r]] = (xs @ QJ[(r, la)]).cpu()
                    C["R"][rr, :, li, : m[r]] = (xs @ QR_[(r, la)]).cpu()
                    C["U"][rr, :, li, : m[r]] = (xs @ QU[r]).cpu()
                Call["Jall"][rows, :, li] = (Xp @ QJall[la]).cpu()
                Call["Rall"][rows, :, li] = (Xp @ QRall[la]).cpu()
                Call["Uall"][rows, :, li] = (Xp @ QUall).cpu()
                logits = lens.readout(Xp.reshape(-1, d), la).reshape(len(pb), 3, -1)  # the J++ logits
                for k, b in enumerate(pb):
                    j = chunk[b]
                    tf, ff = value_forms(tok, j["real"]), value_forms(tok, j["false"])
                    Z[rows[k], :, li] = (logits[k][:, tf].max(-1).values - logits[k][:, ff].max(-1).values).cpu()
            done += B
        print(f"{done}/{len(jobs)} prompts, {time.time() - t1:.0f}s", flush=True)
    t_fwd = time.time() - t1

    # B: the closed-book named recall's cand2 margin, one forward per scene
    t2 = time.time()
    hp = h2_prompts(tok, a, {j["scene"] for j in jobs})
    assert all(hp[j["scene"]]["answer"] == j["real"] and hp[j["scene"]]["bridge"] == j["bridge"] for j in jobs)
    cv_ok = {j["scene"]: j["h2_correct"] for j in jobs}  # the controls run's correct_cand2 per scene
    h2m, by_len = {}, collections.defaultdict(list)
    for sc, p in hp.items():
        by_len[len(p["ids"])].append(sc)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([hp[sc]["ids"] for sc in chunk], device="cuda")
            lg = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1).logits[:, -1].float()
            for b, sc in enumerate(chunk):
                p = hp[sc]
                ok, other = sorted(set(p["ok2"])), sorted(set(p["cands2"]) - set(p["ok2"]))
                c2 = torch.tensor(p["cands2"], device="cuda")
                pick2 = int(c2[lg[b][c2].argmax()])
                h2m[sc] = {"scene": sc, "id": p["id"], "margin": round(float(lg[b][ok].max() - lg[b][other].max()), 4),
                           "correct_cand2_here": pick2 in p["ok2"], "pick2": pick2,
                           "correct_cand2_cv": cv_ok.get(sc)}  # fmt: skip
    t_h2 = time.time() - t2
    for j in jobs:
        j["h2_margin"] = h2m[j["scene"]]["margin"]
    (out_dir / "h2_margin.jsonl").write_text("".join(json.dumps(v) + "\n" for _, v in sorted(h2m.items())))
    agree = sum(v["correct_cand2_here"] == v["correct_cand2_cv"] for v in h2m.values() if v["correct_cand2_cv"] is not None)
    n_cv = sum(v["correct_cand2_cv"] is not None for v in h2m.values())
    print(f"B: {len(h2m)} closed-book H2 margins, {t_h2:.0f}s; cand2 correctness agrees with the controls run on {agree} of {n_cv} scenes", flush=True)

    for si, s in enumerate(SITES):
        torch.save({"layers": layers, "band": band, "site": s, "m": m, "relations": rels, "h": H[:, si].clone(),
                    **{k: v[:, si].clone() for k, v in C.items()}, **{k: v[:, si].clone() for k, v in Call.items()}, "Z": Z[:, si].clone()},
                   out_dir / f"site_{s}.pt")  # fmt: skip
    (out_dir / "index.jsonl").write_text("".join(json.dumps({k: j[k] for k in ("row", "id", "word", "named", "rel", "bridge", "scene", "label", "known", "h2_correct", "h2_margin", "real", "false", "value")}
                                                            | {"pos": dict(zip(SITES, j["pos"], strict=True)), "tok": {s: tok.decode([j["ids"][p]]) for s, p in zip(SITES, j["pos"], strict=True)},
                                                               "m": m[j["rel"]], "n_tokens": len(j["ids"])}) + "\n" for j in probe))  # fmt: skip
    torch.save({"layers": hooked, "rank_true": RK[:, 0].clone(), "rank_false": RK[:, 1].clone(), "n_values": {r: len(vals[r]) for r in rels}}, out_dir / "s3_ranks.pt")
    torch.save({"layers": layers, "band": band, "top": TOP}, out_dir / "claim_top20.pt")
    (out_dir / "claim_index.jsonl").write_text("".join(json.dumps({"crow": j["crow"], "id": j["id"], "word": j["word"], "scene": j["scene"], "rel": j["rel"],
                                                                   "bridge": j["bridge"], "named": j["named"], "label": j["label"], "known": j["known"],
                                                                   "value": j["value"], "s2": j["pos"][1], "s2_tok": tok.decode([j["ids"][j["pos"][1]]])}) + "\n" for j in jobs))  # fmt: skip
    used = sorted(set(TOP.flatten().tolist()))
    (out_dir / "claim_vocab.json").write_text(json.dumps({str(t): model.decoded[t] for t in used}, ensure_ascii=False) + "\n")
    summ = {"n_prompts": len(jobs), "n_by_word": dict(collections.Counter(j["word"] for j in jobs)), "n_probe": n,
            "n_probe_by_word_label": {f"{w}/{lb}": c for (w, lb), c in sorted(collections.Counter((j["word"], j["label"]) for j in probe).items())},
            "n_dropped_other": sum(1 for j in jobs if j["word"] in PROBE_WORDS and j["label"] == "other"),
            "n_unlabelled": sum(1 for j in jobs if j["word"] in PROBE_WORDS and j["label"] is None),
            "layers": layers, "band": band, "m": m, "union_m": M, "fp16_overflow": overflow, "max_abs_h": round(maxabs, 1),
            "seconds": {"load": round(t_load), "forward_and_features": round(t_fwd), "h2_margin": round(t_h2), "total": round(time.time() - t0)},
            "B": {"definition": "the closed-book named recall's (kc2ctl H2) cand2 answer margin, computed by this script (one forward per scene, "
                                "rendered by competence_variants.prompt, variant none): best logit of X's true value's first tokens (ok2) minus "
                                "the best other cand2 candidate's, at the final position; the controls run records no margin",
                  "n_scenes": len(h2m), "cand2_correct_agrees_with_controls_run": f"{agree} of {n_cv}"},
            "seeds": {"rotation": f"{SEED_ROT}+layer", "control_tokens": SEED_CTL_TOK}, "deterministic": "one forward per prompt, no sampling",
            "command": "python " + " ".join(sys.argv), "git_commit": commit}  # fmt: skip
    assert overflow == 0, f"{overflow} residual entries overflow fp16"
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v5kc2_test_chat")
    ap.add_argument("--cv", default=None, help="the competence_variants run for note 30's eligibility (default: derived from --competence)")
    ap.add_argument("--limit", type=int, default=0, help="first N items per word (a smoke)")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--check", action="store_true", help="CPU only: prompts, sites and counts, no model")
    args = ap.parse_args()
    if args.cv is None:
        pre = args.competence[: args.competence.index(args.set)] if args.set in args.competence else ""
        args.cv = f"{pre}jsuite_{args.set.removeprefix('jsuite_').removesuffix('_test_chat')}ctl_cv_v1"
    check(args) if args.check else main(args)
