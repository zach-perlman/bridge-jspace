"""exp01_probes: a bridge probe for each of the 97 entities, split into a J-space part and a remainder.

Stages (run in order):
  check            the entity prompts against the rules in data/entity_prompts.json (tokenizer only, no GPU)
  manifest         write results/exp01_probes/manifest.json before any measurement
  run --tag TAG    keep the prompts Qwen answers correctly, build the probes, decompose them. Writes
                   results/exp01_probes/TAG/ and cache/exp01/TAG/probes.pt (both write-once)
With --topup, each stage uses the prompts plus data/entity_prompts_topup.json (the one allowed top-up round for the
entities left with fewer than MIN_KEPT kept prompts in run TOPUP_AFTER); its manifest is manifest_topup.json.

Probe of entity e at layer l: the mean final-token residual (output of block l) over e's kept prompts, minus the mean
of those entity means over all entities. Decomposition: non-negative OMP with K_ATOMS atoms over the unit J-lens
vectors of every letter-bearing token at that layer; J-part = the fit, remainder = probe - J-part.
"""

import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.data import (check_entity_prompts, entities_of, first_word, load_entity_prompts,  # noqa: E402
                                load_items, sha256_of)

EXP = "exp01_probes"
RESULTS = pins.RESULTS_DIR / EXP
PROBE_LAYERS = tuple(range(16, 49))  # the union of the candidate bands that exp02 sweeps
K_ATOMS = 25
MIN_KEPT = 3
GREEDY_TOKENS = 8
REVIEW_SEED = 0
REVIEW_SAMPLE = 25
INSPECT_LAYER = 32
RANDOM_SEED = 0
TOPUP_AFTER = "v1"


def manifest_path(topup: bool) -> Path:
    return RESULTS / ("manifest_topup.json" if topup else "manifest.json")


def stage_check(topup: bool) -> None:
    prompts, items = load_entity_prompts(topup), load_items()
    problems = check_entity_prompts(prompts, items)
    n = sum(len(rows) for rows in prompts.values())
    print(f"{len(prompts)} entities, {n} prompts, {len(problems)} problems")
    for p in problems:
        print(" -", p)
    sys.exit(1 if problems else 0)


