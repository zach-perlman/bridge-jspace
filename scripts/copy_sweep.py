"""copy_sweep: where do the question / final positions carry the bridge? (Zach, 2026-10-21: the overnight steering runs
showed that copying C's state at the question or final positions at one layer of 28-40 moves only 2-67% of answers, so
the steering sites may not carry the bridge.) For each case: C's residual difference pasted at the question positions or
the final position, (single) at one layer, (from) at that layer and every later swept layer (every --step); flips to C's answer.
Diagnostic: it locates the layers where those positions carry the bridge; no rule.

python scripts/copy_sweep.py --name N --why W [--tasks SET --tasks-competence RUN --families ...] [--n 40] [--step 2]
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import read_write as RW
from scripts import suite_split as P
from scripts.exp04_brew_parts import AddRows
from scripts.write_max import entity_ci

RESULTS = pins.RESULTS_DIR / "copy_sweep"


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    layers = tuple(range(args.step, pins.N_LAYERS - 1, args.step))
    (out_dir / "manifest.json").write_text(json.dumps({
        "run": args.name, "why": args.why, "git_commit": commit, "model": pins.model_pin(), "layers": list(layers),
        "tasks": [args.tasks, args.tasks_competence], "families": args.families, "n_per_family": args.n,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "doc": (__doc__ or "").split("\n\n")[1]},
        indent=2) + "\n")  # fmt: skip
    if args.tasks:
        cases = RW.tasks_cases(tok, args.n, args.tasks, args.tasks_competence, args.families, "all")
    else:
        cases = RW.suite_cases(tok, args.n, "map_A8_v1", "A", args.families)
    t0, outcomes = time.time(), []
    for k, c in enumerate(cases):
        P.unedited_ld(model, c)
        hs = {s: model.run(torch.tensor([c["read_ids"][s]], device="cuda"), record=layers)[1] for s in ("clean", "cf")}
        sites = {"question": c["groups"]["question"], "final": [len(c["read_ids"]["clean"]) - 1]}
        jobs = []
        for pos_name, pos in sites.items():
            delta = {la: hs["cf"][la][pos] - hs["clean"][la][pos] for la in layers}
            for la in layers:
                jobs.append(({"pos": pos_name, "mode": "single", "layer": la}, {la: AddRows(delta[la], pos)}))
                jobs.append(({"pos": pos_name, "mode": "from", "layer": la},
                             {m: AddRows(delta[m], pos) for m in layers if m >= la}))  # fmt: skip
        start = len(outcomes)
        P.read_jobs(model, c, jobs, outcomes)
        for o in outcomes[start:]:
            o["bridge"] = c["bridge"]
        if (k + 1) % 20 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    (out_dir / "outcomes.jsonl").write_text("".join(json.dumps(o) + "\n" for o in outcomes))
    cell: dict = collections.defaultdict(list)
    for o in outcomes:
        cell[(o["family"], o["pos"], o["mode"], o["layer"])].append(o)
    fams = list(dict.fromkeys(c["family"] for c in cases))
    summary: dict = {"seconds": round(time.time() - t0), "flips": {}}
    lines = [f"# copy_sweep / {args.name}: flips to C's answer % when C's state is pasted at the question / final "
             f"positions (single layer | that layer and every later one)", ""]  # fmt: skip
    for pos in ("question", "final"):
        lines += [f"## {pos} positions", "", "| family | " + " | ".join(f"L{la}" for la in layers) + " |",
                  "|---" * (len(layers) + 1) + "|"]  # fmt: skip
        for fam in fams:
            row = []
            for la in layers:
                v = {m: statistics.mean(o["role"] == "b" for o in cell[(fam, pos, m, la)]) for m in ("single", "from")}
                summary["flips"][f"{fam}/{pos}/L{la}"] = v
                row.append(f"{100 * v['single']:.0f} \\| {100 * v['from']:.0f}")
            lines.append(f"| {fam} | " + " | ".join(row) + " |")
        lines.append("")
    best = {}
    for fam in fams:
        for pos in ("question", "final"):
            for la in layers:
                os_ = cell[(fam, pos, "from", la)]
                rate = statistics.mean(o["role"] == "b" for o in os_)
                if rate > best.get(fam, (0, None))[0]:
                    best[fam] = (rate, f"{pos}, from L{la}", entity_ci([(o["bridge"], o["role"] == "b") for o in os_]))
    summary["best_from"] = {f: {"flips": b[0], "site": b[1], "ci": b[2]} for f, b in best.items()}
    lines += ["Best 'from' copy per family: " + ", ".join(f"{f} {100 * b[0]:.0f}% ({b[1]})" for f, b in best.items())]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--families", nargs="+", default=None)
    ap.add_argument("--tasks", default=None)
    ap.add_argument("--tasks-competence", default=None)
    a = ap.parse_args()
    a.families = a.families or (["PP", "PM", "MP", "MM"] if a.tasks else ["BL", "BR", "RL", "RR"])
    main(a)
