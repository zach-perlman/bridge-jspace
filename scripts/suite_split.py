"""suite_split: where does each suite_v1 family carry its bridge, and through which part? exp09's copy-and-split on
part B's prompt suite (scripts/suite_v1.py), scored by reading the answer instead of generating it.

  map    copy C's (or O's) block output into the clean run at a position group, one layer at a time (every 4th layer
         on Qwen3.6-27B, every 2nd on Qwen3.5-9B, below the last three blocks): 'question' (the question's tokens after
         C's changed ones, through the template and 'Answer:'), 'last' (the last token)
  parts  at each family's question-group window, below the layer where the last token alone already carries the
         answer: the copy split into its J-space part (25-atom signed OMP over the frozen J++'s letter-token vectors)
         and the rest, and into its projection on J++'s vectors of the bridge and X and the rest; each part also along
         a matched-norm random direction (its null)

Scoring (Zach, 2026-10-19: a continuous measure next to answer flips): one forward of the edited prompt, with a digit
answer's space token appended (the greedy reply's first token in every unedited competence prompt), read at the
answer's first token. Per edited run: the top token's role (b: X's answer, A: the bridge's, other) and the logit
difference ld = logit(b) - logit(A), also as `frac`, the fraction of the way from the unedited clean run's ld to the
unedited C run's. The map run also generates 8 greedy tokens for every edit of its first 20 cases per family and
reports how often the read's role equals the greedy text's (the check that the read survives edits).

Items: a family's eligible items are those with every prompt right in that model's competence run (clean, C, O and
each step alone; results/suite_v1). BL/BR/RL/RR share scenes, and so do BLR/BRL: a run samples (seed 0) up to 150 scenes
eligible in all of its families of a scene group, so paired families are compared on the same scenes (BLR therefore
on scenes where BRL is also right).

Stages (manifests are written before their runs, write-once):
  manifest_map --name M --families F ... --why W      run_map --name M
  manifest_parts --name P --map M --why W            run_parts --name P
"""

from __future__ import annotations

import argparse
import collections
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
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.tokens import raw_encoding
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp

