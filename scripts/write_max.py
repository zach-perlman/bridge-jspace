"""write_max v2: the strongest fair write we can make, before any "the lens cannot write X" claim (Zach, 2026-10-20;
Phase 1d of the breadth plan; v2 after the steering review the same evening, decided with Zach: a non-lens direction,
breakage gating, a contiguous band, an injection control and entity-clustered intervals).

Cases: suite map_A8_v1 (BL BR RL RR) and countries map_v1, or a tasks_v2 set made with counterfactuals (--tasks: PP PM
MP MM by default, compared at one level). Each case: the clean prompt with bridge I, its C prompt with bridge X.

Sites: position sets question (the question's tokens after C's changed ones, through the end), final (the answer-
reading position only), all (every position); layers: every --single-step-th layer of the band --band (28-40 by
default: where memory-final families break under the depth sweep), and every layer of the band at once ("joint").
Writes (each at every site, each with a matched-norm random control: every row replaced by a random direction of the
same norm):
  copy         C's whole residual difference (lens-free positive control: can this site move the answer at all?);
               2026-10-21: also at every band layer at once at the question / final positions (the ceiling)
  lens_add     alpha x |h| x unit(v_X - v_I), alpha in ALPHAS (v = unit J-lens vectors)
  lens_swap    swap the residual's least-squares coefficients on v_I and v_X, times SWAPS
  lens_transpl the J-space part of C's residual in place of the clean one's (25-atom OMP over the lens dictionary)
  dom_add      alpha x |h| x unit(mu_X - mu_I): mu_e = the mean clean residual (over the site's positions) of other
               cases whose bridge is e, from other scenes only (cross-fitted: the case's own scene is never used)
  dom_natural  (mu_X - mu_I) itself, times 1 and 2 (an in-distribution size)
Injection control (layers --early, question positions): lens_add and embed_add (alpha x |h| x unit(E_X - E_I), the
input-embedding difference: planting the token) at ALPHAS_EARLY. If embed_add flips as often as lens_add there, an
early "write" is the model re-reading an injected token, not a written bridge.
Scored by suite_split's answer read: role b (top token = C's answer), A (the clean answer), other.
Breakage gate: a cell (write x site x strength) counts only if its random control keeps the clean answer on >= 95% of
cases; every reported cell carries its "other" rate. Intervals: 95% bootstrap over bridge entities.

Rules (fixed before the run, 2026-10-20):
  C2 holds at the band if M->P's (RL / MP) best gated lens write (lens_add, lens_swap, lens_transpl; single or joint)
  flips <= its control + 5 points, while M->M's (RR / MM) flips >= 4x its control (and >= 10%).
  Reading of M->P's dom writes (only if C2 holds): dom flips >= its control + 20 points -> "linearly writable at these
  sites, but not along the lens"; dom within control + 5 and copy >= 50% -> "no single direction found here writes it
  (the copy does)"; copy < 50% -> "these sites do not carry M->P's bridge; look elsewhere".
  Injection: early lens_add's best flips within 10 points of embed_add's -> early lens writes are token injection.

A new target (BJ_TARGET; 2026-10-21, Gemma 4 31B-it): --from-competence takes the suite cases from its own competence
run and builds its country cases with the model; --layers gives the band's layers when the lens covers only some.

--writes (Zach, 2026-10-21): only these writes; "--writes copy" re-measures the ceiling (single-layer copies and the joint
paste) on the cases of a run made before 1330338, whose joint copy stacked (c2_graded --ceiling-from).

python scripts/write_max.py --name N --why W [--n 60] [--families ...] [--band 28-40] [--tasks SET --tasks-competence RUN]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
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
from bridge_jspace.run_switches import switches
from scripts import control_split as C
from scripts import read_write as RW
from scripts import suite_split as P
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import AddRows, SetRows, null_rows

RESULTS = pins.RESULTS_DIR / "write_max"
ALPHAS = (0.05, 0.1, 0.2, 0.4, 0.8)
ALPHAS_EARLY = (0.2, 0.4, 0.8, 1.6)
SWAPS = (1.0, 2.0, 4.0)
TRANSPLANTS = (1.0, 2.0)
NATURAL = (1.0, 2.0)
KEEP_GATE = 0.95
LENS_WRITES = ("lens_add", "lens_swap", "lens_transpl")


def swap_delta(h: torch.Tensor, vi: torch.Tensor, vx: torch.Tensor) -> torch.Tensor:
    """For rows h [P, d]: the change that swaps their least-squares coefficients on unit vi and vx."""
    V = torch.stack([vi, vx]).double()  # [2, d]
    coefs = torch.linalg.solve(V @ V.T, V @ h.double().T).T  # [P, 2]
    return ((coefs[:, :1] - coefs[:, 1:]) * (vx - vi).double()).float()


def entity_ci(flags: list[tuple[str, bool]], reps: int = 1000, seed: int = 0) -> tuple[float, float]:
    """95% bootstrap interval of a rate, resampling bridge entities (items sharing a bridge are not independent)."""
    by = collections.defaultdict(list)
    for e, f in flags:
        by[e].append(f)
    groups = list(by.values())
    rng = random.Random(seed)
    stats = sorted(
        sum(sum(g) for g in d) / sum(len(g) for g in d)
        for d in ([groups[rng.randrange(len(groups))] for _ in groups] for _ in range(reps))
    )
    return stats[int(0.025 * reps)], stats[int(0.975 * reps) - 1]


def pool_of(c: dict) -> str:
    return c.get("domain") or ("countries" if c["family"].startswith("country") else "suite")


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
    if args.layers:  # a lens fit at some layers only (Gemma: 24-45, every 3rd): the band is those layers
        band = tuple(sorted(args.layers))
    else:
        lo, hi = (int(x) for x in args.band.split("-"))
        band = tuple(range(lo, hi + 1))
    singles = band[:: args.single_step]
    early = tuple(args.early)
    rec_layers = tuple(sorted(set(band) | set(early)))
    manifest = {"run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "git_commit": commit, "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "band": list(band), "single_layers": list(singles), "early_layers": list(early), "possets": args.possets,
                "alphas": list(ALPHAS), "alphas_early": list(ALPHAS_EARLY), "swaps": list(SWAPS),
                "transplants": list(TRANSPLANTS), "natural": list(NATURAL), "keep_gate": KEEP_GATE,
                "families": args.families, "countries": args.countries, "n_per_family": args.n, "tf32": True,
                "tasks": [args.tasks, args.tasks_competence, args.tasks_level], "tasks_per_word": args.tasks_per_word, "from_competence": args.from_competence, "writes": args.writes,
                "doc": (__doc__ or "").split("\n\n", 1)[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    dic = {la: LensDictionary(wg, lens.J(la)) for la in band}
    emb = model.hf.get_input_embeddings().weight
    if args.tasks:
        cases = RW.tasks_cases(tok, args.n, args.tasks, args.tasks_competence, args.families, args.tasks_level,
                               args.tasks_per_word)  # fmt: skip
        assert cases, "no tasks_v2 cases"
    elif args.from_competence:  # a new target (no map run): its own competence run; countries built with this model
        cases = RW.suite_cases_from_competence(tok, args.n, args.from_competence, args.families)
        cases += C.build_cases(model, tok, args.n)[0] if args.countries else []
    else:
        cases = RW.suite_cases(tok, args.n, "map_A8_v1", "A", args.families)
        cases += RW.country_cases(tok, args.n) if args.countries else []
    print(len(cases), "cases", flush=True)
    t0 = time.time()

    def possets_of(c: dict) -> dict[str, list[int]]:
        n_tok = len(c["read_ids"]["clean"])
        sets = {"question": c["groups"]["question"], "final": [n_tok - 1], "all": list(range(n_tok))}
        return {k: v for k, v in sets.items() if k in args.possets}

    # pass 1: each case's clean residual, averaged over each site's positions, for the cross-fitted means mu_e
    site_mean: list[dict] = []
    for c in cases:
        h = model.run(torch.tensor([c["read_ids"]["clean"]], device="cuda"), record=rec_layers)[1]
        site_mean.append({(la, ps): h[la][pos].mean(0).cpu() for la in rec_layers for ps, pos in possets_of(c).items()})
    sums: dict = {}
    counts: collections.Counter = collections.Counter()
    for c, m in zip(cases, site_mean, strict=True):
        counts[(pool_of(c), c["bridge"])] += 1
        for key, v in m.items():
            k3 = (pool_of(c), c["bridge"], key)
            sums[k3] = sums[k3] + v if k3 in sums else v.clone()
    by_scene = collections.defaultdict(list)
    for i, c in enumerate(cases):
        by_scene[c.get("scene", c["id"])].append(i)

    def mu(e: str, key: tuple, c: dict) -> torch.Tensor | None:
        """Mean clean site residual of cases with bridge e in c's pool, c's own scene left out (None if < 2 left)."""
        pool = pool_of(c)
        own = [i for i in by_scene[c.get("scene", c["id"])] if cases[i]["bridge"] == e and pool_of(cases[i]) == pool]
        n = counts[(pool, e)] - len(own)
        if n < 2 or (pool, e, key) not in sums:
            return None
        s = sums[(pool, e, key)].clone()
        for i in own:
            s -= site_mean[i][key]
        return (s / n).cuda()

    outcomes: list[dict] = []
    check: list[dict] = []  # write_max --check-prefix (2026-10-22)
    dom_missing = 0
    for k, c in enumerate(cases):
        P.unedited_ld(model, c)
        hs = {
            s: model.run(torch.tensor([c["read_ids"][s]], device="cuda"), record=rec_layers)[1] for s in ("clean", "cf")
        }
        ti, tx = model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])
        vecs = {la: lens.vectors(la, torch.tensor([ti, tx], device="cuda")) for la in rec_layers}
        e_dir = torch.nn.functional.normalize((emb[tx] - emb[ti]).float(), dim=-1)
        jobs: list[tuple[dict, dict]] = []
        joint: dict[tuple, dict[int, AddRows | SetRows]] = collections.defaultdict(dict)
        gen = torch.Generator(device="cpu").manual_seed(20_000 + k)  # 2026-10-21: CPU draws, the same on any GPU

        def add(tags: dict, la: int, pos: list[int], delta: torch.Tensor, in_band: bool = True, jobs=jobs,
                joint=joint, gen=gen) -> None:  # fmt: skip
            """The write and its matched-norm random control at one layer (single-layer jobs at the band's single
            layers and at early layers); band layers also go into the joint (every band layer at once) edit."""
            for control, d in ((False, delta), (True, null_rows(delta, gen))):
                t = {**tags, "control": control}
                if not in_band or la in singles:
                    jobs.append(({**t, "layer": la}, {la: AddRows(d, pos)}))
                if in_band:
                    joint[tuple(sorted(t.items()))][la] = AddRows(d, pos)

        missing = False
        for pset, pos in possets_of(c).items():
            for la in band:
                hc, hx = hs["clean"][la][pos], hs["cf"][la][pos]
                vi, vx = vecs[la][0], vecs[la][1]
                norm = hc.norm(dim=-1, keepdim=True)
                tags = {"pos": pset}
                if la in singles:  # copy at single layers (at "all" positions this is C's whole run from there)
                    jobs.append(({**tags, "write": "copy", "strength": 1.0, "control": False, "layer": la},
                                 {la: AddRows(hx - hc, pos)}))  # fmt: skip
                if (
                    pset != "all"
                ):  # 2026-10-21 (Zach): the copy at every band layer at once, the ceiling for joint writes
                    key = tuple(sorted({**tags, "write": "copy", "strength": 1.0, "control": False}.items()))
                    joint[key][la] = SetRows(hx, pos)  # a paste: AddRows(hx - hc) at every layer stacks and overshoots
                lens_dir = torch.nn.functional.normalize(vx - vi, dim=-1)
                for a in ALPHAS:
                    add({**tags, "write": "lens_add", "strength": a}, la, pos, a * norm * lens_dir)
                sd = swap_delta(hc, vi, vx)
                for b in SWAPS:
                    add({**tags, "write": "lens_swap", "strength": b}, la, pos, b * sd)
                if not args.writes or "lens_transpl" in args.writes:  # the OMP fits are the slow part
                    td = omp_fit(dic[la], hx, 25) - omp_fit(dic[la], hc, 25)
                    for b in TRANSPLANTS:
                        add({**tags, "write": "lens_transpl", "strength": b}, la, pos, b * td)
                mx, mi = mu(c["cf_bridge"], (la, pset), c), mu(c["bridge"], (la, pset), c)
                if mx is None or mi is None:
                    missing = True
                    continue
                dom = (mx - mi).expand_as(hc)
                dom_dir = torch.nn.functional.normalize(dom, dim=-1)
                for a in ALPHAS:
                    add({**tags, "write": "dom_add", "strength": a}, la, pos, a * norm * dom_dir)
                for b in NATURAL:
                    add({**tags, "write": "dom_natural", "strength": b}, la, pos, b * dom)
        dom_missing += missing
        if "question" in possets_of(c):
            pos = possets_of(c)["question"]
            for la in early:
                hc = hs["clean"][la][pos]
                norm = hc.norm(dim=-1, keepdim=True)
                lens_dir = torch.nn.functional.normalize(vecs[la][1] - vecs[la][0], dim=-1)
                for a in ALPHAS_EARLY:
                    add({"pos": "question", "write": "early_lens_add", "strength": a}, la, pos, a * norm * lens_dir,
                        in_band=False)  # fmt: skip
                    add({"pos": "question", "write": "early_embed_add", "strength": a}, la, pos,
                        a * norm * e_dir.expand_as(hc), in_band=False)  # fmt: skip
        for key, edits in joint.items():
            jobs.append(({**dict(key), "layer": "joint"}, dict(edits)))
        if args.writes:
            jobs = [j for j in jobs if j[0]["write"] in args.writes]
        start = len(outcomes)
        pstart = min(min(e.positions) for _, ed in jobs for e in ed.values()) if (args.prefix_cache or args.check_prefix) else None
        if args.check_prefix:  # 2026-10-22: the prefix-cache path against the full runs, on the same jobs
            full, fast = [], []
            torch.cuda.synchronize(); t1 = time.time()
            P.read_jobs(model, c, jobs, full)
            torch.cuda.synchronize(); t2 = time.time()
            P.read_jobs(model, c, jobs, fast, prefix_start=pstart)
            torch.cuda.synchronize(); t3 = time.time()
            check.append({"case": c["id"], "prefix": pstart, "seq": len(c["read_ids"]["clean"]), "jobs": len(jobs),
                          "role_agree": sum(a["role"] == b["role"] for a, b in zip(full, fast, strict=True)),
                          "max_abs_dld": max(abs(a["ld"] - b["ld"]) for a, b in zip(full, fast, strict=True)),
                          "mean_abs_dld": statistics.mean(abs(a["ld"] - b["ld"]) for a, b in zip(full, fast, strict=True)),
                          "t_full": round(t2 - t1, 2), "t_prefix": round(t3 - t2, 2)})  # fmt: skip
            print(json.dumps(check[-1]), flush=True)
            if len(check) >= args.check_prefix:
                break
            continue
        P.read_jobs(model, c, jobs, outcomes, prefix_start=pstart)
        for o in outcomes[start:]:
            o["bridge"] = c["bridge"]
        if (k + 1) % 20 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    if args.check_prefix:
        agree = sum(x["role_agree"] for x in check) / sum(x["jobs"] for x in check)
        res = {"cases": check, "role_agreement": agree, "max_abs_dld": max(x["max_abs_dld"] for x in check),
               "seconds": time.time() - t0, "pass": agree >= 0.995}  # fmt: skip
        (out_dir / "prefix_check.json").write_text(json.dumps(res, indent=2) + "\n")
        print(f"prefix-cache check: role agreement {100 * agree:.2f}% over {sum(x['jobs'] for x in check)} jobs, max |dld| "
              f"{res['max_abs_dld']:.3f} -> {'PASS' if res['pass'] else 'FAIL'} (>= 99.5%)")  # fmt: skip
        return
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summarize(out_dir, args, cases, outcomes, dom_missing, time.time() - t0)


def summarize(out_dir: Path, args, cases: list[dict], outcomes: list[dict], dom_missing: int, seconds: float) -> None:
    """Per family and write: the best gated cell (over site, layer and strength), its control, other rate and an
    entity-clustered interval; then the pre-set rules."""
    summary: dict = {"seconds": round(seconds), "dom_missing_cases": dom_missing, "families": {}}
    lines = [f"# write_max v2 / {args.name}: {len(cases)} cases ({dom_missing} without a dom direction)", "",
             f"Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control "
             f"keeps the clean answer on >= {KEEP_GATE:.0%} of cases. [95% CI over bridge entities]", ""]  # fmt: skip
    for fam in dict.fromkeys(c["family"] for c in cases):
        rows = [o for o in outcomes if o["family"] == fam]
        cell: dict = collections.defaultdict(list)
        for o in rows:
            cell[(o["write"], o["pos"], str(o["layer"]), o["strength"], o["control"])].append(o)
        fam_sum: dict = {"n": len({o["name"] for o in rows}), "entities": len({o["bridge"] for o in rows}), "best": {}}
        lines += [f"## {fam} (n={fam_sum['n']}, {fam_sum['entities']} bridges)", "",
                  "| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |",
                  "|---|---|---|---|---|---|"]  # fmt: skip
        for write in dict.fromkeys(k[0] for k in cell):
            best, n_cells = None, 0
            for (w, pos, la, s, control), os_ in cell.items():
                if w != write or control:
                    continue
                ctrl = cell.get((w, pos, la, s, True))
                if write != "copy" and (not ctrl or statistics.mean(o["role"] == "A" for o in ctrl) < KEEP_GATE):
                    continue
                n_cells += 1
                flips = statistics.mean(o["role"] == "b" for o in os_)
                if best is None or flips > best[0]:
                    best = (flips, pos, la, s, os_, ctrl)
            if best is None:
                fam_sum["best"][write] = None
                lines.append(f"| {write} | - (no cell passes the gate) | | | | 0 |")
                continue
            flips, pos, la, s, os_, ctrl = best
            ci = entity_ci([(o["bridge"], o["role"] == "b") for o in os_])
            c_rate = statistics.mean(o["role"] == "b" for o in ctrl) if ctrl else None
            other = statistics.mean(o["role"] == "other" for o in os_)
            fam_sum["best"][write] = {"flips": flips, "ci": ci, "control": c_rate, "other": other, "pos": pos,
                                      "layer": la, "strength": s, "gated_cells": n_cells}  # fmt: skip
            lines.append(f"| {write} | {100 * flips:.0f} [{100 * ci[0]:.0f}-{100 * ci[1]:.0f}] | "
                         f"{'-' if c_rate is None else f'{100 * c_rate:.0f}'} | {100 * other:.0f} | {pos}, {la}, {s:g} | "
                         f"{n_cells} |")  # fmt: skip
        lines.append("")
        summary["families"][fam] = fam_sum
    fams = summary["families"]

    def best_of(fam: str, writes: tuple) -> tuple[float, float] | None:
        got = [fams[fam]["best"][w] for w in writes if fams.get(fam, {}).get("best", {}).get(w)]
        if not got:
            return None
        b = max(got, key=lambda x: x["flips"])
        return b["flips"], b["control"] or 0.0

    mp = "RL" if "RL" in fams else "MP" if "MP" in fams else None
    mm = "RR" if "RR" in fams else "MM" if "MM" in fams else None
    if mp and mm and not args.writes:
        lp, lm = best_of(mp, LENS_WRITES), best_of(mm, LENS_WRITES)
        rule = {"MP_lens_le_control_plus_5": bool(lp and lp[0] <= lp[1] + 0.05),
                "MM_lens_ge_4x_control_and_10pct": bool(lm and lm[0] >= max(4 * lm[1], 0.10))}  # fmt: skip
        rule["C2_holds"] = rule["MP_lens_le_control_plus_5"] and rule["MM_lens_ge_4x_control_and_10pct"]
        dom, copy = best_of(mp, ("dom_add", "dom_natural")), best_of(mp, ("copy",))
        if rule["C2_holds"] and dom and copy:
            if dom[0] >= dom[1] + 0.20:
                rule["MP_dom_reading"] = "linearly writable at these sites, but not along the lens"
            elif dom[0] <= dom[1] + 0.05 and copy[0] >= 0.5:
                rule["MP_dom_reading"] = "no single direction found here writes it (the copy does)"
            elif copy[0] < 0.5:
                rule["MP_dom_reading"] = "these sites do not carry the bridge; look elsewhere"
            else:
                rule["MP_dom_reading"] = "dom between the thresholds: inconclusive"
        el, ee = best_of(mp, ("early_lens_add",)), best_of(mp, ("early_embed_add",))
        if el and ee:
            rule["MP_early_lens_is_injection"] = abs(el[0] - ee[0]) <= 0.10
        summary["rule"] = rule
        lines += [f"Rules ({mp} vs {mm}): {json.dumps(rule)}"]
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--families", nargs="+", default=None, help="default: BL BR RL RR (suite) or PP PM MP MM (--tasks)")
    ap.add_argument("--band", default="28-40", help="contiguous layers written jointly; singles every --single-step")
    ap.add_argument("--layers", nargs="+", type=int, default=None, help="explicit band layers (instead of --band)")
    ap.add_argument("--single-step", type=int, default=2)
    ap.add_argument("--early", nargs="+", type=int, default=[16, 20, 24], help="layers of the injection control")
    ap.add_argument("--possets", nargs="+", default=["question", "final", "all"], choices=["question", "final", "all"])
    ap.add_argument("--no-countries", dest="countries", action="store_false")
    ap.add_argument("--tasks", help="a tasks_v2 set made with --counterfactuals (instead of the suite and countries)")
    ap.add_argument("--tasks-competence", help="the set's competence run (scenes right on every prompt are used)")
    ap.add_argument("--tasks-level", default="pick", help='tasks_v2 level: "pick" (per comparison), "all" or a number')
    ap.add_argument("--tasks-per-word", action="store_true", help="tasks_v2: judge each item on its own (three-step)")
    ap.add_argument("--from-competence", default=None, help="a new target: suite_v1 competence run to take cases from")
    ap.add_argument("--writes", nargs="+", default=None, help='only these writes (e.g. "copy": the ceiling alone)')
    ap.add_argument("--prefix-cache", action="store_true", help="2026-10-22: reuse the unedited prompt prefix (needs a passing --check-prefix run for the model)")
    ap.add_argument("--check-prefix", type=int, default=0, help="2026-10-22: compare the prefix-cache path with full runs on N cases, then stop")
    a = ap.parse_args()
    a.families = a.families or (["PP", "PM", "MP", "MM"] if a.tasks else ["BL", "BR", "RL", "RR"])
    main(a)
