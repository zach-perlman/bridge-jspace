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
the filter is re-run and compared prompt by prompt with run JPP_REPRODUCES); more_jpp_chat (more_jpp's prompts, probe
definition and dictionary in the chat format, README Decisions 2026-10-19: each entity prompt a fill-in-the-blank user
turn, thinking off, "Answer:" prefilled, bridge_jspace.chat; the residual at the prefill's ":", where the model is about
to name the answer, as the raw prompts' last token was).

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

from bridge_jspace import chat, pins
from bridge_jspace.data import (
    check_entity_prompts,
    entities_of,
    first_word,
    load_entity_prompts,
    load_items,
    more_prompt_files,
    sha256_of,
)
from bridge_jspace.run_switches import check_switches, switches
from bridge_jspace.stats import ledoit_wolf

EXP = "exp01_probes"
RESULTS = pins.RESULTS_DIR / EXP
# The union of the candidate bands that exp02 sweeps: 16-48 of Qwen3.6-27B's 64 blocks; another target gets the same
# quarter-to-three-quarters of its depth (Gemma 4 31B-it: 15-45 of 60).
PROBE_LAYERS = (
    tuple(range(16, 49))
    if pins.TARGET == "qwen3.6-27b"
    else tuple(range(pins.N_LAYERS // 4, 3 * pins.N_LAYERS // 4 + 1))
)
K_ATOMS = 25
MIN_KEPT = 3
GREEDY_TOKENS = 8
REVIEW_SEED = 0
REVIEW_SAMPLE = 25
INSPECT_LAYER = pins.N_LAYERS // 2  # 32 on Qwen3.6-27B
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
    "more_jpp_chat": {
        "manifest": "manifest_more_jpp_chat.json",
        "topup": True,
        "more": True,
        "whiten": False,
        "lens": "jpp",
        "format": "chat_prefill",
    },
    # The same, the residual at the statement's last token inside the user turn (before " ___") instead of the
    # prefill's ':': exp02's chat gate failed with more_jpp_chat's probes (full probe 8%) while the lens's own vectors
    # flipped 59-62%, so the probe's position (the assistant turn vs the question's tokens) is the first suspect.
    "more_jpp_chat_stmt": {
        "manifest": "manifest_more_jpp_chat_stmt.json",
        "topup": True,
        "more": True,
        "whiten": False,
        "lens": "jpp",
        "format": "chat_prefill",
        "position": "statement_end",
    },
    # Another target (pins.TARGET): every prompt round at once, self-contained (no cross-run references to Qwen's runs),
    # over J++ (as more_jpp) or the J-lens.
    "all_jpp": {"manifest": "manifest_all_jpp.json", "topup": True, "more": True, "whiten": False, "lens": "jpp"},
    "all_jlens": {"manifest": "manifest_all_jlens.json", "topup": True, "more": True, "whiten": False, "lens": "jlens"},
}
QWEN_ONLY = ("base", "topup", "whiten", "more", "more_jpp", "more_jpp_chat", "more_jpp_chat_stmt")
CHAT_BATCH = 64  # more_jpp_chat: filter continuations generated for this many prompts of one token length at a time  # their manifests chain Qwen runs v1-v3


def manifest_path(variant: str) -> Path:
    return RESULTS / (pins.RUN_PREFIX + VARIANTS[variant]["manifest"])


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
        "model": pins.model_pin(),
        "switches": switches(),
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
    manifest["switches"] = switches()
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
    manifest["switches"] = switches()
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
    manifest["switches"] = switches()
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
    manifest["switches"] = switches()
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


def stage_manifest_more_jpp_chat(variant: str = "more_jpp_chat") -> None:
    """more_jpp's prompts, probe definition and J++ dictionary, in the chat format."""
    path = manifest_path(variant)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = json.loads(manifest_path("more_jpp").read_text())
    manifest.pop("reproduces", None)
    manifest["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["switches"] = switches()
    manifest["variant"] = variant
    manifest["data"]["entity_prompts"]["sha256"] = sha256_of(pins.ENTITY_PROMPTS_FILE)
    manifest["data"]["entity_prompts_topup"]["sha256"] = sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE)
    manifest["data"]["entity_prompts_more"] = more_files_pinned()
    manifest["prompt_format"] = (
        "the chat template, one user turn, thinking off, assistant prefilled 'Answer:': "
        f"'{chat.BLANK_INSTRUCTION}', a blank line, the prompt without 'Fact: ' and ' ___' (bridge_jspace.chat)"
    )
    manifest["filter"] = (
        f"keep a prompt if the first word of the model's greedy continuation after 'Answer:' ({GREEDY_TOKENS} tokens) "
        f"equals an accepted answer, case-insensitively; continuations generated {CHAT_BATCH} prompts of one token "
        "length at a time (Model.generate_batch, no edits)"
    )
    manifest["probe"] = (
        "mean residual (block output) at the prompt's last token, the prefill's ':' (where the model is about to name "
        "the answer, as the raw prompts' last token was), over kept prompts, minus the mean over entities"
    )
    if VARIANTS[variant].get("position") == "statement_end":
        manifest["probe"] = (
            "mean residual (block output) at the statement's last token inside the user turn (the token before ' ___'), "
            "over kept prompts, minus the mean over entities"
        )
        manifest["deviations"].append(
            "Probe position: the statement's last token in the user turn, not the prefill's ':'. exp02's chat gate "
            "(gate_chat_v1) failed with more_jpp_chat's probes (full probe 1-8% at every band) while the lens's own "
            "vectors flipped 45-62%; the probe built in the assistant turn is the first suspect. Chosen by the agent "
            "under Zach's overnight approval (2026-10-19), as the gate rule's 'debug' step."
        )
    manifest["deviations"].append(
        "Chat format (Zach, 2026-10-19; README Decisions): new part B runs use the chat template with 'Answer:' "
        "prefilled, so exp02 and exp09 re-run in it need probes from the same format. Same prompts, probe definition "
        "and J++ dictionary as more_jpp; the filter is re-run in this format (kept prompts may differ)."
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def chat_filter(model, entities: list[str], prompts: dict, position: str = "prefill") -> tuple[list[dict], dict]:
    """more_jpp_chat's filter: every entity prompt rendered in the chat format, continuations generated in batches of
    one token length, and for each kept prompt the residual at its last token (the prefill's ':')."""
    from bridge_jspace.tokens import raw_encoding

    todo, where = [], []
    for entity in entities:
        for row in prompts[entity]:
            text = chat.chat_text(model.tokenizer, chat.blank_content(row["prompt"]))
            enc = raw_encoding(model.tokenizer, text, offsets=True)
            todo.append((entity, row, torch.tensor([enc["input_ids"]], device="cuda")))
            blank = text.index(" ___")  # statement_end: the last token that ends before the blank
            where.append(
                -1 if position == "prefill" else max(i for i, (_, e) in enumerate(enc["offset_mapping"]) if e <= blank)
            )
    by_len: dict[int, list[int]] = {}
    for i, (_, _, ids) in enumerate(todo):
        by_len.setdefault(ids.shape[1], []).append(i)
    texts: list[str] = [""] * len(todo)
    for group in by_len.values():
        for start in range(0, len(group), CHAT_BATCH):
            chunk = group[start : start + CHAT_BATCH]
            batch = torch.cat([todo[i][2] for i in chunk])
            for i, text in zip(chunk, model.generate_batch(batch, GREEDY_TOKENS, [{}] * len(chunk)), strict=True):
                texts[i] = text
    rows, kept_residuals = [], {e: [] for e in entities}
    for (entity, row, ids), continuation, pos in zip(todo, texts, where, strict=True):
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
            _, h = model.run(ids, record=PROBE_LAYERS)
            kept_residuals[entity].append(torch.stack([h[layer][pos] for layer in PROBE_LAYERS]))  # [L, d]
    for entity in entities:
        print(f"{entity}: kept {len(kept_residuals[entity])}/{len(prompts[entity])}", flush=True)
    return rows, kept_residuals


def stage_manifest_all(variant: str) -> None:
    """One self-contained manifest for every prompt round (base, top-up, more) on the target model."""
    path = manifest_path(variant)
    assert not path.exists(), f"{path} exists; manifests are written once"
    lens = VARIANTS[variant]["lens"]
    manifest = {
        "exp": EXP,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "variant": variant,
        "question": "Build a bridge probe per entity and measure how much of it the lens dictionary explains.",
        "model": pins.model_pin(),
        "switches": switches(),
        "lens": {
            "name": lens,
            "source": list(pins.LENS_SOURCES[lens]),
            "vector": "v_t = (g * W_U[t]) @ J_l, unit-normalised; g = the final norm's gain (pins.TARGETS)",
        },
        "data": {
            "probe_swap": {"file": "data/probe_swap.json", "sha256": pins.PROBE_SWAP_SHA256},
            "entity_prompts": {"file": "data/entity_prompts.json", "sha256": sha256_of(pins.ENTITY_PROMPTS_FILE)},
            "entity_prompts_topup": {
                "file": str(pins.ENTITY_PROMPTS_TOPUP_FILE.relative_to(pins.REPO_ROOT)),
                "sha256": sha256_of(pins.ENTITY_PROMPTS_TOPUP_FILE),
            },
            "entity_prompts_more": more_files_pinned(),
        },
        "prompt_format": "raw text, no chat template; the target's BOS first if it needs one (tokens.raw_encoding)",
        "filter": f"keep a prompt if the first word of the model's greedy continuation ({GREEDY_TOKENS} tokens) equals "
        "an accepted answer, case-insensitively",
        "min_kept_prompts_per_entity": MIN_KEPT,
        "probe": "mean final-token residual (block output) over kept prompts minus the mean over entities",
        "probe_layers": list(PROBE_LAYERS),
        "decomposition": {
            "method": "non-negative OMP, NNLS refit each step",
            "k_atoms": K_ATOMS,
            "dictionary": f"unit {lens} vectors of non-special tokens whose decode has a letter",
        },
        "metrics": [
            "kept prompts per entity",
            "fraction of probe variance in the J-part per layer",
            f"chance level of that fraction: isotropic random directions (one per probed entity per layer, seed "
            f"{RANDOM_SEED})",
            "whether the entity's own token is among its J-part atoms",
        ],
        "review": {"seed": REVIEW_SEED, "sample_size": REVIEW_SAMPLE, "inspect_layer": INSPECT_LAYER},
        "deviations": [
            "All prompt rounds at once: on Qwen the top-up and more rounds were added after runs v1 and v2 (see "
            "manifest_topup.json, manifest_more.json); here every round's prompts are filtered on this model in one run.",
            f"Probe layers {PROBE_LAYERS[0]}-{PROBE_LAYERS[-1]}: the same share of the depth as Qwen's 16-48.",
        ],
    }
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

    v = VARIANTS[variant]
    whiten = v["whiten"]
    manifest = json.loads(manifest_path(variant).read_text())
    check_switches(manifest)
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
    elif v.get("format") == "chat_prefill":
        rows, kept_residuals = chat_filter(model, entities, prompts, v.get("position", "prefill"))
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
    own_tokens = {e: model.concept_token(e) for e in probed}
    jparts, atom_ids, atom_coefs, random_fve = decompose(model, lens, probes)

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
    fve, per_layer, top_atoms = layer_summaries(
        model, probed, own_tokens, probes, jparts, atom_ids, atom_coefs, random_fve
    )
    li = PROBE_LAYERS.index(INSPECT_LAYER)
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


@torch.no_grad()
def decompose(model, lens, probes: torch.Tensor):
    """Non-negative OMP of every probe [E, L, d] over the lens's unit vectors of letter-bearing tokens, per layer, and
    the same decomposition of isotropic random directions (chance level). Returns (J-parts [E, L, d], atom ids and
    coefficients per layer, random-direction FVE per layer)."""
    from bridge_jspace.omp import nonneg_omp

    letter_ids = model.letter_token_ids()
    jparts = torch.zeros_like(probes)
    atom_ids: dict[int, list[list[int]]] = {}
    atom_coefs: dict[int, list[list[float]]] = {}
    random_fve: dict[int, list[float]] = {}
    generator = torch.Generator(device="cuda").manual_seed(RANDOM_SEED)
    for li, layer in enumerate(PROBE_LAYERS):
        dictionary = lens.vectors(layer, letter_ids)
        atom_ids[layer], atom_coefs[layer] = [], []
        for ei in range(probes.shape[0]):
            idx, coefs = nonneg_omp(dictionary, probes[ei, li], K_ATOMS)
            jparts[ei, li] = coefs @ dictionary[idx]
            atom_ids[layer].append(letter_ids[idx].tolist())
            atom_coefs[layer].append(coefs.tolist())
        random_fve[layer] = []
        for _ in range(probes.shape[0]):  # chance level: the same decomposition of isotropic random directions
            x = torch.randn(probes.shape[-1], device="cuda", generator=generator)
            idx, coefs = nonneg_omp(dictionary, x, K_ATOMS)
            random_fve[layer].append(float((coefs @ dictionary[idx]).norm() ** 2 / x.norm() ** 2))
        del dictionary
        print(f"layer {layer} decomposed", flush=True)
    return jparts, atom_ids, atom_coefs, random_fve


def layer_summaries(model, probed, own_tokens, probes, jparts, atom_ids, atom_coefs, random_fve):
    """Per-entity J-part share [E, L], per-layer summary, and the top-10 atoms at INSPECT_LAYER per entity."""
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
    top_atoms = {
        e: [
            model.decoded[t]
            for t, _ in sorted(
                zip(atom_ids[INSPECT_LAYER][ei], atom_coefs[INSPECT_LAYER][ei], strict=True), key=lambda tc: -tc[1]
            )[:10]
        ]
        for ei, e in enumerate(probed)
    }
    return fve, per_layer, top_atoms


def redecompose_manifest_path(tag: str) -> Path:
    return RESULTS / f"manifest_{tag}.json"


def stage_manifest_redecompose(tag: str, source: str, lens: str, deviation: str | None = None) -> None:
    """Manifest for re-decomposing run `source`'s cached probes over another lens (no new probes, no filter)."""
    path = redecompose_manifest_path(tag)
    assert not path.exists(), f"{path} exists; manifests are written once"
    probes = pins.CACHE_DIR / "exp01" / source / "probes.pt"
    manifest = {
        "exp": EXP,
        "kind": "redecompose",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "switches": switches(),
        "question": f"Run {source}'s probes, decomposed over the {lens} dictionary instead of its own lens.",
        "probes_from": {"run": source, "file": str(probes.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(probes)},
        "lens": {"name": lens, "source": list(pins.LENS_SOURCES[lens])},
        "decomposition": {
            "method": "non-negative OMP, NNLS refit each step",
            "k_atoms": K_ATOMS,
            "dictionary": f"unit {lens} vectors of non-special tokens whose decode has a letter",
        },
        "deviations": [
            deviation
            or (
                f"Probes are {source}'s, unchanged, so the two lenses' decompositions differ only in the lens. Run "
                f"{source} did not reproduce v3's filter exactly on this box (see its summary), so v3 cannot be "
                "paired with it. Chosen by the human."
            ),
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_redecompose(tag: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    manifest = json.loads(redecompose_manifest_path(tag).read_text())
    check_switches(manifest)
    source = manifest["probes_from"]
    probes_path = pins.REPO_ROOT / source["file"]
    assert sha256_of(probes_path) == source["sha256"], "the source probes changed since the manifest"
    out_dir, cache_dir = RESULTS / tag, pins.CACHE_DIR / "exp01" / tag
    out_dir.mkdir(parents=True, exist_ok=False)
    cache_dir.mkdir(parents=True, exist_ok=False)
    blob = torch.load(probes_path, map_location="cpu", weights_only=True)
    assert blob["layers"] == list(PROBE_LAYERS), "source probes were built on other layers"
    model = load_model()
    lens = JLens(model, manifest["lens"]["name"])
    probes, probed = blob["probe"].cuda(), blob["entities"]
    jparts, atom_ids, atom_coefs, random_fve = decompose(model, lens, probes)
    torch.save(
        {
            **blob,
            "jpart": jparts.cpu(),
            "atom_ids": atom_ids,
            "atom_coefs": atom_coefs,
            "tag": tag,
            "lens": manifest["lens"]["name"],
            "probes_from": source["run"],
        },
        cache_dir / "probes.pt",
    )
    own_tokens = {e: model.concept_token(e) for e in probed}
    _, per_layer, top_atoms = layer_summaries(
        model, probed, own_tokens, probes, jparts, atom_ids, atom_coefs, random_fve
    )
    summary = {
        "manifest": redecompose_manifest_path(tag).name,
        "probes_from": source["run"],
        "probe_definition": blob.get("definition", "mean_difference"),
        "lens": manifest["lens"]["name"],
        "lens_file_keys": lens.file_keys,
        "n_kept": sum(blob["n_kept"].values()),
        "kept_per_entity": blob["n_kept"],
        "per_layer": per_layer,
        f"top_atoms_layer{INSPECT_LAYER}": top_atoms,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    shown = [
        layer
        for layer in PROBE_LAYERS
        if layer in (INSPECT_LAYER, PROBE_LAYERS[len(PROBE_LAYERS) * 3 // 4], PROBE_LAYERS[-1])
    ]
    print(json.dumps({layer: round(per_layer[layer]["fve_median"], 3) for layer in shown}))


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
    parser.add_argument("stage", choices=["check", "manifest", "run", "manifest-redecompose", "redecompose"])
    parser.add_argument("--tag", default=None)
    parser.add_argument("--from", dest="source", help="manifest-redecompose: the exp01 run whose probes to reuse")
    parser.add_argument(
        "--lens", choices=list(pins.LENS_SOURCES), help="manifest-redecompose: the lens to decompose over"
    )
    parser.add_argument(
        "--deviation", default=None, help="manifest-redecompose: the deviation note (default: v3_jlens's)"
    )
    parser.add_argument("--variant", default="base", choices=list(VARIANTS))
    args = parser.parse_args()
    manifest_writers = {
        "base": stage_manifest,
        "topup": stage_manifest_topup,
        "whiten": stage_manifest_whiten,
        "more": stage_manifest_more,
        "more_jpp": stage_manifest_more_jpp,
        "more_jpp_chat": stage_manifest_more_jpp_chat,
        "more_jpp_chat_stmt": lambda: stage_manifest_more_jpp_chat("more_jpp_chat_stmt"),
        "all_jpp": lambda: stage_manifest_all("all_jpp"),
        "all_jlens": lambda: stage_manifest_all("all_jlens"),
    }
    assert pins.TARGET == "qwen3.6-27b" or args.variant not in QWEN_ONLY, (
        f"{args.variant} chains Qwen's runs; on {pins.TARGET} use all_jpp or all_jlens"
    )
    if args.tag:
        pins.check_run_name(args.tag)
    if args.stage == "check":
        stage_check(args.variant)
    elif args.stage == "manifest-redecompose":
        assert args.tag, "manifest-redecompose needs --tag"
        assert args.source, "manifest-redecompose needs --from"
        assert args.lens, "manifest-redecompose needs --lens"
        stage_manifest_redecompose(args.tag, args.source, args.lens, args.deviation)
    elif args.stage == "redecompose":
        assert args.tag, "--tag is required for redecompose"
        stage_redecompose(args.tag)
    elif args.stage == "manifest":
        manifest_writers[args.variant]()
    else:
        assert args.tag, "--tag is required for run"
        stage_run(args.tag, args.variant)
