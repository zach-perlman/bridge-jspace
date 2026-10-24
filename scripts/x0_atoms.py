"""x0_atoms (descriptive, added after data; critic's request via Dan, 24 Oct): which J++ atoms make up the bridge
edit's J++ part. For random X0 items at one layer (fixed seed), Δ at the bridge's word is fitted by signed OMP over
the J++ letter-token atoms up to 100 atoms, in selection order; ranks 1-25 and 26-100 are listed with their
coefficients (the k = 25 fit and the k = 100 fit) and marked: the bridge (org / alt), the other changed person's name,
the asked person's name, another name in the context, another word of the context, or other. The same for asked-first
items. Writes results/x0_atoms/<name>/{manifest.json, atoms.jsonl, tables.md}.

uv run python scripts/x0_atoms.py run --name x0_atoms_27b --source x0_necessity_27b_chat --layer 32   # GPU
uv run python scripts/x0_atoms.py table --name x0_atoms_27b                                            # CPU
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x0_atoms"
RESULTS = pins.RESULTS_DIR / EXP
K_MAX, K_MAIN = 100, X.K_MAIN
PICK = re.compile(r"\b([A-Z][a-z]+) picked (?:the )?([\w-]+)\.")
MARKS = ("bridge_org", "bridge_alt", "other_person", "asked_person", "name", "context", "other")


def ordered_omp(dic, x, k_max: int, k_keep: tuple[int, ...]):
    """Signed OMP of one row x [d] over the unit rows of dic, atoms in selection order (greedy |correlation| with the
    residual, least-squares refit every step). Returns the selected indices [k_max] and, per k in k_keep, the
    coefficients of the k-atom fit and its share of ||x||²."""
    import torch

    sel: list[int] = []
    resid = x.clone()
    fits = {}
    for step in range(1, k_max + 1):
        corr = dic @ resid
        if sel:
            corr[sel] = 0
        sel.append(int(corr.abs().argmax()))
        a = dic[sel]  # [step, d]
        coef = torch.linalg.lstsq(a.T, x[:, None]).solution[:, 0]
        approx = coef @ a
        resid = x - approx
        if step in k_keep:
            fits[step] = (coef.tolist(), float(approx.norm() ** 2 / x.norm() ** 2))
    return sel, fits


def people(context: str) -> dict[str, str]:
    """name -> pick, from '<Name> picked (the) <entity>.' sentences."""
    return {m.group(1): m.group(2) for m in PICK.finditer(context)}


def mark(token: str, case: dict) -> str:
    """What an atom's token is in this item: the bridge (org / alt), a name, another context word, or other."""
    w = token.strip().lower()
    if not w:
        return "other"
    org, cf = people(case["context"]), people(case["cf_context"])
    asked = next(n for n, e in org.items() if e == case["bridge"] and cf.get(n) == case["cf_bridge"])
    other = next((n for n in org if n != asked and org[n] != cf.get(n)), None)
    if w == case["bridge"].lower():
        return "bridge_org"
    if w == case["cf_bridge"].lower():
        return "bridge_alt"
    if other and w == other.lower():
        return "other_person"
    if w == asked.lower():
        return "asked_person"
    if w in {n.lower() for n in org}:
        return "name"
    if w in {t.lower() for t in re.findall(r"[A-Za-z]+", case["context"])}:
        return "context"
    return "other"


def stage_run(name: str, source: str, layer: int, n: int, seed: int) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / source
    sm = json.loads((src / "manifest.json").read_text())
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["rendering"] == "chat" and r["layer"] == layer]
    upstream = {r["scene"]: r["upstream"] for r in rows}
    scenes = sorted(upstream)
    pick_all = sorted(random.Random(seed).sample(scenes, n))
    pick_first = sorted(random.Random(seed).sample([s for s in scenes if not upstream[s]], n))
    share25 = {r["scene"]: r["share"] for r in X.read_jsonl(src / "shares.jsonl")
               if r["rendering"] == "chat" and r["layer"] == layer and (r["dict"], r["k"], r["omp"]) == X.MAIN}  # fmt: skip
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source": source,
         "source_code": sm["code"], "set": sm["set"], "layer": layer, "n": n, "seed": seed, "k_max": K_MAX,
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(),
         "note": "descriptive, added after data (critic via Dan, 24 Oct); not part of X0's rule",
         "samples": {"all": pick_all, "asked_first": pick_first}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, "jpp")
    letters = model.letter_token_ids()
    dic = lens.vectors(layer, letters)
    cases, _ = X.build_cases(model.tokenizer, sm["set"])
    by_scene = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    lines = []
    with torch.no_grad():
        for subset, picks in (("all", pick_all), ("asked_first", pick_first)):
            for s in picks:
                c = by_scene[s]
                ids = c["readers"][X.LOOKUP]["ids"]
                h = {
                    v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]]
                    for v in ("org", "alt")
                }
                x = (h["alt"] - h["org"]).float()
                sel, fits = ordered_omp(dic, x, K_MAX, (K_MAIN, K_MAX))
                case = {k: c[k] for k in ("context", "cf_context", "bridge", "cf_bridge")}
                atoms = [{"rank": i + 1, "token_id": int(letters[j]), "token": model.decoded[int(letters[j])],
                          "coef_k25": fits[K_MAIN][0][i] if i < K_MAIN else None, "coef_k100": fits[K_MAX][0][i],
                          "mark": mark(model.decoded[int(letters[j])], case)} for i, j in enumerate(sel)]  # fmt: skip
                lines.append({"subset": subset, "scene": s, "upstream": upstream[s], **case,
                              "share_k25": fits[K_MAIN][1], "share_k100": fits[K_MAX][1],
                              "source_share_k25": share25.get(s), "atoms": atoms})  # fmt: skip
    (out / "atoms.jsonl").write_text("".join(json.dumps(r) + "\n" for r in lines))
    print("wrote", out / "atoms.jsonl", flush=True)
    return out


