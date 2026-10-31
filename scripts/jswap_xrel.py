"""jswap_xrel (Zach, 2026-10-25, prereg amendment 47): the cross-relation J-swap at the bridge's mention.

jswap (amendment 32) swaps the top-10 J-part at the last token of each mention of the bridge X with the J-part at a
donor country D's mention in the same passage. That passage is themed on the asked relation (its lure sentences use the
answer vocabulary), so D's J-part may carry only a value primed by the theme. Here D's J-part comes from another prompt
of the same test set where D is named, either of the same relation (swap_srel) or of the other country relation
(swap_xrel: a continent-themed passage for a language question, and the reverse). If the mention carries the entity's
attributes in general, swap_xrel moves the answer to D's value of the asked relation about as well as swap_srel.
Relations: countries (continent) and languages, the two v2 relations whose bridges are both countries. Words: the read
and tracked starts (v2's PP PK PM PA PN TP TK TM TA TN); eligibility as the knock-out (the model's competence run).
jsuite v3 (amendment 58 note 5): no two v3 relations share their entities, so the "relation" is the asked
attribute: the entity's own (K finals: "By nationality, D was Kenyan.") or the made-up one about it (P finals: "The
upcoming biopic casts a French actor as D.", same answer words). swap_srel takes D's J-part from another prompt asking
the item's own attribute, swap_xrel from one asking the other; mentions in M A N passages (made-up-fact lures on other
entities) are not used. Words: v3's PP PK PM PA PN TK TM; rows carry the donor prompts' ids (ssrc, xsrc).
Conditions, at every layer of the band (one patched forward each, after one clean forward):
  swap           D's J-part from this prompt (jswap's swap, the reference)
  swap_srel      D's J-part from another prompt of the same relation
  swap_xrel      D's J-part from a prompt of the other relation
  swap_xrel_rot  h_X + (J10(h_D) - J10(h_X)) R^T with swap_xrel's h_D (the same-size change in a fixed random direction)
  swap_xrel_u    swap_xrel over the logit lens's top-10 directions
  paste_xrel     the whole residual from the other relation's prompt (the ceiling)
Donor positions: the last token of D's first mention in the donor prompt. Classes and the transfer index (donor - third,
95% bootstrap over bridges) as jswap; memory finals pooled (PM PA PN TM TA TN) beside each word.

python scripts/jswap_xrel.py --name N --why W --band 32-40 --competence C [--set jsuite_v2_test_chat] [--batch 8] [--limit 0]
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
from bridge_jspace.run_switches import switches
from scripts import jsuite_v2_tables as TB  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts.ablate_v2 import bridge_positions, tasks_prompts  # noqa: E402

RES = pins.RESULTS_DIR / "jswap"
RELS = ("countries", "languages")
CONDS = ("swap", "swap_srel", "swap_xrel", "swap_xrel_rot", "swap_xrel_u", "paste_xrel")
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    band = list(range(int(a.band.split("-")[0]), int(a.band.split("-")[1]) + 1))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "model": pins.model_pin(), "switches": switches(),
                                                       "lens": pins.FROZEN_LENS, "band": a.band, "set": a.set, "competence": a.competence,
                                                       "relations": RELS, "conditions": CONDS, "k": 10, "git_commit": commit, "git_state": pins.git_state(),
                                                       "limit": a.limit, "seed": "random.Random(item id)",
                                                       **({"v3_relations": "fact (K finals) / pfact (P finals); amendment 58 note 5"} if a.set.startswith("jsuite_v3") else {})}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    v3 = a.set.startswith("jsuite_v3")  # amendment 58 note 5: the other relation is the donor's made-up-fact passage
    WORDS = JS.WORDS_V3 if v3 else JS.WORDS_V2
    if v3:
        prompts = [p for p in JS.v3_prompts(tok, a.set, a.competence, WORDS) if items[p["id"]].get("module") == "facts"]
    else:
        prompts = [p for p in tasks_prompts(tok, a.set, a.competence, list(JS.ALL_WORDS_V2), 1000, ["clean"], "all")
                   if items[p["id"]].get("module") == "facts" and items[p["id"]].get("relation") in RELS]  # fmt: skip

    def ctx(it: dict) -> str | None:  # the mention pool a prompt feeds: v2, its relation; v3, the asked attribute
        if not v3:
            return it["relation"]
        return "fact" if it["final"] in "KH" else "pfact" if it["final"] == "P" else None

    by_id = {p["id"]: p for p in prompts}
    mentions = collections.defaultdict(list)  # (relation, country) -> [(prompt id, last token of its first mention)]
    for p in prompts:
        it = items[p["id"]]
        for e in it["entities"]:
            pos = JS.spans(bridge_positions(tok, p["ids"], e))
            if pos and ctx(it):
                mentions[(ctx(it), e)].append((p["id"], pos[0]))
    jobs = []
    for p in prompts:
        if p["family"] not in WORDS:
            continue
        it = items[p["id"]]
        x, kind, rel = it["bridge"], it["kind"], it["relation"]
        same, other = (("pfact", "fact") if it["final"] == "P" else ("fact", "pfact")) if v3 else (rel, RELS[1 - RELS.index(rel)])
        t = JS.table(it) if v3 else TB.REL2[rel]
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
        src = lambda r, e: sorted(m for m in mentions[(r, e)] if m[0] != p["id"])  # noqa: E731
        donors = [e for e in it["entities"][1:] if ans.get(e) and ans[e] != ans[x] and ok_name(e) and bridge_positions(tok, p["ids"], e)
                  and src(same, e) and src(other, e)]  # fmt: skip
        if not xpos or not donors:
            continue
        d = rng.choice(sorted(donors))
        thirds = [e for e in it["entities"][1:] if e != d and ans.get(e) and ans[e] not in (ans[x], ans[d])]
        th = rng.choice(sorted(thirds)) if thirds else None
        dpos = JS.spans(bridge_positions(tok, p["ids"], d))
        jobs.append({**p, "x": x, "d": d, "th": th, "rel": rel, "pairs": [(xp, dpos[min(i, len(dpos) - 1)]) for i, xp in enumerate(xpos)],
                     "ssrc": rng.choice(src(same, d)), "xsrc": rng.choice(src(other, d)),
                     "fx": JS.forms(tok, ans[x], kind), "fd": JS.forms(tok, ans[d], kind), "ft": JS.forms(tok, ans[th], kind) if th else set(),
                     "ax": ans[x], "ad": ans[d], "at": ans[th] if th else None})  # fmt: skip
    if a.limit:
        per = collections.defaultdict(list)
        for j in jobs:
            per[j["family"]].append(j)
        jobs = [j for f in WORDS for j in per[f][: a.limit]]
    print(f"{len(prompts)} eligible prompts in {RELS}; {len(jobs)} jobs; by word {dict(collections.Counter(j['family'] for j in jobs))}", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    rot = {la: rotation(wg.shape[1], JS.SEED_ROT + la) for la in band}

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

    # the donors' clean residuals at their mention in the other prompts, every band layer
    need = sorted({j[k] for j in jobs for k in ("ssrc", "xsrc")})
    vec, t0 = {}, time.time()
    by_len = collections.defaultdict(list)
    for pid, pos in need:
        by_len[len(by_id[pid]["ids"])].append((pid, pos))
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            _, rec = forward(torch.tensor([by_id[pid]["ids"] for pid, _ in chunk], device="cuda"), None, record=True)
            for b, key in enumerate(chunk):
                vec[key] = torch.stack([rec[la][b, key[1]] for la in band])  # [layers, d]
    print(f"{len(vec)} donor residuals, {time.time() - t0:.0f}s", flush=True)

    def classify(lg, j):
        c2 = torch.tensor(j["cands2"], device=lg.device)
        pick = int(c2[lg[c2].argmax()])
        cls = "kept" if pick in j["ok2"] or pick in j["fx"] else "donor" if pick in j["fd"] else "third" if pick in j["ft"] else "other"
        return cls, pick

    rows = []
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            clean, rec = forward(ids, None, record=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            meta = lambda j: {"x": j["x"], "donor": j["d"], "third": j["th"], "ax": j["ax"], "ad": j["ad"], "at": j["at"], "rel": j["rel"],  # noqa: E731
                              **({"ssrc": j["ssrc"][0], "xsrc": j["xsrc"][0]} if v3 else {})}
            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, **meta(j)})
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["pairs"]], device="cuda")
            xi = torch.tensor([xp for j in chunk for xp, _ in j["pairs"]], device="cuda")
            di = torch.tensor([dp for j in chunk for _, dp in j["pairs"]], device="cuda")
            srel = torch.stack([vec[chunk[b]["ssrc"]] for b in bi.tolist()])  # [pairs, layers, d]
            xrel = torch.stack([vec[chunk[b]["xsrc"]] for b in bi.tolist()])
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            for cond in CONDS:

                def hook_fn(la, h, cond=cond):
                    li = band.index(la)
                    hx = h[bi, xi].float()
                    hd = {"swap": rec[la][bi, di], "swap_srel": srel[:, li]}.get(cond, xrel[:, li])
                    if cond == "paste_xrel":
                        new = hd
                    else:
                        D = unembed if cond == "swap_xrel_u" else dic[la]
                        rx, rd = top_span_removal(D, hx, 10, protected=groups), top_span_removal(D, hd, 10, protected=groups)
                        new = hx + (rd - rx) @ rot[la].T if cond == "swap_xrel_rot" else hx - rx + rd
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
    pooled = JS.score([{**r, "family": "memory"} for r in rows if r["family"] in MEMORY])
    summ.update({k: v for k, v in pooled.items()})
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for f in (*(JS.WORDS_V3 if a.set.startswith("jsuite_v3") else JS.WORDS_V2), "memory"):
        for c in ("none", *CONDS):
            cell = summ.get(f"{f}/{c}")
            if cell:
                print(f"{f:6s} {c:13s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}"
                      f"  other {cell['other']:5.1f}  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v2_test_chat")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="first N jobs per word (a smoke)")
    main(ap.parse_args())
