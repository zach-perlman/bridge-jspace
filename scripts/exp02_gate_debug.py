"""exp02_swaps gate debug: why does the full-probe swap flip few answers when the raw J-lens swap flips half?
No swaps; three diagnostics on the exp01 probes, per layer 16..48 (results/exp02_swaps/gate_debug/, write-once).

  identity   leave-one-prompt-out nearest-probe accuracy on the kept entity prompts (cosine, centred like the probes):
             do the probes carry entity identity on their own prompts? Chance is 1 / number of probes.
  detection  on the gate's eligible test items, clean pass: the bridge's rank among all probes by cosine with the
             centred residual, at the final position and at the best position; next to it, the bridge's naming token's
             rank among all probed entities' naming tokens by J-lens logit at the final position.
  asymmetry  share of items whose clean coordinate (pinv, final position, uncentred as in the clamp) on the bridge
             atom exceeds that on the target atom, for full-probe atoms and for raw J-lens atoms; plus the median
             |cos| between the two atoms.

Stages: manifest, then run. Also checks that the recomputed probes reproduce exp01's.

Follow-up part "presence" (results/exp02_swaps/gate_debug_presence/): is the entity present at the probe position?
  presence   on the kept entity prompts, final position: the entity's naming-token rank among all probed entities'
             naming tokens by J-lens logit (the same measure as 'detection' on the test items).
  eta2       share of the kept prompts' residual variance explained by entity labels, with its chance level under
             random labels, (E - 1) / (N - 1).

Follow-up part "centred" (results/exp02_swaps/gate_debug_centred/): does centring the clamp's coordinates help?
  centred    the 'asymmetry' share (bridge coordinate > target coordinate, final position) with coordinates read
             from h (as the clamp does) and from h - m (m = the probes' reference point, the mean of the entity
             means), for the mean-difference probes (v2), the whitened probes (w1) and the raw J-lens atoms.
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.data import load_items, sha256_of
from bridge_jspace.run_switches import check_switches, switches

OUTS = {
    "core": pins.RESULTS_DIR / "exp02_swaps" / "gate_debug",
    "presence": pins.RESULTS_DIR / "exp02_swaps" / "gate_debug_presence",
    "centred": pins.RESULTS_DIR / "exp02_swaps" / "gate_debug_centred",
}
WHITENED_TAG = "w1"
QUESTIONS = {
    "core": "Is the full probe weak because it lacks entity identity (prompts), because it does not detect the bridge "
    "in the test prompts (probe position / distribution), or because the swap does not propagate (band)?",
    "presence": "gate_debug found weak identity (LOO top-1 <= 0.28) and chance-level bridge/target asymmetry. Is the "
    "entity absent at the probe position, or present but swamped by other variance?",
    "centred": "The whitened probes also failed the gate (gate_w1: 8%). The clamp reads coordinates from the raw "
    "residual, but the probes are defined relative to the mean of the entity means, so each swap also "
    "exchanges that mean's coordinates. Does centring the coordinates restore bridge/target asymmetry?",
}
OUT = OUTS["core"]
PROBES_TAG = "v2"
LAYERS = tuple(range(16, 49))
FILTER = pins.RESULTS_DIR / "exp01_probes" / PROBES_TAG / "filter.jsonl"
GATE_ITEMS = pins.RESULTS_DIR / "exp02_swaps" / "gate" / "items.jsonl"


def probes_path(tag: str = PROBES_TAG) -> Path:
    return pins.CACHE_DIR / "exp01" / tag / "probes.pt"


def stage_manifest(part: str) -> None:
    out = OUTS[part]
    out.mkdir(parents=True, exist_ok=True)
    path = out / "manifest.json"
    assert not path.exists(), f"{path} exists; manifests are written once"
    paragraphs = (__doc__ or "").split("\n\n")
    inputs = {
        "probes": {"file": str(probes_path().relative_to(pins.REPO_ROOT)), "sha256": sha256_of(probes_path())},
        "kept_prompts": str(FILTER.relative_to(pins.REPO_ROOT)),
        "eligible_items": str(GATE_ITEMS.relative_to(pins.REPO_ROOT)),
    }
    if part == "centred":
        inputs["whitened_probes"] = {
            "file": str(probes_path(WHITENED_TAG).relative_to(pins.REPO_ROOT)),
            "sha256": sha256_of(probes_path(WHITENED_TAG)),
        }
    manifest = {
        "exp": "exp02_swaps",
        "run": out.name,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": "gate failed: best full-probe flip rate 17% (band 32-48) < 30%; raw J-lens 55% at a ~9x smaller edit",
        "switches": switches(),
        "question": QUESTIONS[part],
        "inputs": inputs,
        "layers": list(LAYERS),
        "diagnostics": paragraphs[{"core": 1, "presence": 3, "centred": 4}[part]],
        "no_swaps": True,
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def rank_of(scores: torch.Tensor, index: int) -> int:
    """1 + the number of entries of a score vector [E] above entry `index`."""
    return int((scores > scores[index]).sum()) + 1


def best_rank(scores: torch.Tensor, index: int) -> int:
    """The best rank of entry `index` over the rows (positions) of scores [S, E]."""
    return min(rank_of(row, index) for row in scores)


def kept_residuals(model, entities: list[str]) -> dict[str, list[torch.Tensor]]:
    """Final-token residuals [L, d] of each probed entity's kept prompts, as in exp01."""
    residuals = {e: [] for e in entities}
    for r in map(json.loads, FILTER.read_text().splitlines()):
        if r["kept"] and r["entity"] in residuals:
            _, h = model.run(model.encode(r["prompt"]), record=LAYERS)
            residuals[r["entity"]].append(torch.stack([h[layer][-1] for layer in LAYERS]))
    return residuals


