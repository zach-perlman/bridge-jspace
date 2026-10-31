"""nn_sd67_datactl (2026-10-30, prereg amendment 88 note 67 "as decided", and its addendum: the 27B primary): a positive control
built from data for answer-orthogonal removal. Note 62: removing the stated city C's J++ span costs the one-hop "{C} is in the
country of" 25-42 points, but the same span orthogonalised to the answers' forms (bridgeJperp) costs ~0. Can a removal that is
orthogonal to the answers (and to a data-defined country subspace) see the subject at all? The removed span here is a
city-identity subspace fitted on data, not the J++ lens's forms.

Fit (inside ko when --fit does not exist yet; deterministic, a few seconds after the model load)
  Cities: every city (bridge e2) of --items-run's person-birthcity-cntry items, dev and test, any round-0 outcome; each city's
  country = its items' e3 (the most common; cities with two are counted in the log). Each city in TEMPLATES (6 neutral
  sentences that never name a country; C never the first token); the residual (the output of each band layer, where the edits
  act) at C's last token, averaged over the templates per city; centred over cities. No answer labels are used for the means.
    raw    an orthonormal basis of the centred city means' span (SVD; singular values < 1e-6 of the top dropped); no cap
    clean  raw projected off the country subspace (the country class means of the same city vectors, cities grouped by their
           country, centred over countries; SVD basis, same tolerance) with ablate_v2.perp_basis (|R_jj| < 1e-3 dropped)
  Logged per layer: the ranks, each basis's mean energy share inside the span of every listed country's J++ forms, and the
  share of the centred city means' energy in clean and in the country subspace. torch.save to --fit (city and country names
  ride along: keep it out of git).
Ko: test split, person-birthcity-cntry, round-0-right items (nn_sd_necessity ko's selection; --n: its seeded sample), the
  conversations onehop (O), solo (P), ctx2hop (I) as note 62 (sd_prompts; ctx2hop's fact list from ctx2hop_spec with note 62's
  pool and avoid rule). Every edit acts only from the question's first token (note 62's mask, nn_sd_necessity.masked_edit).
  Per band of --edits:
    cityRaw       remove the projection onto raw (one basis for every item)
    cityClean     clean projected off the span of the item's answers' J++ forms (ablate_v2.perp_basis; in O and P the two
                  answers e3, e3', in I the 4 listed countries: bridgeJperp's spans); rank logged
    cityRaw_RE, cityClean_RE   energy-matched random residual-space directions: the columns of a Haar orthogonal matrix
                  (ablate.rotation(d, 6700 + layer)) in a per-item order (Random("n67:" + uid)); per item AND layer, k = the
                  smallest prefix whose energy at the edited positions (masked, real tokens; the hook's input) reaches the
                  target's removed energy at that layer, both measured in the target's own forward (note 57's loop, per layer)
    cityClean_RJ  beside: the same matching with random J++ dictionary rows (one pool per layer: Random("n67j:" + layer)
                  samples min(d, 2048) letter rows; Gram-Schmidt order, so a prefix of k columns spans the first k rows)
    bridgeJperp   note 62's arm, exactly (nn_sd_necessity.perp_span_edit)
  A target's forward precedes its _RE / _RJ in the band (asserted). Rows (results/sd_necessity/NAME/rows.jsonl):
  nn_sd_necessity's answer read (cls orig = a first token of K's aliases), edit size, span_rank (mean kept rank over the band),
  per layer k, E_target and E_match (shares of the edited positions' energy), reached. --gen: the unedited 12-token greedy
  answers classified as theirs (gen.jsonl, for the first-token agreement check); edited generations are not made.

python scripts/nn_sd67_datactl.py ko --name {P}sd67_ko_test_v1 --why W --items-run {P}sd_known_v1 --fit /workspace/scratch/n67/{P}fit.pt \
       --edits "16-24:cityRaw,cityRaw_RE,cityClean,cityClean_RE,cityClean_RJ,bridgeJperp" "32-40:..." [--gen] [--n 8]
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins, tokens  # noqa: E402
from scripts import nn_sd_necessity as NS  # noqa: E402
from scripts import sd_prompts as SP  # noqa: E402

RES = NS.RES
CAT = "person-birthcity-cntry"
SEED_RE = 6700  # + layer: the _RE pools' Haar basis
RJ_POOL = 2048  # the _RJ pool's size (random J++ letter rows), d if smaller
SV_TOL = 1e-6  # singular values below this share of the top one are dropped
# amendment 88 note 67: neutral sentences that never name a country; C never the first token (Qwen has no BOS, so token 0 is
# the attention sink): two of the coordinator's examples ("{C} hosted the event.", "{C} came up in conversation.") get a lead-in
TEMPLATES = ("I visited {C} last year.", "Last month, {C} hosted the event.", "There is a story about {C}.",
             "Many people have heard of {C}.", "Yesterday, {C} came up in conversation.", "I read about {C} yesterday.")  # fmt: skip
CONDS = ("cityRaw", "cityRaw_RE", "cityClean", "cityClean_RE", "cityClean_RJ", "bridgeJperp")
MATCH_OF = {"cityRaw_RE": "cityRaw", "cityClean_RE": "cityClean", "cityClean_RJ": "cityClean"}


def c_last(tok, text: str, name: str) -> int:
    """The last token overlapping the name's characters (its first occurrence)."""
    i = text.find(name)
    assert i >= 0, name
    j = i + len(name)
    offs = tokens.raw_encoding(tok, text, offsets=True)["offset_mapping"]
    return max(t for t, (x, y) in enumerate(offs) if x < j and y > i)


