"""exp23_arith (block 8): is an intermediate the model computes by arithmetic, in the prompt, carried in the J-space?

brew's intermediate (a lookup in a colour table) is carried outside the J-space (B2, B3); exp09 found the same for
bridges a lookup in the prompt uses. This asks it of a number the model computes:
  "Ignore {z}. Start with {S}. Add {a}. Then {add|subtract} {b}. What is the result?"   I = S + a, A = I +/- b
every number a single digit 0-9 (one token in Qwen's tokenizer), in the chat format (bridge_jspace.chat). As exp04/exp09:
  C   "Add {a'}": the intermediate becomes X = S + a' (X != I); its answer b = X +/- b (!= A)
  O   "Ignore {z'}": an off-path number changes; the answer stays A
  competence  clean, C and O answered, and each step alone ("Start with S. Add a. What is the result?" -> I; "Start
              with I. Then ... b. What is the result?" -> A), every item, before any edit (README Decisions)
  map         C's (or O's) block output copied into the original at one layer (0-60, every 4th), at the tokens after
              C's change ('after') or the last token ('last'); the answer read as the first number of the continuation
  parts       at the window the map finds (rule below), the copy split into its J-space part (25-atom signed OMP over
              J++'s unit vectors of letter tokens and the 10 digit tokens) and the rest, and into its projection on
              J++'s v_I, v_X (the two digits) and the rest; each against a matched-norm random direction
Rules (fixed here, as exp09's): window = the 'after' layers where C's copy gives b more often than O's copy changes the
answer (Wilson intervals apart), below the first layer where the last token's copy alone gives b for half the items;
per part, exp04's verdict (outside: rest - part above 0 and part - its null not; inside: the reverse; else both or
neither). Prediction: outside, as brew.

Stages (write-once):  make (data/arith.json)   manifest --name N --why "..."   run N
"""

from __future__ import annotations

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

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from bridge_jspace.tokens import raw_encoding
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, AddRows, lens2_part, null_rows, signed_omp

EXP = "exp23_arith"
RESULTS = pins.RESULTS_DIR / EXP
DATA = pins.DATA_DIR / "arith.json"
N_MAKE, MAKE_SEED = 400, 23
N_ITEMS, SAMPLE_SEED = 80, 0
MAP_LAYERS = tuple(range(0, pins.N_LAYERS - 3, 4))
GROUPS = ("after", "last")
MAX_NEW_TOKENS = 8
BATCH = 32
NULL_SEED, N_BOOT, BOOT_SEED = 0, 2000, 0
PARTS = ("lens2", "not_lens2", "jspace", "not_jspace")
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def make_item(rng: random.Random, index: int) -> dict:
    while True:
        s, a = rng.randint(0, 9), rng.randint(1, 9)
        i = s + a
        op = rng.choice(["add", "subtract"])
        b = rng.randint(1, 9)
        ans = i + b if op == "add" else i - b
        if i > 9 or not 0 <= ans <= 9:
            continue
        cands = [a2 for a2 in range(1, 10) if a2 != a and s + a2 <= 9]
        rng.shuffle(cands)
        for a2 in cands:
            x = s + a2
            ans2 = x + b if op == "add" else x - b
            if 0 <= ans2 <= 9 and ans2 not in (ans, i, x, s):  # b's role is then unambiguous
                break
        else:
            continue
        z, z2 = rng.sample([d for d in range(10) if d not in {s, a, b, a2}], 2)
        text = "Ignore {z}. Start with {s}. Add {a}. Then {op} {b}. The result is"
        fill = {"s": s, "a": a, "op": op, "b": b}
        return {
            "name": f"AR-{index:04d}",
            "family": "AR",
            "prompt": text.format(z=z, **fill),
            "cf_prompt": text.format(z=z, **{**fill, "a": a2}),
            "off_prompt": text.format(z=z2, **fill),
            "S": s, "a": a, "op": op, "b": b, "I": i, "A": ans, "a_cf": a2, "X": x, "A_cf": ans2, "z": z, "z_off": z2,
            "hop1": f"Start with {s}. Add {a}. The result is",
            "hop2": f"Start with {i}. Then {op} {b}. The result is",
        }  # fmt: skip


def stage_make() -> None:
    assert not DATA.exists(), f"{DATA} exists; data files are written once"
    rng = random.Random(MAKE_SEED)
    items = [make_item(rng, k) for k in range(N_MAKE)]
    blob = {
        "family": "arith",
        "generator": f"scripts/exp23_arith.py make (n={N_MAKE}, seed {MAKE_SEED})",
        "format": "AR: a distractor number, a start number, an addition and an addition or subtraction, every number a "
        "single digit; C changes the first addend (the intermediate becomes X), O the distractor; ungated",
        "items": items,
    }
    DATA.write_text(json.dumps(blob, indent=1) + "\n")
    print("wrote", DATA, len(items), "items")


