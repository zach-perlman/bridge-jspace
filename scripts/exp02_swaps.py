"""exp02_swaps: swap the bridge entity's representation for the swap target's and see whether the answer follows,
under five definitions of "the representation".

Stages (each run's manifest is written before it runs; both are write-once; --name sets the run's folder,
default = the kind):
  manifest gate --probes TAG [--name N]              band sweep with the raw J-lens and full-probe swaps only
  run N
  manifest main --probes TAG --band A-B [--name N]   all five conditions and their random-direction nulls on one band
  run N

Swap (clamp.SwapClamp): at every band layer and every prompt position except 0, the clean coordinates on a set of
atoms are pinned, with the bridge's and the target's coordinates exchanged. The conditions differ only in the atoms.
Rows 0 and 1 are the bridge's and the target's; any further rows are held at their clean values.
  raw_jlens          J-lens vectors of the bridge's and the target's naming tokens
  full_probe         the unit exp01 probes
  jpart              the unit J-parts of the probes
  remainder          the unit remainders (probe - J-part)
  remainder_clamped  the remainder pair, plus every J-part atom of both entities and both naming-token vectors
Null: the same clamp with each position's edit replaced by a random unit direction (one per layer, seeded) scaled to
that edit's norm.

An item is eligible if its answer and swap answer have single-token surfaces, both entities have probes, and the
clean answer has word rank 1. A flip is the swap answer reaching word rank 1.
"""

import argparse
import csv
import json
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.clamp import SwapClamp, near_parallel  # noqa: E402
from bridge_jspace.data import load_items, sha256_of  # noqa: E402
from bridge_jspace.stats import paired_bootstrap_diff, wilson  # noqa: E402

EXP = "exp02_swaps"
RESULTS = pins.RESULTS_DIR / EXP
CONDITIONS = ("raw_jlens", "full_probe", "jpart", "remainder", "remainder_clamped")
GATE_CONDITIONS = ("raw_jlens", "full_probe")
GATE_BANDS = ("16-32", "24-40", "32-48", "24-48")
GO_FLIP_RATE = 0.30
NULL_SEED = 0
N_BOOT, BOOT_SEED = 2000, 0
COMPARISONS = (("jpart", "remainder"), ("remainder", "remainder_clamped"))
LABELS = {(True, False): "J-mediated", (False, True): "non-J", (True, True): "both", (False, False): "neither"}


def band_layers(band: str) -> tuple[int, ...]:
    """'24-40' -> 24..40 inclusive."""
    lo, hi = map(int, band.split("-"))
    return tuple(range(lo, hi + 1))


def probes_file(tag: str) -> Path:
    return pins.CACHE_DIR / "exp01" / tag / "probes.pt"


