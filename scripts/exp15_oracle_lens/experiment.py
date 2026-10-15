"""exp15_oracle_lens: does the oracle lens name the bridge where the J-lens and J++ both miss it? (design: Danyil)

Reader: the oracle lens (bridge_jspace.oracle: a LoRA on Qwen3.6-27B, its published read contract, greedy decoding)
on the residual at three prompt positions (the last word, -1, the last token of the cue phrase) and layers 28/36/44.

Questions: the 77 two-hop questions 27B answers correctly (part B's v4 labels, trailing space stripped). Each read is
classed by exp12's lens readings at the same question, position and layer: both lenses rank the bridge first among the
97 entities, one does, or neither.

Conditions:
- clean: the activation as the model computes it;
- swapped: after exp14's J++ bridge swap on the cue phrase at layers 24-40 (Brazil -> Mexico); exp14's run says on
  which questions that swap flips the answer;
- mean: the mean clean activation over the questions at each position and layer (what the oracle says for no
  question in particular).

Scores per read: the bridge, its distractor, the answer and the swap answer named in the bullets (whole word, case
and a plural ending ignored); the share of the other questions' bridges named (the cross-question null); and the
bridge's and distractor's ranks among the 97 entities as the first bullet (the token after "-").
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import numpy as np
import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.items import entity_and_answer_pools, load_labelled_items
from bridge_jspace.oracle import named
from bridge_jspace.pins import REPO_ROOT
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.utils import progress

POSITIONS = ("last", "prev", "cue_last")
WORDS = {"bridge": "intermediate", "distractor": "swap_to", "answer": "answer", "swap_answer": "swap_answer"}


class OracleLens(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.clamp import SwapClamp, near_parallel
        from bridge_jspace.lens import JLens
        from bridge_jspace.model import load_model
        from bridge_jspace.oracle import LoraHooks, Oracle, load_adapter, sanity_gate
        from scripts.exp02_swaps import CUE_SPANS, band_layers, regime_positions, span_positions
        from scripts.exp12_position_map.experiment import load_grids

        p = self.params
        model = load_model()  # part B's loader, as exp14 (the swap path); self.model is never built
        tokenizer = model.tokenizer
        # The oracle's gate first (fails the run before any capture): hooks switch off cleanly, the adapter is live,
        # known concepts are named and a random vector names none of them.
        pairs, scale, adapter_config = load_adapter()
        hooks = LoraHooks(model.hf, pairs, scale)
        oracle = Oracle(model, hooks)
        checks = sanity_gate(model, oracle, p["sanity"], p["max_new_tokens"], self.cfg.seed)
        self.save_json("sanity.json", checks)
        if not checks["passed"]:
            raise RuntimeError(f"oracle sanity gate failed: {checks['failed']} (see sanity.json)")
        cues = json.loads(CUE_SPANS.read_text())["cues"]
        all_items = load_labelled_items(REPO_ROOT / p["labels_file"], p["labels_sha256"])
        entity_pool, _ = entity_and_answer_pools(tokenizer, all_items)
        items = [it for it in all_items if it["status"] == "eligible"][: p.get("limit")]
        read_layers, swap = p["read_layers"], p["swap"]
        edit_layers = band_layers(swap["band"])

        exp12 = REPO_ROOT / p["exp12_run"]
        exp12_meta = {m["name"]: m for m in map(json.loads, (exp12 / "items.jsonl").read_text().splitlines())}
        grids = {lens: load_grids(exp12 / f"grids_{lens}.npz") for lens in ("jlens", "jpp")}
        exp12_layers = json.loads((exp12 / "layers.json").read_text())
        assert all(exp12_layers[lens] == list(range(63)) for lens in grids), "exp12's grid rows are not layers 0..62"
        exp14 = {
            o["name"]: o
            for o in map(json.loads, (REPO_ROOT / p["exp14_run"] / "outcomes.jsonl").read_text().splitlines())
            if (o["lens"], o["positions"], o["band"], o["kind"], o["null"])
            == (swap["lens"], swap["positions"], swap["band"], "bridge", False)
        }

        # Phase 1, adapter off (hooks only run inside `hooks.on()`): clean and swapped activations.
        lens = JLens(model, swap["lens"])
        item_rows, vectors = [], []  # vectors: (name, condition, position, layer, [d] fp32 cpu)
        for it in progress(items, "capture"):
            prompt = it["prompt"].rstrip()
            enc = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
            ids = torch.tensor([enc.input_ids], device="cuda")
            seq = ids.shape[1]
            start = prompt.index(cues[it["name"]])
            cue = span_positions(enc.offset_mapping, start, start + len(cues[it["name"]]))
            edit_positions = regime_positions(swap["positions"], seq, cue)
            cue_edited = regime_positions("cue", seq, cue)
            assert cue_edited, f"{it['name']}: no cue-phrase position"
            read_at = {"last": seq - 1, "prev": seq - 2, "cue_last": max(cue_edited)}
            meta = exp12_meta[it["name"]]
            assert len(meta["tokens"]) == seq, f"{it['name']}: exp12 tokenized the prompt differently"
            _, clean_h = model.run(ids, record=tuple(sorted(set(edit_layers) | set(read_layers))))
            tokens = [model.concept_token(it[WORDS["bridge"]]), model.concept_token(it[WORDS["distractor"]])]
            clamps = {}
            for layer in edit_layers:
                atoms = lens.vectors(layer, torch.tensor(tokens, device="cuda"))
                if not near_parallel(atoms[0], atoms[1]):
                    clamps[layer] = SwapClamp(atoms, clean_h[layer], positions=edit_positions)
            swapped_logits, swapped_h = model.run(ids, edits=clamps, record=tuple(read_layers))
            ref = exp14.get(it["name"])
            item_rows.append(
                {"name": it["name"], "category": it["category"], "seq_len": seq, "read_at": read_at,
                 "cue_positions": cue, "edit_positions": edit_positions, "layers_skipped": sorted(set(edit_layers) - set(clamps)),
                 "swap_top_word": model.top_word(swapped_logits),
                 "exp14_flip": ref["flip"] if ref else None, "exp14_top_word": ref["top_word"] if ref else None}
            )  # fmt: skip
            for pos, index in read_at.items():
                for layer in read_layers:
                    vectors.append((it["name"], "clean", pos, layer, clean_h[layer][index].cpu()))
                    vectors.append((it["name"], "swapped", pos, layer, swapped_h[layer][index].cpu()))
        del lens, clean_h, swapped_h
        torch.cuda.empty_cache()
        for pos in POSITIONS:
            for layer in read_layers:
                clean = [v for _, c, ps, ly, v in vectors if (c, ps, ly) == ("clean", pos, layer)]
                vectors.append(("mean", "mean", pos, layer, torch.stack(clean).mean(0)))

        # Phase 2, adapter on: read every vector.
        texts: list[str] = [""] * len(vectors)
        firsts: list[torch.Tensor | None] = [None] * len(vectors)
        batches = [
            [i for i, v in enumerate(vectors) if v[3] == layer][s : s + p["batch_size"]]
            for layer in read_layers
            for s in range(0, sum(v[3] == layer for v in vectors), p["batch_size"])
        ]
        pool = torch.tensor(entity_pool, device="cuda")
        for batch in progress(batches, "read"):
            layer = vectors[batch[0]][3]
            stack = torch.stack([vectors[i][4] for i in batch])
            for i, text in zip(batch, oracle.read(stack, layer, p["max_new_tokens"]), strict=True):
                texts[i] = text
            pool_logits = oracle.first_bullet_logits(stack, layer)[:, pool].cpu()
            for i, row in zip(batch, pool_logits, strict=True):
                firsts[i] = row

        by_name = {it["name"]: it for it in items}
        lens_ranks = lens_lookup(grids, exp12_meta, item_rows, read_layers)
        reads = []
        for (name, condition, pos, layer, _), text, first in zip(vectors, texts, firsts, strict=True):
            for it in items if name == "mean" else [by_name[name]]:  # the mean read is scored for every question
                reads.append(
                    {"name": it["name"], "condition": condition, "position": pos, "layer": layer, "text": text,
                     **score_text(text, it, items),
                     **first_bullet_ranks(first, entity_pool, model.concept_token(it[WORDS["bridge"]]),
                                          model.concept_token(it[WORDS["distractor"]])),
                     **lens_ranks[(it["name"], pos, layer)]}
                )  # fmt: skip
        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("reads.jsonl", reads)
        return {
            "model": "Qwen3.6-27B (part B's loader, pins.py) + oracle lens (pins.ORACLE_DIR)",
            "n_questions": len(items),
            "entity_pool": len(entity_pool),
            "adapter": {"modules": len(pairs), "scale": scale, "r": adapter_config["r"]},
            "checks": {**checks, "exp14_top_word_agree": exp14_agreement(item_rows)},
            **summarize(reads, item_rows, p),
            "decision_rule": p["decision"],
        }


# ---- pure helpers (unit-tested) ------------------------------------------------------------------


def score_text(text: str, item: dict, items: list[dict]) -> dict[str, Any]:
    """Which of the question's four words the read names, and the share of other questions' bridges it names (those
    equal to this question's bridge or distractor left out)."""
    out: dict[str, Any] = {f"named_{role}": named(item[field], text) for role, field in WORDS.items()}
    own = {item["intermediate"].lower(), item["swap_to"].lower()}
    others = sorted({it["intermediate"] for it in items if it["intermediate"].lower() not in own})
    out["named_other_bridges"] = sum(named(w, text) for w in others) / len(others) if others else 0.0
    return out


def first_bullet_ranks(pool_logits: torch.Tensor | None, pool: list[int], bridge: int, distractor: int) -> dict:
    """1-based ranks of the bridge and its distractor among the entity pool as the first bullet."""
    if pool_logits is None:
        return {"first_rank_bridge": None, "first_rank_distractor": None}
    order = torch.argsort(pool_logits, descending=True).tolist()
    rank = {pool[i]: r + 1 for r, i in enumerate(order)}
    return {"first_rank_bridge": rank.get(bridge), "first_rank_distractor": rank.get(distractor)}


def lens_class(jlens_rank: int | None, jpp_rank: int | None) -> str | None:
    """Both lenses have the word first in its pool, one does, or neither."""
    if jlens_rank is None or jpp_rank is None:
        return None
    return {2: "both", 1: "one", 0: "neither"}[(jlens_rank == 1) + (jpp_rank == 1)]


def lens_lookup(
    grids, exp12_meta: dict, item_rows: list[dict], layers: Iterable[int], role: str = "bridge", prefix: str = ""
) -> dict[tuple, dict]:
    """(question, position, layer) -> exp12's J-lens and J++ ranks of `role` in its pool there (bridge: among the 97
    entities; answer: among the 112 answers, single-token answers only) and the cell's class. Grid rows are layers
    0..62 (exp12's layers.json); columns are positions in prompt order, by offset from the last word."""
    out = {}
    for row in item_rows:
        name, last = row["name"], row["seq_len"] - 1
        offsets = exp12_meta[name]["offsets"]
        for pos, index in row["read_at"].items():
            col = offsets.index(index - last)
            for layer in layers:
                ranks = {
                    lens: int(g[f"{role}_pool"][layer, col]) if f"{role}_pool" in (g := grids[lens][name]) else None
                    for lens in ("jlens", "jpp")
                }
                out[(name, pos, layer)] = {
                    f"{prefix}jlens_rank": ranks["jlens"],
                    f"{prefix}jpp_rank": ranks["jpp"],
                    f"{prefix}lens_class": lens_class(ranks["jlens"], ranks["jpp"]),
                }
    return out


def exp14_agreement(item_rows: list[dict]) -> dict[str, int]:
    """Our swapped forward's top word vs exp14's for the same swap (same edit; exp14's came from generate)."""
    shared = [r for r in item_rows if r["exp14_top_word"] is not None]
    return {"shared": len(shared), "agree": sum(r["swap_top_word"] == r["exp14_top_word"] for r in shared)}


def _per_question(reads: list[dict], field: str) -> dict[str, float]:
    by: dict[str, list[float]] = {}
    for r in reads:
        by.setdefault(r["name"], []).append(float(r[field]))
    return {n: statistics.mean(v) for n, v in by.items()}


def compare(reads: list[dict], a: str, b: str, n_boot: int, seed: int) -> dict[str, Any] | None:
    """Field a vs field b over reads, clustered by question (each question's mean over its reads), paired bootstrap."""
    if not reads:
        return None
    qa, qb = _per_question(reads, a), _per_question(reads, b)
    names = sorted(qa)
    diff = paired_bootstrap_diff([qa[n] for n in names], [qb[n] for n in names], n_boot=n_boot, seed=seed)
    return {"n_questions": len(names), "n_reads": len(reads), a: float(np.mean([qa[n] for n in names])),
            b: float(np.mean([qb[n] for n in names])), "diff": diff}  # fmt: skip


def rate_rows(reads: list[dict], keys: tuple[str, ...]) -> list[dict]:
    """Per group: the share of reads naming the bridge / distractor / answer (Wilson), the mean share of other
    questions' bridges named, and the bridge first among the entities as the first bullet."""
    groups: dict[tuple, list[dict]] = {}
    for r in reads:
        groups.setdefault(tuple(r[k] for k in keys), []).append(r)
    out = []
    for key, rows in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        n = len(rows)
        ranked = [r for r in rows if r["first_rank_bridge"] is not None]
        out.append(
            {**dict(zip(keys, key, strict=True)), "n": n, "n_questions": len({r["name"] for r in rows}),
             **{f"named_{role}": wilson(sum(r[f"named_{role}"] for r in rows), n) for role in WORDS},
             "named_other_bridges": float(np.mean([r["named_other_bridges"] for r in rows])),
             "first_top1_bridge": wilson(sum(r["first_rank_bridge"] == 1 for r in ranked), len(ranked)),
             "first_top1_distractor": wilson(sum(r["first_rank_distractor"] == 1 for r in ranked), len(ranked))}
        )  # fmt: skip
    return out


def summarize(reads: list[dict], item_rows: list[dict], p: dict[str, Any]) -> dict[str, Any]:
    n_boot, seed = p["n_boot"], p["boot_seed"]
    clean = [r for r in reads if r["condition"] == "clean"]
    flipped = {r["name"] for r in item_rows if r["exp14_flip"]}
    kept = {r["name"] for r in item_rows if r["exp14_flip"] is False}
    after = p["after_swap"]

    def swap_cells(names: set[str]) -> dict[str, Any]:
        out: dict[str, Any] = {"n_questions": len(names)}
        for pos in after["positions"]:
            for cond in ("clean", "swapped"):
                rows = [r for r in reads if r["condition"] == cond and r["name"] in names and r["position"] == pos
                        and r["layer"] == after["layer"]]  # fmt: skip
                out[f"{pos} {cond}"] = rate_rows(rows, ("position",))[0] if rows else None
            pair = [r for r in reads if r["name"] in names and r["position"] == pos and r["layer"] == after["layer"]]
            swapped = {r["name"]: r for r in pair if r["condition"] == "swapped"}
            clean_r = {r["name"]: r for r in pair if r["condition"] == "clean"}
            both = sorted(set(swapped) & set(clean_r))
            if both:
                out[f"{pos} distractor swapped - clean"] = paired_bootstrap_diff(
                    [swapped[n]["named_distractor"] for n in both],
                    [clean_r[n]["named_distractor"] for n in both],
                    n_boot=n_boot,
                    seed=seed,
                )
        return out

    return {
        "n_reads": {c: sum(r["condition"] == c for r in reads) for c in ("clean", "swapped", "mean")},
        "lens_classes": {c: sum(r["lens_class"] == c for r in clean) for c in ("both", "one", "neither")},
        "clean_by_class": rate_rows(clean, ("lens_class",)),
        "clean_by_class_layer_position": rate_rows(clean, ("lens_class", "layer", "position")),
        "mean_vector": rate_rows([r for r in reads if r["condition"] == "mean"], ("layer", "position")),
        "bridge_vs_distractor": {
            c: compare([r for r in clean if r["lens_class"] == c], "named_bridge", "named_distractor", n_boot, seed)
            for c in ("both", "one", "neither")
        },
        "bridge_vs_other_bridges": {
            c: compare([r for r in clean if r["lens_class"] == c], "named_bridge", "named_other_bridges", n_boot, seed)
            for c in ("both", "one", "neither")
        },
        "bridge_vs_distractor_by_layer": by_layer(
            clean, "lens_class", "named_bridge", "named_distractor", n_boot, seed
        ),
        "after_swap": {"flipped": swap_cells(flipped), "not_flipped": swap_cells(kept)},
        **(answer_sections(clean, n_boot, seed) if clean and "answer_lens_class" in clean[0] else {}),
    }


def by_layer(rows: list[dict], class_field: str, a: str, b: str, n_boot: int, seed: int) -> dict[str, dict]:
    """`compare` of fields a and b per layer and lens class."""
    return {
        str(layer): {
            c: compare([r for r in rows if r[class_field] == c and r["layer"] == layer], a, b, n_boot, seed)
            for c in ("both", "one", "neither")
        }
        for layer in sorted({r["layer"] for r in rows})
    }


def answer_sections(clean: list[dict], n_boot: int, seed: int) -> dict[str, Any]:
    """The same split for the answer (questions with single-token answers): by the lenses' answer class, the oracle
    naming the answer vs the swap answer."""
    rows = [r for r in clean if r["answer_lens_class"] is not None]
    return {
        "answer_lens_classes": {c: sum(r["answer_lens_class"] == c for r in rows) for c in ("both", "one", "neither")},
        "clean_by_answer_class": rate_rows(rows, ("answer_lens_class",)),
        "clean_by_answer_class_layer_position": rate_rows(rows, ("answer_lens_class", "layer", "position")),
        "answer_vs_swap_answer": {
            c: compare(
                [r for r in rows if r["answer_lens_class"] == c], "named_answer", "named_swap_answer", n_boot, seed
            )
            for c in ("both", "one", "neither")
        },
        "answer_vs_swap_answer_by_layer": by_layer(
            rows, "answer_lens_class", "named_answer", "named_swap_answer", n_boot, seed
        ),
    }


def pick_examples(reads: list[dict], k: int, seed: int) -> dict[str, list[dict]]:
    """Up to k clean reads per group, drawn by a fixed seed: cells where neither lens has the bridge (or the answer)
    first, split by whether the oracle names it."""
    rng = np.random.default_rng(seed)
    keep = ("name", "position", "layer", "jlens_rank", "jpp_rank", "answer_jlens_rank", "answer_jpp_rank", "text")
    groups = {
        "bridge lens-blind, oracle names it": lambda r: r["lens_class"] == "neither" and r["named_bridge"],
        "bridge lens-blind, oracle does not": lambda r: r["lens_class"] == "neither" and not r["named_bridge"],
        "answer lens-blind, oracle names it": lambda r: r.get("answer_lens_class") == "neither" and r["named_answer"],
        "answer lens-blind, oracle does not": lambda r: (
            r.get("answer_lens_class") == "neither" and not r["named_answer"]
        ),
    }
    out = {}
    for label, test in groups.items():
        rows = [r for r in reads if r["condition"] == "clean" and test(r)]
        picked = sorted(rng.choice(len(rows), size=min(k, len(rows)), replace=False).tolist()) if rows else []
        out[label] = [{f: rows[i].get(f) for f in keep} for i in picked]
    return out


def load_scored(run_dir: str | Path) -> tuple[list[dict], list[dict], dict[str, Any], dict[str, dict]]:
    """A finished run's readings re-scored with the current `score_text`, with the answer's lens ranks and class
    joined from exp12; numeric answers ('4', '8') get no answer class, since the oracle's numbered bullets ("2. ...")
    would count as naming them. Returns (reads, item_rows, params, items by name)."""
    from scripts.exp12_position_map.experiment import load_grids

    run_dir = Path(run_dir)
    params = json.loads((run_dir / "manifest.json").read_text())["config"]["params"]

    def load(path: Path) -> list[dict]:
        return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

    reads, item_rows = load(run_dir / "reads.jsonl"), load(run_dir / "items.jsonl")
    exp12 = REPO_ROOT / params["exp12_run"]
    exp12_meta = {m["name"]: m for m in load(exp12 / "items.jsonl")}
    grids = {lens: load_grids(exp12 / f"grids_{lens}.npz") for lens in ("jlens", "jpp")}
    answer = lens_lookup(grids, exp12_meta, item_rows, params["read_layers"], role="answer", prefix="answer_")
    items = {it["name"]: it for it in load_labelled_items(REPO_ROOT / params["labels_file"], params["labels_sha256"])}
    scored_on = [items[r["name"]] for r in item_rows]
    numeric = {n for n, it in items.items() if any(ch.isdigit() for ch in it["answer"] + it["swap_answer"])}
    no_answer = {"answer_jlens_rank": None, "answer_jpp_rank": None, "answer_lens_class": None}
    reads = [
        {**r, **score_text(r["text"], items[r["name"]], scored_on),
         **(no_answer if r["name"] in numeric else answer[(r["name"], r["position"], r["layer"])])}
        for r in reads
    ]  # fmt: skip
    return reads, item_rows, params, items


def analyze(run_dir: str | Path) -> Path:
    """Re-summarize a finished run into `<run_dir>/analysis-<timestamp>/`: summary.json, examples.json (lens-blind
    readings, by a fixed seed) and the figures (plot.py), from `load_scored`."""
    from datetime import datetime

    from .plot import plot_run

    run_dir = Path(run_dir)
    reads, item_rows, params, _ = load_scored(run_dir)
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    summary = {"source_run": str(run_dir), **summarize(reads, item_rows, params)}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    (out / "examples.json").write_text(json.dumps(pick_examples(reads, 12, params["boot_seed"]), indent=2))
    plot_run(out, reads, item_rows, params)
    return out


if __name__ == "__main__":
    # uv run python -m scripts.exp15_oracle_lens.experiment analyze <run_dir>
    import sys

    if sys.argv[1:2] != ["analyze"] or len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[2]))
