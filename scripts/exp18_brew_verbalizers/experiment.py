"""exp18_brew_verbalizers: do the oracle lens and the NLA read brew's intermediate from the state or from the text?

exp15 and exp16 found two verbalizers naming the bridge where the J-lens and J++ miss it; exp17 (designed) asks whether
they read the model's state or solve the question from text they reconstruct. Brew separates the two cleanly: in B
the prompt makes S -> I -> A; exp04 found the intermediate carried at four positions after the start line at layers
36-50, and copying the counterfactual C's state there (C: S -> X) makes the model answer f(X) though the text still
says I. A reader that names X there reads the state; one that names I works it out from the text.

Phases (one GPU): Qwen3.6-27B, no adapter, records the read vectors for B clean, C clean, B with C's state patched in
and B with O's (off-path) state patched in, and whether each patch took; the oracle lens (a LoRA on the same model)
passes its gate and reads at layer 44; Qwen is unloaded; the NLA loads, passes its gate and reads at layer 42.
"""

from __future__ import annotations

import gc
import json
import random
from typing import Any

import torch

from bridge_jspace.data import sha256_of
from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import REPO_ROOT
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.utils import progress

CONDITIONS = ("clean", "cf", "patched", "off_patched")
ROLES = ("I", "X", "A", "b", "c", "null")

Vector = tuple[str, str, str, int, torch.Tensor]  # (item, condition, read position, layer, [d] fp32 cpu)


