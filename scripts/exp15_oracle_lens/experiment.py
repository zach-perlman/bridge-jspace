"""exp15_oracle_lens: does the oracle lens name the bridge where the J-lens and J++ both miss it?

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
import re
import statistics
from collections.abc import Iterable, Sequence
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
READER_BY_EXP = {"exp15_oracle_lens": "oracle lens", "exp16_nla": "NLA"}  # the verbalizer whose readings a run holds
WORDS = {"bridge": "intermediate", "distractor": "swap_to", "answer": "answer", "swap_answer": "swap_answer"}


class OracleLens(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.model import load_model
        from bridge_jspace.oracle import LoraHooks, Oracle, load_adapter, sanity_gate

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
        all_items = load_labelled_items(REPO_ROOT / p["labels_file"], p["labels_sha256"])
        entity_pool, _ = entity_and_answer_pools(tokenizer, all_items)
        items = [it for it in all_items if it["status"] == "eligible"][: p.get("limit")]

        # Phase 1, adapter off (hooks only run inside `hooks.on()`): clean and swapped activations.
        item_rows, vectors = capture(model, items, p)

        # Phase 2, adapter on: read every vector.
        read_layers = p["read_layers"]
        texts: list[str] = [""] * len(vectors)
        firsts: list[torch.Tensor | None] = [None] * len(vectors)
        pool = torch.tensor(entity_pool, device="cuda")
        for batch in progress(batches(vectors, read_layers, p["batch_size"]), "read"):
            layer = vectors[batch[0]][3]
            stack = torch.stack([vectors[i][4] for i in batch])
            for i, text in zip(batch, oracle.read(stack, layer, p["max_new_tokens"]), strict=True):
                texts[i] = text
            pool_logits = oracle.first_bullet_logits(stack, layer)[:, pool].cpu()
            for i, row in zip(batch, pool_logits, strict=True):
                firsts[i] = row

        reads = build_reads(vectors, texts, firsts, items, entity_pool, model.concept_token, item_rows, p)
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


# ---- capture and assembly (shared with exp16) -----------------------------------------------------

Vector = tuple[str, str, str, int, torch.Tensor]  # (question or "mean", condition, position, layer, [d] fp32 cpu)


def capture(model: Any, items: list[dict], p: dict[str, Any]) -> tuple[list[dict], list[Vector]]:
    """The residual at the read positions (last word, -1, the cue phrase's last edited token) and `p["read_layers"]`,
    clean and after exp14's swap (`p["swap"]`: lens, positions, band), for every item; then the mean clean vector per
    position and layer. `model` is part B's Model with no adapter active. Returns (item rows, vectors)."""
    from bridge_jspace.clamp import SwapClamp, near_parallel
    from bridge_jspace.lens import JLens
    from scripts.exp02_swaps import CUE_SPANS, band_layers, regime_positions, span_positions

    tokenizer = model.tokenizer
    read_layers, swap = p["read_layers"], p["swap"]
    edit_layers = band_layers(swap["band"])
    cues = json.loads(CUE_SPANS.read_text())["cues"]
    exp12 = REPO_ROOT / p["exp12_run"]
    exp12_meta = {m["name"]: m for m in map(json.loads, (exp12 / "items.jsonl").read_text().splitlines())}
    exp12_layers = json.loads((exp12 / "layers.json").read_text())
    assert all(exp12_layers[lens] == list(range(63)) for lens in ("jlens", "jpp")), "exp12's grid rows are not 0..62"
    exp14 = {
        o["name"]: o
        for o in map(json.loads, (REPO_ROOT / p["exp14_run"] / "outcomes.jsonl").read_text().splitlines())
        if (o["lens"], o["positions"], o["band"], o["kind"], o["null"])
        == (swap["lens"], swap["positions"], swap["band"], "bridge", False)
    }

    lens = JLens(model, swap["lens"])
    item_rows: list[dict] = []
    vectors: list[Vector] = []
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
        assert len(exp12_meta[it["name"]]["tokens"]) == seq, f"{it['name']}: exp12 tokenized the prompt differently"
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
    del lens
    torch.cuda.empty_cache()
    for pos in POSITIONS:
        for layer in read_layers:
            clean = [v for _, c, ps, ly, v in vectors if (c, ps, ly) == ("clean", pos, layer)]
            vectors.append(("mean", "mean", pos, layer, torch.stack(clean).mean(0)))
    return item_rows, vectors


def batches(vectors: list[Vector], layers: list[int], size: int) -> list[list[int]]:
    """Indices of `vectors` in batches of `size`, one layer per batch (a reader's prompt can depend on the layer)."""
    return [
        [i for i, v in enumerate(vectors) if v[3] == layer][s : s + size]
        for layer in layers
        for s in range(0, sum(v[3] == layer for v in vectors), size)
    ]


def build_reads(
    vectors: list[Vector],
    texts: list[str],
    firsts: list[torch.Tensor | None],
    items: list[dict],
    entity_pool: list[int],
    concept_token: Any,
    item_rows: list[dict],
    p: dict[str, Any],
) -> list[dict]:
    """One row per reading: the text, which words it names, the first-bullet ranks (None for readers without
    bullets) and exp12's lens ranks there; the mean vectors' readings are scored for every question."""
    from scripts.exp12_position_map.experiment import load_grids

    exp12 = REPO_ROOT / p["exp12_run"]
    exp12_meta = {m["name"]: m for m in map(json.loads, (exp12 / "items.jsonl").read_text().splitlines())}
    grids = {lens: load_grids(exp12 / f"grids_{lens}.npz") for lens in ("jlens", "jpp")}
    lens_ranks = lens_lookup(grids, exp12_meta, item_rows, p["read_layers"])
    by_name = {it["name"]: it for it in items}
    reads = []
    for (name, condition, pos, layer, _), text, first in zip(vectors, texts, firsts, strict=True):
        for it in items if name == "mean" else [by_name[name]]:
            reads.append(
                {"name": it["name"], "condition": condition, "position": pos, "layer": layer, "text": text,
                 **score_text(text, it, items),
                 **first_bullet_ranks(first, entity_pool, concept_token(it[WORDS["bridge"]]),
                                      concept_token(it[WORDS["distractor"]])),
                 **lens_ranks[(it["name"], pos, layer)]}
            )  # fmt: skip
    return reads


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
        "monitoring": {
            "bridge": monitoring(clean, "lens_class", "named_bridge", "named_distractor"),
            "answer": monitoring(clean, "answer_lens_class", "named_answer", "named_swap_answer")
            if clean and "answer_lens_class" in clean[0]
            else {},
        },
        **(answer_sections(clean, n_boot, seed) if clean and "answer_lens_class" in clean[0] else {}),
    }


