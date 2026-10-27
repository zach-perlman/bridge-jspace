"""exp21_contrastive (Phase 2a): bridge directions from contrasts on exp09's own question, instead of exp01's probes.

exp01's probe of a country is the mean residual at the last token of ~25 prompts that imply it ("The dance at the heart
of the carnival in Rio is the"), minus the mean over entities: a direction for the country as a topic, built far from
exp09's question, at another position. exp09's probe swap moved R's recalled bridge with it (J-part 82%) but not B's
bound bridge (every condition 0%, the full probe included), so B's swaps were not interpreted. This builds, per country
c, the mean residual at the cue phrase of exp09's own question when its bridge is c, minus the mean over countries:
  R  "<three people and countries> What is the capital of the country where {city} is located?": the cue phrase
     "{city} is located", for 3 fit cities per country that exp09's items never use (FIT_CITIES)
  B  "<three people and countries> What is the capital of the country where {person} lives?": the cue phrase
     "{person} lives", the queried person living in c, people's names that exp09's items never use (FIT_NAMES)
in the chat format (bridge_jspace.chat, as the chat runs), a prompt kept only if the model answers c's capital. The
directions are decomposed as exp01's probes (25-atom non-negative OMP over J++'s letter-token vectors) and saved in
exp01's format, so exp09's swaps take them as --probes exp21/<tag>.

Stages (write-once):
  manifest --tag T --family R|B --why "..."    run --tag T
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import check_switches, switches
from bridge_jspace.tokens import raw_encoding
from scripts.exp01_probes import K_ATOMS, PROBE_LAYERS, decompose
from scripts.exp03_brew_swaps import answer_colour
from scripts.exp09_make_items import CAPITALS, CITIES, NAMES

EXP = "exp21_contrastive"
RESULTS = pins.RESULTS_DIR / EXP
CACHE = pins.CACHE_DIR / EXP
FIT_CITIES = {  # 3 per country, none of them in exp09_make_items.CITIES and none a capital
    "France": ["Lille", "Strasbourg", "Nantes"],
    "Spain": ["Zaragoza", "Granada", "Alicante"],
    "Italy": ["Genoa", "Bologna", "Palermo"],
    "Germany": ["Dresden", "Leipzig", "Bremen"],
    "Japan": ["Kobe", "Hiroshima", "Fukuoka"],
    "Russia": ["Volgograd", "Yekaterinburg", "Murmansk"],
    "Egypt": ["Suez", "Hurghada", "Mansoura"],
    "Peru": ["Piura", "Chiclayo", "Huancayo"],
    "China": ["Nanjing", "Tianjin", "Hangzhou"],
    "Canada": ["Winnipeg", "Halifax", "Saskatoon"],
    "Greece": ["Larissa", "Volos", "Ioannina"],
    "Australia": ["Darwin", "Hobart", "Cairns"],
    "Poland": ["Lodz", "Lublin", "Katowice"],
}
FIT_NAMES = ["Olivia", "Liam", "Noah", "Mia", "Lucas", "Zoe", "Ethan", "Ruby", "Leo", "Chloe", "Owen", "Ella",
             "Ivan", "Hugo", "Maya", "Felix", "Iris", "Adam", "Lily", "Max"]  # fmt: skip
PER_CITY, PER_COUNTRY_B = 8, 24  # prompts per fit city (R) and per country (B)
SEED = 21
GREEDY_TOKENS = 8
BATCH = 64
INSPECT_LAYERS = (24, 32, 40)


def fit_prompts(family: str) -> list[dict]:
    """The fit prompts: per country, R's question for each fit city or B's for a queried person living there, after
    three people and countries (the bridge, two other countries), in a seeded order."""
    assert not set(FIT_NAMES) & set(NAMES), "fit names must not be exp09's"
    assert not {c for cs in FIT_CITIES.values() for c in cs} & {c for cs in CITIES.values() for c in cs}
    rng = random.Random(SEED + (0 if family == "R" else 1))
    rows = []
    for country in CAPITALS:
        cues = [c for c in FIT_CITIES[country] for _ in range(PER_CITY)] if family == "R" else [None] * PER_COUNTRY_B
        for cue in cues:
            others = rng.sample([c for c in CAPITALS if c != country], 2)
            held = [country, *others]
            rng.shuffle(held)
            people = rng.sample(FIT_NAMES, 3)
            context = " ".join(f"{p} lives in {c}." for p, c in zip(people, held, strict=True))
            if family == "R":
                question = f"The capital of the country where {cue} is located is"
            else:
                cue = people[held.index(country)]
                question = f"The capital of the country where {cue} lives is"
            rows.append({"country": country, "cue": cue, "prompt": f"{context} {question}"})
    return rows


def stage_manifest(tag: str, family: str, why: str) -> None:
    pins.check_run_name(tag)
    path = RESULTS / tag / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    rows = fit_prompts(family)
    manifest = {
        "exp": EXP,
        "run": tag,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "family": family,
        "question": "A bridge direction per country from exp09's own question (cue phrase, chat format): does it "
        "move the bridge where exp01's probes did not (B), and does its J-space part carry it?",
        "model": pins.model_pin(),
        "switches": switches(),
        "lens": {"jpp": list(pins.LENS_SOURCES["jpp"])},
        "format": "chat_prefill (bridge_jspace.chat: the statement as a question, thinking off, 'Answer:' prefilled)",
        "prompts": {
            "n": len(rows),
            "per_country": len(rows) // len(CAPITALS),
            "cue": "R: a fit city (FIT_CITIES, none in exp09's items); B: the queried person (FIT_NAMES, none in "
            "exp09's items)",
            "seed": SEED + (0 if family == "R" else 1),
            "sha256_of_prompts": sha256_of_text(json.dumps(rows)),
        },
        "filter": f"keep a prompt if the first capital in the greedy continuation ({GREEDY_TOKENS} tokens) is the "
        "country's",
        "direction": "per country and layer, the mean over its kept prompts of the residual (block output) averaged "
        "over the cue phrase's tokens (R: the city, 'is located'; B: the person, 'lives'), minus the mean of those "
        "means over countries; layers as exp01's probes",
        "decomposition": f"exp01's: non-negative OMP, {K_ATOMS} atoms, over J++'s unit letter-token vectors",
        "checks": [
            "held-out decoding: per layer, the country of each kept prompt from the nearest country mean (cosine), the "
            "means fit without that prompt's cue (R: leave one city out; B: leave one prompt out); chance 1/13",
            "the cosine of each direction to exp01's probe of the same country (v4_chat_jpp if present)",
            "the share of the direction's variance in its J-part, against random directions (exp01's FVE)",
        ],
        "use": "exp09 swaps with --probes exp21/<tag> on the chat map, exp02's chat band; read like exp09's swaps "
        "(positive control: the full direction flips more than its null; J-space: the J-part more than the "
        "matched-alignment control)",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path, len(rows), "prompts")


def sha256_of_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode()).hexdigest()


@torch.no_grad()
def stage_run(tag: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir, cache_dir = RESULTS / tag, CACHE / tag
    manifest = json.loads((out_dir / "manifest.json").read_text())
    check_switches(manifest)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    family = manifest["family"]
    rows = fit_prompts(family)
    assert sha256_of_text(json.dumps(rows)) == manifest["prompts"]["sha256_of_prompts"], "prompts changed"
    model = load_model()
    tok = model.tokenizer
    capitals = [c.lower() for c in CAPITALS.values()]
    clause = " is located" if family == "R" else " lives"
    for r in rows:
        text = chat.chat_text(tok, chat.question_content(r["prompt"]))
        enc = raw_encoding(tok, text, offsets=True)
        _, cue_start, cue_end = chat.question_span(text, r["cue"], clause)
        r["ids"] = enc["input_ids"]
        r["cue_positions"] = [i for i, (s, e) in enumerate(enc["offset_mapping"]) if s < cue_end and e > cue_start]
    by_len: dict[int, list[dict]] = {}
    for r in rows:
        by_len.setdefault(len(r["ids"]), []).append(r)
    for group in by_len.values():
        for start in range(0, len(group), BATCH):
            chunk = group[start : start + BATCH]
            texts = model.generate_batch(
                torch.tensor([r["ids"] for r in chunk], device="cuda"), GREEDY_TOKENS, [{}] * len(chunk)
            )
            for r, t in zip(chunk, texts, strict=True):
                r["greedy"] = t
                r["kept"] = answer_colour(t, capitals) == CAPITALS[r["country"]].lower()
    countries = list(CAPITALS)
    reps: dict[str, list[torch.Tensor]] = {c: [] for c in countries}
    cues: dict[str, list[str]] = {c: [] for c in countries}
    for r in rows:
        if r["kept"]:
            _, h = model.run(torch.tensor([r["ids"]], device="cuda"), record=PROBE_LAYERS)
            reps[r["country"]].append(torch.stack([h[layer][r["cue_positions"]].mean(0) for layer in PROBE_LAYERS]))
            cues[r["country"]].append(r["cue"])
    n_kept = {c: len(reps[c]) for c in countries}
    print("kept", n_kept, flush=True)
    assert all(n >= 3 for n in n_kept.values()), "a country has fewer than 3 kept prompts"
    means = torch.stack([torch.stack(reps[c]).mean(0) for c in countries])  # [E, L, d]
    probes = means - means.mean(0, keepdim=True)

    # Held-out decoding: the nearest country mean (cosine), fit without the prompt's cue (R) or the prompt itself (B).
    decoding = {}
    for layer in INSPECT_LAYERS:
        li = PROBE_LAYERS.index(layer)
        hits = n = 0
        for ci, c in enumerate(countries):
            for k, (vec, cue) in enumerate(zip(reps[c], cues[c], strict=True)):
                held = [
                    torch.stack(
                        [v[li] for j, (v, q) in enumerate(zip(reps[d], cues[d], strict=True)) if not (d == c and (q == cue if family == "R" else j == k))]
                    ).mean(0)
                    for d in countries
                ]  # fmt: skip
                m = torch.stack(held)
                m = m - m.mean(0, keepdim=True)
                x = vec[li] - torch.stack(held).mean(0)
                hits += int(torch.nn.functional.cosine_similarity(m, x[None], dim=-1).argmax()) == ci
                n += 1
        decoding[layer] = {"accuracy": hits / n, "n": n, "chance": 1 / len(countries)}
    print("decoding", decoding, flush=True)

    lens = JLens(model, "jpp")
    jparts, atom_ids, atom_coefs, random_fve = decompose(model, lens, probes)
    fve = (jparts.norm(dim=-1) ** 2 / probes.norm(dim=-1) ** 2).mean(0)  # [L]
    exp01_cos = None
    exp01 = pins.CACHE_DIR / "exp01" / "v4_chat_jpp" / "probes.pt"
    if exp01.exists():
        blob = torch.load(exp01, map_location="cuda", weights_only=True)
        idx = [blob["entities"].index(c) for c in countries]
        other = blob["probe"].to("cuda")[idx][:, [blob["layers"].index(layer) for layer in PROBE_LAYERS]]
        cos = torch.nn.functional.cosine_similarity(probes, other.float(), dim=-1)  # [E, L]
        exp01_cos = {layer: round(float(cos[:, PROBE_LAYERS.index(layer)].mean()), 3) for layer in INSPECT_LAYERS}
    cache_dir.mkdir(parents=True, exist_ok=False)
    torch.save(
        {
            "entities": countries,
            "layers": list(PROBE_LAYERS),
            "probe": probes.cpu(),
            "jpart": jparts.cpu(),
            "atom_ids": atom_ids,
            "atom_coefs": atom_coefs,
            "n_kept": n_kept,
            "tag": tag,
            "definition": f"contrastive_{family}",
            "lens": "jpp",
        },
        cache_dir / "probes.pt",
    )
    with open(out_dir / "filter.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ("country", "cue", "prompt", "greedy", "kept")}) + "\n")
    summary = {
        "family": family,
        "n_prompts": len(rows),
        "n_kept": n_kept,
        "held_out_decoding": decoding,
        "jpart_variance_share": {layer: round(float(fve[PROBE_LAYERS.index(layer)]), 3) for layer in INSPECT_LAYERS},
        "random_variance_share": {
            layer: round(sum(random_fve[layer]) / len(random_fve[layer]), 3) for layer in INSPECT_LAYERS
        },
        "cosine_to_exp01_v4_chat_jpp": exp01_cos,
        "probes_file": str((cache_dir / "probes.pt").relative_to(pins.REPO_ROOT)),
        "probes_sha256": sha256_of(cache_dir / "probes.pt"),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run", "show"])
    parser.add_argument("--tag", required=True)
    parser.add_argument("--family", choices=["R", "B"])
    parser.add_argument("--why")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.family, "manifest needs --family"
        assert args.why, "manifest needs --why"
        stage_manifest(args.tag, args.family, args.why)
    elif args.stage == "show":
        for r in fit_prompts(args.family or "R")[:3]:
            print(r)
    else:
        stage_run(args.tag)
