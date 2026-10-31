"""removal_textloss: does J-space removal break the model on plain text, or only on our tasks? (Zach, 2026-10-20,
overnight; on Gemma 4 31B-it the J-space removal breaks every task, lookups too, while a size-matched rotated removal
breaks none.) Mean next-token loss (nats) over 16 WikiText rows of 64+ tokens (first 128 tokens, predictions from
position 4 on) under: none, the J-space removal (ablate_pilot's Remove, all positions, the layers at once) and the
size-matched rotated control (ablate_pilot's Rotated). No verdict rule; the comparison is between models.
2026-10-21 (Zach: is Gemma broken by the current knock-out too, or only by the 25-atom one?): --conditions adds topK and
topK_rot, the headline knock-out's removal (the span of the K highest-scoring lens directions at every position,
ablate_v2's removal_edit "top") and its same-size rotated control (seed 888 + layer, as ablate_v2). Plain text has no
single answer, so nothing is protected: harsher than the task knock-out, which keeps the answer's top 10.

python scripts/removal_textloss.py --name N --why W --layers L [L ...] [--conditions none jspace rotated top10 top10_rot]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit
from bridge_jspace.ablate import rotation as rotation_v2
from bridge_jspace.model import _forward_hooks
from bridge_jspace.run_switches import switches
from bridge_jspace.tokens import raw_encoding
from scripts.ablate_pilot import Remove, Rotated, rotation

RESULTS = pins.RESULTS_DIR / "removal_textloss"


@torch.no_grad()
def main(name: str, why: str, layers: tuple[int, ...], conditions: tuple[str, ...]) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(layers), "conditions": list(conditions),
                "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    every = {"none": {}}
    if {"jspace", "rotated"} & set(conditions):  # 2026-10-23: only when asked (vocab x d per layer; OOMed the 122B)
        jd = {la: lens.vectors(la, letters) for la in layers}
        every |= {"jspace": {la: Remove(jd[la]) for la in layers},
                  "rotated": {la: Rotated(jd[la], rotation(jd[la].shape[1], 888 + la)) for la in layers}}  # fmt: skip
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    for c in conditions:
        if c.startswith("top"):  # topK[_nosink][_rot] (2026-10-21: _nosink leaves attention-sink positions unedited)
            k = int(c[3:].removesuffix("_rot").removesuffix("_nosink"))
            rot = c.endswith("_rot")
            every[c] = {la: _top(dic[la], k, rotation_v2(wg.shape[1], 888 + la) if rot else None, "_nosink" in c)
                        for la in layers}  # fmt: skip
        elif c.startswith("unembed"):  # 2026-10-23: the logit lens top-K (J = identity), as ablate_v2's unembedK
            k = int(c[7:].removesuffix("_rot").removesuffix("_nosink"))
            rot = c.endswith("_rot")
            ud = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
            every[c] = {la: _top(ud, k, rotation_v2(wg.shape[1], 888 + la) if rot else None, "_nosink" in c)
                        for la in layers}  # fmt: skip
    conds = {c: every[c] for c in conditions}
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:16]

    def hook_for(edit):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            h = edit(h[0].float()).to(h.dtype)[None]
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    losses: dict[str, list[float]] = {c: [] for c in conds}
    for ids in texts:
        x = torch.tensor([ids], device="cuda")
        for cname, edits in conds.items():
            with _forward_hooks([(model.layers[la], hook_for(e)) for la, e in edits.items()]):
                logits = model.hf(input_ids=x, use_cache=False).logits[0].float()
            nll = torch.nn.functional.cross_entropy(logits[3:-1], x[0, 4:], reduction="mean")
            losses[cname].append(float(nll))
    summary = {"n_texts": len(texts), "mean_nll": {c: sum(v) / len(v) for c, v in losses.items()}, "per_text": losses}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["mean_nll"]))


def _top(dic, k: int, rot, skip_sinks: bool = False):
    """ablate_v2's top-K removal for one [T, d] residual (no row settings: every position, nothing protected)."""
    edit = removal_edit("top", dic, [RowSettings()], rotation=rot, k=k, skip_sinks=skip_sinks)
    return lambda h: edit(h[None])[0]