@torch.no_grad()
def collect(model, seqs: list[tuple[list[int], int]], layers: list[int], batch: int) -> dict[int, torch.Tensor]:
    """Per sequence (ids, position): each layer's output residual there ([N, d] fp32 on the GPU); right-padded batches."""
    from bridge_jspace.model import _forward_hooks

    pad = model.tokenizer.pad_token_id if model.tokenizer.pad_token_id is not None else model.tokenizer.eos_token_id
    d = int(model.hf.lm_head.weight.shape[1])
    out = {la: torch.zeros(len(seqs), d, device="cuda") for la in layers}
    order = sorted(range(len(seqs)), key=lambda i: len(seqs[i][0]))
    for s in range(0, len(order), batch):
        part = order[s : s + batch]
        width = max(len(seqs[i][0]) for i in part)
        ids = torch.tensor([seqs[i][0] + [pad] * (width - len(seqs[i][0])) for i in part], device="cuda")
        pos = torch.tensor([seqs[i][1] for i in part], device="cuda")
        rows = torch.arange(len(part), device="cuda")
        idx = torch.tensor(part, device="cuda")

        def hook_for(la, pos=pos, rows=rows, idx=idx):
            def hook(_m, _a, o):
                out[la][idx] = (o[0] if isinstance(o, tuple) else o)[rows, pos].float()

            return hook

        with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
            model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
    return out


def svd_basis(M: torch.Tensor) -> torch.Tensor:
    """An orthonormal basis [d, r] of the row span of M [n, d] (double); singular values < SV_TOL of the top dropped."""
    _, S, Vh = torch.linalg.svd(M.double(), full_matrices=False)
    if not S.numel() or S[0] <= 0:
        return torch.zeros(M.shape[1], 0, dtype=torch.float64, device=M.device)
    return Vh[: int((S > SV_TOL * S[0]).sum())].T.contiguous()


def dictionary(model):
    """ablate_v2's letter-token dictionary pieces: wg [n, d] and the token -> row map."""
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    return wg, row_of


