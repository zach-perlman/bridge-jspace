"""exp22_brew_misses (block 6, "competence as data"): on brew items the model gets wrong although it does each step
alone, is the intermediate formed?

exp20 found, on brew's ungated items (fresh 200, test 600; chat + "Answer:", as brew ran), each lookup alone right on
every item but the two composed right on 87-89%: about half the misses answer the intermediate I, as if the potion
were stirred once. Every part B run gates those items out. Here they are the data: at exp04's window (layers 36-50,
positions after the start line), on the clean prompt, unedited,
  code   exp07's linear code (fit on brew_fit, none of these items) read jointly for the intermediate and the answer:
         the (I', A') whose fitted activation, given the item's start colour, is nearest the item's own (squared error
         summed over the positions); unlike exp07's read, the item's answer is not given
  lens   J++'s reading: is I the top-1 of the 12 colours at one or more of the positions; the same for a distractor
         colour (a seeded colour of the table off the item's path), the control
per item and window layer, then averaged over the layers. Groups (exp20 v1, chat + "Answer:"): hit (the composed
answer right), miss (wrong, each step alone right), miss_I (a miss answering I), miss_other.

Stages (write-once): manifest --name N --why "..."   run N
"""

from __future__ import annotations

import argparse
import json
import random
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
from bridge_jspace.stats import wilson
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp07_step_code import CODE_FILE, COLOURS, WINDOW, tokenized

EXP = "exp22_brew_misses"
RESULTS = pins.RESULTS_DIR / EXP
EXP20 = pins.RESULTS_DIR / "exp20_competence" / "v1"
SETS = {"brew_fresh": pins.brew_fresh_items, "brew_test": pins.brew_test_items}
FORMAT = "chat_prefill"
DISTRACTOR_SEED = 22
N_BOOT, BOOT_SEED = 2000, 0
SAME, FAR = 0.10, 0.25  # decision margins on the miss - hit difference in decoding I (see the manifest)