def stage_manifest(kind: str, name: str, probes_tag: str, band: str | None) -> None:
    is_gate = kind == "gate"
    assert is_gate == (band is None), "the gate sweeps its own bands; main needs --band"
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    probes = probes_file(probes_tag)
    definition = torch.load(probes, map_location="cpu", weights_only=True).get("definition", "mean_difference")
    deviations = [
        "Items whose answer or swap answer has no single-token surface are dropped and counted (7 of 90 at setup).",
        "Edit size is the direct edit at the final position, |delta| / |h|, averaged over the edited band layers per "
        "item and reported as the median over items; the edit's downstream effect on later layers is not measured.",
        "Layers where the two swapped atoms are near-parallel (|cos| > 0.999) are skipped and counted.",
    ]
    if is_gate:
        decision = (f"band = the one with the highest full_probe flip rate (first in {list(GATE_BANDS)} on ties); "
                    f"go if that rate >= {GO_FLIP_RATE}, else stop and debug before decomposing. The band is chosen "
                    "on the same items, so its full_probe rate is optimistic.")
        if name != "gate":
            deviations.append("A repeat of the gate with different probes after the first gate (results/exp02_swaps/"
                              "gate) failed; the same items are reused, so passing it is optimistic twice over.")
    else:
        decision = {"paired_bootstraps": [f"{a} - {b}" for a, b in COMPARISONS],
                    "bootstrap": f"B={N_BOOT}, seed {BOOT_SEED}, resampling eligible items",
                    "labels": "2x2 on (jpart flips, remainder_clamped flips): " +
                              ", ".join(f"{v} = {k}" for k, v in LABELS.items())}
        deviations.append("Null direction: one random unit direction per (item, condition, layer), shared across "
                          "positions and scaled to each position's own edit norm, so it matches the real edit, "
                          "which lies in one fixed low-dimensional span at every position.")
    manifest = {
        "exp": EXP, "run": name, "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Does the swap target's answer appear when the bridge's representation is swapped for the "
                    "target's, and does that depend on the J-space part of the representation?",
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "lens": {"repo": pins.LENS_REPO, "revision": pins.LENS_REVISION, "file": pins.LENS_FILE},
        "items": {"file": "data/probe_swap.json", "sha256": pins.PROBE_SWAP_SHA256},
        "probes": {"exp01_tag": probes_tag, "file": str(probes.relative_to(pins.REPO_ROOT)),
                   "sha256": sha256_of(probes), "definition": definition},
        "bands": list(GATE_BANDS) if is_gate else [band],
        "conditions": list(GATE_CONDITIONS if is_gate else CONDITIONS),
        "nulls": not is_gate,
        "null_seed": NULL_SEED,
        "swap": "clamp.SwapClamp at every band layer, positions 1.. (not 0); atoms per condition as in the script "
                "docstring; unit atoms throughout",
        "eligibility": "answer and swap answer have single-token surfaces; both entities have probes; clean answer "
                       "at word rank 1 (formatting tokens excluded)",
        "flip": "swap answer at word rank 1 after the swap",
        "metrics": ["flip rate, Wilson 95% CI", "share keeping the clean answer at rank 1, Wilson 95% CI",
                    "share with neither (collateral damage)", "median edit ratio", "items with skipped layers"],
        "decision": decision,
        "deviations": deviations,
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


class Probes:
    """exp01's probes and their decompositions, indexed by entity and layer (on the GPU)."""

    def __init__(self, path: Path):
        blob = torch.load(path, map_location="cpu", weights_only=True)
        self.index = {e: i for i, e in enumerate(blob["entities"])}
        self.layer_index = {l: i for i, l in enumerate(blob["layers"])}
        self.parts = {"full_probe": blob["probe"].cuda(), "jpart": blob["jpart"].cuda()}
        self.parts["remainder"] = self.parts["full_probe"] - self.parts["jpart"]
        self.atom_ids = blob["atom_ids"]  # {layer: [entity index -> token ids]}

    def unit(self, part: str, entity: str, layer: int) -> torch.Tensor:
        v = self.parts[part][self.index[entity], self.layer_index[layer]]
        assert v.norm() > 0, f"zero {part} for {entity} at layer {layer}"
        return v / v.norm()

    def jpart_atoms(self, entity: str, layer: int) -> list[int]:
        return self.atom_ids[layer][self.index[entity]]


def condition_atoms(condition: str, item: dict, layer: int, probes: Probes, lens, model) -> torch.Tensor:
    """Atoms [K, d] for one condition at one layer: row 0 the bridge's, row 1 the target's, the rest held fixed."""
    bridge, target = item["intermediate"], item["swap_to"]
    naming = [model.concept_token(bridge), model.concept_token(target)]
    if condition == "raw_jlens":
        return lens.vectors(layer, torch.tensor(naming, device="cuda"))
    part = "remainder" if condition == "remainder_clamped" else condition
    pair = torch.stack([probes.unit(part, bridge, layer), probes.unit(part, target, layer)])
    if condition != "remainder_clamped":
        return pair
    held = sorted(set(probes.jpart_atoms(bridge, layer)) | set(probes.jpart_atoms(target, layer)) | set(naming))
    return torch.cat([pair, lens.vectors(layer, torch.tensor(held, device="cuda"))])


def swap(model, ids, clean_h, atoms_by_layer, answer_ids, swap_ids, null_seed: int | None) -> dict:
    """One swapped forward; returns its scores."""
    generator = None if null_seed is None else torch.Generator(device="cuda").manual_seed(null_seed)
    clamps, skipped = {}, []
    for layer, atoms in atoms_by_layer.items():
        direction = None
        if generator is not None:  # drawn for every layer, so a layer's direction does not depend on skips
            direction = torch.nn.functional.normalize(
                torch.randn(atoms.shape[1], device="cuda", generator=generator), dim=0)
        if near_parallel(atoms[0], atoms[1]):
            skipped.append(layer)
            continue
        clamps[layer] = SwapClamp(atoms, clean_h[layer], null_direction=direction)
    logits, _ = model.run(ids, edits=clamps)
    swap_rank, clean_rank = model.word_rank(logits, swap_ids), model.word_rank(logits, answer_ids)
    return {"flip": swap_rank == 1, "kept_clean": clean_rank == 1, "swap_rank": swap_rank, "clean_rank": clean_rank,
            "top_word": model.top_word(logits),
            "edit_ratio": statistics.mean(c.edit_ratio_last for c in clamps.values()) if clamps else 0.0,
            "layers_skipped": skipped}


def prepare(model, probes: Probes, item: dict, layers: list[int]):
    """The item's status, and for eligible items the encoded prompt and clean residuals at `layers`."""
    row = {k: item[k] for k in ("name", "category", "intermediate", "swap_to", "answer", "swap_answer")}
    answer_ids, swap_ids = model.surface_ids(item["answer"]), model.surface_ids(item["swap_answer"])
    missing = [e for e in (item["intermediate"], item["swap_to"]) if e not in probes.index]
    if not answer_ids or not swap_ids:
        return {**row, "status": "multi_token_answer"}, None
    if missing:
        return {**row, "status": "no_probe:" + "+".join(missing)}, None
    ids = model.encode(item["prompt"])
    logits, clean_h = model.run(ids, record=tuple(layers))
    clean_rank = model.word_rank(logits, answer_ids)
    row.update(status="eligible" if clean_rank == 1 else "clean_wrong", clean_rank=clean_rank,
               clean_top_word=model.top_word(logits))
    return row, (ids, clean_h, answer_ids, swap_ids)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    kind = manifest["kind"]
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    probes_path = pins.REPO_ROOT / manifest["probes"]["file"]
    assert sha256_of(probes_path) == manifest["probes"]["sha256"], "probes.pt changed since the manifest"
    bands, conditions = manifest["bands"], manifest["conditions"]
    null_options = (False, True) if manifest["nulls"] else (False,)

    model = load_model()
    lens = JLens(model)
    probes = Probes(probes_path)
    all_layers = sorted({l for band in bands for l in band_layers(band)})
    item_rows, outcomes = [], []
    for index, item in enumerate(load_items()):
        row, prepared = prepare(model, probes, item, all_layers)
        item_rows.append(row)
        if row["status"] != "eligible":
            continue
        ids, clean_h, answer_ids, swap_ids = prepared
        for band in bands:
            for ci, condition in enumerate(conditions):
                atoms = {l: condition_atoms(condition, item, l, probes, lens, model) for l in band_layers(band)}
                for null in null_options:
                    seed = NULL_SEED + 1000 * index + ci if null else None
                    outcomes.append({"name": item["name"], "band": band, "condition": condition, "null": null,
                                     **swap(model, ids, clean_h, atoms, answer_ids, swap_ids, seed)})
        print(f"{item['name']}: " + " ".join(f"{o['condition']}{'/null' if o['null'] else ''}@{o['band']}="
                                             f"{int(o['flip'])}" for o in outcomes if o["name"] == item["name"]),
              flush=True)

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    rows = summarize(outcomes)
    summary = {"items": status_counts(item_rows), "rates": rows}
    if kind == "gate":
        summary["decision"] = gate_decision(rows)
    else:
        eligible = [r["name"] for r in item_rows if r["status"] == "eligible"]
        summary["paired_bootstraps"] = bootstraps(outcomes, eligible)
        summary["labels"] = write_labels(out_dir / "labels.csv", item_rows, outcomes, conditions)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def status_counts(item_rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in item_rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return counts


def summarize(outcomes: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for o in outcomes:
        groups.setdefault((o["band"], o["condition"], o["null"]), []).append(o)
    rows = []
    for (band, condition, null), group in groups.items():
        n = len(group)
        flips, kept = sum(o["flip"] for o in group), sum(o["kept_clean"] for o in group)
        rows.append({"band": band, "condition": condition, "null": null, "n": n,
                     "flip": wilson(flips, n), "kept_clean": wilson(kept, n), "neither": (n - flips - kept) / n,
                     "edit_ratio_median": statistics.median(o["edit_ratio"] for o in group),
                     "items_with_skipped_layers": sum(bool(o["layers_skipped"]) for o in group)})
    return rows


def gate_decision(rows: list[dict]) -> dict:
    full = {r["band"]: r["flip"][0] for r in rows if r["condition"] == "full_probe"}
    band = max(GATE_BANDS, key=lambda b: full[b])  # max keeps the first of equal values
    return {"band": band, "full_probe_flip_rate": full[band], "threshold": GO_FLIP_RATE,
            "go": full[band] >= GO_FLIP_RATE}


def flips(outcomes: list[dict], condition: str, null: bool = False) -> dict[str, bool]:
    return {o["name"]: o["flip"] for o in outcomes if o["condition"] == condition and o["null"] == null}


def bootstraps(outcomes: list[dict], eligible: list[str]) -> dict[str, tuple[float, float, float]]:
    out = {}
    for a, b in COMPARISONS:
        fa, fb = flips(outcomes, a), flips(outcomes, b)
        out[f"{a} - {b}"] = paired_bootstrap_diff([fa[n] for n in eligible], [fb[n] for n in eligible],
                                                  n_boot=N_BOOT, seed=BOOT_SEED)
    return out


def write_labels(path: Path, item_rows: list[dict], outcomes: list[dict], conditions) -> dict[str, int]:
    """Every item, with its status, per-condition flips (real and null) and, for eligible items, its label."""
    real = {c: flips(outcomes, c) for c in conditions}
    null = {c: flips(outcomes, c, null=True) for c in conditions}
    columns = (["name", "category", "intermediate", "swap_to", "answer", "swap_answer", "status", "clean_rank"]
               + [f"flip_{c}" for c in conditions] + [f"null_flip_{c}" for c in conditions] + ["label"])
    counts = {label: 0 for label in LABELS.values()}
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for r in item_rows:
            out = dict(r)
            if r["status"] == "eligible":
                name = r["name"]
                out.update({f"flip_{c}": int(real[c][name]) for c in conditions})
                out.update({f"null_flip_{c}": int(null[c][name]) for c in conditions})
                out["label"] = LABELS[(real["jpart"][name], real["remainder_clamped"][name])]
                counts[out["label"]] += 1
            writer.writerow(out)
    return counts


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pct = lambda w: f"{100 * w[0]:.0f}% [{100 * w[1]:.0f}, {100 * w[2]:.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {run}", "", "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()), "",
             "| band | condition | null | n | flip [95% CI] | kept clean [95% CI] | neither | edit ratio (median) | "
             "items with skipped layers |", "|---|---|---|---|---|---|---|---|---|"]
    for r in summary["rates"]:
        lines.append(f"| {r['band']} | {r['condition']} | {'yes' if r['null'] else ''} | {r['n']} | "
                     f"{pct(r['flip'])} | {pct(r['kept_clean'])} | {100 * r['neither']:.0f}% | "
                     f"{r['edit_ratio_median']:.3f} | {r['items_with_skipped_layers']} |")
    if "decision" in summary:
        d = summary["decision"]
        lines += ["", f"Gate: band {d['band']}, full-probe flip rate {100 * d['full_probe_flip_rate']:.0f}% "
                      f"(threshold {100 * d['threshold']:.0f}%): {'GO' if d['go'] else 'STOP and debug'}."]
    if "paired_bootstraps" in summary:
        lines += ["", "Paired bootstrap differences in flip rate:"]
        lines += [f"- {k}: {100 * v[0]:+.0f} pts [{100 * v[1]:+.0f}, {100 * v[2]:+.0f}]"
                  for k, v in summary["paired_bootstraps"].items()]
        lines += ["", "Labels: " + ", ".join(f"{k} {v}" for k, v in summary["labels"].items())]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", help="manifest: the kind (gate or main); run: the run's folder name")
    parser.add_argument("--probes", help="exp01 run tag (manifest stage)")
    parser.add_argument("--band", help="A-B, inclusive (main manifest only)")
    parser.add_argument("--name", help="the run's folder name (manifest stage; default = the kind)")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.target in ("gate", "main") and args.probes, "manifest needs a kind (gate/main) and --probes"
        stage_manifest(args.target, args.name or args.target, args.probes, args.band)
    else:
        stage_run(args.target)
