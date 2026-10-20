"""control_split: the positive control for suite_split's method (Zach, 2026-10-19, after Neel's proposal feedback).

suite_split called every suite family 'outside' the J-space, recall-used ones included, and exp09's raw-text copy split
on countries gave the J-space part 4% of R's flips against 44% for the full copy. The proposal's 'inside' evidence is
exp02's probe swaps (B1: J-part 52% vs rest 8%), a different intervention: J++ probe directions of the two entities,
swapped at the cue phrase over layers 24-40 at once. Can suite_split's copy-and-split see 'inside' at all? This runs it
on the paper-style place items, in the variants that move it toward exp02's setting:

  items   data/bind_recall.json R (city -> country recalled -> capital) and B (country bound to a person -> capital),
          chat format with 'Answer:' prefilled (exp09's prepare, chat_prefill); capitals as answers
  groups  question (as suite_split), cue (the cue phrase: 'Lyon is located' / 'Emma lives', exp02's swap positions),
          last (map only)
  modes   single (one window layer at a time, suite_split's) and band (every window layer patched at once, as exp02)

Scoring, controls and the concentration verdict are suite_split's (the answer read at the capital's first token;
random-direction nulls; the matched-alignment piece; inside if the concentration's lower bound is above 2).
Windows: the question group's as suite_split (frac rule, below the answer onset, 44 on this model); the cue group's the
same rule restricted to exp02's band 24-40 (below 24 the cue copy still carries the changed city's own token).

Decision (fixed before the run): the method can see 'inside' if R's J-space concentration has its lower bound above 2
in at least one variant (group x mode); those variants become the battery's method. If none does, copy-and-split does
not find the paper-style recalled place in the J-space, and exp02's 'inside' has to come from the probe directions
rather than the model's own counterfactual difference (next: probe swap and copy on the same items).

Stages: manifest_map --name M --why W [--n N]   run_map --name M   manifest_parts --name P --map M --why W
        run_parts --name P
"""

from __future__ import annotations

import argparse
import collections
import json
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
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import answer_colour, write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp

EXP = "control_split"
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("R", "B")
GROUPS = ("question", "cue", "last")
PART_GROUPS = ("question", "cue")
CUE_BAND = tuple(range(24, 41))  # exp02's swap band on Qwen3.6-27B
N_ITEMS = 150
CAPITALS = list(E.ITEM_SETS["bind_recall"][4])


@torch.no_grad()
def omp_without(dictionary: torch.Tensor, x: torch.Tensor, k: int, banned: torch.Tensor) -> torch.Tensor:
    """exp04's signed OMP with some dictionary rows never chosen (the J-space part without given words)."""
    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    for _ in range(k):
        scores = ((x - approx) @ dictionary.T).abs()
        scores[:, banned] = -1.0
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dictionary[chosen].double()
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
    return approx


EXTRA = ("answer2", "words4", "jspace_minus_words")  # parts_v2's diagnostic parts (each with its random null)
EXTRA_V3 = ("jspace_wo_own", "jspace_wo_words4")  # parts_v3: the J-space part of delta after projecting out the words


def judge(text: str) -> str | None:
    return answer_colour(text, CAPITALS)


def build_cases(model, tok, n: int) -> tuple[list[dict], list[dict]]:
    """exp09's eligible items (clean, C and O answered, chat_prefill), a seeded sample of n per family, in
    suite_split's case format."""
    E.N_ITEMS = n
    cases, rows = E.eligible_cases(model, tok, None, item_set="bind_recall", fmt="chat_prefill")
    out = []
    for c in cases:
        c = dict(c)
        c["id"] = c["scene"] = c["name"]
        c["cf_bridge"], c["cf_answer"], c["answer_kind"] = c["target"], c["target_answer"], "word"
        c["read_ids"] = c["ids"]
        c["tok_A"] = S.answer_token(tok, c["answer"], "word")
        c["tok_b"] = S.answer_token(tok, c["cf_answer"], "word")
        if c["tok_A"] != c["tok_b"]:  # the two capitals' first tokens must differ for the read
            out.append(c)
    return out, rows