def labels() -> dict[tuple[str, int], dict]:
    """exp20 v1's judgements in brew's format: per (set, index), the clean, hop1 and hop2 outcomes and the answer."""
    out: dict[tuple[str, int], dict] = {}
    for line in (EXP20 / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["task"] in SETS and r["format"] == FORMAT:
            row = out.setdefault((r["task"], r["index"]), {})
            row[r["kind"]] = r["correct"]
            if r["kind"] == "clean":
                row["said"] = r["said"]
    return out


def group_of(row: dict, item: dict) -> str | None:
    if row["clean"]:
        return "hit"
    if row["hop1"] and row["hop2"]:
        return "miss_I" if row["said"] == item["intermediates"][0] else "miss_other"
    return None  # a step alone is wrong (none in exp20 v1)


def stage_manifest(name: str, why: str) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "run": name,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "question": "On brew items the model gets wrong although it does each step alone, is the intermediate formed "
        "at exp04's window, and what answer does the state hold?",
        "model": pins.model_pin(),
        "items": {
            s: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha}
            for s, (f, sha) in {
                "brew_fresh": (pins.BREW_FRESH_FILE, pins.BREW_FRESH_SHA256),
                "brew_test": (pins.BREW_TEST_FILE, pins.BREW_TEST_SHA256),
            }.items()
        },
        "labels": {"run": "exp20_competence/v1", "items_sha256": sha256_of(EXP20 / "items.jsonl"), "format": FORMAT},
        "format": "chat template, thinking off, 'Answer:' prefilled (exp03's render, as brew ran)",
        "window": {"layers": list(WINDOW), "positions": "after the start line (exp04, exp07)"},
        "code": {"file": str(CODE_FILE.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(CODE_FILE)},
        "readers": {
            "code": "joint argmin over (I', A') of |h - w_0 - E_S[S] - E_I[I'] - E_A[A']|^2 summed over positions",
            "lens": "J++ readout; I top-1 among the 12 colours at >= 1 position; the same for a distractor colour (seed "
            f"{DISTRACTOR_SEED} + index, a table colour off the S -> I -> A path)",
        },
        "groups": "hit: the composed answer right; miss: wrong with each step alone right (miss_I: answers I; "
        "miss_other: anything else)",
        "decision": {
            "primary": "code: the share of window layers decoding I, per item, averaged per group; miss - hit with a "
            f"bootstrap CI (items resampled within groups, B={N_BOOT}, seed {BOOT_SEED})",
            "formed": f"'formed on misses as on hits' if the CI's lower bound is above -{SAME}; 'often not formed' if its "
            f"upper bound is below -{FAR}; otherwise 'partly'",
            "answer": "secondary: on misses, the share of window layers where the code's decoded answer is the model's "
            "own (wrong) answer vs the correct one",
        },
        "prediction": "formed on misses as on hits (the model answers I on half the misses, so I is there); the "
        "decoded answer follows the model's own answer",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def joint_decode(w: torch.Tensor, h: torch.Tensor, start: str) -> tuple[str, str]:
    """(I', A') minimising |h - w_0 - E_S[S] - E_I[I'] - E_A[A']|^2 over positions (w [f, P, d], h [P, d])."""
    k = len(COLOURS)
    r = (h - w[0] - w[1 + COLOURS.index(start)]).double()
    wi, wa = w[1 + k : 1 + 2 * k].double(), w[1 + 2 * k : 1 + 3 * k].double()  # [12, P, d]
    ri, ra = torch.einsum("pd,kpd->k", r, wi), torch.einsum("pd,kpd->k", r, wa)
    ni, na = wi.pow(2).sum((1, 2)), wa.pow(2).sum((1, 2))
    cross = torch.einsum("ipd,apd->ia", wi, wa)
    err = -2 * ri[:, None] - 2 * ra[None, :] + ni[:, None] + na[None, :] + 2 * cross
    i, a = divmod(int(err.argmin()), k)
    return COLOURS[i], COLOURS[a]


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    assert sha256_of(EXP20 / "items.jsonl") == manifest["labels"]["items_sha256"], "exp20's items changed"
    assert sha256_of(CODE_FILE) == manifest["code"]["sha256"], "exp07's code changed"
    lab = labels()
    model = load_model()
    tokenizer: Any = model.tokenizer
    code = torch.load(CODE_FILE, map_location="cpu", weights_only=True)
    w = {layer: code["w"][layer].to("cuda") for layer in WINDOW}
    lens = JLens(model, "jpp")
    colour_tok = torch.tensor([model.concept_token(c) for c in COLOURS], device="cuda")
    rows, skipped = [], 0
    for set_name, load in SETS.items():
        for index, item in enumerate(load()):
            group = group_of(lab[(set_name, index)], item)
            ids, positions = tokenized(tokenizer, item)
            if group is None or [ids[p] for p in positions] != code["suffix_ids"]:
                skipped += 1
                continue
            path = {item["start"], item["intermediates"][0], item["answer"]}
            off = sorted(c for c in item["off_trajectory"] if c not in path)
            distractor = random.Random(DISTRACTOR_SEED + index).choice(off)
            _, rec = model.run(torch.tensor([ids], device="cuda"), record=WINDOW)
            row = {"set": set_name, "index": index, "name": item["name"], "group": group, "said": lab[(set_name, index)]["said"],
                   "S": item["start"], "I": item["intermediates"][0], "A": item["answer"], "distractor": distractor, "layers": {}}  # fmt: skip
            for layer in WINDOW:
                h = rec[layer][positions]
                i_hat, a_hat = joint_decode(w[layer], h, item["start"])
                scores = lens.readout(h, layer)[:, colour_tok]  # [P, 12]
                top = scores.argmax(dim=1).tolist()
                row["layers"][str(layer)] = {
                    "code_I": i_hat,
                    "code_A": a_hat,
                    "lens_I_top1": COLOURS.index(row["I"]) in top,
                    "lens_distractor_top1": COLOURS.index(distractor) in top,
                }
            rows.append(row)
        print(f"{set_name}: done ({len(rows)} items)", flush=True)
    write_jsonl(out_dir / "items.jsonl", rows)
    summary = summarize(rows)
    summary["skipped"] = skipped
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def item_scores(rows: list[dict]) -> dict[str, list[float]]:
    out: dict[str, list[float]] = {k: [] for k in ("code_I", "code_A", "code_said", "lens_I", "lens_distractor")}
    for r in rows:
        ls = r["layers"].values()
        n = len(ls)
        out["code_I"].append(sum(v["code_I"] == r["I"] for v in ls) / n)
        out["code_A"].append(sum(v["code_A"] == r["A"] for v in ls) / n)
        out["code_said"].append(sum(v["code_A"] == r["said"] for v in ls) / n)
        out["lens_I"].append(sum(v["lens_I_top1"] for v in ls) / n)
        out["lens_distractor"].append(sum(v["lens_distractor_top1"] for v in ls) / n)
    return out


def boot_diff(a: list[float], b: list[float]) -> tuple[float, float, float]:
    """mean(a) - mean(b), 95% CI resampling items within each group."""
    rng = random.Random(BOOT_SEED)
    diffs = sorted(
        statistics.mean(rng.choices(a, k=len(a))) - statistics.mean(rng.choices(b, k=len(b))) for _ in range(N_BOOT)
    )
    return statistics.mean(a) - statistics.mean(b), diffs[int(0.025 * N_BOOT)], diffs[int(0.975 * N_BOOT) - 1]


def summarize(rows: list[dict]) -> dict:
    groups = {
        "hit": [r for r in rows if r["group"] == "hit"],
        "miss": [r for r in rows if r["group"].startswith("miss")],
        "miss_I": [r for r in rows if r["group"] == "miss_I"],
        "miss_other": [r for r in rows if r["group"] == "miss_other"],
    }
    scores = {g: item_scores(rs) for g, rs in groups.items()}
    out: dict[str, Any] = {"n": {g: len(rs) for g, rs in groups.items()}, "groups": {}, "differences": {}}
    for g, sc in scores.items():
        out["groups"][g] = {k: statistics.mean(v) if v else None for k, v in sc.items()}
    for g in ("miss", "miss_I", "miss_other"):
        if groups[g]:
            out["differences"][f"{g} - hit"] = {
                k: boot_diff(scores[g][k], scores["hit"][k]) for k in ("code_I", "code_A", "lens_I", "lens_distractor")
            }
    d = out["differences"].get("miss - hit", {}).get("code_I")
    out["verdict"] = (
        None
        if d is None
        else "formed on misses as on hits"
        if d[1] > -SAME
        else "often not formed"
        if d[2] < -FAR
        else "partly"
    )
    by_layer = {}
    for layer in WINDOW:
        key = str(layer)
        by_layer[layer] = {
            g: wilson(sum(r["layers"][key]["code_I"] == r["I"] for r in rs), len(rs))[0] if rs else None
            for g, rs in groups.items()
        }
    out["code_I_by_layer"] = by_layer
    return out


def write_md(path: Path, run: str, s: dict) -> None:
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {run}", "", f"Items: {s['n']} (skipped {s['skipped']})", "", f"Verdict: {s['verdict']}", ""]
    lines += ["| group | n | code decodes I | code decodes A | code's A = the model's answer | J++ has I top-1 | J++ has the distractor top-1 |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for g, v in s["groups"].items():
        if v["code_I"] is None:
            continue
        lines.append(f"| {g} | {s['n'][g]} | {100 * v['code_I']:.0f}% | {100 * v['code_A']:.0f}% | {100 * v['code_said']:.0f}% | {100 * v['lens_I']:.0f}% | {100 * v['lens_distractor']:.0f}% |")  # fmt: skip
    lines += ["", "Differences (pts, 95% bootstrap CI):"]
    for k, d in s["differences"].items():
        lines.append(f"- {k}: " + "; ".join(f"{m} {pts(v)}" for m, v in d.items()))
    lines += ["", "Code decodes I, by layer: " + json.dumps(s["code_I_by_layer"])]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", nargs="?")
    parser.add_argument("--name")
    parser.add_argument("--why")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.target, "run needs the run's name"
        stage_run(args.target)
