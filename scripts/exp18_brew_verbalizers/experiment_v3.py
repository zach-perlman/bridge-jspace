"""exp18_brew_verbalizers v3: do the verbalizers read the intermediate the model computes with, a token direction, or
the text?

v2 (config_v2.yaml) patched C's whole state into B at the positions the readers then read, so the vectors carried C's
own context (its rules give S -> X): a reader that re-solved that context would name X as well. v3 edits B with
directions that carry no counterfactual text, at exp07's site (every position after the start line) and dose (each
edit at the norm of the copy delta = h_C - h_B at that layer and position), at layers 36, 38 and 40 together (v2's
early regime; the code is fit at even layers 36-50):
  code    exp07's code for the intermediate, E_I[X] - E_I[I], fit on brew_fit's items (an average over other tables):
          at one layer it makes the model take X as its step on 34% of items (exp07)
  lens    J++'s v_X - v_I: X's token direction against I's; at one layer it takes the step on 1% (exp07)
  random  a seeded random direction (null)
C enters only through the edits' size. The readers read downstream (the NLA at 42, the oracle lens at 44) at the newline
after "assistant" and the last token. Re-solving B's text predicts I under every edit; reading token directions
predicts X under the lens edit as much as under the code; reading the state the model computes with predicts X under
the code edit (where it took) more than under the lens edit.

Phases (one GPU): Qwen3.6-27B, no adapter, captures the test items (bank, fresh, test; never the fit items) and their
edited answers and read vectors; the oracle lens passes its gate and reads; Qwen is unloaded; the NLA reads.
"""

from __future__ import annotations

import gc
import random
from typing import Any

import torch

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.experiment import Experiment
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.utils import progress

EDITS = ("code", "lens", "random")
CONDITIONS = ("clean", *EDITS)
ROLES = ("I", "X", "A", "b", "null")
ITEM_FILES = {  # set -> (file, sha256, loader); never the fit items, which the code is fit on
    "bank": (pins.BREW_FILE, pins.BREW_SHA256, pins.brew_items),
    "fresh": (pins.BREW_FRESH_FILE, pins.BREW_FRESH_SHA256, pins.brew_fresh_items),
    "test": (pins.BREW_TEST_FILE, pins.BREW_TEST_SHA256, pins.brew_test_items),
}

Key = tuple[str, str, str, int]  # (item, condition, read position, layer)


