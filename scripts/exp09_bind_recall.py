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
from bridge_jspace.tokens import raw_encoding
from scripts.exp03_brew_swaps import answer_colour, write_jsonl
from scripts.exp03_make_items import PALETTE
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp
from scripts.exp09_make_items import CAPITALS, CITIES

EXP = "exp09_bind_recall"
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("R", "B")  # bind_recall's families (the swaps run on them only)
ITEM_SETS = {  # set -> (file, sha256, loader, families, the answer words a continuation is scored against)
    "bind_recall": (
        pins.BIND_RECALL_FILE,
        pins.BIND_RECALL_SHA256,
        pins.bind_recall_items,
        ("R", "B"),
        tuple(c.lower() for c in CAPITALS.values()),
    ),
    "bind_lookup": (pins.BIND_LOOKUP_FILE, pins.BIND_LOOKUP_SHA256, pins.bind_lookup_items, ("L",), tuple(PALETTE)),
    "recall_lookup": (
        pins.RECALL_LOOKUP_FILE,
        pins.RECALL_LOOKUP_SHA256,
        pins.recall_lookup_items,
        ("RL",),
        tuple(PALETTE),
    ),
    "bind_lookup_v2": (
        pins.BIND_LOOKUP_V2_FILE,
        pins.BIND_LOOKUP_V2_SHA256,
        pins.bind_lookup_v2_items,
        ("L",),
        tuple(PALETTE),
    ),
}
GROUPS = ("question", "last")
MAP_LAYERS = tuple(range(0, pins.N_LAYERS - 3, 4))  # every 4th layer below the final block (Qwen: 0-60)
# exp12 (Qwen3.6-27B): the answer is read at the last word from about layer 44; the parts stay below it. Other targets
# have no exp12, so their parts window stops where the map's last token carries the answer.
ANSWER_ONSET = {"qwen3.6-27b": 44}.get(pins.TARGET, pins.N_LAYERS - 1)
N_ITEMS = 80  # per family, a seeded sample of the eligible items
MAX_NEW_TOKENS = 8
CF_SEED, OFF_SEED, SAMPLE_SEED, NULL_SEED = 9000, 9500, 0, 0
N_BOOT, BOOT_SEED = 2000, 0
BATCH = 32  # edited generations per batched call (Model.generate_batch)
CHANCE_DRAWS = 20
# exp01's J++ probes (variant more_jpp, as v3_jpp behind exp02's main_v4_jpp and exp06), rebuilt on the B200 box:
# v3_jpp's cache stayed on the old box. The rebuild checks its kept prompts against v3 one by one.
# Another target: its own exp01 all_jpp probes.
PROBES = pins.CACHE_DIR / "exp01" / {"qwen3.6-27b": "v3_jpp_b200"}.get(pins.TARGET, "gemma4it_v3_jpp") / "probes.pt"


def gate_band(run: str) -> tuple[int, ...]:
    """The band an exp02 gate run picked, as layers (empty until the gate has run)."""
    summary = pins.RESULTS_DIR / "exp02_swaps" / run / "summary.json"
    if not summary.exists():
        return ()
    a, b = json.loads(summary.read_text())["decision"]["band"].split("-")
    return tuple(range(int(a), int(b) + 1))


# exp02's band 24-40 on Qwen3.6-27B; another target's band is the one its own exp02 gate (gate_v4's rule) picked.
SWAP_LAYERS = {"qwen3.6-27b": tuple(range(24, 41))}.get(pins.TARGET) or gate_band(pins.RUN_PREFIX + "gate_v4")
SWAP_CONDITIONS = ("jpart", "full_probe", "remainder", "jpart_matched")
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")


def context(people: list[str], countries: list[str]) -> str:
    return " ".join(f"{p} lives in {c}." for p, c in zip(people, countries, strict=True))


