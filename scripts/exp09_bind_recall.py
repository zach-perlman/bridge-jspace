"""exp09_bind_recall: is a recalled bridge in the J-space and a bridge bound in context not? Both part B methods.

Part B found the two-hop bridge acting through its J-space part when it is recalled (exp02's probe swaps), and brew's
intermediate, computed in context, carried outside the J-space (exp04's patching split, exp07). The settings differ in
much more than where the bridge comes from. This run holds the question, the countries and the second hop fixed and
changes only that (data/bind_recall.json, scripts/exp09_make_items.py; three people with countries come first, and
every prompt names the bridge I, the target X and a third country Z):

  R  "... The capital of the country where {city} is located is"     the bridge recalled from the city
  B  "... The capital of the country where {person} lives is"        the bridge bound to the person in the prompt

Counterfactuals, as exp04's (one binding rewritten, every country still in the prompt): C sets the bridge to X (R: the
city replaced by a city of X; B: the queried person and X's holder swap countries); O swaps X's and Z's holders (off
the path; the answer stays). Both part B methods run on both families:
  map    (exp04) copy C's (or O's) block output into the original at a position group, one layer at a time (0-60,
         every 4th): 'question' (the question's tokens after the changed ones), 'last'
  parts  (exp04_brew_parts) at the question group's window, below the layer where the last token alone already carries
         the answer: the copy split into its J-space part (25-atom signed OMP over J++'s letter-token vectors) and the
         rest, and into its projection on J++'s v_I, v_X and the rest; each against a matched-norm random direction
  swaps  (exp02) exp01's J++ probes of I and X swapped at the cue phrase (R: the city to 'located'; B: the person and
         'lives'), layers 24-40 at once: the J-part, the full probe, the remainder and the matched-alignment control,
         each with its random-direction null
Success everywhere: the answer becomes X's capital.

Stages (manifests are written before their runs and are write-once):
  check                                   tokenizer only: alignment per family
  manifest_map --name M --why "..."       run_map M
  manifest_parts --name P --map M --why   run_parts P
  manifest_swaps --name S --why "..."     run_swaps S
"""

import argparse
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
PROBES = pins.CACHE_DIR / "exp01" / "v3_jpp" / "probes.pt"  # exp01's J++ probes, as exp02's main_v4_jpp and exp06
SWAP_LAYERS = tuple(range(24, 41))  # exp02's band 24-40
SWAP_CONDITIONS = ("jpart", "full_probe", "remainder", "jpart_matched")
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")


def context(people: list[str], countries: list[str]) -> str:
    return " ".join(f"{p} lives in {c}." for p, c in zip(people, countries, strict=True))


def variants(item: dict, index: int) -> dict[str, str]:
    """C (the bridge set to X) and O (X's and Z's holders swap, off the path) prompts for an item."""
    people, held = item["people"], item["countries"]
    question = item["prompt"][len(context(people, held)) + 1 :]
    i_b, i_x, i_z = (held.index(c) for c in (item["bridge"], item["target"], item["third"]))

    def swapped(i: int, j: int) -> list[str]:
        out = list(held)
        out[i], out[j] = out[j], out[i]
        return out

    if item["family"] == "R":
        city2 = random.Random(CF_SEED + index).choice(CITIES[item["target"]])
        cf = f"{context(people, held)} {question.replace(f'where {item["cue"]} is', f'where {city2} is')}"
    else:
        cf = f"{context(people, swapped(i_b, i_x))} {question}"
    return {"cf": cf, "off": f"{context(people, swapped(i_x, i_z))} {question}"}


def changed_tokens(a: list[int], b: list[int]) -> list[int] | None:
    """The positions where two equal-length token lists differ (None if the lengths differ or nothing differs)."""
    if len(a) != len(b):
        return None
    diff = [i for i, (p, q) in enumerate(zip(a, b, strict=True)) if p != q]
    return diff or None


