"""exp18_brew_verbalizers v2: do the oracle lens and the NLA read brew's intermediate from the state or from the text?

v1 (config.yaml, run 20261015-192500): with C's state patched into B, both readers leaned toward the patched colour X
on the 28 items where the patch took, but its rule asked the patched readings to name X 30 points more often than I,
a bar the readers miss even on C itself (they recite the table's colours), and 28 items were too few. v2:
  - the rule compares each reader with itself, as exp15's swap test compared readings before and after the swap: per
    item, d = [names X] - [names I] (either read position); the patch moves the reading from the original (B clean,
    the floor) toward the counterfactual (C clean, the ceiling) if d(patched) - d(clean) is above 0
  - more items where the patch takes: the bank, the fresh and the fit items (brew_fit.json; none is read by exp18 v1
    for its decision), and a second, stronger patch (layers 36-46) read by the oracle at 48
  - only items where the patch took are read (all four conditions), plus a fixed sample for the positive control
  - J++'s own readout of the same vectors (I or X first among the 12 colours), for comparison
  - an item's runs are batched (Model.generate_batch); the readers read in batches of `batch_size`

Phases (one GPU): Qwen3.6-27B, no adapter, captures every vector and the patched answers; the oracle lens (a LoRA on
the same model) passes its gate and reads; Qwen is unloaded; the NLA loads, passes its gate and reads at layer 42.
"""

from __future__ import annotations

import gc
import random
import re
from typing import Any

import torch

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.experiment import Experiment
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.utils import progress

CONDITIONS = ("clean", "cf", "patched", "off_patched")
ROLES = ("I", "X", "A", "b", "c", "null")
ITEM_FILES = {  # set -> (file, sha256, loader)
    "bank": (pins.BREW_FILE, pins.BREW_SHA256, pins.brew_items),
    "fresh": (pins.BREW_FRESH_FILE, pins.BREW_FRESH_SHA256, pins.brew_fresh_items),
    "fit": (pins.BREW_FIT_FILE, pins.BREW_FIT_SHA256, pins.brew_fit_items),
}

Key = tuple[str, str, str, str, int]  # (item, regime or "-", condition, read position, layer)


