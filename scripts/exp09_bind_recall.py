"""exp09_bind_recall: is a recalled bridge in the J-space and a bridge bound in context not? exp04's pipeline on both.

Part B found the two-hop bridge acting through its J-space part when it is recalled (exp02), and brew's intermediate,
computed in context, carried outside the J-space (exp04 parts, exp07). The two settings differ in much more than where
the bridge comes from. This run holds the question, the countries and the second hop fixed and changes only that
(data/bind_recall.json, scripts/exp09_make_items.py):

  R  "{N1} lives in {cA}. {N2} lives in {cB}. The capital of the country where {city} is located is"   (recalled)
  B  "{N1} lives in {c1}. {N2} lives in {c2}. The capital of the country where {Nq} lives is"          (bound)

and runs on both exactly what gave brew's verdict, exp04's two stages, lens-free first:
  counterfactuals (one token changed, token-aligned):
    C  R: the city -> a city of X;  B: the queried person's country -> X  (X: a country not in the prompt); answer X's
    O  the other context country -> another country (off the path; the answer stays)
  map    copy C's (or O's) block output into the original at a position group, one layer at a time (0-60, every 4th),
         downstream of the changed token only: 'question' (the question's tokens, the changed one excluded), 'last'
  window per group, exp04's rule: the layers where C's copy gives X's capital more often than O's copy changes the
         answer (Wilson intervals not overlapping); the parts use the question group's window below layer 44
  parts  at the window, the copy δ = h_C - h_B split as exp04_brew_parts: its J-space part (25-atom signed OMP over
         J++'s letter-token vectors) and the rest, its projection on J++'s v_I, v_X and the rest; each part also along a
         matched-norm random direction. Step score: per item, the share of window layers giving X's capital.

Stages (manifests are written before their runs and are write-once):
  check                                   tokenizer only: alignment and single-token counts per family
  manifest_map --name M --why "..."
  run_map M
  manifest_parts --name P --map M --why "..."
  run_parts P
"""

import argparse
import json
import random
import re
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
from scripts.exp03_brew_swaps import answer_colour, write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp
from scripts.exp09_make_items import CAPITALS, CITIES

EXP = "exp09_bind_recall"
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("R", "B")
GROUPS = ("question", "last")
MAP_LAYERS = tuple(range(0, 61, 4))
ANSWER_ONSET = 44  # exp12: the answer is read at the last word from about layer 44; the parts stay below it
N_ITEMS = 80  # per family, a seeded sample of the eligible items
MAX_NEW_TOKENS = 8
CF_SEED, OFF_SEED, SAMPLE_SEED, NULL_SEED = 9000, 9500, 0, 0
N_BOOT, BOOT_SEED = 2000, 0
CHANCE_DRAWS = 20
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")
SENTENCES = re.compile(r"^(\w+) lives in (\w+)\. (\w+) lives in (\w+)\. ")


def variants(item: dict, index: int) -> dict[str, str]:
    """C and O prompts for an item: C changes the bridge to the item's target X, O an off-path country."""
    prompt, x = item["prompt"], item["target"]
    n1, c1, n2, c2 = SENTENCES.match(prompt).groups()  # type: ignore[union-attr]
    if item["family"] == "R":
        city2 = random.Random(CF_SEED + index).choice(CITIES[x])
        cf = prompt.replace(f"where {item['cue']} is", f"where {city2} is")
        off_name, off_country = n1, c1
    else:
        queried_first = item["cue"] == n1
        cf = prompt.replace(f"{item['cue']} lives in {item['bridge']}.", f"{item['cue']} lives in {x}.", 1)
        off_name, off_country = (n2, c2) if queried_first else (n1, c1)
    taken = {item["bridge"], x, c1, c2}
    new = random.Random(OFF_SEED + index).choice([c for c in CAPITALS if c not in taken])
    off = prompt.replace(f"{off_name} lives in {off_country}.", f"{off_name} lives in {new}.", 1)
    return {"cf": cf, "off": off}


def changed_token(a: list[int], b: list[int]) -> int | None:
    """The one position where two equal-length token lists differ, else None."""
    if len(a) != len(b):
        return None
    diff = [i for i, (p, q) in enumerate(zip(a, b, strict=True)) if p != q]
    return diff[0] if len(diff) == 1 else None


