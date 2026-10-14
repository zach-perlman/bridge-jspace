"""exp03_brew_swaps: swap the intermediate of an in-context two-step lookup and see whether the answer follows the table.

Items: WorkspaceBench's brew_intermediates bank (data/brew_intermediates.json): a ten-row colour table given in the
prompt, two stirs, the start colour last, gated on Qwen3.6-27B. The answer is f(f(start)) and the intermediate is
I = f(start); nothing about it is known before the prompt. Swapping I's lens direction for another colour X's predicts
a specific answer, f(X), read straight off the table: a flip means the model's answer becomes f(X).

Stages (manifests are written before the runs; both are write-once):
  manifest sweep [--name N]                band sweep: raw lens vectors at every position, both lenses, no nulls
  run N
  manifest main --band A-B --sweep S [--name N]
                                           every position regime, both lenses, matched-norm nulls, and the
                                           off-path control, on the band sweep S picked
  run N

Render: Qwen's chat template (no thinking) with the prefill "Answer:", as the bank was gated. Positions are the
rendered prompt's tokens; the regime decides which ones are edited (position 0 never is):
  all          every position
  rules        the rule table's lines
  stir_line    "You stir the potion twice." (before the start colour: nothing can be computed yet)
  start_line   "The potion starts out <start>."
  after_start  everything after the start line (the question, the chat scaffolding, "Answer:")
  last         the final token (the prefilled colon)
Conditions: the swap of I with X (atoms: the lens vectors of their colour tokens), its matched-norm null (as exp02),
and the off-path control: the swap of two colours off the item's trajectory, which predicts no change.
"""

import argparse
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.clamp import SwapClamp, near_parallel
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson

EXP = "exp03_brew_swaps"
RESULTS = pins.RESULTS_DIR / EXP
LENSES = ("jlens", "jpp")
SWEEP_BANDS = ("16-32", "24-40", "32-48", "40-56")
REGIMES = ("all", "rules", "stir_line", "start_line", "after_start", "last")
CONTROL_REGIMES = ("all", "after_start")
MAX_NEW_TOKENS = 6
TARGET_SEED, NULL_SEED = 0, 0
N_BOOT, BOOT_SEED = 2000, 0
PREFILL = "Answer:"


def band_layers(band: str) -> tuple[int, ...]:
    lo, hi = map(int, band.split("-"))
    return tuple(range(lo, hi + 1))


def render(tokenizer, prompt: str) -> str:
    """The prompt as the bank gated it: chat template, thinking off, assistant turn prefilled with "Answer:"."""
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    return text + PREFILL


def spans(item: dict, text: str) -> dict[str, tuple[int, int]]:
    """Character spans of the prompt's regions inside the rendered text."""
    prompt = item["prompt"]
    base = text.index(prompt)
    rules_start = prompt.index("rules:\n") + len("rules:\n")
    stir = prompt.index("You stir the potion")
    start = prompt.index("The potion starts out")
    start_end = prompt.index("\n", start)
    return {
        "rules": (base + rules_start, base + stir),
        "stir_line": (base + stir, base + prompt.index("\n", stir)),
        "start_line": (base + start, base + start_end),
        "after_start": (base + start_end, len(text)),
    }


def regime_positions(regime: str, offsets: list[tuple[int, int]], regions: dict[str, tuple[int, int]]) -> list[int]:
    """Token indices a regime edits (never 0)."""
    last = len(offsets) - 1
    if regime == "all":
        return list(range(1, last + 1))
    if regime == "last":
        return [last]
    lo, hi = regions[regime]
    picked = [i for i, (s, e) in enumerate(offsets) if i > 0 and s < hi and e > lo]
    assert picked, f"regime {regime} selects no position"
    return picked


def answer_colour(text: str, palette: list[str]) -> str | None:
    """The first palette colour named in the continuation's first non-empty line, or None."""
    line = next((ln for ln in text.lower().split("\n") if ln.strip()), "")
    return next((w for w in re.findall(r"[a-z]+", line) if w in palette), None)


