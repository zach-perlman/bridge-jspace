"""exp04_brew_parts: which part of the window's copy carries brew's intermediate, its J-space part or the rest?

exp04's patch_map found the intermediate carried after the start line at layers 36-50 (its window): copying the
counterfactual C's activations there makes the model answer f(X) (X used as the step, B's table for the second
lookup). This run copies only a part of that difference at each window layer, with the same items and counterfactuals:

  δ = h_C - h_B at each position after the start line (one layer at a time); the parts below add up to δ in pairs.
  lens2       δ's orthogonal projection onto span{v_I, v_X} (the lens's own vectors for the two colours)
  not_lens2   δ minus that
  jspace      δ's k-atom signed OMP approximation over the lens's unit vectors of letter-bearing tokens (J-space part)
  not_jspace  δ minus that
  full        δ itself (reproduces patch_map's after_start rows at the window layers)
Lenses: J++ (primary) and the J-lens. Controls: every part again along matched-norm random directions (per position,
seeded), and the off-path counterfactual O's full copy. The answer is read as in patch_map: f(X) (b), c, X, A.

Per item, the step score of a part is the share of window layers at which its copy makes the model answer f(X).

Stages (the manifest is written before the run and is write-once):
  manifest --name N --map M     M: the patch_map run whose window (after_start) this run uses
  run N
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts.exp03_brew_swaps import (
    ITEM_SETS,
    MAX_NEW_TOKENS,
    answer_colour,
    regime_positions,
    spans,
    write_jsonl,
)
from scripts.exp04_brew_patch import EXP, RESULTS, SOURCES, category, prepare

LENSES = ("jpp", "jlens")
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")
K_ATOMS = 25
NULL_SEED = 0
N_BOOT, BOOT_SEED = 2000, 0
CHANCE_DRAWS = 20  # random directions decomposed per lens and layer: the J-space part's chance share of variance


@torch.no_grad()
def signed_omp(dictionary: torch.Tensor, x: torch.Tensor, k: int) -> torch.Tensor:
    """Batched orthogonal matching pursuit with signed coefficients: for each row of x [m, d], the least-squares fit
    on the k rows of `dictionary` [n, d] (unit rows) chosen greedily by |correlation| with the residual. Returns the
    approximations [m, d]."""
    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    for _ in range(k):
        scores = ((x - approx) @ dictionary.T).abs()  # [m, n]
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dictionary[chosen].double()  # [m, s, d]
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)  # [m, s]
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
    return approx


def lens2_part(delta: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """Orthogonal projection of delta [P, d] onto the span of the rows of v [2, d]."""
    v = v.float()
    return delta @ torch.linalg.pinv(v) @ v


class AddRows:
    """Edit for one layer: add delta [P, d] at the given positions."""

    def __init__(self, delta: torch.Tensor, positions: list[int]):
        self.delta, self.positions = delta, positions

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = h[self.positions] + self.delta.to(h.dtype)
        return out


def null_rows(delta: torch.Tensor, generator: torch.Generator) -> torch.Tensor:
    """Each row replaced by a random unit direction scaled to that row's norm (the matched-norm null)."""
    r = torch.randn(delta.shape, device=delta.device, generator=generator)
    return torch.nn.functional.normalize(r, dim=-1) * delta.norm(dim=-1, keepdim=True)


