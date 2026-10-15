"""exp12_position_map: at which prompt positions (and layers) is the bridge readable, and the answer?

Items, labels, words and pools as exp11 (part B's probe-swap items; bridge vs its distractor among all entities,
answer vs its distractor among all answers). Trailing space stripped, as in part B v4.

Readout: every prompt position x every source layer x readers logit lens / J-lens / J++. Positions are aligned
across prompts by their offset from the last content token (the last token that is not whitespace, e.g. " is"):
offset 0 is that token, -1 the one before, ...; the lone " " ending 29 published prompts is offset +1.

Analysis (eligible items, primary band 32-48): per offset, the share of band layers with the word top-1 in its
pool (bootstrap CI over items). The optimal offset per reader and word is chosen on a random half of the items and
scored on the other half (and vice versa), because the best of ~15 offsets is optimistic on the data that chose
it; the same search on the distractor gives the noise ceiling. Items whose bridge is missed at the last token are
checked for earlier positions. Finally exp11's full analysis is rerun at each optimal offset.

Grids are saved per reader (grids_<reader>.npz): pool ranks as uint8, word ranks as uint16 clipped at 65535.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.items import (
    ROLES,
    entity_and_answer_pools,
    load_labelled_items,
    pool_ids,
    role_ranks,
    word_ids,
)
from bridge_jspace.readout import Reader, formatting_mask, readout_logits, residuals
from bridge_jspace.stats import bootstrap_mean
from bridge_jspace.utils import progress
from scripts.exp11_bridge_vs_answer_by_layer.experiment import aggregate as exp11_aggregate
from scripts.exp11_bridge_vs_answer_by_layer.experiment import crossing

from .plot import plot_run

FIELDS = tuple(f"{r}_{k}" for r in ROLES for k in ("pool", "word"))
WORD_CLIP = 65535

Grids = dict[str, dict[str, np.ndarray]]  # item name -> field -> [layers, positions]


class PositionMap(Experiment):
    def run(self) -> dict[str, Any]:
        p = self.params
        lm, tok = self.model.lm, self.model.tokenizer
        readers: dict[str, Reader] = {"logit": None, **self.lenses}
        layers = {n: list(range(lm.n_layers - 1)) if r is None else r.source_layers for n, r in readers.items()}
        sanity = self.sanity_gate()

        items = load_labelled_items(Path(p["labels_file"]), p["labels_sha256"])[: p.get("limit")]
        entity_pool, answer_pool = entity_and_answer_pools(tok, items)
        unembed = getattr(lm, "_lm_head")  # noqa: B009 - vocab size of the head, not the tokenizer's
        mask = formatting_mask(tok, unembed.weight.shape[0]).to(self.model.device)
        record_at = sorted(set().union(*layers.values()))

        grids: dict[str, Grids] = {r: {} for r in readers}
        meta = []
        for it in progress(items, "items"):
            prompt = it["prompt"].rstrip() if p["strip_trailing_space"] else it["prompt"]
            ids = lm.encode(prompt)
            tokens = [tok.decode([t]) for t in ids[0].tolist()]
            last = last_content_index(tokens)
            meta.append(
                {
                    **{k: it[k] for k in ("name", "category", "status", "label", "intermediate", "swap_to", "answer")},
                    "tokens": tokens,
                    "offsets": [i - last for i in range(len(tokens))],
                }
            )
            resid = residuals(lm, ids, record_at)
            words, targets = word_ids(tok, it), pool_ids(tok, it)
            for rname, reader in readers.items():
                per_layer = [
                    role_ranks(
                        readout_logits(lm, reader, resid[layer], layer), words, targets, entity_pool, answer_pool, mask
                    )
                    for layer in layers[rname]
                ]
                grids[rname][it["name"]] = {
                    f: _pack(f, torch.stack([d[f] for d in per_layer]).numpy())
                    for f in FIELDS
                    if per_layer[0][f] is not None
                }
        self.save_jsonl("items.jsonl", meta)
        for rname, g in grids.items():
            save_grids(self.path(f"grids_{rname}.npz"), g)
        self.save_json("layers.json", layers)

        summary = {
            "model": self.cfg.model.name,
            "sanity": sanity,
            "labels_sha256": p["labels_sha256"],
            "strip_trailing_space": p["strip_trailing_space"],
            "pool_sizes": {"entities": len(entity_pool), "answers": len(answer_pool)},
            **analyze_grids(grids, meta, layers, p, self.cfg.seed),
        }
        chance = {"entities": 1 / len(entity_pool), "answers": 1 / len(answer_pool)}
        plot_run(self.run_dir, self.run_dir / f"figures-{_stamp()}", summary, chance)
        return summary


# ---- storage --------------------------------------------------------------------------------


def _pack(field: str, a: np.ndarray) -> np.ndarray:
    return a.astype(np.uint8) if field.endswith("_pool") else np.minimum(a, WORD_CLIP).astype(np.uint16)


def save_grids(path: Path, grids: Grids) -> None:
    arrays: dict[str, Any] = {f"{name}|{f}": a for name, g in grids.items() for f, a in g.items()}
    np.savez_compressed(path, **arrays)


def load_grids(path: Path) -> Grids:
    out: Grids = {}
    with np.load(path) as z:
        for key in z.files:
            name, f = key.split("|")
            out.setdefault(name, {})[f] = z[key]
    return out


# ---- analysis (pure; unit-tested) -------------------------------------------------------------


def last_content_index(tokens: list[str]) -> int:
    """Index of the last token that is not pure whitespace (the published prompts may end in a lone " ")."""
    return max(i for i, t in enumerate(tokens) if t.strip())


def band_score(grid: np.ndarray, offsets: list[int], offset: int, band_rows: list[int]) -> float | None:
    """Share of band layers where the word is top-1 in its pool at `offset`, or None if the prompt lacks it."""
    if offset not in offsets:
        return None
    col = offsets.index(offset)
    return float(np.mean(grid[band_rows, col] == 1))


def scores_by_offset(
    grids: Grids, meta: list[dict[str, Any]], names: list[str], field: str, offsets: list[int], band_rows: list[int]
) -> dict[int, list[float]]:
    by_name = {m["name"]: m for m in meta}
    out: dict[int, list[float]] = {}
    for off in offsets:
        vals = [
            band_score(grids[n][field], by_name[n]["offsets"], off, band_rows)
            for n in names
            if field in grids.get(n, {})
        ]
        out[off] = [v for v in vals if v is not None]
    return out


def best_offset(scores: dict[int, list[float]], min_items: int) -> int | None:
    ok = {o: np.mean(v) for o, v in scores.items() if len(v) >= min_items}
    return max(ok, key=lambda o: (ok[o], o)) if ok else None  # ties -> the later offset


def analyze_grids(
    grids: dict[str, Grids], meta: list[dict[str, Any]], layers: dict[str, list[int]], p: dict[str, Any], seed: int
) -> dict[str, Any]:
    n_boot, (lo, hi) = p["n_boot"], next(iter(p["bands"].values()))  # the first band is primary
    eligible = [m["name"] for m in meta if m["status"] == "eligible"]
    rng = np.random.default_rng(seed)
    half = set(rng.permutation(eligible)[: len(eligible) // 2].tolist())
    splits = {"A": [n for n in eligible if n in half], "B": [n for n in eligible if n not in half]}
    min_items = int(np.ceil(p["min_item_share"] * len(eligible)))
    by_name = {m["name"]: m for m in meta}
    all_offsets = sorted({o for n in eligible for o in by_name[n]["offsets"]})
    offsets = [o for o in all_offsets if sum(o in by_name[n]["offsets"] for n in eligible) >= min_items]

    out: dict[str, Any] = {
        "band": [lo, hi],
        "offsets": offsets,
        "n_per_offset": {o: sum(o in by_name[n]["offsets"] for n in eligible) for o in offsets},
        "tokens_per_offset": {o: _common_tokens(meta, eligible, o) for o in offsets},
        "splits": {k: len(v) for k, v in splits.items()},
        "readers": {},
    }
    for reader, g in grids.items():
        band_rows = [i for i, layer in enumerate(layers[reader]) if lo <= layer <= hi]
        res: dict[str, Any] = {"by_offset": {}, "optimal": {}}
        for role in ROLES:
            field = f"{role}_pool"
            sc = scores_by_offset(g, meta, eligible, field, offsets, band_rows)
            res["by_offset"][role] = {
                o: _ci(bootstrap_mean(v, n_boot, seed)) | {"n": len(v)} for o, v in sc.items() if v
            }
            best = best_offset(sc, min_items)
            if best is None:
                continue
            heldout = {}
            for pick, score in (("A", "B"), ("B", "A")):
                o = best_offset(scores_by_offset(g, meta, splits[pick], field, offsets, band_rows), min_items // 2)
                if o is None:
                    continue
                v = scores_by_offset(g, meta, splits[score], field, [o], band_rows)[o]
                heldout[f"chosen_on_{pick}"] = {"offset": o} | _ci(bootstrap_mean(v, n_boot, seed)) | {"n": len(v)}
            res["optimal"][role] = {
                "offset": best,
                "tokens": out["tokens_per_offset"][best],
                **res["by_offset"][role][best],
                "heldout": heldout,
                "at_offset_0": res["by_offset"][role].get(0),
            }
        res["missed_at_last_token"] = _missed(g, meta, eligible, band_rows, n_boot, seed)
        # exp11's analysis, rerun with each item read at the optimal offset for the bridge and for the answer
        res["at_optimal"] = {}
        for role in ("bridge", "answer"):
            if role not in res["optimal"]:
                continue
            off = res["optimal"][role]["offset"]
            rows, sub_meta = _rows_at_offset(g, meta, reader, layers[reader], off)
            res["at_optimal"][role] = {"offset": off} | exp11_aggregate(
                rows, sub_meta, [reader], p["bands"], p["emerge_run"], n_boot, seed
            )
        res["two_step"] = _two_step(g, meta, eligible, layers[reader], res["optimal"], n_boot, seed)
        res["balanced_panel"] = _balanced_panel(g, meta, eligible, offsets, band_rows, p["panel_min_share"])
        res["by_last_word"] = _by_last_word(g, meta, eligible, band_rows, n_boot, seed)
        out["readers"][reader] = res
    return out


def _two_step(grids: Grids, meta, eligible: list[str], layers: list[int], optimal: dict, n_boot: int, seed: int):
    """Depth at which the bridge (read at its best offset) and the answer (read at its best offset) become top-1 in
    half (or 30%) of the items, and the answer - bridge lag with a bootstrap CI over items."""
    if "bridge" not in optimal or "answer" not in optimal:
        return None
    ob, oa = optimal["bridge"]["offset"], optimal["answer"]["offset"]
    by_name = {m["name"]: m for m in meta}
    names = [
        n for n in eligible if ob in by_name[n]["offsets"] and oa in by_name[n]["offsets"] and "answer_pool" in grids[n]
    ]
    b = np.array([grids[n]["bridge_pool"][:, by_name[n]["offsets"].index(ob)] == 1 for n in names])
    a = np.array([grids[n]["answer_pool"][:, by_name[n]["offsets"].index(oa)] == 1 for n in names])
    return {
        "bridge_offset": ob,
        "answer_offset": oa,
        "n": len(names),
        "crossing": {str(t): crossing(b, a, layers, t, n_boot, seed) for t in (0.3, 0.5)},
    }


def _balanced_panel(
    grids: Grids, meta, eligible: list[str], offsets: list[int], band_rows: list[int], min_share: float
):
    """Optimal offsets again, on the items that reach every offset reached by >= `min_share` of eligible items, so
    the comparison across offsets is between the same items (long prompts no longer dominate far offsets)."""
    by_name = {m["name"]: m for m in meta}
    covered = [o for o in offsets if sum(o in by_name[n]["offsets"] for n in eligible) >= min_share * len(eligible)]
    panel = [n for n in eligible if all(o in by_name[n]["offsets"] for o in covered)]
    out: dict[str, Any] = {"offsets": [min(covered), max(covered)] if covered else None, "n": len(panel)}
    for role in ("bridge", "answer"):
        sc = scores_by_offset(grids, meta, panel, f"{role}_pool", covered, band_rows)
        out[role] = {
            "best_offset": best_offset(sc, 1),
            "by_offset": {o: round(float(np.mean(v)), 4) for o, v in sc.items() if v},
        }
    return out


def _by_last_word(grids: Grids, meta, eligible: list[str], band_rows: list[int], n_boot: int, seed: int):
    """Offsets -3..0 split by the last content word: the most common one (" is") vs the rest. Offsets align by
    distance from the end, not by role; this shows whether the optimum depends on what that last word is."""
    from collections import Counter

    by_name = {m["name"]: m for m in meta}
    last = {n: by_name[n]["tokens"][by_name[n]["offsets"].index(0)].strip() for n in eligible}
    top = Counter(last.values()).most_common(1)[0][0]
    out: dict[str, Any] = {"most_common_last_word": top}
    for group, names in ((f"ends_in_{top}", [n for n in eligible if last[n] == top]),
                         ("ends_otherwise", [n for n in eligible if last[n] != top])):  # fmt: skip
        g: dict[str, Any] = {"n": len(names)}
        for role in ("bridge", "answer"):
            sc = scores_by_offset(grids, meta, names, f"{role}_pool", [-3, -2, -1, 0], band_rows)
            g[role] = {o: _ci(bootstrap_mean(v, n_boot, seed)) for o, v in sc.items() if v}
        out[group] = g
    return out


def _missed(grids: Grids, meta, eligible: list[str], band_rows: list[int], n_boot: int, seed: int) -> dict[str, Any]:
    """Items whose bridge is top-1 in under half the band layers at the prompt's true last token: is it on top at
    some earlier position? The same search for the distractor is the control (best of many positions)."""
    by_name = {m["name"]: m for m in meta}
    missed, rescued, ctrl, best_offsets = [], [], [], []
    for n in eligible:
        g, offs = grids[n], by_name[n]["offsets"]
        if "bridge_pool" not in g:
            continue
        top = g["bridge_pool"][band_rows] == 1  # [band layers, positions]
        if top[:, -1].mean() >= 0.5:
            continue
        missed.append(n)
        earlier = top[:, :-1].mean(0)
        rescued.append(float(earlier.max() >= 0.5) if earlier.size else 0.0)
        dtop = (g["distractor_pool"][band_rows] == 1)[:, :-1].mean(0)
        ctrl.append(float(dtop.max() >= 0.5) if dtop.size else 0.0)
        best_offsets.append(offs[int(np.argmax(earlier))] if earlier.size else None)
    return {
        "n_missed": len(missed),
        "n_eligible": len(eligible),
        "bridge_on_top_earlier": _ci(bootstrap_mean(rescued, n_boot, seed)) if rescued else None,
        "distractor_on_top_earlier": _ci(bootstrap_mean(ctrl, n_boot, seed)) if ctrl else None,
        "best_earlier_offsets": best_offsets,
    }


def _rows_at_offset(grids: Grids, meta, reader: str, layers: list[int], offset: int):
    """exp11-format rows/meta for the items that have `offset`, read at that position."""
    rows, sub = [], []
    for m in meta:
        g = grids.get(m["name"])
        if g is None or offset not in m["offsets"]:
            continue
        col = m["offsets"].index(offset)
        row: dict[str, Any] = {"name": m["name"], "reader": reader, "layers": layers}
        for f in FIELDS:
            row[f] = g[f][:, col].astype(int).tolist() if f in g else None
        rows.append(row)
        sub.append({**m, "ends_with_space": m["tokens"][-1].strip() == ""})
    return rows, sub


def _common_tokens(meta, names: list[str], offset: int, k: int = 3) -> list[list[Any]]:
    from collections import Counter

    by_name = {m["name"]: m for m in meta}
    c = Counter(
        by_name[n]["tokens"][by_name[n]["offsets"].index(offset)] for n in names if offset in by_name[n]["offsets"]
    )
    return [[t, k_] for t, k_ in c.most_common(k)]


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}


def _stamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y%m%d-%H%M%S")


def analyze(run_dir: str | Path, params: dict[str, Any]) -> Path:
    """Re-run the analysis of a finished run from its saved grids into a new `<run_dir>/analysis-<timestamp>/`."""
    run_dir = Path(run_dir)
    manifest = json.loads((run_dir / "manifest.json").read_text())
    meta = [json.loads(x) for x in (run_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    layers = json.loads((run_dir / "layers.json").read_text())
    grids = {r: load_grids(run_dir / f"grids_{r}.npz") for r in layers}
    out = run_dir / f"analysis-{_stamp()}"
    out.mkdir()
    summary = {"source_run": str(run_dir), **analyze_grids(grids, meta, layers, params, manifest["config"]["seed"])}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    pools = json.loads((run_dir / "summary.json").read_text())["pool_sizes"]
    plot_run(run_dir, out, summary, {"entities": 1 / pools["entities"], "answers": 1 / pools["answers"]})
    return out


if __name__ == "__main__":
    # uv run python -m scripts.exp12_position_map.experiment analyze <run_dir>   (params from the current config.yaml)
    import sys

    from bridge_jspace.config import load_config

    if sys.argv[1:2] != ["analyze"] or len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[2], load_config(Path(__file__).with_name("config.yaml")).params))
