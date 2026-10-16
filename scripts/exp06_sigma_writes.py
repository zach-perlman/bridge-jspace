"""exp06_sigma_writes: read with the lens, write along the activation covariance? Two cheap tests of Σ-aware writes.

A lens vector v is a gradient; by Stein's lemma it is roughly a whitened, LDA-like direction, Σ^-1 Cov(h, logit). The
smallest edit that moves <v, h> by a given amount, measured in units of how much activations normally vary
(Mahalanobis), moves along Σv, not v. Our swaps and steering read and write with v. Two tests:

  matched  exp02's matched-alignment control again, with the random part drawn from the activation covariance,
           N(0, Σ_l), instead of isotropically (exp02 matched_v4: J-part 52%, isotropic completion 14% with J++).
           If the covariance-shaped completion flips like the J-part, the matched control's gap measured how natural
           the direction is, not the lens's direction; if it flips like the isotropic one, the lens's direction
           matters. The J-part and isotropic rows rerun matched_v4 and must match it item for item.
  steer    exp03's fresh-item start-line steering (layers 8-24, 3% and 5% of the residual norm) along
           unit(Σ_λ (v_S' - v_S)), Σ_λ = (1 - λ) Σ + λ (tr Σ / d) I, for λ in LAMBDAS. λ = 1 is exp03's steering;
           every λ adds the same Euclidean size.

Σ_l: the covariance of layer l's block output over the first N_POSITIONS token positions of WikiText-103's test split
(data/wikitext103_test.json, non-empty rows joined by newlines) in WINDOW-token windows, position 0 of each window
left out (the attention sink).

Stages (Σ is cached and not committed; the manifest is written before the run and is write-once):
  sigma
  manifest --name N --why "..."
  run N
"""

import argparse
import json
import statistics
import sys
import time
import zlib
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import load_items, sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts.exp02_swaps import Probes, condition_atoms, prepare, swap
from scripts.exp03_brew_swaps import (
    ITEM_SETS,
    MAX_NEW_TOKENS,
    AddDirection,
    answer_colour,
    regime_positions,
    render,
    spans,
    start_target,
    swap_target,
    write_jsonl,
)

EXP = "exp06_sigma_writes"
RESULTS = pins.RESULTS_DIR / EXP
SIGMA_FILE = pins.CACHE_DIR / "exp06" / "sigma.pt"
SWAP_LAYERS, STEER_LAYERS = tuple(range(24, 41)), tuple(range(8, 25))
SIGMA_LAYERS = tuple(sorted({*SWAP_LAYERS, *STEER_LAYERS}))
N_POSITIONS, WINDOW = 100_000, 512
LENSES = ("jpp", "jlens")
CONDITIONS = ("jpart", "jpart_matched", "jpart_matched_sigma")
LAMBDAS = (1.0, 0.5, 0.1, 0.0)
SCALES = (0.03, 0.05)
NULL_SEED = 0
N_BOOT, BOOT_SEED = 2000, 0
MATCHED_V4 = {lens: pins.RESULTS_DIR / "exp02_swaps" / f"matched_v4_{lens}" for lens in LENSES}
FRESH_STEER = pins.RESULTS_DIR / "exp03_brew_swaps" / "fresh_steer" / "outcomes.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