def prepare(item: dict, index: int, tokenizer) -> dict:
    """Token ids of B, C and O, their changed positions, the position groups downstream of C's change, and the cue
    phrase (from the cue word to the word before the final ' is', as exp02's cue spans)."""
    texts = {"clean": item["prompt"], **variants(item, index)}
    enc = {k: tokenizer(t, add_special_tokens=False, return_offsets_mapping=True) for k, t in texts.items()}
    ids = {k: e.input_ids for k, e in enc.items()}
    changed = {s: changed_tokens(ids["clean"], ids[s]) for s in ("cf", "off")}
    out: dict[str, Any] = {"ids": ids, "changed": changed}
    expected = {"cf": 1 if item["family"] == "R" else 2, "off": 2}
    if any(changed[s] is None or len(changed[s]) != n for s, n in expected.items()):
        out["status"] = "unaligned"
        return out
    prompt, offsets = item["prompt"], enc["clean"].offset_mapping
    q_start, cue_start, cue_end = prompt.index("The capital"), prompt.rindex(item["cue"]), prompt.rindex(" is")
    after = max(changed["cf"])
    out["groups"] = {
        "question": [i for i, (_, e) in enumerate(offsets) if e > q_start and i > after],
        "last": [len(offsets) - 1],
        "cue": [i for i, (s, e) in enumerate(offsets) if e > cue_start and s < cue_end],
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
            "C": "the bridge set to X, every country still in the prompt. R: the city replaced by a city of X (seed "
            "9000 + index); B: the queried person and X's holder swap countries",
            "O": "X's and Z's holders swap countries (off the path; the answer stays)",
        },
        "groups": {
            "question": "the question's tokens after C's changed ones (R: after the city; B: the whole question)",
            "last": "the last token",
            "cue": "the cue phrase, from the cue word to the word before the final ' is' (the swaps' positions)",
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
        "the answer at all (Wilson 95% intervals not overlapping)",
        "answer_formed": "per family, the first layer at which copying the last token alone gives X's capital for at "
        "least half the items: from there the copy can carry the answer rather than the bridge",
        "parts_window": f"the question group's window below min(answer_formed, {ANSWER_ONSET}) ({ANSWER_ONSET}: exp12's "
        "answer onset at the last word); if it is empty, that family's parts are not interpreted",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def eligible_cases(
    model, tokenizer, layers: tuple[int, ...] | None, sources: tuple[str, ...] = ("clean", "cf", "off")
) -> tuple[list[dict], list[dict]]:
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
            for source in sources:
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
    summary = {
        "items": status_counts(rows),
        "windows": windows(outcomes),
        "answer_formed": answer_formed(outcomes),
        "rates": map_rates(outcomes),
    }
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


def answer_formed(outcomes: list[dict]) -> dict[str, int]:
    """Per family, the first layer at which the last token's copy alone gives X's capital for half the items or more."""
    out = {}
    for r in map_rates(outcomes):
        if r["group"] == "last" and r["b"][0] >= 0.5 and r["family"] not in out:
            out[r["family"]] = r["layer"]
    return out


def stage_manifest_parts(name: str, map_run: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    map_summary = RESULTS / map_run / "summary.json"
    blob = json.loads(map_summary.read_text())
    cap = {f: min(blob["answer_formed"].get(f, ANSWER_ONSET), ANSWER_ONSET) for f in FAMILIES}
    window = {
        f: [layer for layer in blob["windows"].get(f, {}).get("question", []) if layer < cap[f]] for f in FAMILIES
    }
    manifest = manifest_common(name, why, "bind_recall_parts")
    manifest["question"] = (
        "At each family's window, which part of the copy carries the bridge: its J-space part or the rest?"
    )
    manifest["map"] = {"run": map_run, "summary_sha256": sha256_of(map_summary), "cap": cap, "parts_window": window}
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
    window = manifest["map"]["parts_window"]
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


def stage_manifest_swaps(name: str, why: str) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = manifest_common(name, why, "bind_recall_swaps")
    manifest["question"] = (
        "Does swapping the bridge's J-space part (exp01's probe, exp02's method) change the answer when "
    )
    manifest["question"] += "the bridge is recalled, and when it is bound in context?"
    manifest["probes"] = {"file": str(PROBES.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(PROBES)}
    manifest["swap"] = {
        "positions": "the cue phrase (R: the city, 'is', 'located'; B: the person, 'lives'), as exp02's cue regime",
        "layers": f"{SWAP_LAYERS[0]}-{SWAP_LAYERS[-1]} at once (exp02's band); a layer is skipped if I's and X's atoms "
        "are near parallel",
        "conditions": "exp02's: the J-part, the full probe, the remainder, the matched-alignment direction (the J-part's "
        "cosine to the probe, the rest random); atoms I and X swapped by the coordinate clamp",
        "null": "each condition's edit along seeded random directions at the edit's own norm (exp02's null)",
    }
    manifest["decision"] = {
        "flip": "per item, the swapped greedy continuation's first capital is X's; paired bootstraps over items",
        "positive_control": "per family, the full probe's swap flips more often than its null (CI above 0); otherwise "
        "the probes do not move that family's bridge and its swaps are not interpreted",
        "j_space": "per family, the J-part flips more often than the matched-alignment control (CI above 0): the "
        "J-space part carries the bridge (exp02's result on recalled bridges)",
        "hypothesis": "supported if j_space holds in R and not in B (both positive controls passing); refuted if it "
        "holds in B; otherwise inconclusive",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run_swaps(name: str) -> None:
    from bridge_jspace.clamp import SwapClamp, near_parallel
    from bridge_jspace.model import load_model
    from scripts.exp02_swaps import Probes, condition_atoms

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    assert sha256_of(PROBES) == manifest["probes"]["sha256"], "probes.pt changed since the manifest"
    model = load_model()
    tokenizer: Any = model.tokenizer
    capitals = [c.lower() for c in CAPITALS.values()]
    probes = Probes(PROBES)
    cases, rows = eligible_cases(model, tokenizer, SWAP_LAYERS, sources=("clean",))
    outcomes = []
    for c in cases:
        ids = torch.tensor([c["ids"]["clean"]], device="cuda")
        pair = {"intermediate": c["bridge"], "swap_to": c["target"]}
        for ci, condition in enumerate(SWAP_CONDITIONS):
            atoms = {layer: condition_atoms(condition, pair, layer, probes, None, model) for layer in SWAP_LAYERS}
            for null in (False, True):
                g = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1000 * c["index"] + ci) if null else None
                clamps = {}
                for layer, at in atoms.items():
                    direction = None
                    if g is not None:  # drawn for every layer, so a layer's direction does not depend on skips
                        direction = torch.nn.functional.normalize(
                            torch.randn(at.shape[1], device="cuda", generator=g), dim=0
                        )
                    if not near_parallel(at[0], at[1]):
                        clamps[layer] = SwapClamp(
                            at, c["h"]["clean"][layer], null_direction=direction, positions=c["groups"]["cue"]
                        )
                said = answer_colour(model.generate(ids, MAX_NEW_TOKENS, clamps)[1], capitals)
                outcomes.append(
                    {
                        "family": c["family"],
                        "name": c["name"],
                        "condition": condition,
                        "null": null,
                        "said": said,
                        "role": role_of(said, c),
                        "layers_skipped": len(atoms) - len(clamps),
                    }
                )
        print(f"{c['name']}: done ({len(outcomes)} outcomes)", flush=True)
    write_jsonl(out_dir / "items.jsonl", rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = summarize_swaps(outcomes)
    summary["items"] = status_counts(rows)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [
        f"# {EXP} / {name}",
        "",
        f"Items: {json.dumps(summary['items'])}",
        "",
        f"Hypothesis (the J-part carries a recalled bridge, not a bound one): {summary['hypothesis']}",
        "",
    ]
    for family, f in summary["families"].items():
        lines += [f"## {family} (n={f['n']})", ""]
        lines += [f"- {k}: {100 * v[0]:.0f}% [{100 * v[1]:.0f}, {100 * v[2]:.0f}]" for k, v in f["rates"].items()]
        lines += [f"- {k}: {pts(v)}" for k, v in f["comparisons"].items()]
        lines += [f"- positive control: {f['positive_control']}; J-space carries it: {f['j_space']}", ""]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


def summarize_swaps(outcomes: list[dict]) -> dict:
    out: dict[str, Any] = {"families": {}}
    for family in FAMILIES:
        rows = [o for o in outcomes if o["family"] == family]
        flip = {
            (cond, null): {
                o["name"]: float(o["role"] == "b") for o in rows if (o["condition"], o["null"]) == (cond, null)
            }
            for cond in SWAP_CONDITIONS
            for null in (False, True)
        }

        def diff(a, b, flip=flip):
            names = sorted(set(flip[a]) & set(flip[b]))
            return paired_bootstrap_diff([flip[a][n] for n in names], [flip[b][n] for n in names], N_BOOT, BOOT_SEED)

        comparisons = {
            "full_probe - its null": diff(("full_probe", False), ("full_probe", True)),
            "jpart - jpart_matched": diff(("jpart", False), ("jpart_matched", False)),
            "jpart - its null": diff(("jpart", False), ("jpart", True)),
            "remainder - its null": diff(("remainder", False), ("remainder", True)),
        }
        out["families"][family] = {
            "n": len(flip["jpart", False]),
            "rates": {
                f"{c}{' null' if n else ''}": wilson(round(sum(v.values())), len(v)) for (c, n), v in flip.items()
            },
            "comparisons": comparisons,
            "positive_control": comparisons["full_probe - its null"][1] > 0,
            "j_space": comparisons["jpart - jpart_matched"][1] > 0,
        }
    f = out["families"]
    if not (f["R"]["positive_control"] and f["B"]["positive_control"]):
        out["hypothesis"] = "not interpreted (a positive control failed)"
    elif f["B"]["j_space"]:
        out["hypothesis"] = "refuted"
    else:
        out["hypothesis"] = "supported" if f["R"]["j_space"] else "inconclusive"
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "stage",
        choices=["check", "manifest_map", "run_map", "manifest_parts", "run_parts", "manifest_swaps", "run_swaps"],
    )
    parser.add_argument("target", nargs="?", help="run_map / run_parts: the run's folder name")
    parser.add_argument("--name", help="manifest_*: the run's folder name")
    parser.add_argument("--map", dest="map_run", help="manifest_parts: the map run")
    parser.add_argument("--why", help="manifest_*: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check()
    elif args.stage in ("manifest_map", "manifest_parts", "manifest_swaps"):
        assert args.name, "manifests need --name"
        assert args.why, "manifests need --why"
        if args.stage == "manifest_map":
            stage_manifest_map(args.name, args.why)
        elif args.stage == "manifest_swaps":
            stage_manifest_swaps(args.name, args.why)
        else:
            assert args.map_run, "manifest_parts needs --map"
            stage_manifest_parts(args.name, args.map_run, args.why)
    elif args.stage == "run_map":
        assert args.target, "run_map needs the run's folder name"
        stage_run_map(args.target)
    elif args.stage == "run_parts":
        assert args.target, "run_parts needs the run's folder name"
        stage_run_parts(args.target)
    else:
        assert args.target, "run_swaps needs the run's folder name"
        stage_run_swaps(args.target)
