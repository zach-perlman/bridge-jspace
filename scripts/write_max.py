"""write_max: the strongest lens-based write we can make, before any "the lens cannot write X" claim (Zach, 2026-10-20;
Phase 1d of the breadth plan). On read_write's cases (suite map_A8_v1, countries map_v1), at the transit layers one at
a time and all at once, on three position sets, with three ways to write X's lens direction in place of the bridge I's:

  positions   question (the question's tokens after C's changed ones, through the end: read_write's set), final (the
              answer-reading position only), all (every position of the prompt, the context statements included)
  additive    alpha x the residual's norm x unit(v_X - v_I), alpha in {0.05, 0.1, 0.2, 0.4, 0.8} (natural_rw's scale)
  swap        swap the residual's coefficients on v_I and v_X (least squares in their span), times 1, 2, 4
  transplant  the J-space part of C's residual in place of the clean one's (25-atom OMP over the lens dictionary,
              ablate's omp_fit, TF32), times 1, 2
  copy        C's whole residual difference (the lens-free reference: how much the position set can move the answer)
Controls: every lens-based write with each row replaced by a random direction of the same norm (null_rows).
Scored by suite_split's answer read: flips (top token = X's answer) and frac (share of the way to C).
Rule (fixed before the run, breadth plan v2): C2 holds if M->P's (RL) maximum lens flips over every position set x
write x layer x strength is <= its control's maximum + 5 points, while M->M's (RR) is >= 4x its control's maximum.

python scripts/write_max.py --name N --why W [--n 60] [--families BL BR RL RR] [--layers 32 34 36 38 40]
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
from bridge_jspace.ablate import LensDictionary, omp_fit
from scripts import read_write as RW
from scripts import suite_split as P
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import AddRows, null_rows

RESULTS = pins.RESULTS_DIR / "write_max"
ALPHAS = (0.05, 0.1, 0.2, 0.4, 0.8)
SWAPS = (1.0, 2.0, 4.0)
TRANSPLANTS = (1.0, 2.0)


def swap_delta(h: torch.Tensor, vi: torch.Tensor, vx: torch.Tensor) -> torch.Tensor:
    """For rows h [P, d]: the change that swaps their least-squares coefficients on unit vi and vx."""
    V = torch.stack([vi, vx]).double()  # [2, d]
    coefs = torch.linalg.solve(V @ V.T, V @ h.double().T).T  # [P, 2]
    return ((coefs[:, :1] - coefs[:, 1:]) * (vx - vi).double()).float()


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    torch.backends.cuda.matmul.allow_tf32 = True
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    layers = tuple(args.layers)
    manifest = {"run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "git_commit": commit, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "layers": list(layers), "alphas": list(ALPHAS), "swaps": list(SWAPS), "transplants": list(TRANSPLANTS),
                "families": args.families, "countries": args.countries, "n_per_family": args.n, "tf32": True,
                "tasks": [args.tasks, args.tasks_competence],
                "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    if args.tasks:
        cases = RW.tasks_cases(tok, args.n, args.tasks, args.tasks_competence, args.families, args.tasks_level)
    else:
        cases = RW.suite_cases(tok, args.n, "map_A8_v1", "A", args.families)
        cases += RW.country_cases(tok, args.n) if args.countries else []
    print(len(cases), "cases", flush=True)
    t0 = time.time()
    outcomes: list[dict] = []
    for k, c in enumerate(cases):
        P.unedited_ld(model, c)
        n_tok = len(c["read_ids"]["clean"])
        possets = {"question": c["groups"]["question"], "final": [n_tok - 1], "all": list(range(n_tok))}
        h = {s: model.run(torch.tensor([c["read_ids"][s]], device="cuda"), record=layers)[1] for s in ("clean", "cf")}
        vecs = {la: lens.vectors(la, torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])],
                                                  device="cuda")) for la in layers}  # fmt: skip
        jobs: list[tuple[dict, dict]] = []
        joint: dict[tuple, dict[int, AddRows]] = collections.defaultdict(dict)
        gen = torch.Generator(device="cuda").manual_seed(20_000 + k)

        def add(tags: dict, la: int, pos: list[int], delta: torch.Tensor, jobs=jobs, joint=joint) -> None:
            jobs.append(({**tags, "layer": la}, {la: AddRows(delta, pos)}))
            joint[tuple(sorted(tags.items()))][la] = AddRows(delta, pos)

        for pset, pos in possets.items():
            for la in layers:
                hc, hx = h["clean"][la][pos], h["cf"][la][pos]
                vi, vx = vecs[la][0], vecs[la][1]
                add({"pos": pset, "write": "copy", "strength": 1.0, "control": False}, la, pos, hx - hc)
                writes = {}
                direction = torch.nn.functional.normalize(vx - vi, dim=-1)
                for a in ALPHAS:
                    writes[("additive", a)] = a * hc.norm(dim=-1, keepdim=True) * direction
                sd = swap_delta(hc, vi, vx)
                for b in SWAPS:
                    writes[("swap", b)] = b * sd
                td = omp_fit(dic[la], hx, 25) - omp_fit(dic[la], hc, 25)
                for b in TRANSPLANTS:
                    writes[("transplant", b)] = b * td
                for (name, s), delta in writes.items():
                    add({"pos": pset, "write": name, "strength": s, "control": False}, la, pos, delta)
                    add({"pos": pset, "write": name, "strength": s, "control": True}, la, pos, null_rows(delta, gen))
        for key, edits in joint.items():
            jobs.append(({**dict(key), "layer": "joint"}, dict(edits)))
        P.read_jobs(model, c, jobs, outcomes)
        if (k + 1) % 20 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)

    summary: dict = {"seconds": round(time.time() - t0), "families": {}}
    lines = [f"# write_max / {args.name}: {len(cases)} cases, layers {list(layers)} and all at once", "",
             "Best flips (%) over layers x strengths: lens write / its random control; copy = the lens-free reference.", ""]  # fmt: skip
    for fam in dict.fromkeys(c["family"] for c in cases):
        rows = [o for o in outcomes if o["family"] == fam]
        cell = collections.defaultdict(list)
        for o in rows:
            cell[(o["pos"], o["write"], o["strength"], o["layer"], o["control"])].append(o["role"] == "b")
        rate = {k: statistics.mean(v) for k, v in cell.items()}
        fam_sum: dict = {"n": len({o["name"] for o in rows}), "best": {}}
        lines += [
            f"## {fam} (n={fam_sum['n']})",
            "",
            "| positions | copy | additive | swap | transplant |",
            "|---|---|---|---|---|",
        ]
        for pset in ("question", "final", "all"):
            cells = [f"{100 * max(v for k, v in rate.items() if k[0] == pset and k[1] == 'copy'):.0f}"]
            for w in ("additive", "swap", "transplant"):
                lens_best = max(v for k, v in rate.items() if k[0] == pset and k[1] == w and not k[4])
                ctrl_best = max(v for k, v in rate.items() if k[0] == pset and k[1] == w and k[4])
                fam_sum["best"][f"{pset}/{w}"] = {"lens": lens_best, "control": ctrl_best}
                cells.append(f"{100 * lens_best:.0f} / {100 * ctrl_best:.0f}")
            lines.append(f"| {pset} | " + " | ".join(cells) + " |")
        fam_sum["max_lens"] = max(v for k, v in rate.items() if k[1] != "copy" and not k[4])
        fam_sum["max_control"] = max(v for k, v in rate.items() if k[1] != "copy" and k[4])
        fam_sum["max_copy"] = max(v for k, v in rate.items() if k[1] == "copy")
        lines += ["", f"max over everything: lens {100 * fam_sum['max_lens']:.0f}%, control {100 * fam_sum['max_control']:.0f}%, "
                  f"copy {100 * fam_sum['max_copy']:.0f}%", ""]  # fmt: skip
        summary["families"][fam] = fam_sum
    fams = summary["families"]
    rl, rr = fams.get("RL", fams.get("MP")), fams.get("RR", fams.get("MM"))  # M->P and M->M (suite or tasks_v2 names)
    if rl and rr:
        summary["rule"] = {"RL_lens_le_control_plus_5": rl["max_lens"] <= rl["max_control"] + 0.05,
                           "RR_lens_ge_4x_control": rr["max_lens"] >= 4 * max(rr["max_control"], 0.01)}  # fmt: skip
        lines += [f"Rule: {json.dumps(summary['rule'])}"]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--families", nargs="+", default=["BL", "BR", "RL", "RR"])
    ap.add_argument("--layers", nargs="+", type=int, default=[32, 34, 36, 38, 40])
    ap.add_argument("--no-countries", dest="countries", action="store_false")
    ap.add_argument(
        "--tasks",
        help="a tasks_v2 set made with --counterfactuals (instead of the suite and countries); "
        "--families are then its words, e.g. PP PM MP MM",
    )
    ap.add_argument("--tasks-competence", help="the set's competence run (items right on every prompt are used)")
    ap.add_argument("--tasks-level", default="pick", help='tasks_v2 level: "pick" (calibrated), "all" or a number')
    main(ap.parse_args())