def variants(item: dict, index: int, city2: str | None = None) -> dict[str, str]:
    """C (the bridge set to X) and O (X's and Z's holders swap, off the path) prompts for an item. R: `city2`, a city
    of X (default: the first in `x_cities` order)."""
    people, held = item["people"], item["countries"]
    question = item["prompt"][len(context(people, held)) + 1 :]
    i_b, i_x, i_z = (held.index(c) for c in (item["bridge"], item["target"], item["third"]))

    def swapped(i: int, j: int) -> list[str]:
        out = list(held)
        out[i], out[j] = out[j], out[i]
        return out

    if item["family"] in ("R", "RL"):  # the bridge recalled from the city: C changes the city
        city2 = city2 or x_cities(item, index)[0]
        cf = f"{context(people, held)} {question.replace(f'where {item["cue"]} is', f'where {city2} is')}"
    else:
        cf = f"{context(people, swapped(i_b, i_x))} {question}"
    return {"cf": cf, "off": f"{context(people, swapped(i_x, i_z))} {question}"}


def x_cities(item: dict, index: int) -> list[str]:
    """X's cities in a seeded order (seed 9000 + index): R's C takes the first that keeps the tokens aligned."""
    cities = list(CITIES[item["target"]])
    random.Random(CF_SEED + index).shuffle(cities)
    return cities


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
    if item["family"] in ("R", "RL"):  # the first city of X whose prompt lines up with the original token for token
        n = len(raw_encoding(tokenizer, item["prompt"])["input_ids"])
        fits = [
            c
            for c in x_cities(item, index)
            if len(raw_encoding(tokenizer, variants(item, index, c)["cf"])["input_ids"]) == n
        ]
        texts = {"clean": item["prompt"], **variants(item, index, fits[0] if fits else None)}
    enc = {k: raw_encoding(tokenizer, t, offsets=True) for k, t in texts.items()}  # the target's BOS first, if any
    ids = {k: e["input_ids"] for k, e in enc.items()}
    changed = {s: changed_tokens(ids["clean"], ids[s]) for s in ("cf", "off")}
    out: dict[str, Any] = {"ids": ids, "changed": changed}
    expected = {"cf": 1 if item["family"] in ("R", "RL") else 2, "off": 2}
    cf_changed, off_changed = changed["cf"], changed["off"]
    if (
        cf_changed is None
        or off_changed is None
        or (len(cf_changed), len(off_changed)) != (expected["cf"], expected["off"])
    ):
        out["status"] = "unaligned"
        return out
    prompt, offsets = item["prompt"], enc["clean"]["offset_mapping"]
    q_start, cue_start, cue_end = prompt.rindex("The "), prompt.rindex(item["cue"]), prompt.rindex(" is")
    after = max(cf_changed)
    out["groups"] = {
        "question": [i for i, (_, e) in enumerate(offsets) if e > q_start and i > after],
        "last": [len(offsets) - 1],
        "cue": [i for i, (s, e) in enumerate(offsets) if e > cue_start and s < cue_end],
    }
    out["status"] = "ok"
    return out


def roles(item: dict) -> dict[str, str]:
    """A: the original answer (the bridge's capital, or in L its colour); b: X's."""
    return {"A": item["answer"].lower(), "b": item["target_answer"].lower()}


def role_of(said: str | None, item: dict) -> str:
    if said is None:
        return "none"
    return next((r for r, c in roles(item).items() if c == said), "other")


def stage_check() -> None:
    from bridge_jspace.tokens import load_tokenizer

    tokenizer = load_tokenizer()
    for family in ("R", "B", "L", "RL"):
        counts: dict[str, int] = {}
        sizes: dict[int, int] = {}
        items = {"L": pins.bind_lookup_v2_items, "RL": pins.recall_lookup_items}.get(family, pins.bind_recall_items)()
        for index, item in enumerate(items):
            if item["family"] != family:
                continue
            prep = prepare(item, index, tokenizer)
            counts[prep["status"]] = counts.get(prep["status"], 0) + 1
            if prep["status"] == "ok":
                n = len(prep["groups"]["question"])
                sizes[n] = sizes.get(n, 0) + 1
        print(family, counts, "question-group sizes:", sizes)


