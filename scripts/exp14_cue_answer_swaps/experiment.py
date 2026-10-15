"""exp14_cue_answer_swaps: at the cue phrase, does swapping the answer's lens direction change the answer as often as
swapping the bridge's? (design: Danyil)

Part B (exp02 v4) found that the bridge's J-space swap acts at the cue phrase ("Amazon River ends"), not where part A
reads the bridge (one word before the end). Two readings: the cue phrase holds the bridge and the last token computes
the answer from it (two steps), or it already holds the answer (a shortcut, Amazon River -> Portuguese).

Test: part B's raw lens-vector swap (clamp.SwapClamp on the two words' unit lens vectors, exp02's raw_jlens), once
with the bridge pair (Brazil -> Mexico) and once with the answer pair (Portuguese -> Spanish), in each configured cell
(prompt positions x layer band) and with part B's matched-norm random-direction null, for the J-lens and J++ vectors.
Answer swaps need single-token answers (concept tokens); questions without them are left out of the answer rows.

Leakage: per question, lens, cell and band layer, the cosine between the two swaps' difference vectors and the share
of each swap's edit (computed on the clean residual at the edited positions) that lies in the other pair's span.

Scoring and eligibility as part B v4 (exp02's `prepare` / `swap`): prompts with the trailing space stripped, greedy
continuation judged by exp13's criterion C; a flip is the swap answer in the continuation and not the clean answer.
Checks before any result is read: the eligible set must equal part B's v4 one, and the bridge swaps must reproduce
part B's raw_jlens outcomes in the cells part B ran.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path
from typing import Any

import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import REPO_ROOT, RESULTS_DIR
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.utils import progress

KINDS = ("bridge", "answer")
PAIR = {"bridge": ("intermediate", "swap_to"), "answer": ("answer", "swap_answer")}


class _Everything:
    def __contains__(self, _: object) -> bool:
        return True


class _NoProbes:
    """exp02's `prepare` drops questions whose entities have no exp01 probe; lens-vector swaps need none."""

    index = _Everything()


