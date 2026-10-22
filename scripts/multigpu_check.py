"""multigpu_check (T12, 22 Oct night): is the multi-GPU path (BJ_DEVICE_MAP; model.py, Devices) the single-GPU forward?

The target (pins.TARGET; Qwen3.6-27B by default) is loaded twice in one process: on one GPU (device_map="cuda", what
every run uses by default), then split over the visible GPUs (--device-map, BJ_DEVICE_MAP syntax, default "auto"; at
least 2 GPUs). On both loads, the same prompts and conditions (layers for 64 blocks: record 16 and 48, edit at 48):

  clean     unedited forward: last-token logits, and the block outputs at N/4 and 3N/4 (recorded, home device)
  addrows   exp04's AddRows at 3N/4, a block on another GPU in the split: delta = h_C - h_clean at every position after
            the first, i.e. the counterfactual C's block output copied in (C swaps the queried person's pet)
  knockout  no position after the context can read the context directly, at any layer (knock_out, value mode)
  generate  generate_batch with rows [unedited, addrows], 4 greedy tokens: first-step logits and the texts
  lens      the frozen lens's readout of the clean block output at 3N/4, last position: of the home copy and of a copy
            on the head's GPU (the J map follows the residual)

Prompts: 20 BL items of the animal suite (data/suite_v1/BL.json, wording A), drawn with random.Random(0), rendered as
every run renders them (suite_v1.render: chat format unless BJ_FORMAT=raw). No other randomness.

Pass (all must hold). Per prompt and condition: the argmax of the logits is the same token on both loads and
max |Δ logit| <= TOL = 0.25. The logits are bf16 values (lm_head in bf16) cast to fp32, so 0.25 is two rounding steps
of a logit in [16, 32), where the top logits sit; the same kernels on the same GPU type should give exactly 0, and
`identical` reports how often they do. Recorded block outputs within 1e-2 x their max |value|. Generated texts equal.
Every output on cuda:0 on both loads. The split uses >= 2 GPUs with the edit layer off GPU 0. And the conditions must
matter: on the one-GPU load, the median max |Δ logit| of addrows, knockout and the generate rows vs clean exceeds 4 x
TOL, so an edit or knock-out lost on the split could not pass.

Writes results/multigpu_check/<name>/report.json (write-once; per-prompt numbers included); exits 1 if any check fails.

  CUDA_VISIBLE_DEVICES=2,3 uv run python scripts/multigpu_check.py --name multigpu_check_v1
"""

from __future__ import annotations

import argparse
import gc
import json
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.tokens import raw_encoding
from scripts import suite_v1 as S
from scripts.exp04_brew_parts import AddRows

N_PROMPTS, SEED = 20, 0
FAMILY = "BL"
TOL = 0.25
RECORD_REL_TOL = 1e-2
EFFECT_MIN = 4 * TOL
NEW_TOKENS = 4
EARLY, EDIT = pins.N_LAYERS // 4, 3 * pins.N_LAYERS // 4
RECORD = (EARLY, EDIT)
LOGIT_CONDITIONS = ("clean", "addrows", "knockout", "generate", "lens", "lens_remote")
HOME = torch.device("cuda", 0)


def cases(tok) -> list[dict]:
    items = random.Random(SEED).sample(S.load(FAMILY), N_PROMPTS)
    out = []
    for it in items:
        text = S.render(tok, it["context"], it["question"])
        ids = raw_encoding(tok, text)["input_ids"]
        cf_ids = raw_encoding(tok, S.render(tok, it["cf_context"], it["cf_question"]))["input_ids"]
        assert len(cf_ids) == len(ids), f"{it['id']}: C does not line up with the clean prompt"
        enc = raw_encoding(tok, text, offsets=True)
        c0, c1 = text.index(it["context"]), text.index(it["context"]) + len(it["context"])
        context = [i for i, (s, e) in enumerate(enc["offset_mapping"]) if i > 0 and e > s and s >= c0 and e <= c1]
        out.append({"id": it["id"], "ids": ids, "cf_ids": cf_ids, "context": context})
    return out