class BrewVerbalizersV3(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.model import load_model
        from bridge_jspace.nla import LAYER, NLA, nla_sanity_gate
        from bridge_jspace.oracle import LoraHooks, Oracle, load_adapter, sanity_gate
        from scripts.exp07_step_code import CODE_FILE, RIDGE

        p = self.params
        assert p["nla_layer"] == LAYER, f"the NLA reads layer {LAYER} only"
        code = torch.load(CODE_FILE, map_location="cpu", weights_only=True)
        assert code["items"]["sha256"] == pins.BREW_FIT_SHA256, "the code was fit on other items"
        assert code["ridge"] == RIDGE, "the code was fit with another ridge"
        assert set(p["edit_layers"]) <= set(code["layers"]), "the code is not fit at every edit layer"
        w = {layer: code["w"][layer].to("cuda") for layer in p["edit_layers"]}
        model = load_model()
        item_rows, vectors, lens_reads = capture(model, w, code["suffix_ids"], p)
        to_read = selection(item_rows, p)
        facts = torch.stack(
            [
                model.run(model.encode(f["prompt"]), record=(LAYER,))[1][LAYER][-1].cpu()
                for f in p["sanity_nla"]["facts"]
            ]
        )
        pairs, scale, _ = load_adapter()
        oracle = Oracle(model, LoraHooks(model.hf, pairs, scale))
        checks = {
            "oracle": sanity_gate(model, oracle, p["sanity_oracle"], p["max_new_tokens"]["oracle"], self.cfg.seed)
        }
        if not checks["oracle"]["passed"]:
            raise RuntimeError(f"oracle sanity gate failed: {checks['oracle']['failed']}")
        texts: dict[tuple[str, Key], str] = {}
        keys = sorted(k for k in to_read if k[3] == p["oracle_layer"])
        read_all(
            lambda v, o=oracle: o.read(v, p["oracle_layer"], p["max_new_tokens"]["oracle"]),
            keys,
            vectors,
            texts,
            "oracle",
            p["batch_size"],
        )
        del oracle, pairs, model, w
        gc.collect()
        torch.cuda.empty_cache()
        left = torch.cuda.memory_allocated() / 2**30
        assert left < 4, f"{left:.1f} GiB still allocated after unloading Qwen3.6-27B"
        nla = NLA()
        checks["nla"] = nla_sanity_gate(nla, facts, p["sanity_nla"], p["max_new_tokens"]["nla"], self.cfg.seed)
        if not checks["nla"]["passed"]:
            raise RuntimeError(f"NLA sanity gate failed: {checks['nla']['failed']}")
        keys = sorted(k for k in to_read if k[3] == LAYER)
        read_all(lambda v: nla.read(v, p["max_new_tokens"]["nla"]), keys, vectors, texts, "nla", p["batch_size"])

        rows_by_name = {r["name"]: r for r in item_rows}
        reads = [score(reader, key, text, rows_by_name[key[0]]) for (reader, key), text in texts.items()] + lens_reads
        self.save_json("sanity.json", checks)
        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("reads.jsonl", reads)
        return {
            "code": {"file": str(CODE_FILE.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(CODE_FILE)},
            **summarize(reads, item_rows, p),
        }


def read_all(read, keys: list[Key], vectors: dict[Key, torch.Tensor], texts: dict, reader: str, size: int) -> None:
    for start in progress(range(0, len(keys), size), reader):
        batch = keys[start : start + size]
        for key, text in zip(batch, read(torch.stack([vectors[k] for k in batch])), strict=True):
            texts[reader, key] = text


@torch.no_grad()
def capture(model: Any, w: dict, suffix_ids: list[int], p: dict[str, Any]):
    """Every test item: eligible as exp07 (exp04's B, C and O answers; the suffix and colours the code was fit on); its
    edited answers (did each edit make the model answer f(X)?), its read vectors in each condition, and J++'s top colour
    on them."""
    from bridge_jspace.lens import JLens
    from scripts.exp03_brew_swaps import MAX_NEW_TOKENS, answer_colour, regime_positions, spans
    from scripts.exp04_brew_parts import AddRows
    from scripts.exp04_brew_patch import SOURCES, category, prepare
    from scripts.exp07_step_code import COLOURS, code_of, resized, scaled

    read_layers = sorted({p["oracle_layer"], p["nla_layer"]})
    assert max(p["edit_layers"]) < min(read_layers), "the reads must be downstream of the edits"
    lens = JLens(model, "jpp")
    colour_tok = torch.tensor([model.concept_token(c) for c in COLOURS], device="cuda")
    unit = {layer: lens.vectors(layer, colour_tok) for layer in p["edit_layers"]}  # the lens edit (as exp07)
    readout = {layer: lens.vectors(layer, colour_tok, unit=False) for layer in read_layers}  # J++'s colour (as v2)
    del lens
    torch.cuda.empty_cache()
    tokenizer = model.tokenizer
    rows: list[dict] = []
    vectors: dict[Key, torch.Tensor] = {}
    lens_reads: list[dict] = []
    for set_name in p["item_sets"]:
        path, sha, load = ITEM_FILES[set_name]
        assert sha256_of(path) == sha, f"{path} changed"
        items = load()
        palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
        for index, item in progress(list(enumerate(items))[: p.get("limit")], f"capture {set_name}"):
            prep = prepare(item, index, tokenizer)
            row: dict[str, Any] = {"set": set_name, "name": f"{set_name}:{item['name']}", "status": prep["status"]}
            rows.append(row)
            if prep["status"] != "ok":
                continue
            cfs, roles = prep["cfs"], prep["cfs"]["roles"]
            positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
            if [prep["ids"][i] for i in positions] != suffix_ids:
                row["status"] = "suffix_differs"
                continue
            if any(roles[r] not in COLOURS for r in ("S", "I", "A", "X")):
                row["status"] = "colour_outside_fit"
                continue
            ids = torch.tensor([prep["ids"]], device="cuda")
            src = {s: torch.tensor([prep["sources"][s]["ids"]], device="cuda") for s in SOURCES}
            _, clean_h = model.run(ids, record=tuple(p["edit_layers"]))
            _, cf_h = model.run(src["cf"], record=tuple(p["edit_layers"]))
            seed = p["null_seed"] + 100_000 * list(ITEM_FILES).index(set_name) + index
            g = torch.Generator(device="cuda").manual_seed(seed)
            edits: dict[str, dict] = {e: {} for e in EDITS}
            for layer in p["edit_layers"]:
                delta = cf_h[layer][positions] - clean_h[layer][positions]  # used for its size only
                code = code_of(w[layer], roles["X"]) - code_of(w[layer], roles["I"])
                u = unit[layer][COLOURS.index(roles["X"])] - unit[layer][COLOURS.index(roles["I"])]
                noise = torch.randn(code.shape, device="cuda", generator=g)
                for kind, d in (
                    ("code", resized(code, delta)),
                    ("lens", scaled(u, delta.norm(dim=-1))),
                    ("random", scaled(noise, delta.norm(dim=-1))),
                ):
                    edits[kind][layer] = AddRows(d, positions)
            del clean_h, cf_h
            # B, C and O as written and B under each edit, in one call (C and O are token-aligned with B)
            batch = torch.cat([ids, src["cf"], src["off"], *[ids] * len(EDITS)])
            texts = model.generate_batch(batch, MAX_NEW_TOKENS, [{}, {}, {}, *[edits[e] for e in EDITS]])
            said = [answer_colour(t, palette) for t in texts[:3]]
            if said != [roles["A"], cfs["cf"]["answer"], cfs["off"]["answer"]]:
                row["status"] = "not_eligible"
                continue
            texts = texts[3:]
            off_path = sorted(c for c in item["table"] if c not in roles.values())
            row.update(
                {
                    "status": "eligible",
                    "roles": roles,
                    "null": random.Random(p["off_path_seed"] + index).choice(off_path),
                }
            )
            for e, text in zip(EDITS, texts, strict=True):
                row[f"{e}_answer"] = category(answer_colour(text, palette), roles)
                row[f"{e}_took"] = row[f"{e}_answer"] == "b"
            for cond in CONDITIONS:
                state = model.run(ids, edits={} if cond == "clean" else edits[cond], record=tuple(read_layers))[1]
                for pos, i in p["read_positions"].items():
                    for layer in read_layers:
                        v = state[layer][positions[i]]
                        vectors[row["name"], cond, pos, layer] = v.cpu()
                        top = COLOURS[int((readout[layer] @ v).argmax())]
                        lens_reads.append(
                            {
                                "reader": "jpp",
                                "name": row["name"],
                                "condition": cond,
                                "position": pos,
                                "layer": layer,
                                "top": top,
                                **{f"names_{r}": top == c for r, c in colours_of(row).items()},
                            }
                        )
    return rows, vectors, lens_reads


def colours_of(row: dict) -> dict[str, str]:
    return {**{r: row["roles"][r] for r in ROLES if r != "null"}, "null": row["null"]}


def selection(rows: list[dict], p: dict[str, Any]) -> set[Key]:
    """Every condition of the items where the code edit took, and of a seeded sample of eligible items where it did not."""
    eligible = [r for r in rows if r["status"] == "eligible"]
    took = [r["name"] for r in eligible if r["code_took"]]
    rest = [r["name"] for r in eligible if not r["code_took"]]
    sample = random.Random(p["control_seed"]).sample(rest, min(p["not_took_n"], len(rest)))
    return {
        (name, cond, pos, layer)
        for name in (*took, *sample)
        for cond in CONDITIONS
        for pos in p["read_positions"]
        for layer in (p["oracle_layer"], p["nla_layer"])
    }


def score(reader: str, key: Key, text: str, row: dict) -> dict[str, Any]:
    from bridge_jspace.oracle import named

    name, condition, pos, layer = key
    return {
        "reader": reader,
        "name": name,
        "condition": condition,
        "position": pos,
        "layer": layer,
        "text": text,
        **{f"names_{r}": named(c, text) for r, c in colours_of(row).items()},
    }


def per_item(reads: list[dict], condition: str, names: set[str]) -> dict[str, float]:
    """d = [names X] - [names I] per item, a colour counted if a reading at either read position names it."""
    hit: dict[str, list[bool]] = {}
    for r in reads:
        if r["condition"] == condition and r["name"] in names:
            old = hit.get(r["name"], [False, False])
            hit[r["name"]] = [old[0] or r["names_X"], old[1] or r["names_I"]]
    return {n: float(v[0]) - float(v[1]) for n, v in hit.items()}


def summarize(reads: list[dict], rows: list[dict], p: dict[str, Any]) -> dict[str, Any]:
    eligible = [r for r in rows if r["status"] == "eligible"]
    out: dict[str, Any] = {
        "items": {
            s: {st: sum(r["set"] == s and r["status"] == st for r in rows) for st in {r["status"] for r in rows}}
            for s in p["item_sets"]
        },
        "eligible": len(eligible),
        "took (answers f(X))": {e: wilson(sum(r[f"{e}_took"] for r in eligible), len(eligible)) for e in EDITS},
        "A lost": {e: wilson(sum(r[f"{e}_answer"] != "A" for r in eligible), len(eligible)) for e in EDITS},
        "cells": {},
    }
    took = {r["name"] for r in eligible if r["code_took"]}
    sampled = {k[0] for k in selection(rows, p)} - took

    def diff(a: dict[str, float], b: dict[str, float]) -> tuple[float, float, float]:
        names = sorted(set(a) & set(b))
        if not names:  # smoke runs
            return float("nan"), float("nan"), float("nan")
        return paired_bootstrap_diff([a[n] for n in names], [b[n] for n in names], p["n_boot"], p["boot_seed"])

    for reader, layer in (
        ("nla", p["nla_layer"]),
        ("oracle", p["oracle_layer"]),
        ("jpp", p["nla_layer"]),
        ("jpp", p["oracle_layer"]),
    ):
        mine = [r for r in reads if r["reader"] == reader and r["layer"] == layer]
        d = {c: per_item(mine, c, took) for c in CONDITIONS}
        code_moves, lens_moves = diff(d["code"], d["clean"]), diff(d["lens"], d["clean"])
        code_over_lens, random_moves = diff(d["code"], d["lens"]), diff(d["random"], d["clean"])
        if code_moves[1] > 0 and code_over_lens[1] > 0 and random_moves[1] <= 0:
            verdict = "reads the state the model computes with"
        elif lens_moves[1] > 0 and code_over_lens[1] <= 0:
            verdict = "reads token directions"
        elif code_moves[2] <= p["text_margin"]:
            verdict = "follows the text"
        else:
            verdict = "mixed"
        nt = {c: per_item(mine, c, sampled) for c in ("clean", "code")}
        out["cells"][f"{reader} L{layer}"] = {
            "n_took": len(took),
            "mean X - I (took)": {c: sum(v.values()) / len(v) if v else float("nan") for c, v in d.items()},
            "code - clean": code_moves,
            "lens - clean": lens_moves,
            "code - lens": code_over_lens,
            "random - clean": random_moves,
            "code - clean, where the code did not take (sample)": diff(nt["code"], nt["clean"]),
            "verdict": verdict if reader != "jpp" else "(reference)",
        }
    return out