@torch.no_grad()
def stage_run_centred() -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out = OUTS["centred"]
    manifest = json.loads((out / "manifest.json").read_text())
    check_switches(manifest)
    assert not (out / "summary.json").exists(), "results are write-once"
    assert sha256_of(probes_path()) == manifest["inputs"]["probes"]["sha256"]
    assert sha256_of(probes_path(WHITENED_TAG)) == manifest["inputs"]["whitened_probes"]["sha256"]
    blobs = {
        tag: torch.load(probes_path(tag), map_location="cpu", weights_only=True) for tag in (PROBES_TAG, WHITENED_TAG)
    }
    entities = blobs[PROBES_TAG]["entities"]
    assert blobs[WHITENED_TAG]["entities"] == entities
    index = {e: i for i, e in enumerate(entities)}
    model = load_model()
    lens = JLens(model)

    residuals = kept_residuals(model, entities)
    grand = torch.stack([torch.stack(residuals[e]).mean(0) for e in entities]).mean(0)  # [L, d], the probes' origin
    probe_atoms = {tag: torch.nn.functional.normalize(blob["probe"].cuda(), dim=-1) for tag, blob in blobs.items()}
    naming = torch.tensor([model.concept_token(e) for e in entities], device="cuda")
    eligible = {r["name"] for r in map(json.loads, GATE_ITEMS.read_text().splitlines()) if r["status"] == "eligible"}
    items = [i for i in load_items() if i["name"] in eligible]
    kinds = (PROBES_TAG, WHITENED_TAG, "raw_jlens")
    higher = {(kind, centred): [[] for _ in LAYERS] for kind in kinds for centred in (False, True)}
    for item in items:
        b, t = index[item["intermediate"]], index[item["swap_to"]]
        _, h = model.run(model.encode(item["prompt"]), record=LAYERS)
        for li, layer in enumerate(LAYERS):
            x = h[layer][-1]
            atoms = {
                PROBES_TAG: probe_atoms[PROBES_TAG][[b, t], li],
                WHITENED_TAG: probe_atoms[WHITENED_TAG][[b, t], li],
                "raw_jlens": lens.vectors(layer, naming[[b, t]]),
            }
            for kind, a in atoms.items():
                pinv = torch.linalg.pinv(a)
                for centred in (False, True):
                    c = (x - grand[li] if centred else x) @ pinv
                    higher[(kind, centred)][li].append(float(c[0] > c[1]))

    per_layer = {
        layer: {
            f"{kind}_{'h_minus_m' if centred else 'h'}": statistics.mean(higher[(kind, centred)][li])
            for kind in kinds
            for centred in (False, True)
        }
        for li, layer in enumerate(LAYERS)
    }
    summary = {"n_items": len(items), "per_layer": per_layer}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# exp02_swaps / gate_debug_centred",
        "",
        f"Share of {len(items)} eligible items whose bridge coordinate exceeds the target coordinate at the "
        "final position (0.5 = no asymmetry), coordinates read from h or from h - m.",
        "",
        f"| layer | mean-difference probes ({PROBES_TAG}): h / h - m | whitened probes ({WHITENED_TAG}): h / h - m | "
        "raw J-lens: h / h - m |",
        "|---|---|---|---|",
    ]
    for layer, s in per_layer.items():
        lines.append(
            f"| {layer} | "
            + " | ".join(f"{s[kind + '_h']:.2f} / {s[kind + '_h_minus_m']:.2f}" for kind in kinds)
            + " |"
        )
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