MENTION_TYPES = ("concept", "answer", "retold")
_ANSWER_CUE = re.compile(r"answer\W{0,3}(?:is|:|=|would be|was)?\W{0,6}$", flags=re.IGNORECASE)
_LATIN = re.compile(r"[A-Za-z]")


def mention_type(text: str, word: str) -> str | None:
    """How the oracle's text names `word` (None if it does not): "concept" if a bullet is the word itself (nothing in
    Latin letters before it on its line, so "- Brazil", "- 巴西 (Brazil)", "- **Brazil**"); else "answer" if it follows
    an answer cue ("The answer is Brazil", "(Answer: Brazil)"); else "retold" (inside a sentence, typically the
    question re-told). Fixed before looking at the counts; a human checks a fixed-seed sample."""
    pattern = re.compile(rf"(?<![^\W_]){re.escape(word)}(?:e?s)?(?![^\W_])", flags=re.IGNORECASE)
    kinds = set()
    for line in text.split("\n"):
        body = line.strip().removeprefix("-").strip()
        for m in pattern.finditer(body):
            before = body[: m.start()]
            if not _LATIN.search(before):
                kinds.add("concept")
            elif _ANSWER_CUE.search(before):
                kinds.add("answer")
            else:
                kinds.add("retold")
    return next((k for k in MENTION_TYPES if k in kinds), None)


_QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')


def quote_type(text: str, word: str) -> str | None:
    """Whether the reader names `word` inside a quotation ("..." or “...”, within one line): "quoted", the reader
    re-telling the prompt with the word already in it (the real prompt never contains the bridge); else "commentary",
    its own remark; None if it does not name it. Fixed before counting; a human checks a fixed-seed sample."""
    pattern = re.compile(rf"(?<![^\W_]){re.escape(word)}(?:e?s)?(?![^\W_])", flags=re.IGNORECASE)
    spans = [m.span() for m in _QUOTED.finditer(text)]
    hits = [m.start() for m in pattern.finditer(text)]
    if not hits:
        return None
    return "quoted" if any(a < h < b for h in hits for a, b in spans) else "commentary"