@torch.no_grad()
def stage_sigma(layers: tuple[int, ...] = SIGMA_LAYERS, path: Path = SIGMA_FILE) -> None:
    """Σ_l at `layers`, cached at `path` (exp07 reuses this at its own layers)."""
    from bridge_jspace.model import load_model

    assert not path.exists(), f"{path} exists; delete it to re-estimate"
    model = load_model()
    tokenizer: Any = model.tokenizer
    ids = tokenizer("\n".join(r for r in pins.wikitext_rows() if r.strip()), add_special_tokens=False).input_ids
    # A target that needs a BOS (Gemma) gets it first in every window, then WINDOW - 1 text tokens; position 0 (the BOS
    # here, the first text token on Qwen, whose windows are unchanged) is left out below either way.
    bos = [tokenizer.bos_token_id] if pins.TARGETS[pins.TARGET]["bos"] else []
    step = WINDOW - len(bos)
    windows = [bos + ids[i : i + step] for i in range(0, len(ids) - step + 1, step)]
    n_windows = -(-N_POSITIONS // (WINDOW - 1))
    assert len(windows) >= n_windows, f"{len(windows)} windows, need {n_windows}"
    sums: dict[int, torch.Tensor] = {}
    outer: dict[int, torch.Tensor] = {}
    n = 0
    for w in windows[:n_windows]:
        _, rec = model.run(torch.tensor([w], device="cuda"), record=layers)
        for layer in layers:
            x = rec[layer][1:].double()  # position 0 left out
            if layer not in sums:
                sums[layer] = torch.zeros(x.shape[1], dtype=torch.float64, device="cuda")
                outer[layer] = torch.zeros(x.shape[1], x.shape[1], dtype=torch.float64, device="cuda")
            sums[layer] += x.sum(0)
            outer[layer] += x.T @ x
        n += len(w) - 1
    mean = {layer: sums[layer] / n for layer in layers}
    cov = {layer: (outer[layer] / n - torch.outer(mean[layer], mean[layer])).float().cpu() for layer in layers}
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "layers": list(layers),
            "n_positions": n,
            "window": WINDOW,
            "data": {"file": str(pins.WIKITEXT_FILE.relative_to(pins.REPO_ROOT)), "sha256": pins.WIKITEXT_SHA256},
            "mean": {layer: m.float().cpu() for layer, m in mean.items()},
            "cov": cov,
        },
        path,
    )
    traces = [float(cov[layer].trace()) for layer in layers]
    print(f"wrote {path}: {n} positions, {len(layers)} layers, trace {min(traces):.3g}-{max(traces):.3g}")


class Sigma:
    """The cached covariances, on the GPU: Σ_λ products and N(0, Σ) draws per layer."""

    def __init__(self, path: Path = SIGMA_FILE):
        blob = torch.load(path, map_location="cpu", weights_only=True)
        self.n_positions = blob["n_positions"]
        self.cov = {layer: c.to("cuda", torch.float64) for layer, c in blob["cov"].items()}
        self._root: dict[int, torch.Tensor] = {}

    def apply(self, layer: int, u: torch.Tensor, lam: float) -> torch.Tensor:
        """Σ_λ u with Σ_λ = (1 - λ) Σ + λ (tr Σ / d) I (fp32)."""
        c = self.cov[layer]
        iso = float(c.trace()) / c.shape[0]
        return ((1 - lam) * (c @ u.double()) + lam * iso * u.double()).float()

    def draw(self, layer: int, generator: torch.Generator) -> torch.Tensor:
        """One draw from N(0, Σ_l) (fp32): U sqrt(max(e, 0)) z for Σ_l = U diag(e) U^T."""
        if layer not in self._root:
            e, u = torch.linalg.eigh(self.cov[layer])
            self._root[layer] = u * e.clamp(min=0).sqrt()
        root = self._root[layer]
        z = torch.randn(root.shape[1], device=root.device, dtype=torch.float64, generator=generator)
        return (root @ z).float()


def matched_sigma(probes: Probes, sigma: Sigma, entity: str, layer: int) -> torch.Tensor:
    """exp02's matched direction (the J-part's cosine to the probe), with the rest drawn from N(0, Σ_l) instead of
    isotropically, seeded by entity and layer."""
    probe = probes.unit("full_probe", entity, layer)
    cos = float(probes.unit("jpart", entity, layer) @ probe)
    g = torch.Generator(device="cuda").manual_seed(zlib.crc32(f"sigma:{entity}:{layer}".encode()))
    r = sigma.draw(layer, g)
    r = r - (r @ probe) * probe
    return cos * probe + (1 - cos**2) ** 0.5 * r / r.norm()