def prepare(item: dict, index: int, tokenizer) -> dict:
    """Token ids of B, C and O, the changed position of each, and the position groups (downstream of C's change)."""
    texts = {"clean": item["prompt"], **variants(item, index)}
    enc = {k: tokenizer(t, add_special_tokens=False, return_offsets_mapping=True) for k, t in texts.items()}
    ids = {k: e.input_ids for k, e in enc.items()}
    changed = {s: changed_token(ids["clean"], ids[s]) for s in ("cf", "off")}
    out: dict[str, Any] = {"ids": ids, "changed": changed}
    if None in changed.values():
        out["status"] = "unaligned"
        return out
    q_start = item["prompt"].index("The capital")
    offsets = enc["clean"].offset_mapping
    last = len(offsets) - 1
    out["groups"] = {
        "question": [i for i, (_, e) in enumerate(offsets) if e > q_start and i > changed["cf"]],
        "last": [last],
    }
    out["status"] = "ok"
    return out


def roles(item: dict) -> dict[str, str]:
    return {"A": CAPITALS[item["bridge"]].lower(), "b": CAPITALS[item["target"]].lower()}


def role_of(said: str | None, item: dict) -> str:
    if said is None:
        return "none"
    return next((r for r, c in roles(item).items() if c == said), "other")


def stage_check() -> None:
    from bridge_jspace.tokens import load_tokenizer

    tokenizer = load_tokenizer()
    for family in FAMILIES:
        counts: dict[str, int] = {}
        sizes: dict[int, int] = {}
        for index, item in enumerate(pins.bind_recall_items()):
            if item["family"] != family:
                continue
            prep = prepare(item, index, tokenizer)
            counts[prep["status"]] = counts.get(prep["status"], 0) + 1
            if prep["status"] == "ok":
                n = len(prep["groups"]["question"])
                sizes[n] = sizes.get(n, 0) + 1
        print(family, counts, "question-group sizes:", sizes)


def manifest_common(name: str, why: str, kind: str) -> dict:
    return {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "items": {
            "file": str(pins.BIND_RECALL_FILE.relative_to(pins.REPO_ROOT)),
            "sha256": pins.BIND_RECALL_SHA256,
            "per_family": f"{N_ITEMS}, a seeded sample (seed {SAMPLE_SEED}) of the eligible items",
        },
        "eligibility": "B, C and O each change one token against the original (token-aligned), and the greedy "
        "continuations' first capital of the set is the bridge's (B, O) and X's (C)",
        "counterfactuals": {
            "C": "R: the city replaced by a city of X (seed 9000 + index); B: the queried person's country replaced by X",
            "O": "the other context country replaced by a country not in the prompt and not X (seed 9500 + index)",
        },
        "groups": {
            "question": "the question's tokens after the changed one (R: after the city; B: the whole question)",
            "last": "the last token",
        },
        "outcome": "the patched greedy continuation's first capital of the set: X's capital (b), the bridge's (A), other",
    }