def quote_summary(reads: list[dict], item_rows: list[dict], items: dict[str, dict]) -> dict[str, Any]:
    """Quoted vs commentary namings of the bridge (where both lenses have it 1st, where neither does) and of the swap
    target after the swap (answer changed; last word and -1)."""
    clean = [r for r in reads if r["condition"] == "clean"]
    flipped = {r["name"] for r in item_rows if r["exp14_flip"]}
    groups = {
        "bridge, both lenses 1st": ([r for r in clean if r["lens_class"] == "both"], "intermediate"),
        "bridge, neither lens 1st": ([r for r in clean if r["lens_class"] == "neither"], "intermediate"),
        "swap target after the swap, flipped, last word and -1": (
            [r for r in reads if r["condition"] == "swapped" and r["name"] in flipped and r["position"] in ("last", "prev")],
            "swap_to"),
    }  # fmt: skip
    out = {}
    for label, (rows, field) in groups.items():
        kinds = [k for r in rows if (k := quote_type(r["text"], items[r["name"]][field])) is not None]
        out[label] = {"n_named": len(kinds), **{k: (kinds.count(k) / len(kinds) if kinds else None)
                                                 for k in ("quoted", "commentary")}}  # fmt: skip
    return out


def answer_by_position(clean: list[dict], n_boot: int, seed: int) -> dict[str, Any]:
    """The solving calibrator: per read position, how often the reader names the answer, how often either lens ranks
    the answer 1st there, and how often the reader names the answer's distractor (questions with a single-token word
    answer). Where the lenses rarely have the answer (the cue phrase), a reader naming it is most likely solving."""
    rows = [r for r in clean if r.get("answer_lens_class") is not None]
    out = {}
    for pos in POSITIONS:
        sub = [r for r in rows if r["position"] == pos]
        lens = [{**r, "_lens": r["answer_lens_class"] in ("both", "one")} for r in sub]
        out[pos] = {
            "n_readings": len(sub),
            "reader_names_answer": _clustered_mean(sub, "named_answer", n_boot, seed),
            "a_lens_ranks_answer_1st": _clustered_mean(lens, "_lens", n_boot, seed),
            "reader_names_answer_distractor": _clustered_mean(sub, "named_swap_answer", n_boot, seed),
        }
    return out


def _clustered_mean(rows: list[dict], field: str, n_boot: int, seed: int) -> list[float] | None:
    """Mean of `field` over questions (each question's mean over its readings) with a bootstrap CI over questions."""
    from bridge_jspace.stats import bootstrap_mean

    q = _per_question(rows, field)
    return list(bootstrap_mean(list(q.values()), n_boot, seed)) if q else None


def quote_sample(reads: list[dict], items: dict[str, dict], k: int, seed: int) -> list[dict]:
    """k lens-blind readings that name the bridge, by a fixed seed, with their quote type, for a human check."""
    rows = [r for r in reads if r["condition"] == "clean" and r["lens_class"] == "neither" and r["named_bridge"]]
    rng = np.random.default_rng(seed)
    picked = sorted(rng.choice(len(rows), size=min(k, len(rows)), replace=False).tolist())
    return [{"name": rows[i]["name"], "position": rows[i]["position"], "layer": rows[i]["layer"],
             "bridge": items[rows[i]["name"]]["intermediate"],
             "type": quote_type(rows[i]["text"], items[rows[i]["name"]]["intermediate"]), "text": rows[i]["text"],
             "type_by_human": None} for i in picked]  # fmt: skip


def mention_types(rows: list[dict], items: dict[str, dict], field: str) -> dict[str, Any]:
    """For the readings in `rows` that name the item's `field` word: the share of each mention type, counted per
    reading (a reading with a concept bullet counts as concept even if it also answers)."""
    kinds = [mention_type(r["text"], items[r["name"]][field]) for r in rows]
    named = [k for k in kinds if k is not None]
    return {"n_readings": len(rows), "n_named": len(named),
            **{k: (sum(x == k for x in named) / len(named) if named else None) for k in MENTION_TYPES}}  # fmt: skip


