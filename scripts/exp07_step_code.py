"""exp07_step_code: does a code for brew's intermediate, fit on other items, write the step where the lens does not?

exp04 found brew's intermediate carried after the start line at layers 36-50 (its window): copying the counterfactual
C's activations there (C: the start colour's rule gives X instead of I) makes the model answer f(X), on the bank and on
fresh items, and the copy's J-space part does nothing. exp03's steering along the lens direction v_X - v_I at the same
positions and layers gave X itself, never f(X). This run fits a linear code for the intermediate colour at the window
on other items and writes with it, next to the lens direction and the lens direction reshaped by the activation
covariance Σ (exp06's idea: read along v, write along Σv).

  code    brew_fit's items that the model answers (none is a test item): at each window layer and each position after
          the start line, a ridge least-squares fit of the block output on one-hot codes of the start colour S, the
          intermediate I and the answer A, with an intercept. Row E_I[k] is the code of intermediate colour k;
          E_I[X] - E_I[I] moves an item's intermediate from I to X with S and A held fixed.
  edits   at one window layer at a time, at every position after the start line, as exp04's copy:
            copy                    δ = h_C - h_B, exp04's copy (positive control; reproduces exp04's full rows)
            code                    E_I[X] - E_I[I]
            random                  a seeded random direction per position
            lens                    v_X - v_I, the unit lens vectors of the two colours (exp03's direction)
            sigma_0.5, sigma_0.0    Σ_λ (v_X - v_I), Σ_λ = (1 - λ) Σ + λ (tr Σ / d) I, Σ from WikiText as in exp06
            code_jspace, code_rest  the code's 25-atom signed OMP part over the lens's letter-token vectors, and the rest
          lens, sigma and the code's parts with J++ (primary) and the J-lens.
  dose    "copy" (primary): each edit as large as exp04's copy at that layer (total norm over the positions); the code
          keeps its own spread over the positions, the directions without one (lens, sigma, random) take the copy's,
          and the code's parts are parts of the scaled code. "code": code at its own size, random at the code's norms.
Items: exp04's eligible fresh items (primary) and bank items (replication); the answer is read as in exp04. Per item,
an edit's step score is the share of window layers at which it makes the model answer f(X).

Stages (the manifest is written first and is write-once; the caches are not committed):
  check                           tokenizer only: the same tokens after the start line in every fit and test item
  manifest --name N --why "..."
  fit                             the code, from brew_fit (cache/exp07/code.pt)
  sigma                           Σ at the window layers (cache/exp07/sigma.pt), exp06's estimate
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
    render,
    spans,
    write_jsonl,
)
from scripts.exp03_make_items import PALETTE
from scripts.exp04_brew_parts import K_ATOMS, AddRows, signed_omp
from scripts.exp04_brew_patch import SOURCES, category, prepare
from scripts.exp06_sigma_writes import Sigma, stage_sigma

EXP = "exp07_step_code"
RESULTS = pins.RESULTS_DIR / EXP
CODE_FILE = pins.CACHE_DIR / "exp07" / "code.pt"
SIGMA_FILE = pins.CACHE_DIR / "exp07" / "sigma.pt"
EXP04 = pins.RESULTS_DIR / "exp04_brew_patch"
WINDOW = tuple(range(36, 51, 2))  # exp04's window after the start line (patch_map and patch_map_fresh agree)
MAPS = ("patch_map", "patch_map_fresh")
PARTS_RUNS = {"fresh": "parts_window_fresh", "bank": "parts_window"}  # exp04's full copies, for the reproduction
TEST_SETS = ("fresh", "bank")
COLOURS = PALETTE
RIDGE = 1.0
LENSES = ("jpp", "jlens")
LAMBDAS = (0.5, 0.0)
NULL_SEED = 0
CHANCE_DRAWS = 20
N_BOOT, BOOT_SEED = 2000, 0

COPY = {"direction": "copy", "dose": "copy", "lens": None}
CODE = {"direction": "code", "dose": "copy", "lens": None}
RANDOM = {"direction": "random", "dose": "copy", "lens": None}
CODE_OWN = {"direction": "code", "dose": "code", "lens": None}
RANDOM_OWN = {"direction": "random", "dose": "code", "lens": None}


def lens_edit(direction: str, lens: str) -> dict:
    return {"direction": direction, "dose": "copy", "lens": lens}


def design_row(start: str, inter: str, answer: str) -> torch.Tensor:
    """x = [1, onehot(S), onehot(I), onehot(A)] over COLOURS (fp64)."""
    k = len(COLOURS)
    x = torch.zeros(1 + 3 * k, dtype=torch.float64)
    x[0] = 1.0
    for block, colour in enumerate((start, inter, answer)):
        x[1 + block * k + COLOURS.index(colour)] = 1.0
    return x


def solve_code(xtx: torch.Tensor, xty: torch.Tensor, ridge: float) -> torch.Tensor:
    """Ridge least squares from running sums: W = (X^T X + ridge D)^-1 X^T Y [f, ...], D the identity without the
    intercept. The one-hot blocks are identified only up to shifts the intercept absorbs; the penalty makes each
    block's rows sum to zero."""
    penalty = torch.full((xtx.shape[0],), ridge, dtype=xtx.dtype, device=xtx.device)
    penalty[0] = 0.0
    flat = torch.linalg.solve(xtx + torch.diag(penalty), xty.reshape(xty.shape[0], -1))
    return flat.reshape(xty.shape)