@torch.no_grad()
def measure(model, lens, items: list[dict], label: str) -> list[dict[str, Any]]:
    """Every condition on every prompt; tensors returned on the CPU, with whether each came back on cuda:0."""
    from bridge_jspace.knockout import knock_out

    head_gpu = model.hf.lm_head.weight.device
    rows = []
    for c in tqdm(items, desc=label):
        ids = torch.tensor([c["ids"]], device="cuda")
        last = ids.shape[1] - 1
        clean, rec = model.run(ids, record=RECORD)
        _, rec_cf = model.run(torch.tensor([c["cf_ids"]], device="cuda"), record=(EDIT,))
        pos = list(range(1, last + 1))
        edit = {EDIT: AddRows(rec_cf[EDIT][pos] - rec[EDIT][pos], pos)}
        edited, rec_edited = model.run(ids, edit, record=(EDIT,))
        after = list(range(max(c["context"]) + 1, last + 1))
        with knock_out(model, range(pins.N_LAYERS), [c["context"]], [after]):
            knocked, _ = model.run(ids)
        texts, first = model.generate_batch(ids, NEW_TOKENS, [{}, edit], first_logits=True)
        out = {"clean": clean, "addrows": edited, "knockout": knocked, "generate": first,
               **{f"rec_{la}": rec[la] for la in RECORD}, "rec_addrows": rec_edited[EDIT]}  # fmt: skip
        if lens is not None:
            h = rec[EDIT][-1:]
            out["lens"] = lens.readout(h, EDIT)[0]
            out["lens_remote"] = lens.readout(h.to(head_gpu), EDIT)[0]
        rows.append({"texts": texts, "on_home": all(t.device == HOME for t in out.values()),
                     **{k: t.cpu() for k, t in out.items()}})  # fmt: skip
    return rows


def compare(one: list[dict], two: list[dict]) -> dict[str, Any]:
    """Per condition: max |Δ| between the loads, bit-identity, argmax agreement, and the condition's effect vs clean
    on the one-GPU load (generate: the edited row vs the unedited row)."""
    report: dict[str, Any] = {}
    for cond in LOGIT_CONDITIONS:
        if cond not in one[0]:
            continue
        per = []
        for a, b in zip(one, two, strict=True):
            x, y = a[cond], b[cond]
            row = {"max_abs": float((x - y).abs().max()), "identical": bool(torch.equal(x, y)),
                   "argmax_same": bool(torch.equal(x.argmax(-1), y.argmax(-1)))}  # fmt: skip
            if cond in ("addrows", "knockout"):
                row["effect"] = float((x - a["clean"]).abs().max())
                row["argmax_changed"] = int(x.argmax()) != int(a["clean"].argmax())
            elif cond == "generate":
                row["effect"] = float((x[1] - x[0]).abs().max())
            per.append(row)
        summary: dict[str, Any] = {
            "max_abs": max(r["max_abs"] for r in per),
            "median_max_abs": statistics.median(r["max_abs"] for r in per),
            "identical": f"{sum(r['identical'] for r in per)}/{len(per)}",
            "argmax_same": f"{sum(r['argmax_same'] for r in per)}/{len(per)}",
            "pass": all(r["argmax_same"] and r["max_abs"] <= TOL for r in per),
        }
        effects = [r["effect"] for r in per if "effect" in r]
        if effects:
            summary["effect_median"], summary["effect_min"] = statistics.median(effects), min(effects)
            summary["effect_ok"] = summary["effect_median"] > EFFECT_MIN
        if cond in ("addrows", "knockout"):
            summary["argmax_changed_vs_clean"] = f"{sum(r['argmax_changed'] for r in per)}/{len(per)}"
        report[cond] = {**summary, "per_prompt": per}
    records = {}
    for key in [f"rec_{la}" for la in RECORD] + ["rec_addrows"]:
        rel = [float((a[key] - b[key]).abs().max() / a[key].abs().max()) for a, b in zip(one, two, strict=True)]
        records[key] = {"max_rel": max(rel), "pass": max(rel) <= RECORD_REL_TOL}
    report["records"] = records
    report["texts_equal"] = f"{sum(a['texts'] == b['texts'] for a, b in zip(one, two, strict=True))}/{len(one)}"
    return report