EXP = "suite_split"
RESULTS = pins.RESULTS_DIR / EXP
MAP_LAYERS = tuple(range(0, pins.N_LAYERS - 3, max(1, pins.N_LAYERS // 16)))
# exp12 (Qwen3.6-27B): the answer is read at the last word from about layer 44 (exp09's cap); other targets: the map's
# own answer_formed only.
ANSWER_ONSET = {"qwen3.6-27b": 44}.get(pins.TARGET, pins.N_LAYERS - 1)
GROUPS = ("question", "last")
N_SCENES = 150
N_VALIDATE = 20
SAMPLE_SEED, NULL_SEED, BOOT_SEED, N_BOOT = 0, 0, 0, 2000
BATCH = 64
CHANCE_DRAWS = 20
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")
MATCHED = ("lens2_matched", "jspace_matched")
COMPETENCE = {  # (target, wording) -> the suite_v1 competence runs whose items.jsonl decide eligibility
    ("qwen3.6-27b", "A"): {"main": "competence_v2", "tiebreak": "competence_tiebreak_v1"},
    ("qwen3.6-27b", "B"): {"main": "competence_b_v1", "tiebreak": "competence_b_v1"},
    ("qwen3.5-9b", "A"): {"main": "qwen35_9b_competence_v2", "tiebreak": "qwen35_9b_competence_tiebreak_v1"},
    ("qwen3.5-9b", "B"): {"main": "qwen35_9b_competence_b_v1", "tiebreak": "qwen35_9b_competence_b_v1"},
}
MIN_FRAC = 0.10  # a window layer's copy moves the answer at least this far toward C's, on average
SCENE_GROUP = {"BL": "core", "BR": "core", "RL": "core", "RR": "core", "BLR": "tie", "BRL": "tie"}
LOOKUP_USED = ("BL", "RL", "BLR", "NAMES", "CODE")  # families whose bridge is used by a lookup in the prompt


def matched_rows(part: torch.Tensor, delta: torch.Tensor, generator: torch.Generator) -> torch.Tensor:
    """The matched-alignment control (exp02's jpart_matched, for a part of the copy): each row with the norm of
    `part`'s row and its cosine with delta's row, the rest along a random direction orthogonal to delta's row."""
    d_hat = torch.nn.functional.normalize(delta, dim=-1)
    norm = part.norm(dim=-1, keepdim=True)
    cos = ((part * d_hat).sum(-1, keepdim=True) / norm.clamp_min(1e-12)).clamp(-1.0, 1.0)
    r = torch.randn(delta.shape, device=delta.device, generator=generator)
    r = torch.nn.functional.normalize(r - (r * d_hat).sum(-1, keepdim=True) * d_hat, dim=-1)
    return norm * (cos * d_hat + (1 - cos**2).sqrt() * r)


def competence_file(fam: str, wording: str) -> Path:
    which = "tiebreak" if fam in S.TIEBREAK else "main"
    return S.RESULTS / COMPETENCE[pins.TARGET, wording][which] / "items.jsonl"


def prepare(item: dict, tok) -> dict:
    """Token ids of clean, C and O (and with a digit answer's space appended, for the read), C's and O's changed
    positions, the position groups, and the two answers' first tokens."""
    texts = {
        "clean": (item["context"], item["question"]),
        "cf": (item["cf_context"], item["cf_question"]),
        "off": (item["off_context"], item["question"]),
    }
    rendered = {k: S.render(tok, c, q) for k, (c, q) in texts.items()}
    enc = {k: raw_encoding(tok, t, offsets=True) for k, t in rendered.items()}
    ids = {k: list(e["input_ids"]) for k, e in enc.items()}
    cf_changed, off_changed = S.changed(ids["clean"], ids["cf"]), S.changed(ids["clean"], ids["off"])
    assert cf_changed, f"{item['id']}: C not token-aligned"
    assert off_changed, f"{item['id']}: O not token-aligned"
    q_start = rendered["clean"].rindex("\n" + item["question"]) + 1
    after = max(cf_changed)
    offsets = enc["clean"]["offset_mapping"]
    space = S.ids(tok, " ") if item["answer_kind"] == "digit" else []
    return {
        "ids": ids,
        "read_ids": {k: v + space for k, v in ids.items()},
        "changed": {"cf": cf_changed, "off": off_changed},
        "groups": {
            "question": [i for i, (_, e) in enumerate(offsets) if e > q_start and i > after],
            "last": [len(ids["clean"]) - 1],
        },
        "tok_A": S.answer_token(tok, item["answer"], item["answer_kind"]),
        "tok_b": S.answer_token(tok, item["cf_answer"], item["answer_kind"]),
    }


def sample_cases(families: list[str], tok, n_scenes: int, wording: str) -> tuple[list[dict], dict]:
    """The run's cases: per scene group, up to N_SCENES scenes eligible in all of the run's families of that group."""
    eligible: dict[str, dict[str, dict]] = {}
    for fam in families:
        ok: dict[str, list[bool]] = collections.defaultdict(list)
        for line in competence_file(fam, wording).read_text().splitlines():
            r = json.loads(line)
            if r["family"] == fam:
                ok[r["id"]].append(r["correct"])
        good = {i for i, v in ok.items() if all(v)}
        eligible[fam] = {it.get("scene", it["id"]): it for it in S.load(fam, wording) if it["id"] in good}
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for fam in families:
        groups[SCENE_GROUP.get(fam, fam)].append(fam)
    rng = random.Random(SAMPLE_SEED)
    cases, counts = [], {}
    for group, fams in groups.items():
        scenes = sorted(set.intersection(*(set(eligible[f]) for f in fams)))
        picked = rng.sample(scenes, min(n_scenes, len(scenes)))
        counts[group] = {"families": fams, "eligible_scenes": len(scenes), "sampled": len(picked)}
        for f in fams:
            cases += [{**eligible[f][s], **prepare(eligible[f][s], tok)} for s in picked]
    counts["eligible_items"] = {f: len(eligible[f]) for f in families}
    return cases, counts


def role(top: int, c: dict) -> str:
    return "b" if top == c["tok_b"] else "A" if top == c["tok_A"] else "other"


def unedited_ld(model, c: dict) -> None:
    """The unedited clean and C runs' logit differences (the ends of `frac`)."""
    ids = torch.tensor([c["read_ids"]["clean"], c["read_ids"]["cf"]], device="cuda")
    _, logits = model.generate_batch(ids, 1, [{}, {}], first_logits=True)
    c["ld_clean"], c["ld_cf"] = (float(lg[c["tok_b"]] - lg[c["tok_A"]]) for lg in logits)


def read_jobs(model, c: dict, jobs: list[tuple[dict, dict]], outcomes: list[dict], validate: bool = False) -> None:
    """An item's edited runs (tags, edits) in batches: the answer read, and with `validate` 8 greedy tokens too."""
    read_ids = torch.tensor([c["read_ids"]["clean"]], device="cuda")
    gen_ids = torch.tensor([c["ids"]["clean"]], device="cuda")
    span = c["ld_cf"] - c["ld_clean"]
    for start in range(0, len(jobs), BATCH):
        chunk = jobs[start : start + BATCH]
        edits = [e for _, e in chunk]
        _, logits = model.generate_batch(read_ids, 1, edits, first_logits=True)
        texts = model.generate_batch(gen_ids, 8, edits) if validate else None
        for row, (tags, _) in enumerate(chunk):
            lg = logits[row]
            ld = float(lg[c["tok_b"]] - lg[c["tok_A"]])
            o = {"family": c["family"], "name": c["id"], **tags, "role": role(int(lg.argmax()), c),
                 "ld": round(ld, 3), "frac": round((ld - c["ld_clean"]) / span, 4)}  # fmt: skip
            if texts is not None:
                said = S.said(texts[row], c["answer_kind"])
                o["greedy"] = texts[row]
                o["greedy_role"] = "b" if said == c["cf_answer"] else "A" if said == c["answer"] else "other"
            outcomes.append(o)


def manifest_common(name: str, why: str, kind: str, families: list[str], wording: str) -> dict:
    pins.check_run_name(name)
    files = {f: (S.DATA if wording == "A" else S.DATA_B) / f"{f}.json" for f in families}
    comp = {f: competence_file(f, wording) for f in families}
    return {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "families": families,
        "wording": wording,
        "items": {f: {"file": str(p.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(p)} for f, p in files.items()},
        "eligibility": {f: {"competence": str(p.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(p)} for f, p in comp.items()},
        "sample": f"per scene group, up to {N_SCENES} scenes eligible (every prompt right) in all of the run's families "
        f"of the group, seed {SAMPLE_SEED}; BL/BR/RL/RR and BLR/BRL are scene groups, other families their own",
        "format": "suite_v1's: chat template, thinking off, 'Answer:' prefilled",
        "groups": {"question": "the question's tokens after C's changed ones, through the end of the prompt (the "
                   "instruction, the template's tokens and 'Answer:' included)", "last": "the last prompt token"},
        "read": "one forward of the edited prompt, a digit answer's space token appended; role of the top token (b: X's "
        "answer, A: the bridge's, other); ld = logit(b) - logit(A); frac = (ld - ld_clean) / (ld_C - ld_clean), "
        "ld_clean and ld_C from the unedited clean and C runs",
    }  # fmt: skip


def stage_manifest_map(name: str, why: str, families: list[str], n_scenes: int, wording: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    m = manifest_common(name, why, "map", families, wording)
    m["question"] = "Where, by layer and position group, does each family carry its bridge (lens-free)?"
    m["layers"] = list(MAP_LAYERS)
    m["n_scenes"] = n_scenes
    m["validation"] = f"8 greedy tokens for every edit of the first {N_VALIDATE} cases per family; agreement of roles"
    m["decision"] = {
        "window": f"per family and group: the layers where C's copy moves the answer at least {MIN_FRAC} of the way to "
        "C's (mean frac) and further than O's copy (paired bootstrap 95% lower bound of frac_C - frac_O above 0). Chosen "
        "after the smoke run (8 scenes), before any full run: exp09's flip rule (C's flips vs O's changes, Wilson "
        "intervals apart) found BL only at layers 52-60, above the answer onset, while the copy already moved BL's "
        "answer 11-17% of the way at 32-40; the flip rule's windows are reported as windows_flip",
        "answer_formed": "per family, the first layer at which copying the last token alone gives X's answer for at "
        "least half the cases",
        "parts_window": f"the question group's window below min(answer_formed, {ANSWER_ONSET})",
    }
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def check_inputs(m: dict) -> None:
    for f, pin in m["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} items changed since the manifest"
    for f, pin in m["eligibility"].items():
        assert sha256_of(pins.REPO_ROOT / pin["competence"]) == pin["sha256"], f"{f} competence changed"


@torch.no_grad()
def stage_run_map(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    check_inputs(m)
    model = load_model()
    t0 = time.time()
    cases, counts = sample_cases(m["families"], model.tokenizer, m["n_scenes"], m["wording"])
    print(json.dumps(counts), flush=True)
    outcomes: list[dict] = []
    seen: collections.Counter = collections.Counter()
    for c in cases:
        unedited_ld(model, c)
        h = {
            s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=MAP_LAYERS)[1]
            for s in ("clean", "cf", "off")
        }
        jobs = []
        for group in GROUPS:
            pos = c["groups"][group]
            for layer in MAP_LAYERS:
                for source in ("cf", "off"):
                    delta = h[source][layer][pos] - h["clean"][layer][pos]
                    jobs.append(({"group": group, "layer": layer, "source": source}, {layer: AddRows(delta, pos)}))
        read_jobs(model, c, jobs, outcomes, validate=seen[c["family"]] < N_VALIDATE)
        seen[c["family"]] += 1
        if seen[c["family"]] % 25 == 0:
            print(f"{c['family']}: {seen[c['family']]} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "cases.jsonl", [case_row(c) for c in cases])
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = {"counts": counts, "seconds": round(time.time() - t0), "validation": validation(outcomes),
               "windows": frac_windows(outcomes), "windows_flip": windows(outcomes),
               "answer_formed": answer_formed(outcomes), "rates": map_rates(outcomes)}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# {EXP} / {name}", "", f"Cases: {json.dumps(counts)}", "", f"Read vs greedy: {json.dumps(summary['validation'])}",
             "", f"Windows: {json.dumps(summary['windows'])}", f"Windows by exp09's flip rule: {json.dumps(summary['windows_flip'])}",
             f"Answer formed: {json.dumps(summary['answer_formed'])}", "",
             "| family | group | layer | n | C gives X's answer | O changes the answer | C frac (mean) | O frac (mean) |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    lines += [f"| {r['family']} | {r['group']} | {r['layer']} | {r['n']} | {100 * r['b'][0]:.0f}% | "
              f"{100 * r['off_changed'][0]:.0f}% | {r['frac_cf']:+.2f} | {r['frac_off']:+.2f} |" for r in summary["rates"]]  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


def case_row(c: dict) -> dict:
    keep = ("id", "family", "scene", "bridge", "cf_bridge", "answer", "cf_answer", "ld_clean", "ld_cf", "groups")
    return {k: c[k] for k in keep if k in c}


def validation(outcomes: list[dict]) -> dict:
    v = [o for o in outcomes if "greedy_role" in o]
    pairs = collections.Counter(f"{o['role']}/{o['greedy_role']}" for o in v)
    return {"n": len(v), "agree": round(sum(o["role"] == o["greedy_role"] for o in v) / max(1, len(v)), 4),
            "read/greedy": dict(pairs.most_common())}  # fmt: skip


def families_in(outcomes: list[dict]) -> list[str]:
    return list(dict.fromkeys(o["family"] for o in outcomes))


def map_rates(outcomes: list[dict]) -> list[dict]:
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    for o in outcomes:
        cells[(o["family"], o["group"], o["layer"], o["source"])].append(o)
    rates = []
    for fam in families_in(outcomes):
        for group in GROUPS:
            for layer in MAP_LAYERS:
                cf, off = cells.get((fam, group, layer, "cf"), []), cells.get((fam, group, layer, "off"), [])
                if not cf:
                    continue
                rates.append({"family": fam, "group": group, "layer": layer, "n": len(cf),
                              "b": wilson(sum(o["role"] == "b" for o in cf), len(cf)),
                              "off_changed": wilson(sum(o["role"] != "A" for o in off), len(off)),
                              "frac_cf": statistics.mean(o["frac"] for o in cf),
                              "frac_off": statistics.mean(o["frac"] for o in off)})  # fmt: skip
    return rates


def frac_windows(outcomes: list[dict]) -> dict:
    """The manifest's window rule: mean frac of C's copy >= MIN_FRAC and above O's copy (paired bootstrap)."""
    cells: dict[tuple, dict[str, float]] = collections.defaultdict(dict)
    for o in outcomes:
        cells[(o["family"], o["group"], o["layer"], o["source"])][o["name"]] = o["frac"]
    out: dict[str, dict[str, list[int]]] = {}
    for fam in families_in(outcomes):
        for group in GROUPS:
            for layer in MAP_LAYERS:
                cf, off = cells.get((fam, group, layer, "cf"), {}), cells.get((fam, group, layer, "off"), {})
                names = sorted(set(cf) & set(off))
                if not names:
                    continue
                d = paired_bootstrap_diff([cf[n] for n in names], [off[n] for n in names], N_BOOT, BOOT_SEED)
                if statistics.mean(cf[n] for n in names) >= MIN_FRAC and d[1] > 0:
                    out.setdefault(fam, {}).setdefault(group, []).append(layer)
    return out


def windows(outcomes: list[dict]) -> dict:
    out: dict[str, dict[str, list[int]]] = {}
    for r in map_rates(outcomes):
        if r["b"][1] > r["off_changed"][2]:
            out.setdefault(r["family"], {}).setdefault(r["group"], []).append(r["layer"])
    return out


def answer_formed(outcomes: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in map_rates(outcomes):
        if r["group"] == "last" and r["b"][0] >= 0.5 and r["family"] not in out:
            out[r["family"]] = r["layer"]
    return out


def stage_manifest_parts(name: str, map_run: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    map_m = json.loads((RESULTS / map_run / "manifest.json").read_text())
    map_summary = RESULTS / map_run / "summary.json"
    blob = json.loads(map_summary.read_text())
    families = map_m["families"]
    cap = {f: min(blob["answer_formed"].get(f, ANSWER_ONSET), ANSWER_ONSET) for f in families}
    window = {f: [la for la in blob["windows"].get(f, {}).get("question", []) if la < cap[f]] for f in families}
    m = manifest_common(name, why, "parts", families, map_m["wording"])
    m["question"] = "At each family's window, which part of the copy carries the bridge: its J-space part or the rest?"
    m["map"] = {"run": map_run, "summary_sha256": sha256_of(map_summary), "cap": cap, "parts_window": window}
    m["sample"] = "the map run's cases (cases.jsonl), not resampled"
    m["lens"] = {pins.FROZEN_LENS: list(pins.LENS_SOURCES[pins.FROZEN_LENS]), "sha256": pins.FROZEN_LENS_SHA256}
    m["parts"] = {
        "full": "delta = h_C - h_clean at the question group",
        "lens2": "delta's projection on span{v_I, v_X}, the lens's unit vectors of the bridge and X; not_lens2 the rest",
        "jspace": f"delta's {K_ATOMS}-atom signed OMP part over the lens's unit letter-token vectors; not_jspace the rest",
    }
    m["controls"] = (
        "each part along a seeded random direction at the same per-position norm (its null); lens2_matched and "
        "jspace_matched: per position the part's norm and cosine with delta, the rest a random direction orthogonal to "
        "delta (an equal-sized, equally aligned piece of the copy); O's full copy"
    )
    m["decision"] = {
        "measures": "primary: frac (the logit difference moved, as a fraction of the way to C); secondary: flips (top "
        "token X's answer). Per case, each averaged over the window's layers; paired bootstraps over cases",
        "parts": "per family and measure (paired bootstrap 95% intervals): J-specific if jspace - jspace_matched is "
        "above 0 (the J-space part moves the answer more than an equal-sized, equally aligned piece of the copy); rest "
        "larger if not_jspace - jspace is above 0. Verdict: inside (J-specific, rest not larger), both (J-specific, "
        "rest larger), outside (not J-specific, rest larger), neither. exp09's rule (against the random null only) is "
        "reported as verdict_exp09. Chosen after the smoke run, before any full run: with the continuous measure the "
        "J-space part beat its random null by 2-5 points in every family at n=8 while carrying about its share of the "
        "copy's variance, so 'beats its null' no longer separates a J-space-carried bridge from any piece of the copy",
        "claim_1": "variables used by a lookup in the prompt are carried outside the J-space: refuted if BL is inside "
        "or both (primary measure); supported if BL is outside; the other lookup-used families (RL, BLR, NAMES, CODE) "
        "reported the same way",
        "tie_break": "BLR and BRL: 'what uses the bridge decides' if BLR is outside and BRL inside or both; 'where the "
        "answer comes from decides' if BLR is inside or both and BRL outside; otherwise mixed, reported family by "
        "family",
        "empty_window": "a family with an empty window is not interpreted",
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run_parts(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    check_inputs(m)
    map_dir = RESULTS / m["map"]["run"]
    assert sha256_of(map_dir / "summary.json") == m["map"]["summary_sha256"], "the map changed since the manifest"
    window = m["map"]["parts_window"]
    layers = tuple(sorted({la for v in window.values() for la in v}))
    assert layers, "no family has a window"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    picked = [json.loads(line) for line in (map_dir / "cases.jsonl").read_text().splitlines()]
    items = {f: {it["id"]: it for it in S.load(f, m["wording"])} for f in m["families"]}
    cases = [{**items[p["family"]][p["id"]], **prepare(items[p["family"]][p["id"]], tok)} for p in picked]
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    dictionaries = {la: lens.vectors(la, letters) for la in layers}
    outcomes: list[dict] = []
    fve: list[dict] = []
    g = torch.Generator(device="cuda").manual_seed(BOOT_SEED)
    for la in layers:
        x = torch.randn(CHANCE_DRAWS, dictionaries[la].shape[1], device="cuda", generator=g)
        share = (signed_omp(dictionaries[la], x, K_ATOMS).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
        fve.append({"layer": la, "what": "chance", "share": round(float(share), 4)})
    for k, c in enumerate(cases):
        mine = window[c["family"]]
        if not mine:
            continue
        unedited_ld(model, c)
        pos = c["groups"]["question"]
        h = {
            s: model.run(torch.tensor([c["ids"][s]], device="cuda"), record=tuple(mine))[1]
            for s in ("clean", "cf", "off")
        }
        pair = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["cf_bridge"])], device="cuda")
        jobs: list[tuple[dict, dict]] = []
        for la in mine:
            delta = h["cf"][la][pos] - h["clean"][la][pos]
            jobs.append(({"layer": la, "part": "full", "source": "cf", "null": False}, {la: AddRows(delta, pos)}))
            off = h["off"][la][pos] - h["clean"][la][pos]
            jobs.append(({"layer": la, "part": "full", "source": "off", "null": False}, {la: AddRows(off, pos)}))
            lens2 = lens2_part(delta, lens.vectors(la, pair))
            jspace = signed_omp(dictionaries[la], delta, K_ATOMS)
            total = float(delta.norm() ** 2)
            for what, part in (("lens2", lens2), ("jspace", jspace)):
                fve.append({"family": c["family"], "name": c["id"], "layer": la, "what": what,
                            "share": round(float(part.norm() ** 2) / total, 4)})  # fmt: skip
            parts = {"lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace, "not_jspace": delta - jspace}
            for pi, (pname, part) in enumerate(parts.items()):
                jobs.append(({"layer": la, "part": pname, "source": "cf", "null": False}, {la: AddRows(part, pos)}))
                seed = NULL_SEED + 100000 * k + 10 * la + pi
                noise = null_rows(part, torch.Generator(device="cuda").manual_seed(seed))
                jobs.append(({"layer": la, "part": pname, "source": "cf", "null": True}, {la: AddRows(noise, pos)}))
            for mi, pname in enumerate(("lens2", "jspace")):
                gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 100000 * k + 10 * la + 5 + mi)
                matched = matched_rows(parts[pname], delta, gen)
                tags = {"layer": la, "part": f"{pname}_matched", "source": "cf", "null": False}
                jobs.append((tags, {la: AddRows(matched, pos)}))
        read_jobs(model, c, jobs, outcomes)
        if (k + 1) % 50 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "fve.jsonl", fve)
    summary = summarize_parts(outcomes, fve, window)
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_parts_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def scores(outcomes: list[dict], measure: str, **where) -> dict[str, float]:
    vals: dict[str, list[float]] = collections.defaultdict(list)
    for o in outcomes:
        if all(o.get(k) == v for k, v in where.items()):
            vals[o["name"]].append(float(o["role"] == "b") if measure == "flip" else o["frac"])
    return {n: statistics.mean(v) for n, v in vals.items()}


def verdicts(outcomes: list[dict], measure: str) -> dict:
    s = {
        (p, n): scores(outcomes, measure, part=p, null=n, source="cf")
        for p in (*PARTS, *MATCHED, "full")
        for n in (False, True)
    }

    def diff(a, b):
        names = sorted(set(s[a]) & set(s[b]))
        return paired_bootstrap_diff([s[a][x] for x in names], [s[b][x] for x in names], N_BOOT, BOOT_SEED)

    out: dict[str, Any] = {
        "means": {f"{p}{' null' if n else ''}": statistics.mean(v.values()) for (p, n), v in s.items() if v}
    }
    off = scores(outcomes, measure, part="full", source="off")
    out["means"]["O full"] = statistics.mean(off.values()) if off else None
    for inside, outside in (("lens2", "not_lens2"), ("jspace", "not_jspace")):
        d = {f"{outside} - {inside}": diff((outside, False), (inside, False)),
             f"{inside} - {inside}_matched": diff((inside, False), (f"{inside}_matched", False)),
             f"{inside} - its null": diff((inside, False), (inside, True)),
             f"{outside} - its null": diff((outside, False), (outside, True))}  # fmt: skip
        specific = d[f"{inside} - {inside}_matched"][1] > 0
        rest_larger = d[f"{outside} - {inside}"][1] > 0
        verdict = {(True, False): "inside", (True, True): "both", (False, True): "outside"}.get(
            (specific, rest_larger), "neither"
        )
        old = "both or neither"
        if d[f"{outside} - {inside}"][1] > 0 and d[f"{inside} - its null"][1] <= 0:
            old = "outside"
        elif d[f"{outside} - {inside}"][2] < 0 and d[f"{outside} - its null"][1] <= 0:
            old = "inside"
        out[inside] = {**d, "verdict": verdict, "verdict_exp09": old}
    return out


def summarize_parts(outcomes: list[dict], fve: list[dict], window: dict) -> dict:
    out: dict[str, Any] = {"families": {}}
    for fam, win in window.items():
        if not win:
            out["families"][fam] = {"window": [], "verdicts": "not interpreted (empty window)"}
            continue
        rows = [o for o in outcomes if o["family"] == fam]
        shares: dict[str, list[float]] = collections.defaultdict(list)
        for f in fve:
            if f.get("family") == fam:
                shares[f["what"]].append(f["share"])
        out["families"][fam] = {
            "window": win,
            "n": len({o["name"] for o in rows}),
            "frac": verdicts(rows, "frac"),
            "flip": verdicts(rows, "flip"),
            "variance_share_median": {k: statistics.median(v) for k, v in shares.items()},
        }
    fam = out["families"]

    def v(f: str, measure: str = "frac") -> str | None:
        return fam[f][measure]["jspace"]["verdict"] if isinstance(fam.get(f, {}).get(measure), dict) else None

    claims: dict[str, Any] = {}
    if "BL" in fam:
        if v("BL") is None:
            claims["claim_1"] = "BL not interpreted (empty window)"
        else:
            claims["claim_1"] = {"outside": "supported (BL outside)", "inside": "refuted (BL inside)",
                                 "both": "refuted (BL both)"}.get(v("BL") or "", f"not refuted, not supported (BL {v('BL')})")  # fmt: skip
        claims["lookup_used"] = {f: v(f) for f in LOOKUP_USED if f in fam}
    if "BLR" in fam and "BRL" in fam:
        a, b = v("BLR"), v("BRL")
        claims["tie_break"] = ("what uses the bridge decides" if a == "outside" and b in ("inside", "both") else
                               "where the answer comes from decides" if a in ("inside", "both") and b == "outside" else
                               f"mixed: BLR {a}, BRL {b}")  # fmt: skip
    out["claims"] = claims
    out["chance_share"] = statistics.median(f["share"] for f in fve if f["what"] == "chance")
    return out


def write_parts_md(path: Path, run: str, summary: dict) -> None:
    def pts(d):
        return f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"

    lines = [
        f"# {EXP} / {run}",
        "",
        f"Claims (the manifest's rules, primary measure): {json.dumps(summary['claims'])}",
        "",
    ]
    for fam, s in summary["families"].items():
        lines += [f"## {fam}: window {s['window']}", ""]
        if "frac" not in s:
            lines += [str(s["verdicts"]), ""]
            continue
        for measure in ("frac", "flip"):
            d = s[measure]
            lines.append(
                f"{measure} (n={s['n']}): "
                + ", ".join(f"{k} {100 * x:.0f}%" for k, x in d["means"].items() if x is not None)
            )
            for part in ("jspace", "lens2"):
                lines.append(f"- {part}: " + "; ".join(f"{k} {pts(x)}" for k, x in d[part].items() if not k.startswith("verdict"))
                             + f"; verdict: {d[part]['verdict']} (exp09's rule: {d[part]['verdict_exp09']})")  # fmt: skip
            lines.append("")
        lines += [
            "Median share of delta's variance: "
            + ", ".join(f"{k} {x:.3f}" for k, x in s["variance_share_median"].items()),
            "",
        ]
    lines.append(f"Chance share (a random direction's J-space part): {summary['chance_share']:.3f}")
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest_map", "run_map", "manifest_parts", "run_parts"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--map")
    ap.add_argument("--families", nargs="+", choices=list(S.FAMILIES + S.TIEBREAK))
    ap.add_argument("--wording", choices=["A", "B"], default="A", help="manifest_map: suite_v1's wording A or B")
    ap.add_argument(
        "--scenes", type=int, default=N_SCENES, help="manifest_map: scenes per scene group (a smoke run: few)"
    )
    args = ap.parse_args()
    if args.stage == "manifest_map":
        assert args.why, "manifest_map needs --why"
        assert args.families, "manifest_map needs --families"
        stage_manifest_map(args.name, args.why, args.families, args.scenes, args.wording)
    elif args.stage == "run_map":
        stage_run_map(args.name)
    elif args.stage == "manifest_parts":
        assert args.why, "manifest_parts needs --why"
        assert args.map, "manifest_parts needs --map"
        stage_manifest_parts(args.name, args.map, args.why)
    else:
        stage_run_parts(args.name)
