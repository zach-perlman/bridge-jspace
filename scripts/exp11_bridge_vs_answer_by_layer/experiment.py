"""exp11_bridge_vs_answer_by_layer: at which layers is the bridge readable, and at which the answer?

Items: the 90 probe-swap prompts. Part B's exp02_swaps/main labels.csv (pinned by sha256) gives each item's status
(eligible = the model answers correctly, part B's definition) and label (J-mediated / non-J / both / neither).
Prompts as published, since the labels were computed on them; `strip_trailing_space` switches.

Readout: the last prompt token (the position that predicts the answer), every source layer, readers logit lens /
J-lens / J++. Four words per item, with part B's token conventions:
  bridge (`intermediate`) and its same-category distractor (`swap_to`): `concept_token`, one id each;
  answer and swap answer: all single-token surfaces (`surface_ids`) for the word rank, `concept_token` in pools.
Two rank spaces, both 1 = top: the word rank over the vocabulary (formatting tokens removed, part B's `word_rank`)
and the rank within a pool (all entities' concept tokens for bridge/distractor; all answers' for answer/swap answer;
chance = 1/pool).

Headlines on eligible items: per layer, the share with the bridge top-1 among entities and the answer top-1 among
answers; per item, whether the layer where the bridge's word rank peaks comes before the first layer where the answer
enters the word top-k. Check: part B's gate_debug had the J-lens bridge top-1 among 96 entities at 0.55-0.70 for
layers 34-48 (66 items).
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any

import numpy as np

from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import probe_swap_items
from bridge_jspace.readout import Reader, formatting_mask, pool_ranks, readout_logits, residuals, word_ranks
from bridge_jspace.stats import bootstrap_mean
from bridge_jspace.tokens import concept_token, surface_ids
from bridge_jspace.utils import progress

from .plot import plot_run

ROLES = ("bridge", "distractor", "answer", "swap_answer")


class BridgeVsAnswer(Experiment):
    def run(self) -> dict[str, Any]:
        p = self.params
        lm, tok = self.model.lm, self.model.tokenizer
        readers: dict[str, Reader] = {"logit": None, **self.lenses}
        layers = {n: list(range(lm.n_layers - 1)) if r is None else r.source_layers for n, r in readers.items()}
        sanity = self.sanity_gate()

        items = load_items(Path(p["labels_file"]), p["labels_sha256"])[: p.get("limit")]
        entity_pool = _pool(tok, [w for it in items for w in (it["intermediate"], it["swap_to"])])
        answer_pool = _pool(tok, [w for it in items for w in (it["answer"], it["swap_answer"])])
        unembed = getattr(lm, "_lm_head")  # noqa: B009 - vocab size of the head, not the tokenizer's
        mask = formatting_mask(tok, unembed.weight.shape[0]).to(self.model.device)
        final = lm.n_layers - 1
        record_at = sorted({final}.union(*layers.values()))

        rows, meta = [], []
        for it in progress(items, "items"):
            prompt = it["prompt"].rstrip() if p["strip_trailing_space"] else it["prompt"]
            ids = lm.encode(prompt)
            resid = residuals(lm, ids, record_at)
            words = {
                "bridge": [concept_token(tok, it["intermediate"])],
                "distractor": [concept_token(tok, it["swap_to"])],
                "answer": surface_ids(tok, it["answer"]),
                "swap_answer": surface_ids(tok, it["swap_answer"]),
            }
            # The model's own answer at the readout token, to compare with part B's status on the same prompts.
            out = lm.unembed(resid[final][[-1]]).float()
            own_rank = int(word_ranks(out, [words["answer"]], mask)[0, 0]) if words["answer"] else None
            meta.append(
                {
                    **{k: it[k] for k in ("name", "category", "status", "label", "intermediate", "swap_to")},
                    "ends_with_space": it["prompt"].endswith(" "),
                    "readout_token": tok.decode(ids[0, -1:]),
                    "own_answer_word_rank": own_rank,
                }
            )
            for rname, reader in readers.items():
                logits = _stack_logits(lm, reader, resid, layers[rname])  # [L, vocab]
                row: dict[str, Any] = {"name": it["name"], "reader": rname, "layers": layers[rname]}
                cands = [words[r] for r in ROLES]
                wr = word_ranks(logits, [c or [0] for c in cands], mask)  # [L, 4]; empty sets masked below
                for j, role in enumerate(ROLES):
                    row[f"{role}_word"] = wr[:, j].tolist() if cands[j] else None
                ent = pool_ranks(logits, [words["bridge"][0], words["distractor"][0]], entity_pool)
                row["bridge_pool"], row["distractor_pool"] = ent[:, 0].tolist(), ent[:, 1].tolist()
                a_id, s_id = _concept_or_none(tok, it["answer"]), _concept_or_none(tok, it["swap_answer"])
                if a_id is None or s_id is None:
                    row["answer_pool"] = row["swap_answer_pool"] = None
                else:
                    ans = pool_ranks(logits, [a_id, s_id], answer_pool)
                    row["answer_pool"], row["swap_answer_pool"] = ans[:, 0].tolist(), ans[:, 1].tolist()
                rows.append(row)
        self.save_jsonl("ranks.jsonl", rows)
        self.save_jsonl("items.jsonl", meta)

        summary = {
            "model": self.cfg.model.name,
            "sanity": sanity,
            "labels_sha256": p["labels_sha256"],
            "strip_trailing_space": p["strip_trailing_space"],
            "pool_sizes": {"entities": len(entity_pool), "answers": len(answer_pool)},
            "own_rank_agrees_with_part_b": _agreement(meta),
            "subsets": aggregate(rows, meta, list(readers), p["band"], p["hit_k"], p["n_boot"], self.cfg.seed),
            "ci": f"95% percentile bootstrap over items, n_boot={p['n_boot']}, seed={self.cfg.seed}",
        }
        plot_run(self.run_dir, band=p["band"])
        return summary


# ---- inputs -----------------------------------------------------------------------------------


def load_items(labels_file: Path, sha256: str) -> list[dict[str, Any]]:
    """Probe-swap items joined with part B's labels (status, label) by name; labels file checked against its pin."""
    blob = labels_file.read_bytes()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha256:
        raise ValueError(f"{labels_file} sha256 {got} != pinned {sha256}")
    labels = {r["name"]: r for r in csv.DictReader(blob.decode().splitlines())}
    items = probe_swap_items()
    if set(labels) != {it["name"] for it in items}:
        raise ValueError("labels.csv and probe_swap.json name different items")
    return [{**it, "status": labels[it["name"]]["status"], "label": labels[it["name"]]["label"]} for it in items]