def monitoring(clean: list[dict], class_field: str, word: str, distractor: str) -> dict[str, Any]:
    """The oracle as a second monitor next to the lenses, for one word. Per reading: the lenses "see" it if either
    ranks it 1st, the oracle if it names it; the four combinations' shares, by layer too. Per question (over all its
    readings): seen anywhere by the lenses, by the oracle, by either, by the oracle only. False alarms: the share of
    readings naming the distractor, overall and where the lenses miss the word."""
    rows = [r for r in clean if r.get(class_field) is not None]
    if not rows:
        return {}

    def split(sub: list[dict]) -> dict[str, float]:
        n = len(sub)
        lens = [r[class_field] in ("both", "one") for r in sub]
        oracle = [bool(r[word]) for r in sub]
        return {"n": n,
                "both": sum(a and b for a, b in zip(lens, oracle, strict=True)) / n,
                "lens_only": sum(a and not b for a, b in zip(lens, oracle, strict=True)) / n,
                "oracle_only": sum(b and not a for a, b in zip(lens, oracle, strict=True)) / n,
                "neither": sum(not a and not b for a, b in zip(lens, oracle, strict=True)) / n}  # fmt: skip

    per_q: dict[str, list[tuple[bool, bool]]] = {}
    for r in rows:
        per_q.setdefault(r["name"], []).append((r[class_field] in ("both", "one"), bool(r[word])))
    lens_q = {n for n, v in per_q.items() if any(a for a, _ in v)}
    oracle_q = {n for n, v in per_q.items() if any(b for _, b in v)}
    blind = [r for r in rows if r[class_field] == "neither"]
    return {
        "readings": split(rows),
        "readings_by_layer": {
            str(layer): split([r for r in rows if r["layer"] == layer]) for layer in sorted({r["layer"] for r in rows})
        },
        "questions": {
            "n": len(per_q),
            "lenses": len(lens_q),
            "oracle": len(oracle_q),
            "either": len(lens_q | oracle_q),
            "oracle_only": len(oracle_q - lens_q),
            "lenses_only": len(lens_q - oracle_q),
        },
        "false_alarm": {
            "distractor_named": sum(bool(r[distractor]) for r in rows) / len(rows),
            "distractor_named_where_lenses_miss": sum(bool(r[distractor]) for r in blind) / len(blind)
            if blind
            else None,
        },
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
    """A finished run's readings re-scored with the current `score_text`, with exp12's lens ranks of the answer and of
    both distractors joined; numeric answers ('4', '8') get no answer class, since the oracle's numbered bullets ("2. ...")
    would count as naming them. Returns (reads, item_rows, params, items by name)."""
    from scripts.exp12_position_map.experiment import load_grids

    run_dir = Path(run_dir)
    manifest = json.loads((run_dir / "manifest.json").read_text())
    params = {**manifest["config"]["params"], "reader": READER_BY_EXP.get(manifest["exp_id"], "oracle lens")}

    def load(path: Path) -> list[dict]:
        return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

    reads, item_rows = load(run_dir / "reads.jsonl"), load(run_dir / "items.jsonl")
    exp12 = REPO_ROOT / params["exp12_run"]
    exp12_meta = {m["name"]: m for m in load(exp12 / "items.jsonl")}
    grids = {lens: load_grids(exp12 / f"grids_{lens}.npz") for lens in ("jlens", "jpp")}
    answer = lens_lookup(grids, exp12_meta, item_rows, params["read_layers"], role="answer", prefix="answer_")
    distractor = lens_lookup(
        grids, exp12_meta, item_rows, params["read_layers"], role="distractor", prefix="distractor_"
    )
    swap_answer = lens_lookup(
        grids, exp12_meta, item_rows, params["read_layers"], role="swap_answer", prefix="swap_answer_"
    )
    items = {it["name"]: it for it in load_labelled_items(REPO_ROOT / params["labels_file"], params["labels_sha256"])}
    scored_on = [items[r["name"]] for r in item_rows]
    numeric = {n for n, it in items.items() if any(ch.isdigit() for ch in it["answer"] + it["swap_answer"])}
    no_answer = {f"{p}{k}": None for p in ("answer_", "swap_answer_") for k in ("jlens_rank", "jpp_rank", "lens_class")}
    reads = [
        {**r, **score_text(r["text"], items[r["name"]], scored_on),
         **distractor[(r["name"], r["position"], r["layer"])],
         **(no_answer if r["name"] in numeric else {**answer[(r["name"], r["position"], r["layer"])],
                                                     **swap_answer[(r["name"], r["position"], r["layer"])]})}
        for r in reads
    ]  # fmt: skip
    return reads, item_rows, params, items


def analyze(run_dir: str | Path) -> Path:
    """Re-summarize a finished run into `<run_dir>/analysis-<timestamp>/`: summary.json, examples.json (lens-blind
    readings, by a fixed seed) and the figures (plot.py), from `load_scored`."""
    from datetime import datetime

    from .plot import plot_run

    run_dir = Path(run_dir)
    reads, item_rows, params, items = load_scored(run_dir)
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    clean = [r for r in reads if r["condition"] == "clean"]
    summary = {
        "source_run": str(run_dir),
        **summarize(reads, item_rows, params),
        "mention_types": mention_summary(reads, item_rows, items),
        "quote_types": quote_summary(reads, item_rows, items),
        "answer_by_position": answer_by_position(clean, params["n_boot"], params["boot_seed"]),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    (out / "quote_sample.json").write_text(json.dumps(quote_sample(reads, items, 30, params["boot_seed"]), indent=2))
    (out / "examples.json").write_text(json.dumps(pick_examples(reads, 12, params["boot_seed"]), indent=2))
    plot_run(out, reads, item_rows, params)
    return out


def mention_summary(reads: list[dict], item_rows: list[dict], items: dict[str, dict]) -> dict[str, Any]:
    """How the oracle names the bridge: where both lenses have it first, where neither does, and the swap target after
    the swap on the questions whose answer it changes (last word and -1)."""
    clean = [r for r in reads if r["condition"] == "clean"]
    flipped = {r["name"] for r in item_rows if r["exp14_flip"]}
    return {
        "bridge, both lenses 1st": mention_types([r for r in clean if r["lens_class"] == "both"], items, "intermediate"),
        "bridge, neither lens 1st": mention_types([r for r in clean if r["lens_class"] == "neither"], items,
                                                  "intermediate"),
        "swap target after the swap, flipped, last word and -1": mention_types(
            [r for r in reads if r["condition"] == "swapped" and r["name"] in flipped and r["position"] in ("last", "prev")],
            items, "swap_to"),
    }  # fmt: skip


def mention_sample(reads: list[dict], items: dict[str, dict], k: int, seed: int) -> list[dict]:
    """k lens-blind readings that name the bridge, drawn by a fixed seed, with their mention type, for a human to
    check the classification."""
    rows = [r for r in reads if r["condition"] == "clean" and r["lens_class"] == "neither" and r["named_bridge"]]
    rng = np.random.default_rng(seed)
    picked = sorted(rng.choice(len(rows), size=min(k, len(rows)), replace=False).tolist())
    return [{"name": rows[i]["name"], "position": rows[i]["position"], "layer": rows[i]["layer"],
             "bridge": items[rows[i]["name"]]["intermediate"],
             "type": mention_type(rows[i]["text"], items[rows[i]["name"]]["intermediate"]), "text": rows[i]["text"],
             "type_by_human": None} for i in picked]  # fmt: skip


def load_runs(run_dirs: Sequence[str | Path]) -> tuple[list[dict], list[dict], dict[str, Any], dict[str, dict]]:
    """`load_scored` for runs on the same questions at different layers (e.g. 28/36/44 and 24/32/40/48), pooled;
    params are the first run's with every run's layers."""
    loaded = [load_scored(d) for d in run_dirs]
    names = [sorted(r["name"] for r in item_rows) for _, item_rows, _, _ in loaded]
    assert all(n == names[0] for n in names), "the runs read different questions"
    layer_sets = [set(p["read_layers"]) for _, _, p, _ in loaded]
    assert sum(map(len, layer_sets)) == len(set().union(*layer_sets)), "two runs read the same layer"
    reads = [r for run_reads, _, _, _ in loaded for r in run_reads]
    params = {**loaded[0][2], "read_layers": sorted(set().union(*layer_sets))}
    return reads, loaded[0][1], params, loaded[0][3]


def analyze_combined(run_dirs: Sequence[str | Path]) -> Path:
    """Several runs pooled by `load_runs` into `<last run>/analysis-<timestamp>-combined/`: summary.json over all
    their layers and the figures."""
    from datetime import datetime

    from .plot import plot_combined

    reads, item_rows, params, items = load_runs(run_dirs)
    out = Path(run_dirs[-1]) / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-combined"
    out.mkdir()
    summary = {
        "source_runs": [str(d) for d in run_dirs],
        **summarize(reads, item_rows, params),
        "mention_types": mention_summary(reads, item_rows, items),
        "quote_types": quote_summary(reads, item_rows, items),
        "answer_by_position": answer_by_position(
            [r for r in reads if r["condition"] == "clean"], params["n_boot"], params["boot_seed"]
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    (out / "mention_sample.json").write_text(
        json.dumps(mention_sample(reads, items, 30, params["boot_seed"]), indent=2)
    )
    plot_combined(out, reads, item_rows, params)
    return out


if __name__ == "__main__":
    # uv run python -m scripts.exp15_oracle_lens.experiment analyze <run_dir> [<run_dir> ...]   (several: pooled)
    import sys

    if sys.argv[1:2] != ["analyze"] or len(sys.argv) < 3:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[2]) if len(sys.argv) == 3 else analyze_combined(sys.argv[2:]))
