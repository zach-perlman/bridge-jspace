"""nn_sd_necessity (2026-10-30; design /home/zach/scratch/redteam_1030/sd_necessity_design.md, prereg amendment pending):
the first necessity test of Ni & Zou's "silent dissent" (arXiv 2610.02702 v2). Their protocol (scripts/sd_prompts.py, a
port of their code): two-hop facts whose bridge is never stated; scripted peers unanimously state another fact's answer;
the agent's own round-0 statement visible, hidden ("(answer submitted)") or absent. Our knock-out (ablate_v2's paper10 and
its controls, every position, a band of layers) asks whether holding the original answer needs the J-space, and whether
that need is recall-specific: with its earlier answer visible the agent can look it up; hidden, it must recompute it.

Stages
  known   their known check for every fact of the chosen categories (hop 1 -> e2, hop 2 -> e3, composed -> e3; greedy 12
          tokens, alias match, their prompt prefix), their pairing per split (peer and control facts among the known ones,
          same category, all bridges and answers distinct), then round 0 (the plain transcript, greedy 12 tokens): items
          answered right enter round 1. Writes results/sd_necessity/NAME/{known.jsonl, items.jsonl, manifest.json, summary.json}.
  ko      per item (split, categories, round 0 right) and conversation (--convs, sd_prompts.CONVS): unedited 12-token greedy
          answers classified as theirs (--gen), then one forward per edit (--edits "BAND:cond,cond" ...; plus the unedited
          one) read at the answer position: the top token over the whole vocabulary (orig = a first token of e3's aliases,
          peer = of e3', ctrl = of the control fact's e3, an answer in no transcript; else other), the 2-way pick (orig vs
          peer by their best logits) and the pick among the category's answers (cand). Each forward also reads the six roles
          (their role probes: original / peers' / control bridge and answer) at the last token with --read-lenses at every
          --read-every'th layer and --read-extra layers: the full-vocabulary rank (0 = top) of the role's best probe token.
          Items whose three answers' first tokens collide are left out of the edited reads (as their injection did).
Edits (one forward each; every position edited; band layers each edited):
  paper10, paper10_rot, paper10_pcasize, unembed10, unembed10_rot, paper10_keepA, paper10_keepA_rot: ablate_v2's, exactly
      (the clean top-10 at the answer position protected; keepA's kept span = the J++ vectors of every form of every answer
      of the item's category)
  bridgeJ / bridgeJ_rot: remove the span of the J++ vectors of every form of the item's own bridge e2 (sd_prompts.forms)
      except the forms of either answer (e3, e3'), at every position (ablate_v2.answer_span_edit's procedure; no protected
      tokens); _rot turns the removal vector. Rows record the span's token count (nb; 0 = no edit)
  bridgeJ_ctrl: the same with the control fact's bridge (same category, in no transcript; also minus the bridge's own
      forms): the semantic control (nc)
  ansJ / ansJ_rot: the same with the category's answers' forms (amendment 58 note 3's ansJ, here)
  bridgeJ_ctrl_rot (amendment 73): bridgeJ_ctrl's removal vector turned (as bridgeJ_rot)
  bridgeJ_peer / _rot (amendment 73): the same with the peers' bridge e2' (minus the forms of e2, e3 and e3'); rows carry np
  bridgeJperp (amendment 72 note 54): bridgeJ's unit vectors projected off the span of the item's two answers' (e3, e3') form
      vectors, columns of norm < 1e-3 dropped, re-orthonormalised; rows carry span_rank (mean kept rank over the band)
  bridgeJ_peerperp / _rot (amendment 75): as bridgeJperp with the peers' bridge forms (bridgeJ_peer's); _rot turns the
      removal vector; rows carry span_rank and ans_share (the forms' mean energy share inside the answers' span)
  With any of these (or --log-prot) every row also carries np and prot ({"orig": bool, "peer": bool}: is that answer's
      main first token in the prompt's protected set, the clean top-10's letter rows). --uids: only these fact uids.
  paper10_skipown / _rot, paper10_onlyown / _rot (amendment 67 note 42): paper10 (and its rotated control) at every position
      except the tokens of the agent's own earlier answer, or only at them (own_positions: the tokens of its round-0
      completion inside its visible statement; the whole statement's tokens are logged beside, own_spans.jsonl). Only for
      conversations with the earlier answer in view (press_vis, press1_vis, ...): elsewhere no edit is made and no row written.

python scripts/nn_sd_necessity.py known --name {P}sd_known_v1 --facts data/sd_v1/facts.jsonl --categories C ... [--per-category N]
python scripts/nn_sd_necessity.py ko --name {P}sd_ko_v1 --items-run {P}sd_known_v1 --split test --convs solo press_vis ...
       --edits "32-40:paper10,paper10_rot,paper10_pcasize,unembed10,bridgeJ,bridgeJ_ctrl" "52-55:paper10,paper10_rot" [--n 8]
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

from bridge_jspace import pins, tokens  # noqa: E402
from scripts import sd_prompts as SP  # noqa: E402

RES = pins.RESULTS_DIR / "sd_necessity"
SEED_ROT = 888  # + layer, as ablate_v2 (seed offset 0)
TOPK_CONDS = ("paper10", "paper10_rot", "paper10_pcasize", "unembed10", "unembed10_rot", "paper10_keepA", "paper10_keepA_rot")
SPAN_CONDS = {"bridgeJ": "bforms", "bridgeJ_rot": "bforms", "bridgeJ_ctrl": "cforms", "ansJ": "aforms", "ansJ_rot": "aforms",
              "bridgeJ_ctrl_rot": "cforms", "bridgeJ_peer": "pforms", "bridgeJ_peer_rot": "pforms"}  # the last three: amendments 72-73
PERP_CONDS = ("bridgeJperp",)  # amendment 72 note 54: bridgeJ's unit vectors orthogonalised to the span of the item's two answers' forms
# amendment 75: the same for the peers' bridge (bridgeJ_peer's forms), and its rotation; rows carry span_rank and ans_share
PEERPERP_CONDS = ("bridgeJ_peerperp", "bridgeJ_peerperp_rot")
PERP_MIN = 1e-3  # columns of norm < 1e-3 after the projection are dropped (amendment 72 note 50's convention)
# amendment 67 note 42: paper10 at every position but the agent's own earlier answer (skipown), or only there (onlyown)
OWN_CONDS = ("paper10_skipown", "paper10_skipown_rot", "paper10_onlyown", "paper10_onlyown_rot")
CONDITIONS = TOPK_CONDS + tuple(SPAN_CONDS) + OWN_CONDS + PERP_CONDS + PEERPERP_CONDS


def own_positions(tok, text: str, spans: list[tuple[str, int, int]], fact: dict, own_answer: str) -> tuple[list[int], list[int]]:
    """Note 42: the token positions of the agent's own earlier answer in a transcript where it is visible (sd_prompts.render's
    "own" span, "<composed> <answer>."): the tokens overlapping the answer's characters (its round-0 completion as written
    there), and, logged beside, the tokens overlapping the whole own statement. ([], []) if the earlier answer is not in view."""
    own = [(a, b) for lab, a, b in spans if lab == "own"]
    if not own or text[own[0][0] : own[0][1]] == SP.WITHHELD:
        return [], []
    a, b = own[0]
    ans = own_answer.strip().rstrip(".")
    start = a + len(fact["composed"]) + 1
    end = start + len(ans)
    assert text[start:end] == ans and text[a:start] == fact["composed"] + " ", (fact["uid"], text[a:b])
    offs = tokens.raw_encoding(tok, text, offsets=True)["offset_mapping"]
    ans_pos = [i for i, (x, y) in enumerate(offs) if x < end and y > start]
    line_pos = [i for i, (x, y) in enumerate(offs) if x < b and y > a]
    return ans_pos, line_pos


def manifest_base(a, stage: str) -> dict:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return {"run": a.name, "stage": stage, "why": a.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "git_commit": commit, "git_state": pins.git_state(), "model": pins.model_pin(),
            "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "args": vars(a),
            "protocol": "Ni & Zou 2026 (arXiv 2610.02702 v2), ported from ziangni-sys/silent-dissent@fe78a9f (scripts/sd_prompts.py)"}  # fmt: skip


def new_dir(name: str) -> Path:
    pins.check_run_name(name)
    out = RES / name
    assert not (out / "summary.json").exists(), f"{out} has results; runs are written once"
    out.mkdir(parents=True, exist_ok=True)
    return out


@torch.no_grad()
def generate(model, prompts: list[str], max_new: int, batch: int, desc: str) -> list[str]:
    """Greedy continuations (first line, their clean_answer) of raw-text prompts: prompts of one token length are batched
    together (no padding), through Model.generate_batch with no edits."""
    ids = [tokens.raw_encoding(model.tokenizer, p)["input_ids"] for p in prompts]
    by_len: dict[int, list[int]] = collections.defaultdict(list)
    for i, x in enumerate(ids):
        by_len[len(x)].append(i)
    out = [""] * len(prompts)
    t0, done = time.time(), 0
    for _, idx in sorted(by_len.items()):
        for s in range(0, len(idx), batch):
            part = idx[s : s + batch]
            t = torch.tensor([ids[i] for i in part], device="cuda")
            texts = model.generate_batch(t, max_new, [{} for _ in part])
            for i, txt in zip(part, texts, strict=True):
                out[i] = SP.clean_answer(txt)
            done += len(part)
        print(f"{desc}: {done}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)
    return out


# ------------------------------------------------------------------------------------------------ known


def stage_known(a) -> None:
    from bridge_jspace.model import load_model

    out_dir = new_dir(a.name)
    facts = [json.loads(line) for line in Path(a.facts).read_text().splitlines()]
    facts = [f for f in facts if f["category"] in a.categories]
    if a.per_category:  # smoke: the first N facts of each category (CSV order), every split
        seen: collections.Counter = collections.Counter()
        keep = []
        for f in facts:
            seen[f["category"]] += 1
            if seen[f["category"]] <= a.per_category:
                keep.append(f)
        facts = keep
    (out_dir / "manifest.json").write_text(json.dumps({**manifest_base(a, "known"), "n_facts": len(facts)}, indent=2) + "\n")
    print(f"{len(facts)} facts in {len({f['category'] for f in facts})} categories", flush=True)
    model = load_model()
    t0 = time.time()
    texts = generate(model, [p for f in facts for p in SP.known_prompts(f)], a.gen_tokens, a.batch, "known")
    known, rows = set(), []
    for i, f in enumerate(facts):
        h1, h2, c = texts[3 * i : 3 * i + 3]
        r = {"uid": f["uid"], "category": f["category"], "split": f["split"], "hop1": SP.matches(h1, f["e2_aliases"]),
             "hop2": SP.matches(h2, f["e3_aliases"]), "composed": SP.matches(c, f["e3_aliases"]), "texts": [h1, h2, c]}  # fmt: skip
        rows.append(r)
        if r["hop1"] and r["hop2"] and r["composed"]:
            known.add(f["uid"])
    (out_dir / "known.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    triples = []
    for split in ("dev", "test"):
        pool = [f for f in facts if f["split"] == split and f["uid"] in known]
        triples += [(split, *t) for t in SP.assign_partners(pool, pool, seed=0)]
    solo = [SP.render(f, p, "solo")[0] for _, f, p, _ in triples]
    r0 = generate(model, solo, a.gen_tokens, a.batch, "round 0")
    items = []
    for (split, f, p, c), ans in zip(triples, r0, strict=True):
        items.append({"split": split, "fact": f, "peer": p, "control": c, "r0_answer": ans, "r0_outcome": SP.classify(ans, f, p)})
    (out_dir / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items))
    summ: dict = {"seconds": round(time.time() - t0), "n_facts": len(facts), "known": len(known), "by": {}}
    for split in ("dev", "test"):
        for cat in a.categories:
            fs = [r for r in rows if r["split"] == split and r["category"] == cat]
            its = [it for it in items if it["split"] == split and it["fact"]["category"] == cat]
            summ["by"][f"{split}/{cat}"] = {"facts": len(fs), "known": sum(r["uid"] in known for r in fs), "items": len(its),
                                            "round0_right": sum(it["r0_outcome"] == "original" for it in its)}  # fmt: skip
    for split in ("dev", "test"):
        its = [it for it in items if it["split"] == split]
        summ[f"{split}_items"] = len(its)
        summ[f"{split}_round0_right"] = sum(it["r0_outcome"] == "original" for it in its)
        summ[f"{split}_round0_accuracy"] = round(summ[f"{split}_round0_right"] / max(1, len(its)), 4)
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print(json.dumps(summ, indent=1), flush=True)


# ------------------------------------------------------------------------------------------------ ko


def parse_edits(specs: list[str]) -> list[tuple[tuple[int, ...], list[str]]]:
    out = []
    for s in specs:
        band, conds = s.split(":")
        lo, hi = (map(int, band.split("-")) if "-" in band else (int(band), int(band)))
        cs = conds.split(",")
        bad = [c for c in cs if c not in CONDITIONS]
        assert not bad, f"unknown edits {bad}; known: {CONDITIONS}"
        out.append((tuple(range(lo, hi + 1)), cs))
    return out


def band_label(band: tuple[int, ...]) -> str:
    return f"L{band[0]}-{band[-1]}"


def span_edit(D, rows: list[torch.Tensor], rotation: torch.Tensor | None = None):
    """ablate_v2.answer_span_edit at every position (nothing outside): each batch row loses its projection onto the span
    of D's unit vectors for rows[b]; with rotation the removal vector is turned (same size). A row with no dictionary row
    is left unchanged."""
    bases = []
    for r in rows:
        bases.append(torch.linalg.qr(D.atoms(r).double().T)[0] if r.numel() else None)

    def edit(h: torch.Tensor) -> torch.Tensor:
        out = h.float().clone()
        for b, Q in enumerate(bases):
            if Q is None:
                continue
            x = out[b].double()
            r = (x @ Q) @ Q.T
            if rotation is not None:
                r = r @ rotation.double().T
            out[b] = (x - r).float()
        return out

    return edit


def perp_span_edit(D, brows: list[torch.Tensor], arows: list[torch.Tensor], rotation: torch.Tensor | None = None):
    """Amendment 72 note 54's bridgeJperp (and amendment 75's bridgeJ_peerperp with the peers' bridge rows): as span_edit
    (every position, no protection), with each row's span = the unit vectors of its bridge rows projected off the span of its
    two answers' form rows, columns of norm < PERP_MIN dropped, re-orthonormalised (QR); with rotation (amendment 75's _rot)
    the removal vector is turned, as span_edit's. The returned edit carries .ranks (each row's kept rank; 0 = no edit) and
    .ans_share (each row's mean share of its unit bridge vectors' energy inside the answers' span; None without bridge rows)."""
    bases, shares = [], []
    for rb, ra in zip(brows, arows, strict=True):
        Q, sh = None, None
        if rb.numel():
            B = D.atoms(rb).double().T  # [d, nb] unit columns
            if ra.numel():
                Qa = torch.linalg.qr(D.atoms(ra).double().T)[0]
                PB = Qa @ (Qa.T @ B)
                sh = float((PB * PB).sum() / (B * B).sum())
                B = B - PB
            else:
                sh = 0.0
            B = B[:, B.norm(dim=0) >= PERP_MIN]
            Q = torch.linalg.qr(B)[0] if B.shape[1] else None
        bases.append(Q)
        shares.append(sh)

    def edit(h: torch.Tensor) -> torch.Tensor:
        out = h.float().clone()
        for b, Q in enumerate(bases):
            if Q is None:
                continue
            x = out[b].double()
            if rotation is None:
                out[b] = (x - (x @ Q) @ Q.T).float()
            else:
                out[b] = (x - ((x @ Q) @ Q.T) @ rotation.double().T).float()
        return out

    edit.ranks = [0 if Q is None else Q.shape[1] for Q in bases]
    edit.ans_share = shares
    return edit


@torch.no_grad()
def forward_read(model, ids: torch.Tensor, edits: dict, last: torch.Tensor, layers: list[int]):
    """ablate.first_token_logits (right-padded rows, each read at its own last position) that also returns each row's
    residual at its last position at `layers` ([B, d] fp32, after that layer's edit, if any), and each row's edit size
    (||edit|| / ||h|| averaged over its real positions and the edited layers; 0 without edits)."""
    from bridge_jspace.model import _forward_hooks

    rec: dict[int, torch.Tensor] = {}
    rel: list[torch.Tensor] = []  # per edited layer: each row's mean ||edit|| / ||h|| over its real positions
    rows = torch.arange(ids.shape[0], device=ids.device)
    real = (torch.arange(ids.shape[1], device=ids.device)[None, :] <= last[:, None]).float()  # [B, T]
    want = set(layers)

    def hook_for(layer: int):
        def hook(_m, _a, out):
            h = out[0] if isinstance(out, tuple) else out
            if layer in edits:
                h0 = h.float()
                h1 = edits[layer](h0)
                r = (h1 - h0).norm(dim=-1) / h0.norm(dim=-1).clamp_min(1e-6)
                rel.append((r * real).sum(1) / real.sum(1))
                h = h1.to(h.dtype)
            if layer in want:
                rec[layer] = h[rows, last].float()
            if layer not in edits:
                return None
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    keep = last.unique()
    with _forward_hooks([(model.layers[la], hook_for(la)) for la in sorted(set(edits) | want)]):
        out = model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=keep)
    if out.logits.shape[1] == ids.shape[1]:
        logits = out.logits[rows, last]
    else:
        logits = out.logits[rows, torch.searchsorted(keep, last)]
    size = torch.stack(rel).mean(0).tolist() if rel else [0.0] * ids.shape[0]
    return logits.float(), rec, size


