"""x53_lastconflict (batch 53, test 53.3; jobs/c3/batch53.yaml, the rule fixed in Dan's brief of 29 Oct 09:30 before any
run; no prediction): the conflict test at the last token.

Items: 51.10's (x51_jread.select: the main test's items of the target's X0 run at L, x47_cumulative.select, with P1 / P2
/ P3 per reader), restricted to 49.1's locker-first items as 51.10's write arms; the source run's gate (X0's: 0.80 per
reader on O unedited, >= 150 eligible) asserted. Both readers (lookup PP, recall PM), X0's chat read (the prompt with a
digit's space token appended); P3 = the last token, the appended space (whose next token is the answer).

Layers, per reader: 51.10's read-peak layer (results/x51_jread/<51.10 run>/peak.json) and the answer layer minus 2 (the
answer layer = 51.10's read: per reader the lower median over the locker-first items of the layer from which O's answer
is the logit lens's top token at P3; results/x51_jread/read-<run>-*/read.json, the newest).

The change: Δ = h_S - h_O at P3 at the layer (each reader's own S and O prompts; the readers' prompts differ at P3). The
lens part P_J Δ = its 25 J++ atoms (X0's signed OMP over the letter-token J++ dictionary at the layer, x49_gain.
lens_parts); the random part R Δ = X0's random subspace part at the lens part's share (seed 888 + layer). Arms, each
added at P3 at the layer on O (AddRows), each read: none; whole (Δ); no_jpp ("without the lens part": Δ - P_J Δ);
no_rand ("without a random part of the same share": Δ - R Δ); jpp ("the lens part alone": P_J Δ); rest ("the rest
alone": Δ - P_J Δ, the same vector as no_jpp in this additive patch, read separately and reported under the brief's
name). Switch = the top token over the vocabulary is S's answer's first token.

Rule per reader and layer (Dan's brief, batch 53.3): "computes outside the lens at the last token" if the loss without
the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss
is >= 0.30 beyond random; else "in between". As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) /
S_whole (S_arm = the share of the items switched under the arm); the rest alone's share = S_rest / S_whole; point
estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs over the original bridge entities (10,000, seed 0, paired:
the same draws for every arm) beside; S_whole = 0: "not tested (the whole change switches no item)". X0's validity bar
(S_whole >= 0.30 and >= 30 switches) reported beside, not in the rule.

No prediction, not sealed: the run writes the reads; `verdict` (CPU) writes results/x53_lastconflict/x53_lastconflict-
<UTC>/ (verdict.md, verdict.json, a figure, examples.md: 10 random items, seed 0). UNVERIFIED.

BJ_TARGET=qwen3.5-9b uv run python scripts/x53_lastconflict.py plan                       # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_lastconflict.py run --name qwen35_9b_x53_3 # GPU
uv run python scripts/x53_lastconflict.py verdict --runs qwen35_9b_x53_3                  # CPU
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x49_gain as G
from scripts import x51_jread as JR

EXP = "x53_lastconflict"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
TEST = "53.3"
NO_PREDICTION = "no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)"
SOURCE_RUNS = {**JR.RUNS, **JR.COVERAGE_RUNS}  # 51.10's runs: the read peak and the answer layer
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_3", "qwen3.6-27b": "x53_3_27b", "muse-glimmer-30b": "muse30_x53_3",
        "nemotron-3.5-lightning": "nem35l_x53_3"}  # fmt: skip
READERS, READER_NAME = X.READERS, JR.READER_NAME
RENDERING = G.RENDERING
K = X.K_MAIN  # 25
ARMS = ("none", "whole", "no_jpp", "no_rand", "jpp", "rest")
ARM_TEXT = {"none": "O unedited", "whole": "the whole change Δ = h_S - h_O at P3",
            "no_jpp": "without the lens part: Δ - P_J Δ", "no_rand": "without a random part of the same share: Δ - R Δ",
            "jpp": "the lens part alone: P_J Δ", "rest": "the rest alone: Δ - P_J Δ (the same vector as no_jpp)"}  # fmt: skip
OUTSIDE_MAX, REST_MIN, THROUGH_MIN = 0.10, 0.7, 0.30
EPS = 1e-9
LABELS = {"outside": "computes outside the lens at the last token", "through": "through the lens",
          "between": "in between", "untested": "not tested (the whole change switches no item)"}  # fmt: skip
RULE = (f"per reader and layer: \"{LABELS['outside']}\" if the loss without the lens part is <= 0.10 beyond random and "
        f"the rest alone switches >= 0.7 of the whole; \"{LABELS['through']}\" if the loss is >= 0.30 beyond random; "
        f"else \"{LABELS['between']}\"")  # fmt: skip
AS_COMPUTED = ("the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / "
               "S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); "
               "point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities "
               f"({X.N_BOOT}, seed {X.BOOT_SEED}, paired) beside; S_whole = 0: not tested")  # fmt: skip


# ---- layers and items (CPU) ---------------------------------------------------------------------------------------


def layers_of(target: str) -> dict[str, Any]:
    """Per reader: 51.10's read-peak layer and its answer layer minus 2 (deduplicated, in order), with their sources."""
    run = SOURCE_RUNS[target]
    peak_file = JR.RESULTS / run / "peak.json"
    peaks = json.loads(peak_file.read_text())["peaks"]
    found = sorted(JR.RESULTS.glob(f"read-{run}-*/read.json"))
    assert found, f"no 51.10 read of {run} (results/x51_jread/read-{run}-*/read.json)"
    answer = json.loads(found[-1].read_text())["answer"]
    out: dict[str, Any] = {"source_run": run, "peak_file": str(peak_file.relative_to(pins.REPO_ROOT)),
                           "read_file": str(found[-1].relative_to(pins.REPO_ROOT)), "readers": {}}  # fmt: skip
    for w in READERS:
        name = READER_NAME[w]
        peak, ans = peaks[name], answer[name]["layer"]
        assert peak is not None, f"{run}: {name} has no read peak"
        assert ans is not None, f"{run}: {name} has no answer layer"
        layers = list(dict.fromkeys((int(peak), int(ans) - 2)))
        out["readers"][name] = {"peak": int(peak), "answer": int(ans), "layers": layers}
    return out


