"""jswap (Zach, 2026-10-24, prereg amendment 32): the J-subspace swap at the bridge's mention, a sufficiency test.

The position-restricted knock-outs (amendment 30) put the whole memory-final dependence of a read or tracked bridge on
the bridge's own mention tokens. Here, at the last token of each mention of the bridge X, in every layer of the band, the
top-10 J-part of the residual (paper10's selection: the span of the 10 unit J-lens vectors with the highest lens logits
there, never a protected token = the clean top-10 at the answer position) is replaced by the same part taken from a donor
entity D named in the same passage (its clean residual, at the last token of its matching mention). If that J-part
carries the entity's recalled attributes, a memory-final answer should switch to D's attribute while the passage
lookups (P and K finals) stay with X. Conditions (one patched forward each, after one clean forward):
  swap       h_X - J10(h_X) + J10(h_D)
  remove     h_X - J10(h_X)                    (the knock-out at these positions alone)
  swap_rot   h_X + (J10(h_D) - J10(h_X)) R^T   (the same-size change in a fixed random direction)
  swap_u     the swap over the logit lens's top-10 directions (J = identity)
  swap_comp  J10(h_X) + h_D - J10(h_D)         (everything but the J-part from D)
  paste      h_D                               (the whole residual: the ceiling)
Each answer (the candidate read's pick among the relation's answers) is classed as kept (X's answer), donor (D's), third
(the answer of a third passage entity T, the chance a disrupted answer lands on any given entity's value) or other.
D: a passage entity with an answer different from X's, named in the passage, its name not a prefix of X's or the
reverse; T: another, with an answer different from both (absent on some items). Words: the read and tracked starts (PP
PK PM PA TP TK TM TA); eligibility as the knock-out (scene rule over the 12 words, the model's competence run).

python scripts/jswap.py --name N --why W --band 12-16 --competence C [--set jsuite_v1_facts_test_chat] [--batch 16] [--limit 0]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import string
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
from scripts import natplus as NP  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts.ablate_v2 import bridge_positions, tasks_prompts  # noqa: E402

RES = pins.RESULTS_DIR / "jswap"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
ALL_WORDS = ("PP", "PK", "PM", "PA", "MP", "MK", "MM", "MA", "TP", "TK", "TM", "TA")
WORDS = ("PP", "PK", "PM", "PA", "TP", "TK", "TM", "TA")
CONDS = ("swap", "remove", "swap_rot", "swap_u", "swap_comp", "paste")
SEED_ROT = 888


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def pfact_value(tpl: str, ctx: str, e: str, vocab: list[str]) -> str | None:
    """The value the passage's new-fact sentence (template tpl) gives entity e, or None."""
    rx = ""
    for lit, field, _, _ in string.Formatter().parse(tpl):
        rx += re.escape(lit)
        if field is None:
            continue
        rx += {"x": re.escape(e), "X": re.escape(cap(e)), "a": r"(?P<v>[A-Za-z][A-Za-z ]*?)",
               "al": r"(?P<v>[a-z][a-z ]*?)", "an": r"(?:a|an)"}[field]  # fmt: skip
    m = re.search(rx + r"(?=[.,!?\s])", ctx)
    if not m:
        return None
    v = m.group("v")
    return next((a for a in vocab if a.lower() == v.lower()), None)


def spans(pos: list[int]) -> list[int]:
    """Last token of each run of consecutive positions (each mention)."""
    out = []
    for i, p in enumerate(pos):
        if i + 1 == len(pos) or pos[i + 1] != p + 1:
            out.append(p)
    return out


def forms(tok, v: str, kind: str) -> set[int]:
    return {S.answer_token(tok, v, kind), S.answer_token(tok, v.lower(), kind)}