def manifest_common(name: str, why: str, kind: str, item_set: str = "bind_recall") -> dict:
    pins.check_run_name(name)
    path, sha = ITEM_SETS[item_set][:2]
    return {
        "exp": EXP,
        "run": name,
        "kind": kind,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "items": {
            "set": item_set,
            "file": str(path.relative_to(pins.REPO_ROOT)),
            "sha256": sha,
            "per_family": f"{N_ITEMS}, a seeded sample (seed {SAMPLE_SEED}) of the eligible items",
        },
        "eligibility": "B, C and O each change one token against the original (token-aligned), and the greedy "
        "continuations' first answer word of the set (R, B: the capitals; L: the colours) is the bridge's (B, O) and X's (C)",
        "counterfactuals": {
            "C": "the bridge set to X, every country still in the prompt. R: the city replaced by the first city of X, "
            "in a seeded order (9000 + index), whose prompt lines up token for token; B: the queried person and X's "
            "holder swap countries; L: as B",
            "O": "X's and Z's holders swap countries (off the path; the answer stays)",
        },
        "groups": {
            "question": "the question's tokens after C's changed ones (R: after the city; B: the whole question)",
            "last": "the last token",
            "cue": "the cue phrase, from the cue word to the word before the final ' is' (the swaps' positions)",
        },
        "outcome": "the patched greedy continuation's first capital of the set: X's capital (b), the bridge's (A), other",
        "generation": f"greedy, {MAX_NEW_TOKENS} new tokens, an item's runs batched {BATCH} at a time (Model.generate_batch: "
        "equal to single runs up to batched-kernel rounding, which changed only degenerate continuations in a check)",
    }