class CueAnswerSwaps(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.clamp import SwapClamp
        from bridge_jspace.data import load_items
        from bridge_jspace.lens import JLens
        from bridge_jspace.model import load_model
        from scripts.exp02_swaps import CUE_SPANS, band_layers, prepare, regime_positions, span_positions, swap

        p = self.params
        model = load_model()  # part B's loader (edits, greedy continuation); self.model is never built
        lenses = {name: JLens(model, name) for name in p["lenses"]}
        cues = json.loads(CUE_SPANS.read_text())["cues"]
        cells = [(c["positions"], c["band"]) for c in p["cells"]]
        layers = sorted({layer for _, band in cells for layer in band_layers(band)})

        tokenizer: Any = model.tokenizer  # typed `object` in part B's Model
        no_probes: Any = _NoProbes()  # stands in for exp02's Probes, whose only use in `prepare` is the index
        item_rows, outcomes, leaks = [], [], []
        items = load_items()
        for index, item in enumerate(progress(items[: p.get("limit")], "items")):
            row, prepared = prepare(model, no_probes, item, layers, "greedy_c", "stripped")
            item_rows.append(row)
            if row["status"] != "eligible" or prepared is None:
                continue
            ids, clean_h, answer_ids, swap_ids = prepared
            prompt = item["prompt"].rstrip()
            start = prompt.index(cues[item["name"]])
            enc = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
            assert enc.input_ids == ids[0].tolist(), "offsets come from another tokenization"
            cue = span_positions(enc.offset_mapping, start, start + len(cues[item["name"]]))
            tokens = {kind: _pair_tokens(model, item, kind) for kind in p["kinds"]}
            row["swappable"] = {kind: t is not None for kind, t in tokens.items()}
            for lens_name, lens in lenses.items():
                for regime, band in cells:
                    positions = regime_positions(regime, ids.shape[1], cue)
                    atoms = {
                        kind: {
                            layer: lens.vectors(layer, torch.tensor(t, device="cuda")) for layer in band_layers(band)
                        }
                        for kind, t in tokens.items()
                        if t is not None
                    }
                    for ki, kind in enumerate(p["kinds"]):
                        if kind not in atoms:
                            continue
                        for null in (False, True) if p["nulls"] else (False,):
                            seed = p["null_seed"] + 1000 * index + ki if null else None
                            result = swap(
                                model,
                                ids,
                                clean_h,
                                atoms[kind],
                                item,
                                answer_ids,
                                swap_ids,
                                seed,
                                "greedy_c",
                                positions,
                            )
                            outcomes.append(
                                {"name": item["name"], "lens": lens_name, "positions": regime, "band": band,
                                 "kind": kind, "null": null, **result}
                            )  # fmt: skip
                    if set(atoms) == set(KINDS):
                        for layer in band_layers(band):
                            b, a = atoms["bridge"][layer], atoms["answer"][layer]
                            h = clean_h[layer]
                            d_b = SwapClamp(b, h, positions=positions).delta(h)
                            d_a = SwapClamp(a, h, positions=positions).delta(h)
                            leaks.append(
                                {"name": item["name"], "lens": lens_name, "positions": regime, "band": band,
                                 "layer": layer, "diff_cosine": diff_cosine(b, a),
                                 "bridge_edit_in_answer_span": share_in_span(d_b, a),
                                 "answer_edit_in_bridge_span": share_in_span(d_a, b)}
                            )  # fmt: skip

        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("outcomes.jsonl", outcomes)
        self.save_jsonl("leakage.jsonl", leaks)
        eligible = [r["name"] for r in item_rows if r["status"] == "eligible"]
        summary = {
            "model": "Qwen3.6-27B (part B's loader, pins.py)",
            "items": _counts(item_rows),
            "eligibility_check": eligibility_check(eligible, REPO_ROOT / p["part_b_labels"], p.get("limit")),
            "replication_check": replication_check(outcomes, p["part_b_reference"]),
            "rates": rates(outcomes),
            "bridge_minus_answer": bridge_minus_answer(outcomes, p["n_boot"], p["boot_seed"]),
            "leakage": leakage_summary(leaks),
            "positive_control": positive_control(outcomes, p["control_min_flip"]),
            "decision_rule": p["decision"],
        }
        from .plot import plot_run

        plot_run(self.run_dir, summary)
        return summary


def _pair_tokens(model, item: dict, kind: str) -> list[int] | None:
    """The concept tokens of a swap's two words, or None when one has no single-token surface."""
    try:
        return [model.concept_token(item[field]) for field in PAIR[kind]]
    except ValueError:
        return None


def _counts(rows: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        out[r["status"]] = out.get(r["status"], 0) + 1
    return out


# ---- pure helpers (unit-tested) ------------------------------------------------------------------


def diff_cosine(pair_a: torch.Tensor, pair_b: torch.Tensor) -> float:
    """Cosine between two swaps' difference vectors: (a0 - a1) vs (b0 - b1). A swap's edit lies along its pair's
    difference when the two atoms are near-orthogonal, so this is how much one swap is also the other."""
    return float(torch.nn.functional.cosine_similarity(pair_a[0] - pair_a[1], pair_b[0] - pair_b[1], dim=0))


def share_in_span(delta: torch.Tensor, atoms: torch.Tensor) -> float:
    """Share of an edit [P, d] (Frobenius norm over its positions) lying in span(atoms [K, d]); nan for no edit."""
    norm = float(delta.norm())
    if norm == 0:
        return math.nan
    atoms = atoms.to(delta.dtype)
    return float(((delta @ torch.linalg.pinv(atoms)) @ atoms).norm()) / norm


def _key(o: dict) -> tuple:
    return (o["lens"], o["positions"], o["band"], o["kind"], o["null"])


def rates(outcomes: list[dict]) -> list[dict]:
    """Per lens, cell, kind and null: flip and kept-clean rates (Wilson 95%), collateral damage, edit size."""
    groups: dict[tuple, list[dict]] = {}
    for o in outcomes:
        groups.setdefault(_key(o), []).append(o)
    out = []
    for (lens, positions, band, kind, null), g in groups.items():
        n, flips, kept = len(g), sum(o["flip"] for o in g), sum(o["kept_clean"] for o in g)
        out.append(
            {"lens": lens, "positions": positions, "band": band, "kind": kind, "null": null, "n": n,
             "flip": wilson(flips, n), "kept_clean": wilson(kept, n), "neither": (n - flips - kept) / n,
             "edit_ratio_median": statistics.median(o["edit_ratio"] for o in g),
             "items_with_skipped_layers": sum(bool(o["layers_skipped"]) for o in g)}
        )  # fmt: skip
    return out


def bridge_minus_answer(outcomes: list[dict], n_boot: int, seed: int) -> list[dict]:
    """Per lens and cell, on the questions with both swaps: bridge - answer flip rate, paired bootstrap 95% CI."""
    real = [o for o in outcomes if not o["null"]]
    flips = {(o["lens"], o["positions"], o["band"], o["kind"], o["name"]): o["flip"] for o in real}
    out = []
    for lens, positions, band in sorted({(o["lens"], o["positions"], o["band"]) for o in real}):
        names = sorted({o["name"] for o in real if (o["lens"], o["positions"], o["band"]) == (lens, positions, band)})
        both = [n for n in names if all((lens, positions, band, k, n) in flips for k in KINDS)]
        if not both:
            continue
        b = [flips[(lens, positions, band, "bridge", n)] for n in both]
        a = [flips[(lens, positions, band, "answer", n)] for n in both]
        out.append(
            {"lens": lens, "positions": positions, "band": band, "n": len(both),
             "bridge": sum(b) / len(b), "answer": sum(a) / len(a),
             "diff": paired_bootstrap_diff(b, a, n_boot=n_boot, seed=seed)}
        )  # fmt: skip
    return out


def leakage_summary(leaks: list[dict]) -> list[dict]:
    """Per lens and cell: medians over questions of the per-question mean over band layers."""
    fields = ("diff_cosine", "bridge_edit_in_answer_span", "answer_edit_in_bridge_span")
    by: dict[tuple, dict[str, dict[str, list[float]]]] = {}
    for r in leaks:
        cell = by.setdefault((r["lens"], r["positions"], r["band"]), {})
        for f in fields:
            if not math.isnan(r[f]):
                cell.setdefault(f, {}).setdefault(r["name"], []).append(r[f])
    out = []
    for (lens, positions, band), cell in sorted(by.items()):
        row: dict[str, Any] = {"lens": lens, "positions": positions, "band": band}
        for f in fields:
            per_q = [statistics.mean(v) for v in cell.get(f, {}).values()]
            row[f] = {"median": statistics.median(per_q), "max": max(per_q), "n": len(per_q)} if per_q else None
        out.append(row)
    return out


def positive_control(outcomes: list[dict], min_flip: float) -> dict[str, Any]:
    """Per lens: the answer swap's best last-token flip rate, and whether it reaches `min_flip`."""
    out: dict[str, Any] = {}
    for lens in sorted({o["lens"] for o in outcomes}):
        last = [r for r in rates([o for o in outcomes if o["lens"] == lens])
                if r["positions"] == "last" and r["kind"] == "answer" and not r["null"]]  # fmt: skip
        best = max(last, key=lambda r: r["flip"][0], default=None)
        out[lens] = {"band": best["band"], "flip": best["flip"], "works": best["flip"][0] >= min_flip} if best else None
    return out


def eligibility_check(eligible: list[str], labels_csv: Path, limit: int | None) -> dict[str, Any]:
    """Our eligible questions vs part B's (v4 labels), over the questions this run looked at."""
    with open(labels_csv) as f:
        rows = list(csv.DictReader(f))
    looked = {r["name"] for r in rows[:limit]} if limit else {r["name"] for r in rows}
    theirs = {r["name"] for r in rows if r["status"] == "eligible"} & looked
    ours = set(eligible)
    return {"n_ours": len(ours), "n_part_b": len(theirs), "same": ours == theirs,
            "only_ours": sorted(ours - theirs), "only_part_b": sorted(theirs - ours)}  # fmt: skip


def replication_check(outcomes: list[dict], reference: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Our bridge swaps vs part B's raw_jlens outcomes (real and null) in the cells part B ran: per-question
    agreement and both flip rates."""
    out: dict[str, Any] = {}
    for lens, cells in reference.items():
        for cell, run in cells.items():
            positions, band = cell.split("/")
            path = RESULTS_DIR / "exp02_swaps" / run / "outcomes.jsonl"
            theirs = {
                (o["name"], o["null"]): o["flip"]
                for o in (json.loads(x) for x in path.read_text().splitlines() if x.strip())
                if o["condition"] == "raw_jlens" and o["band"] == band
            }
            ours = {
                (o["name"], o["null"]): o["flip"]
                for o in outcomes
                if (o["lens"], o["positions"], o["band"], o["kind"]) == (lens, positions, band, "bridge")
            }
            shared = sorted(set(ours) & set(theirs))
            if not shared:
                continue
            real = [k for k in shared if not k[1]]
            out[f"{lens} {cell}"] = {
                "part_b_run": run,
                "n": len(real),
                "agree": sum(ours[k] == theirs[k] for k in shared),
                "of": len(shared),
                "flip_ours": sum(ours[k] for k in real) / len(real) if real else None,
                "flip_part_b": sum(theirs[k] for k in real) / len(real) if real else None,
            }
    return out


def by_overlap(outcomes: list[dict], leaks: list[dict]) -> list[dict]:
    """Flip rates split at the median overlap between the two swaps (a question's mean over band layers of the
    cosine between their difference vectors), per lens and cell: does a swap work only where it is also the other?"""
    cos: dict[tuple, list[float]] = {}
    for r in leaks:
        cos.setdefault((r["lens"], r["positions"], r["band"], r["name"]), []).append(r["diff_cosine"])
    mean_cos = {k: statistics.mean(v) for k, v in cos.items()}
    out = []
    for lens, positions, band in sorted({k[:3] for k in mean_cos}):
        names = {k[3]: v for k, v in mean_cos.items() if k[:3] == (lens, positions, band)}
        cut = statistics.median(names.values())
        for half, members in (("low", {n for n, c in names.items() if c < cut}),
                              ("high", {n for n, c in names.items() if c >= cut})):  # fmt: skip
            for kind in KINDS:
                flips = [o["flip"] for o in outcomes if (o["lens"], o["positions"], o["band"], o["kind"]) ==
                         (lens, positions, band, kind) and not o["null"] and o["name"] in members]  # fmt: skip
                out.append({"lens": lens, "positions": positions, "band": band, "overlap": half, "cut": round(cut, 4),
                            "kind": kind, "n": len(flips), "flip": wilson(sum(flips), len(flips))})  # fmt: skip
    return out


def analyze(run_dir: str | Path) -> Path:
    """The overlap split of a finished run, into `<run_dir>/analysis-<timestamp>-overlap/` with its figure."""
    from datetime import datetime

    from .plot import plot_overlap

    run_dir = Path(run_dir)

    def load(name: str) -> list[dict]:
        return [json.loads(x) for x in (run_dir / name).read_text().splitlines() if x.strip()]

    rows = by_overlap(load("outcomes.jsonl"), load("leakage.jsonl"))
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}-overlap"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps({"source_run": str(run_dir), "by_overlap": rows}, indent=2))
    plot_overlap(out / "flip_rates_by_overlap.png", rows)
    return out


if __name__ == "__main__":
    # uv run python -m scripts.exp14_cue_answer_swaps.experiment analyze <run_dir>
    import sys

    if sys.argv[1:2] != ["analyze"] or len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[2]))