def render(tokenizer, text: str) -> str:
    return chat.chat_text(tokenizer, chat.question_content(text))


def number_said(text: str) -> int | None:
    """The first number in the continuation's first non-empty line, as a digit or a number word."""
    line = next((ln for ln in text.lower().split("\n") if ln.strip()), "")
    for tok in re.findall(r"[a-z]+|\d+", line):
        if tok.isdigit():
            return int(tok)
        if tok in WORDS:
            return WORDS.index(tok)
    return None


def role_of(said: int | None, item: dict) -> str:
    if said is None:
        return "none"
    return next((r for r, v in (("b", item["A_cf"]), ("A", item["A"]), ("I", item["I"]), ("X", item["X"])) if v == said), "other")  # fmt: skip


def stage_manifest(name: str, why: str) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "run": name,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "question": "Is a number the model computes in the prompt (S + a) carried in the J-space where it is used?",
        "model": pins.model_pin(),
        "items": {"file": str(DATA.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(DATA)},
        "format": "chat_prefill (bridge_jspace.chat: 'What is the result? Answer with a single word and nothing else.', "
        "thinking off, 'Answer:' prefilled)",
        "competence": "every item, unedited, greedy: clean, C, O, and each step alone (hop1 -> I, hop2 -> A); a number "
        "is read as the first digit or number word of the first line",
        "eligibility": f"clean answers A, C answers b, O answers A; a seeded sample (seed {SAMPLE_SEED}) of {N_ITEMS}",
        "map": {
            "layers": list(MAP_LAYERS),
            "groups": {"after": "the tokens after C's changed one, to the end", "last": "the last token"},
            "sources": ["cf", "off"],
        },
        "parts": {
            "full": "δ = h_C - h_B at the 'after' group",
            "lens2": "δ's projection on span{v_I, v_X}, J++'s unit vectors of the two digit tokens; not_lens2 the rest",
            "jspace": f"δ's {K_ATOMS}-atom signed OMP part over J++'s unit vectors of letter tokens and the 10 digit "
            "tokens; not_jspace the rest",
            "nulls": "each part along seeded random directions at the same per-position norm",
        },
        "lens": {"jpp": list(pins.LENS_SOURCES["jpp"])},
        "decision": {
            "window": "the 'after' layers where C's copy gives b more often than O's copy changes the answer (Wilson "
            "95% intervals apart), below answer_formed (the first layer where the last token's copy gives b for half "
            "the items or more)",
            "parts": "per split, exp04's verdict: outside if rest - part is above 0 and part - its null is not; inside if "
            "part - rest is above 0 and rest - its null is not; otherwise both or neither (paired bootstraps over items)",
            "prediction": "outside, as brew's intermediate (B2)",
        },
        "generation": f"greedy, {MAX_NEW_TOKENS} new tokens, an item's runs batched {BATCH} at a time",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    assert sha256_of(DATA) == manifest["items"]["sha256"], "items changed since the manifest"
    items = json.loads(DATA.read_text())["items"]
    model = load_model()
    tok: Any = model.tokenizer
    t0 = time.time()

    def answers(texts: list[str]) -> list[int | None]:
        enc = [raw_encoding(tok, render(tok, t))["input_ids"] for t in texts]
        out: list[int | None] = [None] * len(texts)
        by_len: dict[int, list[int]] = {}
        for i, ids in enumerate(enc):
            by_len.setdefault(len(ids), []).append(i)
        for idx in by_len.values():
            for s in range(0, len(idx), 64):
                chunk = idx[s : s + 64]
                outs = model.generate_batch(
                    torch.tensor([enc[i] for i in chunk], device="cuda"), MAX_NEW_TOKENS, [{}] * len(chunk)
                )
                for i, t in zip(chunk, outs, strict=True):
                    out[i] = number_said(t)
        return out

    # Competence, every item.
    kinds = {"clean": ("prompt", "A"), "cf": ("cf_prompt", "A_cf"), "off": ("off_prompt", "A"), "hop1": ("hop1", "I"), "hop2": ("hop2", "A")}  # fmt: skip
    said = {k: answers([it[f] for it in items]) for k, (f, _) in kinds.items()}
    correct = {k: [s == it[e] for s, it in zip(said[k], items, strict=True)] for k, (_, e) in kinds.items()}
    competence = {k: dict(zip(("rate", "lo", "hi"), wilson(sum(v), len(v)), strict=True)) | {"n": len(v), "correct": sum(v)} for k, v in correct.items()}  # fmt: skip
    eligible = [i for i in range(len(items)) if correct["clean"][i] and correct["cf"][i] and correct["off"][i]]
    both = [i for i in range(len(items)) if correct["hop1"][i] and correct["hop2"][i]]
    competence["all_three"] = {"n": len(items), "correct": len(eligible), "rate": len(eligible) / len(items)}
    competence["clean_given_both_hops"] = {"n": len(both), "correct": sum(correct["clean"][i] for i in both)}
    print("competence", json.dumps(competence), f"{time.time() - t0:.0f}s", flush=True)

    # Cases: aligned C and O (one changed token each), a seeded sample of the eligible.
    cases = []
    for i in eligible:
        it = items[i]
        ids = {k: raw_encoding(tok, render(tok, it[f]))["input_ids"] for k, f in (("clean", "prompt"), ("cf", "cf_prompt"), ("off", "off_prompt"))}  # fmt: skip
        if len({len(v) for v in ids.values()}) != 1:
            continue
        changed = {
            k: [p for p, (u, v) in enumerate(zip(ids["clean"], ids[k], strict=True)) if u != v] for k in ("cf", "off")
        }
        if any(len(v) != 1 for v in changed.values()):
            continue
        after = list(range(changed["cf"][0] + 1, len(ids["clean"])))
        cases.append({**it, "index": i, "ids": ids, "groups": {"after": after, "last": [len(ids["clean"]) - 1]}})
    rng = random.Random(SAMPLE_SEED)
    cases = rng.sample(cases, min(N_ITEMS, len(cases)))
    print(len(eligible), "eligible,", len(cases), "sampled", flush=True)
    for c in cases:
        c["h"] = {}
        for src in ("clean", "cf", "off"):
            _, rec = model.run(torch.tensor([c["ids"][src]], device="cuda"), record=MAP_LAYERS)
            c["h"][src] = rec

    def run_jobs(c: dict, jobs: list[tuple[dict, dict]], outcomes: list[dict]) -> None:
        ids = torch.tensor([c["ids"]["clean"]], device="cuda")
        for s in range(0, len(jobs), BATCH):
            chunk = jobs[s : s + BATCH]
            texts = model.generate_batch(ids, MAX_NEW_TOKENS, [e for _, e in chunk])
            for (tags, _), text in zip(chunk, texts, strict=True):
                n = number_said(text)
                outcomes.append({"name": c["name"], **tags, "said": n, "role": role_of(n, c)})

    # Map.
    map_out: list[dict] = []
    for c in cases:
        jobs = []
        for group in GROUPS:
            pos = c["groups"][group]
            for layer in MAP_LAYERS:
                for src in ("cf", "off"):
                    delta = c["h"][src][layer][pos] - c["h"]["clean"][layer][pos]
                    jobs.append(({"group": group, "layer": layer, "source": src}, {layer: AddRows(delta, pos)}))
        run_jobs(c, jobs, map_out)
    rates = []
    for group in GROUPS:
        for layer in MAP_LAYERS:
            cf = [o for o in map_out if (o["group"], o["layer"], o["source"]) == (group, layer, "cf")]
            off = [o for o in map_out if (o["group"], o["layer"], o["source"]) == (group, layer, "off")]
            rates.append({"group": group, "layer": layer, "n": len(cf), "b": wilson(sum(o["role"] == "b" for o in cf), len(cf)),
                          "I": wilson(sum(o["role"] == "I" for o in cf), len(cf)),
                          "off_changed": wilson(sum(o["role"] != "A" for o in off), len(off))})  # fmt: skip
    formed = next((r["layer"] for r in rates if r["group"] == "last" and r["b"][0] >= 0.5), pins.N_LAYERS)
    window = [
        r["layer"] for r in rates if r["group"] == "after" and r["b"][1] > r["off_changed"][2] and r["layer"] < formed
    ]
    print("window", window, "answer formed", formed, f"{time.time() - t0:.0f}s", flush=True)

    # Parts at the window.
    parts_out: list[dict] = []
    if window:
        lens = JLens(model, "jpp")
        digits = [tok.convert_tokens_to_ids(str(d)) for d in range(10)]
        dict_ids = torch.cat([model.letter_token_ids(), torch.tensor(digits, device="cuda")])
        dictionaries = {layer: lens.vectors(layer, dict_ids) for layer in window}
        for c in cases:
            pos = c["groups"]["after"]
            two = torch.tensor([digits[c["I"]], digits[c["X"]]], device="cuda")
            jobs = []
            for layer in window:
                delta = c["h"]["cf"][layer][pos] - c["h"]["clean"][layer][pos]
                jobs.append(({"layer": layer, "part": "full", "null": False}, {layer: AddRows(delta, pos)}))
                lens2 = lens2_part(delta, lens.vectors(layer, two))
                jspace = signed_omp(dictionaries[layer], delta, K_ATOMS)
                parts = {"lens2": lens2, "not_lens2": delta - lens2, "jspace": jspace, "not_jspace": delta - jspace}
                for pi, (pname, part) in enumerate(parts.items()):
                    jobs.append(({"layer": layer, "part": pname, "null": False}, {layer: AddRows(part, pos)}))
                    g = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1000 * c["index"] + 10 * layer + pi)
                    jobs.append(
                        ({"layer": layer, "part": pname, "null": True}, {layer: AddRows(null_rows(part, g), pos)})
                    )
            run_jobs(c, jobs, parts_out)

    def scores(**where) -> dict[str, float]:
        hits: dict[str, list[bool]] = {}
        for o in parts_out:
            if all(o.get(k) == v for k, v in where.items()):
                hits.setdefault(o["name"], []).append(o["role"] == "b")
        return {n: sum(v) / len(v) for n, v in hits.items()}

    verdicts = {}
    step = {}
    if parts_out:
        s = {(p, n): scores(part=p, null=n) for p in (*PARTS, "full") for n in (False, True)}
        step = {f"{p}{' null' if n else ''}": statistics.mean(v.values()) for (p, n), v in s.items() if v}

        def diff(a, b):
            names = sorted(set(s[a]) & set(s[b]))
            return paired_bootstrap_diff([s[a][n] for n in names], [s[b][n] for n in names], N_BOOT, BOOT_SEED)

        for inside, outside in (("lens2", "not_lens2"), ("jspace", "not_jspace")):
            d = {f"{outside} - {inside}": diff((outside, False), (inside, False)),
                 f"{inside} - its null": diff((inside, False), (inside, True)),
                 f"{outside} - its null": diff((outside, False), (outside, True))}  # fmt: skip
            v = "both or neither"
            if d[f"{outside} - {inside}"][1] > 0 and d[f"{inside} - its null"][1] <= 0:
                v = "outside"
            elif d[f"{outside} - {inside}"][2] < 0 and d[f"{outside} - its null"][1] <= 0:
                v = "inside"
            verdicts[inside] = {**d, "verdict": v}
    write_jsonl(out_dir / "map_outcomes.jsonl", map_out)
    write_jsonl(out_dir / "parts_outcomes.jsonl", parts_out)
    write_jsonl(out_dir / "competence.jsonl", [{"name": it["name"], **{k: said[k][i] for k in kinds}, **{f"{k}_ok": correct[k][i] for k in kinds}} for i, it in enumerate(items)])  # fmt: skip
    summary = {"competence": competence, "n_cases": len(cases), "map": rates, "answer_formed": formed, "window": window,
               "step_scores": step, "verdicts": verdicts, "seconds": round(time.time() - t0)}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {name}", "", "Competence (every item, chat + Answer:):"]
    lines += [f"- {k}: {v['correct']}/{v['n']}" + (f" {100 * v['rate']:.0f}% [{100 * v['lo']:.0f}, {100 * v['hi']:.0f}]" if "lo" in v else "") for k, v in competence.items()]  # fmt: skip
    lines += ["", f"Cases: {len(cases)}; window {window}; answer formed at the last token from layer {formed}", ""]
    lines += ["| group | layer | C gives b | C gives I | O changes the answer |", "|---|---|---|---|---|"]
    lines += [f"| {r['group']} | {r['layer']} | {100 * r['b'][0]:.0f}% | {100 * r['I'][0]:.0f}% | {100 * r['off_changed'][0]:.0f}% |" for r in rates]  # fmt: skip
    if step:
        lines += ["", "Step scores: " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in step.items())]
        for k, d in verdicts.items():
            lines.append(
                f"- {k}: "
                + "; ".join(f"{m} {pts(v)}" for m, v in d.items() if m != "verdict")
                + f"; verdict: {d['verdict']}"
            )
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["make", "manifest", "run"])
    parser.add_argument("target", nargs="?")
    parser.add_argument("--name")
    parser.add_argument("--why")
    args = parser.parse_args()
    if args.stage == "make":
        stage_make()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.target, "run needs the run's name"
        stage_run(args.target)