def manifest(name: str, why: str, kind: str) -> dict:
    pins.check_run_name(name)
    path, sha = E.ITEM_SETS["bind_recall"][:2]
    return {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "items": {"file": str(path.relative_to(pins.REPO_ROOT)), "sha256": sha, "families": list(FAMILIES)},
        "format": "chat template, thinking off, 'Answer:' prefilled (exp09's chat_prefill: the statement as a question)",
        "eligibility": "exp09's: clean, C and O each answered (greedy, 8 tokens, the capitals judge); a seeded sample "
        f"(seed {E.SAMPLE_SEED}) per family; cases whose two capitals share a first token dropped",
        "read": "suite_split's: one forward, read at the capital's first token; frac of the way from clean to C",
        "doc": (__doc__ or "").split("\n\n")[1],
    }  # fmt: skip


def stage_manifest_map(name: str, why: str, n: int) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    m = manifest(name, why, "map")
    m["n_items"] = n
    m["layers"] = list(P.MAP_LAYERS)
    m["groups"] = list(GROUPS)
    m["decision"] = {"window": "suite_split's frac rule per group", "answer_formed": "suite_split's rule"}
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run_map(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    assert sha256_of(pins.REPO_ROOT / m["items"]["file"]) == m["items"]["sha256"], "items changed"
    model = load_model()
    t0 = time.time()
    cases, rows = build_cases(model, model.tokenizer, m["n_items"])
    counts = {f: sum(c["family"] == f for c in cases) for f in FAMILIES}
    print("cases", counts, f"{time.time() - t0:.0f}s", flush=True)
    outcomes: list[dict] = []
    seen: collections.Counter = collections.Counter()
    for c in cases:
        P.unedited_ld(model, c)
        h = {
            s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=P.MAP_LAYERS)[1]
            for s in ("clean", "cf", "off")
        }
        jobs = []
        for group in GROUPS:
            pos = c["groups"][group]
            for layer in P.MAP_LAYERS:
                for source in ("cf", "off"):
                    delta = h[source][layer][pos] - h["clean"][layer][pos]
                    jobs.append(({"group": group, "layer": layer, "source": source}, {layer: AddRows(delta, pos)}))
        P.read_jobs(model, c, jobs, outcomes, validate=seen[c["family"]] < P.N_VALIDATE, judge=judge)
        seen[c["family"]] += 1
    write_jsonl(out_dir / "items.jsonl", rows)
    write_jsonl(out_dir / "cases.jsonl", [P.case_row(c) for c in cases])
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = {"counts": counts, "seconds": round(time.time() - t0), "validation": P.validation(outcomes),
               "windows": P.frac_windows(outcomes), "windows_flip": P.windows(outcomes),
               "answer_formed": P.answer_formed(outcomes), "rates": P.map_rates(outcomes)}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# {EXP} / {name}", "", f"Cases: {json.dumps(counts)}", f"Read vs greedy: {json.dumps(summary['validation'])}",
             f"Windows: {json.dumps(summary['windows'])}", f"Answer formed: {json.dumps(summary['answer_formed'])}", "",
             "| family | group | layer | n | C gives X's answer | O changes it | C frac | O frac |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    lines += [f"| {r['family']} | {r['group']} | {r['layer']} | {r['n']} | {100 * r['b'][0]:.0f}% | "
              f"{100 * r['off_changed'][0]:.0f}% | {r['frac_cf']:+.2f} | {r['frac_off']:+.2f} |" for r in summary["rates"]]  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