@torch.no_grad()
def stage_run_presence() -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out = OUTS["presence"]
    manifest = json.loads((out / "manifest.json").read_text())
    check_switches(manifest)
    assert not (out / "summary.json").exists(), "results are write-once"
    assert sha256_of(probes_path()) == manifest["inputs"]["probes"]["sha256"]
    entities = torch.load(probes_path(), map_location="cpu", weights_only=True)["entities"]
    model = load_model()
    lens = JLens(model)
    naming = torch.tensor([model.concept_token(e) for e in entities], device="cuda")

    residuals = kept_residuals(model, entities)
    ranks = [[] for _ in LAYERS]
    for ei, e in enumerate(entities):
        for x in residuals[e]:
            for li, layer in enumerate(LAYERS):
                ranks[li].append(rank_of(lens.readout(x[li], layer)[naming], ei))
    X = torch.cat([torch.stack(residuals[e]) for e in entities])  # [N, L, d]
    labels = torch.cat([torch.full((len(residuals[e]),), ei) for ei, e in enumerate(entities)]).cuda()
    centred = X - X.mean(0)
    means = torch.stack([centred[labels == ei].mean(0) for ei in range(len(entities))])  # [E, L, d]
    counts = torch.bincount(labels, minlength=len(entities)).float().view(-1, 1)
    eta2 = ((counts * means.pow(2).sum(-1)).sum(0) / centred.pow(2).sum(-1).sum(0)).tolist()  # [L]
    chance = (len(entities) - 1) / (len(X) - 1)

    per_layer = {
        layer: {
            "lens_top1_own_entity": statistics.mean(r == 1 for r in ranks[li]),
            "lens_rank_own_entity_median": statistics.median(ranks[li]),
            "eta2": eta2[li],
        }
        for li, layer in enumerate(LAYERS)
    }
    summary = {
        "n_entities": len(entities),
        "n_kept_prompts": len(X),
        "chance_top1": 1 / len(entities),
        "eta2_chance": chance,
        "per_layer": per_layer,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# exp02_swaps / gate_debug_presence",
        "",
        f"{len(entities)} entities, {len(X)} kept prompts; chance top-1 {1 / len(entities):.3f}; "
        f"eta2 chance under random labels {chance:.3f}.",
        "",
        "| layer | J-lens: own entity top-1 at final position (median rank) | eta2 (entity labels) |",
        "|---|---|---|",
    ]
    lines += [
        f"| {layer} | {s['lens_top1_own_entity']:.2f} ({s['lens_rank_own_entity_median']:.0f}) | {s['eta2']:.3f} |"
        for layer, s in per_layer.items()
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


@torch.no_grad()
def stage_run() -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    manifest = json.loads((OUT / "manifest.json").read_text())
    check_switches(manifest)
    assert not (OUT / "summary.json").exists(), "results are write-once"
    assert sha256_of(probes_path()) == manifest["inputs"]["probes"]["sha256"]
    blob = torch.load(probes_path(), map_location="cpu", weights_only=True)
    entities, index = blob["entities"], {e: i for i, e in enumerate(blob["entities"])}
    model = load_model()
    lens = JLens(model)

    residuals = kept_residuals(model, entities)
    sums = torch.stack([torch.stack(residuals[e]).sum(0) for e in entities])  # [E, L, d]
    counts = torch.tensor([len(residuals[e]) for e in entities], device="cuda").view(-1, 1, 1)
    grand = (sums / counts).mean(0)  # [L, d]
    probes = sums / counts - grand
    reproduce_err = float((probes.cpu() - blob["probe"]).abs().max() / blob["probe"].abs().max())

    # identity: leave-one-prompt-out nearest probe.
    unit = torch.nn.functional.normalize
    correct = torch.zeros(len(LAYERS))
    n_prompts = 0
    for ei, e in enumerate(entities):
        for x in residuals[e]:  # [L, d]
            loo = probes.clone()
            loo[ei] = (sums[ei] - x) / (counts[ei] - 1) - grand
            cos = torch.einsum("eld,ld->le", unit(loo, dim=-1), unit(x - grand, dim=-1))  # [L, E]
            correct += (cos.argmax(-1) == ei).float().cpu()
            n_prompts += 1
    identity = (correct / n_prompts).tolist()

    # detection and asymmetry on the eligible test items.
    eligible = {r["name"] for r in map(json.loads, GATE_ITEMS.read_text().splitlines()) if r["status"] == "eligible"}
    items = [i for i in load_items() if i["name"] in eligible]
    naming = torch.tensor([model.concept_token(e) for e in entities], device="cuda")
    det_final, det_best, det_lens = ([[] for _ in LAYERS] for _ in range(3))
    asym_probe, asym_raw, cos_probe, cos_raw = ([[] for _ in LAYERS] for _ in range(4))
    for item in items:
        b, t = index[item["intermediate"]], index[item["swap_to"]]
        _, h = model.run(model.encode(item["prompt"]), record=LAYERS)
        for li, layer in enumerate(LAYERS):
            P = unit(probes[:, li], dim=-1)  # [E, d]
            cos = unit(h[layer][1:] - grand[li], dim=-1) @ P.T  # [S-1, E]
            det_final[li].append(rank_of(cos[-1], b))
            det_best[li].append(best_rank(cos, b))
            lens_logits = lens.readout(h[layer][-1], layer)[naming]  # [E]
            det_lens[li].append(rank_of(lens_logits, b))
            for atoms, asym, cosines in (
                (P[[b, t]], asym_probe, cos_probe),
                (lens.vectors(layer, naming[[b, t]]), asym_raw, cos_raw),
            ):
                c = h[layer][-1] @ torch.linalg.pinv(atoms)
                asym[li].append(float(c[0] > c[1]))
                cosines[li].append(abs(float(atoms[0] @ atoms[1])))

    per_layer = {
        layer: {
            "identity_loo_acc": identity[li],
            "probe_rank_final_median": statistics.median(det_final[li]),
            "probe_top1_final": statistics.mean(r == 1 for r in det_final[li]),
            "probe_rank_best_pos_median": statistics.median(det_best[li]),
            "probe_top1_best_pos": statistics.mean(r == 1 for r in det_best[li]),
            "lens_rank_final_median": statistics.median(det_lens[li]),
            "lens_top1_final": statistics.mean(r == 1 for r in det_lens[li]),
            "bridge_coord_higher_probe": statistics.mean(asym_probe[li]),
            "bridge_coord_higher_raw": statistics.mean(asym_raw[li]),
            "atom_abs_cos_probe_median": statistics.median(cos_probe[li]),
            "atom_abs_cos_raw_median": statistics.median(cos_raw[li]),
        }
        for li, layer in enumerate(LAYERS)
    }
    summary = {
        "n_entities": len(entities),
        "n_kept_prompts": n_prompts,
        "n_items": len(items),
        "chance_top1": 1 / len(entities),
        "probe_reproduction_max_rel_err": reproduce_err,
        "per_layer": per_layer,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# exp02_swaps / gate_debug",
        "",
        f"{len(entities)} probes, {n_prompts} kept prompts, {len(items)} eligible items; chance top-1 "
        f"{1 / len(entities):.3f} (higher for 'best pos', which takes the best of every prompt position); "
        f"recomputed probes match exp01 to max rel err {reproduce_err:.1e}.",
        "",
        "| layer | identity (LOO top-1) | probe detects bridge: top-1 final / best pos (median rank final) | "
        "J-lens detects bridge: top-1 final (median rank) | bridge coord > target: probe / raw | "
        "atom abs cos: probe / raw |",
        "|---|---|---|---|---|---|",
    ]
    for layer, s in per_layer.items():
        lines.append(
            f"| {layer} | {s['identity_loo_acc']:.2f} | {s['probe_top1_final']:.2f} / "
            f"{s['probe_top1_best_pos']:.2f} ({s['probe_rank_final_median']:.0f}) | "
            f"{s['lens_top1_final']:.2f} ({s['lens_rank_final_median']:.0f}) | "
            f"{s['bridge_coord_higher_probe']:.2f} / {s['bridge_coord_higher_raw']:.2f} | "
            f"{s['atom_abs_cos_probe_median']:.2f} / {s['atom_abs_cos_raw_median']:.2f} |"
        )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("part", nargs="?", default="core", choices=list(OUTS))
    args = parser.parse_args()
    if args.stage == "manifest":
        stage_manifest(args.part)
    elif args.part == "core":
        stage_run()
    elif args.part == "presence":
        stage_run_presence()
    else:
        stage_run_centred()