def stage_manifest() -> None:
    path = RESULTS / "manifest.json"
    RESULTS.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Build a bridge probe per entity and measure how much of it the J-lens dictionary explains.",
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "lens": {"repo": pins.LENS_REPO, "revision": pins.LENS_REVISION, "file": pins.LENS_FILE,
                 "vector": "v_t = (g * W_U[t]) @ J_l, unit-normalised; g = final-norm gain (1 + weight)"},
        "data": {"probe_swap": {"file": "data/probe_swap.json", "sha256": pins.PROBE_SWAP_SHA256},
                 "entity_prompts": {"file": "data/entity_prompts.json",
                                    "sha256": sha256_of(pins.ENTITY_PROMPTS_FILE)}},
        "prompt_format": "raw text, no chat template, no special tokens added",
        "filter": f"keep a prompt if the first word of Qwen's greedy continuation ({GREEDY_TOKENS} tokens) equals "
                  "an accepted answer, case-insensitively",
        "min_kept_prompts_per_entity": MIN_KEPT,
        "probe": "mean final-token residual (block output) over kept prompts minus the mean over entities",
        "probe_layers": list(PROBE_LAYERS),
        "decomposition": {"method": "non-negative OMP, NNLS refit each step", "k_atoms": K_ATOMS,
                          "dictionary": "unit J-lens vectors of non-special tokens whose decode has a letter"},
        "metrics": ["kept prompts per entity", "fraction of probe variance in the J-part per layer",
                    "chance level of that fraction: the same decomposition of isotropic random directions "
                    f"(one per probed entity per layer, seed {RANDOM_SEED})",
                    "whether the entity's own token is among its J-part atoms"],
        "review": {"seed": REVIEW_SEED, "sample_size": REVIEW_SAMPLE, "inspect_layer": INSPECT_LAYER},
        "deviations": [
            "J-lens vectors include the final-norm gain g (the reference omits it); g rescales dimensions unevenly, so "
            "these are the directions the lens's readout actually uses.",
            "Added (not in the plan): the random-direction chance level for the J-part share.",
            "Entity prompts were written by the coding agent and pass the mechanical checks in data.py; the human has "
            "not reviewed them yet.",
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def stage_manifest_topup() -> None:
    """The base manifest plus the top-up: which entities, why (their kept counts in run TOPUP_AFTER), the file."""
    path = manifest_path(topup=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path(topup=False).read_text())
    kept = json.loads((RESULTS / TOPUP_AFTER / "summary.json").read_text())["kept_per_entity"]
    short = {e: n for e, n in kept.items() if n < MIN_KEPT}
    topped_up = json.loads(pins.ENTITY_PROMPTS_TOPUP_FILE.read_text())["entities"]
    assert sorted(topped_up) == sorted(short), f"top-up entities {sorted(topped_up)} != short entities {short}"
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["data"]["entity_prompts_topup"] = {"file": "data/entity_prompts_topup.json",
                                                "sha256": sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE)}
    manifest["topup"] = {
        "after_run": TOPUP_AFTER, "kept_in_that_run": short,
        "prompts_added": {e: len(rows) for e, rows in topped_up.items()},
        "rule": "the one allowed top-up round: new prompts only for these entities, nothing removed, same checks on "
                "the merged set; the whole pipeline is re-run because the grand mean depends on which entities "
                "have probes",
    }
    manifest["deviations"].append("Top-up round: prompts were added for the entities above after seeing run "
                                  f"{TOPUP_AFTER}'s filter results for them (the plan allows one logged round).")
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(tag: str, topup: bool) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.omp import nonneg_omp

    manifest = json.loads(manifest_path(topup).read_text())
    assert manifest["data"]["entity_prompts"]["sha256"] == sha256_of(pins.ENTITY_PROMPTS_FILE), \
        "entity_prompts.json changed since the manifest"
    if topup:
        assert manifest["data"]["entity_prompts_topup"]["sha256"] == sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE), \
            "entity_prompts_topup.json changed since the manifest"
    out_dir, cache_dir = RESULTS / tag, pins.CACHE_DIR / "exp01" / tag
    out_dir.mkdir(parents=True, exist_ok=False)
    cache_dir.mkdir(parents=True, exist_ok=False)

    items, prompts = load_items(), load_entity_prompts(topup)
    entities = entities_of(items)
    model = load_model()
    lens = JLens(model)

    # 1. Filter: keep a prompt if the first word of Qwen's greedy continuation is an accepted answer.
    rows, kept_residuals = [], {e: [] for e in entities}
    for entity in entities:
        for row in prompts[entity]:
            ids = model.encode(row["prompt"])
            _, h = model.run(ids, record=PROBE_LAYERS)
            continuation = model.greedy_text(ids, GREEDY_TOKENS)
            word = first_word(continuation)
            kept = word is not None and word.lower() in {a.lower() for a in row["answers"]}
            rows.append({"entity": entity, "round": row["round"], "prompt": row["prompt"], "answers": row["answers"],
                         "greedy": continuation, "greedy_word": word, "kept": kept})
            if kept:
                kept_residuals[entity].append(torch.stack([h[l][-1] for l in PROBE_LAYERS]))  # [L, d]
        print(f"{entity}: kept {len(kept_residuals[entity])}/{len(prompts[entity])}", flush=True)
    with open(out_dir / "filter.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_kept = {e: len(kept_residuals[e]) for e in entities}
    probed = [e for e in entities if n_kept[e] >= MIN_KEPT]

    # 2. Probes: entity means minus their grand mean, per layer.
    means = torch.stack([torch.stack(kept_residuals[e]).mean(0) for e in probed])  # [E, L, d]
    probes = means - means.mean(0, keepdim=True)

    # 3. Decomposition per layer.
    letter_ids = model.letter_token_ids()
    own_tokens = {e: model.concept_token(e) for e in probed}
    jparts = torch.zeros_like(probes)
    atom_ids: dict[int, list[list[int]]] = {}
    atom_coefs: dict[int, list[list[float]]] = {}
    random_fve: dict[int, list[float]] = {}
    generator = torch.Generator(device="cuda").manual_seed(RANDOM_SEED)
    for li, layer in enumerate(PROBE_LAYERS):
        dictionary = lens.vectors(layer, letter_ids)
        atom_ids[layer], atom_coefs[layer] = [], []
        for ei in range(len(probed)):
            idx, coefs = nonneg_omp(dictionary, probes[ei, li], K_ATOMS)
            jparts[ei, li] = coefs @ dictionary[idx]
            atom_ids[layer].append(letter_ids[idx].tolist())
            atom_coefs[layer].append(coefs.tolist())
        random_fve[layer] = []
        for _ in range(len(probed)):  # chance level: the same decomposition of isotropic random directions
            x = torch.randn(probes.shape[-1], device="cuda", generator=generator)
            idx, coefs = nonneg_omp(dictionary, x, K_ATOMS)
            random_fve[layer].append(float((coefs @ dictionary[idx]).norm() ** 2 / x.norm() ** 2))
        del dictionary
        print(f"layer {layer} decomposed", flush=True)

    torch.save({"entities": probed, "layers": list(PROBE_LAYERS), "probe": probes.cpu(), "jpart": jparts.cpu(),
                "atom_ids": atom_ids, "atom_coefs": atom_coefs, "n_kept": n_kept, "tag": tag},
               cache_dir / "probes.pt")

    # 4. Summaries for the human.
    fve = (jparts.norm(dim=-1) ** 2 / probes.norm(dim=-1) ** 2).cpu()  # [E, L]
    own_in_atoms = torch.tensor([[own_tokens[e] in atom_ids[l][ei] for li, l in enumerate(PROBE_LAYERS)]
                                 for ei, e in enumerate(probed)], dtype=torch.float)
    per_layer = {l: {"fve_median": float(fve[:, li].median()),
                     "fve_q25": float(fve[:, li].quantile(0.25)), "fve_q75": float(fve[:, li].quantile(0.75)),
                     "random_fve_median": statistics.median(random_fve[l]),
                     "own_token_in_atoms": float(own_in_atoms[:, li].mean()),
                     "atoms_used_mean": statistics.mean(len(a) for a in atom_ids[l]),
                     "probe_norm_median": float(probes[:, li].norm(dim=-1).median())}
                 for li, l in enumerate(PROBE_LAYERS)}
    li = PROBE_LAYERS.index(INSPECT_LAYER)
    top_atoms = {e: [model.decoded[t] for t, _ in sorted(zip(atom_ids[INSPECT_LAYER][ei],
                                                              atom_coefs[INSPECT_LAYER][ei]),
                                                          key=lambda tc: -tc[1])[:10]]
                 for ei, e in enumerate(probed)}
    summary = {"manifest": manifest_path(topup).name, "n_prompts": len(rows), "n_kept": sum(n_kept.values()),
               "kept_per_entity": n_kept,
               "entities_without_probe": [e for e in entities if e not in probed],
               "per_layer": per_layer, f"top_atoms_layer{INSPECT_LAYER}": top_atoms}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    write_review(out_dir, rows, n_kept, prompts, per_layer, top_atoms, fve[:, li])
    print(json.dumps({k: summary[k] for k in ("n_prompts", "n_kept", "entities_without_probe")}, indent=2))


def write_review(out_dir, rows, n_kept, prompts, per_layer, top_atoms, fve_inspect) -> None:
    lines = [f"# {EXP} / {out_dir.name}: review sheet", "",
             f"Prompts kept: {sum(r['kept'] for r in rows)} of {len(rows)}.", "",
             "## Kept prompts per entity (kept / written)", ""]
    lines += [", ".join(f"{e} {n_kept[e]}/{len(prompts[e])}" for e in sorted(n_kept, key=str.lower)), ""]
    lines += [f"## Random sample of {REVIEW_SAMPLE} prompts (seed {REVIEW_SEED})", "",
              "| entity | prompt | accepted | Qwen's greedy continuation | kept |", "|---|---|---|---|---|"]
    for r in random.Random(REVIEW_SEED).sample(rows, REVIEW_SAMPLE):
        greedy = r["greedy"].replace("\n", "\\n").replace("|", "\\|")
        lines.append(f"| {r['entity']} | {r['prompt']} | {'/'.join(r['answers'])} | `{greedy}` | "
                     f"{'yes' if r['kept'] else 'no'} |")
    lines += ["", "## Every rejected prompt", ""]
    lines += [f"- {r['entity']}{' (top-up)' if r['round'] == 2 else ''}: {r['prompt']} -> `{r['greedy'].strip()}` "
              f"(accepted {'/'.join(r['answers'])})" for r in rows if not r["kept"]]
    lines += ["", "## J-part share of probe variance per layer", "",
              "| layer | median | IQR | random-direction median | own token among atoms | probe norm (median) |",
              "|---|---|---|---|---|---|"]
    for l, s in per_layer.items():
        lines.append(f"| {l} | {s['fve_median']:.3f} | {s['fve_q25']:.3f}-{s['fve_q75']:.3f} | "
                     f"{s['random_fve_median']:.3f} | {s['own_token_in_atoms']:.2f} | {s['probe_norm_median']:.1f} |")
    lines += ["", f"## Top-10 J-part atoms at layer {INSPECT_LAYER} (by coefficient)", ""]
    for (e, atoms), share in zip(top_atoms.items(), fve_inspect.tolist()):
        lines.append(f"- **{e}** (J share {share:.2f}): " + " ".join(f"`{a}`" for a in atoms))
    (out_dir / "review.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["check", "manifest", "run"])
    parser.add_argument("--tag", default=None)
    parser.add_argument("--topup", action="store_true", help="include data/entity_prompts_topup.json")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check(args.topup)
    elif args.stage == "manifest" and args.topup:
        stage_manifest_topup()
    elif args.stage == "manifest":
        stage_manifest()
    else:
        assert args.tag, "--tag is required for run"
        stage_run(args.tag, args.topup)