def stage_manifest_parts(
    name: str, map_run: str, why: str, extra: bool | str = False, cap_override: int | None = None
) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    map_summary = RESULTS / map_run / "summary.json"
    blob = json.loads(map_summary.read_text())
    cap = {f: min(blob["answer_formed"].get(f, P.ANSWER_ONSET), P.ANSWER_ONSET) for f in FAMILIES}
    if cap_override is not None:  # a sensitivity run: the window's upper layer set by hand (the manifest records it)
        cap = {f: cap_override for f in cap}
    window = {
        f: {
            "question": [la for la in blob["windows"].get(f, {}).get("question", []) if la < cap[f]],
            # the cue band is exp02's on the 27B; other targets run the question group only (memory on one H200)
            "cue": [la for la in blob["windows"].get(f, {}).get("cue", []) if la < cap[f] and la in CUE_BAND]
            if pins.TARGET == "qwen3.6-27b"
            else [],
        }
        for f in FAMILIES
    }
    m = manifest(name, why, "parts")
    m["map"] = {
        "run": map_run,
        "summary_sha256": sha256_of(map_summary),
        "cap": cap,
        "parts_window": window,
        "cap_override": cap_override,
    }
    m["lens"] = {pins.FROZEN_LENS: list(pins.LENS_SOURCES[pins.FROZEN_LENS]), "sha256": pins.FROZEN_LENS_SHA256}
    m["variants"] = "group (question, cue) x mode (single: each window layer alone; band: all window layers at once)"
    m["extra_parts"] = extra
    if extra == "v3":
        m["extra_v3"] = {
            "parts": "jspace_wo_own: the 25-atom J-space part of delta minus its projection on the bridge's and X's "
            "lens vectors; jspace_wo_words4: the same after projecting out all four words (bridge, X, both answers)",
            "why": "parts_v2's bar test turned out uninformative: the 25 atoms are mostly unrelated tokens (a debug on 3 "
            "R cases at layer 36 found the bridge words among them once), so barring exact surface forms leaves the "
            "J-space part unchanged while the two own-word directions alone carry about 80% of its effect",
            "decision": "fixed before the run: the J-space effect is the bridge words' (H0's own-word clause) if "
            "jspace_wo_own moves the answer less than a quarter as far as jspace (frac; question group, single layer)",
        }
    if extra:
        m["extra"] = {
            "parts": "answer2: delta's projection on the lens vectors of the two answers (capitals); words4: on the "
            "span of the bridge's, X's and both answers' vectors; jspace_minus_words: the 25-atom J-space part with "
            "every single-token surface of those four words barred from the dictionary",
            "decision": "fixed before the run: the J-space effect is the words' if jspace_minus_words moves the answer "
            "less than a quarter as far as jspace (frac, single and band); it is the answer's (Neel's linear-relation "
            "objection) if answer2 moves it further than lens2 (the bridge's own words); reported per variant",
        }
    m["decision"] = {
        "verdict": "suite_split's: concentration (case bootstrap) lower bound above 2 -> inside; upper bound below 2 "
        "and not_jspace - jspace above 0 -> outside; else inconclusive; per family and variant, frac primary",
        "control": "the method can see 'inside' if R is inside in at least one variant; else exp02's 'inside' needs "
        "the probe directions, not the model's own counterfactual difference",
    }
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run_parts(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    map_dir = RESULTS / m["map"]["run"]
    assert sha256_of(map_dir / "summary.json") == m["map"]["summary_sha256"], "the map changed since the manifest"
    window = m["map"]["parts_window"]
    layers = tuple(sorted({la for f in window.values() for v in f.values() for la in v}))
    assert layers, "no window anywhere"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    picked = {json.loads(line)["id"] for line in (map_dir / "cases.jsonl").read_text().splitlines()}
    E.N_ITEMS = m.get("n_items", N_ITEMS)
    items = E.ITEM_SETS["bind_recall"][2]()
    cases = []
    for index, item in enumerate(items):
        uid = E.uid(item, index)
        if uid not in picked:
            continue
        prep = E.prepare(item, index, tok, "chat_prefill")
        c = {**item, "name": uid, "index": index, **prep, "id": uid, "scene": uid, "cf_bridge": item["target"],
             "cf_answer": item["target_answer"], "answer_kind": "word"}  # fmt: skip
        c["read_ids"] = c["ids"]
        c["tok_A"], c["tok_b"] = (S.answer_token(tok, a, "word") for a in (item["answer"], item["target_answer"]))
        cases.append(c)
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    row_of = {int(t): i for i, t in enumerate(letters.tolist())}
    dictionaries = {la: lens.vectors(la, letters) for la in layers}
    extra = m.get("extra_parts", False)
    outcomes: list[dict] = []
    fve: list[dict] = []
    for k, c in enumerate(cases):
        P.unedited_ld(model, c)
        mine = window[c["family"]]
        rec = tuple(sorted({la for v in mine.values() for la in v}))
        if not rec:
            continue
        h = {s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=rec)[1] for s in ("clean", "cf", "off")}
        pair = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])], device="cuda")
        answers = torch.tensor([c["tok_A"], c["tok_b"]], device="cuda")
        words = {i for w in (c["bridge"], c["cf_bridge"], c["answer"], c["cf_answer"]) for i in model.surface_ids(w)}
        words |= {int(t) for t in pair.tolist() + answers.tolist()}
        banned = torch.tensor(sorted(row_of[i] for i in words if i in row_of), dtype=torch.long, device="cuda")
        jobs: list[tuple[dict, dict]] = []
        for gi, group in enumerate(PART_GROUPS):
            win = mine[group]
            if not win:
                continue
            pos = c["groups"][group]
            band: dict[str, dict[int, Any]] = collections.defaultdict(dict)
            for la in win:
                delta = h["cf"][la][pos] - h["clean"][la][pos]
                lens2 = lens2_part(delta, lens.vectors(la, pair))
                jspace = signed_omp(dictionaries[la], delta, K_ATOMS)
                total = float(delta.norm() ** 2)
                for what, part in (("lens2", lens2), ("jspace", jspace)):
                    fve.append({"family": c["family"], "name": c["id"], "group": group, "layer": la, "what": what,
                                "share": round(float(part.norm() ** 2) / total, 4)})  # fmt: skip
                parts = {"full": delta, "lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace,
                         "not_jspace": delta - jspace}  # fmt: skip
                if extra:
                    parts["answer2"] = lens2_part(delta, lens.vectors(la, answers))
                    parts["words4"] = lens2_part(delta, lens.vectors(la, torch.cat([pair, answers])))
                    parts["jspace_minus_words"] = omp_without(dictionaries[la], delta, K_ATOMS, banned)
                    if extra == "v3":
                        parts["jspace_wo_own"] = signed_omp(dictionaries[la], delta - lens2, K_ATOMS)
                        parts["jspace_wo_words4"] = signed_omp(dictionaries[la], delta - parts["words4"], K_ATOMS)
                    for what in EXTRA + (EXTRA_V3 if extra == "v3" else ()):
                        fve.append({"family": c["family"], "name": c["id"], "group": group, "layer": la, "what": what,
                                    "share": round(float(parts[what].norm() ** 2) / total, 4)})  # fmt: skip
                for pi, (pname, part) in enumerate(parts.items()):
                    seed = P.NULL_SEED + 1_000_000 * gi + 1000 * k + 10 * la + pi
                    noise = null_rows(part, torch.Generator(device="cuda").manual_seed(seed))
                    runs = {(pname, False): part, (pname, True): noise}
                    if pname in ("lens2", "jspace"):
                        gen = torch.Generator(device="cuda").manual_seed(seed + 500_000)
                        runs[f"{pname}_matched", False] = P.matched_rows(part, delta, gen)
                    for (pn, null), vec in runs.items():
                        if pn == "full" and null:
                            continue
                        tags = {"group": group, "layer": la, "part": pn, "source": "cf", "null": null}
                        jobs.append((tags, {la: AddRows(vec, pos)}))
                        band[f"{pn}|{null}"][la] = AddRows(vec, pos)
                off = h["off"][la][pos] - h["clean"][la][pos]
                jobs.append(({"group": group, "layer": la, "part": "full", "source": "off", "null": False},
                             {la: AddRows(off, pos)}))  # fmt: skip
                band["off"][la] = AddRows(off, pos)
            for key, edits in band.items():
                if key == "off":
                    tags = {"group": group, "layer": "band", "part": "full", "source": "off", "null": False}
                else:
                    pn, null = key.split("|")
                    tags = {"group": group, "layer": "band", "part": pn, "source": "cf", "null": null == "True"}
                jobs.append((tags, dict(edits)))
        P.read_jobs(model, c, jobs, outcomes)
        if (k + 1) % 50 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "fve.jsonl", fve)
    summary = summarize(outcomes, fve, window)
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# {EXP} / {name}", "", f"Control (the manifest's rule): {summary['control']}", "",
             "| family | group | mode | n | full | rest | J-space | matched | concentration | verdict |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, v in summary["variants"].items():
        mm, c = v["frac"]["means"], v["frac"]["jspace"]["concentration"]
        fam, group, mode = key.split("/")
        lines.append(f"| {fam} | {group} | {mode} | {v['n']} | {100 * mm['full']:.0f}% | {100 * mm['not_jspace']:.0f}% | "
                     f"{100 * mm['jspace']:.1f}% | {100 * mm['jspace_matched']:.1f}% | {c[0]:.2f} [{c[1]:.2f}, {c[2]:.2f}] | "
                     f"{v['frac']['jspace']['verdict']} |")  # fmt: skip
    for key, v in summary["variants"].items():
        if v.get("extra_frac_means"):
            em, sh = v["extra_frac_means"], v["extra_share_median"]
            lines.append(f"- {key}: " + ", ".join(f"{k} {100 * x:.1f}%" for k, x in em.items())
                         + " | variance shares: " + ", ".join(f"{k} {x:.3f}" for k, x in sh.items()))  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