class CodeFit:
    """Running X^T X and X^T Y for the per-layer, per-position ridge fit of activations on design_row."""

    def __init__(self, layers: tuple[int, ...], n_positions: int, d: int, device: str = "cuda"):
        f = 1 + 3 * len(COLOURS)
        self.xtx = torch.zeros(f, f, dtype=torch.float64, device=device)
        self.xty = {layer: torch.zeros(f, n_positions, d, dtype=torch.float64, device=device) for layer in layers}
        self.n = 0

    def add(self, start: str, inter: str, answer: str, h: dict[int, torch.Tensor]) -> None:
        """h: {layer: [P, d]} for one item."""
        x = design_row(start, inter, answer).to(self.xtx.device)
        self.xtx += torch.outer(x, x)
        for layer, rows in h.items():
            for j in x.nonzero().flatten().tolist():
                self.xty[layer][j] += rows.double()
        self.n += 1

    def solve(self, ridge: float) -> dict[int, torch.Tensor]:
        return {layer: solve_code(self.xtx, xty, ridge) for layer, xty in self.xty.items()}


def code_of(w: torch.Tensor, colour: str) -> torch.Tensor:
    """E_I[colour] [P, d] from one layer's coefficients w [f, P, d]."""
    return w[1 + len(COLOURS) + COLOURS.index(colour)]


def decode_intermediate(w: torch.Tensor, h: torch.Tensor, start: str, answer: str) -> str:
    """The intermediate colour whose fitted activation, given the item's S and A, is nearest h [P, d] (squared error
    summed over positions): whether the code reads the intermediate on held-out items."""
    k = len(COLOURS)
    base = w[0] + w[1 + COLOURS.index(start)] + w[1 + 2 * k + COLOURS.index(answer)]
    err = ((h - base)[None] - w[1 + k : 1 + 2 * k]).pow(2).sum(dim=(1, 2))
    return COLOURS[int(err.argmin())]


def scaled(direction: torch.Tensor, norms: torch.Tensor) -> torch.Tensor:
    """direction [P, d] (or one [d] for every position), each row rescaled to norms [P]."""
    rows = direction.expand(len(norms), -1) if direction.dim() == 1 else direction
    return torch.nn.functional.normalize(rows.float(), dim=-1) * norms[:, None]


def resized(edit: torch.Tensor, like: torch.Tensor) -> torch.Tensor:
    """edit [P, d] times one factor, to the total norm of like [P, d] (its spread over positions kept)."""
    return edit.float() * (like.norm() / edit.norm())


