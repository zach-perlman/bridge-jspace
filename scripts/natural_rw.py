"""natural_rw: read without write on natural facts (Zach, 2026-10-20, cheap experiment N before the sprint plan).

TwoHopFact's "country of person's birth city" rows the 27B knows (both facts right alone in twohop_pilot screen_v1),
in two versions that differ only in where the second fact comes from:
  MM  both facts recalled:  "The city where Bill Gates was born is in the country of ___"     (like the suite's RR)
  MC  the second fact in the prompt: three "<city> is in the country of <country>." facts (the bridge's, the
      counterfactual city X's, and a third known row's, shuffled), then the same statement     (like RL)
X is the birth city of another known row whose country differs (and whose first answer token differs). At layers
32/36/40, on the statement's tokens after the person's name:
  read   the J-lens's best rank of the bridge city (any single-token surface) among word tokens
  write  add the lens direction v_X - v_I (unit lens vectors of the two cities) at alpha x the residual's norm per
         position (alpha 0.05-0.8), and a random direction at the same norms; measured on the answer's first token:
         flips (top token = X's country) and the share of the clean margin closed, (ld - ld_clean) / -ld_clean with
         ld = logit(X's country) - logit(the bridge's country)
  MX  conflict (v2): the three facts give each city another known row's country (never its own), so the answer is
      the prompt's country for the bridge city and a lookup in the prompt is the only way to it; steering toward X
      counts a flip to X's prompt country (the lookup written) and, separately, to X's real country (memory written)
Cases: rows answered correctly unedited in every version run, cities with a single-token lens vector. Descriptive; no
verdict rule. (v1's MC turned out not to force a lookup: the model knows every fact, so it can answer from memory.)

python scripts/natural_rw.py --name N --why W [--n K]
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

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.tokens import raw_encoding
from scripts import suite_v1 as S
from scripts import twohop_pilot as T
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import AddRows, null_rows

RESULTS = pins.RESULTS_DIR / "natural_rw"
TYPE = "cntry of person's birthcity"
LAYERS = (32, 36, 40)
ALPHAS = (0.05, 0.1, 0.2, 0.4, 0.8)
SEED = 501
BATCH = 32


def build(tok, model, versions: tuple[str, ...] = ("MM", "MC")) -> list[dict]:
    items = [it for it in json.loads((T.DATA / "screen.json").read_text())["items"] if it["type"] == TYPE]
    ok: dict[str, dict[str, bool]] = collections.defaultdict(dict)
    for line in (T.RESULTS / "screen_v1" / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        ok[r["id"]][r["version"]] = r["correct"]
    known = [it for it in items if ok[it["id"]].get("hop1") and ok[it["id"]].get("hop2")]

    def single(city: str) -> int | None:
        try:
            return model.concept_token(city)
        except ValueError:
            return None

    known = [it for it in known if single(it["e2"]) is not None]
    rng = random.Random(SEED)
    cases = []
    for it in known:
        a_tok = S.answer_token(tok, it["e3"], "word")
        pool = [o for o in known if o["e2"] != it["e2"] and o["e3"] != it["e3"]
                and S.answer_token(tok, o["e3"], "word") != a_tok]  # fmt: skip
        if len(pool) < 2:
            continue
        x, k = rng.sample(pool, 2)
        facts = [f"{c['e2']} is in the country of {c['e3']}." for c in (it, x, k)]
        rng.shuffle(facts)
        statement = it["prompts"]["MM"]
        # conflict: three other rows' countries, all distinct from each other and from the three cities' real ones
        real = {it["e3"], x["e3"], k["e3"]}
        donors = [o for o in known if o["e3"] not in real]
        rng.shuffle(donors)
        chosen: list[dict] = []
        for o in donors:
            used = {S.answer_token(tok, d["e3"], "word") for d in chosen}
            used |= {S.answer_token(tok, c["e3"], "word") for c in (it, x)}
            if o["e3"] not in {d["e3"] for d in chosen} and S.answer_token(tok, o["e3"], "word") not in used:
                chosen.append(o)
            if len(chosen) == 3:
                break
        if len(chosen) < 3:
            continue
        fake = dict(zip((it["e2"], x["e2"], k["e2"]), chosen, strict=True))
        conflict = [f"{c} is in the country of {d['e3']}." for c, d in fake.items()]
        rng.shuffle(conflict)
        texts = {"MM": statement, "MC": " ".join(facts) + " " + statement, "MX": " ".join(conflict) + " " + statement}
        for version in versions:
            text = texts[version]
            rendered = chat.chat_text(tok, chat.blank_content(text))
            enc = raw_encoding(tok, rendered, offsets=True)
            start = rendered.rindex(it["e1"]) + len(it["e1"])
            pos = [i for i, (s, _) in enumerate(enc["offset_mapping"]) if s >= start]
            mx = version == "MX"
            ans, x_ans = (fake[it["e2"]], fake[x["e2"]]) if mx else (it, x)
            cases.append({"id": it["id"], "version": version, "e1": it["e1"], "bridge": it["e2"], "x": x["e2"],
                          "answer": ans["e3"], "x_answer": x_ans["e3"], "aliases": ans["aliases"], "ids": list(enc["input_ids"]),
                          "pos": pos, "tok_A": S.answer_token(tok, ans["e3"], "word"),
                          "tok_b": S.answer_token(tok, x_ans["e3"], "word"),
                          "tok_mem": S.answer_token(tok, x["e3"], "word"), "real_answer": it["e3"],
                          "i_tok": single(it["e2"]), "x_tok": single(x["e2"])})  # fmt: skip
    return cases


@torch.no_grad()
def main(name: str, why: str, n: int, versions: tuple[str, ...] = ("MM", "MC")) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    inputs = [T.DATA / "screen.json", T.RESULTS / "screen_v1" / "items.jsonl"]
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(LAYERS),
                "alphas": list(ALPHAS), "seed": SEED, "n": n, "doc": (__doc__ or "").split("\n\n")[1],
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in inputs}}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    cases = build(tok, model, versions)
    # eligibility: both versions answered correctly, unedited
    for c in cases:
        text = model.generate_batch(torch.tensor([c["ids"]], device="cuda"), 12, [{}])[0]
        c["clean_text"], c["clean_ok"] = text, T.judge(text, c["aliases"])
    good = {c["id"] for c in cases if c["clean_ok"]}
    both = [i for i in dict.fromkeys(c["id"] for c in cases)
            if sum(c["id"] == i and c["clean_ok"] for c in cases) == len(versions)]  # fmt: skip
    keep = set(both[:n])
    cases = [c for c in cases if c["id"] in keep]
    print(len(good), "answered,", len(keep), "items with both versions right", flush=True)
    reads, outcomes = [], []
    for k, c in enumerate(cases):
        ids = torch.tensor([c["ids"]], device="cuda")
        _, logits0 = model.generate_batch(ids, 1, [{}], first_logits=True)
        ld0 = float(logits0[0, c["tok_b"]] - logits0[0, c["tok_A"]])
        _, rec = model.run(ids, record=LAYERS)
        jobs = []
        for la in LAYERS:
            h = rec[la][c["pos"]]
            rank = min(model.word_rank(row, model.surface_ids(c["bridge"])) for row in lens.readout(h, la))
            reads.append({"id": c["id"], "version": c["version"], "layer": la, "rank": rank})
            v = lens.vectors(la, torch.tensor([c["i_tok"], c["x_tok"]], device="cuda"))
            direction = torch.nn.functional.normalize(v[1] - v[0], dim=-1).expand_as(h)
            norms = h.norm(dim=-1, keepdim=True)
            gen = torch.Generator(device="cuda").manual_seed(SEED + 1000 * k + la)
            for a in ALPHAS:
                vec = a * norms * direction
                jobs.append(({"layer": la, "alpha": a, "kind": "lens"}, {la: AddRows(vec, c["pos"])}))
                jobs.append(({"layer": la, "alpha": a, "kind": "random"}, {la: AddRows(null_rows(vec, gen), c["pos"])}))
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            _, logits = model.generate_batch(ids, 1, [e for _, e in chunk], first_logits=True)
            for row, (tags, _) in enumerate(chunk):
                ld = float(logits[row, c["tok_b"]] - logits[row, c["tok_A"]])
                top = int(logits[row].argmax())
                outcomes.append({"id": c["id"], "version": c["version"], **tags, "flip": top == c["tok_b"],
                                 "flip_mem": top == c["tok_mem"] and c["tok_mem"] != c["tok_b"],
                                 "closed": (ld - ld0) / max(-ld0, 1e-6)})  # fmt: skip
        if (k + 1) % 50 == 0:
            print(f"{k + 1}/{len(cases)} cases, {time.time() - t0:.0f}s", flush=True)
    write_jsonl(
        out_dir / "cases.jsonl",
        [{x: c[x] for x in ("id", "version", "e1", "bridge", "x", "answer", "x_answer", "clean_text")} for c in cases],
    )
    write_jsonl(out_dir / "reads.jsonl", reads)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary: dict = {"n_items": len(keep), "seconds": round(time.time() - t0), "versions": {}}
    for ver in versions:
        best: dict[str, int] = {}
        for r in reads:
            if r["version"] == ver:
                best[r["id"]] = min(best.get(r["id"], 10**9), r["rank"])
        write = {}
        for a in ALPHAS:
            for kind in ("lens", "random"):
                sel = [o for o in outcomes if o["version"] == ver and o["alpha"] == a and o["kind"] == kind]
                write[f"{kind}_{a:g}"] = {"flips": statistics.mean(o["flip"] for o in sel),
                                          "flips_to_memory": statistics.mean(o["flip_mem"] for o in sel),
                                          "closed": statistics.mean(o["closed"] for o in sel)}  # fmt: skip
        summary["versions"][ver] = {"read_top10": statistics.mean(v <= 10 for v in best.values()),
                                    "read_top1": statistics.mean(v <= 1 for v in best.values()),
                                    "median_rank": statistics.median(best.values()), "write": write}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [f"# natural_rw / {name}: {len(keep)} items, layers {list(LAYERS)}", "",
             "| version | lens reads the city (top-10 / top-1) | " + " | ".join(f"a={a:g}" for a in ALPHAS) + " |",
             "|---" * (len(ALPHAS) + 2) + "|"]  # fmt: skip
    for ver, s in summary["versions"].items():
        w = s["write"]
        cells = [f"{100 * w[f'lens_{a:g}']['flips']:.0f}% ({100 * w[f'lens_{a:g}']['closed']:.0f}%) / "
                 f"{100 * w[f'random_{a:g}']['flips']:.0f}% ({100 * w[f'random_{a:g}']['closed']:.0f}%)" for a in ALPHAS]  # fmt: skip
        lines.append(
            f"| {ver} | {100 * s['read_top10']:.0f}% / {100 * s['read_top1']:.0f}% | " + " | ".join(cells) + " |"
        )
    lines += [
        "",
        "Write cells: lens | random direction: flips (share of the clean margin closed), single layers averaged.",
        "MX flips go to X's country as the prompt gives it; the lens's flips to X's real country, per alpha: "
        + json.dumps(
            {
                f"{a:g}": round(
                    summary["versions"].get("MX", {}).get("write", {}).get(f"lens_{a:g}", {}).get("flips_to_memory", 0),
                    3,
                )
                for a in ALPHAS
            }
        ),
    ]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=150)
    ap.add_argument("--layers", nargs="+", type=int, default=list(LAYERS))
    ap.add_argument("--versions", nargs="+", default=["MM", "MC"], choices=["MM", "MC", "MX"])
    args = ap.parse_args()
    LAYERS = tuple(args.layers)
    main(args.name, args.why, args.n, tuple(args.versions))