class BrewVerbalizersV2(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.model import load_model
        from bridge_jspace.nla import LAYER, NLA, nla_sanity_gate
        from bridge_jspace.oracle import LoraHooks, Oracle, load_adapter, sanity_gate

        p = self.params
        cells = [(c["reader"], c["regime"], c["layer"]) for c in p["cells"]]
        assert all(layer == LAYER for reader, _, layer in cells if reader == "nla"), f"the NLA reads layer {LAYER}"
        model = load_model()
        item_rows, vectors, lens_reads = capture(model, p)
        to_read = selection(item_rows, cells, p)
        facts = torch.stack(
            [
                model.run(model.encode(f["prompt"]), record=(LAYER,))[1][LAYER][-1].cpu()
                for f in p["sanity_nla"]["facts"]
            ]
        )

        # The oracle lens: a LoRA on the same model, active only inside its hooks.
        pairs, scale, _ = load_adapter()
        oracle = Oracle(model, LoraHooks(model.hf, pairs, scale))
        checks = {
            "oracle": sanity_gate(model, oracle, p["sanity_oracle"], p["max_new_tokens"]["oracle"], self.cfg.seed)
        }
        if not checks["oracle"]["passed"]:
            raise RuntimeError(f"oracle sanity gate failed: {checks['oracle']['failed']}")
        texts: dict[tuple[str, Key], str] = {}
        for reader, _, layer in cells:
            if reader == "oracle":
                keys = sorted(k for k in to_read[reader, layer])
                read_all(
                    lambda v, layer=layer, o=oracle: o.read(v, layer, p["max_new_tokens"]["oracle"]),
                    keys,
                    vectors,
                    texts,
                    reader,
                    p["batch_size"],
                    f"oracle L{layer}",
                )
        del oracle, pairs, model
        gc.collect()
        torch.cuda.empty_cache()
        left = torch.cuda.memory_allocated() / 2**30
        assert left < 4, f"{left:.1f} GiB still allocated after unloading Qwen3.6-27B"

        # The NLA: a second 27B, layer 42 only.
        nla = NLA()
        checks["nla"] = nla_sanity_gate(nla, facts, p["sanity_nla"], p["max_new_tokens"]["nla"], self.cfg.seed)
        if not checks["nla"]["passed"]:
            raise RuntimeError(f"NLA sanity gate failed: {checks['nla']['failed']}")
        keys = sorted(to_read.get(("nla", LAYER), set()))
        read_all(lambda v: nla.read(v, p["max_new_tokens"]["nla"]), keys, vectors, texts, "nla", p["batch_size"], "nla")

        rows_by_name = {r["name"]: r for r in item_rows}
        reads = [
            score(reader, key, text, rows_by_name[key[0]], p["chinese_colours"])
            for (reader, key), text in texts.items()
        ]
        reads += lens_reads
        self.save_json("sanity.json", checks)
        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("reads.jsonl", reads)
        return {"n_items": len(item_rows), "checks_passed": True, **summarize(reads, item_rows, cells, p)}


def read_all(read, keys: list[Key], vectors: dict[Key, torch.Tensor], texts: dict, reader: str, size: int, label: str):
    for start in progress(range(0, len(keys), size), label):
        batch = keys[start : start + size]
        for key, text in zip(batch, read(torch.stack([vectors[k] for k in batch])), strict=True):
            texts[reader, key] = text


@torch.no_grad()
def capture(model: Any, p: dict[str, Any]) -> tuple[list[dict], dict[Key, torch.Tensor], list[dict]]:
    """Every item's eligibility (as exp04), its read vectors in each condition and regime, whether each regime's patch
    took, and J++'s colour ranks on every vector."""
    from bridge_jspace.lens import JLens
    from scripts.exp03_brew_swaps import MAX_NEW_TOKENS, answer_colour, regime_positions, spans
    from scripts.exp04_brew_patch import PatchFrom, category, prepare
    from scripts.exp07_step_code import COLOURS

    tokenizer = model.tokenizer
    regimes = p["regimes"]
    read_layers = sorted({c["layer"] for c in p["cells"]})
    patch_layers = sorted({layer for r in regimes.values() for layer in r["patch_layers"]})
    for name, r in regimes.items():
        reads = [c["layer"] for c in p["cells"] if c["regime"] == name]
        assert max(r["patch_layers"]) < min(reads), f"{name}: the reads must be downstream of the patch"
    lens = JLens(model, "jpp")
    colour_tok = torch.tensor([model.concept_token(c) for c in COLOURS], device="cuda")
    colour_v = {layer: lens.vectors(layer, colour_tok, unit=False) for layer in read_layers}  # J++ readout rows
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
            roles = prep["cfs"]["roles"]
            ids = {"clean": prep["ids"], **{s: prep["sources"][s]["ids"] for s in ("cf", "off")}}
            stacked = torch.tensor([ids["clean"], ids["cf"], ids["off"]], device="cuda")
            said = [answer_colour(t, palette) for t in model.generate_batch(stacked, MAX_NEW_TOKENS, [{}] * 3)]
            if said != [roles["A"], prep["cfs"]["cf"]["answer"], prep["cfs"]["off"]["answer"]]:
                row["status"] = "not_eligible"
                continue
            positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
            assert len(positions) == 21, f"{item['name']}: {len(positions)} positions after the start line"
            patch_at = [positions[i] for i in p["patch_positions"]]
            read_at = {pos: positions[i] for pos, i in p["read_positions"].items()}
            h = {
                k: model.run(stacked[i : i + 1], record=(*patch_layers, *read_layers))[1]
                for i, k in enumerate(("clean", "cf", "off"))
            }
            off_path = sorted(c for c in item["table"] if c not in roles.values())
            row.update(
                {
                    "status": "eligible",
                    "roles": roles,
                    "null": random.Random(p["off_path_seed"] + index).choice(off_path),
                }
            )
            states = {("-", "clean"): h["clean"], ("-", "cf"): h["cf"]}
            for name, r in regimes.items():
                edits = {
                    s: {layer: PatchFrom(h[s][layer], patch_at) for layer in r["patch_layers"]} for s in ("cf", "off")
                }
                answers = model.generate_batch(stacked[:1], MAX_NEW_TOKENS, [edits["cf"], edits["off"]])
                row[f"{name}_answer"] = category(answer_colour(answers[0], palette), roles)
                row[f"{name}_off_answer"] = category(answer_colour(answers[1], palette), roles)
                row[f"{name}_took"] = row[f"{name}_answer"] == "b"
                for s, cond in (("cf", "patched"), ("off", "off_patched")):
                    states[name, cond] = model.run(stacked[:1], edits=edits[s], record=tuple(read_layers))[1]
            for (regime, cond), state in states.items():
                for pos, at in read_at.items():
                    for layer in read_layers:
                        v = state[layer][at]
                        vectors[row["name"], regime, cond, pos, layer] = v.cpu()
                        logits = colour_v[layer] @ v
                        top = COLOURS[int(logits.argmax())]
                        lens_reads.append(
                            {
                                "reader": "jpp",
                                "name": row["name"],
                                "regime": regime,
                                "condition": cond,
                                "position": pos,
                                "layer": layer,
                                "top": top,
                                **{f"names_{r_}": top == c for r_, c in colours_of(row).items()},
                            }
                        )
    del lens, colour_v
    torch.cuda.empty_cache()
    return rows, vectors, lens_reads


def colours_of(row: dict) -> dict[str, str]:
    return {**{r: row["roles"][r] for r in ROLES if r != "null"}, "null": row["null"]}


def selection(
    rows: list[dict], cells: list[tuple[str, str, int]], p: dict[str, Any]
) -> dict[tuple[str, int], set[Key]]:
    """What each reader reads at each layer: every condition of the items where the cell's regime took, and B and C
    clean on a fixed sample of eligible items (the positive control)."""
    eligible = [r["name"] for r in rows if r["status"] == "eligible"]
    sample = random.Random(p["control_seed"]).sample(eligible, min(p["control_n"], len(eligible)))
    out: dict[tuple[str, int], set[Key]] = {}
    for reader, regime, layer in cells:
        keys = out.setdefault((reader, layer), set())
        took = [r["name"] for r in rows if r.get(f"{regime}_took")]
        for pos in p["read_positions"]:
            for name in took:
                keys |= {
                    (name, "-", "clean", pos, layer),
                    (name, "-", "cf", pos, layer),
                    (name, regime, "patched", pos, layer),
                    (name, regime, "off_patched", pos, layer),
                }
            for name in sample:
                keys |= {(name, "-", "clean", pos, layer), (name, "-", "cf", pos, layer)}
    return out


def score(reader: str, key: Key, text: str, row: dict, chinese: dict[str, str]) -> dict[str, Any]:
    from bridge_jspace.oracle import named

    name, regime, condition, pos, layer = key
    colours = colours_of(row)
    out = {
        "reader": reader,
        "name": name,
        "regime": regime,
        "condition": condition,
        "position": pos,
        "layer": layer,
        "text": text,
        **{f"names_{r}": named(c, text) for r, c in colours.items()},
    }
    out.update({f"zh_names_{r}": named(c, text) or re.search(chinese[c], text) is not None for r, c in colours.items()})
    return out


def summarize(reads: list[dict], rows: list[dict], cells: list[tuple[str, str, int]], p: dict[str, Any]) -> dict:
    eligible = [r for r in rows if r["status"] == "eligible"]
    out: dict[str, Any] = {
        "items": {
            s: {st: sum(r["set"] == s and r["status"] == st for r in rows) for st in {r["status"] for r in rows}}
            for s in p["item_sets"]
        },
        "took": {name: wilson(sum(r[f"{name}_took"] for r in eligible), len(eligible)) for name in p["regimes"]},
        "off_patch_changed": {
            name: wilson(sum(r[f"{name}_off_answer"] != "A" for r in eligible), len(eligible)) for name in p["regimes"]
        },
        "cells": {},
    }
    sample = set(
        random.Random(p["control_seed"]).sample([r["name"] for r in eligible], min(p["control_n"], len(eligible)))
    )
    for reader, regime, layer in [*cells, *[("jpp", c[1], c[2]) for c in cells]]:
        label = f"{reader} L{layer} ({regime})"
        if label in out["cells"]:
            continue
        mine = [r for r in reads if r["reader"] == reader and r["layer"] == layer and r["regime"] in ("-", regime)]
        took = {r["name"] for r in eligible if r[f"{regime}_took"]}

        def per_item(condition: str, names: set[str], prefix: str = "names", roles=("X",), against=("I",), mine=mine):
            """Per item: [a role in `roles` named] - [a role in `against` named], either read position."""
            hit: dict[str, list[float]] = {}
            for r in mine:
                if r["condition"] == condition and r["name"] in names:
                    a = any(r[f"{prefix}_{x}"] for x in roles)
                    b = any(r[f"{prefix}_{x}"] for x in against)
                    old = hit.get(r["name"], [0.0, 0.0])
                    hit[r["name"]] = [max(old[0], a), max(old[1], b)]
            return {n: v[0] - v[1] for n, v in hit.items()}

        def diff(a: dict[str, float], b: dict[str, float]) -> tuple[float, float, float]:
            names = sorted(set(a) & set(b))
            return paired_bootstrap_diff([a[n] for n in names], [b[n] for n in names], p["n_boot"], p["boot_seed"])

        def mean(d: dict[str, float]) -> float:
            return sum(d.values()) / len(d) if d else float("nan")

        d = {c: per_item(c, took) for c in CONDITIONS}
        positive = diff(per_item("cf", sample), per_item("clean", sample))
        moved = diff(d["patched"], d["clean"])
        off = diff(d["off_patched"], d["clean"])
        ceiling = diff(d["cf"], d["clean"])
        state = {c: per_item(c, took, roles=("X", "b"), against=("I", "A")) for c in CONDITIONS}
        zh = {c: per_item(c, took, prefix="zh_names") for c in ("clean", "patched")} if reader == "oracle" else None
        if positive[1] <= 0:
            verdict = "not interpreted: the reader does not tell C from B (positive control)"
        elif moved[1] > 0 and off[1] <= 0:
            verdict = "reads the state"
        elif moved[2] < ceiling[1] / 2 and moved[1] <= 0:
            verdict = "follows the text"
        else:
            verdict = "mixed"
        out["cells"][label] = {
            "n_took": len(took),
            "n_control": len(sample),
            "mean X - I": {c: mean(v) for c, v in d.items()},
            "positive control: C - B (sample)": positive,
            "patched - clean (took)": moved,
            "C - B (took, the ceiling)": ceiling,
            "recovered": moved[0] / ceiling[0] if ceiling[0] else float("nan"),
            "off_patched - clean (took)": off,
            "state colours (X, f(X)) - text colours (I, A): patched - clean": diff(state["patched"], state["clean"]),
            **({"with Chinese names: patched - clean": diff(zh["patched"], zh["clean"])} if zh else {}),
            "verdict": verdict,
        }
    return out