def stage_manifest_map(name: str, why: str, item_set: str = "bind_recall") -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = manifest_common(name, why, "bind_recall_map", item_set)
    manifest["question"] = "Where, by layer and position group, does each family carry the bridge (lens-free)?"
    manifest["layers"] = list(MAP_LAYERS)
    manifest["decision"] = {
        "window": "per family and group: the layers where C's copy gives X's capital more often than O's copy changes "
        "the answer at all (Wilson 95% intervals not overlapping)",
        "answer_formed": "per family, the first layer at which copying the last token alone gives X's capital for at "
        "least half the items: from there the copy can carry the answer rather than the bridge",
        "parts_window": f"the question group's window below min(answer_formed, {ANSWER_ONSET}) ("
        + ("44: exp12's answer onset at the last word" if pins.TARGET == "qwen3.6-27b" else "no exp12 on this model")
        + "); if it is empty, that family's parts are not interpreted",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def uid(item: dict, index: int) -> str:
    """An item's id: its family and its index in its item file (data/bind_recall.json, data/bind_lookup.json). The file's own `name` field is not unique
    (exp09_make_items.py numbered each list comprehension from the same length), so nothing keys on it."""
    return f"{item['family']}-{index:04d}"


def run_jobs(model, c: dict, jobs: list[tuple[dict, dict]], capitals: list[str], outcomes: list[dict]) -> None:
    """Run an item's edited generations (tags, edits) in batches and append their outcomes."""
    ids = torch.tensor([c["ids"]["clean"]], device="cuda")
    for start in range(0, len(jobs), BATCH):
        chunk = jobs[start : start + BATCH]
        texts = model.generate_batch(ids, MAX_NEW_TOKENS, [edits for _, edits in chunk])
        for (tags, _), text in zip(chunk, texts, strict=True):
            said = answer_colour(text, capitals)
            outcomes.append({"family": c["family"], "name": c["name"], **tags, "said": said, "role": role_of(said, c)})


@torch.no_grad()
def eligible_cases(
    model,
    tokenizer,
    layers: tuple[int, ...] | None,
    sources: tuple[str, ...] = ("clean", "cf", "off"),
    map_items: Path | None = None,
    item_set: str = "bind_recall",
) -> tuple[list[dict], list[dict]]:
    """Eligible items (as the manifest), a seeded sample of N_ITEMS per family, with their runs' block outputs.
    With `map_items` (a map run's items.jsonl, one row per item in file order) the eligibility is read from that run
    instead of regenerated, and the same seeded sample follows."""
    _, _, load, families, answers = ITEM_SETS[item_set]
    capitals = list(answers)
    items = load()
    rows, pool = [], []
    before = [json.loads(line) for line in map_items.read_text().splitlines()] if map_items else None
    assert before is None or len(before) == len(items), "the map's items.jsonl does not cover the item file"
    for index, item in enumerate(items):
        prep = prepare(item, index, tokenizer)
        row = {"family": item["family"], "name": uid(item, index), "status": prep["status"]}
        rows.append(row)
        if prep["status"] != "ok":
            continue
        if before is not None:
            eligible = before[index]["status"] in ("eligible", "eligible_not_sampled")
        else:
            keys = list(prep["ids"])  # clean, cf, off: aligned, so one batch
            texts = model.generate_batch(
                torch.tensor([prep["ids"][k] for k in keys], device="cuda"), MAX_NEW_TOKENS, [{}] * 3
            )
            said = {k: answer_colour(text, capitals) for k, text in zip(keys, texts, strict=True)}
            eligible = said == {"clean": roles(item)["A"], "cf": roles(item)["b"], "off": roles(item)["A"]}
        row["status"] = "eligible" if eligible else "not_eligible"
        if eligible:
            pool.append({**item, "name": uid(item, index), "index": index, **prep})
    rng = random.Random(SAMPLE_SEED)
    cases = []
    for family in families:
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
    item_set = manifest["items"].get("set", "bind_recall")
    file, sha, _, families, answers = ITEM_SETS[item_set]
    assert sha256_of(file) == manifest["items"]["sha256"] == sha, "items changed since the manifest"
    model = load_model()
    tokenizer: Any = model.tokenizer
    capitals = list(answers)
    cases, rows = eligible_cases(model, tokenizer, MAP_LAYERS, item_set=item_set)
    print({f: sum(c["family"] == f for c in cases) for f in families}, "items", flush=True)
    outcomes = []
    for c in cases:
        jobs = []
        for group in GROUPS:
            pos = c["groups"][group]
            for layer in MAP_LAYERS:
                for source in ("cf", "off"):
                    delta = c["h"][source][layer][pos] - c["h"]["clean"][layer][pos]
                    jobs.append(({"group": group, "layer": layer, "source": source}, {layer: AddRows(delta, pos)}))
        run_jobs(model, c, jobs, capitals, outcomes)
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


def families_in(rows: list[dict]) -> tuple[str, ...]:
    return tuple(f for f in ("R", "B", "L", "RL") if any(r["family"] == f for r in rows))


def status_counts(rows: list[dict]) -> dict:
    return {
        f: {s: sum(r["family"] == f and r["status"] == s for r in rows) for s in {r["status"] for r in rows}}
        for f in families_in(rows)
    }


def map_rates(outcomes: list[dict]) -> list[dict]:
    rates = []
    for family in families_in(outcomes):
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
    item_set = json.loads((RESULTS / map_run / "manifest.json").read_text())["items"].get("set", "bind_recall")
    families = ITEM_SETS[item_set][3]
    cap = {f: min(blob["answer_formed"].get(f, ANSWER_ONSET), ANSWER_ONSET) for f in families}
    window = {
        f: [layer for layer in blob["windows"].get(f, {}).get("question", []) if layer < cap[f]] for f in families
    }
    manifest = manifest_common(name, why, "bind_recall_parts", item_set)
    manifest["question"] = (
        "At each family's window, which part of the copy carries the bridge: its J-space part or the rest?"
    )
    manifest["map"] = {"run": map_run, "summary_sha256": sha256_of(map_summary), "cap": cap, "parts_window": window}
    manifest["eligibility_from"] = "the map run's items.jsonl (the same items and seeded sample, not regenerated)"
    manifest["lens"] = {"jpp": list(pins.LENS_SOURCES["jpp"])}
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
        "RL": "recall_lookup only: RL 'outside': the in-context use decides (a recalled bridge leaves the J-space when "
        "a lookup in the prompt uses it); RL 'inside': the recalled source decides; otherwise inconclusive",
        "L": "bind_lookup only: L 'outside' (as brew): an in-context second step moves the bound bridge out of the "
        "J-space; L 'inside' (as B): it does not, so brew's difference is its first step (a table lookup) or its "
        "format; otherwise inconclusive",
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
    item_set = manifest["items"].get("set", "bind_recall")
    model = load_model()
    tokenizer: Any = model.tokenizer
    capitals = list(ITEM_SETS[item_set][4])
    map_items = RESULTS / manifest["map"]["run"] / "items.jsonl"
    cases, rows = eligible_cases(model, tokenizer, layers, map_items=map_items, item_set=item_set)
    lens = JLens(model, "jpp")
    dictionaries = {layer: lens.vectors(layer, model.letter_token_ids()) for layer in layers}
    outcomes, fve = [], []
    g = torch.Generator(device="cuda").manual_seed(BOOT_SEED)
    for layer in layers:
        x = torch.randn(CHANCE_DRAWS, dictionaries[layer].shape[1], device="cuda", generator=g)
        share = (signed_omp(dictionaries[layer], x, K_ATOMS).norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2).mean()
        fve.append({"layer": layer, "what": "chance", "share": round(float(share), 4)})
    for c in cases:
        pos = c["groups"]["question"]
        tok = torch.tensor([model.concept_token(c["bridge"]), model.concept_token(c["target"])], device="cuda")
        jobs: list[tuple[dict, dict]] = []

        def run(layer, delta, jobs=jobs, pos=pos, **tags):
            jobs.append(({"layer": layer, **tags}, {layer: AddRows(delta, pos)}))

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
        run_jobs(model, c, jobs, capitals, outcomes)
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
    for family in window:
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
    if "RL" in fam:
        v = fam["RL"]["decisions"]["jspace"]["verdict"] if isinstance(fam["RL"].get("decisions"), dict) else None
        out["hypothesis"] = {
            "outside": "RL outside: the in-context use, not the recalled source, puts the bridge outside the J-space",
            "inside": "RL inside: the recalled source keeps the bridge in the J-space, whatever uses it",
        }.get(v or "", "RL: inconclusive" if v else "RL: not interpreted (empty window)")
    elif "L" in fam:
        v = fam["L"]["decisions"]["jspace"]["verdict"] if isinstance(fam["L"].get("decisions"), dict) else None
        out["hypothesis"] = {
            "outside": "L outside: an in-context second step moves the bound bridge out of the J-space",
            "inside": "L inside: brew's difference is its first step (a table lookup) or its format",
        }.get(v or "", "L: inconclusive" if v else "L: not interpreted (empty window)")
    elif all(isinstance(fam[f].get("decisions"), dict) for f in FAMILIES):
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
    assert SWAP_LAYERS, f"no exp02 swap band for {pins.TARGET} yet"
    maps = sorted(
        d.name
        for d in RESULTS.iterdir()
        if (d / "summary.json").exists() and d.name.startswith(pins.RUN_PREFIX + "map")
    )
    assert maps, "run the map first: the swaps reuse its eligibility and sample"
    manifest["map"] = {"run": maps[-1], "items_sha256": sha256_of(RESULTS / maps[-1] / "items.jsonl")}
    manifest["eligibility_from"] = "the map run's items.jsonl (the same items and seeded sample, not regenerated)"
    manifest["swap"] = {
        "positions": "the cue phrase (R: the city, 'is', 'located'; B: the person, 'lives'), as exp02's cue regime",
        "layers": f"{SWAP_LAYERS[0]}-{SWAP_LAYERS[-1]} at once (exp02's band"
        + ("" if pins.TARGET == "qwen3.6-27b" else f", picked by {pins.RUN_PREFIX}gate_v4")
        + "); a layer is skipped if I's and X's atoms "
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
    map_items = RESULTS / manifest["map"]["run"] / "items.jsonl"
    assert sha256_of(map_items) == manifest["map"]["items_sha256"], "the map's items.jsonl changed"
    cases, rows = eligible_cases(model, tokenizer, SWAP_LAYERS, sources=("clean",), map_items=map_items)
    outcomes = []
    for c in cases:
        pair = {"intermediate": c["bridge"], "swap_to": c["target"]}
        jobs: list[tuple[dict, dict]] = []
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
                tags = {"condition": condition, "null": null, "layers_skipped": len(atoms) - len(clamps)}
                jobs.append((tags, clamps))
        run_jobs(model, c, jobs, capitals, outcomes)
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
    parser.add_argument("--items", default="bind_recall", choices=list(ITEM_SETS), help="manifest_map: the item set")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check()
    elif args.stage in ("manifest_map", "manifest_parts", "manifest_swaps"):
        assert args.name, "manifests need --name"
        assert args.why, "manifests need --why"
        if args.stage == "manifest_map":
            stage_manifest_map(args.name, args.why, args.items)
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
