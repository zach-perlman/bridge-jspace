"""ablate_v2: the J-space knock-out, version 2 (Zach, 2026-10-21). Removals and controls are in
src/bridge_jspace/ablate.py (decided with Zach on 2026-10-21); one model load runs every band x condition on every
prompt, sharing the unedited forward. TF32 is on for the OMP's matmuls (benchmark 2026-10-21: 5.1x, same atoms).

Plans (--plan):
  v1check   ablate_pilot v1's configuration (layers 32/36/40, the lens dictionary and v1's Gaussian random dictionary,
            v1's prompts) run with this code; compared item by item with results/ablate_pilot/v1
  depth     contiguous 3-layer bands sliding by 2 over layers 0 to n-2, and every one of those layers at once
  bands     the bands given with --bands, e.g. "32,36,40" "16-28"
Conditions (--conditions): omp25, omp25_rot, omp25_rdict, paper10, paper10_rot, paper10_rdict, keep_own, skip_subject,
  gauss (v1's Gaussian dictionary). Prompt kinds (--kinds): clean (the whole question), hop (the last step alone, as
  v1), step1/step2/step3 (each step alone). Reported per band x family/kind x condition: accuracy (top token = the
  answer's first token) and the mean change in the answer token's log-probability from the unedited run.

python scripts/ablate_v2.py --name N --why W --plan depth [--n 100] [--families BL BR RL RR R B] [--kinds clean]
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.ablate import (
    OWN_COS,
    LensDictionary,
    MatrixDictionary,
    RotatedDictionary,
    RowSettings,
    first_token_logits,
    removal_edit,
    rotation,
)
from scripts import ablate_pilot as A
from scripts import control_split as C
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl

RESULTS = pins.RESULTS_DIR / "ablate_v2"
COMPETENCE = {  # the 27B's competence runs per suite family (eligibility: every check right)
    "BL": "competence_v2", "BR": "competence_v2", "RL": "competence_v2", "RR": "competence_v2",
    "BLR": "competence_tiebreak_v1", "BRL": "competence_tiebreak_v1",
    "TYPO": "competence_computed_v1", "TRANS": "competence_computed_v1",
    "TBL": "competence_tool_v1", "TBR": "competence_tool_v1",
}  # fmt: skip
CONDITIONS = ("omp25", "omp25_rot", "omp25_rdict", "paper10", "paper10_rot", "paper10_rdict", "keep_own",
              "skip_subject", "gauss")  # fmt: skip
SEED_ROT, SEED_DICT, SEED_GAUSS = 888, 999, 777  # + layer (888 and 777 as ablate_pilot)


def suite_prompts(tok, fams: list[str], kinds: list[str], n: int, competence: dict[str, str]) -> list[dict]:
    out = []
    for fam in fams:
        good = A.eligible_ids(competence[fam], (fam,)).get(fam, set())
        got = 0
        for it in S.load(fam):
            if got >= n or it["id"] not in good:
                continue
            try:
                prep = P.prepare(it, tok)
            except AssertionError:  # C or O not aligned in this tokenizer (as v1)
                continue
            got += 1
            for kind in kinds:
                if kind == "clean":
                    out.append({"family": fam, "id": it["id"], "kind": "clean", "ids": prep["read_ids"]["clean"],
                                "tok": prep["tok_A"], "bridge": it["bridge"]})  # fmt: skip
                    continue
                key = ("hop3" if "hop3" in it else "hop2") if kind == "hop" else "hop" + kind.removeprefix("step")
                if key not in it:
                    continue
                hop = it[key]
                text = S.render(tok, hop.get("context", it["context"]), hop["question"])
                ids = S.ids(tok, text) + (S.ids(tok, " ") if hop["kind"] == "digit" else [])
                out.append({"family": fam, "id": it["id"], "kind": kind, "ids": ids,
                            "tok": S.answer_token(tok, hop["answer"], hop["kind"]), "bridge": it["bridge"]})  # fmt: skip
    return out


def country_prompts(tok, fams: list[str], n: int) -> list[dict]:
    """ablate_pilot v1's country prompts (map_v1's cases, chat_prefill), whole question only."""
    picked = [json.loads(line)["id"] for line in (C.RESULTS / "map_v1" / "cases.jsonl").read_text().splitlines()]
    items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(items)}
    seen: collections.Counter = collections.Counter()
    out = []
    for uid in picked:
        index, item = by_uid[uid]
        if item["family"] not in fams or seen[item["family"]] >= n:
            continue
        seen[item["family"]] += 1
        prep = E.prepare(item, index, tok, "chat_prefill")
        out.append({"family": f"country-{item['family']}", "id": uid, "kind": "clean", "ids": prep["ids"]["clean"],
                    "tok": S.answer_token(tok, item["answer"], "word"), "bridge": item["bridge"]})  # fmt: skip
    return out


def bridge_positions(tok, ids: list[int], word: str) -> list[int]:
    """Token positions overlapping a mention of the word (case-insensitive, any suffix: cow, cows, Cow)."""
    pieces = [tok.decode([i]) for i in ids]
    starts, pos = [], 0
    for p in pieces:
        starts.append(pos)
        pos += len(p)
    text = "".join(pieces)
    spans = [(m.start(), m.end()) for m in re.finditer(r"(?i)\b" + re.escape(word), text)]
    return [
        i
        for i, (s, p) in enumerate(zip(starts, pieces, strict=True))
        if any(s < e and s + len(p) > b for b, e in spans)
    ]


def make_bands(plan: str, n_layers: int, spec: list[str], workspace: int | None = None) -> list[tuple[int, ...]]:
    if plan == "v1check":
        return [(32, 36, 40)]
    if plan == "depth":
        top = n_layers - 2  # the last edited layer; the final block is the lens's target
        bands = [tuple(range(s, s + 3)) for s in range(0, top - 1, 2)]  # 3 contiguous layers, sliding by 2
        bands += [tuple(range(s, s + 9)) for s in range(0, top - 7, 4)]  # 9 contiguous layers, sliding by 4
        bands.append(tuple(range(0, top + 1)))  # every layer
        if workspace is not None:  # every layer from the first where the lens mostly stops reading the input token
            bands.append(tuple(range(workspace, top + 1)))
        return bands
    bands = []
    for b in spec:
        if "-" in b:
            lo, hi = map(int, b.split("-"))
            bands.append(tuple(range(lo, hi + 1)))
        else:
            bands.append(tuple(int(x) for x in b.split(",")))
    return bands


WIDE = 9  # bands wider than this run paper10 and its controls only (Zach, 2026-10-20: OMP at whole depth breaks
#           everything, its random controls too, so it says nothing there)


def conditions_for(band: tuple[int, ...], conditions: list[str]) -> list[str]:
    return [c for c in conditions if len(band) <= WIDE or c.startswith("paper10")]


def label(band: tuple[int, ...]) -> str:
    contiguous = band == tuple(range(band[0], band[-1] + 1))
    return f"L{band[0]}-{band[-1]}" if contiguous and len(band) > 1 else "L" + ",".join(map(str, band))


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    torch.backends.cuda.matmul.allow_tf32 = not args.no_tf32
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    bands = make_bands(args.plan, pins.N_LAYERS, args.bands, args.workspace)
    manifest = {"run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "git_commit": commit, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "plan": args.plan, "bands": [label(b) for b in bands], "conditions": args.conditions,
                "families": args.families, "kinds": args.kinds, "n_per_family": args.n, "batch": args.batch,
                "tf32": not args.no_tf32, "workspace_start": args.workspace, "wide": WIDE, "seeds": {"rotation": f"{SEED_ROT}+layer", "rotated_dictionary": f"{SEED_DICT}+layer",
                "gauss": f"{SEED_GAUSS}+layer"}, "own_cos": OWN_COS, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    suite_fams = [f for f in args.families if f in COMPETENCE]
    if args.plan == "v1check":  # exactly v1's prompts
        prompts = [
            dict(p)
            for p in A.prompts(tok, args.n)
            if p["family"] in args.families + [f"country-{f}" for f in args.families]
        ]
        bridge_of = {it["id"]: it["bridge"] for f in suite_fams for it in S.load(f)}
        for p in prompts:
            p["bridge"] = bridge_of.get(p["id"], "")
    else:
        prompts = suite_prompts(tok, suite_fams, args.kinds, args.n, COMPETENCE)
        prompts += country_prompts(tok, [f for f in args.families if f in ("R", "B")], args.n)
    for p in prompts:
        p["skip"] = bridge_positions(tok, p["ids"], p["bridge"]) if p["bridge"] else []
    print(len(prompts), "prompts;", len(bands), "bands;", len(args.conditions), "conditions", flush=True)

    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    layers = sorted({la for b in bands for la in b})
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    rot = {la: rotation(wg.shape[1], SEED_ROT + la) for la in layers}
    rdict = {la: RotatedDictionary(dic[la], rotation(wg.shape[1], SEED_DICT + la)) for la in layers}
    gauss = {}
    if "gauss" in args.conditions:
        for la in layers:  # v1's control, drawn exactly as ablate_pilot did
            g = torch.Generator(device="cuda").manual_seed(SEED_GAUSS + la)
            gauss[la] = MatrixDictionary(torch.nn.functional.normalize(torch.randn((letters.numel(), wg.shape[1]),
                                                                                    device="cuda", generator=g), dim=-1))  # fmt: skip
    own_cache: dict[tuple[str, int], torch.Tensor] = {}

    def own_rows(word: str, la: int) -> torch.Tensor:
        if (word, la) not in own_cache:
            rows = {int(row_of[i]) for i in model.surface_ids(word) if int(row_of[i]) >= 0}
            try:
                concept = int(row_of[model.concept_token(word)])
            except ValueError:
                concept = -1
            if concept >= 0:
                cos = dic[la].scores(dic[la].atoms(torch.tensor([concept], device="cuda")))[0]
                rows |= set((cos >= OWN_COS).nonzero().squeeze(1).tolist())
            own_cache[(word, la)] = torch.tensor(sorted(rows), dtype=torch.long, device="cuda")
        return own_cache[(word, la)]

    t0 = time.time()
    rows_out, band_seconds = [], collections.Counter()
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    for group in by_len.values():
        for start in range(0, len(group), args.batch):
            chunk = group[start : start + args.batch]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            answer = torch.tensor([p["tok"] for p in chunk], device="cuda")
            clean = first_token_logits(model, ids, {})
            base_logp = clean.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
            for row, p in enumerate(chunk):
                rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": "-", "condition": "none",
                                 "correct": int(clean[row].argmax()) == p["tok"], "logp": float(base_logp[row])})  # fmt: skip
            protected = [row_of[t][row_of[t] >= 0] for t in clean.topk(10, dim=1).indices]
            # does the protected set (clean top-10 at the answer position) shield the bridge itself? (logged per row)
            shields = [bool(p["bridge"]) and bool(set(model.surface_ids(p["bridge"])) & set(t.tolist()))
                       for p, t in zip(chunk, clean.topk(10, dim=1).indices, strict=True)]  # fmt: skip
            for band in bands:
                tb = time.time()
                for cond in conditions_for(band, args.conditions):
                    edits = {}
                    for la in band:
                        if cond.startswith("paper10"):
                            rs = [RowSettings(protected=protected[i]) for i in range(len(chunk))]
                        elif cond == "keep_own":
                            rs = [RowSettings(banned=own_rows(p["bridge"], la) if p["bridge"] else None) for p in chunk]
                        elif cond == "skip_subject":
                            rs = [RowSettings(skip=p["skip"]) for p in chunk]
                        else:
                            rs = [RowSettings() for _ in chunk]
                        method = "top" if cond.startswith("paper10") else "omp"
                        d = rdict[la] if cond.endswith("_rdict") else gauss[la] if cond == "gauss" else dic[la]
                        edits[la] = removal_edit(method, d, rs, rotation=rot[la] if cond.endswith("_rot") else None)
                    logits = first_token_logits(model, ids, edits)
                    logp = logits.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
                    for row, p in enumerate(chunk):
                        rows_out.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "band": label(band),
                                         "condition": cond, "correct": int(logits[row].argmax()) == p["tok"],
                                         "logp": float(logp[row]), "bridge_protected": shields[row]})  # fmt: skip
                band_seconds[label(band)] += time.time() - tb
            print(f"{len(rows_out)} rows, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "rows.jsonl", rows_out)

    base = {(r["family"], r["id"], r["kind"]): r for r in rows_out if r["condition"] == "none"}
    cells: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (bl, fk, cond), rs in _group(rows_out).items():
        cells[bl][fk][cond] = {"n": len(rs), "accuracy": statistics.mean(r["correct"] for r in rs),
                               "dlogp": statistics.mean(r["logp"] - base[(r["family"], r["id"], r["kind"])]["logp"] for r in rs)}  # fmt: skip
    none_acc = {
        fk: statistics.mean(r["correct"] for r in rs) for (bl, fk, cond), rs in _group(rows_out, none=True).items()
    }
    summary = {"seconds": round(time.time() - t0), "band_seconds": {k: round(v) for k, v in band_seconds.items()},
               "unedited_accuracy": none_acc, "cells": cells}  # fmt: skip
    if args.plan == "v1check":
        summary["v1_agreement"] = v1_agreement(rows_out)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# ablate_v2 / {args.name}: {len(prompts)} prompts, {time.time() - t0:.0f}s", "",
             "Unedited accuracy: " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in none_acc.items()), ""]  # fmt: skip
    fks = list(none_acc)
    for cond in args.conditions:
        lines += [
            f"## {cond}: accuracy (%) by band",
            "",
            "| band | " + " | ".join(fks) + " |",
            "|---" * (len(fks) + 1) + "|",
        ]
        for band in bands:
            c = cells[label(band)]
            lines.append(
                f"| {label(band)} | "
                + " | ".join(f"{100 * c[fk][cond]['accuracy']:.0f}" if cond in c[fk] else "-" for fk in fks)
                + " |"
            )
        lines.append("")
    if args.plan == "v1check":
        lines += ["## agreement with ablate_pilot v1 (same items)", "", json.dumps(summary["v1_agreement"], indent=1)]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text()[:3000])


def _group(rows: list[dict], none: bool = False) -> dict:
    g: dict = collections.defaultdict(list)
    for r in rows:
        if (r["condition"] == "none") == none:
            g[(r["band"], f"{r['family']}/{r['kind']}", r["condition"])].append(r)
    return g


def v1_agreement(rows: list[dict]) -> dict:
    """Item-by-item agreement with ablate_pilot v1 (omp25 vs v1's 'jspace', gauss vs 'random', none vs 'none')."""
    v1 = {}
    for line in (A.RESULTS / "v1" / "rows.jsonl").read_text().splitlines():
        r = json.loads(line)
        v1[(r["family"], r["id"], r["kind"], r["condition"])] = r
    names = {"none": "none", "omp25": "jspace", "gauss": "random"}
    out = {}
    for ours, theirs in names.items():
        pairs = [(r, v1.get((r["family"], r["id"], r["kind"], theirs))) for r in rows if r["condition"] == ours]
        pairs = [(a, b) for a, b in pairs if b is not None]
        if pairs:
            out[ours] = {"n": len(pairs), "same_correct": statistics.mean(a["correct"] == b["correct"] for a, b in pairs),
                         "median_abs_dlogp": statistics.median(abs(a["logp"] - b["logp"]) for a, b in pairs),
                         "accuracy_ours": statistics.mean(a["correct"] for a, _ in pairs),
                         "accuracy_v1": statistics.mean(b["correct"] for _, b in pairs)}  # fmt: skip
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--plan", choices=["v1check", "depth", "bands"], required=True)
    ap.add_argument("--bands", nargs="*", default=[], help='with --plan bands: "32,36,40" or "16-28"')
    ap.add_argument("--conditions", nargs="+", default=["omp25", "omp25_rot", "omp25_rdict", "paper10", "paper10_rot",
                                                        "paper10_rdict"], choices=CONDITIONS)  # fmt: skip
    ap.add_argument("--families", nargs="+", default=["BL", "BR", "RL", "RR", "R", "B"])
    ap.add_argument("--kinds", nargs="+", default=["clean"], choices=["clean", "hop", "step1", "step2", "step3"])
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--no-tf32", action="store_true", help="full fp32 matmuls (the v1 numerics check)")
    ap.add_argument("--workspace", type=int, default=None, help="depth plan: first layer of the workspace range")
    main(ap.parse_args())