def median_cos(a: torch.Tensor, b: torch.Tensor) -> float:
    """Median over positions of the cosine between rows of a [P, d] and b ([P, d] or [d])."""
    b = b.expand_as(a) if b.dim() == 1 else b
    return statistics.median(torch.nn.functional.cosine_similarity(a.float(), b.float(), dim=-1).tolist())


def tokenized(tokenizer, item: dict) -> tuple[list[int], list[int]]:
    """The rendered prompt's token ids and the positions after the start line (as exp04)."""
    text = render(tokenizer, item["prompt"])
    enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    return enc.input_ids, regime_positions("after_start", [tuple(o) for o in enc.offset_mapping], spans(item, text))


def stage_check() -> None:
    from bridge_jspace.tokens import load_tokenizer

    tokenizer = load_tokenizer()
    seen: dict[tuple[int, ...], dict[str, int]] = {}
    outside = 0
    for set_name, items in (("fit", pins.brew_fit_items()), *((s, ITEM_SETS[s][2]()) for s in TEST_SETS)):
        for item in items:
            ids, positions = tokenized(tokenizer, item)
            after = tuple(ids[p] for p in positions)
            seen.setdefault(after, {}).setdefault(set_name, 0)
            seen[after][set_name] += 1
            outside += any(c not in COLOURS for c in item["table"])
    for ids, counts in seen.items():
        print(f"{len(ids)} tokens after the start line: {counts} -> {tokenizer.decode(list(ids))!r}")
    print(f"items with a colour outside the fit's palette: {outside}")