def role_ranks(logits: torch.Tensor, probes: list[dict[str, list[int]]]) -> list[dict[str, int]]:
    """Per row: each role's best full-vocabulary rank (0 = top; the number of tokens with a strictly higher logit) over its
    probe tokens; -1 for a role with none."""
    s = logits.sort(dim=1).values
    V = logits.shape[1]
    U = max(1, max(len({t for ids in p.values() for t in ids}) for p in probes))
    idx = torch.zeros(len(probes), U, dtype=torch.long)
    cols = []
    for b, p in enumerate(probes):
        u = sorted({t for ids in p.values() for t in ids})
        cols.append({t: j for j, t in enumerate(u)})
        if u:
            idx[b, : len(u)] = torch.tensor(u)
    idx = idx.to(logits.device)
    vals = logits.gather(1, idx).contiguous()
    rk = (V - torch.searchsorted(s.contiguous(), vals, right=True)).cpu().tolist()
    out = []
    for b, p in enumerate(probes):
        out.append({role: (min(rk[b][cols[b][t]] for t in ids) if ids else -1) for role, ids in p.items()})
    return out


def read_answer(logits: torch.Tensor, p: dict) -> dict:
    """The answer reads of one row's final logits [V]."""
    top = int(logits.argmax())
    tg = p["targets"]
    cls = next((k for k in ("orig", "peer", "ctrl") if top in tg[k]), "other")
    lo, lp = logits[tg["orig"]].max(), logits[tg["peer"]].max()
    logp = logits.log_softmax(-1)
    c = torch.tensor(p["cands"], device=logits.device)
    ctop = int(c[logits[c].argmax()])
    ccls = next((k for k in ("orig", "peer", "ctrl") if ctop in tg[k]), "other")
    return {"top_id": top, "cls": cls, "pick2": "orig" if lo > lp else "peer", "margin": round(float(lo - lp), 4),
            "lp_orig": round(float(logp[tg["main"]["orig"]]), 4), "lp_peer": round(float(logp[tg["main"]["peer"]]), 4),
            "cand_cls": ccls}  # fmt: skip


