"""wrong_bridge_causal (Zach, 2026-10-23, prereg amendment 18): causal tests on WorkspaceBench's wrong_bridge items.

Each item (data/wsb_wrong_bridge.json, camilablank/workspace-bench@ba33098 evals/wrong_bridge, MIT) is a raw-text
two-hop prompt on which Qwen3.6-27B resolves a WRONG bridge B' and answers hop2(B') = A' instead of hop2(B) = A
("Fact: The composer of Piano Sonata No. 18 in D Major was born in the city of" -> Bonn via Beethoven; true: Salzburg
via Mozart), gated by the benchmark (A' and B' in >= 4/10 samples; injecting B' gives A', injecting B gives A; ...).

Read: teacher-forced log-probability of each full answer (" Bonn", " Salzburg"; cities and years are multi-token),
edits applied to prompt positions only. margin = logP(A') - logP(A); flip = logP(A) > logP(A').
Conditions at the model's band (every layer of it, every prompt position):
  knock-out: paper10 (top-10 J++ directions per position, the clean top-10 at the last prompt position protected),
             paper10_rot (the same removal turned by a fixed rotation), unembed10 (the logit lens's top 10),
             paper10_spare (paper10 that never removes the wrong bridge's own token direction, B''s surname token)
  writes:    lens_add of unit(v_X - v_B') x alpha x |h| at the band's layers jointly, at the last prompt position
             ("final") or at every prompt position from the third on ("span"), alpha in 0.1 0.2 0.4 0.8, for X = B (the
             true bridge) and X = C (a control person: another item's true bridge, not B or B'); v = unit J++ lens
             vectors of the first token of " " + surname.
--screen: no edits; which items the target model also answers through the wrong bridge (logP(A') > logP(A) and its
greedy continuation starts with A'), written to results/wrong_bridge/RUN/screen.json; --items-from takes that list.

BJ_TARGET=... python scripts/wrong_bridge_causal.py --name RUN --why W --band LO-HI [--screen] [--items-from SCREEN]
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch  # noqa: E402

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit, rotation  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from bridge_jspace.run_switches import switches
from bridge_jspace.tokens import raw_encoding  # noqa: E402

DATA_FILE = pins.REPO_ROOT / "data" / "wsb_wrong_bridge.json"
OUT = pins.RESULTS_DIR / "wrong_bridge"
ALPHAS = (0.02, 0.05, 0.1, 0.2, 0.4)  # 18 note: 0.8 dropped, smaller added after the smoke
SEED_ROT = 888


def surname_token(tok, name: str) -> int:
    return tok(" " + name.split()[-1], add_special_tokens=False).input_ids[0]


@torch.no_grad()
def answer_lp(model, prompt_ids: list[list[int]], answers: list[list[int]], edit_maker) -> list[float]:
    """Sum of answer-token log-probabilities per row, prompt + answer right-padded into one batch; edit_maker(rows)
    returns {layer: edit} given per-row (prompt length, total length)."""
    seqs = [p + a for p, a in zip(prompt_ids, answers, strict=True)]
    width = max(map(len, seqs))
    pad = model.tokenizer.pad_token_id if model.tokenizer.pad_token_id is not None else model.tokenizer.eos_token_id
    ids = torch.tensor([s + [pad] * (width - len(s)) for s in seqs], device="cuda")
    meta = [(len(p), len(s)) for p, s in zip(prompt_ids, seqs, strict=True)]
    edits = edit_maker(meta, width)

    def hook_for(layer: int):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            new = edits[layer](h.float()).to(h.dtype)
            return (new, *out[1:]) if isinstance(out, tuple) else new

        return hook

    with _forward_hooks([(model.layers[la], hook_for(la)) for la in sorted(edits)]):
        logits = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False).logits.float()
    lp = logits.log_softmax(-1)
    out = []
    for b, (pl, tl) in enumerate(meta):
        out.append(float(sum(lp[b, t - 1, seqs[b][t]] for t in range(pl, tl))))
    return out


@torch.no_grad()  # without it each lens dictionary keeps a vocab x d autograd graph (~5 GB per layer on the 27B)
def main(a) -> None:
    pins.check_run_name(a.name)
    out_dir = OUT / a.name
    assert not out_dir.exists(), f"{out_dir} exists; results are written once"
    items = json.loads(DATA_FILE.read_text())
    items = items if isinstance(items, list) else items["items"]
    if a.limit:
        items = items[: a.limit]
    if a.items_from:
        keep = set(json.loads(Path(a.items_from).read_text())["transfer"])
        items = [it for it in items if it["name"] in keep]
    lo, hi = (int(x) for x in a.band.split("-"))
    band = list(range(lo, hi + 1))
    out_dir.mkdir(parents=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "model": pins.model_pin(), "switches": switches(), "lens": pins.FROZEN_LENS,
                                                       "band": band, "screen": a.screen, "items_from": a.items_from, "n_items": len(items),
                                                       "alphas": ALPHAS, "git_commit": commit, "data": str(DATA_FILE.name),
                                                       "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    P = [list(raw_encoding(tok, it["prompt"])["input_ids"]) for it in items]
    Ap = [tok(" " + it["target"], add_special_tokens=False).input_ids for it in items]
    A = [tok(" " + it["correct_answer"], add_special_tokens=False).input_ids for it in items]
    none = lambda meta, width: {}  # noqa: E731
    t0 = time.time()
    if a.screen:
        rows = []
        for s in range(0, len(items), 8):
            sl = slice(s, s + 8)
            n = len(P[sl])
            lps = answer_lp(model, P[sl] * 2, Ap[sl] + A[sl], none)
            for i, it in enumerate(items[sl]):
                ids = torch.tensor([P[s + i]], device="cuda")
                text = model.generate_batch(ids, 6, [{}])[0]
                rows.append({"name": it["name"], "lp_Ap": lps[i], "lp_A": lps[n + i], "greedy": text,
                             "transfer": lps[i] > lps[n + i] and text.strip().startswith(it["target"])})  # fmt: skip
        tr = [r["name"] for r in rows if r["transfer"]]
        (out_dir / "screen.json").write_text(json.dumps({"transfer": tr, "rows": rows}, indent=1) + "\n")
        (out_dir / "summary.json").write_text(json.dumps({"n": len(rows), "transfer": len(tr), "seconds": round(time.time() - t0)}, indent=2) + "\n")
        print(f"SCREEN {pins.TARGET}: {len(tr)} of {len(rows)} items answered through the wrong bridge")
        return
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    ud = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    rot = {la: rotation(wg.shape[1], SEED_ROT + la) for la in band}
    bp_tok = [surname_token(tok, it["intermediates"][0]) for it in items]
    b_tok = [surname_token(tok, it["true_intermediates"][0]) for it in items]
    rng = random.Random(0)
    c_tok = []
    for i, it in enumerate(items):  # control person: another item's true bridge, neither B nor B'
        pool = [j for j in range(len(items)) if items[j]["true_intermediates"][0] not in (it["true_intermediates"][0], it["intermediates"][0])
                and items[j]["intermediates"][0] != it["true_intermediates"][0]]  # fmt: skip
        c_tok.append(b_tok[rng.choice(pool)])
    unit = lambda la, t: lens.vectors(la, torch.tensor([t], device="cuda"), unit=True)[0]  # noqa: E731
    rows_out = []
    for s in range(0, len(items), a.batch):
        idx = list(range(s, min(s + a.batch, len(items))))
        n = len(idx)
        Pb = [P[i] for i in idx] * 2
        Ab = [Ap[i] for i in idx] + [A[i] for i in idx]
        base = answer_lp(model, Pb, Ab, none)
        # the protected set: the clean top 10 at the last prompt position (as ablate_v2's paper10)
        prot = []
        for i in idx:
            x = torch.tensor([P[i]], device="cuda")
            lg = model.hf(input_ids=x, use_cache=False, logits_to_keep=1).logits[0, -1].float()
            r = row_of[lg.topk(10).indices]
            prot.append(r[r >= 0])
        prot = prot * 2

        def settings(meta, width, extra=None):
            rs = []
            for b, (pl, tl) in enumerate(meta):
                p_ = prot[b] if extra is None else torch.cat([prot[b], extra[b]])
                rs.append(RowSettings(skip=list(range(pl, width)), protected=p_))
            return rs

        def ko(kind: str):
            def make(meta, width):
                if kind == "paper10_spare":
                    sp = [row_of[torch.tensor([bp_tok[i]], device="cuda")] for i in idx] * 2
                    sp = [x[x >= 0] for x in sp]
                    rs = settings(meta, width, sp)
                else:
                    rs = settings(meta, width)
                d_ = (lambda la: ud) if kind == "unembed10" else (lambda la: dic[la])
                return {la: removal_edit("top", d_(la), rs, rotation=rot[la] if kind == "paper10_rot" else None, k=10) for la in band}
            return make

        def write(target: list[int], posset: str, alpha: float, where: str = "joint"):
            layers_ = band if where == "joint" else [band[len(band) // 2]]

            def make(meta, width):
                eds = {}
                for la in layers_:
                    dirs = [torch.nn.functional.normalize(unit(la, target[i]) - unit(la, bp_tok[i]), dim=0) for i in idx] * 2

                    def edit(h, dirs=dirs, meta=meta):
                        h = h.clone()
                        for b, (pl, tl) in enumerate(meta):
                            pos = [pl - 1] if posset == "final" else list(range(2, pl))
                            hp = h[b, pos]
                            h[b, pos] = hp + alpha * hp.norm(dim=-1, keepdim=True) * dirs[b]
                        return h

                    eds[la] = edit
                return eds
            return make

        conds = {k: ko(k) for k in ("paper10", "paper10_rot", "unembed10", "paper10_spare")}
        for tgt_name, tgt in (("B", b_tok), ("C", c_tok)):
            for where in ("joint", "mid"):
                for posset in ("final", "span"):
                    for al in ALPHAS:
                        conds[f"write_{tgt_name}/{where}/{posset}/{al}"] = write(tgt, posset, al, where)
        for cname, mk in conds.items():
            lps = answer_lp(model, Pb, Ab, mk)
            for j, i in enumerate(idx):
                rows_out.append({"name": items[i]["name"], "hop2": items[i]["hop2"], "condition": cname,
                                 "base_Ap": base[j], "base_A": base[n + j], "lp_Ap": lps[j], "lp_A": lps[n + j]})  # fmt: skip
        print(f"{len(rows_out)} rows, {time.time() - t0:.0f}s", flush=True)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows_out))
    summary = summarise(rows_out)
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    for k, v in summary["conditions"].items():
        if not k.startswith("write"):
            print(f"WB {k:22s} dlp(A') {v['d_lp_Ap']:+.2f}  dmargin {v['d_margin']:+.2f} {v['d_margin_ci']}  flips {v['flip']:.2f}")
    print("WB cross-validated writes:", json.dumps(summary["cv_writes"]))


def summarise(rows: list[dict]) -> dict:
    by = {}
    for r in rows:
        by.setdefault(r["condition"], []).append(r)
    rng = random.Random(0)

    def ci(vals):
        bs = sorted(statistics.mean(rng.choice(vals) for _ in vals) for _ in range(1000))
        return [round(bs[25], 2), round(bs[974], 2)]

    out = {"n_items": len({r["name"] for r in rows}), "conditions": {}}
    for c, rs in by.items():
        dm = [(r["lp_Ap"] - r["lp_A"]) - (r["base_Ap"] - r["base_A"]) for r in rs]
        out["conditions"][c] = {"d_lp_Ap": round(statistics.mean(r["lp_Ap"] - r["base_Ap"] for r in rs), 3),
                                "d_lp_A": round(statistics.mean(r["lp_A"] - r["base_A"] for r in rs), 3),
                                "d_margin": round(statistics.mean(dm), 3), "d_margin_ci": ci(dm),
                                "flip": round(statistics.mean(r["lp_A"] > r["lp_Ap"] for r in rs), 3)}  # fmt: skip
    # cross-validated write: the (posset, alpha) with the most flips for B on even-indexed items, scored on the odd ones
    names = sorted({r["name"] for r in rows})
    even, odd = set(names[0::2]), set(names[1::2])
    cells = sorted({c.split("/", 1)[1] for c in by if c.startswith("write_B/")})
    flips = lambda c, part: statistics.mean(r["lp_A"] > r["lp_Ap"] for r in by[c] if r["name"] in part)  # noqa: E731
    # 18 note: only non-destructive cells are candidates: the better of the two answers loses < 3 nats on even items
    drop = lambda c, part: statistics.mean(max(r["base_Ap"], r["base_A"]) - max(r["lp_Ap"], r["lp_A"])  # noqa: E731
                                           for r in by[c] if r["name"] in part)
    ok = [cell for cell in cells if drop(f"write_B/{cell}", even) < 3.0]
    out["write_cells"] = {cell: {"B_flip": round(flips(f"write_B/{cell}", set(names)), 3), "C_flip": round(flips(f"write_C/{cell}", set(names)), 3),
                                 "B_best_answer_drop": round(drop(f"write_B/{cell}", set(names)), 2)} for cell in cells}  # fmt: skip
    if ok:
        best = max(ok, key=lambda cell: flips(f"write_B/{cell}", even))
        out["cv_writes"] = {"cell": best, "B_flip_heldout": round(flips(f"write_B/{best}", odd), 3),
                            "C_flip_heldout": round(flips(f"write_C/{best}", odd), 3), "candidates": len(ok)}  # fmt: skip
    else:
        out["cv_writes"] = {"cell": None, "note": "no write cell keeps the better answer within 3 nats"}
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--screen", action="store_true")
    ap.add_argument("--items-from", default=None)
    ap.add_argument("--limit", type=int, default=0, help="the first N items only (smoke)")
    main(ap.parse_args())
