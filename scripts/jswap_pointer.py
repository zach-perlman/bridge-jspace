"""jswap_pointer (Zach, 2026-10-26, prereg amendment 51): what the bridge mention's J-part carries, three tests.

jswap (amendment 32) swaps the top-10 J++ part at the last token of each mention of the bridge X with the J-part at a
donor entity D's mention in the same passage; the cross-relation swap (amendment 47) showed, for the country relations,
that D's J-part from another relation's passage transfers as well. Here, on every relation of the facts module, with
jswap's own jobs (same donors, thirds and positions, so `swap` is jswap's):
  1. A context-free donor. D's J-part from a one-sentence neutral prompt in the same chat framing ("A reader asked a
     question about D in the letters page.", a sentence the passages use; the residual at D's last token is computed
     before anything else in that prompt): swap_neutral, its same-size rotation (swap_neutral_rot), the logit lens's
     top-10 instead of J++'s (swap_neutral_u), and the whole residual (paste_neutral).
  2. The entity's own name. X's and D's own-word dictionary rows (their surface tokens and every row with cosine >=
     OWN_COS to their concept token, ablate_v2's keep_own rows): swap_own swaps only the span of the (up to 10)
     own-word rows with the highest logits at each side; swap_noown is jswap's swap with those rows never chosen.
  3. When the attribute is looked up. Under none, swap and swap_neutral, the J++ lens's pick among the item's candidate
     answers at the answer position, at every lens layer from the band's first on (timeline.jsonl): the layer from
     which the donor's answer leads.
Classes and the transfer index (donor - third, 95% bootstrap over bridges) as jswap; memory finals pooled (PM PA PN TM
TA TN) overall and by relation.

python scripts/jswap_pointer.py --name N --why W --band 12-16 --competence C [--set jsuite_v2_test_chat] [--batch 8]
       [--limit 0] [--sample-per-word 0]
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
from bridge_jspace.ablate import OWN_COS, LensDictionary, rotation, top_span_removal  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from bridge_jspace.run_switches import switches
from scripts import jsuite_v2_tables as TB  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402
from scripts.ablate_v2 import bridge_positions, tasks_prompts  # noqa: E402

RES = pins.RESULTS_DIR / "jswap"
CONDS = ("swap", "swap_neutral", "swap_neutral_rot", "swap_neutral_u", "paste_neutral", "swap_own", "swap_noown")
TIMELINE = ("none", "swap", "swap_neutral")
NEUTRAL = "A reader asked a question about {} in the letters page."
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")


def span_proj(atoms: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """x [d] projected on the span of atoms [k, d]."""
    if atoms.shape[0] == 0:
        return torch.zeros_like(x)
    Q, _ = torch.linalg.qr(atoms.double().T)
    return (Q @ (Q.T @ x.double())).float()


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    band = list(range(int(a.band.split("-")[0]), int(a.band.split("-")[1]) + 1))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "model": pins.model_pin(), "switches": switches(),
                                                       "lens": pins.FROZEN_LENS, "band": a.band, "set": a.set, "competence": a.competence,
                                                       "conditions": CONDS, "timeline": TIMELINE, "neutral": NEUTRAL, "own_cos": OWN_COS,
                                                       "k": a.k, "git_commit": commit, "git_state": pins.git_state(), "limit": a.limit,
                                                       "sample_per_word": a.sample_per_word, "seed": "random.Random(item id), as jswap"}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    v3 = a.set.startswith("jsuite_v3")  # amendment 58 note 5
    WORDS = JS.WORDS_V3 if v3 else JS.WORDS_V2
    base = JS.v3_prompts(tok, a.set, a.competence, WORDS) if v3 else tasks_prompts(tok, a.set, a.competence, list(JS.ALL_WORDS_V2), 1000, ["clean"], "all")
    prompts = [p for p in base if p["family"] in WORDS and items[p["id"]].get("module") == "facts"]  # fmt: skip
    jobs = []
    for p in prompts:  # jswap's jobs exactly (the same rng draws)
        it = items[p["id"]]
        x, kind = it["bridge"], it["kind"]
        t = JS.table(it)
        vocab = it["answer_vocab"]
        if it["final"] == "P":
            ans = {e: JS.pfact_value(t["pfact"][it["wording"]], it["context"], e, vocab, the=v3) for e in it["entities"]}
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
                     "ax": ans[x], "ad": ans[d], "at": ans[th] if th else None, "kind_": kind, "format_": it["format"]})  # fmt: skip
    per = collections.defaultdict(list)
    for j in jobs:
        per[j["family"]].append(j)
    if a.sample_per_word:
        pick = {f: set(range(len(v))) if len(v) <= a.sample_per_word else set(random.Random(f"0:{f}").sample(range(len(v)), a.sample_per_word))
                for f, v in per.items()}  # fmt: skip
        jobs = [j for f in WORDS for k, j in enumerate(per[f]) if k in pick[f]]
    if a.limit:
        jobs = [j for f in WORDS for j in per[f][: a.limit]]

    # 1. the neutral donor prompts, one per donor entity (and read kind / format, as the chat render needs)
    neutral = {}
    for j in jobs:
        key = (j["d"], j["kind_"], j["format_"])
        if key not in neutral:
            text = T.render(tok, {"framing": "chat", "context": NEUTRAL.format(j["d"]), "question": "Has anyone else heard about this?",
                                  "kind": j["kind_"], "format": j["format_"]})  # fmt: skip
            ids = S.ids(tok, text)
            pos = JS.spans(bridge_positions(tok, ids, j["d"]))
            neutral[key] = (ids, pos[0] if pos else None)
    missing = {k for k, v in neutral.items() if v[1] is None}
    jobs = [j for j in jobs if (j["d"], j["kind_"], j["format_"]) not in missing]
    print(f"{len(prompts)} eligible prompts; {len(jobs)} jobs; {len(neutral)} neutral donor prompts ({len(missing)} without a findable mention); "
          f"by word {dict(collections.Counter(j['family'] for j in jobs))}; by relation {dict(collections.Counter(j['rel'] for j in jobs))}", flush=True)  # fmt: skip

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    rot = {la: rotation(wg.shape[1], JS.SEED_ROT + la) for la in band}
    tl_layers = [la for la in sorted(int(x) for x in lens.source_layers) if la >= band[0]]
    hooked = sorted(set(band) | set(tl_layers))

    own_cache: dict = {}

    def own_rows(word: str, la: int) -> torch.Tensor:  # ablate_v2's keep_own rows
        if (word, la) not in own_cache:
            rows = {int(row_of[i]) for i in model.surface_ids(word) if int(row_of[i]) >= 0}
            try:
                concept = int(row_of[model.concept_token(word)])
            except ValueError:
                concept = -1
            if concept >= 0:
                cos = dic[la].scores(dic[la].atoms(torch.tensor([concept], device="cuda")))[0]
                rows |= set((cos >= OWN_COS).nonzero().squeeze(1).tolist())
            own_cache[(word, la)] = torch.tensor(sorted(rows), dtype=torch.long, device="cuda")
        return own_cache[(word, la)]

    def forward(ids, hook_fn, record=False, final=False):
        rec, fin = {}, {}

        def hook_for(la):
            def hook(_m, _a, out):
                h = out[0] if isinstance(out, tuple) else out
                if record and la in band:
                    rec[la] = h.float().clone()
                if hook_fn is not None and la in band:
                    h = hook_fn(la, h)
                if final and la in tl_layers:
                    fin[la] = h[:, -1].float().clone()
                if hook_fn is not None and la in band:
                    return (h, *out[1:]) if isinstance(out, tuple) else h
                return None

            return hook

        with _forward_hooks([(model.layers[la], hook_for(la)) for la in hooked]):
            logits = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1).logits[:, -1].float()
        return logits, rec, fin

    # the neutral donors' residuals at their mention, every band layer
    vec, t0 = {}, time.time()
    by_len = collections.defaultdict(list)
    for key, (ids, pos) in neutral.items():
        if pos is not None:
            by_len[len(ids)].append(key)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            _, rec, _ = forward(torch.tensor([neutral[k][0] for k in chunk], device="cuda"), None, record=True)
            for b, key in enumerate(chunk):
                vec[key] = torch.stack([rec[la][b, neutral[key][1]] for la in band])
    print(f"{len(vec)} neutral donor residuals, {time.time() - t0:.0f}s", flush=True)

    def classify(lg, j):
        c2 = torch.tensor(j["cands2"], device=lg.device)
        pick = int(c2[lg[c2].argmax()])
        cls = "kept" if pick in j["ok2"] or pick in j["fx"] else "donor" if pick in j["fd"] else "third" if pick in j["ft"] else "other"
        return cls, pick

    rows, tl = [], []
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            clean, rec, fin = forward(ids, None, record=True, final=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            meta = lambda j: {"x": j["x"], "donor": j["d"], "third": j["th"], "ax": j["ax"], "ad": j["ad"], "at": j["at"], "rel": j["rel"]}  # noqa: E731

            def timeline(cond, fin):
                for la in tl_layers:
                    lg = lens.readout(fin[la], la)
                    for b, j in enumerate(chunk):
                        tl.append({"id": j["id"], "family": j["family"], "condition": cond, "layer": la, "cls": classify(lg[b], j)[0]})

            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, **meta(j)})
            timeline("none", fin)
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["pairs"]], device="cuda")
            xi = torch.tensor([xp for j in chunk for xp, _ in j["pairs"]], device="cuda")
            di = torch.tensor([dp for j in chunk for _, dp in j["pairs"]], device="cuda")
            nd = torch.stack([vec[(chunk[b]["d"], chunk[b]["kind_"], chunk[b]["format_"])] for b in bi.tolist()])  # [pairs, layers, d]
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            for cond in CONDS:

                def hook_fn(la, h, cond=cond):
                    li = band.index(la)
                    hx = h[bi, xi].float()
                    hd = nd[:, li] if "neutral" in cond else rec[la][bi, di]
                    if cond == "paste_neutral":
                        new = hd
                    elif cond in ("swap_own", "swap_noown"):
                        new = torch.empty_like(hx)
                        for m in range(hx.shape[0]):
                            jb = chunk[int(bi[m])]
                            ox, od = own_rows(jb["x"], la), own_rows(jb["d"], la)
                            if cond == "swap_own":  # only the own-word span: up to 10 rows with the highest logits at each side
                                def own_part(v, rows_):
                                    if rows_.numel() == 0:
                                        return torch.zeros_like(v)
                                    at = dic[la].atoms(rows_[None])[0]  # [n, d]
                                    top = (at @ v).topk(min(a.k, rows_.numel())).indices
                                    return span_proj(at[top], v)
                                new[m] = hx[m] - own_part(hx[m], ox) + own_part(hd[m], od)
                            else:  # jswap's swap with the own-word rows (and the answer's protected rows) never chosen
                                p_ = prot[int(bi[m])]
                                gx = [(torch.zeros(1, dtype=torch.long, device="cuda"), torch.cat([p_, ox]))]
                                gd = [(torch.zeros(1, dtype=torch.long, device="cuda"), torch.cat([p_, od]))]
                                new[m] = hx[m] - top_span_removal(dic[la], hx[m : m + 1], a.k, protected=gx)[0] + top_span_removal(dic[la], hd[m : m + 1], a.k, protected=gd)[0]
                    else:
                        D = unembed if cond == "swap_neutral_u" else dic[la]
                        rx, rd = top_span_removal(D, hx, a.k, protected=groups), top_span_removal(D, hd, a.k, protected=groups)
                        new = hx + (rd - rx) @ rot[la].T if cond == "swap_neutral_rot" else hx - rx + rd
                    h = h.clone()
                    h[bi, xi] = new.to(h.dtype)
                    return h

                lg, _, fin = forward(ids, hook_fn, final=cond in TIMELINE)
                for b, j in enumerate(chunk):
                    cls, pick = classify(lg[b], j)
                    rows.append({"id": j["id"], "family": j["family"], "condition": cond, "cls": cls, "pick": pick, **meta(j)})
                if cond in TIMELINE:
                    timeline(cond, fin)
        print(f"{len(rows)} rows, {time.time() - t0:.0f}s", flush=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out_dir / "timeline.jsonl").write_text("".join(json.dumps(r) + "\n" for r in tl))
    summ = JS.score(rows)
    summ.update(JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY]))
    for rel in sorted({r["rel"] for r in rows}):
        summ.update({k.replace("memory/", f"memory_{rel}/"): v for k, v in JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY and r["rel"] == rel]).items()})
    # the timeline over memory items right unedited: share of items whose lens pick at the answer position is X's / D's
    ok = {r["id"] for r in rows if r["condition"] == "none" and r["cls"] == "kept" and r["family"] in MEMORY}
    tsum: dict = {}
    for cond in TIMELINE:
        for la in tl_layers:
            sel = [x["cls"] for x in tl if x["condition"] == cond and x["layer"] == la and x["id"] in ok]
            if sel:
                tsum[f"{cond}/L{la}"] = {"n": len(sel), "kept": round(100 * sel.count("kept") / len(sel), 1), "donor": round(100 * sel.count("donor") / len(sel), 1)}
    summ["timeline_memory"] = tsum
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for f in ("memory", *[f"memory_{rel}" for rel in sorted({r['rel'] for r in rows})]):
        for c in ("none", *CONDS):
            cell = summ.get(f"{f}/{c}")
            if cell:
                print(f"{f:18s} {c:16s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}"
                      f"  other {cell['other']:5.1f}  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip
    for c in ("PP", "PK", "TP", "TK"):
        for cond in CONDS:
            cell = summ.get(f"{c}/{cond}")
            if cell:
                print(f"{c:18s} {cond:16s} n {cell['n']:4d}  kept {cell['kept']:5.1f}")
    for cond in TIMELINE:
        print("timeline " + cond + ": " + " ".join(f"L{k.split('/L')[1]} {v['kept']:.0f}/{v['donor']:.0f}" for k, v in tsum.items() if k.startswith(cond + "/")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v2_test_chat")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="first N jobs per word (a smoke)")
    ap.add_argument("--sample-per-word", type=int, default=0, help="a seeded random N jobs per word (0: all)")
    ap.add_argument("--k", type=int, default=10, help="size of the swapped J-part (2026-10-27, amendment 55 note 1; default 10)")
    main(ap.parse_args())