def stage_manifest(name: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    maps = {}
    for run in MAPS:
        summary = EXP04 / run / "summary.json"
        window = json.loads(summary.read_text())["decision"]["windows"]["after_start"]
        assert tuple(window) == WINDOW, f"{run}'s window {window} is not {WINDOW}"
        maps[run] = {"summary_sha256": sha256_of(summary), "window_after_start": window}
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "step_code",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "At exp04's window (after the start line, layers 36-50), does a linear code for the intermediate "
        "colour, fit on other items, make the model take X as the step (answer f(X)) where the lens direction v_X - v_I "
        "does not? Does reshaping the lens direction by the activation covariance (Σv) do it?",
        "why": why,
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "window": {"layers": list(WINDOW), "positions": "after_start (everything after the start line)", "maps": maps},
        "fit": {
            "items": {"file": str(pins.BREW_FIT_FILE.relative_to(pins.REPO_ROOT)), "sha256": pins.BREW_FIT_SHA256},
            "gate": "the model's greedy answer is A (exp03's reading)",
            "model": f"per window layer and position after the start line, ridge least squares (ridge {RIDGE}, "
            "intercept not penalised) of the block output on one-hot codes of S, I and A over the 12-colour palette",
            "code": "E_I[k], the coefficient row of intermediate colour k (each one-hot block's rows sum to zero)",
        },
        "sigma": "the WikiText-103 test covariance of block outputs at the window layers, estimated as exp06's "
        "(100,000 positions, 512-token windows, position 0 left out)",
        "test_items": {
            s: {"file": str(ITEM_SETS[s][0].relative_to(pins.REPO_ROOT)), "sha256": ITEM_SETS[s][1]} for s in TEST_SETS
        },
        "eligibility": "as exp04 (B answers A, C answers c, O answers A; C and O token-aligned with B), with the same "
        "tokens after the start line as the fit items",
        "lenses": {lens: pins.LENS_FILES[lens] for lens in LENSES},
        "edits": {
            "copy": "δ = h_C - h_B (exp04's copy), at the copy dose by definition",
            "code": "E_I[X] - E_I[I], per position",
            "random": "a seeded Gaussian direction per position",
            "lens": "v_X - v_I (unit lens vectors of the colours' concept tokens), the same at every position",
            "sigma_λ": "Σ_λ (v_X - v_I), Σ_λ = (1 - λ) Σ + λ (tr Σ / d) I, λ in " + str(list(LAMBDAS)),
            "code_jspace": f"the copy-dosed code's {K_ATOMS}-atom signed OMP approximation over the lens's unit "
            "vectors of letter-bearing tokens",
            "code_rest": "the copy-dosed code minus code_jspace",
        },
        "dose": {
            "copy": "primary: each edit as large as the copy δ at that layer (total norm over the positions after the "
            "start line). code is rescaled by one factor, keeping its own spread over the positions; lens, sigma_λ and "
            "random take δ's norm at each position; code_jspace and code_rest are parts of the rescaled code",
            "code": "code at its own size; random at the code's norm at each position",
        },
        "layers": "each window layer on its own",
        "outcome": "the edited continuation's first palette colour as a role (b = f(X), X, I, A, ...), as exp04",
        "decision": {
            "step_score": "per item, the share of window layers at which the edit gives f(X); differences are paired "
            "bootstraps over items (95%)",
            "gate": "the run is interpreted only if, on the fresh items, copy's step score exceeds random's (copy dose)",
            "code": "primary, fresh items, copy dose: the code writes the step if code - random is above 0; it writes "
            "where the lens direction does not if code - lens (J++) is above 0 as well",
            "sigma": "secondary: Σ-shaping helps if sigma_λ - lens is above 0 for λ = 0.5 or 0 (J++; the J-lens alike)",
            "code_parts": "secondary, exp04's rule with random as the null: the code's step is outside the J-space if "
            "code_rest - code_jspace is above 0 and code_jspace - random is not; inside if code_jspace - code_rest is "
            "above 0 and code_rest - random is not; otherwise both or neither",
            "code_own_size": "secondary: the code at its own size writes the step if code - random (code dose) is above 0",
            "replication": "the same comparisons on the bank items, reported",
            "reproduce": "copy must reproduce exp04's full-copy rows (parts_window_fresh, parts_window) item for item "
            "(reported)",
        },
        "diagnostics": [
            "read: on each test item's own activations, the intermediate decoded from the fit (given S and A), per "
            "layer; chance 1/12",
            "the median cosine of the code to the lens direction and to each Σ_λ lens direction",
            "the share of the code's squared norm in its J-space part, and of a random direction's (chance)",
            "the code's norm over the copy's, per position",
        ],
        "deviations": [
            "The code is an average over items with S and A held fixed; exp04's copy is item-specific. At the copy "
            "dose the code is rescaled to the copy's size, which can be far from its own (both doses are run).",
            f"Σ comes from WikiText at the window layers (exp06 estimated 8-40); λ = {LAMBDAS[0]} and {LAMBDAS[1]} only.",
            "Each window layer is edited on its own, as in exp04.",
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_fit() -> None:
    from bridge_jspace.model import load_model

    assert not CODE_FILE.exists(), f"{CODE_FILE} exists; delete it to refit"
    model = load_model()
    tokenizer: Any = model.tokenizer
    fit, reference, used, wrong = None, None, [], []
    for item in pins.brew_fit_items():
        ids_list, positions = tokenized(tokenizer, item)
        after = [ids_list[p] for p in positions]
        reference = reference or after
        assert after == reference, f"{item['name']}: the tokens after the start line differ (see `check`)"
        ids = torch.tensor([ids_list], device="cuda")
        if answer_colour(model.generate(ids, MAX_NEW_TOKENS)[1], list(COLOURS)) != item["answer"]:
            wrong.append(item["name"])
            continue
        _, rec = model.run(ids, record=WINDOW)
        fit = fit or CodeFit(WINDOW, len(positions), rec[WINDOW[0]].shape[1])
        fit.add(item["start"], item["intermediates"][0], item["answer"], {lay: rec[lay][positions] for lay in WINDOW})
        used.append(item["name"])
    assert fit is not None
    w = fit.solve(RIDGE)
    CODE_FILE.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "layers": list(WINDOW),
            "colours": list(COLOURS),
            "ridge": RIDGE,
            "suffix_ids": reference,
            "items": {
                "file": str(pins.BREW_FIT_FILE.relative_to(pins.REPO_ROOT)),
                "sha256": pins.BREW_FIT_SHA256,
                "used": used,
                "wrong": wrong,
            },
            "w": {layer: w[layer].float().cpu() for layer in WINDOW},
        },
        CODE_FILE,
    )
    print(f"wrote {CODE_FILE}: fit on {len(used)} items ({len(wrong)} answered wrongly, left out)")


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    for run, info in manifest["window"]["maps"].items():
        assert sha256_of(EXP04 / run / "summary.json") == info["summary_sha256"], f"{run} changed since the manifest"
    code = torch.load(CODE_FILE, map_location="cpu", weights_only=True)
    assert code["items"]["sha256"] == manifest["fit"]["items"]["sha256"], "the code was fit on other items"
    assert code["layers"] == list(WINDOW), "the code was fit at other layers"
    assert code["ridge"] == RIDGE, "the code was fit with another ridge"
    model = load_model()
    tokenizer: Any = model.tokenizer
    sigma = Sigma(SIGMA_FILE)
    w = {layer: code["w"][layer].to("cuda") for layer in WINDOW}
    cases, item_rows, reads, diagnostics = [], [], [], []
    # Phase 1: the eligible test items (as exp04), their copies δ and their own reading of the code.
    for set_name in TEST_SETS:
        item_file, _, load_items = ITEM_SETS[set_name]
        assert sha256_of(item_file) == manifest["test_items"][set_name]["sha256"], f"{set_name} items changed"
        items = load_items()
        palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
        for index, item in enumerate(items):
            prep = prepare(item, index, tokenizer)
            row: dict[str, Any] = {"set": set_name, "name": item["name"], "status": prep["status"]}
            item_rows.append(row)
            if prep["status"] != "ok":
                continue
            cfs, roles = prep["cfs"], prep["cfs"]["roles"]
            positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
            if [prep["ids"][p] for p in positions] != code["suffix_ids"]:
                row["status"] = "suffix_differs"
                continue
            if any(roles[r] not in COLOURS for r in ("S", "I", "A", "X")):
                row["status"] = "colour_outside_fit"
                continue
            ids = torch.tensor([prep["ids"]], device="cuda")
            source_ids = {s: torch.tensor([prep["sources"][s]["ids"]], device="cuda") for s in SOURCES}
            colours = {"clean": answer_colour(model.generate(ids, MAX_NEW_TOKENS)[1], palette)}
            for s in SOURCES:
                colours[s] = answer_colour(model.generate(source_ids[s], MAX_NEW_TOKENS)[1], palette)
            ok = colours == {"clean": roles["A"], "cf": cfs["cf"]["answer"], "off": cfs["off"]["answer"]}
            row["status"] = "eligible" if ok else "not_eligible"
            if not ok:
                continue
            _, clean_h = model.run(ids, record=WINDOW)
            _, cf_h = model.run(source_ids["cf"], record=WINDOW)
            for layer in WINDOW:
                decoded = decode_intermediate(w[layer], clean_h[layer][positions], roles["S"], roles["A"])
                reads.append(
                    {"set": set_name, "name": item["name"], "layer": layer, "decoded": decoded, "I": roles["I"]}
                )
            cases.append(
                {
                    "set": set_name,
                    "index": index,
                    "name": item["name"],
                    "ids": ids,
                    "roles": roles,
                    "positions": positions,
                    "palette": palette,
                    "delta": {layer: cf_h[layer][positions] - clean_h[layer][positions] for layer in WINDOW},
                    "h_norm": {layer: clean_h[layer][positions].norm(dim=-1) for layer in WINDOW},
                }
            )
            del clean_h, cf_h
    print(f"{len(cases)} eligible items", flush=True)

    outcomes: list[dict] = []

    def run_edit(case: dict, layer: int, delta: torch.Tensor, **tags) -> None:
        _, text, _ = model.generate(case["ids"], MAX_NEW_TOKENS, {layer: AddRows(delta, case["positions"])})
        colour = answer_colour(text, case["palette"])
        outcomes.append(
            {
                "set": case["set"],
                "name": case["name"],
                "layer": layer,
                **tags,
                "continuation": text,
                "colour": colour,
                "role": category(colour, case["roles"]),
                "edit_ratio": round(float((delta.norm(dim=-1) / case["h_norm"][layer]).mean()), 4),
            }
        )

    def code_edit(case: dict, layer: int) -> torch.Tensor:
        return code_of(w[layer], case["roles"]["X"]) - code_of(w[layer], case["roles"]["I"])

    # Phase 2: the lens-free edits.
    for case in cases:
        for layer in WINDOW:
            delta, edit = case["delta"][layer], code_edit(case, layer)
            seed = NULL_SEED + 1_000_000 * TEST_SETS.index(case["set"]) + 1000 * case["index"] + layer
            noise = torch.randn(edit.shape, device="cuda", generator=torch.Generator(device="cuda").manual_seed(seed))
            run_edit(case, layer, delta, **COPY)
            run_edit(case, layer, resized(edit, delta), **CODE)
            run_edit(case, layer, scaled(noise, delta.norm(dim=-1)), **RANDOM)
            run_edit(case, layer, edit, **CODE_OWN)
            run_edit(case, layer, scaled(noise, edit.norm(dim=-1)), **RANDOM_OWN)
            ratio = float(edit.norm() / delta.norm())
            tags = {"set": case["set"], "name": case["name"], "layer": layer, "lens": None}
            diagnostics.append({**tags, "what": "code norm over copy norm", "value": round(ratio, 4)})
        print(f"lens-free {case['name']}: done ({len(outcomes)} outcomes)", flush=True)

    # Phase 3: per lens, its direction, the Σ-shaped directions and the code's J-space part and rest.
    for lens_name in LENSES:
        lens = JLens(model, lens_name)
        colour_tok = torch.tensor([model.concept_token(c) for c in COLOURS], device="cuda")
        letter_ids = model.letter_token_ids()
        colour_v = {layer: lens.vectors(layer, colour_tok) for layer in WINDOW}
        dictionaries = {layer: lens.vectors(layer, letter_ids) for layer in WINDOW}
        g = torch.Generator(device="cuda").manual_seed(BOOT_SEED)
        for layer in WINDOW:
            x = torch.randn(CHANCE_DRAWS, dictionaries[layer].shape[1], device="cuda", generator=g)
            share = (signed_omp(dictionaries[layer], x, K_ATOMS).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
            diagnostics.append({"lens": lens_name, "layer": layer, "what": "chance", "value": round(float(share), 4)})
        for case in cases:
            ii, xi = COLOURS.index(case["roles"]["I"]), COLOURS.index(case["roles"]["X"])
            for layer in WINDOW:
                delta, edit = case["delta"][layer], code_edit(case, layer)
                size = delta.norm(dim=-1)
                u = colour_v[layer][xi] - colour_v[layer][ii]
                shaped = {lam: sigma.apply(layer, u, lam) for lam in LAMBDAS}
                dosed = resized(edit, delta)
                jspace = signed_omp(dictionaries[layer], dosed, K_ATOMS)
                run_edit(case, layer, scaled(u, size), **lens_edit("lens", lens_name))
                for lam, direction in shaped.items():
                    run_edit(case, layer, scaled(direction, size), **lens_edit(f"sigma_{lam}", lens_name))
                run_edit(case, layer, jspace, **lens_edit("code_jspace", lens_name))
                run_edit(case, layer, dosed - jspace, **lens_edit("code_rest", lens_name))
                tags = {"set": case["set"], "name": case["name"], "layer": layer, "lens": lens_name}
                diagnostics.append({**tags, "what": "cos code~lens", "value": round(median_cos(edit, u), 4)})
                for lam, direction in shaped.items():
                    cos = median_cos(edit, direction)
                    diagnostics.append({**tags, "what": f"cos code~sigma_{lam}", "value": round(cos, 4)})
                share = float(jspace.norm() ** 2 / dosed.norm() ** 2)
                diagnostics.append({**tags, "what": "code jspace share", "value": round(share, 4)})
            print(f"{lens_name} {case['name']}: done ({len(outcomes)} outcomes)", flush=True)
        del dictionaries, colour_v, lens
        torch.cuda.empty_cache()

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "reads.jsonl", reads)
    write_jsonl(out_dir / "diagnostics.jsonl", diagnostics)
    summary = summarize(outcomes, reads, diagnostics)
    summary["items"] = {
        s: {
            status: sum(r["status"] == status for r in item_rows if r["set"] == s)
            for status in {r["status"] for r in item_rows}
        }
        for s in TEST_SETS
    }
    summary["caches"] = {
        "code": {
            "sha256": sha256_of(CODE_FILE),
            "fit_items_used": len(code["items"]["used"]),
            "fit_items_wrong": len(code["items"]["wrong"]),
        },
        "sigma": {"sha256": sha256_of(SIGMA_FILE), "n_positions": sigma.n_positions},
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def step_scores(outcomes: list[dict], **where) -> dict[str, float]:
    """Per item, the share of window layers at which the matching edits give f(X)."""
    hits: dict[str, list[bool]] = {}
    for o in outcomes:
        if all(o.get(k) == v for k, v in where.items()):
            hits.setdefault(o["name"], []).append(o["role"] == "b")
    return {n: sum(v) / len(v) for n, v in hits.items()}


def edits_run() -> list[dict]:
    """Every edit as an outcome filter, lens-free first."""
    out = [COPY, CODE, RANDOM, CODE_OWN, RANDOM_OWN]
    for lens in LENSES:
        out += [lens_edit(d, lens) for d in ("lens", *(f"sigma_{lam}" for lam in LAMBDAS), "code_jspace", "code_rest")]
    return out


def label(edit: dict) -> str:
    own = " (own size)" if edit["dose"] == "code" else ""
    return f"{edit['lens'] + ' ' if edit['lens'] else ''}{edit['direction']}{own}"


def summarize(outcomes: list[dict], reads: list[dict], diagnostics: list[dict]) -> dict:
    per_set: dict[str, Any] = {}
    for set_name in TEST_SETS:
        rows = [o for o in outcomes if o["set"] == set_name]
        if not rows:
            continue
        scores = {label(e): step_scores(rows, **e) for e in edits_run()}

        def diff(a: dict, b: dict, scores=scores) -> tuple[float, float, float]:
            sa, sb = scores[label(a)], scores[label(b)]
            names = sorted(set(sa) & set(sb))
            return paired_bootstrap_diff([sa[n] for n in names], [sb[n] for n in names], N_BOOT, BOOT_SEED)

        comparisons = {"copy - random": diff(COPY, RANDOM), "code - random": diff(CODE, RANDOM)}
        verdicts: dict[str, Any] = {"interpreted": comparisons["copy - random"][1] > 0}
        for lens in LENSES:
            comparisons[f"code - {lens} lens"] = diff(CODE, lens_edit("lens", lens))
            for lam in LAMBDAS:
                comparisons[f"{lens} sigma_{lam} - {lens} lens"] = diff(
                    lens_edit(f"sigma_{lam}", lens), lens_edit("lens", lens)
                )
            jspace, rest = lens_edit("code_jspace", lens), lens_edit("code_rest", lens)
            parts = {
                "rest - jspace": diff(rest, jspace),
                "jspace - random": diff(jspace, RANDOM),
                "rest - random": diff(rest, RANDOM),
            }
            comparisons.update({f"{lens} code {k}": v for k, v in parts.items()})
            verdict = "both or neither"
            if parts["rest - jspace"][1] > 0 and parts["jspace - random"][1] <= 0:
                verdict = "outside"
            elif parts["rest - jspace"][2] < 0 and parts["rest - random"][1] <= 0:
                verdict = "inside"
            verdicts[f"{lens} code parts"] = verdict
            verdicts[f"{lens} sigma helps"] = any(
                comparisons[f"{lens} sigma_{lam} - {lens} lens"][1] > 0 for lam in LAMBDAS
            )
        comparisons["code - random (own size)"] = diff(CODE_OWN, RANDOM_OWN)
        verdicts["code writes the step"] = comparisons["code - random"][1] > 0
        verdicts["code writes where the J++ lens does not"] = (
            verdicts["code writes the step"] and comparisons["code - jpp lens"][1] > 0
        )
        verdicts["code at its own size writes the step"] = comparisons["code - random (own size)"][1] > 0
        collateral = {}
        for e in edits_run():
            cells = [o for o in rows if all(o.get(k) == v for k, v in e.items())]
            collateral[label(e)] = {r: sum(o["role"] == r for o in cells) / len(cells) for r in ("A", "b", "X", "I")}
        by_layer = []
        for e in edits_run():
            for layer in WINDOW:
                cells = [o for o in rows if o["layer"] == layer and all(o.get(k) == v for k, v in e.items())]
                n = len(cells)
                by_layer.append(
                    {
                        "edit": label(e),
                        "layer": layer,
                        "n": n,
                        **{r: wilson(sum(o["role"] == r for o in cells), n) for r in ("A", "b", "X", "I")},
                        "edit_ratio_median": statistics.median(o["edit_ratio"] for o in cells),
                    }
                )
        before = {}
        with open(EXP04 / PARTS_RUNS[set_name] / "outcomes.jsonl") as f:
            for line in f:
                o = json.loads(line)
                if o["part"] == "full" and o["source"] == "cf":
                    before[o["name"], o["layer"]] = o["role"]
        now = {(o["name"], o["layer"]): o["role"] for o in rows if o["direction"] == "copy"}
        both = [k for k in now if k in before]
        set_reads = [r for r in reads if r["set"] == set_name]
        per_set[set_name] = {
            "n": len({o["name"] for o in rows}),
            "step_scores": {k: statistics.mean(v.values()) for k, v in scores.items()},
            "comparisons": comparisons,
            "verdicts": verdicts,
            "collateral": collateral,
            "by_layer": by_layer,
            "read_accuracy": {
                layer: statistics.mean(r["decoded"] == r["I"] for r in set_reads if r["layer"] == layer)
                for layer in WINDOW
            },
            "reproduce_copy": {"cells": len(both), "match": sum(before[k] == now[k] for k in both)},
        }
    values: dict[str, list[float]] = {}
    for d in diagnostics:
        values.setdefault(f"{d['lens'] + ' ' if d['lens'] else ''}{d['what']}", []).append(d["value"])
    return {"sets": per_set, "diagnostics_median": {k: statistics.median(v) for k, v in values.items()}}


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {run}", ""]
    lines += [f"Items ({s}): " + ", ".join(f"{k} {v}" for k, v in c.items() if v) for s, c in summary["items"].items()]
    lines += [f"Caches: {json.dumps(summary['caches'])}", ""]
    for set_name, s in summary["sets"].items():
        lines += [f"## {set_name} items (n={s['n']})", ""]
        lines += [
            f"Copy reproduces exp04's full rows: {s['reproduce_copy']['match']}/{s['reproduce_copy']['cells']}",
            "Read accuracy of the code (intermediate decoded on the items' own activations, chance 8%): "
            + ", ".join(f"L{layer} {100 * a:.0f}%" for layer, a in s["read_accuracy"].items()),
            "",
            "| edit | step score | A kept | X | I |",
            "|---|---|---|---|---|",
        ]
        for k, v in s["step_scores"].items():
            c = s["collateral"][k]
            lines.append(f"| {k} | {100 * v:.0f}% | {100 * c['A']:.0f}% | {100 * c['X']:.0f}% | {100 * c['I']:.0f}% |")
        lines += ["", "Paired differences in step score (pts, 95% CI):"]
        lines += [f"- {k}: {pts(v)}" for k, v in s["comparisons"].items()]
        lines += ["", "Verdicts (rules in the manifest):"]
        lines += [f"- {k}: {v}" for k, v in s["verdicts"].items()]
        lines += [""]
    lines += ["Diagnostics (medians over items, layers and positions):"]
    lines += [f"- {k}: {v:.3f}" for k, v in summary["diagnostics_median"].items()]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["check", "manifest", "fit", "sigma", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument("--why", help="manifest: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    elif args.stage == "fit":
        stage_fit()
    elif args.stage == "sigma":
        stage_sigma(WINDOW, SIGMA_FILE)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