def swap_target(item: dict, index: int) -> str | None:
    """A colour X for the intermediate I whose prediction f(X) is distinct from the answer, I, X and the start."""
    f, start, inter, answer = item["table"], item["start"], item["intermediates"][0], item["answer"]
    rows = sorted(c for c in f if c not in (start, inter, answer))
    ok = [x for x in rows if f[x]["stir"] not in (answer, inter, x, start)]
    return random.Random(TARGET_SEED + index).choice(ok) if ok else None


def control_pair(item: dict, index: int) -> tuple[str, str] | None:
    """Two off-trajectory colours to swap with each other: a swap that predicts no change in the answer."""
    off = sorted(item["off_trajectory"])
    if len(off) < 2:
        return None
    a, b = random.Random(TARGET_SEED + 1000 + index).sample(off, 2)
    return a, b


def stage_manifest(kind: str, name: str, band: str | None, sweep: str | None) -> None:
    is_sweep = kind == "sweep"
    assert is_sweep == (band is None) == (sweep is None), "the sweep picks its own band; main needs --band and --sweep"
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "In an in-context two-step lookup, does swapping the intermediate's lens direction move the answer "
        "to the one the table predicts for the swapped-in colour, and at which prompt positions?",
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "lenses": {lens: pins.LENS_FILES[lens] for lens in LENSES},
        "items": {"file": "data/brew_intermediates.json", "sha256": pins.BREW_SHA256},
        "render": "chat template, enable_thinking=False, assistant prefilled with 'Answer:'",
        "eligibility": "greedy continuation's first palette colour is the answer",
        "swap": "clamp.SwapClamp of the two colours' unit lens vectors (concept tokens) at every band layer",
        "flip": "the swapped continuation's first palette colour is f(X), the table's answer for the swapped-in X",
        "target": f"X per item: a table colour (not the start, I or the answer) with f(X) not in {{answer, I, X, start}}, "
        f"drawn with seed {TARGET_SEED} + item index",
        "bands": list(SWEEP_BANDS) if is_sweep else [band],
        "regimes": ["all"] if is_sweep else list(REGIMES),
        "nulls": not is_sweep,
        "control_regimes": [] if is_sweep else list(CONTROL_REGIMES),
        "decision": (
            "band = the one with the highest flip rate, averaged over the two lenses (first on ties); picked on these "
            "same items, so its rate is optimistic"
            if is_sweep
            else {"sweep": sweep, "paired_bootstraps": "after_start - rules, per lens"}
        ),
        "deviations": [
            "Colours are swapped through their single-token lens vectors only (no probes): the colours are in the "
            "prompt, so a probe built from other prompts would add little.",
            "A swap at positions inside the rule table can rewrite the rules themselves, not the computed "
            "intermediate; the regimes keep the two apart.",
        ],
    }
    if not is_sweep:
        assert sweep is not None
        decision = json.loads((RESULTS / sweep / "summary.json").read_text())["decision"]
        assert decision["band"] == band, f"main must use sweep {sweep}'s band ({decision['band']})"
        manifest["sweep"] = {"run": sweep, **decision}
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def run_swap(model, ids, clean_h, atoms_by_layer, positions, null_seed: int | None) -> tuple[str, list[int], float]:
    generator = None if null_seed is None else torch.Generator(device="cuda").manual_seed(null_seed)
    clamps, skipped = {}, []
    for layer, atoms in atoms_by_layer.items():
        direction = None
        if generator is not None:
            direction = torch.nn.functional.normalize(
                torch.randn(atoms.shape[1], device="cuda", generator=generator), dim=0
            )
        if near_parallel(atoms[0], atoms[1]):
            skipped.append(layer)
            continue
        clamps[layer] = SwapClamp(atoms, clean_h[layer], null_direction=direction, positions=positions)
    _, text, _ = model.generate(ids, MAX_NEW_TOKENS, clamps)
    ratio = statistics.mean(c.edit_ratio_edited for c in clamps.values()) if clamps else 0.0
    return text, skipped, ratio


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    assert sha256_of(pins.BREW_FILE) == manifest["items"]["sha256"], "brew items changed since the manifest"
    model = load_model()
    lenses = {lens: JLens(model, lens) for lens in LENSES}
    items = pins.brew_items()
    palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
    layers = sorted({layer for band in manifest["bands"] for layer in band_layers(band)})
    item_rows, outcomes = [], []
    for index, item in enumerate(items):
        tokenizer: Any = model.tokenizer
        text = render(tokenizer, item["prompt"])
        enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
        ids = torch.tensor([enc.input_ids], device="cuda")
        _, clean_h = model.run(ids, record=tuple(layers))
        _, clean_text, _ = model.generate(ids, MAX_NEW_TOKENS)
        clean = answer_colour(clean_text, palette)
        inter, x = item["intermediates"][0], swap_target(item, index)
        f = item["table"]
        row = {
            "name": item["name"],
            "start": item["start"],
            "intermediate": inter,
            "answer": item["answer"],
            "swap_to": x,
            "swap_answer": f[x]["stir"] if x else None,
            "control_pair": control_pair(item, index),
            "clean_continuation": clean_text,
            "clean_colour": clean,
            "n_tokens": len(enc.input_ids),
        }
        regions = spans(item, text)
        offsets = [tuple(o) for o in enc.offset_mapping]
        # The bank's labelled cells, from its own render: our start line and last token must land on them.
        bank_start = sorted(int(k) for k, v in item["regions"].items() if v == "start")
        bank_colon = max(int(k) for k, v in item["regions"].items() if v == "emit_colon")
        row["render_matches_bank"] = (
            regime_positions("start_line", offsets, regions)[: len(bank_start)] == bank_start
            and len(offsets) - 1 == bank_colon
        )
        row["status"] = "eligible" if clean == item["answer"] and x else "clean_wrong" if x else "no_target"
        item_rows.append(row)
        if row["status"] != "eligible":
            continue
        jobs = [
            ("swap", r, null)
            for r in manifest["regimes"]
            for null in ((False, True) if manifest["nulls"] else (False,))
        ]
        jobs += [("control", r, False) for r in manifest["control_regimes"]]
        for band in manifest["bands"]:
            for lens_name, lens in lenses.items():
                for li, (kind, regime, null) in enumerate(jobs):
                    a, b = (inter, x) if kind == "swap" else row["control_pair"]
                    if a is None or b is None:
                        continue
                    tok = torch.tensor([model.concept_token(a), model.concept_token(b)], device="cuda")
                    atoms = {layer: lens.vectors(layer, tok) for layer in band_layers(band)}
                    positions = regime_positions(regime, offsets, regions)
                    seed = NULL_SEED + 1000 * index + li if null else None
                    out_text, skipped, ratio = run_swap(model, ids, clean_h, atoms, positions, seed)
                    colour = answer_colour(out_text, palette)
                    outcomes.append(
                        {
                            "name": item["name"],
                            "band": band,
                            "lens": lens_name,
                            "kind": kind,
                            "regime": regime,
                            "null": null,
                            "continuation": out_text,
                            "colour": colour,
                            "flip": kind == "swap" and colour == row["swap_answer"],
                            "kept_clean": colour == item["answer"],
                            "said_swapped_colour": colour == b,
                            "n_positions": len(positions),
                            "edit_ratio": ratio,
                            "layers_skipped": skipped,
                        }
                    )
        print(f"{item['name']}: done ({len(outcomes)} outcomes)", flush=True)

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    rows = summarize(outcomes)
    summary = {"items": status_counts(item_rows), "rates": rows}
    if manifest["kind"] == "sweep":
        summary["decision"] = sweep_decision(rows)
    else:
        summary["paired_bootstraps"] = bootstraps(outcomes)
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
        groups.setdefault((o["band"], o["lens"], o["kind"], o["regime"], o["null"]), []).append(o)
    rows = []
    for (band, lens, kind, regime, null), group in groups.items():
        n = len(group)
        flips, kept = sum(o["flip"] for o in group), sum(o["kept_clean"] for o in group)
        rows.append(
            {
                "band": band,
                "lens": lens,
                "kind": kind,
                "regime": regime,
                "null": null,
                "n": n,
                "flip": wilson(flips, n),
                "kept_clean": wilson(kept, n),
                "said_swapped_colour": sum(o["said_swapped_colour"] for o in group) / n,
                "neither": (n - flips - kept) / n,
                "edit_ratio_median": statistics.median(o["edit_ratio"] for o in group),
                "n_positions_median": statistics.median(o["n_positions"] for o in group),
            }
        )
    return rows


