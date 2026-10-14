"""exp01_probes: a bridge probe for each of the 97 entities, split into a J-space part and a remainder.

Stages (run in order), each for one --variant (see VARIANTS; default base):
  check            the variant's entity prompts against the rules in data/entity_prompts.json (tokenizer only)
  manifest         write the variant's manifest in results/exp01_probes/ before any measurement
  run --tag TAG    keep the prompts Qwen answers correctly, build the probes, decompose them. Writes
                   results/exp01_probes/TAG/ and cache/exp01/TAG/probes.pt (both write-once)
Variants: base (data/entity_prompts.json); topup (+ data/entity_prompts_topup.json, the one allowed top-up round for
the entities left with fewer than MIN_KEPT kept prompts in run TOPUP_AFTER); whiten (the topup prompts as kept in
run WHITEN_FROM, no re-filtering, whitened probes); more (+ data/entity_prompts_more/, a second round for every
entity after two failed exp02 gates); more_jpp (more's prompts and probes, decomposed over J++ instead of the J-lens;
the filter is re-run and compared prompt by prompt with run JPP_REPRODUCES).

Probe of entity e at layer l: the mean final-token residual (output of block l) over e's kept prompts, minus the mean
of those entity means over all entities. Whitened probe: that difference times the inverse of the pooled
within-entity covariance (Ledoit-Wolf shrinkage), rescaled to the difference's norm. Decomposition: non-negative OMP
with K_ATOMS atoms over the unit lens vectors (J-lens, or J++ for more_jpp) of every letter-bearing token at that layer; J-part = the fit,
remainder = probe - J-part.
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

from bridge_jspace import pins
from bridge_jspace.data import (
    check_entity_prompts,
    entities_of,
    first_word,
    load_entity_prompts,
    load_items,
    more_prompt_files,
    sha256_of,
)
from bridge_jspace.stats import ledoit_wolf

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
WHITEN_FROM = "v2"
JPP_REPRODUCES = "v3"
VARIANTS = {  # which prompt rounds a run uses, whether its probes are whitened, its lens, and its manifest
    "base": {"manifest": "manifest.json", "topup": False, "more": False, "whiten": False, "lens": "jlens"},
    "topup": {"manifest": "manifest_topup.json", "topup": True, "more": False, "whiten": False, "lens": "jlens"},
    "whiten": {"manifest": "manifest_whiten.json", "topup": True, "more": False, "whiten": True, "lens": "jlens"},
    "more": {"manifest": "manifest_more.json", "topup": True, "more": True, "whiten": False, "lens": "jlens"},
    "more_jpp": {"manifest": "manifest_more_jpp.json", "topup": True, "more": True, "whiten": False, "lens": "jpp"},
}


def manifest_path(variant: str) -> Path:
    return RESULTS / VARIANTS[variant]["manifest"]


def variant_prompts(variant: str) -> dict[str, list[dict]]:
    v = VARIANTS[variant]
    return load_entity_prompts(topup=v["topup"], more=v["more"])


def stage_check(variant: str) -> None:
    prompts, items = variant_prompts(variant), load_items()
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
        "lens": {
            "repo": pins.LENS_REPO,
            "revision": pins.LENS_REVISION,
            "file": pins.LENS_FILE,
            "vector": "v_t = (g * W_U[t]) @ J_l, unit-normalised; g = final-norm gain (1 + weight)",
        },
        "data": {
            "probe_swap": {"file": "data/probe_swap.json", "sha256": pins.PROBE_SWAP_SHA256},
            "entity_prompts": {"file": "data/entity_prompts.json", "sha256": sha256_of(pins.ENTITY_PROMPTS_FILE)},
        },
        "prompt_format": "raw text, no chat template, no special tokens added",
        "filter": f"keep a prompt if the first word of Qwen's greedy continuation ({GREEDY_TOKENS} tokens) equals "
        "an accepted answer, case-insensitively",
        "min_kept_prompts_per_entity": MIN_KEPT,
        "probe": "mean final-token residual (block output) over kept prompts minus the mean over entities",
        "probe_layers": list(PROBE_LAYERS),
        "decomposition": {
            "method": "non-negative OMP, NNLS refit each step",
            "k_atoms": K_ATOMS,
            "dictionary": "unit J-lens vectors of non-special tokens whose decode has a letter",
        },
        "metrics": [
            "kept prompts per entity",
            "fraction of probe variance in the J-part per layer",
            "chance level of that fraction: the same decomposition of isotropic random directions "
            f"(one per probed entity per layer, seed {RANDOM_SEED})",
            "whether the entity's own token is among its J-part atoms",
        ],
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
    path = manifest_path("topup")
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path("base").read_text())
    kept = json.loads((RESULTS / TOPUP_AFTER / "summary.json").read_text())["kept_per_entity"]
    short = {e: n for e, n in kept.items() if n < MIN_KEPT}
    topped_up = json.loads(pins.ENTITY_PROMPTS_TOPUP_FILE.read_text())["entities"]
    assert sorted(topped_up) == sorted(short), f"top-up entities {sorted(topped_up)} != short entities {short}"
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["data"]["entity_prompts_topup"] = {
        "file": "data/entity_prompts_topup.json",
        "sha256": sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE),
    }
    manifest["topup"] = {
        "after_run": TOPUP_AFTER,
        "kept_in_that_run": short,
        "prompts_added": {e: len(rows) for e, rows in topped_up.items()},
        "rule": "the one allowed top-up round: new prompts only for these entities, nothing removed, same checks on "
        "the merged set; the whole pipeline is re-run because the grand mean depends on which entities "
        "have probes",
    }
    manifest["deviations"].append(
        "Top-up round: prompts were added for the entities above after seeing run "
        f"{TOPUP_AFTER}'s filter results for them (the plan allows one logged round)."
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def stage_manifest_whiten() -> None:
    """The top-up manifest with the probe definition changed to the whitened probe."""
    path = manifest_path("whiten")
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path("topup").read_text())
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["probe"] = (
        "(pooled within-entity covariance of the kept prompts' residuals, Ledoit-Wolf shrinkage, per "
        "layer)^-1 @ (mean final-token residual over kept prompts - mean over entities), rescaled to "
        "the norm of that difference"
    )
    manifest["filter"] = f"none: the prompts kept in run {WHITEN_FROM} (same rule, same prompts)"
    manifest["deviations"].append(
        "Probe definition changed after the first exp02 gate failed (full-probe flips 17% < 30%; exp02_swaps/"
        "gate_debug: the entity is present at the probe position but entity labels explain only ~5-7 points of "
        "residual variance above chance, so ~6-prompt means are mostly prompt noise). Whitening was chosen by the "
        "human; the shrinkage is set analytically (Ledoit-Wolf), not tuned on the test items."
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def more_files_pinned() -> list[dict]:
    return [{"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for f in more_prompt_files()]


def stage_manifest_more() -> None:
    """The top-up manifest plus the second prompt round (every entity), with mean-difference probes."""
    path = manifest_path("more")
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path("topup").read_text())
    added = {e: len(rows) for f in more_prompt_files() for e, rows in json.loads(f.read_text())["entities"].items()}
    current = {(e, r["prompt"]) for e, rows in variant_prompts("topup").items() for r in rows}
    dropped = [
        {k: r[k] for k in ("entity", "prompt", "kept")}
        for r in map(json.loads, (RESULTS / WHITEN_FROM / "filter.jsonl").read_text().splitlines())
        if (r["entity"], r["prompt"]) not in current
    ]
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["data"]["entity_prompts"]["sha256"] = sha256_of(pins.ENTITY_PROMPTS_FILE)
    manifest["data"]["entity_prompts_more"] = more_files_pinned()
    manifest["more"] = {
        "prompts_added": added,
        "total_added": sum(added.values()),
        f"dropped_since_{WHITEN_FROM}": dropped,
        "rule": "new prompts for every entity; the merged set passes the checks in data.py, now "
        "including the name-derived-word check",
    }
    manifest["deviations"] += [
        "Second prompt round beyond the plan's one top-up: ~20 more prompts per entity, written after two failed exp02 "
        "gates (mean-difference probes 17%, whitened 8%; exp02_swaps/gate_debug*: ~6-prompt means are mostly prompt "
        "noise). Chosen by the human. Written by coding subagents, checked mechanically, not human-reviewed.",
        "New check (a stricter reading of 'never names the entity'): no prompt word or accepted answer may be built on "
        "the entity's name (first five letters, or irregular forms such as Chinese/French/nitrate; data.py). The "
        f"earlier prompts that break it are dropped (listed above; they were in runs v1-{WHITEN_FROM}), as are 18 new "
        "prompts that broke it before pinning.",
    ]
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def stage_manifest_more_jpp() -> None:
    """The more manifest with the decomposition dictionary switched to J++ (part A's second reader)."""
    path = manifest_path("more_jpp")
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path("more").read_text())
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["data"]["entity_prompts_more"] = more_files_pinned()
    manifest["lens"]["file"] = pins.JPP_FILE
    manifest["lens"]["vector"] = manifest["lens"]["vector"].replace("J_l", "J++_l")
    manifest["decomposition"]["dictionary"] = "unit J++ vectors of non-special tokens whose decode has a letter"
    manifest["reproduces"] = {
        "run": JPP_REPRODUCES,
        "check": "same prompts, filter and probe definition as that run, so the kept flags must match prompt by "
        "prompt (mismatches are counted in summary.json); only the decomposition dictionary differs",
    }
    manifest["deviations"].append(
        f"J++ decomposition: run {JPP_REPRODUCES}'s probes are rebuilt (its cache was not kept) and decomposed over "
        "J++ instead of the J-lens, so part B's J-space matches the second reader part A uses. Chosen by the human."
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def whitened_probes(kept_residuals: dict, probed: list[str], means: torch.Tensor, probes: torch.Tensor):
    """Per layer, probe_e = (shrunk pooled within-entity covariance)^-1 @ (mu_e - m), rescaled to |mu_e - m|.
    Returns (probes [E, L, d], Ledoit-Wolf shrinkage per layer)."""
    within = torch.cat([torch.stack(kept_residuals[e]) - means[i] for i, e in enumerate(probed)])  # [N, L, d]
    out, shrinkage = torch.empty_like(probes), []
    for li in range(probes.shape[1]):
        cov, a = ledoit_wolf(within[:, li])
        w = torch.linalg.solve(cov, probes[:, li].double().T).T.float()  # [E, d]
        out[:, li] = w * (probes[:, li].norm(dim=-1, keepdim=True) / w.norm(dim=-1, keepdim=True))
        shrinkage.append(a)
    return out, shrinkage


@torch.no_grad()
def stage_run(tag: str, variant: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.omp import nonneg_omp

    v = VARIANTS[variant]
    whiten = v["whiten"]
    manifest = json.loads(manifest_path(variant).read_text())
    assert manifest["data"]["entity_prompts"]["sha256"] == sha256_of(pins.ENTITY_PROMPTS_FILE), (
        "entity_prompts.json changed since the manifest"
    )
    if v["topup"]:
        assert manifest["data"]["entity_prompts_topup"]["sha256"] == sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE), (
            "entity_prompts_topup.json changed since the manifest"
        )
    if v["more"]:
        assert manifest["data"]["entity_prompts_more"] == more_files_pinned(), (
            "entity_prompts_more/ changed since the manifest"
        )
    out_dir, cache_dir = RESULTS / tag, pins.CACHE_DIR / "exp01" / tag
    out_dir.mkdir(parents=True, exist_ok=False)
    cache_dir.mkdir(parents=True, exist_ok=False)

    items, prompts = load_items(), variant_prompts(variant)
    entities = entities_of(items)
    model = load_model()
    lens = JLens(model, v["lens"])

    # 1. Filter: keep a prompt if the first word of Qwen's greedy continuation is an accepted answer (or, when
    #    whitening, take the rows of run WHITEN_FROM, whose prompts are the same).
    rows, kept_residuals = [], {e: [] for e in entities}
    if whiten:
        rows = [json.loads(line) for line in (RESULTS / WHITEN_FROM / "filter.jsonl").read_text().splitlines()]
        assert [r["prompt"] for r in rows] == [r["prompt"] for e in entities for r in prompts[e]]
        for r in rows:
            if r["kept"]:
                _, h = model.run(model.encode(r["prompt"]), record=PROBE_LAYERS)
                kept_residuals[r["entity"]].append(torch.stack([h[layer][-1] for layer in PROBE_LAYERS]))
    else:
        for entity in entities:
            for row in prompts[entity]:
                ids = model.encode(row["prompt"])
                _, h = model.run(ids, record=PROBE_LAYERS)
                continuation = model.greedy_text(ids, GREEDY_TOKENS)
                word = first_word(continuation)
                kept = word is not None and word.lower() in {a.lower() for a in row["answers"]}
                rows.append(
                    {
                        "entity": entity,
                        "round": row["round"],
                        "prompt": row["prompt"],
                        "answers": row["answers"],
                        "greedy": continuation,
                        "greedy_word": word,
                        "kept": kept,
                    }
                )
                if kept:
                    kept_residuals[entity].append(torch.stack([h[layer][-1] for layer in PROBE_LAYERS]))  # [L, d]
            print(f"{entity}: kept {len(kept_residuals[entity])}/{len(prompts[entity])}", flush=True)
    with open(out_dir / "filter.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_kept = {e: len(kept_residuals[e]) for e in entities}
    filter_mismatches = None
    if variant == "more_jpp":
        reference = {
            (r["entity"], r["prompt"]): r["kept"]
            for r in map(json.loads, (RESULTS / JPP_REPRODUCES / "filter.jsonl").read_text().splitlines())
        }
        filter_mismatches = [
            {"entity": r["entity"], "prompt": r["prompt"], "kept": r["kept"]}
            for r in rows
            if reference.get((r["entity"], r["prompt"])) != r["kept"]
        ]
        print(f"filter vs {JPP_REPRODUCES}: {len(filter_mismatches)} of {len(rows)} prompts differ", flush=True)
    probed = [e for e in entities if n_kept[e] >= MIN_KEPT]

    # 2. Probes: entity means minus their grand mean, per layer (whitened if asked).
    means = torch.stack([torch.stack(kept_residuals[e]).mean(0) for e in probed])  # [E, L, d]
    probes = means - means.mean(0, keepdim=True)
    shrinkage = None
    if whiten:
        probes, shrinkage = whitened_probes(kept_residuals, probed, means, probes)
    definition = "whitened_ledoit_wolf" if whiten else "mean_difference"

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

    torch.save(
        {
            "entities": probed,
            "layers": list(PROBE_LAYERS),
            "probe": probes.cpu(),
            "jpart": jparts.cpu(),
            "atom_ids": atom_ids,
            "atom_coefs": atom_coefs,
            "n_kept": n_kept,
            "tag": tag,
            "definition": definition,
            "lens": v["lens"],
        },
        cache_dir / "probes.pt",
    )

    # 4. Summaries for the human.
    fve = (jparts.norm(dim=-1) ** 2 / probes.norm(dim=-1) ** 2).cpu()  # [E, L]
    own_in_atoms = torch.tensor(
        [
            [own_tokens[e] in atom_ids[layer][ei] for li, layer in enumerate(PROBE_LAYERS)]
            for ei, e in enumerate(probed)
        ],
        dtype=torch.float,
    )
    per_layer = {
        layer: {
            "fve_median": float(fve[:, li].median()),
            "fve_q25": float(fve[:, li].quantile(0.25)),
            "fve_q75": float(fve[:, li].quantile(0.75)),
            "random_fve_median": statistics.median(random_fve[layer]),
            "own_token_in_atoms": float(own_in_atoms[:, li].mean()),
            "atoms_used_mean": statistics.mean(len(a) for a in atom_ids[layer]),
            "probe_norm_median": float(probes[:, li].norm(dim=-1).median()),
        }
        for li, layer in enumerate(PROBE_LAYERS)
    }
    li = PROBE_LAYERS.index(INSPECT_LAYER)
    top_atoms = {
        e: [
            model.decoded[t]
            for t, _ in sorted(
                zip(atom_ids[INSPECT_LAYER][ei], atom_coefs[INSPECT_LAYER][ei], strict=True), key=lambda tc: -tc[1]
            )[:10]
        ]
        for ei, e in enumerate(probed)
    }
    summary = {
        "manifest": manifest_path(variant).name,
        "probe_definition": definition,
        "lens": v["lens"],
        "lens_file_keys": lens.file_keys,
        **({} if filter_mismatches is None else {f"filter_mismatches_vs_{JPP_REPRODUCES}": filter_mismatches}),
        "ledoit_wolf_shrinkage": dict(zip(PROBE_LAYERS, shrinkage, strict=True)) if shrinkage else None,
        "n_prompts": len(rows),
        "n_kept": sum(n_kept.values()),
        "kept_per_entity": n_kept,
        "entities_without_probe": [e for e in entities if e not in probed],
        "per_layer": per_layer,
        f"top_atoms_layer{INSPECT_LAYER}": top_atoms,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    write_review(out_dir, rows, n_kept, prompts, per_layer, top_atoms, fve[:, li])
    print(json.dumps({k: summary[k] for k in ("n_prompts", "n_kept", "entities_without_probe")}, indent=2))


def write_review(out_dir, rows, n_kept, prompts, per_layer, top_atoms, fve_inspect) -> None:
    lines = [
        f"# {EXP} / {out_dir.name}: review sheet",
        "",
        f"Prompts kept: {sum(r['kept'] for r in rows)} of {len(rows)}.",
        "",
        "## Kept prompts per entity (kept / written)",
        "",
    ]
    lines += [", ".join(f"{e} {n_kept[e]}/{len(prompts[e])}" for e in sorted(n_kept, key=str.lower)), ""]
    lines += [
        f"## Random sample of {REVIEW_SAMPLE} prompts (seed {REVIEW_SEED})",
        "",
        "| entity | prompt | accepted | Qwen's greedy continuation | kept |",
        "|---|---|---|---|---|",
    ]
    for r in random.Random(REVIEW_SEED).sample(rows, REVIEW_SAMPLE):
        greedy = r["greedy"].replace("\n", "\\n").replace("|", "\\|")
        lines.append(
            f"| {r['entity']} | {r['prompt']} | {'/'.join(r['answers'])} | `{greedy}` | "
            f"{'yes' if r['kept'] else 'no'} |"
        )
    lines += ["", "## Every rejected prompt", ""]
    lines += [
        f"- {r['entity']}{' (top-up)' if r['round'] == 2 else ''}: {r['prompt']} -> `{r['greedy'].strip()}` "
        f"(accepted {'/'.join(r['answers'])})"
        for r in rows
        if not r["kept"]
    ]
    lines += [
        "",
        "## J-part share of probe variance per layer",
        "",
        "| layer | median | IQR | random-direction median | own token among atoms | probe norm (median) |",
        "|---|---|---|---|---|---|",
    ]
    for layer, s in per_layer.items():
        lines.append(
            f"| {layer} | {s['fve_median']:.3f} | {s['fve_q25']:.3f}-{s['fve_q75']:.3f} | "
            f"{s['random_fve_median']:.3f} | {s['own_token_in_atoms']:.2f} | {s['probe_norm_median']:.1f} |"
        )
    lines += ["", f"## Top-10 J-part atoms at layer {INSPECT_LAYER} (by coefficient)", ""]
    for (e, atoms), share in zip(top_atoms.items(), fve_inspect.tolist(), strict=True):
        lines.append(f"- **{e}** (J share {share:.2f}): " + " ".join(f"`{a}`" for a in atoms))
    (out_dir / "review.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["check", "manifest", "run"])
    parser.add_argument("--tag", default=None)
    parser.add_argument("--variant", default="base", choices=list(VARIANTS))
    args = parser.parse_args()
    manifest_writers = {
        "base": stage_manifest,
        "topup": stage_manifest_topup,
        "whiten": stage_manifest_whiten,
        "more": stage_manifest_more,
        "more_jpp": stage_manifest_more_jpp,
    }
    if args.stage == "check":
        stage_check(args.variant)
    elif args.stage == "manifest":
        manifest_writers[args.variant]()
    else:
        assert args.tag, "--tag is required for run"
        stage_run(args.tag, args.variant)