@torch.no_grad()
def fit_entities(model, names: list[str], classes: list[str], layers: list[int], batch: int, meta: dict, out: Path) -> dict:
    """The identity subspaces (module docstring) of `names`, cleaned of the subspace of their `classes`' class means, per
    layer; saved to `out` (atomically) with a .json log beside."""
    from bridge_jspace.ablate import LensDictionary
    from bridge_jspace.lens import JLens
    from scripts.ablate_v2 import perp_basis

    tok = model.tokenizer
    seqs, own = [], []
    for ci, c in enumerate(names):
        for t in TEMPLATES:
            text = t.format(C=c)
            seqs.append((tokens.raw_encoding(tok, text)["input_ids"], c_last(tok, text, c)))
            own.append(ci)
    t0 = time.time()
    X = collect(model, seqs, layers, batch)
    own_t = torch.tensor(own, device="cuda")
    kset = sorted(set(classes))
    kidx = torch.tensor([kset.index(k) for k in classes], device="cuda")
    lens = JLens(model, pins.FROZEN_LENS)
    wg, row_of = dictionary(model)
    allc = sorted({t for k in kset for t in SP.forms(tok, k)})
    ar = row_of[torch.tensor(allc, device="cuda")]
    ar = ar[ar >= 0].unique()
    res: dict = {"layers": {}, "log": {}, "names": names, "classes": classes, "templates": list(TEMPLATES), "n_names": len(names),
                 "n_classes": len(kset), "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                 "min_c_pos": min(p for _, p in seqs), **meta}  # fmt: skip
    for la in layers:
        means = torch.zeros(len(names), X[la].shape[1], device="cuda", dtype=torch.float64).index_add_(0, own_t, X[la].double())
        means /= len(TEMPLATES)
        V = means - means.mean(0, keepdim=True)
        raw = svd_basis(V)
        km = torch.zeros(len(kset), V.shape[1], device="cuda", dtype=torch.float64).index_add_(0, kidx, means)
        km /= torch.bincount(kidx, minlength=len(kset)).double()[:, None]
        Qc = svd_basis(km - km.mean(0, keepdim=True))
        clean = perp_basis(Qc, raw.T)
        Qa = torch.linalg.qr(LensDictionary(wg, lens.J(la)).atoms(ar).double().T)[0]
        tot = float(V.pow(2).sum())

        def share_in(B_, Q=Qa):
            return round(float((Q.T @ B_).pow(2).sum()) / max(B_.shape[1], 1), 4)

        res["layers"][la] = {"raw": raw.float().cpu(), "clean": clean.float().cpu()}
        res["log"][la] = {"rank_raw": raw.shape[1], "rank_class": Qc.shape[1], "rank_clean": clean.shape[1],
                          "raw_share_in_class_forms": share_in(raw), "clean_share_in_class_forms": share_in(clean),
                          "n_class_form_rows": int(ar.numel()),
                          "energy_in_clean": round(float((V @ clean).pow(2).sum()) / tot, 4) if tot else None,
                          "energy_in_class": round(float((V @ Qc).pow(2).sum()) / tot, 4) if tot else None,
                          "mean_norm": round(float(means.norm(dim=1).mean()), 2), "mean_norm_centred": round(float(V.norm(dim=1).mean()), 2)}  # fmt: skip
    res["seconds"] = round(time.time() - t0)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    torch.save(res, tmp)
    tmp.rename(out)
    out.with_suffix(".json").write_text(json.dumps({k: v for k, v in res.items() if k not in ("layers", "names", "classes")}, indent=1) + "\n")
    print(f"fit: {len(names)} names, {len(kset)} classes, {res['seconds']}s; "
          + "; ".join(f"L{la} raw {v['rank_raw']} class {v['rank_class']} clean {v['rank_clean']}" for la, v in res["log"].items()), flush=True)  # fmt: skip
    return res


def fit_sd(model, a, layers: list[int]) -> dict:
    """Note 67's city fit: every city of --items-run's person-birthcity-cntry items (dev and test, any outcome), its country
    the most common e3 of its items."""
    every = [json.loads(line) for line in (RES / a.items_run / "items.jsonl").read_text().splitlines()]
    cc: dict = collections.defaultdict(collections.Counter)
    for it in every:
        if it["fact"]["category"] == CAT:
            cc[it["fact"]["e2"].strip()][it["fact"]["e3"].strip()] += 1
    cities = sorted(cc)
    meta = {"items_run": a.items_run, "n_names_two_classes": sum(len(cc[c]) > 1 for c in cities)}
    return fit_entities(model, cities, [cc[c].most_common(1)[0][0] for c in cities], layers, a.fit_batch, meta, Path(a.fit))


def fit_v4(model, a, layers: list[int]) -> dict:
    """Note 67's v4 fit: every bridge of the set's MM items (any eligibility), its class the MM answer (memory_answer)."""
    from scripts import tasks_v2 as T

    bb: dict = collections.defaultdict(collections.Counter)
    for it in T.load(a.tasks):
        if it["word"] == "MM":
            bb[it["bridge"].strip()][it["memory_answer"].strip()] += 1
    names = sorted(bb)
    meta = {"tasks": a.tasks, "n_names_two_classes": sum(len(bb[c]) > 1 for c in names)}
    return fit_entities(model, names, [bb[c].most_common(1)[0][0] for c in names], layers, a.fit_batch, meta, Path(a.fit))


def parse_edits(specs: list[str], conds_ok: tuple) -> list[tuple[tuple[int, ...], list[str]]]:
    out = []
    for s in specs:
        band, conds = s.split(":")
        lo, hi = (map(int, band.split("-")) if "-" in band else (int(band), int(band)))
        cs = conds.split(",")
        assert all(c in conds_ok for c in cs), f"unknown edits {cs}; known {conds_ok}"
        for c in cs:
            if c in MATCH_OF:
                assert MATCH_OF[c] in cs and cs.index(MATCH_OF[c]) < cs.index(c), f"{c} needs {MATCH_OF[c]} before it"
        out.append((tuple(range(lo, hi + 1)), cs))
    return out


def basis_edit(Qs: list):
    """Each batch row loses its projection onto its orthonormal basis Qs[b] ([d, r] double; r = 0: unchanged)."""

    def edit(h: torch.Tensor) -> torch.Tensor:
        out = h.float().clone()
        for b, Q in enumerate(Qs):
            if Q.shape[1] == 0:
                continue
            x = out[b].double()
            out[b] = (x - (x @ Q) @ Q.T).float()
        return out

    edit.ranks = [int(Q.shape[1]) for Q in Qs]
    return edit


def observed(inner, la: int, emask: torch.Tensor, Qs: list, pools: dict, acc: list):
    """Note 57's matching, per layer: on the hook's input h at the edited positions (emask [B, T]), per row the target's
    removed energy |h Q_b|^2, the total |h|^2, and each pool's per-column energy (pools: name -> (P [d, m] orthonormal fp32,
    per-row column orders or None)), into acc[b][la]. Returns inner(h), unchanged."""

    def f(h: torch.Tensor) -> torch.Tensor:
        for b in range(h.shape[0]):
            x = h[b][emask[b, : h.shape[1]]].float()
            l = acc[b].setdefault(la, {"target": 0.0, "tot": 0.0})
            if Qs[b].shape[1]:
                l["target"] += float((x.double() @ Qs[b]).pow(2).sum())
            l["tot"] += float(x.double().pow(2).sum())
            for name, (P, order) in pools.items():
                c = (x @ P).pow(2).sum(0).double()
                if order is not None:
                    c = c[order[b]]
                l[name] = c if name not in l else l[name] + c
        return inner(h)

    f.ranks = inner.ranks
    return f


def match_k(l: dict, name: str) -> tuple[int, bool, float]:
    """The smallest prefix of pool `name` whose energy reaches the target's: (k, reached, the prefix's energy)."""
    cum = l[name].cumsum(0)
    hit = (cum >= l["target"]).nonzero()
    k = int(hit[0]) + 1 if hit.numel() else int(cum.numel())
    return k, bool(hit.numel()), float(cum[k - 1])


class Arms:
    """Every arm's machinery for one model and fit: the J++ dictionaries, the fitted bases, the random pools."""

    @torch.no_grad()
    def __init__(self, model, F: dict, spec: list):
        from bridge_jspace.ablate import LensDictionary, rotation
        from bridge_jspace.lens import JLens

        self.spec = spec
        elayers = sorted({la for b, _ in spec for la in b})
        assert max(elayers) <= pins.N_LAYERS - 2
        assert all(la in F["layers"] for la in elayers), "the fit lacks a band layer"
        lens = JLens(model, pins.FROZEN_LENS)
        wg, self.row_of = dictionary(model)
        self.dic = {la: LensDictionary(wg, lens.J(la)) for la in elayers}
        self.d = d = wg.shape[1]
        self.raw = {la: F["layers"][la]["raw"].to("cuda").double() for la in elayers}
        self.clean = {la: F["layers"][la]["clean"].to("cuda").double() for la in elayers}
        kinds = {kind(c) for _, cs in spec for c in cs}
        self.G = {la: rotation(d, SEED_RE + la).float() for la in elayers} if kinds & {"Raw_RE", "Clean_RE"} else {}
        self.RJ = {}
        if "Clean_RJ" in kinds:
            for la in elayers:
                rr = torch.tensor(random.Random(f"n67j:{la}").sample(range(wg.shape[0]), min(d, RJ_POOL)), device="cuda")
                self.RJ[la] = torch.linalg.qr(self.dic[la].atoms(rr).double().T)[0].float()

    def rows_of(self, toks: list[int]) -> torch.Tensor:
        r = self.row_of[torch.tensor(toks, dtype=torch.long, device="cuda")] if toks else torch.zeros(0, dtype=torch.long, device="cuda")
        return r[r >= 0].unique()

    @torch.no_grad()
    def run(self, model, chunk: list[dict], pad_id: int, read_fn, base: list[dict], band_seconds) -> list[dict]:
        """One right-padded batch: the unedited read, then every band x arm, each acting from the row's mask_from on."""
        from scripts.ablate_v2 import perp_basis

        B, d = len(chunk), self.d
        width = max(len(p["ids"]) for p in chunk)
        ids = torch.tensor([p["ids"] + [pad_id] * (width - len(p["ids"])) for p in chunk], device="cuda")
        last = torch.tensor([len(p["ids"]) - 1 for p in chunk], device="cuda")
        mf = torch.tensor([p["mask_from"] for p in chunk], device="cuda")
        ar_ = torch.arange(width, device="cuda")[None, :]
        pm = ar_ >= mf[:, None]  # note 62's mask (pads after a row's last token are edited too; they never reach its read)
        emask = pm & (ar_ <= last[:, None])  # the energies: masked, real tokens
        perms = [torch.tensor(random.Random(f"n67:{p['uid']}").sample(range(d), d), device="cuda") for p in chunk] if self.G else None
        logits0, _, _ = NS.forward_read(model, ids, {}, last, [])
        out_rows = [{**base[b], "band": "-", "cond": "none", **read_fn(logits0[b], p)} for b, p in enumerate(chunk)]
        for band, conds in self.spec:
            tb = time.time()
            accs: dict = {}  # target cond -> per row {layer: energies}
            for cond in conds:
                kd = kind(cond)
                ext = [{} for _ in chunk]
                if cond in MATCH_OF:
                    pool = "G" if kd.endswith("_RE") else "J"
                    l_ = accs[MATCH_OF[cond]]
                    ms = [[match_k(l_[b][la], pool) for la in band] for b in range(B)]
                    edits = {la: basis_edit([(self.G[la][:, perms[b][: ms[b][j][0]]] if pool == "G" else self.RJ[la][:, : ms[b][j][0]]).double()
                                             for b in range(B)]) for j, la in enumerate(band)}  # fmt: skip
                    for b in range(B):
                        tots = [l_[b][la]["tot"] for la in band]
                        ext[b] = {"k": [m[0] for m in ms[b]], "reached": all(m[1] for m in ms[b]),
                                  "E_target": [round(l_[b][la]["target"] / t, 6) if t else None for la, t in zip(band, tots, strict=True)],
                                  "E_match": [round(m[2] / t, 6) if t else None for m, t in zip(ms[b], tots, strict=True)]}  # fmt: skip
                elif kd == "bridgeJperp":  # note 62's arm, exactly
                    edits = {la: NS.perp_span_edit(self.dic[la], [self.rows_of(p["bforms"]) for p in chunk], [self.rows_of(p["perp_forms"]) for p in chunk])
                             for la in band}  # fmt: skip
                else:
                    qby = {}
                    for la in band:
                        if kd == "Raw":
                            qby[la] = [self.raw[la]] * B
                        else:  # Clean: off the span of the item's answers' J++ forms (perp_forms)
                            qby[la] = []
                            for p in chunk:
                                ra = self.rows_of(p["perp_forms"])
                                Qa = torch.linalg.qr(self.dic[la].atoms(ra).double().T)[0] if ra.numel() else torch.zeros(d, 0, device="cuda", dtype=torch.float64)
                                qby[la].append(perp_basis(Qa, self.clean[la].T))
                    edits = {la: basis_edit(qby[la]) for la in band}
                    pools = [k_ for k_, suf in (("G", "_RE"), ("J", "_RJ")) if f"{cond}{suf}" in conds]
                    if pools:  # note 57's loop: measure in this forward, per layer
                        accs[cond] = [{} for _ in chunk]
                        edits = {la: observed(e, la, emask, qby[la], {k_: ((self.G[la], perms) if k_ == "G" else (self.RJ[la], None)) for k_ in pools}, accs[cond])
                                 for la, e in edits.items()}  # fmt: skip
                edits = {la: NS.masked_edit(e, pm) for la, e in edits.items()}
                logits, _, size = NS.forward_read(model, ids, edits, last, [])
                for b, p in enumerate(chunk):
                    r = {**base[b], "band": NS.band_label(band), "cond": cond, "edit_rel": round(size[b], 5), **read_fn(logits[b], p), **ext[b]}
                    if kd in ("Raw", "Clean", "bridgeJperp"):
                        r["span_rank"] = round(sum(edits[la].ranks[b] for la in band) / len(band), 2)
                    if cond in accs:
                        r["E_target"] = [round(accs[cond][b][la]["target"] / accs[cond][b][la]["tot"], 6) if accs[cond][b][la]["tot"] else None for la in band]
                    out_rows.append(r)
            band_seconds[NS.band_label(band)] += time.time() - tb
        return out_rows


def kind(cond: str) -> str:
    """cityRaw / entRaw -> Raw, cityClean_RE -> Clean_RE, ...; bridgeJperp as is."""
    for pre in ("city", "ent"):
        if cond.startswith(pre):
            return cond[len(pre) :]
    return cond


def load_fit(model, a, layers: list[int], fitter) -> tuple[dict, float, str]:
    t = time.time()
    if Path(a.fit).exists():
        F = torch.load(a.fit, weights_only=False)
        assert F["model"] == pins.model_pin(), "the fit is another model's"
        assert all(la in F["layers"] for la in layers), "the fit lacks a band layer"
    else:
        F = fitter(model, a, sorted(set(layers) | set(a.fit_layers)))
    return F, time.time() - t, hashlib.sha256(Path(a.fit).read_bytes()).hexdigest()


def finish(out_dir: Path, rows_path: Path, t0: float, t_fit: float, band_seconds, F: dict, manifest: dict, group: str, ok: str, okfn) -> None:
    """summary.json: per group (conversation / word) and band/cond, n and the read's share (ok)."""
    acc: dict = collections.defaultdict(list)
    for line in rows_path.read_text().splitlines():
        r = json.loads(line)
        acc[(r[group], f"{r['band']}/{r['cond']}")].append(r)
    cells: dict = collections.defaultdict(dict)
    for (g, bc), rs in sorted(acc.items()):
        cells[g][bc] = {"n": len(rs), ok: round(sum(bool(okfn(r)) for r in rs) / len(rs), 4)}
    summ = {"seconds": round(time.time() - t0), "fit_seconds": round(t_fit), "band_seconds": {k: round(v) for k, v in band_seconds.items()},
            "peak_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2), "fit_log": F["log"], "cells": cells,
            "command": " ".join(sys.argv), "git_commit": manifest["git_commit"]}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print(json.dumps(summ, indent=1)[:5000], flush=True)


@torch.no_grad()
def stage_ko(a) -> None:
    from bridge_jspace.model import load_model

    out_dir = NS.new_dir(a.name)
    torch.backends.cuda.matmul.allow_tf32 = True
    spec = parse_edits(a.edits, CONDS)
    every = [json.loads(line) for line in (RES / a.items_run / "items.jsonl").read_text().splitlines()]
    items = [it for it in every if it["split"] == a.split and it["r0_outcome"] == "original" and it["fact"]["category"] == CAT]
    if a.n and a.n < len(items):  # nn_sd_necessity's --n: a seeded random subset
        items = random.Random(a.seed).sample(items, a.n)
    model = load_model()
    tok = model.tokenizer
    F, t_fit, fit_sha = load_fit(model, a, sorted({la for b, _ in spec for la in b}), fit_sd)
    assert F.get("items_run") == a.items_run, "the fit is another run's"
    assert all(it["fact"]["e2"].strip() in set(F["names"]) for it in items), "an item's city is not in the fit"
    pool62: dict = collections.defaultdict(list)
    for x in every:
        pool62[(x["split"], x["fact"]["category"])].append(x["fact"])
    vocab = {x["e3"] for it in items for x in (it["fact"], it["peer"], it["control"])}
    cands = sorted(SP.first_ids(tok, sorted(vocab)))
    prompts, n_collide = [], 0
    for it in items:
        f, p, c = it["fact"], it["peer"], it["control"]
        tg = SP.answer_targets(tok, f, p, c)
        n_collide += tg["collide"]
        ans_f = set(SP.forms(tok, f["e3"])) | set(SP.forms(tok, p["e3"]))
        bforms = sorted(set(SP.forms(tok, f["e2"])) - ans_f)
        ctx = SP.ctx2hop_spec(f, pool62[(it["split"], f["category"])], tok, seed=a.seed, avoid=(p, c)) if "ctx2hop" in a.convs else None
        for conv in a.convs:
            text, _ = SP.render(f, p, conv, own_answer=it["r0_answer"], control=c, ctx=ctx if conv == "ctx2hop" else None)
            ids = tokens.raw_encoding(tok, text)["input_ids"]
            offs = tokens.raw_encoding(tok, text, offsets=True)["offset_mapping"]
            qc = SP.question_char(text)
            q_pos = next(i for i, (x, y) in enumerate(offs) if y > qc)
            assert offs[q_pos][0] <= qc
            perp = sorted({t for x in [f] + ctx["dist"] for t in SP.forms(tok, x["e3"])}) if conv == "ctx2hop" else sorted(ans_f)
            prompts.append({"uid": f["uid"], "split": it["split"], "category": f["category"], "bridge": f["e2"], "conv": conv,
                            "ids": ids, "targets": tg, "collide": tg["collide"], "cands": sorted(set(cands) | set(tg["orig"]) | set(tg["peer"])),
                            "bforms": bforms, "perp_forms": perp, "q_pos": q_pos, "mask_from": q_pos, "text": text})  # fmt: skip
    read = [p for p in prompts if not p["collide"]]
    arms = Arms(model, F, spec)
    d = arms.d
    manifest = {**NS.manifest_base(a, "ko"), "note": "prereg amendment 88 note 67 (sd stage)", "fit": a.fit, "fit_sha256": fit_sha,
                "fit_log": F["log"], "fit_n_names": F["n_names"], "fit_n_classes": F["n_classes"], "templates": list(TEMPLATES),
                "n_items": len(items), "n_prompts": len(prompts), "n_read": len(read), "items_collide": n_collide,
                "edits": [[NS.band_label(b), cs] for b, cs in spec], "pos_from": "question",
                "seeds": {"re_pool": f"ablate.rotation(d, {SEED_RE}+layer), order Random('n67:'+uid)",
                          "rj_pool": f"Random('n67j:'+layer).sample(letter rows, {min(d, RJ_POOL)})", "items": a.seed}}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with (out_dir / "prompts_sample.txt").open("w") as fh:
        for conv in a.convs:
            for p in [q for q in prompts if q["conv"] == conv][:1]:
                fh.write(f"===== {conv} {p['uid']} ({len(p['ids'])} tokens; mask from {p['q_pos']})\n{p['text']}\n\n")
    print(f"{len(items)} items, {len(prompts)} prompts ({len(read)} read; {n_collide} collide); fit {t_fit:.0f}s; edits {manifest['edits']}", flush=True)
    t0 = time.time()
    if a.gen:  # the unedited 12-token outcome (the first-token agreement check), as nn_sd_necessity's --gen
        answers = NS.generate(model, [p["text"] for p in prompts], 12, a.gen_batch, "unedited 12 tokens")
        by_uid = {it["fact"]["uid"]: it for it in items}
        with (out_dir / "gen.jsonl").open("w") as fh:
            for p, ans in zip(prompts, answers, strict=True):
                it = by_uid[p["uid"]]
                fh.write(json.dumps({"uid": p["uid"], "conv": p["conv"], "answer": ans,
                                     "outcome": SP.classify(ans, it["fact"], it["peer"])}, ensure_ascii=False) + "\n")  # fmt: skip
    rows_path = out_dir / "rows.jsonl"
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    order = sorted(read, key=lambda p: len(p["ids"]))
    band_seconds: collections.Counter = collections.Counter()
    n_rows = 0
    for start in range(0, len(order), a.batch):
        chunk = order[start : start + a.batch]
        base = [{"uid": p["uid"], "conv": p["conv"], "split": p["split"], "category": p["category"], "bridge": p["bridge"],
                 "nb": len(p["bforms"]), "q_pos": p["q_pos"], "mask_from": p["q_pos"]} for p in chunk]  # fmt: skip
        out_rows = arms.run(model, chunk, pad_id, NS.read_answer, base, band_seconds)
        with rows_path.open("a") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in out_rows)
        n_rows += len(out_rows)
        print(f"{n_rows} rows, {start + len(chunk)}/{len(order)} prompts, {time.time() - t0:.0f}s, peak {torch.cuda.max_memory_allocated() / 2**30:.1f} GB", flush=True)
    finish(out_dir, rows_path, t0, t_fit, band_seconds, F, manifest, "conv", "K", lambda r: r["cls"] == "orig")