# ---- prereg amendment 72 note 55 (2026-10-30): plain-text top-1 agreement with the clean model (Fig. 22's metric) ----
# Called by scripts/paper_ko_decomp.py --bands (one model load for the tasks and the text); main() above is unchanged.
# Texts: the 64 pinned WikiText rows x 128 tokens of ablate_v2.pca_dictionaries (its rule; the PCA conditions' directions
# are fitted on these same rows), and 64 v4 passages beside (the first 64 distinct passages of jsuite_v4_test_chat in file
# order, each item's prompt as the task runs render it, first 128 tokens). Scored positions: 3 .. T-2 (removal_textloss's:
# predictions from position 4 on). Every position is edited. Agreement: the edited model's top-1 next token equals the
# clean model's; nll beside (nats, against the text's own next token). J and logit-lens conditions protect each
# position's own clean top-10 (their letter-token dictionary rows are never chosen at that position; the task runs
# protect the answer position's top-10 at every position); PCA conditions protect nothing (ablate_v2's pca rule);
# paper10_noprot is paper10 with nothing protected (this script's top10, beside).
TEXT_TOKENS, TEXT_FROM, TEXT_V4_SET = 128, 3, "jsuite_v4_test_chat"
TEXT_CONDS = ("paper10", "paper10_rot", "top3", "top30", "pca3", "pca10", "pca30", "unembed10", "unembed30",
              "paper10_pcasize", "paper10_noprot", "unembed100", "unembed300")  # fmt: skip  # the last two: amendment 74


def wiki_texts(tok, n: int) -> list[list[int]]:
    """ablate_v2.pca_dictionaries' rows (>= 64 words, first 2000 characters, raw encoding, first 128 tokens), first n."""
    from scripts.ablate_v2 import PCA_ROWS

    rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64][:PCA_ROWS][:n]
    return [raw_encoding(tok, r)["input_ids"][:TEXT_TOKENS] for r in rows]