def stage_manifest_map(name: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = manifest_common(name, why, "bind_recall_map")
    manifest["question"] = "Where, by layer and position group, does each family carry the bridge (lens-free)?"
    manifest["layers"] = list(MAP_LAYERS)
    manifest["decision"] = {
        "window": "per family and group: the layers where C's copy gives X's capital more often than O's copy changes "
        "the answer at all (Wilson 95% intervals not overlapping). The parts use the question group's window below "
        f"layer {ANSWER_ONSET}; if it is empty there, that family's parts run is not made and the map is reported."
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def eligible_cases(model, tokenizer, layers: tuple[int, ...] | None) -> tuple[list[dict], list[dict]]:
    """Eligible items (as the manifest), a seeded sample of N_ITEMS per family, with their runs' block outputs."""
    capitals = [c.lower() for c in CAPITALS.values()]
    rows, pool = [], []
    for index, item in enumerate(pins.bind_recall_items()):
        prep = prepare(item, index, tokenizer)
        row = {"family": item["family"], "name": item["name"], "status": prep["status"]}
        rows.append(row)
        if prep["status"] != "ok":
            continue
        said = {
            k: answer_colour(model.generate(torch.tensor([v], device="cuda"), MAX_NEW_TOKENS)[1], capitals)
            for k, v in prep["ids"].items()
        }
        want = {"clean": roles(item)["A"], "cf": roles(item)["b"], "off": roles(item)["A"]}
        row["status"] = "eligible" if said == want else "not_eligible"
        if row["status"] == "eligible":
            pool.append({**item, "index": index, **prep})
    rng = random.Random(SAMPLE_SEED)
    cases = []
    for family in FAMILIES:
        mine = [c for c in pool if c["family"] == family]
        cases += rng.sample(mine, min(N_ITEMS, len(mine)))
    picked = {c["name"] for c in cases}
    for row in rows:
        if row["status"] == "eligible" and row["name"] not in picked:
            row["status"] = "eligible_not_sampled"
    if layers:
        for c in cases:
            c["h"] = {}
            for source in ("clean", "cf", "off"):
                _, rec = model.run(torch.tensor([c["ids"][source]], device="cuda"), record=layers)
                c["h"][source] = {layer: rec[layer] for layer in layers}
    return cases, rows


@torch.no_grad()
def stage_run_map(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    assert sha256_of(pins.BIND_RECALL_FILE) == manifest["items"]["sha256"], "items changed since the manifest"
    model = load_model()
    tokenizer: Any = model.tokenizer
    capitals = [c.lower() for c in CAPITALS.values()]
    cases, rows = eligible_cases(model, tokenizer, MAP_LAYERS)
    print({f: sum(c["family"] == f for c in cases) for f in FAMILIES}, "items", flush=True)
    outcomes = []
    for c in cases:
        ids = torch.tensor([c["ids"]["clean"]], device="cuda")
        for group in GROUPS:
            pos = c["groups"][group]
            for layer in MAP_LAYERS:
                for source in ("cf", "off"):
                    delta = c["h"][source][layer][pos] - c["h"]["clean"][layer][pos]
                    said = answer_colour(model.generate(ids, MAX_NEW_TOKENS, {layer: AddRows(delta, pos)})[1], capitals)
                    outcomes.append(
                        {
                            "family": c["family"],
                            "name": c["name"],
                            "group": group,
                            "layer": layer,
                            "source": source,
                            "said": said,
                            "role": role_of(said, c),
                        }
                    )
        print(f"{c['name']}: done ({len(outcomes)} outcomes)", flush=True)
    write_jsonl(out_dir / "items.jsonl", rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = {"items": status_counts(rows), "windows": windows(outcomes), "rates": map_rates(outcomes)}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        f"# {EXP} / {name}",
        "",
        f"Items: {json.dumps(summary['items'])}",
        "",
        f"Windows: {json.dumps(summary['windows'])}",
        "",
    ]
    lines += ["| family | group | layer | C gives X's capital | O changes the answer |", "|---|---|---|---|---|"]
    lines += [
        f"| {r['family']} | {r['group']} | {r['layer']} | {100 * r['b'][0]:.0f}% | {100 * r['off_changed'][0]:.0f}% |"
        for r in summary["rates"]
    ]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


def status_counts(rows: list[dict]) -> dict:
    return {
        f: {s: sum(r["family"] == f and r["status"] == s for r in rows) for s in {r["status"] for r in rows}}
        for f in FAMILIES
    }


def map_rates(outcomes: list[dict]) -> list[dict]:
    rates = []
    for family in FAMILIES:
        for group in GROUPS:
            for layer in MAP_LAYERS:
                cell = [o for o in outcomes if (o["family"], o["group"], o["layer"]) == (family, group, layer)]
                cf = [o for o in cell if o["source"] == "cf"]
                off = [o for o in cell if o["source"] == "off"]
                if not cf:
                    continue
                rates.append(
                    {
                        "family": family,
                        "group": group,
                        "layer": layer,
                        "n": len(cf),
                        "b": wilson(sum(o["role"] == "b" for o in cf), len(cf)),
                        "off_changed": wilson(sum(o["role"] != "A" for o in off), len(off)),
                    }
                )
    return rates


def windows(outcomes: list[dict]) -> dict:
    out: dict[str, dict[str, list[int]]] = {}
    for r in map_rates(outcomes):
        if r["b"][1] > r["off_changed"][2]:
            out.setdefault(r["family"], {}).setdefault(r["group"], []).append(r["layer"])
    return out


def stage_manifest_parts(name: str, map_run: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    map_summary = RESULTS / map_run / "summary.json"
    found = json.loads(map_summary.read_text())["windows"]
    window = {f: [layer for layer in found.get(f, {}).get("question", []) if layer < ANSWER_ONSET] for f in FAMILIES}
    manifest = manifest_common(name, why, "bind_recall_parts")
    manifest["question"] = (
        "At each family's window, which part of the copy carries the bridge: its J-space part or the rest?"
    )
    manifest["map"] = {"run": map_run, "summary_sha256": sha256_of(map_summary), "window_question_below_44": window}
    manifest["lens"] = {"jpp": pins.LENS_FILES["jpp"]}
    manifest["parts"] = {
        "full": "δ = h_C - h_B at the question group",
        "lens2": "δ's projection on span{v_I, v_X}, J++'s unit vectors of the two countries; not_lens2 the rest",
        "jspace": f"δ's {K_ATOMS}-atom signed OMP part over J++'s unit letter-token vectors; not_jspace the rest",
    }
    manifest["controls"] = "each part along a seeded random direction at the same per-position norm; O's full copy"
    manifest["decision"] = {
        "step_score": "per item, the share of window layers at which the copy gives X's capital; paired bootstraps",
        "parts": "per family, exp04's rule: outside if not_jspace - jspace is above 0 and jspace - its null is not; "
        "inside if jspace - not_jspace is above 0 and not_jspace - its null is not; otherwise both or neither (the "
        "same for lens2)",
        "hypothesis": "supported if R is 'inside' or 'both or neither' with jspace above its null, and B is 'outside'; "
        "refuted if B's jspace is above its null; a family with an empty window is not interpreted",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run_parts(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    map_summary = RESULTS / manifest["map"]["run"] / "summary.json"
    assert sha256_of(map_summary) == manifest["map"]["summary_sha256"], "the map changed since the manifest"
    window = manifest["map"]["window_question_below_44"]
    layers = tuple(sorted({layer for v in window.values() for layer in v}))
    assert layers, "no family has a window"
    model = load_model()
    tokenizer: Any = model.tokenizer
    capitals = [c.lower() for c in CAPITALS.values()]
    cases, rows = eligible_cases(model, tokenizer, layers)
    lens = JLens(model, "jpp")
    dictionaries = {layer: lens.vectors(layer, model.letter_token_ids()) for layer in layers}
    outcomes, fve = [], []
    g = torch.Generator(device="cuda").manual_seed(BOOT_SEED)
    for layer in layers:
        x = torch.randn(CHANCE_DRAWS, dictionaries[layer].shape[1], device="cuda", generator=g)
        share = (signed_omp(dictionaries[layer], x, K_ATOMS).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
        fve.append({"layer": layer, "what": "chance", "share": round(float(share), 4)})
    for c in cases:
        ids = torch.tensor([c["ids"]["clean"]], device="cuda")
        pos = c["groups"]["question"]
        tok = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["target"])], device="cuda")

        def run(layer, delta, c=c, ids=ids, pos=pos, **tags):
            said = answer_colour(model.generate(ids, MAX_NEW_TOKENS, {layer: AddRows(delta, pos)})[1], capitals)
            outcomes.append(
                {
                    "family": c["family"],
                    "name": c["name"],
                    "layer": layer,
                    **tags,
                    "said": said,
                    "role": role_of(said, c),
                }
            )

        for layer in window[c["family"]]:
            delta = c["h"]["cf"][layer][pos] - c["h"]["clean"][layer][pos]
            run(layer, delta, part="full", source="cf", null=False)
            run(layer, c["h"]["off"][layer][pos] - c["h"]["clean"][layer][pos], part="full", source="off", null=False)
            lens2 = lens2_part(delta, lens.vectors(layer, tok))
            jspace = signed_omp(dictionaries[layer], delta, K_ATOMS)
            total = float(delta.norm() ** 2)
            for what, part in (("lens2", lens2), ("jspace", jspace)):
                fve.append(
                    {
                        "family": c["family"],
                        "name": c["name"],
                        "layer": layer,
                        "what": what,
                        "share": round(float(part.norm() ** 2) / total, 4),
                    }
                )
            parts = {"lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace, "not_jspace": delta - jspace}
            for pi, (part_name, part) in enumerate(parts.items()):
                run(layer, part, part=part_name, source="cf", null=False)
                seed = NULL_SEED + 1000 * c["index"] + 10 * layer + pi
                noise = null_rows(part, torch.Generator(device="cuda").manual_seed(seed))
                run(layer, noise, part=part_name, source="cf", null=True)
        print(f"{c['name']}: done ({len(outcomes)} outcomes)", flush=True)
    write_jsonl(out_dir / "items.jsonl", rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "fve.jsonl", fve)
    summary = summarize_parts(outcomes, fve, window)
    summary["items"] = status_counts(rows)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_parts_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def step_scores(outcomes: list[dict], **where) -> dict[str, float]:
    hits: dict[str, list[bool]] = {}
    for o in outcomes:
        if all(o.get(k) == v for k, v in where.items()):
            hits.setdefault(o["name"], []).append(o["role"] == "b")
    return {n: sum(v) / len(v) for n, v in hits.items()}


def summarize_parts(outcomes: list[dict], fve: list[dict], window: dict) -> dict:
    out: dict[str, Any] = {"families": {}}
    for family in FAMILIES:
        rows = [o for o in outcomes if o["family"] == family]
        if not window.get(family):
            out["families"][family] = {"window": [], "verdicts": "not interpreted (empty window)"}
            continue
        s = {(p, n): step_scores(rows, part=p, null=n, source="cf") for p in (*PARTS, "full") for n in (False, True)}

        def diff(a, b, s=s):
            names = sorted(set(s[a]) & set(s[b]))
            return paired_bootstrap_diff([s[a][n] for n in names], [s[b][n] for n in names], N_BOOT, BOOT_SEED)

        decisions = {}
        for inside, outside in (("lens2", "not_lens2"), ("jspace", "not_jspace")):
            d = {
                f"{outside} - {inside}": diff((outside, False), (inside, False)),
                f"{inside} - its null": diff((inside, False), (inside, True)),
                f"{outside} - its null": diff((outside, False), (outside, True)),
            }
            verdict = "both or neither"
            if d[f"{outside} - {inside}"][1] > 0 and d[f"{inside} - its null"][1] <= 0:
                verdict = "outside"
            elif d[f"{outside} - {inside}"][2] < 0 and d[f"{outside} - its null"][1] <= 0:
                verdict = "inside"
            decisions[inside] = {**d, "verdict": verdict}
        off = step_scores(rows, part="full", source="off")
        shares: dict[str, list[float]] = {}
        for f in fve:
            if f.get("family") == family:
                shares.setdefault(f["what"], []).append(f["share"])
        out["families"][family] = {
            "window": window[family],
            "n": len(s["full", False]),
            "step_scores": {f"{p}{' null' if n else ''}": statistics.mean(v.values()) for (p, n), v in s.items() if v},
            "off_full": statistics.mean(off.values()) if off else None,
            "decisions": decisions,
            "variance_share_median": {k: statistics.median(v) for k, v in shares.items()},
        }
    fam = out["families"]
    if all(isinstance(fam[f].get("decisions"), dict) for f in FAMILIES):
        r, b = fam["R"]["decisions"]["jspace"], fam["B"]["decisions"]["jspace"]
        verdict = "inconclusive"
        if b["jspace - its null"][1] > 0:
            verdict = "refuted"
        elif r["jspace - its null"][1] > 0 and r["verdict"] != "outside" and b["verdict"] == "outside":
            verdict = "supported"
        out["hypothesis"] = verdict
    else:
        out["hypothesis"] = "not interpreted (a family has no window)"
    out["chance_share"] = statistics.median(f["share"] for f in fve if f["what"] == "chance")
    return out


def write_parts_md(path: Path, run: str, summary: dict) -> None:
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [
        f"# {EXP} / {run}",
        "",
        f"Items: {json.dumps(summary['items'])}",
        "",
        f"Hypothesis (recalled in the J-space, bound not): {summary['hypothesis']}",
        "",
    ]
    for family, s in summary["families"].items():
        lines += [f"## {family}: window {s['window']}", ""]
        if not isinstance(s.get("decisions"), dict):
            lines += [str(s["verdicts"]), ""]
            continue
        lines += [f"Step scores (n={s['n']}): " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in s["step_scores"].items())]
        lines += [f"O's full copy: {100 * (s['off_full'] or 0):.0f}%", ""]
        for part, d in s["decisions"].items():
            lines.append(
                f"- {part}: "
                + "; ".join(f"{k} {pts(v)}" for k, v in d.items() if k != "verdict")
                + f"; verdict: {d['verdict']}"
            )
        lines += [
            "",
            "Median share of δ's variance: " + ", ".join(f"{k} {v:.3f}" for k, v in s["variance_share_median"].items()),
            "",
        ]
    lines += [f"Chance share (a random direction's): {summary['chance_share']:.3f}"]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["check", "manifest_map", "run_map", "manifest_parts", "run_parts"])
    parser.add_argument("target", nargs="?", help="run_map / run_parts: the run's folder name")
    parser.add_argument("--name", help="manifest_*: the run's folder name")
    parser.add_argument("--map", dest="map_run", help="manifest_parts: the map run")
    parser.add_argument("--why", help="manifest_*: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check()
    elif args.stage in ("manifest_map", "manifest_parts"):
        assert args.name, "manifests need --name"
        assert args.why, "manifests need --why"
        if args.stage == "manifest_map":
            stage_manifest_map(args.name, args.why)
        else:
            assert args.map_run, "manifest_parts needs --map"
            stage_manifest_parts(args.name, args.map_run, args.why)
    elif args.stage == "run_map":
        assert args.target, "run_map needs the run's folder name"
        stage_run_map(args.target)
    else:
        assert args.target, "run_parts needs the run's folder name"
        stage_run_parts(args.target)