def sweep_decision(rows: list[dict]) -> dict:
    by_band = {
        band: statistics.mean(r["flip"][0] for r in rows if r["band"] == band and r["kind"] == "swap")
        for band in SWEEP_BANDS
    }
    band = max(SWEEP_BANDS, key=lambda b: by_band[b])
    return {"band": band, "flip_rate_mean_over_lenses": by_band[band], "by_band": by_band}


def bootstraps(outcomes: list[dict]) -> dict[str, tuple[float, float, float]]:
    out = {}
    for lens in LENSES:
        pick = {
            r: {o["name"]: o["flip"] for o in outcomes if o["lens"] == lens and o["kind"] == "swap" and not o["null"]
                and o["regime"] == r}
            for r in ("after_start", "rules")
        }  # fmt: skip
        names = sorted(pick["after_start"])
        out[f"{lens}: after_start - rules"] = paired_bootstrap_diff(
            [pick["after_start"][n] for n in names], [pick["rules"][n] for n in names], n_boot=N_BOOT, seed=BOOT_SEED
        )
    return out


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pct = lambda w: f"{100 * w[0]:.0f}% [{100 * w[1]:.0f}, {100 * w[2]:.0f}]"  # noqa: E731
    lines = [
        f"# {EXP} / {run}",
        "",
        "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()),
        "",
        "| band | lens | kind | regime | null | n | flip [95% CI] | kept clean [95% CI] | said swapped colour | "
        "edit ratio (median) | positions (median) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in summary["rates"]:
        lines.append(
            f"| {r['band']} | {r['lens']} | {r['kind']} | {r['regime']} | {'yes' if r['null'] else ''} | {r['n']} | "
            f"{pct(r['flip'])} | {pct(r['kept_clean'])} | {100 * r['said_swapped_colour']:.0f}% | "
            f"{r['edit_ratio_median']:.3f} | {r['n_positions_median']:.0f} |"
        )
    if "decision" in summary:
        d = summary["decision"]
        lines += [
            "",
            f"Sweep: band {d['band']} (flip rate {100 * d['flip_rate_mean_over_lenses']:.0f}%, mean of lenses).",
        ]
    if "paired_bootstraps" in summary:
        lines += ["", "Paired bootstrap differences in flip rate:"]
        lines += [
            f"- {k}: {100 * v[0]:+.0f} pts [{100 * v[1]:+.0f}, {100 * v[2]:+.0f}]"
            for k, v in summary["paired_bootstraps"].items()
        ]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", help="manifest: the kind (sweep or main); run: the run's folder name")
    parser.add_argument("--band", help="A-B, inclusive (main manifest only)")
    parser.add_argument("--sweep", help="the sweep run that picked --band (main manifest only)")
    parser.add_argument("--name", help="the run's folder name (manifest stage; default = the kind)")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.target in ("sweep", "main"), "manifest needs a kind (sweep/main)"
        stage_manifest(args.target, args.name or args.target, args.band, args.sweep)
    else:
        stage_run(args.target)