def stage_table(name: str) -> Path:
    out = RESULTS / name
    m = json.loads((out / "manifest.json").read_text())
    rows = X.read_jsonl(out / "atoms.jsonl")
    lines = [f"# J++ atoms of the bridge edit: {name}", "",
             f"Source {m['source']} (layer {m['layer']}, set {m['set']}); {m['n']} random items and {m['n']} asked-first "
             f"items, seed {m['seed']}; signed OMP over the J++ letter-token atoms up to {m['k_max']} atoms, in selection "
             "order. Descriptive, added after data; not part of X0's rule. UNVERIFIED.", "",
             "Marks: bridge_org / bridge_alt = the asked person's pick before / after the change; other_person = the "
             "other changed person's name; asked_person; name = another person in the context; context = another word "
             "of the context; other = none of these.", ""]  # fmt: skip
    gap = [abs(r["share_k25"] - r["source_share_k25"]) for r in rows if r["source_share_k25"] is not None]
    if gap:
        lines += [f"Check: the k = 25 share here vs X0's shares.jsonl, max |difference| {max(gap):.4f} over {len(gap)} "
                  "items (same fit, recomputed).", ""]  # fmt: skip
    lines += ["## Marks by rank band (share of atoms)", "", "| subset | ranks | " + " | ".join(MARKS) + " | atoms |",
              "|" + "---|" * (len(MARKS) + 3)]  # fmt: skip
    for subset in ("all", "asked_first"):
        mine = [r for r in rows if r["subset"] == subset]
        for lo, hi in ((1, 5), (1, K_MAIN), (K_MAIN + 1, K_MAX)):
            atoms = [a for r in mine for a in r["atoms"] if lo <= a["rank"] <= hi]
            cnt = collections.Counter(a["mark"] for a in atoms)
            lines.append(f"| {subset} | {lo}-{hi} | " + " | ".join(f"{cnt[k] / len(atoms):.2f}" for k in MARKS)
                         + f" | {len(atoms)} |")  # fmt: skip
        top1 = collections.Counter(r["atoms"][0]["mark"] for r in mine)
        lines.append(f"| {subset} | rank 1 | " + " | ".join(str(top1[k]) for k in MARKS) + f" | {len(mine)} items |")
    lines += ["", "Median share of ||Δ||²: k = 25 " + f"{statistics.median(r['share_k25'] for r in rows):.3f}, k = 100 "
              f"{statistics.median(r['share_k100'] for r in rows):.3f}.", ""]  # fmt: skip
    for r in rows:
        head = (f"### {r['subset']} · {r['scene']} · {r['bridge']} → {r['cf_bridge']} · "
                f"{'upstream change' if r['upstream'] else 'asked first'} · share k=25 {r['share_k25']:.3f}")  # fmt: skip
        fmt = lambda a, key: f"`{a['token']!r}` {a[key]:+.2f} ({a['mark']})"  # noqa: E731
        lines += [head, "", f"Context: {r['context']}", "",
                  "Ranks 1-25 (k = 25 fit): " + "; ".join(fmt(a, "coef_k25") for a in r["atoms"][:K_MAIN]), "",
                  "Ranks 26-100 (k = 100 fit): " + "; ".join(fmt(a, "coef_k100") for a in r["atoms"][K_MAIN:]), ""]  # fmt: skip
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    print(out / "tables.md")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "table"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--source", default="x0_necessity_27b_chat")
    ap.add_argument("--layer", type=int, default=32)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, a.source, a.layer, a.n, a.seed)
    stage_table(a.name)


if __name__ == "__main__":
    main()