@torch.no_grad()  # 2026-10-30: without it every LensDictionary kept its full wg @ J product in an autograd graph (wg comes from
#                    lm_head.weight, a parameter): ~4.6 GB per band layer on the 27B (its OOM). Values are bit-identical either way.
def stage_ko(a) -> None:
    from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit, rotation
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = new_dir(a.name)
    torch.backends.cuda.matmul.allow_tf32 = True
    edits_spec = parse_edits(a.edits)
    items = [json.loads(line) for line in (RES / a.items_run / "items.jsonl").read_text().splitlines()]
    items = [it for it in items if (a.split == "all" or it["split"] == a.split) and it["r0_outcome"] == "original"
             and (not a.categories or it["fact"]["category"] in a.categories)]  # fmt: skip
    if a.uids:  # amendment 73 (note 54 extended, 27B): only these fact uids (one value that is a file: one uid per line; uids hold spaces)
        one = len(a.uids) == 1 and Path(a.uids[0]).is_file()
        want = {x.strip() for x in Path(a.uids[0]).read_text().splitlines() if x.strip()} if one else set(a.uids)
        items = [it for it in items if it["fact"]["uid"] in want]
    if a.n and a.n < len(items):  # a seeded random subset (smoke)
        items = random.Random(a.seed).sample(items, a.n)
    model = load_model()
    tok = model.tokenizer
    n_layers = pins.N_LAYERS
    # the category's answer vocabulary: every answer (fact, peer or control) of the loaded items, per category
    vocab: dict[str, set[str]] = collections.defaultdict(set)
    for it in items:
        for k in ("fact", "peer", "control"):
            vocab[it["fact"]["category"]].add(it[k]["e3"])
    cands = {cat: sorted(SP.first_ids(tok, sorted(v))) for cat, v in vocab.items()}
    aforms = {cat: sorted({t for x in sorted(v) for t in SP.forms(tok, x)}) for cat, v in vocab.items()}
    prompts, n_collide, leak = [], 0, collections.Counter()
    need_own = any(c in OWN_CONDS for _, cs in edits_spec for c in cs)  # note 42 only: the earlier answer's token span
    for it in items:
        f, p, c = it["fact"], it["peer"], it["control"]
        tg = SP.answer_targets(tok, f, p, c)
        n_collide += tg["collide"]
        probes = SP.role_probes(tok, f, p, c)
        # bridgeJ's spans: every form of the bridge minus every form of either answer of the item (a university named after
        # its city must not take the answer's directions with it), and the same for the control fact's bridge
        ans_f = set(SP.forms(tok, f["e3"])) | set(SP.forms(tok, p["e3"]))
        bforms = sorted(set(SP.forms(tok, f["e2"])) - ans_f)
        cforms = sorted(set(SP.forms(tok, c["e2"])) - ans_f - set(SP.forms(tok, f["e2"])))
        # amendment 73: bridgeJ_peer's span, the peers' bridge e2' minus the forms of e2, e3 and e3' (as bridgeJ for e2)
        pforms = sorted(set(SP.forms(tok, p["e2"])) - ans_f - set(SP.forms(tok, f["e2"])))
        for conv in a.convs:
            text, spans = SP.render(f, p, conv, own_answer=it["r0_answer"], control=c)  # control: amendment 84's instr_city_lure only
            tail = f" {SP.norm(text[len(SP.PLAIN_HEADER) + len(SP.PLAIN_SHOTS):])} "
            bnamed = any(SP.norm(x) and f" {SP.norm(x)} " in tail for x in f["e2_aliases"])  # an alias of the bridge is written
            leak[conv] += bnamed  # (descriptive; the reader can leave such items out: --drop-bridge-named)
            prompts.append({"uid": f["uid"], "split": it["split"], "category": f["category"], "bridge": f["e2"], "conv": conv,
                            "text": text, "ids": tokens.raw_encoding(tok, text)["input_ids"], "targets": tg,
                            "collide": tg["collide"], "bnamed": bnamed, "probes": probes, "cands": sorted(set(cands[f["category"]]) | set(tg["orig"]) | set(tg["peer"])),
                            "bforms": bforms, "cforms": cforms, "aforms": aforms[f["category"]], "pforms": pforms, "ansforms": sorted(ans_f)})  # fmt: skip
            if need_own:
                prompts[-1]["own_pos"], prompts[-1]["own_line_pos"] = own_positions(tok, text, spans, f, it["r0_answer"])
    read = [p for p in prompts if not p["collide"]]
    lens = JLens(model, pins.FROZEN_LENS)
    read_lenses = {"jpp": lens}
    for name in a.read_lenses:
        if name == "logit":
            read_lenses["logit"] = None
        elif name != "jpp" and name != pins.FROZEN_LENS:
            read_lenses[name] = JLens(model, name)  # a lens in pins.LENS_SOURCES (27B: "jlens", the paper's lens file)
    src = set(int(x) for x in lens.source_layers)
    read_layers = sorted({la for la in src if la % a.read_every == 0} | (set(a.read_extra) & src))
    manifest = {**manifest_base(a, "ko"), "n_items": len(items), "n_prompts": len(prompts), "n_read": len(read),
                "items_collide": n_collide, "prompts_naming_bridge": dict(leak), "read_layers": read_layers,
                "read_lenses": sorted(read_lenses), "edits": [[band_label(b), cs] for b, cs in edits_spec],
                "seeds": {"rotation": f"{SEED_ROT}+layer"}, "cand_sizes": {k: len(v) for k, v in cands.items()},
                "aforms_sizes": {k: len(v) for k, v in aforms.items()}}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with (out_dir / "prompts_sample.txt").open("w") as fh:  # two rendered prompts per conversation, for the record
        for conv in a.convs:
            for p in [q for q in prompts if q["conv"] == conv][:2]:
                fh.write(f"===== {conv} {p['uid']} ({len(p['ids'])} tokens)\n{p['text']}\n\n")
    if need_own:  # note 42: the earlier answer's token span per prompt, for the record
        with (out_dir / "own_spans.jsonl").open("w") as fh:
            for p in prompts:
                fh.write(json.dumps({"uid": p["uid"], "conv": p["conv"], "own_pos": p["own_pos"], "own_tokens": [tok.decode([p["ids"][i]]) for i in p["own_pos"]],
                                     "own_line_pos": p["own_line_pos"]}, ensure_ascii=False) + "\n")  # fmt: skip
    print(f"{len(items)} items, {len(prompts)} prompts ({len(read)} read; {n_collide} items collide); edits {manifest['edits']}", flush=True)
    t0 = time.time()
    if a.gen:  # their outcome: unedited greedy 12 tokens, classified as theirs
        answers = generate(model, [p["text"] for p in prompts], a.gen_tokens, a.gen_batch, "round 1 (unedited)")
        by_uid = {it["fact"]["uid"]: it for it in items}
        with (out_dir / "gen.jsonl").open("w") as fh:
            for p, ans in zip(prompts, answers, strict=True):
                it = by_uid[p["uid"]]
                fh.write(json.dumps({"uid": p["uid"], "conv": p["conv"], "answer": ans,
                                     "outcome": SP.classify(ans, it["fact"], it["peer"])}, ensure_ascii=False) + "\n")  # fmt: skip
    # the edits' dictionaries (ablate_v2's)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    elayers = sorted({la for b, _ in edits_spec for la in b})
    assert max(elayers) <= n_layers - 2, "the last edited layer is n_layers - 2 (the final block is the lens's target)"
    dic = {la: LensDictionary(wg, lens.J(la)) for la in elayers}
    rot = {la: rotation(wg.shape[1], SEED_ROT + la) for la in elayers}
    all_conds = {c for _, cs in edits_spec for c in cs}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda")) if any(c.startswith("unembed") for c in all_conds) else None
    pca, PCA_K = {}, None
    if any(c.endswith("_pcasize") for c in all_conds):
        from scripts.ablate_v2 import PCA_K, pca_dictionaries

        pca = pca_dictionaries(model, sorted({la for b, cs in edits_spec for la in b if any(c.endswith("_pcasize") for c in cs)}))

    def rows_of(toks: list[int]) -> torch.Tensor:
        r = row_of[torch.tensor(toks, dtype=torch.long, device="cuda")] if toks else torch.zeros(0, dtype=torch.long, device="cuda")
        return r[r >= 0].unique()

    def make_edit(cond: str, la: int, chunk: list[dict], protected: list[torch.Tensor], width: int = 0):
        if cond in PERP_CONDS:  # amendment 72 note 54
            return perp_span_edit(dic[la], [rows_of(p["bforms"]) for p in chunk], [rows_of(p["ansforms"]) for p in chunk])
        if cond in PEERPERP_CONDS:  # amendment 75: the peers' bridge (pforms), orthogonalised to both answers' forms
            return perp_span_edit(dic[la], [rows_of(p["pforms"]) for p in chunk], [rows_of(p["ansforms"]) for p in chunk],
                                  rotation=rot[la] if cond.endswith("_rot") else None)
        if cond in OWN_CONDS:  # note 42: paper10 with the earlier answer's tokens left unedited (skipown) or edited alone (onlyown)
            rs = []
            for i, p in enumerate(chunk):
                own = set(p.get("own_pos") or [])
                if not own:  # the earlier answer is not in view: no edit (and no row is written)
                    skip = list(range(width))
                elif "skipown" in cond:
                    skip = sorted(own)
                else:
                    skip = [t for t in range(width) if t not in own]
                rs.append(RowSettings(skip=skip, protected=protected[i]))
            return removal_edit("top", dic[la], rs, rotation=rot[la] if cond.endswith("_rot") else None, k=10)
        if cond in SPAN_CONDS:
            return span_edit(dic[la], [rows_of(p[SPAN_CONDS[cond]]) for p in chunk], rot[la] if cond.endswith("_rot") else None)
        keep = None
        if "_keepA" in cond:
            keep = []
            for p in chunk:
                rr = rows_of(p["aforms"])
                keep.append(torch.linalg.qr(dic[la].atoms(rr).double().T)[0])
        return removal_edit("top", unembed if cond.startswith("unembed") else dic[la],
                            [RowSettings(skip=[], protected=protected[i]) for i in range(len(chunk))],
                            rotation=rot[la] if cond.endswith("_rot") else None, k=10,
                            size_match=pca[la].D[:PCA_K] if cond.endswith("_pcasize") else None, keep_span=keep)  # fmt: skip

    def lens_ranks(rec: dict, chunk: list[dict]) -> list[dict]:
        out = [{} for _ in chunk]
        probes = [p["probes"] for p in chunk]
        for name, ln in read_lenses.items():
            per = [{role: [] for role in SP.ROLES} for _ in chunk]
            for la in read_layers:
                lg = model.unembed(rec[la]) if ln is None else ln.readout(rec[la], la)
                for b, rr in enumerate(role_ranks(lg.float(), probes)):
                    for role, v in rr.items():
                        per[b][role].append(v)
            for b in range(len(chunk)):
                out[b][name] = per[b]
        return out

    # amendments 72-73: rows carry np (bridgeJ_peer's span size) and prot ({"orig", "peer"}: is that answer's main first token in
    # the prompt's protected set, the clean top-10's letter rows) when the run has any of their edits, or with --log-prot;
    # otherwise rows are as before, byte for byte
    tail = a.log_prot or bool(all_conds & (set(PERP_CONDS) | set(PEERPERP_CONDS) | {"bridgeJ_ctrl_rot", "bridgeJ_peer", "bridgeJ_peer_rot"}))
    if tail:
        manifest["row_tail"] = ["np", "prot"]
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    rows_path = out_dir / "rows.jsonl"
    assert not rows_path.exists(), f"{rows_path} exists"
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    order = sorted(read, key=lambda p: len(p["ids"]))
    n_rows, band_seconds = 0, collections.Counter()
    for start in range(0, len(order), a.batch):
        chunk = order[start : start + a.batch]
        width = max(len(p["ids"]) for p in chunk)
        ids = torch.tensor([p["ids"] + [pad_id] * (width - len(p["ids"])) for p in chunk], device="cuda")
        last = torch.tensor([len(p["ids"]) - 1 for p in chunk], device="cuda")
        out_rows = []
        clean, rec, _ = forward_read(model, ids, {}, last, read_layers)
        protected = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
        lr = lens_ranks(rec, chunk)
        ext = [{} for _ in chunk]
        if tail:
            for b, p in enumerate(chunk):
                pr = set(protected[b].tolist())
                ext[b] = {"np": len(p["pforms"]), "prot": {k: int(row_of[p["targets"]["main"][k]]) in pr for k in ("orig", "peer")}}
        for b, p in enumerate(chunk):
            out_rows.append({"uid": p["uid"], "conv": p["conv"], "split": p["split"], "category": p["category"], "bridge": p["bridge"],
                             "bnamed": p["bnamed"], "nb": len(p["bforms"]), "nc": len(p["cforms"]), "band": "-", "cond": "none", **read_answer(clean[b], p), "ranks": lr[b],
                             **ext[b]})  # fmt: skip
        for band, conds in edits_spec:
            tb = time.time()
            for cond in conds:
                edits = {la: make_edit(cond, la, chunk, protected, width) for la in band}
                logits, rec, size = forward_read(model, ids, edits, last, read_layers)
                lr = lens_ranks(rec, chunk)
                for b, p in enumerate(chunk):
                    if cond in OWN_CONDS and not p.get("own_pos"):
                        continue
                    sr = {"span_rank": round(sum(edits[la].ranks[b] for la in band) / len(band), 2)} if cond in PERP_CONDS + PEERPERP_CONDS else {}
                    if cond in PEERPERP_CONDS:  # amendment 75: the peers' bridge span's energy share inside the answers' span
                        shs = [edits[la].ans_share[b] for la in band if edits[la].ans_share[b] is not None]
                        sr["ans_share"] = round(sum(shs) / len(shs), 4) if shs else None
                    out_rows.append({"uid": p["uid"], "conv": p["conv"], "split": p["split"], "category": p["category"],
                                     "bridge": p["bridge"], "bnamed": p["bnamed"], "nb": len(p["bforms"]), "nc": len(p["cforms"]), "band": band_label(band), "cond": cond,
                                     "edit_rel": round(size[b], 5), **read_answer(logits[b], p),
                                     "ranks": lr[b], **ext[b], **sr})  # fmt: skip
            band_seconds[band_label(band)] += time.time() - tb
        with rows_path.open("a") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in out_rows)
        n_rows += len(out_rows)
        print(f"{n_rows} rows, {start + len(chunk)}/{len(order)} prompts, {time.time() - t0:.0f}s", flush=True)
    # a plain summary (the reader does the statistics)
    cells: dict = collections.defaultdict(dict)
    acc: dict = collections.defaultdict(list)
    for line in rows_path.read_text().splitlines():
        r = json.loads(line)
        acc[(r["conv"], f"{r['band']}/{r['cond']}")].append(r)
    for (conv, bc), rs in sorted(acc.items()):
        n = len(rs)
        cells[conv][bc] = {"n": n, **{k: round(sum(r["cls"] == k for r in rs) / n, 4) for k in ("orig", "peer", "ctrl", "other")},
                           "pick2_peer": round(sum(r["pick2"] == "peer" for r in rs) / n, 4),
                           "cand_peer": round(sum(r["cand_cls"] == "peer" for r in rs) / n, 4)}  # fmt: skip
    summ = {"seconds": round(time.time() - t0), "band_seconds": {k: round(v) for k, v in band_seconds.items()}, "cells": cells}
    if a.gen:
        g: dict = collections.defaultdict(collections.Counter)
        for line in (out_dir / "gen.jsonl").read_text().splitlines():
            r = json.loads(line)
            g[r["conv"]][r["outcome"]] += 1
        summ["gen"] = {conv: {k: round(v / sum(c.values()), 4) for k, v in c.items()} | {"n": sum(c.values())} for conv, c in g.items()}
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print(json.dumps(summ, indent=1)[:4000], flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    k = sub.add_parser("known")
    k.add_argument("--name", required=True)
    k.add_argument("--why", required=True)
    k.add_argument("--facts", default="data/sd_v1/facts.jsonl")
    k.add_argument("--categories", nargs="+", required=True)
    k.add_argument("--per-category", type=int, default=0, help="smoke: the first N facts of each category")
    k.add_argument("--gen-tokens", type=int, default=12)
    k.add_argument("--batch", type=int, default=64)
    o = sub.add_parser("ko")
    o.add_argument("--name", required=True)
    o.add_argument("--why", required=True)
    o.add_argument("--items-run", required=True, help="the known stage's run name")
    o.add_argument("--split", default="test", choices=["test", "dev", "all"])
    o.add_argument("--categories", nargs="*", default=None)
    o.add_argument("--convs", nargs="+", default=["solo", "agree_vis", "agree_hid", "press_vis", "press_hid"], choices=sorted(SP.CONVS))
    o.add_argument("--edits", nargs="+", required=True, help='"LO-HI:cond,cond" per band')
    o.add_argument("--n", type=int, default=0, help="a seeded random N items (smoke); 0: all")
    o.add_argument("--seed", type=int, default=0)
    o.add_argument("--batch", type=int, default=32)
    o.add_argument("--gen", action="store_true", help="also their 12-token greedy answers, unedited")
    o.add_argument("--gen-tokens", type=int, default=12)
    o.add_argument("--gen-batch", type=int, default=64)
    o.add_argument("--read-lenses", nargs="*", default=["jpp"], help='jpp (the frozen lens), logit, or a pins lens name ("jlens": 27B)')
    o.add_argument("--read-every", type=int, default=2)
    o.add_argument("--read-extra", nargs="*", type=int, default=[], help="more read layers (e.g. their band)")
    o.add_argument("--uids", nargs="*", default=None, help="only these fact uids (or one file of uids, one per line)")
    o.add_argument("--log-prot", action="store_true", help="rows carry np and prot even without an amendment 72-73 edit")
    args = ap.parse_args()
    {"known": stage_known, "ko": stage_ko}[args.stage](args)
