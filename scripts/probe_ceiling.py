"""probe_ceiling (Zach, 2026-10-25, prereg amendment 48; the TA: "do more with probes, upper ceiling"): how much of a
bridge's recalled attribute is linearly present at its mention, how much of that the J++ lens reads, and whether the
probe's directions carry what the J++ part does not.

A. Readout, every --stride-th lens layer. At the last token of an entity's first mention in a facts passage, a linear
   probe per relation (multinomial logistic regression on standardised residuals, L2 chosen by entity-grouped 4-fold
   cross-validation on the train set at the band's middle layer) predicts the entity's value of the item's relation
   (pins' facts table). Train: every entity mention in jsuite_v2_dev_chat's eligible prompts (bridges and passage
   entities), never a test bridge. Test: the bridge's first mention in jsuite_v2_test_chat's eligible prompts with the
   bridge named in the passage (starts P, T) and a memory final with no statement of its value (M, N); test bridges
   share no entity with dev bridges. Beside it, on the same test items: the J++ lens's and the logit lens's pick among
   the relation's answer tokens. Chance = the most frequent test value. Test items and CV held-out items whose value no
   training entity has are left out (most relations hold one or two entities per value). A relation's probe is valid if
   its CV accuracy at the middle layer beats the held-out majority rate by VALID_MARGIN (dev data only).
B. Causal, at the band (--band), at the last token of each mention of X as jswap (amendment 32), donor D from the same
   passage: swap (J++ top-10, jswap's), swap_probe (X's part in the probe subspace replaced by D's), swap_probe_rot (the
   same-size change in a fixed random direction), remove (J++ top-10), remove_probe, paste (the ceiling). The probe
   subspace per relation and layer: the top <= 10 right singular vectors of the probe's centred class weights mapped
   back to residual units (size-matched to J++'s 10). Transfer (donor - third) and classes as jswap; memory finals
   pooled (PM PA PN TM TA TN), over all relations and over the probe-valid ones (memory_valid). The probe subspace has
   min(10, values - 1) dimensions, so it is smaller than J++'s 10 on relations with few values (probe_dims).

python scripts/probe_ceiling.py --name N --why W --band 32-40 --dev-competence C1 --test-competence C2 [--stride 2]
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
from scripts import jsuite_v2_tables as TB  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts.ablate_v2 import bridge_positions, tasks_prompts  # noqa: E402

RES = pins.RESULTS_DIR / "probe_ceiling"
DEV, TEST = "jsuite_v2_dev_chat", "jsuite_v2_test_chat"
CONDS = ("swap", "swap_probe", "swap_probe_rot", "remove", "remove_probe", "paste")
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")
SEED_PROBE_ROT = 4242
VALID_MARGIN = 0.10  # a relation's probe is valid if its dev CV accuracy beats the held-out majority rate by this


def fit_probe(X: torch.Tensor, y: torch.Tensor, n_cls: int, lam: float, steps: int = 200) -> torch.Tensor:
    """Multinomial logistic regression, weights [n_cls, d + 1] (bias last), L2 lam on the weights, LBFGS on the GPU."""
    W = torch.zeros(n_cls, X.shape[1] + 1, device=X.device, requires_grad=True)
    Xb = torch.cat([X, torch.ones(len(X), 1, device=X.device)], 1)
    opt = torch.optim.LBFGS([W], max_iter=steps, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(Xb @ W.T, y) + lam * (W[:, :-1] ** 2).sum()
        loss.backward()
        return loss

    with torch.enable_grad():
        opt.step(closure)
    return W.detach()


def predict(W: torch.Tensor, X: torch.Tensor) -> torch.Tensor:
    return (torch.cat([X, torch.ones(len(X), 1, device=X.device)], 1) @ W.T).argmax(1)


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    band = list(range(int(a.band.split("-")[0]), int(a.band.split("-")[1]) + 1))
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    src = sorted(int(x) for x in lens.source_layers)
    layers = sorted(set(src[:: a.stride]) | set(band))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "model": pins.model_pin(), "lens": pins.FROZEN_LENS,
                                                       "band": a.band, "layers": layers, "dev_competence": a.dev_competence,
                                                       "test_competence": a.test_competence, "conditions": CONDS, "k_max": 10,
                                                       "git_commit": commit, "git_state": pins.git_state(), "seeds": {"probe_rot": f"{SEED_PROBE_ROT}+layer", "cv": 0}}, indent=2) + "\n")  # fmt: skip
    items = {s: {json.loads(x)["id"]: json.loads(x) for x in (JS.DATA / s / "items.jsonl").read_text().splitlines()} for s in (DEV, TEST)}

    def facts_prompts(set_name, comp):
        return [p for p in tasks_prompts(tok, set_name, comp, list(JS.ALL_WORDS_V2), 1000, ["clean"], "all")
                if items[set_name][p["id"]].get("module") == "facts"]  # fmt: skip

    dev_p, test_p = facts_prompts(DEV, a.dev_competence), facts_prompts(TEST, a.test_competence)
    test_bridges = {(items[TEST][p["id"]]["relation"], items[TEST][p["id"]]["bridge"]) for p in test_p}

    def record(prompts_pos):
        """prompts_pos: [(prompt, pos)] -> {layer: [n, d] fp32} residuals at those positions."""
        out = {la: [None] * len(prompts_pos) for la in layers}
        at, first = collections.defaultdict(list), {}  # one forward per prompt, all its mentions read from it
        for i, (p, pos) in enumerate(prompts_pos):
            at[p["id"]].append((i, pos))
            first.setdefault(p["id"], p)
        by_len = collections.defaultdict(list)
        for p in first.values():
            by_len[len(p["ids"])].append(p)
        for group in by_len.values():
            for s in range(0, len(group), a.batch):
                chunk = group[s : s + a.batch]
                ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
                bi = torch.tensor([b for b, p in enumerate(chunk) for _ in at[p["id"]]], device="cuda")
                pi = torch.tensor([pos for p in chunk for _, pos in at[p["id"]]], device="cuda")
                idx = [i for p in chunk for i, _ in at[p["id"]]]
                rec = {}

                def hook_for(la):
                    def hook(_m, _a, o):
                        h = o[0] if isinstance(o, tuple) else o
                        rec[la] = h[bi, pi].float()

                    return hook

                with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
                    model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
                for la in layers:
                    for k, i in enumerate(idx):
                        out[la][i] = rec[la][k]
        return {la: torch.stack(v) for la, v in out.items()}

    # A. training mentions (dev) and test mentions (test bridges, P/T starts, M/N finals)
    train, test = [], []  # (prompt, pos, relation, entity, value)
    for p in dev_p:
        it = items[DEV][p["id"]]
        facts = TB.REL2[it["relation"]]["facts"]
        for e in it["entities"]:
            if e in facts and (it["relation"], e) not in test_bridges:
                pos = JS.spans(bridge_positions(tok, p["ids"], e))
                if pos:
                    train.append((p, pos[0], it["relation"], e, facts[e][0]))
    seen = set()
    for p in test_p:
        it = items[TEST][p["id"]]
        if it["start"] not in "PT" or it["final"] not in "MN":
            continue
        pos = JS.spans(bridge_positions(tok, p["ids"], it["bridge"]))
        if pos:
            test.append((p, pos[0], it["relation"], it["bridge"], TB.REL2[it["relation"]]["facts"][it["bridge"]][0]))
            seen.add(p["id"])
    train = list({(t[0]["id"], t[1]): t for t in train}.values())
    print(f"probe data: {len(train)} train mentions (dev), {len(test)} test mentions (test bridges)", flush=True)
    t0 = time.time()
    Xtr, Xte = record([(t[0], t[1]) for t in train]), record([(t[0], t[1]) for t in test])
    print(f"recorded {len(layers)} layers, {time.time() - t0:.0f}s", flush=True)

    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    rels = sorted({t[2] for t in test})
    readout, probes, mid = {}, {}, band[len(band) // 2]
    for rel in rels:
        tr = [i for i, t in enumerate(train) if t[2] == rel]
        te = [i for i, t in enumerate(test) if t[2] == rel]
        classes = sorted({train[i][4] for i in tr})
        cid = {v: k for k, v in enumerate(classes)}
        te_cov = [i for i in te if test[i][4] in cid]
        if len(classes) < 2 or not te_cov:
            continue
        ytr = torch.tensor([cid[train[i][4]] for i in tr], device="cuda")
        yte = torch.tensor([cid[test[i][4]] for i in te_cov], device="cuda")
        ents = sorted({train[i][3] for i in tr})
        fold = {e: k % 4 for k, e in enumerate(random.Random(0).sample(ents, len(ents)))}
        fidx = torch.tensor([fold[train[i][3]] for i in tr], device="cuda")
        # L2 by entity-grouped 4-fold CV at the band's middle layer
        X = Xtr[mid][tr]
        mu, sd = X.mean(0), X.std(0) + 1e-6
        Z = (X - mu) / sd
        best = None
        for lam in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0):  # the 1025 smoke picked the grid's low edge, so it is widened
            acc, base = [], []
            for f in range(4):
                m_tr = fidx != f
                # held-out mentions scored only if the training folds hold their value, as the test is (te_cov): with
                # one or two entities per value in most relations, an unseen value cannot be predicted at all
                m_te = (fidx == f) & torch.isin(ytr, torch.unique(ytr[m_tr]))
                if m_te.sum() == 0 or len(set(ytr[m_tr].tolist())) < 2:
                    continue
                W = fit_probe(Z[m_tr], ytr[m_tr], len(classes), lam)
                acc.append((predict(W, Z[m_te]) == ytr[m_te]).float().mean().item())
                base.append(max(collections.Counter(ytr[m_te].tolist()).values()) / int(m_te.sum()))
            score = sum(acc) / max(1, len(acc))
            if best is None or score > best[0]:
                best = (score, lam, sum(base) / max(1, len(base)))
        lam = best[1]
        cand = {v: JS.forms(tok, v, "open") for v in classes}  # the relation's answer tokens (first token, both cases)
        cids = torch.tensor(sorted({t for s_ in cand.values() for t in s_}), device="cuda")
        chance = max(collections.Counter(yte.tolist()).values()) / len(yte)
        readout[rel] = {"n_train": len(tr), "n_test": len(te_cov), "n_test_all": len(te), "classes": len(classes), "lam": lam,
                        "cv_acc_mid": round(best[0], 3), "cv_chance_mid": round(best[2], 3), "probe_valid": best[0] >= best[2] + VALID_MARGIN,
                        "chance": round(chance, 3), "by_layer": {}}  # fmt: skip
        probes[rel] = {}
        for la in layers:
            X, Xt = Xtr[la][tr], Xte[la][te_cov]
            mu, sd = X.mean(0), X.std(0) + 1e-6
            W = fit_probe((X - mu) / sd, ytr, len(classes), lam)
            p_acc = (predict(W, (Xt - mu) / sd) == yte).float().mean().item()
            lj = lens.readout(Xt, la)[:, cids]
            lu = model.unembed(Xt)[:, cids]
            pick_j, pick_u = cids[lj.argmax(1)], cids[lu.argmax(1)]
            truth = [cand[classes[c]] for c in yte.tolist()]
            j_acc = sum(int(t_) in s_ for t_, s_ in zip(pick_j.tolist(), truth, strict=True)) / len(truth)
            u_acc = sum(int(t_) in s_ for t_, s_ in zip(pick_u.tolist(), truth, strict=True)) / len(truth)
            readout[rel]["by_layer"][la] = {"probe": round(p_acc, 3), "jlens": round(j_acc, 3), "logit": round(u_acc, 3)}
            if la in band:  # the probe subspace in residual units: top <= 10 right singular vectors of the centred weights / sd
                Wr = W[:, :-1] / sd
                Wr = Wr - Wr.mean(0, keepdim=True)
                _, S_, Vh = torch.linalg.svd(Wr, full_matrices=False)
                k = int(min(10, (S_ > 1e-6 * S_[0]).sum().item()))
                probes[rel][la] = Vh[:k].contiguous()
        print(f"{rel}: n train {len(tr)}, test {len(te_cov)}/{len(te)}, {len(classes)} classes, lam {lam}, chance {chance:.2f}; "
              + " ".join(f"L{la} p{v['probe']:.2f}/j{v['jlens']:.2f}/u{v['logit']:.2f}" for la, v in readout[rel]["by_layer"].items() if la in band or la % 8 == 0), flush=True)  # fmt: skip
    (out_dir / "readout.json").write_text(json.dumps(readout, indent=1) + "\n")

    # B. causal, at the band, swap jobs as jswap
    jobs = []
    for p in test_p:
        it = items[TEST][p["id"]]
        if p["family"] not in JS.WORDS_V2 or it["relation"] not in probes:
            continue
        x, kind = it["bridge"], it["kind"]
        t = TB.REL2[it["relation"]]
        vocab = it["answer_vocab"]
        if it["final"] == "P":
            ans = {e: JS.pfact_value(t["pfact"][it["wording"]], it["context"], e, vocab) for e in it["entities"]}
        else:
            ans = {e: t["facts"][e][0] for e in it["entities"]}
        if ans.get(x) is None:
            continue
        xpos = JS.spans(bridge_positions(tok, p["ids"], x))
        rng = random.Random(p["id"])
        ok_name = lambda e: not (e.lower().startswith(x.lower()) or x.lower().startswith(e.lower()))  # noqa: E731
        donors = [e for e in it["entities"][1:] if ans.get(e) and ans[e] != ans[x] and ok_name(e) and bridge_positions(tok, p["ids"], e)]
        if not xpos or not donors:
            continue
        d = rng.choice(sorted(donors))
        thirds = [e for e in it["entities"][1:] if e != d and ans.get(e) and ans[e] not in (ans[x], ans[d])]
        th = rng.choice(sorted(thirds)) if thirds else None
        dpos = JS.spans(bridge_positions(tok, p["ids"], d))
        jobs.append({**p, "x": x, "d": d, "th": th, "rel": it["relation"], "pairs": [(xp, dpos[min(i, len(dpos) - 1)]) for i, xp in enumerate(xpos)],
                     "fx": JS.forms(tok, ans[x], kind), "fd": JS.forms(tok, ans[d], kind), "ft": JS.forms(tok, ans[th], kind) if th else set(),
                     "ax": ans[x], "ad": ans[d], "at": ans[th] if th else None})  # fmt: skip
    if a.limit:
        per = collections.defaultdict(list)
        for j in jobs:
            per[j["family"]].append(j)
        jobs = [j for f in JS.WORDS_V2 for j in per[f][: a.limit]]
    print(f"{len(jobs)} swap jobs; by word {dict(collections.Counter(j['family'] for j in jobs))}", flush=True)
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    rot = {la: rotation(wg.shape[1], SEED_PROBE_ROT + la) for la in band}

    def forward(ids, hook_fn, record_=False):
        rec = {}

        def hook_for(la):
            def hook(_m, _a, out):
                h = out[0] if isinstance(out, tuple) else out
                if record_:
                    rec[la] = h.float().clone()
                if hook_fn is None:
                    return None
                new = hook_fn(la, h)
                return (new, *out[1:]) if isinstance(out, tuple) else new

            return hook

        with _forward_hooks([(model.layers[la], hook_for(la)) for la in band]):
            logits = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1).logits[:, -1].float()
        return logits, rec

    def classify(lg, j):
        c2 = torch.tensor(j["cands2"], device=lg.device)
        pick = int(c2[lg[c2].argmax()])
        cls = "kept" if pick in j["ok2"] or pick in j["fx"] else "donor" if pick in j["fd"] else "third" if pick in j["ft"] else "other"
        return cls, pick

    rows, t0 = [], time.time()
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            clean, rec = forward(ids, None, record_=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            meta = lambda j: {"x": j["x"], "donor": j["d"], "third": j["th"], "ax": j["ax"], "ad": j["ad"], "at": j["at"], "rel": j["rel"]}  # noqa: E731
            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, **meta(j)})
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["pairs"]], device="cuda")
            xi = torch.tensor([xp for j in chunk for xp, _ in j["pairs"]], device="cuda")
            di = torch.tensor([dp for j in chunk for _, dp in j["pairs"]], device="cuda")
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            prel = [chunk[b]["rel"] for b in bi.tolist()]
            for cond in CONDS:

                def hook_fn(la, h, cond=cond):
                    hx, hd = h[bi, xi].float(), rec[la][bi, di]
                    if cond == "paste":
                        new = hd
                    elif cond in ("swap", "remove"):
                        rx = top_span_removal(dic[la], hx, 10, protected=groups)
                        new = hx - rx + top_span_removal(dic[la], hd, 10, protected=groups) if cond == "swap" else hx - rx
                    else:
                        Q = torch.stack([torch.nn.functional.pad(probes[r][la], (0, 0, 0, 10 - probes[r][la].shape[0])) for r in prel])  # [m, 10, d]
                        px = (Q.transpose(1, 2) @ (Q @ hx.unsqueeze(2))).squeeze(2)
                        pd = (Q.transpose(1, 2) @ (Q @ hd.unsqueeze(2))).squeeze(2)
                        new = {"swap_probe": hx - px + pd, "swap_probe_rot": hx + (pd - px) @ rot[la].T, "remove_probe": hx - px}[cond]
                    h = h.clone()
                    h[bi, xi] = new.to(h.dtype)
                    return h

                lg, _ = forward(ids, hook_fn)
                for b, j in enumerate(chunk):
                    cls, pick = classify(lg[b], j)
                    rows.append({"id": j["id"], "family": j["family"], "condition": cond, "cls": cls, "pick": pick, **meta(j)})
        print(f"{len(rows)} rows, {time.time() - t0:.0f}s", flush=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summ = JS.score(rows)
    summ.update(JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY]))
    valid = sorted(r for r, v in readout.items() if v["probe_valid"])
    summ.update({k.replace("memory/", "memory_valid/"): v for k, v in JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY and r["rel"] in valid]).items()})
    summ["probe_valid_relations"] = valid
    summ["probe_dims"] = {r: {la: int(q.shape[0]) for la, q in v.items()} for r, v in probes.items()}
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    print(f"probe-valid relations (dev CV at the mid layer >= its majority rate + {VALID_MARGIN}): {valid}", flush=True)
    for f in (*JS.WORDS_V2, "memory", "memory_valid"):
        for c in ("none", *CONDS):
            cell = summ.get(f"{f}/{c}")
            if cell:
                print(f"{f:6s} {c:14s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}"
                      f"  other {cell['other']:5.1f}  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--dev-competence", required=True)
    ap.add_argument("--test-competence", required=True)
    ap.add_argument("--stride", type=int, default=2)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="first N swap jobs per word (a smoke)")
    main(ap.parse_args())