def stage_manifest(name: str, map_run: str) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    map_dir = RESULTS / map_run
    map_manifest = json.loads((map_dir / "manifest.json").read_text())
    window = json.loads((map_dir / "summary.json").read_text())["decision"]["windows"]["after_start"]
    assert window, f"{map_run} found no after_start window"
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "patch_parts",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Which part of the window's copy carries the intermediate as a step: its lens coordinates for I "
        "and X, its J-space part, or the rest?",
        "model": map_manifest["model"],
        "items": map_manifest["items"],
        "map": {"run": map_run, "summary_sha256": sha256_of(map_dir / "summary.json"), "window_after_start": window},
        "counterfactuals": "patch_map's (C: S -> X, X -> c; O: two off-path rules changed), same seeds",
        "positions": "after_start (everything after the start line)",
        "layers": window,
        "lenses": {lens: list(pins.LENS_SOURCES[lens]) for lens in LENSES},
        "parts": {
            "full": "δ = h_C - h_B",
            "lens2": "δ's orthogonal projection onto span{v_I, v_X} (unit lens vectors of the colours' concept tokens)",
            "not_lens2": "δ - lens2",
            "jspace": f"δ's {K_ATOMS}-atom signed OMP approximation over the lens's unit vectors of letter-bearing tokens",
            "not_jspace": "δ - jspace",
        },
        "controls": "each part's edit along seeded random directions at the same per-position norm; O's full copy",
        "outcome": "the patched continuation's first palette colour as a role (b = f(X), c, X, A, ...), as patch_map",
        "decision": {
            "step_score": "per item, the share of window layers at which the part's copy gives f(X)",
            "lens2": "J++ primary: the step is outside the lens's I/X coordinates if not_lens2's step score exceeds "
            "lens2's (paired bootstrap CI above 0) and lens2's does not exceed its null's (CI of lens2 - null not "
            "above 0); inside if lens2's exceeds not_lens2's and not_lens2's does not exceed its null's; otherwise "
            "both or neither",
            "jspace": "the same rule for jspace vs not_jspace: outside the J-space, inside it, or both or neither",
            "reproduce": "full must reproduce patch_map's after_start rows at the window layers item for item",
        },
        "deviations": [
            f"The J-space part is a {K_ATOMS}-atom approximation of the difference δ, not of each activation: signed "
            "coefficients, since δ removes I as it adds X. Its chance share of a random direction's variance is "
            "reported per layer.",
            "Each window layer is copied on its own, as in patch_map.",
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    map_dir = RESULTS / manifest["map"]["run"]
    assert sha256_of(map_dir / "summary.json") == manifest["map"]["summary_sha256"], "patch_map changed"
    item_file, _, load_items = ITEM_SETS[manifest["items"]["set"]]
    assert sha256_of(item_file) == manifest["items"]["sha256"], "brew items changed since the manifest"
    layers = manifest["layers"]
    model = load_model()
    tokenizer: Any = model.tokenizer
    items = load_items()
    palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
    # Phase 1: every eligible item's prompts, positions and activations at the window layers (as patch_map).
    cases, item_rows = [], []
    for index, item in enumerate(items):
        prep = prepare(item, index, tokenizer)
        row: dict[str, Any] = {"name": item["name"], "status": prep["status"]}
        item_rows.append(row)
        if prep["status"] != "ok":
            continue
        cfs = prep["cfs"]
        ids = torch.tensor([prep["ids"]], device="cuda")
        _, clean_h = model.run(ids, record=tuple(layers))
        colours = {"clean": answer_colour(model.generate(ids, MAX_NEW_TOKENS)[1], palette)}
        source_h = {}
        for source in SOURCES:
            source_ids = torch.tensor([prep["sources"][source]["ids"]], device="cuda")
            _, source_h[source] = model.run(source_ids, record=tuple(layers))
            colours[source] = answer_colour(model.generate(source_ids, MAX_NEW_TOKENS)[1], palette)
        ok = colours == {"clean": cfs["roles"]["A"], "cf": cfs["cf"]["answer"], "off": cfs["off"]["answer"]}
        row["status"] = "eligible" if ok else "not_eligible"
        if not ok:
            continue
        positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
        cases.append(
            {
                "index": index,
                "name": item["name"],
                "ids": ids,
                "roles": cfs["roles"],
                "positions": positions,
                "delta": {
                    s: {layer: (source_h[s][layer][positions] - clean_h[layer][positions]) for layer in layers}
                    for s in SOURCES
                },
                "h_norm": {layer: clean_h[layer][positions].norm(dim=-1) for layer in layers},
            }
        )
        del clean_h, source_h
    print(f"{len(cases)} eligible items", flush=True)

    outcomes, fve = [], []

    def run_edit(case, layer, delta, **tags):
        _, text, _ = model.generate(case["ids"], MAX_NEW_TOKENS, {layer: AddRows(delta, case["positions"])})
        colour = answer_colour(text, palette)
        outcomes.append(
            {
                "name": case["name"],
                "layer": layer,
                **tags,
                "continuation": text,
                "colour": colour,
                "role": category(colour, case["roles"]),
                "edit_ratio": round(float((delta.norm(dim=-1) / case["h_norm"][layer]).mean()), 4),
            }
        )

    # Phase 2: the full copies (lens-free), then each lens's parts.
    for case in cases:
        for layer in layers:
            for source in SOURCES:
                run_edit(case, layer, case["delta"][source][layer], lens=None, part="full", source=source, null=False)
    for lens_name in LENSES:
        lens = JLens(model, lens_name)
        letter_ids = model.letter_token_ids()
        dictionaries = {layer: lens.vectors(layer, letter_ids) for layer in layers}
        g = torch.Generator(device="cuda").manual_seed(BOOT_SEED)
        for layer in layers:
            x = torch.randn(CHANCE_DRAWS, dictionaries[layer].shape[1], device="cuda", generator=g)
            approx = signed_omp(dictionaries[layer], x, K_ATOMS)
            share = (approx.norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
            fve.append({"lens": lens_name, "layer": layer, "what": "chance", "share": round(float(share), 4)})
        for case in cases:
            roles = case["roles"]
            tok = torch.tensor([model.concept_token(roles["I"]), model.concept_token(roles["X"])], device="cuda")
            for layer in layers:
                delta = case["delta"]["cf"][layer]
                lens2 = lens2_part(delta, lens.vectors(layer, tok))
                jspace = signed_omp(dictionaries[layer], delta, K_ATOMS)
                total = float(delta.norm() ** 2)
                for what, part in (("lens2", lens2), ("jspace", jspace)):
                    fve.append(
                        {
                            "lens": lens_name,
                            "layer": layer,
                            "what": what,
                            "name": case["name"],
                            "share": round(float(part.norm() ** 2) / total, 4),
                        }
                    )
                parts = {"lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace, "not_jspace": delta - jspace}
                for pi, (part_name, part) in enumerate(parts.items()):
                    run_edit(case, layer, part, lens=lens_name, part=part_name, source="cf", null=False)
                    seed = NULL_SEED + 100_000 * LENSES.index(lens_name) + 1000 * case["index"] + 10 * layer + pi
                    noise = null_rows(part, torch.Generator(device="cuda").manual_seed(seed))
                    run_edit(case, layer, noise, lens=lens_name, part=part_name, source="cf", null=True)
            print(f"{lens_name} {case['name']}: done ({len(outcomes)} outcomes)", flush=True)
        del dictionaries
        torch.cuda.empty_cache()

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "fve.jsonl", fve)
    summary = summarize(outcomes, fve, layers, map_dir)
    summary["items"] = {s: sum(r["status"] == s for r in item_rows) for s in {r["status"] for r in item_rows}}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary, layers)
    print((out_dir / "summary.md").read_text())


def step_scores(outcomes: list[dict], **where) -> dict[str, float]:
    """Per item, the share of window layers at which the matching copies give f(X)."""
    hits: dict[str, list[bool]] = {}
    for o in outcomes:
        if all(o.get(k) == v for k, v in where.items()):
            hits.setdefault(o["name"], []).append(o["role"] == "b")
    return {n: sum(v) / len(v) for n, v in hits.items()}


def summarize(outcomes: list[dict], fve: list[dict], layers: list[int], map_dir: Path) -> dict:
    cells: dict[tuple, list[dict]] = {}
    for o in outcomes:
        cells.setdefault((o["lens"], o["part"], o["source"], o["null"], o["layer"]), []).append(o)
    rates = []
    for (lens, part, source, null, layer), batch in cells.items():
        n = len(batch)
        count = {r: sum(o["role"] == r for o in batch) for r in ("A", "b", "c", "X")}
        rates.append(
            {
                "lens": lens,
                "part": part,
                "source": source,
                "null": null,
                "layer": layer,
                "n": n,
                **{r: wilson(k, n) for r, k in count.items()},
                "edit_ratio_median": statistics.median(o["edit_ratio"] for o in batch),
            }
        )
    scores, decisions = {}, {}
    full = step_scores(outcomes, part="full", source="cf")
    scores["full"] = statistics.mean(full.values())
    for lens in LENSES:
        s = {(p, null): step_scores(outcomes, lens=lens, part=p, null=null) for p in PARTS for null in (False, True)}
        for (p, null), v in s.items():
            scores[f"{lens} {p}{' null' if null else ''}"] = statistics.mean(v.values())
        for inside, outside in (("lens2", "not_lens2"), ("jspace", "not_jspace")):
            names = sorted(s[inside, False])
            diff = paired_bootstrap_diff(
                [s[outside, False][n] for n in names], [s[inside, False][n] for n in names], N_BOOT, BOOT_SEED
            )
            above_null = {
                p: paired_bootstrap_diff(
                    [s[p, False][n] for n in names], [s[p, True][n] for n in names], N_BOOT, BOOT_SEED
                )
                for p in (inside, outside)
            }
            verdict = "both or neither"
            if diff[1] > 0 and above_null[inside][1] <= 0:
                verdict = "outside"
            elif diff[2] < 0 and above_null[outside][1] <= 0:
                verdict = "inside"
            decisions[f"{lens} {inside}"] = {
                f"{outside} - {inside}": diff,
                **{f"{p} - its null": d for p, d in above_null.items()},
                "verdict": verdict,
            }
    shares: dict[str, list[float]] = {}
    for f in fve:
        shares.setdefault(f"{f['lens']} {f['what']}", []).append(f["share"])
    before = {}
    with open(map_dir / "outcomes.jsonl") as f:
        map_outcomes = [json.loads(line) for line in f]
    for o in map_outcomes:
        if o["source"] == "cf" and o["group"] == "after_start" and o["layer"] in layers:
            before[o["name"], o["layer"]] = o["role"]
    now = {(o["name"], o["layer"]): o["role"] for o in outcomes if o["part"] == "full" and o["source"] == "cf"}
    both = [k for k in now if k in before]
    return {
        "rates": rates,
        "step_scores": scores,
        "decisions": decisions,
        "variance_share_median": {k: statistics.median(v) for k, v in shares.items()},
        "reproduce_full": {"cells": len(both), "match": sum(before[k] == now[k] for k in both)},
    }


def write_summary_md(path: Path, run: str, summary: dict, layers: list[int]) -> None:
    pct = lambda w: f"{100 * w[0]:.0f}%"  # noqa: E731
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [
        f"# {EXP} / {run}",
        "",
        "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()),
        f"Full copy reproduces patch_map (item x layer cells): {summary['reproduce_full']['match']}/"
        f"{summary['reproduce_full']['cells']}",
        "",
        "Step score (mean over items of the share of window layers giving f(X)):",
    ]
    lines += [f"- {k}: {100 * v:.0f}%" for k, v in summary["step_scores"].items()]
    lines += ["", "Decisions (paired bootstrap over items, pts):"]
    for k, d in summary["decisions"].items():
        lines.append(
            f"- {k}: "
            + "; ".join(f"{kk} {pts(vv)}" for kk, vv in d.items() if kk != "verdict")
            + f"; verdict: {d['verdict']}"
        )
    lines += ["", "Median share of δ's variance in each part (and of a random direction's, 'chance'):"]
    lines += [f"- {k}: {v:.3f}" for k, v in summary["variance_share_median"].items()]
    lines += [
        "",
        "| lens | part | source | null | layer | n | A | b = f(X) | c | X | edit ratio |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(summary["rates"], key=lambda r: (str(r["lens"]), r["part"], r["source"], r["null"], r["layer"])):
        lines.append(
            f"| {r['lens'] or ''} | {r['part']} | {r['source']} | {'yes' if r['null'] else ''} | {r['layer']} | {r['n']} | "
            f"{pct(r['A'])} | {pct(r['b'])} | {pct(r['c'])} | {pct(r['X'])} | {r['edit_ratio_median']:.3f} |"
        )
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument(
        "--map", dest="map_run", default=pins.RUN_PREFIX + "patch_map", help="manifest: the patch_map run"
    )
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.name, "manifest needs --name"
        stage_manifest(args.name, args.map_run)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