@torch.no_grad()  # 2026-10-24: the first full run kept autograd activations and ran out of GPU memory
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    band = list(range(int(a.band.split("-")[0]), int(a.band.split("-")[1]) + 1))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "band": a.band,
                                                       "set": a.set, "competence": a.competence, "conditions": CONDS, "k": 10,
                                                       "git_commit": commit, "limit": a.limit}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / a.set / "items.jsonl").read_text().splitlines()}
    prompts = [p for p in tasks_prompts(tok, a.set, a.competence, list(ALL_WORDS), 1000, ["clean"], "all") if p["family"] in WORDS]
    jobs = []
    for p in prompts:
        it = items[p["id"]]
        x, dom, kind = it["bridge"], it["domain"], it["kind"]  # the whole question's read kind (chat: "open")
        t = NP.TYPES[dom]
        vocab = it["answer_vocab"]
        if it["final"] == "P":
            tpl = t["pfact"][it["wording"]]
            ans = {e: pfact_value(tpl, it["context"], e, vocab) for e in it["entities"]}
        else:
            ans = {e: t["facts"][e][0] for e in it["entities"]}
        if ans.get(x) is None:
            continue
        xpos = spans(bridge_positions(tok, p["ids"], x))
        rng = random.Random(p["id"])
        ok_name = lambda e: not (e.lower().startswith(x.lower()) or x.lower().startswith(e.lower()))  # noqa: E731
        donors = [e for e in it["entities"][1:] if ans.get(e) and ans[e] != ans[x] and ok_name(e) and bridge_positions(tok, p["ids"], e)]
        if not xpos or not donors:
            continue
        d = rng.choice(sorted(donors))
        thirds = [e for e in it["entities"][1:] if e != d and ans.get(e) and ans[e] not in (ans[x], ans[d])]
        th = rng.choice(sorted(thirds)) if thirds else None
        dpos = spans(bridge_positions(tok, p["ids"], d))
        pairs = [(xp, dpos[min(i, len(dpos) - 1)]) for i, xp in enumerate(xpos)]
        jobs.append({**p, "x": x, "d": d, "th": th, "pairs": pairs, "dom": dom, "final": it["final"],
                     "fx": forms(tok, ans[x], kind), "fd": forms(tok, ans[d], kind), "ft": forms(tok, ans[th], kind) if th else set(),
                     "ax": ans[x], "ad": ans[d], "at": ans[th] if th else None})  # fmt: skip
    if a.limit:
        per = collections.defaultdict(list)
        for j in jobs:
            per[j["family"]].append(j)
        jobs = [j for f in WORDS for j in per[f][: a.limit]]
    print(f"{len(prompts)} eligible prompts; {len(jobs)} with a donor; by word {dict(collections.Counter(j['family'] for j in jobs))}", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    rot = {la: rotation(wg.shape[1], SEED_ROT + la) for la in band}

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
            clean, rec = forward(ids, None, record=True)
            prot = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            for b, j in enumerate(chunk):
                cls, pick = classify(clean[b], j)
                rows.append({"id": j["id"], "family": j["family"], "condition": "none", "cls": cls, "pick": pick, "x": j["x"],
                             "donor": j["d"], "third": j["th"], "ax": j["ax"], "ad": j["ad"], "at": j["at"]})  # fmt: skip
            bi = torch.tensor([b for b, j in enumerate(chunk) for _ in j["pairs"]], device="cuda")
            xi = torch.tensor([xp for j in chunk for xp, _ in j["pairs"]], device="cuda")
            di = torch.tensor([dp for j in chunk for _, dp in j["pairs"]], device="cuda")
            groups = [((bi == b).nonzero().squeeze(1), prot[b]) for b in range(len(chunk)) if prot[b].numel()]
            for cond in CONDS:

                def hook_fn(la, h, cond=cond):
                    hx, hd = h[bi, xi].float(), rec[la][bi, di]
                    D = unembed if cond == "swap_u" else dic[la]
                    rx, rd = top_span_removal(D, hx, 10, protected=groups), top_span_removal(D, hd, 10, protected=groups)
                    new = {"swap": hx - rx + rd, "remove": hx - rx, "swap_rot": hx + (rd - rx) @ rot[la].T, "swap_u": hx - rx + rd,
                           "swap_comp": rx + hd - rd, "paste": hd}[cond]  # fmt: skip
                    h = h.clone()
                    h[bi, xi] = new.to(h.dtype)
                    return h

                lg, _ = forward(ids, hook_fn)
                for b, j in enumerate(chunk):
                    cls, pick = classify(lg[b], j)
                    rows.append({"id": j["id"], "family": j["family"], "condition": cond, "cls": cls, "pick": pick, "x": j["x"],
                                 "donor": j["d"], "third": j["th"], "ax": j["ax"], "ad": j["ad"], "at": j["at"]})  # fmt: skip
        print(f"{len(rows)} rows, {time.time() - t0:.0f}s", flush=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    summ = score(rows)
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for f in WORDS:
        for c in ("none",) + CONDS:
            cell = summ.get(f"{f}/{c}")
            if cell:
                print(f"{f} {c:9s} n {cell['n']:4d}  kept {cell['kept']:5.1f}  donor {cell['donor']:5.1f}  third {cell['third']:5.1f}"
                      f"  other {cell['other']:5.1f}  donor-third {cell['transfer']:+5.1f} {cell['ci']}")  # fmt: skip


def score(rows: list[dict]) -> dict:
    """Per word x condition: % kept / donor / third / other over items right unedited (kept under none), and the
    transfer index donor - third (third counted on items with a third entity) with a 95% bootstrap over bridges."""
    ok = {r["id"] for r in rows if r["condition"] == "none" and r["cls"] == "kept"}
    out, rng = {}, random.Random(0)
    cells = collections.defaultdict(list)
    for r in rows:
        if r["id"] in ok:
            cells[(r["family"], r["condition"])].append(r)
    for (f, c), rs in cells.items():
        n = len(rs)
        pct = {k: 100 * sum(r["cls"] == k for r in rs) / n for k in ("kept", "donor", "third", "other")}
        wt = [r for r in rs if r["third"]]
        tr = lambda xs: 100 * (sum(r["cls"] == "donor" for r in xs) - sum(r["cls"] == "third" for r in xs)) / max(1, len(xs))  # noqa: E731
        by = collections.defaultdict(list)
        for r in wt:
            by[r["x"]].append(r)
        keys = sorted(by)
        bs = sorted(tr([r for k in (rng.choice(keys) for _ in keys) for r in by[k]]) for _ in range(1000)) if keys else []
        out[f"{f}/{c}"] = {"n": n, **{k: round(v, 1) for k, v in pct.items()}, "n_third": len(wt), "transfer": round(tr(wt), 1),
                           "ci": [round(bs[25], 1), round(bs[974], 1)] if bs else None}  # fmt: skip
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v1_facts_test_chat")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0, help="first N jobs per word (a smoke)")
    main(ap.parse_args())