def select(tok, target: str) -> tuple[list[dict], dict]:
    """51.10's items (x51_jread.select) restricted to 49.1's locker-first ones (51.10's write arms)."""
    items, counts = JR.select(tok, target)
    lf = [it for it in items if it["lf"]]
    return lf, {**counts, "items_used": len(lf), "entities_used": len({it["entity"] for it in lf})}


def n_reads(lay: dict[str, Any]) -> int:
    """Reads per item: per reader O unedited plus every arm at each of its layers."""
    return sum(1 + len(r["layers"]) * (len(ARMS) - 1) for r in lay["readers"].values())


def stage_plan() -> dict:
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    lay = layers_of(target)
    items, counts = select(tok, target)
    blob = {"target": target, "run": RUNS[target], "layers": lay, "counts": counts,
            "gate": G.source_gate(G.SOURCES[target]), "reads": len(items) * n_reads(lay),
            "forwards_states": len(items) * 2 * 2}  # fmt: skip
    print(json.dumps(blob, indent=1))
    return blob


# ---- the parts and the run (GPU) ----------------------------------------------------------------------------------


def arm_vectors(delta, pj, rj) -> dict[str, Any]:
    """The vectors the arms add at P3 (rows of Δ [n, d]); none adds nothing."""
    return {"whole": delta, "no_jpp": delta - pj, "no_rand": delta - rj, "jpp": pj, "rest": delta - pj}


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "53.3 reads X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"53.3 runs on {sorted(RUNS)}, not {target}"
    lay = layers_of(target)
    per_reader = {w: lay["readers"][READER_NAME[w]]["layers"] for w in READERS}
    all_layers = sorted({la for v in per_reader.values() for la in v})
    source = G.SOURCES[target]
    src = X.RESULTS / source
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, *(src / f for f in ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl")),
              pins.REPO_ROOT / lay["peak_file"], pins.REPO_ROOT / lay["read_file"]]  # fmt: skip
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": TEST,
         "spec": "jobs/c3/batch53.yaml (53.3)", "question": NO_PREDICTION,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs}, "source": source,
         "L": X.PREDICTED[target], "layers": lay, "k": K, "arms": ARM_TEXT, "rule": RULE, "as_computed": AS_COMPUTED,
         "items_rule": "51.10's items (x51_jread.select), 49.1's locker-first ones (51.10's write arms)",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = the top token over the "
                 "vocabulary is S's answer's first token",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT, "sealed": "none (no prediction)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    gate = G.source_gate(source)
    assert G.gate_passes(gate), f"{source}: the gate fixed in advance does not pass ({gate})"
    model = load_model()
    lens = JLens(model, "jpp")
    missing = [la for la in all_layers if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at {missing}"
    tok = model.tokenizer
    items, counts = select(tok, target)
    assert items, "no locker-first items"
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    dev = model.device
    digits = torch.tensor(X.digit_ids(tok), device=dev)
    letters = model.letter_token_ids()
    d = int(model.hf.lm_head.weight.shape[1])
    n = len(items)
    with torch.no_grad():  # memory lesson 1: nothing built from the weights keeps a graph
        # 1. the states at P3 at each reader's layers (one forward per item, reader and O / S), copied to the CPU
        h = {(w, v): {la: torch.zeros(n, d) for la in per_reader[w]} for w in READERS for v in JR.VARIANTS}
        for i, it in enumerate(progress(items, "53.3: states at P3 (item: 2 readers x O / S)")):
            for w, rd in it["readers"].items():
                for v in JR.VARIANTS:
                    ids = torch.tensor([rd["ids"][v] + it["space"]], device=dev)
                    _, rec = model.run(ids, record=tuple(per_reader[w]))
                    p3 = it["jpos"][w]["P3"][v]
                    assert p3 == ids.shape[1] - 1, f"{it['scene']}: P3 is not the last token"
                    for la in per_reader[w]:
                        h[(w, v)][la][i] = rec[la][p3].float().cpu()  # a copy (memory lesson 2)
                    del rec
        # 2. the parts per layer (the J++ dictionary built and freed per layer)
        vecs: dict[tuple[str, int], dict[str, Any]] = {}
        norms = []
        for la in all_layers:
            jdic = lens.vectors(la, letters)
            basis = SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
            for w in READERS:
                if la not in per_reader[w]:
                    continue
                delta = (h[(w, "alt")][la] - h[(w, "org")][la]).to(dev)
                pj, rj = G.lens_parts(jdic, delta, K, basis)
                vecs[(w, la)] = {k: v.float().cpu().clone() for k, v in arm_vectors(delta, pj, rj).items()}
                sj, sr = G.share(pj, delta), G.share(rj, delta)
                norms += [{"scene": it["scene"], "reader": w, "layer": la, "norm_delta": round(float(delta[i].norm()), 4),
                           "share_J": round(float(sj[i]), 6), "share_rand": round(float(sr[i]), 6)}
                          for i, it in enumerate(items)]  # fmt: skip
            del jdic, basis
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        # 3. the reads: per item and reader, O unedited and every arm at each of the reader's layers (one batch list)
        rows = []
        for i, it in enumerate(progress(items, "53.3: reads (item: 2 readers x arms x layers)")):
            for w, rd in it["readers"].items():
                p3 = it["jpos"][w]["P3"]["org"]
                names = [(la, a) for la in per_reader[w] for a in ARMS[1:]]
                edits = [{}] + [{la: AddRows(vecs[(w, la)][a][i : i + 1].to(dev), [p3])} for la, a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], None)
                for (la, a), lg in zip([(None, "none"), *names], logits, strict=True):
                    rows.append({"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w,
                                 "layer": la, "arm": a, **X.read_row(lg, rd, digits),
                                 "top_text": model.decoded[int(lg.argmax())]})  # fmt: skip
        X.write_jsonl(out / "outcomes.jsonl", rows)
    print(f"wrote {out}: {len(rows)} reads of {n} items", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def label(excess: float, rest: float) -> str:
    """The brief's rule on one reader and layer (point estimates, EPS at the bars)."""
    if excess <= OUTSIDE_MAX + EPS and rest >= REST_MIN - EPS:
        return "outside"
    if excess >= THROUGH_MIN - EPS:
        return "through"
    return "between"


def cell_numbers(rows: list[dict], reader: str, layer: int, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One reader at one layer: each arm's switch rate (none: O unedited), the excess and the rest's share with paired
    cluster-bootstrap CIs over the bridge entities, the label."""
    by: dict[tuple[str, str], int] = {}
    ent: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader and (r["layer"] == layer or r["arm"] == "none"):
            by[(r["scene"], r["arm"])] = int(r["switched"])
            ent.setdefault(r["scene"], r["entity"])
    scenes = list(ent)
    missing = [(s, a) for s in scenes for a in ARMS if (s, a) not in by]
    assert not missing, f"{reader} L{layer}: {len(missing)} reads missing, e.g. {missing[:3]}"
    sw = {a: [by[(s, a)] for s in scenes] for a in ARMS}
    ents = [ent[s] for s in scenes]
    boot = X.resampled_rates(sw, ents, n_boot)
    rate = {a: float(np.mean(sw[a])) for a in ARMS}
    with np.errstate(divide="ignore", invalid="ignore"):
        ex_b = (boot["no_rand"] - boot["no_jpp"]) / boot["whole"]
        rest_b = boot["rest"] / boot["whole"]
    s_whole = rate["whole"]
    if s_whole <= 0:
        excess = rest = math.nan
        lab = "untested"
    else:
        excess = (rate["no_rand"] - rate["no_jpp"]) / s_whole
        rest = rate["rest"] / s_whole
        lab = label(excess, rest)
    return {"reader": READER_NAME[reader], "layer": layer, "n": len(scenes), "entities": len(set(ents)),
            "rates": {a: [rate[a], *X.interval(boot[a])] for a in ARMS},
            "switches_whole": int(sum(sw["whole"])), "excess": [excess, *X.interval(ex_b)],
            "rest_share": [rest, *X.interval(rest_b)], "label": lab, "text": LABELS[lab],
            "x0_valid": bool(s_whole >= X.VALID_S - EPS and sum(sw["whole"]) >= X.VALID_N),
            "rest_equals_no_jpp": sw["rest"] == sw["no_jpp"]}  # fmt: skip


def run_numbers(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cells = [cell_numbers(rows, w, la, n_boot) for w in READERS
             for la in m["layers"]["readers"][READER_NAME[w]]["layers"]]  # fmt: skip
    return {"run": run, "target": m["model"]["target"], "layers": m["layers"], "cells": cells}


def fmt(v: list) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def figure(models: list[dict], path: Path) -> None:
    """Per model a panel: per reader and layer each edit arm's switch rate with its 95% CI."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    arms = ARMS[1:]
    fig, axes = plt.subplots(1, len(models), figsize=(5.5 * len(models), 3.8), squeeze=False)
    for ax, mdl in zip(axes[0], models, strict=True):
        cells = mdl["cells"]
        width = 0.8 / len(arms)
        for j, a in enumerate(arms):
            xs = [i + (j - (len(arms) - 1) / 2) * width for i in range(len(cells))]
            ys = [c["rates"][a][0] for c in cells]
            err = [[max(0.0, c["rates"][a][0] - c["rates"][a][1]) for c in cells],
                   [max(0.0, c["rates"][a][2] - c["rates"][a][0]) for c in cells]]  # fmt: skip
            ax.bar(xs, ys, width, yerr=err, capsize=2, label=ARM_TEXT[a].split(":")[0])
        ax.set_xticks(range(len(cells)))
        ax.set_xticklabels([f"{c['reader']} L{c['layer']}\n{c['text'][:24]}" for c in cells], fontsize=7)
        ax.set_ylim(0, 1)
        ax.set_ylabel("switched to S's answer")
        ax.set_title(f"{mdl['target']} ({mdl['run']})", fontsize=9)
    axes[0][0].legend(fontsize=6)
    fig.suptitle("53.3: the conflict test at the last token (UNVERIFIED)", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items (seed 0): per reader its answers and every arm's top token per layer (the prompts as read are
    51.10's, marked in its plan)."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = X.read_jsonl(src / "outcomes.jsonl")
    pick = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    lines = [f"## {run}: {len(pick)} random items of {len(items)} (seed {seed})", ""]
    for i in pick:
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} → {it['cf_bridge']}", "",
                  f"O's context: {it.get('context', '-')}", "", f"S's context: {it.get('cf_context', '-')}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['question']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}",
                      "", "| layer | arm | top token | switched |", "|---|---|---|---|"]  # fmt: skip
            for r in reads:
                if r["scene"] == it["scene"] and r["reader"] == w:
                    lines.append(f"| {'-' if r['layer'] is None else r['layer']} | {r['arm']} | {r['top_text']!r} | "
                                 f"{r['switched']} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    models = [run_numbers(r, n_boot) for r in runs]
    out = RESULTS / f"x53_lastconflict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 53.3: the conflict test at the last token", "",
             f"Batch 53, test 53.3 (jobs/c3/batch53.yaml; {NO_PREDICTION}). The change at the last token (P3) at 51.10's "
             "read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.", "",
             f"Rule (Dan's brief): {RULE}.", "", f"As computed: {AS_COMPUTED}.", "",
             "| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | "
             "the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for mdl in models:
        for c in mdl["cells"]:
            info = mdl["layers"]["readers"][c["reader"]]
            why = "read peak" if c["layer"] == info["peak"] else f"answer L{info['answer']} - 2"
            r = c["rates"]
            lines.append(f"| {mdl['target']} | {c['reader']} | {c['layer']} ({why}) | {c['n']} ({c['entities']}) | "
                         f"{fmt(r['whole'])} | {fmt(r['no_jpp'])} | {fmt(r['no_rand'])} | {fmt(r['jpp'])} | "
                         f"{fmt(r['rest'])} | {fmt(c['excess'])} | {fmt(c['rest_share'])} | **{c['text']}** | "
                         f"{'yes' if c['x0_valid'] else 'no'} |")  # fmt: skip
    floors = "; ".join(f"{m['target']} {c['reader']} {fmt(c['rates']['none'])}" for m in models for c in m["cells"])
    sources = "; ".join(f"{m['target']}: {m['layers']['peak_file']}, {m['layers']['read_file']}" for m in models)
    lines += ["", f"O unedited switched (floor): {floors}.", "", f"Layer sources: {sources}.", "",
              "Figure: x53_lastconflict.png"]  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    (out / "verdict.json").write_text(json.dumps({"runs": runs, "question": NO_PREDICTION, "rule": RULE,
                                                  "as_computed": AS_COMPUTED, "models": models}, indent=1) + "\n")  # fmt: skip
    figure(models, out / "x53_lastconflict.png")
    ex = ["# 53.3 examples (verify pack): every arm's top token per layer for 10 random items per run. UNVERIFIED.", ""]
    for mdl in models:
        ex += example_lines(mdl["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x53_lastconflict/<name>/)")
    ap.add_argument("--runs", nargs="+", default=None, help="verdict: the runs (default: every one of RUNS here)")
    ap.add_argument("--why", default="batch 53, test 53.3 (jobs/c3/batch53.yaml)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        runs = a.runs or [r for r in RUNS.values() if (RESULTS / r / "outcomes.jsonl").exists()]
        stage_verdict(runs, a.n_boot)


if __name__ == "__main__":
    main()