def stage_manifest(name: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    blob = torch.load(SIGMA_FILE, map_location="cpu", weights_only=True)
    fresh_file, fresh_sha, _ = ITEM_SETS["fresh"]
    probes = {lens: pins.CACHE_DIR / "exp01" / f"v3_{lens}" / "probes.pt" for lens in LENSES}
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "sigma_writes",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Do edits shaped by the activation covariance (Σv) act more than the lens's own directions (v)?",
        "why": why,
        "model": pins.model_pin(),
        "lenses": {lens: list(pins.LENS_SOURCES[lens]) for lens in LENSES},
        "sigma": {
            "file": str(SIGMA_FILE.relative_to(pins.REPO_ROOT)),
            "sha256": sha256_of(SIGMA_FILE),
            "n_positions": blob["n_positions"],
            "window": blob["window"],
            "layers": blob["layers"],
            "data": blob["data"],
            "estimate": "population covariance of block outputs over positions 1.. of each window",
        },
        "matched": {
            "items": "exp02's probe_swap items, eligible as in matched_v4 (stripped prompts, criterion C)",
            "probes": {
                lens: {"file": str(p.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(p)} for lens, p in probes.items()
            },
            "conditions": list(CONDITIONS),
            "layers": f"{SWAP_LAYERS[0]}-{SWAP_LAYERS[-1]}",
            "jpart_matched_sigma": "per entity and layer: the J-part's cosine to the probe, the rest a seeded draw from "
            "N(0, Σ_l) projected orthogonal to the probe",
            "nulls": "each condition's matched-norm random-direction null, as exp02",
        },
        "steer": {
            "items": {"file": str(fresh_file.relative_to(pins.REPO_ROOT)), "sha256": fresh_sha},
            "eligibility": "as exp03's fresh_steer: answered correctly, with exp03's X and S'",
            "direction": "unit(Σ_λ,l (v_S' - v_S)) per layer, v unit lens vectors; Σ_λ = (1 - λ) Σ + λ (tr Σ / d) I",
            "lambdas": list(LAMBDAS),
            "scales": list(SCALES),
            "layers": f"{STEER_LAYERS[0]}-{STEER_LAYERS[-1]}",
            "nulls": "one seeded random direction per lens and scale, at the same size",
        },
        "decision": {
            "matched": "fixed before the run: if jpart - jpart_matched_sigma's paired CI includes 0, the matched-control "
            "gap is attributed to how natural the direction is; if jpart_matched_sigma - jpart_matched's CI includes 0 "
            "and jpart - jpart_matched_sigma's is above 0, to the lens's direction; otherwise reported as mixed. J++ "
            "primary, J-lens secondary",
            "steer": "Σ-aware writing helps if, for J++ at 3% (the primary dose), some λ < 1 reaches f(f(S')) more often "
            "than λ = 1 (paired bootstrap CI above 0); 5% and the J-lens are secondary",
            "reproduce": "jpart and jpart_matched must match matched_v4, and λ = 1 must match exp03 fresh_steer, item for "
            "item (reported, not fixed)",
        },
        "deviations": [
            "Σ comes from WikiText, not from the items' own prompts: it describes generic text, as the lens's Jacobians do.",
            "At λ < 1 the same Euclidean size moves the lens readings less; the test asks whether the shape of the "
            "edit matters more than its reading.",
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
    assert sha256_of(SIGMA_FILE) == manifest["sigma"]["sha256"], "Σ changed since the manifest"
    model = load_model()
    sigma = Sigma()
    item_rows, outcomes = [], []
    for lens_name in LENSES:
        lens = JLens(model, lens_name)
        probe_info = manifest["matched"]["probes"][lens_name]
        assert sha256_of(pins.REPO_ROOT / probe_info["file"]) == probe_info["sha256"], "probes changed"
        probes = Probes(pins.REPO_ROOT / probe_info["file"])
        run_matched(model, lens, lens_name, probes, sigma, item_rows, outcomes)
        run_steer(model, lens, lens_name, sigma, item_rows, outcomes)
    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = summarize(outcomes)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def run_matched(model, lens, lens_name, probes, sigma, item_rows, outcomes) -> None:
    for index, item in enumerate(load_items()):
        row, prepared = prepare(model, probes, item, list(SWAP_LAYERS), "greedy_c", "stripped")
        item_rows.append({"task": "matched", "lens": lens_name, **row})
        if row["status"] != "eligible":
            continue
        assert prepared is not None
        ids, clean_h, answer_ids, swap_ids = prepared
        for ci, condition in enumerate(CONDITIONS):
            if condition == "jpart_matched_sigma":
                pair = (item["intermediate"], item["swap_to"])
                atoms = {
                    layer: torch.stack([matched_sigma(probes, sigma, e, layer) for e in pair]) for layer in SWAP_LAYERS
                }
            else:
                atoms = {layer: condition_atoms(condition, item, layer, probes, lens, model) for layer in SWAP_LAYERS}
            for null in (False, True):
                seed = NULL_SEED + 1000 * index + ci if null else None
                result = swap(model, ids, clean_h, atoms, item, answer_ids, swap_ids, seed, "greedy_c")
                outcomes.append(
                    {
                        "task": "matched",
                        "lens": lens_name,
                        "name": item["name"],
                        "condition": condition,
                        "null": null,
                        **result,
                    }
                )
        print(f"matched {lens_name} {item['name']}: done", flush=True)


def run_steer(model, lens, lens_name, sigma, item_rows, outcomes) -> None:
    items = ITEM_SETS["fresh"][2]()
    palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
    tokenizer: Any = model.tokenizer
    for index, item in enumerate(items):
        f, start, answer = item["table"], item["start"], item["answer"]
        text = render(tokenizer, item["prompt"])
        enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
        ids = torch.tensor([enc.input_ids], device="cuda")
        _, clean_text, _ = model.generate(ids, MAX_NEW_TOKENS)
        s2 = start_target(item, index)
        targets = s2 is not None and swap_target(item, index) is not None
        ok = answer_colour(clean_text, palette) == answer
        status = "eligible" if ok and targets else "clean_wrong" if targets else "no_target"
        item_rows.append({"task": "steer", "lens": lens_name, "name": item["name"], "status": status})
        if status != "eligible":
            continue
        assert s2 is not None
        predicted = f[f[s2]["stir"]]["stir"]
        positions = regime_positions("start_line", [tuple(o) for o in enc.offset_mapping], spans(item, text))
        tok = torch.tensor([model.concept_token(start), model.concept_token(s2)], device="cuda")
        plain = {}
        for layer in STEER_LAYERS:
            atoms = lens.vectors(layer, tok)
            plain[layer] = torch.nn.functional.normalize(atoms[1] - atoms[0], dim=0)
        runs: list[tuple[float | None, dict[int, torch.Tensor]]] = []
        for lam in LAMBDAS:
            runs.append(
                (
                    lam,
                    {
                        layer: torch.nn.functional.normalize(sigma.apply(layer, u, lam), dim=0)
                        for layer, u in plain.items()
                    },
                )
            )
        for si, scale in enumerate(SCALES):
            g = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1000 * index + si)
            null = {
                layer: torch.nn.functional.normalize(torch.randn(u.shape[0], device="cuda", generator=g), dim=0)
                for layer, u in plain.items()
            }
            for lam, directions in [*runs, (None, null)]:
                edits = {layer: AddDirection(d, scale, positions) for layer, d in directions.items()}
                _, out_text, _ = model.generate(ids, MAX_NEW_TOKENS, edits)
                colour = answer_colour(out_text, palette)
                cos = statistics.median(float(directions[layer] @ plain[layer]) for layer in STEER_LAYERS)
                outcomes.append(
                    {
                        "task": "steer",
                        "lens": lens_name,
                        "name": item["name"],
                        "lam": lam,
                        "null": lam is None,
                        "scale": scale,
                        "continuation": out_text,
                        "colour": colour,
                        "predicted": predicted,
                        "flip": colour == predicted,
                        "kept_clean": colour == answer,
                        "cos_to_plain_median": round(cos, 4),
                    }
                )
        print(f"steer {lens_name} {item['name']}: done", flush=True)


def pick(outcomes: list[dict], **where) -> dict[str, bool]:
    """{item: flip} over outcomes matching every key=value."""
    return {o["name"]: o["flip"] for o in outcomes if all(o.get(k) == v for k, v in where.items())}


def summarize(outcomes: list[dict]) -> dict:
    rows, diffs, reproduce = [], {}, {}
    for lens in LENSES:
        for condition in CONDITIONS:
            for null in (False, True):
                f = pick(outcomes, task="matched", lens=lens, condition=condition, null=null)
                rows.append(
                    {
                        "task": "matched",
                        "lens": lens,
                        "condition": condition,
                        "null": null,
                        "n": len(f),
                        "flip": wilson(sum(f.values()), len(f)),
                    }
                )
        jp, iso, sig = (pick(outcomes, task="matched", lens=lens, condition=c, null=False) for c in CONDITIONS)
        names = sorted(jp)
        diffs[f"matched {lens}: jpart - matched_sigma"] = paired_bootstrap_diff(
            [jp[n] for n in names], [sig[n] for n in names], N_BOOT, BOOT_SEED
        )
        diffs[f"matched {lens}: matched_sigma - matched"] = paired_bootstrap_diff(
            [sig[n] for n in names], [iso[n] for n in names], N_BOOT, BOOT_SEED
        )
        before = read_jsonl(MATCHED_V4[lens] / "outcomes.jsonl")
        for c in CONDITIONS[:2]:
            old = {o["name"]: o["flip"] for o in before if o["condition"] == c and not o["null"]}
            new = pick(outcomes, task="matched", lens=lens, condition=c, null=False)
            both = [n for n in new if n in old]
            reproduce[f"matched {lens} {c}"] = {"items": len(both), "match": sum(old[n] == new[n] for n in both)}
        fresh = read_jsonl(FRESH_STEER)
        for scale in SCALES:
            base = pick(outcomes, task="steer", lens=lens, lam=1.0, scale=scale)
            for lam in (*LAMBDAS, None):
                f = pick(outcomes, task="steer", lens=lens, lam=lam, scale=scale)
                rows.append(
                    {
                        "task": "steer",
                        "lens": lens,
                        "lam": lam,
                        "null": lam is None,
                        "scale": scale,
                        "n": len(f),
                        "flip": wilson(sum(f.values()), len(f)),
                    }
                )
                if lam is not None and lam != 1.0:
                    names = sorted(set(f) & set(base))
                    diffs[f"steer {lens} {scale}: lambda {lam} - lambda 1"] = paired_bootstrap_diff(
                        [f[n] for n in names], [base[n] for n in names], N_BOOT, BOOT_SEED
                    )
            old = {o["name"]: o["flip"] for o in fresh if o["lens"] == lens and o["scale"] == scale and not o["null"]}
            both = [n for n in base if n in old]
            reproduce[f"steer {lens} {scale} lambda 1"] = {
                "items": len(both),
                "match": sum(old[n] == base[n] for n in both),
            }
    return {"rates": rows, "paired_bootstraps": diffs, "reproduce": reproduce}


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pct = lambda w: f"{100 * w[0]:.0f}% [{100 * w[1]:.0f}, {100 * w[2]:.0f}]"  # noqa: E731
    lines = [
        f"# {EXP} / {run}",
        "",
        "| task | lens | condition / λ | scale | null | n | flip [95% CI] |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in summary["rates"]:
        what = r.get("condition") or ("" if r.get("lam") is None else f"λ={r['lam']}")
        lines.append(
            f"| {r['task']} | {r['lens']} | {what} | {r.get('scale') or ''} | {'yes' if r['null'] else ''} | {r['n']} | {pct(r['flip'])} |"
        )
    lines += ["", "Paired bootstrap differences in flip rate:"]
    lines += [
        f"- {k}: {100 * v[0]:+.0f} pts [{100 * v[1]:+.0f}, {100 * v[2]:+.0f}]"
        for k, v in summary["paired_bootstraps"].items()
    ]
    lines += ["", "Reproduction of earlier runs (items whose flip matches):"]
    lines += [f"- {k}: {v['match']}/{v['items']}" for k, v in summary["reproduce"].items()]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["sigma", "manifest", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument("--why", help="manifest: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "sigma":
        stage_sigma()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