def _concept_or_none(tok, word: str) -> int | None:
    try:
        return concept_token(tok, word)
    except ValueError:
        return None


def _pool(tok, words: list[str]) -> list[int]:
    """Unique concept tokens of `words` (words without a single-token surface are left out)."""
    return list(dict.fromkeys(t for w in dict.fromkeys(words) if (t := _concept_or_none(tok, w)) is not None))


def _stack_logits(lm, reader: Reader, resid: dict, layers: list[int]):
    import torch

    return torch.cat([readout_logits(lm, reader, resid[layer][[-1]], layer) for layer in layers])


def _agreement(meta: list[dict[str, Any]]) -> dict[str, int]:
    """Our clean answer rank vs part B's status (only meaningful on the as-published prompts)."""
    out = {"both_correct": 0, "both_wrong": 0, "only_part_b_correct": 0, "only_ours_correct": 0}
    for m in meta:
        if m["status"] == "multi_token_answer" or m["own_answer_word_rank"] is None:
            continue
        ours, theirs = m["own_answer_word_rank"] == 1, m["status"] == "eligible"
        key = {(True, True): "both_correct", (False, False): "both_wrong"}.get(
            (ours, theirs), "only_part_b_correct" if theirs else "only_ours_correct"
        )
        out[key] += 1
    return out


# ---- aggregation (pure; unit-tested) ---------------------------------------------------------


def peak_layer(ranks: list[int], layers: list[int]) -> int:
    """Layer of the best (lowest) rank; the earliest on ties."""
    return layers[int(np.argmin(ranks))]


def first_layer_within(ranks: list[int], layers: list[int], k: int) -> int | None:
    """First layer whose rank is <= k, or None."""
    return next((layer for layer, r in zip(layers, ranks, strict=True) if r <= k), None)


def subsets(meta: list[dict[str, Any]]) -> dict[str, list[str]]:
    el = [m for m in meta if m["status"] == "eligible"]
    return {
        "eligible": [m["name"] for m in el],
        "eligible_j_mediated": [m["name"] for m in el if m["label"] == "J-mediated"],
        "eligible_neither": [m["name"] for m in el if m["label"] == "neither"],
        "eligible_ends_with_space": [m["name"] for m in el if m["ends_with_space"]],
        "eligible_no_trailing_space": [m["name"] for m in el if not m["ends_with_space"]],
        "all": [m["name"] for m in meta],
    }


def aggregate(
    rows: list[dict[str, Any]],
    meta: list[dict[str, Any]],
    readers: list[str],
    band: list[int],
    hit_k: int,
    n_boot: int,
    seed: int,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    by_key = {(r["name"], r["reader"]): r for r in rows}
    for subset, names in subsets(meta).items():
        if not names:
            continue
        out[subset] = {"n": len(names)}
        for reader in readers:
            rr = [by_key[(n, reader)] for n in names]
            layers = rr[0]["layers"]
            in_band = [i for i, layer in enumerate(layers) if band[0] <= layer <= band[1]]
            res: dict[str, Any] = {}
            for role in ROLES:
                pool = [r[f"{role}_pool"] for r in rr if r[f"{role}_pool"] is not None]
                if pool:
                    # per item: share of band layers where the word is top-1 in its pool
                    res[f"{role}_pool_top1_band"] = _ci(
                        bootstrap_mean([np.mean([p[i] == 1 for i in in_band]) for p in pool], n_boot, seed)
                    )
            # bridge above its distractor in the vocabulary word rank, share of band layers per item
            res["bridge_above_distractor_band"] = _ci(
                bootstrap_mean(
                    [np.mean([r["bridge_word"][i] < r["distractor_word"][i] for i in in_band]) for r in rr],
                    n_boot,
                    seed,
                )
            )
            # order: does the bridge peak before the answer enters the word top-k?
            lags = []
            for r in rr:
                if r["answer_word"] is None:
                    continue
                emerge = first_layer_within(r["answer_word"], layers, hit_k)
                if emerge is not None:
                    lags.append(emerge - peak_layer(r["bridge_word"], layers))
            if lags:
                res["order"] = {
                    "n": len(lags),
                    "bridge_peaks_first": _ci(bootstrap_mean([lag > 0 for lag in lags], n_boot, seed)),
                    "median_lag_layers": float(np.median(lags)),
                }
            out[subset][reader] = res
    return out


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}