class BrewVerbalizers(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.model import load_model
        from bridge_jspace.nla import LAYER, NLA, nla_sanity_gate
        from bridge_jspace.oracle import LoraHooks, Oracle, load_adapter, sanity_gate

        p = self.params
        assert p["nla_layer"] == LAYER, f"the NLA reads layer {LAYER} only"
        model = load_model()
        item_rows, vectors = capture(model, p)
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
        texts: dict[int, str] = {}
        for layer in p["oracle_layers"]:
            index = [i for i, v in enumerate(vectors) if v[3] == layer]
            for start in progress(range(0, len(index), p["batch_size"]), f"oracle L{layer}"):
                batch = index[start : start + p["batch_size"]]
                out = oracle.read(torch.stack([vectors[i][4] for i in batch]), layer, p["max_new_tokens"]["oracle"])
                texts.update(zip(batch, out, strict=True))
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
        index = [i for i, v in enumerate(vectors) if v[3] == LAYER]
        for start in progress(range(0, len(index), p["batch_size"]), "nla"):
            batch = index[start : start + p["batch_size"]]
            out = nla.read(torch.stack([vectors[i][4] for i in batch]), p["max_new_tokens"]["nla"])
            texts.update(zip(batch, out, strict=True))

        rows_by_name = {r["name"]: r for r in item_rows}
        reads = [score(vectors[i], texts[i], rows_by_name[vectors[i][0]]) for i in sorted(texts)]
        self.save_json("sanity.json", checks)
        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("reads.jsonl", reads)
        return {"n_items": len(item_rows), "checks_passed": True, **summarize(reads, item_rows, p)}


@torch.no_grad()
def capture(model: Any, p: dict[str, Any]) -> tuple[list[dict], list[Vector]]:
    """Per eligible item: the read vectors in the four conditions, and whether C's patch made the model answer f(X)."""
    from scripts.exp03_brew_swaps import ITEM_SETS, MAX_NEW_TOKENS, answer_colour, regime_positions, spans
    from scripts.exp04_brew_patch import PatchFrom, category, prepare

    path = REPO_ROOT / p["items_file"]
    assert sha256_of(path) == p["items_sha256"], f"{path} changed"
    eligible = {
        r["name"]
        for r in map(json.loads, path.read_text().splitlines())
        if r["set"] == p["item_set"] and r["status"] == "eligible"
    }
    items = ITEM_SETS[p["item_set"]][2]()
    palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
    tokenizer = model.tokenizer
    patch_layers, read_layers = p["patch_layers"], sorted({*p["oracle_layers"], p["nla_layer"]})
    assert max(patch_layers) < min(read_layers), "the reads must be downstream of the patch"
    chosen = [(i, it) for i, it in enumerate(items) if it["name"] in eligible][: p.get("limit")]
    rows: list[dict] = []
    vectors: list[Vector] = []
    for index, item in progress(chosen, "capture"):
        prep = prepare(item, index, tokenizer)
        assert prep["status"] == "ok", f"{item['name']}: {prep['status']}"
        roles = prep["cfs"]["roles"]
        positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
        assert len(positions) == 21, f"{item['name']}: {len(positions)} positions after the start line"
        patch_at = [positions[i] for i in p["patch_positions"]]
        read_at = {name: positions[i] for name, i in p["read_positions"].items()}
        ids = {"clean": prep["ids"], **{s: prep["sources"][s]["ids"] for s in ("cf", "off")}}
        tensors = {k: torch.tensor([v], device="cuda") for k, v in ids.items()}
        h = {k: model.run(t, record=(*patch_layers, *read_layers))[1] for k, t in tensors.items()}
        states = {"clean": h["clean"], "cf": h["cf"]}
        said = {}
        for name, source in (("patched", "cf"), ("off_patched", "off")):
            edits = {layer: PatchFrom(h[source][layer], patch_at) for layer in patch_layers}
            states[name] = model.run(tensors["clean"], edits=edits, record=tuple(read_layers))[1]
            said[name] = category(
                answer_colour(model.generate(tensors["clean"], MAX_NEW_TOKENS, edits)[1], palette), roles
            )
        off_path = sorted(c for c in item["table"] if c not in roles.values())
        null = random.Random(p["off_path_seed"] + index).choice(off_path)
        rows.append(
            {
                "name": item["name"],
                "roles": roles,
                "null": null,
                "patched_answer": said["patched"],
                "took": said["patched"] == "b",
                "off_patched_answer": said["off_patched"],
                "patch_at": patch_at,
                "read_at": read_at,
            }
        )
        for condition in CONDITIONS:
            for pos, at in read_at.items():
                for layer in read_layers:
                    vectors.append((item["name"], condition, pos, layer, states[condition][layer][at].cpu()))
    return rows, vectors


def score(vector: Vector, text: str, row: dict) -> dict[str, Any]:
    from bridge_jspace.oracle import named

    name, condition, pos, layer, _ = vector
    colours = {**{r: row["roles"][r] for r in ROLES if r != "null"}, "null": row["null"]}
    reader = "nla" if layer == 42 else "oracle"
    return {
        "name": name,
        "condition": condition,
        "position": pos,
        "layer": layer,
        "reader": reader,
        "text": text,
        **{f"names_{r}": named(c, text) for r, c in colours.items()},
    }


def summarize(reads: list[dict], rows: list[dict], p: dict[str, Any]) -> dict[str, Any]:
    took = {r["name"] for r in rows if r["took"]}
    out: dict[str, Any] = {"n_took": len(took), "took_rate": wilson(len(took), len(rows)), "readers": {}}
    for reader in ("oracle", "nla"):
        mine = [r for r in reads if r["reader"] == reader]
        if not mine:
            continue

        def per_item(condition: str, role: str, names: set[str], mine=mine) -> dict[str, float]:
            hit: dict[str, bool] = {}
            for r in mine:
                if r["condition"] == condition and r["name"] in names:
                    hit[r["name"]] = hit.get(r["name"], False) or r[f"names_{role}"]
            return {n: float(v) for n, v in hit.items()}

        def diff(a: dict[str, float], b: dict[str, float]) -> tuple[float, float, float]:
            names = sorted(set(a) & set(b))
            return paired_bootstrap_diff([a[n] for n in names], [b[n] for n in names], p["n_boot"], p["boot_seed"])

        everyone = {r["name"] for r in rows}
        rates = {
            f"{c} names {role}": statistics_mean(per_item(c, role, everyone)) for c in CONDITIONS for role in ROLES
        }
        rates.update(
            {f"{c} names {role} (took)": statistics_mean(per_item(c, role, took)) for c in CONDITIONS for role in ROLES}
        )
        positive = diff(per_item("cf", "X", everyone), per_item("clean", "X", everyone))
        state = diff(per_item("patched", "X", took), per_item("patched", "I", took))
        off_moves = diff(per_item("off_patched", "X", took), per_item("clean", "X", took))
        if positive[1] <= 0:
            verdict = "not interpreted: the reader does not name C's intermediate on C (positive control)"
        elif state[0] >= 0.30 and state[1] > 0 and off_moves[1] <= 0:
            verdict = "reads the state"
        elif state[2] < 0:
            verdict = "solves from the text"
        else:
            verdict = "mixed"
        out["readers"][reader] = {
            "rates": rates,
            "positive control: C clean - B clean, names X": positive,
            "took: patched names X - names I": state,
            "took: O patch - B clean, names X": off_moves,
            "verdict": verdict,
        }
    return out


def statistics_mean(values: dict[str, float]) -> float:
    return sum(values.values()) / len(values) if values else float("nan")
