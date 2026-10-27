"""lens_table: one table of lens quality over every lens we use, scored the way Zach's cards score his (Dan,
2026-10-22): the J++ recipe's own held-out evaluation (safety-research/jpp_lens@93f02cd `jpp_cli.py evaluate --items
held-out:0`; the readout-eval items the model answers right), pass@10 per eval and the macro (mean of the five evals),
item-weighted, best rank over the layers scored.

Numbers are recomputed from the recipe's per-layer rank files (eval_ranks*.csv), so every lens of a model is scored at
the same layers (the model's comparison set: the layers its lenses share), and a lens's number at every layer it has
and at Zach's C1 band (lens_check.py's bands) come from the same file. Sources, in order of preference per row:
results/lens_eval/<job>/ (scripts/lens_fit/lens_eval.py), the fit folders (results/lens_fit/<fit>/, the newest
<fit>_<stamp>/ for our J++ fit records, exp19's fit_v2), Zach's files on origin/zach/v8-breadth-1021 (read with git
show), and last his published card numbers. The item sets differ by model (each model answers different items right),
so compare lenses within a model; across models compare lens minus logit lens. A lens scored by its own fit's evaluate
(our J++ fits) can keep other items than the logit lens's lens_eval run, as each run grades the model itself: its
difference to the logit lens is then taken on the items both kept, and the table says so. The lens gate columns are
left for Dan to fill. Descriptive; nothing here is verified.

uv run python -m scripts.lens_table                                   # -> results/lens_table/<stamp>/table.md, table.json
uv run python -m scripts.lens_table figure results/lens_eval/<run>    # -> <run>/analysis-<stamp>/pass_at_10.png
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import subprocess
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path
from statistics import mean

REPO = Path(__file__).resolve().parents[1]
EVALS = ("association", "multihop", "multilingual", "poetry", "typo")  # the recipe's MACRO_EVALS
K = 10
ZACH_REF = "origin/zach/v8-breadth-1021"
LOGIT = "logit"

Rank = tuple[str, str, str, str, int, int]  # eval, lens, item, intermediate, layer, rank


@dataclass(frozen=True)
class Model:
    label: str
    hf: str
    compare: tuple[int, ...]  # the layers every lens of this model is scored at (the ones they share)
    band: tuple[int, int] | None = None  # Zach's C1 rule band (scripts/lens_fit/lens_check.py), inclusive


@dataclass(frozen=True)
class Row:
    model: str
    lens: str  # the name in the ranks files (the lens file's stem; "logit" for the logit lens)
    label: str
    kind: str  # "J++", "plain J-lens", "logit lens"
    source: str
    recipe: str
    files: tuple[str, ...] = ()  # candidate rank files, preferred first: repo-relative globs, or "zach:<path>"
    pooled: str | None = None  # the pooled lens of the same fit, scored in the same file
    published: dict = field(default_factory=dict)  # Zach's card / Hub numbers: per eval, "macro", "pooled", "layers"
    note: str = ""  # shown below the table, always
    pending: str = ""  # shown below the table while the row has no numbers


def r(lo: int, hi: int, step: int = 1) -> tuple[int, ...]:
    return tuple(range(lo, hi + 1, step))


MODELS = {
    "qwen3.6-27b": Model("Qwen3.6-27B", "Qwen/Qwen3.6-27B", r(0, 62), (32, 40)),
    "qwen3.5-9b": Model("Qwen3.5-9B", "Qwen/Qwen3.5-9B", r(0, 30), (16, 20)),
    "qwen3-32b": Model("Qwen3-32B", "Qwen/Qwen3-32B", r(16, 51), (32, 40)),  # our J++ fit's layers (h200_fit.py)
    "olmo-3-7b-instruct": Model("OLMo-3-7B-Instruct", "allenai/Olmo-3-7B-Instruct", r(0, 30, 3)),  # mhough's layers
    "gemma-4-31b-it": Model("Gemma 4 31B-it", "google/gemma-4-31B-it", r(0, 58), (30, 38)),
    "muse-glimmer-30b": Model("Muse Glimmer 30B", "meta-models/Muse-Glimmer-30B", r(0, 50)),
    "qwen3.5-122b": Model("Qwen3.5-122B-A10B (FP8)", "Qwen/Qwen3.5-122B-A10B-FP8", ()),
}
NP = "neuronpedia/jacobian-lens@e166deb5"
ZACH_DAY3 = "Zach, Day 3 plan, as relayed by the coordinator on 22 Oct (not in the committed docs/day3_plan_zach.md)"
MUSE_HUB = "zachperlman20/Muse-Glimmer-30B-jpp-lens@68ecd838 eval/eval_ranks_pass_at_k.csv (item-weighted, layers 0-50)"
ROWS = (
    # Qwen3.6-27B: scored by Zach in exp19 fit_v2 (17 Oct; same recipe evaluate, held-out:0, its own grading)
    Row("qwen3.6-27b", "Qwen3.6-27B_jpp_lens", "published J++", "J++", f"{NP} (sha256 bbef480b, = 9fa267f8)",
        "jpp_lens recipe (koayon/jpp-lenses), 64 WikiText prompts", ("results/exp19_fit_data/fit_v2/eval_ranks.csv",),
        note=f"Zach's lens_check: J++ - logit at the C1 band +0.30 ({ZACH_DAY3})."),
    Row("qwen3.6-27b", "Qwen3.6-27B_jacobian_lens_n1000", "published plain J-lens (n1000)", "plain J-lens",
        f"{NP} (sha256 1718c8c5, = 9fa267f8)", "plain J-lens, 1000 WikiText prompts",
        ("results/exp19_fit_data/fit_v2/eval_ranks.csv",)),
    Row("qwen3.6-27b", LOGIT, "logit lens", "logit lens", "-", "-", ("results/exp19_fit_data/fit_v2/eval_ranks.csv",)),
    # Qwen3.5-9B: Zach is scoring it (coordinator, 22 Oct); no spec here
    Row("qwen3.5-9b", "Qwen3.5-9B_jpp_lens", "published J++", "J++", f"{NP} (sha256 8cda12f7)",
        "jpp_lens recipe (koayon/jpp-lenses), 64 WikiText prompts",
        ("results/lens_check/qwen3.5-9b/eval_ranks*.csv", "zach:results/lens_check/qwen3.5-9b/eval_ranks.csv"),
        pending="Zach is scoring it (his lens_check writes results/lens_check/qwen3.5-9b/); no spec written here."),
    Row("qwen3.5-9b", LOGIT, "logit lens", "logit lens", "-", "-",
        ("results/lens_check/qwen3.5-9b/eval_ranks*.csv", "zach:results/lens_check/qwen3.5-9b/eval_ranks.csv"),
        pending="with the 9B's J++ (Zach)."),
    # Qwen3-32B
    Row("qwen3-32b", "Qwen3-32B_jacobian_lens", "published plain J-lens", "plain J-lens", f"{NP} (sha256 0af5ccf2)",
        "plain J-lens, 557 WikiText prompts (stopping threshold not reached)",
        ("results/lens_eval/qwen3_32b_lens_eval/eval_ranks*.csv",),
        pending="jobs/lens_eval/qwen3_32b_lens_eval.yaml (not enqueued)."),
    Row("qwen3-32b", "Qwen3-32B_jpp_lens", "Zach's J++ (32 prompts)", "J++", "Zach's fit (not published)",
        "J++ (jpp_lens@93f02cd), 32 WikiText prompts",
        ("results/lens_fit/qwen3_32b/eval_ranks.csv", "zach:results/lens_fit/qwen3_32b/eval_ranks.csv"), "pooled_lens",
        note=f"Zach's lens_check: J++ - logit at the C1 band +0.31 ({ZACH_DAY3}).",
        pending="ranks not on origin/zach/v8-breadth-1021 (his lens_check reads results/lens_fit/qwen3_32b/)."),
    Row("qwen3-32b", "Qwen3-32B_jpp_lens", "our J++ (64 prompts)", "J++",
        "ours (H200 fit, scripts/lens_fit/h200_fit.py; danorel/Qwen3-32B-jpp-lens@8d43d036, sha256 7d6856b6)",
        "J++ (jpp_lens@93f02cd), 64 WikiText prompts (2 shards x 32), layers 16-51",
        ("results/lens_fit/qwen3_32b_jpp64_*/eval_ranks*.csv",), "pooled_lens",
        note="Our J++ has layers 16-51 only (the fit's range), so it, the plain J-lens and the logit lens are compared "
        "on 16-51.",
        pending="no rank file in results/lens_fit/qwen3_32b_jpp64_<stamp>/ (the fit record)."),
    Row("qwen3-32b", LOGIT, "logit lens", "logit lens", "-", "-",
        ("results/lens_eval/qwen3_32b_lens_eval/eval_ranks*.csv", "results/lens_check/qwen3-32b/eval_ranks_logit.csv",
         "zach:results/lens_check/qwen3-32b/eval_ranks_logit.csv"),
        pending="jobs/lens_eval/qwen3_32b_lens_eval.yaml (not enqueued)."),
    # OLMo-3-7B-Instruct
    Row("olmo-3-7b-instruct", "olmo-3-7b-instruct", "mhough plain J-lens", "plain J-lens",
        "mhough/olmo3-jacobian-lenses@d15b6af0 (sha256 b847dbba)", "plain J-lens, 616 WikiText prompts, layers 0-30 every 3rd",
        ("results/lens_eval/olmo3_7b_instruct_lens_eval/eval_ranks*.csv",),
        pending="jobs/lens_eval/olmo3_7b_instruct_lens_eval.yaml (not enqueued)."),
    Row("olmo-3-7b-instruct", "Olmo-3-1025-7B_jacobian_lens", "neuronpedia plain J-lens (base model)", "plain J-lens",
        f"{NP} (sha256 0683d972)", "plain J-lens fit on Olmo-3-1025-7B (base), 568 WikiText prompts, layers 0-30",
        ("results/lens_eval/olmo3_7b_instruct_lens_eval/eval_ranks*.csv",),
        pending="jobs/lens_eval/olmo3_7b_instruct_lens_eval.yaml (not enqueued)."),
    Row("olmo-3-7b-instruct", "Olmo-3-7B-Instruct_jpp_lens", "our J++ (64 prompts)", "J++",
        "ours (jobs/lens_fit/olmo3_7b_instruct_jpp_fit.yaml; danorel/Olmo-3-7B-Instruct-jpp-lens@fd8f1d4e, sha256 "
        "6847cfb3)", "J++ (jpp_lens@93f02cd), 64 WikiText prompts, layers 0-30",
        ("results/lens_fit/olmo3_7b_instruct_jpp_*/eval_ranks*.csv",), "pooled_lens",
        pending="no rank file in results/lens_fit/olmo3_7b_instruct_jpp_<stamp>/ (the fit record, publish_lens.py)."),
    Row("olmo-3-7b-instruct", LOGIT, "logit lens", "logit lens", "-", "-",
        ("results/lens_eval/olmo3_7b_instruct_lens_eval/eval_ranks*.csv",),
        pending="jobs/lens_eval/olmo3_7b_instruct_lens_eval.yaml (not enqueued)."),
    # Gemma 4 31B-it
    Row("gemma-4-31b-it", "gemma-4-31B-it_jpp_lens", "Zach's J++ (every layer)", "J++",
        "zachperlman20/gemma-4-31B-it-jpp-lens@c3c4340e (sha256 d16d81d8)",
        "J++ (jpp_lens@93f02cd), 64 WikiText prompts, layers 0-58",
        ("zach:results/lens_fit/gemma_it_full/eval_ranks.csv",), "pooled_lens",
        {"macro": 0.6327429643527205, "pooled": 0.502753600058478, "layers": "0-58", "source": "card"},
        note=f"Scored by Zach before the fp16 export. His lens_check: J++ - logit at the C1 band +0.35 ({ZACH_DAY3})."),
    Row("gemma-4-31b-it", "gemma-4-31B_jpp_lens", "neuronpedia J++ (base model)", "J++", f"{NP} (sha256 ef50bc54)",
        "jpp_lens recipe (koayon/jpp-lenses) on google/gemma-4-31B (base), 64 WikiText prompts",
        ("results/lens_eval/gemma4it_lens_eval/eval_ranks*.csv",),
        note="Earlier score at layers 24-45 every 3rd only: macro .376 "
        "(results/lens_fit/gemma_it_refit/eval_ranks_baselens_pass_at_k.csv).",
        pending="jobs/lens_eval/gemma4it_lens_eval.yaml (not enqueued)."),
    Row("gemma-4-31b-it", LOGIT, "logit lens", "logit lens", "-", "-",
        ("results/lens_eval/gemma4it_lens_eval/eval_ranks*.csv",
         "results/lens_check/gemma-4-31b-it-full/eval_ranks_logit.csv",
         "zach:results/lens_check/gemma-4-31b-it-full/eval_ranks_logit.csv"),
        pending="jobs/lens_eval/gemma4it_lens_eval.yaml (not enqueued)."),
    # Muse Glimmer 30B: Zach's Hub numbers only
    Row("muse-glimmer-30b", "Muse-Glimmer-30B_jpp_lens", "Zach's J++ (every layer)", "J++",
        "zachperlman20/Muse-Glimmer-30B-jpp-lens@68ecd838 (sha256 90fc5e52)",
        "J++ (jpp_lens@93f02cd + jpp_lens_muse_1022.patch), 32 WikiText prompts, layers 0-50",
        published={"association": 1.0, "multihop": 1.0, "multilingual": 0.8125, "poetry": 0.9807692307692307, "typo": 1.0,
                   "macro": 0.9586538461538462, "pooled": 0.8926095509428842, "layers": "0-50", "source": MUSE_HUB},
        note="Readout weights rest on 112 graded-correct items (his card)."),
    Row("muse-glimmer-30b", "Muse-Glimmer-30B_jacobian_lens", "eyes-ml plain J-lens", "plain J-lens",
        "eyes-ml/Muse-Glimmer-30B_jacobian-lens@71d8434f", "plain J-lens (neuronpedia fit_lens), 900 WikiText prompts "
        "(stop rule not reached)", ("results/lens_eval/muse30b_lens_eval/eval_ranks*.csv",),
        pending="not scored: the recipe's env on the A100 box (transformers 5.14.1) has no muse_glimmer, and Zach's "
        "jpp_lens_muse_1022.patch covers the loader and LRP only; Zach is scoring Muse (coordinator)."),
    Row("muse-glimmer-30b", LOGIT, "logit lens", "logit lens", "-", "-",
        published={"association": 0.6296296296296297, "multihop": 0.8888888888888888, "multilingual": 0.5148809523809523,
                   "poetry": 0.6538461538461539, "typo": 0.6623376623376623, "macro": 0.6699166574166574,
                   "layers": "0-50", "source": MUSE_HUB}),
    # Qwen3.5-122B-A10B
    Row("qwen3.5-122b", "Qwen3.5-122B-A10B_jpp_lens", "published J++", "J++", f"{NP} (sha256 b771e502)",
        "jpp_lens recipe (koayon/jpp-lenses), fit on the bf16 weights",
        pending="other box: the FP8 model needs an H200 / B200 (not on the A100 queue)."),
)  # fmt: skip


# ---------------------------------------------------------------- scoring


def pass_at_k(ranks: Iterable[Rank], layers: Iterable[int], k: int = K) -> dict[str, float]:
    """The recipe's item-weighted pass@k (lens_evals.readout_eval_scoring.pass_at_k_over_layers) for one lens: per
    (item, intermediate) the best rank over `layers`; per item the share of its intermediates with that rank <= k; per
    eval the mean over items; "macro" the mean over the five macro evals (absent if one is missing)."""
    keep = set(layers)
    best: dict[tuple[str, str, str], int] = {}
    for ev, _, item, inter, layer, rank in ranks:
        if layer in keep:
            key = (ev, item, inter)
            best[key] = min(best.get(key, rank), rank)
    per_item: dict[tuple[str, str], list[bool]] = defaultdict(list)
    for (ev, item, _), rank in best.items():
        per_item[(ev, item)].append(rank <= k)
    per_eval: dict[str, list[float]] = defaultdict(list)
    for (ev, _), hits in per_item.items():
        per_eval[ev].append(sum(hits) / len(hits))
    out = {ev: mean(v) for ev, v in per_eval.items()}
    if all(ev in out for ev in EVALS):
        out["macro"] = mean(out[ev] for ev in EVALS)
    return out


def read_ranks(text: str) -> list[Rank]:
    return [(d["eval"], d["lens"], d["item"], d["intermediate"], int(d["layer"]), int(float(d["rank"])))
            for d in csv.DictReader(io.StringIO(text))]  # fmt: skip


def zach_commit() -> str | None:
    p = subprocess.run(["git", "-C", str(REPO), "rev-parse", ZACH_REF], capture_output=True, text=True, check=False)
    return p.stdout.strip() or None


_CACHE: dict[str, list[Rank]] = {}


def load(location: str) -> dict[str, list[Rank]]:
    """{file: ranks} for one candidate location: a repo-relative glob, or "zach:<path>" on ZACH_REF (git show). A glob
    that matches several folders (fit records, <name>_<stamp>/) reads the newest one only (last by name), so two
    records of one fit are never pooled."""
    if location.startswith("zach:"):
        path = location.removeprefix("zach:")
        key = f"{ZACH_REF}:{path}"
        if key not in _CACHE:
            p = subprocess.run(["git", "-C", str(REPO), "show", key], capture_output=True, text=True, check=False)
            _CACHE[key] = read_ranks(p.stdout) if p.returncode == 0 else []
        return {key: _CACHE[key]} if _CACHE[key] else {}
    files = [f for f in sorted(REPO.glob(location)) if not f.name.endswith("_pass_at_k.csv")]
    newest = max((f.parent for f in files), default=None)
    out = {}
    for f in files:
        if f.parent != newest:
            continue
        key = str(f.relative_to(REPO))
        if key not in _CACHE:
            _CACHE[key] = read_ranks(f.read_text())
        out[key] = _CACHE[key]
    return out


def find(row: Row) -> tuple[list[str], list[Rank], list[Rank]]:
    """(files, the lens's ranks, the same files' ranks for its pooled lens) from the first location that has it."""
    for loc in row.files:
        files = load(loc)
        mine = [x for ranks in files.values() for x in ranks if x[1] == row.lens]
        if mine:
            pooled = [x for ranks in files.values() for x in ranks if row.pooled and x[1] == row.pooled]
            return sorted(files), dedupe(mine), dedupe(pooled)
    return [], [], []


def dedupe(ranks: list[Rank]) -> list[Rank]:
    """One rank per (eval, lens, item, intermediate, layer): a lens scored in two groups of a run (the logit lens)."""
    return list({x[:5]: x for x in ranks}.values())


def items_of(ranks: list[Rank]) -> frozenset[tuple[str, str]]:
    return frozenset((x[0], x[2]) for x in ranks if x[0] in EVALS)


def layers_text(layers: Iterable[int]) -> str:
    """Compact layer list: 0-62, 0-30 every 3rd, or the list."""
    ls = sorted(set(layers))
    if not ls:
        return "-"
    if len(ls) == 1:
        return str(ls[0])
    steps = {b - a for a, b in pairwise(ls)}
    if len(steps) == 1:
        (s,) = steps
        return f"{ls[0]}-{ls[-1]}" + ("" if s == 1 else f" every {s}{'rd' if s == 3 else 'th'}")
    return ",".join(map(str, ls))


def score_row(row: Row, logit: dict | None) -> dict:
    """The row's numbers (or why it has none). `logit` is the model's logit row, already scored, for the differences."""
    m = MODELS[row.model]
    files, ranks, pooled = find(row)
    rec: dict = {"model": m.label, "lens": row.label, "type": row.kind, "source": row.source, "recipe": row.recipe}
    if not ranks:
        if row.published:
            pub = row.published
            rec.update(status="published", files=[pub["source"]], layers=pub["layers"], items=None,
                       per_eval={ev: pub.get(ev) for ev in EVALS}, macro=pub.get("macro"), pooled=pub.get("pooled"))  # fmt: skip
            # the same published evaluation (one source, same layers) has the logit lens: same items
            if logit and logit.get("status") == "published" and logit["files"] == rec["files"] and row.lens != LOGIT:
                rec["d_logit"] = rec["macro"] - logit["macro"]
        else:
            rec.update(status="pending")
        return rec
    have = {x[4] for x in ranks}
    cmp_layers = sorted(set(m.compare) & have) or sorted(have)
    res = pass_at_k(ranks, cmp_layers)
    items = items_of(ranks)
    rec.update(status="scored", files=files, layers=layers_text(cmp_layers), layers_list=cmp_layers,
               missing_compare=sorted(set(m.compare) - have), items=len(items), items_set=items,
               per_eval={ev: res.get(ev) for ev in EVALS}, macro=res.get("macro"),
               macro_all=pass_at_k(ranks, have).get("macro"), all_layers=layers_text(have))  # fmt: skip
    if m.band and set(range(m.band[0], m.band[1] + 1)) <= have:
        rec["band_macro"] = pass_at_k(ranks, range(m.band[0], m.band[1] + 1)).get("macro")
    if pooled:
        rec["pooled"] = pass_at_k(pooled, cmp_layers).get("macro")
    elif row.published.get("pooled") is not None:
        rec["pooled"] = row.published["pooled"]
    if row.published.get("macro") is not None:
        rec["published_macro"] = f"{row.published['macro']:.3f} (layers {row.published['layers']})"
    if logit and logit.get("status") == "scored" and row.lens != LOGIT:
        mine, lr = ranks, logit["ranks"]
        shared = items & logit["items_set"]
        if shared != items or shared != logit["items_set"]:
            # a lens scored by its own fit's evaluate (our J++ fits) can keep other items than the logit lens's run:
            # the two runs graded the model separately (model_correctness.csv); compare on the items both kept
            mine = [x for x in ranks if (x[0], x[2]) in shared]
            lr = [x for x in lr if (x[0], x[2]) in shared]
            rec["shared_items"] = len(shared)
            rec["vs_logit"] = (f"items differ from the logit lens's run (graded separately: {len(items)} here, "
                               f"{logit['items']} there, {len(shared)} shared); compared on the shared items")  # fmt: skip

        def both(layers: Iterable[int]) -> tuple[float | None, float | None]:
            return pass_at_k(mine, layers).get("macro"), pass_at_k(lr, layers).get("macro")

        lr_layers = {x[4] for x in lr}
        a, b = both(cmp_layers)
        if a is not None and b is not None and set(cmp_layers) <= lr_layers:
            rec.update(d_logit=a - b, macro_same=a, logit_same=b)
        common = sorted(have & lr_layers)
        a, b = both(common)
        if a is not None and b is not None and common != cmp_layers:  # every layer both lenses have
            rec.update(d_logit_common=a - b, common_layers=layers_text(common), macro_common=a, logit_common=b)
        if rec.get("band_macro") is not None and m.band:
            a, b = both(range(m.band[0], m.band[1] + 1))
            rec["d_logit_band"] = None if a is None or b is None else a - b
    if row.lens == LOGIT:
        rec["ranks"] = ranks
    return rec


# ---------------------------------------------------------------- table


def f3(v) -> str:
    return "" if v is None else f"{v:.3f}"


def signed(v) -> str:
    return "" if v is None else f"{v:+.3f}"


def build() -> tuple[list[dict], list[str]]:
    recs: list[dict] = []
    for key in MODELS:
        rows = [row for row in ROWS if row.model == key]
        logit_row = next((row for row in rows if row.lens == LOGIT), None)
        logit = score_row(logit_row, None) if logit_row else None
        for row in rows:
            rec = logit if row is logit_row else score_row(row, logit)
            assert rec is not None
            rec["row"] = row
            recs.append(rec)
    head = ["model", "lens", "type", "source", "recipe, prompts", "layers scored", "items", *EVALS, "**macro**",
            "macro − logit", "macro, every layer it has", "C1 band macro (− logit)", "pooled macro",
            "published macro", "gate v1", "gate v2", "numbers from"]  # fmt: skip
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    notes: list[str] = []
    for i, rec in enumerate(recs, 1):
        row: Row = rec["row"]
        status = rec["status"]
        if status == "pending":
            cells = [rec["model"], f"{rec['lens']} [{i}]", rec["type"], rec["source"], rec["recipe"], "", "",
                     *[""] * len(EVALS), "**pending**", "", "", "", "", "", "", "", ""]  # fmt: skip
        else:
            m = MODELS[row.model]
            band = ""
            if rec.get("band_macro") is not None:
                band = f"{rec['band_macro']:.3f}" + (
                    f" ({signed(rec.get('d_logit_band'))})" if "d_logit_band" in rec else ""
                )
            items = "" if rec.get("items") is None else str(rec["items"])
            every = "" if status != "scored" else f"{f3(rec['macro_all'])} ({rec['all_layers']})"
            if "d_logit_common" in rec:
                every += f"; − logit at {rec['common_layers']}: {signed(rec['d_logit_common'])}"
            vs = signed(rec.get("d_logit"))
            if vs and "shared_items" in rec:
                vs += f" on the {rec['shared_items']} shared items ({f3(rec['macro_same'])} vs {f3(rec['logit_same'])})"
            cells = [rec["model"], f"{rec['lens']} [{i}]", rec["type"], rec["source"], rec["recipe"], rec["layers"],
                     items, *[f3(rec["per_eval"][ev]) for ev in EVALS], f"**{f3(rec['macro'])}**",
                     vs or rec.get("vs_logit", ""), every,
                     band or ("-" if m.band is None else ""), f3(rec.get("pooled")) or ("n/a" if row.kind == "J++" else "-"),
                     rec.get("published_macro", ""), "", "", "; ".join(rec["files"])]  # fmt: skip
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
        extra = [row.note] if row.note else []
        if rec.get("vs_logit"):
            extra.append(f"{rec['vs_logit'][0].upper()}{rec['vs_logit'][1:]}.")
        if status == "pending" and row.pending:
            extra.append(f"Pending: {row.pending}")
        if rec.get("missing_compare"):
            extra.append(f"Not scored at the comparison layers {layers_text(rec['missing_compare'])}.")
        if status == "published":
            extra.append("Card / Hub numbers, not recomputed here (no rank file in this repo).")
        if extra:
            notes.append(f"[{i}] " + " ".join(extra))
    return recs, [*lines, "", *notes]


def write_table(out_root: Path | None = None) -> Path:
    recs, body = build()
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    out = (out_root or REPO / "results" / "lens_table") / stamp
    out.mkdir(parents=True, exist_ok=False)
    zc = zach_commit()
    cmp = "; ".join(f"{m.label} {layers_text(m.compare) if m.compare else '-'}" for m in MODELS.values())
    bands = "; ".join(f"{m.label} {m.band[0]}-{m.band[1]}" for m in MODELS.values() if m.band)
    text = [
        "# Lens quality: every lens we use, scored as Zach's cards score his",
        "",
        "Held-out readout evals of the J++ recipe (safety-research/jpp_lens@93f02cd, `jpp_cli.py evaluate --items "
        "held-out:0`): pass@10 per eval and the macro (mean of the five), item-weighted, best rank over the layers "
        "scored, on the items each model answers right. Recomputed here from the per-layer rank files "
        "(scripts/lens_table.py). Descriptive, single fits, no CIs; UNVERIFIED.",
        "",
        f"- Layers scored = the model's comparison set (the layers its lenses share): {cmp}.",
        f"- C1 band = Zach's lens_check bands (scripts/lens_fit/lens_check.py): {bands}; '-' where none is defined.",
        "- macro − logit: minus the logit lens on the same items and layers (the item sets differ by model, so across "
        "models compare this, not the macro). Where a lens was scored by its own fit's evaluate and that run kept other "
        "items than the logit lens's run (each grades the model itself), both are scored on the items both kept, and the "
        "cell gives that count and the two macros. 'macro, every layer it has' adds the difference at every layer the "
        "lens and the logit lens both have where that differs from the layers scored. pooled macro: the recipe's pooled "
        "lens of the same fit, the baseline on Zach's cards; n/a for published J++ (no pooled lens is published); '-' "
        "for J-lenses and the logit lens.",
        "- gate v1 / v2: lens gate results, for Dan to fill.",
        f"- Zach's files read from {ZACH_REF} at {zc or 'NOT FETCHED (git fetch origin zach/v8-breadth-1021)'}.",
        "",
        *body,
        "",
    ]
    (out / "table.md").write_text("\n".join(text))
    keep = ("model", "lens", "type", "source", "recipe", "status", "files", "layers", "items", "per_eval", "macro",
            "d_logit", "shared_items", "macro_same", "logit_same", "macro_all", "all_layers", "d_logit_common",
            "common_layers", "macro_common", "logit_common", "band_macro", "d_logit_band", "pooled", "published_macro",
            "vs_logit")  # fmt: skip
    (out / "table.json").write_text(json.dumps({"zach_ref": zc, "rows": [{k: r_[k] for k in keep if k in r_}
                                                                          for r_ in recs]}, indent=1) + "\n")  # fmt: skip
    print("\n".join(text))
    return out


# ---------------------------------------------------------------- one run's figure


def figure(run: Path) -> Path:
    """pass@10 per eval for every lens of a lens_eval run, at the layers they all share, into <run>/analysis-<stamp>/."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    from bridge_jspace import plotting as P

    manifest = json.loads((run / "manifest.json").read_text())
    ranks = dedupe([x for f in sorted(run.glob("eval_ranks*.csv")) if not f.name.endswith("_pass_at_k.csv")
                    for x in read_ranks(f.read_text())])  # fmt: skip
    by_lens: dict[str, list[Rank]] = defaultdict(list)
    for x in ranks:
        by_lens[x[1]].append(x)
    lenses = [n for n in manifest["lenses"] if n in by_lens] + ([LOGIT] if LOGIT in by_lens else [])
    shared = sorted(set.intersection(*({x[4] for x in by_lens[n]} for n in lenses)))
    scores = {n: pass_at_k(by_lens[n], shared) for n in lenses}
    n_items = {ev: len({x[2] for x in by_lens[lenses[0]] if x[0] == ev}) for ev in EVALS}
    groups = [*EVALS, "macro"]
    colors = ["#2a78d6", "#eb6834", "#1baf7a"]  # the reference palette's first three slots (validated all-pairs)
    color = {n: (P.MUTED if n == LOGIT else colors[i]) for i, n in enumerate(lenses)}
    fig, ax = plt.subplots(figsize=(9, 5.4))
    P.style_axes(ax)
    width = 0.8 / len(lenses)
    for j, n in enumerate(lenses):
        xs = [g + (j - (len(lenses) - 1) / 2) * width for g in range(len(groups))]
        vals = [scores[n].get(g, 0.0) for g in groups]
        ax.bar(xs, vals, width=width - 0.03, color=color[n], edgecolor=P.SURFACE, linewidth=1)
        ax.annotate(f"{vals[-1]:.2f}", (xs[-1], vals[-1]), xytext=(0, 2), textcoords="offset points", ha="center",
                    va="bottom", fontsize=8, color=P.INK)  # fmt: skip
    ax.set_xticks(
        range(len(groups)), [f"{g}\n(n={n_items[g]})" if g in n_items else "macro\n(mean of 5)" for g in groups]
    )
    ax.set_ylim(0, 1.08)
    P.percent_axis(ax)
    ax.set_ylabel("pass@10 (held-out items)", color=P.MUTED, fontsize=9)
    model = manifest["model"]["hf_model_name"]
    handles = [Patch(color=color[n], label="logit lens (baseline)" if n == LOGIT else n) for n in lenses]
    explain = [
        ("What we did", "The J++ recipe's own readout eval (jpp_lens@93f02cd evaluate, held-out:0): for each held-out "
         "item the model answers right, the share of its intermediates (the bridge, the corrected word, ...) that are "
         "among the lens's top 10 tokens at some layer scored; averaged over the eval's items."),
        ("How to read", "Higher is better. Bars of one group are the same items; macro is the mean of the five evals, "
         "as on Zach's cards. Compare lenses within this model only."),
        ("Control", "The logit lens (grey) on the same items and layers."),
        ("Data", f"{model}; layers {layers_text(shared)} (shared by every lens here); one fit per lens, no CIs."),
    ]  # fmt: skip
    out = run / f"analysis-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}"
    out.mkdir(parents=True, exist_ok=False)
    P.finish(fig, out / "pass_at_10.png", f"Which lens names the intermediate on {model.split('/')[-1]}?", "",
             handles=handles, ncols=len(handles), explain=explain)  # fmt: skip
    (out / "summary.json").write_text(json.dumps({"layers": shared, "items": n_items, "pass_at_10": scores}, indent=1))
    print(f"figure -> {out / 'pass_at_10.png'}")
    return out


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    fg = sub.add_parser("figure", help="pass@10 per eval for one results/lens_eval/<run>/")
    fg.add_argument("run", type=Path)
    args = ap.parse_args(argv)
    if args.cmd == "figure":
        figure(args.run)
    else:
        write_table()


if __name__ == "__main__":
    main()