@torch.no_grad()
def stage_v4(a) -> None:
    """Note 67's v4 stage: note 37's v4 items (ablate_v2.tasks_prompts, its competence eligibility and nn_swap.v4_split's gate;
    the cand2 read), MP and MM, every edit from the question's first token (ablate_v2.question_start: the passage untouched);
    entRaw / entClean (cleaned of the MM answers' class means, then per item of the relation's answer forms, ablate_v2's
    `forms`) and their energy-matched randoms."""
    from bridge_jspace.model import load_model
    from scripts import ablate_v2 as A2
    from scripts.nn_swap import v4_split

    out_dir = NS.new_dir(a.name)
    torch.backends.cuda.matmul.allow_tf32 = True
    spec = parse_edits(a.edits, V4_CONDS)
    model = load_model()
    tok = model.tokenizer
    prompts = A2.tasks_prompts(tok, a.tasks, a.tasks_competence, a.tasks_words, a.n, ["clean"], a.tasks_level, ("core",), True, None)
    v4ok = {i for i, s_ in v4_split(a.tasks_competence, a.tasks_v4_h1, a.tasks).items() if s_ == "ok"}
    prompts = [p for p in prompts if p["id"] in v4ok]
    if a.n_smoke:  # smoke: a seeded random N items per word
        by: dict = collections.defaultdict(list)
        for p in prompts:
            by[p["family"]].append(p)
        keep = {p["id"] for f, ps in by.items() for p in random.Random(f"{a.seed}:{f}").sample(ps, min(a.n_smoke, len(ps)))}
        prompts = [p for p in prompts if p["id"] in keep]
    F, t_fit, fit_sha = load_fit(model, a, sorted({la for b, _ in spec for la in b}), fit_v4)
    assert F.get("tasks") == a.tasks, "the fit is another set's"
    names = set(F["names"])
    assert all(p["bridge"].strip() in names for p in prompts), "a prompt's bridge is not in the fit"
    for p in prompts:
        p["uid"] = p["id"]
        q0 = A2.question_start(tok, p["ids"])
        p["mask_from"] = q0
        p["perp_forms"] = p["forms"]  # the relation's answer span A (note 37's forms)
    arms = Arms(model, F, spec)
    d = arms.d
    manifest = {**NS.manifest_base(a, "v4"), "note": "prereg amendment 88 note 67 (v4 stage)", "fit": a.fit, "fit_sha256": fit_sha,
                "fit_log": F["log"], "fit_n_names": F["n_names"], "fit_n_classes": F["n_classes"], "templates": list(TEMPLATES),
                "n_prompts": len(prompts), "by_word": dict(collections.Counter(p["family"] for p in prompts)),
                "edits": [[NS.band_label(b), cs] for b, cs in spec], "pos_from": "question (ablate_v2.question_start)", "read": "cand2",
                "seeds": {"re_pool": f"ablate.rotation(d, {SEED_RE}+layer), order Random('n67:'+id)",
                          "rj_pool": f"Random('n67j:'+layer).sample(letter rows, {min(d, RJ_POOL)})", "smoke": a.seed}}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"{len(prompts)} prompts {manifest['by_word']}; fit {t_fit:.0f}s; edits {manifest['edits']}", flush=True)
    rows_path = out_dir / "rows.jsonl"
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    order = sorted(prompts, key=lambda p: len(p["ids"]))
    band_seconds: collections.Counter = collections.Counter()
    t0, n_rows = time.time(), 0

    def read_fn(logits, p):
        x = A2.reads(logits, p, "cand2")
        return {k: x[k] for k in ("correct", "correct_top", "correct_cand2", "top_id", "pick2")}

    for start in range(0, len(order), a.batch):
        chunk = order[start : start + a.batch]
        base = [{"id": p["id"], "family": p["family"], "domain": p["domain"], "bridge": p["bridge"], "n_tokens": len(p["ids"]),
                 "mask_from": p["mask_from"], "n_forms": len(p["forms"])} for p in chunk]  # fmt: skip
        out_rows = arms.run(model, chunk, pad_id, read_fn, base, band_seconds)
        with rows_path.open("a") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in out_rows)
        n_rows += len(out_rows)
        print(f"{n_rows} rows, {start + len(chunk)}/{len(order)} prompts, {time.time() - t0:.0f}s, peak {torch.cuda.max_memory_allocated() / 2**30:.1f} GB", flush=True)
    finish(out_dir, rows_path, t0, t_fit, band_seconds, F, manifest, "family", "correct", lambda r: r["correct"])