def v4_texts(tok, n: int) -> tuple[list[list[int]], list[str]]:
    """The first n distinct passages of the v4 test set (file order), each item's full prompt as tasks_v2 renders it."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    out, ids, seen = [], [], set()
    for it in T.load(TEXT_V4_SET):
        if it["context"] in seen:
            continue
        seen.add(it["context"])
        out.append(S.ids(tok, T.render(tok, it))[:TEXT_TOKENS])
        ids.append(it["id"])
        if len(out) == n:
            break
    return out, ids


class _PerPositionProtected:
    """A dictionary whose lens logits are -inf at each row's protected dictionary rows (prot [m, 10], -1 = none): the
    per-position protection, for one call of top_span_removal over exactly those m rows (removal_edit's single chunk)."""

    def __init__(self, base, prot: torch.Tensor):
        self.base, self.prot = base, prot

    @property
    def n(self) -> int:
        return self.base.n

    def logits(self, x: torch.Tensor) -> torch.Tensor:
        assert x.shape[0] == self.prot.shape[0], "one chunk per call (rows <= removal_edit's chunk)"
        out = self.base.logits(x)
        ok = self.prot >= 0
        out[torch.arange(x.shape[0], device=x.device)[:, None].expand_as(self.prot)[ok], self.prot[ok]] = float("-inf")
        return out

    def scores(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def atoms(self, idx: torch.Tensor) -> torch.Tensor:
        return self.base.atoms(idx)


def text_edit(cond: str, la: int, dic: dict, unembed, pca: dict, rot: dict, prot: torch.Tensor):
    """The edit of one text condition at layer la for a batch [B, T, d]; prot [B * T, 10] (each position's clean top-10
    as dictionary rows, -1 for a non-letter token)."""
    import re

    from scripts.ablate_v2 import PCA_K, top_k

    base = cond.removesuffix("_noprot")
    k = top_k(base)
    m = re.fullmatch(r"(top|pca|unembed|paper)(\d+)(_rot|_pcasize)?", base)
    assert m and k, cond
    d = pca[la] if m[1] == "pca" else unembed if m[1] == "unembed" else dic[la]
    protect = m[1] != "pca" and not cond.endswith("_noprot")
    kw = {"rotation": rot[la] if base.endswith("_rot") else None, "k": k,
          "size_match": pca[la].D[:PCA_K] if base.endswith("_pcasize") else None}  # fmt: skip

    def edit(h: torch.Tensor) -> torch.Tensor:  # the batch's B rows as rows of B * T positions, in pieces of removal_edit's chunk
        B, T, dd = h.shape
        step = 4096 if k <= 100 else max(128, min(4096, 2**33 // (k * dd * 8)))  # removal_edit's own chunk (one per piece)
        x = h.reshape(B * T, dd)
        out = []
        for s in range(0, B * T, step):
            dp = _PerPositionProtected(d, prot[s : s + step]) if protect else d
            out.append(removal_edit("top", dp, [RowSettings()], **kw)(x[None, s : s + step])[0])
        return torch.cat(out).reshape(B, T, dd)

    return edit


@torch.no_grad()
def agreement(model, texts: list[list[int]], bands: dict[str, list[int]], conds, dic, unembed, pca, rot, row_of,
              batch: int = 16) -> list[dict]:  # fmt: skip
    """Per text, band and condition: agreement count and n over the scored positions, mean nll, and |edit| / |h| (the
    root of the summed squared edit over the summed squared residual, the band's layers and every position)."""
    groups: dict[int, list[int]] = {}
    for i, t in enumerate(texts):
        groups.setdefault(len(t), []).append(i)
    out = []
    for T, members in sorted(groups.items()):
        for b0 in range(0, len(members), batch):
            idx = members[b0 : b0 + batch]
            x = torch.tensor([texts[i] for i in idx], device="cuda")
            full = model.hf(input_ids=x, use_cache=False).logits.float()
            prot = row_of[full.topk(10, dim=-1).indices].reshape(len(idx) * T, 10)  # every position's own clean top-10
            clean_top = full[:, TEXT_FROM:-1].argmax(-1)
            nll0 = torch.nn.functional.cross_entropy(full[:, TEXT_FROM:-1].transpose(1, 2), x[:, TEXT_FROM + 1 :], reduction="none").mean(1)
            del full
            for j, i in enumerate(idx):
                out.append({"text": i, "band": "-", "cond": "none", "agree": int(clean_top.shape[1]), "n": int(clean_top.shape[1]),
                            "nll": float(nll0[j]), "edit_rel": 0.0})  # fmt: skip
            for bname, layers in bands.items():
                for c in conds:
                    acc = torch.zeros(len(idx), 2, dtype=torch.float64, device="cuda")
                    edits = {la: text_edit(c, la, dic, unembed, pca, rot, prot) for la in layers}

                    def hook_for(e, acc=acc):
                        def hook(_module, _args, o):
                            h = o[0] if isinstance(o, tuple) else o
                            hf = h.float()
                            new = e(hf)
                            acc[:, 0] += (new - hf).double().pow(2).sum((1, 2))
                            acc[:, 1] += hf.double().pow(2).sum((1, 2))
                            new = new.to(h.dtype)
                            return (new, *o[1:]) if isinstance(o, tuple) else new

                        return hook

                    tc = time.time()
                    with _forward_hooks([(model.layers[la], hook_for(e)) for la, e in edits.items()]):
                        lg = model.hf(input_ids=x, use_cache=False).logits[:, TEXT_FROM:-1].float()
                    agree = (lg.argmax(-1) == clean_top).sum(1)
                    nll = torch.nn.functional.cross_entropy(lg.transpose(1, 2), x[:, TEXT_FROM + 1 :], reduction="none").mean(1)
                    agree_l, nll_l, rel_l = agree.tolist(), nll.tolist(), (acc[:, 0] / acc[:, 1]).sqrt().tolist()  # syncs the GPU
                    sec = round(time.time() - tc, 3)  # the batch's wall time for this band and condition
                    for j, i in enumerate(idx):
                        out.append({"text": i, "band": bname, "cond": c, "agree": int(agree_l[j]), "n": int(lg.shape[1]),
                                    "nll": float(nll_l[j]), "edit_rel": float(rel_l[j]), "sec": sec})  # fmt: skip
                    del lg
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--layers", nargs="+", type=int, required=True)
    ap.add_argument("--conditions", nargs="+", default=["none", "jspace", "rotated"])
    args = ap.parse_args()
    main(args.name, args.why, tuple(args.layers), tuple(args.conditions))