def summarize(outcomes: list[dict], fve: list[dict], window: dict) -> dict:
    out: dict[str, Any] = {"variants": {}}
    for fam in FAMILIES:
        for group in PART_GROUPS:
            if not window.get(fam, {}).get(group):
                continue
            for mode in ("single", "band"):
                rows = [o for o in outcomes if o["family"] == fam and o["group"] == group
                        and ((o["layer"] == "band") == (mode == "band"))]  # fmt: skip
                shares = [f for f in fve if f.get("family") == fam and f.get("group") == group]
                means = {
                    f"{p}{' null' if nl else ''}": statistics.mean(v.values())
                    for p in EXTRA + EXTRA_V3
                    for nl in (False, True)
                    if (v := P.scores(rows, "frac", part=p, null=nl, source="cf"))
                }
                out["variants"][f"{fam}/{group}/{mode}"] = {
                    "extra_frac_means": means,
                    "extra_share_median": {
                        w: statistics.median(f["share"] for f in shares if f["what"] == w)
                        for w in EXTRA + EXTRA_V3
                        if any(f["what"] == w for f in shares)
                    },
                    "window": window[fam][group],
                    "n": len({o["name"] for o in rows}),
                    "frac": P.verdicts(rows, "frac", shares),
                    "flip": P.verdicts(rows, "flip", shares),
                    "share_median": statistics.median(f["share"] for f in shares if f["what"] == "jspace"),
                }
    r = {k: v["frac"]["jspace"]["verdict"] for k, v in out["variants"].items() if k.startswith("R/")}
    passed = [k for k, v in r.items() if v == "inside"]
    out["control"] = (f"passes: R inside in {passed}" if passed else
                      f"fails: R inside in no variant ({r})")  # fmt: skip
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest_map", "run_map", "manifest_parts", "run_parts"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--map")
    ap.add_argument("--n", type=int, default=N_ITEMS, help="manifest_map: items per family (a smoke run: few)")
    ap.add_argument("--extra", action="store_true", help="manifest_parts: add the answer-word and words-removed parts")
    ap.add_argument("--cap", type=int, default=None, help="manifest_parts: override the window's upper layer")
    ap.add_argument("--v3", action="store_true", help="manifest_parts: --extra plus the J-space part after the words")
    args = ap.parse_args()
    if args.stage == "manifest_map":
        assert args.why, "manifest_map needs --why"
        stage_manifest_map(args.name, args.why, args.n)
    elif args.stage == "run_map":
        stage_run_map(args.name)
    elif args.stage == "manifest_parts":
        assert args.why, "manifest_parts needs --why"
        assert args.map, "manifest_parts needs --map"
        stage_manifest_parts(args.name, args.map, args.why, "v3" if args.v3 else args.extra, args.cap)
    else:
        stage_run_parts(args.name)