V4_CONDS = ("entRaw", "entRaw_RE", "entClean", "entClean_RE", "entClean_RJ")
MATCH_OF.update({"entRaw_RE": "entRaw", "entClean_RE": "entClean", "entClean_RJ": "entClean"})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    o = sub.add_parser("ko", help="the sd stage")
    o.add_argument("--items-run", required=True, help="nn_sd_necessity's known stage run")
    o.add_argument("--split", default="test", choices=["test", "dev"])
    o.add_argument("--convs", nargs="+", default=["onehop", "solo", "ctx2hop"])
    o.add_argument("--n", type=int, default=0, help="a seeded random N items (smoke); 0: all")
    o.add_argument("--gen", action="store_true", help="the unedited 12-token answers (gen.jsonl), for the agreement check")
    o.add_argument("--gen-batch", type=int, default=64)
    v = sub.add_parser("v4", help="the v4 stage")
    v.add_argument("--tasks", default="jsuite_v4_test_chat")
    v.add_argument("--tasks-competence", required=True)
    v.add_argument("--tasks-v4-h1", required=True)
    v.add_argument("--tasks-words", nargs="+", default=["MP", "MM"])
    v.add_argument("--tasks-level", default="all")
    v.add_argument("--n", type=int, default=1000, help="tasks_prompts' n per word (note 37: 1000)")
    v.add_argument("--n-smoke", type=int, default=0, help="smoke: a seeded random N items per word")
    for x in (o, v):
        x.add_argument("--name", required=True)
        x.add_argument("--why", required=True)
        x.add_argument("--fit", required=True, help="the fit (torch file); fitted here first if it does not exist")
        x.add_argument("--fit-layers", nargs="*", type=int, default=[], help="more layers to fit beside the band layers")
        x.add_argument("--fit-batch", type=int, default=64)
        x.add_argument("--edits", nargs="+", required=True, help='"LO-HI:cond,cond" per band')
        x.add_argument("--seed", type=int, default=0)
        x.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()
    {"ko": stage_ko, "v4": stage_v4}[args.stage](args)