def placement_summary(model) -> dict[str, Any]:
    by_device: dict[str, list[int]] = {}
    for la in range(pins.N_LAYERS):
        by_device.setdefault(str(next(model.layers[la].parameters()).device), []).append(la)
    return {"blocks": {d: [ls[0], ls[-1], len(ls)] for d, ls in by_device.items()},
            "embedding": str(model.device), "head": str(model.hf.lm_head.weight.device)}  # fmt: skip


def load(device_map: str, timings: dict, key: str):
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    t0 = time.time()
    model = load_model(device_map=device_map)
    lens = JLens(model, pins.FROZEN_LENS) if pins.FROZEN_LENS in pins.LENS_SOURCES else None
    if lens is not None and EDIT not in lens.source_layers:  # it reads the recorded output at the edit layer only
        lens = None
    timings[f"{key}_load"] = round(time.time() - t0)
    return model, lens


def peak_gib() -> dict[str, float]:
    return {f"cuda:{i}": round(torch.cuda.max_memory_allocated(i) / 2**30, 1) for i in range(torch.cuda.device_count())}


def main() -> int:
    from bridge_jspace.knockout import kernel_path

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--device-map", default="auto", help="the split's BJ_DEVICE_MAP value (default: auto)")
    a = ap.parse_args()
    pins.check_run_name(a.name)
    out = pins.RESULTS_DIR / "multigpu_check" / a.name
    assert not (out / "report.json").exists(), f"{out} exists; runs are written once"
    assert torch.cuda.device_count() >= 2, f"{torch.cuda.device_count()} GPU(s) visible; the split needs 2 or more"
    timings: dict[str, int] = {}

    model, lens = load("", timings, "one_gpu")
    items = cases(model.tokenizer)
    t0 = time.time()
    one = measure(model, lens, items, "one GPU")
    timings["one_gpu_run"] = round(time.time() - t0)
    peak_one = peak_gib()
    del model, lens
    gc.collect()
    torch.cuda.empty_cache()
    for i in range(torch.cuda.device_count()):
        torch.cuda.reset_peak_memory_stats(i)

    model, lens = load(a.device_map, timings, "split")
    split = placement_summary(model)
    edit_gpu = str(next(model.layers[EDIT].parameters()).device)
    t0 = time.time()
    two = measure(model, lens, items, "split")
    timings["split_run"] = round(time.time() - t0)

    report = compare(one, two)
    checks = {
        "logits": all(report[c]["pass"] for c in LOGIT_CONDITIONS if c in report),
        "records": all(r["pass"] for r in report["records"].values()),
        "texts": report["texts_equal"] == f"{len(items)}/{len(items)}",
        "on_home": all(r["on_home"] for r in one + two),
        "split_used": len(split["blocks"]) >= 2 and edit_gpu != str(HOME),
        "effects": all(report[c]["effect_ok"] for c in ("addrows", "knockout", "generate")),
    }
    full = {
        "target": pins.TARGET, "model": pins.model_pin(), "kernel_path": kernel_path(),
        "gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        "device_map": {"one_gpu": "cuda", "split": a.device_map}, "split": split, "edit_gpu": edit_gpu,
        "prompts": {"file": f"data/suite_v1/{FAMILY}.json", "n": len(items), "sample_seed": SEED,
                    "ids": [c["id"] for c in items]},
        "layers": {"record": list(RECORD), "edit": EDIT, "lens": EDIT if "lens" in report else None,
                   "lens_name": pins.FROZEN_LENS},
        "tolerance": {"logits_max_abs": TOL, "record_rel": RECORD_REL_TOL, "effect_min_median": EFFECT_MIN},
        "checks": checks, "all_ok": all(checks.values()),
        "conditions": report, "texts": {"one_gpu": [r["texts"] for r in one], "split": [r["texts"] for r in two]},
        "seconds": timings, "peak_gib": {"one_gpu": peak_one, "split": peak_gib()},
    }  # fmt: skip
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(full, indent=2) + "\n")
    summary = {c: {k: v for k, v in report[c].items() if k != "per_prompt"} for c in LOGIT_CONDITIONS if c in report}
    print(json.dumps({"checks": checks, "split": split, "conditions": summary, "records": report["records"],
                      "texts_equal": report["texts_equal"]}, indent=1))  # fmt: skip
    print("wrote", out / "report.json")
    return 0 if full["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
