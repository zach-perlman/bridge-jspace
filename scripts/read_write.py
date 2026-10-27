"""read_write: can the J-lens read the bridge where the model carries it, and can its direction write it? (Zach,
2026-10-20: quick experiment L4 before the sprint plan.)

On the cases of suite_split's map_A8_v1 (animal suite, wording A) and control_split's map_v1 (countries R, B), at
Qwen3.6-27B's window (layers 32, 36, 40; another target: --layers, each a layer its frozen lens has a map at) on the
question tokens:
  read   the J-lens readout (the target's frozen lens, pins.FROZEN_LENS: J++ on Qwen, the J-lens on OLMo; recorded in
         the manifest with its layers) of the clean run: the bridge's best rank among word tokens over the question
         positions (formatting tokens removed; any single-token surface of the bridge counts), per layer; the same
         for X (the counterfactual bridge, absent from the clean prompt) as the floor
  write  add the lens direction v_X - v_I (unit lens vectors of X and the bridge I, their difference rescaled per
         position to the norm of C's copy delta there, times 1 or 4) at the question tokens, one layer at a time and
         at all three at once; controls: a random direction at the same norms, and C's full copy itself
Scored by suite_split's answer read (frac of the way to C; flips). n per family: up to 60 cases (the first in each
map's case order). Descriptive: no verdict rule; it decides whether read-vs-write enters the sprint plan.

python scripts/read_write.py --name N --why W    (writes results/read_write/N)
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from scripts import control_split as C
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import AddRows, null_rows

RESULTS = pins.RESULTS_DIR / "read_write"
LAYERS = (32, 36, 40)
N_PER_FAMILY = 60
SCALES = (1.0, 4.0)


def suite_cases(
    tok, n: int, map_run: str = "map_A8_v1", wording: str = "A", families: list[str] | None = None
) -> list[dict]:
    rows = [json.loads(line) for line in (P.RESULTS / map_run / "cases.jsonl").read_text().splitlines()]
    rows = [r for r in rows if families is None or r["family"] in families]
    items = {f: {it["id"]: it for it in S.load(f, wording)} for f in {r["family"] for r in rows}}
    seen: collections.Counter = collections.Counter()
    out = []
    for r in rows:
        if seen[r["family"]] >= n:
            continue
        seen[r["family"]] += 1
        it = items[r["family"]][r["id"]]
        out.append({**it, **P.prepare(it, tok)})
    return out


def suite_cases_from_competence(tok, n: int, comp_run: str, families: list[str]) -> list[dict]:
    """The first n items per family with every prompt right in a suite_v1 competence run (no map run needed: a new
    target); items whose C or O does not line up token for token in this tokenizer are skipped."""
    ok: dict[str, list[bool]] = collections.defaultdict(list)
    for line in (S.RESULTS / comp_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        ok[r["id"]].append(r["correct"])
    out = []
    for fam in families:
        got = 0
        for it in S.load(fam):
            if got >= n or not ok.get(it["id"]) or not all(ok[it["id"]]):
                continue
            try:
                out.append({**it, **P.prepare(it, tok)})
                got += 1
            except AssertionError:
                continue
    return out


def tasks_cases(tok, n: int, set_name: str, comp_run: str, words: list[str], level: str = "pick",
                per_word: bool = False) -> list[dict]:  # fmt: skip
    """The first n items per word of a tasks_v2 set made with counterfactuals, from scenes its competence run got
    right on every prompt of the compared words, at one level for the comparison (tasks_v2.eligible). A scene with an
    item whose C or O does not line up in this tokenizer is dropped whole (its words stay paired) and the next scene
    takes its place; generation checks alignment with the same tokenizer, so any drop is reported."""
    from bridge_jspace.tokens import concept_token
    from scripts import tasks_v2 as T

    scenes: dict[str, list[dict]] = collections.defaultdict(list)
    for it in T.eligible(set_name, comp_run, words, 10**9, level, per_word=per_word):
        if "cf_context" not in it:  # knock-out tier items have no C or O (a merged set like full_v8); 2026-10-21
            continue
        scenes[it["scene"]].append(it)
    out, got, dropped = [], collections.Counter(), 0
    for its in scenes.values():
        its = [
            it for it in its if got[it["word"]] < n
        ]  # 2026-10-21: words still short (a full word no longer skips its scene)
        if not its:
            continue
        try:
            prepped = [{**it, **T.prepare(it, tok)} for it in its]
            for c in prepped:  # 2026-10-22: the lens writes need a single-token bridge surface (Muse: 'iota' has none)
                concept_token(tok, c["bridge"]), concept_token(tok, c["cf_bridge"])
        except (AssertionError, ValueError):
            dropped += 1
            continue
        out += prepped
        got.update(it["word"] for it in its)
    print(f"tasks_cases: {len(out)} cases from {len(out) and len({c['scene'] for c in out})} scenes; {dropped} scenes "
          "dropped (C/O alignment, first tokens or no single-token bridge)", flush=True)  # fmt: skip
    return out


def country_cases(tok, n: int, map_run: str = "map_v1") -> list[dict]:
    picked = [json.loads(line)["id"] for line in (C.RESULTS / map_run / "cases.jsonl").read_text().splitlines()]
    items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(items)}
    seen: collections.Counter = collections.Counter()
    out = []
    for uid in picked:
        index, item = by_uid[uid]
        if seen[item["family"]] >= n:
            continue
        seen[item["family"]] += 1
        prep = E.prepare(item, index, tok, "chat_prefill")
        c = {**item, **prep, "id": uid, "scene": uid, "cf_bridge": item["target"], "cf_answer": item["target_answer"],
             "answer_kind": "word"}  # fmt: skip
        c["read_ids"] = c["ids"]
        c["tok_A"], c["tok_b"] = (S.answer_token(tok, a, "word") for a in (item["answer"], item["target_answer"]))
        out.append(c)
    return out


@torch.no_grad()
def main(
    name: str,
    why: str,
    n: int,
    map_run: str = "map_A8_v1",
    wording: str = "A",
    countries: bool = True,
    country_map: str = "map_v1",
    families: list[str] | None = None,
    comp_run: str | None = None,
) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)  # the target's prefix; "_raw" iff BJ_FORMAT=raw
    pins.check_lens_layers(LAYERS)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    sources = (
        [S.RESULTS / comp_run / "items.jsonl"]
        if comp_run
        else [P.RESULTS / map_run / "cases.jsonl", C.RESULTS / country_map / "cases.jsonl"]
    )
    inputs = {p: sha256_of(p) for p in sources}
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "lens_layers": pins.LENS_LAYERS, "layers": list(LAYERS),
                "scales": list(SCALES), "n_per_family": n, "doc": (__doc__ or "").split("\n\n")[1],
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): s for p, s in inputs.items()}}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    if comp_run:  # a new target: cases from its competence run; countries from exp09's eligibility (generated here)
        cases = suite_cases_from_competence(tok, n, comp_run, families or ["BL", "BR", "RL", "RR"])
        cases += C.build_cases(model, tok, n)[0] if countries else []
    else:
        cases = suite_cases(tok, n, map_run, wording, families) + (
            country_cases(tok, n, country_map) if countries else []
        )
    print(len(cases), "cases", flush=True)
    reads, outcomes = [], []
    for k, c in enumerate(cases):
        P.unedited_ld(model, c)
        pos = c["groups"]["question"]
        h = {s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=LAYERS)[1] for s in ("clean", "cf")}
        i_tok, x_tok = model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])
        i_ids, x_ids = model.surface_ids(c["bridge"]), model.surface_ids(c["cf_bridge"])
        jobs: list[tuple[dict, dict]] = []
        band: dict[str, dict[int, AddRows]] = collections.defaultdict(dict)
        for la in LAYERS:
            logits = lens.readout(h["clean"][la][pos], la)
            ri = min(model.word_rank(row, i_ids) for row in logits) if i_ids else None
            rx = min(model.word_rank(row, x_ids) for row in logits) if x_ids else None
            reads.append({"family": c["family"], "name": c["id"], "layer": la, "rank_bridge": ri, "rank_x": rx})
            delta = h["cf"][la][pos] - h["clean"][la][pos]
            norms = delta.norm(dim=-1, keepdim=True)
            v = lens.vectors(la, torch.tensor([i_tok, x_tok], device="cuda"))
            direction = torch.nn.functional.normalize(v[1] - v[0], dim=-1).expand_as(delta)
            gen = torch.Generator(device="cuda").manual_seed(10_000 * k + la)
            edits = {"copy": delta}
            for sc in SCALES:
                edits[f"lens_x{sc:g}"] = sc * norms * direction
                edits[f"random_x{sc:g}"] = null_rows(sc * norms * direction, gen)
            for pname, vec in edits.items():
                jobs.append(({"layer": la, "part": pname, "source": "cf", "null": False}, {la: AddRows(vec, pos)}))
                band[pname][la] = AddRows(vec, pos)
        for pname, e in band.items():
            jobs.append(({"layer": "band", "part": pname, "source": "cf", "null": False}, dict(e)))
        P.read_jobs(model, c, jobs, outcomes)
        if (k + 1) % 100 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "reads.jsonl", reads)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary: dict = {"families": {}, "seconds": round(time.time() - t0)}
    for fam in dict.fromkeys(c["family"] for c in cases):
        rd = [r for r in reads if r["family"] == fam]
        best: dict[str, int] = {}
        best_x: dict[str, int] = {}
        for r in rd:
            if r["rank_bridge"] is not None:
                best[r["name"]] = min(best.get(r["name"], 10**9), r["rank_bridge"])
            if r["rank_x"] is not None:
                best_x[r["name"]] = min(best_x.get(r["name"], 10**9), r["rank_x"])
        write = {}
        for mode in ("single", "band"):
            rows = [o for o in outcomes if o["family"] == fam and (o["layer"] == "band") == (mode == "band")]
            for pname in dict.fromkeys(o["part"] for o in rows):
                sel = [o for o in rows if o["part"] == pname]
                write[f"{mode}/{pname}"] = {"frac": statistics.mean(o["frac"] for o in sel),
                                            "flips": statistics.mean(o["role"] == "b" for o in sel)}  # fmt: skip
        summary["families"][fam] = {
            "n": len(best),
            "read_top10": statistics.mean(v <= 10 for v in best.values()) if best else None,
            "read_top1": statistics.mean(v <= 1 for v in best.values()) if best else None,
            "median_rank": statistics.median(best.values()) if best else None,
            "x_top10": statistics.mean(v <= 10 for v in best_x.values()) if best_x else None,
            "write": write,
        }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = ["| family | n | lens reads bridge (top-10 / top-1) | X top-10 (floor) | copy | lens x1 | lens x4 | random x4 | "
             "lens x4, all 3 layers | copy, all 3 layers |", "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for fam, s in summary["families"].items():
        w = s["write"]

        def f(key, w=w):
            return f"{100 * w[key]['frac']:.0f}% ({100 * w[key]['flips']:.0f}%)" if key in w else "-"

        lines.append(f"| {fam} | {s['n']} | {100 * s['read_top10']:.0f}% / {100 * s['read_top1']:.0f}% | "
                     f"{100 * s['x_top10']:.0f}% | {f('single/copy')} | {f('single/lens_x1')} | {f('single/lens_x4')} | "
                     f"{f('single/random_x4')} | {f('band/lens_x4')} | {f('band/copy')} |")  # fmt: skip
    lines += ["", f"Write cells: mean frac of the way to C (flips), single layers averaged over {list(LAYERS)}.", "",
              "Strength sweep (single layers): lens direction | random direction, frac (flips), per scale", "",
              "| family | " + " | ".join(f"x{sc:g}" for sc in SCALES) + " |", "|---" * (len(SCALES) + 1) + "|"]  # fmt: skip
    for fam, s in summary["families"].items():
        w = s["write"]
        cells = []
        for sc in SCALES:
            lw, rw = w.get(f"single/lens_x{sc:g}"), w.get(f"single/random_x{sc:g}")
            cells.append(f"{100 * lw['frac']:.0f}% ({100 * lw['flips']:.0f}%) / {100 * rw['frac']:.0f}% ({100 * rw['flips']:.0f}%)"
                         if lw and rw else "-")  # fmt: skip
        lines.append(f"| {fam} | " + " | ".join(cells) + " |")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=N_PER_FAMILY, help="cases per family (a smoke run: few)")
    ap.add_argument("--map", default="map_A8_v1", help="suite_split map run whose cases to use")
    ap.add_argument("--wording", default="A", choices=["A", "B", "C"])
    ap.add_argument("--no-countries", action="store_true")
    ap.add_argument("--country-map", default="map_v1", help="control_split map run whose country cases to use")
    ap.add_argument("--families", nargs="+", default=None, help="suite families to include (default: all in the map)")
    ap.add_argument("--layers", nargs="+", type=int, default=list(LAYERS))
    ap.add_argument("--scales", nargs="+", type=float, default=list(SCALES))
    ap.add_argument("--from-competence", default=None, help="suite_v1 competence run to take cases from (no map run)")
    args = ap.parse_args()
    LAYERS, SCALES = tuple(args.layers), tuple(args.scales)
    main(
        args.name,
        args.why,
        args.n,
        args.map,
        args.wording,
        not args.no_countries,
        args.country_map,
        args.families,
        args.from_competence,
    )
