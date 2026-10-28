"""nn_swap (Zach, 2026-10-28, prereg amendment 58 note 9): does a never-named bridge act as a workspace entity?

Items (jsuite v3, rendering 0, the model's v3 competence and note 4's eligibility): never-named RM (the question
describes the bridge, "the novelist who wrote Arrow of God"; the passage never names it), with references: MM (the same
kind of description, the bridge also named once in passing) and PM (named; edited at its mention, as jswap).
Site: RM / MM, the last token of the description in the question (--site last) or every description token (--site
span); PM, the last token of each mention of the bridge X. --site qmark: the question's "?" token; --site final: the
prompt's last token (both for every word; exp11 / exp14 read latent bridges at the last token from mid-late layers).
Donor D: another bridge of X's relation with a different answer, an eligible RM prompt of its own, and a name token
different from X's (many names share a first token; the clamp needs distinct name directions); seeded per item;
third: a random other answer of the relation (the chance of landing on any one answer).
Donor vectors, at every band layer:
  insert   D's residual at its last token in jswap_pointer's neutral sentence ("A reader asked a question about D ...")
  latent   D's residual at the last token of D's description in one of D's own eligible RM prompts (a computed bridge)
Conditions (k: the top-k J++ span by the lens's logits at each side, never one of the clean answer position's top-10, as
jswap):
  {src}_k{k}        h_X - Jk(h_X) + Jk(h_D)
  {src}_k{k}_rot    h_X + (Jk(h_D) - Jk(h_X)) R^T   (the same-size change in a fixed random direction)
  {src}_k{k}_rand   the transplant over a fixed random k-dim subspace: h_X - P h_X + P h_D
  {src}_k{k}_u      the transplant over the logit lens's top-k
  clamp             the paper's clamp (Gurnee et al. 2026; bridge_jspace.clamp.SwapClamp), at every position from 1: the
                    coordinates on X's and D's unit J-lens name vectors exchanged (clean coordinates, swapped), the rest
                    of the residual unchanged
  clamp_null        the clamp's edit, norm-matched, along a fixed random unit direction
  remove_k{k}       (note 9 addendum, necessity) h_X - Jk(h_X) at the site, no donor; remove_k{k}_rot: h_X - Jk(h_X) R^T
  note 10, the paper's decomposition of the patch D = h_D - h_X over S = the union of X's and D's top-10 J++ atoms:
  full_{src}        h_D (the whole patch)
  lens_{src}        h_X + P_S D            (the lens part only)
  rem_{src}         h_X + D - P_S D        (the remainder only)
  remfix_{src}      h_D - P_S h_D + P_S h_X_clean   (the remainder, the site's lens part held at its clean value)
  lensrand_{src}    h_X + P_R D, R a fixed random 20-dim subspace (control)
Answers: the cand2 read among the relation's answers, classed kept (X's) / donor (D's) / third / other; transfer = donor
- third, 95% bootstrap over bridges (jswap.score), per word.

python scripts/nn_swap.py --name N --why W --band 12-16 --competence C [--words RM MM PM] [--site last|span]
       [--ks 10] [--conds ...] [--sweep 4-8 8-12 ...] [--sample-per-word 0] [--batch 8] [--limit 0]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.ablate import LensDictionary, rotation, top_span_removal  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts.ablate_v2 import bridge_positions  # noqa: E402
from scripts.jswap_pointer import NEUTRAL  # noqa: E402

RES = pins.RESULTS_DIR / "nn_swap"
SEED_RAND = 5800  # + layer: the random k-dim subspaces
SEED_NULL = 5900  # + layer: clamp_null's direction


def conds_for(ks: list[int]) -> list[str]:
    """Note 9: at k 10 every control; at the other k, the transplant and its random-subspace control."""
    out = []
    for k in ks:
        for src in ("insert", "latent"):
            out += [f"{src}_k{k}", f"{src}_k{k}_rand"] + ([f"{src}_k{k}_rot", f"{src}_k{k}_u"] if k == 10 else [])
    return [*out, "clamp", "clamp_null"]


def name_token(model, tok, name: str) -> int:
    try:
        return model.concept_token(name)
    except ValueError:
        return S.ids(tok, " " + name)[0]


@torch.no_grad()
def run_band(a, model, tok, lens, items, jobs, band: list[int], conds: list[str], tag: str, rows: list, t0: float) -> None:
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    d = wg.shape[1]
    rot = {la: rotation(d, JS.SEED_ROT + la) for la in band}
    rand = {la: rotation(d, SEED_RAND + la) for la in band}  # first k columns: an orthonormal random k-subspace
    null = {la: rotation(d, SEED_NULL + la)[:, 0] for la in band}

    def forward(ids, hook_fn, record=False):
        rec = {}

        def hook_for(la):
            def hook(_m, _a, out):
                h = out[0] if isinstance(out, tuple) else out
                if record:
                    rec[la] = h.float().clone()
                if hook_fn is None:
                    return None
                new = hook_fn(la, h)
                return (new, *out[1:]) if isinstance(out, tuple) else new

            return hook

        with _forward_hooks([(model.layers[la], hook_for(la)) for la in band]):
            logits = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1).logits[:, -1].float()
        return logits, rec

    # donor vectors at every band layer: neutral sentences (insert) and D's own description end (latent)
    need = {}
    for j in jobs:
        need[("insert", j["d"], j["kind_"], j["format_"])] = j["neutral"]
        need[("latent", j["lat_id"])] = (j["lat_ids"], j["lat_pos"])
    vec = {}
    by_len = collections.defaultdict(list)
    for key, (ids, _pos) in need.items():
        by_len[len(ids)].append(key)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            _, rec = forward(torch.tensor([need[k][0] for k in chunk], device="cuda"), None, record=True)
            for b, key in enumerate(chunk):
                vec[key] = torch.stack([rec[la][b, need[key][1]] for la in band])
    print(f"[{tag}] {len(vec)} donor residuals, {time.time() - t0:.0f}s", flush=True)

    def classify(lg, j):
        c2 = torch.tensor(j["cands2"], device=lg.device)
        pick = int(c2[lg[c2].argmax()])
        cls = "kept" if pick in j["ok2"] or pick in j["fx"] else "donor" if pick in j["fd"] else "third" if pick in j["ft"] else "other"
        return cls, pick

    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            clean, rec = forward(ids, None, record=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            meta = lambda j: {"x": j["x"], "donor": j["d"], "third": j["at"], "ax": j["ax"], "ad": j["ad"], "at": j["at"], "rel": j["rel"], "band": tag}  # noqa: E731
            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, **meta(j)})
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["sites"]], device="cuda")
            xi = torch.tensor([p for j in chunk for p in j["sites"]], device="cuda")
            ins = torch.stack([vec[("insert", chunk[b]["d"], chunk[b]["kind_"], chunk[b]["format_"])] for b in bi.tolist()])  # [m, L, d]
            lat = torch.stack([vec[("latent", chunk[b]["lat_id"])] for b in bi.tolist()])
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            # the clamp: X's and D's unit J-lens name vectors per item and layer; clean coordinates swapped
            clamp_atoms, clamp_pinv, clamp_tgt = {}, {}, {}
            if any(c.startswith("clamp") for c in conds):
                rows_xd = torch.tensor([[int(row_of[j["tx"]]), int(row_of[j["td"]])] for j in chunk], device="cuda")
                ok_rows = (rows_xd >= 0).all(dim=1)
                for la in band:
                    A = dic[la].atoms(rows_xd.clamp_min(0))  # [B, 2, d]
                    P = torch.linalg.pinv(A.double()).float()  # [B, d, 2]
                    c = rec[la] @ P  # [B, T, 2] clean coordinates
                    clamp_atoms[la], clamp_pinv[la], clamp_tgt[la] = A, P, c[..., [1, 0]]
            for cond in conds:

                def hook_fn(la, h, cond=cond):
                    li = band.index(la)
                    h = h.clone()
                    if cond.startswith("clamp"):
                        delta = (clamp_tgt[la] - h.float() @ clamp_pinv[la]) @ clamp_atoms[la]  # [B, T, d]
                        if cond == "clamp_null":
                            delta = delta.norm(dim=-1, keepdim=True) * null[la]
                        delta[:, 0] = 0  # position 0 (the attention sink) is never edited, as SwapClamp
                        delta[~ok_rows] = 0
                        return (h.float() + delta).to(h.dtype)
                    if cond.split("_")[0] in ("full", "lens", "rem", "remfix", "lensrand"):  # note 10: the paper's decomposition
                        kind, src = cond.split("_")
                        hx = h[bi, xi].float()
                        hd = (ins if src == "insert" else lat)[:, li]
                        if kind == "full":
                            new = hd
                        else:
                            if kind == "lensrand":  # control: a fixed random 20-dim subspace
                                Q = rand[la][:, :20][None].expand(hx.shape[0], -1, -1)
                            else:  # the union of X's and D's top-10 J++ atoms at the site (one subspace for every cell)
                                _, cx = top_span_removal(dic[la], hx, 10, protected=groups, return_chosen=True)
                                _, cd = top_span_removal(dic[la], hd, 10, protected=groups, return_chosen=True)
                                Q = torch.linalg.qr(dic[la].atoms(torch.cat([cx, cd], dim=1)).transpose(1, 2).double())[0].float()
                            proj = lambda v, Q=Q: (Q @ (Q.transpose(1, 2) @ v.unsqueeze(2))).squeeze(2)  # noqa: E731
                            if kind in ("lens", "lensrand"):
                                new = hx + proj(hd - hx)
                            elif kind == "rem":
                                new = hx + (hd - hx) - proj(hd - hx)
                            else:  # remfix: the remainder, with the site's lens part held at its clean value
                                hc = rec[la][bi, xi]
                                new = hd - proj(hd) + proj(hc)
                        h[bi, xi] = new.to(h.dtype)
                        return h
                    src, kk = cond.split("_")[0], int(cond.split("_")[1][1:])
                    hx = h[bi, xi].float()
                    if src == "remove":  # note 9 addendum: the slice erased at the site, no donor (necessity)
                        rx = top_span_removal(dic[la], hx, kk, protected=groups)
                        new = hx - rx @ rot[la].T if cond.endswith("_rot") else hx - rx
                        h[bi, xi] = new.to(h.dtype)
                        return h
                    hd = (ins if src == "insert" else lat)[:, li]
                    if cond.endswith("_rand"):
                        Q = rand[la][:, :kk]
                        new = hx - (hx @ Q) @ Q.T + (hd @ Q) @ Q.T
                    else:
                        D = unembed if cond.endswith("_u") else dic[la]
                        rx, rd = top_span_removal(D, hx, kk, protected=groups), top_span_removal(D, hd, kk, protected=groups)
                        new = hx + (rd - rx) @ rot[la].T if cond.endswith("_rot") else hx - rx + rd
                    h[bi, xi] = new.to(h.dtype)
                    return h

                lg, _ = forward(ids, hook_fn)
                for b, j in enumerate(chunk):
                    if cond.startswith("clamp") and not bool(ok_rows[b]):
                        continue
                    cls, pick = classify(lg[b], j)
                    rows.append({"id": j["id"], "family": j["family"], "condition": cond, "cls": cls, "pick": pick, **meta(j)})
        print(f"[{tag}] {len(rows)} rows, {time.time() - t0:.0f}s", flush=True)


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    bands = [list(range(int(w.split("-")[0]), int(w.split("-")[1]) + 1)) for w in (a.sweep or [a.band])]
    conds = a.conds or (["insert_k10", "insert_k10_rand"] if a.sweep else conds_for(a.ks))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "model": pins.model_pin(), "lens": pins.FROZEN_LENS,
                                                       "bands": [f"{b[0]}-{b[-1]}" for b in bands], "set": a.set, "competence": a.competence, "words": a.words,
                                                       "site": a.site, "conditions": conds, "ks": a.ks, "sample_per_word": a.sample_per_word, "limit": a.limit,
                                                       "neutral": NEUTRAL, "seeds": {"items": "random.Random(item id)", "rand": f"{SEED_RAND}+layer", "null": f"{SEED_NULL}+layer", "rot": f"{JS.SEED_ROT}+layer"},
                                                       "git_commit": commit, "git_state": pins.git_state(), "bj_gram_proj": __import__("os").environ.get("BJ_GRAM_PROJ")}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    prompts = [p for p in JS.v3_prompts(tok, a.set, a.competence, list(a.words)) if p["family"] in a.words]
    rm_by = collections.defaultdict(list)  # (relation, bridge) -> eligible RM prompts (latent donors)
    for p in prompts:
        if p["family"] == "RM":
            it = items[p["id"]]
            pos = bridge_positions(tok, p["ids"], it["start_desc"])
            if pos:
                rm_by[(it["relation"], it["bridge"])].append((p, pos[-1]))
    jobs = []
    for p in prompts:
        it = items[p["id"]]
        x, rel, kind = it["bridge"], it["relation"], it["kind"]
        t = JS.table(it)
        ans = lambda b, t=t: t["facts"][b][0]  # noqa: E731
        ax = ans(x)
        if p["family"] in ("PM", "PK") and a.site in ("last", "span"):
            sites = JS.spans(bridge_positions(tok, p["ids"], x))
        elif a.site == "final":
            sites = [len(p["ids"]) - 1]
        elif a.site == "qmark":  # the question's own "?": the last token whose text contains "?" after the description
            pieces = [tok.decode([i]) for i in p["ids"]]
            desc_end = (bridge_positions(tok, p["ids"], it["start_desc"]) or [0])[-1]
            sites = [i for i, piece in enumerate(pieces) if "?" in piece and i >= desc_end][:1]
        else:
            pos = bridge_positions(tok, p["ids"], it["start_desc"])
            sites = pos if a.site == "span" else pos[-1:]
        if not sites:
            continue
        rng = random.Random(p["id"])
        ok_name = lambda e: not (e.lower().startswith(x.lower()) or x.lower().startswith(e.lower()))  # noqa: E731
        tx = name_token(model, tok, x)  # the clamp needs distinct name directions: no donor whose name token is X's
        donors = sorted(b for (r, b) in rm_by if r == rel and b != x and ans(b) != ax and ok_name(b) and name_token(model, tok, b) != tx)
        if not donors:
            continue
        dn = rng.choice(donors)
        lat_p, lat_pos = rng.choice(rm_by[(rel, dn)])
        thirds = sorted(set(it["answer_vocab"]) - {ax, ans(dn)})
        at = rng.choice(thirds)
        text = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(dn), "question": "Has anyone else heard about this?", "kind": kind, "format": it["format"]})
        nids = S.ids(tok, text)
        npos = JS.spans(bridge_positions(tok, nids, dn))
        if not npos:
            continue
        jobs.append({**p, "x": x, "d": dn, "rel": rel, "sites": sites, "kind_": kind, "format_": it["format"], "neutral": (nids, npos[0]),
                     "lat_id": lat_p["id"], "lat_ids": lat_p["ids"], "lat_pos": lat_pos, "tx": tx, "td": name_token(model, tok, dn),
                     "fx": JS.forms(tok, ax, kind), "fd": JS.forms(tok, ans(dn), kind), "ft": JS.forms(tok, at, kind), "ax": ax, "ad": ans(dn), "at": at})  # fmt: skip
    per = collections.defaultdict(list)
    for j in jobs:
        per[j["family"]].append(j)
    if a.sample_per_word:
        jobs = [j for f in a.words for k, j in enumerate(per[f])
                if len(per[f]) <= a.sample_per_word or k in set(random.Random(f"0:{f}").sample(range(len(per[f])), a.sample_per_word))]  # fmt: skip
    if a.sample_refs:  # note 10: the reference words (all but RM) capped at N, seeded
        jobs = [j for f in a.words for k, j in enumerate(per[f])
                if f == "RM" or len(per[f]) <= a.sample_refs or k in set(random.Random(f"0:{f}").sample(range(len(per[f])), a.sample_refs))]  # fmt: skip
    if a.limit:
        jobs = [j for f in a.words for j in per[f][: a.limit]]
    print(f"{len(prompts)} eligible prompts; {len(jobs)} jobs; by word {dict(collections.Counter(j['family'] for j in jobs))}; "
          f"by relation {dict(collections.Counter(j['rel'] for j in jobs))}; bands {[f'{b[0]}-{b[-1]}' for b in bands]}; conditions {conds}", flush=True)  # fmt: skip
    lens = JLens(model, pins.FROZEN_LENS)
    rows, t0 = [], time.time()
    for band in bands:
        run_band(a, model, tok, lens, items, jobs, band, conds, f"L{band[0]}-{band[-1]}", rows, t0)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summ = {}
    for tag in sorted({r["band"] for r in rows}):
        summ.update({f"{tag}/{k}": v for k, v in JS.score([r for r in rows if r["band"] == tag]).items()})
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for k, cell in summ.items():
        if cell.get("n"):
            print(f"{k:34s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}  other {cell['other']:5.1f}"
                  f"  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", default=None)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    ap.add_argument("--words", nargs="+", default=["RM", "MM", "PM"])
    ap.add_argument("--site", choices=["last", "span", "qmark", "final"], default="last")
    ap.add_argument("--ks", nargs="+", type=int, default=[10])
    ap.add_argument("--conds", nargs="+", default=None)
    ap.add_argument("--sweep", nargs="+", default=None, help="layer windows, e.g. 4-8 8-12 (one run per window)")
    ap.add_argument("--sample-per-word", type=int, default=0)
    ap.add_argument("--sample-refs", type=int, default=0, help="note 10: cap every word but RM at N (seeded)")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    assert a.band or a.sweep, "--band or --sweep"
    main(a)
